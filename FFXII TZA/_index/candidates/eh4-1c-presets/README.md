# EH-4: the +0x1C indices the seventeenth pass called engine-unwritten are preset at construction

OPUS, 2026-09-27. Static, image sha 73461d08…

**Question.** The record page's seventeenth pass says the engine reads thirteen `+0x1C` indices and writes only six by a
literal, so `0, 4, 5, 6, 7, 14, 16, 17` "can only be arriving from `reqenable` / `reqdisable` arguments in the shipped
scripts". A SWE2-DATA census built on that premise concluded that bits 0 and 6 have "zero producers, script or
executable".

**Discriminator.** The second pass's own table: `00266BD0` stores a whole-word `+0x1C` preset per `+0x03` kind row. If
the initialiser reaches it unconditionally and nothing later clears those bits, the eight have an executable writer.

**Result.** It does, and they do.
- `00266BD0` has one caller, `002665B1`, which is in the entry path of `ActorStorage_InitializeRecord` `00266530`.
- Its presets are `0 -> 0`, `1-2 -> 0x38`, `3-4 -> 0x40`, `5-6 -> 0x30004` and `7 -> 0x34C85`.
- The initialiser's later `+0x1C` writes are masked and touch only indices 2, 8, 10 and 13.

Which rows preset each index:

| index | preset by rows |
| ---: | --- |
| 0 | 7 |
| 4, 5 | 1, 2 |
| 6 | 3, 4 |
| 7 | 7 |
| 14 | 7 |
| 16, 17 | 5, 6, 7 |

The seventeenth pass counted call sites of the index setters (`0026B4A0` / `0025D5E0`) and did not include the
whole-word store.

**Not claimed.** What any of the eight means, and how often a record is carved with rows 3, 4 or 7.

**Control.** `eh4_1c_presets.py` (run from the Database directory or anywhere; it resolves the exe from the repository):
- C1: one caller, on the entry path.
- C2: the eight decoded presets.
- C3: the later writes touch only 2, 8, 10 and 13.
- R1: each of the eight is preset by some row. This rejects the "never written by the engine" reading.
- R2: rows 1-2 preset 4 and 5 together. This rejects "the engine protects two indices it never sets".
- N1: index 1 is in no preset, a negative control on the decoder.

Expected `FAILS 0`.

## Second correction: the LOD verbs write the secondary context, not this record

The fifth pass's sweep matched short setters by displacement. Two of its sixteen verb-backed setters store through a
different receiver:
- `002EC680` (`setlod` / `partysetlod`) reloads `rcx = [rcx + 0xC0]` before `mov byte [rcx + 0x13], dl`.
- `002EC6A0` (`puppetsetlod`) is called only with a puppet-table entry + 0x10.

Their shared tail `002E8CE0` is also called with `[record + 0xC0]`. So "+0x13 IS THE WHOLE-BYTE LOD SETTING" of the
actor storage record is withdrawn, along with what it was said to settle (the initialiser's `&0x3C`, and `0025E2AA`'s
`cmp 0x80`). The type store already had the LOD byte on `SecondaryContextElement +0x013 lodLevel`. The other thirteen
setters store through their entry `rcx`.

**Control.** `eh4_lod_receiver.py`:
- L1–L3: the two receivers and the tail.
- L4: the thirteen others. The predicate flags `002EC680` itself when applied to it.
- L5: the type-store row.
- R1: rejects the fifth pass's reading.

Expected `FAILS 0`.
