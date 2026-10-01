# Update 09 — original owner request production and terminal queue behavior

**Apply after Updates 01–08**, on the uploaded `FFXII TZA(20260922-211246).zip` base.
Date: 2026-09-23. Local production completed and validated; formal independent acceptance pending.

## Copy-and-merge installation

1. Back up the six existing files listed below, or back up your database folder.
2. Extract `FFXII_TZA_UPDATE_09_Owner_Request_Production.zip` to a temporary directory.
3. Copy its **FFXII TZA** folder into the parent directory that already contains your existing
   **FFXII TZA** folder. Merge the folders and replace the matching files.

Do not delete the existing database or create an extra FFXII TZA folder inside it. Only changed
and new files are in this ZIP. No game image, unchanged database payload, Ghidra project,
reconstruction source, dependencies, compiled binaries or Git directory is included.

A newer local edit to any replacement is a real merge conflict, not permission to overwrite it.
The patch manifest contains exact before/after hashes. The complete TSV files are included for
ordinary file replacement, but only IndexedExternalSourceRequest's rows change; every unrelated
line remains byte-identical. Its one type stays one; its nine fields become ten.

## Six replacements

```text
FFXII TZA/
├── 02-Resource-And-Asset-Pipeline/
│   ├── CONTRACT-resource-input-ownership.md
│   ├── CONTRACT-resource-request-queue.md
│   └── the-external-source-owner-and-borrowed-view-lifetime.md
├── _types/
│   ├── types.tsv
│   └── fields.tsv
└── _index/_inbox/
    └── EXTERNAL-CONTINUATION.md
```

A new mechanism page is at
`02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md`.
All reproduction, findings, hashes and checks are under
`_experiments/evidence/continuation-section09-owner-producer/`.

## No user commands required

An agent may optionally run the read-only checker from the evidence directory:

```sh
python verify_overlay.py --target '/path/to/FFXII TZA'
```

It accepts exact expected preimages, already-applied output and absent new files. It refuses
newer conflicting bytes and unsafe paths. It does not install, delete, change claims or alter
Git. Its manifest excludes its own hash to avoid a circular self-hash.

## What became established

Original arming/state2, full producer selection/allocation, provider index/length/offset rules,
preferred arena11 versus arena6 fallback, pin/class separation, held-state1 behavior, explicit
rearm after state0 failure, real handle-capacity failures and terminal pump/owner composition.
A queue slot retiring after positive error or cancellation does not notify this owner; source
handle equality is not unique request identity. Real IO and outer recovery remain open.

[Technical review and exact fixture scope](REVIEW.md) distinguish synthetic status from live
completion and local production from independent acceptance. No global scores, L2 verdicts,
TEAM tasks, historical experiments or reconstruction implementation are changed.

## Reproduction

On Linux x86-64 with Python3.10+ and GCC:

```sh
python run_review.py --exe /absolute/path/FFXII_TZA.exe --output /absolute/path/new-results
```

The authorized EXE is required; nothing is downloaded. Binaries are temporary. The native
fixture requires only Python's standard library and GCC; the separate optional content checker
requires PyYAML. This is not Windows/game deployment or a live IO test.

[File manifest](PATCH_MANIFEST.json), [canonical changes](canonical_changes.diff),
[validation summary](results/summary.json), [delivery check](results/delivery_validation.json).
