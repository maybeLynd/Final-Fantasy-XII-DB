# S-12: the weather apply `0026D910` executed as shipped code over the shipped tables, stub-free (OPUS, 2026-09-25, block 303)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- S-12's runtime cell is NOT MET, and `CONTRACT-weather.md` §13 reads "Empty".
- This narrow OPUS harness is the first execution of the contract's load-bearing apply.
- It is not an ORACLE EXP.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image and **stubs nothing**.
- **Stop point.** It runs `0026D910` real through its entire reach: `0017D490` / `001D50D0`, `002EF2B0` / `002EF640`, `00180620` → `001A9930` / `001A7E40` / `001F0850`, `003148F0`, `00377850` → `003777C0`, and the tail `002E3D40` → `00264F10` / `00265920` / `003777A0` / `003777B0`. It **stops at the entry of the presentation body `0040AAD0`** (a stop boundary, not a stub) and records that call's arguments.
- **Failure rule.** Entering any other function fails a case.
- **Data.** Both authored tables are the **shipped files**, loaded verbatim from the vbf extract (`in` locale):
  - `map_ref.bin` (`MRF\x02`), published at `[02099D88]`;
  - `gramap_weatherinfo.bin`, published at `[02ADD0B0]`.

  Their SHA-256 values are in `result.json`.
- **Fixtures** are planted data only:
  - the lazy-singleton cells `[01F81428]` (debug block; `+0xAAC` = the override), `[01F82EA8]` and `[01F81168]`;
  - the loaded guard `[02099D90]`;
  - the payload bytes `+0x1044` (field), `+0x1060` (committed slot) and `+0x1061` (restore gate).
- **Test choice.** The field and selectors are **chosen from the data** by the shipped extractor, so the slots under
  test carry distinct, non-zero values. That gives field 464 (selector 351, block 39), and selector 43 for I-5.

**5 / 5 cases pass, identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `ungated-commit` | the commit and the postcondition | slot 3 requested from committed slot 1 → `+0x1060` = index 2, `+0x1061` = 0; `02099DA8` / `DAC` / `DB0` / `DBC` written; both `00377850` extractions use slot 3; `0040AAD0` is entered with slot 3's preset (5), field-2 value 0 and field-3 value 1 |
| `gated-discard-and-split-slots` | **I-3** (the gate discards) + **I-7** (the apply is not slot-atomic) | with the gate armed, the request is **discarded** (`+0x1060` stays 0) and the gate is **cleared once**. The gameplay extraction uses the **requested** slot 3 (so `02099DAC` = 2, the `≥ 4` class of preset 5), while **`0040AAD0` receives the committed slot 1's preset 2**: slot 1's sky under slot 3's combat class, exactly as I-7 states |
| `i2-saturation` | **I-2** | requests 0 and 1 → index 0; 9 → 2; −5 → 0; 2 → 1. Nothing reports |
| `debug-override-forces-slot` | the debug `+0xAAC` override (§3 table) | override 2 with request 3 → index 1: the positive override replaces the argument |
| `i5-selector-bound-slot-unchecked` | **I-4 / I-5** | `003777C0` returns 0 for `selector = count`. Slot 0 of selector 43 equals selector 42's slot 3, and slot 4 equals selector 44's slot 1 (both 1), while selector 43's own slot 1 reads 0. **The slot is not bounds-checked, and the `−1` bias of I-4 is visible** |

## Related execution not cited in the row

EXP-144 (S-46) and EXP-106 (S-15) run three other weather entries stub-free:
- the alternate resolver `0025ABA0`, both arms;
- the probability call `002658B0`;
- the init core `002620E0` (P-1 / P-2's latch).

Neither record names the weather contract.

## Not covered

- the roll `0025ACA0` end to end;
- the verb handler `003565C0`;
- the presentation body `0040AAD0` itself;
- a live game.
