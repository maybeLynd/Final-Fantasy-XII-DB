"""yebis_preset2.py - (v2, on ASTRA-REQ-FABLE-PRESET-BOUNDARY-BINDING: the boundary test decodes the image it is given, and every gate forwards it) the UC-1 body 00712180: ASTRA's selector coupling re-derived, and its semantic context (FABLE, Claude Opus 5.5,
2026-09-28, on ASTRA-REQ-FABLE-PRESET-SELECTOR-COUPLING). Decoded from the certified image's bytes; nothing is executed.

  P1 the branches: a null target returns it untouched; selector 1 (edx) negative skips, else min(edx, 7) picks an 8-byte row of
     01F3C5B0 -> +0x4C, +0x54; selector 2 (r8d) negative skips selectors 2 AND the fallback, else min(r8d, 10 or 0x13 by the byte
     00D9F05E) picks a 0x1C-byte row of 01F3C5F0 -> +0x7C, +0x84, +0x88, +0xCC, +0x8C, +0xE4, +0xE8, loading row + 0x10 into edx; selector
     3 (r9d) negative then takes edx (0071222A) - the second row's +0x10 - and only a still-negative value skips; min(r9d, 9) picks
     a 0x38-byte row of 01F3C820 -> +0x90 .. +0xC4
  P2 the coupling is live in the data: every second-table row's +0x10 (all 20 rows) is a non-negative index 1..5, so a selected
     second row with a negative third selector always copies a third-table row
  R1 the body's only entry is the 5-byte thunk 006DAA30 (jmp 00712180), and nothing in the image reaches the thunk or the body:
     no E8 / E9 / jcc rel32 or rel8 at a real instruction start, no rip-relative lea, no u64 VA, u32 VA or u32 RVA in any section
  S1 the semantic context: the third table's only other code reference is 0070288A, in 006FF900 - the YEBIS CPostEffect member
     populate the post-processing contract routes to - which copies a 0x38-byte row by index (r12d) into its frame at +0x410..
     as the alternative to caller-supplied values (+0x3E4..): the three tables are YEBIS post-effect parameter presets, and
     00712180 is a library preset setter that FFXII's code never calls
  C  controls: a real call planted at 00712090 is found; the same call bytes hidden at 00712095 inside a 10-byte mov rax, imm64 are
     rejected, because the boundary test decodes the image it is given; the S1 scan finds its four table references
  Scope of R1: the literal reference forms listed, each gated by the nearest-.pdata linear-decode boundary test. A computed, encoded
     or out-of-image entry is not searched and not excluded
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
    return None if best is None else best + 0x120000
def boundary(va, img=d):
    """va starts an instruction in the linear decode of img from the nearest .pdata function start at or below va."""
    f = fstart(va)
    if f is None: return False
    return va in {i.address for i in MD.disasm(img[off(f):off(f) + (va - f) + 16], f)}
B = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x712180):off(0x712180) + 353], 0x712180)}
rip = lambda a: min(x for x in B if x > a) + int(re.search(r"rip \+ 0x(\w+)\]", B[a]).group(1), 16)
ok("P1", B[0x712186] == "je 0x7122dd" and B[0x71218E] == "js 0x7121b3" and B[0x712190] == "mov eax, 7" and rip(0x712195) == 0x1F3C5B0
   and B[0x7121B6] == "js 0x71222d" and rip(0x7121B8) == 0xD9F05E and B[0x7121BF] == "mov eax, 0xa" and B[0x7121C4] == "mov ecx, 0x13"
   and B[0x7121D5] == "imul rcx, rax, 0x1c" and rip(0x7121D9) == 0x1F3C5F0 and B[0x712207] == "mov edx, dword ptr [rcx + 0x10]"
   and B[0x712228] == "jns 0x712236" and B[0x71222A] == "mov r9d, edx" and B[0x712230] == "js 0x7122dd" and B[0x712236] == "mov eax, 9"
   and B[0x712244] == "imul rcx, rax, 0x38" and rip(0x712248) == 0x1F3C820 and B[0x7122E0] == "ret",
   "caps 7 / 10 or 0x13 / 9; a negative selector 3 takes the second row's +0x10 at 0071222A; a negative selector 2 skips both")
rows = [struct.unpack_from("<i", d, off(0x1F3C5F0) + 0x1C * k + 0x10)[0] for k in range(20)]
ok("P2", all(1 <= v <= 5 for v in rows), "second-table +0x10 over 20 rows: %s" % rows)
blob = d[T0:T0 + TN]
def refs(target, img=d):
    b = img[T0:T0 + TN]; out = []
    for m in re.finditer(rb"[\xE8\xE9]", b):
        va = TV + m.start()
        if va + 5 + struct.unpack_from("<i", b, m.start() + 1)[0] == target and boundary(va, img): out.append(("rel32", va))
    for m in re.finditer(rb"\x0F[\x80-\x8F]", b):
        va = TV + m.start()
        if va + 6 + struct.unpack_from("<i", b, m.start() + 2)[0] == target and boundary(va, img): out.append(("jcc32", va))
    for m in re.finditer(rb"[\x70-\x7F\xEB]", b):
        va = TV + m.start()
        if va + 2 + struct.unpack_from("<b", b, m.start() + 1)[0] == target and boundary(va, img): out.append(("jcc8", va))
    for m in re.finditer(rb"[\x48\x4C]\x8D[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]", b):
        va = TV + m.start()
        if va + 7 + struct.unpack_from("<i", b, m.start() + 3)[0] == target: out.append(("lea", va))
    for label, pat in (("u64", struct.pack("<Q", target)), ("u32va", struct.pack("<I", target)), ("u32rva", struct.pack("<I", target - 0x120000))):
        for n, vs, va, rs, ra in SECS:
            for m in re.finditer(re.escape(pat), img[ra:ra + rs]): out.append((label, va + m.start() + 0x120000))
    return out
thunk = [(i.mnemonic, i.op_str) for i in MD.disasm(d[off(0x6DAA30):off(0x6DAA30) + 5], 0x6DAA30)]
r_thunk, r_body = refs(0x6DAA30), refs(0x712180)
ok("R1", thunk == [("jmp", "0x712180")] and r_thunk == [] and r_body == [("rel32", 0x6DAA30)],
   "thunk %s; references to the thunk %s; to the body %s" % (thunk, r_thunk, [(k, "%08X" % a) for k, a in r_body]))
def table_refs(lo, hi):
    out = []
    for m in re.finditer(rb"[\x48\x4C]\x8D[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]", blob):
        va = TV + m.start(); t = va + 7 + struct.unpack_from("<i", blob, m.start() + 3)[0]
        if lo <= t < hi and boundary(va): out.append((va, t))
    return out
tr = table_refs(0x1F3C5B0, 0x1F3C820 + 10 * 0x38)
F = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x702879):off(0x702879) + 0x70], 0x702879)}
want = {(0x712195, 0x1F3C5B0), (0x7121D9, 0x1F3C5F0), (0x712248, 0x1F3C820), (0x70288A, 0x1F3C820)}
ok("S1", set(tr) == want and fstart(0x70288A) == 0x6FF900 and F[0x702886] == "imul rcx, rax, 0x38" and F[0x702896] == "mov dword ptr [rbp + 0x410], eax",
   "table lea references: %s; 0070288A is in %08X and copies a 0x38-byte row by index to its frame" % ([("%08X" % a, "%08X" % t) for a, t in sorted(tr)], fstart(0x70288A)))
pl = bytearray(d); o = off(0x712090); pl[o:o + 5] = bytes([0xE8]) + struct.pack("<i", 0x6DAA30 - (0x712090 + 5))      # a real call at a start
planted = [a for k, a in refs(0x6DAA30, bytes(pl)) if k == "rel32"]
hid = bytearray(d); o = off(0x712090)                                                                   # the call hidden in an imm64
hid[o:o + 10] = bytes([0x48, 0xB8, 0, 0, 0, 0xE8]) + struct.pack("<i", 0x6DAA30 - (0x712095 + 5))
hid_hits = [a for k, a in refs(0x6DAA30, bytes(hid)) if k == "rel32"]
hid_decode = next(MD.disasm(bytes(hid)[o:o + 16], 0x712090))
ok("C", planted == [0x712090] and hid_decode.mnemonic == "movabs" and hid_decode.size == 10 and 0x712095 not in hid_hits and len(tr) == 4,
   "a real call planted at 00712090 is found %s; the same call hidden at 00712095 inside a 10-byte %s is rejected %s; S1 finds 4 table references"
   % (["%08X" % a for a in planted], hid_decode.mnemonic, 0x712095 not in hid_hits))
print("FAILS", fails); sys.exit(1 if fails else 0)
