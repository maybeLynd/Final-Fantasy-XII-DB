# SWE2-AUDIT-SPEC review of DD residue batch 4 (swe2contract-ddres-b4-0930 at 3198ee367): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Author: SWE2-CONTRACT (OPUS's
subagent). Reviewed: `3198ee367`, the RC-22..RC-34 incorporation from SWE2-DATA's `rc22-34-resource-readers-0930`
(`1261e2044`), plus this lane's batch-1 narrowing (the counter row and the `rip_refs.py` windows). Image
`73461D08…`, static.

| request | record | commit | verdict |
|---|---|---|---|
| `SWE2CONTRACT-REQ-AUDITSPEC-DDRES-B4-0930` | [swe2contract-ddres-b4-0930](../swe2contract-ddres-b4-0930/README.md) | `3198ee367` | ACCEPT-WITH-NARROWING |

**Re-run** ([rerun.py](rerun.py), [rerun_summary.txt](rerun_summary.txt)). Every output is byte-identical to its
committed `.out` ignoring CR, and every run exits 0:
- `rip_refs.py` with the five windows the batch-1 README now records: `02064ACC 02064AD0`, `02CB8084 02CB8088`,
  `01F832B0 01F832C8`, `00369D30` (default) and `02CB7FD0 02CB843C`;
- `counter_access.py`.

The windows question is closed: the recorded windows reproduce the outputs.

**Controls (counter_access.py).** C2, the image-base-relative re-find of `001CD1CB` (disp `0xAFCEC`), is sensitive to
the defect it guards: a rip-only sweep fails it. C1 guards the rip decoder. What neither control covers is code outside
`functions.tsv` extents, which is the sweep's population. So I re-ran the census over raw `.text`.

**Re-derived independently: counters.** [counter_raw.py](counter_raw.py) / [.out](counter_raw.out) uses `tk.py` raw
disp32 sweeps over all `.text`:
- rip 14, image-base-relative 7, DIR64 0;
- the **21 sites equal `counter_access.out`'s 21 exactly** (only-raw `[]`, only-theirs `[]`).

The display-side row therefore holds: `001D0190` has one `cmp` (`001D01EE`), and `001D0390` / `001D5260` / `001D5520`
have no direct access.

**Re-derived independently: RC-25 residue.** [setter_sites.py](setter_sites.py) / [.out](setter_sites.out) sweeps raw
E8/E9/jcc to the setter `002CEE00` and finds 2 sites:
- `00567A52` with `or ecx, 0xffffffff`;
- `0056A05E` with `movsx ecx, word [rax+0x60]`.

The control (the `00282DF0` call feeding `0056A05E`) was found. The row's residue "the values the setter's two call
sites pass" is correct but looser than DATA's record, which says only the second site is open (the record word `+0x60`
of `00282DF0`'s result). RC-25 has since been answered (`0b5dd5720`), so I make no correction.

**RC-30 row** matches DATA's §3: three unbounded sites, `002CEAE0`, `003C9950` and `00575C30`, plus the 18
computed-kind path sites. It has since been answered (`7fa0f7d33`).

**Narrowing 1: the console page table is 15 rows, not 14.** The RC-29 row ("14 x 22 page layout table"), the cl2 and
mrp page notes ("14 pages × 22 rows … `0x4D0` bytes") and this record's consumer line all carry DATA's extent
`008FCE00`–`008FD2D0`. [console_row14.py](console_row14.py) / [.out](console_row14.out) and
[manifest_rows.out](../auditspec-review-ddres-b3-0930/manifest_rows.out) show a 15th row:
- The image has exactly 2 dword stores to `[reg+0xA88]`: `001D1503` (`001D0390`, `ebx`) and `001D536D` (`001D5260`,
  `0xE`).
- `001D5260` takes the `<Information Page>` header branch when `[rbx+0xC56] != 0`. It then stores `0xE` to `+0xA88`,
  and at `001D53A2`/`001D53B0` reads `[r14 + (0xE*0x16 + col)*4]`, which is row 14 at `008FD2D0`.
- Row 14 holds 12 command ids (`2 3 DE DD 6 8 CC 9 A 65 66 122`, then zeros), all within the renderer's
  `id-1 <= 0x125` bound. The next dword, at `008FD328`, is ASCII.

So the table is 14 paged rows plus the Information-page row: 15 × 22 u32, `0x528` bytes, `008FCE00`–`008FD328`. DATA's
"14 pages hard-coded: `mov dword [rbx+0xA88], 0xE`" reads that store as a page count. It is the row index of the
information page. The premise refutation is unaffected.

**Narrowing 2: `lst` header `+0x04`, census scope dropped.** DATA's §4 says `+0x04` = 100 "is not read by either reader
or by anything else in the census" (the 27 functions holding a rip reference to `02AED490`). The `lst-menuquest-list.md`
note, superseded-readings line and status line say "read by nothing" / "unread". That is a universal claim built on a
27-function census.

**Correction wording for the row owner (SWE2-CONTRACT)**
- RC-29 row, cl2 and mrp page notes: replace "14 x 22 page layout table" / "14 pages × 22 rows of u32 command ids
  (stride `0x58`, `0x4D0` bytes)" with "15 × 22 u32 command ids (stride `0x58`, `0x528` bytes, `008FCE00`–`008FD328`):
  14 paged rows plus the Information-page row 14 at `008FD2D0`, which `001D5260` selects with `mov dword
  [rbx+0xA88], 0xE`". Route the same extent fix to SWE2-DATA for `rc22-34-resource-readers-0930` §3.
- `lst-menuquest-list.md` (answered note, superseded-readings line, status line): replace "`+0x04` is read by
  nothing" / "`+0x04` unread" with "`+0x04` is read by neither reader nor any of the 27 functions holding the list
  pointer `02AED490` (census scope)".

**Not checked.** The as7 LZ decode (DATA's `as7_decode.py`, 7,216 pages), the mg sub-mesh directory and the SWE2-EC7
role-label routing were not re-derived; the author's receipts are recorded as re-run by SWE2-CONTRACT only.
