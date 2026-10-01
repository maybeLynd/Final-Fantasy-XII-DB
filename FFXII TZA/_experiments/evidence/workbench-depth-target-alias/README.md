# A saved destination can change Restore's remaining count

**PASS_STATIC_CONDITIONAL — method A, not a new execution or live observation.**
Full shipping Save89B0036D930 and Restore66B0036D8E0 are retained in source.json,
verified against executable SHA73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Save SHAebabe24f505f83317a9b63e3ebc8556c5d1207cdf926f3bb1b2a1f754a7bddda;
Restore SHA5bb9d143a12bf8959ae1c75d5f7245c4b1081d9ae3432095ebfd253953ec253b.

The contract states no Save may be outstanding and then promises that Restore
returns every named item's 16B to its Save-time bytes. The first condition alone
does not establish the promise for arbitrary otherwise-valid target pointers.

Save copies each target into the value array before assigning count to depth at
0036D982. Restore reads depth at0036D8E6, writes the current saved value through
its saved pointer with MOVUPS at0036D90F, then **reads depth again** at0036D912.
The unsigned JB0036D918 uses that new memory value. The count is not latched at
entry. Its final zeroing at0036D91A is a separate write.

| Conditional source layout, initial depth0 / count2 | Predicted restored slots | Second row |
|---|---|---|
| target0=022D8F08 depth; target1=022D8F90 | 0 only | caller's clobber remains |
| target0=022D8F30; target1=022D8F90 | 0,1 | original bytes restored |
| target0=022D8F90; target1=022D8F08 depth | 0,1 | both named snapshots written |

For the first case, target0's snapshot contains zero depth, because no Save was
outstanding. Save records both valid pointers and then assigns depth2. The caller
clobbers only the separate row. Restore writes saved zero into depth before its
comparison; EDX is1 and unsigned1<0 is false, so target1 is skipped. Both pointer
and value arrays are assumed valid/disjoint from these targets and unchanged;
this does not need an invalid pointer, nesting or a caller overwriting depth.

These are **source-level conditional calculations**, derived from the pinned
instructions; result.json is not a raw runtime trace. Its source-transfer helper
is explanatory and checked against the byte obligations. Agreement with that
helper alone would not prove original execution. No emulated/native/live run was
performed here, because original store/read order distinguishes the hypotheses.

A useful sufficient condition for this specific hazard is that restored 16B
destination spans exclude the four counter bytes at022D8F08..022D8F0B. It is not
necessary in every layout: the depth-last contrast succeeds. This packet does
not classify all target/value/pointer-array overlaps, concurrency, invalid counts
or other ABI/validity obligations, and does not prove a shipped caller reaches
the counter-target layout. The existing nine-caller row findings remain separate.

**Consumers:** OPUS contract/precondition and executable-spec scope; FABLE save/
restore semantics. The existing differential source is retained, not rerun. Its
ordinary disjoint fixtures do not settle this alias question. The old OPUS S05
candidate/request calls the pair's first execution absent, while the primary
contract §13 already records its isolated pair differential run; attribution and
evidence class should be reconciled, not fixed by another ordinary capture.

Source identities, complete decode, real RIP destinations, exact target-store
width, both counter reads and unsigned branch ordering are checked. The checker
verifies an existing immutable result and never rewrites it on a normal check;
missing or differing results fail. Independent review and canonical incorporation
remain pending. Producer/control preconditions and limits are in PLAN.md.

**Player version:** this is about preserving temporary graphics data. Saving a
pointer to the mechanism's own counter can make it stop restoring too soon. It
is a contract hazard for modifications, not an observed failure during gameplay.
No game/PC controls, process attachment, save/config/reference writes occurred;
no live cleanup or normal-game responsiveness claim is made.
