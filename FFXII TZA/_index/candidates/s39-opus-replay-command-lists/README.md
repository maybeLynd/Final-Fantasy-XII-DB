# S-39: the render command lists and the handshake wait executed as shipped code (OPUS, 2026-09-25, block 312)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.** S-39's runtime cell is NOT MET with the gap "runtime
evidence". `CONTRACT-render-command-list-and-graphics-handshake.md` has no execution; this narrow OPUS harness runs its
entry points.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set: 50 functions**, made of the entries' static closures plus the indirect targets the bodies reach:
  - the EASTL allocator vtable `00902720`'s five slots;
  - the planted command class's three slots;
  - the render-params getter `00193D50` / `0018D630`;
  - the device getter `00189120`;
  - the delete path `00809950` → `00210EB0`.
- **Imports.** The import directory is parsed from the image, **every IAT slot points at a unique trap**, and only
  five imports are bridged by name: `malloc` and `_aligned_malloc` (a bump heap; one case makes `malloc` return 0),
  `free` and `_aligned_free` (recorded), and `memmove`. Any other import would fail the case by name.
- **Command objects.**
  - The real enqueue `0018C610` builds its own class (vtable `009031D0`).
  - The walks, the flush and the destroy run over planted objects of the shipped `MapOrderedObject` class (vtable
    `009010D8`). Its slot 1 `00212C60` is a null-gated delegate that returns when `+0x08` is null; its slot 2
    `0016EE70` returns 4; its slot 0 `001E11D0` is the scalar-deleting destructor. **Every indirect call therefore runs
    shipped code**, and the harness counts the slot-1 / slot-2 / slot-0 calls per object.
- **Fixtures** are planted data only: the planted objects, `[01F7F5F0]` (render params `+0x49C`), `[01F7F598]` (device
  holder), `[01DF08FC]` / `[01F7F594]`, and `[02EBA3F8]`.

**7 / 7 pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `A_construction` | §3, I-3 | `0018B480` → `malloc(0x30)` + ctor: mask `0xFFFFFFFF`, split 0, armed 0, reverse mark −1, **reserve = 5,000 entries** (one `_aligned_malloc(0x9C40, 16)` through the EASTL allocator); allocator vtable `00902720`. `0018C9E0` → `malloc(0x20)`, same allocator, **no reserve** |
| `B_enqueue_both_lists` | I-1, I-9 | three enqueues append **the same pointer, in the same order, to both lists**; each object is `malloc(0x20)`, vtable `009031D0`, `+0x08 = 0`, `+0x10 = 1`, `+0x18 = arg`. **A failed `malloc` appends a null to both lists** |
| `C_walks_I4_I5_I7` | I-4, I-5, I-7, §2 | forward: part 1 = `[0, split)`, part 0 = `[split, count)`, in stored order; the null is skipped; the key is called once per entry. **List mask with bit 2 cleared: the key is called and nothing executes** (a mask, not a sort). **I-7:** with `[01DF08FC] = 0` and `[01F7F594] = 1` the walk exits at the first masked-in entry, before executing it. `0018B1B0`: **the key is called twice per non-null entry** (10 for 5). `r9b = 0` executes in ascending order and `r9b = 1` in descending order |
| `D_marks_and_clear_I8_I1` | I-8, I-1 | `0018B510` armed → `+0x28 = 1`, `+0x24 = 0`; unarmed → `+0x24` = count. `0018B030` → `+0x2C` = count. `0018B070` toggles bit 1. **The clear resets `pEnd`, `+0x24 = 0` and `+0x2C = −1`, frees nothing, calls no slot 0, and leaves every object unchanged** |
| `E_owner_destroys_I1` | I-1 | `0018B810` calls slot 0 with the free bit on **each non-null entry**, and each is freed; the vector is emptied |
| `F_flush_I6` | I-6 | `0018C8F0` executes **only the entry whose `+0x10` is 0** (one of three), **then destroys all three** and empties the vector |
| `G_handshake_I10` | I-10 | `0036F2C0` returns at once and leaves `[02EBA3F8] = 0xFFFF & 0xFFFFFEF3` (bits 2, 3 and 8 clear) |

## What the execution adds to the contract

1. **I-3 is true of the ordered list only.** The owner vector has no reserve and grows geometrically through
   `_aligned_malloc` (a separate probe: capacity 1 → 2 → 4 → 8 on the 1st, 2nd, 3rd and 5th enqueue). "The list never
   grows in practice" should name the ordered list.
2. **The flush is also a destroy.** After executing the `+0x10 == 0` entries, `0018C8F0` runs slot 0 with the free bit
   on **every** entry and empties the vector (`0018C958`–`0018C9A5`). I-6 describes only the selection; I-1's "the
   owning vector destroys" has a second site here.
3. **I-7's exit happens before the entry's execute.** The masked-in entry that meets the gate is not executed.

## Not covered

- the ~40 other enqueue functions and the command classes' real execute bodies (`009031D0`'s `001F3300`, draw jobs);
- the teardown order I-2 (it is in the callers `0017CD53` / `00188204`);
- the render pass that arms I-7;
- a live game.

## I-2 executed at the scene-teardown site (OPUS, 2026-09-26)

`i2.py` runs over this harness (imported unchanged; its cases run first).
- **Setup.** Both lists come from the shipped constructors, and three commands are enqueued by the real enqueue, so
  both lists hold the same three pointers (I-1).
- **The run.** The scene teardown `001E0590` then runs as shipped. In addition to this block's allowed set, it allows
  the closure of `001E0590` and the command class's destroy target `001F2460`, which is reached indirectly inside the
  flush.
- **Stop boundary** (recorded, not stubbed): `001A14D0`, which `001E0590` calls last to release a global object this
  world does not build.

| case | asserted |
|---|---|
| I-1 precondition | both lists hold the three enqueued pointers |
| order | the clear `0018B040` (`001E05A9`) is entered before the flush `0018C8F0` (`001E05B6`) |
| at the flush | the ordered list is **empty** and the owner still holds the three commands (events: clear at 3/3, flush at 0/3) |
| frees | all three commands are freed inside the flush, after the ordered list emptied: it never holds a freed pointer |
| boundary | the run reaches `001DB620` and ends at `001A14D0` |

The other two sites (`0017CD53`/`0017CD60` in the frame tick, `00188204`/`00188211` at the end of the render pass) are
the same pair in the same order statically, and are not executed here.

**Runs.** 5/5, and two runs give an identical `i2_result.json` (md5 `7421772e446df567eadeca51997f116b`).
