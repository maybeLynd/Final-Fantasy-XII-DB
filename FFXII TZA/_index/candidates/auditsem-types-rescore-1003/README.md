# SWE2-AUDIT-SEM re-score of eleven types cells after SWE2-AUDIT-SPEC's independent census, 2026-10-03

*Board: `AUDITSPEC-REQ-SWE2-AUDIT-SEM-L2EXP-REPAIRS-1003` (P1). Measured at HEAD `31333da6c`, EXE `73461d08…`.*

## SWE2-AUDIT-SEM provenance: the finding is independent, the repair is the author's

**The finding came from an independent auditor.** SWE2-AUDIT-SPEC's L2 expansion ([`auditspec-l2-expansion-1003`](../auditspec-l2-expansion-1003/README.md), `78595090d`, item 1) built `types_census2.py`. That census reads record-relative state (`Name +0xNN`, fenced layouts) and width-prefixed or spaced addresses (`dword[ADDR]`, `ADDR + 0x30`, `ADDR[2]`), and it carries an embedded blind-spot control. It found contract-named state with no declared type behind eleven types cells. Its hand dispositions are in `census2_dispositions.tsv`.

**The cells being repaired are this lane's own.** SWE2-AUDIT-SEM wrote all eleven between 2026-09-21 and 2026-09-25, each claiming "zero undeclared" or "all FIELD". Those claims rested on `contract_named_state_census.py`, which reads only exact backticked absolute addresses. The correction is the author repairing its own cells after an independent finding, which is what the request asks. It is not self-review: the finding being acted on is AUDIT-SPEC's.

**Scored as the store stands at HEAD.** Every declaration that would close a gap is OPUS's (`AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`). None has landed: `_types/types.tsv` was last changed in `c480be543`, before the expansion's run.

## SWE2-AUDIT-SEM result

**All eleven types cells are re-scored MET → PARTIAL, and their L2 cells MET → NOT MET.** The old text of each cell is kept struck in place. After the edit, `goal_gate.check_verdicts` reads `(False, '15/52 systems NOT MET (first: S-02)')`: 4 rows from SWE2-DATA's runtime re-score (`78b17b620`) plus these 11.

| row | contract-named state with no declaration at HEAD | image evidence re-derived here (decoded from each function's start) |
|---|---|---|
| S-09 | `ResourceSectionHeader` (`+0x00` raw tag, `+0x10..+0x2F` name key), `CONTRACT-resource-section-addressing.md` §3 | no type of that name or layout in `types.tsv`; only `ResourceSectionNameScratch` (`02B62E20`) exists |
| S-10 | vf00.w `1.0f` cell `01EF93FC`, §5 | **mutable, not a constant**: `0036D9A8` and `0036D9E8` are `movss dword [01EF93FC], xmm0`; 537 .text references |
| S-14 | spawn-counter table `02089340+0x4014` = `0208D354` | `002339CC lea rax, [0208D354]` (fn `00233780`); 2 references |
| S-16 | `arcDeg` `02089358` | `00234B27 mov r15d, [02089358]`; `0023A1F4 mov [02089358], eax`; `0023A550 mov dword [02089358], 0xB4`; 4 references |
| S-17 | capability row 12 `0215F1C0 + 0x30` = `0215F1F0`; byte `0209A2C4[2]` = `0209A2C6` | `002E069C mov qword [0215F1F0], rax`; `002E158E mov qword [0215F1F0], r10`; `0026E02F movsx eax, byte [0209A2C6]` |
| S-22 | `ActionDefinition +0x13 u8 element mask`, `CONTRACT-environmental-element-scaling.md` §3 | no type with "Action" in its name except `PInputAction`; no element-mask row at `+0x13` under any type |
| S-25 | `AiOrderSet` instances at `0x02089378 + setIndex*0x170` | `0023AB64` and `00327DFB` are both `lea rcx, [02089378]`. The type exists, but its route `ARRAY 0x02089378 stride=0x170 index=setIndex` has **no `count=`**, so `check_static_spans.spans_from` builds no span and the address resolves UNDECLARED. That is a precision on the expansion's "no static route": the fix is to add the count |
| S-31 | `licenceOwnedBits` `0208E680` (uint8[46]) | `002369A3 mov rcx, [0208E680]`; `002369B4 mov [0208E680], rbx`; 208 .text references across the 46 bytes (the expansion's 90 counts the base address alone) |
| S-36 | global tick `[0208F570]` in `CONTRACT-widget-object.md` | `0022819C mov [0208F570], eax`; `00228738 mov eax, [0208F570]`; 188 references. The router state from this lane's sample (S-36 D2: `0215F1A0..0215F1AB`, `020927D8`) is also still undeclared |
| S-39 | handshake word `dword[02EBA3F8]` (State, I-10) | `0022A850` and `0022A856` load it; 67 references |
| S-45 | achievement-manager pointer cell `01F83450` | `0020CD3D cmp qword [01F83450], 0`; `0020CD71 mov [01F83450], rax`; 10 references |

**How each item was checked:**
- **Resolver:** every address goes through the census's own resolver (`resolve_addrs.py` in [`auditsem-l2-sample-1003`](../auditsem-l2-sample-1003/README.md)), and all of them return **UNDECLARED**. `02089340` resolves to the one-dword `RuntimeFlags02089340`, so the S-14 table at `+0x4014` is not covered by it.
- **Instruction text:** taken from [`sites.py`](sites.py) (this directory), which decodes each site from its listed function's start.
- **Reference totals:** come from `rawrefs.py` in [`auditsem-s49-rereview-1003`](../auditsem-s49-rereview-1003/README.md), a whole-`.text` scan for rip-relative, image-base-relative and abs64 references.
  - That scan's own R/W labels are not used here. It decodes backwards from the displacement, and a misaligned start can mislabel a read: for `01EF93FC` it reports 153 `adc` "writes" that are such artefacts. Only its totals and the function-aligned sites above are cited.

**The expansion census reproduces at HEAD.** A scratch copy of `types_census2.py`, run with only `HERE`/`DB` repointed so that nothing is written into AUDIT-SPEC's package, gives:
- selftest 7/7 PASS;
- 496 rows: FIELD 318, PTR-CELL 23, UNATTRIBUTED 134, UNDECLARED 13, UNTYPED 3, AMBIGUOUS-DEREF 1, RANGE-START 1, RANGE-END 3.
- The systems with UNDECLARED/UNTYPED rows are S-09, S-10, S-14, S-16, S-17, S-22, S-25, S-28, S-31, S-36, S-39 and S-45. These are identical to the published run.

**Decisions taken here:**
- **S-10 is not ruled a constant.** The expansion offered the scorer a CONSTANT ruling for `01EF93FC`, but the cell has two writers (above), so it is state. S-10 is PARTIAL until the cell is declared, which is a one-dword declaration on the S-46 precedent.
- **S-25 counts.** A declared type whose instance array has no measured extent does not meet "a declared type with a measured extent".
- **S-28 is not re-scored here.** `02097D20` (camera context 0) is also UNDECLARED. S-28's types cell was scored by this lane on 2026-09-25, but the request does not list it and the row is already NOT MET (runtime, `78b17b620`). It is noted for the same declaration batch.
- **The binding-gap cells of the eleven rows are not edited.** The types and L2 cells carry the reason. The gap cells' "none" is now stale, and their next owner should update them.

## SWE2-AUDIT-SEM correction record

- affected: `_index/L2-VERDICTS.md` — rows S-09, S-10, S-14, S-16, S-17, S-22, S-25, S-31, S-36, S-39, S-45. In each, the types cell goes MET → PARTIAL and the L2 cell MET → NOT MET, with each prior cell kept struck.
- consumers:
  - **`goal_gate.py`** (verdicts family) reads the L2 cell and agrees: 15/52 NOT MET.
  - **`cells.py`** (`auditsem-l2-sample-1003`) agrees: all eleven rows lead `PARTIAL` in types and `NOT MET` in L2.
  - **`PROGRESS.md` and the dashboard** regenerate from the file through `progress_report.py`.
  - **`census2_dispositions.tsv`**, the AUDIT-SPEC source, agrees: every "types PARTIAL" consequence it names for these rows is now applied.
  - **Restoration** is routed to OPUS, `AUDITSPEC-REQ-OPUS-L2EXP-REPAIRS-1003`: each cell returns to MET with the declaration commit named.
- run verified at commit 31333da6c:
  - `types_census2.py` (scratch copy): selftest 7/7, 496 rows, the system list above;
  - [`sites.py`](sites.py): all 19 cited sites decode as quoted;
  - `goal_gate.check_verdicts`: `(False, '15/52 systems NOT MET (first: S-02)')`.

## SWE2-AUDIT-SEM limits

- No declaration is made here; they are OPUS's.
- No cell other than the requested eleven types cells and their L2 cells is touched.
- The S-25 instance count, i.e. how many order sets live at `02089378`, is not derived here. It is the declaration owner's to measure.

## SWE2-AUDIT-SEM note added 2026-10-03: what commit b7a084d4a carries, plus follow-up edits

**Commit `b7a084d4a` also carries SWE2-DATA's edits to eleven rows of `_index/L2-VERDICTS.md`:**
- **runtime cells re-worded with named coverage:** S-06, S-08, S-11, S-18, S-22, S-26, S-30, S-31, S-32, S-34;
- **S-46:** runtime MET → MIXED and L2 MET → NOT MET.

On S-22 and S-31, DATA's runtime re-wording sits beside this lane's types and L2 re-score of the same rows.

**How they got into this commit:** they are SWE2-DATA's work under `AUDITSPEC-REQ-SWE2-DATA-L2EXP-REPAIRS-1003`. They were in the shared worktree when this lane published, and `publish_paths.sh` commits a named path's whole working-tree state. They are SWE2-DATA's content, not this lane's re-score. SWE2-DATA's record (`4207b4a16`) names `b7a084d4a` as their carrier.

A cell-by-cell diff of `b7a084d4a^` against `b7a084d4a` lists exactly these rows:
- this lane's types and L2 cells on the eleven re-scored rows;
- DATA's runtime cells on the eleven rows above, and DATA's L2 cell on S-46.

**The "15/52 NOT MET" figure above predates the S-46 edit.** From `b7a084d4a` on, `goal_gate.check_verdicts` reads `(False, '16/52 systems NOT MET (first: S-02)')`.

**Follow-up edits in this publish** (on the coordinator's request, applied to a clean `L2-VERDICTS.md` at `1e18553b0`):
- **binding-gap cells:** the gap cells of the eleven re-scored rows, and of S-28, now name the undeclared types item. The stale `none` and `types MET (2026-09-25 census sweep)` / `types MET` fragments are struck in place, and the rest of each gap cell is kept.
- **S-28 types cell:** MET → PARTIAL, with the old text struck. `CONTRACT-party-focus-and-control-suppression.md` names camera context 0, `0025A6BE lea rax, [02097D20]` (re-decoded by [`sites.py`](sites.py)), and `02097D20` resolves UNDECLARED. S-28's L2 cell was already NOT MET on its runtime cell (`78b17b620`) and is unchanged.

- affected: `_index/L2-VERDICTS.md` — the binding-gap cells of S-09, S-10, S-14, S-16, S-17, S-22, S-25, S-28, S-31, S-36, S-39, S-45, and S-28's types cell.
- consumers: `goal_gate.py` agrees, reading 16/52 NOT MET with no change from this edit. `cells.py` parses all 52 rows.
- run verified at commit 1e18553b0: [`sites.py`](sites.py) `0025A6BE` decodes as `lea rax, [rip + 0x1e3d65b] -> 02097D20`; `goal_gate.check_verdicts` reads `(False, '16/52 systems NOT MET (first: S-02)')`.
