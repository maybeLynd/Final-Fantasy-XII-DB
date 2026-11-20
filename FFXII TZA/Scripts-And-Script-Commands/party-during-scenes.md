[Home](../../README.md) / [Scripts and script commands](README.md) / Party during scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Party during scenes: hiding the party, the summon leader and followers, summon space, capturing a member and the event party modes | system | Scripts and script commands | Event scenes | What a scene does with the party: hiding the party's bodies, the summon leader and its followers, moving the group into summon space and back, capturing a member's body with capturepc and releasing it, and the event party modes. | 0x003415D0, 0x00342250, 0x00341CB0, 0x002ECD50, 0x00352FA0, 0x0034C3D0, 0x00264050, 0x00263750, 0x00262F50, 0x00262F90, 0x002693D0, 0x00266AD0, 0x0035AE10, 0x0034C990, 0x003B6F30, 0x0037D120, 0x00355FE0, 0x00358800, 0x0035AA50, 0x003B6F80, 0x003B6DE0, 0x003B7770, 0x003B8030, 0x003B7A30, 0x003B79D0, 0x02EBCAC0, 0x02EBCC68, 0x0034EB30, 0x01EF2C80, 0x00505240, 0x003B7B00, 0x003B7D80, 0x003B7F40, 0x003B8140, 0x003B8170, 0x003CC2F0, 0x003B7440, 0x003B7E20, 0x003B7BB0, 0x003B7C60, 0x00359B80, 0x00269530 |

## What the player sees

When a scene starts the party's bodies vanish, and a scene or a summon can take a party member's body over: the
character turns, plays a short motion, and control returns. The same "take over the body" step happens on a small
scale every time the player talks to a townsperson or opens a door.

## How it works

### Hiding the party

`hideparty` (`0x0147`, `0x003415D0`) and `showparty` (`0x0148`, `0x00342250`) call `0x002ECD50(actor,
0 or 1)` for party slots 0 to 3 through `0x00263750`. `0x002ECD50` acts only on a class-3 actor that is
not a captured member (bind state `+0x18` is not 1, `0x002ECD50`-`0x002ECD54`): it writes bit `0x1` of
byte `+0x10` of the presentation record (`+0xC0`) and refreshes visibility through `0x002E8FD0`. It
hides the body and leaves the actor and its battle unit in place.

`hideparty_without_uc` (`0x0498`, `0x00341CB0`) skips the controlled character: it resolves the
party-focus handle¹ and, for each slot 0 to 3 whose `0x00263750` actor is
non-null and is not that actor², calls `0x002ECD50(actor, 0)` through its
thunk `0x0026DC40`. When the handle resolves to null, every non-null slot actor is hidden.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003590D0`, `0x003588B0` |
| ² | `0x00341CDA`, `0x00341CDC` |

</details>

`disposepartywithoutcontrol` (`0x0202`, `0x0034C990` → `0x003B6F30`) clears the party-control dword
`0x02B40534`, empties the follower list¹, narrows the controlled set to one actor², the actor of the party slot that holds the summoner's row `+0x5AD5` ([party control
modes](../Engine-Core/party-control-modes.md), `0x003B6D69`-`0x003B6D82`), turns its [animation-driven
movement](../Movement-And-Pathfinding/animation-driven-movement.md) off³ and
sets its `+9` bit `0x4`⁴, and snapshots each controlled actor's pose⁵.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6DE0` |
| ² | `0x003B6D60` |
| ³ | `0x0026B500`, `0x003B6D9B` |
| ⁴ | `0x003B6DA0` |
| ⁵ | `0x003B7510` |

</details>

`capturepartyforsummon`
(`0x0232`) does the same and binds the set to manager 3's entries¹: for entry i of the
second list of the script image's `+0x68` table ([EBP script image](../EBP-Script-Files/ebp-script-image.md))
with a non-negative ordinal, it clears that actor's `+9` bit `0x1`² and has it capture
controlled actor i³. `releasepartyforsummon` (`0x0233`) releases them
(`0x003B7AB0`, which does not read the manager slot 3 its handler passes).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B72F0` |
| ² | `0x003B736E` |
| ³ | `0x00262F50`, `0x003B7375` |

</details>

`hide_freetarget_group(g)` (`0x04B8`, `0x003569E0`) and `show_freetarget_group(g)` (`0x04B9`,
`0x00356D00`) call `0x0035AA50(0, g, 0 or 1)`. It walks manager 0's ordinal window (first ordinal at
`+0x1DE`, count at `+0x1D6`), skips party members (`0x002647B0`: byte `+0x12` below 4) and passes
every other actor to `0x002ECD50`, all of them for a negative `g`, otherwise only those whose group
`0x00263BE0` returns equals `g`. The group comes from the class nibble `+0x0E`: 0 gives 1, 1, 2 and 7
give 0, 3 gives 2, any other value 1.

`0x0035AA50` takes each actor from `0x00358940` without a null test and reaches `0x002ECD50` through
`0x0026DC40`. `0x00263BE0` returns 1 for a null actor and `0x002647B0` reads byte `+0x12` of it, so a null
entry faults at `0x002647B0` for a negative `g`¹ or a `g` of 1² and is skipped
for any other `g`³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035AAE0` |
| ² | `0x0035AAAD` |
| ³ | `0x0035AAA8` |

</details>

### The summon leader and followers

`setupsummonforevent(n)` (`0x0193`, `0x00346FA0`) names a leader: the actor at ordinal `n` of the current manager¹, or for a negative `n` the controlled character (`0x003590D0`, `0x003588B0`; the pop and the
choice, `0x00346FA9`-`0x00346FCC`). With a leader it ends with `0x003B6F80(leader)` as a tail jump, and with none it does
nothing².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002640C0`, `0x00358940` |
| ² | `0x00346FD4`-`0x00346FDE` |

</details>

`0x003B6F80(leader)` walks managers 0, 1 and 2 (`0x003B7036` loops while the manager index is at most 2) whose byte
`+0x10` has bit `0x1` set and collects, up to 31, the handles¹ of every actor with byte `+9` bit `0x10`
set other than the leader; it clears `+9` bits `0x4` and `0x10` on every actor it visits and sets its requested speed
to 0 with mode 2 (`0x0026D6D0` → `0x0026D6F0`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003589B0` |

</details>

It reads `+9` of each ordinal's `0x00358940` actor without a null test¹, so a null entry
faults there. The leader's own handle also comes from `0x003589B0`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6FFD` |
| ² | `0x003B6FB4` |

</details>

It then hands the list to `0x003B6DE0(leader handle, count, handles)`. That keeps the requested count (at
most 32, `0x003B6E12`; a negative count becomes 0, `0x003B6E05`-`0x003B6E07`) at `0x02EBCC60` and the
handles at `0x02EBCBE0`, and resolves each handle¹. On each actor that resolves it clears
`+9` bit `0x8` and sets bit `0x4`, so a stale mark cannot drop an actor, and stores it in the slot;
a handle that resolves to null leaves that slot's previous pointer in place.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003588B0` |

</details>

A second pass keeps each actor once, marking it with `+9` bit `0x8`, and writes the unique ones to the
front of the followers at `0x02EBCAC0` with their count at `0x02EBCBC0`; it reads every slot without a
null check¹, so a slot that still holds null faults there. The leader's handle goes to
`0x02EBCC70` and its actor to `0x02EBCC68`. `0x003B6F30` calls it with an empty list, which is the
follower-list clear above.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B6E8A` |

</details>

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `hidenobattletarget` | `0x0196` | `0x00347D80` → `0x003B7770` | first resolves the first follower handle (`0x003B7794`) and handle 0 (`0x003B779B`) and discards both results; then for every actor of the managers among 0 to 2 with `+0x10` bit `0x1` set: in each actor's presentation record (`[actor + 0xC0]`, which `0x002E97B0` returns), the leader gets bit `0x2` of byte `+0x10`; any other actor gets that bit from its own `+9` bit `0x4`, or from bit `0x1` of `+0x14F` of the same record; each actor with a presentation record is refreshed (`0x002E8FD0`, which tests bits `0x1`, `0x2` and `0x8` of that byte); the actor from `0x00358940` is not null-tested, so a null entry faults reading `+9` at `0x003B77FC`, unless the leader is null too, in which case it takes the leader path and `0x002E97B0` returns null, so it is skipped (`0x003B77F4`) |
| `showsummontarget`, `hidesummontarget` | `0x01D8`, `0x01D9` | `0x00342000`, `0x00342320` → `0x003B70B0(1)`, `0x003B70B0(0)` | for each follower, or its capturer (`0x00263F40`), with a presentation record (`0x002E97B0`): sets or clears bit `0x2` of byte `+0x10`, then refreshes visibility (`0x002E8FD0`) |
| `setrotangzxsummonspace(a)` | `0x0199` | `0x00348660` → `0x003B8030` | pops a float and sets it as the heading (`0x0026B620`) of each follower, or of its capturer when the follower is captured (`0x00263F40`) |
| `releaseallforsummon` | `0x019B` | `0x00348DA0` → `0x003B7A30` | runs `0x002693D0(…, 1)` on the leader and on every follower, or on its capturer when it is captured (`0x00263F40`) |
| `summonplaymotionall` | `0x02AB` | `0x0034EB30` (a `jmp`) → `0x003B79D0` | calls `0x0017F5B0(1)` first when `0x022BE970` is non-zero, then `0x002EB030(follower, 0x1049)` for each follower |

`0x0034EB30` is reached through its pointer at `0x01EF2C80`, the result slot of record `0x2AB` in the
family 0 table.

### Moving the group into summon space and back

Each actor keeps a pose snapshot at `+0xED0` of the record its `+0x30` points to (`0x00359B80`, null
when there is no record). `duplicatebattletarget` (`0x0194`, `0x003475D0` → `0x003B7440`) fills it for the
leader¹ and for every non-null slot of the requested count: the position², the three floats at body `+0x20`³, the heading⁴, the movement
heading (`0x00263CC0`, stored at `+0x34` twice, `0x003B74CB`, `0x003B74E2`) and the presentation byte `+0x13`
(`0x002E9BE0`, -1 when the actor's `+0xC0` is null, `0x002E9BF6`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003B73B0` |
| ² | `0x00265020` |
| ³ | `0x00265240` |
| ⁴ | `0x00265200` |

</details>

What each read gives depends on the actor's class, byte `+3` >> 5. For class 3 the position is body
`+0x00`-`+0x08`, the three floats are body `+0x20`-`+0x28`, the heading is body `+0xA8` and the movement
heading body `+0xA4`. For class 1 the position is the same, both headings are body `+0x38`, and snapshot
`+0x10`-`+0x18` keeps what it held. Any other class gets a zero position and headings of 0.0, and
`+0x10`-`+0x18` again keeps what it held¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00265020`-`0x0026505C`, `0x00265240`-`0x00265268`, `0x00265200`-`0x00265233`, `0x00263CC0`-`0x00263CF3` |

</details>

A slot or leader whose `0x00359B80` record is null is skipped (`0x003B748C`; `0x003B73B0` returns for a
null leader at `0x003B73B3` and for a null record at `0x003B73CD`).

`setpossummonspace` (`0x0191`, `0x003482E0` → `0x003B7E20`) clears the party-control dword `0x02B40534`,
calls `0x0025A5F0(1)` and `0x0036D840(0)`, and takes as origin the position of the first follower
handle¹ when the requested count is above 0 and that handle resolves to an actor², otherwise `(0, 0, 0)`. `0x003B7F40(actor, origin)` then places each follower and the
leader, or their capturers³; it returns at once for a null actor⁴, which
skips a null leader.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x02EBCBE0` |
| ² | `0x003B7E77` |
| ³ | `0x00263F40` |
| ⁴ | `0x003B7F43` |

</details>

`0x003B7F40` sets the position¹ to the actor's own x and z minus the origin's, with a
height of 0, or of `0x002ECE50(actor, 0x9000505)` when bit `0x1` of `+0x151` in the actor's `+0xC0`
record is set². It also computes the old height minus `0x00264670(actor)` but never
uses it, so the old height is discarded rather than offset.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026B0C0` |
| ² | `0x002644C0` |

</details>

It then sets presentation `+0x13` to 1¹, sets bit `0x20` of `+0x151` in the `+0xC0` record² and re-applies the render scale³. Last, `0x003B7E20` runs the same motion
step as `summonplaymotionall`: `0x0017F5B0(1)` when `0x022BE970` is non-zero, then
`0x002EB030(follower, 0x1049)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EC680` |
| ² | `0x0026ACE0` |
| ³ | `0x002E4A40` |

</details>

`0x003B7B00(actor)` restores one snapshot, the actor's own (`0x00359B80(actor)`), onto the actor's
capturer, or the actor itself¹: movement heading², heading³,
the movement heading again⁴, position⁵, the body `+0x20` floats⁶, bit `0x20` of `+0x151` cleared⁷, presentation `+0x13` from the snapshot⁸ and the render scale⁹. It returns at once for a null actor¹⁰
or a null snapshot record¹¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263F40` |
| ² | `0x0026A0D0` |
| ³ | `0x0026B620` |
| ⁴ | `0x003B7B50` |
| ⁵ | `0x0026B0C0` |
| ⁶ | `0x0026B720` |
| ⁷ | `0x0026ACE0` |
| ⁸ | `0x002EC680` |
| ⁹ | `0x002E4A40` |
| ¹⁰ | `0x003B7B03` |
| ¹¹ | `0x003B7B2C` |

</details>

`0x002E4A40(actor)`, the render scale, acts only while `0x00377DB0()` is non-zero and the actor's presentation record
(`+0xC0`) is non-null with a first dword other than -1¹. The scale is 1.0 on all three axes² when bit `0x20` of the presentation record's byte `+0x151` is set; otherwise it is the floats `+0x50`,
`+0x54` and `+0x58` of the presentation record's `+0x138` record (`0x00265970` returns that record plus `0x30`), read
again after `0x002ED6A0(actor, that record)` when bit `0x10` is clear³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4A57`-`0x002E4A8B` |
| ² | `0x01CEBBA8` |
| ³ | `0x002E4AAE`-`0x002E4B06` |

</details>

The first read has no null test, so a null `+0x138` record faults at `0x002E4AD9`. Each of the presentation record's
four handles at `+0x00`, `+0x30`, `+0x60` and `+0x90` whose first dword is not -1 is passed with the scale to
`0x002EDD70(its first word, x, y, z)`¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002E4B0C`-`0x002E4B90` |

</details>

`0x002EDD70` stores x, y and z at `+0x380`-`+0x388` of the render record the word names and sets bit `0x8` of its
`+0x290` only when the word is not -1, the record is non-null and its `+0x284` is non-zero¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EDD70`-`0x002EDDAA` |

</details>

`0x002E9560(actor)`, the render value, returns 0.0 for a null actor, a null presentation record or a first dword of -1,
30.0¹ when the record's first word is -1, or when, as a signed index, it names a render record
`[0x022C6F28] + word × 0x740` whose address is null or whose `+0x284` is 0, and otherwise the value of `0x00423280` for
that record².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008F8D80` |
| ² | `0x002E9563`-`0x002E95AA` |

</details>

`summongethertarget(d)` (`0x0370`, `0x00340DA0` → `0x003B8140`) pops a float. It first has `0x003B7D80`
put back the body `+0x20` floats from the snapshot of every non-null slot of the requested count,
onto that slot's capturer or the slot actor itself¹, skipping a slot whose
snapshot record is null², then calls `0x00505240(count, 0x02EBCAC0, d)` over all the
followers. `summongethertarget_one(d)`
(`0x0572`, `0x003410A0` → `0x003B8170`) does the same with a count of 1, the first follower only.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00263F40`, `0x003B7DB1` |
| ² | `0x003B7DC4` |

</details>

`0x00505240` works from the origin `(0, 0, 0)` on each actor, or its capturer. For an actor at the
origin its reach point is the larger of the two floats `0x00265090` reads, its height (`0x00263940`,
body `+0xC0` × `+0x24`) and 0.

For any other actor `0x003CC130` measures its heading around the
origin, its elevation and its distance, and `0x003CC2F0(origin, 0, elevation, distance)` rebuilds a
point from them (at `0x00505393` its first angle argument is 0). The heading is dropped, so the point
keeps the actor's distance and elevation but not its direction; the larger float and the height
are then added to its x and y.

The reach is that point's distance from the origin¹. When the largest reach exceeds
`d`, every actor's position and its body `+0x20` floats are multiplied by `s = d / reach`², which
applies when that largest reach is non-zero and `s < 1.0`³: each value becomes `v * s`⁴, which draws the group in
around the origin.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC130` |
| ² | `0x00505431` |
| ³ | `0x00505415`-`0x00505439` |
| ⁴ | `0x00505456`-`0x00505466`, `0x0050549C`-`0x005054A4`; `0x0026B0C0`, `0x00265240`, `0x0026B720` |

</details>

`0x003CC2F0(origin, a, b, distance, out)` is a shared helper, also used by the camera code: it
builds a rotation from two angles¹, rotates `(0, 0, distance)` by it and adds the
origin. Its body has one path, with no branch.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC480` |

</details>

It calls `0x003CC480(b, a, 0, matrix)`¹, which fills a 4×4 matrix on the stack from
`sinf` and `cosf` of the three angles. The matrix's translation row is `(0, 0, 0, 1)` (`0x003CC505`
to `0x003CC51A`) and its third row is `(sin a × cos b, −sin b, cos a × cos b, 0)`², so the third angle, given 0, does not reach the result.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC32D` |
| ² | `0x003CC53B`, `0x003CC5A1`, `0x003CC5BC`, `0x003CC534` |

</details>

The body sets the vector `(0, 0, distance, 1.0)` on the stack (`0x003CC344` to `0x003CC355`) and
`0x00202B70` multiplies it by the matrix in place, the row vector `v = v × M`¹, so its
first three floats are `distance` times that third row. It then writes three floats to `out`: x is origin x +
distance × sin a × cos b², y is origin y − distance × sin b³ and z is origin z +
distance × cos a × cos b⁴; `out + 0xC` is not written. With `a` given 0 at `0x00505393`,
the point is origin + `(0, −distance × sin b, distance × cos b)`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC35E`; `0x00217060` |
| ² | `0x003CC373` |
| ³ | `0x003CC382` |
| ⁴ | `0x003CC38C` |

</details>

Neither pointer is checked: an `origin` below `0x10000` (null included) faults at its first read¹, and such an `out` faults at its first write². The body ends with the
stack-cookie check `0x00808C40`³, which on a mismatch jumps to the failure report at
`0x00809654`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003CC369` |
| ² | `0x003CC373` |
| ³ | `0x003CC399` |

</details>

| Verb | Id | Handler | Effect |
|---|---|---|---|
| `resumeposbattletarget` | `0x0195` | `0x00347850` → `0x003B7BB0` | raises `0x02B40534`, restores the leader and every slot of the requested count with `0x003B7B00`, calls `0x002E7A10(follower, 0)` for each follower for which `0x002E7600` is non-zero, then `0x0025A5F0(0)` and `0x0036D840(1)` |
| `resumepartyinfo_spattack` | `0x02A4` | `0x0034D330` → `0x003B7C60`, then `0x003B7180` | the same `0x002E7A10` step for the followers, raises `0x02B40534`, and for each actor of the party set at `0x02EBCA80` calls `0x0026B500(actor, 1)` and `0x003B7B00`; then `0x0025A5F0(0)` and `0x0036D840(1)` |

### Capturing a party member

`capturepc(slot)` (`0x0057`, `0x00352FA0`) is how a script on another actor takes a party member's
body. A slot outside 0 to 3 (`0x002647C0` is an unsigned test for below 4) is replaced by byte
`+0x12` of the controlled character's record (`0x00264050(0, −1)` resolves the party-focus handle),
so `capturepc(−1)` means "the character the player controls"; a slot at or above 0 first calls
the town test `0x00377C20` and drops the result. The actor is `0x00263750(slot)`; `0x00262F50(owner, pc)` binds
them and on success the verb returns 1 and cancels the member's battle action¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035AE10` |

</details>

The verb writes its result through `0x0026B4E0`:

- When the party-focus handle (`0x022C7FE0`, read by `0x003590D0`) is 0 or resolves to null
 ¹, the slot keeps its out-of-range value. `0x00264050` points `0x02099D70` at
  the slot array `0x02098E10` for the lookup and restores it².
- `0x00263750` returns null for any slot outside 0 to 3 (an unsigned compare, so a `+0x12` byte of
  `0xFF` also gives null); the verb then returns 0 without a bind³.
- A refused bind returns 0⁴; the 1 and the cancel follow only a successful bind
  (`0x0035300C`, then the tail jump to `0x0035AE10(pc, 1)` at `0x00353028`).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00264092`, `0x00352FE0` |
| ² | `0x0026406B`, `0x0026409B`, `0x002640AA` |
| ³ | `0x00352FF3`, `0x0035302D` |
| ⁴ | `0x00353005` |

</details>

`0x00262F90(owner, pc)` binds only when the member is non-null¹, the member's manager is
active, neither record is already bound (`+0x18` is 0) and the two differ; otherwise it returns 0.
It reads the owner's `+0x18` without a null test², so a null owner faults there. On a
bind the member gets `+0x18` = 1 with the owner's manager at `+0x19` and id at `+0x1A`, the owner
gets `+0x18` = 2 with the member's; `0x002E4A40(owner)` re-applies the render scale; the owner copies
the member's body pointers (`+0xC0` and `+0xB8`); `0x002681E0` refreshes both; it returns 1.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00262FA0` |
| ² | `0x00262FD0` |

</details>

`0x002681E0(actor)` acts only when the actor's presentation record (`+0xC0`) is non-null and the actor is class 3¹; it reads `+0xC0` without testing the actor², so a null actor faults there.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002681F3`-`0x00268201` |
| ² | `0x002681E9` |

</details>

It writes a value to word `+0x80` of the presentation record's `+0x138` record and to the presentation record's byte
`+0x153`, only when that `+0x138` record is set¹. The value comes from the presentation
record's byte `+0x152`: 3 for 2, 5 for 3 and 2 for any other non-zero value².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00268294`-`0x002682B5` |
| ² | `0x00268215`-`0x00268226` |

</details>

For a byte `+0x152` of 0 the value is 1 when the handle¹ of the actor, or of the member it holds when it
is a capturer and that member resolves², is not the party-focus handle `0x003590D0` returns³. When it is, the value is 1 when bit `0x10` of the actor's byte `+0xC` is set and
`0x00265680()` is non-zero and 0 otherwise, then 1 when `0x002672B0()` is 0, and then 5 when `0x0037C860()` is non-zero⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003589B0` |
| ² | `0x00263F10` |
| ³ | `0x0026823B`-`0x00268254`, `0x0026828A` |
| ⁴ | `0x00268256`-`0x00268283` |

</details>

`0x002ECCF0(owner, v)` then clears presentation `+0x11` bit `0x80` and sets it again from bit `0x1`
of `v`¹, so `(owner, 1)` sets it: `0x00262F50` calls it only after a
bind that returned 1², and `0x002ECCF0` writes only when the owner and its `+0xC0` record
are non-null and the record's first dword is not -1³. `0x00262F50` returns the
bind's result.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002ECD06`-`0x002ECD0D` |
| ² | `0x00262F66` |
| ³ | `0x002ECCF3`-`0x002ECD04` |

</details>

`capturepc_not_cancelbattlecommand` (`0x0582`) and the by-id form `capturepcbyentryid`
(`0x02A2`, `0x0034C3D0`, which resolves a handle through `0x003588B0`) skip or keep the cancel.
`0x0034C3D0` pops the handle¹, returns at once when it resolves to null² and
after a successful `0x00262F50` bind cancels the member's battle action (`0x0035AE10(pc, 1)`,
`0x0034C40B`); it calls neither the town test nor `0x0026B4E0`, so it writes no verb result.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00267E10` |
| ² | `0x0034C3F2` |

</details>

`captureactor` (`0x0366`, `0x00354E10`) captures by name. It reads the issuer's own entry name
(`0x00263A30(manager, ordinal)`: payload plus its `+0x4C` dword plus the first int of the entry's
`+0x40` record,
`"NOACTOR"` when there is no entry) and has `0x00358800(0, name)` search manager 0's ordinal window for
an entry with the same name (a byte-for-byte compare, `0x00358850`-`0x00358861`), returning the first
match's actor from the table at manager `+8`. It returns null when no entry matches¹,
or when that table is null or the ordinal is not below its count².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035886D` |
| ² | `0x0035888A`-`0x0035889B` |

</details>

When one is found and it is not the issuer, `0x00262F50(issuer, found)` binds them, so a scene's
actor takes over the zone actor of the same name. The bind is also gated on `0x0053DD10(name)`, which
is `mov eax, 1; ret` and always passes. `captureactor_367(name)` (`0x0367`, `0x00355570`) takes the name as a
string operand resolved through `0x002650B0`.

`releasepc` (`0x0058`, a jump into `0x002693D0(owner, 1)`; `releasepc_404` passes a popped flag)
undoes it. `0x002693D0(record, flag)` acts on the record's bind state `+0x18`¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002693DF`-`0x002693EF` |

</details>

- For a capturer (2) whose partner's manager is active (`+0x10` bit `0x1`, `0x0026940F`), `0x002693D0`
  resolves the member (`0x00358940`, not null-tested, so a null member faults in `0x0026AE90` at
  `0x0026AE96`) and sets its steering mode to 0¹.
- For a class-3 member it then clears its steering byte, `+0x28` of `[[member + 0xB8] + 0xF0]`
 ², runs `0x002EBE50(member, 0, 0)` and `0x002E8EE0(member)` when that request's `+0x65` is
  non-zero³, and hands the old byte to `0x002E6300`⁴.
- It re-applies the owner's render value⁵, rebuilds the member's four body
  pointers with `0x00266AD0` from its sequence (`+0x03` bits `0x1F`) rather than restoring a saved
  copy, resets its locomotion (steering and movement modes 0, `0x0026AE90`, `0x0026C120`), refreshes the
  owner's lane index⁶, and with the flag runs `0x002EB430` (the idle motion) on the owner
 ⁷.
- It re-applies the owner's render scale⁸, refreshes the member⁹ and
  releases the member by calling itself on it¹⁰, which takes the captured path below;
  then the owner gets the same reset, so both records get `+0x18` = `0xFFFF0000` and a refresh.
- For a captured record (1), or a capturer whose partner's manager is inactive, `0x00266AD0` rebuilds
  the record's own four body pointers, `+0x18` becomes `0xFFFF0000`, `0x002681E0` refreshes it and
  the render value is re-applied¹¹. Called on a captured member directly,
  this leaves its capturer at `+0x18` = 2.
- Any other `+0x18` value returns at once¹².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026AE90`, `0x0026942B` |
| ² | `0x00269453` |
| ³ | `0x00269462` |
| ⁴ | `0x00269489` |
| ⁵ | `0x002E9560`, `0x002E4F40` |
| ⁶ | `0x002EAC90` |
| ⁷ | `0x002694D1` |
| ⁸ | `0x002E4A40` |
| ⁹ | `0x002681E0` |
| ¹⁰ | `0x002694EB` |
| ¹¹ | `0x002694F5`-`0x0026951A` |
| ¹² | `0x002693EF` |

</details>

`releasepc_battlemember` (`0x057D`, a jump into `0x00269530`) releases every roster member a scene
actor holds: for each of the four roster actors whose `+0x18` is 1 it resolves the owner from
`+0x19` and `+0x1A`¹ and, when that is another record, runs `0x002693D0(owner, 1)`. It
reads `+0x18` of each roster pointer without testing it for null².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003587C0` |
| ² | `0x00269556` |

</details>

### Event party modes

`seteventpartymode(v)` (`0x050F`, `0x00351B40` → `0x0037D120` → `0x00307240`) writes bit `0x4` of the party block word
`[0x02EBF190] + 0x5B04` and `seteventparty2mode` (`0x0514`) bit `0x8`; `geteventpartymode` (`0x0510`,
`0x00355FE0`) returns whether the mode ladder `0x0030D9A0` reads 4, and `geteventpartymodebit`
(`0x0513`) returns bit `0x4`.

## Layouts

<details>
<summary>Show the memory layouts</summary>

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2EBF190` | `void*` | partyBlock | `+0x5B04` bit `0x4` event party mode, bit `0x8` event party mode 2 |
| `+0x2EBCC68` | `void*` | summonLeader | the leader's actor |
| `+0x2EBCC70` | `u32` | summonLeaderHandle | the leader's handle |
| `+0x2EBCAC0` | `void*[32]` | followers | the unique follower actors |
| `+0x2EBCBC0` | `i32` | followerCount | count of `followers` |
| `+0x2EBCBE0` | `u32[32]` | followerHandles | the handles as passed |
| `+0x2EBCC60` | `i32` | followerRequested | the requested count, at most 32 |

Actor record fields used here:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x09` | `u8` | summonFlags | bit `0x1` cleared on a manager-3 actor before it captures a controlled actor (`0x003B736E`), bit `0x4` follower (also set on the summoner's actor by `0x003B6D60`, `0x003B6DA0`), bit `0x8` dedup mark, bit `0x10` follower candidate |
| `+0x18` | `u8` | bindState | 1 captured, 2 capturer |
| `+0x19` | `u8` | otherManager | the bound partner's manager |
| `+0x1A` | `u16` | otherId | the bound partner's id |

PoseSnapshot (at `+0xED0` of the record an actor's `+0x30` points to):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `f32[3]` | position | from `0x00265020`: body `+0x00`-`+0x08` for class 1 or 3, else 0 |
| `+0x10` | `f32[3]` | bodyVector | body `+0x20` to `+0x28`, from `0x00265240`, class 3 only (other classes leave it unchanged) |
| `+0x24` | `f32` | heading | from `0x00265200`: body `+0xA8` for class 3, `+0x38` for class 1, else 0.0 |
| `+0x34` | `f32` | moveHeading | from `0x00263CC0`: body `+0xA4` for class 3, `+0x38` for class 1, else 0.0 |
| `+0x64` | `i8` | presentation13 | presentation `+0x13`, from `0x002E9BE0`; -1 when the actor has no presentation record |

</details>

## Shipped data

<details>
<summary>Show the shipped data</summary>

| Fact | Value |
|---|---|
| `capturepc` uses in the US scripts | 8,353; `releasepc` 8,632 |
| `hideparty` uses | 1,539 |

</details>

## Operations

Per capture: one binding write on each record and one action cancel.

## State

<details>
<summary>Show the state it keeps</summary>

The capture bindings in every actor record, the summon leader and follower globals, and the party block mode
word.

</details>

## Modding notes

- `capturepc(−1)` always takes the character the player controls; a script that needs a specific
  member passes its slot.
- `hideparty` hides bodies only; the actors keep running and can still be captured.
- `releasepc` rebuilds the body pointers from the record's sequence (`+0x03` bits `0x1F`, read by
  `0x00266AD0` at `0x00266AD3`), so a capturer that swapped them is not restored to a saved state but to
  that sequence's default¹.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002694F8` |

</details>

## Related

- [Event scenes](event-scenes.md): loading, playing and disposing a scene, movies and skips.
- [The world lock](world-lock.md): what holds everyone else still during a talk or scene.
- [Party verbs](party-verbs.md): the summon party switches.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 597 calls with 75 other topics</summary>

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md), [party control modes](../Engine-Core/party-control-modes.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [hud](../Menus-And-HUD/hud.md), [frame update order](../Engine-Core/frame-update-order.md), [battle verbs](battle-verbs.md), [target selection](../Battle-Actions/target-selection.md), [script name bindings](script-name-bindings.md), [script requests](script-requests.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [actor record fields](../Characters-And-Objects/actor-record-fields.md), [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [reward verbs](reward-verbs.md), [debug menu](../Engine-Core/debug-menu.md), [party verbs](party-verbs.md), [field runtime](../Characters-And-Objects/field-runtime.md), [event scenes](event-scenes.md), [battle units](../Characters-And-Objects/battle-units.md), [actor managers](../Characters-And-Objects/actor-managers.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0026B500`](party-during-scenes.md) | is called by | [`0x003B6CC0`](../Engine-Core/subsystem-update-flags.md) (on subsystem update flags)<br>[`0x003B6D60`](party-during-scenes.md) |
| [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility | is called by | [`0x00265B60`](../Characters-And-Objects/actor-record.md) (on actor record)<br>[`0x002E35B0`](../Menus-And-HUD/clan-primer.md) (on clan primer) |
| [`0x003B6F30`](party-during-scenes.md) | calls | [`0x003B6D60`](party-during-scenes.md) |
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is called by | [`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots)<br>[`0x0035A8D0`](verb-table.md) (on verb table) |
| [`0x00263940`](party-during-scenes.md) | is called by | [`0x00271380`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x002718E0`](party-during-scenes.md) |
| [`0x00263A30`](party-during-scenes.md) | calls | [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x00263BE0`](../Battle-Actions/target-selection.md) (on target selection) | is called by | [`0x0035A7A0`](party-during-scenes.md)<br>[`0x0035A990`](party-during-scenes.md)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x00263CC0`](party-during-scenes.md) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta)<br>[`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x00263F40`](party-during-scenes.md) | calls | [`0x003587C0`](script-requests.md) (on script requests) |
| [`0x00264050`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x00264670`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta) |
| [`0x002647B0`](party-during-scenes.md) | is called by | [`0x0035A7A0`](party-during-scenes.md)<br>[`0x0035A990`](party-during-scenes.md)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x002647C0`](party-during-scenes.md) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x00236300`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: snapshot world actor runtime state (on heading speed to position delta)<br>[`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x00265240`](party-during-scenes.md) | is called by | [`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x00266AD0`](party-during-scenes.md) | is called by | [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record)<br>[`0x002693D0`](party-during-scenes.md) |
| [`0x002681E0`](party-during-scenes.md) | calls | [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) |
| [`0x002681E0`](party-during-scenes.md) | is called by | [`0x00266530`](../Characters-And-Objects/actor-record.md) Actor storage: initialize record (on actor record)<br>[`0x002693D0`](party-during-scenes.md) |
| [`0x002693D0`](party-during-scenes.md) | calls | [`0x00266AD0`](party-during-scenes.md)<br>[`0x002693D0`](party-during-scenes.md)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x002693D0`](party-during-scenes.md) | is called by | [`0x0025B070`](../Characters-And-Objects/actor-lifecycle.md) Actor system: release manager records (on actor lifecycle)<br>[`0x002693D0`](party-during-scenes.md)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x00269530`](party-during-scenes.md) | calls | [`0x002693D0`](party-during-scenes.md)<br>[`0x003587C0`](script-requests.md) (on script requests) |
| [`0x0026A0D0`](party-during-scenes.md) Actor: set desired movement heading | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x0026AE90`](party-during-scenes.md) Movement: set steering mode | is called by | [`0x002693D0`](party-during-scenes.md) |
| [`0x0026B620`](party-during-scenes.md) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x0026C120`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md) |
| [`0x0026D6D0`](party-during-scenes.md) | is called by | [`0x0035A590`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0035A720`](battle-verbs.md) (on battle verbs)<br>[`0x0035A7A0`](party-during-scenes.md)<br>[`0x0035A8D0`](verb-table.md) (on verb table)<br>[`0x003B6F80`](party-during-scenes.md) |
| [`0x002E4A40`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002E4F40`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md) |
| [`0x002E6300`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md) |
| [`0x002E7600`](world-lock.md) (on world lock) | is called by | [`0x00263050`](world-lock.md) (on world lock)<br>[`0x00263230`](world-lock.md) (on world lock)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x002E8EE0`](world-lock.md) (on world lock) | is called by | [`0x00263050`](world-lock.md) (on world lock)<br>[`0x00263230`](world-lock.md) (on world lock)<br>[`0x002693D0`](party-during-scenes.md)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility | is called by | [`0x002EBB80`](reward-verbs.md) (on reward verbs) |
| [`0x002E9560`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md) |
| [`0x002E97B0`](party-during-scenes.md) | is called by | [`0x0035A720`](battle-verbs.md) (on battle verbs)<br>[`0x0035A7A0`](party-during-scenes.md)<br>[`0x0035A8D0`](verb-table.md) (on verb table)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002E9BE0`](party-during-scenes.md) | is called by | [`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x002EAC90`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002EB030`](party-during-scenes.md) | is called by | [`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields) |
| [`0x002EB430`](party-during-scenes.md) | is called by | [`0x002693D0`](party-during-scenes.md)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x002EBE50`](party-during-scenes.md) | is called by | [`0x00263050`](world-lock.md) (on world lock)<br>[`0x00263230`](world-lock.md) (on world lock)<br>[`0x002693D0`](party-during-scenes.md)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | is called by | [`0x00300FC0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x00341CB0`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x00346FA0`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal<br>[`0x003B6F80`](party-during-scenes.md) |
| [`0x00348DA0`](party-during-scenes.md) | calls | [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x0034C3D0`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record)<br>[`0x0035AE10`](party-during-scenes.md) |
| [`0x00352FA0`](party-during-scenes.md) | calls | [`0x00264050`](party-during-scenes.md)<br>[`0x0035AE10`](party-during-scenes.md) |
| [`0x00354E10`](party-during-scenes.md) | calls | [`0x00263A30`](party-during-scenes.md) |
| [`0x003587C0`](script-requests.md) (on script requests) | calls | [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x003587C0`](script-requests.md) (on script requests) | is called by | [`0x0025AE00`](party-during-scenes.md)<br>[`0x00268650`](script-requests.md) (on script requests)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability)<br>[`0x0026CE60`](../Characters-And-Objects/actor-managers.md) Actor system: initialize manager runtime (on actor managers)<br>[`0x003DBDC0`](script-requests.md) Actor resource: start entry script execution (on script requests)<br>[`0x003DC0D0`](script-requests.md) (on script requests) |
| [`0x00358800`](party-during-scenes.md) | calls | [`0x00263A30`](party-during-scenes.md)<br>[`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is called by | [`0x0025AE00`](party-during-scenes.md)<br>[`0x0025B070`](../Characters-And-Objects/actor-lifecycle.md) Actor system: release manager records (on actor lifecycle)<br>[`0x0025B250`](script-requests.md) (on script requests)<br>[`0x0025B820`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x0025C070`](event-scenes.md) (on event scenes)<br>[`0x0025C170`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00263A30`](party-during-scenes.md)<br>[`0x00264010`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00264050`](party-during-scenes.md)<br>[`0x00265A20`](../Engine-Core/frame-update-order.md) Actor system: bind battle units for eligible records (on frame update order)<br>[`0x00266C50`](../EBP-Script-Files/ebp-script-image.md) (on ebp script image) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is also called by | [`0x00268B10`](script-requests.md) (on script requests)<br>[`0x00268D10`](script-requests.md) (on script requests)<br>[`0x002693D0`](party-during-scenes.md)<br>[`0x00269800`](../Characters-And-Objects/field-runtime.md) (on field runtime)<br>[`0x00269AD0`](script-requests.md) (on script requests)<br>[`0x00269BA0`](script-requests.md) (on script requests)<br>[`0x0026B8E0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0026CE60`](../Characters-And-Objects/actor-managers.md) Actor system: initialize manager runtime (on actor managers)<br>[`0x0026D3E0`](script-variables.md) (on script variables)<br>[`0x0035A590`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0035A7A0`](party-during-scenes.md)<br>[`0x0035A990`](party-during-scenes.md) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is also called by | [`0x003B6F80`](party-during-scenes.md)<br>[`0x003DB1F0`](../Engine-Core/frame-update-order.md) (on frame update order)<br>[`0x0046BAC0`](../Battle-Actions/target-selection.md) (on target selection) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x00234480`](../Characters-And-Objects/battle-unit-fields.md) Battle unit: allocate slot and bind actor (on battle unit fields)<br>[`0x0025C230`](script-requests.md) (on script requests)<br>[`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x00268650`](script-requests.md) (on script requests)<br>[`0x00268D10`](script-requests.md) (on script requests)<br>[`0x0037B4D0`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x003B6F80`](party-during-scenes.md) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x0025B600`](script-requests.md) (on script requests)<br>[`0x0025D9E0`](../Story-Events-And-Hunts/opening-setup-scripts.md) Actor manager: run field runtime pass (on opening setup scripts)<br>[`0x00263050`](world-lock.md) (on world lock)<br>[`0x00263230`](world-lock.md) (on world lock)<br>[`0x00263AC0`](../Characters-And-Objects/battle-units.md) (on battle units)<br>[`0x00264010`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00264050`](party-during-scenes.md)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability)<br>[`0x0026C8C0`](../Game-Files-And-Data-Tables/character-se-tables-chse.md) Actor manager: bind loaded definition payload (on character se tables chse)<br>[`0x0026DFB0`](script-requests.md) (on script requests) |
| [`0x00359B80`](party-during-scenes.md) | is called by | [`0x00265A20`](../Engine-Core/frame-update-order.md) Actor system: bind battle units for eligible records (on frame update order)<br>[`0x003B73B0`](party-during-scenes.md)<br>[`0x003B7440`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x0035AA50`](party-during-scenes.md) | calls | [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x0035AE10`](party-during-scenes.md) | calls | [`0x00233F50`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |
| [`0x0035AE10`](party-during-scenes.md) | is called by | [`0x00263230`](world-lock.md) (on world lock)<br>[`0x0026C5D0`](../Controls-And-Input/action-availability.md) (on action availability) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x0025C830`](../Menus-And-HUD/text-npc-names.md) (on text npc names)<br>[`0x003266C0`](../Party/party-slots.md) Battle group: refresh four actor definitions (on party slots) |
| [`0x003B6D60`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x003B6DE0`](party-during-scenes.md) | calls | [`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x003B6DE0`](party-during-scenes.md) | is called by | [`0x003B6F80`](party-during-scenes.md) |
| [`0x003B6F30`](party-during-scenes.md) | calls | [`0x003B6DE0`](party-during-scenes.md)<br>[`0x003B7510`](party-during-scenes.md) |
| [`0x003B6F80`](party-during-scenes.md) | calls | [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal<br>[`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets)<br>[`0x003B6DE0`](party-during-scenes.md) |
| [`0x003B7180`](party-during-scenes.md) | calls | [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) |
| [`0x003B72F0`](party-during-scenes.md) | calls | [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x003B73B0`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position<br>[`0x00359B80`](party-during-scenes.md) |
| [`0x003B73B0`](party-during-scenes.md) | is called by | [`0x003B7440`](party-during-scenes.md) |
| [`0x003B7440`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position<br>[`0x00359B80`](party-during-scenes.md)<br>[`0x003B73B0`](party-during-scenes.md) |
| [`0x003B7510`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position<br>[`0x00359B80`](party-during-scenes.md) |
| [`0x003B7770`](party-during-scenes.md) | calls | [`0x00263FF0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record)<br>[`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal |
| [`0x003B7A30`](party-during-scenes.md) | calls | [`0x002693D0`](party-during-scenes.md) |
| [`0x003B7AB0`](party-during-scenes.md) | calls | [`0x002693D0`](party-during-scenes.md) |
| [`0x003B7B00`](party-during-scenes.md) | calls | [`0x00359B80`](party-during-scenes.md) |
| [`0x003B7D80`](party-during-scenes.md) | calls | [`0x00359B80`](party-during-scenes.md) |
| [`0x003B7E20`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position<br>[`0x003588B0`](../Characters-And-Objects/actor-record.md) Actor handle: resolve registry entry by packed id (on actor record) |
| [`0x003B7F40`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position |
| [`0x00505240`](party-during-scenes.md) | calls | [`0x00265020`](party-during-scenes.md) Actor: get world position<br>[`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) |

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00362850`](../Sound-And-Music/spatial-sound.md) (on spatial sound) |

**Enemy AI and gambits** (explained on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [glossary](../Engine-Core/glossary.md), [battle verbs](battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263940`](party-during-scenes.md) | is called by | [`0x0032A4D0`](../Enemy-AI-And-Gambits/enemy-ai.md) Battle perception: test cached spatial visibility pair (on enemy ai) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x0030F130`](../Party/party-slots.md) Ai order: build candidate target buffer from stored range and status (on party slots) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x003014C0`](../Enemy-AI-And-Gambits/gambits.md) Ai order: evaluate and resolve action target (on gambits)<br>[`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets)<br>[`0x00305AB0`](../Enemy-AI-And-Gambits/gambits.md) Battle unit: select and commit next action (on gambits) |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md), [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [traps](../World-Areas-And-Travel/traps.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [battle orders](../Battle-Actions/battle-orders.md), [action phases](../Battle-Actions/action-phases.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [reward verbs](reward-verbs.md), [jump thunks](../Engine-Core/jump-thunks.md), [quickenings and summons](../Battle-Actions/quickenings-and-summons.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [action definition row](../Battle-Actions/action-definition-row.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [call signatures](../Engine-Core/call-signatures.md), [battle verbs](battle-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0017F5B0`](party-during-scenes.md) | is called by | [`0x003065D0`](../Damage-And-Battle-Formulas/hp-and-ko.md) (on hp and ko) |
| [`0x00263F40`](party-during-scenes.md) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x002F8060`](../World-Areas-And-Travel/traps.md) Battle unit: try trigger nearby authored field action (on traps)<br>[`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect)<br>[`0x00320E10`](../Battle-Actions/action-range.md) (on action range) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x002FDC30`](../Battle-Actions/battle-orders.md) (on battle orders)<br>[`0x002FEB80`](../Battle-Actions/action-range.md) Battle action: compute effective range bands (on action range) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x0026A0D0`](party-during-scenes.md) Actor: set desired movement heading | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x0026B0C0`](party-during-scenes.md) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x0026B620`](party-during-scenes.md) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | is called by | [`0x002FFCF0`](../Engine-Core/force-fight-mode.md) Battle action: check action availability reason (on force fight mode)<br>[`0x00313DB0`](../Battle-Actions/action-phases.md) (on action phases) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x00319F50`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle actor timeline event (on ko and game over)<br>[`0x00325260`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: handle action timeline event (on ko and game over) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00317E60`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x00319090`](../Characters-And-Objects/battle-units.md) (on battle units) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x002FFA60`](../Battle-Actions/target-selection.md) Battle action: is target eligible for current action (on target selection)<br>[`0x002FFCF0`](../Engine-Core/force-fight-mode.md) Battle action: check action availability reason (on force fight mode)<br>[`0x002FFF50`](../Battle-Actions/area-of-effect.md) Battle target: compute eligibility block mask (on area of effect)<br>[`0x00305110`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x00305230`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x00305430`](../Battle-Actions/action-phases.md) (on action phases)<br>[`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect)<br>[`0x0030C010`](../Battle-Actions/combos.md) (on combos)<br>[`0x0030D160`](../Battle-Actions/area-of-effect.md) Battle: build action target set (on area of effect)<br>[`0x0030D600`](../Battle-Actions/quickenings-and-summons.md) (on quickenings and summons)<br>[`0x0030DA30`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) (on heading speed to position delta)<br>[`0x0030F760`](../Engine-Core/identifier-spaces.md) Battle unit: commit action (on identifier spaces) |
| [`0x00377C20`](party-during-scenes.md) | is also called by | [`0x00311B20`](../Menus-And-HUD/battle-menu.md) Battle unit: issue command by focus handles with optional party fanout (on battle menu)<br>[`0x00311CF0`](battle-verbs.md) Battle unit: issue command (on battle verbs)<br>[`0x00312FA0`](battle-verbs.md) Battle unit: try commit engage auto attack (on battle verbs)<br>[`0x00313CD0`](../Battle-Actions/action-commit.md) Battle unit: process pending action selection queue (on action commit)<br>[`0x00313DB0`](../Battle-Actions/action-phases.md) (on action phases) |

**Damage and battle formulas** (explained on [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x00384F40`](../Battle-Actions/action-results.md) (on action results) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00300530`](../Characters-And-Objects/battle-unit-fields.md) Battle stats: modify hp and process lethal state (on battle unit fields) |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0053DD10`](event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x0022B6E0`](../Items-Equipment-Shops-And-Licenses/bazaar.md) (on bazaar) |

**Gameplay** (explained on [bestiary](../Enemy-Spawning/bestiary.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [force fight mode](../Engine-Core/force-fight-mode.md), [enmity](../Enemy-AI-And-Gambits/enmity.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement)<br>[`0x00339630`](../Battle-Actions/action-phases.md) (on action phases) |
| [`0x002EB030`](party-during-scenes.md) | is called by | [`0x003299B0`](../Damage-And-Battle-Formulas/hp-and-ko.md) Battle unit: dispatch actor presentation event (on hp and ko) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | is called by | [`0x00309A90`](../Engine-Core/party-control-modes.md) (on party control modes) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x0031ADB0`](../Movement-And-Pathfinding/animation-driven-movement.md) (on animation driven movement) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00307D10`](../Engine-Core/force-fight-mode.md) Battle unit: update engagement state flag (on force fight mode)<br>[`0x0030A8A0`](../Party/party-slots.md) Battle unit: collect mapped four slot units by flags (on party slots)<br>[`0x0030C210`](../Enemy-AI-And-Gambits/enmity.md) Battle unit: has relationship class2 plus in slot mask (on enmity)<br>[`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md), [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x00263BE0`](../Battle-Actions/target-selection.md) (on target selection) | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x002647B0`](party-during-scenes.md) | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x00359B80`](party-during-scenes.md) | is called by | [`0x00226BE0`](world-lock.md) (on world lock) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00253C70`](../Controls-And-Input/controls.md) (on controls) |
| [`0x0053DD10`](event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x002E09A0`](../Menus-And-HUD/menus.md) (on menus)<br>[`0x0035FCA0`](../Controls-And-Input/vibration.md) (on vibration)<br>[`0x0035FDD0`](../Controls-And-Input/controls.md) (on controls)<br>[`0x0046DD50`](../Game-Files-And-Data-Tables/file-size-tables-fst.md) (on file size tables fst) |

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00313A00`](../Battle-Actions/action-phases.md) (on action phases) |

**Items, equipment, shops and licenses** (explained on [reward verbs](reward-verbs.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00309FB0`](../Party/party-slots.md) Inventory: query owned count including reserved action items (on party slots)<br>[`0x0030FD10`](../Items-Equipment-Shops-And-Licenses/equipment.md) Equipment: unequip encoded item from active roster (on equipment) |

**Movement and pathfinding** (explained on [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [bestiary](../Enemy-Spawning/bestiary.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [battle units](../Characters-And-Objects/battle-units.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md), [world lock](world-lock.md), [party control modes](../Engine-Core/party-control-modes.md), [party data](../Party/party-data.md), [force fight mode](../Engine-Core/force-fight-mode.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md), [target selection](../Battle-Actions/target-selection.md), [party leader](../Party/party-leader.md), [actor record fields](../Characters-And-Objects/actor-record-fields.md), [ebp position entries](../EBP-Script-Files/ebp-position-entries.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [native commands](native-commands.md), [script binding lifecycle](script-binding-lifecycle.md), [script requests](script-requests.md), [verb table](verb-table.md), [player movement](../Movement-And-Pathfinding/player-movement.md), [party slots](../Party/party-slots.md), [script name bindings](script-name-bindings.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x0017F5B0`](party-during-scenes.md) | is called by | [`0x003B7E20`](party-during-scenes.md) |
| [`0x0025A5F0`](party-during-scenes.md) | is called by | [`0x003B7E20`](party-during-scenes.md) |
| [`0x00262F90`](party-during-scenes.md) | calls | [`0x002E4A40`](party-during-scenes.md) |
| [`0x00263750`](../Graphics/model-asset-list.md) (on model asset list) | is called by | [`0x0034A940`](party-during-scenes.md)<br>[`0x0037CF00`](party-during-scenes.md)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots) |
| [`0x00263940`](party-during-scenes.md) | is called by | [`0x00334C90`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x003357B0`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: query dynamic actor obstruction (on battle locomotion)<br>[`0x0033D660`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: check actor pair clearance (on battle locomotion)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x00263CC0`](party-during-scenes.md) | is called by | [`0x002E5750`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |
| [`0x00263F40`](party-during-scenes.md) | is called by | [`0x00300310`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position (on spawn record fields)<br>[`0x003003F0`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position and facing (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x0033FFC0`](party-during-scenes.md)<br>[`0x00345430`](verb-table.md) (on verb table)<br>[`0x00349680`](party-during-scenes.md)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots)<br>[`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7D80`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x002644C0`](party-during-scenes.md) | is called by | [`0x003B7F40`](party-during-scenes.md) |
| [`0x00264670`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x003B7F40`](party-during-scenes.md) |
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x0024B6F0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002EBFA0`](world-lock.md) (on world lock)<br>[`0x002EC2C0`](world-lock.md) (on world lock)<br>[`0x00300310`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00311E20`](../Engine-Core/party-control-modes.md) (on party control modes)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x00336710`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: build solver context (on battle locomotion)<br>[`0x00337C10`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x00337D90`](../Random-Numbers/which-roll-uses-which-generator.md) (on which roll uses which generator) |
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is also called by | [`0x0033CA00`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x003B7E20`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x002FB340`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) (on navigation mesh and pathfinding)<br>[`0x002FB500`](party-during-scenes.md)<br>[`0x00309B10`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0030A130`](../Battle-Actions/action-range.md) Battle unit: get navigation clearance radius (on action range)<br>[`0x00312730`](../EBP-Script-Files/ebp-position-entries.md) Battle locomotion: decode order goal (on ebp position entries)<br>[`0x00334790`](../Battle-Actions/target-selection.md) (on target selection)<br>[`0x00334A70`](../Battle-Actions/target-selection.md) (on target selection)<br>[`0x00336210`](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md) (on navigation mesh and pathfinding)<br>[`0x00336710`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: build solver context (on battle locomotion)<br>[`0x00336E40`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x00337700`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x003377C0`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is also called by | [`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x00339A60`](../Party/party-leader.md) (on party leader)<br>[`0x00339BF0`](../Engine-Core/force-fight-mode.md) Battle locomotion: compute step distance (on force fight mode)<br>[`0x0033A720`](../Movement-And-Pathfinding/battle-locomotion.md) (on battle locomotion)<br>[`0x0033D660`](../Movement-And-Pathfinding/battle-locomotion.md) Battle locomotion: check actor pair clearance (on battle locomotion)<br>[`0x00392170`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x00392740`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x0024B6F0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x002E5750`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002EBE50`](party-during-scenes.md)<br>[`0x002FB500`](party-during-scenes.md)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x003343D0`](../Random-Numbers/which-roll-uses-which-generator.md) Battle locomotion: try start randomized avoidance maneuver (on which roll uses which generator)<br>[`0x00336E40`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over)<br>[`0x00338490`](../Party/party-leader.md) Party follow: solve formation (on party leader)<br>[`0x0033CA00`](../Status-Effects-And-KO/ko-and-game-over.md) (on ko and game over) |
| [`0x00265240`](party-during-scenes.md) | is called by | [`0x00505240`](party-during-scenes.md) |
| [`0x002681E0`](party-during-scenes.md) | is called by | [`0x0025DF00`](../Characters-And-Objects/field-runtime.md) World actor: update runtime and script execution state (on field runtime)<br>[`0x0026A7F0`](../World-Areas-And-Travel/chocobos-and-airships.md) (on chocobos and airships) |
| [`0x002693D0`](party-during-scenes.md) | calls | [`0x0026AE90`](party-during-scenes.md) Movement: set steering mode<br>[`0x0026C120`](party-during-scenes.md)<br>[`0x002E4A40`](party-during-scenes.md)<br>[`0x002E6300`](party-during-scenes.md)<br>[`0x002EBE50`](party-during-scenes.md) |
| [`0x0026A0D0`](party-during-scenes.md) Actor: set desired movement heading | is called by | [`0x00239210`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x0023A070`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Battle unit: apply movement intent to world actor (on heading speed to position delta)<br>[`0x003003F0`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position and facing (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00310D30`](party-during-scenes.md)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x0034A940`](party-during-scenes.md)<br>[`0x003538C0`](party-during-scenes.md)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots)<br>[`0x003B7B00`](party-during-scenes.md) |
| [`0x0026ACE0`](party-during-scenes.md) | is called by | [`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md) |
| [`0x0026AE90`](party-during-scenes.md) Movement: set steering mode | calls | [`0x002E55C0`](party-during-scenes.md) Movement: clear steering request |
| [`0x0026AE90`](party-during-scenes.md) Movement: set steering mode | is called by | [`0x002EAB80`](world-lock.md) (on world lock)<br>[`0x00343E20`](party-during-scenes.md)<br>[`0x00344290`](party-during-scenes.md)<br>[`0x0034EBC0`](party-during-scenes.md)<br>[`0x0034F210`](party-during-scenes.md)<br>[`0x00350510`](party-during-scenes.md)<br>[`0x00350C30`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x00357980`](../Movement-And-Pathfinding/facing-and-steering.md) Vm: actor steer toward actor (on facing and steering)<br>[`0x00357A20`](verb-table.md) (on verb table)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots) |
| [`0x0026B0C0`](party-during-scenes.md) | calls | [`0x002E4A10`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002E5C70`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |
| [`0x0026B0C0`](party-during-scenes.md) | is called by | [`0x0026B170`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026B230`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026BA70`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00300310`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00310D30`](party-during-scenes.md)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x0034EBC0`](party-during-scenes.md)<br>[`0x0034F210`](party-during-scenes.md)<br>[`0x00350510`](party-during-scenes.md)<br>[`0x00350C30`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots) |
| [`0x0026B0C0`](party-during-scenes.md) | is also called by | [`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x0026B620`](party-during-scenes.md) | calls | [`0x0026B6A0`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |
| [`0x0026B620`](party-during-scenes.md) | is called by | [`0x00239210`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x0026C120`](party-during-scenes.md)<br>[`0x003003F0`](../Enemy-Spawning/spawn-record-fields.md) Battle unit: publish locomotion position and facing (on spawn record fields)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00310D30`](party-during-scenes.md)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields)<br>[`0x0034A940`](party-during-scenes.md)<br>[`0x00350510`](party-during-scenes.md)<br>[`0x00350C30`](../EBP-Script-Files/ebp-navigation-icons.md) (on ebp navigation icons)<br>[`0x0037D000`](../Party/party-slots.md) (on party slots)<br>[`0x003B7B00`](party-during-scenes.md) |
| [`0x0026B720`](party-during-scenes.md) | is called by | [`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7D80`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x0026C120`](party-during-scenes.md) | calls | [`0x0026B620`](party-during-scenes.md)<br>[`0x002E6300`](party-during-scenes.md)<br>[`0x002EBE50`](party-during-scenes.md) |
| [`0x0026C120`](party-during-scenes.md) | is called by | [`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002E55C0`](party-during-scenes.md) Movement: clear steering request<br>[`0x002E5750`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002EAB80`](world-lock.md) (on world lock)<br>[`0x0033FFC0`](party-during-scenes.md)<br>[`0x00345430`](verb-table.md) (on verb table)<br>[`0x003488B0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00349680`](party-during-scenes.md)<br>[`0x003567D0`](party-during-scenes.md) |
| [`0x0026D6D0`](party-during-scenes.md) | calls | [`0x0026D6F0`](world-lock.md) Movement: set requested speed (on world lock) |
| [`0x002E4A40`](party-during-scenes.md) | calls | [`0x002ED6A0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x002E4A40`](party-during-scenes.md) | is called by | [`0x002E5180`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) (on heading speed to position delta)<br>[`0x0037CF00`](party-during-scenes.md)<br>[`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md) |
| [`0x002E6300`](party-during-scenes.md) | is called by | [`0x0026C120`](party-during-scenes.md) |
| [`0x002E7600`](world-lock.md) (on world lock) | is called by | [`0x002690D0`](world-lock.md) (on world lock) |
| [`0x002E8EE0`](world-lock.md) (on world lock) | is called by | [`0x0026C120`](party-during-scenes.md)<br>[`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002E3110`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild)<br>[`0x002E64E0`](world-lock.md) (on world lock)<br>[`0x002EAAA0`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering)<br>[`0x002EBE50`](party-during-scenes.md) |
| [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility | is called by | [`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x002E3110`](../Characters-And-Objects/actor-model-rebuild.md) (on actor model rebuild) |
| [`0x002E97B0`](party-during-scenes.md) | is called by | [`0x0025DF00`](../Characters-And-Objects/field-runtime.md) World actor: update runtime and script execution state (on field runtime)<br>[`0x0026A490`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation) |
| [`0x002EB030`](party-during-scenes.md) | is called by | [`0x003B7E20`](party-during-scenes.md) |
| [`0x002EB430`](party-during-scenes.md) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x0033FFC0`](party-during-scenes.md)<br>[`0x00345430`](verb-table.md) (on verb table)<br>[`0x00349680`](party-during-scenes.md) |
| [`0x002EBE50`](party-during-scenes.md) | calls | [`0x00265200`](party-during-scenes.md)<br>[`0x002EC3F0`](../Movement-And-Pathfinding/facing-and-steering.md) (on facing and steering) |
| [`0x002EBE50`](party-during-scenes.md) | is called by | [`0x002690D0`](world-lock.md) (on world lock)<br>[`0x0026C120`](party-during-scenes.md) |
| [`0x002EC680`](party-during-scenes.md) | is called by | [`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7F40`](party-during-scenes.md) |
| [`0x002ECE50`](../Battle-Actions/action-range.md) (on action range) | is called by | [`0x003B7F40`](party-during-scenes.md) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | is called by | [`0x00309AE0`](../Party/party-leader.md) (on party leader)<br>[`0x00311F70`](../Enemy-Spawning/spawn-record-fields.md) (on spawn record fields) |
| [`0x00340DA0`](party-during-scenes.md) | calls | [`0x003B8140`](party-during-scenes.md) |
| [`0x003410A0`](party-during-scenes.md) | calls | [`0x003B8170`](party-during-scenes.md) |
| [`0x003587C0`](script-requests.md) (on script requests) | is called by | [`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002EBFA0`](world-lock.md) (on world lock)<br>[`0x00377560`](verb-table.md) (on verb table) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is called by | [`0x00392740`](../World-Areas-And-Travel/mpk-map-pack.md) (on mpk map pack) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x002E5610`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) Movement: integrate position and measure displacement (on heading speed to position delta)<br>[`0x002EBFA0`](world-lock.md) (on world lock) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x0026D6F0`](world-lock.md) Movement: set requested speed (on world lock)<br>[`0x0026D810`](../Movement-And-Pathfinding/player-movement.md) (on player movement)<br>[`0x002E45E0`](../Movement-And-Pathfinding/facing-and-steering.md) Movement: update steering toward target (on facing and steering)<br>[`0x002E5180`](../Movement-And-Pathfinding/heading-speed-to-position-delta.md) (on heading speed to position delta)<br>[`0x00319490`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) (on loot pickups)<br>[`0x00325D90`](battle-verbs.md) Battle unit: can advance combat navigation (on battle verbs)<br>[`0x00326BB0`](../Party/party-data.md) (on party data)<br>[`0x00326D60`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x00343E20`](party-during-scenes.md)<br>[`0x00345430`](verb-table.md) (on verb table) |
| [`0x00359B80`](party-during-scenes.md) | is called by | [`0x0025DF00`](../Characters-And-Objects/field-runtime.md) World actor: update runtime and script execution state (on field runtime)<br>[`0x003B7B00`](party-during-scenes.md)<br>[`0x003B7D80`](party-during-scenes.md) |
| [`0x0035AE10`](party-during-scenes.md) | is called by | [`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze) |
| [`0x0036D840`](party-during-scenes.md) | is called by | [`0x003B7E20`](party-during-scenes.md) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x0025B470`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x0026C3E0`](../Engine-Core/time-stop-and-freeze.md) (on time stop and freeze)<br>[`0x002E28E0`](../Movement-And-Pathfinding/movement-bodies-and-separation.md) (on movement bodies and separation)<br>[`0x00310920`](../Party/party-slots.md) (on party slots)<br>[`0x00313670`](../Party/party-slots.md) (on party slots) |
| [`0x003B6F80`](party-during-scenes.md) | calls | [`0x0026D6D0`](party-during-scenes.md) |
| [`0x003B73B0`](party-during-scenes.md) | calls | [`0x00263CC0`](party-during-scenes.md)<br>[`0x00265200`](party-during-scenes.md)<br>[`0x00265240`](party-during-scenes.md) |
| [`0x003B7440`](party-during-scenes.md) | calls | [`0x00263CC0`](party-during-scenes.md)<br>[`0x00265200`](party-during-scenes.md)<br>[`0x00265240`](party-during-scenes.md) |
| [`0x003B7510`](party-during-scenes.md) | calls | [`0x00263CC0`](party-during-scenes.md)<br>[`0x00265200`](party-during-scenes.md)<br>[`0x00265240`](party-during-scenes.md) |
| [`0x003B7B00`](party-during-scenes.md) | calls | [`0x0026A0D0`](party-during-scenes.md) Actor: set desired movement heading<br>[`0x0026ACE0`](party-during-scenes.md)<br>[`0x0026B0C0`](party-during-scenes.md)<br>[`0x0026B620`](party-during-scenes.md)<br>[`0x0026B720`](party-during-scenes.md)<br>[`0x002E4A40`](party-during-scenes.md) |
| [`0x003B7BB0`](party-during-scenes.md) | calls | [`0x003B7B00`](party-during-scenes.md) |
| [`0x003B7C60`](party-during-scenes.md) | calls | [`0x003B7B00`](party-during-scenes.md) |
| [`0x003B7D80`](party-during-scenes.md) | calls | [`0x0026B720`](party-during-scenes.md) |
| [`0x003B7D80`](party-during-scenes.md) | is called by | [`0x003B8140`](party-during-scenes.md)<br>[`0x003B8170`](party-during-scenes.md) |
| [`0x003B7E20`](party-during-scenes.md) | calls | [`0x003B7F40`](party-during-scenes.md) |
| [`0x003B7F40`](party-during-scenes.md) | calls | [`0x002644C0`](party-during-scenes.md)<br>[`0x00264670`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x0026ACE0`](party-during-scenes.md)<br>[`0x0026B0C0`](party-during-scenes.md)<br>[`0x002E4A40`](party-during-scenes.md) |
| [`0x003B7F40`](party-during-scenes.md) | is called by | [`0x003B7E20`](party-during-scenes.md) |
| [`0x003B8030`](party-during-scenes.md) | calls | [`0x0026B620`](party-during-scenes.md) |
| [`0x003B8140`](party-during-scenes.md) | calls | [`0x003B7D80`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x003B8170`](party-during-scenes.md) | calls | [`0x003B7D80`](party-during-scenes.md)<br>[`0x00505240`](party-during-scenes.md) |
| [`0x003CC130`](party-during-scenes.md) | is called by | [`0x00505240`](party-during-scenes.md) |
| [`0x003CC2F0`](party-during-scenes.md) | is called by | [`0x00505240`](party-during-scenes.md) |
| [`0x00505240`](party-during-scenes.md) | calls | [`0x00263940`](party-during-scenes.md)<br>[`0x00265240`](party-during-scenes.md)<br>[`0x0026B0C0`](party-during-scenes.md)<br>[`0x0026B720`](party-during-scenes.md) |
| [`0x00505240`](party-during-scenes.md) | is called by | [`0x003B8140`](party-during-scenes.md)<br>[`0x003B8170`](party-during-scenes.md) |

**Graphics** (explained on [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [frame update order](../Engine-Core/frame-update-order.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [weather](../World-Areas-And-Travel/weather.md), [bestiary](../Enemy-Spawning/bestiary.md), [map screens](../Menus-And-HUD/map-screens.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [character render records](../Graphics/character-render-records.md), [party verbs](party-verbs.md), [script name bindings](script-name-bindings.md), [battle units](../Characters-And-Objects/battle-units.md), [effect element runtime](../Graphics/effect-element-runtime.md), [effect element types](../Graphics/effect-element-types.md), [battle numbers](../Menus-And-HUD/battle-numbers.md), [hud](../Menus-And-HUD/hud.md), [authored presentation commands](../Graphics/authored-presentation-commands.md), [legacy ps2 gs layer](../Graphics/legacy-ps2-gs-layer.md), [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle verbs](battle-verbs.md), [add motion tables](../Graphics/add-motion-tables.md), [scripted camera](../Graphics/scripted-camera.md), [field camera](../Graphics/field-camera.md), [collision mesh movement](../Movement-And-Pathfinding/collision-mesh-movement.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00263940`](party-during-scenes.md) | is called by | [`0x003223C0`](party-during-scenes.md) |
| [`0x00263F40`](party-during-scenes.md) | is called by | [`0x003B70B0`](party-during-scenes.md) |
| [`0x00264670`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x003A4290`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x003B62D0`](../Graphics/authored-presentation-commands.md) (on authored presentation commands) |
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x002B7B80`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x00322360`](../Movement-And-Pathfinding/battle-locomotion.md) Battle unit: test actor view frustum at current position (on battle locomotion)<br>[`0x0037AD40`](../EBP-Script-Files/ebp-lighting-lgt2.md) (on ebp lighting lgt2)<br>[`0x003A40F0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x003C29A0`](../Menus-And-HUD/map-screens.md) (on map screens)<br>[`0x003C37B0`](../Engine-Core/ps2-cpu-emulation.md) (on ps2 cpu emulation) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x003223C0`](party-during-scenes.md) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x003C29A0`](../Menus-And-HUD/map-screens.md) (on map screens) |
| [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility | calls | [`0x003E6A60`](party-during-scenes.md)<br>[`0x00428DE0`](party-during-scenes.md) Render record: set presentation flag400<br>[`0x00428E10`](party-during-scenes.md) Render record: set presentation flag800<br>[`0x00429020`](../Graphics/character-render-records.md) Render hierarchy: set presentation flag1000 (on character render records) |
| [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility | is called by | [`0x003B70B0`](party-during-scenes.md) |
| [`0x002E97B0`](party-during-scenes.md) | is called by | [`0x003B70B0`](party-during-scenes.md) |
| [`0x002ECD50`](party-during-scenes.md) | calls | [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility |
| [`0x002ECE50`](../Battle-Actions/action-range.md) (on action range) | calls | [`0x003E6150`](../Graphics/model-files-cm-ca.md) (on model files cm ca) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | is called by | [`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over) |
| [`0x003587C0`](script-requests.md) (on script requests) | is called by | [`0x00256F60`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is called by | [`0x003A4290`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x00465120`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00465690`](../Graphics/lens-flares.md) (on lens flares) |
| [`0x003589B0`](../Graphics/effect-anchors-and-targets.md) Actor handle: encode registry entry (on effect anchors and targets) | is called by | [`0x003A4290`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x00465120`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00465690`](../Graphics/lens-flares.md) (on lens flares)<br>[`0x00506700`](../Menus-And-HUD/battle-numbers.md) (on battle numbers) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x003A4290`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets)<br>[`0x003A56F0`](../Graphics/effect-element-runtime.md) (on effect element runtime)<br>[`0x003F1A60`](../Menus-And-HUD/hud.md) (on hud)<br>[`0x00426090`](../Graphics/character-render-records.md) Render system: update character records (on character render records)<br>[`0x004264A0`](../Graphics/character-render-records.md) Character render system: update lod and render state (on character render records)<br>[`0x004640A0`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x004643D0`](party-during-scenes.md)<br>[`0x00464650`](party-during-scenes.md)<br>[`0x00464BD0`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00465120`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00465690`](../Graphics/lens-flares.md) (on lens flares)<br>[`0x0046CC70`](../Sound-And-Music/animation-sounds.md) (on animation sounds) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00307E70`](../Party/party-slots.md) Party combat: update stance state (on party slots)<br>[`0x003125E0`](../Status-Effects-And-KO/ko-and-game-over.md) Battle unit: compute presentation suppression mask (on ko and game over)<br>[`0x00313B30`](../Party/party-slots.md) Battle unit: broadcast party combat target relation (on party slots)<br>[`0x003714A0`](../Graphics/add-motion-tables.md) Add motion: apply bone pose (on add motion tables) |
| [`0x003B70B0`](party-during-scenes.md) | calls | [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility |
| [`0x003B7770`](party-during-scenes.md) | calls | [`0x002E8FD0`](party-during-scenes.md) Actor: refresh presentation visibility |
| [`0x003CC130`](party-during-scenes.md) | is called by | [`0x00256960`](../Graphics/scripted-camera.md) (on scripted camera)<br>[`0x0032B1C0`](../Graphics/field-camera.md) (on field camera)<br>[`0x0032BEB0`](../Graphics/field-camera.md) (on field camera)<br>[`0x0032CA70`](../Graphics/field-camera.md) (on field camera) |
| [`0x003CC480`](party-during-scenes.md) | is called by | [`0x00256960`](../Graphics/scripted-camera.md) (on scripted camera)<br>[`0x00256CA0`](../Graphics/scripted-camera.md) (on scripted camera)<br>[`0x0032CA70`](../Graphics/field-camera.md) (on field camera) |
| [`0x0053DD10`](event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x004355D0`](../Graphics/effect-element-types.md) (on effect element types)<br>[`0x00462540`](../Graphics/script-screen-effects.md) (on script screen effects) |

**Rewards: EXP, LP, gil and loot** (explained on [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x002FB150`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) Loot: find overlapping pickup index (on loot pickups)<br>[`0x00312280`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle unit: process defeat rewards and loot (on strong and weak mode) |
| [`0x00265090`](../Movement-And-Pathfinding/battle-locomotion.md) Actor runtime: get class3 float pair (on battle locomotion) | is called by | [`0x002FB150`](../Rewards-EXP-Gil-And-Loot/loot-pickups.md) Loot: find overlapping pickup index (on loot pickups) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x00312280`](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md) Battle unit: process defeat rewards and loot (on strong and weak mode) |

**Enemy spawning** (explained on [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x00234AF0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning)<br>[`0x00234DA0`](../Party/party-slots.md) Spawn: validate candidate distance to players (on party slots)<br>[`0x002350C0`](../Enemy-Spawning/enemy-spawning.md) Spawn lifecycle: check and retire by native range (on enemy spawning) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x00234AF0`](../Enemy-Spawning/enemy-spawning.md) (on enemy spawning) |

**Status effects and KO** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [frame update order](../Engine-Core/frame-update-order.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x0030E360`](../Engine-Core/identifier-spaces.md) Battle stats: change status and process side effects (on identifier spaces)<br>[`0x0030F690`](../Damage-And-Battle-Formulas/augments.md) Battle stats: remove statuses from mask and recompute (on augments)<br>[`0x00310DB0`](../Battle-Actions/action-results.md) Battle unit: run periodic combat maintenance (on action results) |

**Menus and HUD** (explained on [battle units](../Characters-And-Objects/battle-units.md), [party list](../Menus-And-HUD/party-list.md), [map screens](../Menus-And-HUD/map-screens.md))

Each row is a function this page names (left) and the functions from this topic that call it (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00265020`](party-during-scenes.md) Actor: get world position | is called by | [`0x003C5130`](../Characters-And-Objects/battle-units.md) (on battle units) |
| [`0x00265200`](party-during-scenes.md) | is called by | [`0x003C5130`](../Characters-And-Objects/battle-units.md) (on battle units) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x00299BD0`](../Menus-And-HUD/party-list.md) (on party list)<br>[`0x002C7660`](../Menus-And-HUD/battle-menu.md) (on battle menu) |
| [`0x0053DD10`](event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x003C80C0`](../Menus-And-HUD/map-screens.md) (on map screens) |

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [frame update order](../Engine-Core/frame-update-order.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party control modes](../Engine-Core/party-control-modes.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00358940`](party-during-scenes.md) Actor manager: get record by ordinal | is called by | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x002623A0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x003590D0`](../Graphics/effect-anchors-and-targets.md) (on effect anchors and targets) | is called by | [`0x0025E400`](../Characters-And-Objects/actor-record-fields.md) (on actor record fields)<br>[`0x002623A0`](../Engine-Core/frame-update-order.md) (on frame update order) |
| [`0x002E4A40`](party-during-scenes.md) | calls | [`0x00377DB0`](../Story-Events-And-Hunts/opening-setup-scripts.md) (on opening setup scripts) |
| [`0x0030D9A0`](party-during-scenes.md) Battle runtime: get mode0 to5 from flags and field bit15 | calls | [`0x00377C20`](party-during-scenes.md) |
| [`0x00352FA0`](party-during-scenes.md) | calls | [`0x00377C20`](party-during-scenes.md) |
| [`0x00377C20`](party-during-scenes.md) | calls | [`0x003148F0`](../World-Areas-And-Travel/treasure-chests.md) World transition: get active or pending field id (on treasure chests) |
| [`0x00377C20`](party-during-scenes.md) | is called by | [`0x002342F0`](../Enemy-Spawning/enemy-respawning.md) (on enemy respawning) |
| [`0x0053DD10`](event-scenes.md) Input device: query availability state always1 (on event scenes) | is called by | [`0x003789A0`](../Graphics/effect-files-efx-efb.md) (on effect files efx efb) |

</details>
