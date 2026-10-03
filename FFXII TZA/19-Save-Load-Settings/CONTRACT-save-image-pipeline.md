---
contract: Move one save image from live state to a file and back — four buffers, two copies, one size
category: 19-Save-Load-Settings
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md, Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md, Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md
entries: ["002EF570", "002EF5F0", "002EF620", "002EF630", "002EF640", "002EF650", "002EF690"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — the four buffer addresses and their spacing, every reference to each buffer
    image-wide, every site loading the image-size immediate, and both block-copy loops read in full
    **including the instructions after their `jne`**. **This records checks performed on that date,
    not the method of the original derivation**, which is on the three pages; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-save-image-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the save-image pipeline

> **Authored 2026-09-22 by FABLE.** S-43's binding gap is *"three family contracts span the subject
> but none states the subsystem"*. Those three —
> [`CONTRACT-save-image-buffers.md`](CONTRACT-save-image-buffers.md),
> [`CONTRACT-save-container-transform.md`](CONTRACT-save-container-transform.md) and
> [`CONTRACT-storage-read-completion.md`](CONTRACT-storage-read-completion.md) — are each
> `scope: family`, and between them they cover holding the image, wrapping it, and reporting a read.
> **What none of them states is what must be true as the image passes between them.**
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is six
> such invariants.

## 1. Purpose

Carry one save image between four fixed buffers, so that what the player's file contains is what the
running game held.

## 2. Interface

| operation | body | size |
|---|---|---:|
| clear the active buffer | `002EF5F0` | 35 B |
| clear it again, with the icall guard | `002EF650` | 50 B |
| get the active buffer | `002EF640` | 8 B |
| get the capture staging buffer | `002EF620` | 8 B |
| get the write-submission buffer | `002EF630` | 8 B |
| **copy active → backup** | `SaveImage_BackupActiveRuntimeBuffer` (`002EF570`) | 122 B |
| **copy capture → submission, then write** | `SaveImage_CopyCaptureToWriteSubmissionBuffer` (`002EF690`) | 161 B |

## 3. Types

| buffer | address | role |
|---|---|---|
| active runtime | `02164280` | the live save state |
| capture staging | `021BA940` | the snapshot taken when you save |
| write submission | `02211000` | what is handed to the file write |
| backup | `022676C0` | a copy of the active buffer — **see SV-4** |

Image `0x56690` (353,936 bytes); header `0x200` (512); payload from `+0x200`.

## 4. Preconditions · postconditions · invariants

### The six cross-operation invariants

**SV-1 — Four buffers, one spacing, and the padding is deliberate.** The three gaps are each exactly
`0x566C0`, and the image is `0x56690`, so **48 bytes of padding separate each image from the next**.
*The buffers are spaced, not packed*, and an implementation that packs them will have three of the
four at the wrong address.

**SV-2 — Both block copies are the same shape and BOTH ARE COMPLETE.** Each is a fully-unrolled
`0x80`-byte block loop — eight `movups` pairs — running `0xACD` (2,765) times, **followed by a
sixteen-byte tail copy after the loop**: `002EF5E3`/`002EF5E6` in the backup, `002EF70C`/`002EF70F`
in the submission copy. `0xACD × 0x80 + 0x10 = 0x56690` **exactly the image size**.

> *This is the invariant to check first, and it is a trap.* Stopping at the `sub rdx, 1 / jne` gives
> `0x56680` and the conclusion that the copy is **sixteen bytes short**. It is not; the tail is the
> two instructions after the branch. **The loop count alone is not the copy extent**, and the two
> functions agree only because both carry the tail — which is also an independent derivation of the
> `353,936` figure from the loop rather than from the literal.

**SV-3 — The image size is known in two layers, not one.** Six sites load the immediate `0x56690`:
three in this buffer family (`002EF5FD`, `002EF65D`, `002EF718`) and **three in the save-controller
layer** (`0057E42F`, `00581117`, `00581F2F`). *So the size is not encapsulated behind these
accessors; a change here would leave three other sites stating the old value.*

**SV-4 — The backup buffer is written by one function and READ BY NOTHING.** Image-wide, `022676C0`
has **exactly one reference** — `002EF570`'s own `lea`, the destination of the copy. The other three
buffers have 4, 2 and 3. **A complete, correct, 353,936-byte copy is made and nothing in the image
ever looks at it.** *It belongs with this database's written-and-never-consumed findings, and a
reimplementation may omit the buffer entirely without any observable difference — but should know it
is omitting something the original does.*

**SV-5 — The active buffer has two distinct clears.** `002EF5F0` and `002EF650` both `memset` it to
zero at full size. *(Corrected 2026-09-23, SWE2-CONTRACT: both reach `_guard_check_icall` —
`002EF5F0` tail-jumps to `0016D6A0`, `002EF650` calls it. The real difference is that `002EF650`
is a compound: it follows the clear with `00253A80` `SaveRuntime_InitializeHeaderAndImageBackedState`,
`002EF2D0` and `00238A80` — clear-**then-reinitialise** — while `002EF5F0` is the bare clear.)*
The callers are now known: the compound is taken by `0022B6E0`, `00280140` and `00394130`
(paths that must leave valid runtime state); the bare clear is taken only by `003601D0`, the
teardown path (§14.1).

**What the compound's reinitialise does** *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 335, which executed it; `00236760` and `00253A80`'s first and last stores re-read.)*. `00253A80` first zeroes the `0x58`-byte object behind
`02092758` and the `0x4818`-byte object behind `020927C0`. Then it restamps the active buffer's header dwords
`+0x58`–`+0x6C`, including the constants `0x131F3EA` and `0x4818`. It rebuilds the twelve image-backed pointer
descriptors, and ends by zeroing further ranges of the `020927C0` object. OPUS's run also saw it apply the sound
settings through the audio registry. That step is attributed to the run, not re-read here.

**SV-6 — The submission buffer is handed ~~to the writer~~ by tail-call to `0020E540`, with the size passed
explicitly.** *(corrected 2026-10-02, OPUS: `0020E540` is no writer — `0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`, checked at `0020E540`–`0020E576`; the copy reaches no file, and only `0057E310` and `00581DA0` reach the storage machine)* `002EF690` ends `jmp 0020E540` with the submission buffer in `rdx`, `0x56690` in `r8d`
and a ~~handle~~ **0/1 selector** in `ecx` obtained from `00236760` **before** the copy begins. ~~*So the handle is acquired
first and the copy is not conditional on it — an implementation that acquires the handle after
copying changes what happens when acquisition fails.*~~ *(2026-09-25, FABLE, Claude Opus 5.5, on OPUS block 335, which executed it; `00236760` and `00253A80`'s first and last stores re-read.)* `00236760` is five instructions long. It returns bit 12 of
the dword `d[q[02EBF190] + 4]` (`0023676A shr eax, 0xc` / `and eax, 1`). So there is nothing to acquire and nothing
that can fail. The writer receives a one-bit choice with `rdx = 02211000` and `r8d = 0x56690`. *~~What the writer~~
~~selects with that bit is the writer's question, not this contract's.~~* *(answered: it selects nothing — `0020E540` is a compiled-out stub, as corrected above; 2026-10-02, OPUS)*

## 5. State

**Owned:** the four buffers. **Written and never read:** the backup (SV-4). **Read, never written
here:** the ~~handle source~~ selector source `00236760`, a one-bit read, not a handle *(answered: see SV-6 and CONTRACT-save-image-buffers.md §14 item 2; 2026-10-02, OPUS)*. **Not this contract's:** the compress/encrypt transform and the read-result
reporting, which are the two sibling family contracts.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-save-image-buffers.md`](CONTRACT-save-image-buffers.md) — the buffers as a family |
| **Sibling** | [`CONTRACT-save-container-transform.md`](CONTRACT-save-container-transform.md) — what happens to the submission buffer's contents |
| **Sibling** | [`CONTRACT-storage-read-completion.md`](CONTRACT-storage-read-completion.md) — what a read reports |
| **Downstream** | `0020E540`, ~~the writer~~ a compiled-out stub, not a writer *(corrected 2026-10-02, OPUS: `0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`, checked at `0020E540`–`0020E576`)* |

## 7. State transitions

~~*live → (capture) staging → (copy, SV-2) submission → (tail-call, SV-6) writer.*~~ *live → (storage queue, kind 8) file* for a manual save; the staging and submission copies serve only the autosave `0057E310` *(corrected 2026-10-02, OPUS: checked at `00581DCA`–`00581DCF` `rdi = 002EF640()`, `00581F27`–`00581F2F` element `+0x28 = rdi`, `+0x30 = 0x56690`, kind 8 at `00581F51`; and `0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`; save-image-buffers-header-and-payload.md §5)*. Separately and off
that path: *live → (copy, SV-2) backup → nothing (SV-4).*

## 8. Script · resource · event interactions

None directly. The payload's contents and the version stamps are the other two pages' subjects.

## 9. Determinism

Fully deterministic. No generator is drawn in any of the seven bodies.

## 10. Failure paths and edge conditions

- ~~The handle from `00236760` is obtained before the copy and its failure handling is not visible in
  this body (SV-6).~~ `00236760` is a one-bit read and cannot fail (SV-6, corrected 2026-09-25 on OPUS block 335).
- Neither copy is bounded by anything but its constant count; there is no size argument to get wrong
  and no partial-copy path.

## 11. Observable behaviour

Saving copies a third of a megabyte twice — once into the submission buffer and once into a backup
nobody reads.

## 12. Reproduction formula

Fill the active buffer with a known pattern, run `002EF570`, and assert **all 353,936 bytes** match —
including the final sixteen, which is what a loop-count-only reading gets wrong. Then assert nothing
but `002EF570` touches `022676C0`.

## 13. Runtime validation

~~**None.** No experiment executes these seven bodies. S-43's runtime cell is not addressed by this
contract. *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*~~ **Superseded 2026-09-25**: OPUS block 335 executed all seven bodies as shipped code
([package](../_index/candidates/s43-opus-replay-save-image-pipeline/README.md)). The evidence class is native
replay, not live.

## 14. Unresolved

- ~~Which callers take the guarded clear `002EF650` and which the unguarded `002EF5F0`.~~ —
  **resolved 2026-09-23 (SWE2-CONTRACT), with an SV-5 correction.** Both clears reach
  `0016D6A0` (`_guard_check_icall`, a bare `ret`) — `002EF5F0` tail-jumps to it, `002EF650`
  calls it — so "only `002EF650` follows with the guard" is wrong. The real difference is that
  `002EF650` is a **clear-then-reinitialise compound**: after the `memset` it runs
  `00253A80` (`SaveRuntime_InitializeHeaderAndImageBackedState`), `002EF2D0` (clears `0x1538`
  bytes at `buffer+0x200`, tail `00379160`) and tail-calls `00238A80` (republishes the
  `base+0x4E68C` pointer). Caller census (whole `.pdata` call/jmp index): the compound is taken
  by `0022B6E0` (the CoreRuntimeScheduling hub, at `0022B78B`) and the two save-header writers
  `00280140` (`0028037B`) and `00394130` (`003941E5`, `003942F2`) — paths that must leave the
  runtime state *valid*, not merely zeroed. The bare clear `002EF5F0` has exactly **one**
  caller: `003601D0` at `00360341`, the teardown/skip-family body that unwinds fades, audio and
  the seven-slot `002EF840` loop before discarding the buffer — it clears without reinitialising
  because nothing downstream is being kept alive.
- ~~Why the backup exists at all, given SV-4. The pages record it as written before a **load**;
  nothing reads it on either path.~~ — **bounded 2026-09-23 (SWE2-CONTRACT): the timing now
  narrows the intent.** The sibling contract's whole-image census (five route forms, decode-
  verified) finds the backup image span has exactly **one** accessor — the writer `002EF570`'s
  own `lea` — and no reader anywhere. The write runs on `0027F5D0`'s load-mode arm immediately
  *before* `SaveLoad_OpenController(ctx+0xD4, 1)`: that is the shape of a restore-on-failure
  snapshot of the live image, but no reader was ever shipped, so the restore half does not
  exist in this build. Intent stays residue — the mechanism and the deadness are closed.
- ~~What the 48 bytes of inter-buffer padding hold, if anything.~~ — **resolved 2026-09-23
  (SWE2-CONTRACT): for the backup buffer the tail is NOT padding** — a live record sits at
  `0x22BDD50` (`backup + 0x56690`), accessed by `002EF840`/`002EF890`/`002EF910`/`002EFA70` and
  a `subsd` reader at `001C3227`; it is the head of whatever follows the buffer array by
  allocation, not slack. The other three tails (`0x21BA910`, `0x2210F90`, `0x2267660`) have
  zero references of any route form — those 48 bytes are dead slack. So the answer is split:
  three tails are padding, the backup's tail is a live record, and `0x566C0`-sized accesses
  against the backup buffer corrupt it.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| SV-1 — spacing and padding | the four addresses differenced; `0x566C0 − 0x56690 = 0x30` | 1 |
| SV-2 — both copies complete | both loops read **past the `jne`**; the tail `movups` pair present in each; `0xACD × 0x80 + 0x10 = 0x56690` | 1 |
| SV-3 — six size sites in two layers | every site loading the immediate `0x56690`, enumerated image-wide | 1 |
| SV-4 — the backup is never read | every rip-relative reference to each of the four buffers, image-wide, **with the active buffer's four as the control** — a sweep that found the backup as quiet as the active one would not be reaching these bodies | 1 |
| SV-5, SV-6 | the two clears and `002EF690`'s tail-call read at their addresses | 1 |
| The header extent and the payload base | [the buffers page](Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md) | 1 |
| `002EF650` is the clear+reinitialise compound (callers `0022B6E0`/`00280140`/`00394130`); `002EF5F0` is the bare clear (sole caller `003601D0`) | whole-`.pdata` call/jmp census 2026-09-23: `002EF650` ← `0022B78B`, `0028037B`, `003941E5`, `003942F2`; `002EF5F0` ← `00360341` only; both bodies decoded — both reach `0016D6A0`, only `002EF650` continues into `00253A80`/`002EF2D0`/`00238A80` | 1 |
| the backup's 48-byte tail holds a live record; the other three tails are dead slack | rip census over `.pdata` bodies 2026-09-23: zero references to `0x21BA910`/`0x2210F90`/`0x2267660`; the `0x22BDD50` record's five accessors per the sibling contract's census | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on SV-1 through SV-6. **SV-2 is the one to test
first**: the natural reading of either copy loop is sixteen bytes short of correct.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Save_Load_Settings — internal.** All seven bodies are this category's own.
- **CoreRuntimeScheduling — MECHANICAL.** The guarded clear `002EF650` is called from that layer;
  ~~which of the two clears a caller takes is SV-5's open question,~~ *(answered: see §14 — resolved 2026-09-23, this caller `0022B6E0` takes the compound clear `002EF650`; 2026-10-02, OPUS)* and that caller is one of the cases
  it is about. *Its address is deliberately not cited: it is a hub whose own callee set spans several
  further layers, none of which this contract says anything about.*
- **ActorEntity, Input, Script_VM_Native_Bridge, WorldAreaField — MECHANICAL.** All four are reached
  through `00236760`, the ~~handle source~~ one-bit selector *(answered: see SV-6; 2026-10-02, OPUS)* SV-6 names, or through the two 8-byte buffer getters. **A
  getter's callers are not this subsystem's relationships** — they are everyone who needs the
  address.
- **Every other layer reached is MECHANICAL** in the same way, through the writer and the CRT
  `memset`. *Their addresses are deliberately not cited: each is a hub, and naming one imports its
  whole edge set for a statement this contract does not make.*

## 17. Related

- [Save image — buffers, header and persistent payload](Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md)
- [The save's version stamps, and what loading normalises](Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
- [The save-image payload — a field map](Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md)

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** §2's sizes, SV-1 to SV-6 and the corrected callers became checks. SV-3's immediate census is function-bounded,
with a raw count of the dword in `.text` as the control. SV-4's reference census ran on both the bounded and the linear
instrument. Script: `Tools/analysis-kit/gfz-scripts/falsify_save_image.py`, output `falsify_save_image.out`, image
`73461d08…`, 0 BROKEN, exit 0. SV-5's reinitialise and SV-6's selector are OPUS block 335's execution; their bytes were
re-read here.

| # | Clause attacked | Result |
|---|---|---|
| G0 | §2 | **survives**: 35 / 50 / 8 / 8 / 8 / 122 / 161 B |
| G1 | SV-1 | **survives**: four buffers `0x566C0` apart against a `0x56690` image, 48 bytes of padding |
| G2 | SV-2 | **survives**: both loops are `0xACD` × (8 loads + 8 stores of 16 B), each followed by a 16-byte tail; `0xACD × 0x80 + 0x10 = 0x56690` |
| G3 | SV-3 | **survives**: exactly six `mov`-immediate sites, and the dword occurs exactly six times in `.text` |
| G4 | SV-4 | **survives**: references 4 / 2 / 3 / 1 on both instruments; the backup's one is `002EF570`'s own `lea` |
| G5 | SV-5 | **survives**: the bare clear tail-jumps to `0016D6A0`; the compound calls it, then `00253A80` and `002EF2D0`, and tail-jumps to `00238A80`. Compound callers `0022B6E0`, `00280140`, `00394130` (twice); the bare clear only from `003601D0` |
| G6 | SV-6 | **survives**: the one-bit selector (`00236760`, five instructions) is read before the copy; the tail-call passes the bit, `02211000` and `0x56690` |

No correction.

## Cross-subsystem neighbours — pass 22 (FABLE, 2026-09-29)

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page. §16a states classes under a numbered heading, which the crossings gate does not read; this section names the edges.*

**ActorEntity — CLIENT, SERVICE (3 edges).** `BattleUnit_TeardownAndDespawn` (`00300E40`) calls the selector `00236760`; `ActorManager_RunFieldRuntimePass` (`0025D9E0`) calls `002EFA70`, the entry starter of the seven-slot table that sits just past the backup buffer (§14); and the teardown body `003601D0` calls the slot-block getter `00263FF0`. The selector is a one-bit read any body can make, and the table past the backup is used by the field pass; neither touches a save buffer, so neither bears on SV-1 to SV-6.

**Audio — SERVICE (9 edges).** The teardown body `003601D0` - the only caller of the bare clear (SV-5) - calls `002DF060`, `002DF0F0`, `002DF370` (the group-mask setter), `00360D70`, `00362850`, `003633B0`, `003636A0`, `00363750` and `00363E40`. That body unwinds audio state before it discards the active buffer; the audio calls are part of the teardown, and the contract's claim about it is only which clear it takes.

**CoreRuntimeScheduling — CLIENT, SERVICE (5 edges).** The frame dispatcher `0022A580` calls `0022B6E0`, which calls the compound clear `SaveRuntime_ResetActiveImageAndRebindState` (`002EF650`); `003601D0` calls `00229EE0` and `00229EF0`; and `00394130` calls `001EDEC0`. `0022B6E0` - the mode-0 boot frame - is the scheduling-layer caller SV-5 names for the clear-then-reinitialise compound; the other two are scheduling helpers called on the teardown and header-writer paths.

**Gameplay — SERVICE (1 edge).** `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`), the compound's tail, calls `BattleSystem_ResetRuntimeState` (`00237DF0`). Re-initialising the active image resets the battle system's runtime state as part of the rebind; the reset itself belongs to the battle pages.

**Input — SERVICE, CLIENT (4 edges).** `0022B6E0` calls `00249C30` (the conditional input republication) and `InputControl_SetOneShotFrameCallback` (`0035E9A0`); the load path `0027F5D0` calls `002D66A0`; and the arbiter `InputGameplay_ArbitrateDigitalInputAndModalState` (`00253C70`) calls the selector `00236760`. The boot frame that resets the image also runs the conditional input-snapshot republication and sets a one-shot input frame callback, and the arbiter reads the same one-bit selector the writer receives (SV-6); the save buffers are not involved in either.

**Items_Equipment_Shops_License — SERVICE (1 edge).** `SaveRuntime_RebindImageBackedGameplayState` (`00238A80`) calls `InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState` (`0030B6A0`). The inventory's class descriptors point into the image, so the rebind rebases them after the active buffer is re-initialised; that is the image-backed-pointer part of SV-5's compound.

**Presentation — SERVICE (5 edges).** `0022B6E0` calls `00252A20`, `002E65A0`, `0036D400`, `GraphicsSync_ClearSharedCommandStateBits` (`0036F2C0`) and `GraphicsSync_WaitBackendState100ClearAndResetSharedState` (`0036F2F0`). The boot frame that takes the compound clear also synchronises and resets render state; this contract's claim about it is only the clear it calls.

**RNG_Random_Selection — SERVICE (1 edge).** `0022B6E0` calls `RNG_MT19937_NextU32_Thunk` (`00379CD0`). The boot frame draws one random number on its path; no save buffer depends on it.

**Resource — SERVICE (5 edges).** `0022B6E0` and `003601D0` call `0032E520`; the load path `0027F5D0` calls `0024A5A0`; the header writer `00280140` calls `0032E4D0`; and `002EF910` calls `001D6C80`. These are resource-layer calls on the reset, teardown, load and header-writing paths and in the table poll; the contract's buffers are copied and cleared without them.

**Script_VM_Native_Bridge — CLIENT (10 edges).** Script verbs call the table past the backup buffer - `003559B0`, `00355EB0`, `00356270`, `00356650`, `00356A50` and `00356FE0` call the entry starter `002EFA70`, `00349B30` and `0034A050` call the one-slot release `002EF840`, and `00355350` calls the all-slots release `002EF890` - and `0050F540` calls the selector `00236760`. Scripts start and release entries in the seven-slot table §14 found living in the backup buffer's tail, which is why `0x566C0`-sized accesses against the backup would corrupt it; the table's purpose is not named here.

**Story_Event_Quest_Hunt — SERVICE (2 edges).** `002EF2D0`, the compound's second step, tail-calls `PersistentFlag_ApplyAuthoredInitialPrimarySet` (`00379160`), which calls `PersistentFlag_SetPrimary` (`0032AB60`). After clearing `0x1538` payload bytes the compound restores the authored initial story flags into the fresh image; the flag values are the story pages' matter.

**UI — SERVICE, CLIENT (2 edges).** The load path `0027F5D0` calls `0028E790`, and `0027EFA0` (on the game-over route) calls the entry starter `002EFA70`. A UI body runs on the load path that writes the backup (§14), and the game-over route starts an entry in the table past it; neither changes how the buffers are copied.

**World — CLIENT (1 edge).** `00266D10` calls `002EF2D0`. A world-layer body runs the payload clear and initial-flag restore directly, outside the compound.

**WorldAreaField — SERVICE, CLIENT (21 edges).** The two header writers call the transition layer - `00280140` and `00394130` call `WorldTransition_RequeueCurrentFieldForRestore` (`00267C90`), `WorldPersistence_ResetBanksAndMarkInitializationState` (`00268320`) and `WorldTransition_RequestFieldTransition` (`00314440`), and `00394130` also `WorldTransition_SetActiveOrPendingFieldId` (`00314DC0`); `0022B6E0` calls `003318C0` and `003601D0` calls `00331920`; the transition bodies read the buffers - `WorldTransitionSnapshot_CaptureRuntimeState` (`00229B40`) and `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot` (`00584580`) call the capture getter `002EF620`, and `00229B40`, `WorldTransition_StageFieldTransition` (`003145E0`) and `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot` (`005843E0`) call the active getter `002EF640`; `003145E0`, `005843E0` and `00584580` call the selector `00236760`; `WorldTransition_RequestFieldTransition`, `WorldTransition_RequeueCurrentFieldForRestore` (`00314530`) and `003145E0` call `002EFA70`; and the tick `00314020` calls the table poll `002EF910`. Loading a save requeues the field and requests a transition, and field transitions capture and restore persistence through the active and capture buffers this contract owns; the transition logic is the world pages', the buffer addresses and copies are this contract's.

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../_index/candidates/fable-contract-save-image-pipeline-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002DF060` | 8 B | sets `ecx` to -1 and tail-jumps to `001DBE40(-1)` | `002DF063` |
| `002EF890` | 120 B | for `i` = 0 to 6 (the index clamped to 0..6 by a signed test and `cmovg`), reads dword `+0` of the 0x30-byte entry `i` of the table at `022BDD60` and, when it is non-zero, calls `0024CFF0` with it and then zeroes that dword and byte `+4` of the entry; returns nothing | `002EF8C4`, `002EF8D0`, `002EF8D8`, `002EF8DD`, `002EF8E1` |
| `00349B30` | 40 B | takes `e` = `00267E10(r9)`, calls `0017DB70(00D10C20)` and tail-jumps to `002EF840(e)` | `00349B39`, `00349B47`, `00349B53` |
| `0034A050` | 53 B | calls `00267F90(r9, 0)`, takes `e` = `00267E10(r9)`, calls `0017DB70(00D10C20)` and tail-jumps to `002EF840(e)` | `0034A05E`, `0034A066`, `0034A074`, `0034A080` |
| `003633B0` | 88 B | when `ecx` is non-zero, calls `00363840()` unless unsigned byte `022CBB2D` already equals `ecx`, and stores `cl` to byte `022CBB2D`; when `ecx` is 0, calls `002DF0F0(0)` if dword `022CBA70` or dword `022CBA7C` is non-zero, then zeroes dword `022CBA70` and byte `022CBB2D` | `003633C3`, `003633C7`, `003633CC`, `003633ED`, `003633F2` |
