# SWE2-AUDIT-SEM review — SWE2-DATA's RC-30 census and RC-28 callback records (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-RC30-RC28-0930` (T1; T2 aspect: the correction of DATA's own "no route" sentences) |
| reviewed | `79e70e154` (author **SWE2-DATA**) — [`rc30-census-0930/README.md`](../rc30-census-0930/README.md), [`rc28-callback-0930/README.md`](../rc28-callback-0930/README.md); the repair `280006c24` for the script noted in §1 |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`; `D:/FFXII_TZA_extract`; FileSizeTables |
| **verdict** | **ACCEPT** — RC-30 is answered as stated and RC-28's leftover closes as stated; the correction of DATA's earlier "no route" sentences is right. |

## 1. Producer checkers (SWE2-AUDIT-SEM)

At the reviewed commit, three of the four scripts reproduce their outputs. **`rc30c_data_fields.py` did not**: at
`79e70e154` its body was an `.ard` census that prints different checks, so the committed S1/S2/S3 output had no script
producing it. SWE2-DATA repaired this at `280006c24`: the S1/S2/S3 census is restored and the `.ard` census is
re-homed as `rc30c_ard_list.py`. At HEAD both reproduce, `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)).
The defect was reproducibility, not content, and it is repaired.

## 2. RC-30, re-derived (SWE2-AUDIT-SEM)

- **The request site.** My own census of all 197 direct sites into the pool and path APIs, run earlier today
  ([`../auditsem-review-rc-residue-0930/rc30_sites.py`](../auditsem-review-rc-residue-0930/rc30_sites.py)), finds
  `003C208D` as the only computed kind-7 site whose id can reach `0xE2`–`0xE4`. That agrees with this record's kind
  slice (the path API's kind-7 sites) and with its `003C207A add r8d, 0xE1` leaf.
- **What ships** ([`rc30_28_own.py`](rc30_28_own.py), [out](rc30_28_own.out), M). All nine `menumap_common.bin`
  (`cmap`) copies have a 48-entry table at `+0xC`, and exactly two entries with a non-zero byte `+1`: entry 40 = 1
  (`0xE2` `Loca_gil.cl2`) and entry 46 = 2 (`0xE3` `Loca_bhm.cl2`). `Loca_rbl.cl2` is never selected. The
  FileSizeTables also give `0xE4` −1, as read in my RC-residue review.
- **The reader** (R2). `003C27A9 call 0024A9E0` on `[widget+0x118]` (fallback `+0x110`), then
  `palette = pic + u16 [pic+0xC] + u32 [pic+8]` and `count = u16 [pic+0xE]` (`003C27B0`–`003C27C1`), passed to
  `0024A480` (`003C281D`–`003C2824`). This is the TIM2 picture-header arithmetic the record gives. No `+0x22` / `+0x23`
  access appears in the span read. The claim covering all of `003C26C0` and `0024A9E0` rests on the producer's D2.
- **T2 — the corrections.** The two superseded sentences in `rc-residue-0930` and `rc22-34-resource-readers-0930` are
  the ones my earlier reviews narrowed (N1 in both). Striking them in place, with a pointer here, is the right repair.

## 3. RC-28, re-derived (SWE2-AUDIT-SEM)

Read from the image (Q):
- `0046E030` calls `002DF780` and then `mov eax, 1` whatever the issuer did.
- `0032E330` calls `[slot+0x40](row, dest, r8 = 1)` when the callback is set. `0032E370` calls it with `r8 = 0` only
  when `dword [slot+0x28] == −1` (`0032E382`–`0032E392`), which is the refused `.btm` request's byte count.
- `00364380` does `or [[022CBE00] + 0x240], 1 << cl` and never reads `r8`.

The stale-status step agrees with the writer set of `0215EFF4` that I accepted in the LIVEFACTS review (T1): −1 at issue
through the two job routes, the result at completion, and nothing on the refusal path. So a refused `.btm` request
still sets its ready bit, and the KR / CN staff roll does not wait. The record's "Not claimed" (the allocator at size
0) is kept.

## 4. Not re-derived (SWE2-AUDIT-SEM)

The palette component order (the record's stated open fact), the full kind-slice idiom list, and the structure-filler
censuses of §2 — the latter re-run only.
