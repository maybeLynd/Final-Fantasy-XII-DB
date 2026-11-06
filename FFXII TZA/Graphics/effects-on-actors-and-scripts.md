---
title: "Effects on actors and scripts: numbered effects on actors and the script effect slots"
kind: "system"
category: "Graphics"
addresses: "0x0024B270"
---

## What the player sees

Abilities and events play numbered effects on a character and its targets, and event scripts load
and play effects of their own.

## How it works

### Numbered effects on actors

`0x003B02A0(owner, targets, count, number, kind)` plays effect `number` as an instance of kind 5, 6 or 9
and refuses any other kind. Unless the request kind below is 1, it also refuses when
`0x002FC9B0()` plus `0x003B0B70()` exceeds 23, `0x002FC9B0() + 0x003B0B70() >= 0x18` (`0x003B0377`-`0x003B0388`). It makes
the instance (`0x0024B270`) with state 2 and the number in `+0x373`, stores the owner at `+0x08`, and appends each
target whose render record is live and passes `0x002E9FE0` to the target array `+0x10`. Numbers 100 to 103 and
`0x94` are kind-3 requests in the table below.

The requests sit in 36 entries of `0x18` bytes at `0x02EBEC00`, packed from the start:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` |  | handle: kind << 28 \| serial (`0x02EBEF60`) |
| `+0x04` | `u32` |  | set by `0x003B0FD0` |
| `+0x08` | `void*` |  | the instance |
| `+0x10` | `u8` |  | effect number |
| `+0x11` | `u8` | target test |  |
| `+0x12` | `u8` | kind |  |
| `+0x13` | `u8` |  | bits `0x6`: request kind (3 for 100-103 and `0x94`, 1 when the number's `0x01EFE260` byte is 1, else 0) |

- `0x003B0980` returns the first free entry; with all 36 taken it ends the first instance whose
  request kind is 0 or 3 (`0x0024EE60`), closes the gap and returns the last entry.
- `0x003AFFB0(n)`, from `0x002FCCC0`, ends requests from the front of the table until `n` are left,
  sparing request kinds 1 and 2. `0x003B0B70` returns half the number of entries in use.
- `0x003B0BF0(handle)` returns the entry, `0x003B0940(handle)` its effect number or −1, and
  `0x003B0FD0(handle, v)` stores `v` at `+0x04`. `0x003B0C30(owner, number)` is
  `0x003B02A0(owner, 0, 0, number, 5)`.
- `0x003B0820(v)`, with arena 8 selected, ends the instance (`0x0024EE60`) of every entry whose `+0x04`
  equals `v`, closes each gap and clears `0x02EBEF48`. `0x002FCB60(handle)` calls it with its own
  handle first (`0x002FCB79`).

The last entry, `0x02EBEF48`-`0x02EBEF5F`, is the one a closed gap leaves behind. After moving the later entries up one,
`0x003B0770` and `0x003AFFB0` clear its handle `0x02EBEF48` and its instance `0x02EBEF50` (`0x003B07F2`-`0x003B07FC`,
`0x003B00D9`-`0x003B00E0`), and `0x003B0820` (`0x003B089D`) and `0x003B0220` (`0x003B028B`) clear its handle. When `0x003B0980` ends an instance to free an
entry, it clears bit `0x1` of the last entry's `+0x13`, `0x02EBEF5B` (`0x003B0A9D`), and returns that entry (`0x003B0AA4`).

- `0x003B1260(handle, kind)`, for a kind of 1 to 10, calls `0x0024FE70(instance, kind)` with arena 8
  selected.
- `0x003B1050(targets, n)`, from `0x0024FBF0`, raises bit `0x4` of `+0x368` on every kind-5 instance
  whose request kind is 0, or is 1 or 3 and whose owner `+0x08` equals an id of the list (`+0x11`
  = 0) or the value `0x002E9B80` returns for one (`+0x11` = 1).
- `0x002FD090()`, from the same `0x0024FBF0` (`0x0024FC58`), raises bit `0x4` of `+0x368` on the instance `+0x10` of
  every handle on the kind-1 active list `0x02EC3D60`, without a test.

### Script effect slots

Event scripts reach the loaded-file queue through 32 slots of `0x18` bytes at `0x022D94B0`: the
queue id `+0x00`, a state word `+0x04` (0 free, 1 reading, 2 read, 3 playing, 4 cancelled), the
reading manager `+0x08` and the signal bytes `+0x10` ([native commands](../Scripts-And-Script-Commands/native-commands.md)).
Every slot number is clamped to 0 to 31, `slot < 0 ? 0 : slot > 31 ? 31 : slot`, at the start of each slot
function (`0x0036E32C`-`0x0036E33D` in `0x0036E320`; `0x0036E540`, `0x0036E5A0`, `0x0036E5E0`, `0x0036E8B0`, `0x0036DDC0`,
`0x0036DF80`, `0x0036E460`).

- Read: `effectread(id)` (`0x00DB`), `locationeffectread(id)` (`0x0127`) and `questeffectread(id)`
  (`0x01DA`) push slot 0 and the kind 0, 1 or 2; their two-argument forms (`0x00E0`, `0x0128`,
  `0x01DB`) take the slot first. The shared body `0x003576D0` calls `0x0036E320` unless the issuer's
  manager is skipping (`0x00267310`), and then `0x00314D40(1)`.
- `0x0036E320(manager, slot, id, kind)` acts only on a free slot: it clears the signal bytes, adds
  `0x1000` to the id for kind 1 or `0x2000` for kind 2, files it with `0x003B1A80(id, slot)`, which puts
  the slot in mask `0xFC0` of the queue id, keeps the manager, and sets state 1 when it got an id.
- `effectreadsync` (`0x00DC`, slot 0) and `effectreadsync_e1(slot)` (`0x00E1`) poll `0x0036E540`: a
  reading slot waits until `0x0024DE70(id)` reports 2 or 3, then becomes state 2.
- Play: `effectplay(n)` (`0x00DD`, slot 0) and `effectplay_e2(slot, n)` (`0x00E2`) call
  `0x0036E8B0(slot, n)`. A slot in state 2 or 3 whose file reports 2 or 3 becomes state 3 and is
  played by `0x003B1BA0` with the owner `[0x02EBCC70]`, the target list `0x02EBCBE0` (count
  `[0x02EBCC60]`) and `n`. Then `0x0024F8D0` sets mask `0x7000` of the instance's `+0x36A` to 3 for a
  slot read by manager 3 and to 0 otherwise, which picks the target table above.
- `effectsync` (`0x00DE`, slot 0) and `effectsync_e3(slot)` (`0x00E3`) wait while the state word
  (`0x0036E5A0`) is non-zero; a skip cancels the slot instead.
- Cancel: `effectcancel` (`0x00DF`, slot 0) and `effectcancel_e4(slot)` (`0x00E4`) run `0x0036DDC0`,
  which sets state 4 on a slot in any state but 0 and 4 and, unless the queue entry's flag bit `0x1` is
  set (`0x003B24C0`), releases the entry (`0x003B18E0`). `effectcancelall` (`0x00E5`,
  handler `0x00350FA0` `jmp 0x0036DE20`) runs `0x003B1710` over the queue and sets every slot to state 4.
- Triggers: `effecttriggersync` (`0x0274`, `0x0275`) waits while `0x0036E5E0(slot, n)` holds: for a
  playing slot, `0x0024FDA0` makes the instance current (`0x0024ED80`) and hands `0x003333F0` the first qword
  of its `+0x130` block, a timeline player (`0x0024FDF6`, `0x0024FE25`).
- `0x003333F0` asks whether one of that player's 16 track pointers, at player + 8 x k for k from 0 to 15,
  has byte `+0x11` equal to `n` (`0x00333400`-`0x00333415`), or else `0x003A8FC0(n)` (`0x0033341A`). The
  player and its tracks are in [Effect element runtime](effect-element-runtime.md).
- `effecttriggercancel` (`0x01DC`, slot 0) and `effecttriggercancel_1dd(slot, n)` (`0x01DD`) run
  `0x0036DF80`, which passes a non-free slot's id to `0x003B27A0`.
- `effectsignal(slot, v)` (`0x0241`, `0x0036E460`) passes `v` to `0x0024F3C0`, which, for `v` = 1,
  adds 1 to the bits under mask `0xF0` of the instance's word `+0x378`.
- `effecthitsyncbyid` (`0x0440`) waits while `0x0036E640(id)` holds: the file reports 2 or 3 and bit `0x20`
  of the instance's `+0x36A` is clear (`0x0024E210(id, 0)`).

## Related

- [Effect element runtime](effect-element-runtime.md): instances, emitters, the update and timeline tracks.
- [Effect drawing](effect-drawing.md): the display layers and the draw list.
- [Effect anchors and targets](effect-anchors-and-targets.md): anchor queries and target slots.
- [Effect file loading](effect-file-loading.md): battle effect slots and the loaded-file queue.
- [Native commands](../Scripts-And-Script-Commands/native-commands.md): the effect verbs of event scripts.
