# S-25 runtime: per-invariant stub exposure for EXP-095 (+ EXP-091, commit-action) (OPUS, 2026-09-25, block 305)

*Drafted by a delegated OPUS pass and reviewed before publication (block 305): its concrete address claims were spot-checked against the image; see the block-305 inbox entry for which.*

**Row:** S-25 gambit evaluation and enmity. Runtime **MIXED** — *"EXP-095 executes the gambit walk and EXP-091
the commit-action callees under isolated original-code replay … no per-invariant stub-exposure analysis yet"*.
Binding gap: *"types PARTIAL and nothing executed — runtime is ASTRA/ORACLE's gap; the contract no longer binds it"*.

Contracts (column 6 of `important-subsystems.tsv`), both under `09-Combat-AI-And-Gambits/`:
- `CONTRACT-gambit-walk.md` (scope `operation`, entry `00305CC0`). Its claims sit in §4 (subgroup addressing),
  §4a (global suspension bit), §5 (one invariant, two postconditions), §6 (resume) and §7 (two-call rule, third
  call); there are no I-labels. They are labelled **G-§n** below.
- `CONTRACT-enmity.md`: E-1..E-8, over six bodies `003216E0`, `00321850`, `003219D0`, `00321B00`, `00321530`,
  `00321D30`.

Evidence classes: isolated original-code replay and static. Nothing here is live. This note scores nothing.

**Probes:** `_index/candidates/s25-probes/`. Each script sits next to its `.out.txt`; `common.py` is the
hash-checked image loader.

| probe | kind | what it measures |
|---|---|---|
| `p1_walk_static` | static, capstone | the walk's stores and field reads |
| `p2_commit_return_by_target` | shipped `0030F760` executed | the commit's return by target word |
| `p3_walk_with_commit_writes` | EXP-095 cases re-run | the cases with the commit's real unit stores applied |
| `p4_matched_spec_outside_commit_band` | EXP-095 world | does the real evaluator match specs `0x4165`–`0x4168`? |
| `p5_set_referencers_vs_stub_closures` | static | which functions reference the set base, and whether stubs reach them |
| `p6_condition_table_address` | static | which spec table the condition arm reads, and its empty slots |

The replay probes record the final RIP and whether the run reached its return sentinel.

## Which records belong to this row

| record | front-matter contract | runs any body of this row's contracts? |
|---|---|---|
| **EXP-095** `evidence/gambit-walk-exec/` | `CONTRACT-gambit-walk.md` | **yes:** the walk `00305CC0` and its evaluator |
| **EXP-091** `evidence/commit-callees-exec/` | `../07-Combat-Action/CONTRACT-commit-action.md`, **S-20's contract** | **no.** Its `bodies.json` lists 53 real bodies, including `0030F760` (the callee EXP-095 scripts). None is `00305CC0`, `003014C0` or an enmity body (grep of the record, `check.py` and `bodies.json`). Its substitutions are analysed in `s20-runtime-per-invariant-exposure.md`, not here. Relevance to S-25: it is the real-execution authority EXP-095 cites for the scripted commit, and its band statement ("anything else → return 0") agrees with P2 |

**Enmity:** no record under `_experiments/` names any of the six enmity bodies (grep of records, `check.py` and
`bodies.json`, by `00321xxx` and `0x321xxx`).

## Substitutions per record (EXP-095)

Read from `check.py` (`STUBS`, `CALLS`, `World.__init__`, `on_call`, `build_cases`) and `bodies.json`.

| runs as shipped | substituted |
|---|---|
| 11 bodies (hashes in `bodies.json`): walk `00305CC0`; evaluator `003014C0`; `00308EC0` target-spec resolver; `00301830` condition dispatch (reads the shipped `.rdata` spec table `01ED0460`); LCG `00328370`; `002E9C00` unit-arm first gate; `00316CF0` memset wrapper; thunk `00861EC0`; `00808C40` cookie check; notify `004697C0`; `002F8E90`. The whole image is mapped | **Application stubs (2):**<br>• **`0030F760` commit**: `ret` at entry; its return is scripted per call (`cm`).<br>• **`00301AD0` slot resolver**: `ret` at entry; its return is the record's slot `hitret`, and on `hitret > 0` it writes a synthetic hit list `{+1 mode, +4 cnt, +8 {obj, score}}` to the out cursor.<br>**Import bridge (1):** memset IAT `008C2A60` → fixture `rep stosb`. Every other IAT slot is nulled, so an unexpected import faults.<br>**Fixtures:**<br>• cookie `01F44830`; suspension byte `02089340`; LCG state `022C256C`;<br>• unit (`+0x10`, `+0x698`, `+0x6A0`, `+0x708`, `+0x714`), stats, gambit set with header counts;<br>• the resume context: either a separate object `CTXB` with a flags word at `+4`, or a record's address;<br>• hit objects.<br>**Planted intervention:** `patch=(call, idx, val)` rewrites a count byte at the Nth evaluator entry (`count-shrink`, `count-grow`) |

## Per invariant

| invariant | executed by (EXP-095 case / mutant) | can a substitution reach it? |
|---|---|---|
| **G-§2/§10.1** a null set returns 0 (`00305CF2`–`00305D01`) | `null-set` | **no**; body-local, before any call |
| **G-§4** base = `set + 0x20 + 24·Σcounts[0..idx−1]`; index sign-extended; stride `0x18` | `sub0`–`sub5-walk`, `neg-index`; `m-sx`, `m-stride`, `m-count-loop` | **no**; body-local |
| **G-§4** an empty subgroup walks nothing (`00305D89`) | `empty-sub`, `empty-sub3` | **no** |
| **G-§4** the count byte is re-read every iteration (`00305DFD`, after the evaluator and commit calls; P1) | `count-shrink`, `count-grow`, via the **planted intervention** | **The walk's response: no.** The intervention stands in for a callee writing the byte, which the contract itself scopes: "whether any real evaluator or commit does write it is not established … the walk would follow it if one did". **P5:** the set base `02089378` is referenced by `0023A570`, `00327DE0`, `00327F80` and `00328140` only. None is in the direct-call closure of the commit stub (992 functions), the slot-resolver stub (761), the real evaluator (878) or notify (474). So no stubbed callee's skipped behaviour reaches the count bytes through direct calls; indirect calls are not covered |
| **G-§4a** bit 5 of `02089340` stops every evaluation (`00301511`) | `suspended`; `m-susp` | **no.** The bit is a planted fixture byte and the test is real. The bit's writers (`00238B70`, `00359A30`, `0035AB20`, `0035A6F0`) are **not executed**; that is coverage |
| **G-§5 invariant** orders are tried in address order; no re-sort | all multi-record traces (`E0 E1 …`) | **no**; body-local |
| **G-§5 postcondition** on 0, nothing committed and "no state changed by this function" | returns of 0 in `commit-never`, `all-nomatch` and others | **no.** P1: the walk's **only 8 stores are `rsp`-based** (`00305CD6` … `00305DEC`; non-stack writes: 0). The claim excludes callees by its own wording. EXP-095 compares trace and return, not memory; this half rests on P1 (static) |
| **G-§6** `resuming` = mode ∧ ctx ∧ `ctx+4 & 0x4000`; `0x40` offered while resuming; `0x80` skipped in mode; ctx == record → return 1 (`00305DA4`) | `res-*` (8 cases), `resume-at-rec`; `m-respt`, `m-40gate`, `m-80gate`, `m-ctx4000` | **no.** P1: `[unit+0x708]` is read **once**, at `00305D53`, before the first call (`00305DD2`). The stubbed commit's skipped store to `+0x708` cannot feed the same walk. P3 applies the shipped commit's stores (P2) on every scripted success and gets **35/35 cases identical**, every run reaching `RETQ` (`62000000`) with no faults. See finding F-2 on the fixture context object |
| **G-§7** both calls must succeed; a commit failure continues the walk (`00305DF9`–`00305DFB`) | `commit-fail-cont`, `commit-never`, `eval-then-match`; `m-commit` | **The walk's handling: no** (body-local `test`/`jne`). **The scenario it is exercised on is supplied by the stub:** the commit's return is the selection input, scripted 0 for target `0x4086`. P2 shows the shipped commit returns 0 only outside `[0, 0x21E] ∪ [0x4000, 0x4166]`: rax = 1 for `0x4086`; rax = 0 only via the `ja` at `0030F7EC` to `0030F981`; every run `reached_sentinel=True`. So both failure cases are counterfactual for that target. See F-1 |
| **G-§7** ~~the target slot starts at `0xFFFF`, param at 0~~ **the action slot starts at `0xFFFF`, the target slot at 0** (`00305CCF`–`00305CDE`) *(corrected 2026-09-26, OPUS: `commit_walk.py` W2/W3 — the evaluator writes the decoded action id and the target id into them)* | every commit trace (`t…`, `p0`) | **no**; body-local stores before any call. The evaluator (real) overwrites both |
| **G-§7** the third call `004697C0([unit+0x698], ~~target~~ **action**, latched +0x714, 4)` *(corrected 2026-09-26, OPUS: its second argument is the action word, `00305E44`; `commit_walk.py` W6)* only when mode ≠ 0 and the latched word ≠ `0xFFFF` | `notify-sent`, `notify-sentinel`, `notify-nomode`; `m-notify-const`, `m-notify-gate`, `m-w714` | **no.** P1: `+0x714` is read once at `00305CE5`, before any call. The shipped commit stores ~~the target~~ **the action id** *(corrected 2026-09-26, OPUS: `+0x714` = `0x96` after an Attack commit, W3)* into `+0x714` at `0030F806` (P2), but the walk passes the latched value. P3 `notify-sent` is identical with that store applied (`N t4086 w20 f4`). Notify runs real; its ring-insert arms are not reached (coverage) |
| **G-§9** no RNG in the walk; randomness only in the evaluation | `roll-match`, `roll-nomatch` (real LCG) | **no** |
| **enmity E-1..E-8** | **not executed** by any record | coverage, not exposure |

## Findings

**F-1: in EXP-095, "a satisfied condition whose commit fails" is produced by the stub, not by the shipped commit.**
- **P2** executed shipped `0030F760` with its callees returning 0. It returns 0 **only** through `0030F7EC ja` →
  `0030F981`, for targets `0x21F`–`0x3FFF` and `≥ 0x4167`. For `0x0000`–`0x021E` and `0x4000`–`0x4166` it
  returns 1 and stores `+0x708` = record pointer, `+0x710` = param, `+0x714` = target. EXP-091's own text says
  the same.
- **P4:** the real evaluator matches spec `0x4166` (`E0 C0 t4166`, `RETQ` reached) and does **not** match `0x4167`
  or `0x4168`. Spec `0x4165` **faulted**: an unmapped read at `0x3` from `00265090`, RIP not at `RETQ`. That is a
  special arm outside the fixture, so no result for it.
- **Why, statically (P6):** the condition arm applies the **same bound as the commit's band 2** before any table
  read: `003018DD lea eax,[rdx-0x4000]` / `003018E3 cmp eax,0x166` / `003018E8 ja 00301AA4`. The commit's check is
  at `0030F7E1`–`0030F7EC`.
- **What follows:** no condition-arm match can produce a target the commit refuses. This is structural, not a
  property of the planted cases. The walk's
  continue-on-failure branch is real and correctly measured on a scripted 0. A **shipped** reach of that branch
  would need a target from the unit arm or the slot combiner in `0x21F`–`0x3FFF`. Neither arm is executed.
- This bears on §7's **player-visible explanation** ("why a gambit can visibly do nothing while its condition is
  plainly true"), not on the walk rule. Whether any evaluated target lands in `0x21F`–`0x3FFF` is open.
- **Also:** on its failure path the shipped commit still calls `003105D0` (with arg5 = 1, which the walk passes)
  before the band test (P2 callee list). That callee's writes could feed later evaluations in the same walk. They
  are not executed or read here.

**F-2: the resume context's `+4` word, fixture vs shipped writer.**
- The only `+0x708` store measured here is the commit's, at `0030F7F9`. It stores the **committed record's
  address**, so in shipped state `ctx+4` would be that record's own flags word (`record + 0x04`).
- EXP-095 exercises `resuming` through a separate fixture object `CTXB` whose `+4` flags are set independently.
  The walk's test reads the same bytes either way, so there is no exposure.
- But the contract's §3 ("the action context; its `+0x04` word's `0x4000`…") and the fixture both treat the
  context as a distinct object.
- Whether any **other** writer of `unit+0x708` stores a non-record context was **not read**.

**F-3: the binding gap is stale.**
- "types PARTIAL": the types cell reads MET (re-scored 2026-09-25).
- "nothing executed": EXP-095 executes the walk and its evaluator. It stays true only for `CONTRACT-enmity.md`,
  whose §13 ("None") is accurate.

**F-4 (minor): closure sizes differ.** EXP-095 describes `00301AD0`'s static closure as 804 bodies; P5's closure
over `Tools/work/graph/edges.tsv` gives 761. The edge set likely differs by version. Not investigated.

**F-5: EXP-095 names the wrong spec table, and its hole list does not match the table the code reads.** The S-20
draft flagged this; confirmed here by P6.
- `00301830` indexes **`01EEC460`** (`003018F0 lea rcx,[rip -> 01EEC460]`, 8-byte entries, 0x167 slots,
  `[0] = 002FDA60`).
- EXP-095's record and `check.py` name `0x1ED0460`. Over the same extent that address holds only 24 nonzero
  bytes in 2,872.
- `01EEC460`'s empty slots are `0x4025`, `0x4036`–`0x4045` and `0x4128`: 18 in all. EXP-095's finding 7 lists
  the holes as `0x4038`–`0x4047` and `0x4128`–`0x412F`.
- No EXP-095 case depends on the named address, since the harness maps the whole image and the code reads its own
  table. So this corrects the record's text, not the replay. It also means `0x4167`'s non-match is the `0x166`
  bound, not a table hole.
- A later draft note, not this one, owns the question of what `01EEC460` is. The S-20 cell ties the same
  `id − 0x4000` vs `0x166` window to the action handler table.

**Side effect of the probes.** P3 imported EXP-095's `check.py` by path, which re-wrote the harness's own
**gitignored** bytecode cache, `_experiments/evidence/gambit-walk-exec/__pycache__/check.cpython-314.pyc`. No
tracked file changed; `git status` for that directory is clean. P4 and P5 ran with bytecode writing disabled.

## For the scorer

- **EXP-095 substitutes** 2 application stubs (commit `0030F760`, slot resolver `00301AD0`), 1 import bridge
  (memset, IAT `008C2A60`), fixtures, and a planted count-byte intervention that the contract scopes in.
- **Gambit-walk claims:** no substitution reaches any value or ordering the walk asserts.
  - The walk stores nothing outside its frame (P1).
  - It latches `+0x708` and `+0x714` before any call (P1).
  - Applying the shipped commit's stores changes none of the 35 outcomes (P3).
  - The set base is outside every stub's direct closure (P5).
- **One scenario is stub-supplied:** G-§7's commit failure (F-1). Its handling is measured. For the condition
  arm, shipped reachability is structurally excluded: the same `0x166` bound sits at `003018E3` and in the commit.
  For the unexecuted unit-arm and combiner paths it is open.
- EXP-095's text names the spec table `0x1ED0460` and gives holes that do not match the table the code reads,
  `01EEC460` (F-5). This is a correction to the record's text, not an exposure.
- **Not executed:** enmity E-1..E-8 (all six bodies); the §4a bit writers; the unit-arm and slot-combiner paths.
  This is coverage, not exposure.
- **EXP-091 belongs to S-20's commit-action contract.** It executes none of this row's bodies.
- The binding gap is stale (F-3). `live_game` is false for both records.
