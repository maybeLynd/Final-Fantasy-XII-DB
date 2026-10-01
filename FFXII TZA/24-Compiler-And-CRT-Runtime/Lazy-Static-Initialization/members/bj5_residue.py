"""bj5_residue.py - BJ-5's residue: the lazy-static holders that call neither atexit nor a reflection routine and are
in neither published family, rebuilt from the image and classified one by one (FABLE, Claude Opus 5.5, 2026-09-26).

Controls (the page's published figures, which must come back exactly before anything is classified):
  707 holders (bodies calling _Init_thread_header 008092FC), 526 reaching atexit 00808B90 by call or jmp,
  535 reaching a Phyre.Reflection.* routine, complement 107, and 30 once both family member lists are removed.
Classification of each residual holder, from its own body (intra-body jumps excluded):
  PAIR    - writes two .data globals exactly 8 bytes apart (a {tagged pointer, 0} pair)
  TABLE   - calls cosf / sinf / powf (or their forwarders): a computed constant table
  OTHER   - neither; printed with size, external callees and the globals it writes, for reading
Writes bj5-residue.tsv beside this script.
"""
import csv, struct, sys, re
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
from capstone.x86 import X86_OP_MEM, X86_OP_IMM

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
d = (ROOT / "Database/Tools/work/exe/FFXII_TZA.exe").read_bytes()
BASE = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]
opt = struct.unpack_from("<H", d, pe + 20)[0]
secs = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
names = [d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0").decode() for i in range(n)]
def off(v):
    for vs, va, rs, ro in secs:
        if BASE + va <= v < BASE + va + rs: return v - BASE - va + ro
def sec_of(v):
    for (vs, va, rs, ro), nm in zip(secs, names):
        if BASE + va <= v < BASE + va + max(vs, rs): return nm
cs = Cs(CS_ARCH_X86, CS_MODE_64); cs.detail = True
rows = list(csv.reader(open(ROOT / "Database/Tools/work/graph/functions.tsv", encoding="utf-8"), delimiter="\t"))[1:]
F = {}
for r in rows:
    try: F[int(r[0], 16)] = (r[1], int(r[2]), r[8] if len(r) > 8 else "")
    except ValueError: pass
GUARD, ATEXIT = 0x8092FC, 0x808B90
REFL = {a for a, (nm, sz, tag) in F.items() if "Phyre.Reflection" in tag}
MATH = {a for a, (nm, sz, tag) in F.items() if re.fullmatch(r"(cosf|sinf|powf|cos|sin|pow|acosf|atan2f|sqrtf)", nm)}
def scan(a, sz):
    ext, writes = set(), []
    for x in cs.disasm(d[off(a):off(a) + sz], a):
        if x.mnemonic in ("call", "jmp") and x.operands and x.operands[0].type == X86_OP_IMM:
            t = x.operands[0].imm
            if not (a <= t < a + sz): ext.add(t)
        if x.operands and x.operands[0].type == X86_OP_MEM and cs.reg_name(x.operands[0].mem.base) == "rip" \
                and x.mnemonic in ("mov", "movups", "movaps", "movsd", "movss", "and", "or"):
            writes.append(x.address + x.size + x.operands[0].mem.disp)
    return ext, writes
holders = {}
for a, (nm, sz, tag) in F.items():
    if sz <= 0 or off(a) is None: continue
    ext, w = scan(a, sz)
    if GUARD in ext: holders[a] = (ext, w)
atx = {a for a, (e, w) in holders.items() if ATEXIT in e}
refl = {a for a, (e, w) in holders.items() if e & REFL}
comp = sorted(set(holders) - atx - refl)
fams = set()
for f in ("descriptor-pair-accessors.tsv", "magic-static-pair-initialisers.tsv"):
    for r in csv.reader(open(HERE / f, encoding="utf-8"), delimiter="\t"):
        if r and re.fullmatch(r"[0-9A-Fa-f]{8}", r[0]): fams.add(int(r[0], 16))
res = [a for a in comp if a not in fams]
print("controls: holders %d (707)  atexit %d (526)  reflection %d (535)  complement %d (107)  residue %d (30)"
      % (len(holders), len(atx), len(refl), len(comp), len(res)))
ok = (len(holders), len(atx), len(refl), len(comp), len(res)) == (707, 526, 535, 107, 30)
# The nine that are neither PAIR nor TABLE were read by hand; each reading is checked here from the bytes.
def guarded(a):
    """Instructions between the guard's _Init_thread_header call and its _Init_thread_footer call."""
    L = list(cs.disasm(d[off(a):off(a) + F[a][1]], a))
    i = next((k for k, x in enumerate(L) if x.mnemonic == "call" and x.op_str == "0x8092fc"), None)
    if i is None: return []
    j = next((k for k in range(i + 1, len(L)) if L[k].mnemonic == "call" and L[k].op_str == "0x80929c"), len(L))
    return ["%s %s" % (x.mnemonic, x.op_str) for x in L[i + 1:j]]
def cstr(a, s):
    m = re.search(r"rip \+ (0x[0-9a-f]+)", s)
    return None
def hand(a):
    g = guarded(a)
    calls = [s for s in g if s.startswith("call ")]
    if calls == ["call 0x5cda30"] and any(s.startswith("mov qword ptr [rip") and s.endswith(", rax") for s in g):
        return "CACHED_PTR"       # caches the Phyre::PTTYCallback singleton 005CDA30 returns (vtable 00D360A0)
    if calls == ["call 0x18a620"] and "add rax, 8" in g:
        return "CACHED_PTR"       # caches 0018A620() + 8
    if calls == ["call 0x6ccd80"]:
        return "NAMED_RECORD"     # 006CCD80 builds {name, 0, 0, 0}; the names are PCollisionGroup / PRigidBodyType
    if not calls and any(s.startswith("movss dword ptr [rip") for s in g):
        return "COMPUTED_CONST"   # one float computed inline and stored
    if [s for s in g if not s.startswith(("cmp ", "jne ", "lea rcx"))] == []:
        return "EMPTY_GUARD"      # header, the -1 test, then the footer: nothing initialised in between
    return "OTHER"
out = []
for a in res:
    ext, w = holders[a]
    data = sorted({g for g in w if sec_of(g) == ".data"})
    pair = any(g + 8 in data for g in data)
    tbl = bool(ext & MATH)
    cls = "TABLE" if tbl else "PAIR" if pair else hand(a)
    callees = sorted(F[t][0] if t in F else "%08X" % t for t in ext - {GUARD, 0x80929C})
    out.append((a, F[a][1], cls, len(data), ",".join(callees[:6])))
with open(HERE / "bj5-residue.tsv", "w", encoding="utf-8", newline="") as f:
    f.write("# bj5_residue.py - the 30 residual lazy-static holders, classified from their own bodies\n")
    f.write("entry\tbytes\tclass\tdata_globals_written\texternal_callees\n")
    for a, sz, cls, nd, cl in out: f.write("%08X\t%d\t%s\t%d\t%s\n" % (a, sz, cls, nd, cl))
from collections import Counter
print(Counter(c for _, _, c, _, _ in out))
for a, sz, cls, nd, cl in out:
    if cls == "OTHER": print("OTHER %08X %4d B  globals %d  callees %s" % (a, sz, nd, cl))
print("CONTROLS", "PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
