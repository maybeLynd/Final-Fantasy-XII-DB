# Navigation: instruction semantics versus admitted conversion domain

**PASS_STATIC_ONLY — A. No new original-code executions or live runs.**
Uses exact committed`bff8d55d0053e538360dfabc3631e9a06f0c6f15` source.json,
checked against that commit's nonempty manifest and ancestor identity. Full
00383F10 body542B SHA`03d069e5f80b0ca4064fe36f11683df4110a494a96d7f920e1d43c19e1bef773`,
shipping image73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8.
Retains original bytes/import witness and current canonical navigation-page preimage.
The parent's B fixture and finite host classifier stub are provenance, not proof
of the native library's effects. No settled upper-bound tests were rerun.

Question: the page's four-arithmetic-behaviours section correctly names signed
IDIV/CVTT semantics, but says an out-of-range coordinate becomes a very negative
cell index and is rejected downstream. Does the actual stable finite query path
admit those conversions, and is there a downstream index-range rejection?

Original source requires **four earlier ordered bounds**, before either CVTT:

| guard | original condition that exits FF | requirement to continue (finite stable point) |
|---|---|---|
|00383F77|originX > X|X >= originX|
|00383F93|originZ > Z|Z >= originZ|
|00383FAF|X > originX + cw*cols|X <= originX + cw*cols|
|00383FCD|Z > originZ + ch*rows|Z <= originZ + ch*rows|

Origins are **signed16** at header+4/+6 (`movsx`), cell widths/heights and
counts **unsigned8** at+0/+1/+2/+3 (`movzx`). Each product is at most255²=65025;
the largest absolute upper coordinate is32767+65025=97792. All those integer
endpoints are exactly representable in binary32, and integer construction does
not overflow. With stable finite point/header/bindings, exact subtraction is in
`[0,65025]`; ordinary binary32 rounding keeps it within the same representable
endpoints. Thus00383FF7/00384020 CVTT results are **0..65025**, not negative or
the invalid-conversion integer-indefinite. This is an interval/source proof,
not a fresh native float test, actual caller state or installed MXCSR observation.
FP exception behaviour/continuation under unusual controls is not certified.

**Generic instruction facts remain facts.** CVTT on invalid input has its ISA
behaviour, and signed IDIV truncates toward zero. Those facts are distinct from
the admitted domain of this function. Stable finite points below origin or above
upper bounds take the original earlier exits; they do not reach a negative index
that the query checks and rejects later. The corrected domain statement requires
stability: the function reloads point/header words after calls and guards, so no
atomic snapshot or safety under concurrent mutation is inferred.

The source calls import IAT008C2C10 `_fdclass` twice and explicitly exits FF when
returned AX equals2, at00383F48/5E. That branch is **before CVTT**. This A package
proves the source branch/import identity, not classification by the installed
native provider. It does not turn the parent's finite stub into NaN evidence.

After conversion, nonzero divisor is a separate precondition to completing IDIV
at00384001/25. Source has no zero-divisor guard. With nonzero u8 divisors, quotient
can reach the corresponding count; the combined index has coarse upper bound
`255*255+255=65280`, still nonnegative/int32-safe. But **int32-safe is not in-table**:
00384027 adds,0038402A sign-extends,0038402C immediately reads the cell word.
There is **no postconversion index-range guard**. The FFFF sentinel check occurs
after the read. Existing equality and finite rounding out-of-table observations
in nav-upper-bound-admission remain valid and open for consumer incorporation;
this domain proof neither repeats them nor removes their required preconditions.

`check.py` independently decodes retained raw bytes, fixes complete body identity,
checks all field-extension/guard/product/conversion/division/load sites, requires
all four interval obligations and exact representable endpoints. Widened16-bit
extents would exceed INT32 and invalidate this proof; dropping a bound would lose
that axis's obligation. These controls expose the representation dependencies,
not manufactured native cases. Frozen validation is compared, never overwritten.

Reusable limits: stable finite point/header/reference bindings, readable objects,
normal ABI; nonzero divisor for completed division. No live initialization,
classifier/native callback effect, atomicity, allocator placement, authored
occurrence or all-caller validity. FABLE owns mechanism-page corrections, OPUS
the representation/precondition contract; independent SPEC acceptance pending.
Artifact-only cleanup; PC OFF, game/saves/config/reference unchanged. Menu recovery
allowance remains spent/unapproved; whole accepted L1+L2 and final audit NOT_MET.
