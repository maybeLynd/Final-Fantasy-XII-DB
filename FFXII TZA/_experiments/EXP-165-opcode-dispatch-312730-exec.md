---
id: EXP-165
title: "312730 transform-opcode dispatcher — real native replay; 312DF0 scatter loop decoded"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp165_check.py
result: 140/140 (stable x3)
---

# EXP-165 — `312730`, executed

The 246-insn sibling of `312700` — miscatalogued in EXP-162 as
"`312700` itself" — is a **transform/position opcode dispatcher**
executed end-to-end. Corrects the record: the wrapper is `312700`;
this body starts at `0x312730`.

## `312730(rec=rcx, cmd=rdx, out1=r8, out2=r9, a5=outf)` — executed

- `ebx = w[cmd]` (opcode), `r14d = w[cmd+2]` (signed arg).
- `265090(q[rec+0x10], &f70, &f78)` → `xmm6 = maxss(f70,f78)` —
  scale seed.
- `op > 0x4035` → extended singles chain: `0x4124`, `0x4125`,
  `0x414A`, `0x414E`, `0x4165`; else reject.
- `0x4026..0x4035` → `2367A0(op - 0x4026)` entity scan (below).
- `0x4000..0x4025` → 2-level jump table: index map
  `b[0x312B10 + (op-0x4000)]` → offset `d[0x312AF8 + idx*4]` +
  `0x120000` → `jmp rcx`.
- Success epilogue: `movaps xmm0,[out1]` → `movdqa [out2]`
  (input quad copied to result), `movss [a5]` = xmm6, ret 1.
  Reject = `xor eax,eax`.

## Arm decode

| opcode(s) | arm | behaviour |
|---|---|---|
| `0x4000..0x401F` | `0x3127C7` | `edx = op-0x3FFF` (subop 1..0x20), `ecx=0`, `r8d=arg` → `312DF0` scatter |
| `0x4020` | `0x3127D7` | member-only (`b[objrow+5]==1` gate): seed = `q[rec+0x6A0]+0x50` — the quad `311F70` mirrors — → `312DF0` |
| `0x4021` | `0x312AD4` | reject |
| `0x4022` | `0x31289E` | (unexercised) |
| `0x4023` | `0x312804` | `31B7E0(d[rec+0x710])` owner → `312DF0` seed `[rbx+0xD0]` + `30A130` |
| `0x4024` | `0x312913` | (unexercised) |
| `0x4026..0x4035` | `0x312970` | `2367A0(op-0x4026)` → `0x312918`: copy found rec's `+0xD0` quad to out1+out2, `d[outf] = 30A130(found) + arg + xmm6` |
| `0x4124` | `0x312A91` | `31B7E0(d[rec+0x24])` owner → copy `+0x120`/`+0x130` quads → `d[out?]` = `d[owner+0x154]` |
| `0x4125` | `0x312A50` | (adjacent arm) |
| `0x414A` | `0x312A43` | (adjacent arm) |
| `0x414E` | `0x3129F3` | (adjacent arm) |
| `0x4165` | `0x3129A9` | `319850(rec, out1)` + quad copy + `xmm6 += 1.0f - const` |

## `312DF0(rcx=seed?, edx=subop, r8d=arg, r9=rec)` — executed

Position-scatter generator:

- `rsi = a5` (out vec). `rcx==0` → `320940(ecx=subop, &vec)` →
  `3DFD00(0, subop, &stack)` — group-0 row fetch:
  `q[0x2B59D48 + 0]` row group, `b[+7] >= 0x33`, `subop < d[+0xC]`,
  copies 3 quads of a `0x30`-stride row. Null/missing → ret −1.
- `rcx!=0` → seed = `[rcx]` quad (member mirror for op `0x4020`).
- Loop `edi = 0..8`: `328370()` RNG ×2 →
  `(rand % (2*arg+1)) - arg` jitter added to vec x/z →
  `317DE0(rec, vec, arg!=0)` validates → `337700` (`arg==0`) /
  `3377C0` (`arg!=0`, 0x1B8-frame heavy check).
- Returns: `0` = first valid position (`317DE0` nonzero →
  `xor eax,eax`), `−2` = 9 failed iterations, `−1` = seed fetch
  failed. `312730` rejects on `<0`.

## `2367A0(selector)` — executed

Scans the shipped global entity array `q[0x41E6688]` (stride
`0xF50`, count `d[0x41E66A0]`): match
`w[q[row+0x698]+4] == selector` (`0xFF` → wildcard `0xFFFF`).
Found → returns row. Executed: resolved a shipped row whose
`w[objrow+4]==0` matched selector 0.

## Proven

- `t2730-bad`/`t2730-4021`: out-of-range and idx-5 reject → `eax=0`.
- `t2730-4000`: `0x4000` → `312DF0` → `320940` → `3DFD00` — shipped
  group slot empty → −1 → reject.
- `t2730-scat`: planted `0x2B59D48` group (`count=2`, seed rows) →
  full scatter loop: `328370` RNG ×2 + `317DE0` → `337700` →
  `383F10` zone lookup → **authentic null-global fault**
  (`q[0x2AEDFB0]`, `expect_fault=0x383F23` — same disclosed boundary
  as EXP-164's aux arm; the zone-context global is the shared
  blocker for all position-validation paths).
- `t2730-4020`: foe `b[objrow+5]==0` → reject before `312DF0`
  (member gate proven).
- `t2730-4020m`: member `b5==1` + `rec+0x6A0` → scatter loop seeded
  from the `311F70` mirror quad → same `0x383F23` boundary.
- `t2730-4026`: `2367A0(0)` resolved a shipped row → `0x312918`
  copied `+0xD0` → `30A130` → `265090` faulted on the row's null
  `+0x10` object — **authentic**: static-image entity rows are
  unlinked (`expect_fault=0x265090`).
- `t2730-4124`: `31B7E0(d[rec+0x24]=0)` → null owner → reject.
- All 132 prior cases re-proven — 140/140 across three processes.

## Fixture disclosures (planted)

- `cmd` buffer (`w op`/`w arg`), `out1`/`out2`/`outf` (r8/r9/a5).
- `scatrow`: `q[0x2B59D48]` row group (`b[+7]=0x33`, `d[+0xC]=2`,
  two `0x30`-stride seed rows).
- `rec6a0`/`objb5` for the member arm; prior fixture unchanged.
- `expect_fault` boundaries: `0x383F23` (zone-context global
  `q[0x2AEDFB0]` null — needs the real zone object),
  `0x265090` (`2367A0`-resolved shipped row has null `+0x10`).
- `328370` RNG executed real (returns whatever its internal state
  produces — the jitter amounts are therefore not asserted, only
  the call count).

NATIVE-REPLAY only — no initialized-gameplay reachability claimed.
