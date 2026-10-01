---
id: EXP-168
title: "312730 unexercised opcode arms — 0x4022 / 0x4024 / 0x4125 / 0x414A / 0x414E with real owner resolvers"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp166_check.py
result: 149/149 (stable x3)
---

# EXP-168 — the remaining 312730 opcode arms, executed

Exercises the five `312730` dispatch arms EXP-165 left
unexercised. The blocker was the shared owner/member resolver
gate — a **mis-computed RIP-relative cell** (7-byte
`test byte ptr [rip+disp], imm8` measured as 8) put the gate at
`0x208B340`/`0x2089341` when the real cell is **`0x2089340`**.
All four resolver bodies (`31B7E0`, `31ABE0`, `3272A0`,
`3272F0`) read that one byte. Confirmed live: an emu
`UC_HOOK_MEM_READ` trace showed the test hitting `0x2089340`.

## Resolve chain — executed real

`31B7E0` / `31ABE0` / `3272A0` all gate on
`b[0x2089340] & 0x10`, then:

- **`3588B0(id)`** — `cls = id>>0x10 & 0xF` (`< 5`),
  `idx = id & 0xFFFF`, `gen = id>>0x14 & 0x7FF` →
- **`263FF0(cls)`** — cls descriptor `0x2098E10 + cls*0x288`:
  `{q+0 base, q+8 rowptrs{count, ptr…}, b+0x10&1 active,
  d+0x20 count}` → bounds + active + `w[row+0x16]==gen` →
- **`263E30(row)`** — returns `q[row+0x30]` = the resolved rec.

Fixture plants one cls-1 descriptor + row + rec; id
`0x110000` = gen 1 / cls 1 / idx 0.

## Arm semantics — executed

- **`0x4022` (t2730-4022, eax=1)** — foe arm:
  `q[rec+0x698]` non-null, `b[objrow+5]==0` →
  `31B7E0(d[rec+0x24])` → copies `rec+0x120` quad → out1
  (observed `1.0,2.0,3.0,4.0`), owner `+0xD0` quad → out2
  (`5.0,6.0,7.0`), `outf = 309B10(rec) + 309A90(rec)` =
  `0x41C0CCCD`. All callees real: `t31b7e0`, `t3588b0`,
  `v263ff0`, `u263e30`, `t309b10`, `t309a90`.
- **`0x4024` (t2730-4024, eax=1)** — `3272A0` =
  `3590D0()` (leader id `d[0x22C7FE0]` — *another*
  off-by-one corrected: `0x3590D6+0x1F6EF0A=0x22C7FE0`,
  not `0x252D7E0`) → gate → `3588B0` → `263E30` →
  **`b[rec]&8` required** → shared `0x312918` body: owner
  `+0xD0` → out1 & out2, `outf = 30A130(owner)+arg+xmm6`.
- **`0x414A` (t2730-414a, eax=1)** — `31B7E0(d[rec+0x24])` →
  the *same* `0x312918` shared body — same owner-quad copy,
  `v30a130` real.
- **`0x414E` (t2730-414e, eax=1)** — `31ABE0(d[rec+0x710])`
  → `3588B0` → **row** (not rec — no `263E30`) →
  `265390(row, out1, out1+4, out1+8)` kind-dispatch on
  `b[row+3]>>5`: kind3 arm (`&0xE0==0x60`) reads
  `q[row+0xB8]` node → `d[node]`/`f[node+4]`/`d[node+8]`
  → out quad (`11,12,13` observed), `d[outf]=0` written
  by the arm itself.
- **`0x4125` (t2730-4125, eax=0)** — `312DF0` scatter
  seeded by `rec+0xD0` quad, `r8d=0x14`, `edx=-1` →
  takes the **`3377C0`** validator variant (vs `337700`
  on the group-row path). 9 real iterations through the
  EXP-166 zone ctx (`z383f10` ×9, `t337700` ×9 nested —
  `3377C0` itself calls `337700`), exhausts → reject.
  Interesting: `t31abe0` fires ×9 inside the loop — the
  validator consults the member resolver per iteration.

## Fixture additions

- `ownerres` — gate bytes `0x2089340 |= 0x10`, cls-table row
  at `0x2098E10 + cls*0x288`, rowptrs `{count, ptr}`, orow
  `{w[+0x16] gen, q[+0x30] rec}`, orec `{+0xD0 pos quad,
  b[0]&8 flag, q[+0x10] obj}`.
- `leaderid` — `d[0x22C7FE0]` for `3272A0`'s `3590D0` read.
- `rec710` — `d[rec+0x710]` for `31ABE0`.
- `orecb0`/`orowb3`/`orownode`/`orec10` — resolved-rec flag
  and `265390` node inputs.

## Disclosures

- Hand-built cls-table/row/rec fixture — **NATIVE-REPLAY**,
  not initialized-gameplay reachability. The gate byte
  `0x2089340` is OR'd (`|= 0x10`), preserving shipped bits.
- `265390` kind-3 arm additionally reads `q[r11+0xC0]` for an
  optional `+0x140/+0x144` add — r11 is whatever the
  dispatcher left; observed path skipped the add (null).
- `309B10`/`309A90` constants are whatever the planted
  `q[rec+0x10]` kind-3 node yields — outf value is
  fixture-dependent, structure is real.
- `0x4125` exhaust (eax=0) is a *reject* proof, not accept —
  accept would need `erow`+`egrid` (the EXP-166 accept
  fixture) combined with the `0x14`-arg validator arm.
