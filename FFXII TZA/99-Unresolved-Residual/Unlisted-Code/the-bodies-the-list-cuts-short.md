---
system: The bodies the list cuts short - functions.tsv's body_bytes against the control flow it is supposed to bound
category: 99-Unresolved-Residual
status: AUDITED - 164 listed bodies are truncated (corrected 2026-09-29 from 177; falsification pass 2), and every extension is adjudicated in a ledger of record: five by the applied UC-1 band, and 159 in _index/FUNCTION-EXTENT-ERRATA.tsv (158 underrun-extend rows applied by SWE2-FRONTIER at 906d5480a, plus 0026C8C0's existing identical row). The population readers still read only merge verdicts; their switch to the underrun-extend rows is tooling, carried by OPUS-REQ-DATA-UC1-BAND-UNDERRUN-EXTENDS. The 14 misclassified blocks are reclassified in section 3. Owner read 2026-09-29 (OPUS)
owner_layer: measurement - this is about the function table and what reads it, not about any one subsystem
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every listed entry walked as a control-flow graph over [entry, next listed entry) rather
    than over [entry, entry + body_bytes), following direct branches and resolving image-base-relative
    jump tables (`mov ecx, dword ptr [rN + rIdx*4 + disp]` / `add rcx, rN` / `jmp rcx`, table at
    BASE + disp holding RVAs); truncation counted from the END of the last reachable NON-PADDING
    instruction, since body_bytes excludes the int3 tail by convention; the adjudicated unlisted
    blocks tested for reachability from the listed body before them. Control throughout: 0037C3F0,
    eleven arms resolved, nine past the recorded end, out to 0037C6C3.
last_reviewed: 2026-09-29
audit:
  passes: 2
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state_2: opus-falsification-pass-2-2026-09-29-exe-73461d08 - check_body_underruns.py re-walks every listed body
    with every ret form, int3/ud2/hlt, indirect jmp through memory and noreturn calls as terminators, and follows an indirect
    jmp only through a bounded image-base-relative table. 164 truncated, 1,486 bytes; 13 of the 177 were the old walk's
    artefacts (repz ret read as not-ret, decode past jmp [mem], past noreturn calls, and into jump-table data).
  last_pass_kind_1: derivation
  last_pass_state: opus-body-bytes-underrun-1 - 177 listed bodies have non-padding code past
    body_bytes, 2,564 bytes in all, 19 of them with a jump table resolved. A first count said 592
    and was two thirds artefact - 394 overshot by zero bytes because the walk counted the
    terminating int3 - and that figure is not reported. 51 of the 1,471 adjudicated unlisted
    blocks are reached from the listed body before them: 34 already carry verdict=continuation, 3
    are ambiguous, and 14 carry verdict=body and are misclassified. None of the 139 established-floor
    blocks is among them, so the UC-1 floor is unaffected and the ceiling arithmetic is left to the
    blocked population task.
  crossref_clean: true
  reopened_count: 0
  note: promoted DOCUMENTED -> AUDITED 2026-09-30 by SWE2-AUDIT-SPEC (promotion sweep):
    falsification pass-2 controls re-executed - check_body_underruns.py reproduces 164 bodies /
    1,486 bytes beyond and all three stated controls (0037C3F0 truncated; 00148F10, 00862022 not);
    the pass-2 corrections are applied in the status line and section 3, so no standing killer;
    classified neighbour edges dispositioned; zero open boxes
---

# The bodies the list cuts short

FABLE found one function whose recorded extent is a fifth of its real body and asked what rests
on that. `0037C3F0` is recorded in `functions.tsv` as 248 bytes; its dispatcher indexes a jump
table and nine of the eleven arms lie past the recorded end, out to `0037C6C3`. The question
routed to OPUS was how much of the population work, and of any published denominator, derives
from `body_bytes`.

This page answers it by resolving the tables rather than inferring from the gap.

## The instrument, and the control that earns it

From each listed entry, walk the control-flow graph over `[entry, next listed entry)` — not over
`[entry, entry + body_bytes)` — following direct branches and resolving jump tables.

The tables are **not** addressed RIP-relatively here, which is why a scan looking for a
RIP-relative `lea` finds nothing:

    0037C4B3  cmp   eax, 0xa
    0037C4B6  ja    0x37c6db
    0037C4BE  mov   ecx, dword ptr [r12 + rax*4 + 0x25c6f8]
    0037C4C6  add   rcx, r12
    0037C4C9  jmp   rcx

`r12` holds the image base, so the table sits at `BASE + 0x25C6F8 = 0x0037C6F8` and its entries
are RVAs. **The control is FABLE's own case**: eleven arms, nine past the recorded end, code
reaching `0037C6F8`. The first version of this scan resolved zero arms and its control failed;
that run's numbers were discarded rather than reported.

**Padding is not a truncation.** A first count said 592 bodies overshoot — and 394 of them by
*zero* bytes, because the walk adds the terminating `int3` to the reached set and `body_bytes`
excludes the `int3` tail by convention. A count that is two thirds artefact is not a count. The
figure below takes the END of the last reachable **non-padding** instruction.

## What is actually truncated: ~~177 bodies, 2,564 bytes~~ 164 bodies, 1,486 bytes (corrected, pass 2, OPUS)

> **CORRECTED 2026-09-29 (OPUS, falsification pass 2).** The first walk read **13 terminated bodies as continuing** -
> 1,073 of the 2,564 bytes. It tested for the mnemonic `ret` and so walked past `repz ret` (`00148F10`, `001491A0`,
> `001492B0`); it let an indirect `jmp [mem]` fall through (`007A0FC0`, `00830EB0`, `00862022`, `0086202E`); it did not stop
> at calls to `noreturn` functions (`00829E10`, `0082A5D0` call `00824330`); and it decoded jump-table data after the
> dispatch as code (`002AB8F0`, `0056E880`, `006A3980`, `00713760` - every one of their tables' arms lies inside the
> recorded body). [`check_body_underruns.py`](../../../Tools/analysis-kit/gfz-scripts/check_body_underruns.py) re-walks
> every listed body with those terminators and passes three controls: `0037C3F0` truncated (FABLE's case, to `0037C6C3`),
> `00148F10` and `00862022` not. It **reproduces 164 of the 177, finds no new one**, and resolves 12 tables where the old walk
> claimed 19. The corrected list is
> [`listed-bodies-with-code-past-body-bytes-rewalk-0929.tsv`](listed-bodies-with-code-past-body-bytes-rewalk-0929.tsv); the old
> list is kept unchanged as the first run's raw result. Corrected histogram: 1-8 bytes 133, 9-32 27, 33-128 2, over 128 2. The
> four largest are `0037C3F0` (248 recorded, 528 beyond), `00729920` (189, 131), `00393240` (290, 41) and `00808D78` (330, 34).
> The first walk's figures follow as history.

| bytes past the recorded end | bodies |
| --- | --- |
| 1–8 | 137 |
| 9–32 | 28 |
| 33–128 | 8 |
| over 128 | 4 |

Nineteen of the 177 have a jump table resolved; the rest are reached by ordinary branches past
the recorded end. The four largest are `00148F10` (49 recorded, 539 beyond), `0037C3F0` (248,
528), `001491A0` (46, 133) and `00729920` (189, 131). The full list is
[`listed-bodies-with-code-past-body-bytes.tsv`](listed-bodies-with-code-past-body-bytes.tsv).

**177 is not FABLE's 457, and the two are not competing figures.** 457 is the SIGNATURE
population — an indirect `jmp reg` in the recorded body plus more than 16 bytes of unlisted space
after it — which FABLE stated in terms is suggestive rather than proof per case, because a table
parked after a COMPLETE body produces the same gap. 177 is the resolved measurement of how many
of those gaps really are the function continuing.

**The bodies this database leans on are not among them.** `WorldActorScriptVM_InterpretBytecode`
(`0025E4C0`, 14,646 bytes), `AiOrder_EvaluateTargetSelector` (`00301AD0`, 6,963) and the three
type dispatchers `002F3BC0`, `002F3910`, `002F4020` all have their control flow contained inside
their recorded extents. That is worth stating plainly: the alarm was justified and the specific
worry did not land.

## What it does to the population: fourteen rows, and the floor stands

A block reached by the previous listed function's own control flow is a **tail** of that
function, not a distinct body. Of the 1,471 adjudicated unlisted blocks, **51 are reached**:

| current verdict | reached | in the 139-block established floor |
| --- | --- | --- |
| `continuation` | 34 | 0 |
| `body` | 14 | 0 |
| `ambiguous` | 3 | 0 |

The 34 are already right — the adjudication caught them. ~~**The 14 with `verdict=body` are
misclassified**~~ **(CORRECTED 2026-09-29, pass 2: only five are tails - see the table below)**: they are arms and branch targets of the function before them, and the guard the
admissions table records for them — "predecessor ends in `ret`" — is exactly what the end of an
arm looks like, so it never could have separated the two. They are
`00148F41`, `001491CE`, `001492FF`, `006A3A5C`, `007137BC`, `0076666F`, `0078F3AF`, `007A104E`,
`007C2A29`, `007C9BF8`, `007DF1E2`, `00830EE5`, `00862028` and `00862034`, listed with their
predecessors in
[`unlisted-blocks-reached-from-the-listed-body.tsv`](unlisted-blocks-reached-from-the-listed-body.tsv).

**Re-derived 2026-09-29 (pass 2), block by block, from direct branches, table arms and whole-image references:**

| block | what it is | how it is reached | population today |
| --- | --- | --- | --- |
| `0076666F`, `0078F3AF`, `007C2A29`, `007C9BF8`, `007DF1E2` | tails of the function before | direct `jcc` from the predecessor | covered: the applied UC-1 band extends each predecessor over it |
| `001491CE`, `001492FF` | ~~switch data after `repz ret`~~ one `nop` of padding after `repz ret`, then code *(corrected 2026-10-02, OPUS: `001491CE`+0x2 begins the v 32x32 intra predictor and `001492FF`+0x1 the h 32x32 predictor, the libvpx bodies UC-3 names)* | ~~read by the predecessor's dispatch~~ no rel32 or pointer reference to either entry | held (UC-1 held rows, accepted) |
| `007137BC` | the 14-entry table after `jmp rcx` | the predecessor's table | held |
| `006A3A5C` | the predecessor's jump table itself | `006A39B1 mov edx, [rcx+rax*4+0x583A5C]` | not a body; outside the population |
| `00862028`, `00862034` | 6-byte `jmp qword ptr [rip+x]` import thunks | called directly (`call` x1 each) | correctly admitted as frontier bodies |
| `00148F41`, `007A104E`, `00830EE5` | unreferenced | no branch, table, call or pointer anywhere in the image | outside the population |

So the "misclassification" was the walk's, not the admissions table's, for nine of the fourteen. No population row is wrong.

**None of the 139 established-floor blocks is a tail.** The floor of 34,409 is unaffected. The
ceiling of 35,572 loses the 14, and that arithmetic is not applied here: moving a verdict moves
the population ceiling, and the population change is the blocked UC-1 task, which is blocked
precisely because a denominator move is not OPUS's alone to make.

## What else reads body_bytes

Thirty-one tools in the kit mention `body_bytes`. These use it as an extent or a denominator, so
they inherit the defect:

- `gen_uc1_routes.py` and `unlisted_admissions.py` build the listed extents as
  `(entry, body_bytes)`, which is what makes a truncated tail look like unlisted space in the
  first place. `unlisted_admissions.py` already applies an **errata** extent file,
  `_index/FUNCTION-EXTENT-ERRATA.tsv`, and re-measures a shortened body before adjudicating its
  successor block. That is the mechanism a correction would use — its `corrected_end` column
  takes any end, not only a shorter one — but all 43 of its rows today are the OVERRUN direction.
- `program_coverage.py` takes `size = body_bytes` — a published coverage figure.
- `receiver_flow_census.py` (`listed = start + body_bytes`) and `field_disp_scan.py` slice the
  decode window at `body_bytes`, so on one of the 177 they census a prefix of the function and
  report a clean result. That is the type lane, and it is the reason this was routed here. *(The count is 164 after pass 2.)*
- `check_body_hashes.py` hashes the recorded extent and already states the limitation.

`check_extent_overruns.py` audits the OPPOSITE defect — `entry + body_bytes` past the next listed
entry, 29 cases — and adjudicates them. ~~There is no sibling instrument for the underrun~~ **The sibling now exists**
(2026-09-29): [`check_body_underruns.py`](../../../Tools/analysis-kit/gfz-scripts/check_body_underruns.py), with its three
controls. The 159 extensions ~~not yet applied~~ *(answered: see "The 159 extensions applied (OPUS, 2026-09-29)" and "Resolved 2026-09-30" below; 2026-10-02, OPUS)* are prepared as `_index/FUNCTION-EXTENT-ERRATA.tsv` rows in
[`underrun-errata-rows-0929.tsv`](underrun-errata-rows-0929.tsv); applying them moves extents that `program_coverage.py`,
`receiver_flow_census.py` and `field_disp_scan.py` read, so the application is FRONTIER's
(OPUS-REQ-FRONTIER-EXTENT-ERRATA-UNDERRUN-159).

## What is not claimed

That the code past a recorded end always belongs to the same function. A `jmp` into the gap can
be a tail call to a genuinely separate unlisted body — FABLE found `002EB5D0`, an
argument-defaulting prologue, and `002EBD40`, a complete 19-byte setter. For a census that slices
`[entry, entry + body_bytes)` the distinction does not matter, because the code is missed either
way; for the population it matters entirely, which is why the 51 are listed individually rather
than folded into a number.

## Evidence

*Added 2026-09-30 (OPUS), gathering this page's claims for the terminal audit's pass 7. No claim is new; each row
points at the section and instrument above.*

| claim | evidence | tier | confidence |
|---|---|---|---|
| `0037C3F0`'s dispatcher indexes an image-base-relative table at `BASE + 0x25C6F8`: 11 arms, 9 past the recorded end, out to `0037C6C3` | `0037C4B3`–`0037C4C9` read; `check_body_underruns.py` control 1 | NATIVE/STATIC | PROVEN |
| 164 listed bodies are truncated, 1,486 bytes past their recorded ends | `check_body_underruns.py` (every `ret` form, `int3`/`ud2`/`hlt`, `jmp [mem]`, `noreturn` calls as terminators; bounded tables; controls `0037C3F0`, `00148F10`, `00862022`); `listed-bodies-with-code-past-body-bytes-rewalk-0929.tsv` | NATIVE/STATIC | PROVEN, bounded by the walk's terminator set |
| the first walk's 177 / 2,564 was 13 artefacts too high | falsification pass 2, the four artefact classes, each with named sites | NATIVE/STATIC | PROVEN |
| the interpreter `0025E4C0`, `00301AD0` and the dispatchers `002F3BC0` / `002F3910` / `002F4020` keep their control flow inside their recorded extents | the same walk | NATIVE/STATIC | PROVEN |
| of the 14 reached unlisted blocks, 5 are tails the UC-1 band extends over, 3 are held switch data, 1 is a jump table, 2 are import thunks and 3 are unreferenced | pass 2 block-by-block re-derivation (direct branches, table arms, whole-image references) | NATIVE/STATIC | PROVEN |
| none of the 139 established-floor blocks is a tail; the floor of 34,409 stands | the same re-derivation | NATIVE/STATIC | PROVEN |
| the extent readers named in "What else reads body_bytes" slice at `body_bytes` | their source, read | SOURCE-PROVEN | PROVEN |
| since `d20226c17` (2026-09-30), `program_coverage`, `field_disp_scan`, `receiver_flow_census` and the executable view read the adjudicated `underrun` ends | `uc1_band.apply_extents`; `test_build_views` B11 (16,914 UNKNOWN bytes move) | SOURCE-PROVEN | PROVEN |
| that the code past a recorded end always belongs to the same function | **not established**: a `jmp` into the gap can be a tail call to a separate body (FABLE's `002EB5D0`, `002EBD40`) | — | UNKNOWN |

## Falsification pass 2 - 2026-09-29 (OPUS): the walk, not the population, was wrong

Prompted by the status-currency rule's owner read (FABLE, b27e23f80): before re-statusing, the residue was re-derived.
[`check_body_underruns.py`](../../../Tools/analysis-kit/gfz-scripts/check_body_underruns.py) states its killers as
controls: FABLE's `0037C3F0` must come out truncated, and `00148F10` (ends `repz ret`) and `00862022` (a `jmp [mem]` thunk)
must not. Its walk treats every `ret` form, `int3`/`ud2`/`hlt`, an indirect `jmp` through memory and a call to a `noreturn`
function as terminators, and follows a register jump only through a bounded image-base-relative table.

- **The headline was 8 % too high in bodies and 42 % too high in bytes**: 164 and 1,486, not 177 and 2,564.
- **The fourteen "misclassified" blocks were mostly not tails** (section 3's new table); the population needs no row change.
- **Tried and not broken:** all three table sites the old walk used to "extend" the four largest bodies resolve with their arms
  inside the recorded body; the five blocks the band extends over are reached by direct branches, as the band assumed.
- **Consumers:** `_index/candidates/uc1-held-rows-opus/` already said the held switch tables are data, not body (agrees);
  `uc1-extent-collision-consumer-check.md` carries `007C2A29` as pending (agrees: a real tail, extended by the band).

## The 159 extensions applied (OPUS, 2026-09-29)

SWE2-FRONTIER applied the prepared rows at `906d5480a`
([`consumer-check.md`](../../_index/candidates/underrun-errata-apply-0929/consumer-check.md)):
- **158 new `underrun-extend` rows** in `_index/FUNCTION-EXTENT-ERRATA.tsv`, recovering 1,461 bytes past listed ends.
- **`0026C8C0`** already carried the same verdict with the identical `corrected_end` `0026CDF3`.
- **Seven entries** now carry two rows, one per verdict: an interior alignment pad and an end-of-body underrun.

~~**Stated limit, carried as tooling.** The errata readers (`unlisted_admissions.load_errata`,
`script_verb_shapes.load_corrected_ends`) filter `verdict == "merge"`, and the population readers go through `uc1_band`.
So no census reads the grown extents yet, and the prefix-only censuses named above still see a prefix of these bodies.
The switch is `OPUS-REQ-DATA-UC1-BAND-UNDERRUN-EXTENDS`. It is a reader change, not open knowledge.~~
**Resolved 2026-09-30 (OPUS, `d20226c17`, the chained-tails apply).** `uc1_band.apply_extents` reads every adjudicated
`underrun` row, taking the furthest end per entry; the 254 `pdata-chain` rows joined the ledger in the same commit.
`program_coverage.py`, `field_disp_scan.py`, `receiver_flow_census.py` (which now accepts the adjudicated end) and the
dashboard's executable view (definition v4) read the grown extents. `unlisted_admissions` and `script_verb_shapes` still
filter `merge`. Whether they should read the grown extents is not assessed here.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**This page cites bodies because the function list cuts them short, and uses four as walk controls. Their
neighbours are their own call graphs; the page claims only the extents.**

**Script_VM_Native_Bridge and ActorEntity — CLIENT, 34 edges, through `WorldActorScriptVM_InterpretBytecode`
(`0025E4C0`).**
- The interpreter, one of the truncated bodies, calls 17 script-VM helpers (`WorldActorScriptVM_ServiceRequestWaitState`,
  `VMNativeCommand_ExecuteLifecycle`, the `ScriptVM_WaitList_*` probes and more).
- It also calls ten actor-entity helpers (`ActorManager_GetRecordByOrdinal`, `ActorResource_RemoveActiveEntry`,
  `ActorResource_RecycleEntryRange`, `ActorResource_GetEntryByOrdinal` and more).
- The target selector below walks the battle units, and `0037C3F0` calls `00263FF0`.

**CombatAI, Gameplay, CombatAction, Party, WorldAreaField and Presentation — CLIENT, 23 edges, through
`AiOrder_EvaluateTargetSelector` (`00301AD0`).** Another truncated body, it calls its usual gambit callees:
- the selector scalar, the relation and distance tests, and the eligibility tests;
- the encoded-id dispatch and the buffer reset;
- the focus and leader resolvers;
- the field record reads;
- the view-frustum test.

Its behaviour is `CONTRACT-gambit-walk`'s.

**Movement and Input — MECHANICAL, two edges.** `WorldActor_UpdateRuntimeAndScriptExecutionState` calls the
interpreter, and the dispatch `002AB8F0` (a jump-table control in pass 2) calls `001E0C10`.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*
- **Save_Load_Settings - SERVICE (1 edge).** `0026C8C0` reaches bodies filed to save/load/settings: `002EF2B0` - shared machinery across the layer boundary, no shared ownership.
- **Story_Event_Quest_Hunt - SERVICE (1 edge).** `0026C8C0` reaches bodies filed to story/event: `00377440` - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-the-bodies-the-list-cuts-short-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0082A5D0` | 135 B | Increments the word at `+0x46` of the object at `rcx+0x38` and returns when it is at most 0xC8 (unsigned `jbe`); otherwise, with the state record at `rcx+0x30`, it takes a location string (`01CCCFD8` when the dword `+0x68` of the record's first-qword object is zero, else `0081BFF0` formatting `01CCCFE8` with that dword), formats `01CCD000` with `01CCD068`, 0xC8 and that string through `0081BFF0` (both formats on the qword `+0x38` of the record's `+0x18` object), and passes the result with the record's `+0x18` qword to `00824330`, where the listed range ends. | `0082A5E3`, `0082A5EF`, `0082A628`, `0082A646`, `0082A652` |
