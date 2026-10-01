# FJ-4 — which code reads which field of the menu's unit-display records

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.** Control: `fj4_check.py` (2 checks,
FAILS 0), which runs `fj4_record_readers.py`.

**The question.** FJ-4 asked two things. What the two unread callers `0031FEC0` / `0031FF70` add was answered on
2026-09-12: they are actor-to-slot wrappers. The rest was left as "which drawer reads which offset of the `0209AC30`
table".
- **The table.** `00283270` builds nine unit-display records (the `00329220` layout,
  [page](../../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md)) at `[0209AC30] + 0x408 +
  i × 0xC0`. It keeps a sorted pointer list to them at `+0xAC8`.
- **The census.** `fj4_record_readers.py` starts from all 456 functions that load `[0209AC30]`. It follows record
  pointers, formed from the pointer list or a slot address, through copies, stack spills, and callees that receive
  one as an argument (depth 3). It also follows them out of the two accessors that return one, `00282DF0` and
  `00282E10`, into their callers.

| field (record offset) | read by | where that code sits |
|---|---|---|
| `+0x20` HP, `+0x24` effective max, `+0x2C` MP, `+0x30` capacity | `00283E40` only | the party-member panel on the menu screens (its status icons are GA-1's `+0x10` list) |
| `+0x44` status presence | `00283E40`, `002C5660`, `002C56F0` | the party panel, and the action list's status cursor list |
| `+0x86` charges | `00283E40`, `00583D60` | the party panel; the save/load screen |
| `+0x87` bars | `00283E40`, `0055BFF0`, `0055CD40`, `00583D60` | the party panel; the license board view (`0055CD40` is its view proc); the save/load screen |
| `+0x90` experience, `+0x94` to next level | `002C1000` | the license board's grid build |
| `+0x9A`–`+0xAA` the five equipment words | `002CA7C0`, `0057B1A0` | the item record flag setter, and the shop's per-row emitter (who can equip) |
| `+0xB0` LP | `00283E40`, `002C1000`, `00560210`, `005618E0` | the party panel; the license grid build; the menu launcher's licence family; the licence detail pane |
| `+0xBA` level | `00283E40`, `00583D60` | the party panel; the save/load screen |
| `+0xBB` licence count | `0055BFF0`, `0055CD40` | the license board view |
| `+0x60` type, `+0x00` flags | 57 and 15 functions | the slot selector and validity test every consumer applies |

The screen names come from the pages that cite each function:
- the layout-parameter and query-record pages for `00283E40`;
- the license-board pages for `002C1000`, `0055BFF0`, `0055CD40` and `005618E0`;
- the menu-screen atlas for `00560210`;
- the save/load crossing on the per-frame gate contract for `00583D60`;
- the shop and bazaar pages for `0057B1A0` and `002CA7C0`.

**Limits.**
- A record handed on more than three calls deep is not followed.
- The census covers reads, not writes.
- Record fields no code reads (for example `+0x28` cap, `+0x34`, `+0x38`) are not claimed unused beyond this census.
