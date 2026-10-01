# The scratch block's per-unit record and the field map's movement-flag rows corrected on GR-8 (FABLE, 2026-09-30)

Request: `DATA-REQ-FABLE-GR8-PAGE-CORRECTIONS-0930`. Source: OPUS's record
[`gr8-unit-record-64-0930`](../gr8-unit-record-64-0930/README.md), section "Contradictions and consumers (routed, not
edited here)", commit `48de14c6b`. Pages:
[the formula scratch block](../../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md) §2.5 (and its §4
layout block, which states the same fields), and
[the battle-unit field map](../../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md), rows `0033D890` and
`0033CB10`.

The edit is staged as `Database/Tools/work/FABLE/pagecorr/apply_gr8.py`. It has 8 anchors over the two pages, and each
matches once. It is CRLF-safe and all-or-nothing, and `--check` validates without writing. Every byte fact the edit
states was read again in the image by [`gr8_page_check.py`](gr8_page_check.py) → [out](gr8_page_check.out), 57 steps,
**FAILS 0**.

## What is applied

**Scratch block §2.5 (the per-unit record table).**
- **`+0x10`.** "the previewed action id (`003857E1`)" is struck. The preview saves the word (`003857A3`), clears
  `+0x10`..`+0x13` (`003857B2`, a dword store) and writes the saved word back (`003857E1`). The previewed id goes to
  `02AEDFD4` (`003857EC`). Only the `0x9F` draw (`00387ADE`) stores an id here.
- **Reader column.** The "—" is struck for three fields:
  - `+0x00` is read by `00388E60`, `0038DA68`, `0038ED17` and `0038EDD6`.
  - `+0x04` is loaded at `0038633F` for a `bt` that stores result kind 6 (`00386347`).
  - `+0x08` is loaded at `003862FB` for a `bt` that stores kind `0xA` (`00386303`).
- **`+0x00` width.** "u64" is struck and replaced by u32. Every access other than the clears is a dword (`00388E51`,
  `0038DA5D`, `0038ECD5`, `0038ECFF` write, and the four reads above). OPUS's record raises this against the register
  row and the combos page. The §2.5 row makes the same claim, so it is corrected here too.
- **New rows:**
  - `+0x0C`: marked targets. `00387B97` sets the mark, and there are 15 direct call sites of `00387B00`. `002FA352`
    reads it.
  - `+0x14`: the HP-credit tick counter, through `00386860`'s `0208D494` / `0208DE94` anchors.
  - `+0x18`: the walking-MP carry (`002F95A6` / `002F9474`).
  - `+0x1C`: movement flags, bit 0 and bit 1 as in the field-map correction below.
  - `+0x20`..`+0x3F`: nothing accesses it. The activation clear is exactly four qwords, `00386C5B`–`00386C66`, and
    OPUS's census finds no wider access.

**Scratch block §4.** The layout block is code, so nothing inside it is struck. A dated note under the block says
three things: `+0x00` is u32; `+0x10` holds only the `0x9F` draw, not "lastActionId"; and "nothing touches the rest"
is true only of `+0x20`..`+0x3F`.

**Field map, row `0033D890`.**
- "`+0x1C` bit 1 (the bit `0033CB10` sets" is struck. The bit `0033CB10` sets is value 1, bit 0 (`0033CB60`), and the
  solver tests value 1 (`0033D953`).
- Bit 1 (value 2) is the solver's own latch: it is set at `0033DA73` and tested at `0033DA77`.
- "`+0xEA9` category" is struck and replaced by the slot index.

**Field map, row `0033CB10`.** "(the perception category)" is struck and replaced by "the unit's slot index", which is
what the page's `+0xEA9` row and CS-6 say.

## What is not applied, and why

- **"called from 15 formula-slot functions"** (OPUS's `+0x0C` row) is written as "15 direct call sites". retool's
  index finds 15 sites, but its extents place them in 14 functions. The two counts may differ only in extents, and
  this check does not settle which is right.
- **The register row GR-8, the combos page's Limits ("u64"), and `_types/fields.tsv`** are OPUS's routing and outside
  this request. Nothing was edited there.

## Limits

- Static only. Each cited instruction is decoded linearly from its function's start, and the check confirms that the
  function forms its address from the record banks by a `lea`. Full base tracking, the 57-access census and the
  "`+0x20`..`+0x3F` never accessed" result are OPUS's `structflow` work (`gr8_record_census_check.py`). This check does
  not repeat them.

## Check

[`gr8_page_check.py`](gr8_page_check.py) → [out](gr8_page_check.out): 57 steps, **FAILS 0**. Controls:
- **P1:** the known restore at `003857E1` must decode.
- **P2:** a raw `.text` `lea` scan into the banks must give OPUS's 34 sites (16 + 16 + 1 + 1).
- **P3:** a wrong expectation, "the solver tests value 2 at its bit-0 test", must fail to match.

## Consumer check

affected: `Database/FFXII TZA/08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`

- consumer: `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` §2.5 table and §4 layout block: revised-here.
- consumer: `08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md` §2.2 row `02AEDFD4` ("the preview stores it", id `0x9F` replaced by the record's `+0x10`): agrees.
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` rows `0033D890` and `0033CB10`: revised-here.
- consumer: `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` `+0xEA9` row ("slotIndex"): agrees.
- consumer: `07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md` ("the saved `+0x10` word is restored"): agrees.
- consumer: `08-Combat-Formula/combos-and-the-guard-parry-flag.md` Limits ("u64"): routed-to FABLE (OPUS's record names it; not in this request).
- consumer: `_index/OPEN-QUESTIONS.md` row GR-8 ("u64", "previewed / drawn action id"): routed-to OPUS (no register edit here).

## Regression

run: gr8_page_check.py at 4b748e8af (FAILS 0; controls P1 to P3)
