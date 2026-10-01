# SWE2-AUDIT-SPEC review of SD-5 (sd5-display-requests-0930 at ce2b4380d): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Author: OPUS.
Reviewed: commit `ce2b4380d`, record [`sd5-display-requests-0930`](../sd5-display-requests-0930/README.md). Static, the
certified image. Request: `OPUS-REQ-AUDITSPEC-SD5-0930`.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD5-0930 | sd5-display-requests-0930 | `ce2b4380d` | ACCEPT |

**Re-run.** `sd5_display_requests.py` re-run from its own directory
([`rerun_sd5_display_requests.out`](rerun_sd5_display_requests.out)). Every line is identical to the committed `.out`
(ignoring CR) except the timing on line 1 (307 s committed, 317 s here). Control P PASS. No tracked file changed.

**Re-derived independently** (my own scripts; none uses the SD-7 value-flow engine):
- **The failed-resize path** ([`sd5_indep.out`](sd5_indep.out), linear dump of `0079C4A0`-`0079C5C5`). `0079C4CE`
  tests `+0x1E`; the pass stores the size at `+0xD24` / `+0xD28`, then `0079C526 call [rax+0x48]` (slot 9). A non-zero
  return logs through `005CDAA0` and `0079C549 jmp 0079C69E`, which is the epilogue (restores and pops). The only clear,
  `0079C54E mov byte [rdi+0x1E], 0`, is on the zero-return path. Holds.
- **Slot 9.** The game vtable `008C5760` holds `0017D0C0` at slot 9 and the base vtable `01CB2508` holds `007A05D0`.
  `0017D0C0` copies `+0xD24` / `+0xD28` into the object from `00189120` and ends `jmp 007A05D0`, so its return value is
  the base's. Holds.
- **The three setters have no caller** ([`sd5_indep.out`](sd5_indep.out)). Raw rel32 sweep of all `.text`
  (E8 / E9 / 0F 8x), rip-relative references and DIR64 relocations for `007A0B10`, `0079F140` and `007A1180`: **0 branch
  references, 0 rip references**. Each has exactly 2 relocations, and these are slots 12 / 13 / 18 of the two vtables
  above. Indirect calls through `+0x60` / `+0x68` / `+0x90` in the framework range and `0017xxxx`: 12 sites. They go
  through other objects (`[r13+0x78]`, a COM-style `[rsp+0x70]`, `SteamController_PollState`'s interface), except the
  generic thunks `0017F150` (`jmp [vt+0x60]`) and `0017F250` (`jmp [vt+0x90]`). [`sd5_thunks.out`](sd5_thunks.out):
  each thunk has **1** raw caller (`0053BECB` in `0053AB50`, rcx = `[rax+0x6B8]`; `00477E2E` in `00477B10`), and
  neither owner references the application holders `01F7E350` / `02EA5368`. Holds.
- **The start-up setter writes the application.** `0079E5ED call 0079F150` loads rcx from `[02EA5368]` (the framework's
  application pointer), and `0079F19E` stores `+0x1E` = 1. Holds.
- **The `007A07C0` hit is the window data.** `0079E520` passes its rcx (`00798616 lea rcx, [rbp-0x40]` in `007980A0`)
  unchanged into `0079B300` (`0079E53C` / `0079E53F`). There `0079B330 mov r13, rcx` and `0079B6EA` call the import
  `SetWindowLongPtrA` (IAT `008C2878`, name read from the import thunk) with `edx = -21` (`GWLP_USERDATA`). Holds.

**Controls.** Control P (the pass gate's five reads are found) proves that the value-flow census reaches the pass. It is
not sensitive to a missed *setter* route. The setter claim instead rests on the SD-7 route set, which the record
states. My raw-reference sweep above is the missing completeness control, and it agrees.

**Precision notes for the record (non-blocking; the answer is unchanged):**
1. The table credits slot 12 `007A0B10` with `+0x20` only. It also stores `+0x1E` = 1 (`007A0B16`), and the census
   `.out` lists this. Since slot 12 has no caller, the answer does not change.
2. `0079B6EA` does not pass rcx itself. It passes `movsxd r8, r13d` (`0079B6E2`), the pointer truncated to 32 bits and
   sign-extended. The stored user data is the window-data object only while that stack address fits in 32 bits.
   This matters to anyone reading the window procedure's object as a full pointer. It does not bear on SD-5.
