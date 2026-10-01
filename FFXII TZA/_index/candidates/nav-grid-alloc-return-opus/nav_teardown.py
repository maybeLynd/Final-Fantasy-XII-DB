"""nav_teardown.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-NAV-GRID-TEARDOWN (_experiments/evidence/nav-grid-teardown-boundary/), written without ASTRA's code, and the
update of OPUS's NavGridParams / NavSlotPointerArray release cells (NavGridParams said 'no free of the previous base was
located on this pass ... the release may sit in the caller or in an arena reset, neither of which was read').

  T  00392710 (45 B): rcx = [02AEE0A0] (NavGridParams +0x40, the heap block's base); when it is non-null, call 003844F0; then
     memset(02AEE060, 0, 0x460) as a tail jump to 00861EC0 (VCRUNTIME140 memset). The clear spans [02AEE060, 02AEE4C0): the
     whole 0x60-byte NavGridParams block and the first 0x400 bytes from 02AEE0C0, where NavSlotPointerArray's head is
  R  003844F0 is `jmp 003697F0`, and 003697F0 is the null-safe raw release: test rcx / je ret / xor edx, edx / jmp 00369860
  C  00392710's one direct caller is 002341D5, inside 002341C0 - the area-teardown reset battery the unload path runs
     (002695DD calls it) - right after 00383A20 (Navigation_ClearDataset) and 00306570(0)
  M  mutant controls on copies of the image: the release guard je -> jne, and the clear length 0x460 -> 0x60, both make T fail
  Not established: that every rebuild (003924B0) is preceded by this teardown (so no leak on a repeated rebuild), what 00369860
  does natively, the table's capacity (0x400 bytes clears 128 qwords; that is not a proven element bound), and the clear of the
  run-state root 02AEDFB0, which lies outside this range.
  S  REGRESSION: both release cells carry the route (FAILS before)
Usage: python nav_teardown.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [(d[pe + 24 + opt + i * 40:pe + 24 + opt + i * 40 + 8].rstrip(b"\0"),) + struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
def off(v):
    for nm, vs, va, rs, ro in SECS:
        if B + va <= v < B + va + rs: return v - B - va + ro
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(buf, a):
    x = next(cs.disasm(buf[off(a):off(a) + 16], a)); m = re.search(r"rip ([+-]) (0x[0-9a-f]+|\d+)", x.op_str)   # capstone prints small displacements in decimal
    return x.mnemonic, x.op_str, (x.address + x.size + (1 if m.group(1) == "+" else -1) * int(m.group(2), 0)) if m else None
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def T(buf):
    A = lambda a, v: at(buf, a)[:2] == v
    return (at(buf, 0x392714)[0] == "mov" and at(buf, 0x392714)[2] == 0x2AEE0A0 and A(0x39271B, ("test", "rcx, rcx")) and A(0x39271E, ("je", "0x392725"))
            and A(0x392720, ("call", "0x3844f0")) and A(0x392725, ("xor", "edx, edx")) and at(buf, 0x392727)[0] == "lea" and at(buf, 0x392727)[2] == 0x2AEE060
            and A(0x39272E, ("mov", "r8d, 0x460")) and A(0x392738, ("jmp", "0x861ec0")))
check("T", T(d) and at(d, 0x861EC0)[2] == 0x8C2A60, "00392710: release [02AEE0A0] when non-null, then memset(02AEE060, 0, 0x460) through 00861EC0")
check("R", at(d, 0x3844F0)[:2] == ("jmp", "0x3697f0") and [at(d, a)[:2] for a in (0x3697F0, 0x3697F3, 0x3697F5, 0x3697F7, 0x3697FC)]
      == [("test", "rcx, rcx"), ("je", "0x3697fc"), ("xor", "edx, edx"), ("jmp", "0x369860"), ("ret", "")],
      "003844F0 -> 003697F0: null-safe, 00369860(ptr, 0)")
text = next(s for s in SECS if s[0] == b".text"); tlo = B + text[2]; callers = []
for i in range(off(tlo), off(tlo) + text[3] - 5):
    if d[i] in (0xE8, 0xE9) and tlo + i - off(tlo) + 5 + struct.unpack_from("<i", d, i + 1)[0] == 0x392710: callers.append(tlo + i - off(tlo))
check("C", callers == [0x2341D5] and [at(d, a)[:2] for a in (0x2341C9, 0x2341D0, 0x2341D5)] == [("call", "0x383a20"), ("call", "0x306570"), ("call", "0x392710")]
      and at(d, 0x2695DD)[:2] == ("call", "0x2341c0"), "one caller, 002341D5 in the area-teardown battery 002341C0 (after 00383A20); 002695DD calls the battery")
m1 = bytearray(d); k = off(0x39271E); assert m1[k] == 0x74; m1[k] = 0x75
m2 = bytearray(d); k2 = off(0x39272E) + 2; assert struct.unpack_from("<I", m2, k2)[0] == 0x460; struct.pack_into("<I", m2, k2, 0x60)
check("M", not T(bytes(m1)) and not T(bytes(m2)), "mutants rejected: guard je -> jne; clear length 0x460 -> 0x60")
TY = os.path.join(DB, "_types", "types.tsv"); REC = "_index/candidates/nav-grid-alloc-return-opus/nav_teardown.py"
GP = (" || RELEASE ROUTE READ 2026-09-28 (OPUS, %s T R C M; ASTRA nav-grid-teardown-boundary): the area-teardown battery 002341C0 "
      "(the unload path, 002695DD) calls 00392710, which releases the heap block at +0x40 through 003844F0 -> 003697F0 (null-safe, "
      "00369860(ptr, 0)) when it is non-null, then clears 0x460 bytes from 02AEE060 - this whole block and the first 0x400 bytes of "
      "the pointer table at 02AEE0C0. So the block is released on area unload. Whether every rebuild by 003924B0 is preceded by this "
      "teardown (no leak on a repeated rebuild), and what 00369860 does natively, stay not established" % REC)
SP = (" || CLEARED ON AREA UNLOAD 2026-09-28 (OPUS, %s T C): 00392710's memset of [02AEE060, 02AEE4C0) zeroes 0x400 bytes from this "
      "array's head (128 qwords). That is a clear range, not a proven capacity; the elements' own lifetimes stay not established" % REC)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and REC not in c[6]: c[6] += GP; tl[i] = "\t".join(c) + e
        if c[0] == "NavSlotPointerArray" and REC not in c[6]: c[6] += SP; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8")); print("patched"); sys.exit(0)
Tt = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
check("S", GP in Tt["NavGridParams"][6] and SP in Tt["NavSlotPointerArray"][6], "both release cells carry the teardown route")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
