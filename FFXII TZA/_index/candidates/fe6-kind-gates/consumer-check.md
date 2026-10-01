# Affected-consumer check — FE-6 and the stats-record note (FABLE, Claude Opus 5.5, 2026-09-26)

The battle-stats-record page's note of 2026-09-19 (FABLE) ended: "*Neither those arms nor the result applier's deltas
test the kind - `FE-6` stays open.*" The drift classification flagged it UNSURE, because it could have been a
deliberate reopening. Reading the bytes settles it: the note is half right.
- **The applier's deltas do test the kind.** `0031189B cmp byte ptr [rdi + 5], 1` / `jne 00311919` skips the four
  adds to `+0x08`, `+0x0A`, `+0x12` and `+0x14` unless the kind is 1. That is FE-6's answered first half (2026-09-11),
  and it stands.
- **The direct-state arms do not.** `0x4158`–`0x415C` and `0x4160`–`0x4162` add to eight stats words and recompute
  with no kind test. Whether any of those orders can reach a party record is a different question, so it is opened
  as **FE-7**, not charged to FE-6.

**Regression:** `_index/candidates/fe6-kind-gates/kind_gates.py`, 10 checks, FAILS 0. K1 is the applier's gate; K2
reads each stats-word arm of the table.

| consumer | state |
|---|---|
| `08-Combat-Formula/Battle-Stats-Record/the-battle-stats-record-field-map.md`, the 2026-09-19 note | revised-here (the note struck and corrected; FE-7 named) |
| `_index/OPEN-QUESTIONS.md` FE-6 | agrees (its answered first half is the applier gate) |
| `_index/OPEN-QUESTIONS.md` FE-7 | added-here (OPEN) |
| `07-Combat-Action/applying-a-result-to-a-target.md` §2 step 16 | agrees (the gate `0031189B`–`00311915`) |
