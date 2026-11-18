[Home](../../README.md) / [Story, events and hunts](README.md) / Location title scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Location title scenes: each region title scene and the field scripts that load it | reference | Story, events and hunts | Scenes and scripts by area / Scenes that recur through the story | The location title scene scripts ttl_z0000 to ttl_z0009: the event id of each, the fields of other regions whose zone scripts load it, most of them only on the party's first arrival, and the one flag a title sets. | 0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x0032FC30, 0x003CA140, 0x00309230 |

## What it lists

The table [titles-scenes.tsv](titles-scenes.tsv) has one row per scene script of the title group `ttl` under
`plan_master/us/event`. No zone script shares their file-name prefix, so their `next` column is `-`;
the zone scripts that load them belong to other regions: `loaded_by` names each, and the table below names their
fields from the load records of every group.

| Scene | Event | Loaded in | Lines | What follows |
|---|---:|---|---:|---|
| `ttl_z0000` | `215` | Banks of the Sogoht (Jahara); Walk of Flitting Rifts, Walk of Dancing Shadow (The Feywood); Walk of Sky, Ward of Measure (Stilshrine of Miriam); Field of Fallen Wings, The Switchback (Ozmone Plain); Fading Vale, Icebound Flow (Paramina Rift) | 0 | - |
| `ttl_z0001` | `216` | Augur Hill, The Sandscale Bank (Nam-Yensa Sandsea); Central Spur Stairs (Garamsythe Waterway); Starfall Field, Gizas South Bank (Giza Plains); Galtea Downs, Shimmering Horizons (Dalmasca Westersand); Invitation to Heresy, Halls of Ardent Darkness, The Balamka Fault, Darkened Wharf, Canopy of Clay (Zertinan Caverns) | 0 | - |
| `ttl_z0002` | `217` | Hall of Slumbering Might (Necrohol of Nabudis); Greencrag, Field of the Fallen Lord (Nabreus Deadlands); The Omen-Spur (The Salikawood); Southern Skirts, Summit Path (Mosphoran Highwaste); Realm of the Elder Dream (Tchita Uplands); Path of Hidden Blessing (Ridorana Cataract); Old Elanise Road, South Liavell Hills (Cerobi Steppe); Sea Breeze Lane, Saccio Lane (Balfonheim Port) | 0 | - |
| `ttl_z0003` | `430` | The Stepping (Dalmasca Estersand) | 0 | - |
| `ttl_z0004` | `431` | Throne Road (Giza Plains) | 0 | - |
| `ttl_z0005` | `432` | Paths of Chained Light (Golmore Jungle) | 0 | - |
| `ttl_z0006` | `433` | North Entrance (Henne Mines) | 0 | - |
| `ttl_z0007` | `434` | - | 0 | - |
| `ttl_z0008` | `358` | The Wellspring (Pharos - First Ascent); The Reach (Pharos - Second Ascent); Penumbra - Interior (Pharos - Subterra); Spire Ravel - 1st Flight (Pharos - Third Ascent) | 0 | - |
| `ttl_z0009` | `436` | Cellar Stores (Royal Palace) | 0 | - |

### The scenes

- A field's director loads its title. 30 of the 42 loading functions run the load only while a map-jump group flag is
  clear (`ismapjumpgroupflag(N) == 0`) and set that flag after the scene, so the title plays on the party's first
  arrival.
- Field of Fallen Wings (Ozmone Plain), for one, loads event 215 when the party arrives by entrance 1 while
  `g_com_mnp_オズモーネ平原ロケタイ`, the Ozmone Plain location title, is 0 and flag `0x0031` is clear, and sets the flag after
  the scene ([Ozmone Plain scripts](ozmone-plain-scripts.md)).
- One title serves several fields: `ttl_z0000`, `ttl_z0001` and `ttl_z0002` are each loaded in nine to twelve fields,
  and the camera actor of `ttl_z0000` holds functions named for fields (`オズモーネa01`, `ゴルモアa01`, `パラミナa01` and others).
- None of the ten holds text of its own: their section 2 has no entries (`lines` 0). They give no items and do not
  change the party.
- `ttl_z0009`, loaded in the Cellar Stores of the Royal Palace after story counter 200 is written, sets flag `0x002F`,
  the location map's exits between Garamsythe Waterway and Royal Palace ([Royal Palace
  scripts](royal-palace-scripts.md)).
- `ttl_z0007` (event 434) is the Phon Coast title: its camera functions are `フォーン海沿岸01` and `フォーン海沿岸02`, and it
  reads location effect 37. No script names event 434. In the game the Phon Coast title plays inside the arrival
  scene `fon_a0600` (event 251), which reads the same location effect 37 and which `fon_a06` loads on the first
  visit, while `g_com_mnp_フォーン海沿岸ロケタイ` is 0.
- The load goes through `eventread` (`0x0E7`, `0x003529E0`) or `eventread_e8` (`0x0E8`, `0x00351880`), and `0x0032FCA0`
  reads the scene from index `4n` of the event file table ([event
  scenes](../Scripts-And-Script-Commands/event-scenes.md)).

## Columns

| Column | Meaning |
|---|---|
| `scene` | the scene script, by its file name |
| `event_id` | the event id that loads it |
| `loaded_by` | the zone script, actor and function whose `eventread` or `eventread_e8` call names the event; `-` for `ttl_z0007`, whose event no script names |
| `lines` | the number of entries in the scene's section 2, empty strings included |
| `synopsis` | the `us` text of every non-empty entry, in entry order, separated by ` / `; a choice list is written as `(choices: ...)`; a scene with no non-empty entry: one sentence of what its script does |
| `items` | items the scene's own functions give or take, by name; a fixed count is written `xN`, and a count the game computes reads `, as many as <expression> gives` |
| `party` | members who join and the fighting party the scene sets |
| `flags_set` | story flags set by the scene, with the first sentence of each explanation on [story flag ids](story-flag-ids.md) |
| `counter_set` | story counter values written by the scene, with the first sentence of each explanation on [story counter values](story-counter-values.md) |
| `next` | the scene or map that follows when the loading script has the same file-name prefix; `-` here |
| `plays_when` | when the scene plays, in game terms: where, and what the player does (entering the map, talking to someone, touching a spot, winning a battle); the story counter values it plays at, named from [story counter values](story-counter-values.md), with the cases of its switch that come first applied (a switch starts at the first case that matches); every other test on the way to the loading step in what the game holds; and the listing lines it rests on (a step table's line) |

## Related

- [Title screen and location title scripts](titles-scripts.md) - the title screen scripts of the same group and the one row of `ttl_z0009`.
- [Royal Palace scripts](royal-palace-scripts.md) - the Cellar Stores, which load `ttl_z0009`.
- [Golmore Jungle scripts](golmore-jungle-scripts.md), [Feywood scripts](feywood-scripts.md), [Paramina Rift scripts](paramina-rift-scripts.md) and [Cerobi Steppe scripts](cerobi-steppe-scripts.md) - fields that load a title.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - Field of Fallen Wings and The Switchback.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 42 calls with 11 other topics</summary>

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0032FC30` | calls | `0x0032FCA0` |
| `0x0032FC30` | is called by | `0x0025D9E0` |
| `0x0032FCA0` | calls | `0x002628B0`, `0x0032ED80`, `0x00330310`, `0x003306E0` |

**Characters and objects** (explained on [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [ps2data bin families](../Game-Files-And-Data-Tables/ps2data-bin-families.md))

**Battle actions** (explained on [battle units](../Characters-And-Objects/battle-units.md))

| Function | | Functions |
|---|---|---|
| `0x00309230` | is called by | `0x00306BD0` |
| `0x0032FC30` | is called by | `0x00306BD0` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00354D00` | calls | `0x00229EA0` |

**Game files and data tables** (explained on [debug menu](../Engine-Core/debug-menu.md), [startup constants](../Engine-Core/startup-constants.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

| Function | | Functions |
|---|---|---|
| `0x0032FCA0` | calls | `0x002DF980`, `0x0032E400`, `0x0032E620` |
| `0x00351880` | calls | `0x001D6A70` |
| `0x003529E0` | calls | `0x001D6A70` |

**Scripts and script commands**

| Function | | Functions |
|---|---|---|
| `0x00264D60` | is called by | `0x00348DF0`, `0x0034ADA0`, `0x00352A50`, `0x00352EC0`, `0x003534F0`, `0x003545B0`, `0x00354F20`, `0x003555F0`, `0x00356B70`, `0x0050EAB0` |
| `0x0032FC30` | is called by | `0x003522C0`, `0x00353080`, `0x00353590`, `0x0050D0C0` |
| `0x00348DF0` | calls | `0x00267E10` |
| `0x00348DF0` | is called by | `0x00349800` |
| `0x00351880` | calls | `0x00267E10` |
| `0x003529E0` | calls | `0x00267E10`, `0x00267F90` |
| `0x00354D00` | calls | `0x00267E10` |

**Scripts and script commands** (explained on [archades scenes](archades-scenes.md), [archades scripts](archades-scripts.md), [ebp text sections](../EBP-Script-Files/ebp-text-sections.md), [npc names](../Characters-And-Objects/npc-names.md), [event scenes](../Scripts-And-Script-Commands/event-scenes.md))

**Scripts and script commands** (explained on [ebp script container](../EBP-Script-Files/ebp-script-container.md), [debug menu](../Engine-Core/debug-menu.md), [force fight mode](../Engine-Core/force-fight-mode.md), [native commands](../Scripts-And-Script-Commands/native-commands.md))

**Menus and HUD** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

| Function | | Functions |
|---|---|---|
| `0x003CA140` | is called by | `0x002D70F0` |

**World, areas and travel**

| Function | | Functions |
|---|---|---|
| `0x0032FC30` | calls | `0x0025D4D0`, `0x003319D0`, `0x003EA6E0` |
| `0x0032FC30` | is called by | `0x00314020` |
| `0x0032FCA0` | is called by | `0x0032FC30` |
| `0x003522C0` | calls | `0x0032FC30` |
| `0x00353080` | calls | `0x0032FC30` |

**World, areas and travel** (explained on [frame update order](../Engine-Core/frame-update-order.md), [debug logging](../Engine-Core/debug-logging.md), [debug menu](../Engine-Core/debug-menu.md))

</details>
