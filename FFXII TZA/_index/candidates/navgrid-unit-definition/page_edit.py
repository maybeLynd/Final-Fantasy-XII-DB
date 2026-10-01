"""Unit-definition page: the grid-rebuild row corrected on ASTRA-RETURN-FABLE-NAV-GRID-QUANTIZATION, the unread density
scale, and ASTRA's one authored case as arithmetic (FABLE, Claude Opus 5.5, 2026-09-27). Strikes verbatim, per line."""
from pathlib import Path
P = Path(r"C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md")
REC = "../../_index/candidates/navgrid-unit-definition/README.md"
E = [
 ("scale from the `.rdata` thresholds at `009146E8`–`009146FC` before handing it to `003924B0`\n"
  "(`0023441E`) — the grid rebuild below.",
  "scale from the `.rdata` thresholds at `009146E8`–`009146FC` ~~before handing it to `003924B0`~~\n"
  "~~(`0023441E`)~~ — 8.0 up to an area of 20000, 12.0 up to 30000, else 16.0 — and passes it in `xmm0` to `003924B0`\n"
  "(`0023441E`), the grid rebuild below. **The builder never reads it** *(2026-09-27, FABLE, Claude Opus 5.5)*: its\n"
  "first `xmm0` access is a write (`00392575`), after the getter call (`003924E4`) has already clobbered the register,\n"
  "and `0023441E` is its only caller, with no address-taken reference. So in this build the tiers change nothing, and\n"
  "the cell budget is a constant ([record](" + REC + "))."),
 ("| `003924B0` sets `02AEE0B8=0x24`, divides `0x2800/(n+1)` for the cell budget, `sqrtf`s `w*h/budget` into a cell size, "
  "derives `cols*rows` (`02AEE060`/`02AEE064`), allocates `ebx` bytes via `00384580` and memsets it",
  "| `003924B0` sets `02AEE0B8=0x24` (n) — before the getter, so a zero bounds return skips everything but that store — "
  "~~divides `0x2800/(n+1)` for the cell budget, `sqrtf`s `w*h/budget` into a cell size,~~ *(corrected 2026-09-27, FABLE, "
  "Claude Opus 5.5, on ASTRA-RETURN-FABLE-NAV-GRID-QUANTIZATION; bytes re-read)* takes the budget `(0x2800 − n)/(n+1)` = "
  "275 cells, a first size `c0 = sqrtf(w*h/275)`, refines it to `max(w/trunc(w/c0), h/trunc(h/c0))` and stores `floorf` of "
  "that `+ 1.0` as `NavGridParams.cellSize`; the origins and maxima are the getter's rectangle; it "
  "derives `cols*rows` as `trunc((w + cell − 1)/cell)` by `trunc((h + cell − 1)/cell)` (`02AEE060`/`02AEE064`), allocates "
  "~~`ebx` bytes~~ `cols*rows*(n+1) + n` bytes via `00384580` and memsets it"),
 ("is the same registry row the authored-table census attributes 170 consumers to.\n",
  "is the same registry row the authored-table census attributes 170 consumers to.\n\n"
  "**One authored case, worked as arithmetic** *(2026-09-27, FABLE, Claude Opus 5.5, from ASTRA's two returns)*. The\n"
  "formula is ASTRA's ([`nav-grid-quantization`](../../_experiments/evidence/nav-grid-quantization/README.md)). One\n"
  "authored header gives it a real input ([`authored-grid-shape`](../../_experiments/evidence/authored-grid-shape/README.md)):\n"
  "an extracted `alc0102.mpk`, identified by its SHA-256, whose slot-4 header describes a 50 × 50 rectangle. Put through the\n"
  "row above, that is cell 4, a 13 × 13 grid, and an allocation argument of 6,289 bytes. Without the `floorf` it would be\n"
  "cell 4.125, 12 × 12 and 5,364 bytes, so the case tells the two formulas apart.\n"
  "- **This is arithmetic over an authored header, not an execution.** Nothing ran the builder, the imported `sqrtf` /\n"
  "  `floorf` or the allocator on it.\n"
  "- **Not shown:** that the game loads this copy, and how common the shape is in other areas.\n"
  "- **The regression is [`navgrid_unitdef.py`](" + REC.replace("README.md", "navgrid_unitdef.py") + ").** It checks the\n"
  "  budget, the floor-plus-one and the unread scale against the image, with a planted `xmm0`-read control.\n"),
]
s = P.read_bytes().decode("utf-8"); crlf = "\r\n" in s; s = s.replace("\r\n", "\n")
for a, b in E:
    assert s.count(a) == 1, (a[:70], s.count(a)); s = s.replace(a, b)
if crlf: s = s.replace("\n", "\r\n")
P.write_bytes(s.encode("utf-8")); print("edited", len(E))
