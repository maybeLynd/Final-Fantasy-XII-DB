---
title: "KO and Game Over: what happens to a fallen unit's body, how it stands up again, and when a party wipe ends the game"
kind: "system"
category: "Status effects and KO"
addresses: "00300FC0, 002372E0, 00237260, 002371B0, 00237140, 00234590, 0035C7B0, 003250F0, 00319F50, 003125E0, 00233F70, 00300E40, 00301140, 00336E40"
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

Adding KO, Stone or X-Zone runs `00300FC0(unit, 0)` ([Gaining and losing statuses](status-changes.md)), and
tearing a unit down runs `00300FC0(unit, 1)` (`00300E59`). It does (`00300FC0`-`00301132`):

1. **A summoned Esper** (a party record of type `0x1B`-`0x27`) with argument 0 has its action cancelled
   (`003105D0`) and is dismissed (`003138D0(0)`), and nothing else happens (`00300FD3`-`00301005`).
2. **Anyone else** loses its target relations (`00310780`), has unit flag bits 1, 19, 20 and 33 and bit 34 cleared,
   and stops moving (`0030100D`-`00301043`). Then `003219D0(type, 0, null, 1)` sets every living enemy's
   grudge against its party type to 1 where it was above 0 (`00301048`-`0030105E`;
   [Enmity](../Enemy-AI-And-Gambits/enmity.md)).
3. Then the KO-time wipe tests run, below. On a wipe it sets battle flag `0x400` or `0x200`, runs the survivors'
   pass `003001D0`, arms the request and recomputes party control (`00301063`-`003010C0`).
4. Otherwise a fallen summoner sets battle flag `0x800` (`002373C0`, `003010C5`-`003010CE`), and a fallen
   controlled character sets `0x100` and arms request `0x17` (`003010D8`-`003010F1`).
5. With argument 0, in summon mode, when the fallen unit is the summoner, the Esper is dismissed and party
   control recomputed (`003010F6`-`00301123`).

The survivors' pass collects the up to four active members still standing and calls `002ECEC0` on each
(`003001F8`-`00300263`).

### The four wipe tests

Each test walks the four active slots (`0031B810`) and, for two of them, the nine roster records (`00320AB0`).
A unit is down when it has KO, Stone or X-Zone and the field's bit 15 is clear. A main character is a party
record of type 0-6; a guest is a party record of type 7-25. Each test returns 0 when no slot or record exists.

| Test | Returns 1 when | Used |
|---|---|---|
| `002372E0` | no main character in the four or in the roster is up | at the KO, latch `0x400` |
| `00237260` | none of the four is up and not a guest | at the KO, latch `0x200`; every frame |
| `002371B0` | no main character in the four is not torn down, and none in the roster is up | every frame, Game Over |
| `00237140` | none of the four that is not a guest is not torn down | every frame, the `0x18` screen |

Torn down is unit flag bit 1, set when a party member's body is torn down (below). So the frame tests count a
fallen character as gone only once its body has been torn down.

### Arming and posting the request

`0035C8A0(kind)` arms a request without posting it (`0035C8A0`-`0035C8DC`):

| Kind | Flag in `022C83E8` | Input lock |
|---|---|---|
| `0x0B`, Game Over | `0x02` | `00254850(1)`: bit 8 of ten input groups |
| `0x18`, the active party down | `0x01` | `00254940(1)` |
| `0x17`, the controlled character down | `0x10` | `002548F0(1)` |

Every field frame, `00234590` posts one (`002345EF`-`0023461F`). Unless a request is pending (`0035C700`: flag
`0x100`, mode `02092730` already `0x0B` or `0x18`, or `002E12D0`) or a special-sequence scene is running
(`00306BB0`, [Field frame](../Engine-Core/frame-update-order.md)), it
posts `0x0B` when `002371B0` is 1, else `0x18` when `00237140` is 1, through `0035C7A0`, which calls
`0035C7B0(kind, 1)` (`0023461F`, `0035C7A5`):

- **`0x0B`**: flag `0x100`; `00227370` halts the actors, unless bit 22 of `01FD46D4` is set; `002E1B10(0x0B, 0)`
  stores the mode request at `0215F1A0`-`0215F1A8`, unless `0215F1A1` refuses it; then the arming above
  (`0035C806`-`0035C870`).
- **`0x18`**: `00254B40` opens the mode-`0x18` screen, then the arming (`0035C7FD`, `0035C832`-`0035C844`).

`0035C7B0(0x0B)` has one other caller, for a wipe that lands outside the field frame: `0027EFA0`, run from the
main loop through `00254E50` (`0022AC73`, `00254E61`). It posts Game Over when `002805D0` allows it: Game Over is
armed (`022C83E8` bit 1, `0035C740`), the screen object's `+0xD4` is 0, and the mode `02092730` is 6, 10,
`0x0F`, `0x11`, `0x12` or `0x13`, or 2 with its `+0xC4` state past `0x42`. It then also runs `00252B40(0x0B)`.

Later in the same frame the field frame keeps three latches current (`0023471C`-`0023483F`): `0x200` from
`00237260`, arming `0x18` when it rises; `0x100` while the party leader is missing or down, arming `0x17` when it
rises and disarming it with `0035C8E0` when it falls; and `0x800` from the summoner test. The falling edge of
`0x200` also calls `0035C8E0`, with `0x18`, which that function ignores, so the `0x18` arming stays
(`0023475B`).

### The two signals from the fall

A fallen body is torn down only after two unit flag bits are set:

1. **Bit 33, the fall has played.** `003250F0` sets it when a unit with flag bit 2 gets animation event `0x2007`,
   `0x2008`, `0x200C` or `0x200E` (`00325136`-`0032519F`). Those are the death clips the HP write and the Stone
   and X-Zone arms start ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)).
2. **Bit 34, hide the body.** `00319F50` sets it on actor timeline code 4 for a unit with KO, Stone or X-Zone
   without the field's bit 15, together with flag bit 10, and on code 6 for any unit, then refreshes visibility
   (`0031A100`-`0031A159`, `0031A198`-`0031A1A4`). Code 4 is ignored while the unit is carrying out Revive
   (`0xAE`) on itself.

Bit 33 has a second setter: `00319F50` sets it on actor timeline code 2, which first sets the HP of a unit that is
not down to 0 (`00300520`), unless it is carrying out Revive on itself (`0031A042`-`0031A0AA`).

Timeline codes reach `00319F50` through `002EB740` from two senders: the battle effect program `003B8670`
(`003B887D`, `003B8988`, `003B8A1C`, `003B9208`), and `002FC010`, which sends the queued codes of a finished entry
of the list `02EC3D60` and then code 0 (`002FC103`, `002FC158`).

The fall also starts an effect. On action timeline events 2 and 6, a unit with KO, Stone or X-Zone starts battle
effect `0x78` on itself and keeps its handle in `+0x74`, unless it is an enemy whose class row byte
`+0x18 & 0x0E` is 4 (`003255DB`-`00325649`). Event 9 sets bit 19, the drop of a hovering body
(`003256FB`).

### Hiding the body

`003125E0(unit)` builds the hide mask, and the model is shown only while it is 0 (`003125E0`-`003126DD`,
`00312700`). For an active unit:

| Mask bit | Condition |
|---|---|
| `0x10` | KO, Stone or X-Zone without the field's bit 15, and torn down (flag bit 1) |
| `0x20` | bit 34 |
| `0x02`, `0x04`, `0x08` | flag bits 11, 10, 9 |
| `0x40`, `0x80` | an enemy whose spawn record has bit 4 or bit 3 |

The unit frame refreshes it every frame (`00234034`, `00234112`, `00234133`). The switch is on or off; there is
no fade.

`003126E0(unit)` returns 1 while the mask is 0 (`003126E4`-`003126ED`). `00328530` asks it for the
target and builds its target line through `00290320` only when it returns 1 (`00328555`-`003285A0`).

### The fallen unit's frame

`00233F70` runs a different frame for an active unit with KO, Stone or X-Zone that is not torn down
(`00234039`-`00234112`):

- an enemy whose class row byte `+0x18 & 0x0E` is 4 only keeps its position up to date;
- anyone else sets battle flag 2 (unless a group completion is pending), stops moving, runs the drop below, and is
  torn down with `00300E40(unit, 0)` once bits 33 and 34 are both set and the presentation test on its slot
  `0030CA50` allows it: `00322310` non-zero, or `003228E0` zero (`002340BC`-`00234100`).

The drop `003057D0` runs while the unit is down, has bit 19 and not bit 20, and its actor passes `00264490`. Each
frame it lowers the body's height offset by an amount that grows by 0.02 per frame (`+0x19C`), stops at 0, and
then sets bit 20 (`003057E5`-`00305896`).

### Tearing down

`00300E40(unit, keep)` runs the defeat cleanup with argument 1, cancels the action and clears the issued command,
sets bit 53 and removes the unit's effect `+0x74` (`00300E54`-`00300ED5`). Then:

- **A party member** keeps its unit. With no attackers left (`+0xEA0` 0) it also runs `00322050` and `00301310`
  and clears bit 26. Then bits 34, 19, 20 and 33 are cleared and **bit 1 is set**, and visibility is refreshed,
  so the hide mask's `0x10` keeps the model hidden (`00300EEE`-`00300F45`).
- **Anyone else** loses its definition (`0023A570(unit, 0xFFFF)`) and its actor (`0025AB30`, `002697E0`), unless a
  spawn group holds it (`00300F5D`-`00300FA4`).

### Standing up again

Removing the last of KO, Stone and X-Zone runs `00301140(unit)` (`0030E811`;
[Gaining and losing statuses](status-changes.md)). With none of the three left (`00301146`-`003012F6`):

1. A body that is hidden, and not already placed (flag bit 26), is placed with `00311F70` (`0030116B`-`00301185`).
   The hidden test is `002E9600(actor)` returning 0; it returns bit 3 of byte `+0x10` of `[actor+0xC0]`
   for an actor whose byte `+3` has `0x60` in its top three bits, and 0 otherwise (`002E9600`-`002E9623`).
2. The actor is refreshed from the definition, the action cancelled and the issued command cleared.
3. Revive effect `0x7B` starts on the unit (`003011F5`-`00301216`), and the re-plan set is installed
   ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)).
4. The stand-up clip, event `0x200D`, plays (`0030127A`-`00301282`); it clears bit 24 when it lands (`0032517C`).
5. Bits 34, 8-10, 1, 19, 20 and 33 are cleared, bits 24 and 30 set, the old effect removed, and visibility
   refreshed, so the model is shown.

`00311F70` asks `00336E40` for a point and moves and turns the actor to it (`00311FCE`-`003120D5`). Without a
reference unit, `00336E40` returns the unit's own position when `022C7D10` is 0; otherwise the anchor
`022C7DD0` for the party leader, and a point near the anchor for anyone else (`00336F79`-`00336F98`). In summon
mode `00311F70` asks for mode 1 instead (`00311FAB`-`00311FC9`). `0033CA00`
records the anchor from the actor of the character under control (`0033CA15`-`0033CAF2`).

## Modding notes

- Game Over is posted only through `0035C7B0`, from the field frame and from `0027EFA0`; refusing `0x0B` there
  keeps the game running, but the KO-time arming has already locked input.
- A party member's body is never removed, only hidden; a revive shows it again.

## Related

- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write that adds KO and starts the death clip.
- [Gaining and losing statuses](status-changes.md) - the KO, Stone and X-Zone arms.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - what a fallen enemy pays.
- [Field frame](../Engine-Core/frame-update-order.md) - the frame that
  posts the request.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md) - the enmity removed at a fall.
