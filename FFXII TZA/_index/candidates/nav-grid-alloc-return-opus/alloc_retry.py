"""alloc_retry.py - OPUS (Claude Opus 5.5), 2026-09-28. STATIC, certified EXE only. Independent derivation for
ASTRA-REQ-OPUS-ALLOCATOR-RETRY-RETURN (_experiments/evidence/allocator-retry-return-domain/), written without ASTRA's code, and
the narrowing of OPUS's allocator-caller claims.

  A1 0036A190 = mov edx, 1 / jmp 0036A1A0: its only difference from a direct call is the flag 1 in edx
  A2 0036A1A0 keeps that flag in esi, tries 0036BC60 once, and on null calls the retry body 0036BFE0 with the flag stored as the
     SIXTH stack argument ([rsp+0x28] = esi at 0036A1E2) and 0 as the fifth ([rsp+0x20] at 0036A1EB); a null result skips the
     header stamping (0036A1F8 test / 0036A1FB je) and returns null
  A3 0036BFE0 (push r14 / sub rsp, 0x20, so its fifth and sixth incoming slots sit at [rsp+0x50] / [rsp+0x58]) never addresses
     either slot anywhere in its body: the flag 0036A190 sets is never read. Its final call 0036BC60 (0036C0A9) is followed by
     the diamond: a non-null result returns; a null result returns when its local edi and esi are both zero (0036C0AE..0036C0BF)
     and goes back to 0036C013 otherwise. So the local code CAN return null
  M  mutant control: 0036C0B9 jne -> je (same target) makes A3's diamond predicate fail
  C  the NavRunStateBlock copy at 00378CF6: the 0036A190 result goes to the initializer 0036C660 (00378D0B) and memcpy (00861EBA,
     00378D27) with no null test between, then the pack section 02ADCFE8 is freed (00378D33) and repointed at the copy (00378D4C)
  Not established: what the callback, reclaim and allocator do natively, or whether play ever reaches the null return.
  S  REGRESSION: the NavGridParams precondition and NavRunStateBlock's allocation cell carry this (FAILS before)
Usage: python alloc_retry.py [--patch]
"""
import hashlib, os, re, struct, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + i * 40 + 8) for i in range(n)]
off = lambda v: next(v - B - va + ro for vs, va, rs, ro in SECS if B + va <= v < B + va + rs)
cs = Cs(CS_ARCH_X86, CS_MODE_64)
def at(buf, a): x = next(cs.disasm(buf[off(a):off(a) + 16], a)); return x.mnemonic, x.op_str
def A(buf, pairs): return all(at(buf, a) == v for a, v in pairs)
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
check("A1", A(d, [(0x36A190, ("mov", "edx, 1")), (0x36A195, ("jmp", "0x36a1a0"))]), "0036A190 = edx 1, then 0036A1A0")
check("A2", A(d, [(0x36A1B4, ("mov", "esi, edx")), (0x36A1C9, ("call", "0x36bc60")), (0x36A1D3, ("test", "rax, rax")), (0x36A1D6, ("jne", "0x36a1fd")),
                  (0x36A1E2, ("mov", "dword ptr [rsp + 0x28], esi")), (0x36A1EB, ("mov", "qword ptr [rsp + 0x20], rbp")), (0x36A1F0, ("call", "0x36bfe0")),
                  (0x36A1F8, ("test", "rax, rax")), (0x36A1FB, ("je", "0x36a218")), (0x36A211, ("mov", "rax, rbx"))]),
      "0036A1A0: the flag goes out as the sixth stack argument; a null retry result skips the stamping and returns null")
def diamond(buf):
    return A(buf, [(0x36C0A9, ("call", "0x36bc60")), (0x36C0AE, ("test", "edi, edi")), (0x36C0B0, ("jne", "0x36c0c1")), (0x36C0B2, ("test", "rax, rax")),
                   (0x36C0B5, ("jne", "0x36c0ca")), (0x36C0B7, ("test", "esi, esi")), (0x36C0B9, ("jne", "0x36c013")), (0x36C0BF, ("jmp", "0x36c0ca")),
                   (0x36C0C1, ("test", "rax, rax")), (0x36C0C4, ("je", "0x36c013")), (0x36C0E4, ("ret", ""))])
body = [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x36BFE0):off(0x36C0E5)], 0x36BFE0)]
slots = [o for m, o in body if re.search(r"\[rsp \+ 0x(50|58)\]", o)]
check("A3", A(d, [(0x36BFEA, ("push", "r14")), (0x36BFEC, ("sub", "rsp, 0x20"))]) and not slots and diamond(d) and body[-1] == ("ret", ""),
      "0036BFE0 never reads [rsp+0x50] / [rsp+0x58] (%d hits); final diamond: null returns only when edi and esi are both 0" % len(slots))
mut = bytearray(d); k = off(0x36C0B9); assert mut[k:k + 2] == b"\x0f\x85"; mut[k + 1] = 0x84
check("M", not diamond(bytes(mut)), "mutant 0036C0B9 jne -> je rejected")
check("C", A(d, [(0x378CF6, ("call", "0x36a190")), (0x378D05, ("mov", "rcx, rax")), (0x378D08, ("mov", "rdi, rax")), (0x378D0B, ("call", "0x36c660")),
                 (0x378D24, ("mov", "rcx, rdi")), (0x378D27, ("call", "0x861eba")), (0x378D33, ("call", "0x3697f0"))])
      and not any(m in ("test", "cmp") and "rax" in o for m, o in [(x.mnemonic, x.op_str) for x in cs.disasm(d[off(0x378CFB):off(0x378D0B)], 0x378CFB)]),
      "00378CF6: no null test before the initializer and the memcpy")
TY = os.path.join(DB, "_types", "types.tsv"); FI = os.path.join(DB, "_types", "fields.tsv"); REC = "_index/candidates/nav-grid-alloc-return-opus/alloc_retry.py"
NARROW = (" || FAILURE PATH NARROWED 2026-09-28 (OPUS, %s A1-A3 M; ASTRA allocator-retry-return-domain): 0036A190's local code can "
          "return null. Its flag 1 reaches the retry body 0036BFE0 only as the sixth stack argument, which that body never reads, and "
          "0036BFE0 returns a null final allocation when its local edi and esi are both zero (it retries otherwise). What the "
          "callback, reclaim and allocator do natively, and whether play reaches that return, stay not established" % REC)
RUN = (" || PRECONDITION 2026-09-28 (OPUS, %s C A1-A3): the copy exists only when the allocation SUCCEEDS - 00378CF6's result goes to "
       "the initializer 0036C660 and memcpy (00861EBA) with no null test, and the pack section is then freed (00378D33) and 02ADCFE8 "
       "repointed at the result (00378D4C); 0036A190's local code can return null (0036BFE0 returns null when its local edi and esi "
       "are both zero), and whether play reaches that is not established" % REC)
def cells(l): return l.rstrip("\r\n").split("\t")
if "--patch" in sys.argv:
    tl = open(TY, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(tl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and REC not in c[4]: c[4] += NARROW; tl[i] = "\t".join(c) + e
        if c[0] == "NavRunStateBlock" and REC not in c[4]: c[4] += RUN; tl[i] = "\t".join(c) + e
    open(TY, "wb").write("".join(tl).encode("utf-8"))
    fl = open(FI, "rb").read().decode("utf-8").splitlines(keepends=True)
    for i, l in enumerate(fl):
        c = cells(l); e = l[len(l.rstrip("\r\n")):]
        if c[0] == "NavGridParams" and c[3] == "cellBitsetArray" and REC not in c[5]: c[5] += NARROW; fl[i] = "\t".join(c) + e
    open(FI, "wb").write("".join(fl).encode("utf-8")); print("patched"); sys.exit(0)
T = {cells(l)[0]: cells(l) for l in open(TY, "rb").read().decode("utf-8").splitlines()}
F = [cells(l) for l in open(FI, "rb").read().decode("utf-8").splitlines() if cells(l)[0] == "NavGridParams" and cells(l)[3] == "cellBitsetArray"]
check("S", NARROW in T["NavGridParams"][4] and RUN in T["NavRunStateBlock"][4] and F and NARROW in F[0][5],
      "NavGridParams (allocation cell, +0x40) and NavRunStateBlock (allocation cell) carry the local null domain")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
