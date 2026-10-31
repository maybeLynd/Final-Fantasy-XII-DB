---
title: "Location title scenes: each region title scene and the field scripts that load it"
kind: "reference"
category: "Story, events and hunts"
addresses: "0x003529E0, 0x00351880, 0x00353080, 0x003522C0, 0x0032FCA0, 0x00348DF0, 0x00264D60, 0x00354D00, 0x0032FC30, 0x003CA140, 0x00309230"
---

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

## Related

- [Title screen and location title scripts](titles-scripts.md) - the title screen scripts of the same group and the one row of `ttl_z0009`.
- [Royal Palace scripts](royal-palace-scripts.md) - the Cellar Stores, which load `ttl_z0009`.
- [Golmore Jungle scripts](golmore-jungle-scripts.md), [Feywood scripts](feywood-scripts.md), [Paramina Rift scripts](paramina-rift-scripts.md) and [Cerobi Steppe scripts](cerobi-steppe-scripts.md) - fields that load a title.
- [Ozmone Plain scripts](ozmone-plain-scripts.md) - Field of Fallen Wings and The Switchback.
- [Event scenes](../Scripts-And-Script-Commands/event-scenes.md) - how an event id loads a scene script.
