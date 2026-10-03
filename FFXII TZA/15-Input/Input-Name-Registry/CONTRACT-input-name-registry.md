---
contract: register one input name into its string-keyed startup list
category: 15-Input
scope: operation
level: L2
readiness: RUNTIME VALIDATED and DIFFERENTIAL TESTED
confidence: PROVEN
implements: 15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md
entries: ["00879570", "00876C80"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 34 addresses cited - 11 data, 16 entry, 7 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-input-name-registry-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Behavioural contract — the input name registry insert

**Subsystem:** input name registration · **Entry:** `00879570` (channels) and `00876C80` (keys)
**Maturity:** L2 RECONSTRUCTION-GRADE · **Readiness:** `RUNTIME VALIDATED` **and** `DIFFERENTIAL TESTED`
**Reconstruction:** [`name_registry.c`](../../../../Reconstruction/Game/Input/name_registry.c) ·
**Test:** [`diff_name_registry.py`](../../../../Reconstruction/Tests/Differential/diff_name_registry.py)
**System document:** [the input name registry and channel aliases](the-input-name-registry-and-channel-aliases.md)

## 1. Purpose

Every name a binding can use — `Button_Square`, `Key_A`, `Button_LeftMB` — is a static object in
the executable that **registers itself into a string-keyed list before `main` runs**. This is the
one operation that does the registering. A name that fails to register is a name the game cannot
bind, so the whole of `keymap.ini`'s vocabulary rests on 132 bytes.

The list is built at startup and never appears in the shipped file: **what the image contains is
the registrations, not the list.**

## 2. Interface

```c
uint32_t Register(Node *self);      /* MS x64: self in rcx, code in eax */
```

Two instances exist, one per registry:

| entry | registry | list head | names |
|---|---|---|---|
| `00879570` | `PInputChannelSemantic` | `02EB9D80` | 143 |
| `00876C80` | `PInputKeySemantic` | `02EB83B8` | 97 |

> **They are NOT byte-identical, and the difference is the whole point.** All 132 bytes agree
> except **two RIP-relative displacements**, at `+29` and `+106`, and each names its own head:
>
> ```text
> 00879570  +29   mov rbx, [rip + 0x26407EC]   -> 02EB9D80
>           +106  mov [rip + 0x264079F], r11   -> 02EB9D80
> 00876C80  +29   mov rbx, [rip + 0x2641714]   -> 02EB83B8
>           +106  mov [rip + 0x26416C7], r11   -> 02EB83B8
> ```
>
> Targets computed with capstone, never by hand. **One read, one write, and they are the only
> bytes that differ** — which is also why `globals_index.py` finds exactly one writer per head.

## 3. Types

```c
typedef struct Node {            /* 32 bytes; arrays are contiguous at stride 0x20 */
    void       *type;            /* +0x00  vtable; RTTI lives at vtable - 8        */
    const char *name;            /* +0x08  the registry key                        */
    struct Node *next;           /* +0x10  zero in the image, linked at startup    */
    int32_t     value;           /* +0x18  the semantic's numeric code             */
} Node;                          /*        +0x1C is not read by this operation     */
```

RTTI names both types: `.?AVPInputChannelSemantic@PInputs@Phyre@@` and
`.?AVPInputKeySemantic@PInputs@Phyre@@`.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `self` is a valid `Node`. `self->name` may be `NULL` — that is a handled input,
not a violation. `*head` may be zero (empty list).

**Postconditions on `OK`.** `self->next` is the previous head and `*head == self`. **The list grew
by exactly one node and no other node's `next` changed.**

**Postconditions on either failure.** *Nothing is written at all* — not `self->next`, not `*head`.
A rejected node is left exactly as it was found.

**Invariants.**

- **No name appears twice in a list**, by string value — this is what the operation exists to
  guarantee.
- The operation **allocates nothing and frees nothing**; every node is a static object.
- **`self->value` is never read**, so registration cannot depend on the numeric code.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | `self->name` (`+0x08`); each listed node's `name` and `next`; `*head` | body disassembled |
| written | `self->next` (`+0x10`) and `*head` — **only on `OK`** | the two stores at `+106` and the node store |
| allocated | nothing | no allocator call in 132 bytes |
| deallocated | nothing | — |

`globals_index.py --addr`: **`02EB9D80` — 1 writer, 148 readers. `02EB83B8` — 1 writer, 102
readers.** The single writer in each case *is* the insert. **Blind spot recorded:** that index is
RIP-relative only, so "1 writer" is a statement about one instrument; a write through a register
base would not appear.

Both heads were the database's most-read unexplained globals — `02EB9D80` ranked **#1** and
`02EB83B8` **#3** in [`UNEXPLAINED-GLOBALS.md`](../../_index/UNEXPLAINED-GLOBALS.md).

## 6. Relationships

**Callers.** CRT static initialisers, one per name, all of one shape: `lea rcx, [node]` ·
`call Register` · `lea rcx, [dtor]` · `jmp atexit`. There is no other caller.

**The subsystem is five paired functions, and all five are now read** — 2026-09-08, `EW-4`:

| channel | key | size | what it is |
|---|---|---:|---|
| `008794F0` | `00876C00` | 122 | **scalar deleting destructor** — installs the vtable, **unlinks the node from the list**, then `operator delete(this, 0x20)` when the low bit of the second argument is set |
| **`00879570`** | **`00876C80`** | **132** | **the insert** — this contract |
| `00879600` | `00876D10` | 103 | **find by name, out-parameter form** — writes the node or `NULL` and returns **`0x13` when not found**, `0` when found |
| `00879670` | `00876D80` | 222 | **enumerate into a flat array** — counts the list, and only when the count differs from the caller's does it allocate `count * 8`, free the old array and refill; then walks the list writing each node pointer in order |
| `00879760` | `00876E60` | 87 | **find by name, pointer-returning form** — `NULL` for a `NULL` name and `NULL` when absent; no status code |

**Every difference between a pair is a pair of adjacent bytes** — the low half of a
displacement — and each key-side function was checked to reference **its own** head `02EB83B8`
and its own vtable `01CD89D8`, so the pairing is **verified rather than inherited**.
*(Enumeration method: the readers of each head from `globals_index.py`, intersected with the
functions inside the two address runs.)*

> ### The return-code family has a fourth member
>
> `0x13` is **NOT_FOUND**. The full family is **`0x00` OK, `0x11` NULL_KEY, `0x12` DUPLICATE,
> `0x13` NOT_FOUND** — and **the insert can never return the fourth**, which is why reading only
> the insert never revealed it.

> ### The enumerator's count field carries an ownership bit
>
> Before freeing the previous array it tests **bit 31 of the stored count**
> (`shr eax,0x1F / not al / test al,1`) and frees only when that bit is **clear**, so a caller
> can hand in a **borrowed** array by setting the high bit and it will be refilled, not freed.

**Callees.** None. The `strcmp` is **inlined** as `movzx edx,[rax] / movzx ecx,[rax+r8]` with
`r8 = key - n->name`, so no string-function cross-reference finds it.

## 7. State transitions

```text
list L, node N
    N->name == NULL                     -> L unchanged, return 0x11
    some M in L with strcmp(M->name, N->name) == 0
                                        -> L unchanged, return 0x12
    otherwise                           -> N->next = head; head = N; return 0x00
```

The scan walks from the head and stops at the first match; on no match it has walked the whole
list, so **the cost is linear in the list and the last name registered is the first compared**.

## 8. Script · resource · event interactions

**None.** No opcode, archive or authored table participates. The names are consumed later by
`keymap.ini` parsing, which is a different subsystem and reads the *result*, never this operation.

## 9. Determinism

- **RNG** — none drawn.
- **Timing / update ordering** — runs entirely before `main`, in **CRT static-initialiser order**.
  That order decides the list's order, and it is now **recovered**: `Empty = 0` registers first,
  then **strictly descending by value** — in both registries. §13.
- **Threading** — single-threaded at static-init time; no lock is taken and none is needed.

**Given a fixed registration order the operation is fully deterministic**: no input outside the
node and the list affects the result.

## 10. Failure paths and edge conditions

| condition | code | what happens |
|---|---:|---|
| `self->name == NULL` | `0x11` | tested first; the list is never walked |
| a node in the list has an equal name | `0x12` | the scan stops at that node |
| the list is empty | `0x00` | the scan body never runs; `self` becomes the head |
| a name equal by **value** at a different address | `0x12` | the comparison is `strcmp`, not pointer identity |

| a **non-zero** `name` that does not point at readable memory | — | **the function faults.** There is no validity check beyond `!= NULL` |

**A duplicate is rejected, not replaced.** The first registration of a name wins, and the loser is
left unlinked — so registration order decides which node a later lookup finds.

### The last row, and how a failed test produced it — added 2026-09-12 (`OPUS-NAMEREG-UNGUARDED`)

`00879574 mov r10, [rcx+8]` loads the name and `0087957B test r10, r10` is the **only** check it
gets. From there the scan dereferences both sides directly — `008795A0 mov rax, [r9+8]` for the
chain node's name, then `008795B0 movzx edx, byte [rax]` and `008795B3 movzx ecx, byte [rax+r8]`,
the pointer-difference `strcmp`. **Nothing validates either pointer.** A node whose `name` is
non-zero and garbage is not refused; it is read, and the read is whatever that address happens to
be.

This was found by trying to kill a mutation. Two mutants in the reconstruction survived its whole
campaign, both on the path taken when an address **fails to resolve**:

    name_registry.c:23  load_q       `if (!p) return 0;`   ->  `return 1;`
    name_registry.c:58  names_equal  `return a == b;`      ->  `return a != b;`

A case was added to drive exactly that: a node whose `name` is non-zero and in no mapped region.
**The original faulted** — `emulation error at 008795B3: Invalid memory read` — and the case was
withdrawn, because a test that drives the original outside its domain measures nothing.

> **Those two mutants are not a test gap, and calling them one would be wrong.** They mutate code
> that has **no counterpart in the original**: `NameImage_At`'s bounds check exists because the
> harness emulates a partial address space, and the shipped function simply reads. No case can kill
> them, and none should be contrived to. **A mutation score should name this category rather than
> bury it in "survived"** — a reconstruction carries scaffolding the original does not have, and
> mutating scaffolding produces an unkillable mutant every time.
>
> The consequence for a reimplementation is the opposite of what the guard suggests: **keep the
> guard if you want a robust registry, but know that dropping it is what parity means here.** A
> reimplementation that refuses a bad pointer where the original faults is safer and is not the
> same program.

## 11. Observable behaviour

- The **return code**, one of three.
- The **resulting chain**, walkable from the head: length, order, and each node's `name` and
  `value`.
- **In play:** `Button_Square`, `Button_X`, `Button_0` and `Button_LeftMB` all bind to the same
  thing, because they are four names registered at **channel 11**. 143 names resolve to 113
  channels through 16 alias groups; 46 names sit in those groups, so **30 names are synonyms of
  another name** (143 − 30 = 113).

## 12. Reproduction formula

```c
uint32_t Register(Node *self)
{
    const char *key = self->name;               /* +0x08                      */
    if (key == NULL)
        return 0x11;                            /* NULL_KEY                   */
    for (Node *n = *head; n != NULL; n = n->next)   /* +0x10                  */
        if (strcmp(n->name, key) == 0)
            return 0x12;                        /* DUPLICATE                  */
    self->next = *head;
    *head = self;                               /* push front                 */
    return 0x00;                                /* OK                         */
}
```

Alias arithmetic, reproducible by hand: the 16 groups have sizes
`4,4,4,3,3,3,3,3,3,2,3,3,2,2,2,2` = **46 names**; one name per group is the survivor, so
`46 − 16 = 30` synonyms and `143 − 30 = 113` distinct channels. The 97 key names are a **strict
subset** of the 143 (names only in the key registry = 0; names only in the channel registry = 46).

## 13. Runtime validation

| claim | how it was observed live | date | result |
|---|---|---|---|
| both lists exist and are walkable from their heads | `walk_name_registry.py`, cycle-checked and length-bounded | 2026-09-08 | **143 and 97 nodes**, every one with a readable name |
| the recovered name sets are complete | live names against the 240 recovered statically | 2026-09-08 | **0 live-only, 0 static-only**, both registries |
| the real registration order | the chain reversed — the list is push-front, so it preserves the order it was built in | 2026-09-08 | `Empty = 0` first, then **strictly descending by value** |
| the 16 alias groups | the only places consecutive registrations share a value | 2026-09-08 | **exactly values 11..26**, matching §11's grouping derived statically |
| the reconstruction rebuilds the game's own list | `integration_name_registry.py` — the game's nodes, at their own addresses, in its own order, compared against its own chain | 2026-09-08 | **0 of 143 and 0 of 97 nodes differ**; `OK` ×143 and `OK` ×97 |

> **The last row uses the running game as the oracle**, not the shipped bytes under emulation.
> It is also the first test of the **key** registry's behaviour: §16 recorded `00876C80` as
> *inherited, not tested*, and its live list is now rebuilt node for node.

**What it still does not show:** that the reconstruction would be **called** the way the game
calls it. The CRT initialiser sequence is not executed — only its **order** is recovered and its
**result** compared. `INTEGRATION` remains `NOT COVERED`, for that reason alone.
> **SUPERSEDED 2026-09-19 (OPUS)** - that reason no longer holds. EXP-116 executes the
> CRT initialiser sequence in its real shuffled `.CRT` order over the real insert twins,
> which is the caller this paragraph says is missing. See *INTEGRATION closes* below.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**33 generated points: 24 KILLED · 2 SURVIVED · 5 EQUIVALENT · 0 NO_BUILD · 2 TIMEOUT · 0 INVALID. Verdict `FAIL_INCOMPLETE`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/name_registry` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

Both survivors are **kind B, fixture scaffolding** — see §10. They mutate `NameImage_At`'s bounds check, which exists because the harness emulates a partial address space; the shipped function has no such check and dereferences directly. A case written to kill them made the ORIGINAL fault at `008795B3`, and was withdrawn. The two `TIMEOUT` cases are mutations of the walk's termination condition that make the chain circular; the instrument records a timeout rather than guessing, and the campaign is `FAIL_INCOMPLETE` because of them rather than because of a survivor.

## 14. Unresolved

1. ~~**The real registration order.**~~ **RESOLVED 2026-09-08** — `Empty = 0` first, then strictly
   descending by value, in both registries. `EW-5`, and §13.
2. ~~**Whether a channel value is what `keymap.ini` stores.**~~ *(Superseded: **ANSWERED 2026-09-22 (FABLE)** on the system page - the node `+0x18` value IS the keymap control code for buttons too, 13 of 13 worked examples, 46 of 46 button values inside the band 11-27; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* The keymap document proves
   `keymapCode = PInputKeySemantic − 1` for keys, 28 of 28; **no equivalent check was run for the
   `Button_*` channels.** `DM-3`.
3. ~~**Whether the alias groups stay indistinguishable downstream.**~~ *(Superseded: **ANSWERED 2026-09-22 (FABLE)** on the system page - downstream separates mouse buttons, codes 1-3 on their own backend, from pad buttons, 11-27; but no name reaches codes 1-3, so `Button_LeftMB` binds the pad; propagated 2026-10-01, OPUS, from the system page; register rows answered.)* They are one channel here;
   whether a consumer separates mouse from pad is unread. `DM-1`.
4. ~~**Whether 143 and 97 are complete.**~~ **RESOLVED 2026-09-08** — the live chains are exactly
   **143 and 97** with **0 live-only names**, so nothing is registered at runtime in the state
   observed (the front-end). `EW-5`.
5. ~~**The other four entry points per registry.**~~ **RESOLVED 2026-09-08** — destructor, two
   lookup forms and an enumerator; §6. **Still not reconstructed**, which is a different thing
   and is what `FULL-SUBSYSTEM` measures. `EW-4`.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| Signature and return convention | body `00879570` disassembled whole (twin `00876C80`); node in `rcx`, code in `eax` | 1 | PROVEN |
| The three return codes `0x00` / `0x11` / `0x12` | the three exit paths — `00879580` (`0x11`, null name), `008795D4` (`0x00`, inserted), `008795E6` (`0x12`, duplicate) | 1 | PROVEN |
| Node layout: name `+0x08`, next `+0x10`, value `+0x18`, stride `0x20` | field reads in the body; 97 key nodes span `01F456C8`…`01F462C8` at one stride | 1 | PROVEN |
| The comparison is a string comparison, not pointer identity | the inlined `movzx`/`movzx` at `008795B0`/`008795B3` with `r8 = key − name` computed at `008795A4`/`008795A7`, and a differential case using a **copied** name at another address | 1 | PROVEN |
| Insert is push-front, and only on success | `self->next = head; head = self` at `008795D0`/`008795DA` after the scan; neither store is reached on either failure path | 1 | PROVEN |
| Exactly one function writes each head | `globals_index.py --addr`: `02EB9D80` 1 writer / 148 readers, `02EB83B8` 1 writer / 102 readers. **RIP-relative instrument only** | 2 | VERY HIGH |
| The two inserts differ only in the two displacements naming their own head | byte compare of all 132 bytes (4 differ, in two adjacent pairs) + capstone-resolved targets at `+29` (`0087958D`/`00876C9D`, the head load) and `+106` (`008795DA`/`00876CEA`, the head store) | 1 | PROVEN |
| a non-zero `name` pointer is dereferenced with no validity check | `00879574` / `0087957B` are the only test, and `008795A0`, `008795B0`, `008795B3` read both sides directly. Executed — a case supplying a non-zero unmapped pointer made the ORIGINAL fault under emulation at `008795B3`, which is the behaviour rather than an instrument failure | 1 (isolated original-code) | PROVEN |
| Each registry is five paired functions of identical size | sizes 122/132/103/222/87 in both runs; every difference is a pair of adjacent bytes | 1 (static) | PROVEN  **§15a: true, and the shape occurs EIGHT times image-wide, not twice** — this contract describes two of them |
| The other four are destructor, two finds and an enumerator | bodies read 2026-09-08: unlink + `operator delete(this,0x20)`; a `Find` returning **`0x13` NOT_FOUND**; a pointer-returning `Find`; a count-cached flattening whose count field's **bit 31 is an ownership flag**. Each key-side twin verified to reference `02EB83B8` and vtable `01CD89D8` | 1 | PROVEN |
| 143 channel names, 113 channels, 16 alias groups, 97 key names | `named_registry.py`, 240 of 240 recovered, 0 unrecovered; `B ⊆ A` measured | 1 (corpus) | PROVEN |
| The real registration order | walked live in both registries: `Empty = 0` first, then **strictly descending by value**; the channel registry's only ties are values 11..26, exactly the 16 alias groups | **10** *(corrected 2026-09-13 from 3: this is runtime evidence, not a qualified symbol)* | PROVEN |
| any runtime observation | §13 — five observations, including the reconstruction rebuilding the game's own 143- and 97-node lists with 0 differing nodes | **10** (live) *(corrected 2026-09-13 from 3, same reason)* | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### Every counted claim reproduced exactly

| claim | measured |
|---|---|
| `02EB9D80`: **1 writer / 148 readers** | 1 writer (`008795DA`, in the channel insert `00879570`), **148** distinct reading functions |
| `02EB83B8`: **1 writer / 102 readers** | 1 writer (`00876CEA`, in the key insert `00876C80`), **102** distinct reading functions |
| the two inserts differ only in the displacements naming their own head | both **132 bytes**; **exactly 4 bytes differ**, in two adjacent pairs at `0x20`–`0x21` and `0x6D`–`0x6E` — the low halves of the two rip displacements |
| five paired functions of sizes 122 / 132 / 103 / 222 / 87 | both groups present, sizes exact |

> **Worth recording beside the transform workbench.** The *same* instrument, built the same way,
> **could not reproduce** that contract's writer/reader figures, and reproduces these two **exactly,
> first time**. That contrast is what makes the earlier non-reproduction a finding about those
> numbers rather than a doubt about the method.

### Scope: this shape is not a pair, it is a family of eight

Searching the image for the size quintet `122 / 132 / 103 / 222 / 87` finds **eight** groups. Every
one of the eight inserts is **132 bytes**, writes **exactly one** global head, and differs from the
key insert `00876C80` by **4 bytes** — 6 for the two furthest away, whose displacements need more
digits:

| insert | head written | bytes differing from `00876C80` |
|---|---|---:|
| `006D9680` | `02EA06D8` | 6 |
| `006D9A70` | `02EA0748` | 6 |
| `008760A0` | `02EB8260` | 4 |
| `00876490` | `02EB82D8` | 4 |
| `008768A0` | `02EB8348` | 4 |
| **`00876C80`** | **`02EB83B8`** | **0 — the key registry, §2** |
| `00877060` | `02EB8428` | 4 |
| **`00879570`** | **`02EB9D80`** | 4 — **the channel registry, §2** |

**Five of those heads form a regular array** — `02EB8260`, `02EB82D8`, `02EB8348`, `02EB83B8`,
`02EB8428`, **exactly `0x78` apart** — and §2's *key* registry is the **fourth** of the five. The
`006D9xxx` pair is a second cluster `0x70` apart, and the channel registry stands alone at
`02EB9D80`.

> **The claim is true and its scope is narrower than the pattern.** "Each registry is five paired
> functions" describes two registries; the engine builds **eight** from the same 132 bytes, differing
> only in which head they name. **Nothing here says what the other six hold** — the size match
> establishes *shape*, not *contents* — so that is registered as `IR-1` rather than guessed.

**Not claimed:** the other six registries' contents, and nothing in this pass is a runtime
observation — §13's five live observations are untouched.

### `IR-1` answered — what the other six registries hold (2026-09-14, FABLE)

**Method.** Every registration site was found with a raw `E8` scan of `.text` for calls to each registry's 132-byte push-front
insert. Each site is a 32-byte CRT initialiser of the form `lea rcx, [node]` / `call insert`, so every node is a static in
`.data`. For each node the name was read from its `+0x08` string pointer, and the class from the RTTI locator of its
`+0x00` vtable.

| head | class (RTTI) | nodes | the names |
|---|---|---:|---|
| `02EA06D8` | `Phyre::PLOD::PLODMetricType` | 3 | `DistanceToNode`, `DistanceToBoundBox`, `ScreenSize` |
| `02EA0748` | `Phyre::PLOD::PLODBlendType` | 2 | `Distance`, `Time` |
| `02EB8260` | `Phyre::PInputs::PInputTypeSemantic` | 25 | `Key`, `JoypadButton`, `JoypadAxis`, `MouseButton`, `MouseDeltaX/Y`, `TouchDragX/Y`, `TouchTwoFingerDragX/Y`, `TouchPinch`, `TouchRotate`, `MotionQuatX/Y/Z/W`, `MotionAngularVelocityX/Y/Z`, `MotionLinearAccelerationX/Y/Z`, `VisionTrackerX/Y/Z` |
| `02EB82D8` | `Phyre::PInputs::PInputAxisSemantic` | 10 | `XAxis_0`–`2`, `YAxis_0`–`2`, `ZAxis_0`–`2`, `Gyro` |
| `02EB8348` | `Phyre::PInputs::PInputJoypadButtonSemantic` | 44 | `Empty`, `Button_0`–`Button_15`, the Xbox names (`A`, `B`, `X`, `Y`, `LB`, `RB`, `LT`, `RT`, `LS`, `RS`, `Back`, `Start`), the PlayStation names (`Cross`, `Circle`, `Square`, `Triangle`, `L1`–`L3`, `R1`–`R3`, `Select`) and the d-pad (`Up`, `Down`, `Left`, `Right`) |
| `02EB8428` | `Phyre::PInputs::PInputMouseButtonSemantic` | 4 | `Empty`, `LeftMB`, `MiddleMB`, `RightMB` |

The two this contract already documents are `PInputKeySemantic` (`02EB83B8`, 97 nodes) and `PInputChannelSemantic`
(`02EB9D80`, 143 nodes).
- **The channel registry is the union.** Its names are the joypad buttons, the mouse buttons and the keys, sharing one
  `Empty`.
- **The five heads `0x78` apart** are the input type, axis, joypad button, key and mouse button semantics, in that order.
- **The two LOD registries** are separate, and belong to the Phyre LOD module.
- **Not claimed:** which values the engine or authored data selects from any of the six.

## 16. Parity plan

`diff_name_registry.py` runs 154 cases — the 143 real nodes out of `.data` plus 11 injected —
comparing every return code and then the resulting 144-node chain node for node. **Both sides are
given the same image regions at the same virtual addresses**, because the nodes point at each
other and at their names by absolute address.

**Real data alone would be a weak test**: every shipped name is distinct, so a suite built only
from real nodes never takes the duplicate path. The injections exist to reach it — and the
**copied-name** case is the only one that can show the comparison is by string rather than by
pointer.

What is still missing, in this contract's own terms:

- **`INTEGRATION`** — ~~**half the criterion now holds.** The inputs and the oracle are the game's
  own: its nodes, at their own addresses, in its own order, against its own list. **The caller is
  not** — the initialiser sequence is never executed, so a reconstruction that inserted correctly
  but was never invoked would look identical here.~~ **BOTH HALVES HOLD as of 2026-09-19 (OPUS):**
  EXP-116 executes the caller — 97 + 143 thunks in the real shuffled `.CRT` order over the real
  insert twins, from the real load-time state. See *INTEGRATION closes* below for what remains
  scripted (`atexit` only, which touches neither head).
- **`FULL-SUBSYSTEM`** — **5 of 5 identified, 1 of 5 reconstructed.** §6 now says what each of
  the other four *does*, so the gap is a reimplementation gap rather than an understanding one.
- **The second instance.** `00876C80` is still not *emulated* — but its **behaviour** is no longer
  inherited: the reconstruction rebuilds the key registry's live 97-node list node for node, so the
  two instances now agree on a real result as well as on their bytes.

<!-- OPUS-ADOPT-EXP116 -->
### INTEGRATION closes, 2026-09-19 (OPUS), answering `REQ-OPUS-NAME-REGISTRY-INIT-FINDINGS`

**`INTEGRATION` was `NOT COVERED` "for that reason alone", and the reason is now executed.** This
contract named the gap twice - *"the CRT initialiser sequence is not executed - only its order is
recovered and its result compared"*, and *"a reconstruction that inserted correctly but was never
invoked would look identical here."* **EXP-116 runs the caller**: all **97 key and 143 channel
thunks in the real shuffled `.CRT` order**, over the shipped node objects and name strings,
calling the **real insert twins** `00879570` and `00876C80`, from the real load-time state with
both heads zero in BSS. 10/10 cases, 17/17 mutants, stable across three processes.

**The two halves now hold, and neither does alone.** The 2026-09-08 row supplies the game's own
inputs and its own list as oracle; EXP-116 supplies the game's own **caller**. The criterion
asked for both.

**What is still scripted, so the closure is not read as more than it is.** `00808B90` (`atexit`)
is a disclosed boundary and takes no part in building the lists - each thunk's registration is
recorded as an `ate:` token and the registrar touches neither head - so **list construction is
fully executed and teardown registration is not**. This is isolated original machine code
(method B, `live_game: false`), a different evidence class from the live comparison it completes.

| invariant | evidence | n (class) | status |
|---|---|---|---|
| the `.CRT` table order is load-bearing, not the thunk arrays' address order | the arrays are contiguous (`97 + 143 × 0x20`) but the table links them shuffled - `0x16B5E0 → 0x16B760 → 0x16BFE0 → 0x16C020 → …`. Running in address order produces a different list; the executed shuffled order is what puts `Empty` at the tail and the alias groups adjacent, matching the live lists. EXP-116 | 1 (isolated original-code) | PROVEN |
| a duplicate name returns `0x12` and links nothing, compared by BYTE CONTENT not pointer identity | `dup-shipped-name` (same shipped name pointer) and `dup-copied-name` (a copy at a different address) both return `0x12`; the `inc`→`dec` cursor mutant is distinguishable only on the copied-name case. EXP-116 | 2 (isolated original-code) | PROVEN |
| first registration wins, and push-front ordering is what keeps `Empty` reachable at the tail | `dup-shipped-name` leaves the list unchanged - the already-registered name stays and the late duplicate is refused. EXP-116 | 1 (isolated original-code) | PROVEN |
| **HAZARD - the two lists have NO type separation** | `cross-list` inserts a real **key** node through the **channel** insert: it links onto the channel head and returns `0`. The twins differ only in which head global they touch, so nothing in the code prevents a reimplementation from cross-linking them. EXP-116 | 1 (isolated original-code) | PROVEN |
| the insert refuses a null name before touching the list | `name = [rcx+8]`; null → return `0x11`, no walk and no link. EXP-116 | 1 (isolated original-code) | PROVEN |

**`FULL-SUBSYSTEM` is untouched by this** and remains 5 of 5 identified, 1 of 5 reconstructed.
Closing INTEGRATION does not narrow that gap, which is a reimplementation gap.

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-contract-input-name-registry-ee-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `006D9680` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EA06D8`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EA06D8` and returns 0 | `006D968E`, `006D96C8`, `006D96D5`, `006D96E0`, `006D96EA` |
| `006D9A70` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EA0748`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EA0748` and returns 0 | `006D9A7E`, `006D9AB8`, `006D9AC5`, `006D9AD0`, `006D9ADA` |
| `008760A0` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB8260`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB8260` and returns 0 | `008760AE`, `008760E8`, `008760F5`, `00876100`, `0087610A` |
| `00876490` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB82D8`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB82D8` and returns 0 | `0087649E`, `008764D8`, `008764E5`, `008764F0`, `008764FA` |
| `008768A0` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB8348`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB8348` and returns 0 | `008768AE`, `008768E8`, `008768F5`, `00876900`, `0087690A` |
| `00876D80` | 222 B | counts the nodes of the list whose head is qword `02EB83B8` (links at qword `+0x10`); when the count differs from dword `[rdx]` it allocates the array with `0017D260(count*8, 8)` and zeroes it (a zero count uses a null array, and a failed allocation returns 0xd), calls `00584730` on the old qword `[rdx+8]` when that differs from the new array, is non-null and dword `[rdx]` is not negative, and stores the new array and count to `[rdx+8]` and `[rdx]`; it then writes each node pointer in list order into the array at `[rdx+8]` and returns 0 | `00876DB5`, `00876DCC`, `00876DD7`, `00876E15`, `00876E30` |
| `00877060` | 132 B | reads the name pointer qword `[rcx+8]` and returns 0x11 when it is null; otherwise it walks the list whose head is qword `02EB8428`, following each node's qword `+0x10`, comparing the zero-terminated string at each node's qword `+8` byte by byte with the name, and returns 0x12 at the first equal string; when no node matches it stores the old head to qword `[rcx+0x10]`, stores `rcx` to `02EB8428` and returns 0 | `0087706E`, `008770A8`, `008770B5`, `008770C0`, `008770CA` |
| `00879670` | 222 B | counts the nodes of the list whose head is qword `02EB9D80` (links at qword `+0x10`); when the count differs from dword `[rdx]` it allocates the array with `0017D260(count*8, 8)` and zeroes it (a zero count uses a null array, and a failed allocation returns 0xd), calls `00584730` on the old qword `[rdx+8]` when that differs from the new array, is non-null and dword `[rdx]` is not negative, and stores the new array and count to `[rdx+8]` and `[rdx]`; it then writes each node pointer in list order into the array at `[rdx+8]` and returns 0 | `008796A5`, `008796BC`, `008796C7`, `00879705`, `00879720` |
