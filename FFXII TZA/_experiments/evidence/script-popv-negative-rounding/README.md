# Negative float coercion reverses the bit-neighbor direction — 75

Method B: two **new negative** original-code guests, no positive72 case replay.
The corrected72 runner/source/code/table/provider files are verified at its actual
commitc4cbbfb8. Original integer-to-float stage and store execute under injected
postresolve kind2/descriptor58000000/selectorR8D1/tag1/depth1/stack/guard/MXCSR
state. No full POPV/resolver/lookup/native CPU/live execution or callback stubs.
EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

Question: for a negative signed input, does rounding upward make the value less
negative, or can the existing helper's positive bit increment move the wrong way?
Static model/domain inspection is combined with exact new original-code converted
bits/destination effects. First control succeeds before the second is accepted.

| input | masked mode | original converted/stored bits | float value |
|---|---|---|---|
| −16777219 | nearest1F80 | CB800002 | −16777220 |
| −16777219 | upward5F80 | CB800001 | −16777218 |

The raw float bits **decrease** for numerical upward movement in this negative
case. The actual unchanged FABLE `cvt()` helper, whose RU branch explicitly
comments **positive values**, returns CB800003 (−16777222) if called outside that
domain for RU. Its original default still passes positive-domain fixtures.
This narrows the helper's usable domain; it does **not retract accepted positive72**
or claim FABLE previously established negative behavior.

Original MOVD/CVTDQ2PS visits and exact converted record+20/depth decrement/store
write are checked, with only expected writes and unchanged guards/record/code/
table/sentinel/fullstore return under32+64 budgets. Initial labels now match actual
requested RC/selector, following72's repaired metadata path. The actual shared
adapter classifies payload read/value write; source/AST of the consumer is pinned.
Three faults reject positive-bit-order extrapolation, RU moving this value more
negative, and treating a positive-only green default as negative-domain coverage.
Raw-default reduces unchanged raw; no extra original execution.

Consumer: for a general signed32 coercion contract, use sign-aware bit neighbors
and add this negative control to producer/default/spec. Alternatively, explicitly
bound the small helper to its positive test domain **while leaving the required
negative database behavior open** until a general consumer incorporates the
original instruction semantics. Do not exclude negative VM inputs to close a
queue. Preserve new tested negative results and72 historical input-label correction.
FABLE/OPUS/DATA owners and SPEC independent acceptance remain pending.

Not proved: all negative values/directions, native MXCSR flags/status/unmasked
exceptions, actual game RC, valid shipped kind/width/value combinations, normal
caller reachability, bank initialization/lifetime or live presentation. No host
native allocation, process/PC/instrument/save/config/reference change. S19 spent
budget/unapproved extension persist; full L1+L2 DB_GOAL=NOT_MET.
