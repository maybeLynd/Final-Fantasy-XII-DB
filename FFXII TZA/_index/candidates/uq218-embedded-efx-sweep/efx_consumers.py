"""efx_consumers.py - UQ-218: does anything but the stub read the @FEF entry's embedded EFX0010 payload? (FABLE, Claude Opus 5.5,
2026-09-28). An image-wide sweep of the certified image, including the jcc / thunk edges the earlier sweep did not run.

  E0 the binder path's only consumer, 0016D6A0, is C2 00 00 (ret 0); the binder 00504940 forms the payload pointer
     (@FEF entry + 0x30) from the entry it stores at rec + 0x230 (005049A7) and passes it there
  E1 the effect-instance builders have one caller each, both in the name-keyed spawn path 00409FE0: 003B38B0 (0040A174) and
     003B3B10 (0040A1C4); counted over every E8 / E9 rel32, jcc rel32 and rel8, and rip-relative lea in .text, each at a real
     instruction start (linear decode from its .pdata function start), plus raw u64 pointers in the data sections
  E2 the '@FEF' tag 0x46454640 is an immediate at exactly three code sites: the spawn path's presence gate 0040A0A4 and the
     render-record binder 00504F00 (00504F78, 00504FCE)
  E3 over every .pdata function body, no qword read of [R + 0x230] has the render record's shape on the same base register R
     (word [R + 0x228], dword [R + 0x238] or qword [R + 0x1F8], widths anchored); the two partial matches are listed and are
     not the render record
  C  controls: the same fingerprint over qword WRITES of [R + 0x230] finds the binder 00504940 with all three fields (so a reader
     of that shape would be seen); the tag scan finds the binder's two sites
  Not claimed: a reader through a copied pointer or a base the fingerprint cannot see, or any native effect of the dispatcher.
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
def boundary(va):
    f = fstart(va)
    if f is None: return False
    o = off(f)
    return va in {i.address for i in MD.disasm(d[o:o + (va - f) + 16], f)}
blob = d[T0:T0 + TN]
def edges(target):
    out = []
    for m in re.finditer(rb"[\xE8\xE9]", blob):
        va = TV + m.start()
        if va + 5 + struct.unpack_from("<i", blob, m.start() + 1)[0] == target and boundary(va): out.append(va)
    for m in re.finditer(rb"\x0F[\x80-\x8F]", blob):
        va = TV + m.start()
        if va + 6 + struct.unpack_from("<i", blob, m.start() + 2)[0] == target and boundary(va): out.append(va)
    for m in re.finditer(rb"[\x70-\x7F\xEB]", blob):
        va = TV + m.start()
        if va + 2 + struct.unpack_from("<b", blob, m.start() + 1)[0] == target and boundary(va): out.append(va)
    for m in re.finditer(rb"[\x48\x4C]\x8D[\x05\x0D\x15\x1D\x25\x2D\x35\x3D]", blob):
        va = TV + m.start()
        if va + 7 + struct.unpack_from("<i", blob, m.start() + 3)[0] == target: out.append(va)
    raw = [va + k for n, vs, va, rs, ra in SECS if n != b".text" for k in range(0, rs - 7, 8)
           if struct.unpack_from("<Q", d, ra + k)[0] in (target, target - 0x120000 + 0x140000000)]
    return out, raw
stub = d[off(0x16D6A0):off(0x16D6A0) + 3]
B = {i.address: (i.mnemonic + " " + i.op_str).strip() for i in MD.disasm(d[off(0x504940):off(0x504940) + 0x100], 0x504940)}
ok("E0", stub == b"\xC2\x00\x00" and B.get(0x5049A7) == "mov qword ptr [rbx + 0x230], rax" and "call 0x16d6a0" in B.values(),
   "0016D6A0 = %s; the binder stores the entry at rec + 0x230 and calls the stub" % stub.hex())
e1, r1 = edges(0x3B38B0); e2, r2 = edges(0x3B3B10)
ok("E1", e1 == [0x40A174] and e2 == [0x40A1C4] and not r1 and not r2,
   "003B38B0 <- %s; 003B3B10 <- %s; raw pointers %s" % (["%08X" % x for x in e1], ["%08X" % x for x in e2], r1 + r2))
def imm_sites(val):
    pat = struct.pack("<I", val); out = []
    for m in re.finditer(re.escape(pat), blob):
        va = TV + m.start()
        for back in range(1, 9):
            s = va - back
            if boundary(s):
                ins = next(MD.disasm(d[off(s):off(s) + 16], s), None)
                if ins and s + ins.size >= va + 4: out.append(s); break
    return out
tags = imm_sites(0x46454640)
ok("E2", tags == [0x40A0A4, 0x504F78, 0x504FCE], "'@FEF' immediates at %s" % ["%08X" % x for x in tags])
FP = {"0x228": "word", "0x1f8": "qword", "0x238": "dword"}
ends = {}
for b0, e0 in PD: ends[b0] = max(ends.get(b0, 0), e0)
def census(kind):
    out = []
    pat = r"r\w+, qword ptr \[(r\w+) \+ 0x230\]$" if kind == "read" else r"qword ptr \[(r\w+) \+ 0x230\], r\w+$"
    for b0 in sorted(ends):
        f = b0 + 0x120000; n = ends[b0] - b0
        if n <= 0 or n > 0x20000: continue
        try: o = off(f)
        except StopIteration: continue
        ops = [(i.address, i.op_str) for i in MD.disasm(d[o:o + n], f) if i.mnemonic == "mov" or "ptr [" in i.op_str]
        for a, s in ops:
            m = re.match(pat, s)
            if not m or m.group(1) == "rsp": continue
            R = m.group(1)
            fp = sorted(x for x, w in FP.items() if any(re.search(r"(?<![a-z])%s ptr \[%s \+ %s\]" % (w, R, x), s2) for a2, s2 in ops))
            if fp: out.append((f, a, fp))
    return out
reads = census("read"); full = [r for r in reads if len(r[2]) == 3]
ok("E3", not full and all(len(r[2]) < 3 for r in reads),
   "qword reads of [R + 0x230] with the full render-record shape: %d; partial matches %s" % (len(full), [("%08X" % f, "%08X" % a, fp) for f, a, fp in reads]))
writes = census("write")
ok("C", any(f == 0x504940 and fp == ["0x1f8", "0x228", "0x238"] for f, a, fp in writes) and 0x504F78 in tags and 0x504FCE in tags,
   "the fingerprint over writes finds the binder: %s" % [("%08X" % f, "%08X" % a, fp) for f, a, fp in writes if len(fp) == 3])
print("FAILS", fails); sys.exit(1 if fails else 0)
