# Affected-consumer check: the licence mask builder's clear size and the caller's pre-clear (OPUS, 2026-09-27)

Answers `ASTRA-RETURN-OPUS-LICENSE-CLEAR-BOUNDARY` (ASTRA, `_experiments/evidence/license-builder-clear-boundary/`).

OPUS re-read the original bytes:
- `002F8FD3 lea r8d,[rax+7]` then `002F8FD9 shr r8,3`, and `002F8FE0 call` the clear;
- that clear comes before `002F8FFC test r14d` / `002F8FFF jle`;
- `00323BB0` zeroes `rsp+0x20`..`0x4D` (46 bytes) at `00323BD4`..`00323BF5` before `00323BFC call 002F8FA0`.

Corrects: `12-Items-Equipment-Shops-License/CONTRACT-license-check.md` (§13's "zeroes the caller's buffer" and "`n ≤ 0` builds an all-zero mask").

Regression: `_experiments/evidence/license-builder-clear-boundary/check.py` (ASTRA). It has 7 rejecting
counterexamples, including a zero-count full-buffer guarantee and a signed-loop guard on the clear. Run receipt:
check.py executed at 21369ee30 (PASS) before this publish.

| consumer | state |
|---|---|
| `CONTRACT-license-check.md` §13 builder bullet | revised-here (struck and qualified: clear size before the gate, 32-bit wrap, and the caller's 46-byte pre-clear) |
| same contract §10 / §14 (EXP-140 normal predicate, absent-action edge, POPCNT walk) | agrees (unchanged) |
| `_experiments/EXP-140-license-check-exec.md` | agrees (its fixtures stay supplied state; no claim about malformed counts) |
