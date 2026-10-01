# joins.py - data joins that test candidate field meanings against other tables (us battle_pack.bin).
import sys, os, struct, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pack import TABLES, records
T = {n: records(d)[0] for n, s, d in TABLES}
u16 = lambda r, o: struct.unpack_from("<H", r, o)[0]
u32 = lambda r, o: struct.unpack_from("<I", r, o)[0]
act = T["action_data"]

def report(label, ok, total, bad):
    print("%-70s %d / %d%s" % (label, ok, total, ("  first mismatches: " + str(bad[:6])) if bad else ""))

# 1. item row +7 = action row: action[+7].+0x22 == 0x0000 + item row, and action[+7].+0x34 == item +8 (name word)
bad = []; ok = 0
for i, r in enumerate(T["dougu_data"]):
    a = act[r[7]]
    if u16(a, 0x22) == i and u16(a, 0x34) == u16(r, 8) and a[0x1E] == 3: ok += 1
    else: bad.append((i, r[7], hex(u16(a, 0x22)), hex(u16(a, 0x34)), hex(u16(r, 8)), a[0x1E]))
report("dougu +7 -> action row with +0x22 == item row, +0x34 == item +8, +0x1E == 3", ok, len(T["dougu_data"]), bad)

# 2. magick / technick row +2 = action row whose +0x22 is the class id (0x3000 + row / 0x4000 + row) and +0x1E 1 / 2
for name, base, cat in (("maho_data", 0x3000, 1), ("waza_data", 0x4000, 2)):
    bad = []; ok = 0
    for i, r in enumerate(T[name]):
        a = act[r[2]]
        if u16(a, 0x22) == base + i and u16(a, 0x34) == u16(r, 4) and a[0x1E] == cat: ok += 1
        else: bad.append((i, r[2], hex(u16(a, 0x22)), hex(u16(a, 0x34)), hex(u16(r, 4)), a[0x1E]))
    report("%s +2 -> action row with +0x22 == %#x+row, +0x34 == +4 name, +0x1E == %d" % (name, base, cat), ok, len(T[name]), bad)

# 3. quickening row +2 (u16) = action row; +0 name word == action +0x34 ; +0x22 == 0xC000 + row ?
bad = []; ok = 0; ok22 = 0
for i, r in enumerate(T["menkyo_data"]):
    a = act[u16(r, 2)]
    if u16(a, 0x34) == u16(r, 0): ok += 1
    else: bad.append((i, u16(r, 2), hex(u16(a, 0x34)), hex(u16(r, 0))))
    if u16(a, 0x22) == 0xC000 + i: ok22 += 1
report("menkyo +2 (u16) -> action row whose +0x34 name word == menkyo +0", ok, 32, bad)
print("   of those, action +0x22 == 0xC000 + row on", ok22, "/ 32")
print("   menkyo +4 == row index on", sum(1 for i, r in enumerate(T["menkyo_data"]) if r[4] == i), "/ 32")

# 4. sort-key fields: distinct within the table?
for name, off, w in (("dougu_data", 0, 1), ("eventitem_data", 8, 2), ("maho_data", 6, 1), ("waza_data", 6, 1),
                     ("m_daiji", 2, 2), ("g_daiji", 2, 2), ("q_daiji", 2, 2)):
    vals = [int.from_bytes(r[off:off + w], "little") for r in T[name]]
    c = collections.Counter(vals)
    print("%-16s sort key +%#x: %d distinct of %d rows; repeated: %s" % (name, off, len(c), len(vals), [(v, k) for v, k in c.items() if k > 1][:5]))

# 5. key-item +0 : does it equal anything obvious?
for name in ("m_daiji", "g_daiji", "q_daiji"):
    rs = T[name]
    print(name, "+0 first 40:", [u16(r, 0) for r in rs[:40]])
    print(name, "+0 == row index on", sum(1 for i, r in enumerate(rs) if u16(r, 0) == i), "/", len(rs), "; +0 == +2 on", sum(1 for r in rs if u16(r, 0) == u16(r, 2)))
