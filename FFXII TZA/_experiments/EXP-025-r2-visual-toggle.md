---
experiment: EXP-025
title: R2 modal toggle visible identity and state controls
status: VALIDATED — visible settled state; held-output timing unresolved
date_designed: 2026-09-10
method: C - ordinary UI input and read-only process observation
live_game: true
contract: none - the R2 modal toggle path has no contract. Its globals (020927E0, 020927E4, 01E0C2B4, 01E0C2B8) are documented on a page, not in a CONTRACT-*.md, so there is nothing to file this against and nothing to reciprocate.
---

# EXP-025 — what does the R2 toggle look like in the field?

The existing R2 modal-toggle page leaves visible behavior unknown under
PROPOSED-repos2d-7. Static code identifies profile-1 slot 9, keymap code 117
(LeftControl), with toggle 020927E0, latch 020927E4 and sticky override 01E0C2B4.
The output flag 01E0C2B8 has inverted polarity relative to the requested state and
is gated by feature-enable bytes 02B4053C/3D and other policy. Do not label the mode
from the working force-fight name or general knowledge of controller layouts.

In a fresh verified Stepping field, keep Vaan stationary near the initial safe
position. Preserve the named save and baseline screenshot. Sample the raw globals,
input held array, frame brackets and relevant gates for one second without input,
one second with LeftControl down, and one second after release. The expected input
index is 89 (117 minus 28); verify focus and accepted down/up events and release.
Use read-only process access; no debugger or process-memory intervention.

Hypothesis 1: an edge flips the toggle once, the latch follows the held key, the
output follows the documented gated polarity, and a recognizable visible mode
persists after release. Hypothesis 2: this state pins/refuses the mode, or its visible
behavior differs from the hypothesized input role. Capture the actual screen after
release before deciding. Perform the same bounded press/release once more to test
reversibility, then capture the screen again. Do not infer immunity, enemy aggression,
path safety or automatic battle cancellation from a stationary visual result.

Initial qualification must preserve full code/module identity, read constants and
field state. Sampling cannot prove instruction-level ordering and can miss intra-frame
transients. Frame brackets label non-atomic reads. Latch samples during a known held
key are a positive instrument control; a gated no-change result is not a missing key.
Close the owned reference and restore all save/config hashes before releasing runtime.
Return evidence to the semantic owner under the existing request mechanism.

## Result

Fresh PID 38024 loaded the named Stepping save, level-1 Vaan at HP103. No movement,
enemy encounter, attack or process-memory write was performed. The first ordinary
LeftControl press activated the visible **FLEEING** label, still present after key
release. A second press removed the label. The screenshots preserve the baseline,
first-release and second-release views. This identifies the mode in this field;
it does not establish enemy behavior, immunity, command cancellation or safe passage.

The stable phases match the documented output polarity:

| Phase | Toggle 020927E0 | Latch 020927E4 | Sticky 01E0C2B4 | Output 01E0C2B8 | Visible label after release |
|---|---:|---:|---:|---:|---|
| Initial baseline | 0 | 0 | 1 | 1 | absent |
| First release | 1 | 0 | 0 | 0 | FLEEING |
| Second release | 0 | 0 | 0 | 1 | absent |

Sticky is cleared by the press and does not return to its initial value. Therefore
only the visible mode/toggle/output returned to baseline; the full raw state did not.
Both feature-enable bytes remained 1, the captured override/audio gates remained 0,
and UI register 022C83EC remained 0 in these samples. Uncaptured policy/caller context
is not thereby proven constant or irrelevant.

## Held-output discrepancy retained

Each run has 96 baseline, 96 held and 96 released samples. These are two input cycles
in one loaded state, not 576 distinct game states. The first run's held tuples
(toggle,latch,sticky,output) are `(0,0,1,1)` once, `(1,1,0,1)` **94 times**, then
`(1,1,0,0)` once. The equal-one tuple spans sample times 1.0142714 to 1.9876546 seconds
and many field frames. The first released phase is `(1,0,0,0)` throughout.

The second run begins in `(1,0,0,0)`, retains it in the first held sample, then
records `(0,1,0,1)` for the other 95 held samples. Release is `(0,0,0,1)` throughout.
The first and second runs span frames 1452–1636 and 3011–3195 respectively; three
sample read brackets cross a frame in the first run, none in the second. Reads are
still non-atomic even when a frame bracket does not cross. However, the recurring
first-hold tuple must not be dismissed as a single torn read or an instant transient.

No writer trace establishes why the output lagged the first toggle. A delayed call,
uncaptured gate, or another writer remains possible. The screen was captured after
release, so its exact first appearance relative to the key edge is also unmeasured.
The initial board shorthand about a transitional mixture was superseded by this
frequency analysis and the explicit held-lag request before publication.

## Controls, cleanup and integration

Both runs accept one down and one up event, observe only held index89/code117,
have clean no-key baseline/release samples, and retain verified foreground on every
sample. Fresh field reads keep the player's position and HP103 unchanged. Initial
and final qualification compare all 7,996,981 selected .text bytes to the authority
executable, SHA-256 5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4.
Executable SHA-256 is 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base0x120000; known-constant and self-index controls pass. Full module lists preserve
the overlay context, with a clean watched-module verdict. No debugger was attached.

PID38024 was closed and all26 original save/config hashes restored with no extra
files. Only GameSetting.ini's adapter LUIDLow rewrite differed. Runtime is released.

ASTRA-REQ-FABLE-R2-VISUAL routes the bounded visible result for integration into the
R2 and force-fight pages and PROPOSED-repos2d-7. ASTRA-REQ-FABLE-R2-HELD-LAG separately
routes the unresolved held-output behavior. The latter prevents a claim of immediate
same-frame application but does not invalidate the observed settled FLEEING identity.
