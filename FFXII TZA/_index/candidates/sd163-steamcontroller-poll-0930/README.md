# SD-163: SteamController_PollState reads 16 buttons and two sticks and drives the rumble (OPUS, 2026-09-30)

Register row SD-163 was registered by SWE2-DATA ([steam-integration-and-achievement-catalogue.md](../../../20-Platform-Online-Achievements/steam-integration-and-achievement-catalogue.md)
section 3). It asks what `SteamController_PollState` (`007A1CD0`, 1,124 B) does with the controller state beyond the
connect and disconnect messages.

This record is static. The checker is `sd163_poll.py` (output `sd163_poll.out`, `FAILS 0`). The ISteamController
method names are the Steamworks interface's vtable order:

| offset | method |
|---|---|
| `0x18` | GetConnectedControllers |
| `0x48` | GetDigitalActionData |
| `0x60` | GetAnalogActionData |
| `0x88` | TriggerVibration |

~~That naming is an identification matched to the call shapes, not a symbol.~~ The slot names are confirmed against the shipped `steam_api64.dll` (`SteamController005`): its flat
exports `SteamAPI_ISteamController_*` call through the same slots (SWE2-AUDIT-SPEC review 2026-09-30). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd163-0930/REVIEW.md))*

**Already on record (cited per SWE2-AUDIT-SEM's DD-4 review, `18c11f3b1`, C4):** DM-2's
[`dm2-code27`](../dm2-code27/README.md) point D3 (2026-09-27) reads P2's 16 button bytes `+0x43C`..`+0x44B`, in the
PlayStation order the XInput poll uses. The [vtable method index](../../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
names `007A1CD0` slot 5 of `PFramework::PInputDevicePadSteamController`, and RC-10 reads P1's two log gates. New here:
P3's axes, P4's rumble and P5's binding update.

## The answer (OPUS)

- **P1: the gate.** The interface at `[02EA9508]` lists the connected controllers (`+0x18`). The poll runs only when
  the first of them is the stored controller handle `[02EA95A0]`. It logs "SteamController Connected" once (flag
  `+0xA9`). Otherwise it logs "SteamController Disconnected" once and clears the flag.
- **P2: sixteen buttons.** For each of 16 digital action handles ~~(qwords `02EA9510`…`02EA9590`)~~ (qwords `02EA9510`…
  `02EA9588`) *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd163-0930/REVIEW.md))*, `+0x48` returns the
  action data. Its first byte, the pressed state, is stored at the device's `+0x43C`…`+0x44B`, one byte per action.
- **P3: two sticks.** Two analog actions (handles `02EA9590`, `02EA9598`) are each read twice through `+0x60`:
  - x × 256 → `+0x414` / `+0x418`;
  - y × −256 → `+0x420` / `+0x424`. The y axis is inverted.

  The ×256 puts the −1…1 Steam range into the integer scale the rest of the input stack uses.
- **P4: rumble out.** `+0x88` (TriggerVibration) is called with the controller and the device's two motor bytes
  `+0x98` / `+0x99`, each × 256. So the game's rumble reaches the Steam Controller through this poll.
- **P5: then the bindings.** `007A15A0(this)` walks the device's binding list (`this+0x18`) and updates each binding
  from its state byte. That is the shared step every input device runs.

**For modding:** a Steam Controller feeds the game the same way as a pad does: 16 buttons, two sticks (y inverted)
and two rumble motors. Remapping belongs to the Steam action set, not to the game.

## Limits (OPUS)

- ~~**Which game input each action means.** The 16 action handles are looked up by name elsewhere, and their mapping is
  not read here.~~ **Which button each byte is** (the review's optional wording): the name table at `01F40210` names the
  cells Up, Down, Left, Right, Circle, Cross, Square, Triangle, L1, L2, L3, R1, R2, R3, Start, Select in order, so
  `+0x43C`..`+0x44B` are Square, Cross, Circle, Triangle, L1, R1, L2, R2, Select, Start, L3, R3, Up, Right, Down,
  Left, the XInput poll's PlayStation order. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd163-0930/REVIEW.md))*
- ~~**What `007A15A0` does per binding** beyond walking the list is not read.~~ **`007A15A0`'s edge rule** (the review's optional wording): it walks the ring at `this+0x18`; for a
  node with a state pointer `+0x38` it sets `+0x31` = 1 on a 0->1 edge and `+0x32` = 1 on a 1->0 edge, then `+0x30` =
  the new state; otherwise, with `+0x40` set, it calls `0079A5F0`. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd163-0930/REVIEW.md))*
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
