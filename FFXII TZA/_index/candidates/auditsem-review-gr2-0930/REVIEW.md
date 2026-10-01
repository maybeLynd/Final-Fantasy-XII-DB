# SWE2-AUDIT-SEM review: FABLE's GR-2 answer, what each free-target type value denotes (SWE2-AUDIT-SEM for OPUS, 2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). Requested by FABLE; assigned by OPUS.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GR2-0930` |
| reviewed | `8583801b7` (FABLE): record [`gr2-free-target-types-fable-0930`](../gr2-free-target-types-fable-0930/README.md), register row GR-2, and the kind page (`battle-record-kind-byte.md`) section 7 box and status line. The record folder is unchanged between `8583801b7` and the HEAD this review ran at (`e9f01bab2`). |
| image | `FFXII_TZA.exe` SHA-256 `73461D08…D89721F8`; shipped scripts read from the VBF through the kit decoder `gen_req_channel_census.py` |
| checker | [`gr2_sem.py`](gr2_sem.py), [out](gr2_sem.out): 19 PASS, `FAILS 0`. |
| producer re-run | `gr2_join.py` re-runs byte-identical, both `gr2_join.out` and `gr2-type-scripts.tsv`. It was run through a write-redirecting wrapper, so nothing in the shared tree was written. |
| **verdict** | **ACCEPT-WITH-NARROWING.** The naming readings for 1, 3 and 5 hold as naming readings, and the per-type sums reproduce. The reading of 4 gains engine-side support the record does not cite: the verb `npc_to_gimmick`. But the record misses two of the type's writers, and both are script verbs. It misstates where 0 and 2 come from. It turns "argument 3 means type 4" into an unconditional join, although the engine makes it conditional. And it carries none of the run-time limits. Corrections C1–C5 follow. |

Evidence classes: **static** (S, F1–F3 and F8, from the image), **data** (D1–D2, F4–F7 and F9, from the shipped scripts)
and **record** (F8's verb-adapter table row). Nothing here is live.

## 1. What holds (SWE2-AUDIT-SEM for OPUS)

- **S1: the table.** `002396B0` stores `{1, 5, 3, 4}[v]` from `01E09EE8`, or 0 for v > 3, into the battle unit's
  `+0x58`. It does not store into the nibble.
- **D1, D2: the counts.** The decode reproduces SD-160's eight (verb, argument) counts over 16,666,842 CALL-family
  sites. The record's per-type sums reproduce: 59,832 / 612 / 2,709 / 234 / 45.
- **F6: type 3's largest group.** Five `disp_tama` scripts in seven `rbl` zones carry 35 distinct sites (315 with copies),
  all `setfreetargettype(3)`. The record lists them, but its reading "allied or event combatant" fits only the other
  half (C5).
- **The readers.** The record's agreement with the readers is as stated (AL-3): 5 is the classifier's neutral value, 3
  is singled out, and {1, 2, 7} is the enemy group.

## 2. Findings (SWE2-AUDIT-SEM for OPUS)

| id | finding | consequence |
|---|---|---|
| F8, F9 | **Two more script verbs write the nibble.** `npc_to_gimmick` (`0x048E`, adapter `0034DA20` → `00267CC0`) stores **4**, and `gimmick_to_npc` (`0x048F`, `0034DD80` → `002659A0`) stores **5**. Both are in the verb table (`01EF68E0` / `01EF6900`) and in the kit's verb catalogue. `npc_to_gimmick` is authored at **2,036 sites in the us copy**, in 390 files: 1,966 in `treasure_NN` scripts, 42 in `tama` / `o_tama`, and the map and key pots. `gimmick_to_npc` has no shipped site. | The record's census, "every shipped call of the two verbs that set the type", misses type 4's largest authored source. Its type-4 count of 2,709 is a two-verb count, not the type's. The engine's own verb name, *npc → gimmick*, supports the reading "an object the player interacts with". |
| F8 | **A third non-verb writer.** `ActorSystem_BindBattleUnitsForEligibleRecords` (`00265A20`, `00265ACA` / `00265ACE`) stores **1** in the nibble of each record it binds (`r14d` = 1 at `00265A99`). | The record and AL-3 name only the refresh and `setfreetargettype` as writers. |
| F3 | **Value 0 is the record initialiser's, not the refresh's.** `ActorStorage_InitializeRecord` (`00266530`) clears the nibble (`002666F8` `and byte [rbx+0xe], 0xf0`), then calls `00265FF0`. That function seeds 4 only for actor kind 1 and 5 only for kind 3; kind 2's branch writes `+8`, not `+0xE`. Every other kind keeps 0. The refresh never stores 0: it skips the write for mode 0 (`00238E34` / `00238E36`, F2). | The record's "0, 2, 7: they come only from the unit refresh" is wrong for 0. |
| F3 | **No writer read here produces 2.** A census of the nibble-clear idiom finds every partial clear (six sites). The six writers it identifies store 0, 1, 4, 5, the verb's argument (1, 3, 4 or 6 as authored), or the refresh mode (1, 3, 4, 5 or 7). | "2 comes from the refresh" is unsupported. Statically, 2 has no producer in the shipped game. The readers that accept 2 test a value nothing writes. Limit: a whole-byte `mov` to `+0x0E` from a non-actor function was not excluded; the actor-range ones were read. |
| F1, F2 | **`btlAtelSetUnitType(3)` → type 4 is conditional.** `002396B0` raises the spawn record's flag bit 5 for mode 4 only when that record's bits 0 and 2 are clear (`002396E2` `test cl, 5`). With bit 5 clear, the refresh rewrites mode 4 to 1 (`00238DBD`–`00238DC3`). It also turns mode 1 into 7 for an enemy row whose definition byte `+0x03` has bit 4. | The 369 sites give type 4 only for units whose spawn record allows it. Otherwise they give 1. 7 of the 31 us (file, script) pairs that pass 3 also pass 0 in the same script (F5). So "a monster parked as type 4" is a reading the bytes neither confirm nor exclude. |
| F2 | **The refresh overwrites the nibble from the mode at every refresh** (`00238E0D` → `00238E3E`). | For an actor with a bound battle unit and a nonzero mode, a `setfreetargettype` value lasts until the next refresh. The table records what scripts ask for, not the value at any moment. OPUS's record states this limit; FABLE's does not. |
| F4 | **Every count is nine language copies.** The 9 languages carry the same (file, script, verb, argument) multiset. Each count is 9 × the us count; for example, `setfreetargettype(1)` = 18 is 2 distinct sites, and `system_crystal_actor` 2,187 is 243 sites. | The record does not say so. OPUS's record folds the copies. |
| F7 | **Type 6** is set in three scripts. Only two carry the `STAY_` prefix. `BOSS_Dウォール` has no such prefix and also passes 1 to the same verb. `STAY_ダイダロス` names a whole boss. | "Stationary boss part" reads more into the names than they carry. |

## 3. Corrections for the owner (pipe-free wording) (SWE2-AUDIT-SEM for OPUS)

- **C1: the writers.** Replace "SWE2-AUDIT-SEM's review C3 pointed at SD-160's census … This record joins every value"
  and the method's two-verb scope with this:

  > The nibble has six writers: `setfreetargettype` (`00269FE0`, as authored 1, 3, 4, 6); `npc_to_gimmick` (`0x048E`, `00267CC0`, stores 4; 2,036 us-copy sites, nearly all `treasure_NN`); `gimmick_to_npc` (`0x048F`, `002659A0`, stores 5; unused); the unit refresh (the battle unit's mode, which `btlAtelSetUnitType` sets through `{1, 5, 3, 4}`, rewritten to 1 or 7 as below); `ActorSystem_BindBattleUnitsForEligibleRecords` (stores 1); and the record initialiser (0, then 4 for kind 1 or 5 for kind 3).

  Type 4's row should add `npc_to_gimmick` as its largest authored source.
- **C2: 0, 2 and 7.** Replace "never authored: they come only from the unit refresh, AL-3's other writer" with this:

  > No script passes 0, 2 or 7. 7 is the unit refresh's, for mode 1 on an enemy row whose definition byte `+0x03` has bit 4 while the spawn flag bit 5 is clear. 0 is the record initialiser's, for actors of kinds other than 1 and 3 that nothing retypes, and the getter's answer for a null actor. No writer read produces 2.

- **C3: type 4 from monsters.** Replace "ordinary `monster_*` scripts in 18 zones … a monster parked as one" with this:

  > `btlAtelSetUnitType(3)` (369 sites, 41 distinct) gives type 4 only while the unit's spawn record has bit 5. `002396B0` raises it when that record's bits 0 and 2 are clear; otherwise the next refresh turns mode 4 into 1. 7 of the 31 us-copy scripts that pass 3 also pass 0.

- **C4: the limit.** Add this:

  > The table is what the scripts ask for. The unit refresh rewrites the nibble from the unit's mode at every refresh, so a live actor's value can differ from its script's.

- **C5: types 3 and 6.**
  - For 3, use this wording:

    > an allied or event combatant, plus the five `disp_tama` objects of seven `rbl` zones (35 of the 68 distinct sites)

  - For 6, use this wording:

    > the type three boss-fight scripts set (`BOSS_Dウォール`, which also sets 1, `STAY_ボス武器`, `STAY_ダイダロス`); "stationary" is the `STAY_` naming of two of them

- **Counts.** State that every site count is nine language copies (F4).

The same corrections apply to the register row GR-2 and the kind page's box, which repeat the record's table.

## 4. Cross-check against OPUS's record (SWE2-AUDIT-SEM for OPUS)

OPUS's `gr2-free-target-values-0930` gives the same five readings. It folds the language copies, and it states the
refresh limit (C4). It shares the record's gaps in C1 (`npc_to_gimmick` / `gimmick_to_npc`, the binder) and in the origin
of 0. Its limits name only the record initialisation's "4 or 5". It also reads type 6 as "stationary boss parts" (C5).
Those points apply to OPUS's record as well. They are routed to OPUS in this review and are not deferred to it.

Routing: C1–C5 go to FABLE (the GR-2 row and the kind page), and the same points go to OPUS for its parallel record.
This review edits no page or register row.
