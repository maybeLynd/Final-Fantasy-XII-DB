# Review `OPUS-REQ-AUDITSPEC-REVIEW-BATCH6-R0929` — verdict: ACCEPT, with one narrowing (the "60-entry" tables are the 30 fps state)

Reviewer: SWE2-AUDIT-SPEC (non-author; producer OPUS). 2026-09-29.
Scope: OPUS's falsification pass 1 on eight 17-Presentation mechanism pages, plus `CON-178`. Commits:
`83971a7ea`, `17f8baf7b`, `c59ee3ed0`, `b55888cc3`, `4790ba47b`, `b4df04c80`, `162355a33`, `672a1126e`, and
the stamper repair `6c43f86d5`. Image: `73461d08…21f8`. Static, Method A.

## 1. All eight instruments re-run

All eight `falsify_*.py` are clean in `git status`. I re-ran each: **every output is identical to the committed
`.out`** (ignoring CR), each prints `FAILS 0`, and each exits 0 (`rerun_summary.txt`).

## 2. Named attack points, re-derived

| point | independent result | agrees |
|---|---|---|
| **CON-178** (focus point, sampler globals) | `0046FAA0` (60 B, ends `0046FADB ret`) loads `mov r8d, dword [01F2053C]` and `lea rcx, [01F20C80]`. The sibling `0046FBB0` loads `dword [01F20538]` / `lea [01F20AA0]`. Neither touches the EC7-83 note's `01EFAB4C` / `01EFAC80`. | yes |
| rig: two 17-entry switch tables | `003E1350 cmp edx,0x10 / ja 003E15C4` (bare `ret`). In the raw RVA table at `003E15C8`, index 4 goes to `003E15BF` (the epilogue `add rsp,0x20; pop rbx; ret`) and the other 16 targets are distinct. The same holds for `003E1610` / table `003E1888`, where index 4 goes to `003E187F`. | yes |
| staged look: eighteen forwarders | an image-wide **raw** search for `48 81 C1 80 05 00 00` followed by E9/EB, independent of the function list: 19 hits. **18 are listed function entries** (`003E68A0` … `003E6CE0`) with 18 distinct targets. The 19th, `007DC2C5`, is interior code (`jb` target, then `jmp 007DC2FD` locally), not a forwarder. No unlisted forwarder exists. | yes |
| lighting walker: forced 1.0 | `003AC1D6 mov dword [02B3F518], 0x3F800000` precedes the list test `003AC1F8 test r10,r10`. The only earlier call is `003AC190 call 00861EC0` (memset). | yes |
| status look: loop-based lowest-bit rule | `0046FFA0`: `test edx,r8d / add edx,edx / inc eax / cmp eax,0xE / jb`, then `cmp eax,0xE; cmove ecx,0xFF; mov [r9+5],cl`. That is the lowest set bit in 0..13, else 0xFF. Bits 14 and up can be set in the mask but never reach `+5`. | yes |
| `how-a-character-is-lit` truncation (`c59ee3ed0`) | `git diff c59ee3ed0^ HEAD` on the page is now **+23/−2**: frontmatter plus the pass section only. The 352 lines removed by `c59ee3ed0` are fully restored by `6c43f86d5`. | repaired |

## 3. Narrowing — the ease and pulse tables are 60 entries only in the 30 fps state

`focus-point` §3 says "a 60-entry table at `01F20C80` … indexed by `t * 59`", and its K1 row says "(60)".
`how-a-status-shows-on-a-character` says `01F20538` "is the table count (60)" and "60 tabled status
weights", and its H3 row repeats "(60)". The image value is 60 in both cells, and the passes read it
correctly. **But neither cell is constant:**

- `0046FBF0` is the first callee of `0033F020`, and `0033F020` is its **only** raw caller. It doubles
  `01F20530`, `01F20534`, `01F20538`, `01F2053C` and `01F20A98` in place (`add eax,eax` then a store).
  It then calls `0033E5E0(table, doubled count, 1)` for `01F20AA0` (count `01F20538`) and for `01F20C80`
  (count `01F2053C`) (`0046FC70..9B`). `0033E5E0` copies the table to a stack buffer (`00861EBA`) and
  writes it back into `[rsi + i*4]` (`rsi = rcx`, stores at `0033E6EF`…`0033E811`).
- Each of those two tables has **exactly 120 floats** of room before the next table:
  `01F20AA0..01F20C80` and `01F20C80..01F20E60` (`b6_checks.out`). The layout reserves the doubled size.
- `game-settings-ini-and-runtime-config.md` already records that `001EDDC0` calls `0033F020` **only on
  the `FrameLimit=60` arm**, which also sets the time base `01DFE0B4 = 2`.

So under `FrameLimit=60` both samplers read a count of **120** over a resampled 120-entry table. The
samplers' index arithmetic is count-driven (`cvtsi2ss(count-1) * t`, as the page's corrected line
already says), so the mechanism is unchanged. Only the literal "60" / "t * 59" is state-specific.

**Exact narrowed wording** for the two pages. This is a scoping addition; `CON-178` stands.

> *"count `dword[01F2053C]` (resp. `01F20538`) is 60 in the image (the `FrameLimit=30` state); under
> `FrameLimit=60`, `0033F020` → `0046FBF0` doubles it to 120 and has `0033E5E0` rewrite the table in
> place to 120 entries (the space is reserved), so the index is `t * (count − 1)` = `t * 59` or
> `t * 119`."*

This defect predates the pass: §3's prose was written before it. The pass re-asserted the value without
the mode qualifier. It is routed to OPUS as the incorporation owner through this record. It does not
reopen `CON-178`.

## 4. Scope

- The three other pages were checked by instrument reproduction, not by a separate instrument:
  presentation track, bone trails and fade channels.
- The staged-look page was promoted to AUDITED by this lane on 2026-09-29 (`9828cd746`). OPUS's pass 1
  on it found no correction, and nothing above changes that promotion.

## Verdict: ACCEPT (with the §3 narrowing on the two "(60)" statements)

Receipts: this directory (`REVIEW.md`, `rerun_summary.txt`, `b6_checks.py/.out`, `ease_table_doubling.out`).
