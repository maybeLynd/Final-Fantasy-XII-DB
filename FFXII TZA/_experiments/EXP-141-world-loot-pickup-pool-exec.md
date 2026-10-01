---
experiment: EXP-141
title: world-loot pickup-pool execution — the S33 five-op family
  (00319B10 / 00319CA0 / 00319600 / 00319920 / 003197B0) executes
  native under Unicorn through the real presentation dispatcher,
  presence helpers, object lookup, drop-tier classifier and
  pointer decoder; the full-pool head-eviction and
  one-despawn-per-tick behaviours are confirmed on shipping bytes
contract: 13-Rewards-Progression-Economy/CONTRACT-world-loot-pickup-pool.md
  (ASTRA-TRANSFER-ORACLE-S33-WORLD-LOOT; committed d6b7e2dce)
method: B
live_game: false
tool: evidence/loot-pool-exec/check.py
---
# EXP-141 — loot-pool-exec

**Status:** complete · **68/68 functional cases, 57/57 byte-precise
mutants killed, stable across three processes**
**Evidence:** `evidence/loot-pool-exec/` (`check.py`, `result.json`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base
`0x120000`

## Objective

Isolated original-code run of the S33 world-loot pickup pool,
transferred from ASTRA. Execute the five shipped bodies against
the §12 reproduction formula; distinguish init, creation,
full-pool eviction, expiry, collection, removal, callback
identity/order/arguments, inventory and presence boundaries, and
the uninitialized stack payload passed to presentation ops 4/5.
The fixtures are synthetic: they exercise the bounded predicates
on real bytes but say nothing about initialized-gameplay
reachability of those inputs.

## Body census

| VA | role | span |
|---|---|---|
| `00319B10` | INIT — 10-node unroll + PTAB tail | real |
| `00319CA0` | CREATE — scan/evict/append/copy/op1 | real |
| `00319600` | TICK — walk, state dispatch, despawn | real |
| `00319920` | COLLECT — 7-slot grant + counter + op3 | real |
| `003197B0` | REMOVE — op3 retire only | real |
| `00319A00` / `00319830` | collect/remove wrappers | real |
| `00319A20` | RARE — drop-tier classifier 0/1/2 | real |
| `0031E9F0` | TIER — class byte → btab → jtab arm | real |
| `0028F000` | PRES — op dispatcher → leaf calls | real |
| `002FB250` | PTAB — clears 10 presence flag bytes | real |
| `002FB2A0` | PCLR — presence clear; `>9` → −1 | real |
| `002FB2D0` | PPUB — publish 16B + flag; occupied → −2 | real |
| `0028EFE0`/`003FA730` | object state lookup | real |
| `0028EFC0`/`003FA6E0` | object create/lookup sibling | real |
| `00202C90` | 16-byte copy helper | real |
| `0020E600` | DECODE — `rax = ecx + q[0x1F83530]` | real |
| `0016D6A0` | GATE0 — shipped `ret 0` no-op | real |
| `00808C40` | `__security_check_cookie` | real (shipped cookie) |

Scripted boundary — five leaf calls, all reached through the real
dispatcher and traced at the call boundary:

- `003FA160` — presentation op1 (returns the stored handle);
- `003FAA10` — op2;
- `003FA820` — ops 3/4/5 shared leaf;
- `003FA900` — op6;
- `00300B80` — inventory grant (`inv:id:qty:arg`).

Everything else — pool walk, intrusive links, the class byte →
tier chain, the descriptor decode, presence-table flag logic —
executes as shipped bytes.

## Findings verified on native bytes

**INIT unrolls all ten nodes.** Each 0x60 node: state+stamp
zeroed as one qword at `+4`, links `+0x10`/`+0x18` cleared,
handle `+0x58` cleared, slot index `0..9` written; head/tail
globals zeroed; tail-jmps `002FB250` which clears the ten
presence flag bytes at `0x22BE7F0 + i·0x20`.

**CREATE scans `d[node+4]` with stride 0x60** — the state dword,
not the handle or a flag byte. On a full pool it retires the head
through presentation op5 *before* relinking, then reuses that
same node at the tail (`c-evict`: ten `pres1` creates, one
`pres345` eviction, eleventh `pres1`).

**The drop copy is 56 bytes** (three `movups` + one `movsd`) into
`node+0x20..0x57`; `d[node+4] = 1` arms state 1; the op1 return
is stored at `node+0x58`.

**The op1 payload carries the rare flag and a global-index table
value.** Stack frame `+0x20`: `{pos.xyz, 1.0f, rare, tblval}` —
the leaf receives `r8d = rare` (`+0x30`) and `r9d = tblval`
(`+0x34`). `tblval = TBLZ[gidx]` for `gidx ≤ 3`, else `ebp`
(0). **TBLZ is at `0x1EED3A8` and ships as the identity table
`[0,1,2,3]`** — so under shipped data `tblval == gidx`
(`c-tvalidx` patches `TBLZ[3]=0xBEEF` and observes
`pres1:2:beef:…`, proving the read is the table, not the index).

**RARE (`00319A20`) classifies each of the seven drop slots:**
skips `0xFFFF` and any id with `(id & 0xF000) != 0x1000`; a
qualifying drop's row is `decodelo + stride·(id−0x1000)`
(32-bit truncated) through `0020E600`; `b[row+9]` is the class
byte → TIER. Tier 1–5 returns **0** immediately; tier 6 sets
`r=1` via `cmove ebp, r12d` (`r12d = ebp−1 = 1`); otherwise the
default **2** stands. Early-0 fires mid-loop and overrides a
prior tier-6 result (`c-rare5` → 0).

**TIER's jump-table arms are compiler-interleaved**, not
sequential: `btab[class] → slot → ret` with arm returns
`[1,2,3,4,6,7,8,9,5]` — so class `0x13`→7, `0x12`→6,
`0x1A`→5, `0x10`→2; `>0x1A`→0 (`d-tier-13/1a/1b`).

**TICK walks the head list once.** Dispatch: state ≤0 → skip;
state 1 → object-readiness transition (`EFE0` handle lookup →
`d[obj+0x260] == 2` → publish presence via `FB2D0`, state→2);
states 2..6 → blink/presentation progression; state 7 → despawn
retire (op4, uninitialized payload slot) — **and the retire
clears the node's next pointer before the loop advance reads it,
so a despawn ends the walk: at most one retirement per tick**
(`t-despawn-mid`, `t-despawn-tail`).

**The handle is a truncated object pointer.** `003FA730` walks
the manager's intrusive list (`mgr+0x2490` at `mgr+0x7C70`)
comparing `rax == rdx` against the handle and returns
`d[obj+0x260]` — the object's state field. This settles the
UQ-137 mechanism on bytes.

**COLLECT grants all seven slots** skipping `0xFFFF`
(`inv:101:2:1`, `inv:202:1:1`, `inv:303:5:1`, four `0:0`
padding grants — `g-collect`), increments `CNT_G`, then retires
op3. **REMOVE retires op3 without grants or the counter.**

**Presence boundaries are range-checked.** `FB2A0` returns −1 for
unsigned slot `> 9` (`d-fb2a0-10`); `FB2D0` refuses to overwrite
an occupied slot — returns −2 without writing (`d-fb2d0-occ`).

**Ops 4/5 pass an uninitialized stack slot** to the dispatcher —
the payload qword at `f+0x20` is whatever the frame holds; the
harness records the observed residue without claiming it is
meaningful.

## Harness corrections made during bring-up (disclosed)

- **`TBLZ` was initially planted at `0x1ED13A8` — wrong by
  `0x10000`.** The real `lea rcx,[rip+0x1BD35C1]` resolves to
  `0x1EED3A8`. The symptom (load returning the index value) was
  misdiagnosed mid-bring-up as a Unicorn TCG writeback defect;
  the actual cause was the fixture patching the wrong address —
  the shipped table's identity contents made `r9 == gidx` either
  way. Corrected on bytes; no emulator defect exists.
- **The `ITD` fixture collided with `MGR`'s 0x8000-byte span**
  (`HEAP+0x62000` inside `0x40060000..0x40068000`) — the
  descriptor was zeroed by the later write, forcing every
  qualifying drop onto the class-0 → tier-1 → early-0 path.
  Moved to `HEAP+0x68000`.
- Tier expectations and ~20 mutant byte sites were corrected
  against the image (immediates after modrm/disp, REX-prefixed
  encodings, near-jump second bytes).

## Fixture disclosure

All globals are BSS/data cells; the harness plants:

- pool `0x2EC0FA0` (10 × 0x60), head/tail `0x2EC1360/368`,
  field clock `0x208D45C`, counter `0x22C3174`;
- `q[MGR_G]` → fixture manager with the intrusive object list at
  `+0x7C70`; planted objects carry `d[+0x260]` state and
  `b[+0x272]` flag;
- `q[ITD_G]` → descriptor `{stride=0x20, enc=IROWS−BASEP}`; the
  `BASEP` pool holds item rows with `b[+9]` class bytes;
- `q[BASECELL]` = `BASEP`; `GIDX_G`, `GGATE_G`, `SCAL_C`
  (ships 1.0f) as documented;
- `TBLZ` override only in `c-tvalidx` (disclosed data patch —
  the shipped bytes `[0,1,2,3]` are restored everywhere else).

These are **synthetic supplied pools, descriptors and rows** —
they exercise the bounded predicates on real code but say nothing
about initialized gameplay reachability or the real table
populations. MODEL-PROVEN-tier fixtures on native bodies; the
executed control flow, field offsets, callback order/arguments,
memory effects and fault residues are original behaviour.

## Cases (68)

- **INIT:** zeroing/layout/idempotent re-init (`d-init`,
  `d-init-idem` on a dirty pool).
- **CREATE:** empty/mid/full scans, `d[node+4]` scan field, 0x60
  stride, head eviction + tail reuse (`c-evict`), `op1ret0`
  null-handle, null manager, `gate0` arm (`c-gate`), GIDX table
  path (`c-tvalidx`), rarity lanes (`c-rare2/5/6/7th/mask`).
- **TICK:** empty walk, state 0/8 skip, state-1 readiness
  transition (handle-0, no-flag, not-on-list, not-ready,
  occupied, null-mgr edges), blink 2/6, scalar gate
  (`t-scalar2`), despawn variants incl. mid-walk and tail —
  proving at most one retire per tick.
- **COLLECT/REMOVE:** grants, counter, op3, head/tail unlink,
  wrapper arg shapes (`w-collect2`, `w-negidx`, `w-idx10`,
  `w-remove0`).
- **Direct bodies:** presence clear/publish bounds and occupied
  refusal, dispatcher op0/2/6/7/null-mgr, decode, `EFC0`,
  `EFE0` hit/miss/deep/noflag, `RARE` 0/2 lanes, `TIER`
  classes `0x13/0x1A/0x1B`.
- **`life`:** dirty init → create (op1 plants handle OBJ) →
  tick @clk — the whole chain native.

## Mutants (57, all killed)

Scan/pool mutations (`+4`→`+5` scan field, stride `0x60`→`0x61`,
bound `0xA`→9, `je`↔`jne` on found/prev/next/tail), eviction op
(`5`→`6`, handle offset `0x58`→`0x59`), state store (`1`→`2`),
drop-tail `movsd` offset (`0x50`→`0x51`), op1→op2, `cmp gidx,3`
→2, gate `jle`→`jg`, RARE mask `0xF000`→`0xE000`, class bound
`0x1000`→`0x2000`, loop bound `7`→`6`, `cmove`→`cmovne`,
tier≤5 `jle`→`jg`, `ebp` default `2`→`3`, tier bound
`0x1A`→`0x19`; TICK dispatch compares/jumps, state bound `6`→`5`,
blink bound, despawn imm `7`→`6`, presence publish offset
`+0x10`→`+0x11` and flag `1`→`0`, clear bound `9`→`8`, store
`0`→`1`; FA730 flag/match/return-offset mutants; dispatcher
bounds; collect/remove call sites and offsets. Four first-pass
candidates proved equivalent (the `movsd` tail shift invisible on
an all-zero drop tail — hence the `c-rare7th` binding; the
`cmovne` flip needs a tier-≥6 qualifier at the line; the
`jle`→`jg` early-0 flip is absorbed when a tier-6 drop precedes
it — hence `c-rare6`; the loop-bound mutant needed the
classification itself at index 6) and were re-aimed rather than
declared.

## Limitations

- Synthetic pool/descriptor/row/manager fixtures: the bounded
  predicates are proven on original bytes; real gameplay pool
  contents and reachability remain fixture-tier.
- Five leaf calls are scripted at their call boundaries (the
  dispatcher, argument marshalling and return plumbing are all
  real).
- The uninitialized op4/op5 payload is recorded as observed
  residue; no claim is made about its initialized-gameplay value.

## Evidence tier

**NATIVE-REPLAY-adjacent**: original shipped bytes executed under
Unicorn on disclosed synthetic state. Fixture content is
MODEL-PROVEN; the executed instruction stream, branch outcomes,
callback order/arguments, memory effects and fault residues are
native authority for the bounded inputs supplied. Not
engine-in-loop; no claim that initialized gameplay drives these
inputs.
