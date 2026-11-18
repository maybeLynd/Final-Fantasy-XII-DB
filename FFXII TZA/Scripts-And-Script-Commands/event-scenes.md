[Home](../../README.md) / [Scripts and script commands](README.md) / Event scenes

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Event scenes: the scene managers, loading, starting, waiting on and disposing a scene, movies and skips | system | Scripts and script commands | Event scenes | How a script runs a story scene: the three scene managers and the verbs that load, release, wait on and dispose a scene, the start hold on the load mask, the two global gates every scene verb tests, pre-rendered movies, and the skip table and masks. | 0x02098E10, 0x02099DE2, 0x00264170, 0x0026A5A0, 0x001C3370, 0x00351880, 0x00351C90, 0x003522C0, 0x00353080, 0x003541B0, 0x00354B20, 0x00355970, 0x00356D40, 0x00332130, 0x00332190, 0x0032ED70, 0x0032F1B0, 0x00267210, 0x022C6E48, 0x022C6D20, 0x0034C9A0, 0x0026B750, 0x00863240, 0x003567F0, 0x00356050, 0x0035B840, 0x0035B7D0, 0x0035B8D0, 0x0035B740, 0x00357300, 0x00184860, 0x00360980, 0x00360710, 0x003604A0, 0x0034DB30, 0x022CB730, 0x02099011, 0x003B08F0, 0x00360670, 0x00360650 |

## What the player sees

A story scene: the screen fades, the party vanishes and the scene's own actors take the stage, the camera takes
over, characters talk and move on their own, and at the end control comes back. Some scenes are pre-rendered movies.
Many can be skipped from the pause menu.

Behind this, the area script asks for the scene's files to load into one of three scene slots kept apart from the
area's own actors. The files may finish early, but the scene starts only when the script's play command lifts a hold
on it, and a wait command can hold the script until the scene's slot goes idle.

## How it works

### Scene managers and the two gates

A scene runs in its own actor manager, 1, 2 or 3, beside the zone's manager 0 (`0x02098E10 +
m × 0x288`). Every scene verb takes a slot argument and uses manager `clamp(slot + 1, 1, 3)`; the
plain-named forms (`eventread`, `eventplay`, `eventsync`) fix the slot at 0, manager 1.

Two gates sit in almost every scene verb. `0x00264170` returns the event switch byte `0x02099DE2`, which area
initialisation sets to 1 and `system_seteventexecstatus` (`0x141`) writes through `0x0026A5A0`; while it is 0 the load,
play and sync verbs do nothing. `0x001C3370` returns whether byte `+0x10D4` of the application object `0x00796E20` returns
is non-zero (`0x001C3374`-`0x001C3381`), a byte written only to 0 by the constructor `0x00792350` and read otherwise by the
auto-test walker `0x001C2F50`: an auto-test switch that is never set in retail, so scene verbs always proceed past it.

### Loading, the start hold, playing and disposing

| Verb | Id | Callbacks | What it does |
|---|---|---|---|
| `eventread_e8(slot, id)` | `0x00E8` | begin `0x00351880`, poll `0x00351C90`, result `0x003522C0` | the begin stores both and calls `0x001D6A70(id, slot)`, which ends in the empty `0x0016D6A0`, so nothing is fetched (`0x001D6A95`); the poll waits while manager `m` is active (`+0x10` bit `0x1`) and busy (`+0x13`) (`0x00351CBD`, `0x00351CC3`) and tests neither gate; the result queues the load `0x0032FC30(m, id)` and sets the hold `0x0032ED70(m)`, and does nothing when the event switch is 0 (`0x003522D8`), the auto-test byte is non-zero (`0x003522E2`) or the slot is negative (`0x003522E6`) |
| `eventread(id)` | `0x00E7` | begin `0x003529E0`, poll `0x00352D70`, result `0x00353080` | the begin pops the id, pushes 0 and the id back and pops them again, storing the id at `+4` and 0 at `+0`, and calls `0x001D6A70(id, 0)` as `eventread_e8`'s begin does, so nothing is fetched (`0x003529F8`-`0x00352A3C`); the poll looks up the manager record (`0x00263FF0`), drops it and answers 0 on both of its paths, so it never waits (`0x00352D88`, `0x00352D9E`); the result: slot 0, the same gates, sign test and load (`0x003530AA`, `0x003530B3`, `0x003530B7`), after `0x00314D40(1)`, which sets byte `0x022C253D` to 1 and runs before the gates (`0x00353099`) |
| `eventreadsync_ea(slot)` | `0x00EA` | begin `0x00353A10`, poll `0x003541B0` | the begin stores `m` (`0x00353A28`, `0x00353A3E`); the poll waits while `0x0032F6C0(m)` reports loads pending other than the start hold bit `0x1` (`0x0032F6CD`) in the mask's low 32 bits (`0x0032F6CA`), so for the scene's files and not for `eventplay`, calling `0x00314D40(1)` on each poll that finds loads pending (`0x003541F6`); it stops waiting when the auto-test byte is non-zero (`0x003541C7`) or the event switch is 0 (`0x003541E4`). With no load pending it asks `0x0053DD10`, which always returns 1, so it stops (`0x0035420B`) and the branch to the stub `0x0016D6A0` (`0x00354210`) never runs; the `0x00264190(m)` call between the two gates, after the auto-test test and before the event-switch test, has its result discarded (`0x003541D8`) |
| `eventplay_ec(slot)` | `0x00EC` | result `0x00354B20` | releases the hold `0x00332130(m)`, then `0x001EC680(m)`, `0x0020AF10(m, −1)` and `0x001EC600()` |
| `eventsync_ee(slot)` | `0x00EE` | begin `0x00353A10`, poll `0x00355970` | waits while `0x00267210(m)` is non-zero: manager active or busy (`0x003559A5`); it stops waiting when the event switch is 0 (`0x00355998`), and when the auto-test byte is non-zero it stores 1 into the auto-test walker's arrival word `0x01EEBADC` (`0x00355983`) and stops waiting without testing the switch or the manager (`0x00355989`) |
| `eventstartsync(slot)` | `0x0165` | begin `0x0034F3C0`, poll `0x0034F6F0` | the begin pushes a 0 flag first (`0x00267F90`, `0x0034F3DA`), pops it and the slot, and keeps the manager record `0x00263FF0(m)` at scratch `+0` and the flag at `+8` (`0x0034F3E2`-`0x0034F41D`); waits while manager `+0x10` has bit `0x2` and not bit `0x1`; with bit `0x1` set the 0 flag ends the wait at once (`0x0034F703`) |
| `eventstartsync_166(slot, flag)` | `0x0166` | begin `0x0034E460`, poll `0x0034EAB0` | the begin pops the flag and the slot and keeps the same two values as `eventstartsync`'s begin (`0x0034E478`-`0x0034E4B3`); waits while `+0x10` has bit `0x2` and not bit `0x1`, or has bits `0x1` and `0x80` while the flag is set; with bit `0x1` set, a clear flag or a clear bit `0x80` ends the wait whatever bit `0x2` holds (`0x0034EAC6`, `0x0034EACC`) |
| `eventstartsync_167()` | `0x0167` | begin `0x0034FC50`, poll `0x0034F6F0` | the begin pushes two zeros: manager 1, flag 0 |
| `eventdispose_f2(slot)` | `0x00F2` | begin `0x00356D40`, poll `0x0033F150` | `0x00332190(m)`: when manager `m` is busy (`+0x13`), active or loading (`+0x11` bit `0x8`) it sets `0x022C6D20[m]` to 1 (`0x003321BD`) and, when the manager is active, requests its teardown through `0x0026A5F0` (`0x003321CA`); a manager that is idle, inactive and not loading is left as it is (`0x003321B0`). A negative slot means the issuer's own manager, `[0x02099D70] + 0x28` (`0x00356DAC`), disposed only when it is 1 to 3 (`0x00356DB5`); from manager 0 or 4 the begin disposes nothing. The begin clears its flag (`0x00356D5C`) and sets it to 1 when `m` is the issuer's manager (`0x00356DBE`, `0x00356DC3`), and the poll halts the issuer (`+0x14` bit `0x40`) when it disposed itself. After a non-negative slot's dispose it calls the stub `0x0016D6A0(m)` (`0x00356D83`, `0x00356D9D`), which does nothing; on every path it then releases the depth-of-field focus with `0x00382B50(-1, 0, 0)` (`0x00356DD1`, [post-processing](../Graphics/post-processing.md)) and tail-jumps to `0x001EC4B0(m)` (`0x00356DE7`), which empties event-slot panel slot `m` (`0x0020A760`) and raises the scene-reset byte (`0x00214B30`) |

The `eventdispose_f2` poll `0x0033F150` halts the issuer (`+0x14` bit `0x40`) and returns 1 when the begin's flag
(scratch `+0`, set at `0x00356DC3`) is set, and returns 0 otherwise (`0x0033F150`-`0x0033F162`).

The load request `0x0032FC30` queues the scene's files, and `0x0032ED70` sets bit `0x1` of the manager's
pending-load mask at `0x022C6E48 + m × 8`. That bit is the start hold: the files are loaded when
every other bit is clear, but the scene does not start until `eventplay` calls `0x00332130`, which
clears bit `0x1` (`0x00332154`). When the mask is then empty it also clears manager `+0x11` bit `0x8`
(`0x0033215F`, `0x00332168`) and, if the mask was non-zero before the call, runs the finaliser
`0x0032F1B0(m)` (`0x0033216F`, `0x00332174`, `0x00332178`).

A second call on an empty mask clears `+0x11` bit `0x8` again and does not run the finaliser; while other bits are
still pending the call only clears bit `0x1`.

Neither `eventplay` (`0x00EB`) nor `eventplay_ec` (`0x00EC`) has a begin or a poll callback: each runs its result
callback once at its step and does not wait for the files. `eventreadsync` and `eventreadsync_ea` wait for them; they
share the poll `0x003541B0` (`eventreadsync`'s `0x00354740` is a jump to it). `moviestandby`'s ready test `0x0035B7A0` also
waits while manager 3's loads are pending (`0x00254A80`, `0x0035B7B4`-`0x0035B7BB`).

For a manager above 0 the finaliser resets light group `m` (`0x0037B230`, `0x0032F1D4`) and clears its ready byte
(`0x003DE920(m, 0)`, `0x0032F1E0`). When the payload's lighting section `0x022C6E20[m]` is set (`0x0032F1F2`) it binds it
(`0x0037AA90`, `0x0032F1F9`), sets the ready byte again (`0x0032F207`) and stores the first cut id plus 1 at manager
`+0x1FC` (`0x0037B290`, `0x0032F215`); a manager of 0 or below skips all of this (`0x0032F1BB`)
([lighting](../EBP-Script-Files/ebp-lighting-lgt2.md)).

Every manager is then activated (`0x0026CE60`, `0x0032F227`, which posts the start entry's request list through
`0x00266C50`), and the finaliser returns `0x00263C30(m)` through its tail jump (`0x0032F233`): the manager's record count
`+0x20` while it is active, else 0. The first field pass then warms the start entry up
([script requests](script-requests.md)).

`startscene(n)` (`0x011B`, `0x0034C9A0`) reports the pair (scene id, n) to the achievement hook
`0x00863240`. The scene id is `0x0032F240` of the issuer's manager `[0x02099D70] + 0x28` (`0x0034C9B5`, `0x0034C9B8`): the
event-script number registered for it, or -1 when its byte `0x022C6D18[m]` is 0 (`0x0032F24A`, `0x0032F25C`). The hook
does nothing when no Steam manager `[0x01F83450]` exists (`0x00863256`) and otherwise passes the pair to `0x0020CB50`
(`0x00863265`, [achievements](../Steam-And-Achievements/achievements.md)).

The verb then tail-jumps to `0x0026B750(n)` (`0x0034C9CD`). It reads the frame counter `0x022C252C` through `0x00314890` and
discards the value (`0x0026B758`), resets the counter to 0 (`0x00314010`), stores `n` at `0x022C2538` and 0 at the bytes
`0x022C253C` and `0x022C253D` (`0x00314DF0`). It pushes `n`, not the scene id, into the event-slot panel slot of the
issuer's manager through `0x0020AF10` (`0x001EC6A0(m, n)`, a jump to `0x0020AF10`, `0x0026B775`).

For a slot of 0 to 4, an `n` other than -1 and a slot with a name, `0x0020AF10` appends `n` to the slot's vector and
adds 1 to the slot's count at `0x01F832B0` (`0x0020AF61`-`0x0020AFB4`).

It ends with a tail jump to `0x001EC600` (`0x0026B77F`), which jumps to the cutscene JSON loader `0x001C5930` when the
slot `0x0020AF10` marked at `0x01DFE40C` has a non-zero count (`0x001EC600`-`0x001EC617`) and otherwise returns. The
loader's gate byte `0x01DF6E48` ships as 1 (`0x001C5958`); the
[debug menu](../Engine-Core/debug-menu.md) has the event-slot panel.

### Movies

| Verb | Id | Callbacks | Effect |
|---|---|---|---|
| `moviestandby(id)` | `0x0368` | `0x003567F0` / `0x00356050` / `0x00356460` (→ `0x0035B840(id, manager)`) | waits until `0x0035B7A0` says no fade or load is active, then resets the movie screen size `0x02ADD933` to 3 (`0x0037B470(−1)`, `0x0035B851`), reads the manager's skip mask through `0x00267310` and discards it (`0x0035B858`), sets action row 0 bit `0x1`, which bars the main menu, and bit `0x100000` of the same row, which no reader tests (`0x002E1C20`, `0x0035B861`, `0x0035B86D`, [action availability](../Controls-And-Input/action-availability.md)), sets the arena mode to 1 (`0x0037B450(1)`, `0x0035B877`, [resource arena](../Game-Files-And-Data-Tables/resource-arena-and-relocation.md)), raises busy bit `0x10000` (`0x003601B0(0x10)`, `0x0035B881`), frees `0x022C8058` when it is set (`0x003697F0`, `0x0035B890`) and zeroes it (`0x0035B897`), fetches the kind-28 entry `2 × id + 1` through `0x002DF980` and discards it (`0x0035B8AE`, [movies](../Graphics/movies.md)), opens the movie (`0x001848A0`) and dismisses the loading page `[0x01F82CD8]` through its tail jump to `0x00183070` (`0x0035B8C4`, [game application](../Engine-Core/game-application.md)) |
| `movieplay(v)` | `0x036A` | `0x00356D20` (pops a value it ignores, then `0x0035B7D0`) | switches off the field systems (`0x00358750` and its siblings, `0x002E1CD0(0, 0)`, which sets the action row 0 mask `0x139203`, `0x002E1C40(0, 4)`, and `0x00368AA0(0, 0)`, which sets bit `0x1` of `0x02EC0B39`, `0x0035B82B`) and starts playback `0x001848C0` through its tail jump (`0x0035B834`) |
| `getmoviestatus` | `0x036F` | `0x00340870` (→ `0x0035B740`) | returns the player's state `0x00184860` when it is 1, 2 or 3, else 0, and pumps the opening player (`0x00184880`) while it is 1 |
| `moviecancel` | `0x036E` | `0x0033FEC0` (→ `0x0035B720`) / `0x00357300` / `0x0033FA20` | asks the player to stop, waits while the status is 1 to 3, then ends |
| `movieend` | `0x036D` | `0x0033FA20` → `0x0035B8D0` | stops the player (`0x001848E0(0)`, `0x0035B8D6`), frees the buffer `0x022C8058` when it is set and zeroes it (`0x0035B8E5`, `0x0035B8EC`), clears busy bit `0x10000` (`0x003601C0(0x10)`, `0x0035B8FC`) and switches the field systems back on: `0x00358750(0, 0)`, the same siblings with 1, `0x00358650(1)` and `0x00358700(1)`, which set bits `0x4` and `0x8` of `0x022C7F92` and which `movieplay` does not touch (`0x0035B953`, `0x0035B95D`), `0x002E1CD0(1, 0)`, which clears the action row 0 mask `0x139203` and with it the bits `0x1` and `0x100000` that `moviestandby` set, `0x002E1C40(1, 4)` and `0x00368AA0(0, 1)`; it ends by setting the arena mode back to 0 through its tail jump to `0x0037B450(0)` (`0x0035B98B`) |

`0x0033FA20` and `0x0033FEC0` are reached through the verb table: `0x0033FA20` is the result callback of both `movieend`
(`0x01EF44C0`) and `moviecancel` (`0x01EF44E0`), and `0x0033FEC0` is `moviecancel`'s begin (`0x01EF44C8`); nothing calls or
jumps to either directly, and no other pointer to them is stored.

The player object at `0x01F81218` keeps its state at `+4`: 0 idle, 1 opening, 2 ready, 3 playing,
4 the last 233 ms, 5 ending, 6 the skip fade. A script therefore reads "finished" from the last
frames onward.

### Skips

Skip slots are 16-byte entries at `0x022CB730`, indexed `index + manager × 8`: `+0` bit, `+1` mask
index, `+2` state, `+4` record id, `+8` executed, `+0xC` armed. `skipstart(i)` (`0x051A`,
`0x0034D3A0` → `0x00360980(i, manager, record id)`, with the issuer's byte `+0x15` as the manager and its 16-bit word
`+0` as the record id, `0x0034D3B1`, `0x0034D3B7`) returns at once for manager 0 (`0x00360982`).

For a scene manager `0x00360980` sets action row 0 bits `0x2000` and `0x80000` (`0x002E1C20(0, 0xD)` and
`0x002E1C20(0, 0x13)`, `0x003609A7`, `0x003609B3`), the two bits that steer Start's event-skip arm
([action availability](../Controls-And-Input/action-availability.md)). It then sets state 1 and armed (`0x003609ED`,
`0x003609E9`), sets the bit in `0x022CB9C0` and clears it in `0x022CB9D8` (`0x003609F3`, `0x003609FD`), clears the executed
word (`0x00360A05`) and stores the record id (`0x00360A0D`). `skipcheck(i)` (`0x051C`) returns the executed word
through `0x003604A0`.

`skipexec(i)` (`0x0539`, `0x0034ECF0` → `0x00360710`, for the issuer's manager byte `+0x15`) runs only for a manager other
than 0 whose slot is live with bit `0x80` of its `+0x10` clear (`0x00267330` answers 0, `0x00360758`) and whose entry is
armed (`+0xC` non-zero, `0x00360768`); otherwise it returns 0 and changes nothing.

When it runs it returns 1: state 2, executed 1, busy bit `0x8000`, the entry's bit set in `0x022CB9D8` and cleared in
`0x022CB9C0` (`0x003607CD`, `0x003607D9`), time-stop request 27 (`0x002273E0`), the teardown of the manager's sound, effects
and presentation, and finally the mask bit `0x0026A5B0(manager, 1, i)` that ends the waits ([native
commands](native-commands.md)).

Part of that teardown, `0x003B08F0`, also run when a skip ends, walks the 36-entry table of 24-byte
effect records at `0x02EBEC00` and stops at the first entry whose first dword is 0. It frees every
entry that is not marked to keep (`+0x13` bit `0x1`) and whose type byte `+0x10` is not `0x63`,
through `0x003B0770` and `0x0024EE60`. `0x003B0770` moves the later entries down one place, so after a
free the walk examines the same slot again.

`0x00360670` reports whether any skip of mask index 1 to 3 has executed (`0x022CB9DC` to
`0x022CB9E4`); while it does, or while byte `0x022CB726` is set (`0x003603C0`), the character sound
player `0x002E9D90` behind the `charseplay` verbs plays nothing.

`skipend(i)` (`0x051B`, begin `0x0034D820`, poll `0x0034DB30`) marks an entry whose state is not 2
(`0x00360650`) in its scratch and releases it at once (`0x00360A20`); otherwise it waits through four
stages (`0x0025C070`; `0x003608D0`, which starts the track `skipexec` recorded, or only sets its volume
when it already plays
([music](../Sound-And-Music/music.md)); `0x00360D60`; then no music track end still scheduled and no load pending), releases,
and waits one more stage on `0x00229EB0`.

The third stage asks the scheduled-task test `0x002F1A30(1)` (`0x0034DBCE`, [frame update
order](../Engine-Core/frame-update-order.md)) and then `0x0032E520(1)` (`0x0034DBD9`), and stays while either
answers non-zero (`0x0034DBD5`, `0x0034DBE0`). The argument is 1 from `0x0034DB49` on that path.

The poll keeps the stage in scratch `+4` and returns 1 while it waits, 0 when it is done. Any negative stage,
not only −1, releases (`0x0034DB4E`; `0x00360A20(i, manager)` with the issuer's byte `+0x15`, `0x0034DB59`) and
returns 0. Stage 0 moves to 1 once
`0x0025C070(manager, issuer)` is non-zero (`0x0034DC12`, `0x0034DC1B`) and waits in either case. Stage 1 stays while
`0x003608D0` returns 0 (`0x0034DBB3`) and stage 2 while `0x00360D60` (`0x022CBA58` non-zero) is non-zero (`0x0034DBC3`); a
stage that is passed falls through to the next in the same poll (`0x0034DBB5`, `0x0034DBC5`).

`0x0025C070(manager, issuer)` is 1 when the manager's `+0x10` has bit `0x1` clear, or when every actor `0x00358940`
returns from its actor table for the indexes below the signed dword at `+0x20`, other than the issuer, has `+0x14` bit
`0x40` set, and 0 otherwise (`0x0025C09B`-`0x0025C0CB`, `0x0025C0E5`). Past the table's own count `0x00358940` returns 0
(`0x00358944`-`0x0035895B`), and `0x0025C070` then reads byte `+0x14` of that null (`0x0025C0BF`).

Past the third stage the poll releases the entry (`0x0034DBE8`), stores the game-step count `0x02064AD0` (`0x00229EB0`)
in scratch byte `+8` (`0x0034DBF2`) and moves to stage 4 (`0x0034DBF7`). Stage 4 returns 0 once the count differs from
that byte (`0x0034DB92`), one game step later. The begin and the poll store only the stages −1 to 4; a stage above 4
returns 1 (`0x0034DB84`).

`0x00360A50`, which `skipend`'s release `0x00360A20` calls (`0x00360A26`; [native
commands](native-commands.md#the-skip-mask)), does not write the entry's executed word `+8`, so `skipcheck` keeps
answering 1 until the next `skipstart` of that entry (`0x00360A05`), or until `0x003605A0` or `0x003604D0` zero the word
(below).

`0x003603F0(m)` ends all eight skips of manager `m` through `0x00360A50` (`0x00360410`-`0x00360430`), with `0x003601C0(0xF)`
after each that had executed (`0x0036041D`-`0x00360424`). When any had, it then calls `0x003600D0`, `0x003601C0(0xF)`, the
fade `0x002EFA70(4, 8, 1, 0)` ([screen fades](../Graphics/screen-fades.md)) and `0x002260E0`
(`0x00360432`-`0x00360458`).

The manager unload `0x002628B0(m)` ([frame update order](../Engine-Core/frame-update-order.md)), which
`0x0025BFB0` runs for each manager whose bit is set in `0x02099ABC` (`0x0025C030`-`0x0025C036`; `eventdispose` sets it through
`0x0026A5F0`, `0x0026A61C`-`0x0026A620`), calls `0x003603F0` (`0x0026293F`) and then `0x003605A0` (`0x00262946`), both only while
the manager's byte `+0x10` has bit `0x1` (`0x0026292C`-`0x00262930`).

`0x003605A0(m)` rebuilds the eight entries of manager `m`: `+0` the index, `+1` = `m`, and state `+2` and the words `+8`
and `+0xC` zero (`0x00360604`-`0x0036061B`); it also zeroes the manager's words of both mask arrays (`0x003605CC`,
`0x003605E2`). The initialiser `0x003604D0`, which `0x002628B0` runs for manager 0, under the same bit `0x1` test, when
`0x003603C0()` answers non-zero (`0x002629BA`, `0x00262A87`-`0x00262AB3`), does the same for managers 0 to 4
(`0x00360507`-`0x00360548`, `0x0036054B`) and also zeroes the byte `0x022CB9BC` (`0x00360581`), which `0x003606E0` sets while a
skip of mask index 1 to 3 has executed.

Start's event-skip arm ([action availability](../Controls-And-Input/action-availability.md)) builds the task `0x00228C70` through
`0x00228700` and `0x002289D0` when the task pointers `[0x0209AC30] + 0xC8` and `+0xD0` are both empty (`0x0022871A`,
`0x002289EA`). The task formats the line built from legend scene 15 into the buffer `0x01FD4840` (`0x00228CC0`-`0x00228CF4`)
and draws it only while its `+0xF0` bit `0x2` is set (`0x00228C39`-`0x00228C60`).

The task sets that bit only on a tick in state 1 when its mode changes to 0, and then only while its `+0xE0`, the arm
from Start's handler, is 1 (`0x00228E96`-`0x00228EFB`, `0x00228FE9`-`0x00228FF3`). It clears the bit when the mode changes to
1 or 2 (`0x00228F9C`, `0x00228F3E`) and at other sites, and in state 1, unless the bit-`0x1` test of `0x0029DBE0(0x17)` has
already moved it to state 2 (`0x002292D3`-`0x00229308`), the bit also gates the task's test of `0x0029DBE0(0x113)`, which,
when the mask equals both words `0x02F97368` and `0x02F9736A`, moves it to state 3 (`0x0022930D`-`0x00229342`).

## Layouts

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2098E10` | `SceneManager[5]` | managers | manager `m` at `+ m × 0x288`, five slots ([actor managers](../Characters-And-Objects/actor-managers.md)); 0 is the zone, 1 to 3 the scenes |
| `+0x22C6E48` | `u64[4]` | pendingLoad | per manager; bit `0x1` is the start hold |
| `+0x22C6D20` | `u8[4]` | unloadRequest | per manager |
| `+0x22CB730` | `SkipEntry[40]` | skips | entry `i + m × 8`, stride 16; the initialiser `0x003604D0` builds 5 groups of 8 (`0x00360559`, `0x0036056D`) |
| `+0x22CB9C0` | `u32[5]` | skipArmed | per mask index 0-4 (`0x0036056D`); set by `skipstart`, cleared by `skipexec`, `0x00360A50`, `0x003604D0` and `0x003605A0` |
| `+0x22CB9D8` | `u32[5]` | skipExecuted | per mask index 0-4; set by `skipexec`, cleared by `skipstart` (`0x003609FD`), `0x00360A50` (`0x00360AF1`), `0x003604D0` and `0x003605A0` |
| `+0x1F81218` | `MoviePlayer` | movie | the movie player |
| `+0x2099DE2` | `u8` | eventSwitch | 0 stops the scene verbs |

SceneManager (stride `0x288`):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x008` | `void*` | actors | actor table: `u32` count, then actor pointers from its `+8` |
| `+0x010` | `u8` | flags | bit `0x1` active |
| `+0x011` | `u8` | loadFlags | bit `0x8` loading |
| `+0x013` | `u8` | busy | non-zero while busy |
| `+0x1D6` | `u16` | windowCount | entries in the ordinal window |
| `+0x1DE` | `u16` | windowFirst | first ordinal of the window |
| `+0x1E0` | `i32` | lockCount | world-lock takes |
| `+0x201` | `u8` | skipMask | one bit per skip index (`0x02099011 + m × 0x288`) |

SkipEntry (16 bytes):

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u8` | bit | bit index in the masks |
| `+0x01` | `u8` | maskIndex | which mask word |
| `+0x02` | `u8` | state | 1 started, 2 executed |
| `+0x04` | `u32` | recordId | record id |
| `+0x08` | `u32` | executed | read by `skipcheck` |
| `+0x0C` | `u32` | armed | set by `skipstart` |

MoviePlayer:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x04` | `u32` | state | 0 idle, 1 opening, 2 ready, 3 playing, 4 last frames, 5 ending, 6 skip fade |

## Shipped data

| Fact | Value |
|---|---|
| scene managers | 3 (1 to 3) beside the zone's manager 0 |
| `startscene` uses | 3,789 |
| `eventread_e8` / `eventplay_ec` / `eventsync_ee` uses | 596 / 567 / 553 |
| skip verbs | `skipstart` 292, `skipend` 291, `skipcheck` 237, `skipexec` 19 |
| movie status values a script sees | 1 opening, 2 ready, 3 playing; 0 otherwise |

## Operations

Per scene: load (one request), wait, release the hold, run, wait for the manager to idle, dispose.

## State

The three scene managers' active, busy and loading bits, the pending-load masks, the skip table and masks, and
the movie player state.

## Modding notes

- A scene cannot start before `eventplay` clears the hold, however early its files finish loading.

## Related

- [The party during scenes](party-during-scenes.md): hiding, capturing and the summon group.
- [The world lock](world-lock.md): what holds everyone else still during a talk or scene.
- [Native commands](native-commands.md): the skip mask that ends waits.

### Cross-subsystem neighbours

Calls between the functions this page cites and code in other parts of the program, from the program's call graph:

- Actor entity: `0x0032F1B0` calls `0x0037AA90`; `0x0037B230` is called by `0x0037AA90`; those functions are documented on
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
- Actor entity: `0x00183070` is called by `0x0025D9E0`; `0x0025C070` calls `0x00358940`; `0x00263C30` is called by `0x0032F1B0`;
  `0x00266C50` calls `0x00358940`, `0x003DBB60`; `0x00266C50` is called by `0x0026CE60`; `0x0026A5F0` is called by `0x0025D9E0`;
  `0x0026CE60` calls `0x00233CF0`, `0x002572E0`, `0x00263660`, `0x00265A20`, `0x00266C50`, `0x002679F0`, `0x00268EA0`, `0x0026D3E0`,
  `0x003587C0`, `0x00358940`, `0x003DB1F0`.
- Actor entity: `0x0026CE60` is called by `0x0025BFB0`, `0x0032F1B0`; `0x002DF980` is called by `0x0032FCA0`; `0x002E1C40` is
  called by `0x0025D9E0`, `0x002628B0`; `0x002E1CD0` is called by `0x0025C830`, `0x00263050`, `0x00263660`, `0x00268D10`,
  `0x0026C5D0`; `0x002E9D90` calls `0x00263FF0`; `0x002F1A30` is called by `0x0025D9E0`; `0x00314010` is called by `0x002695A0`,
  `0x0026CE60`; `0x00314DF0` is called by `0x002695A0`, `0x0026CE60`.
- Actor entity: `0x0032E520` is called by `0x002628B0`; `0x0032F1B0` calls `0x00263C30`, `0x00263FF0`, `0x0026CE60`, `0x0037B230`,
  `0x0037B290`, `0x003DE920`; `0x0032F1B0` is called by `0x0032F850`, `0x0032FA10`, `0x0032FAC0`, `0x0032FB70`, `0x00330060`,
  `0x00330110`, `0x00330190`, `0x00330220`, `0x003302B0`, `0x003304A0`, `0x00331610`, `0x003316B0`; `0x0032F1B0` is also called by
  `0x00331760`, `0x003317C0`, `0x00331820`, `0x00332130`.
- Actor entity: `0x0032F240` is called by `0x0026C8C0`; `0x0032F6C0` is called by `0x0025D9E0`; `0x0032FC30` calls `0x0032FCA0`;
  `0x0032FC30` is called by `0x0025D9E0`; `0x00332130` calls `0x00263FF0`, `0x0032F1B0`; `0x00332190` calls `0x00263FF0`; `0x0034C9A0`
  calls `0x0032F240`; `0x0034DB30` calls `0x0025C070`; `0x0034E460` calls `0x00263FF0`; `0x0034F3C0` calls `0x00263FF0`; `0x0034FC50`
  calls `0x00263FF0`; `0x00351C90` calls `0x00263FF0`.
- Actor entity: `0x00354B20` calls `0x00332130`; `0x003601B0` is called by `0x002628B0`; `0x003603C0` is called by `0x0025D9E0`,
  `0x002628B0`; `0x003604D0` is called by `0x002628B0`; `0x00360D60` is called by `0x0025D9E0`; `0x00368AA0` is called by
  `0x002628B0`; `0x0037AA90` calls `0x0037B230`; `0x0037AA90` is called by `0x0032F1B0`; `0x0037B230` is called by `0x002628B0`,
  `0x0032F1B0`; `0x0037B290` is called by `0x0032F1B0`.
- Actor entity: `0x003DE920` calls `0x0037ACA0`, `0x0037ACD0`; `0x003DE920` is called by `0x002628B0`, `0x0032F1B0`.
- Actor entity: those functions are documented on
  [frame update order](../Engine-Core/frame-update-order.md),
  [zone changes and mapjump](../World-Areas-And-Travel/zone-changes-and-mapjump.md),
  [script requests](script-requests.md), [party control modes](../Engine-Core/party-control-modes.md).
- Actor entity: and on [actor managers](../Characters-And-Objects/actor-managers.md),
  [actor lifecycle](../Characters-And-Objects/actor-lifecycle.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [force fight mode](../Engine-Core/force-fight-mode.md).
- Actor entity: and on [ps2 cpu emulation](../Engine-Core/ps2-cpu-emulation.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [startup constants](../Engine-Core/startup-constants.md),
  [actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md).
- Actor entity: and on [ebp lighting lgt2](../EBP-Script-Files/ebp-lighting-lgt2.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md),
  [ard area battle data](../Game-Files-And-Data-Tables/ard-area-battle-data.md),
  [ebp camera tables](../EBP-Script-Files/ebp-camera-tables.md).
- Actor entity: and on [tim2 images](../Game-Files-And-Data-Tables/tim2-images.md),
  [ebp script container](../EBP-Script-Files/ebp-script-container.md),
  [ebp camera shake](../EBP-Script-Files/ebp-camera-shake.md), [script variables](script-variables.md),
  [weather](../World-Areas-And-Travel/weather.md).
- Application: `0x00792350` is called by `0x0015BC40`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Audio: `0x00267330` is called by `0x003A1070`, `0x003A1180`; `0x0034DB30` calls `0x003608D0`; `0x003601B0` is called by
  `0x003614E0`; `0x003601C0` is called by `0x00361460`; `0x003603C0` is called by `0x002DEF40`, `0x002DEFA0`, `0x002DF010`,
  `0x002DF120`, `0x002DF220`, `0x002DF2C0`, `0x002DF560`; `0x00360710` calls `0x002DEDD0`; `0x003608D0` calls `0x002DE350`,
  `0x002DEE30`.
- Audio: those functions are documented on [sound banks](../Sound-And-Music/sound-banks.md),
  [force fight mode](../Engine-Core/force-fight-mode.md), [music](../Sound-And-Music/music.md),
  [frame update order](../Engine-Core/frame-update-order.md), [map sounds](../Sound-And-Music/map-sounds.md),
  [audio manager](../Sound-And-Music/audio-manager.md).
- Audio: and on [scripted camera](../Graphics/scripted-camera.md),
  [native commands](native-commands.md), [menu screens](../Menus-And-HUD/menu-screens.md).
- Combat action: `0x0032E520` is called by `0x002FC3C0`; `0x0032ED70` is called by `0x00306BD0`; `0x0032F6C0` is called by
  `0x00306B10`; `0x0032FC30` is called by `0x00306BD0`; `0x00332130` is called by `0x00306760`; `0x00332190` is called by
  `0x00306570`, `0x003065D0`.
- Combat action: those functions are documented on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [battle units](../Characters-And-Objects/battle-units.md), [action phases](../Battle-Actions/action-phases.md),
  [party control modes](../Engine-Core/party-control-modes.md).
- Combat action: and on [frame update order](../Engine-Core/frame-update-order.md).
- Core runtime: `0x001C2F50` is called by `0x0017D6E0`; `0x0032E520` is called by `0x0022B6E0`, `0x0022B7E0`; `0x0034DB30` calls
  `0x00229EB0`; `0x003603C0` is called by `0x0022A770`; `0x0053DD10` is called by `0x0022B6E0`.
- Core runtime: those functions are documented on [debug menu](../Engine-Core/debug-menu.md),
  [frame update order](../Engine-Core/frame-update-order.md),
  [save and teleport crystals](../World-Areas-And-Travel/save-and-teleport-crystals.md).
- Developer: `0x00796E20` is called by `0x001C2F50`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Input: `0x002273E0` calls `0x00226BE0`; `0x00267310` is called by `0x002E09A0`; `0x0053DD10` is called by `0x002E09A0`,
  `0x0035FCA0`, `0x0035FDD0`, `0x0046DD50`; `0x00796E20` is called by `0x0017DDC0`, `0x0017DE10`, `0x0017DE60`, `0x0017DFC0`,
  `0x00196680`, `0x00196710`, `0x001967D0`, `0x00196C40`, `0x00196DF0`, `0x00196EE0`, `0x00197160`, `0x00197990`.
- Input: `0x00796E20` is also called by `0x00198E80`, `0x001E0920`, `0x001E0C30`, `0x001E0C50`, `0x001E0CE0`, `0x001E0D30`,
  `0x001E0E00`, `0x001E0E70`.
- Input: those functions are documented on [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [frame update order](../Engine-Core/frame-update-order.md), [controls](../Controls-And-Input/controls.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Input: and on [force fight mode](../Engine-Core/force-fight-mode.md),
  [player movement](../Movement-And-Pathfinding/player-movement.md),
  [control remapping](../Controls-And-Input/control-remapping.md), [pause screen](../Menus-And-HUD/pause-screen.md),
  [game application](../Engine-Core/game-application.md).
- Input: and on [debug menu](../Engine-Core/debug-menu.md), [vibration](../Controls-And-Input/vibration.md),
  [field camera](../Graphics/field-camera.md),
  [on screen keyboard](../Controls-And-Input/on-screen-keyboard.md).
- Input gameplay: `0x002E1C20` is called by `0x00313A00`; `0x002E1C40` is called by `0x00313A00`; those functions are
  documented on [force fight mode](../Engine-Core/force-fight-mode.md).
- Movement: `0x00267310` is called by `0x002E45E0`, `0x002E5750`; `0x002E1CD0` is called by `0x0026C3E0`; `0x003DE920` is called
  by `0x00379080`, `0x00379110`.
- Movement: those functions are documented on
  [facing and steering](../Movement-And-Pathfinding/facing-and-steering.md),
  [time stop and freeze](../Engine-Core/time-stop-and-freeze.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md); and on
  [character lighting and shadows](../Graphics/character-lighting-and-shadows.md).
- Party: `0x00267330` is called by `0x00358CB0`, `0x00359150`; `0x0026CE60` calls `0x00358BB0`; `0x003601B0` is called by
  `0x0034CDF0`, `0x0034D4E0`, `0x00350160`, `0x00350CD0`, `0x00352AF0`; `0x003601C0` is called by `0x0034CDF0`.
- Party: those functions are documented on
  [movement bodies and separation](../Movement-And-Pathfinding/movement-bodies-and-separation.md),
  [map screens](../Menus-And-HUD/map-screens.md), [frame update order](../Engine-Core/frame-update-order.md),
  [party verbs](party-verbs.md).
- Platform: `0x00792350` calls `0x005CD0A0`; those functions are documented on
  [game application](../Engine-Core/game-application.md).
- Platform online achievements: `0x0020CB50` is called by `0x00863240`; `0x0034C9A0` calls `0x00863240`; `0x00796E20` is called
  by `0x008655A0`; `0x00863240` calls `0x0020CB50`, `0x0020CE00`; those functions are documented on
  [achievements](../Steam-And-Achievements/achievements.md),
  [steam integration](../Steam-And-Achievements/steam-integration.md).
- Presentation: `0x0024EE60` is called by `0x003AFFB0`, `0x003B02A0`, `0x003B0980`, `0x003B2BC0`, `0x003B2D80`, `0x003B3300`;
  `0x00263C30` is called by `0x00256F60`, `0x003A4290`, `0x003A56F0`, `0x00465120`, `0x00465690`; `0x00267310` is called by
  `0x003DD4C0`; `0x002DF980` is called by `0x001BB2B0`; `0x002E9D90` is called by `0x0046CC70`; `0x0032E520` is called by
  `0x003B53C0`; `0x0032F240` is called by `0x003DD4C0`.
- Presentation: `0x0053DD10` is called by `0x004355D0`, `0x00462540`; `0x00796E20` is called by `0x00186CD0`, `0x00187950`,
  `0x0018D160`, `0x0018D850`, `0x001CD0E0`, `0x001D1660`, `0x001D5260`.
- Presentation: those functions are documented on
  [effect file loading](../Graphics/effect-file-loading.md),
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [effects on actors and scripts](../Graphics/effects-on-actors-and-scripts.md).
- Presentation: and on [menu effects](../Graphics/menu-effects.md),
  [license board screen](../Menus-And-HUD/license-board-screen.md),
  [character effects](../Graphics/character-effects.md),
  [frame update order](../Engine-Core/frame-update-order.md).
- Presentation: and on [authored expressions](../Game-Files-And-Data-Tables/authored-expressions.md),
  [effect element runtime](../Graphics/effect-element-runtime.md),
  [effect element types](../Graphics/effect-element-types.md),
  [script name bindings](script-name-bindings.md).
- Presentation: and on [file size tables fst](../Game-Files-And-Data-Tables/file-size-tables-fst.md),
  [character se tables chse](../Game-Files-And-Data-Tables/character-se-tables-chse.md),
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md).
- Presentation: and on [game application](../Engine-Core/game-application.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [render parameters and shader assets](../Graphics/render-parameters-and-shader-assets.md); and on
  [debug menu commands](../Engine-Core/debug-menu-commands.md).
- Resource: `0x001D6A70` calls `0x001DADA0`; `0x0020A760` is called by `0x0020AC30`; `0x002DF980` is called by `0x001DA290`,
  `0x002EEEE0`; `0x0032E520` calls `0x0032E070`, `0x0046DFE0`; `0x0032E520` is called by `0x0024AC30`; `0x0034DB30` calls
  `0x0032E520`; `0x00351880` calls `0x001D6A70`; `0x003529E0` calls `0x001D6A70`; `0x0035B840` calls `0x002DF980`; `0x0037B450` is
  called by `0x0024AC30`; `0x00796E20` is called by `0x001A7A50`.
- Resource: those functions are documented on
  [file path resolution](../Game-Files-And-Data-Tables/file-path-resolution.md),
  [debug menu](../Engine-Core/debug-menu.md), [debug logging](../Engine-Core/debug-logging.md).
- Resource: and on
  [file requests and the read queue](../Game-Files-And-Data-Tables/file-requests-and-the-read-queue.md),
  [prefetch manifests](../Game-Files-And-Data-Tables/prefetch-manifests.md).
- Save load settings: `0x002E1C20` is called by `0x005823B0`, `0x00582860`; those functions are documented on
  [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md),
  [game application](../Engine-Core/game-application.md).
- UI: `0x0024EE60` is called by `0x0024B9B0`; `0x0026CE60` calls `0x00253A30`; `0x002E1C20` is called by `0x00276650`, `0x00279E20`,
  `0x0035CF10`, `0x0035D6B0`; `0x002F1A30` is called by `0x003EF2E0`; `0x0053DD10` is called by `0x003C80C0`; `0x00796E20` is called
  by `0x0018EEE0`.
- UI: those functions are documented on [frame update order](../Engine-Core/frame-update-order.md),
  [actor managers](../Characters-And-Objects/actor-managers.md),
  [force fight mode](../Engine-Core/force-fight-mode.md),
  [tutorial battle commands](../Battle-Actions/tutorial-battle-commands.md).
- UI: and on [chocobos and airships](../World-Areas-And-Travel/chocobos-and-airships.md),
  [action availability](../Controls-And-Input/action-availability.md), [game over](../World-Areas-And-Travel/game-over.md),
  [map screens](../Menus-And-HUD/map-screens.md), [graphics settings](../Engine-Core/graphics-settings.md).
- World area: `0x00314010` is called by `0x00266D10`; `0x00314D40` is called by `0x00266D10`; `0x00314DF0` is called by
  `0x00266D10`; `0x003604D0` is called by `0x00266D10`; those functions are documented on
  [force fight mode](../Engine-Core/force-fight-mode.md).
- World area: `0x00267310` is called by `0x00314020`; `0x0026A5F0` is called by `0x00314440`, `0x00314530`, `0x003145E0`;
  `0x0026CE60` calls `0x002342F0`; `0x002DF980` is called by `0x00379A10`; `0x002E1C40` is called by `0x00314440`; `0x0032E520` is
  called by `0x003145E0`; `0x0032FC30` calls `0x0025D4D0`, `0x003319D0`, `0x003EA6E0`; `0x0032FC30` is called by `0x00314020`;
  `0x00332130` is called by `0x00378120`; `0x003522C0` calls `0x0032FC30`.
- World area: `0x00353080` calls `0x0032FC30`; `0x003601B0` is called by `0x003145E0`; `0x0037AA90` is called by `0x003775D0`;
  `0x003DE920` is called by `0x003775D0`, `0x00378230`; `0x0053DD10` is called by `0x003789A0`.
- World area: those functions are documented on [debug logging](../Engine-Core/debug-logging.md),
  [debug menu](../Engine-Core/debug-menu.md),
  [game application](../Engine-Core/game-application.md),
  [changing areas](../World-Areas-And-Travel/changing-areas.md).
- World area: and on [force fight mode](../Engine-Core/force-fight-mode.md),
  [standard file formats](../Game-Files-And-Data-Tables/standard-file-formats.md),
  [frame update order](../Engine-Core/frame-update-order.md); and on
  [doors gates and map changes](../World-Areas-And-Travel/doors-gates-and-map-changes.md),
  [mpk map pack](../World-Areas-And-Travel/mpk-map-pack.md).
