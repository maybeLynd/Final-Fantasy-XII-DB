# Final Fantasy XII: The Zodiac Age — knowledge database (read-only snapshot)

This repository is a **text-only snapshot** of the FF12 TZA engine knowledge database. The database is authored in the
working checkout (`XIIOnline/Database`) by the fixed team identities (OPUS, FABLE, ASTRA and the SWE2 lanes). It is
mirrored here for backup and for cloud sessions. **Do not author database changes here.** Refresh it with
`python tools/sync_from_xiionline.py --apply` on the workstation, then commit and push.

## What is here

- `FFXII TZA/`: the database. It holds:
  - the topic pages (`00-…` to `99-…`);
  - the register of questions (`_index/OPEN-QUESTIONS.md`);
  - candidate records with their checkers and outputs (`_index/candidates/`);
  - types (`_types/`);
  - experiment records (`_experiments/`).
- `Tools/`: the analysis kit (`analysis-kit/gfz-scripts`), the dashboard code, and docs.

## What is deliberately NOT here

- **No game data or binaries.** This covers the shipping executable, the extracted archive, images, `.bin` / `.fst` /
  `.ebp` / `.phyre` / `.vbf` / `.st2e` and other extracted formats, archives, objects and compiled bytecode. The sync
  script admits text types only and refuses any file containing a NUL byte.
- `Tools/work/` (the local game executable, the extracted data and scratch), the generated `knowledge.sqlite`, and the
  live team board `_index/_inbox/TEAM.json`.

So most checkers here **cannot be re-run in a cloud session**: they read `Tools/work/exe/FFXII_TZA.exe` or the
extracted archive, which exist only on the workstation. Cloud work on this repo must be self-contained, such as
reading, cross-checking pages against each other, tooling and documentation.

## Cloud sessions are temporary (user, 2026-10-01)

The account has $250 of Claude Code cloud-session credit, which expires on 2026-11-05. Use cloud agents to the best of
their capability while the credit lasts. Once it is used up or expired, cloud agents are no longer used or relied on.
No milestone, workflow or gate may depend on them.

## Authority

Source beats prose: the shipping EXE (sha256 `73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`) is
the native authority. The evidence policy is `FFXII TZA/_index/EVIDENCE-POLICY.md`.
