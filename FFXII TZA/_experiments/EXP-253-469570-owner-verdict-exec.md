# EXP-253 — `00469570` owner-verdict arms (`rsi`, `q[+0x10]` gate)

**Status:** complete — **551/551 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `f8606e0f` prefix; 551
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on two extended fixtures; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..252; new `q6own0` case key plants `q[q6s+0]` and
`oar4` spec gains `"ci0"` leaving `q[row+0x10]` null).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

The stat-change notifier's owner resolver `00469570(ecx=tag,
rdx=q[r14], r8=q[r14+8])` resolves the *sending* object row, stores
it in the global owner cell `q[02EBF188]`, and — only when that row
carries client-info at `q[row+0x10]` — consults `002FA3B0`'s distance
gate before `0046AB10` decides whether the dedup ring/notify runs.
This package pins both lookup arms and the no-client-info default.

## Mechanism exercised (all shipped bytes)

`00469570` structure (verified against shipped bytes):

- Desc gate: `q[02EBF018]` → `0020E600(d[desc+0xC])` resolves the
  element row ×3 (`e600`×4 in trace); `b[elem_base + w[desc+8]·tag
  +3] >= 0x80` → `ret 1` (early proceed).
- **rsi arm** (`rdx` carrier): `0031B860(rsi)` hit →
  `q[02EBF188] = row` → `q[row+0x10]` nonnull → second `0031B860` →
  `rbx = q[row+0x10]` → **`002FA3B0(rbx)` decides** (`ret` gates
  `0046AB10`: 0 → `je 0046AC7A` exit; nonzero → ring/insert).
- **rdi arm** (`r8` carrier): identical pair on rdi when rsi==0 or
  the rsi lookup misses/`q[row+0x10]==0` falls through.
- `q[row+0x10]==0` → `mov eax,1` → **proceed without consult**.

New cases:

- **`q6mid-rsi`** (`oar4={2:{}}`, `q6own0=2`): `q[q6s+8]==0` so
  `0046AB10`'s own scan is skipped by `test rcx,rcx; je` — the
  mid-gates never apply when the +8 carrier is null. Resolver's rsi
  arm runs: `b860`×2 on `oar4[2]`'s rec → `q[02EBF188]==row2` →
  `2FA3B0(ci2)` (`l272a0`/`l3590d0`/`l265020`/`l3a1920`/`sqrtf`/
  `cookie` deep chain, all REAL) → nonzero → insert fires.
- **`q6mid-noci`** (`oar4={1:{"ci0":1}}`, `q6own=1`): `0046AB10`'s
  scan hits row1 → gates clear → rdi arm: `b860` →
  `q[02EBF188]==row1` → `q[row1+0x10]==0` → `je 469685` → **ret 1,
  no `2FA3B0` consult** → insert fires anyway. The owner row without
  client-info defaults to proceed.

`q6mid-ok` gained verdict pins: `q[02EBF188]==oar4[1]` row,
`lfa3b0` arg `== q[row+0x10]` (ci).

## Corrections of record (assert-first guesses that shipped bytes overturned)

- `46AB10`'s pre-scan is guarded by `test rcx,rcx; je` — with a null
  `q[r8+8]` carrier no `0031B860` call happens at all (not a
  called-with-0 early-out).
- `q[row+0x10]==0` does **not** call `002FA3B0(0)` — it jumps to the
  `mov eax,1` arm (rdi arm's equivalent), i.e. missing client-info
  means proceed, not veto.

## Not claimed

- `002FA3B0` returning 0 (the veto arm — its distance gate internals
  `l272a0`/`l3590d0`/`l265020`/`l3a1920` ran real but always
  returned nonzero on these fixtures); `00469570`'s
  `b[elem+3]>=0x80` early-proceed arm and desc-null arm;
  `q[02EBF188]` consumers; `005369C0` real; live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- Remaining stub census unchanged (`b3b02a0` ×14,
  `c1ccb20`/`n210ec0` ×9, `d8bf0` ×7, `s181330` ×2, singles…).
