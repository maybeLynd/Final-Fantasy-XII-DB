---
system: The action definition row — the 60-byte record behind registry slot 02EBF138, field by field
category: 07-Combat-Action
status: DOCUMENTED — GR-4, GR-5, GR-6, GR-7 and UQ-107 are ANSWERED and UQ-106 is SUPERSEDED (owner re-status 2026-09-30, OPUS, on SWE2-STRUCT's DD batch 11) — UQ-106 SUPERSEDED (its residue went to AY-2, ANSWERED 2026-09-26) and UQ-107 ANSWERED 2026-09-27; re-read 2026-09-30 (FABLE), and what remained was registered and is since answered - +0x28's reader (GR-4), +0x0B's reader (GR-5), what the 436 bit-15-clear +0x24 words select (GR-6) and who reads the unit mask +0x3A feeds (GR-7)
owner_layer: PrimaryOwner:CombatAction (the formula fields are CombatFormula's, the strings Presentation's)
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every byte and word of the 543 shipped rows tallied (us battle_pack.bin, directory +0x3C), and a
    reader census that follows the inline row idiom (slot -> +0x0C -> 0020E600 -> base + stride x id)
    through the 129 functions referencing 02EBF138 and records every [row + disp] access it reaches
corpus_validated: "543 rows x 60 bytes, us battle_pack.bin directory +0x3C (2026-09-12); 41 functions with a resolved-row access"
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-action-definition-row-pass-1
  last_pass_kind: falsification
  crossref_clean: true
  reopened_count: 0
---

# The action definition row — what the 60 bytes behind `02EBF138` hold

> Every magick, technick, item use, Quickening, Esper attack and plain Attack is one 60-byte row of
> the action table. This page maps the row: which bytes the engine reads, what the shipped data puts
> in them, and which bytes no reader has been found for. It closes **AG-8** as far as the readers
> reach and leaves the rest as shape. *(2026-09-30, SWE2-STRUCT for OPUS: answered - AY-2, ANSWERED 2026-09-26: every one of the 60 bytes is placed; `+0x21` and `+0x0B` are read by nothing (AY-2, GR-5), and `+0x28` has its reader (GR-4).)*

## 1. What the player sees

Cure costs what it costs, hits for what it hits, takes its charge time, carries its element and its
help text, and — for a summon — brings a particular Esper. All of that is one row of one table, 543
rows long, indexed by the action id the engine parks at `02AEDFD4` while a recipe runs.

## 2. Native mechanism

### 2.1 The row idiom

No function calls a getter. Each reader inlines the same shape: load the registry slot `02EBF138`,
resolve its `+0x0C` reference through `0020E600` into the row array's base, multiply the slot's
`+0x08` stride (60) by the action id, add, and read (`00389046`–`00389089` is a compact example:
`BattleFormula_LoadHitAvoidGuardThresholds` fetching `+0x12`). The reader census below follows
exactly that idiom and stops when the row register is overwritten, so it under-reports: a row
pointer handed to a callee, or rebuilt from a stack copy, is not followed. 41 of the 129 referencing
functions yielded an access; the rest hold the pointer in a form the tracker does not see.
*Followed up 2026-09-17 (FABLE, `UQ-106`): a second tracker that enforces slot provenance, follows forward jumps and
hops one call reaches **128 of the 129** and 232 sites — [`members/action-row-reader-hops.tsv`](members/action-row-reader-hops.tsv).*

### 2.2 The field map

Widths are the access widths; "shipped" is the tally over the 543 `us` rows. **Meaning** is stated
only where a reader fixes it; **shape** is what the data alone shows.

| offset | width | shipped (`us`) | reader(s) | meaning / shape |
|---|---|---|---|---|
| `+0x00` | u16 | `4000` on 327 rows, else `4001`–`4321`, and row *n* carries `4000 + n + 1` **for rows 0–80 only** (Cure `4001`, Blindna `4002` …); **row 81 has no help text and the rule shifts to `4000 + n` from row 82 on** — 216 rows carry a help id and 81 satisfy the `+ 1` form (§9, 2026-09-13) | — (the low-pool resolver `002F9860` maps `4000 + k` to group 4, [the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) §5.1) | **the help-text string id**, `4000` = none — by the id scheme, not by a traced read |
| `+0x02`, `+0x03` | u8, u8 | 0 on 537 rows; `1` / `20` / `15` on six | by argument and a computed index, `BattleAction_GetAuthoredRangeBandComponent` (`00320DE9`, `row + component + 2`) — *read 2026-09-19, FABLE* | **the near and middle range-band components, in tenths** - used when `+0x0C` bit 26 is clear ([how close a unit must stand to act](../how-close-a-unit-must-stand-to-act.md)) |
| `+0x04` | u8 | 0 × 425, `100` × 26, `5` × 17, `50` × 16, `40` × 12 … | `00388B50` (`00388BE6`) — *hop census 2026-09-17* | ~~a percent-shaped byte; reader not found~~ **the action's knockback chance base** - *read 2026-09-30 (FABLE)*: `00388B50` stores `max(0, +0x04 + roll % first[+0x1C2] − roll % second[+0x1C2])` into the knockback chance `02AEDFD8` (`00388B74`–`00388BFB`, two draws of `RNG_MT19937_NextU32_Thunk`), the same shape as `BattleFormula_ComputeKnockbackChance`, which takes its base from the weapon row instead ([the formula scratch block](../../08-Combat-Formula/Scratch-Block/the-formula-scratch-block.md), `02AEDFD8`) |
| `+0x05` | u8 | `100` × 212, 0 × 130, `30` × 56, `20` × 50, `255` × 39 | `00384F40` (`0038503B`) — *hop census 2026-09-17*; by argument, `BattleAction_GetPrimaryRangeScalar` (`00309380`) — *read 2026-09-19, FABLE* | **the action's reach, in tenths** (`100` = 10.0) - used when `+0x0C` bit 26 is clear; with the bit set the reach is the weapon's ([how close a unit must stand to act](../how-close-a-unit-must-stand-to-act.md)). ~~*What `00384F40` does with it was not read.*~~ *Answered on [the result record](../Result-Record/the-result-record-field-map.md) (`+0x010`), re-read 2026-09-30 (FABLE): `00384F40` is the Reflect retarget picker. Its only caller is `BattleFormula_ApplyPreResolutionTargetGates` (`00390E39`), which reaches it when `+0x0C` bit 16 is set, writes result kind 8 (`00390E35`) and stores the unit it returns at result `+0x10` (`00390E42`). The picker returns the nearest eligible unit whose surface distance is inside `+0x05` / 10 (`0038503B`–`00385046`, `divss` by 10.0).* |
| `+0x06` | u8 | 0 × 296, `10` × 98, `8` × 63, `6` × 46, `100` × 13 (`8` on Aero, Fira, Thundara, Blizzara, Bio …) | `0030C0E0` (`0030C1C6`, tested against 0), `Battle_BuildActionTargetSet` (`0030D20E`); by argument, `0031A990` (`0031A995`, `0031A9B2`, converted to float) — *hop census 2026-09-17* | ~~a cost-shaped byte; reader not found~~ **the area radius** - *read 2026-09-19 (FABLE)*: 0 = the primary target only; compared squared against ground-plane distance from the primary target, or from the actor when `+0x0C` bit 21 is set; [how an action gathers its targets](../how-an-action-gathers-its-targets.md) |
| `+0x07` | u8 | 0 × 490, `180` × 33, `60` × 7, `75` × 3 | by argument, `0031A990` (`0031A9C2`, converted to float beside `+0x06`) — *hop census 2026-09-17* | ~~shape only~~ **the cone's half-angle in degrees (`+0x0C` bit 24) or the line's half-width (bit 25)** - *read 2026-09-19 (FABLE)*; 180 makes the cone a circle round the actor; [how an action gathers its targets](../how-an-action-gathers-its-targets.md) |
| `+0x08` | u8 | 0–108, `65` × 85, 0 × 73 | `BattleFormula_ResolveTargetResult` (`0038617E`) | **the recipe index** into the 109 lists at `01EF96C0` ([the count-clock page](../../08-Combat-Formula/Recipe-System/the-count-clock-and-bank-recipes.md)); 0 = "take the weapon's recipe" ([attack-defense](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §5.1) |
| `+0x09` | u8 | 0 × 212, `3` × 149, `23` × 81 (the white magicks Cure … Dispelga), `1` × 32, `2` × 24 | `BattleAction_ComputeChargeLimitTicks` (`002F8410`) | **the charge-time class** the charge computation starts from |
| `+0x0A` | u16 | 0 × 371, `2` × 23, `3` × 14, `8` × 12, `1` × 11 … ≤ 768 | the query-record filler, class 20 ([the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.4: copied to the record's `+0x28` when non-zero) | ~~a small count the menus read; what it counts is not fixed~~ **the MP cost** - *reconciled 2026-09-30 (FABLE)*. Every reader takes the low **byte**: `BattleAction_ComputeModifiedResourceCostAmount` at `002F962B` (the authored cost the modifiers start from, [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) §2, "the spend side", CS-5) and the class-20 query filler at `0031DBD2`, which is the number the menu shows. The byte is `0` × 397 and at most `72`; Cure is `8`. A kind-5 / 6 action spends `max MP × +0x0A` Mist charges instead (same page). The high byte `+0x0B` is a separate field: it is non-zero (`1`–`3`) only on the 26 rows 182–207, and no reader of it is named (GR-5). The `≤ 768` ceiling above is the word's: `768` is `+0x0B = 3` over `+0x0A = 0` |
| `+0x0C` | u32 | low byte `140` × 243, `136` × 81, `76` × 69, 0 × 44; the word `17036` × 99, `9612` × 78 | `BattleFormula_ResolveTargetResult` (bit 11, `00386079`), `00320E10`, `BattleFormula_ApplyPreResolutionTargetGates` (`00390AB0`) | **the action flags word**; bit 11 clears the result's byte `+0` bit 5 ([the result record](../Result-Record/the-result-record-field-map.md)); the other bits are read by the two gates, not yet decoded *(2026-09-30, SWE2-STRUCT for OPUS: answered - UQ-107, ANSWERED 2026-09-27 (§7): every bit 12-31 has its reader and meaning or is shown reader-less, [record](../../_index/candidates/uq107-action-flag-bits/README.md))* |
| `+0x10` | u8 | 0 × 242, `100` × 36, `90` × 15, `50` × 14 … ≤ 253 | thirteen preparation slots (`00389DD0`, `00389F80`, `0038A820`, `0038A9D0`, `0038ABC0`, `0038CC10`, `0038CD60`, `0038CE40`, `0038CF20`, `0038D000` …) | **the action power** — the attack term of the magick and technick recipes, with the `[P, P × 1.125)` variance ([attack-defense](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §5.1) |
| `+0x11` | u8 | 0 × 497, `255` × 11, `60` / `100` × 3 | `00388C10`, `0038F1B0`, `003900C0`; slot 74 (`BattleFormula_PrepareActionPowerPair`) | **the second power byte** (the pair's multiplier; recipe 101's `+0x10 × 100 + +0x11`) |
| `+0x12` | u8 | `100` × 312, 0 × 157, `50` × 14, `60` × 11 | `00388FE0` (`BattleFormula_LoadHitAvoidGuardThresholds`, `00389089`) | **the hit threshold** written to `02AEDFE0` before the avoid / guard rolls |
| `+0x13` | u8 | 0 × 447, `1` × 19, `16` / `32` / `128` × 13 | `0038B010`, `0038B220` (the weather / terrain stage, bit 0), `BattleFormula_ApplyActionElementAffinity` (`0038B6A0`), `0038C940`, `0038D7E0`; the query record's `+0x30` | **an element / affinity flags byte** — bit 0 gates the weather / terrain scaling ([weather-terrain](../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)); bits 4, 5, 7 present in the data, their readers among the five |
| `+0x14` | u8 | 0 × 494; `100` on Bio, Scourge, Meteorite, Holy Mote, Infuse, Charm; `35` on the *-ja* spells; `50` on Darkja | `0038F970` (the non-weapon percent-gate loader, `0038F9B0`) | **the on-hit status chance** — loaded into the percent gate `02AEDFE8` that slots 176 / 182 roll against ([attack-defense](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) AJ-11) |
| `+0x15`–`+0x17` | — | 0 on all 543 | — | padding |
| `+0x18` | u32 | 0 × **387** (~~424~~ — that was the **u16** count at this offset; corrected 2026-09-13, §9); single bits and small masks (`1024` × 12, `1` × 10 …) | `BattleAction_ComputeAuthoredStatusMask` (`003872D0`), `00384C30`, `003875D0` | **the authored status mask** the action inflicts, one bit per status id |
| `+0x1C` | u8 | `3` × 186, `1` × 147, 0 × 84, `2` × 34, `4` × 31 … ≤ 9 | `BattleUnit_HasCurrentFocusEngagementEvidence` (`0030BBCD`, read and decremented — an index); by argument, `BattleAction_SelectPhasePresentationEvent` (`0030A37F`) — *hop census 2026-09-17* | ~~a small enum; reader not found~~ **the action category 0–9** - *reconciled 2026-09-30 (FABLE)*: `BattleAction_SelectPhasePresentationEvent` (`0030A37F`) indexes its three-event table with it (0 attack, 1 magick, 2 item, 3 / 6 ability, 5 steal; [BT-4 record](../../_index/candidates/bt4-event-motion-slots/README.md), credited in the [UQ-80 record](../../_index/candidates/uq80-table-field-coverage/README.md)) |
| `+0x1D` | u8 | 0 × 360, then 10 / 16 / 12 / 28 … | by argument, `BattleEnmity_ApplyActionParameters` (`00321716`) — *hop census 2026-09-17* | ~~shape only~~ **the direct enmity parameter** - *reconciled 2026-09-30 (FABLE)*: when the caster is a party-table unit, the value goes to the enmity write for the target toward the caster (`00321716`–`0032172E`); [gambit evaluation and enmity](../../09-Combat-AI-And-Gambits/gambit-evaluation-and-enmity.md) §8e, Z-5 |
| `+0x1E` | u8 | `7` × 235, `1` × 81, `255` × 56 (the `NOT USED` / *Reserve* rows), `3` × 51, `9` × 26 | `BattleAction_GetSubtype3Field22OrFFFF` (`003093D0`), `004698C0`, `BattleFormula_DispatchPostResultEvents` (`00469EC0`) | **the id-class byte** (called "the category" until 2026-09-30; it is not `+0x1C`'s action category 0-9 *(qualified 2026-09-30, FABLE, on SWE2-AUDIT-SEM's [review](../../_index/candidates/auditsem-review-dd-gameplay-0930/REVIEW.md) N5; record [`dd-gameplay-corrections-fable-0930`](../../_index/candidates/dd-gameplay-corrections-fable-0930/README.md))*), and it selects what `+0x22` holds — `1`→magick id (81 rows), `2`→technick id (24), `3`→**item** id (51), `5`/`6`→nibble-`C` id (13/18), every other value → `0xFFFF`, with **no exception in 543 rows** except `255`, where 13 of 56 still carry an item id ([item use](../../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md) §9, 2026-09-13). Also **the message kind** — `2` and `7` select per-action message ids ([post-result events](../Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)) |
| `+0x1F`–`+0x21` | u8 × 3 | small values (`+0x21`: `6` × 174, 0 × 129, `8` × 64 …) | by argument, `BattleEnmity_ApplyActionParameters` (`+0x1F` at `00321733`, `+0x20` at `00321744`); `+0x21` has no reader found — *hop census 2026-09-17* | ~~shape only~~ *reconciled 2026-09-30 (FABLE)*: **`+0x1F` the enmity propagation parameter** (to the foes that already hold enmity, `00321733`) and **`+0x20` the redistribution parameter**, applied negated to the other combatants (`00321744`–`0032174B`), Z-5 as for `+0x1D`; **`+0x21` is authored and unread** (AY-2, ANSWERED 2026-09-26: two instruments find no reader) |
| `+0x22` | u16 | `0xFFFF` × 343; the other **200** rows carry **four** encoded-id kinds, not one — nibble `3` × 81 (rows 0–80, `0x3000 + row` exactly), nibble `0` × 64, nibble `4` × 24, nibble `0xC` × 31, each a **contiguous row block** numbering from its own base (§9, 2026-09-13) | `BattleAction_GetSubtype3Field22OrFFFF` (`003093D0`); the query record's `+0x2C` | **an id whose space `+0x1E` names** — the class-3 magick / technick id the action is sold and learned as *when `+0x1E` is 1 or 2*; an **item** id when `+0x1E` is `3` (§9 of [item use](../../12-Items-Equipment-Shops-License/using-an-item-is-an-action-that-costs-an-item.md), 2026-09-13) |
| `+0x24` | u16 | 351 distinct; `0xFFFF` × 68, `210` × 35 | *(also, hop census 2026-09-17: `0030AC50` at `0030AD10`, `0031ADB0` ×3, `BattleUnit_HandleActionTimelineEvent` ×3, `003257D0` ×3)* the trap applier in `BattleUnit_RunPeriodicCombatMaintenance` (`00311052`–`0031106B`: bit 15 stripped, handed to `002EACD0(unitId, 1, &unit+8, id)`) | **an attached-effect id** (bit 15 a flag): the trap rows carry `0x8073`–`0x8076` → effects 115–118 — one reader found 2026-09-12 (FABLE); ~~whether the 351 values on other rows reach the same call is not shown~~ *narrowed 2026-09-30 (FABLE)*: the selector `0030AC50` returns `+0x24 & 0x7FFF` only when bit 15 is set and `+0x0C` bit 30 is clear (`0030AD10`–`0030AD2F`); for `0xFFFF` it falls back to the weapon row's `+0x2C` word (`0030AD48`–`0030AD5A`); and it returns −1 for anything else. Over the 543 rows, bit 15 is set on **39** words, all with bit 30 clear: rows 111–123 (`0x808B`), the sixteen trap rows 246–261, and rows 427–435 and 440. The word is `0xFFFF` on 68 rows, and **436** carry bit 15 clear. `BattleUnit_HandleActionTimelineEvent` and `003257D0` send every other non-`0xFFFF` word (bit 15 clear, or `+0x0C` bit 30 set) down a branch this page has not read (`00325476` and `00325968`, each a `jne` on `0xFFFF`). What those 436 values select is open (GR-6) *(answered 2026-09-30, OPUS `addead717`, [`gr6-action-row-24-0930`](../../_index/candidates/gr6-action-row-24-0930/README.md): the low 15 bits are the action's own effect id, served by `0030A190` / `0030CA80` to the effect request and budget and instantiated per target of a periodic action by `00310DB0`; on the 62 summon-class rows, `+0x0C` bit 30 set, the word is the special-sequence load id. `00325476` / `00325968` lead only to the two readers' exits)* |
| `+0x26` | u8 | 0 × 530; `27`–`39` on the thirteen summon rows (Belias `27` … Zodiark `39`) | `BattleAction_UpdateSpecialPresentationSequence` (`00306760`, the summon's mode-1 block) | **the Esper's party-table row** ([the mode ladder](../../00-Engine-Core-Runtime/Battle-Runtime-Mode/battle-runtime-mode-ladder.md) §2c) |
| `+0x28` | u8 | 0 × 517; `120`–`153` on ~~the 26 Esper attacks~~ the 26 Quickening-family rows *(corrected 2026-09-27, FABLE, Claude Opus 5.5: ids `0xD0`-`0xE1` are the 18 Quickenings and `0xE2`-`0xE5`, `0xE7`, `0xEA`, `0xED`, `0xF1` the 8 Concurrences, Inferno to Black Hole; none is an Esper attack; [UQ-80 record](../../_index/candidates/uq80-table-field-coverage/README.md))* (Red Spiral `120`, White Whorl `121` … ) | — | ~~a per-Esper-attack index~~ a per-row index on the 26 Quickening-family rows (*corrected 2026-09-30, FABLE, to agree with the correction in the shipped column*); reader not found - the two-hop census and the UQ-80 instrument both list none (GR-4) *(answered 2026-09-30, OPUS `8259918bb`, [`gr4-gr5-action-row-readers-0930`](../../_index/candidates/gr4-gr5-action-row-readers-0930/README.md): one reader, `BattleAction_GetPresentationParameter` `0030A190` (word read `0030A209`), which returns this word as the Quickening / Concurrence cinematic effect id for ids `0xD0`-`0xF1` while the special-sequence state is 5 or 6)* |
| `+0x2C` | u8 | 0 × 259, `32` × 166, `1` × 21, `40` × 21, `49` × 17 | `BattleAction_IsTargetEligibleForCurrentAction` (`002FFA60`), `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`003008A0`), `00305110`, `00305230`, `00305430`, `BattleUnit_HasCurrentFocusEngagementEvidence` (`0030BB30`), `0031C5D0` (`& 7` into the magick query record), `BattleFormula_ApplyTargetStatusActionPostModifiers` (`00390F20`) | **bits 0–2 the element**; ~~bit 5 (`32`, 166 rows) a second flag the eligibility readers test~~ *corrected 2026-09-17 (FABLE): the eligibility readers test bits 6 and 7, which no shipped row sets; bit 5 has no immediate test found; `00390F20` tests bit 10 and `0030BB30` returns bit 14 (UQ-107)* |
| `+0x2D` | u8 | `4` × 170, 0 × 146, `32` × 47, `64` × 28, `72` × 22; **bit 5 set on 98 rows** across eight values (`32, 48, 96, 100, 104, 105, 160, 176`) | `BattleStats_HasRequiredLicenseForAction` (`00323EC0`, at `00323F52`) | a flags byte. ~~reader not found~~ — **bit 5 is "this action needs no License"** (2026-09-13): the check tests it as `0x2000` of the **word** at `+0x2C`, which is why a byte-wise field map and a word-wise reader missed each other ([the License check](../../12-Items-Equipment-Shops-License/license-check-what-the-board-actually-tests.md) §3, §9) |
| `+0x2E` | u16 | 0 × 342; `10000 + k` on 201 rows | the query record's `+0x10` (`desc(row+0x2E)`) | **the description string id** (low pool, group 10) |
| `+0x30` | u16 | 0 × 358; **`500`**–`4008` (~~`600`~~ — one row holds `500`; corrected 2026-09-13) | `BattleAction_SelectPhasePresentationEvent` (`0030A370`, a dword read at `0030A457` / `0030A46A`) *(found 2026-09-27, FABLE, Claude Opus 5.5)* | ~~an id-shaped word; reader not found~~ **the action's own presentation event in phases 9-11** - returned whenever non-zero, and for ids `0xD0`-`0xE1` in world state 5 or 6; a kind-0 event above the priority table, naming the per-character motion pack `c<char>_<set>_<value>.ca` (`c1004` ships `_3000`-`_3002`), [record](../../_index/candidates/bt4-event-motion-slots/README.md) |
| `+0x34` | u16 | `0`–`542`, one per row, ~~equal to the row index~~ equal to the row index **except rows 128–142**, which hold 136, 137, 128, 129, 130, 138, 139, 140, 141, 135, 142, 131, 132, 133, 134 *(2026-09-12)* | `00305F10`, `0031C5D0`; the query record's `+0x20 ← (row+0x34 >> 8) & 3`; bank 0 names | **the name word** — the readers take **bank = word >> 11, entry = word & 0x7FF** from the text bank table `02EBF170` (`00305F90`–`00305FD4`, `0031DB44`–`0031DB89`), bank 0 of the battle text ([the battle text banks](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md)) ~~at the row's own index~~ — at the row's own index for 528 rows; **rows 128–142 take the name of the entry their word names**, so a reader that names row *r* with entry *r* mislabels fifteen actions |
| `+0x36` | u8 | 0 × 312, `16` × 140, `17` × 51, `18` × 22, `48` × 11 | `BattleAction_CheckTargetEligibility` (`00308446`, a **u16** read with bit 5 tested), `BattleAction_ComputeAuthoredStatusMask` (`00387331`), `003875D0` (`00387629`), `BattleFormula_ApplyPreResolutionTargetGates` (`00390D55`, u16) — *hop census 2026-09-17* | shape only - *except, read 2026-09-19 (FABLE)*: **bit 3 = an area hits everyone, bit 2 = it hits the side opposite the primary target, neither = the primary target's side** (`0030D36C`); [how an action gathers its targets](../how-an-action-gathers-its-targets.md) |
| `+0x38` | u16 | `0xFFFF` × 386; `{high, low}` pairs on 157 rows — Cure `0x0001`, Cura `0x0101`, Curaga `0x0201`, Curaja `0x0301`, Blindna `0x0901`, Regen `0x0502` | — | two bytes: ~~the low one `1` or `2`, the high one a per-spell index; reader not found~~ *corrected 2026-09-30 (FABLE), to agree with §7's 2026-09-18 narrowing*: **the action's place in the player's command list**. The low byte is the page (0–10) and the high byte the row on it (0–16); Cure and Regen above are pages 1 and 2. The reader is the action-table binder `00237FC0`: it reads both bytes (`00238033`, `00238043`) and files each listed action into a page × row grid ([UQ-80 record](../../_index/candidates/uq80-table-field-coverage/README.md), "Corrected in review") |
| `+0x3A` | u8 | `255` × 475; `16` on Cure … Curaja, the Potions and Float Mote, `14` on Dispel / Dispelga, `15` on Balance / Reflectga Mote, `12` on Elixir / Megalixir | `00312170` (`003121F5`, read and decremented — an index) — *hop census 2026-09-17* | a remedy category on 68 rows (~~12–16~~ **10–16**: `15` × 49, `16` × 8, `13` × 4, `14` × 3, `12` × 2, `10` and `11` × 1 - *corrected 2026-09-30, FABLE, from the tally*); ~~reader not found~~ *read 2026-09-30 (FABLE)*: **a bit number**. After the relationship test (`0030AB40` above 1), `00312170` sets bit `+0x3A` of a mask when the byte is 1–254 (`003121F5`–`00312203`). It ORs in the element byte `+0x13` and `+0x0C` bits 13 and 14 as bits 8 and 9, then ORs the mask into operand-store kind 10 of the second unit it is handed (`0031224D`–`0031225E`). Who reads that kind-10 mask, and so what the category means to its reader, is open (GR-7) *(answered 2026-09-30, OPUS `f0c46d818`, [`gr7-kind10-reader-0930`](../../_index/candidates/gr7-kind10-reader-0930/README.md): kind 10 is the unit's `+0xB90` mask, read only by the enemy AI order selectors through `AiTargetSelector_ResolveOperandValue`; `+0x3A` is an AI reaction class)* |
| `+0x3B` | — | 0 on all 543 | — | padding |

> **Rows 246–261 are the trap actions, 2026-09-12 (FABLE).** Named by no bank-0 string, they are the
> only ids a shipped trap record carries ([the trap record](../../14-Story-Event-Quest-Hunt/persistent-flag-banks.md)):
> recipe 94 (slot 106, HP damage `(1 + roll % +0x10) × (1 + roll % level)`, power 30 / 90 / 180 on
> 246–248), 95 (slot 107, the same into MP loss, power 20 / 100 on 249 / 257), 96 (slot 108, HP
> gain, power 80 on 260), 97 (slot 109, MP gain, power 50 on 261), 99 (slot 163, gil loss, power 99
> on 259) and 98 (slot 181, the `+0x18` status mask: 250 Sap, 251 Confuse + Berserk, 252 Petrify,
> 253 Blind, 254 Silence, 255 Reverse + Disable, 256 Disease, 258 Oil). Their `+0x24` is
> `0x8073`–`0x8076`, the attached effect the applier plays. Row 245, "Chain Bonus", sits just before them.

### 2.3 What the map says about the table

- *Updated 2026-09-30 (FABLE): the count below is the 2026-09-12 state. With the hop census (UQ-106), the UQ-80 record and this re-read, every non-padding field in §2.2 has a traced reader except `+0x0B` (GR-5), `+0x21` (unread: AY-2) and `+0x28` (GR-4).* *(2026-09-30, SWE2-DATA: GR-4 and GR-5 are answered - `+0x28` is read by `0030A190`, and `+0x0B` has no reader in the executable; [`gr4-gr5-action-row-readers-0930`](../../_index/candidates/gr4-gr5-action-row-readers-0930/README.md).)*
- **Fourteen of the thirty-two non-zero fields have a traced reader** — the recipe, charge class,
  flags, power pair, hit threshold, affinity byte, status chance, status mask, message kind, linked
  menu id, Esper row, element byte, description and name. They are the fields the formula, the
  message and the menu systems need; the rest are read by systems whose row access the tracker
  does not follow (the pointer is passed on) or by nobody.
- **The strings are three ids in three pools**: the name at `+0x34` (bank 0 ~~by row index~~ by the word, which equals the row index except on rows 128–142), the
  description at `+0x2E` (group 10) and the help text at `+0x00` (group 4).
- **Summons and ~~Esper attacks~~ Quickenings are ordinary rows** with two private bytes: `+0x26` names the Esper's
  party row on the thirteen summons and `+0x28` carries `120`–`153` on the twenty-six ~~attacks~~ Quickening-family
  rows *(corrected 2026-09-30, FABLE: the 18 Quickenings and 8 Concurrences, as the §2.2 correction of 2026-09-27
  already says)*.
- **The 56 rows whose `+0x1E` is `255` are the `NOT USED` and *Reserve* rows** — the table's holes
  keep a sentinel message kind.

## 3. Key addresses

| Address | Name | Verified |
|---|---|---|
| `02EBF138` | the registry slot: header `{+0x04 count 543, +0x08 stride 60, +0x0C rows}` | ✅ |
| `0020E600` | `ImageAddress_ResolveRuntimePointer` — resolves the `+0x0C` reference | ✅ |
| `02AEDFD4` | the parked action id the recipes index with | ✅ |
| `0038617E` | the resolver's read of `+0x08` (the recipe) | ✅ |
| `002F8410` | `BattleAction_ComputeChargeLimitTicks` — reads `+0x09` | ✅ |
| `00389040` | `BattleFormula_LoadHitAvoidGuardThresholds` — reads `+0x12` | ✅ |
| `003872D0` | `BattleAction_ComputeAuthoredStatusMask` — reads `+0x18` | ✅ |
| `0038F970` | the non-weapon percent-gate loader — reads `+0x14` | ✅ |
| `003093D0` | `BattleAction_GetSubtype3Field22OrFFFF` — reads `+0x1E`, `+0x22` | ✅ |

## 4. Data structures and formulas

```
ActionDefinitionRow (60 B, 543 rows, us battle_pack.bin directory +0x3C; action_data.bin per language)
  +0x00 u16  helpTextId (4000 = none)      +0x1E u8   messageKind (255 = unused row)
  +0x08 u8   recipe (0 = weapon's)         +0x22 u16  linkedMenuId (0xFFFF = none)
  +0x09 u8   chargeClass                   +0x26 u8   esperPartyRow (summons)
  +0x0A u8   mpCost                        +0x28 u8   quickeningIndex (120..153, reader not found)
  +0x0B u8   b0B (1..3 on rows 182-207)
  +0x0C u32  flags (bit 11 ...)            +0x2C u8   element (bits 0-2); bit 5 read by nothing (UQ-107)
  +0x10 u8   power                         +0x2E u16  descriptionId (10000 + k, 0 = none)
  +0x11 u8   power2                        +0x34 u16  nameId (= row index EXCEPT rows 128-142; see the field map)
  +0x12 u8   hitThreshold
  +0x13 u8   affinityFlags (bit 0 weather / terrain gate)
  +0x14 u8   statusChance (percent)
  +0x18 u32  statusMask
  no reader found (2026-09-30): +0x0B, +0x21 (AY-2), +0x28; every other field's reader is in the section 2.2 table
```

*(2026-09-30, SWE2-DATA: the block's `+0x28` "reader not found" is answered by GR-4 - `0030A190` reads it as the cinematic effect id; `+0x0B` stays unread, GR-5; [`gr4-gr5-action-row-readers-0930`](../../_index/candidates/gr4-gr5-action-row-readers-0930/README.md).)*

## 5. Call chain

```
action id parked at 02AEDFD4 (the resolver)
  -> every reader: [02EBF138] -> +0x0C -> 0020E600 -> base ; + 60 x id -> row
     -> formula: +0x08 recipe, +0x10/+0x11 power, +0x12 hit, +0x13 affinity, +0x14 chance, +0x18 mask, +0x2C element
     -> messages: +0x1E kind ; menus: +0x00 / +0x2E / +0x34 strings, +0x22 menu id, +0x0A MP cost, +0x38 list place
     -> enmity: +0x1D / +0x1F / +0x20 ; Reflect retarget: +0x05 reach (00384F40, when +0x0C bit 16)
     -> summons: +0x26 Esper row
```

## 6. Modding notes

- **Power lives at `+0x10`/`+0x11`, hit rate at `+0x12`, status chance at `+0x14`, status at
  `+0x18`, element at `+0x2C` bits 0–2** — the five numbers a balance edit touches, all bytes.
- **Changing `+0x08` re-routes the whole formula**: it is the recipe index, and 0 hands the choice to
  the equipped weapon.
- **The MP cost is the byte `+0x0A`**, before the augment modifiers
  ([where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) §2). The three enmity numbers are
  `+0x1D` / `+0x1F` / `+0x20` (added 2026-09-30, FABLE).
- **The name is not in the row** — `+0x34` is ~~only the row's own index~~ an index into bank 0 (its own row index
  on 528 rows); renaming means editing the text bank, and **giving a row another row's name is a one-word edit**,
  which is what rows 128–142 ship with.
- **XIIOnline:** the table is bound once at boot from the STATIC blob and never rebound
  ([the registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) AG-11), so
  two clients with the same `battle_pack.bin` read identical rows; a mismatched pack diverges on
  every field above.

## 7. What is not known

- [x] **UQ-106.** *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **AY-2**)* The readers of the eighteen unread bytes (`+0x02`–`+0x07`, `+0x1C`, `+0x1D`, `+0x1F`–`+0x21`,
      `+0x24`, `+0x2D`, `+0x30`, `+0x36`, `+0x38`, `+0x3A`) — the tracker follows one idiom only;
      a hop census that follows the row pointer through call arguments would find the rest.
      ***NARROWED 2026-09-17 (FABLE): the hop census the row asked for was built, and it finds readers for eleven of the eighteen.** `members/action_row_reader_hops.py` re-implements the slot idiom with its provenance enforced (the resolve's argument must come from `[02EBF138]+0xC` - several readers resolve two or three registry slots in one body, and the first version of the census attributed other tables' rows to this one until that check was added), follows the row through register copies, stack slots, `lea`-derived pointers and FORWARD JUMPS, and hops one call into any callee that receives it. Controls: the page's `+0x08` at `0038617E` and `+0x12` at `00389089` both reappear. What the page's tracker missed was mostly one shape - a read just past a branch join, where the other arm supplies the row from a saved register (`add ecx, eax / jmp L / … / L: movzx eax, [rcx+4]`). New readers, all hand-checked in context: `+0x04` (`00388B50`), `+0x05` (`00384F40`), `+0x06` (`0030C0E0`, `Battle_BuildActionTargetSet`, and by argument `0031A990`), `+0x07` (by argument `0031A990`), `+0x1C` (`BattleUnit_HasCurrentFocusEngagementEvidence`, by argument `BattleAction_SelectPhasePresentationEvent`), `+0x1D`/`+0x1F`/`+0x20` (by argument `BattleEnmity_ApplyActionParameters`), `+0x24` (four more beside the trap applier), `+0x36` (four, two of them u16 reads testing bit 5), `+0x3A` (`00312170`). **Still no reader at hop 0 or 1: `+0x02`, `+0x03`, `+0x21`, `+0x30`, `+0x38`** (`+0x2D`'s reader the page already had by another route). The bound: one hop, from the 129 functions that reference the slot; a row handed on twice, or reached from a function that never touches the slot, is not seen. 232 sites in `members/action-row-reader-hops.tsv`.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - AY-2, ANSWERED 2026-09-26, and the §2.2 table: `+0x02` / `+0x03` are read by `00320D70` (`00320DE9`), `+0x30` by `BattleAction_SelectPhasePresentationEvent` (`0030A457`), `+0x38` by the action-table binder `00237FC0` (`00238033`); `+0x21` is read by nothing.)*
      ***Second hop 2026-09-17 (FABLE), negative.** The census was re-run with its hop gate widened from one call to two (a visited set on callee, bound registers and depth keeps it finite): from the same 128 rooted functions it hops into 22 callee sites and 13 distinct callees against 21 and 12 at one hop, so exactly one function receives the row at the second hop, and it reads none of `+0x02`, `+0x03`, `+0x21`, `+0x30` or `+0x38`. The bound is now two hops from the slot's referencing functions; a reader of those five bytes, if one exists, takes the row from a place that never resolves the slot or hands it on three times.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - AY-2, as in the note above: four of the five have readers the census could not reach, and `+0x21` has none.)*
      ***NARROWED 2026-09-18 (FABLE), DATA: two of the five reader-less bytes are named by their values, and they sit on disjoint row sets.** *`+0x38` is the action's position in the player's list.* Over the 543 rows the word is `0xFFFF` on 386 and a `{row, page}` pair on 157: the low byte is a page 0..10 and the high byte a row 0..16, seventeen rows to a page, and the pages read in the game's own order: page 0 is Attack alone; pages 1..5 hold the 81 magicks (Cure, Cura, Curaga, Curaja, Renew, Raise, Arise, Esuna ... on page 1; Protectga, Shell, Shellga, Bravery, Faith, Regen ... page 2; Aero ... Sleepga page 3; Hastega ... Reflect page 4; Gravity ... Ardor, thirteen, page 5); pages 6..8 the 51 battle items (Potion, Hi-Potion, X-Potion, Ether ... Meteorite); pages 9..10 the 24 technicks (Steal, Libra, Poach, First Aid ... Shear). So it is the menu's sort key, and its reader is a menu list builder that reaches the row outside the combat slot idiom the census followed. *`+0x30` is a shared performance id on a hundreds grid, on exactly the other 185 rows* (no row carries both): 500..508 the nine basic enemy attacks (Ram, Gnaw, Lunge, Rake, Slap, Kick, Rush ...), 600..613 fourteen ids shared by 57 enemy casts (Darkness, Ice Break, Water Spout, Shining Ray, Tremor ... 57 rows on 14 ids, so it names a shared performance, not the row), 700..743 the 47 monster technicks (Jump, Mach Punch, Goblin Attack ...), 900..944 the 45 boss and Esper moves (Breath of Life, Spawn, Ground Shaker ...), 3000..3017 the 18 Quickenings (Red Spiral, White Whorl, Pyroclasm ...) and 4000..4008 the 9 Esper finishers (Quakeja, Firaja, Blizzaja ...). It is not a sound-bank id (none of the 139 distinct values is a `se%06d` bank) and not a text key (44 coincidences with `help_action`'s hundreds grid, none with the others), so it addresses the presentation of a non-player action, and its reader is in that system. Still without a reader or a reading: `+0x02`..`+0x03` (six rows) and `+0x21`. DATA from `battle_pack.bin` joined to bank 0.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - `+0x02` / `+0x03` are read by `00320D70` (2026-09-19, §2.2) and `+0x21` by nothing (AY-2, ANSWERED 2026-09-26); the two readers this paragraph sends elsewhere are `00237FC0` for `+0x38` and `0030A370` for `+0x30` (§2.2).)*
      *Further, 2026-09-18 (FABLE): one more hop finds nothing.* The census was re-run with the call-following raised to two levels (a scratch copy of `members/action_row_reader_hops.py` with `hop <= 1`, the row pointer bound into the callee's argument register and followed the same way). It reaches 22 hops into 13 callees, exactly one of them at depth 2 (`00254A10` → `00229E40`), and the readers it finds for `+0x02`, `+0x03` and `+0x21` are still none. So along every static call chain of depth two or less that carries the row pointer, those bytes are not read; if they are consumed at all it is through a copy of the row (a memcpy into another record) or a pointer stored in a field, neither of which a register-and-stack tracker can follow. Static: the depth-2 run. *(2026-09-30, SWE2-STRUCT for OPUS: answered - AY-2, ANSWERED 2026-09-26: `+0x02` / `+0x03` do have a reader (`00320D70`, §2.2), and a second instrument over all 129 functions that reference the slot finds no `+0x21` read, so `+0x21` is authored and unread.)*
- [x] **UQ-107 ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5)** - every `+0x0C` bit 12-31 has its reader and meaning, or
      is shown reader-less:
      - bits 15, 18 and 20 are authored and never read;
      - bits 22 and 23 are unused;
      - `+0x2C` bit 5 is read by nothing.
      [Record](../../_index/candidates/uq107-action-flag-bits/README.md). *Earlier state, kept:* The bits of `+0x0C` beyond bit 11, and of `+0x13` beyond bit 0, and `+0x2C` bit 5 — their
      readers are named above; the bit meanings are not read. *(2026-09-30, SWE2-STRUCT for OPUS: answered - the ANSWERED line at the head of this item, 2026-09-27.)*
      ***NARROWED 2026-09-17 (FABLE): `+0x13` closes by cross-reference, two of `+0x2C`'s bits are placed and two are dead in the data; `+0x0C`'s bits stay open.** *`+0x13`* is the action's element mask, one bit per element: the affinity stage `0038B6A0` ANDs the whole byte against the target's four behaviour bytes `+0x40`..`+0x43` and the source's `+0x44` (`0038B709`..`0038B90D`), which is [the affinity page](../../08-Combat-Formula/elemental-affinity-and-the-five-bytes.md)'s five-byte AND, and the weather stage `0038B220` tests bits 0..5 one by one against the environment classes (`0038B295`..`0038B65E`), [the weather page](../../08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md)'s per-element boosts; bits beyond 0 are therefore the other elements, not further flags. *`+0x2C`*: the four eligibility readers `002FFA60`, `00305110`, `00305230` and `00305430` test **bits 6 and 7** (`0x40`, `0x80`) of the row they resolve from `[02EBF138]` (`0030543F`..`0030549E`), not bit 5, and the shipped table never sets either (values 0, 1, 32, 40, 49), so those arms are dead in this data; the post-modifier `BattleFormula_ApplyTargetStatusActionPostModifiers` `00390F20` tests the word with `0x400` (`0039110D`..`00391116`), that is `+0x2D` bit 2, the value 4 on 170 rows; and `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30` returns bit 14 of the word (`0030BC0C`), `+0x2D` bit 6. Bit 5 of `+0x2C` (`0x20`, 166 rows) has no immediate test in any function that references the action table; the `& 7` readers take only the element. *`+0x0C`*: the immediates tested on a `+0xC` word inside functions that reference the action table are `0x1`..`0x8`, `0x60`, `0x800`, `0x2000`, `0x4000`, `0x10000`, `0x20000`, `0x80000`, `0x200000`, `0x3000000`, `0x4000000`, `0x10000000`, `0x20000000` and `0x40000000`, in `0031EB20`, `003230E0`, `00327A10`, `0030D160`, `0031AA30`, `00385F60`, `00387FD0`, `002FFCF0`, `00390AB0`, `00390F20`, `00325260`, `003257D0`, `0030AC50` and others; which of those words is the action row and which another record with a `+0xC` word is exactly what the hop census with provenance (`members/action_row_reader_hops.py`, UQ-106) is built to decide, and it has not been run over these sites. Static.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - the census was run on 2026-09-18 (the next paragraph), and UQ-107 is ANSWERED at the head of this item.)*
      ***NARROWED 2026-09-18 (FABLE): the hop census was run over the `+0x0C` sites, and it decides which immediates are the action row's — eleven bits, with their readers.*** The census lists 23 provenance-verified reads of the row's `+0x0C` dword (the row pointer traced from `02EBF138`, hop 0, plus one at hop 1), and every one of the 23 tests a mask that is read at the site: [`members/action-row-0x0C-bit-readers.tsv`](members/action-row-0x0C-bit-readers.tsv). **Bit 30** (`0x40000000`) has seven readers — `BattleAction_TryEnterGlobalSpecialSequence` (`0030CE93`), `BattleAction_AcquirePresentationSlot` (`0030D011`, then `(id − 0xD0) ≤ 0x21`), `BattleUnit_HandleActionTimelineEvent` (`003253D8`, `003254BD`), `00300060` (`003000EA`, then unit `+0x6B4` in 6..7), `0030AC50`, `0031ADB0` (twice) and `003257D0` (twice) — the presentation and timeline family; **bit 13** (`0x2000`) and **bit 14** (`0x4000`) are read by `BattleFormula_ApplyPreResolutionTargetGates` (`00390EE5`, `00390E9A`), `BattleFormula_ApplyTargetStatusActionPostModifiers` (`003910C3`, `00391076`) and `00312170`, which folds them into bits 8 and 9 of the flag word it builds (`0031221E`, `0031222C`), and bit 13 also by `BattleAction_ComputeChargeLimitTicks` (~~`002F868F`~~ `002F868C`, `shr 0xd`), which reads **bit 27** (`0x8000000`) as well (~~`002F849A`~~ `002F8497`, `shr 0x1b`); **bit 19** (`0x80000`) by `BattleAction_CheckActionAvailabilityReason` (`002FFE56`, with row `+0x1E == 1` giving ~~reason~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: status mask)* `0x8000221B`); **bit 16** (`0x10000`) and **bit 26** (`0x4000000`) by the pre-resolution target gates (`00390DF1`, `00390C7F`); **bit 17** (`0x20000`) by `BattleFormula_RollSpecialGuardOutcome` (`00388058` — the `0x2018` that follows there is on another record's `+8`); **bit 11** (`0x800`) by `0031AA30` (`0031AB02`, selecting 1/2 against 3/4); **bit 12** and **bit 24** by `0031A990` at hop 1 (`bt 0xc`, `bt 0x18`, ~~together setting `[rdx] = 3`~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: bit 24 alone sets 3; bit 12 gives 0, or 5 with bit 1)*). The immediates the list above carried that no verified read tests — `0x1`..`0x8`, `0x60`, `0x200000`, `0x3000000`, `0x10000000`, `0x20000000` — ~~are tests of other records' `+0xC` words or of reads the census does not reach, and are not the action row's.~~ *(corrected 2026-09-27, FABLE, Claude Opus 5.5: all of them are - `0031EB20`, `003230E0` and `00327A10` test the rest on verified row pointers, and the census has 60 reads, not 23; [record](../../_index/candidates/uq107-action-flag-bits/README.md))* ***CORRECTED 2026-09-19 (FABLE): three of them are.*** *`0x2`, `0x200000` and `0x3000000` are tested on the action row by `Battle_BuildActionTargetSet` (`0030D461`, `0030D271`, `0030D2C0`) - whole party, centre on the actor, cone / line; [how an action gathers its targets](../how-an-action-gathers-its-targets.md). The census missed them because that routine forms the row pointer with a 32-bit add (`0030D1E9`) the provenance trace does not follow. The others in the list were not re-examined.* *(2026-09-30, SWE2-STRUCT for OPUS: answered - the 2026-09-27 correction earlier in this paragraph: `0031EB20`, `003230E0` and `00327A10` test the rest on verified row pointers.)* The shipped words the table above profiles (`0x428C` sets bit 14, `0x258C` sets bit 13) carry those two among these, so they are the live ones in the data; what each bit *means* beyond its reader's role is still not read *(superseded by the ANSWERED line at the head of this item, 2026-09-27; noted 2026-09-30, FABLE)*. Static: the census and the 23 sites.
      ***Further, same day (FABLE): the `+0x2C` clause, by the same census — bits 3 and 4 are placed, bits 6 / 7 and the element triple confirmed with provenance, and bit 5 has no literal reader at any verified site.*** The census lists 40 provenance-verified reads of `+0x2C` (byte or word); classifying each site's mask gives [`members/action-row-0x2C-bit-readers.tsv`](members/action-row-0x2C-bit-readers.tsv). **Bits 3 and 4** (`0x08`, `0x10`) are read by `BattleAction_ComputeCasterPrimaryResourceGainFromHpDamage` (`002F9323`, `002F9377`) — the two flags that shape the caster's resource gain from HP damage — and both are live in the data (the shipped values 40 = `0x28` and 49 = `0x31`). **Bits 0–2** are the element at `& 7` in `002376F0`, `00317C80`, `0031C5D0`, `0032A3E0` and `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` (`00300B3F`, then `cmp 4`); **bits 6 and 7** at the six readers named above plus `Battle_ProcessActionTarget` (`003074BE`..`003078EE`) and `00301310`; on the word, **bit 12** by `AiOrder_EvaluateTargetSelector` (`00303499`) and **bit 14** by `BattleUnit_HasCurrentFocusEngagementEvidence` (`0030BC13`), as read above. **Bit 5** (`0x20`, 166 rows) is tested by no literal at any of the 40 sites. The only verified routes that could consume it are the six word tests against a register mask — `BattleStats_HasRequiredLicenseForAction` (`00323F52`), `BattleFormula_BuildCandidateStatusMask` (`003852AB`), `BattleAction_ComputeAuthoredStatusMask` (`00387382`), `003875D0` (`0038767A`) and `BattleFormula_ApplyTargetStatusActionPostModifiers` (`00391112`, `00391192`), each `test word [row+0x2C], ax` with `ax` built by the status-mask family — the `cmp word, cx` in `AiOrder_EvaluateTargetSelector` (`00303434`), and the bare reads that use the byte or word as a value (`002376F0` four times, `AiOrder_ComputeBoundedSelectorScalar` `00308CF2`, `00322B62`, `003871CE`). So bit 5's meaning, if any, lives in what those register masks carry, which is the status-mask pages' to read. Static: the census and the 40 sites. *(2026-09-30, SWE2-STRUCT for OPUS: answered - UQ-107, ANSWERED 2026-09-27: `+0x2C` bit 5 is read by nothing. The six word tests named above use immediates loaded just before them (`0x2000`, `0x200`, `0x400`, `0x800`, `0x8000`), and no read of the 40 tests `0x20`; [record](../../_index/candidates/uq107-action-flag-bits/README.md).)*
- [x] **GR-4** *(registered 2026-09-30, FABLE)*: who reads `+0x28`, the index `120`–`153` on the 26 Quickening-family
      rows. The two-hop census (UQ-106) and the UQ-80 instrument both find no reader. The instrument does not follow row
      pointers handed on, nor copies of the row. *(Answered 2026-09-30, OPUS `8259918bb`; register row GR-4, record [`gr4-gr5-action-row-readers-0930`](../../_index/candidates/gr4-gr5-action-row-readers-0930/README.md): the one reader is `0030A190`, see the section 2.2 `+0x28` row.)*
- [x] **GR-5** *(registered 2026-09-30, FABLE)*: who reads `+0x0B`, non-zero (`1`–`3`) only on rows 182–207. Every
      reader of `+0x0A` named in §2.2 takes the low byte only. *(Answered 2026-09-30, OPUS `8259918bb`; register row GR-5: nothing in the executable reads `+0x0B`. On rows 182-207 it repeats the matching summon row's `+0x0A`, and the summon's cost is taken from the summon row, so editing it changes nothing in play.)*
- [x] **GR-6** *(registered 2026-09-30, FABLE)*: what the 436 `+0x24` words with bit 15 clear select. The selector
      `0030AC50` refuses them. The two timeline readers send them down a branch not read here (`00325476`, `00325968`). *(Answered 2026-09-30, OPUS `addead717`; register row GR-6, record [`gr6-action-row-24-0930`](../../_index/candidates/gr6-action-row-24-0930/README.md): an effect id, see the section 2.2 `+0x24` row.)*
- [x] **GR-7** *(registered 2026-09-30, FABLE)*: who reads the operand-store kind-10 mask that `00312170`
      builds from `+0x3A`, `+0x13` and `+0x0C` bits 13 and 14. The answer is also what the `+0x3A` category means. *(Answered 2026-09-30, OPUS `f0c46d818`; register row GR-7, record [`gr7-kind10-reader-0930`](../../_index/candidates/gr7-kind10-reader-0930/README.md): kind 10 is battle unit `+0xB90`, the what-was-used-on-me mask, read only by the enemy AI order selectors (opcode `0x36` / `0x37` mode 3); `+0x3A` is an AI reaction class.)*
- [x] ~~Whether the nine per-language `action_data.bin` files differ in anything but the three
      string ids (the `us` file is the one tallied).~~ **Answered 2026-09-12 — the premise was wrong.** The table
      tallied here is `battle_pack.bin` `+0x3C`, which is **byte-identical in all nine languages**; `action_data.bin`
      exists only in `ch`, `cn`, `in` and `kr` — the `ch` and `in` copies equal to the table, the `cn` and `kr`
      copies with fifteen `+0x34` words zeroed ([the VBF page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §12).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 543 × 60, the `us` section | `battle_pack.bin` directory `+0x3C` → `st2e` count `0x21F`, stride `0x3C` | data |
| the slot is bound from that section | STATIC loader id `0x13` (manifest position 19, `battle_pack`) → `00238850` → `00236C30`; `ecx = [blob + 0x3C]`, `call 00237FC0` at `00236D82`–`00236D85` | 1 |
| the section is identical in all nine languages | [the census](../../_experiments/evidence/action-table-language-census/census.py) over the archive | data |
| names index by the word, not the row | `00305F90`–`00305FD4`, `0031DB44`–`0031DB89`: `shr 0xB` for the bank, `and 0x7FF` for the entry | 1 |
| the row idiom | `00389046`–`00389089` and the 41 functions the census reached | 1 |
| every reader in §2.2 | the census site addresses, each a decoded `[row + disp]` access after the idiom | 1 |
| the shipped values | the tally over all 543 rows, every byte and word | data |
| the string-id schemes | the low-pool resolver `002F9860` (group = id / 1000) and bank 0 by the `+0x34` word ~~by row index~~ | 1 (the resolver) / data |
| `+0x04` is the knockback chance base | `00388B50` read whole (183 B): `00388BE6` reads the byte, `00388BFB` stores `max(0, …)` to `02AEDFD8` (2026-09-30, FABLE) | 1 |
| `+0x0A` is the MP cost, read as a byte | `002F962B` (`movzx … byte [rcx+0xa]`) and `0031DBD2`; the spend side on [where MP comes from](../../10-Status-Periodic-Terminal/where-mp-comes-from.md) §2 (CS-5) | 1 |
| `+0x1D` / `+0x1F` / `+0x20` are the three enmity parameters | `BattleEnmity_ApplyActionParameters` read whole (141 B): `00321716`, `00321733`, `00321744` + `neg` at `0032174B` | 1 |
| `+0x05` bounds the Reflect retarget | `00390E35` / `00390E39` / `00390E42`; the picker's `0038503B`–`00385046` (read whole, 681 B) | 1 |
| the `+0x24` selector's three cases | `0030AC50` read whole (305 B): `0030AD10`–`0030AD80` | 1 |
| `+0x3A` is a bit number into the kind-10 mask | `00312170` read whole (264 B): `003121F5`–`00312203`, `0031224D`–`0031225E` | 1 |
| the 2026-09-30 tallies (`+0x0A` / `+0x0B` bytes, `+0x24` bit 15 on 39 rows, `+0x3A` values, `+0x28` rows) | `adr_tally.py` in the [2026-09-30 DD record](../../_index/candidates/dd-content-fable-0930/) over the 543 `us` rows, parsed by the UQ-80 record's `pack.py` | data |

## 9. Related

- [`../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md`](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md) — slot `02EBF138`, AG-1 / AG-8
- [`../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §3 — `action_data.bin`
- [`../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md`](../../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) — the formula readers of `+0x10`–`+0x14`
- [`../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md`](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) — the query record's copies of `+0x0A`, `+0x13`, `+0x22`, `+0x2E`, `+0x34`
- [`../Post-Result-Events/the-post-result-events-and-the-battle-message-table.md`](../Post-Result-Events/the-post-result-events-and-the-battle-message-table.md) — the message kind `+0x1E`

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

The shipped table was re-decoded from `battle_pack.bin` independently of the prose, and the section
header states the page's own headline:

```
0x13210  magic "st2e"   count 543   stride 60 (0x3C)   data at +0x20
```

**543 rows of 60 bytes**, exactly as claimed, with the rows running `0x13230`–`0x1B174` and four bytes
of tail padding.

### Eighty tallies re-counted; seventy-nine exact

Every per-value figure in §2.2 was re-counted over the 543 rows. **79 of 80 reproduce exactly** —
`+0x04`, `+0x05`, `+0x06`, `+0x07`, `+0x08`, `+0x09`, `+0x0A`, `+0x10`, `+0x11`, `+0x12`, `+0x13`,
`+0x14`, `+0x1C`, `+0x1D`, `+0x1E`, `+0x21`, `+0x22`, `+0x24`, `+0x26`, `+0x28`, `+0x2C`, `+0x2D`,
`+0x2E`, `+0x30`, every listed value of each. So do the structural statements:

| claim | measured |
|---|---|
| `+0x15`–`+0x17` padding | **zero on all 543** |
| `+0x00` = `4000` on 327 rows, else `4001`–`4321` | **327**, and **4001 … 4321** |
| `+0x26` — thirteen summon rows, `27`–`39` | **13 rows**, values **27–39**, all thirteen distinct |
| `+0x28` — 26 Esper attacks, `120`–`153` | **26 rows**, **120–153** |
| `+0x2E` — `10000 + k` on 201 rows | **201** |
| `+0x22` — `0xFFFF` × 343, 200 others | **343** and **200** |
| the stated ceilings `+0x0A ≤ 768`, `+0x10 ≤ 253`, `+0x1C ≤ 9`, `+0x08` 0–108 | **768, 253, 9, 0–108** |

### ⚠ `+0x18`'s zero count was taken at the wrong width

The row declares `+0x18` as **u32** and tallies `0 × 424`. At u32 the zero count is **387**. `424` is
the count of rows whose **u16** at `+0x18` is zero (the u8 count is 475).

> This is [`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s own amendment — *a count
> without its unit cannot be checked* — landing on a row that does state its unit and then counts in
> another. Corrected to **387**.

### ⚠ `+0x22` holds four id spaces, and the table is blocked

The 200 non-`0xFFFF` rows are not one `0x3000 + n` run. By high nibble — which
[the encoded-id space page](../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md)
§2.1 maps to a class as `nibble + 5`:

| nibble | class | rows | row block | ids |
|---:|---:|---:|---|---|
| `0x3` | 8 | **81** | **0–80**, contiguous | `0x3000 + row`, exactly |
| `0x0` | 5 | **64** | 82–145, contiguous | `0x0000 + k` |
| `0x4` | 9 | **24** | 158–181, contiguous | `0x4000 + k` |
| `0xC` | 17 | **31** | within 208–274 | `0xC000 + k` |

**Each block numbers from its own base, `k` being the position within the block** — so
"`0x3000 + n`" is true, but only because the class-8 block happens to start at row 0. Read from the
top of the table the rule looks universal; it is one of four.

### ⚠ The help id changes rule at a single missing row

`+0x00 = 4000 + n + 1` holds **for rows 0 through 80 and no further**. Row 81 carries `4000` — no
help text — and from **row 82 the rule is `4000 + n`** (row 82 → `4082`, row 83 → `4083` …).

> **One row without a string shifts every id after it by one**, which is what a `+ 1` in an id scheme
> usually means: the pool is allocated in order and the gap is not reserved. 216 rows carry a help
> id; **81** satisfy the published form.

> And the same 81 rows are the class-8 block above. **Rows 0–80 are one authored block** — sequential
> help ids `4001`–`4081` and sequential menu ids `0x3000`–`0x3050`, one per row. The table is
> blocked, and both id schemes are per-block sequences rather than per-row properties.

### `+0x30`

Stated `600`–`4008`; the true non-zero range is **`500`–`4008`**, with one row at `500`.

**Not claimed:** §2.1's reader census (41 of 129 functions) was taken as given — it depends on a
register tracker this pass did not rebuild, and §2.1 already says it under-reports. No reader
attribution in the field map was re-derived, and nothing here changes what any field *means*: this
pass checked the shipped bytes against the tallies, not the readers against the bytes. Nothing was
executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings (the image-address resolver, the audio request chain) are recorded in the registry, not here.*

- **RNG_Random_Selection — SERVICE.** Ten combat-formula bodies in `00389DD0`–`0038D7E0` draw the gameplay MT
  (`RNG_MT19937_NextU32_Thunk`). Those are rolls on the combat-formula stream
  ([which roll](../../21-RNG-And-Determinism/which-roll-is-on-which-generator.md)).
- **Gameplay — SERVICE.**
  - `00305230`, `00305430` and `BattleAction_UpdateSpecialPresentationSequence` (`00306760`) dispatch presentation
    events.
  - `003093D0` and `00323EC0` ask the id-validity query. The 8,136-byte body asks the id-query family. `00320E10` is
    called by a 1,790-byte body.
  - `0030BB30` is read by `BattleUnit_HasActiveEngagementEvidence`.
- **ActorEntity — SERVICE.**
  - `00306760` walks the unit table and calls a 93-byte actor helper.
  - `00320E10` resolves an actor handle (`ActorHandle_ResolveRegistryEntryByPacked…`) and its world position.
  - `002EACD0` is called by a 157-byte actor body.
- **Movement — SERVICE.**
  - `00305110` and `00305230` publish the unit's locomotion position (`BattleUnit_PublishLocomotionPosition…`).
  - `00305430` calls a 448-byte locomotion helper.
  - `00320E10` reads `BattleUnit_GetNavigationClearanceRadius`.
  - `002EACD0` is also called by the 68-byte stance-bit setter.
- **Rewards_Progression_Economy — CLIENT and SERVICE.** `002EACD0` is called by the level-up path, and `00306760` calls
  the 432-byte level-rank function.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15, 3 edges).** `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` `00238880` — the action-definition row feeds the gambit menu lookup; `AiOrder_EvaluateTargetSelector` and `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` reach the cited `003093D0`/`003872D0`. The row is consumed by the AI's order selection — a real crossing, small.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatFormula — SERVICE and CLIENT (31 edges).** Most of the row's readers in §2.2 are formula stages, and they reach the formula layer's accessors and siblings: `BattleFormula_ResolveTargetResult` `00385F60` calls `BattleStats_FindOwningBattleUnit` `0031B860`, `BattleFormula_BuildEvaluationContext` `003847C0`, `BattleFormula_InitializeResultRecord` `003848E0`, `BattleFormula_ResetScratchState` `003849B0`, `BattleFormula_UpdateLowHpThresholdStatusMask` `00385B10`, `BattleFormula_ComputeKnockbackImpulseScale` `00385E50` and `BattleFormula_ApplyTargetStatusActionPostModifiers` `00390F20`, and is called by `BattleFormula_QueryResolvedScalarPreview` `00308B90` and `00390F20`; `BattleFormula_ApplyPreResolutionTargetGates` `00390AB0` calls `0031B860` and `00384F40` and is called by `BattleFormula_EvaluateTargetPreview` `00385680`; `00384F40`, `BattleFormula_RollSpecialGuardOutcome` `00387FD0`, `0038B220`, `004698C0` and `BattleFormula_DispatchPostResultEvents` `00469EC0` call `0031B860`, and `004698C0` / `00469EC0` also call `BattleStats_GetByBattleSlotIndex` `00320A40` and `BattleStats_ResolveByActorHandle` `00320A70`; `00469EC0` is called by `BattleFormula_ApplyResultMetadata` `00385BA0`; `00384C30` is called by `BattleFormula_BuildCandidateStatusMask` `003851F0`; the hit-threshold loader `00388FE0` is called by the three step bodies `003889F0`, `00390190` and `00390240`; `BattleFormula_ApplyActionElementAffinity` `0038B6A0` calls `00384B10`; outside the layer, `BattleFormula_ApplyTargetResult` `003112F0` calls `Inventory_ModifyEncodedItemAndUpdateDiscoveryState` `003008A0`, `BattleAction_UpdateSpecialPresentationSequence` `00306760` calls `00320A40`, and `Battle_BuildActionTargetSet` `0030D160` calls `BattleStats_GetByMappedBattleSlot` `00320AB0`. The row is an input to the damage pipeline: its readers are the pipeline's own stages (resolve, pre-resolution gates, element and weather stages, post-result dispatch), so these edges are that pipeline calling itself and its stats-record lookups, not a second owner of the row.

**CoreRuntimeScheduling — SERVICE (1 edge).** `00254A10` calls `00229E40`. `00229E40` is a 7-byte getter that returns one global scheduling dword, and `00254A10` returns 1 when that value is 0, 7, 8, 10 or 11 (the bit mask it tests) and 0 otherwise; §7 records this as the only depth-2 hop the reader census found, and it is a mode test, not a row read.

**Items and Items_Equipment_Shops_License — CLIENT and SERVICE (16 edges).** The row reader `003008A0` (`Inventory_ModifyEncodedItemAndUpdateDiscoveryState`, reading `+0x2C`) calls `Inventory_QueryEncodedItemStateByClass` `00309F30` and is called by every inventory writer: `InventoryBundleClass09_ApplyGilAndNestedItems` `002FD530`, `InventoryBundleClass0A_ApplyNestedItems` `002FD640`, `InventoryBundleClass0D_ApplyNestedItems` `002FD780`, `Shop_CommitPurchaseItemAndGil` `002FEEB0`, `Inventory_GrantEncodedLootItem` `00300B80`, `Inventory_MutateEncodedItemPrimaryChannelMode1` `00300BA0`, `BattleIdClassD_ResetPurchasedEntryAndNestedPrerequisiteState` `0030B180`, `EquipmentInventory_IncrementSecondaryCountChannel` `0030C410`, `EquipmentInventory_DecrementSecondaryCountChannel` `0030F9A0`, `InventoryEquipment_RestoreTemporarySnapshotAndClearBackup` `0030FAA0`, `InventoryEquipment_SnapshotAndClearTemporaryState` `0030FBE0` and `Shop_CommitSaleItemAndGil` `00310870`; the License reader `BattleStats_HasRequiredLicenseForAction` `00323EC0` (bit 5 of `+0x2D`) calls `BattleStats_HasLicensePrerequisiteForRequirement` `00323BB0` and `BattleStats_CountLicenseBits00To17` `00324020`; and the table initialiser `00236C30` calls `00238660`, the bespoke binder of one more authored table. Two of the row's readers belong to the item and License layer: the one item-change entry that every shop, loot and bundle path funnels through, and the License check, which consults the row's no-License bit before its own prerequisite tests.

**Party — SERVICE (10 edges).** `00305110`, `00305230`, `00305430`, `BattleUnit_HasCurrentFocusEngagementEvidence` `0030BB30`, `0030C0E0`, `Battle_BuildActionTargetSet` `0030D160`, `0031ADB0` and `BattleMenu_BuildCommandEntryList` `0031EB20` call `BattleUnit_ResolveByFocusHandle` `0031B7E0`; `0031ADB0` also calls `PartyFocus_GetCurrentPackedActorHandle` `003590D0`; and the Party-owned `00312EE0` calls `002EACD0`. The row's readers ask the party layer which unit is the player's focus, and `00312EE0` (a unit-visibility reset that clears two state bits and recomputes presentation suppression) is one more caller of the forwarder `002EACD0`; neither edge reads or writes the row.

**Resource — SERVICE (1 edge).** `00236C30` calls `003843F0`. `003843F0` is the loader registration that binds the `"STATIC"` section (loader `0x13`) to its delivery stub — its only call site in the image — so the edge is how the blob holding this row's table gets delivered, not a row read.

**Save_Load_Settings — CLIENT (1 edge).** `SaveSlotMetadata_BuildSubmissionDescriptor` `005832B0` calls `00254A10`. The save-slot descriptor builder asks the same mode test the reader census reached at depth 2; it is a second consumer of that 41-byte test, unrelated to the action row.

**Script_VM_Native_Bridge — CLIENT (3 edges).** `0033FED0` and `0034BA00` call the scheduling getter `00229E40`, and `0034FFC0` (23 bytes) pops one integer off the script value stack and tail-jumps into the `+0x34` reader `00305F10`. Script verbs reach one row reader directly with a script-supplied argument, and two others read the same scheduling global; the row itself is not a script structure.

**Status_Periodic_Terminal — CLIENT (3 edges).** `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140` and `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` call `002EACD0`, and `00310DB0` also calls `BattleFormula_ResolveTargetResult` `00385F60`. The maintenance tick is where the `+0x24` attached-effect id is applied through `002EACD0` (the trap applier of §2.2), and the tick resolves its periodic results through the same formula entry that reads `+0x0C`; the status layer is a caller of these readers, not a reader of the row.
