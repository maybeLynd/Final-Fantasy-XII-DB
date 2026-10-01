"""review.py - OPUS (Claude Opus 5.5), 2026-09-28. Independent structural review of ASTRA-REVIEW-REFERENCE-FILE-BACKING-CONTROL
(_experiments/evidence/reference-base-file-backing-control/). STATIC, certified EXE only; written without ASTRA's capture/check code.

  H  the section table: .data RVA 01CD0000, VirtualSize 011A7530, SizeOfRawData 0018E400, PointerToRawData 01CCE600; with base
     00120000 the raw-backed VA end is 01F7E400 and the virtual end 02F97530
  U  the cell 01F83530 is .data-relative 0x193530: inside VirtualSize, past SizeOfRawData, so it has no file bytes (the
     zero-filled virtual tail of the PE section rule)
  A  the unsafe formula PointerToRawData + (VA - base - RVA) gives file offset 01E61B30, which is not .data's: it lies in .pdata's
     raw data (PointerToRawData 01E5CA00), 12-byte aligned, entry 1732, and the eight bytes there - 90FB0500 BAFB0500 - are that
     RUNTIME_FUNCTION's begin / end RVAs (0005FB90 / 0005FBBA -> 0017FB90..0017FBBA), contiguous with entry 1731 (..0017FB8C).
     So the quoted low four bytes are exactly what the unchecked mapping returns, and they are an unwind-table entry
  R  a second, independent reader - the section lookup the OPUS checks use, bounded by SizeOfRawData - refuses the cell and the
     raw end, and accepts the last backed qword. LIMIT, disclosed: that lookup bounds the START address only, not the read
     length, so a read starting in the last seven backed bytes would run into the next section's file bytes; no OPUS check is
     claimed audited for that here
  VERDICT: AGREE with ASTRA's structural finding - the nonzero bytes cannot be a file-backed sample of the cell. A narrows the
  failure hypothesis (an unchecked VirtualSize-only mapping reproduces them, and they are a .pdata entry); it still does not
  identify SPEC's actual producer, and says nothing of the live value, which needs its own provenance.
Usage: python review.py
"""
import hashlib, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__)); DB = os.path.abspath(os.path.join(HERE, "..", "..", "..")); ROOT = os.path.dirname(DB)
d = open(os.path.join(ROOT, "Tools", "work", "exe", "FFXII_TZA.exe"), "rb").read()
if hashlib.sha256(d).hexdigest() != "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8":
    print("REFUSED  not the certified image"); sys.exit(2)
B = 0x120000
pe = struct.unpack_from("<I", d, 0x3C)[0]; n = struct.unpack_from("<H", d, pe + 6)[0]; opt = struct.unpack_from("<H", d, pe + 20)[0]
S = {}
for i in range(n):
    h = pe + 24 + opt + i * 40; S[d[h:h + 8].rstrip(b"\0").decode()] = struct.unpack_from("<IIII", d, h + 8)   # vs, va, rs, ro
fails = 0
def check(tag, ok, text):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
vs, va, rs, ro = S[".data"]
check("H", struct.unpack_from("<Q", d, pe + 24 + 24)[0] == B and (va, vs, rs, ro) == (0x1CD0000, 0x11A7530, 0x18E400, 0x1CCE600)
      and B + va + rs == 0x1F7E400 and B + va + vs == 0x2F97530, ".data header and its raw / virtual VA ends")
CELL = 0x1F83530; rel = CELL - B - va
check("U", rel == 0x193530 and rs <= rel < vs, "the cell is in .data's virtual tail (rel 0x%X, raw 0x%X, virtual 0x%X)" % (rel, rs, vs))
unsafe = ro + rel; pvs, pva, prs, pro = S[".pdata"]
b0, e0, u0 = struct.unpack_from("<III", d, unsafe); b1, e1, u1 = struct.unpack_from("<III", d, unsafe - 12)
check("A", unsafe == 0x1E61B30 and pro <= unsafe < pro + prs and (unsafe - pro) % 12 == 0 and (unsafe - pro) // 12 == 1732
      and d[unsafe:unsafe + 8] == bytes.fromhex("90fb0500bafb0500") and (b0, e0) == (0x5FB90, 0x5FBBA) and e1 <= b0,
      "the unsafe offset is .pdata entry %d: %08X..%08X (previous ends %08X)" % ((unsafe - pro) // 12, b0 + B, e0 + B, e1 + B))
SECS = list(S.values())
def off(v):
    for vs_, va_, rs_, ro_ in SECS:
        if B + va_ <= v < B + va_ + rs_: return v - B - va_ + ro_
check("R", off(CELL) is None and off(0x1F7E400) is None and off(0x1F7E3F8) == ro + rs - 8,
      "the SizeOfRawData-bounded lookup refuses the cell and the raw end and accepts the last backed qword (start-only bound)")
print("VERDICT AGREE" if not fails else "VERDICT NOT REACHED")
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
