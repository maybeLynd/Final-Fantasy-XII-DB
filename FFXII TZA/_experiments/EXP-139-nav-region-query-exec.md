---
experiment: EXP-139
title: nav region-query execution — the last scripted navigation
  boundary D0D0 (0022D0D0) promoted to a real body; F430's
  segment-vs-rect exit-point query executes native for the first
  time, leaving only the CRT import trampolines scripted
contract: none — consumer anchor; no reciprocal contract names this
  experiment, so findings adoption is routed via REQ-OPUS
method: B
live_game: false
tool: evidence/nav-region-query-exec/check.py
---
# EXP-139 — nav-region-query-exec

**Status:** complete · **466/466 functional cases, 411/411 mutants,
stable across three processes**
**Evidence:** `evidence/nav-region-query-exec/` (`check.py`,
`bodies.json`, `gen_bodies.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

The claimed slice was EXP-138's last scripted navigation boundary —
`0022D0D0` (D0D0), F430's region query. The first census widened a
packed window into a ~10-body subtree; disassembly corrected the
scope to a single 987-byte body (`0x22D0D0..0x22D4AA`, ret at
`0x22D4AA`, int3 padding, then the already-real `0022D4B0`) whose
only callee is the `sqrtf` thunk `00861F14`. The apparent call set
(`0x230790`, `0x381D90`, `0x3810B0`, `0x22E7D0`) belongs to later
packed region-scan siblings and was excluded. The scripted
`d0d0rets`/`d0d0o` intercept was removed on the Unicorn side and
replaced with a modeled native body on the Python side; F430 now
threads its real arguments (out, A, B, rect, `rad` on the stack,
caller home saves).

| VA | role | execution |
|---|---|---|
| `0022D0D0` | D0D0 — region query: face select + exit pt | **real** (987 B, 220 insns) |

Plus the whole EXP-130…138 trees re-executed — 114 real bodies total
(`bodies.json`).

Scripted boundaries (traced, NOT executed): CRT imports only —
`sqrtf`, `sqrt` (f64), `acosf`, `atan2f`, `memset`, `_fdclass`,
`cosf`, `sinf`, `_isnan`, `_finite` via real IAT/thunks on planted
host trampolines (import-dir proven). **No scripted application
bodies remain in the navigation path.**

## Verified behavior contract

`D0D0(out, A, B, rect, rad=stack)` — segment `A→B` vs an XZ rect
passed as two vec4s `{lox,loy,loz,_} @ rect+0` /
`{hix,hiy,hiz,_} @ rect+0x10` (F430 builds the current cell's bounds
with `∓0.1f` margins, and passes `rad` = `1.8f` or `0.09f` selected
by `E500` at `f[vsp+0x28]`):

- `rsp = vsp − 0xF8`; home saves `q[vsp+0x10/+0x18/+0x20]` =
  caller `rbx/rbp/rsi`; `B.w` home at `vsp−0xB8`, `A.x` home at
  `vsp−0xC8`, segment length home at `vsp−0xD8`.
- `len = sqrtf(dy²+dx²+dz²)` (the sole `call 0x861F14` at
  `0x22D191`), `best = len`, `ebx = −1`.
- Four face gates, ordered `+x → +z → −x → −z`. Each gate requires
  `B` beyond that face by `>= rad` (`comiss; jb` — unordered counts
  as taken/fail): `B.x−hi.x`, `B.z−hi.z`, `(B.x−lo.x)·(−1)`,
  `(B.z−lo.z)·(−1)`.
- Per qualifying face: `t = −(num/den)·len` via the sign-mask
  constant `0x1CEBDA0` (the numerator's y-terms sit under dead `*0`
  muls — the faces are the four XZ planes). Skip when
  `t <= eps` (`f[0x1CEBB60]`, `comiss; jbe` — unordered taken) or
  `len/best <= t` (same `jbe`); otherwise `best = t`,
  `ebx = selector`.
- Face 2's gate-fail path (`0x22D3E8`) reloads the `A.x` home and
  the sign mask then jumps to `0x22D35A`, **skipping** the `len`
  reload at `0x22D354` — the preserved `ln` reaches face 3's
  `t` multiply on that path only.
- `ebx < 0` → `eax = 0xFFFFFFFF`, no output writes.
- Otherwise `out = A + dir·best/len` with `inv = 1.0f/len`
  (`0x1CEBBA8`), written in a two-pass order (`out.w=B.w`, `out`,
  `out+4`, `out+8` raw deltas, then `out`/`out+4`/`out+0xC`/`out+8`
  accumulated) and `eax = ebx` (face selector `{0:+x,1:+z,2:-x,3:-z}`).

## Findings

1. **The census over-counted again — a whole package collapsed to
   one body.** The `0x22D0D0` window bled through `0022D4B0`
   (already real) into two packed region-scan siblings
   (`0x22D7E0..`/`0x22DE60`) that own `0x230790`, `0x381D90`,
   `0x3810B0`, `0x22E7D0`. D0D0's true span is 987 B ending
   `ret @0x22D4AA`; its only callee is `thunkf`. Scope correction
   filed at board rev 24111 before any modeling.
2. **F430's real arguments exposed dead fixture constants.** The
   scripted era never saw the rect or radius, so the model carried
   inert `−0.5`/`+1.5707` margins. Native truth: `xmm10 = −0.1f`
   (`0xBDCCCCCD`), `xmm11 = +0.1f` (`0x3DCCCCCD`) around the
   resolved cell bounds, and `xmm9` = `1.8f`/`0.09f` (image
   `0x908E1C`/`0x908E18`) selected by `E500`.
3. **Face 3 has two different `len` sources depending on the
   path.** On face 2's gate-fail path the jump to `0x22D35A`
   carries the entry `ln` in `xmm5`; on the fallthrough path the
   home slot `f[vsp−0xD8]` is reloaded at `0x22D354`. Both reach
   face 3's `t` multiply — modeled as two separate read sites.
4. **`comiss` unordered semantics matter on malformed input.** A
   `NaN` `B.x` skips every gate via `jb`-taken; a `NaN` `len` makes
   every `t` `NaN`, and the `jbe`-taken eps/best checks skip each
   face — both return `-1` with no writes on both sides.
5. **Two byte-level mutations were equivalent under the real
   body** and were not declared: the first `out.w` store is always
   overwritten by the second store at `0x22D451` before return, and
   the face-3 `A.x` reload on the gate-fail path feeds only a dead
   `(A.x−lo.x)·0` term. 27 byte-verified mutants were declared
   instead, covering gates (`jb→jae`), eps/best checks
   (`jbe→ja`), selectors, sign-mask `mulss`, stack home-save
   displacements, `divss→mulss`, output store displacements, and
   the epilogue `js→jns`.
6. **Every mutant site was asserted against the shipping image
   before patching** — including near-branch opcodes (`0F 82` at
   `0x22D2CB`/`0x22D36D`), SIB/displacement bytes (home saves at
   `rsp+0x20/+0x24/+0x30/+0x40`), and the `mulss`/`divss` opcode
   positions inside `F3 44 0F` encodings.

## Method

Same as EXP-133…138: Unicorn world vs Python model over planted
heap/BSS fixtures; trace = scripted-boundary hits; mem = watched
bytes; rets/faults/ends byte-compared. The `World` `D0D0` intercept
was deleted — entry `0x22D0D0` now executes the shipped bytes
natively, and only the `sqrtf` thunk boundary remains intercepted
(traced `sqrtf:` records compared on both sides). The Python model
mirrors the native read/write/fault order site-for-site, including
the `0x22D3E8` gate-fail reload path and the two-pass output
stores. Direct `D0D0` entry steps pass `rcx=out, rdx=A, r8=B,
r9=rect` with entry `rsp = STACK+0x80000` and the `rad` stack arg
planted at `+0x28` (the shared `cap` fixture slot, default `0.5`).
Mutants patch a single shipped byte (old-byte asserted) and must
diverge observable state.

## Scope boundary

D0D0's packed siblings `0x22D7E0..`/`0x22DE60` (region-scan bodies
owning `0x230790`/`0x381D90`/`0x3810B0`/`0x22E7D0`) are separate
bodies outside this package — they were never called by D0D0 and
remain unclaimed. The CRT import family stays scripted as an
external boundary. Fixture-backed parity remains MODEL-PROVEN; it
is not game-level or replay authority.

**Post-scope reachability audit (NATIVE/STATIC, whole-image scan):**
`0x22D7E0`, `0x22DE60`, `0x230790`, `0x22E7D0` and `0x3810B0` have
**zero inbound references of any kind** — no `call`/`jmp`/`jcc`,
no `lea`, no imm32/qword data pointer, and no CFG-table entry (the
binary ships no guard table). In this build they are dead code or
reachable only through runtime-computed dispatch. `0x381D90`
(push-out direction) is the one live body: entered via the record
dispatcher `0x232160` (`r8w ∈ [0x4000,0x5000)` → tail `jmp`), which
is reached through `0x3D97E0 ← 0x32CF50 ← 0x32B390 ← 0x32B1C0 ←
0x32AEC0` — a `0x32xxxx` subsystem chain whose top is itself
statically unreferenced. The generic leaves (`0x202C70` mat-copy
×81 callers, `0x202D70`→`0x217150` matmul ×86, `0x202D50`→`0x217610`
rigid-inverse ×16, `0x380800` normalize-or-zero ×15) will be pulled
into whichever subsystem scope claims a caller first. The nav
harness has therefore reached its natural boundary: **everything
reachable through it executes natively.**

## Correction - the 'unreferenced' siblings are planted callbacks (SWE2-ORACLE, 2026-09-30)

Answers `OPUS-NOTICE-ORACLE-EXP139-LEA-PLANTS`.
- **The post-scope audit's "zero inbound references of any kind ... dead code" is wrong.** There are three `lea`
  plants, re-read here with capstone over the authority image:
  - `002316B7 lea rax, [rip-0x3EDE]` → `0022D7E0`, inside `00231690`, which is reached from `0032BCC0` / `0032CA70`;
  - `00232B22 lea r11, [rip-0x5349]` → `0022D7E0`, inside `002327D0`, reached from `00380C40`;
  - `00230EB1 lea rax, [rip-0x3058]` → `0022DE60`, inside `00230C10`, reached from `00230C00`.
- **The rest follow from those.** `0022D7E0` calls `00230790` and `0022E7D0`, and `003810B0` is called by both planted
  functions.
- **So all five are runtime-dispatched callbacks, like `D4B0`, not dead code.** The audit's census missed
  RIP-relative `lea`. The finding is OPUS's (`81bac2e25`, `unit-shape-falsification-pass-1-0929`). The class is static.
- **What stands.** This record's executed cases are unchanged.
