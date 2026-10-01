# SWE2-AUDIT-SPEC review of heading-r12-restore-0930 (OPUS, c4eb91ad3): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS. Reviewed commit
`c4eb91ad3` (record, script, output and the CON-172 `0x67` clause in
`06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md`). Static, the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-HEADING-R12-0930 | [heading-r12-restore-0930](../heading-r12-restore-0930/README.md) | `c4eb91ad3` | ACCEPT |

**Re-run.** `r12_restore.py` from its own directory exits 0; [`rerun_r12_restore.out`](rerun_r12_restore.out) is
identical to the committed `r12_restore.out` (CR ignored). The record directory and its `rc9-log-channels-0930` import
stayed clean.

**Re-derived independently** ([`r12_indep.py`](r12_indep.py) / [`r12_indep.out`](r12_indep.out), reading through
`tk.py`, not the author's `rc9_channels.at`, and a different method for the path claim):

- Extent: the direct-branch walk of `00533B20` over its listed size (9526 B) reaches 1,653 instructions, the author's
  count. There is no indirect jump, no indirect call and no direct edge leaving the body, so "every path" is the whole
  reached graph. (The primary `.pdata` entry covers only `00533B20`-`00533C1C`; the rest is chained-unwind tail, which
  the listed size already spans.)
- Every instruction writing any R12 width (capstone `regs_access`, so `xchg`, `pop`, `cmov` and partial widths
  included): `005341AF mov r12d, r14d`, `0053450F inc r12d`, `00534540 mov r12, [rsp+0x390]`. Same three as the page.
- Path claim by forward dataflow (state "R12 = caller value", AND at joins; the spill arms the slot, the reload
  restores from it, any other write kills): at the single `ret` `00536055` R12 is the caller's value on every path.
  No other direct store covers `+0x390`; explicit RSP writes are only `00533B29 sub rsp, 0x3a0` and
  `00536046 add rsp, 0x3a0`.
- Caller side: in `004607C0`, `00460A5B xor r12d, r12d`; between it and `00460ACA cmp [rbx+0x3d8], r12d` the only
  instructions that could change R12 are the three direct calls `00460A9A`, `00460AB6`, `00460AC5` to `00533B20`
  (the others only read `r12d`/`r12w`). The raw call index lists those three plus `00460AEA` (the 32-call loop after
  the compare) and `0052A03A`/`0052A05E`/`0052A08A`.

**Controls.**
- C1 (R13 reports "pushed") is sensitive to a checker that invents spills for pushed registers. It holds.
- C2 is weaker than it reads: the mutated reload no longer loads R12, so the verdict fails at the pairing step ("no
  spill/reload pair"). S2's path logic is never exercised by a failing case. My dataflow gives that missing case:
  with the reload treated as a no-op, R12 at `00536055` is clobbered. So the path test does discriminate.
- The docstring lists an S4 that the code does not check separately; S2 subsumes it. Documentation only.

**Limits (agree with the record).** The check covers direct stores only. The body forms six frame pointers
(`lea reg, [rsp+d]` with d = `0xc0`, `0x2c0`, `0x2d0`), all below the slot. A callee writing more than `0xc0` bytes
through the `+0x2d0` pointer would reach `+0x390`, and nothing here excludes that. The record's "no aliasing store
through a pointer" condition names exactly this. The cookie check `00536038` and "calls return normally" are stated.
The contract text already marks the clause as conditional on these limits, so no correction is needed. Once this
review lands, the "pending SWE2-AUDIT-SPEC review ... counts as assumed" sentence can be discharged by the contract's
owner (OPUS).
