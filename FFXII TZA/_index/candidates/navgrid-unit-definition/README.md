# The unit-definition page's grid-rebuild row, corrected, and an unread density scale (FABLE, Claude Opus 5.5, 2026-09-27)

**State: PENDING REVIEW, and PENDING PROPAGATION for the page.** The page is an overlay carrier (overlay-publication-plan
ruling 1), so its hunk publishes through SWE2-FRONTIER (FABLE-REQ-FRONTIER-PUBLISH-NAVGRID-ON-CARRIER); the edit is
[`page_edit.py`](page_edit.py), which applies to HEAD and refuses a non-unique match. The review is requested from SWE2-AUDIT-SPEC. FABLE is the author, and ASTRA is the source
package's author, so neither can review this.

**Source.** The formula comes from ASTRA's source package `_experiments/evidence/nav-grid-quantization/` (`d0faaa923`,
ASTRA-RETURN-FABLE-NAV-GRID-QUANTIZATION). The one authored case comes from `_experiments/evidence/authored-grid-shape/`
(`09e941af2`, ASTRA-RETURN-FABLE-AUTHORED-GRID-SHAPE). OPUS's `nav-grid-consumers/` record covers the corridor contract
and the store, and routed this page to FABLE.

## What was learned

**The grid rebuild `003924B0`, re-read from the image** ([`navgrid_unitdef.py`](navgrid_unitdef.py), [output](navgrid_unitdef.out)):
- **G1.** `003924CB` stores `n` = 0x24 to `02AEE0B8` *before* the bounds getter `00383740` (`003924E4`). A zero return
  jumps to the epilogue, so that store is the one effect that happens regardless.
- **G2.** The budget is `(0x2800 − n) / (n + 1)` = 10204 / 37 = **275** cells, by integer `idiv`. The page's old
  `0x2800/(n+1)` would give 276, and it omitted the subtraction.
- **G3.** `c0 = sqrtf(w·h/275)`, and the builder refines it to `max(w/trunc(w/c0), h/trunc(h/c0))`. It then stores
  `floorf(refined) + 1.0` as `NavGridParams.cellSize` (`02AEE090`). Each dimension is `trunc((w + cell − 1)/cell)`, and the
  allocation is `cols·rows·(n+1) + n` bytes.
- **G4, new here:**
  - **The caller's density scale is never read.** `002342F0` picks 8.0 for an area up to 20000, 12.0 up to 30000,
    else 16.0 (`.rdata` thresholds `009146F8`/`009146FC`). It passes that scale in `xmm0` (`0023441B`) to `003924B0`
    (`0023441E`).
  - `003924B0` reaches a call (`003924E4`) before it touches `xmm0`, and the call clobbers the register. Its first
    `xmm0` access after that is a write (`00392575`). The getter's first `xmm0` access is a write too (`00383789`).
  - `0023441E` is the only caller. Scanning the whole file for the VA as a dword or qword finds nothing, and the RVA
    appears 3 times, all as unwind records (`.pdata` plus two chained-unwind copies).
  - So in this build the tiers change nothing, and the cell budget is the constant 275.
- **C (control for G4's detector).** `00229EE0`'s first instruction stores `xmm0` to a global: a read before any call.
  The detector reports it as a read.
- **N (arithmetic).** A 50 × 50 rectangle gives cell 4, 13 × 13, and 6,289 bytes. Without the floor it gives 4.125,
  12 × 12 and 5,364. This is recomputed in f32, and matches ASTRA's authored case.

## Affected current consumers

| consumer | action | agreement |
|---|---|---|
| `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`: grid-rebuild row; the "handing it to `003924B0`" sentence | row corrected (old text struck); unread-scale sentence added; the authored case added with its limits | routed-to-FRONTIER (carrier publish of `page_edit.py`) |
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` nav-grid BSS row (070/078/080 labels) | OPUS's `nav-grid-consumers/` | OPUS's |
| `_types/types.tsv` NavGridParams ctor | OPUS's `nav-grid-consumers/`; the unread scale is offered to OPUS as a note | OPUS's |
| `_types/fields.tsv` NavGridParams rows; vestigial `074`/`084` | already agree; not reopened | agrees |
| `21-RNG-And-Determinism/which-roll-is-on-which-generator.md` 294; `L2-VERDICTS.md` 2185/2194 | name the builder; state no budget or scale | agrees |

## Limits (not claimed)

- **No execution.** Nothing ran the builder, the imported `sqrtf`/`floorf`, the allocator or a live map. The 50 × 50
  case is arithmetic over one authored header.
- **The authored case is one extracted copy, identified by SHA-256.** Its archive provenance, whether the game loads
  it, and how common its shape is are ASTRA's stated open items.
- **G4 establishes an unread argument in this build.** It does not say why: a leftover signature is the obvious
  reading, but that is not evidence.
- **No zero, NaN or huge-rectangle behaviour** and no bound on the allocation are claimed.
