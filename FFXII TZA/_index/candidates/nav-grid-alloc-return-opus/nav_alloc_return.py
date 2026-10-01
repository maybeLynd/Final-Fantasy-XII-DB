"""nav_alloc_return.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-NAV-GRID-ALLOC-RETURN (_experiments/evidence/nav-grid-allocation-return-boundary/), written without ASTRA's code,
and the qualification of OPUS's NavGridParams consumers.

  W  the wrapper 00384580 (104 B): size in ecx -> ebx; 0036C1D0(4, r9d) and 0036C1A0(6); 0036A190(ecx = size); rbx = rax;
     test / je over 0036C660(rax, rsi, edi) - the initializer runs only for a non-null result; then 0036C110 and 0036C140;
     returns rax = rbx. So a null from 0036A190 comes back as null (rbx is callee-saved across the two calls under the Win64 ABI;
     their bodies are not read here)
  K  the caller 003924B0: ebx = the computed size; mov ecx, ebx / call 00384580 (0039266A); then movsxd r8, ebx (0039266F),
     xor edx, edx, mov rcx, rax, mov [02AEE0A0], rax (00392677), call 00861EC0 (0039267E) = jmp [008C2A60] = VCRUNTIME140 memset.
     No test of rax between the call and the memset, and the base is stored (NavGridParams +0x40) BEFORE it is cleared
  X  width: the allocator receives the size as the 32-bit ecx (how 0036A190 treats it beyond 32 bits is not read here), the clear
     receives movsxd r8, ebx - the same low 32 bits sign-extended; the two agree for sizes below 2^31
  M  mutant controls on copies of the image: flipping the wrapper's je (0x74) to jne makes W fail; changing the caller's
     `mov rcx, rax` to `mov rcx, rbx` makes K fail
  So the heap block is a SUCCESSFUL-ALLOCATION precondition of the builder, not a state it guarantees: on a null return it
  publishes null at +0x40 and passes null to memset. What 0036A190 does on failure (null, fault, abort) is not established here.
  S  REGRESSION: NavGridParams' allocation cell and its +0x40 row carry the qualification (FAILS before)
Usage: python nav_alloc_return.py [--patch]
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
def imp_name(slot):
    ir = struct.unpack_from("<I", d, pe + 24 + 0x78)[0]   # import directory RVA (PE32+ data directory 1)
    i = off(ir + B)
    while True:
        oft, ts, fc, name, ft = struct.unpack_from("<IIIII", d, i)
        if not name: return None
        k = 0
        while True:
            thunk = struct.unpack_from("<Q", d, off(oft + B) + 8 * k)[0]   # the lookup (name) table entry for IAT slot ft + 8k
            if not thunk: break
            if ft + B + 8 * k == slot and not thunk >> 63:
                return d[off(name + B):off(name + B) + 32].split(b"\0")[0], d[off((thunk & 0x7FFFFFFF) + B) + 2:off((thunk & 0x7FFFFFFF) + B) + 40].split(b"\0")[0]
            k += 1
        i += 20
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
def W(buf):
    A = lambda a, v: at(buf, a)[:2] == v
    return (A(0x384592, ("mov", "ebx, ecx")) and A(0x3845AE, ("mov", "ecx, ebx")) and A(0x3845B0, ("call", "0x36a190")) and A(0x3845B5, ("mov", "rbx, rax"))
            and A(0x3845B8, ("test", "rax, rax")) and A(0x3845BB, ("je", "0x3845cb")) and A(0x3845C3, ("mov", "rcx, rax")) and A(0x3845C6, ("call", "0x36c660"))
            and A(0x3845CB, ("call", "0x36c110")) and A(0x3845D0, ("call", "0x36c140")) and A(0x3845DA, ("mov", "rax, rbx")) and A(0x3845E7, ("ret", "")))
def K(buf):
    A = lambda a, v: at(buf, a)[:2] == v
    return (A(0x392668, ("mov", "ecx, ebx")) and A(0x39266A, ("call", "0x384580")) and A(0x39266F, ("movsxd", "r8, ebx")) and A(0x392672, ("xor", "edx, edx"))
            and A(0x392674, ("mov", "rcx, rax")) and at(buf, 0x392677)[0] == "mov" and at(buf, 0x392677)[1].endswith("], rax") and at(buf, 0x392677)[2] == 0x2AEE0A0
            and A(0x39267E, ("call", "0x861ec0")))
check("W", W(d), "00384580 returns 0036A190's result; its initializer 0036C660 is skipped for null")
mem = at(d, 0x861EC0)
check("K", K(d) and mem[0] == "jmp" and imp_name(mem[2]) == (b"VCRUNTIME140.dll", b"memset"),
      "003924B0: no test between 00384580 and memset; +0x40 (02AEE0A0) is stored before the clear; 00861EC0 -> %s" % (imp_name(mem[2]),))
check("X", at(d, 0x392668)[:2] == ("mov", "ecx, ebx") and at(d, 0x3845AE)[:2] == ("mov", "ecx, ebx") and at(d, 0x39266F)[:2] == ("movsxd", "r8, ebx"),
      "allocation size = 32-bit ecx; clear length = movsxd of the same low 32 bits")
m1 = bytearray(d); assert m1[off(0x3845BB)] == 0x74; m1[off(0x3845BB)] = 0x75
m2 = bytearray(d); assert bytes(m2[off(0x392674):off(0x392674) + 3]) == b"\x48\x8b\xc8"; m2[off(0x392674):off(0x392674) + 3] = b"\x48\x8b\xcb"
check("M", not W(bytes(m1)) and not K(bytes(m2)), "mutants rejected: wrapper je->jne; caller mov rcx, rax -> mov rcx, rbx")
TY = os.path.join(DB, "_types", "types.tsv"); FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-grid-alloc-return-opus/nav_alloc_return.py"
Q = (" || PRECONDITION 2026-09-28 (OPUS, %s W K X; ASTRA nav-grid-allocation-return-boundary): the heap block exists only when the "
     "allocation SUCCEEDS. 00384580 returns 0036A190's result unchanged and skips its initializer for null; 003924B0 stores the result "
     "at +0x40 (02AEE0A0) and passes it to memset with no null test, the store before the clear. A null return would be published "
     "and cleared; what 0036A190 does on failure is not established. The size reaches the allocator as the 32-bit ecx and the clear "
     "as its sign extension, which agree below 2^31" % REC)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and REC not in c[4]: c[4] += Q; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8"))
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[3] == "cellBitsetArray" and REC not in c[5]: c[5] += Q; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams" and cells(l)[3] == "cellBitsetArray"]
check("S", REC in T["NavGridParams"][4] and len(F) == 1 and REC in F[0][5] and "SUCCEEDS" in F[0][5],
      "NavGridParams' allocation cell and +0x40 row state the successful-allocation precondition")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
