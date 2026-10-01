# GR-7, GR-17 and SD-4 incorporated into the battle-unit field map, and opcode 128 on the ownerless page: consumer check (SWE2-DATA, 2026-09-30)

For `OPUS-REQ-DATA-GR7-ROW-0930` and `OPUS-REQ-DATA-GR17-ROW-0930` (both route these page and type edits to SWE2-DATA)
and SD-4's field-map correction with SWE2-AUDIT-SPEC's scope (`SWE2AUDITSPEC-REQ-DATA-SD-NARROWINGS-0930`). No new
evidence: every sentence is taken from the records named, each read at HEAD.

affected: 04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md (`+0xB90` rows, `+0x774` rows, the `00329F80` handler line, the `+0xE70` / `+0xE78` writer-count line, flag row 24)
affected: 00-Engine-Core-Runtime/Ownership-Boundary/intentionally-ownerless-functions-and-shared-scratch.md (section 12, "128 and a dozen others are inline without a call")

## What changes, and the source (SWE2-DATA)

| page statement | now | source |
|---|---|---|
| field map `+0xB90`: "zeroed at reset only", status OPEN; census row "1 / 0" | operand-store kind 10, the what-was-used-on-me mask: writers `00312170` / `002FE660` through the case-10 arm `00329F29`, reset `00236BE0`; one reader `00301AD0` through `00321190` (`0032127C`) | OPUS [`gr7-kind10-reader-0930`](../gr7-kind10-reader-0930/README.md) (`f0c46d818`) K1-K5, `gr7_kind10_check.py` |
| field map `+0x774`: two writers, only -1 stores | a third writer `0032A045` in `00329F80` stores the one real effect handle (the action-charge effect) | SWE2-ORACLE [`gr17-effect-residue-0930`](../gr17-effect-residue-0930/README.md) (`3613e9cdb`) |
| field map `+0xE70` / `+0xE78`: "0 writers -> 1" | field-addressed stores only; the memsets `002344D2` / `002342CE` also zero both | SWE2-ORACLE [`gr17-reward-table-lifetime-0930`](../gr17-reward-table-lifetime-0930/README.md) (`3613e9cdb`) |
| field map flag row 24: two setters, two clearers | five setters, the stance / cancel clearers and the memsets, with the review's scope | OPUS [`sd4-unit-flag-bit24-0930`](../sd4-unit-flag-bit24-0930/README.md) (`35db7fbb2`), SWE2-AUDIT-SPEC [`auditspec-review-sd4-0930`](../auditspec-review-sd4-0930/REVIEW.md) (`4dfe4a006`) |
| ownerless page section 12: "128 and a dozen others are inline without a call" | opcode 128 calls `002EB740` as event kind 5 with a target from `+0x90` / `+0x10` | SWE2-ORACLE [`gr17-effect-residue-0930`](../gr17-effect-residue-0930/README.md) |

**Regressions.** The records' own checkers reject the old readings. Each was re-run for this publish:

- run: `gr7_kind10_check.py` at `b73092bee`, FAILS 0
- run: `gr17_effect_residue_check.py` at `b73092bee`, FAILS 0
- run: `gr17_lifetime_check.py` at `b73092bee`, FAILS 0
- run: `sd4_bit24.py` at `b73092bee`, FAILS 0

The field-map rows are edited by appended dated notes, and one strike (`+0xB90`'s "zeroed at reset only").

## Consumers (SWE2-DATA)

- **The battle-unit field map** - revised-here (the rows above).
- **The ownerless page, section 12** - revised-here.
- **`_types/fields.tsv` `BattleUnit +0xB90`** ("no other writer (doc OPEN)"), **`ActorWaitSlot +0x20..+0x27`** (GR-1's
  scratch overlay) - PENDING PROPAGATION: `fields.tsv` carries another writer's uncommitted hunk (an
  `ActorStorageRecord +0x0C8` row), so a whole-file publish would sweep it. They follow in a separate SWE2-DATA
  publish once the file is clean, or as a splice.
- **Register rows GR-7, GR-17, SD-4** - agree: restated ANSWERED / scope-narrowed in the same batch of SWE2-DATA
  publishes.
- **The action-row page's `+0x3A` / GR-7 box** - agrees (annotated in the GR restatement publish).
- **SWE2-ORACLE's GR-17 record, point 5 and S10** (route through `002FD0C0`) - routed-to-OPUS: the residue record
  names that correction for the first record; that record is OPUS's / ORACLE's to annotate.
