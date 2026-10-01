---
experiment: EXP-031
title: Loaded-state control of the exact private deadline capture
status: PARTIAL — fresh live positive; original matched campaign incomplete
method: C
live_game: true
contract: none - debugger instrument validation in a loaded state. PARTIAL, and its finding is about the capture's timing, not about anything the game guarantees.
date_designed: 2026-09-11
---

# EXP-031 — loaded-state deadline cleanup control

## Separate follow-up completed; timing deviation retained — 2026-09-13

[Fresh PID11032](evidence/EXP-031-loaded-deadline/matched/README.md) recorded197
entries with the same one-second candidate,102 clear/readback contexts and detach.
Baseline/capture/post65s windows all completed, including6235 debugger-absent samples
in the separate post window with repeated CPU advancement. Guarded Enter/C and
menu screenshots establish responsiveness before and after attachment and after the
full follow-up. Normal exit, PC reset and26-file hash restoration passed.

Actual Enter offsets36.4088/54.6486/58.2556s and C offsets67.5575/68.2464/76.7840s
are not matched. The original campaign remains short of that requirement; this
is a bounded liveness positive with the missing full-post observation now supplied
in its own fresh run. No quantitative overhead, general debugger safety or handler
promotion follows. Do not repeat interactive timing blindly; independent scoped
review must assess these limits. Historical runs and omissions remain below.

## Fresh continuation — 2026-09-13

[PID40504 recovered evidence](evidence/EXP-031-loaded-deadline/recovered/README.md)
preserves195 actual003A1C50 entries from the exact EXP-030 one-second candidate,
successful stopped-event clear/readback of101 threads and detach. A fresh65s
baseline and65s capture window include20.9443s of sampled debugger absence and
advancing CPU after detach. Subsequent guarded Enter/C registered49/2 and visibly
opened/closed the menu. Normal exit, PC-control reset and all26 original/backup
hashes were verified. No combat or handler claim follows.

The input timings were not matched and a separate65s post window was omitted
before exit. The [derived record](evidence/EXP-031-loaded-deadline/recovered/observation.json)
therefore retains a **bounded positive with the original campaign INCOMPLETE**.
These missing controls are not waived. The fresh receipts are separate from the
historical interrupted run below; no later run is attached to an old baseline.

## Historical checkpoint and interruption — 2026-09-11

Fresh PID13964 loaded the named Stepping save with Vaan at HP103. Executable,
module and live selected-text identities passed. The no-attach baseline completed
65seconds with6154 samples, foreground controls, debugger absent throughout, and
accepted Enter/C input with held indices49/2 and clear release receipts. A screenshot
shows the command menu opened. The subsequent screenshot request was stopped by
the user's physical Escape key; menu-close visual proof was not collected. No
armed capture or post-capture window ran. This is incomplete evidence, not a failed
debugger test and not a runtime validation of EXP-030.

On continuation, PID13964 was closed. Ordinary cleanup rejected the changed
GameSetting.ini before restoring: alongside LUIDLow, the four window-position
values WindowPosX/WindowPosY/LastX/LastY differed. Inspection verified those were
the only differences in the sole changed file. The configuration was preserved in
ignored EXP031-config-before-restore, then all26 original hashes were restored.
The runtime reservation is released. A future attempt requires fresh state and
matched controls; do not silently append a later capture to this baseline.

[Raw receipts and exact sources](evidence/EXP-031-loaded-deadline/manifest.json)
are retained. [Validation](evidence/EXP-031-loaded-deadline/validation.json) explicitly
reports INCOMPLETE and lists the missing windows and screenshot. No handler or
debugger-safety claim is promoted. The original design follows for reproducibility.

## Original prospective design

EXP-030's exact private duration-only capture passed cold and positive disposable
controls. This experiment tests whether a brief armed deadline capture preserves
responsiveness in the known Stepping save. It does not measure combat handlers or
enemy deaths. No runtime validation is claimed by this design.

Use a fresh, verified reference process and the named level1 Stepping save. Back up
all26 existing save/config files and verify their hashes before launch. Reserve
runtime before any launch, driving, attachment or close. Preserve the actual process
PID, full executable/module/selected-text identities and input read control.

Adapt EXP-018's matched65-second observation windows: baseline without attachment,
capture window, then post-capture window. Send Enter at5 seconds and C at50 seconds
in each window, using the established input/focus receipts. Preserve menu-open and
menu-closed screenshots, held-key release and foreground controls. Compare repeated
CPU intervals; one CPU total is not a liveness verdict.

In the capture window launch the unchanged EXP-030 CLI at approximately2 seconds,
with angle entry003A1C50 armed alone for1 second after initial debugger readiness.
The duration limit, rather than hit count, must initiate cleanup. This reuses a site
with a prior positive loaded-state control while bounding breakpoint load. It is
not a cold-handler negative control. Inputs occur after the brief capture; this
tests post-detach responsiveness rather than input delivery while attached.

Required outcome: positive entry hits, all capture/cleanup API gates pass, cleanup
at the requested stopped event, successful detach, debugger absent afterward,
working menu input and advancing CPU over repeated post intervals. Capture errors,
identity changes, unmatched focus/input or missing receipts invalidate promotion.
Keep any failed run and stop to classify it; do not repeat a frozen target blindly.

After the final window verify reference code/module identity, close only the owned
process and restore original save/config hashes. Only the previously understood
GameSetting.ini LUIDLow rewrite can be restored by the ordinary recipe; other
changes require inspection and preservation before restoration. Release runtime.

The result, if successful, would validate this exact instrument in one loaded state
for this brief positive capture. It would not establish arbitrary exception safety,
long armed windows, combat reachability or the truth of an unobserved handler zero.
