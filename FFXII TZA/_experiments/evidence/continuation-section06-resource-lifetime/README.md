# Update06 — Resource Ownership and Lifetime

Changed-files-only overlay for `FFXII TZA(20260922-211246).zip` plus Updates01–05.

Extract the ZIP and merge its **FFXII TZA** folder into the parent directory containing your existing
**FFXII TZA** folder. Replace only matching files; do not delete the old directory or nest one copy
inside another. Back up touched files. Newer local edits need an actual merge.

The complete type/field TSVs are included because they are the files being replaced. Only three
named types and their targeted fields change. No executable, Ghidra project, dependencies, compiled
binaries, unchanged database files, Git directory or reconstruction files are included.

[Technical review](REVIEW.md) records original-code controls and limitations. [Manifest](PATCH_MANIFEST.json)
records exact preimage/output hashes (excluding its own self-hash). [Preflight](verify_overlay.py)
is optional and read-only. No user command is required for ordinary merge installation.

Local production complete; formal independent acceptance pending. TEAM and global acceptance are
not altered. Repeatable isolated execution does not establish fresh live-game lifetime behavior.
