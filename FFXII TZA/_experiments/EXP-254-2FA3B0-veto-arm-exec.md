# EXP-254 — `002FA3B0` veto arm inside `00469570`

**Status:** complete — **552/552 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `d58645cb` prefix; 552
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on one extended fixture; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..253; `oar4` spec `trip` key — already present —
drives `002FA3B0`'s distance gate).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## What a player sees

The owner resolver's last word is `002FA3B0` — a 24-unit distance
gate against the camera position `vec3[01EBBB00]`. EXP-253 showed
the consult only runs when the owner row carries client-info
(`q[row+0x10]`); this package exercises its **veto**: an owner whose
client-info vec3 sits ~100 units from camera makes `002FA3B0`
return 0 → `00469570` ret 0 → `0046AB10` takes `je 0046AC7A` — the
report is refused *before* the dedup ring and the broadcast notify.

## Mechanism exercised (all shipped bytes)

- `q6mid-veto` (`oar4={1:{"trip":[100,0,0]}}`, `q6own=1`):
  `0046AB10`'s own `0031B860` scan hits row1 (`q[q6s+8]`=rec) →
  mid-gates clear → `00469570` rdi arm → `0031B860` pair →
  `q[02EBF188]`=row1 → `rbx=q[row+0x10]`=ci → **`002FA3B0(ci)`**:
  `00265020` copies `q[ci+0xB8]` vec3 (`b[ci+3]>>5=1` ∈ {1,3}) →
  `003A1920`/`sqrtf` vs `vec3[01EBBB00]` (zeroed → camera at origin)
  → dist ≈ 100 → `24.0 > dist` false → **ret 0** → `test eax,eax`
  → `je 0046AC7A` → `0046AB10` **ret 0**.

**Distinguishing return identities on the three `0046AB10` exits:**

| path | trigger | `46AB10` ret |
|---|---|---|
| cap `d[r8+0x28]≥0x1FF` | `q6dup-cap` | 0 (nothing ran) |
| mid-gate `d[02089340]&0x3080` / `b[row+4]&0x20` | `q6mid-g3080`/`b20` | **owner row** (rax carried) |
| veto `2FA3B0` ret 0 | `q6mid-veto` | **0** (eax=0 from `test eax`) |

Pins: `q[02EBF188]`==row1 (owner cell still stored before the
consult), `lfa3b0` arg `==` ci, `s5369c0` absent, ring row and
cursor `d[02EBB54C]` untouched, `ret==0`.

## Not claimed

- `002FA3B0`'s `b[obj+3]>>5` rejection arm (zero-vec3 → dist 0 →
  always proceed — the camera-origin degenerate case), the
  `3272A0`-gated camera-cell refresh path (`g272f0&0x10` — existing
  `fa3b0-fl` covers it standalone), exact boundary at dist==24.0
  (`fa3b0-edge` covers it standalone but not through `0046AB10`),
  `q[02EBF188]` consumers, `005369C0` real, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- Remaining stub census unchanged.
