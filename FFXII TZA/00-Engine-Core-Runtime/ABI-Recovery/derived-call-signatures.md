---
system: Derived call signatures - recovering an ABI from register liveness
category: 00-Engine-Core-Runtime
status: DOCUMENTED — every register row is closed: stack arguments are detected callee-side (UQ-1, answered 2026-09-17); the 27 lower-bound forwarders narrow rather than inherit (UQ-3, answered 2026-09-17); the 222 outside the frontier were a stale premise, 442 today, in derived-call-signatures-explained.tsv (UQ-4, answered 2026-09-17); types beyond slots (UQ-2) are SUPERSEDED 2026-09-27 under FRONTIER's class-1 ruling, the 562 rows enumerated and position 1 typed for 51, the residue carried by the register row UQ-2 and uq2-p1-representation.tsv (151 pointers and 16 undecided of 321); owner read 2026-09-29 (OPUS)
owner_layer: CodeDomain:ABI_UNRESOLVED_DEFAULT
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: read-before-write liveness over a basic-block worklist, validated against 46 signatures
    parsed mechanically out of the CONTRACT-*.md interface tables
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-abi-recovery-1 - the page IS the measurement. 562 functions tagged
    ABI_UNRESOLVED_DEFAULT analysed; 535 settled, 27 lower bounds. The instrument was validated
    FIRST against 46 contract-stated signatures at 95.7%, and the two disagreements are contract
    errors corrected by this pass, not instrument errors.
  crossref_clean: false
  reopened_count: 0
---

# Derived call signatures

> **784 functions carry `ABI_UNRESOLVED_DEFAULT`** - a tag that records what the classifier could
> not work out. This page works out as much of it as register liveness can, says exactly how far
> that is, and does not pretend it is more.

## 1. What a derived signature is, and is not

**A parameter is a register read before anything writes it, on some path from the entry.** That is
all. It gives arity, which slots are used, whether a value comes back in `rax`, and whether the
entry spills argument registers to their home slots - the MSVC variadic prologue.

> **A derived signature is not an explanation.** Knowing a function takes three integers and
> returns a value says nothing about what it does. **This page disposes of nothing and does not
> move the EC-7 frontier**, and the 562 functions below are still in it *(answered: see the 2026-09-17 update below, the frontier now holds 342; 2026-10-02, OPUS)*.

## 2. The instrument was validated before it was used

Signatures were parsed **mechanically** out of every `CONTRACT-*.md` interface table and compared
against the derivation:

| | |
|---|---:|
| control rows parsed from contracts | **47** |
| derivation matches the contract | **44** |
| disagrees | **2** |
| skipped - tail-jump forwarder | 1 |
| **accuracy on comparable rows** | **95.7%** |

> **The control had to come from the documents.** My first control list was assembled from memory
> and scored five misses; three of them were my memory being wrong, including one where I
> "remembered" a four-argument signature for a function the contract plainly documents as taking
> two. **An instrument validated against a person's recollection is validated against nothing.**

## 3. The two disagreements are contract errors

A validated instrument disagreeing with a document is a finding about the document.

**`0031B760`** - documented `()`, and its complete 13-byte body is:

```asm
test rcx, rcx
jne  0x31b768
xor  eax, eax
ret
jmp  0x263e30
```

It **reads `rcx`, null-tests it, and returns 0 when null.** It takes one pointer. The same
contract's own key-address table names it `ActorWork_GetBattleUnit`, which takes an `ActorWork*` -
so the interface row contradicted the page it sits in.

**`003299B0`** - documented `(BattleUnit* rcx, int event edx)`, and at `003299C2` it executes
`mov dword ptr [rcx + 0x2C], r8d`. **It takes a third argument** and parks it at `+0x2C` across the
call to `002EB030`, then writes `0` back there at `003299F6`. A reimplementation built from the
two-argument row drops a value the callee reads.

Both rows are corrected in
[`CONTRACT-group-completion-and-respawn`](../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md) §2.

## 4. The result over the unresolved population

**562** of the 784 tagged functions are still in the EC-7 frontier and were analysed:

> *Re-measured 2026-09-17 (FABLE): the frontier now holds **342** of the 784 (arity 0 → 79, 1 → 104, 2 → 95, 3 → 38, 4 → 26; 25 lower bounds). The 562-row table below is the dated result and is left as published; the 442 now outside the frontier are in `derived-call-signatures-explained.tsv` (`UQ-4`).*

| derived arity | functions |
|---:|---:|
| 0 | 144 |
| 1 | 163 |
| 2 | 155 |
| 3 | 63 |
| 4 | 37 |

- **535 settled**; **27** are tail-jump forwarders whose arity is only a **lower bound**.
- **468** write `rax` before returning.
- **6** use a float argument slot.
- **7** spill argument registers to their home slots at entry - the **variadic** shape, the same one
  that turned out to matter for `005A7E90` in
  [animation channel binding](../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md).

The full table is [`derived-call-signatures.tsv`](derived-call-signatures.tsv), one row per
function, with the lower-bound flag carried per row so no consumer can lose it.

## 5. Two rules learned by getting them wrong

1. **`xor r, r` is not a read.** Capstone reports the register as read - the instruction does read
   it - but the zeroing idiom does not. Before this was special-cased, **every** function containing
   `xor ecx, ecx` looked like it took a parameter in `rcx`, and `SpawnGroup_ResetLifecycleLedger`,
   which takes none, was derived as taking one.
2. **A `call` does not forward arguments; a tail `jmp` does.** The first version treated both as
   pass-through and flagged **326 of 562** results as unusable lower bounds. After the fix: **27**.
   After a call returns this function continues, and a register the callee happens to read is not
   thereby a parameter of ours.

## 6. What is not known

- [x] ~~**UQ-1.** **Stack arguments are not detected.** A fifth-and-beyond parameter arrives above the shadow
      space and this pass does not read frame layout, so **every arity here is a count of register
      slots, not necessarily of parameters.** `002465F0` is the known case *(answered: see the note below, `002465F0` is not in the dataset; 2026-10-02, OPUS)*: four register arguments
      and a fifth at `[rsp+0x20]`, derived here as 4.~~
      ***ANSWERED 2026-09-17 (FABLE): stack arguments are now detected, from the callee side, for every row, and twelve rows read one.** The detector reads each body with the frame displacement tracked through push and pop, `sub` and `add rsp` by an immediate, `mov rbp, rsp` and `lea rbp, [rsp+N]`, reset to the prologue value after every `ret` and `jmp`; any load, compare or test whose entry-relative offset is 0x28 or more reads a fifth-or-later argument (0x28 is position 5, eight bytes per position), stores are ignored and the home slots 0x08..0x20 belong to the four register arguments. Controls: `00632960` and `00632A10` read positions 5 to 8 at the offsets the reflection constructors are known to take, and four bodies that would fool a naive scan (epilogue restores after a tail jump in `001E0AA0` and `00323C60`, the `rax` frame of `001993B0`, the early-out prologue of `0057EBB0`) read none. Over the 562 rows, **12 read stack parameters**: nine with derived arity 4, one with 3 (`002FD420`, position 5), two with 2 (`008628F0`, position 5; `0085DDE0`, positions 7 to 9); the highest position anywhere is 9. Ten of the twelve lie inside the 75-row at-risk union of the RE-STATED block above and two (`002FD420`, `0085DDE0`) outside it, so that floor was a floor. Twenty-nine rows have at least one frame-relative read the tracker could not place (the stack aligned or adjusted by a register), so their result is itself a floor; none of the twelve depends on such a read except `00309480` and `00317930`, whose placed reads already show positions 5 and 6. The per-row result is [`derived-call-signatures-stack-args.tsv`](derived-call-signatures-stack-args.tsv) (562 rows: positions read, highest position, first reading instruction, whether every read was placed). The arity column of the main table is left as published; the new table is the correction. Static; nothing executed.*

      **BOUNDED 2026-09-13 (OPUS):** ~~*"every arity here" is 37 of 562, not all of them*~~ —
      **and the example this bullet names is not in the table.**
      *(The struck clause is superseded by OPUS's own RE-STATED block below, which reads
      "the at-risk set is at least 37 + 38 = 75 of 562 (13.3 %), not 37 (6.6 %)". The 2026-09-16
      repair struck the two body sentences carrying that figure and left this heading, which
      states it too — and a heading is the first thing read, so the bullet opened on the number
      its own correction rejects. Struck 2026-09-16 by FABLE, author of the contradiction, as
      the completion of a repair OPUS began; OPUS recused itself from judging whether the repair
      was complete, and my answer was that it was not. **The bound survives as a bound** — the
      bullet's "every arity here" really is not all of them — only the figure was stale.
      `FABLE-REFUSES-UQ1-MARKER-DISPOSITION-THE-BOUNDED-HEADING-IS-STILL-LIVE`.)*
      **The ABI does the bounding, not an instrument.** A fifth integer argument reaches
      `[rsp+0x20]` only once `rcx`/`rdx`/`r8`/`r9` are all allocated, so a row can hide a stack
      parameter only if its arity is already **4**. The distribution in
      [`derived-call-signatures.tsv`](derived-call-signatures.tsv) is **0 → 144, 1 → 163, 2 → 155,
      3 → 63, 4 → 37**, so ~~**525 of 562 rows cannot be affected by this caveat at all** and the
      warning applies to **6.6%** of the table.~~
      **With one leak, stated rather than glossed.** Liveness sees a position only when something
      *reads* it. A function declaring five parameters but never reading the fourth derives as 3 and
      still takes a stack argument. ~~**So the at-risk set is "the 37, plus an unmeasured tail of
      functions with a dead register parameter"**~~

      > **RE-STATED 2026-09-16 (OPUS), on FABLE's contradiction — the tail is not unmeasured, and
      > this table measures it.** The leak clause above was right about the mechanism and wrong to
      > call its population unknown, which made *"cannot be affected at all"* too strong for 38 rows.
      > An argument's POSITION is fixed by its register — `rcx`/`xmm0` 1, `rdx`/`xmm1` 2, `r8`/`xmm2`
      > 3, `r9`/`xmm3` 4 — so a row that reads a HIGHER position while leaving a LOWER one unread has
      > a dead position, and that is the leak, countable from the columns already here. OPUS
      > re-derived it independently of FABLE's report and got the same numbers:
      >
      > | | |
      > |---|---|
      > | rows with a dead position below their own maximum | **59 of 562 (10.5 %)** |
      > | dead by position | 1 → 49, 2 → 24, 3 → 14 |
      > | derived arity of those rows | 2 → 24, 3 → 14, 4 → 21 |
      > | of the 59, arity < 4 — inside the "unaffectable" 525 | **38** |
      >
      > **So the at-risk set is at least 37 + 38 = 75 of 562 (13.3 %), not 37 (6.6 %), and 487 rows
      > — not 525 — SHOW NO EVIDENCE OF UNDER-REPORTING**, which is a weaker and truer claim than
      > "cannot be affected at all". It is still a floor: a function whose every register position is
      > dead is invisible to this test too.
      >
      > It also explains a shape in the file that would otherwise read as a defect: **arity is not
      > `#int_regs + #flt_regs` in exactly those 59 rows**, because arity is the highest position
      > observed, not the count of registers listed.
      **`002465F0` IS NOT IN THE DATASET.** This bullet cites it as *"the known case… derived here as
      4"*, but it appears nowhere in the 562 rows — only six rows begin `0024` and none is this one.
      A reader cannot check the illustration against the table it illustrates.
      **AND A DETECTOR RESULT IS DELIBERATELY WITHHELD.** I scanned backwards from each arity-4 call
      site for a `mov [rsp+0x20…], reg` and found three functions flagged. **The control refused it:**
      run against the 49 call sites of the variadic logger `0017D280`, where fifth arguments must
      occur, it fired on 2. (24 of those 49 sites sit inside script-VM verb bodies — the
      `0050Cxxx`–`0050Fxxx` dispatch arms log through it — and the rest spread across
      **resource** `002EEEE0`/`001F4340`/`001B14E0`/`0017D9D0` and **save** `001DF350`/`001DE5D0`
      — so the control population is mostly Script_VM_Native_Bridge code; a second control on a
      render-path logger would be a different population.) The derived subjects' own callers are
      equally spread: `0031B760` is called by **gameplay** `0030BFB0`/`0030B050`/`0030BA30`,
      **movement** `00239210` and **party** `0030BEB0`; `002EB030` by `003299B0`/`003B7E20`;
      `003299B0` by `00313500`. That is consistent both with a working detector — most log calls pass
      fewer than five arguments — and with a broken one, so it discriminates nothing. **The three
      addresses are not published, because an uncontrolled detector's output is not a measurement.**
- [x] **UQ-2.** **Types are not derived, only slots.** Whether `rcx` holds a `BattleUnit*` or a `char*` is
      outside what liveness can say.
      ***NARROWED 2026-09-17 (FABLE): one position typed for 40 rows, from a different system.** Liveness cannot name a type, but RTTI can name one - a function installed in a class's vtable takes that class's `this` in `rcx`. Joining the 562 rows against the recovered RTTI method table ([members/rtti-methods.tsv](../Object-Model/members/rtti-methods.tsv), the committed snapshot of `rtti_recover.py`'s output; the audited single-class subset is [the vtable method index](../Object-Model/vtable-method-index.md)): **40 sit at a vtable slot**, so their position 1 is `Class*`; 24 belong to one class (mostly `Phyre::PFramework` input devices and the application object), 16 are ICF-folded across several classes, so their `this` type is a set (`0053DD10` sits in 24 vtables). Two of the 40 derive with position 1 DEAD (`0079D6A0`, `0079D730`: `rdx` read, `rcx` not) and four derive arity 0 - a `this` the body never touches, consistent with the dead-position leak `UQ-1` measures. Table: `derived-signatures-this-types.tsv` beside the page. What is not typed: every other position, and position 1 of the 522 rows at no vtable slot; the next route is the callers (an argument passed from a typed field or a typed getter), not done.*
      *Narrowed 2026-09-18 (FABLE): seven more rows have position 1 typed, by their own bodies.* A body that stores an RTTI-named vtable **through `rcx`** (or a register copied from it) is a constructor or destructor of that class, so its position 1 is `Class*` without any caller. Sweeping the 522 no-slot rows for that shape (every rip-relative `lea` of an `.rdata` address whose `[−8]` is a valid RTTI locator, then the store's base register traced back to `rcx`) finds seven: the `PFramework` input-device constructors `007927C0` (`PInputDeviceKeyboard`, arity 2), `00792870` (`PInputDeviceMouse`, 2), `00792940` (`PInputDevicePad`, 2, the base the three pad variants call), `00792AB0` (`PInputDevicePadDirectInput`, 3), `00792B70` (`PInputDevicePadSteamController`, 1), `00792CB0` (`PInputDevicePadXInput`, 3), each installing the base vtable first and the derived one last, and the non-deleting destructor `007935C0` (`PInputDevicePadDirectInput`, 1), which installs DirectInput, then Pad, then `PInputDevice` and frees `+0xB0` through `00809054`. One candidate was rejected on the rule: `001993B0` installs a `std::wofstream` vtable, but into a stack local at `[rsp+0x20]`, so its derived arity 0 stands and the class is not its position 1 — the rule is *stored through `this`*, not *installs a vtable*. Table: [`derived-signatures-ctor-types.tsv`](derived-signatures-ctor-types.tsv) beside the page. That leaves 515 rows at no slot and with no such store, for which the caller route is still the next step. Static: the sweep and the seven bodies.
      *SUPERSEDED 2026-09-27 (FABLE, Claude Opus 5.5) in the register (OPUS, cd73ae1d5) under FRONTIER's class-1 ruling (Extensions 2026-09-27c/d): the 562 liveness rows are enumerated, 228 typed; the residue - the 511 untyped position-1 rows - is a finite derivable list in OPUS's structural lane. Ticked on OPUS-NOTICE-FABLE-TICK-FIVE-SUPERSEDED-BOXES.*
      *Residue re-counted 2026-09-27 (OPUS), in the register row: of the 511 untyped rows, 140 have arity 0, 3 take position 1 in `xmm0` and 47 never read it, so 321 read `rcx` untyped. Their bodies settle the kind: 151 pointers, 133 integers, 16 undecided 64-bit values, 19 handed on untouched, 2 unused. The class-derivation residue is the 151 pointers plus the 16 undecided. Table `_index/candidates/uq2-caller-route/uq2-p1-representation.tsv`; controls `uq2_residue.py` and `uq2_p1_representation.py`.*
- [x] ~~**UQ-3.** Whether the 27 lower-bound forwarders inherit their targets' full signatures. Each names one
      tail target; none has been followed.~~
      **ANSWERED 2026-09-17 (FABLE) - 27 of 27 followed, and the answer is mostly no: they narrow, they do not inherit.** Method (2026-09-15): for each argument position the TARGET reads before writing, the forwarder either SUPPLIES it (writes that register before the tail jump - its own value, not a parameter) or PASSES it (never writes it - the target's read is the forwarder's incoming argument). **22 are EXACT** (the derived arity already covers everything passed through) and **5 RAISE**: `00321840` 0→1, `0079D620` 0→2, `00308010` 1→2, `003235C0` 2→3, `00323600` 2→3. The three branchy bodies held back on 2026-09-16 were read path-sensitively today: in each, the passed register is written on NO path, so the verdict does not depend on which arm runs. `002D6640`'s flag is explained rather than wrong - it has no unconditional `jmp` but a conditional tail jump `je 00249840`, whose target reads nothing. The `lower_bound` column therefore means *narrows* for 22 rows and *short by 1* for 5; the TSV is the instrument's output and is left as derived, the resolved arities live in the table under this box. Static, body reads.

      | forwarder | derived | tail target | target reads | verdict | arity | why |
      |---|---:|---|---|---|---:|---|
      | `00197980` | 2 | `00197990` FUN_00197990 | [1] | EXACT | **2** |  |
      | `001C1710` | 1 | `001C1810` SaveloadManager_RequestDisableAutosaveList | [1] | EXACT | **1** |  |
      | `002681C0` | 1 | `00269C70` PartyRoster_AssignActorToSlot | [1, 2] | EXACT | **1** | supplies 2 |
      | `0026D6D0` | 0 | `0026D6F0` Movement_SetRequestedSpeed | [1, 2, 3] | EXACT | **0** | supplies all three: `xmm1` from `01DFE0BC`, `xmm0` zeroed, `r8d = 2` |
      | `002A28E0` | 0 | `0036FF70` InputGameplay_GetRemappedHistoryMask04 | [] | EXACT | **0** |  |
      | `002A2940` | 0 | `0036FFC0` InputGameplay_GetRemappedHistoryMask08 | [] | EXACT | **0** |  |
      | `002A29A0` | 0 | `0036FFD0` InputGameplay_GetRemappedHistoryMask0C | [] | EXACT | **0** |  |
      | `002A2A00` | 0 | `0036FFE0` InputGameplay_GetRemappedHistoryMask10 | [] | EXACT | **0** |  |
      | `002D6640` | 2 | `00249840` FUN_00249840 | [] | EXACT | **2** | **the flag explained:** no unconditional `jmp`, but `002D6647 je 00249840` is a CONDITIONAL tail jump out of the body; the target reads nothing, and the forwarder's own `test cx` / `test edx` fix arity 2 |
      | `00308010` | 1 | `00308040` / `00308130` BattleUnit_HasNonPartyEngagementEvidence / BattleUnit_ComputePartyBattleStance | [1, 2] / [1] | RAISES | **2** | read path-sensitively: two tail targets (`je 00308130` when the `+0x698` record's byte 5 is zero, else `00308040`); `rdx` is written on NO path, so `00308040`'s read of it is the caller's argument |
      | `0030A880` | 2 | `0030A8A0` BattleUnit_CollectMappedFourSlotUnitsByFlags | [1, 2, 3] | EXACT | **2** | supplies 3 |
      | `0031EA90` | 1 | `0031E9F0` BattleDefinition_MapByte9ToRuntimeCategory | [1] | EXACT | **1** |  |
      | `00321840` | 0 | `00321770` BattleEnmity_AnyAboveThreshold | [1, 2] | RAISES | **1** | `xor edx, edx` supplies 2; `rcx` passes to `test rcx, rcx` |
      | `003235C0` | 2 | `00323910` BattleStats_SetLicenseNodeStateAndApplySideEffects | [1, 2, 3, 4] | RAISES | **3** | read path-sensitively: both arms supply 1 (`ecx = 0` when `cl > 0x27`, else the `0x1C8`-stride record at `[02EBF190] + 8 + cl*0x1C8`) and 4 (`r9d = 0`), read 2 themselves (`movzx edx, dx`), and neither writes `r8` — so position 3 passes |
      | `00323600` | 2 | `00323D10` BattleStats_CheckLicenseNodeAcquireReason | [1, 2, 3] | RAISES | **3** | same two arms as `003235C0` without the `r9d` store; `r8` passes on both |
      | `0032AB50` | 2 | `0030B570` BattleIdClassD_SetRuntimeFlagBit1IfSupported | [1, 2] | EXACT | **2** |  |
      | `00369080` | 0 | `00863520` FUN_00863520 | [2] | EXACT | **0** | supplies 2 |
      | `003690F0` | 0 | `00863800` FUN_00863800 | [1] | EXACT | **0** | supplies 1 |
      | `004686D0` | 2 | `00861F14` sqrtf | [] | EXACT | **2** |  |
      | `00581350` | 1 | `00249C60` FUN_00249c60 | [] | EXACT | **1** |  |
      | `005819F0` | 2 | `005C5230` FUN_005c5230 | [] | EXACT | **2** |  |
      | `005823B0` | 2 | `005C5230` FUN_005c5230 | [] | EXACT | **2** |  |
      | `00799860` | 0 | `007998E0` FUN_007998e0 | [] | EXACT | **0** |  |
      | `0079D620` | 0 | `00796FC0` FUN_00796fc0 | [1, 2] | RAISES | **2** | `mov ecx, 2` supplies 1; `rdx` passes, read at `00796FEA` |
      | `007A08A0` | 1 | `0079BDF0` FUN_0079bdf0 | [1] | EXACT | **1** |  |
      | `00862670` | 2 | `001E09B0` InputAPI_PollControlState | [1] | EXACT | **2** |  |
      | `008628F0` | 2 | `001E1120` InputFeedback_DispatchViaManagerGate | [1, 2, 3] | EXACT | **2** | supplies 1 and 3 — and reads `[rsp+0x28]` first, the fifth slot (`UQ-1`) |

- [x] ~~**UQ-4.** The remaining **222** `ABI_UNRESOLVED_DEFAULT` functions outside the frontier were not
      analysed here.~~
      **ANSWERED 2026-09-17 (FABLE), and the premise number was stale.** The tag `ABI_UNRESOLVED_DEFAULT` marks 784 functions; on the day the page was written 562 were in the EC-7 frontier and 222 outside it. Re-measured today the frontier holds **342** of them and **442** are outside - 333 since A-measured and 109 declared by a family (32 `Phyre PFramework module`, 17 `Trivial global accessors`, 12 `ScriptVM.VerbAdapter`, 11 `internal tail-call forwarders`, 7 `NativeLeaf.ClampedTableLookup`, …). The same validated instrument was run over all 442 (`abi_signatures.analyse`, no frontier filter): arity 0 → 106, 1 → 109, 2 → 110, 3 → 91, 4 → 26; 19 lower bounds; 376 return in `rax`; 5 use a float slot; 6 spill home slots. Table with each row's explaining family: `derived-call-signatures-explained.tsv` beside the page. A derived signature is still not an explanation: these rows are outside the frontier BECAUSE they are explained, and the family pages own their meaning.

## 7. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| the derivation is 95.7% accurate against documented signatures | 47 control rows parsed mechanically from `CONTRACT-*.md`; 44 match, 2 contract errors, 1 skipped | 1 |
| `0031B760` takes one pointer argument | its complete 13-byte body, above | 1 |
| `003299B0` takes a third argument in `r8d` | `003299C2 mov dword ptr [rcx + 0x2C], r8d`, and `003299F6` clearing the same field | 1 |
| 535 of 562 settled, 27 lower bounds | `abi_signatures.py --tag ABI_UNRESOLVED_DEFAULT` | 1 |

## 8. Related

- [`../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md`](../../05-Spawn-Encounter-Lifecycle/CONTRACT-group-completion-and-respawn.md) - the two corrected interface rows
- [`../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`](../../22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md) - `005A7E90`, where the home-slot spill turned out to be a variadic signature

*(Pass 22 live-graph completion, 2026-09-15: the signature corpus also touches `Presentation`
— `002EEEE0` is called by the console dispatcher `001D1660`, and `0030BFB0` calls `00308130`
(2 edges) — and `RNG_Random_Selection` — `00239210` calls `00328370` (1). The control
population's callees reach the render path and the random stream like every other shared
helper set.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: the dispatcher `001D1660` cited above also calls
`Audio` `002DEBA0`/`001DBB00` (2 edges) — the console machinery's audio legs, present in the
signature corpus as in every slice.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_DispatchActorPresentationEvent` is called by `BattleStats_ChangeStatusAndProcessSideEffects` and `BattleUnit_RecoverFromTerminalStatusSetIfClear`, so status changes post presentation events through it.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**UI — CLIENT, and the finding exists because one wrapper sits ONE CALLER below the hub cut.**
The UI layer reaches this page almost entirely through `00249C60`, a **51-byte** sound-request
wrapper owned by Audio: it gates on `0x2091098` and refuses `-1` before forwarding. Menu bodies ask
it for sounds — `BattleMenu_UpdateCommandSelectionAndDispatch` (9,374 B) is the heaviest of them —
and one further edge arrives through the six-byte `InputDevice_QueryAvailabilityState_Always1`.
**Neither is a claim by this page**: a derived signature is what the *instrument* recovered, and a
menu calling a sound wrapper says nothing about signature recovery. *Worth recording about the
instrument rather than the page: `00249C60` has **99 callers**, one below the >100 hub threshold the
neighbour surface excludes as substrate. One more caller anywhere in the image and this finding
disappears — so its existence is a property of where the threshold falls, not of how connected the
page is.*

**Items, equipment, shops and licence — BOTH DIRECTIONS, through the equipment and licence
predicates.** Seven of this page's subjects carry it, and the heaviest is
`Equipment_CheckItemEligibleForSlot` (`00317930`, 493 B), reached by five callers that are all
equipment-slot setters — the by-stats-index and by-mapped-id variants and the direct setter. The
rest run through the licence predicates `BattleStats_HasRequiredLicenseForEquipment`,
`BattleStats_CheckLicenseNodeAcquireReason` and `BattleStats_SetLicenseNodeStateAndApplySideEffects`,
and through `InventoryBitsetClass_MutateState`. **This page owns none of it.** Those functions appear
here because the instrument recovered their signatures; what they decide about equipment and
licences is the items layer's subject and is documented there.

**Rewards, progression and economy — CLIENT, one edge, and it is geometry.**
`Vector3_ComputeXZDistance` (`004686D0`, 35 B) is called by `Loot_FindOverlappingPickupIndex`
(253 B) — the loot-pickup overlap search measuring a distance in the XZ plane. **A shared geometry
helper being used by a loot search is not a crossing this page makes**, and the edge is here only
because the helper's signature is one the instrument recovered.

**ActorEntity — CLIENT (31 edges through 10 of this page's functions).** The ActorEntity layer reaches this page at `0031B760`, `00328370`, `003B7E20`, `00239210` and 6 more. `ActorWork_GetBattleUnitRaw` is the worked example, read in full - it is **five bytes** that say where the link is: `return [actor + 0x30]`, the actor's battle-unit pointer, with no test of any kind; **3 of the 25 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatAI — CLIENT.** `BattleUnit_SelectAiOrderSetVariantFromAuthoredTable`, owned by that layer, calls `0031B760` on this page. That caller is the variant choice, bounded at **four** indices: `word[[+0xE60] + 0x50 + index*2]` names a row in the table at `[02EBF168]`, and the resolved pointer is stored at the unit's `+0x6E0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**CombatFormula — CLIENT.** `BattleStats_ModifyHPAndProcessLethalState`, owned by that layer, calls `003299B0` on this page. That caller is the HP-modification entry point: it resolves the owning unit for both the source and the target, reads the target unit's `dword[+0x48]`, and decodes its flags argument bit by bit - bits 0, 1, 2, 4 and 5 each select a separate behaviour; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — BOTH DIRECTIONS, 61 edges, and every one belongs to the input stack's own pages.** The signature table
holds the input stack's entry points because they were `ABI_UNRESOLVED_DEFAULT`, and their input neighbours come with
them:
- the poll path `InputBridge_PollControlState` (`00862670`) → `InputAPI_PollControlState` (`001E09B0`) →
  `InputManager_PollAndBuildControlState`;
- the feedback path `InputFeedbackBridge_DispatchTwoBytePair` (`008628F0`, a UQ-3 forwarder row) →
  `InputFeedback_DispatchViaManagerGate` (`001E1120`) → `InputManager_DispatchFeedbackToDeviceById`;
- the four remapped-mask getters `InputGameplay_GetActorStateAwareRemappedMask04`-`10` (`002A28E0`-`002A2A00`) and
  their history-mask leaves `0036FF70`-`0036FFE0`;
- the `PFramework` input-device constructors `007927C0`-`00792CB0` and the destructor `007935C0` (the UQ-2
  ctor-typed rows), created by `InputSystem_CreateControllerForEnumeratedDeviceDescriptor` (`00797690`);
- the six-byte `InputDevice_QueryAvailabilityState_Always1` (`0053DD10`), called by
  `InputControl_UpdateRegisteredChannels` and `InputControl_UpdateChannelByIndex`.

**This page owns none of it.** It records the arity and liveness the instrument recovered. What those functions do
is documented in the input stack's pages (`input-stack-device-channel-and-bindings`,
`how-a-gamepad-becomes-a-controller-object`, `binding-profiles-remapping-and-control-state`).

**RNG_Random_Selection — SERVICE, two edges.** `RNG_SharedGameplayLCG_NextU32` (`00328370`) is a signature row here. It
is called by `BattleData_ResolveWeightedId` (`00308EC0`), and `00239210` calls it. The shared gameplay generator
serves both, and the RNG layer's `which-roll-is-on-which-generator` owns which draw is which. This page claims only
the draw's signature.

**Spawn_Encounter_Lifecycle — CLIENT, 32 edges through five of this page's functions.** The spawn layer consumes two
of this page's subjects wholesale:
- **`ActorWork_GetBattleUnit` (`0031B760`) has 25 spawn callers.** Among them are the `SpawnEntry_*` getters and
  setters (death limit, death count, ticks since last death, candidate unit id, respawn cooldown, script selection,
  range-reentry pending), `Spawn_SelectContinuousEntry`, `Spawn_SelectPreviousMapEntry`,
  `Spawn_SelectAndPrepareAutomaticEntry` and `SpawnUnit_FinalizeSpawnEntryActivation`. Each resolves an actor to its
  battle unit before touching the spawn-keep entry.
- **`RNG_SharedGameplayLCG_NextU32` has 5 spawn callers:** `Spawn_TrySelectCandidatePosition`,
  `Spawn_PrepareRandomCandidateForCurrentEntry`, `SpawnPoint_GeneratePositionFromAuthoredRegion`,
  `SpawnKeep_InitializeEntriesFromDefinitionTable` and `002398F0`.

The other three are single edges:
- `SpawnUnit_FinalizeSpawnEntryActivation` calls `BattleUnit_ShouldEnterEngagedActionState` (`00308010`);
- `SpawnGroup_RecordMemberDeathAndHandleCompletion` calls `BattleUnit_DispatchActorPresentationEvent` (`003299B0`);
- the one DEPENDENCY edge runs the other way: `BattleUnit_HasNonPartyEngagementEvidence` (`00308040`) calls
  `Spawn_ValidateCandidateDistanceToPlayers`.

The spawn lifecycle is documented in the 05 pages (`the-spawn-keep-entry-field-map`,
`when-a-group-is-wiped-and-when-it-comes-back`); this page holds the signatures they call.

**WorldAreaField — CLIENT, five edges.**
- The world tick `World_UpdateSimulationTick` (`00314020`) calls `0017D280` and `002DEBA0`.
- The field-frame orchestrator `BattleSystem_RunFieldFrameOrchestrator` (`00234590`) calls
  `BattleUnit_BuildFilteredFourSlotUnitBuffer` (`0030A880`).
- `003789A0` calls `0053DD10`.
- The one DEPENDENCY edge: `BattleUnit_CollectMappedFourSlotUnitsByFlags` (`0030A8A0`) reads
  `FieldData_GetActiveFieldRecordBit15`.

The tick order is documented in `the-world-tick-and-the-field-frame`. *These four entries: tier 2 - ledger names,
sizes and `edges.tsv`, no body read for the note (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-derived-call-signatures-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00197980` | 7 B | copies `edx` into `ecx` and tail-jumps `00197990(edx)` | `00197982` |
| `002681C0` | 9 B | tail-jumps `00269C70(rcx, sign-extended byte +0x12 of rcx)` | `002681C4` |
| `002D6640` | 61 B | when the word `cx` and `edx` are both zero tail-jumps `00249840` with the incoming registers; otherwise stores byte 1 at `02F973A0`, byte 1 or 0 for `edx` non-zero at `02F973A2`, and the word `cx` at `02F973AA`, `02F973A8`, `02F973A6` and `02F973A4`, and returns `cx` zero-extended | `002D6647`, `002D6652`, `002D6659`, `002D6660`, `002D6675` |
| `002FD420` | 267 B | takes the word `cx` as an id, loads the qword at `01EEBCC0 + (id >> 12)*0x58 + 8` and returns 0 when it is null; otherwise, in the 16-bit word at index `(id AND 0xFFF) >> 4` of that array, sets bit `id AND 0xF` when v is positive and clears it otherwise, where v is `edx` when `r8d` is non-zero and the old bit plus `edx` when `r8d` is zero; then calls `00325F40(id, old bit, new bit)`, also calls `0046A630(id, edx)` when `r8d` is zero and bit 0 of the fifth (stack) argument is set, and returns the new bit | `002FD461`, `002FD494`, `002FD4E9`, `002FD4F6`, `002FD509` |
| `0030BEB0` | 63 B | calls `0031B760(rcx)` with the incoming `rcx` and returns 0 when the result is null, when bit 3 of its dword `+0` is clear, when its qword `+0x698` is null or when byte `+5` of that object is non-zero; otherwise returns the inverse of bit 23 of the dword `+0` | `0030BEB4`, `0030BEC3`, `0030BEC7`, `0030BED3`, `0030BEDE` |
| `0030BFB0` | 96 B | calls `0031B760(rcx)` with the incoming `rcx` and returns 0 when the result is null or bit 4 of its byte `+0` is clear; otherwise loads its qword `+0x698` and, when the OR of that object's dwords `+0x64` and `+0x3C` has any bit of `0x8000201B` set, returns bit 23 of the result's dword `+0`; else, when the `+0x698` pointer is non-null and its byte `+5` is zero, tail-jumps `00308130(result, that pointer)`, and otherwise tail-jumps `00308040(result, 0)` | `0030BFC1`, `0030BFD0`, `0030BFD3`, `0030BFF9`, `0030C004` |
| `0032AB50` | 14 B | tail-jumps `0030B570(rcx, 1 when edx is non-zero else 0)` | `0032AB56`, `0032AB59` |
| `0057EBB0` | 163 B | returns at once unless `ecx` is 3; otherwise, on the object at `r8d` zero-extended, ORs 1 into dword `+0xC4` when `edx` is zero, or clears its bit 0 and ORs in 2 when `edx` is non-zero; when qword `+0xC8` is non-null calls `00247510(that qword, 0x1D, stack record)` with the record holding dword 3, a byte (byte `+0x39A` of the object at qword `02CA99C0`, or 0xFF when that is null) and dword `edx`; finally clears bit 1 of dword `+0xC0` when its bit 0 is clear | `0057EBD4`, `0057EBE4`, `0057EC0F`, `0057EC28`, `0057EC3A` |
| `00792870` | 206 B | on `rcx` makes self-linked list heads at `+0x8` and `+0x18`, stores `rdx` at `+0x28`, links the `+0x8` node at the tail of the list headed at `01F401E8` (tail pointer `01F401F0`) and sets the table pointer at `+0` to `01CB23F8` (after first `01CB23C0`); calls `00808FE4(rcx+0x30, 0x48, 6, 00792D90, 0016D6A0)`; zeroes byte `+0x1E6`, qword `+0x1E8` and dword `+0x1F0` and, in a three-step loop, bytes `+0x1E0` to `+0x1E5` and `+0x1F4` to `+0x1F6`; returns `rcx` | `007928A6`, `007928C2`, `007928D0`, `007928F3`, `00792920` |
| `0079D620` | 10 B | sets `ecx` to 2 and tail-jumps `00796FC0` with the other argument registers unchanged | `0079D625` |
| `007A08A0` | 65 B | returns 9 when byte `+0x69` of `rcx` is non-zero; otherwise, when dword `+0x64` is zero, calls the virtual slot `+0x48` of `rcx` and returns its result when that is non-zero; in the remaining cases increments dword `+0x64` and tail-jumps `0079BDF0(qword +0x58)` | `007A08A6`, `007A08AF`, `007A08C3`, `007A08CA`, `007A08D6` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-derived-call-signatures-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00511660` | 61 B | makes the call at `00511660+0x09` with the incoming registers unchanged and returns its value when non-zero; otherwise reads a and then b with the calls at `00511660+0x1A` and `00511660+0x24` (each with `r9`) and returns `002D6640(b, a)` | Interior anchor `00511669`; Interior anchor `00511670`; Interior anchor `0051167A`; Interior anchor `00511684`; Interior anchor `0051168D` |
