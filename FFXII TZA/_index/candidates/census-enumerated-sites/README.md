# Census positives from loop enumeration are marked; one more phantom-backed row corrected (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC, which owns tool-policy reviews.

**The mechanism.**
- `census_receiver_fixpoint.py` joins register states generously: candidate bases union across predecessors, up to
  `BASECAP` = 16. So a loop `add rbx, stride` around a call reaches the callee at every base the extent allows, and that
  includes elements the loop's trip count never produces.
- The tool does this **by design**. Its failure direction must stay over-report, because its negatives are published,
  and that is unchanged here.
- The defect is downstream. Store rows took such a **positive** as proof that an access exists.
- Found in `lgs-nested-chunk-record/`: a two-iteration clear loop was reported at three phantom elements, and two
  TYPE RESOLVED rows rested on those hits alone.

**The change (additive).**
- `EMIT_JSON` now carries `enumerated_sites`, as `disp:width:site`. These are the sites with no recording traceable to a
  seed through single-candidate steps.
- Each access and each call enqueue notes its context:
  - the (function, base) pair being scanned;
  - whether the base register held more than one candidate.
- A pair is **plain** when a seed reaches it through single-candidate enqueues. A site is **enumerated** when none of its
  recordings is a single-candidate one inside a plain pair.
- The per-site map, the printed totals and the self-test are unchanged. Check E compares a live run with the receipt.
- An enumerated site does not mean the access is false. The first loop pass is plain; a later pass may be real. The census
  simply has not established the trip count.

**Audit** ([`enum_check.py`](enum_check.py)). Every type whose TYPE RESOLVED rows cite a `census_receiver_fixpoint` seed
was checked: 10 types, 11 seeds, receipts in [`receipts/`](receipts/).

| row | census hits | outcome |
|---|---|---|
| `LegacyPs2GsTextureContext +0x23C` `field023C` | `002F7236` only, enumerated | **corrected**: it cites that site alone. The loop from `+0x1E8`, stride 0x18, runs twice (count 2 in `[rsp+0x28]`, written only by the loop), so a read at `+0x23C` would be a fourth pass (check L). Now DISCOVERED, old text struck, old type as WAS |
| `LegacyPs2GsTextureContext +0x228` `admittedSlotCount` | `002F724A`, enumerated | stands: the row rests on `LegacyPs2GsDerivedSlotRecord`'s route, not on the census |
| `CPostEffect +0x400` `field400` | `006FF790`, enumerated | stands: the row rests on the flow census read `007029D9` |

`field0118` / `field0148` were corrected earlier today in `lgs-nested-chunk-record/`, which is why they no longer appear.

**Checks.**
- **E:** control, run live.
- **L:** the second loop's count.
- **A:** the audit.
- **S:** the regression. No row rests on enumerated sites alone. It FAILED before the patch (`+0x23C`) and passes after.

**Not done here.**
- The census's join is not narrowed. Bounding trip counts is a method change with coverage consequences for every
  published negative.
- Other instruments' receipts are not re-read.
- `WidgetConsumer02AEE4C8`'s ctor seed `002465F0` is the shared widget initialiser. The tool's own docstring warns that
  such a seed can credit one type with another's fields. That is noted, not adjudicated.

**Amended the same day.** Evidence migrated between types under rule 0 carries the source type's census citation.
`enum_check.py` now reads seeds only from a row's own evidence, the text before `MIGRATED from`. Without that, Widget's
rows migrated from MapScreenContainer (`mapscreen-child-widget/`) were audited under MapScreenContainer's seed.

**Run receipt.** Run verified at dbc974247:
- `enum_check.py --receipt` FAILS 1 (S) before `--patch`, then FAILS 0 after;
- `census_receiver_fixpoint.py --self-test` PASS (147);
- `test_access_policy_producers.py` FAILS 0;
- `types_index.py --validate` 0 errors;
- `lgs_nested68.py` and `ramp_recut.py` FAILS 0.
