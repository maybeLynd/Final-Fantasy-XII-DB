# EXP-252 — `0046AB10` owner-scan hit + mid-gate exits

**Status:** complete — **549/549 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `148a3c80` prefix; 549
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on three extended fixtures; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..251; new `q6own` case key plants `q[q6s+8]` as an
`oar4` row's linked rec so the already-REAL `0031B860` owner scan
hits).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

`0046AB10` is the stat-change notifier's core: before it even asks
"was this `{tag, payload}` reported recently?" it asks "who owns this
notification?" — `0031B860` scans the object array for a row whose
`q[+0x698]` matches `q[r8+8]`. EXP-249 covered the dedup ring; every
prior case left `q[r8+8]==0` so the scan never ran. This package
plants a live owner row and executes **both previously unreachable
mid-gate exits plus the pass-through**.

## Mechanism exercised (all shipped bytes)

`0031B860(rdi)` (REAL since EXP-192 — `rcx==0` early-out, else
`00236850()` row count → `00236820(i)` rows → `q[row+0x698]==rdi`
→ ret row). New `q6own` fixture writes `q[q6s+8]` =
`oar4[slot]`'s linked rec `ri`, making the scan hit row
`oarr+slot*0xF50`. Then `0046AB10` runs, in order:

- **`q6mid-g3080`** (`owngl=0x3080`): `test dword ptr [02089340],
  0x3080` → `jne 0046AC7A` — first mid-gate exit. Resolver
  `00469570`, ring scan, and `s5369c0` never run.
- **`q6mid-b20`** (`oar4` row `flags` qword byte 4 = `0x20`):
  `test byte ptr [rax+4], 0x20` → `jne 0046AC7A` — second
  mid-gate exit, same suppression.
- **`q6mid-ok`** (both clear): `00469570` runs — its own
  `0031B860` pair (`q[r14]`=0 skipped-inside, `q[r14+8]`=ri hits)
  executes — then the dedup insert arm: `w[ring]==0x1234`,
  `q[ring+8]==payload`, cursor `0→1`, `s5369c0(q6pay, 0x1234,
  q6s)` fires.

## Correction of record

The gate exits do **not** return 0: `jne 0046AC7A` lands in the
epilogue with `rax` still holding `0031B860`'s return — the suite
observed `ret == oar4[1][0]` (the owner row). Pinned as such; the
old `eax==0` guess was replaced, not relaxed (it strengthens the
assertion to an exact shipped identity).

Pins on `q6mid-g3080`/`q6mid-b20`: `b860` rargs arg `==` the planted
rec, `l69570` absent, `s5369c0` absent, ring row and cursor
`d[02EBB54C]` untouched, `ret==row`. On `q6mid-ok`: `b860 ×3`
(`0046AB10` + `00469570`'s two lookups), `l69570 ×1` `ecx==0x1234`,
`s5369c0 ×1`, `w[02EBB560]==0x1234`, `d[02EBB54C]==1`, `ret==0`.

## Not claimed

- `00469570`'s hit arm semantics (it runs inside `q6mid-ok` but its
  internal decision is only observed through the insert proceeding —
  the two lookups both executing is recorded, their verdict path is
  not pinned separately).
- `0031B860`'s `rcx==0` early-out (runs silently inside `00469570`
  on `q6mid-ok`, not separately pinned) and scan-miss arm.
- `005369C0` real body (still a scripted boundary ×15), the
  `002EBB560` ring's non-zero-cursor wrap, `d[01DFE0B4]!=1`
  window coefficient, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- Remaining stub census unchanged (`b3b02a0` ×14,
  `c1ccb20`/`n210ec0` ×9, `d8bf0` ×7, `s181330` ×2, singles…).
