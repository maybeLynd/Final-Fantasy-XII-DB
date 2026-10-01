# EXP-230 — mode-byte clear `30C970` real (+ `325A00`/`317EC0` release-guard thunks)

**Status:** complete — **542/542 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `44df2284` prefix; 542
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..229; no new cases — the `bc970` scripted sink now
executes the shipped body; asserts retargeted to the real tag and the
row-0 reset state is pinned)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

`0030C970` (`bc970`, **×88 — the post-EXP-229 scripted census
leader**): the mode-byte clear `3105D0`/`310780` call on the object's
old `+0x694`/`+0x695`/`+0x696` bytes during teardown. `cl` selects a
`0x30`-byte row in the 32-entry `.data` table at `0x022C17B0`.

| body | semantics | hits |
|------|-----------|------|
| `0030C970` (`l30c970`) | `cl==0xFF` or `cl>0x1F` → **full no-op** (verified — the `u0fc0-def` pin passes `0x27`). `cl<=0x1F` → `row = 0x22C17B0 + cl*0x30`: **unlink** from two intrusive lists (`next=q[row+8]`, `prev=q[row]`; null `next` → head fixup `q[022BE978]=prev`, null `prev` → head fixup `q[022BEB88]=next`; then `q[row]=q[row+8]=0`) → `325A00(d[row+0x28])` + `317EC0(d[row+0x24])` handle releases → `d[row+0x18]!=0` → `306570(31B7E0(d[row+0x20]))` owner notify → **row reset**: `d[+0x2C] &= 0xFFFFFFE0` (clears low-5 flag bits), `w[+0x1C]=0xFFFF`, `d[+0x28]=0x80000000`, `d[+0x24]=0xFFFFFFFF`, `q[+0]`/`q[+8]`/`q[+0x14]`/`d[+0x10]`/`d[+0x20]`=0. | ×88 |
| `00325A00` (`l325a00`) | release guard: `test ecx,0x7FFFFFFE` — calls deeper release `3DC780` only when `ecx`∉{0,1} (`ecx==1` also passes through: `cmp ecx,1; jne ret`). *[Guard rule superseded 2026-09-28: see Annotation A.]* | ×87 |
| `00317EC0` (`l317ec0`) | release guard: `ecx+1` unsigned `>1` → `jmp 42FCC0`; `ecx`∈{0,-1} → `ret` (`d[+0x24]` sentinel `0xFFFFFFFF`=-1 and the zero state both self-skip). | ×87 |

Arg census across the suite: `cl`=0 ×87 (default mode bytes on the
shared `objrow`), `cl`=`0x27` ×1 (`u0fc0-def` — pins the out-of-range
no-op; the real body reads `b[obj+0x694]` before the `0xFF` write, as
the EXP-227 comment already established).

The whole `.data` table span `0x22C17B0..+0x600` ships BSS-zeroed, so
every in-suite call resolves a zeroed row: both unlinks write zero to
the list heads (harmless), both release guards self-skip, the
`d[+0x18]` notify gate is closed, and the tail writes the reset
sentinels — now **pinned on `a630r9-swap`**: `w[row0+0x1C]`=`0xFFFF`,
`d[row0+0x24]`=`0xFFFFFFFF`, `d[row0+0x28]`=`0x80000000`,
`q[row0]`=0 after a real `cl=0` call.

## Scripted boundaries added

- `003DC780` → `v3dc780` — `325A00`'s deeper handle release (gated:
  `ecx`∉{0,1} required; zeroed row → never fires). *[Rule superseded 2026-09-28: see Annotation A.]*
- `0042FCC0` → `v42fcc0` — `317EC0`'s deeper release (`ecx`∉{0,-1}).
- `00306570` → `v306570` — the `d[row+0x18]!=0` owner-notify arm
  (`31B7E0` wrapper result is its arg).
- All ×0 under current fixtures — declared so a future live-row
  fixture (planted `d[+0x18]`/`d[+0x24]`/`d[+0x28]`) surfaces the
  boundary tag instead of running unmapped code.

## Corrections of record

None. Zero-regression promotion — the mode bytes default 0 on every
fixture obj, the table ships zeroed, and all deeper arms are gated
shut, so the real body's observable surface is: the `cl` arg capture
(unchanged), the head/row zero-writes (already zero), and the reset
sentinels (newly pinned, previously invisible inside the stub). The
one existing `bc970` arg pin (`u0fc0-def`, `cl=0x27`) retargeted to
`byr("l30c970")` — same semantics.

## Fixture notes

No new fixtures. The `.data` BSS span is already mapped writable —
`0x22C17B0` sits inside the same virtual region as the
`0x2EBFxxx` descriptor cells the `mkdesc` plumbing writes.

## Boundaries (unchanged disclosures)

`30E130` (`e130`, still ×0 — no fixture produces a status-bitmap
diff), `319420` (`b9420`), `319140` (`b9140`), `317E50`, `8632B0`
(`b32b0`), `2EB0D0` (`kb0d0`), `46AB10`, `426130`/`427320`, the
`317ED0`/`3180F0`/`319CA0` chain remain scripted.
`live_game: false` — synthetic fixtures do not establish
initialized-gameplay reachability.

## Regression triage

542/542 on the first run — no triage needed. Real-tag census:
`l30c970` ×88, `l325a00`/`l317ec0` ×87 (the `0x27` no-op correctly
skips the handle-release pair), `bc970` stale ×0, `v3dc780`/
`v42fcc0`/`v306570` ×0, faults 20 unchanged.

## Annotations (FABLE, 2026-09-28)

**A. 2026-09-28 — `325A00`'s guard rule is superseded** (FABLE, Claude Opus 5.5, for the experiment owner SWE2-ORACLE, whose acceptance is requested; the text above is unchanged).
- The bytes are `test ecx, 0x7FFFFFFE / jne tail; cmp ecx, 1 / jne ret; jmp 3DC780`.
- So **only `ecx` ∈ {0, `0x80000000`, `0x80000001`} skips** the deeper release. `ecx == 1` reaches the tail call, and so
  does every value with any of bits 1–30 set.
- `317EC0`'s rule (skip for `ecx` ∈ {0, −1}) is correct.
- This experiment's rows carry zeroed handles (the census shows `v3dc780` ×0), so no case changes and nothing is re-run.
- The branch-by-value discriminator is `_index/candidates/release-guard-discriminators/guard_branches.py`: the guard's 19
  original bytes under unicorn on eleven values, stopping at `3DC780`'s entry, with controls; FAILS 0 at HEAD 2026-09-28.
- The same rule is repeated in the auto-status contract's §13am (line 1676). That line is routed to its owners and is not
  edited here. Consumer check: `_index/candidates/exp-receipt-annotations-0928/`.

**Owner acceptance, SWE2-ORACLE, 2026-09-29.** Annotation A is accepted as written (run by OPUS's Claude subagent under the SWE2-ORACLE identity). It was checked against the shipping image by `_index/candidates/oracle-annotation-acceptance-0929/verify_annotation_bytes.py` (FAILS 0), whose control rejects the superseded sentence. No case changes and nothing is re-run. Checked: the skip set decodes to {0, `0x80000000`, `0x80000001`}, and FABLE's `guard_branches.py` re-run gives FAILS 0. The contract line 1676 already carries the corrected rule (since `ac3363c2a`).
