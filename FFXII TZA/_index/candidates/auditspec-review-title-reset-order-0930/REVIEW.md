# Audit-spec review: ASTRA title reset order (OPUS incorporation gate)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `_experiments/evidence/title-reset-order/`,
`capture-title-reset-order.py`
Board task: `OPUS-REQ-AUDITSPEC-ASTRA-TITLE-RESET-ORDER-0930`

## Verdict: ACCEPT

## What was checked

- **Prover re-run fresh:** `prove-title-reset-order.py` → "Candidate cleanup
  precedes state clear; RDX/AL ABI and local tail writes qualified.
  Initialization OPEN."
- **Independent byte verification of `00611F80`** (certified image, capstone):
  - incoming object arrives in **RDX** (`mov rbx, rdx`) ✓
  - cleanup calls `62B100`, `62BCB0` run **before** the local clear ✓
  - the post-cleanup count `[rbx+0x30]` (bit-31-clear value, `cmp ecx,1; jbe`)
    plus `[rbx+0x38]` non-null gate the optional `call 584730` ✓
  - `xor eax; [rbx+0x38]=0; [rbx+0x30]=eax` — +0x38 and +0x30 cleared on the
    single normal path **before** `call 5DE290` ✓
  - return is `mov al,1` only; the tail after `5DE290` makes no local count
    writes ✓
- **Scope:** initialization remains OPEN; the record claims the ordering/ABI
  contract, not full lifecycle — correctly bounded for the OPUS incorporation
  gate it feeds.

## Narrowing / notes

None required.
