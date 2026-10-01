---
experiment: EXP-018
title: Two-hit stopped-event cleanup with checked debugger-exit policy
status: COMPLETE — bounded two-hit liveness observation
contract: none — diagnostic instrument validation
tool: private hwbp variant based on EXP-017 repaired source
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-018 — repeat the candidate after correcting exit-policy setup

[EXP-016](EXP-016-trap-cleanup-order.md) showed sustained input after clear-before-
continue in one loaded session. Its same-proxy old-order comparator had a visible
hang but failed to deliver the required input control. [EXP-017](EXP-017-debugger-exit-policy.md)
then corrected a separate pre-attach policy defect. This experiment asks whether
the early-clear candidate still preserves input on that corrected setup. It is
not a repeat of the invalid comparator and does not claim to isolate causality.

## Intervention, controls and falsification

Use the private [source package](evidence/EXP-018-cleanup-policy/). The hash-guarded
generator retains checked post-attach policy, adds buffered API receipts and the
same two-hit early-clear branch. Policy setup failures now save receipts before
main aborts. Shared cleanup remains unchanged. Event fixtures cover old versus
early-clear order, failed clear/fallback, and policy failure without context work.
These fixtures are simulated control flow, not live observations.

Reserve runtime only when ready. Back up and hash all save/config files. Launch
the verified Steam reference, load The Stepping autosave (00:08:42, Vaan level 1),
explicitly dismiss Load complete, and obtain a field screenshot before baseline.
Area 227 and save head are supporting checks, not substitutes for that screenshot.

Run 65-second baseline, two-hit angle entry/ret-site capture at 003A1C50/003A1C8C
with a ten-second limit, and a separate 65-second post window. Require successful
attach then policy, both hits, every final-event clear, resume/continuation and
detach. Require Enter/C bytes 49/2 with visible command menu open/close in all
three windows, valid focus/read controls, code identity, and debugger absence
after detach. Record all five-second CPU intervals and loaded overlays.

H1: checked-policy early-clear preserves sustained input in this session. H2:
input fails despite successful prescribed operations. Missing hits, any relevant
API failure, timeout, failed foreground/key delivery or missing visual controls
make the affected comparison incomplete, not H2. A timeout fallback is not the
stopped-event path and cannot qualify as candidate validation. Preserve failures;
poll original child handles and obtain terminal state before any new attempt.

Close only the owned reference session, verify exit, restore any changed save/config
files from the exact verified backup and release runtime. H1 would support bounded
use of this two-hit candidate, not arbitrary-duration captures, all cleanup paths,
general debugger safety, or pending semantic requests without their own controls.

## Preparation checkpoint

At preparation, private sources were derived from the policy repair; there was
no game observation or production cleanup promotion. The completed run follows.

## Live result after preparation

Fresh reference PID **38756**, matching Stepping save and area **227**, completed
all three windows. `save-list-ready.jpg` is the named-save proof; `save-list.jpg`
was captured during the preceding title transition and is retained under its
original filename. `loaded-field.jpg` proves the field after explicit modal dismissal.

The exact variant SHA256 is
`81a8510288dc5a4e1d93c221659c49926039e66aa277da3f1fea59aa193879f6`.
The trace has one pair on thread **13220**, XMM0 **-3.13068414** at entry and ret-site.
Attach and subsequent False exit-policy setup both returned 1. All **103** enumerated
threads were cleared successfully before final continuation; no fallback clear ran.
The receipt records 314 GetThreadContext, 312 SetThreadContext and 209
ContinueDebugEvent successes, successful detach, and **no recorded API failure**.

| Window, each 65 s | Five-second CPU fraction of one core | Held input and menu |
|---|---|---|
| Baseline | 0.444–0.571 | Enter/C indices 49/2; visible open/close |
| Two-hit capture | 0.444–0.569 | Same indices; visible open/close after capture |
| Separate post | 0.471–0.512 | Same indices; visible open/close |

All windows had zero foreground misses, ended with no held bytes and no debugger,
and matched the full compared executable .text bytes (7,996,981 bytes, SHA256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`).
Nine external samples observed the brief capture attachment; none saw a debugger
in baseline or separate post. Source receipts match the tools actually run.
Steam/NVIDIA/Discord overlays remain in the captured module lists. The reference
classifier's clean verdict does not mean overlay-free.

H1 is supported **for this two-hit capture in this loaded state**. The result adds
a successful live checked-policy setup to EXP-016's early-clear liveness evidence.
It does not establish cleanup ordering as the sole cause of the old failure, repair
the incomplete old-order input control, or validate timeout/failed-clear paths.
The shared cleanup code is unchanged; use the private candidate only within its
observed scope and continue to require per-session controls.

PID 38756 exited. Only adapter LUIDLow changed (79439→78642) in one GameSetting.ini;
the exact backup was restored. `restore.json` verifies all **26** save/config hashes
match. Runtime is released. Three event fixtures pass, including retention of a
policy-failure receipt before abort. Raw receipts, source versions, screenshots and
normalized observations are preserved separately from this interpretation.

Next: the pending read-only group-ledger observation can proceed without relying
on unvalidated arbitrary-duration hardware-breakpoint cleanup. Retain the latter
limitation for the handler-reachability request rather than broadening this result.
