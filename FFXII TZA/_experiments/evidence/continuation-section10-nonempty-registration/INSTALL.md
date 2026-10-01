# Update10 — Nonempty PRF Registration

Apply AFTER Updates01–09 to `FFXII TZA(20260922-211246).zip`.

Extract the ZIP. Copy its `FFXII TZA` folder into the parent directory containing your existing
`FFXII TZA` folder. Merge folders and replace matching files. Do not delete the existing database,
and do not put one FFXII TZA folder inside the other. Only changed/new files are supplied.
Back up affected files first. Any newer local edits require a merge rather than blind replacement.

Six existing Markdown files change; one new mechanism and bounded evidence are added. No type
stores, TEAM/L2/global metrics, reconstruction, historical raw data or previous update evidence are
replaced. No EXE, Ghidra project, dependency wheels, compiled binaries or Git directory is included.
`PATCH_MANIFEST.json` records exact preimages/new hashes (except its own circular self-hash).

The optional read-only preflight takes the actual existing database folder:

```sh
python verify_overlay.py --target '/path/to/FFXII TZA'
```

No user command is necessary for ordinary copy-and-merge installation. Local production and
validation are complete; formal independent peer acceptance remains pending. See REVIEW.md for
original-instruction evidence, substitutions, synthetic-state limits and remaining work.
