"""yebis_preset.py - the UC-1 body 00712180: ASTRA's selector coupling re-derived, and its semantic context (FABLE, Claude Opus 5.5,
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
  C  controls: a planted call to 006DAA30 is found by the R1 scan; the S1 scan finds the setter's own three table references
"""
import hashlib, os, re, struct, sys
import capstone
EXE = os.environ.get('FFXII_EXE', 'C:/Users/Kristian/source/repos/XIIOnline/Database/Tools/work/exe/FFXII_TZA.exe')
d = open(EXE, 'rb').read()
if hashlib.sha256(d).hexdigest() != '73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8':
    print('REFUSED  not the certified image')
    sys.exit(2)
pe = struct.unpack_from('<I', d, 60)[0]
ns = struct.unpack_from('<H', d, pe + 6)[0]
opt = struct.unpack_from('<H', d, pe + 20)[0]
SECS = []
for i in range(ns):
    o = pe + 24 + opt + 40 * i
    SECS.append((d[o:o + 8].rstrip(b'\x00'),) + struct.unpack_from('<IIII', d, o + 8))
off = lambda v: next((ra + v - 1179648 - va for n, vs, va, rs, ra in SECS if va <= v - 1179648 < va + rs))
text = next((s for s in SECS if s[0] == b'.text'))
T0, TV, TN = (text[4], text[2] + 1179648, text[3])
MD = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
exc_rva, exc_sz = struct.unpack_from('<II', d, pe + 24 + 112 + 8 * 3)
PD = sorted((struct.unpack_from('<II', d, off(1179648 + exc_rva) + 12 * k) for k in range(exc_sz // 12)))
fails = 0

def ok(tag, cond, msg):
    global fails
    print(('PASS ' if cond else 'FAIL ') + tag + '  ' + msg)
    fails += not cond

def fstart(va):
    r = va - 1179648
    best = None
    for b0, e0 in PD:
        if b0 <= r:
            best = b0
        else:
            break
    return None if best is None else best + 1179648

def boundary(va, img=d):
    f = fstart(va)
    if f is None:
        return False
    return va in {i.address for i in MD.disasm(img[off(f):off(f) + (va - f) + 16], f)}

def refs(target, img=d):
    b = img[T0:T0 + TN]
    out = []
    for m in re.finditer(b'[\\xE8\\xE9]', b):
        va = TV + m.start()
        if va + 5 + struct.unpack_from('<i', b, m.start() + 1)[0] == target and boundary(va, img):
            out.append(('rel32', va))
    for m in re.finditer(b'\\x0F[\\x80-\\x8F]', b):
        va = TV + m.start()
        if va + 6 + struct.unpack_from('<i', b, m.start() + 2)[0] == target and boundary(va, img):
            out.append(('jcc32', va))
    for m in re.finditer(b'[\\x70-\\x7F\\xEB]', b):
        va = TV + m.start()
        if va + 2 + struct.unpack_from('<b', b, m.start() + 1)[0] == target and boundary(va, img):
            out.append(('jcc8', va))
    for m in re.finditer(b'[\\x48\\x4C]\\x8D[\\x05\\x0D\\x15\\x1D\\x25\\x2D\\x35\\x3D]', b):
        va = TV + m.start()
        if va + 7 + struct.unpack_from('<i', b, m.start() + 3)[0] == target:
            out.append(('lea', va))
    for label, pat in (('u64', struct.pack('<Q', target)), ('u32va', struct.pack('<I', target)), ('u32rva', struct.pack('<I', target - 1179648))):
        for n, vs, va, rs, ra in SECS:
            for m in re.finditer(re.escape(pat), img[ra:ra + rs]):
                out.append((label, va + m.start() + 1179648))
    return out
