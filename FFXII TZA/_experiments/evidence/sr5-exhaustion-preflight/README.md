# SR-5 exhausted-bank observation: distinguish empty from exhausted

Result **TRIGGER_COVERAGE_CORRECTION; NO_LIVE_OCCURRENCE_RESULT**. Consumer/reviewer:
FABLE audio contract; preparation FRONTIER. Source request
`FABLE-REQ-ASTRA-SR5-IS-A-NON-RESIDENT-BLOCK-EVER-REQUESTED` asks whether ordinary
play requests a block without a resident bank. That occurrence remains OPEN.

Method A qualifies its proposed observation address; it does not repeat the
bank-reader census or simulate playback. `reference.json` contains all138B of
shipping0021B5B0, exact EXE73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
preferred image base120000 and complete Capstone decode/version. Extraction
reads the unchanged repository reference copy, checks its complete SHA, and
requires the byte range to be PE-section backed. No process was launched or read.

Competing explanations: proposed0021B608 fires on every no-bank lookup; or it
fires only on a nonempty exhausted list while empty-list requests bypass it.
The original bytes establish the latter:

| original route after receipt minting | decisive edge |608 hit?|callback00224540?|
|---|---|---|---|
|head equals sentinel, empty|21B5F4 `je21B621`|no|no|
|nonempty, traversed to sentinel without match|21B606 falls through608 `jmp21B621`|yes|no|
|bank block matched|21B5FE `je21B60A`; callback at21B61A|no|call present|

These are **static decoded CFG witnesses**, not observed trace events or
isolated original execution. `check.py` follows declared branch predicates
through the original decoded instructions; external calls remain opaque.
The original receipt call at21B5E2 precedes head load21B5E7. Hence “empty” here
means empty **after that call**, not necessarily at function entry. RCX loads
the head from controller+8; RBX advances to that same controller+8 sentinel.

FABLE's local receipt-preservation reading holds: the two miss routes do not
rewrite RAX/EAX, and the match path restores EAX from ESI after its callback.
This does not execute the minting callback or certify audible output, native
initialization, successful playback or real caller/bank ordering. Background
audio cannot be declared silent merely because this lookup has no match.

The proposed608 breakpoint remains useful as a **positive nonempty-exhaustion
detector**. Its absence is not evidence excluding the empty-list miss. Shared
epilogue621 is reached by match, empty and nonempty miss; observing it alone
does not classify the route either. Neither a bounded non-hit nor inability to
prepare a state supports “never occurs/dead in play.”

Candidate future discriminator:21B5F1, immediately before the first comparison,
has loaded RCX=head and RBX=sentinel. With validated actual controller identity,
`RCX==RBX` distinguishes the empty-list route in an actual request. This is a
preparation candidate, **not a qualified or deployed breakpoint**, and the
nonempty no-match route still needs its own observer coverage. The signed block
quotient is EDI; caller stack/normal reachability must be independently retained.

Required C preparation: named save/area/normal sound-producing trigger and
canonical consumer; exact process/module/reference identity; actual controller,
list and request-key identity; positive matched request and separated miss/empty
observations; bounded event/time budget and observer qualification; start/end
responsiveness and fatal-dialog checks; detach/debug-register cleanup; save/
config integrity. The existing S19 input stop-loss is unchanged. No new live
setup, debugger, code/data write or general observer backend was used here.

`validation.json` records four rejecting controls: wrong EXE identity, corrected-
hash/redecoded mutation redirecting the empty branch to608, text/bytes mismatch,
and an acceptance rule equating one trigger's absence with all misses. Static
positives distinguish the match/callback, empty bypass and nonempty exhaustion.
PASS qualifies this preflight only; live semantic closure is empty. Raw code,
normalized routes, extractor/reducer, controls and limits are preserved.

Affected claim: narrow the request's detector/negative criterion; preserve the
valid conditional contract mechanism; leave ordinary-play occurrence open.
Owner review/consumer agreement is required. Peer canonical files were not
edited. No game/save/config/reference writes or cleanup actions were necessary.
