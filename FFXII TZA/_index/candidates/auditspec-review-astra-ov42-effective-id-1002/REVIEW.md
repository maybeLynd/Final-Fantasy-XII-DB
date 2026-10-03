# SWE2-AUDIT-SPEC review: ASTRA OV-42 effective-ID source

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-EFFECTIVE-ID-1002` · Package: `_experiments/evidence/ov42-effective-id-source/`
(publisher commit `2cce275ad`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00387090` (`BattleRuntime_GetEffectiveActionId`):**
  - Table selection: when `rcx` is non-null and `byte +5 == 0` it uses `0208D480 + 64*byte[+4]`; otherwise the first
    owner O1 = `31B860(rcx)` gives `0208DE80 + 64*byte[O1+EA9h]` (0 when O1 is NULL). O1 is also stored to
    `02EBF188`.
  - It then resolves the **second** owner O2 = `31B860(rcx)` (`003870EC`).
  - Only `WORD[O2+714h] == 9Fh` with a non-null table substitutes `WORD[table+10h]`. Otherwise it returns the
    zero-extended `WORD[O2+714h]`.
  - Candidates 511..534 therefore pass unchanged on the direct leg. There is no local bound.
- **`0031B860`:** a NULL query returns 0 before any registry call (`0031B86E`).
- **No safe sentinel:** when O2 is NULL, `je 387118` still executes `movzx eax, word [rax+714h]` with `rax` = 0, so
  there is no safe sentinel return. This is a precondition, not an observed fault.
- O1 == O2 is not assumed; the two calls are separate.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` re-run: exit 0, output **byte-identical** to `result-01.json`.
- `control.py` re-run: `control-result-01.json` **byte-identical**. Its four CLI refusals include the failed
  feasibility with output present.

The upstream `+714h` writer and admission, normal reachability, owner registry, table binding and lifetime stay
OPEN.
