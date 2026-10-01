---
experiment: EXP-015
title: Does arming a breakpoint preserve the loaded reference state?
status: COMPLETE
contract: none — state-dependent instrument validation (RT-1)
tool: Database/Tools/analysis-kit/gfz-scripts/hwbp.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-10
date_run: 2026-09-10
---

# EXP-015 — loaded-state armed control

## Question and predictions

[EXP-010](EXP-010-loaded-state-no-arm.md) preserved input and repeated liveness
in loaded area 227 with no breakpoint armed. Does programming a single likely-cold
site preserve the same controls, and does a bounded positive entry/return capture?

H1: the armed zero-hit window loses responsiveness: investigate programming/event
handling before attributing failure to trap rate. H2: it survives but a two-hit
positive capture fails: actual trap/resume/detach becomes the next discriminator.
H3: both survive: proceed to bounded semantic observations with their own controls.
These are predictions, not exhaustive causal explanations.

## Original plan: state, method, controls and stop conditions

Use the shipped Steam executable with SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Back up and hash existing saves/config, load The Stepping autosave (00:08:42,
Vaan level 1), establish area 227 and record the loaded screen. The initial plan
(amended below before arming) compares a 35-second
baseline, 30-second single-site window at `003250F0`, and a separate positive
window at angle-normalizer entry `003A1C50` and ret instruction `003A1C8C`, stopping
after two total hits or ten seconds. Unexpected cold hits are also bounded at two.
Pair hits only in the same thread and retain incomplete pairs as such.

The original hwbp implementation remains unchanged. Arming and resume-flag changes
are instrumentation interventions; inputs are explicit interventions. Each window
has an external observer of live/disk code identity, full module list, CPU intervals,
foreground PID, debugger presence and held-key bytes. Enter/C open/close the command
menu at matched offsets. Screenshots must fall inside the interval they purport to
observe. Separate 35-second post-detach windows test sustained behavior.

Do not run the positive stage after an unhealthy cold stage. Preserve failures,
verify debugger absence, close only this reference PID, compare saves and restore
any experiment-caused configuration changes. Release runtime ownership after cleanup.

## Evidence and limitations

[Raw evidence](evidence/EXP-015-armed/) separates tool receipts from interpretation.
`target-code.txt` decodes the exact positive-control body and cold entry from the
hash-verified executable. `save-before.json` identifies the fresh ignored backup.
The failed sandbox input and successful elevated input are separate receipts.

No cold zero proves handler dead code: this is not yet FABLE's requested fight/kill.
The legacy trace has no timestamps, RSP or return-address stack. It cannot establish
call scheduling or satisfy the handler caller request. The observer's clean label
is the wrapper's narrow mod classifier, not a claim that overlay hooks are absent.
The instrument's detach return and cleanup register writes are unchecked internally;
external presence and post-window controls are required. CPU alone is insufficient.

## Protocol amendments and failed setup controls

Before any armed run, the initial baseline began while the screen still displayed
"Load complete", although the memory classifier already said IN-WORLD with area
227 and populated save bytes. Reject that window as a matched loaded-field baseline.
`loaded-state.jpg` records that intermediate screen; its filename is not proof.
`baseline-mid.jpg` subsequently shows the field. No breakpoint was armed then.

The next baseline had valid input-byte controls but its screenshot arrived after
the scheduled C input: the screenshot tool took 29.5 seconds. Preserve the missing
open-menu proof. Extend subsequent observation windows to **65 seconds**, the cold
attachment to **60 seconds**, and scheduled C to offset 50 seconds after the setup
delay; Enter remains at offset 5. Positive attachment stays capped at two hits or
ten seconds. `protocol-amendment.json` predates all armed runs. `baseline3` is the
matched baseline. Earlier wrapper versions are retained in `instrument-sources`.
`baseline3-after.jpg` was taken before C and still shows the menu; the later
`baseline3-closed.jpg` is the actual closure evidence. Use timestamps and content.

## Actual observation and result

Same reference PID **31676**, image base `0x120000`, area **227**, save head
`e70993b10100000096000000d3020000`. Every observer verifies the expected executable,
known read control and all 7,996,981 compared .text bytes against disk (SHA256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`). Full module
lists include Steam GameOverlayRenderer64, NVIDIA nvspcap64 and DiscordHook64.
This remains an overlay-loaded reference, not an overlay-free experiment.

| Window | Five-second CPU fractions of one core | Input/menu | Debugger observation |
|---|---|---|---|
| baseline3, 65 s | 0.518–0.613 | Enter/C held bytes 49/2; menu opened and closed | Absent throughout |
| cold, 65 s observer | 0.437–0.524 | Same held bytes and visible open/close | Present during attachment, absent at end |
| postcold, 65 s | 0.447–0.515 | Same held bytes and visible open/close | Absent throughout |
| positive, 65 s observer | First 0.614, then 0.266; remaining 0.037–0.134 | OS accepts Enter/C; no held byte, menu stays closed | Eight samples present, absent at end |
| postpositive, 65 s | 0.034–0.131 | OS accepts Enter/C again; no held byte, menu stays closed | Absent throughout |

All windows have zero foreground-PID mismatches and empty held arrays at the end.
The cold run reports **103 threads armed, zero hits, 60.1 seconds**. Its open-menu
screenshot timestamp is within 0.002 seconds of an external sample with debugger
presence true. This supports survival of the tested zero-hit armed window only.

The positive trace records exactly two rows: thread **7184** enters `003A1C50`
then reaches `003A1C8C`; XMM0 is **-3.13068414** in both. The instrument reports
101 threads armed and about 0.1 seconds attached. This is one observed local
entry/ret-site pair, not proof that the caller resumed normally. No stack was captured.

**Result:** the loaded state survived the zero-hit armed control but lost observed
game input after a bounded two-hit capture, persisting through a separate 65-second
post-detach window. A sustained high-volume breakpoint storm is not necessary for
this reproduced failure. This narrows the next investigation to actual trap handling
and its resume/cleanup/detach interaction; it does not identify which operation is
responsible or exclude environment/state interactions. Nonzero CPU is not recovery.
The legacy input probe's printed "real negative" is not promoted to a semantic claim.

## Cleanup, falsification and next discriminator

`process-cleanup.json` records closure of only PID 31676 and no remaining FFXII
process. No save file changed. Only the adapter LUIDLow in one GameSetting.ini
changed (79439 to 78642); its exact backup was restored. `restore.json` verifies
all **26** original save/config files match, with no additional files. Runtime
ownership was released immediately after verification.

The experiment falsifies general claims that a two-hit capture or low total hit
count guarantees responsiveness in this state. It does not satisfy FABLE's handler
fight/kill or caller-stack request, establish handler dead code, or validate native
substitution. The next bounded test should compare cleanup while the final debug
event still holds threads stopped against current continue-then-clear ordering,
with API return receipts and the same state/input/post-window controls. That is a
candidate mechanism, not an established cause; do not change production behavior
or promote a revised instrument before the comparison.
