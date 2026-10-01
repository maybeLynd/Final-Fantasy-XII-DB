---
experiment: EXP-082
title: Same-session save reload feasibility
status: INCOMPLETE - modern baseline observed; older load not reached
evidence_class: live setup observation
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - and the record already says so in its own words. Its `contract_coverage` line reads "Does not close same-session older-save import, native load chronology, or combat contracts"; status INCOMPLETE, the older save was never loaded. This field now states machine-readably what that sentence states in prose.
execution_scope: Modern autosave loaded and sampled; one pause input had no visible menu response; no older save loaded.
contract_coverage: Does not close same-session older-save import, native load chronology, or combat contracts.
date_designed: 2026-09-13
date_run: 2026-09-13
---

# EXP-082 - same-session reload was not reached

**The intended question remains open.** EXP080 loaded the older save from a fresh
boot; EXP081 loaded the modern save in another process. Neither establishes what
loading the older save does over a modern save's initialized session state. This
attempt established its modern baseline but did not reach the older load. Its
successful memory checks are not a successful reload experiment.

Player version: the modern Stepping save loaded with Vaan at103HP. The pause key
had no visible menu response, so the older Southgate save was never selected.
No conclusion about older-save compatibility follows from this attempt.

## Question, method and boundary

Distinguish whether older manual004 imports its party block or retains the
previous modern block in **one running process**. Method C is required for the
actual resource/initialization and ordinary load path. Reuse the existing observer
and ordinary menu route; no emulator, debugger, memory write or injected call.
Stop if the bounded pause-menu feasibility fails; do not repeat stationary combat
waits or a sweep of keyboard inputs. No user stop/takeover occurred in this run.

## Exact starting state and evidence

- Reference PID50736, window21894358, executable base120000. Exact executable
  SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
  [Process](evidence/spawn-live-reload/process.json) and
  [environment](evidence/spawn-live-reload/environment.json) retain the full path.
- [CloudOFF/empty launch options](evidence/spawn-live-reload/steam-before.jpg)
  verified before launch; [all26 originals backed up](evidence/spawn-live-reload/save-before.json).
  The backed-up originals remain protected; the live folder is the disposable
  working copy, with no save command or area transition issued.
- [Selected modern autosave](evidence/spawn-live-reload/modern-selected.jpg):
  The Stepping000:08:42, level01,gil150. FFXII_0005331B,
  SHA859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825;
  SAFH declared56690/rotation12. These are file/header and menu observations,
  not a new decoding run.
- The [observer](evidence/spawn-live-reload/observe.py) is EXP081's reader with
  only task/label changes; exact SHA8a40086c22cb7eb446749386d07033642796c8a0c558983f1429d1bd4def4b61.
  Every state retains full module inventory, full7996981-byte live/disk text
  equality, known LUAC bytes19930d0a1a0a, null-read rejection, complete-span checks,
  pointer/identity brackets and closed read handles. Source copies are preserved.

## Observations and limits

[Load-complete memory](evidence/spawn-live-reload/current-complete-memory.json)
and [field memory](evidence/spawn-live-reload/current-field-memory.json) each
contain two samples. All88 full-span reads normalize successfully in the
[setup-only result](evidence/spawn-live-reload/observation.json). At load complete,
both keep banks are zero and no occupied+actor+stats-bound unit occurs in the
sampled32 slots. In the field, party slot0 binds its stats to B+8; three kind1
slots4/5/7 bind stats to their SpawnKeep+80 with separate enemy/class rows. This
agrees with EXP081 and is retained as setup evidence, not a new architectural
closure. Primary keep328 nonzero bytes, secondary0; history00E3/0131 and raw
clock557/572 in the field. Reads are sequential, not atomic or a lifetime trace.

[UI method receipt](evidence/spawn-live-reload/ui-method.json) preserves the
sequence. A brief title click did not visibly open the list; a2px mouse drag did.
The same bounded gesture loaded the autosave and dismissed Load complete. One
ordinary Escape key call then produced no visible pause menu in its immediate
and later [field screenshot](evidence/spawn-live-reload/after-pause-no-menu.jpg).
The saved keymap binds Start=64 (Escape); **input registration was not sampled**.
This is not proof that the key never reached FF12, nor that duration caused the
failure. No return-to-title or old-save load was attempted after that boundary.

Input sent -> registration -> acceptance -> execution -> consequence remain
separate. A successful control-tool call does not complete those stages. The
mouse success does not validate keyboard registration; screenshots do not identify
internal writers. No whole-module/data integrity, native callback order, save
retention, inventory/gambit presentation, combat or handler reachability is claimed.

## Cleanup and continuation

AltF4 opened the [exit dialog](evidence/spawn-live-reload/exit-dialog-1.jpg), with
PAUSE visible behind it. Do not attribute that later pause to the earlier Escape.
Return confirmed exit; [process absence](evidence/spawn-live-reload/process-after.json)
was verified separately. No instrument was attached; read handles closed after
each observation. Computer-use JS was reset immediately after exit.
[Cleanup](evidence/spawn-live-reload/cleanup.json) records the soleLUIDLow change,
preservation of the working config, restoration of all26 originals and unchanged
backup. Runtime released6466; ordinary live authorization remains ACTIVE.

FABLE-REQ-ASTRA-OLD-SAVE-LOAD stays open. Before another attempt, observe game
input registration and its current binding through a controlled supported input
method; do not replay this menu failure or promote successful setup to a reload
result. This package does not advance final audit eligibility or complete L1/L2.
