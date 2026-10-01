# Brief: DD owner-read worksheets (stream D)

You are a cloud session working for OPUS on the FF12 TZA knowledge database (this private repo, a text-only snapshot).
Read `docs/CLOUD_PROGRAM.md` and `FFXII TZA/_index/EVIDENCE-POLICY.md` first.

## Why

A page can be re-statused from PARTIAL to DOCUMENTED only when nothing on it still reads as open where the question
register (`FFXII TZA/_index/OPEN-QUESTIONS.md`) is closed. Earlier owner reads did this by hand:
- a worked example: `FFXII TZA/_index/candidates/swe2contract-ddres-b20-1001/README.md` (its R1-R13 table);
- an applied re-status: `FFXII TZA/_index/candidates/opus-dd-restatus-24-1001/README.md`.

## The task

For each page named in the launch message:
1. **Find every sentence that reads as open.** Look for "not established", "unknown", "still open", "untested", "not
   yet", "pending", "unread", unticked `- [ ]` boxes, "TODO", and questions in the text. Ignore anything already
   struck through (`~~...~~`) or already followed by a dated "Answered ..." note.
2. **Classify each one:**
   - **STALE.** Already answered: on the page further down, in a register row (give the row id and its status cell),
     or on another page (give path and section). Propose the dated pointer sentence to add after it, in the page's
     style: *"(Answered YYYY-MM-DD on ..., see ...)"*.
   - **LIMIT.** A statement of the evidence's scope, not a question, for example "no live observation". Propose
     nothing; just mark it.
   - **ROW.** A genuine open question the text cannot settle. Propose an id-less register row: the question, the page
     and why it is open.
3. **Record the register state.** List every register id the page names, with its status cell as it reads now.

## Output

Write `cloud-reports/dd/<page-slug>.md`. Give one table per page with these columns:

| line | quoted text | class | where it is answered | proposed sentence |
|---|---|---|---|---|

Then add the register-id list.

Do not edit the page or the register. Quote exactly. Every "answered" claim must name its source with path and line
or row id. OPUS re-checks each one.

## Git

1. Work on the branch `cloud/dd-<first slug>`.
2. Commit and push after each page.
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Never push to `main`.
5. When done, open a pull request to `main` titled `cloud: DD worksheets for <slugs>`.
