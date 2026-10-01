# EXP-255 — `00469570` early arms (`b[elem+3]≥0x80`, desc-null) + direct probes

**Status:** complete — **555/555 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `a1c54544` prefix; 555
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on three extended fixtures; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..254; `q6desc` gains `"b3"` = `b[elemb+3]` class
byte, new `q6arg` case key hands an `oar4` rec to register args for
direct-entry resolver probes).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes)

- **`q6mid-g80`** (`q6desc={"elf":1,"b3":0x80}`, `q6own=1`):
  `0046AB10`'s scan hits (`b860`×1) → mid-gates clear → `00469570`'s
  desc gate resolves `0020E600(d[desc+0xC])` → element `elemb`;
  `b[elemb+3]>=0x80` → `jae 00469685` → **ret 1 before any owner
  lookup** — `q[02EBF188]` stays null, `002FA3B0` never consulted;
  `0046AB10` proceeds straight to the scan arm → insert + notify.
  `e600`×6 total (4 in the resolver gate + 2 in `0046AB10`'s own
  `0046AB83` element resolve).
- **`q69570-null`** (direct `entry=0x469570`, `ecx=0x1234`, `rdx=0`,
  `r8`=oar4[1] rec): `q[02EBF018]`==0 → `je 469603` — desc-null is
  **not** an early ret; it falls straight to the owner arms.
  rdi arm: `b860`×2 → `q[02EBF188]`=row1 → `2FA3B0(ci1)` →
  **ret 1** (the `2FA3B0` verdict, near-origin → nonzero).
- **`q69570-rsi`** (direct, `edx`=oar4[2] rec, `r8=0`): rsi arm
  fires first — `b860`×2 on rec2 → `q[02EBF188]`=row2 →
  `2FA3B0(ci2)` → ret 1; the rdi arm is unreachable once the rsi
  consult returns.

`00469570` semantic summary now pinned end to end:

```
desc-null || elem-null      -> owner arms still run
b[elem + w[desc+8]*tag +3] >= 0x80 -> ret 1 (no owner consult)
lookup miss / q[row+0x10]==0 -> ret 1 (proceed, no veto)
q[row+0x10] nonnull         -> ret = 2FA3B0(ci) verdict
```

`0046AB10` treats only `ret==0` as refuse; every `ret 1` path
proceeds to the ring.

## Not claimed

- `00469570`'s desc-nonnull + `q[row+0x10]==0` rsi→rdi fallthrough
  (rsi arm null-ci falls *to the rdi arm*, not to ret 1 — the two
  carriers were not both planted on a null-ci row in this package);
  `002FA3B0`'s `b[obj+3]>>5` rejection arm; `q[02EBF188]` consumers;
  `005369C0` real; live-game reachability — `NATIVE-REPLAY`,
  `live_game: false`.
- Remaining stub census unchanged.
