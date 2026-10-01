#!/usr/bin/env python3
"""Census of typed-list item type ids over the embedded MRP units inside
the locale `packfiles/mrppack_ys.bin` archives in FFXII_TZA.vbf.

Companion to gen_listtype_census.py (which covers the 116 standalone
`mrp_menu/*.mrp` files); this script covers the second half of the
344-blob typed-list corpus, for UQ-76 on
a-typed-list-measured-once-and-built-in-one-allocation.md.

Packfile layout (verified against all ten shipped packs):

    +0x00  u32[32]   unit offset table; unused slots are 0xFFFFFFFF
    units            contiguous MRP blocks, each 'MRP\\0'-magic, sliced
                     to the next valid offset (last unit to EOF)
    unit             same layout as a standalone .mrp:
                     +0x08 items-blob end offset (walk lands within a
                          zero pad of it)
                     +0x1C outer record count
                     +0x20 outer table offset

The nine 23-unit packs are us/kr/it/in/fr/es/de/cn/ch; `in_sdver` ships
21 units.  Total: 228 units.

Answers: count per type id over the embedded set, which units carry
types 3, 6 or 9, and validation of every unit boundary (magic, table
range, walk landing on the unit's own +0x08 within a zero pad).

Usage: gen_listtype_census_embedded.py [vbf-path]
    -> writes listtype-census-embedded.tsv beside this script and
       prints the summary.
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
    packs = sorted(p for p in names if "mrppack_ys" in p.lower())

    type_dist = collections.Counter()
    units_with = collections.defaultdict(list)  # type id -> [(pack, unit)]
    t6_bodies = []
    total_units = 0
    total_records = 0
    total_items = 0
    issues = []

    tsv = io.open(os.path.join(HERE, "listtype-census-embedded.tsv"), "w",
                  encoding="utf-8", newline="\n")
    tsv.write("# typed-list item type census - embedded MRP units inside "
              "locale packfiles/mrppack_ys.bin; same walk as "
              "gen_listtype_census.py\n")
    tsv.write("pack\tunit\tunit_off\trecords\titems\ttypes_seen\twalk_end"
              "\thdr_0x08\twalk_ok\n")

    for p in packs:
        blob = V.read_entry(f, names, blocks, p)
        n_slots = U32(blob, 0) // 4
        offs = [o for o in struct.unpack_from("<%dI" % n_slots, blob, 0)
                if o != 0xFFFFFFFF]
        tag = p.split("/")[-3] if "/" in p else p
        for ui, uoff in enumerate(offs):
            if uoff + 0x24 > len(blob) or blob[uoff:uoff + 4] != b"MRP\x00":
                issues.append((p, ui, "bad magic/short"))
                continue
            uend = offs[ui + 1] if ui + 1 < len(offs) else len(blob)
            unit = blob[uoff:uend]
            n = U32(unit, 0x1C)
            toff = U32(unit, 0x20)
            items_end = U32(unit, 0x08)
            if toff + 20 * n > len(unit) or items_end > len(unit):
                issues.append((p, ui, "table/items_end out of range"))
                continue
            counts = [U32(unit, toff + 20 * i) & 0x3FF for i in range(n)]
            pos = toff + 20 * n
            types = []
            ok = True
            for _ in range(sum(counts)):
                if pos + 2 > len(unit) or unit[pos] < 2 \
                        or pos + unit[pos] > len(unit):
                    ok = False
                    break
                ty = unit[pos + 1]
                types.append(ty)
                if ty == 6:
                    t6_bodies.append(
                        (tag, ui, hex(pos),
                         unit[pos + 4:pos + unit[pos]].hex()))
                pos += unit[pos]
            gap = items_end - pos
            ok = ok and 0 <= gap <= 12 and all(
                unit[pos + j] == 0 for j in range(gap))
            if not ok:
                issues.append((p, ui, "walk_end", hex(pos),
                               hex(items_end)))
            total_units += 1
            total_records += n
            total_items += len(types)
            seen = collections.Counter(types)
            for t in seen:
                type_dist[t] += seen[t]
                units_with[t].append((tag, ui))
            tsv.write("%s\t%d\t0x%x\t%d\t%d\t%s\t0x%x\t0x%x\t%s\n"
                      % (p, ui, uoff, n, len(types),
                         ",".join("%d:%d" % kv for kv in
                                  sorted(seen.items())),
                         pos, items_end, ok))
    tsv.close()

    print("packs", len(packs), "units", total_units,
          "records", total_records, "items", total_items)
    print("issues:", issues[:10], "total", len(issues))
    print("type dist:", dict(sorted(type_dist.items())))
    for t in (3, 6, 9):
        print("units carrying type %d:" % t,
              collections.Counter(u for u, _ in units_with.get(t, []))
              if t != 6 else t6_bodies)


if __name__ == "__main__":
    main()
