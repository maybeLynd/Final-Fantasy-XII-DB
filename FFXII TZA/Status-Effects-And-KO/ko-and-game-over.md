---
title: "KO and Game Over: what happens to a fallen unit's body, how it stands up again, and when a party wipe ends the game"
kind: "system"
category: "Status effects and KO"
addresses: "0x00300FC0, 0x002372E0, 0x00237260, 0x002371B0, 0x00237140, 0x00234590, 0x0035C7B0, 0x003250F0, 0x00319F50, 0x003125E0, 0x00233F70, 0x00300E40, 0x00301140, 0x00336E40"
---

## What the player sees

- A unit at 0 HP plays its fall, and a hovering one drops to the ground.
- When every main character is down, the game stops and Game Over begins.
- When the four fighting characters are down but a reserve member is still standing, the game does not end:
  it opens a separate screen first.
- When the character under control falls, control is locked until a leader is standing again.
- A revived character stands up where it lay; one whose body had been hidden reappears beside the character
  under control.

## How it works

### The defeat cleanup

Adding KO, Stone or X-Zone runs `0x00300FC0(unit, 0)` ([Gaining and losing statuses](status-changes.md)), and
tearing a unit down runs `0x00300FC0(unit, 1)` (`0x00300E59`). It does (`0x00300FC0`-`0x00301132`):

1. **A summoned Esper** (a party record of type `0x1B`-`0x27`) with argument 0 has its action cancelled
   (`0x003105D0`) and is dismissed (`0x003138D0(0)`), and nothing else happens (`0x00300FD3`-`0x00301005`).
2. **Anyone else** loses its target relations (`0x00310780`), has unit flag bits 1, 19, 20 and 33 and bit 34 cleared,
   and stops moving (`0x0030100D`-`0x00301043`). Then `0x003219D0(type, 0, null, 1)` sets every living enemy's
   grudge against its party type to 1 where it was above 0 (`0x00301048`-`0x0030105E`;
   [Enmity](../Enemy-AI-And-Gambits/enmity.md)).
3. Then the KO-time wipe tests run, below. On a wipe it sets battle flag `0x400` or `0x200`, runs the survivors'
   pass `0x003001D0`, arms the request and recomputes party control with `0x0023B040`
   ([Party leader](../Party/party-leader.md)) (`0x00301063`-`0x003010C0`).
4. Otherwise a fallen summoner sets battle flag `0x800` (`0x002373C0`, `0x003010C5`-`0x003010CE`), and a fallen
   controlled character sets `0x100` and arms request `0x17` (`0x003010D8`-`0x003010F1`).
5. With argument 0, in summon mode, when the fallen unit is the summoner, the Esper is dismissed and party
   control recomputed (`0x003010F6`-`0x00301123`).

The survivors' pass collects the up to four active members still standing and calls `0x002ECEC0` on each
(`0x003001F8`-`0x00300263`).

### The four wipe tests

Each test walks the four active slots (`0x0031B810`) and, for two of them, the nine roster records (`0x00320AB0`).
A unit is down when it has KO, Stone or X-Zone and the field's bit 15 is clear. A main character is a party
record of type 0-6; a guest is a party record of type 7-25. Each test returns 0 when no slot or record exists.

| Test | Returns 1 when | Used |
|---|---|---|
| `0x002372E0` | no main character in the four or in the roster is up | at the KO, latch `0x400` |
| `0x00237260` | none of the four is up and not a guest | at the KO, latch `0x200`; every frame |
| `0x002371B0` | no main character in the four is not torn down, and none in the roster is up | every frame, Game Over |
| `0x00237140` | none of the four that is not a guest is not torn down | every frame, the `0x18` screen |

Torn down is unit flag bit 1, set when a party member's body is torn down (below). So the frame tests count a
fallen character as gone only once its body has been torn down.

### Arming and posting the request

`0x0035C8A0(kind)` arms a request without posting it (`0x0035C8A0`-`0x0035C8DC`):

| Kind | Flag in `0x022C83E8` | Input lock |
|---|---|---|
| `0x0B`, Game Over | `0x02` | `0x00254850(1)`: bit 8 of ten input groups |
| `0x18`, the active party down | `0x01` | `0x00254940(1)` |
| `0x17`, the controlled character down | `0x10` | `0x002548F0(1)` |

While Game Over is armed (bit 1 of `0x022C83E8`, read by `0x0035C740`) or a mode request is stored in `0x0215F1A0`
(`0x002E12D0`), or `0x00228380` answers non-zero (`0x00253CC3`), the input arbiter `0x00253C70` returns before reading
any field button (`0x00253C97`-`0x00253CCC`,
[Controls](../Controls-And-Input/controls.md)).

Every field frame, `0x00234590` posts one (`0x002345EF`-`0x0023461F`). Unless a request is pending (`0x0035C700`: flag
`0x100`, mode `0x02092730` already `0x0B` or `0x18`, or `0x002E12D0`) or a special-sequence scene is running
(`0x00306BB0`, [Field frame](../Engine-Core/frame-update-order.md)), it
posts `0x0B` when `0x002371B0` is 1, else `0x18` when `0x00237140` is 1, through `0x0035C7A0`, which calls
`0x0035C7B0(kind, 1)` (`0x0023461F`, `0x0035C7A5`):

- **`0x0B`**: flag `0x100`; `0x00227370` halts the actors by starting time-stop request 22 (`0x00226BE0(0x16, ...)`,
  [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), unless bit 22 of `0x01FD46D4` is set; `0x002E1B10(0x0B, 0)`
  stores the mode request at `0x0215F1A0`-`0x0215F1A8`, unless `0x0215F1A1` refuses it; then the arming above
  (`0x0035C806`-`0x0035C870`).
- **`0x18`**: `0x00254B40` opens the mode-`0x18` screen, then the arming (`0x0035C7FD`, `0x0035C832`-`0x0035C844`).

`0x0035C7B0(0x0B)` has one other caller, for a wipe that lands outside the field frame: `0x0027EFA0`, run from the
main loop through `0x00254E50` (`0x0022AC73`, `0x00254E61`). It posts Game Over when `0x002805D0` allows it: Game Over is
armed (`0x022C83E8` bit 1, `0x0035C740`), the screen object's `+0xD4` is 0, and the mode `0x02092730` is 6, 10,
`0x0F`, `0x11`, `0x12` or `0x13`, or 2 with its `+0xC4` state past `0x42`. It then also runs `0x00252B40(0x0B)`.

Later in the same frame the field frame keeps three latches current (`0x0023471C`-`0x0023483F`): `0x200` from
`0x00237260`, arming `0x18` when it rises; `0x100` while the party leader is missing or down, arming `0x17` when it
rises and disarming it with `0x0035C8E0` when it falls; and `0x800` from the summoner test. The falling edge of
`0x200` also calls `0x0035C8E0`, with `0x18`, which that function ignores, so the `0x18` arming stays
(`0x0023475B`).

### The two signals from the fall

A fallen body is torn down only after two unit flag bits are set:

1. **Bit 33, the fall has played.** `0x003250F0` sets it when a unit with flag bit 2 gets animation event `0x2007`,
   `0x2008`, `0x200C` or `0x200E` (`0x00325136`-`0x0032519F`). Those are the death clips the HP write and the Stone
   and X-Zone arms start ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)).
2. **Bit 34, hide the body.** `0x00319F50` sets it on actor timeline code 4 for a unit with KO, Stone or X-Zone
   without the field's bit 15, together with flag bit 10, and on code 6 for any unit, then refreshes visibility
   (`0x0031A100`-`0x0031A159`, `0x0031A198`-`0x0031A1A4`). Code 4 is ignored while the unit is carrying out Revive
   (`0xAE`) on itself.

Bit 33 has a second setter: `0x00319F50` sets it on actor timeline code 2, which first sets the HP of a unit that is
not down to 0 (`0x00300520`), unless it is carrying out Revive on itself (`0x0031A042`-`0x0031A0AA`).

Timeline codes reach `0x00319F50` through `0x002EB740` from two senders: the battle effect program `0x003B8670`
(`0x003B887D`, `0x003B8988`, `0x003B8A1C`, `0x003B9208`), and `0x002FC010`, which sends the queued codes of a finished entry
of the list `0x02EC3D60` and then code 0 (`0x002FC103`, `0x002FC158`).

The fall also starts an effect. On action timeline events 2 and 6, a unit with KO, Stone or X-Zone starts battle
effect `0x78` on itself and keeps its handle in `+0x74`, unless it is an enemy whose class row byte
`+0x18 & 0x0E` is 4 (`0x003255DB`-`0x00325649`). Event 9 sets bit 19, the drop of a hovering body
(`0x003256FB`).

### Hiding the body

`0x003125E0(unit)` builds the hide mask, and the model is shown only while it is 0 (`0x003125E0`-`0x003126DD`,
`0x00312700`). For an active unit:

| Mask bit | Condition |
|---|---|
| `0x10` | KO, Stone or X-Zone without the field's bit 15, and torn down (flag bit 1) |
| `0x20` | bit 34 |
| `0x02`, `0x04`, `0x08` | flag bits 11, 10, 9 |
| `0x40`, `0x80` | an enemy whose spawn record has bit 4 or bit 3 |

The unit frame refreshes it every frame (`0x00234034`, `0x00234112`, `0x00234133`). The switch is on or off; there is
no fade.

`0x003126E0(unit)` returns 1 while the mask is 0 (`0x003126E4`-`0x003126ED`). `0x00328530` asks it for the
target and builds its target line through `0x00290320` only when it returns 1 (`0x00328555`-`0x003285A0`).

### The fallen unit's frame

`0x00233F70` runs a different frame for an active unit with KO, Stone or X-Zone that is not torn down
(`0x00234039`-`0x00234112`):

- an enemy whose class row byte `+0x18 & 0x0E` is 4 only keeps its position up to date;
- anyone else sets battle flag 2 (unless a group completion is pending), stops moving, runs the drop below, and is
  torn down with `0x00300E40(unit, 0)` once bits 33 and 34 are both set and the presentation test on its slot
  `0x0030CA50` allows it: `0x00322310` non-zero, or `0x003228E0` zero (`0x002340BC`-`0x00234100`).

The drop `0x003057D0` runs while the unit is down, has bit 19 and not bit 20, and its actor passes `0x00264490`. Each
frame it lowers the body's height offset by an amount that grows by 0.02 per frame (`+0x19C`), stops at 0, and
then sets bit 20 (`0x003057E5`-`0x00305896`).

### Tearing down

`0x00300E40(unit, keep)` runs the defeat cleanup with argument 1, cancels the action and clears the issued command,
sets bit 53 and removes the unit's effect `+0x74` (`0x00300E54`-`0x00300ED5`). Then:

- **A party member** keeps its unit. With no attackers left (`+0xEA0` 0) it also runs `0x00322050` and `0x00301310`
  and clears bit 26. Then bits 34, 19, 20 and 33 are cleared and **bit 1 is set**, and visibility is refreshed,
  so the hide mask's `0x10` keeps the model hidden (`0x00300EEE`-`0x00300F45`).
- **Anyone else** loses its definition (`0x0023A570(unit, 0xFFFF)`) and its actor (`0x0025AB30`, `0x002697E0`), unless a
  spawn group holds it (`0x00300F5D`-`0x00300FA4`).

### Standing up again

Removing the last of KO, Stone and X-Zone runs `0x00301140(unit)` (`0x0030E811`;
[Gaining and losing statuses](status-changes.md)). With none of the three left (`0x00301146`-`0x003012F6`):

1. A body that is hidden, and not already placed (flag bit 26), is placed with `0x00311F70` (`0x0030116B`-`0x00301185`).
   The hidden test is `0x002E9600(actor)` returning 0; it returns bit 3 of byte `+0x10` of `[actor+0xC0]`
   for an actor whose byte `+3` has `0x60` in its top three bits, and 0 otherwise (`0x002E9600`-`0x002E9623`).
2. The actor is refreshed from the definition, the action cancelled and the issued command cleared.
3. Revive effect `0x7B` starts on the unit (`0x003011F5`-`0x00301216`), and the re-plan set is installed
   ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)).
4. The stand-up clip, event `0x200D`, plays (`0x0030127A`-`0x00301282`); it clears bit 24 when it lands (`0x0032517C`).
5. Bits 34, 8-10, 1, 19, 20 and 33 are cleared, bits 24 and 30 set, the old effect removed, and visibility
   refreshed, so the model is shown.

`0x00311F70` asks `0x00336E40` for a point and moves and turns the actor to it (`0x00311FCE`-`0x003120D5`). Without a
reference unit, `0x00336E40` returns the unit's own position when `0x022C7D10` is 0; otherwise the anchor
`0x022C7DD0` for the party leader, and a point near the anchor for anyone else (`0x00336F79`-`0x00336F98`). In summon
mode `0x00311F70` asks for mode 1 instead (`0x00311FAB`-`0x00311FC9`). `0x0033CA00`
records the anchor from the actor of the character under control (`0x0033CA15`-`0x0033CAF2`).

## Modding notes

- Game Over is posted only through `0x0035C7B0`, from the field frame and from `0x0027EFA0`; refusing `0x0B` there
  keeps the game running, but the KO-time arming has already locked input.
- A party member's body is never removed, only hidden; a revive shows it again.

## Related

- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write that adds KO and starts the death clip.
- [Gaining and losing statuses](status-changes.md) - the KO, Stone and X-Zone arms.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - what a fallen enemy pays.
- [Field frame](../Engine-Core/frame-update-order.md) - the frame that
  posts the request.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md) - the enmity removed at a fall.
