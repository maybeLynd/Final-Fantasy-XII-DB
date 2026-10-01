"""Cross-check every declared field width against its own access census.

Three artefact classes make a census say a width it does not mean, and all three were
found the hard way while populating the store:

  * multi-byte NOPs -- `nop dword ptr [rax + rax]` pads with a ModRM memory operand and
    touches nothing, but reads as a 4-byte access. 48 rows across the eight censuses.
  * unrolled SIMD block copies -- a function moving a region emits a run of `movups
    xmmword`, none of which is a 16-byte field. This one corrupted a published layout
    twice before it was recognised.
  * indexed accesses with no displacement -- `[rcx + rax*8]` is filed at +0x000 though
    it is an array element reached through the base.

This excludes all three and reports every declared row whose size no longer matches.
A row declared as an ARRAY or a whole SPAN is expected to disagree with its element
width, so those are listed separately rather than as findings.

    check_census_widths.py
"""
import collections
import glob
import io
import os
import re

NOP = re.compile(r"^\s*nop\b", re.I)
INDEXED = re.compile(r"\[\s*\w+\s*\+\s*\w+\s*\*\s*[1248]\s*\]")
FORMS = (("xmmword", 16), ("qword ptr", 8), ("dword ptr", 4), ("byte ptr", 1))

CENSUS = {
    "SaveImageHeader": "save-header-accesses.tsv",
    "SavePayload": "save-payload-accesses.tsv",
    "BattleUnit": "battle-unit-accesses.tsv",
    "ActorStorageRecord": "actor-storage-record-accesses.tsv",
    "ActorManagerSlot": "actor-manager-record-accesses.tsv",
    "BattleStatsRecord": "battle-stats-record-accesses.tsv",
    "BattleSystemState": "battle-state-block-accesses.tsv",
    "BattleResultRecord": "result-record-accesses.tsv",
}
paths = {os.path.basename(p): p
         for p in glob.glob("Database/FFXII TZA/**/*-accesses.tsv", recursive=True)}


def width_of(ins):
    if NOP.match(ins):
        return None
    i = ins.lower()
    for tok, w in FORMS:
        if tok in i:
            return w
    if "word ptr" in i:
        return 2
    return None


def clean(path):
    per = collections.defaultdict(collections.Counter)
    xmm = collections.Counter()
    raw = []
    for n, line in enumerate(io.open(path, encoding="utf-8")):
        if n == 0:
            continue
        c = line.rstrip("\n").split("\t")
        if len(c) < 6:
            continue
        try:
            off = int(c[3], 16)
        except ValueError:
            continue
        if off == 0 and INDEXED.search(c[5]):
            continue
        w = width_of(c[5])
        if w is None:
            continue
        if w == 16:
            xmm[c[0]] += 1
        raw.append((off, w, c[0]))
    bulk = {fn for fn, n in xmm.items() if n >= 4}
    for off, w, fn in raw:
        if w == 16 and fn in bulk:
            continue
        per[off][w] += 1
    return per


declared = collections.defaultdict(dict)
for line in io.open("Database/FFXII TZA/_types/fields.tsv", encoding="utf-8"):
    c = line.rstrip("\n").split("\t")
    if len(c) > 2 and c[0] in CENSUS:
        try:
            declared[c[0]][int(c[1], 16)] = (int(c[2]), c[3], c[4] if len(c) > 4 else "",
                                             c[8] if len(c) > 8 else "")
        except ValueError:
            pass

bad = 0
spans = []
deliberate = []
for tname, fname in CENSUS.items():
    if fname not in paths:
        print("no census for", tname)
        continue
    per = clean(paths[fname])
    for off, (size, name, ct, ev) in sorted(declared[tname].items()):
        c = per.get(off)
        if not c:
            continue
        best = c.most_common(1)[0][0]
        if size == best:
            continue
        if "WIDTH DELIBERATE" in ev:
            # A row may declare a width the census disagrees with, PROVIDED it says
            # why in its own evidence. A union span and a field whose writers and
            # readers use different widths are both legitimate; a check that stays
            # permanently red is one nobody reads, so the exception is explicit,
            # carried by the row itself, and listed here rather than hidden.
            deliberate.append((tname, off, size, name, dict(c)))
            continue
        if size > 16 or ct.endswith("]") or size in (10, 16) and ct.endswith("]"):
            spans.append((tname, off, size, name, dict(c)))
            continue
        widths = sorted(c)
        if best != min(widths) and c[min(widths)] >= c[best]:
            best = min(widths)
        if size != best:
            bad += 1
            print("  MISMATCH %-20s +0x%04X declared %-4d name=%-24s clean evidence %s"
                  % (tname, off, size, name[:24], dict(c)))
print()
print("declared whole (array or span) - disagreement expected: %d" % len(spans))
for tname, off, size, name, c in spans:
    print("  span     %-20s +0x%04X declared %-5d %-24s elements %s"
          % (tname, off, size, name[:24], c))
print()
print("declared deliberately against the census, with a reason in the row: %d" % len(deliberate))
for tname, off, size, name, c in deliberate:
    print("  stated   %-20s +0x%04X declared %-5d %-24s census %s"
          % (tname, off, size, name[:24], c))
print()
print("ROWS WHOSE DECLARED SIZE DISAGREES WITH THE CLEANED CENSUS: %d" % bad)
raise SystemExit(1 if bad else 0)
