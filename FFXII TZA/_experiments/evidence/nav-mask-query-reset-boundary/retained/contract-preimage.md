---
contract: Corridor query — ask whether an agent may move along a proposed segment, and answer with a small integer
category: 06-Movement-And-Navigation
scope: family
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: >
  06-Movement-And-Navigation/how-a-unit-finds-its-way-across-the-navigation-mesh.md (the query layer
  it documents), and the consumer half of
  06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md, which names
  00335B60 and 003357B0 as TestForwardStepClearance and QueryDynamicActorObstruction
entries: ["00335B60", "003357B0", "0033A3D0", "00335F90", "00391410"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: >
    Every entry body was read from the authority image by OPUS on 2026-09-20 before this contract
    was written - BLKCHK and PATHW end to end, PVAL's full control structure, GATE's prologue and
    return tail, and LQUERY's mask sites. The behavioural detail is SWE2-ORACLE's, executed under
    EXP-132 through EXP-137 (92 bodies, 1,531 functional cases, 1,281 byte-precise mutants, all
    committed at c36dcda20). The determinism and global-write claims in sections 5 and 9 are
    mechanical results over the family's own 102-body call closure, not readings.
    Address resolution: 35 distinct addresses cited, 19 resolving to a function entry or interior
    and 16 to data or BSS, 0 unresolved - run against the authority image on 2026-09-20.
last_reviewed: 2026-09-20
audit:
  passes: 0                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: null              # YYYY-MM-DD
  last_pass_state: null        # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the corridor query family

> **Why a `family` and not five contracts.** These five entries share one shape: *agent or point
> pair, plus geometry, in; a small non-negative integer out.* They call each other, they share the
> leaf accessors, and they share the conventions in §4 that a reimplementation gets wrong
> together or not at all. Splitting them would repeat those conventions five times and let them
> drift. Splitting them by *function* would be worse still — `PVAL` alone is nine steps over four
> of the others.
>
> **What this contract is NOT.** It does not restate the navigation mechanism. The mesh, the
> search, the portal cost rule and the step-follower are
> [the nav-mesh page's](how-a-unit-finds-its-way-across-the-navigation-mesh.md) subject and are
> unchanged by anything here. This contract is the **query layer above them**.

## 1. Purpose

Before a unit commits to moving, something has to answer *"can it actually go that way?"* — is the
straight line clear, is a body in the corridor, is the agent's own path blocked, does the swept
capsule touch a wall. This family is those questions. Each entry takes the agent (or a pair of
points) and some geometry and returns a small integer verdict; nothing here moves anything,
allocates anything, or decides what to do about the answer.

## 2. Interface

All five are `__fastcall` (Microsoft x64). Float arguments occupy the **same argument index** as the
integer registers they displace, which is why `GATE`'s `ctx` is in `r9` while its radius is in
`xmm2` — they are arguments 3 and 2.

> **Two of these already had names in this store and this contract uses them.** `00335B60` is
> **`TestForwardStepClearance`** and `003357B0` is **`QueryDynamicActorObstruction`**, both named on
> [the battle-locomotion page](Battle-Locomotion/battle-locomotion-steering-and-recovery.md). I wrote
> this contract from SWE2-ORACLE's working labels (`PVAL`, `GATE`) and found the existing names only
> when checking which subsystem owns the page - a check that should have come first. The labels are
> kept as short aliases because the experiment records use them throughout, but **the store's names
> are the names.** They also corroborate the verdict table below from a document written by someone
> else: a *clearance test* returning `0` for usable, and an *obstruction query*, are exactly the
> polarities §2 derives from the disassembly. The other three entries have no name anywhere in the
> store, so their labels remain ORACLE's.

| entry | size | parameters | returns |
|---|---:|---|---|
| `TestForwardStepClearance` (`PVAL`) `00335B60` | 748 B | `rcx`=agent, `xmm1`=angA, `xmm2`=angB, `xmm3`=tol, `[rsp+0x28]`=cap, `[rsp+0x30]`=flags | `0`, `1` or `2` |
| `QueryDynamicActorObstruction` (`GATE`) `003357B0` | 943 B | `rcx`=posA, `rdx`=posB, `xmm2`=rad, `r9`=ctx, `[rsp+0x28]`=excl, `[rsp+0x30]`=flags | `0`, `1` or `2` |
| `PATHW` `0033A3D0` | 405 B | `rcx`=A, `rdx`=B | `0` or `1` |
| `BLKCHK` `00335F90` | 161 B | `rcx`=agent | `0` or `1` |
| `LQUERY` `00391410` | 758 B | `rcx`=p1, `rdx`=p2, `xmm2`=rad | `0` or `1` |

**The stack arguments are CALLEE-relative `+0x28`/`+0x30`.** The caller writes them at its own
`rsp+0x20`/`rsp+0x28` before the `call`; after the return address and the callee's own prologue they
are read at `+0x28`/`+0x30`. EXP-134 records an intercept that first read the callee's `rsp+8`/`+0x10`
— the caller's shadow space, which is always zero — and got a silently degenerate answer. **A
reimplementation or an instrumentation harness must resolve these two slots explicitly.**

### Return semantics

**Every non-zero exit returns a LITERAL small integer, never a callee's own value.** `BLKCHK` is the
clearest case: three different probes can decide it, and all three converge on `mov eax, 1`
(`0x33601C`). A port that returns the probe's result instead will agree on zero-versus-non-zero and
disagree on the value.

| entry | `0` | `1` | `2` |
|---|---|---|---|
| `PVAL` | the proposed direction is usable | rejected — by the gate, the mode-3 query, the walk/width probe, or the LOS query | reached only when `GATE` returned `2`, via `cmove` at `0x335E0D` |
| `GATE` | nothing in the corridor | a candidate was **accepted** as blocking (`r12d != 0`) | no blocker, but candidates were **counted** (`esi != 0`), `neg esi / sbb eax,eax / and eax,2` |
| `PATHW` | **no route** | **a route exists** | — |
| `BLKCHK` | corridor clear | corridor blocked | — |
| `LQUERY` | nothing hit | first non-zero capture | — |

**`PATHW`'s polarity is derived, and the derivation is given because it is counter-intuitive.** The
control flow is proven from the image:

```
Q(B→A,1) != 1                         → return 1
Q(B→A,1) == 1 → for θ in {+π/4, −π/4}:
                  w = B + R(θ)·((A−B)·0.5)
                  Q(B→w,1) == 1       → this round continues
                  else Q(w→A,1) == 1  → this round continues
                  else                → return 1
                both rounds continued → xor eax,eax → return 0
```

Reading `QWALK == 1` as *"blocked"* — which is how `BLKCHK` uses it at `0x335FDF` — this says: return
`1` when the direct segment is **unblocked**, or when a half-way lateral detour is **fully**
unblocked; return `0` only when the direct segment is blocked *and* both detours have at least one
blocked leg. **So `1` means a route exists.** The control flow is `PROVEN`; the polarity inherits
`BLKCHK`'s reading of `QWALK` and is marked `HIGH` in §15 rather than `PROVEN`.

> **`0x33A40B` is not a dead tail.** It is `mov eax, 1` / `jmp 0x33A544`, the shared return-1 exit,
> reached from the direct-probe fall-through and from both round-failure branches. See `CON-130`;
> an earlier reading of it as `add [rax],al` came from decoding one byte late.

## 3. Types

This family **declares one type of its own**, the agent (`CorridorNavAgent`, declared 2026-09-25). It reads three that the store
already declares, plus one BSS parameter block (now covered by `NavGridParams`).

| what | where | status |
|---|---|---|
| the agent's nav sub-record | `*(agent + 0x108)`, fields `+0x10C` (f32 scale), `+0x110` (f32 radius), `+0x174` (u8 mode) | ~~UNRESOLVED as a type~~ **RESOLVED 2026-09-25 (OPUS): it is `BattleUnit + 0x80`, an interior pointer.** The agent initialiser `00336710` stores its source there (`003367B4`), and every path passes `BattleUnit + 0x80` (`lea … + 0x80` at `0023406F`, `00308673`, `00317E9D`, `00325BC4`, `002FDC42`, `003048EF`, `003105F9`). The three fields are declared `BattleUnit` rows: `+0x18C collisionExtentA`, `+0x190 collisionExtentB`, `+0x1F4 placementMode` |
| the agent itself | `rcx` of every entry | **declared 2026-09-25 (OPUS): `CorridorNavAgent`, 0x110** — a stack local built by `00336710` below the cookie at `rsp+0x130` (`00336CE0`, `0033A120`); its first four rows copy `BattleUnit` +0xE0/+0xF0/+0x100/+0x110 with w = 1.0 |
| `ActorManagerSlot` | `ARRAY 0x02098E10 stride=0x288 count=5`, reached by `N63FF0 00263FF0` | declared |
| `ActorStorageRecord` | via the packed actor handle — see below | declared |
| the nav-grid BSS block | `0x2AEDFB0` root, ~~`0x2AEE070` cell size, `0x2AEE078`/`0x2AEE080` eps cells~~ `0x2AEE070`/`0x2AEE078` origins, `0x2AEE080`/`0x2AEE088` maxima, `0x2AEE090` cell size (corrected 2026-09-27, OPUS: the builder `003924B0` stores the getter's minima, maxima and floorf(refined) + 1.0 there; ASTRA nav-grid-quantization, _index/candidates/nav-grid-consumers/), `0x2AEE0B0` mask base | ~~not a declared type~~ **declared**: `NavRunStateBlock` behind `PTR 0x02AEDFB0` (0x30) and `NavGridParams` (0x60 at `0x02AEE060`, covering `070/078/080/088/090/0B0`); all BSS, all ship zero |
| the shared axis basis | `0x8C5F80`…`0x8C5FE0`, six 16-byte rows `+X +Y −Y +Z −Z W` | shipped const, documented on the dyngeo page |

**The packed actor handle is this family's identity ABI.** `GATE` resolves its own identity with
`movzx ecx, byte [ctx+0xEA9]` → `GTAB` → `mov ecx, dword [rax+8]` → `MABE`, and that **32-bit** value
decodes as:

| bits | field | role |
|---|---|---|
| 31 | — | unused |
| 30–20 | `ActorStorageRecord.handleTag11` | staleness tag; cycles `1..0x7FF`, period 2047, never `0` |
| 19–16 | `ActorStorageRecord.handleTag4` | the owning `ActorManagerSlot`'s index, bounded `< 5` |
| 15–0 | `ActorStorageRecord.selfIndex` | index into that slot's `recordPool` |

A stale handle resolves to **null**, not to the wrong actor (`cmovne rax, 0` at `0x358925`), so the
walk's `h == self` skip simply skips nothing. See `CON-131`.

## 4. Preconditions · postconditions · invariants

**Preconditions.**

1. **Several leaves have no null guard and the caller carries that obligation.** `OBJD` is
   `q[h+0x30]` unguarded (`h == 0` faults at `0x263E30`); `O1F2` and `O1F3` read `b[obj+3]` with no
   check; `MABESP` runs `q[T+8]` unconditionally after the table select, so a null table faults at
   `0x3588EB` rather than returning `0`. **Only `O1F` and `O3FW` guard their object.**
2. `PVAL` requires the agent's `+0x108` sub-record to exist; it is dereferenced without a check.
3. `LQUERY`'s root comes from `ROOTL 00383840`; a null root exits early with `0`, so this one is
   guarded.

**Postconditions.** A verdict in `eax`, zero-extended. **No argument is written** except `LQUERY`'s
record-mask scratch and `CPSEG`/`RDEC`-style out-parameters, which are caller-supplied.

**Invariants.**

- **The family writes no global on any path that returns.** Across its 102-body call closure there
  are exactly two rip-relative global write sites and no absolute ones: `RDEC`'s packed scratch at
  `0x22D91B0` (see `CON-135` — the published figure was wrong by `0x3C000`), and seven cells inside
  `__report_gsfailure 00809654`, which is reached only when `__security_check_cookie 00808C40` fails
  and **does not return**.
- **No verdict depends on a random draw.** See §9.
- **The mode byte is re-read.** `BLKCHK` loads `b[sub+0x174]` into `esi` at `0x335FB5` and uses it
  for both `PRED` and `QWALK`, but the `mode == 3` test at `0x335FEB` **re-loads `q[agent+0x108]` and
  re-reads the byte**. If either probe mutates it, the third test sees the new value. A port that
  caches the mode once is not equivalent.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | agent `+0x20` (position), `+0xE0`, `+0xF0`, `+0x108`→`+0x10C`/`+0x110`/`+0x174`; ctx `+0xEA9`, `+0x1F4`; object `+0x3`, `+0x10`, `+0xC0`, `+0x30`, `+0x698`, `+0x714`; nav BSS `0x2AEDFB0`, `0x2AEE070/78/80/B0`; consts `0x8FCC8C` (0.9f), `0x8F30F8` (0.2f), `0x8F3108` (0.8f), `0x1CEBB70` (0.5f), `0x1CEBDA0` (sign mask), `0x908E30` (1/4096), `0x8C5F80`… | read from the image 2026-09-20 (OPUS); executed EXP-132…137 |
| written | **nothing global on a returning path.** `RDEC` scratch `0x22D91B0`; `BMASK` memsets and ORs a caller-supplied record mask | 102-body closure write census, 2026-09-20 (OPUS) |
| allocated | **nothing** | same census — no allocator is in the closure |
| deallocated | **nothing** | same |

*Census blind spot, stated because a negative is being claimed: it resolves `rip`-relative and
absolute destinations and classifies register-based ones by base register only. A write through a
register that happens to hold a global address would be counted as "through a register" (171 sites),
not as a global. The claim is therefore **no global write by a rip-relative or absolute form**.*

## 6. Relationships

**Callees, by layer.** `PVAL` → `GATE`, `AGENTQ 00318CA0`, `QWALK 0033D3E0` or `PRED 00335E50`,
`LQUERY`, `DE6A0 0032A6A0`. `GATE` → `GTAB 00236820`, `MABE 0031ABE0` → `MABESP 003588B0` →
`N63FF0 00263FF0`, `GCHK 002EA7F0`, `GPT`/`GSEG`, `GFILT`, and the accessor leaves. `BLKCHK` →
`PRED`, `QWALK`, `AGENTQ`. `PATHW` → `QWALK` ×5 and the transform primitives. `LQUERY` → `ROOTL`,
`BMASK 003912E0`, `CAPT0 00468D50`, `CAPT1 00468E50`, `CPSEG 004691A0`, `TRIGD 00468580`,
`RDEC 0032A6E0`.

**Shared with other contracts.** The transform primitives (`MLOAD`, `RBUILD`, `ROTCOL`, `MXV`,
`MXVW`, `VADD`, `VSUB`, `VSCALE`, `NORM`, `XPROD`) belong to
[`CONTRACT-transform-primitives.md`](../00-Engine-Core-Runtime/CONTRACT-transform-primitives.md) and
are not re-specified here. The actor handle decode is shared with
[`CONTRACT-manager-slot-entry-tables.md`](../04-Actor-Entity/CONTRACT-manager-slot-entry-tables.md).
**No entry in this contract appears in `CONTRACT-facing-and-steering.md` or
`CONTRACT-movement-body-pool.md`** — checked entry-by-entry before this document was created.

## 7. State transitions

**None.** This family is a set of predicates: no entry advances a state machine, sets a mode, or
records that it ran. That is itself the contract — a caller may invoke any of these repeatedly
within a frame and observe the same answer for the same inputs.

## 8. Script · resource · event interactions

**None directly.** No opcode, verb or authored table reaches these entries. The nav data they read is
loaded by the field/area layer before they run; `ctx+0xEA9` is planted by whoever built the context.

## 9. Determinism

- **RNG — none.** A call-closure walk from the five entries reaches **102 bodies**, and **not one**
  of the fourteen generator entries named by
  [`CONTRACT-gameplay-generators.md`](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) and
  [`CONTRACT-which-generator-serves-which-roll.md`](../21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md)
  is among them. **The corridor query is a pure function of agent state, geometry and nav data.**
  This distinguishes it sharply from the scripted-camera family, which draws from the gameplay MT.
- **Timing / ordering.** Callers run inside the movement update; the nav root and pools must already
  be populated. Nothing here depends on a frame counter.
- **Threading.** Single-threaded in the observed callers. `RDEC`'s scratch at `0x22D91B0` is a
  **shared global buffer**, so two concurrent `RDEC` calls would race — nothing in this family
  protects it. Not a live-observed hazard; recorded as a structural one.

## 10. Failure paths and edge conditions

The ones that change behaviour, not every arithmetic edge:

1. **Ordered-vs-unordered compares decide real branches.** `PVAL` step 1 is `ucomiss tol, 0` with
   *both* `jp` and `jne` continuing, so **NaN `tol` proceeds** and only an ordered zero returns
   early. `CAPV`'s `t > 1` test is `ja` — ordered only — so a NaN `t` falls into the lerp and
   produces NaN coordinates that propagate into the distance.
2. **`cvttss2si` on overflow or NaN yields `0x80000000`** - that instruction fact stands, ~~so an out-of-range
   coordinate becomes a very negative cell index and is rejected downstream rather than at the conversion.~~
   What happens to an out-of-range coordinate depends on the function (corrected 2026-09-27, OPUS; ASTRA
   `nav-conversion-domain`, re-read in `_index/candidates/nav-conversion-consumers/`):
   - **`00383F10`** (the grid region query) exits before either conversion: its four ordered bounds (`ja` at
     `00383F77` / `00383F93` / `00383FAF` / `00383FCD`) and its classifier branch run first, and the origins are
     s16 and the sizes and counts u8. So for stable finite inputs the converted values are `0..65025`, never negative.
     There is no index-range test after the conversion either (item 8).
   - **`LQUERY`** (`00391410`) converts its box edges with no bounds before them, and `003912E0` clamps each index
     ~~to `[0, count - 1]`~~ **piecewise: `i < 0 ? 0 : min_signed(i, count - 1)`** (qualified 2026-09-28, OPUS; ASTRA
     `nav-mask-zero-count`). Each negative path zeroes its register and **jumps past** the upper clamp, so a negative
     index, including `0x80000000`, becomes 0. The coordinate is clamped, not rejected. The result lies in
     `[0, count - 1]` **only for positive counts**: with a count of 0, a non-negative index becomes -1, and
     `003912E0` has no zero-dimension exit before its loops. That is a source calculation, not an observed read, and
     whether game state ever has an empty dimension is not established. Do not substitute `min(max(i, 0), count - 1)`
     or `max(min(i, count - 1), 0)`; they differ at count 0.
3. **`angB == 0` skips the `cosf` divide** in `PVAL`; NaN or non-zero both take it.
4. **`GATE` returns `0` immediately when `GCHK` fails** (`0x335822`), before its register saves —
   a legitimate early exit, not a truncated one.
5. **`PATHW`'s probes are asymmetric**: `Q(B→w)` then `Q(w→A)`, flag `1`. A test corpus built around
   `A→w` never reaches the second probe's branch at all.
6. **Stale handle ⇒ null, not wrong actor** (§3). Fails safe, silently.
7. **`LQUERY`'s record-mask bits live at `mask + 0x10 + i/8`** — a 16-byte header. A fixture planting
   bits at `lsrc+0` produces all-zero parity on both sides and looks like agreement.
8. **The grid region query `00383F10` admits the exact upper edge, and its cell index is unguarded**
   (added 2026-09-27, OPUS, re-read from the bytes; ASTRA `nav-upper-bound-admission`, bff8d55d0).
   - The lower checks reject only `origin > x` and the upper checks at `00383FAF` / `00383FCD` are `ja`
     against `origin + count × size`, so both edges are admitted.
   - The index `trunc(z − oZ) / cellH × cols + trunc(x − oX) / cellW` is loaded at `0038402C` with no
     bound check. At `x == upperX` the column equals `cols` and aliases the next row's first cell; at
     `z == upperZ` the row equals `rows`, past the table.
   - **The precondition is on the computed indices, not the world coordinates.** A strictly smaller X is
     not enough: with origin −32768, cellW 255 and cols 255, X = 32256.998046875 (one f32 ULP below the
     upper edge 32257) has an exact distance on a rounding midpoint, and `subss` rounds it to 65025.0, so
     the column is 255. A caller or reconstruction must keep each computed column and row inside its
     declared count, with non-zero cell sizes and valid table storage.
   - Fixture evidence only (isolated original instructions, synthetic grids). Whether ordinary callers
     produce such points is not established.
   - **What lies past the table, on the one retained authored grid** (added 2026-09-28, OPUS; ASTRA
     `authored-grid-shape`, slot SHA-256 `b5d6da52...9626`, check T in `_index/candidates/nav-grid-consumers/`).
     The table is `u16` at `decode(grid+8)` and the list pool is at `decode(grid+0xC)` (`00383F2E`). An entry of
     `0xFFFF` is an empty cell (`00384031`). Any other entry is an offset to a `0xFF`-terminated region list.
     - In alc0102 slot 4 (10 x 10), the table is exactly `cols x rows` = 100 entries, then 8 zero pad bytes, then
       the 192-byte pool.
     - A row index equal to `rows` reads, per entry:
       - 100-103: the pad, which gives offset 0, an empty list;
       - 104 and 108-110: `0xFFFF`, an empty cell;
       - 105-107: pool bytes read as offsets, all outside the pool.
     - So the out-of-range read may be harmless or not, depending on the bytes that follow. The authored layout
       gives no guard.
     - One decoded sample only. No load, allocation, other pack's padding or live scene is claimed.
9. **The grid builder `003924B0` needs more than positive extents** (added 2026-09-28, OPUS, re-read from the
   bytes; ASTRA `nav-grid-initial-truncation`). It sizes a provisional cell `c0 = sqrtf(w × h / 275)` (`00392587`),
   then takes **truncating** counts `nx = cvttss2si(w / c0)` and `ny = cvttss2si(h / c0)` (`003925A9` / `003925CE`),
   and divides each extent by its count (`003925E9` / `003925FC`) with no zero test before `maxss` hands the larger
   to `floorf` (`00392607`).
   - A thin positive rectangle truncates one count to 0. For w 1 and h 400, `nx` = 0, and `+inf` reaches `floorf`.
   - So the constructor's input domain is: each of `w / c0` and `h / c0` at least 1, not merely `w, h > 0`.
   - This is evidence at a supplied post-`sqrtf` boundary: the original instructions ran, the `sqrtf` result was a host
     prediction. Native `sqrtf` / `floorf`, the rest of the constructor, and whether any authored grid is this thin are
     not established. The getter's byte encoding of such a rectangle is representable, but it is not an observed record.

## 11. Observable behaviour

From outside the process: a unit refusing to walk into a gap it could physically fit through, or
accepting one it cannot, is this family's answer changing. In memory, each entry's verdict is
observable directly at its `ret` — these are pure functions, so **a differential test can call them
with planted state and compare `eax` byte-for-byte**, which is exactly what EXP-132…137 did.
`RDEC`'s scratch at `0x22D91B0` is observable after a call. Nothing here is visible in a save file.

## 12. Reproduction formula

`BLKCHK(agent)`, the smallest complete member, with real constants:

```
sub   = *(void**)(agent + 0x108)
scale = *(f32*)(sub + 0x10C) * 0.9f            /* 0.9f at 0x8FCC8C */
mode  = *(u8*)(sub + 0x174)
if (PRED(agent, agent + 0x20, scale, mode) != 0)          return 1;
if (QWALK(agent, agent + 0x20, mode)       == 1)          return 1;
if (*(u8*)(*(void**)(agent + 0x108) + 0x174) == 3)        /* RE-READ, see §4 */
    if (AGENTQ(agent, agent + 0x20, 0, 0)  != 0)          return 1;
return 0;
```

`PATHW`'s waypoint, in evaluation order: `d = A − B` (`VSUB`); `d *= 0.5f` (`VSCALE`, `0x1CEBB70`);
`M = identity` (`MLOAD`, rows `0x8C5F80/90/B0/D0` of the axis bank); `θ' = AWRAP(θ)`;
`M = RBUILD(M, θ')`; `w = MXVW(M, d)`; `w = w + B` (`VADD`, `0x202B10` — **not** `MXV`).

## 13. Runtime validation

| claim | how it was observed live | date | result |
|---|---|---|---|

**Empty, and that is the readiness ceiling.** Nothing in this family has been observed in the running
game. Everything below `RUNTIME VALIDATED` in the frontmatter follows from that, and it is why the
S-18 runtime column does not move on the strength of this contract.

## 14. Unresolved

1. **The agent's `+0x108` sub-record has no declared type.** Three fields are proven
   (`+0x10C`, `+0x110`, `+0x174`); the extent is unknown. *Resolved by:* a seeded receiver census
   over the sub-record pointer, not by bounding it from the three known offsets.
   **Resolved (OPUS, 2026-09-25, block 249): it is not a separate record. It is `BattleUnit` seen from `+0x80`.**
   The agent builder `00336710` stores its source argument at `+0x108` (`003367B4`). Its five callers pass their
   own `rcx`:
   - `lea rcx, [unit+0x80]` at `0030867A` and `00317EA4`: the live unit;
   - at `003019BF`, `lea rcx, [rsp+0x30]` in `AiOrder_CheckActionPreconditions(unit, order)` `00301830`. That
     function copies `unit+0x80..+0x68F` (0x610 bytes, `00301857`–`003018DA`) and overwrites `+0x40`, `+0xD0` and
     `+0x160` (`003019D0`–`003019DB`) before the query. **The corridor is asked about an edited snapshot of the
     unit, not the unit.**

   The three proven fields are therefore the already-declared `BattleUnit+0x18C` `collisionExtentA`, `+0x190`
   `collisionExtentB` and `+0x1F4` `placementMode` (BLKCHK `00335FAD` / `00335FB5` / `00335FEB`). The extent is
   `BattleUnit`'s (live) or 0x610 bytes (snapshot). **Traced (block 250):** the other nine call sites all pass the live
   `unit+0x80`: `002FDBC1`, `002FDD5B`, `00310758`, `00325BDC`, `00325D0A`, `00304D15`, `0030867A`, `00317EA4`
   and `00234076` (where the unit is `OBJD(actor)` via `0031B760`). Of ten call sites, nine use the live unit and one
   uses the snapshot.
2. **`QWALK == 1` is read as "blocked" from `BLKCHK`'s use of it**, which is what fixes `PATHW`'s
   polarity in §2. *Resolved by:* `QWALK`'s own contract, or a live observation.
3. **`GATE`'s candidate population is a fixture.** The walk is executed; what the shipped game puts
   in the collector is not. *Resolved by:* a live capture of the collector output.
4. **Five one-hop boundaries remain scripted** — `EF2B0`, `F4F0`, `F430`, `EB0`, `D5A0`. Their
   contracts are fixture agreements, not native authority. **Resolved (SWE2-CONTRACT, static body
   reads — the fixture agreements are confirmed where they touched the truth, and corrected where
   they didn't):**
   - **`EF2B0` `002EF2B0` (20 B) — not a policy at all.** `call 002EF640; add rax, 0x200; ret`:
     `SaveImage_GetActiveBuffer` is `lea rax, [02164280]`, so the return is the constant
     `02164480` — the save-image persistent-payload base. The scripted `ef2rets` agreement was
     exact; there is nothing else to learn. (Same field the persistent-flag-banks contract
     censuses.)
   - **`F4F0` `002324F0` (624 B) — a nearest-edge selector, not a pure predicate.** `dx` is a
     signed word index ×0x20 into `[rcx+0x10]`'s subrecords; it then runs a **fixed three-edge
     loop** (`cmp ebx,3`) over vertex-index pairs in the `00908DE8` table into `[rcx+8]`'s
     16-byte vertices. Per edge it writes a normalized segment frame into the caller's ctx `r8`
     (endpoints at `+0x10`/`+0x18`, deltas vs the query point at `+0x20`/`+0x30`, length-normalized
     via `00861F14`, denom at `+0x3C`, a `+0x54` degeneracy gate tested against `B8D1B717`), then
     scores `|dot(P0→Q, dir)/den − 0.5|` — the query point's projection distance from the edge
     **midpoint** — and keeps the minimum. `eax` = argmin edge index 0–2, or −1 when all three
     edges fail the `den ≤ 38D1B717`/`+0x54` gates; the callers' sign test is `eax < 0`. Caveat the
     fixture hid: **the ctx is overwritten per edge** — on return it holds edge 2's frame, not the
     winner's; the winner lives only in `eax`/`r12d`. A port that reads the ctx as "the selected
     edge" is wrong.
   - **`F430` `0022F430` — `N315E0`'s ctx writer *and* walk driver; the fixture planted only the
     write half.** It seeds the ctx from `rdx`: `w[+0x44]=0`, `w[+0x42]=−1` (no-hit), the delta
     vector `[+0x18]−[+0x10]` at `+0x00..+0x0B` with its length at `+0x30`/`+0x34`, and `w[+0x3C]`
     from `00233050(rdi, [rbx+0x18])`. The radius constant is selected by `rdi == 0026E500()` —
     `1.8f` (`00908E1C`) when equal, `0.09f` (`00908E18`) otherwise. It then walks the `00908DF8`
     sentinel list: per cell it forms `w[+0x3E]`/`w[+0x40]` from the `[rdi+0x20]` column table and
     calls **`qword [rbx+0x28]`** — the planted per-cell edge callback (`D4B0` in production). On a
     band hit (`xmm7` inside the `[?, xmm8)` gate) it commits `w[+0x42]`, `w[+0x44]` and stores
     `xmm6` to `[[rbx+0x20]]` — the hit position. The scripted `D0D0` intercept covers a real call:
     `F430`'s region query is one step inside the walk, not the whole body.
   - **`EB0` `00381EB0` — point-in-unit-shape, dispatch on `dword [shape]`** — confirmed the
     primitives page. `00202B70(&local, shape+0x50, point)` applies the inverse transform, then:
     type 0 → sphere `x²+y²+z² < 1` (`seta`); type 1 → cylinder `|y|<1 ∧ x²+z²<1`; type 2 → box
     `|x|,|y|,|z| < 1`; type ≥3 → `0`. `eax` ∈ {0,1} — a real bool, matching `eb0rets`.
   - **`D5A0` `003DA5A0` (246 B) — capsule-pair *horizontal* distance.** Per capsule:
     `003A1D30(003DA730(capsule, otherPos))` (the anisotropic metric pair already owned in
     04-Actor-Entity) plus radius `[capsule+0xC]`. Returns `xmm0 = sqrt(Δx²+Δz²) − (mA+rA+mB+rB)`
     via double `sqrt` `00861F5C`; negative means overlapping. Optional out `r14` receives
     `{Δx, Δy, Δz, horizontalDist}` — the XZ-only form the fixture's `d5rets` approximated.
     The `Δy` is written to the out-vector but **never enters the distance** — a port that uses
     full 3-D distance is not equivalent.
5. **`RDEC`'s shared scratch is unsynchronised** (§9). *Resolved by:* establishing whether any
   caller can run concurrently.
   **Resolved (OPUS, 2026-09-25, block 267): no caller can run concurrently.** `0x22D91B0` lies inside the
   emulated EE/VU0 register bank (`EeVu0RegisterBank`, `022D8F10`..`022D949F`), and `RDEC` `0032A6E0` is a
   census member of that bank (`00-Engine-Core-Runtime/Shared-Transform-Workbench/members/ee-register-census.tsv`,
   class A). The bank page's thread question was answered on 2026-09-18 (FABLE): no worker thread reaches
   any member by a direct call, and the thread pools carry no jobs, so **the bank has exactly one user
   thread**. The scratch is therefore not shared across threads. It is still shared across *calls*: the
   next bank user can overwrite it, as for any emulated register (§9).

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the five signatures and body sizes | read from the image 2026-09-20 (OPUS) | NATIVE/STATIC | PROVEN |
| every non-zero exit returns a literal | `BLKCHK` `0x33601C` read; all five entries' tails read | NATIVE/STATIC | PROVEN |
| `PATHW`'s control flow | all 405 bytes read 2026-09-20 (OPUS); `CON-130` | NATIVE/STATIC | PROVEN |
| `PATHW`'s **polarity** (`1` = route exists) | derived from `BLKCHK`'s use of `QWALK == 1` | INFERENCE | HIGH |
| the arithmetic and fault behaviour | EXP-132…137, 1,531 cases / 1,281 mutants, `c36dcda20` | NATIVE-REPLAY | PROVEN for the bodies |
| no RNG in the family | 102-body closure vs 14 declared generator entries | NATIVE/STATIC | PROVEN |
| no global write on a returning path | 102-body closure write census, with the blind spot in §5 | NATIVE/STATIC | PROVEN as bounded |
| the packed handle decode | `003588B0` read in full; encoder `0046BE80` agrees | NATIVE/STATIC | PROVEN |
| the five one-hop boundaries' native semantics | `002EF2B0`, `002324F0`, `0022F430`, `00381EB0`, `003DA5A0` bodies read from the authority image (SWE2-CONTRACT): EF2B0 = payload-base constant `02164480`; F4F0 = 3-edge argmin-midpoint-projection selector returning −1 on all-reject, ctx holds the *last* edge's frame not the winner's; F430 = ctx writer *and* walk driver calling `qword[ctx+0x28]`, radius `1.8f`/`0.09f` selected by `rdi==0026E500()`; EB0 = type-dispatched sphere/cylinder/box unit-membership bool; D5A0 = XZ-only capsule distance minus summed metrics, `Δy` written but unused | NATIVE/STATIC | PROVEN |
| production integration | **none** | — | UNRESOLVED |

**Not summed.** The replay tier proves what the bodies compute over a disclosed synthetic fixture.
It is not evidence about what the shipped game passes them, and nothing in this contract should be
read as if it were.

## 16. Parity plan

**Testable now, from this document:** `STRUCTURAL` (the five signatures and the callee-relative stack
slots), `CONTRACT` (verdict values, including the literal-`1` convention), `CALCULATION` (the
reproduction formulas in §12), `EDGE-CASE` (the ordered/unordered compares and `cvttss2si`
indefinite in §10). EXP-132…137 already exercise all four.

**Explicitly NOT tested, and why:**

- `RNG` — **not applicable**, and that is a finding rather than a gap: §9 establishes there is no
  draw to test.
- `STATE-TRANSITION` — not applicable; §7 establishes there are no transitions.
- `SERIALIZATION` — nothing here reaches a save file.
- `TIMING` and `INTEGRATION` — **untestable without a live capture.** The candidate population, the
  call frequency and the ordering against the rest of the movement update are all unobserved.
- `PRESENTATION` — the visible effect is indirect (a unit's route), so it cannot discriminate this
  family from its callers.
- `FULL SUBSYSTEM` — blocked on the same live capture as `INTEGRATION`.

`00319110` (40 B) is the dual optional-vector copy: it writes the 16-byte value at `rdx` - or `rcx + 0x50` when `rdx` is null - into `rcx + 0x80`, then the 16-byte value at `r8` - or `rcx + 0x50` when `r8` is null - into `rcx + 0x90`, giving the corridor query record its two defaulted source vectors in one call.

Interior anchor `00319119` (function `00319110`).

## Cross-subsystem neighbours — batch-145 addition (SWE2-EC7)

**CombatAction — CLIENT.** `00319110` is a Movement-owned dual-source-vector default on this page whose only inbound edges are the CombatAction callers `002FDA60` and `00304850` - combat bodies consume the corridor query's defaulted-argument helper; the query itself never calls into CombatAction.
