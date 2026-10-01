"""SWE2-AUDIT-SPEC independent checks for OPUS batch 6 (run from the repo root, system python + pefile/capstone).
  F  staged look: image-wide raw search for `add rcx, 0x580` (48 81 C1 80 05 00 00) followed by E9/EB, not limited to listed functions
  R  rig: both 17-entry RVA tables read raw; index 4 target and distinctness
  T  table room: bytes between the two resampled tables and the next table (120 floats = 0x1E0)
"""
import re, struct, pefile
EXE = "Database/Tools/work/exe/FFXII_TZA.exe"
FT = "Database/Tools/work/graph/functions.tsv"
pe = pefile.PE(EXE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
raw = open(EXE, "rb").read()
tx = next(s for s in pe.sections if s.Name.startswith(b".text")); t = tx.get_data(); tva = IB + tx.VirtualAddress
ents = set(int(l.split("\t")[0], 16) for l in open(FT, encoding="utf-8").read().splitlines()[1:] if l[:1].strip())
fw = []
for m in re.finditer(re.escape(bytes.fromhex("4881c180050000")), t):
    h = m.start(); n = t[h + 7]
    tgt = tva + h + 12 + struct.unpack_from("<i", t, h + 8)[0] if n == 0xE9 else (tva + h + 9 + struct.unpack_from("<b", t, h + 8)[0] if n == 0xEB else None)
    if tgt: fw.append((tva + h, tgt, (tva + h) in ents))
print("F: add rcx,0x580 + jmp: %d; at listed entries %d; distinct targets among listed %d" % (len(fw), sum(x[2] for x in fw), len({x[1] for x in fw if x[2]})))
for a, g, l in fw:
    if not l: print("   not a listed entry: %08X -> %08X" % (a, g))
for tab in (0x003E15C8, 0x003E1888):
    off = pe.get_offset_from_rva(tab - IB)
    e = [IB + struct.unpack_from("<I", raw, off + 4 * i)[0] for i in range(17)]
    print("R: table %08X idx4 -> %08X; other 16 distinct: %s; idx4 unique: %s" % (tab, e[4], len(set(e) - {e[4]}) == 16, e.count(e[4]) == 1))
for a, b in ((0x01F20AA0, 0x01F20C80), (0x01F20C80, 0x01F20E60)):
    print("T: %08X..%08X = %d floats" % (a, b, (b - a) // 4))
