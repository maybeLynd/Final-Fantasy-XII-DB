# Re-landing FABLE's R-5 drain-guard correction after SWE2-CONTRACT's stale overwrite (SWE2-CONTRACT, 2026-10-03)

**What happened.** FABLE corrected the UI request router's R-5 in `fa2f75e21` (2026-09-26 03:25) and the dependent
world-tick prose in `30b2fd926` (02:59). SWE2-CONTRACT's batch publish `95b1f3a4c` (2026-09-26 11:12, "38 staged
packages") was built on a stale preimage of both files and restored the pre-correction text. HEAD therefore said
again that the drain guard tests `+0x3E` bit 7 and that a blocked request is deferred. SWE2-AUDIT-SEM found it (S-36
defect D1 in `auditsem-l2-sample-1003`, commit `bcbf43096`). **The regression is SWE2-CONTRACT's: `95b1f3a4c`.** This
publish was written by the Claude stand-in operating SWE2-CONTRACT while the lane's Devin session was rate-limited.

affected: `16-UI/CONTRACT-ui-request-router.md` (R-5)
affected: `00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md` (the EX-3 note and the third entry gate)
affected: `00-Engine-Core-Runtime/Developer-Tuning-Console/the-event-slot-panel-and-its-dead-feeder.md` (one pointer line)

## The change (SWE2-CONTRACT)

- **The router contract and the world-tick page get FABLE's text back byte for byte.** `restore_edit.py`
  (SWE2-CONTRACT scratch, `Database/Tools/work/SWE2-CONTRACT/standin/regr/`) takes the old and new blocks from the git
  objects `fa2f75e21^`/`fa2f75e21` and `30b2fd926^`/`30b2fd926`, so nothing is retyped. These are the only hunks on
  those two pages. Both pages carried a peer's uncommitted edits at publish time; those were left in the worktree and
  are not in this commit.
- **One line on the event-slot page.** Its "2026-09-30 pointer" sentence was written by SWE2-CONTRACT after
  `95b1f3a4c` and copied the reverted bit-7 wording, so it carried the regression to a third page. It now reads bit 0
  and names FABLE's reading. This is the only text not taken from FABLE's commits.

## The bytes, re-read for this publish (SWE2-CONTRACT)

Control: [`check.py`](check.py), output in [`check.out`](check.out). It reads the shipping image only and never a page.
run: check.py at 51dc0cb0be7d35c987fc9e5891f0eb3dfd723f81 - FAILS 0.

- **G1, the drain's guard:** `movzx` of byte `+0x3E`, then `shl al, 7` / `sar al, 7`, then OR with `+0x38`, then `jne`.
  The shift pair keeps bit 0.
- **G2, the probe `002E0540`:** the same pair on `cl`.
- **G3, the device term:** `mov eax, 1; ret`. The `cmove esi, ebp` after it cannot fire, so the transition test never
  blocks.
- **G4, the not-ready arm:**
  - A non-zero answer from the slot-0 readiness query zeroes `r8b`.
  - It stores the zero register into the request word, its argument and the second byte, then jumps to the store
    that writes `r8b` into the pending byte.
  - The request is discarded, not deferred.
- **S1, sensitivity:** simulating the shift pair gives block for a bit-0-only byte and dispatch for a bit-7-only byte.
  The reverted bit-7 reading predicts the opposite, so this control would fail on it.

## Consumers (EVIDENCE-POLICY rule 4a) (SWE2-CONTRACT)

- consumer: the router contract's R-5 — revised-here (FABLE's `fa2f75e21` text).
- consumer: the world-tick page, EX-3 note and the third entry-gate paragraph — revised-here (FABLE's `30b2fd926` text).
- consumer: the event-slot page's 2026-09-30 pointer line — revised-here.
- consumer: the field-runtime-pass page and the party roster page, both describing `002E0540` — agrees. Both already
  say `byte[+0x3E]` bit 0 sign-folded (or sign-extended) OR `byte[+0x38]`; no edit.
- consumer: OPUS's replay record `s36-opus-replay-request-router` (r45) — agrees. It measured `0x01` blocking and
  `0x80` dispatching, which is FABLE's text.
- consumer: the S-36 verdict row in the L2 verdicts — routed-to-SWE2-AUDIT-SEM. D1 is repaired by this publish. D2
  (undeclared router state), D3 (the runtime cell) and the re-score stay with the verdict owner.
- consumer: the router falsifier's U7 case, which tests only R-5's single call site (AUDIT-SEM point 7) —
  routed-to-SWE2-AUDIT-SEM as part of the same S-36 finding. This record's check.py is the guard-level regression.

**Regression:** `check.py` (above).

## Did `95b1f3a4c` revert anything else? (SWE2-CONTRACT)

Two independent sweeps over the 43 files it touched (all but TEAM.json):
1. AUDIT-SEM's `survive.py` since 2026-09-12. Hits attributed to `95b1f3a4c`: FABLE's `fa2f75e21` (11 of 11 added
   lines lost), FABLE's `30b2fd926` (3 of 3), and the generated `ADDRESS-INDEX.md`, whose rows are rewritten on every
   regeneration. There is nothing else.
2. A blame of every line `95b1f3a4c` removed against its parent, grouped by the peer commit that wrote it.
   Peer commits dated 2026-09-24 or later:
   - `30b2fd926` and `fa2f75e21` (FABLE): the two re-landed here.
   - `1905a7e58` (FABLE, shop stock ladders, 7 lines): **merged, not reverted.** The batch rewrote that §14 block, and
     FABLE's facts survive in the new text (11 rows, not 12; row 2 falls through `003153E1`).
   - `577806707` (SWE2-EC7, the thirty-two statuses, 4 lines): EC7's `002FA560` paragraph and its interior anchor were
     dropped by the batch, but **both are present at HEAD** (since corrected by OPUS on 2026-10-02). Nothing is
     outstanding.
   - Older peer lines the batch removed are the lane's own closures and rewrites of questions those pages posed (for
     example EH-1, BL-3, GE-1, the shop gate-kind census); each was read in the diff.
