# EXP-200 — EXP/LP share-formula family `002F8BB0` / `002F90C0` execution

**Status:** complete — **360/360 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`bd903eb43fae93068a3dbda1d1e99f6ff6d101c35c46ac168b2e4c781c5fd93a`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..199; 326 inherited + 34 new `f8bb0-*`/`f90c0-*` direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Promotes the share-formula family from scripted retkeys to shipped-byte
execution, as planned in EXP-199:

- `002F8BB0` — EXP share formula (real, 0x1AE bytes to `0x2F8D5D`)
- `002F90C0` — LP share formula (real, 0xB2 bytes to `0x2F9172`)
- `00313800` — leader-slot byte leaf: `b[glob+0x5AD5]` → tail `00320890`
- `00320890` — slot-map index resolver: scan `b[glob+0x5A48+i*2]`, `i<9`,
  for the byte; `0xFF` or miss → `-1`
- `00264150` — global LP-suppress leaf: `movsx eax, b[020AA2AA]` (ships 0;
  `lflag` fixture)

Already-real callees reused: `003135C0` (`0030D9A0()==1` mode check),
`0030D9A0` mode map, `0031B860` owner scan, `0031B810` member-slot resolve,
`00320AB0`/`0031B9F0` class maps, `002367A0` OBJARR scan, `00322C50` bound
validators, `00377C20` can-die leaf. No `0020E600`-tree callee is reachable
from either formula body — the deep machinery worry from the EXP-199 scope
note does not materialise; every call lands in the already-real helper set.

Scripted boundaries kept (unchanged from EXP-199): `00316A50` msg,
`0028FB80` broadcast, gauge trio, position chain, `0030C650`, hooks,
`00808C40` cookie.

## `002F8BB0(rcx=guest, rdx=objrow)` — decoded structure

`arg2` is the member/object row (`rdx` in `00312280` = `r14` = its own
entry `rdx`), *not* the record — the formula follows `q[objrow+0x698]`
itself.

**Guest validation (skipped when `rcx==0`):** `b[guest+5]` must be `0`;
`0031B860(guest)` must resolve an OBJARR row (guest must be somebody's
linked record — `f8bb0-nown`); if `b[guest+5]==0` then `b[guest+4]` must not
be in `[0x1B,0x27]` (`f8bb0-gb4`); `(d[guest+0x64]|d[guest+0x3C]) &
0x80000003` must be `0` (`f8bb0-gflg`). Any failure → return 0.

**Record gate:** `objrow` non-null, `rec = q[objrow+0x698]` non-null,
`b[rec+5]==1` (`f8bb0-null`/`norec`/`b5rec`).

**Mode split** on `003135C0()` (i.e. `0030D9A0()==1`):

- **mode≠1 — member-share path:** `ebp` counts hits over `i=0..3` of
  `0031B810(i)` = member-slot map `b[glob+0x5A5A+i*2]` → `002367A0(map)`
  OBJARR scan (`w[rec+4]==map`). A resolved member row's rec is skipped when
  `(d64|d3C)&0x80000003` set, `b5==0 && b4∈[0x1B,0x27]`, or `b5==0 &&
  b4==0x1A`; otherwise counted (null rec also counts). If `ebp==0` the
  compute is **skipped entirely** — `esi` stays 0, the routine returns 0
  (`f8bb0-zdiv`). Otherwise
  `esi = ((b[rec+0x1C2]-b[rec+0x88]) * d[q[objrow+0xE78]+0x34]
        + d[q[objrow+0xE70]+0x34]) / ebp`
  — **signed `idiv`, truncation toward zero** (`f8bb0-ndiv`: −5/2 → −2).
  Negative results pass through (`f8bb0-neg`: −5 → `0xFFFFFFFB`); the
  `[0,999999]` clamp lives in `00312280`, not here.
- **mode==1 — leader path:** `idx = 00313800()` = `00320890(b[glob+0x5AD5])`
  (slot index of the leader byte in the `0x5A48` map; miss → −1 →
  `00320AB0` resolves row 0 → no match). For `rcx!=0` the guest must equal
  `00320AB0(idx,1)`'s resolved row — the member-map (`0x5A5A`) row —
  else return 0 (`f8bb0-lead` vs `f8bb0-nlead`/`lmiss`). `rcx==0` skips the
  match and takes the **full undivided** formula value
  (`f8bb0-lead0` = 50, no `ebp` division in this path at all).

**Guest modifiers:** `b[guest+0x6B]&8 || b[guest+0x7B]&8` → `esi *= 2`
(`f8bb0-dbl`, `f8bb0-dbl7b`); `b[guest+0x6B]&0x20 || b[guest+0x7B]&0x20` →
`esi = 0` (`f8bb0-zero`).

## `002F90C0(rcx=guest, rdx=objrow)` — decoded structure

Same argument convention. Head: `00264150()` nonzero → return 0 (shipped
cell is 0; `f90c0-flag` proves the arm). Guest validation (skipped for
`rcx==0`): `b[guest+5]==0`; `b[guest+4]` must be `0x1A`, `<=6`, or `>=0x28`
(`f90c0-gb4lo` rejects 7, `f90c0-gb4a`/`f90c0-gb4hi` allow `0x1A`/`0x28`);
`(d64|d3C)&0x80000003` rejects (`f90c0-gflg`). **No `0031B860` owner check**
— LP pays an unlinked guest that passes the flag/type gates
(`f90c0-nolink` = 10). Record gate identical (`f90c0-norec`/`b5rec`).

Formula — **no member division, no mode split:**
`esi = (b[rec+0x1C2]-b[rec+0x88]) * b[q[objrow+0xE78]+0x2F]
      + b[q[objrow+0xE70]+0x2F]` — **byte-width** LP rates (`f90c0-split` =
10, `f90c0-neg` → `0xFFFFFFFB`). Guest mod: `b[+0x6B]&0x10 || b[+0x7B]&0x10`
→ `esi *= 2` (`f90c0-dbl`/`dbl7b` = 20).

## Corrections of record

- EXP-199 listed the formulas' arg2 as the record; it is the member row
  (`r14`/`rdx`), confirmed by live `rargs` at both call sites.
- `ebp==0` (no resolvable member) yields **share 0**, not the undivided
  raw — the whole compute+`idiv` sits under `test ebp,ebp; je`.
- Member count uses `w[rec+4]` (word), so a `b5==1` record (`w+4=0x0100`)
  can never match a byte map entry — `objrow` never self-counts; linked
  guests (`w+4==0`, `b5==0`, `b4==0`) **do** count as members.
- `0030D9A0` order confirmed: `&8→5`, `&4→4`, `00377C20()≠0→3`, `&2→2`,
  else `d[glob+0x5B04]&1` — mode-1 (leader path) therefore requires
  `00377C20()==0`; the harness default `cd_words=[0x8000]*8` forces mode 3,
  so leader cases plant `cd_words=[0]`.
- **Semantic find:** the same `(d64|d3C)&0x80000003` flags that gate the
  `00312280` retain scan re-gate inside both formulas — a `00377C20`-
  retained flagged guest is *stashed but awarded 0* (`d228-gflg`: stash set,
  exp/lp unchanged, `00316A50` edx=0). Retention ≠ payment.
- EXP-199's `d228-*` asserted exp/lp values survive byte-exact
  (`d228-g1` 150/30, `d228-2g`, `d228-ecap` cap, `d228-lvl` level-4 target)
  driven by real formula inputs instead of retkeys — `oar4` "link" rows give
  `0031B860` the OBJARR presence EXP validation requires.

## Validation

`python check.py` — 360/360, run three times independently, `result.json`
SHA256 `bd903eb43fae93068a3dbda1d1e99f6ff6d101c35c46ac168b2e4c781c5fd93a`
identical each time. New fixtures: `e78e/e70e` (+0x34 dword EXP mult/add),
`e78l/e70l` (+0x2F byte LP mult/add), `memslots` (member map
`glob+0x5A5A+i*2`), `lflag` (`b[020AA2AA]`), `rcx=("guest",N)` row
resolution, `cfml()` direct-entry helper.

**Not claimed:** live-game reachability, initialized-state identity of any
fixture row, or `0020E600` coverage (unreached here — deliberately out of
scope; it feeds other bodies, not these formulas).
