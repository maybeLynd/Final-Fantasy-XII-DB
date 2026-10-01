"""gen_ym00_tag2226_census.py -- census the tag-22 and tag-26 chunks inside every shipped YM00.

Reproduces members/ym00-tag2226-census.tsv from the shipped VBF. Both chunks use the
nested index `{u32 count; (count+1) x {u24 offset16 | u8 tag}}` -- the same encoding as
YM00's own directory. Per pack, one row per tag:

    pack            file name (basename)
    tag             22 or 26
    chunkSize       bytes
    count           dword[0]
    sentinelOK      sentinel off16 * 16 == chunkSize (end lands exactly at EOF)
    ascending       offsets non-decreasing
    tagsSeen        the distinct tag bytes on interior entries (0 for tag22, 0xFF for tag26)
    records         count entries parse:
                      tag26 -- every record is {char[0x28] name; u32 picCount; u32 0; TIM2
                      at +0x30}, +0x28 mirrors the TIM2's u16 picCount at +0x36, and the
                      TIM2 +0x05 flag is 0 in all (pictures at +0x10)
                      tag22 -- every record is {vec4 AABBmin(w=1); vec4 AABBmax(w=1);
                      vec4(128x4); u32 axisMode; u32 period; tail} -- the consumer
                      002F4520 reads +0x30/+0x34 only; row reports per-pack mode
                      histogram (0=static,1=lane2,2=lanes1+3,3=all)
    picTotal        tag26: sum of picture counts (the runtime entry count = sum, entries
                    are 0x60-stride at qword[buf+8]); tag22: '-'
    sampleNames     tag26: first two record names

Run:  python gen_ym00_tag2226_census.py    # writes ym00-tag2226-census.tsv next to this script
"""

import os
import struct
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "..", "agent_flow", "tools")))
import vbfextract

VBF = "D:/FFXII MP Mod/FFXII_TestClient1/FFXII_TZA.vbf"


def mpk_slot(payload, idx):
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


def ym00_chunks(b):
    n = struct.unpack_from("<I", b, 0x10)[0]
    ents = []
    for i in range(n + 1):
        v = struct.unpack_from("<I", b, 0x14 + 4 * i)[0]
        ents.append((v & 0xFFFFFF, v >> 24))
    out = {}
    for i, (off, tag) in enumerate(ents[:-1]):
        out[tag] = b[0x10 + off * 16:0x10 + ents[i + 1][0] * 16]
    return out


def inner_index(c):
    cnt = struct.unpack_from("<I", c, 0)[0]
    offs, tags = [], set()
    for i in range(cnt + 1):
        v = struct.unpack_from("<I", c, 4 + 4 * i)[0]
        offs.append(v & 0xFFFFFF)
        if i < cnt:
            tags.add(v >> 24)
    return cnt, offs, tags


def main():
    f = open(VBF, "rb")
    names, blocks = vbfextract.load_index(f)
    out = [__doc__.strip().splitlines()[0]]
    out.append("# pack\ttag\tchunkSize\tcount\tsentinelOK\tascending\ttagsSeen\trecords\tpicTotal\tsampleNames")
    for p in sorted(n for n in names if n.lower().endswith(".mpk")):
        y = mpk_slot(vbfextract.read_entry(f, names, blocks, p), 8)
        if not y:
            continue
        ch = ym00_chunks(y)
        for tag in (22, 26):
            c = ch.get(tag)
            if c is None or not len(c):
                continue
            cnt, offs, tags = inner_index(c)
            sent = offs[-1] * 16 == len(c)
            asc = all(offs[i + 1] >= offs[i] for i in range(cnt))
            recs = pic_total = 0
            samples = []
            if tag == 26:
                for i in range(cnt):
                    r = offs[i] * 16
                    ok = (c[r + 0x30:r + 0x34] == b"TIM2"
                          and c[r + 0x35] == 0
                          and struct.unpack_from("<I", c, r + 0x28)[0] == struct.unpack_from("<H", c, r + 0x36)[0]
                          and struct.unpack_from("<I", c, r + 0x2C)[0] == 0
                          and all(32 <= x < 127 for x in c[r:r + 0x28].split(b"\0")[0]))
                    if ok:
                        recs += 1
                        pic_total += struct.unpack_from("<H", c, r + 0x36)[0]
                        if len(samples) < 2:
                            samples.append(c[r:r + 0x28].split(b"\0")[0].decode("ascii"))
                rec_field = "%d ok" % recs
                pic_field = str(pic_total)
            else:
                modes = {}
                for i in range(cnt):
                    r = offs[i] * 16
                    if (offs[i + 1] - offs[i]) * 16 < 0x38:
                        continue  # zero-length index alias (offset repeats)
                    ok = (struct.unpack_from("<f", c, r + 0x0C)[0] == 1.0
                          and struct.unpack_from("<f", c, r + 0x1C)[0] == 1.0
                          and struct.unpack_from("<4f", c, r + 0x20) == (128.0,) * 4)
                    if ok:
                        recs += 1
                        m, pd = struct.unpack_from("<II", c, r + 0x30)
                        modes[m] = modes.get(m, 0) + 1
                        if m == 0:
                            assert pd == 0
                rec_field = "%d ok m{%s}" % (recs, ",".join(
                    "%d:%d" % kv for kv in sorted(modes.items())))
                pic_field = "-"
            out.append("%s\t%d\t%d\t%d\t%d\t%d\t%s\t%s\t%s\t%s" % (
                p.split("/")[-1], tag, len(c), cnt, int(sent), int(asc),
                ",".join("0x%02x" % t for t in sorted(tags)), rec_field, pic_field,
                ";".join(samples)))
    open(os.path.join(os.path.dirname(__file__), "ym00-tag2226-census.tsv"), "w").write("\n".join(out) + "\n")
    print("wrote", len(out) - 2, "rows")


if __name__ == "__main__":
    main()
