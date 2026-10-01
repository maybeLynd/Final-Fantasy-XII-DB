# Update03 — retained reward bindings and reward consumers

Apply **after Update02 and Update01**, based on `FFXII TZA(20260922-211246).zip`.
The ZIP contains only changed/new files in their existing nested `FFXII TZA/` paths.

Extract the ZIP. Copy its `FFXII TZA` folder into the **parent directory that already contains your
existing `FFXII TZA` folder**. Merge the folders and replace matching files. Do not delete the
existing folder or nest one `FFXII TZA` folder inside the other. Back up the affected files first.
Newer local edits to the same files must be merged rather than blindly replaced.

No commands are required for ordinary copy-and-merge installation. An agent may optionally use
`verify_overlay.py --target '/path/FFXII TZA'` for a read-only conflict check before copying.
It compares exact preimages/new-file hashes; it does not accept scientific claims or modify files.

The updated contracts/pages correct NULL-recipient EXP division, the distinct LP gate/ownership
rules, the sentinel roster exception, the scope of retained reward bindings and the gil reporting
arithmetic. The evidence includes 24 original-body hashes, 88 retained spans, 71 native synthetic
controls, six rejected code variants and ten new corrupted-record controls. The historical checker
also reproduces its preserved output and four controls. Full live game and full old Unicorn
campaigns were not rerun. Peer acceptance remains pending.

The exact replaced/new files and before/after hashes are in `PATCH_MANIFEST.json`. It excludes its
own self-hash; the delivered ZIP has an external SHA-256. No unchanged DB file, EXE, Ghidra project,
compiled binary or dependency is included. TEAM/L2/global scores/reconstruction remain unchanged.

See [the detailed review](REVIEW.md) for every correction, controls, evidence limits and reproduction.
