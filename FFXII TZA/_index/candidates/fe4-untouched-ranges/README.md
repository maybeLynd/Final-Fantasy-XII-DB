# FE-4 — the battle-stats record's last unaccounted bytes, with every named route followed

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `fe4_ranges.py` (5 checks, FAILS 0; a few minutes, since R3/R4 disassemble the image).

## Where the row stood

FE-4 asked two things.
- **Which routes the field scan does not follow.** OPUS's §2.3b answered three: writers beyond the third hop (the scan
  saturates), record-as-index (demonstrated on the gambit block), and the array seed (the scan never entered 41 of
  the 46 functions that form the record's address). Two were left open: *pointers stored into other objects*, and
  repairing the seed.
- **Whether the six untouched ranges are real.** §2.3a/§2.3b reduced 67 bytes to 10, in five gaps, and called every one
  alignment padding.

## What this record adds

**The seed is repaired, and nothing touches the open gaps (R3).** 68 functions either read `02EBF190` and use the
`0x1C8` stride, or call the record getter `00320A40`. Every access in them whose displacement covers `+0x5C`..`+0x63`
belongs to a different object. Its base is one of:
- a `0035D330` layout record;
- the battle unit itself (`00310DEC`);
- the unit's spawn record (`[unit + 0x6A0]`, `003079F4`);
- or a qword field at `+0x58`/`+0x60`, which the stats record cannot hold there: its `+0x58` is the u16 equipment
  slot 4, read only as a word.

**Pointers stored into other objects (R4, R5).** The stats pointer lives in the battle unit at `+0x698`. Two sources
are followed forward, and into callees that receive the pointer in `rcx`/`rdx`/`r8`/`r9`, to depth 3:
- all 604 sources — every `[X + 0x698]` load plus every getter result;
- the controls: `+0x24` (max HP) is found 3 times and `+0x64` (status word 1) 165 times;
- nothing reaches `+0x5C`..`+0x63`;
- the getter's result is never stored to non-stack memory at any of its 23 call sites.

**The page's `+0x05C` row is stale (R2).** Its three accesses (`00386E43`, `00386E56`, `00386EEC`) are
`[r14 + r12 − 0x60]`, with `r14 = stats + 0xBC + 4i` and `r12 = result − stats`, so they address the *result* record
at `+0x5C + 4i`. FE-3 said so on 2026-09-13. The table row, and the type store's `BattleStatsRecord 0x05C
slotCounter5C`, were never updated. With it gone, stats `+0x5C`..`+0x5F` is untouched as well.

## The answer

| bytes | what they are | evidence |
|---|---|---|
| `+0x22`–`+0x23` | alignment padding | a word at `+0x20`, then an `s32` at `+0x24` (R1) |
| `+0x4F` | alignment padding | a byte at `+0x4E`, then the qword-initialised `u16[5]` at `+0x50` (R1) |
| `+0xBB` | alignment padding | the gambit count byte at `+0xBA`, then the `u32[32]` at `+0xBC` (R1) |
| `+0x1C6`–`+0x1C7` | tail padding | the selector byte at `+0x1C5`, then the `0x1C8` stride (R1) |
| `+0x5C`–`+0x63` | **an 8-byte region no code reads or writes**, on every route above | R2–R5 |

**This refines §2.3b.** Its "every one of them sitting exactly where a compiler pads" holds for four gaps, not for
`+0x60`–`+0x63`. That slot is a 4-aligned 4-byte slot between two `u32`s, and once the stale `+0x5C` row is removed
it is part of an 8-byte hole after the u16 at `+0x5A`. Alignment cannot produce either shape. The region is real:
the PC build allocates it and never uses it. §2.3b is OPUS's section, so the refinement is routed to OPUS rather
than edited here.

**Not claimed.** What the region held in the PS2 original, or whether a whole-record copy (save/load or `memcpy`)
carries bytes through it. A bulk copy moves them but does not give them a meaning.
