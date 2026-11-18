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
party-focus handle (`0x003590D0`, `0x003588B0`) and, for each slot 0 to 3 whose `0x00263750` actor is
non-null and is not that actor (`0x00341CDA`, `0x00341CDC`), calls `0x002ECD50(actor, 0)` through its
thunk `0x0026DC40`. When the handle resolves to null, every non-null slot actor is hidden.

`disposepartywithoutcontrol` (`0x0202`, `0x0034C990` → `0x003B6F30`) clears the party-control dword
`0x02B40534`, empties the follower list (`0x003B6DE0`), narrows the controlled set to one actor
(`0x003B6D60`), the actor of the party slot that holds the summoner's row `+0x5AD5` ([party control
modes](../Engine-Core/party-control-modes.md), `0x003B6D69`-`0x003B6D82`), turns its [animation-driven
movement](../Movement-And-Pathfinding/animation-driven-movement.md) off (`0x0026B500`, `0x003B6D9B`) and
sets its `+9` bit `0x4` (`0x003B6DA0`), and snapshots each controlled actor's pose (`0x003B7510`).

`capturepartyforsummon`
(`0x0232`) does the same and binds the set to manager 3's entries (`0x003B72F0`): for entry i of the
second list of the script image's `+0x68` table ([EBP script image](../EBP-Script-Files/ebp-script-image.md))
with a non-negative ordinal, it clears that actor's `+9` bit `0x1` (`0x003B736E`) and has it capture
controlled actor i (`0x00262F50`, `0x003B7375`). `releasepartyforsummon` (`0x0233`) releases them
(`0x003B7AB0`, which does not read the manager slot 3 its handler passes).

`hide_freetarget_group(g)` (`0x04B8`, `0x003569E0`) and `show_freetarget_group(g)` (`0x04B9`,
`0x00356D00`) call `0x0035AA50(0, g, 0 or 1)`. It walks manager 0's ordinal window (first ordinal at
`+0x1DE`, count at `+0x1D6`), skips party members (`0x002647B0`: byte `+0x12` below 4) and passes
every other actor to `0x002ECD50`, all of them for a negative `g`, otherwise only those whose group
`0x00263BE0` returns equals `g`. The group comes from the class nibble `+0x0E`: 0 gives 1, 1, 2 and 7
give 0, 3 gives 2, any other value 1.

`0x0035AA50` takes each actor from `0x00358940` without a null test and reaches `0x002ECD50` through
`0x0026DC40`. `0x00263BE0` returns 1 for a null actor and `0x002647B0` reads byte `+0x12` of it, so a null
entry faults at `0x002647B0` for a negative `g` (`0x0035AAE0`) or a `g` of 1 (`0x0035AAAD`) and is skipped
for any other `g` (`0x0035AAA8`).

### The summon leader and followers

`setupsummonforevent(n)` (`0x0193`, `0x00346FA0`) names a leader: the actor at ordinal `n` of the current manager
(`0x002640C0`, `0x00358940`), or for a negative `n` the controlled character (`0x003590D0`, `0x003588B0`; the pop and the
choice, `0x00346FA9`-`0x00346FCC`). With a leader it ends with `0x003B6F80(leader)` as a tail jump, and with none it does
nothing (`0x00346FD4`-`0x00346FDE`).

`0x003B6F80(leader)` walks managers 0, 1 and 2 (`0x003B7036` loops while the manager index is at most 2) whose byte
`+0x10` has bit `0x1` set and collects, up to 31, the handles (`0x003589B0`) of every actor with byte `+9` bit `0x10`
set other than the leader; it clears `+9` bits `0x4` and `0x10` on every actor it visits and refreshes it
(`0x0026D6D0`).

It reads `+9` of each ordinal's `0x00358940` actor without a null test (`0x003B6FFD`), so a null entry
faults there. The leader's own handle also comes from `0x003589B0` (`0x003B6FB4`).

It then hands the list to `0x003B6DE0(leader, count, handles)`. That keeps the requested count (at
most 32, `0x003B6E12`; a negative count becomes 0, `0x003B6E05`-`0x003B6E07`) at `0x02EBCC60` and the
handles at `0x02EBCBE0`, and resolves each handle (`0x003588B0`). On each actor that resolves it clears
`+9` bit `0x8` and sets bit `0x4`, so a stale mark cannot drop an actor, and stores it in the slot;
a handle that resolves to null leaves that slot's previous pointer in place.

A second pass keeps each actor once, marking it with `+9` bit `0x8`, and writes the unique ones to the
front of the followers at `0x02EBCAC0` with their count at `0x02EBCBC0`; it reads every slot without a
null check (`0x003B6E8A`), so a slot that still holds null faults there. The leader's handle goes to
`0x02EBCC70` and its actor to `0x02EBCC68`. `0x003B6F30` calls it with an empty list, which is the
follower-list clear above.

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
leader (`0x003B73B0`) and for every non-null slot of the requested count: the position
(`0x00265020`), the three floats at body `+0x20` (`0x00265240`), the heading (`0x00265200`), the movement
heading (`0x00263CC0`, stored at `+0x34` twice, `0x003B74CB`, `0x003B74E2`) and the presentation byte `+0x13`
(`0x002E9BE0`, -1 when the actor's `+0xC0` is null, `0x002E9BF6`).

What each read gives depends on the actor's class, byte `+3` >> 5. For class 3 the position is body
`+0x00`-`+0x08`, the three floats are body `+0x20`-`+0x28`, the heading is body `+0xA8` and the movement
heading body `+0xA4`. For class 1 the position is the same, both headings are body `+0x38`, and snapshot
`+0x10`-`+0x18` keeps what it held. Any other class gets a zero position and headings of 0.0, and
`+0x10`-`+0x18` again keeps what it held (`0x00265020`-`0x0026505C`, `0x00265240`-`0x00265268`,
`0x00265200`-`0x00265233`, `0x00263CC0`-`0x00263CF3`).

A slot or leader whose `0x00359B80` record is null is skipped (`0x003B748C`; `0x003B73B0` returns for a
null leader at `0x003B73B3` and for a null record at `0x003B73CD`).

`setpossummonspace` (`0x0191`, `0x003482E0` → `0x003B7E20`) clears the party-control dword `0x02B40534`,
calls `0x0025A5F0(1)` and `0x0036D840(0)`, and takes as origin the position of the first follower
handle (`0x02EBCBE0`) when the requested count is above 0 and that handle resolves to an actor
(`0x003B7E77`), otherwise `(0, 0, 0)`. `0x003B7F40(actor, origin)` then places each follower and the
leader, or their capturers (`0x00263F40`); it returns at once for a null actor (`0x003B7F43`), which
skips a null leader.

`0x003B7F40` sets the position (`0x0026B0C0`) to the actor's own x and z minus the origin's, with a
height of 0, or of `0x002ECE50(actor, 0x9000505)` when bit `0x1` of `+0x151` in the actor's `+0xC0`
record is set (`0x002644C0`). It also computes the old height minus `0x00264670(actor)` but never
uses it, so the old height is discarded rather than offset.

It then sets presentation `+0x13` to 1 (`0x002EC680`), sets bit `0x20` of `+0x151` in the `+0xC0` record
(`0x0026ACE0`) and re-applies the render scale (`0x002E4A40`). Last, `0x003B7E20` runs the same motion
step as `summonplaymotionall`: `0x0017F5B0(1)` when `0x022BE970` is non-zero, then
`0x002EB030(follower, 0x1049)`.

`0x003B7B00(actor)` restores one snapshot, the actor's own (`0x00359B80(actor)`), onto the actor's
capturer, or the actor itself (`0x00263F40`): movement heading (`0x0026A0D0`), heading (`0x0026B620`),
the movement heading again (`0x003B7B50`), position (`0x0026B0C0`), the body `+0x20` floats
(`0x0026B720`), bit `0x20` of `+0x151` cleared (`0x0026ACE0`), presentation `+0x13` from the snapshot
(`0x002EC680`) and the render scale (`0x002E4A40`). It returns at once for a null actor (`0x003B7B03`)
or a null snapshot record (`0x003B7B2C`).

`0x002E4A40(actor)`, the render scale, acts only while `0x00377DB0()` is non-zero and the actor's presentation record
(`+0xC0`) is non-null with a first dword other than -1 (`0x002E4A57`-`0x002E4A8B`). The scale is 1.0 on all three axes
(`0x01CEBBA8`) when bit `0x20` of the presentation record's byte `+0x151` is set; otherwise it is the floats `+0x50`,
`+0x54` and `+0x58` of the presentation record's `+0x138` record (`0x00265970` returns that record plus `0x30`), read
again after `0x002ED6A0(actor, that record)` when bit `0x10` is clear (`0x002E4AAE`-`0x002E4B06`).

The first read has no null test, so a null `+0x138` record faults at `0x002E4AD9`. Each of the presentation record's
four handles at `+0x00`, `+0x30`, `+0x60` and `+0x90` whose first dword is not -1 is passed with the scale to
`0x002EDD70(its first word, x, y, z)` (`0x002E4B0C`-`0x002E4B90`).

`0x002EDD70` stores x, y and z at `+0x380`-`+0x388` of the render record the word names and sets bit `0x8` of its
`+0x290` only when the word is not -1, the record is non-null and its `+0x284` is non-zero (`0x002EDD70`-`0x002EDDAA`).

`0x002E9560(actor)`, the render value, returns 0.0 for a null actor, a null presentation record or a first dword of -1,
30.0 (`0x008F8D80`) when the record's first word is -1, or when, as a signed index, it names a render record
`[0x022C6F28] + word × 0x740` whose address is null or whose `+0x284` is 0, and otherwise the value of `0x00423280` for
that record (`0x002E9563`-`0x002E95AA`).

`summongethertarget(d)` (`0x0370`, `0x00340DA0` → `0x003B8140`) pops a float. It first has `0x003B7D80`
put back the body `+0x20` floats from the snapshot of every non-null slot of the requested count,
onto that slot's capturer or the slot actor itself (`0x00263F40`, `0x003B7DB1`), skipping a slot whose
snapshot record is null (`0x003B7DC4`), then calls `0x00505240(count, 0x02EBCAC0, d)` over all the
followers. `summongethertarget_one(d)`
(`0x0572`, `0x003410A0` → `0x003B8170`) does the same with a count of 1, the first follower only.

`0x00505240` works from the origin `(0, 0, 0)` on each actor, or its capturer. For an actor at the
origin its reach point is the larger of the two floats `0x00265090` reads, its height (`0x00263940`,
body `+0xC0` × `+0x24`) and 0.

For any other actor `0x003CC130` measures its heading around the
origin, its elevation and its distance, and `0x003CC2F0(origin, 0, elevation, distance)` rebuilds a
point from them (at `0x00505393` its first angle argument is 0). The heading is dropped, so the point
keeps the actor's distance and elevation but not its direction; the larger float and the height
are then added to its x and y.

The reach is that point's distance from the origin (`0x003CC130`). When the largest reach exceeds
`d`, every actor's position and its body `+0x20` floats are multiplied by `s = d / reach` (`0x00505431`), which
applies when that largest reach is non-zero and `s < 1.0` (`0x00505415`-`0x00505439`): each value becomes `v * s`
(`0x00505456`-`0x00505466`, `0x0050549C`-`0x005054A4`; `0x0026B0C0`, `0x00265240`, `0x0026B720`), which draws the group in
around the origin.

`0x003CC2F0(origin, a, b, distance, out)` is a shared helper, also used by the camera code: it
builds a rotation from two angles (`0x003CC480`), rotates `(0, 0, distance)` by it and adds the
origin. Its body has one path, with no branch.

It calls `0x003CC480(b, a, 0, matrix)` (`0x003CC32D`), which fills a 4×4 matrix on the stack from
`sinf` and `cosf` of the three angles. The matrix's translation row is `(0, 0, 0, 1)` (`0x003CC505`
to `0x003CC51A`) and its third row is `(sin a × cos b, −sin b, cos a × cos b, 0)` (`0x003CC53B`,
`0x003CC5A1`, `0x003CC5BC`, `0x003CC534`), so the third angle, given 0, does not reach the result.

The body sets the vector `(0, 0, distance, 1.0)` on the stack (`0x003CC344` to `0x003CC355`) and
`0x00202B70` multiplies it by the matrix in place, the row vector `v = v × M` (`0x003CC35E`; `0x00217060`), so its
first three floats are `distance` times that third row. It then writes three floats to `out`: x is origin x +
distance × sin a × cos b (`0x003CC373`), y is origin y − distance × sin b (`0x003CC382`) and z is origin z +
distance × cos a × cos b (`0x003CC38C`); `out + 0xC` is not written. With `a` given 0 at `0x00505393`,
the point is origin + `(0, −distance × sin b, distance × cos b)`.

Neither pointer is checked: an `origin` below `0x10000` (null included) faults at its first read
(`0x003CC369`), and such an `out` faults at its first write (`0x003CC373`). The body ends with the
stack-cookie check `0x00808C40` (`0x003CC399`), which on a mismatch jumps to the failure report at
`0x00809654`.

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
them and on success the verb returns 1 and cancels the member's battle action (`0x0035AE10`).

The verb writes its result through `0x0026B4E0`:

- When the party-focus handle (`0x022C7FE0`, read by `0x003590D0`) is 0 or resolves to null
  (`0x00264092`, `0x00352FE0`), the slot keeps its out-of-range value. `0x00264050` points `0x02099D70` at
  the slot array `0x02098E10` for the lookup and restores it (`0x0026406B`, `0x0026409B`, `0x002640AA`).
- `0x00263750` returns null for any slot outside 0 to 3 (an unsigned compare, so a `+0x12` byte of
  `0xFF` also gives null); the verb then returns 0 without a bind (`0x00352FF3`, `0x0035302D`).
- A refused bind returns 0 (`0x00353005`); the 1 and the cancel follow only a successful bind
  (`0x0035300C`, then the tail jump to `0x0035AE10(pc, 1)` at `0x00353028`).

`0x00262F90(owner, pc)` binds only when the member is non-null (`0x00262FA0`), the member's manager is
active, neither record is already bound (`+0x18` is 0) and the two differ; otherwise it returns 0.
It reads the owner's `+0x18` without a null test (`0x00262FD0`), so a null owner faults there. On a
bind the member gets `+0x18` = 1 with the owner's manager at `+0x19` and id at `+0x1A`, the owner
gets `+0x18` = 2 with the member's; `0x002E4A40(owner)` re-applies the render scale; the owner copies
the member's body pointers (`+0xC0` and `+0xB8`); `0x002681E0` refreshes both; it returns 1.

`0x002681E0(actor)` acts only when the actor's presentation record (`+0xC0`) is non-null and the actor is class 3
(`0x002681F3`-`0x00268201`); it reads `+0xC0` without testing the actor (`0x002681E9`), so a null actor faults there.

It writes a value to word `+0x80` of the presentation record's `+0x138` record and to the presentation record's byte
`+0x153`, only when that `+0x138` record is set (`0x00268294`-`0x002682B5`). The value comes from the presentation
record's byte `+0x152`: 3 for 2, 5 for 3 and 2 for any other non-zero value (`0x00268215`-`0x00268226`).

For a byte `+0x152` of 0 the value is 1 when the handle (`0x003589B0`) of the actor, or of the member it holds when it
is a capturer and that member resolves (`0x00263F10`), is not the party-focus handle `0x003590D0` returns
(`0x0026823B`-`0x00268254`, `0x0026828A`). When it is, the value is 1 when bit `0x10` of the actor's byte `+0xC` is set and
`0x00265680()` is non-zero and 0 otherwise, then 1 when `0x002672B0()` is 0, and then 5 when `0x0037C860()` is non-zero
(`0x00268256`-`0x00268283`).

`0x002ECCF0(owner, v)` then clears presentation `+0x11` bit `0x80` and sets it again from bit `0x1`
of `v` (`0x002ECD06`-`0x002ECD0D`), so `(owner, 1)` sets it: `0x00262F50` calls it only after a
bind that returned 1 (`0x00262F66`), and `0x002ECCF0` writes only when the owner and its `+0xC0` record
are non-null and the record's first dword is not -1 (`0x002ECCF3`-`0x002ECD04`). `0x00262F50` returns the
bind's result.

`capturepc_not_cancelbattlecommand` (`0x0582`) and the by-id form `capturepcbyentryid`
(`0x02A2`, `0x0034C3D0`, which resolves a handle through `0x003588B0`) skip or keep the cancel.
`0x0034C3D0` pops the handle (`0x00267E10`), returns at once when it resolves to null (`0x0034C3F2`) and
after a successful `0x00262F50` bind cancels the member's battle action (`0x0035AE10(pc, 1)`,
`0x0034C40B`); it calls neither the town test nor `0x0026B4E0`, so it writes no verb result.

`captureactor` (`0x0366`, `0x00354E10`) captures by name. It reads the issuer's own entry name
(`0x00263A30(manager, ordinal)`: payload plus its `+0x4C` dword plus the first int of the entry's
`+0x40` record,
`"NOACTOR"` when there is no entry) and has `0x00358800(0, name)` search manager 0's ordinal window for
an entry with the same name (a byte-for-byte compare, `0x00358850`-`0x00358861`), returning the first
match's actor from the table at manager `+8`. It returns null when no entry matches (`0x0035886D`),
or when that table is null or the ordinal is not below its count (`0x0035888A`-`0x0035889B`).

When one is found and it is not the issuer, `0x00262F50(issuer, found)` binds them, so a scene's
actor takes over the zone actor of the same name. The bind is also gated on `0x0053DD10(name)`, which
is `mov eax, 1; ret` and always passes. `captureactor_367(name)` (`0x0367`, `0x00355570`) takes the name as a
string operand resolved through `0x002650B0`.

`releasepc` (`0x0058`, a jump into `0x002693D0(owner, 1)`; `releasepc_404` passes a popped flag)
undoes it. `0x002693D0(record, flag)` acts on the record's bind state `+0x18` (`0x002693DF`-`0x002693EF`):

- For a capturer (2) whose partner's manager is active (`+0x10` bit `0x1`, `0x0026940F`), `0x002693D0`
  resolves the member (`0x00358940`, not null-tested, so a null member faults in `0x0026AE90` at
  `0x0026AE96`) and sets its steering mode to 0 (`0x0026AE90`, `0x0026942B`).
- For a class-3 member it then clears its steering byte, `+0x28` of `[[member + 0xB8] + 0xF0]`
  (`0x00269453`), runs `0x002EBE50(member, 0, 0)` and `0x002E8EE0(member)` when that request's `+0x65` is
  non-zero (`0x00269462`), and hands the old byte to `0x002E6300` (`0x00269489`).
- It re-applies the owner's render value (`0x002E9560`, `0x002E4F40`), rebuilds the member's four body
  pointers with `0x00266AD0` from its sequence (`+0x03` bits `0x1F`) rather than restoring a saved
  copy, resets its locomotion (steering and movement modes 0, `0x0026AE90`, `0x0026C120`), refreshes the
  owner's lane index (`0x002EAC90`), and with the flag runs `0x002EB430` (the idle motion) on the owner
  (`0x002694D1`).
- It re-applies the owner's render scale (`0x002E4A40`), refreshes the member (`0x002681E0`) and
  releases the member by calling itself on it (`0x002694EB`), which takes the captured path below;
  then the owner gets the same reset, so both records get `+0x18` = `0xFFFF0000` and a refresh.
- For a captured record (1), or a capturer whose partner's manager is inactive, `0x00266AD0` rebuilds
  the record's own four body pointers, `+0x18` becomes `0xFFFF0000`, `0x002681E0` refreshes it and
  the render value is re-applied (`0x002694F5`-`0x0026951A`). Called on a captured member directly,
  this leaves its capturer at `+0x18` = 2.
- Any other `+0x18` value returns at once (`0x002693EF`).

`releasepc_battlemember` (`0x057D`, a jump into `0x00269530`) releases every roster member a scene
actor holds: for each of the four roster actors whose `+0x18` is 1 it resolves the owner from
`+0x19` and `+0x1A` (`0x003587C0`) and, when that is another record, runs `0x002693D0(owner, 1)`. It
reads `+0x18` of each roster pointer without testing it for null (`0x00269556`).

### Event party modes

`seteventpartymode(v)` (`0x050F`, `0x00351B40` → `0x0037D120` → `0x00307240`) writes bit `0x4` of the party block word
`[0x02EBF190] + 0x5B04` and `seteventparty2mode` (`0x0514`) bit `0x8`; `geteventpartymode` (`0x0510`,
`0x00355FE0`) returns whether the mode ladder `0x0030D9A0` reads 4, and `geteventpartymodebit`
(`0x0513`) returns bit `0x4`.

## Layouts

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

## Shipped data

| Fact | Value |
|---|---|
| `capturepc` uses in the US scripts | 8,353; `releasepc` 8,632 |
| `hideparty` uses | 1,539 |

## Operations

Per capture: one binding write on each record and one action cancel.

## State

The capture bindings in every actor record, the summon leader and follower globals, and the party block mode
word.

## Modding notes

- `capturepc(−1)` always takes the character the player controls; a script that needs a specific
  member passes its slot.
- `hideparty` hides bodies only; the actors keep running and can still be captured.
- `releasepc` rebuilds the body pointers from the record's sequence (`+0x03` bits `0x1F`, read by
  `0x00266AD0` at `0x00266AD3`), so a capturer that swapped them is not restored to a saved state but to
  that sequence's default (`0x002694F8`).

## Related

- [Event scenes](event-scenes.md): loading, playing and disposing a scene, movies and skips.
- [The world lock](world-lock.md): what holds everyone else still during a talk or scene.
- [Party verbs](party-verbs.md): the summon party switches.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 597 calls with 75 other topics</summary>

**Characters and objects** (explained on [actor record](../Characters-And-Objects/actor-record.md))

| Function | | Functions |
|---|---|---|
| `0x0026B500` | is called by | `0x003B6CC0`, `0x003B6D60` |
| `0x002E8FD0` | is called by | `0x00265B60`, `0x002E35B0` |
| `0x003B6F30` | calls | `0x003B6D60` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00263750` | is called by | `0x003266C0`, `0x0035A8D0` |
| `0x00263940` | is called by | `0x00271380`, `0x002718E0` |
| `0x00263A30` | calls | `0x00358940` |
| `0x00263BE0` | is called by | `0x0035A7A0`, `0x0035A990`, `0x0046BAC0` |
| `0x00263CC0` | is called by | `0x00236300`, `0x003B73B0`, `0x003B7440`, `0x003B7510` |
| `0x00263F40` | calls | `0x003587C0` |
| `0x00264050` | calls | `0x003588B0`, `0x00358940` |
| `0x00264670` | is called by | `0x00236300` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x002647B0` | is called by | `0x0035A7A0`, `0x0035A990`, `0x0046BAC0` |
| `0x002647C0` | is called by | `0x0037B4D0` |
| `0x00265020` | is called by | `0x00236300`, `0x0037B4D0`, `0x003B73B0`, `0x003B7440`, `0x003B7510` |
| `0x00265090` | is called by | `0x00236300` |
| `0x00265200` | is called by | `0x00236300`, `0x003B73B0`, `0x003B7440`, `0x003B7510` |
| `0x00265240` | is called by | `0x003B73B0`, `0x003B7440`, `0x003B7510` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00266AD0` | is called by | `0x00266530`, `0x002693D0` |
| `0x002681E0` | calls | `0x003589B0` |
| `0x002681E0` | is called by | `0x00266530`, `0x002693D0` |
| `0x002693D0` | calls | `0x00266AD0`, `0x002693D0`, `0x00358940` |
| `0x002693D0` | is called by | `0x0025B070`, `0x002693D0`, `0x0026C5D0` |
| `0x00269530` | calls | `0x002693D0`, `0x003587C0` |
| `0x0026A0D0` | is called by | `0x0037B4D0` |
| `0x0026AE90` | is called by | `0x002693D0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x0026B620` | is called by | `0x0037B4D0` |
| `0x0026C120` | is called by | `0x002693D0` |
| `0x0026D6D0` | is called by | `0x0035A590`, `0x0035A720`, `0x0035A7A0`, `0x0035A8D0`, `0x003B6F80` |
| `0x002E4A40` | is called by | `0x002693D0`, `0x0037B4D0` |
| `0x002E4F40` | is called by | `0x002693D0` |
| `0x002E6300` | is called by | `0x002693D0` |
| `0x002E7600` | is called by | `0x00263050`, `0x00263230`, `0x0026C5D0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x002E8EE0` | is called by | `0x00263050`, `0x00263230`, `0x002693D0`, `0x0026C5D0` |
| `0x002E8FD0` | is called by | `0x002EBB80` |
| `0x002E9560` | is called by | `0x002693D0` |
| `0x002E97B0` | is called by | `0x0035A720`, `0x0035A7A0`, `0x0035A8D0`, `0x0037B4D0` |
| `0x002E9BE0` | is called by | `0x003B73B0`, `0x003B7440`, `0x003B7510` |
| `0x002EAC90` | is called by | `0x002693D0`, `0x0037B4D0` |
| `0x002EB030` | is called by | `0x0037B4D0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x002EB430` | is called by | `0x002693D0`, `0x0026C5D0` |
| `0x002EBE50` | is called by | `0x00263050`, `0x00263230`, `0x002693D0`, `0x0026C5D0` |
| `0x0030D9A0` | is called by | `0x00300FC0`, `0x003266C0` |
| `0x00341CB0` | calls | `0x003588B0` |
| `0x00346FA0` | calls | `0x003588B0`, `0x00358940`, `0x003B6F80` |
| `0x00348DA0` | calls | `0x00263FF0` |
| `0x0034C3D0` | calls | `0x003588B0`, `0x0035AE10` |
| `0x00352FA0` | calls | `0x00264050`, `0x0035AE10` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00354E10` | calls | `0x00263A30` |
| `0x003587C0` | calls | `0x00263FF0` |
| `0x003587C0` | is called by | `0x0025AE00`, `0x00268650`, `0x0026C5D0`, `0x0026CE60`, `0x003DBDC0`, `0x003DC0D0` |
| `0x00358800` | calls | `0x00263A30`, `0x00263FF0` |
| `0x00358940` | is called by | `0x0025AE00`, `0x0025B070`, `0x0025B250`, `0x0025B820`, `0x0025C070`, `0x0025C170`, `0x0025D9E0`, `0x00263A30`, `0x00264010`, `0x00264050`, `0x00265A20`, `0x00266C50` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x00358940` | is also called by | `0x00268B10`, `0x00268D10`, `0x002693D0`, `0x00269800`, `0x00269AD0`, `0x00269BA0`, `0x0026B8E0`, `0x0026CE60`, `0x0026D3E0`, `0x0035A590`, `0x0035A7A0`, `0x0035A990` |
| `0x00358940` | is also called by | `0x003B6F80`, `0x003DB1F0`, `0x0046BAC0` |
| `0x003589B0` | is called by | `0x00234480`, `0x0025C230`, `0x0025C830`, `0x00268650`, `0x00268D10`, `0x0037B4D0`, `0x003B6F80` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x003590D0` | is called by | `0x0025B600`, `0x0025D9E0`, `0x00263050`, `0x00263230`, `0x00263AC0`, `0x00264010`, `0x00264050`, `0x0026C5D0`, `0x0026C8C0`, `0x0026DFB0` |
| `0x00359B80` | is called by | `0x00265A20`, `0x003B73B0`, `0x003B7440`, `0x003B7510` |
| `0x0035AA50` | calls | `0x00263FF0`, `0x00358940` |
| `0x0035AE10` | calls | `0x00233F50` |
| `0x0035AE10` | is called by | `0x00263230`, `0x0026C5D0` |
| `0x00377C20` | is called by | `0x0025C830`, `0x003266C0` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x003B6D60` | calls | `0x003588B0` |
| `0x003B6DE0` | calls | `0x003588B0` |
| `0x003B6DE0` | is called by | `0x003B6F80` |
| `0x003B6F30` | calls | `0x003B6DE0`, `0x003B7510` |
| `0x003B6F80` | calls | `0x00263FF0`, `0x00358940`, `0x003589B0`, `0x003B6DE0` |
| `0x003B7180` | calls | `0x003589B0` |
| `0x003B72F0` | calls | `0x00358940` |
| `0x003B73B0` | calls | `0x00265020`, `0x00359B80` |
| `0x003B73B0` | is called by | `0x003B7440` |

**Characters and objects**

| Function | | Functions |
|---|---|---|
| `0x003B7440` | calls | `0x00265020`, `0x00359B80`, `0x003B73B0` |
| `0x003B7510` | calls | `0x00265020`, `0x00359B80` |
| `0x003B7770` | calls | `0x00263FF0`, `0x003588B0`, `0x00358940` |
| `0x003B7A30` | calls | `0x002693D0` |
| `0x003B7AB0` | calls | `0x002693D0` |
| `0x003B7B00` | calls | `0x00359B80` |
| `0x003B7D80` | calls | `0x00359B80` |
| `0x003B7E20` | calls | `0x00265020`, `0x003588B0` |
| `0x003B7F40` | calls | `0x00265020` |
| `0x00505240` | calls | `0x00265020`, `0x00265090` |

**Characters and objects** (explained on [party control modes](../Engine-Core/party-control-modes.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [hud](../Menus-And-HUD/hud.md), [frame update order](../Engine-Core/frame-update-order.md), [battle verbs](battle-verbs.md))

**Characters and objects** (explained on [target selection](../Battle-Actions/target-selection.md), [script name bindings](script-name-bindings.md), [script requests](script-requests.md), [identifier spaces](../Engine-Core/identifier-spaces.md), [actor record fields](../Characters-And-Objects/actor-record-fields.md))

**Characters and objects** (explained on [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md), [reward verbs](reward-verbs.md), [debug menu](../Engine-Core/debug-menu.md), [party verbs](party-verbs.md), [field runtime](../Characters-And-Objects/field-runtime.md), [event scenes](event-scenes.md))

**Characters and objects** (explained on [battle units](../Characters-And-Objects/battle-units.md), [actor managers](../Characters-And-Objects/actor-managers.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md))

**Sound and music** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x00362850` |
| `0x003590D0` | is called by | `0x00362850` |

**Enemy AI and gambits**

| Function | | Functions |
|---|---|---|
| `0x00263940` | is called by | `0x0032A4D0` |
| `0x00265090` | is called by | `0x0030F130` |
| `0x00377C20` | is called by | `0x003014C0`, `0x00301AD0`, `0x00305AB0` |

**Enemy AI and gambits** (explained on [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [enemy ai](../Enemy-AI-And-Gambits/enemy-ai.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [glossary](../Engine-Core/glossary.md), [battle verbs](battle-verbs.md))

**Battle actions**

| Function | | Functions |
|---|---|---|
| `0x0017F5B0` | is called by | `0x003065D0` |
| `0x00263F40` | is called by | `0x00307300` |
| `0x00265020` | is called by | `0x002F8060`, `0x00307300`, `0x00320E10` |
| `0x00265090` | is called by | `0x002FDC30`, `0x002FEB80` |
| `0x00265200` | is called by | `0x00307300` |
| `0x0026A0D0` | is called by | `0x00307300` |
| `0x0026B0C0` | is called by | `0x00307300` |
| `0x0026B620` | is called by | `0x00307300` |
| `0x0030D9A0` | is called by | `0x002FFCF0`, `0x00313DB0` |

**Battle actions**

| Function | | Functions |
|---|---|---|
| `0x003589B0` | is called by | `0x00319F50`, `0x00325260` |
| `0x003590D0` | is called by | `0x00317E60`, `0x00319090` |
| `0x00377C20` | is called by | `0x002FFA60`, `0x002FFCF0`, `0x002FFF50`, `0x00305110`, `0x00305230`, `0x00305430`, `0x00307300`, `0x0030C010`, `0x0030D160`, `0x0030D600`, `0x0030DA30`, `0x0030F760` |
| `0x00377C20` | is also called by | `0x00311B20`, `0x00311CF0`, `0x00312FA0`, `0x00313CD0`, `0x00313DB0` |

**Battle actions** (explained on [frame update order](../Engine-Core/frame-update-order.md), [battle unit fields](../Characters-And-Objects/battle-unit-fields.md), [traps](../World-Areas-And-Travel/traps.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md))

**Battle actions** (explained on [battle orders](../Battle-Actions/battle-orders.md), [action phases](../Battle-Actions/action-phases.md), [force fight mode](../Engine-Core/force-fight-mode.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md), [reward verbs](reward-verbs.md))

**Battle actions** (explained on [jump thunks](../Engine-Core/jump-thunks.md), [quickenings and summons](../Battle-Actions/quickenings-and-summons.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [action definition row](../Battle-Actions/action-definition-row.md))

**Battle actions** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md), [call signatures](../Engine-Core/call-signatures.md), [battle verbs](battle-verbs.md))

**Damage and battle formulas** (explained on [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md))

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x00384F40` |
| `0x00377C20` | is called by | `0x00300530` |

**Engine core** (explained on [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x0053DD10` | is called by | `0x0022B6E0` |

**Gameplay**

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x0031ADB0`, `0x00339630` |
| `0x002EB030` | is called by | `0x003299B0` |
| `0x0030D9A0` | is called by | `0x00309A90` |
| `0x003589B0` | is called by | `0x0031ADB0` |
| `0x003590D0` | is called by | `0x0031ADB0` |
| `0x00377C20` | is called by | `0x00307D10`, `0x0030A8A0`, `0x0030C210`, `0x0030D9A0` |

**Gameplay** (explained on [bestiary](../Enemy-Spawning/bestiary.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [force fight mode](../Engine-Core/force-fight-mode.md))

**Gameplay** (explained on [enmity](../Enemy-AI-And-Gambits/enmity.md), [frame update order](../Engine-Core/frame-update-order.md))

**Controls and input**

| Function | | Functions |
|---|---|---|
| `0x00263750` | is called by | `0x00226BE0` |
| `0x00263BE0` | is called by | `0x00226BE0` |
| `0x002647B0` | is called by | `0x00226BE0` |
| `0x00358940` | is called by | `0x00226BE0` |
| `0x003590D0` | is called by | `0x00226BE0` |
| `0x00359B80` | is called by | `0x00226BE0` |
| `0x00377C20` | is called by | `0x00253C70` |
| `0x0053DD10` | is called by | `0x002E09A0`, `0x0035FCA0`, `0x0035FDD0`, `0x0046DD50` |

**Controls and input** (explained on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md), [force fight mode](../Engine-Core/force-fight-mode.md), [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md))

**Controls and input** (explained on [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md))

**Input gameplay** (explained on [force fight mode](../Engine-Core/force-fight-mode.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00313A00` |

**Items, equipment, shops and licenses** (explained on [reward verbs](reward-verbs.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x00309FB0`, `0x0030FD10` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0017F5B0` | is called by | `0x003B7E20` |
| `0x0025A5F0` | is called by | `0x003B7E20` |
| `0x00262F90` | calls | `0x002E4A40` |
| `0x00263750` | is called by | `0x0034A940`, `0x0037CF00`, `0x0037D000` |
| `0x00263940` | is called by | `0x00334C90`, `0x003357B0`, `0x0033D660`, `0x00505240` |
| `0x00263CC0` | is called by | `0x002E5750` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00263F40` | is called by | `0x00300310`, `0x003003F0`, `0x00310920`, `0x00311F70`, `0x0033FFC0`, `0x00345430`, `0x00349680`, `0x0037D000`, `0x003B7B00`, `0x003B7D80`, `0x003B7F40`, `0x00505240` |
| `0x002644C0` | is called by | `0x003B7F40` |
| `0x00264670` | is called by | `0x003B7F40` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x0024B6F0`, `0x002E45E0`, `0x002EBFA0`, `0x002EC2C0`, `0x00300310`, `0x00310920`, `0x00311E20`, `0x00311F70`, `0x00326BB0`, `0x00336710`, `0x00337C10`, `0x00337D90` |
| `0x00265020` | is also called by | `0x0033CA00`, `0x003B7E20`, `0x003B7F40`, `0x00505240` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00265090` | is called by | `0x002FB340`, `0x002FB500`, `0x00309B10`, `0x0030A130`, `0x00312730`, `0x00334790`, `0x00334A70`, `0x00336210`, `0x00336710`, `0x00336E40`, `0x00337700`, `0x003377C0` |
| `0x00265090` | is also called by | `0x00338490`, `0x00339A60`, `0x00339BF0`, `0x0033A720`, `0x0033D660`, `0x00392170`, `0x00392740`, `0x00505240` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00265200` | is called by | `0x0024B6F0`, `0x002E5750`, `0x002EBE50`, `0x002FB500`, `0x00326BB0`, `0x003343D0`, `0x00336E40`, `0x00338490`, `0x0033CA00` |
| `0x00265240` | is called by | `0x00505240` |
| `0x002681E0` | is called by | `0x0025DF00`, `0x0026A7F0` |
| `0x002693D0` | calls | `0x0026AE90`, `0x0026C120`, `0x002E4A40`, `0x002E6300`, `0x002EBE50` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0026A0D0` | is called by | `0x00239210`, `0x0023A070`, `0x003003F0`, `0x00310920`, `0x00310D30`, `0x00311F70`, `0x0034A940`, `0x003538C0`, `0x0037D000`, `0x003B7B00` |
| `0x0026ACE0` | is called by | `0x003B7B00`, `0x003B7F40` |
| `0x0026AE90` | calls | `0x002E55C0` |
| `0x0026AE90` | is called by | `0x002EAB80`, `0x00343E20`, `0x00344290`, `0x0034EBC0`, `0x0034F210`, `0x00350510`, `0x00350C30`, `0x00357980`, `0x00357A20`, `0x0037D000` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0026B0C0` | calls | `0x002E4A10`, `0x002E5C70` |
| `0x0026B0C0` | is called by | `0x0026B170`, `0x0026B230`, `0x0026BA70`, `0x00300310`, `0x00310920`, `0x00310D30`, `0x00311F70`, `0x0034EBC0`, `0x0034F210`, `0x00350510`, `0x00350C30`, `0x0037D000` |
| `0x0026B0C0` | is also called by | `0x003B7B00`, `0x003B7F40`, `0x00505240` |
| `0x0026B620` | calls | `0x0026B6A0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0026B620` | is called by | `0x00239210`, `0x0026C120`, `0x003003F0`, `0x00310920`, `0x00310D30`, `0x00311F70`, `0x0034A940`, `0x00350510`, `0x00350C30`, `0x0037D000`, `0x003B7B00` |
| `0x0026B720` | is called by | `0x003B7B00`, `0x003B7D80`, `0x00505240` |
| `0x0026C120` | calls | `0x0026B620`, `0x002E6300`, `0x002EBE50` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x0026C120` | is called by | `0x002E45E0`, `0x002E55C0`, `0x002E5750`, `0x002EAB80`, `0x0033FFC0`, `0x00345430`, `0x003488B0`, `0x00349680`, `0x003567D0` |
| `0x0026D6D0` | calls | `0x0026D6F0` |
| `0x002E4A40` | calls | `0x002ED6A0` |
| `0x002E4A40` | is called by | `0x002E5180`, `0x0037CF00`, `0x003B7B00`, `0x003B7F40` |
| `0x002E6300` | is called by | `0x0026C120` |
| `0x002E7600` | is called by | `0x002690D0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x002E8EE0` | is called by | `0x0026C120`, `0x002E28E0`, `0x002E3110`, `0x002E64E0`, `0x002EAAA0`, `0x002EBE50` |
| `0x002E8FD0` | is called by | `0x002E28E0`, `0x002E3110` |
| `0x002E97B0` | is called by | `0x0025DF00`, `0x0026A490` |
| `0x002EB030` | is called by | `0x003B7E20` |
| `0x002EB430` | is called by | `0x0026C3E0`, `0x0033FFC0`, `0x00345430`, `0x00349680` |
| `0x002EBE50` | calls | `0x00265200`, `0x002EC3F0` |
| `0x002EBE50` | is called by | `0x002690D0`, `0x0026C120` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x002EC680` | is called by | `0x003B7B00`, `0x003B7F40` |
| `0x002ECE50` | is called by | `0x003B7F40` |
| `0x0030D9A0` | is called by | `0x00309AE0`, `0x00311F70` |
| `0x00340DA0` | calls | `0x003B8140` |
| `0x003410A0` | calls | `0x003B8170` |
| `0x003587C0` | is called by | `0x002E45E0`, `0x002EBFA0`, `0x00377560` |
| `0x00358940` | is called by | `0x00392740` |
| `0x003589B0` | is called by | `0x002E5610`, `0x002EBFA0` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x003590D0` | is called by | `0x0026C3E0`, `0x0026D6F0`, `0x0026D810`, `0x002E45E0`, `0x002E5180`, `0x00319490`, `0x00325D90`, `0x00326BB0`, `0x00326D60`, `0x00343E20`, `0x00345430` |
| `0x00359B80` | is called by | `0x0025DF00`, `0x003B7B00`, `0x003B7D80` |
| `0x0035AE10` | is called by | `0x0026C3E0` |
| `0x0036D840` | is called by | `0x003B7E20` |
| `0x00377C20` | is called by | `0x0025B470`, `0x0026C3E0`, `0x002E28E0`, `0x00310920`, `0x00313670` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x003B6F80` | calls | `0x0026D6D0` |
| `0x003B73B0` | calls | `0x00263CC0`, `0x00265200`, `0x00265240` |
| `0x003B7440` | calls | `0x00263CC0`, `0x00265200`, `0x00265240` |
| `0x003B7510` | calls | `0x00263CC0`, `0x00265200`, `0x00265240` |
| `0x003B7B00` | calls | `0x0026A0D0`, `0x0026ACE0`, `0x0026B0C0`, `0x0026B620`, `0x0026B720`, `0x002E4A40` |
| `0x003B7BB0` | calls | `0x003B7B00` |
| `0x003B7C60` | calls | `0x003B7B00` |
| `0x003B7D80` | calls | `0x0026B720` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x003B7D80` | is called by | `0x003B8140`, `0x003B8170` |
| `0x003B7E20` | calls | `0x003B7F40` |
| `0x003B7F40` | calls | `0x002644C0`, `0x00264670`, `0x0026ACE0`, `0x0026B0C0`, `0x002E4A40` |
| `0x003B7F40` | is called by | `0x003B7E20` |
| `0x003B8030` | calls | `0x0026B620` |
| `0x003B8140` | calls | `0x003B7D80`, `0x00505240` |
| `0x003B8170` | calls | `0x003B7D80`, `0x00505240` |
| `0x003CC130` | is called by | `0x00505240` |
| `0x003CC2F0` | is called by | `0x00505240` |

**Movement and pathfinding**

| Function | | Functions |
|---|---|---|
| `0x00505240` | calls | `0x00263940`, `0x00265240`, `0x0026B0C0`, `0x0026B720` |
| `0x00505240` | is called by | `0x003B8140`, `0x003B8170` |

**Movement and pathfinding** (explained on [subsystem update flags](../Engine-Core/subsystem-update-flags.md), [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [frame update order](../Engine-Core/frame-update-order.md), [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md))

**Movement and pathfinding** (explained on [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md), [bestiary](../Enemy-Spawning/bestiary.md), [battle unit construction](../Characters-And-Objects/battle-unit-construction.md), [time stop and freeze](../Engine-Core/time-stop-and-freeze.md))

**Movement and pathfinding** (explained on [battle units](../Characters-And-Objects/battle-units.md), [spawn record fields](../Enemy-Spawning/spawn-record-fields.md), [navigation mesh and pathfinding](../Movement-And-Pathfinding/navigation-mesh-and-pathfinding.md), [enemy spawning](../Enemy-Spawning/enemy-spawning.md))

**Movement and pathfinding** (explained on [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md), [heading speed to position delta](../Movement-And-Pathfinding/heading-speed-to-position-delta.md), [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md))

**Movement and pathfinding** (explained on [world lock](world-lock.md), [party control modes](../Engine-Core/party-control-modes.md), [party data](../Party/party-data.md), [force fight mode](../Engine-Core/force-fight-mode.md), [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md))

**Movement and pathfinding** (explained on [target selection](../Battle-Actions/target-selection.md), [party leader](../Party/party-leader.md), [actor record fields](../Characters-And-Objects/actor-record-fields.md), [ebp position entries](../EBP-Script-Files/ebp-position-entries.md))

**Movement and pathfinding** (explained on [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [animation driven movement](../Movement-And-Pathfinding/animation-driven-movement.md), [native commands](native-commands.md), [script binding lifecycle](script-binding-lifecycle.md))

**Movement and pathfinding** (explained on [script requests](script-requests.md), [verb table](verb-table.md), [player movement](../Movement-And-Pathfinding/player-movement.md), [party slots](../Party/party-slots.md), [script name bindings](script-name-bindings.md))

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x00263940` | is called by | `0x003223C0` |
| `0x00263F40` | is called by | `0x003B70B0` |
| `0x00264670` | is called by | `0x003A4290`, `0x003A56F0`, `0x003B62D0` |
| `0x00265020` | is called by | `0x002B7B80`, `0x00322360`, `0x0037AD40`, `0x003A40F0`, `0x003A56F0`, `0x003C29A0`, `0x003C37B0` |
| `0x00265090` | is called by | `0x003223C0` |
| `0x00265200` | is called by | `0x003C29A0` |
| `0x002E8FD0` | calls | `0x003E6A60`, `0x00428DE0`, `0x00428E10`, `0x00429020` |

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x002E8FD0` | is called by | `0x003B70B0` |
| `0x002E97B0` | is called by | `0x003B70B0` |
| `0x002ECD50` | calls | `0x002E8FD0` |
| `0x002ECE50` | calls | `0x003E6150` |
| `0x0030D9A0` | is called by | `0x003125E0` |
| `0x003587C0` | is called by | `0x00256F60` |
| `0x00358940` | is called by | `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690` |
| `0x003589B0` | is called by | `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690`, `0x00506700` |

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x003590D0` | is called by | `0x003A4290`, `0x003A56F0`, `0x003F1A60`, `0x00426090`, `0x004264A0`, `0x004640A0`, `0x004643D0`, `0x00464650`, `0x00464BD0`, `0x00465120`, `0x00465690`, `0x0046CC70` |
| `0x00377C20` | is called by | `0x00307E70`, `0x003125E0`, `0x00313B30`, `0x003714A0` |
| `0x003B70B0` | calls | `0x002E8FD0` |
| `0x003B7770` | calls | `0x002E8FD0` |
| `0x003CC130` | is called by | `0x00256960`, `0x0032B1C0`, `0x0032BEB0`, `0x0032CA70` |

**Graphics**

| Function | | Functions |
|---|---|---|
| `0x003CC480` | is called by | `0x00256960`, `0x00256CA0`, `0x0032CA70` |
| `0x0053DD10` | is called by | `0x004355D0`, `0x00462540` |

**Graphics** (explained on [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md), [frame update order](../Engine-Core/frame-update-order.md), [battle locomotion](../Movement-And-Pathfinding/battle-locomotion.md))

**Graphics** (explained on [weather](../World-Areas-And-Travel/weather.md), [bestiary](../Enemy-Spawning/bestiary.md), [map screens](../Menus-And-HUD/map-screens.md), [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md), [character render records](../Graphics/character-render-records.md))

**Graphics** (explained on [party verbs](party-verbs.md), [script name bindings](script-name-bindings.md), [battle units](../Characters-And-Objects/battle-units.md), [effect element runtime](../Graphics/effect-element-runtime.md), [effect element types](../Graphics/effect-element-types.md))

**Graphics** (explained on [battle numbers](../Menus-And-HUD/battle-numbers.md), [hud](../Menus-And-HUD/hud.md), [authored presentation commands](../Graphics/authored-presentation-commands.md), [legacy ps2 gs layer](../Graphics/legacy-ps2-gs-layer.md))

**Graphics** (explained on [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md), [force fight mode](../Engine-Core/force-fight-mode.md), [battle verbs](battle-verbs.md), [add motion tables](../Graphics/add-motion-tables.md))

**Graphics** (explained on [scripted camera](../Graphics/scripted-camera.md), [field camera](../Graphics/field-camera.md), [collision mesh movement](../Movement-And-Pathfinding/collision-mesh-movement.md))

**Rewards: EXP, LP, gil and loot** (explained on [loot drops](../Rewards-EXP-Gil-And-Loot/loot-drops.md), [area flags navimapdata](../World-Areas-And-Travel/area-flags-navimapdata.md))

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x002FB150`, `0x00312280` |
| `0x00265090` | is called by | `0x002FB150` |
| `0x00377C20` | is called by | `0x00312280` |

**Enemy spawning** (explained on [enemy spawning](../Enemy-Spawning/enemy-spawning.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x00234AF0`, `0x00234DA0`, `0x002350C0` |
| `0x00265200` | is called by | `0x00234AF0` |

**Status effects and KO** (explained on [force fight mode](../Engine-Core/force-fight-mode.md), [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00377C20` | is called by | `0x0030E360`, `0x0030F690`, `0x00310DB0` |

**Menus and HUD** (explained on [battle units](../Characters-And-Objects/battle-units.md), [party list](../Menus-And-HUD/party-list.md), [map screens](../Menus-And-HUD/map-screens.md))

| Function | | Functions |
|---|---|---|
| `0x00265020` | is called by | `0x003C5130` |
| `0x00265200` | is called by | `0x003C5130` |
| `0x003590D0` | is called by | `0x00299BD0`, `0x002C7660` |
| `0x0053DD10` | is called by | `0x003C80C0` |

**World, areas and travel** (explained on [actor record fields](../Characters-And-Objects/actor-record-fields.md), [frame update order](../Engine-Core/frame-update-order.md))

| Function | | Functions |
|---|---|---|
| `0x00358940` | is called by | `0x0025E400`, `0x002623A0` |
| `0x003590D0` | is called by | `0x0025E400`, `0x002623A0` |

**World, areas and travel**

| Function | | Functions |
|---|---|---|
| `0x002E4A40` | calls | `0x00377DB0` |
| `0x0030D9A0` | calls | `0x00377C20` |
| `0x00352FA0` | calls | `0x00377C20` |
| `0x00377C20` | calls | `0x003148F0` |
| `0x00377C20` | is called by | `0x002342F0` |
| `0x0053DD10` | is called by | `0x003789A0` |

**World, areas and travel** (explained on [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md), [force fight mode](../Engine-Core/force-fight-mode.md), [party control modes](../Engine-Core/party-control-modes.md), [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md))

</details>
