# Access-flag producer repair (OPUS, 2026-09-27)

**Request:** FRONTIER-REQ-OPUS-ACCESS-FLAG-PRODUCER-REPAIR, a bounded repair with no new classifier.

**State: PENDING REVIEW.**

**The policy.** This record uses `reg_tracking.op_kind` / `reg_tracking.written`, introduced in 8e15ad96d ("238 reversed
access labels were two capstone defects"). The hash the request names, `3b0727b9e`, does not exist in this repository.
Under that policy, the mnemonic tables from the SDM are consulted first and capstone's operand flags only after. An
operand with no flag is `?`, never a positional guess.

**What was wrong.** Four producers still read capstone 5.0.7's raw flags:
- `arg_extent_scan.py`
- `census_receiver_fixpoint.py`
- `disp_image_census.py`
- `singleton_field_scan.py`

Measured over all 733,142 memory operands in the image, the raw labels disagree with the policy at **23,260 sites**
([`changed_sites.tsv`](changed_sites.tsv): site, old, new, mnemonic, operands):

| old → new | mnemonic | sites |
|---|---|---|
| read → write | `movups` (store form) | 13,816 |
| read → none | `nop` (multi-byte padding) | 8,662 |
| none → read | `test [m], reg` | 477 |
| read → write | `movq` / `movhps` / `movd` / `movhpd` / `movlpd` / `vmov*` / `setcc` stores | ~270 |
| read → read+write | `lock cmpxchg` | 30 |
| read → none | `prefetch*` | 5 |

The trackers also killed registers by capstone's exact register id, so `mov ecx, 1` did not kill a tracked `rcx`. They
used capstone's implicit-write tables, which are wrong for `cmpxchg`, `cdq` and `test`.

**The repair.**
- Each producer now labels memory operands with `RT.op_kind(ins, op, oi)`:
  - `addr` for `nop` / `prefetch` is skipped as a non-access;
  - `lea` stays separate as before;
  - `?` is counted as unknown, never as a read.
- The three register trackers kill through `RT.written(ins)`, folding sub-registers to their parent.
- Every producer's own self-test still passes:
  - `arg_extent_scan`: four reach controls;
  - `singleton_field_scan`: three offsets plus the static-mode control;
  - `disp_image_census`: the known-displacement control;
  - `census_receiver_fixpoint`: 147 displacements, gate ≥ 130.

**Regression.** [`../../../../Tools/analysis-kit/gfz-scripts/test_access_policy_producers.py`](../../../../Tools/analysis-kit/gfz-scripts/test_access_policy_producers.py)
checks three things:
- **STATIC:** none of the four producers reads a raw flag, and each routes through `op_kind` (and `written` where it
  tracks registers).
- **POLICY:** 13 hand-encoded instructions, covering store, load, `lea`, `nop`, `prefetch`, `lock cmpxchg`, both `test`
  forms, `cmp`, `setcc` and a plain read-modify-write.
- **KILLS:** a sub-register write, `cmpxchg`, `cdq` and `test`.

It passes, and its STATIC part fails on the pre-repair producers.

**Affected claims, found by the site list, not by re-running everything.**
- 38 type-store rows cite one of the four producers and name a changed site.
- 27 of them already described the site correctly by hand ("block store", "write 0030EDC7", "carried by the 16-byte
  copy") and are unaffected.
- **11 rows relied on the wrong label and are corrected in `_types/fields.tsv`.** Each correction strikes the old text,
  states the new label and cites this record:

| row | was | now |
|---|---|---|
| `CorridorNavAgent +0x070` / `+0x080` | `r1 w0` at `002030C9` | `r0 w1` (a `movups` store) |
| `CorridorNavAgent +0x090` | `r1 w3` | `r0 w4` |
| `LegacyPs2GsTextureContext +0x00` / `+0x10` / `+0x20` / `+0x30` | `r0 w0` | `r0 w1` (`movups` stores) |
| `ManagerSub0209BE80_8FA0 +0x10D0` (census line) | 1 read, 1 write | 0 reads, 2 writes |
| `SpawnRecord +0x070` | `002335AF … r` | `w` |
| `CPostEffect +0x3B8` | read at 3 sites incl. `006FF784` | 2 sites; `006FF784` is `nop dword ptr [rax]` |
| `ImageBackedStateBlock +0x0000` | 4-byte hits `00252ED9` / `0025364C` | qualified: those are `nop` padding; the width rests on `003153A4`; the read count is not re-derived |

**Residue, bounded and named.**
- Other rows cite these producers' counts without naming a changed site. Their counts may still include a
  `movups`-store-as-read or a padding `nop`.
- `changed_sites.tsv` is the instrument: any row's cited count can be re-checked against it, or the patched producer can
  be re-run for that type.
- Only claims that turn on direction are at stake: "read-only", "WRITE-ONLY", "rN wN". Widths and extents are unaffected,
  because `op.size` was never wrong.

**Found in passing, NOT repaired here (reported to FRONTIER).** Nine more scripts read raw flags:
- `FFXII TZA/_index/candidates/type-flow-census/type_flow_census.py`. This is OPUS's re-cut census, and CPostEffect's
  `006FF784` came from it. Repair will be a separate OPUS package with its own measurement.
- `crr-flow-census/crr_flow_census.py`
- `static-gap-row-audit/span_census.py`
- `undeclared-written-statics/undeclared_written_statics.py`
- `bl8-b0-nas-review-opus/tfc_multi_static.py`
- `s25-probes/p1_walk_static.py`
- `t4-initializer-closure/t4_closure_check.py`
- `Tools/analysis-kit/gfz-scripts/member_reach_scan.py`
- `02-Resource-And-Asset-Pipeline/members/image_address_base_writer_bounds.py`

The `_experiments/evidence` checkers are immutable receipts and are not edited.

**Run receipt.** Run verified at 60e631848:
- `test_access_policy_producers.py` FAILS 0;
- the four producers' self-tests pass;
- `types_index.py --validate`: 0 errors.

**Correction, 2026-09-28 (OPUS): this repair broke `census_receiver_fixpoint`'s `EMIT_JSON` flags.**
- The repair stored `RT.op_kind` in `_k`. Two lines later the per-site key reuses `_k`, so the per-site test compared a
  tuple against `("r", "rw")`. Every `EMIT_JSON` site was written `[0, 0]`.
- The printed read and write totals and the per-displacement detail lines were **not** affected: they count from the
  label before the reuse. The 11 row corrections above rest on `changed_sites.tsv` and are unaffected.
- Consumers of the per-site flags:
  - SWE2-DATA's `census-rerun/evaluate.py` last ran on 2026-09-23, before the repair.
  - `static-gap-row-audit/ptr_gap_ctor_cross.py` reads only site keys.
  - No `EMIT_JSON` receipt has been committed since 6b6a423db.
- **Fix:** the label has its own name, `_ak`.
- **Regression:** an EMIT part in `test_access_policy_producers.py` runs the census on RampChannelRecord (cell
  `02B40528`, extent 0xE0) and requires `003B64D7` (`mulss xmm0, [rbx+8]`) to be `[1, 0]` and `003B573D`
  (`mov dword [rbx+8], imm`) to be `[0, 1]`. It FAILS with the defect restored.
- Found while building `ramp-channel-recut/`.

Run verified at daec30974: `test_access_policy_producers.py` FAILS 0; `census_receiver_fixpoint.py --self-test` PASS
(147 displacements).
