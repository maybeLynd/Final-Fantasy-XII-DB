# OPUS DD content work, folders 15–99: batch 1 (OPUS, 2026-09-30)

Board task `OPUS-DD-UNCLAIMED-15-99-0930`. It covers clean, unclaimed pages from the DD owner-read worksheet
(`_index/candidates/dd-owner-read-0929/worksheet.tsv`). FABLE holds 04–13, SWE2-CONTRACT 00–02, and
`OPUS-DD-TYPES-CRT-0930` 22/24.

## r2-force-fight-toggle.md: PARTIAL → DOCUMENTED

Page: [r2-force-fight-toggle.md](../../../15-Input/Modal-Toggles/r2-force-fight-toggle.md).

- **Why the status was stale.** The status line said SD-1 and SD-2 "stay open", but both register rows are ANSWERED
  (OPUS `473de1075` and `7573a1b87`).
- **The status line** now states what they answered.
- **§1 gains the answer in player terms.** With `FLEEING` on:
  - units without Confuse or Berserk stop chaining combos, enemies included;
  - a spawned unit's status change clears its engaged state;
  - enemy AI order checks and enemy movement take the other threshold and divisors;
  - the stance and reason `0x24` change only for the party;
  - the label is drawn letter by letter while the arming counter runs.
- **§7's SD-2 registration note** gains the answer.
- `documented_rule.py`: **READY**.

## the-widget-constructor-and-object-sizes.md: REOPENED → DOCUMENTED

Page: [the-widget-constructor-and-object-sizes.md](../../../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md).

- **The reopen trigger is closed.** It was "SECTION-04 additions, peer review pending". SWE2-AUDIT-SPEC's non-author
  review `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929` (`Tools/work/SWE2-AUDIT-SPEC/REVIEW-0929-FINAL-BATCH.md`)
  byte-verified the section-04 evidence package and ran its receiver audit (16/16), verdict ACCEPT.
- **§2.1a is anchored.** At `002465F0`'s return, RAX is `001EDDA0`'s answer when non-zero (`0024674A`, `00246751`),
  else `00314960`'s (`00246753`). Nothing writes RAX after that before `0024677A ret`. The SECTION-04 control W04-4
  covers the 1 and 0 cases.
- **The §2.2 `+0xB4` row is left as it was, with a pointer.** The worksheet read it as contradicting UQ-188 and citing
  a missing §3a. Both readings are wrong. §3a is [the widget contract's](../../../16-UI/Widget-Object-Model/CONTRACT-widget-object.md),
  and there "60 Hz in mode 0" is HALFRATE (`01F82E38` set, `01DFE0C0` clear), the same reading as UQ-188. The row and the
  §9 "Not claimed" line now link the contract. (A first draft of this batch "corrected" the row; it was withdrawn before
  publication, after the contract was read.)
- **A call-chain section is added (§4a).** It covers the three construction doors into `002465F0`, the battle-menu
  instance chain, and the per-frame drain. It is assembled from facts the page and its §7 answers already cite.
- `documented_rule.py`: **READY**.

## Limits (OPUS)

- **No new measurement,** apart from the `002465F0` tail read (seven instructions, cited on the page).
- **Both re-statuses lean on answers routed for review.** SD-1 and SD-2 are with SWE2-AUDIT-SPEC per their records,
  and SECTION-04 has the acceptance named above.
