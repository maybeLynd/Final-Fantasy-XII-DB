# UQ-351: what makes the nine-patch guard's word non-zero (OPUS, 2026-09-25)

**Question.** `00392A00` tests `word [rcx+0x58]` and enters the box renderer `00392A10` when it is non-zero. What makes it
non-zero?

**Answer.** `rcx` is always `[widget+0x38]`, the node's **live draw record**, and `+0x58` is that record's **alpha
scale** (0x80 = 1.0). The widget-tree pass composes it from the node's opacity byte `+0xA0` and its ancestors'. The box
therefore draws for every widget that is not fully transparent.

| step | address | what the code does |
|---|---|---|
| callers | `002A62DF`, `002C0916`, `002C0D5A` (message 3's arm `002C0D53`), `00573F6D` | each loads `[widget+0x38]` into the guard's `rcx` |
| publish | `00245EB0` / `002463BE` | `00245E60` stores the address of its stack record at `+0x38`, and zeroes the field when the node's draw ends |
| build | `002D8C00` | zero-fills the 0xA0-byte record; sets `+0x5A` = 0x80 (RGB scale), `+0x5C` bit 17, the state words `+0x78` = 0x44 / `+0x80` = 0x1001 / `+0x88` = 0x60, the colours `+0x90`/`+0x94` = 0x80808080 and 1.0f at `+0x60`/`+0x68`/`+0x6C`. **`+0x58` stays 0** |
| root | `00245ED3` / `00245EF0` | `+0x58` = node byte `+0xA0`; `+0x5A` is not touched (stays 0x80) |
| child | `00246480` (`002464F5`), `00245F81`-`00245F9C` | `+0x58` = (parent record `+0x58` * node `+0xA0`) >> 7 |
| child | `00245F38`-`00245F49` | `+0x5A` = (parent record `+0x5A` * node `+0xA1`) >> 7 |
| default | `002465F0` at `0024670A` / `002466E6` | `+0xA0` = 0x80, `+0xA1` = 0x80 |

**Why `+0x58` is alpha.** The fourth tint byte (`+0x93`) is scaled by `+0x58`, and the other three by `+0x5A` (`002A4967`,
`002D857D`; the rectangle primitive `002DBDD0`). The packed tint goes to the GS RGBAQ register. See
`99-Unresolved-Residual/drawing-one-coloured-rectangle.md`.

## The replay (`check.py`)

Evidence class **NATIVE-REPLAY** (unicorn), `live_game: false`. It uses `world.py`'s Session, the same builder as
blocks 318-353, and **no application stub**.

- **A.** `002D8C00` runs over a buffer poisoned with 0xA5. `+0x58` reads 0, so it is an explicit write and not untouched
  storage, and `+0x5A` reads 0x80.
  - *This rejects "the builder sets alpha 0x80"* (the map-screens page row before this correction).
- **B.** The guard runs with `+0x58` = 0, and then with 0x80, 1 and -1.
  - At 0 it returns without entering `00392A10`.
  - Every other value enters `00392A10`. That is a **recorded stop boundary** (outside the allowed set), not a stub.
  - *This rejects "the island is dead".*
- **C.** `00245E60` runs over a two-node tree (root and child, no handlers). The tree links are the widget contract's:
  `+0x10` parent, `+0x18` first child, `+0x20` next sibling.
  - The root's record is read at the child loop (`0024635C`), and the child's right after its `+0x58` store
    (`00245FA0`).
  - The grid has seven cases, including 0 propagation, `0x7F*0x7F >> 7 = 0x7E` rounding, and a root `+0xA1` of 0x20 that
    leaves the root record's `+0x5A` at 0x80.
  - Root and child each hold a **distinct stack address** at `+0x38`.
  - *This rejects "Widget +0x38 has no writer"* (the type row's bounded negative).
  - **STOP BOUNDARY:** after the child's record is composed, its draw reaches the screen-configuration getter `001DDAB0`
    through `001844D0`. `001DD8C4` then reads the first dword of `[01F82D18]`, which this world does not build.
  - Nothing is fabricated to run past that point. So the end-of-draw clear at `002463BE` is **static** evidence here.

**Runs.** Two runs give an identical `result.json` (md5 `be2538a838fa61ec44a6a375a268f548`). The output is in
`run_output.txt`.

**Not read:** which widgets animate `+0xA0` to 0 at run time, and what the other message-3 handlers do to the record.

## The record's census (`census.py`) (OPUS, 2026-09-25)

`census.json` records every read and write of the two draw records (root and child) that `00245E60` builds, up to the
boundary. The hooks are registered **before** the only run: a hook added after a first run misses reads, which was
measured here as 1 read event. It backs the `WidgetDrawRecord` (0xA0) rows in `_types`.
