# EXP-031 fresh loaded-state trace — bounded positive, original campaign incomplete

**Method C, 2026-09-13.** PID40504 loaded the known Stepping autosave. The unchanged
EXP-030 duration capture recorded **195 entries at 003A1C50** during its one-second
armed interval. Cleanup cleared and verified **101 thread contexts**, then detached.
Enter/C subsequently registered and visibly opened/closed the battle menu.
This does **not** complete the originally planned matched three-window campaign.

Player version: the short tracer ran while Vaan stood in the desert. The battle
menu still worked afterward. FF12 is closed, PC control is off, and the original
save/settings files are restored. No attack or enemy death was tested.

## Question and method

Competing outcomes: the exact duration capture can observe this loaded game and
cleanly return control, or attachment/deadline cleanup leaves a detectable debugger,
breakpoint, stalled process or broken input. Offline/native disposable controls
already exist; actual FF12 initialization, threads and responsiveness require C.
The pre-run board checkpoint selected one known positive site for one second,
raw API receipts, read-only CPU/debugger sampling, guarded controls and cleanup.
An empty hit set, failed API/identity/release control or interrupted run cannot pass.

This is an **intervention**: hardware debug registers, debugger events and the
cleanup break affect scheduling. Inputs use the existing dual-form sender held
about350ms. There are no game-memory writes or injected native gameplay calls.

## Reference and starting state

- Shipping EXE SHA256:
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- Base `00120000`; full mapped `.text` virtual extent **7,996,981 bytes**, SHA256
  `5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
- [Environment](environment.json), [process](process.json),
  [exact source origins](origins.json), [invocation](capture-invocation.json).
  All four capture-source hashes match the previous EXP-031 source pins.
- [Cloud OFF](cloud-setting.json) and [26-file backup census](save-before.json)
  precede launch. The backup was not used as the live working save directory.
- [Named save](named-save-ready-0.jpg), [Load complete](load-complete-0.jpg),
  [initialized field](baseline-field-before-0.jpg): Dalmasca Estersand/The Stepping,
  level1, Vaan103/103. `named-save-0.jpg` is an earlier transition, **not** save-list proof.

## Raw observations and controls

| Observation | Evidence and bound |
|---|---|
| No-attach baseline | [baseline-window.json](baseline-window.json):65s,6247 samples; debugger absent throughout |
| Capture window | [capture-window.json](capture-window.json):65s,6240 samples;105 debugger-present samples, then absent |
| Actual trace | [result.json](deadline-capture/result.json):195 nonzero entry observations, all RIP003A1C50; no errors |
| Clear/detach | [api.json](deadline-capture/api.json):2601 receipts; no failed recorded API return; stopped cleanup,101 clear/readback pairs, successful detach |
| Post-detach liveness | 2009 debugger-absent samples spanning20.9443s in the capture window; four successive5s CPU intervals advance by2.171875/2.28125/2.234375/2.234375 CPU seconds |
| Input registration | Seven pulse JSONs preserve zero baseline, nonzero held bytes, clear release, before/after code/module checks, null-read rejection and closed read handles |
| Visible responsiveness | [menu opens](capture-menu-open-0.jpg) after [Enter](capture-enter.json), then [closes](capture-menu-closed-0.jpg) after [C](capture-c.json); Vaan103/103 |
| Cleanup | [cleanup-before.json](cleanup-before.json), [cleanup.json](cleanup.json):normal exit, no FF12 process, PC-control kernel reset, all26 original and backup hashes match |

The current seven pulses independently reproduce Enter index49 and C index2.
OS delivery, internal registration and visible menu transitions are distinct facts.
No target selection, queued combat command, executed action or consequence follows.
The earlier brief-input failure's cause remains **unisolated**: duration and packet
form were not independently varied.

## Deviations and remaining qualification

The original design called for three65s windows and matched input timing. Actual
baseline Enter occurred28.8979s after its start; C occurred142.0557s after that start.
Capture Enter/C occurred289.6544s/304.2064s after the capture-window start, both well
after detach and after the observer ended. **No separate65s post window was recorded
before exit.** Those are operator execution omissions, not a game or instrument failure.

Therefore retain this positive and its20.9443s post-detach samples, but leave the
original campaign **INCOMPLETE**. The timing mismatch cannot support a quantitative
overhead comparison. Do not splice this run into the interrupted PID13964 baseline.
The remaining matched/post controls belong in a fresh run with its own baseline;
they can accompany the next justified handler-stack instrument qualification.

CPU advancement does not prove every game subsystem progresses. The observer's
reads are sequential samples, not atomic snapshots; debugger absence is bounded
by the sampling cadence. The recorded module census/watch policy does not prove
every module's unobserved state. This one state/site/duration does not qualify long
armed captures, the separate stack extension, arbitrary exceptions or handler zeros.

Affected claims: EXP-030 has this specific live positive; EXP-031's full matched
qualification remains open. `FABLE-REQ-ASTRA-HANDLERS`, EE-3/EE-4/EE-12 and all
combat/action consequence questions remain open. No contract/type/EC-7 result is promoted.

[review.py](review.py) checks the actual raw receipts and derives
[observation.json](observation.json). Its status is deliberately
`PARTIAL_POSITIVE_ORIGINAL_CAMPAIGN_INCOMPLETE`, never the CLI's campaign-wide PASS.
The unchanged cleanup helper restored only the inspected/preserved
`GameSetting.ini` LUIDLow79439→84456 delta. No new stop/takeover occurred; permission
remains active. Final database completion and its required audits are unfinished.

Publication control: the first checkpoint `58576896` normalized line endings in20
files. A direct committed-blob SHA256 check caught the mismatch before signoff;
the original local bytes were intact. This directory now disables text conversion,
and the repair commits those exact bytes. Use the repaired tree with this manifest;
the first commit alone cannot reproduce the recorded file hashes. No live result
changed and no live replay was needed.
