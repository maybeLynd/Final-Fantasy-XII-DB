---
id: EXP-164
title: "336E40 transform-struct fill — real native replay; mode/aux arm structure decoded"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp164_check.py
result: 132/132 (stable x3)
---

# EXP-164 — `336E40`, executed

The 346-insn transform-struct producer on the `311F70` reposition
path promoted from the `n336_fill` scripted caller-frame hook to
real native execution. Context-object layout and arm structure now
execution-verified.

## `311F70` → `336E40` context layout — executed

`311F70` builds `ctx` at `rsp+0x40`:

- `d[ctx+0]` = `sete(30D9A0() == 1)` — a **boolean** mode flag
  (only arms 0/1 reachable through this caller; the `2` arm needs
  other callers).
- `q[ctx+8]` = arg0 (aux object; `0` on `301140`'s callsites).
- `q[ctx+0x10]` = arg1 (primary object = `q[rec+0x10]`).

## `30D9A0` — full return decode (NATIVE/STATIC + replay)

`cl = d[q[0x2EBF190]+0x5B04]` then in order:

| condition            | eax |
|----------------------|-----|
| `cl & 8`             | 5   |
| `cl & 4`             | 4   |
| `377C20() != 0`      | 3   |
| `cl & 2`             | 2   |
| otherwise            | `cl & 1` |

`377C20`: `3148F0()` index → `q[0x2ADD100]` flag table, 3-byte
stride; null/out-of-bounds → `0xFFF >> 0xF` = 0, else
`(b[r8+idx*3+9]<<8 | b[r8+idx*3+8]) >> 0xF` — word bit15 (the
"can-die" flag the EXP-154+ fixture already plants).

## `336E40` arm structure — executed

- **Null-aux arm** (`q[ctx+8]==0`): the `0x336F79`/`0x3373CF`
  tail — kind-dispatched accessors `2646C0` / `265200` /
  `265090` (`b[obj+3] >> 5` → `q[obj+0xB8]` node; floats at
  `+0`, `+0x50`, `+0xA8`) — all real tags fire
  (`n2646c0`/`n265200`/`n265090`), then `808C40`.
- **Aux arm** (`q[ctx+8]!=0`): `202F00` 4x4 `movups` matrix copy
  → CRT helper stubs `861F08`/`861F0E` (`jmp q[IAT]` —
  unresolvable in harness, scripted) → `383F10` zone lookup:
  `d[q[0x2AEDFB0]+0x20]` on a null runtime global → **authentic
  fault** (`t1f70-aux`, `expect_fault=0x383F23`; deeper IAT trig
  calls also unresolvable — disclosed boundary).
- **Mode-1 arm** (`aux + d[ctx]==1`): `265090` → `309AE0` →
  `259B10` (index into a `0x110`-stride table, reads `+0x90/
  +0x94/+0x98`) → `203080` → `4687F0` → `call q[IAT]` at
  `0x3370D2` → wild exec into `.rdata` → **deterministic fetch
  fault** at `0x1CCEF20` (`t1f70-mode1`, `expect_fault`; import
  table contents are file-name RVAs — disclosed).
- `32A790`→`26E350`→`231900` remains the scripted scale/dispatch
  boundary (`n32a790` — 92-insn `231900` fan-out).

## Proven

- `t1f70-base`: `stateflags=0` → `30D9A0` ret 0 → `d[ctx]=0` —
  null-aux arm, `u30d9a0`, `n336e40`, `n2646c0`, `n265200`,
  `t265020`, `t392170`, `q[rec] |= 0x4000000`, no `26B0C0`.
- `t1f70-posw`: planted `rec10pos` **flows through the real
  gather** — transform position == `265020` read → equal → no
  write. Stronger than EXP-163's scripted fill: proves the gather
  consumed the same planted object position source.
- `t1f70-aux`: aux arm real through `202F00` copy → authentic
  null-global fault inside `383F10` (disclosed).
- `t1f70-mode1`: `stateflags&1` + `cd_words=[0]*8` (clears
  `377C20`'s bit15 return) → ret 1 → `d[ctx]=1` arm → real
  `n309ae0` + `n259b10` → IAT-call fault boundary (disclosed).
- `t1f70-memb`: member mirror write retained.
- `t2700-wrap`, `u1140-*`, `v8bf0-*`, and all 117 prior cases
  re-proven — 132/132 across three separate processes.

## Fixture disclosures (planted)

- `stateflags` → `d[statecell+0x5B04]` (drives `30D9A0`).
- `cd_words=[0]*8` — clears `377C20`'s bit15 word so `30D9A0`
  can reach the `cl&1` arm.
- Prior fixture unchanged (objrow link, `+0x10` object,
  `E60`/`E68`, registry, state cell).
- Scripted: `0x861F08`/`0x861F0E` CRT `jmp q[IAT]` stubs,
  `32A790`→`26E350`→`231900`, inbound `311F70` on `301140`
  callsites, prior boundaries unchanged.
- `expect_fault` boundaries: `0x383F23` (zone-context global
  `q[0x2AEDFB0]` null), `0x1CCEF20` (post-`4687F0` `call q[IAT]`
  wild exec — IAT holds name RVAs in the file image).

NATIVE-REPLAY only — no initialized-gameplay reachability claimed.
