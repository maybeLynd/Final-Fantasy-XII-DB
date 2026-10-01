# OPDIV zero predicate distinguishes unordered — 79

QUESTION: does the floating zero guard conflate unordered (NaN) with zero?
Major system ScriptVM arithmetic, FABLE BF-1 semantic/OPUS VM contract consumers.
Current BF-1 says OPDIV guards zero on both paths; this result supports it and
provides its exact predicate. It does not report a canonical regression.

METHOD A, STATIC_ONLY. Original OPDIV298 bytes `0025F0AC..0025F1D6`, opcode15
dispatch entry, original24-byte descriptor/name pointer and OPDIV string identity.
Shipping EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Retained certified reader, reviewed access-role adapter, exact source/init/result
bytes, immutable consumer preimage plus separate dirty hash, tool/provider pins,
raw/reducer/driver and receipts. No new guest/native/live or prior77 replay.

SOURCE OBSERVATION: `UCOMISS XMM6,XMM7` at25F197, then `JP25F19A` and `JNE25F19C`
both target `DIVSS XMM0,XMM6` at25F1A3. Only ordered-equal (`PF0/ZF1`) substitutes
XMM7 into XMM0 at25F19E. Top/popped operand becomes divisorXMM6; lower/next operand
becomes dividendXMM0. Original local interpreter setup at25E555 setsEBP1 and
25E55F zerosXMM7. This is source-backed setup, not actual live initialization or
proof every native callback preserves it. Result tagging/payload write has a
capacity check; no actual stack effects were executed here.

| supplied comparison flags | source branch |
|---|---|
| ordered equal PF0/ZF1 | substitute XMM7 |
| ordered unequal PF0/ZF0 | DIVSS |
| unordered PF1/ZF1 | DIVSS |

These are conditional source calculations, not three game or original-code tests.
Under supplied/source-backed zero baseline, zero uses the zero-result branch;
unordered avoids it. The proposed conflation is REFUTED without an expensive test.
No arithmetic result, NaN propagation/status or native exception policy is claimed.

CONTROLS: table/name/handler identity, exact JP/JNE targets, DIVSS order, source
zero substitution and integer zero branch. Actual shared adapter classifies
store/read/LEA; labelled private RMW bytes control its affected role. Raw-default
and three rejected alternatives cover lost parity, reversed division and an
integer TEST/JE replacement. BF-1 K9's narrower zero guard remains valid; extending
the specification can add exact parity/order checks without calling K9 a failed
NaN contract it never claimed.

PREPARATION LESSON: an initial adjacent companion offset25E67B decoded from inside
an instruction. It was never raw/result or accepted evidence. Original helper is
retained inert with failure note; actual capture/check uses real branch target
25E682 and fully decoded64 bytes. No accepted conclusions relied on bad slice.

LIMITS: no execution of opcode, classification helper/calls, callbacks, pop/push,
DIVSS/IDIV results, native status/unmasked exceptions, actual game RC/caller/values,
full interpreter or live presentation. Integer INT_MIN/-1/exception policy remains
unsettled. Consumer incorporation and independent acceptance pending. PC OFF, no
host instrumentation/save/config/reference changes. S19 consumed allowance and
unapproved extension persist. Full L1+L2 goal ACTIVE / NOT_MET.
