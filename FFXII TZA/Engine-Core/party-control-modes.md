[Home](../../README.md) / [Engine core](README.md) / Party control modes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Party control modes: the summon, chocobo, town and event-party levels and who may set them | system | Engine core | Main loop and game states | The level from 0 to 5 that 0x0030D9A0 computes from four bits of the party block and the current area's town flag; the script verbs and engine paths that set each bit and the side effects of the setters; the predicates and readers that ask for the level; the enter and leave handlers the transition dispatcher runs from its five-row table; what the level changes in the focus row and the party selection maps; and how the word is carried across an area change, restored and reset. | 0x0030D9A0, 0x00377C20, 0x00377C70, 0x003148F0, 0x003135C0, 0x00303EC0, 0x003072C0, 0x00307280, 0x003135E0, 0x00313550, 0x0035C620, 0x00303EE0, 0x00303D90, 0x003072E0, 0x00307240, 0x003072A0, 0x00307200, 0x0034E1F0, 0x0034FE80, 0x0050FFB0, 0x00355C40, 0x00356A30, 0x00347230, 0x00347820, 0x003514D0, 0x00355910, 0x00356630, 0x00351B40, 0x00355FE0, 0x00356DF0, 0x00351E50, 0x00356370, 0x003573A0, 0x0037C8F0, 0x0037C860, 0x003CA2E0, 0x0037C870, 0x0037C900, 0x0037C890, 0x0037C8B0, 0x0037CFF0, 0x0037CFC0, 0x0037D100, 0x0037D110, 0x0037D120, 0x00306760, 0x00328BD0, 0x00313840, 0x00584210, 0x00304680, 0x0035CA70, 0x0030D8B0, 0x002EA8E0, 0x002EA8B0, 0x003E7CC0, 0x003E7C70, 0x00313600, 0x00313730, 0x00313650, 0x00304180, 0x00304400, 0x00304060, 0x00304140, 0x0016D6A0, 0x00233AA0, 0x00233CF0, 0x0025D9E0, 0x0037C730, 0x0026CE60, 0x0037C980, 0x0037CA00, 0x0037CA80, 0x00326500, 0x003266C0, 0x00327850, 0x00327200, 0x003594B0, 0x00234590, 0x00300FC0, 0x0023B040, 0x00253C70, 0x00309A90, 0x00303CC0, 0x00303F00, 0x00304440, 0x00313590, 0x002EF3C0, 0x002EF410, 0x003139D0, 0x00304790, 0x003047C0, 0x0030DA10, 0x00237DF0, 0x003EBC50, 0x003EBD00, 0x002E73C0, 0x002EB030, 0x00314D40, 0x003139C0, 0x003138D0 |

## What the player sees

An Esper on the field, a chocobo under the party, a town, and a cutscene that has taken the party
over are four states the game keeps apart with one number. While an Esper is out, the summoner is
the character the game follows and the Esper holds the fourth place in the party selection. On a
chocobo the rider steers the mount and the other members leave the field. In a town the party is
never out of play from KO, Stone or X-Zone, and the town's own leader row is followed. During an
event the script owns the party: the gambits, the battle menu and the controls stop answering.

The four states rank. A script's event claim beats the town, the town beats a chocobo ride, and a
ride beats a summon, so riding into a town keeps the chocobo under the party while every rule that
asks "is the party riding?" answers no, and a summon that is still running when an event starts
waits in the background until the event's claim is withdrawn.

## How it works

### The level

`0x0030D9A0()` reads the dword at `[0x02EBF190] + 0x5B04` and returns the first match: bit `0x8` gives 5, bit `0x4` gives
4, the town flag `0x00377C20()` gives 3, bit `0x2` gives 2, and otherwise bit `0x1` gives 1 or 0; the dword is reloaded
after the town call. Only the bits `0xF` are consulted.

The town flag is authored data ([area flags](../World-Areas-And-Travel/area-flags-navimapdata.md)): `0x00377C20` takes the
area index `0x003148F0()`, checks it against the count at `[0x02ADD100] + 4` and returns bit `0x8000` of the 16-bit word
at `+8 + 3 × index`; with no table (`0x00377C33`) or an index not below the count (`0x00377C39`) it shifts the default
word `0x0FFF` instead (`0x00377C5F`) and returns 0, not a town.

| Level | Condition | Meaning | Set by |
|---|---|---|---|
| 5 | bit `0x8` | the second event-party claim | `seteventparty2mode` |
| 4 | bit `0x4` | the event-party claim | `seteventpartymode` |
| 3 | the area's town flag | a town | authored data |
| 2 | bit `0x2` | a chocobo ride | `ridechocobo`, `setchocobomode`, the mount stage of a special sequence |
| 1 | bit `0x1` | a summon | `summonread`, `btlAtelSetSummonMode`, the summon stage |
| 0 | no other row matches | | |

Four predicates compare the level: `0x003135C0` (= 1, thunk `0x0037C8F0`), `0x00303EC0` (= 2, thunks
`0x0037C860` and `0x003CA2E0`), `0x003072C0` (= 4) and `0x00307280` (= 5).

### The four bits and their setters

| Bit | Getter | Setter | What the setter does when the bit changes |
|---|---|---|---|
| `0x1` | `0x003135E0` (thunk `0x0037C900`) | `0x00313550(on)` | writes the bit, then `0x0035C620` (`0x00273E30` on `0x022CA408`, the width cache) |
| `0x2` | `0x00303EE0` (thunk `0x0037C870`) | `0x00303D90(on)` | on: the bit, the charge bits `0xC` set in `+0x5AE0` (three turbo charges), `+0x5AE4` = 180.0 (the ride time). Off: the bit cleared, the roster entry-3 actor's render record gets presentation request 3 (`0x002E73C0`), `+0x5AEC` = 0, and when `+0x5AE0` bit `0x2` (the turbo) was on, event `0x2001` to that actor (`0x002EB030`) and that bit cleared (a toggle guarded on the bit being set, so it never sets it) |
| `0x4` | `0x003072E0` (thunk `0x0037C8B0`) | `0x00307240(on)` | the bit only |
| `0x8` | `0x003072A0` (thunk `0x0037C890`) | `0x00307200(on)` | the bit only |

Every setter writes nothing when the bit already equals its argument. The compare takes the whole argument
(`0x00313563`, `0x00303DA9`, `0x00307256`, `0x00307216`), so a non-zero argument other than 1 always takes the on branch:
it rewrites a set bit, and for bit `0x1` runs `0x0035C620` again, for bit `0x2` refills the charges and the ride time
(`0x00303DB5`-`0x00303DD4`). Who calls them:

- bit `0x1` on: `summonread` (`0x0034E1F0`: `0x00313550(1)`, `0x00314D40(1)` sets `0x022C253D`, then the task
  installer `0x0037CA80`); `btlAtelSetSummonMode` (`0x0050FFB0`: pops the Esper's row into `+0x5AD4`
  through `0x003139C0`, then pops the on/off argument; the script's first argument is the one popped
  last); the summon stage of the special sequence
  `0x00306760` ([quickenings and summons](../Battle-Actions/quickenings-and-summons.md)).
- bit `0x1` off: `summontopartyread` (`0x0034FE80`: `0x00313550(0)`, `0x00314D40(1)`, `0x0037CA00`); the
  sequence's end; the party-row clear `0x00328BD0(row)` when the row is the summoner's `+0x5AD5`
  (after `0x003138D0(1)`); the reset `0x00313840`; the save handover `0x00584210` on both of its sides.
- bit `0x2`: `ridechocobo` (`0x00347230` → `0x0037CFF0` → `0x00303D90(1)`), `getoffchocobo` (`0x00347820` →
  `0x0037CFC0` → `0x00303D90(0)`), `setchocobomode(arg)` (`0x003514D0` → `0x0037D100`), the mount stage of
  the special sequence and its stage 6 (`0x022C215C` = 6: `0x00303D90(0)` at `0x00306A90`), the dismount `0x00304680`
  (which calls `0x00303D90(0)` first), state 1 of the task `0x0035CA70`
  ([chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md)).
- bit `0x2`, also: the load step `0x005843E0` (called from `0x00582860`), which clears the bit itself (`0x0058446A`) when bit `0x1000` of
  the dword at `[0x02EBF190] + 4` is set (`0x00236760`) and otherwise restores the mode flags through `0x002EF410`.
- bits `0x4` and `0x8`: only the verbs `seteventpartymode` (`0x00351B40` → `0x0037D120` → `0x00307240`) and
  `seteventparty2mode` (`0x00351E50` → `0x0037D110` → `0x00307200`); no engine path sets them.
- the restore `0x002EF410` writes the whole dword (below).

### The verbs

| Id | Verb | Handler | Does |
|---|---|---|---|
| `0x0203` | `summonread` | `0x0034E1F0` | bit `0x1` on, `0x022C253D` = 1, installs the summon task |
| `0x0207` | `summontopartyread` | `0x0034FE80` | bit `0x1` off, `0x022C253D` = 1, installs the task with step -1 |
| `0x3044` | `btlAtelSetSummonMode` | `0x0050FFB0` | bit `0x1` = the first argument, `+0x5AD4` = the second (the handler pops the last argument first) |
| `0x0408` | `getsummonmode` | `0x00355C40` → `0x0037C8F0` | level = 1 |
| `0x0512` | `getsummonmodebit` | `0x00356A30` → `0x0037C900` | bit `0x1` |
| `0x037E` | `ridechocobo` | `0x00347230` | bit `0x2` on |
| `0x037F` | `getoffchocobo` | `0x00347820` | bit `0x2` off |
| `0x03EC` | `setchocobomode` | `0x003514D0` | bit `0x2` = the argument |
| `0x0407` | `getchocobomode` | `0x00355910` → `0x0037C860` | level = 2 |
| `0x0511` | `getchocobomodebit` | `0x00356630` → `0x0037C870` | bit `0x2` |
| `0x050F` | `seteventpartymode` | `0x00351B40` | bit `0x4` = the argument |
| `0x0510` | `geteventpartymode` | `0x00355FE0` → `0x003072C0` | level = 4 |
| `0x0513` | `geteventpartymodebit` | `0x00356DF0` → `0x0037C8B0` | bit `0x4` |
| `0x0514` | `seteventparty2mode` | `0x00351E50` | bit `0x8` = the argument |
| `0x0515` | `geteventparty2mode` | `0x00356370` → `0x00307280` | level = 5 |
| `0x0516` | `geteventparty2modebit` | `0x003573A0` → `0x0037C890` | bit `0x8` |

The `…mode` getters return the level comparison and the `…bit` getters the raw bit: in a town or
under an event claim `getchocobomode` is 0 while `getchocobomodebit` is still 1.

### The transition dispatcher

`0x0030D8B0(commit)` reads the level, the previous level at `+0x5B08` and the town flag. It writes
the flag as bit `0x4` of the two source bytes `0x0215FD44` and `0x0215FD45` (`0x002EA8E0(2, town)` and
`0x002EA8B0(2, town)`): any set bit in a byte sets `0x02B59D70` or `0x02B59D71`, and the second byte's
value also runs, through `0x003E7C70(1 or 0)` (which stores it in `0x02B59D71` at `0x003E7C74`),
`0x003ACA80(0x20)`, `0x003AC8F0(0)` and `0x003E0B40(1)` when non-zero, else `0x003ACA90(0x20)`, `0x003AC8F0(1)` and
`0x003E0B40(0)`; the argument `0x20` is loaded for both arms at `0x003E7C7C`.

`0x003AC8F0(v)` stores the low byte of `v` in `0x02B3F502` (`0x003AC8F0`).

Then it indexes the table `0x01EECFC0`, five rows of four pointers: column 0
enters or stays without commit, column 1 leaves without commit, column 2 enters or stays with
commit, column 3 leaves with commit. Same level: that level's enter column. Changed: the old
level's leave column, then the new level's enter column, and with commit `+0x5B08` = the new
level. Level 5 has no row: nothing runs for it, though the level it replaces still gets its leave.

| Row | enter, no commit | leave, no commit | enter, commit | leave, commit |
|---|---|---|---|---|
| 0 | | | | |
| 1 summon | `0x0016D6A0` (return stub) | `0x00313730` | `0x00313600` | `0x00313650` |
| 2 chocobo | `0x00304180` | `0x00304400` | `0x00304060` | `0x00304140` |
| 3 town | `0x0016D6A0` | `0x0016D6A0` | `0x0016D6A0` | `0x0016D6A0` |
| 4 | | | | |

The handlers:

- `0x00313600`: countdown channel 2 = max(2.0, `+0x5AD8`) (`0x003EBC50(2, t)`, `0x003EBD00(2)`) and
  `+0x5AD0` bit `0x2` set: the summon timer runs.
- `0x00313730`: `+0x5AD0` bit `0x2` cleared, then the focus row = the summoner's `+0x5AD5` through
  `0x00327850`, which rebuilds the focus with `0x00326500`.
- `0x00313650`: with bit `0x1` already clear, the reset `0x00313840` (`+0x5AD5` = 0, `+0x5AD4` = `0x1B`,
  `+0x5AD0` bits `0x1` and `0x2` cleared, `+0x5AD8` and `+0x5ADC` = 0); with bit `0x1` set, nothing.
- `0x00304180`: collects up to nine main members (row type below 7, byte `+5` zero, status words
  clear of `0x80000003` or a town) into `0x022C1740` and makes the first the focus row; then, once
  per ride (unit flag bit `0x4000000`), snaps the mount's position and heading to the rider's (`0x00265020`,
  `0x0026B0C0`, `0x00392170`, `0x0026A0D0`, `0x0026B620`); `0x0035C900(1)` sets `0x022C83E8` bit `0x8`.
  - It returns at once, before the collection and `0x0035C900(1)`, when roster entry 3 has no unit
    (`0x0031B8C0(3)`, `0x003041A5`).
  - The collection runs only when the saved leader's member record (`0x00327240`) exists with byte `+5` zero and a
    row type from 7 to `0x19` (`0x003041B3`-`0x003041D7`).
  - The snap sets the unit flag (`0x00304398`), copies 16 bytes to the unit's `+0xD0` and `+0xE0`, the
    rider's position and a fourth stack dword to which `0x00304180` makes no store (`0x00304371`-`0x00304387`),
    copies the rider's heading (`0x00265200`) to `+0x15C` and `+0x160`, and calls `0x0026B0C0` only when the
    two positions differ (`0x00304322`-`0x00304347`).
  - `0x00304180` makes no test of the rider: when `0x0031ABF0` gives no actor (the leader in no seat or in
    seats 4 to 8, or a null seat pointer at `0x0209A1F0`), `0x00265020` and `0x00265200` give 0, 0, 0 and 0.0
    and the snap still runs toward them (`0x003042D3`-`0x003042FC`, `0x00263750`-`0x00263766`).
  - The members come from `0x00320AB0(i, 3)` for i 0 to 8. The three tests above run on
    each, the town test being a non-zero answer of `0x00377C20`, and a kept member's
    pointer goes to the next qword of `0x022C1740` (`0x00304210`-`0x0030425C`). The focus is
    set with `0x00327850(type)`, the type being byte `+4` of the first collected member
    (`0x00304280`-`0x003042AE`).
  - The rider is `0x0031ABF0(0x00327200())` (`0x003042D3`-`0x003042DA`). The position call
    `0x0026B0C0` and the heading calls `0x0026A0D0` and `0x0026B620` each run on
    `0x00263F40(unit +0x10)` and only when that is not null (`0x00304349`-`0x0030436C`,
    `0x003043B1`-`0x003043CF`); `0x00392170(unit +0x10)` runs between them (`0x0030438F`).
  - The position call is also passed over when the position `0x00265020` gives for the
    rider equals the one it gives for unit `+0x10` (`0x0030431C`-`0x00304347`). All the rider
    steps run only while bit `0x4000000` of the unit's first dword is clear
    (`0x003042C0`-`0x003042C8`), and they set that bit (`0x00304398`).
- `0x00304060`: attaches the rider (the selector entry of `+0x5AA4`, `0x00327200`) to the slot-3 unit
  (`0x002E28C0`, `0x002ECF10(rider, 1)`), `0x0025A160` of `0x0031B950(3)`, channel 1 = max(2.0,
  `+0x5AE4`), channel 2 = `+0x5AE8`, `0x00303F00(turbo bit)`, `+0x5AE0` bit `0x1` set.
  - It returns at once when roster entry 3 has no unit (`0x0031B8C0(3)`, `0x00304076`).
  - The turbo call's argument equals the bit, so it only sets the presentation request (1 or 3) and
    `+0x5AEC` (`0x00303F4D`-`0x00303F61`).
- `0x00304400`: `+0x5AE0` bit `0x1` cleared, `0x022C1F48 &= 0xF9`, `0x022C1F40` = 0, the rider detached
  (`0x002E6B10`).
- `0x00304140`: `0x0025A160` of the rider's selector entry; when bit `0x2` is already clear, the dismount
  `0x00304680` and `0x0035C770(0)`.

Two wrappers call the dispatcher. `0x00233AA0` (`0x0030D8B0(1)`, `0x00326500`, `0x00311E10(0)`,
`0x00311E20`) runs from the actor drive pass `0x0025D9E0` ([frame update
order](frame-update-order.md)) when the slot's byte `+0x200` has bit `0x2`, all four roster entries are
empty or have finished their pass (byte `+0x10` clear) and the manager's `+0x28` is 0, and from
state 3 of the summon task `0x0037C730` once `0x0037CB50()` succeeds.

`0x00233CF0` (`0x0030D8B0(0)`,
`0x003266C0`, `0x00311E10(1)`) runs from the manager runtime init `0x0026CE60` and from the task
installers `0x0037C980`, `0x0037CA00` and `0x0037CA80`, which place the task `0x0037C730` at `0x02EBF400`
with its entry `0x02EBF3FE` = 0 or 3 and its step `0x02EBF3FD` = 1 or -1. An installer reaches `0x00233CF0`
only when the allocator `0x002F16B0` returns a task: with a null one it still stores the null pointer at
`0x02EBF400` and the mode byte `0x02EBF3FC`, then returns without filling the task or calling the wrapper
(`0x0037C99A`, `0x0037CA1A`, `0x0037CA9A`).

`0x00233CF0` takes no argument. It makes the three calls in the order `0x0030D8B0`, `0x003266C0` and
`0x00311E10`, the second with no argument set, and answers 1 whatever they answer
(`0x00233CF4`-`0x00233D0A`).

### What the level changes

`0x0030D9A0` has 21 direct callers; the level-2 predicate has 6 direct callers and 16 through its
thunks; the level-1 predicate has 7 direct and 9 through its thunk. The ones read for this page:

- the focus row `0x00326500` (the commit wrapper and `0x00327850`): at levels 0 and 1 the saved leader
  `+0x5AA4`, at level 2 row `0x1A` (the chocobo), at level 3 the town's row `0x00377C70()` (mask `0x70`
  of the area record's third byte, shifted down by 4; 0 with no table or an area index not below the
  count, `0x00377C83`, `0x00377C88`, `0x00377CA4`), and at levels 4 and 5 the row `0xFF`, which no unit has.
  - When that row has no unit with a record it falls back to the first selection entry with one,
    then to `0x003589B0` of roster entry 0, so under an event claim the focus is the first selected
    unit; at level 1 it also runs `0x00317400(unit)`; the result goes out through `0x003594B0`
    (`0x022C7FE4`, `0x022C7FF8` = 1).
  - Before the pick it runs `0x00311E20` and `0x00326620` (`0x0032650C`, `0x00326511`). `0x00326620` acts at level 0
    only: when `+0x5AA4` is `0xFF` or not among entries 0 to 3 of `+0x5A5A`, it sets `+0x5AA4` to the row of
    the first unit `0x0030A880(list, 3)` returns and runs `0x00326500` again (`0x00326626`-`0x003266A9`).
    `0x00311E20` runs again before the request (`0x003265DB`).
- the [slot maps](../Party/party-slots.md#the-nine-seats) `0x003266C0` (the no-commit wrapper): map 0 at `+0x5A48` (nine 2-byte
  entries) is copied whole to `+0x5A5A` and `+0x5A7E`; entries 4 to 8 of the first copy are then
  set to -1 and it is copied again to `+0x5A6C` and `+0x5A90`. The per-level loops touch entries
  0 to 3 only, and `+0x5A7E` keeps all of map 0.
  - level 1: entry 3 becomes the Esper's row `+0x5AD4` (`0x003137E0`) in the three maps, -1 for row `0xFF`; of entries 0
    to 2 only the summoner's survives, the map-0 seat that `0x00313800` finds for the summoner's row `+0x5AD5` among all
    nine (`0x00320890`), and only when that seat is 0, 1 or 2: a summoner in seat 3, in seats 4 to 8 or not found keeps
    no entry (`0x003269D2`-`0x00326A32`);
  - level 2: entry 3 becomes row `0x1A` in the first and third maps and -1 in the second; the
    other entries are -1 except the rider's in the second map and entries 0 to 2 of the third;
  - level 3: the third map is first restored to its contents from before the rebuild, the town's
    row is looked up in it (entry 3 when the row is absent; `0x00377C70` answers 0 to 7, never `0xFF`), and only
    that entry survives in the first two maps;
  - level 4: only the leader's entry survives; under the town flag (`0x00377C20`) the surviving entry is
    instead the controlled member's seat (`0x003272F0`) holding the town's row, and when that seat or the
    leader's entry is not among entries 0 to 3 all four become -1 (`0x0032683F`-`0x003268EE`);
    level 5 does the same after restoring the third map and rewrites only the first two;
  - each changed entry goes through `0x0023A570`, then `0x00326500` runs and the active count
    `0x022C2670` is recounted.
- the field frame orchestrator `0x00234590` sets battle-state bit `0x800` at level 1 unless the summoner's
  unit is in play; the unit teardown `0x00300FC0` at level 1 runs `0x003138D0(0)` and the lock
  evaluator when the torn-down unit is the summoner's ([frame update order](frame-update-order.md)).
- the lock evaluator `0x0023B040` tests level 2, and at level 1 tests the summoner's unit
  (`0x0031B770(0x003137F0())`: no record, or status words holding `0x80000003` without the town flag,
  raises every lock bit); the input arbiter `0x00253C70` tests level 2.
  - At level 2 the evaluator skips the leader's derivation and publishes its start mask (all ones under
    `0x02089340` bit `0x40`, else 0; `0x0023B050`-`0x0023B06C`); at level 1 a missing summoner unit leaves the mask
    as it is (`0x0023B191`-`0x0023B194`).
- `0x00309A90`, the approach distance ([battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md)): 24.0 while the party is fighting (`0x00253B90()` = 0, [force fight
  mode](force-fight-mode.md)), else 3.8 at level 1 and 2.2 at any other level while fleeing.
- `0x00303CC0`: at level 2 only, the walkable-ground test `0x00336390` at the mount's position (`0x00265020`)
  with the larger of the rider's two `0x00265090` radii (`0x00303D21`-`0x00303D6C`), which allows a dismount; it
  returns 0 at any other level and when the mount or the rider has no actor (`0x00303D06`, `0x00303D1F`).
- `0x00303F00` grants a turbo at level 2 only and with a non-zero charge count (bits `0xC` of `+0x5AE0`,
  `0x00303F82`-`0x00303F92`), lowering that two-bit count by one, or refilling it to 3 while `0x0017D3A0()`
  holds (`0x00303FCD`-`0x00303FFD`).
- the ride's frame step `0x00304440` runs only while `+0x5AE0` bit `0x1` is set (`0x0030444B`-`0x00304452`);
  it refreshes `+0x5AE4` from channel 1 (`0x003EBA90(1)`, or 180.0
  while `0x0017D380()` holds) and `+0x5AE8` from channel 2, then ends the ride (`0x00311E20`,
  `0x0035CFA0(1)`) only when `0x00303CC0()` passes, channel 1 has expired (`0x003EBB70(1)`), `0x0017D380()`
  is 0, the level is 2 and `0x0031B8C0(3)` is non-null.
- after that the same step ends the turbo when channel 2 has expired (`0x003EBB70(2)`) and `+0x5AE0` bit `0x2`
  is on: presentation request 3 on the roster entry-3 actor (`0x002E73C0`), `+0x5AEC` = 0, event `0x2001` to
  that actor (`0x002EB030`, skipped when there is no actor) and that bit cleared (`0x003044EC`-`0x00304584`).
- `0x00313590`: at level 1, `0x0031E860(3)`, the actor handle of roster slot 3 (the Esper): `0x00263750(3)`, then
  `0x003589B0` of that actor, or 0 when the slot is empty ([identifier spaces](identifier-spaces.md)); at any other
  level 0.
- `0x00303E90` returns `0x0031E860(3)`, the handle of the mount in slot 3, when `0x0030D9A0()` is 2 and 0 otherwise;
  `0x003200A0` calls it (`0x00320116`).

The direct calls to `0x0023A570(unit, id)` come from three functions. The slot maps' call above (`0x00326B0A`), made for a
seat's roster actor (`0x00326A4A`) with a unit (`0x00326A5E`) whose present id differs from the seat's word
(`0x00326A64`-`0x00326A82`), is the only one that can pass a party id; their loop walks seats 0 to 3 only (`0x00326B15`).
`0x00300E40(unit, n)`, which calls the unit teardown `0x00300FC0(unit, 1)` at its start (`0x00300E59`), passes `0xFFFF`
(`0x00300F75`) for a unit without a stats record `+0x698` or whose record's byte `+5` is not 0 (`0x00300EDA`-`0x00300EEC`).

`0x0023A3B0(actor, n)`, which the begin `0x00510160` of `btlAtelSetUnit` calls with the value `n` it pops through
`0x00267E10` (`0x00510173`-`0x0051017D`), returns for an actor without a unit (`0x0023A3CF`). Otherwise it first runs
`0x002355A0` (`0x0023A3D4`), which can set the unit's bit `0x4000000` (`0x002356E2`), and passes `n | 0x100`, or `0xFFFF`
for `n` = `0xFF` (`0x0023A3D9`-`0x0023A3F1`); `0x0023A570` installs an `n | 0x100` id only while that bit is set
(`0x0023A641`-`0x0023A648`).

### Carried across an area change, restored and reset

`0x002EF3C0(rec)` captures `0x021B28E4` at `rec+4`, the ride block `+0x5AE0..+0x5AEF` at `rec+8`, the
summon block `+0x5AD0..+0x5ADF` at `rec+0x18` and the mode flags at `rec+0x28`.

`0x002EF410(rec)`
restores the ride block and the mode flags unconditionally; the summon block only when `rec+0x18` has
bit `0x2` (the summon timer was running), restarting channel 2 from `rec+0x20`, never below 2.0 (`0x003139D0`);
and when `rec+8` has bit `0x1` (the ride timers were armed) it restarts channel 1 from `rec+0xC`, never
below 2.0 (`0x00304790`), and channel 2 from `rec+0x10` as it is (`0x003047C0`), then sets bit `0x2` and clears
bit `0x1` of the mode flags (`0x002EF47E`-`0x002EF48C`). When both apply, the ride's load of channel 2 comes last and
stands.
`+0x5B08` is not captured.

`0x0030DA10` zeroes the mode flags and `+0x5B08`; its only caller is the battle-storage reset `0x00237DF0`, which also
runs `0x00313840`, the dismount `0x00304680`, and resets the speed index (`0x00229ED0(0)`, [frame update
order](frame-update-order.md)). The save handover `0x00584210` clears bit `0x1` on both of its sides ([save data
fields](../Saving-Loading-And-Settings/save-data-fields.md)): the stash at load mode 3 with the header flag `+0x57` bit
`0x1` clear (`0x005842C4`) and the restore at any other mode with that flag set (`0x0058438C`).

Load mode 3 with the flag set and any other mode with it clear leave the bit as it is (`0x0058424F`, `0x005842F3`).

## Layouts

Party block [`0x02EBF190`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x5A48` | `u8[18]` | slot map 0 | nine 2-byte seats |
| `+0x5A5A` | `u8[18]` | slot map 1 | nine 2-byte seats (seats 0-3 rebuilt by level) |
| `+0x5A6C` | `u8[18]` | slot map 2 | nine 2-byte seats (seats 0-3 rebuilt by level) |
| `+0x5A7E` | `u8[18]` | slot map 3 | a whole copy of map 0 |
| `+0x5A90` | `u8[18]` | slot map 4 | nine 2-byte seats (seats 0-3 rebuilt by level) |
| `+0x5AA4` | `u8` |  | saved leader |
| `+0x5AD0` | `u16` | summon flags | bit `0x2` the timer runs |
| `+0x5AD4` | `u8` | Esper's row | `0x1B` after reset |
| `+0x5AD5` | `u8` |  | summoner's row |
| `+0x5AD8` | `f32` | summon timer | one of the two summon timers |
| `+0x5ADC` | `f32` | summon timer | one of the two summon timers |
| `+0x5AE0` | `u32` | ride flags | bit `0x1` timers armed, bit `0x2` turbo on, mask `0xC` charges |
| `+0x5AE4` | `f32` |  | ride time |
| `+0x5AE8` | `f32` |  | turbo time |
| `+0x5AEC` | `u32` |  | last turbo argument |
| `+0x5B04` | `u32` | mode flags | bit `0x1` summon, bit `0x2` chocobo, bit `0x4` event party, bit `0x8` event party 2 |
| `+0x5B08` | `u32` | previous level | written by the dispatcher with commit |

Globals:

| Address | Type | Name | Meaning |
|---|---|---|---|
| `0x01EECFC0` | `void*[5][4]` | transition table | rows = levels 0-4; columns = enter, leave, enter with commit, leave with commit |
| `0x0215FD44` | `u8` | source byte | one of the two source bytes; bit `0x4` = the town flag (the dispatcher), bit `0x1` the world-lock apply |
| `0x0215FD45` | `u8` | source byte | one of the two source bytes; bit `0x4` = the town flag (the dispatcher), bit `0x1` the world-lock apply |
| `0x02B59D70` | `u8` | any-bit byte | "any bit set" of the two source bytes |
| `0x02B59D71` | `u8` | any-bit byte | "any bit set" of the two source bytes |

The area record table [`0x02ADD100`]:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `...` | count |  |
| `+0x08` | `...` | rows | rows of 3 bytes; word bit `0x8000` = town, byte +2 bits under mask `0x70` = the town's row |

Transition record:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `...` |  | captured `0x021B28E4` |
| `+0x08` | `u8[16]` | ride block | the ride block (16 bytes) |
| `+0x18` | `u8[16]` | summon block | the summon block (16 bytes) |
| `+0x28` | `...` |  | mode flags |

## Shipped data

| Fact | Value |
|---|---|
| the transition table | row 1 `0x0016D6A0`, `0x00313730`, `0x00313600`, `0x00313650`; row 2 `0x00304180`, `0x00304400`, `0x00304060`, `0x00304140`; row 3 `0x0016D6A0` four times; rows 0 and 4 null |
| the ride time | 180.0 (`0x43340000`) |
| the Esper row after reset | `0x1B` |
| the chocobo's row | `0x1A` |
| timer restart floor | 2.0 (`0x01CEBC08`) for the ride countdown on channel 1 (`0x00304790`) and the summon countdown on channel 2 (`0x003139D0`); the chocobo turbo countdown on channel 2 is restored as saved (`0x003047C0`) |
| `0x00309A90` | 24.0, 3.8, 2.2 |

## Operations

Per simulation step: the drive pass's commit run when the roster is settled; the orchestrator's
level-1 test; the ride's frame step. Per verb: one bit written and, for the summon verbs, the
no-commit run through the task installer. Per area change: the capture, the restore, and the
first dispatcher run after it.

## State

The mode flags and the previous level; the summon block; the ride block; the five slot maps, the saved
leader; the two source bytes.

## Modding notes

- An area's town flag outranks a chocobo ride and a summon without any code change: every
  level-2 and level-1 reader stops matching, while the two event claims still win.
- The two event claims come only from scripts; a script that sets one and never clears it leaves
  the party in an event configuration across area changes, because the mode flags are in the transition
  record.
- Level 5 has no row in the table: the level it replaces still runs its leave handler, but entering
  or leaving 5 itself runs nothing.
- The `…bit` verbs read the mode flags and the `…mode` verbs the level; a script that needs to know
  whether the party is physically mounted inside a town must use the bit.
- A saved ride forces the chocobo bit on and the summon bit off when restored; a saved summon
  survives only through the mode flags themselves and loses its bit at the save handover.

## Related

- [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md): the town flag and the town's row.
- [Chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md): the ride timers, the
  turbo and the dismount task.
- [Quickenings and summons](../Battle-Actions/quickenings-and-summons.md): the special sequence
  that sets the summon and mount bits.
- [Frame update order](frame-update-order.md): the drive pass and the orchestrator that run the
  dispatcher and test the level.
- [Save data fields](../Saving-Loading-And-Settings/save-data-fields.md): the transition record.
- [`party-control-modes-manager-0209ac60-accesses.tsv`](party-control-modes-manager-0209ac60-accesses.tsv): the
  accesses to the menu state block `0x0209AC60` (`0xE00` bytes, [menu screens](../Menus-And-HUD/menu-screens.md)) at its address
  or through the pointer `[0x0209AC30]` with a fixed displacement, each at its loop's first pass (1,027 rows).

  Not listed: the accesses that add an index register (the pointers from `+0xAC8`, the bytes from `+0xB2E`, the slots
  at `+0x170`, `+0x290`, `+0x2B8` and `+0x2C8`), the clear at `0x002800FA` and later loop passes.
- [`party-control-modes-manager-sub-0209ac60-02f8-accesses.tsv`](party-control-modes-manager-sub-0209ac60-02f8-accesses.tsv):
  every access to the description window that the block's `+0x2F8` points to (83 rows).
- [`party-control-modes-manager-sub-0209ac60-02f8-00c0-accesses.tsv`](party-control-modes-manager-sub-0209ac60-02f8-00c0-accesses.tsv):
  every access to the object at that window's `+0xC0` (128 rows).
- [`party-control-modes-party-selection-registry-ptrs-022c8388-accesses.tsv`](party-control-modes-party-selection-registry-ptrs-022c8388-accesses.tsv):
  the two stores of the party rebuild `0x0035BC50` to the four actor record pointers of the party slots at `0x022C8388`
  ([party list](../Menus-And-HUD/party-list.md)) (2 rows).

  Both sit in the four-pass loop `0x0035BDB0`-`0x0035BE6C`: `0x0035BDC3` writes all four pointers, `0x0035BDDF` the pointer of
  each slot that passes the tests at `0x0035BDC6` and `0x0035BDD2`; the clears `0x0035BB85` and `0x0035C573` zero them.

In the `route` cells of these tables, `Manager0209AC60` names the menu state block and `ManagerSub0209AC60_02F8` the
description window.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 1 call with 1 other topic</summary>

**Saving, loading and settings** (explained on [mrp menu resource packages](../Game-Files-And-Data-Tables/mrp-menu-resource-packages.md))

| Function | | Functions |
|---|---|---|
| `0x00582860` | calls | `0x00582790` |

</details>
