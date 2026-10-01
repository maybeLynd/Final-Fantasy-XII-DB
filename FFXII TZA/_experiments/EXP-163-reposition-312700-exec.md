---
id: EXP-163
title: "311F70 reposition helper + 312700 wrapper — last scripted mainline callees of 301140 promoted"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp163_check.py
result: 131/131 (stable x3)
---

# EXP-163 — `311F70`/`312700`, executed

Two remaining scripted callees on the `301140` despawn path promoted
to real. `312700` turns out to be a trivial wrapper; `311F70` is the
105-insn reposition/transform helper gated on `d[rec]` bit `0x1A`.

## `312700(rec)` — executed semantics

12-insn wrapper: `3125E0(rec)` → `26DC60(q[rec+0x10], eax==0)` →
`2EBB80`. The 246-insn jump-table body at `0x312730` is a **separate
sibling** — a `0x4000..0x4035` opcode-range dispatcher (37-way
`jmp rcx` through `rip-0x1f27b1` tables), not part of `312700`.
Verified: `t2700-wrap` tags `u3125e0 → u26dc60 → u2ebb80`.

## `311F70(mode=rcx, rec=rdx, arg3=r8)` — executed semantics

- `30D9A0(rec)` — state-cell code (real; reads
  `d[q[0x2EBF190]+0x5B04]`).
- `336E40(&rsp+0x40, eax==1)` — fills a transform out-struct on the
  caller frame. 346i — scripted boundary with a fill hook
  (`n336_fill`) that writes caller `rsp+0x60..+0x78` through the
  pushed-return adjustment.
- `265020(q[rec+0x10], &x,&y,&z)` — reads the object's current
  position into stack floats.
- `ucomiss` ×3 vs the struct's `+0x60/64/68` floats — **any
  difference or unordered (NaN) →** `263F40(obj)` →
  `26B0C0(handle, x,y,z)` position write. Both directions proven:
  zero-fill → equal → no write; `0xCD`-garbage fill → unordered →
  write (`t1f70-nofill`); nonzero fill → write (`t1f70-fill`).
- `movups [rec+0xD0]` and `[rec+0xE0]` ← `{pos.x,pos.y,pos.z,pad}`
  (the stack `rsp+0x30` quad) — orientation/state vector write.
- `392170(q[rec+0x10])`.
- Member arm: `arg3!=0 && b[objrow+5]==1` → `movups
  [q[rec+0x6A0]+0x50]` ← same quad (proven: `d[6a0+0x50]` = fill[0]
  = `9.0f` = `0x41100000`).
- `q[rec] |= 0x4000000` — the bit26 flag (proven set on base).
- `d[rec+0x15C]` / `d[rec+0x160]` ← scalar `d[rsp+0x70]` from the
  struct (proven `5.0f` = `0x40A00000` with fill[4]).
- `263F40(obj)` → `26A0D0(handle, float)`; `26B620` → `26B6A0`;
  `808C40` cookie check — all real.

## Proven

- `t1f70-base`: equal-compare path — `u30d9a0`, `m336e40`,
  `t265020`, `t392170`, `q[rec]|0x4000000`, no `26B0C0`.
- `t1f70-nofill`: `0xCD` stack garbage → `ucomiss` parity → write
  arm fires (authentic NaN-unordered branch).
- `t1f70-fill`: nonzero transform → `t263f40`→`t26b0c0` write.
- `t1f70-memb`: member mirror write at `6A0+0x50` + scalar at
  `+0x15C/+0x160`.
- `t2700-wrap`: wrapper decomposition.
- `u1140-*`/`v8bf0-*` re-proven — `312700` now real inside
  `238BF0` (its `u3125e0`/`u2ebb80` tags appear in the detach
  tail), `311F70` retained as scripted boundary on inbound calls
  from `301140` (same disposition as `fed0`-inbound; direct-entry
  runs real via the entry-bypass).

## Fixture disclosures (planted)

- `n336_fill` hook — writes six caller-frame floats past the
  scripted `336E40` boundary; `0xCD` stack-garbage variant retained
  as its own case.
- `q[rec+0x6A0]` flag/mirror block; prior EXP-161/162 fixture
  (objrow link, `+0x10` object, `E60`/`E68`, registry, state cell).
- Scripted: `336E40` (struct fill — semantic content unproven),
  inbound `311F70` on `301140` callsites, prior boundaries
  unchanged.

NATIVE-REPLAY only — no initialized-gameplay reachability claimed.
