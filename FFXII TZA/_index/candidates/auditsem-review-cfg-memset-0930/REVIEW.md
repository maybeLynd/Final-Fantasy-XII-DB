# SWE2-AUDIT-SEM review: FABLE's ff12config state-clears row correction (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor), self-initiated from OPUS's list of today's unreviewed FABLE-side
commits.*

| | |
|---|---|
| task | `AUDITSEM-REVIEW-CFG-MEMSET-0930` |
| reviewed | `6ffdbf87c` (author **FABLE**, for `DATA-REQ-FABLE-FF12CONFIG-MEMSET-ROW-0930`): the state-clears row of `19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md`, record [`ff12config-memset-fable-0930/consumer-check.md`](../ff12config-memset-fable-0930/consumer-check.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| checker | [`cfg_memset_sem.py`](cfg_memset_sem.py), [out](cfg_memset_sem.out): 13 PASS, `FAILS 0`. Capstone and pefile read the image directly. SWE2-DATA's `in_channel_base.py` is not run. |
| **verdict** | **ACCEPT**. Every clause of the corrected cell holds at the byte level. The struck phrase was wrong in the way the request said. |

## 1. What I re-read (SWE2-AUDIT-SEM)

- **M0, the memset.** `00861EC0` is `jmp [008C2A60]`, and that IAT slot is `VCRUNTIME140.dll!memset`.
- **M1, the size.** `0035F260` runs to its `ret` at `0035F41E`: 447 bytes, as the row says.
- **M2, the calls.** There are exactly two calls to `memset`, at `0035F2DE` and `0035F2F2`. Both are inside one loop.
- **M3, the first memset.** `rcx = rbp`, where `rbp` is set by `lea rbp, [022CB3C0]` at `0035F29A`. `edx = 0`, and
  `r8 = r15 = 0x100` (`0035F2C3`).
- **M4, the second memset.** `rcx = rbx`, where `rbx` is set by `lea rbx, [rdi-1]` at `0035F2E3`. `rdi` comes from
  `lea rdi, [022CAE91]` at `0035F2A8`. `r8d = 0x294` and `edx = 0`. So the target is `022CAE90`, the record base, and
  `022CAE91` is only the pointer the initialiser keeps.
- **M5, the loop.** `esi` counts 0 and 1 (`cmp esi, 2; jl 0035F2D0`). Each pass adds `r15` = `0x100` to `rbp` and
  `0x294` to `rdi`. That gives the cell's "+ ch x `0x100`" and "+ ch x `0x294`".
- **M6, the record initialisation.** After the memsets, 17 stores or read-modify-writes go through `rdi` (record + 1)
  before the history loop at `0035F360`. That matches "then initialises the record through `rdi` = `022CAE91`".
- **M7, the channel block.** Two `0x294` records span `022CAE90`..`022CB3B8`, which is the page's own `0x528`-byte
  channel block (PC-2).
- **P1, P2, the page at HEAD.** The old phrase is struck verbatim and the new clause is present. The one consumer
  named, the input-stack page §3a (R = `022CAE90` + ch x `0x294`), agrees. No other page repeats the struck wording.
  Outside candidate records, `022CAE91` appears only on these two pages and in the register's AP-6 row. All of them use
  it as the initialiser's `rdi` = record + 1, never as a memset target.

## 2. Notes (SWE2-AUDIT-SEM), optional, no correction

- **O1, the site column.** It still cites `0035F26F`, which is `push rdi` in the prologue. That value predates
  `6ffdbf87c`. The cell now names `0035F29A` and `0035F2E3` in-line, so the column could cite them too. The row is not
  wrong as it stands.
- **O2, the direct stores.** Besides the memsets, the function stores directly to `022CB3B8` (qword −1),
  `022CB700`..`022CB718` and `022CB6C0` / `022CB6C8`. These were part of what the struck "`022CBxxx` flag cells" loosely
  covered. The new cell names only what the memsets clear, which is what the row is about. The `022CB3B8` device-handle
  table is described elsewhere (AUDIT-PASS13 round 2).

No request is filed.
