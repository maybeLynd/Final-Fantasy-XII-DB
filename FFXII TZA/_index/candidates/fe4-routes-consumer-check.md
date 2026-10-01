# Affected-consumer check: BattleStatsRecord store corrections (FE-4 follow-up, OPUS, 2026-09-27)

**State: PENDING REVIEW.** Independent review is routed to SWE2-AUDIT-SPEC.

Corrects: `_types/fields.tsv` BattleStatsRecord `+0x05C` (with `+0x060`), `+0x1C3` (with a new `+0x1C4`) and `+0x1C5`.

**Scope.** FE-4's register answer is FABLE's: `_index/candidates/fe4-untouched-ranges/`, reached independently on the
same day with the same result. OPUS withdrew its own register and page answer for FE-4 so as not to publish a
competing text. This record carries only the type-store corrections, as the store's owner. That includes the one
FABLE's record routes to OPUS (`FABLE-REQ-OPUS-STATS-5C-TYPE-ROW-AND-2.3B-GAP`).

**The corrections** (`_index/candidates/fe4-routes/fe4_routes.py`):
1. **`+0x05C` 'slotCounter5C' is not a stats-record field (R6).**
   - Its three accesses, `00386E43` / `00386E56` / `00386EEC`, are `[r14 + r12 - 0x60]`. Here `r14 = stats + 0xBC + 4i`
     (`00386C90`), `rsi = stats` (`00386CA6`) and `r12 = result - rsi` (`00386CBE` / `00386CC6`).
   - So they address `result + 0x5C + 4i` (FE-3, 2026-09-13).
   - `+0x05C`..`+0x063` becomes one 8-byte unobserved region: after the u16 at `+0x5A`, before the u32 at `+0x64`.
     Alignment cannot produce it (R4), and no route reaches it (R1–R3).
2. **`+0x1C3` / `+0x1C5` are the three byte-wide licence-board selectors (R5),** as the field map's own §2.3b table
   has said since 2026-09-17. The initialisers' `0xFFFF` word store sets `+0x1C3` and `+0x1C4` together.

**Regressions.**
- R5 and R6 fail on the pre-fix store and pass after it.
- R2's bias is now per form: a form that adds `+8` itself reads its displacement as written. The earlier "both biases"
  reading turned three `[rec + 0x64]` loads into false `+0x5C` hits.

**Consumers:**

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` BattleStatsRecord rows above | corrected; history kept in each evidence cell | revised-here |
| the battle-stats field map (§2.3 sentinel sentence, "every one of them … pads" in §2.3b, the layout summary line) | routed-to-OPUS by FABLE; edited 2026-09-27 after FABLE's 71a0ed9c0 (FE-4 part 2: the 2.3 sentence, the 2.3b table row and conclusion, the struck `+0x5C is private` bullet and the layout summary; regression `fe4-routes/fe4_page_check.py` P1-P4) | revised-here |
| `_index/OPEN-QUESTIONS.md` FE-4 | FABLE's answer; not edited here | agrees |
| `04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md` §2.5 (the initial `0xFFFF` / `0xFF` values) | the values stand as the selectors' "none" defaults | agrees |

Run receipt: executed at 424eff121 - `fe4_routes.py` R1–R6 PASS, FAILS 0, after the store patch (R4–R6 fail on the pre-fix store); `types_index.py --validate` 0 errors, 0 gaps; `check_census_widths.py` flags +0x1C3 declared 1 against the initialisers' paired 0xFFFF word store over +0x1C3/+0x1C4, the documented shape.

Part 2 receipt (2026-09-27): `fe4_page_check.py` FAILS 4 (P1-P4) on the page at 71a0ed9c0 and FAILS 0 after `Tools/work/OPUS/fe4p2/patch_page.py` (tested first on a copy through PAGE_PATH).
