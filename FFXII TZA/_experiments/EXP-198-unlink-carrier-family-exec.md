# EXP-198 — Unlink-carrier family `00300FC0`/`00301140` + dispatch thunk `0024FE30` execution

**Status:** complete — **300/300 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `ad86cdae834dd99da0572f34346623773a10e6b08ede62f3ca65b6f7e10f2d7f`), zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..197; 271 inherited + 29 new `u0fc0-*`/`l01140-*`/`l4fe30-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Executes the shared unlink-carrier family the auto-status contract scripted:

- `00300FC0` — detach/unlink carrier: `edx==0` fast path vs full teardown.
- `00301140` — full slot-release carrier (inlines the `00300140` unlink-mark
  sequence plus a complete field reset).
- `0024FE30` — id→sub query dispatch thunk (kind nibble → three scan tables).
- Promoted leaf/helper callees: `002372E0`, `00237260`, `002373C0`,
  `003135C0`, `003272E0`, `003219D0`, `003001D0`, `00310780`, `003138D0`,
  `002ED180`, `0026A330`, `0035C8A0`, `002E9600`, `002E8060`, `00319E30`,
  `003125E0`, `0026DC60`, `0031B7E0`, `002FD0C0`, `003B2830`, `003B1260`.

**Scope corrections while scoping** (recorded because they reverse earlier
labels): `0024FE30` is a 0x24-byte dispatch thunk — the "~950-body carrier"
figure covered its callee tree, not the thunk; `00312280` is an EXP/LP
guest-share distribution routine, **not** part of the unlink family — split
out and deferred to EXP-199; `00300FC0`'s context table is `q[02EBF190]` (the
existing `glob` fixture), not `02BCF190`/`02ECF190`.

## `00300FC0(obj, edx)` — detach/unlink carrier

**Fast path** (`u0fc0-fast`): `edx==0` AND `q[obj+0x698]` nonnull AND
`b[rec+5]==0` AND `b[rec+4]-0x1B <= 0xC` (b4 ∈ [0x1B,0x27]) →
`003105D0(obj)` (scripted) then tail `jmp 003138D0` with `ecx=0`. No flag
writes on this path.

**Full path** (`u0fc0-def`, `edx==0` + `b5!=0` — also taken for `edx!=0`,
`u0fc0-m1`): `00310780(obj)` → `002ED180(d[obj+8])` → `d[obj+4] &= ~4` →
`q[obj] &= 0xFFFFFFFDFFE7FFFD` → `0026DAC0(q[obj+0x10])` → `0026A330(ent)` →
`003219D0(b[rec+4], 0, 0, 1)` → then the slot predicates set
`d[02089340]`:

| predicate | bit | + `003001D0` + `0035C8A0(arg)` → `d[022C83E8]` post |
|---|---|---|
| `002372E0()`≠0 | `0x400` | `35C8A0(0xB)` → `|=2` + `00254850(1)`; tail `jmp 0023B040` |
| `00237260()`≠0 | `0x200` | `35C8A0(0x18)` → `|=1` + `00254940(1)`; tail `jmp 0023B040` |
| `002373C0()`≠0 | `0x800` | continues to `003272E0` check below |
| `003272E0()`==`d[obj+8]` | `0x100` | `35C8A0(0x17)` → `|=0x10` + `002548F0(1)` |

The `0x400`/`0x200` arms **tail-jump to `0023B040`**, skipping the lower
predicates. The `edx==0` tail then runs: `0030D9A0()==1` AND
`0031B770(b[glob+0x5AD5])==obj` → `003138D0(0)` + `0023B040()` (`u0fc0-mtail`
drives it via `slothit` so `31B770` resolves to the carrier row).

`u0fc0-norec` (`q[obj+0x698]=0`, edx=0): `test rcx,rcx; je` bypasses the fast
path, then the full path derefs `b[rax+4]` at `0030105A` — fault on `rax=0`.
**No null guard on the second read** — the fast-path null check does not
protect the shared tail.

## `00310780(obj)` — detach bookkeeping (real)

- Early out on `rcx==0` or `q[obj+0x698]==0`.
- `0031B7E0(d[obj+0x710])` → contributor row; iff nonnull AND `q[obj]` bit22
  ~~set~~ **clear** (`003107BE bt rcx,0x16` / `003107C3 jb` skips when set) *(corrected 2026-10-03, SWE2-ORACLE, on ASTRA's SPEC-accepted `uq147-ko-release-partition` - review `auditspec-review-astra-uq147-ko-release-partition-1003`; record `swe2oracle-ko-consumers-1003`)* AND `d[row2+0xEA4]` has bit `1 << b[obj+0xEA9]`: `b[row2+0xEA8]--`,
  `d[row2+0xEA4] &= ~bit`, then `00313B30(obj,row2)` + `002FEAD0(row2)`
  (scripted boundaries, arg-captured).
- Then `00308270(obj)` (scripted), `q[obj] &= 0xFFFFFFFFEFFFFFDF` (clears
  `0x10000020` in the low dword — folds with `00300FC0`'s own masks to the
  observed `q[obj] = 0xFFFFFFF9EFE7FFDD` on all-ones),
  `0030C970(b[obj+0x694])` then `b[obj+0x694] = 0xFF`,
  `00319420(&obj+0x6B0)`, `00319140(obj, 1)`, and `00317E50` iff
  `w[obj+0x714] == 0x414E`.

## `003138D0(arg)` — mode-1 word toggle (real)

`0030D9A0()==1` gate (else immediate ret) → `0031B8C0(mode+2=3)` → row →
bail iff (`d[row]` bit14 && `w[row+0xBA0]==0x113`) OR `w[row+0x714]==0x113` →
`0031B7E0(d[row+8])` twice → `00311CF0(rdi, d[row+8], 0, 0x113, [rsp]=0)`
when rdi nonnull → **`w[glob+0x5AD0] ^= (w[glob+0x5AD0] ^ arg) & 1`** — arg
is `ecx` at the tail (0 for both `00300FC0` call sites), so the effective
write is `w ^= w & 1`: bit0 cleared, other bits preserved. `w=3 → 2` verified
(`u0fc0-fastt`, `u0fc0-mtail`).

**`0030D9A0()` mode map** (drives the gate): `d[glob+0x5B04]` bit3→5,
bit2→4, `00377C20()`≠0→3, bit1→2, bit0→1, else 0.

## `003219D0(id, edx, r8, r9)` — OBJARR capability scan (real)

Iterates `00236850`-count rows via `00236820`; per row: `q[row+0x698]` rec
nonnull, `b[rec+5]==1`, `row != r8`, `q[row+0x6A0]` cap block nonnull, then
`00322C50(2, id)` — the **kind-2 bound is `d[FOED+4]`** (the foe-table
descriptor `q[02EBF130]` — same cell the foe pipeline uses; my initial
`capd` fixture at `02ECF130` was wrong, corrected to reuse `foed`) →
`b[cap+0x1A+id] > 0` → `r8==0` arm: `00321850(row, id&0xFF, edx, r9)`
(scripted, arg-captured: `u0fc0-caps` verified `[row1, 0x21, 0, 1]`);
`r8!=0` arm scans the `d[row+0xBC4]`-count `+0xBC8` entry table for
`q[r8+0x10]` before calling.

## `002372E0`/`00237260`/`002373C0` — member-slot predicates (real)

- `002372E0`: for i<4, `0031B810(i)` → `002367A0(map)` row; each hit sets the
  running flag, disqualified iff rec `b5!=0`→flags-check arm or
  `b4<=6 && (d64|d3C)&0x80000003==0` → ret 0; pending recs pass through
  `00313F60` (scripted, ret 0 keeps). Loop 2: `00320AB0(i,3)` class-3 map
  rows (`b[glob+0x5A7E+i*2]`, `0xFF`→null) with a clean-rec disqualifier.
  Ret 1 = a live member row still occupies the scanned slots
  (`u0fc0-s400` drives `edi=1` via `oar4` row2 `id=2` + `recd{0x64:1}`
  pending + `00313F60`→0).
- `00237260`: same `0031B810` loop, rec arms differ — `b5!=0` or
  `b4∉[7,0x19]` fall to the flags check (`==0` → ret 0); a hit whose rec is
  `b5==0 && b4∈[7,0x19]` passes → ret 1 (`u0fc0-s200`: `globb[0x5A5A]=7`,
  `oar4` row2 `id=7` → `w[rec+4]==7` match).
- `002373C0`: mode-1 busy check — `003135C0` + `0031B770`/`00236850`-style
  scan (`u0fc0-s800`).

## `00301140(obj)` — full slot-release carrier (real)

Bail iff `(d[rec+0x64] | d[rec+0x3C]) & 0x80000003` — the record is
pending/scripted-busy (`l01140-bail`: only `d[+0x748]` untouched-check;
no release calls). Otherwise, in order:

1. `002E9600(obj)`; `q[obj]` bit26 set → `00311F70` (scripted — `l01140-f70`
   arg-captures `(0, obj, 0)`).
2. `00238BF0(obj)` (scripted), `003105D0(obj)` (scripted).
3. Unlink-mark inline: clears `q[+0x6F8]`, `d[+0x748]`, `d[+0x770]`,
   `q[+0x750]`, `d[+0x74C]`; `d[+0x788] &= ~0x400`; `d[+0x6B0] &= ~2`;
   `q[obj] |= 0x1000000`; sentinel-gated `q[obj]` bit14 clear
   (`w[+0xBA0]==0x113` keeps it — `l01140-sent`/`sentc`);
   `d[obj+4] |= 0x200000` then `&= ~4`.
4. `002EACD0(d[obj+8], 1, &obj+8, 0x7B)` → `003B02A0(0, &obj+8, 1, 0x7B)`
   (scripted, arg-captured).
5. `002E8060(q[obj+0x10])`; string select `q[obj+0x6E8]` =
   `0x1EEC3C0` (b[rec+5]==0) / `0x1EEC410` (b5!=0 — `l01140-strn`);
   `d[obj+0xDCC] = 0`; `d[obj+0x74] = -1`; `002ECF10(ent)` (scripted).
6. `003299B0(obj, 0x200D)` **real** (EXP-197 body — node stamp +
   `d[obj+0x5C]=0x200D`, `002EB0D0` kick observed).
7. `00319E30(d[obj+0x74])`.
8. `d[obj+0xDD0] = 0032A150() − int(f[01DFE0B8](=1.0) × f[01CEBCAC](=-30.0)) × 5`
   — `0032A150` is a pure accessor returning `d[0208D45C]` (correction: the
   cell is `0x208D45C`, not `0x208B45C`; `imgd` fixture targets it).
   With count=1000 → `1000 − (−150)` = **1150** (`l01140-rel`).
9. `003125E0(obj)` → `0026DC60(ent, ret==0)` → `jmp 002EBB80` (scripted,
   arg-captured).

`l01140-norec` (`q[obj+0x698]=0`): faults at `00301150` reading
`d[rax+0x64]` on `rax=0` — the flags gate derefs the record before any null
check. **No null-record tolerance on entry.**

## `003125E0(obj)` — flag-word composer (real)

`d[obj]` bit11→out bit1, bit10→out bit2, bit9→out bit3; `d[obj+4]` bit2→out
bit5; `d[q[obj+0x6A0]]` capability dword: bit4 (`0x10`)→out bit6, bit3
(`0x8`)→out bit7; plus global-mode contributions.

## `0024FE30(ecx=id, edx=sub)` — dispatch thunk (real)

`kind = (ecx >> 0x1C) & 0xF` → `1`→`002FD0C0`, `7`→`003B2830`,
`5`/`6`/`9`→`003B1260`, else `ret 0`. Dispatch is unconditional on `edx` —
`002FD0C0` handles `edx==0` internally (no lock/query observed at `edx=0`,
`l4fe30-n1d0`).

Targets (all real): static `.data` scans — `002FD0C0` walks `02EC32E0`
stride-0x38 entries matching `d[entry]==id`; `003B1260` walks `02EBEC00`
stride-0x30; `003B2830` walks `02EBE5E0` stride-0x30 (multi-slot match on
`d[entry]==id`, first-match wins). Match → `0036C1D0(8, 0xA)` lock →
`0024FE70(entry, sub)` scripted query → `0036C140` unlock → ret 1
(`l4fe30-n1`, `n5`, `n7`; miss → 0, `n1m`/`n6`/`n9`). `003B2830` additionally
writes `w[entry+0x378] = 3` on the hit path (`l4fe30-n7`).

All three scan tables are **zero-initialized BSS** in the shipped image —
positive results require the `imgd`/`imgq` fixtures; the shipped-default
empty-table path is what `l4fe30-n1m`/`n6`/`n9` measure.

## Fixtures added (synthetic, disclosed)

`imgd`/`imgq`/`imgb` → direct image-cell writes (string values resolve
against `self.*` attrs for planted pointers); `oar4` extended with `recb`/
`recd`/`cap` (per-row `q[+0x6A0]` capability block); `capd` was dropped —
`00322C50` kind-2 reuses the existing `foed` descriptor (`q[02EBF130]`).
`b8c0_ret` (0031B8C0 scripted return) resolves `"objrow"`.

## Still scripted (disclosed)

`003105D0`, `00238BF0`, `00311F70`, `0023B040`, `002ECF10`, `002EBB80`,
`0031B8C0`/`00311CF0`/`00313B30`/`002FEAD0`, `00308270`/`0030C970`/
`00319420`/`00319140`/`00317E50`, `00321850`, `00327200`, `002E9780`,
`0026D6F0`, `003E6B40`, `00254850`/`002548F0`/`00254940`, `0036C1D0`/
`0036C140`, `0024FE70`, `00426FA0`, `003B0770`, `002E9BB0`, `002EC5B0`,
`003BBD00`/`003284D0` formatter family (CRT closure),
`00312280` (EXP/LP share — EXP-199 scope), `002EB0D0`, `00210EC0`,
`001CCB20`, CRT/import thunks.

## Harness mechanics corrected while landing

- `on_code` never traces `self.entry` — the entry function's tag never
  appears in `w.trace` (assert on post-state, not entry tag).
- `w.objent` exists only under `objlink` — case-group preambles must guard
  (`w.objent if w.objrow else 0`).
- RIP-relative constants verified by emulation, not head math — two
  digit-transposed cells (`0x208B45C`→`0x208D45C`, `0x2ECF130`→`0x2EBF130`)
  produced wrong fixtures until a `UC_HOOK_MEM_READ` trace showed the true
  access addresses.
