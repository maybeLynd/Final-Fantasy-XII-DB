# OV42 follow-up: special-action selector preconditions

**Question, chosen before process setup:** can ordinary action-table values
cause a negative narrowed ns8 index; does the immediate parent gate exclude
the `FFFF` sentinel? Existing native selector/owner byte sequence is retained
in the first packet, commit9fffe3ca12e484df00b7e147252f123a1277b804.
Choose retained original data and code plus bounded predicates (method1–3),
not a forced native call or live gameplay.

**Results at producer level:**

1. All nine shipped `battle_pack.bin` action tables have543 rows of60 bytes.
   Every non-sentinel word+24 gives `(4*word+1) mod65536 <32768`.
   This excludes that data-value subset as a negative owner-index source.
2. The `FFFF` word occurs in68 rows per pack. The hypothesis that the
   immediate parent bit30 gate excludes all of them is **false**. Ordinary
   rows511..534 have word+24=`FFFF` AND flags+0C=`40000211` in every pack;
   they satisfy the local bit30 predicate. They are above the parent's
   D0..F1 special exclusion range. No claim that play selects these rows.
3. Row113 also has word+24=`FFFF` and bit30, but `00309230` has a distinct
   pointer-identity branch for it. Under successful identity/codec premises,
   it reads the actor type and indexes a thirteen-entry stack table instead
   of returning word+24. The actual type bound/row identity must be proved;
   this packet does not assert unrestricted type safety or natural entry.

**Original path:** `0030CE10` normalizes a row, tests bit30 at0030CE93,
and skips to0030CF31 if clear. A surviving path calls00306BD0 at0030CF0D.
That loader's bounded prefix calls00309230 at00306C4D, moves EAX into EDX
and calls0032FC30 at00306C56. The helper's ordinary arm is an unsigned
word load at003092C5 with no mask or local range clamp. These are source
relationships, not observed execution, initialized manager or successful IO.

**Primary inputs and provenance:** shipping EXE73461d08…21f8/base120000;
`special-admission-raw-01.json` preserves complete contiguous code spans,
bytes and the actual shared-role adapter controls. `action-selectors-01/`
preserves nine exact selected `st2e` tables and the source entry/table hashes.
All nine retained full packs were compared byte-for-byte against the current
designated test archive entries. The archive size/index hash and exact entry
metadata/hash are recorded; **no whole31GB archive hash was computed**.
Do not represent index identity as a whole-archive digest. Extractor source
and final driver hashes are in result receipts.

**Controls/results:** actual native role path checks SSE store, LEA and RMW.
Action-table reader rejects missing/truncated directories and wrong descriptor
pointers; a changed actual word to2000 is detected as non-sentinel negative.
Admission reducer independently requires original instruction witnesses and
table identity, detects that changed word, and clears the candidate set when
all bit30 flags are privately cleared. Truncated table is refused. These are
private input/claim controls, not code execution or independent peer acceptance.
All completed captures/reducers exited0; earlier caller reader missing-positive
and whole-fragment decode failures produced no accepted result. Successful
caller prefixes use the actual25DAED call, not25DAE1 argument setup.

**Semantic consequence:** stop treating either population limits or a bit30
test as proof that no negative owner submission can occur. Most action values
are ruled out by a real complete data invariant. The residue is precisely the
admission of rows511..534, the row113 identity/type branch and other selector
sources. Sentinel-derived full indices also exceed the FST row/array bounds;
this packet does not claim their size lookup, primary load, companion directory
or later owner submit succeeds. A synthetic forced call would skip these gaps.

**Next discriminator:** inspect command/AI/script action-id producers and
eligibility for rows511..534 before0030CE10; prove exclusion, or a valid shipped
selection path. Then analyze loader/metadata/owner ordering if that path exists.
Also complete ordinary eventread/summoneventread and field selector domains.
Original caller prefixes already show the eventread clamp applies to the
manager, not the DWORD selector; no native signed16 bound is established.
All whole OV42/OV21 reachability obligations stay OPEN. Newly closed whole
runtime questions remains0. FABLE semantic/OPUS contract consumer after SPEC
independent review; peer pages/raw inputs are not edited here.

**Cleanup:** read-only source/data and copied evidence only. No process, PC
control, input, instrumentation, save/config change or detach needed. First
published packet remains immutable. No menu setup or EXP127 trace repeated.
