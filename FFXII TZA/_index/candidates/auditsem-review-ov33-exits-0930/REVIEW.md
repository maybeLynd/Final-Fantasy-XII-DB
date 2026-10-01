# SWE2-AUDIT-SEM review — FABLE's OV-33 (ii)/(iii) static answer: which no-status exits shipped play can take (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-OV33-EXITS-0929` |
| reviewed | `87de83743` (author **FABLE**) and its addenda — [`ov33-no-status-exits-fable-0929/README.md`](../ov33-no-status-exits-fable-0929/README.md), 12 scripts |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT**, for each exit: E1 REACHABLE, E2 DEPENDS-ON, E3 UNREACHABLE, E4 loose UNREACHABLE, E4 archive DEPENDS-ON, and the RC-5 negative |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

All 12 scripts re-run with output identical to the committed `.out`. Eleven end `STATUS COMPLETE`, and
`e4_manifest_models.py` ends `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)). Three need `pefile`, so they
run under the system Python.

## 2. Question 1 — the E1 route through a save-crystal menu (SWE2-AUDIT-SEM)

Own reads: [`ov33_reads.py`](ov33_reads.py), [out](ov33_reads.out).

- **The router's open dispatch.** It indexes the table at `00280090` with `(request & 0x7FFF) − 2`, bounded to 0x14
  (`0027FE09`–`0027FE30`).
  - Request 6 (index 4) reaches `0027FFD6`, and request 16 (index 14) reaches `0027FFCA`. Both store `+0xCC = 2`.
  - Requests 2 and 22 (indexes 0 and 20) both reach `0027FE32`. For a parameter of 0x40/0x41, that arm calls
    `002D7070` (`0027FE88`). That is route 2's entry. The verdict table's "requests 16 and 22 (0x40/0x41)" should be
    read that way: 16 by itself, and 2 or 22 with the parameter.
- **The tick.** State 2 (`0027FC0F`) calls `0024AC10([+0xCC])` at `0027FC2C`, the only caller of `0024AC10`.
  `0024AC10(2)` tail-jumps to `0024AC30` with `edx = 0`.
- **`0024AC30`.**
  - It calls `0032E400(0x23, ecx+7)` at `0024AC47`–`0024AC4C` and keeps the result in `esi`.
  - When `0037B330() == 0` (`0024AC5A`), it calls `0037B450(3)`, then `0032E620(0x23, id, [01FD4A18], esi)` at
    `0024AC9F`. There is **no sign test on `esi`** anywhere between.
  - At `002DF780`, `002DF7B0` compares the FST cell with -1, and `002DF7B9` `je` takes the exit.
  - The done callback `0024ACF0` is address-taken at `0024AC6D` and only stores `02091094 = 1`, as stated.
- **The mode.** `0037B330` returns 4 when byte `02ADD931 != 0`, and otherwise byte `02ADD930`.

  My own store census ([`ov33_stores.py`](ov33_stores.py), [out](ov33_stores.out)) covers every rip-relative access to
  the two bytes. It finds seven writes:

  | writer | what it stores |
  |---|---|
  | `0037B2F0` (×2, caller `002E66D3`) | copies `02ADD932`, unless that byte is 4 |
  | `0037B390` (boot, caller `0022A399`) | `931 = 1`, then `930 = 0` and `931 = 0`, so both end 0 |
  | `0037B450` (×2) | the value its caller passes |

  The five `0037B450` callers pass:
  - `0024AB6F`: 0;
  - `0024AC7F`: 3 (the overlay itself);
  - `0035B877`: 0 or 1;
  - `0035B98B`: 0;
  - `003DD715`: 2.

  This matches `e1_mode_writers.py`. So the mode is 0 from boot, and it is 0 again after `0024AB60`, which the router
  calls at `0027F841`, `00280194` and `00281EA3`. That is enough for REACHABLE.

## 3. Question 2 — E3 UNREACHABLE (SWE2-AUDIT-SEM)

- **Only two writes.** The same census finds just two writes to `01F81160`:
  - `001A11E4` in `001A11B0` stores the allocation, or null (`001A11CC`–`001A11E4`);
  - `001A120A` in `001A11F0` stores 0.
- **One caller each.** `001A11B0` is called only from `0017D56C` and `001A11F0` only from `0017D679`, and no qword
  names either one.
- **Order.** In `0017D4C0`, `0017D56C` runs in straight-line code before the boot call `0017D5CC`.
- **Who can reach the exit.** The two job builders that test the pointer are `001D6D90` (callers `002DF777`,
  `002DF853`) and `001D6FB0` (callers `002DF735`, `002DF821`). Both are reached only from the issuers `002DF780`
  (caller `0046E03E` ← `0032E0F1`) and `002DF6C0` (caller `0032E111`), which are the pump. `e3_shutdown_reach.py`
  re-runs identically and shows that the teardown after `0017D679` reaches no pump entry.

The verdict holds, with the allocation-failure premise the record states.

## 4. Question 3 — E4 loose UNREACHABLE and the two DEPENDS-ON facts (SWE2-AUDIT-SEM)

- **E4 loose.**
  - `001D6FB0` stores its `rcx` (the record `001D6F20` returned) at job `+0x138` (`001D7067`), then calls
    `001A0BB0(…, job, r8b = 1)` (`001D7076`–`001D707C`), which runs `001A07B0` inline (`001A0BD9`–`001A0BDE`).
  - `001A0E50` loads that record from `rsi + 0x118` = job `+0x138` (`001A0E7E`). Between there and the `0059D900` test
    at `001A0EB5` it calls:
    - `001FDF70`, only when the stored size is -1. It is a one-instruction getter (`mov eax, dword [rcx]; ret`);
    - `0059FBA0` (the seek).
  - `0059FBA0` stores nothing. It tail-jumps with the *field values* `[rec+0x10]` (to `00215220`), `[rec+8]` (to an
    import) or `[rec+0x20]` (to `001D6CE0`), not with the record. So none of them can write the record's
    `+8`/`+0x10`/`+0x20` through its argument.
  - `0059D900` tests exactly those three fields. The job runs inline on the caller's thread.
- **E2 and E4-archive.** Both facts are stated as the code leaves them: an archive-absent path is required, and the
  E2 census gives six rows. `e2_path_census.py` re-runs identically.
- **The addendum's m = 4 mapping,** which FABLE did not re-read, is right. `0032FD22`–`0032FD2E` give `esi = m − 3 = 1`
  (kind 1) and `ebp = set + 0x6B`. So the two sites that can carry 4 give ids 319 and {107, 147..184, 317, 462}, and
  none is in 127..132.

## 5. Question 4 — the RC-5 negative (SWE2-AUDIT-SEM)

`0032FCA0` computes each size before it requests anything (`0032FD69`–`0032FDF1`):

| result | holds | when m = 0 | when m > 3 |
|---|---|---|---|
| `0032E400(kind, base+2)` | `ebx` | -1 | -1 |
| `0032E400(kind, base+1)` | `[rsp+0xA8]` | computed | -1 |
| `0032E400(kind, base+3)` | `r12d` | -1 | -1 |
| `0032E400(0x25, base+3)` | `[rsp+0xB0]` | -1 | -1 |

(`r12d` and `[rsp+0xB0]` are computed only for m = 1..3.)

Each request is behind its own result:
- `js` `0032FE5E` → the request at `0032FE9E`;
- `jl` `0032FED2` → `0032FF0B`;
- `js` `0032FF38` → `0032FF76`;
- `jl` `0032FFA3` → `0032FFE2`.

`00330310` skips a non-positive size at `00330378` (`jle`) before `00330444`. So no negative size reaches the pump from
this chain, as stated.

## 6. Strongest counterexamples tried (SWE2-AUDIT-SEM)

- **A thread that runs the pump during teardown.** I looked for a caller of either job builder outside the pump, and
  found none.
- **A mode writer outside the census.** The rip-relative sweep of `02ADD930`/`02ADD931` finds no writer beyond the
  seven above.
- **A write to the record inside the seek's tail targets.** Excluded, because they receive the field values, not the
  record.

None changes a verdict. The record's stated limits stand: the staff-roll scripts, the model-id sources of
`002E6700`, `00377DC0`'s rewrite, and the FileCache insert paths.
