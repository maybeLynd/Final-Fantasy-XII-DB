"""UNRESOLVED rows whose MEANING is already established enough to carry a name.

A field's name is FABLE's call, not OPUS's - several rows say so outright ("Name is FABLE's", "Name
requested from FABLE"). What OPUS can do is say which rows are ready: the ones whose meaning cell
already states a definite role in the indicative, rather than recording a width, a sentinel or a
list of access sites.

The filter is deliberately about SHAPE, not confidence: a meaning that opens "the X that ..." or
"a X which ..." is a claim about what the field IS. One that opens "a 32-bit value read and written
by plain dword moves" is a claim about how it is touched. The second is not nameable and the first
usually is - but every row still has to be read, which is why this emits a worklist and not names.

usage: nameable_rows.py [--type NAME] [--min-meaning 120]
"""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
STORE = (sys.argv[sys.argv.index("--store") + 1] if "--store" in sys.argv
         else os.path.join(ROOT, "Database", "FFXII TZA", "_types", "fields.tsv"))

only = sys.argv[sys.argv.index("--type") + 1] if "--type" in sys.argv else None
minlen = int(sys.argv[sys.argv.index("--min-meaning") + 1]) if "--min-meaning" in sys.argv else 120

# a role stated in the indicative, at the very start of the meaning
ROLE = re.compile(r"^(?:the|a|an)\s+[A-Za-z][A-Za-z0-9 \-]{2,40}?\b"
                  r"(?=\s+(?:that|which|the|it|for|of|this|is|holds|carries|selects|counts|"
                  r"indexes|drives|gates|receives|published|written|read|applied)\b)", re.I)
# THE ROW ANSWERS IN THE SECOND CLAUSE, and the first version of this filter never read it (FABLE,
# 2026-09-16, returning 5 of 25). Selecting on the OPENING of the meaning is a test of grammar, not
# of what the row goes on to say: nineteen of twenty-five opened in the indicative and then withdrew
# - "+0x210 ... ROLE NOT ESTABLISHED", "+0x15C ... what consumes the value is not established here",
# MovementContext +0x034 "records the type and that fact rather than a meaning it cannot support".
# None of them overreached; the filter did. A cell that retracts anywhere is not waiting on a name.
WITHDRAWN = re.compile(r"not established|is not claimed|no censused reader|cannot support|"
                       r"not settled|is a reading|nothing (?:here )?names|what it (?:measures|holds|"
                       r"consumes) is not|role not established", re.I)
# shapes that describe ACCESS rather than role, and are therefore not ready
NOT_READY = re.compile(r"^(?:a|an|the)?\s*\d*[\- ]?(?:32-bit|16-bit|8-bit|4-byte|8-byte|2-byte|"
                       r"1-byte|byte|word|dword|qword)\b|^\s*\d+\s+(?:writes?|reads?)\b|"
                       r"^(?:MINUS ONE|SIGNATURE|width )|"
                       # A REMARK ABOUT THE STORE IS NOT A MEANING: thirteen ActorStorageRecord rows
                       # open "the field map marks this offset *not in the store*", which says where
                       # the field is recorded and nothing whatever about what it holds.
                       r"^the field map\b", re.I)

rows = [l.rstrip("\r").split("\t") for l in io.open(STORE, encoding="utf-8").read().splitlines()]
ready = []
for r in rows[1:]:
    if len(r) < 9 or r[3] != "UNRESOLVED":
        continue
    if only and r[0] != only:
        continue
    m = r[5].strip()
    if len(m) < minlen or NOT_READY.match(m) or WITHDRAWN.search(m):
        continue
    hit = ROLE.match(m)
    if not hit:
        continue
    ready.append((r[0], r[1], hit.group(0).strip(), m))

print("%d UNRESOLVED row(s) whose meaning opens with a stated role\n" % len(ready))
by_type = {}
for t, off, phrase, m in ready:
    by_type.setdefault(t, []).append((off, phrase, m))
for t in sorted(by_type, key=lambda k: -len(by_type[k])):
    print("%s  (%d)" % (t, len(by_type[t])))
    for off, phrase, m in sorted(by_type[t])[:8]:
        print("   %-7s %s" % (off, m[:118]))
    print()
