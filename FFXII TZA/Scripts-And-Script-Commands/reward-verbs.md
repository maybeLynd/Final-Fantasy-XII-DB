---
title: "Reward verbs: every script verb that adds or removes items, gil, equipment or party members, and exactly what it writes"
kind: "system"
category: "Scripts and script commands"
summary: "The script side of rewards: the item verbs and the one inventory mutator they all reach, the gil verbs, the treasure chest sequence and the roll inside btlAtelOpenTreasureMessage that decides and grants the contents, what joining and leaving the party writes to the inventory and gil, the verbs that take away and give back everything, the quest result window, and the verbs that look like rewards but write nothing."
addresses: ["00345080", "003449A0", "0034A6D0", "0034ABF0", "0034B1E0", "003459C0", "00345520", "00344630", "0032A810", "0032A830", "0032A860", "00300B80", "00300BA0", "003008A0", "00346930", "00346E30", "0032A7F0", "003004B0", "00254EE0", "0050DEE0", "0032A800", "00354400", "00355830", "00356570", "00356A10", "0050FAF0", "002FAFD0", "002FB430", "02EC3E60", "0208CD18", "0034C370", "0034CDF0", "003172E0", "00328B20", "00316DF0", "00323540", "00349F90", "0034A790", "0030FBE0", "0030FAA0", "0034A300", "003497B0", "0030FD10", "00342230", "00328BD0", "00344C60", "00290130", "0050F200", "00510720", "003403E0", "0050F910", "02EBF190", "02EBF130", "00316A50", "00309F30", "0035DF20", "003272A0", "002FA260", "002FA470", "002F7FA0", "002341C0", "00236740", "00317480", "0030C470", "0035A620", "0035A630", "00320AB0", "00324380", "0035A250", "0030BAD0", "00559760", "003138D0", "00327CB0", "002398F0", "0030DD70", "0030DCB0", "0030DD10", "003F8C60", "003F4AA0"]
---

# Reward verbs: every script verb that adds or removes items, gil, equipment or party members, and exactly what it writes

## What the player sees

Talking to someone hands over an item with a "Received" message; a chest gives an item or gil; a
quest takes an item away; a story scene adds a character to the party or a guest joins; a prison
stretch strips everyone of their gear and gives it back later. Each of those is a script verb,
and every one of them ends in the inventory mutator `003008A0` or the gil store `00254EE0`.

## How it works

### Items

| Verb | Id | Handler | What it writes |
|---|---|---|---|
| `additem(item, count)` | `0x02E5` | `00345080` | pushes 1 as the message flag, pops flag, count and item, queues the "received" message (`002A3060(item, count, 1)`) and grants through `0032A810`; returns the new count |
| `additem_47f(item, count, msg)` | `0x047F` | `003449A0` | the same with an explicit message flag |
| `additemmes(item, count)` | `0x0480` | begin `0034A6D0`, poll `0034ABF0`, result `0034B1E0` | the begin queues the message without a grant flag (`002A3060(item, count, 0)`) and stores the pair; the poll runs while the message queue is busy (`002A2BF0` → `0035DF20(0)`, busy while `022CA430` is non-zero); the result grants through `0032A810` |
| `subitem(item, n)` | `0x02F2` | `003459C0` | `0032A810(item, −n)` |
| `setitemnum(item, n)` | `0x055C` | `00345520` | `0032A830(item, n)`: sets the count |
| `haveitem(item)` | `0x02E4` | `00344630` | `0032A860`: the count through `00309FB0`, floored at 0 |

`0032A810` is `00300B80(item, delta, 0)` with the result floored at 0, and `0032A830` the same
through `00300BA0`; both end in `003008A0(item, n, set, 1, mode)`, the one inventory mutator.

`003008A0` returns −1 for ids `0xFFFF` and `0x1000`, classes above `0xE` and an index at or past the
class's count at `01EEBCFC + class × 0x58`. Otherwise it reads the old count (`00309F30`) and calls
the class's handler from `01EEBD08 + class × 0x58`; when that slot is null it returns the old count
and writes nothing.

When its fourth argument is 1, the old count is below 1 and the new count is above 0, it sets
discovery bits in `[02EBF190] + 4`:

- class 3: bit 0, plus `01EECF98[s]`, where s is word `+0x2C & 7` (below 5) of the `02EBF138` row
  that byte `+2` of the `02EBF0F0` row `id − 0x3000` names;
- class 4: bit 6;
- key items: bit 7 for `0xC000` to `0xC011`, bit 8 for `0xC012` to `0xC01E`.

Grants made with another mode set no bits: `00300490` (mode 4) and `0030C410` (mode 2).

### Gil

`addgill(n)` (`0x02E7`, `00346930`) and `subgill(n)` (`0x02E8`, `00346E30`) call
`0032A7F0(±n)` → `003004B0(n, 0)`. `003004B0` computes `max(0, gil + n)` and hands it to
`00254EE0`, which records the change in statistics counter 6 (gain) or 7 (loss) through
`00316A50` and stores `min(total, 99,999,999)`; the gil window notify `00469E80` is skipped because
the flag is 0. The verb returns the uncapped value, so it can report more than is stored.

The debug verb `debug_setgill` (`0x20A3`, `0050DEE0` → `0032A800` → `00300500`) sets gil outright.
The `gillwinopen`, `gillwinclose`, `gillwinstart` and `gillwinsync` verbs (`0x0487` to `0x048A`)
drive the gil window and write nothing.

### Treasure chests

All 1,966 chest talk functions in the US scripts run the same calls in this order:

```
settrapshowstatus(0); ucoff(); btlAtelOpenTreasureStart(); talktreasure(id); sethpmenu_436(0, 5);
btlAtelOpenTreasureMessage(id); sethpmenu_436(1, 5); talktreasureafter(id); btlAtelOpenTreasureFinish(); ucon();
```

`setuptreasure` (`0x02BE`, begin `00354400`) places the chest actor and rolls its presence through
`002FAED0`: no chest when the opened flag `0032AA60(record[9])` is set, otherwise a chest when
`rand % 100` is below byte `+0xA` (script name bindings).

`talktreasure(ref)` (`0x02BF`, begin `00355830`) resolves the chest record through the reference,
has the controlled character approach it (`00269090`), stops its movement (`0026D6D0`) and disarms
the issuer's slot 2 (`0025D5E0(actor, 2)`); its poll `00355E20` waits on the interaction latch
`0208CD18`. `talktreasureafter` (`0x0414`, begin `00356570`, poll `00356A10`) waits on `00319180`,
the latch's getter, for the controlled character.

`btlAtelOpenTreasureMessage(ref)` (`0x3037`, begin `0050FAF0`) is the payout. It takes a message
record (`0035E550`), resolves the chest record through the reference and runs `002FAFD0`:

1. The opened flag is set (`0032AD70(record[9], 1)`) when byte `+9` is not `0xFF`, and the
   per-field presence ledger is marked (`002FB430(02EC3E60, field, record[0], 0)`).
2. `rand % 100` at or above byte `+0xB` gives an item, below it gil.
3. The alternate contents apply when the unit `003272A0` returns has `+0x6B` or `+0x7B` bit 1 set
   and none of the statuses `0x80000003`.
4. Item: a second `rand % 100` picks word `+0x10` (below 95) or `+0x12` with the alternate flag,
   otherwise `+0xC` (below 50) or `+0xE`. `0xFFFF` gives nothing; any other id gives one.
5. Gil: word `+0x16` with the alternate flag, otherwise `+0x14`. A word of 0 gives nothing. With
   record flag `+8` bit 6 the amount is `rand % word + 1`.

The verb then grants the item through `00300B80(item, 1, 0)` or the gil through `003004B0(gil, 0)`
and shows the message (`0035E500`, `0035DF40`).

The presence ledger at `02EC3E60` is a ring of three `{field, value bits, mask bits}` entries with
its cursor at `02EC3E84` and count at `02EC3E88`. Its other users are the clear `002FA260` (called
from `00233C10` and `00237DF0`), `002FA470` (called from `002341C0`, which adds an entry for field
`022BE940` with mask `0xFF` and value 0) and the reorder `002F7FA0`. None of them, nor `002FAED0`,
reads the value or mask bits to decide presence (immediate-address references to
`02EC3E60..02EC3E88`), so a chest's presence is re-rolled every time `setuptreasure` runs.

### Party membership

`addpartymember(sel)` (`0x0353`) grants through `003172E0`: a main character not already in the
nine slots at `[02EBF190] + 0x5A48` is written into a free index 4 to 8 of a staged copy and
activated with `00316DF0(record, 0)`. `removepartymember(sel)` (`0x0354`) clears the slot through
`00328B20` and deactivates with `00323540`. The guest verbs (`addguestbattlemember`,
`removeguestbattlemember`) and the treasure flag verbs are on [party verbs](party-verbs.md) and
script name bindings.

Activation `00316DF0(record, arg)` acts only on a record whose flags bit 4 is clear. Unless arg bit
1 is set while `00236740()` is 0, it first calls `00317480(record)` and, when `00236740()` is
non-zero and flags bit 3 is clear, `0030C470(record, 0x5A)`. For a party-side record (`+5` = 0)
with selector below `0x1A`:

- a main character (selector below 7) gets each of the five equipment words at `+0x50` as one owned
  item (`00300B80`) and one equipped count (`0030C410`, which counts class-1 ids other than
  `0x1000`);
- on the first activation (flags bit 3 clear), each entry of the `+0x88` list selected by the mask
  word at `+0xB8` grants its low half as an item; for a main character the id at `+0x22` of the
  action row its high half names is granted too (`00300490` below `0x1000`, `00300B80` otherwise);
- also on the first activation, the ten starting pairs of the character's row in `02EBF130`
  (`+0x58` ids, `+0x34` counts) and the starting gil `+0x3E` (`003004B0`).

Every activation then sets flags bits 3 and 4 and writes `+0x48`: `max(+0x48, 1)` when status bit
16 is set (`+0x64 | +0x3C`), otherwise `+0x24`, doubled when status bit 28 is set. Deactivation
`00323540` removes each equipped item once (`0030F9A0`, `00300B80(item, −1)`) and clears bit 4.

### Taking and giving back everything

`takeaway_item_and_equip` (`0x0388`, begin `00349F90` → `0035A620` → `0030FBE0`) walks the nine
roster indices (`00320AB0(i, 3)`), keeping records with `+5` ≠ 0 or a selector outside 7 to `0x19`:
each copies its five equipment words to `+0x5A` and clears the slots (`0031A300`). After
`00324380` it copies the class-0 counts at `[02EBF190] + 0x4748` to `+0x4F84` and the class-1
counts at `+0x47C8` to `+0x5004`, zeroing each through `003008A0(id, 0, set)`, bounded by
`01EEBCD0` and `01EEBD28`.

`giveback_item_and_equip` (`0x0387`, `0034A790` → `0035A630` → `0030FAA0`) adds the saved counts
back (bounded by `01EEBCFC` and `01EEBD54`), re-equips from `+0x5A` (`0031A710`), calls `00324380`
and clears the `0x83C`-byte backup. Both poll `0034A300`, which runs while `0030BAD0()` is
non-zero (`0035A250`) and then calls `00314D40(1)`.

`takeoff_equip(item)` (`0x055B`, `003497B0` → `0030FD10`) unequips one item id from every alive
main-character record (`0031A630(record, slot, 0xFFFF, 1)`).

`resetJobs(sel)` (`0x05D6`, `00342230` → `00328BD0`) refuses a selector above 5 (returns −1). It
clears the character's equipment (`0031A260`) and both job bytes `+0x1C3` and `+0x1C4`
(`00328990`), calls `00559760`, and, when the selector is the character recorded at
`[02EBF190] + 0x5AD5`, issues command `0x113` to party slot 3 (`003138D0(1)`,
[battle verbs](battle-verbs.md)) and calls `00313550(0)`.

It then rebuilds the ability list (`0030FED0(record, 0x97)`), calls `00327CB0` with the `+0x14`
word of the character's `02EBF130` row, and for selectors 0 and 5 adds one to byte `+0xBA` (capped
at 12). It calls `00326030` and `00327DE0`, clears `+0x68..+0x87`, `+0x37`, `+0x4E` and `+0x20`,
calls `00283270(1)`, sets `+0x1C3`/`+0x1C4` to `0xFFFF` and `+0x1C5` to `0xFF`. One US script uses it.

### The quest result window

`questresultwindow(n)` (`0x037C`, begin `00344C60`) resolves the quest row (`00473C90`, falling
back to row 0), takes capability row 3 (`002E1CD0(0, 3)`), opens the window through `00290130` and
raises busy bit 13 (`003601B0(0xD)`). `00290130` grants at once, when the window opens: it builds
the reward bundle (`003F8C60`, `0029014D`) and grants it (`003F4AA0`, `0029015B`), adding gil
straight through `00254EE0` (`gil + [bundle + 4]`) when flag bit 0 is set, and `(item, count)`
pairs and single ids through `00300B80`.

### Verbs that look like rewards and write nothing

`fs_setclanrank` (`0x7031`) and `btlAtelSetPcLevel` (`0x307F`) share `0050F200`, which pops two
values and jumps to the `ret` stub `0016D6A0`; `btlAtelAddMaxLicensePoint` (`0x3078`) and the
others on `00510720` pop one. `addclanpoint(n)` (`0x04DC`, `003403E0` → `002E2380`) adds to
statistics counter 17 (`00316A50(0x11, n)`) and no script uses it.

`btlAtelSetLevel(a, b)` (`0x3031`, `0050F910` → `002398F0`) sets a foe's level to a random value
from a to a + b (`0030C470(record, a + rand % (b + 1), a)`), refused when `[[unit + 0x6A0]] & 5` is
non-zero. The debug give-all verbs add 99 of every id (`003008A0(id, 99, 0, 1, 0)`): items
(`00510850` → `0030DD70`, class 0), equipment (`00510860` → `0030DCB0`, class 1) and event items
(`0050F0E0` → `0030DD10`, class 2).

## Layouts

```
inventory call   003008A0(item id, n, set, mode, arg): class = id >> 12, index = id & 0xFFF, class count at 01EEBCFC + class × 0x58
discovery bits   [02EBF190] + 4: bit 0 and 01EECF98[school] for magicks, bit 6 technicks, bit 7 key items 0xC000..0xC011, bit 8 0xC012..0xC01E
gil              003004B0(n, notify) = max(0, gil + n); 00254EE0 stores min(total, 99,999,999) and logs counter 6 or 7
chest record     +0 index in the field, +8 flags (bit 6 random gil), +9 opened-flag id, +0xA presence %, +0xB item %,
                 +0xC/+0xE item words, +0x10/+0x12 alternate item words, +0x14 gil, +0x16 alternate gil
presence ledger  02EC3E60: 3 × {u32 field, u32 value bits, u32 mask bits}, cursor 02EC3E84, count 02EC3E88
party record     [02EBF190] + 8 + selector × 0x1C8: +0 flags (bit 3 first activation, bit 4 active), +0x50 u16[5] equipment,
                 +0x5A u16[5] saved equipment, +0x88 u32[] grants with mask +0xB8 and count +0xBA
backup counts    [02EBF190] + 0x4F84 (class 0) and + 0x5004 (class 1), 0x83C bytes
```

## Shipped data

| Fact | Value |
|---|---|
| item verb uses in the US scripts | `additemmes` 4,364; `additem_47f` 2,136; `additem` 1,067; `subitem` 400; `haveitem` 4,044 |
| gil verbs | `addgill` 23, `subgill` 64 |
| chest sequence | 1,966 chests in 385 files, each calling the five chest verbs once |
| `questresultwindow` | 56 uses |
| inventory classes the mutator accepts | 0 to `0xE`, ids `0xFFFF` and `0x1000` refused |

## Operations

Per item verb: one message queue entry and one mutator call. Per chest: one roll and one grant.
Per party join: up to five equipment grants, the first-activation list, ten starting pairs and the
starting gil.

## State

The inventory counts and discovery bits in the party block, the gil total, each chest's opened
flag, the interaction latch `0208CD18`, the presence ledger, and the equipment backup words.

## Modding notes

- Every scripted item grant passes through `003008A0`; a hook there sees chests, talks, quests and
  party joins alike. The discovery bits are set on the first copy only for mode-1 grants, so the
  action ids a party join grants through `00300490` set none.
- A chest's contents are decided when it is opened, by the roll in `002FAFD0`; its presence is
  decided when `setuptreasure` runs and is never remembered.
- Joining the party grants the character's equipment and starting items; leaving takes only the
  equipment back.
- `additemmes` grants after the message closes, `additem` before it shows.
- `questresultwindow` pays out when the window opens, not when the player closes it.

## Related

- [Party verbs](party-verbs.md): the slot maps the membership verbs write.
- [Loot pickups](../Rewards-EXP-Gil-And-Loot/loot-pickups.md): the inventory mutator in full.
- [Gil](../Rewards-EXP-Gil-And-Loot/gil.md): the gil setter and its clamp.
- [Script verb table](verb-table.md): the ids and handlers.
