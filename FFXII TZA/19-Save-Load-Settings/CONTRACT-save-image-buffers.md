---
contract: hold the save image in four fixed buffers and move it between them
category: 19-Save-Load-Settings
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md
entries: ["002EF5F0", "002EF640", "002EF690"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 45 addresses cited - 7 data, 19 entry, 19 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-save-image-buffers-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the save image buffers

Four buffers of identical size, evenly spaced in `.data`, and the operations that clear one and move
one to another. Everything a saved game contains lives in these, and a reconstruction that gets the
size or the spacing wrong produces files the original cannot read.

## 1. Purpose

The save image is a single flat block. One copy is live while you play~~, one is the snapshot taken~~
~~when you save, one is what gets handed to the file write,~~ and is the one a manual save writes; one is the autosave's snapshot and one what the autosave `0057E310` hands to the storage machine *(corrected 2026-10-02, OPUS: checked at `00581DCA`–`00581DCF` and `00581F27`–`00581F2F`, the manual save's element `+0x28` is `002EF640()`, the active buffer)*; and one is a backup. Nothing here parses the
image — these operations move it whole.

## 2. Interface

| | |
|---|---|
| `002EF5F0` | `SaveImage_ClearActiveRuntimeBuffer` (35 B) — no parameters, no return |
| `002EF640` | `SaveImage_GetActiveRuntimeBuffer` (8 B) — returns the active buffer; two instructions, `lea rax, [rip+…]` / `ret` |
| `002EF690` | `SaveImage_CopyCaptureToWriteSubmissionBuffer` (161 B) — no parameters |
| calling convention | Microsoft x64 |

## 3. The four buffers

| role | address | evidence |
|---|---|---|
| active runtime | `0x02164280` | `002EF5F6 lea rcx, [rip + 0x1e74c83]` and the getter's `002EF640 lea rax, [rip + 0x1e74c39]`, both resolving here |
| capture staging | `0x021BA940` | the copy's source, `002EF6A4 lea rcx, [rip + 0x1ecb295]` |
| write submission | `0x02211000` | the copy's destination, `002EF69D lea r8, [rip + 0x1f2195c]` |
| backup | `0x022676C0` | written by one function ~~nothing calls~~ called through the thunk `00584490` at `0027F974` on load-mode opens *(answered: see §10 item 3, THE WRITER HAS A CALLER; 2026-10-02, OPUS)* and read by nothing (`V-6`) |

**The spacing is exactly `0x566C0` between consecutive buffers**, and the image is `0x56690` — 48
bytes smaller. The buffers are padded, not packed, and **the padding is not part of the image**: a
reconstruction that writes `0x566C0` bytes overruns into the next buffer.

## 4. The image size stands on three independent witnesses

1. **A literal in the clear.** `002EF5FD mov r8d, 0x56690` as the fill length.
2. **The copy loop's arithmetic.** `002EF6AB mov r9d, 0xACD` counts iterations; each body moves eight
   `movups` pairs — 128 bytes — and after the loop a single 16-byte `movups` tail runs
   (`002EF70C`/`002EF70F`). `0xACD × 0x80 + 0x10 = 0x56690` exactly.
3. The second literal site the source page records.

None of the three is derived from the others, and the second is arithmetic over a loop bound rather
than a stated constant, which is what makes it independent rather than a restatement.

## 5. The copy is inlined, not a call

`SaveImage_CopyCaptureToWriteSubmissionBuffer` does **not** call a memory-copy routine. It carries its
own unrolled SIMD loop: eight source/destination `movups` pairs per iteration at a stride of `0x80`,
`sub r9, 1 / jne`, then the tail. A reimplementation may of course use `memcpy` — the observable
result is identical — but anything reasoning about the *call graph* of the save path must know that
no copy callee appears in it.

## 6. Preconditions · postconditions · invariants

**Preconditions.** None. All three operations address fixed globals and take no arguments; none
validates anything, because there is nothing to validate.

**Postconditions.** The clear leaves `0x56690` zero bytes at `0x02164280` and then tail-jumps to
`0016D6A0` with `ecx = 0` — which is `_guard_check_icall`, a bare `ret` in this build, so the tail-jump is simply a return and nothing happens there. The copy leaves the write submission buffer byte-identical to the capture
staging buffer over `0x56690` bytes. The getter has no effect.

**Invariant.** The three operations never touch the 48 bytes between images.

## 7. State

| | what | evidence |
|---|---|---|
| read | `0x021BA940` for `0x56690` bytes | `002EF6A4`, the loop |
| written | `0x02164280` (clear) and `0x02211000` (copy), `0x56690` bytes each | `002EF5FD`, `002EF69D` |
| allocated / deallocated | none — all four buffers are static `.data` | |

**No destructor can exist** for any of them.

## 8. Relationships

The clear tail-jumps to `0016D6A0` (`_guard_check_icall`, a bare `ret`) rather than returning normally, so it is the last thing on its own path and the jump has no effect of its own. It reaches the CRT `memset` through the import thunk at `00861EC0`.

**CORRECTED 2026-09-12 (`OPUS-SAVEIMG-ISOLATED`): this section said the family "otherwise calls
nothing", and that is wrong by two calls.** Reading `002EF690` end to end, the copy:

1. calls `00236760` and keeps the result in `ebx` across the move;
2. runs its own unrolled loop (§5 — no copy callee);
3. calls `0020E4E0` at `002EF713`, after the loop;
4. **tail-jumps to `0020E540`** at `002EF72C` with `ecx = ebx`, `rdx = 0x02211000` and
   `r8d = 0x56690`.

~~Step 4 is the write submission, and it is the *point* of the operation: the copy does not merely~~
~~stage the image, it hands it on. A reader who took this section at its word would build a~~
~~reconstruction that fills a buffer nobody collects.~~ Step 4 reaches no file: `0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`, so the submission buffer this copy fills is collected by nothing *(corrected 2026-10-02, OPUS: checked at `002EF72C` and `0020E540`–`0020E576`; only `0057E310` and `00581DA0` reach the storage machine — save-image-buffers-header-and-payload.md §5)*.

## 9. Determinism

Fully deterministic, no RNG, no timing, no synchronisation. The buffers are global and nothing here
locks them, so the family assumes the save path is not concurrent with play on another thread.

## 10. Failure paths and edge conditions

1. **There are none inside the family.** No operation can fail, return an error, or refuse: three
   fixed addresses and two fixed lengths.
2. **The 48-byte gap is the only edge that matters**, and it is an edge for the *caller*: writing
   `0x566C0` rather than `0x56690` silently corrupts the next buffer, and reading `0x566C0` picks up
   48 bytes that belong to nothing.
3. ~~The backup buffer at `0x022676C0` is written by a function with no callers~~ **— THE WRITER HAS A
   CALLER, and this contract said otherwise.** It is reached through the thunk `00584490`
   (`jmp 002EF570`), called at `0027F974` by the save controller's state handler `0027F5D0`, on the
   arm with a non-zero controller id and immediately before `SaveLoad_OpenController(ctx+0xD4, 1)`.
   The thunk is why the caller graph missed it, and a raw `E8`/`E9` index that does not depend on the
   function list is what found it.

   **What survives, and it is the half that matters:** the buffer is still **read by nothing**, so it
   is dead storage and a reimplementation that omits the write remains unobservable. But the write
   **runs on every load-mode open** — the `0027F5D0` arm's non-zero controller id opens the
   controller in load mode (`SaveLoad_OpenController(ctx+0xD4, 1)`) immediately after the copy —
   so one that reproduces it must do so AT THAT POINT rather than wherever convenient. *(Corrected
   2026-09-23, SWE2-CONTRACT: this line previously read "runs on every save"; the arm the thunk is
   invoked from is the load-mode arm, per the owning page's request-6 reading.)* Folded from
   FABLE's V-6 note by OPUS 2026-09-13.

   > **"No callers" and "no readers" failed independently here, and only one of them failed.** A
   > caller-graph negative is a statement about the function list; a rip-sweep negative is a
   > statement about the image. This contract had them in one sentence and they are not the same
   > kind of claim.
   > *Corrected 2026-09-12 (FABLE, V-6). **FOLDED BY OPUS 2026-09-13**; the item above carries it.* The writer
   > **has** a caller: the thunk `00584490` (`jmp 002EF570`) is called at `0027F974` by the save
   > controller's state handler `0027F5D0`, on the arm with a non-zero controller id, immediately
   > before `SaveLoad_OpenController(ctx+0xD4, 1)`. The buffer is still read by nothing (rip sweep),
   > so "dead storage" holds, but the write runs on ~~every save~~ every load-mode open *(corrected 2026-10-02, OPUS: §10 item 3's correction of 2026-09-23 — `0027F8DB`–`0027F984`, the arm that opens the controller in load mode)* — a reimplementation that omits it
   > is still unobservable, one that reproduces it must do so at that point. Found by a raw
   > `E8`/`E9` index that does not depend on the function list.

## 11. Observable behaviour

In memory: after the clear, `0x56690` zero bytes at `0x02164280` with the 48 bytes before
`0x021BA940` untouched. After the copy, the two ranges compare equal. In a file: the written image is
`0x56690` bytes, header first.

## 12. Reproduction formula

```
IMAGE   = 0x56690        /* 353,936 */
SPACING = 0x566C0        /* 353,984 - the image plus 48 bytes of padding */
active = 0x02164280; capture = active + SPACING;
submit = capture + SPACING; backup = submit + SPACING;

clear()  : memset(active, 0, IMAGE)
getActive(): return active
copy()   : bit = selectorBit()          /* 00236760, read BEFORE the move and held in ebx */
           memcpy(submit, capture, IMAGE)
           beforeSubmit()               /* 0020E4E0 */
           return submitWrite(bit, submit, IMAGE)   /* 0020E540, a TAIL JUMP */   <- corrected 2026-10-02, OPUS: 0020E540 is a stub (call 001C18E0; jmp 0016D6A0 = ret 0); nothing is written
```

**The last three lines were missing until 2026-09-12** — the formula read `copy(): memcpy(submit,
capture, IMAGE)` and stopped. See §8. The ordering is load-bearing and not an implementation
detail: the bit is read *first* and survives the copy in a callee-saved register, so it is an input
to this operation rather than something the submit callee could fetch for itself. A reconstruction
that reads it afterwards is indistinguishable here and wrong the moment the copy can change what
the global says.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent *for these three bodies*.**
(2026-09-12; amended 2026-09-13 — `EXP-080` reads this family's buffers in a live process without
executing, tracing or measuring any of them. See the review at the end of this section.)

All three bodies have been executed at their real virtual addresses under Unicorn against an
independent reconstruction. Nothing has run in a live process, which is what still holds
`RUNTIME VALIDATED` open, and §11 remains the description of what a live read would show.

**The buffers are mapped where the shipped code's `lea`s actually resolve** — `0x02164280` and three
more at `0x566C0` — because these operations reach their data through no argument at all. Planting
them anywhere else would not be running this code.

**Instrument:** [`Reconstruction/Tests/Differential/diff_save_image.py`](../../../Reconstruction/Tests/Differential/diff_save_image.py)
against [`Reconstruction/Game/SaveLoad/save_image.c`](../../../Reconstruction/Game/SaveLoad/save_image.c).

**Result: 72 commands, 53 compared lines, 0 mismatches** — 17 distinct image digests out of 25,
**19 distinct padding images out of 19**, and 4 of 7 traces carrying the submit call.

### Two claims are carried by execution rather than by reading

- **`0016D6A0` is a bare return.** That page is mapped from the image and the address is *run*, not
  hooked. A body that was not `ret 0` would not come back. This closes §14.3, which had been standing
  next to its own answer in §6 since the contract was written.
- **`00236760` returns a bit, and the bit is real.** Its three instructions execute over a planted
  global, so the selector reaching the submit callee is genuinely
  `[[0x02EBF190]+4] >> 0xC & 1` and not a number the harness chose. Driven at both values; the
  reconstruction takes it from an oracle and the two agree, which is what makes the extraction
  itself evidence. This closes §14.2.

Only three things are answered rather than run: the CRT `memset` thunk, whose import slot is empty
in the file, and the two callees after the copy, whose bodies reach far outside this subsystem.

### The 48 bytes, checked from both directions

This suite exists for one hazard: `IMAGE` is 48 bytes shorter than `SPACING`, and a reimplementation
that moves `SPACING` is **byte-identical over every byte a digest would look at**. So the padding
behind each buffer is compared as its own line, and both directions were exercised:

1. **A deliberate positive control.** The reconstruction's tail was temporarily changed to move
   `SI_TAIL + SI_PAD`, which is exactly the overrun §10.2 warns about. The suite failed on three
   `PAD` lines — the padding of the submit buffer after each copy — and passed again when reverted,
   with the reverted file verified byte-identical to its backup.
2. **Mechanically, by mutation.** `SI_SPACING 0x566C0 → 0x566C1` was **KILLED**.

**A false pass, and what caused it.** The first attempt at control 1 reported `RESULT: OK` on a
reconstruction that was provably overrunning. The build had failed silently and the harness ran a
**stale executable**; the build output had been discarded. The control was only believed once the
compile was watched and the binary's timestamp checked. *A test result is a statement about the
binary that ran, not about the file on disk, and the two are the same only when something checks.*

### How far the instrument itself has been tested

**15 mutants: 6 KILLED · 3 EQUIVALENT · 1 SURVIVED · 5 NO_BUILD · 0 TIMEOUT · 0 INVALID.**
Production inputs verified stable. **No unexplained survivor.**

| outcome | mutation | reading |
|---|---|---|
| SURVIVED | `SI_BUFFERS 4 → 5` | **Equivalent, and the reason is a fact about the subsystem:** no operation in this family has any notion of *how many* buffers exist. The clear touches one, the copy touches two, the getter returns one, and every address is a fixed global. The count of four belongs to the layout page, not to these three bodies. |
| EQUIVALENT | `SI_BACKUP 3 → 4` | Same root cause — the backup buffer is dead storage (§10.3) and nothing here names it. Proven byte-identical. |
| EQUIVALENT ×2 | the size check's `? 1 : -1` | A dummy array bound; proven byte-identical. |
| NO_BUILD ×5 | `SI_IMAGE`, `SI_LOOP_COUNT`, `SI_BLOCK`, `SI_TAIL`, and the check's own `==` | `si_size_check` asserts `0xACD × 0x80 + 0x10 == 0x56690`. Break any term and the translation unit refuses to compile. |

**The NO_BUILDs are why control 1 had to exist.** The image *geometry* cannot be built wrong — which
also means no test ever has to catch a wrong geometry, so the suite's ability to detect an overrun
was never demonstrated by those five mutants. The manual control breaks the invariant a different
way, keeping `0xACD × 0x80 + 0x10 == 0x56690` intact while writing 48 bytes past the image, and that
is the case the padding comparison exists for. *A compile-time guard and a test do not cover the same
thing, and a campaign full of NO_BUILDs can look like strength while hiding an untested detector.*

### The first campaign was measured over the wrong surface

The first run produced **five** mutants for a subsystem whose entire content is constants. The cause
was in the generator, not in this pilot: `mutation_test.py`'s literal pattern ended
`(?![A-Za-z0-9_])` immediately after the digits, so a constant written `0x56690u` **did not match at
all** — the `u` is a word character. Every literal carrying a `u`, `U`, `l`, `L` or `f` suffix was
invisible, silently, in every pilot: **221 of them across the reconstructions**, and re-measuring
after the fix raises the literal mutation surface from **452 to 548 points across 16 pilots**
(`rng_generators` +21, `widget_construct` +11, this pilot +10).

**Every campaign run before 2026-09-12 therefore measured a surface smaller than its file's, and its
counts are a floor rather than a total.** The other pilots are not re-run here — that is separate
work and is filed as such — but no earlier campaign number should be read as complete.

### What is still owed, and it is live-only

1. **What the selector bit selects** inside `0020E540` — the family reads it and passes it on, and
   nothing here can say what it means.
2. **Whether the backup buffer is ever written in a running game**, which would contradict `V-6`.
3. **That a written save file is `0x56690` bytes**, which is the one end-to-end check that would tie
   this family to the thing a player sees.

Queued; the live-automation pause stands.

### The first live capture that touches this family — reviewed, and what it does *not* do 2026-09-13 (OPUS, `ASTRA-REQ-OPUS-OLD-SAVE-LIVE-REVIEW`)

**`EXP-080` is a live process, so the line above — “Live capture: still absent” — is no longer true
of the *family*. It remains true of these three bodies.** Nothing in `EXP-080` executes `002EF5F0`,
`002EF640` or `002EF690`, traces a call into them, or measures a buffer's size; it reads the active
image at `02164280` and the block at `+0x4E68C` from outside. `RUNTIME VALIDATED` stays closed.

**I re-derived its three static controls from my own copy of the image rather than accepting them,
and all three reproduce exactly:**

| control | `EXP-080` | re-derived here |
|---|---|---|
| live `.text` equals disk, 7,996,981 B, SHA-256 `5421e8b2…` | asserted | **identical** — and the count is `.text`'s **virtual** size `0x7A0635`, not its raw size `0x7A0800`; the 459-byte difference is file-alignment padding that is never mapped. The record does not say which extent it used, and the number only checks out under one of them |
| known-byte `01CCD300` = `19930d0a1a0a` | asserted | **identical** |
| clock helper `0032A160`, 11 bytes, SHA-256 `341fefc9…` | asserted | **identical**: `c705f232d60100000000 c3` = `mov dword ptr [rip+0x1D632F2], 0` ; `ret`, and the target resolves to `0208D45C` |

The reference process's executable SHA-256 `73461d08…` is this contract's own `verified_against`
value, so the live process and every static claim on this page are the same binary.

**One wording correction, in this contract's own idiom.** The evidence calls `0032A160` “a
conditional native reset path”. The *body* is unconditional and so is its call site:
`BattleSystem_ResetRuntimeState` (`00237DF0`) is **branch-free from its loop exit to its `ret`**, so
`0032A160` runs whenever that function runs — and `0032A160` has **exactly one caller in the whole
image**. The conditionality is entirely in whether `00237DF0` is reached, which `EXP-080` correctly
does not claim. *(`00237DF0` is reached statically from `00233C10`, one of the three addresses the
record lists as untraced — naming the edge is not observing it, and the chronology stays open.)*

~~**One control ASTRA had in hand and did not claim**~~ — **RETRACTED and narrowed 2026-09-13
(`ASTRA-CONTRA-OPUS-EXP080-SNAPSHOT-BOUNDS`, upheld in full).** What the captures support:

- the bound block's digest `d48734d6…` is **equal at all four sampled instants** of Load complete and
  Southgate, and the restored contents were **already present at the pre-dismissal sample**;
- the sampled raw tick reads `0` in all four bracket reads of fresh title and Load complete.

**What I wrote instead was an interval claim, and four point samples cannot carry one.** The original
text said *“everything the load did to the bound block was already done before the popup was dismissed,
and nothing touched it afterwards”*, and called both states *“quiescent”*. ASTRA's re-read gives the
numbers that refuse it: roughly **46 seconds** separate the last Load-complete read
(`…849.598`) from the first Southgate read (`…895.760`). Equal digests at four instants exclude **net**
change at those instants — not a same-value rewrite, not a change reverted before the next sample, not
a write outside the sampled schedule. And a **stopped sampled field clock is a fact about that counter**,
not evidence that every writer is stopped.

> **This is the third time today I have met this failure class and the first time I produced it.**
> I flagged it in `FRP-4` (then `FP-4`) (a census's silence is the filter's property), upheld ASTRA's version of it in
> the config gate (an exact-destination census cannot see covering writes) — and then read an absence
> of observed change as an absence of writes. **A snapshot bounds what was true when it was taken.**

The bounded finding stands and is the one worth propagating: **the restored state was present before the
popup was dismissed.** No chronology, no absence of writes, and nothing here is *“stronger than”* the
record's own statement — it is a different and weaker kind of claim than I dressed it as.

**One raw fact in the reviewer's own output that neither the record nor the re-derivation mentions.**
The changed span begins at block `+0x4` because **the block's flag word at `+0x4` changes `0x40` →
`0x17F`** across the load — bit 6 alone before, bits 0–6 and 8 after, with bit 12 (`restart`, the
only bit the [field map](../11-Party/Battle-State-Block/the-battle-state-block-field-map.md)
names at that offset) clear in both. Eight observed bits at a documented offset with one documented
meaning. Routed to FABLE as `OPUS-REQ-FABLE-BLOCKFLAGS-0X4` rather than written into a page whose
`§2.9` was re-derived the same day.

**Not closed by this review, and deliberately:** same-session current-to-old reuse, nonzero keep-bank
behaviour (both banks were all-zero in all six samples, so preservation, copy, swap and wipe are
indistinguishable), enemy respawn, loaded gambit/inventory presentation, and the native call
chronology. The three items under *“What is still owed”* above are untouched — in particular
**no written save file was measured**, which is still the end-to-end check this family lacks.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-057`](../_experiments/EXP-057-save-checksum-controls.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

1. ~~**Why the backup buffer exists**, given that nothing calls its writer and nothing reads it (`V-6`).~~
   **BOUNDED 2026-09-23 (SWE2-CONTRACT): the mechanism is closed; only intent remains.**
   A raw disp32 scan over **all** of `.text` — not just `.pdata` bodies, which is the blind spot
   that hid the writer — decode-verifies exactly **one** accessor into the image span
   `[0x22676C0, 0x22BDD50)`: the writer's own `lea rcx, [rip→0x22676C0]` at `002EF570`. No reader
   exists by any route form (rip operands, immediates, data qwords; the image-base+RVA disp32
   form is also negative — zero `0x21476C0` bytes in `.text`). So the buffer is dead storage
   written once per **load** — the save-controller state handler `0027F5D0` runs it on the
   non-zero-controller-id arm, immediately before `SaveLoad_OpenController(ctx+0xD4, 1)` opens
   the controller in load mode (`0027F974` → thunk `00584490` → `002EF570`, active→backup copy,
   0x56690 B) — diagnostic/vestigial class, same shape as the `02099DB0` weather global. The
   timing narrows the intent: a snapshot taken immediately before a load overwrites the active
   image is the shape of a restore-on-failure backup — but no reader exists, so the restore half
   was never shipped. Intent remains residue; the mechanism is closed.
   **Side finding:** the 48-byte stride tail is not dead space — a small live record sits at
   `0x22BDD50` (the backup buffer's `+0x56690`), accessed by `002EF840`/`002EF890`/`002EF910`/
   `002EFA70` bodies and a `subsd` reader at `001C3227`. §3's warning gains a second reason:
   writing `0x566C0` corrupts that record, not just "the next buffer".
2. ~~What `00236760` returns and why the copy keeps it across the move.~~ **ANSWERED 2026-09-12.**
   It returns a **single bit**, not a handle: `mov rax, [0x02EBF190]` / `mov eax, [rax+4]` /
   `shr eax, 0xC` / `and eax, 1`. The copy keeps it because it becomes the **first argument to the
   submit callee** at `002EF725 mov ecx, ebx`. ~~What the bit *selects* inside `0020E540` is outside~~
   ~~this family and stays open.~~ *(answered: nothing — `0020E540` is `call 001C18E0` then `jmp 0016D6A0`, and `0016D6A0` is `ret 0`, checked at `0020E540`–`0020E576`; 2026-10-02, OPUS)*
3. ~~What the clear's tail-jump to `0016D6A0` does with `ecx = 0`.~~ **ANSWERED — and it was already
   answered in §6 when this question was written.** `0016D6A0` is `ret 0`. The harness maps that
   address from the image and **executes it** rather than hooking it, so the claim is now carried by
   a run and not only by a reading: a body that was not a bare return would not come back.
   *A question left standing beside its own answer is a defect of the same kind as a wrong answer.*

## 15. Evidence

The claim column is the wording `diff_save_image.py`'s `CONTRACT_MAP` carries, and
`parity_status.py` compares the two every time it runs, so an edit here that the harness does not
follow is reported rather than absorbed.

| claim | evidence | tier | confidence |
|---|---|---|---|
| The image is 0x56690 bytes | four independent witnesses: the literal at `002EF5FD`; the loop's arithmetic `0xACD × 0x80 + 0x10`; the second literal at `002EF718`; and `SaveImageHeader` 0x200 + `SavePayload` 0x56490. Executed — a distinct pattern moved and compared byte for byte | 1 (isolated original-code) | PROVEN |
| The buffers are 0x566C0 apart | the differences between `002EF5F6`, `002EF6A4`, `002EF69D` and the backup writer's address. Executed — all four addressed at that stride and digested independently | 1 (isolated original-code) | PROVEN |
| The 48 bytes between images are never touched | `0x566C0 − 0x56690`. Executed — the padding behind every buffer compared as its own line, 19 of 19 distinct, with a deliberate positive control below | 1 (isolated original-code) | PROVEN |
| The clear writes 0x56690 zero bytes to the active buffer | `002EF5F6` `lea rcx` / `002EF5FD mov r8d, 0x56690` / `002EF603 call 00861EC0`. Executed | 1 (isolated original-code) | PROVEN |
| The getter returns the active buffer | `002EF640`–`002EF647`, two instructions. Executed — the returned pointer compared as an offset | 1 (isolated original-code) | PROVEN |
| The copy is inlined, with no copy callee | `002EF6B1`–`002EF70A` is the whole loop and contains no call. Executed — the trace lists every call the body makes and no copy routine appears | 1 (isolated original-code) | PROVEN |
| The copy reads the selector bit first and holds it across the copy | `002EF696 call 00236760` / `002EF69B mov ebx, eax`, used at `002EF725`. Executed — `00236760` runs for real over a planted global at both bit values | 1 (isolated original-code) | PROVEN |
| The copy hands the submit callee the buffer and 0x56690 | `002EF718 mov r8d, 0x56690` / `002EF71E lea rdx` → `0x02211000` / `002EF725 mov ecx, ebx` / `002EF72C jmp 0020E540`. Executed — the three arguments compared | 1 (isolated original-code) | PROVEN |
| The clear's tail jump to 0016D6A0 is a bare return | `0016D6A0` is `ret 0`. Executed — that address is mapped from the image and RUN, not hooked | 1 (isolated original-code) | PROVEN |
| the backup buffer's image span has exactly one accessor (its writer `002EF570`); no reader exists by any route form, and the `+0x56690` stride tail holds a live record | raw disp32 scan over all of `.text`, decode-verified (covers non-`.pdata` bodies — the blind spot that hid `002EF570`): one `lea rcx, [rip→0x22676C0]` at `002EF570`, zero readers; written on the load-mode arm of `0027F5D0`, not per save; image-base-relative form also negative (zero `0x21476C0` RVA bytes in `.text`); `0x22BDD50` record accessed by `002EF840`/`002EF890`/`002EF910`/`002EFA70` and `001C3227` | 1 (static) | PROVEN |
| any runtime observation | — | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every number in this contract is either an instruction operand or an arithmetic identity, so every
one was recomputed rather than read.

| claim | recomputed |
|---|---|
| the image is `0x56690` bytes | `0xACD × 0x80 + 0x10 = ` **`0x56690`** — the loop's own arithmetic, and `002EF5FD mov r8d, 0x56690` is the literal beside it |
| the buffers are `0x566C0` apart | see below — **a fourth witness** |
| the 48 bytes between images are never touched | `0x566C0 − 0x56690 = 0x30 = ` **48** |
| the clear writes `0x56690` zeros to the active buffer | `002EF5F6 lea rcx, [rip → 02164280]` / `002EF5FD mov r8d, 0x56690` / `002EF603 call 00861EC0` |
| the getter returns the active buffer | `002EF640 lea rax, [rip → 02164280]` / `002EF647 ret` — **two instructions, and the same address the clear zeroes** |
| the submit takes the buffer and `0x56690` | `002EF718 mov r8d, 0x56690` / `002EF71E lea rdx, [rip → 02211000]` |
| the copy is inlined, with no copy callee | `002EF6B1`–`002EF70A` is **20 instructions and 0 calls** |
| the clear's tail jump target is a bare return | `0016D6A0` is `ret 0` |

### A fourth witness for the `0x566C0` stride, from the submit's own operand

The clear and the getter name `02164280`; the submit names `02211000`. The difference is

```
02211000 − 02164280 = 0xACD80 = 2 × 0x566C0
```

**exactly two strides** — so the stride is confirmed a fourth way, by an operand the stride claim
never cites, in a function that is doing something else entirely. Three buffer slots therefore sit at
`02164280`, `021BA940` and `02211000`.

### `0016D6A0` again

That the clear tail-jumps into `ret 0` is the **same three bytes** — `C2 00 00` — this sweep read in
[the verb dispatch ABI](../01-Script-VM-Native-Bridge/Verb-Dispatch/CONTRACT-verb-dispatch-abi.md),
where the same address stands in for an absent callback in every dispatch table. **One three-byte
stub serves as both a no-op callback and a no-op tail across unrelated subsystems** — worth knowing
before a reconstruction gives either use its own stub.

**Not claimed:** nothing here is a runtime observation; §15's `UNKNOWN` row stands.

## 16. Parity plan

`SERIALIZATION` — write an image and compare its length against `0x56690` exactly.
`STRUCTURAL` — after a clear, assert the 48 bytes before the next buffer are unchanged.
`CONTRACT` — after a capture, assert the staging and submission ranges compare equal over `0x56690`
and differ nowhere.

**All three are done offline** — see §13. `CALCULATION`, `STRUCTURAL`, `STATE-TRANSITION`,
`SERIALIZATION`, `CONTRACT` and `EDGE-CASE` are covered. `INTEGRATION` is not, because the submit
callee is answered rather than run, so nothing here reaches a file or a device. `FULL-SUBSYSTEM` is
not, because whatever fills the capture buffer is outside this family.

**This is the first pilot to cover `SERIALIZATION`.** Before it the dimension read eleven `n/a` and
one `no` across the whole parity page — the one dimension with no `yes` anywhere — which is what
made this contract worth executing ahead of two cheaper ones.

**Four things a reimplementer must take from this contract:**

1. **Move `IMAGE`, never `SPACING`.** The 48-byte difference is the entire hazard, it is unchecked,
   and a reimplementation that gets it wrong is byte-identical over everything a digest would look
   at. §13 records the control that proves the suite catches it.
2. **The copy submits.** It is not a staging helper. Building from the old §12 formula produces a
   function that fills a buffer nobody collects.
3. **Read the selector bit before the move, not after.** It is held in a callee-saved register
   across the copy precisely so that it is an input to the operation.
4. **Nothing here validates anything.** Three fixed addresses and two fixed lengths; there is no
   error path to reproduce and no argument to check.

## 17. Related

- `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md` —
  the page this formalises.
- `_types/types.tsv` — `SaveImageHeader` (0x200) and `SavePayload` (0x56490); `0x200 + 0x56490 =
  0x56690`, which is the fourth check on the size and the reason the header and payload types tile it
  exactly.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `00180A70` | 519 | save-buffer body (caller `00181580`): `0016D680`, `0017EBD0`, `00861EC0`, `0062C360`, `0016D6A0` — allocation + copy helpers |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **ActorEntity — CLIENT and SERVICE.**
  - The 17-byte flag getter `00236760` is also read by `BattleUnit_TeardownAndDespawn`.
  - `BattleSystem_ResetRuntimeState` (`00237DF0`) initialises the slot-map classes through
    `BattleSlotMap_InitializeMappingClasses`.
  - `BattleStats_InitializeDefinitionRecord` (`0023AC80`) is called by `BattleUnit_ApplyUnitDefinition`.
- **CoreRuntimeScheduling — SERVICE and MECHANICAL.**
  - `0020E4E0`, the 21-byte `SaveloadManager` accessor, is called by a 465-byte core body.
  - `00233C10` and `00237DF0` read 7- and 11-byte core getters.
  - `0023AC80`'s resolver reads are MECHANICAL.
- **Resource — SERVICE.** `0027F5D0` calls a 75-byte Resource-filed helper.
- **Audio — SERVICE, not read.** `0062C360` calls a 4-byte Audio-filed stub.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatFormula — SERVICE.** `0030C470` on this page calls `BattleStats_ReconcileResourcesToEffectiveCapacity`, owned by that layer. What it reaches is the resource reconciliation: the effective value is `word[+0x28]` when `byte[+0x6C]` is non-negative and `byte[+0x7C]` is not below zero, and zero otherwise, compared against `word[+0x4C]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `BattleSystem_ResetRuntimeState`, owned by that layer, calls `0032A160` on this page. That caller is the runtime reset: it walks **40 records of `0x1C8` bytes** from `[02EBF190] + 8` and resets each through `0023AC80`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `0023AC80` on this page calls `FUN_0030c470`, owned by that layer. What it reaches is a per-record step that reads the `byte[+4]` / `byte[+5]` kind-and-state pair and clears `byte[+0x1C2]`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Spawn_Encounter_Lifecycle — CLIENT.** `FUN_002398f0`, owned by that layer, calls `0030C470` on this page. That caller is a 110-byte draw: the unit's `[+0x6A0]` must be clear of bits 0 and 2, and only then does it take a number from the shared LCG stream; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — SERVICE and CLIENT (SWE2-CONTRACT 2026-09-15, 4 edges).** `00181580` is consulted by two UI
bodies, `003C9E50` and `0035C430`; in the other direction `00237DF0`
(`BattleSystem_ResetRuntimeState` — already above for its Gameplay walk) calls `00313840`, and
`0027F5D0` calls `0028E790`. Incidental helper sharing on a save-path page.

**Platform — CLIENT (SWE2-EC7 2026-09-18, 13 edges).** `005CD7D0`, the 0x100-class
sized-delete shared tail placed below, is called by thirteen Platform-filed bodies
(`0061F200`, `0061F710`, `006209C0`, `006239C0`, and nine more `0061xxxx`/`0062xxxx`
destructors); the crossing is that the Platform object family ends on the same
`0016C6A0` delete path this page's `0062C360` save-buffer helper also reaches — the
layer consults the shared tail, it does not share ownership of it.

**Party — MECHANICAL (SWE2-EC7-34, 1 edge).** `00583D60` — the save-buffer sibling this page cites — calls `003271D0` on the Party layer. Shared-helper fan-in below the buffer op; no party relationship to the buffer machinery.

**Story_Event_Quest_Hunt — MECHANICAL (SWE2-EC7-34, 1 edge).** `00583D60` — the same save-buffer sibling — calls `0032A8A0` on the Story_Event_Quest_Hunt layer. Shared-helper fan-in below the buffer op.

## SWE2-EC7-20 update (2026-09-18) — `0062C360` buffer-body window + `0061E200` recursive walker + `005CD7D0` delete tail

`0062C360` (515 B) is the index-bounded element dispatcher this contract's
`00180A70` row names (the copy helper behind `0016D680`/`0016D6A0`/`0017EBD0`):
`edx` must be under the element count `max(1, [rbx+0x30]&0x7FFFFFFF)` else it
returns 3 (`0062C388`..`0062C3A2`); the `+0x38` table resolves count>1 →
`[rbx+0x38]`, 1 → `&rbx+0x38` inline, 0 → null (`0062C3A7`..`0062C3C3`), and
`r15 = edx*0x58` selects the row — an empty `[r15+row]` returns 0x15
(`0062C3C6`..`0062C3D5`). `ebp` caps iterations at `min(0xB, (+0x18 bit-1 ? 0 :
+0x10))` (`0062C3DA`..`0062C3EF`). When `+0xB4 & 0x10000` is clear it copies
`r8`'s 0xC8-byte block into `rbx+0xC0` (`0062C409`..`0062C48C`), back-links
`rbx`/`edx` into the row's `+0x40` element (`0062C4AA`..`0062C4B5`), and calls
`0062EB90` with the `01F7F590`/`01F7F5B8` globals (`0062C4B9`..`0062C4C7`);
the set arm runs `00615BC0`/`005FD050`, then `ebp` rounds of the `[r15+row]`
element's `+0x78` vcall on `r14 = [rax+0x110]` (`0062C4F0`..`0062C521`),
closed by `005FCF20`→`00225690`/`005CD7D0` (`0062C523`..`0062C542`). Callers
`0017E8E0`/`0017F3B0`/`00180A70`/`00180C80`/`00183320`/`00183640`/`00183A00`/
`00183C60`/`00183EE0`/`00184140`/`00193F90`/`001946E0`/`001B1630`/`001D8D60`/
`00607FA0` — ~~the save-image write family~~ the D3D11 texture path *(corrected 2026-10-02, OPUS: none of these bodies references a save buffer; the rows are `Texture2DD3D11Element` records, the section below)*.

**The texture path behind `0062C360` (OPUS, 2026-10-01; ASTRA's packages, each ACCEPTed by SWE2-AUDIT-SPEC at its own scoped bounds; static, nothing executed).** The rows are `Texture2DD3D11Element` records (0x58 bytes) of a `PTexture2DD3D11`.
- *Admission*, ASTRA [`texture-async-boundary`](../_experiments/evidence/texture-async-boundary/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../_index/candidates/auditspec-review-texture-async-boundary-0930/REVIEW.md)): the 0xC8-byte copy is twelve 16-byte load/store pairs and one 8-byte pair, each written as it is read, so no overlap guarantee follows. The element's `+0x40` async data takes the texture pointer at its `+8` and the index at its `+0x10` (element `+0x48` / `+0x50`); its slot 0 (`00D54348`, `00621FF0`) tails `00622010`. `0062EB90` hands `context + 0x38*bank` to `00199DB0`, which inserts the pointer as a **key in an ordered tree**, refusing a key already present, rather than appending a callback pair; an insertion increments the container's `+0x28`. That container count is not the element's `+0x38` wait counter.
- *The update callback*, ASTRA [`texture-update-arguments`](../_experiments/evidence/texture-update-arguments/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../_index/candidates/auditspec-review-texture-update-arguments-0930/REVIEW.md)): `00622010` calls graphics-context slot `0x180` once per mip, from mip 0 to `min(11, +0x18 bit 1 ? 0 : +0x10)` (1 to 12 calls), with `rcx` the context, `rdx` the element's resource, `r8d` the mip, `r9d` 0, and on the stack the running source pointer, a dword row pitch and 0. The first source pointer is element `+0x28`; the resource, count and format are read again inside the loop, so the admitted 0xC8-byte copy is not a frozen upload snapshot. With B the format dword `+0x14` and F bit 0 of format byte `+0x18`, a dimension rounds to `(d + 3) & ~3` when F is set; the pitch is `(B * w * (F ? 4 : 1)) >> 3` and the source advance `(B * w * h) >> 3`, each product cut to 32 bits before the shift. After the loop a masked count of 1 frees and clears the selected element's `+0x28` through `00584730`.
- *Removal*, ASTRA [`texture-async-removal`](../_experiments/evidence/texture-async-removal/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../_index/candidates/auditspec-review-texture-async-removal-0930/REVIEW.md)): `0062EC70` searches one bank, `context + 0x38*bank`, for the key (node key `+0x20`); on a hit it decrements the bank's `+0x28`, unlinks the node and frees its 0x28 bytes through the bank allocator's slot `0x18`, and a miss returns before any of that. The caller at `0062BD75` passes the bank current at release time (`01F7F590`) and the context `01F7F5B8`, not the bank the key was queued in, so a key left in another bank is not found by this call. That is a conditional source result, not an observed state.
- *Bank dispatch*, ASTRA [`texture-async-bank-dispatch`](../_experiments/evidence/texture-async-bank-dispatch/README.md), ACCEPTed by SWE2-AUDIT-SPEC ([review](../_index/candidates/auditspec-review-texture-async-bank-dispatch-0930/REVIEW.md)): `00185A50` submits with the bank current before the call, then sets `01F7F590` to the bank plus one, modulo 4, and returns it whatever the submission returned. `005FEA50` writes a 0x80-byte command (opcode `0x2F` at 0, the callback at `+8`, the data at `+0x10`), or returns 0xD when it cannot reserve one. The callback `00186610` reads the bank at `+0x10` and the current context and tails `0062EBC0`, which calls each key's virtual slot 0 before taking the tree successor, then frees the tree and resets the bank's count `+0x28`. Which interpreter executes opcode `0x2F` is open.
- Open across all four: real callers, threads and timing, every writer of element `+0x38`, natural pending work in another bank, and lifetime (FABLE's scheduling questions).

`0061E200` (105 B) is the state-gated lazy dispatch the same family drives:
`ecx = [rbx+0x30]` with bit 31 stripped (`0061E20B`/`0061E20E`) selects the
element slot — `>1 → [rbx+0x38]`, `==1 → &rbx+0x38` inline, `0 → null`
(`0061E212`..`0061E223`). When the slot is empty it forwards `rbx` into
`0061FDA0` with `r8b=1` and `r9b = bit-10 of [rbx+0x18]` (`0061E22C`..`0061E242`);
both arms stamp `dword[rbx+0xBC] = 1` (`0061E247`/`0061E259`), the non-empty arm
returning 0. Callers `0017E8E0`/`0017EBD0`/`0017F3B0`/`00183A00`/`00183C60`/
`00183EE0`/`00184140`/`00184380`/`001946E0`/`00607FA0`/`0062AB00`/`006510B0`/
`00686DE0` — including this contract's `0017EBD0` buffer arm.

`005CD7D0` (74 B) is a thread-keyed recursive-lock release: `call [008C21D8]`
fetches the current id (`005CD7D9`); when it matches `[rbx+0x20]` the `+0x24`
recursion count decrements and a zero count `lock cmpxchg`s the owner slot to 0
(`005CD7E3`..`005CD7FA`). With `[rbx+0x18] > 0` it tails into `005CD570` on
`&rbx+8` (`005CD802`..`005CD80F`), else returns. Twelve callers — `0017F760`/
`00616700`/`0061ED00`/`0061F200`/`0061F710`/`006209C0`/`006239C0`/`00626120`/
`006264F0`/`0062C360`/`0062C570`/`0062C820` — including this contract's
`0062C360`.

## SWE2-EC7-21 update (2026-09-18) — `0061DE20` element dispatcher + `006160B0` `??_G` pair

`0061DE20` (437 B) is a `dl&1`-gated resource-publish body: when bit 0 is set
and `[rbx+0x168]` is null it vcalls `+0xB0` on the `005FD050` service's
`[rax+0x108]` object with `rdx=&rbx+4`/`r8=&rbx+0x168` (`0061DE4C`..`0061DE70`),
then names the created resource `"RasterState"` through `0061C550` (`0061DE8E`..
`0061DE9A`); a null `[rbx+0x170]` repeats the publish with a staged `{2, rbx+4
block, rbx+0x14..+0x24}` record (`0061DE9F`..`0061DEEF`). `HRESULT < 0` exits
(`0061DE76`/`0061DEEF`); the `+0x180` arm continues the same pattern past the
verified span. The lazy resource registration the serialization family runs per
record. Callers `0061E760`/`006215A0`/`00624C30`/`00629580`/`00629C70`/`00686DE0`/
`006C8CA0`/`006C9CD0` — the `0061xxxx`/`0062xxxx` save-image family plus the
`006Cxxxx` dyngeo instances.

`006160B0` (139 B) is a constructor for one of the family's 0x100-byte records:
`005DCBE0(rcx)` runs the base init (`006160C2`), then `rbx+0x30` is set to 0
while the embedded sub-record at `+0x38` is zeroed — seven qwords plus a dword
(`006160C8`..`006160F1`) — and its `+0x40` slot takes the `00D54348` vtable
(`006160F4`/`006160FB`); `+0x30` then marks state 1 (`006160FF`), `+0xB8` and
`+0x90..+0xB0` zero (`00616106`..`0061612B`), and `rax=rbx` returns the object
(`00616132`). Callers `00162370`/`0017E8E0`/`0017F3B0`/`00183A00`/`00183C60`/
`00183EE0`/`00184140`/`00184380`/`001B6D90`/`005D38D0`/`006123F0`/`00615840`/
`00874350` — the same `0017Exxx`/`00183xxx` save-buffer caller cluster as
`0061E200`/`0062C360`.

## SWE2-EC7-29 update (2026-09-18) — `00615BC0` TLS-indexed wait pump

`00615BC0` (197 B) is the blocking wait the set arm runs inside
`005FD050`: the TLS slot `[gs:0x58] + dword[02EAED3C]*8 + 4` holds a
per-thread stamp compared against `02CC0400`; when the global leads,
`008092FC`/`0080929C` interlocked-update it and a `02CC0400 == -1` first
pass lazily constructs the `02CC03D8` condition object through
`005CC8A0` and registers the `008ACDA0` teardown via `00808B90`. The
loop then waits `005CD720(&02CC03D8, 0x3E8)` — each 1-second timeout
re-tests and invokes the `02CEDA18` wake-callback on `02CEDA10` when
registered; a signalled wait exits through `005FCF20` -> `00225690`,
with `eax == 1` chaining `005FD050`. Interior anchor `00615C40` (the
`call 005CD720` 1-second wait).

## SWE2-EC7-33 update (2026-09-19) - `00686DE0`

`00686DE0` (3,463 B) is ~~the save-image serializer~~ a D3D11 texture-path body, not a save-image serializer *(corrected 2026-10-02, OPUS: the four buffers' only rip references are the `002EF4A0`–`002EF7C0` bodies, SV-4, and no `006xxxxx` body calls a buffer getter; the save file is written by the storage machine, `003BAEB0` → `00862620` / `00866AD0` → `00866200`)* - 6 `00686D40` calls plus `0059D510`/`00584730`/`0017D260`/`0066FE20` over the buffer records. Interior anchor `00687A28` (a `00686D40` call).

## SWE2-EC7-33 update (2026-09-19) - `006215A0`

`006215A0` (**1,626 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,790 B, a wrong literal in the batch-33 append — the body is 1,626 B per the function list*) is the record marshal - three `movups` record copies plus `00628730`/`006227D0`/`0061DE20`, `02CBB900` referenced. Interior anchor `00621661` (the `00628730` call).

## SWE2-EC7-33 update (2026-09-19) - `006510B0`

`006510B0` (**1,227 B** — *corrected 2026-09-19 (SWE2-EC7); this line printed 1,007 B, a wrong literal in the batch-33 append — the body is 1,227 B per the function list*) is the `0063A990`-driven serializer - 9 calls plus `0060DE00`/`00625F10`/`00625F00`/`0061E270`/`0061E200`/`0060DD70`. Interior anchor `00651116` (a `0063A990` call).

## The header's last 320 bytes are never INDIVIDUALLY written and never read (2026-09-19, OPUS)

> **CORRECTED SAME DAY, by my own later finding.** This section first read *"never written and
> never read"*, and the first half is wrong. `SaveImageHeader` is the first `0x200` bytes of the
> save buffer, and **`SaveImage_ClearActiveRuntimeBuffer` and `SaveRuntime_ResetActiveImageAndRebindState`
> both run `memset(02164280, 0, 0x56690)`** — the whole image, header included — so these 320 bytes
> are **zeroed wholesale** every time the image is cleared. What the evidence below establishes is
> that **no code writes them individually**, which is a different and weaker claim. The distinction
> is the one this database kept losing today: *unread* is not *untouched*, and here *unwritten* was
> not *unwritten* either. The bytes have a defined value — zero — and a reimplementation must
> reproduce it.

`SaveImageHeader` is the first `0x200` bytes of each save buffer, and the store carries `0xC0`–`0x1FF`
as `unobservedTail00C0` — 320 bytes, 62 % of the type. They are not merely unobserved by a census:
**nothing initialises them and nothing reads them**, on every route measured.

**Initialisation stops long before them.** `00253A80 SaveRuntime_InitializeHeaderAndImageBackedState`
clears only the first `0x58` bytes — [`00253A93`](../_index/ADDRESS-INDEX.md) calls `00861EC0`
with `r8d = 0x58` on the buffer taken from the cached pointer at `02092758` — and then writes
individual fields at `+0x58`, `+0x5C`, `+0x60`, `+0x64`, `+0x68` and `+0x6C`, each through a fresh
`002EF640` call. Nothing in that body touches `+0xC0` or beyond within the header.

**The bulk clear deliberately skips the header.** [`002EF2E8`](../_index/ADDRESS-INDEX.md) memsets
`buffer + 0x200` for `0x1538` bytes — it starts exactly where the header ends. The header is
treated as a separate region that is populated field by field, not wiped.

**Four read routes, all silent in the tail:**

| route | result |
|---|---|
| static base scan of `02164280` (`singleton_field_scan --static --span 0x200`) | 35 offsets corroborate named fields, **0 inside any unobserved span** |
| the accessor closure — 28 callers of `SaveImage_GetActiveRuntimeBuffer` (`002EF640`), return value tainted | **0** in the tail; no indirect handoffs, so that closure is complete |
| the cached-pointer global `02092758`, whose **nine** readers include `GameState_GetGil` and `GameState_SetGil` | 6 offsets, **all at `+0x08`–`+0x1B`** |
| escaping interior pointers | only `+0x000`, the buffer pointer itself |

**For reconstruction:** those 320 bytes must exist — the header is `0x200` and every later offset
depends on it — but no code sets them~~, so what reaches the save file is whatever the buffer already~~
~~held~~ individually, and both clears zero them with the whole image *(corrected 2026-10-02, OPUS: `002EF5F6`–`002EF603` and `002EF656`–`002EF663` run `memset(02164280, 0, 0x56690)`, and the boot frame `0022B6E0` takes `002EF650` before any save; the correction at the head of this section)*. The buffer is `.bss` (`INTERIOR` storage at `02164280`, no allocation call), so on a fresh
process that is zero; across a save/load cycle it is whatever the previous contents were. **~~A~~
~~reimplementation that zeroes them is not reproducing the engine, and~~ A reimplementation must zero them, and one that writes anything into
them is inventing data the engine never wrote.** *(corrected 2026-10-02, OPUS: zero is the engine's value, as above)*

**Limit.** This is four static routes plus the initialiser, not a runtime observation. A writer
reached in a form the taint does not model would look identical — the same bound stated for
`BattleUnit +0x298` and the `ManagerSingleton` hole.

## `+0x20` is a seven-entry roster array, and `vec4StoreHead30` is a copy displacement

The store carries four semantically identified bytes at `+0x20`–`+0x23` — `slotRosterCharId`,
`slotRosterLevel`, `slotRosterJobNibbles`, `slotRosterFlags` — then a 12-byte gap
`unobservedSpan0024`, then `vec4StoreHead30` at `+0x30`. **All three rows describe one array.**

`SaveImage_FinalizeHeaderAndChecksum` (`00583D60`) writes those four bytes **indexed**:
[`00583E8A`](../_index/ADDRESS-INDEX.md) `mov byte ptr [rdi + r8*4 + 0x20], al`, and likewise
`+0x21`, `+0x22`, `+0x23` — scale 4, so they are the four bytes of **element `r8`**, not four
scalars. The count is in the tail fill: [`00583EBE`](../_index/ADDRESS-INDEX.md) `cmp rdx, 7 /
jge`, then `lea rax, [rdx + 8]` and `lea rax, [rdi + rax*4]` — address `rdi + rdx*4 + 32`, the same
base the entry writes use — and `rcx = 7 - rdx` entries are filled with `0xFF`
([`00583EE0`](../_index/ADDRESS-INDEX.md)).

So element *k* is at `+0x20 + 4k` and there are **seven**, spanning `+0x20`–`+0x3B` and ending
exactly where `conditionalFlagDword3C` begins. `unobservedSpan0024` is elements 1–3. Unwritten
entries are `0xFF`-filled, which is the sentinel a reader must expect rather than zero.

**`vec4StoreHead30` overlaps elements 4–6 and is not a field.** Its basis is a 16-byte `movups` at
`record+0x30` cited from three bodies — and in every one of them that instruction is a single step
of an **unrolled whole-header copy**: `SaveUI_RestoreActiveHeaderFromControllerBackup` has 23
`movups` around it marching `-0x80, -0x70, -0x60, -0x50…` in 16-byte steps,
`SaveWrite_PrepareAndSubmitFullImage` 18, `WorldTransitionSnapshot_CaptureRuntimeState` 24. **A
block copy's displacement is not a field.** This corpus has recorded that idiom twice before — the
nine phantom 16-byte elements inside `CharacterRenderObject`'s constructor memset, and the save
payload map that read one unrolled `0x200` copy as eight fields — and this is the third.

The row should be withdrawn to a gap and the array declared. That store edit is **prepared and not
applied**, for the reason given above.

**One false lead is recorded because it nearly became a fifth route.**
`SaveSlotTransaction_StateMachine` appeared to store the buffer pointer into memory at `00581E0E`.
It does not: `00581DCA` calls the accessor into `rax`, `00581E06` is `xor eax, eax`, and the store
writes **zero** into `[buffer+0]`. The scan had kept the taint because a 32-bit write did not clear
the 64-bit register — sub-register aliasing, now handled in `member_reach_scan.py`.



## The flags `006510B0` tests have a three-channel dispatcher behind them (2026-09-19, OPUS)

*`006505A0` surfaced from the `U-6` census (`12abaf9a9`) as one of three layout-bearing bodies no page
in the database cites. It is placed here because the `SWE2-EC7-33` section above records `006510B0`
calling `00625F10` and `00625F00`, and those are two of the three predicates this function dispatches
on — the same flags, read by a neighbouring body. **What the object is is NOT claimed**: it is
unnamed and unowned in the ledger, in a region (`00620000`–`0065FFFF`) whose documented citations are
overwhelmingly PhyreEngine. This section establishes its shape, not its identity.*

### A two-field wrapper: a pointer and a tag

`006505A0(w)` (183 B) reads exactly two things from its argument — `[w+0x00]`, a pointer to an inner
object, and **`byte [w+0x08]`, a tag** ([`006505AD`](../_index/ADDRESS-INDEX.md)). The tag selects one
of three arms; `NULL`, a tag `>= 3`, and a `NULL` inner pointer each fall through to a plain return,
so the function is total and silent on every malformed input.

### The three arms are the same contract three times

Each arm tests one dword on the **same inner object**, and on a non-zero result tail-jumps to a
handler. The handlers are not merely related — **each one clears the very dword its guard tested**:

| tag | guard | tests | handler | clears it at |
|---|---|---|---|---|
| `0` | `00625F00` | `[inner+0xBC] != 0` | `0062BCB0` (647 B) | [`0062BCCA`](../_index/ADDRESS-INDEX.md) |
| `1` | `00625F10` | `[inner+0x8C] != 0` | `0062BF40` (448 B) | [`0062BF5A`](../_index/ADDRESS-INDEX.md) |
| `2` | `00625F20` | `[inner+0xA4] != 0` | `0062C100` (502 B) | [`0062C11A`](../_index/ADDRESS-INDEX.md) |

The three guards are byte-identical eleven-byte bodies (`cmp dword [rcx+disp], 0 / setne al / ret`)
differing only in the displacement. The three handlers open with **byte-identical eight-instruction
prologues** — save `rbx`, push `r14`, `sub rsp,0x20`, `mov rbx,rcx`, one `call`, `mov rcx,[rbx+0x20]`,
`xor r14d,r14d`, then the clearing store — differing only in the callee (`0062B100`, `0062B170`,
`0062B1E0`, themselves **`0x70` apart and 112 bytes each**, so a parallel family of three) and in the
displacement cleared. The register stored is provably zero: `xor r14d, r14d` immediately precedes each
store.

**So the guard and the handler are two halves of one mechanism: a condition that is tested before the
work and consumed by it.** ~~Each channel is one-shot — running a handler twice without something~~
~~re-setting its dword does nothing the second time, because the guard will refuse.~~ Through the guarded dispatcher `006505A0`, each channel is one-shot: it tests the channel's dword (channel 0: `00625F00`, called at `006505A0+0x93`) before it tail-jumps to the handler (`006505A0+0xA8`). The handler itself tests nothing, so a direct call is not guarded. On channel 0, `00616C60` calls `0062BCB0` unconditionally (`00616C60+0x1B`), and `005DE250` calls it under the guard (`005DE250+0x1F`) and then tail-jumps to `00616C60` (`005DE250+0x2D`). On normal returns that path runs the handler twice when `+0xBC` is non-zero, and a second run is not shown to do nothing. *(corrected 2026-10-02, OPUS: ASTRA's title cleanup-guard qualification, SWE2-AUDIT-SPEC ACCEPT, routed by FABLE as R3 in [`astra-returns-title-fable-1002`](../_index/candidates/astra-returns-title-fable-1002/README.md))* That is a contract
a reimplementation has to preserve on all three channels or none.

### What this does and does not settle

- **Settled:** the wrapper's two fields; the tag's three legal values; that the three dwords are
  independent channels on one object; the guard/clear pairing on each; that `[inner+0x20]` is read by
  every handler; and that the dispatcher is total over bad input.
- **Inference, not proven:** that the dwords are *pending-work* or *dirty* flags. The test-then-clear
  shape is what a pending flag looks like, and `006510B0` testing two of them in a serializer is
  consistent with it — but **no writer of any of the three dwords has been read**, and until one is,
  "what sets it" is exactly the part that would turn this from a shape into a meaning.
- **NOT CLAIMED:** what the object is, what the three channels do, what `0062B100`/`0062B170`/
  `0062B1E0` are, and what `[inner+0x20]` holds.
- **Adopted 2026-10-02 (OPUS), from ASTRA's title packets** (each SWE2-AUDIT-SPEC ACCEPT; routed by FABLE as R4 in
  [`astra-returns-title-fable-1002`](../_index/candidates/astra-returns-title-fable-1002/README.md)). These narrow the list above for channel 0
  and say nothing about channels 1 and 2:
  - **Count and selector.** n is the low 31 bits of `+0x30` (`00623DF0` clears bit 31 with `btr` before it
    compares). Bit 31 is ignored by the selector and gates `00584730`. Records are `0x58` bytes. `00623DF0`
    returns `base + 0x58 * k + 0x38`, the address of a record's `+0x38` field, not a record base. The base is the
    pointer at `+0x38` for n > 1, the object's own `+0x38` for n = 1, and 0 for n = 0. There is no index bound
    and no write. `0062B100` walks indices up to max(1, n) and calls `005CCB80` with ECX = 1 while the selected
    DWORD is positive. With n = 0, its first read is at absolute address `0x38`: a precondition on valid
    state, not an observed fault.
  - **The deferred-call queue the title cleanup uses.** Entries are 16-byte `{function, data}` pairs, in four
    32-byte banks at `ctx+0xC38+32*k`, indexed by `ctx[+0xCB8]`. The consumer `00186230` calls `function(data)`
    with RCX = data (`00186230+0x43`, `+0x47`). The flush `00185C20` is called by the per-frame pump only when
    `01FD4A68` is zero, at most once per pump call. The getter `00189120` takes no argument.
  - **Heap ownership.** The queued data pointer reaches the CRT `free` import after `005DE250`.
  - **Still open:** that n >= 1 holds for the real caller, `005CCB80`'s effects, title lifetime, cancellation and
    idempotence.

## SWE2-EC7-34 update (2026-09-19) - `00626120`

`00626120` (971 B) is a save-buffer op - EH frame, `[rcx+0x30]&0x7fffffff` size, `00615BC0`/`005FD050`/`005FCF20`/`005CD7D0`/`00225690`/`00861EC0`. Interior anchor `006263D3` (an `00615BC0` call).



## SWE2-EC7-35 update (2026-09-19) - `00624C30`

`00624C30` (824 B) is a save-buffer sibling - `01F2FEB0`/`01F2FEB4`/`01F3021C`/`01F30220` state fields, `00808C40`/`0061DE20`/`0061C550`. Interior anchor `00624E8A` (a call site).

## SWE2-EC7-35 update (2026-09-19) - `00183320`

`00183320` (799 B) is a CRT import-bridge - `008C5B40`/`008C5B34` import thunks, `01F7F5A0` table, three `00861EBA` calls plus `0017EBD0`/`0016D6A0`/`0016D680`. Interior anchor `0018339B` (an `00861EBA` call).

## SWE2-EC7-35 update (2026-09-19) - `0061E760`

`0061E760` (790 B) is a save-image record init - `01F2DEB8`/`01F2DEC0`/`01F2DEC8`/`01F2DEB8` state, `0062BA30`/`0061DE20`/`0061D320`/`006187A0`. Interior anchor `0061E8AE` (a `0062BA30` call).

## SWE2-EC7-35 update (2026-09-19) - `0062AB00`

`0062AB00` (750 B) is a save-image diagnostics path - the `"StretchBlit"` name and the `4E89D2086F15AAF2` magic qword, `00620F60`/`0061E200` pairs plus `00626C30`/`00621C00`/`00808C40`. Interior anchor `0062AB58` (an `00808C40` call).


## SWE2-EC7-36 update (2026-09-19) - `0062C570`

`0062C570` (678 B) is a save-buffer op sibling - `005FD050`/`005FCF20` pairs plus `00615BC0`/`005CD7D0`/`00225690`/`00808C40`. Interior anchor `0062C5F9` (a `005FD050` call).

## SWE2-EC7-37 update (2026-09-19) - `00193F90`

`00193F90` (595 B) is a save-buffer record builder - `02CBB900`/`01F7F5A0`/`01F44830`/`02CF7368`, `0063A990`/`0060DD70`/`00610990`/`0017EBD0`/`0062C360` pairs plus `0016D680`/`0016D6A0`. Interior anchor `00193FCA` (a `0016D680` call).

## SWE2-EC7-37 update (2026-09-19) - `00183A00`

`00183A00` (593 B) is a save-buffer sibling - `01F44830`/`02CF7480`/`02CF7A30`/`01F7F5A0`, `00861EC0` pair plus `0085E730`/`006160B0`/`0060DD70`/`00610990`/`00625F00`/`0061E200`. Interior anchor `00183A4F` (an `0085E730` call).

## SWE2-EC7-37 update (2026-09-19) - `00183C60`

`00183C60` (589 B) is the next save-buffer sibling - same `00861EC0`/`0085E730`/`006160B0`/`0060DD70`/`00610990`/`00625F00`/`0061E200` shape over `02CF7480`/`02CF7A30`. Interior anchor `00183CAF` (an `0085E730` call).

## SWE2-EC7-37 update (2026-09-19) - `00180A70`

`00180A70` (519 B) is a save-buffer helper - `01F44830`/`01F7F5A0`, `0016D680`/`0017EBD0`/`00861EC0`/`0062C360`/`0016D6A0`/`00808C40`. Interior anchor `00180AAC` (a `0016D680` call).

## SWE2-EC7-37 update (2026-09-19) - `0017F3B0`

`0017F3B0` (512 B) is a save-buffer op - `01F44830`/`02CF7480`/`008C5AD0`/`02CF7A30`, `00625F00` pair plus `0085E730`/`00861EC0`/`006160B0`/`0060DD70`/`005CDAA0`/`00628100`. Interior anchor `0017F3EC` (an `0085E730` call).

## SWE2-EC7-38 update (2026-09-19) - `00180C80`

`00180C80` (452 B) is a save-buffer helper - `01F44830`/`01F7F5A0`, `0016D680`/`0017EBD0`/`00861EC0`/`00679570`/`0062C360`/`0016D6A0`. Interior anchor `00180CBA` (a `0016D680` call).

## SWE2-EC7-39 update (2026-09-19) - `006209C0`

`006209C0` (427 B) is a save-image Platform body - `005FCF20` quadruple/`005FD050` triple/`00225690`/`005CD7D0` pairs plus `00615BC0` and one vcall. Interior anchor `006209EB` (a `00615BC0` call).

## SWE2-EC7-40 update (2026-09-19) - `0062C820`

`0062C820` (384 B) is a save-image Platform sibling - `01F7F590`/`01F7F5B8`, `005FCF20`/`005CD7D0` pairs plus `00615BC0`/`0062EB90`/`00225690`/`005FD050`. Interior anchor `0062C8A1` (a `00615BC0` call).

## SWE2-EC7-40 update (2026-09-19) - `0061F710`

`0061F710` (383 B) is a save-image Platform body - `005FCF20` quadruple/`005FD050` triple/`00225690`/`005CD7D0` pairs plus `00615BC0` and one vcall. Interior anchor `0061F740` (a `00615BC0` call).

## SWE2-EC7-42 update (2026-09-19) - `003C9E50`

`003C9E50` (304 B) is a save-image body - `01E0C1E8`/`01EFE384`/`01EFE388`, `0024A5A0`/`00861EBA`/`00181580`/`003697F0`. Interior anchor `003C9E81` (a `0024A5A0` call).

## SWE2-EC7-42 update (2026-09-19) - `0035C430`

`0035C430` (300 B) is a save-image body - `0209AC30`/`022CA470`, `00861EBA`/`00181580`. Interior anchor `0035C4F9` (an `00861EBA` call).

## SWE2-EC7-47 update (2026-09-19) - `0017EBD0`

`0017EBD0` (219 B) is the save-buffer copy helper - `005CCB80`/`0061E200`/`00625F00`/`00626120`. Interior anchor `0017EBFC` (a `005CCB80` call).

## SWE2-EC7-47 update (2026-09-19) - `00183640`

`00183640` (211 B) is a save-buffer sibling - `0016D680`/`0016D6A0`/`0017EBD0`/`0062C360`/`00679570`/`00808C40`. Interior anchor `00183674` (an `0016D680` call).

## SWE2-EC7-52 update (2026-09-19) - `00621C00`

`00621C00` (760 B) is a save-image marshal body - `00628730`/`00629580`/`00626010`/`0061C690`/`0061C740`/`006227D0` plus `02CBB900`. Interior anchor `00621C7A` (a `00628730` call).


## SWE2-EC7-52 update (2026-09-19) - `00620F60`

`00620F60` (1594 B) is a save-image diagnostics path body - `0061FDA0`/`005FD050`/`00624090`/`00624270` plus `02CF7A30` fields. Interior anchor `00620FF6` (a `0061FDA0` call).


## SWE2-EC7-52 update (2026-09-19) - `006227D0`

`006227D0` (968 B) is a save-image marshal body - `0061C1C0`/`00808C40` plus `01F2DEC8`/`01F2DEB8` fields. Interior anchor `006227F8` (a `0061C1C0` call).


## SWE2-EC7-52 update (2026-09-19) - `00628730`

`00628730` (1039 B) is a save-image marshal leaf - `call qword [rax+0x180]` vtable call, no direct calls. Interior anchor `00628AF0` (the `[rax+0x180]` vcall).

## SWE2-EC7-53 update (2026-09-19) - `0066FE20`

`0066FE20` (589 B) is the `PIndexDataBlock` save-image block - `005FD050`, `0061C550` name-table registration, `call [rax+0x18]`/`call [rax+0x38]` vcalls, `00808C40`. Interior anchor `0066FE41` (a `005FD050` call).

## SWE2-EC7-54 update (2026-09-19) - `0061C740`

`0061C740` (339 B) is a call-free index-mapped gather-scatter - `[rsp+rdx*4]`/`[rsp+rax*4]` mapped writes into `[rcx+0x20..0x58]` (leaf/helper-band sibling of `0061C690`). Interior anchor `0061C783` (the `[rcx+0x20]` store).

## SWE2-EC7-57 update (2026-09-19) - `00626C30`

`00626C30` (175 B) is a save-image body - `0017D260`/`00584730`. Interior anchor `00626C7D` (a `0017D260` call).

## SWE2-EC7-58 update (2026-09-19) - `0061D320`

`0061D320` (166 B) is a save-image body - `00808C40` plus three vcalls, `01F44830`. Interior anchor `0061D3B6` (a `00808C40` call).

## SWE2-EC7-59 update (2026-09-19) - `0061C690`

`0061C690` (164 B) is a call-free six-slot `0x30`-stride record defaults - `[rcx]`/`+0x30`/`+0x60`/`+0x90`/`+0xC0`/`+0xF0` each `{float,float,eax,1.0f}`. Interior anchor `0061C6B0` (the `+0x34` float store).


## SWE2-EC7-59 update (2026-09-19) - `00629580`

`00629580` (160 B) is a save-image helper - `0062BA30` single call. Interior anchor `00629594` (a `0062BA30` call).

## SWE2-EC7-61 update (2026-09-19) - `0060DE00`

`0060DE00` (152 B) is a call-free save-buffer validator - `1<<cl` bound then compares `edx`/`r8d`/`r9d` against `[r11+0x28]`/`+0x2C`/`+0x30` and `rax` against `[r11]`, returns a small code. Interior anchor `0060DE2C` (the `+0x28` compare).



## SWE2-EC7-64 update (2026-09-19) - `00181580`

`00181580` (139 B) is the save-buffer caller of `00180A70` - `0016D6A0`/`00180A70`/`00180C80`/`001B11D0`/`001B1C00`. Interior anchor `001815A2` (a `001B1C00` call).



## SWE2-EC7-65 update (2026-09-19) - `00686D40`

`00686D40` (135 B) is the save-image serializer's element body - `001AA0A0`/`001B7CE0`. Interior anchor `00686DAB` (a `001B7CE0` call).


## SWE2-EC7-67 update - `00679570`

`00679570` (129 B) is a save-buffer helper - single call then tail `00861EBA`. Interior anchor `006795CA` (a `00861EBA` call).

## SWE2-EC7-69 update (2026-09-19) - `00625F10` predicate measured

`00625F10` (11 B) measured - **the contract's predicate table is exact**:
`dword[+0x8C] != 0`, `setne`, ret. Call-free; it is the first of the three
predicates `006510B0` dispatches.
Interior anchor `00625F17` (the `setne`).

## SWE2-EC7-69 update (2026-09-19) - `00625F20` predicate measured

`00625F20` (11 B) measured - `00625F10`'s sibling predicate:
`dword[+0xA4] != 0`, `setne`, ret. Call-free; `+0xA4` is the flag
`0061E2E0` (below) writes on its init path.
Interior anchor `00625F27` (the `setne`).

## SWE2-EC7-69 update (2026-09-19) - `0061E270` lazy-slot init measured

`0061E270` (105 B) is the first lazy-init body behind `00625F10`'s flag:
`ecx = dword[+0x38]` with bit 31 `btr`'d off; `ecx > 1` uses the pointer at
`[+0x40]`, `ecx == 1` uses `&[+0x40]`, `ecx == 0` selects NULL (callers hold
`+0x38 != 0`). When the selected slot reads nonzero it returns 0; when empty
it calls `00620250(this, 0, 1, ([+0x18] >> 0xA) & 1, 0)` - bit 10 of `+0x18`
is the mode arg - and returns its result. Every path sets `dword[+0x8C] = 1`,
which is the flag `00625F10` tests.
Interior anchor `0061E2B2` (the `00620250` call).

## SWE2-EC7-69 update (2026-09-19) - `0061E2E0` lazy-slot init measured

`0061E2E0` (96 B) is `0061E270`'s sibling on the second slot pair: `ecx =
dword[+0x30]` `btr`-31 selects `&[+0x38]` (count 1) or `[+0x38]` (count >1);
empty slot → `00620630(this, 0, 1, 0, 0)` with a fixed `r9d = 0` instead of
the `+0x18`-bit extract; non-empty → return 0. Every path sets
`dword[+0xA4] = 1` - the flag `00625F20` tests.
Interior anchor `0061E319` (the `00620630` call).

## SWE2-EC7-79 update (2026-09-20) - `0062BA30` + `00620630` + `00620250` measured

`0062BA30` (126 B) is the four-pointer virtual release: `+0x168`,
`+0x170`, `+0x180`, `+0x178` each get `call [obj][0]+0x10` when
non-NULL, then are zeroed - the save-image teardown's child sweep.
Interior anchor `0062BA4E` (the `call [rax+0x10]`).

`00620630` (902 B) is the `PCubeMap` create path: the `01F44830`
config flag picks the early arm; `005FD050` runs the shared gate;
then `0061C550("PCubeMap")` resolves the descriptor, `0061FC50`
allocates, `00620E10` initialises, and `00808C40` cleans the
failure arm - with `+0x28`/`+0x50` virtual hooks on the record.
Interior anchor `00620941` (the `0061C550` descriptor call).

`00620250` (978 B) is the sibling `PTexture3D` create path -
identical shape with `0061C550("PTexture3D")`, `0061FAF0` alloc,
`00620CB0` init, and `+0x30`/`+0x50` virtual hooks.
Interior anchor `006205A1` (the `0061C550` descriptor call).

## SWE2-EC7-103 update (2026-09-20) - `0027EF00` measured

`0027EF00` (68 B) is the `0x6E`-keyed four-call
sequence `0027F5D0` and `002814E0` run:
`002C9400(0x6E)` opens, `002C9060` takes the three
`01E0C3E0`/`01E0C3BC`/`01E0C3E8` dwords,
`002C9890(0x6E)` re-keys, and a
`002C9490(0, 0, [01E0C3E8])` tail closes - the
fixed-id command bracket the save-buffer arms
post.
Interior anchor `0027EF21` (the `002C9060`
call).

## SWE2-EC7-120 update (2026-09-21) - `00650660` measured

`00650660` (62 B) is the
tag dispatch `006510B0`
calls: a `[rcx]` equal to
`02CF7A30` returns 7, else
`00625F10(rcx)` true
returns 0, else it tails
`0061E270(rcx)`.
Interior anchor `00650680`
(the `00625F10` call).

`002804E0` (232 B) is the two-arm widget submit `0027F5D0` runs: `0209AC30 + 0x3F0` bit 8 set submits widget `0x5F` twice through `002C9400`/`002C9060` and `002C9890`/`002C9490` with the `01E0C3C0`/`01E0C3E8` rect constants, then `002903D0([+0x3E8])` + `002903F0(6)` and tails `0028E790`; bit 8 clear uses widget `0x6E` with the `01E0C3BC`/`01E0C3E0` constants and a zero-arg `002C9490`, then `002903D0([+0x3E8])` and tails `0028E630` - both arms run `002CD7B0` first when bit 9 is set

Interior anchor `0028056B` (function `002804E0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Presentation — BOTH DIRECTIONS, 156 edges: ~~the save image is captured through the renderer's own graphics-device~~
~~layer.~~** *(corrected 2026-10-02, OPUS: these bodies are the D3D11 texture path, not a save-image route — the save image is written by the storage machine)* ~~The save-image write family this page names~~ The texture-path family shares its helpers with the renderer:
- the `0017E8E0` / `0017EBD0` / `0017F3B0` / `00183A00` / `00183C60` / `00183EE0` / `00184140` / `00184380` /
  `001946E0` bodies;
- the device wrappers they drive: the `005FD050` service, the resource namer `0061C550` (`"RasterState"`), the lazy
  dispatch `0061E200`, `00615BC0` / `00616700`, `0062C360`, the `0063A990`-driven serializer and `00686DE0`.

The renderer's use of them:
- `Renderer_CreateRandomNoiseTextureFromGraphicsMT19937` calls eight of those wrappers.
- The render bodies `00180E70`, `00181000`, `00181190`, `00181250`, `001A4DB0`, `003AA6B0` and `00500C00` call the
  getters `001B1C00`, `00184140` and `00183EE0`.
- `0018D850`, `00193AD0` and `001D5970` call `00615BC0` / `00616700`.

This contract owns the buffers, the header and the copy. The device layer is presentation machinery
(`CONTRACT-render-command-list-and-graphics-handshake`).

**Input — MECHANICAL, 32 edges.**
- The same device helpers have input-side callers: `0063A990` from 25 bodies in `00873090`-`008731E0`, and
  `00615BC0` / `00616700` from `0079C140` / `007A05D0`.
- `InputGameplay_ArbitrateDigitalInputAndModalState` asks the mode predicate `00236760`.
- The controller state handler `0027F5D0` calls `002D66A0`.
- The teardown's `002814E0` calls `001E0F20`.

**WorldAreaField — BOTH DIRECTIONS, twelve edges.** A field transition snapshots and restores the same buffers:
- `WorldTransitionSnapshot_CapturePersistencePairForActiveSlot`, `WorldTransitionSnapshot_RestorePersistencePairForActiveSlot`,
  `WorldTransitionSnapshot_CaptureRuntimeState` and `WorldTransition_StageFieldTransition` call `00236760` and
  `SaveImage_GetActiveRuntimeBuffer`.
- `WorldTransition_RequestFieldTransition`, `WorldTransition_RequeueCurrentFieldForRestore` and
  `WorldTransition_StageFieldTransition` call `002EFA70`, a reader of the live record at the backup buffer's
  `+0x56690`.
- `World_UpdateSimulationTick` calls `002EF910`.
- The header finalizer `SaveImage_FinalizeHeaderAndChecksum` reads `MapRef_GetPersistenceGroupId` and
  `WorldTransition_GetActiveOrPendingFieldId`.

**Script_VM_Native_Bridge — CLIENT, eleven edges.** Script handlers call the `+0x56690` record's accessors: `002EFA70`
(6, from `003559B0`, `00355EB0`, `00356270`, `00356650` and others), `002EF840` (`00349B30`, `0034A050`) and
`002EF890` (`00355350`). The predicate `00236760` is called from `0050F540`, and `002398F0` from `0050F910`.

**Items_Equipment_Shops_License, Status_Periodic_Terminal and CombatAI — CLIENT, six edges: the load-time reset.**
- The load path `00233C10` rebuilds the inventory (`InventoryRuntime_RebaseClassDescriptorsAndClearDerivedState`) and
  the gambits (`GambitRuntime_RebuildAllOrderSets`).
- `BattleSystem_ResetRuntimeState` re-initialises the inventory from its authored table.
- `0030C470` recomputes the licence rank and the auto-statuses (`BattleStats_ComputeLicenseDerivedRank`,
  `BattleStats_RemoveStatusesFromMaskAndRecompute`, `BattleStats_RecomputeDerivedStateAndAutoStatuses`).

Each layer owns what it rebuilds.

**RNG_Random_Selection — SERVICE, two edges.**
- The noise texture draws the graphics-owned `GraphicsNoiseMT19937_TwistState`.
- `002398F0` draws `RNG_SharedGameplayLCG_NextU32`.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page reads them; no new body read (OPUS, 2026-09-29,
pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-save-image-buffers-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00162370` | 81 B | runs four initialisers, each with the object address in `rcx`: a 139-byte one on `02CBBE00`, an 89-byte one on `02CBBF88`, a 102-byte one on `02CBC018` and a 31-byte one on `02CBC368`; then tail-jumps `atexit` with a 12-byte exit stub | `00162384`, `00162391`, `0016239E`, `001623AB`, `001623BC` |
| `00185A50` | 45 B | calls a 209-byte routine with the incoming `rcx`, a 15-byte callback in `rdx` and dword `01F7F590` in `r8d`, then stores dword `01F7F590` plus 1, ANDed with 3, back to `01F7F590` | `00185A54`, `00185A62`, `00185A6F`, `00185A72` |
| `00186230` | 125 B | advances dword `[rcx + 0xCB8]` to `(value + 1) AND 3`, then for that index walks the 16-byte entries from qword `[rcx + 0xC38 + index * 0x20]` up to qword `[rcx + 0xC40 + index * 0x20]`, calling each entry's first qword with its second qword in `rcx`, and finally stores the `+0xC38` qword over the `+0xC40` qword | `0018624A`, `0018624D`, `00186277`, `0018627D`, `0018629A` |
| `00186610` | 15 B | tail-jumps to the 167-byte slot reset with qword `01F7F5B8` in `rcx` and dword `[rcx + 0x10]` of the incoming `rcx` in `edx` | `00186613`, `0018661A` |
| `001AA0A0` | 116 B | when qword `[rcx + 0x28]` is null it zeroes qwords `[rcx]`, `+8` and `+0x10` and dword `+0x18`; otherwise, with `s = [rcx + 0x28]` and `r = [s + 0x50]`, it stores dword `[r + 0x38]` to `+0x10`, qword `[s + 0x60]` to `[rcx]`, dword `[s + 0x74]` to `+0x14`, dword `[r + 0xF8]` to `+0x18` and qword `[s + 0x10]` to `+8`, and when the `+0x14` value is nonzero it then, while `[rcx]` equals `[rcx + 8]`, adds the `+0x10` value to `[rcx]` and replaces `[rcx + 8]` by the qword it points to | `001AA0A7`, `001AA0B9`, `001AA0D1`, `001AA0F0`, `001AA0F6` |
| `001B11D0` | 105 B | gets a key from the 159-byte routine that formats `rdx` through `%s%s%s` and lower-cases it, then searches the tree rooted at qword `[rcx + 0x2218]` with head `rcx + 0x2208`, keeping each node whose dword `+0x20` is at least the key (unsigned) and descending `+8` from it, else descending `+0`; when the kept node is the head or its key is above the key it returns 0, otherwise it tail-jumps a 4-byte getter that returns qword `[[node + 0x28]]` | `001B11D9`, `001B11F4`, `001B120F`, `001B122C`, `001B1231` |
| `0028E630` | 37 B | calls a 648-byte routine with `ecx = 0` and `edx = 6`, then a 19-byte setter that stores its `ecx` argument (the incoming `ecx`) into dword `+0x179D4` of a global object when that object exists, and tail-jumps to a 364-byte routine | `0028E638`, `0028E63F`, `0028E646`, `0028E650` |
| `00623DF0` | 56 B | clears bit 31 of dword `[rcx + 0x30]` and returns `base + edx * 0x58 + 0x38` (edx zero-extended), where the base is qword `[rcx + 0x38]` when the remaining value is above 1 (unsigned), `rcx + 0x38` when it is 1 and null when it is 0 | `00623DF3`, `00623DFA`, `00623E02`, `00623E18`, `00623E20` |
| `0062EBC0` | 167 B | takes the `0x38`-byte slot `rcx + edx * 0x38` (edx zero-extended): walks its node chain from qword `+0x10` up to the head `slot + 8` through a 68-byte successor helper, calling the first virtual slot of each node's `+0x20` object; then, for each node from qword `+0x18` along the `+8` links, calls a 96-byte recursive helper on `(slot, [node])` and frees the node through virtual slot `+0x18` of `slot + 0x30` with size `0x28`; finally stores `slot + 8` to `+0x10` and `+8`, 0 to qword `+0x18`, byte `+0x20` and dword `+0x28` | `0062EBD1`, `0062EBEC`, `0062EC16`, `0062EC30`, `0062EC49` |

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-save-image-buffers-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001AA120` | 280 B | for each 32-byte record in the range from qword `+0x2A0` to qword `+0x2A8` of `rcx`, looks up the node keyed by the record's dword `+0` (node key: dword `+0x20`) in the tree map at `rcx+0x268`, inserting it through `001A37C0` when absent, and calls `00183320(node qword +0x28, record qword +8, record word +0x10, word +0x12, dword +0x14, dword +0x18)` | `001AA13B`, `001AA181`, `001AA1D1`, `001AA203`, `001AA208` |
| `005DDBB0` | 164 B | tears down four members of `rcx` in order: `006167C0(rcx+0x568)`; for `rcx+0x218` `0062C100` only when `00625F20` returns non-zero, then `00616D20`; for `rcx+0x188` `0062BF40` only when `00625F10` returns non-zero, then `00616CC0`; for `rcx` itself `0062BCB0` only when `00625F00` returns non-zero, then `00616C60` | `005DDBCE`, `005DDBDB`, `005DDC06`, `005DDC2D`, `005DDC43` |
