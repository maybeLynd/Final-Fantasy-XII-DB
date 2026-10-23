---
title: "World lock: the stop request that freezes everyone but the scene or the talk, the field hold, and event time stop"
kind: "system"
category: "Scripts and script commands"
addresses: "0x0034DC30, 0x00263230, 0x00263050, 0x00263480, 0x00226BE0, 0x00225CD0, 0x00377700, 0x00314A60, 0x02099DE7, 0x02099DB4"
---

## What the player sees

While a talk or scene runs, the rest of the world holds still: nobody else starts a conversation and nothing else
moves.

## How it works

### The world lock

The lock is stop request 6 of the registry. `0x00263230(actor, 1)` takes it when no take is active
(`0x02099DB4` at 0) and `0x0209A2A8` is set: `0x00226BE0(6, 0, 0, 0, 4, flag)` with the flag
`0x00377700() != 0`, then the counter at manager `+0x1E0` is raised and summed into `0x02099DB4` and
the taken actor's battle action is cancelled. The request engine reaches it with flag 1: the talk
filer passes it for slot 2, so every conversation takes the lock when its script starts
([script requests](script-requests.md)).

`0x00263230` also turns the controlled character toward the taken actor: `0x002EC2C0(focus, record
+0x20)` for a class-1 actor or `0x002EBFA0(focus, manager, ordinal, 0x30B)` for class 3, then
`0x002EC380(focus, 2, 6.0)`, `0x002EBE50(focus, 1)`, `0x002E8EE0` and `0x002ED040(focus, 1)`. That is the
turn the player sees at the start of every talk.

`0x00263050(actor, 1)` is the release: it lowers the
counter and, at 0, runs the field hold `0x00263480` and `0x00225CD0(6, 4)`.

`0x00377700` returns 1 only when the field byte and the save byte are both clear: the field byte is
`[0x02ADD100] + 8 + 3 × field + 2`, read only when the table exists and the field index is below
its count at `+4`, otherwise taken as clear; the save byte is the persistent `+0x1062` bit 0
(`0x00314A60`, set by `setsaverambattlestatus(0)`).

The field hold `0x00263480(actor, mode)` raises request 5
for mode 0, 4 for mode 1 and 7 for mode 2 with the actor as a one-entry list, passing
`0x02099DE7 == 0` as the flag; with the hold bytes `0x02099DE5` and `0x02099DE6` both clear it releases
5, 4 and 7 instead. The talk filer sets `0x02099DE7` to `0x00377700() == 0` and `0x02099DE5` to 1; the
release resets them.

Every request locks every actor of managers 0 to 2 and then releases the configured rows: the
focus actor always, the other party members only when the flag is 0, and the non-party types by
their configuration. A locked actor keeps the request's bit in `+0x10C`, and the interpreter gate
refuses its script every frame ([script interpreter](script-interpreter.md)), which is why
townspeople stand still while the player talks and why the talk partner, released by the request's
own list, keeps acting.

### Event time stop

`seteventtimestop(v)` (`0x0398`, `0x0034DC30`) raises stop request 11
through `0x002273B0` or releases it through `0x002260C0` when held ([time stop and
freeze](../Engine-Core/time-stop-and-freeze.md)).

## Layouts

Globals:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x2099DE5` | `u8` | hold1 | field hold byte |
| `+0x2099DE6` | `u8` | hold2 | field hold byte |
| `+0x2099DE7` | `u8` | holdFlag | the flag the hold passes |
| `+0x2099DB4` | `i32` | activeTakes | sum of the managers' lock counts |

## Shipped data

| Fact | Value |
|---|---|
| `seteventtimestop` uses | 4,725 |

## Operations

Per lock take: one registry request over managers 0 to 2 and its release.

## State

The lock counter and the hold bytes.

## Modding notes

- A conversation takes the world lock with the flag from `0x00377700`: on a field whose record bit
  is set, or after `setsaverambattlestatus(0)`, the other party members keep moving.

## Related

- [Event scenes](event-scenes.md): loading, playing and disposing a scene, movies and skips.
- [The party during scenes](party-during-scenes.md): hiding, capturing and the summon group.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the registry behind the lock.
- [Script requests](script-requests.md): the talk filer and the start flag.
