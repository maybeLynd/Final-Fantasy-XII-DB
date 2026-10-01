---
experiment: EXP-142
title: S-01 boot primitives execute native under Unicorn — the
  timing bootstrap both branches (001EDDC0), the MT19937
  generator seeding wrapper (00863D30 → 00866D60), and the
  eleven-allocation boot pool battery (0022A0B0 → 0036D240 →
  00369D30); every result verified against shipping bytes and an
  external MT19937 ground truth
requests:
  - FABLE-REQ-ORACLE-S01-TIMING-BOOTSTRAP-BOTH-BRANCHES
  - FABLE-REQ-ORACLE-S01-GENERATOR-SEEDING-WITH-AN-EXTERNAL-GROUND-TRUTH
  - FABLE-REQ-ORACLE-S01-MEMORY-BUDGET-ELEVEN-ALLOCATIONS
contract: ../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md
method: B
live_game: false
tool: evidence/s01-boot-exec/check.py
---
# EXP-142 — s01-boot-exec

**Status:** complete · **10/10 cases, stable across three
processes**
**Evidence:** `evidence/s01-boot-exec/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

Three FABLE requests, one harness. Execute three boot-time
bodies in isolation against the shipping image: (1) the timing
bootstrap `001EDDC0` under both `ecx` branches; (2) the MT
seeding wrapper `00863D30` plus its init `00866D60` against an
independently computed MT19937 state; (3) the eleven-`malloc`
battery inside `0022A0B0` and the nine `00369D30` pool
registrations that follow it. No live game; the allocator and
WINMM/CRT imports are scripted boundaries, everything else runs
as shipped bytes. Synthetic fixture memory only — this says
nothing about initialized-gameplay reachability.

## Harness mechanics

- Image mapped `0x120000–0x30A0000` from the exact shipped EXE
  (SHA-256 verified at load).
- **Generic IAT interception**: any `ff 15`/`ff 25` through an
  import cell resolves the PE import directory to
  `dll!name` and dispatches a named stub — `memcpy`/`memmove`/
  `memset` copy semantics emulated, `malloc` bump-allocated into
  a lazy `0x12000000` pool region pre-dirtied `0xAA`, the WINMM
  trio scripted per case, unknown imports return 0 and are
  recorded by name. The shipped IAT cells hold loader hints, not
  callable addresses — no import executes for real.
- Every non-import callee executes as shipped bytes: the whole
  `0033F020` LUT battery, `0032AE70`/`003333D0`/`00337A00`,
  `00866D60`, `00369D30`, `0036A490`, `0017D2E0`,
  `0020E620`, `0020E600`.
- Emulated writes into watched cells and returned blocks are
  recorded with their executing-site label; stub-side copy
  destinations are logged separately (`stub_writes`).

## Timing bootstrap — `001EDDC0`

Before-entry controls capture the shipped static values
(`B4=1`, `B8=1.0f`, `BC=1.0f`, `E38=0`, `E3C=0`, `E40=0`).

| case | branch | WINMM order | cells after |
|---|---|---|---|
| `t-ecx1-flag0` | `ecx=1`, flag 0 | — | `B4=2 B8=2.0 BC=0.5 E38=1 E3C=0 E40=0` |
| `t-ecx1-flag1` | `ecx=1`, flag 1, period `0x1234` | `timeEndPeriod(0x1234)` after `33F020` | triple + `E3C` cleared, `E40` kept `0x1234` |
| `t-ecx0-ok` | `ecx=0` | `timeGetDevCaps` → `timeBeginPeriod(0xBEEF)` | **none of the four**; `E40=wPeriodMin`, `E3C=1` |
| `t-ecx0-fail` | `ecx=0`, devcaps fails | `timeGetDevCaps` only | all six unchanged |

Findings on native bytes:

- **The `B8=2.0f`/`BC=0.5f`/`E38=1`/`B4=2` quadruple is written
  only on the nonzero branch** — `ecx==0` leaves all four at
  their shipped static values on both the success and failure
  WINMM arms (`t-ecx0-ok`, `t-ecx0-fail`).
- `ecx!=0` calls `0033F020` **before** the flag check; with the
  flag planted the order is `enter33f020` → `timeEndPeriod` →
  `enter32ae70` → `enter3333d0` → `enter337a00`. With the flag
  clear, no WINMM call occurs at all.
- `ecx==0` never enters `0033F020`; the call order is
  `timeGetDevCaps` → `timeBeginPeriod` → the three tail calls.
  `wPeriodMin` (low TIMECAPS dword) is stored to `01F82E40`
  and passed to `timeBeginPeriod`; flag `01F82E3C` is set
  **after** the begin call, only on success.
- A failed `timeGetDevCaps` skips `E40`/`E3C` entirely and
  still runs the common tail — no early exit.
- Both branches end `jmp 002BDA90`; the harness stops at
  `001EDE60`, one instruction before — `002BDA90` is outside
  the 165-byte isolated scope and is not executed.

## MT seeding — `00863D30` → `00866D60`

Reference is an independently computed standard MT19937
init-by-seed recurrence (`state[i] = 0x6C078965·(state[i-1] ^
(state[i-1]>>30)) + i`), not image data.

| case | calls to `00866D60` (edx arg) | state | flag |
|---|---|---|---|
| `s-first-4537` | `5489`, `4537` | == MT(4537), all 624 dwords | 0→1 |
| `s-twice-4537` | `5489`, `4537`, `4537` | == MT(4537) | stays 1 |
| `s-boot-seq` | `5489`, `5489`, `4537` | == MT(4537) | 0→1 |
| `s-flag-preset` | `4537` only | == MT(4537) | stays 1 |
| `s-mtinit-badptr` | `00866D60(rcx=0xDEAD, edx=42)` | == MT(42) | — |

- The implicit `5489` (`0x1571`) pass happens **once**, on the
  first wrapper call only; the second call seeds just the
  caller's value — `s-twice-4537` records exactly
  `[5489, 4537, 4537]`.
- `00866D60` writes all 624 state dwords and stores index
  `0x270` (624); `00863D30` sets the initialized flag
  **between** the two init calls.
- `rcx` (the "object" pointer) is never dereferenced by
  `00866D60` — `0xDEAD` produces a correct state, so the first
  argument carries no pointer reachability requirement.

## Memory battery — `0022A0B0`

Eleven `malloc` calls execute in order through the real thunk
chain `0022A0B0 → 0036D240 → 0085E730 → IAT`. The stub returns
distinct, ordered, page-aligned blocks:

| # | size | tail arg | registered? |
|---|---|---|---|
| 1 | `0x01DC0010` | `0x10` | yes, idx 2 |
| 2 | `0x00D20100` | `0x100` | yes, idx 3 |
| 3 | `0x00100010` | `0x10` | yes, idx 4 |
| 4 | `0x001C0100` | `0x100` | yes, idx 5 |
| 5 | `0x06C00400` | `0x400` | yes, idx 6 |
| 6 | `0x03000100` | `0x100` | yes, idx 7 |
| 7 | `0x02000100` | `0x100` | yes, idx 8 |
| 8 | `0x01200010` | `0x10` | yes, idx 9 |
| 9 | `0x00400100` | `0x100` | yes, idx 0xB |
| 10 | `0x00080000` | — | **no** |
| 11 | `0x00100000` | — | **no** |

- All eleven sizes match the documented request verbatim and in
  order; the two tail-less allocations get **no** registration
  call — exactly nine `00369D30` invocations with
  `(ecx=idx, rdx=ptr, r8=base, r9=tail)`.
- **`00369D30` writes bookkeeping near the head of the block,
  never the end-of-block tail bytes.** Recorded write offsets
  span `0..~0x783C` (603–6930 stores, proportional to pool
  size); `head40` post-state is zeroed for all nine registered
  blocks; `tail40` stays `0xAA` — the last 64 bytes of every
  allocation are untouched. The `+0x10/+0x100/+0x400` tail is
  headroom for the head-resident ledger, **not** slot records
  at the end of the block (corrects the earlier static
  reading).
- The two unregistered blocks remain fully `0xAA` — allocated
  but entirely unwritten by the battery.
- Registration calls `0017D2E0` → `0016D670` (a
  `vsprintf` wrapper — name formatting, stubbed no-op) and
  `0036A490` → `0020E620` ×9 per pool; these effects are inside
  the blocks and the registered-side globals, included in the
  recorded write sets.

## Scripted-boundary disclosure

- `malloc` is a bump allocator over lazy zero pages — block
  addresses are fixture addresses; the return-value *sequence*
  is real, the addresses are not engine addresses.
- `timeGetDevCaps`/`timeBeginPeriod`/`timeEndPeriod` are
  scripted at the call site (canned `TIMECAPS`, success codes);
  call order and arguments are real observations.
- `vsprintf`, `sqrt`, and other imports not named above return
  0 without side effects and are logged as `iat:dll!name`.
- All evidence is NATIVE-REPLAY over shipping bytes — synthetic
  fixture memory, no initialized-gameplay reachability claim.

## Evidence-class statement

- **NATIVE-REPLAY** — all findings above: real shipped
  instruction bodies under Unicorn, scripted import boundary.
- **MODEL-PROVEN** — fixture layouts, canned TIMECAPS, bump
  allocator.
- Nothing here claims POST-WIRE or LIVE reachability.
