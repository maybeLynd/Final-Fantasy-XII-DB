# Initialized Phyre globals — bounded live request

Requests: OPUS-REQ-ASTRA-PHYRE-DEFAULT-INSTANCE-BYTES and
OPUS-REQ-ASTRA-PHYRE-HIERARCHY-AT-RUNTIME. Method C: observe actual registered
descriptors/default buffers after ordinary startup. Static construction recipes
cannot establish which lazy preparation has occurred in this process. Existing
EXP079 already answers the separately queued arena-base sample; do not repeat it.

Competing hypotheses: the default buffer remains loader-zero/unprepared, has
prepared nonzero bytes, or carries poison/other state. Read descriptor name, size,
parent, default pointer and flags with each complete buffer. Bit31 and actual
pointer/size/name identity distinguish preparation states; bit31 alone does not
guarantee a usable default. No zero sample proves all newly allocated objects are zero.
For hierarchy, compare observed +78 links against the current static parent table;
a link is not by itself a subobject offset or proof of arbitrary containment.

Three requested classes form the first feasibility probe: PAnimatableComponent,
PAnimationChannel and PDeferredLightingBase. Full capture is bounded to the 177
sized classes (173 requested default buffers, 34,392 bytes total) and at most 32
ancestors per selected descriptor, with a 512-node overall limit. Abort on failed
read/identity controls; record disagreements rather than inventing a match. Use
the existing runtime_probe/ffxii_runtime read path, query/read handles only, no
debugger, writes, native calls, hooks or suspension.

Controls: exact reference EXE and full mapped .text before/after; nonzero LUAC
constant; unreadable address zero must fail; descriptor name/size/default pointer
matched to pinned target rows; flag/header brackets detect visible changes. Two
snapshots are sequential, not atomic, and cannot exclude intervening writes.
Record visible title state, module lists/tool hashes and clean close/save census.
Do not promote unprepared buffers into initialized defaults. If title data is
insufficient, retain that result and choose a justified ordinary trigger later.

Runtime bound: one ordinary startup and up to two short captures; no save load is
needed for this first state. Protect all saves/config, verify cloud off, stop on
takeover or changed target. No automatic restart after a stop. Audit raw evidence
before OPUS integrates type values. Full L1/L2 completion remains open.


## Result and revised scope

The173-buffer census succeeded:166 preparation flags set,7 unprepared-zero
buffers,140 nonzero buffers including7 all-A5,26 prepared-zero buffers.70 explicit
parent addresses match;103 blank/root entries point to the zero-size PBase.
The177-target attempt failed its first supplied D3D descriptor mapping. See
[scope revision](scope-revision.json); the4 non-default rows remain unresolved.

[EXP124](../../EXP-124-phyre-startup-globals.md) carries interpretation/limits and
[review.json](review.json) the raw-data reconciliation. [cleanup.json](cleanup.json)
verifies process exit, read-handle closure, PC-control reset and all26 save/config
and backup hashes restored. User authorization remains active. No experiment is
running. Independent audit and OPUS consumer integration remain pending.
