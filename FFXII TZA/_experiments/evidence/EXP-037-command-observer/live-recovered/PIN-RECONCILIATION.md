# Pin reconciliation — EXP-037 runtime_probe.py

SWE2-ORACLE, 2026-09-15, for `ASTRA-REQ-ORACLE-COMMAND-OBSERVER-PIN`.

## Question

EXP-037's `dependencies.json` pins `runtime_probe.py` at
`f82b0c6a26b4cc0416fbb19f35754a5f9fc1b679ab36271adb0a4f6fc9a9700f`; the file on
disk is `83775bcc6263035830489b40cc1083273085476b17a3b405c378e851d40a1172`.
Is the drift semantically safe to repin, or does the imported behavior differ?

## Finding: the drift never reaches the imported surface

Exact old source identified: the pin matches commit `797828d6`
(2026-09-08, "runtime: ET-1 built"). Two commits separate it from current:

- `ce1a28dc` — usage-docstring fix only ("--at takes an actual object
  address"); no code change.
- `bb26093c` — adds `check_value()`, `CHECK_FORMATS`, `import math`, and
  rewires the `--check` TSV path to strict numeric comparison with header
  validation, error counting, and nonzero exit on zero rows.

`observe.py` imports `runtime_probe` inside `main()` and uses exactly four
symbols: `find_process`, `module_base`, `CONTROL_ADDR`, `CONTROL_BYTES`.
`git diff 797828d6 bb26093c` touches four hunks only — the usage docstring,
the import block, the new `check_value` helper, and the `--check` branch of
`main()`. None of the four imported symbols appears in any hunk; their text
is byte-identical (only line numbers shifted). The `--check` path runs only
under `runtime_probe.main()`, which `observe.py` never invokes.

**Disposition: repin justified.** The pin was cosmetically stale, not
semantically. The strictness improvement to `--check` is a benefit the
candidate inherits for free, not a behavioral risk.

## Candidate

`live-recovered/` holds the resumed candidate. Changes vs. the historical
EXP-037 sources are minimal and mechanical — the directory is one level
deeper, so:

- `KIT = HERE.parents[3]` → `parents[4]`
- `board_path = HERE.parents[2]` → `parents[3]`
- sibling experiment sys.path entries: `HERE.parent` → `HERE.parent.parent`
- `dependencies.json`: every relative name gains one `../`;
  `runtime_probe.py` repinned to `83775bcc`; the other nine pins verified
  still matching current files (all `MATCH`).

Historical EXP-037 `observe.py`, `test_observe.py`, `dependencies.json` are
untouched in place.

## Controls run

`python test_observe.py` in `live-recovered/`: **11/11 pass**, including
`test_pinned_dependencies_and_source_receipts` (verifies the new
dependencies.json hashes from the deeper location against live files) and
the real-disk-bytes qualification positive against the actual shipping EXE
at `D:\SteamLibrary\...\FFXII_TZA.exe`. All five corrected paths verified to
resolve on disk.

## Limits

- No live run performed — the candidate is an offline-verified preparation,
  same as the original EXP-037.
- The repin argument is a diff-scope argument: it proves the four imported
  symbols are unchanged, not that every future edit is safe. Any further
  `runtime_probe.py` drift requires re-running this reconciliation.
- `runtime_input_probe.py`, `runtime_poke.py`, `window_focus.py` pins still
  match but are imported nowhere in `observe.py`; they are pinned for the
  record only.
