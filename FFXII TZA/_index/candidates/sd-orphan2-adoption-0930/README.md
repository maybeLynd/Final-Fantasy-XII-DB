# Second orphaned SD restatement set adopted (SWE2-DATA, 2026-09-30)

affected: _index/OPEN-QUESTIONS.md (rows SD-41, SD-120, SD-140, SD-160, SD-162, SD-165, SD-180, SD-181, SD-190, SD-192), 06-Movement-And-Navigation/clamping-a-point-into-a-volume.md, 06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md, 99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md, 17-Presentation-Rendering/Effect-File-Formats/effect-mesh-records-kind-54.md

run: at 3dac81ee9: orphan2_check.py over the ten adopted rows, FAILS 0 (the .out beside it). For each row it
confirms four things:
- the cited record folders (or the cited review) are tracked at HEAD;
- the cited commits are ancestors of HEAD;
- every script in the record re-runs with FAILS 0;
- every backticked token of the new status appears in the record, the cited commits, or an audit review that names
  the id.

Control C1: an invented token is not found.

**Origin.** The worktree register held uncommitted SD-section restatements of 15 rows, written around 13:28 local. No
board claim covered them, and FABLE confirmed they are not its. SWE2-DATA owns the SD section and adopts them here.
The pre-adoption register is saved in SWE2-DATA's work folder as `oq_orphan2.save`.

| rows | disposition |
|---|---|
| SD-41 (OUT OF EVIDENCE BOUNDARY; SWE2-AUDIT-SPEC review ACCEPT), SD-120, SD-140, SD-162 (SWE2-ORACLE records), SD-165 (OPUS census, merged question), SD-180, SD-192 (ANSWERED), SD-181, SD-190 (PARTIAL, narrowed on the batch-5 review) | adopted as written; all verified |
| SD-160 | the orphan's question cell is adopted ("one of the four defeat-tally gates", per the batch-4 review C8); HEAD's status is kept (`b1ebce335` carries C8) |
| SD-161, SD-163, SD-164, SD-166, SD-167 | HEAD kept: `b1ebce335` is newer. The orphan's SD-161 still read OPEN, and its SD-166 C6 text is already in HEAD |

**Pages.** The boxes for SD-180, SD-192 and SD-120 are ticked with a dated note linking the record. The orphan's
edit to the kind-0x54 effect-mesh page (SD-140 ticked with SWE2-ORACLE's answer) is adopted with the row. Two other
uncommitted page edits from the same window are not adopted, and are routed-to-OPUS: `save-image-buffers-header-and-payload`
and `version-stamps-and-what-loading-normalises` each raise their status word to DOCUMENTED as an "owner re-status
(OPUS)", which is OPUS's role, not SWE2-DATA's.

## Consumer check

| consumer | disposition |
|---|---|
| OPEN-QUESTIONS rows listed above | revised-here |
| the four pages named in `affected:` | revised-here (boxes follow the rows) |
| the two save pages with a pending status re-status | routed-to-OPUS |
