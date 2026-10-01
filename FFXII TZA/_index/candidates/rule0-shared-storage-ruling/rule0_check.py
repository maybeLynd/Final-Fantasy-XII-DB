"""rule0_check.py - the facts behind FABLE's shared-storage clause for rule 0 (Claude Opus 5.5, 2026-09-28, on
OPUS-NOTICE-FABLE-RULE0-SHARED-STORAGE-AB30). Decoded from the certified image's bytes.

  R1 00273A20 is 'xor eax, eax / cmp qword [rcx], rax / setne al / ret': it asks only whether the storage holds a live widget
     (a non-null +0), which both occupants of singleton + 0xAB30 satisfy - it does not say which one
  R2 in 002906D0 the read of singleton + 0xB240 (= 0xAB30 + 0x710) at 002906FF runs when 00273A20 returned 1 and BEFORE the
     bit-0x2000 test at 00290707: nothing on its path says which occupant it reads
  R3 the other two +0x710 accesses are proven: 00290630 tests bit 0x2000 (00290640) and liveness before its tail jump to 00296490
     (002964BA); 00290680 does the same (00290694) before its tail jump to 00296960 (0029696A), which the 0x720 widget's installed
     handler 002985D0 also calls (002986B4) - the handler that 00296940 installs (lea r8 at 00296943 -> 002985D0)
  R4 bit 0x2000 of + 0x10F68 is set by one literal write, 00290726, right after 00290713 builds the 0x720 widget (00296940, edx
     0x720), and cleared by one literal write, 00290617 ('and 0xFFFFDFFF'); the other writers store a whole register value and
     are listed, not resolved
  C  control: the dominance test used for R2 / R3 reports the bit test as dominating at 002964BA (via 00290630) and not at
     002906FF, so it separates the two cases rather than passing both
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = [struct.unpack_from("<IIII", d, pe + 24 + opt + 40 * i + 8) for i in range(ns)]
off = lambda v: next(ra + v - 0x120000 - va for vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def body(a, n): return [(i.address, (i.mnemonic + " " + i.op_str).strip()) for i in MD.disasm(d[off(a):off(a) + n], a)]
def upto(a, n, stop):
    out = []
    for x, s in body(a, n):
        out.append((x, s))
        if x == stop: break
    return out
L = [s for x, s in body(0x273A20, 9)]
ok("R1", L == ["xor eax, eax", "cmp qword ptr [rcx], rax", "setne al", "ret"], "00273A20: %s" % L)
def bit_test_before(entry, n, access):
    """straight-line: is a 'test dword [reg + 0x10f68], 0x2000' seen on the fall-through path before the access?"""
    for x, s in upto(entry, n, access):
        if x == access: return False
        if re.match(r"test dword ptr \[r\w+ \+ 0x10f68\], 0x2000$", s): return True
    return False
P = dict(body(0x2906D0, 0x6A))
ok("R2", P[0x2906EE] == "call 0x273a20" and P[0x2906FA] == "cmp eax, 1" and P[0x2906FD] == "jne 0x290707"
   and P[0x2906FF] == "cmp dword ptr [rcx + 0xb240], eax" and P[0x290707] == "test dword ptr [rcx + 0x10f68], 0x2000"
   and not bit_test_before(0x2906D0, 0x6A, 0x2906FF),
   "002906FF reads +0xB240 after the liveness test and before the bit test at 00290707")
A = dict(body(0x290630, 0x48)); B = dict(body(0x290680, 0x50)); H = dict(body(0x2985D0, 0xF0)); W = dict(body(0x296940, 0x14))
ok("R3", A[0x290640] == "test dword ptr [rcx + 0x10f68], 0x2000" and A[0x29066F] == "jmp 0x296490" and dict(body(0x296490, 0x40))[0x2964BA] == "mov dword ptr [rbx + 0x710], 1"
   and B[0x290694] == "test dword ptr [rcx + 0x10f68], 0x2000" and B[0x2906C5] == "jmp 0x296960" and dict(body(0x296960, 0x14))[0x29696A] == "cmp dword ptr [rcx + 0x710], 0"
   and H.get(0x2986B4) == "call 0x296960" and W[0x29694A] == "mov edx, 0x720" and W[0x296943].startswith("lea r8, [rip") and 0x29694A + 0x1C86 == 0x2985D0
   and bit_test_before(0x290630, 0x48, 0x29066F) and bit_test_before(0x290680, 0x50, 0x2906C5),
   "002964BA and 0029696A are reached behind the bit test or from the widget's own handler 002985D0")
C = r"C:/Users/Kristian/AppData/Local/Temp/claude/C--Users-Kristian-source-repos/3c89ec72-2988-46c1-ba7b-44218ae1bb19/scratchpad/y1p_all.txt"
writes = []
# image-wide: every literal 'and / or / xor / mov dword [reg + 0x10f68], ...' over the function bodies that write the flag word
pat = re.compile(rb"[\x81\x83][\x80-\xBF]\x68\x0F\x01\x00|\x89[\x80-\xBF]\x68\x0F\x01\x00|\x31[\x80-\xBF]\x68\x0F\x01\x00|\x21[\x80-\xBF]\x68\x0F\x01\x00|\x09[\x80-\xBF]\x68\x0F\x01\x00")
tsec = [s for s in SECS if s[1] <= 0x2906D0 - 0x120000 < s[1] + s[2]][0]
T0, TV, TN = tsec[3], tsec[1] + 0x120000, tsec[2]
for m in pat.finditer(d[T0:T0 + TN]):
    va = TV + m.start()
    for back in (0, 1):
        ins = next(MD.disasm(d[off(va - back):off(va - back) + 16], va - back), None)
        if ins and "0x10f68" in ins.op_str and ins.mnemonic in ("and", "or", "xor", "mov"):
            writes.append((va - back, (ins.mnemonic + " " + ins.op_str).strip())); break
lit_set = [(a, s) for a, s in writes if s.startswith("or") and re.search(r", (0x[0-9a-f]+)$", s) and int(re.search(r", (0x[0-9a-f]+)$", s).group(1), 16) & 0x2000]
lit_clr = [(a, s) for a, s in writes if s.startswith("and") and re.search(r", (0x[0-9a-f]+)$", s) and not int(re.search(r", (0x[0-9a-f]+)$", s).group(1), 16) & 0x2000]
regw = [(a, s) for a, s in writes if not re.search(r", (0x[0-9a-f]+|\d+)$", s)]
ok("R4", [a for a, s in lit_set] == [0x290726] and [a for a, s in lit_clr] == [0x290617] and P[0x29071A] == "call 0x296940",
   "literal set %s; literal clear %s; whole-register writes (not resolved) %s" % (["%08X" % a for a, s in lit_set], ["%08X" % a for a, s in lit_clr], ["%08X" % a for a, s in regw]))
ok("C", bit_test_before(0x290630, 0x48, 0x29066F) is True and bit_test_before(0x2906D0, 0x6A, 0x2906FF) is False,
   "the dominance test separates the proven site from the unproven one")
print("FAILS", fails); sys.exit(1 if fails else 0)
