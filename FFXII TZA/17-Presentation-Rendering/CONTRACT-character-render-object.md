---
contract: The character render object — one construction, a one-way ready latch, a double-buffered publish
category: 17-Presentation-Rendering
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: Character-Rendering/character-render-object.md
entries: ["001F4DA0", "001F51E0", "001F6E70", "001FB120"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-22 (FABLE) on this document's own citations, every
    one resolving into a known section of the authority image; and §4's invariants re-measured from
    the shipping bytes — every site loading the immediate `0x668`, every reference to the vtable,
    every access at `+0x4B4` split by ACCESS WIDTH, and the publish body's instruction, `movups` and
    backward-jump counts. **This records checks performed on that date, not the method of the
    original derivation**, which is on the render-object page; see §15.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-render-object-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# Contract — the character render object

> **Authored 2026-09-22 by FABLE.** S-38's binding gap is *"the render OBJECT has no contract — only
> one write into it does"*.
> [`CONTRACT-character-transform-publish.md`](CONTRACT-character-transform-publish.md) is
> `scope: operation` with **one** entry, and its subject is publishing a transform into the inactive
> half of a double buffer — *one write into the object rather than the object*.
>
> Written against FRONTIER's adequacy test: *a narrower contract is adequate exactly when the
> system's operations have no cross-operation invariant or ordering it leaves unstated.* §4 is seven
> such invariants, and the first four are about the object's whole life rather than any one write.

## 1. Purpose

Hold everything the renderer needs about one character — its record array, its material list, its
view parameters and its published transforms — from a single construction to a single destruction,
and refuse to do any of it until setup has finished.

## 2. Interface

| | body | size |
|---|---|---:|
| construct | `CharacterRenderObject_Construct` (`001F4DA0`) | 516 B |
| destruct / teardown | `001F51E0` | — |
| finish setup (sets the latch) | `001F6E70` (vtable slot 2) | 2,328 B |
| publish the transform | `001FB120` (vtable slot 13) | 496 B |

Allocation: `mov ecx, 0x668` at `001BD527`, then `001F4DA0`. **1,640 bytes, one site.**

## 3. Types

The layout is on [the render-object page](Character-Rendering/character-render-object.md) §4 and is
not restated. The three fields this contract is about:

```
+0x058 / +0x060 / +0x068   the record-array vector — elements of 0x318 bytes
+0x4B4                      BYTE — the ready latch
+0x4C4 .. +0x583            transform bank A — three 4x4 matrices
+0x584 .. +0x643            transform bank B — three 4x4 matrices
```

## 4. Preconditions · postconditions · invariants

### The seven cross-operation invariants

**R-1 — One construction site, and allocation and deallocation agree on the size.** Exactly **three**
sites in the image load the immediate `0x668`: the allocation at `001BD527`, the **sized
`operator delete`** in the deleting destructor at `001F5309`, and one unwind funclet at `00897C19`
which is banned as evidence. *The object cannot be allocated at one size and freed at another, and
that is checked rather than assumed.*

**R-2 — The class is identified by exactly two vtable references.** `00903B68` is referenced by
`001F4DA0` and `001F51E0` and by nothing else in the image. **So construction and teardown are the
class's whole identity surface**, and any other body that handles one of these objects received the
pointer. *(OPUS block 353 measured that after the teardown `001F51E0` the object carries the base vtable `00906D10`,
not the class's `00903B68`. R-2's two references still hold.)*

**R-3 — `+0x4B4` is a ONE-WAY ready latch, and the claim is only safe because of ACCESS WIDTH.**
Cleared to zero in the constructor (`001F4EC9`, `mov byte ptr [rdi + 0x4b4], sil` with `esi` zeroed
at `001F4DDF`) and set to one exactly once (`001F7729`, `mov byte ptr [r8 + 0x4b4], 1`) at **+2,233
of a 2,328-byte method** — the very end of setup. **Nothing ever clears it back.**

> **The discriminator, stated because it is what makes the invariant true.** Sweeping the whole
> image at that displacement returns **13 writes**, which would refute "written twice". Eleven of
> them are `word`, `dword` or `movss` stores on **unrelated structures that happen to have a field at
> `+0x4B4`**. Exactly **two are byte-width**, and they are the two above. *A displacement sweep that
> does not record the width would report this latch as written thirteen times by eleven functions.*

**R-4 — Seventeen byte-width reads in sixteen functions, and the latch is consulted two different
ways.** ~~Twelve read it in their method's first instructions as an **entry precondition**; slot 16
reads it at instruction 118, **inside a submission loop, as one term of a per-element skip test**.~~
*Restated 2026-09-26 (FABLE, Claude Opus 5.5), on `OPUS-NOTE-FABLE-S38-R4-READERS-MEASURED`. OPUS executed the
readers (`candidates/s38-opus-replay-render-object/r4.py`), and the points below were re-read here from the bytes.
The sixteen readers split four ways:*
- **Thirteen gate at entry.** Eleven are vtable methods (slots 3, 8, 9, 10, 12, 13, 14, 19, 20, 24, 30). The other two
  are the non-virtual `001F89E0` (ResetState) and `001FAD50`. `001F89E0` stores `edx` to `+0x480` at `001F89E7`
  before its test, so with the latch clear it still writes the object once. *(corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: slot 24 has the same
  shape. With `edx` non-zero it stores 1 to byte `+0x230` of a singleton it fetches, at `001FA1C2`, before its latch test
  at `001FA1C9`.)*
- **One does not gate.** Slot 27's getter `001F86D0` returns the byte and branches on nothing.
- **One gates late.** The frame-side reader the page names reads the latch only after three lookups and a scene test.
  A second read in the same body guards a `+0x4B5` clear.
- **Slot 16 uses it per element.** The latch is one of two per-element terms; the other is ~~the record's `+0x10` bit 0~~
  *(corrected 2026-09-27, FABLE, Claude Opus 5.5, BB-1: `+0x10` bit 0 of the object the record holds at `+0x00`, loaded at `001FA5DA`)* (`001FA5DE`). Both are bypassed when the mode word is 2 (`001FA5BC`–`001FA5C1`), which is the emit path.
*The same byte is a "may I run at all" and a "may I emit this element", and an implementation that
hoists the second into an entry check changes what is drawn.*

**R-5 — The transform publish is double-buffered into two contiguous, equal, adjacent banks, and
this object does not choose between them.** Bank A begins at `+0x4C4`, bank B at `+0x584`;
`0x584 − 0x4C4 = 0xC0`, exactly three 64-byte matrices, so the banks are the same size and abut.
The selecting byte is reached through a shared accessor (`001FB1AC` then `cmp byte ptr [rax + 0x1c], 0`).
**Which bank is current is decided outside this object**, so the publish is a write into whichever
half it is told, never a swap. *(Named 2026-09-25, FABLE, Claude Opus 5.5, on [OPUS block 353](../_index/candidates/s38-opus-replay-render-object/README.md): the selector is byte
`+0x1C` of the singleton `[01F7F598]`, returned by the one-instruction accessor `00189120`. The publish also stores a
per-bank float pair into the record-array element: `+0x8` / `+0x10` for bank A, `+0xC` / `+0x14` for bank B.)*

**R-6 — The publish has no loops at all.** `001FB120` is 105 instructions, **48 of them `movups`**,
with **zero backward jumps** — twelve 16-byte moves per bank, fully unrolled, plus the scalars.
*Three source pointers and three destinations, written straight through.*

**R-7 — When the latch is clear the publish writes NOTHING, and the previous contents of both banks
stand.** `001FB126` reads the latch and `001FB13A` returns on zero, before any store. **A
not-yet-ready character does not publish an identity transform or a zeroed one — it publishes
nothing, and whatever the banks last held is what the renderer reads.** *This is the invariant most
likely to be lost in a reimplementation that initialises its buffers defensively.*

## 5. State

**Owned for the object's whole life:** the four vectors and their allocators, the two transform
banks, the view parameters and the latch. **Set once, never reset:** `+0x4B4`. **Written by others,
read here:** the bank-selecting byte, reached through the shared accessor.

## 6. Relationships

| | |
|---|---|
| **Sibling** | [`CONTRACT-character-transform-publish.md`](CONTRACT-character-transform-publish.md) — the *operation* R-5 and R-6 describe; this contract is the object it writes into |
| **Sibling** | the render-record pool lifecycle and the coast-down latch contracts, which cover the *other* S-38 page |
| **Upstream** | whatever calls the allocation at `001BD527` — one site |

## 7. State transitions

`allocated → constructed (latch 0) → set up (latch 1, one way) → destroyed`. There is no
`ready → not ready` edge anywhere in the image. Per publish: `latch clear → return` or
`latch set → write one bank`.

## 8. Script · resource · event interactions

None directly; the object's contents come from the record array and material list it holds, which
other systems fill.

## 9. Determinism

Deterministic. No generator is drawn in the construction, the setup or the publish.

## 10. Failure paths and edge conditions

- **Allocation failure skips construction** (`001BD539` jumps past the constructor), so the caller
  holds a null and the object is simply absent.
- A publish on a not-ready object is a no-op (R-7), not an error.
- Slot 16's per-element test can skip individual elements while the object as a whole is ready.

## 11. Observable behaviour

A character that has been created but not finished setting up is not drawn wrong — it is not drawn
at all, and anything already in its transform banks stays there until setup completes.

## 12. Reproduction formula

Construct, assert `+0x4B4 == 0`, call the publish and assert **both banks are byte-identical to
before**. Run setup, assert the latch is 1, publish, and assert exactly one bank changed and the
other did not. Then assert no code path returns the latch to 0.

## 13. Runtime validation

~~**None.** No experiment executes these four bodies. S-38's runtime cell is not addressed by this
contract.~~ **Superseded 2026-09-25:** [OPUS block 353](../_index/candidates/s38-opus-replay-render-object/README.md) executed the constructor, the transform publish and the teardown
(6/6). The evidence class is native replay, not live. *The historical note continues:* *Stated rather than left blank so a CONTRACT READY header is not read as evidence of
execution.*

## 14. Unresolved

- What the bank-selecting byte at `+0x1C` of the shared accessor's result is, and who writes it.
- The extent of the embedded object at `+0x3E0`.
- ~~Which of the sixteen latch readers are vtable slots and which are not — the page's list of thirteen
  is the vtable's, and the image-wide byte sweep finds sixteen.~~ *Answered 2026-09-26 in R-4: twelve are vtable slots
  (eleven gates and slot 27's getter), and slot 16 makes thirteen. The non-virtual readers are `001F89E0`, `001FAD50`
  and the late frame-side reader.*

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| R-1 — three `0x668` sites, allocation and sized delete agreeing | every site loading that immediate, enumerated image-wide; `001BD527`, `001F5309`, and one unwind funclet | 1 |
| R-2 — exactly two vtable references | rip-relative sweep for `00903B68` across every function body | 1 |
| R-3 — two byte-width writes against thirteen at the displacement | the same sweep split by access width; **the eleven non-byte writes are listed so the discriminator can be checked** | 1 |
| R-3's position | `001F6E70` is `0x918` = 2,328 bytes and the write at `001F7729` sits at +2,233 | 1 |
| R-4 — seventeen byte reads in sixteen functions | the byte-width sweep's read side | 1 |
| R-5, R-6 — the banks and the unrolled publish | `0x584 − 0x4C4 = 0xC0`; `001FB120` counted: 105 instructions, 48 `movups`, 0 backward jumps | 1 |
| R-7 | `001FB126` / `001FB13A` precede every store in the body | 1 |
| The object layout and the slot table | [the render-object page](Character-Rendering/character-render-object.md), falsified once 2026-09-02 | 1 |

## 16. Parity plan

L3 is out of scope. A reimplementation is judged on R-1 through R-7. **R-7 is the one to test first**:
a not-ready publish must leave both banks untouched, which a defensively-initialised buffer would
violate without any visible error.

## 16a. Crossings into other layers (FABLE, 2026-09-22)

- **Presentation — internal.** All four bodies are this category's own.
- **Every other layer reached is MECHANICAL**, through the constructor's and the publish's own
  callees — the allocator, the shared accessor and the vector allocators. *Their addresses are
  deliberately not cited: each is a hub, and naming one imports its whole edge set for a one-line
  remark.*

## 17. Related

- [The character render object](Character-Rendering/character-render-object.md) — the mechanism
- [Contract — character transform publish](CONTRACT-character-transform-publish.md) — the operation
- [The character render record array](Character-Render-Records/the-character-render-record-array.md) — S-38's other page

## Falsification pass 1 — 2026-09-29 (OPUS): every invariant survives

**Attack.** §2's sizes (against their `.pdata` chain unions), R-1 to R-7 became checks. The displacement censuses decode
every function to the larger of its catalogue size and its chain union, so the catalogue's short tails are included.
Script: `Tools/analysis-kit/gfz-scripts/falsify_render_object.py`, output `falsify_render_object.out`, image `73461d08…`,
0 BROKEN, exit 0. R-4's four-way split is OPUS block 353's execution plus FABLE's re-read, and was not re-classified;
its counts were re-measured.

| # | Clause attacked | Result |
|---|---|---|
| O0 | §2 | **survives**: 516 / 2,328 / 496 B, each equal to its chain union |
| O1 | R-1 | **survives as worded**: exactly three instructions *load* `0x668` (`001BD527`, `001F5309`, `00897C19`). Two unrelated arithmetic uses (`00210843 add`, `0055C6D3 adc`) are not loads |
| O2 | R-2 | **survives**: `00903B68` is referenced only from `001F4DA0` and `001F51E0`, on both instruments |
| O3 | R-3 | **survives**: 13 stores at `+0x4B4` image-wide (2 byte, 4 word, 7 dword); the byte-width two are the clear and the set at +2,233 |
| O4 | R-4 | **survives**: 17 byte-width reads in 16 functions |
| O5 | R-5 | **survives**: banks `0xC0` apart; the selector is byte `+0x1C` of the singleton `[01F7F598]`, returned by the one-instruction accessor `00189120` |
| O6 | R-6 | **survives**: 105 instructions, 48 `movups`, no backward jump |
| O7 | R-7 | **survives**: the latch read and the `je` precede the first store |

No correction.
