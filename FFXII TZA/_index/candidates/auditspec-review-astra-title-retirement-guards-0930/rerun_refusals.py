"""SWE2-AUDIT-SPEC: re-run the packet's positive checker and its two CLI refusal cases, plus one extra control, in a
scratch dir outside the repo (the packet's control-title-retirement-inputs.py writes into the packet, so it is not run).
python rerun_refusals.py <scratch-dir> > rerun_refusals.out
"""
import sys, subprocess, shutil, pathlib, json, hashlib
ROOT = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline")
P = ROOT / "Database/FFXII TZA/_experiments/evidence/title-retirement-local-guards"
SRC = P / "section04-title-member-source"
HERE = pathlib.Path(__file__).resolve().parent
S = pathlib.Path(sys.argv[1]); S.mkdir()
drv = P / "prove-title-retirement-guards.py"
def run(tag, source, out):
    r = subprocess.run([sys.executable, str(drv), str(out), str(source)], capture_output=True, text=True, cwd=str(ROOT))
    last = (r.stderr.strip().splitlines() or [""])[-1][:110]
    print("%-28s exit=%d result_exists=%s  %s" % (tag, r.returncode, out.exists(), last if r.returncode else r.stdout.strip()[:90]))
    return r.returncode
# positive, into the review dir
pos = HERE / "rerun_result.json"
if pos.exists(): pos.unlink()
run("positive", SRC, pos)
a = json.loads(pos.read_text()); b = json.loads((P / "title-retirement-local-guards-result-02.json").read_text())
print("positive vs title-retirement-local-guards-result-02.json: identical=%s; differing keys=%s" % (a == b, sorted(k for k in set(a) | set(b) if a.get(k) != b.get(k))))
# case 1: missing manifest
c = S / "missing-manifest"; shutil.copytree(SRC, c); (c / "original_body_manifest.json").unlink()
run("missing-manifest", c, S / "m1.json")
# case 2: same-line-count changed mask text (the packet's mutation)
c = S / "same-count-changed-mask"; shutil.copytree(SRC, c); p = c / "original_disassembly.txt"; z = p.read_text()
old = "0024A6D1 25003f0000               and      eax, 0x3f00"; assert z.count(old) == 1
p.write_text(z.replace(old, old.replace("0x3f00", "0x3f20")))
run("same-count-changed-mask", c, S / "m2.json")
# extra (reviewer): does the semantic need() gate itself refuse, independent of the hash pin? Patch the checker copy's
# pins to the mutated file's hashes so only need(0x24a6d1,'and','eax, 0x3f00') can catch the change.
c2 = S / "need-gate-only"; shutil.copytree(c, c2 / "src")
drv2 = c2 / "prove.py"; t = drv.read_text()
h = lambda q: hashlib.sha256(q.read_bytes()).hexdigest()
t = t.replace("ca93837847ed6efdc72a7ee26d8457324fc44ef06dddcfe60ffcf43c4aad1c57", h(c2 / "src" / "original_disassembly.txt"))
t = t.replace("W=pathlib.Path(__file__).resolve().parent;ROOT=W.parents[4]", "W=pathlib.Path(__file__).resolve().parent;ROOT=pathlib.Path(%r)" % str(ROOT))
drv2.write_text(t)
r = subprocess.run([sys.executable, str(drv2), str(c2 / "m3.json"), str(c2 / "src")], capture_output=True, text=True)
print("%-28s exit=%d result_exists=%s  %s" % ("need-gate-only (reviewer)", r.returncode, (c2 / "m3.json").exists(), (r.stderr.strip().splitlines() or [""])[-1][:110]))
