---
experiment: EXP-104
title: Auto-status Sinks (00307D10 / 0030E060 / 003105D0 / 0030E130 / 0030E360) under isolated original execution
contract: ../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md
method: B
live_game: false
tool: evidence/autostatus-sinks-exec/check.py
---
# EXP-104 — autostatus-sinks-exec

**Status:** complete · **65/65 cases, 22/22 mutants, stable across three
processes**
**Evidence:** `evidence/autostatus-sinks-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The five auto-status sink bodies — SINK `00307D10`, TAIL `0030E060`,
RESET `003105D0`, APPLY `0030E130`, CASCADE `0030E360` — are the write
side of the stat-event path whose constructor (NOTIFY `002FEF30`) was
proven in EXP-103. This experiment executes all five subjects **from
shipped bytes**, plus the real resolver/pool family closure inherited
from EXP-101/102 and the quiet-zone helper bodies each subject calls.
Mega-closure carriers, unresolved-IAT CRT thunks, and value-steering
boundaries are disclosed scripted stubs — the same disclosure classes as
EXP-100/103.

**Relationship to EXP-086.** `0030E360` was previously executed as a
standalone subject by [EXP-086](EXP-086-status-write-execution.md)
(67/67, shipped `status_data.bin` planted verbatim, 14 side-effect
callees stubbed). EXP-104's coverage is complementary, not duplicative:
the subject is here reached *through the sink family* — `30FED0` runs
real and drives CASC/APPLY/NOTIFY as nested calls against post-write
virtual state — plus per-bitidx arm disclosure and the NOTIFY
`obj+0x24..0x47` zero/rebuild block measured for the first time. The
other four subjects had no prior subject-level execution.

| VA | role | execution |
|---|---|---|
| `00307D10` | SINK subject — status-bit sink dispatcher | **real** (224 B) |
| `0030E060` | TAIL subject — unit-side notify tail | **real** (200 B) |
| `003105D0` | RESET subject — unit field reset | **real** (418 B) |
| `0030E130` | APPLY subject — `unit+0x68/+0x78` bitmask apply | **real** (553 B) |
| `0030E360` | CASC subject — recursive cascade dispatcher | **real** (1323 B) |
| `00307CE0..0035xx` | resolver/pool family (EXP-101/102 set: GCHK FAM ORC REL LSCAN BRES MEMB BSCAN B7E0 HDEC B760 E30 FAMIDX UFLAG UIDX UBASE UGLB RESOLVE COUNT GET FIND NOOP UNOT RNG GHDL GHGET VEXT COOKIE) | **real** (29 bodies) |
| `00310780` | RESET helper: detach + byte resets | **real**, quiet `~t78` (225 B) |
| `0030C970` | index detach (2× RESET, 1× R780) | **real**, quiet `~c97` (224 B) |
| `00300280` | RESET helper | **real**, quiet `~o28` (138 B) |
| `00316CF0` | list init at `unit+0x778` | **real**, quiet `~k6c` (57 B) |
| `003291B0` / `0033C9B0` | `unit+0x80` helpers | **real**, quiet `~w91`/`~z9b` (90/75 B) |
| `0030EDA0` | `unit+0xB88` → `+0x6B0..0xB9F` xmm copy (0x4F0 B) | **real** (250 B) |
| `00308270` | bit22-gated unit writes (`u0/u4` masks, `+0x28/+0xDC8/+0xE58`) | **real** (120 B) |
| `00290B90` | `G_CTX29` linked-list walk | **real** (78 B) |
| `00336710` | element copy, `GET(byte[src+0x177])` | **real** (965 B) |
| `003839F0` | 0xFF fill | **real** (34 B) |
| `00319420`→`002EAEA0` | hub path to `S24FE30` stub | **real** (49+5 B) |
| `00322C50` | APPLY index-gate dispatch (arm `0x1D`) | **real**, quiet `~f22` (1025 B) |
| `0030EA40` | APPLY helper (action ∈ {0,2}) | **real**, quiet `~ea4` (150 B) |
| `00386AE0`/`00386A50`/`00386A70` | APPLY/CASC struct builders | **real**, quiet `~be0`/`~b50`/`~b70` (297/32/103 B) |
| `0046A790`/`0046A720` | APPLY notify carriers | **real**, quiet `~479`/`~472` (108 B ea) |
| `003279B0` | bitidx `0x68..0x71` clamped-byte callback | **real**, quiet `~79b` (94 B) |
| `0030FED0` | family mask propagation (recursively calls APPLY, then NOTIFY) | **real**, quiet `~fed` (1787 B) |
| `002FEF30` | NOTIFY (EXP-103 subject) — zeroes `obj+0x24..0x47`, rebuilds | **real** (2859 B) |
| `003BBD00` | notify formatter | scripted `P` (arg capture) |
| `003A1920` | SSE vector norm | entry-intercepted (IAT tail-jump); harness writes xmm0 |
| `00861EC0`/`00861F14` | CRT `memset`/`sqrtf` jmp-thunks → unresolved IAT | entry-intercepted |
| `0024FE30` | 950-body carrier (`319420`→`2EAEA0` thunk) | scripted ret-0 `~sq24` |
| `00300FC0` | 1085-body eligibility eval | scripted ret-0 `~sfc` |
| `0017D470` | context carrier via `30B7F0` | scripted ret-0 `~sd47` |
| `003112F0` | mega-dispatcher (builder flag) | scripted ret-0 `~s2f` |
| `0033E1F0` | element serializer (CRT vararg tail) | scripted ret-0 `~se1` |
| `0030B9B0`/`0030B8E0` | CASC eligibility wrappers | value stubs `~sb9`/`~sb8` |
| `00387730`/`003876D0` | arg4/arg5 `<0` decoders | value stubs `~s73`/`~s6d` |
| `00300140`/`00301140`/`00312280`/`003299B0`/`003284D0`/`0046A800` | CASC arm carriers | value stubs `~s014`/`~s114`/`~s228`/`~s99b`/`~s4d0`/`~sa8` |
| `00384B10` | `rand()` bit-picker inside `~be0` | value stub `~s4b1` |

## Measured semantics (native execution, not static reading)

### SINK `00307D10(rec rdi)`

```
  if (dword[rec+4] & 0x1A) == 0 -> ret            ; band gate
  flags = dword[rec+?];  rel = REL(rec)
  u4 &= ~0x10600 in some paths
  -> LSCAN (0x200 bit) or BSCAN (member walk) of carrier lists
  -> BRES handle decode -> HDEC -> fam/tag checks -> writes
  rec==0 faults at +0x64 read; REL faults +0x64 when A's rec null
```

### TAIL `0030E060(unit rcx, tflags rdx)`

```
  F = FIND(u2-rec) -> n g0 ; d (noop tail when masked)
  UNOT: D<mask>=0 v s j H w z + P (FMT arg = &local)
  RNG: VEXT type gate (b[3]>>5 in {2,3}) -> float triple ->
       VNORM = sqrt(sum sq) via IAT thunk (intercepted)
  fam path when rec==0 or b[rec+5]!=0
```

### RESET `003105D0(unit rcx)`

```
  rec = qword[unit+0x698];  rec==0 -> ret
  ~t78 (310780): bit22-gated rdi block; clears u0 bits 5,20;
                 c97(u+0x694) then b694=0xFF
  ~c97 x2 (index detach, args 0xFF and 5)
  ~o28 ; d ; n g0/g1/g2 (FIND/COUNT/RESOLVE triple)
  ~k6c (list init +0x778); ~w91/~z9b (unit+0x80 element copies,
      ecopy GET(byte[u+0x1F7]) faults null when count==0)
  qword[unit+0] AND-chain: ~0x8000020, ~0x4000080, hi-dword masks
      -> net clear bits {13,20,22,24,25,31,39,43,45,49,53,61}
  byte writes 0x695=0x696=0xFF; d[0x700] &= ~3; d[0x1F0] &= ~0x20
  308270 (bit22 set): 30EDA0 copies src[0..0x4EF] -> u+0x6B0..0xB9F
      (overwrites +0x718/0x720/0x728/0x778/0x780 first), u+0x28,
      u+0xDC8, u+0xE58, u+0x695=0xFF
  memset thunk intercept (dst,0,0x208); sqrtf intercept in z9b
```

### APPLY `0030E130(unit rcx, bitidx dl, arg3 r8d, flags r9d, action [sp+0x28])`

```
  ~f22 = 322C50 selector 0x1D: table = qword[0x2EBF040]
         gate = table && 0 <= bitidx < dword[table+4]
  action > 5 -> ret
  edi = 1<<bitidx ; a02flag = action in {0,2}
  a02flag -> ~ea4 (30EA40)
  action 0: u+0x68 &= ~edi (exit if bit already clear)
  action 1: u+0x78 &= ~edi (same early exit)
  action 2: u+0x68 |= edi ;  action 3: u+0x78 |= edi
  action 4: u+0x78 &= ~edi ;  action 5: u+0x78 |= edi
  builder: action in {2,3} -> ~be0 (386AE0) else ~b50 (386A50;
           b50 always clears struct+0x2c bit0 -> no ~s2f dispatch)
  !(flags&2) -> ~472 (46A720) for clear actions / ~479 (46A790) else
  bitidx in 0x68..0x71 -> ~79b (3279B0): B79 table clamped byte
      writes at base+0x5B42+(3*b4+i)*0x34, i=0..2
  !(flags&0x200) -> ~fed (30FED0): mask-diff vs u+0x78..0x87,
      nested APPLY(flags=1, actions 1/3) per changed bit, then NOTIFY
```

### CASC `0030E360(rsi rcx, u2 rdx, bitidx r8b, arg4 r9d, arg5/flags/action stack)`

```
  f1 = FIND(u2) ; f2 = FIND(rsi)          ; F..n tokens each
  edi = 1<<bitidx ; is34 = action in {3,4}
  flag58 = action in {0,3} ; flag5c = !(flags>>4 &1) ; flag60 = !(flags>>1 &1)
  before = ((d[0x3C] | d[0x64]) & edi) != 0
  !(flags&1):
    r = ~sb9 (30B9B0) ; r != 0 -> exit
    is34 -> r = ~sb8 (30B8E0) ; r && bitidx in {0,1,31} -> exit
  is34 eligibility:
    rec = f2+0x698 row ; recok = b[rec+5]==0 && b[rec+4]-0x1B <= 0xC
    recok && bitidx in {0,1,31} -> ~sfc (300FC0) -> exit
    !recok && bitidx in {0,1,31} && (d3c|d64)&0x80000003:
        uflag() == 0 -> exit
  action > 5 -> ret
  dispatch (vstate reads/writes; nested calls see post-write values):
    a0: d64 &= ~edi (exit if clear)   a1: d3c &= ~edi
    a2: d38 &= ~edi                   a3: d64 |= edi (exit if set or d38&edi)
    a4: d3c |= edi (exit if set)      a5: d38 |= edi (exit if set)
  flag58: d[rsi + bitidx*4 + 0xBC] = arg4 (or ~s73 ret when arg4<0)
          w[rsi + bitidx*2 + 0x13C] = arg5 (or ~s6d ret when arg5<0)
  presence-after == before -> exit
  is34 -> ~b50 else ~b70 builder ; !(flags&2) -> d (16D6A0 noop)
  arm map @0x30E8C4 per bitidx ->
    0: ~s114 (is34: ~sa8)   1/4/27: ~s99b / ~s014-SINK / RESET path
    2/8: f2+0xE9A bit 1/0 write (reads u2+5, not f2's record)
    5/27: ~s014 -> nested SINK body   31: ~s99b/SFC/serializer path
    arm4 -> recursive CASC call (C token)
  !(flags&0x200) -> ~fed same as APPLY; NOTIFY zeroes obj+0x24..0x47
```

## Findings measured by the suite

- **APPLY's gate global is `0x2EBF040`, not `0x2EBF047`** — selector
  `0x1D` dispatches to arm `0x323017`, which reads its own rip-relative
  global; bound is `dword[table+4]` with null-table -> 0.
- **`~fed` recursively calls APPLY.** Quiet-body suppression needed an
  RSP guard on the return hook: APPLY's epilogue `0x30E32E` collides with
  `~fed`'s return address, so suppression ended early without it.
- **Nested calls observe post-write state.** The model carries `vstate`
  (virtual writes) so a nested APPLY/CASC reads the parent mutation, not
  fixture memory; final observations dedupe `(addr,width)` last-wins —
  FED's re-clear legitimately overrides the dispatch write for
  `apply-set78`.
- **NOTIFY clears `obj+0x24..0x47` then rebuilds conditionally.** For
  `casc-arm-99b` (record byte `+5 == 0`) native clears `COBJ+0x3C` after
  the action-4 `0x10` write; `casc-uflag-pass`/`casc-recok-dispatch` exit
  before `~fed` and retain planted values.
- **E9A arms read `u2+5`**, not the resolved record of `f2`.
- **`~472`/`~479` gate on `!(flags&2)`** via `dword[rsp+0x40]`; targets
  are `0x46A720`/`0x46A790` (rip-relative arithmetic corrected from an
  earlier `0x3247xx` misread).
- **`30EDA0` copies `0x4F0` bytes** (`src[0..0x4EF]` -> `u+0x6B0..0xB9F`),
  which overwrites `u+0x718/0x720/0x728/0x778/0x780` before RESET's own
  copy reads them — observation order matters.
- **`unit+0` and `unit+4` are one qword**: three qword masks shape the
  high dword plus a dword-AND, producing the net 12-bit clear above.
- **CRT thunks jump into unresolved IAT hint/name data** (`0x861EC0`
  memset `(dst,0,0x208)`, `0x861F14` sqrtf) — same disclosure class as
  EXP-103's VNORM: entry-intercepted, result computed by the harness.
- **`00290B90` walks a list rooted at `qword[0x209BE80]+0x10F10`** —
  BSS-zero in a bare fixture faults; a planted context with an empty
  list head is required.

## Mutation coverage

22 mutants, all killed (patch site -> case):

| mutant | site | kills via |
|---|---|---|
| m-sink-band | `0x307D34` band `0x1A`->`0x1B` | sink-band1a |
| m-sink-diffmask | `0x307D5D` `0x8000020`->`0x4000020` | sink-flag-hit |
| m-sink-u4mask | `0x307D87` test `0x200`->`0x400` | sink-bscan-memb-hit |
| m-sink-bit16 | `0x307DE1` shl `0x10`->`0x11` | sink-band1a |
| m-sink-clrmask | `0x307DD4` `~0x600`->`~0x400` | sink-uflag-clear |
| m-memb-stride | `0x30BF4E` idx*3 -> idx*5 | sink-bscan-memb-hit |
| m-lscan-stride | `0x30B0A7` step `+0x10`->`+8` | sink-lscan-hit |
| m-bscan-bound | `0x30C29D` bit bound `0x20`->`0x10` | sink-bscan-highbit |
| m-tail-mask | `0x30E07D` `&0x410`->`&0x210` | tail-notify |
| m-tail-write | `0x30E113` `[rdi+0x4E]`->`+0x4F` | tail-basic |
| m-gchk-sete | `0x253B98` sete -> setne | sink-gchk-sidefx |
| m-rel-sete | `0x30AC22` sete -> setne | sink-lscan-hit |
| m-apply-gate | `0x323030` jl -> jge (gate always fails) | apply-clr68 |
| m-apply-a0exit | `0x30E244` je -> jne (bit-set early exit) | apply-clr68 |
| m-apply-notifygate | `0x30E2E4` je -> jne (~472/~479 gate) | apply-clr68 |
| m-apply-a02flag | `0x30E191` `{0,2}` -> `{0,4}` action flag | apply-stub34 |
| m-apply-fedskip | `0x30E320` bt bit `9`->`8` (fed skip) | apply-flag9-skip |
| m-casc-a0exit | `0x30E4EC` je -> jne | casc-clr64 |
| m-casc-a3gate | `0x30E52B` jne -> je | casc-arm-full |
| m-casc-is34 | `0x30E43D` je -> jne (sb8 gate) | casc-elig-non34 |
| m-casc-armmap | `0x30E8C8` arm byte `3`->`4` (bitidx4) | casc-arm-99b |
| m-casc-presence | `0x30E407` `or eax,[rsi+0x64]`->`+0x65` | casc-clr64 |

## Scripted boundaries

Three disclosure classes, all asserted in traces:

- **Quiet zones** (`~tag<arg>`): real body executes; inner hooked tokens
  suppressed until the body's own return (RSP-guarded so nested family
  calls — `~fed` -> APPLY — do not end suppression early).
- **Value stubs** (`~s<tag><arg>=<ret>`): return value from
  `case["qret"]`, default 0; used for eligibility wrappers, arm
  carriers, arg<0 decoders, and the `rand()` bit-picker.
- **Entry intercepts**: FMT (`P` + arg capture), VNORM/MEMSET/SQRTF
  (unresolved-IAT tail targets — harness computes the result), and the
  ret-0 mega-closure stubs.

## Results

- `cases: 65/65`, `mutants: 22/22 killed` — `run.log`, `run2.log`,
  `run3.log` (three independent processes, identical results).
- `result.json` records per-case trace, observations, diffs and faults.
- `bodies.json` records measured spans and sha256 for all 59 real
  bodies plus the 19 scripted/intercepted boundary entries.
