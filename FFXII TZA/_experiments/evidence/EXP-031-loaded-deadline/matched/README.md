# EXP-031 separate full post window — live positive with timing deviation

**Actual result, 2026-09-13:** method C, fresh PID11032, known Stepping save.
The exact EXP030 one-second trace recorded **197 entries003A1C50**, cleared and
verified **102 thread contexts**, and detached without recorded API failures.
All three65s windows exist: baseline6234/capture6234/post6235 samples. The separate
post window has no debugger-present sample and CPU advances in every10s interval.
Nine guarded inputs establish Enter49/C2 registration and clean release. Screenshots
show the battle menu opening and closing before capture, after capture and after
the separate follow-up. Vaan remains103/103. No combat command/action was executed.

Player version: the brief tracer ran, the game kept running through a full extra
minute, and the battle menu still worked. FF12 is closed, PC control is off, and
the original save/settings files are restored.

## Raw evidence and reference state

- [Environment](environment.json), [process](process.json), [source origins](origins.json),
  [Cloud OFF](cloud-before-0.jpg), [backup census](save-before.json).
- [Named Stepping save](named-save-ready-0.jpg), [Load complete](load-complete-0.jpg),
  [initialized field](baseline-field-before-0.jpg). The two transition images are not
  initialized-state proof. The camera framing varies between captures; do not infer
  identical presentation state from equal HP or code identity.
- [Invocation](capture-invocation.json), [entry/cleanup result](deadline-capture/result.json),
  [raw API receipts](deadline-capture/api.json).
- [Baseline](baseline-window.json), [capture](capture-window.json), [post](post-window.json).
  Capture includes28.3489s/2719 debugger-absent samples after detach in addition to
  the separate post window. Sampling is sequential, not atomic whole-process proof.
- [Post Enter](post-enter.json), [menu open](post-menu-open-0.jpg),
  [post C](post-c.json), [menu closed](post-menu-closed-0.jpg). Corresponding baseline
  and capture pulse/screenshot files retain the other state transitions.
- [Cleanup](cleanup.json):normal exit, no FF12 process, PC kernel reset; all26 original
  and backup hashes match. Sole LUIDLow79439→84456 config delta inspected and preserved.
- [Review](review.py) derives [observation.json](observation.json) from raw bytes.
  [Manifest](manifest.json) pins exact file bytes; local attributes prevent Git text conversion.

EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
base00120000; full mapped `.text` virtual extent7,996,981 bytes SHA256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
Each input has full code/module checks before and after, a known/null read control,
raw zero/held/release samples and a closed read handle. All original capture sources
still match the recovered source pins. The observer only adds its existing recorded
start timestamp to stdout; copied adapters disclose LF normalization.

## What remains open

| Window | Enter offset | C offset |
|---|---:|---:|
| Baseline |36.4088s|67.5575s|
| Capture |54.6486s|68.2464s|
| Post |58.2556s|76.7840s|

The original nominal20/50s targets were missed. Before attachment the plan was
retargeted to the observed baseline; even that5s tolerance was not met. All C pulses
occurred after their65s observer windows. Preserve **timing deviation**, not a matched
campaign PASS. The full separate post control is now present; do not re-list it as
missing. No timing-equivalent overhead comparison follows. Repeating this same
interactive timing method to chase a nominal match is not justified; review the
bounded liveness claim and the exact remaining qualification before another run.

The prior PID40504 record remains a separate incomplete campaign. This run does not
retroactively fill its missing interval. Neither run proves arbitrary debugger safety,
long-duration capture safety, the EXP038 stack extension, handler absence, caller
identity, target/command/action flow or combat consequences. Hardware breakpoints,
cleanup breaks and simulated input are interventions; there were no game-memory
writes or injected native gameplay calls. Negative reachability claims remain open.

The four fake guard controls reproduced. The first invocation lacked the copied
expected-results fixture, so its comparison was incomplete; it was repaired and
rerun before further input. [The receipt](guard-test-run.json) also records that a
title input was issued between that failed comparison and repair. It used the
previously controlled guard; it is not represented as a passed current test.

Affected frontier: EXP031 now has a full follow-up liveness observation but retains
the timing qualification for independent review. FABLE-REQ-ASTRA-HANDLERS remains
open; next instrument is the existing EXP038 stack reader with EXP039 controls,
followed by actual target→queued command→executed action evidence. No database
contract/type/EC7 or full-completion claim is promoted.

## Prospective notes retained unchanged

# EXP-031 matched continuation — prospective, no result yet

Method C: actual loaded FF12 threads and responsiveness are required. The prior
recovered positive omitted a separate65s post window and matched input timings;
this fresh run cannot be spliced into that exited PID. Reuse exact EXP030 candidate,
known Stepping save,three65s observer windows. Aim Enter at20s and C at50s in each
(with5s tolerance,record actual offsets); middle window contains one-second
003A1C50 trace before Enter. Require nonzero real entries,stopped clear/readbacks,
detach,debugger absence and advancing repeated CPU plus visible menus,identity
checks and26-file restoration. No quantitative overhead or handler conclusion.
A new stop/takeover halts automation; failed controls retain incomplete status.
Observer only adds its already-recorded start timestamp to stdout to avoid the
previous timing omission. No new input method or laboratory platform.

Before armed capture: baseline actual input offsets {'enter': 36.408812284469604, 'c': 67.55748081207275}. Tool latency missed nominal20/50 targets. Remaining windows target the measured baseline offsets within5s; keep this prospective revision and actual receipts. No overhead estimate.
