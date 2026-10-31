---
title: "Script censuses: story writes that lower the counter, save and teleport declarations, exits that choose a destination, and the verbs that steer battle AI"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00342490, 0x00343010, 0x00343470, 0x00352C80, 0x003532D0, 0x00264CA0, 0x02099FF0, 0x0026DB30"
---

## What it lists

Four censuses over the 1,114 `us` scripts under `plan_master/us` (769 zone scripts, the rest event and `evt_t`
developer scripts), read from their decompiled listings. Each call carries its script, actor, function, line, the
conditions that hold where it runs and whether any path reaches it. A line is reached when a reached block starts
with it, when it is a `case` or `default` label of a reached `switch`, when the line before it is reached and is no
`goto`, `return`, `break` or `continue`, or when a reached `goto` names its label.

### Story writes that lower the counter

The [main story counter](story-progress.md) takes 1,759 script writes, each a literal
([story counter values](story-counter-values.md)). A write lowers progress when its guard admits a counter above the
value it stores. Reading the `if` chains and every `switch` case form (`case N`, `between`, `lt`, `lte`, `gt`,
`gte`, `default`) gives: raises or keeps 179, lowers 33, unguarded 1,545, may lower 2.

All 33 lowering writes are in `evt_t` developer scripts (debug menus). The two "may lower" writes stay on the
forward side on shipped paths. `bhm_d01` main line 192 writes 7100 under `g_btl_ラスト・ヴェイン == 1`, a state
that moves only 0 to 1 (`pre_z0000` line 242) and then to 2 (`bhm_d01` line 307, before 7150 at line 315).
`gil_d01` main line 696 writes 4400; the only write in 4401-4999 is developer `evt_t0505` line 14333.

Map scripts often test the counter once in `init` and keep the answer in a file variable. Giving a test of a file
variable the counter bounds of that value's stores (three passes to a fixed point) gives: raises or keeps 194,
lowers 33, unguarded 1,530, may lower 2. With reachability, the shipped writes are:

| Verdict | Reached | Unreachable |
|---|---:|---:|
| raises or keeps | 138 | 13 |
| unguarded | 128 | 80 |
| may lower | 2 | 0 |

The 80 unreachable unguarded writes are seven copies of one hunt-board dispatch (`掲示板.talk` of `alc_f04`,
`byu_a18`, `fon_b01`, `nac_a02`, `var_a14`, and the talks of `rbn_a14` and `rbn_a16`) that follows an unconditional
jump with no label before it, plus `byu_a18` `配置監督.main` lines 821 and 833. At the bytes, `fon_b01`'s copy starts
at `0C332` and no jump in the function targets it.

The 128 reached unguarded writes were read by hand: what starts the function, which other variables guard it, and
which maps lead in. All 128 raise or keep the counter. Four of them rest on how the maps connect:

- `gil_a02` touch line 854 (4300) and `gil_c02` touch line 969 (4350), the Daedalus and Tyrant fights in Giruvegan. The
  Giruvegan writes above them (`gil_c01` 4320, `gil_g10` 4370, `gil_d01` 4400) lie past warps that open only after each
  kill:
  - `gil_a02`'s warp needs bit `0x1` of `0x0922`, and `gil_c02`'s warp into the Great Crystal bit `0x1` of `0x0926`,
    each set in that fight's touch and otherwise only inside the Crystal (its `Map_Director` inits) or by the developer
    menu `evt_t0081`, which nothing shipped loads.
  - No write above 4300 in another area runs at that counter: `var_z01` stores 5150 only when entered at 5100 or more.
- `mic_c01` main line 233 stores 340 on every entry into Terminus No. 4, before any test. From counter `0x0155`
  on, `mic_b02`'s `Map_Director` closes floor group 2, which holds both polygons of its exit to `mic_c02`, so the
  maps past it are entered only below `0x0155`.
- `mrm_c01` main line 749 (2100), the first entry into the Stilshrine boss room. The link `mrm_b02` to `mrm_d02`
  (line 359) lies in a walkable piece of its own in `mrm_b02`'s collision mesh, which only the arrival from
  `mrm_d02` stands in, so the d-wing is first entered through `mrm_c01`.

### Save, teleport and anchor declarations

A map declares no point by a verb of its own. Its zone image carries them, and the system actors read them in
`init` ([save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md)). Section 0 holds the
teleport arrival entrance at `+0x52` (`gettelepoindex`, `0x00342490`), the save entrance at `+0x78` (`getsaveindex`,
`0x00343010`) and the anchor entrance at `+0x7A` (`getanchorindex`, `0x00343470`, `movsx ebx, word [rdx+0x7a]` at
`0x0034348E`).

The image's `+0x70` word points to five list offsets. Each list holds a count at `+0` and `0x20`-byte entries from
`+0x10`; `0x00264CA0` maps kind 3 to list 2 and kind 8 to list 4. `getcrystalid(3, 0)` returns entry 0's `u16` at
`+0x14` of list 2 (`0x00352CB5`). `getanchorid(8, 0)` returns entry 0's `u16` at `+0x16` of list 4 (`0x00353305`).
`setposbynaviicon` places the actor at the same entry for kinds 3 and 8; kinds 6 and 9 go to the global table
reader `0x003DFAC0` instead.

The census finds 460 calls in 83 zone scripts, all reached:

| Verb | Id | Calls |
|---|---|---:|
| `gettelepoindex` | `0x032D` | 167 |
| `setposbynaviicon` | `0x030D` | 96 |
| `getsaveindex` | `0x032E` | 90 |
| `getcrystalid` | `0x030E` | 81 |
| `getanchorindex` | `0x032F` | 13 |
| `getanchorid` | `0x030F` | 13 |

`system_crystal_actor` declares a crystal in 81 maps: 56 save crystals (number 0) and 25 gate crystals.
One of the 81, `mic_b07`, is a script no field id names (02 asset-paths kind 5), so its crystal is never loaded.
`system_anchor_actor` declares an anchor in 13 maps: `dst_a05` 3, `ene_a08` 12, `enw_a05` 13, `fon_a06` 8,
`mnt_d01` 6, `ozm_b04` 10, `pbc_c01` 14, `pla_a06` 9, `rwf_a01` 17, `sav_c02` 5, `sav_f02` 19, `srb_a04` 15,
`wdl_a06` 4. `system_terepo_ctrl` reads `+0x52` in `init` and `main` of the same 81 maps (162 calls).

The other 16 calls: 14 in the directors of 8 scripts (`dst_b01`, `mic_b06`, `mnt_d01`, `rbn_a18`, `rrp_a01`,
`rui_a05`, `sav_b01`, `vic_a03`), which read the save or teleport entrance to place a scene, and 2 in the Sprawl.
`slm_a01` and `slm_a02` declare no crystal; their `shop_npc01.shopnpc_bindon` places the shopkeeper with
`setposbynaviicon(6, 0)`.

The `talk` switch of `system_crystal_actor` names a key item for each gate number: `0x803F + n` for the 21 numbers 1,
3-6, 8-13, 15 and 17-25, then 28 `0x8059`, 29 `0x805A`, 32 `0x805B` and 33 `0x805C`; no map declares 2, 7, 14 or 16. All 25 arms of the `telepoeffect` switch send the
key's crystal to its own map at that map's `+0x52`. The `default` arm (`pla_a06`, field 142, entrance 3) serves
`0x805C`, crystal 33.

### Exits that choose a destination

`mapjump` (`0x008D`) takes (field, entrance, mode). 7,356 calls are parsed, the verb table's `us_calls`. An exit is listed when its function
reaches two or more (field, entrance) pairs under different conditions; one row per branch. A variable argument is
followed to its stores: a script variable within its script, `scratch1` within its script (it is cleared on every
field change), and `scratch2` (class 5, `0x02099FF0`) within the zone scripts of one persistence group (`0x0026DB30`
clears it when the group changes).

`nowmap()` is the field the script runs in. Many zone scripts carry one director for a whole area, with a case per
map, so a line under a `nowmap()` test that excludes the script's own field id runs in another map's copy. 178
`mapjump` calls and 153,149 stores sit under such a test and are left out; 7,178 calls remain. When a map's own
`init` stores a `scratch2` destination on every load, the stores of other maps are left out as well (573
argument reads).

| Exits | Zone | Developer (`evt_t`) |
|---|---:|---:|
| Exits | 830 | 14 |
| Branches (rows) | 10,738 | 1,906 |
| All arguments literal | 259 | 10 |
| Some argument from a store | 571 | 4 |
| Two field ids of one place name | 147 | 8 |

By kind, the zone exits are 538 walking exits (`__MJ_CTRL###`), 81 gate-crystal teleports, 59 doors, 42 elevators,
34 warps, 29 other script functions, 19 trial-mode jumps, 13 Strahl flights, 9 talks and 6 mine carts. The
developer exits are 10 debug menus and 4 script functions. 30 more zone exits differ only in the mode argument
(the chocobo mode) and are counted, not listed.

By area, Giruvegan (`gil`) holds 443 of the zone exits: 432 walking exits, 7 warps and 4 gate-crystal teleports. Its
directors store each walking exit's field and entrance in `scratch2` per map. Next come `grm` 90, `dor` 80, `rbl` 55,
`lus` 22, `tri` 19 and `rbn` 13.

Every Great Crystal map loads one collision mesh (`gil0301.mpk`; `gil_i11` `gil0304.mpk`) that holds all six walking
exits. Its `Map_Director` case opens only the bridges toward the exits whose field it stores, and the bridge blocks of
`main` build only those. So in the map's own field, each exit that would read a value an earlier map stored lies in a
walkable piece apart from the exits the map stores itself (292 exits).

What the conditions test, counted once per exit and test kind (zone): exit lock 657, choice or local value 622,
value stored by another map 343 (292 of them the Great Crystal exits above, 50 Draklor doors that return to
`lastmap()` at the entrance `dor_a12` stored, and `dgl_n01`'s jump to the field `rbl_a01` stored), arrival or map 198, file variable 134, other 98, story counter 73, global flag 13,
party state 2. The exit lock is `regI3 = sysucoff()` ([boss fights](../Battle-Actions/boss-fights.md)).

Two examples. The aerodrome desks of `alc_e01`, `byu_b01`, `nac_b01`, `rbn_b01` and `var_b01`
(`発着イベント監視.イベント再生とマップジャンプ`) test `global_flag[2]`: 1, 7 and 14 go to `alc_e01` (794,
`0x031A`) entrance 7; 2, 4 and 6 to `rbn_b01` (788) entrance 4; 3, 8 and 10 to `nac_b01` (800) entrance 3; 5 and
12 to `byu_b01` (791) entrance 7; 9, 11 and 13 to `var_b01` (797) entrance 7.

The Draklor north elevator (`dor_a01` `北ＥＶ実処理`) reads its floor from `file_var_s6_1`. Below counter `0x0D48`
floor 67 is `dor_a12` (1019); from `0x0D48` it is `dor_d01` (1054). Floors 66, 68 and 69 split the same way.

#### Destinations the call computes

Four kinds of exit name no field in the call; `destination_map` gives the maps they reach:

- **Draklor room doors.** The door (`扉`, door) of a Draklor Laboratory room jumps to `lastmap()`, the area the party
  came from (verb `0x92`: `0x00314870` reads payload `+0x104C`, which the zone change sets to the old area). 399 rows in
  21 rooms name the corridor whose door jumps into the room: `dor_c01` (66th Floor), `dor_c12` (70th Floor),
  `dor_d01` (67th Floor) or `dor_e01` (68th Floor), each door taking the Lab Access Card.
- **The World Map picker.** The aerodrome desks of `alc_e01`, `byu_b01`, `nac_b01`, `rbn_b01` and `var_b01` and the
  Strahl flights (`ym_shutoraljump.shtjump`, 13 zones) jump to the value `openfullscreenmenu_48d(0x8000, 0)` returns.
  Selector 0 opens the World Map as a destination picker (menu id 17), which hands back the chosen area's destination
  value (`0x003C0250`, stored by `0x002901D0` at `[0x0209BE80] + 0x10FAC`).
- **Trial Mode.** The last map of a stage set (`tri_a05` to `tri_s05`) jumps from its director (`トライアル監督`, the
  Trial Mode director) to `nowmap() + 1`, then `+ 3` in its own field (`main` lines 1818-1901): the first map of the
  next set, `tri_b01` (stage 6) to `tri_t01` (stage 96).
- **Hell's Challenge.** `dgl_n01` jumps back to the map in `g_iw_陰陽師終了後ジャンプ先` (the Shadowseer fight's return
  map), which the dais (`ele.talk`) of The Wellspring (`rbl_a01`) and of Penumbra, Umbra and Abyssal - Interior
  (`rbl_g01`, `rbl_h01`, `rbl_i01`) set to its own map.

The picker's 18 values are the destination table of `menumap_world.bin` (`us`: the count 18 at `0x7AC`, four-byte
entries from `0x7B0` to `0x7F7`): 788 Rabanastre, 800 Nalbina, 231 Dalmasca Estersand, 350 Dalmasca Westersand, 248
Giza Plains, 1151 Mosphoran Highwaste, 794 Archades, 483 Phon Coast, 142 Tchita Uplands, 533 Ozmone Plain, 791
Bhujerba, 386 Ogir-Yensa Sandsea, 394 Nam-Yensa Sandsea, 473 Paramina Rift, 500 Cerobi Steppe, 797 Balfonheim Port,
509 Ridorana Cataract and 924 the Bahamut.

Every one of the 18 scripts has a `switch` on the returned value that sets the entrance in the same order, and sends
248 to field 265 (`sav_f02`) while the Giza Plains season `mp_sav季節` is 0, the Rains
([Weather](../World-Areas-And-Travel/weather.md)).

#### Readable conditions

`condition_text` reads each zone row's condition in game terms. The story counter (`シナリオフラグ`) gets the stage of
that value from [Story counter values](story-counter-values.md), or of the last value written below it. `regI3`, set by
`sysucoff()` in the exit's own function, is the exit lock. `nowmap()` names the map and `nowjumpindex()` the arrival
entrance.

The script globals with a game meaning on a page or in their store lines are named with the developer name in brackets
once: the airship route code (`global_flag[2]`), the Giza Plains season (`mp_sav季節`), the Pharos offering flags
(`mp_rbl_flg6`), the Firemane battle state (`g_btl_ブッシュファイア`) and others. Any other variable is named by what
its store lines put there, with the function and line: a question's answer, the gate-crystal destination chosen in
the teleport menu, a value set at given lines.

### Verbs that steer battle AI

32 verbs were taken from the verb table and the verb pages, and 32,071 calls in 915 scripts were counted. 29 verbs
have their effect stated on a final page; 3 foe set-up verbs (`btlAtelSetRealBattleMode`, `btlSetFriendMode`,
`btlAtelSetSummonMode`) are counted apart.
Each verb's count equals a grep of its name over the listings and the table's `us_calls`.

| Group | Verbs (id: calls) | Scripts |
|---|---|---:|
| Thinking off or on | `setbattlethinkstatus` `0x02AA`: 208; `setbattlethinkstatus_freetarget_group` `0x04B7`: 1,514 | 392 |
| Battle pause | `suspendbattle` `0x0069`: 1,490; `suspendbattle_no_resetmotion` `0x0587`: 206; `resumebattle` `0x006A`: 1,915 | 533 |
| Stance | `setforcefight` `0x0483`: 2,107; `clearforcefight` `0x0484`: 2,120; `setforcefightmode` `0x0334`: 177 | 395 |
| Engagement | `setemergency` `0x03BF`: 104; `setemergency_one` `0x0546`: 74; `resetemergency` `0x0554`: 32; `resetemergency_one` `0x057F`: 1,088 | 296 |
| Control level | `seteventpartymode` `0x050F`: 511; `seteventparty2mode` `0x0514`: 325 | 246 |
| Fighting party | `addguestbattlemember` `0x035B`: 27; `removeguestbattlemember` `0x035C`: 30; `setbattlemember` `0x0355`: 26; `addpartymember` `0x0353`: 45; `removepartymember` `0x0354`: 36 | 28 |
| Gambits | `setgambit_slotmax` `0x0504`: 2 | 1 |
| Issued command | `resetJobs` `0x05D6`: 1 | 1 |
| Foe order set | `btlAtelSetDefaultLogic` `0x3060`: 6,746 | 502 |
| Battle words | `btlAtelSetBattleLogicFlag` `0x303A`: 13,286 | 495 |
| Foe set-up | `btlAtelSetRealBattleMode` `0x3024`: 1 | 1 |

Eight listed verbs have no call in the `us` scripts. Six have a page: `setbattlethinkstatus_52e` `0x052E`,
`cancel_battle_think_only_crystal_talk` `0x057A`, `resetemergency_with_animetionmode` `0x0555`,
`suspendbattle_resetmotion` `0x0586`, `setbattlememberone` `0x0359` and `setbattlememberlock` `0x035A`. Two are foe
set-up verbs: `btlSetFriendMode` `0x3012` and `btlAtelSetSummonMode` `0x3044`.

By the kind of actor that makes the call: foes (type 7) 20,193, type 6 5,245, type 0 5,023, type 1 1,550, party
(type 5) 58, type 3 2. Foes make every `btlAtel*` call bar 2 and 162 of the thinking calls. Type 6 makes 4,221 of
the 4,404 stance calls and type 0 2,561 of the 3,611 pause calls. 750 of the 836 control-level calls are type 0.

A call can name another actor (`actor.verb(...)`): `setbattlethinkstatus` 26 times, all on `BOSS_*` and `THIRD_*`
actors, `resetemergency_one` 400 times, all on party (type 5) actors, and `setforcefight` and `clearforcefight` once
each on `cap_van` (type 6) in `bul_b01`. 348 calls are unreachable: control level
230, battle pause 116, engagement 1, thinking 1.

Guests join the fighting party by `addguestbattlemember` in eight zone scenes, by
[party row](../Party/party-members.md): `grm_b02` `イベント管理.アルマゲスト加入_PLAY` line 1096 (7, Amalia),
`mic_a01` (8, Basch), `mic_b06` (9, Basch), `byu_a01` (10, Lamont), `rsn_a01` `イベント管理.ウォースラー救援_再生`
line 915 (11, Vossler), `ene_a02` (12, Vossler), `glf_a02` (13, Larsa), `var_z01` (14, Reddas). The other 19 calls
are in `evt_t` developer scripts.

## Columns

The story-write table has one row per write; the other three have one row per call (per branch in the exits
table). `line` is the listing line of the write or call.

### script-censuses.tsv

| Column | Meaning |
|---|---|
| `script`, `script_kind` | The script, and `shipped` or `developer (evt_t)` |
| `function`, `line`, `value` | Where the write is and the value it stores in the main story counter |
| `lower_bound`, `upper_bound` | The counter bounds its guards admit (`-` for none), file-variable tests included |
| `verdict` | `raises or keeps`, `lowers`, `may lower` or `unguarded`, from the bounds |
| `guards` | The `if` and `switch` tests that hold at the write |
| `reach` | `reached` or `unreachable` |
| `read_guard`, `started_by`, `counter_range` | For the 128 reached unguarded shipped writes, read by hand: what guards the write, what starts its function, and the counter values at which it runs; `-` for the other rows |
| `read_verdict`, `evidence` | The hand reading's verdict and the listing lines it rests on; `-` for the other rows |

### [`script-census-declarations.tsv`](script-census-declarations.tsv)

| Column | Meaning |
|---|---|
| `script`, `field`, `place` | The zone script, its field id and the map's us name |
| `actor`, `function`, `line` | Where the call is |
| `verb`, `verb_id` | The verb and its table id |
| `arguments` | As the script passes them |
| `meaning` | What the verb reads, with its native address and page |
| `shipped_value` | The value it returns in the shipped zone image (entrance, or crystal or anchor number and key item) |
| `reach` | `reached` or `unreachable` |

### [`script-census-version-doors.tsv`](script-census-version-doors.tsv)

| Column | Meaning |
|---|---|
| `script`, `script_kind` | The script and `zone`, or `developer (evt_t)` |
| `field`, `place` | The script's field id and map name |
| `actor`, `function`, `exit_kind` | The exit and its kind (walking exit, door, elevator, warp, gate crystal teleport, Strahl flight, mine cart, trial mode, talk, debug menu, script function) |
| `line`, `verb`, `verb_id`, `arguments` | The `mapjump` call |
| `condition` | The conditions of the call and of the stores that give its arguments, joined by `and` |
| `condition_text` | The same conditions in game terms, one clause per test, joined by `;` (`-` on the developer rows) |
| `tests` | What the condition tests: story counter, file variable, global flag, party state, arrival or map, item or flag, exit lock, choice or local value, value stored by another map, other |
| `destination_field`, `destination_map` | The field id, or the expression the call passes, and the map or maps it reaches: for `lastmap()` the corridor that jumps into the room, for the World Map picker the 18 destinations with their entrances, for Trial Mode and `dgl_n01` the map the computed or stored value gives |
| `entrance`, `mode` | The entrance and mode; `one of ...` when the stores do not pair them |
| `resolved_from` | `literal`, or the store lines that give the field or entrance |
| `reach` | `reached` or `unreachable` |

### [`script-census-ai-verbs.tsv`](script-census-ai-verbs.tsv)

| Column | Meaning |
|---|---|
| `script`, `script_kind` | The script and `zone`, `event` or `developer (evt_t)` |
| `actor`, `actor_type` | The calling actor and the type in its `actor name(type)` header |
| `function`, `line` | Where the call is |
| `target`, `target_type` | `self`, or the actor an `actor.verb(...)` call names, and its type |
| `verb`, `verb_id`, `group` | The verb, its table id and the group above |
| `arguments` | As the script passes them |
| `meaning`, `page` | The effect and the page that states it |
| `condition` | The conditions that hold at the call |
| `reach` | `reached` or `unreachable` |

## Related

- [Story progress](story-progress.md): the counter and how scenes move it on.
- [Story counter values](story-counter-values.md): every value written.
- [Save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md): the crystal actor and its
  menus.
- [Doors, gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md): what `mapjump` does.
- [Battle verbs](../Scripts-And-Script-Commands/battle-verbs.md) and
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md): the verbs of the last census.
