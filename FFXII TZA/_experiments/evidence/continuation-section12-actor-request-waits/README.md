# Update12 — actor request arming and waits

This is a changed-files-only overlay, not a full database or game mod binary.

## Apply

1. Use the September23 20:56:05 FFXII TZA database with Update11 already merged.
2. Back up matching files. Preserve newer Devin/peer edits by merging them rather than overwriting.
3. Extract the ZIP and copy its **FFXII TZA** folder into the PARENT directory containing your
   existing **FFXII TZA** folder. Merge folders and replace the listed files.
4. Do not delete the existing database or place an FFXII TZA folder inside itself.

No command is required. The optional `verify_overlay.py --target '/path/to/FFXII TZA'` only reads
and reports preimage/already-installed/conflicting files. It never applies changes.

Nine existing files are replaced; only two type rows and nine field rows are changed in the full
TSV replacements. New mechanism/evidence files preserve their nested locations. No game image,
compiled binary, dependencies, Ghidra project, Git directory or unchanged database file is included.

[Detailed research and limits](REVIEW.md). Local production is validated; formal independent
acceptance remains pending. No TEAM/L2/global completion or reconstruction source is changed.
