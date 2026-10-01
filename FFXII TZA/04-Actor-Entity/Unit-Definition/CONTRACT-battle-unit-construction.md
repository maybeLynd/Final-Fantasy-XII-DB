---
contract: install a class-selected definition onto a reset battle unit while preserving native guard and rekey ordering
category: 04-Actor-Entity
scope: subsystem
level: L2
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md
entries: ["0023A570", "00236A60", "00236100", "00322050", "00322C50", "0023A7A9", "00328FF0", "002FEAB0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: "SECTION-01 re-read the original installer and selected callees, checked retained EXP-150 records, and executed independent original-CPU reset, reject/rekey, tracked-table, pulse-reset and blob controls. No live installation or full EXP-150 rerun."
last_reviewed: 2026-09-30
review_status: "Production correction; T2 peer review and canonical acceptance remain pending."
previous_review: "OPUS, 2026-09-20: carried page evidence and bounded EXP-075 guard results."
audit:
  passes: 1
  last_pass: 2026-09-30
  last_pass_kind: falsification
  last_pass_state: opus-unit-construction-falsification-pass-1
---

# Contract — battle-unit construction from its definition

Current statement after [SECTION-01](../../_experiments/evidence/continuation-section01-result-install/REVIEW.md).
**[page]** denotes the [mechanism page](how-a-battle-unit-is-built-from-its-definition.md);
**[EXP-075/150]** denote retained isolated-code experiments; **[SECTION-01]** denotes
new original-code reading and bounded CPU execution. Experimental case names are not
semantic type names: EXP-150's `in-member` uses selector class 1 (spawn-backed enemy),
and `in-foe` uses class 0 (party). The canonical mapping below is retained.

## 1. Purpose

Apply a definition ID to an existing BattleUnit: remember relevant old identity,
reset defined reuse state, choose the party or enemy data path, resolve authored
records and stats, initialize a fresh spawn when required, and install common state.
A failed apply is not a transaction that restores the previous unit.

## 2. Interface

`BattleUnit_ApplyUnitDefinition(BattleUnit *unit /*RCX*/, uint16_t id /*EDX*/)` at
`0023A570..0023AC7F`, 1,808 bytes. The low byte chooses the row and the next byte the
class. Return 1 denotes completed installation; 0 denotes a rejected/disabled path.
The original code is not a general safe API for arbitrary/null receiver or malformed
resource state. `0xFFFF` chooses the unsupported-class path used by teardown.

### Evidence restored by the owner (OPUS, 2026-09-25)

The SECTION-01 rewrite was published inside `69e9cad19` without the five citations the owner review
(`_index/candidates/section01-owner-review.md`) asked to be kept. Each was re-read from the image before
being restored here:

- **The id split.** `0023A580 mov eax, edx`, then `0023A585 sar eax, 8` / `0023A594 movzx esi, al` give
  class = `(id >> 8) & 0xFF`; `0023A58B movzx r12d, dl` gives row = `id & 0xFF`.
- **Teardown is "apply no definition".** In `BattleUnit_TeardownAndDespawn` the spawn at `+0x6A0` is
  released first (`00300F61`/`00300F68`). Then the unit is re-applied with `0xFFFF` (`00300F6D mov edx, 0xffff`,
  `00300F75 call 0023A570`).
- **The reset call site is `0023A5B0`** (`call 00236A60`, I2).
- **The party path nulls the spawn explicitly** (`0023AAB1 xor ebp, ebp`), so `+0x6A0` is null for a
  party unit (§3).
- **`EXP-047`** executed the two re-key wrappers' local stores; the delegate's effects remain static.

## 3. Types

The receiver is **BattleUnit**, not BattleStatsRecord. Its `+0x698` points to stats:
class 0 uses `q[02EBF190]+8+row*0x1C8`; class 1 uses the particular SpawnRecord's
embedded stats at `spawn+0x80`. `+0x6A0` is the enclosing enemy spawn, or null on
party installs. `+0xE68` is a separate authored class record, not interchangeable
with the stats pointer. `+0xE60` is the selected definition row. **[page]**

## 4. Preconditions · postconditions · invariants

**I1 — class 0 is party, class 1 is enemy.** Other classes execute
`and qword[unit], 0xFFFFFFFFFBFFFFFF` at `0023A633`: clear **bit26**, then return 0.
The same mask is used by the common terminal-state arm at `0023AC4B`, followed by
bit1 set; common success sets bit2. It does not clear bit42 (EXP-150's prose), nor
bit24 (the older page's terminal summary). **[page, SECTION-01]**
**A class-1 rejection keeps bit 26** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 343](../../_index/candidates/s14-opus-replay-enemy-install/README.md), which executed it 5/5; `0023A626`–`0023A662` and `0023A965`–`0023A9F4` re-read.)*. The enemy path's two early refusals jump to the shared
`return 0` at `0023A63A`, **past** the bit-26 clear at `0023A633`:
- placement bit 26 already clear (`0023A643`–`0023A648`);
- the row index above the table's count (`0023A65F`–`0023A662`).

Only a class above 1 falls through `0023A633` and clears the bit. *So a failed enemy install leaves the
placement armed, while an unknown class disarms it.*

**I2 — reset precedes the master-enable rejection.** `00236A60` clears defined reuse
fields, masks flags and restores sentinels. `d[02089300]==0` then returns 0. Reset is
not whole-object zeroing: `+0xEAC/+0xEB0`, for example, survive reset and are separately
cleared by the common successful path's pulse-reset call. With its optional cleanup
callback bridged, all-ones flags yield `0xFFEF7FB9FFE7B0E1`; this is a bounded measured
conjunction, not a claim about arbitrary callback effects. **[EXP-150, SECTION-01]**

**I3 — a return of 0 can follow identity changes.** The old word at stats `+4` is read
before reset when unit bit2 is set. Rekey selection occurs before the class dispatch.
Except for the explicit selected-teardown bypass at `0023A5CD..0023A5F2`, rekey occurs
when the incoming class byte is nonzero, or when the saved old ID is neither the
incoming ID nor `0xFFFF`. Consequently class 2 can rekey and then fail. The special
bypass prevents describing this as unconditional for every nonzero class. The wrapper
`00322050` clears `+0xEA4/+0xEA8`, invokes the inner resolver on `q[unit+0x10]`, then
stores the returned handle at `+8`. **[page, EXP-150, SECTION-01]**

**I4 — the class fixes the stats' owner and location.** Party and enemy paths install
different records belonging to their respective units. Party explicitly has no enclosing
spawn. Their shared layout is not evidence that they are one interchangeable object.
**[page]**

**I5 — preserve the actual bounds arithmetic.** On the enemy path, definition words
`+0`, `+0x22`, `+0x24` use unsigned comparison against a dword count minus one;
zero/missing counts wrap to `0xFFFFFFFF` and admit the 16-bit index at that guard.
The `+0x50` order join uses a zero-extended 16-bit count minus one and a **signed**
`jg`, so zero/missing count rejects. Passing a guard is not proof that later pointer
use is safe; missing descriptors/resolvers have separate effects. EXP-075 exercises
the two reward guards; EXP-150 adds retained coverage of the other cited guard paths.
The shipped-data reachability census is separately scoped on the page. **[page, EXP-075/150]**

**I6 — spawn initialization and counting share the freshness gate.** The enemy path
requires placement bit26. The spawn init, steal-availability setup and counter work
are inside `byte[spawn]&5 == 0`. Existing initialized spawns skip the entire block.
For an enabled counter slot, old count is stored at spawn `+0x12`, then the word count
increments or wraps to 1 at the cap; retained fixtures exercise `0x10->0x11` and
`0x34->1`. ~~The actual spawn-record initializer remains a scripted EXP-150 boundary.~~ **The spawn-record
initializer now runs real** on shipped area data *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 343](../../_index/candidates/s14-opus-replay-enemy-install/README.md), which executed it 5/5; `0023A626`–`0023A662` and `0023A965`–`0023A9F4` re-read.)*. The freshness gate is measured on both sides:
the initializer and the counter write happen together or not at all.
**[page, EXP-150, OPUS block 343]**
**The two reward rows are fixed here too** *(2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 343](../../_index/candidates/s14-opus-replay-enemy-install/README.md), which executed it 5/5; `0023A626`–`0023A662` and `0023A965`–`0023A9F4` re-read.)*. The install stores unit `+0xE70` as the row of table
`[02EBF148]` indexed by definition `+0x22`, and `+0xE78` as the row of `[02EBF140]` indexed by `+0x24`
(`0023A965`–`0023A9F4`). The row address is formed with a 32-bit `add ecx, eax`. These are the rows the
defeat sequence's gil and experience terms read. The stat rebuild indexes the same two tables by the same two
definition fields (re-read here; OPUS block 342 executed it) for the foe's main stat value
reads. So reward and stat terms are adjacent fields of the same authored rows. *No meaning is claimed for
either table.*

**I7 — tracked-HP registration is conditional.** `00328FF0(row, code, slot)` writes
only when `(code != 0 || slot < 0)` and `row < 2` under the original signed check.
The table is **`02EC1380`**, stride 24; the written dwords are `{slot, code}`.
The installer passes row 0 and a zero-extended byte slot, so its write requires a
nonzero code. It does not register every install. EXP-150 reads a different address
`02E81380` and makes no assertion on that observation; its record alone cannot prove
this table's writes. New controls verify the actual table and reject the wrong-base
mutation. **[SECTION-01]**

**I8 — pulse reset is narrow and the class-specific float paths differ.**
`002FEAB0` is a ten-byte body that zeroes the qword at receiver `+0xEAC`, covering
`+0xEAC/+0xEB0`, and returns. It is not a heavy float writer at `+0x2E0`.
On class 1, common `+0x6C` receives the class record's `byte+0x27` converted to float;
the `x1.5` multiplication is on class 0's `byte+0x2B` path. **[page, SECTION-01]**

## 5. State

Authored slots `02EBF120` (enemy), `02EBF130` (party), enemy joins
`02EBF150/168/148/140`, battle-state block `02EBF190`, text slot `02EBF170`, master
flag `02089300`, spawn-counter table `02089340+0x4014`, and tracked table `02EC1380`.
The selector/global state and old unit identity also influence control flow.

## 6. Relationships

Reset `00236A60`; spawn resolver `00236100`; rekey wrapper/inner `00322050/003220E0`;
validator `00322C50`; blob/string selector `002B58B0`; tracked writer `00328FF0`;
engagement selector `00237040` and its two branches; pulse reset `002FEAB0`.
The blob helper returns null for null input, returns a nonzero-header blob unchanged,
or skips a two-zero-byte prefix and then `n` zero-terminated strings. Negative/zero
`n` returns the first string. This is a bounded text selection rule, not a universal
resource decoder. **[page, SECTION-01]**

## 7. State transitions

```text
capture old identity where valid
reset defined reuse state
if master disabled: return 0
apply the exact rekey/bypass conditions
class0 -> party records and BattleSystemState stats; no spawn
class1 -> placement gate, enemy joins, spawn, gated fresh initialization
other  -> clear bit26; return 0
perform common identity/stats stores
choose engagement; clear pulse qword +0xEAC
terminal-state branch may clear bit26 and set bit1
set bit2; return 1
```

## 8. Script · resource · event interactions

Authored ARD/party tables supply data; scripts select definitions. The tracked gauge
and spawn history have downstream consumers identified on the page. Synthetic descriptor
plantings used in replay are not evidence that every malformed combination is shipped.

## 9. Determinism

The installer body has no direct random draw identified here. Outcome is conditional
on its complete input state: old identity, selector/master flags, bound tables,
spawn state/counters and callee results. Calling the spawn counter the *only* stateful
input would be incorrect.

## 10. Failure paths and edge conditions

Disabled master, unsupported class, missing placement, failed guards and unavailable
spawn can return 0. Reset has already occurred; some paths also rekey. Count-zero
unsigned guard acceptance is not safe-resource validation. A null receiver is not
made safe merely by the initial conditional old-ID read.

## 11. Observable behaviour

A unit obtains party or enemy identity and appropriate stats/spawn ownership, possibly
fresh spawn history and tracked-gauge registration. Teardown uses an unsupported
selector. No new live scene, save transition or player-visible outcome is certified
by SECTION-01's synthetic-state controls.

## 12. Reproduction formula

Preserve branch order and state effects on failed paths; the three unsigned and one
signed joins; conditional spawn setup and tracked registration; distinct party/enemy
stats ownership; and the separate pulse reset. Never derive bit numbers from a prose
label when the mask is available in the original instruction.

## 13. Validation and adjudication

EXP-075 retains fourteen guard controls with explicit no-effect callees. Those historical
limits remain true of that experiment, not of every later result.

EXP-150 retains **39 reported passing cases**, including **three private guard mutations**.
It executes many real callees but scripts `003220E0` — **subsequently executed by EXP-151** —
`00377C20` through the KO gate — **executed by EXP-153** (a 4-leaf chain, not the
400-instruction body earlier surveys decoded past its `ret`) — `00308010`, `003271D0`,
`003105D0` — **executed by EXP-161** as the unlink/reset helper — and `0023AC80` —
**executed by EXP-152** — (and implements memset). `00308010` and `003271D0` —
**executed by EXP-193** — remain scripted in EXP-150's own scope. It is neither a live installation nor a complete native
transitive call graph. The unsupported-class case begins with bit42 clear; its bit42
assertion cannot demonstrate the claimed clear.

EXP-151 (NATIVE-REPLAY, `live_game: false`) executed the rekey inner `003220E0` through
`00322050` end-to-end — id compose `003589B0`, generation bump `002659D0`
(`w[+0x16]=(w+1)&0x7FF`, wrap→1, **no null guard**), slot-occupant search `00327150`
(idx `b[q[02EBF190]+0x5AA4] ≤ 0x27`; scans `q[0208E688]+i*0xF50` for `q[+0x698]` ==
slot row), id→object resolve `003588B0` (cls-table `02098E10`, bounds+flag+generation
checks), leaves `263FF0`/`236850`/`236820`/`263E30` — **24/24 cases, stable ×3**
**[EXP-151]**. Executed: match on the occupant's `d[+8]` == old id always stores
`d[glob+0x5AA4]` (DWORD — clobbers +0x5AA5..7) and notifies `00326500` (scripted);
`b[02089340]&0x10` gates only the resolve — flag clear stores `0xFF` directly.

EXP-152 (NATIVE-REPLAY, `live_game: false`) executed the spawn-record initializer
`0023AC80` as shipped bytes — memset `rec,0,0x1C8`, sentinel fields, `d[02089300]`
gate and mode dispatch (byte0 idx / byte1 mode): mode-0 foe re-resolves FOED, gil
`00323790`, `idx<=6` ability-scan grants, 5× `0031A630` slots, `00327CB0` pair copy,
`00326030` counter, `00327DE0` order materializer; mode-1 member path resolves
MEMB and writes 4× slots; `0030C470` stats header copies row→rec fields —
**22/22 cases, stable ×3** **[EXP-152]**. Scripted boundaries retained:
`0030C650`/`0030FED0`, the stat cluster `0030F690`/`0030F340`/`0030F5A0`,
`00323910` deep grant, `00324100` override, `00317930`, `00318B40`, and the
member-block chain (`r9d!=0` only — never passed).

EXP-153..160 progressively promoted EXP-152's scripted set to real execution:
the stat cluster `0030F690`/`0030F340`/`0030F5A0` + `00377C20` chain (EXP-153,
37/37), per-bit core `0030E360` (EXP-154, 53/53), reconcile applies
`00300BC0`/`00300CE0` + `0030E060` fraction notify (EXP-155, 68/68), broadcast
wrappers `0030F3F0`/`0030F4B0` + slot resolvers (EXP-156, 77/77), stat apply
`00300530` delta commit (EXP-157, 86/86), spawn-id resolver `003008A0`
(EXP-158, 102/102), stat-change dispatcher `0030FED0` (EXP-159, 109/109), and
per-bit handler `0030E130` (EXP-160, 117/117) — all stable ×3, all
NATIVE-REPLAY `live_game: false`. EXP-192 drove `0031A630` with `r9d!=0`
and executed the member-block chain real end-to-end: unequip/equip gates
`0030F9A0`/`0030C410` → `3008A0` → `309F30` → class-1 `2FD8D0`/`2FD150`
count±delta (cap `w&0x3FF`), owner scan `0031B860`, and teardown `00324470`
(`d[+0x64]|d[+0x3C] & 0x80000003` must be nonzero to reach `313F60`/`300E40`;
`b[mbr]&2` skips `300E40`; `or d[mbr],0x40` terminal) — 116/116, ×3.
EXP-193 executed the remaining small boundaries as shipped bytes (156/156,
×3): slot-eligibility `00317930` (kind-6 `322C50` member range, tag
`b[row+7]>>5`, `309EC0` free-count real via `2FD8D0`, `323C60` nonzero=allow
final), pair-rebalance `00318B40` (drives the real `30F9A0`/`30C410` chain),
unlink `003243F0` + `0x40`-gated wrapper `00324450`, dispatch `00308010`,
licence scan `00324100`, and accessor `003271D0` (`b[02EBF190+0x5AA4]`).
EXP-194 promoted the leaves behind them (186/186, ×3): `00308130`
(state-step: `307D10` bit16 recompute + or-mask/`253B90` join + `3081E0`
RNG/`32A150` compare — all real incl. LCG `328370`), `00308040`
(flags/float/range predicate), `00308FF0` (`02EBF138` indexed accessor,
`b[+0x1E]∈{5,6}` → `b[+0xA]`), `00324020` (18-position licence popcount),
`00323C60` (`322C50` kind-1 class-nibble auto-dispatch via `309440`,
member-row `b[+7]&0x10`, else `323BB0`→`2F8FA0` ABILD requirement-bitmap
intersect with `rec+0x194`). Still scripted: notify `00326500`,
`0030C650`, deep grant `00323910`, spatial query `00234DA0`, `00263E30`.
EXP-195 executed the notify dispatcher and its tree real (202/202, ×3):
`00326500` (`311E20` → `326620` → `30D9A0` mode on `d[glob+0x5B04]` —
`&8`→5/`&4`→4/`377C20`≠0→3/`&2`→2/`&1`→0,1 — slot byte `b[5AA4]` modes
0/1, `0x1A` mode 2, `377C70` mode 3, `0xFF` modes 4/5 → `31B770` slotrow
scan `glob+8+bl*0x1C8` → `ebp=d[objrow+8]` + `317400` at mode 1, else
4-slot `b[glob+0x5A5A+i*2]` → `2367A0` scan, else `3589B0(263750(0))` id
compose → `311E20` → `3594B0` commit `d[022C7FE4]`+flag `022C7FF8`);
`311E20`/`3272F0`/`31ABF0`/`263750`/`265970`/`265020`/`265200`/`33CA00`
ctx-refresh chain (`022C7D18`/`022C7D20..` 0xB0 copy/`022C7DD0` triple/
`022C7DE0` float/`022C7D10` flag); `326620` ctor (`30A880`/`30A8A0` flag-3
gates — `&1`'s `377C20` requirement is unreachable under mode 0) +
recursive `326500`; `31B770`/`2367A0`/`31B810`/`317400`/`3137E0`/
`3137F0`/`26DAC0`; `3588B0`/`3589B0` id resolve/compose; and `00263E30`
(`ret q[rcx+0x30]`). EXP-196 executed the last three scripted bodies
(238/238, ×3): level-set `0030C650` (target clamp `0x63`; per-level FOED
level-row + `02EBF108` growth desc → `2F9A60` HP / `2F9B20` MP / `2F9BD0`
×4 float stats `f[+0x10..1C]` — HP jitter calls `379CD0`→`863BF0` MT with
`f[09136E4]<0` saturating the modulus to `INT_MIN`, MP jitter verified
byte-exact `temper % (g*100)`; `b[rec+5]` suppresses growth+tail,
`r8&2` suppresses the tail only; `31B860` once per level,
`46A690`/`3B02A0`/`35D8C0` once at final; serial tail `267330`→`3A1180`
(`02AEF3FC` key, `02AEEDC0` rows stride `0x18`, ret `(w8<<9)|7`)→
`2DF220`→`1DBDB0`→`329210` write `d[0208D32C]`), licence grant/revoke
`00323910` (`323D10` type arms — `b[abilrow+6]` 1→`324280` 7-row
cross-slot scan, 2→`324020` popcount, ≥4→LP gate; grant `bts`
`b[rec+0x194+id>>3]` + `d[rec+0x190]-=b[row+4]` clamped at 0; `r9&1`
silent; revoke skips `323D10`; `id==0xE5`→`31B860`→`3105D0` teardown;
rank chain `324020`→`30A310`→`b[lvrow+4]∈0xD0..0xE1`→`300B80`→real
`3008A0`; grade `id∈[0x12,0x1E)`→`308FF0`→`b[0x20]=min(max(cur,ret),3)`;
always `30FED0(rec,0x97)`), and proximity scan `00234DA0` (all four
`b[glob+0x5A5A+i*2]` slots via `31B810`; `q[+0x698]` rec →
`(d[+0x64]|d[+0x3C])&0x80000003`+`313F60` alive gate → `3273B0` ctx-id
vs `d[022C7FE0]` (a5 suppresses) → `265020` triple (ctx `b3>>5∈{1,3}`)
→ `31E620`/`3A1960` d² vs `f[pmin]`/`f[pmax]` → `f[pout]`+ret 1).
**No scripted bodies remain on this contract's call surface.**

SECTION-01 checks retained-record structure and original bodies, then independently
executes selected helpers/reset and the original disabled/unsupported-class paths.
It deliberately seeds **both bits26 and42** and confirms only bit26 clears. It does
not rerun the full Unicorn suite or verify its three-process stability claim.

Disposition: **incorporate with corrections/narrowing**, preserving measured reset,
guard/path results while rejecting the false bit, pulse-body and table-address claims.
Formal peer acceptance remains pending; the original producer harness/result files are
preserved, with their known observation/assertion limitations recorded in the review.

## 14. Remaining questions

Required live installation evidence and initialized-state reachability; unexecuted
callback semantics (inner-rekey closed by EXP-151, spawn-record init closed by
EXP-152, stat cluster + `00377C20` closed by EXP-153, per-bit/apply/dispatch
closed by EXP-154..160, unlink `003105D0` closed by EXP-161, member-block
`0030F9A0`/`0030C410`/`0031B860`/`00324470` closed by EXP-192,
slot-eligibility/rebalance/teardown/dispatch/licence/accessor
`00317930`/`00318B40`/`003243F0`/`00324450`/`00308010`/`00324100`/`003271D0`
closed by EXP-193, leaf arms `00308130`/`00308040`/`00308FF0`/`00324020`/
`00323C60`+`323BB0`/`2F8FA0` closed by EXP-194, notify dispatcher
`00326500`+tree and `00263E30` closed by EXP-195, level-set `0030C650`,
licence grant `00323910`, proximity scan `00234DA0` closed by EXP-196 —
**the contract's scripted set is empty; every body on the construction
call surface has been executed as shipped bytes**);
complete data/ownership obligations of the
major system; peer review and repair/rerun of the producer harness's wrong table observation
and nondiscriminating bit check. Existing authored-data and static findings elsewhere
must be consumed before proposing new experiments. No wholesale L2 promotion occurs here.

## 15. Evidence

[Mechanism page](how-a-battle-unit-is-built-from-its-definition.md) ·
[EXP-075](../../_experiments/EXP-075-reward-index-prechecks.md) ·
[EXP-150](../../_experiments/EXP-150-battle-unit-construct-exec.md) ·
[EXP-151](../../_experiments/EXP-151-rekey-inner-exec.md) ·
[EXP-152](../../_experiments/EXP-152-spawn-record-init-exec.md) ·
[EXP-153](../../_experiments/EXP-153-stat-cluster-exec.md) ·
[EXP-154](../../_experiments/EXP-154-per-bit-core-exec.md) ·
[EXP-155](../../_experiments/EXP-155-stat-apply-exec.md) ·
[EXP-156](../../_experiments/EXP-156-broadcast-wrappers-exec.md) ·
[EXP-157](../../_experiments/EXP-157-stat-apply-300530-exec.md) ·
[EXP-158](../../_experiments/EXP-158-spawn-id-resolver-exec.md) ·
[EXP-159](../../_experiments/EXP-159-stat-change-dispatch-exec.md) ·
[EXP-160](../../_experiments/EXP-160-per-bit-handler-exec.md) ·
[EXP-161](../../_experiments/EXP-161-teardown-unlink-exec.md) ·
[EXP-192](../../_experiments/EXP-192-member-block-chain-exec.md) ·
[EXP-193](../../_experiments/EXP-193-slot-eligibility-teardown-exec.md) ·
[EXP-194](../../_experiments/EXP-194-state-predicate-leaves-exec.md) ·
[EXP-195](../../_experiments/EXP-195-notify-dispatcher-exec.md) ·
[EXP-196](../../_experiments/EXP-196-level-grant-proximity-exec.md) ·
[SECTION-01 source checks and native controls](../../_experiments/evidence/continuation-section01-result-install/REVIEW.md).

## 16. Parity plan

Distinguish disabled master, unsupported class, rekey-before-failure and selected-teardown
bypass; positive/zero/missing counts; fresh versus existing spawn; code-zero versus
nonzero tracked writes; both class-specific float paths; sentinel reset versus total
zeroing; and exact bit masks. Use nonzero prior values for negative controls. These
probes test L1+L2 claims without requiring completed L3 implementation.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

*Every subject below is cited in §13/§14 as a body on the construction call surface that a native replay executed. This contract claims what those bodies do when `0023A570` installs a definition. It does not claim anything about their other callers, and it does not claim the rest of what their callees do. Each paragraph names both.*

**Audio — SERVICE (2 edges).** The level-set `0030C650` calls `003A1180` and `002DF220` in its serial tail (EXP-196). `003A1180` resolves the current packed sound-bank handle to a sound id, which is bank-local slot 7, and `002DF220` is the sound play entry. The level-set plays the level-up sound when it finishes. Construction reaches it only through a level set, and no audio state feeds back into the installed unit.

**Combat — CLIENT (1 edge).** `003206E0`, filed under the `Combat` code domain, calls the raw unit getter `00263E30`. It is the `(handle, 0, 100)` HP clamp that the lethal-transition page names. It reads a unit through the same one-instruction getter that this contract executed (EXP-195). It is a consumer of the getter, and it is not part of construction.

**CombatAI — CLIENT and SERVICE (24 edges).** The spawn-record initializer `0023AC80` calls three gambit bodies: `GambitConfig_InitializeThreeBanksFromBasePairs` `00326030`, `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders` `00327CB0` and `GambitRuntime_RebuildOrderSetForStatsRecord` `00327DE0`. EXP-152 records these as the pair copy, the counter and the order materializer. The other edges run the opposite way. `00301AD0`, the seven enmity bodies from `BattleEnmity_ReadForCombatantId` `003215C0` to `BattleEnmity_ClampAndStore` `00321E40`, `00327A10` and `00327CB0` call the id validator `00322C50`. `BattleUnit_RebuildPerceptionCandidateCache` `003247F0` and `00324F20` call the getter `00263E30`. `AiOrder_CheckActionPreconditions` `00301830` calls the stance predicates `00308040` and `00308130`. `BattleUnit_UpdateCombatFrame` `00308610` calls the unlink `003105D0`. `003014C0`, `00301AD0` and `00305AB0` call the field predicate `00377C20`. `003279B0` is called from the per-bit handler `0030E130`. Construction seeds a new unit's gambit banks and orders through the AI layer's own initializers, and the AI layer's evaluators consume the shared validators, getters and predicates that construction also executes.

**CombatAction — CLIENT and SERVICE (74 edges).** Most of these edges are callers of shared bodies on the construction surface. The id validator `00322C50` is called by seven action bodies, among them `BattleAction_CheckActionAvailabilityReason` `002FFCF0`, `BattleAction_GetPrimaryRangeScalar` `00309300` and `0031A7B0`. The field predicate `00377C20` is called by 17 bodies, among them `Battle_ProcessActionTarget` `00307300`, `Battle_BuildActionTargetSet` `0030D160` and `BattleUnit_CommitAction` `0030F760`. The owner scan `0031B860` is called by four preview and availability bodies. The HP and resource mutators `00300530`, `00300BC0` and `00300CE0` are called by `BattleAction_ConsumeExecutionResources` `00305640`, `Battle_ProcessActionTarget` `00307300` and `BattleSpecialSequence_CommitAccumulatedTargetHp` `0030EB10`. The service direction is the unlink `003105D0`. It calls `BattleAction_RefundReservedExecutionResources` `00300280`, `BattleAction_ReleasePresentationSlot` `0030C970` and `BattleUnit_ReleaseTargetRelationAndActionState` `00310780`. The HP, resource and status mutators call the eligibility-mask and suppression tests `0030B770`, `0030B7F0`, `0030B8E0` and `0030B9B0`. The action layer is the main other user of the stat mutators, validators and teardown that construction runs, and the unlink hands in-flight action state back to that layer when construction resets a reused unit.

**CombatFormula — CLIENT and SERVICE (92 edges).** Thirty-five formula and runtime bodies call the owner scan `0031B860` to map a stats record back to its owning unit. Among them are `BattleFormula_ApplyTargetResult` `003112F0`, `BattleFormula_ResolveTargetResult` `00385F60`, `BattleFormula_BuildEvaluationContext` `003847C0` and `BattleFormula_DispatchPostResultEvents` `00469EC0`. `003112F0` also calls the HP, resource, status, level and recompute bodies on this surface: `00300530`, `00300BC0`, `00300CE0`, `0030C650`, `0030E130`, `0030E360` and `0030FED0`. The status bodies call `BattleFormula_BuildInactiveStatusTransitionResult` `00386A50` and its siblings. `BattleUnit_ApplyUnitDefinition` itself calls the formula-filed initializer `BattleStats_InitializeDefinitionRecord` `0023AC80`. The mutators construction executes are the same ones the damage-and-status formula applies a result through, so formula is their main other client. Construction also enters the stats record through that layer's initializer.

**CoreRuntimeScheduling — MECHANICAL (2 edges).** `00300530` and `00308130` each call `GameClock_GetRawTickCounter` `0032A150`, a 7-byte read of the raw game tick. In `00308130` the tick is the recheck-timer comparison (EXP-194). This is a clock read, and no scheduling decision is involved.

**Gameplay — CLIENT and SERVICE (36 edges).** Several bodies that construction itself executes are filed to Gameplay. They are the id validator `00322C50`, which eight bodies on this surface call, and the engagement predicate `00308040`, which `00308010` calls. The stance recompute `BattleUnit_UpdateEngagementStateFlag` `00307D10`, which `00308130` and `0030E360` call, and the mode read `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` `0030D9A0`, which `00326500` calls, are also on that list. The other edges are further battle-state users of the same bodies. `BattleSlotMap_ResolveMappedBattleSlot` `0031B9F0` and `0031C5D0` call the validator, and `WorldActor_QueryCombatStanceState` `0030BFB0` calls `00308040` and `00308130`. `Battle_EmitReactionPresentationForSlot` `003176E0`, `0031ADB0` and `ActorHandle_GetPrimaryFormulaResourceByte26` `00321380` read the getter `00263E30`. `BattleSystem_ResetRuntimeState` `00237DF0` calls `0023AC80`, the definition-runtime side-effect bodies `00316DF0` and `00323540` call the count channels `0030C410` and `0030F9A0`, and four more bodies read `00377C20`. Gameplay is the code-domain label on the battle-state helpers that construction uses for id validation, engagement and stance, and the remaining edges are other battle code consulting those same helpers.

**Input and InputGameplay — CLIENT (2 edges).** `InputGameplay_ArbitrateDigitalInputAndModalState` `00253C70` (Input) and `00313A00` (InputGameplay) call the field predicate `00377C20`. The input arbiter and the capability reconciliation read the same area bit-15 action-permission override that the stat cluster reads here. Nothing flows between input and construction.

**Items_Equipment_Shops_License — CLIENT and SERVICE (84 edges).** The member-block chain executed in EXP-192/193 is this layer's own machinery. It runs through the slot setters `BattleStats_SetEquipmentSlotDirect` `0031A630`, `0031A410` and `0031A510`, the eligibility tests `Equipment_CheckItemEligibleForSlot` `00317930` and `BattleStats_HasRequiredLicenseForEquipment` `00323C60`, the pair rebalance `00318B40`, and the count channels `0030C410` and `0030F9A0`. Through those channels it reaches the inventory mutator `003008A0` and `Inventory_QueryEncodedItemStateByClass` `00309F30`. Twelve inventory and shop bodies call `003008A0`, for example `Shop_CommitPurchaseItemAndGil` `002FEEB0`, `Shop_CommitSaleItemAndGil` `00310870` and `Inventory_GrantEncodedLootItem` `00300B80`. Thirteen equipment and licence bodies call the validator `00322C50`. Construction installs equipment and licence state by calling the items layer's slot, licence and inventory bodies. Shops, loot and the licence board are that layer's other clients of the same bodies.

**Movement — CLIENT and SERVICE (26 edges).** The reset `00236A60` calls `Navigation_ResetPathPredecessors` `003839F0` and `003839C0`, and the unlink `003105D0` calls `BattleLocomotion_ResetPathAndSetTargets` `003291B0` and `0033C9B0`. In the other direction, ten locomotion and follow bodies read units through the getter `00263E30`, among them `PartyFollow_SolveFormation` `00338490` and `BattleLocomotion_QueryDynamicActorObstruction` `003357B0`. `Movement_IntegratePositionAndMeasureDisplacement` `002E5610` and `002EBFA0` compose handles through `003589B0`, and five movement bodies call the field predicate `00377C20`. The notify dispatcher `00326500` starts its context refresh in the Movement-filed `00311E20`, which EXP-195 executed. `0033CB10` and `0033D890` call the owner scan `0031B860`, and `0031BAC0` and `00326BB0` call the validator `00322C50`. Resetting a reused unit clears its path state through the movement layer's own resets. Movement is otherwise a reader of the same unit accessors.

**Party — CLIENT and SERVICE (32 edges).** The notify dispatcher `00326500` commits the chosen actor through `PartyFocus_RequestPackedActorHandle` `003594B0` after reading `PartyRoster_GetActorBySlot` `00263750`, which the EXP-195 tree lists. The rekey inner `003220E0` calls `00326500`, and the proximity scan `00234DA0` calls `PartyFocus_IsCurrentPackedActorHandle` `003273B0`. In the other direction, nine `PartyConfiguration_*` roster bodies call the validator `00322C50`. `PartyRoster_AssignActorToSlot` `00269C70` and four focus and VM bodies compose handles through `003589B0`. `00328BD0` clears a member's equipment and then re-runs `0030FED0`, `00326030`, `00327CB0` and `00327DE0`. `VMPartyCommand_ReconcileRuntimeRosterFirstThreeAndPreferredFocus` `0034D4E0` reads the preferred selector `003271D0`, and four `PartyConfiguration`/leader bodies from `0031B7E0` to `003273D0` read the getter `00263E30`. A rekey re-points the party focus through the party layer's commit path. The roster bodies share the validator, the handle composer and the gambit and stats initializers with construction.

**Presentation — CLIENT (10 edges).** `003A4290`, `003A56F0`, `00465120`, `00465690` and `00506700` compose actor handles through `003589B0`, and `00506700` also calls the blob and string selector `002B58B0`. `PartyCombat_UpdateStanceState` `00307E70`, `BattleUnit_ComputePresentationSuppressionMask` `003125E0`, `BattleUnit_BroadcastPartyCombatTargetRelation` `00313B30` and `AddMotion_ApplyBonePose` `003714A0` call the field predicate `00377C20`. Presentation bodies use the same handle composer, text selector and area predicate as construction, but construction calls no presentation body.

**Rewards_Progression_Economy — CLIENT and SERVICE (19 edges).** The stats-header copy `0030C470` and the level-set `0030C650` call the growth bodies `002F9A60` (HP), `002F9B20` (MP), `002F9BD0` (float stats) and `002F8F20`. EXP-196 lists the first three as the per-level growth steps. In the other direction, `BattleUnit_ProcessDefeatRewardsAndLoot` `00312280` calls `0030C650` and `00377C20`, and the per-bit core `0030E360` calls `00312280`. `Reward_ComputeExperienceForRecipient` `002F8BB0` calls the owner scan `0031B860`. Both the stats-header copy `0030C470` and the level-set are progression-filed bodies that the initializer `0023AC80` reaches. Construction levels a new record with the progression layer's own growth bodies, and defeat rewards later call the same level-set.

**Save_Load_Settings — CLIENT (1 edge).** `SaveImage_FinalizeHeaderAndChecksum` `00583D60` calls `PartyFocus_GetPreferredDefinitionSelector` `003271D0`. The save header reads the preferred-selector byte that this accessor returns (the battle-state block's `+0x5AA4`), and construction reads that byte through the same accessor. The save path only reads it.

**Script_VM_Native_Bridge — CLIENT (18 edges).** Twelve small bridge bodies compose packed actor handles through `003589B0`, among them `00342150`, `0034B5D0`, `00354F20` and `0050C7A0`. `00344740`, `00352FA0`, `003537D0` and `00355680` read the field predicate `00377C20`. `00356500` calls the broadcast wrapper `0030F4B0`, and `0050F560` calls the slot-occupant search `00327150`. Script native verbs reach units through the same handle composer and predicates. §8's "scripts select definitions" is the only script claim this contract makes.

**Spawn_Encounter_Lifecycle — CLIENT and SERVICE (8 edges).** Two spawn bodies call into construction: `Spawn_ApplyScriptSelectedUnit` `0023A3B0` calls `0023A570`, and `SpawnUnit_FinalizeSpawnEntryActivation` `0023A410` calls `00308010` and `0030FED0`. In the other direction, `0023A570` calls `SpawnKeep_ResolvePrimaryEntry` `00236100` (the spawn resolver of §6), `00300530` calls `SpawnGroup_RecordMemberDeathAndHandleCompletion` `00306F00`, and `0030C470` is called by `002398F0`. The spawn search `Spawn_TrySelectCandidatePosition` `00234AF0` calls the proximity scan `00234DA0`, and the engagement predicate `00308040` calls that scan. Spawn is the layer that invokes enemy construction, and construction resolves the spawn record through it.

**Status_Periodic_Terminal — CLIENT and SERVICE (48 edges).** The per-bit core `0030E360`, the recompute `0030FED0`, the status-layer handler `0030E130` and `0030F690` call and are called by this layer's bodies. Among them are `BattleUnit_ResetActionControlForStatusTransition` `00300140`, `BattleUnit_RecoverFromTerminalStatusSetIfClear` `00301140`, `BattleStatus_ComputeDefaultShortTimer` `003876D0` and `BattleStats_RemoveStatusMode0` `0030E990`. `BattleUnit_RunPeriodicCombatMaintenance` `00310DB0` calls `00300CE0`, `00322C50` and `00377C20`, and `002F9400` and `00386860` call `0031B860`. Construction's status work runs through the status layer's own add, remove and recompute bodies. The periodic tick is another client of the same mutators.

**UI — CLIENT (17 edges).** Fourteen UI bodies call the blob and string selector `002B58B0`, among them `00273E30`, `002986E0`, `002C4720` and `00560210`. `BattleMenu_BuildCommandEntryList` `0031EB20` reads the getter `00263E30` and the validator `00322C50`, and `0035BC50` reads the preferred selector `003271D0`. §6 bounds `002B58B0` as a text-selection rule, and the UI is its main user for picking the n-th string out of a text blob. The battle menu reads units through the same accessors, and none of this feeds construction.

**WorldAreaField — SERVICE (10 edges).** The spawn resolver side (`00234DA0`, `0023A570`, `003243F0` and `00324470`) calls the predicate thunk `00313F60`. `00300530`, `0030E360` and `0030F690` call the predicate `00377C20` itself, which reads the active field id through `WorldTransition_GetActiveOrPendingFieldId` `003148F0` and is also called by `BattleSystem_InitializeAreaState` `002342F0`. `00326500` calls `00377C70`, the mode-3 slot source of EXP-195. The area's bit-15 action-permission override is the one world input the construction surface reads, and it is read, never written.

## Falsification pass 1 — 2026-09-30 (OPUS): every clause tested survives

**Attack.** The contract's addressed clauses were turned into checks at their instructions: §2's entry, id split,
teardown and party spawn; I1's bit-26 mask and the enemy refusals that bypass it; I2's reset and master flag; I3's
re-key wrapper; I6's freshness gate and reward rows; I7's tracked-HP table; and I8's pulse reset and float paths.
SECTION-01, EXP-150 and OPUS block 343 are carried, not re-run. Script:
`Tools/analysis-kit/gfz-scripts/falsify_unit_construction.py`, output `falsify_unit_construction.out`, image
`73461d08…`, 0 BROKEN, exit 0.

| # | Clause attacked | Result |
|---|---|---|
| B1 | §2 1,808 bytes; class = `(id >> 8) & 0xFF`, row = `id & 0xFF` | **survives**. `0023A580 mov eax, edx`, `0023A585 sar eax, 8`, `0023A594 movzx esi, al`, `0023A58B movzx r12d, dl` |
| B2 | §2 teardown re-applies `0xFFFF` | **survives**. `00300F6D mov edx, 0xffff`, `00300F75 call 0023A570` |
| B3 | I2 the reset, then the master flag | **survives**. `0023A5B0 call 00236A60`, then `02089300` is read at `0023A5B5` |
| B4 | §2 the party path nulls the spawn | **survives** (`0023AAB1 xor ebp, ebp`) |
| B5 | I1 the bit-26 clear, and the class-1 refusals that skip it | **survives**. `0023A633` and `0023AC4B` are `and qword [rdi], 0xfffffffffbffffff`. The enemy path's refusals at `0023A643`–`0023A648` and `0023A65F`–`0023A662` jump to `0023A63A`, past the clear |
| B6 | I3 the re-key wrapper | **survives**. `00322050` writes `dword [+0xea4] = 0` and `byte [+0xea8] = 0`, resolves `q[unit + 0x10]` through `003220E0`, and stores the 32-bit handle at `+8` |
| B7 | I6 the freshness gate `byte[spawn] & 5 == 0` | **survives** (`0023A791 test byte [rbp], 5`) |
| B8 | I6 the reward rows | **survives**. `0023A965`–`0023A9F4` read `02EBF148` and `02EBF140` by definition `+0x22` / `+0x24`, store `+0xE70` / `+0xE78`, and form the row with `add ecx, eax` |
| B9 | I7 tracked-HP registration | **survives**. `00328FF0` writes `{slot, code}` into `02EC1380 + row·24` (`lea r9, [rax + rax*2]`, `*8`). It writes only when `code ≠ 0` or `slot < 0` (`jns`), and only under a signed `cmp ecx, 2` / `jge` |
| B10 | I8 the pulse reset and the class float paths | **survives**. `002FEAB0` is 10 bytes (`xor eax, eax; mov [rcx + 0xeac], rax; ret`). Class 1's `byte +0x27` goes to `xmm7` by `cvtdq2ps` with no multiply. Class 0's `byte +0x2B` goes to `xmm7` and is multiplied by the 1.5f at `00901B3C` (`0023ABAD`). The common store is `0023ABD6 movss [rdi + 0x6c], xmm7` |

**Verdict.** The contract's addressed clauses hold. Tier 1 (static).
