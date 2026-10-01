---
experiment: EXP-128
title: EXP-109 queue/poll pump — the E070 six-arm task state machine,
  the EB70 tick pacer + EA30 thunk, retire twins, progress wrapper and
  the active/idle list splice, executed real
contract: ../02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md
method: B
live_game: false
tool: evidence/exp109-poll-pump-exec/check.py
---
# EXP-128 — exp109-poll-pump-exec

> **SECTION-02 current interpretation (2026-09-22):** [review and controls](evidence/continuation-section02-resource-queue/REVIEW.md) reconcile list-global names, the two-read state-2 sequence, offset arithmetic and common-footer terminology below. Historical producer source/results remain unchanged; the complete Unicorn campaign was not rerun in this section.

**Status:** complete · **137/137 functional cases, 123/123 mutants,
stable across three processes**
**Evidence:** `evidence/exp109-poll-pump-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

EXP-121 left two scripted boundaries in the EXP-109 queue/poll layer:
`0032E070` (the task pump) and `0035EA30` (a thunk that forces `edx=0`
and jumps to `0035EB70`). This package executes both end to end — the
pump's full six-arm state machine, the pacer's wait-spin and resync
arms, and every local helper they call — while preserving the EXP-126
allocator free-path integration: the retire arms tail into `003697F0`,
which jumps into the real PREL free body:

| VA | role | execution |
|---|---|---|
| `0032E070` | E070 — task pump (six-arm JTAB dispatch) | **real** (605 B, 156 insns) |
| `0035EA30` | EA30 — `edx=0` thunk → EB70 | **real** (7 B, 2 insns) |
| `0035EB70` | EB70 — tick pacer (wait spin + resync) | **real** (258 B, 61 insns) |
| `0032E330` | E330 — retire helper (cb + free tail) | **real** (59 B, 19 insns) |
| `0032E370` | E370 — gated retire helper | **real** (62 B, 21 insns) |
| `0032E3B0` | E3B0 — progress-callback wrapper | **real** (58 B, 19 insns) |
| `0032EC40` | EC40 — active→idle list splice | **real** (147 B, 35 insns) |
| `0035E810` | E810 — tick getter leaf | **real** (8 B, 2 insns) |
| `00368C70` | G8C70 — `ret d[0x22D7FB0]` leaf | **real** (7 B, 2 insns) |
| `0046E0E0` | GE0E0 — `ret d[0x215EFF4]` leaf | **real** (7 B, 2 insns) |
| `0016D6A0` | G6A0 — `ret 0` leaf | **real** (3 B, 1 insn) |
| `008620C0` | G20C0 — yield tail → `16D6A0` | **real** (14 B, 3 insns) |
| `003697F0` | G97F0 — free-if-nonnull → PREL | **real** (13 B, 5 insns) |
| `00369860` | PREL — allocator free path (re-executed) | **real** (1009 B, 246 insns) |
| `0046DFE0` | FLAG — S3/S4 poll gate leaf (re-executed) | **real** (18 B, 5 insns) |

Scripted boundaries (entry-intercepted, traced, NOT executed):

| VA | role |
|---|---|
| `003EADD0` | init gate (`eax` gate) |
| `0046E030` | submit-A shim → deep `002DF780` slot-table tree |
| `002DF6C0` | submit-B (`eax` gate) |
| `0046DD50` | common post-pass read-layer service |
| `003E9780` | common post-pass service |
| `0036FD50` | post-pass service gate (`eax`; nonzero → `003BB790`) |
| `003BB790` | conditional post-pass service |
| `00862090` | tick source — double-indirect thunk (`q[0x8C21D0]` → `q[0x1CCC358]` → `00826B00`, ships **live**, unlike the dormant hook cells; deep CRT tree `00812500` beyond) |
| `0017D3E0` | resync gate (`eax`) |
| `003691B0` / `00369190` | resync helpers |
| `0035E7A0` | resync value source (`eax`) |
| `0x63010000/20000/30000` | planted `ret`-stub task callbacks (`q[+0x40]/+0x48]/+0x50]`) — entry-hooked for arg trace |

## Fixture globals — all BSS (ship 0), planted and disclosed

- `q[0x22C51C0]` (`TASKG`) — pending head; the pump repeatedly re-reads it.
- `q[0x22C51C8]` — pending tail. `q[0x22C51D0]` — mutable free head.
  Historical active/idle labels do not change these independently checked directions.
- `q[0x22CA5E0]` (`TICKQ`) — the tick global; E810 reads it, EB70
  spins on it (a visit hook bumps it per iteration so the spin exits).
- `d[0x22D7FB0]` (`TICKD`) — the secondary tick dword G8C70 returns.
- `d[0x22CA5C4..+0x64]` (`PACC`) — EB70's pacer-state dword cluster.
- `d[0x215EFF4]` (`FLAGG`) — FLAG leaf state cell.
- Task records T1–T4 (`0x40060000+`, `0x78` B each), list links
  `q[+0x10]/+0x18]`, fields per the disasm below.

## Measured semantics (native execution, not static reading)

**E070** (`0032E070`) pumps `q[0x22C51C0]` in a loop. Each iteration
takes the head task, reads `b[+0x20] − 1`, bounds it `<= 5` (else
common footer), and dispatches through a six-entry offset table at
`0x32E2D0` (offsets `BD/49/63/63/AB/AB` + image base — rdata bytes
embedded in `.text`, byte-verified):

- **S1** — calls `3EADD0`; nonzero → common footer. `d[+0x28] == 0` → E330
  retire + state 0 + EC40 requeue. Else submit: `b[+0x21] != 0xFF` →
  `46E030(b[+0x21], d[+0x24], d[+0x2C], d[+0x28], stack=q[+0x38])`;
  `== 0xFF` → `2DF6C0`. Success stamps `q[+8] = E810()`, state 2.
- **S2** — two calls total: discard the first E810 return, then add the second to `q[0]` and store that **same second value** to `q[+8]`; state 3. There is no third getter call and no subtraction of the prior stamp.
- **S3/S4** — call the real FLAG leaf (`d[0x215EFF4]`); nonzero →
  common footer. S4 additionally calls `q[+0x48]`(cb48) with `ecx=d[+0x60]`
  when set and clears `d[+0x28]` on that callback-present branch; then retires. With no callback, that count is preserved. S3 reads `GE0E0()` and picks
  state `5 + (d[0x215EFF4] < 0)` via `sets`.
- **S5/S6 shared** — `b[+0x22]==0` → E330 (S5) / E370 (S6) retire;
  `b22==1 && b23==2` → E3B0 requeue-probe (ret 1 → requeue); S6 →
  E370 + `b[+0x23]=0` + retire; else **progress**: `d[+0x34] -=
  d[+0x28]` → exhausted → E330 + `b23=0` + retire; else `d[+0x2C] +=
  d[+0x28]`, `q[+0x38] += d[+0x28]`, E3B0; ret 1 → requeue arm:
  `d[+0x28] = min(d[+0x30], d[+0x34])` (`cmp`+`cmovl`), `q[0]=0`,
  state 1, `b[+0x23]=0`, and `d[+0x2C]` rounds **down** to a `0x800`
  boundary via `cdq; and edx,0x7ff; add eax,edx; and eax,0xfffff800` (signed-bias
  semantics verified by the negative-d2c case).
- **Common footer** (historical trace labels call this teardown; shutdown is not established) — `46DD50`, `16D6A0`, `3E9780`,
  `16D6A0`, `36FD50`; nonzero → `3BB790`; then epilogue `ret`.
- Two retire tails differ: the S6/exhausted-progress tail clears
  `b[+0x23]`; the S1/S4/`b22==0` tails do not.

**EB70** (`0035EB70`, `(ecx=lim_lo?, edx)`) — calls G8C70
(`d[0x22D7FB0]`, sign-extended) vs the scripted tick source
`00862090` (`rax`):
- **Differ** → spins `while (E810() − saved < max(ecx,1))` — the
  `cmovg` floor is **signed** (`edi>0 ? edi : 1`); returns the elapsed
  tick difference.
- **Equal** → resync arm: `17D3E0` gate; zero → `3691B0` + `369190`;
  folds `PACC+0x00` and `PACC+0x0C` into the `PACC` dword cluster
  (`+0x00/+0x14/+0x1C/+0x30/+0x40/…`), calls `35E7A0`, recomputes the
  positive wait limit (signed `cmovg` again), returns the prior pacer
  value.
- **EA30** (`0035EA30`) = `xor edx,edx; jmp EB70`.

**E330** (`0032E330`) — `q[+0x40]` cb → `cb(d[+0x60], q[+0x70],
r8d=1)`; `b[+0x21]==0xFF` → tail `jmp 3697F0` with `movsxd rcx,
d[+0x24]` (the real free path). **E370** (`0032E370`) — same shape but
the callback is **gated on `d[+0x28] == -1`**; gated-out returns the
callback pointer itself in `rax` (byte-verified). **E3B0**
(`0032E3B0`) — `q[+0x50]==0` → **return 1** (`mov eax,1` — not 0);
else `ebx = cb50()`; results outside `{1,2,3}` run the real `8620C0`
yield (`lea rdx,[0x1CCF998]; xor ecx,ecx; jmp 16D6A0` — the residual
`rdx` is observable in the next FLAG call). **EC40** (`0032EC40`) —
unlinks `+0x10/+0x18` (with `cmove` tail/head-cell fixups on
`0x22C51C0`/`0x22C51C8`), pushes on the idle list `q[0x22C51D0]`,
stamps `d[+0x64] = -1`, returns the **old idle head in rax**, tails
`jmp 16D6A0`.

## Execution findings beyond the static reading

1. **The pump exposes residual registers at the FLAG leaf** — E070's
   direct `call 46DFE0` arrives with `rdx`/`r8` still holding whatever
   the previous arm left (submit args, the yield's `0x1CCF998`, EC40's
   loaded links). The hook trace made these visible; the model now
   tracks `_rdx`/`_r8` through every arm.
2. **`46E030`'s fifth argument lives at `rsp+0x28` at callee entry**,
   not `+0x20` — the caller's outgoing-arg slot above the return
   address. First-attempt `+0x20` read produced a systematic diff.
3. **E370's gated-out return is the callback pointer, not 0** — the
   gate only skips the `call rax`; `rax` was loaded at entry.
4. **EC40 returns the old idle-list head** — the pushed node's
   displaced neighbour, live in `rax` at the `jmp 16D6A0`.
5. **`003697F0` is a PREL thunk, not a boundary** — `test rcx,rcx;
   je ret; xor edx,edx; jmp 369860`; the retire arms' free tail
   executes the full EXP-126 free path for real.
6. **`00862090` ships live** — `q[0x8C21D0]` → `q[0x1CCC358]` →
   `00826B00` real code (unlike the `0x8C2D80`-family dormant cells);
   its `00812500` tree is deep CRT and stays scripted.
7. **The JTAB is rdata-in-text at `0x32E2D0`**, not the `0x22E2D0` a
   first scan produced — `mov ecx,[rdi+rax*4+0x20e2d0]` with `rdi` =
   image base.
8. **EB70's spin floor is signed** — `cmovg` on `edi`, so `ecx<=0`
   paces at 1 tick; an unsigned reading inverts the wait.

## Mutation campaign

123 byte-precise mutants, all killed. Coverage: the JTAB byte and all
six arm-gate compares (`cmp eax,5`, `je d28`, `b21==0xFF`, `b22`,
`b23==2`, `state==5/6`), the S1/S2/S4 stamps, the FLAG gate `jne`, the
`sets` polarity, the progress arithmetic (`d34-=`, `d2c+=`, `q38+=`,
`jg`, `al==1`), the `min` `cmovl`, both rounding immediates
(`0x7ff`/`0xf800`), all retire-tail `b20`/`b23` clears, E330's `je`/
`r8d`/`jne`, E370's `d28==-1` gate, E3B0's `je` and `mov eax,1`, all
six EC40 splices (`cmove`×2, `+0x10`/`+0x18`×2, TASKI store,
`d64=-1`), EB70's arm-select `je`, signed `cmovg`×2, the spin `jb`,
the return `sub`, the resync `jne`/`esi` store, G97F0's `je`, and the
leaf displacements (E810/G8C70/GE0E0 cell −1/−2, G6A0 `ret 0`→`ret 8`).
Three sites needed repointing during bring-up: the `cmovg` at
`0x35EC1D` (opcode byte, not the `0x0f` prefix byte at `+1C`), the
progress-arm `cmovl` (the b23-2 arm uses `jge+mov`, not `cmovl`), and
`e070-s5-progress`'s `d2c` raised to `0x800` so `+step`/`−step`
mutants survive the `0xF800` round differently.

## Limits / boundaries

- Twelve scripted boundaries + three planted callback stubs, all
  listed above; the pump/pacer/helpers/leaves/thunk are real.
- `00862090`'s tick value is planted (`xval` sequence); EB70's spin is
  bounded by a TICKQ bump hook — real spin semantics, scripted source.
- The pacer cluster and tick/task globals are BSS (ship 0) — planted
  fixture; every executed instruction and address is real.
- Callback trampolines are planted `0xC3` stubs; the entry hook
  captures args (`cb40:`/`cb48:`/`cb50:` tokens) — the pump's calling
  convention is what's proven, not a callback body.
- The submit-A/B, service-gate/footer and resync boundaries return
  scripted sequences consumed in call order (`_xval`); their internal
  semantics remain unexecuted (disclosed).

## Board routing

- Audit request → `SWE2-AUDIT-SPEC`
- Findings request → `OPUS`
- Publication queued → `EXP128-PUB`
