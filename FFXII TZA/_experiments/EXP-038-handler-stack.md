---
experiment: EXP-038
title: stopped-event stack receipt preparation
status: PREPARED - offline controls only
contract: none - Stack-capture preparation with mocked APIs; no FF12 handler or native fixture execution in this record.
evidence_class: offline preparation
method: A - offline instrument preparation
live_game: false
execution_scope: Mocked stack receipt and capture integration controls; no native target used.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-038-handler-stack/test_capture.py
date_designed: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-038: stopped-event stack receipt preparation

**Status:** OFFLINE PREPARATION; no original-game or disposable-process debugger run.
**Owner:** ASTRA. **Date:** 2026-09-11.

## Question and evidence gap

`FABLE-REQ-ASTRA-HANDLERS` asks whether `003250F0`, `00325260` and `00325090` execute during an
ordinary fight with an enemy kill, including the first caller and top of stack. The private
[EXP-030](EXP-030-deadline-integration.md) capture records entry registers and RSP but reads no
stack memory. Those old receipts cannot retroactively supply the requested return address.

This package prepares that missing read in a private copy. It does not answer whether the handlers
execute, close FABLE's request, or replace the outstanding loaded armed-deadline control from
[EXP-031](EXP-031-loaded-deadline-control.md). Game automation remains paused pending the user's
resumption preference after the physical Escape stop.

## Instrument and intervention boundary

[capture.py](evidence/EXP-038-handler-stack/capture.py) derives from EXP-030's duration-only
candidate. [Origins](evidence/EXP-038-handler-stack/origins.json) identify the exact source copies;
`timeout_cleanup.py`, `api_receipts.py` and `hwbp-source.py` are unchanged. Shared debugger tools
and EXP-030's historical evidence were not edited.

For a recognized single-step event at a configured address, the candidate gets registers, calls
[stack_receipt.snapshot](evidence/EXP-038-handler-stack/stack_receipt.py) at RSP, and records the
result **before** `resume_past_breakpoint` and `ContinueDebugEvent`. The helper requests exactly
64 bytes with a pointer-width-correct `ReadProcessMemory` declaration. Only API success with an
exact 64-byte count returns `READ`, eight little-endian qwords and `top_qword`. Failed or partial
reads retain the API result, reported count and available raw prefix, but no interpreted qword.
Invalid ranges, exceptions and impossible counts also yield `INVALID`.

The stack status is recorded both with the hit and in the buffered API audit. A failed stack read
invalidates the overall capture even when the existing requested-break cleanup and detach succeed.
The stack helper only reads memory; the enclosing debugger still changes debug registers and
requests a cleanup breakpoint. It remains an intervention with unvalidated original-game effects.

The first qword is raw stack evidence, not automatically an attributed caller. At a verified
function entry it can be examined as a return-address candidate, but tail entry, non-call control
flow and address attribution require separate evidence. The other seven qwords are not an unwound
stack trace, and the Windows shadow space is not proof of saved argument values.

## Offline controls and actual results

Both suites passed using mocked API events and memory; no debug attachment occurred.

- [Three helper tests](evidence/EXP-038-handler-stack/test_stack.txt) check distinctive 64-bit
  values and exact raw bytes, invalid ranges without a read, exceptions and an excessive byte count.
- [Three integration tests](evidence/EXP-038-handler-stack/test_capture.txt) cover a successful
  hit, two stack failures, and the ten inherited API failures (attach, policy, arm, continue,
  resume, cleanup request, clear, register readback, breakpoint association and detach).
- The fake read requires the event to remain stopped. The positive case asserts the exact local
  order `stack → resume → continue` and retained qwords. Both partial-read and API-failure cases
  retain invalid raw receipts, reject `top_qword`, and still complete the mocked cleanup/detach.

These controls establish the candidate's tested read/ordering/error policy. They do not validate
real API behavior, handler entry identity, stack lifetime after resumption, debugger overhead,
cleanup liveness or an ordinary-fight negative result. The earlier native disposable controls apply
to EXP-030's exact source, not automatically to this modified capture. The sealed
[manifest](evidence/EXP-038-handler-stack/manifest.json) identifies the candidate and test outputs.

## Required next evidence

Before original-game promotion: run this exact candidate against a disposable positive with a
known entry return address and a cold-address control, preserve debugger/cleanup/liveness receipts,
then complete the fresh loaded-state control after UI resumption. Reserve `@runtime` for reference
work, verify executable/modules/live code and the named save state, and preserve/restore saves.
Only then observe the requested handlers during a proven ordinary fight with an enemy death,
with separate detection and liveness controls. Attribute any captured candidate to qualified
code and its actual call/transfer boundary rather than guessing the caller from pointer range.
