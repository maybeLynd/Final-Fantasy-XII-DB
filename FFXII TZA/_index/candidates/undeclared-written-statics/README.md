# Written static state that no type declares (OPUS, 2026-09-25, block 275)

**Question.** The types criterion reads the contract-named-state census, which is at UNDECLARED 0. That census only
covers the addresses contracts name. How much of the *written* static state has no type at all?

**Instrument.** `undeclared_written_statics.py`:
- takes every rip-relative memory operand with **write** access (the shared policy `reg_tracking.op_kind` since 2026-09-28; capstone's raw flag before), in every function of
  `Tools/work/graph/functions.tsv`, whose target lies in `.data`/`.bss` (`01C00000..02FFFFFF`);
- subtracts every declared `STATIC` / numeric-`ARRAY` span, and each `PTR` cell (8 bytes);
- clusters what remains (gap ≤ 0x40) and ranks clusters by the number of distinct writing functions.

Output: `undeclared_written_statics.out.txt`, all clusters (1,253 as regenerated 2026-09-28).

~~**Result: 10,246 of 11,224 write targets (91%) are outside every declared static span, in 1,251 clusters.**~~ **Corrected 2026-09-28 (OPUS): the write test read capstone's raw flags, which call `movups` stores reads.** Re-run on the store as of 2026-09-28 with the shared policy (`reg_tracking.op_kind`): **10,251 of 11,587 write targets (88.5%) are outside every declared span, in 1,253 clusters.** The raw-flag version on the same store gives 9,905 of 11,224 (88.2%) in 1,248 clusters, so the policy itself adds 363 write targets, 346 of them undeclared. The rest of the move from 91% is types declared since 2026-09-25.

**How to read it.**
- **It measures direct writes only.** Statics written only through a pointer are not counted, and neither is
  read-only state.
- **The spans come from STATIC / ARRAY / PTR routes.** A static reached only through an `EMBED`, `DYNAMIC` or `FN`
  route is counted as uncovered even if a type describes it.
- **Many clusters are library plumbing:** CRT, PhyreEngine, Lua, middleware. Undeclared does not mean important. The
  ranking by writer count is a triage aid, not a priority order.
- **It is not a gate measure.** The types criterion is the contract-named census. This is coverage debt the gate
  does not see.

**Top of the ranking, read:**
- `02E41000..02E41017` (752 writers): the Phyre script-object accessors' error context. All 747 `PObjectAccessor`
  functions store `__FILE__` / `__LINE__` / `__FUNCTION__` before reporting (`phyre-script-object-accessors.md`).
  **Declared in this block** as `PhyreScriptErrorContext02E41000`.
- `01F44D40..` (334 writers): begins with the shared byte-stream vector `01F44D40/48/50`
  (`spawn-placement-and-retirement.md`, `CONTRACT-storage-read-completion.md`). The cluster is long, and whether it is
  one object is not established.
- The rest are listed in the output for triage.
