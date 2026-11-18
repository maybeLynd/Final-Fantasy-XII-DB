[Home](../../README.md) / [Status effects and KO](README.md) / KO and Game Over

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| KO and Game Over: what happens to a fallen unit's body, how it stands up again, and when a party wipe ends the game | system | Status effects and KO | KO and MP | What follows KO, Stone or X-Zone once the status has landed: the defeat cleanup and the four party-wipe tests it and the field frame run, the latches and the Game Over request, the two signals from the death animation and its effect that decide when a body is hidden and torn down, the drop of a hovering body, what tearing down does to a party member and to anyone else, and how a revive stands the body up where it lay or beside the controlled character. | 0x00300FC0, 0x002372E0, 0x00237260, 0x002371B0, 0x00237140, 0x00234590, 0x0035C7B0, 0x003250F0, 0x00319F50, 0x003125E0, 0x00233F70, 0x00300E40, 0x00301140, 0x00336E40 |

## What the player sees

- A unit at 0 HP plays its fall, and a hovering one drops to the ground.
- When every main character is down, the game stops and Game Over begins.
- When the four fighting characters are down but a reserve member is still standing, the game does not end:
  it opens a separate screen first.
- When the character under control falls, control is locked until a leader is standing again.
- A revived character stands up where it lay; one whose body had been hidden reappears beside the character
  under control.

A fallen body is put away only after two signals: its death animation has played, and a separate hide signal has
arrived from the battle timeline. Each field frame the game checks the four fighting characters, and when every main
character among them is put away and no main character in reserve is standing, it posts Game Over.

## How it works

### The defeat cleanup

Adding KO, Stone or X-Zone runs `0x00300FC0(unit, 0)` ([Gaining and losing statuses](status-changes.md)), and
tearing a unit down runs `0x00300FC0(unit, 1)` (`0x00300E59`). It does (`0x00300FC0`-`0x00301132`):

1. **A summoned Esper** (a party record of type `0x1B`-`0x27`) with argument 0 has its action cancelled
   (`0x003105D0`) and is dismissed (`0x003138D0(0)`), and nothing else happens (`0x00300FD3`-`0x00301005`).
2. **Anyone else** loses its target relations (`0x00310780`), has unit flag bits `0x2`, `0x80000`, `0x100000` and
   `0x200000000` and bit `0x400000000` cleared, stops aiming at another actor (`0x002ED180` with its handle `+8`,
   which runs `0x00512EE0` on the aim block `+0x650` of its render record when that record is in use, `0x00301015`),
   and stops moving (`0x0030100D`-`0x00301043`).
3. Then `0x003219D0(type, 0, null, 1)` sets every living enemy's
   grudge against its party type to 1 where it was above 0 (`0x00301048`-`0x0030105E`;
   [Enmity](../Enemy-AI-And-Gambits/enmity.md)).
4. Then the KO-time wipe tests run, below. On a wipe it sets battle flag `0x400` or `0x200`, runs the survivors'
   pass `0x003001D0`, arms the request and recomputes party control with `0x0023B040`
   ([Party leader](../Party/party-leader.md)) (`0x00301063`-`0x003010C0`).
5. Otherwise a fallen summoner sets battle flag `0x800` (`0x002373C0`, `0x003010C5`-`0x003010CE`), and a fallen
   controlled character sets `0x100` and arms request `0x17` (`0x003010D8`-`0x003010F1`).
6. With argument 0, in summon mode, when the fallen unit is the summoner, the Esper is dismissed and party
   control recomputed (`0x003010F6`-`0x00301123`).

The survivors' pass collects the up to four active members still standing and calls `0x002ECEC0` on each
(`0x003001F8`-`0x00300263`).

### The four wipe tests

Each test walks the four active slots (`0x0031B810`) and, for two of them, the nine roster records (`0x00320AB0`).
A unit is down when it has KO, Stone or X-Zone and the field's bit `0x8000` is clear. A main character is a party
record of type 0-6; a guest is a party record of type 7-25. Each test returns 0 when no slot or record exists.

| Test | Returns 1 when | Used |
|---|---|---|
| `0x002372E0` | no main character in the four or in the roster is up | at the KO, latch `0x400` |
| `0x00237260` | no member of the four who is not a guest is up | at the KO, latch `0x200`; every frame; the Escape Mode applier `0x00252B60` (`0x00252BA8`), only while input snapshot bit `0x2000000` and bits `0x40`, `0x200` and `0x400` of the action availability mask `0x002E0FA0()` are clear (`0x00252B7A`-`0x00252BA6`): a 1 zeroes the toggle with `force` 1 (`0x00252BAD`-`0x00252BB3`) unless bits `0x1`, `0x4` or `0x8` of `0x0035C6F0()` replace it |
| `0x002371B0` | every main character in the four is torn down, and no main character in the roster is up | every frame, Game Over |
| `0x00237140` | every member of the four who is not a guest is torn down | every frame, the `0x18` screen; closing the Party Menu, `0x00280B70` (`0x00280C00`), while the `0x18` arming is set |

Torn down is unit flag bit `0x2`, set when a party member's body is torn down (below). So the frame tests count a
fallen character as gone only once its body has been torn down.

### Arming and posting the request

`0x0035C8A0(kind)` arms a request without posting it (`0x0035C8A0`-`0x0035C8DC`):

| Kind | Flag in `0x022C83E8` | Input lock |
|---|---|---|
| `0x0B`, Game Over | `0x02` | `0x00254850(1)`: bits `0x1`, `0x2`, `0x4`, `0x10`, `0x20`, `0x40`, `0x80`, `0x200`, `0x800` and `0x100000` of input group 8 (`0x002E1C20`) |
| `0x18`, the active party down | `0x01` | `0x00254940(1)` |
| `0x17`, the controlled character down | `0x10` | `0x002548F0(1)` |

`0x0035C8A0` is called by the defeat cleanup `0x00300FC0` with `0x0B` (`0x00301080`), `0x18` (`0x003010B1`) and `0x17`
(`0x003010F1`), and by the field frame's `0x18` and `0x17` latches (`0x00234736`, `0x002347D9`).

While Game Over is armed (bit `0x2` of `0x022C83E8`, read by `0x0035C740`) or a mode request is stored in `0x0215F1A0`
(`0x002E12D0`), or `0x00228380` answers non-zero (`0x00253CC3`), the input arbiter `0x00253C70` returns before reading
any field button (`0x00253C97`-`0x00253CCC`,
[Controls](../Controls-And-Input/controls.md)).

Every field frame, `0x00234590` posts one (`0x002345EF`-`0x0023461F`). Unless a request is pending (`0x0035C700`: flag
`0x100`, mode `0x02092730` already `0x0B` or `0x18`, or `0x002E12D0`) or a special-sequence scene is running
(`0x00306BB0`, [Field frame](../Engine-Core/frame-update-order.md)), it
posts `0x0B` when `0x002371B0` is 1, else `0x18` when `0x00237140` is 1, through `0x0035C7A0`, which calls
`0x0035C7B0(kind, 1)` (`0x0023461F`, `0x0035C7A5`):

- **`0x0B`**: flag `0x100`; `0x00227370` halts the actors by starting time-stop request 22 (`0x00226BE0(0x16, ...)`,
  [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md)), unless bit `0x400000` of `0x01FD46D4` is set; `0x002E1B10(0x0B, 0)`
  stores the mode request at `0x0215F1A0`-`0x0215F1A8`, unless `0x0215F1A1` refuses it; then the arming above
  (`0x0035C806`-`0x0035C870`).
- **`0x18`**: `0x00254B40` opens the mode-`0x18` screen, then the arming (`0x0035C7FD`, `0x0035C832`-`0x0035C844`).

`0x0035C7B0(0x0B)` has one other caller, for a wipe that lands outside the field frame: `0x0027EFA0`, run from the
main loop through `0x00254E50` (`0x0022AC73`, `0x00254E61`). It posts Game Over when `0x002805D0` allows it: Game Over is
armed (`0x022C83E8` bit `0x2`, `0x0035C740`), the screen object's `+0xD4` is 0, and the mode `0x02092730` is 6, 10,
`0x0F`, `0x11`, `0x12` or `0x13`, or 2 with its `+0xC4` state outside `0x40` to `0x42` (`0x00280630`-`0x0028063C`).
For mode 2 that state is the screen parameter: 0 for Triangle, `0x21` for Select or L3.

It then also runs `0x00252B40(0x0B)`. It calls `0x0035C7B0(0x0B, 0)` (`0x0027EFC8`), so `0x0035C7B0` skips its
`0x002E1B10` write (`0x0035C815`).

`0x0035C7A0(0x0B)` also has a caller outside the field frame: `0x00237D60`, the begin of the script verb `callgameover`
(`0x04D8`, through `0x0033F640`), which calls it (`0x00237D70`) unless `0x0035C700` answers non-zero, and returns 1.

Later in the same frame the field frame keeps three latches current (`0x0023471C`-`0x0023483F`): `0x200` from
`0x00237260`, arming `0x18` when it rises; `0x100` while the party leader is missing or down, arming `0x17` when it
rises and disarming it with `0x0035C8E0` when it falls; and `0x800` from the summoner test. The falling edge of
`0x200` also calls `0x0035C8E0`, with `0x18`, which that function ignores, so the `0x18` arming stays
(`0x0023475B`).

`0x0035C8E0` acts only on `0x17`: it clears bit `0x10` of `0x022C83E8` and jumps to `0x002548F0(0)`; any other kind, `0x0B`
among them, returns at once (`0x0035C8E0`-`0x0035C8F8`). `0x0035D8D0` clears bits `0x1` and `0x10` after calling
`0x00254850(1)` when bit `0x2` is set (`0x0035D958`-`0x0035D96F`).

The `0x18` arming, bit `0x1` of `0x022C83E8`, is re-decided when the Party Menu closes: while it is set, `0x00280B70`
stores `0x00237140()` in it and hands that answer to `0x00254940` through `0x0035C940` (`0x00280BF7`-`0x00280C07`,
`0x0035C940`-`0x0035C955`), so the close leaves it armed only when every member of the four who is not a guest is torn
down by then.

Otherwise, while the `0x17` arming, bit `0x10`, is set (`0x00280C0E`-`0x00280C15`), `0x00280B70` answers 1 when any of the
nine records at `[0x0209AC30] + 0xAC8` whose word `+0x60` is not negative and equals the low byte of `0x003271D0()`, and
whose byte `+0x00` has bit `0x2` clear, has a bit of `0x80000003` in its dword `+0x44`, and 0 otherwise
(`0x00280C17`-`0x00280C5C`); `0x0035C920` stores that answer in bit `0x10` and jumps to `0x002548F0` with it
(`0x0035C920`-`0x0035C938`).

Within an area nothing clears the wipe's battle flag or the Game Over arm. Battle flag `0x400` is set only at the KO
(`0x0030106C`) and cleared only by the boot `0x002368D0`, which stores 0 (`0x002369FB`), and the area init `0x002342F0`,
which, while the up flag `0x02089300` is non-zero (`0x002342F4`-`0x002342FB`), keeps only bits `0x2`-`0x10` and `0xC000` and
up and then sets `0x10` (`0x0023432D`-`0x00234343`).

So after a wipe that sets battle flag `0x400`, the battle-wide mask of `0x0030B770` has bit `0x4`
(`0x0030B7B4`-`0x0030B7BE`), and `0x0030B9B0` refuses every change it gates, for any target and source
(`0x0030B9E2`-`0x0030B9F6`; [status changes](status-changes.md)), until the area init `0x002342F0`, with the up flag set, or
the boot `0x002368D0` clears it. Its six direct calls are at `0x0030060F`, `0x00301E61`, `0x00307695`, `0x0030E42C`, `0x00311360`
and `0x00319257`, and each branches away on that answer.

The Game Over arm, bit `0x2` of `0x022C83E8`, is cleared only at boot, by `0x0035C560`, which zeroes the `0x23C8` bytes
from `0x022C8060` and then sets bit `0x20` (`0x0035C566`-`0x0035C578`), and by the field teardown `0x0035BB70`: its
`and 0xFFFC02EC` at `0x0035BB8A` clears bits `0x1`, `0x2`, `0x10`, `0x100` and `0x400`-`0x20000`, so the three arms and
the posted bit `0x100` together. `0x0035C560` is called from `0x00253970` (`0x002539C5`), `0x0035BB70` from `0x00253A30`
(`0x00253A3E`) and from `0x003C5E50` (`0x003C5EA7`).

### The two signals from the fall

A fallen body is torn down only after two unit flag bits are set:

1. **Bit `0x200000000`, the fall has played.** `0x003250F0` sets it when a unit with flag bit `0x4` gets animation event `0x2007`,
   `0x2008`, `0x200C` or `0x200E` (`0x00325136`-`0x0032519F`). Those are the death clips the HP write and the Stone
   and X-Zone arms start ([HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md)).
2. **Bit `0x400000000`, hide the body.** `0x00319F50` sets it on actor timeline code 4 for a unit with KO, Stone or X-Zone
   without the field's bit `0x8000`, and for a unit with no stats record (`0x0031A124`-`0x0031A127`), together
   with flag bit `0x400`, and on code 6 for any unit, then refreshes visibility
   (`0x0031A100`-`0x0031A159`, `0x0031A198`-`0x0031A1A4`). Code 4 is ignored while the unit is carrying out Revive
   (`0xAE`) on itself.

Bit `0x200000000` has a second setter: on actor timeline code 2 `0x00319F50` sets the unit's HP to 0
(`0x00300520` with flags `0x14`) and then sets the bit (`0x0031A089`-`0x0031A0AA`), unless the unit is carrying
out Revive on itself. A unit with no stats record leaves the arm with nothing done, and so does a unit
that is already down, one with a bit of `0x80000003` in stats `+0x64` or `+0x3C`, while `0x00313F60`
answers 0 (`0x0031A042`-`0x0031A066`).

`0x00313F60` jumps to `0x00377C20`, which answers bit `0x8000` of the 16-bit word at
`[0x02ADD100] + 8 + 3 × 0x003148F0()`, or 0 with no table or an index at or past its count
(`0x00377C24`-`0x00377C5F`). `0x003148F0` takes no argument: it answers the field id, the dword `+0x1044` of the
save's persistent payload `0x002EF2B0()` gives, read as 0 when negative (`0x003148F0`-`0x0031490A`). The word
therefore belongs to the area: a down unit in an area whose word has that bit goes on like a unit that
is not down.

`0x00319F50` does nothing for a unit with flag bit `0x2`, answering 0, or while `0x00306BB0()` reports `0x022C2160` at 5 or
6, answering 1 (`0x00319FA3`-`0x00319FB3`). Code 7 sets flag bit `0x200` and refreshes visibility with `0x00312700(unit)`
for a unit whose byte `+4` has bit `0x40` (`0x0031A1AB`-`0x0031A1BA`).

Timeline codes reach `0x00319F50` through `0x002EB740` from two senders: the battle effect program `0x003B8670`
(`0x003B887D`, `0x003B8988`, `0x003B8A1C`, `0x003B9208`), and `0x002FC010`, which sends each queued value of a finished entry
of the list `0x02EC3D60` with timeline code 0 (`0x002FC085`, `0x002FC103`) and then timeline code 1 with the value 0
(`0x002FC12D`, `0x002FC158`).

The fall also starts an effect. On action timeline events 2 and 6, a unit with KO, Stone or X-Zone starts battle
effect `0x78` on itself and keeps its handle in `+0x74`, unless it is an enemy whose class row byte
`+0x18 & 0x0E` is 4 (`0x003255DB`-`0x00325649`). Event 9 sets bit `0x80000`, the drop of a hovering body
(`0x003256FB`).

### Hiding the body

`0x003125E0(unit)` builds the hide mask, and the model is shown only while it is 0 (`0x003125E0`-`0x003126DD`,
`0x00312700`). For an active unit, one with flag bit `0x10` (`0x003125F1`):

| Mask bit | Condition |
|---|---|
| `0x10` | KO, Stone or X-Zone without the field's bit `0x8000`, or no stats record, and torn down (flag bit `0x2`) (`0x00312652`-`0x0031267C`) |
| `0x20` | bit `0x400000000` |
| `0x02`, `0x04`, `0x08` | flag bits `0x800`, `0x400`, `0x200` |
| `0x40`, `0x80` | an enemy whose spawn record has bit `0x10` or bit `0x8` |

A unit without flag bit `0x10` gets mask 1 (`0x00312642`), except mask 0 when it has flag bit `0x8` and a stats
record and is not down (`0x003125F5`-`0x0031261D`), or at party control level 2, a chocobo ride (`0x0030D9A0`, [Party
control modes](../Engine-Core/party-control-modes.md)), when it is the rider, the unit `0x0031B8C0` gives
for the rider's seat `0x00327200` (`0x00312623`-`0x0031263C`).

The unit frame refreshes it every frame (`0x00234034`, `0x00234112`, `0x00234133`). The switch is on or off; there is
no fade.

`0x003126E0(unit)` returns 1 while the mask is 0 (`0x003126E4`-`0x003126ED`). `0x00328530` asks it for the
target and builds its target line through `0x00290320` only when it returns 1 (`0x00328555`-`0x003285A0`).

### The fallen unit's frame

`0x00233F70` runs a different frame for an active unit with KO, Stone or X-Zone that is not torn down
(`0x00234039`-`0x00234112`), and for a unit with flag bit `0x10` that has no `+0x698` record (`0x00233FD6`):

- a unit with flag bit `0x2` set runs only `0x00312700` (`0x00234039`-`0x0023403C`, `0x00234130`);
- an enemy whose class row byte `+0x18 & 0x0E` is 4 only keeps its position up to date: with flag bit `0x2`
  clear, a `+0x698` record whose byte `+5` is 1 and that class row (`[+0xE68]`, `0x00234042`-`0x00234065`) it runs
  `0x00236300`, `0x0033A240(unit + 0x80)`, `0x0023A070` and `0x00312700`;
- anyone else sets battle flag 2 (unless a group completion is pending), stops moving, runs the drop below, and is
  torn down with `0x00300E40(unit, 0)` once bits `0x200000000` and `0x400000000` are both set and the presentation
  test on its slot `0x0030CA50` allows it: `0x00322310` non-zero, or `0x003228E0` zero (`0x002340BC`-`0x00234100`); it ends
  with `0x00312700` either way (`0x00234112`, `0x00234133`).

The drop `0x003057D0` runs while the unit is down, has bit `0x80000` and not bit `0x100000`, and its actor passes `0x00264490`. Each
frame it lowers the body's height offset by an amount that grows by 0.02 per frame (`+0x19C`), stops at 0, and
then sets bit `0x100000` (`0x003057E5`-`0x00305896`).

### Tearing down

`0x00300E40(unit, keep)` runs the defeat cleanup with argument 1 (`0x00300FC0`), cancels the action (`0x003105D0`) and
zeroes `+0x6F8` (8 bytes), `+0x748` and `+0x770`. It clears the issued command (flag bit `0x4000`) unless that
bit is set with word `+0xBA0` holding `0x113` or `0x95` (`0x00300E7B`-`0x00300EAA`), clears bit `0x400` of
`+0x788` and bit `0x2` of `+0x6B0`, zeroes `+0x750` (8 bytes) and `+0x74C`,
sets bit `0x20000000000000` and removes the unit's effect `+0x74` (`0x00300E54`-`0x00300ED5`). Then:

- **A party member** (a stats record `+0x698` of kind 0) keeps its unit. With no attackers left (`+0xEA0` 0) it
  also runs `0x00322050` and `0x00301310`
  and clears bit `0x4000000`. Then bits `0x400000000`, `0x80000`, `0x100000` and `0x200000000` are cleared and
  **bit `0x2` is set**, the effect handle `+0x74` becomes -1 (`0x00300F2E`), and visibility is refreshed,
  so the hide mask's `0x10` keeps the model hidden (`0x00300EEE`-`0x00300F45`).
- **Anyone else** (a null stats record or another kind, `0x00300EE4`, `0x00300EEC`) first has its spawn record
  cleared by `0x00237080` when `keep` is 0 (`0x00300F5D`-`0x00300F68`). It loses its definition
  (`0x0023A570(unit, 0xFFFF)`) and has flag bit `0x200000` cleared (`0x00300F7A`).
- It also loses its actor (`0x0025AB30`), and `0x002697E0`, which is `0x00269860(actor, 0)`, starts one of the
  actor's script functions through `0x003DBB60(actor, 2, entry, 0, 0)` when bit `0x4000` of its `+0x1C` is set
  (`0x00269910`-`0x002699AB`) and then runs `0x00269640`, unless a spawn group holds it: `0x00236760()` is non-zero (bit
  `0x1000` of the party block's flag dword `[0x02EBF190]+4`) and `+0xE99` has bit `0x2`, group mode 2
  (`0x00300F80`-`0x00300FA4`).

Both arms zero dword `+0x30` before returning (`0x00300F4A`, `0x00300FA9`).

### Standing up again

Removing the last of KO, Stone and X-Zone runs `0x00301140(unit)` (`0x0030E811`;
[Gaining and losing statuses](status-changes.md)). It reads the stats record `+0x698` with no null test
(`0x00301146`-`0x00301150`), so a unit without one faults there, and with any of the three still set it returns at
once (`0x0030115C`). With none of the three left (`0x00301146`-`0x003012F6`):

1. A body that is hidden, and not already placed (flag bit `0x4000000`), is placed with `0x00311F70` (`0x0030116B`-`0x00301185`).
   The hidden test is `0x002E9600(actor)` returning 0; it returns bit `0x8` of byte `+0x10` of `[actor+0xC0]`
   for an actor whose byte `+3` has `0x60` in its top three bits, and 0 otherwise (`0x002E9600`-`0x002E9623`).
2. The actor is refreshed from the definition (`0x00238BF0`) and the action cancelled (`0x003105D0`); `+0x6F8`,
   `+0x748` and `+0x770` are zeroed, and the issued command (flag bit `0x4000`) is cleared unless it holds
   `0x113` or `0x95` (`0x0030118A`-`0x003011DD`).
   - Then bit `0x400` of `+0x788` and bit `0x2` of `+0x6B0` are cleared, `+0x750` and `+0x74C` zeroed, and
     flag bit `0x20000000000000` set (`0x003011E0`-`0x0030120B`).
3. Revive effect `0x7B` starts on the unit, `0x002EACD0` with the unit id `+8`, 1, the address of `+8` and
   `0x7B` (`0x003011F5`-`0x00301216`), then `0x002E8060(actor)` runs (`0x0030121F`), and the re-plan set is installed
   ([Enemy AI](../Enemy-AI-And-Gambits/enemy-ai.md)).
   - With the install, flag bits `0x800000`, `0x20000000000`, `0x40000000000` and `0x1000000000000` are cleared
     and `+0xDCC` zeroed, and the weapon is sheathed at once with `0x002ECF10(actor, 0, 0)` (`0x00301224`-`0x00301272`).
4. The stand-up clip, event `0x200D`, plays (`0x0030127A`-`0x00301282`); it clears bit `0x1000000` when it lands
   (`0x0032517C`).
5. Unit flag bits `0x400000000`, `0x700`, `0x2`, `0x180000` and `0x200000000` are cleared, bits `0x1000000` and
   `0x40000000` set, the old effect removed, and visibility refreshed, so the model is shown.
   - The old effect is `+0x74`, removed by `0x00319E30` and then set to -1 (`0x0030129E`-`0x003012B3`).
   - `+0xDD0` = `0x0032A150()` - 5 x trunc(`[0x01DFE0B8]` x -30.0), 150 ticks ahead while `[0x01DFE0B8]` holds its
     image value 1.0 (`0x003012BA`-`0x003012DB`).
   - Visibility is `0x0026DC60(actor, 0x003125E0(unit) = 0)` (`0x003012E1`-`0x003012F1`), and last `+0x30` = 0
     (`0x003012F6`).

`0x00311F70` asks `0x00336E40` for a point and moves and turns the actor to it (`0x00311FCE`-`0x003120D5`). Without a
reference unit, `0x00336E40` returns the unit's own position when `0x022C7D10` is 0; otherwise the anchor
`0x022C7DD0` for the party leader, and a point near the anchor for anyone else (`0x00336F79`-`0x00336F98`). In summon
mode `0x00311F70` asks for mode 1 instead (`0x00311FAB`-`0x00311FC9`). `0x0033CA00`
records the anchor from the actor of the character under control (`0x0033CA15`-`0x0033CAF2`).

## Modding notes

- Game Over is posted only through `0x0035C7B0`, from the field frame, from the verb `callgameover`
  (`0x00237D60` through `0x0035C7A0`) and from `0x0027EFA0`; refusing `0x0B` there keeps the game running, but
  the KO-time arming has already locked input.
- A party member's body is never removed, only hidden; a revive shows it again.

## Related

- [HP and KO](../Damage-And-Battle-Formulas/hp-and-ko.md) - the HP write that adds KO and starts the death clip.
- [Gaining and losing statuses](status-changes.md) - the KO, Stone and X-Zone arms.
- [Kill rewards](../Rewards-EXP-Gil-And-Loot/kill-rewards.md) - what a fallen enemy pays.
- [Field frame](../Engine-Core/frame-update-order.md) - the frame that
  posts the request.
- [Enmity](../Enemy-AI-And-Gambits/enmity.md) - the enmity removed at a fall.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 7 calls with 4 other topics</summary>

**Saving, loading and settings**

| Function | | Functions |
|---|---|---|
| `0x00236760` | is called by | `0x001C1720`, `0x002EF690`, `0x00583D60` |
| `0x002E1C20` | is called by | `0x005823B0`, `0x00582860` |

**Saving, loading and settings** (explained on [saving and loading](../Saving-Loading-And-Settings/saving-and-loading.md), [party data](../Party/party-data.md), [strong and weak mode](../Rewards-EXP-Gil-And-Loot/strong-and-weak-mode.md), [game application](../Engine-Core/game-application.md))

**Steam and achievements** (explained on [handbook files](../Game-Files-And-Data-Tables/handbook-files.md))

| Function | | Functions |
|---|---|---|
| `0x003148F0` | is called by | `0x003160C0` |

**Random numbers** (explained on [enemy respawning](../Enemy-Spawning/enemy-respawning.md))

| Function | | Functions |
|---|---|---|
| `0x002342F0` | calls | `0x00328D80` |

</details>
