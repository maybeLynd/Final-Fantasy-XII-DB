---
title: "Script calls in every script: story writes that lower the counter, save and teleport declarations, exits that choose a destination, and the verbs that steer battle AI"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00342490, 0x00343010, 0x00343470, 0x00352C80, 0x003532D0, 0x00264CA0, 0x02099FF0, 0x0026DB30, 0x00355680, 0x002677F0, 0x0034E260, 0x00265680, 0x003456C0, 0x00233D20, 0x0034A590"
---

## What it lists

Four lists of calls over the 1,114 `us` scripts under `plan_master/us` (769 zone scripts, the rest event and `evt_t`
developer scripts). Each call carries its script, actor, function, line, the
conditions that hold where it runs and whether any path reaches it. A line is reached when a reached block starts
with it, when it is a `case` or `default` label of a reached `switch`, when the line before it is reached and is no
`goto`, `return`, `break` or `continue`, or when a reached `goto` names its label.

### Story writes that lower the counter

The [main story counter](story-progress.md) takes 1,759 script writes, each a literal
([story counter values](story-counter-values.md)). A write lowers progress when its guard admits a counter above the
value it stores. Reading the `if` chains and every `switch` case form (`case N`, `between`, `lt`, `lte`, `gt`,
`gte`, `default`) gives: raises or keeps 179, lowers 33, unguarded 1,545, may lower 2.

All 33 lowering writes are in `evt_t` developer scripts (debug menus). The two "may lower" writes stay on the
forward side on story paths. `bhm_d01` main line 192 writes 7100 under `g_btl_ラスト・ヴェイン == 1`, a state
that moves only 0 to 1 (`pre_z0000` line 242) and then to 2 (`bhm_d01` line 307, before 7150 at line 315).
`gil_d01` main line 696 writes 4400; the only write in 4401-4999 is developer `evt_t0505` line 14333.

Map scripts often test the counter once in `init` and keep the answer in a file variable. Giving a test of a file
variable the counter bounds of that value's stores (three passes to a fixed point) gives: raises or keeps 194,
lowers 33, unguarded 1,530, may lower 2. With reachability, the 361 writes in story scripts are as below; the other
1,398, in the `evt_t` developer scripts, are all reached (1,322 unguarded, 43 raise or keep, 33 lower):

| Verdict | Reached | Unreachable |
|---|---:|---:|
| raises or keeps | 138 | 13 |
| unguarded | 128 | 80 |
| may lower | 2 | 0 |

The 80 unreachable unguarded writes are six copies of one hunt-board dispatch (`掲示板.talk` of `alc_f04`, `byu_a18`,
`fon_b01`, `nac_a02`, `var_a14`, and the talk of `rbn_a14`) that follows an unconditional jump with no label before
it, plus `byu_a18` `配置監督.main` lines 821 and 833. The seventh copy, in the talk of `rbn_a16` (lines 1341 to 1377),
sits under `シナリオフラグ > 80`, so its 13 writes are the 13 unreachable ones that raise or keep the counter. At the bytes,
`fon_b01`'s copy starts at `0C332` and no jump in the function targets it.

For the 128 reached unguarded writes the table gives what starts the function, which other variables guard it, and
which maps lead in. 127 raise or keep the counter. One may lower it: `mrm_e01` main line 551 (2150) runs on the first
entry into a boss room, and the counter tests on the story scripts' map jumps leave other areas open before that
entry, where later writes store more, so the listings give the counter at that entry no upper bound. Six of the 127
rest on how the maps connect:

- `gil_a02` touch line 854 (4300) and `gil_c02` touch line 969 (4350), the Daedalus and Tyrant fights in Giruvegan. The
  Giruvegan writes above them (`gil_c01` 4320, `gil_g10` 4370, `gil_d01` 4400) lie past warps that open only after each
  kill:
  - `gil_a02`'s warp needs bit `0x1` of `0x0922`, and `gil_c02`'s warp into the Great Crystal bit `0x1` of `0x0926`,
    each set in that fight's touch and otherwise only inside the Crystal (its `Map_Director` inits) or by the developer
    menu `evt_t0081`, which nothing shipped loads.
  - No write above 4300 in another area runs at that counter: `var_z01` stores 5150 only when entered at 5100 or more.
- `mic_c01` main line 233 stores 340 on every entry into Terminus No. 4, before any test. From counter `0x0155`
  on, `mic_b02`'s `Map_Director` closes floor group 2 (`counter >= 0x0155`, the `else` of `init` line 403), which
  holds both polygons of its exit to `mic_c02`, so the maps past it are entered only below `0x0155`.
- `mrm_c01` main line 749 (2100), the first entry into the Stilshrine boss room. The link `mrm_b02` to `mrm_d02`
  (line 359) lies in a walkable piece of its own in `mrm_b02`'s collision mesh, which only the arrival from
  `mrm_d02` stands in, so the d-wing is first entered through `mrm_c01`.
- `rui_c01` main line 210 (3200) and `rui_d01` main line 225 (3150), the first entries into two Sochen Cave Palace
  boss rooms. Before them the party can reach the Feywood and Balfonheim, but no further:
  - below `0x1040`, `mfr_a04`'s `Map_Director` closes floor group 1 (`counter < 0x1040`: the `main` line 1108
    switch cases `lt(0x1004)` and `lt(0x1040)`) so that no entrance joins the exit into `mfr_b01`, the only way on
    to the Feywood's inner maps and Giruvegan;
  - for counters 1 to `0x0FA0`, `var_a01`'s `EventDirector` closes floor group 1 (`counter && counter <= 0x0FA0`,
    `init` line 1371) so that only the arrival from `var_a02` joins the exit into the town;
  - the airship into Balfonheim needs a destination stored only at `0x1004` or more, or in Archades.
  - The other writes above 3150 on the maps open before them run only at higher counters: `mfr_a04` touchon line
    1309 at `0x1004` to `0x103F`, and `alc_z01` main line 194 at 2000 or more, while `alc_z01` is entered only at
    1130, 1973 and 1998.

### Save, teleport and anchor declarations

A map declares no point by a verb of its own. Its zone image carries them, and the system actors read them in
`init` ([save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md)). Section 0 holds the
teleport arrival entrance at `+0x52` (`gettelepoindex`, `0x00342490`), the save entrance at `+0x78` (`getsaveindex`,
`0x00343010`) and the anchor entrance at `+0x7A` (`getanchorindex`, `0x00343470`, `movsx ebx, word [rdx+0x7a]` at
`0x0034348E`).

`getanchorindex` reads the zone image through the first pointer of actor manager 0 (`0x00263FF0(0)`, `0x02098E10`) and
answers 0 when that pointer is null (`0x0034347D`-`0x0034348C`); it writes the answer through `0x0026B4E0` (`0x003434A1`).

The image's `+0x70` dword (`0x00264B03`, `0x00264B10`) points to five list offsets. Each list holds a count at `+0` and `0x20`-byte entries from
`+0x10`; `0x00264CA0` maps kind 3 to list 2 and kind 8 to list 4. `getcrystalid(3, 0)` returns entry 0's `u16` at
`+0x14` of list 2 (`0x00352CB5`). `getanchorid(8, 0)` returns entry 0's `u16` at `+0x16` of list 4 (`0x00353305`).
`setposbynaviicon` places the actor at the same entry for kinds 3 and 8; kinds 6 and 9 go to the global table
reader `0x003DFAC0` instead.

`getanchorid` (`0x003532D0`) pops the index and then the kind (`0x003532E8`, `0x003532F2`) and answers the `u16` at
`+0x16` of the entry `0x00264CA0(kind, index)` returns, or -1 when it returns null (`0x00353303`-`0x0035330B`); it
writes the answer through `0x0026B4E0` (`0x00353320`).

There are 460 calls in 83 zone scripts, all reached:

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

A map's crystals and arrival points are not written in its scripts: the map's zone file holds them, and the shared
crystal actor reads them when the map starts. Each gate crystal's number is tied to a key item, and teleporting to
that crystal lands the party at its map's own arrival point.

### Exits that choose a destination

`mapjump` (`0x008D`) takes (field, entrance, mode). 7,356 calls are parsed, the verb table's `us_calls`. An exit is listed when its function
reaches two or more (field, entrance) pairs under different conditions; one row per branch.

A variable argument is
followed to its stores: a script variable within its script, `scratch1` within its script (it is cleared on every
field change), and `scratch2` (class 5, `0x02099FF0`) within the zone scripts of one persistence group (`0x0026DB30`
clears it when the group changes, `0x0026DC11`, and on an arrival whose transition mode has bit `0x8`, a teleport,
`0x0026DC2E`).

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
floor 67 is `dor_a12`, from `0x0D48` `dor_d01`: `file_var_s6_2 = counter < 0x0D48 ? 1019 : 1054` (`dor0101` line
1944). Floors 66, 68 and 69 split the same way.

#### Destinations the call computes

Four kinds of exit name no field in the call; `destination_map` gives the maps they reach:

- **Draklor room doors.** The door (`扉`, door) of a Draklor Laboratory room jumps to `lastmap()`, the area the party
  came from (verb `0x92`: `0x00314870` reads payload `+0x104C`, which the zone change sets to the old area). 399 rows in
  21 rooms name the corridor whose door jumps into the room: `dor_c01` (66th Floor), `dor_c12` (70th Floor),
  `dor_d01` (67th Floor) or `dor_e01` (68th Floor), each door taking the Lab Access Card.
- **Draklor rooms no exit enters.** The other 551 room-door rows are in 29 rooms (`dor_a02` to `dor_e16`, such as Rm 6613 West) that no story exit enters: in the listings of all nine language trees the only jumps to their field ids are the developer menus `evt_t0084` and `evt_t0509`, no stored room id reaches a jump call, and none of the 29 holds a save crystal.
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

The engine calls that conditions test read as follows:

- `istownmap()` (`0x053C`, `0x00355680`) is the town flag of the current area: bit `0x8000` of its word in the map-info
  table (`0x00377C20`, [kill chain](../Rewards-EXP-Gil-And-Loot/kill-chain.md)); 1 in a town.
- `istouchuc()` (`0x026D`, `0x0033FA40`, `0x002677F0`) is 1 when the controlled character (`0x003590D0`) touches the
  calling actor: a trigger rect (class 1) tests its party-slot mask `+0x60`, an actor with a contact box (class 3)
  its contact mask `+0x100` (filled by the touch test `0x0025C230`, `0x0025C6A1`); any other class gives 0. The handler
  passes `0x002677F0` a 0 that it pushes and pops (`0x0033FA5D`-`0x0033FA65`); a non-zero one would test `+0x228`.
  - `0x002677F0(actor, flag)` reads the controlled character's actor record, `0x003588B0(0x003590D0())`, and gives 0
    when that record is null (`0x00267815`) or its party-slot byte `+0x12` is outside 0-3 (`0x0026781E`). The bit it
    tests is the bit value `1 << slot` (`0x00267829`), in the calling actor's block `[actor+0xB8]` (`0x0026783C`,
    `0x0026787D`); the class is the actor's byte `+0x03` shifted right by 5 (`0x0026782B`-`0x0026782F`).
- `keyscan(m)` (`0x0015`, `0x0034E260`) is 1 when a button of the mask `m` is held: `m & 0x0036FF70()`, the held word
  after the button map (`0x02AD9E04`, [controls](../Controls-And-Input/controls.md)).
- `getucstatus()` (`0x014D`, `0x00343690`, `0x00265680`) is 1 while the party is under player control: manager slot 0
  active and every active manager ready, with no text window holding the field (`0x002E0540`,
  [EBP text sections](../EBP-Script-Files/ebp-text-sections.md);
  [player movement](../Movement-And-Pathfinding/player-movement.md)).
  - `0x00265680` answers 1 only when manager 0 is live (`0x02098E20` bit `0x1`) with `0x02098E21` bit `0x1` and `0x02098E20`
    bit `0x80` clear, every live manager's byte `+0x17` holds bits `0x1` and `0x2` (`0x002656C0`-`0x002656D2`),
    `0x002E0540()` is 0 and `0x00265720()` finds bytes `+0x14`, `+0x15` and `+0x16` non-zero on every live manager;
    any other case gives 0.
- `get_talk_run_status()` (`0x057C`, `0x003456C0`) returns `0x02099DB4`, the world locks held by running talks (the sum of
  the managers' `+0x1E0` counters); the talk button works only while it is 0
  ([script requests](../Scripts-And-Script-Commands/script-requests.md)).
- `is_enable_run_event()` (`0x04FF`, `0x003475E0`, `0x00233D20`) is 1 when no party-down state is set
  (`0x02089340 & 0xF00` = 0) and time-stop request 10, the one-at-a-time action display, is not raised
  (`0x00226BD0(10)`, [time stop](../Engine-Core/time-stop-and-freeze.md)).
- `getsummonid()` (`0x050D`, `0x0034A590`) is the summoned Esper's character row (block byte `+0x5AD4`, `0x003137E0`)
  while summon mode is on (`0x003135C0`), and -1 otherwise.

The script globals with a game meaning on a page or in their store lines are named with the developer name in brackets
once: the airship route code (`global_flag[2]`), the Giza Plains season (`mp_sav季節`), the Pharos offering flags
(`mp_rbl_flg6`), the Firemane battle state (`g_btl_ブッシュファイア`), the Garamsythe sluice gates (1 closed, 0 open),
the two Lhusu Mines switches and others.

Any other variable is named by what it records in the game: a question's answer with the answer's text, the number
the script gives the field picked in the destination map menu, or what the player did or saw when the script stored it
(the Spire Ravel trip count, the Site 9 cart stop, a device inscription read, a hunt accepted), with the bit value for a
flag bit; no zone row names a value only by the lines that store it.

A store's own tests are not repeated when the row already states them. A cell longer than 600 characters names the
stores' places only. When every value the script stores in a local or file variable fails a test, and a store without
a test sets one of them earlier in the exit's own function, that test's clause ends "so this test never passes and the
exit is never taken"; it ends "so this test always passes" when every value passes. A test the script compares with
itself is marked the same way.

Every store of each saved value a door condition tests, with that store's own condition, is in
[saved-value-stores.tsv](../World-Areas-And-Travel/saved-value-stores.tsv): a script's own variable under the script and
its listing name, an engine-held value under its block, unit and offset (a scratch1 value with its script, a scratch2
value with its area's script prefix), and a value the game's symbols name, such as `global_flag[2]`, by that name in its
`store` column. A tested value that no script stores has no rows.

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
| `script`, `script_kind` | The script, and `story` or `developer (evt_t)` |
| `function`, `line`, `value` | Where the write is and the value it stores in the main story counter |
| `lower_bound`, `upper_bound` | The counter bounds its guards admit (`-` when the guards set no bound), file-variable tests included |
| `verdict` | `raises or keeps`, `lowers`, `may lower` or `unguarded`, from the bounds |
| `guards` | The `if` and `switch` tests that hold at the write |
| `reach` | `reached` or `unreachable` |
| `read_guard`, `started_by`, `counter_range` | For the 128 reached unguarded story writes: what guards the write, what starts its function, and the counter values at which it runs; `-` for the other rows |
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
| `destination_field`, `destination_map` | The field id, or the expression the call passes, and the map or maps it reaches: for `lastmap()` the corridor that jumps into the room, for the World Map picker the 18 destinations with their entrances, for Trial Mode and `dgl_n01` the map the computed or stored value gives; for the 191 developer debug-menu rows that name no field in the call, every field the menu's answer gives, or the current field (`nowmap()`) the menu reloads |
| `entrance`, `mode` | The entrance and mode; `one of ...` when the stores do not pair them |
| `resolved_from` | `literal`, or the store lines that give the field or entrance; on those 191 rows, the question whose answer leads to the jump (its line, choice count, answers and answer test line) and the tests that bound the field. A store in another function gives a jump a row unless the jump's own function stores the variable on every path to it |
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
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md): the verbs of the last list.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x00226BD0` is called by `0x0025C830`; `0x00233D20` is called by `0x0025C830`; `0x0025C230` calls `0x003589B0`,
  `0x003DBB60`; `0x0025C230` is called by `0x0025C170`; `0x00263FF0` is called by `0x0032F1B0`, `0x0032F850`, `0x0032FA10`,
  `0x0032FAC0`, `0x0032FB70`, `0x00330060`, `0x00330110`, `0x00330190`, `0x00330220`, `0x003302B0`, `0x00330310`, `0x003304A0`.
- Actor entity: `0x00263FF0` is also called by `0x003306E0`, `0x00331610`, `0x003316B0`, `0x00331760`, `0x003317C0`, `0x00331820`,
  `0x00332130`, `0x003587C0`, `0x003588B0`, `0x0035A590`, `0x0035A7A0`, `0x0035A990`; `0x00263FF0` is also called by `0x003B6F80`,
  `0x003DB1F0`, `0x003DBCF0`, `0x003DDC20`, `0x0046BAC0`; `0x00265680` is called by `0x0025B600`, `0x00263660`, `0x0026C5D0`,
  `0x0026DFB0`; `0x002677F0` calls `0x003588B0`.
- Actor entity: `0x0026DB30` is called by `0x0026C8C0`; `0x003137E0` is called by `0x003266C0`; `0x00342490` calls `0x00263FF0`;
  `0x00343010` calls `0x00263FF0`; `0x00343470` calls `0x00263FF0`; `0x003590D0` is called by `0x0025B600`, `0x0025D9E0`,
  `0x00263050`, `0x00263230`, `0x00263AC0`, `0x00264010`, `0x00264050`, `0x0026C5D0`, `0x0026C8C0`, `0x0026DFB0`; `0x00377C20` is called
  by `0x0025C830`, `0x003266C0`.
- Actor entity: those functions are documented on [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md),
  [identifier spaces](../Engine-Core/identifier-spaces.md),
  [script requests](../Scripts-And-Script-Commands/script-requests.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md).
- Actor entity: and on [event scenes](../Scripts-And-Script-Commands/event-scenes.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md),
  [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md),
  [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md).
- Actor entity: and on [ebp lighting lgt2](../EBP-Script-Files/ebp-lighting-lgt2.md),
  [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md).
- Actor entity: and on [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md),
  [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Actor entity: and on [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md),
  [actor managers](../Characters-And-Objects/actor-managers.md), [target selection](../Battle-Actions/target-selection.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Actor entity: and on [debug menu](../Engine-Core/debug-menu.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Audio: `0x00226BD0` is called by `0x00229AF0`; `0x003590D0` is called by `0x00362850`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Combat AI: `0x00377C20` is called by `0x003014C0`, `0x00301AD0`, `0x00305AB0`; those functions are documented on
  [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [glossary](../Engine-Core/glossary.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Combat action: `0x003590D0` is called by `0x00317E60`, `0x00319090`; `0x00377C20` is called by `0x002FFA60`, `0x002FFCF0`,
  `0x002FFF50`, `0x00305110`, `0x00305230`, `0x00305430`, `0x00307300`, `0x0030C010`, `0x0030D160`, `0x0030D600`, `0x0030DA30`,
  `0x0030F760`; `0x00377C20` is also called by `0x00311B20`, `0x00311CF0`, `0x00312FA0`, `0x00313CD0`, `0x00313DB0`.
- Combat action: those functions are documented on [jump thunks](../Engine-Core/jump-thunks.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [quickenings and summons](../Battle-Actions/quickenings-and-summons.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Combat action: and on [spawn record fields](../Enemy-Spawning/spawn-record-fields.md),
  [action phases](../Battle-Actions/action-phases.md),
  [battle unit fields](../Characters-And-Objects/battle-unit-fields.md),
  [action definition row](../Battle-Actions/action-definition-row.md).
- Combat action: and on [identifier spaces](../Engine-Core/identifier-spaces.md),
  [call signatures](../Engine-Core/call-signatures.md),
  [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md).
- Combat formula: `0x00377C20` is called by `0x00300530`; those functions are documented on
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Core runtime: `0x0036FF70` is called by `0x0022A770`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Gameplay: `0x003135C0` calls `0x0030D9A0`; `0x003590D0` is called by `0x0031ADB0`; `0x00377C20` is called by `0x00307D10`,
  `0x0030A8A0`, `0x0030C210`, `0x0030D9A0`.
- Gameplay: those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [bestiary](../Enemy-Spawning/bestiary.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [enmity](../Enemy-AI-And-Gambits/enmity.md).
- Input: `0x00263FF0` is called by `0x00226BE0`, `0x002E09A0`; `0x00265680` is called by `0x00253C70`, `0x002E09A0`; `0x0034E260`
  calls `0x0036FF70`; `0x003590D0` is called by `0x00226BE0`; `0x0036FF70` is called by `0x002A28E0`; `0x00377C20` is called by
  `0x00253C70`.
- Input: those functions are documented on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [message windows](../Menus-And-HUD/message-windows.md).
- Input gameplay: `0x00377C20` is called by `0x00313A00`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Items equipment shops license: `0x00377C20` is called by `0x00309FB0`, `0x0030FD10`; those functions are documented on
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Movement: `0x00263FF0` is called by `0x002E28E0`, `0x00392740`; `0x00265680` is called by `0x0026C3E0`; `0x003135C0` is called
  by `0x0031BAC0`, `0x00338490`; `0x003590D0` is called by `0x0026C3E0`, `0x0026D6F0`, `0x0026D810`, `0x002E45E0`, `0x002E5180`,
  `0x00319490`, `0x00325D90`, `0x00326BB0`, `0x00326D60`, `0x00343E20`, `0x00345430`; `0x00377C20` is called by `0x0025B470`,
  `0x0026C3E0`, `0x002E28E0`, `0x00310920`, `0x00313670`.
- Movement: those functions are documented on
  [script binding lifecycle](../Scripts-And-Script-Commands/script-binding-lifecycle.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [game over](../World-Areas-And-Travel/game-over.md).
- Movement: and on [bestiary](../Enemy-Spawning/bestiary.md),
  [player movement](../Movement-And-Pathfinding/player-movement.md),
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [battle units](../Characters-And-Objects/battle-units.md).
- Movement: and on
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [party data](../Party/party-data.md), [party slots](../Party/party-slots.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Party: `0x00265680` is called by `0x00358CB0`, `0x00358F90`; `0x00265720` is called by `0x00358CB0`; `0x002677F0` calls
  `0x003590D0`; `0x0026DB30` calls `0x003590E0`; `0x003135C0` is called by `0x0023B040`; `0x003590D0` is called by `0x00263770`,
  `0x00269C70`, `0x00327270`, `0x003272A0`, `0x003272F0`, `0x003273B0`; `0x00377C20` is called by `0x00304180`.
- Party: those functions are documented on
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md),
  [player movement](../Movement-And-Pathfinding/player-movement.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Party: and on [script variables](../Scripts-And-Script-Commands/script-variables.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md),
  [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md),
  [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md).
- Party: and on [debug menu](../Engine-Core/debug-menu.md),
  [enemy spawning](../Enemy-Spawning/enemy-spawning.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Presentation: `0x00226BD0` is called by `0x002B7B80`; `0x00263FF0` is called by `0x003A4290`, `0x003A56F0`, `0x003DD4C0`,
  `0x00465120`, `0x00465690`; `0x00265680` is called by `0x001EC560`; `0x003590D0` is called by `0x003A4290`, `0x003A56F0`,
  `0x003F1A60`, `0x00426090`, `0x004264A0`, `0x004640A0`, `0x004643D0`, `0x00464650`, `0x00464BD0`, `0x00465120`, `0x00465690`,
  `0x0046CC70`.
- Presentation: `0x00377C20` is called by `0x00307E70`, `0x003125E0`, `0x00313B30`, `0x003714A0`; those functions are documented
  on [frame update order](../Engine-Core/frame-update-order.md),
  [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md),
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Presentation: and on [effect element runtime](../Graphics/effect-element-runtime.md),
  [effect element types](../Graphics/effect-element-types.md),
  [debug menu](../Engine-Core/debug-menu.md), [hud](../Menus-And-HUD/hud.md).
- Presentation: and on
  [authored presentation commands](../Graphics/authored-presentation-commands.md),
  [legacy ps2 gs layer](../Graphics/legacy-ps2-gs-layer.md),
  [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md).
- Presentation: and on [force fight mode](../Engine-Core/force-fight-mode.md),
  [battle units](../Characters-And-Objects/battle-units.md), [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md),
  [add motion tables](../Graphics/add-motion-tables.md).
- Rewards progression economy: `0x003135C0` is called by `0x002F8BB0`; `0x00377C20` is called by `0x00312280`; those functions
  are documented on [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md).
- Save load settings: `0x0026DB30` calls `0x002EF2B0`; `0x00314870` calls `0x002EF2B0`; those functions are documented on
  [script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md).
- Spawn encounter lifecycle: `0x00233D20` is called by `0x00307030`; those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md).
- Status periodic terminal: `0x00265680` is called by `0x00310DB0`; `0x00377C20` is called by `0x0030E360`, `0x0030F690`,
  `0x00310DB0`; those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- UI: `0x00265680` is called by `0x00279E20`; `0x002901D0` is called by `0x00550400`, `0x005528C0`; `0x003135C0` is called by
  `0x0031EB20`; `0x003590D0` is called by `0x00299BD0`, `0x002C7660`; `0x003C0250` is called by `0x002901D0`.
- UI: those functions are documented on [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md),
  [map screens](../Menus-And-HUD/map-screens.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md),
  [action definition row](../Battle-Actions/action-definition-row.md), [party list](../Menus-And-HUD/party-list.md); and on
  [battle units](../Characters-And-Objects/battle-units.md).
- World area: `0x0026DB30` is called by `0x00266D10`; `0x003590D0` is called by `0x0025E400`, `0x002623A0`; those functions are
  documented on [force fight mode](../Engine-Core/force-fight-mode.md),
  [actor record fields](../Characters-And-Objects/actor-record-fields.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- World area: `0x0026DB30` calls `0x00314870`, `0x003148D0`, `0x003148F0`, `0x003149E0`; `0x003135C0` is called by `0x00234590`;
  `0x00314870` is called by `0x0026DB30`; `0x00355680` calls `0x00377C20`; `0x00377C20` calls `0x003148F0`; `0x00377C20` is called
  by `0x002342F0`.
- World area: those functions are documented on [script variables](../Scripts-And-Script-Commands/script-variables.md),
  [party control modes](../Engine-Core/party-control-modes.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [party verbs](../Scripts-And-Script-Commands/party-verbs.md).
