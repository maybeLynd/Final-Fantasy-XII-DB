---
contract: The widget object — allocate, construct, message, destroy
category: 16-UI
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: HIGH
implements: the-widget-constructor-and-object-sizes.md, the-widget-message-protocol.md
entries: [00244F50, 00245000, 002465F0, 00244F00, 00245020, 002473B0, 00248030, 00247930, 00244960, 002448D0]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 191 addresses cited - 16 data, 72 entry, 103 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-22
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-widget-object-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the widget object

> **SECTION-04 local production, 2026-09-22; independent acceptance pending.**
> The full initializer's return contract and a concrete title-widget receiver/census case were
> re-derived. Existing audit dates/counts below remain historical; they do not certify these edits.
> [Bounded mechanism](the-title-asset-singleton-and-its-distinct-consumer.md) and
> [reproduction](../../_experiments/evidence/continuation-section04-widget-receiver/REVIEW.md).

> **The third behavioural contract in this database, and the first for a subsystem three separate
> blocks went into.** It formalises
> [the widget constructor](the-widget-constructor-and-object-sizes.md) and
> [the widget message protocol](the-widget-message-protocol.md) into something an engineer can
> reimplement and a differential test can be written from.
>
> **Readiness is `CONTRACT READY`, not `RECONSTRUCTION READY`** — §13 carries no LIVE observation. Nothing here has been
> observed in a live process, and the charter's readiness gate requires it.

## 1. Purpose

Every window, list, panel, gauge and options row in FFXII is one of these objects. A parent builds
its children **inside its own allocation**; each object carries a **handler** at `+0x00` that answers
a stream of small numbered messages; and the whole tree is torn down by a broadcast. **267 distinct
handlers** are built from **297 constructor transfer sites** (280 calls + 17 tail-jump forwards).
*(267 corrected from 251 on 2026-09-13; §15b has every term.)*

## 2. Interface

| operation | entry | conv | signature | returns |
|---|---|---|---|---|
| allocate + construct | `00244F50` (175 B) | MS x64 | `(uint32 size ecx, proc rdx, const Msg* initArgs r8)` | the object, or a pool slot |
| construct in place | `00245000` (31 B) | MS x64 | `(void* obj rcx, uint32 size edx, proc r8, void* locals r9)` | `rax = obj` |
| construct, full | `002465F0` (395 B) | MS x64 | `(void* obj rcx, uint32 size edx, proc r8, void* locals r9, int pooled [rsp+0x20])` | mutates `obj`; **no object-pointer return guarantee** (the final predicates leave incidental 0/1 in tested paths). Wrappers restore the object return; SECTION-04 |
| destroy | `00244F00` (68 B) | MS x64 | `(Widget* rcx)` | — |
| tear down | `00245020` (132 B) | MS x64 | `(Widget* rcx)` | — |
| broadcast to a subtree | `002473B0` (55 B) | MS x64 | `(Widget* rcx)` — sends `{18,0,0}` | — |
| generation reconcile | `00248030` (339 B) | MS x64 | `(Widget* rcx)` | — |
| set `+0x44` | `00247930` (26 B) | MS x64 | `(Widget* rcx, uint16 dx)` — also sets `[parent +0x40] |= 0x2000` when `[rcx+0x10]` non-null (`00247935`–`00247943`); store at `00247945` | — |
| attach to the manager | `00244960` (12 B) | MS x64 | `(Manager* rcx, Widget* rdx)` | — |
| detach / pop focus | `002448D0` | MS x64 | `(Widget* rcx)` | — |

**A handler is `void proc(Widget *self, const WidgetMessage *msg)`**, stored at `self[0]`, and is
**never null** — `002465F0` substitutes `005C5230`, the default handler, when the argument is null
(`00246635 cmove`).

## 3. Types

```c
struct WidgetMessage {          /* 24 bytes */
    int32_t  id;                /* +0x00 */
    uint64_t a;                 /* +0x08 */
    uint64_t b;                 /* +0x10 */
};
```

**In the type store as `Widget`** (2026-09-08), `SIGNATURE RESOLVED` — **the size is an argument**,
so `size` is `UNRESOLVED` and only the header below is declared. 15 fields.

**Widget header**, written by `002465F0` on every object regardless of size:

| offset | value at construction | anchor |
|---|---|---|
| `+0x00` | the handler, or `005C5230` | `00246641` |
| `+0x40` | flags: `or 0x80A`, bit `0x20000` from the global `0208ED5C`, bit `0x4000` cleared **and then re-set from the 5th argument** — `(pooled & 1) << 14`, i.e. **bit 14 means "this object came out of the fixed pool"** | `00246653`, `002466D1`, `002466F2` |
| `+0x44` | low word `0x64` = **100**; bits `0x70000` cleared | `002466FA`, `00246670` |
| `+0x48` | `00915198` — the **default** transition descriptor. This table's frame is *value at construction*, and that value is right; but it is a default, not a constant, and the row is **not** evidence that a widget still holds it later. The setter `00247570` is `test rcx,rcx / test rdx,rdx / lea rax,[00915198] / cmovne rax,rdx / mov [rcx+0x48],rax` — `00915198` is the **default arm of a `cmov`**, taken only when the caller passes a null descriptor. Measured 2026-09-20 (OPUS) over the graph's **127 callers**: decoding each body gives **137 call sites**, of which **97 pass a different descriptor** covering **64 distinct `.rdata` addresses**, **2** pass null and take the default, and **38** are unresolved by the method and scored neither way. `BattleMenuChildWidget1620`'s handler passes `00915A80` at `0027AEE3`. What the record *contains* is UQ-187's answer and is unaffected | `00246687`, setter `00247570` |
| `+0x98` | `0` | `00246711` |
| `+0x9C` | `0x800080` | `00246717` |
| `+0xA0` | `0x80` | `0024670A` |
| `+0xA1` | `0xFF80` | `002466E6` |
| `+0xAC`, `+0xAD` | `6` or `0xF9` (`−7`), chosen by two bits of `+0x44` — **which this constructor has already cleared**, so the value is always `0` and **both bytes always receive `6`**. `00246670` clears bits `0x70000`; `0024667E`-`00246684` reads those same bits back (`shl edx,0xd / sar edx,0x1d`). The `0xF9` arm is **unreachable from this function**. Corrected 2026-09-08; found because six mutants across the reconstruction's copy of this branch compiled to byte-identical code, which only happens when the compiler proves the code dead. See `WD-1` | `002466C1`, `002466CB` |
| `+0xB4` | `1`, but only inside `World_UpdateSimulationTick` and only at 60 Hz in mode 0 — **this is a half-rate phase counter**, see §3a | `0024675C` |
| `+0xB8` | `0x3F800000` — **1.0f** | `00246700` |

**The three draw-time fields** (`UQ-351` ANSWERED 2026-09-25, OPUS; [replay](../../_index/candidates/uq351-opus-replay-widget-alpha-guard/)):
- **`+0x38`** is the node's live draw record. It is non-null only while `00245E60` draws the node: set at `00245EB0` to a 0xA0-byte stack record that `002D8C00` fills, and cleared at `002463BE`.
- **`+0xA0`** is the node's opacity (0x80 = 1.0). The pass composes it into the record's alpha scale `+0x58` as `(parent * it) >> 7`; a root takes it as-is.
- **`+0xA1`** is the node's RGB scale. It composes into `+0x5A` the same way for a child; a root's record keeps 0x80.

Tree links, from the broadcast walker (`002473B0`): **`+0x10` parent**, **`+0x18` first child**,
**`+0x20` next sibling**. *(`+0x10` as parent is read from `00247930`, which sets a flag on
`[self+0x10]`; `+0x18`/`+0x20` are proven by the recursion.)*

**26 distinct object sizes** across 49 direct sites, from `0xC0` to `0xBC08`. **The size is an
argument**, so there is no single `sizeof(Widget)` — only a common header.

### 3a. `+0xB4` is the widget tree's half-rate phase counter

Decoded 2026-09-10 from the three functions that touch it. It is **not** an opaque flag.

**The two globals.** `01F82E38` is the process-wide *"running at 60"* gate — one write in the whole
image, at `001EDDE8`, on the 60 fps arm of the `FrameLimit` path (see
[`19-Save-Load-Settings`](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)).
`01DFE0C0` is a second mode toggle with **one writer**, the setter `001EDEF0(ecx)`, and three
readers, all in this family. Call the condition `01F82E38 != 0 && 01DFE0C0 == 0` **HALFRATE**.

| function | returns | meaning |
|---|---|---|
| `001EDDA0()` | `0` iff HALFRATE, else `1` | "we are *not* in half-rate mode" |
| `001EDEC0(x)` | `1` unless HALFRATE; under HALFRATE, `(~x) & 1` | "does a widget whose counter is `x` run this frame?" |
| `001EDEF0(ecx)` | — | the toggle's only writer |

**The two writers.**

| site | what it does | when |
|---|---|---|
| `0024675C`, in the constructor | `+0xB4 = 1` | only if `001EDDA0() == 0` **and** `00314960() != 0`. `00314960` is a 7-byte read of `022C2548`, which `World_UpdateSimulationTick` (`00314020`) sets to `1` at its first instruction and back to `0` at its last — so it means **"we are inside the world simulation tick"**. Three references image-wide, positive control passed |
| `00248050`/`00248059`, and the same pair again at `002480BC`/`002480C8` and `00248131`/`0024813A`, in the tree walker `00248030` | `+0xB4 = 0` when `001EDDA0() != 0`; **`++(+0xB4)`** when it returns `0` | once per node the walk visits |

**The consumer.** `001EDEC0` is called with `[self+0xB4]` in **33 places inside handlers that answer
message id 1**, always as `mov ecx,[self+0xB4] / call 001EDEC0 / test eax,eax / je <skip>`. In the
two sampled by jump table — `00241D40` at `0024218B` and `0057FE80` at `00580356` — the site sits on
the **id 2** arm, not the id 1 arm.

**So the mechanism is:** outside half-rate mode the counter is pinned to `0` and `001EDEC0` always
returns `1`, so every widget does its id-2 work every frame. Under half-rate mode the reconcile walk
increments each widget's counter every pass and the id-2 gate passes only on **even** counts — the
tree does its per-frame work **every other 60 Hz frame**. A widget constructed *inside* the
simulation tick starts at `1` instead of `0`, which puts it on the **opposite phase** from one
constructed outside it.

**Bounded limits.** The 33 sites are direct handler-body hits from a displacement scan over the 217
id-1-answering handlers (positive control `+0x44`: 47 hits); the base register is not proven to be
`self` at every one, and the handlers' callees were not searched. Two sites were resolved to an arm
by decoding their jump tables; the other 31 were not. Nothing here establishes *which thread* runs
the walk.

### Where the object lives — added 2026-09-12 (`OPUS-WIDGET-INSTANCE`)

**The constructor does not allocate; `00244F50` does, and it has two paths.** A requested size of
0 becomes `0xC0`; a size **above `0x120` skips the pool entirely** and takes a heap block from
`002497B0(size)`. At or below it, the allocator scans a **fixed pool of 112 slots** at
`*(char **)0x0208EA58`, stride `0x120`, linearly from slot 0, and takes the first where **both**
`+0x40 & 0x4000` is clear and the byte at `+0xA2` is zero. It then writes the slot's **1-based
index** into `+0xA2` and passes `pooled = 1` as the constructor's fifth argument; the heap path
passes 0.

> **That fifth argument is the same bit 14 this contract's §7 already describes**, and the loop
> closes: the constructor ORs `pooled` into bit 14 of the flags word at `+0x40`, and the allocator
> tests bit 14 of `+0x40` to decide a slot is taken. **The occupancy flag and the "came out of the
> fixed pool" flag are one bit, written by the constructor and read by the next allocation.**
>
> **First free wins — there is no free list and no high-water mark**, so slot reuse order is
> allocation order, and a reimplementation that pools every widget regardless of size is wrong for
> every size above `0x120`, which is most of the 26 this object is built at.

> **✖ Correction, 2026-09-17 (FABLE, independent read of `00244F50` and `002465F0`).** The slot-index write
> is dead. `00244FF4` does store `slot + 1` into `+0xA2` of the slot the factory takes, but the constructor's
> first act is `memset(object, 0, size)` through the import thunk `00861EC0` (`VCRUNTIME140!memset`, IAT
> `008C2A60`) at `00246626`, over the requested size, which always covers `+0xA2`; then `002466E6` writes the
> word `0xFF80` at `+0xA1`, leaving `+0xA2 = 0xFF`. **The value a taken slot carries at `+0xA2` is the
> constructor's `0xFF`, not the slot index**, and it is the same for every slot; the free test at `00244F99`
> (`+0xA2 == 0`) works because the release path this contract records zeroes the byte, not because construction numbered it. `+0xA2` sits
> in the run the constructor initialises as `+0x9C = 0x800080`, `+0xA0 = 0x80`, `+0xA1 = 0x80`, `+0xA2 = 0xFF`,
> so the occupancy byte doubles as a colour-like component whose fully-set value is the occupied mark.
> §7's row for `+0xA2` ("1-based index") and the *allocated* row ("taking it sets `[+0xA2] = 1`") describe
> the factory's dead write, not the object's state. Static, bodies read.

### 3b. Do not merge a handler receiver with a message or a published dependency

`WidgetSingleton02AEE4C0` is the 0xD8 object constructed through `00394460` with handler
`00394070`. `003939B0` is a **different**, 0x1D0 consumer, selected by `00394530` and
published at `02AEE4C8`. At consumer entry RBX receives RDX (message) and RSI receives
RCX (consumer). The later load of `02AEE4C0` supplies the asset widget in RDX; it does not
retroactively change either incoming object's identity.

`003939F7 [rbx+8]` reads message payload. `003939FB xor ebx,ebx` clears the whole RBX,
and `00393A23 lea edx,[rbx+0x15]` therefore computes 21 **without a memory access**.
Neither is evidence of byte+8 or DWORD+0x15 in the asset widget. Actual asset fields include
ready flags+0xC0 and retained pointers+0xC8/+0xD0, with different cleanup behavior.

The raw initializer `002465F0` does not restore RAX to its object. Its final scheduler
predicates leave tested returns 0/1; `00245000` and `00244F50` separately restore an object
pointer in RAX. Do not give all three entries the same return guarantee.

The [concrete mechanism and limits](the-title-asset-singleton-and-its-distinct-consumer.md)
separate real original instructions, scripted service boundaries, and unanswered live/lifetime
questions. The missing producer scanner is not patched or certified by the replacement diagnostic.

## 4. Preconditions · postconditions · invariants

**Preconditions.** `002465F0` requires ~~`size` bytes~~ **`max(size, 0xBC)` bytes** of writable storage. It `memset`s
`size` bytes (`00246626`), then writes the fixed header at `+0x40`–`+0xBB` whatever `size` was: `+0x40`, `+0x44`, `+0x48`,
and `+0x98`–`+0xBB`, the last being the dword `+0xB8` (`00246700`). *Corrected 2026-09-25 (FABLE, Claude Opus 5.5), on OPUS
block 298, which executed a small-size case (`size = 0x40`).*
- **Bytes `size`…`0xBB` are written without being cleared first.** Some of those writes are read-modify-writes: the
  `xor` merge into `+0x40` (`00246647`–`00246660`), the `and` masks on `+0x44` (`00246670`) and `+0x40` (`002466D1`),
  and the `or` into `+0x40` (`002466F2`).
- So for `size < 0x44`, the flags word at `+0x40` keeps bits from whatever the storage held before.
- `00244F50` requires nothing — it allocates.

**Postconditions.** After construction: the header above is written and **the handler has been
called once with message id 1**. The message is `{1, locals->a, locals->b}` — **both** payload
qwords are copied from the caller's record (`00246726` reads `[rsi+8]`, `0024672F` reads
`[rsi+0x10]`), and both are left zero when the argument is NULL.

**Invariants.**
- `self[0] != NULL` — always. A null handler becomes the default.
- **Every widget starts with `1.0f` at `+0xB8` and `100` at `+0x44`.**
- An unhandled message id **tail-jumps to `005C5230`**; a handler never simply returns for an id it
  does not know. *(Observed in every handler read; not proven for all 267.)*

## 5. State

| | detail |
|---|---|
| **read** | `0208ED5C` (generation parity), `00915198` (header table), `0208EA58` (the pool), `0208EA28` (**one of three UI roots** - see below), `0208EAC0`/`0208EBC0`/`0208EBC8` (the focus stack) |
| **written** | the object; the pool slot's `+0xA2`; the focus stack on detach |
| **allocated** | `00244F50`: a **fixed pool of 112 records at stride `0x120`** for `size <= 0x120`, else `002497B0` (heap). A slot is free when `!(flags[+0x40] & 0x4000)` **and** `[+0xA2] == 0`; taking it sets `[+0xA2] = 1` |
| **deallocated** | `00245020` → `002482E0` on the ordinary path |

### ✖ WITHDRAWN 2026-09-13: `0208EA28` is written, and a reimplementation must NOT pass NULL

**ASTRA is right** (`ASTRA-CONTRA-OPUS-WIDGET-ROOTS`). `0208EA20`, `0208EA28` and `0208EA30` are
**three UI roots, and a startup loop writes all three**:

```
00247CF2  mov  ebp, 3                       ; three of them
00247D20  lea  rdi, [rip+...]  -> 0208EA20  ; the base
00247D74  mov  ecx, 0xC8 / call 002497B0    ; allocate a 0xC8-byte object
00247D9A  call 002465F0                     ; construct it (this contract's own §1)
00247D9F  mov  qword ptr [rdi], rbx         ; <-- THE STORE
00247DAC  add  rdi, 8
00247DB0  sub  rbp, 1 / jne 00247D40
```

**Re-derived from the image on 2026-09-13; ASTRA's reading holds in every particular**, including
`ebp = 3` and the `+8` stride.

> **Why my evidence said otherwise, which is the part worth keeping.** The withdrawn paragraph
> reported *"149 loads and **zero stores**"* from a raw byte scan of `.text`, and boasted that the
> figure did not depend on the function graph being complete. **It was a scan for `mov [rip+disp],
> reg` — and this store is `mov [rdi], rbx`.** An indirect store through a walking pointer is
> invisible to it, by construction.
>
> The paragraph even *anticipated* the objection and got it wrong in the most specific way
> available: it said the two functions that `lea` the neighbouring base `0208EA20` — naming
> `00247D20`, the very instruction above — *"write only `[base+0]`, never `[base+8]`"*. **I had the
> right instruction in my hand and did not follow the loop it starts.** A `lea` of an array base is
> the beginning of a walk, and "never written" is a negative that a rip-relative scan cannot
> establish for any array member.

**What this costs.** The architectural conclusion — *"a reimplementation must pass NULL there too"*
— is **wrong and would have been expensive**: every menu would be built parentless. `00247950`
loads `*(0208EA28)` and **attaches** a parentless widget under it via `00248220`; it never reaches
`00245020`, which is teardown (`00244980` is what reaches that, after `00246C20`). The request-router
page already carries that half, corrected on `ASTRA-CONTRA-FABLE-WIDGET-ROOTS`.

**What survives, reduced to what it actually shows.** Sampled readers `00228117` and `0023BD04` load
the root into `rcx` and pass it into `00244960` / `00246AD0` with no null test, and **those two
callees work on `rdx`**. That was a sample of 2 of 139 then and it is a sample of 2 of 139 now; it
never supported "the pointer is ignored" as a general claim, and with the root now known to be
non-NULL it supports even less. **Two callees not dereferencing a valid pointer is unremarkable.**

**Still open:** what each of the three roots is for, what orders children under them, and when the
startup loop runs relative to area load. Those are ASTRA's `missing_information` and are not settled
here.

## 6. Relationships

```
00244F00  destroy
   ├─ flags40 |= 0x40
   ├─ if (flags40 & 0x21) == 0x21  ->  00244DD0        (deferred path — schedules, then sends {15})
   ├─ handler(self, &MSG_15)                            00915058 = {15,0,0}   SELF ONLY
   └─ 00245020  tear down
        ├─ 002448D0   detach / pop the focus stack
        ├─ 00244700(self, 1)
        ├─ handler(self, &MSG_18)                       00915070 = {18,0,0}
        ├─ 002473B0   broadcast MSG_18 down +0x18 / +0x20   SELF AND SUBTREE
        └─ (flags40 & 0x20) ? 002473F0 + set bit 10 : tail-jump 002482E0
```

## 7. State transitions

```
(no object)
   ──[00244F50 or caller-owned storage]──▶ RAW
RAW ──[002465F0: memset, header, handler(self,{1,·,locals})]──▶ LIVE
LIVE ──[00248030, generation bit 17 != 0208ED5C, and bit 18 CLEAR]──▶ handler(self,{2,·,·}), then bit 17 := parity, LIVE
LIVE ──[00248030, generation differs, bit 18 SET]──▶ no handler call; bit 17 := parity, LIVE   (bit 18 SUPPRESSES)
LIVE ──[draw pass]──▶ handler(self,{3|4|5}) ──▶ LIVE
LIVE ──[00244F00]──▶ handler(self,{15}) ──▶ DYING
DYING ──[00245020]──▶ handler(self,{18}) to self and every descendant ──▶ RELEASING
DYING ──[flags40 & 0x20]──▶ DEFERRED   (bit 1 cleared, bit 10 set; not freed)
RELEASING ──[002482E0: children first, unlink, resources]──▶ handler(self,{24}) ──▶ bit 10 cleared
RELEASING ──[flags40 bit 14 CLEAR]──▶ FREED   (0x3697F0 releases the object)
RELEASING ──[flags40 bit 14 SET]──▶ POOLED  (bit 14 cleared, +0xA2 zeroed; NOT freed)
FREED|POOLED ──[saved +0x08, if non-null]──▶ `jmp` continuation, no arguments
```

> **✖ Two corrections here, 2026-09-13 (`ASTRA-CONTRA-OPUS-WIDGET-GENERATION`).**
>
> **1. The bit-18 polarity was inverted.** `002480E1 bt ecx, 0x12` / `002480E5 jb 0x248101`
> **jumps past** the `call rax` at `002480F9`. `jb` after `bt` means *carry set* means *bit set*,
> so **a set bit 18 suppresses message 2** - the transition above said it admitted it. The
> protocol page was corrected first; this state machine was not, and **a state machine is the
> worst place for an inverted guard**, because a reimplementation reads the transition and not
> the prose.
>
> **2. Bit 17 is replaced, not cleared.** `00248101` clears it and `00248108`-`00248110`
> immediately re-sets it from `0208ED5C & 1`. The global is **reloaded at `002480FB`, after the
> callback**, so a handler that flips the parity has its new value stamped; on the suppressed
> path the value read before the branch is used. **Both paths stamp**, which is why the
> suppressed node still leaves the walk consistent.
>
> The `+0x40` bit-10 release ASTRA names (`00248097` → `002482E0`) is an **earlier** gate on the
> same generation mismatch and is not part of this transition.

## 8. Script · resource · event interactions

None directly. Message ids **above 25 are sent only from outside the widget core**
(`00244000`–`00249000`) — they are the application's own vocabulary, and id 16 alone has 20 senders.

## 9. Determinism

**RNG:** none. **Timing:** message 2 is driven by a global generation counter, not a clock.
**Threading:** UNRESOLVED — nothing here establishes which thread runs the tree.

## 10. Failure paths and edge conditions

| condition | behaviour | anchor |
|---|---|---|
| handler argument is NULL | replaced with `005C5230` | `00246635` |
| `size == 0` at `00244F50` | becomes `0xC0` | `00244F70` |
| `size > 0x120` | skips the pool, heap-allocates | `00244F7D` |
| pool exhausted (112 slots) | falls through to the heap | `00244FAB` |
| `00244F00(NULL)` | returns immediately | `00244F03` |
| an id no handler arm matches | tail-jump to the default handler | every handler read |

## 11. Observable behaviour

A panel appears, answers input, and vanishes. **The player-visible consequence of the two-phase
destroy is that a widget gets warning (`15`) before its subtree is told (`18`)** — 27.5 % of handlers
answer the first, 65.4 % the second.

## 12. Reproduction formula

**Re-derived instruction by instruction from `002465F0` on 2026-09-13
(`OPUS-WIDGET-SPEC-ALIGN`).** The previous formula had drifted from §3's own header table, which was
already right: it dropped the pool bit, the phase counter, two field writes and the real shape of
the construct message. What follows matches the body.

```c
Widget *Widget_Create(uint32_t size, WidgetProc proc, const WidgetMessage *initArgs)
{
    /* NOT re-derived by this pass -- see the note below. */
    if (size == 0) size = 0xC0;
    void *mem = (size <= 0x120) ? pool_take() : heap_alloc(size);   /* pool: 112 x 0x120 */
    if (!mem) mem = heap_alloc(size);
    return Widget_Construct(mem, size, proc, initArgs, mem_came_from_pool);
}

/* `initArgs` is a WidgetMessage*, NOT an opaque payload. 5th argument at [rsp+0x20]. */
Widget *Widget_Construct(void *obj, uint32_t size, WidgetProc proc,
                         const WidgetMessage *initArgs, int pooled)
{
    /* The message is built on the stack BEFORE the object is touched: id first, then both
       payload qwords zeroed by one 16-byte store. 0024660A, 00246620. */
    WidgetMessage m;
    m.id = 1;  m.a = 0;  m.b = 0;

    memset(obj, 0, size);                                   /* 00246626 -- the lifetime begins */
    Widget *w = obj;

    w->proc = proc ? proc : Widget_DefaultProc;             /* 00246635 cmove, 00246641 */

    /* Bit 17 is a masked REPLACE, not an OR: the xor-and-xor idiom at 00246644-00246650. */
    uint32_t g = *(uint32_t *)0x0208ED5C;
    w->flags = (w->flags & ~0x20000) | ((g << 17) & 0x20000);
    w->flags |= 0x80A;                                      /* 00246653 */
    if (*(uint32_t *)0x0208F560 != 0)                       /* 00246659 */
        w->flags ^= (g & 1) << 17;                          /* 00246665-0024666D: forces bit 17 to 0 */
                                                            /* CHECKED AGAIN 2026-09-13 and this is RIGHT: the masked */
                                                            /* replace above has already set bit 17 to (g & 1), so the */
                                                            /* xor with the same value clears it either way. An earlier */
                                                            /* pass this session read 0024666B in isolation and nearly */
                                                            /* published a correction to a correct line. */

    w->field44 &= ~0x70000;                                 /* 00246670 */
    w->table    = &TABLE_00915198;                          /* 00246687 */
    w->fAC = 6;  w->fAD = 6;                                /* always 6 -- see the +0xAC row in §3 */
    w->flags &= ~0x4000;                                    /* 002466D1 */
    w->f7C   &= ~0xF;                                       /* 002466D8 */
    w->fA1    = 0xFF80;                                     /* 002466E6, a 16-bit store */
    w->flags |= (pooled & 1) << 14;                         /* 002466F2 -- THE POOL BIT */
    *(uint16_t *)&w->field44 = 100;                         /* 002466FA, a 16-bit STORE, not an OR */
    w->fB8 = 1.0f;                                          /* 00246700 */
    w->fA0 = 0x80;                                          /* 0024670A */
    w->f98 = 0;                                             /* 00246711 */
    w->f9C = 0x800080;                                      /* 00246717 */

    /* The caller's message is forwarded by PAYLOAD, not by pointer: its id is discarded and
       replaced by 1, and only its two qwords are copied. 00246721-00246733. */
    if (initArgs) { m.a = initArgs->a;  m.b = initArgs->b; }

    w->proc(w, &m);                       /* 00246748 -- the construct message, id 1 */

    /* AFTER the callback, never before. 0024674A-0024675C. */
    if (!NotHalfRate() && InsideWorldSimulationTick())
        w->fB4 = 1;                                         /* the half-rate phase counter, §3a */

    return w;
}
```

### What the previous formula got wrong, and why each matters

| drift | consequence for a reimplementation |
|---|---|
| `WidgetMessage m = { 1, 0, (uint64_t)locals }` | **The payload is wrong.** `locals` is a `WidgetMessage *`; the constructor copies `initArgs->a` **and** `initArgs->b` into a fresh message whose id is forced to `1`. The old form put the *pointer* in `b` and left `a` zero, so every construct handler that reads `a` would see `0` and every one that reads `b` would dereference a pointer where a value belongs. |
| `& ~0x4000` with no `\| (pooled << 14)` | **The pool bit is lost.** §3 records bit 14 as *"this object came out of the fixed pool"*; the constructor clears it and then re-sets it from the fifth argument. A reimplementation built from the old formula marks **every** object as heap-owned. |
| no `0208F560` gate | The generation bit is set unconditionally instead of being **forced to 0** when that global is non-zero. |
| no `+0xAC` / `+0xAD` | Two header bytes left at `0` instead of `6`. §3 already had this, including the proof that the `0xF9` arm is unreachable. |
| no `+0x7C &= ~0xF` | A fourth header field left untouched. |
| `\| 100` on `+0x44` | The code does a **16-bit store**, not an OR. Equivalent only because the memset ran first — true here, and not a property of the expression. |
| the `+0xB4` write absent | **The ordering fact, and the one worth most.** See below. |

### Callback ordering and the lifecycle boundary

**The object's life begins at the `memset` (`00246626`) and every header field is written before the
handler is called** (`00246748`). The handler is therefore the first moment any other code sees the
object, and it sees a fully initialised header — **except one field**.

**`+0xB4` is set after the callback returns.** A construct handler that reads its own `+0xB4` during
message id 1 sees **`0`**, never `1`, whatever the frame-rate mode is. §3a records 33 handler sites
that call `001EDEC0([self+0xB4])`, and notes that the two resolved by jump-table decode sit on the
**id 2** arm rather than id 1 — consistent with this ordering, and the reason it matters: a
reimplementation that sets the phase counter before dispatching id 1 changes what those sites read
on the object's very first frame.

**The handler call is unconditional in practice.** `0024673B test rbx, rbx / je` guards it, but
`rbx` was already `cmove`d to `005C5230` at `00246635` when the argument was null, so it **cannot**
be zero at the test. The guard is dead code; the formula omits it deliberately rather than
reproducing a branch that never taken.

> **Not re-derived by this pass.** `Widget_Create`'s own body (`00244F50`) — the `0xC0` default, the
> `0x120` pool threshold, the 112-slot pool and the heap fallback — is carried over unchanged from
> the earlier reading and was **not** re-read here. `NotHalfRate()` and
> `InsideWorldSimulationTick()` stand for `001EDDA0` and `00314960`, decoded in §3a, not re-derived
> here either.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent** — nothing here has been
observed in a live process, which is why readiness stops at `CONTRACT READY`.

**RECLASSIFIED 2026-09-12 (`OPUS-S13-CLASSIFY-THREE`), and this one is the clearest case of the
three.** The isolated evidence was already written — in **§13b, immediately below**. `check_gate26`
reads §13, found the word `EMPTY`, and scored the contract `nothing executed` while a full
differential run sat one heading away. **The evidence existed, was correct, and was in a place the
instrument does not look.**

**Instrument:** [`diff_widget_construct.py`](../../../../Reconstruction/Tests/Differential/diff_widget_construct.py)
against [`widget_construct.c`](../../../../Reconstruction/Game/UI/widget_construct.c).
**Re-run 2026-09-12:** structural and state parity over 192 bytes of header, across **every shipped
object size and all 16 combinations** of the environment the constructor reads. §13b has the detail
and is unchanged.

*A heading is part of the evidence.* Nothing about the live gap changes.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface — and adjudicated

**99 generated points: 73 KILLED · 10 SURVIVED · 14 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 2 INVALID. Verdict `FAIL_INCOMPLETE`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/widget_construct2` (ignored path); the first run, before the case added below, is `widget_construct`. The table for every pilot, and the four kinds a survivor can be, are on [`../../../Reconstruction/MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

**Twelve survivors became ten, and the ten have a single root cause.**

**The two that were real gaps (kind D), now killed.** `msg_out->pad04 = 0` → `= 1` and the message build's `(a != NULL) ? ld64(a + 0x08) : 0` → `: 1` sit on the **NULL args** arm, and every case passed a real args block. The NULL path is the original's, not an invention — `0024661A mov rsi, r9` saves the pointer and `00246721 test rsi, rsi` tests it, which is why the reconstruction carries the ternary — so driving it is inside the function's domain. Four cases now do, on the smallest and largest real object sizes, through a sentinel both sides read identically. 324 cases, 0 mismatches.

**The ten that remain cannot be killed, and one sentence explains all of them:**

> **The constructor zeroes the object before it reads anything back**, so every read-modify-write it performs afterwards reads either freshly-zeroed memory or a value this same function just wrote — and the largest value it ever writes into the flags word is `0x20000 | 0x80A`. **Byte 3 is zero at every `ld32` in the operation, every mask is applied to zero or to a small value, and the two offset mutants write ZERO into ZEROED memory.**

| mutant | kind | why no case can kill it |
|---|---|---|
| `ld32`'s `p[3]`, its `<< 24`, and the `<<` in it | **A** | all three are only observable if the byte at `+3` of some read is non-zero, and it never is |
| `0x20000` → `0x20001` in the generation seed | **A** | the value masked is `gen << 17`, whose bit 0 is clear by construction, so the two masks agree on every input |
| `0xFFF8FFFF` → `0xFFF90000` at `+0x44` | **A** | `+0x44` is zero at that read — the memset precedes it and nothing writes it in between — and `0 & anything` is `0` |
| `13` → `14` in the three-bit sign-extend | **A** | the same `+0x44`, still zero: `0 << 13` and `0 << 14` both give `0`, so `d` is `0` either way |
| `0xFFFFFFF0` → `0xFFFFFFF1` at `+0x7C` | **A** | `+0x7C` is zero at its only read before the write |
| `WIDGET_F7C 0x7C` → `0x7D` and `WIDGET_F98 0x98` → `0x99` | **A** | both write **zero**, and both destinations are inside the zeroed region, so the object is byte-identical either way |
| `st64`'s `i < 8` → `i < 9` | **C** | the ninth iteration evaluates `v >> 64` on a `uint64_t`, which is **undefined**, not a behaviour a suite can be required to distinguish |

> **This is a fact about the original, not only about the fixture.** Those masks are **unobservable in this path**: the constructor cannot see a non-zero `+0x44` or `+0x7C` because it zeroed them itself, and every real object size covers the whole header — the smallest the harness drives is `0xC0` and the highest field is `+0xB8`. **A reimplementation may drop every one of those masks and remain byte-identical here**, and it must not, because nothing establishes that this is the object's only constructor.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-068`](../../_experiments/EXP-068-ui-generic-controls.md) — **method B**, isolated original-code execution.
- [`EXP-069`](../../_experiments/EXP-069-ui-native-feedback.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 13b. One operation reimplemented and differential-tested — 2026-09-08

**Reconstruction:** [`../../../../Reconstruction/Game/UI/widget_construct.c`](../../../../Reconstruction/Game/UI/widget_construct.c)
**Test:** [`../../../../Reconstruction/Tests/Differential/diff_widget_construct.py`](../../../../Reconstruction/Tests/Differential/diff_widget_construct.py)

§12's reproduction formula for the **header** was implemented and compared against the shipped 395
bytes at `002465F0` under emulation:

```
cases                     : 320   (20 real object sizes x 16 environment combinations)
header bytes compared     : 192 per case
  non-zero in the densest : 20    (so 172 of 192 bytes must stay ZERO)
mismatches                : 0
```

**The sparseness is the test.** A reconstruction that wrote one stray byte anywhere in `0x00..0xC0`
fails here and would fail nowhere else — the three earlier harnesses compare a return value, a
31-int array and a linked list, none of which can catch a spurious write.

**Readiness stays `CONTRACT READY`.** §2 lists ten operations and **one** is tested; §13 is still
empty. Promoting the subsystem on its header writer would be exactly the overstatement the ladder
exists to prevent.

## 14. Unresolved

- ~~**The deferred destroy path `00244DD0`** (301 B), taken when `flags40 & 0x21 == 0x21`, is unread —
  so the 15-before-18 ordering is established for one path only.~~ **Read 2026-09-18 — `DL-3`
  closed.** `00244DD0` is a **deferred-completion scheduler**, not a teardown: it computes the
  widget's timescale `+0xB8` (`1.0f`, or `1.0f/[01E02820]` when `byte[02064AD2]!=0` and
  `sbyte[02064AD3]==2` — the global resets itself to `1.0f` when ≤0), then dispatches on `+0x7C`'s
  low nibble. Modes **0 and 3** schedule: `+0x40 |= bit9` (the deferred-destroy arm the
  `and 0xFFFFFBFF` clear at release names), `+0x68` = the named record `009151AC`
  (`"map\rbl_a\rbl_a02\global"`) when `+0x40` bit 16 is set, else `[+0x48]+0x14`; `+0x74` = the
  global tick `[0208F570]`; `+0x78` = `1.0f`; `+0x70` = the record's `u16[+2]` **× 60/1000** —
  a milliseconds-to-ticks conversion (`edi*0x3C * 0x10624DD3 >> 38`, the `⌈2³⁸/1000⌉` magic),
  forced to 0 when `[001EBA40()+0x280]==1`, or taken from `+0x7C`'s top 10 bits when its bit
  0xB was armed (that bit is cleared). Mode **2** recomputes the deadline:
  `+0x74 = 2*[0208F570] - [+0x70] - [+0x74]` (and zeroes `+0x70` first when `+0x40` bit 16 is
  clear). Mode **1** bails before even the shared tail. The tail arms `+0x7C` nibble = 4 and
  bits 4–5, then sends **`{15}`** to self through `[rbx]` — so the 15-before-18 ordering holds
  on **both** destroy paths; what the deferred path omits is `{18}` and `00245020` inline,
  whose work is left for the timer the schedule describes.
- **23 of the 32 message ids have no meaning.** `DL-1`.
- **Whether handlers exist that were installed without a constructor call.** `DL-2`.
- **Which thread runs the tree.** ~~And what `+0xB4`'s two global predicates are~~ — **answered
  2026-09-10, §3a**: `001EDDA0` is the half-rate-mode test over `01F82E38`/`01DFE0C0`, and
  `00314960` reads `022C2548`, the inside-`World_UpdateSimulationTick` flag. What remains open is
  narrower: **which arm of which handlers actually consults `001EDEC0(self->fieldB4)`** — 33
  direct sites found, 2 resolved to the id-2 arm, 31 unresolved, callees unsearched.
- **The 112-slot pool's eviction policy**, if any: nothing read shows a slot being released.
- **Everything past `+0xC0`.** The differential test compares 192 bytes because that is where the
  constructor's writes stop; objects run to `0xBC08` and the rest is written by their own procs.

## 15. Evidence

| claim | evidence | tier |
|---|---|---|
| handler at `+0x00`, default `005C5230` | `00246641`, `00246635` | 1 |
| the constructor sends id 1 | `0024660A` builds `{1,·,·}`; `00246748` calls through `[obj]`. **Recorded from the emulated original 2026-09-08**: exactly **one** call per construction over 320 cases, and the message is **24 bytes** — `id = 1`, `+0x04` zero, `+0x08` and `+0x10` the caller's argument qwords **copied verbatim**. A first reading of the `movdqu` said those sixteen bytes were zeroed with only a zero-extended dword at `+0x10`; the recording disagreed on 320 of 320, and the reading was wrong | 1 |
| `+0x18` child / `+0x20` sibling | the recursion in `002473B0` | 1 |
| destroy is two-phase, 15 then 18 | `00244F34` then `00244F39` → `00245020` | 1 |
| the deferred destroy path `00244DD0` also sends `{15}` — to self via `[rbx]` — but schedules the rest instead of running `{18}`/`00245020` inline, so 15-before-18 holds on both destroy paths | `00244F0A` `+0x40 \|= 0x40`; `00244F14`–`00244F19` `(+0x40 & 0x21)==0x21` → tail-jmp `00244DD0`; `00244EF2` `call [rbx]` with record `01E0C0F8` `{0xF,…}`; no `{18}`/`00245020` site exists in the body | 1 (static) |
| `00244DD0` schedules the deferred completion: `+0x68` message/record pointer, `+0x74` start tick `[0208F570]`, `+0x70` delay = `u16[+2] * 60/1000` (ms→60 Hz ticks), `+0x78`/`+0xB8` timescales | `00244E88` store `+0x68` (`009151AC` `"map\rbl_a\rbl_a02\global"` when `+0x40` bit 16, else `[+0x48]+0x14`); `00244E8C` `mov eax,[0208F570]` → `+0x74`; `00244EC2`–`00244ED4` `edi*0x3C * 0x10624DD3 >> 38` → `+0x70`; `+0x7C` nibble → 4, bits 4–5 at `00244ED7`–`00244EDF` | 1 (static) |
| `00244DD0`'s `+0x7C` low-nibble is a mode field: 0/3 schedule, 2 recomputes the deadline, 1 bails before the tail | `00244E2F`–`00244E41` `sar([+0x7C]<<0x1C,0x1C)` then `je`/`sub 2`/`cmp 1` chain; mode-2 arm `00244E6D` `2*[0208F570] - [+0x70] - [+0x74]`; mode-1 falls to `00244EF7` | 1 (static) |
| 297 sites / 267 handlers / 32 ids | `widget_messages.py`, three passes with denominators; 297 = 280 `call` + 17 tail-jump `jmp` transfer sites | 1  **§15a: all three reproduced 2026-09-12; §15b: the handler census rebuilt on the proc-slot rule 2026-09-13** |
| the pool is 112 × `0x120` | `00244FAB` bound, `00244FA4` stride | 1 |
| `+0xB4` is a half-rate phase counter: constructor sets `1` under HALFRATE **and** inside the sim tick; the walker `00248030` pins it to `0` outside HALFRATE and increments it under it; `001EDEC0(x)` gates id-2 work on `x` being even | all three functions read instruction by instruction (`0024674A`-`0024675C`, `00248044`-`0024813A`, `001EDEC0`); `022C2548` written only by `World_UpdateSimulationTick`'s first and last instructions, 3 references image-wide with a passing control; `01DFE0C0` 4 references, one writer | 1 |
| the constructor calls the proc **before** writing `+0xB4` | `00246748` `call rax`, then `0024674A`/`00246753` predicates, then `0024675C`. The object was `memset` to zero at `00246626`, so **an id-1 handler always sees `+0xB4 == 0`** | 1 |
| `002445D0` roots on `dword[arg]==1`: `+0x40 |= 0x23`, `[arg+8]`→`+0xC0`, `+0x98`=0, `+0x9C`/`+0x9E`=`0x200`/`0x1C0` | body read 2026-09-15 (`002445D0`–`0024460C`); both paths return 0 | 1 (static) |
| `00248220` tail-appends on `+0x18`/`+0x20`, sets `child+0x10`=parent, `parent+0x30`++; propagates parent bit 5 through `002463F0`+`002418E0`; `+0x40 \|= 0x2000` always | body read 2026-09-15 (`00248220`–`002482DD`) | 1 (static) |
| `002463F0` is a pre-order recursive visitor: `call rdx` then `+0x18`/`+0x20` descent | body read 2026-09-15 (`002463F0`–`00246446`) | 1 (static) |
| `00247490` prunes subtrees: gate `+0x40` bit 1 **and** bit 0 `!= edx`; flips bit 0, fires `[+0x00]` callback, recurses only on pass | body read 2026-09-15 (`00247490`–`00247505`) | 1 (static) |
| `00582790`'s 12-slot binding is `00249580`: first-fit over `02090790`, 12 × `0x20` slots, bit-0 busy | `00249590`–`0024959E` scan loop, `002495A3`–`002495BB` claim | 1 (static) |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The three-number census reproduces exactly

`widget_messages.py` re-run over the shipped image:

| stated | measured |
|---|---|
| **297 sites** | 297 constructor transfer sites — 280 `call` + 17 tail-jump `jmp` forwards (276 of the calls recover a handler, 4 do not) |
| ~~280 sites~~ *(superseded)* | 280 constructor `call` sites only — the old instrument did not match `jmp` transfers |
| **267 handlers** | **267 — corrected 2026-09-13**; the 251 below is superseded. 251 − 5 + 14 + 7, each term re-derived from the image (§15b) |
| ~~251 handlers~~ *(superseded)* | 251 — 239 confirmed by an address-order `lea`, 13 candidates reached by a backward branch, **one address in both** |
| ~~**32 ids**~~ *(denominator restated 2026-09-20)* | ids 1–26 plus 29, 30, 53, 285, 287, 289 — 32 distinct **over the 247 handlers `widget_messages.py` decodes as EXACT**, not over the 267. Its 11 BOUNDED and 9 UNPARSED handlers are excluded from that histogram by its own rule ("upper bounds, NOT counted below"), and **twenty of those carry ids the 32 does not**. See §15c. |
| **56 ids** | ids **1–53 except 27 and 28**, plus **285–289** — **56 distinct** over the 264 `exact` rows of `widget-message-handlers.tsv`, every one re-derived from the image by `check_widget_message_ids.py`. §15c |

### 15b. The population is 267, and one rule replaces three heuristics — 2026-09-13 (OPUS)

FABLE raised (`FABLE-REQ-OPUS-WIDGETPOP`, answering DL-2) that pass 1 missed procedures installed
through routes its heuristic could not see. **Every term is confirmed here independently, by asking
one question of each candidate: does its address reach a widget constructor's `proc` slot?**

| term | verdict |
|---|---|
| **− 5** | `0027D700`, `0027D740` (interior read 2026-09-17, SWE2-FRONTIER: `00808F10` first at [`0027D747`](../../_index/ADDRESS-INDEX.md), `00273270` at `0027D819`), `0027E3E0`, `0027E4E0`, `0027E7B0` reach `00368A50`, `002969F0`, `00279C48` — **never a widget constructor**. Not widget procedures |
| **+ 14** | all fourteen reach a `proc` slot: thirteen as `rdx` into `00244F50`, and `002985D0` as `r8` |
| **+ 7** | materialised into `r9` or `r15` and **forwarded one hop**: `00564B44 mov rdx, r9` then `00564B4B call 0x244F50`, and `004070FC mov rdx, r15` then `00407102 call 0x244F50` |

**251 − 5 + 14 + 7 = 267.** Every per-id share is therefore over 251 and is restated against 267.

> **The lesson is about the instrument, not the count.** Pass 1 searched for *ways an address gets
> installed* — a direct store, then a `jmp` constructor site, then a wrapper — and each new route
> needed a new rule. **The definition needs only one: a widget procedure is an address that reaches a
> constructor's `proc` slot.** That single test subsumes all three proposed extensions and, applied
> here, sorted 26 candidates that the reachability census could not tell apart — all 26 are
> address-taken by exactly one `lea` and stored nowhere, so *how* the address travels discriminates
> nothing. **Where it lands discriminates everything.**
>
> The one thing a tool must still do that a displacement scan does not: **follow one hop of argument
> forwarding**, since the `+7` reach the constructor only through `00564AC0` and `00406E80`.

### The one handler in both sets is the default stub

`251` is the size of the **union**, and the single address appearing in both halves is **`005C5230`
— the default handler itself**, whose whole body is `33 C0 C3`: `xor eax, eax` / `ret`. That is
exactly the handler one would expect to be reached both by a direct `lea` and by a backward branch
into a shared call site: it is the most widely shared handler in the system, so it is the one the two
recovery routes both find.

> **The tool said `population 251 = 239 confirmed + 13 candidates`, and 239 + 13 is 252.** The number
> was right and the arithmetic beside it was not — a line that invites a reader to "correct" a
> correct figure. `widget_messages.py` now prints `239 confirmed UNION 13 candidates, 1 in both` and
> names the overlap.

### Confirmed at the byte level

| claim | image |
|---|---|
| the pool is 112 × `0x120` | `00244FA4 add rbx, 0x120` and `00244FAB cmp eax, 0x70` — 288-byte stride, 112 entries |
| the default handler is `005C5230` | `33 C0 C3` — `xor eax, eax` / `ret`, three bytes, returning **0** |
| destroy's second phase | `00244F39 call 00245020` |

**Not claimed:** the emulated-original record behind "the constructor sends id 1" is unchanged, and
nothing here is a live observation.

### 15c. The id count is 56 — two thirds a denominator, one third a defect — 2026-09-20 (OPUS)

`widget_messages.py` still reports 32 distinct ids when re-run today. `widget-message-handlers.tsv`,
whose 264 `exact` rows are now each re-derived from the image by `check_widget_message_ids.py`,
gives **56**. The 24-id gap comes from exactly **17 handlers**, and they split into two kinds that
must not be reported as one.

**Eleven are an honest floor.** `widget_messages.py` classifies its 267 handlers as
**247 EXACT / 11 BOUNDED / 9 UNPARSED** and prints its histogram over the 247 alone — its own line
says the BOUNDED are "upper bounds, **NOT** counted below". Nine of its eleven BOUNDED and two of
its nine UNPARSED carry **ids 31–52**, sixteen of them from a single row — the one whose
`upper-bound` cell claimed all 52 ids and answers 21. Nothing is wrong here except the label on the
figure: **"32 ids" reads as a statement about the protocol and is a statement about a 247-handler
subset.**

**The other six are a defect in the instrument, and it is the same defect the table inherited.**
Asked directly, `widget_messages.py` returns **one id for each of ten handlers that answer six to
ten**, every one classified **EXACT** rather than as a bound. And every one of the ten is the same
thing: **the pivot of the body's binary-search root** — the `cmp <id>, K` immediately after
`mov ecx, dword ptr [rdx]`, whose `jg` opens the high half and whose `je` takes K's own arm. The
tool reads that compare and stops. One mechanism, not ten coincidences, and it is worse than the
eleven above, because **a confident under-report looks authoritative** where an admitted bound does
not. Four of the ten returned `12`, and the rest `18`, `16`, `10` and `8` twice. Read end to end
they answer sets of six, seven, eight, nine and ten ids; the six that matter here supply **286** and
**288**, completing the high band.

**The per-handler evidence is on the rows, not here.** Each of the ten carries its full dispatch
reading — pivot, `jg` subtree, running subtractions, range test and jump-table arms, with the
default-arm entries counted out — in its own `note` in
[`widget-message-handlers.tsv`](widget-message-handlers.tsv), which is where those addresses are the
subject rather than a citation. **Naming them in this section would make it inherit ten edges into
Items/Equipment/Shops/License and two into CombatAction that it makes no claim about**, and a
reconciliation section is the wrong place to open a crossings analysis. Pass 22's alternative is
taken deliberately.

`widget_messages.py` is **not** fixed here — it is a separate instrument with its own consumers,
six database documents and three peer work trees among them, and the correction it needs is
recorded rather than applied.

**So the id space has two bands, and the shape is the finding rather than the count.** The low band
is **1–53 with only 27 and 28 absent** — 51 of 53, effectively dense. The high band is
**285–289 (`0x11D`–`0x121`), five values, contiguous, with 231 unused between them.** Id **1 is
answered by 262 of the 264 rows**; ten ids — 23, 36, 45, 47, 48, 49, 50, 51, 52, 289 — are answered
by exactly one handler each.

**The floor, stated:** this is the set of ids handlers **test for**, not the set senders can send.
An id nobody tests is invisible to both instruments and would reach `005C5230` and return 0
indistinguishably from one that is tested and ignored.

### 15d. The decision on `widget_messages.py`, with the blast radius measured — 2026-09-20 (OPUS)

§15c recorded the pivot defect and deliberately did not fix it. This is the decision it asked for,
and the measurement changed it: **the defect is not hypothetical — it has already produced two
withdrawn published claims, and the chain is now traced end to end.**

**What the tool actually returns for the seven high-band receivers**, asked directly today:

| handler | `widget_messages.py` | `widget-message-handlers.tsv` (re-derived from the image) |
|---|---|---|
| `00280DE0` | `exact [1, 2, 10, 12, 13, 14, 15, 16, 18, 19, 287]` | agrees |
| `0055CD40` | `exact [1, 2, 4, 8, 9, 10, 12, 15, 18, 19, 20, 23, 285]` | agrees |
| `005691E0` | `exact [1, 2, 5, 8, 9, 10, 12, 16, 17, 18, 19, 20, 22, 26, 289]` | agrees |
| `002C2320` | **`exact [8]`** | `1, 8, 9, 10, 12, 14, 18, 19, **287**` |
| `003FF360` | **`exact [12]`** | `1, 8, 10, 12, 18, 19, **285**` |
| `00557DB0` | **`exact [10]`** | `1, 2, 10, 12, 15, 18, 19, 20, **285**` |
| `00565E00` | **`exact [8]`** | `1, 8, 9, 10, 12, 13, 14, 16, 18, **287**` |

**Four of the ten are exactly the receivers that complete ids 285 and 287.** The tool's histogram
therefore prints `285 → 1 handler`, `287 → 1 handler`, `289 → 1 handler`, when the true counts are
**3, 3 and 1**.

**And that is where the high band's withdrawn property came from.** The chain:

> pivot defect → histogram shows one handler each for 285/287/289 → *"Exactly one receiver each"* on
> [the protocol page](the-widget-message-protocol.md) → that property used in `OPEN-QUESTIONS.md`
> DL-1 to take 285/287/289 off the open count as a family → and `CON-133`'s second property, the
> *"dedicated `je` on their own large constant"*, misreading the same binary-search roots.

FABLE withdrew the first property on 2026-09-20; `CON-133` withdrew the second the same day. **Both
trace to this instrument.** `003FF360` returning `12` is the defect in one line: `12` is `0xC`, the
pivot of its root `cmp ecx, 0xC`, and the id it really answers — `285` — is reached through
*cumulative subtractions* (`sub ecx,0x12` / `sub ecx,1` / `cmp ecx,0x10A`), so **the literal `0x11D`
never appears in the body at all.**

**The decision: retire the id histogram, keep the tool.**

1. **Do not write a general comparison-tree decoder.** That approach is already measured and already
   rejected — `OPUS-NOTE-THE-GENERAL-COMPARISON-TREE-DECODER-WAS-WORSE-AND-WAS-REVERTED` records a
   tree walker scoring **2 of 201** against the flat walk's **171 of 201**, because a chain decoder
   cannot infer where the dispatch *ends* while a jump table gets that boundary for free.
2. **The id histogram has an authoritative replacement already in the store.**
   `check_widget_message_ids.py` re-derives all 264 `exact` rows of `widget-message-handlers.tsv`
   from the image. Keeping a second, wrong id source beside it *is* the defect.
3. **The rest of the tool is unaffected and worth keeping.** The 297-site / 267-handler census and
   the `--senders` scan do not decode dispatch at all; the defect cannot reach them.
4. **Immediate safety step, ahead of any retirement:** a pivot-only read must be classified
   **BOUNDED**, never `EXACT`. That moves 247 / 11 / 9 to **237 / 21 / 9** and costs nothing but a
   label — and §15c's own reason stands: *a confident under-report looks authoritative where an
   admitted bound does not.*

**Blast radius, measured rather than estimated.** Live carriers of the tool's id figure are two:
this contract's §15 table (already struck and restated on 2026-09-20) and
`_index/PARITY-STATUS.md`, which still carried `32 ids` unqualified and is corrected in the same
publish. `_index/RULES.md` carries a one-line tool registry entry with no figure;
`_index/AUDIT-LOG.md` entries are historical and are not restated. `the-widget-message-protocol.md`
uses the tool for the **site census and the sender scan**, neither of which the defect touches.
`SWE2-FRONTIER`'s inbox references it — routed, not edited here.

**Not done here, and named so it is not assumed:** the tool is still unfixed. This section schedules
the change and measures what it touches; applying it is a Tools edit with three peer work trees in
scope and belongs in its own package.

## 16. Parity plan

**Differential-testable now**, without a live process, in the pattern the three existing harnesses
use: map `002465F0`'s bytes at their real address, hand it a scratch object and a stub handler, and
compare the **whole header** against the reproduction formula in §12 — the same
*compare-resulting-memory* shape `quality_preset` proved.

**Not testable statically:** the destroy broadcast, which needs a real tree; and anything depending
on the generation global. Those wait on §13.

### 16. Teardown: two traversals with opposite caching, and the `+0x08` continuation — 2026-09-13 (OPUS)

`ASTRA-REQ-OPUS-WIDGET-TEARDOWN`. Every structural claim confirmed instruction by instruction, and
the state machine above corrected: **`00245020` does not free anything.**

#### `00245020` notifies; `002482E0` releases

`00245020` (132 B) detaches (`002448D0`), calls `00244700(self, 1)`, sends **`{18,0,0}`** to self, walks
the children with `002473B0`, then **tail-jumps to `002482E0`** — unless `+0x40 & 0x20` is set, in
which case it calls `002473F0(self, 0)`, clears bit 1, **sets bit 10** and returns with the object
alive. Both message sites — `002473C2` and `00245050` — `lea` the **same** constant `00915070`,
whose twelve bytes are `12 00 00 00 …` = `{18, 0, 0}`.

#### The caching discipline is opposite in the two traversals, and that is the reentrancy contract

```asm
002473B0  (notify)                          002482E0  (release)
  mov rbx, [rcx+0x18]   ; FIRST CHILD         mov rcx, [rcx+0x18]  ; first child
  call rax              ;   <- after caching  mov rbx, [rcx+0x20]  ; NEXT SIBLING first
  ...                                         call 0x2482E0        ;   <- then destroy it
  call 0x2473B0         ; child
  mov  rbx, [rbx+0x20]  ; NEXT SIBLING after
```

> **The notify traversal caches the first child *before* the handler runs and reads each next sibling
> *after*. The release traversal caches the next sibling *before* the recursion.** Both are forced,
> and for opposite reasons: a handler may relink the tree, so the notify walk must hold the entry
> point it already has — but it re-reads `+0x20` and will follow a handler's change to a sibling
> link. The release walk cannot re-read `+0x20` at all, because by then the child it would read from
> has been freed. **A reimplementation that uses one discipline for both traversals is wrong in one
> of them**, and the failure is a use-after-free in the release direction.

#### What `002482E0` does, in order

1. **children first**, recursively;
2. **unlink** from the parent: `prev->next = next` or `parent->firstChild = next`, `next->prev = prev`,
   then `dec dword [parent+0x30]` — the parent's child count;
3. **resources**: if `[+0x50] & 2`, walk the array at `[+0x60]`, call `0029F100` for entries whose
   `[+8] & 0x3C == 0x1C`, release the array through `0x3697F0`, null `[+0x60]`;
4. **`{24,0,0}` to self** — `002483A8` leas `00915040`, whose bytes are `18 00 00 00 …` = **24**;
5. **clear bit 10** of `+0x40` (`and 0xFFFFFBFF`) — the bit the deferred path set — and clear the low
   nibble of `+0x7C`; call `00228450`;
6. **`mov rbx, [rdi+8]`** — the continuation, read **while the object is still valid**;
7. `mov qword ptr [rdi], 0` — **the handler pointer is nulled**;
8. **bit 14 of `+0x40` decides**: clear → `0x3697F0(self)` frees it; set → `btr` bit 14,
   `byte [+0xA2] = 0`, **the object is returned to the pool, not freed**;
9. ~~`jmp rbx` — the continuation.~~ *Restated 2026-09-26 (OPUS), on `FABLE-REQ-OPUS-WIDGET-S16-CONTINUATION-JMP-RAX`:*
   `test rbx, rbx` (`002483F8`). **A null `+0x08` is legal and skipped**: `je 00248408` goes to `add rsp,0x20` / `pop rbx`
   / plain `ret`. Otherwise `mov rax, rbx` / `add rsp, 0x20` / `pop rbx` / **`jmp rax`** (`002483FD`–`00248405`). The
   jump is through `rax` because `pop rbx` first restores the caller's `rbx`.

> **Step 8 closes a two-sided contract this page already had half of.** `+0x40` bit 14 is documented
> above as *"this object came out of the fixed pool"*, set by the constructor from
> `(pooled & 1) << 14`. **The destructor reads that same bit to decide pool-return versus heap-free**
> — producer and consumer now both inspected, from opposite ends.

#### The `+0x08` ABI, which is what makes it dangerous to call

**`+0x08` is a tail continuation, not a destructor callback.**

- it is **read at step 6, before** the object is freed or pooled — the same caching discipline as the
  sibling link, and for the same reason;
- it is entered by ~~**`jmp rbx` after `add rsp,0x20` / `pop rbx`**~~ **`jmp rax` after `mov rax, rbx` /
  `add rsp,0x20` / `pop rbx`** (`002483FD`–`00248405`; *corrected 2026-09-26, OPUS: the jump register is `rax`, since
  `pop rbx` restores the caller's `rbx` first*) — the frame is already restored, so
  it runs on `002482E0`'s *caller's* frame and its `ret` returns to that caller;
- **a null `+0x08` is legal**: `002483F8 test rbx, rbx` / `je 00248408` skips it and `002482E0` returns with a plain
  `ret`;
- **it receives no defined arguments.** `rcx` last held the widget at `002483BB`, but `00228450`,
  and on the heap path `0x3697F0`, are called afterwards and `rcx` is volatile. **Nothing guarantees
  the widget pointer — or anything else — at entry.**

> **So a `+0x08` continuation must take no arguments and must not touch the widget.** By the time it
> runs, the object has already been freed or returned to the pool and its handler pointer is null.
> A reimplementation that passes `self` here, or a callback that reads a field, is a use-after-free
> that will usually appear to work.

**Not established here:** the load/area-controller hierarchy and which closing path it picks;
deferred-completion timing; the allocator's own effects; and `00247490`, the full child helper.
`00244DD0`'s conditional `{15}` and its absence of a direct `{18}` / `00245020` are ASTRA's reading
and are not re-derived on this pass.


### 17. The batch completion has three exits, and one of them calls a callback with no arguments

`ASTRA-REQ-OPUS-WIDGET-RETENTION`. `002495C0` runs when a batch member completes. Confirmed
instruction by instruction, and one finding is an ABI defect of the same shape as `+0x08` in §16.

```asm
002495DC  mov  rax, qword ptr [rbx+0x10]   ; the MEMBER's callback
002495E5  mov  rcx, rbx                    ; rcx = the member  <-- properly set
002495E8  call rax
002495EA  mov  rdi, qword ptr [rbx]        ; the batch
002495ED  inc  word ptr [rdi+0x1A]         ; <-- THE COUNT IS INCREMENTED AFTER THE CALLBACK
002495F1  test byte ptr [rdi], 2           ; sealed?
002495FA  cmp  ax, word ptr [rdi+0x18]     ; count == expected?
00249600  cmp  dword ptr [rdi+4], 0
00249604  je   0x24960B
00249606  call qword ptr [rdi+0x10]        ; *** CUSTOM batch callback ***
00249609  jmp  0x249637                    ; ... skipping 00249634
0024960B  mov  rcx, qword ptr [rdi+8]      ; STANDARD path: rcx = the object
00249612  mov  dword ptr [rsp+0x20], 0x10  ;               message 16
0024962D  lea  rdx, [rsp+0x20]             ;               rdx = the message
00249632  call rax                         ;               a properly formed (rcx, rdx) call
00249634  and  dword ptr [rdi], 0xFFFFFFFE ; clear the BATCH's active bit 0
00249637  and  dword ptr [rbx+0x20], 0xFFFFFFFE   ; clear the MEMBER's, on every path
```

> **⚠ The custom batch callback at `00249606` is called with no defined `rcx`.** The last write to
> `rcx` was `002495E5`, and `002495E8 call rax` sits between them — `rcx` is volatile under MS x64,
> so whatever the member callback left there is what the custom callback receives. **The standard
> path two instructions later does set `rcx` and `rdx` correctly**, which is what makes the omission
> visible as an omission rather than a convention.
>
> **So a custom batch callback must take no arguments**, exactly like the `+0x08` continuation in
> §16. Two independent callback slots in this engine are **bare continuations**, and in both a
> reimplementation that helpfully passes `self` is wrong.

**Two more properties, both confirmed:**

- **The count is incremented *after* the member callback runs** (`002495E8` then `002495ED`), so a
  member callback that inspects `[batch+0x1A]` sees the count **not yet including itself**.
- **The custom branch leaves the batch ACTIVE.** `00249606`/`00249609` jump to `0x249637` and skip
  `00249634`, so only the standard path clears the batch's bit 0. The member's own bit 0 is cleared
  on every path. **None of the three exits tests bit 0 before acting** — there is no guard against
  completing a batch that is already complete.

**Not established here:** later reclamation of a retained widget, the actual load/area ordering,
`00249660` / `00249670` materialisation and its allocation lifetime, and whether ordinary play
repeats the notification.

The four remaining ASTRA readings were re-derived from the shipped bodies 2026-09-15
(SWE2-CONTRACT); every one confirmed, with sharper detail:

- **`002445D0` (61 B)** sets the root flags only when `dword[arg] == 1` (`002445D0`):
  `or dword [root+0x40], 0x23` — bits 0, 1 and 5 — then `[arg+8]` → `root+0xC0`,
  `root+0x98` zeroed, and `+0x9C`/`+0x9E` written as words from `01E0C1D8`/`01E0C1DC`
  (`0x200`/`0x1C0`). Every path returns 0 (`0024460A`); a first dword other than 1
  touches nothing.
- **`00248220` (190 B)** appends the child at the tail of the parent's `+0x18` →
  `+0x20` list (`[tail+0x20] = child`, `[child+0x28] = prev`), sets
  `[child+0x10] = parent` and increments `parent+0x30`. The **propagation**: when the
  parent's `+0x40` bit 5 is set, the child's bit 5 is raised and `002463F0` walks the
  child's *existing* subtree applying `002418E0(node, 1)` — and `002418E0` is the
  14-byte leaf that rewrites `+0x40` bit 5 from `edx&1` (`and ~0x20; or (edx&1)<<5`).
  `002463F0` (`002463F0`–`00246446`, 87 B) is the pre-order recursive visitor:
  `call rdx` on the node with `edx = r8` (`0024640C`), then recurse over the
  `+0x18`-headed child chain linked by `+0x20` siblings (`00246429`/`0024642E`).
  Finally, `parent+0x40 & 1 && child+0x40 & 2` invokes
  `002473F0(child, 1)`, and `parent+0x40 |= 0x2000` runs on every path.
- **`00247490` (118 B)** is the gated recursive prune: each node must carry `+0x40`
  bit 1 **and** have `bit 0 != edx` before anything happens — either failure jumps
  straight to the epilogue (`002474AE`, `002474B7`), so a gated-out node takes its
  whole subtree with it. On a live node it flips bit 0 toward `edx`
  (`(flags ^ (flags ^ edx) & 1)` at `002474B9`–`002474C2`), invokes the node's own
  `[+0x00]` callback with `rdx = r8` when non-null, **then** recurses the
  `+0x18`/`+0x20` child chain (`002474E8`/`002474ED`).
- **`00582790` (197 B)** opens on `00249580` — **the 12-slot binding is that
  allocator**: a first-fit scan over `02090790`, twelve `0x20`-stride records bounded
  at `edx < 0xC`, free iff `[slot] bit 0` is clear; on a hit it zeroes
  `+0x00/+0x08/+0x10/+0x18`, raises bit 0 and stores the arg at `+0x08`. `00582790`
  then binds `rbx+0x100` and `rbx+0x108` through `00393460`/`003933F0` (named
  resources at `00D23D80`/`00D23D98`), and — only while `[rbx+0xC1] == 0` — binds
  `+0x110` and `+0x118` through two `00249210` calls (`edx=7`, ids `0x2C`/`0x2D`,
  counts `3`/`2`, `[result+8]` stored),
  writes `00393600(2)` to `+0x120`, and tails into `00249410` — the batch seal:
  `or [rcx], 2`, then count-vs-expected at `+0x18`/`+0x1A` gates the `+0x10`
  custom callback or the standard `[[rcx+8]]` message-`0x10` call — the same
  shape §17's `002495C0` arms show.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

Uncited residuals whose documented neighbour is this contract, read at call-signature level:

| function | size | role |
|---|---:|---|
| `0023ED80` | 466 | widget-task constructor: `[rcx+0xC0]`/`[rsi+0xC0..0xE8]` record fields, indexed record fetch `00243260`, then factory `00244F50` (same factory as the screen-fade task object) + `00244960`; small jump table present (not decoded) |
| `002D66D0` | 616 | already cited as the `AutoWindow…` widget entry in [the layout-parameter page](../Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md); here: `[rdi+0x40]`/`[+0xC0..0xCC]` + `[rbx+0x10]`/`+0x18`, calls `00247570`/`002475D0`/`00247930` (widget helpers), `002F9860` ×3, `00364980`/`00365B30`, `002B4090`, `002D8B00`, `002CC8D0`; jump table present (not decoded) |
| `003F8790` | 492 | widget teardown sibling on `[rcx+0xE0]`: `00244F00`, `002468A0`, `00246AD0`, `00244960`, `003F8640` — same helper set as the contract's destroy paths |
| `003FAF10` | 1226 | two-part layout calc on `[rdi+0xC2]`/`[+0xC4]`/`[+0x38]` and `[rbx+0x58]`/`+0x5A`: `0035D480` context getter, `003FB8F0` ×2, `002D8D10` ×2 + `00861F74` ×2 (math pair), `00296F50`, `0029F6E0`, `00244F00`, `002432B0`; `0035D480` first at [`003FAFC1`](../../_index/ADDRESS-INDEX.md), `002D8D10` at [`003FB182`](../../_index/ADDRESS-INDEX.md) |
| `00566680` | 997 | **already placed** — item-sort widget procedure, decoded on [the shared-dialog page](../Shared-Dialogs/the-shared-dialog-widgets.md) (`246391ed`) |
| `0056F810` | 621 | **already placed** — menu-list widget procedure, same page (`246391ed`) |

Not claimed: `0023ED80`'s and `002D66D0`'s jump tables are not decoded; roles are head+signature
reads.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Presentation — MECHANICAL (SWE2-CONTRACT 2026-09-15).** 56 edges measured; all are Presentation
bodies *calling* helpers this page cites — ~35 are the 27-byte frame helper `001EDDA0`'s
Presentation fan-in (with `00314960`), plus `002D2DB0` `Presentation.DebugCapture.ScreenCapture`
callers of `001EDEC0`/`00243260`/`002D8D10`. Shared-helper populations, not a second owner of the
widget object.

## Interior citation — frontier hub `002432B0` (2026-09-17, SWE2-EC7)

`002432B0` — the typed-list decoder this contract's layout bodies call (108 callers per the
typed-list page's census). Interior verified: [`002432C8`](../../_index/ADDRESS-INDEX.md) is
`mov ecx, dword ptr [rdx + 0x20]` — loading the outer record table out of the owner record,
matching the documented contract `(out, obj, index, ctx)`. The body walks `obj`'s list at
`[rdx+0x20]` via `0020E600`-resolved pointers, applies the 20-byte-record bit-field pack seen in
the typed-list document, and dispatches per-type constructors through the six-case jump table at
`[r9 + rax*4 + 0x123514]` over `0029F4C0`/`0029FEB0`/`0029ED40`/`0029F130`/`0029F930`/`0029ECB0`.
64 frontier callers.

NOT claimed here: the page's own per-type semantics — those live on the typed-list document,
which owns the full walk.

## Interior citation — frontier hub `00243260` (2026-09-18, SWE2-EC7)

`00243260` — 75 B, 8 A-measured callers; the indexed 4-word fetch beside `002432B0`'s
materialiser. Interior verified: `word(rcx[0] >> 2)` is the element count — index `dx` at or
above it returns 0 (`0024326F`); otherwise `[+0x10]` is the record pointer table, element
`[rax + dx*8]`'s words `+0xC`/`+0xE`/`+0x10`/`+0x12` copy to the `r8` out-record at
[`00243282`](../../_index/ADDRESS-INDEX.md)–`002432A0`, returning 1. Bounded indexed read into an 8-byte
out-struct — the query-record getter the materialiser's callers pair with it.


## Interior citation — frontier hub `00247730` (2026-09-18, SWE2-EC7)

`00247730` — 78 B, 7 A-measured callers; the subtree flag propagation over the `+0x18`/`+0x20`
child chain this contract already documents. Interior verified: null-guarded, it clears
`[rcx+0x40] & ~0x01000000` (`0024773A`), then ORs `(edx & 1) << 24` back in
([`00247751`/`00247754`](../../_index/ADDRESS-INDEX.md)) — arg bit 0 becomes the widget's bit-24
flag — and recurses on itself for each child: `rbx = [rcx+0x18]`, loop body `call 00247730`
with the same `edx` at [`00247765`](../../_index/ADDRESS-INDEX.md), advance `rbx = [rbx+0x20]`.
One bit, pushed through a whole subtree.

### Interior citation — frontier hub 0029F6E0 (2026-09-18, SWE2-EC7)

**0029F6E0** (586 B, 4 A-measured callers) — the fixed-width decimal record formatter the `003FAF10` layout calc reaches. Flag-driven digit emission: computes `10^edx` via a `r10*5*2` loop, then per digit writes the two-word record via the ring writer; on `r8 < 0` the arm marks slots `or [rax], 1` across `0x40`-stride records (up to `r9d` fills ×4) and stamps `word = 10` / `= 9` — the pad rows the layout's decimal column emits for negative values. In-scope: `10^n` loop head [`0029F780`](../../_index/ADDRESS-INDEX.md); slot-mark arm [`0029F7B0`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**ActorEntity — this page is the CALLER.** `00273270` on this page calls
**`ActorHandle_ResolveRegistryEntryByPackedId`** (`003588B0`), owned by ActorEntity, at
**`00273291`**. Read from the shipping bytes: `00273270` takes a packed id in `ecx`, skips the call
entirely when it is zero (`0027328D`–`0027328F`), and abandons the whole body when the resolve
returns null (`00273296`–`00273299`) — so the widget path treats an unresolvable handle as "nothing
to draw" rather than as an error.

**The crossing is a consultation, not ownership: this page resolves an actor handle and owns nothing
in ActorEntity.** `003588B0` is the same resolver `EXP-091` executes as `idres`, whose own gates
(nibble `> 5` → `-1`, then the `00263FF0` table and the idxt `mark` / `bit10` / `list` / `bound` /
version `+0x16` checks) are measured there rather than here.

## SWE2-EC7-24 update (2026-09-18) — `00368A50` global pair publish

`00368A50` (15 B) stores `rcx` and `rdx` into `022CBE90`/`022CBE98` — the
two-qword publish the widget state machine reads back on its next pass.
Interior anchor `00368A57` (the second store).

## SWE2-EC7-26 update (2026-09-18) — `002468A0` widget state-commit + `00365B30` tail wrapper

`002468A0` (364 B) is the cookie-checked widget state-commit behind the
`002D66D0` AutoWindow entry: with `byte[+0x80] & 0xE` clear and
`word[+0x98] == edx`, `word[+0x9A] == r8d` both matching, it runs the
`[rbx]` vcall twice (stack kind 0 then 1) and returns 0. On mismatch it
commits: `+0x80 |= 1`, `&= 0xFFFFC3FF`, `|= (r9 & 0xF) << 0xA`; the
deltas land in `word[+0x84]`/`[+0x86]`/`[+0x8C]`/`[+0x8E]`; `+0x94`
takes `dword[0208F570]`; `+0x90` is computed from the stack arg by
`imul 0x3C` + the `0x10624DD3` signed reciprocal; `+0xB8` defaults to
1.0f and becomes `1.0 / 00229E70()` when `00229DF0` != 0 and
`00229EA0` == 2. Interior anchor `0024694E` (the `0xFFFFC3FF` mask).

`00365B30` (29 B) spills `r8`/`r9`, points `r9` at `[rsp + 0x48]` as the
out slot, and tail-calls `00365B50` — the thin wrapper `002D66D0` runs
beside `00364980`. Interior anchor `00365B43` (the call).

## SWE2-EC7-27 update (2026-09-18) — `00229E70` rate lazy-initializer

`00229E70` (37 B) reads `float[01E02820]`: if it is still zero it writes
1.0f back and returns it, otherwise returns the stored rate — the
lazy-default source `002468A0`'s `+0xB8` divides into when the widget
commit path takes the `00229DF0`/`00229EA0`-gated branch. Interior
anchor `00229E88` (the default store).

## SWE2-EC7-28 update (2026-09-18) — `002969F0` two-pointer store

`002969F0` (20 B) is the `+0xB20`/`+0xB30` writer the "-5" offset row
names in the `00368A50`/`00279C48` chain: null-guards `rcx`, stores
`rdx` at `+0xB20` and `r8` at `+0xB30` — the pair-commit sibling of
`002969E0`'s single `+0xB28` store. Interior anchor `002969F5` (the
`+0xB20` store).

## SWE2-EC7-36 update (2026-09-19) - `00365B50`

`00365B50` (628 B) is a widget-object body - `00365E50`/`00861EBA`/`00808C40`. Interior anchor `00365D10` (an `00861EBA` call).

## SWE2-EC7-38 update (2026-09-19) - `003F8790`

`003F8790` (492 B) is a widget-object body - `01F44830`, `00244F00`/`002468A0`/`003F8640`/`00246AD0`/`00244960`/`00808C40`. Interior anchor `003F8835` (a `00244F00` call).

## SWE2-EC7-40 update (2026-09-19) - `003FB8F0`

`003FB8F0` (392 B) is a widget-object body - `01F44830`, `00861F0E` pair plus `002752E0`/`00808C40`. Interior anchor `003FB9AB` (an `00861F0E` call).

## SWE2-EC7-41 update (2026-09-19) - `003F8640`

`003F8640` (335 B) is a widget body - `009155D8`/`00D11D50`/`01F44830`, `00244F00`/`003F8490`/`00245000`/`002F9860` pair/`0029CD00`/`00808C40`. Interior anchor `003F8674` (a `00244F00` call).

## SWE2-EC7-44 update (2026-09-19) - `002985D0`

`002985D0` (266 B) is the `r8`-passed proc body of the fourteen-slot table - `00244960`/`00245000`/`00245020`/`00246AC0`/`00273A20`/`00296960`/`0035BAD0`. Interior anchor `002985FE` (a `00244960` call).

## SWE2-EC7-44 update (2026-09-19) - `0029F930`

`0029F930` (264 B) is a body - `0020E600`/`002432B0`/`00244960`/`002D14E0`. Interior anchor `0029F95D` (a `0020E600` call).

## SWE2-EC7-51 update (2026-09-19) - `0029F4C0`

`0029F4C0` (177 B) is a body - `002A0060` single call. Interior anchor `0029F4DA` (the `002A0060` call).

## SWE2-EC7-51 update (2026-09-19) - `0029FEB0`

`0029FEB0` (174 B) is a body - `0020E620`/`002F9920`. Interior anchor `0029FECA` (a `0020E620` call).

## SWE2-EC7-53 update (2026-09-19) - `00365E50`

`00365E50` (378 B) is a call-free `0x66666667`-magic `/5` countdown loop over `edx` (`00365B50` calls it). Interior anchor `00365E88` (the `imul r10d` magic step).


## SWE2-EC7-102 update (2026-09-20) - `00290490` measured

`00290490` (28 B) is the `+0x10F78` slot test
`002778C0` and `0027E3E0` call: a null
`[[0209BE80] + 0x10F78]` returns `-1`; otherwise the
slot forwards through a `00296580` tail - the
presence-gated widget call the protocol arms
share.
Interior anchor `00290497` (the slot read).

## SWE2-EC7-103 update (2026-09-20) - `0027BB70` measured

`0027BB70` (154 B) is the mask-filtered collect
`0027D740` and `0027E050` call: `rbp = edx`
`0x8`-stride entries at `rcx + 0x50` are scanned,
`r14d == 1` adds a `00273710` gate on entries with
`byte[+4]` bit 1 clear, every surviving entry is
masked by `002647E0` against `r12d`, and matches
are copied forward with `edi` counted into
`[r15 + 0x40]` - the filtered list-compaction the
widget object exposes.
Interior anchor `0027BBC0` (the `002647E0`
call).

## SWE2-EC7-115 update (2026-09-21) - `005670F0` measured

`005670F0` (145 B) is the
two-record visibility bit
`00567690` tails into and
`005641F0`/`00566680` also
run: when `edx` is nonzero
AND `byte[rax+0x150] > 1`
(`rax` = `qword[rcx+0x10]`),
it ORs bit 0 into
`dword[+8]` of two records -
`[[r8+0x60]][word[rcx+0xDA]*8]`
and
`[[r8+0x60]][word[r8+0xD8]*8]`;
otherwise it ANDs the same
bit off both. The `edx`
parameter is the show/hide
switch `00567690` derives
from `param != 0`.
Interior anchor `00567129`
(the first `+8` bit set).

`00565CD0` (249 B) is the callback registrar `00566680` (the item-sort widget, already placed on the shared-dialog page) runs: `00564380()` indexes `00D23960`'s word pairs, `00252F40(tbl.w0)` -> `[+4]` -> `0020E600` resolves the object, and `00252FA0(word[rbx])` answering <= 1 returns -1; otherwise the `(edi, esi)` pair picks one of five handlers — `esi` == 0 -> `002CFFE0`, `esi` == 1 dispatches `edi` {0,3}->`002CFD30` / 1->`002CFEE0` / 2->`002D0100`, `esi` == 2 -> `002D0200` — and `00249CE0(&rec, obj, 2, fn)` registers the pick.

Interior anchor `00565D99` (function `00565CD0`).

`005641F0` (259 B) is the `[+0xE0]`-record select `005651E0` runs — the sibling of `005687F0` on the sibling record: `[+0xE0]` null returns 1; `00368240` answering 2 writes `[+0xD8]+0xFD` = 0xFF and returns 1; else `[+0xD8]` takes `+0xE0` = `di` with `+0xE4` |= 0x40000 | 4 | 0x20000, a live `[+0xC8]` runs `005670F0([+0xC8]+0xC0, 0)`, `00295D50(0)` fires, the `(+0xF2·+0xEC) + +0xEE + +0xED` extent lands in `+0x178` with `di` in `+0x17A`/`+0x17C`, `00368A60(4)` and `00368830(0)` run, `+0x181` = 1, and 0 returns.

Interior anchor `005642CC` (function `005641F0`).

`0029F130` (841 B) is the percentage-bar builder the typed list's slot 7 names: `or [rcx+0x20], 0x2000000` flags the node, `word[rdi+0xC]` feeds `002A0060` for the atlas object at `[rbx+0x28]`, `word[rdi+0xE]` keys the `word[r9+rax*2+0x14]` metric table, and `0020E600`/`0024A5F0` x2/`0024A610` finish the two-strip emit - the bar widget's measured body.

Interior anchor `0029F161` (function `0029F130`).

`002727F0` (426 B) is the record clone `0027D740` calls: `00808F10` probes a `0x1080` stack frame, `dword[r8]` then five `movups`/`movsd` copy the `0x40`-byte record into `rcx`, and `00861EBA`/`00808C40` handle the tail - the widget's big-struct copy.

Interior anchor `002727FA` (function `002727F0`).

`002729A0` (411 B) is the broadcast `0027D740` calls: `00808F10` probes `0x11B0`, `dword[rcx+0x40] > 0` gates, `movups` copies `rbx+8`/`+0x18`/`+0x28` into the frame with `rbx+0x50` as source, and `00861EBA`/`0035BAD0`/`002E9D10`/`00249110`/`002748E0` run the emit - the widget's counted broadcast.

Interior anchor `002729A7` (function `002729A0`).

`00249110` (102 B) is the fixed-point re-quantizer `002729A0`'s broadcast calls (also `00272B40`/`0035C160`/`0035DCC0`): `0024AD00` resolves `rcx`, then a `r9d`-counted loop over `rbx` (0x10 stride) rewrites `dword[0]` and `dword[+4]` of each element as `(v - 0x8000) >> 4 + (01E0C1D8 >> 1)` / `(01E0C1DC >> 1)` - the re-centering pass applied to the emitted coordinate array.

Interior anchor `00249123` (function `00249110`).

`002748E0` (698 B) is the sorter `002729A0`/`00272B40` call: `ecx - 1` seeds `r14d`, `esi`/`edi` walk the range while a dword stack at `[rsp+rdi*4]`/`[+0x80]` pushes and pops pivot pairs - partitions longer than `0xA` recurse through the stack, shorter ranges pop it - the widget's iterative quicksort over the broadcast order.

Interior anchor `00274B82` (function `002748E0`).

`00298130` (276 B) is the quad-list alpha ramp the message-30 handler `0029A0A0` runs on the widget: `byte[rcx+0xD8] & 0x80` picks the direction - `word[+0x112]` rises `0x20` a tick toward `0x100` or falls `0x20` toward 0 - and `r8d = (0x100 - level) >> 1` becomes the scale; three linked vertex runs under `[rcx+0x60]` (offsets `+0`, `+8`, `+0x10`) each rewrite four 4-byte vertices, copying the source dword from `[vertex + (datalen - 0x17)]` and rescaling the alpha byte `x r8d >> 7` - the fade the widget drives per message.

Interior anchor `002981B0` (function `00298130`).

## Cross-subsystem neighbours — SWE2-EC7-171

**CoreRuntimeScheduling — CLIENT (SWE2-EC7-171, 1 edge).** `0029A0A0` — the message-30 handler whose `00298130` alpha ramp this page gains — calls `001EDEC0`, the shared resolver `002D2DB0`/`00241D40`/`0057FE80` also reach. A measured call, not shared ownership: the handler borrows the layer's name table for one lookup per dispatch.

`00241A70` (207 B) is the mode-dispatched notify `00241D40` runs: `[+0x3BE] == 1`/`2` sends the 16-byte constant block `0xC | 0x8101`/`0x8102` through `[+0xD0]`'s first vtable slot when the callback is bound; `[+0x3BE] == 0` instead checks `+0x3C4 & 0x800` to `00247510`s `0x8104` on `[+0xD0]`, then always `002D4650`s `[+0xC8]` with `[+0xC0]` - returns 1 only on the vtable path

Interior anchor `00241AB3` (function `00241A70`).

`00241B40` (167 B) is the availability emit `00241D40` runs on the widget's `+0xC8` object: `([+0xF2] + [+0xF4]) * byte[+0xEC] + sbyte[+0xEE] + sbyte[+0xED]` nonzero selects `0x8101` over `0x8100`, and the code rides a `{0xC, code, 0}` frame into the `+0xD0` object's vtable slot 0 before the stack-cookie check returns 1

Interior anchor `00241BCE` (function `00241B40`).

`002C19E0` (152 B) is the gated emit `002C1A80` calls on the `[0209AC30]+0x118` object: skipped when `dword[+0x7C] & 0xF0` shifted to the sign bits is positive; otherwise it `00246AD0`s the `0208EA28` root with `rbx` and a stack template `{0x5000000050000000, 0x5000000050000000}`, resolves `word[[rbx+0x48]+2]` through `002CCCF0`, and when `dword[+0x40] & 0x1000000` and the result is non-null runs `00247730(rax, 1)` - cookie-protected (`00808C40`).

Interior anchor `002C1A33` (function `002C19E0`).
