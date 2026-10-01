---
id: EXP-171
title: "2FEF30 member-arm fixture — four-desc stat-table resolve, member stat accumulation, owner 6A0 tail"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 155/155 (stable x3)
---

# EXP-171 — the 2FEF30 member arm, executed

Closes the long-standing `fed0-b5`/`fed0-b5own` fixture gap:
both member-rec (`b[rec+5]==1`) cases previously stopped at an
authentic fault (`0x2FF1FC`) and now run the member arm fully.

## `2FEF30(rec, slotlist?, out, r8?)` — member arm decoded

`b[rdi+5]!=0` → `0x2FF0E1`, a four-level `20E600` resolver
chain producing four stat-table rows:

| level | desc global | index field | row |
|-------|-------------|-------------|-----|
| r13 member | `q[0x2EBF120]` (MEMD) | `b[rdi+4]` | `e600 + w[g+8]*b4` |
| rbp | `q[0x2EBF148]` | `w[r13+0x22]` | `e600 + w[g+8]*idx` |
| rbx | `q[0x2EBF140]` | `w[r13+0x24]` | same |
| r11 | `q[0x2EBF150]` | `w[r13+0]` | same |

Each triple is the same shipped pattern: `q[G]` →
`e600(d[g+0xC])` → `q[G]` → `e600` → `w[g+8]` stride →
`base + stride*idx`. The old fault: `rbx` (level 3,
`0x2EBF140`) resolved null → `w[rbx+0x24]` read at
`0x2FF1FC`.

Then ~200 insns of stat accumulation:

- `ecx = b[rdi+0x1C2] - b[rdi+0x88]` (level delta).
- Eight stat slots computed as
  `rbx.b[+0x27..+0x2C]*ecx + rbp.b[same] + rec.w[…]`
  (`+8,+0xA,+0xC,+0xE,+0x16,+0x12,+0x14,+0x10`).
- HP/MP pair: `d[rbx+0x20]*ecx + d[rbp+0x20]` and
  `w[rbx+0x24]*ecx + w[rbp+0x24] + w[rdi+0x1C]` etc.
- `b[r11+0x29..+0x2D]` → 5 bytes into `out+0x1C..+0x20`.
- `b[r13+0x15]` bit-test gates two more stat arms
  (bit1 → `rbx.b[+2]/rbp.b[+2]` path at `0x2ff336`;
  bit2 → `rbx.b[+0x2D/+0x2E]` path at `0x2ff388`).
- Tail: `322C50` loop over the `w[rdi+0x50]` slot list.

## `30FED0` member tail — executed

After the `30E360` bit loop, `b[rec+5]==r13b` →
`31B860(rec)` owner scan (`e6850`/`e6820` object-array
walk) → `q[owner+0x6A0]` → `test b[obj],0x80` →
`b[obj+0x78]` → `b[rec+0x40]` store. The `b5own` fault
was this `q[objrow+0x6A0]==0` deref — new `obj6a0`
fixture key plants it.

## Executed

- `fed0-b5`: full member arm clean — `e600`×8 (all four
  resolver pairs), `v2c50`×10, `n0e060` notify, 0 faults.
- `fed0-b5own`: same plus `b860`×5 + `e6850`/`e6820`×5
  owner scan + `6A0` bit7 test (bit clear → skip arm),
  0 faults.
- Fixture: `membarm` plants descs at `0x2EBF148`,
  `0x2EBF140`, `0x2EBF150` (`mkdesc`, stride 0x40,
  elemb offs 0x4000/0x8000/0xC000); `obj6a0` plants
  `q[objrow+0x6A0]`; `objreg` for the `300280` teardown
  boundary (not reached on this path — b5's
  `q[rec+0x698]` null → early-out).

## Disclosures

- Resolved rows are zeroed elemb regions — the stat math
  runs real but computes zeros; index fields
  `w[r13+0x22]/+0x24/+0` default 0 → each level resolves
  element 0. Nonzero-value coverage would need distinct
  planted tables — the *structure* is proven, per-row
  values remain fixture-free.
- NATIVE-REPLAY only — not initialized-gameplay
  reachability.
