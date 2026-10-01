#!/usr/bin/env python3
"""Census of typed-list item type ids over every shipped .mrp file in
FFXII_TZA.vbf, for FABLE-REQ-SWE2-DATA-LIST-TYPE-ID-CENSUS / UQ-76 on
a-typed-list-measured-once-and-built-in-one-allocation.md.

File layout (verified against the walk landing exactly on header +0x08 in
save_load.mrp):

    header  +0x00 'MRP\\0'
            +0x08 u32   items-blob end offset (walk lands within a
                          0/4/8/12-byte zero pad of it)
            +0x1C u32   outer record count
            +0x20 u32   outer table offset (0x30 in all files probed)
    outer record, 20 bytes:
            dword0  bits 0-9 item count, bits 10-27 record's own index,
                    bit 28 a per-record flag (clear in 55 of 1,458 records:
                    party_book 5/25/28/40, title 3, title_fore3 3)
            dword4  arena offset of this record's item bytes (relative to
                    the outer-table base at runtime - not needed here)
    item bytes: a contiguous stream starting at table end; each item is
            {u8 length, u8 type, ...} and self-sizes.  Walking sum(count)
            items from table end lands on header +0x08 within a zero pad of
            0/4/8/12 bytes in all 116 files (never overshot, gap always
            zero-filled) - that is the control that proves the stream
            interpretation.

Answers: count per type id corpus-wide, which files carry types 3 or 6,
and max((dword0 >> 10) & 0x3FFFF) over all outer records.

Usage: gen_listtype_census.py [vbf-path]
    -> writes listtype-census.tsv beside this script and prints the summary.
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                                 "agent_flow", "tools")))
import vbfextract as V

VBF = sys.argv[1] if len(sys.argv) > 1 else \
    r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]


def main():
    f = io.open(VBF, "rb")
    names, blocks = V.load_index(f)
    mrps = sorted(p for p in names if p.lower().endswith(".mrp"))

    type_dist = collections.Counter()          # type id -> items, corpus
    files_with = collections.defaultdict(list) # type id -> [files]
    max_mid = 0                                # max bits 10-27 of dword0
    mid_where = ""
    total_items = 0
    total_records = 0
    walk_misses = []                           # files where walk != hdr+8
    bit28_clear = 0
    bad_files = []

    tsv = io.open(os.path.join(HERE, "listtype-census.tsv"), "w",
                  encoding="utf-8", newline="\n")
    tsv.write("# typed-list item type census - every shipped .mrp, items "
              "walked as the contiguous {u8 len,u8 type} stream that lands "
              "on header +0x08\n")
    tsv.write("file\trecords\titems\ttypes_seen\tmax_bits10_27\twalk_end"
              "\thdr_0x08\twalk_ok\n")

    for p in mrps:
        blob = V.read_entry(f, names, blocks, p)
        if len(blob) < 0x24 or blob[:4] != b"MRP\x00":
            bad_files.append((p, "bad magic/short"))
            continue
        n = U32(blob, 0x1C)
        toff = U32(blob, 0x20)
        items_end = U32(blob, 0x08)
        if toff + 20 * n > len(blob) or items_end > len(blob):
            bad_files.append((p, "table/items_end out of range"))
            continue
        counts = []
        fmax = 0
        b28 = 0
        for i in range(n):
            d0 = U32(blob, toff + 20 * i)
            counts.append(d0 & 0x3FF)
            mid = (d0 >> 10) & 0x3FFFF
            if mid > fmax:
                fmax = mid
            if mid > max_mid:
                max_mid, mid_where = mid, p + " record %d" % i
            if not (d0 >> 28) & 1:
                b28 += 1
        pos = toff + 20 * n
        types = []
        ok = True
        for _ in range(sum(counts)):
            if pos + 2 > len(blob):
                ok = False
                break
            ln = blob[pos]
            if ln < 2:
                ok = False
                break
            types.append(blob[pos + 1])
            pos += ln
        gap = items_end - pos
        ok = ok and 0 <= gap <= 12 and all(
            blob[pos + j] == 0 for j in range(gap))
        if not ok:
            walk_misses.append((p, hex(pos), hex(items_end)))
        total_items += len(types)
        total_records += n
        bit28_clear += b28
        seen = collections.Counter(types)
        for t in seen:
            type_dist[t] += seen[t]
            files_with[t].append(p)
        tsv.write("%s\t%d\t%d\t%s\t%d\t0x%x\t0x%x\t%s\n"
                  % (p, n, len(types),
                     ",".join("%d:%d" % kv for kv in sorted(seen.items())),
                     fmax, pos, items_end, ok))
    tsv.close()

    print("files", len(mrps), "records", total_records, "items", total_items)
    print("bad files:", bad_files)
    print("walk misses (pos != hdr+8):", walk_misses[:10], "total", len(walk_misses))
    print("records with bit28 clear:", bit28_clear)
    print("type dist:", dict(sorted(type_dist.items())))
    print("files carrying type 3:", files_with.get(3, []))
    print("files carrying type 6:", files_with.get(6, []))
    print("max bits10-27 of dword0:", max_mid, "at", mid_where)


if __name__ == "__main__":
    main()
