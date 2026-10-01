---
experiment: EXP-010
title: Does the current no-arm debugger control preserve a loaded-save reference process?
status: COMPLETE
contract: none — state-dependent instrument validation (RT-1)
tool: Database/Tools/analysis-kit/gfz-scripts/hwbp.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-010 — loaded-state no-arm control

## Question and distinguishing observations

Compare a clean loaded-save no-attach baseline against the current `hwbp.py --no-arm` in
the same named loaded state, with matched focus/input and repeated post-detach observations.
The historical control survived pre-load; that does not settle the loaded-save failure in RT-1.

H1: this no-breakpoint control itself wedges a loaded-save process. H2: it survives, narrowing
the next test to armed capture or its interaction with this state. A CPU sample alone does not
establish either: record CPU rates repeatedly plus actual input/state responsiveness and read controls.

## Existing evidence and instrument boundary

[ASTRA's triage](../_index/_inbox/ASTRA.md) cites the two loaded-state armed failures and the
pre-load survivors in PROGRAM-STATE section 4bk. Those observations are inherited, not repeated here.

**Source inspection before this run:** current `hwbp.py --no-arm` sets `slots=[]`, but the
CREATE_PROCESS/CREATE_THREAD/timeout paths still call `set_slots`, and cleanup calls it again.
That helper clears DR0–DR3/DR6/DR7 using `SetThreadContext`. The CLI wording "programming NOTHING"
therefore overstates isolation. This experiment tests that exact implementation unchanged;
it does not separate attachment/event handling from those debug-context writes.

## Initial state, controls and action

- Preserve existing save/config files and record their hashes before launch.
- Use the designated clean Steam reference, authorized executable SHA256
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- Record exact instrument hashes, command arguments, time windows, full live module list,
  actual module base and relevant live code identity. Refuse mismatches/unreadable controls.
- Launch with the existing runtime wrapper; use the existing known-save recipe, verifying each
  menu transition and named loaded state visually and through the runtime state/read controls.
- Keep save/area, menu state, focus and input procedure matched across the baseline and no-arm
  window. Test responsiveness using a reversible menu transition rather than a zone transition.
- Record repeated CPU/read/input observations before, during, immediately after, and after a
  settling interval following a bounded no-arm run. Do not interpret elapsed setup as loaded time.
- Retain failed observations. Close only the reference process created for this experiment,
  verify exit, compare save hashes and release runtime ownership.

## Evidence and result

Raw receipts and outputs: [EXP-010-RT1](evidence/EXP-010-RT1/).
**Result: the current no-arm implementation survived this loaded state in the recorded module
environment.** The authority-matching shipped reference's no-attach
baseline and 30-second no-arm window used the same PID 23532, autosave (00:08:42), area 227,
position, focus, and Enter/C command-menu sequence. A subsequent 45-second no-arm window
resolved a screenshot-timing gap by leaving the menu open until capture. It is a within-session
follow-up, not an independent clean-launch replicate. No armed breakpoints were tested.

### Observations, controls and normalization

- `loaded-state.jpg` shows Vaan in Dalmasca Estersand; `save-list-confirmed.png` identifies
  The Stepping autosave. State receipts show `IN-WORLD`, area 227 and populated save bytes
  `e70993b10100000096000000d3020000` before/after the paired windows. The free SCRIPT-table
  slots are not interpreted as an unloaded world.
- Every promoted observation window has the authorized disk executable hash, full module paths,
  actual image base, known read-control bytes, and full live `.text` bytes matching the disk
  section. **The module classifier's `clean` verdict is narrower than an overlay-free process:**
  `gameoverlayrenderer64.dll`, `nvspcap64.dll`, and `DiscordHook64.dll` were present in the menu,
  baseline, attached and post windows. Their paths are retained in every receipt. These are
  ambient instrumentation and were not removed or varied, so this does not certify a process
  free of external hooks. Unchanged game `.text` does not rule out hooks in other modules/data.
  Sources used by the runs are preserved by hash in `sources/`.
- The same held-key method (350 ms; virtual-key and scan-code forms together) delivered Enter
  at input index 49 and C at index 2, with zero no-key baseline and no held bytes after release.
  Both forms were accepted by SendInput; which form the game consumed is not distinguished.
  All samples in the five promoted observation windows had foreground PID 23532.
- `baseline-during.jpg`, `attached-open-confirmed.jpg`, `attached-close-confirmed.jpg`, and
  `post-open-confirmed.jpg` establish actual menu consequences separately from held-array bytes.
  The attached screenshot timestamps fall inside the independently measured debugger-present
  interval; `summarize.py` asserts that condition. `CheckRemoteDebuggerPresent` is false in
  both post windows. This externally verifies detach, whose API return hwbp itself ignores.

| Window | Duration | Five-second CPU ranges (% of one core) | Debugger present |
|---|---:|---:|---|
| Matched no-attach baseline | 35 s | 42.32–47.90 | no |
| No-arm comparison | 35 s observer / 30 s debugger | 46.98–51.40 | observer seconds 1.96–32.09 |
| First post-detach | 35 s | 46.34–51.04 | no |
| Visual follow-up | 50 s observer / 45 s debugger | 49.11–54.53 | observer seconds 1.96–47.00 |
| Final post-detach | 15 s | 45.36–51.41 | no |

These are process CPU rates, not frame times, engine scheduling parity or proof of every thread's
progress. Small window endpoint differences are retained in `normalized.json`. No declining-to-zero
post-detach sequence occurred. The visual/input controls, not CPU alone, support responsiveness.

### Failed controls and interpretation corrected during the run

The initial sandboxed wrapper launch could not establish readable readiness; its reported process
later exited. The authoritative OS check confirmed absence before the explicit interactive launch.
Subsequent runtime reads required the elevated execution context: sandbox unreadability was not
classified as reference contamination. `launch.json` retains the failed setup.

Brief UI key presses and one initial held probe did not advance the title menu. After focus/setup
work, the held probe produced positive input bytes and actual menu transitions. The earlier zeros
do not prove a different input array or native behavior. `save-list.png` is misnamed: it still shows
the title menu; `save-list-confirmed.png` is the successful save-list proof. The legacy probe's
"real negative" wording and claim to open only read permissions are not promoted (it uses RW).

`noarm-during-enter.jpg` and `post-enter.jpg` were initially suspected to show failed menu response.
Receipt/file timestamps prove they were captured **after** the scheduled C close action. That
interpretation is retracted; both images are valid closed-menu observations, not negative evidence.
The explicit visual follow-up closes this observation gap. Original images/receipts are retained.

### Falsification, consequence and limits

The hypothesis that this current no-arm implementation necessarily wedges this loaded state is
contradicted. The next discriminating runtime package is an armed capture bounded by hit count in
the same saved state, with its own entry/return and post-detach controls. Attach/event handling and
debug-register clearing are still combined here; survival does not identify the armed failure's
cause. A stricter overlay-free reference needs its own environment control; the existing wrapper
does not establish that property. No debugger event-loop rewrite is justified by this result alone. Historical armed failures
remain unresolved. Exact live behavior elsewhere, callback scheduling and producer ownership are
not established by this experiment.

### Cleanup and affected records

`cleanup.json` confirms only the designated PID was present before close and none remained after.
All save bytes remained unchanged. The game rewrote only `GameSetting.ini`'s adapter `LUIDLow`
(79439 to 78642); the hash-verified backup was restored after exit. `restore.json` confirms every
saved/config file then matched the pre-run hash census. Runtime ownership was released immediately.

Affected active descriptions: `hwbp.py` help/docstring, runtime methodology §8d, and ASTRA's inbox.
The first two now describe DR clearing and the state-bound evidence; the instrument implementation
is unchanged. RT-1 remains open for armed capture. No isolated emulation, stubs or reconstruction
results are represented as live evidence.

Reproduction: use the checked-in `window_run.py` commands in `baseline-run.json` and
`noarm-run.json` after establishing the named save, then `--mode post`. Use `--mode visual`
only for the explicit visual gap and capture the open menu before sending C. Those scripts require
the existing runtime environment and a separately verified reference PID; they do not load saves.
`input_receipt.py` records the narrow extension which adds the displayed C Back key, prints OS
delivery results and guarantees release. Raw receipts, normalization and interpretation are separate.
This bounded test cannot prove a general engine law, full debugger correctness, scheduling parity,
or a cause/cure for every historical stall.
