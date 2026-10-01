# ASTRA: rear pan and source-channel spread in the original mixer

2026-09-21. **Method B: isolated original FF12 machine code.** No running FF12,
PC control, OS sound output, save/config change or reconstruction phase.
Source request: `FABLE-REQ-ASTRA-REAR-HALF-VOICE-PAN-LISTENING-TEST`.
Consumer: FABLE, UQ-242 and the audio boundary page; OPUS for exact mixer limits.

Player version: the script's pan byte does not by itself tell us where a stereo
voice will be heard. The mixer treats each source channel separately. With the
tested spread value zero, the two channels favor opposite outputs; at spread one,
both point in the mono direction. Actual cue content and later playback still matter.

## Question, competing explanations and method

FABLE's static interpretation predicts rear byte 240 gives roughly 111 degrees;
the alternative front/back-mirror interpretation predicts roughly 249 degrees.
The page also leaves the spread parameter's effect uncharacterized. Determine
the original matrix coefficients, first for mono and then for stereo source channels
at two outputs, while preserving the distinction from scene/device behavior.

H1: the shipping negative-frpan half-turn favors numeric output 1 for the supplied
mono rear-pan inputs. H2: a mirror would favor output 0. H3: the same pan/frpan targets
alone determine a whole stereo voice's output preference. Source-count and spread
controls distinguish H3; a deliberately changed half-turn instruction tests detection
of the opposite mono outcome. No live scene is required to settle this arithmetic.

The request's actual cue/parent-layer/device question still needs C. Reading just
the Sound interpolator targets cannot establish that later layers leave the values
unchanged or that the material uses the mono path. This package supplies a concrete
discriminator and does not close that live remainder.

## Reference, ABI and initialized fixture state

EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
preferred base `0x120000`, read from `Database/Tools/work/exe/FFXII_TZA.exe`.
Unicorn 2.1.0, Capstone 5.0.7; full Python/platform versions in raw JSON.
`tool-files.json` records related executable/package/DLL hashes after execution;
this is not a full loaded-module census or pre/post integrity measurement.
Exact original bytes, decoding and hashes are retained for:

| Function | Bytes | Role |
|---|---:|---|
| `007B8430` | 1,895 | one row of the source-by-output gain matrix |
| `007B8BA0` | 217 | original cosine approximation |
| `007B8C80` | 192 | original sine approximation |
| `00808C40` | 33 | original security-cookie check, including its failure branch |

**No stubs.** All mathematical helpers execute their original instructions; no host
sin/cos implementation supplies the result. A cookie failure exits the allowed
code region and invalidates the run. The normal original check executes in each
accepted row. The harness reuses the existing EXP115 PE/guest-memory pattern.

Inputs at entry: XMM0 pan, XMM1 frpan, XMM2 udpan, XMM3 center weight; stack arguments
at entry RSP+28 LFE, +30 source-channel count, +38 source-channel index, +40 output
count, +48 output pointer, +50 spread. These are fixture inputs, not captured game
state. The wrapper's exactly representable `(191-byte)/128, -1` rear pair is supplied
directly; the wrapper, Sound initialization, parent combiner and voice routine do
**not** run. Output count is 2; center and LFE are zero. MXCSR is set to `0x1F80`.

File-backed PE data supplies the speaker tables and constants. Uninitialized BSS
is not used as a runtime default. Every data read must be in original file-backed
bytes or the explicit synthetic stack/output. Read addresses and values are retained.
Output starts poisoned; adjacent canaries guard its eight-byte extent. Writes outside
stack/output, code outside the four named bodies, missing cookie/return, wrong stack
or nonvolatile restoration, or exhaustion of 12,000 instructions invalidate a row.
Raw output writes and full instruction address order are preserved.

## Feasibility and results

Before the full campaign, three original-code controls returned normally: mono center,
output-1 axis, output-0 axis. Center coefficients agree within `1e-6`; axes discriminate
greater than `.99` versus magnitude below `1e-6`. Exact tiny residuals are retained,
not rounded to mathematical zero. `pre-full.json` pins the unchanged harness and
feasibility receipt before the full campaign. `full.json` contains 23 normal rows
and two intervention/invalidation controls, not 25 valid semantic cases.

Representative measured rows (output 0, output 1):

| Controlled input | Output 0 | Output 1 |
|---|---:|---:|
| mono byte 215 | 0.471396714 | 0.881921172 |
| mono byte 240 | 0.183039829 | 0.983105421 |
| mono byte 250 | 0.061320677 | 0.998118043 |
| mono mirror input for 240 | 0.983105421 | 0.183039844 |
| stereo byte 240, spread 0, source 0 | 0.565731704 | 0.824589252 |
| stereo byte 240, spread 0, source 1 | 0.824589312 | 0.565731645 |
| stereo byte 240, spread 1, either source | 0.183039829 | 0.983105421 |

This supports H1 for the supplied mono inputs. It refutes H3: the stereo rows at spread
zero favor opposite outputs despite identical overall pan/frpan. Applying identical
signals to both measured rows gives approximately `1.390321` in each output. That is
a **linear calculation from coefficients**, not rendered or recorded audio. Real
source samples, phase, levels and downstream processing determine the audible result.
Numeric output 1 is not independently identified here as the physical right speaker.

Other boundaries: mono byte 127 favors output 1 while 128 favors output 0, retaining
the wrapper/mixer discontinuity; frpan zero gives exactly `(0.5,0.5)` in the tested
mono case. Changing udpan from zero to one leaves the controlled center row identical.
These observations do not establish arbitrary-input, NaN, exceptional FP or device parity.

## Previously uncharacterized spread operation

For a two-channel source and two outputs, original constants give pre-wrap offsets
`o=1.5` (source 0) and `o=0.5` (source 1), equivalent to `-0.5,+0.5` at spread zero.
The shared branch at `007B86BD..007B86E6` does:

```text
s <= 0: leave o unchanged
s > 0 and o > 1: o' = o + (o - 1) * s
s > 0 and o < 1: o' = o - o * s
o == 1: unchanged
then add o' to pan and apply the original wrapping/negative-frpan logic
```

Thus spread 1 collapses these two offsets to the same direction modulo the pan
coordinate's period of 2 (offsets `2` and `0`), rather than widening them. The full
native runs confirm intermediate `.5`, collapse at `1`, unchanged behavior at `-1`
versus `0`, and swapped source rows at `2`. Values -1 and 2 are **controlled boundary
inputs**, not proof that callers allow or use them. The ordinary initialized spread
value and its permissible caller range remain open. General source counts, six/eight
outputs, special material routing and parent layers are outside this package.

## Controls, falsification and artifacts

- `feasibility.json`: first three native-instruction positive controls.
- `pre-full.json`: source/feasibility hash receipt before full execution.
- `full.json`: raw instruction order, original read values, output writes, exact float
  bits, stack/nonvolatile/canary checks, identity and limits for every row.
- `normalized.json`: derived comparisons, including the explicitly calculated mix.
- `check.py`: read-only receipt reducer. It verifies exact original bodies/read bytes,
  expected cases, output bytes reconstructed from writes, execution completion,
  controls, and rejects malformed/empty evidence. It does not count an invalid run as pass.
- `run.py`: preserved execution harness. Original raw files refuse overwrite.

The instruction-budget-one control does not return and is rejected. The labelled
mutation replaces only the negative-frpan half-turn add at `007B8769` with NOPs in
disposable emulated memory; it returns but changes mono 240 to output-0 dominance,
so the original-side discriminator rejects it. This is a falsification control,
not original behavior or a live intervention. Raw original/mutant evidence remains
separate. Five malformed receipt inputs are rejected without editing retained data.

Run from the repo root:

```powershell
.\Collaboration\Tools\analysis\venv\Scripts\python.exe 'Database/FFXII TZA/_experiments/evidence/audio-pan-matrix-original-exec/check.py'
# Optional independent fresh original-code replay; does not overwrite raw evidence:
.\Collaboration\Tools\analysis\venv\Scripts\python.exe 'Database/FFXII TZA/_experiments/evidence/audio-pan-matrix-original-exec/check.py' --replay
```

## Consumers, live remainder and cleanup

Route to FABLE for UQ-242's measured mixer boundary and spread description, and to
SWE2-AUDIT-SPEC for independent original-byte/ABI/result review. Canonical acceptance
remains pending. Do not promote a Sound-target snapshot to the final matrix or sound.

Any later listening package must identify the authored cue and normal scene trigger,
source channel count, special routing flags, final parent-combined pan/frpan/spread,
actual output count/mapping, and positive left/right controls. Record actual target
updates and executed voice/matrix output, with presentation/audio separately. Choose
the least invasive read/capture that resolves the named remaining claim. A sampled
target or an injected mixer call alone does not show ordinary scene reachability.

The isolated process exited normally; emulator memory is disposable. No native FF12
process was opened, no debugger attached, no PC controls acquired, no saves/config/
reference bytes changed. No game cleanup/restoration or live-health claim is needed.
This result does not cure or qualify the failed EXP127 game trace.
