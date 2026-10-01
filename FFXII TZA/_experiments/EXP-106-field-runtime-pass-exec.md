---
experiment: EXP-106
title: Field-runtime pass (0025D9E0 / 0025DF00 / 002620E0) under isolated original execution
contract: ../04-Actor-Entity/CONTRACT-field-runtime-pass.md
method: B
live_game: false
tool: evidence/field-runtime-pass-exec/check.py
---
# EXP-106 — field-runtime-pass-exec

**Status:** complete · **58/58 cases, 46/46 mutants, stable across three
processes**
**Evidence:** `evidence/field-runtime-pass-exec/` (`check.py`,
`result.json`, `bodies.json`, `run.log`, `run2.log`, `run3.log`,
`gen_bodies.py`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-field-runtime-pass` executed the entry gate of the per-frame
field pass (`diff_field_gate.py`) and explicitly left the rest
unexecuted: *"the pass body `0025DA5C`+ and its 49-callee closure are
not executed."* This experiment closes that residual — the whole
function `0025D9E0` (gate re-executed for stack discipline: the
`+0x11`-bit2 path jumps back into the gate epilogue), the wait resolver
`0025DF00` as co-subject (8-arm kind dispatch on a shipped jump table),
and the init core `002620E0`.

| VA | role | execution |
|---|---|---|
| `0025D9E0` | PASS subject — entry gate, publish, fold2, deferred block, drive loop, audio path, roster, fold1, slot-0 post-chain, bit-7 republish | **real** (1297 B) |
| `0025DF00` | WRES subject — preamble, wait-list loop, kind dispatch 0–8, interpreter arm, post-mark, settle tail | **real** (1228 B) |
| `002620E0` | init core — `b28` early-ret, `b10&4` gate, 3×`ice`-gated `icf`, `b10|=4`, `ick(0xB/0xC)` | **real** (231 B) |
| `002EF2B0`/`002EF640` | `gefb` -> `0x2164480`, `gf64` -> `0x2164280` leaf getters | **real** (20+8 B) |
| `00358940`/`003588B0`/`00263FF0` | record-by-ordinal, focus resolver + inner fam resolver | **real** (30+143+21 B) |
| `0032F6E0`/`0032F6C0`/`003603C0`/`00583920`/`00377DB0`/`003590D0` | gate/head leaf readers (`pslt`/`pck`/`gt3`/`busy`/`dfr`/`fh`) | **real** |
| `00361010`/`00360D60`/`0037CB40` | `g610` table mask, `gd60`/`gb40` qword tests | **real** |
| `003135C0`/`00303EC0`/`0030D9A0`/`00377C20`/`003148F0`/`00314910`/`003148D0`/`00314DA0` | mode chain (`g8f0`/`g860` -> `mode` bit-scan -> `g7c2` table -> `g48f`/`g491`/`gd0`/`gda0`, all nesting `gefb`/`gf64`) | **real** |
| `0020E600`/`003DB550`/`003DB640`/`003DC050` | `rc` resolver, `g550` accessor, `gb64`/`gc05` wait checkers | **real** |
| `00359B80`/`0031AD90`/`002E97B0`/`003DA710`/`002E4A10`/`001EDDA0` | settle/preamble leaf bodies | **real** |
| `00357760`/`00357770` | `G_777` clear + read-back (`g770==0` always -> `+0x16` mark) | **real** (11+7 B) |
| `001EC560`/`00265760`/`002E0540`/`0022A030`/`0022A080`/`00265270`/`0020AA30`/`0020AA40` | resolver-family leaf readers inside the `1ED*`/`265*` closures | **real** |
| `002EFE40`/`002EFE50`/`00363A80` | global byte writers (`xe40`/`xe50`/`xa80`) | **real** (7+7+7 B) |
| `00269860` | settle-mark helper inside roster/fold1 arms | **real** (364 B) |
| `0016D6A0`/`00808C40` | shipped no-op (`d`), stack-cookie check (silent `K`) | **real** (3+33 B) |
| `0025E4C0` | bytecode VM interpreter (14.6 KB) — own contract's subject | scripted `~interp` |
| `00261F90` | audio subsystem call | scripted `~audio` |
| `0032FC30` | deferred mode request | scripted `~dreq`, args `(1,0xD4)` captured |
| `00259B30`/`003E8980`/`0025ACA0`/`0017D490`/`0026FAD0`/`00379860`/`00379290`/`003DE920`/`00363B40`/`003601C0` | init-core external chain | scripted `~icb`..`~ick` |
| `0025B600`/`0025B740`/`0025B820`/`0025C170`/`0025B250`/`0025E400`/`0026A5F0`/`00233AA0` | lifecycle helpers (`lc`/`l740`/`l820`/`l170`/`l250`/`e400`/`a5f`/`a3aa`) | scripted |
| `00263660`/`00250960`/`00259FB0`/`00268690`/`003B7130`/`002E1C40`/`00254A90`/`00234150`/`002EFD20`/`002F1A30`/`00183070`/`002677B0`/`002EFA70`/`003EAA70`/`0017E7D0` | slot-0 post-chain helpers | scripted `~x*` |
| `001ED180`/`001ED130`/`001EDE80`/`001EC5C0`/`001EC5E0` | wres predicate closures (`xd1`/`xd3`/`xde8`/`xc5c`/`xc5e`) | scripted |
| `003DBF60`/`003DB2A0`/`002674B0`/`00267420`/`002E6310`/`002681E0`/`002E5030`/`002E5750`/`003E6EF0`/`003E68B0`/`003E6A70`/`0026D6F0`/`00269860`-arm helpers | wres arm checkers + settle notifies | scripted `~x*` |
| `record+0x38` fn-ptr / scratch | settle callback target | planted `cb` body |

## Measured semantics (native execution, not static reading)

### PASS `0025D9E0(ecx = slot index)`

```
  r14 = movsxd(ecx) ; rbx = [0x2098E10] + r14*0x288   ; slot block
  busy(583920)!=0 -> ret 1
  republish: b[+0x11] = (b11&~1) | ((b10>>7)&1)        ; shr al,7
  b13==0 && !(b10&1) -> ret 1                         ; refuse
  b11&8 -> skip pslt block ; else pslt(32F6E0,slot)->a5f(26A5F0)->ret1
  !(b10&1) -> ret 1 ; gt3(3603C0)->ret1
  G_SLOT(2099D70)=rbx ; G_FOC(2099D78)=gres(fh)       ; publish
  b17&0x10 -> e400(slot,slot+1) ret 1
  b11&4 -> ret 1
  r12d=1 -> 1EDDA0-driven head gate
```

### `b10 < 0x80` — fold2

```
  for edi=0..d[+0x20]-1:
      rsi = grec(358940, rbx, edi)          ; record by ordinal
      wres(25DF00, rbx, rsi)                ; per-record resolve
      slot==0 -> l740(25B740)
      r12d &= (b[rsi+0x14]>>6)&1            ; settle accumulator
  tails: l170(25C170) l250(25B250) l820(25B820) -> lc
```

### `b10 >= 0x80` — deferred block + drive loop + roster + fold1

```
  dfr(377DB0)!=0 && slot==0 && pck(32F6C0,1)&~1 ==0:
      dreq(32FC30, 1, 0xD4) -> b10|=8 -> epilogue ret
  al = (dfa(20990A8)&1) | dfb(20990AB)      ; G_DFA/G_DFB alias
      !=0 -> epilogue ret                   ; slot-1 +0x10/+0x13
  b10 |= 0x10                               ; latch
  drive loop while b[+0x12] != 0:
      rsi = grec(rbx, edi) ; wres(rbx,rsi) ; slot0 -> l740
      cl = b[rsi+0x14]
      cl&0x40 -> exit A: b[+0x12]=r12b(0) + initcore(2620E0)
      !(cl&0xF) -> exit B: jmp epilogue (r12d return)
  roster: r12d=r14d=r15d=0, ebp=1
      for each of 4 qword members at 0209A1F0:
          member -> x986(269860) mark ; +8 |= 0x40
          r14d |= rotmask ; busy bit -> a3aa(233AA0)
      b200(+0x200) &= ~2 when all-4 mask met
  fold1: active records -> x986 + gdda/g9b8/g97b checks
  x1a3(2F1A30)==1 && r14d==0 -> b11 |= 2 ; b11&2 -> &=~2, ebp=1
  slot0 post-chain (b10>=0x80 && ebp==0 && b28==0):
      xe7d(17E7D0) ; xa80(363A80, ebp+1) ; g8f0 -> xb71 arm
      xfd2(2EFD20,2)==0 -> skip
      else: xe40(2EFE40,6) xe50(2EFE50,0xFF) x830(183070)
            xa70(2EFA70,2,8,1) ; x77b(2677B0)!=0 ->
            x869(268690,9) gd0(3148D0)->gda0(314DA0, d[gefb+0x1054]&~0x18)
      x1c4(2E1C40,1,2) ; b10 &= 0x7F ; x4a9 x341 ; clf gate -> x096
  republish: b10 = (b10&0x7F) | (ebp<<7) ; ++d[+0x24] ++d[+0x38]
```

### WRES `0025DF00(rdi = slot block, rsi = wait record)`

```
  preamble: g4a1(2E4A10) writes ctx dwords when armed
  loop at 25DFA0 over wait slots:
      xd1(1ED180)==0 -> xde8 exit path
      dispatch b[rsi+0x14] via table [r14+rax*4+0x13E3CC]:
      kind 0 -> mark +0x16=1 -> settle
      kind 1/2 -> interp arm
      kind 3 -> rc(20E600)+xbf6(3DBF60): ==0xFF -> mark ;
               else +0x14=1,+0x27=1 -> loop
      kind 4 -> gc05(3DC050): ==0xFF -> mark ; else xb2a -> +0x14=1
      kind 5 -> x74b(2674B0)!=0 -> mark ; else +0x14=1 -> loop
      kind 6 -> rc+gb64(3DB640)!=0 -> mark ; else +0x14=1,+0x27=1
      kind 7 -> x742(267420)!=0 -> mark ; else +0x14=1 -> loop
      kind 8 -> settle
      >8 -> mark
  interp arm: publish rdi->G_9D90 ; g760(357760) clears G_777 ;
      interp(25E4C0, r15, rdi, rsi) ;
      rv==0 -> xd3 gate -> skip-publish (G_SKIP cmp)
      g770(357770)==0 -> +0x16=1 -> settle ; !=0 -> mark site
  settle: b[+0x1C]&0x800 && !(b14&0x40):
      g550(3DB550) row match (h[+0xDE] vs wsub+4) -> esi=1
      else esi=ebp ; d[+0x108]=ebp ; or/and b+c/b+d flag fixups
  cb arm: b[+0x10]==0 && (b14&0x40||esi) -> g9b8 -> q[+0x30] ->
      cb(rec, kind) -> b+d |= 0x40
  row tail: node = g97b(rec+0xC0) ; b[+0x10]&=~4 ;
      d[row+0x284]!=esi -> xef0/x8b0/xa70 chained row calls ;
      esi=(rv>>1)&1 ebp=rv&1 ; node+0x10 = (node&~4)|(esi<<2) ;
      esi!=0 -> rec+0xC |= 0x10
  notifies: x81e(rec) x503(rec,esi,&l30) x575(rec,ebp,&l40)
```

### INITC `002620E0`

```
  b28 != 0 -> ret                         ; early-out
  !(b10&4):
      3x { ice(17D490) -> rv>0 (signed jle) ->
           gefb + byte read -> icf(26FAD0, 0x1F/0x20/0x21, rv, d[+0x28]) }
      icg(379860) ich(379290) ici(3DE920) icj(363B40) ; b10 |= 4
  ick(3601C0, 0xB) ; ick(3601C0, 0xC)
```

## Findings measured by the suite

- **The slot block is `[0x2098E10] + slot*0x288`** — the same
  0x288-stride table the focus resolver `263FF0` indexes by family.
  `m-stride` (imm `0x288`->`0x290`) is killed by `fold2-slot1`.
- **`G_DFA`/`G_DFB` alias slot-1's own block** (`+0x10`/`+0x13`). The
  deferred flag read `(dfa&1)|dfb` runs *after* the `dreq` arm and
  exits straight to the epilogue when nonzero — verified on
  `deferred-dfa`/`deferred-dfb`; `m-deferred-flags` (`or`->`and`)
  killed.
- **Drive loop has two exits with different semantics**: settled
  (bit6) publishes `+0x12=0` and invokes init core; nibble-clear
  (`!(cl&0xF)`) jumps straight to the epilogue returning `r12d`.
  `m-drive-bit6`/`m-drive-exitA` pin both.
- **`gefb`/`gf64` constants are `0x2164480`/`0x2164280`**, not the
  earlier stale values — every gefb-derived read/write in the mode
  chain, init core and slot-0 chain was re-verified against
  RIP-relative decode.
- **The roster accumulator is `r12d=0`/`r14d=0`/`ebp=1` at init**, not
  r12=1 — the rotating mask `r14d` folds into `b200`'s bit-1 clear and
  the `x1a3`/`b11` bit-2 path. `m-roster-acc` (`or r14d`->`and`)
  killed by `roster-settle`.
- **Kind dispatch is `cmp eax,7; ja mark`** — kinds 0–8 all have arms
  (kind 8 lands on the same settle path); `>8` marks `+0x16=1`.
  `m-wres-tbl` (`cmp 7`->`6`) killed by `wres-kind7`.
- **The interpreter arm always funnels to settle** — proceed kinds set
  `+0x14=1` and loop back through the interp arm; `interp rv==0` runs
  the `xd3`/`G_SKIP`/`g770` post-mark (`+0x16=1` when `g770==0`, which
  is always: `357760` clears `G_777` before the call).
- **The settle row tail uses three chained row calls** (`xef0`/`x8b0`/
  `xa70`) gated on `d[row+0x284]!=esi`; `xa70`'s return splits
  `esi=(rv>>1)&1` / `ebp=rv&1`, feeding the node write
  `+0x10 = (&~4)|(esi<<2)` and the rec `+0xC|=0x10` — all four
  mutants on that tail killed by `wres-settle-row`.
- **Init core re-arms only when `b10&4` is clear**: three
  `ice`-gated `icf` calls (signed `jle` on the `ice` return —
  `m-ic-jle` `7e->7f` killed), then `b10|=4`, then the `ick(0xB)`/
  `ick(0xC)` pair which runs even on the `b10&4` path.

## Mutation coverage

46 mutants, all killed (patch site -> discriminator case):

| mutant | site | kills via |
|---|---|---|
| m-stride | `0x25d9f9` `88020000`->`90020000` | fold2-slot1 |
| m-rep-shr | `0x25da16` `07`->`06` | audio-base |
| m-gate-b13 | `0x25da22` `01`->`02` | gate-b13-taken |
| m-gate-b11b8 | `0x25da28` `08`->`04` | gate-b11bit8 |
| m-gate-b10t | `0x25da50` `01`->`02` | fold2-idle |
| m-head-b17 | `0x25da5f` `10`->`20` | head-e400 |
| m-e400-arg | `0x25da64` `01`->`02` | head-e400 |
| m-head-b11b2 | `0x25da7e` `04`->`08` | head-b11bit2 |
| m-r12-init | `0x25da88` `01000000`->`00000000` | fold2-idle |
| m-dreq-imm | `0x25dae9` `d4`->`d5` | deferred-dreq |
| m-deferred-or | `0x25daf5` `08`->`10` | deferred-dreq |
| m-deferred-flags | `0x25db12` `0a`->`22` | deferred-dfb |
| m-deferred-latch | `0x25db21` `10`->`20` | deferred-latch |
| m-drive-bit6 | `0x25db4e` `40`->`80` | drive-exit-a |
| m-drive-exitA | `0x25db4f` `75`->`74` | drive-exit-b |
| m-g610-mask | `0x361029` `01`->`02` | b17-t610 |
| m-roster-or | `0x25dc91` `40`->`80` | roster-active |
| m-roster-acc | `0x25dcbf` `440bf5`->`4423f5` | roster-settle |
| m-fold-shr | `0x25deaa` `06`->`05` | fold2-rec2 |
| m-b11-set | `0x25dd7f` `02`->`04` | chain-x1a3 |
| m-slot0-b10 | `0x25dd96` `0f82`->`0f83` | chain-fd2 |
| m-slot0-ebp | `0x25dd9e` `0f85`->`0f84` | chain-fd2 |
| m-xa80-arg | `0x25ddb4` `01`->`02` | chain-77b |
| m-xfd2-arg | `0x25ddce` `02`->`03` | chain-fd2 |
| m-gda0-mask | `0x25de21` `e7`->`cf` | chain-77b |
| m-clr-b10 | `0x25de39` `7f`->`6f` | chain-77b |
| m-clf-gate | `0x25de50` `74`->`75` | chain-clf |
| m-ic-b10t | `0x2620f6` `04`->`80` | audio-base |
| m-ic-b10or | `0x2621a7` `04`->`08` | audio-base |
| m-ic-jle | `0x262115` `7e`->`7f` | audio-base |
| m-icf1f | `0x26215e` `1f`->`1e` | audio-base |
| m-ick-arg | `0x2621a9` `0b`->`0a` | audio-base |
| m-wres-mark | `0x25e11d` `01`->`00` | wres-kind1-interp1 |
| m-wres-skip | `0x25e10f` `74`->`75` | wres-kind1 |
| m-wres-tbl | `0x25dff6` `07`->`06` | wres-kind7 |
| m-xbf6-cmp | `0x25e041` `ff`->`fe` | wres-kind3-miss |
| m-gc05-cmp | `0x25e0a5` `ff`->`fe` | wres-kind4-miss |
| m-settle-or | `0x25e1a3` `4008770c`->`4020770c` | wres-settle-800 |
| m-settle-and | `0x25e1b0` `bf`->`ff` | wres-settle-800 |
| m-cb-set | `0x25e21a` `40`->`80` | wres-settle-cb |
| m-node-clr | `0x25e27a` `fb`->`fe` | wres-settle-row |
| m-row-je | `0x25e2e7` `74`->`75` | wres-settle-row |
| m-row-td | `0x25e32b` `02`->`04` | wres-settle-row |
| m-xa70-je | `0x25e361` `74`->`75` | wres-settle-row |
| m-node-shl | `0x25e37d` `02`->`03` | wres-settle-row |
| m-rec-set | `0x25e388` `10`->`20` | wres-settle-row |

Two first-draft issues were corrected during bring-up: `m-gda0-mask`
needed `d[gefb+0x1054]!=0` planted (`chain-77b` now carries
`raw={0x21654D4:0x1F}` — with `dv==0` the `&~0x18`->`&~0x30` patch is
provably equivalent); several mutant VAs from the bad-offset session
were re-verified against the correct `va-0x120A00` file mapping.

## Model notes / limitations

- The interpreter `0025E4C0` is a **disclosed scripted boundary** —
  its invocation and return-driven continuation are modelled; its
  bytecode execution is not claimed here (separate contract).
- Trace normalization masks pointer-valued addresses so fixture
  layout doesn't create false diffs; return values, captured args and
  memory observations are compared exactly.
- `1EDDA0` returns 1 on shipped `.data` (`d[0x1DFE0C0]!=0`); the
  `gdda1`/`gdda2` globals are opt-in fixture overrides for the
  zero-path.
- `NOWATCH` hooks (`ga71`, `g4a1`, `g760`, `xe40`, `xe50`, `xa80`)
  emit tokens without `=rv` — their return registers are
  architecturally stale.
- `initcore`'s `b10|=4` write is synchronized back into the pass
  model's local `b10` before the tail republish — a real cross-body
  state dependency measured on `audio-base`.

## Results

- `cases: 58/58`, `mutants: 46/46 killed` — `run.log`, `run2.log`,
  `run3.log` (three independent processes, identical results; a fourth
  run reproduced them while capturing `run.log`).
- `result.json` records per-case trace, observations, diffs and faults.
- `bodies.json` records measured spans and sha256 for all 52 real
  bodies plus the scripted/intercepted boundary entries.


## SECTION-11 evidence consumption — 2026-09-23

The historical interpreter substitution remains part of this experiment's scope; it is not
retroactively described as original execution. Section11 separately runs the FULL original
0025DF00 entry for runnable kind1 under controlled idle services, the original0025E4C0 interpreter,
and selected real command callbacks. It proves selected wait/resume and active-request-index
behavior, not the full outer0025D9E0 frame driver, every wait kind, actual services or live scheduling.

[Review](evidence/continuation-section11-script-resume/REVIEW.md). Local production is validated;
formal independent acceptance remains pending. Historical source, raw records and audit status
are preserved.


## SECTION-12 follow-on evidence — 2026-09-24

[SECTION-12](evidence/continuation-section12-actor-request-waits/REVIEW.md) runs original cross-actor
request arming/start/return and non-kind-1 request-driver paths, including original interpreter
continuation. Its 139 assertions/eight falsifiers are a separate fixture; this historical EXP-106
program, raw result and scripted interpreter boundary are unchanged. The new controls refute
canonical prose that called0025E127 the proceed path: it is the blocked exit. Kind4 resumes on a
FOUND matching notification, whereas kinds3/5/6/7 wait while their dependency is active.
This addition is local production evidence, not live runtime or formal independent acceptance.
