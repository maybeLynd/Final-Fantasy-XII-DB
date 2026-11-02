---
title: "Rabanastre scripts: what each script function shows, sets, gives and starts"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x00348DF0, 0x00349800, 0x0034A420, 0x0034A090, 0x00349BF0, 0x00264D60, 0x0034B9A0, 0x0034EE20, 0x0034DFA0, 0x0034E320, 0x0034E980, 0x0034DD90, 0x0034E0B0, 0x00354D00, 0x003529E0, 0x00351880, 0x003449A0, 0x0034A6D0, 0x00345080, 0x003459C0, 0x0034A790, 0x00355830, 0x00349B60, 0x00510840, 0x00353770, 0x0034C030, 0x0034D4E0, 0x00377B60, 0x003778B0"
---

## What it lists

The table [rabanastre-scripts.tsv](rabanastre-scripts.tsv) has one row per script function of Rabanastre that does
something a player can observe. It covers the twenty zone scripts and the sixteen scene scripts of the region, from
`plan_master/us`:

| Script | Kind | Map or scene | Actors | Functions | Rows | Shared helpers |
|---|---|---|---:|---:|---:|---|
| `rbn_a01` | zone | North End, field `289` | 50 | 242 | 26 | 1 |
| `rbn_a02` | zone | Muthru Bazaar, field `290` | 33 | 150 | 17 | 0 |
| `rbn_a03` | zone | East End, field `291` | 64 | 414 | 50 | 1 |
| `rbn_a04` | zone | Southern Plaza, field `292` | 42 | 241 | 21 | 1 |
| `rbn_a07` | zone | Amal's Weaponry, field `295` | 18 | 89 | 2 | 1 |
| `rbn_a08` | zone | Panamis's Protectives, field `296` | 16 | 73 | 2 | 0 |
| `rbn_a09` | zone | Migelo's Sundries, field `297` | 25 | 145 | 9 | 1 |
| `rbn_a10` | zone | Yugri's Magicks, field `298` | 19 | 93 | 3 | 1 |
| `rbn_a11` | zone | Batahn's Technicks, field `299` | 16 | 75 | 2 | 0 |
| `rbn_a12` | zone | Yamoora's Gambits, field `300` | 16 | 78 | 4 | 0 |
| `rbn_a13` | zone | Samalzalam Manor, field `301` | 7 | 34 | 1 | 0 |
| `rbn_a14` | zone | The Clan Hall, field `302` | 33 | 256 | 16 | 1 |
| `rbn_a16` | zone | The Sandsea, field `304` | 35 | 203 | 16 | 1 |
| `rbn_a17` | zone | Eastgate, field `305` | 45 | 233 | 21 | 5 |
| `rbn_a18` | zone | Southgate, field `306` | 40 | 206 | 24 | 5 |
| `rbn_a19` | zone | Westgate, field `307` | 46 | 238 | 23 | 5 |
| `rbn_b01` | zone | Aerodrome, field `788` | 32 | 146 | 34 | 0 |
| `rbn_x01` | zone | field `860` | 8 | 12 | 1 | 0 |
| `rbn_y01` | zone | field `910` | 8 | 13 | 1 | 0 |
| `rbn_z01` | zone | field `50` | 5 | 6 | 1 | 0 |
| `rbn_a0100` | scene | event `107` | 22 | 128 | 11 | 0 |
| `rbn_a0200` | scene | event `100` | 33 | 347 | 8 | 0 |
| `rbn_a0300` | scene | event `101` | 30 | 428 | 8 | 0 |
| `rbn_a0380` | scene | event `709` | 24 | 141 | 11 | 0 |
| `rbn_a0381` | scene | event `711` | 24 | 170 | 4 | 0 |
| `rbn_a0382` | scene | event `726` | 16 | 71 | 1 | 0 |
| `rbn_a0480` | scene | event `721` | 14 | 89 | 5 | 0 |
| `rbn_a0980` | scene | event `707` | 10 | 84 | 10 | 0 |
| `rbn_a1300` | scene | event `120` | 28 | 359 | 21 | 0 |
| `rbn_a1600` | scene | event `109` | 30 | 169 | 14 | 0 |
| `rbn_a1601` | scene | event `119` | 21 | 126 | 12 | 0 |
| `rbn_a1700` | scene | event `108` | 23 | 290 | 29 | 0 |
| `rbn_a1701` | scene | event `118` | 32 | 326 | 38 | 0 |
| `rbn_x0100` | scene | event `106` | 21 | 161 | 8 | 0 |
| `rbn_y0100` | scene | event `104` | 38 | 464 | 12 | 0 |
| `rbn_z0100` | scene | event `102` | 16 | 119 | 4 | 0 |

Eastgate, Southgate and Westgate carry the five helper actors that many zone scripts share: the crystal
(`system_crystal_actor`, `telepoeffectctrl`, `crystaldummyPC`, `saveactor`) and the key-item and message helper
`イベント特殊効果画面`.

North End, East End, Southern Plaza, Amal's Weaponry, Migelo's Sundries, Yugri's Magicks, The Clan Hall and The
Sandsea carry the key-item and message helper alone. Their functions are described once on [Shared zone-script
actors](shared-zone-script-actors.md) and have no rows here; the Shared helpers column counts them.

A function is listed when it shows a line, sets or releases a story flag, writes the story counter, gives or takes
items, jumps to another map, makes one of the battle calls below, loads a scene or changes the party.

Functions that only move, animate, wait, play sound or set the camera have no row in this table; each listed row
counts the other functions of its actor in `other_functions`. Every function, these included, has its steps in the
steps table described under [Every step](#every-step). The scenes themselves, with their dialogue, are on [Rabanastre
scenes](rabanastre-scenes.md).

### What the scripts do

- North End (field 289): at story counter 100, `常駐監督.main` restores the party, loads and plays scene `rbn_a0100`
  (event 107), shows "You are now free to enter Lowtown and leave Rabanastre." and writes 105, the value after Vaan's
  resolve. `Map_Director.init` sets flag `0x004D`.
- North End: below story counter 100 the door to Lowtown (`mapダウンタウン扉`) answers "All traffic with Lowtown is suspended
  until the new consul reaches the palace."; from 100 it leads to North Sprawl (Lowtown), field 701. A door leads to
  Yamoora's Gambits, field 300, and the exits to Muthru Bazaar, field 290, and East End, field 291.
- North End: holding the Clan Primer, the clan watch (`クラン守護者１`) asks "Ah, you've got your Primer, so you have." and,
  on "Okay, let me in.", lets the party into The Clan Hall, field 302; without it he says "Hah! You don't even have
  one!" Once he has let the party in, the hall's door (`mapクラン本部`) leads there too; until then it reads "The door is
  firmly shut."
- North End and East End: the shop signs (`ショップFSレクト01`) give the shops' slogans, such as "A mind without instruction
  can no more bear fruit than can a field without cultivation." (Yamoora's Gambits). One North End sign reads "???
  (You're not sure what this sign is for.)" until the party has joined Clan Centurio, then "??? (This is a sign for
  Clan Centurio, but only clan members would know it as such.)"
- North End: the cockatrice Renn (`コカトリス`) asks "Tell me: has Chit returned home?"; on one branch of "Yes, actually."
  it gives the Deathbringer ("Oh, and take this. A small token of my gratitude for everything you've done."), on the
  other it answers "Lies! I would smell her scent on you had you seen her." The clan watch offers advice on catching
  cockatrices.
- Ktjn (`カトリーヌ`) talks with the party in Muthru Bazaar ("H-Hello. I am called Ktjn."); `g_iw_カトリーヌ結果` then decides
  where she stays. Her gift of thanks is the Hunting Crossbow in the North End, the Firefly in East End, the Fuzzy
  Miter in Migelo's Sundries or the Runeblade in The Clan Hall; as `カトリーヌ５` in the North End, Muthru Bazaar, East End
  and the Aerodrome she gives an Ether and three Hi-Potions.
- Across the town the townsfolk's lines change with the story counter, from "We're on heightened watch until the
  Consul's inauguration ceremony is complete." to "Our Emperor is dead, and Lord Vayne rules as autocrat in his
  stead."
- Muthru Bazaar (field 290): at story counter 33, `常駐監督.init` loads scene `rbn_a0200` (event 100), and `main` has
  `ヴァン登場イベント` play it, write 35, the value after Vaan the pickpocket, and jump to East End, field 291.
- Muthru Bazaar: at story counter 1570, `常駐監督.main` loads and plays scene `rbn_a0382` (event 726) and writes 1580, the
  start of the hidden Garif. Flag `0x0078`, a map icon in Muthru Bazaar, is set once the party has joined Clan
  Centurio and released before.
- From story counter 341 the Moogling (`モグシー`) stands in Muthru Bazaar, East End, Eastgate, Southgate and Westgate
  ("The Moogling lets you teleport to several select locations across Rabanastre."); `mogxiMapJumpDirector.mogjump`
  takes the party to East End, Muthru Bazaar, Eastgate, Southgate or Westgate (fields 291, 290, 305, 306 and 307).
- East End (field 291): at story counter 35, `常駐監督.main` plays scene `rbn_a0300` (event 101), shows "World Map has
  been added to the Party Menu." and writes 38, the value after Penelo appears, and 40, the value after the Map
  command tutorial. At 40 the field loads scene `rbn_a0380` (event 709).
- East End: touching `制御レクト２` has `常駐監督.EVミゲロ登場` play `rbn_a0380`, write 45, the value after Migelo appears, and set
  flags `0x0055` and `0x014A`, which `Map_Director.init` releases below 45 and sets from 45.
- East End: below story counter 45 the doors of The Sandsea, Yugri's Magicks, Panamis's Protectives, Amal's Weaponry
  and Batahn's Technicks answer "I really should go see Migelo first."; from 45 they lead to fields 304, 298, 296, 295
  and 299. Below 100 the door to Lowtown answers "No traffic in or out of Lowtown until the Lord Consul's assumed his
  post."; from 100 it leads to North Sprawl (Lowtown), field 701.
- East End: at story counter 390, arriving by entrance 1 or by the Moogling has `常駐監督.main` play scene `rbn_a0381`
  (event 711) at once; otherwise the field loads it and touching `制御レクト` plays it. Either way the story counter
  becomes 400, the value after Vaan and Basch.
- Southern Plaza (field 292): from story counter 50 to 65, `読み込み監督０１.init` loads scene `rbn_a0480` (event 721);
  touching `制御レクト` has `常駐監督.EV東門を抜けて` play it, write 68, the value after leaving through Eastgate, and jump to
  Eastgate, field 305.
- Southern Plaza: below story counter 100 the three city gates (`map東門`, `map南門`, `map西門`) answer "It's securely
  shut."; from 100 they open onto Eastgate, field 305, Southgate, field 306, and Westgate, field 307, whose gates lead
  back. While `g_iw_ラバナスタ通行止め状態` is not 0, two guards turn the party back ("South gate's closed, boy. Move along
  now.", "Gate's closed until the Consul's appointment ceremony is over.").
- Southern Plaza: from story counter 50 a bangaa merchant asks "Could you take him something for me?" and gives the
  Small Package; the merchant waiting in Eastgate asks "Did a bangaa merchant happen to give you an item to deliver?"
  and takes it ("Well, what do you know! My thanks, boy.").
- Southern Plaza: the Cartographers' Guild moogle (`地図屋`) asks "Would you like to buy a map, kupo?" and sells the maps
  of Dalmasca Estersand, Dalmasca Westersand and Giza Plains, each followed by "Your location map for this area is
  complete!"; when the party holds all of them it answers "What a shame, kupo! You already own all of the maps I have
  for sale."
- Amal's Weaponry, Panamis's Protectives, Migelo's Sundries, Yugri's Magicks and Batahn's Technicks lead back to East
  End, field 291, and Yamoora's Gambits to the North End, field 289. The keepers' words change with the story counter;
  below 62 Yugri's keeper says "I'm sorry, we're still getting the shop in order. Please call again soon!"
- Migelo's Sundries (field 297): from story counter 343 below 375, on the first visit (bit `0x1` of
  `g_iw_sb03_rbn_flg[0]` clear), `常駐監督.init` loads scene `rbn_a0980` (event 707) and plays it.
- Yugri's Magicks: the Sotted Imperial (`酔いどれ兵士`) and the Curious Woman of the Southern Plaza (`メダル女`) follow
  `メダルかけら２進行フラグ`. At 4 he asks "Necklace? What's this about a necklace?"; at 6 Shyle meets him ("...Shyle? I could've
  sworn I'd seen you, but I thought it must be my eyes playin' tricks on me."), gives the Grimy Fragment, the value
  becomes 7 and the party returns to East End, field 291.
- Samalzalam Manor (field 301): from story counter 1 to 1569, `常駐監督.main` plays scene `rbn_a1300` (event 120), writes
  1570, the value after the hidden power, and jumps to Muthru Bazaar, field 290.
- The Clan Hall (field 302): Montblanc (`モンブラン`) makes the party members at the first talk ("You are now a member of
  Clan Centurio!") and later gives one reward package for each clan rank above the last one rewarded, twelve in all.
  `常駐監督.main` sets flag `0x0139` and releases `0x0138`, map icons in North End.
- The Clan Hall: when the Yiazmat hunt is won, Montblanc has the moogles gather ("Have you really done it? Have you
  defeated Yiazmat?" ... "You will always be welcome in the halls of Clan Centurio!"). Ma'kenroh (`マッケンロウ`) tells
  where the marks are found, for example "Hunting the Rogue Tomato? Hrgm... Find it in the Dalmasca Estersand."
- The Sandsea (field 304): at story counter 45 or below, `常駐監督.init` loads scene `rbn_a1601` (event 119), and `main`
  plays it; Tomaj explains hunts ("So, here's how it works."), gives the Clan Primer, the Orrachea Armlet and the Writ
  of Transit ("Clan Primer has been added to the Party Menu.", "Licenses has been added to the Party Menu."), and the
  director writes 65, the start of the first hunt.
- The Sandsea: at story counter 400, `読み込み監督０１.init` loads scene `rbn_a1600` (event 109) and `main` places a touch
  area; touching it has `常駐監督.最速の飛空艇` play the scene, write 420, the value after the fastest airship, and add Balthier
  and Fran to the party ("Ba'Gamnan's note can only be referring to the Lhusu Mines in Bhujerba.").
- The Sandsea: once the Rogue Tomato fight is won (`g_btl_nm_パック` 2), Tomaj pays the bounty, closes the hunt and tells
  of "a bangaa standing watch in front of a building in the North End"; unless flag `0x0139` is set, he sets `0x0138`,
  a map icon in North End, and releases `0x0139`.
- The Sandsea: Gatsly (`依頼人`) petitions the Thextera hunt ("You saw my bill? My bill to hunt Thextera?") and closes it
  when it is won ("You did it! You brought down Thextera!"); the Marilith's petitioner closes that hunt and takes the
  Serpentwyne Must ("Ah, you've brought it!"). Above story counter 80 the notice board asks "Which bill would you like
  to read?"
- Eastgate (field 305) holds the crystal. Below story counter 78 the gate guard (`門番兵士`) asks "Foodstuffs for the
  banquet wasn't it? Well, do you need to pass?"; on "Yeah, open the gate." he answers "I don't see any foodstuffs on
  you." and lets the party back to the Southern Plaza, field 292.
- Eastgate: at story counter 78, `読み込み監督０１.init` loads scene `rbn_a1701` (event 118); talking to Kytes ("Ah, Vaan! I
  guess I'm not the only one who got locked out of the city!") has `常駐監督.EV東門のいざこざ` play it, take the Galbana Lilies,
  write 80 and 85, the value after the invitation to the parade, and jump to field 910 (`rbn_y01`).
- Eastgate, Southgate and Westgate: at story counter 343, `常駐監督` of the gate the party arrives at loads and plays
  scene `rbn_a1700` (event 108), writes 350, the value after the return to Rabanastre, restores the party, removes
  Basch as a guest and Balthier and Fran from the party and sets the fighting party to Vaan.
- Arriving by entrance 3 sets flag `0x001B` in Eastgate, by entrance 3 `0x001C` in Southgate and by entrance 5
  `0x001D` in Westgate: the location map's exits between Rabanastre and Dalmasca Estersand, Giza Plains and Dalmasca
  Westersand. Eastgate's exit leads to The Stepping (Dalmasca Estersand), field 227; Westgate's lead to Galtea Downs
  (Dalmasca Westersand), field 345, and to the Aerodrome, field 788.
- Eastgate, Southgate and Westgate: Gurdy (`NPC01`) hires out chocobos ("Only [value] gil should you wish to hire
  one."); a hired chocobo sets flag `0x0073`, riding a chocobo, and the party jumps to The Stepping (Dalmasca
  Estersand), field 227, from Eastgate and to Galtea Downs (Dalmasca Westersand), field 345, from Westgate.
- Southgate (field 306) holds the crystal. Its exit leads to Throne Road (Giza Plains): while `mp_sav初回` is 0, to
  field 236 below story counter 1475 and to field 253 from it; otherwise to field 253 when
  `(getplayloophour() - mp_sav補正時間) % 3` is 0 and to field 236 when it is not. From 100 the door to Lowtown leads to
  South Sprawl (Lowtown), field 702.
- Westgate (field 307) holds the crystal. Up to story counter 290 a guard bars the aerodrome ("Archadian citizens and
  their guests only inside the aerodrome today.") and `Map_Director.init` releases flag `0x0074`; from 291 it sets it.
  From 420 below 460 Fran stands in Westgate ("Balthier is waiting inside. If you've made ready, we can leave at
  once.").
- Westgate: from story counter 1210, for a clan rank of at least 4, Sorbet (`モグシー`) petitions the White Mousse hunt
  ("You've come about the bill I posted? Thank you, kupo!"). When it is won she takes the Broken Key and, from story
  counter 1540, gives the Sluice Gate Key in the same talk.
- Westgate: Rimzat (`リムザ`) asks for help ("I have been sent from Archadia to study the sandstorms of the Dalmasca
  Westersand") and sends the party to Cotze in the Southern Plaza, who sends it to Northon. At the last stage Cotze
  and Northon join Rimzat, the Wind Globe is taken and the Windvane given ("There. This should let you make your way
  through the storm.").
- Aerodrome (field 788): below story counter 6100 the counters sell passage to Archades, Nalbina and Bhujerba ("This
  counter serves travelers wishing to book passage to Archades."); boarding plays `pas_z0000` (event 214). The flight
  ends in the Sky Saloon (Skyferry), field 125, when a draw of 100 falls below 4, 8, 16, 32 or 64 by the stage of
  quest 153, else in the Observation Parlour (Skyferry), field 124, or the destination aerodrome.
- Aerodrome: Balthier (`バルフレア`) asks "You ready to leave?" and, after "I'm really ready.", `常駐監督.ムービー再生` plays the
  Strahl's departure with its subtitles ("This is the Strahl." ... "I'm coming, Penelo."), writes 460, the value after
  the Strahl takes off, and jumps to field 862 (`byu_z01`, Bhujerba).
- Aerodrome: the private airship desk ("We handle all private airship arrivals and departures from this desk.") boards
  the Strahl and loads `str_z0000` (event 211, [Strahl scene](strahl-scenes.md)); Nono (`ノノ`) tends the ship ("I'm
  gathering the parts I need to make repairs as quickly as I can").
- Field 860 (`rbn_x01`): from story counter 1 to 800, `常駐監督.main` plays scene `rbn_x0100` (event 106), writes 830, the
  value after Vayne's scheme, and jumps to the Bridge (Dreadnought Leviathan), field 871.
- Field 910 (`rbn_y01`): from story counter 25 to 90, `常駐監督.main` plays scene `rbn_y0100` (event 104), writes 95, the
  value after Vayne's speech, then 100, and jumps to North End, field 289.
- Field 50 (`rbn_z01`): up to story counter 290, `常駐監督.main` plays scene `rbn_z0100` (event 102), writes 301, the
  value after the vision of Reks, and jumps to the Stockade (Nalbina Dungeons), field 48.

### How a call is read

A call's arguments are read when they are literals; a computed argument is named by the variable that holds it.

| Verb | Id | Native body | Column | Meaning |
|---|---|---|---|---|
| `amese`, `amest`, `ames`, `ames_1fe` | `0x145`, `0x082`, `0x00F`, `0x1FE` | `0x0034A420`, `0x0034A090`, `0x00349BF0`, `0x00349800` | `lines` | the second argument is a section 2 text id |
| `setnpcname` | `0x38A` | `0x0034B9A0` | `speaker` | the actor's name pair ([NPC names](../Characters-And-Objects/npc-names.md)) |
| `setmapjumpgroupflag`, `releasemapjumpgroupflag`, `ismapjumpgroupflag` | `0x430`-`0x432` | `0x0034EE20`, `0x0034DD90`, `0x0034E0B0` | `flags_*` | Primary bank flag ([story flag ids](story-flag-ids.md)) |
| `settalknpcname`, `releasetalknpcname`, `istalknpcname` | `0x399`-`0x39B` | `0x0034DFA0`, `0x0034E320`, `0x0034E980` | `flags_*` | `Bank2048` flag: the name tag ([story flag ids](story-flag-ids.md), [NPC names](../Characters-And-Objects/npc-names.md)) |
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

1. `amese` (`0x0034A420`) pushes 0, 0, 0 and -1; `amest` (`0x0034A090`) pushes 0; `ames` (`0x00349BF0`) pushes 1. Each then
   jumps to `0x00349800`, the body of `ames_1fe`.
2. `0x00349800` pops two values (`0x00349827`, `0x00349831`), pushes 0 and 0 (`0x0034983D`, `0x00349847`) and then pushes the
   two values back in their original order (`0x00349851`, `0x0034985B`), so the zeros lie beneath them; it jumps to
   `0x00348DF0` (`0x00349884`).
3. `0x00348DF0` pops eight values. The seventh, the script's second argument, is passed with the current field context
   to `0x00264D60` (`0x00348E6A`-`0x00348E74`), the section 2 lookup, which keeps the low 24 bits of the id.

### Speakers, places and scenes

- The speaker of a line is the name its window shows. A `{name:P}` header (escape `0F 8`) names pair P in `us`
  `npcdic.bin`, P read as the parser `0x003FFB00` reads it. A plain name before the first line break,
  after `{instant:8181}` or at the start of a zone line, shows that name. An `{actor-name}` header (escape `0F >`)
  shows the name `0x00263990` gives the actor the window speaks for.
- The header's name comes from `0x002639E0`, which three of the five callers of `0x003FFB00` call next
  (`0x002ADDAA`, `0x002B16D4`, `0x002B52EF`): the first name while the pair's name flag is clear, the second once it is set. The
  `speaker` cell gives the second name. The window sets the flag of the pair of the actor it speaks for (next
  item), and `settalknpcname` sets any pair's ([NPC names](../Characters-And-Objects/npc-names.md)).
- The window speaks for the message call's target, the calling actor or the actor an `X.` prefix names: `0x002621D0`
  passes it to the verb, and `0x00348DF0` hands it to `0x002E16B0`. That actor's name is the second name of each pair its
  `setnpcname` calls name; `0x002E16B0` sets the actor's name flag before the window opens, and `0x00263990` shows the
  second name while that flag is set.
- An actor no `setnpcname` or `setshopname` call names keeps the name id `0xFFFF` and the empty text the record set-up
  `0x00266530` writes (`0x0026668B`, `0x0026669B`-`0x002666B4`), so its `{actor-name}` header shows no name; that line reads
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
- A field id is named by its map name, entry `id` of `us` `planmapname.bin` (`0x00377B60`), and its region, the
  entry after the map names that `0x003778B0` selects through the field's group in `map_ref.bin` (`0x00264F90`).
- An event id `n` names the scene script at index `4n` of the event file table, which `0x0032FCA0` loads for scene
  managers 1 to 3.

### Every step

The steps table [`rabanastre-script-steps.tsv`](rabanastre-script-steps.tsv) has one row for each step of every
function of the thirty-six scripts, in the order the function runs them: each call, request, store, branch, loop, case
and return. It has 96,213 rows.

A row gives where the step sits in the script, the branch it runs under, the verb and its arguments, and what those
arguments name in the game: the actor, the model, the animation and its motion file, the effect file, the event sound,
the camera shot, the message window or the variable. It also gives the frames the step takes, what it waits for, and
the functions it starts on other actors.

| Script | Steps | Script | Steps |
|---|---:|---|---:|
| `rbn_a01` | 5,850 | `rbn_y01` | 68 |
| `rbn_a02` | 5,545 | `rbn_z01` | 28 |
| `rbn_a03` | 8,747 | `rbn_a0100` | 1,606 |
| `rbn_a04` | 5,599 | `rbn_a0200` | 2,185 |
| `rbn_a07` | 2,191 | `rbn_a0300` | 2,414 |
| `rbn_a08` | 1,664 | `rbn_a0380` | 1,695 |
| `rbn_a09` | 2,846 | `rbn_a0381` | 1,639 |
| `rbn_a10` | 1,631 | `rbn_a0382` | 839 |
| `rbn_a11` | 1,898 | `rbn_a0480` | 1,383 |
| `rbn_a12` | 1,630 | `rbn_a0980` | 838 |
| `rbn_a13` | 275 | `rbn_a1300` | 2,927 |
| `rbn_a14` | 6,218 | `rbn_a1600` | 1,650 |
| `rbn_a16` | 4,540 | `rbn_a1601` | 1,914 |
| `rbn_a17` | 5,495 | `rbn_a1700` | 2,741 |
| `rbn_a18` | 3,234 | `rbn_a1701` | 2,705 |
| `rbn_a19` | 3,525 | `rbn_x0100` | 1,424 |
| `rbn_b01` | 5,479 | `rbn_y0100` | 3,031 |
| `rbn_x01` | 62 | `rbn_z0100` | 697 |

The five shared helper actors have their steps once, in [`shared-zone-script-steps.tsv`](shared-zone-script-steps.tsv)
(1,283 rows over 26 templates for 29 functions: the template of a function that only returns, cecbbef6fb, serves the
`init` of イベント特殊効果画面, telepoeffectctrl and crystaldummyPC and the `main` of saveactor). In this table each of their
functions has a single `shared template` row naming the template; Rabanastre has 167 such rows.

Some actors run another actor's code: `クランＦＳレクト` in `rbn_a01` starts at the same place as `ショップFSレクト01` and runs the
same functions. Such an actor has one `same code` row naming the actor whose steps it runs. There are 308 of these
rows: 25 in `rbn_a01`, 21 in `rbn_a02`, 29 in `rbn_a03`, 33 in `rbn_a04`, 17 in `rbn_a07`, 13 in `rbn_a08`, 12 in
`rbn_a09`, 7 in `rbn_a10`, 14 in `rbn_a11`, 8 in `rbn_a12`, 19 in `rbn_a14`, 17 in `rbn_a16`, 33 in `rbn_a17`, 17 in
`rbn_a18`, 15 in `rbn_a19` and 28 in `rbn_b01`.

The steps by their `resolution` cell:

| Resolution | Steps |
|---|---:|
| `resolved` | 95,955 |
| empty | 256 |
| `does not ship`, with the fact | 2 |

The two `does not ship` rows are `motionread` calls that read an empty entry: entry 0 of `rbn_a14.mot` and entry 2 of
`rbn_a0381.mot`. A row whose `resolution` cell is empty gives the step as the listing writes it: the verb, and the
arguments as the script writes them (`-` for a verb without arguments). Its `addresses`, `timing` and `sync` cells carry
what they give for the step, for example the variable that receives a result, and `-` otherwise.

A scene reads from top to bottom in its director's function. In `rbn_a1601` (event `119`), `ディレクター.main` fades the
music to volume 80 over 90 frames and starts `準備` on nine actors together, among them `ヴァン`, `トマジ` and `カイツ`, waiting
for seven of them to end. It files `パーティー全体.イベント開始前準備` and `ボイス.準備２` and waits for both, then files `ディレクター.イベント進行`
and `パーティー全体.イベント終了処理` in turn, waiting until each ends. It fades the music back to volume 127 over 90 frames and
fades the screen out over 0 frames.

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
| `flags_set`, `flags_released`, `flags_tested` | the flag ids, each with the first sentence of its explanation on [story flag ids](story-flag-ids.md); a `Bank2048` flag carries its bank name |
| `counter_set` | each value written to the story counter, with the first sentence of its explanation on [story counter values](story-counter-values.md) |
| `counter_tested` | each comparison of the story counter, as the relation and the decimal value |
| `items` | items received or lost, with their names; `the item held in` and the variable for an item a variable holds; for a request of the helper, the item the requesting function hands over; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `jumps` | each `mapjump`: the target map (region), its field id and the entrance; `field held in` and the variable when the target field is a variable |
| `battles` | not used by these scripts: `-` on every row |
| `scenes` | each scene script the function loads, with its event id |
| `party` | members who join and the fighting party a call sets |
| `other_functions` | the actor's functions that have no row |
| `shared_actor` | `-` for an ordinary actor; for a function of a shared helper actor that is listed, whether its body matches the shared one |

In the `line_text` column, a choice list is written as `(choices: ...)`, and a value the game fills in when the line
is shown is written `[value]`.

The script list [rabanastre-script-list.tsv](rabanastre-script-list.tsv) holds the first table above, one row per
script:

| Column | Meaning |
|---|---|
| `script`, `kind`, `place` | the script, `zone` or `scene`, and its map (region) and field id, or its event id |
| `actors`, `functions` | the script's actors and functions, shared helpers included |
| `rows` | the script's rows in the main table |
| `shared_actors` | the shared helper actors the script carries whose functions all match; `differs:` names a carried one that does not |

The steps table [`rabanastre-script-steps.tsv`](rabanastre-script-steps.tsv) has one row per step:

| Column | Meaning |
|---|---|
| `script`, `actor`, `function` | as in the main table |
| `step` | the step's number in its function, from 1, in the order the function's bytes run |
| `at` | where the step's instruction sits: its offset in section 0, the script image, of the shipped `plan_master/us` `.ebp`. For `case`, `default` and `label` it is where their code starts. For `shared template` and `same code` it is where the function or actor starts |
| `line` | the step's line in the script listing, `-` for the `shared template` and `same code` rows |
| `condition` | the tests the step runs under, outermost first, separated by `;`. A case is written `x = v` (the switch starts at the first case that matches, so a value an earlier case also matches starts at that earlier case), a default `x is none of ...`, an else part `not (test)` and a loop body `loop while test`. After the enclosing tests come, in listing order, the ways the function leaves before the step: a `return`, a `break` (it leaves its repeat or switch), a `continue` (it skips the rest of the pass) or a `goto` past the step that an earlier test sends the run to, and a repeat that never ends. Each is written as the test that keeps the run on its way to the step: `not (regI0 == 0)` after `if (regI0 == 0) { return; }`, or `not ((test) and (test))` when several tests together lead away. A test inside a repeat counts for the pass the step runs in, and a test the run does not reach counts as one that does not hold. After a repeat that a `return` or a `goto` can also leave, a step reached only when the repeat ends by itself carries `the repeat at line N ended at its own test or a break` (`through a break` for an endless repeat), and a way out of it reads `the repeat at line N was left at line M`. When a `goto`, or a case that runs on into the next case, also leads to the step, only the enclosing tests that hold on every way to the step are written, followed by the same items for the ways that miss it. A function that a `goto` of another function enters at one of its labels runs either from its top or from that label: an item then names where the run came in, `the run began at the top of the function` or `the run entered at line N through a goto from another function`. A `case` or `default` step is a test of its switch, so it runs whenever the switch runs. `unreachable in the listing` marks a step that no path of the function in the decompiled listing reaches; it rests on the labels the listing prints for jump targets |
| `verb` | the verb the step calls, by its name in the [verb table](../Scripts-And-Script-Commands/verb-table.md), written `Actor.verb` for a call on another actor. Otherwise the kind of step: `if`, `else if`, `while`, `for`, `switch`, `case`, `default`, `break`, `goto`, `label`, `return`, `returnT`, `store`, `shared template` or `same code` |
| `arguments` | the arguments as the script writes them; for `store` it is `variable = value`, and for a branch or loop it is the test. A number with a fraction is the listing's print of a 32-bit float to nine significant digits, here and in `condition`: 1.60000002 is the float nearest to 1.6, and 2.36000005e-06 is 2.36000005 times 10 to the power -6 |
| `addresses` | what the arguments name in the game: the actor, model, animation and motion file, effect file, event sound, camera shot, message window, request slot or variable |
| `quoted_lines` | for a call that shows dialogue or a system message, each line it shows, written `line N: ` and the us text with its text codes dropped; `-` for every other step |
| `timing` | the frames, fade lengths and speeds the step uses |
| `sync` | what the step waits for, and for a request whether it waits until the function starts, until it ends or not at all |
| `calls` | the functions a request starts, as `actor.function`; for a `goto` into another function, that function |
| `resolution` | `resolved`; `does not ship:` and the fact; or empty |
| `source` | the page or table that gives the meaning, or the function whose body was read |

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
- [Rabanastre scenes](rabanastre-scenes.md) - the sixteen scenes these scripts own.
- [Aerodrome airship scenes](aerodrome-airship-scenes.md) - the scene boarding a passenger airship plays.
- [Strahl scene](strahl-scenes.md) - the private airship scene the anchor loads.
- [Lowtown scripts](lowtown-scripts.md) - North Sprawl and South Sprawl, beyond the doors to Lowtown.
- [Garamsythe Waterway scripts](garamsythe-waterway-scripts.md) - the sluice gates the Sluice Gate Key works, and the way out of the waterway into Muthru Bazaar.
- [Dalmasca Estersand scripts](dalmasca-estersand-scripts.md) - The Stepping, beyond Eastgate.
- [Dalmasca Westersand scripts](dalmasca-westersand-scripts.md) - Galtea Downs, beyond Westgate.
- [Giza Plains scripts](giza-plains-scripts.md) - Throne Road, beyond Southgate.
- [Skyferry scripts](skyferry-scripts.md) - the Sky Saloon and the Observation Parlour.
- [Bhujerba scripts](bhujerba-scripts.md) - field 862, where the Strahl's first flight ends.
- [Dreadnought Leviathan scripts](dreadnought-leviathan-scripts.md) - the Bridge field 860 jumps to.
- [Nalbina Dungeons scripts](nalbina-dungeons-scripts.md) - the Stockade field 50 jumps to.
- [Hunts](hunts.md) - the marks and their petitioners.
- [Story flag ids](story-flag-ids.md) - every flag id with what it opens.
- [Story counter values](story-counter-values.md) - every value scripts write to the story counter.
- [Scene rewards](scene-rewards.md) - every item a script gives, with the place it is given.
