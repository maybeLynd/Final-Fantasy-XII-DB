# SD-190: the direct-delta path runs while an authored move-and-turn tween is still turning (OPUS, 2026-09-30)

Register row SD-190 was registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[setting-the-movement-mode-and-which-way-a-character-turns.md](../../../06-Movement-And-Navigation/Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md)
sections 9 and 10. It asks what bit 0 of `003E6A70`'s result reports. The row already reads that the one caller,
`0025DF00`, turns that bit into the facing integrator `002E5750`'s second argument, so 1 selects the direct-delta
path.

This record is static. The checker is `sd190_tween.py` (T1–T6, output `sd190_tween.out`, `FAILS 0`).

## The answer (OPUS)

**Bit 0 means: this character's render record has an authored move-and-turn tween whose turn phase is still
running.**

- **T1: what `003E6A70` reads.** It resolves the render record's handle (`003E6E60`), then runs `003AEF50` on the
  record's embedded tween object at `+0x550` (`embeddedTweenObj` in `fields.tsv`).
- **T2: what `003AEF50` returns.** It walks the tween object's node list (head `[+0x18]`, next at node `+0x48`) and
  ORs two flags:
  - **bit 0** if any node's byte `+1` is set;
  - **bit 1** if any node's byte `+2` is set.
- **T3: where nodes come from.** `003AED70` starts a node from a 128-slot, `0x60`-stride pool, with bytes `+1` and
  `+2` both set. Its callers are:
  - `003E6340`: authored presentation command `0x1A`, "move and turn toward the target along a profile"
    ([the-authored-presentation-command-handlers.md](../../../17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md));
  - `003E65E0`.

  Starting a node clears byte `+1` on every node already on the object, so a new turn supersedes an old one.
- **T4: what the two bytes mean.** The per-frame stepper `003AEF90` (from `003AF220`) treats them as two phases:
  - **byte `+2` is the move phase.** While it is set, the stepper adds a scaled vector (node `+0x30`…`+0x38`) to the
    translation output, and clears the byte when the move ends.
  - **byte `+1` is the turn phase.** While it is set, the stepper steps an angle into the rotation output (`+4`), and
    clears the byte when the turn ends.
- **T5: how the caller uses it.** `0025DF00` passes bit 0 to the integrator and keeps bit 1 (the move phase)
  separately.
- **T6: a second gate before the read** (added on SWE2-AUDIT-SEM's DD-owner-read-5 correction C2). At `0025E31D`,
  `0025DF00` first calls `003E68B0(record)`: the same handle resolve, then `003AEF20` on `+0x550`, which answers 1
  when the tween object's count `[+0]` is non-zero and its list `[+0x18]` is non-empty. That answer counts only when
  the actor's byte `+0x0D` has bit 1 (`cmovne` at `0025E32E`). If either fails, `003E6A70` is not read and the
  direct-delta argument stays 0 (`ebp`, zeroed at `0025DF1F`).

So while an authored `0x1A`-style tween is still turning the character, **and the actor's `+0x0D` bit 1 is set**,
the facing integrator takes the direct-delta path. It adds the two floats at its third argument to heading and pitch, instead of steering toward a target.

## Limits (OPUS)

- **What each tween routine does is read from its instructions only.** That `003E6340` is command `0x1A` is the
  authored-command page's reading. `003E65E0`'s arm (`word[+2] - 0xE`) is not named here.
- **What actor `+0x0D` bit 1 means is not named here.** It is a precondition of the direct-delta path, read from
  the instructions only.
- **Whether the integrator's third argument is the tween's own rotation output is not traced.** The row reads it as
  "the two floats at its third argument". This record does not follow those floats back to `003AEF90`'s `+4` output.
