# Brief: text-only audit pre-run (stream A)

You are a cloud session working for OPUS on the FF12 TZA knowledge database (this private repo, a text-only snapshot).
Read `docs/CLOUD_PROGRAM.md` first.

## Why

The database is accepted only after **30 consecutive clean passes** of its terminal audit. The full audit runs on the
workstation, where the game executable and extracted data exist. Many of its checkers need neither: they read only
the pages, the register and the TSV records. Your job is to run every such checker here and report what fails, so
the owners fix it before the real run.

## The task

1. **Python.** Use the sandbox's `python3`. Do not install packages beyond the standard library. If a checker imports
   something missing (for example `capstone`), record it as `NEEDS-PACKAGE <name>` and move on.
2. **Find the checkers.** Look in `Tools/analysis-kit/gfz-scripts/` for `check_*.py`, `audit_*.py`, `adrift_report.py`
   and `goal_gate.py`. For each, read the top docstring and its argument parsing, then run it the way it expects
   (most take `--db "FFXII TZA"` or default to the snapshot path; some have a `--self-test`).
3. **Classify each run.** Give each checker exactly one of these outcomes:
   - `CLEAN`;
   - `FINDINGS n`;
   - `NEEDS-EXE`: it reads `Tools/work/exe/FFXII_TZA.exe`, the extracted archive, or `knowledge.sqlite`;
   - `NEEDS-PACKAGE`;
   - `CRASH`: give the exception's last line.
   - Set a timeout of 10 minutes per checker.
4. **Report failures fully.**
   - For every checker with findings, list each finding with file and line, the quoted text, and the checker's own
     message.
   - Do not fix anything. Do not judge whether a finding is right: OPUS and the owners do that.
   - Group findings by the page's folder.

## Output

`cloud-reports/audit/2026-10-01-prerun.md`:
1. **A table first:** one row per checker, giving checker, outcome, count, seconds.
2. **Then the findings,** grouped by checker.
3. **At the end, the run's environment:** the Python version and the snapshot commit (`git log -1 --format=%h`).

## Git

1. Work on the branch `cloud/audit-prerun-1001`.
2. Commit and push after every 20 checkers.
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Edit nothing outside `cloud-reports/`.
5. Never push to `main`.
6. When done, open a pull request to `main` titled `cloud: text-only audit pre-run 2026-10-01`.
