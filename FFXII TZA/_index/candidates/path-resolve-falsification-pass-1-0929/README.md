# Consumer check: falsification pass 1 on how-a-path-is-resolved-to-bytes (OPUS, 2026-09-29)

corrects: 02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-a-path-is-resolved-to-bytes.md (§3 the census row "24")

## What was corrected

- **The census row `24`.** The site is `001DAFD8`'s `lea r8d, [r14 + 3]`. Every path to it writes `r14b` to 0
  (`001DAEA2`) or 1 (`001DAFB5`), so it passes 3 or 4. Both log nothing under §4's rule. `CON-165`.
- **Made exact.**
  - The `1 × 13` row is 11 sites of `00597970` plus both sites of `00597930`, whose selector arrives in `r9b`.
  - Route 1's hash is `00674A00`.
  - Route 2's MD5 is `0019AEE0`.
- **What survives.** The vtables and slots, `IsOpen`, the ownership bit, the prefetch token loop, the resolver's six callers,
  the three tags, and both key derivations.

## Current consumers

- consumer: [how-the-prefetch-manifests-are-read.md](../../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md)
  agrees. Its line on `0x001DAFD8` already says "computes `r14+3` (3 or 4)".
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-165`).
- consumer: [ta-texture-animation-lists.md](../../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md) agrees.
  It derives the same 33-multiplicative hash that R7 locates in `00674A00`.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_path_resolve.py`, checks R0-R8.
- R3 fails if `r14b` gains a third write, or if a path reaches `001DAFCC` without one. It rejects "24".

run: verified at 44bf9ce41 (BROKEN 0), against the certified image `73461d08…`.
