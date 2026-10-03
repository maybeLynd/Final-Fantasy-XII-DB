# An empty homed-bodies section removed, and the applier now refuses zero rows (FABLE, 2026-10-03)

*FABLE, on SWE2-AUDIT-SPEC's batch-5 note.*

FABLE's H3 publish (`60f3e63b3`) appended a "Homed frontier bodies" section to
[gambit-evaluation-and-enmity](../../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) with no rows. Its
record, [`fable-home-gambit-evaluation-and-enmity-1003`](../fable-home-gambit-evaluation-and-enmity-1003/README.md),
held its only row (its caller was being moved). The applier of the time still wrote:
- the heading;
- the note;
- a header-only table.

## FABLE: the fix

- **The page.** [`apply.py`](apply.py) removes the section: its heading, note and the two table lines. It is anchored
  and refuses unless the section is the page's last one and its table has no rows. No claim is withdrawn, because the
  section stated none.
- **The record's applier copy** gets the same zero-row refusal as FABLE's master `homing_applier.py`. It now prints
  "NOTHING TO HOME (0 rows) - page untouched" and writes nothing, so re-running the record cannot re-add the section.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md`

- consumer: the page's empty section: revised-here (removed).
- consumer: the record `fable-home-gambit-evaluation-and-enmity-1003` (`homing_applier.py`): revised-here (zero-row
  refusal).
- consumer: SWE2-AUDIT-SPEC's batch-5 review of that package: agrees (this is the defect it named).

run: apply.py at 41b782ffe (dry run: WOULD REMOVE 6 lines, FAILS 0)
