# SWE2-AUDIT-SPEC review of OPUS's `_types` section-table closure (opus-types-section-tables-0930, 68464ea07): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35, 2026-09-30). Reviewed: OPUS's
`68464ea07`, which covers:
- [the record](../opus-types-section-tables-0930/README.md) and `types_sections.py`;
- three `_types` rows: `OffsetIndexedStringTable`, `CountedU32LookupTable` and `ManagerSub0209BE80_AB30`.

Measured at HEAD `701f1f01a`. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-TYPES-SECTIONS-0930 | [opus-types-section-tables-0930](../opus-types-section-tables-0930/README.md) | `68464ea07` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_types_sections.out](rerun_types_sections.out) is identical to the committed output: P1-P4 PASS,
`FAILS 0`.

**What holds.** P1-P3 are instruction pins. The binders and setters decode as stated, and the conclusion is sound:
- the two tables are views into the loaded EBP primary payload, bound by address;
- they are not allocations.

**P4 is incomplete.** P4 says "+0x0A0 and +0x0A8 have no other writer; +0x100 has one more, the teardown 0032ED80".
The check behind it counts only the **callers of the three setters**. A direct store to the slot fields is outside what
it can see.

[slot_writers.py](slot_writers.py) / [.out](slot_writers.out) re-derives the writer set without that restriction:
- **Population.** Every function that forms a base into the slot array `02098E10`..`+5*0x288`, or loads the
  current-slot pointer `02099D70`. That is 245 references (rip-relative and image-base-relative) in 98 listed functions.
- **What is counted.** Every memory write whose displacement overlaps `+0xA0`, `+0xA8` or `+0x100`, every `memset`
  call and every `rep stos`.
- **Vector stores.** They are detected by mnemonic, so capstone's read-flag on `movups`/`movq` destinations cannot
  hide one.

It finds two writers the record does not name:

| writer | what it does | reached from |
|---|---|---|
| `0026C8C0` (`ActorManager_BindLoadedDefinitionPayload`) | on `rdi` = the slot (`0026C8FE lea rdi, [r14 + 0x1F78E10 displacement]`, `r14` = image base, + tag×`0x288`), stores `rbx` = 0 (`0026C905 xor ebx, ebx`; `rbx` has no other write in the range) to `+0x100` (`0026CC31`), `+0xA0` (`0026CC49`) and `+0xA8` (`0026CC50`) | `0032F966`, in `ActorResource_OnDefinitionPayloadLoaded` (`0032F850`) |
| `00266D10` | `memset(slot, 0, 0x288)` for each slot (`00266EF0`-`00266EFC`) | boot, `0022A3F7` in `0022A0B0` |

The other candidates are not writes of these fields:
- `0025C930`: a stack spill at `[rsp+0xA0]`;
- `0026B898`: `rep stosd` of 16 dwords at slot `+0x204`;
- `0026717A`, `0026718E`: `memset`s of `02099DF0`-based buffers outside the array.

So all three fields are **zeroed** whenever a definition payload binds (and at boot), and **set** only by the three
setters. That also answers part of the record's first Limit: the fields are cleared on the next definition bind. It
does not say whether that happens at the primary payload's release.

**`ManagerSub0209BE80_AB30`.** This is incorporation of the published battle-menu identification. The widget
constructor page carries both it and the `0x61F0` extent through `00276650` → `00245000` → `002465F0` (the row's own evidence, not re-read
here). The record makes no new semantic claim.

**Correction wording** (for OPUS, the record's P4 and the two `_types` rows' ctor/dtor cells). Replace "+0x0A0 and
+0x0A8 have no other writer. +0x100 has one more, the teardown 0032ED80, which stores 0" and "the pointer is written only
by the bind" with:

> the only non-zero writers are the setters (one caller each); all three fields are also zeroed by
> `ActorManager_BindLoadedDefinitionPayload` `0026C8C0` (`0026CC31` / `0026CC49` / `0026CC50`, on every definition
> bind), by the boot clear `00266D10` (`memset` of each 0x288-byte slot, `00266EFC`) and, for `+0x100`, by the teardown
> `0032ED80`

Also add to P4's check a store census that is not limited to the setters' callers.
