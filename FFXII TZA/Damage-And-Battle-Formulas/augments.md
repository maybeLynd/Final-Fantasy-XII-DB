---
title: "Augments: how a unit's augments, auto-statuses and status immunities are rebuilt from its character, gear, licenses and an enemy's script"
kind: "system"
category: "Damage and battle formulas"
addresses: "0x0030FED0, 0x0030E130, 0x0030E360, 0x002390B0, 0x002394C0, 0x0030E060, 0x00323890"
---

## What the player sees

Augments are the passive abilities from the License Board and from gear, such as the +30 HP license
(augment 74) or the extra Steal rolls of Thief's Cuffs. Some gear also keeps a status on its wearer or
makes the wearer immune to statuses.

- Equipping an item gives its augment at once, and removing it takes the augment away: the set is worked
  out again from scratch, so nothing is left behind.
- Buying an augment license gives its augments the same way.
- Enemies get their augments and status immunities from their own script.

## How it works

### The rebuild

`0x0030FED0(stats, flags)` rebuilds a unit's augment set. It forces flag bits `0x202` on (`0x0030FEFB`) and
starts from an empty 128-bit set (`0x0030FF02`-`0x0030FF0A`). Its 25 call sites:

| Caller | Sites |
|---|---|
| the equipment setters `0x0031A410`, `0x0031A510`, `0x0031A630` | `0x0031A4CA`, `0x0031A5ED`, `0x0031A6D4` |
| the License setter `0x00323910` | `0x00323B87` |
| the level setter `0x0030C470` and the level-up `0x0030C650` | `0x0030C602`, `0x0030C7CE` |
| the layer write `0x0030E130`, the status write `0x0030E360`, `0x0030E8F0` and `0x0030F690` | `0x0030E329`, `0x0030E828`, `0x0030E94D`, `0x0030F735` |
| the result applier `0x003112F0` | `0x00311AC5` |
| the spawn finalisation `0x0023A410` | `0x0023A502` |
| `0x00328BD0` | `0x00328C66` |
| the direct stat orders `0x002FDDA0` ([Battle orders](../Battle-Actions/battle-orders.md)) | `0x002FDEF7`, `0x002FE163`, `0x002FE1DB`, `0x002FE22F`, `0x002FE283`, `0x002FE2D7`, `0x002FE32D`, `0x002FE383`, `0x002FE3D9`, `0x002FE42D`, `0x002FE481`, `0x002FE4D5` |

### The four sources

The wanted set is the OR of these sources:

| Source | For | Adds | Sites |
|---|---|---|---|
| character row | party records | bits of words `+0x50` (augments 0-31) and `+0x54` (32-63) of the row of `0x02EBF130` the type byte `+0x04` selects | `0x0030FF1F`-`0x00310018` |
| enemy mask | enemy-side records | the 128 bits at battle unit `+0xE80` | `0x0031001A`-`0x0031006F` |
| equipment | everyone | byte `+0x1A` of each equipped item of group 3 (helms, armor, accessories), unless it is `0xFF` | `0x00310071`-`0x00310121` |
| licenses | everyone | the eight `u16` at `+0x08`-`+0x16` of each owned node (bit *i* of stats `+0x194`, *i* < 361) whose type byte `+0x05` is 15-18, skipping `0xFFFF` | `0x00310127`-`0x003102DF` |

Every source sets its augment's bit in the one 128-bit set at `[rsp + 0x40]` with `bts` (`0x0030FF9D`, `0x0030FFC2`,
`0x0031000A`, `0x0031005C`, `0x00310114`, `0x003101C5`-`0x003102CF`), so two sources of one augment (two pieces of gear, or
gear and a license) give one bit, and the augment does not stack.

The License node's type is classed by `0x003241D0` and `0x00323890`: types 15-17 are group `0x1B` and type 18
group `0x1C`, and both groups are class 2, the only class that adds augments (`0x00310192`-`0x0031019E`).

### Applying the difference

The wanted set is compared with the augment layer `+0x78` (`0x003102E5`-`0x00310336`):

```python
added = (wanted ^ layer) & wanted      -> 0x0030E130(stats, id, 0, flags, mode 3)
removed = (wanted ^ layer) & layer       -> 0x0030E130(stats, id, 0, flags, mode 1)
```

The walk covers ids 0-127 (`0x00310338`-`0x003103A3`). Mode 3 sets the bit in `+0x78` and mode 1 clears it,
each with the side effects of `0x0030E130`. Then the stats rebuild `0x002FEF30` runs (`0x003103AD`,
[Stats](stats.md)).

### Auto-statuses and immunities from gear

The stats rebuild ORs two status words into the stats record
([Stats](stats.md)): the character row's words `+0x48` and `+0x4C`, and each equipped item's attribute
words `+0x08` and `+0x0C` (`0x002FF0A3`-`0x002FF0D9`, `0x002FF505`-`0x002FF51E`):

| Stats word offset | From row | From item | What it does |
|---|---|---|---|
| `+0x3C` | `+0x48` | `+0x08` | statuses the unit has as long as the source stays (status word 2) |
| `+0x38` | `+0x4C` | `+0x0C` | statuses the unit cannot get: adding one to `+0x64` is refused (`0x0030E531`) |

The status write `0x0030E360` picks its word by mode (jump table `0x0030E88C`): modes 0, 1 and 2 clear a bit in
`+0x64`, `+0x3C` and `+0x38`; modes 3, 4 and 5 set it, mode 3 refusing a status already in `+0x64` or in
`+0x38` (`0x0030E4E7`-`0x0030E564`).

### An enemy's scripted augments and immunities

Two script commands set an enemy's two masks:

- **`btlAtelSetAbility(a, b)`**: the handler `0x00510440` pops two numbers and jumps to `0x002390B0`, which
  clears `+0xE80` and sets the augments of the two words in reverse bit order: bit *j* of the first argument
  sets augment 31 - *j*, bit *j* of the second sets augment 63 - *j* (`0x002390D8`-`0x00239161`). Only augments 0-63
  can be set this way.
  - The handler's first pop (`0x00267E10`) is the word pushed last, the second argument, and it is `0x002390B0`'s
    first word.
  - For an actor without a battle unit (`0x0031B760` gives 0) `0x002390B0` returns at once and clears nothing
    (`0x002390CA`).
- **`btlAtelSetStatus(table)`**: the handler `0x005103B0` resolves its argument to 8 bytes of script data and
  jumps to `0x002394C0`, which returns at once for an actor without a battle unit (`0x002394D9`), zeroes
  `+0xE90` (`0x002394FC`) and reads 32 two-bit codes, one per status (`0x00239504`-`0x00239527`):

| Code | Effect |
|---:|---|
| `3` | the status goes into the immunity mask `+0xE90` (`0x00239538`) |
| `2` | the status is added once, while the spawn record is fresh (`0x00239551`-`0x00239577`) |
| `1` | the same, when bit `0x1` of a shared gameplay LCG draw is set (`0x00239547`-`0x0023954F`) |
| `0` | nothing |

"Fresh" means bits `0x1` and `0x4` of the spawn record's first dword are clear (`0x002394DF`-`0x002394F9`); the
spawn record pointer `+0x6A0` is read with no null test, so a null one faults at `0x002394F7`. Codes 1 and 2 add
the status with `0x0030EAE0(record +0x698, 0, status, -1, -1, 0x297)` (`0x00239556`-`0x00239577`). After the
stats rebuild, `0x0030FED0` turns every bit of `+0xE90` into an immunity with `0x0030E360(..., mode 5)`,
which sets it in `+0x38` (`0x003103B2`-`0x00310413`). The stats rebuild clears `+0x38` first, so the loop puts
the immunities back on every rebuild.

### Enemy affinity changes

For an enemy with a battle unit, the rebuild then reconciles the five affinity bytes with the spawn
record (`0x00310415`-`0x003104BC`, [Elements](elements.md)):

- spawn record byte `+0` bit `0x80` set: the spawn record's `+0x78`-`+0x7C` are copied over stats
  `+0x40`-`+0x44`;
- clear: the stats bytes are copied into the spawn record.

The result applier sets that bit when it changes an enemy's affinities
([Action results](../Battle-Actions/action-results.md)), so the change survives the rebuild.

### The clamps

Last, the rebuild limits three values without going through the HP write (`0x003104BF`-`0x00310594`):

| Value | Limit |
|---|---|
| current HP `+0x48` | max HP `+0x24`, doubled under Bubble (status 28); under Disease (status 16), the current HP itself, at least 1 |
| current MP `+0x4C` | max MP `+0x28`, or 0 when augment 39 (Emptiness) is in either layer (byte `+0x6C` or `+0x7C`, bit `0x80`) |
| Mist pool `+0x06` | max MP times the MP bars `+0x37` (0 counting as 1), or 0 under augment 39 (Emptiness) |

The values only go down. Then `0x0030E060` sets the charge count `+0x4E` to `+0x06 / +0x28` when `+0x37` is
not 0, and to 0 otherwise (`0x0030E0AF`-`0x0030E0C3`, `0x0031059C`); it does nothing when max MP `+0x28` is 0 or less
(`0x0030E093`). With the rebuild's flags bit `0x2` clear, a changed count also goes to `0x0016D6A0`, a bare `ret`
(`0x0030E0C6`-`0x0030E0D5`). The new count is stored in `+0x4E` on every path past `0x0030E093` (`0x0030E111`).

When the rebuild's flags have `0x400` without `0x10` and the record has a battle unit (`0x0031B860`),
a changed count is posted as a hit or heal reaction with the difference (`0x003283D0`, `0x0030E102`;
[HP and KO](hp-and-ko.md)), which `0x003283D0` posts as a battle number through `0x003BBD00` (`0x00328462`,
[Battle numbers](../Menus-And-HUD/battle-numbers.md)).

### Damage Spikes

Damage Spikes (58) is bit `0x4` of the layer bytes `+0x6F` and `+0x7F`. After the recipe's slots the resolver calls
`0x00390F20(source, target, &context)` (`0x003863F8`), which tests it on the target first (`0x00390F2F`-`0x00390F46`). When the target holds it in either layer
and the damage the action resolved, the scratch word `0x02AEE004` ([Damage formula](damage-formula.md)), is not -1,
the user's HP loss `0x02AEE014` grows by the damage divided by 20, truncated, or is set to it while it is -1, and is
then held to 9,999 (`0x00390F48`-`0x00390F85`):

```python
spikes = trunc(damage / 20)                  multiply by 0x66666667, keep the high word >> 3, round toward 0
userHpLoss = min(9999, (userHpLoss == -1 ? 0 : userHpLoss) + spikes)
```

The damage is read before Greater Barrier's cut later in the same function (`0x00390F8B`-`0x00390FC3`). The resolver
then puts the user's HP gain minus that loss in result `+0x20` (`0x00386642`, `0x0038665B`). A 2,000-damage hit costs the
attacker 100 HP, and a hit of 19 or less costs nothing.

### Saboteur

Saboteur (18) is bit `0x4` of the layer bytes `+0x6A` and `+0x7A` and of the context byte `+0x1C`. Its one
fixed-position reader is the hit-rate slot 21 of the calculator, `0x00388F20`, which tests it in the merged context
(`+0x1C` bit `0x4`, `0x00388F2A`) and sets the hit chance `0x02AEDFE0` to 100 when it is set (`0x00388F37`); otherwise
the chance is the action row's `+0x12` less the target's Vitality plus the user's Magick Power
(`[0x02AEDFE0] = row[+0x12] - target[+0x2C] + user[+0x2B]`, `0x00388F8C`-`0x00388FA1`; [Formula slots](formula-slots.md)).

The recipes whose lists hold slot 21 are 3, 8, 9, 10, 12, 14, 15, 68 and 72.

Five functions test an augment by a computed id, and this is what each does with 18:

- the context merge `0x003847C0` walks ids 0-127 (`0x00384851`) and copies each layer bit into the context
  (`0x00384827`, `0x00384831`, `0x0038484C`), which is how the bit reaches `0x00388F2A`;
- the enemy-order selector tests augment `s` for opcodes 32 and 33 (`0x00302494`, `0x0030249B`;
  [Enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md)). 22 shipped orders test Saboteur (18) on
  the deciding enemy itself ([Enemy order sets](../Enemy-AI-And-Gambits/enemy-order-sets.md), whose [`enemy-orders.tsv`](../Enemy-AI-And-Gambits/enemy-orders.tsv) lists them):
  - 7 "has" tests, each guarding an order that clears it (action word `0x40E4`);
  - 15 "lacks" tests, each guarding an order that sets it (`0x40A4`);
  - in the areas frs_a, rui_c, rui_d, mnt_b, gil_g, pbc_c, mfr_c, gil_e, gil_f, tri_e, tri_f and tri_h;
- the state change `0x0030E130` tests the id's bit in both layers before and after the change (`0x0030E1BE`,
  `0x0030E1C9`; `0x0030E269`, `0x0030E26F`) to tell whether the state changed; the orders above reach it with 18, and so
  does the rebuild below;
- the timer pass `0x00385570` walks every id and reads the timer slot `+0x06` of each set augment's row
  (`0x00385619`); row 18's slot is `0xFF` ([Augment list](augment-list.md)), so the pass goes on to the next id
  (`0x0038561D`);
- the stats rebuild `0x002FEF30` tests only the 44 ids of its three lists `0x00D10290`, `0x00D102A0` and `0x00D102B0`
  (`0x002FF5CA`, `0x002FF668`, `0x002FF708`, loop ends `0x002FF638`, `0x002FF6D6`, `0x002FF776`), and 18 is in none of them.

Two functions read the layers whole:

- the rebuild from licences and equipment `0x0030FED0` XORs the old layer bytes with the new
  (`0x00310310`-`0x0031032E`) and calls `0x0030E130` for every id whose bit went off (`0x00310378`) or came on
  (`0x00310396`), 18 included, so a licence or equipment change that turns Saboteur on or off is applied through
  the same state change as an order;
- the party-member status builder `0x00329220` ORs the two layers into the record's `+0x4C`-`+0x5B`
  (`0x00329480`-`0x003294AF`; [Party member status record](../Characters-And-Objects/party-member-status-record.md)); of that
  copy only `+0x51` bit `0x2` (augment 41) is ever read (`0x002BFFAA`), so the copied bit `0x40000` is read by nothing.

No other instruction in the executable tests bit `0x40000`: no instruction reaches bit `0x4` of the stats record's `+0x1C`, `+0x6A` or
`+0x7A` outside the eight functions above, and the bit is stored nowhere but the two layers, the context byte and
the status record's copy.

## Shipped data

| Source | Count in the `us` data |
|---|---|
| License nodes of types 15-18 (`battle_pack.bin` section 12) | 87 of 361 (11, 21, 44 and 11 by type) |
| Augments those nodes grant | 87 different ids, each from one node |
| Scripts calling `btlAtelSetAbility` / `btlAtelSetStatus` | 502 each, 6,746 calls each |

Each augment's text is entry *id* of the augment text bank (text word `0x5000` + id in the augment table
`0x02EBF040`), for example 74 "Increases max HP by 30" and 20 "Gain MP after dealing magick damage".

## Modding notes

- An armor piece or accessory gives one augment: byte `+0x1A` of its equipment row. Weapons and shields
  are ignored here.
- A License node of type 15-18 can give up to eight augments, the words `+0x08`-`+0x16` of its row.
- An enemy's immunities are code 3 in its `btlAtelSetStatus` table; its augments are the two words of
  `btlAtelSetAbility`, read in reverse bit order.

## Related

- [Stats](stats.md) - the stats rebuild this one calls, and the attribute record.
- [Elements](elements.md) - the affinity bytes and Weatherproof.
- [Steal](steal.md) - Thief's Cuffs, augment 17.
- [Action results](../Battle-Actions/action-results.md) - the applier that changes enemy affinities.
- [HP and KO](hp-and-ko.md) - the HP write the HP clamp bypasses.
