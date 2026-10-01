"""rc5_action_word24.py - RC-5 residue item "the authored +0x24 word of the record 00306BD0 hands to 00309230" (FABLE, 2026-09-29).

00309230 (BattleSpecialSequence_DeriveActionPresentationCode) returns the record's unsigned word +0x24 (003092C5), except
for the one row whose pointer equals the computed special entry, where it indexes the 13-entry actor-type table (42, 45,
.., 78). The record is an action-table row: 0030CE10 tests flags +0x0C bit 30 (0030CE93) and only then reaches 00306BD0
(0030CF0D), which calls 00309230 (00306C4D) and hands EAX to 0032FC30 as the set id (00306C56) - ASTRA's
ov42-special-action-preconditions packet, SPECIAL-ACTION-RESULT.md "Original path".
Data: the nine retained action tables (action-selectors-01/tables/action_data_<lang>.st2e = the pack bytes from the st2e magic; 543 rows x 60 bytes; layout
as ASTRA's check-action-selectors.py: t = u32 @0x3C; count, stride, rows @ t+4; word @ t+rows+i*60+0x24).
Output: per language, the +0x24 words of the bit-30 rows, and which of them are set ids ORACLE's rc5_paths.tsv names
(kind-8, 'us' names), in particular the sum_<x>0001 names that set flag A.
Control: ASTRA's reported invariants reproduce - 543 rows, stride 60, 68 FFFF words per pack, and rows 511..534 carry
FFFF with flags 0x40000211."""
import collections, csv, io, os, struct, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
TAB = os.path.join(DB, "_experiments", "evidence", "ov42-special-action-preconditions", "action-selectors-01", "tables")
PATHS = os.path.join(DB, "_index", "candidates", "rc5-event-slot-routes-0930", "rc5_paths.tsv")
names = {}
for r in csv.DictReader(io.open(PATHS, encoding="utf-8"), delimiter="\t"):
    if r["kind"] == "8" and r["locale"] == "us" and r["regex"] == "MATCH":
        names[int(r["set_id"])] = (r["stored_name"], r["class"])
fails = 0
per = {}
for fn in sorted(os.listdir(TAB)):
    blob = open(os.path.join(TAB, fn), "rb").read()
    t = 0                                    # the retained file is the table itself: blob[t:end] of the pack, 'st2e' first
    if blob[:4] != b"st2e":
        fails += 1; print("FAIL not an st2e table", fn); continue
    count, stride, rows = struct.unpack_from("<III", blob, t + 4)
    base = t + rows
    words = [struct.unpack_from("<H", blob, base + i * stride + 0x24)[0] for i in range(count)]
    flags = [struct.unpack_from("<I", blob, base + i * stride + 0x0C)[0] for i in range(count)]
    ffff = sum(1 for w in words if w == 0xFFFF)
    band = all(words[i] == 0xFFFF and flags[i] == 0x40000211 for i in range(511, 535))
    ok = count == 543 and stride == 60 and ffff == 68 and band
    fails += not ok
    b30 = [(i, words[i]) for i in range(count) if flags[i] & 0x40000000]
    vals = collections.Counter(w for i, w in b30)
    per[fn] = (b30, vals)
    print("%s: rows %d stride %d FFFF %d band511-534 %s -> CONTROL %s; bit-30 rows %d, their +0x24 words: %s" % (
        fn, count, stride, ffff, band, "PASS" if ok else "FAIL", len(b30), dict(sorted(vals.items()))))
us = per.get("action_data_us.st2e")
if us:
    b30, vals = us
    print("\n'us' bit-30 rows by +0x24 word -> the set id's name (rc5_paths.tsv):")
    for w in sorted(vals):
        print("  %5s x%-3d rows %s -> %s" % ("FFFF" if w == 0xFFFF else w, vals[w],
              [i for i, x in b30 if x == w][:12], names.get(w, ("(no kind-8 name)", ""))))
    flagA = sorted(w for w in vals if names.get(w, ("", ""))[1].startswith("A("))
    print("sum_<x>0001 (flag A) set ids reached by a bit-30 row's +0x24:", flagA or "NONE")
same = len({tuple(sorted(v[1].items())) for v in per.values()}) == 1
print("all nine languages give the same bit-30 word multiset:", same)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
