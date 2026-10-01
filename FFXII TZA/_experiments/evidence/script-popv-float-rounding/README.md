# Float-kind coercion depends on MXCSR rounding — 72

Method B: **two** original-code guest controls, retained without replay. The
integer-kind70 cases were not rerun. Two controls settle this specific question;
negative inputs/directed-down/other float domains are not claimed or added merely
for counts. Original selected float-kind postresolve stage starts at `00267E9C`,
stops at `00267F1E`, then an explicit second-entry ABI intervention invokes the
verified original store leaf. Resolver/query/full POPV/native/live execution is
omitted at boundaries; no callback stubs.

Question: an always-nearest host cast or raw integer-bit copy versus original
`MOVD/CVTDQ2PS/MOVSS` coercion governed by masked MXCSR RC. Injected record.kind2,
descriptor58000000 (float width5 +bit27), selectorR8D1, depth1/tag1/payload16777217,
stack and destination guards. Source/kind/branch identities and provider files
match exact published70 originals. EXE SHA256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

| source-derived initial MXCSR | executed converted float bits | stored float value |
|---|---|---|
| masked nearest-even1F80 | `4B800000` | 16,777,216 |
| masked toward-positive-infinity5F80 | `4B800001` | 16,777,218 |

The source/input invocation differs only in RC. Visits establish actual MOVD,
CVTDQ2PS and value store, not merely successful tool calls. Exact converted bits,
depth decrement, record+20, destination dword, guards, code/table/sentinel and full
store return are checked under32+64 instruction budgets. The actual sourcecompiled
shared adapter classifies conversion payload read and record write. Native MXCSR
flag/status and unmasked parity remain unproved; guest status values are preserved.

**Input-label correction:** the initial feasibility adapter looked for dictionary
key syntax in AST-unparsed `dict(keyword=...)`. The executable `reg_write` received
the requested1F80/5F80 and R8D1, but the returned initial metadata retained literal
1F80 for both cases and omitted the selector label. The first semantic reducer
failed on that missing metadata before producing a result. Original raw and
executed runner are immutable. `state-metadata-correction.json` derives normalized
inputs from the preserved original invocation/source plus recorded poststage RC.
This is **not a newly measured initial state**. No accepted consumer conclusions
depended on the failed reducer; the original pilot was explicitly unaccepted.

Producer fix matches the actual keyword constructor, asserts the replacement,
and includes selector/RC metadata. An AST-selected control executes the actual
producer's string adapter and initial metadata constructor with dummy buffers:
RN/RU labels differ, a literal-nearest label would fail. The actual raw-default
invokes that control and reduces unchanged raw; no two-case recapture. Frozen old
helpers/failure correction remain evidence. Checker faults reject always-nearest,
raw bit-copy and using the original stale input label. The corrected adapted runner
is preserved separately and was **not** executed as new original guest evidence.

Consumer: preserve MXCSR RC dependence of this exact tested float-kind integer
coercion in OPUS contracts/specs and FABLE prose, with state-label correction and
source-derived input limitation. DATA propagation and SPEC independent acceptance
remain pending. No inference about valid shipped kind/width combinations, normal
caller reachability, actual bank state, initialization, scheduling, lifetime or
live presentation. No native allocation/process/PC/save/config/reference changes.
S19 spent budget/unapproved extension persist; full L1+L2 DB_GOAL=NOT_MET.
