"""SWE2-AUDIT-SPEC: reproduce ASTRA's two refusal controls in THIS directory (the packet's control writes into the packet),
plus (a) a positive baseline - the unmutated copy must succeed, else refusals prove nothing - and (b) sensitivity
mutations of the instructions the reported guard polarity rests on, in the copied continuation source:
  sete->setne at 0059ECE1, cmp eax,1 -> cmp eax,0 at 0059ECDE, shr r15d,6 -> shr r15d,5 at 0059ECB5.
A reducer that checks the polarity it reports must refuse each; exit 0 with a result means the claim is unpinned.
First pass (ASTRA's copy set = source_pins only) is kept as 'pins-only-baseline' to show the copy set is incomplete."""
import hashlib, json, pathlib, shutil, subprocess, sys
HERE = pathlib.Path(__file__).resolve().parent
W = HERE.parents[2] / "_experiments" / "evidence" / "phyretext-pointer-key-binding"
REPO = HERE.parents[4]
r = json.loads((W / "softedges-pointer-key-binding-result-03.json").read_text())
driver = W / "reduce-softedges-pointer-key-binding.py"
print("reducer sha matches result03:", r["checker_sha256"] == hashlib.sha256(driver.read_bytes()).hexdigest())
out = HERE / "controls"
if out.exists(): shutil.rmtree(out)   # created by this script only
out.mkdir()
CONT = "softedges-member-resolution-continuation-code-01.json"
def mutate(s, pc, field, old, new):
    p = s / CONT; j = json.loads(p.read_text()); n = 0
    for q in j["ranges"]:
        for x in q["instructions"]:
            if x["pc"] == pc and x[field] == old: x[field] = new; n += 1
    p.write_text(json.dumps(j) + "\n"); return n
CASES = [("pins-only-baseline", None), ("baseline", None), ("missing-guard-source", None), ("wrong-count-base", None),
         ("sete-to-setne", ("0x59ece1", "mnemonic", "sete", "setne")),
         ("cmp1-to-cmp0", ("0x59ecde", "args", "eax, 1", "eax, 0")),
         ("bit6-to-bit5", ("0x59ecb5", "args", "r15d, 6", "r15d, 5"))]
for name, mut in CASES:
    c = out / name; s = c / "source"; s.mkdir(parents=True)
    for item in r["source_pins"]:
        p = s / item["path"]; p.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / item["path"], p)
    if name != "pins-only-baseline":   # the reducer also opens the retained asset, which source_pins does not list
        a = "softedges-resource-source-01/phyretext.fx.phyre"; (s / a).parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(W / a, s / a)
    note = ""
    if name == "missing-guard-source":
        (s / "softedges-array-terminal-guard-source-01/original-code.json").unlink()
    elif name == "wrong-count-base":
        p = s / "softedges-header-membership-code-01.json"; j = json.loads(p.read_text())
        x = next(x for q in j["ranges"] for x in q["instructions"] if x["pc"] == "0x59cd07")
        x["args"] = "r9d, dword ptr [r14 + 0x14]"; p.write_text(json.dumps(j) + "\n")
    elif mut:
        note = "mutated=%d" % mutate(s, *mut)
    a = subprocess.run([sys.executable, str(driver), str(c / "result.json"), str(s)], cwd=REPO, capture_output=True, timeout=120)
    ok = (c / "result.json").exists()
    last = (a.stdout + a.stderr).decode(errors="replace").strip().splitlines()[-1:] or [""]
    tail = last[0].split("No such file or directory: ")[-1][-110:]
    print("%-20s exit=%d result=%-5s %-10s | %s" % (name, a.returncode, ok, note, tail))
    if ok and name != "baseline":
        g = json.loads((c / "result.json").read_text()).get("guard_correction", "")
        print("   guard_correction still reads:", g[:120])
