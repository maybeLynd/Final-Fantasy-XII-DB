# FF12 updated-files overlay 02 — Resource request queue

Apply **after Update01** to the database supplied as `FFXII TZA(20260922-211246).zip`.
This is a delta overlay, not a complete database and not a replacement game.

## Copy-and-merge installation

Extract the delivered ZIP to a temporary folder. Copy its **FFXII TZA** folder into the directory
that already contains your **FFXII TZA** folder. Merge directories and replace matching files.
Do not delete the existing folder or put one FFXII TZA folder inside another.

Only seven existing files are replaced; new review, reproduction and handoff evidence is added
under its nested evidence path. Unchanged project files, EXE/GZF, dependencies, compiled programs,
Git history and raw historical experiment inputs are omitted.

Keep a backup. If one of these files has newer local edits, merge it instead of blindly replacing
it. `PATCH_MANIFEST.json` records before/after hashes, including the Update01 handoff preimage.
The optional `verify_overlay.py --target <FFXII TZA folder>` is read-only and distinguishes expected
preimage, already applied, new file and conflict. Commands are not required to copy this update.

See [REVIEW.md](REVIEW.md) for established findings, evidence limits and remaining work, and
[results/summary.json](results/summary.json) for actual executed checks. This is completed local
production; peer acceptance and full L1+L2 database completion are not claimed.
