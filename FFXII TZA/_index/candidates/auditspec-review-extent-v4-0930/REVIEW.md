# SWE2-AUDIT-SPEC review of the chained-tail extent apply (OPUS, d20226c17): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). This resumes
a dead worker's partial review. Its scripts are in this folder, and I re-ran them. Reviewed: OPUS's `d20226c17`, which
touches `chained_tail_errata.py`, the 254 `pdata-chain` rows of `_index/FUNCTION-EXTENT-ERRATA.tsv`,
`uc1_band.errata_extends/apply_extents`, and the consumers wired to them: `build_views.text_intervals` (executable view
v4), `program_coverage.py`, `field_disp_scan.py`, `receiver_flow_census.py` and `test_build_views.py` B11. I measured at
HEAD `9b6c5bc93`. HEAD moved to `30f461a92` during the review, but none of the reviewed files changed between the two.
Static evidence only, on the certified image (sha256 asserted in [pdata_pefile.py](pdata_pefile.py) and
[consumer_sensitivity.py](consumer_sensitivity.py)).

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-EXTENT-V4-0930 | auditspec-review-extent-v4-0930 | `d20226c17` | ACCEPT-WITH-NARROWING (the rows, the executable view and receiver_flow_census are accepted; field_disp_scan's wiring has a defect that needs repair; see the correction wording) |

**Re-run.**
- `chained_tail_errata.py` (report mode, no `--apply`) → [rerun2_chained_tail_errata.out](rerun2_chained_tail_errata.out):
  - `3828 (control 3,828)`, `non-contiguous: 0`, `270 (control 270)`, `16361 (control 16,361)`, `PASS controls`, exit 0.
  - `rows to emit: 0` and `already in the ledger with the same end: 270`, because the rows are already applied.
  - The output is identical to the earlier worker's [rerun_chained_tail_errata.out](rerun_chained_tail_errata.out).
- The earlier worker's four scripts ([chain_indep](chain_indep.py), [tail_bytes](tail_bytes.py),
  [tail_disp_hits](tail_disp_hits.py) and [tail_kinds](tail_kinds.py)) reproduce their committed `.out` files exactly at
  HEAD (CR ignored).
- `test_build_views.py` → [rerun2_test_build_views.out](rerun2_test_build_views.out):
  - B5, B8, B9, B10 and B11 PASS. B11 prints `unknown bytes v3 41558 -> v4 25060 (16498 moved)` and `362 entries grown
    by 17325 bytes from 364 adjudicated errata extents`, the same as the earlier worker's 14:57 run.
  - `FAILS 2` (B1 and B7), exit 1. Both failures are the `progress`/`overview` views (`undeclared ... ('progress',
    'L2-specific'), ('progress', 'L2-cumulative')`, `'overview': 'FAILED'`). They come from a peer's uncommitted edits
    to `build_views.py`/`requirements.py`, which were in the working tree before my runs. Those edits do not touch
    `text_intervals` or the extent code. The earlier worker's run had `FAILS 0`.
- None of these scripts writes into the package. `git status --porcelain` over `analysis-kit/`, `dashboard/` and the
  errata ledger was identical before and after my runs (119 pre-existing peer lines). No new change was caused by me.
  Scratch copies of the ledger and the field_disp_scan outputs went to `C:\t\auditspec`.

**Re-derived independently.**

The 254 rows were derived twice, by two parsers that share no code with each other or with the author.
- [chain_indep.py](chain_indep.py) / [.out](chain_indep.out) uses its own UNWIND_INFO decode on tk.py's section map.
  [pdata_pefile.py](pdata_pefile.py) / [.out](pdata_pefile.out) uses pefile's exception-directory parser and
  `FunctionEntry` of UNW_FLAG_CHAININFO. Both give:
  - 35,713 `.pdata` entries and 11,353 chained ones;
  - `chained roots 3828; non-contiguous 0; roots not in functions.tsv 0; short roots 270; bytes 16361`, so all four
    controls reproduce.
- chain_indep also finds 0 chained triples that differ from their own `.pdata` entry.
- pdata_pefile also finds 0 entries in the indirect `UnwindData & 1` form, which neither the author nor chain_indep
  decodes.
- chain_indep builds its own row set against the pre-apply ledger (`d20226c17^`): `same-end skip 16, beside 49, ledger
  past chain 0, rows to emit 254`. Its rows equal the committed 254 on start and end (`diff own-com 0 com-own 0`). The
  author's `rows()` on that ledger gives `emit 254, beside 49, skipped 16, conflicts 0, refused 0`.
- pdata_pefile checks the ledger at HEAD:
  - the 254 `pdata-chain` rows are exactly the 270 short roots minus the 16 with a same-end instruction-scan row;
  - 0 ledger rows run past a chain end;
  - for all 270 roots, the furthest adjudicated end equals the chain end.

**The tails are mostly switch tables, not code** ([tail_kinds.out](tail_kinds.out)). Of the 254 rows (16,254 tail
bytes):
- 153 rows (15,026 bytes) are jump or index tables. In all 153, the listed body forms the table's address.
- 45 rows (45 bytes) are 1-byte `CC`/`90` pads.
- 16 rows (964 bytes) are code reached from the body.
- 40 rows (219 bytes) are other.

Two tables, read from the bytes:
- `001D1660`: `001D167D cmp r9d, 0x119`, `001D168F lea rcx,[rip-0xb1696]` (the image base), then
  `001D16A3 mov r9d,[rcx+rax*4+0xb4c1c]` (a 0xb4c1c displacement). The 1,131-byte tail is 3 pad bytes plus 282 dwords,
  and all 282 are RVAs inside the function.
- `0023B530`: `0023B55A cmp eax, 0x16`, `0023B56C movzx eax, byte [r14+rax+0x11b6d8]` and
  `0023B575 mov ecx,[r14+rax*4+0x11b6c4]`. The tail `0023B6C2..0023B6EF` is `66 90`, then five dword RVAs (`0023B664`
  ...), then a 23-byte index table.

This is consistent with the ruling's "extent, not semantics". The bytes belong to the function. Most of them are not
instructions.

**Where the tail bytes land in v3** ([pdata_pefile.out](pdata_pefile.out)). Of the 16,361 bytes:
- 15,533 are in no body, 258 are fill, and 570 are held;
- 0 are in any other listed, frontier or funclet body.

The 570 held bytes are two whole UC-1 held rows:
- `00441A8F..00441B29` (154 B) inside `00441970`'s chain;
- `00602CF9..00602E99` (416 B, from the 257-up band) inside `00602A40`'s chain.

The author's overlap guard checks only the next `functions.tsv` start, so it cannot see held rows or frontier bodies.
Its "0 overlaps with the next entry" is true as worded.

The ruling measured 16,156 bytes in no body at `624e3534e`. Today's figures fit that: 15,791 (no body + fill) + 416
(the held row the 257-up band added later) − 51 = 16,156, where the 51 bytes were in a population body at that commit.
I did not trace which body held those 51 bytes.

**Consumers: are the extents applied, and is each one sensitive to a row?**
([consumer_sensitivity.py](consumer_sensitivity.py) / [.out](consumer_sensitivity.out)). Each consumer ran with the real
ledger, then with scratch copies: one with no `pdata-chain` rows, and one without the single row for the ruling's
example `00729920`.

- **Executable view v4 (`build_views.text_intervals`). Applied and sensitive.** The overlap is `+0` in every case.

  | change | unknown | listed | held | fill |
  |---|---:|---:|---:|---:|
  | v3 → v4 | −16,498 | +17,325 | −570 | −257 |
  | the 254 chain rows alone | −15,045 | +15,863 | −570 | −248 |
  | removing `00729920`'s row | +60 | −60 | | |

  The 60 bytes are that row's 191 minus the 131 already covered by its instruction-scan row (`00729A60`).
- **`receiver_flow_census.check_extent_against_graph`. Applied and sensitive.**
  - Extent `00729920..00729A9C` is ACCEPTED with the row and REFUSED without it.
  - The positive control is an end 1 byte short (`00729A9B`). It is REFUSED even with the row, so the guard accepts only
    the adjudicated end.
- **`program_coverage`. Applied, but nothing reads it.** The two 115-line reports ([pc_with.md](pc_with.md) and
  [pc_nochain.md](pc_nochain.md)) differ only in the series-break note: `grows 362 entries by 17325 bytes (364 errata
  extents)` against `159 entries by 1462 bytes (159 ...)`. No figure in the script reads `fns[..]["size"]` after
  loading. So "Byte figures before 2026-09-30 are a different series" describes no byte figure in this report.
  Separately, the committed `COVERAGE-DIMENSIONS.md` dates from `de630e72a` (2026-09-22) and carries no series-break
  note.
- **`field_disp_scan`. Applied and sensitive, but it has a defect.**
  - A real run pair on `0023B530` with `--disp 0x11b6 0x11b6d8`, where the control is the body read at `0023B56C`. With
    the row, the output has the site `0023B6D3 add byte ptr [rbx + 0x11b6], ah`, kind `rw`, and names `0023B530` as a
    WRITER of +0x11b6. Without the row there are 0 sites.
  - `0023B6D3` lies inside the five-dword jump table (`0023B6C4..0023B6D8`), so it is table data decoded as an
    instruction.
  - Over all 254 tails, field_disp_scan's own linear decode and filter (base not rip/rsp/rbp, displacement > 0) emit
    143 tail sites. 137 of them are in 56 jump-table tails, and 84 of those have a displacement below 0x2000, the size a
    field offset would have. The other 6 are in 3 other tails.
  - The script also grows the raw list, without the UC-1 band. It therefore prints `364 entries grown by 17376 bytes`,
    not the view's 362/17,325.

**Controls.**
- The one-hop walk variant gives 5,068 roots, 189 short and 11,987 bytes. So the 3,828/270/16,361 controls would catch a
  walker that stops after one hop (chains here are up to 6 hops deep).
- The contiguity check is inert on this image, because there are 0 non-contiguous chains.
- B11 is sensitive to losing all the chain rows: the move would be 1,453 bytes and 159 entries grown, and both fail it.
  It is not sensitive to single rows: its margin is 16,498 − 16,156 = 342 bytes.
- B11's threshold is the ruling's chain figure. The move it compares against includes the 159 instruction-scan extents
  applied in the same step. The chain rows alone move 15,045, which is less than 16,156.
- Nothing asserts the 570 held → listed bytes.

**Citations checked.** Every figure in the commit message's chained-tails paragraph matches the tool output above: 3,828,
all contiguous, 270, 16,361, 254, 49 beside, 16 skipped, 0 conflicts, 0 next-entry overlaps, 362/17,325 and "at least
16,156". The ruling's example is also confirmed: `00729920`, 189 B catalogued, chain end `00729A9C`. The one exception
is the B11 attribution (below).

**Runtime routing.** None. This is settled statically.

**Correction wording** (the producer applies it):
1. Commit and record B11 line: "v4 moves 16,498 UNKNOWN bytes (v3 41,558 → v4 25,060): 15,045 from the 254 chain rows
   and 1,453 from the 159 instruction-scan extents first applied in the same step. 570 held bytes (UC-1 held rows
   `00441A8F` and `00602CF9`, each wholly inside a chain tail) and 257 fill bytes also move to listed."
2. program_coverage: "program_coverage prints the extent series break; none of its figures reads a function size, so
   its tables do not change under the rule."
3. field_disp_scan (**repair required** before its extended-tail output counts as instruction evidence): "Under the
   extent rule, 153 of the 254 chain tails are switch or index tables (15,026 of 16,254 bytes). field_disp_scan decodes
   them linearly and emits 137 table-byte sites in 56 tails, e.g. a false `rw` of +0x11b6 in `0023B530` at `0023B6D3`."
   The repair can do either of two things: skip tail bytes that the body indexes as a table, or decode past the listed
   end only from branch targets. Re-run `consumer_sensitivity.py fds` afterwards: the tail site must be gone while the
   control stays.
4. Held rows (for FRONTIER/UC-1 owners, not a defect of the rows): "the chain extents resolve held rows `00441A8F` and
   `00602CF9` as bytes of `00441970` and `00602A40`; the band still reports them as held."
