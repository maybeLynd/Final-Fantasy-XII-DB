# Update 04 — widget receiver identity and resource lifecycle

Production date: 2026-09-22. Local validation completed; formal independent acceptance is pending.

## Installation — ordinary folder merge, no commands required

Apply this update to `FFXII TZA(20260922-211246).zip` **after Updates 01, 02 and 03, in that order**.
The overlay contains only new or changed files under the root `FFXII TZA/`. Unchanged files and
directories are intentionally absent.

1. Back up the affected existing files or your database folder.
2. Extract `FFXII_TZA_UPDATE_04_Widget_Receiver_Identity.zip` into a temporary folder.
3. Copy the extracted **FFXII TZA** folder into the parent directory that already contains your
   existing **FFXII TZA** folder. Merge folders and replace matching files.

Do not delete the existing database first. Do not put one `FFXII TZA` folder inside the other.
If other agents or local edits changed any of the affected files after Update 03, merge those
changes rather than blindly overwriting them. Before/after hashes in the manifest identify the
exact expected inputs and delivered replacements.

## Existing files replaced

```text
FFXII TZA/
├── _types/
│   ├── types.tsv
│   └── fields.tsv
├── 16-UI/Widget-Object-Model/
│   ├── CONTRACT-widget-object.md
│   └── the-widget-constructor-and-object-sizes.md
└── _index/_inbox/
    └── EXTERNAL-CONTINUATION.md
```

Only the `WidgetSingleton02AEE4C0` row changes in `types.tsv`. Only that type's field rows change
in `fields.tsv` (25 old rows become 23 corrected rows). Every unrelated TSV line is byte-identical.
The whole TSV files are delivered because a folder merge replaces files, not individual rows.

A new mechanism page, `the-title-asset-singleton-and-its-distinct-consumer.md`, is added beside the
widget contract. The remaining additions are this section's evidence, validation code, results,
exact differences and installation metadata in the present evidence directory.

No original executable, Ghidra project, external dependency, compiled binary, Git metadata or
unchanged database file is bundled. Historical raw experiments, TEAM claims, L2 verdicts, global
completion dashboards and reconstruction source are unchanged. No deletions are required.

## Optional agent-side conflict check

The read-only standard-library checker compares this overlay with a target database. It does not
write to the target, launch the game, install dependencies or apply changes:

```sh
python verify_overlay.py --target "/absolute/path/FFXII TZA"
```

Run it from this extracted evidence directory or supply the script's complete path. Expected
preimages, already-applied replacements and absent new files are accepted; differing local content,
missing required old files, directory collisions and unsafe relative paths are refused.
This check is optional; no user command is needed for ordinary copy-and-merge installation.

The manifest excludes its own digest to avoid recursive hashing. The complete ZIP has an external
SHA-256 published with the download.

## What changed and how it was validated

See [the technical review](REVIEW.md) for original-code anchors and test boundaries. The section
separates message accesses and arithmetic from widget fields, restores the actual +0xC8 resource
pointer, records publication/readiness/teardown behavior, and corrects the raw initializer's return
contract. It does not claim full UI/resource semantics or peer acceptance.

[The reproduction driver](run_review.py) needs the exact original EXE, Linux x86-64, GCC, Python
3.10+ and the pinned Capstone distribution in [requirements.txt](requirements.txt). Dependencies
and the EXE must already be available. Nothing is downloaded. The fixture uses explicitly listed
synthetic service boundaries; it is not a Windows game-session test.

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-empty-results
```

[Patch manifest](PATCH_MANIFEST.json) · [canonical changes](canonical_changes.diff) ·
[run summary](results/summary.json) · [content validation](results/content_validation.json)
