# SWE2-AUDIT-SPEC review of SD-126, the battle-HUD widget procedure arms (OPUS, c3570bf4b): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `c3570bf4b`, [README](../sd126-hud-proc-arms-0930/README.md) and `sd126_arms.py`. Measured at HEAD
`b58c633f7`. Package re-runs repeated at `701f1f01a`, identical. Static analysis of the certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD126-0930 | sd126-hud-proc-arms-0930 | `c3570bf4b` | ACCEPT-WITH-NARROWING |

**Re-run.** [rerun_sd126_arms.out](rerun_sd126_arms.out) is identical to the committed `.out` (CR ignored). A1-A4
PASS, `FAILS 0`. The package dir was clean after the re-run.

**Re-derived independently** ([sd126_indep.py](sd126_indep.py) / [.out](sd126_indep.out), using
[sdx.py](../auditspec-review-sd141-0930/sdx.py), not retool.py).
- **The id -> arm maps hold.**
  - **`002778C0`.** I decoded both tables from the bytes: byte table `00279D98` into dword table `00279D60`, bound
    45. There are 14 armed ids. `10` and `11` share `00277A64`, and 31 ids go to `00279D2C`.
  - **`00405310`.** Dword table `00405724`, bound 19. There are 6 armed ids, and 13 go to `004056FD`.
  - **`003FDFE0` / `003FF360`.** The compare chains read as the README states. `003FDFE0`: `sub 1 / 9 / 2 / 3`,
    `cmp 3`, default `003FE02B call 005C5230`. `003FF360`: pivot `cmp ecx, 0xc`, low `sub 1 / 7`, `cmp 2`; high
    `sub 0x12 / 1`, `cmp 0x10a`; default `003FF79E`.
  - All four id sets equal [widget-message-handlers.tsv](../../../16-UI/Widget-Object-Model/widget-message-handlers.tsv).
  - The message names match the protocol table's rows 1, 2, 4, 8, 10, 11, 12, 14, 15, 18, 19 and 285.
- **The "direct callees" column is not each arm's callees.**
  - **What the column is.** `sd126_arms.py`'s `callees()` lists the calls met walking straight from the arm start. It
    stops at the first `jmp` / `ret`, after 0x180 bytes, or after 10 calls.
  - **What I measured.** I built a recursive-descent reach over each function's full `.pdata` chain. It resolves all
    four `002778C0` jump tables from the bytes, including `002786D6`, `00278D86` and `00279569`, so no indirect jmp is
    left unresolved. An arm's own code is what it reaches minus what every other arm and the default reach.
  - **How far they differ.** The two agree on 18 of 31 arms. 13 arms call more than the column lists:

    | procedure | id | README | own-code callees (measured) |
    |---|---|---|---|
    | `002778C0` | 12 | "none (inline)" | **18 direct calls, 1 indirect** |
    | `002778C0` | 2 | `00274BD0` | **22 direct, 2 indirect** |
    | `002778C0` | 31 | 2 | **36 direct**, incl. `0027E050` and `005C5230` |
    | `002778C0` | 10, 11 | 2 | **9 direct, 5 indirect** |
    | `002778C0` | 35 | 4 | **8 direct, 2 indirect** |
    | `00405310` | 2 | "none" | `00244F00`, `00404D40` |
    | `00405310` | 14 | 1 | 2 (adds `00405770`) |
    | `003FDFE0` | 12 | 4 | 11 |
    | `003FDFE0` | 1 | 1 | 5 |
    | `003FF360` | 10 | 5 | 14 |
    | `003FF360` | 1 | 6 | 9 |
    | `003FF360` | 12 | 6 | 9 |
    | `003FF360` | 285 | 2 | 8 |

    The full lists are in the `.out`.
  - **Where they agree, including "none".** The "none" arms that do have no own calls are `002778C0` 32, 44 and 45,
    `003FDFE0` 15 and `003FF360` 18. For the last two, the common exit is `00808C40`, the GS cookie check (`cmp rcx,
    [01F44830]` … `jmp 00809654`, 2,390 callers), so README "none (the common exit)" is right. The `.out`'s
    `00808C40` entries are that exit, reached linearly.
- **Id 30 does have a protocol row.** It is listed with `25` and marked **narrowed**. So "private to the command menu
  (no protocol name)" is exact for 31, 32, 35, 44 and 45 only.

**Controls.**
- The table decoder reproduces the TSV's id sets (T-002778C0 and T-00405310 PASS).
- The reach resolves `002778C0`'s dispatch table to exactly the 14 targets decoded from the bytes.
- The own-code measure agrees with the package where an arm is straight-line: `002778C0` ids 1, 4, 15, 18 and 30, and
  `00405310` ids 1, 4, 18 and 19. So it does not inflate by construction.

**Citations checked.** These names come from the pages: `00244F00` the destroy entry, `00244F50` the fixed-pool widget
allocator, `002432B0` the typed-list decoder. `003697F0` is `test rcx, rcx` / `je` / `jmp 00369860`, a null-guarded
free.

**Correction wording** (the producer applies).
- **Rename the column** "direct callees" to "calls before the arm's first jump (straight-line prefix)". Add under
  Limits:

  > This column is the straight-line prefix of each arm, not its callee set. Measured over each arm's own code (the
  > code no other arm reaches), 13 of 31 arms call more:
  > - `002778C0` id 12 makes 18 direct calls, and id 2 makes 22;
  > - `00405310` id 2 calls `00244F00` and `00404D40`.
  >
  > See `auditspec-review-sd126-0930/sd126_indep.out`.
- **Change two cells:** `002778C0` id 12 "none (inline)" becomes "none before its first jump", and `00405310` id 2
  "none" becomes "none before its first jump".
- **Replace "30, 31, 32, 35, 44, 45 | private to the command menu (no protocol name)"** with:

  > 31, 32, 35, 44, 45: no protocol row; 30: the protocol's narrowed id.

  In the modding line, "six private message ids (30–45)" becomes "five private ids (31–45) and the narrowed id 30".
