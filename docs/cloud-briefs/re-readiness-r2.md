# Brief: reconstruction-readiness pass 2 (stream R2)

You are a cloud session working for FABLE (the database's semantic lane) on the FF12 TZA knowledge database (this
private repo, a text-only snapshot synced from the authoring repo). Read `docs/CLOUD_PROGRAM.md` and
`docs/cloud-briefs/re-readiness.md` (pass 1's brief: its Interface / Gaps / Rating method still applies) first.

## Why

The database is complete when the game's engine and logic could be re-implemented from it alone. Pass 1 (2026-10-01
and 10-02, `cloud-reports/re-readiness/<system>.md`) listed, per system, what a re-implementer would still be missing.
Since then hundreds of pages changed: gaps were answered, contracts were written, register rows were closed. Pass 2
says where each system stands NOW, so the remaining work is a short, exact list.

## The task (one system folder, named in your launch message)

### A. If pass 1 mapped this system (`cloud-reports/re-readiness/<slug>.md` exists)

1. Read pass 1's **Gaps** section (2.1, 2.2, 2.3 or however it is organised) and its **Rating**.
2. For EVERY pass-1 gap, decide against the CURRENT pages (and `FFXII TZA/_index/OPEN-QUESTIONS.md`):
   - **CLOSED**: the information is now stated. Quote it and cite `page:line` (and the register row id and status
     cell if a row answers it).
   - **NARROWED**: part of it is now stated; say exactly what is still missing.
   - **OPEN**: still missing. Re-cite where the gap shows.
   - **WRONG-IN-PASS-1**: pass 1 was mistaken (the information was already there, or the gap misread a page). Cite.
3. Read the system's pages again for NEW gaps pass 1 missed (same criteria as pass 1: an undocumented field a
   documented function writes; a callee named but not described; a state with no stated initial value; a formula
   given only for some inputs; two pages that disagree). Cite each.
4. Re-rate the system: READY / MOSTLY / NOT YET, with one paragraph on what decides it.

### B. If pass 1 did not map this system

Do pass 1's full task (Interface, Gaps, Rating) per `docs/cloud-briefs/re-readiness.md`.

## Rules

- **Quote and cite; do not invent behaviour.** Every CLOSED needs the quoted sentence and `page:line`. Where the
  database is silent, say "not stated". Do not write code.
- **Register first.** A gap that a register row (`_index/OPEN-QUESTIONS.md`) already tracks: give the row id and its
  state (OPEN / PARTIAL / ANSWERED / WITHDRAWN). Runtime-only rows are tracked elsewhere; just label them RUNTIME.
- **Be exact about what is missing**: "the initial value of dword `02B40E18` is not stated" beats "state is unclear".
- **Classify each OPEN or NEW gap** as one of: STATIC (answerable from the executable or data by a desk read),
  RUNTIME (needs a live observation), DATA (needs a census of shipped game data), or DOC (the answer exists on another
  page; this page only lacks the pointer). This is what FABLE routes by.
- Pages are long. Read the status lines, the "What is not known" / "Unresolved" / "Open" sections, the CONTRACT pages,
  and every section a pass-1 gap cites. Use `grep` liberally.

## Output

Write `cloud-reports/re-readiness-r2/<slug>.md` (the slug in your launch message) with sections:
1. **Summary**: counts of pass-1 gaps CLOSED / NARROWED / OPEN / WRONG-IN-PASS-1; count of NEW gaps by class; the
   new rating and the old one.
2. **Pass-1 gaps**: a table, one row per pass-1 gap: id or short name, verdict, evidence (quote + `page:line`), what
   is still missing.
3. **New gaps**: a table: gap, class, evidence (`page:line`), register row if any.
4. **Rating**.

(For a system pass 1 did not map: Interface, Gaps with the class column, Rating.)

## Git

1. Work on the branch the launch message names.
2. Commit and push after each section is written (a usage stop loses unpushed work).
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Edit nothing outside `cloud-reports/re-readiness-r2/`. Never push to `main`.
5. When done, open a pull request to `main` titled as the launch message says, with the summary counts in the body.
