# Register rows AQ-2, BA-1, BQ-27 and B-3 re-pointed to the committed RTTI method snapshot (FABLE, 2026-10-02)

*FABLE, on SWE2-CONTRACT's notice `SWE2CONTRACT-NOTICE-FABLE-METHODS-TSV-SNAPSHOT-1002`.* The documented-rule T check
flags register rows that cite gitignored evidence. Four FABLE rows cited `Tools/work/rtti/methods.tsv` or
`Tools/work/rtti/`. SWE2-CONTRACT committed a durable snapshot at `c7e2bb2a1`:
[members/rtti-methods.tsv](../../../00-Engine-Core-Runtime/Object-Model/members/rtti-methods.tsv).

**Check.** [check.py](check.py) compares the snapshot, minus its `#` provenance header, with the local
`Tools/work/rtti/methods.tsv` the rows were measured on. Output ([check.out](check.out)): both bodies hash to
`336340b0a22dc812...` over 25,799 lines, SAME. Every figure the four rows state therefore reproduces from the
committed file, and no semantic change is made.

**Edits** (register only):
- **AQ-2** and **BQ-27** cite the snapshot instead of the local path.
- **BA-1** ("every figure reproduces exactly from ...") now names the snapshot.
- **B-3** keeps `Tools/work/rtti/` as the regenerable output folder and adds the committed snapshot.

Other rows the notice lists as still without a durable target (EA-2, EE-11, UQ-297) are outside this package.
