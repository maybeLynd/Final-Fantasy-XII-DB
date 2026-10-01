# OPUS's own raw-flag readers moved onto the shared access policy (OPUS, 2026-09-28)

**Why.** SOL's procedural-mode-cost producer bypassed the corrected shared policy and trusted capstone 5.0.7's raw
operand flags. SOL repaired its own producer with a bounded adapter to `reg_tracking.op_kind`. The canonical index
did not regress. The right owner for the other raw-flag readers is whoever wrote them. OPUS's
[access-flag-producers](../access-flag-producers/README.md) record listed nine. OPUS authored eight of them (commits
under `maybeLynd`, OPUS's git identity). **The ninth was a false positive in that list:** it is FABLE's, and it does not
read raw flags.

**The policy, unchanged.** `Tools/analysis-kit/gfz-scripts/reg_tracking.py`:
- `op_kind` (from 8e15ad96d) labels memory operands;
- `written` gives register kills, with sub-registers folded and capstone's implicit-write defects for `cmpxchg`, `cdq`
  and `test` corrected.

No new classifier is added. Every repair either routes a label through `op_kind` or a kill through `written`.

**Method, per producer.** Run the committed version and the repaired one on the same inputs, diff the outputs, then
check every claim that rests on a changed output.

| producer | change | measured effect | claims checked |
|---|---|---|---|
| `type-flow-census/type_flow_census.py` | register kills via `written` (labels were repaired in e90e6c0b3) | all 23 `recut_check.py` runs and `cpe_recut_check.py` FAILS 0, with and without `--receipt`; every regenerated receipt is **byte-identical** | store rows it feeds: unchanged |
| `crr-flow-census/crr_flow_census.py` | labels via `op_kind`, `nop` / `prefetch` carry no operand, kills via `written` | 8 `movups` stores r -> w, 1 `nop` row dropped; receipt regenerated | the 8 cited sites (`003E5E38`, `003E5E43`, `004204BE`/`C6`/`CE`/`D7`, `004217E9`, `00424185`) are already described as stores or block copies in `_types/fields.tsv`; `crr_flow_check.py` FAILS 0 |
| `crr-flow-census/crr_flow_check.py` | writes the tracked receipt only with `--receipt` (it used to rewrite it on every run) | - | the same guard the type-flow checks carry |
| `bl8-b0-nas-review-opus/tfc_multi_static.py` | as `crr_flow_census.py` | 3 `nop` rows dropped; the four `+0xB0` rows identical | BL-8 negative 2 (only the constructor self-link and the destructor at `+0xB0`) stands |
| `t4-initializer-closure/t4_closure_check.py` | r / w sets via `op_kind` | FAILS 0, unchanged | its closure claims stand |
| `static-gap-row-audit/span_census.py` | r / w via `op_kind` | `EeVu0RegisterBank +0x490` and `+0x224` identical; `AppBootStatic01F7F480 +0x10` / `+0x20` read 1 -> 0 (`lea` at `0017D990` is address formation) | the rows already say "address taken"; the audit's 137 / 140 used reference existence only |
| `s25-probes/p1_walk_static.py` | r / w via `op_kind` | output identical | S-20 / 24 / 25 stub-exposure claims stand |
| `undeclared-written-statics/undeclared_written_statics.py` | writes via `op_kind` | +363 write targets (`movups` stores), 346 of them undeclared | the headline is struck and corrected in its README: 10,251 of 11,587 (88.5%), 1,253 clusters, on the 2026-09-28 store |
| `Tools/analysis-kit/gfz-scripts/member_reach_scan.py` | register kills via `written`; `lea` stays excluded, as before | `--self-test`: all controls behave | none changed |

**Correction to access-flag-producers' list.** `02-Resource-And-Asset-Pipeline/members/image_address_base_writer_bounds.py`
(FABLE's) was listed as a raw-flag reader, and it is not one. Its line 8 is a comment saying it never uses `op.access`,
because the flag is wrong for `movups` stores, and it classifies by operand position instead. The list was built with a
grep that matched that comment. A notice raised to FABLE on the same mistake (OPUS-NOTICE-FABLE-RAW-FLAG-WRITER-BOUNDS)
was withdrawn with a note. The published record stays as run, and this line supersedes its ninth entry.

**What this does not do.**
- It does not reclassify any cohort from one sentinel.
- It does not rewrite immutable `_experiments` receipts.
- It does not touch function boundaries or admissions.

Affected: `_index/candidates/undeclared-written-statics/README.md` (the headline struck and corrected)

**Run receipt.** Run verified at e779af776: the per-producer comparisons above, each on identical inputs.
