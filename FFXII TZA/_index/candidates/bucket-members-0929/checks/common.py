"""common.py - shared helpers for the agentB bucket checks (read-only).
EXE: the shipping image (SHA256 checked); EXTRACT: the full game extract. check(name, cond, detail) prints PASS/FAIL
and counts failures; finish() prints the FAILS line and exits non-zero on failure."""
import hashlib, os, struct, sys, glob
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
EXE = r"C:\Users\Kristian\source\repos\XIIOnline\Database\Tools\work\exe\FFXII_TZA.exe"
SHA = "73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8"
EXTRACT = "D:/FFXII_TZA_extract"
BASE = 0x120000
d = open(EXE, "rb").read()
_pe = struct.unpack_from("<I", d, 0x3C)[0]; _ns = struct.unpack_from("<H", d, _pe + 6)[0]; _opt = struct.unpack_from("<H", d, _pe + 20)[0]
secs = []
for _i in range(_ns):
    _o = _pe + 24 + _opt + _i * 40
    _vs, _va, _rs, _ro = struct.unpack_from("<IIII", d, _o + 8)
    secs.append((d[_o:_o + 8].rstrip(b"\0").decode(), BASE + _va, _vs, _ro, _rs))
def off(a):
    for nm, va, vs, ro, rs in secs:
        if va <= a < va + vs: return ro + (a - va) if a - va < rs else None
def q(a): o = off(a); return struct.unpack_from("<Q", d, o)[0] if o is not None else None
def cstr(a):
    o = off(a)
    if o is None: return None
    return d[o:d.index(b"\0", o)].decode("latin1")
md = Cs(CS_ARCH_X86, CS_MODE_64)
def ins_at(a):
    o = off(a); x = next(md.disasm(d[o:o + 16], a, 1), None)
    return f"{x.mnemonic} {x.op_str}" if x else None
def rip_target(a):
    """resolved rip-relative target of the instruction at a (None if not rip-relative)"""
    o = off(a); x = next(md.disasm(d[o:o + 16], a, 1))
    s = x.op_str
    for sep, sg in (("rip + ", 1), ("rip - ", -1)):
        if sep in s:
            return x.address + x.size + sg * int(s.split(sep)[1].split("]")[0], 16)
    return None
KIND_ARRAYS = {2: 0x1E4D830, 9: 0x1E4DAD0, 7: 0x1E4D830 + 450 * 8}   # first-language-arm arrays (002DF9A0)
def kind_path(kind, idx): p = q(KIND_ARRAYS[kind] + 8 * idx); return cstr(p) if p else None
def copies(pattern): return sorted(glob.glob(os.path.join(EXTRACT, pattern).replace("\\", "/"), recursive=True))
FAILS = 0; CHECKS = 0
def check(name, cond, detail=""):
    global FAILS, CHECKS
    CHECKS += 1
    if not cond: FAILS += 1
    print(f"  [{'PASS' if cond else 'FAIL'}] {name}" + (f" -- {detail}" if detail else ""))
def expect_ins(a, *subs):
    s = ins_at(a) or ""
    check(f"{a:08X} decodes as {' & '.join(subs)!r}", all(x in s for x in subs), s)
def header():
    check("EXE SHA256", hashlib.sha256(d).hexdigest().upper() == SHA)
def finish():
    print(f"CHECKS {CHECKS}  FAILS {FAILS}")
    sys.exit(1 if FAILS else 0)
