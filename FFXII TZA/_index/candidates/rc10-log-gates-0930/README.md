# RC-10: no caller gates the formatted log call on a shared verbosity value (OPUS, 2026-09-30)

Input for `RC-10` ([the formatted log call and its level gate](../../../00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md)
section 9). SWE2-CONTRACT registered the row, so it applies this. Static evidence only (shipping image `73461d08…`).

## Method

`rc10_log_gates.py` finds every `rel32` call or tail jump to `005CDAA0` with a raw `E8`/`E9` index over `.text`. It
finds **245 sites in 136 functions**, the page's own counts (the row's 136 callers and RC-9's 245 sites); that
agreement is the positive control.

For each site the owning function is decoded, and every conditional jump before the site that can jump past it is
classified by what set its flags: the `cmp`/`test` before it and, one step back, the register load feeding it.
- **GLOBAL:** a rip-relative operand, or a register loaded from one.
- **TLS:** a `gs:` operand.
- **LOCAL:** anything else.

For every global found this way, its writers were then listed image-wide by a rip-relative sweep. Output:
`rc10_log_gates.tsv`, one row per site.

## Result

| class | sites |
|---|---:|
| never skipped by any branch | 26 |
| skippable only by local conditions (arguments, results, fields) | 195 |
| behind a branch on a global | 24, through 20 distinct globals |
| behind a per-thread (`gs:`) value | **0** |

- **No global gates log calls in more than one function** (0 of 20). A verbosity control would be one value
  consulted around many log calls. Each of these 20 guards the sites of a single function.
- **18 of the 20 are written by code, and they are state rather than verbosity.**
  - `02EAC278` is written at `0079A16C` inside the same function it guards (`0079A120`), an init-once flag skipping the
    whole block.
  - `02CB813C` is written four times by the console dispatcher `001D1660`, whose own log site it gates.
  - `02EA95A0` (24 references), `02EA5248` (57) and `02EA5488` (17) are shared state words of their subsystems,
    written by their own code.
  - The rest have one writer each, in or beside the gated function.
- **2 of the 20 are never written:** `02EA5220` and `02EA5228`, gating sites in `0079F150`. They belong to the
  input-script facility, which the database already records as dead in this build: `[02EA5220]` has one read and no
  writer ([`s36-opus-replay-arbiter-input-gate/`](../s36-opus-replay-arbiter-input-gate/README.md), L2 verdict S-36).
  They switch that facility, not the log's verbosity.

So no caller conditions `005CDAA0` on a global or per-thread verbosity value. The call has no level gate of its own
(section 9), and nothing around it adds one.

## Not claimed

- An indirect route is excluded as far as data can show: no 8-byte pointer to `005CDAA0` exists, and its only 32-bit RVA references
  are its own `.pdata` entries (`02FD5C0C`, `02FD5C14`).
- The meaning of each state flag beyond "written by its own subsystem's code".
- That a flag could not be flipped externally (a debugger or a mod).
