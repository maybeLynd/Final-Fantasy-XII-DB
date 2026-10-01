"""rv_controls.py - SWE2-AUDIT-SPEC reviewer controls for the spattack remap checker (2026-09-30).

usage: python rv_controls.py SCRATCH_DIR   (fresh dir outside the packet; the packet is only read)

Runs the packet's own prove-spattack-word-roundtrip.py, with only its W/ROOT input line re-pointed (the packet's own
exercise script does the same), against inputs mutated to carry one defect each:
  failed01_asis     the real failed capture invalid-output-writer-01/inner-capture.json as the writer input
  failed01_forged   the same capture plus wrapper_complete=True and the current writer-driver hash
  mnemonic_only     30EEB2 'add' -> 'sub' in the retained listing, bytes untouched
  bytes_consistent  30DBDA imm 0xD0 -> 0xCF in the listing bytes AND the span sha rebuilt to match the listing
"""
import hashlib, json, pathlib, shutil, subprocess, sys

PKT = pathlib.Path(__file__).resolve().parents[3] / "_experiments/evidence/spattack-native-word-remap"
ROOT = PKT.parents[4]
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=False)
text = (PKT / "prove-spattack-word-roundtrip.py").read_text()
line = "W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]"
assert text.count(line) == 1
INPUTS = ["capture-index-path.py", "effective-and-script-id-raw-01.json", "capture-effective-and-script-id.py",
          "spattack-output-writers-raw-02.json", "capture-spattack-output-writers.py",
          "spattack-queue-reader-raw-01.json", "capture-spattack-queue-reader.py",
          "spattack-info-raw-01.json", "capture-spattack-info.py",
          "spattack-leaves-and-guard-raw-01.json", "capture-spattack-leaves-and-guard.py"]
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()


def run(case, mutate):
    f = out / case
    f.mkdir()
    for n in INPUTS:
        shutil.copyfile(PKT / n, f / n)
    mutate(f)
    s = f / "checker-input-adapted.py"
    s.write_text(text.replace(line, "W=pathlib.Path(" + repr(str(f)) + ");ROOT=pathlib.Path(" + repr(str(ROOT)) + ")"))
    r = subprocess.run([sys.executable, "-B", str(s), str(f / "result.json")], cwd=ROOT, capture_output=True,
                       text=True, timeout=60)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    print("%-17s exit=%d result=%s  %s" % (case, r.returncode, (f / "result.json").exists(),
                                           last if r.returncode else r.stdout.strip()))


def failed01(forge):
    def m(f):
        cap = json.loads((PKT / "invalid-output-writer-01/inner-capture.json").read_text())
        print("  failed01 capture spans:", [(x["start"], x["end_exclusive"]) for x in cap["ranges"]])
        if forge:
            cap["wrapper_complete"] = True
            cap["invocation_driver_sha256"] = sha(PKT / "capture-spattack-output-writers.py")
        (f / "spattack-output-writers-raw-02.json").write_text(json.dumps(cap, indent=2) + "\n")
    return m


def mnemonic_only(f):
    p = f / "effective-and-script-id-raw-01.json"
    r = json.loads(p.read_text())
    n = 0
    for s in r["ranges"]:
        for i in s["instructions"]:
            if i["pc"] == "0x30eeb2":
                i["mnemonic"] = "sub"
                n += 1
    assert n == 1
    p.write_text(json.dumps(r, indent=2) + "\n")


def bytes_consistent(f):
    p = f / "spattack-leaves-and-guard-raw-01.json"
    r = json.loads(p.read_text())
    n = 0
    for s in r["ranges"]:
        hit = False
        for i in s["instructions"]:
            if i["pc"] == "0x30dbda":
                assert i["bytes"] == "2dd0000000", i["bytes"]
                i["bytes"] = "2dcf000000"
                i["args"] = "eax, 0xcf"
                hit = True
                n += 1
        if hit:
            s["sha256"] = hashlib.sha256(bytes.fromhex("".join(i["bytes"] for i in s["instructions"]))).hexdigest()
    assert n == 1
    p.write_text(json.dumps(r, indent=2) + "\n")


run("positive", lambda f: None)
run("failed01_asis", failed01(False))
run("failed01_forged", failed01(True))
run("mnemonic_only", mnemonic_only)
run("bytes_consistent", bytes_consistent)
