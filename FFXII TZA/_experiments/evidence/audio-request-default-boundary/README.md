# ASTRA — voice request defaults and live boundary, 2026-09-21

**The `voiceplay` default request is pan `0x40`, volume `0x7F`.** The voice-pack
page's modding note reverses those values. This is established from original
argument flow and the pending cue's producer/consumer, without running FF12.

## Question, hypotheses and selected method

Source request `OPUS-REQ-ASTRA-AUDIO-GATE-LIVE` combines selective gate behavior
and actual voice parameters. Existing EXP-096 already executes the sound-effect
request path through resolver/masking, with the dispatcher explicitly stubbed.
That is not a native voice or audibility result, and was not replayed.

During boundary preparation, the voice-pack page said volume64/pan127, while
the sound-request page identifies pan64/volume127. These could be different
interfaces or a swapped description. **Method A is sufficient**: follow the
actual `voiceplay` integer stack and cue fields, not an analogy with the other
interface. The competing value assignments reach different stored bytes.

## Identity, raw evidence and observation

Reference EXE SHA-256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
`observation.json` retains complete original bytes and decoded instructions for
twelve bounded bodies, their hashes and normalized flow. `check.py` verifies
these against the reference and checks the differentiating moves, stores and
reader argument positions. `validation.txt` and `manifest.json` seal the result.
The integer-pop body matches EXP-096's already-retained body identity.

| Boundary | Original observation |
|---|---|
| `003515B0` | Pushes64 at `003515D8`, then127 at `003515E5`, then tails to `00351020`. |
| VM push/pop | `00267F90` pushes a typed integer and increments depth; `00267E10` decrements depth and returns that integer slot. |
| `00351020` | Pops127,64,cue into ESI,EDI,EBX; pushes−1,cue,64,127,1; tails to `003581B0`. |
| `003581B0` | Pops flag1,volume127,pan64,cue,speaker−1. If not muted, sends R8D=64 and R9D=127 through `003E9BF0` into `003E9C10`. |
| Cue write | R9D is clamped and stored in bits24–30 of cue+08 (`003E9D06`); R8B is stored at cue+0F (`003E9D09`). |
| Request pump | `003E981F` reads volume byte+0B into R8D; `003E9825` reads pan byte+0F into EDX; calls `002DF680` after masking volume. |
| Stream boundary | `002DF680 ->001DC280` preserves pan/volume positions into the controller call `00211230`. No controller execution is claimed. |

The independent parameter adapters agree with the interpretation: `002256F0`
uses `(pan−64)/128` on the <=127 branch and stores the supplied pan at voice+20;
`002257E0` clamps volume0..127, stores it at voice+1C and scales by127. Their
original instructions and relevant literal values are checked. These adapter
bodies identify the parameters; this package does not demonstrate their execution
for a live cue or prove that the full downstream call graph is reached.

## What this corrects, and what stays open

FABLE consumer: `18-Audio/the-voice-pack-slots-and-the-voice-verbs.md`, section3
line saying “volume `0x40`, pan `0x7F`”. Correct to **pan `0x40`, volume `0x7F`**,
and carry explicit argument order into any typed/contract consumers. The page's
section2.3 parameter signature and cue field roles already match the code.
Do not globally swap field names or change independent custom-argument forms.

This is a request-value result. It does not show actual voice initialization,
playback scheduling, audible loudness, speaker balance or normal reachability.
Adequate VM stack capacity and a well-formed typed cue argument are preconditions.
The script mute predicate, loaded slot state3, selected language table and cue
bounds gate the write; handle completion, pending state and runtime mode gate the
pump's start call. Calls must return and preserve their Win64 nonvolatile state.
No default write or sound is promised in invalid or uninitialized states.

The outstanding C request must separate these two questions:

1. **Selective request gate:** an exact ordinary trigger for a gated wrapper and
   a matched positive-control path that bypasses that gate, with valid resolver
   bank/generation, second gate and world-live state. Observe actual requests and
   downstream acceptance, then any claimed audio output. A silent trace/sample
   without a successfully detected matched sound cannot establish muting.
2. **Actual voice parameters/output:** one identified native voice belonging to
   an exact ordinary cue, observed after request acceptance/execution; preserve
   authored bank/cue metadata, settings and gain/pan transformations. The constants
   or pending queue bytes alone are insufficient. A screenshot cannot prove sound.

FRONTIER must supply the exact current-format disposable save, ordinary trigger,
resource binding and canonical consumer before launch. Use existing validated
instruments; start with a bounded feasibility/control observation. Trace controls
must include normal responsiveness and fatal-dialog inspection; EXP-127 remains
invalid and its unchanged setup must not be reused. An injected call or gate write
would be an explicitly labelled intervention, not proof of ordinary reachability.
Stop on failed controls/health or user takeover; preserve raw evidence, restore
backed-up state and verify detach. No blanket live session is prepared by this
static package.

## Validation and cleanup

```text
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/audio-request-default-boundary/check.py"
```

No machine instructions were executed, no live game or PC control was started,
and no save/configuration was modified. Historical experiments remain intact.
Owner acceptance and canonical propagation are pending; database completion is
not asserted.
