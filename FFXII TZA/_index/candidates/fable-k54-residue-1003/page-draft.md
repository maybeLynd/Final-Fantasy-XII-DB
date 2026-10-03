# Page draft: effect-mesh-records-kind-54.md, the lighting residue (FABLE, 2026-10-03)

Target: `Database/FFXII TZA/17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md`. The diff is
taken against the working tree at HEAD `28534fcdb`; the page's last change is `949d310aa`. Evidence: `README.md` beside
this file, `k54_residue.out` (100 checks, FAILS 0) and `census_k54_modes.out` (FAILS 0). Every number below is copied
from those two outputs.

## Citation conventions

**Functions the page did not cite before** are referenced by call site:
- the kind-0x54 dispatcher as `00449AB0`+0x6AB, its only call (`0044A15B`);
- the float-track evaluator as `00449AB0`+0x543.

The type-0x04 / 0x06 / 0x07 walks are reached through the type tables, so they have no direct call site. They are named
by their sibling page and by their calls into the two grid paths the page already cites.

**Left out on purpose.** The matrix globals and the setup routines of types 0x04 and 0x06 are not cited here; they are in
`README.md`. Their 8-hex tokens would import a neighbour edge set into this page.

## 1. Status line (frontmatter `status:`)

OLD:

```text
; open: which pass modes shipped effects use, and the other four draw paths' selectors (status line current 2026-10-03, SWE2-DATA)
```

NEW:

```text
; the residue answered 2026-10-03 (FABLE, fable-k54-residue-1003, k54_residue.py 100 checks FAILS 0, census_k54_modes.py FAILS 0: all five draw paths share one pass switch and read the planar scalar of their own pass, k = p; the pass bytes are authored slot bytes, and shipped data authors modes 1-4 in 348 of 9,846 active pass slots, none above 4); open: what the matrices hold at draw time, the non-constant planar scalars, and what +0x1F1 bit 3 changes in the drawing (status line current 2026-10-03, FABLE)
```

## 2. The italic residue after "The lit per-normal table is answered"

OLD:

```text
*Not established (the record's Limits): which modes and matrices shipped effects use and what the matrices hold at
draw time (a population and runtime question); the selectors of the four other draw paths (`00437130`, `00438860`,
`004434D0`, `00444340`), which call the same five routines; and whether the planar index k equals the pass index.*
```

NEW:

```text
~~*Not established (the record's Limits): which modes and matrices shipped effects use and what the matrices hold at
draw time (a population and runtime question); the selectors of the four other draw paths (`00437130`, `00438860`,
`004434D0`, `00444340`), which call the same five routines; and whether the planar index k equals the pass index.*~~
*(Answered 2026-10-03, FABLE, except the matrices' contents. Record
`../../_index/candidates/fable-k54-residue-1003/README.md`: `k54_residue.py` 100 checks FAILS 0, static and executed;
`census_k54_modes.py` FAILS 0, authored data.)*

- **The per-pass selector is one switch in all five draw paths.**
  - Each path reads the mode byte `param + 0x1B0 + p` (`00437486`, `00438C70`, `00443865`, `00444711`) and the axis
    byte `param + 0x1B4 + p`.
  - Each reaches the same routine per mode and axis as above. Mode 0, and every mode from 5 to 255, builds no table.
  - The planar call sits on the mode-2 arm only.
- **Which path draws a kind-`0x54` mesh** is chosen per element, by the parameter block's byte `+0x1F1`.
  - The dispatcher has one caller, `00449AB0`+0x6AB. It runs `00438860` when `+0x1F1` is `0x80` or above, else
    `00437130` when bit 3 is set, else its inline path.
  - `00449AB0` builds `+0x1F1` from definition byte `+0x590` (executed over all 256 values):
    - bit 7 is `+0x590` bit 5;
    - bit 3 is bit 0 or bit 5;
    - bits 4-6, the two-mesh switches of §8, are bits 1-3.
  - Over every EFX stream, the 5,204 type-`0x05` elements split 1,800 / 522 / 2,882 (`00437130` / `00438860` /
    inline).
- **`004434D0` and `00444340` draw no kind-`0x54` record.**
  - Their only callers are the type-`0x04`, `0x06` and `0x07` walks of `the-element-types-00-0a.md`. The calls are at
    `00445AF8` / `00445AFF`, `004477D9` / `004477E0` and `004487A1` / `004487A8`; there is no other branch reference and
    no stored pointer.
  - Each walk draws the procedural ring, column or dome grid it builds itself.
  - Definition bit 0 of `+0x672` (type `0x04`) or of `+0x6D2` (`0x06` / `0x07`) picks `00444340`; clear, it picks
    `004434D0`. The same bit becomes `+0x1F1` bit 3.
  - Shipped elements, `004434D0` / `00444340`: type `0x04` 169 / 4, type `0x06` 3 / 22. Type `0x07` is not authored.
- **The planar index k equals the pass index p.**
  - In all five paths the planar call's pointer is `param + 0x1D8 + 4p`, with the same p that indexes `+0x1B0` (call
    sites `004375BE`, `00438D98`, `004439AE`, `00444864` and the inline path's).
  - This is proven inductively over each pass loop: every counter starts at 0 and gains 1 on every back edge.
  - The walks write `+0x1D8 + 4p` with that same p. The value comes from the float track 0x10 bytes before the pass's
    slot, evaluated at `00449AB0`+0x543. So a mode-2 pass scales by the scalar authored for its own slot.
- **The pass bytes are authored.** Each walk goes through the definition's four `0xF0`-byte pass slots (type `0x05`:
  definition `+0x250`).
  - For the p-th kept slot it copies slot byte `+7` to `+0x1B0 + p` and slot byte `+0xB` bit 0 to `+0x1B4 + p`
    (`00449D08`).
  - It skips a slot whose byte `+0` is 0 or whose texture lookup fails, and later slots move down (executed, 2,592 slot
    patterns per walk).
  - The element setups, `00538DB0` among them, leave those bytes as loaded.
- **What ships.** All EFX streams, all locales; 9,846 active pass slots, none of mode 5 or above:

| element type | active slots | mode 0 | mode 1 (axis y / z) | mode 2 | mode 3 (y / z) | mode 4 (y / z) |
|---|---:|---:|---:|---:|---:|---:|
| `0x05` kind-`0x54` mesh | 9,622 | 9,294 | 54 (28 / 26) | 152 | 21 (7 / 14) | 101 (44 / 57) |
| `0x04` ring band | 173 | 157 | 0 | 16 | 0 | 0 |
| `0x06` column | 51 | 47 | 3 (3 / 0) | 0 | 1 (1 / 0) | 0 |

  - **Mesh paths.** `00437130` meets mode 2 only (8 slots). Mode 1 runs on `00438860` 24 times and inline 30, mode 3 on
    17 and 4, mode 4 on 36 and 65.
  - **Grid paths.** `004434D0` meets modes 2 (16) and 3 (1); `00444340` meets mode 1 only (3).
  - **The constant planar scalar.** 21 of the 152 type-`0x05` mode-2 slots author it as the constant 0.0.

*Not established:*
- *what the matrices hold at draw time (a runtime question). Modes 1 and 3 read one matrix global and modes 2 and 4
  another, in 79 and 269 shipped slots;*
- *the planar scalars authored as resource or curve tracks;*
- *the runtime pass index, since a failed texture lookup drops a slot;*
- *what `+0x1F1` bit 3 changes in the drawing beyond selecting the path.*
```

## 3. Unchanged

The line `*(Residue replaced 2026-10-03, SWE2-DATA, consuming OPUS-REQ-DATA-K54-LIGHTING-RESIDUE-1002.)*` stays as it
is, after the new block.

## Notes for the publisher

- **The populations differ.**
  - The section-5 figures (514 / 1,791 / 2,859 over 5,164 elements) come from the page's walk, which stops at each
    `.efb`'s first blob.
  - The new figures cover every stream (5,204 elements).
  - `census_k54_modes.py` check N3 shows that the path rule reproduces the section-5 figures on the page's own TSV.
- **The struck sentence is quoted exactly** from the working tree. Run `git diff` after applying it.
- **Run the neighbour pre-check on the NEW text before publishing.**
  - The new citation tokens are the call sites `00445AF8`, `00445AFF`, `004477D9`, `004477E0`, `004487A1` and
    `004487A8`. These are instructions inside the three grid walks, which the page did not cite before.
  - The other new tokens are interior sites of functions the page already cites.
