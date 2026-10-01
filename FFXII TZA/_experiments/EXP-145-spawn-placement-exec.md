---
experiment: EXP-145
title: Spawn placement executed — 00234AF0 both modes with planted
  field-data/leader/unit fixtures; return-window pair, fetch
  convention, arc-then-band point validation, two-draw area mode,
  region shape filter, and the unwritten-Y provenance all observed
  on shipped bytes
contract: 05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md
method: B
live_game: false
tool: evidence/spawn-placement-exec/check.py
---
# EXP-145 — spawn-placement-exec

**Status:** complete · **20 cases, zero failures, stable ×3**
**Evidence:** `evidence/spawn-placement-exec/` (`check.py`,
`result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

`CONTRACT-spawn-placement.md` §13 carried **UNLINKED /
nothing-executed** — no placement body had ever run. This
experiment executes `Spawn_TrySelectCandidatePosition`
(`00234AF0`) in both modes, the `SpawnKeep_Get/SetReturnWindow`
pair (`00235330`/`00235340`), the candidate fetch
(`003209C0 → 003DFD00`), and through them the shared four-slot
range probe `00234DA0`, on shipped bytes.

## Executed signature

`00234AF0(ecx=candidateIndex, rdx=outPos f32×3, xmm2=minR,
xmm3=maxR, [rsp+0x28]=scoreOut-or-0, [rsp+0x30]=allSlots)`.
The two stack arguments feed the probe directly (its `rbp` /
`r12d`). Arc degrees come from `d[02089358]`; the band is
`(xmm3−xmm2)` compared squared against per-slot XZ distance².

## Executed behaviour table

| case | setup | observed |
|---|---|---|
| `win-neg` | `00235340(−5)` then `00235330` | cell `0208936C` → **300**, getter returns 300 (I1) |
| `win-zero` | `00235340(0)` | cell → **0** — `cmovs` is sign-only, zero is not clamped |
| `win-pos` | `00235340(7)` | cell → 7 |
| `empty-band` | `minR==maxR==5` | ret 0, **fetch never called** (I5) |
| `fetch-null` | `q[02B59D48]=0` | `003DFD00` reached, returns fail → ret 0 |
| `fetch-oob` | `count=0` | ret 0 |
| `fetch-direct` | `003209C0(0)` / `(5)` standalone | in-range → **eax=0**, record copied; oob → **eax=−1** (I2 executed, not just read) |
| `null-leader` | `b[02089340]&~0x10` | ret 0, **but `outPos` already holds the authored point** — the copy precedes the leader check |
| `point-hit` | rec mode 0, authored (0,0,8), leader at origin heading 0, band [5,15] | ret 1, out = authored pos, **score-out = 64.0 = dist²**, 0 RNG draws |
| `point-arc-miss` | authored (8,0,−8), arc 90° | ret 0, **probe never entered** — arc gate precedes distance |
| `point-band-far` | authored (0,0,20), dist²=400 > 225 | ret 0 via probe |
| `point-band-near` | authored (0,0,2), dist²=4 < 25 | ret 0 via probe — the band has a **lower** edge too |
| `point-coincident` | authored == leader pos | `0031AC90` fallback (dx=dz=0 → heading=yaw) → arc hit; probe rejects dist²=0 → ret 0 |
| `point-no-slots` | member table empty | probe ORs slots — all dead → esi stays 0 → ret 0 |
| `probe-allslots-fail` | arg6=1, second live unit at (900,900) | leader slot passes but slot-1 fails bounds → **immediate ret 0** — with `allSlots` every live slot must be in-band |
| `area-box-hit` | rec mode 1, huge extents | ret 1; **exactly 2 LCG draws** (`0x11111111→0xD6217D13` = two `00328370` calls); out = drawn point `(-2.51, ?, 4.35)` |
| `area-box-miss` | rec mode 1, extents 1.0 centred (1e6,1e6) | ret 0; **still exactly 2 draws** — RNG is spent even on rejection; out keeps the authored centre (pre-copy) |
| `area-ellipse-hit` | rec mode 2, huge radii | ret 1 — the `rec[0]==2` arm is an ellipsoid test (`Σ(t/r)² ≤ 1` via `00325EA0` rotation) |
| `area-shape3` | rec mode 3 | ret 0 — `002374E0` accepts only modes 1 and 2; other non-zero modes always fail |
| `oldfmt-point` | record-set version `0x20 < 0x33` | ret 1 — `003DFD00` **forces `rec[0]=0`** on the old layout: pre-v51 format-0 candidates are structurally point-mode-only |

## Findings

- **I1 executed.** `00235340`: `test ecx,ecx / mov eax,0x12C /
  cmovs ecx,eax` — strictly negative → 300; zero stays zero.
  `00235330` reads `d[0208936C]` back unchanged.
- **I2 executed.** `003209C0` maps `003DFD00`'s 1/0 to 0/−1 via
  `neg/sbb/neg/dec`; the parent tests `js` — **0 is success**.
- **I3 executed.** `rec[0]==0` → point (arc then band);
  non-zero → area (two draws, region only). Region shapes are
  `{1: rotated box, 2: ellipsoid}`; `rec[0]≥3` in area mode is
  unreachable-by-data in practice — the region test fails it.
- **I4 executed.** Leader chain is `003590D0` id → `003588B0`
  id-decode (`gen<<20 | tbl<<16 | slot` → descriptor
  `02098E10+idx*0x288`, gen check `w[obj+0x16]`) → `00263E30`
  `q[obj+0x30]` → `b[rec]&8`. Gate cell `b[02089340]&0x10`.
  **Null leader still leaves the authored position in `outPos`.**
- **I5 executed.** `ucomiss (max−min), 0` with `jp`/`jne` both
  continuing — an empty band refuses **before** the fetch; a NaN
  band would proceed (parity flag path), noted not probed.
- **I6 confirmed at execution depth.** `out_observed` (the
  probe's `rbp` score slot) is written only when the probe's
  second `003273B0` leader-check passes; the parent passes its
  own arg5 through untouched — in area mode nothing writes it.
- **I7 executed with provenance.** `00319390` writes `out+0` and
  `out+8` only (`X = base.x + r·sinθ`, `Z = base.z + r·cosθ`,
  32,768-entry sine table `01F004E0`, `cos = sin[(0x2000−i)&
  0x7FFF]` — matching I8). The caller then copies the
  **unwritten** `out+4` local into `result.y`: with a 0xCD
  stack sentinel, `area-box-hit` produced `out.y =
  0xCDCDCDCD (−4.3×10²⁶)`, replacing authored `y=7.5`. **The
  area-mode Y is uninitialised-stack data** — §14's "what
  supplies Y" is now: *nobody, at this level; whatever supplies
  the real Y must run downstream of `00234AF0`*.
- **§9 executed.** Point mode draws **zero**; area mode draws
  **exactly two** (`00328370` ×2, three ANSI-C rounds each),
  whether or not the region test passes. `arcDeg` integer comes
  from `d[02089358]`; draw1 feeds `r`, draw2 feeds `θ`.
- **Probe semantics, executed.** `00234DA0` = OR-over-slots with
  early-fail: each live, gate-passing slot must satisfy
  `min² ≤ dist²(candidate, slot) ≤ max²`; a single in-scope slot
  failing bounds returns 0 immediately; `r12d==0` restricts
  evaluation to the leader-identified slot (`003273B0` id
  compare); `rbp` non-null + leader-check → score written.
- **Old record format is structurally point-only.** Version
  byte `b[tbl+7] < 0x33` takes the 0x10-byte record layout and
  writes `rec[0]=0` — no authored mode byte can reach area mode
  on pre-v51 format-0 data.

## Scripted boundaries

- `0x861F02` — the `0031AC90` tail call — is a `jmp qword` through
  cell `0x8C2BD0`, which is **not** a named import (file content
  `0x1CCED38`, an encoded CRT pointer). Emulated as
  `atan2f(dx,dz)` per contract I8 and returned to the caller.
- Generic `ff 15`/`ff 25` → named-import stubs (none reached in
  practice besides the cookie path — `00808C40`
  `__security_check_cookie` executes shipped bytes and passes
  with a consistent zero cookie).

## Fixture disclosure

All fixture state is disclosed MODEL-PROVEN planting — the cells
are runtime BSS/descriptor state by construction:

- Format-0 record set at `q[02B59D48]` (header `{b+7 version,
  d+C count}`, v≥0x33 → 0x30-byte records at +0x10, else
  0x10-byte records at +0x10 with `rec[0]` forced 0).
- Leader chain cells: `b[02089340]|=0x10`, `d[022C7FE0]` =
  `0x100000`, descriptor block `02098E10` (`q+8` array,
  `d+0x20` count, `b+0x10` enable), object `w[+0x16]=gen`,
  `q[+0x30]` rec with `b[0]|=8`, `q[rec+0x10]` sub.
- Unit array `q[0208E688]`/`d[0208E6A0]` (stride 0xF50),
  member-index bytes at `q[02EBF190]+0x5A5A+i·2`, per-unit
  `q[+0x698]` sub (matched on `w[sub+4]`), `d[+8]` id,
  `q[+0x10]` position sub (`b[sub+3]=0x20`, `q[+0xB8]` →
  `{x,y,z}`, `f[+0x38]` heading).
- Class-2 validator descriptor at `q[02EBF130]` (`d[desc+4]`=64)
  — without it `002367A0` rejects every member index (BSS).
- `d[02089358]` arc degrees = 90.
- Evidence class: **NATIVE-REPLAY** over shipped bytes with
  disclosed fixtures. No reachability claim — the gate flag
  `00377C20` path is planted-ready but unexercised (all unit
  subs carried zero flag words, skipping it).

## Correction - the `0x861F02` boundary is a named import (SWE2-ORACLE, 2026-09-30)

Answers `ORACLE-REQ-OPUS-294-EXP145-BOUNDARY-IS-A-NAMED-IMPORT`.
- **"Not a named import - encoded CRT pointer" is wrong,** both under Scripted boundaries above and in the
  `check.py` header comment.
- **What the cell is.** The PE import directory resolves cell `0x8C2BD0` to `api-ms-win-crt-math-l1-1-0.dll!atan2f`;
  `0x1CCED38` is that import's hint/name RVA, as the unbound file holds it. The same resolution gives `008C2B40`
  `malloc` and `008C2B60` `_aligned_malloc` (`candidates/s16-iat-resolve.py`, OPUS `f61f97971`).
- **The emulation is unaffected.** It reads xmm0/xmm1 and returns `atan2f(dx, dz)`, which is what the named import
  computes. S-16's strict-world re-run (`7d1b56515`) treats it as one named import, 20/20.
- **Class.** Static (PE import-table read). The `check.py` comment is left as committed; this section is the
  correction of record.
