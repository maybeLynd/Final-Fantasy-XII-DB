---
title: "Gambits: how a character's gambit list is checked top to bottom, what runs before it, the three gambit sets and the authored presets"
kind: "system"
category: "Enemy AI and gambits"
addresses: "0x00305AB0, 0x00305CC0, 0x003014C0, 0x00308EC0, 0x00327DE0, 0x00326030, 0x00327CB0, 0x0030F760"
---

## What the player sees

When a character is ready to act:

1. **A command the player gave** is carried out first; the gambits are not looked at.
2. **Confuse**, and **Berserk** on a party member, replace the gambit list with their own behaviour.
3. Otherwise the **gambit list** is tried from the top. The first line whose target condition finds a
   target and whose action can be carried out is the one that runs; the lines below it are not tried.
   A party member whose record is not marked for gambits only carries out commands (below).
4. A line that is switched off, or has no condition or no action, is not in the list at all.
5. A "Foe" condition only picks an enemy that already holds enmity toward someone. An enemy that has not
   noticed anyone is not a gambit target until something raises its enmity ([Enmity](enmity.md)).

Each character has three gambit sets. All three start as copies of the character's preset, and the menu
chooses which one is used.

The game does not walk the menu's lines directly: it rebuilds the chosen set into the same kind of order list an enemy
reads from its area file, one order per switched-on line, copying each line's tests from its condition's row in
`battle_pack.bin`. The preset is also a row of `battle_pack.bin`, named by the character's party table row.

## How it works

### What runs before the gambits

`0x00305AB0(unit, resume)` picks the next action (`0x00305AB0`-`0x00305CB4`). A unit with flag bit `0x400000` first runs
`0x00308270` (`0x00305AC1`-`0x00305AC8`). Then:

1. **A pending command.** When unit flag `0x4000` is set it is cleared (`0x00305AEB`); the command's action
   `+0xBA0` and target `+0xBB8` are committed with `0x0030F760(unit, unit + 0xBA0, action, target, 1)`
   (`0x00305B2F`). Ids `0x4000`-`0x4166` (orders) skip the availability check `0x002FFCF0`
   (`0x00305AF6`-`0x00305B09`). A successful commit ends the turn.
   - Any other id that check answers non-zero for is dropped without a commit (`0x00305B10`); a refused or
     dropped command goes on to step 2 (`0x00305B36`).
2. **Confuse or Berserk.** When the unit has Confuse (status 5), or is an enemy-table unit with Berserk
   (27), the order set at `0x01EEC320` is walked instead (`0x00305B66`-`0x00305B90`). Outside a town the stats
   record is read here with no null test (`0x00305B66`-`0x00305B70`), so a unit without one faults.
3. **The unit's own lists.** The set at `+0x6E8` is walked; a party record with Berserk then walks the set
   at `0x01EEC370` (`0x00305BBB`-`0x00305BE5`) and, when that fails, goes on to step 5.
4. **The gambit list.** For a party record, the walk of the gambit set at `+0x6E0` happens only when bit `0x4`
   of its stats record's first dword is set; otherwise a command set at `+0x6F8` is walked if one is
   queued (`0x00305BE7`-`0x00305C32`). Enemy records walk `+0x6E0` with their subgroup `+0x6B5`
   ([Enemy AI](enemy-ai.md)). The `+0x6E0` walk first clears `+0x6F8` and `+0x748` (`0x00305C3C`-`0x00305C4C`).
   - A `+0x6F8` walk that does not commit clears `+0x6F8` and `+0x748` (`0x00305C23`-`0x00305C2C`).
5. **The last set** at `+0x6F0` is walked (`0x00305C61`-`0x00305C71`).
6. **Nothing matched.** Unless resuming, the unit commits order `0x4021`, a wait, from `0x01EEC298`
   (`0x00305C7E`-`0x00305C9B`, [Battle orders](../Battle-Actions/battle-orders.md)).

With bit `0x8000` of the active field record set, a party record skips steps 2-5 and goes straight to step 6
(`0x00305B3C`-`0x00305B57`), and every other unit skips step 2 (`0x00305B5D`-`0x00305B64`) and the `0x01EEC370` walk of
step 3 (`0x00305BB2`-`0x00305BB9`).

### The walk

`0x00305CC0(unit, set, subgroup, resume)` walks one subgroup of an order set (`0x00305CC0`-`0x00305E64`); a null
set returns 0 at once (`0x00305CF2`-`0x00305CF7`):

1. The set's first `0x20` bytes count the orders of each subgroup; the subgroup's first order is after
   the counts of all earlier subgroups (`0x00305D24`-`0x00305D97`). A subgroup with a count of 0 walks
   nothing.
2. For each order in turn it calls the evaluator `0x003014C0(unit, order, &action, &target)` and, when that
   matches, the commit `0x0030F760(unit, order, action, target, 1)` (`0x00305DC2`-`0x00305DF9`).
3. The first order that both matches and commits ends the walk with 1. Otherwise it moves 24 bytes on, up
   to the subgroup's count, which it re-reads every time (`0x00305DFD`-`0x00305E0A`).

In resume mode, an order with flag `0x80` is skipped, and while the order in flight (`[unit+0x708]`) has
flag `0x4000` only orders with flag `0x40` are tried (`0x00305D6B`-`0x00305DC0`). Reaching the order the context points at
returns 1 without trying it (`0x00305DA4`). A resumed commit also calls
`0x004697C0([unit+0x698], action, previous action, 4)` (`0x00305E31`-`0x00305E5A`), where the previous action is
`+0x714` as the walk began (`0x00305CE5`); a previous action of `0xFFFF` skips the call (`0x00305E3F`).

### One line's test

`0x003014C0` decides whether one order can run (`0x003014C0`-`0x0030180E`):

1. It decodes the action (`0x00308EC0`, below) into `*action` (`0x00301500`); `0xFFFF` fails.
2. Bit `0x20` of the battle flags `0x02089340`, the battle freeze, fails every order
   ([Boss fights](../Battle-Actions/boss-fights.md); `0x00301511`).
3. Every order but `0x414D` fails for a unit that cannot act (`0x0030151A`-`0x00301580`): its flag byte lacks
   bit `0x10`, it has no stats record, it has KO, Stone or X-Zone and the field's bit `0x8000` does not waive it, or it
   is an enemy-table unit whose spawn record's first byte has a bit of `0x30` or `0x48`. So a KO'd
   character's gambits never run.
4. An order with flag `0x800` fails while it is the unit's previous order `+0x738`; for an action id only
   when the previous command's `+0x730` bit `0x1` is set (`0x003015A6`-`0x003015C9`).
5. For an action outside the order band, the actor and the availability check must pass
   (`0x003015EA`-`0x00301606`), and an order with a non-zero chance word `c` at `+0x02` passes only when a shared
   gameplay LCG draw gives `0x00328370() % 100 < (s16)c` (`0x00301608`-`0x00301637`; the draw is `0x00328370`,
   [Random number generators](../Random-Numbers/random-number-generators.md)).
6. It builds the candidates for an action with `0x0030F130` (`0x00301649`). An order id instead must pass
   `0x00301830` and takes the unit's perception list `+0xBC0` as its candidates (`0x00301599`, `0x003015D4`-`0x003015E1`;
   [Enemy AI](enemy-ai.md)). Then it runs the order's tests, below.

### The target tests

An order holds three 6-byte tests from `+0x06`, each a relation, a sub-selector, an opcode and an operand.
`0x003014C0` runs them in turn (`0x00301681`, `0x0030176D`, `0x00301771`):

- a test whose relation is 0 is skipped (`0x00301685`);
- each test runs the selector `0x00301AD0` over the same candidates, unless bits `0x20 >> i` and
  `0x20 >> (i + 1)` of the order's flags are both set, which makes test i + 1 filter test i's result
  (`0x003016BE`-`0x003016E0`);
- a test that keeps no unit fails the order (`0x003016AD`);
- the target is chosen from what the first test kept, by `0x003087E0` (`0x003017BF`).

A gambit line copies its flags from the condition row's `+0x0E`, which is 0 in every shipped row, so a second
test only has to find one unit. Every test, opcode and pick rule of the shipped conditions is on
[Gambit conditions](gambit-conditions.md).

### The walk end to end

This section follows one line from the walk to the commit, with the candidate list it carries. The pieces are the
sections above and [Gambit conditions](gambit-conditions.md); this section strings them together and adds the list
record and the picker's selection, read at `0x003014C0`, `0x0030F130`, `0x003087E0` and `0x003083B0`.

1. **The order.** `0x00305CC0` hands `0x003014C0(unit, order, &action, &target)` one 24-byte order (`0x00305DD2`). The
   evaluator zeroes `*target` (`0x003014ED`), decodes the action word into `*action` (`0x00308EC0`, `0x00301500`) and
   runs the actor checks (One line's test).
2. **The candidates.** `0x0030F130(unit, action, out)` fills a `0x208`-byte candidate list (Layouts):
   - with the unit's float `+0x6D0` at 0 it copies the unit's own perception list `+0xBC0` whole
     (`0x0030F163`-`0x0030F1C6`);
   - otherwise it clears the list (`0x00316CF0`) and appends each perception entry (`+0xBC8`, `0x10` bytes each,
     `+0xBC4` of them) whose unit lies within `max(0x00265090 radii) + +0x6D0` of the unit's `+0x6C0`
     (`0x00319460`, `0x0030F1F0`-`0x0030F25A`);
   - then, for party slots 0-3 (`0x0031B810`), it appends the member when the action's status mask (`0x003872D0`)
     meets the member's statuses `+0x64 | +0x3C` in bits `0x1`, `0x2` or `0x80000000` (`0x0030F266`-`0x0030F2B2`): an action that
     removes KO, Stone or X-Zone sees those members even when perception does not.
3. **The tests.** Each of the order's three tests that runs (The target tests) writes the units it keeps with
   `0x00301AD0(unit, order, action, i, list, out)` into the list at the output pointer:
   - the pointer starts at the evaluator's frame `+0x460` and moves to `+0x460 + (i + 1) x 0x208` after test i runs
     unchained (`0x00301750`-`0x00301768`); a skipped test leaves it where it is;
   - a chained test i + 1 reads a copy of test i's list (frame `+0x40`) and writes over test i's list
     (`0x003016E2`-`0x0030174B`).
4. **The pick.** For an action id up to `0x21E`, the order `0x4023`, or the orders `0x4122`, `0x4123`, `0x414B` and
   `0x414E` (`0x0030177A`-`0x003017AD`), `0x003087E0(unit, list, out, action)` picks from the list at frame `+0x460`: the
   first test that ran, or the last test chained to it.
   - It drops every unit `0x003083B0(unit, candidate unit, action)` answers 1 for, the candidate's battle unit from
     its entry (`0x0031B760`, `0x00308839`-`0x00308848`;
     [Gambit conditions](gambit-conditions.md#units-the-action-would-not-change)).
   - With key type 1 (the integer arm, `0x003089C3`) or 2 (the float arm, `0x00308873`) at list `+0x01` it keeps the
     units with the highest (pick rule 3) or lowest (pick rule 2) key, ties kept together (`0x00308873`-`0x00308AEB`); any
     other pick rule with those key types keeps no unit, so the line fails (`0x00308925`, `0x00308A6A`). With any other
     key type it walks the list plain and keeps every unit that passed the filter (`0x00308825`-`0x0030886E`).
   - With more than one unit left, pick rule 1 draws `0x00328370() % count` (`0x00308B0D`-`0x00308B1C`); any other rule
     takes the unit nearest to the deciding unit by `0x0031E620(unit + 0xE0, candidate + 0xE0)` (`0x00308B2F`-`0x00308B76`);
     the result is an index into the output list.
5. **The target.** An empty output fails the line (`0x003017C4`-`0x003017CD`); otherwise `*target` is the chosen unit's
   actor handle `+0x08`, read through the entry's actor and its `+0x30` unit (`0x003017CF`-`0x003017E7`;
   [Battle unit fields](../Characters-And-Objects/battle-unit-fields.md)), and the evaluator returns 1. Any other action word
   returns 1 with `*target` still 0 (`0x003017E9`).
6. **The commit.** `0x00305CC0` passes `(order, *action, *target)` to `0x0030F760` (`0x00305DF4`) and the walk ends as
   The walk, step 3, says ([Committing an action](../Battle-Actions/action-commit.md)).

So a "Foe: HP < 50%" line reaches the commit only for a foe in perception that passes the relation and HP tests, is
not a unit the action would not change, and has the lowest HP % among them, the nearest on a tie
(`0x00308B2F`-`0x00308B76`).

### Which units a condition may pick

`0x0030BD00(unit, candidate, mode)` admits a candidate by the relation mode (`0x0030BD27`-`0x0030BE3E`). It first asks
`0x0030AB40` whether the two are on the same side (`0x0030AB40`-`0x0030AC41`):

- a null unit, a unit whose actor class nibble is 5, or one whose flag byte lacks bit `0x10`, is on neither
  side, and the answer is 0 (`0x0030AB64`-`0x0030AB70`, `0x0030AB93`-`0x0030ABB2`);
- a party record, or an actor of class nibble 3, is on the party side, and every other unit on the other
  side (`0x0030ABB8`-`0x0030AC0A`);
- a deciding unit under Confuse sees the two sides swapped (`0x0030AC14`-`0x0030AC25`); `0x0030BD00` passes flags 0
  (`0x0030BD1A`), so this Confuse test always runs. It reads the deciding unit's stats record with no null
  test, and no unit reaches it without one:
  - the flag bit `0x10` it needs first (`0x0030ABA6`) is set only by `0x0023412D`, after `0x00234123` has found
    `+0x698` non-null;
  - the reset `0x00236A60` nulls `+0x698` (`0x00236AB4`) only while it clears that bit (`0x00236AA6`).

| Mode | Admits | Gambit word | Site |
|---:|---|---|---|
| `0` | every unit | - | `0x0030BD45` |
| `1` | a unit on the other side | Foe | `0x0030BD6D` |
| `2` | a unit on the same side | Ally | `0x0030BD5E` |
| `3` | the unit whose id is the deciding unit's `+0x24` | - | `0x0030BDBC` |
| `4` | the deciding unit itself | Self | `0x0030BD4F` |
| `5` | a unit with the same team byte `+0x54` | - | `0x0030BDCB` |
| `6` | a unit on the same side other than itself | - | `0x0030BDDB` |
| `7` | a unit with the same team byte other than itself | - | `0x0030BDF1` |
| `8` | a unit with a different team byte | - | `0x0030BE08` |
| `9` | the deciding unit's current target `+0x710` | - | `0x0030BE18` |
| `10` | the unit in the deciding unit's `+0x748` | - | `0x0030BE2A` |

For mode 1, when a party record looks at an enemy-table record, the enemy must also hold enmity above 0
toward one of the 40 combatants (`0x0030BDA0`, `0x00321840` → `0x00321770`). Without it no Foe condition, not even
"Foe: party leader's target", picks that enemy.

### A weighted action

`0x00308EC0` reads the order's action word (`0x00308EC0`-`0x00308FCC`). A word below `0x8000` is the action id
itself. A word from `0x8000` is an index into the weighted table `[0x02EBF160]`: entries `index` to
`index + 1` of its pointer list bound a run of 4-byte entries (below), and a shared
gameplay LCG roll `r = LCG % 100` picks the first entry whose running weight sum is above `r`
(`0x00308F61`-`0x00308F99`). With no such entry the result is `0xFFFF`.

A word from `0x8000` whose index is not below the table's count `+0x00`, which is every such word while
`[0x02EBF160]` is null, comes back unchanged (`0x00308EDD`-`0x00308EFA`).

Each weighted entry, 4 bytes:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | action | the action id |
| `+0x02` | `u8` | weight | its weight in the roll |
| `+0x03` | `u8` | pad | not read by the pick |

### From the menu to the list

Each party member's twelve gambit lines are stored as a bank of `0x34` bytes in the party block
`[0x02EBF190]`: the bank of member `k` is `+0x5B10 + (k * 3 + selected) * 0x34`, with the selected set at
`+0x7370 + 4 * k` (`0x00327E27`-`0x00327E4B`). `0x00327DE0(stats)` rebuilds the member's order set at
`0x02089378 + type * 0x170` from it (`0x00327DE0`-`0x00327F70`):

- every line whose bit in the mask `+0x30` is set and whose condition and action are both not `0xFFFF`
  becomes one 24-byte order, in line order (`0x00327E60`-`0x00327F4B`);
- the order's action word is the line's action, and its flags and condition fields are copied from the
  condition's row of `0x02EBF0D8` (id `0x6000` + row, `0x00327EC1`-`0x00327F33`); the chance word `+0x02` is not
  written;
- the number of orders is stored as the count of subgroup 0 (`0x00327F60`).

A switched-off line is therefore not in the walked list.

The condition id is not range-checked here: the row is the table's word `+8` times `condition - 0x6000` plus the
value `0x0020E600` gives for the table's `+0xC`, added in 32 bits (`0x00327EC1`-`0x00327ED2`). A null `[0x02EBF0D8]` or
a 0 from `0x0020E600` leaves the row at 0 (`0x00327EDD`), and the first field read, word `+0x08` at `0x00327EDF`,
faults. Only the orders built are written, so those past the new count keep what they held.

The count is a byte store (`0x00327F60`). The bank and the selected set are read from `[0x02EBF190]` itself, with `k`
the stats byte `+0x04` (`0x00327DED`-`0x00327E4B`).

### The three sets and the presets

`0x00326030(state, k)` resets member `k`'s selected set to 0 and copies the 52-byte gambit block at stats
`+0x88`-`+0xBB` into all three banks (`0x00326039`-`0x003260D5`).

The stats record is the state's own `+8 + k * 0x1C8` while the low byte of `k` is at most `0x27`
(`0x00326041`-`0x00326054`). For a larger `k` the source pointer stays 0 and the first copy reads address `0x88`
(`0x00326057`), which faults; the selected-set store, with `k` sign-extended, comes before it (`0x00326033`-`0x00326039`).

That block is filled from an authored preset by `0x00327CB0(stats, preset)` (`0x00327CB0`-`0x00327DD9`). A preset
is a row of `0x02EBF0E0`, id `0x5000` + row, with twelve condition words from `+0x00` and twelve action words
from `+0x20`. The loader copies the pairs into the twelve 4-byte slots from `+0x88` until either word is
`0xFFFF`, sets a mask bit for each (`+0xB8`) and stores the count (`+0xBA`) (`0x00327D42`-`0x00327D84`). The unit
definition passes the party table row's word `+0x14` as the preset (`0x0023AEEE`).

The loader returns at once for a null record or one whose kind byte `+5` is not 0 (`0x00327CB3`, `0x00327CCE`). The
row address is the table's word `+8` times `preset - 0x5000` plus the value `0x0020E600` returns for the table's
`+0xC`, added in 32 bits (`0x00327D19`-`0x00327D26`). A preset that fails `0x00322C50(0xA, preset, 0)`, a null
`[0x02EBF0E0]` or a 0 from `0x0020E600` leaves the row at 0, and then no pair is read and the count is 0
(`0x00327CE8`-`0x00327D2A`, `0x00327D36`-`0x00327D40`).

The slots from the count to 11 are set to `0xFFFFFFFF` and their mask bits cleared (`0x00327D8A`-`0x00327DC0`), and
the loader ends with `0x00327DE0(stats)` (`0x00327DC5`).

The fresh stats record `0x0023AC80` calls `0x00327CB0`, `0x00326030` and `0x00327DE0` in turn (`0x0023AEF5`-`0x0023AF1D`,
[Battle unit construction](../Characters-And-Objects/battle-unit-construction.md)). The party-row reset `0x00328BD0`, run
by the script verb `resetJobs`, makes the same three calls (`0x00328CAA`-`0x00328D1E`,
[Party table](../Party/party-table.md), [Reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)).

## Layouts

The gambit bank, `0x34` bytes, three per party member:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16[24]` | lines | twelve (condition, action) pairs; `0xFFFF` = empty (`0x00327E6B`-`0x00327E80`) |
| `+0x30` | `u16` | enabled | bit value `1 << i` set: line i is on (`0x00327E60`-`0x00327E65`) |
| `+0x32` | `u8` | count | number of line slots the menu shows, 0-12; setgambit_slotmax adds to it (`0x00327930`) |
| `+0x33` | `u8` | pad33 | read and written by no instruction on its own; nothing fixes its width. It moves only inside the dword copies of `+0x30`-`+0x33`: bank to stats record `0x00234ED0` (`0x00234F30`, `0x00234F88`, `0x00234FE1`, `0x0023503A`, `0x0023509B`), the save image to a bank `0x00235AF0` (`0x00235BF8`), stats record to the three banks `0x00326030` (`0x00326095`, `0x003260CF`, `0x00326109`), `0x00327BE0` and `0x00327C40` (its bank lookup starts at `0x00327C60`) to a caller's copy (`0x00327C29`, `0x00327C9D`), a copy back to a bank `0x003282D0` (`0x00328347`), and the gambit screen's copy `0x005691E0` (`0x005695D5`) |

One order of a walked set, 24 bytes from set `+0x20`:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | action | action id, or `0x8000` + weighted-table index (`0x00308ECA`) |
| `+0x02` | `i16` | chance | percent chance the line is tried; 0 = always (`0x00301608`) |
| `+0x04` | `u16` | flags | `0x40` try while resuming, `0x80` skip on resume (`0x00305DB2`, `0x00305DBC`); `0x4000` on the order in flight limits a resume to `0x40` orders (`0x00305D7F`); `0x20` >> i with `0x20` >> (i + 1) chains test i + 1 to test i (`0x003016BE`); `0x800` not repeated while it is the previous order `+0x738`, an action id outside the order band only when the previous command's `+0x730` bit `0x1` is set (`0x003015A6`-`0x003015C9`); a gambit line takes the condition row's `+0x0E` (`0x00327F2F`) |
| `+0x06` | `u16` | relation0 | first test: relation mode, 0 = no test (`0x00301685`; row `+0x10`, `0x00327EEA`) |
| `+0x08` | `u8` | sub0 | first test: sub-selector (`0x00301B1A`; row `+0x08`, `0x00327EDF`) |
| `+0x09` | `u8` | opcode0 | first test: opcode; even = highest, set or at least, odd = lowest, clear or below (`0x00301B14`, `0x00301B44`) |
| `+0x0A` | `i16` | operand0 | first test: operand (`0x00301B1F`; row `+0x18`, `0x00327EF2`) |
| `+0x0C` | `u16` | relation1 | second test, from row `+0x11` (`0x00327F02`) |
| `+0x0E` | `u8` | sub1 | from row `+0x0A` (`0x00327EFA`) |
| `+0x0F` | `u8` | opcode1 | from row `+0x0B` (`0x00327EFA`) |
| `+0x10` | `i16` | operand1 | from row `+0x1A` (`0x00327F0A`) |
| `+0x12` | `u16` | relation2 | third test, from row `+0x12` (`0x00327F1A`) |
| `+0x14` | `u8` | sub2 | from row `+0x0C` (`0x00327F12`) |
| `+0x15` | `u8` | opcode2 | from row `+0x0D` (`0x00327F12`) |
| `+0x16` | `i16` | operand2 | from row `+0x1C` (`0x00327F22`) |

One gambit condition, a row of `battle_pack.bin` section 7 (`0x02EBF0D8`, 32 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8[3]` | pad00 | 0 in every row |
| `+0x03` | `u8` | b03 | `0xFF` in every row; copied to the menu record `+0x2C` (`0x0031D0CB`) |
| `+0x04` | `u16` | helpId | 16000 + row: the help line (`0x0031D0BE`) |
| `+0x06` | `u16` | value06 | 50, 70, 100 or 300; copied to the menu record `+0x28` (`0x0031D0B7`) |
| `+0x08` | `u8` | sub0 | first test sub-selector (`0x00327EDF`) |
| `+0x09` | `u8` | opcode0 | first test opcode (`0x00327EDF`) |
| `+0x0A` | `u8` | sub1 | second test sub-selector (`0x00327EFA`) |
| `+0x0B` | `u8` | opcode1 | second test opcode (`0x00327EFA`) |
| `+0x0C` | `u8` | sub2 | third test sub-selector, 0 in every row (`0x00327F12`) |
| `+0x0D` | `u8` | opcode2 | third test opcode, 0 in every row (`0x00327F12`) |
| `+0x0E` | `u16` | orderFlags | copied to the order's flags, 0 in every row (`0x00327F2F`) |
| `+0x10` | `u8` | relation0 | 1 Foe, 2 Ally, 4 Self (`0x00327EEA`) |
| `+0x11` | `u8` | relation1 | second test relation (`0x00327F02`) |
| `+0x12` | `u8` | relation2 | third test relation, 0 in every row (`0x00327F1A`) |
| `+0x13` | `u8` | pad13 | 0 in every row |
| `+0x14` | `u16` | nameWord | section 61 sub-table word >> 11, entry word & `0x7FF` (`0x0031D034`) |
| `+0x16` | `u8` | menuColumn | gambit menu column; `0xFF` = not listed (`0x002388F3`) |
| `+0x17` | `u8` | menuRow | gambit menu row (`0x00238903`) |
| `+0x18` | `i16` | operand0 | first test operand (`0x00327EF2`) |
| `+0x1A` | `i16` | operand1 | second test operand (`0x00327F0A`) |
| `+0x1C` | `i16` | operand2 | third test operand, 0 in every row (`0x00327F22`) |
| `+0x1E` | `u16` | pad1E | 0 in every row |

One candidate list, `0x208` bytes: the unit's perception list at `+0xBC0`, the evaluator's three test lists and the
picker's output all have this shape (`0x00316CF0` clears one, keeping bit `0x1` of `+0x00`; `0x00316CD0` appends). The entries
are laid out on [Area of effect](../Battle-Actions/area-of-effect.md#layouts):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | bit `0x1` is kept across a clear (`0x00316D10`-`0x00316D16`); the other bits are cleared with the list |
| `+0x01` | `u8` | keyType | 0 no key, 1 integer keys, 2 float keys: set with the pick rule by the selector (key 1 at `0x003022C7`, key 2 at `0x003027F4`, both bytes as a word at `0x00301ECC`); the picker reads it at `0x00308813` |
| `+0x02` | `u8` | pickRule | with key type 1 or 2: 2 lowest, 3 highest, any other value keeps no unit (`0x00308923`, `0x00308A68`); with any other key type: 1 random, any other value nearest (`0x00308B0D`) |
| `+0x03` | `u8` | pad03 | moved only by the whole-list copies in `0x0030F130` and `0x003014C0` (read at `0x0030F177`, `0x003016F7`; written at `0x0030F181`, `0x00301705`) and zeroed by the clear's memset (`0x00316D0B`); no instruction of `0x003014C0`, `0x0030F130`, `0x00301AD0`, `0x003087E0` or `0x00316CF0` reads it alone |
| `+0x04` | `i32` | count | entries in use; the append refuses at 32 (`0x00316CD4`); read at `0x00308828`, `0x00308AFB` |
| `+0x08` | `u8[512]` | entries | 32 entries of 16 bytes ([Area of effect](../Battle-Actions/area-of-effect.md) layout): `+0x00` the unit's actor (unit `+0x10`, `0x0030F242`, `0x0030F2A1`), `+0x08` the test's key, i32 or f32, `+0x0C` copied with the entry (`0x0030885B`, `0x00308A14`, `0x003088C8`) |

## Shipped data

The presets are `battle_pack.bin` section 8, 40 rows of 64 bytes. 29 party table rows name one in word
`+0x14`; rows 14 and 16 share `0x500E`, and rows 6 and 17-26 have no preset (`0xFFFF`). Presets `0x5006` and
`0x5010`-`0x501A` are named by no party row. Party rows 0-5 are Vaan, Ashe, Fran, Balthier, Basch and Penelo,
the characters the "Ally: Vaan" to "Ally: Penelo" conditions test, and rows 27-39 are the Espers.

Scenario preset rows load six of them: `0x5015`-`0x5019` in scenario sets 3-9 and `0x501A` in set 2 ([Scenario presets](../Party/scenario-presets.md), word `+0x0E`). A new game asks for set 0 (`0x003942F9`), `naf_b04` for set 1 and the developer script `evt_t0505` for sets 0, 2, 3, 11-13, 15, 17, 18, 20 and 22-49 (verb handler `0x0050F810`). No row of either table names `0x5006` or `0x5010`-`0x5014`, and the preset loader `0x00327CB0` takes its id only from those rows (`0x0023AEF5` and `0x00328CAA` from the party row's `+0x14`, `0x00239C00` from the preset row's `+0x0E`), so nothing loads these six.

All 40 rows, with their condition ids and action rows, are in [gambit-preset-list.tsv](gambit-preset-list.tsv),
read from the shipped file. The twelve presets no party row names hold "Foe: nearest visible → Attack": once in `0x5006` and
`0x5010`-`0x5019`, twelve times in `0x501A`.

| Preset | Party rows | Lines, top first |
|---|---|---|
| `0x5000` | 0 | Foe: party leader's target → Attack |
| `0x5001` | 1 | Ally: HP < 50% → Potion; Foe: nearest visible → Attack |
| `0x5002` | 2 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5003` | 3 | Ally: any → First Aid; Foe: nearest visible → Attack |
| `0x5004` | 4 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5005` | 5 | Foe: party leader's target → Attack |
| `0x5007` | 7 | Ally: HP < 50% → Cure; Foe: nearest visible → Attack |
| `0x5008` | 8 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x5009` | 9 | Foe: party leader's target → Attack; Foe: nearest visible → Attack |
| `0x500A` | 10 | Ally: HP < 30% → Cura; Ally: HP < 50% → Cure; Self: HP < 70% → Potion; Foe: targeting self → Attack; Foe: nearest visible → Attack; Ally: any → Poisona; Ally: any → Blindna; Ally: any → Vox |
| `0x500B` | 11 | Foe: flying → Telekinesis; Foe: party leader's target → Attack; Foe: targeting self → Attack; Foe: targeting ally → Attack; Foe: nearest visible → Attack; Foe: any → Attack |
| `0x500C` | 12 | Foe: flying → Telekinesis; Foe: party leader's target → Attack; Foe: targeting self → Attack; Foe: targeting ally → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Phoenix Down |
| `0x500D` | 13 | Ally: HP < 50% → Cura; Self: HP < 70% → Potion; Foe: party leader's target → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Poisona; Ally: any → Blindna; Ally: any → Vox |
| `0x500E` | 14, 16 | Foe: party leader's target → Attack; Foe: targeting ally → Attack; Foe: targeting self → Attack; Foe: nearest visible → Attack; Foe: any → Attack; Ally: any → Arise; Ally: any → Serum; Ally: any → Gold Needle; Ally: any → Echo Herbs; Self: HP < 30% → Domaine Calvados |
| `0x500F` | 15 | Foe: nearest visible → Attack |
| `0x501B` | 27 | `0x60FF` → Hellfire; Foe: fire-vulnerable → Painflare; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501C` | 28 | `0x60FF` → Frostwave; Foe: ice-vulnerable → Flash-Freeze; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501D` | 29 | `0x60FF` → Judgment Bolt; Foe: lightning-vulnerable → Flash Arc; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x501E` | 30 | `0x60FF` → Gaia's Wrath; Foe: earth-vulnerable → Roxxor; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x501F` | 31 | `0x60FF` → Blight; Foe: undead → Attack; Foe: nearest visible → Malaise; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5020` | 32 | `0x60FF` → Tsunami; Foe: water-vulnerable → Briny Cannonade; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5021` | 33 | `0x60FF` → Condemnation; Foe: nearest visible → Kill; Foe: nearest visible → Attack; Ally: HP < 100% → Cura |
| `0x5022` | 34 | `0x60FF` → Soul Purge; Foe: nearest visible → Devour Soul; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5023` | 35 | `0x60FF` → Tornado; Foe: wind-vulnerable → Whirlwind; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5024` | 36 | `0x60FF` → Big Bang; Foe: nearest visible → Gravity Well; Foe: nearest visible → Attack |
| `0x5025` | 37 | `0x60FF` → Meteor; Foe: nearest visible → Comet; Foe: nearest visible → Attack; Ally: HP < 100% → Curaja |
| `0x5026` | 38 | `0x60FF` → Eschaton; Foe: holy-vulnerable → Redemption; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |
| `0x5027` | 39 | `0x60FF` → Final Eclipse; Foe: dark-vulnerable → Banish Ray; Foe: nearest visible → Attack; Ally: HP < 100% → Renew |

Every Esper preset starts with condition `0x60FF`, which takes the foe with the highest max HP while the summon
timer is below 20 ([Gambit conditions](gambit-conditions.md)).

### Columns of gambit-preset-list.tsv

| Column | Holds |
|---|---|
| `line_text` | the preset's lines, top first, as `N. condition: action` separated by semicolons: the condition's name from its id in `conditions` and the action's name from its row in `actions`; a preset holds up to twelve lines and ends at the first `0xFFFF` |
| `used_by` | who loads the preset: each party table row that names it in word `+0x14`, as row number and name (`0 Vaan`, `14 Reddas, 16 Reddas`), and for `0x5015` to `0x501A` the scenario sets whose rows load it, with the characters (`scenario 8 Vaan, scenario 9 Ashe`); the six presets no row names (`0x5006`, `0x5010` to `0x5014`) say so |

## Modding notes

- A character's starting gambits are the preset its party row names in `+0x14`; editing a preset row
  changes every character that uses it.
- Order of lines is priority: the walk never re-sorts them.
- A line's percent chance and weighted action are features of the order format; the gambit rebuild
  writes neither, so a party line's action is the one the menu shows.

## Related

- [Gambit conditions](gambit-conditions.md) - every target condition.
- [Enemy AI](enemy-ai.md) - the same walk for enemies and the subgroups.
- [Enemy order sets](enemy-order-sets.md) - every shipped enemy order, in the 24-byte order layout.
- [Action commit](../Battle-Actions/action-commit.md) - `0x0030F760`.
- [Battle orders](../Battle-Actions/battle-orders.md) - the order ids, including `0x4021`.
- [Boss fights](../Battle-Actions/boss-fights.md) - the battle freeze.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Resource: `0x005691E0` calls `0x00249580`; those functions are documented on
  [battle text tables](../Game-Files-And-Data-Tables/battle-text-tables.md).
- Save load settings: `0x00234ED0` is called by `0x005844A0`; `0x00235AF0` calls `0x002EF640`; those functions are documented
  on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [global state accessors](../Engine-Core/global-state-accessors.md).
