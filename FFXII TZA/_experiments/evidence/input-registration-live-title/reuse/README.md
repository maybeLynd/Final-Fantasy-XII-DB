# Recovered Enter/C delivery — live FF12, 2026-09-13

**Player version:** the existing held-key method works. Enter opened Load Game,
loaded the known Stepping save, dismissed Load complete and opened the battle
menu. C closed that menu. Vaan remained at 103/103 HP. FF12 exited normally,
all 26 original save/config hashes were restored, and PC control ended.

ASTRA's decision to wait on FABLE's title-keyboard analysis as a prerequisite
for all further live work was **too broad and is withdrawn**. The controls were
already documented, and EXP-031 preserved a successful delivery method. The
user explicitly directed ASTRA to recover that method and also reiterated that
memory/native-command interventions are available when justified. No such game
memory intervention was needed for this recovery.

## Question and method

Can EXP-031's existing dual-form keyboard sender, held for 350 ms, establish
registered input and visible acceptance in the current title and loaded state?
H1: expected key-state bytes and corresponding menu transitions are observed.
H2: they are not, leaving a narrower delivery/state boundary to investigate.

Method **C** is sufficient and necessary for this current-process qualification.
Reuse `runtime_input_probe.send_key` from the successful EXP-031 receipt, the
EXP-024 read-only Reader, EXP-037 full-code qualification and the existing
`input_sample.snapshot`. The small [pulse wrapper](pulse.py) adds a bounded
single-key run, exact raw samples, exclusive output, read-only process access,
Escape/focus/cursor stop checks and guaranteed key release on delivery/read
failure. It does not call the legacy probe's main routine or accept its broad
negative verdicts. No new input platform, mapping discovery or live-test quota.

The user specifically requested recovery of the historical input path. The
standard Computer Use interface handled window observation, launch and exit;
the existing experiment sender supplied the held game-key events. These are
**simulated OS-input interventions**. No FF12 memory writes, injected native
calls, hooks, breakpoints, suspension or debugger attachment occurred.

## Reference and starting state

The owned process was PID **22784**, window **462184**, at the designated
`D:\SteamLibrary\steamapps\common\FINAL FANTASY XII THE ZODIAC AGE\x64\FFXII_TZA.exe`.
Executable SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Base `0x120000`. Each pulse compared the complete mapped `.text` virtual extent
of **7,996,981 bytes** against disk before and after delivery, SHA-256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
File-alignment padding is outside that extent. Known-byte and rejected-null read
controls passed; complete module inventories and exact source hashes are retained
in each pulse receipt. Watched-module classification is not a proof that every
other module's bytes or transient process state were unmodified.

Steam's current properties showed Cloud OFF and empty advanced launch options
([screenshot](cloud-before-0.jpg)). [Setup](save-before.json) copied and verified
all 26 originals before launch. The original backup was never loaded directly.

`initial-0.jpg` is the boot autosave notice; it is not the title-state proof.
`title-before-enter-0.jpg` shows Load Game selected. The save list then shows
the selected **Dalmasca Estersand / The Stepping** autosave, level 1, 150 gil.
`stepping-load-selected-0.jpg` shows Load complete. `loaded-field-0.jpg` is the
immediate black transition; **`field-ready-0.jpg`** proves the visible loaded
field with Vaan at 103/103 HP. Do not label the transition image as initialized.

## Raw evidence and normalized observations

Each linked receipt retains no-input baseline, held and release samples, raw
256-byte state, pointer-chain brackets, timestamps, API return counts, exact
code/source identity and closed read-handle receipt. No sample counter alone
is a semantic verdict.

| Intended transition | Raw pulse | Observed held index | Visible result |
|---|---|---:|---|
| Title Load Game confirmation | [title-enter.json](title-enter.json) | 49 / code 77 | [Save list opened](title-after-enter-0.jpg) |
| Select named Stepping save | [load-stepping-enter.json](load-stepping-enter.json) | 49 / code 77 | [Load complete](stepping-load-selected-0.jpg) |
| Dismiss Load complete | [dismiss-load-enter.json](dismiss-load-enter.json) | 49 / code 77 | [Loaded field](field-ready-0.jpg) |
| Open battle menu | [field-menu-enter.json](field-menu-enter.json) | 49 / code 77 | [Attack/Magicks/Items menu](field-menu-open-0.jpg) |
| Cancel battle menu | [field-menu-c.json](field-menu-c.json) | 2 / code 30 | [Menu closed, HP 103/103](field-menu-closed-0.jpg) |

All five pulses had clean baselines, the expected sampled held index and a zero
release sample, with two accepted down forms and two accepted up forms. Actual
measured holds were approximately 353–355 ms. The run observed no stop, cursor
movement or focus-loss condition. [Guard controls](guard-controls.json) separately
exercise positive release, focus loss, Escape before delivery and partial delivery
with fakes; those controls are **offline**, not FF12 behavior evidence.

## Interpretation, limits and affected work

This restores a usable input route and establishes that the existing keyboard
array can expose Enter in this actual title state as well as in the loaded field.
The earlier all-zero `resumed` capture stays inconclusive; it is not erased or
retrospectively promoted. This run does not isolate hold duration from packet form,
tool focus behavior or other differences between the two methods.

The evidence stages established here are **input sent → expected held state
sampled → visible menu/load acceptance**. No battle command was committed, no
target selected and no combat action or consequence observed. A screenshot proves
the menu presentation; the memory samples prove the observed input state. Their
timing is sequential, not atomic and not a caller/write trace.

FABLE retains ownership of `ASTRA-REQ-FABLE-TITLE-KEYBOARD-POLL`; its static
writer/caller question remains useful but **is no longer a gate on ASTRA's live
work**. The recovered route enables the outstanding loaded armed-deadline control,
then the high-priority handler request with target → command → executed action
evidence. Memory/native-call interventions remain an alternative for questions
they can answer, with justified ABI/thread/state and explicit reachability limits.

## Cleanup

Alt-F4 opened the normal [Exit Dialog](exit-dialog-1.jpg); its confirmation was
sent separately. The immediate window list could still see the closing window;
an independent process enumeration then found no FF12 process. PC-control JS was
reset after that verification.

The sole changed file was `GameSetting.ini`: only `LUIDLow=79439` became
`LUIDLow=84456`. The changed file was preserved, the exact byte delta checked,
and [cleanup](cleanup.json) restored all 26 hashes and verified the original
backup unchanged. All pulse read handles closed. No real save progress changed.
Authorization remains ACTIVE; a new user stop/takeover still halts automation.
