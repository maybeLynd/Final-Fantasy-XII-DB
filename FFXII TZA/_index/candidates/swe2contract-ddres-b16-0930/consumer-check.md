# Consumer check: DD batch 16 correction on the gambit page (SWE2-CONTRACT for OPUS, owner re-status pending, 2026-10-01)

SWE2-CONTRACT's batch 16 (this folder's README) closed the prose residue of one page. Two sentences about the AI
order record's flag bit `0x04` were wrong and are struck: the bit has a reader. The page's other residue sentences got
dated pointer notes, which strike nothing. No status word was moved. OPUS re-statuses after its owner read.

- **Corrects:** in gambit-evaluation-and-enmity.md: section 7's Z-19 box, "`0x04` unread"; and section 8g's Z-19
  table, the `0x0004` row's "**no reader found** — the shifted test stops at entry 2" and "authored but unread". The
  bit is read by `BattleUnit_CanAdvanceCombatNavigation` (`00325D90`, at `00325DF4`). While the unit's current order
  carries it, the gate returns 0, and `BattleUnit_UpdateCombatNavigationStep` (`00325BB0`) then does not route or
  solve a step.
- **Affected:** 09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's own section 7 box, section 8g table and the section 8l pointer | revised-here |
  | OPEN-QUESTIONS.md Z-19 (status cell: "`0x04` authored (256 records) but unread") | disagrees: `0x04` is read at `00325DF4` (N4–N6). Routed to the row's owner, not edited |
  | CONTRACT-gambit-walk.md §14 item 2 ("`0x0004` is authored but has no reader") and its evidence row ("`0x0004` unread") | disagrees, for the same reason. Routed to the contract's owner, not edited |
  | Battle-Locomotion/battle-locomotion-steering-and-recovery.md (`00325BB0`, the step's entry from CombatAction) | untouched; agrees. It does not describe the step's opening gate, and this batch adds the gate's order-flag condition |
  | 04-Actor-Entity/Battle-Unit/battle-unit-accesses.tsv (`00325D90` `BattleUnit_CanAdvanceCombatNavigation`, the `+0x708` read at `00325DE8`) | agrees and is cited |
  | PROGRAM-STATE.md and _inbox/FABLE.md (dated log entries: "0x04 authored-unread", "`0x04` unread") | untouched: historical log entries, superseded by this record |
  | _experiments evidence snapshots of the register (question-ledger.md, 03-OPEN-QUESTIONS.md preimages) | untouched: frozen evidence copies |

- **Regression:** Database/FFXII TZA/_index/candidates/swe2contract-ddres-b16-0930/b16_checks.py (89 checks). N4–N6
  reject the "no reader" reading. They do it by taint census of every record-pointer access covering `+4`, finding
  exactly eleven accesses, with the seven Z-19 reader sites as positive controls. The only bit-2 test among them is
  `00325DF4`. N3 keeps the true half ("the shifted test stops at entry 2"). Z1–Z2 confirm the struck text is kept
  verbatim.
  run: _index/candidates/swe2contract-ddres-b16-0930/b16_checks.py at d526b865b (FAILS 0)
