# C-13: MapScreenPage +0x108..+0x117 is one embedded 0x14-byte object, not storage used two ways (OPUS, 2026-09-25)

**Status: PUBLISHED 2026-09-26; independent review requested (author OPUS).** The type rows are applied: `RectTween`
(0x14) in `_types/types.tsv` / `fields.tsv`, embedded at `MapScreenPage +0x108` as one `rectTween` row that replaces
the census rows `word0108`..`word0116` and `dword0118`. The register cell is staged with OPUS's other staged answers
until `OPEN-QUESTIONS.md` is clean.
**Evidence class: STATIC.** Every instruction below was re-read in the shipping image.

**The row's premise.** `004022D0` writes five dwords at `+0x108`. Later in the same body, `002B840F` stores an
"8-byte pointer" at `+0x110`. The row read that as two incompatible uses of one block ("storage used two ways") and
asked for the discriminator.

**What the code shows: there is no second use.**
- **`+0x108` is the base of an embedded object.** Both page procedures pass `lea rcx, [r14+0x108]` to its methods:
  - `002B7C7C` and `002BB081` pass it to `004022D0`, the initialiser;
  - `002B80B7` and `002BB510` pass it to `004026D0`;
  - `002BBCA3` passes it to `00402610`;
  - `002B83A8` and `002BBCE9` pass it to `00403330`.
  - A displacement census of the page cannot see these methods' reads. That is why the stretch looked write-only.
- **The object's layout, from its methods:**
  - `+0x00` u16[4]: a rectangle. `004026D0` writes it as four words (`00402714`-`0040271F`); `00402610` writes it as one
    qword, the first half of `00275320`'s 16-byte result (`00402644`).
  - `+0x08` u16[4]: a second rectangle. `004026D0` writes its words at `004026EE`-`004026FC`; `00402610` copies
    `[src+0x30..+0x36]` into it word by word (`0040265A`-`00402668`).
  - `+0x10` dword: `0x100` at init, 0 after `00402610`; `00403330` reads it at `00403341` and adds a step to it at
    `00403357`.
  - The initialiser `004022D0` writes `{0, 0, 8, 8}` at `+0x00`, `{0, 0, 8, 8}` at `+0x08` and `0x100` at `+0x10`.
    The row's "five dwords" are exactly that, stored as dwords plus one merged qword.
- **The "pointer" store is the same rectangle copy.**
  - `002B83FB`-`002B840F` loads `rax = [[page+0xBBC8]+0x30]` and stores it at `[page+0x110]`, which is the object's
    `+0x08` rectangle, moved as one qword.
  - `00402610`'s source is the same object: `002BBC9C` passes `rdx = [page+0xBBC8]` with `rcx = &page+0x108`. So the
    word copy and the qword store move the **same eight bytes** (`[page+0xBBC8]+0x30..+0x37`) into the **same place**.
  - The location page does the same: `002BBD3C`-`002BBD50` loads `[[page+0xBBC8]+0x30]` and stores it at
    `[page+0x110]`, after the same `call 002B66E0`.
  - Nothing overwrites a live value of another shape.

**Answer.** `MapScreenPage +0x108..+0x11B` is one embedded 0x14-byte object: two `u16[4]` rectangles and a dword.
The qword at `+0x110` is its second rectangle, copied from `[page+0xBBC8]+0x30`, and not a pointer. There is no
overlay and no discriminator to find. The store's existing `word0108` / `word010C` / `word0110` / `word0114` /
`dword0118` rows are consistent at word granularity: the mixed widths are multi-word moves.


## The object is a rectangle tween (added the same day)

`00275320(out, from, to, t)` interpolates each edge as `from + ((to - from) * t >> 8)` (`00275335`-`00275395`).
`00402610` calls it with `from = +0x00`, `to = +0x08` and `t = [+0x10]`, stores the result at `+0x00`, loads a new
target into `+0x08` and zeroes `+0x10`. So the fields are:
- `+0x00`: the current rectangle;
- `+0x08`: the target rectangle;
- `+0x10`: the blend in 1/256 steps (`0x100` = arrived), which `00403330` steps.

The methods, re-read in full on 2026-09-26:
- `004022D0` **init**: current `{0,0,8,8}`, target `{0,0,8,8}`, blend `0x100`.
- `004026D0` **snap**: copies the source rectangle `[src+0x30..+0x37]` into both target and current. The blend is
  unchanged.
- `00402610` **retarget**: current = `00275320(current, target, blend)`, target = the source rectangle, blend = 0.
- `00403330` **step**: blend += max((0x100 - blend) / 6, 6), clamped to `0x100` (`00403330`-`00403369`); it returns 1
  once the blend has arrived. That is an ease-out.
- The two page stores (`002B840F`, `002BBD50`) replace the target with one qword **without** resetting the blend.

The source object at `[page+0xBBC8]` is not a `Widget` (`Widget +0x30` is `childCount`). Its type is not claimed;
only its eight bytes at `+0x30` are read here as a rectangle.

**Applied** to `_types` on 2026-09-26. `types_index.py --validate`: 776 types, 0 errors, 0 gaps. `check_storage_class.py`: 0 hard failures.
