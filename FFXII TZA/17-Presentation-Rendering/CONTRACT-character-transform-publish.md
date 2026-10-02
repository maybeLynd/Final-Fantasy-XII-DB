---
contract: publish a character's transform and motion scalars into the inactive half of a double buffer
category: 17-Presentation-Rendering
scope: operation
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 17-Presentation-Rendering/Character-Rendering/character-render-object.md
entries: ["001FB120"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 74 addresses cited - 4 data, 22 entry, 48 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-character-transform-publish-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the character transform publish

Vtable slot 13 of `CharacterRenderObject`, 496 bytes, 105 instructions, 48 of them `movups`, no loops
and no `jmp` leaving the extent. It is the operation that hands a character's pose to the renderer,
and it is the reason the object is 0x668 bytes rather than 0x4C4.

## 1. Purpose

Everything a character shows on screen this frame — three 4×4 matrices and two motion scalars — is
written here, into **one of two banks**. The other bank holds the previous publish untouched. Which
bank is current is decided elsewhere, by a byte this operation only reads.

## 2. Interface

| | |
|---|---|
| entry point | `001FB120` (496 B), reached only through vtable slot 13 at `00903B68 + 13*8` |
| calling convention | Microsoft x64 |
| parameters | `rcx` = the `CharacterRenderObject`; `edx` = an index into the object's record array; `r8d` = a flag tested only for zero (`001FB185 test r8d, r8d / sete cl`); `xmm3` = a motion scalar, moved to `xmm7` on entry; a second motion scalar arrives on the stack at `[rsp+0x70]` and is loaded into `xmm6`; three source matrix pointers arrive on the stack |
| return type | none used |
| return semantics | — |
| callbacks / indirect dispatch | reached only as a vtable slot; it calls one accessor, `00189120` |

> ### ⚠ §2 and §3 describe the second half of this function
>
> **CORRECTED 2026-09-12 (`OPUS-CHARPUB-ISOLATED`), by reading the body end to end.** The sections
> above and below describe the bank copy, and three things happen *before* it that they do not
> mention. A reimplementation built from §2's parameter list would ship none of the three.
>
> **Two of them were already in §15** — the ready flag and the NaN-aware zero test each have an
> evidence row. That is the more precise statement and it matters: the contract *knew*, and its
> **interface section did not say**, which is the failure mode a reimplementer actually hits. They
> read §2 for the signature and §3 for the shapes. The third, the two sinks, was in neither.
>
> 1. **An early-out, and it is total.** `001FB126 movzx eax, byte [rcx+0x4B4]` / `test al, al` /
>    `je 001FB305` skips the **entire** operation — no scalars, no matrices, and neither of the two
>    flags below. A disabled object publishes nothing at all.
> 2. **A zero-motion test.** Both motion scalars are compared against `0.0` with `ucomiss`, and the
>    `jp` arms route an **unordered** compare exactly where a mismatch goes. So the dword published
>    below is `0` only when **both scalars are exactly zero and neither is NaN**.
> 3. **Two optional sinks**, at `record+0xE0` and `record+0xE8`, each null-checked. When present, a
>    **16-bit** offset at its own `+0x10` indexes a buffer reached through `[[record] + 8]`, and a
>    dword is stored there: the zero-motion result into the first, `(flag == 0)` into the second.
>    Both are written **before** the accessor call and before any matrix moves.
>
> All three are now executed — §13.

## 3. Types

Three structures participate and the operation writes into **two different ones**, which is the
single most important thing to get right about it.

| structure | role | evidence |
|---|---|---|
| `CharacterRenderObject` (0x668) | holds the two matrix banks at `+0x4C4` and `+0x584`, 192 bytes each | `001FB26D` / `001FB1CD` and the twelve `movups` after each |
| the record at `object+0x58` (stride 0x318) | holds the two motion scalar pairs | `001FB14A imul rdi, rax, 0x318` then `001FB15C add rdi, qword ptr [rcx + 0x58]` |
| the object behind `*(char**)0x01F7F598` | carries the bank parity byte at `+0x1C` | `00189120` is `mov rax, qword ptr [rip + 0x1df6471]; ret`, then `001FB1B1 cmp byte ptr [rax + 0x1c], 0` |

Bank layout, and the two banks are contiguous, equal and adjacent:

| | matrices | motion scalars |
|---|---|---|
| **bank A** (parity byte `== 0`) | `object + 0x4C4 .. 0x583` | `record + 0x08`, `record + 0x10` |
| **bank B** (parity byte `!= 0`) | `object + 0x584 .. 0x643` | `record + 0x0C`, `record + 0x14` |

`0x584 − 0x4C4 = 0xC0 = 192 = three 64-byte matrices`, and the scalar slots are four bytes apart in
the same pattern. Each matrix is copied with four `movups` from a pointer on the stack: three
sources, three destinations, twelve 16-byte moves per bank, fully unrolled.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `rcx` must be a constructed `CharacterRenderObject` with `+0x58` pointing at its
record array, and `edx` must be a valid index into it — **the operation does not bound-check `edx`**
(§10.2). The ready flag at `object+0x4B4` must be non-zero or nothing happens at all.

**Postconditions.** Exactly one bank is written: three matrices and two scalars. The other bank, and
every other byte of both structures, is unchanged.

**Invariants.** The operation never writes both banks, never reads the bank it writes, and never
writes the parity byte. It is therefore safe to run while a reader walks the other bank — which is
the entire point of the arrangement.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `object+0x4B4` (the gate), `object+0x58` (the record array), `*(char**)0x01F7F598 + 0x1C` (the parity), the record's `+0xE0` and `+0xE8`, three matrix pointers from the stack | `001FB126`, `001FB15C`, `001FB1B1`, `001FB17E`, `001FB198` |
| written | one bank's three matrices and two scalars | `001FB26D`…`001FB2F4` (bank A), `001FB1CD`…`001FB254` (bank B) |
| allocated | none | |
| deallocated | none | |

## 6. Relationships

**Callees:** `00189120` only — a two-instruction getter for the parity object.
**Callers:** none directly; the operation is reached through vtable slot 13.

## 7. State transitions

There is one edge, and it belongs to the caller rather than to this operation: the parity byte flips
somewhere else, and that flip is what makes the bank this operation just wrote become the one the
renderer reads. **This operation cannot advance the double buffer** and nothing in its 496 bytes
writes the parity byte.

## 8. Script · resource · event interactions

None. The matrices arrive as pointers from the caller; no authored table or opcode participates.

## 9. Determinism

**RNG** — none.
**Ordering** — ~~the publish must run before whatever flips the parity byte,~~ *(answered: see §14.1 - nothing flips it per frame; it is a camera-source flag; 2026-10-02, OPUS)* and the renderer must read
the other bank while it runs. Neither ordering is enforced here; both are assumed.
**Threading** — no synchronisation. The double buffer *is* the synchronisation, and it only works if
the parity flip happens between publishes rather than during one.
**Floating point** — the motion flag is computed by comparing two floats against zero with `ucomiss`
and branching on both the parity and zero flags (`001FB162`–`001FB179`). A NaN in either scalar takes
the unordered branch and yields 1, and **negative zero compares equal to zero and yields 0**. A
reimplementation writing `(a == 0.0f && b == 0.0f) ? 0 : 1` reproduces both, which is worth stating
because the obvious alternatives — a bit-pattern test, or `fabsf(a) < eps` — do not.

## 10. Failure paths and edge conditions

1. **The ready flag gates everything.** `001FB126 movzx eax, byte ptr [rcx + 0x4b4]` / `test al, al` /
   `je 001FB305`: with it clear the operation returns having written nothing, and **the previous
   contents of both banks stand**. A reimplementation that clears or defaults a bank when not ready
   will show a character snapping to identity rather than holding its last pose.
2. **`edx` is not bound-checked.** It is multiplied by 0x318 and added to the record array pointer
   with no comparison against any count. Nothing in this operation prevents an out-of-range index
   from writing past the array.
3. **The record's `+0xE0` and `+0xE8` are null-tested** (`001FB18B`, `001FB1A2`) and the dependent
   writes are skipped when either is null; the matrix publish itself is unaffected.
4. **Both motion scalars zero** yields flag 0, anything else yields 1 — see §9 for the two cases that
   look like exceptions and are not.

## 11. Observable behaviour

In memory: with the character visible and moving, the 192 bytes at `object+0x4C4` or `object+0x584`
change every frame and the *other* 192 bytes do not — **but NOT alternating frame by frame: which of
the two is live is fixed by the camera source (§14.1), so it changes at a camera hand-over and not
otherwise.** With the
ready flag cleared, neither changes. On screen: a character whose ready flag is cleared mid-motion
holds its last published pose rather than resetting.

## 12. Reproduction formula

```
publish(object, index, flag, scalarA /*xmm3*/, scalarB /*[rsp+0x70]*/, m0, m1, m2):
    if object[0x4B4] == 0: return                  # nothing is written, both banks stand
    record = *(char**)(object + 0x58) + index * 0x318
    moving = (scalarA == 0.0f && scalarB == 0.0f) ? 0 : 1
    ...                                            # the two null-tested record writes, §10.3
    parity = (*(char**)0x01F7F598)[0x1C]
    if parity == 0:                                # bank A
        record[0x08] = scalarA;  record[0x10] = scalarB
        copy 3 matrices of 64 bytes from m0,m1,m2 to object+0x4C4
    else:                                          # bank B
        record[0x0C] = scalarA;  record[0x14] = scalarB
        copy 3 matrices of 64 bytes from m0,m1,m2 to object+0x584
```

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-12)

The 496-byte body runs at its real virtual address under Unicorn against an independent
reconstruction, driven through the same eight-argument interface the vtable slot is called with:
four in registers, and **the second motion scalar and all three matrix pointers on the stack**.

**Instrument:** [`diff_character_publish.py`](../../../Reconstruction/Tests/Differential/diff_character_publish.py)
against [`character_publish.c`](../../../Reconstruction/Game/Presentation/character_publish.c).

**Result: 156 commands, 101 compared lines, 0 mismatches** — 14 distinct bank images out of 21,
5 distinct sink-buffer images out of 20, and **exactly 1 of 20 traces without the accessor call**,
which is the early-out case and no other.

### What the run established that reading had put in the wrong section

All three of the things §2 and §3 omitted are now executed, and one of them was in **neither** §2
nor §15 before this pilot: **the two optional sinks**. Each is null-checked, each indexes the buffer
at `[[record] + 8]` through a **16-bit** offset at its own `+0x10`, and both are written before the
accessor call. They are driven present and absent independently and at two offsets. §15 now carries
the row.

**The early-out is total, and the trace is what proves it.** With the ready flag clear, the banks,
both scalar pairs and the sink buffer are all unchanged — and the accessor is never called. A
reconstruction that returned early but still resolved the parity object would pass every state
comparison and differ only in the trace.

**The NaN arms are driven, and they are the reason the zero test is not a plain `== 0`.** Cases at
`(NaN, 0)` and `(0, NaN)` take the `jp` route, which lands where a mismatch lands. A reconstruction
written as `a == 0 && b == 0` happens to be right in C — a NaN compares unequal to `0.0` — but
nothing in a suite without NaN cases would have told the author whether that was reasoning or luck.

**And the flag argument is tested only for zero**, driven at 0, 1 and 12345, with 1 and 12345
required to publish the same dword. A case at one non-zero value would have tested a value; two test
the claim.

### How far the instrument itself has been tested

**42 mutants: 34 KILLED · 3 EQUIVALENT · 5 NO_BUILD · 0 INVALID · 0 TIMEOUT · **0 SURVIVED**.** (Re-run 2026-09-12: the six INVALID were mutants this suite HAD caught and the instrument could not read — `OPUS-CONTRA-HARNESS-LINECOUNT-INVALID`. All six are kills.)
Production inputs verified stable, and all four input hashes checked against the working tree after
the last edit.

**Zero survivors, and the four that the first clean campaign did have shared one cause worth
recording: the fixture was importing the constants it was supposed to test.** The driver included
`character_publish.h` and planted the enable byte at `CP_ENABLE_AT`, the record pointer at
`CP_RECORDS_AT` and so on. A mutation of any of those moved the **fixture and the reconstruction
together**, leaving them consistent with each other, and the mutants survived for that reason alone.
Every offset in the driver is now written out as a literal, duplicating the header on purpose.
*A fixture that derives its layout from the header under test cannot detect a layout error in it.*

**The five NO_BUILDs are the bank-gap check firing** — `cp_bank_gap_check` asserts
`CP_BANK_B - CP_BANK_A == CP_BANK_BYTES`, so moving either bank base, the matrix size or the matrix
count refuses to compile.

**The six INVALIDs are detections the campaign cannot score, and unlike the workbench pair this one
cannot be fixed by a better fixture.** Each mutates a *pointer* offset — `[object+0x58]`, the record
stride, `[[record]+8]`, `[record+0xE0]`, `[record+0xE8]`, or the sink's own `+0x10` — so the mutant
reads a pointer out of the middle of a randomly filled block and dereferences whatever it finds. The
driver dies. That is a real difference, observed violently rather than quietly: the reference does
not crash and the mutant does. The workbench pair's crashes were fixable because the slots being
misread were *unused pointer slots* that could be pointed somewhere safe; there is no fixture here
in which every wrong offset still yields a valid pointer, and building one would mean a block that
is nothing like a record.

**An input-drift run was discarded rather than cited.** The first clean attempt was launched and
then the harness's `CONTRACT_MAP` was edited while it ran — the rule this project already has, in
my own words, is to finish every edit, run the harness green once, and only then launch. The
campaign's own `production_inputs_stable` came back **False** and the hash of
`diff_character_publish.py` no longer matched, so the numbers were not usable. The tool caught it;
the discipline did not.

Every claim is otherwise a decoded instruction from the verified image.

> **⚠ THE EXPERIMENT THIS SECTION USED TO PROPOSE WOULD HAVE RETURNED A FALSE NEGATIVE, and it is
> withdrawn.** It read: *"watching two 192-byte ranges alternate across frames is a cheap and
> decisive observation"*. It is cheap and it is **not decisive** — §14.1 now establishes that the
> banks are chosen by CAMERA SOURCE, so in steady play with one camera **they do not alternate at
> all** and an observer would record "no alternation" as a refutation of a contract that is right.
>
> **The discriminating observation is a CAMERA HAND-OVER** between the default view and a scripted
> or event view: the bank in use should change at the hand-over and not between frames within
> either camera. Stated here rather than left implied, because a live run is the scarcest evidence
> this project has and the cost of spending one on a test that cannot fail informatively is paid
> twice — once in the run, and again in the wrong conclusion it licenses.

## 14. Unresolved

1. ~~**What flips the parity byte at `*(char**)0x01F7F598 + 0x1C`, and when in the frame.**~~
   **ANSWERED — and the question's premise was wrong. NOTHING FLIPS IT PER FRAME.** It is not a
   parity byte at all: it is a **camera-source flag**, written by the view publish. Folded from
   FABLE's E-9 note by OPUS 2026-09-13, with its three load-bearing instructions re-verified at the
   image first: `00185A1D mov byte ptr [rcx + 0x1c], 1` and `001860E6 mov byte ptr [rcx + 0x1c], 0`
   are ~~the only two other writers image-wide~~ two of the three writers besides the constructor (the third is the per-frame method `00189CE0`, at `00189CE0`+0x40A) *(corrected 2026-10-02, OPUS: the constructor is `00184F20`, `00184F20`+0x39 `mov word ptr [rcx + 0x1c], si`; `00189CE0` is called from the per-frame pump at its `+0x89`)*, both reached through the getter `00189120`; and
   `00259FA0` is `lea rdx, [02097B80]` / `cmp rcx, rdx` / `sete al` — it returns 1 **iff the
   published view IS the static default view object**, 0 for anything else. `003829D0` chooses
   between the two writers on that result. So the byte says *default camera versus scripted or
   event view*, and it is rewritten on every camera publish rather than every frame.

   > **The consequence for §7 and §11 is larger than the answer.** The two banks at `+0x4C4` and
   > `+0x584` are **selected by camera source, not alternated frame by frame**, so a reimplementation
   > that ticks a parity bit each frame would be wrong in the ordinary case — in steady play with one
   > camera, the same bank is written every frame and the other is stale.
   > *Answered 2026-09-12 (FABLE, E-9). **FOLDED INTO THE CONTRACT BY OPUS 2026-09-13**, with its key instructions re-verified at the image; the item above carries it.* **Nothing
   > flips it per frame; the camera publish writes it.** The object behind `01F7F598` is the
   > thrice-pumped per-frame singleton of [the application root](../00-Engine-Core-Runtime/Application-Root/game-application.md) (`Ensure` `00189000`, constructed by
   > ~~`00189CE0`, which zeroes the byte at `0018A0EA`~~ `00184F20` (`00189000`+0x61); `00189CE0` is a per-frame method that also zeroes the byte, at `00189CE0`+0x40A *(corrected 2026-10-02, OPUS: `00189000`+0x67 stores the constructed object in `01F7F598`; `00189CE0` is called from the per-frame pump at its `+0x89`)*). ~~Image-wide,~~ Besides it, the byte has exactly two other
   > writers, both reached through the getter `00189120`: `00185A10` stores **1** (`00185A1D`) and
   > `001860E0` stores **0** (`001860E6`), each then queueing one of the object's callback blocks
   > (`+0x358` / `+0x690`) on the queue behind `0018CA40` (`0018CBC0`). Their only callers are the
   > wrappers `001821F0` / `00182340`, and *those* are called from one place: `003829D0`, the view
   > publish that copies a `0xD0`-byte view record into the active view and then chooses **1 when the
   > published record is the static default view object at `02097B80`** (`00259FA0`: `view ==
   > 02097B80`) **and 0 otherwise** (`00382B18`–`00382B28`). `003829D0` runs from
   > `CameraSystem_SelectAndPublishActiveView` (`00259820`, at `00259932`, with the active view
   > pointer `020972F0`), from `00259970` and from `003ED8A0`; the camera publish is reached from
   > `00314370`, which the field frame `0022A770` calls at three sites and
   > `MainLoop_UpdateAndRenderFrame` at two — so the byte is rewritten on every camera publish of the
   > frame, before the render objects' slot-13 publish reads it. **So the "parity" is a view-source
   > flag — default camera versus any scripted or event view — and the two banks at `+0x4C4` /
   > `+0x584` are selected by camera source, not alternated frame by frame.** The live check written
   > below (banks alternating across frames) would therefore *not* see alternation in steady play; the
   > discriminating observation is a camera hand-over between the default view and an event view. All
   > static.
2. ~~**What the record's `+0xE0` and `+0xE8` point at**, and what the dependent writes mean.~~
   **ANSWERED — they are SHADER-PARAMETER BINDINGS RESOLVED BY NAME**, not pointers to data: `+0xE0`
   is `PS2ZBiasEnabled` and `+0xE8` is `PS2ZBiasNoGS`, bound by `001F7790` through
   `0018D240(material, name)`, which walks the material's two descriptor lists and returns the
   descriptor whose `+0x10` is the u16 offset the sinks index. So the operation publishes the
   zero-motion result into `PS2ZBiasEnabled` and `(r8d == 0)` into `PS2ZBiasNoGS`. **A reimplementation
   cannot hard-code these offsets**: they are whatever the material's own name lookup returns. Folded
   from FABLE's E-10 note by OPUS 2026-09-13.
   > *Answered 2026-09-12 (FABLE, E-10). **FOLDED INTO THE CONTRACT BY OPUS 2026-09-13**, with its key instructions re-verified at the image; the item above carries it.* **They are
   > shader-parameter bindings resolved by name: `+0xE0` is `PS2ZBiasEnabled` and `+0xE8` is
   > `PS2ZBiasNoGS`, so the operation publishes the zero-motion result into `PS2ZBiasEnabled` and
   > `(r8d == 0)` into `PS2ZBiasNoGS`.** The 0x318-stride record is reached by the accessor
   > `001F6E50` (`imul rax, rdx, 0x318` + `[rcx + 0x58]`) and bound by `001F7790`, which fills a run
   > of descriptor slots with the result of `0018D240(material, name)` — the name is loaded, the
   > lookup called, the result stored (`001F79FE` → `001F7A0F` → `001F7A1B` for `+0xE0`; `001F7A14` →
   > `001F7A25` → `001F7A31` for `+0xE8`). `0018D240` walks the material's two descriptor lists
   > (`+0x40` / `+0x48` and `+0x50` / `+0x58`, 0x18-byte entries whose `+8` is a tagged name pointer)
   > comparing bytes (`0018D270`–`0018D2AE`) and returns the descriptor, whose `+0x10` is the u16
   > offset the sinks index — the `[[record] + 8]` buffer is the material's parameter block
   > (`record + 0` is stored at `001F8452`). The run this note read: `+0x88` `lichtColor5`, `+0x90`
   > `lichtColor6`, `+0x98` `lichtAmbient`, `+0xA0` `AlphaThreshold`, `+0xA8` `PS2FogVec`, `+0xB0`
   > `clutBank`, `+0xB8` `TextureSampler`, `+0xC0` `PTAlphaThreshold` (the float sink `001FA0A0`
   > writes), `+0xC8` `paletteEnabled`, `+0xD0` `indexTex`, `+0xD8` `palette`, `+0xE0`
   > `PS2ZBiasEnabled`, `+0xE8` `PS2ZBiasNoGS`, `+0xF0` `PS2ZBiasOriginal`, `+0xF8`
   > `PS2ZBiasInstance`, `+0x100` `PS2WHMatrix`, `+0x108` `PS2HSMatrix` — and `001FAD50` copies the
   > ~~two 192-byte matrix banks (`+0x4C4` / `+0x584`) into the last two~~ three 64-byte matrices of one bank (`+0x4C4` or `+0x584`, chosen by byte `+0x1D`) into `+0x100`, `+0x108` and a third slot `+0x110` *(corrected 2026-10-02, OPUS: `001FAD50`+0x71, `001FAD50`+0xAF and `001FAD50`+0xED test the record's `+0x100`, `+0x108` and `+0x110`; the bank test is `001FAD50`+0x3B `cmp byte ptr [rax + 0x1d], 0`)* (`001FADCD`–`001FAE23`,
   > `001FAEC8`–`001FAF1E`), which corroborates the family. So the two null tests are "does this
   > material's shader declare the parameter": a material without the PS2 z-bias parameters skips
   > the two dword writes and nothing else. The PS2 z-bias emulation is therefore switched per
   > character by motion (`PS2ZBiasEnabled` non-zero when either motion scalar is non-zero) and by
   > the caller's `r8d` (`PS2ZBiasNoGS` set when it is zero); what the shader does with the two
   > flags is the shader's contract, not this one. The 792-byte record itself is the character's
   > **material-parameter binding record** (one per material slot), which names the undeclared type.
3. **What `r8d` selects.** It is tested only for zero and the result feeds a byte the operation writes
   *(2026-09-12, FABLE: the byte lands in the shader parameter `PS2ZBiasNoGS` — see item 2; the
   selector's own meaning stays with the caller, which the function list does not reach: `001FB120`
   has no direct call site, so it is a vtable or callback entry.)* *(answered: see character-render-object.md - it is slot 13 of the vtable `00903B68`, called through `[rax+0x68]` by slot 16 at `001FA3D0`+0x378; 2026-10-02, OPUS)*
   through a computed address; the consumer is outside this function.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the ready flag gates the whole operation | `001FB126`/`001FB138`/`001FB13A` | 1 (static, isolated original code) | PROVEN |
| the record array stride is 0x318 | `001FB14A imul rdi, rax, 0x318` with `001FB15C add rdi, qword ptr [rcx + 0x58]` | 1 (static, isolated original code) | PROVEN |
| the bank is chosen by a byte behind a global | `00189120` is a two-instruction getter on `01F7F598`; `001FB1B1 cmp byte ptr [rax + 0x1c], 0` | 1 (static, isolated original code) | PROVEN |
| bank A is `+0x4C4` and takes the `== 0` branch | `001FB1BA je 001FB260`, whose first matrix store is `001FB26D movups xmmword ptr [rbx + 0x4c4], xmm0` | 1 (static, isolated original code) | PROVEN |
| bank B is `+0x584` and is the fall-through | `001FB1C0`/`001FB1C5` write `record+0xC`/`+0x14`, then `001FB1CD movups xmmword ptr [rbx + 0x584], xmm0` | 1 (static, isolated original code) | PROVEN |
| each bank is three 64-byte matrices | twelve 16-byte `movups` stores per branch at a stride of 16 — `001FB1CD`–`001FB254` for B, `001FB26D`–`001FB2F4` for A; `0x584 - 0x4C4 = 0xC0 = 3 * 64` | 1 (static, isolated original code) | PROVEN |
| the scalar slots are four bytes apart between banks | `001FB260`/`001FB265` versus `001FB1C0`/`001FB1C5` | 1 (static, isolated original code) | PROVEN |
| the motion flag is a two-float zero test with NaN handling | `001FB162`–`001FB179`, branching on both `jp` and `jne`. Executed at (0,0), (0,x), (x,0), (NaN,0) and (0,NaN) | 1 (isolated original-code) | PROVEN |
| the flag argument is tested only for zero | `001FB185 test r8d, r8d / sete cl` — the value is never otherwise read. Executed at 0, 1 and 12345, and 1 and 12345 publish the same dword | 1 (isolated original-code) | PROVEN |
| two optional sinks publish the two flags before any matrix moves | **NOT IN THIS TABLE BEFORE 2026-09-12.** `[record+0xE0]` and `[record+0xE8]`, each null-checked at `001FB18B` and `001FB19F`; when present, a **uint16** at its `+0x10` indexes the buffer `[[record]+8]` and a dword is stored — the zero-motion result into the first, `(flag == 0)` into the second. Executed present and absent independently and at two offsets | 1 (isolated original-code) | PROVEN |
| nothing observed live | — | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The two banks, every store enumerated

`FUN_001FB120` is 496 bytes. Counting the 16-byte stores in each branch and printing their
displacements turns the `0xC0` subtraction from an inference into a demonstration:

| branch | stores | displacements |
|---|---:|---|
| **A**, taken at `001FB1BA je 001FB260` | **12** | `+0x4C4, 0x4D4, 0x4E4, 0x4F4, 0x504, 0x514, 0x524, 0x534, 0x544, 0x554, 0x564, 0x574` |
| **B**, the fall-through | **12** | `+0x584, 0x594, 0x5A4, 0x5B4, 0x5C4, 0x5D4, 0x5E4, 0x5F4, 0x604, 0x614, 0x624, 0x634` |

Twelve stores, **stride exactly 16**, `12 × 16 = 192 = 3 × 64` — three 64-byte matrices per bank, as
claimed. And the two runs are **contiguous**: A's last store covers `+0x574`–`+0x583`, and B's first
begins at **`+0x584`**. `0x584 − 0x4C4 = 0xC0` is not merely the distance between two labels — the
banks abut, with no gap and no overlap, which the subtraction alone could not show.

### Confirmed where each stands

`001FB14A imul rdi, rax, 0x318` (the record stride); `001FB185 test r8d, r8d` (the flag is tested
only for zero); `001FB1B1 cmp byte ptr [rax + 0x1c], 0` (the bank selector byte).

### The motion flag tests **both** floats, and guards both against NaN

```asm
001FB162  ucomiss xmm7, xmm0
001FB16C  jp  001FB179          ; unordered -> "moving"
001FB16E  jne 001FB179          ; non-zero  -> "moving"
001FB170  ucomiss xmm6, xmm0    ; only if the first was an ordered zero
001FB173  jp  001FB179
001FB177  je  001FB17E          ; both ordered zeros -> "still"
001FB179  mov edx, 1
```

§15 says *"a two-float zero test with NaN handling"* and that is exact: **each** float gets its own
`ucomiss`, and **each** has a `jp` in front of its equality test, so a NaN in *either* component
reports motion. The second `ucomiss` is reached only when the first compared equal — a short-circuit,
not a pair of independent tests.

**Not claimed:** nothing observed live.

## 16. Parity plan

`STRUCTURAL` — the two 192-byte banks and their adjacency.
`STATE-TRANSITION` — publish with the parity byte forced to each value and assert only the
corresponding bank changes.
`EDGE-CASE` — clear the ready flag mid-motion and assert both banks are byte-identical across the
frame.
`CALCULATION` — drive the motion scalars with `0.0f`, `-0.0f` and a NaN and assert the flag is 0, 0
and 1.
`TIMING` — ~~the one this contract cannot specify until §14.1 is answered~~ *(answered: see §14.1, answered: no per-frame flip exists to order against; 2026-10-02, OPUS)*.

**Done offline 2026-09-12** — see §13. `CALCULATION`, `STRUCTURAL`, `STATE-TRANSITION`, `EDGE-CASE`
and **`CONTRACT`** are covered; this is the fourth pilot to cover `CONTRACT`, because every
behavioural row of §15 is exercised and the only excluded row is the live-observation question.
`INTEGRATION` and `PRESENTATION` are not covered — the accessor is answered, no caller is
reconstructed, and nothing is drawn. `FULL-SUBSYSTEM` is not: the reader of the other bank and
whatever flips the parity byte are outside this operation.

`TIMING` is declared `N/A` by the harness, and the reason it gave — *"the frame alternation is the
caller's"* — **rested on the same wrong model §14.1 has now corrected: there is no frame
alternation.** The conclusion survives its reasoning: this operation writes whichever bank the
selector byte names and has no ordering of its own, so there is still nothing here for a timing test
to hold. **The bank choice is the CALLER'S and it tracks the camera, not the frame.**

**Five things a reimplementer must take from this contract:**

1. **Check the ready flag first, and return completely.** Not just the matrices — the two published
   flags must not be written either, and the parity accessor must not be called.
2. **Publish the two flags before the bank copy**, through the two optional sinks, each null-checked
   and each carrying its own 16-bit offset.
3. **The zero-motion dword is `0` only when both scalars are zero and neither is NaN.**
4. **One bank's matrices go with the same bank's scalars.** Mixing them tears a frame without ever
   writing out of bounds, which no bounds check would catch.
5. **The flag argument is a zero test, not a value.** Any non-zero value means the same thing.

## 17. Related

- `17-Presentation-Rendering/Character-Rendering/character-render-object.md` — the object, §4 and the
  slot 13 read this formalises.
- `_types/types.tsv` — `CharacterRenderObject`; its `+0x58` row carries the 0x318 stride.
- `17-Presentation-Rendering/Character-Render-Records/character-render-record-accesses.tsv` — a
  different record array; **not** the 0x318 one this operation indexes.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT and SERVICE.** Cited functions are called by the 2,001-byte core frame body (2) and core bodies of 79, 129, 237 and 404 bytes. They call core bodies of 7, 277 and 2,232 bytes.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT.** `FUN_0037b4d0`, owned by that layer, calls `002681D0` on this page. That caller is a 3,175-byte routine whose first act is to resolve its argument's `dword[+0]` through the image-base helper and abandon the call when that yields nothing; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — SERVICE.** `0022A770` on this page calls `FUN_0036f460`, owned by that layer. What it reaches is a float normalisation against 1.0 that keeps the previous value in the global at `02AD9B50` and steps by -1.0 until it is in range; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — SERVICE.** `00358BC0` on this page calls `FUN_002681d0`, owned by that layer. What it reaches is a 10-byte null guard that returns at once on a null argument and otherwise tail-jumps to the routine that follows it; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0022A770` on this page calls `PartyFocus_CommitPendingPackedActorHandle_Thunk`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00358BC0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**PlatformOnlineAchievements — SERVICE.** `0022A770` on this page calls `FUN_00316930`, owned by that layer. What it reaches is a 287-byte walk of the same `[022C2550]` table against the data at `01EED130`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — SERVICE (SWE2-CONTRACT 2026-09-15, 2 edges, R5-visible).** `0037B4D0` — the 3,175-byte
ActorEntity caller already accounted above — also calls Gameplay's
`WorldActor_GetDefinitionByte12OrMinus1` `002E9C00` and
`ActorHandle_GetPrimaryFormulaResourceByte26` `00321380`. Visible only once `0x`/`FUN_` citations
count; the crossing is the same caller's Gameplay callees.

**CombatAI — MECHANICAL (SWE2-CONTRACT 2026-09-15, 1 edge).** The just-cited `002E9C00` is called by
`AiOrder_EvaluateAndResolveActionTarget` `003014C0` — a stack-cookie-guarded evaluator with an
`0xAB8` frame that zeroes its out-parameter on entry (OPUS, read from the shipping bytes) —
fan-in imported by the Gameplay note, not a publish-path relationship. (`003014C0` itself
consults the CombatAction availability check — one further hop of the same fan-in.)

## The `001821F0`/`00182340` exclusive-subtree cluster — both roots bound (SWE2-FRONTIER, followup queue)

Two identical singleton-gated forwarders over `00189120` (the transform
singleton getter): non-null → re-fetch and tail-jump to the member;
null → silent return.

| root | member (forward target) | interior |
| --- | --- | --- |
| `001821F0` (36 B) | `00185A10` | [`0018220A`](../_index/ADDRESS-INDEX.md) |
| `00182340` (36 B) | `001860E0` | [`0018235A`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00189120`.

## SWE2-EC7-62 update (2026-09-19) - `0018CBC0`

`0018CBC0` (150 B) is a `+0x358`/`+0x690` queue body - `0018B4E0`/`001AB570`/`001F1E80`/`0085E730`. Interior anchor `0018CBE3` (a `0085E730` call).


## SWE2-EC7-75 update (2026-09-19) - `002ECA00` + `002E9810` + `002E97C0` element/handle helpers measured

`002ECA00` (36 B) is the SecondaryContext-element bit-4 setter: when
`rcx`, `[rcx+0xC0]`, and `[rax] != -1` all hold, `byte[rax+0x11]` is
masked `0xEF` then OR'd `(dl & 1) << 4` - the same protocol `00363AD0`
runs on `+8`.
Interior anchor `002ECA16` (the `and byte [rax+0x11]` mask).

`002E9810` (25 B) is the record handle pack: `([rcx+0x24] << 16) |
word[rcx+0x1A]` with bit 15 set - NULL `rcx` returns 0.
Interior anchor `002E9821` (the `bts eax, 0xF`).

`002E97C0` (68 B) is the matching verify: `ecx & 0x7FFF` must be under
0x80, indexes `0215FDA0` at `0x40` stride, rebuilds the same packed
handle from the record and returns the record only when it equals
`r8d` - the NameBindingEntry handle-check the publish bodies run.
Interior anchor `002E97F4` (the `bts edx, 0xF` rebuild).

## SWE2-EC7-93 update (2026-09-20) - `0036ECA0` + `0036EC10` measured

`0036ECA0` (54 B) is the nibble-indexed byte fetch `0037B4D0` calls
from the publish path: `ecx < 0` answers 0, otherwise `(ecx & 0xF) *
24` indexes the `011EA009` table and `cl & 0xF0` picks between the
`+0x21B9AE0` and `+0x21B9AB0` variants before the byte returns.
Interior anchor `0036ECBA` (the index computation).

`0036EC10` (63 B) is the same table walk turned destructive: the
nibble picks the same record, `cl & 0xF0` picks the same variant,
and the word at `+0x16` is decremented with a saturate-to-zero floor
instead of a byte being read.
Interior anchor `0036EC3D` (the `dec word [rax+0x16]`).

## SWE2-EC7-98 update (2026-09-20) - `002E49B0` measured

`002E49B0` (83 B) is the type-0x60 publish `0034A3F0`,
`0034A860`, `0037B4D0` and `0037CF00` call: `byte[rcx+3] &
0xE0 == 0x60` admits, `rdx = [rcx+0xC0]` then `[+0x138]` must
be non-null, `r8` defaults to `rdx+0x30` while `rdx+0x50` is
the second argument to `0026E530`, and the call's result bit
lands in `byte[+0xB]` bit 7 (`& 0x7F` then `al << 7` fold) -
the publish-and-flag the transform path runs per record.
Interior anchor `002E49EE` (the `0026E530` call).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Script_VM_Native_Bridge — CLIENT, 28 edges: script verbs reach the SecondaryContext element helpers.** The
element and handle helpers `002E97C0` (10 script callers) and `002E9810` (10) are called by script-VM verb handlers
in `0033F330`-`00346AA0`, as are the bit-4 setter `002ECA00`, the type-0x60 publish `002E49B0` and the
nibble fetches `0036EC10` / `0036ECA0`. `0034A860` pops its argument through `VMValueStack_PopNumericDiscard`. What
the verbs mean is the script VM's subject; the publish they reach is this contract's.

**Input, UI, Resource and WorldAreaField — MECHANICAL, sixteen edges through one frame body.** This page cites the
field frame `0022A770` for one fact: it calls the camera publish `00314370` at three sites. The same frame body runs
the rest of the frame:
- **the input rebuild**, 10 edges: `InputGameplay_RebuildFrameSnapshotFromChannelHistory`,
  `InputControl_SetOneShotFrameCallback`, `InputGameplay_RebuildRemappedTransitionMaskState` and the remapped history
  masks;
- **a UI body** `00254E50`;
- **a resource body** `00324510`;
- **`World_UpdateSimulationTick`**.

Its order belongs to `the-world-tick-and-the-field-frame`.

The other edges:
- **Resource.** The vector grow `001AB570` is also called by the asset-manifest parser `0019E7B0`.
- **WorldAreaField.** The 3,175-byte `0037B4D0` reads the field words `00377A90` / `00377DB0`, and
  `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`) reads `FieldData_GetActiveFieldRecordBit15`.

**RNG_Random_Selection — SERVICE, two edges.** `AiOrder_EvaluateAndResolveActionTarget` (`003014C0`), cited here as a
caller of `002E9C00`, also draws `RNG_SharedGameplayLCG_NextU32` and `BattleData_ResolveWeightedId`. That is AI target
selection using the shared generator, owned by the gambit and RNG pages.

*Tier 2: ledger names, sizes and `edges.tsv`, roles as this page and the cited pages read them; no new body read
(OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-contract-character-transform-publish-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0034A3F0` | 37 B | calls `0026AD40(rdx, 1)` and then tail-jumps `002E49B0(rdx, 0)` | `0034A3F9`, `0034A401`, `0034A406`, `0034A410` |
| `0034A860` | 137 B | calls `00267DB0(r9)` three times and builds a stack array of four floats holding the third result, the second result, the first result and 1.0 (`01CEBBA8`) in that order; calls `0026AD40(rdx, 1)` and then `002E49B0(rdx, &array)`, under the stack-cookie check of `01F44830` and `00808C40` | `0034A884`, `0034A890`, `0034A8B6`, `0034A8BF`, `0034A8CC` |
