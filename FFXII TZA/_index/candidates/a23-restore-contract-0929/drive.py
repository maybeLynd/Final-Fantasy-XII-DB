"""A23 restore receipt (OPUS, 2026-09-29, on ASTRA-REQ-OPUS-A23-WINDOWS-SNAPSHOT-RESTORE). Native host-format evidence only.
Against the exact candidate ZIP g20260929T213407Z-9c7238 (sha256 23256f18...157c7):
  NEG  ZipFile.extractall into a fresh folder, then the ordinary reader (generation.Store.open_generation): reproduces
       ASTRA's five refusals (the `pkg:` inputs extract as `pkg_`)
  POS  generation.restore_zip into a fresh folder, then the ordinary reader: clean, CURRENT set, every manifest input
       present at its portable name with the manifest's bytes
  REF  restoring into the (now non-empty) POS folder again is refused
Writes only beneath this directory; refuses to reuse an existing fixture."""
import hashlib, json, os, sys, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "Database", "Tools", "analysis-kit", "gfz-scripts"))
import generation as G  # noqa: E402
ZIP = os.path.join(ROOT, "Database", "Tools", "work", "dashboard-exports", "g20260929T213407Z-9c7238.zip")
neg, pos = os.path.join(HERE, "fixture-extractall"), os.path.join(HERE, "fixture-restore")
for d in (neg, pos):
    if os.path.exists(d):
        raise SystemExit("REFUSING: fixture exists: %s" % d)
zsha = G.sha256_file(ZIP)
label, info = G.verify_zip(ZIP)
with zipfile.ZipFile(ZIP) as z:
    man = json.loads(z.read(G.MANIFEST))
    gen = man["generation"]
    z.extractall(os.path.join(neg, gen))
msha = hashlib.sha256(open(os.path.join(neg, gen, G.MANIFEST), "rb").read()).hexdigest()
_, _, neg_probs = G.Store(neg).open_generation(gen, msha)
restored = G.restore_zip(ZIP, pos)
pman, pdir, pos_probs = G.Store(pos).open_current()
colon = sorted(n for n in man["inputs"] if G.snapshot_name(n) != n)
byte_ok = all(G.sha256_file(G.input_file(pdir, n)) == c["sha256"] for n, c in man["inputs"].items()
              if c["state"] in ("present", "empty") and not c.get("external"))
try:
    G.restore_zip(ZIP, pos); again = None
except G.GenerationError as e:
    again = str(e)
res = {"zip": os.path.relpath(ZIP, ROOT).replace("\\", "/"), "zip_sha256": zsha, "verify_zip": [label, info],
       "generation": gen, "generation_module_sha256": G.sha256_file(G.__file__), "python": sys.version,
       "escaped_inputs": colon, "escaped_file_names": [G.snapshot_name(n) for n in colon],
       "NEG_extractall_reader_problems": neg_probs, "POS_restore_generation": restored, "POS_reader_problems": pos_probs,
       "POS_inputs_byte_exact": byte_ok, "REF_second_restore": again}
ok = (zsha.startswith("23256f18") and label == "VERIFIED" and len([p for p in neg_probs if "input snapshot" in p]) == len(colon) == 5
      and restored == gen and pos_probs == [] and byte_ok and again and "non-empty" in again)
res["verdict"] = "PASS" if ok else "FAIL"
json.dump(res, open(os.path.join(HERE, "result.json"), "w"), indent=1)
print(res["verdict"], "| NEG problems %d | POS problems %d | escaped %d | refuse-again: %s" % (len(neg_probs), len(pos_probs), len(colon), bool(again)))
raise SystemExit(0 if ok else 1)
