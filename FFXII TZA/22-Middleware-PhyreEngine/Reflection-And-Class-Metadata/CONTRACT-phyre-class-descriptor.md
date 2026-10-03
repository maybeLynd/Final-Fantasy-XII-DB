---
contract: The PClassDescriptor - what reflected class metadata is, in bytes
category: 22-Middleware-PhyreEngine
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: class-descriptor-and-metadata-system.md
entries: ["00633390", "006388C0", "0063D550", "0063D640", "005847E0", "00584730", "0063E410"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 69 addresses cited - 4 data, 16 entry, 49 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-phyre-class-descriptor-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the `PClassDescriptor`, in bytes

> **Authored 2026-09-12 by OPUS.** The mechanism, the family census and the layout are the source
> page's, [the class descriptor and metadata system](class-descriptor-and-metadata-system.md),
> which carries a falsification pass.
>
> **Every offset in this contract was re-read from the image, and that is not a formality.** That
> page has corrected its own offsets **twice** — once because decompiler *qword indices* were
> transcribed as byte offsets, and once because the type name was placed at `+0x60` by doing
> arithmetic on the first mistake. A contract that restated them without re-reading would have been
> the third. **Everything below is confirmed against `0063D550`, `00633390` and `006388C0`.**

## 1. Purpose

**This is what the engine knows about its own classes.** Phyre writes down, at runtime, every
reflected class's name, its members, their offsets and their types — and `.phyre` files carry the
same schema as text (see [the packed namespace](../Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md)).
The descriptor is the runtime half.

For a player, nothing. For anyone reading FFXII's asset formats, **the two halves agree and neither
was derived from the other**, which is what makes the file schema trustworthy.

## 2. Interface

| | |
|---|---|
| size | ~~**at least `0x140`**~~ **`0x100`**, and `0x140` for `PClassDescriptorDynamic` *(corrected 2026-10-02, OPUS: PCD-3, answered 2026-09-25; 90 pairs of the schema's static descriptors sit exactly `0x100` apart in `.data`)* — `0063D550` writes `+0x138` and `+0x104`, fields of the Dynamic form ~~; the exact end is not established (§14)~~ |
| allocation | **`_aligned_malloc`**, not `operator new`; released through `_aligned_free` (`00584730`) |
| destructor | `00633390`, 500 bytes — the base `PClassDescriptor` destructor |
| per-class deleting destructor | one generated function per reflected class, e.g. `005847E0`, 92 bytes; **1,149 of them** |
| name lookup | `006388C0`, `PType_FindOrRegisterByName` |
| reset / rebind | `0063D550`, 233 bytes |

**There are 4,557 generated reflection functions across 42 families.** The descriptor is not one
object type; it is a family the compiler stamps out per class.

## 3. Types and state — the byte layout

**Re-read from `0063D550` and `00633390`.** Offsets are **bytes**.

> **Two classes, not one (OPUS, 2026-09-25).** Rows `+0x100` onwards belong to the derived
> **`PClassDescriptorDynamic`** (0x140 bytes), not to the base.
>
> - The base, `PhyreClassDescriptor`, is 0x100: the reach of its constructor `00632D80`.
> - `0063D550` is a method of the derived class.
> - Its constructor `00632E80` calls `00632D80`, installs vtable `00D58380` (RTTI
>   `.?AVPClassDescriptorDynamic@Phyre@@`), and writes `+0x100..+0x13F`.
> - `0059AC00` allocates exactly `0x140` for it (`0059AD27`).
>
> Both classes are declared in `_types`. `+0x108`/`+0x118`/`+0x128` are three counted buffers,
> each `{count with bit 31 = borrowed, data*}`.

| offset | width | meaning |
|---|---|---|
| `+0x00` | 8 | vftable. The destructor overwrites it with ~~`PType`'s before releasing anything~~ `PClassDescriptor`'s on entry and `PType`'s on exit *(corrected 2026-10-02, OPUS: `006333BC` stores `00D581C0`, `.?AVPClassDescriptor@Phyre@@`; `00633568` stores `00D31168`, `.?AVPType@Phyre@@`)* |
| `+0x30` | 8 | **the type name, a plain `char *`.** `006388C0` loads it, returns 0 if null, and hashes the bytes it points at |
| `+0x38`, `+0x3C` | 4, 4 | copied from the **parent** descriptor's `+0x38` / `+0x3C` during a rebind |
| `+0x50` | 16 | **intrusive list 1** — head at `+0x50`, tail at `+0x58`. **This one is a MEMBERSHIP node, not a list the descriptor owns**: `0063D640` unlinks it from whatever list it is in and self-links the head (§13a) |
| `+0x60` | 16 | **intrusive list 2** |
| `+0x70` | 8 | a sub-object, destroyed **first** by `0063D640` |
| `+0x78` | 8 | **the parent descriptor**, or null |
| `+0x80` | 16 | **intrusive list 3** |
| `+0x90` | 16 | **intrusive list 4** — the first one the destructor walks |
| `+0xA0` | 16 | **intrusive list 5** |
| `+0xB0` | 16 | **intrusive list 6** |
| `+0xC0` | 8 | **the default instance** — the object every new instance is `memcpy`'d from. Set by the one-instruction setter `0063DC80` (`mov [rcx+0xC0], rdx`); consumed by `0063C910`, which does `rdx = [descriptor+0xC0]; if (rdx) memcpy(instance, rdx, [descriptor+0x38])` |
| `+0xC8` | 8 | ~~**a second full-size instance**~~ **an instance-size byte mask** *(corrected 2026-10-02, OPUS: `00639C80` fills it with `0xFF` over the instance size, `00639CBE`-`00639CD3`; purpose read below)*, set by `0063DF90` (`mov [rcx+0xC8], rdx`). ADDED 2026-09-19 (OPUS) |
| `+0xD0` | 8 | ~~**a third full-size instance**~~ **an instance-size byte mask** *(corrected 2026-10-02, OPUS: `00639C80` zero-fills it, `00639CD8`-`00639CE4`)*, set by `0063DFA0` (`mov [rcx+0xD0], rdx`). ADDED 2026-09-19 (OPUS) |
| `+0xD8`, `+0xE0` | 8, 8 | two further pointer slots the constructor zeroes at `00632E24` and `00632E2B` alongside `+0xC0`/`+0xC8`/`+0xD0`. **No setter found**, so they are declared as part of the same family and nothing more |
| `+0xE8` | 4 | a **registration counter** (§7) |
| `+0xF0` | 4 | the parent's `+0x38`, **negated** |
| `+0x100` | 4 | a two-word guard (`+0x100` and `+0x102` compared) that can skip the whole reset |
| `+0x104` | 4 | a copy of the parent's `+0x38` |
| `+0x138` | 8 | **a tagged pointer**: `+0x30` is this value with **bit 0 cleared** |

### Six lists, and they are circular

```asm
0063D572  lea  rax, [rcx + 0x50]      ; and again at +0x80, +0x90, +0xA0, +0xB0, +0x60
0063D57B  mov  qword ptr [rax], rax   ; head -> itself
0063D57E  mov  qword ptr [rax + 8], rax   ; tail -> itself
```

**A list is empty when its head points at itself**, which is how the destructor tests them:
`cmp rdi, r14 / cmove rdi, rbp` — head equal to the list address becomes null.

> **The source page says four lists; the reset helper initialises SIX**, and this contract's reading
> agrees with the correction rather than the original table.

### ⚠ CORRECTED 2026-09-12 by the destructor pilot — the destructor does not "walk four lists"

**This contract said the destructor walks four lists and leaves `+0x50` and `+0x60` alone. It does
neither.** `00633390` does **two different things to two different sets**:

| phase | lists, in order | what it does |
|---|---|---|
| **free-walks** | `+0x90` (`006333E6`), `+0xA0` (`0063344E`) | tests each node's ownership bit and, when set, unlinks it and releases **both** its `+0x18` pointer and the node |
| **drain loops** | `+0x80` (`006334B2`), `+0x90` (`006334E4`), `+0xA0` (`00633508`), `+0xB0` (`0063352C`) | unlinks **every** node and self-links it, and **frees nothing at all** — those four loop bodies contain no `call` |
| handed off | `+0x60` (the call `0063355B`; `00633557` is its argument `lea rcx, [r15+0x60]`, anchor corrected 2026-09-27 (OPUS, on ASTRA's descriptor-lifetime-claim-boundary)) | to `006B6700`, **a pure drain** — unlink only, no frees (§13a) |
| **not in this body — but not left alone** | `+0x50` | `0063D640` unlinks and self-links it (§13a). **The descriptor is passed to that callee in `rdx` for exactly this purpose**, so a reimplementation that reads only `00633390` leaves the node linked |

**So `+0x90` and `+0xA0` are processed TWICE, and the consequence is a lifetime fact rather than a
detail of order: A NODE IN `+0x80` OR `+0xB0` IS NEVER RELEASED BY THIS DESTRUCTOR, whatever its
ownership bit says.** Only `+0x90` and `+0xA0` free anything.

> **How it was caught.** The pilot's case with one owned node in each of the four lists freed
> **four** addresses where the reconstruction built from the paragraph above freed **eight**; and a
> case with an owned and an unowned node in one list showed the original **emptying the list head**,
> which no per-node walk can do. The drain loops are what does it.

> **The list head is emptied either way.** After the drains, every one of those four heads points at
> itself and every surviving node is self-linked — so "the destructor left my node in the list" is
> never the observable. **The node survives; its membership does not.**

### The list NODE, and its ownership bit

**Re-read from the destructor's walk at `00633400`–`0063344C`.** The lists are not lists of opaque
things:

| offset | width | meaning |
|---|---|---|
| `+0x00` | 8 | **next** |
| `+0x08` | 8 | **prev** |
| `+0x18` | 8 | an owned pointer, released with `_aligned_free` |
| `+0x20` | 1 | a flag; **bit 0 means the node is OWNED** |

```asm
00633415  test byte ptr [rbx + 0x20], 1
00633419  je   0x633449                  ; NOT owned -> leave it linked and do not free
0063341B  mov  rcx, [rbx] / mov rax, [rbx+8]
00633422  mov  [rcx + 8], rax            ; next->prev = prev
00633426  mov  [rax], rcx                ; prev->next = next
00633429  mov  [rbx], rbx / mov [rbx+8], rbx   ; and self-link the node it just removed
00633436  mov  rcx, [rbx + 0x18] / call 0x584730   ; free the owned pointer
00633443  mov  rcx, rbx / call 0x584730            ; then the node
```

> **A node that does not claim ownership is left in the list and not freed** — ~~so a descriptor's~~
> ~~destructor does not necessarily empty its own lists.~~ *(Qualified 2026-09-27 (FABLE, Claude Opus 5.5), on
> `ASTRA-RETURN-FABLE-DESCRIPTOR-MEMBERSHIP-PROVENANCE`: "left in the list" holds for this first free-walk only.*
> - *The drains that follow unlink and self-link every surviving node of `+0x80`, `+0x90`, `+0xA0` and `+0xB0`.*
> - *`+0x60` is handed to the `006B6700` drain (the phase table above).*
> - *So the heads end empty, and no node's membership outlives the destructor.*
> - *The ownership bit decides only whether this destructor frees the node. It does not show where an unfreed node's
>   storage came from: static, external, pool or arena storage all fit an unlink without a free.)*
>
> That is the same shape as the namespace
> buffer's bit-31 flag in [the cluster header contract](../Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md)
> §3: **this middleware marks borrowed storage rather than tracking it**, and it does so in more
> than one place.
>
> **The walk advances before it unlinks** (`00633408` reads `[rdi]` into the cursor at the top of
> the body), which is what makes freeing the current node safe.

> **The name is stored twice.** `0063D550` computes `+0x30` as `[+0x138] & ~1`, so **`+0x138` is a
> tagged pointer and `+0x30` is its untagged cache.** ~~What bit 0 marks is not established (§14)~~ *Bit 0 marks a
> borrowed name, which the destructor does not free; no writer sets it in this image (§14 item 2, 2026-09-25)* —
> but a reimplementation that writes only one of the two, or that forgets the mask, gives
> `006388C0` a misaligned pointer to hash.

## 4. Preconditions · postconditions · invariants

**Invariants.**

1. **The name is a plain `char *` at `+0x30`, and nothing else is.** Reading `+0x0C` or `+0x60` as
   the name — both of which this subsystem's own documentation once did — reads a list link.
2. **A descriptor is aligned storage.** Its deleting destructor calls `_aligned_free`, so a
   reimplementation that pairs it with `free` is wrong at the allocator.
3. **Six lists, all circular and self-linked when empty.**
4. **The destructor releases the sub-object at `+0x70` before touching any list**, and overwrites
   the vftable before that — **with a different constant from the one it writes on the way out**
   (`00D581C0` at `006333BC`, `00D31168` at `00633568`), so the object passes through two vtable
   identities during its own destruction.

## 5. Relationships

`005847E0` (and 1,148 siblings) → `00633390` → `0063D640` (the `+0x70` sub-object) and the list
walks → `00584730` = `_aligned_free`. `0063D550` rebinds a descriptor against its parent at `+0x78`
and then calls `0063E410`.

## 6. State transitions

Built by a static initializer per class, rebound by `0063D550`, destroyed by `00633390`.

## 7. The registration counter is a high-water mark

```asm
006333BF  mov  eax, dword ptr [rcx + 0xe8]
006333C5  inc  eax
006333C7  mov  edx, dword ptr [rip + …]        ; -> 02CF8260
006333CF  jne  0x6333d9
006333D1  dec  edx
006333D3  mov  dword ptr [rip + …], edx        ; -> 02CF8260
```

**If this descriptor's counter plus one equals the global, the global is decremented.** That is a
high-water mark being wound back when the topmost registration is destroyed — not a refcount, and
not an id that is reused. **Destroying a descriptor that is not the topmost leaves the global
alone**, so the counter space is not compacted.

## 8. The deleting-destructor convention

```c
void *ClassDescriptorForType_X::~scalar_deleting(void *self, unsigned long long flags)
{
    *(void **)self = PClassDescriptorForType<X>::vftable;
    PClassDescriptor_dtor(self);              /* 00633390 */
    if (flags & 1) {                          /* bit 0: also free the storage */
        if (!(flags & 4)) _aligned_free(self);        /* 00584730 */
        else              _guard_check_icall(self, 0x100, …);   /* bit 2: the CFG path */
    }
    return self;
}
```

**This is the MSVC scalar-deleting-destructor convention**: bit 0 means "delete after destructing".
~~Bit 2 selects a Control Flow Guard-mediated path instead of the direct `_aligned_free`.~~ Bit `0x4` (with bit `0x1`) calls `0016D6A0(self, 0x100)` instead of `_aligned_free` (`00584820`..`00584828`), and `0016D6A0` is a single `ret 0`: nothing is freed on that arm. *(corrected 2026-10-03, OPUS, S-49 point 3)*

## 9. Determinism

Deterministic given the registration order, which is static-initializer order and therefore link
order. **Nothing here is data-driven.**

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | `+0x30` is null | `006388C0` returns 0 without hashing — the only guarded case on that path |
| 2 | a list is empty (head points at itself) | the walk is skipped via `cmove` |
| 3 | `+0x78` (parent) is null | `0063D550` skips the whole rebind and returns |
| 4 | the `+0x100` / `+0x102` guard matches | the reset is skipped entirely |
| 5 | `flags & 1` clear | the object is destructed and **not** freed |

**Provably dead branches, and there are five of them.** `0063D550` does `lea rax, [rcx + N]` and
then `test rax, rax / je` for **every one of its six lists**. A `lea` of a non-null base plus a
small constant cannot be null, so **none of those six tests can ever fire.** They are a compiler
artifact of a null-checking helper being inlined, and a reimplementation that writes them as real
guards is more defensive than the original.

## 11. Observable behaviour

Nothing directly. In memory: the descriptor's fields, the six list heads, and the global at
`02CF8260`.

## 12. Reproduction formula

```c
void PClassDescriptor_Reset(PClassDescriptor *d)        /* 0063D550 */
{
    if (*(uint16 *)((char *)d + 0x100) == *(uint16 *)((char *)d + 0x102)
        && *(uint16 *)((char *)d + 0x100) != 0)
        goto tail;                                      /* the guard skips everything */

    for (int off : { 0x50, 0x80, 0x90, 0xA0, 0xB0, 0x60 }) {
        void **l = (void **)((char *)d + off);
        l[0] = l;  l[1] = l;                            /* circular, empty */
    }
    *(uint32 *)((char *)d + 0x100) = 0;

    PClassDescriptor *parent = *(void **)((char *)d + 0x78);
    if (parent) {
        uint32 a = *(uint32 *)((char *)parent + 0x38);
        *(uint32 *)((char *)d + 0x104) = a;
        *(uint32 *)((char *)d + 0x38)  = a;
        *(uint32 *)((char *)d + 0x3C)  = *(uint32 *)((char *)parent + 0x3C);
        *(uint32 *)((char *)d + 0xF0)  = -(int32)a;
        FUN_0063E410(d);
    }
tail:
    /* the name is the tagged pointer with bit 0 cleared */
    uintptr_t tagged = *(uintptr_t *)((char *)d + 0x138);
    *(char **)((char *)d + 0x30) = (char *)(tagged - (tagged & 1));
    …
}
```

## 13. Runtime validation

**Evidence class: isolated original-code, and now over BOTH halves of this contract.**

| what | pilot | cases | mismatches |
|---|---|---:|---:|
| reset and rebind, `0063D550` | [`diff_class_descriptor.py`](../../../../Reconstruction/Tests/Differential/diff_class_descriptor.py) — the 38th | 22 | **0** |
| **the destructor, `00633390`** | [`diff_class_descriptor_dtor.py`](../../../../Reconstruction/Tests/Differential/diff_class_descriptor_dtor.py) — the 39th | 30 | **0** |

**The destructor pilot compares the addresses passed to `_aligned_free`, in order**, alongside the
descriptor, the node heap and the global counter. That is the whole point: a destructor that
releases the right number of things in the wrong order, or releases a node it should have left
alone, is identical on every other observable.

### It refuted this contract's account of the destructor

**§3 now carries the correction.** The contract said the destructor walks four lists and leaves
`+0x50` and `+0x60` alone. **It runs two free-walks and four drain loops**, and the case with one
owned node in each of the four lists **freed four addresses where the reconstruction built from that
sentence freed eight.** A second case, an owned and an unowned node in one list, showed the original
**emptying the list head** — which no per-node walk can do, and which the drains explain.

> **That is two contracts in a row whose own pilot corrected them**, and in both the error was a
> plausible reading of the right instructions. The leas really do name `+0x90`, `+0xA0`, `+0x80` and
> `+0xB0`; what reading them in order does not reveal is that the last two belong to a different
> phase that frees nothing.

**Mutation campaign: 62 points — 43 KILLED, 11 SURVIVED,
3 EQUIVALENT, 2 TIMEOUT, 3 INVALID. Status `FAIL_INCOMPLETE`,
and that status is reported rather than smoothed over.** Adding the cases below moved it from 40
killed to 43.

### Every non-kill, adjudicated

- **5 are kind A, provable equivalences.** Two grow a table the loop bound never reaches. One
  perturbs the **entry** vftable constant, which the **exit** write overwrites before anything can
  observe it. Three turn a sentinel `0` into `1` where the very next step resolves the address and
  gets nothing either way.
- **5 are kind B, fixture scaffolding.** The address-resolution helper's bounds and its
  not-found return, the drain's iteration guard, and `CDT_MAX_EVENTS` — none has a counterpart in
  `00633390`, which resolves nothing and bounds nothing.
- **1 is kind C, undefined behaviour**: reading one past a four-entry table.
- **2 TIMEOUTS are also kind C, and they are the first in this database.** One widens a
  byte-serialisation loop from 8 to 9 and corrupts the neighbouring field; the other flips the
  drain's `cur == listAddr` to `!=`, so the walk follows the list head back into itself forever.
  **A mutant that does not terminate is not a survivor** — the instrument records it separately and
  that is the right answer, not a gap.
- **3 INVALIDS are kind B detected by the instrument**: two change the fixture's buffer
  sizes and one shifts a node field, so the driver's fixed-width output stops being parseable. The
  run is scored `FAIL_INCOMPLETE` because of them, and **the honest reading is that three mutations
  of the harness could not be evaluated — not that three behaviours went untested.**

**No kind D remains.** The two the campaign did find were closed by cases: an **unowned** node in
each drained list (every earlier case either freed its node or left the list empty, so the drain's
effect on a named list was never separately visible), and counter values whose **upper bytes**
matter — the same shape that this session's other campaigns kept producing.

**Three callees are scripted**: `_aligned_free` (four call sites, hooked to record rather than to
free, since the fixture owns the memory), the `+0x70` sub-object destructor `0063D640`, and the
`+0x60` handler `006B6700`. **A stub is not proof of its native effects** — what is established is
which addresses reach `_aligned_free` and that the other two are called exactly once each.

Receipts: `Database/Tools/work/OPUS/litsuffix/class_descriptor`, `class_descriptor2`, `cd_dtor` and
`cd_dtor2` (ignored path), and the counts rows in
[`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

### 13a. The two scripted callees, executed — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-097)

**Evidence class: isolated original-code execution of the real shipping bytes** (EXP-097, 15/15
fixtures and 10/10 mutants killed across two processes), **plus an independent re-read of both
bodies here.** *Qualified 2026-09-27 (OPUS, on ASTRA's descriptor-lifetime-claim-boundary): one of the ten, `m-selflink`, is not the mutation its label says. Its NOP4 at `006334F1` covers the three-byte `mov rcx, [rdx]` and the first REX byte of `006334F4`, not an isolated self-link store; that drain's neighbour-unlink store is `006334F8` and its node self-links are `006334FF` / `00633502`. The recorded kill stands as a historical modified-code result, not as intended coverage; the harness repair is SWE2-ORACLE's (`ASTRA-RETURN-ORACLE-EXP097-NODE-OBSERVER-AND-MUTATION`). EXP-097's saved observations are the heads, the registry and embedded nodes, the counter and the vtable - not the spans of individual list members.* Every claim below was checked against the instructions before it was written; where
the experiment and this contract's earlier prose disagreed, the bytes decided.

#### `0063D640` takes `(rcx = the sub-object, rdx = the descriptor)` — and this contract had it the other way

The call site settles it: `006333D9 mov rdx, r15` (the descriptor) then
`006333DC mov rcx, [rcx + 0x70]` (the sub-object), `006333E0 call 0063D640`. §15's row reads
*"`006333DC mov rcx,[rcx+0x70] / call 0063D640`"*, which is true and incomplete — it omits the
argument that makes the callee's first act possible. **An argument order taken from prose rather
than from the call site is how a reimplementation destroys the wrong object**, and EXP-097's harness
notes record that its fixture was corrected to match the body rather than the description.

The 109-byte body does three things, in order, and **any one of the last two can end it early**:

1. **It unlinks the DESCRIPTOR's `+0x50` node and self-links that head.** `0063D646`–`0063D665`:
   `rax = [rdx+0x58]`, `r8 = rdx+0x50`, `rdx = [rdx+0x50]`, then `[rdx+8] = rax` / `[rax] = rdx`
   removes it, and `[r8] = r8` / `[r8+8] = r8` empties the head. **This is why the destructor passes
   the descriptor at all**, and it is the fact the phase table above used to record as
   *"never mentioned"*.
2. **It gives up if the sub-object's `+0x10` list is NOT empty.** `0063D65C`–`0063D681`:
   `rax = rcx+0x10`, `rdx = [rax]`, `cmp rdx, rax` / `cmove rdx, 0` — the same head-points-at-itself
   emptiness test used everywhere in this object — then `lea rax, [rdx - 0x50]` and `jne` out.
   *The `-0x50` is a container-of adjustment from a node to an object at offset `0x50`, so the
   things on that list are other objects' `+0x50` nodes; only its nullness is used here, so that is
   what the idiom shows rather than what this body proves.*
3. **Otherwise it asks who the current object is, and detaches the sub-object unless it is that
   one.** `0063D683 call 006373D0`, `cmp rbx, rax`, `je` out; else **`006373D0` is called a second
   time** (`0063D68D`) and the sub-object's own node at `[rbx]` / `[rbx+8]` is unlinked and
   self-linked. EXP-097 drove all three arms — empty-and-not-current (getter called twice, node
   detached), list-nonempty (getter never called), and empty-but-current (called once, no detach) —
   and `m-regcmp` (`je`→`jne`) detaches the current object and diverges in 13 cases.

#### `006B6700` frees nothing at all

71 bytes, and the whole body is one loop: `cmp rdx, r8` / `cmove` for emptiness, `lea rax, [rdx-8]`
as the container-of, then `[rcx+8] = rax` / `[rax] = rcx` to unlink and `[rdx] = rdx` /
`[rdx+8] = rdx` to self-link, and `jmp` back. **There is no `call` in it.** So the `+0x60` handoff
is a drain exactly like the four in `00633390`, and **`+0x60` is the fifth list this destructor
empties without releasing anything**.

#### What this adds to the reconstruction, stated as the boundary a reimplementer needs

- **The descriptor is removed from one list and its sub-object from another, conditionally.** Getting
  the argument order wrong swaps which.
- **Six lists, and only `+0x90` and `+0xA0` ever free.** `+0x50`, `+0x60`, `+0x80` and `+0xB0` are
  unlink-only, now on executed evidence rather than on absence of a `call` in a listing. *Scope, 2026-09-27 (OPUS, on ASTRA's descriptor-lifetime-claim-boundary): for the `00633390` drains the pilot compares the whole node heap byte for byte; for `006B6700` EXP-097 observed the head, and the node side is ASTRA's raw-node control - the unmodified 71-byte body over a two-node ring (one node above 4 GiB) leaves both complete 56-byte nodes self-linked with every other byte unchanged, and a NOP of the node prev self-link at `006B6740` still returns an empty head while the node back-links stay stale, which a heads-only observer passes. Unlink-only says the teardown releases no memory; it says nothing about who allocated a surviving node.*
- **The registry getter is called twice on the detach path.** A reimplementation that caches it is
  observably different under an entry hook, which is how EXP-097 distinguished the three arms.
- **The counter guard wraps.** `counter-wrap` drove field `0xFFFFFFFF` + 1 → 0 against counter 0, and
  the guarded decrement stored `0xFFFFFFFF`; §7's high-water-mark reading survives it.

#### What is still not claimed

`006373D0`'s lazy-init arm is unproven — EXP-097 plants the initialised state and exercises only
the already-initialised path. `_aligned_free`'s internals are a boundary. And **none of this touches
`PCD-1`**: the teardown mechanics of five lists are now executed, and what any of those lists HOLDS
is exactly as open as it was. *(Superseded 2026-09-25/26 by `PCD-1`, FABLE: five of the six lists are named - `+0x50` the descriptor's own registry node, `+0x60` the annotation list, `+0x80` data members, `+0x90` instance methods, `+0xA0` static functions; `+0xB0` is the residue carried by `BL-8`.)*

## 14. Unresolved

*Renumbered 2026-09-14 (FABLE, `OPUS-REQ-FABLE-QUESTION-ID-INTEGRITY`): these ids were `CD-1`…`CD-5`, which the question register already uses for different questions (EBP container questions). The register keeps its ids; this list moved, and the rows are registered under the new ids.*

1. ~~**`PCD-1`** — **what each of the six lists holds.** The source page says their roles are not
   established and this contract does not improve on that. The member registrations documented in
   [the recovered field schema](member-registration-and-the-recovered-field-schema.md) attach to
   `+0x80`, which names one of six.~~ **PARTIAL 2026-09-25 (FABLE, Claude Opus 5.5): five of the six are named, and
   `+0xB0` is the residue (`BL-8`).** Four were already answered on
   [the metadata page](class-descriptor-and-metadata-system.md) (Q-1) and had not reached this list. `+0x60` is new.
   Static evidence only.

   | head | holds | how it is known |
   |---|---|---|
   | `+0x50` | not a list the descriptor owns: **its own node** in the registry's class ring | RTTI puts the `PSimpleDoubleListElement<PClassDescriptor>` base at `+0x50`. `00639160` splices the node in right after the parent's when the parent's `+0x70` is the same registry, and ~~appends it otherwise~~ links it at the head otherwise *(corrected 2026-10-02, OPUS: `0063922E`-`00639244` sets the sentinel `rbx+0x10`'s first pointer to the node)* |
   | `+0x60` | **the annotation list** | RTTI puts the `PAnnotatable` base at `+0x60` here and at `+0x38` in `PClassDataMember` (`00D580B0`). `006B6700` — the §3 hand-off — is the drain the data-member destructors `00633240`/`00633900` run on their own `+0x38` |
   | `+0x80` | the data members, linked through their node at member `+8` | `0062EFD0` |
   | `+0x90` | **instance methods** | records that point at a `PMethodCallerConcrete<Class, Return, Args…>`, e.g. `"setSpeed"`, `<PAnimatableComponent, void, float>`, vtable `00D34968`; name-checked by `005A7A40` |
   | `+0xA0` | **static functions** | the same record pointing at a `PFunctionCallerConcrete`, e.g. `"GetTime"` returning `double`, vtable `00D27CD0`; name-checked by `005A0470` |
   | `+0xB0` | **nothing, as far as the sweeps below reach** | initialised by `0063D550` and drained by the destructor; no insert found |

   **The record in `+0x90`/`+0xA0`, and what the §3 ownership bit guards.**
   - `00632FB0` builds the record: next, prev, the owning descriptor at `+0x10`, the name at `+0x18`, flags at `+0x20`.
     `+0x28` points at the caller object, which the registrars embed at `+0x30`.
   - It copies the name to the heap only when flag bit 0 is set. The static registrations read here pass 0, so their records survive
     the free-walk.
   - `00632960` builds a data member's header the same way at member `+8`. That is why §3's node layout
     (`+0x18` freed, `+0x20` bit 0) fits both.

   **The populations, image-wide.**
   - **`+0x90`:** 205 register-formed inserts (`lea`/`add` of the head, then a store at head `+8`). 150 of them are
     followed within 0xC0 bytes by a method-caller vtable, and none by a function caller. There are 7 more direct
     RIP-relative tail stores.
   - **`+0xA0`:** 11 inserts, each followed by a function-caller vtable. The RTTI has 11 `PFunctionCallerConcrete`
     vtables against 156 `PMethodCallerConcrete`. The one direct store is `00635980`, into `PNamespace`'s descriptor
     (vtable `00D56C00`).
   - **`+0x60`:** all 70 calls to the annotation add `006B67D0` target a data member's `+0x38`, and none targets a
     descriptor.
   - **`+0x60`/`+0xB0` by inline code:** none of the register-formed, RIP-relative-head or direct-tail-store shapes
     inserts into either on a descriptor. The last two were run over the 410 statics that receive a descriptor-class
     vtable. *Controls:* the same shapes return `0062EFD0` for `+0x80`, the counts above, and `00635980`'s store.
   - *Head-insert helpers swept 2026-09-29 (FABLE, accepted by SWE2-AUDIT-SEM's
    `auditsem-review-takebacks2-0930`):* the inverted census
    [`t4_descriptor_inserters.md`](../../_index/candidates/fable-astra-live-facts-0930/t4_descriptor_inserters.md)
    searches by what an insert must store rather than where it writes — 15 helpers found, all 70 `006B67D0` call
    sites resolve to data-member `+0x38` heads, and none of the other helpers' resolved heads is `+0x60` or `+0xB0`
    of a descriptor. Its limits: 21 unresolved call sites of 14 helpers outside the reflection band, a head held
    in memory across a long window, and code outside the function list. Heap descriptors whose head is held in
    memory stay unswept; the live read of real heads that `BL-8` names is still the closing step.
   - *Not established:* what `+0xB0` was meant to hold.
     ***Narrowed 2026-09-27 (FABLE, Claude Opus 5.5): nothing reads `+0xB0` either.** An image-wide census of the sentinel-walk idiom (`lea` of the head, load, compare with the head) finds the destructor `00633390` as the only function that walks `+0xB0`, and it only unlinks; the same census finds the name lookups `005A7A40` / `005A7B50` / `00682E30` on `+0x90` and `005A0470` / `005A7AB0` on `+0xA0`, and 22 walkers of `+0x80`. Every other touch is a self-link (the base constructors, the ten per-class constructors in `006316C0`-`00632780`, the reset `0063D550`). So the shipped build constructs, resets and tears the list down but never fills or consults it; what it was meant to hold leaves no trace in the build. [Record](../../_index/candidates/bl8-b0-walkers/README.md).*
2. ~~**`PCD-2`** — what bit 0 of the tagged pointer at `+0x138` marks.~~ **ANSWERED 2026-09-25 (FABLE, Claude Opus
   5.5): bit 0 set means the name is borrowed, so the destructor does not free it. In this image no writer ever sets
   it.** Static.
   - **The reader.** `0063D550` only strips the bit. The code that reads it is the dynamic descriptor's destructor
     `00633590`: it loads `+0x138` and skips the `_aligned_free` (`00584730`) when bit 0 is set
     (`0063361B`–`0063362F`: `not al; test al, 1; je`).
   - **The one writer** is the constructor `00632E80` (`00632F11`). It stores a heap copy of the name made by a
     string-copy helper with a 2-aligned allocation. So the bit is clear, and the destructor frees the copy.
   - **The sweep.** An image-wide sweep of qword stores at `+0x138` finds 68. None is preceded, within 0x40 bytes, by an
     `or`/`lea`/`bts` that would tag bit 0 on the stored register. That is a pattern check, not a receiver trace.
   - **So bit 0 is a borrowed-name tag**, in the spirit of the borrowed flag §3's counted buffers carry in bit 31.
     The member and method records use the opposite polarity: their flag bit 0 marks a heap-copied name, which
     `00632FB0` makes. This build never exercises the borrowed case for a descriptor name.
3. ~~**`PCD-3`** — the descriptor's exact size. `+0x138` is written, so it is at least `0x140`; no
   allocation site has been read to confirm the figure.~~ **ANSWERED by §3's "Two classes, not one" note (OPUS,
   2026-09-25); this item is propagated 2026-09-25 (FABLE, Claude Opus 5.5).** There are two sizes because there are
   two classes. The base `PhyreClassDescriptor` family reaches `+0xFC`, since its constructor `00632D80` writes nothing
   beyond, so it is `0x100`. `PClassDescriptorDynamic` is **`0x140`**: `0059AC00` allocates exactly `0x140`
   (`0059AD27`) and runs its constructor `00632E80` on the block (`0059AD49`), and that constructor writes up to
   `+0x138` (`00632F11`). Re-read for this propagation.
4. ~~**`PCD-4`** — the `+0x100` / `+0x102` guard's meaning, and what state makes the two words equal.~~ **ANSWERED FOR
   THE CLASS'S OWN CODE (2026-09-26, OPUS, owner, on `FABLE-REQ-OPUS-PCD4-GUARD-WORDS-ALWAYS-EQUAL`; FABLE's register
   answer re-derived).**
   - **Every writer that belongs to `PClassDescriptorDynamic` changes both words identically.** These are word-width
     writes, verified at each site:
     - the constructor `00632E80` zeroes both with one dword store (`00632ED3`);
     - the linkers `00639290` and `0063D410` increment both (`006392F0` / `006392FA`, `0063D4C5` / `0063D4CF`);
     - the unlinker `0063D790` adds `0xFFFF` to both (`0063D7C2` / `0063D7C9`);
     - the reset zeroes both with one dword store (`0063D5E0`).
   - **So, for a descriptor written only by that code, the two words are one member count, and the guard reduces to
     "member count non-zero".** Equal and zero resets. The reset re-initialises the six member-list heads only when the
     descriptor holds no members.
   - **What is not proven: "always equal" for every object in the image.** OPUS's own image-wide sweep of word-width
     `mov/add/sub/inc/dec/and/or/xor` at `[reg + 0x100]` and `[reg + 0x102]` finds **five more functions** that write
     both words, with independent values: `00266530`, `003AAA50`, `0041B550`, `00552250` and `005528C0`. It finds one,
     `00269F40`, that writes `+0x102` alone.
     - `003AAA50`'s receiver is a stack local (`003AAA57 lea rbp, [rsp - 0x198]`), not a descriptor.
     - The other four receivers (`this` in `rcx`, `[rbx + 0x160]`, and a pointer from an array at `[rdx + r10·8 + 8]`)
       are **not shown to be this class**, and **not shown not to be**.
     - FABLE's "an image-wide sweep … finds no other function touching both" is therefore too strong as worded. The
       conclusion holds conditioned on those receivers being other types. *(Routed back to FABLE for the register
       row.)*
   - **What the two parallel counts were meant to differ on is not in the image.**
5. ~~**`PCD-5`** — `0063E410`, called at the end of a successful rebind, is unread.~~ **Read 2026-09-14 (FABLE):** it
   recomputes two totals of `+0xF0` over the parent chain.
   - **`+0xF4`**: zeroed, then summed over the descriptor itself and each ancestor reached through `+0x78`. The walk
     stops before the fixed root descriptor at `02CF8270` or at a null parent (`0063E416`–`0063E448`).
   - **`+0xF8`**: the parent's own `+0xF8` plus this descriptor's `+0xF0` clamped at zero, or just the clamped value
     when there is no parent (`0063E44A`–`0063E47F`).
   - Since `+0xF0` is the negated copy of the parent's `+0x38` written earlier in the same rebind, both totals are running
     sums of that value down the class chain.
   - Differences between the two: `+0xF4` excludes the root and admits negative terms, while `+0xF8` builds on the
     parent's cached total and never adds a negative.
   - **Not established:** what `+0x38` measures, and so what the two totals mean. *(answered: see the 2026-09-20 reading - `+0x38` is this contract's own size field, the one `0063C910` passes to `memcpy`; 2026-10-02, OPUS)*

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| **six circular intrusive lists at `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0`, `+0xB0`** | **re-read by me**: `0063D550` does `lea rax,[rcx+N]` / `mov [rax],rax` / `mov [rax+8],rax` for each of the six | 1 | PROVEN |
| a list is empty when its head points at itself | **re-read**: `00633390`'s `cmp rdi, r14 / cmove rdi, rbp` on the `+0x90` walk | 1 | PROVEN |
| **the type name is a `char *` at `+0x30`** | **re-read**: `006388C0 mov rsi, [rcx+0x30]` / `test rsi,rsi` / `xor al,al` on null / `movzx ebx, byte [rsi]` | 1 | PROVEN |
| **`+0x30` is `[+0x138]` with bit 0 cleared, so `+0x138` is a tagged pointer** | **re-read**: `0063D61B mov rax,[rbx+0x138]` / `movzx ecx, byte [rbx+0x138]` / `and ecx,1` / `sub rax,rcx` / `mov [rbx+0x30], rax` | 1 | PROVEN |
| the sub-object at `+0x70` is released first, after the vftable is overwritten | **re-read**: `006333BC mov [rcx], rax` then `006333DC mov rcx,[rcx+0x70] / call 0063D640` | 1 | PROVEN |
| **the destructor runs TWO free-walks (`+0x90`, `+0xA0`) and then FOUR drain loops (`+0x80`, `+0x90`, `+0xA0`, `+0xB0`) that free nothing** | **EXECUTED**: the pilot compares the freed addresses in order, and a case with one owned node in each of the four lists frees **four**, not eight. This row replaces a claim that the destructor walks four lists | 1 | PROVEN |
| **a node in `+0x80` or `+0xB0` is never released, whatever its ownership bit** | **EXECUTED**: same case; and the drain bodies at `006334C0`, `006334E4`, `00633508`, `00633533` contain no `call` | 1 | PROVEN |
| after the drains every walked head points at itself and every survivor is self-linked | **EXECUTED**: the object and the node heap are both compared | 1 | PROVEN |
| the vftable is written TWICE, with different constants | **re-read**: `006333B5 lea rax, [rip+0x724e04]` -> `00D581C0`, and `00633561 lea rax,[rip+0x6fdc00]` -> `00D31168` | 1 | PROVEN |
| **`+0xE8` is a high-water mark wound back only when it is the topmost** | **re-read**: `006333BF`–`006333D3` against the global at `02CF8260` | 1 | PROVEN |
| the parent is at `+0x78`, and four fields are copied from it | **re-read**: `0063D5E6`–`0063D609`, including `neg eax` into `+0xF0` | 1 | PROVEN |
| **a list node is `{next, prev, ..., owned ptr at +0x18, flag at +0x20}`, and bit 0 of the flag gates BOTH the unlink and the two frees** | **re-read by me**: `00633415 test byte [rbx+0x20], 1` guarding the unlink at `00633422`-`0063342C` and the two `call 0x584730` at `0063343A` and `00633443` | 1 | PROVEN |
| the walk advances the cursor before unlinking the current node | **re-read**: `00633408 mov rax, [rdi]` at the top of the body, before `0063341B` | 1 | PROVEN |
| **six `test rax, rax` guards in `0063D550` are provably dead** | **re-read**: each follows a `lea rax,[rcx+N]`, which cannot be null | 1 | PROVEN |
| descriptors are `_aligned_malloc` storage freed by `_aligned_free` | `005847E0`'s `00584730` call, and `00584730` → IAT `008C2B70` → `_aligned_free`, resolved in [the cluster header contract](../Phyre-Asset-Container/CONTRACT-phyre-cluster-header.md) §5 | 1 | PROVEN |
| the deleting-destructor flag convention: bit `0x1` frees, ~~bit 2 takes the CFG path~~ bit `0x4` with it calls the `ret 0` stub `0016D6A0` and frees nothing *(corrected 2026-10-03, OPUS, S-49 point 3)* | the source page's `005847E0` | 1 | PROVEN |
| 4,557 generated reflection functions in 42 families, 1,149 deleting destructors | the source page's census, **corrected by its own falsification pass**; the total survived exactly and the family split was revised | 1 | PROVEN |
| any execution of any of this | ~~**none**; §13~~ *(answered: see the EXP-097 execution and the PCD-3 answer; 2026-10-02, OPUS)* | none | UNKNOWN |
| what the six lists hold, what bit 0 tags, the descriptor's size, the `+0x100` guard, `0063E410` | first four **not established** (`PCD-1`…`PCD-4`) *(2026-09-25, FABLE: `PCD-1` PARTIAL — five of six lists named;
`PCD-2` ANSWERED — borrowed-name tag; `PCD-4` answered in the register; see §14)* *(2026-09-26, FABLE, Claude Opus 5.5: `PCD-3` is ANSWERED too — the base descriptor is `0x100` bytes and the dynamic one `0x140`, §3 — and `PCD-1` is SUPERSEDED, its last list carried by `BL-8`)*; `0063E410` **read 2026-09-14** — `PCD-5` answered (open item 5: recomputes `+0xF4`/`+0xF8` over the parent chain) | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The six dead guards, checked exhaustively rather than by example

`0063D550` is 233 bytes / **62 instructions**. It contains **exactly six** `test rax, rax` sites, and
**every one** is immediately preceded by a `lea rax, [rcx + N]`:

| guard | preceded by |
|---|---|
| `0063D576` | `lea rax, [rcx + 0x50]` |
| `0063D589` | `lea rax, [rcx + 0x80]` |
| `0063D59C` | `lea rax, [rcx + 0x90]` |
| `0063D5AF` | `lea rax, [rcx + 0xA0]` |
| `0063D5C2` | `lea rax, [rcx + 0xB0]` |
| `0063D5D2` | `lea rax, [rcx + 0x60]` |

Six guards, six list heads, and no `test rax, rax` anywhere else in the body — so "six, all dead" is
exhaustive, not a sample. The claim holds.

### The initialisation order is not the layout order

The six heads are written in the order **`0x50`, `0x80`, `0x90`, `0xA0`, `0xB0`, `0x60`** — `+0x60`
is initialised **last, not second**. §15 lists them ascending, which is the *layout*; a reconstruction
that follows the document's order writes the same six fields in a different sequence. That is
harmless here because each is an independent self-link — **but it is only harmless because nothing
between them reads another**, which this pass checked rather than assumed.

*(The packed namespace contract makes the same distinction about its swap order; this is the second
place in the database where an ascending list is the layout and not the code.)*

### Confirmed at the byte level

| claim | image |
|---|---|
| the vftable is written **twice, with different constants** | `006333B5 lea rax, [rip → 00D581C0]` / `mov [rcx], rax`, and `00633561 lea rax, [rip → 00D31168]` / `mov [r15], rax` — **two distinct vftables** |
| `+0x138` is a tagged pointer, `+0x30` is it with bit 0 cleared | `0063D61B mov rax, [rbx+0x138]` / `0063D622 and ecx, 1` / `0063D625 sub rax, rcx` — the clear is a **subtract of the extracted bit**, which is exactly `p & ~1` |
| the type name is a `char *` at `+0x30` | `006388CA mov rsi, [rcx+0x30]` (three instructions into the function §15 cites by its entry) |
| the walk advances the cursor before unlinking | `00633408 mov rax, [rdi]` then `0063340B mov rdi, rax`, before anything is unlinked |

*Status 2026-09-26 (FABLE, Claude Opus 5.5): in the register `PCD-2`, `PCD-3` and `PCD-4` are now ANSWERED and `PCD-1` is SUPERSEDED (five of six lists named; the remaining list is carried by `BL-8`), so the "stay open" below is history. Nothing was executed; §13 is still unchanged.*

**Not claimed:** none of this was executed — §13 is unchanged — and `PCD-1`…`PCD-4` stay open
(`PCD-5` was read 2026-09-14 — open item 5), as does the census this contract inherits from its
source page.

## 16. Parity plan

**Constructed and run, 2026-09-12** — `STRUCTURAL`, `STATE-TRANSITION`, `CALCULATION` and
`EDGE-CASE` are `COVERED` by `diff_class_descriptor.py` **for the reset and rebind**: the six list
offsets, the name pointer and its tag, the parent copies and the negation, and the guard at the one
value that can expose a mis-shifted 16-bit read.

**The destructor is now covered too** — `STRUCTURAL`, `STATE-TRANSITION`, `CALCULATION` and
`EDGE-CASE` by `diff_class_descriptor_dtor.py`: the node layout, the ownership bit, both free-walks
and all four drains, the two vftable writes, and the counter at and around the global.

**Two of the three scripted callees are no longer scripted.** `0063D640` and `006B6700` were executed as real shipping bytes by EXP-097 and re-read here instruction by instruction (§13a), so `INTEGRATION` now has native semantics for both. **`_aligned_free` stays a boundary and not a claim** — the pilot compares the addresses handed to it, which is the observable that matters, and the allocator's internals are not this contract's business.

**What remains uncovered is a different question than it was, and a smaller one:** not what the teardown DOES, but what the lists MEAN. `PCD-1` is untouched by any of this — EXP-097 says so itself — and the `+0x70` sub-object is still identified only by what is done to it.

## 17. Related## 17. Related

- [`class-descriptor-and-metadata-system.md`](class-descriptor-and-metadata-system.md) — the
  mechanism, the family census and the two offset corrections this contract re-verified.
- [`member-registration-and-the-recovered-field-schema.md`](member-registration-and-the-recovered-field-schema.md)
  — what attaches to `+0x80`.
- [`../Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md`](../Phyre-Asset-Container/CONTRACT-phyre-packed-namespace.md)
  — the same schema as it appears in a file, from a completely independent source.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `005DD890` | 581 | **container teardown, not registration** (`Runtime.Container.Teardown` in `99-Unresolved-Residual/residual-109-classification.tsv`): two loops that walk the object's pointer arrays (`+0xA8`/`+0xA0`, then `+0xB8`/`+0xB0`, counts masked of bit 31 at `005DD8BC`/`005DD921`), null each slot (`005DD8DD`), and per element run `00625EF0` (tests `+0x60`) → `0062BB40` (release: `0062B090` polls `00623DB0` with `Sleep`, zeroes `+0x60`, walks `+0x18`/`+0x20`) → `00616C00` → free `00584730`, nine frees total. Reached from `005D46D0` (a 19-byte atexit thunk, `call 005DD890` at `005D46D7`) and the CRT startup thunks `0089FC9B`/`008B0B30`/`008B7C80` — a static-destruction body for a global double-array container. **Belongs to the CRT static-teardown family, not this contract** — nothing in it touches a descriptor field. |

> **Corrected 2026-09-14 (FABLE, FINAL-AUDIT pass 22): `005DD890` is a teardown loop, not a registration.** It walks
> the pointer array at `+0xA8` (count at `+0xA0`, top bit masked). For each slot it nulls the slot and destroys what was
> there (`005DD8D0`–`005DD91C`):
>
> 1. `00625EF0` tests the element's `+0x60` (`setne`).
> 2. When that is set, `0062BB40` releases the element. It first calls `0062B090`, which polls `00623DB0` with `Sleep`,
>    then zeroes `+0x60` and walks the element's own array at `+0x18` / `+0x20`.
> 3. `00616C00` runs, then the free `00584730`.
>
> Further frees follow. Nothing in the loop touches a descriptor field. The same test / release / `005DE210` / free
> sequence opens `00650D40`, which the ledger files under **Platform**. It runs twice there (`00650D75`–`00650DE3`),
> after which `00650D40` allocates replacements and builds them (`00650E05`–`00650E90`).
> That shared sequence is the page's whole crossing into Platform. Where `005DD890` belongs goes back to SWE2-FRONTIER
> (`FABLE-NOTICE-FRONTIER-005DD890-PLACEMENT`).
>
> **Placed 2026-09-14 (SWE2-FRONTIER): `005DD890` is CRT static-teardown, not part of this contract.** The row above now
> reads it correctly: a static-destruction body for a global container holding two pointer arrays, registered through
> the CRT atexit machinery (`005D46D0`, 19 B thunk; `0089FC9B`/`008B0B30`/`008B7C80`). Its census home is
> `Runtime.Container.Teardown`. **`00650D40` stays Platform-owned** — it opens with the same test/release/`005DE210`/free
> sequence because it releases the same element type, then allocates and builds replacements; that is a
> release-and-rebuild under the Platform layer, and the shared sequence is exactly the crossing the paragraph above
> describes.

## SWE2-EC7-40 update (2026-09-19) - `0062BB40`

`0062BB40` (360 B) is a class-descriptor body - `0062B090` plus four vcalls. Interior anchor `0062BB53` (the `0062B090` call).


## §14b. Three full-size instances per class, not one (2026-09-19, OPUS)

The layout table above ran from `+0xB0` to `+0xE8`, leaving `+0xC0`–`+0xE0` undeclared. The
constructor zeroes all five of those slots together (`00632E16`, `00632E1D`, `00632E24`,
`00632E2B`, `00632E32`), and **three of them have named one-instruction setters**:

```
0063DC80   mov qword ptr [rcx + 0xC0], rdx ; ret
0063DF90   mov qword ptr [rcx + 0xC8], rdx ; ret
0063DFA0   mov qword ptr [rcx + 0xD0], rdx ; ret
```

`PDeferredLightingBase`'s registrar `006442E0` calls all three in sequence, and **the three buffers
it hands them are consecutive**:

| slot | buffer | |
|---|---|---|
| `+0xC0` | `02CF9970` | the default instance, already in `members/phyre-default-instances.tsv` |
| `+0xC8` | `02CFDB50` | `+0x41E0` |
| `+0xD0` | `02D01D30` | `+0x41E0` |

The class's instance size is `0x41D8` and the stride is `0x41E0` — the same object three times
with eight bytes of alignment padding between them, laid out as one array by the compiler.

**What they are for is not established.** Three parallel full-size instances behind reflection
metadata has an obvious candidate reading, and the obvious reading is exactly what this contract
should not assert without a consumer: `0063C910` reads `+0xC0` and nothing read here reads `+0xC8`
or `+0xD0`. **The slots, their setters and their contents are recorded; their purpose is open.**

> **Purpose read 2026-09-25 (FABLE, Claude Opus 5.5): `+0xC8` and `+0xD0` are byte masks over the instance, not
> instances.** They are built by `00639C80`, the function the metadata page already names as `+0xD0`'s reader. The
> sentence above ("nothing read here reads `+0xC8` or `+0xD0`") is superseded. Static.
> - **Start.** `00639C80` fills `+0xC8` with `0xFF` and `+0xD0` with 0 over the instance size (`00639CD3`,
>   `00639CE4`). It then copies the parent's two masks over the parent's part, through getters that only it calls
>   (`0063C1A0` for `+0xC8`, `0063C5E0` for `+0xD0`).
> - **Per member of `+0x80` whose type has no descriptor.** It clears the member's bytes in `+0xC8` (`0063A033`). In
>   `+0xD0` it writes the member's `WriteMask` annotation value, or `0xFF` bytes when there is none
>   (`0063A03D`–`0063A084`). The annotation is found by `006B67F0` on the member's `+0x38`, and its value is read
>   through the annotation's slot 1, which returns `annotation + 0x30`.
> - **A member whose type has a descriptor** gets that type's two masks copied in, once per element.
> - **Members with flag bit 1** (member `+0x28`), and kind-2 members with flag bit 6, have their `+0xC8` bytes cleared
>   and their `+0xD0` bytes left at 0.
> - **So `+0xC8` marks the bytes no reflected member covers.** The deserializer merge `0063A790` keeps exactly those
>   bytes from the live object, `dst = (src & ~mask) | (dst & mask)`
>   ([the cluster-header page](../Phyre-Asset-Container/the-cluster-header-and-what-the-loader-rejects.md)).
> - **`+0xD0` marks the member bits that carry data.** The image's only annotation is `WriteMask = 0x7FFFFFFF`, on
>   every `m_count`. It takes out bit 31, which §3's counted buffers use as "borrowed" (`BL-5`).
> - ~~*Not established:* a reader of `+0xD0` other than `00639C80` itself. The Phyre band's other `[reg+0xD0]` loads
>   were not opened.~~ **Opened 2026-09-26 (FABLE, Claude Opus 5.5): no other body in the Phyre band reads the mask.**
>   `members/d0_loads.py` lists every qword load `[reg+0xD0]` in `00590000`–`006C0000`, eight functions. Its control
>   is the getter `0063C5E0`, which it lists.
>   - Two are `00639C80` and its getter.
>   - Two are whole-object copy routines that move `+0xC8`, `+0xD0` and their neighbours field by field.
>   - Four sit together in the `0065xxxx` band and hold a pointer at `+0xD0`. One passes it on to another routine and
>     one tests it for null. Two treat it as a tagged reference: one compares the pointee's byte `+8`, the other hands
>     it to a release that switches on that byte (0, 1 or 2). None of the four loads the descriptor's `+0xC8` mask or
>     its list heads `+0x80`, `+0x90` or `+0xA0`.
>   - None indexes `+0xD0` by a member offset. The mask's consumer, if any, is not a qword load in this band.
>   - *Not claimed:* the rest of the image. A reader outside the band, or one that reaches the mask through
>     `00639C80`'s output buffer by another route, is not excluded.
`+0xD8` and `+0xE0` are zeroed by the constructor with the other three and have no setter at all.

## SWE2-EC7-79 update (2026-09-20) - `00625EF0` occupancy getter measured

`00625EF0` (8 B) is the `+0x60` occupancy test the descriptor
callers read: returns `dword[rcx+0x60] != 0`.
Interior anchor `00625EF4` (the `setne al`).

## ASTRA's startup capture consumed, and the root confirmed from the image — 2026-09-20 (OPUS)

`ASTRA-RETURN-OPUS-PHYRE-STARTUP` returned a live startup capture — 173 default spans, 34,392
bytes, per-class flags, and **103 blank/root rows pointing at `02CF8270`, named `PBase`, size 0,
parent 0** — and asked that only audit-supported values be integrated.

**The root is confirmed statically, which is the strongest form this could take.** A live
reading and a static derivation are different evidence classes, and here they agree without
either being assumed. `00164180` is the root's static constructor and it is eight instructions:

```
00164184  lea   rcx, [02CF8270]          ; the descriptor
0016418B  call  006318A0                 ; the PClass constructor
00164190  lea   rax, [00D582D0]          ; its vftable
00164197  mov   dword [02CF82A8], 0      ; 02CF8270 + 0x38 — THE SIZE, written zero
001641A1  lea   rcx, [008AF190]          ; the destructor thunk
001641A8  mov   qword [02CF8270], rax    ; the vftable into +0x00
001641B3  jmp   atexit
```

`+0x38` is this contract's own size field — the one `0063C910` passes to `memcpy` — and it is
written **0** explicitly. `+0x78`, the parent, is never written in this constructor, so it stays
null. The literal `PBase` exists in `.rdata` at `00D58400` and is materialised inside the
constructor `006318A0`, whose first act on the object is the `+0x50` self-link this contract
already documents (*"unlinks it from whatever list it is in and self-links the head"*). So
**`02CF8270` is a real, constructed, zero-size `PBase` with a null parent** — not an absent
descriptor, and not a null pointer. ASTRA's live reading is right and the image says the same
thing for its own reasons.

**What that changes for `+0x78`.** The layout row reads *"the parent descriptor, or null"*. That
stays true of the root itself, but the sampled data says a **blank or root parent in a derived
class is not 0** — 103 of the sampled rows carry a pointer to this zero-size `PBase`. A
reconstruction that tests `parent == null` to find a root will therefore miss 103 of them, and
one that dereferences the parent will find a valid descriptor whose size is zero. Both
behaviours are now recorded rather than left to be discovered.

**PENDING AN AUDIT THAT HAS NOT RUN, and I should not have written the numbers below without saying so.** ASTRA's return asks to *"integrate only audit-supported sampled values"*, and its board task depends on `ASTRA-REVIEW-EXP124-RAW` - an independent audit of exactly these 173 defaults and parent links, assigned to SWE2-AUDIT-SPEC, which is **still READY and not done**. The board refused my claim on that dependency and that refusal is what surfaced this. **The static derivation above is unaffected**: the root's construction is read from the shipping image and owes the audit nothing. **Everything in the paragraph below is live, sampled and UNAUDITED**, and must not be consumed as audit-supported until that task closes.

*Acceptance recorded 2026-09-28 (OPUS, ASTRA-RETURN-OPUS-PHYRE-AUDIT-CURRENT-STATE); the paragraph above is kept as the record of what was true when it was written.* **The audit it waited for has run and ACCEPTED these numbers.** `ASTRA-REVIEW-EXP124-RAW` went DONE on 2026-09-21 (SWE2-AUDIT-SPEC). It re-derived from `defaults.bin` / `defaults.tsv`, not from this page:
- 173 spans and 34,392 bytes;
- 166 with bit 31 set; 7 bit-31-clear all-zero and 26 bit-31-set all-zero; 140 non-zero; 7 all-`0xA5`;
- the 70 + 103 parent partition;
- 0 per-row hash mismatches, on the canonical EXE.

**Which review file.** The board's result reference names `REVIEW-EXP124-POOL-DEFAULTS-RAW.md`, which is not in the current checkout. The review present is `Tools/work/SWE2-AUDIT-SPEC/REVIEW-EXP124-PHYRE-STARTUP-GLOBALS.md`. It is headed with the same task id and carries the same verdict and figures: the same review under another file name.

**The review's limits stay with the numbers:**
- sampled values only: no constructor or copy was traced, nor the `0xA5` arm or the bit-31 write;
- the seven unprepared all-zero classes keep unknown defaults;
- a parent link is not a subobject offset or ownership proof;
- `PBase`'s size-zero / null parent is a read of the descriptor cell.

Nothing was recaptured for this note.

**What is offered with limits, and not generalised.** The default-buffer flag distribution is
sampled live and is consumed as such: **166 of 173 with bit 31 set, 26 prepared-zero, 7
unprepared-zero, 7 all-`0xA5`**. Two cautions ASTRA asked for are adopted verbatim because they
are the kind of thing a reconstruction gets wrong silently:

* **Do not assume the gaps are zero.** `0063C910` does `if (rdx) memcpy(instance, rdx,
  [descriptor+0x38])`, so a non-null `+0xC0` means the bytes are copied *whatever they contain*.
  An all-`0xA5` span is a fill pattern, not a default value, and copying it produces an instance
  that looks initialised and is not.
* **Bit 31 set is not a usable zero-default.** 166 of 173 carry it; reading it as "the default
  is zero" would license skipping the copy for almost the whole population.

**Held open exactly as returned:** the 7 unprepared defaults, portable pointer semantics, and
the 4 mapping gaps — the last being the four D3D descriptor addresses, answered separately today.
**That answer was half right and the half that was wrong is corrected below: the supplied
addresses really are thread-safe-static guards, but "the object sits at guard − 0x58" is not the
route and the four real descriptors are elsewhere entirely.**

## The four D3D descriptors, and a control over every address in the parent map

`ASTRA-CONTRA-OPUS-PHYRE-CORRECTED-DESCRIPTOR-IDENTITY` (2026-09-20) was right. Re-derived from
the image rather than accepted:

| class | registrar | descriptor | the guard that was in the map | size | align |
|---|---|---|---|---|---|
| `CD3D11_BLEND_DESC` | `00613800` | `02CF6320` | `02CF6678` | `0x108` = 264 | 4 |
| `CD3D11_DEPTH_STENCIL_DESC` | `00613A30` | `02CF5A80` | `02CF6618` | `0x34` = 52 | 4 |
| `CD3D11_RASTERIZER_DESC` | `00613E80` | `02CF52C0` | `02CF65B8` | `0x28` = 40 | 4 |
| `D3D11_RENDER_TARGET_BLEND_DESC` | `00614640` | `02CF5EB0` | `02CF6558` | `0x20` = 32 | 4 |

### Why the four guards were mistakable, and why the corrected four are not (OPUS)

**Consuming `ASTRA-RETURN-OPUS-PHYRE-STARTUP`, 2026-09-20.** EXP-124 stopped on this: its first
identity control failed because `02CF6678` yields `0x10` where a name pointer belongs, and it asks
that the mappings be reconciled *before another hierarchy capture*. The table above already
corrects them; what was missing is **why the wrong four were plausible**, which is what stops the
same substitution happening again.

**The four guards are one array.** They are spaced **exactly `0x60` apart** —
`02CF6558 → 02CF65B8 → 02CF6618 → 02CF6678` — which is a contiguous run of four `0x60`-byte
records, not four independent class descriptors. **The four corrected descriptors are spaced
irregularly** (`0x7C0`, `0x430`, `0x470` between them in address order), which is what independent
registrations look like. Regular spacing was the tell and it was there to be seen.

**And one of the guards sits inside another class's registrar.** `02CF6558` is referenced from
within `00613800`'s own body — the `CD3D11_BLEND_DESC` registrar — at `00613991`, `00613999`,
`006139A5` and `006139ED`. A *class* descriptor for `D3D11_RENDER_TARGET_BLEND_DESC` would have no
reason to appear there. **`02CF6558` is not a descriptor at all. It is an MSVC thread-safe
local-static guard word** (re-read 2026-09-25, OPUS):

- `00613991` compares it with the thread's epoch.
- `00613999` enters `_Init_thread_header` (`008092FC`).
- `006139A5` tests it for `-1`.
- `006139ED` leaves through `_Init_thread_footer` (`0080929C`).

What it guards is the `"RenderTarget"` **member** descriptor at `02CF64F0`, constructed by
`00632A70` at `006139DB`. So four guard words of consecutive member statics were mapped as four
classes. Once initialised, a guard word holds an epoch count, which is *consistent with* the `0x10`
EXP-124 read where a name pointer belongs. That reading is not measured.

**The corrected address is confirmed from the registrar's own instructions**, which is the check
available without a live process: `00613834` is `lea rbx, [rip+0x26e2ae5]` resolving to `02CF6320`,
and `00613886` is `mov qword ptr [rip+0x26e2a93], rax` **storing into it**. The registrar takes and
writes that cell; it never touches `02CF6678`.

> **Neither set can be checked statically, and that is the point of EXP-124's control.** All eight
> addresses lie past raw section data — they are BSS and ship zero — so reading `+0x30` from the
> image proves nothing either way. Only a live read distinguishes them, which is exactly what the
> experiment's identity control did. **A static census cannot validate a descriptor address here**,
> and any future map of these classes should be checked the same way rather than by derivation
> alone.

**So the reconciliation EXP-124 asked for is complete**: the four corrected descriptors stand, the
reason the wrong four were adopted is recorded, and a re-capture can proceed against the table
above. `CD3D11_DEPTH_STENCIL_DESC`, `CD3D11_RASTERIZER_DESC` and `D3D11_RENDER_TARGET_BLEND_DESC`
were never observed by that experiment — only the first was attempted — so they remain
**unobserved rather than confirmed**, and that is a coverage gap, not a resolved one.


Each registrar does `lea rcx,[descriptor]` then `call 00632C90` with `r8` = a **literal `.rdata`
name string** and `r9d` = the size; `00613886` then stores the vtable at the descriptor's `+0`.
**The names were never unavailable** — the claim that the image could not say which class is which
was made without searching this store, which already carried all four sizes and two of the
registrar addresses. The sizes are **hex**; written bare they read as decimal and every one would
be wrong. All four match the real Direct3D 11 structure sizes.

These four are **roots by construction, not by absence of evidence**: `00632C90` takes no parent
argument and writes `mov qword ptr [rcx + 0x78], r10` with `r10` zeroed at entry — unlike
`00632D80`, which takes a 6th argument for `+0x78`.

**The control, run over all 330 rows rather than the four.** An address is decided by what the
image does with it as `rcx`:

- reaches a **descriptor constructor** — `00632C90` or `00632D80`, found by their own
  `+0x30`/`+0x38`/`+0x3C` writes rather than from a list — **or** a **descriptor-shaped
  consumer**: `006388C0`, which does `mov rsi,[rcx+0x30]` and then `movzx ebx, byte ptr [rsi]`
  (§ the name is a `char *` at `+0x30`), or `0063BC00`, which reads `[rcx+0xD8]` and `[rcx+0xFC]`
  and dispatches `[rcx] → [rax+0x60]` → **a descriptor**;
- reaches `008092FC` `_Init_thread_header` and neither of those → **a 4-byte guard**.

**330 of 330 decided: 326 descriptors, 4 guards, 0 undecided.** The blast radius is exactly those
four. A first version of this control used only `00632C90` and decided 15 of 330 — reported here
because "only four rows are wrong" would otherwise have rested on 4.5% of the population.

**The cause is fixed in `gen_phyre_parent_chain.py`, not only in the rows.** Its sweep took
whatever was last `lea`'d into `rcx` at a call to a registrar, and in `00617E60` a guard's
`lea rcx` sits above an intervening call. *The obvious repair was worse and is recorded in the
generator:* dropping the caller-saved registers at every call is correct by the ABI and took
recovery from 330 to 315 — it removed the four wrong answers and **eleven right ones**, and also
destroyed parent resolution entirely (182 → 0), because registrars really do keep the descriptor
in `rcx` across a call. The candidate is now **tested** against the control above instead. After
the fix: 330 of 330 descriptors, 182 non-null parents, 181 resolved, both size controls at 0
violations.

*Class of evidence:* the root's construction is **static, read from the shipping image**; the
173-span flag distribution is **live and sampled**, and is recorded as a distribution over what
was sampled rather than over all reflected classes.


## Cross-subsystem neighbours — 2026-09-25 (FABLE, Claude Opus 5.5)

**Presentation — TAG ONLY (shared callee, shared allocator).** The descriptor code crosses into functions that the
ownership table tags `Presentation`, but none of the crossings is a dependency on rendering.
- **The main case is `00639A60`.** The constructor `00632E80`, `0063BC00`, `0063C910` and §14b's mask builder all run
  it immediately before `00639C80`. Its domain tag is `Presentation.Rendering.ShaderMaterial`, but what it does is the
  reflection construct-and-compare ([the metadata page](class-descriptor-and-metadata-system.md)).
- **The other Presentation edges run the other way.** Renderer code frees aligned blocks through the same
  `_aligned_free` (`00584730`) that the descriptor destructor uses. It looks types up by name through `006388C0`, as
  code in every other layer does.
- **Actor - SERVICE (1 edge).** ActorStorage_InitializeRecord (`00266530`) reaches bodies filed to Actor: `00265B60` - shared machinery across the layer boundary, no shared ownership.
- **ActorEntity - CLIENT and SERVICE (7 edges).** ActorStorage_InitializeRecord (`00266530`) is called by bodies filed to ActorEntity: ActorStorage_AllocateAndInitializeRecords (`002679F0`); ActorStorage_InitializeRecord (`00266530`) reaches bodies filed to ActorEntity: `00266AD0`, `00266BD0`, `00268EA0`, `003DB280` (+2 more) - shared machinery across the layer boundary, no shared ownership.
- **CoreRuntimeScheduling - MECHANICAL (1 edge).** Shared-helper fan-in on `001EDEC0`. All 1 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Movement - SERVICE (2 edges).** ActorStorage_InitializeRecord (`00266530`) reaches bodies filed to Movement: `00265FF0`, `00268380` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (2 edges).** `00269F40` is called by bodies filed to Script_VM_Native_Bridge: `0034B9A0`, `0034C170` - shared machinery across the layer boundary, no shared ownership.
- **UI - SERVICE (27 edges).** `00552250`, `005528C0` reach bodies filed to UI: `002901D0`, `0035C080`, thunk_FUN_0028fcb0 (`0035C140`), `00550470` (+22 more) - shared machinery across the layer boundary, no shared ownership.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-phyre-class-descriptor-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00617E60` | 543 B | calls `006388C0(02CF1540)`, then registers four members of the class `02CF1540`, each once under its thread-safe guard (dwords `02CF65B8`, `02CF6618`, `02CF6678`, `02CF66D8`, each compared with the epoch dword `+4` of this thread's TLS block at index dword `02EAED3C`; `008092FC` before, `0080929C` after): `00632960(member, 02CF1540, type, name, offset, 0x10, 0, 0)` with (`02CF6560`, `00613E80()`, 'm_rasterDesc', 4), (`02CF65C0`, `00613A30()`, 'm_depthDesc', 0x2C), (`02CF6620`, `00613800()`, 'm_blendDesc', 0x60) and (`02CF6680`, `0062FFC0()`, 'm_stencilRef', 0x188), registering the exit routines `00808B90` with `008AEDB0`, `008AECE0`, `008AEC60` and `008AEE10`; finally tail-jumps to `00639450(02CF1540)` | `00617E7B`, `00617EF2`, `00617F65`, `00617FD8`, `0061804B` |
| `006318A0` | 440 B | once, under the thread-safe guard dword `02CF94EC` (TLS epoch at index dword `02EAED3C`; `008092FC` / `0080929C`), initialises the static at `01F2E330`: qwords `01F2E330`/`01F2E338` = `01F2E330`, `01F2E340`/`01F2E348` = `01F2E340`, dword `01F2E350` = 0, `01F2E358`/`01F2E360` = `01F2E358`, with exit routine `00808B90(008AF490)`; then constructs `o` = `rcx`: two-pointer self-linked heads at `+0x50`, `+0x60`, `+0x80`, `+0x90`, `+0xA0` and `+0xB0`, a three-pointer one at `+8` with dword `+0x20` and qword `+0x28` = 0, qword `+0x30` = 'PBase', dwords `+0x38` and `+0x3C` = 1, qwords `+0x40`, `+0x48`, `+0x78` and `+0xC0`..`+0xE0` = 0, qword `+0x70` = `01F2E330`, dword `+0xE8` = dword `02CF8260` (which it then increments), dword `+0xEC` = -1, qwords `+0xF0`/`+0xF8` = 0, and vtable `00D581C0` then `00D58248` at `[o]`; returns `o` | `006318D7`, `00631A04`, `00631904`, `006319B5`, `006319BB` |
| `00635980` | 507 B | calls `006388C0(02CF8980)`; once under guard dword `02CF94E4` (TLS epoch at index dword `02EAED3C`; `008092FC` / `0080929C`) it appends the node `01F2E290` to the list at `02CF8A20` (tail qword `02CF8A28`) unless `005A0470(02CF8980, 'GetGlobalNamespace')` is non-zero, registering exit `00808B90(008AF1C0)`; stores `00D58FE0` and `006373D0` to qwords `01F2E2C0`/`01F2E2C8` and `01F2E2C0` to `01F2E2B8`; once under guard `02CF94E8` does the same with node `01F2E2E0`, list `02CF8A10` (tail `02CF8A18`), `005A7A40(02CF8980, 'getClassDescriptor')` and exit `008AF3D0`; stores `00D59040` to qword `01F2E310`, `0063BA10` and dword 0 to the 16 bytes at `01F2E318` (their last dword copied from an unwritten stack slot) and `01F2E310` to `01F2E308`; calls `00639160(qword [02CF89F0], 02CF8980)`; sets `0x40000000` in dword `02CF8A7C`, and when it has `0x1` self-links qwords `02CF8988`..`02CF8998`, zeroes dword `02CF89A0` and qword `02CF89A8` and tail-jumps to `006388C0(02CF8980)`, else returns | `006359E3`, `00635A10`, `00635A8A`, `00635B22`, `00635B2D` |

### Crossings into other layers - functions this page's newest interior rows name (OPUS, 2026-10-03)

- **Resource - SERVICE (23 edges).** `0062FFC0` is also called by `00585270`, `005862F0`, `00586470`, `005865F0` (+8 more), filed to resource (+11 more edges of the same shape) - shared machinery across the layer boundary, no shared ownership.
