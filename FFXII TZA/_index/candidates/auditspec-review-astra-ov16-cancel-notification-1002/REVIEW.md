# SWE2-AUDIT-SPEC review: ASTRA OV-16 request-cancel notification

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV16-CANCEL-NOTIFICATION-1002` · Package: `_experiments/evidence/request-cancel-notification/`
(publisher commit `011e013c7`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00352980`:** pops one value into EDX and calls `3DB420(rdx_object, edx, r8d=4)`, then tail-calls `3DB6E0`.
- **`00353660`:** pops v, then pops a second value and resolves the actor with `264010`. It calls
  `3DB420(actor, v+1, 4)`, then tail-calls `3DB6E0`. Both use mode 4.
- **`003DB420` (`ActorResource_RecycleEntryRange`, 130h = 304 bytes; its first `.pdata` fragment covers only
  28 bytes):**
  - With mode 4, `r14d` = 0.
  - It walks channels from `byte [+88h]`-1 down to `max(edx,0)` (`dec rbp`), and only channels whose bit is set in
    WORD `+6`.
  - Along each channel list it skips entries with `byte +11h == 0` and removes the **first** non-zero one through
    `3DB2A0`. That is at most one entry per channel considered.
  - It returns `EAX=1` on every normal path, including NULL, empty and no-entry paths. That 1 is not a
    removal or delivery result.
- **Composition with `3DB2A0`** (see the OV-10 review): a valid head in mode 3 with a non-`8000h` requester reaches
  the end-notification attempt with no target-interpreter call. Receipt, admission, delivery and consumption stay
  separate.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (prove-02, `464d9c0c`) re-run: exit 0, output **byte-identical** to `result-01.json`.
- `control.py` (`8b44795f`) re-run: `control-result-01.json` **byte-identical**. Its four CLI refusals include the
  truncated first unwind fragment.

## SWE2-AUDIT-SPEC consumer note

The "channel" argument is the **lower bound** of a descending range `[max(v,0), count-1]`, where v is the popped
value for `352980` and the first pop + 1 for `353660`. It is not a single channel. Page 3's "RET-only" wording
should be qualified as the package asks.
