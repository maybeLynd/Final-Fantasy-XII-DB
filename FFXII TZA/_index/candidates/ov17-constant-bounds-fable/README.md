# OV-17: script constants are in range by authoring, and the tables live as long as the bound payload (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-17, the script-from-bytecode page §8):** "Establish bytecode/label/constant resource lifetime and authored input
constraints."

[`constant_bounds.py`](constant_bounds.py) runs I, H, C and M: FAILS 0 ([output](constant_bounds.out)). Static, plus every
shipped `.ebp`.

## Authored input constraints: the constant pools (answered)

- **I.** The interpreter does not bound `PUSHI` or `PUSHF`: each reads `pool + operand*4 + 4` with no compare. `PUSHTAG`
  is bounded: out of range, it pushes `0x8000`.
- **H.** In all 10,036 shipped `.ebp` files, each pool's header count fits before the next table the header names.
- **C.** Every `PUSHI` operand (4,275,239) and every `PUSHF` operand (6,035,106), across 237,662 scripts, is below its pool's
  count. **The shipped data never indexes past a constant pool.** That guarantee comes from the authoring tool, not the engine.
  A reimplementation that bounds-checks is safe; one that trusts the operand is safe only for shipped data.
- **M (sensitivity).** 46,802 operands use their pool's last slot, so a pool one entry shorter would fail C.

## Lifetime: prior art

- **The tables are rebased pointers into the payload.** The bytecode, constant pools, variable descriptors and tag table all
  live in the bound definition payload (manager slot `+0x000`). The bind rebases each header offset into the slot:
  `+0x68` / `+0x70` / `+0x78` / `+0x80`
  ([the bytecode page](../../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md), "What
  `ActorManager_BindLoadedDefinitionPayload` reads").
- **They live exactly as long as that bind.** The actor-request page §7 (answered 2026-09-26) shows the resource-set load
  unloads a slot unconditionally before it binds a new payload, and that no route binds a slot still holding its old
  records. Nothing outlives the payload through these pointers.

## Not covered: jump and label targets, and variable-descriptor indices

Those are the other operand kinds OV-17's "authored input constraints" can mean. This record does not census them.

**Proposal for FRONTIER.** Narrow OV-17 to that residue: jump and label targets within their script, and variable indices
within the descriptor table. Mark the constant and lifetime halves answered with this record.

run: constant_bounds.py at afdc8ee77, FAILS 0.
