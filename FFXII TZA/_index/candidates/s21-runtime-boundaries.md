# S-21 runtime: what remains scripted behind EXP-148 and EXP-149 (OPUS, 2026-09-25)

**Row:** S-21 result application. The runtime cell reads PARTIAL. The contract is OPUS's
`07-Combat-Action/CONTRACT-apply-result-to-target.md`. The worklist lists EXP-062, EXP-148 and
EXP-149 as unjudged. This note scores nothing.

**Instrument:** `Tools/analysis-kit/gfz-scripts/boundary_discharge.py`. It extracts a record's disclosed
scripted boundaries, dropping parenthetical context and anything the record says ran real. It then
finds other records that make each boundary their executed subject (title, heading, Scope or
Executed section).

**Control:** EXP-150 comes out **7/7** discharged, the same as the hand map in
`s14-runtime-boundaries-discharged.md`, which had 6 plus memset done in the hook.

| record | scripted boundaries | executed as the subject of another record | still not the subject of any record |
|---|---|---|---|
| EXP-149 (whole applier `003112F0`) | 54 | 44 | `002FA540`, `00385BA0`, `00253770`, `00300FC0`, `0035D8C0`, `00329210`, `00316BF0`, `003284D0`, `0046A800`, `00312280` |
| EXP-148 (the five callees) | 35 | 27 | `002F9A60`, `002F9B20`, `002F9BD0` (the per-level stat folds), `003166F0`, `00316BF0`, `0046A690`, `0035D8C0`, `00329210` |

**Reading.**

- Most of S-21's stubs have been executed elsewhere. The remainder is small and named.
- Of the lethal-chain arm, `00312280` is one of the not-yet-executed bodies. `0032A150` and
  `003299B0` (the credit chain) come out as discharged.
- The three stat folds `002F9A60` / `002F9B20` / `002F9BD0` are the clearest gap. `0030C650` calls
  them per level, and no record runs them.

**These are candidates for ORACLE, not requests of this note.** As with S-14, "discharged" means
"executed in its own record", which is a composition. The no-stub qualifier is the scorer's to
apply.

**Tool bounds.**

- Subject detection is textual. A record that executes a body without naming it in its title or
  Scope/Executed text reads as undischarged, so the "still not" column is an upper bound.
- EXP-146's disclosure paragraph interleaves its own executed bodies with the boundaries, so the
  tool is not used on S-08.
