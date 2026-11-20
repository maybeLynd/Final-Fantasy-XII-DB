[Home](../../README.md) / [Battle actions](README.md) / Area of effect

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Area of effect: radius, cone and line targeting, which side an area hits, and the target list | system | Battle actions | How an action runs | How a battle action turns its one chosen target into everyone it hits - the radius byte, a circle on the target or on the user, cones and lines, the side rule that follows the chosen target and ignores Confuse, which units an area skips, the whole-party flag and the 32-entry target list. | 0x0030D160, 0x0030AB40, 0x002FFF50, 0x0031A990, 0x00316CF0, 0x00316CD0, 0x00316D70 |

## What the player sees

The player, a gambit or an enemy's AI picks one target. Everyone else the action hits is gathered
later, when the action's state machine reaches its target step, from where everybody stands at that
moment.

- **Radius.** An action with a radius of 0 hits only its target. Otherwise it hits units within that
  distance on the ground (height is ignored). Fire, Cure and Protect have no radius; Fira has 8, Cura, Curaja and Protectga 10, and the eight attack spells ending
in -ja 100, which covers any battle area.
- **Centre.** The circle is centred on the target, except for actions centred on the user, such as
  the cries and songs (Screech, Wail, Angelsong, the Soundwaves), with a radius from 6 to 100. Every
  one is in the table under [Shipped data](#shipped-data).
- **Cones** (for example the breaths, the gazes, Flash and Tremor; every one is under
  [Shipped data](#shipped-data)) hit units in the radius that are also within an
  angle either side of the line from the user to the target. On most of them that angle is 180
  degrees, which makes the cone test pass for everyone in the radius, so the area is the plain
  circle around the target. Two cones have an angle of 0, which in practice leaves the target alone.
- **Lines** (Gust, Gale, Judgment, Innocence, Mach Wave) hit units in the radius whose sideways
  distance from the line between the user and the target is small enough.
- **Side.** An area spreads to the units on the same side as the chosen target, whichever side the
  user is on: Fira on an enemy spreads to its allies, Cura on a party member spreads to the party.
  Confuse on the target does not turn this around. Self-Destruct spreads to the other side from its
  target, and Mass-Destruct hits everyone in range.
- **Who is skipped.** Units that are KO, Stone or X-Zone (except in towns, whose town flag waives this;
  [Area flags](../World-Areas-And-Travel/area-flags-navimapdata.md))
  and units failing the other targeting checks below are not added. An Invisible enemy is not
  skipped by this test.
- An action hits at most 32 units.

## How it works

### The gatherer

`0x0030D160` (1,004 bytes) is called once, by the standard-action state machine at
`0x00304EE2`, as `(unit, effectiveActionId, focusHandle, buffer)`: the action id comes from
`0x00387090`¹, the focus handle from the action state `+0x60`, and the buffer is the
action's target list, at action state `+0xC8` (the action state, [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), starts at unit `+0x6B0`, so the list is at unit `+0x778`)². It returns the list's count³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00304ECC` |
| ² | `0x00304ED1`-`0x00304EE2` |
| ³ | `0x0030D51C` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | The chosen target is resolved from the focus handle; if it does not resolve the function returns 0 and leaves the list alone. | `0x0031B7E0`<br>`0x0030D18A`-`0x0030D195` |
| 2 | The action row is `table + stride * id`, with the table at `0x02EBF138` (base through `0x0020E600`, stride the `u16` at table `+8`). | `0x0030D19B`-`0x0030D1E9` |
| 3 | The list is cleared, keeping bit `0x1` of its flag byte, and the chosen target is appended first. | `0x00316CF0`<br>`0x0030D1F3`-`0x0030D200` |
| 4 | **Stats-record path.** When the user's stats-record list (below) is not empty, nothing below runs; with a radius the list is rewritten from the mapped battle slots. | `0x0030D205`-`0x0030D250` |
| 5 | **Radius.** With the row's byte `+0x06` at 0, the area pass is skipped. Otherwise the radius is squared and compared with squared XZ distances. The centre is the user's position (unit `+0xE0`) when bit `0x200000` (`0x200000`) of the flag word `+0x0C` is set, otherwise the chosen target's. | `0x0030D255`-`0x0030D26B`<br>`0x0030D2BD`, `0x0030D3A3`-`0x0030D3AC`<br>`0x0030D271`-`0x0030D29B` |
| 6 | **Heading.** When bit `0x1000000` or `0x2000000` is set (`0x3000000`, `0x0030D2C0`), the heading from the user to the chosen target is computed (`0x0031AC90`; the user's facing `+0x160` when the two positions coincide in X and Z). The row's byte `+0x07` is kept as a width and, times 2 pi / 360, as an angle. | `0x0030D2D2`-`0x0030D2E7`<br>`0x01CEBC78`, `0x00902438`<br>`0x0030D2EC`-`0x0030D308` |

What the gatherer needs and leaves is in
[`call-signatures-contracts.tsv`](../Engine-Core/call-signatures-contracts.tsv). It stores neither the
unit nor the list in memory. The list keeps each hit unit's `+0x10` value. It writes up to four unit pointers at
`0x022C1788` when bit `0x2` of the row's `+0xC` is set¹, and takes no lock to do so.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030D4B8` |

</details>

### Candidates

Every slot from 0 to `0x00236850()` whose unit has bit `0x10` of its first byte set¹ is a
candidate; the chosen target itself is skipped². A candidate is appended with
`0x00316CD0`³ when it passes these tests, in order:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00321170` |
| ² | `0x0030D313`-`0x0030D34D` |
| ³ | `0x0030D422` |

</details>

| Test | Passes when |
|---|---|
| eligibility | `0x002FFEF0(candidate, user, 1)` returns non-zero (`0x0030D35F`); see below |
| side | bit `0x8` of the row's word `+0x36` is set, or the side predicate called as `(chosenTarget, candidate, 1)` returns 0 (`0x0030D36C`-`0x0030D391`) |
| distance | the candidate is inside the radius (`0x0030D3A8`) |
| cone (bit `0x1000000`) | the absolute angle between the heading and the user-to-candidate heading, normalised to plus or minus pi by `0x0031A930`, is not above the angle (`0x0030D3B1`-`0x0030D3E1`) |
| line (bit `0x2000000`, bit `0x1000000` clear) | the candidate's offset from the user, rotated into the heading by `0x00325EA0`, has an absolute sideways component not above the width (`0x0030D3E3`-`0x0030D419`) |

The side predicate is `0x0030BB10` when bit `0x4` of `+0x36` is clear (it returns 1 for relationship class
0 or 2) and `0x0030BCB0` when bit `0x4` is set (1 for class 0 or 1). The two are loaded with `lea` and
called through `rax`.

### Whole party

When bit `0x2` of the flag word is set - whatever the radius - the units at the four party positions
(`0x0031B810(i)`, the slot byte at `[0x02EBF190] + 0x5A5A + i*2`) are appended, unless already in the
list¹. Only units that have a stats record and either none of status bits `0x1`, `0x2` and `0x80000000`² or a non-zero `0x00377C20()` count; they are staged in `0x022C1788` first³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00316D70` |
| ² | `0x80000003` |
| ³ | `0x0030D461`-`0x0030D50A` |

</details>

### The stats-record list

Besides the unit list, the user can carry a list of stats-record indices (actor type ids): count
`+0x6B6`, bytes from `+0x6B9`.

- The commit `0x0030F760` puts one entry there (from `0x022C1DB8 + 12 * [unit+0xEA9]`) when bit `0x2` of the
  command word `unit+0x6B0` is set¹.
- The action reset `0x003105D0` clears it².
- The effect applier `0x00307300` resolves each byte through `0x00320A40` and applies the result to it
 ³.
- With a radius, the gatherer rewrites the list from index 0: each mapped battle slot 4 to 8 whose
  stats record exists (`0x00320AB0(slot, 3)`) contributes its byte `+0x04`, and the new count goes to
  `+0x6B6`. Without a radius the committed entry stands.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030F865`-`0x0030F894` |
| ² | `0x0031060A` |
| ³ | `0x003073D7`-`0x0030744B` |

</details>

### The relationship class

`0x0030AB40(a, b, flags)` returns 0 when either unit is null, either
actor's class nibble¹ is 5, or either unit lacks bit `0x10` of its first byte². A unit is on the party side when its stats byte `+0x05` is 0 or its class
nibble is 3. The result is 1 when both are on the same side and 2 when not; when bit `0x1` of `flags` is
clear and `a` has status bit `0x20` (Confuse) in `+0x64 | +0x3C`, the answer is swapped³. The gatherer passes 1 to the side predicates, so Confuse never changes
an area's side.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263C20` |
| ² | `0x0030AB64`-`0x0030ABB2` |
| ³ | `0x0030ABB8`-`0x0030AC25` |

</details>

The Confuse test reads `a`'s stats record `+0x698` with no null test¹ when bit `0x1` of `flags` is
clear. No `a` reaches it without a record: the flag bit `0x10` tested first² is set only by `0x0023412D`,
after `0x00234123` has found `+0x698` non-null, and the reset `0x00236A60` nulls `+0x698`³ only while it
clears that bit⁴. With the bit set the test is skipped and the answer is the side
answer alone⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030AC14` |
| ² | `0x0030ABA6` |
| ³ | `0x00236AB4` |
| ⁴ | `0x00236AA6` |
| ⁵ | `0x0030AC0C`-`0x0030AC12` |

</details>

### Eligibility

`0x002FFEF0(candidate, user, mode)` asks `0x0030AB40(candidate, user, 0)` - here
Confuse on the candidate does count - and passes 1 as the hostile flag when the class is above 1,
else 0. It returns 1 when `0x002FFF50(candidate, hostile, mode)` returns an empty mask¹. `0x002FFF50` sets:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FFF07`-`0x002FFF35` |

</details>

| Bit | When |
|---|---|
| `0x01` | the unit is null or lacks bit `0x10` of its first byte; the mask is then 1 alone, with every later test skipped (`0x002FFF67`-`0x002FFF73`, `0x00300042`) |
| `0x02` | no stats record, or status bits `0x1`, `0x2` or `0x80000000` (KO, Stone, X-Zone) set while `0x00377C20()` returns 0 |
| `0x04` | `0x003125E0(unit)` returns non-zero: for an active unit, when its flag word has bit `0x200`, `0x400` or `0x800`, the word at `+0x04` has bit `0x4`, bit `0x2` is set while the unit has no stats record or is KO, Stone or X-Zone (without the map waiver), or, for an enemy-side unit, bit `0x8` or `0x10` of the dword at `[unit+0x6A0]` is set |
| `0x08` | `0x0030B950(unit, hostile)` returns non-zero: any of bits `0xE00` of `0x02089340` (`0x0030B770` bits `0x4`, `0x8` and `0x10`; its bits `0x1` and `0x2` are masked out by `0xFFFC`, `0x0030B975`), or `0x0030B7F0` - unit flag bit `0x100`, unit flag bit `0x40000000` when `hostile`, a party-side unit of type id `0x1A` - tested through the 16-bit mask `0xFFF7` (`0x0030B97F`), so the unit answer `0x8` (`+4` bit `0x20`) does not count, and neither does `0x0017D470()` in state 1 or 2, whose bits `0x10000` and `0x20000` (`0x0030B8A6`, `0x0030B8C0`) lie above the tested word |
| `0x10` | enemy side (stats `+0x05` = 1), `mode` is not 1, and status bit `0x1000000` (Invisible) set |
| `0x20` | enemy side, `mode` is not 3, and bit `0x20` of the byte at `[unit+0x6A0]` |
| `0x40` | enemy side and bit `0x40` of the byte at `[unit+0x6A0]` |

The gatherer uses mode 1, so bit `0x10` is never set for its candidates. `0x00377C20` returns bit `0x8000`
of the current field's map-info word.

### Entry flags

The effect applier `0x00307300` writes each entry's `+0x08`: the low byte is the
outcome code from `0x0030DAE0`¹, and bits `0x100`, `0x200`, `0x400` and `0x800` are set from result flags 3, 2, 1
and 0 (bit `0x400` only when bit `0x200000` of the user's word `+0x04` is clear, `0x003075C3`-`0x003075EC`). None of these
steps clears a bit: the code is a byte store² and the four bits are ORed in³, so a
bit already set in `+0x08` stays set.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003075BF` |
| ² | `0x003075BF` |
| ³ | `0x003075CB`-`0x003075F9` |

</details>

Readers: the HP write `0x00300530` (bit `0x100`, `0x0030071A`), `0x0031ADB0` (bits `0x100` and `0x800`; the
first entry's low byte against 0, 2-5 and 7, `0x0031B0F1`-`0x0031B105`, `0x0031B30B`-`0x0031B32B`; low byte 10
of an indexed entry, `0x0031B44F`), `0x00322760` (low byte 8), `0x003176E0` (low byte), and the combo
continuation `0x00308610`/`0x0030C010` (bit `0x400`); bit `0x400` is
cleared at `0x002FFA14`, `0x0030019B`, `0x00300EAD`, `0x003011E0` and `0x0030AFF8`.

Before it resolves a target, the applier turns the entry's low byte back into an outcome with
`0x002FEE20`, the inverse of `0x0030DAE0`, and passes it in the result's byte `+0x04` to `0x00385F60`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307552`-`0x00307577` |

</details>

| Entry code | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | other |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Outcome (`0x002FEE20`) | `0` | `5` | `1` | `3` | `2` | `4` | `6` | `7` | `8` | `10` | `11` | `9` |

`0x0030DAE0` is the forward map, through the table `0x0030DB40`: outcomes 0 to 8 give codes 0, 2, 4, 3, 5, 1, 6, 7 and 8,
outcome 9 gives 11, 10 gives 9 and 11 gives 10, and any outcome above 11 gives 11¹.
Code 11 is one of the codes above 10, for which the applier's dispatch below calls nothing.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030DAE0`-`0x0030DAF9`, `0x0030DB3A` |

</details>

The applier has one caller, the per-target step `0x003191B0(unit, entry, again)` (471 bytes). The actor timeline handler
`0x00319F50`¹ and the action timeline handler `0x00325260`² call it as
`0x003191B0(unit, unit + 0x780 + 0x10 * i, 0)` for an entry `i` of the unit's target list. It returns at once when the
entry's actor `+0x00` is null or `0x00263E30(actor)` gives no unit, the target unit below³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A022` |
| ² | `0x00325515` |
| ³ | `0x003191E0`-`0x003191F7` |

</details>

Two steps run only with `again` 0; a bounce pass (`again` 1) jumps past both to the code byte¹.
First it sets the target unit's dword `+0xDD4 + 4 * slot`, for a user slot byte `+0xEA9` up to 31, to the tick counter
`[0x0208D45C]` less `10 * (int)([0x01DFE0B8] * -30.0)`, 300 ticks ahead as shipped ([Enemy
AI](../Enemy-AI-And-Gambits/enemy-ai.md))².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003191FD`-`0x00319200` |
| ² | `0x00319206`-`0x0031923F` |

</details>

Second, while the user's dword `+0x700` has bit `0x2` clear, it pays the action once: with the action id the user's
word `+0x714`, when `0x0030B9B0(target unit, unit)` answers 0 and `0x002FFA60(action, target unit)` answers non-zero, it
calls `0x00305640(unit, row, 1)` and sets that bit¹. The row is the action's row of `[0x02EBF138]`
from the second of two `0x0020E600` calls, 0 when the table or the first answer is null. It leaves the bit clear when a
gate refuses, so a later entry of the same action can pay.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00319241`-`0x003192BC` |

</details>

It then reads the entry's code byte `+0x08`. Any code but 8 calls `0x002FFA60(action, target unit)` and, when that
answers non-zero, the applier `0x00307300(action, unit, target unit, entry, 0, again)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00319333`-`0x00319362` |

</details>

For code 8, a bounced entry, it looks for the target unit's actor, its qword `+0x10`, among the actors of the unit's
target list (`+0x780`, count `+0x77C`, `0x10` bytes each). When it is at index `k` and the bounce slot
`+0x988 + 0x10 * k` holds an actor, it starts over with that slot as the entry and `again` 1, so the mark and the
payment are skipped for it¹. It returns when no entry matches or that slot is empty.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003192C3`-`0x0031932E` |

</details>

The applier as a whole, `0x00307300(action, user, target, entry, first, flag)`, works in this order, which is
the order of its code. It first looks up the action's row: `row` is
`0x0020E600([t+0x0C]) + [t+0x08] × action` with `t` the table pointer `[0x02EBF138]` and `[t+0x08]` a word, or
null when `t` or that answer is null¹. The applier calls `0x0020E600([t+0x0C])` twice
in each lookup, once for the null test and once for the sum, and repeats the lookup inline before each later
test of the row: six lookups, twelve calls.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030732D`-`0x00307385` |

</details>

With `first` = 1 it then returns at once when `0x002FFCF0(action, user)` answers non-zero, and otherwise calls
`0x0030EF20(user, row)` and `0x00305640(user, row, 0)`¹; its one caller, the per-target step above,
passes `first` 0², so this step does not run as shipped. It clears a `0x148`-byte result on its stack
through `0x00861EC0(result, 0, 0x148)`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307388`-`0x003073B9` |
| ² | `0x00319354` |
| ³ | `0x003073C5`-`0x003073D2` |

</details>

When the user's count `+0x6B6` is not 0 it handles the stats-index list as told above: each byte that
`0x00320A40(byte)` resolves to a record is resolved with outcome 9, `0x00385F60(action, user stats, record,
result)`, and applied with `0x003112F0(result, user stats, record, action, 0)`, and a byte for which
it gives null is passed over with neither call¹. It then stores 0 in the count and
returns².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003073FF` |
| ² | `0x003073D7`-`0x00307452` |

</details>

Otherwise it returns unless there is a target whose first byte has bit `0x10`¹. For
an action up to `0x115` whose row byte `+0x2C` has bit `0x40` or `0x80` it clears bit `1 << [user+0xEA9]` of
the target's dword `+0xEA0`². The result's dword `+0x00` takes bit `0x2` when `flag` is
not 0, bit `0x1` when bit `0x800000000` of the user's first qword is set and bit `0x4` when its bit
`0x400000` is set³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307457`-`0x00307463` |
| ² | `0x00307469`-`0x00307511` |
| ³ | `0x00307517`-`0x0030754E` |

</details>

Each test of a row byte looks the row up again through `0x0020E600([t+0x0C])`, with the same null tests as the first
lookup: here¹, and in the two steps of entry code 0 below².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307481`-`0x003074FB` |
| ² | `0x003077BF`-`0x0030783D`, `0x003078B7`-`0x003078EC` |

</details>

It then turns the entry's code back into an outcome with `0x002FEE20(entry byte +0x08)`, stores it in the
result's byte `+0x04` and resolves with `0x00385F60(action, user stats, target stats, result)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307552`-`0x00307577` |

</details>

After that call it asks `0x0017D360()`. When that answers non-zero, the user has a stats record whose
byte `+0x05` is 0, and the target has no stats record or one whose byte `+0x05` is not 0, the result's dword
`+0x24` becomes `0xFFFE7961`, -99,999¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030757C`-`0x003075AD` |

</details>

Then the entry's low byte `+0x08` is set
from `0x0030DAE0(the result's byte +0x04)` and its bits `0x100`, `0x400`, `0x200` and `0x800` from bits `0x8`,
`0x2`, `0x4` and `0x1` of the result's dword `+0x18`, as told under Entry flags,
and `0x003216E0(user, target, row)` runs¹, before a dispatch on the entry code
through the table `0x00307BB4`²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003075B5`-`0x0030760A` |
| ² | `0x0030760F`-`0x0030762E` |

</details>

| Entry code | The applier's step |
|---|---|
| 0 | `0x0030AD90(user)`. Only when it answers other than -1 (`0x0030763A`-`0x0030763D`): `0x002EACD0([user+0x08], 1, target + 8, that answer)` and, for action `0x96`, the user's byte `+0x6B8` goes up by 1 and, when it is then above 1, `0x0028E920([user+0x08], the byte)` runs. In either case `0x00312170(user, target, action)` follows (`0x00307630`-`0x00307685`) |
| 1 | `0x00328480(target, 4)` (`0x003076B2`-`0x003076BA`) |
| 2, 4 | `0x00328480(target, 0)`, then `0x002EACD0([user+0x08], 1, target + 8, c)` with `c` = `0x82` when the word `+0x50` of the target's stats record is `0x1000`, else `0x80` (`0x003076C4`-`0x003076E9`, `0x0030773F`-`0x00307749`) |
| 3, 5 | `0x00328480(target, 0)`, then the same `0x002EACD0` call with `0x81` (`0x003076EF`-`0x003076F9`) |
| 6 | `0x0030B9B0(target, user)`; when it answers 0, `0x00328480(target, 1)` (`0x0030768F`-`0x003076A8`) |
| 7, 9 | `0x00329F70(target, 4, v)` with `v` = `0x79` when bit `0x2000` of `[row+0x0C]` is clear, else `0x78`, `0x00328480(target, 5)`, then the same `0x002EACD0` call with `0x82` (`0x0030770D`-`0x00307739`) |
| 8, and any code above 10 | no call (`0x00307617`, `0x0030774E`) |
| 10 | `0x00328480(target, 0)` (`0x00307701`-`0x00307706`) |

An entry with bit `0x800` then gets `0x00328480(target, 2)` and, for entry code 0 when `0x0030AD90` did not answer
-1, `0x002EACD0([user+0x08], 1, target + 8, 0x86)`¹. An entry with bit `0x200` stores the
user's dword `+0x08` at the target's `+0x28` unless bit `0x400000` of the user's flag dword is set².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307751`-`0x0030777D` |
| ² | `0x00307782`-`0x00307798` |

</details>

Entry code 0 has two more steps before the result is applied¹. For an action up to
`0x115` whose row byte `+0x2C` has bit `0x40` or `0x80`, it calls `0x00311F70(user, target, 0)` after two
tests, in this order. A target with a stats record must have any of bits `0x80000003` in that record's
dwords `+0x3C` and `+0x64`, and `0x00377C20()` must then answer 0²; a target without a
stats record skips that test. Then `0x002E9600(the target's actor)` must answer 0³; it is not called when the first test fails.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030779B`-`0x00307A97` |
| ² | `0x0030784C`-`0x00307870` |
| ³ | `0x00307876`-`0x00307881` |

</details>

For an action from `0x116` to `0x21E` whose row byte `+0x2C` has bit `0x40`, on a target whose stats byte
`+0x05` is 1, it calls `0x002E8060(the target's actor)` and `0x003299B0(target, 0x200D, 0)`, clears bit `0x10`
of the dword at `[target+0x6A0]`, calls `0x0026DC60(actor, 0x003125E0(target) == 0)` and sets bit `0x1000000` of
the target's first qword¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0030789A`-`0x0030790C`, `0x00307A5C`-`0x00307A97` |

</details>

Action `0x1C7` first moves that target onto the user¹. It reads the user's position
with `0x00265020(user's actor, &x, &y, &z)` and heading with `0x00265200(user's actor)` ([facing and
steering](../Movement-And-Pathfinding/facing-and-steering.md#three-angles-and-two-wraps)), and the target's position
with `0x00265020(target's actor, &x, &y, &z)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307912`-`0x00307A54` |

</details>

When the positions differ and
`0x00263F40(target's actor)` gives an object, it passes the user's position to `0x0026B0C0(object, x, y, z)` on that
object. It stores 16 bytes, the user's three position floats and the dword after them on its stack, at the
target's `+0xD0` and `+0xE0`, calls `0x00392170(target's actor)`, and for a target whose stats byte
`+0x05` is 1 stores them at `[target+0x6A0] + 0x50` too¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307992`-`0x003079F4` |

</details>

It then sets bit `0x4000000` of the target's first qword, stores the heading at `+0x15C` and `+0x160`, passes
it to `0x0026A0D0(object, heading)` and `0x0026B620(object, heading)` on the object `0x00263F40(target's actor)`
gives, when there is one, and for the same kind of
target stores it at `[target+0x6A0] + 0x70`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003079FC`-`0x00307A4F` |

</details>

Every path that gets this far applies the result with `0x003112F0(result, user stats, target stats, action, 0)`¹. An entry with bit `0x100` then calls `0x00323350(user, target, the float at result
+0x134, n)`; `n` is 0 when the target has a stats record with none of bits `0x80000003` in `+0x3C` and
`+0x64`, or one for which `0x00377C20()` answers non-zero, and 1 otherwise².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307A9E`-`0x00307ABD` |
| ² | `0x00307AC2`-`0x00307B04` |

</details>

A result whose dword `+0x2C` has bit `0x100` and not bit `0x8` passes what `0x002F91A0(user, target, v,
action)` returns to `0x00300CE0(target stats, that, 0x10)`, and what `0x002F9240(user, target, v, action, k)`
returns to `0x00300CE0(user stats, that, 0x10)`; `v` is the dword value at the result's `+0x24` and `k`
follows the same rule as `n`, with its own call of `0x00377C20()`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00307B09`-`0x00307B8C` |

</details>

### The shape reader

`0x0031A990(row, out)` (154 bytes) describes the same fields as a shape: it
writes 0 to `out+4`; with no radius or with bit `0x1000` of the flag word set, the shape is 5 (with
`out+4` = 1) when bit `0x2` is set and 0 otherwise; otherwise 3 for bit `0x1000000` (radius at `+8`, the angle in
radians at `+0xC`), 4 for bit `0x2000000`, and 1 or 2 for bit `0x200000` clear or set (radius at `+8`)¹. Its one caller is `0x0031AA30`², which is called from `0x00321060`
and `0x00328530` and jumped to from `0x0031AB80`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031A990`-`0x0031AA29` |
| ² | `0x0031AB58` |

</details>

`0x00321060(handle, kind out, reach out)` answers -1 unless bit `0x10` of `0x02089340` is
set and `0x003588B0` and then `0x00263E30` give a unit for the handle¹. Otherwise it calls `0x0031AA30(unit, 0, word +0x714 of the unit, local)`,
copies the local's dword `+0` to the kind pointer and its dword `+4` to the reach
pointer, each when the pointer is not null, and answers what `0x0031AA30` answered².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0032106A`-`0x0032108E`, `0x003210C8` |
| ² | `0x00321090`-`0x003210BB` |

</details>

Its one call site, `0x0027DE82`, passes a null reach pointer¹; on a negative
answer it returns 0 without asking for a line and without closing the unit's lines
(`0x0027DE87`-`0x0027DE89`, to `0x0027DE74`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0027DE78` |

</details>

The list append `0x00316CD0` answers the count after the append, or the count as it
stands when it refuses¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00316CE4`, `0x00316CE7` |

</details>

The lookup `0x00316D70(list, actorWork)` walks the 16-byte entries from `list + 0x08`, as many as the count, the i32 at
`list + 0x04`, and answers, as a 32-bit int, the index of the first whose qword `+0x00` equals `actorWork`, and -1
when none does or the count is 0 or below¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00316D70`-`0x00316D9E` |

</details>

## Layouts

<details>
<summary>Show the memory layouts</summary>

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | flags | bit `0x1` kept by the clear (`0x00316D05`-`0x00316D16`); the rest cleared |
| `+0x01` | `u8` | keyType | the key the candidate picker `0x003087E0` sorts by: 1 takes the arm at `0x003089C3` (`0x00308817`-`0x0030881A`), 2 the arm at `0x00308873` (`0x00308820`-`0x00308823`), and 0 or any other value the plain walk at `0x00308825`; cleared to 0 together with `+0x02` by the 16-bit store at `0x00316D1D` |
| `+0x02` | `u8` | pickRule | the picker's rule, compared with 3 (`0x00308873`-`0x00308879`); cleared by the same 16-bit store |
| `+0x03` | `u8` | pad3 | cleared by the memset of `0x00316D0B` |
| `+0x04` | `i32` | count | entries in use; signed (movsxd at `0x00316CD0` and `0x00316D70`); append refuses at 32 (`0x00316CD4`) |
| `+0x08` | `u8[512]` | entries | 32 ActionTargetEntry records of 16 bytes |

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u64` | actorWork | the unit's `+0x10` object; stored by `0x00316CDC`, compared by `0x00316D83` |
| `+0x08` | `u32` | entryFlags | low byte the outcome code (`0x0030DAE0`), bits `0xF00` result flags; written by the effect applier `0x00307300` |
| `+0x0C` | `u32` | tail | cleared with the whole list by the clear's memset of `0x208` bytes (`0x00316CFF`-`0x00316D0B`); the append (`0x00316CDC`) writes only `+0x00`, and the effect applier `+0x08`; neither the per-target step `0x003191B0` nor the applier reads it: their entry reads are `+0x00` and `+0x08` (`0x003191E0`, `0x003192C3`, `0x003192F0`, `0x0031930C`; `0x00307552`-`0x00307AC2`) |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

The shipped action table (`battle_pack.bin`, read through `0x02EBF138`) marks 26 actions as centred on the user (bit `0x200000`
of the flag word `+0x0C`). The radius is the row's byte `+0x06`. The same rows carry the flag name "area centred on
the user" in [Action list](action-list.md).

| Radius | Actions centred on the user (id) |
|---|---|
| `6` | Piercing Graviga (`443`) |
| `8` | Angelsong (`349`), Magick Ballad (`350`), Warsong (`351`), Vespersong (`352`), Mystery Waltz (`353`), Hero's March (`354`), Time Requiem (`355`), Soul Etude (`356`), Fly, Enkidu! (`463`), Now, Enkidu! (`464`), Eviscerator (`475`), Force of Will (`486`), Azure Vortice (`488`), Crimson Vortice (`489`) |
| `10` | Screech (`342`), Scream (`343`), Wail (`344`), Eerie Soundwave (`345`), Joyous Soundwave (`346`), Rage (`418`), Shockstorm (`457`), Pollen Dance (`478`) |
| `20` | Monarch Sword (`468`) |
| `100` | Inviolable Will (`491`), Ascension (`495`) |

Cones (bit `0x1000000`) and lines (bit `0x2000000`) take the angle or half-width from byte `+0x07`; in [Action list](action-list.md)
they carry the flag names "cone area" and "line area". Monarch Sword and Eviscerator are both centred on the user
and cones.

| Shape | Radius | Angle or width | Actions (id) |
|---|---|---|---|
| cone | `3` | `40` | Cloying Breath (`376`) |
| cone | `3` | `60` | Bad Breath (`377`) |
| cone | `3` | `80` | Putrid Breath (`378`) |
| cone | `3` | `120` | High Jump (`476`) |
| cone | `4` | `45` | Tail Swipe (`404`) |
| cone | `4` | `75` | Stone Gaze (`335`), Phantasmal Gaze (`336`), Flash (`337`) |
| cone | `4` | `180` | Spiral Cut (`394`), Snake Lash (`398`), Flatten (`403`) |
| cone | `6` | `60` | Aqua Bubbles (`357`), Mythril Bubbles (`358`), Breath (`362`), White Breath (`363`), Stone Breath (`364`), Poison Breath (`365`) |
| cone | `6` | `180` | Darkness (`327`), Ice Break (`328`), Water Spout (`329`), Shining Ray (`330`), Tremor (`331`), Tempest (`332`), Sandstorm (`333`), Pyromania (`334`), Blast Wave (`372`), Shock Wave (`373`), Pulsar Wave (`374`), Dark Shock (`375`), Spinkick (`390`), Sonic Turn (`399`), Chain Reaction (`409`), Discharge (`422`), Pollen (`424`), Power Stun (`438`), Power Spin (`442`), Bushfire (`458`), Sporefall (`459`), Sword Dance (`461`), Circle of Judgment (`471`) |
| cone | `8` | `0` | Eviscerator (`475`) |
| cone | `8` | `180` | Screwtail (`406`) |
| cone | `10` | `45` | Gatling Gun (`481`) |
| cone | `10` | `180` | Ultimate Illusion (`466`) |
| cone | `15` | `180` | Ground Shaker (`456`) |
| cone | `18` | `180` | Choco-Comet (`426`) |
| cone | `20` | `0` | Monarch Sword (`468`) |
| cone | `20` | `180` | Tree of Sephira (`492`) |
| cone | `100` | `180` | Gigaflare Sword (`496`) |
| line | `3` | `2` | Gust (`359`) |
| line | `4` | `3` | Innocence (`474`) |
| line | `5` | `2` | Mach Wave (`487`) |
| line | `5` | `3` | Gale (`360`) |
| line | `20` | `10` | Judgment (`411`) |

</details>

## Modding notes

- The area fields are bytes of the action row: `+0x06` radius, `+0x07` cone angle in degrees or line
  half-width; flag word `+0x0C` bits `0x2` (whole party), `0x200000` (centre on user), `0x1000000` (cone), `0x2000000` (line);
  word `+0x36` bits `0x4` (other side from the target) and `0x8` (everyone).
- Shipped `battle_pack.bin`: 247 of 543 action rows have a radius (3, 4, 5, 6, 8, 10, 15, 18, 20 or
  100); 26 rows are centred on the user, 49 are cones (32 of them 180 degrees, two at 0), 5 are lines;
  no row has both cone and line bits, and no row without a radius has bits `0x200000`, `0x1000000` or `0x2000000`.
- Of the 247 area rows, 245 follow the target's side, Self-Destruct has bit `0x4` and Mass-Destruct bit
  `0x8`. Bit `0x2` is set only on 13 rows named Reserve.
- Remora Strike has an angle byte (180) but neither cone nor line bit, so its angle has no effect.
- 18 rows with radius 10 have bit `0x1000`: the 18 Quickenings, ids 208 to 225 (Red Spiral to
  Resplendence): the gatherer spreads them over the radius, while `0x0031A990` reports them
  as shape 0.
- Raising the radius to 100 makes a spell cover the whole battle area, as the eight attack spells ending in -ja do.

## Related

- [The action definition row](action-definition-row.md) - the row these
  bytes and bits belong to.
- [Action range](action-range.md) - how close the user stands before the action runs.
- [Gambits and enmity](../Enemy-AI-And-Gambits/gambits.md) - other uses of
  the relationship class.
- [The thirty-two statuses](../Status-Effects-And-KO/statuses.md) - status bits
  `0x1`, `0x2`, `0x20`, `0x1000000` and `0x80000000`.
- [The field record table](../World-Areas-And-Travel/area-flags-navimapdata.md)
  - the map-info word whose bit `0x8000` `0x00377C20` returns.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 6 calls with 4 other topics</summary>

**Random numbers** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x003087E0`](area-of-effect.md) Ai order: select final target from candidates | calls | [`0x00328370`](../Random-Numbers/random-number-generators.md) (on random number generators) |

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md), [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](../Scripts-And-Script-Commands/party-during-scenes.md) Actor: get world position (on party during scenes) | is called by | [`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003112F0`](../Rewards-EXP-Gil-And-Loot/gil.md) Battle formula: apply target result (on gil) | calls | [`0x002DF220`](../Sound-And-Music/sound-effects.md) (on sound effects)<br>[`0x003A1180`](../Engine-Core/identifier-spaces.md) (on identifier spaces) |

**Steam and achievements** (explained on [item use](../Items-Equipment-Shops-And-Licenses/item-use.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00305640`](area-of-effect.md) Battle action: consume execution resources | calls | [`0x00316440`](../Steam-And-Achievements/achievements.md) (on achievements) |

**Game files and data tables** (explained on [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over) | calls | [`0x001D6AE0`](../World-Areas-And-Travel/zone-changes-and-mapjump.md) (on zone changes and mapjump) |

</details>
