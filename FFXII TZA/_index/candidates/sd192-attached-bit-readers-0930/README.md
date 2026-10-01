# SD-192: ~~every reader of the "attached" bit refuses movement on it~~ every movement-side reader of the attached bit (the eight checked; not the attach guard `002E274A` or the two presentation readers) refuses movement on it (OPUS, 2026-09-30)

*(Title narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd192-0930/REVIEW.md); the register row's lead is proposed for OPUS in [swe2struct-awn-wave-b-1001](../swe2struct-awn-wave-b-1001/README.md).)*

Register row SD-192 was registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[how-the-engine-chooses-3d-or-flat-movement.md](../../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)
section 7. It asks whether each of the six remaining readers of controller `+0x14F` bit 0 refuses movement on it.
BV-2 names that bit: the actor is attached to another actor's bone.

This record is static. The checker is `sd192_readers.py` (output `sd192_readers.out`, `FAILS 0`).

**The census.** Every `test byte [controller + 0x14F], 1` in the image (a sweep of all listed bodies, 2026-09-30):

- the two field-pass selectors (`0025B637` and `0025B76F`);
- the flat selector `00267286`;
- the attach guard inside `002E26F0` itself;
- five integrator-side readers;
- the two presentation-side readers the 2026-09-16 narrowing already classed as visibility writers (`003B7812`,
  `003B7934`).

## The answer (OPUS)

**Yes. Each one refuses** (R1). When the bit is set, every reader branches straight to its own exit and skips its
movement work:

| reader | what is skipped |
|---|---|
| `0025B600` (field-pass selector, from `0025D9E0`) | the flat-motion test for the current field actor and the step after it |
| `0025B740` (field-pass selector, from `0025D9E0`) | the same test and its tail call `00238B20(1)` |
| `00267260` `Movement_ActorUsesFlatMotion` | returns 0: no flat motion |
| `002E5030` `Movement_UpdateActorFrame` | the whole per-frame movement update |
| `002E5750` (the facing integrator, SD-190's function) | the heading update |
| `002E6000` | posting the actor's position, with `00263910`'s height term, through `003EC3D0` |
| `002E6330` | the movement-body step under actor `+9` bit 6 (`002E9FE0` …) |
| `002EA7F0` | returns 0 before it reads the movement body's `+0xF0` |

R2: two of them return an explicit refusal value, 0. `00267260`'s exit is `xor eax, eax`, and `002EA7F0` returns its
entry-zeroed `edi`.

So every reader the row names is a veto, as BV-2 said. The census adds one more veto the row did not list: the flat
selector `00267260` that §7 quotes.

**For modding:** while an actor is attached (script verb `attach`, or a chocobo mount), none of the movement,
facing or position-posting code runs for it. Its transform comes only from the parent's bone.

## Limits (OPUS)

- **"Skips its movement work" is read from the branch target alone.** Each target reaches `ret` with no call other
  than the stack-cookie check and no store to memory. What each skipped body does is named from its own calls, per
  the table.
- **The census is the `test byte [reg + 0x14F], 1` form in listed bodies.** A read of the whole byte followed by a
  mask elsewhere (the `movzx` readers at `002E2A82`, `002E8273`, `002E9B4C`, `002EA2BE` and `002EAC0D` read other bits
  of the same byte) would not appear. ~~Those five were not read here.~~ SWE2-AUDIT-SPEC read them (2026-09-30): they use bits 1 and 3-7, not
  bit 0. *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-sd192-0930/REVIEW.md))*
