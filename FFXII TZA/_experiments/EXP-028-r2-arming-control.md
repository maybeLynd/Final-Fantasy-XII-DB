---
experiment: EXP-028
title: R2 arming counter and output timing after a short press
status: VALIDATED — short-press arming progression; atomic ordering and HUD driver unmeasured
date_designed: 2026-09-11
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - same subject as EXP-025 and the same reason: the R2 arming counter (022CBE18, threshold 022CBE08, time base 01DFE0B4) belongs to a documented path with no contract.
---

# EXP-028 — measure the intervening arming state

FABLE's215e880 corrects the omitted intermediate state in the R2 path: toggle1
drives acquire00366870, but the output writer receives engaged bit2 of022CBE1A.
The u16 counter022CBE18 advances toward u32 threshold022CBE08, initialized to
30 times u32 time-base01DFE0B4. EXP025 did not capture these fields. FM-1 asks for
the live check. This package complements the static work without rereading it.

In a fresh verified Stepping state, sample the EXP025 globals plus counter, threshold,
state word, sound handle022CBE1C and time base. Preserve raw values and frame brackets.
Use1second baseline, a short0.15second LeftControl press, then2seconds after release.
This is deliberately shorter than the predicted arming interval: if the toggle
persists, the counter should continue after physical release, engage at the threshold
and clear the output. It discriminates an activation delay from a continuous hold
requirement. A second equally short press may test disarming after the first result
is inspected. Do not infer the HUD driver's read site from a screenshot.

Controls: exact executable/module/full selected text identity, known raw-read constant,
read-only handles, initial named save, foreground each sample, sole held index89,
accepted one down/up, clean release and fresh stationary player HP/position. The
sampler is the EXP025 source extended with the five new fields and phase durations;
retain exact before-run source identities. No debugger, movement or memory write.

Predicted ordering is counter below threshold / engaged0 / flag1, then counter at
threshold / engaged1 / flag0 while toggle remains1 after release. Bracket any observed
crossing by adjacent samples and their game-frame counters. Reads are non-atomic,
including same-frame brackets, so sampling cannot prove instruction-level write
order or certify exact same-frame application. An unexplained mismatch reopens the
proposed explanation; it is not discarded as a torn read without evidence.

Close only the owned reference, restore all26 original save/config hashes, release
runtime and return results to FABLE under the existing request mechanism.

## Observed activation

Fresh PID35836 loaded the named Stepping save with stationary Vaan at HP103. The
first0.15-second press produced the following captured progression:

| Point | Sample time (s) | Frame bracket | Toggle / latch | Counter | State word | Output flag |
|---|---:|---|---|---:|---:|---:|
| Initial baseline | 0.000084 | 1379 / 1379 | 0 / 0 | 0 | 0x02 | 1 |
| First sampled activation | 1.02963 | 1441 / 1441 | 1 / 1 | 1 | 0x11 | 1 |
| Last held sample | 1.15472 | 1449 / 1449 | 1 / 1 | 9 | 0x11 | 1 |
| First released sample | 1.22662 | 1453 / 1453 | 1 / 0 | 13 | 0x11 | 1 |
| Last sample below threshold | 1.99399 | 1499 / 1499 | 1 / 0 | 59 | 0x11 | 1 |
| First sampled engagement | 2.00467 | 1500 / 1500 | 1 / 0 | 60 | 0x15 | 0 |

Threshold remained60 and time-base2 throughout both captures. The counter continued
after physical release, then stayed at60. Thus this state requires a toggle activation,
not a continuous one-second key hold. The0x11 to0x15 change sets engaged bit2; the
output flag is0 in the same captured tuple at the threshold. The screenshot after
release shows **FLEEING**. This is direct live support for the intermediate arming
state FABLE recovered, beyond EXP025's correlation between toggle and output alone.

The threshold/output transition is bracketed by adjacent samples in game frames1499
and1500, about10.68ms apart. Both sample brackets are within one frame-counter value,
but the individual field reads remain sequential. No writer trace establishes atomic
ordering, the precise input-consumption instant or the HUD driver's read site. This
does not independently certify exact same-frame output application in every state.

## Disarming and residual values

The second0.15-second press starts from toggle1, counter60, word0x15 and flag0.
It produces toggle0, word0x02 and flag1 while held; release clears the latch and
the screenshot no longer shows FLEEING. Counter stays60 and the stored sound handle
stays9, while the handle-held bit4 is cleared. The retained numeric handle does not
prove an active sound or valid resource: handle lifecycle/audio output was not traced.
Sticky stays0 instead of its initial1. This is not a full-state restoration.

There are302 samples per capture:96 baseline,15 held,191 released. These are two
input cycles in one loaded field, not604 distinct states. Each capture has two
cross-frame read brackets; all are retained. Frame ranges are1379–1573 and4344–4537.

## Controls and cleanup

Both pulses accepted one down/up packet and observed only held index89/code117;
baseline/released held arrays are clear and foreground is verified each sample.
Feature bytes remained1, override/audio gates and UI register remained0. Full
selected .text/module identity passed before/after and known read constants passed.
The four fresh field endpoints preserve the same player position and HP103.
No movement, encounter, debugger or process-memory write occurred.

PID35836 closed and all26 original save/config hashes were restored without extra
files. Only the known adapter LUIDLow config rewrite differed. Runtime is released.
Return FM-1's bounded arming result to FABLE; the HUD-driver and enemy-behavior
questions remain open, as do broader timing states beyond this60-fps field.
