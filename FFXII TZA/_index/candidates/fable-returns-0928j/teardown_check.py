"""teardown_check.py - ASTRA-REQ-FABLE-NAV-GRID-TEARDOWN re-derived from the certified image's bytes (FABLE, Claude Opus 5.5,
2026-09-28).

  T1 00392710 (45 B): rcx = [02AEE0A0]; test / je past the release; call 003844F0 (= jmp 003697F0, which null-tests and
     tail-jumps to 00369860 with edx = 0); then edx = 0, rcx = lea 02AEE060, r8d = 0x460, and a tail jmp to memset 00861EC0.
     The cleared range [02AEE060, 02AEE4C0) holds the 0x60-byte NavGridParams block and the 0x400 bytes after it; the root
     02AEDFB0 lies below it
  T2 an image-wide raw scan of .text (every E8 / E9 rel32 whose address starts an instruction in the linear decode from its .pdata function start) finds exactly one caller of
     00392710 (002341D5, in the area-teardown reset 002341C0) and one of the rebuild 003924B0 (0023441E, in
     BattleSystem_InitializeAreaState 002342F0)
  T3 every rip-relative qword store to 02AEE0A0 in .text is one site, 00392677 in the rebuild, which does not release a
     previous block first: the block lives from area initialisation to area unload
  C  controls: the scan finds the known call 00392720 -> 003844F0; a call-shaped byte sequence planted inside the 7-byte load at
     00392714 is a raw hit, and the boundary test (a real instruction start in the linear decode from the .pdata function
     start of the original image) rejects it
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
fails = 0
def ok(tag, cond, msg):
    global fails
    print(("PASS " if cond else "FAIL ") + tag + "  " + msg); fails += (not cond)
def body(a, n):
    return {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(a):off(a) + n], a)}
t = body(0x392710, 45); r = body(0x3844F0, 5); s = body(0x3697F0, 13)
ok("T1", t.get(0x392714, "").startswith("mov rcx, qword ptr [rip") and t[0x39271B] == "test rcx, rcx" and t[0x39271E] == "je 0x392725"
   and t[0x392720] == "call 0x3844f0" and t[0x392725] == "xor edx, edx" and t[0x392727].startswith("lea rcx, [rip") and t[0x39272E] == "mov r8d, 0x460"
   and t[0x392738] == "jmp 0x861ec0" and r[0x3844F0] == "jmp 0x3697f0" and s[0x3697F3] == "je 0x3697fc" and s[0x3697F5] == "xor edx, edx" and s[0x3697F7] == "jmp 0x369860"
   and 0x392714 + 7 + struct.unpack_from("<i", d, off(0x392714) + 3)[0] == 0x2AEE0A0 and 0x392727 + 7 + struct.unpack_from("<i", d, off(0x392727) + 3)[0] == 0x2AEE060
   and 0x2AEE060 + 0x460 == 0x2AEE4C0 and not (0x2AEE060 <= 0x2AEDFB0 < 0x2AEE4C0),
   "null-guarded release of [02AEE0A0] via 003844F0 -> 003697F0 -> 00369860 (edx 0); memset(02AEE060, 0, 0x460); root 02AEDFB0 outside")
exc_rva, exc_sz = struct.unpack_from("<II", d, pe + 24 + 112 + 8 * 3)
PD = sorted(struct.unpack_from("<II", d, off(0x120000 + exc_rva) + 12 * k) for k in range(exc_sz // 12))
def fstart(va):
    r = va - 0x120000; best = None
    for b0, e0 in PD:
        if b0 <= r: best = b0
        else: break
    return best + 0x120000
def boundary(va):
    """va starts an instruction in the ORIGINAL image's linear decode from its .pdata function start."""
    f = fstart(va); o = off(f)
    return va in {i.address for i in MD.disasm(d[o:o + (va - f) + 16], f)}
def raw_hits(target, blob=d):
    out = []
    for m in re.finditer(rb"[\xE8\xE9]", blob[T0:T0 + TN]):
        o = T0 + m.start(); va = TV + m.start()
        if va + 5 + struct.unpack_from("<i", blob, o + 1)[0] == target: out.append(va)
    return out
callers = lambda target, blob=d: [va for va in raw_hits(target, blob) if boundary(va)]
C1, C2 = callers(0x392710), callers(0x3924B0)
own = lambda va: max(a for a in (0x2341C0, 0x2342F0) if a <= va)
ok("T2", C1 == [0x2341D5] and C2 == [0x23441E] and own(0x2341D5) == 0x2341C0 and own(0x23441E) == 0x2342F0,
   "callers of 00392710: %s; of 003924B0: %s" % (["%08X" % x for x in C1], ["%08X" % x for x in C2]))
stores = []
for m in re.finditer(rb"\x48\x89[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]|\x4C\x89[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]", d[T0:T0 + TN]):
    o = T0 + m.start(); va = TV + m.start()
    if va + 7 + struct.unpack_from("<i", d, o + 3)[0] == 0x2AEE0A0:
        ins = next(MD.disasm(d[o:o + 7], va), None)
        if ins and ins.size == 7 and ins.mnemonic == "mov": stores.append(va)
ok("T3", stores == [0x392677], "rip-relative qword stores to 02AEE0A0 in .text: %s" % ["%08X" % x for x in stores])
blob = bytearray(d); po = off(0x392717)                     # plant E8 rel32(00392710) inside the load at 00392714
blob[po] = 0xE8; blob[po + 1:po + 5] = struct.pack("<i", 0x392710 - (0x392717 + 5))
raw = raw_hits(0x392710, bytes(blob))
ok("C", 0x392720 in callers(0x3844F0) and 0x392717 in raw and 0x392717 not in callers(0x392710, bytes(blob)),
   "known positive 00392720 -> 003844F0 found; a planted call-shaped sequence at 00392717 is a raw hit %s and is rejected by the boundary test %s"
   % (0x392717 in raw, 0x392717 not in callers(0x392710, bytes(blob))))
print("FAILS", fails); sys.exit(1 if fails else 0)
