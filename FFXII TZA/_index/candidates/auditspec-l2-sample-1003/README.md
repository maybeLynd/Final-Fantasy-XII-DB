# Independent L2 sample, exact-behaviour families (SWE2-AUDIT-SPEC, 2026-10-03)

*SWE2-AUDIT-SPEC (second instance, standing in for the lane's Devin session). User package
`Tools/work/FABLE/FFXII_INDEPENDENT_CORPUS_AUDIT_FOLLOWUP_2026-10-03.md` §6. Audited at HEAD `050fd9350`, against EXE
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` (image base `0x00120000`). SWE2-AUDIT-SEM takes
the semantic families. This record changes no page, contract, type row or verdict cell. Under REVIEW-POLICY the
producers repair their own work.*

## Result in one table (SWE2-AUDIT-SPEC)

| family | system sampled | verdict |
|---|---|---|
| ScriptVM interpreter + native bridge | **S-07** zone-script VM and native bridge | **ACCEPT-WITH-NARROWING** |
| resource request / binding / lifetime | **S-08** resource request queue and file layer | **ACCEPT-WITH-NARROWING** (queue only; the scope question goes to OPUS) |
| combat action + lethal transition | **S-23** HP write and lethal transition | **ACCEPT-WITH-NARROWING** |
| combat formula / RNG | **S-22** formula step table and calculator slots | **REJECT** |
| presentation / render resource path | **S-39** render command list and graphics handshake | **REJECT** |

**No sampled system was accepted as written. Two are rejected on named defects, and both defects come from one
systemic instrument blind spot (SF-2).** §6 says *"If the sample exposes a systemic scoring defect, expand the audit
before terminal certification."* That condition is met, so this record **recommends expansion** (see the end).

## Method (SWE2-AUDIT-SPEC)

- **Sources.** Each system's row was read in full in `L2-VERDICTS.md`, together with its registry subject in
  `important-subsystems.tsv`, its primary pages, every credited contract, its `_types/fields.tsv` and `types.tsv`
  rows, and the code of the validator its runtime cell cites.
- **Re-derivation.** Load-bearing claims were re-derived from the shipping image with `disr.py` and `disw.py`
  (`Tools/work/FABLE/pub140-scratch`). Every address below was read at the bytes.
- **Who did the work.** The S-08, S-22, S-23 and S-39 reads were split across four sub-instances of this lane. All
  of them used the same tools and wrote no repo files.
- **What I re-verified myself.** Every defect a verdict rests on was re-run by me, and is marked **[re-verified]**.
  Findings not re-run by me are marked **[sub-instance]**.
- **Validator runs.** Three were run (S-08 `pump_states.py`, S-22 `we1.py`, S-23 `ey.py`), and each stated md5
  reproduced. They run only under `C:\Python314` (unicorn 2.1.4). The prescribed venv (unicorn 2.1.0) crashes at
  `uc.ctl_flush_tb()`, so the packages do not pin their dependency (SF-6). For S-07, `check.py` was read in full,
  not run.
- **Sample choice.** In each family I took the MET row with the widest blast radius:
  - **S-07.** It is the only MET row in its family, and every authored script crosses it.
  - **S-08.** Every asset load passes through it, and its registry subject is the widest of the resource rows
    (S-08, S-09, S-47, S-49).
  - **S-23.** It names the lethal transition directly. S-20 and S-21 feed it.
  - **S-22.** It was chosen over S-46 RNG and S-24: every damage and heal number passes through the step table,
    while RNG routing is a narrower question once streams are identified.
  - **S-39.** It was chosen over S-38 and S-37: every frame's draw jobs pass through the ordered list, and S-38 is
    one of its clients.
- **Verdict authorship.** The task brief describes the verdicts as OPUS's and FABLE's. In fact, every cell in this
  sample was re-scored by **SWE2-AUDIT-SEM**, on closer packages that OPUS produced (`s07-opus-replay-*`,
  `s08-opus-replay-*`, …) and on contracts that FABLE and OPUS wrote. SWE2-AUDIT-SPEC wrote none of the three, so
  this review is independent of all of them.

## Systemic findings (SWE2-AUDIT-SPEC) — read these first

**SF-1. The contract author sets the denominator of the types and runtime cells, and the contract cell does not test
implementability against the registry subject.**
- Types cell: *"the denominator is the contract's state enumeration"* (`L2-VERDICTS.md` ~L2785).
- Runtime cell: *"the contract narrows its own runtime denominator by its words"* (~L2878).
- Contract cell: it asks for page/subject coverage plus cross-operation adequacy. Nothing scores "states enough
  behaviour to implement the registry subject".
- Result: a registry subject can be wider than anything that is measured.
  - **S-08.** The file layer (FST sizing, loose-then-archive issue, BigFile index, the `0215EFF4` status producer)
    is in the registry subject. No contract covers it and no type is declared for it, yet the row reads MET. The
    contract excludes it in §7/§14, and the runtime cell repeats the exclusion.
  - **S-22.** The 152 step-target bodies are ruled *"a coverage statement, not a named invariant"*, which places
    them outside the runtime denominator (the "380 precedent"). Meanwhile the step-table contract's own §14 L175
    still lists *"What 125 of the 152 targets do"* as unresolved.
- Seven MET rows carry denominator-exclusion language in their cells: **S-04, S-08, S-13, S-22, S-23, S-26, S-30**.

**SF-2. The types-cell instrument sees only one syntax of one kind of state.** `contract_named_state_census.py`
L42 extracts `` `ADDR` ``, `` `0xADDR` `` and `` `[ADDR]` `` cells for .data addresses only.
- **Width-prefixed addresses** (`` `dword[ADDR]` ``) are invisible. **[re-verified]** S-39 names `dword[02EBA3F8]`,
  the handshake word, in §5 (L216–217). The census row list for S-39 never contains it. The census's own
  `resolve()` returns `('UNDECLARED','','')` for `0x02EBA3F8`, and `types.tsv`/`fields.tsv` have 0 hits. The
  resolver works and the extraction never asked it.
- **Record-relative state** (`Type +0xNN`) is never checked. **[re-verified]** S-22's env-scaling contract §3 (L56–57)
  names `ActionDefinition +0x13 u8 element mask`. No `ActionDefinition` type exists, no field row anywhere carries an
  element mask at `+0x13`, and the census scored the contract "3 FIELD, zero undeclared" from its three absolute
  addresses alone.
- **Existence is checked, not meaning.** S-22 `EvaluationContext +0x004` is `SEMANTICALLY IDENTIFIED` while its own
  text says *"what any of the three means is not established"*. **[re-verified]** Its only write merges two dwords
  of the third argument: `00384808 mov eax,[r8+0x64]` / `00384811 or eax,[r8+0x3C]` / `00384818 mov [rcx+4],eax`.
  S-39's `OrderedCommandList +0x2A` / `OrderedObject +0x08` rows contradict the contract's §14 **[sub-instance]**.
- **Wider scan.** A rough scan of every credited contract's Types/State sections found record names missing from
  `types.tsv` under the same name in six MET systems: S-09, S-12, S-18, S-19, S-22, S-26. Five resolve to aliases
  (for example `CollisionBody` = `MovementBody`, and `FormulaEvaluationContext` = `EvaluationContext`), but **none
  of those aliases is recorded in `NAME-EQUIVALENCES.tsv`**. S-22 is the confirmed miss.
- This is the S-28 helper's pattern 5, and it is **wider than reported there**.

**SF-3. A runtime cell can say "every named invariant covered" on a case that cannot fail.**
- S-39 `G_handshake_I10` plants a constant word on one thread, so it cannot falsify a cross-thread premise.
- S-22 `we1.py` plants an action row with only `+8`, so "both stages read `+0x13`" is met by reading a zero byte.
- S-08 `pump_states.py` never runs kind `0xFF` or the real issue path. The FST entry is planted −1, so the run
  returns at `002DF7B9`.
- S-23 `ey.py` runs flag words with bit 1 set. The production leg (bit 1 clear, which calls `00469BB0`) has never
  run stub-free (see S-23).
- **This holds S-28's pattern 2 ("harness PASS = observation recorded") in two of five systems, S-22 and S-39.**
  S-07's `check.py` and S-23's `ey.py` assert fixed expected values that discriminate, so in those two the gap is
  coverage, not vacuity.

**SF-4. Contract text lags the scoring.**
- (a) **Stale §13 (S-28 pattern 3), which holds.** Four contracts read "None"/"Empty" although their runtime cells are
  MET on replays: S-22 `CONTRACT-formula-step-table` / `-environmental-element-scaling` / `-weapon-recipes` ("**None.**
  No experiment executes…"), and S-39 ("**Empty. Nothing in this contract has been observed**"). **[re-verified]**
- (b) **Stale cells after contract growth (S-28 pattern 1), which holds.**
  - **S-07.** The contract cell's receipt (2026-09-22, "V-5 holds") binds to text that SECTION-11 later overturned.
    `git show 457fe26dd` L202–204 says V-5 is *harmless*, *"an opcode above `0x63` … no fault"* and *"nothing here
    times it out"*. The current I5/I6 say the opposite: the `0025E5AF` read can fault, and a 65,536-instruction
    budget exists. The contract has 18 later commits, and the cell was never re-scored (EVIDENCE-POLICY rule 8).
    The runtime cell (09-26) also predates the 10-02 §7 cancel-notification clause, which the contract labels "a
    conditional static reading".
  - **S-23.** The runtime cell (09-26) predates the 09-27 floor ≤ cap qualification (`63df3d49b`) and the 09-28
    G4/G6 items (`96272843d`).
  - Across all 52 rows: every one of the 26 dated contract cells has later commits to its contracts. Most are
    cosmetic (pass-22 blocks, citations). The point is that nothing detects the substantive ones.
- (c) **Frontmatter.** 22 of 52 MET systems credit at least one contract still marked `level: L1` (S-02, 05, 09, 11,
  13, 19, 20, 22, 23, 24, 25, 28, 29, 30, 32, 38, 43, 45, 46, 47, 48, 52). S-23's only contract reads `level: L1`,
  `readiness: BEHAVIORALLY UNDERSTOOD`. **[re-verified]** S-07's three contracts read `local_production_status:
  "… formal independent acceptance pending"`, while their own trailing comment and both pages say "accepted
  non-author 2026-09-29 (OV-18)".

**SF-5. Bare cells are accepted without the record the rulings require.**
- 21 of 52 MET rows have a bare `MET` contract cell (S-01, 03, 04, 06, 08, 10, 12, 14, 15, 16, 17, 21, 23, 31, 33,
  37, 39, 44, 46, 49, 50). The 2026-09-20 scope ruling (`L2-VERDICTS.md` L14–16) requires the cell to record either
  the subsystem contract's path or `adequately covered by <contract> — <reason>`.
- 9 rows carry `N/A stated` script/data cells (S-02, 05, 18, 19, 20, 21, 23, 33, 38). **[re-verified]** S-23's is
  contradicted by its own contract §14 item 1 (L499–500): the HP floor is written only from the script VM (`005105E0`
  → `00239820`, `00239832`). S-21 (*"the battle message table"*) and S-33 (loot) are suspect on their subject text
  alone.

**SF-6. The validators do not pin their emulator.** The S-08, S-22 and S-23 packages reproduce under unicorn 2.1.4
only. The venv the lane is told to use (2.1.0) crashes at `uc.ctl_flush_tb()`.

**S-28's pattern 4 ("page contracted ≠ mechanism contracted") holds in three of five systems.**
- **S-08.** The file-layer pages are not contracted at all.
- **S-22.** All four pages are contracted, but the calculator-slot bodies are not.
- **S-07.** The interpreter's refusal side effect is stated only on an S-13 page.

## S-07 — zone-script VM and native bridge (SWE2-AUDIT-SPEC)

**Re-derived [re-verified]:**
- **Dispatch table.** `00261DF8` holds 100 RVAs. All 100 land in the 14,646-byte body, and 92 are distinct.
- **Lengths.** The words at `01EFEA60+op*24` read 0 for `0x00`–`0x02`, 1 for `0x03`–`0x47` and 3 for
  `0x48`–`0x63`.
- **Length lookups.** There are 22 in the body: 21 are followed by `sub r14,rax`, and 1 feeds `add r14,rax` @`0025E641`.
- **Entry.** `0025E4D8` zeroes the depth at `02099AC0` before any gate test.
- **Pre-decode and bound.** `cmp r12b,0x47`/`jb` sits at `0025E5A9`, the operand read is `0025E5AF movzx ebx,[r14+2]`,
  and `cmp eax,0x63`/`ja 0025E60A` bounds the dispatch.
- **Jump polarity.** It matches the BF-1 table: `0x53` `jle` skip, `0x54` `jl`, `0x55` `jge`, `0x56` `jg`, with
  Y = `[rsi+0xC]`.
- **Arithmetic.** `OPMOD` `0025F1D6` runs `cdq; idiv ebx` with no zero test, while the `OPDIV` integer path has
  `test ebx,ebx / je`. `OPSRL` uses `sar`.
- **Lifecycle `002621D0`.**
  - The id splits with `sar r12d,0xC`/`and r15d,0xFFF`.
  - The request is the fifth argument, `[rsp+0x90]`.
  - The begin callback's fifth argument is `[rsp+0x70]`, the manager.
  - A missing result leaves phase < 2, which appends an implicit int 0 (`0026227A`–`002622A3`).
- **Family tables.** `003DC2D0` fills 16 slots with `01F26720` (`rep stosq`), then overwrites 0/3/5/7. `003DC2A0`
  computes `inc rax; shl rax,5`.
- **Table contents.** Counts are 1,496/147/1/104/212, which is 1,960. The fourth slot is non-NULL in 0 rows.
  `result(count−1)` resolves to `00342560`, NULL, NULL, `00510970`, NULL, and the packed ends are `01F29418` and
  `01F29440`.

| # | point | result | evidence |
|---|---|---|---|
| 1 | implementable | **PASS** | The dispatch, lengths, stack, lifecycle N-1..N-7 and bridge are stated. Per-opcode effects are in `candidates/bf1-opcode-semantics/README.md` (100 rows, static, linked from the interpreter page §7), and the contract says it is "a bounded execution slice" (§1). Nit: the contract writes opcode ranges in bare hex ("03..47", "Opcodes >63", "Opcode32") next to a bare decimal "Depth63" (= `0x3F`). |
| 2 | types | **PASS** | `VmValueStack` 0x284 matches the four array stores (`0025F206`–`0025F219`, `00262292`–`002622A3`). `ActorWaitSlot` 0x28 is declared field by field (`+0x08` ordinal, `+0x0C` value, `+0x10` accumulator, `+0x14` kind, `+0x15` phase, `+0x18` scratch), all at PROVEN except the gap byte `+0x17`. |
| 3 | contract coverage | **PARTIAL** | §7 says *"A blocked actor gate discards previous evaluation depth while preserving the request PC and actor registers"*, generalised from the one arm SECTION-11 runs (`native_controls.c:59`, `+0x14 = 0x70`). The image has three refusal arms. **(a)** `+0x14` bit 6: return 1 (`0025E4FF`). **(b)** `+0x13` bit 0 or `+0x10C`, not exempted by `+0x0B` bit 5: return 1 (`0025E524`–`0025E53A`). **(c)** `+0x14` bit 4 **or** bit 5 clear: `call 0025B500`, then return 1 (`0025E504`/`0025E53F` → `0025E509`). `0025B500` clears `+0x0C` bit 6, `dec [02098E10+slot*0x288+0x1E4]`, rewrites `02099DB8` from three enable-gated counters, and when the sum is ≤ 0 calls `00226100` and tail-calls `002E1CD0(1,0xD)`. The S-07 contracts neither state nor link this; it is stated only on S-13's `the-record-behind-every-actor.md` (~L849) and the system-stop page. **[re-verified]** |
| 4 | claim class | **PASS** | SECTION-11 is "isolated original-instruction execution against synthetic state" with zero substitutions and zero bridges (`scope.json`). The bridge closer is NATIVE-REPLAY with `live_game:false`. BF-1 is labelled "NATIVE/STATIC". |
| 5 | script/data | **PASS (bare cell)** | BF-5 decodes the whole `.ebp` corpus (7,565 files, 114.9 M instructions), and none of the six inert opcodes appears at an opcode position. OV-17 covers operand bounds, and the five command tables are named authored data. The verdict cell itself names no evidence. |
| 6 | adjacent bounded | **PASS** | §14 and §16 bound the remaining opcode and wait semantics, reentrancy, live identity and field-frame composition. The exception is point 3. |
| 7 | validator vs prose | **PASS** | `s07-opus-replay-vm-bridge/check.py`, read in full, traps every IAT slot, fences an 8-function closure and plants only a stack and a record. Its 8 cases assert fixed expected values, exactly the runtime cell's list. SECTION-11's `claim_matrix.tsv` maps its 146 assertions onto I1–I7 with sites. |

**Verdict: ACCEPT-WITH-NARROWING.** Proposed contract-cell wording:

> MET for the interpreter's dispatch, length and stack model, the native lifecycle (N-1..N-7) and the bridge, re-scored
> against the SECTION-11/12 text. Refusal semantics are stated for the halt arm only. The enable-arm refusal
> (`+0x14` bit 4 or 5 clear → `0025B500`: `+0x0C` latch release, manager `+0x1E4` decrement, `02099DB8` recount,
> possible `002E1CD0(1,0xD)`) is unstated in S-07 and unexecuted.

Repairs:
- Re-score the contract cell against the current text (SF-4b).
- Reconcile `local_production_status` with the OV-18 acceptance.

## S-08 — resource request queue and file layer (SWE2-AUDIT-SPEC)

| # | point | result | evidence |
|---|---|---|---|
| 1 | implementable | **FAIL (scope)** | The registry subject is *"queue **and file layer** — 64 slots, the file-size table, loose files then the archive, the BigFile index"*. The only credited contract, `CONTRACT-resource-request-queue.md`, says in §7 that external read behaviour is separate, and in §14 that the read/file/archive layer is unresolved. It never links `file-size-tables-fst.md` or the BigFile-index page, and no contract `implements:` them. The contract cell is a bare MET (SF-5). For the queue alone the doc is implementation-grade. **[sub-instance; scope text re-verified]** |
| 2 | types | **PASS (queue) / FAIL (file layer)** | `ResourceRequestSlot` 0x80×64, `ResourceRequestQueue` 0x28, generation, read status and override table are declared. Constructor `0032E450` matches the slot rows (`cmp edx,0x40`). The file layer has no FST, VBF or BigFile type. Nits: `+0x22`/`+0x23` names are swapped against their own descriptions, and the `022C5150` "referenced nowhere else" claim is wrong because it is slot 63's `+0x10` link. **[sub-instance]** |
| 3 | contract coverage | **FAIL (one named defect)** | §7 row 1 (L177): *"Kind-FF nonzero submit result revisits the same head; … **Every other kind is taken as issued**."* But `002DF6C0` returns `xor eax,eax` on every path (`002DF747`, and `002DF77C` → `002DF749`), so `0032E116 test eax,eax / 0032E118 jne` is dead in the shipped image. Kind FF is taken as issued too, and a null stream open leaves `0215EFF4` stale exactly as RC-37 describes for other kinds. **[re-verified]** I3, I4 and I6 hold at `0032E870` (free-head stall, `shl ecx,6`/`and 0x3F`/`cmovg`, 0x800 rounding). `0046E030` = `call 002DF780; mov eax,1`, and `0046DFE0` = `cmp [0215EFF4],-1; cmove eax,2`. **[sub-instance]** |
| 4 | claim class | **PASS** | Static, NATIVE-REPLAY and live are kept apart, with `live_game:false`. |
| 5 | script/data | **FAIL** | The cell is a bare MET. The issue path's one authored dependency, the `.fst` table, is not linked from the contract or the row. |
| 6 | adjacent bounded | **PARTIAL** | Completion as state 5 or 6 is decided only by `0215EFF4`, whose producer (`001D6DD4`, callback `001D6D70`) is in the excluded layer. That is a cross-operation dependency, so under FRONTIER's adequacy test the narrow contract is not adequate for the subject as written. |
| 7 | validator vs prose | **PARTIAL** | `pump_states.py` 8/8 reproduced md5 `32bc3d9c`. It runs the shipped pump closure with imports trapped and callbacks disclosed as recorders. But every request is kind `0x24`, so `0032E105`–`0032E12B` never runs. S1 runs only the refused-read path (FST entry planted −1 at `02F73B6C`). The busy gate and empty-list rows have no assertion. So "executes every §7 state row" is broader than the run. **[sub-instance]** |

**Verdict: ACCEPT-WITH-NARROWING.** Proposed wording:

> MET for the resource request queue: the 64-slot pool, requester/builder (`0032E620`/`0032E780`/`0032E870`/
> `0032E990`), recycle `0032EC40`, pump `0032E070` and cancel `0032E590`. With planted completion, the pump executes
> §7 S1–S6 and C1–C3/CE for non-FF kinds. The kind-FF branch has no shipped-code execution. The file layer (FST
> sizing, `002DF780`/`002DF6C0` issue, BigFile index, the `0215EFF4` producer) is not scored at L2: no contract, no
> types.

**Escalated to OPUS (scope only):** either split the file layer into its own registry row, or score S-08's contract
cell SCOPE-SHORT. Under the second option, S-08 is not L2 MET.

**Producer repair:** §7 row 1 must say that `002DF6C0` returns 0 on every path, so the "nonzero revisits" clause is a
dead branch.

## S-23 — HP write and lethal transition (SWE2-AUDIT-SPEC)

| # | point | result | evidence |
|---|---|---|---|
| 1 | implementable | **PASS** | `00300530` (0x370 B) matches §2–§10. The clamp is floor first, then the cap; `max(old,1)` applies under 0x10000, doubled under `bt ecx,0x1c`. There is a single store `00300749`, the lethal test `0030078B cmp [rsi+0x48],floor / jg`, and the event inversion `neg r13d; sbb; add 0x2008` vs `lea edx,[r13+0x2005]`. **[sub-instance; lethal and store sites re-verified]** |
| 2 | types | **PASS** | `BattleStatsRecord` +0x24/+0x3C/+0x48/+0x64, `BattleUnit` +0x30/+0x48/+0x778 and `BattleTargetEntry` +0x08 are all declared. |
| 3 | contract coverage | **PASS (wording fixes)** | §13a L376 says *"Gate-3 refusal suppresses the store and the lethal block"*. **[re-verified]** Gate 3 is asked only when `[rsp+0x50]==0` and the delta is ≤ 0 (`0030072F`–`00300738`). A refusal jumps to `0030074D`, past the store, and `jle 00300784` then runs the lethal test on the **unchanged** `+0x48`, so a refused zero-delta at or below the floor re-runs the death sequence. Separately, "all three callers" counts direct E8 calls only; the main caller `003112F0` reaches it via `call rax` (`00311668`). |
| 4 | claim class | **PASS (frontmatter)** | §13 is honestly isolated-replay, but the contract frontmatter still reads `level: L1` / `BEHAVIORALLY UNDERSTOOD` (SF-4c). |
| 5 | script/data | **FAIL (cell label)** | "N/A stated" is contradicted by the contract §14.1 (L499–500): the floor setter `00239820` (`00239832`) is reached only from VM verb `005105E0`. The death also posts battle-message row 0x10, and `SpawnRecord.death_count` has a script reader. |
| 6 | adjacent bounded | **PARTIAL** | **[re-verified]** `[rsp+0x58] = ~(flags>>1)&1` (`00300580`–`0030059C`), and `0030079C cmp [rsp+0x58],0 / je` skips `call 00469BB0` only when flag bit 1 is set. The combat applier builds the flag word from result bits only into bits 4/5/6/8 (`00311608`–`00311651`). Bit 1 is never set, so **`00469BB0` runs on every combat kill**. The runtime cell calls it "callee-depth … outside the contract's subject" and says it "ran real under EXP-093", but EXP-093 L49–63 stubs `005369C0` and `0046A800` inside it. |
| 7 | validator vs prose | **PASS (notes)** | `ey.py` 7/7 reproduced md5 `b131fd68`. It patches no application code and runs a closure allow-list, with undisclosed bridges `sqrtf`×14 and `memset`×8. Its assertions discriminate. The cell's "480+400→500" is the no-Bubble control; with bit 28 the result is 880. **[sub-instance]** |

**Verdict: ACCEPT-WITH-NARROWING.** Proposed wording:
- **Runtime:** "stub-free on flag words with bit 1 set. The combat applier never sets bit 1 (`00311608`–`00311651`), so
  the production lethal leg through `00469BB0` has run only under EXP-093, with `005369C0`/`0046A800` stubbed."
- **Script/data:** "MET (linked): script-only floor `005105E0`→`00239820`, the `death_count` script reader, battle
  message 0x10", replacing "N/A stated".
- **Contract §13a:** "…suppresses the store; the lethal test still runs on the unchanged HP."

## S-22 — formula step table and calculator slots (SWE2-AUDIT-SPEC)

**Re-derived (held) [sub-instance]:**
- 202 slots at `01EFA5C0`, with slot 202 = `3F80000000060303`.
- 152 distinct targets; 42 no-op slots point at `0016D6A0`, which is `c2 00 00`.
- Seven multi-id targets.
- 109 recipe pointers, terminator `000000B4FFFFFFFF`.
- Dual recipes order step 94 before 95.
- The resolver `00385F60` skip mask `0x4000140000004E` is tested by `bt`/`jae` at `0038624E`–`0038625C`, and the
  loop stops early at `003863D7 cmp [02AEDFB8],1`.

| # | point | result | evidence |
|---|---|---|---|
| 1 | implementable | **FAIL (partial)** | The table, recipe format, resolver, preparation family, env stage and finaliser are specified. Calculator-slot arithmetic is not. **[re-verified]** Slot 165 `0038F890` (used in 13 recipes, including every weapon recipe 20–29): `movzx ecx,[r8+0x20]`, `test cl,2` → `mulss [008FCC90]`=1.2; `test cl,4` → doubled loss stored to `02AEE004` **and** `02AEE014` (`0038F8CA`/`0038F8D0`). Pages give only its name and "reads `02AEE004`" (step-table page L299). Contract §14 L175: *"What 125 of the 152 targets do."* Slot 89 `0038AF20` ×3.0 is likewise unstated. **[slot 89 sub-instance]** |
| 2 | types | **FAIL** | (a) `ActionDefinition +0x13` is named in env-scaling §3 L56–57 but declared nowhere (SF-2), and the row's `+0x10`..`+0x14` are undeclared too. (b) `EvaluationContext +0x004` is SEMANTICALLY IDENTIFIED while its text says the meaning is not established, and the writer merges `[r8+0x64]|[r8+0x3C]` (`00384808`–`00384818`). **[re-verified]** Under the ruled types criterion, contract-named state is undeclared, so the cell is PARTIAL, not MET. |
| 3 | contract coverage | **FAIL** | Step-table §3 L58 / ST-4 call the three words `02AEE054`/`58`/`5C` *"the ONLY channel between steps"*. **[re-verified]** Slot 21 `00388F20` writes the hit chance `02AEDFE0` (`00388F37`, `00388FA1`), and slot 40 `00389670` reads it (`0038968D cmp [02AEDFE0],r8d`). Steps also set `02AEDFB8`/`BC`, which the loop reads. |
| 4 | claim class | **PASS** | Static plus NATIVE-REPLAY, with `live_game:false`. But three contracts' §13 still read "None" (SF-4a). |
| 5 | script/data | **PASS** | `recipe-users.tsv` maps all 109 recipes to action ids and weapon rows. |
| 6 | adjacent bounded | **FAIL** | The exclusion is explicit, not silent, but it removes the declared core, "calculator slots" (SF-1). |
| 7 | validator vs prose | **PARTIAL** | `we1.py` 4/4 reproduced md5 `5680857b`, with no app stub and an 871-function fence. The action row carries only `+8`, so "both stages read `+0x13`" reads a zero byte and no element rule fires (SF-3). **[sub-instance]** |

**Verdict: REJECT.**
- **Named defects:** contract-named `ActionDefinition` undeclared, so the types cell is not MET; ST-4 is false at
  `00388FA1`/`0038968D`.
- **Producer repairs:**
  - Declare the action-row type (`+0x08`, `+0x10`..`+0x14`).
  - Correct `EvaluationContext +0x004`.
  - Restate ST-4 as "the BattleFormulaScratch block (`02AEDFB8`, 0xA8) plus the result record".
  - Update the three §13 sections.
  - State the arithmetic of slots 165 and 89.
- **After repair, the most the evidence supports:** "MET for the step-table dispatch (ST-1/2/3/5), recipe selection
  and stop flag (RW-1/2), the preparation family 60–79, the env/element stage 94, the severe-weather gate 35/36 and
  the finaliser 113/125. The other calculator-slot bodies are not executed and are partly unstated."

## S-39 — render command list and graphics handshake (SWE2-AUDIT-SPEC)

| # | point | result | evidence |
|---|---|---|---|
| 1 | implementable | **PASS (minor)** | The list half is specified in §3/§4/§7/§12. §12 omits `0018B1B0`'s forward arm (`r9b=0`, used by `001F06D0` at `001F07BD`). **[sub-instance]** |
| 2 | types | **FAIL** | **[re-verified]** The handshake word `02EBA3F8`, named in §5 (L216–217) and I-10 (L200–202), is UNDECLARED, and the census never saw it (SF-2). The `OrderedCommandList +0x2A` (DISCOVERED, "no other access", but written at `001F3531`/`001F3556`) and `OrderedObject +0x08` rows contradict contract §14. **[sub-instance]** |
| 3 | contract coverage | **FAIL** | §10.1 (L319–321) says a failed `malloc` appends a null that is *"absorbed silently"*. **[re-verified]** The enqueue `0018C610` appends `rbx`=0 (`0018C655`, `0018C673`) to the vector its caller passes. `00182970` passes `0018CA40`'s return, `[01F7F5E8]`. The flush `0018C8F0`, which the teardown `001E0590` calls at `001E05B6` on the same `0018CA40` vector, does `0018C930 mov rdi,[rbx]` / `0018C933 cmp byte [rdi+0x10],bpl` with **no null test**; only its destroy loop tests (`0018C97A`). So a null entry faults on scene teardown. Also, §14.2's "sole reader `001F5D70`" of `+0x29` is wrong: `001E2AF0` reads it at `001E2D2C`. **[sub-instance]** |
| 4 | claim class | **PARTIAL** | I-10 ("the handshake wait never waits") rests on CG-3's static walk, bounded by §14.5. A single-threaded replay cannot test it, yet the runtime cell counts it as executed. §13 says "Empty", and §16 says FULL SUBSYSTEM cannot be claimed (SF-4a). |
| 5 | script/data | **PASS (qualified)** | The `jsondata-schema` evidence is real for this row (`ApplyJsonForCutSceneObj` slot 1 `001F29C0` → `001C3C30`, `ReadPresetDofForCutSceneObj` `001F3500` → `001C6E20`), though most of the corpus belongs to the render-parameter system. The reader's handling of the 30 non-strict files (27 of them cutscene files) is bounded in the schema README, not in §14. No other L2 row cites it. **[sub-instance]** |
| 6 | adjacent bounded | **PASS** | §14 bounds the `executeTarget` writer, UQ-228 and CG-3's limit. I-10's sentence should carry §14.5's bound. |
| 7 | validator vs prose | **FAIL (partial)** | `check.py` traps every import and has no app stubs. But `G_handshake_I10` plants a constant on one thread, so it cannot fail. The `r9b` ordering is printed, not asserted. The `0018B1B0` `+0x2C`/`+0x49C` selection is never exercised. No case puts a null in the owner list. `i2.py`'s "freed inside the flush" checks only final set membership. **[sub-instance]** |

**Verdict: REJECT.**
- **Named defects:** `02EBA3F8` undeclared, so the types cell is not MET; §10.1 is false at `0018C933`.
- **Producer repairs:**
  - Declare `02EBA3F8`.
  - Rewrite §10.1 as "the flush `0018C8F0` reads `[entry+0x10]` at `0018C933` without a null test, so a null owner
    entry faults on `001E0590`", and add a replay case for it.
  - Fix §14.2 to name two readers.
  - Align the `+0x2A`/`+0x08`/`+0x10` type rows (EVIDENCE-POLICY 4a).
  - Narrow the runtime cell to "I-1, I-3..I-6, I-8, I-9 executed stub-free on planted state; I-7's gate executed and
    its arming static; I-10's spin shape executed and its no-other-writer premise static (CG-3, §14.5); `0018B1B0`
    mark selection and `r9b` direction unasserted".
  - Update §13.

## Expansion recommended before terminal certification (SWE2-AUDIT-SPEC)

These are re-checks of existing cells. None of them is a new register, dashboard or percentage (package §11).
1. **Re-run the types census for all 52 rows** with extraction that also sees `width[ADDR]` cells and record-relative
   `Type +0xNN` state, and that cross-checks the declared meaning against the contract (SF-2). Expect at least S-22
   and S-39 to drop.
2. **Read every row whose cell excludes material from its denominator** (S-04, S-08, S-13, S-22, S-23, S-26, S-30)
   against its registry subject text, not its contract's invariants (SF-1).
3. **Give each of the 9 `N/A stated` script/data cells and each of the 21 bare `MET` contract cells** the reason
   their rulings require, or rescore them (SF-5).
4. **Sample "every named invariant covered" runtime cells** for cases that cannot fail (SF-3). Re-score any cell
   whose contract gained invariants after the cell's date (SF-4b).
5. **Pin unicorn in the replay packages** (SF-6).

## Limits (SWE2-AUDIT-SPEC)

- One system per family. The other 47 MET rows are not audited here, beyond the mechanical counts in SF-1, SF-4 and
  SF-5. Those counts measure the presence of a pattern, not that a cell is wrong.
- **[sub-instance]** findings were not re-run by me. Each verdict's named defect was.
- S-07's validator was read, not run. SECTION-11's 146 assertions were checked through `claim_matrix.tsv` and
  `native_controls.c`, not re-executed.
- No live evidence was gathered, and no claim here is about live behaviour.
- The S-28 helper's patterns (`Tools/work/SWE2-AUDIT-SEM/standin1003/l2sample/S-28-FINDINGS-PAUSED.md`) were tested
  in this sample.
  - **Hold:** pattern 1 (S-07, S-23), pattern 3 (S-22, S-39), pattern 4 (S-07, S-08, S-22), and pattern 5, which is
    wider here.
  - **Holds partially:** pattern 2 (S-22, S-39; not S-07, S-23).
