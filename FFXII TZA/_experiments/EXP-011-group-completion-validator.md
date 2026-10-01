---
experiment: EXP-011
title: Does the group-completion differential detect callback and output-boundary defects?
status: COMPLETE
contract: ../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md
tool: Reconstruction/Tests/Differential/diff_group_completion.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-011 — observable group-completion callbacks

## Question, hypotheses and existing defect

The prior comparator claimed callback count/order coverage but reduced the three prologue calls
to `any(...)`. Its driver counted one aggregate hook, discarded dispatch's unit argument,
silently truncated its event buffer, and the comparator used unchecked `zip` streams. Unicorn's
instruction limit could end emulation without reaching the expected return address. Thus its
green result did not prove the advertised callback equivalence.

H1: a wrong prologue identity/order/count/argument or callback-visible memory order can survive
the old observation boundary. H2: an exact invocation record, output census and return-boundary
check distinguish those faults while preserving a matching unmodified probe. This experiment
repairs and challenges the instrument; it is not live original-game evidence.

## Original-code authority and scope

Reference executable SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The tool rejects a different executable or image base. Function `00306F00` (303 bytes) and helpers
`00263D30` (8 bytes) and `002360D0` (39 bytes) execute under Unicorn 2.1.4 at original addresses.
Their byte hashes, driver executable hash, adjacent source hashes and commands are in each receipt.
Source hashes alone do not attest a compiled driver: the bounded-control build receipts tie each
driver hash to the exact copied source set and compile command. Snapshots preserve source versions.

A fresh disassembly confirms calls at `00306F9A`, `00306FA4`, `00306FAE` to `00307140`, `00238B70`,
`00238AE0`, each with ECX=1. Dispatch at `00306FE8` or `00307012` receives the unit pointer,
EDX=`0x2005`/`0x2008`, and R8D=0. Only these defined arguments are compared; incidental volatile
register contents are not invented as parameters. The parent returns 0/1. Callee return values
are ignored here; the native callee bodies, their outputs, ownership effects and scheduling are
**not executed**. Four `ret` stubs remain explicit on the original-code side; hooks remain explicit
on the reconstruction side.

## State, actions and controls

Both sides receive the same synthetic ledger, units, map and record regions, including boundary
slots 31/32, null unit, out-of-range bkei, and the truncated group-64 ledger. The same seed
20260908 and 48 units generate 100 ordered calls, with repeated unit calls and planted cases.
This is 100 calls in one constructed state sequence, not 100 independent game states.

The probe now calls each prologue hook separately with the original callee identity and argument.
The driver does not fabricate three events from one aggregate callback. Its schema records case
index, unit, result, ordered invocation list and memory digests at callback entry and parent return.
Dispatch includes its third argument. A full buffer is an invalid run, not a shortened log.

The comparator rejects missing/surplus/reordered case output before pairing records. Original
execution must stop at the expected return sentinel with RSP advanced by eight bytes. It compares
exact invocation records, per-boundary FNV digests and byte-for-byte final region contents. The
digests are bounded state fingerprints, not a claim of mathematical collision impossibility.
It retains synthetic inputs, raw driver output, normalized original records and both final images.

Five adversarial tests passed: exact census/schema, callback dimensions, case identity/order,
instruction-budget exhaustion versus actual return, and reference identity rejection. A synthetic
infinite loop fails the return check; a synthetic `ret` is its positive control. These tests
exercise instrument failure modes, not substitute native semantics.

## Actual observations and falsification

The freshly built baseline matched all **100 calls / 19 completions**, including 17 dispatches of
`0x2008` and two of `0x2005`. Four completed units recur (respectively 5, 3, 2 and 3 completed calls).
Repeated masks can therefore coexist with repeated callback sequences in this stubbed execution;
the previous broad death-idempotence comment was narrowed to mask-bit idempotence.

Nine deliberately changed source variants compiled and were rejected:

| Change | Distinguishing observation |
|---|---|
| Swap first two prologue calls | ordered identities differ |
| Omit third prologue call | invocation count differs |
| Duplicate first prologue call | invocation count differs |
| Change prologue argument to 2 | argument differs |
| Change third callee identity | target differs |
| Dispatch a different unit | first dispatch argument differs |
| Change dispatch's third argument | third argument differs |
| Change arm-A event to arm-B event | event identity differs |
| Set the arm-B unit flag before prologue calls | callback-entry memory differs |

The final variant is especially discriminating: **final bytes and the old final digest still
match**, but cases 2 and 80 fail at the callback boundary. This demonstrates why final-state
equality alone cannot establish effect order. The targeted controls passed their expectations;
they are not a complete mechanically generated mutation campaign or full subsystem parity.

## Reproduction, cleanup and correction dependencies

[Evidence](evidence/EXP-011-group-validator/) contains `controls-run-1` (baseline plus seven
faults) and `controls-run-2` (baseline plus the event/memory-order faults). `validate_callbacks.py`
accepts a new `--out` directory, optionally `--only` selected control names; baseline always runs.
It uses unique temporary source/output trees, records build logs, and checks that production
sources remain byte-identical and temporary case directories are removed. No shared source is
mutated by these controls. The known-defective general `mutation_test.py` was not used.

Unicorn was absent from the existing Python environments. Version 2.1.4 was installed only in
ASTRA's scratch dependency directory; no shared environment was changed. These dependencies were
readable only in the elevated execution context. An initial build emitted three outputs in the
checkout root; they were moved into ASTRA scratch immediately. The controlled builds then used
their own temporary working directories throughout.

Affected active executable records are the group probe hook interface, driver and comparator.
The FABLE request preserves native callback semantic/ownership dependencies; the OPUS request
routes parity-scope and config/widget correction dependencies under their claims. Historical
full-effect interpretations remain unsupported: explicit invocation matching does not execute
the four native callees, prove callback scheduling, or certify live integrated behavior.
General mutation isolation/invalid verdict repair is the next independent validation package.
