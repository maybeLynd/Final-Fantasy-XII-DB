[Home](../../README.md) / [Party](README.md) / Party data

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Party data: every field of the block the save game keeps for the party, above the forty member stats records | reference | Party | Party data | Each field of the 0x7410-byte party block behind 0x02EBF190: the magic and flag word, the forty member stats records, the owned-item counts and learned bits of every inventory class with their backups, the bazaar flags, the five slot maps and the leader selector, the walked distance, the summon and chocobo state, the party control mode words, the Traveler, Knot of Rust and Numerology counters, and the forty members' gambit banks, with each field's width, meaning, and the functions that write and read it. | 0x02EBF190, 0x00233C10, 0x002370C0, 0x0030B6A0, 0x00320A40, 0x0031B9F0, 0x00327C40 |

## What it lists

The party block is `0x7410` bytes inside the save image: buffer `0x02164280` + `0x4E68C`, which is payload
`+0x4E48C` ([Save data](../Saving-Loading-And-Settings/save-data-fields.md)). `0x00233C10` points `0x02EBF190` at it when the
pointer is empty and rebases the inventory class descriptors, and checks the magic `0x05071901` when it is set¹. Before that it runs `0x00235AF0`², which compares the block with the image's
copy ([Save file format](../Saving-Loading-And-Settings/save-file-format.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00233C25`-`0x00233C4D` |
| ² | `0x00233C14` |

</details>

With an empty pointer (twice, `0x00233C3F` and `0x00233C48`) or a wrong magic¹ `0x00233C10` then runs the
battle-state reset `0x00237DF0`,
whose first step `0x0023AF50` resets the block and adds the starting inventory
([Starting inventory](starting-inventory.md)). With the magic in place it rebuilds the gambit order set of all forty
members with `0x00327F80`, the loop form of `0x00327DE0` (`0x00233CAD`; [Gambits](../Enemy-AI-And-Gambits/gambits.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00233C59` |

</details>

On that path `0x00233C10` also, in this order:

- before the rebuild, sets bit `0x1000` of the flag dword `+0x04` when bit `0x1` of the battle flags `0x02089344` is
  set, then clears that bit and zeroes the dword `+0x5B00`, the word `+0x5B0C` and the byte `+0x5B0E`; with bit
  `0x1` clear it clears bit `0x1000`¹;
- after it, clears bit `0x2` of the word `+0x5AD0` (`0x003139A0(0)`, `0x00233CB4`) and bit `0x1` of the dword
  `+0x5AE0` (`0x00304770(0)`, `0x00233CBB`);
- empties the ring of fired traps `0x02EC3EA0` (`0x002FA230`, `0x00233CC0`;
  [Traps](../World-Areas-And-Travel/traps.md)) and the presence ledger `0x02EC3E60` (`0x002FA260`, `0x00233CC5`;
  [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md));
- calls the empty `0x0016D6A0`², which does no work;
- sets the speed index `0x01FD4A98` to 0 (`0x00229ED0(0)`, `0x00233CD1`) and stores a dword 0 at `0x0208E6B4`
 ³ ([Frame update order](../Engine-Core/frame-update-order.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00233C65`-`0x00233CA6` |
| ² | `0x00233CCA` |
| ³ | `0x00233CD6` |

</details>

The reset `0x002370C0` clears all `0x7410` bytes, writes the magic, clears the inventory counts and empties the inventory lists of `[0x020927C0]` ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md#the-inventory-lists)) (`0x003047F0`, `0x002370E5`; [Save data](../Saving-Loading-And-Settings/save-data-fields.md)), empties map 0's seats
and zeroes the walked distance¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002370CD`-`0x0023712E` |

</details>

The block holds:

- the forty member stats records from `+8` ([Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md));
- the inventory: owned counts and learned bits per class, laid out by the descriptors at `0x01EEBCC0` and rebased by
  `0x0030B6A0` ([Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md));
- the seats, the leader selector and party control mode ([Party slots](party-slots.md),
  [Party control modes](../Engine-Core/party-control-modes.md));
- the mode flags `+0x5B04`, whose bits `0x1` and `0x2` the status view `0x00329220` tests for its flag bits `0x400` and `0x800`; the
  screens read members through that view, the battle menu's target window `0x002BFD20` among them
  ([Party member status record](../Characters-And-Objects/party-member-status-record.md),
  [Battle menu](../Menus-And-HUD/battle-menu.md));
- the counters three formulas keep ([Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md));
- the gambit banks ([Gambits](../Enemy-AI-And-Gambits/gambits.md)). `0x00327C40(type, out)` copies member
  `type`'s selected bank, the 52 bytes at `+0x5B10 + (3 * type + [+0x7370 + 4 * type]) * 0x34`, to `out` and
  returns 1; for a type above 39 it copies nothing and returns 0¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00327C46`-`0x00327CA8` |

</details>

## Columns

[`party-data.tsv`](party-data.tsv), one row per field:

| Column | Meaning |
|---|---|
| `offset` | the field's offset in the block |
| `width_type` | its width and type; `record`, `bank` and the bracketed counts are arrays |
| `field` | its name on this page |
| `meaning` | what it holds, with the instructions that show it |
| `writers`, `readers` | the functions that write and read the field, with one site each |

Rows named `pad` are the bytes between two fields.

### How an access is counted

- A store or a read counts for every row its bytes cover; a clear or copy of a span counts for every row in it.
- A function that only takes a field's address is listed as a reader.
- An access through an inventory descriptor counts for the regions its handler serves¹: `0x002FD150`
  and `0x002FD8D0` for rows 0-2 (items, equipment, loot), `0x002FD420` and `0x002FD970` for the five bit rows, and
  `0x003047F0` for all eight count regions; `+0x20` is the loot tally and `+0x30` the items-ever-owned bits.
- The `members` row lists the functions that reach a member stats record through the block, directly or through the
  roster array `0x022C1740`, whose nine entries are member stats records from `0x00320AB0`; the functions that reach one
  through a battle unit are on [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01EEBCC0` |

</details>

The columns hold every access through the block pointer `0x02EBF190`, the active image `0x02164280`¹,
the roster array `0x022C1740`, the inventory descriptors `0x01EEBCC0` and the save file layer.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF640` |

</details>

### What carries the whole block

- The reset `0x002370C0` clears all `0x7410` bytes¹, and `0x002EF5F0` and `0x002EF650` clear the whole
  active image²; `0x0030FAA0` clears `+0x4F84`-`+0x57BF`, the two backups and the bytes
  after them, once it has put the backups back³.
- `0x00229B40` copies the block's first `0x6000` bytes, `0xC0` chunks of `0x80`, to image `+0x2200` (payload
  `+0x2000`; `0x00229B7B`-`0x00229BE2`), and `0x8000` bytes, `0x100` chunks of `0x80`, from the block into the capture
  image⁴. `0x005844A0` copies the same `0x6000` bytes to image `+0x2200`⁵
  when the block's first byte is not 0⁶.
- `0x002EF4A0`, called by `0x00235AF0`⁷, copies those `0x6000` bytes at image `+0x2200` back over the
  block's first `0x6000` bytes, `0xC0` chunks of `0x80`⁸.
- `0x0057E310` and `0x002EF690` copy the capture image into the write buffer `0x02211000` as `0xACD` chunks of `0x80`
  bytes and a 16-byte tail, `0x56690` bytes in all⁹; `0x002EF570`
  copies the active image into the backup `0x022676C0` the same way¹⁰.
- On a save the file layer's write `0x00866AD0` copies the write buffer into the file vector byte by byte
 ¹¹. On a load `0x00580EB0` queues a read request of `0x56690` bytes into the active image
 ¹²; the read `0x00866A00` moves the bytes from the file vector one at a time¹³.
- `+0x5AD0`-`+0x5ADF` and `+0x5AE0`-`+0x5AEF` are also copied as 16-byte blocks into the save-transition record
 ¹⁴ and back¹⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002370D3` |
| ² | `0x002EF603`, `0x002EF663` |
| ³ | `0x0030FBC7` |
| ⁴ | `0x00229BE4`-`0x00229C41` |
| ⁵ | `0x00584515`-`0x00584572` |
| ⁶ | `0x0058450B` |
| ⁷ | `0x00235B76` |
| ⁸ | `0x002EF4A0`-`0x002EF504` |
| ⁹ | `0x0057E347`-`0x0057E3A6`, `0x002EF6AB`-`0x002EF70F` |
| ¹⁰ | `0x002EF577`-`0x002EF5E6` |
| ¹¹ | `0x00866B1C`, `0x00866B40` |
| ¹² | `0x005810BC`-`0x0058111E` |
| ¹³ | `0x00866A46`-`0x00866A4D` |
| ¹⁴ | `0x002EF3D3`, `0x002EF3E5`, `0x002EF517` |
| ¹⁵ | `0x002EF424`, `0x002EF44C` |

</details>

## Related

- [Unit stats fields](../Damage-And-Battle-Formulas/unit-stats-fields.md) - the forty member stats records.
- [Party slots](party-slots.md) - the five slot maps and the leader selector.
- [Party leader](party-leader.md) - the leader handle the selector becomes.
- [Scenario presets](scenario-presets.md) - the sets that reset and refill the block.
- [Gambits](../Enemy-AI-And-Gambits/gambits.md) - the gambit banks.
- [Inventory](../Items-Equipment-Shops-And-Licenses/inventory.md) - the count words, bits and tallies.
- [Weapon formulas](../Damage-And-Battle-Formulas/weapon-formulas.md) - the Traveler, Knot of Rust and Numerology counters.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 21 calls with 6 other topics</summary>

**Movement and pathfinding** (explained on [frame update order](../Engine-Core/frame-update-order.md), [party control modes](../Engine-Core/party-control-modes.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0031AC00`](party-data.md) | is called by | [`0x0031BD60`](party-slots.md) (on party slots) |
| [`0x00326500`](party-leader.md) Party focus: select and request default actor (on party leader) | calls | [`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x003266C0`](party-slots.md) Battle group: refresh four actor definitions (on party slots) | calls | [`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x00326BB0`](party-data.md) | calls | [`0x00265200`](../Scripts-And-Script-Commands/party-during-scenes.md) (on party during scenes) |

**Game files and data tables** (explained on [startup constants](../Engine-Core/startup-constants.md), [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EF300`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format) | calls | [`0x0032E620`](../Graphics/effect-file-list.md) (on effect file list) |
| [`0x005691E0`](../Menus-And-HUD/menu-screens.md) (on menu screens) | calls | [`0x00249580`](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md) (on mrp menu resource packages) |

**Scripts and script commands** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md), [party verbs](../Scripts-And-Script-Commands/party-verbs.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002EF300`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format) | is called by | [`0x0050D9A0`](../Saving-Loading-And-Settings/save-file-format.md) (on save file format) |
| [`0x003170E0`](party-members.md) Party configuration: add selector07 to25 to available primary index (on party members) | is called by | [`0x00352190`](../Story-Events-And-Hunts/mt-bur-omisace-scripts.md) (on mt bur omisace scripts) |
| [`0x0031B510`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | is called by | [`0x0034F5A0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs)<br>[`0x003509E0`](../Battle-Actions/weapon-motion-list.md) (on weapon motion list) |
| [`0x00320800`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) | is called by | [`0x0034B4B0`](../Scripts-And-Script-Commands/party-verbs.md) (on party verbs) |
| [`0x00320AB0`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags) | is called by | [`0x0050FD00`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FD50`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FDD0`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FE20`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FE80`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FED0`](../Damage-And-Battle-Formulas/stats.md) (on stats)<br>[`0x0050FF20`](../Characters-And-Objects/battle-unit-construction.md) (on battle unit construction) |
| [`0x00327930`](../Damage-And-Battle-Formulas/unit-stats-fields.md) Gambit config: adjust available entry count by stats index (on unit stats fields) | is called by | [`0x00348B40`](../Damage-And-Battle-Formulas/unit-stats-fields.md) (on unit stats fields) |

**Enemy spawning** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00229B40`](../Saving-Loading-And-Settings/save-data-fields.md) World transition snapshot: capture runtime state (on save data fields) | calls | [`0x00233440`](../Saving-Loading-And-Settings/save-data-fields.md) Spawn keep: serialize persistence banks (on save data fields) |

**Status effects and KO** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00320AB0`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags) | is called by | [`0x00310DB0`](../Battle-Actions/action-results.md) Battle unit: run periodic combat maintenance (on action results) |

</details>
