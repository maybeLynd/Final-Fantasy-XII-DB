# EXP-199 — EXP/LP guest-share distribution `00312280` + suppression leaf `00236780` execution

**Status:** complete — **326/326 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`cec2549a190ef20429e85ba30649854621750e5dbe1d81bb6815c57f8ddd20d2`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..198; 300 inherited + 26 new `d228-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Executes the EXP/LP guest-share distribution routine the auto-status contract
scripted:

- `00312280` — guest-slot scan, per-guest EXP/LP award with clamps,
  level-up loop, source-row tail, gauge/position tail.
- `00236780` — EXP-suppression flag leaf (`d[glob+4] >> 0xE & 1`).

Share calculators (`002F8BB0`/`002F90C0`), message post (`00316A50`),
broadcast (`0028FB80`), gauge trio (`00253690`/`00254EE0`/`00469E80`),
position chain (`00319490`/`003180F0`/`00319CA0`), pre/post hooks
(`00317ED0`/`003171C0`/`00317090`), per-guest stat applier `0030C650`,
and the cookie epilogue `00808C40` remain **scripted boundaries** —
share formulas pull the deep `0020E600` machinery tree and are their own
future package.

## `00312280(rcx=peer, rdx=objrow)` — decoded structure

**Head:** `rec = q[rdx+0x698]`; iff `rec != 0 && b[rec+5]==1 && rcx != 0 &&
b[rcx+5]==0` → `00317ED0(rdx)` (scripted). Always `003171C0(rdx)` (scripted).

**Gate:** return iff `rec == 0` OR `b[rec+5] != 1` OR `b[rdx+0xE9A] & 8`
(`d228-null`, `d228-norec`, `d228-b5rec`, `d228-e9a8`).

**Scan arm** iff `(b[rdx+0xE9A] & 5) == 5`, or
`((d[rec+0x64] | d[rec+0x3C]) & 2) && (b[rdx+0xE9A] & 2)`, or
`rcx != 0 && b[rcx+5] == 0` (`d228-gate5`, `d228-gatef2`, `d228-gaterc`).
For `i = 0..8`: `row = 00320AB0(i, 3)` real → `glob + 8 + map*0x1C8` where
`glob = q[02EBF190]` and `map = b[glob+0x5A7E+i*2]` (0xFF → no row). Retained
iff row nonnull AND (`(d[row+0x64] | d[row+0x3C]) & 0x80000003 == 0` OR
`00377C20() != 0`); up to nine rows stashed at `q[022C1740 + j*8]`
(`d228-g1`, `d228-gflg`, `d228-gflg0`, `d228-2g`).

**Per guest** (`row`):
- `ebx = clamp(002F8BB0(row, rec), 0, 999999)` — share formula scripted,
  retkey `s8bb0_ret`.
- `esi = clamp(002F90C0(row, rec), 0, 999)` — retkey `s90c0_ret`.
- If `b[row+0x69] & 0x10` OR `b[row+0x79] & 0x10`: `esi` is consumed — no
  guest LP add, `00316A50` gets edx=0, and `r12 += b[row+0x1C2] * esi * 5`
  feeds the source FP tail (`d228-lp5`: `s54ee0` got 1281 = `(10-2)*3+7+
  5*10*5*5` … accumulated `level*lp*5` term, verified arg-exact).
- `00236780()==0` gate → `d[row+0x18C] = min(d[+0x18C]+ebx, 0x5F5E0FF)`
  (`d228-ecap`, `d228-sup` — suppression flag `d[glob+4]` bit14 clears both
  guest and source EXP).
- `d[row+0x190] = min(d[+0x190]+esi, 0x1869F)` (`d228-lcap`); negative
  scripted shares clamp to 0 (`d228-neg`).
- `00316A50(edx=esi, cl=0xB)` scripted, arg-captured.
- Level-up loop: `ebx = b[row+0x1C2]`; `while 0 < 002F8F20(ebx) <=
  d[row+0x18C]: ebx++` — `002F8F20` real. Then `0030C650(row, ebx, 0)`
  (scripted `c650`, arg-captured). `d228-lvl`: level 2, exp 400 →
  `f8f20(2)=169` and `f8f20(3)=386` pass, `f8f20(4)=736` fails → edx=4,
  exactly 3 `f8f20` evaluations.

**Source tail** (always runs after the guest loop, even with zero guests —
`d228-gate5`/`d228-fp`/`d228-src`):
- `exp = 002F8BB0(0, rec)` clamped [0,999999]; suppressed to 0 when
  `00236780()!=0` (`d228-sup` — `sfb80` edx=0 while r8d=lp stays).
- `lp = 002F90C0(0, rec)` clamped [0,999].
- `0028FB80(d[rec+8], exp, lp)` scripted (`d228-src` arg-verified
  `[0x1234, 77, 88]`).
- FP/gauge: `contrib = (b[rec+0x1C2] - b[rec+0x88]) * d[q[rec+0xE78]+0x30]
  + d[q[rec+0xE70]+0x30] + r12` → `ebp = max(00253690()+contrib, 0)` →
  `00254EE0(ebp)` → `00469E80(ebp - 00253690())`. `d228-fp` verified 36/31;
  `d228-fpneg` verified the `max(...,0)` floor and the 32-bit
  zero-extension of the negative delta (`ecx = 0xFFFFFFFB`).
- Position chain: `00319490(&t)` gate → `003180F0(rec, &u)` gate →
  `00319CA0(&u, &t)` (`d228-pos` fires all three; `d228-pos2` stops after
  `s9490`).
- `00265020(q[rec+0x10], triple)` real; `00317090(rec)` scripted;
  `00808C40` cookie epilogue scripted.

## `00236780()` — suppression leaf (real)

`ret = d[q[02EBF190] + 4] >> 0xE & 1` — reads the same `glob` context block
as the guest scan; `globb={5: 0x40}` sets `d[glob+4]` bit14. (A first-pass
read of the RIP-relative target as `02F02190` was a digit transposition —
emulated `rax` at `00236787` is `glob`.)
`d228-globn` (`glob_null`) faults at `0031BA57` in the `0031B9F0` map read
before `00236780` is reached — shipped null-deref preserved as evidence.

## Corrections landed while scoping

- **Guest table cell:** `00320AB0`/`0031B9F0`/`0031B810` all read
  `q[02EBF190]` — the existing `glob` fixture — not a separate `02ECF190`/
  `02F02190` table. A first-pass `ctxc` fixture resolved rows to the wrong
  base; guest rows are `glob + 8 + (map & 0xFF) * 0x1C8`.
- **Stash base:** `q[022C1740 + j*8]`, not `0x21BB740` (digit-transpose;
  verified by `UC_HOOK_MEM_WRITE`-backed post-state read).
- **`002F8F20` curve** (real, measured by direct execution, not head math):
  L1=51, L2=169, L3=386, L4=736, L5=1254, L6=1979 — an earlier prose table
  (136/265/450) was wrong and inverted the `d228-lvl` expectation.
- **`0030C650` scripted:** a stale `REAL` entry (`lc650`) was shadowed by the
  SCR stub since SCR is consulted first — removed the dead map entry; per-
  guest stat application is a scripted `c650` boundary with arg capture.
- **Source-tail pointers:** `q[rec+0xE78]`/`q[rec+0xE70]` must be mapped;
  `c228` defaults them to zeroed blocks (`e78`/`e70` set the `d[+0x30]`
  contribution).

## Fixtures added (synthetic, disclosed)

`guest={i:{"d","b"}}` — plants a row at `glob+8+map*0x1C8` for `slotmap`
entry `i`, tracked in `self.guests`; `glob_null` zeroes `q[02EBF190]`;
`globb={5:0x40}` sets the suppression bit; `e78`/`e70` plant the source-FP
contribution blocks; `oar4` gained `"link": N` to reuse `guests[N]` as an
object-array row's `q[+0x698]` (retained plumbing; the level-up case no
longer needs it since `0030C650` is scripted); `c228(**kw)` case helper +
`SM_NONE` slotmap constant.

## Still scripted (disclosed)

`00317ED0`, `003171C0`, `00317090`, `002F8BB0`/`002F90C0` (share formulas —
retkey-driven, own package), `00316A50`, `0028FB80`, `00253690`,
`00254EE0`, `00469E80`, `00319490`, `003180F0`, `00319CA0`, `0030C650`,
`00808C40`, plus the EXP-198 scripted set.

## Next package

`003BBD00`/`003284D0` formatter family (CRT closure evaluation), or the
`002F8BB0`/`002F90C0` share-formula family now that their call sites are
pinned. Fallback: drafted EXP-152 spawn-record initialization.
