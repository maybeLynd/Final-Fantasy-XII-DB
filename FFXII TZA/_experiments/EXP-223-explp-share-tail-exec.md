# EXP-223 — `312280` EXP/LP-share accessor tail real (`253690`/`254EE0`/`317090`/`3171C0`/`28FB80`/`469E80`)

**Status:** complete — **541/541 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `91bdc2e8` prefix; 541 cases),
zero unexpected faults** (the 10 faulted cases are the same pre-existing
intentional-null fixtures that assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..222; 1 new case this round — `d228-msg`; 19 `d228-*`
cases retargeted from scripted return keys to real fixtures)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

The six-member accessor tail of `00312280` (the EXP/LP distribution
worker): real `312280` calls these in order `317ED0`(scripted) →
`3171C0` → `316A50`(scripted award) → `28FB80` → `253690` → `254EE0` →
`469E80` → `319490`/`3180F0`/`319CA0`(scripted) → `317090`. Real trace
hits in-suite: `t53690` ×19, `t54ee0` ×19, `t69e80` ×19, `tfb80` ×19,
`t7090` ×19, `t71c0` ×26, `t89d00` ×6, `t53770` ×43, `t53750`/`t15820`
×1.

| body | semantics |
|------|-----------|
| `00253690` | FP-total getter: `d[q[0x02092758]+8]` — one global-object dereference, returns the stored total (×19). |
| `00254EE0` | FP setter: `edx = ecx − d[q[0x02092758]+8]`; `edx>0` → `cl=6`, `edx<0` → `edx=−edx, cl=7`, `edx==0` → no call — `316A50(ecx\|kind, \|delta\|)` **on the full ecx** (kind is only the low byte; e.g. value 1281 → ecx `0x506`); stores clamped `min(max(ecx,0),0x5F5E0FF)` into `d[q[0x02092758]+8]`. |
| `0028FB80` | paired-slot source-share: resolves `q[0x0209BE80]` device object, invokes `00289D00` twice — `(dev+0x5380, ecx=d[r14+8], edx=exp, r9d=0)` and `(..., edx=lp, r9d=1)` — the EXP/LP pair write into the +0x5380 slot block. |
| `00317090` | FP-stat add: `(d[obj+0x1C2]−d[obj+0x88])·w[e78rec+0] + w[e70rec+0]` — real source-FP computation before the accessor chain; notifies `316A50(0x11, val)` via `00253770` (`jmp 316A50`). |
| `003171C0` | member-seen counter: `316A50(4,1)` early; `263C20(q[obj+0x10])!=3` gate (`b[+0xE]&0xF`); `w[q[obj+0xE68]+0x52]!=0xFFFF` → `00253750`/`00315820(rsi=w52)` → `b[q[0x020927C0]+rsi+0x3404]` use-counter (0→2 on `00315D50` miss). |
| `00469E80` | delta notifier: `ecx>0` → `0046AB10` (scripted `q6ab10`); `ecx<=0` → silent return. Receives `new−old` FP delta from `312280`. |

Helpers pulled real by the tail: `00289D00` (paired-record writer,
arg-checked at ×6), `00253770` (`jmp 316A50` award forwarder, ×43),
`00253750`/`00315820`/`00315D50` (message-id use-counter path, ×1 arm),
`00263C20` (entity-class nibble read).

## Corrections of record

- **`254EE0` notifies on the whole `ecx`, not an isolated kind.**
  `mov cl,6`/`mov cl,7` patches only the low byte of the new value —
  `316A50` sees `ecx = (value & ~0xFF) | kind`. Asserts must mask
  `c[1] & 0xFF` (kind) rather than compare the register.
- **`3171C0`'s `316A50(4,1)` fires before the gate checks** — it is an
  unconditional per-member tick, not gated by the `263C20`/`e68` arms.
- **`rargs` widened to 5 columns** `[tag, rcx, rdx, r8, r9]` — required
  to witness `28FB80`/`289D00`'s r9d pair-selector (0=EXP, 1=LP).
- New fixtures: `q[0x02092758]` → planted FP-total object (`fptot` case
  key writes `d[fpp+8]`); `q[0x020927C0]` → message-counter table
  (`msgtab`); `q[obj+0xE68]` → message record (`objlink`, `e68w52`
  default `0xFFFF`); `q[0x0209BE80]` → paired-slot device (`fbdev`);
  `e78`/`e70` records extended with `e78w`/`e70w` word multipliers.
- New case `d228-msg`: `w[e68+0x52]=5` + `msgtab` → real `315820`
  bumps `b[tab+5+0x3404]` 0→2 (the `315D50` miss arm;
  `q[0x022C2550]==0`).

## Scripted boundaries retained

`00317ED0`, `00316A50` (all notifies recorded as `s6a50`),
`00319490`/`003180F0`/`00319CA0` (position/entity-node chain —
`319490`→`3377C0` entity-context subtree not yet modeled), `0046AB10`
(`q6ab10`), `s7ed0`, `c650`, `s2alloc`/`s2dealloc`. None claim
initialized-gameplay reachability.

## Verification

- Suite: `python check.py` → **541/541**, run 3× fresh — `result.json`
  SHA256 prefix `91bdc2e8` identical all three runs.
- All six `s*` stubs removed from the SCR map; zero leftover scripted
  hits for the promoted set.
- Fault census: 10, all pre-existing intentional-null fixtures
  (`*-nulld`/`*-norec`/`*-globnull`/`d228-globn`/…), each asserting the
  fault.
