# Consumer check: the nav grid teardown (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md

**Request:** ASTRA-REQ-FABLE-NAV-GRID-TEARDOWN. The evidence is ASTRA's `nav-grid-teardown-boundary` package. Everything
below is re-derived from the certified image's bytes in [`teardown_check.py`](teardown_check.py)
([output](teardown_check.out)). **Verdict: ACCEPT.**

- **T1: the teardown body.**
  - `00392710` (45 B) loads `[02AEE0A0]` and skips the release when it is 0.
  - Otherwise it calls `003844F0`, which is `jmp 003697F0`. That routine null-tests and tail-jumps to `00369860`
    with `edx = 0`.
  - It then tail-jumps to `memset(02AEE060, 0, 0x460)`. The cleared range `[02AEE060, 02AEE4C0)` holds the 0x60-byte
    `NavGridParams` block and the 0x400 bytes after it.
  - The root `02AEDFB0` lies outside that range.
  - What `00369860` does with `edx = 0` is not re-derived here.
- **T2: the pairing, from an image-wide raw scan.** Every `E8` / `E9` rel32 in `.text` is counted when its address
  starts an instruction in the linear decode from its `.pdata` function start.
  - `00392710` has one caller: `002341D5`, in the area-teardown reset `002341C0` (← `002695A0` ← `002628B0`, the
    unload path, as the world-tick page's §"The `002341C0` exclusive subtree" records).
  - The rebuild `003924B0` has one caller: `0023441E`, in `BattleSystem_InitializeAreaState` `002342F0`.
- **T3: the grid pointer's only store.** In `.text`, the only rip-relative qword store to `02AEE0A0` is `00392677`,
  in the rebuild. The rebuild does not release a previous block first.
  - So the grid block lives from area initialisation to area unload.
  - Whether initialisation can run twice without an unload between is not established. If it can, the first block would
    be lost.
  - The scan sees rip-relative stores only. A store through a register-held address, or an image-base-relative one, is
    outside it.
- **Controls (C).**
  - The scan finds the known call `00392720` → `003844F0`.
  - A call-shaped byte sequence planted inside the 7-byte load at `00392714` is a raw hit, and the boundary test rejects it.

**The defect this corrects.** The world-tick page's `00392710` row (FRONTIER, `beb4d2f51`, 2026-09-15) gave the
released cell as `[02AE82A0]` and the cleared base as `02AE8060`. The code uses `02AEE0A0` and `02AEE060`, and the two
offsets differ (0x5E00 and 0x6000), so these are copy errors, not a base shift. The row also did not say what the
teardown is.

| consumer | action | agreement |
|---|---|---|
| `the-world-tick-and-the-field-frame.md`, the `00392710` row of the `002341C0` subtree | the two cells struck and corrected; the row now names the nav grid teardown, its init / unload pairing and the open questions (repeat init, 128-entry capacity) | revised-here |
| `_index/_inbox/SWE2-FRONTIER.md` lines 757-758 (the same cells in FRONTIER's handoff) | handoff history, immutable | unchanged |
| OPUS's `NavGridParams` rows (dtor, heap, pointer domain) | OPUS's to qualify, per ASTRA's routing | routed-to-OPUS |

Not claimed:
- the 128-entry logical capacity, from arithmetic alone;
- what the release routine does natively;
- the order of the root clear relative to unload;
- whether an initialised grid ever survives to a second initialisation.

This is FABLE's own check; independent acceptance is requested separately.

Regression: `teardown_check.py` (T1, T2, T3, C). Run verified at 1c1bb325e: FAILS 0.
