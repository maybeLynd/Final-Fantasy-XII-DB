# SEAD Category: the embedded sound-handle list, and the users of +0x50..+0x68 (OPUS, 2026-09-28)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SEM. STATIC evidence, certified EXE only; nothing
executed.

**What was wrong in the store.** `SQEX::Sd::Driver::Category` (0x88 bytes) carried:
- `+0x08` "secondaryVtable", `+0x10` / `+0x18` a node list's head / tail (citing the config page) and `+0x20..+0x37`
  unobserved;
- `+0x50` one `uint16`, `+0x60` a qword, `+0x68` a `uint32`, `+0x70` a qword - each "a value the constructor zeroes".

The constructor's merged zeroing stores (`007A96F0`: qwords at `+0x10..+0x40`, `+0x60`, `+0x78`; a word at `+0x50`) are
store merges, not field widths. The users below define the widths.

**What the image shows** ([`category_list.py`](category_list.py), checks R K D I S C U W):
- **R / K:** RTTI names `+0x00`'s vtable `Category` and `+0x08`'s `FixedList<0, SeadHandle>`. The constructor installs
  both, so `+0x08` is a second base subobject: an embedded 0x30-byte list.
- **D:** the list's own scalar deleting destructor (`007A98E0`) frees 0x30 bytes and array-deletes its node array.
  Category's destructor `007A9760` does the same inline.
- **I / S:** `007AA010` Init (capacity `+0x08`, node array `+0x10`, capacity x 0x28 with a count cookie), `007B6AA0`
  reset (free head `+0x18`), `007AF380` insert (active head `+0x20`, tail `+0x28`, count `+0x0C`, node flag bit 0,
  payload node `+0x20`).
- **C:** the initialiser `007AA110` stores its `edx` at `+0x60`. Its caller `007AAA40` passes the table slot index.
  It stores a pointer into the ctgr element at `+0x70`, and runs Init on `Category + 0x08` with the element's u16 `+4`.
- **U (added before publication):**
  - `007AA680` increments the dword `+0x64`. On 0 -> 1 it first calls handle slot `+0x18` (its float argument,
    r8d = -1) on every listed handle whose category byte (slot `+0xC0`) equals `+0x60`. It then stores the float at
    `+0x68`.
  - `007AA3E0` decrements it, clamped at 0. When the count was 1 it calls slot `+0x20` on the same handles.
  - `007A9A10` (a newly attached handle) replays slot `+0x18` with `+0x68` while `+0x64 > 0`.
  - `007AA770`, the per-update step, subtracts its argument from `+0x68` and clamps at 0.0.
  - `+0x50` / `+0x51` are separate bytes. `007AA540` / `007AA530` set them with the volume / pitch masters.
    `007AA770` reads and clears them, then pushes through slot `+0x28` / `+0x30`.
  - Every walk starts at Category `+0x28` (the list's active head) and follows node `+0x10` while node `+0x1C` bit 0
    is set. That is an independent read of the list layout from I / S.
- **W:** the regression. It FAILED before `--patch` and passes after.

**The first draft was wrong in one row.** It would have written `+0x64` as an unobserved span ("no other access found
here"). A scan of every `+0x64` / `+0x68` access in the SEAD code range found the four users above. U is the check that
rejects that draft.

**Result in the store.**

| before | after |
|---|---|
| `+0x08` secondaryVtable, `+0x10` nodeListHead, `+0x18` nodeListTail, `+0x20` unobservedSpan0020 | `+0x08` `soundHandleList` `SeadFixedListSeadHandle30` (48 bytes) |
| `+0x50` word0050 `uint16` | `+0x50` / `+0x51` `uint8` (volume / pitch master changed) |
| `+0x60` qword0060 | `+0x60` `categoryIndex60` `uint32`, `+0x64` `holdCount64` `int32` |
| `+0x68` dword0068 `uint32` | `holdArgument68` `float` |
| `+0x70` qword0070 | `configElement70` `void*` |
| - | new types `SeadFixedListSeadHandle30` (0x30) and `SeadFixedListSeadHandleNode28` (0x28) |

**Not claimed:**
- the SeadHandle payload's encoding;
- what `+0x70` is read for;
- who inserts into a Category's list;
- what handle slots `+0x18` / `+0x20` do;
- `+0x68`'s units.

The names `holdCount64` / `holdArgument68` are labels only.

**Consumer check.**
- corrects: `_types/fields.tsv` (Category `+0x08..+0x37`, `+0x50`, `+0x60..+0x6B`, `+0x70`) and `_types/types.tsv`
  (two new rows); both are touched by this publish.
- `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md` ("allocates that many 0x28-byte nodes at Category
  `+0x10`/`+0x18`"): agrees. The capacity is at `+0x10` and the node array at `+0x18`. It never called them head/tail.
- `18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md` ("the category number at `+0x60`"):
  agrees.
- `18-Audio/sqex-sd-sound-driver-architecture.md` §7 (list sizes 4 / 48 / 8, the `+0x58` reference): agrees.
- No page, verdict or candidate cites the replaced row names (grep of every `.md` / `.tsv` for them).

The regression that measures the change is `category_list.py` check W.

**Run receipt.** `category_list.py` executed at c57c75ac8: FAILS 1 (W) before `--patch`, then FAILS 0 after
([`category_list.out`](category_list.out)). At the same commit:
- `types_index.py --validate`: 0 errors;
- `check_census_widths.py`: 0 disagreements;
- `type-flow-census/typing_check.py`: FAILS 0.
