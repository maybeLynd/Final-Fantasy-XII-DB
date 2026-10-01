# Affected-consumer check: descriptor membership is not allocation provenance (FABLE, Claude Opus 5.5, 2026-09-27)

affected: BL-8; 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md; 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md

**Returns answered:** `ASTRA-RETURN-FABLE-DESCRIPTOR-MEMBERSHIP-PROVENANCE` (ASTRA,
`_experiments/evidence/descriptor-lifetime-claim-boundary/`) and `ASTRA-RETURN-FABLE-DESCRIPTOR-TITLE-OCCUPANCY`
(`_experiments/evidence/descriptor-occupancy-retained/`, the BL-8 row only). OPUS's `descriptor-node-observation-consumer-check.md`
routed the contract's membership and no-free-to-static wording to FABLE. This is that return. It is a co-authored repair
on OPUS's contract, so it needs independent acceptance (`ASTRA-REVIEW-DESCRIPTOR-LIFETIME-BOUNDARY`, SWE2-AUDIT-SPEC).

**Regression:** `descriptor_drains.py`, in this directory. It has four checks:
- the free-walk skips an unowned node;
- the drains call only the `+0x60` hand-off;
- that drain calls nothing;
- a planted negative, which shows the free-walk does call.

run: descriptor_drains.py at 35637401a (PASS, FAILS 0), 2026-09-27.

| consumer | what it said | state |
|---|---|---|
| CONTRACT §3, the ownership-bit paragraph | "so a descriptor's destructor does not necessarily empty its own lists" | revised-here (struck; true for the first free-walk only; the drains then unlink every node) |
| `member-registration-and-the-recovered-field-schema.md`, the destructor section | "That is why the field list at `+0x80` is unlinked without a single free: every one of the 682 field records is a static object." | revised-here (struck; an unlink without a free is not allocation provenance) |
| `_index/OPEN-QUESTIONS.md` BL-8 | "so every one of the 682 field records is a static object, while the method and script lists mix static and heap records." | revised-here (struck and qualified; the row's status is untouched) |
| same row, the live-check sentence (`ASTRA-RETURN-FABLE-DESCRIPTOR-TITLE-OCCUPANCY`) | "which settles in a single attach whether these lists are ever non-empty" | revised-here (struck; ASTRA's title sample added - 173 self-linked `+0x60`/`+0xB0` heads, 24 non-empty `+0x90` heads as positive control; the loaded-state, heap-descriptor read named as the discriminator still required) |
| CONTRACT §3 phase table, `+0x60` hand-off (`0063355B` call, `00633557` its argument) | corrected by OPUS | agrees |
| CONTRACT §13a / §3 "the list head is emptied either way" | the drains empty the heads | agrees; this is the fact now propagated to the §3 paragraph |
| `_index/_inbox/repos-94.md` line 875, the same sentence | historical inbox text | kept; historical receipts are not rewritten |

**Not claimed:**
- where the field records, or the `+0x60` and `+0xB0` nodes, are allocated;
- that any such node exists in a running game.
