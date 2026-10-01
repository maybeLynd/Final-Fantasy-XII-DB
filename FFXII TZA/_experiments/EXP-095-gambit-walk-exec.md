---
experiment: EXP-095
title: Gambit walk under isolated original execution
contract: ../09-Combat-AI-And-Gambits/CONTRACT-gambit-walk.md
method: B
live_game: false
tool: evidence/gambit-walk-exec/check.py
---
# EXP-095 — gambit-walk-exec

**Status:** complete · **35/35 cases, 14/14 mutants, stable across two processes**
**Evidence:** `evidence/gambit-walk-exec/` (`check.py`, `result.json`,
`bodies.json`, `run.log`, `run2.log`)
**EXE:** `FFXII_TZA.exe` sha256 `73461d08…721f8` · image base `0x120000`

## Objective

`CONTRACT-gambit-walk.md` describes `00305CC0` — the per-frame walk that turns
a unit's gambit subgroup into at most one committed action. The differential
suite (`Reconstruction/Tests/Differential/diff_gambit_walk.py`, 34 cases /
68 comparisons / 0 mismatches) established contract-level *trace* semantics
with all three callees scripted. This experiment re-drives the comparison with
the walk **and two of its three callees executed as real shipped bytes**:

| VA | role | execution |
|---|---|---|
| `00305CC0` | the walk | **real** — subject under test |
| `003014C0` | evaluator (`AiOrder…ResolveActionTarget`) | **real**, bounded closure |
| `004697C0` | third call on commit-success | **real** |
| `0030F760` | commit (`BattleUnit_CommitAction`) | scripted per-call — real execution is **EXP-091** evidence; here its answer is a walk input |
| `00301AD0` | per-slot hit resolver | scripted per-slot — 804-body static closure (the target-scan machinery), disclosed boundary |

The observable is the call trace, as in the differential suite: which records
were offered to eval / commit / notify, in what order, and with what
target/param/kind args. `E<i>` = eval offered record *i*, `C<i> t<x> p<y>` =
commit offered with eval-produced target/param, `S<i>.<k>` = scripted slot
resolver call (slot *k* of record *i*), `N t<x> w<y> f<z>` = notify args.
Scripted-callee answers are functions of record content (slot aux fields /
commit script), never of call index.

## Executed bodies (real shipping bytes)

11 bodies, spans + sha256 in `bodies.json`:

| VA | role |
|---|---|
| `00305CC0` | the walk — subgroup offset loop, per-record gates, eval→commit→notify |
| `003014C0` | evaluator — spec resolve, suspend gate, condition dispatch, slot loop |
| `00308EC0` | target-spec resolver — returns spec itself below `0x8000` |
| `00301830` | condition dispatch — shipped spec table `0x1ED0460`, roll arm, chance gate |
| `00328370` | deterministic 3-iterate LCG, state dword `0x22C256C` |
| `002E9C00` | unit-arm first gate (returns −1 on the synthetic unit) |
| `00316CF0` | memset wrapper → IAT thunk |
| `00861EC0` | memset IAT thunk (slot `0x8C2A60` planted to a fixture memset) |
| `00808C40` | `__security_check_cookie` |
| `004697C0` | notify — third call on the success path |
| `002F8E90` | kill/status kind classifier (EXP-093 chain) |

## Scripted / stubbed boundaries (all disclosed)

- `0030F760` commit — `ret`-stubbed; answer from a per-call script supplied
  identically to expectation. Real-execution authority: EXP-091.
- `00301AD0` slot resolver — `ret`-stubbed; per-slot answer read from the
  record's own slot fields `(count,hitret,aux)` at `+6/+0xC/+0x12`. On
  `hitret>0` the script also writes the hit-list shape the combiner would
  read (`{+1 mode,+4 cnt,+8 {obj,score}}` entries), so downstream plumbing is
  exercised with realistic data.
- `002F8E90`→`0046AB10` ring insert — never reached: condition-spec matches
  produce target ≥ `0x21F`-class values, outside the insert gate. The arm is
  EXP-093 evidence; here notify runs real as a traced no-op call.
- Fixture globals: `0x1F44830` cookie, `0x2089340` suspension byte,
  `0x22C256C` LCG state (planted per case; real 3-iterate LCG advances it).
- All IAT slots nulled except `0x8C2A60` (memset → fixture routine). An
  unplanted slot holds the ILT hint RVA; an unexpected IAT call faults rather
  than executing import-name data.

## Not exercised (disclosed, not claimed)

- The unit-arm eligibility cascade past `002E9C00` (`002FFCF0`,
  `00306480`, `00303BD0`, `0030F130`, `003087E0` combiner, param-write tail):
  the "is action performable" machinery is a separate contract surface. With
  the synthetic unit, `002E9C00` returns −1 and the arm fails closed.
- Notify's deeper kill-ring insert/latch arms (need a matched target in the
  ring-eligible range; see above).
- Special condition specs (`0x4022`, `0x4050`, `0x4091`, `0x4122`, `0x4124`
  arms in `00301830`) — only the generic table-driven roll arm is driven.

## Findings (native-verified; contract corrections marked †)

1. **Walk ABI**: `(rcx=unit, rdx=set, r8d=subgroup index (signed),
   r9d=resume mode)`. Null `set` → ret 0.
2. **Subgroup addressing**: record base = `set+0x20 + 24*sum(counts[0..idx-1])`,
   iterated count = `counts[idx]` — reread from memory every loop iteration
   (`count-shrink`/`count-grow` kill the latched-count model). The offset sum
   uses an unrolled pair loop (even/odd accumulators) plus a leftover element;
   negative indices sign-extend (`movsxd`) and read `counts[-1]` — the byte
   before the header (`neg-index` case).
3. **Record stride 0x18**; `E`/`C` order interleaved per record; commit
   failure does **not** stop the walk (`commit-fail-cont`); the walk returns
   after the **first** successful commit.
4. **Resume semantics** (r9d≠0): resuming = `mode≠0 AND ctx≠0 AND
   ctx+4 & 0x4000`. When resuming, only records with flag `0x40` are offered
   (mask test — `0x41` qualifies). Independently, mode≠0 skips any record
   with flag `0x80`. `ctx == record address` → early ret 1 *before* that
   record is evaluated (the resume point is where a prior walk stopped).
   † The flags have opposite polarity to the naive reading: `0x40` = offer
   while resuming, `0x80` = skip while mode set.
5. **Third call**: on commit success AND mode≠0 AND latched
   `word[unit+0x714] != 0xFFFF` → `004697C0(rcx=[unit+0x698],
   rdx=out_target, r8d=word714, r9d=4)`. The `+0x714` word is latched at walk
   entry (`00305CE5`); r9d=4 is a hardcoded kind constant.
6. **Evaluator dispatch** (`003014C0`): writes `out_target=0xFFFF` first;
   `00308EC0` resolves the spec (identity below `0x8000`); sentinel/resolved
   `0xFFFF` → ret 0; suspension `byte[0x2089340] & 0x20` → ret 0; unit arm
   (spec < `0x4000`) gates through `002E9C00` → −1 → ret 0 on the fixture.
7. **Condition arm** (`00301830`): the shipped spec table `0x1ED0460` covers
   most of `0x4000–0x4167`; probed holes — `0x4038–0x4047`, `0x4128–0x412F`,
   `≥0x4168`, all of `0x8000+` — return 0. A nonzero entry reaches the roll
   arm: **`chance==0` → unconditional match; else match iff
   `roll % 100 < chance`** (`cmp r8d,ebp; jge skip` at `00301962`). † The
   "only `0x4086–0x408D` nonzero" static reading was wrong — the table
   entries are broadly populated through `0x4167`.
8. **LCG `00328370`** is a 3-iterate `x' = 0x41C64E6D·x + 0x3039` folding
   30 bits of state; state dword at **`0x22C256C`** † (a hand-computed
   `0x2C2256C` in the draft harness silently read 0 — caught by the
   per-seed roll probe: real roll%100 was constant 84 until the address was
   corrected; mirror and native now agree per seed).
9. **On eval match**: `out_target = spec`, param stays 0 for slotless
   records; the walk passes them to commit as `(r8d=target, r9d=param)`.
10. **Slot loop**: slot *k* with `count>0` calls `00301AD0`; `ret ≤ 0` aborts
    eval (ret 0); positive returns continue to the combiner path
    (`slotfail`, `slot-hit-match`).

## Mutation evidence — 14/14 killed

Byte patches over shipped code (sites verified against the image):

| mutant | site | kills by |
|---|---|---|
| m-stride | `00305E07` `add rbx,0x18→0x30` | every offer index shifts |
| m-count-loop | `00305E08` `cmp edi,eax→ebx` | wrong loop bound |
| m-respt | `00305DA7` `je`→nop×6 | resume-point record evaluated |
| m-40gate | `00305DB5` mask `0x40→0x20` | resuming records offered wrongly |
| m-80gate | `00305DBF` mask `0x80→0x40` | mode-only skip reads wrong bit |
| m-ctx4000 | `00305D75` imm `0x4000→0x2000` | resuming from wrong ctx bit |
| m-commit | `00305DFB` `jne→je` | commit-failure takes success path |
| m-notify-const | `00305E4B` `r9d 4→5` | kind constant change |
| m-notify-gate | `00305E42` `je→jmp` | `0xFFFF` no longer suppresses N |
| m-w714 | `00305CE9` `+0x714→+0x716` | latched word from wrong offset |
| m-susp | `00301517` mask `0x20→0x40` | suspension bit never consulted |
| m-eval-ret | `003016B0` `jle→jge` | slot-resolver ≤0 abort inverted |
| m-roll | `00301962` `jge→jl` | chance gate inverted |
| m-sx | `00305CCC` `movsxd→mov eax` | subgroup index loses sign extension |

## Fixture bugs found and fixed during bring-up

- IAT memset slot left at ILT hint RVA → thunk `00861EC0` jumped into import
  names and executed data (`rip=0x1CCEB5F`). Fix: null all IAT slots, plant
  `0x8C2A60` → fixture memset.
- `G_LCG` hand-computed as `0x2C2256C`; real address `0x22C256C` (verified
  by mem-hooking the LCG's accesses). Symptom: seed-independent roll%100=84.
- `res-ctx-4001` fixture used `ctx_flags=0x4001`, which *contains* `0x4000` —
  resuming legitimately computed true. Corrected to `0x2001`.
- Case fixtures realigned to the verified subgroup-offset rule
  (`sum(counts[0..idx-1])`, count=`counts[idx]`).

## Reproduction

```text
cd "Database/FFXII TZA/_experiments/evidence/gambit-walk-exec"
python check.py   # 35/35 cases, 14/14 mutants; writes result.json
```

Deterministic: fixed fixtures, per-case LCG seeds chosen by the mirrored LCG,
no wall-clock or environment inputs. Stable across two separate processes
(`run.log`, `run2.log`).

## Annotation - steps 5 and 6: the out slot is the action (SWE2-ORACLE, 2026-09-30)

Answers `OPUS-NOTE-ORACLE-EXP095-OUT-SLOT-IS-THE-ACTION`. Steps 5 and 6 above named the wrong thing.
- **The word slot is the action id, not a target.** The slot at `[rsp+0x70]` (initialised `0xFFFF`) that the
  evaluator `003014C0` writes first is its **out = the decoded action id** (`00301500`). It is passed to `0030F760` as
  `r8w`, and to `004697C0` as `edx`.
- **Re-read here.** `00305E44` is `movzx edx, word [rsp+0x70]`, and `00305E56` puts the `+0x714`-gated word
  `[rsp+0x78]` in `r8d`.
- **Where the target goes.** It goes through `[rsp+0x30]` (`003017E7`) as the commit's `r9d`.
- **Measured by OPUS** with the real evaluator (`candidates/s25-opus-replay-gambit-walk/commit_walk.py` W2/W3/W6).
  W6 is `004697C0([unit+0x698], 0x96, 0x4021, 4)`.
- **What stands.** The executed results and the 14/14 mutant kills are unchanged, and the contract section 7 is already
  corrected. Read `out_target` above as `out_action`.
