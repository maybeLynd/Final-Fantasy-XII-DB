# Brief: cross-read of drafted rows (stream V)

You are a cloud session working for FABLE on the FF12 TZA knowledge database (this private repo, a text-only
snapshot). Another session drafted the rows you are given; you did not. Your job is to find what is wrong with them.
Read `docs/CLOUD_PROGRAM.md`, `docs/cloud-briefs/f-interior.md` (the rules every row must meet), then this brief, then
your pack(s) in `cloud-input/verify/`.

## The task

Each pack lists drafted rows. Each row is one function: a `DRAFT` sentence on what the body does, its `ANCHORS`
(interior instruction addresses with mnemonics), and the function's annotated listing. For every row, read the
listing yourself, then decide:

- **ACCEPT**: every clause is true of the listing, every path is stated, and each anchor is an instruction inside the
  body that does what a clause says.
- **CORRECT**: the row is fixable. Give the corrected `text` and `anchors`, both meeting the f-interior rules, and say
  in `why` what was wrong.
- **REJECT**: the row cannot be stated reliably from the listing. Say why.

## What to check, clause by clause

- Branch and guard coverage: a guard that skips the work, the value returned on each path, early exits.
- Direction and sign: `cmovg` vs `cmovl`, `ja`/`jb` (unsigned) vs `jg`/`jl` (signed), `sub a, b` order, `test`/`and`
  masks, shift directions and counts.
- Arguments: which register carries which argument (`rcx`, `rdx`, `r8`, `r9`, then stack), and argument order at
  each call.
- Widths and offsets: `byte`/`word`/`dword`/`qword`, the exact displacement, loop strides and bounds.
- Named addresses: every 8-hex address in the sentence appears in that function's listing; no jump-table or
  after-code data address; calls are cited by site (`<entry>` + 0xNN) unless the callee is in the same pack.
- Anchors: 1 to 5, strictly inside the body (never the entry), mnemonic exactly as printed, and each one does work a
  clause names.
- Overreach: no purpose or meaning the listing does not show; a "consistent with <routine>" clause must name the
  string, constant or call shape that supports it, or be removed.

Expect to find faults: in earlier batches about one row in ten was wrong on first draft. Do not rewrite a correct row
for style. CORRECT only when a fact, a missing path or an anchor is wrong.

## Output

Write `cloud-reports/verify/<record>.json`, one per pack, with this shape:

```json
{
 "record": "<the record name from the pack file name>",
 "session": "<your session id if you know it>",
 "verdicts": [
  {"fn": "0080F2E0", "verdict": "ACCEPT"},
  {"fn": "0080F400", "verdict": "CORRECT", "why": "the cmovl keeps the smaller value; the draft said larger",
   "text": "<full corrected sentence>", "anchors": [["0080F41A", "cmovl"], ["0080F420", "mov"]]},
  {"fn": "0080F500", "verdict": "REJECT", "why": "two indirect jumps whose targets the listing does not resolve"}
 ],
 "notes": "anything FABLE should know"
}
```

Every row in the pack gets exactly one verdict.

## Git

1. Work on the branch the session brief names.
2. Commit and push after **each** pack.
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Do not edit anything outside `cloud-reports/`. Never push to `main`.
5. When done, open a pull request to `main` titled as the session brief says, with the counts in the body
   (ACCEPT / CORRECT / REJECT).
