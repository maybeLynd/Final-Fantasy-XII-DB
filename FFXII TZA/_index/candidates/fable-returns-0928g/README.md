# Consumer check: three ASTRA returns — allocator retry, nav grid block, mask reset (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md

All three are re-derived in [`alloc_nav_check.py`](alloc_nav_check.py) ([output](alloc_nav_check.out)). It decodes
from the certified image's own bytes, never from a text view, and refuses any other image. Each verdict below is
**ACCEPT**.

- **ALLOCATOR-RETRY-RETURN (A1–A4).**
  - `0036A190` is `mov edx, 1` and a tail-jump into `0036A1A0`. That wrapper tests both allocators' results
    (`0036A1D3`, `0036A1F8`) and, on null, jumps past its header stamps.
  - `0036BFE0` never reads its fifth or sixth stack argument. So the flag `0036A1A0` stores at `[rsp+0x28]` has no
    local effect. The same pattern does find the four accesses to `+0x30` / `+0x38`.
  - Its exit diamond returns every non-null result. It returns null only when both are 0:
    - ESI, the callback `[heap+0xA0]`'s result (or 0 when the slot is empty);
    - EDI, from the reclaim step `0036AAD0` / `0036ABE0`.

    Otherwise it retries at `0036C013`.
  - A heap whose bit in `022D89B8` is clear spins at `0036C000`.
  - **Not established:** what the callback and the reclaim do; whether EDI and ESI are counts or flags; whether the
    retry terminates.
- **NAV-GRID-ALLOC-RETURN (G1–G3).**
  - `00384580` skips its initializer on null (`003845BB`) and returns the null.
  - `003924B0` sizes the block `cells·(n+1) + n`, with `n = [02AEE0B8]` = 0x24.
  - It stores the result to `02AEE0A0` (`00392677`) and `memset`s it (`0039267E`). Nothing is tested between the
    call and the `memset`.
  - The block is carved into records (`cells·n`), occupancy bytes (`cells`) and the `n`-byte mask scratch. OPUS's
    `NavGridParams` field rows already record this carve.
  - **New here:** the budget `(0x2800 − n)/(n+1)` = 275 is exactly the largest cell count whose block fits in 0x2800
    bytes. 275 cells take 10,211 bytes; 276 would need 10,248.
- **NAV-MASK-RESET (M1–M3).**
  - `003912E0` takes four integers and no destination pointer.
  - It resets the mask with `memset(02AEE0B0, 0, [02AEE0B8])` at `0039130E`, before any branch or call.
  - Its only memory write outside the stack is the OR through that pointer. It returns the same pointer.
  - **Every function that ORs through the mask resets it first:** `003912E0`, `00391710` (`00391780` before
    `003918B3`) and `00391A30` (`00391AAB` before `00391BD3`).
  - The only earlier exits are the null-grid guards, which land past the OR loops.
  - The six bodies decoded from the image hold all 13 references to `02AEE0B0`, the same count as the cache census.
    None are image-base-relative.
  - So the mask is **per-query scratch in the grid block's tail**: shared by all queries, cleared on every call, and
    not supplied by the caller.

Controls (C), all in memory, with nothing written or executed:
- `0036C0B9` changed from JNE to JE flips the diamond;
- a test planted before the grid `memset` is seen;
- a branch planted before the mask reset is seen;
- an early jump into `00391710`'s OR loop fails M3.

| consumer | action | agreement |
|---|---|---|
| `where-the-games-memory-comes-from.md`, the opening ("never checks whether the memory it just asked for actually arrived") | struck and corrected: the wrappers test and the retry allocator retries | revised-here |
| the same page §1, the out-of-memory paragraph ("writes to it anyway … an instant close to desktop with no dialog") | struck and corrected: not observed; some callers test and some do not (named); no caller census | revised-here |
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` §5, "`BMASK` memsets and ORs a caller-supplied record mask" | the mask is the shared scratch at the grid block's tail, not caller-supplied; the write is heap state reached through a global pointer | routed-to-OPUS |
| `_types/fields.tsv` `NavGridParams +0x050`, "zeroed once at 0039267E rather than per query" | every writer resets it per call (M3) | routed-to-OPUS |

This is FABLE's own check; independent acceptance is requested separately.

Regression: `alloc_nav_check.py` (A1-A4, G1-G3, M1-M3, C). Run verified at 1d8a0fd1b: FAILS 0.
