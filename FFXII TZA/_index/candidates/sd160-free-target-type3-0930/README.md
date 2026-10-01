# SD-160: the units that carry free-target type 3 (OPUS, 2026-09-30)

Register row SD-160 was registered by SWE2-DATA
([steam-integration-and-achievement-catalogue.md](../../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)
section 7). It asks which units carry free-target type 3, and so which defeated units the bestiary defeat tally skips.

The evidence is of two kinds, kept apart:

- **F1–F3 are static**, read from the certified image.
- **C1–C3 are a census of the shipped scripts.** `sd160_census.py` decodes every `.ebp` in the VBF with FABLE's decoder
  (`25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py`). Script names come from the name
  pool at header `+0x4C` (BW-5). Its output is ~~`sd160-census.tsv` (every call of the two verbs) and
  `sd160-type3-scripts.tsv` (the type-3 sites).~~ `sd160-census.tsv` (the 612 type-3 sites, all languages) and
  `sd160-type3-scripts.tsv` (one row per zone, verb and script). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd160-0930/REVIEW.md))*

The checker is `sd160_check.py` (output `sd160_check.out`, `FAILS 0`).

## What decides type 3 (OPUS)

- **F1: the skip.** `003171C0` handles a defeated unit whose record is kind 1:
  - it always calls `00253770(4, 1)`;
  - it calls the bestiary tally `00253750` only when the actor's free-target type (`00263C20`, actor `+0x0E & 0xF`)
    is **not 3** (`cmp eax, 3` at `00317207`) **and** the unit definition's `+0x52` is not `0xFFFF`.
- **F2: `setfreetargettype` (`0x0265`, `003528C0`) stores its argument as is.** It passes the executing actor and the
  popped int to `00269FE0`, which writes the low nibble of `+0x0E` (`0026A033`–`0026A03B`). An argument of 3 gives
  type 3.
- **F3: `btlAtelSetUnitType` (`0x3005`, `00510340`) goes through a table.** It tail-calls `002396B0(actor, v)`, which
  stores `{1, 5, 3, 4}[v]` from `01E09EE8` (0 when `v > 3`) into the actor's battle unit `+0x58`. The unit refresh
  copies that byte into the nibble (AL-3). **So argument 2, not 3, gives type 3;** argument 3 gives type 4.

## Who carries it (OPUS)

- **C1: every call is a constant.** The shipped scripts hold 63,432 calls of the two verbs, and every one pushes a
  constant argument. `btlAtelSetUnitType(2)` has 297 of them and `setfreetargettype(3)` 315.
- **C2: one list, nine languages.** Every type-3 site is in a `plan_master` zone file. The nine language copies carry
  the same sites: 68 per language (612 in all), in 29 zone files.
- **C3: the 68 sites.** Each is a distinct (zone, script) pair.

| verb | scripts | zones | sites |
|---|---|---|---:|
| `btlAtelSetUnitType(2)` | ~~`THIRD_*` (Gabranth, Larsa, Montblanc and seven more third-party allies)~~ `THIRD_*` (Gabranth and Larsa, from `ガブラス` / `ラーサー`, and eight more third-party scripts, among them `モーニ` twice; `モーニ` is not Montblanc's Japanese name `モンブラン` and is not resolved to a character here) | `bhm_c01`, `enw_c01`, `frs_a04`, `grm_b02`, `pbc_b01`, `rui_a04`, `sav_g01`, `srb_b04`, `ztc_a03` | 10 |
| | `npc_battle_00` | `dst_a02`, `fon_c02`, `ozm_a03`, `sav_c03`, `sav_f01`, `wdl_a01` | 6 |
| | `event_garif_00` | `ozm_a03` | 1 |
| | `DAL_SOLDIER_A/B/C`, `BASH` | `naf_a02`, `naf_b01`, `naf_b02` | 12 |
| | `ex_trial_00/03/05` | `tri_f05`, `tri_k02`, `tri_l04`, `tri_n05` | 4 |
| `setfreetargettype(3)` | `disp_tama01`–`disp_tama05` | seven `rbl_` zones (`rbl_b01`, `rbl_g02/g03`, `rbl_h02/h03`, `rbl_i02/i03`) | 35 |

**For modding:** type 3 is what the scripts give **allied third parties and event combatants**: guest-style allies,
field NPCs that fight, the `naf_` soldiers beside `BASH`, four Trial Mode actors, and the `disp_tama` objects. A
defeat of any of them never reaches the bestiary tally while it carries type 3.

## Limits (OPUS)

- **Type 3 is not the only skip.** F1 also skips a unit whose definition `+0x52` is `0xFFFF`, and only kind-1 records
  reach the check. The tally `00315820` has its own conditions: AA-7 lists eleven special monsters (`00315D50`).
  SD-160 names the type-3 set only, as SWE2-AUDIT-SEM's DD-4 review (`18c11f3b1`) noted.
- **The census reads what the scripts ask for, not the value at defeat.** The refresh can replace the unit mode's
  value: 4 with the spawn flag bit 5, 7 for enemy rows whose byte `+0x03` has bit 4 (AL-3). A later
  `setfreetargettype` or refresh can also overwrite a script's 3. Which of these units is ever defeated, and with
  what type at that moment, is a run-time fact.
- **Only these two verbs are censused.** The nibble's other writers are AL-3's: the refresh, which copies `+0x58` (so
  its 3 is F3's), and the record initialisation (4 or 5).
- ~~The Japanese script names are decoded as cp932; the English names in the table (Gabranth, Larsa, Montblanc) are
  readings of `ガブラス`, `ラーサー`, `モーニ`, and the "seven more" are `カロリーヌ`, `アルマ`, `シーク`, `バンサト`,
  `ヴィエラ`, `ガリフ` and a second `モーニ`.~~ The Japanese script names are decoded as cp932. `THIRD_*` (Gabranth and Larsa, from `ガブラス` /
  `ラーサー`, and eight more third-party scripts, among them `モーニ` twice; `モーニ` is not Montblanc's Japanese name
  `モンブラン` and is not resolved to a character here). The other six are `カロリーヌ`, `アルマ`, `シーク`, `バンサト`,
  `ヴィエラ` and `ガリフ`. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd160-0930/REVIEW.md))*
