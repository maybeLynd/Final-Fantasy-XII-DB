---
id: EXP-155
title: "Stat apply pair 300BC0/300CE0 + 30E060 fraction notify"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp155_check.py
result: 68/68 (stable x3)
---

# EXP-155 — `300BC0`/`300CE0` stat apply pair, executed

The bodies `0030F5A0` (EXP-153) calls to land computed deltas. Both resolve
the `31B860` owner row first, then run the `30B770`+`30B7F0` veto pair unless
`notify & 1`.

## `300BC0(rec, delta, notify)` — HP apply (65i)

```
new  = movsx w[rec+6] + delta
cap  = (b[rec+0x6C] < 0 || b[rec+0x7C] < 0) ? 0
     : (b[rec+0x37] != 0 ? w[rec+0x28] * b[rec+0x37] : w[rec+0x28])
w[rec+6] = clamp(new, 0, cap)
30E060(rec, notify)
```

Executed: basic +50 → 150; +500 → clamped 200; -100 → floor 0; `b6C<0`
gate → forced 0; `b37=3` → cap 300; `notify&1==0` + veto → unchanged.

## `300CE0(rec, delta, notify)` — `w[+0x4C]` gauge apply (117i)

Notify decodes: `r13 = ~(notify>>4)&1` (→ `3283D0` owner msg),
`r15 = ~(notify>>7)&1` (→ `28F1F0` gauge event), `notify&1` skips veto.

- `new = movsx w[+0x4C] + delta`, clamped `0 .. cap` where
  `cap = (b6C<0||b7C<0) ? 0 : w[+0x28]` (no `b37` scale here).
- Owner row present: `r13` → `3283D0(row, delta, delta>0, 1)`;
  `r15` → `28F1F0(d[row+8], old, new, 1)`.
- `delta < 0`: second `30B770`/`30B7F0` veto on the **hi word**.
- `w[+0x4C] = new`.
- **`delta > 0` → `300BC0(rec, delta, notify)`** — heals apply to both
  gauges. Executed: ce0(+30) → w4C 50→80 AND w6 10→40.
- `new < old` → `2FA540(row)` drop notify. Executed.

## `30E060(rec, notify)` — HP-fraction notify (63i)

- `ebx = (w[+0x28] > 0 && b[+0x37] != 0) ? movsx(w6)/movsx(w28) : 0` —
  integer fraction (0 or 1 at these scales).
- `ebp = ~(notify>>1)&1` → `16D6A0(rec, ebx-esi)` — **a literal `ret`
  sink**: a dummied-out notification (dead call, no effect).
- `notify & 0x410 == 0x400` + owner row + fraction changed →
  `3283D0(row, ebx-esi, ebx>esi, 1)` then `b[rec+0x4E] = ebx` (cached).

Executed: fraction 0→1 posts + caches 1; unchanged fraction silent;
1→0 posts with sign 0 and caches 0.

## Correction to the EXP-153 model

`30F5A0` section-2 `computed` is **`b37 ? b37*w28 : w28`** — the same
scale-default-1 cap `300BC0` uses, not plain `b37*w28`. Proven live:
`w28=100, b37=0, w6=0` → section2 delta +50 (after cascade) → `w6=100`.

## Scripted boundaries (disclosed)

`30B770`, `30B7F0` (owner veto pair), `28F1F0` (gauge event post),
`2FA540` (drop/death notify), `2FA3B0` (msg post inner). `3283D0` runs
real into scripted `2FA3B0`. All instrumented; args recorded.

## Fixture disclosures

Same fixture as EXP-154 (`exp155_check.py` derives from it): hand-planted
object array, can-die cells, cascade desc — MODEL-PROVEN elements only;
no live-game reachability claimed.
