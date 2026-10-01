# Shipping engine pump to callback queue

Method A / producer checked; independent acceptance pending. No live/native run.

Player version: the engine has a normal code path that gets the shared renderer
context and enters the cleanup queue, when a global gate is zero. Its internal
repeat loop skips that cleanup entry. This gives a precise code relationship;
it does not measure elapsed frames or prove a particular title widget's lifetime.

Question: is the queue consumer only a forced-call boundary, or does shipping code
supply a caller, and does the pump's repeat loop repeat the consumer? Original
caller/tail/getter bytes and CFG suffice for the static relationship. Exact EXE
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8;
reviewed access-role adapter5fcc64842c96d99c3ef9df4f7e3adc528dfad0dfd44b2f6bb5bf43beda092a38
actually used, Capstone5.0.7. Exact404B pump pdata and5B tail retained. The tail
has no pdata here; only its known direct entry/unconditional jump is claimed.

17D6E0 sets EBX0, compares DWORD01FD4A68, preserves flags through MOV/MOVAPS,
then nonzero skips the direct flush. Zero reads189120/global01F7F598, passes RAX
unchanged as RCX to185C20, whose exact5B jump enters186230. The ordinary ABI tail
adds no staging or object lookup. Later189CE0/189570 each read the global again.
Context stability/initialization is a premise, not an observed invariant.

The complete local normal CFG proves the direct flush site can execute at most
once per pump invocation: after17D71B no path returns to17D716. Repeat backedge
17D853->17D723 skips the first gate/getter/queue site. Nested reentry through
opaque callees is excluded from this local count. Four enabled consumer entries
from the prior queue proof are not necessarily four internal updates or frames.

Controls: one checked positive reducer; three actual CLI refusals for missing
getter, reversed gate and changed backedge. Each exits nonzero with no result.
The positive is reused. Both source-gate exits/identity stages and helper hashes
remain; missing evidence is not valid empty data. No native run count from CFG,
source predicates, algebraic cycles or external corroboration.

The CALL-only zero candidate in the previous packet remains preparation only.
The follow-up positive reference preparation included JMP and found the actual
17D716 CALL185C20 and185C20 JMP186230, with known CALL185ADC1858A0 and JMP controls.
This packet's semantic proof relies on original caller/tail source and CFG, not
an absence claim or a claimed complete incoming/indirect caller census.

OPEN: actual process gate/context state, thread/frame, pointer changes, natural
callback overlap, allocation interfaces and5DE250/19C590 effects. No title resource
ticket cancellation, full lifetime closure, natural execution observation or L3.
SPEC reviews this new static caller question; FABLE incorporates accepted renderer/
title scheduling and routes OPUS-owned contract changes once. Prior local queue
ABI/tracker/getter reviews remain separate.

Reproduce from repo root, fresh output:

    python <packet>/prove-title-queue-pump-boundary.py <fresh-result.json>

Optional second argument uses disposable source copies for refusal controls.
Published inputs/results stay immutable; manifest integrity is not acceptance.

Cleanup: own synchronous scripts exited. No PC/game/process/instrument/save/config/
reference writes; parked menu remains spent/unapproved; EXP127 invalid. Goal
ACTIVE/NOT_MET. One original caller/order question answered offline; whole runtime
rows newly closed0, cumulative previous source-retired request1.
