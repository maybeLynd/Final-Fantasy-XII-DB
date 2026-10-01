# Consumer-check record — DD content pass on eight PARTIAL pages (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/04-Actor-Entity/the-field-runtime-pass.md`
affected: `Database/FFXII TZA/04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md`
affected: `Database/FFXII TZA/05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md`
affected: `Database/FFXII TZA/07-Combat-Action/how-a-combo-continues-and-what-it-blocks.md`
affected: `Database/FFXII TZA/07-Combat-Action/Action-Definition-Row/the-action-definition-row.md`
affected: `Database/FFXII TZA/08-Combat-Formula/combos-and-the-guard-parry-flag.md`
affected: `Database/FFXII TZA/08-Combat-Formula/where-a-stat-number-comes-from.md`
affected: `Database/FFXII TZA/08-Combat-Formula/Recipe-System/ranged-weapon-recipes.md`

## What changed

This pass does the DD content work OPUS's owner read asked for
([`../dd-owner-read-0929/worksheet.tsv`](../dd-owner-read-0929/worksheet.tsv)). For each page it:
- fills the missing sections from what the page already establishes;
- anchors the uncited claims;
- answers the residue from the binary where it could, and registers what remains ([`new_rows.tsv`](new_rows.tsv), 8 rows);
- reconciles stale prose.

Most edits reconcile stale text. The corrections below change a published claim, and each lists its consumers. Strikes
cover only text that was on the HEAD page.

### Corrections that change a claim

| # | page | old claim | new claim | evidence |
|---|---|---|---|---|
| 1 | where-a-stat-number | the party helpers "take the **level** at `+0x08`" | they scale the base HP (`+0x08`) and base MP (`+0x0C`) by party-row bytes; no level | `002F8E50` (30 B) and `002F9180` (21 B) read whole; call sites in the rebuild |
| 2 | where-a-stat-number | "two dwords of affinity flags are OR-ed in" | two status-word masks (row `+0x4C` into stats `+0x38`, row `+0x48` into stats `+0x3C`) | stores at the rebuild's `002FF0D3` / `002FF0D9` |
| 3 | where-a-stat-number | every clamp floors a negative at 0 | the main value (max HP) floors at 1 | the `r15 = 1` compare in the main-value clamp |
| 4 | the-action-definition-row | `+0x0A` "a small count; what it counts is not fixed", tallied as u16 | the MP cost, read as a byte; `+0x0B` is a separate byte (GR-5) | byte reads at `002F962B` and `0031DBD2`; where-mp-comes-from §2 (CS-5) |
| 5 | the-action-definition-row | `+0x38` "low byte 1 or 2, high a per-spell index; reader not found" | page 0–10 / row 0–16 of the player's list; reader `00237FC0` | §7's 2026-09-18 narrowing; the UQ-80 record's review correction |
| 6 | the-action-definition-row | `+0x3A` values "12–16" | 10–16 (10 and 11 once each) | `adr_tally.py` over the 543 rows |
| 7 | the-action-definition-row | `+0x28` "a per-Esper-attack index"; §2.3 and the struct fence "Esper attacks" | the 26 Quickening-family rows (the §2.2 shipped column's 2026-09-27 correction, carried to the other three places) | the UQ-80 record |
| 8 | ranged-weapon-recipes | §5 put the threshold loader, the weather scales and the outcome resolvers in the committed list, and named two element stages | the decoded lists: those steps are in the first list; neither recipe names slots 25, 94 or 95 | `rwr_recipes.py`, `rwr_slots.py` |
| 9 | ranged-weapon-recipes | "a UI damage preview runs the first list … change both or previews will lie" | the first list runs at execution (stage 9) and decides hit / evade / knockback / weather accuracy | the stage-9 call in `BattleUnit_AdvanceStandardActionState`; scratch block §2.5 / §5; AJ-7 |
| 10 | ranged-weapon-recipes | §4 ActionDefinition `+0x12` → hit chance, `+0x13` element, for these recipes | neither is read by recipes 25 / 26; the hit chance starts at 100 (slot 22) | slot 22's body, read whole |
| 11 | the-field-runtime-pass | `GetRecordByOrdinal(actor, word [actor + 0x50])` | `(slot, word [slot.payload + 0x50])` | the first-drive block of the pass |
| 12 | the-field-runtime-pass | "slot 3 additionally on one conditional path" | slots 0–4 on the mode-0 path, slots 3–4 on the mode-1 path | the tick's slot loop |
| 13 | the-field-runtime-pass | wait `+0x27` "set only by kinds 3 and 6" | kinds 3, 6 and 7 (kind 7 shares kind 6's store) | the resolver's jump table, decoded |
| 14 | the-field-runtime-pass | `001EDE80` "group-2 set still populating" | the HALFRATE step count | its two getters' globals |
| 15 | battle-record-kind-byte | AL-1 "unanswerable from the binary" | answered 2026-09-10 (the definition table the unit was built from) | AL-1's register row |
| 16 | spawn-placement-and-retirement | L-12 / L-13 "register row is WITHDRAWN" | SUPERSEDED (2026-09-26, 2026-09-27) | the register rows' lead words |
| 17 | spawn-placement-and-retirement | upstream "encounter/spawn controllers"; `004058E0` a "spawn-record body" | the raw call index's named callers; `004058E0` is a per-frame extent/scale step with no spawn state | the raw call index; the body, read whole |
| 18 | spawn-placement-and-retirement | FRONTIER-subtree sizes (`003145E0` 168 B, `00584580` 238 B, `00314440` ~117 B, `0032ED80` ~62 B, `0037AA90` ~78 B, `001831A0` 17 B), one call list, three copy descriptions, "no shared callees" | 563 / 143 / 233 / 1,001 / 491 / 21 B; call list and copies corrected; shared callees listed | function extents; disassembly |
| 19 | how-a-combo-continues / combos-and-the-guard-parry-flag | the combo cap reads the **target's** class row | the **attacker's** | the slot's first argument is the source |
| 20 | combos-and-the-guard-parry-flag | "status bit 23" | unit flag bit 23, the engaged flag | the guard/parry mode roll's test |
| 21 | how-a-combo-continues | "No document has read what any `+0x6B4` value means" | struck: UQ-118 / UQ-108 read them | the page's own §8 |

## Consumers

- 1: `CONTRACT-stat-derivation.md` line 61 says "plus the level at `+0x08`". **routed-to-OPUS** (the contract's
  implementer of record; it is not in this batch). `Battle-Stats-Record/the-battle-stats-record-field-map.md` (`+0x008`
  base HP) **agrees**.
- 2: no other page says "affinity flags" for these dwords. The UQ-80 manifest (`chr_data` `+0x48` / `+0x4C`) **agrees**.
- 3: `CONTRACT-stat-derivation.md` §10 (floor `r15d = 1`) and the field map's `+0x024` row **agree**. The field map
  gives the foe cap as 999,999,999, but the literal is 1,000,000,000 (`0x3B9ACA00`). **routed-to-field-map owner**.
- 4, 5, 6: `where-mp-comes-from.md` §2 and `battle-command-availability-and-reason-codes.md` (Mist charges ×
  `+0x0A`) **agree**. The AY-2 row (list position) **agrees**. `uq80-table-field-coverage/uq80_manifest.tsv` still lists
  `action_data` `+0x0A` (and `+0x04`, `+0x1D`, `+0x1F`, `+0x20`, `+0x3A`) as shape: **routed-to-FABLE** (UQ-80 record
  refresh; the record is SUPERSEDED and its residue list is the named follow-on).
- 7: the UQ-80 README **agrees**. The page's own falsification table (§9, 2026-09-13) still quotes "26 Esper attacks"
  as the claim it checked; that is dated history and is left as written.
- 8, 9, 10: `Step-Table/combat-formula-step-table.md` (slots 96–99, the element family) and
  `Scratch-Block/the-formula-scratch-block.md` (the preview runs before the action executes, and its memo is read back)
  **agree**, as does AJ-7. `CONTRACT-weapon-recipes.md` RW-2 ("the first list is preview-side") **agrees** in wording.
  Its §14 residual calls `0x3858E7` statically orphaned, but that address is inside `BattleFormula_EvaluateTargetPreview`,
  which has two direct callers. **routed-to-FABLE** (the contract's author).
- 11, 12, 14: no other page states the old forms. The world-tick page and the game-settings page **agree**.
- 13: the actor-request page **agrees**. `Actor-Storage-Record/the-record-behind-every-actor.md` (L1819, and its kinds
  table) says kinds 3 and 6 only: **routed-to that page's owner**.
- 15: the inbound links (availability §11, when-a-group-is-wiped §2, status-write §2) do not rely on AL-1 being open;
  **agrees**. Separately, `Battle-Unit/the-battle-unit-field-map.md` L1022 says `00321810` writes `edx ? 1 : 0` at
  `+0x19`, but the byte stored is 0. **routed-to that page's owner**.
- 16: the L-12 / L-13 register rows **agree** (they are the source).
- 17: `_index/ADDRESS-INDEX.md` maps `004058E0` to the spawn page: **routed-to-SWE2-FRONTIER** (residual placement).
- 18: the page's own §12 / §16 / §27 already had 563 / 143 / 233 and the copy widths; they **agree**, and the rest
  is **revised-here**.
- Also under 16–18: `09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md` L1632 says the restore "copies them
  back" (both banks), against ASTRA's one-bank correction. **routed-to that page's owner**.
- 19: `CONTRACT-combo-continuation.md` (CB-3 item 4, "foe-class record") and the unit-definition page §2.1 **agree**.
- 20: the scratch block's `02AEDFC4` row and the field map's bit-23 row **agree**.
- 21: the field map's `+0x6B4` row, native-command-seam §7 (UQ-108) and the gambit page **agree**.

## Regression

Every script is in this folder, and each prints a control before its answer. The page checks ran on a `git archive`
export of the HEAD named below with the drafts applied (`apply.py --keep-placeholders`), not on the shared tree.

run: rwr_recipes.py at 4407f8484, control pointers for recipes 25 / 26 match; both lists reproduce the page's §2
run: rwr_slots.py at 4407f8484, control slots 35 / 42 match; slots 25, 94, 95 absent from both lists
run: wsn_lists.py at 4407f8484, control constant reads 10.0; three lists of 16 / 16 / 12 ids
run: adr_tally.py at 4407f8484, 543 rows x 60 B; 39 bit-15 words, 436 bit-15-clear, 68 sentinel
run: record_flag_or_sites.py at 4407f8484, 15 sites, control 8 of 8
run: dd_verdicts.py at 4407f8484, verdicts before and after in README.md; documented_rule.py S self-test PASS (32 cases) on the live tree
