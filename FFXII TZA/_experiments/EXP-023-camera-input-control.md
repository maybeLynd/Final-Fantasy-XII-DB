---
experiment: EXP-023
title: Distinguish camera arrow input from keypad navigation
status: VALIDATED — bounded horizontal-camera input control
date_designed: 2026-09-10
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - input-probe identity. Establishes that a SendInput packet reaches the game as keymap code 106 (Keyboard2 Right) and not as camera RX_P, which is a fact about the INSTRUMENT. No contract operation was exercised.
---

# EXP-023 — camera input identity before another group approach

EXP-019's camera-right-1.json records VK 0x27 moving held-array index 78, code 106,
with clean baseline, accepted events, no lost focus and clean release. The actual
saved keymap maps 106 to Keyboard2 Right (D-pad), while camera RX_P is 92. These
receipts do not show that a camera command was delivered. No-rotation is therefore
not evidence of camera failure or game unresponsiveness.

The shared probe sends two events: a virtual-key event and a scan-code event,
both using MapVirtualKeyW type 0 without KEYEVENTF_EXTENDEDKEY. Microsoft's
[KEYBDINPUT documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput)
requires the extended-key flag for an E0 scan, and
[MapVirtualKeyW](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mapvirtualkeyw)
type 4 is documented to preserve extended prefixes. The first packet control failed:
on this host type 4 still returned unprefixed arrow scans. That failed candidate and
result are preserved. The revised candidate explicitly
marks only the four dedicated arrows using Microsoft's
[scan-code table](https://learn.microsoft.com/en-us/windows/win32/inputdev/about-keyboard-input),
checks their expected low bytes, and emits one scan event with the prefix represented
by the flag, retaining key-up on release. Unsupported E1/unmapped keys
fail before delivery. This is a private experiment instrument, not a shared-tool
promotion or general keyboard implementation.

Hypotheses: the old packet encodes the keypad counterpart, so the candidate moves
index 64 (code 92) and visibly rotates the field camera; or corrected delivery still
fails to reach the expected byte/axis, requiring a different input/state diagnosis.
Packet controls inspect actual Windows mapping without sending input. The live
comparison must use a fresh clean reference and named loaded save, no debugger,
matched short holds, focused input, baseline/release controls and saved screenshots.
It must preserve process/code and instrument identity. Mere SendInput acceptance
cannot establish the expected byte, camera motion or liveness.

Keep the player stationary during this control. Do not infer enemy identity,
completion timing or combat success. Close only the owned reference and restore
all save/config hashes before releasing runtime. A successful camera control can
enable a later bounded route; it is not itself a successful route.

## Result and falsification

Fresh PID 15600 loaded the named Stepping save, Vaan level 1, HP 103/103. Three
matched one-second controls gave:

| Input | Held index / code | Visible result |
|---|---|---|
| Original Right, two events without E0 flag | 78 / 106 | Camera view unchanged |
| Candidate Right, one scan event with E0 flag | 64 / 92 | Camera rotated to show the Rabanastre exit behind Vaan |
| Candidate Left, one scan event with E0 flag | 63 / 91 | Camera returned toward its original view |

Each live control had a clean one-second no-key baseline, accepted down/up events,
zero polls with lost focus, and no held byte after release. Raw receipts preserve
the exact flags and counts. The screenshots field-before, field-after-original,
field-after-candidate and field-after-left record the visible outcomes. Camera
motion is directly visible; exact angle and exact reversal are not measured.

The old packet cannot be used as a test of the actual Right-arrow/camera binding.
The candidate is usable for the next bounded horizontal-camera approach. This
comparison changes both extended-key encoding and the number of injected forms;
it does not independently estimate either change's effect or establish which old
event the game consumed. Vertical arrows have packet controls only, not live camera
validation. Other keys and other layouts are outside this result.

Before/after read controls compare all 7,996,981 selected .text bytes exactly to the
authority executable, SHA-256 5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4.
Executable identity is 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base 0x120000; the known constant and active slot self-index checks pass. Full
module lists retain overlays; the watched-module classification is clean. Both
one-second snapshots retain player HP 103, group actor HP 134, member 1/dead 0/flags 0
and slot3 0. They are identity/state controls, not a kill or scheduling experiment.

The shared probe still opens a write-capable handle and has limited negative-verdict
logic. No process-memory writes or debugger were used here; only the explicit positive
held-byte, focus/release and visual results are promoted. This private candidate does
not certify the shared probe's general negative conclusions or error-path cleanup.

## Failed setup and cleanup

The sandbox launch's PID 32764 exited before readiness. No camera test occurred.
The Computer Use launch produced PID 15600. A sandbox input attempt failed opening
the probe's write-capable handle, and a sandbox identity attempt could not enumerate
modules. All failures are retained. Running the already-authorized probes outside
the sandbox supplied the missing access; no disabled-control results were accepted.

The first MapVirtualKey-only packet candidate failed its arrow-prefix control and
was retained before the explicit dedicated-arrow correction. Ten packet cases then
passed with delivery intercepted: no OS input was sent by those controls.

PID 15600 was closed. All 26 original save/config hashes were restored with no extra
files; only GameSetting.ini's adapter LUIDLow rewrite differed. Runtime is released.
The group-completion request still lacks a reached and defeated final group member.
