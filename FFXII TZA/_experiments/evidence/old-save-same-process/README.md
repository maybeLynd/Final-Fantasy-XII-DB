# ASTRA: older-save import after a modern load in one process

Status: **INCOMPLETE — valid setup evidence; older load not reached.**
Task `FABLE-REQ-ASTRA-OLD-SAVE-LOAD`.
Major systems: save/load normalization and initialized battle state. Consumers:
FABLE's save-image page V-12 and spawn/load L-13; OPUS's corresponding types and
contracts. This is L1/L2 evidence, not implementation parity.

Player version: the modern save loaded and the documented keyboard method opened
the main menu. Config has no return-to-title option, and cancelling the OS Exit
dialog resumed Config. The older save was not loaded. FF12 exited normally, all26
original save/config hashes were restored, and PC control ended.

The prelaunch design below is retained as a plan, not as work completed. The
actual observations, failed route and next discriminating change follow it.

## Question and hypotheses

EXP-080 already disproved the original prediction of no compatibility import on
a fresh-title legacy load. EXP-081 supplies a modern-load positive; EXP-082 never
reached its older load. Do not repeat these as new architectural evidence.

The remaining question is what happens across the **same process's** modern
field -> returned title -> old load-complete -> old field transition:

- H1: the old compatibility records replace the modern battle prefix and bank0.
- H2: some prior modern battle state survives and is used instead of that import.
- H3: returning to title resets the relevant state before the older load. This
  prevents attributing a field-to-old difference solely to the older loader.
- Temporary keep banks may be cleared, retained, or repopulated between sampled
  phases. Endpoint equality does not establish uninterrupted lifetime or writers.

Method **C**, read-only memory and ordinary menus, is required for the actual
initialized load path. Existing source and isolated code cannot establish this
same-process composition. No breakpoints, hooks, writes, suspension or native
calls. EXP-127's failed trace is not involved.

## Identity, inputs and preparation

Shipping executable SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Base `120000`; full mapped text `7996981` bytes, SHA256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
The designated reference is the Steam installation, not any mod client.

Fresh read-only census before preparation found 26 save/config files. Both inputs
still match the retained experiments:

- modern account `76561198045890736/FFXII_000`, 5331 bytes,
  `859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`;
  decoded extent `56690`, The Stepping `000:08:42`, level1 / 150 gil.
- old account `76561197960267366/FFXII_004`, 7066 bytes,
  `8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc`;
  decoded extent `4E690`, Southgate `006:53:57`, six level21 portraits / 9999999 gil
  in retained save-list metadata. Modification history of that test save is unknown.

Before launch, observe current Steam Cloud OFF and empty launch options, perform
a fresh full hash-verified backup, check environment identity and confirm no game
already runs. The preserved backup is never played; the live folder is the
disposable copy and is restored before any future sync. Never issue Save or cross
an area boundary. Loading may still change files; cleanup checks the whole census.

## Prepared observation and control route

Reuse EXP-082's observer with only an explicit runtime-claim guard. Its absolute
active-image base is `02164280`, and the bound B block is read through `02EBF190`.
Keep banks are read through `0208E690/698`. Every recorded span carries address,
extent, bytes and hash. No offsets from `002EF2B0` are substituted: CON-129's
200h difference from `002EF640` is material to any coordinate comparison.

Capture two samples, 250ms apart, at each of four phases: current-field,
returned-title, old-after-current-complete, old-after-current-field. Optional
current-complete adds two samples only if needed to distinguish initialization.
At most ten samples total. Retain screenshots showing named selections, loaded
locations and load completion separately from memory. Maximum 20 minutes from
launch; stop sooner on a failed control or missing route.

Input reuses the qualified 350ms dual-form sender from
`input-registration-live-title/reuse/pulse.py`. Enter, C and Space are existing
live positives. R/I/K are the documented current bindings, with expected keyboard
array indices17/8/10; their registration and menu acceptance must be observed
before relying on them. The actual save-folder keymap matches the recorded hash
`8d98f85e0b571d819dc155c8774aad553f6e6119d6ede1cdd62245cfb9f6cf6d`.

Small feasibility control: after the modern field baseline, one registered R
pulse opens the documented menu. Follow only visible Config/return-to-title
choices with a fresh observation after each action. If that route is unavailable,
preserve the result and stop; no blind key sweep or repeat of EXP-082's brief
Escape attempt. Escape remains the sender's emergency stop. Standard window
controls provide ordinary exit. No automated Escape hold masks that stop.

The pulse preserves baseline/held/released raw input states, foreground/cursor
guards, full code/module checks and guaranteed key release on delivery failure.
Its API return proves delivery only; raw state proves sampled registration;
screenshots separately prove menu acceptance. No combat execution is claimed.

## Acceptance, failure and limits

Require the same exact PID/process identity through all four phases, unchanged
code, full module inventories, known nonzero read control, rejected null read,
complete nonempty samples, pointer/identity brackets and closed read handles.
Compare B's stamp and first six levels; full pre-gambit prefix; all40 bank0 records
against their compatibility records; selected banks; both keep banks; actor/stats
bindings; field/history/tick. Report changes from current field to title separately
from changes from title to older load. A previous nonzero keep bank is required
before interpreting a later all-zero bank as a cleared/changed observation.

Acceptance of H1 requires observable old import that differs from the preceding
sample, not just a success popup. A zero-versus-zero selector or bank comparison
cannot establish a reset. A different useful observation may be retained while
the intended claim stays open. Sequential reads are not atomic and cannot prove
call order, every intermediate writer, native object lifetime or universal behavior.
Screenshots do not prove internal semantics; memory does not prove presentation.

Check ordinary menu responsiveness and absence of fatal dialogs before and after
the capture. Failed game/session health invalidates semantic closure despite valid
read receipts. On failed controls, missing trigger, identity drift or takeover,
stop and retain the failure; do not retry unchanged or extend the budget. A new
user stop suspends automation until renewed authorization.

## Cleanup and evidence package

Exit the owned FF12 instance normally, confirm process absence and end PC control.
No debugger attachment is planned; verify every read handle closed. Preserve any
changed working file, review its exact delta and restore the fresh originals.
Require the complete pre/post save/config census and unchanged backup, plus
reference executable identity. The inherited cleanup intentionally refuses
unexpected file changes rather than overwriting them blindly.

Return raw captures/screenshots, source hashes and adaptation provenance, a
nonempty reducer/checker with failure controls, normalized comparisons,
interpretation, limits, health and restoration receipts. Route accepted evidence
to the named consumers; leave canonical closure pending their incorporation.
No experiment or database completion is claimed by this preparation document.

## Bounded route amendment before additional input

The registered R pulse opened the main menu; Config contains no return-to-title
option, so the proposed Config route is rejected. A350ms I hold registered index8
and repeated navigation, selecting Inventory after wrapping; do not call it one
menu step. Wheel+240 selected Config. No setting was changed.

EXP-082 already retained PAUSE behind its ordinary OS Exit dialog. One explicit
feasibility amendment: issue normal Alt-F4, inspect the Exit dialog, cancel once,
and inspect whether PAUSE remains with a normal return-to-title action. H-route1:
close-request cancellation leaves that action available; H-route2: it resumes the
prior menu/field. No Escape injection or emergency-stop suppression. If H-route2,
end the attempt normally and retain the narrower route gap. This uses the existing
window interface and keeps the original20minute/sample budget and cleanup rules.

## Actual observations and interpretation

Owned PID52384 / window102564144. [Process](process.json), [environment](environment.json),
[fresh backup](save-before.json) and [Cloud observation](cloud-before-0.jpg) identify
this run. [Seven input receipts](observation.json) retain35 zero baseline samples
each, positive held detection at the expected array index, and zero release;
every down/up accepted two forms and every read handle closed. Full mapped code
matched before/after each pulse. [check.py](check.py) reduces raw bytes rather
than accepting the recorded `nonzero_indices` labels. Empty and no-detection
variants are rejected. These are input/control checks, not save-load completion.

- Enter opened Load Game, loaded the selected Stepping autosave and dismissed
  Load complete. [Field proof](current-field-before-0.jpg) shows Vaan103/103HP.
- [R registered index17](open-main-menu-r.json) and opened the
  [main menu](main-menu-r-response-0.jpg), showing level1 Vaan and150gil.
- A small mouse drag at the Config label confirmed the currently selected Status
  action instead of selecting Config by pointer location. Its settled screen
  asked for a character. C registered index2 and returned to the main selection.
- I registered index8, but the350ms hold repeated through multiple menu positions;
  Inventory was selected afterward. A wheel+240 then selected Config. Do not
  describe a held pulse as one logical navigation step.
- Enter opened [Config](config-open-0.jpg). A wheel-120 wrapped to the bottom;
  [the settled bottom](config-bottom-settled-0.jpg) has Max.Gil as its last item.
  No setting or parameter action was confirmed. In particular, no gil was granted.
- Alt-F4 produced the normal Exit dialog with PAUSE behind it. The tool's child
  element9 lookup failed without activating Cancel. After refreshing, Tab visibly
  focused Cancel; Return dismissed it. [The settled result](exit-route-cancel-settled-0.jpg)
  is Config without PAUSE. This rejects the proposed shortcut **from Config**;
  it does not establish what cancellation from a field would do.

The [memory baseline](current-field-memory.json) contains two complete samples,
52 spans total. Both have B=`021B290C` and stamp`05071901`, first-six levels
`1,1,1,1,2,1`, and keep-bank nonzero counts`328,0`. The bound block equals the
corresponding bytes in the active image. This is a usable nonzero baseline, but
no returned-title or older-load sample exists. **H1/H2/H3 for save import remain
unresolved by this run.** It adds no native writer, lifetime or conversion claim.

The settings screenshot also shows **Screen Shake OFF**. This is a presentation
setting observed in this session, not proof of its internal effect or a global
user preference. A future camera experiment must record that setting before
interpreting the absence of visible shaking; native driver/RNG state is separate.

## Health, restoration and next exact action

Menu opening/cancellation and the normal Exit dialog were responsive, with no
fatal runtime dialog observed. The final Alt-F4/Return exited PID52384; the
immediate window list still contained a closing window, whereas the subsequent
[process enumeration](process-after.json) found no FF12. All eight read sessions
closed their handles. No debugger/hook was attached. PC-control JS was reset
immediately after process absence was confirmed.

[Cleanup](cleanup.json) preserved the sole changed working file and restored
all26 original hashes; only `GameSetting.ini`'s LUIDLow changed79439->78748.
The fresh backup was unchanged. [Reference recheck](reference-after.json) matched
the exact executable. No stop/takeover was detected and authorization remains
ACTIVE, while `@runtime` was released after cleanup. No unchanged live retry.

Next preparation is **one reversible control-binding intervention**, not another
Config search: add unused code43 (`P`) as the disposable file's Keyboard2 Start
binding, leaving Keyboard1 Escape and the sender's Escape emergency stop intact.
Verify against the existing original registry/scancode and reserved/duplicate
checks; retain original/edited file bytes and hashes. Extend the bounded sender
for P/index15 without changing its hold/release/stop logic. A fresh backed-up run
must visibly accept P as Pause before using any displayed return-to-title action.
File parsing or a registered P byte alone does not prove Start acceptance. If
the Pause route has no normal title return, retain that exact limitation and stop.
Label the input binding intervention; it is not a default-controls observation.
The fresh live run has **not** been performed here. The candidate preparation was then completed offline as recorded below.

FABLE/OPUS may use the recovered menu controls, but the same-process save request
stays open. No source-derived save conversion is withdrawn by an unreached load.
Database L1/L2 completion and required final reviews remain outstanding.

## Candidate preparation completed offline after cleanup

[next-start-binding/preflight.json](next-start-binding/preflight.json) retains the
verified original Key_P node/name, scancode19h, ASCII mapping43 and all35 reserved
codes. [prepare.py](next-start-binding/prepare.py) reproduces the bounded check
against the exact shipping image and protected original keymap. The84-slot
candidate has no duplicate nonzero or reserved values; its primary range is valid.
Only Keyboard2 Start changes0->43. Both original and candidate bytes are retained.
This checks source/file preconditions, **not native parsing or Pause acceptance**.
The initial in-memory candidate attempt assumed CRLF and rejected the LF file
before writing any candidate; the corrected recipe pins the exact LF source hash.
No real keymap was modified and no second game session was launched.

Next: claim a separate bounded capture directory, adapt the existing scripts for
that directory/fresh backup and P/index15 only, then reserve runtime. Verify fresh
Cloud/source state, backup, deploy the one labelled disposable binding and prove
P -> registered -> Pause accepted before proceeding through an observed title
return. Restore the keymap as well as any other reviewed session changes afterward.
