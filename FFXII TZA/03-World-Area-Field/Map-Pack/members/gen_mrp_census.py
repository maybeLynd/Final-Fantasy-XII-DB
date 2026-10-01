"""gen_mrp_census.py -- census the `MRP` (slot 15) sections of every shipped map-control pack.

Reproduces members/mrp-census.tsv from the shipped VBF. Only two packs carry slot 15
(rwg0201, rwg0202) and the payloads are byte-identical, so the census is a layout proof
of the single shared block rather than a population survey. Columns:

    pack            file name (basename)
    fileSize        section payload size in bytes
    sha16           first 16 hex of the payload SHA-256 (identical across the 2 packs)
    magic           first 4 bytes -- 'MRP\\0' (flag byte +3 = 0, un-relocated)
    tailCount/Off   u32 pair at +0x04/+0x08  -> 2 records x 0x10 at 0x470 (char[16] names)
    descCount/Off   u32 pair at +0x1C/+0x20  -> 5 records x 0x14 at 0x30 (rect descriptors)
    tblBCount/Off   u32 pair at +0x24/+0x28  -> 2 records x 0x0C at 0x490; the ONLY populated
                    table B in the MRP corpus (all 116 mrp_menu files ship it empty)
    tblBSpans       per record {flag, len, relOff}: relOff is relative to the table-B base
                    (the relocator 002A0147 adds the base); each span is a {char[16] name;
                    TIM2 image} resource, and they tile the file: 0x4B0+0x8430 == 0x88E0 and
                    0x88E0+0x209B0 == fileSize
    descs           the 5 descriptor rows {index, sub, tag, u, v, w, h, aux, refAbs} --
                    ref is row-relative (relocator 002A1AD0 adds the row address)

Run:  python gen_mrp_census.py           # writes mrp-census.tsv next to this script
"""

import hashlib
import os
import struct
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "agent_flow", "tools")))
import vbfextract

VBF = "D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf"


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
    out.append("# pack\tfileSize\tsha16\tmagic\ttailCount\ttailOff\tdescCount\tdescOff\ttblBCount\ttblBOff\ttblBSpans\tdescs")
    for p in sorted(n for n in names if n.lower().endswith(".mpk")):
        b = slot(vbfextract.read_entry(f, names, blocks, p), 15)
        if not b:
            continue
        magic = b[:4]
        tailCount, tailOff = struct.unpack_from("<II", b, 4)
        spareC0, spareO0, spareC1, spareO1 = struct.unpack_from("<IIII", b, 0x0C)
        descCount, descOff, tbCount, tbOff = struct.unpack_from("<IIII", b, 0x1C)
        assert magic == b"MRP\x00"
        assert spareC0 == spareC1 == 0 and spareO0 == spareO1 == tbOff
        assert tailOff + 0x10 * tailCount <= tbOff
        descs = []
        for i in range(descCount):
            off = descOff + i * 0x14
            r = b[off:off + 0x14]
            idx, sub, z, tag = r[0], r[1], r[2], r[3]
            u, v, w, h = struct.unpack_from("<4H", r, 4)
            aux, ref = struct.unpack_from("<II", r, 0x0C)
            assert z == 0 and off + ref < len(b)
            descs.append("{%d,%d,0x%02x,0x%x,0x%x,0x%x,0x%x,0x%x->0x%x}" % (idx, sub, tag, u, v, w, h, aux, off + ref))
        spans = []
        for i in range(tbCount):
            off = tbOff + i * 0x0C
            flag, ln, rel = struct.unpack_from("<III", b, off)
            tgt = tbOff + rel
            name = b[tgt:tgt + 16].split(b"\0")[0].decode("ascii")
            assert b[tgt + 16:tgt + 20] == b"TIM2"
            assert flag == 1 and tgt + ln <= len(b)
            spans.append("{%d,0x%x->0x%x '%s' TIM2}" % (flag, ln, tgt, name))
        out.append("%s\t%d\t%s\t%s\t%d\t0x%x\t%d\t0x%x\t%d\t0x%x\t%s\t%s" % (
            p.split("/")[-1], len(b), hashlib.sha256(b).hexdigest()[:16], magic,
            tailCount, tailOff, descCount, descOff, tbCount, tbOff,
            ";".join(spans), ";".join(descs)))
    open(os.path.join(os.path.dirname(__file__), "mrp-census.tsv"), "w").write("\n".join(out) + "\n")
    print("wrote", len(out) - 2, "pack rows")


if __name__ == "__main__":
    main()
