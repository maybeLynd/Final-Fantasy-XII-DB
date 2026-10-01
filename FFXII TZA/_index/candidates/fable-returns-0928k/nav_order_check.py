"""nav_order_check.py - ASTRA-REQ-FABLE-NAV-ROOT-CALL-ORDER re-derived from the certified image's bytes (FABLE, Claude Opus 5.5,
2026-09-28).

  O1 the area-teardown reset 002341C0 (62 B) calls, with no branch before 002341D5: 0030FE60, 00383A20, 00306570 (ecx 0),
     then 00392710 - so on its normal entry the dataset pointer is cleared before the grid is torn down, and 00306570 runs
     between them
  O2 00383A20 (12 B) is 'mov qword [02AEDFB0], 0 / ret': Navigation_ClearDataset
  O3 an image-wide census of E8 / E9 rel32 callers of 00383A20 (each a real instruction start in the linear decode from its
     .pdata function start), so the page does not imply the teardown reset is the only clear
  C  controls: the order check reports the reverse when the two call targets are swapped in memory; the census finds the
     known call 002341C9
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get("FFXII_EXE", r"C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe")
d = open(EXE, "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8": print("REFUSED  not the certified image"); sys.exit(2)
pe = struct.unpack_from("<I", d, 0x3c)[0]; ns = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
SECS = []
for i in range(ns):
    o = pe + 24 + opt + 40 * i
    SECS.append((d[o:o + 8].rstrip(b"\0"), ) + struct.unpack_from("<IIII", d, o + 8))
off = lambda v: next(ra + v - 0x120000 - va for n, vs, va, rs, ra in SECS if va <= v - 0x120000 < va + rs)
text = next(s for s in SECS if s[0] == b".text"); T0, TV, TN = text[4], text[2] + 0x120000, text[3]
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
exc_rva, exc_sz = struct.unpack_from("<II", d, pe + 24 + 112 + 8 * 3)
PD = sorted(struct.unpack_from("<II", d, off(0x120000 + exc_rva) + 12 * k) for k in range(exc_sz // 12))
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def fstart(va):
    r = va - 0x120000; best = None
    for b0, e0 in PD:
        if b0 <= r: best = b0
        else: break
    return best + 0x120000
def boundary(va):
    f = fstart(va); o = off(f)
    return va in {i.address for i in MD.disasm(d[o:o + (va - f) + 16], f)}
def callers(target):
    out = []
    for m in re.finditer(rb"[\xE8\xE9]", d[T0:T0 + TN]):
        o = T0 + m.start(); va = TV + m.start()
        if va + 5 + struct.unpack_from("<i", d, o + 1)[0] == target and boundary(va): out.append(va)
    return out
def order(img):
    ins = list(MD.disasm(img[off(0x2341C0):off(0x2341C0) + 62], 0x2341C0))
    seq, branch_before = [], False
    for i in ins:
        if i.mnemonic == "call": seq.append((i.address, int(i.op_str, 16)))
        if i.mnemonic.startswith("j") and i.address < 0x2341D5: branch_before = True
    tg = [t for a, t in seq]
    return tg, branch_before, (tg.index(0x383A20) < tg.index(0x392710)) if 0x383A20 in tg and 0x392710 in tg else None
tg, br, clear_first = order(d)
ok("O1", tg[:4] == [0x30FE60, 0x383A20, 0x306570, 0x392710] and not br and clear_first,
   "calls in order %s; branch before 002341D5: %s" % (["%08X" % t for t in tg], br))
leaf = [(i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x383A20):off(0x383A20) + 12], 0x383A20)]
ok("O2", leaf == ["mov qword ptr [rip + 0x276a585], 0", "ret"] and 0x383A20 + 11 + 0x276A585 == 0x2AEDFB0, "00383A20 = qword [02AEDFB0] = 0; ret")
C3 = callers(0x383A20)
ok("O3", 0x2341C9 in C3, "callers of 00383A20: %s" % ["%08X in %08X" % (c, fstart(c)) for c in C3])
sw = bytearray(d)
def put(a, t): o = off(a); sw[o + 1:o + 5] = struct.pack("<i", t - (a + 5))
put(0x2341C9, 0x392710); put(0x2341D5, 0x383A20)
ok("C", order(bytes(sw))[2] is False and 0x2341C9 in C3, "swapped targets read as teardown-first: %s" % (order(bytes(sw))[2] is False))
print("FAILS", fails); sys.exit(1 if fails else 0)
