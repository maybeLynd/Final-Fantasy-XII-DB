---
system: How a Phyre class registers its array members and its annotations
category: 22-Middleware-PhyreEngine
status: AUDITED — SD-61, SD-62, SD-63 and UQ-281 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — +0x58/+0x5C are the element size and the array kind (UQ-281, reconciled 2026-09-30); SD-61 answered 2026-09-30 (OPUS `73e6ff01f`; AUDIT-SEM review `auditsem-review-dd-owner-read-2-0930` §3), SD-62 answered 2026-09-30 (SWE2-ORACLE `dedfaf0d7`, after OPUS's `e2777d3c8` narrowing: the root's two lists and the class-name hash tree), SD-63 answered 2026-09-30 (OPUS `ce6a553b2`: the scene-wide shader parameter table and its constant-buffer layout); both PAnnotation destructors read (006B6750 on the page, 006B6780 on 2026-09-18: a 0x30-byte object) (status line current 2026-09-30, SWE2-DATA)
owner_layer: Phyre — from the ledger, not inferred from callers
evidence_tier: 1
level: L1
readiness: SIGNATURE RESOLVED
confidence: PROVEN
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 64 addresses cited - 18 data, 33 entry, 13 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-08
falsification_passes: 1
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-phyre-reflection-pass-1
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-phyre-reflection-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# How a Phyre class registers its array members and its annotations

## 1. What the player sees

Nothing, directly — and that is the honest answer for this one. What a player sees *indirectly* is
that FFXII's authored content works at all: every table the game loads, every field an editor could
set, every value a tool could read back, exists because the engine carries a description of its own
types at runtime. A class says *"I have a field called this, of that type, at this offset"*, and the
loaders, savers and inspectors all read that description rather than hard-coded layouts.

This page covers two of the small pieces that description is built from — **an array-valued member**
and **an annotation** — and one family of machinery that hands them out.

## 2. Why these three, and not something else

`EL-1` lists the largest genuinely uncited high-connectivity functions: nodes with many callers that
no document mentions. Ranked by **distinct non-EH callers** among Phyre-owned functions, the top of
that list is:

| entry | body | callers | what it is |
|---|---:|---:|---|
| `00632A10` | 91 B | **124** | `Phyre::PClassDataMemberArray` construction |
| `006B6750` | 36 B | ~~**71**~~ **1** | `Phyre::PAnnotation` destruction — **corrected 2026-09-13, §9** |
| `006B66C0` | 37 B | **70** | `Phyre::PAnnotation` construction |
| `0062FF50`, `0062FFC0`, `00630030`, `006300A0`, `00630110`, `00630260`, `006302D0` | 98 B each | 26–52 | **seven lazy-static accessors**, §5 |

> **One row of that table is wrong (2026-09-13, §9).** `006B6750` has **one** caller in the
> whole image, not 71. It does not belong on a high-connectivity ranking at all, and `EL-1`
> should not have offered it as one. The other rows reproduce exactly.

*(Caller counts exclude edges whose source is an unwind funclet or catch handler. Identity comes from
MSVC RTTI: each constructor installs a vtable, and `rtti_recover.py` resolves that vtable's first
slot to a class. The binary names its own types; nothing here is inferred from a caller.)*

## 3. `00632A10` — an array member is a plain member plus two numbers

```c
/* Phyre::PClassDataMemberArray::PClassDataMemberArray(this, a2, a3, a4, a5, a6, a7, a8) */
Phyre_Reflection_DataMemberRegistration(this, a2, a3, a4, a5, a6, a7, /* a8 */ 0);  /* 00632960 */
this->vtable   = &PClassDataMemberArray_vtable;    /* 00D58100 */
this->[+0x5C]  = a7;                               /* the SAME value the base also received */
this->[+0x58]  = a8;                               /* consumed here; the base was passed 0 */
return this;
```

Three things a reimplementation must get right, and only the last is guessable:

1. **It is a base call plus a vtable swap.** The base is `00632960`, already named
   `Phyre.Reflection.DataMemberRegistration` (165 B) — the routine that builds an ordinary
   `Phyre::PClassDataMember`. The array form runs the ordinary registration first and then
   *overwrites* the vtable pointer at `+0x00`, which is the standard shape of a derived constructor.
2. **`a7` is forwarded and kept.** It goes to the base as its seventh argument **and** is stored at
   `+0x5C`. It is not one or the other.
3. **`a8` is intercepted.** The caller's eighth argument is stored at `+0x58`, and the base is handed
   a literal **`0`** in that slot instead. So the base never sees it.

The argument arithmetic, since it is easy to get wrong: the function does `push rdi` then
`sub rsp, 0x40`, so on entry `a5`…`a8` sit at `[rsp+0x70]`, `[rsp+0x78]`, `[rsp+0x80]`, `[rsp+0x88]`,
and they are re-laid at `[rsp+0x20]`…`[rsp+0x38]` for the call.

~~**What `+0x58` and `+0x5C` mean is not established.** They are two 32-bit values that distinguish an~~
~~array member from a scalar one — element count and stride are the obvious guess and are **not~~
~~claimed**.~~ *(Corrected 2026-09-30, SWE2-DATA: `UQ-281` (FABLE, 2026-09-17) answers both. `+0x5C` is the array kind: 1 is a fixed-size C array, set by the fixed-size subclass; 2 a dynamic array through a pointer; 3 a `PArray`; 4 a `PSharray`. `+0x58` is the element size. Across all 165 call sites, `a7` is 3 at 86, 2 at 70 and 4 at 9. `a8` is 8 at 113, 4 at 36, 1 at 7, 2 at 6 and `0x10` at 3. No slot of the class's own vtable reads either field; the animation-channel binder reads `+0x5C` (`UQ-281`). `_index/candidates/dd-data-2-0930/array_member_args.py` M1–M3, C1.)*

## 4. `Phyre::PAnnotation` — a list node with three fields

The pair is a constructor and a destructor of one class. ~~which is why their caller counts are 70
and 71 rather than one being a variant of the other.~~

> **Corrected 2026-09-13 (§9): the counts are 70 and *one*.** The constructor's 70 reproduces
> exactly; the destructor has a single caller in the entire image — `005AABBF`, inside
> `FUN_005AABB0`. The identification of the pair stands on RTTI, not on the counts, and
> everything this section says the two *do* reproduces instruction for instruction. What the
> corrected numbers show instead is an asymmetry worth stating: **70 constructions against one
> destruction.**

### `006B66C0` — construct

```c
/* Phyre::PAnnotation::PAnnotation(this, a2, a3, a4) */
Node *n   = (Node *)((char *)this + 0x08);
n->next   = n;                                   /* an EMPTY circular list, pointing at itself */
n->prev   = n;
this->vtable  = &PAnnotation_vtable;             /* 00D80930 */
this->[+0x18] = a2;                              /* qword */
this->[+0x20] = a3;                              /* qword */
this->[+0x28] = (uint32_t)a4;                    /* dword */
return this;
```

**`+0x08` is an intrusive circular doubly-linked list head**, self-linked on construction. That is
the whole reason the destructor exists.

### `006B6750` — destruct

```c
/* Phyre::PAnnotation::~PAnnotation(this) */
Node *n = (Node *)((char *)this + 0x08);
this->vtable = &PAnnotation_vtable;              /* re-installed, as MSVC does at a dtor's head */
n->next->prev = n->prev;                         /* unlink from whatever list it joined */
n->prev->next = n->next;
n->next = n;                                     /* and leave the head empty again */
n->prev = n;
```

**It unlinks and then re-empties.** Re-emptying after unlinking is not redundant here: it leaves the
node in the same state the constructor produced, so a destroyed annotation is indistinguishable from
a fresh one.

> **The vtable's slot 0 is `006B6780`, not `006B6750`.** On MSVC x64 slot 0 of a polymorphic class is
> the *scalar deleting destructor*, so `006B6750` is a non-virtual destructor reached by a direct
> call. ~~That is consistent with its 71 callers and is why it appears in the call graph at all.~~
> **Corrected 2026-09-13 (§9):** it appears in the call graph because of **one** call, and
> `006B6780` is reached only through the vtable — it has **no** direct call site anywhere in
> the image.

## 5. The seven 98-byte functions are machinery, not behaviour

> **There are fifteen of them, not seven (2026-09-13, §9).** The seven below are the seven that
> cleared `EL-1`'s caller threshold; this section's own shape test — 98 bytes, calls `008092FC`
> — returns **fifteen** on one contiguous run of guards, and the shape claim is true of all
> fifteen.

`0062FF50`, `0062FFC0`, `00630030`, `006300A0`, `00630110`, `00630260` and `006302D0` are 98 bytes
each, sit in one tight range, and **every one of them calls `008092FC`** — `_Init_thread_header`, the
magic-static guard documented in
[lazy statics and the one-time init lock](../../24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md).

They are **lazy-static accessors**: each guards one reflection singleton and returns it. Their 26–52
callers are that singleton's consumers, not evidence of seven distinct behaviours.

**Disposition C — proven implementation machinery.** The upstream is named (`_Init_thread_header`),
the boundary is stated: *which* singleton each one returns is **not** established here, and the shape
was established from the shared callee, not from reading all seven bodies.

## 6. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00632A10` | `Phyre::PClassDataMemberArray` constructor | 91 B | base call, vtable swap, `+0x58`/`+0x5C` |
| `00632960` | `Phyre.Reflection.DataMemberRegistration` | 165 B | builds the ordinary `Phyre::PClassDataMember` |
| `00D58100` | `Phyre::PClassDataMemberArray` vtable | — | slot 0 = `00633FB0`; RTTI locator `01D14A68` |
| `006B66C0` | `Phyre::PAnnotation` constructor | 37 B | self-links `+0x08`, stores `+0x18`/`+0x20`/`+0x28` |
| `006B6750` | `Phyre::PAnnotation` destructor | 36 B | unlinks, then re-empties the head |
| `00D80930` | `Phyre::PAnnotation` vtable | — | slot 0 = `006B6780`; RTTI locator `01D33110` |
| `006B6780` | `Phyre::PAnnotation` scalar deleting destructor | 68 B | read 2026-09-18 (FABLE): stores the vtable `00D80930`, unlinks the intrusive node at `+0x08` and self-links it (the non-virtual destructor `006B6750` inlined, `006B678D`–`006B67A8`), then `free`s **0x30 bytes** when bit 0 of `edx` is set (`006B67AC`–`006B67B6`) — so a `PAnnotation` is a 0x30-byte object |
| `0062FF50`–`006302D0` | seven lazy-static accessors | 98 B each | all call `008092FC` |
| `008092FC` | `_Init_thread_header` | 103 B | the magic-static guard |

## 7. What this document does not establish

- ~~**What `+0x58` and `+0x5C` of an array member hold.** Two 32-bit values, written from `a8` and `a7`.~~ *(Answered: the element size and the array kind, `UQ-281`; §3. SWE2-DATA 2026-09-30.)*
- ~~**What `+0x18`, `+0x20` and `+0x28` of an annotation hold**, or what an annotation annotates. The constructor stores its three arguments there (`rdx`, `r8`, `r9d`); none of the 70 call sites forms them next to the call.~~ *(`SD-61` answered 2026-09-30, OPUS `73e6ff01f`: an annotation is key `+0x18` — a static `{name,0}` object naming **"WriteMask"** at the 69 sites — value type `+0x20` (`PTypeDefault<unsigned int>`), `+0x28` = 0, and value `+0x30` = `0x7FFFFFFF`, linked into the annotated member's list at member `+0x38`. All 69 sites follow a `m_count` member registration through `00632960`; the 70th is the generic `PAnnotationWithValue<unsigned int>` helper `006315B0`. The "no call site forms the arguments" claim was wrong — the key is BL-5's, read by `006B67F0`. The classes themselves and who applies `WriteMask` are not named.)*
- **Which singleton each of the seven accessors returns.** Only that all seven are that shape.
  *Narrowed 2026-09-13 (§9):* there are **fifteen** accessors, their guards are a contiguous run
  of dwords `02CF94EC`…`02CF9524`, and each returns a distinct element of **one `0x50`-stride
  array** at `01F2E330`…`01F2E780`. **None of them constructs anything** — the cold path is
  `_Init_thread_header`, **`atexit`** (`00808B90`, already named in the function list) with its
  own 15-byte thunk, and `_Init_thread_footer`. The objects are zero-initialised and only
  their teardown is generated, which is why no accessor names its type. The open question is
  now **what one `0x50`-byte element is**, not which of seven unrelated globals each returns.
  *Answered 2026-09-14 (FABLE): thirteen of the fifteen elements are Phyre type objects, and they are **not**
  zero-initialised.* The image's `.data` already holds each one's vtable, a self-linked node at `+0x08`–`+0x18`, a
  name pointer at `+0x30` and a `u32` size and alignment at `+0x38`/`+0x3C`, so an accessor has nothing to construct.
  MSVC RTTI on the vtables names them:
  - `01F2E370` is `Phyre::PType` itself (vtable `00D31168`, size `0x50`);
  - the other twelve are `Phyre::PTypeDefault<T>` scalars. RTTI read for `bool` (`00D58A18`), `PChar` = `char`
    (`00D58A68`), `PUInt32` (`00D311B0`), `double` (`00D58CF0`) and `PUInt128` = `PQWord` (`00D58D40`); the other
    seven share the layout, with names `PUInt8`, `PInt16`, `PUInt16`, `PInt32`, `PUInt64`, `PInt64` and `float`
    read from `+0x30`.
  
  The class nests `PTypeDefault<T>` : `PType` : `PHashEntryConst` : `PRedBlackTreeNode` (at `+0x08`) : `PMemoryBase`.
  Each 15-byte teardown `008AFE00`… is the inlined destructor: `lea rax, [00D31168] ; mov [record], rax ; ret`, which
  restores `PType`'s vtable. The two remaining elements, `01F2E330` (accessor `006373D0`) and `01F2E780` (`00637440`),
  are not type records ~~and their cold paths were not read~~ *(their cold paths are only `atexit` registration —
  each is a list-headed static object; `SD-62` narrowed 2026-09-30, OPUS `e2777d3c8`: `01F2E330` is the root the
  384/385 class descriptors are built against — `00632D80` stores it at each new descriptor's `+0x70`; `SD-62` answered 2026-09-30, SWE2-ORACLE `dedfaf0d7`, [`sd62-registry-list-links-0930`](../../_index/candidates/sd62-registry-list-links-0930/README.md): the root chains class descriptors on its `+0x10` (descriptor node `+0x50`, inserter `00639160`) and non-root owner objects on its `+0x28` (node `+0x00`), and `01F2E780` is a 0x30-byte name-hash tree of class descriptors (node `+0x08`, key `+0x20` hash / `+0x28` name; insert `006388C0`, remove `00638F00`). The `PWorld` / `"getInstanceCount"` slots after it belong to a separate method record at `01F2E7B0`, linked into `PWorld`'s descriptor `+0x90` list by `00635B80`, not to `01F2E780`)* (**`SD-62`**, SWE2-DATA 2026-09-30). The twelve scalar types key Phyre serialization's 12 × 12
  conversion tree ([image hardening, the 145 teardowns](../../24-Compiler-And-CRT-Runtime/Binary-Hardening-And-Hooking/image-hardening-cfg-aslr-dep-and-stack-cookies.md)).
- **Any runtime observation.** Every claim is static disassembly at the certified hash, plus RTTI
  read out of the same image.
- **That these are the only high-connectivity uncited Phyre nodes.** They are the top of one ranking;
  `EL-1` also names `0026EE00`, `002432B0`, `005CDAA0` and `0019C5D0`, which are **not** Phyre-owned
  and are untouched here. *(Corrected 2026-09-08: of those four, **`0026EE00` and `002432B0` were already
  documented** — by the shared-transform-workbench pages and by [a typed list measured once](../../02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md) respectively.
  `EL-1`'s list was stale when this was written. The other two are now documented in [the formatted log
  call](../../00-Engine-Core-Runtime/Diagnostics-Logging/the-formatted-log-call-and-its-level-gate.md).)*

## 8. Falsification checklist

- [x] **`00632A10` constructs `PClassDataMemberArray`.** *Killer:* a different class behind
      `00D58100`. Its slot 0, `00633FB0`, resolves through MSVC RTTI to `Phyre::PClassDataMemberArray`.
- [x] **`a8` does not reach the base.** *Killer:* the base receiving it. `[rsp+0x38]` is written the
      literal `0` at `00632A28`, before the call.
- [x] **`+0x08` of an annotation is a self-linked list head.** *Killer:* either store pointing
      elsewhere. `mov [rax], rax` / `mov [rax+8], rax` with `rax = rcx + 8`.
- [x] **`006B6750` is a destructor, not a variant constructor.** *Killer:* it initialising rather than
      unlinking. It reads `next` and `prev` and splices them together before resetting.
- [x] **The seven are lazy-static accessors.** *Killer:* any of them not calling `008092FC`. All seven
      do.

> **Killers run 2026-09-14 (FABLE); all five hold.**
> - `00632A10` stores `lea rax, [00D58100]` into `[rdi]` at `00632A55`. Slot 0 there is `00633FB0`, and the complete
>   object locator `01D14A68` names `.?AVPClassDataMemberArray@Phyre@@` (8 base classes).
> - `a8` does not reach the base. `[rsp+0x38]`, the base call's eighth argument, is the literal `0` (`00632A28`).
>   The caller's `a8` (`[rsp+0x88]`) is stored at `+0x58` only after `00632960` returns (`00632A58`–`00632A5F`).
> - The self-linked head: `006B66C0` does `lea rax, [rcx+8] ; mov [rax], rax ; mov [rax+8], rax`, then the vtable.
> - `006B6750` resets the vtable to `00D80930`, splices `next` / `prev` together (`006B675E`–`006B6769`), and
>   self-links the node again. That is an unlink, not a construction.
> - All seven 98-byte accessors (`0062FF50`, `0062FFC0`, `00630030`, `006300A0`, `00630110`, `00630260`,
>   `006302D0`) contain `call 008092FC`.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md)'s 2026-09-13 amendment. It returned
`EL-1`, which is this page's own selection input and is where the defect below lives.)*

§8 is a falsification checklist with named killers. Every killer was run.

### The reading reproduces, instruction for instruction

| checklist item | killer | result |
|---|---|---|
| `00632A10` constructs `PClassDataMemberArray` | a different class behind `00D58100` | `lea rax, [rip + 0x7256B3]` at `00632A46` resolves to **`00D58100`**; its slot 0 is **`00633FB0`**, its locator **`01D14A68`**, and the type descriptor spells **`.?AVPClassDataMemberArray@Phyre@@`** |
| `a8` does not reach the base | the base receiving it | `00632A28  mov qword ptr [rsp + 0x38], 0` — written **before** the call, exactly as claimed |
| `+0x08` is a self-linked list head | either store pointing elsewhere | `lea rax, [rcx + 8]` / `mov [rax], rax` / `mov [rax + 8], rax` |
| `006B6750` is a destructor | it initialising rather than unlinking | it reads `[rdx]` and `[rdx + 8]`, splices them, then re-empties |
| the seven are lazy-static accessors | any not calling `008092FC` | all seven do, all are 98 bytes, and `008092FC` is **103 bytes**, as §6 says |

The stack arithmetic §3 offers "since it is easy to get wrong" is right: `a5`…`a8` at
`[rsp+0x70]`, `[rsp+0x78]`, `[rsp+0x80]`, `[rsp+0x88]`, re-laid at `[rsp+0x20]`…`[rsp+0x38]`.
`+0x5C` takes `a7` (through `ebx`, `00632A4D`) and `+0x58` takes `a8` (`00632A5F`). The `PAnnotation`
vtable is `00D80930` from both `006B66CB` and `006B6754`, its slot 0 is `006B6780`, its locator
`01D33110`, and its type descriptor spells **`.?AVPAnnotation@Phyre@@`**. The caller counts
**124** for `00632A10` (over **165** sites — the page says *callers*, and means it) and **70** for
`006B66C0` reproduce, and so does §5's 26–52 range: **26, 27, 27, 39, 47, 50, 52**.

### ⚠ The destructor has one caller, not 71

Scanning the **whole of `.text`** for a `rel32` call to `006B6750` — not just listed function bodies,
because unwind funclets are exactly the code a listed-body census would miss:

| | sites | inside a listed body | outside every listed body |
|---|--:|--:|--:|
| `006B66C0` constructor — **the control** | **70** | 70, in 70 distinct functions | 0 |
| `006B6750` destructor | **1** | 1 — `005AABBF`, in `FUN_005AABB0` | **0** |

> **The instrument reproduces the row beside the one it refutes**, which is what makes the refutation
> readable. And the address occurs **nowhere in the image as a qword or as a dword RVA** — so it is in
> no vtable and no unwind table either. There is no population of 71 anywhere to be found.

It is not the deleting destructor's count borrowed by mistake: **`006B6780` has *no* direct call site
at all** (one qword reference, its own vtable slot). Two sentences rest on the 71 and both fail —
*"which is why their caller counts are 70 and 71"* and *"that is consistent with its 71 callers and
is why it appears in the call graph at all"*. It appears because of one call.

**What survives is everything the section actually reads.** The identification is RTTI, not
connectivity, and the unlink-then-re-empty reading is exact. The correction is to the *reason for
reading it*: `EL-1` offered it as the second-busiest uncited Phyre node, and it is not busy at all.
The genuine finding in the numbers is the asymmetry — **70 constructions, one destruction.**

### ⚠ The accessor family is fifteen, not seven

§5's own shape test — **98 bytes and a call to `008092FC`** — was swept over every listed function.
It returns **17** image-wide, and **fifteen** of them form one series:

* their guards are the **contiguous** dword run `02CF94EC`, `02CF94F0`, … `02CF9524` — fifteen
  values, no gaps;
* each returns a distinct element of a **`0x50`-stride array** at `01F2E330`…`01F2E780`; *(2026-09-30, SWE2-ORACLE [`sd62-registry-list-links-0930`](../../_index/candidates/sd62-registry-list-links-0930/README.md): from `01F2E780` up the objects do not follow that stride - `01F2E780` is 0x30 bytes and `01F2E7B0` a separate record of about 0x28 bytes; the rest of the array was not re-read)*
* each registers **its own** 15-byte `atexit` thunk, on a `0x10` stride: `008AFE00`, `008AFE10`, …
  `008AFEC0` for the twelve in the main band.

The eight the page does not name are `00630180`, `006301F0`, `00630340`, `006303B0`, `00630420`,
`00630490`, `006373D0` and `00637440`. **They are the same machinery with fewer callers** — so
"the seven 98-byte functions" is a fact about `EL-1`'s threshold, not about the code. (The other two
of the 17, `005CD9C0` and `006372B0`, sit outside the guard run and are not claimed as part of it.)

> **Crossing into Presentation — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `006372B0` has the same thread-safe static
> shape but guards a different object. Its guard is `02CF9404`, it registers `008AF500` with `atexit`, and it returns
> the static at `01F2E0D0`. That static's first quadword is `00D26BE0`, whose RTTI names
> **`Phyre::PClassLayoutInterface`**. It has 7 raw callers. One of them is a 703-byte body that the ledger
> files under Presentation (called at `00608DA2`). That body first runs a loop rewriting the `+0x08` / `+0x0A` words of
> 24-byte records (`005FD320`–`005FD3A7`). It then fetches the layout interface at `005FD3AD` and passes it to
> `005FD700` as the fifth argument. The class-layout service is therefore consumed by rendering-side record layout as
> well as by registration. ~~What that body lays out is not read~~ *(`SD-63` answered 2026-09-30, OPUS `ce6a553b2`:
> the body `005FD2A0` builds **Phyre's scene-wide shader parameter table** — 23 named entries (`00D3EB38`, name +
> two dwords) into 24-byte records at `02CB7DA8`, names pooled at `02CBC390`, the dwords as bytes `−6`/`−5`, `+0x08`
> cleared, `+0x0A` cut to top 3 bits — and `005FD700` lays out its constant buffer (size rounded to 16 at `02CB8458`,
> `size × even-instance-count` buffer zeroed at `02CB8460`). The entries are the per-scene parameters: camera
> (`EyeDirWS`, `EyePosWS`, `Proj`, `View*`, `ViewProj`), clip/viewport (`NearFarPlane`, `AspectRatio`,
> `ViewportWidthHeight(Inv)`, `ScreenWidthHeight(Inv)`), `GlobalAmbientColor`, `Time`, and the resource bindings
> (`DitherNoiseTexture`, `LowResDepthTexture`, `RWDeferredLightBuffer`, `RWCapturedTriangleBuffer`,
> `SceneWideParameterConstantBuffer`)* (**`SD-63`**, SWE2-DATA 2026-09-30).

### And what an accessor actually does — §7's third unknown, narrowed

Read in full, `0062FF50` never calls a constructor:

```asm
0062FF54  mov  rax, qword ptr gs:[0x58]          ; the thread epoch
0062FF6F  cmp  dword ptr [rip + 0x26C9583], eax  ; its guard, 02CF94F8
0062FF77  lea  rax, [rip + 0x18FE492]            ; its static,  01F2E410  <- the whole hot path
0062FF8A  call 0x8092FC                          ; _Init_thread_header
0062FF9F  call 0x808B90                          ; atexit(008AFE00)
0062FFAB  call 0x80929C                          ; _Init_thread_footer
```

`00808B90` is already named **`atexit`** in the function list. **The singleton is zero-initialised
and only its teardown is generated** *(corrected 2026-09-14, FABLE: not zero-initialised — the image holds each
record's vtable, name and size; see §7)* — which is why the fifteen bodies are identical and why none of
them names its type. §7's question shrinks from *"which of seven unrelated singletons"* to **"what is
one `0x50`-byte element of the array at `01F2E330`"**.

**Not claimed.** ~~What `+0x58`/`+0x5C` of an array member hold, or~~ `+0x18`/`+0x20`/`+0x28` of an
annotation ~~— both stay open~~ *(`+0x58`/`+0x5C` answered since, `UQ-281`; the annotation fields are `SD-61`. SWE2-DATA 2026-09-30)*. What the fifteen singletons *are*. ~~Why the destructor has one caller:~~
~~whether `PAnnotation` teardown normally runs through some other path, or whether these objects simply~~
~~outlive the process, is **not** established — only that no direct call and no pointer to `006B6750`~~
~~exists in the image. `FUN_005AABB0` was identified but not read. `008AFE00`'s fifteen bytes were not~~
~~decoded.~~ *(Corrected 2026-09-30, SWE2-DATA. The one caller, `005AABB0`, is slot 0 of the `PAnnotationWithValue<unsigned int>` vtable `00D32D50`: a scalar deleting destructor that calls `006B6750` and frees `0x38` bytes. `PAnnotation`'s own deleting destructor `006B6780` inlines the same unlink (§6), so the out-of-line body has one caller because the other teardown paths inline it. `_index/candidates/dd-data-2-0930/annot_checks.py` N1. `008AFE00` is decoded in §7: `lea rax, [00D31168]; mov [record], rax; ret`.)* Nothing was executed and nothing was observed live.

## Call chain (SWE2-DATA, 2026-09-30)

```
class-descriptor initialisers (static init)
  -> 00632A10  PClassDataMemberArray ctor (124 callers, 165 sites)  -> 00632960  plain-member base (+0x58 / +0x5C kept)
  -> 00632960  PClassDataMember, directly (248 callers)
  -> 006B66C0  PAnnotation ctor (70 callers)
teardown
  PAnnotationWithValue<unsigned int> deleting destructor 005AABB0 -> 006B6750  PAnnotation destructor (its one caller)
  PAnnotation deleting destructor 006B6780                          (006B6750 inlined)
lazy statics
  fifteen 98-byte accessors -> 008092FC _Init_thread_header -> atexit 00808B90 (15-byte teardown) -> footer
```

Counts from `_index/candidates/dd-data-2-0930/annot_checks.py` (N3) and `array_member_args.py`; the accessors from §9.

## Modding notes (SWE2-DATA, 2026-09-30)

Nothing here is authored data: the member descriptors are built by code at static initialisation. For a tool that
reads Phyre files, the useful fact is §3's pair. An array member's `+0x5C` names its kind (fixed, pointer, `PArray`,
`PSharray`) and `+0x58` its element size. Those two decide how a reader walks the array (`UQ-281`).

## What is still open (SWE2-DATA, 2026-09-30)

- [x] ~~What an annotation's `+0x18`, `+0x20` and `+0x28` carry, and so what an annotation annotates.~~ **`SD-61` — answered 2026-09-30 (OPUS `73e6ff01f`):** key "WriteMask", type `PTypeDefault<unsigned int>`, value `0x7FFFFFFF`, linked into the annotated `m_count` member's list (69 classes).
- [x] ~~What the two non-type accessor elements `01F2E330` and `01F2E780` are (their cold paths are unread).~~ **`SD-62` — answered 2026-09-30 (SWE2-ORACLE `dedfaf0d7`, after OPUS's `e2777d3c8` narrowing):** `01F2E330` is the class-descriptor root (descriptors on `+0x10`, owner objects on `+0x28`); `01F2E780` is the class-name hash tree. The `PWorld` / `getInstanceCount` slots are a separate method record at `01F2E7B0`.
- [x] ~~What the 703-byte layout body that fetches the class-layout interface lays out.~~ **`SD-63` — answered 2026-09-30 (OPUS `ce6a553b2`):** Phyre's scene-wide shader parameter table (23 named parameters) and its constant-buffer layout.

## Evidence (SWE2-DATA, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| `00632A10` constructs `PClassDataMemberArray`; `a8` bypasses the base | §3, §8, §9: body read, RTTI | 1 |
| `+0x5C` = array kind, `+0x58` = element size | `UQ-281`; `array_member_args.py` M1–M3 (165-site census) | 1 |
| `PAnnotation` construct / destruct, the 0x30-byte object | §4, §6: bodies read, RTTI | 1 |
| the destructor's one caller is `PAnnotationWithValue<unsigned int>`'s deleting destructor | `annot_checks.py` N1 | 1 |
| fifteen lazy-static accessors over one `0x50` array; thirteen type records | §7, §9 | 1 |
| the descriptor pass's flag word is 0 | `annot_checks.py` N2 | 1 |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Resource — CLIENT, fan-in of 230 edges.** Cited registration functions are called by 383-byte Resource bodies~~, 60 call sites in the most-called case~~. *(Corrected 2026-09-30, SWE2-DATA: a direct-call census does not reproduce 60. The most sites one caller has into a registration function is 20, into the plain-member base (682 sites from 248 callers). The array constructor's peak is 7 (165 sites from 124 callers), and the annotation constructor's is 1 (70 from 70). `_index/candidates/dd-data-2-0930/annot_checks.py` N3.)*

- **Platform - SERVICE (1 edge; added 2026-09-30, SWE2-DATA, with the SD-63 incorporation).** `005FD2A0`, the scene-wide shader parameter table builder named for SD-63, calls one body filed to Platform (described, not named) - a service the builder uses, no shared ownership and no claim of this page.

## The eleven `008AFxxx` teardown thunks — 2026-09-14 (NOCALLER-INSTALLERS; corrected by FRONTIER-CONTRA-6349B0-THUNK-ROLE)

`006349B0` is the class-descriptor initializer. For eleven `m_*` properties it builds a member-descriptor object in
place and hands one no-caller function to the CRT `atexit` wrapper. The functions in the table are those
arguments.

**They are the objects' destructors, registered for process exit. They do not run during the pass.**
*(Corrected 2026-09-14, FABLE ruling on `FRONTIER-CONTRA-6349B0-THUNK-ROLE`. This section previously called them
"static-descriptor initializers" that each "run once from `006349B0`'s registration pass".)*

**What the pass does**, read at the first pair:
1. It fills the object at `02CF9080` inline and makes its list head at `02CF90B8` point to itself.
2. It calls slot `+0x40` through the table pointer held in `02CF8580` (`00634AA3`), with `rsi` as `rcx` and the object as `rdx`.
3. It stores `edi` into the flag word at `02CF90A8`. ~~The value of `edi` was not traced.~~ *(Traced 2026-09-30, SWE2-DATA: `edi` is 0. The pass clears it at `006349F6`, it is non-volatile across the calls, and no instruction before the store writes it. `_index/candidates/dd-data-2-0930/annot_checks.py` N2.)*
4. It loads `008AFB90` into `rcx` at `00634AAC` and calls `atexit`.

The other ten lea sites in the table are also each followed at once by the `atexit` call, and the pass contains
eleven such calls. Across the whole image, each of the eleven has exactly one `rip`-relative reference, its own `lea`, and no `E8`/`E9` call or jump site.

**What each member does.** All eleven are 103 bytes with the same shape. Each of them:
- re-stamps the descriptor vtable `00D580B0` into its own cell, the object itself;
- when the object's `+0x08` list is not empty, calls slot `+0x48` of the object named at `+0x18`, passing the cell;
- unlinks the list head at `+0x38` through `006B6700`;
- frees the `+0x20` pointer through `00584730`, only when bit 0 of `+0x28` is set.

That is the shape of an inlined destructor: vtable restore, detach, owned-list clear, conditional free. It mirrors
the pass's construction step, which uses slot `+0x40` where the destructor uses `+0x48`. The pairing is the same
static-lifetime pattern as the `atexit`-armed singletons above.

**When they run:** once, at normal process exit, from the CRT's exit table. That step is inferred from the `atexit`
contract. No exit was observed.

| member | property name (installer `lea` site) | descriptor cell | interior |
|---|---|---|---|
| `008AFB90` | `m_size` (`00634AAC`) | `02CF9080` | `008AFB9D` |
| `008AFB20` | `m_size` (`00634B05`) | `01F2E000` | `008AFB2D` |
| `008AF9D0` | `m_offsetFromParent` (`00634BCB`) | `02CF90E0` | `008AF9DD` |
| `008AFA40` | `m_offsetToBase` (`00634C91`) | `02CF9140` | `008AFA4D` |
| `008AFAB0` | `m_offsetToBaseInAllocatedBlock` (`00634D57`) | `02CF91A0` | `008AFABD` |
| `008AF6C0` | `m_currentMemberCount` (`00634E1D`) | `02CF9200` | `008AF6CD` |
| `008AF570` | `m_actualSize` (`00634EE3`) | `02CF9260` | `008AF57D` |
| `008AF8F0` | `m_actualSize` (`00634F38`) | `01F2E060` | `008AF8FD` |
| `008AF730` | `m_defaultBufferStorage` (`00635033`) | `02CF92C0` | `008AF73D` |
| `008AFD00` | `m_validationBufferStorage` (`00635127`) | `02CF9330` | `008AFD0D` |
| `008AFD70` | `m_writeMaskBufferStorage` (`0063521B`) | `02CF93A0` | `008AFD7D` |

Two properties register twice — `m_size` and `m_actualSize` each bind a `02CF9xxx` cell and a
`01F2Exxx` cell — the second cell sits beside the `01F2E330` array the fifteen singletons index,
so those two properties carry both a descriptor cell and an array element. The interior column
cites the vtable `lea` inside each member's own 103-byte body; all eleven bodies were bounded at
their real extents (`interior_cite.py scan`) after a scan-boundary defect was found and repaired.
