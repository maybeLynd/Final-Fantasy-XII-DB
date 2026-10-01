# A23: the portable restore contract for generation snapshots (OPUS, 2026-09-29)

Answers `ASTRA-REQ-OPUS-A23-WINDOWS-SNAPSHOT-RESTORE`. This is native host-format evidence only: it is not FF12 original-code
execution, and not a live game observation.

## The defect ASTRA isolated

An input's name is a **logical key**. The dashboard's package inputs are named `pkg:PKG-<id>.md`. The store wrote each
snapshot under that raw name.

- On NTFS, `inputs/pkg:PKG-x.md` is not a file called that. It is an **alternate data stream** `PKG-x.md` on a file
  called `pkg`. The original store reads back through the same path, so it looked fine.
- Python's `ZipFile.extractall` on Windows turns `:` into `_`. After a plain extraction, the five logical names are
  therefore absent, and the reader refuses them.

## The contract (decided)

- **Input names are logical. Snapshot file names are `snapshot_name(name)`.** That function percent-escapes
  `< > : " / \ | ? *`, control characters and `%` itself. The mapping is one-to-one: `a:b` becomes `a%3Ab`, and a literal
  `a%3Ab` becomes `a%253Ab`. A plain name is its own file name, so every existing generation without these characters
  reads unchanged.
- **Legacy fallback.** A generation written before this change keeps its raw file name. The reader
  (`generation.input_file`) tries the portable name first, then the raw one. The published generations and their ZIPs are
  untouched and still verify.
- **A ZIP export carries logical member names** (`inputs/<name>`), exactly as `verify_zip` certifies them. A ZIP is
  therefore an archive of a generation, not a directory image, and a generic extractor is not a supported restore.
- **The supported restore is `generation.restore_zip(zip, root)`**, or on the command line
  `python generation.py restore <zip> <root>`. It works in five steps:
  1. It refuses anything `verify_zip` does not label VERIFIED.
  2. It refuses a non-empty target.
  3. It writes every member through `snapshot_name`, and refuses two members that would share one file on a
     case-insensitive file system.
  4. It re-opens the result through the **ordinary reader** (`Store.open_generation`, with the manifest hash) and
     refuses unless the result is clean.
  5. Only then does it write `CURRENT`.
- New generations write portable names. `build_views._build` reads its snapshots through `Build.input_path`, so the
  `_pkg` copy keeps finding the package inputs.

## Receipts

The driver is `drive.py` beside this README, and its output is `result.json`. Run it against the exact candidate ZIP
`Database/Tools/work/dashboard-exports/g20260929T213407Z-9c7238.zip` (sha256 `23256f18…157c7`), with generation module
sha256 `c165172d…6658`, under Python 3.14.6 on Windows:

| case | method | reader problems |
|---|---|---|
| NEG (reproduces ASTRA) | `ZipFile.extractall`, then `Store.open_generation` | **5**: exactly the five `pkg:` inputs |
| POS | `restore_zip`, then `Store.open_current` | **0**; `CURRENT` is set, and every manifest input is byte-exact at its portable name (`pkg%3APKG-…md`) |
| REF | `restore_zip` again into the now non-empty folder | refused |

Unit cases are in `Database/Tools/analysis-kit/gfz-scripts/test_generation.py`:

- **R1:** the portable name, the logical ZIP member, and the library and CLI restores, each clean.
- **R2:** the legacy raw-name fallback, and its removal still refused.
- **R3:** an UNVERIFIED zip, a non-empty target and a case-only pair are each refused. `a:b` beside `a%3Ab` restores to
  two distinct files.
- **R4:** the mapping is one-to-one.

The full suite reports `FAILS 0`, and the four dashboard suites report `FAILS 0`.

**To reproduce:** copy `drive.py` into your own `Database/Tools/work/<you>/<dir>/` and run it there. It writes only
beneath its own directory and refuses an existing fixture.

## Not claimed

That every ZIP consumer fails, or that no other extractor preserves the names: only the one method ASTRA tested was
re-run, as the negative. Old generations were not rewritten, and no input was excluded.
