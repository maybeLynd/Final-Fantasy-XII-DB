# Consumer clamp misses signed-min dimension wrap — 73

**STATIC_ONLY, method A.** Original shipping instruction analysis plus execution
of the unchanged published consumer's Python function/default, not original FF12
instruction execution, a live array or observed storage fault.

Question: does the consumer's unqualified negative-dimension `dim-1` rule preserve
the original 32-bit computation at INT_MIN, or extrapolate unbounded arithmetic?
Exact original591B resolver is pinned at69 commit3a7de76e, EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Original FABLE primary/default/source/AST/commit identity is retained unchanged.

At `00262513`, **LEA EAX,[RSI-1]** writes a32-bit result. For signed dimension
`80000000` (INT_MIN), its upper-bound bits wrap to`7FFFFFFF`. The following signed
`CMP ECX,ESI / CMOVL EAX,ECX` cannot select the nonnegative lower-clamped ECX
against that negative dimension. The conditional predicted result is therefore
**+2,147,483,647**, not −2,147,483,649.

The unchanged FABLE `clamp()` uses Python `dim-1` and returns −2,147,483,649 for
all three tested signed indices−1/0/INT_MAX at INT_MIN dimension. Its actual
original default still exits0/FAILS0: its fixtures cover dimensions3/0/−2 but
miss this boundary. This is a concrete producer/control gap, not a declaration
that the entire canonical index or69 original precondition finding regressed.

Positive controls preserve previous outcomes at dim3/0/−2 and INT_MIN+1. The
corrected private Python predicate uses signed32(low32(dim-1)), matching the
decoded source calculation. Calculations and model agreement are explicitly
**not original instruction execution**. The actual sourcecompiled shared adapter
marks LEA as address calculation; exact operands/bytes/signed CMOV predicates
establish the original width and branch. Two checker faults reject unrestricted
real-number subtraction and treating a green producer default as coverage.

Consumer change: repair FABLE's actual `clamp()` producer/default/control and
the negative-dimension prose/contract/spec to preserve32-bit subtraction; add
INT_MIN and neighboring boundary controls. Route OPUS's similar formula where
affected. Keep positive-dimension/dim0 claims and original source/history intact.
No peer-owned file was edited. FABLE/OPUS/DATA consumers and SPEC independent
review/adjudication remain pending.

No actual shipped INT_MIN array, accepted malformed resource, native access/fault,
storage safety, flatten-product overflow, fullresolver/bank initialization,
lifetime, normalcaller reachability or livepresentation is proved. No process,
PC, instrumentation, save/config or reference binary changes. S19 spent budget
and unapproved extension persist. Full L1+L2 DB_GOAL=NOT_MET.
