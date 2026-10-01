"""gen_wd_census.py -- census the `WD` (slot 1) sections of every shipped map-control pack.

Reproduces members/wd-census.tsv from the shipped VBF. Columns:

    pack            file name (basename)
    fileSize        section payload size in bytes
    field02         u16 at +0x02 (per-pack id; 0x1FA..0x251 corpus-wide, all distinct)
    dataSize        u32 at +0x04; the trailing blob occupies [fileSize-dataSize, fileSize)
    count           u32 at +0x08 (= u32 at +0x0C, always equal)
    flags14         u32 at +0x14; 0x8000 (11 packs), 0x10000 (6), 0 (29); +0x10 u32 is 0
    dataStart       fileSize - dataSize (always 0x40-aligned)
    firstOff        first offset-table entry = align16(0x20 + 4*count)
    tableSpill      1 if the 0x20-stride record table runs past dataStart (27/46 packs)
    records         count x 0x20 records: A(u32 0; u32 X; u32 Y; u32 0x5FE800FF) +
                    B(u32 hash; u32 0x407F7F3C; u32 0; u32 0) interleaved at off_i / off_i+0x10
    Xmonotonic      1 if X is non-decreasing across the pack's records (46/46)
    XYunderDsz      1 if every X and Y is < dataSize (225/225 records)
    XeqY            number of records with X == Y (177/225 corpus-wide)

Run:  python gen_wd_census.py            # writes wd-census.tsv next to this script
"""

import os
import struct
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "agent_flow", "tools")))
import vbfextract

VBF = "D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf"

# Same slot extractor as gen_ym00_census.py: mpk header padded to 0x40, then per nonzero
# slot a 0x40 slot header + payload.
def slot(payload, idx):
    count = struct.unpack_from("<I", payload, 0)[0]
    pos = (count + 1) * 4 + 0x3F & ~0x3F
    for i in range(count):
        size = struct.unpack_from("<I", payload, 4 + 4 * i)[0]
        if size == 0:
            continue
        pos += 0x40
        if i == idx:
            return payload[pos:pos + size]
        pos += size
    return None


def main():
    f = open(VBF, "rb")
    names, blocks = vbfextract.load_index(f)
    out = [__doc__.strip().splitlines()[0]]
    out.append("# pack\tfileSize\tfield02\tdataSize\tcount\tflags14\tdataStart\tfirstOff\ttableSpill\trecords\tXmonotonic\tXYunderDsz\tXeqY")
    npacks = nrec = neq = 0
    for p in sorted(n for n in names if n.lower().endswith(".mpk")):
        b = slot(vbfextract.read_entry(f, names, blocks, p), 1)
        if not b:
            continue
        field02, dataSize, c1, c2, u10, flags14 = struct.unpack_from("<HIIIII", b, 2)
        assert c1 == c2 and u10 == 0 and flags14 in (0, 0x8000, 0x10000)
        data = len(b) - dataSize
        offs = [struct.unpack_from("<I", b, 0x20 + 4 * i)[0] for i in range(c1)]
        first = (0x20 + 4 * c1 + 0xF) & ~0xF
        assert offs[0] == first and all(offs[i + 1] - offs[i] == 0x20 for i in range(c1 - 1))
        xs = []
        eq = under = 0
        recs = []
        for o in offs:
            u0, X, Y, FL = struct.unpack_from("<IIII", b, o)
            h, sc, z1, z2 = struct.unpack_from("<IIII", b, o + 0x10)
            assert u0 == 0 and FL == 0x5FE800FF and sc == 0x407F7F3C and z1 == 0 and z2 == 0
            recs.append(f"{o:#x}:{X:#x},{Y:#x},{h:#x}")
            xs.append(X)
            eq += X == Y
            under += (X < dataSize) + (Y < dataSize)
        npacks += 1
        nrec += c1
        neq += eq
        mono = int(all(xs[i + 1] >= xs[i] for i in range(len(xs) - 1)))
        spill = int(offs[-1] + 0x20 > data)
        out.append(f"{os.path.basename(p)}\t{len(b)}\t{field02:#x}\t{dataSize:#x}\t{c1}\t{flags14:#x}\t{data:#x}\t{offs[0]:#x}\t{spill}\t\"{';'.join(recs)}\"\t{mono}\t{int(under == 2 * c1)}\t{eq}")
    out.append(f"# {npacks} packs, {nrec} records, {neq} with X==Y")
    open(os.path.join(os.path.dirname(__file__), "wd-census.tsv"), "w").write("\n".join(out) + "\n")
    print(f"{npacks} packs, {nrec} records, {neq} X==Y")


if __name__ == "__main__":
    main()
