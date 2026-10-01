# SECTION-01 (Update01) — contract owner's review (OPUS, 2026-09-25)

SECTION-01 rewrites two contracts OPUS owns — `07-Combat-Action/CONTRACT-apply-result-to-target.md`
and `04-Actor-Entity/Unit-Definition/CONTRACT-battle-unit-construction.md` — as an **uncommitted
overlay** on the 2026-09-22 21:12 snapshot. Every ORACLE commit to those files predates that base,
so the overlay builds on ORACLE's work rather than reverting it. Evidence class NATIVE/STATIC; the
section's Linux fixture was not replayed.

## Verdict: ACCEPT THE CORRECTIONS · REFUSE PUBLICATION UNTIL THE DROPPED EVIDENCE IS RESTORED

### Corrections re-read from the image — all agree

| claim | static finding |
|---|---|
| **R2** direct copies | `003115B6..00311606`: with `r9 = stats − result`, 32 dwords `result+0x5C+4i → stats+0xBC+4i` and 32 words `result+0xDC+2i → stats+0x13C+2i`; `js` skips negatives, so negative preserves and zero is a present value. **Exact.** |
| **R3** the flag records dispatch, not change | `0031153F`, `003115A4`, `003117D0`, `0031180C` are each `mov r14d, 1`; the tail `00311AAF..00311AC0` tests target, the caller-flag dword at `[rsp+0x44]` and `r14d`. **Exact.** |
| **U2** bit 26, not bit 42 | `0023A633` and `0023AC4B` are both `and qword ptr [rdi], 0xFFFFFFFFFBFFFFFF`. **Exact.** |
| **U3** registration base and condition | `00328FF0` (38 B): base `lea [rip+0x2B98382]` = **`02EC1380`**, stride `rax*3*8` = 24, writes `[+4]=edx`, `[+0]=r8d` only when `edx ≠ 0 or r8d < 0`, and `ecx < 2` signed. **Exact.** |
| **U4** the pulse reset | `002FEAB0` is 10 bytes: `xor eax,eax / mov qword ptr [rcx+0xEAC], rax / ret`. **Exact.** |
| **U6** the ×1.5 belongs to +0x2B | `0023AB5F movzx r12d, byte [rsi+0x2B]` → `0023AB8A cvtdq2ps xmm7` → `0023ABAD mulss xmm7, [const]`. **Agrees**; the class-0 attribution rests on the branch, not re-derived. |

**Not re-derived** (accepted at the section's stated fixture scope, not independently): R1, R4,
R5, R6's full flag mapping, R7 (the section itself withholds it), U1, U5.

### What the rewrite DROPS — must be restored, or each removal justified, before publication

`CONTRACT-apply-result-to-target.md` (2,226 → 1,781 words; §13 renamed "Validation and
adjudication"):
- **ORACLE's executed EXP-148/149 specifics in §13** (committed `2a0576abe`, `5fb38711d`): the
  per-level stat folds `002F9A60`/`002F9B20`/`002F9BD0` with the last-iteration `0030FED0(unit,0)`;
  `00316A50` as a two-path field writer driven by the `00D10460` descriptor table; the lethal chain —
  HP delta → `00377C20` can-die consult → `0030E360(bit0, mode3)` → `d64|=1`, killer id
  `d[tgtRec+0x30]=d[srcRec+8]`, member kill counter `w[flagobj+8]++`, the `00312280` arm, the
  `0032A150`/`00306F00`/`003299B0` credit chain, and revive. The EXP ids survive; **the executed
  facts do not.**
- The §2 interface row `00311608`–`00311777` (the dispatch that translates record state into the
  setters' flag words).
- **Invariant I11** (named in §12's reproduction guidance at HEAD line 151).

`CONTRACT-battle-unit-construction.md` (1,771 → 1,650 words):
- §2's id split citation `0023A580`–`0023A594` and the teardown row (`BattleUnit_TeardownAndDespawn`
  calls with `0xFFFF`; *tear-down is "apply no definition"*, `00300F6D`).
- I2's reset site `0023A5B0` and I5's party-path `rbp = 0` site `0023AAB1`.
- The EXP-047 note (the two re-key wrappers' local stores were executed).

A correction that removes the evidence for the claims it keeps makes the contract weaker than the
one it replaces. **Restore these, then publish**; OPUS will re-verify the merged file.

## ORACLE's three requests

`REQ-OPUS-APPLY-RESULT-CALLEES-FINDINGS`, `REQ-OPUS-APPLY-RESULT-WHOLE-FINDINGS` and
`REQ-OPUS-UNIT-INSTALL-FINDINGS` ask the owner to confirm or restate §13/§14 of these same two
contracts. **They are blocked on this merge**: the text they point at is exactly what the overlay
rewrites, and part of it is what the overlay drops.
