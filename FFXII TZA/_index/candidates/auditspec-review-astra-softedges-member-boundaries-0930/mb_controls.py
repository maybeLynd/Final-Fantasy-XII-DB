"""SWE2-AUDIT-SPEC controls for phyretext-member-boundaries (nothing is written into the packet).
(A) every instruction in the four retained captures is compared byte-for-byte with the shipping EXE, and its
    mnemonic/args with a fresh capstone decode of those EXE bytes (closes the checker's text-trust gap for the
    shipped captures);
(B) actual CLI runs of the packet checker on disposable copies under C:\\t\\auditspec, including a bytes-only
    mutation with the span hash recomputed and the text left unchanged (probes what the checker can see)."""
import hashlib, json, pathlib, shutil, subprocess, sys, tempfile
sys.path.insert(0, r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\FABLE\takebacks")
import tk
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
md = Cs(CS_ARCH_X86, CS_MODE_64)
P = pathlib.Path(r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_experiments\evidence\phyretext-member-boundaries")
CAPS = ["softedges-elements-callback-source-01/original-code.json", "softedges-member-assignment-code-01.json",
        "softedges-member-resolution-code-01.json", "softedges-member-resolution-continuation-code-01.json"]
n = bad_b = bad_t = 0
for c in CAPS:
    r = json.loads((P / c).read_text())
    for q in r["ranges"]:
        for x in q["instructions"]:
            pc = int(x["pc"], 16); z = bytes.fromhex(x["bytes"]); o = tk.off(pc); n += 1
            if tk.d[o:o + len(z)] != z: bad_b += 1; print("BYTE MISMATCH", c, x["pc"])
            y = next(md.disasm(tk.d[o:o + 16], pc), None)
            if y is None or (y.mnemonic, y.op_str) != (x["mnemonic"], x["args"]) or y.size != len(z):
                bad_t += 1; print("TEXT MISMATCH", c, x["pc"], x["mnemonic"], x["args"], "| exe:", y and (y.mnemonic, y.op_str))
print("(A) captured instructions %d; byte mismatches vs EXE %d; mnemonic/args mismatches vs fresh decode %d" % (n, bad_b, bad_t))
lf = tk.d[tk.off(0x60F3D0):tk.off(0x60F3D0) + 33].hex(); cbk = tk.d[tk.off(0x60F280):tk.off(0x60F280) + 16].hex()
print("    checker's hardcoded dispatcher bytes == EXE:", lf == "488b41704d8bd04c8bda4885c0740c458bc1498bd2498bcb48ffe0b815000000c3",
      "; callback bytes == EXE:", cbk == "4883ec28e857fdffff33c04883c428c3")
T = pathlib.Path(r"C:\t\auditspec"); T.mkdir(parents=True, exist_ok=True)
tmp = pathlib.Path(tempfile.mkdtemp(prefix="mb-cli-", dir=str(T)))
def copy(dd):
    shutil.copytree(P, dd, ignore=shutil.ignore_patterns("softedges-member-boundaries-controls-01", "*.py", "softedges-member-boundaries-result-*", "softedges-resource-source-01"))
def patch_insn(dd, cap, pc, newbytes=None, newargs=None):
    p = dd / cap; r = json.loads(p.read_text())
    for q in r["ranges"]:
        hit = False
        for x in q["instructions"]:
            if int(x["pc"], 16) == pc:
                if newbytes: x["bytes"] = newbytes
                if newargs is not None: x["args"] = newargs
                hit = True
        if hit: q["sha256"] = hashlib.sha256(b"".join(bytes.fromhex(x["bytes"]) for x in q["instructions"])).hexdigest()
    p.write_text(json.dumps(r))
def cli(name, alter, expect):
    dd = tmp / "".join(ch if ch.isalnum() else "_" for ch in name); copy(dd); alter(dd); out = dd / "MUST-NOT-EXIST.json"
    r = subprocess.run([sys.executable, "-B", str(P / "check-softedges-member-boundaries.py"), str(dd), str(out)], capture_output=True, text=True, timeout=60)
    tail = (r.stderr.strip().splitlines() or [r.stdout.strip()])[-1][:95]
    print("(B) %-44s exit=%d result=%s expected=%s | %s" % (name, r.returncode, out.exists(), expect, tail))
cli("unchanged copy", lambda d: None, "pass")
cli("missing callback source", lambda d: shutil.rmtree(d / "softedges-elements-callback-source-01"), "refuse")
def incomplete(d):
    p = d / CAPS[3]; r = json.loads(p.read_text()); r["ranges"] = r["ranges"][:-1]; p.write_text(json.dumps(r))
cli("continuation missing its last range", incomplete, "refuse")
cli("callback xor eax,eax -> 2-byte nop (hash recomputed)", lambda d: patch_insn(d, CAPS[0], 0x60F289, "6690"), "refuse")
cli("dispatcher null return 0x15 -> 0x16 (hash recomputed)", lambda d: patch_insn(d, CAPS[0], 0x60F3EB, "b816000000"), "refuse")
cli("59ED3F args text eax -> rax", lambda d: patch_insn(d, CAPS[3], 0x59ED3F, None, "rax, [rdx + rbx]"), "refuse")
cli("59ED42 BYTES add rax,r13 -> add eax,r13d, text kept", lambda d: patch_insn(d, CAPS[3], 0x59ED42, "4401e8"), "GAP probe")
cli("60EFFD BYTES mov eax,5 -> mov eax,0, text kept", lambda d: patch_insn(d, CAPS[1], 0x60EFFD, "b800000000"), "GAP probe")
shutil.rmtree(tmp); print("disposable dir removed:", not tmp.exists())
