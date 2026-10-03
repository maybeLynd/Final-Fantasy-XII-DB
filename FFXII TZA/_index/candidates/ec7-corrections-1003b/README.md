# SWE2-EC7's lines corrected at the bytes, set B - the 00297C10 matched row, the 004309C0 combiner tail, the 00399B80 / 0039A150 transforms (SWE2-EC7, 2026-10-03)

*SWE2-EC7, operated by a Claude stand-in (Opus 5.5) while the lane's Devin session was rate-limited. Requests:
`OPUS-REQ-EC7-00297C10-MATCHED-ROW-1003`, `FABLE-REQ-EC7-RANDOMNESS-PAGE-COMBINER-1003`,
`FABLE-REQ-EC7-TRANSFORM-PRIMITIVES-0039A150-1003`. None is disputed. Each edit strikes the old text and states the
reading the bytes support. Applier: [`apply_ec7corr_b.py`](apply_ec7corr_b.py), 4 edits.*

- **00297C10** (the widget-message page, EC7's batch-140 row). A matched row (bit `0x2` of byte `+0x26` in either
  half, and dword `+0xB0` = `[rsi+4]`) jumps from `00297C45` straight to the tail at `00297CE2` and never calls
  `003F89C0`, so its callbacks are kept. Only a free row is initialised. This is OPUS's replacement text, which
  SWE2-AUDIT-SPEC accepted in its OV-42 gauge-binding review.
- **004309C0's combiner tail** (the randomness page, section 6 table). It is `004307C0`, tail-jumped at `00430A56`.
  `00430540` is the per-channel keyed evaluator it calls. This is FABLE's SD-197 reading (FABLE's sd197/sd199 folder,
  not yet at HEAD).
- **00399B80's return** (the transform-primitives page, the `00434CD0` paragraph). It returns 1 on the first vertex
  that fails the range test and 0 when every vertex passes.
- **0039A150 / 00399B80** (the same page, the 2026-09-17 note). They are project / range-test / pack transforms, not
  scalar-blend members. FABLE executed both under Unicorn (FABLE's SD-199 remainder folder, not yet at HEAD, check
  133 PASS / FAILS 0). The static sites are re-checked here.

## Consumer check (SWE2-EC7)

affected: `Database/FFXII TZA/16-UI/Widget-Object-Model/the-widget-message-protocol.md`
affected: `Database/FFXII TZA/02-Resource-And-Asset-Pipeline/Authored-Expressions/how-an-authored-number-gets-its-randomness.md`
affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md`

- consumer: the three pages: revised-here.
- consumer: the `003F89C0` and `003F8A50` rows on the widget page: agree (they name `00297C10` as a caller, which the
  free path still is).
- consumer: the SPEC review record of the OV-42 gauge binding: agrees (it is the source of the reading).

run: `ec7_corr_b_check.py` at 33eb7192f (FAILS 0, [output](ec7_corr_b_check.out)) - [script](ec7_corr_b_check.py)
