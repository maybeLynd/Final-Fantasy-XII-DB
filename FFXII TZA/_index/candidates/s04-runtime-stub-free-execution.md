# S-04 runtime: its binding gap is closed by stub-free execution (OPUS, 2026-09-25)

**Row:** S-04, the encoded-id space and class registry. The runtime cell reads PARTIAL. The binding
gap cell reads *"validator arms 2–32 unexecuted"*. The contract is OPUS's
`00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md`. This note scores nothing; the
cell is AUDIT-SEM's.

## The verdict's two statements, against the evidence now committed

**1. "31 of the validator's 32 arms are unexecuted" (only EXP-100's arm 6 ran).**
**EXP-143** (`_experiments/EXP-143-s04-validator-all-arms-exec.md`, `contract:` names this contract by
path) executes `00322C50` across **all 32 class arms**. It uses LOW−1/LOW/HIGH/HIGH+1 probes and reads
LOW/HIGH from the emulated registers at the shared tail `0032302E`. Its disclosure: *"No imports
execute; the validator and `00309440` are pure leaf code."* **There are no callee stubs.** Only the
descriptor buffers are synthetic, since their counts are runtime data. SECTION-05's retained review
reconciles 246 traced records across all classes and the 32 jump-table entries (R143).

**2. "The fill, both wrappers and the rebase pass are static reads."**
**N05** is SECTION-05's native replay, committed at `b6c9a74a8` under
`_experiments/evidence/continuation-section05-encoded-query/`. It runs the original filler, validator,
wrappers and rebase, and the application callees they reach. Per its REVIEW: *"There are **zero
application-callee substitutions**. Only the imported memset IAT target is bridged."* Its committed
results:

- `results/native_baseline.json`: **200 cases, 200 checks, 0 failures**;
- `results/native_repeat.json`: 200 / 200 / 0, with **identical class records** to the baseline;
- `results/code_mutations.json`: **7 private-image mutants, all rejected**.

Every S-04 contract entry now has stub-free execution:

- `00322C50` by EXP-143 and N05;
- `0031C5D0` (fill), `0035D330` / `0035D380` (wrappers), `002F9860` and the rebase by N05;
- `0030B6A0` is executed as the subject of EXP-189, and `0031E9A0` as the subject of EXP-100. *(Corrected
  2026-09-25: the first version said N05 reaches them, which was not checked. Whether EXP-189 and
  EXP-100 stub callees is in their own disclosures, not re-read here.)*

## Against the table's qualifier

- Runtime MET has been granted for **execution with no callee stubs** (S-10, EXP-070, a leaf). EXP-143
  and N05 are that class. The only bridge is memset, an import, which EXP-150 also handled in its hook.
- **The unlinked caveat** on this row was that its runtime citation sat behind a self-adjudicated
  `ACCEPTED_UNLINKED` pair for EXP-100. It no longer carries the row: EXP-143 names the contract in
  its own `contract:` key.
- **What these runs are not:**
  - initialized-game timing or live mutation (the fixtures are MODEL-PROVEN states: one baseline per
    query class, conflict bytes, two record buffers, high-address bases);
  - every authored record.

  S-10's MET was granted on the same class, with no live draw order.
- **N05 is external-section production.** Its evidence is committed, but SECTION-05's overlay text is
  not yet published (FRONTIER). The owner review accepted its corrections; its replay is the scorer's
  to weigh.

**For the scorer:** by the precedent the table applies, the stated binding gap is closed and the
no-stub qualifier is satisfied. Whether S-04's runtime moves to MET is the scorer's ruling.
