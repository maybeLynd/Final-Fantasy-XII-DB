# The last two UNRESOLVED allocation sites in `_types`: both tables are views into the loaded EBP payload (OPUS, 2026-09-30)

Before this record, `_types/types.tsv` carried exactly two rows whose `allocation_site` read UNRESOLVED:
`OffsetIndexedStringTable` (reached through `ActorManagerSlot` `+0x0A0` and `+0x0A8`) and `CountedU32LookupTable`
(`+0x100`). Both rows had been declared on 2026-09-21 from their readers alone. S-13's verdict named them "bare pointer
slots whose target type is unknown".

This record is static, from the certified image. The checker is `types_sections.py` (output `types_sections.out`,
`FAILS 0`).

## The answer (OPUS)

- **P1.** `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`003304A0`) is the EBP primary-payload
  dispatcher described on the spawn-placement page §31. For each present section it passes
  `(payload + dword[payload + off]) | tag` to a binder:
  - section `+0x18` → `00330190`;
  - section `+0x1C` → `00330220`;
  - section `+0x40` → `0032FB70`.

  The pointer is carried as 32 bits (`mov ecx, eax`), so the payload is assumed to sit below 4 GB.
- **P2.** Each binder masks the tag off, keeps the base in its per-tag table (`022C6CA0` / `022C6CC8` / `022C6DA8`), and
  calls its slot setter with the base.
- **P3.** The setters `0026C880` / `0026C8A0` / `0026CE40` write `ActorManagerSlot` `+0x0A0` / `+0x0A8` / `+0x100`,
  at `02098E10 + tag × 0x288`, the 5-slot array.
- **P4.** ~~`+0x0A0` and `+0x0A8` have no other writer. `+0x100` has one more, the teardown `0032ED80`, which stores 0.~~ The only non-zero writers are the setters (one caller each); all three fields are also zeroed by
  `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` (`0026CC31` / `0026CC49` / `0026CC50`, on every definition
  bind), by the boot clear `00266D10` (`memset` of each 0x288-byte slot, `00266EFC`) and, for `+0x100`, by the teardown
  `0032ED80`. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-types-sections-0930/REVIEW.md); the store census that is not limited to the setters' callers is the review's `slot_writers.py`. `types_sections.py` P4 is unchanged and still counts the setters' callers only.)*

**So neither type is an allocation.** Each table is authored bytes inside the actor's EBP primary payload, and the slot
records its address when the payload binds. Their lifetime is the payload's. The two `_types` rows now say this in
`allocation_site`, `ctor` and `dtor`, and no row in the store reads UNRESOLVED any more.

## Also in this publish: one row incorporated (OPUS)

`ManagerSub0209BE80_AB30` (`0x61F0`, HUD `+0xAB30`) moves from DISCOVERED / PROBABLE to **SEMANTICALLY IDENTIFIED /
PROVEN**. The row's own evidence already measured the extent end to end: the constructor's `memset(base, 0, 0x61F0)`,
read through `00276650` → `00245000` → `002465F0`. FABLE identified the object on 2026-09-12 as the **battle menu
widget**: UI requests 1 and 4 reach `00290CF0`, which builds it through `00276650` with handler `00279E20`. That reading
is published on [the widget-constructor page](../../../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md)
§7, so this is incorporation, not a new semantic claim.

## Limits (OPUS)

- **Whether `+0x0A0` / `+0x0A8` are cleared when the payload is released is not read.** `+0x100` is cleared by the
  teardown.
- **Which EBP file sections these are by name** is the EBP container pages' question; here they are identified only by
  their offsets in the section table.
- **Static only.**
