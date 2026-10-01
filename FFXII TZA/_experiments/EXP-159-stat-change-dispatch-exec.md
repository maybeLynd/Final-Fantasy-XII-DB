---
id: EXP-159
title: "Stat-change dispatcher 30FED0 — watch-mask seeds, per-bit dispatch, walker tail"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp159_check.py
result: 109/109 (stable x3)
---

# EXP-159 — `30FED0` stat-change dispatcher, executed

`0030FED0` is the unconditional tail of `30F690`/`30F340`/`30F5A0` —
called on every touched rec as `30FED0(rec, 0x217)`. 506 insns. It is
the stat-change fan-out: it collects which of the 128 stat bits changed
from three sources and dispatches per-bit handlers.

## Structure (executed)

`30FED0(rec=rcx, notify=edx)` — `r15d = edx | 0x202` throughout:

- **Phase A — descriptor watch-mask**: `q[0x2EBF130]` (FOED) →
  `20E600(d[desc+0xC])` ×2 → row `= w[desc+8]*b[rec+4] + eax2` →
  `d[row+0x50]` watch-bitmask → sets bits in stack bitmap `rsp+0x40`.
- **Phase B — member seed** (`b[rec+5]==1`): `31B860(rec)` owner scan →
  copies `b[owner+0xE80 + bit/8]` bits over 128 iterations into the same
  bitmap.
- **Phase C — field diff**: `b[rec+0x78+i]` XOR snapshot loop writes the
  changed-bit map `rsp+0x50` and cleared-bit map `rsp+0x60`.
- **Phase D — per-bit dispatch** (128 iters): `rsp+0x50` set bit i →
  `30E130(rec, i, 0, r15, 3)`; `rsp+0x60` set bit i →
  `30E130(rec, i, 0, r15, 1)`. `30E130` is scripted (it calls `30FED0`
  back plus `call rax` arms and `3112F0`/`3279B0`).
- **Phase E**: `2FEF30(rec, 0, 0)` — the 735-insn walker, executed real
  (139 insns on the base rec; its `2F8E50`/`2F9180` sub-calls scripted).
- **Phase F — member owner-bit clear** (`b[rec+5]==1`): `31B860` again →
  iterates `d[owner+0xE90]` 32 bits → `30E360(rec, 0, bit, ...)` clears
  per set bit — the owner's flag bitmap drives rec-side clears.

## Executed findings

- **No null guard.** `test rcx,rcx; je` lands at the loop entry
  `0x310071`, not a return — `rcx=0` faults at `0x310080` reading
  `w[0x50]`. Caller-side guard lives in `30F690` (`test rcx,rcx; je`
  before the tail call). Documented via `expect_fault`.
- **Watch-mask dispatch proven**: `rec_b={4:2}` resolves the FOED row
  (`foerow`); `d[foerow+0x50]=0x5` → two `30E130(rec, bit, 0, 0x217)`
  intercepts for bits 0 and 2; `0x80` → one for bit 7.
- **Member path boundary**: `b[rec+5]=1` routes `2FEF30` into a
  member-resolution arm whose stat-row pointer (`rbx`, read as
  `w[rbx+0x24]`/`b[rbx+0x88]`/`b[rbx+0x1C2]`/`d[rbx+0x20]`/`b[rbx+0x26]`)
  is not planted → authentic fault at `0x2FF1FC`. Disclosed.
- Scripted boundaries reached live: `m2f8e50`, `m2f9180`, `m30e130`.

## Cross-package link

`300280` (inside the `3105D0` unlink helper) calls `3008A0` — unlink
deregisters entity ids through the EXP-158 resolver: spawn-bitmap clear
+ `q[0x2EBF190]+4` flag update.

## Real layer added

`30FED0`, `2FEF30` (partial coverage — member arm disclosed),
`861EC0`, `808C40`, `809950`, `31E9A0`/`31E9F0`, `323890`/`3241D0`,
`252FD0`. Scripted: `30E130`, `3112F0`, `3279B0`, `2F8E50`, `2F9180`,
`252E60`, `46AB10` plus the inherited boundary set.

## Boundary disclosure

Fixture recs/descriptor rows/state cell planted; runtime-only pointers
(`q[0x2EBF130]` desc chain, `q[row+8]` bitmap, `q[0x2EBF190]`) disclosed.
`30E130`/`3112F0`/`3279B0`/`2F8E50`/`2F9180`/`252E60`/`46AB10` returns
scripted. The `b[rec+5]==1` member path faults on unplanted member-slot
state — expect_fault, not a promoted claim. MODEL-PROVEN/NATIVE-REPLAY
only.
