[Home](../../README.md) / [Story, events and hunts](README.md) / Giruvegan scripts

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Giruvegan scripts: what each script function shows, sets, gives and starts | reference | Story, events and hunts | Scenes and scripts by area / Feywood and Giruvegan | Every function of the Giruvegan and Great Crystal zone and scene scripts that a player can observe, apart from the shared crystal and item-message actors counted per script: what triggers it, the lines it shows and who speaks them, the story flags and story counter values it sets or tests, the items it gives or takes, its map jumps, battle calls and scene loads. | 0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x00352EA0, 0x00353390, 0x00354000, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0 |

## What it lists

The table [giruvegan-scripts.tsv](giruvegan-scripts.tsv) has one row per script function of Giruvegan and the Great
Crystal that does something a player can observe. It covers the eighty-one zone scripts and the fourteen scene scripts
of the region, from `plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `gil_a01` | zone | Gate of Earth, field `686` | 33 | 145 | 8 | 5 |
| `gil_a02` | zone | Gate of Water, field `687` | 21 | 107 | 6 | 0 |
| `gil_b01` | zone | The Trimahla Water-Steps, field `690` | 40 | 139 | 13 | 1 |
| `gil_b02` | zone | The Aadha Water-Steps, field `691` | 29 | 92 | 11 | 0 |
| `gil_c01` | zone | The Haalmikah Water-Steps, field `694` | 24 | 126 | 5 | 5 |
| `gil_c02` | zone | Gate of Fire, field `695` | 32 | 130 | 10 | 0 |
| `gil_d01` | zone | Gate of Wind, field `698` | 25 | 116 | 9 | 0 |
| `gil_e01` | zone | A Prama Vikaari, field `621` | 24 | 82 | 11 | 0 |
| `gil_e02` | zone | Kabonii Jilaam Pratii'vaa, field `622` | 24 | 77 | 10 | 0 |
| `gil_e03` | zone | Kabonii Jilaam Avaa, field `623` | 24 | 77 | 10 | 0 |
| `gil_e04` | zone | Dha Vikaari Bhrum, field `624` | 22 | 74 | 9 | 0 |
| `gil_e05` | zone | Sthaana Scorpio, field `625` | 23 | 75 | 9 | 0 |
| `gil_e06` | zone | A Vikaari Dhebon, field `626` | 22 | 74 | 9 | 0 |
| `gil_f01` | zone | A Vikaari Kabonii, field `926` | 22 | 74 | 9 | 0 |
| `gil_f02` | zone | Sthaana Cancer, field `927` | 22 | 74 | 9 | 0 |
| `gil_f03` | zone | Bhrum Pis Avaa, field `928` | 25 | 78 | 10 | 0 |
| `gil_f04` | zone | Bhrum Pis Pratii, field `929` | 27 | 86 | 12 | 0 |
| `gil_f05` | zone | Dha Vikaari Trahk, field `930` | 22 | 74 | 9 | 0 |
| `gil_g01` | zone | A Vikaari Bhrum, field `332` | 28 | 108 | 11 | 0 |
| `gil_g02` | zone | Trahk Pis Praa, field `333` | 25 | 78 | 10 | 0 |
| `gil_g03` | zone | Sthaana Pisces, field `334` | 24 | 82 | 11 | 0 |
| `gil_g04` | zone | Dha Vikaari Jula, field `335` | 22 | 74 | 9 | 0 |
| `gil_g05` | zone | Trahk Jilaam Praa'dii, field `336` | 25 | 78 | 10 | 0 |
| `gil_g06` | zone | Sthaana Aries, field `337` | 28 | 80 | 9 | 0 |
| `gil_g10` | zone | Crystal Core, field `341` | 25 | 123 | 5 | 5 |
| `gil_h01` | zone | Crystal Peak, field `888` | 32 | 115 | 16 | 0 |
| `gil_i01` | zone | Dha Vikaari Kabonii, field `939` | 27 | 96 | 12 | 0 |
| `gil_i02` | zone | A Vikaari Kanbhru Ra, field `940` | 35 | 127 | 13 | 0 |
| `gil_i03` | zone | Dhebon Jilaam Praa'dii, field `941` | 29 | 98 | 12 | 0 |
| `gil_i04` | zone | Dhebon Jilaam Pratii'dii, field `942` | 29 | 98 | 12 | 0 |
| `gil_i05` | zone | Sthaana Sagittarius, field `943` | 29 | 98 | 12 | 0 |
| `gil_i06` | zone | A Vikaari Sirhru Pratii, field `944` | 29 | 98 | 12 | 0 |
| `gil_i07` | zone | A Vikaari Sirhru Praa, field `945` | 29 | 98 | 12 | 0 |
| `gil_i08` | zone | Dhebon Jilaam Avaapratii, field `946` | 32 | 103 | 14 | 0 |
| `gil_i09` | zone | A Vikaari Sirhru Si, field `947` | 36 | 105 | 12 | 0 |
| `gil_i11` | zone | Dhebon Jilaam Avaa, field `949` | 29 | 107 | 14 | 0 |
| `gil_j01` | zone | Dha Vikaari Dhebon Praa, field `952` | 28 | 97 | 12 | 0 |
| `gil_j02` | zone | Dha Vikaari Dhebon Pratii, field `953` | 28 | 97 | 12 | 0 |
| `gil_j03` | zone | Sirhru Phullam Praa, field `954` | 39 | 110 | 14 | 0 |
| `gil_j04` | zone | Sthaana Leo, field `955` | 36 | 105 | 12 | 0 |
| `gil_j05` | zone | Sirhru Phullam Praa'vaa, field `956` | 38 | 109 | 14 | 0 |
| `gil_j06` | zone | Sirhru Phullam Pratii'vaa, field `957` | 38 | 109 | 14 | 0 |
| `gil_j07` | zone | Sthaana Gemini, field `958` | 36 | 105 | 12 | 0 |
| `gil_j08` | zone | Sirhru Phullam Udiipratii, field `959` | 39 | 110 | 14 | 0 |
| `gil_j09` | zone | Sirhru Jilaam Praa'dii, field `960` | 25 | 94 | 12 | 0 |
| `gil_j10` | zone | Sirhru Jilaam Pratii'dii, field `961` | 25 | 94 | 12 | 0 |
| `gil_j11` | zone | Sirhru Jilaam Praa, field `962` | 26 | 95 | 12 | 0 |
| `gil_j12` | zone | Sirhru Jilaam Pratii, field `963` | 26 | 95 | 12 | 0 |
| `gil_j13` | zone | Sirhru Jilaam Praa'vaa, field `964` | 30 | 101 | 14 | 0 |
| `gil_j14` | zone | Sirhru Jilaam Pratii'vaa, field `965` | 30 | 101 | 14 | 0 |
| `gil_j15` | zone | Sirhru Pis Praa, field `966` | 26 | 95 | 12 | 0 |
| `gil_j16` | zone | Sirhru Pis Pratii, field `967` | 26 | 95 | 12 | 0 |
| `gil_j17` | zone | Sirhru Pis Avaa, field `968` | 25 | 94 | 12 | 0 |
| `gil_j18` | zone | Sirhru Jilaam Avaapratii, field `969` | 25 | 94 | 12 | 0 |
| `gil_j19` | zone | Sirhru Jilaam Avaapraa, field `970` | 25 | 94 | 12 | 0 |
| `gil_j20` | zone | A Vikaari Uldobi, field `971` | 28 | 97 | 12 | 0 |
| `gil_j21` | zone | A Vikaari Uldobi Si, field `972` | 36 | 105 | 12 | 0 |
| `gil_j22` | zone | Dha Vikaari Dhebon Si, field `973` | 36 | 105 | 12 | 0 |
| `gil_k01` | zone | Dha Vikaari Sirhru, field `979` | 29 | 98 | 12 | 0 |
| `gil_k02` | zone | Sthaana Virgo, field `980` | 27 | 96 | 12 | 0 |
| `gil_k03` | zone | Uldobi Jilaam Praa'dii, field `981` | 25 | 94 | 12 | 0 |
| `gil_k04` | zone | Uldobi Jilaam Pratii, field `982` | 25 | 94 | 12 | 0 |
| `gil_k05` | zone | Uldobi Jilaam Praa, field `983` | 25 | 94 | 12 | 0 |
| `gil_k06` | zone | Uldobi Phullam Pratii'dii, field `984` | 34 | 105 | 14 | 0 |
| `gil_k07` | zone | Sthaana Capricorn, field `985` | 27 | 96 | 12 | 0 |
| `gil_k08` | zone | Dha Vikaari Sirhru Si, field `986` | 32 | 101 | 12 | 0 |
| `gil_k09` | zone | Uldobi Phullam Udiipraa, field `987` | 28 | 99 | 14 | 0 |
| `gil_k10` | zone | Uldobi Phullam Pratii'vaa, field `988` | 27 | 96 | 12 | 0 |
| `gil_k11` | zone | Uldobi Phullam Praa'vaa, field `989` | 26 | 95 | 12 | 0 |
| `gil_k12` | zone | Uldobi Phullam Pratii, field `990` | 27 | 98 | 14 | 0 |
| `gil_k13` | zone | Sthaana Taurus, field `991` | 28 | 97 | 12 | 0 |
| `gil_k14` | zone | Sthaana Libra, field `992` | 26 | 95 | 12 | 0 |
| `gil_k15` | zone | Uldobi Jilaam Praa'vaa, field `993` | 27 | 96 | 12 | 0 |
| `gil_k16` | zone | Uldobi Jilaam Pratii'vaa, field `994` | 27 | 96 | 12 | 0 |
| `gil_k17` | zone | Uldobi Jilaam Avaa, field `995` | 25 | 94 | 12 | 0 |
| `gil_k18` | zone | A Vikaari Kanbhru, field `996` | 29 | 98 | 12 | 0 |
| `gil_l01` | zone | Dha Vikaari Uldobi, field `1002` | 32 | 101 | 12 | 0 |
| `gil_l02` | zone | Kanbhru Pis, field `1003` | 30 | 125 | 13 | 5 |
| `gil_l03` | zone | Dha Vikaari Dhebon Ra, field `1004` | 32 | 101 | 12 | 0 |
| `gil_l04` | zone | Sthaana Aquarius, field `1005` | 32 | 101 | 12 | 0 |
| `gil_z01` | zone | Siti Bhrusuna, field `916` | 7 | 13 | 3 | 0 |
| `gil_a0100` | scene | event `207` | 22 | 138 | 6 | 0 |
| `gil_a0200` | scene | event `143` | 15 | 98 | 0 | 0 |
| `gil_a0201` | scene | event `144` | 15 | 55 | 0 | 0 |
| `gil_c0100` | scene | event `208` | 19 | 112 | 6 | 0 |
| `gil_c0200` | scene | event `145` | 14 | 70 | 0 | 0 |
| `gil_c0201` | scene | event `146` | 15 | 71 | 0 | 0 |
| `gil_d0100` | scene | event `147` | 14 | 80 | 0 | 0 |
| `gil_d0101` | scene | event `148` | 17 | 69 | 13 | 0 |
| `gil_d0102` | scene | event `229` | 18 | 105 | 5 | 0 |
| `gil_g1000` | scene | event `209` | 19 | 118 | 6 | 0 |
| `gil_h0100` | scene | event `149` | 15 | 82 | 0 | 0 |
| `gil_h0101` | scene | event `205` | 17 | 106 | 14 | 0 |
| `gil_i1000` | scene | event `174` | 14 | 66 | 0 | 0 |
| `gil_z0100` | scene | event `206` | 28 | 419 | 45 | 0 |

Gate of Earth, The Haalmikah Water-Steps, Crystal Core and Kanbhru Pis carry the five helper actors that many zone
scripts share: the crystal (`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the
key-item and message helper `イベント特殊効果画面`.

The Trimahla Water-Steps carries the key-item and message helper alone. Their functions are described once on [Shared
zone-script actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Giruvegan
scenes](giruvegan-scenes.md).

### What the scripts do

- Gate of Earth: below story counter 4250, `EventDirector.main` plays scene `gil_a0100` (event 207) and writes 4250;
  on that arrival by entrance 4, the one The Edge of Reason (The Feywood) jumps to, it also sets flag `0x002A`, the
  location map's exits between Giruvegan and The Feywood. `Map_Director.init` releases flag `0x00C6`, a map icon in
  The Edge of Reason.
- Gate of Earth holds the crystal. The gate (`gil_gate`) leads to The Edge of Reason (The Feywood), field 550, and the
  device ("Magicks stir within this device.") to Gate of Water, field 687: `gil0101_warp` below story counter 5000,
  `gil0101_warp_b` from 5000.
- Gate of Water: below story counter 4300, `EventDirector.main` loads and plays scenes `gil_a0200` (event 143) and
  `gil_a0201` (event 144) and shows the boss gauge; while `g_btl_ダイダロス` is 1 and the counter is below 4295,
  `ボス登場.main` writes 4295, the value at which Daedalus appears.
- Gate of Water: touching `ボス登場` starts the fight; when it ends it removes every foe, loads the victory pose scene
  `pos_z0000` (event 427, [Victory pose scenes](victory-pose-scenes.md)), sets `g_btl_ダイダロス` to 2 and writes 4300, the
  value after the Daedalus battle. Its devices lead to Gate of Earth, field 686 (`gil0102_warp`), and The Trimahla
  Water-Steps, field 690 (`gil0102_warp_flg`).
- The Trimahla Water-Steps: two barriers (`gil_magic01`, `gil_magic02`) read "A barrier of powerful magicks prevents
  passage. There might be a mechanism to lower the barrier elsewhere." Each stone (`gil_switch01`, `gil_switch02`:
  "Ancient beyond reckoning, the device still functions.") opens or closes its barrier when touched, and does not
  respond while allies are near the gate.
- The Trimahla Water-Steps: the device `gil_warp01` leads to Gate of Water, field 687. Talking to `ロケ地図` gives the
  area map, Giruvegan, with system message 110 ("Your location map for this area is complete!").
- The Aadha Water-Steps: three barriers (`gil_maパレルトン`, `gil_maパロン`, `gil_maメッロン`) and their stones work in the same
  way. The first of `gil_swパロン` and `gil_swパレルトン` to open its barrier keeps it open: that stone then answers only "The
  device sleeps."
- Giruvegan: the devices and stones set map-icon flags: `0x00D0` (Gate of Earth), `0x00D1` and `0x00D2` (Gate of
  Water), `0x00D3` to `0x00D5` (The Trimahla Water-Steps), `0x00D6` to `0x00D8` (The Aadha Water-Steps), `0x011A`
  (Gate of Fire), and `0x00D9` and `0x00DA` (Gate of Wind).
- The Haalmikah Water-Steps: below story counter 4320, `EventDirector.main` plays scene `gil_c0100` (event 208) and
  writes 4320. The Haalmikah Water-Steps hold the crystal; the door `gil_door02` leads to Gate of Fire, field 695.
- Gate of Fire: below story counter 4350, while `g_btl_タイラント` is 1, `EventDirector.main` loads and plays scenes
  `gil_c0200` (event 145) and `gil_c0201` (event 146) and shows the boss gauge; touching `ボス登場` starts the fight, and
  when it ends removes every foe, loads `pos_z0000` (event 427), sets `g_btl_タイラント` to 2 and writes 4350, the value
  after the Tyrant battle.
- Gate of Fire: when the `g_btl_nm_ピスコディーモン` fight ends, `wanted_kansi.main` removes the foes of a group. The device
  `gil0204_warp_flg` leads to A Prama Vikaari (The Great Crystal), field 621, and the door `gil_door01` to The
  Haalmikah Water-Steps, field 694.
- Gate of Wind: below story counter 5000, while `g_btl_シュミハザ` is 1, `EventDirector.main` loads and plays scenes
  `gil_d0100` (event 147) and `gil_d0101` (event 148); `ボス登場.main` shows the boss gauge and, when the fight ends,
  removes every foe, loads `pos_z0000` (event 427), sets `g_btl_シュミハザ` to 2 and writes 4400, the value after the
  Shemhazai battle.
- Gate of Wind: from story counter 5000 to 5099, `EventDirector.main` plays scene `gil_d0102` (event 229) and writes
  5100. The device `gil_warp01` leads to Crystal Core (The Great Crystal), field 341.
- Gate of Wind: below story counter 5000 the device `gil_warp02` first shows "The device bears a timeworn
  inscription."; once the inscription ("By this path, and no other, reach ye the Round of the Undying, walk of the
  Chosen.") has been read, "Touch the device." jumps to Siti Bhrusuna, field 916.
- Gate of Wind: from story counter 5000 the device `gil_warp02b` takes its place ("By this, return ye to the Gate of
  Earth. By other means, return ye back to this place.") and leads to Gate of Earth, field 686.
- The Great Crystal: every room's `Map_Director.init` releases flags `0x00FD` to `0x0103` and sets the one for its own
  fields: `0x0101` for fields 621 to 629, `0x0102` for 926 to 932, `0x0103` for 332 to 341, `0x0100` for 939 to 951,
  `0x00FF` for 952 to 978, `0x00FE` for 979 to 1001, and `0x00FD` for 888 and 1002 to 1007. Gate of Fire and Gate of
  Wind release all seven.
- The Great Crystal: the waystones (`warp`, `warp_up`: "Magicks stir within this device.") jump to the field the
  room's director stores. In A Vikaari Kanbhru Ra (field 940) the waystone answers "Nothing happens. There must be a
  corresponding device elsewhere." until the one in Dha Vikaari Dhebon Ra (field 1004) has been used.
- The Great Crystal: in Sthaana Scorpio, Sthaana Cancer, Sthaana Pisces and Sthaana Aries (fields 625, 927, 334 and
  337) a device (`magic_switch`) raises or lowers barriers (`gil_magicwall_1st`, `gil_magicwall_2nd`: "A barrier of
  powerful magicks prevents passage. There might be a mechanism to lower the barrier elsewhere.", "The shimmering gate
  beckons you.") each time it is touched.
- Sthaana Scorpio: below story counter 5000 its device shows "This device has not stirred for long ages." and,
  touched, "The device does not respond, but voiceless words chime within your head: 'For my master's chosen, and no
  other, the way will I lay open.'" without working; from 5000 it shows "The device wakens in presence of the
  Treaty-Blade." once and works from then on.
- Crystal Core: below story counter 4370, `EventDirector.main` plays scene `gil_g1000` (event 209) and writes 4370.
  Crystal Core holds the crystal; its devices lead to Dha Vikaari Jula, field 335 (`warp0`), and Gate of Wind
  (Giruvegan), field 698 (`warp1`).
- Crystal Peak: while `g_btl_アルテマ` is 1, `EventDirector.main` loads and plays scenes `gil_h0100` (event 149) and
  `gil_h0101` (event 205) and shows the boss gauge; touching `ボス登場` starts the fight, and when it ends removes every
  foe, loads `pos_z0000` (event 427) and sets `g_btl_アルテマ` to 2.
- The Great Crystal: touching the device (`magic_switch_up`) in Sthaana Sagittarius, Sthaana Leo, Sthaana Gemini,
  Sthaana Virgo, Sthaana Capricorn, Sthaana Taurus, Sthaana Libra or Sthaana Aquarius starts a gauge timer, set to 72
  in Sthaana Sagittarius and Sthaana Libra, 108 in Sthaana Virgo, 144 in Sthaana Gemini, 180 in Sthaana Capricorn, 216
  in Sthaana Leo, 252 in Sthaana Taurus and 288 in Sthaana Aquarius.
- The Great Crystal: while a timer runs, these devices answer "Ancient beyond reckoning, it looks as though the
  slightest touch might bring the device to a halt." When the timer reaches 0, `gil_timer.main` sets
  `mp_gil_c_magicf_ctrl` to 0 and, in the rooms it lists, requests `map_timer_off` of the barriers
  (`gil_magicwall_1st`, `gil_magicwall_2nd`).
- A Vikaari Kanbhru Ra: `hunt_kansi.main` gives the Skull Trophy and removes the foes of a group.
- Dhebon Jilaam Avaa: while `g_btl_オメガ` is 1, `EventDirector.main` loads and starts scene `gil_i1000` (event 174) and
  shows the boss gauge; a running device timer stops for the fight. When the fight ends it removes every foe, loads
  `pos_z0000` (event 427), sets `g_btl_オメガ` to 2 and starts the timer again.
- Kanbhru Pis holds the crystal.
- Siti Bhrusuna: `常駐監督.main` restores the party, plays scene `gil_z0100` (event 206), whose own functions give the
  Treaty-Blade, writes 5000 and jumps to `alc_z03` (Archades), field 868.
- The Trimahla Water-Steps holds 5 treasure chests.
- The Aadha Water-Steps and Gate of Fire hold 3 treasure chests each.
- Gate of Wind, Crystal Peak, Dhebon Jilaam Avaapratii, Sirhru Phullam Praa, Sirhru Phullam Praa'vaa, Sirhru Phullam
  Pratii'vaa, Sirhru Phullam Udiipratii, Sirhru Jilaam Praa'vaa, Sirhru Jilaam Pratii'vaa, Uldobi Phullam Pratii'dii,
  Uldobi Phullam Udiipraa and Uldobi Phullam Pratii hold 2 treasure chests each.
- The Haalmikah Water-Steps, Kabonii Jilaam Pratii'vaa, Kabonii Jilaam Avaa, Bhrum Pis Avaa, Bhrum Pis Pratii, Trahk
  Pis Praa and Trahk Jilaam Praa'dii hold 1 treasure chest each.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settreasureflag`, `releasetreasureflag`, `istreasureflag` | `0x3F1`, `0x3F2`, `0x3F5` | `0x00352EA0`, `0x00353390`, `0x00354000` | `flags_*` | `Bank512, second half` flag ([story flag ids](story-flag-ids.md)) |
| `mapjump` | `0x08D` | `0x00354D00` | `jumps` | field, entrance, mode ([zone changes](../World-Areas-And-Travel/zone-changes-and-mapjump.md)) |
| `eventread`, `eventread_e8` | `0x0E7`, `0x0E8` | `0x003529E0`, `0x00351880` | `scenes` | the event id, the first or second argument ([event scenes](../Scripts-And-Script-Commands/event-scenes.md)) |
| `additem`, `additem_47f`, `additemmes`, `subitem` | `0x2E5`, `0x47F`, `0x480`, `0x2F2` | `0x00345080`, `0x003449A0`, `0x0034A6D0`, `0x003459C0` | `items` | item id and count ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)) |
| `giveback_item_and_equip`, `talktreasure` | `0x387`, `0x2BF` | `0x0034A790`, `0x00355830` | `items` | the saved items and equipment back; a treasure chest |
| `bossgaugeopen` | `0x3CA` | `0x00349B60` | `battles` | the boss gauge ([battle menu](../Menus-And-HUD/battle-menu.md)) |
| `bosskillall`, `zakokillall` | `0x3B8`, `0x3A8` | `0x00510840`, `0x00353770` | `battles` | removes the foes ([boss fights](../Battle-Actions/boss-fights.md)) |
| `addpartymember`, `setbattlemember` | `0x353`, `0x355` | `0x0034C030`, `0x0034D4E0` | `party` | party row selectors ([party verbs](../Scripts-And-Script-Commands/party-verbs.md)) |

The story counter is the script's global `short` at offset 0, named `シナリオフラグ` in the scripts of this table that write
or test it: every assignment to it is a write and every comparison a test ([story counter
values](story-counter-values.md)).

### The four message verbs reach one window call

The four message verbs all end in `mes` (`0x461`, `0x00348DF0`), which looks the text id up in the issuing script's
section 2 ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)):

| Step | What happens | Where in the code |
|---|---|---|
| 1 | `amese` pushes 0, 0, 0 and -1; `amest` pushes 0; `ames` pushes 1. Each then jumps to `0x00349800`, the body of `ames_1fe`. | `0x0034A420`<br>`0x0034A090`<br>`0x00349BF0` |
| 2 | `0x00349800` pops two values, pushes 0 and 0 and then pushes the two values back in their original order, so the zeros lie beneath them; it jumps to `0x00348DF0`. | `0x00349827`, `0x00349831`<br>`0x0034983D`, `0x00349847`<br>`0x00349851`, `0x0034985B`<br>`0x00349884` |
| 3 | `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context to `0x00264D60`, the section 2 lookup, which keeps the low 24 bits of the id. | `0x00348E6A`-`0x00348E74` |
| 4 | `0x00348DF0` reads the entry's flag through `0x002673A0`, bit `0x1` of the entry's upper half, and opens the window through `0x002E16B0` only when that flag is clear. With the flag set it still makes its six slot calls and fills the call record but opens no window ([EBP text sections](../EBP-Script-Files/ebp-text-sections.md)). | `0x00348E85`<br>`0x00348EE0`-`0x00348EFF`<br>`0x00348E91`-`0x00348ECA`<br>`0x00348ED7`-`0x00348EDC` |

### Speakers, places and scenes

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
 ¹: the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- `0x00348DF0` makes that `0x002E16B0` call only for a line whose section 2 flag is clear²; for a flagged
  line it opens no window, so the actor's name flag is not set there.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes³, so its `{actor-name}` header shows no name; that line reads
  `no name shown`. A system message reads `system message`.
- A line whose text carries no name takes the window actor's `setnpcname` name. Failing that, a scene subtitle
  (centred, or in the subtitle font `{alt-font}`) takes the character the window speaks for.
- Then any line without a name takes the speaker of the voice cue joined to it ([Voices](../Sound-And-Music/voices.md)),
  else the actor of the row's `TAGmes_<actor>_<n>` function, else the actor whose mouth function (`paku_on`,
  `unapaku_on`, `クチウナオン`, `kutipaku_on`, `kutipakuON`) is requested in its window or around the request of its
  function.
- A scene subtitle these steps leave without a speaker takes the speaker of the one voice cue that starts on the frame
  the subtitle opens or within 10 frames after, else of the one speaker whose cues play through at least half the
  frames it is shown while no other speaker's cues play through more than a fifth. Every showing of the line must give
  the same speaker, and a subtitle of two speakers, which starts `- `, takes no speaker by this step.
- The frames are those of the clock of [Voices](../Sound-And-Music/voices.md) ("How a cue is joined to its line"), which
  runs every function of the scene, one that no other function starts on a clock of its own. A variable keeps the
  value its declaration or its last store gives.
- Each case of a `switch` on a value the run cannot know runs on a clock of its own, a `sysReqwait` for a function
  another function requested waits for the end of that request, and a line stays shown until the next message call or
  `mesclose` on its window.
- A cue whose `speaker` cell names no actor takes the character its sound code belongs to, the letters after the
  number in its `sound` name ([Voices](../Sound-And-Music/voices.md)), when three or more cues with that code name a
  speaker and three quarters of them or more name that one character.
- A cue whose sound code belongs to another character than its speaker plays through another actor's slot, so it names
  no speaker by these two steps, unless the two characters share a party model. A line shown on a movie's frames takes
  no cue's speaker: its function, or each function that requests it, waits on `getmovieframe` before showing it.
- A character's game name is the second name its `setnpcname` gives; else the party member whose model its bind verbs
  name, the `c` entries of the script's [actor manifest](../EBP-Script-Files/ebp-actor-manifest.md) read
  against the `model` column of the [party table](../Party/party-table.md), a main member before a guest; else
  the NPC name or string table row whose `in` cell is the actor's name.
- The actor `REX` of `naf_a0100`, `naf_b0100`, `naf_b0400` and `naf_b0401` (`Rex` in `naf_a0201`) has no `c`
  entry. Its bind verb names a `C` entry, a high-detail model, `high/c10/c1025/hc1025_02` (`hc1025_01` in
  `naf_a0201`); `chara/c10/c1025/c1025` is model `c15`, and row 6 of the party table, model `c15`, is Reks, the
  name the rows of these scenes give that actor.
- An actor these steps leave unnamed whose bind verbs name one `n` entry of the manifest takes the name the game
  gives the other actors bound to that `n` model, by these steps or as a voice cue's speaker
  ([Voices](../Sound-And-Music/voices.md)), when they all give one name and two or more actors give it or the bestiary
  gives the same.
- Failing that, it takes the [bestiary](../Enemy-Spawning/bestiary.md) name of that model id (its
  `model_id` cell), when the bestiary gives it one name. A `c` model is left out of these two steps, since the
  bestiary can name a battle alias there: Amalia for Ashe's `c11`.
- An actor these steps leave unnamed whose only body is `capturepc(-1)`, the character the player controls, speaks as
  Reks in a scene each of whose loading steps runs while the story counter is below 25: until then the party is
  [scenario preset](../Party/scenario-presets.md) 0, Reks alone, and the
  [party table](../Party/party-table.md) gives no join below 25.
- Failing that, an actor every one of whose voice cues in the scene carries a sound code that belongs to one
  character, by the sound-code step above, takes that character's name. An actor bound to a `c` model is left out of
  this step, since two party rows can share one: Larsa and Lamont share `c16`.
- An actor bound to `c16` is the guest row its `capturebattleid` names; else the one `c16` guest the party holds at
  every story counter value the scene's loading steps allow, by the joins and leaves of the
  [party table](../Party/party-table.md): Lamont (row 10) from story progress 546 until 645, Larsa (row 13) from
  story progress 1640 until 2000. Any other `c16` actor reads its label, as below.
- Any other line without a name reads `no name shown`. A scene subtitle shows no name on screen, so its cell gives
  what the data holds: `movie subtitle` for a line shown on a movie's frames; for a line whose voice cue's actor has
  no game name, that actor's label as the script writes it, marked `(script label)`; else `no name shown`.
- A Japanese label carries an English gloss after a comma: the game's own English name where its text has one, as
  `グラミス (script label, Gramis)`, by line 19 of `alc_z0101` in
  [Archades dialogue](../Menus-And-HUD/archades-dialogue.md); else a plain translation, as
  `平ジャッジ (script label, rank-and-file Judge)`, or a plain reading of an abbreviation the text does not spell out.
- A line whose name is `???` reads `???`: the game prints `???` as that speaker's name at that line. A row lists its
  speakers in line order, each once.
- A field id is named by its map name, entry `id` of `us` `planmapname.bin`⁴, and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin`⁵.
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ADDAA`, `0x002B16D4`, `0x002B52EF` |
| ² | `0x00348EE0` |
| ³ | `0x0026668B`, `0x0026669B`-`0x002666B4` |
| ⁴ | `0x00377B60` |
| ⁵ | `0x00264F90` |

</details>

### Every step

The steps table has one row for each step of every function of the ninety-five scripts, in the order the function runs
them: each call, request, store, branch, loop, case and return. It has 621,315 rows. That leaves out the 1,719
functions in the spawn groups of the scripts' foes (entry, spawn and respawn);
[Bestiary](../Enemy-Spawning/bestiary.md) reads their entry functions as enemy placements. The rows
are in four files split between scripts:

| File | Scripts | Steps |
|---|---|---:|
| [`giruvegan-script-steps-1.tsv`](giruvegan-script-steps-1.tsv) | `gil_a01` to `gil_i09` | 189,120 |
| [`giruvegan-script-steps-2.tsv`](giruvegan-script-steps-2.tsv) | `gil_i11` to `gil_j19` | 184,644 |
| [`giruvegan-script-steps-3.tsv`](giruvegan-script-steps-3.tsv) | `gil_j20` to `gil_k17` | 184,086 |
| [`giruvegan-script-steps-4.tsv`](giruvegan-script-steps-4.tsv) | `gil_k18` to `gil_z0100` | 63,465 |

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `gil_a01` | 1,203 | `gil_j12` | 9,187 |
| `gil_a02` | 1,476 | `gil_j13` | 9,242 |
| `gil_b01` | 1,313 | `gil_j14` | 9,242 |
| `gil_b02` | 1,056 | `gil_j15` | 9,187 |
| `gil_c01` | 1,809 | `gil_j16` | 9,187 |
| `gil_c02` | 2,443 | `gil_j17` | 9,182 |
| `gil_d01` | 1,674 | `gil_j18` | 9,182 |
| `gil_e01` | 5,509 | `gil_j19` | 9,182 |
| `gil_e02` | 5,049 | `gil_j20` | 9,199 |
| `gil_e03` | 5,049 | `gil_j21` | 9,240 |
| `gil_e04` | 5,023 | `gil_j22` | 9,240 |
| `gil_e05` | 5,026 | `gil_k01` | 9,205 |
| `gil_e06` | 5,025 | `gil_k02` | 9,192 |
| `gil_f01` | 5,025 | `gil_k03` | 9,182 |
| `gil_f02` | 5,022 | `gil_k04` | 9,182 |
| `gil_f03` | 5,054 | `gil_k05` | 9,182 |
| `gil_f04` | 5,536 | `gil_k06` | 9,265 |
| `gil_f05` | 5,023 | `gil_k07` | 9,192 |
| `gil_g01` | 6,639 | `gil_k08` | 9,220 |
| `gil_g02` | 5,054 | `gil_k09` | 9,232 |
| `gil_g03` | 5,504 | `gil_k10` | 9,192 |
| `gil_g04` | 5,026 | `gil_k11` | 9,187 |
| `gil_g05` | 5,054 | `gil_k12` | 9,226 |
| `gil_g06` | 5,053 | `gil_k13` | 9,197 |
| `gil_g10` | 2,043 | `gil_k14` | 9,187 |
| `gil_h01` | 3,346 | `gil_k15` | 9,192 |
| `gil_i01` | 9,193 | `gil_k16` | 9,192 |
| `gil_i02` | 10,380 | `gil_k17` | 9,182 |
| `gil_i03` | 9,206 | `gil_k18` | 9,205 |
| `gil_i04` | 9,206 | `gil_l01` | 9,202 |
| `gil_i05` | 9,205 | `gil_l02` | 9,230 |
| `gil_i06` | 9,202 | `gil_l03` | 9,202 |
| `gil_i07` | 9,202 | `gil_l04` | 9,202 |
| `gil_i08` | 9,252 | `gil_z01` | 119 |
| `gil_i09` | 9,240 | `gil_a0100` | 1,706 |
| `gil_i11` | 9,480 | `gil_a0200` | 1,129 |
| `gil_j01` | 9,199 | `gil_a0201` | 612 |
| `gil_j02` | 9,199 | `gil_c0100` | 1,149 |
| `gil_j03` | 9,289 | `gil_c0200` | 573 |
| `gil_j04` | 9,239 | `gil_c0201` | 655 |
| `gil_j05` | 9,284 | `gil_d0100` | 1,261 |
| `gil_j06` | 9,284 | `gil_d0101` | 906 |
| `gil_j07` | 9,239 | `gil_d0102` | 719 |
| `gil_j08` | 9,289 | `gil_g1000` | 913 |
| `gil_j09` | 9,182 | `gil_h0100` | 574 |
| `gil_j10` | 9,182 | `gil_h0101` | 999 |
| `gil_j11` | 9,187 | `gil_i1000` | 739 |
| | | `gil_z0100` | 5,370 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Giruvegan has 126 such rows.

Some actors run another actor's code: `PlayerJack1` in `gil_a01` starts at the same place as `PlayerJack0` and runs
the same functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 33 of these
rows: 3 in `gil_a01`, 3 in `gil_a02`, 3 in `gil_b01`, 3 in `gil_c01`, 3 in `gil_c02`, 3 in `gil_d01`, 3 in `gil_g01`,
3 in `gil_g10`, 3 in `gil_h01`, 3 in `gil_i02` and 3 in `gil_i11`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 620,677 |
| empty | 638 |

A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the arguments as the
script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry what they give
for the step, for example the variable that holds the standard motion `stdmotionplay` plays, or the variable that
receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `gil_a0100` (event `207`), `古代都市ギルヴェガンへ.main` files
`ＢＧＭ.ＢＧＭ準備` and `常駐モーション.破棄`, waiting until each ends. It reads motions 1 and 4 of `gil_a0100.mot` and event sound
slot 0, waiting for each, waits for effect slot 0, hides the party and files `取得` on seven actors from `ヴァン` to `ラスラ`,
waiting for all seven. It then starts scene cuts 1 to 6, 106, 8 and 9 in turn, filing the matching `カット` function at
each and waiting until it ends.

## Columns

| Column | Meaning |
|---|---|
| `script` | the script, by its file name |
| `place` | for a zone script, its map (region); for a scene script, `scene, event` and its event id |
| `actor`, `function` | the actor and the function, as the script names them |
| `trigger` | the function's slot (`talk`, `touch`, `touchon`, `across`, `main`, `mapjump`), `init`, or `requested by` and the functions of the same script that request it by name; `-` when neither applies |
| `speaker` | for an actor with a `setnpcname` call, the second names of its pairs; for any other row with a section 2 line, who speaks each line, in line order, by the rules under "Speakers, places and scenes": a name, `???`, `no name shown`, `system message`, `movie subtitle`, or an actor's label marked `(script label)`; `-` for a row without a section 2 line |
| `lines` | the section 2 entries the function passes to the message verbs, and `system message N` for each message from the shared system-message list that the key-item and system-message helper shows for the function ([Shared zone-script actors](shared-zone-script-actors.md)), at the place of the request; two numbers joined by `or` are the values the function's stores leave, and which one is shown is decided at run time |
| `line_text` | the `us` text of those entries, in the same order, separated by ` / `; for a `system message N` entry, the text of message N in the system-message list |
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank512, second half` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `treasure chest` and its record reference for a chest; `the item held in` and the variable for an item a variable holds; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | `boss gauge shown`, `every foe in a group removed`, `every foe in group 0 removed` |
| `scenes` | each scene script the function loads, with its event id |
| `party` | not used by these scripts: `-` on every row |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [giruvegan-script-list.tsv](giruvegan-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table, in four files ([`giruvegan-script-steps-1.tsv`](giruvegan-script-steps-1.tsv),
[`giruvegan-script-steps-2.tsv`](giruvegan-script-steps-2.tsv),
[`giruvegan-script-steps-3.tsv`](giruvegan-script-steps-3.tsv) and
[`giruvegan-script-steps-4.tsv`](giruvegan-script-steps-4.tsv)), has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. A case whose values meet an earlier case's is followed by `not (x = w)` for each such earlier case `w`, so the cell names only the values the case runs on: `x = lte(78); not (x = lt(78))` runs when x is 78. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. When such a way passes a case that an earlier case overlaps, the item counts only the values that case takes: after `case lt(0x0177)`, a `case lt(0x0182)` that returns gives the item `not (x = lt(0x0182)) or x = lt(0x0177)`, which holds unless 0x0177 <= x < 0x0182. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets, and, for a case whose every value an earlier case already matches, on the case values |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

In `arguments` and `condition`, `bitor`, `or` and `and` stand for the listing's `|`, `||` and `&&`. A comparison
`A == B` that is an operand of `bitor` is written in brackets, `(A == B) bitor (C == D)`, because the script evaluates
the comparison first.

The shared steps table [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv) has the same columns from `at`
on, after these:

| Column | Meaning |
|---|---|
| `template` | the template id that the `shared template` rows name |
| `actor`, `function`, `step` | the shared actor, its function and the step number |
| `reference` | the script whose copy of the function the steps were read from, and where the function starts there |

In this table, `at` is the step's distance from the function's start, written `+0x..`. Variable names, text ids,
section 3 string offsets and the lines `addresses` names are those of the script named in `reference`. The other
scripts' copies differ only in these.

## Related

- [Shared zone-script actors](shared-zone-script-actors.md) - the crystal, the teleport and the key-item and message actors, described once.
- [Giruvegan scenes](giruvegan-scenes.md) - the fourteen scenes these scripts own.
- [Victory pose scenes](victory-pose-scenes.md) - the scene that follows a boss fight.
- [Feywood scripts](feywood-scripts.md) - the region beyond the gate of the Gate of Earth.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 121 calls with 22 other topics</summary>

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md), [frame update order](../Engine-Core/frame-update-order.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [npc names](../Characters-And-Objects/npc-names.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [party during scenes](../Scripts-And-Script-Commands/party-during-scenes.md), [script requests](../Scripts-And-Script-Commands/script-requests.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md), [reward verbs](../Scripts-And-Script-Commands/reward-verbs.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265B60`](../Characters-And-Objects/actor-record.md) (on actor record) |
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | calls | [`0x00358940`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor manager: get record by ordinal (on party during scenes) |
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x0025C230`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x00268D10`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x00272CB0`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen)<br>[`0x00272CE0`](../Characters-And-Objects/npc-names.md) (on npc names) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00266AD0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x00266BD0`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x00268EA0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DB280`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x003DB580`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003DBB60`](../Scripts-And-Script-Commands/script-requests.md) (on script requests) |
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | is called by | [`0x002679F0`](../EBP-Script-Files/ebp-script-image.md) Actor storage: allocate and initialize records (on ebp script image) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002628B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032ED80`](../EBP-Script-Files/ebp-camera-shake.md) (on ebp camera shake)<br>[`0x00330310`](../EBP-Script-Files/ebp-script-container.md) Actor resource: begin primary payload load (on ebp script container)<br>[`0x003306E0`](../EBP-Script-Files/atel-debug-companions.md) (on atel debug companions) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x0025D5E0`](../Scripts-And-Script-Commands/script-requests.md) (on script requests)<br>[`0x003588B0`](../Menus-And-HUD/map-screens.md) Actor handle: resolve registry entry by packed id (on map screens) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00229EA0`](../Graphics/effect-drawing.md) (on effect drawing) |

**Movement and pathfinding** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record) | calls | [`0x00265FF0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x00268380`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x0026D6D0`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |

**Party** (explained on [debug menu](../Engine-Core/debug-menu.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [party control modes](../Engine-Core/party-control-modes.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | calls | [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list)<br>[`0x0026DC40`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes)<br>[`0x003271D0`](../Scripts-And-Script-Commands/party-verbs.md) Party focus: get preferred definition selector (on party verbs)<br>[`0x00327850`](../Party/party-leader.md) Party focus: set preferred definition selector and refresh (on party leader)<br>[`0x00328DB0`](../Party/party-members.md) Party configuration: reconcile runtime roster first three from requested selectors (on party members)<br>[`0x00359C00`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x0035A050`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003601B0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |

**Graphics** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x002639E0`](../Menus-And-HUD/text-npc-names.md) (on text npc names) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x002BAF80`](../Menus-And-HUD/widgets.md) (on widgets) |
| [`0x003FFB00`](archades-scripts.md) (on archades scripts) | is called by | [`0x002B0280`](../Menus-And-HUD/text-drawing.md) (on text drawing) |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | calls | [`0x002DF980`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes)<br>[`0x0032E400`](../Graphics/effect-file-list.md) (on effect file list)<br>[`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x001D6A70`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) |

**Saving, loading and settings** (explained on [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00583D60`](../Saving-Loading-And-Settings/save-file-format.md) Save image: finalize header and checksum (on save file format) |

**Scripts and script commands** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [native commands](../Scripts-And-Script-Commands/native-commands.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md), [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | calls | [`0x003DC240`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003DC270`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch)<br>[`0x003DC2A0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x002621D0`](../Scripts-And-Script-Commands/script-interpreter.md) Vm native command: execute lifecycle (on script interpreter) | is called by | [`0x0025E4C0`](../Scripts-And-Script-Commands/script-interpreter.md) World actor script vm: interpret bytecode (on script interpreter) |
| [`0x00264D60`](../Menus-And-HUD/aerodrome-airship-dialogue.md) (on aerodrome airship dialogue) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x00352A50`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00352EC0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003534F0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x00354F20`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x003555F0`](../Engine-Core/identifier-spaces.md) (on identifier spaces)<br>[`0x00356B70`](../Characters-And-Objects/npc-names.md) (on npc names)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x00357450`](archades-scripts.md) (on archades scripts)<br>[`0x0050CDE0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x002673A0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x003545B0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x002E16B0`](../Menus-And-HUD/message-windows.md) (on message windows) | is called by | [`0x0033F950`](../Menus-And-HUD/message-windows.md) (on message windows)<br>[`0x00348DF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034ADA0`](nalbina-town-scripts.md) (on nalbina town scripts)<br>[`0x0050EAB0`](../EBP-Script-Files/ebp-text-sections.md) (on ebp text sections) |
| [`0x003449A0`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00345080`](victory-pose-scripts.md) (on victory pose scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x003459C0`](mt-bur-omisace-scripts.md) (on mt bur omisace scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00348DF0`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x00349800`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00348DF0`](archades-scripts.md) (on archades scripts) |
| [`0x00349800`](archades-scripts.md) (on archades scripts) | is called by | [`0x00349BF0`](archades-scripts.md) (on archades scripts)<br>[`0x0034A090`](ending-message-scripts.md) (on ending message scripts)<br>[`0x0034A420`](archades-scripts.md) (on archades scripts)<br>[`0x0034A7A0`](archades-scripts.md) (on archades scripts) |
| [`0x00349BF0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A090`](ending-message-scripts.md) (on ending message scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A420`](archades-scripts.md) (on archades scripts) | calls | [`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00349800`](archades-scripts.md) (on archades scripts) |
| [`0x0034A6D0`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034B9A0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034C030`](cerobi-steppe-scripts.md) (on cerobi steppe scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034D4E0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034DD90`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x0034E0B0`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x0034EE20`](archades-scripts.md) (on archades scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00351880`](mt-bur-omisace-scenes.md) (on mt bur omisace scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x003529E0`](../Scripts-And-Script-Commands/event-scenes.md) (on event scenes) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x00267F90`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00352EA0`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00353390`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00354000`](barheim-passage-scripts.md) (on barheim passage scripts) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter)<br>[`0x0026B4E0`](../Scripts-And-Script-Commands/verb-dispatch.md) (on verb dispatch) |
| [`0x00354D00`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |
| [`0x00355830`](../World-Areas-And-Travel/treasure-chests.md) (on treasure chests) | calls | [`0x00267E10`](../Scripts-And-Script-Commands/script-interpreter.md) (on script interpreter) |

**Menus and HUD** (explained on [augments](../Damage-And-Battle-Formulas/augments.md), [zone asset list](../World-Areas-And-Travel/zone-asset-list.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263990`](../Menus-And-HUD/enemy-names-on-screen.md) (on enemy names on screen) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x002639E0`](../Menus-And-HUD/text-npc-names.md) (on text npc names) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x003778B0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0029C530`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) |
| [`0x003FFB00`](archades-scripts.md) (on archades scripts) | is called by | [`0x002AC5F0`](../Menus-And-HUD/text-drawing.md) (on text drawing) |

**World, areas and travel** (explained on [changing areas](../World-Areas-And-Travel/changing-areas.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [debug menu](../Engine-Core/debug-menu.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) | is called by | [`0x003145E0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) World transition: stage field transition (on zone changes and mapjump)<br>[`0x003778B0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list)<br>[`0x003C0450`](../Game-Files-And-Data-Tables/menu-map-files.md) (on menu map files)<br>[`0x0057FB00`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |
| [`0x0032FCA0`](../Sound-And-Music/voices.md) Actor resource: begin manager resource set load (on voices) | is called by | [`0x0032FC30`](tutorials-scenes.md) (on tutorials scenes) |
| [`0x003778B0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) | calls | [`0x00264F90`](../World-Areas-And-Travel/zone-asset-list.md) Map ref: get persistence group id (on zone asset list) |
| [`0x003778B0`](../World-Areas-And-Travel/zone-asset-list.md) (on zone asset list) | is called by | [`0x0057FB00`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |
| [`0x00377B60`](../World-Areas-And-Travel/area-flags-navimapdata.md) (on area flags navimapdata) | is called by | [`0x0057FB00`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) (on strong and weak mode) |

</details>
