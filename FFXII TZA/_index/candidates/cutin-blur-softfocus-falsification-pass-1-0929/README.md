# Consumer check: falsification pass 1 on cut-in-motion-blur-and-soft-focus (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Script-Screen-Effects/cut-in-motion-blur-and-soft-focus.md (the SWE2-EC7-90 and SWE2-EC7-112 notes: CON-183)

## What was corrected

- **`003B1130` stops at the first empty slot.** A zero key jumps to the `ret` (`003B1144` → `003B1173`). Its sibling
  `003B3B50` skips an empty tag and continues.
- **`00182490`'s out-parameters are the reverse of the note.** `rcx` receives `00186AA0`, the width, and `rdx` receives
  `00186A90`.
- **What survives.**
  - All 35 sizes, and every caller set.
  - The frame-mode gate, the late-release list and the allocator's dead size arguments.
  - The one-shot returns and the walker's release.
  - The five verb mappings.
  - Blur play's dead test and blur clear's inverted handle test.
  - The capture-once skip dword.
  - The soft-focus service and its play.
  - The teardown tail, the fade poll and the cut-in constants.
  - The other notes.

## Current consumers

- consumer: `_index/ADDRESS-INDEX.md` lists both addresses by page only; it needs no change.
- consumer: `00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md` says `0024FC80`
  tail-jumps `003B1130`, which "clears bit 1 of `+0x368` on the `02EBEC08` records". It gives no slot count; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-183`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_cutin_blur_softfocus.py` Z10 and Z11. Z10 fails unless a
zero key in `003B1130` branches to its `ret`. Z11 fails unless `00186AA0`'s result is stored through the saved `rcx`.

run: verified at ce6fccd87 (BROKEN 0, exit 0), against the certified image `73461d08…`.
