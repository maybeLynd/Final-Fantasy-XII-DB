# GR-2 answered: what each free-target type value denotes as authored (OPUS, 2026-09-30)

Register row GR-2 asks what each value of the actor's free-target type nibble (`+0x0E & 0xF`, AL-3) denotes as authored:
its readers' behaviour per value was known, the values themselves were not named. The row's plan: census the immediate
values scripts pass to `setfreetargettype` (0x0265) and `btlAtelSetUnitType` (0x3005) and join each to the actor it targets.
The page is [the battle record kind byte](../../../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md) §7.

Method: SD-160's census loop (`sd160-free-target-type3-0930/sd160_census.py`, FABLE's `.ebp` decoder over every shipped
script) reused verbatim in `gr2_census.py`, which maps each call to the value it stores - `setfreetargettype(v)` stores `v`
(`00269FE0`), `btlAtelSetUnitType(v)` stores `{1, 5, 3, 4}[v]` (`002396B0`, table `01E09EE8`; SD-160 F2-F3) - and tabulates the
scripts per value (`gr2-values.tsv`; language copies folded). Checker `gr2_check.py` (output `gr2_check.out`, **`FAILS 0`**).

## The answer (OPUS)

| value | calls | what the scripts give it to |
|---:|---:|---|
| **1** | 59,832 | **ordinary enemies** - the default: `btlAtelSetUnitType(0)` in every `monster_NN`, unique-monster, trial and lot script (59,814), plus 18 `setfreetargettype(1)` |
| **3** | 612 | ~~**allied third parties and event combatants** -~~ **an allied or event combatant, plus the five `disp_tama` objects of seven `rbl` zones (35 of the 68 distinct sites)** (C5) - the `THIRD_*` guests (Larsa, Gabranth, ~~Montblanc~~ ...; *Montblanc struck 2026-10-01, OPUS: the script name `モーニ` is not his Japanese name `モンブラン`, per SWE2-AUDIT-SPEC's [SD-160 review](../auditspec-review-sd160-0930/REVIEW.md)*), `npc_battle_00`, the `naf_` soldiers beside Basch, Trial actors, the `disp_tama` objects (SD-160) |
| **4** | 2,709 | **system objects** - save crystals (`system_crystal_actor`, 2,187), anchor actors, treasure chests, a soldier's corpse - and a few monsters set to it. **Not counted here: `npc_to_gimmick` (0x048E) also stores 4, at 2,036 us-copy sites, nearly all `treasure_NN`; it is type 4's largest authored source (C1)** |
| **5** | 234 | **non-combatant NPCs** - town and prison people (`TWN_*`, `SND_*`, `PRISON_*`) and briefly Basch / a Dalmascan soldier |
| **6** | 45 | ~~**stationary boss parts** - the Demon Wall (`BOSS_Dウォール`), a boss's weapon and Daedalus (`STAY_*`)~~ **the type three boss-fight scripts set (`BOSS_Dウォール`, which also sets 1, `STAY_ボス武器`, `STAY_ダイダロス`); "stationary" is the `STAY_` naming of two of them** (C5) |
| 2, 7 | 0 | never authored by either verb; 7 is the unit refresh's value for enemy rows with byte `+0x03` bit 4 (AL-3). **No writer read produces 2 (C2)** |

So the readers' behaviour lines up with the authored meaning: 5 is neither friend nor foe because it marks townspeople; the
field cursor helpers accept 1-3, 3 and 5 as the kinds of actor the player can point at; the time-stop sweep's groups
{1, 2, 7}, {3} and the rest separate enemies, allies and objects.

**In player terms:** the game tags every scripted actor as an enemy, an allied guest, an object (crystal, chest), a
townsperson or a fixed boss part, and that tag decides whether your targeting, gambits and time effects treat it as a foe.

## Corrections from SWE2-AUDIT-SEM's review (OPUS, 2026-10-01)

[`auditsem-review-gr2-0930`](../auditsem-review-gr2-0930/REVIEW.md) accepted the five readings with narrowing. Its checker
`gr2_sem.py` reproduces at 19 PASS, FAILS 0 (re-run by OPUS). The table above carries C1 and C5 in place. The rest:

- **C1, the writers.** This census read two verbs, but the nibble has six writers:
  - `setfreetargettype` (`00269FE0`; as authored 1, 3, 4, 6);
  - `npc_to_gimmick` (`0x048E`, `00267CC0`; stores 4);
  - `gimmick_to_npc` (`0x048F`, `002659A0`; stores 5, unused);
  - the unit refresh (from the battle unit's mode, which `btlAtelSetUnitType` sets through `{1, 5, 3, 4}`, rewritten to
    1 or 7);
  - `ActorSystem_BindBattleUnitsForEligibleRecords` (`00265A20`; stores 1);
  - the record initialiser (`002666F8`; 0, then 4 for kind 1 or 5 for kind 3).
- **C2, 0, 2 and 7.** No script passes 0, 2 or 7. 7 is the unit refresh's value for mode 1 on an enemy row whose
  definition byte `+0x03` has bit 4 while spawn flag bit 5 is clear. 0 is the record initialiser's value, for actors of
  kinds other than 1 and 3 that nothing retypes; it is also the getter's answer for a null actor. No writer read produces 2.
- **C3, type 4 from `btlAtelSetUnitType(3)`.** It gives type 4 only while the unit's spawn record has bit 5; otherwise the
  next refresh turns mode 4 into 1.
- **Counts.** Every site count in the table is nine language copies of the same sites. "Language copies folded" in the
  method refers to the script list, not to the counts.

## Limits

- The census reads what the scripts ask for; the unit refresh can replace the value at run time (4 with the spawn flag bit
  5, 7 for enemy rows with `+0x03` bit 4 - AL-3), so a live actor's value can differ from its script's.
- Value 2 has no authored source in these two verbs; whether another writer produces it is AL-3's (the refresh) and is not
  re-derived.

## Consumers (routed, not edited here)

- The kind-byte page §7 (FABLE's) and register row **GR-2**, via the GR restatement batch.
