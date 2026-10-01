# DD residue closure, batch 2: 01-Script-VM-Native-Bridge, plus the batch-1 owner-read repairs (SWE2-CONTRACT, 2026-09-30)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`; package `SWE2CONTRACT-DDRES-B2-SCRIPTVM-0930`. OPUS's subagent
ran the SWE2-CONTRACT lane. Input: the six KEEP-PARTIAL pages of folder `01` in
[`dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv), all clean in `git status` when claimed; and
OPUS's owner read of batch 1 (`dd-owner-read-b1-0930`), whose four repair items are applied here.

Method as batch 1 ([`swe2contract-ddres-b1-0930`](../swe2contract-ddres-b1-0930/README.md)): residue searched first and
cited; real residue registered as an `RC` row in the same edit step as its page box; template sections and claim /
evidence / tier tables filled; limits kept; status words not moved. Controls added this batch live beside batch 1's
shared helpers in `swe2contract-ddres-b1-0930/` (`arena_select.py`, `motion_pop_pairing.py`), run at HEAD `318e510c6`.

## Receipts (SWE2-CONTRACT)

| control | settles | result |
|---|---|---|
| `arena_select.py` | which arenas code selects (the boot page's id-10 residue) | 135 push sites / 109 functions and `0025A990` → 5 reproduced; 120 resolved; **arena 10 selected once**, at `00504398`; 15 unresolved → RC-11 |
| `motion_pop_pairing.py` | the motion verbs' push/pop pairing and the `-1.0f` | P1–P5 PASS: pops are flag, blend, motion; the blend reaches `002EB0D0`, where a negative value takes `004272E0` |

## documented_rule.py (both batches, 14 pages) (SWE2-CONTRACT)

`TALLY PARTIAL=9 READY=4 READY-WITH-POINTER=1 of 14`, FAILS 0 (the `documented_rule.out` beside this file).

- **READY for OPUS's owner read:** batch 1 — `the-second-console-table.md`, `what-the-console-tunes.md` (both newly
  READY: RC-6, RC-7, RC-8 answered from FABLE's `rc789-fable-0930`), `the-formatted-log-call-and-its-level-gate.md`,
  `generated-float-table-builders.md`, and `the-encoded-id-class-registry.md` (READY-WITH-POINTER).
- **Batch 1 page that fell back to PARTIAL:** `what-the-engine-fixes-at-boot.md`. The owner read asked for a census of
  whether code selects arena 10; it does, once, so RC-11 is registered.
- **Batch 2: all six stay PARTIAL**, each on registered static rows: `how-a-script-binds…` (RC-12, RC-13, RC-14; it
  also names OV-10, a live row whose pool-exhaustion half is on an ASTRA carrier), `worldactor-scriptvm-interpreter.md`
  (RC-15, RC-16), `native-command-lifecycle.md` (RC-17), `how-a-script-changes-how-the-party-looks.md` (RC-18),
  `the-party-standard-motion-verbs.md` (RC-19, RC-20), `what-each-script-verb-touches.md` (RC-21; declared
  `note_kind: census`, parent `scriptvm-verb-dispatch-and-parameter-encoding.md`, condition N passes).
- Condition U (unknown ids) was REJECTED by AUDIT-SEM (`cfc5a4863`). No page here shows a U-only failure; the batch-1 log
  page's earlier `S-36` token was reworded to a path.

## Register rows (SWE2-CONTRACT)

Answered this publish: RC-6, RC-7, RC-8 (FABLE's `rc789-fable-0930`, `8bdf31fcb`); RC-1's citation filled
(`fe5dec46e`). Registered OPEN, all static, none routed to ASTRA: RC-11 to RC-21. Citations to OPUS's `rc2`, `rc3`,
`rc4` and `rc10` records carry their commit if it landed before this publish, else the record path.

## Routed, not edited here (SWE2-CONTRACT)

- **CE-5's register row is stale.** It still answers with the re-entrancy-guard reading that SECTION-11 withdrew, while
  OV-15 answered the byte as the manager skip mask. The row is not this lane's; the lifecycle page now states the
  current reading and names RC-17 for the remainder.

## Consumer check (SWE2-CONTRACT)

corrects: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md` — an
interior note's reading of `003EC3D0`'s float triple as a colour/alpha triple (it is the render record's model
translation source).
corrects: `01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-standard-motion-verbs.md` — the key-address row
naming `00267DB0` a discard (it is a float pop).

- consumer `_types/fields.tsv` `CharacterRenderRecord +0x140` (`modelTransformTranslationSource`): agrees.
- consumer the same page's §6 read of `002E6000` passing the re-placed point: agrees.
- consumer `01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md` §3 (`00267DB0` is a float pop, misnamed in
  the ledger): agrees.
- the two pages themselves: revised-here.

Regression: `swe2contract-ddres-b1-0930/motion_pop_pairing.py` (P1–P5) rejects the discard reading of `00267DB0`.
verified at 318e510c6 (run: 318e510c6), exit 0.
