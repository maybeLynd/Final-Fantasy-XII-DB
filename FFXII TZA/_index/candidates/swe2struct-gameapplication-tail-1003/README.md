# SWE2-STRUCT ruling: GameApplication is declared (0x1140 at 01F7E350) and the boot static is re-based to 01F7F490 (2026-10-03)

affected: `_types/types.tsv` (GameApplication, PApplication route, AppBootStatic01F7F490), `_types/fields.tsv` (GameApplication rows, AppBootStatic01F7F490 rows)

*SWE2-STRUCT (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-STRUCT-GAMEAPPLICATION-TAIL-1003. A
route-level choice in the store; OPUS (with repos-91's measurement) offered two shapes.*

## SWE2-STRUCT ruling: shape A - no overlap

The store declared only the 0x1130 `PApplication` base at `01F7E350` and a separate 0x124 static at `01F7F480`. The bytes
say the object at `01F7E350` is larger:
- its slot-0 deleting destructor passes **0x1140** to the sized delete (`0017CCB0 mov edx, 0x1140` / `0017CCB8 call
  0016D6A0`; the callee is a bare `ret`, so nothing is freed, but the size is the class's), so it spans
  `01F7E350..01F7F490`;
- its own methods use `[this+0x113C]` (`0017D074 mov byte [rbx+0x113c], 1`; `0017CCD6 cmp byte [rcx+0x113c], 0`) and
  `[this+0x113D]` (`0017CD1E cmp byte [rbx+0x113d], 0` / `0017CD31 mov byte [rbx+0x113d], 1`) - re-read here.
`01F7E350 + 0x1130 = 01F7F480`, so the boot static's first 16 bytes are this object's tail; overlapping two statics
(shape B) would leave two types claiming one cell. Applied:
- **GameApplication** 0x1140, `STATIC 0x01F7E350`, ctor `0015BC40`, dtor `0017CC70`; fields `+0x0000 base PApplication`,
  `+0x1130` qword and `+0x1138` dword (moved unchanged from the static's `+0x00`/`+0x08`), `+0x113C startupLatch` and
  `+0x113D runOnceGuard` (the two bytes the store had as the static's `word000C`; the boot body's word store `0015BC68`
  clears both), `+0x113E` reserved.
- **PApplication**: its route's `STATIC 0x01F7E350` becomes `EMBED GameApplication +0x0`; the PTR route stays.
- **AppBootStatic01F7F480 -> AppBootStatic01F7F490**, 0x114 at `0x01F7F490`; its 51 rows at `+0x10` and above are
  re-based by -0x10 with the old offset recorded in each row's evidence.

## SWE2-STRUCT consumers

- consumer: `game-application.md` (the startup latch `+0x113C`, slots 4/7/8) - agrees; the store now names the cell on
  the object the page describes.
- consumer: OPUS's `l2_recut_AppBootStatic01F7F480` offset map - revised-here (re-based offsets; OPUS applies its
  non-structural re-cuts on the new rows).
- consumer: derived listings that name the old type (TYPE-COVERAGE, census outputs, the knowledge mirror) - routed-to-
  their generators: they regenerate from the store.

`types_index.py` after the edit: `843 type(s), 9191 field(s), 3 error(s)` - the three are the off-ladder readiness values at
HEAD from `c6de67245`, unchanged; `check_static_spans.py` reports no GameApplication / PApplication / AppBoot overlap.
