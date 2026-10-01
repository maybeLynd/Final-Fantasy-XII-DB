---
id: EXP-161
title: "Teardown chain 301140/3105D0 — unlink deregisters through the EXP-158 resolver"
status: executed
evidence: NATIVE-REPLAY
exe_sha256: 73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8
harness: exp161_check.py
result: 122/122 (stable x3)
---

# EXP-161 — `3105D0`/`301140` teardown chain, executed

`003105D0` is the unlink/reset helper (83 insns) called from the
despawn path; `00301140` is the despawn/death teardown entry (102
insns) gated on the object row's engaged mask. The package closes the
loop predicted in EXP-159: `301140 -> 3105D0 -> 300280 -> 3008A0` —
the unlink path deregisters the entity through the EXP-158 spawn
id-resolver.

## `301140(rec)` — executed semantics

- `rax = q[rec+0x698]` — the rec's back-pointer to its object row.
  `edx = d[rax+0x64] | d[rax+0x3C]`; `edx & 0x80000003` nonzero →
  bail (the same engaged mask `30E360` arm3/`300530` drive). A null
  back-pointer faults at `0x301150` — authentic, no guard.
- `2E9600(q[rec+0x10])` — inspects the rec's `+0x10` object:
  `b[obj+3]&0xE0==0x60` → `q[obj+0xC0]` → `b[obj2+0x10]>>3&1`.
- `311F70(0, rec, 0)` runs only when `2E9600()==0` AND `d[rec]` bit
  `0x1A` is **clear** (`bt`/`jb` skips on set). 105i helper — scripted
  boundary; both polarities proven.
- `238BF0(rec)` — 235i cleanup chain, scripted boundary.
- `3105D0(rec)` — real unlink (below).
- Teardown writes: `q[+0x6F8]=0`, `d[+0x748]=0`, `d[+0x770]=0`;
  `q[rec]` bit `0x4000` with `w[rec+0xBA0] ∈ {0x113, 0x95}` spares
  `btr 0xE`, else clears bit 14; `d[+0x788]&=~0x400`,
  `d[+0x6B0]&=~2`, `q[+0x750]=0`, `d[+0x74C]=0`, `d[+4]|=0x200000`.
- `2EACD0(d[rec+8], 1, rec+8, 0x7B)` — small thunk that tail-jumps
  into `0x3B02A0`, a large (0xCA0-frame) wait/dispatch that spins on
  `0x24F610` lookups — cross-thread/async boundary, scripted at
  `0x3B02A0`. The `0x148`-byte `861EC0` memset inside it was already
  hooked.
- `2E8060(q[rec+0x10])` — guarded leaf.
- Name/anim pointer select: `ecx = b[objrow+5]` (or `0xFF` when no
  objrow) → `q[rec+0x6E8] = ecx ? rodata_ptr_A : rodata_ptr_B`.
- `2ECF10(q[rec+0x10], 0, 0)` — real (EXP-148-proven).
- `3299B0(rec, 0x200D, 0)` — despawn message post, scripted
  (EXP-155 message family).
- Final flag pass: `d[+4]&=~4`, `q[rec] &= 0xFFFFFFFDFFE7FFFD`,
  `d[rec]&=~0x700`, `q[rec]|=0x1000000`, `d[rec]|=0x40000000`,
  `d[rec+0x74]=-1`.
- `319E30(d[rec+0x74])` real; `32A150()` real; `d[rec+0xDD0] =
  eax - 5*cvttss2si(const*const)` — respawn/timer field recompute.
- `3125E0(rec)` → `30D9A0` reads `d[q[0x2EBF190]+0x5B04]` state-cell
  flags → small return code.
- `26DC60(q[rec+0x10], eax==0)` — trampoline → `2EBB80` (13i leaf).
- `d[rec+0x30]=0`, ret.

## `3105D0(rec)` — executed semantics

83 insns, the unlink/reset core. Executes `310780`, `30C970`
(reference release, ×3 call sites), `300280`, `16D6A0`, `236850` /
`236820` (object count/array accessors), `316CF0` (→`861EC0` memset),
`3291B0` (→`3839F0`), `33C9B0` (→`808C40`).

`300280` — nested state reset — calls **`3008A0`** (the EXP-158
id/entity resolver): unlink deregistration flows through the
spawn-bitmap mutator (`2FD420`) + validator dispatch (`309F30`) +
notify (`325F40`). Proven live: `u5d0-base` trace contains
`u300280 → a08a0 → l9f30` with the resolver running real.

`u5d0-noown`: rec without the object-row back-pointer still runs the
helper cleanly (internal guards), `300280` path differs.

## Proven

- `u5d0-base`: full `3105D0` body — `u310780`, `u30c970` ×3,
  `u300280 → a08a0` loop closure, `u316cf0` memset, `u3291b0`,
  `u33c9b0` — 0 faults.
- `u1140-base`: full teardown — engaged-mask clear path, `311F70`
  skipped (bit `0x1A` set), `238BF0` scripted, `3105D0` real, all
  tail leaves (`2E8060`, `2ECF10`, `319E30`, `32A150`, `3125E0`,
  `30D9A0`, `26DC60→2EBB80`) real, `3299B0(0x200D)` scripted post.
- `u1140-eng`: `objrow+0x64` engaged bit → early bail before any
  teardown.
- `u1140-noflg`: bit `0x1A` clear → `311F70` fires.

## Fixture disclosures (planted, MODEL-PROVEN components)

- `q[rec+0x698]` → planted object row; `q[objrow+0x698]` → rec
  (bidirectional link, `objlink`/`recback`).
- `q[0x209BE80]` → 0x12000 zeroed **object registry** (`290B90` /
  `290DF0` walk `+0x10Fxx` linked lists; null slots → early-out).
- `q[0x2EBF190]` → 0x6000 state cell (`30D9A0` reads `+0x5B04`).
- `q[rec+0x10]` → planted object (`b[+3]` configurable).
- Scripted boundaries: `311F70`, `238BF0`, `0x3B02A0` (async wait —
  reached via `2EACD0` tail-jmp), `3299B0`, `290DF0` (safety),
  `336710`, `33E1F0`, inbound `30FED0`.

NATIVE-REPLAY only — no initialized-gameplay reachability claimed.
