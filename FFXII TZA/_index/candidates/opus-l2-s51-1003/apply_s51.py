"""apply_s51.py [--apply] - S-51: claim what BattleUnit +0x080 is, from the corridor contract's own resolution (OPUS,
2026-10-03). The row said "NOT CLAIMED: what the object is". CONTRACT-corridor-query-family.md (OPUS block 249/250) had
already resolved it: the corridor agent's +0x108 sub-record IS BattleUnit seen from +0x80. OPUS re-read the chain:
`00308673 lea rcx,[rbx+0x80]` -> `0030867A call 0033A240`; `00317E9D lea rcx,[rax+0x80]` -> `00317EA4 call 0033C9B0`;
each wrapper reaches 00336710 with that base as its second argument (0033C9B0: `0033C9C9 mov rdx, rcx`), and
00336710 stores it at agent+0x108 (`003367B4 mov qword ptr [rcx+0x108], rdx`). Replaces the one sentence; keeps the
row's measured extent, evidence and readiness. Idempotent; refuses on an uncommitted BattleUnit line. FAILS n."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
F = os.path.normpath(os.path.join(HERE, "..", "..", "..", "_types", "fields.tsv"))
OLD = ("NOT CLAIMED: what the object is, or its members on this base - the memset establishes an extent and a "
       "lifetime, nothing more.")
NEW = ("CLAIMED 2026-10-03 (OPUS, S-51, from CONTRACT-corridor-query-family.md blocks 249/250, chain re-read): this base "
       "is the unit as the corridor query sees it - the agent builder 00336710 stores it at agent+0x108 (003367B4), "
       "reached with rcx = unit+0x80 from nine of ten call sites (e.g. 00308673 lea / 0030867A call 0033A240; "
       "00317E9D lea / 00317EA4 call 0033C9B0, which passes it as rdx at 0033C9C9); the tenth passes an edited "
       "0x610-byte copy of this region (00301830). So agent+0x108's +0x10C/+0x110/+0x174 are this type's +0x18C, "
       "+0x190 and +0x1F4. Its members on this base are not separately claimed.")
b = io.open(F, encoding="utf-8", newline="").read()
row = [l for l in b.splitlines() if l.startswith("BattleUnit\t0x080\t")]
if len(row) != 1:
    print("BattleUnit 0x080 row: %d found (need exactly 1)" % len(row))
    print("FAILS 1")
    sys.exit(1)
if NEW in row[0]:
    print("ALREADY")
    print("FAILS 0")
    sys.exit(0)
if OLD not in row[0]:
    print("the old sentence is not in the row")
    print("FAILS 1")
    sys.exit(1)
d = subprocess.run(["git", "-C", os.path.dirname(F), "diff", "--", "fields.tsv"], capture_output=True, text=True).stdout
# 2026-10-03: ANY uncommitted line that is not this record's refuses - publishing fields.tsv would carry a peer's hunks
# sibling records apply_l2_set.py applied earlier from a clean store (their diff lines, named in $OPUS_APPLY_ALLOWED)
allowed = set(io.open(os.environ["OPUS_APPLY_ALLOWED"], encoding="utf-8").read().splitlines()) \
    if os.environ.get("OPUS_APPLY_ALLOWED") else set()
if any(not (OLD in l or NEW in l) and l[1:] not in allowed
       for l in d.splitlines() if l[:1] in "+-" and not l.startswith(("+++", "---"))):
    print("REFUSED: fields.tsv carries uncommitted lines that are not this record's (another lane's work)")
    print("FAILS 1")
    sys.exit(1)
if "--apply" not in sys.argv:
    print("DRY")
    print("FAILS 0")
    sys.exit(0)
b2 = b.replace(row[0], row[0].replace(OLD, NEW), 1)
tmp = F + ".opus-tmp"
io.open(tmp, "w", encoding="utf-8", newline="").write(b2)
os.replace(tmp, F)
print("APPLIED")
print("FAILS 0")
