# Update 05 — encoded-ID registry and query mechanism

**Apply after Updates01,02,03,04 to `FFXII TZA(20260922-211246).zip`.**
This archive is a changed-files overlay, not a replacement for the complete database.

## Copy-and-merge installation

Back up the matching files. Extract the ZIP and copy its `FFXII TZA` folder into the parent directory
that already contains the existing `FFXII TZA` folder. Merge folders and replace the matching files.
Do not delete the existing database and do not put one `FFXII TZA` folder inside another.

Seven existing files are replaced:

```text
FFXII TZA/
  00-Engine-Core-Runtime/
    CONTRACT-encoded-id-space-and-class-registry.md
    the-encoded-id-space-and-the-query-record.md
    the-encoded-id-class-registry.md
  _types/types.tsv
  _types/fields.tsv
  _experiments/EXP-143-s04-validator-all-arms-exec.md
  _index/_inbox/EXTERNAL-CONTINUATION.md
```

The new mechanism page is `00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md`.
Supporting evidence is nested in `_experiments/evidence/continuation-section05-encoded-query/`.
Only the two specified type rows and their field rows change; whole TSV files are included for normal
file replacement. All unrelated TSV lines remain byte-identical. No unchanged database files, EXE,
Ghidra project, dependencies, compiled binaries, Git directory or older raw evidence are shipped.

Any edits made locally after the baseline/Update04 to these same files need merging, not blind
replacement. The optional verifier checks expected preimages and already-applied outputs without
writing files. It verifies byte identity, not the correctness of a research claim:

```sh
python verify_overlay.py --target '/path/to/existing/FFXII TZA'
```

No command is needed for ordinary installation.

## What changes

The contract and pages now specify registry rebase/reset, class-selected input, original validation,
tagged partial outputs, static-buffer reuse and failure clearing. The section resolves the known
class12/EFFE/nibble errors and adds meaningful behavior: equipment bit54's actual masked writer,
class10's strided tail, auxiliary text pointer08, conditional action/licence fields, distinct
inventory-query shapes, three key-item intervals versus four-descriptor validity, and pointer-width
and availability boundaries.

## Evidence and limits

200 original-instruction assertions, identical repeat, seven intended code-mutant refusals;19
selected body hashes and9 data spans verified. The original application callees are not replaced;
only imported memset is bridged. Data/state are synthetic. The null-row faults occur in disposable
children, not FF12. Retained EXP-143 review checks246 traced records plus4 summary-only returns,
with8 negative controls. It does not rerun the historical emulator campaign.

This is completed LOCAL PRODUCTION, with formal independent acceptance pending. It does not declare
S04 or the database complete. TEAM, global metrics, L2 verdicts and reconstruction remain unchanged.

See [REVIEW.md](REVIEW.md), [claim map](claim_matrix.tsv), [summary](results/summary.json),
[manifest](PATCH_MANIFEST.json) and [current handoff](../../../_index/_inbox/EXTERNAL-CONTINUATION.md).
The handoff link is relative to the evidence directory only; canonical path is
`FFXII TZA/_index/_inbox/EXTERNAL-CONTINUATION.md`.
