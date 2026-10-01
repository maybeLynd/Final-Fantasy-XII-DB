"""SWE2-AUDIT-SPEC: compare every instruction in the field-extent packet's four retained code captures with the
shipping EXE (bytes + fresh capstone decode), and probe whether the reducer notices a bytes-only change of the
copy-source displacement at 001EA5C1 with the span hash recomputed and the text kept (disposable copy)."""
import hashlib, json, pathlib, shutil, subprocess, sys, tempfile
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
P = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\phyretext-softedges-field-extent")
S = P / "softedges-resource-source-01"
CAPS = ["original-code-raw-01.json", "array-binding-code-01.json", "member-bridge-code-01.json", "constructor-source-retained-01.json"]
n = bb = bt = 0
for c in CAPS:
    for q in json.loads((S / c).read_text())["ranges"]:
        for x in q["instructions"]:
            pc = int(x["pc"], 16); z = bytes.fromhex(x["bytes"]); o = tk.off(pc); n += 1
            if tk.d[o:o + len(z)] != z: bb += 1; print("BYTE MISMATCH", c, x["pc"])
            y = next(md.disasm(tk.d[o:o + 16], pc), None)
            if y is None or (y.mnemonic, y.op_str) != (x["mnemonic"], x["args"]): bt += 1; print("TEXT MISMATCH", c, x["pc"], x["mnemonic"], x["args"], y and (y.mnemonic, y.op_str))
print("captured instructions %d; byte mismatches vs EXE %d; text mismatches vs fresh decode %d" % (n, bb, bt))
T = pathlib.Path(r"C:\t\auditspec"); tmp = pathlib.Path(tempfile.mkdtemp(prefix="fe-gap-", dir=str(T)))
dd = tmp / "src"; shutil.copytree(S, dd)
p = dd / CAPS[0]; r = json.loads(p.read_text()); hit = 0
for q in r["ranges"]:
    for x in q["instructions"]:
        if int(x["pc"], 16) == 0x1EA5C1: x["bytes"] = "4c8d96c8090000"; hit = 1   # lea r10,[rsi+0x9c8], text kept '[rsi + 0x118]'
    q["sha256"] = hashlib.sha256(b"".join(bytes.fromhex(x["bytes"]) for x in q["instructions"])).hexdigest()
p.write_text(json.dumps(r)); out = tmp / "MUST-NOT-EXIST.json"
rr = subprocess.run([sys.executable, "-B", str(P / "reduce-softedges-field-extent.py"), str(dd), str(out)], capture_output=True, text=True, timeout=60)
print("bytes-only 001EA5C1 disp 0x118->0x9c8 (patched=%d): exit=%d result=%s | %s" % (hit, rr.returncode, out.exists(), (rr.stdout.strip() or rr.stderr.strip())[-110:]))
shutil.rmtree(tmp); print("disposable dir removed:", not tmp.exists())
