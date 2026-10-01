# Brief: F-interior drafts (stream F)

You are a cloud session working for OPUS on the FF12 TZA knowledge database (this private repo, a text-only snapshot).
Read `docs/CLOUD_PROGRAM.md`, then this brief, then your pack(s) in `cloud-input/f-interior/`.

## The task

Each pack lists F-frontier functions that a database page names only at their **entry address**. For every function,
write:
- one sentence on what the body does;
- 1 to 5 **interior anchors**: addresses of instructions inside the body that do what the sentence says.

OPUS verifies your rows against the real executable and applies them to the page as a table. Your work is a draft.
Precision matters more than coverage: a wrong sentence costs more than a skipped function.

## Rules for the sentence

- **Access and representation only.** Say what the body reads, writes, compares, calls and returns: offsets, widths,
  globals, constants, bit operations, loop bounds, strides. Do **not** state purpose or meaning ("handles the menu",
  "the player's HP") unless the listing itself shows it, for example by a string it passes.
- **Name only what the listing shows.** Every 8-hex-digit address you write must appear in that function's listing:
  the function itself, an instruction address, a resolved `; -> XXXXXXXX` target, an `image base + ... = XXXXXXXX`
  table, or a branch target. Name globals by their resolved address. **Never name an address of a jump table** or any
  data that sits right after a function's code: describe its cases instead ("maps 0 to 1, 1-4 to 2-5, ...").
- **Use the decoded values.** Constants (`[f32 1.0]`, `[str "Nobody"]`) are already decoded: use them ("1.0
  (`01CEBBA8`)"). Do not guess a value the listing does not decode.
- **Formatting.**
  - Wrap addresses and expressions in backticks: `` `+0x168` ``, `` `0020E600(dword +0x10)` ``.
  - Use `rcx`, `edx`, `r8d` and so on for incoming arguments, and "the fifth (stack) argument" for stack arguments.
  - Name callees by address with their arguments where the listing shows them: `` `0018CCF0(0018CA40(), 1)` ``.
- **No literal `|` character anywhere.** Write "OR" / "AND" in words.
- **Length.** One sentence; a long body may take two or three clauses joined by semicolons. Stay under 600 characters
  unless the body really needs more (hard limit 1,200).
- **Branches.** State every path. If a guard can skip the work, say so ("when `001DDAB0()` is non-null, ..."), and say
  what is returned on the other path. Check signed versus unsigned comparisons, `cmov` direction, and the
  fall-through order of switch arms.

## Rules for the anchors

- **Inside the body.** 1 to 5 instruction addresses from the listing, each **strictly inside** the body: never the
  entry address itself.
- **Mnemonic.** Each anchor carries its mnemonic exactly as the listing prints it (`mov`, `movss`, `cmovne`, `jmp`, ...).
- **Coverage.** Pick the instructions that do the stated work: the store, the compare, the call, the tail jump. Cover
  each clause of the sentence.
- **Entry-only work.** If the function's whole work is its entry instruction (for example a one-instruction store
  followed by `ret`), do not row it. Put it under `skipped` with the reason.

## Output

Write `cloud-reports/f-interior/<slug>.json` (the pack's slug) with this shape:

```json
{
 "page": "<the page path the pack names, relative to FFXII TZA/>",
 "session": "<your session id if you know it>",
 "rows": [
  {"fn": "0017E7A0",
   "text": "adds `ecx` to dword `01DF0010` and stores the sum, except that a negative sum is stored as 2 and a sum above 2 as 0",
   "anchors": [["0017E7AA", "mov"], ["0017E7BA", "cmovg"], ["0017E7BD", "mov"]]}
 ],
 "skipped": [{"fn": "002F1CD0", "why": "its whole work is the entry instruction"}],
 "notes": "anything OPUS should know: listings you could not read, doubts per function"
}
```

Before you write each row, re-read the sentence against the listing once more. In OPUS's own batches, about one row
in fifteen was wrong on first draft: a missed guard, a reversed `cmov`, or the wrong argument order.

## Git

1. Work on the branch `cloud/f-interior-<first slug>`.
2. Commit and push after **each** pack (a usage stop loses unpushed work).
3. Use the git author `maybeLynd` with an empty email, and no Co-Authored-By trailer.
4. Do not edit anything outside `cloud-reports/`.
5. Never push to `main`.
6. When done, open a pull request to `main` titled `cloud: F-interior drafts for <slugs>`. Put the counts in the body:
   rows, skipped and doubts.
