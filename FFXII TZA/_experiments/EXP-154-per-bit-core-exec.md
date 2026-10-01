---
id: EXP-154
title: "Per-bit stat core 0030E360 — six-arm flag mutation, cascade, handler dispatch"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp154_check.py
result: 53/53 (stable x3)
---

# EXP-154 — `0030E360` per-bit stat core, executed

`0030E360` is the per-bit engine behind `0030F690`'s dirty-mask dispatch
(EXP-153). It is a 342-instruction body with a stack cookie, self-recursion,
two `call rax` handler selections, and **two embedded jump tables** — one
selecting the flag-mutation arm, one dispatching a per-bit follow-on arm.

## Signature

`30E360(rcx=rec, rdx=src, r8b=bit, r9=arg4, [rsp+0x20]=arg5, [rsp+0x28]=arg6, [rsp+0x30]=arg7)`

`30F690` invokes `(rec, 0, bit, 0, 0, 0x217, 0)`. Direct-entry fixture:
retaddr@rsp, stack args at `rsp+0x28/+0x30/+0x38` (entry rsp sits 8 above a
real call's).

## Jump table 1 — six flag arms (`sel`@`0x30E88C`, arg7)

| arg7 | op | dword | edge gate |
|------|----|-------|-----------|
| 0 | clear bit | `d[rec+0x64]` | bail if already clear |
| 1 | clear bit | `d[rec+0x3C]` | bail if already clear |
| 2 | clear bit | `d[rec+0x38]` | bail if already clear |
| 3 | set bit   | `d[rec+0x64]` | bail if set in `+0x64` **or `+0x38`** |
| 4 | set bit   | `d[rec+0x3C]` | bail if already set |
| 5 | set bit   | `d[rec+0x38]` | bail if already set |

All six executed and verified (set/clear/conflict/no-op).

## Post-transition block — gated `al & 0x4C` (arms 0 and 3 only)

On a successful transition for arms 0/3 (the `+0x64` stat dword):

- `d[rec+0xBC + bit*4]` = r9 — or `387730(bit, rec)` when r9 < 0
  (`r8==2` returns `0xB`; else returns the saved rsi value).
- `w[rec+0x13C + bit*2]` = arg5 — or `3876D0(bit)` when the arg5 **dword**
  is negative. `3876D0` resolves via the `0x02EBF118` descriptor:
  `row = elemb + d[desc+0xC] + bit*w[desc+8]` (two `20E600` hops), then
  `b[row+9] * d[0x1DFE0B4] * 0x1E` — multiplier cell verified live
  (planted 2 → 0xB4; image default 1 → 0x5A).

## Handler pair A — `call rax` at `0x30E60E` (after 0x148 memset)

`edi = d[rec+0x44]` (= arg7 ∈ {3,4}) selects:

- `386A50(blk, src, bit)` — `3848E0(blk)` block reset, then clears
  `d[blk+0x2C]` bit 0.
- `386A70(blk, src, bit)` — `3848E0(blk)`, then iff `bit == 0x1C` and
  `d[src+0x48] != 0`: `d[blk+0x2C] |= 0x108`,
  `d[blk+0x24] = (d[src+0x48]+1) >> 1`. Effects land in the stack block.

`3848E0` = 0x148-byte stat-block reset: `memset(blk+8, 0x140)` + sentinel
fields (`d[+0x38]=-1`, `w[+0x30/0x11C..]`=0xFFFF, `d[+0x2C]|=1`, …).

## Handler pair C — `call rax` at `0x30E727` (gated `d[+0x60]`)

`d[rsp+0x60] = ~(arg6>>1) & 1`; when set, `edi ? 46A800 : 16D6A0`:

- `46A800(rec, bit)` — if scripted `2FA390` passes: `bit==1 → 46AB10(rec,0x12)`,
  `bit==0x1F → 46AB10(rec,0x11)`.
- `16D6A0` — a bare `ret` (no-op sink for the non-mode arm).

## Jump table 2 — per-bit arm dispatch (`idx`@`0x30E8C4`, `off`@`0x30E8A4`)

Reached when the `31B860` owner row (`rbx`) is nonzero and bit ≤ 0x1F:

| bit | arm | action |
|-----|-----|--------|
| 0 | `0x30E80A` | non-mode: `301140(rbx)`; mode: `300FC0(rbx,0)` + `312280(src,rbx)` |
| 1 | `0x30E850` | non-mode: `301140`; mode: `3299B0(rbx,0x200C)` + `300FC0` + `312280` |
| 2 | `0x30E7DD` | `b[rbx+0xE9A]` bit-1 write (gated `b[src+5]==0`) |
| 4 | `0x30E75B` | `3299B0(rbx, 0x2001)` |
| 5, 0x1B | `0x30E770` | `d[rbx]` bt 0x18 + `w[+0x714]`/`b[+0x6B4]` checks → `300140(rbx)` + `307D10(rbx)` |
| 8 | `0x30E7B3` | `b[rbx+0xE9A]` bit-0 write |
| 0x1F | `0x30E85E` | non-mode: `301140`; mode: `3299B0(rbx,0x200E)` + `300FC0` + `312280` |
| other | `0x30E816` | join |

Arm bodies `301140`/`312280`/`3299B0`/`300140`/`307D10`/`3284D0` remain
scripted boundaries (recorded at their call sites).

## arg6 notify mask decode

- `arg6 & 1` — skip both owner checks (`30B9B0`; plus `30B8E0` when mode).
- `d[rsp+0x5C] = ~(arg6>>4) & 1` — notify/scan gate (with `edi`+`rbx` → `3284D0`).
- `d[rsp+0x60] = ~(arg6>>1) & 1` — gates handler pair C.
- `arg6` bit 9 — skips the tail `30FED0(rsi, arg6)`.

`0x217` = owner-checks skipped, both notify gates cleared, bit9 clear
(fed0 fires).

## Cascade — descriptor `0x02EBF118`

`edi` (mode) path resolves `row = elemb + d[desc+0xC] + bit*w[desc+8]`;
`d[row+0xC]` is a follow-on bitmask iterated `bt` per bit → recursive
`30E360(rec, src, followbit, 0, 0, arg6|bit9, 0)` — i.e. arm-0 clears on
`d[rec+0x64]` with the fed0 tail suppressed. Executed: arm3 set bit2 while a
planted cascade mask recursively cleared pre-set bit4.

## Scripted boundaries (disclosed)

`30B9B0`, `30B8E0` (owner checks), `300FC0` (unlink), `3112F0` (blk notify),
`2FA390`, `46AB10` (46A800 inners), `301140`, `312280`, `3299B0`, `300140`,
`307D10`, `3284D0` (jt2 arm bodies) — all instrumented, args recorded.
`30FED0` stays scripted per the EXP-148/152/153 precedent.

## Fixture disclosures (MODEL-PROVEN elements)

Planted cells: `0x02EBF118` cascade desc + `0x70000` row region,
`0x1DFE0B4` multiplier, `0x0208E6A0`/`0x0208E688` object array (owner rows),
`0x02ADD100` can-die table + `0x21654C4` index, `0x0208D320/0x208D324`
f690 mask gates, `0x01F83530` element base — plus the whole EXP-152/153
fixture set. All hand-planted; no live-game reachability claimed.
