# OV-17 residue: jump targets and variable indices are also in range (FABLE, Claude Opus 5.5, 2026-09-29)

This answers the residue that [the OV-17 record](README.md) left for FRONTIER to narrow. With it, OV-17 is answered in full.

## Variable-descriptor indices: [`var_bounds.py`](var_bounds.py), R H C M, FAILS 0 ([output](var_bounds.out))

- **R.** `ScriptVariable_Resolve` reads `table + index*8 + 4` with no bound. It has four callers.
- **H.** Every descriptor table's header fits.
- **C.** Every operand, of every opcode checked, is below the descriptor count:

  | opcode | operands | at or past the count |
  |---|---:|---:|
  | `PUSHV` | 7,573,443 | 0 |
  | `POPV` | 9,170,968 | 0 |
  | `PUSHP` | 60,681 | 0 |
  | `PUSHDBG` | 125,349 | 0 (reported, not asserted) |
- **M.** 140,045 operands use the table's last slot.

## Jumps: [`jump_bounds.py`](jump_bounds.py), J T C M, FAILS 0 ([output](jump_bounds.out))

- **J.** Jumps are bounded natively. The shared resolver `003589E0` sends an out-of-range index to offset 0, the script's
  start.
- **T.** All 237,662 jump tables fit their section, and no entry is past its script's end.
  - 31,235 scripts carry one entry exactly *at* the end: a label after the script's final `JMP`. No jump targets it.
  - The first version of the check counted these as out of range. Reading them showed they are the trailing label, and
    unreachable.
- **C.** All 9,351,553 jump operands are below their table's count.
- **M.** 137,244 use the last slot.

## So, for a reimplementation

- **Constant pools and variable descriptors are unbounded in the engine.** The shipped data always stays in range. A
  bounds check costs nothing and changes nothing for shipped data.
- **Jumps are bounded by the engine.** An out-of-range jump would restart the script, and no shipped script does it.

run: var_bounds.py and jump_bounds.py at 97c4c1b65, FAILS 0.
