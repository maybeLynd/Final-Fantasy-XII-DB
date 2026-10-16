---
title: "Cutscenes and the world lock: loading, starting, waiting on and unloading an event scene, hiding and capturing party members, movies, skips, and the lock that freezes everyone but the scene"
kind: "system"
category: "Scripts and script commands"
summary: "How a script runs a story scene: the three scene managers and the verbs that load, release, wait on and dispose a scene, the start hold on the load mask, the two global gates every scene verb tests, how a script hides the party and captures a party member's body with capturepc and gives it back with releasepc, the pre-rendered movie verbs and the status a script sees, the skip slots and the skip mask, the event party mode bits, and the world lock a talk or scene takes through the stop registry and the actors it spares."
addresses: ["02098E10", "02099DE2", "00264170", "0026A5A0", "001C3370", "00351880", "00351C90", "003522C0", "00353080", "003541B0", "00354B20", "00355970", "00356D40", "0033F710", "00332130", "00332190", "0032ED70", "0032F1B0", "00267210", "022C6E48", "022C6D20", "0034C9A0", "0026B750", "00863240", "003415D0", "00342250", "00341CB0", "002ECD50", "00352FA0", "003537D0", "0034C3D0", "00264050", "00263750", "00262F50", "00262F90", "002693D0", "00266AD0", "0035AE10", "0034C990", "003B6F30", "00348130", "003484A0", "003567F0", "00356050", "0035B840", "0035B7D0", "0035B8D0", "0035B740", "00357300", "00184860", "00360980", "00360710", "00360A50", "003604A0", "0034DB30", "022CB730", "02099011", "0037D120", "00355FE0", "0034DC30", "00263230", "00263050", "00263480", "00226BE0", "00225CD0", "00377700", "00314A60", "02099DE7", "02099DB4"]
---

# Cutscenes and the world lock: loading, starting, waiting on and unloading an event scene, hiding and capturing party members, movies, skips, and the lock that freezes everyone but the scene

## What the player sees

A story scene: the screen fades, the party vanishes and the scene's own actors take the stage, the
camera takes over, characters talk and move on their own, and at the end control comes back. Some
scenes are pre-rendered movies. Many can be skipped from the pause menu. The same "take over the
body" step happens on a small scale every time the player talks to a townsperson or opens a door:
the character turns, plays a short motion, and control returns. While a talk or scene runs, the
rest of the world holds still: nobody else starts a conversation and nothing else moves.

## How it works

### Scene managers and the two gates

A scene runs in its own actor manager, 1, 2 or 3, beside the zone's manager 0 (`02098E10 +
m × 0x288`). Every scene verb takes a slot argument and uses manager `clamp(slot + 1, 1, 3)`; the
plain-named forms (`eventread`, `eventplay`, `eventsync`) fix the slot at 0, manager 1.

Two gates sit in almost every scene verb. `00264170` returns the event switch byte `02099DE2`,
which area initialisation sets to 1 and `system_seteventexecstatus` (`0x141`) writes through
`0026A5A0`; while it is 0 the load, play and sync verbs do nothing. `001C3370` returns byte
`+0x10D4` of the application object `00796E20` returns, written only to 0 by the constructor
`00792350` and read otherwise by the auto-test walker `001C2F50`: an auto-test switch that is
never set in retail, so scene verbs always proceed past it.

### Loading, the start hold, playing and disposing

| Verb | Id | Callbacks | What it does |
|---|---|---|---|
| `eventread_e8(slot, id)` | `0x00E8` | begin `00351880`, poll `00351C90`, result `003522C0` | the begin stores both and prefetches `001D6A70(id, slot)`; the poll waits while manager `m` is active (`+0x10` bit 0) and busy (`+0x13`); the result queues the load `0032FC30(m, id)` and sets the hold `0032ED70(m)` |
| `eventread(id)` | `0x00E7` | result `00353080` | slot 0, the same load after `00314D40(1)` |
| `eventreadsync_ea(slot)` | `0x00EA` | begin `00353A10`, poll `003541B0` | waits while `0032F6C0(m)` reports loads pending, calling `00314D40(1)` each poll |
| `eventplay_ec(slot)` | `0x00EC` | result `00354B20` | releases the hold `00332130(m)`, then `001EC680(m)`, `0020AF10(m, −1)` and `001EC600()` |
| `eventsync_ee(slot)` | `0x00EE` | begin `00353A10`, poll `00355970` | waits while `00267210(m)` is non-zero: manager active or busy |
| `eventstartsync(slot)` | `0x0165` | begin `0034F3C0`, poll `0034F6F0` | the begin pushes a 0 flag first; waits while manager `+0x10` has bit 1 |
| `eventstartsync_166(slot, flag)` | `0x0166` | begin `0034E460`, poll `0034EAB0` | waits while `+0x10` has bit 1, or bit 0 while the flag is set and bit 7 is set |
| `eventstartsync_167()` | `0x0167` | begin `0034FC50`, poll `0034F6F0` | the begin pushes two zeros: manager 1, flag 0 |
| `eventdispose_f2(slot)` | `0x00F2` | begin `00356D40`, poll `0033F150` | `00332190(m)`: marks `022C6D20[m]` and, when the manager is active, requests its teardown through `0026A5F0`; a negative slot means the issuer's own manager, and the poll halts the issuer (`+0x14` bit 6) when it disposed itself |

The load request `0032FC30` queues the scene's files, and `0032ED70` sets bit 0 of the manager's
pending-load mask at `022C6E48 + m × 8`. That bit is the start hold: the files are loaded when
every other bit is clear, but the scene does not start until `eventplay` calls `00332130`, which
clears bit 0 and manager `+0x11` bit 3 and, when the mask is now empty, runs the finaliser
`0032F1B0(m)`.

The finaliser binds the payload's lighting sections (`0037AA90`), activates the
manager (`0026CE60`, which posts the start entry's request list through `00266C50`) and the first
field pass then warms the start entry up ([script requests](script-requests.md)).

`startscene(n)` (`0x011B`, `0034C9A0`) reports the pair (scene id, n) to the achievement hook
`00863240` and calls `0026B750(n)`: it resets the frame counter `022C252C`, stores `n` at
`022C2538`, pushes the scene id into the event-slot panel through `0020AF10` and runs the debug
cutscene JSON hook `001EC600`, which returns at once in retail.

### Hiding the party

`hideparty` (`0x0147`, `003415D0`) and `showparty` (`0x0148`, `00342250`) call `002ECD50(actor,
0 or 1)` for party slots 0 to 3 through `00263750`; `hideparty_without_uc` (`0x0498`,
`00341CB0`) skips the controlled character. `002ECD50` acts only on a class-3 actor whose
lifecycle byte is not 1: it writes bit 0 of byte `+0x10` of the presentation record (`+0xC0`) and
refreshes visibility through `002E8FD0`. It hides the body and leaves the actor and its battle
unit in place.

`disposepartywithoutcontrol` (`0x0202`, `0034C990` → `003B6F30`) clears the party-control byte
`02B40534`, empties the follower list (`003B6DE0`), narrows the controlled set to the leader
(`003B6D60`) and snapshots each controlled actor's pose (`003B7510`). `capturepartyforsummon`
(`0x0232`) does the same and binds the set to manager 3's entries (`003B72F0`);
`releasepartyforsummon` (`0x0233`) releases them (`003B7AB0`).

### Capturing a party member

`capturepc(slot)` (`0x0057`, `00352FA0`) is how a script on another actor takes a party member's
body. A slot outside 0 to 3 (`002647C0` is an unsigned test for below 4) is replaced by byte
`+0x12` of the controlled character's record (`00264050(0, −1)` resolves the party-focus handle),
so `capturepc(−1)` means "the character the player controls"; a slot at or above 0 first calls
the town test `00377C20` and drops the result. The actor is `00263750(slot)`; `00262F50(owner, pc)` binds
them and on success the verb returns 1 and cancels the member's battle action (`0035AE10`).

`00262F90(owner, pc)` binds only when the member's manager is active, neither record is already
bound (`+0x18` is 0) and the two differ: the member gets `+0x18` = 1 with the owner's manager at
`+0x19` and id at `+0x1A`, the owner gets `+0x18` = 2 with the member's; `002E4A40(owner)`
re-applies the render scale; the owner copies the member's body pointers (`+0xC0` and `+0xB8`);
`002681E0` refreshes both.

`002ECCF0(owner, 1)` then sets presentation `+0x11` bit 7.
`capturepc_not_cancelbattlecommand` (`0x0582`) and the by-id form `capturepcbyentryid`
(`0x02A2`, `0034C3D0`, which resolves a handle through `003588B0`) skip or keep the cancel.

`releasepc` (`0x0058`, a jump into `002693D0(owner, 1)`; `releasepc_404` passes a popped flag)
undoes it. For a capturer, `002693D0` resolves the member, clears its steering byte, re-applies
the owner's render value, rebuilds the member's four body pointers with `00266AD0` from its class
rather than restoring a saved copy, resets its locomotion, and with the flag runs `002EB430` (the
idle motion); then both records get `+0x18` = `0xFFFF0000` and a refresh.

### Movies

| Verb | Id | Callbacks | Effect |
|---|---|---|---|
| `moviestandby(id)` | `0x0368` | `003567F0` / `00356050` / `00356460` (→ `0035B840(id, manager)`) | waits until `0035B7A0` says no fade or load is active, then denies user control, raises busy bit 16, frees `022C8058` and opens the movie (`001848A0`) |
| `movieplay(v)` | `0x036A` | `00356D20` (pops a value it ignores, then `0035B7D0`) | switches off the field systems (`00358750` and its siblings, `002E1CD0(0, 0)`, `002E1C40(0, 4)`) and starts playback `001848C0` |
| `getmoviestatus` | `0x036F` | `00340870` (→ `0035B740`) | returns the player's state `00184860` when it is 1, 2 or 3, else 0, and pumps the opening player (`00184880`) while it is 1 |
| `moviecancel` | `0x036E` | `0033FEC0` (→ `0035B720`) / `00357300` / `0033FA20` | asks the player to stop, waits while the status is 1 to 3, then ends |
| `movieend` | `0x036D` | `0033FA20` → `0035B8D0` | stops the player, frees the buffer, clears busy bit 16 and switches the field systems back on |

The player object at `01F81218` keeps its state at `+4`: 0 idle, 1 opening, 2 ready, 3 playing,
4 the last 233 ms, 5 ending, 6 the skip fade. A script therefore reads "finished" from the last
frames onward.

### Skips

Skip slots are 16-byte entries at `022CB730`, indexed `index + manager × 8`: `+0` bit, `+1` mask
index, `+2` state, `+4` record id, `+8` executed, `+0xC` armed. `skipstart(i)` (`0x051A`,
`0034D3A0` → `00360980`) clears user-control denials 13 and 19, sets state 1 and armed, sets the
bit in `022CB9C0` and clears it in `022CB9D8`. `skipcheck(i)` (`0x051C`) returns the executed word
through `003604A0`.

`skipexec(i)` (`0x0539`, `0034ECF0` → `00360710`) runs only when the manager's skip mask is
clear and the entry is armed: state 2, executed 1, busy bit 15, the teardown of the manager's
sound, effects and presentation, and finally the mask bit `0026A5B0(manager, 1, i)` that ends
the waits ([native commands](native-commands.md)).

`skipend(i)` (`0x051B`, poll `0034DB30`)
releases an entry that was not executed at once (`00360A20`); otherwise it waits through four
stages (`0025C070`, `003608D0`, `00360D60`, the resource queue idle through `002F1A30` and
`0032E520`), releases, and waits one more stage on `00229EB0`.

### Event party modes and event time stop

`seteventpartymode(v)` (`0x050F`, `0037D120`) writes bit 2 of the party block word
`[02EBF190] + 0x5B04` and `seteventparty2mode` (`0x0514`) bit 3; `geteventpartymode` (`0x0510`,
`00355FE0`) returns whether the mode ladder `0030D9A0` reads 4, and `geteventpartymodebit`
(`0x0513`) returns bit 2. `seteventtimestop(v)` (`0x0398`, `0034DC30`) raises stop request 11
through `002273B0` or releases it through `002260C0` when held ([time stop and
freeze](../Engine-Core/time-stop-and-freeze.md)).

### The world lock

The lock is stop request 6 of the registry. `00263230(actor, 1)` takes it when no take is active
(`02099DB4` at 0) and `0209A2A8` is set: `00226BE0(6, 0, 0, 0, 4, flag)` with the flag
`00377700() != 0`, then the counter at manager `+0x1E0` is raised and summed into `02099DB4` and
the taken actor's battle action is cancelled. The request engine reaches it with flag 1: the talk
filer passes it for slot 2, so every conversation takes the lock when its script starts
([script requests](script-requests.md)).

`00263230` also turns the controlled character toward the taken actor: `002EC2C0(focus, record
+0x20)` for a class-1 actor or `002EBFA0(focus, manager, ordinal, 0x30B)` for class 3, then
`002EC380(focus, 2, 6.0)`, `002EBE50(focus, 1)`, `002E8EE0` and `002ED040(focus, 1)`. That is the
turn the player sees at the start of every talk.

`00263050(actor, 1)` is the release: it lowers the
counter and, at 0, runs the field hold `00263480` and `00225CD0(6, 4)`.

`00377700` returns 1 only when the field byte and the save byte are both clear: the field byte is
`[02ADD100] + 8 + 3 × field + 2`, read only when the table exists and the field index is below
its count at `+4`, otherwise taken as clear; the save byte is the persistent `+0x1062` bit 0
(`00314A60`, set by `setsaverambattlestatus(0)`).

The field hold `00263480(actor, mode)` raises request 5
for mode 0, 4 for mode 1 and 7 for mode 2 with the actor as a one-entry list, passing
`02099DE7 == 0` as the flag; with the hold bytes `02099DE5` and `02099DE6` both clear it releases
5, 4 and 7 instead. The talk filer sets `02099DE7` to `00377700() == 0` and `02099DE5` to 1; the
release resets them.

Every request locks every actor of managers 0 to 2 and then releases the configured rows: the
focus actor always, the other party members only when the flag is 0, and the non-party types by
their configuration. A locked actor keeps the request's bit in `+0x10C`, and the interpreter gate
refuses its script every frame ([script interpreter](script-interpreter.md)), which is why
townspeople stand still while the player talks and why the talk partner, released by the request's
own list, keeps acting.

## Layouts

```
scene manager     02098E10 + m × 0x288: +0x10 bit 0 active, +0x11 bit 3 loading, +0x13 busy, +0x1E0 lock count
pending-load mask 022C6E48 + m × 8 (u64): bit 0 = the start hold
unload request    022C6D20 + m (u8)
capture binding   actor +0x18 u8 state (1 captured, 2 capturer), +0x19 u8 other manager, +0x1A u16 other id
skip entry        022CB730 + 16 × (i + m × 8): +0 bit, +1 mask index, +2 state, +4 record id, +8 executed, +0xC armed
skip masks        022CB9C0 armed, 022CB9D8 executed (u32 per mask index); 02099011 + m × 0x288 the manager's skip mask
movie player      01F81218: +4 state 0..6
party block       [02EBF190] + 0x5B04: bit 2 event party mode, bit 3 event party mode 2
hold bytes        02099DE2 event switch, 02099DE5/02099DE6 hold, 02099DE7 flag; 02099DB4 active takes
```

## Shipped data

| Fact | Value |
|---|---|
| scene managers | 3 (1 to 3) beside the zone's manager 0 |
| `capturepc` uses in the US scripts | 8,353; `releasepc` 8,632 |
| `startscene` uses | 3,789; `seteventtimestop` 4,725; `hideparty` 1,539 |
| `eventread_e8` / `eventplay_ec` / `eventsync_ee` uses | 596 / 567 / 553 |
| skip verbs | `skipstart` 292, `skipend` 291, `skipcheck` 237, `skipexec` 19 |
| movie status values a script sees | 1 opening, 2 ready, 3 playing; 0 otherwise |

## Operations

Per scene: load (one request), wait, release the hold, run, wait for the manager to idle, dispose.
Per capture: one binding write on each record and one action cancel. Per lock take: one registry
request over managers 0 to 2 and its release.

## State

The three scene managers' active, busy and loading bits, the pending-load masks, the capture
bindings in every actor record, the skip table and masks, the movie player state, the party block
mode word, and the lock counter with the hold bytes.

## Modding notes

- A scene cannot start before `eventplay` clears the hold, however early its files finish loading.
- `capturepc(−1)` always takes the character the player controls; a script that needs a specific
  member passes its slot.
- `hideparty` hides bodies only; the actors keep running and can still be captured.
- `releasepc` rebuilds the body pointers from the record's class, so a capturer that swapped them
  is not restored to a saved state but to the class default.
- A conversation takes the world lock with the flag from `00377700`: on a field whose record bit
  is set, or after `setsaverambattlestatus(0)`, the other party members keep moving.

## Related

- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the registry behind the lock.
- [Script requests](script-requests.md): the talk filer and the start flag.
- [Native commands](native-commands.md): the skip mask that ends waits.
- [Party verbs](party-verbs.md): the summon party switches.
