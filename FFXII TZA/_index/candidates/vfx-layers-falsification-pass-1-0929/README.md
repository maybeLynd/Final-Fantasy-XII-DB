# Consumer check: falsification pass 1 on the-six-vfx-display-layers (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md (four appended notes: CON-180)

## What was corrected

- **SWE2-EC7-99, `002D7E00`.** The zeroed table is `0209E6C0 + id * 48`, not `0209F6C0`. The notify `002D7E30` gets the
  id, the caller's `rdx` and `r8`, and `r9` = 0. It is not `(ecx, 0, 0)`.
- **The `001B2530` note.** `0017D980`'s answer picks between `0017FEE0` and `0017FE60`, and `edi > 5` is only their
  argument. The second emit always uses `0017FEE0`, the third `0017FDE0`.
- **The `0039CFF0` note.** `00258EE0` calls it only in layer 4, twice, with ids `0x3C00` / `0x3700`. The reallocation
  passes `0x100` / `0xE0` / 1, not "`0xE0 + [rsp+0x20]` entries".
- **SWE2-EC7-106, `0024C640`.** It runs from `00258EE0`'s shared tail after layers 1, 2 and 4 on every request, and from
  `002590F0`. It is not a reload-only quiesce.
- **What survives.**
  - Sections 1, 1a, 1b and 2: the layer table and its five markers, the group order and the drain, and the odd waits.
  - The group draw's three conditions, the group gate, the nine published globals and the per-container gate's kinds.
  - The notes on `00862C30` / `00862C10`, `0024C640`'s body, `00183060`, `00376320`, `0036F550`'s submit, `0036F9F0`'s
    records and `001B2530`'s stores.

## Current consumers

- consumer: `02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md` says `002D7E00` passes through a
  caller's id and names no table address; it agrees.
- consumer: `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md` lists `002D7E00` as a callee only;
  it needs no change.
- consumer: `17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md` names `001B2530` as
  a writer and does not restate the pick; it needs no change.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-180`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_vfx_layers.py` V9 to V12. Each row fails unless:
- V9: `002D7E00` addresses `0209E6C0` and never sets `edx` / `r8d`;
- V10: the `0017FEE0` / `0017FE60` branch follows `0017D980`'s test;
- V11: `0039CFF0`'s only call sites in `00258EE0` lie in layer 4's arm;
- V12: `0024C640`'s only call site in `00258EE0` is the shared tail `00258F8B`.

run: verified at 6c43f86d5 (BROKEN 0, exit 0), against the certified image `73461d08…`.
