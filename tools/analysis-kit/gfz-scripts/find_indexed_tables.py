# -*- coding: utf-8 -*-
"""Undeclared indexed tables, grouped by access site.

METHOD AND ITS LIMITS, both established by control rather than assumption.

An access `[breg + ireg*N + disp]` recorded in a route-tracked census at type-relative offset X says:
X is reached by indexing, so an ARRAY covers X, its element size is a positive MULTIPLE of N, and
the array's base is at or below X. It does NOT say the array starts at X, and it does not say the
element is N bytes - x86 scales stop at 8, so larger or non-power-of-two elements are reached by
pre-multiplying the index.

POSITIVE CONTROL (run separately, 14/14): where the store already declares an array at an offset the
censuses index, the observed scale divides the declared element size in every case - including the
two pre-multiplied ones, BattleStatsRecord[40] element 456 with scales 2 and 4, and GambitConfig[120]
element 52 with scale 4.
NEGATIVE CONTROL: only 50.7 percent of declared array element sizes are divisible by 2 and 27.4 by 4,
so random pairings with the same scale mix would pass 6.2 of 14. The control discriminates.

GROUPING. Offsets reached through the SAME base and index register with the SAME scale AND THE SAME
ROUTE are members of one element of one table, not separate tables - `[rdi+rdx*4+0x88]` and
`[rdi+rdx*4+0x8a]` are two 2-byte members of a 4-byte element. So the group, not the offset, is the
unit, and the group's minimum offset is the tightest available upper bound on the table base.

FUNCTION PLUS REGISTER WAS NOT ENOUGH. Grouping on those alone produced a BattleSystemState "table"
whose members sat 29552 bytes apart, because a long function reloads the same registers for
different objects. The route column records where the register was established and separates exactly
those cases, so it is part of the key.

NOR WAS THE ROUTE. The same 29552-byte span survived it, because a `seed` route means the register
IS the object at offset 0, so every seeded indexed access in one function keys alike. There is no
route fine enough to separate two tables reached the same way, so the final rule is arithmetic and
conservative: within a key, SPLIT wherever consecutive offsets differ by the scale or more. Members
of one element whose size equals the scale must lie closer together than that, so this never merges
two tables; it does split a pre-multiplied table into pieces, which reports more tables with smaller
extents and leaves every base bound valid. Under-clustering is the safe direction of error here.
"""
import io
import os
import re
import glob
import collections
import kit_paths as KP  # noqa: E402

DB = os.path.join(KP.ROOT, "Database", "FFXII TZA")
# An x86 scale of 1 is not printed, so `[rax + rcx + 0x1000]` is indexed and shows no `*N`.
# Matching only on `*N` missed 131 rows - a third of every indexed access in the censuses, and
# they were the byte-stride ones: `and` / `or` / `test byte ptr [rax + rcx + 0x1000]`, which is
# what a BITMAP looks like and the exact shape this prospector exists to find. Measured against
# hop_scan's own note="idx" marker, which it sets from capstone's decoded mem.index: 260 rows
# agree, 131 are seen only by the marker, 0 only by the text. The marker is the authority here;
# the text is the fallback for a census without the column.
MEM = re.compile(r"\[\s*(?P<b>[a-z0-9]{2,4})\s*\+\s*(?P<i>[a-z0-9]{2,4})\s*"
                 r"(?:\*\s*(?P<n>[1248])\b)?", re.I)
ARR = re.compile(r"\[\s*(\d+)\s*\]\s*$")
W = re.compile(r"\b(byte|word|dword|qword|xmmword) ptr", re.I)
WID = {"byte": 1, "word": 2, "dword": 4, "qword": 8, "xmmword": 16}

CENSUS = {
    "save-header-accesses.tsv": "SaveImageHeader",
    "save-payload-accesses.tsv": "SavePayload",
    "battle-unit-accesses.tsv": "BattleUnit",
    "actor-storage-record-accesses.tsv": "ActorStorageRecord",
    "actor-manager-record-accesses.tsv": "ActorManagerSlot",
    "battle-stats-record-accesses.tsv": "BattleStatsRecord",
    "battle-state-block-accesses.tsv": "BattleSystemState",
    "result-record-accesses.tsv": "BattleResultRecord",
    "movement-context-accesses.tsv": "MovementContext",
    "secondary-context-accesses.tsv": "SecondaryContext",
    "game-setting-config-accesses.tsv": "GameSettingConfig",
}

paths = {os.path.basename(p): p for p in glob.glob(os.path.join(DB, "**", "*-accesses.tsv"),
                                                   recursive=True)}
groups = collections.defaultdict(list)      # (type, func, breg, ireg, scale) -> rows
for fn, t in CENSUS.items():
    p = paths.get(fn)
    if not p:
        continue
    for n, l in enumerate(io.open(p, encoding="utf-8")):
        if not n:
            continue
        c = l.rstrip("\n").split("\t")
        if len(c) < 6:
            continue
        txt = c[5].lstrip()
        if txt.startswith("nop") or txt.startswith("lea"):
            continue          # padding is not an access; a lea reads nothing
        marked = len(c) > 7 and c[7].strip() == "idx"
        m = MEM.search(c[5])
        if not m or not (marked or m.group("n")):
            continue
        try:
            off = int(c[3], 16)
        except ValueError:
            continue
        wm = W.search(c[5])
        rt = c[6] if len(c) > 6 else ""
        groups[(t, c[1], rt, m.group("b").lower(), m.group("i").lower(), (int(m.group("n")) if m.group("n") else 1))].append(
            (off, c[2], WID.get(wm.group(1).lower()) if wm else 0, c[5].strip()))

TYPENAMES = set()
for _n, _l in enumerate(io.open(os.path.join(DB, "_types", "types.tsv"), encoding="utf-8")):
    if _n and _l.strip():
        TYPENAMES.add(_l.split("\t")[0])

fields = collections.defaultdict(dict)
for n, l in enumerate(io.open(os.path.join(DB, "_types", "fields.tsv"), encoding="utf-8")):
    if not n:
        continue
    c = l.rstrip("\n").split("\t")
    if len(c) > 4:
        try:
            fields[c[0]][int(c[1], 16)] = (int(c[2]), c[3], c[4].strip())
        except ValueError:
            pass


def covering_array(t, off):
    """A declared row whose extent covers off - an array, or a reference to another store type.

    It need not start at off. Accepting only arrays counted SavePayload's byte bitmaps at +0x1000
    and after as undeclared when all of them sit inside persistentFlagPayloadRegion, a 5432-byte row
    at +0 whose ctype is PersistentFlagPayload. A sub-object declaration covers its interior exactly
    as an array does. A plain scalar row covers nothing beyond itself, so `sz > 8` is required before
    a non-array row is allowed to cover anything.
    """
    for o, (sz, nm, ct) in fields[t].items():
        if not (o <= off < o + sz):
            continue
        if ARR.search(ct):
            return o, nm, ct, sz
        if sz > 8 and ct.rstrip("*") in TYPENAMES:
            return o, nm, ct, sz
    return None


und = collections.defaultdict(list)
n_cov = n_und = 0
for k in sorted(groups, key=lambda k: (k[0], min(r[0] for r in groups[k]))):
    t, fn, rt, b, i, sc = k
    rows = sorted(set(groups[k]))
    allo = sorted({r[0] for r in rows})
    runs, cur = [], [allo[0]]
    for a, b in zip(allo, allo[1:]):
        (cur.append(b) if b - a < sc else (runs.append(cur), cur.__setitem__(slice(None), [b])))
    runs.append(cur)
    for offs in runs:
        offs = list(offs)
        sub = [r for r in rows if r[0] in set(offs)]
        if covering_array(t, offs[0]):
            n_cov += 1
            continue
        n_und += 1
        und[t].append((offs, sc, fn, sub))

print("UNDECLARED INDEXED TABLES  (no declared array covers the group's lowest offset)")
print()
for t in sorted(und):
    print("== %s" % t)
    for offs, sc, fn, rows in sorted(und[t], key=lambda g: g[0][0]):
        span = offs[-1] - offs[0]
        wid = sorted({r[2] for r in rows if r[2]})
        d = fields[t].get(offs[0])
        print("   base <= +0x%05X  scale %d  %d member offset(s) spanning %d byte(s)  widths %s"
              % (offs[0], sc, len(offs), span, "/".join(str(w) for w in wid) or "?"))
        print("        in %s   e.g. %s" % (fn[:52], rows[0][3][:60]))
        if len(offs) > 1:
            print("        members at +%s" % ", +".join("0x%X" % (o - offs[0]) for o in offs))
        print("        store at that offset: %s"
              % ("%s %s size %d" % (d[1][:24], d[2][:18], d[0]) if d else "no field row"))
    print()
print("access groups covered by a declared array : %d" % n_cov)
print("access groups NOT covered                 : %d" % n_und)

# ---- the controls, run here rather than asserted in prose -------------------------------------
# POSITIVE: where the store independently declares an array at an offset the censuses index, the
# observed scale must divide the declared element size. NEGATIVE: measure how often a random pairing
# would also pass, because divisibility by 2 is nearly free. A report whose positive control cannot
# run, or whose margin over the base rate is nil, proves nothing and must not be trusted.
agree = disagree = 0
scales = []
for t in sorted(groups):
    pass
for k in groups:
    t, fn, rt, b, i, sc = k
    for off, site, w, txt in groups[k]:
        d = fields[t].get(off)
        if not d:
            continue
        m = ARR.search(d[2])
        if not m:
            continue
        cnt = int(m.group(1))
        if not cnt or d[0] % cnt:
            continue
        elem = d[0] // cnt
        scales.append(sc)
        if elem and elem % sc == 0:
            agree += 1
        else:
            disagree += 1
            print("  CONTROL FAILURE  %s +0x%X scale %d vs declared element %d" % (t, off, sc, elem))

els = []
for t in fields:
    for o, (sz, nm, ct) in fields[t].items():
        m = ARR.search(ct)
        if m and int(m.group(1)) and sz % int(m.group(1)) == 0:
            els.append(sz // int(m.group(1)))
print()
print("POSITIVE CONTROL  scale divides the declared element size: %d agree, %d disagree"
      % (agree, disagree))
if not agree:
    print("NOTHING PROVED - no declared array coincided with an indexed access")
    raise SystemExit(2)
if els:
    exp = sum(sum(1 for e in els if e % sc == 0) / float(len(els)) for sc in scales)
    print("NEGATIVE CONTROL  same scale mix against %d declared element sizes would pass %.1f of %d"
          % (len(els), exp, len(scales)))
    if exp >= 0.95 * len(scales):
        print("BASE RATE TOO HIGH - the positive control cannot discriminate here")
        raise SystemExit(2)
raise SystemExit(1 if disagree else 0)
