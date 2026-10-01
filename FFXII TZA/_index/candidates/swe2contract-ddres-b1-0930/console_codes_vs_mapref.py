"""console_codes_vs_mapref.py - join the developer console's authored-code table (01DF6E68, 16-byte entries
{char* code, u32 index+1, u32 0}) with map_ref.bin's per-field own-pack census
(03-World-Area-Field/Map-Pack/members/map-ref-field-packs.tsv) by index = field id.
SWE2-CONTRACT, 2026-09-30, for the DD residue closure batch 1. Static + authored data. Reads only.

Positive control: entry 0 must decode to 'ous0101' (published on the page) and the sequence word must equal index+1
for all 1,314 entries (published in the contract, I-7 / D7). A code whose table offset does not land on a string is
reported, not guessed. The comparison strips '.mpk'; census rows marked ambiguous count as agreeing when any
candidate matches, and are tallied separately.
"""
import io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
EXE = os.path.join(DB, "..", "Tools", "work", "exe", "FFXII_TZA.exe")
TSV = os.path.join(DB, "03-World-Area-Field", "Map-Pack", "members", "map-ref-field-packs.tsv")
BASE, TABLE, N = 0x120000, 0x01DF6E68, 1314


def sections(pe):
    e = struct.unpack_from("<I", pe, 0x3C)[0]
    nsec = struct.unpack_from("<H", pe, e + 6)[0]
    opt = struct.unpack_from("<H", pe, e + 20)[0]
    out = []
    for i in range(nsec):
        o = e + 24 + opt + 40 * i
        vsz, va, rsz, rptr = struct.unpack_from("<IIII", pe, o + 8)
        out.append((BASE + va, vsz, rsz, rptr))
    return out


def reader(pe, secs):
    def at(addr, n):
        for va, vsz, rsz, rptr in secs:
            if va <= addr < va + max(vsz, rsz):
                off = addr - va
                return pe[rptr + off: rptr + off + n] if off + n <= rsz else None
        return None
    return at


def main():
    pe = io.open(EXE, "rb").read()
    at = reader(pe, sections(pe))
    codes, seq_bad = [], 0
    for i in range(N):
        raw = at(TABLE + 16 * i, 16)
        ptr, seq, pad = struct.unpack("<QII", raw)
        seq_bad += (seq != i + 1) or (pad != 0)
        s = None
        if ptr:
            b = at(ptr, 16)
            s = b.split(b"\0")[0].decode("ascii", "replace") if b else "<unmapped %X>" % ptr
        codes.append(s)
    fails = 0
    ok0 = codes[0] == "ous0101" and seq_bad == 0
    fails += not ok0
    print("%s  control: entry0=%r, sequence==index+1 for all %d: %s" % ("PASS" if ok0 else "FAIL", codes[0], N, seq_bad == 0))
    census = {}
    for line in io.open(TSV, encoding="utf-8").read().splitlines():
        if line.startswith("#") or line.startswith("field\t") or not line.strip():
            continue
        c = line.split("\t")
        census[int(c[0])] = c[2]
    populated = [i for i, s in enumerate(codes) if s]
    agree = amb = disagree = missing = 0
    bad = []
    for i in populated:
        own = census.get(i)
        if own is None:
            missing += 1; bad.append((i, codes[i], "no census row")); continue
        cands = [x.replace(".mpk", "") for x in own.replace("ambiguous:", "").split("/")]
        if codes[i] in cands:
            agree += 1; amb += own.startswith("ambiguous:")
        else:
            disagree += 1; bad.append((i, codes[i], own))
    print("entries %d, populated %d, census rows %d" % (N, len(populated), len(census)))
    print("agree %d (of which census-ambiguous %d), disagree %d, no census row %d" % (agree, amb, disagree, missing))
    for b in bad[:40]:
        print("  MISMATCH", b)
    # negative control: the same join shifted by one field must mostly disagree, or the agreement is not index-bound
    shifted = sum(1 for i in populated if census.get(i + 1) and codes[i] in
                  [x.replace(".mpk", "") for x in census[i + 1].replace("ambiguous:", "").split("/")])
    print("negative control (join at field id + 1): agree %d of %d" % (shifted, len(populated)))
    fails += shifted * 2 > len(populated)
    console = [i for i in populated if i <= 293]
    print("console id space 0..293: populated %d" % len(console))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
