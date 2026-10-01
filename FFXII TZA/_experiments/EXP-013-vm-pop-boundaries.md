---
experiment: EXP-013
title: Original-code controls for integer and float VM pop boundaries
status: COMPLETE
contract: ../01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md
tool: evidence/EXP-013-vm-pop-boundaries/probe.py
method: B - isolated original-code execution
live_game: false
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-013 — the two pop error paths differ

## Question and predictions

FABLE's static correction says integer pop is silent on an empty stack and reports unknown
tags; float pop reports an empty stack and is silent on unknown tags. The prior shared empty-stack
error description was wrong. Independently test those four paths, depth changes and coercion
using the original instruction bytes, with a positive control for the error-call recorder.

## Method, state and identity

Original `00267E10` (78 bytes) and `00267DB0` (84 bytes) execute in Unicorn 2.1.4. The reader
rejects an executable other than SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Code hashes, reader/probe hashes, instruction addresses, error arguments, VM-memory writes,
before/after bytes and expected/observed returns are in
[observations.json](evidence/EXP-013-vm-pop-boundaries/observations.json).

Each call gets a fresh synthetic 0x284-byte stack object with depth at +0, tag at +4 and payload
at +0x184; all other bytes start at 0xA5. Seven states per pop: depth 0, depth -1, tags 0/3/255
at depth 1, integer tag 1 with payload 42, and float tag 2 with payload 2.75. Negative depth and
unknown tags are controlled invalid-state interventions; no claim of their live reachability.

`008620C0` is a **ret stub**. Its entry/ECX/depth are observed; native reporting effects and
whether it returns in every real environment are not executed. The parent must reach the expected
return sentinel with the correct stack pointer within 100 instructions. The whole VM object is
compared, so an unexpected write outside depth would fail the control.

## Observations and falsification

All 14 calls reached their return boundary and matched the predicted values and bytes:

| Case | Integer pop | Float pop | Depth |
|---|---|---|---|
| Empty / negative | 0, no error call | +0.0, one `008620C0(1)` | unchanged |
| Unknown tag 0/3/255 | 0, one `008620C0(1)` | +0.0, no error call | 1 → 0 |
| Integer 42 | 42, no error | 42.0, no error | 1 → 0 |
| Float 2.75 | 2, no error | 2.75, no error | 1 → 0 |

The reporting float-underflow and integer-invalid-tag paths are relevant positive controls for
the silent paths. Those negatives therefore mean no error-handler call within these executed
bodies, not an unproven empty trace. Only depth changed in positive-depth cases; the remaining
object bytes stayed identical. The shared empty-stack-reporting hypothesis is contradicted.

## Result, limits and dependencies

This corroborates FABLE's corrected contract and calling-convention page with isolated execution
of original code. It is not live-game behavior, a reconstructed implementation, full VM parity,
or evidence about the native error handler's effects. Return values after a stubbed error call
are conditional on that handler returning. No game, debugger attachment or production state was
used; the only persistent outputs are this bounded probe and its receipts.

FABLE's existing correction remains authoritative for documentation integration. This adds an
independent method, not an independent whole-system audit. Current canonical correction:
[bridge contract §10](../01-Script-VM-Native-Bridge/CONTRACT-script-to-native-bridge.md#10-failure-paths-and-edge-conditions).

The exact reader used is preserved as
[reader-snapshot.py](evidence/EXP-013-vm-pop-boundaries/reader-snapshot.py); its SHA256 matches
the observation receipt. To reproduce the historical run, use that snapshot as
`diff_group_completion.py` in a private copy of the original directory layout. Preserve the
original observations and direct new output to that private copy.
