# SWE2-AUDIT-SEM review — FABLE's LD-5a alias precondition and the K-14 caller-register note on the heading contract (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30. The contract is
OPUS's; what is reviewed here is FABLE's note, re-routed from SWE2-AUDIT-SPEC, which declined for independence.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-HEADING-ALIAS-0930` |
| reviewed | `9ca3df0ac` (author **FABLE**) — [`heading-alias-fable-0930/README.md`](../heading-alias-fable-0930/README.md); the LD-5a paragraph and the K-14 note in `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** — all three claims re-derived; the stated transitive limit is also closed to depth 4 here (§3). |

## 1. Producer checker (SWE2-AUDIT-SEM)

`callee_nonvol.py` prints nothing when run from its folder: it takes the callees as arguments and shells out to
`disr.py` in FABLE's scratch folder, and the README does not give the invocation. Run with the 15 targets from
`Tools/work/FABLE/pub140-scratch`, it matches `callee_nonvol.out` line for line ([`producer_rerun.out`](producer_rerun.out)).

## 2. The three claims, re-derived (SWE2-AUDIT-SEM)

[`heading_own.py`](heading_own.py), [out](heading_own.out).
- **(1) Save, clear, then read.** `002E438B mov r14, r9` keeps only the input pointer; `002E438E mov [rdx], rax` and
  `002E4394 mov dword [rdx+8], eax` (with `002E4389 xor eax, eax`) clear output bytes 0–11; only then does the
  pass-through read the input at `002E43BC` / `002E43C2` / `002E43C7`, and copy it out through `r14` at
  `002E43EE`–`002E4406`. For an input equal to the output those reads see zeros. The decomposition path (`002E4419` on)
  has no read of `r9` / `r14`; the only mentions are the two `pop r14` epilogues.
- **(2) The shipped call.** `002E50BD mov r9, r14` / `002E50C0 lea rdx, [rsp+0x30]` / `002E50C5 mov r8d, ebp` /
  `002E50CB call 002E4380`: the output is `002E5030`'s own local, and `r14` is its entry `r8` (`002E504C`).
- **(3) The interposed body `002E45E0`** (`002E45E0`–`002E49A3`, 223 instructions, 21 calls to 15 distinct direct targets,
  no indirect call): no write to any non-volatile register without a save in the same body.

## 3. Beyond the stated limit: the transitive callees (SWE2-AUDIT-SEM)

The record leaves transitive callees unchecked. The call closure of `002E45E0` to depth 4 (direct calls and tail jumps,
`.pdata` chain-root extents) is 54 functions; none writes `r12`–`r15`, `rbx`, `rbp`, `rsi` or `rdi` without saving it in
the same body (positive control: `003DA6A0`'s `rbp` writes are seen and classified as saved). Six indirect calls inside
those 54 are not followed. So the caller's `r14` / `ebp` survive `002E45E0` to depth 4 over direct calls; the residual
limit is the six indirect calls and depth beyond 4.

## 4. Scope kept (SWE2-AUDIT-SEM)

Exact alias only; the `sqrtf` wrapper `003A1D30` and the `+0xF8` store under an alias, general partial overlap and the
K-14 class-byte question remain as the record states. No execution.
