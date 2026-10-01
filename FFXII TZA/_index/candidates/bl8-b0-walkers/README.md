# BL-8: the class descriptor's `+0xB0` list is never read - only the destructor walks it (FABLE, Claude Opus 5.5, 2026-09-27)

**Question (BL-8):** the class descriptor's six intrusive lists.

Five are named: `+0x50` its own registry node, `+0x60` the annotation list, `+0x80` data members, `+0x90` instance
methods, `+0xA0` static functions ([descriptor contract](../../../22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md)
§14 item 1). `+0xB0` was open, with no insert found by three insert shapes (2026-09-25).

**Finding: nothing reads `+0xB0` either.** Every code path that touches it is housekeeping:
- the base constructors (`00632C90`, `00632D80` and the per-class constructors in `006316C0`…`00632780`) self-link
  it empty;
- the reset `0063D550` self-links it again;
- the destructor `00633390` walks it only to unlink nodes (`0063352C`).

No function walks it to use a node. That makes it a list the shipped build constructs, resets and tears down, but
never fills or consults.

## Evidence (`bl8_walkers.py`, output `bl8_walkers.out`, FAILS 0)

**Sentinel-walk idiom, image-wide over every listed body.** The shape is `lea rH, [rB + D]`, then within 12
instructions `mov rN, [rH]` and a compare of `rN` with `rH`. Sites found per offset:

| D | sites | functions |
|---|---:|---|
| `+0x80` | 22 | the field walkers (`00630500`…`0063E2E0`, `00597220`, `0059B430`, …) and the destructor |
| `+0x90` | 4 | **name lookups** `005A7A40`, `005A7B50`, `00682E30`, and the destructor |
| `+0xA0` | 3 | **name lookups** `005A0470`, `005A7AB0`, and the destructor |
| **`+0xB0`** | **1** | **the destructor `00633390` only** |

- **The controls are real users.** `005A7A40` and `005A0470` walk `+0x90` / `+0xA0` and `strcmp` each node's `+0x18`
  name against their argument; that is the record header `00632FB0` builds. The instrument therefore finds the
  consumers of the lists that have them.
- **Known positive:** the destructor is found at all four offsets.
- **Direct head loads compared with a `lea` of the head:** none at `+0x80`–`+0xB0`.
- **Head passed to a call:** 108 sites at `+0xB0`, none in the descriptor band or the reflection routines. The seven
  in `0059`–`006B` belong to other objects (renderer and loader bodies). This shape is not selective at such common
  offsets, and it is printed for completeness only.

## Limits

- **Static.** A walker built from a head held in memory, or reached through a helper that receives the head in a
  non-argument way, is not excluded. The live read of real heads (BL-8's closing step) would show them empty.
- **What `+0xB0` was *meant* to hold is not in the build.** No producer and no consumer means no type evidence. The
  destructor's unlink is generic, so it carries none either. That residue is intent: filed for a NAS review, not
  guessed.

## Files

- `bl8_walkers.py`, `bl8_walkers.out` and `consumer-check.md`.
