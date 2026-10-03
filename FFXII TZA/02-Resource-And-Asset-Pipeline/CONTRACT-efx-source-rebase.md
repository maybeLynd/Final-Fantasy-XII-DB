---
contract: republish an EFX source base and repair its selected lookup and instance references
category: 02-Resource-And-Asset-Pipeline
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 02-Resource-And-Asset-Pipeline/authored-reference-lifetime-evidence.md
entries: ["003B3480", "0024D970", "0024D940", "003A8FF0", "003AB7F0", "0036B130"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 70 addresses cited - 2 data, 22 entry, 46 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-23
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-13
  last_pass_state: opus-falsification-pass-1-2026-09-13
  crossref_clean: false
  reopened_count: 0

external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# Contract — the EFX source rebase, and the ±2 GiB range it is correct over

The source block an EFX caller reads from can move. The driver repairs **selected consumer
references**, using one delta over particular lists/tables. It does not rewrite every pointer
field: context +870/+878 run origins survive the reviewed refresh unchanged. This contract states the mechanism, its consumers, and — the part that matters — **the exact
range of movement over which it is correct**, which is narrower than it looks.

Raised by ASTRA from isolated original-code execution (`ASTRA-REQ-OPUS-EFX-REBASE`, section 15 of
[the authored-reference lifetime evidence](authored-reference-lifetime-evidence.md)) and re-derived
here from the shipping bodies instruction by instruction.

## 1. The mechanism

```asm
003B3480                                    ; the driver
003B34F5  movsxd rcx, dword ptr [rbx+0x860] ; sign-extend the tagged source handle
003B34FC  call   0x3AB7F0                   ; resolve it -> a 64-bit base, or 0
003B3501  movsxd rsi, dword ptr [rbx+0x864] ; sign-extend the signed source offset
003B3508  add    rsi, rax                   ; newBase = sext(+0x864) + resolved
003B350B  cmp    rsi, qword ptr [rbx+0x858] ; against the stored FULL 64-bit base
003B3512  je     ...                        ; unchanged -> nothing to repair
003B351A  call   0x24D970                   ; rebase the caller template
003B3524  cmp    rsi, qword ptr [rdi+0x390] ; a second object with its own base field
003B3533  call   0x24D940                   ; rebase that one too
```

**The object is identified by field fingerprint, not by a matching offset.** `003B3480` touches
`+0x18`, `+0x38`, `+0x840`, `+0x848`, `+0x850`, `+0x858`, `+0x860` and `+0x864` on `rbx`, which is
the declared [`EfxCallerTemplate`](../_types/types.tsv) layout — `resolvedSourceBase` at `+0x858`
and the two source dwords at `+0x860`/`+0x864`.

### What `+0x860` and `+0x864` actually are

The type row already said these are **two independent dwords that must not be modelled as the halves
of one 64-bit pointer**. This contract says what they are instead:

| field | role |
|---|---|
| `+0x860` | the **tagged source handle**, sign-extended at `003B34F5` and passed to the resolver |
| `+0x864` | a **signed 32-bit offset**, sign-extended at `003B3501` and *added to the resolver's result* |

**Both are signed.** ASTRA's report named the sign-extension at `+0x860`; `+0x864` is sign-extended
by the very next instruction and is equally load-bearing, because it is what turns a resolved block
base into this caller's source base.

## 2. The resolver, and a 32-bit guard on a 64-bit pointer

```asm
0036B130  ; handle -> base, 41 bytes
  test ecx,ecx / je            ; 0 -> 0
  test cl,3    / je            ; the low 2 bits are a TAG; untagged -> 0
  cmp  ecx,0x100000 / jb       ; -> 0
  mov  eax,ecx                 ; zero-extend; the handle addresses below 4 GiB
  and  rax,0xFFFFFFFC          ; strip the tag
  mov  rax,[rax+8]             ; a FULL 64-bit base
  add  rax,0x40

003AB7F0  ; the wrapper, 99 bytes
  test dl,3 ... setne cl       ; untagged -> return the input unchanged (003AB846)
  mov  ecx,edx                 ; truncate to the 32-bit handle -- by design, it IS 32-bit
  call 0x36B130
  movsxd rcx,eax               ; <-- sign-extend only the LOW 32 BITS of a 64-bit pointer
  cmp  rcx,0x40
  cmovbe rax,rbx               ; rbx = 0
```

**The full 64-bit result survives unless `unsigned(sext(low32(result))) <= 0x40`** — which is exactly
what ASTRA asked to have confirmed, and it is confirmed, including that `cmovbe` makes the comparison
**unsigned** while `movsxd` makes the value **signed**.

> **⚠ The guard tests 32 bits of a 64-bit pointer.** Its evident intent is to catch a null load:
> `[rax+8] == 0` makes the result `0x40`, and `<= 0x40` rejects it. But it reads only the low half,
> so it **also rejects a valid high base** whenever
> `low32([rax+8]) == 0` or `low32([rax+8]) >= 0xFFFFFFC0` — that is, a block allocated at or just
> below a 4 GiB boundary. The failure is silent: the caller receives 0 and treats the source as
> absent. **This is a hazard characterised from the instructions, not an observed defect**; no
> capture in evidence has hit it.

### The tag selects source representation; it is not the context borrow bit

Four bodies share one prologue — `test cl,3` / `cmp ecx,0x100000` / `and rax,0xFFFFFFFC` /
`mov rax,[rax+8]` — so the handle ABI is common: **a handle is a table-slot address with a 2-bit
tag; an untagged value is a raw pointer the table knows nothing about.** The tag selects the slot representation. The tree-membership pair is a no-op on raw pointers,
but actual raw release `003AB7C0` -> `003697F0` is not. This tag is distinct from context+2
mask4, which decides parser borrowing:

| body | after loading `[slot+8]` | on an **untagged** input |
|---|---|---|
| `0036A000` | `movzx eax, word [rbx+0x1C]` vs `cmp word [rdx+6], ax` — **generation check**, then **removes the entry from the arena tree** | — |
| `0036D170` | the same generation check, then **adds the entry to the arena tree** | — |
| `003AB880` | tail-calls `0036A000` | **returns the input unchanged** |
| `003AB940` | tail-calls `0036D170` | **returns with no call and no write** |
| **`0036B130`** | **nothing — `add rax, 0x40` and return** | — |

> **Corrected same day.** An earlier revision of this table described `0036D170`'s
> `test byte [rbx+0x15], 2` as part of the generation validation. **It is not** — that bit is
> *tree membership*, and the pair is an add/remove, not two releases. See
> [`CONTRACT-resource-entry-tree.md`](CONTRACT-resource-entry-tree.md). The untagged column is
> unaffected, and so is everything §3 and §4 conclude.

> **⚠ `0036B130`, the resolver this rebase depends on, performs no generation check.** Its three
> siblings compare the slot's `+6` word against the object's `+0x1C` before trusting the pointer;
> `0036B130` loads `[slot+8]` and returns it. **A stale handle therefore resolves to whatever the
> slot now points at**, and §2's guard will not catch it — that guard only rejects values whose low
> 32 bits are `<= 0x40`. This is the precise content of ASTRA's *"`36B130` skips active/word
> checks"*, and it is a property of the shipping code, not an observed failure.

## 3. The repair, and the range it is correct over

```asm
0024D970  ; rebase the template
  mov ebx, edx                       ; low32 of the NEW base
  sub ebx, dword ptr [rcx+0x858]     ; minus low32 of the OLD base  -> a 32-BIT delta
  call 3AA3D0 / 3A9BA0 / 3A9860      ; three repair walks, each given ecx = that delta
  mov qword ptr [rdi+0x858], rsi     ; publish the FULL 64-bit new base

0024D940  ; the same shape for the second object, base field +0x390, repair 3A8FF0

003A8FF0  ; a repair walk
  movsxd r9, ecx                     ; sign-extend the 32-bit delta to 64 bits
  add qword ptr [r8+0x108], r9       ; then add it to every stored pointer, 64-bit
  add rcx, r9 ; mov [r8+0x100], rcx
  add qword ptr [rax+0x18], r9
  add rdx, r9 ; mov [rax+0x20], rdx  ; inner list via [rax+0x30], outer via [r8+8]
```

**All four repair walks sign-extend, decoded rather than assumed:** `3A8FF0` `movsxd r9, ecx`;
`3A9BA0` `movsxd rsi, ecx`; `3A9860` `movsxd rsi, ecx`; and `3AA3D0`, which applies nothing itself —
it walks a list dispatching on a type byte at `+0x0E` (`0x52`, `0x56`) and forwards the 32-bit delta
in `edx` to `00501420` (`movsxd rax, edx`) and `00503F10` (`movsxd rdi, edx`). So the bound below is
uniform across every path, not a property of the one walk that was easiest to read.

The delta is computed in 32 bits and applied as `sext32`. Because
`low32(new) − low32(old) == low32(new − old)` in two's complement, that is **exact if and only if the
true delta fits in a signed 32-bit range**:

> ### Exact signed-delta range: −2^31 <= newBase − oldBase <= 2^31−1
>
> Outside that inclusive signed range the published base is still **correct** — it is stored as a full `qword` — while every
> repaired pointer is shifted by the **wrong** amount. The two disagree, and nothing detects it.
>
> **This tightens ASTRA's finding rather than merely confirming it.** ASTRA exercised a *controlled
> 4 GiB difference* and observed the base published high while the tables still referenced the old
> location. At exactly 4 GiB the 32-bit delta is **zero**, so the pointers are not moved at all —
> the most visible form of the failure. But the failure does not begin at 4 GiB: **it begins at
> 2 GiB**, where the delta's sign flips and pointers move by `delta − 2³²`. A 3 GiB move is already
> broken and looks less obviously so.

## 4. A second, independent 32-bit narrowing — the offset round-trip

One repair does not store a pointer at all. `00503F10` repairs a **32-bit offset field** at `+0x10`
by converting out, adding the delta, and converting back:

```asm
00503F1D  movsxd rdi, edx              ; the delta
00503F20  mov    ecx, [rcx+0x10]       ; the stored 32-bit OFFSET
00503F23  call   0x20E600              ; offset -> pointer
00503F35  lea    rcx, [rdi + rax]      ; + delta
00503F39  call   0x20E620              ; pointer -> offset
00503F3E  mov    dword ptr [rbx+0x10], eax   ; stored back as 32 bits
```

and the two converters are **not symmetric in width**:

```asm
0020E600  mov eax, ecx                 ; ZERO-extend the offset
0020E602  add rax, qword ptr [01F83530]  ; + arena base, read as a QWORD   -> 64-bit pointer
0020E620  sub ecx, dword ptr [01F83530]  ; - arena base, read as a DWORD   -> 32-bit, in 32 bits
0020E626  mov eax, ecx
```

> **`0020E620` computes the offset entirely in 32 bits, and reads the arena base as a `dword` where
> its inverse reads a `qword`.** The round trip therefore preserves `low32(offset + delta)` and
> nothing more. **So a second constraint sits alongside the ±2 GiB one: every offset-form pointer
> must stay inside `[arenaBase, arenaBase + 4 GiB)`.** ~~Past that~~ Above that window the stored offset wraps and later
> resolves to the wrong address ~~*inside* the arena~~ back inside the window — silently, and without the delta being wrong; below the base it decodes `2^32` too high, outside the window *(corrected 2026-10-02, OPUS: `0020E620` keeps 32 bits and `0020E600+0x2` adds the qword base to the zero-extended offset, so a pointer below the base comes back as `p + 2^32`; the entry-tree contract's 2026-09-15 correction, EXP-083)*.
>
> This is the concrete instance of the engine-wide question
> [the registry page](authored-data-table-registry.md) raised as **BW-2**: whether the allocator
> guarantees a sub-4 GiB arena. **Here it is not a curiosity about one instruction — it is a
> correctness precondition of the rebase.**

## 5. The same narrowing appears as a `memcpy` length

The EFX parser `003EDAD0` computes its copy size the same way the rebase computes its delta — as a
**32-bit pointer difference, sign-extended**:

```asm
003EE111  sub    ebx, r12d          ; low32(end) - low32(source), 32-bit
003EE114  sub    ebx, 4
...
003EE04C  mov    eax, ebx
003EE04E  cdq                       ; the signed round-to-16 idiom:
003EE04F  and    edx, 0xF           ;   (x + (x<0 ? 15 : 0)) & ~15
003EE052  add    eax, edx
003EE05E  and    eax, 0xFFFFFFF0
003EE061  movsxd r8, eax            ; <-- the memcpy LENGTH, sign-extended
003EE064  call   0x861EBA           ; rcx = [ctx+0x878], rdx = r12
```

> **A wrong delta repairs a pointer badly; a wrong length is a `memcpy` size.** The ±2 GiB bound of
> §3 therefore is not confined to the rebase — it is a property of how this subsystem computes
> *every* derived quantity. Note also that the length is rounded **down** to a multiple of 16 for a
> positive value, so a payload is copied in whole 16-byte units and any remainder is not copied by
> this call.

### `+0x002` bit 2 again, now choosing copy versus borrow

The same bit that gates publication (§1) and withholds the chunk release chooses, at parse time,
whether the context **owns** its payload or **borrows** it:

```asm
003EE117  test byte ptr [rax+2], 4   ; rax = [02F97340], the published context
003EE11B  jne  0x3EE16A
003EE11D  mov  edx, 0xA              ; CLEAR -> allocate (36C1D0/36A100) and memcpy: OWNS a copy
...
003EE171  mov  qword ptr [rax+0x870], r12   ; SET -> store the caller's pointer: BORROWS it
```

**That completes the bit's meaning and makes the other two uses follow from it.** Set means *this
context borrows its payload from someone else*, so of course it must not free the chunk
(`003A9613`), and of course it is the shared/published one (`003B348A`). **One bit, three sites, one
consistent ownership rule** — each verified independently before being joined.

> **⚠ A naming trap worth stating, because it manufactures a contradiction that is not there.**
> `A00` denotes two different things in this subsystem. It is a **handler id** — `003EE069
> mov r11d, 0xA00`, the site that uses chunk **`+0x878`** — and it is also a **table byte size**:
> teardown `003A9600` clears chunk **`+0x870`** while walking a `0xA00`-byte table (320 slots).
> So *"A00 pairs with `+0x878`"* and *"`0xA00` pairs with `+0x870`"* are **both correct**. The
> pairing by handler is `800 → +0x870` and `A00 → +0x878`; the teardown tables are `+0x870 → 0xA00`
> (319 walked) and `+0x878 → 0x1800` (767 walked).

## 6. What this contract does not establish

- ~~**The second object's type.**~~ **Resolved 2026-09-20 — it is the effect container.** The
  fingerprint, taken the same way `rbx`'s was: `003B3480` has **one** call site in `.text`
  (`003B3C4D`, inside `003B3C00(id, index)`), which loads `rdi` from
  `02EBD480 + (id & 0x3F) * 0x38 + 0x10` — the character-bound container handle table
  ([the six VFX display layers](../17-Presentation-Rendering/Effect-File-Formats/the-six-vfx-display-layers.md)
  names `02EBD480` as the table a render record reaches its effect container through). `0024ED80`,
  which `003B3480` runs on `rdx` first, is the same doc's "make a container current" body: it
  publishes `[obj+0x340]`'s template fields to the EFX globals and the container's own `+0x120` /
  `+0x130` / `+0x1B8` (`+0x1B8` is the `003A8FF0` repair-walk list head `02EBEF88`). The rest of the
  fingerprint is the group-draw node's own fields: `+0x348` next, `+0x364` / `+0x36A` / `+0x380` /
  `+0x39B` / `+0x3A8` gates, `+0` kind byte, `+4` the dword indexing the handle table. So `+0x390`
  is **the container's own 64-bit source base**, compared and repaired separately from its
  context's `+0x858`; neither the comparisons nor their publications are an atomic pair.
  The `CharacterRenderObject +0x390` offset match is disproven semantically — that row is
  `auxVec36Begin`, a `0x24`-element vector begin freed by the destructor in element units, not a
  rebase base. `003B3480`'s own `rcx` is `[container+0x340]`, the heap `EfxCallerTemplate`
  context — consistent with `rbx`'s fingerprint. `003B3C00(id, index)` bounds `index` to
  `0..0xA` inclusive: negative values and `0xB` are rejected. Index zero returns 1
  without refresh or child start; indices 1..10 refresh first and then call `0024FE70`. A rejected
  child start may therefore follow a completed source repair. These distinctions are executed by SECTION-07.
- **Actual movement and refresh are different operations (SECTION-07 correction).** The original
  arena producer is `0036A2A0`, selected by `0036AAD0`/`0036ABE0`. It is reached by explicit
  `00369C60` maintenance and the `0036BFE0` allocation-pressure fallback. It republishes the
  tagged slot and physically relocates allocated bytes; it does not repair EFX consumer fields.
  A binding-change/child-start request is not itself proof of relocation.
  `003E6AA0` stores one low-five-bit index in `+0x304[31:27]` and sets `+0x294` bit27.
  A later request replaces the earlier index. `00427DE0` leaves the bit pending when `+0x288 == -1`;
  otherwise it calls `003B3C00` and clears the bit regardless of the return. Stale tickets,
  invalid indices, and failed starts are not thereby retried. Index zero succeeds without rebase.
  The element-kind `0x28` site `003B939F` is a second direct demand path, not proof that all source
  moves are accompanied by a request or repaired within a frame.
- **Restored by the owner (OPUS, 2026-09-25): who asks for a rebase** — the requester census of
  `003E6AA0(record, n)` the rewrite dropped, **re-counted from the image: 23 control transfers, not the
  22 HEAD stated** — 18 calls, 3 tail jumps (`003B50D0`, `003B5660`, `003B56C1`) and 2 conditional tail
  branches (`002E73FA`, `002E743E`, inside `002E73C0`, the mount path's n = 3 request). Requesters: the
  battle-runtime-mode binding family `003B4B60`–`003B5520` (calls `003B4CBE` … `003B55D7`, `003B566D`,
  `003B567F`; n ∈ 2..0xB, on a mode/binding hand-over of the `02B40514` current-record word);
  `003B8260` itself at `003B846F`/`003B855C` (n = 0xA, link word `+6` no longer matching the pass's
  expected index); authored presentation command `0x28` = `00520720` (`00520727`, n = operand `+4`).
  Delivery: `RenderRecords_ProcessDirtyState` `00427DE0` calls `003B3C00` at `0042865B`. The per-step
  poll: `003B8260`'s element-kind dispatch (`jmp rcx` at `003B879B`, byte map `0x3B994C`) routes kind
  `0x28` to the arm at `003B936B` (`or ecx, -1` → `003A3FD0(-1)`, then `003326C0`); it reads the record's
  bound container index `+0x288` (`003B938D`; −1 skips) and calls `003B3C00(+0x288, element.+4)` at `003B939F`.
  Per SECTION-07 above, each of these is a **request**, not proof of relocation. **[page, OPUS re-count]**
  **There is also the combined container walk `0024D540`**: its `0024D565..0024D6A9` window,
  when the caller argument is zero, follows `02091108`/container `+0x348`, conditionally repairs
  borrowed contexts, and separately compares each container's `+0x390`. That window is executed
  with a documented entry/exit fixture; its surrounding render/service calls are not validated.
  The earlier same-frame/next-step language inferred a whole-game safety schedule from local call
  order. It is withdrawn. See [the producer and refresh specification](the-source-block-mover-and-separate-consumer-refresh.md).
- **Whether the arena can exceed 4 GiB in practice.** §4 establishes that the offset round-trip
  *requires* it not to; it does not establish what the allocator actually guarantees. That is BW-2,
  and it is now a question with a consequence attached rather than an observation.
  **Narrowed 2026-09-20 (SWE2-CONTRACT): the question splits, and half of it is answered.**
  *Capacity* is statically bounded: `0022A0B0`'s boot table allocates nine fixed-size backings
  totalling ≈256 MiB (29.75+13.125+1+1.75+108+48+32+18+4 MiB), arena 11 regrows to ≤4 MiB, and
  the nested arenas 12–14 are carved *inside* existing backings — ≈260 MiB maximum, so no arena
  can exceed 4 GiB of *extent*. What is not bounded is *placement*: the backings are ordinary
  CRT `malloc`s and the OS chooses their addresses — EXP-079 observed all of them below 2 GiB
  absolute at two states, but nothing in the image guarantees it. And since `01F83530` is
  ~~zero for the process's life (CD-2: BSS, no in-image writer by five instruments)~~ **zero at
  image load; one undriven in-image store route exists (the texture-id writer, id `0xFFFB`);
  zero for the process life is supported, not proven** (CD-2 narrowed 2026-09-26,
  FABLE-NOTICE-FRONTIER-EFX-REBASE-CARRIER-01F83530-SCOPE), the real
  precondition is the stronger absolute form — **every address the machinery touches must sit
  below 4 GiB in the address space** — which rests on CRT/OS placement policy, not on any
  allocator promise the engine makes. That half stays a live-observation question with the
  ASTRA line (EXP-077/078/079).
- **Lifetime.** SECTION-06 establishes selected disposal ordering and SECTION-07 executes real
  source movement followed by selected refresh paths. A stale raw pointer exists between those
  operations in the synthetic fixture. Universal pin discipline, overlapping-copy semantics in the
  actual Windows import, reentrancy/thread scheduling, and every specialized consumer remain open.

## 7. The pattern, named once: a 32-bit allocator wearing 64-bit pointers

Five independent places in this subsystem derive a quantity from 64-bit pointers **in 32 bits**.
They were found one at a time, in four separate reviews, and each looked like a local quirk. Together
they are a design:

| where | the 32-bit quantity | the window it is correct in |
|---|---|---|
| `0024D970` / `0024D940` rebase | the delta, `low32(new) − low32(old)`, `movsxd` on use | **±2 GiB** (§3) |
| `003EE111` EFX parse | the `memcpy` **length**, a 32-bit pointer difference, `movsxd` (§5) | **±2 GiB** |
| `0020E620` offset round-trip | the arena base subtracted as a **`dword`** where `0020E600` adds it as a `qword` (§4) | **4 GiB from `[01F83530]`** |
| resource entry tree links | `+0x24`/`+0x28`/`+0x2C` are arena **offsets**, resolved through the same pair ([tree contract](CONTRACT-resource-entry-tree.md) §1) | **4 GiB** |
| `0036B5F0` free-list bucket | `cmp dword ptr [rax], r8d` — **the ordering key is the low 32 bits of a 64-bit pointer**, while `mov qword ptr [rax], r8` stores all 64 | **4 GiB** |

> **The last one is the clearest statement of the whole pattern.** A 64 KiB bucket keeps the
> lowest-addressed free block; it decides *"lowest"* on 32 bits and then stores 64. **Two free blocks
> in one bucket that straddle a 4 GiB boundary therefore order wrongly** — the bucket keeps the
> higher, believing it lower — and nothing downstream can detect it, because the pointer it stored
> is perfectly valid.
>
> **Consumers should treat "the arena stays inside one 4 GiB window" as a precondition of this whole
> family, not as a property of any one function.** That is a stronger and more useful statement than
> five separate notes, and it is why `BW-2` is a correctness question rather than a curiosity.

### The `0x40` that appears in both directions

`0036B130` resolves a handle and **adds `0x40`**; `00369860` takes the pointer it is given and
**subtracts `0x40`** (`003698C1 lea rbx, [rcx - 0x40]`) before checking anything. The block header is
therefore **`0x40` bytes below the payload**, and the two constants are one fact seen from both
ends — which is what `0036B130`'s otherwise unexplained `add rax, 0x40` was doing all along.

The free routine's guards, all on that header: **`word[hdr] == 0xFF12`** (`003698D5`),
**`word[hdr+0x3E] == 0`** (`00369A80`, reached only once the magic matches), and
**`byte[hdr+0x14] & 1`** (`00369ABE`), with `00369B09 and byte [rbx+0x14], 0xFE` clearing that bit as
the block is released. **And the tag check comes first**: `00369892 test r14b, 3` sends a *tagged*
pointer to a diagnostic (`0x17D2E0`) instead of freeing it — the same tag-is-ownership rule as §2,
now guarding the allocator itself.

## 8. Script · resource · event interactions

The original `0050E300` script adapter pops two values, supplies arena ID and repeat flag to
`00369C60`, and returns the movement count. The `002E65A0` maintenance caller also invokes
arena 6/10 compaction. These callers are re-derived statically here; their full surrounding
script/load sessions are not executed. An ordinary allocation can reach the same movers through
`0036BFE0` before returning. Consumer refresh is separate: demand delivery and the combined
container-walk paths repair only their selected borrowed references. Movement, binding, and
refresh must not be collapsed into one event or one automatic all-pointer guarantee.

## 9. Determinism

- **RNG** — none.
- **Timing / ordering** — the rebase runs when the stored base disagrees with the resolved one; the
  combined path `0024D540` updates `+0x858` first and repairs `+0x390` only when the two differ by a
  full 64-bit comparison. Order between the two repairs is therefore fixed and observable.
- **Threading** — not established; the repair mutates walked lists with no lock read in these
  bodies, and concurrent relocation is precisely the hazard the mechanism exists for.

## 10. Failure paths and edge conditions

- **Identical base** — `0024D540` skips the `+0x390` repair on exact pointer equality (`je` at
  `0024D670`): a no-op, not a no-op walk.
- **Unresolved or null source** — the resolver returns 0; the `sext(low32)` guard rejects results
  `<= 0x40` — and *also* valid bases whose low 32 bits are 0 or `>= 0xFFFFFFC0` (the 4 GiB-boundary
  hazard, §2).
- **Untagged handle** — rejected by `test cl,3`; the trampolines pass raw pointers through.
- **Stale handle** — resolves without a generation check (`0036B130` skips what its three siblings
  do): the caller gets whatever the slot now points at, and the guard does not catch it.
- **~~`|delta| >= 2 GiB`~~ `delta` outside `[-2^31, 2^31)`** — pointers shift by ~~`delta - 2^32`~~ `delta - 2^32` above and `delta + 2^32` below (`-2^31` itself is exact) *(corrected 2026-10-02, OPUS: `0024D970+0x14` `sub ebx, dword ptr [rcx + 0x858]` forms a 32-bit delta and `003A9BA0+0xA` `movsxd rsi, ecx` sign-extends it; §13's `reb-delta-neg2gib-exact`)*; the published base stays correct and
  nothing detects the divergence. At exactly 4 GiB the delta is 0 — the most visible form.
- **Offset before the arena base** — cannot round-trip at all: `0020E600` zero-extends, so the
  window is unsigned `[base, base + 4 GiB)`, not signed ±2 GiB.

## 11. Observable behaviour

The repaired pointers live in the caller template's walked lists (`+0x108`, `+0x100`, `+0x18`,
`+0x20`, inner list via `+0x30`, outer via `+8`) and the two published base fields `+0x858` /
`+0x390` — all measurable in memory. The observable signature of the failure mode is a base field
pointing at the new block while every derived pointer still references the old one.

## 12. Reproduction formula

```
resolve (0036B130, called via 003AB7F0):
    if handle == 0 or (handle & 3) == 0: return 0      # tag required   <- corrected 2026-10-02, OPUS - through 003AB7F0 an untagged handle is returned unchanged (003AB7F0+0x13 test dl, 3; 003AB7F0+0x56 mov rax, rdx); only 0036B130 itself returns 0 for it
    if handle < 0x100000: return 0
    rax = qword[(handle & 0xFFFFFFFC) + 8] + 0x40      # block header sits 0x40 below payload
    if u32(sext32(low32(rax))) <= 0x40: rax = 0        # the 32-bit guard on a 64-bit pointer

newBase = sext32(+0x864) + resolve(sext32(+0x860))     # 003B3501 / 003B3508
if newBase == qword[+0x858]:  nothing to repair        # 003B3512

rebase +0x858 (0024D970):   delta = sext32(low32(newBase) - low32(oldBase))
    walks 003AA3D0 (dispatches on type byte +0x0E -> 00501420 / 00503F10), 003A9BA0, 003A9860
    every stored pointer += delta  (64-bit add of the sign-extended 32-bit delta)
    qword[+0x858] = newBase                            # full 64-bit publish
rebase +0x390 (0024D940):   the same shape, delta from low32(+0x390), walk 003A8FF0
    in 0024D540 this repair runs only when rsi != qword[+0x390]   # 64-bit equality guard

offset fields (00503F10):  p = off + qword[01F83530]; p += delta; off' = p - dword[01F83530]
    exact iff 0 <= p - base < 2^32  (unsigned); the delta itself exact iff -2^31 <= delta < 2^31
```

## Falsification pass 1 — 2026-09-13 (OPUS): there are **two** deltas, and the guard between them

*(Unnumbered: it previously held the `## 14.` heading, which collides with the template's
Unresolved section now written below.)*

Re-derived from the shipping image
([`falsify_efx_rebase.py`](../../Tools/analysis-kit/gfz-scripts/falsify_efx_rebase.py), every VA
resolved through the PE section table). The `movsxd` in each named walk confirms, the `0020E600` /
`0020E620` asymmetry confirms, and the arithmetic claim confirms. **Two statements are sharpened and
one is a structural correction.**

### The correction: "*that* delta" is two deltas, over two base fields

§15 cites `0024D970`'s `sub ebx, dword ptr [rcx+0x858]` as the rebase delta, and says all four walks
sign-extend it. Both halves are true, and together they read as one family. The image has **two
sibling rebasers**:

| entry | delta computed from | walks it drives | base it then stores |
|---|---|---|---|
| `0024D940` | `sub ecx, dword ptr [rbx+0x390]` | **`003A8FF0`** | `mov qword ptr [rbx+0x390], rdi` |
| `0024D970` | `sub ebx, dword ptr [rcx+0x858]` | `003AA3D0`, `003A9BA0`, `003A9860` | `mov qword ptr [rdi+0x858], rsi` |

**The four walks are 1 + 3 across two different base fields**, not four walks over one. A
reimplementation that satisfies §15 exactly — sign-extend the delta in all four — and drives all four
from the `+0x858` delta is wrong, and nothing in the contract as written would catch it.

Both fields show the same width asymmetry the storage contract shows: the base is **written as a
`qword`** and **read as a `dword`** to form the delta, which is precisely why the delta is
`low32(new) − low32(old)` and why §15's first row is right.

### The guard nobody recorded

`0024D540` runs both, and the second is **conditional**:

```asm
0024D662  mov qword ptr [rbp+0x858], rsi      ; the +0x858 base is updated
0024D669  cmp rsi, qword ptr [rdi+0x390]      ; are the two bases already the same?
0024D670  je  0x24D686                        ; <-- if so, SKIP the +0x390 repair entirely
0024D674  sub ecx, dword ptr [rdi+0x390]
0024D67A  call 0x3A8FF0
0024D67F  mov qword ptr [rdi+0x390], rsi
```

The comparison is a **full 64-bit `cmp`** while the delta it guards is 32-bit. So the skip is taken
only on exact pointer equality, and the repair it guards is the one whose exactness depends on the
2 GiB range — the conservative direction, but it is a behaviour a reimplementation has to reproduce:
**rebasing to an identical base must do nothing, not do a no-op walk.**

### Two sharpenings, both on claims stated as absolutes

**`|newBase − oldBase| < 2 GiB` is off by one value.** Sign-extension is identity exactly on
`−2³¹ ≤ d < 2³¹`. At `d = −2 GiB` the round trip *is* exact and the stated condition excludes it; at
`d = +2 GiB` it is not, and the stated condition also excludes it. A claim written as **if and only
if** has to carry the asymmetric range, not the symmetric absolute value.

**The offset round trip is not bounded by 2 GiB at all.** `0020E600` is `mov eax, ecx` — a **zero**
extension — then `add rax, qword [base]`; `0020E620` is `sub ecx, dword [base]`. So
`decode(encode(p)) == p` **iff `0 ≤ p − base < 2³²`**, unsigned: a pointer *before* the arena base
cannot round-trip at all, and one up to 4 GiB above it can. The asymmetry §15 names is real — the base
is added as a `qword` and subtracted as a `dword` — but the consequence is an **unsigned 4 GiB window
anchored at the base**, which is a different and stricter statement than the signed 2 GiB one that
governs the rebase delta. **Two different 32-bit truncations in one contract, with two different
safe ranges**, and the page had one bound for both.

## 13. Runtime validation

~~**Evidence class: static original-code reading, plus a call-graph census for the walk owners. Nothing~~
~~has been executed.** (2026-09-13, falsification pass 1.)~~

**Evidence class: static original-code reading PLUS isolated original-code execution (method B).**
**Consumed 2026-09-16 (OPUS) from [`EXP-084`](../_experiments/EXP-084-efx-source-rebase-execution.md)**
on `SWE2-ORACLE-REQ-OPUS-EFX-REBASE-FINDINGS` — **52 / 52 cases, 7 / 7 byte-level mutants detected**,
Unicorn 2.1.4 against the shipping EXE at canonical VAs. The sentence above is kept because it is what
pass 1 believed and why the experiment was designed.

**BOTH CASES THIS SECTION ASKED FOR WERE RUN, and one is sharper than it expected:**

- *rebasing to an identical base must perform no walk* — executed. Mutants `mut6` and `mut7` flip the
  `+0x390` and `+0x858` guards at `0024D670` / `0024D643` and the walks then run on identical bases,
  so the skip is a property of those guards and not of the caller.
- *an offset pointing before the arena base must fail to round-trip* — executed as `off-delta-underflow`,
  and **it does not fail. It wraps.** `0x100 − 0x200` stores `0xFFFFFF00`: a wrong-side pointer with no
  signal. `off-wrap-past-4gib` is the mirror — `0xFFFFF000 + 0x2000` stores `0x1000` and re-enters the
  arena low. **Silent wrap in both directions is a stronger failure than the non-round-trip this
  section predicted.**

**Measured edges a reconstruction can get silently wrong:**

| case | what executes |
|---|---|
| `reb-delta-neg2gib-exact`, `reb-delta-pos2gib-minus1` | the signed-32 window is exact at −2³¹ and +2³¹−1: every walked pointer moves with the published base |
| `reb-delta-pos2gib-diverges` | at +2³¹ the base publishes **+2 GiB up while every link moves −2 GiB down** (`0xFFFFFFFFB0015000`), no signal |
| `reb-delta-4gib-noop` | low32 delta 0 **freezes every link while the base publishes 4 GiB higher** — ASTRA's §6 observation, executed |
| `comb-low32-same-high-diff` | the guards are **64-bit** and the delta is **32-bit**: all four walks run with `delta32 == 0` and both bases republish low. `mut3` shows a 32-bit compare leaving the stale high base published while `+0x390` still rebases |
| `comb-390-differs-only` | the two deltas are **independent and per-field** — `0024D970` drives `003AA3D0`/`003A9BA0`/`003A9860`, `0024D940` drives `003A8FF0` alone |
| `res-high-4gib-boundary`, `res-high-wrap-c0`, `res-high-wrap-ff`, `res-neg-low32-kept` | the resolver's `<= 0x40` test is a **low-32 wrap band**: rejected is exactly `low32(slot+8) ∈ {0} ∪ [0xFFFFFFC0, 0xFFFFFFFF]`, and a result whose low32 has bit 31 set **survives** because `sext32` makes it unsigned-huge |
| `off-zero-base0`, `off-zero-baseNZ` | null is preserved **only under base 0**; under a nonzero base an offset of 0 decodes to the base, is "repaired", and stores the delta — a null silently becomes real |

**Two executed witnesses that the codec base must be zero**, agreeing with EXP-083: the null-offset
repair above, and list termination — `003AA3D0`'s terminator is offset 0, so a nonzero base ends the
walk's termination condition as well.

The two deltas, the 1 + 3 split of the repair walks across `+0x390` and `+0x858`, the 64-bit equality
guard and both truncation ranges are read from the shipping instructions; the caller set for
`003A8FF0` comes from `edges.tsv`, which is a census and not an execution.

**What would move this.** A harness that plants a small arena, records the encoded offsets, rebases to
a second base and checks every link — with the two deltas driven **separately**, because the whole
finding of pass 1 is that a reimplementation can drive all four walks from one delta and still be
wrong. Two cases are worth the trouble on their own: rebasing to an *identical* base must perform no
walk at all, and an offset pointing **before** the arena base must fail to round-trip, since
`0020E600` zero-extends.

**Still not established, and not by this:** whether any arena exceeds 4 GiB in practice. That is a
property of the allocator at runtime, not of these bodies.

## 14. Unresolved

1. ~~**The second object's type**~~ — **resolved 2026-09-20: the effect container** (`02EBD480`
   handle-table `+0x10`, one call site `003B3C4D`; `+0x340` = its `EfxCallerTemplate` context
   pointer, `+0x390` = its own source base; `CharacterRenderObject +0x390` is `auxVec36Begin`,
   a coincidence). See §6.
2. **Original mover established; global safety schedule remains open.** SECTION-07 executes the
   exact/adjacent selectors, actual block relocation, normal allocation-pressure fallback, full dirty
   delivery with one selected request, and an explicitly isolated combined-refresh window. The local
   ordering is specified in the linked mechanism. It does not prove every consumer is refreshed
   before use or that callbacks/threads cannot observe the producer's intermediate state.
3. **Whether any arena exceeds 4 GiB in practice** — **narrowed 2026-09-20** (§6): splits into
   *capacity*, statically bounded at ≈260 MiB (`0022A0B0`'s nine fixed backings ≈256 MiB plus
   arena-11 regrowth ≤4 MiB; nested arenas carve inside existing backings — no arena can exceed
   4 GiB of extent), and *placement*, which the image does not control — CRT `malloc` backings,
   observed below 2 GiB absolute (EXP-079), guaranteed by OS policy alone. Since `01F83530` is
   ~~zero for process life (CD-2)~~ **zero at image load; one undriven in-image store route
   exists (the texture-id writer, id `0xFFFB`); zero for process life is supported, not proven**
   (CD-2 narrowed 2026-09-26, FABLE-NOTICE-FRONTIER-EFX-REBASE-CARRIER-01F83530-SCOPE), the live
   precondition is the absolute form: every touched
   address < 4 GiB. The placement half stays with the ASTRA live line (EXP-077/078/079).
4. **Repaired-pointer lifetime** — SECTION-06 disposal and SECTION-07 real movement are bounded
   evidence. External-owner replacement, all pin/unpin callers, arbitrary specialized payloads and
   actual Windows overlapping-copy behavior remain independent obligations.

## 15. Evidence

> **Numbered 15, header lowercase `claim`, on purpose.** `parity_status.py` reads a
> contract's claim list from a heading that literally begins `## 15.` and keeps only a table
> whose first header cell is `claim`; miss either and it finds **zero** claims and refuses
> any harness written against this page instead of reporting a mismatch.

| claim | evidence | tier |
|---|---|---|
| the rebase delta is a 32-bit subtraction, `low32(new) - low32(old)`, sign-extended on use | `0024D970` `sub ebx, dword ptr [rcx+0x858]`; `003A8FF0` `movsxd r9, ecx` | 1 |
| all four repair walks sign-extend that delta — but **the four split 1 + 3 across TWO base fields**, `+0x390` (`0024D940` -> `3A8FF0`) and `+0x858` (`0024D970` -> `3AA3D0`, `3A9BA0`, `3A9860`); see pass 1 (falsification section) | `3A8FF0`, `3A9BA0`, `3A9860` `movsxd` directly; `3AA3D0` forwards `edx` to `00501420` and `00503F10`, which both `movsxd` | 1 |
| the repair is exact if and only if ~~\|newBase - oldBase\| < 2 GiB~~ **-2 GiB <= newBase - oldBase < +2 GiB** (sharpened by pass 1: sign-extension is identity on the asymmetric range, and `d = -2 GiB` exactly is exact) | `low32(new) - low32(old) == low32(new - old)`, and `sext32` is identity only on that range | 1 (static) |
| `0036B130` performs no generation check, unlike its three siblings | `0036A000` and `0036D170` compare `word [slot+6]` against `word [obj+0x1C]`; `0036B130` loads `[slot+8]`, adds `0x40`, returns | 1 |
| `+0x002` bit 2 means the context BORROWS its payload | `003EE117` stores the caller's pointer when set; `003A9613` skips the chunk release; `003B348A` gates publication | 1 |
| the offset round-trip is 32-bit in one direction only, and is exact **iff `0 <= p - base < 2**32` UNSIGNED** — `0020E600` **zero**-extends the offset, so a pointer before the base never round-trips (pass 1, falsification section) | `0020E600` adds the arena base as a `qword`; `0020E620` subtracts it as a `dword` | 1 |
| rebasing to an identical base is **skipped**, not walked — `0024D669 cmp rsi, qword ptr [rdi+0x390]` / `je`, a full 64-bit comparison guarding a 32-bit delta | `0024D662`-`0024D67F` in the combined path `0024D540` | 1 |
| the second object `0024D940` rebases at `+0x390` is the effect container the six-layer draw walk iterates — `+0x340` its `EfxCallerTemplate` context pointer, `+0x390` its own source base | one `003B3480` call site in `.text` (`003B3C4D`, E8 scan): `rdi = [02EBD480 + (id&0x3F)*0x38 + 0x10]`; `0024ED80` "make a container current" publishes `[obj+0x340]` template fields plus container `+0x120`/`+0x130`/`+0x1B8`; container fingerprint `+0x348`/`+0x364`/`+0x36A`/`+0x380`/`+0x39B`/`+0x3A8`/`+0`/`+4` matches the group-draw node; `CharacterRenderObject +0x390` disproven (`auxVec36Begin`, dtor-freed vector) | 1 |
| source movement and selected refresh have distinct triggers; demand zero does not refresh and bound failures consume the pending bit | SECTION-07 original native controls; `0036A2A0`, `0036BFE0`, `003E6AA0`, `0042863B..00428660`, `003B3C00`; original combined window `0024D565..0024D6A9` tested separately | isolated original instructions; not live scheduling |
| **what the ramp/source semantics mean, and whether any arena exceeds 4 GiB in practice** | arena **capacity** statically bounded ≈260 MiB (`0022A0B0` nine fixed backings ≈256 MiB + arena-11 regrowth ≤4 MiB; nested arenas inside existing backings); **placement** not established — CRT `malloc` backings observed <2 GiB absolute (EXP-079), OS-policy only; ramp/source semantics still open | capacity: 1 / placement: none |

## 16. Parity plan

~~No harness exists;~~ *(answered: see *Consumed 2026-09-16 (OPUS) from EXP-084* above - 52 / 52 cases; 2026-10-02, OPUS)* §13 names the experiment: plant a small arena, record encoded offsets, rebase to
a second base, and check every link — driving the two deltas **separately** (the `+0x390` repair and
the `+0x858` repair are independent inputs, and a reconstruction that drives all four walks from one
delta is wrong). Two cases stand alone: an identical-base rebase must perform no walk, and an offset
before the arena base must fail to round-trip.

**Dimensions that apply:** `CALCULATION` (both truncations and their exact ranges), `STATE-TRANSITION`
(the published base fields), `EDGE-CASE` (the `±2 GiB`/`4 GiB` boundaries, the null-source guard, the
identical-base skip). **Not covered, recorded:** `INTEGRATION` (the trigger and the EFX loader are
out of scope); `FULL-SUBSYSTEM`, `TIMING`, `PRESENTATION` do not apply to a relocation repair.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

- **CoreRuntimeScheduling — CLIENT and MECHANICAL.**
  - The combined path `0024D540` is run by `MainLoop_UpdateAndRenderFrame` ~~and a 463-byte core body~~, the 463-byte core body and the 1,583-byte frame body `0022B0B0` *(corrected 2026-10-02, OPUS: three direct callers, `0022B0B0+0xE1`, `0022B8C0+0x67` and `0022BC20+0x4F`)*, and it calls an
    8-byte getter.
  - `00369860`, `003AA3D0` and `00503F10` reach tables through the resolver / encoder pair.
- **Audio — CLIENT.**
  - The resolver sibling `0036B130` is also called by a 256-byte Audio-filed body.
  - The tree insert `0036D170` is called by three 83-byte Audio-filed bodies.
  - `0024D540` calls a 225-byte Audio-filed body.

  **Sound code uses the same resource arena and handle resolution as effects.**

- **Presentation — CLIENT and SERVICE (SWE2-CONTRACT 2026-09-15).** The rebase path is inside the
  render pass's resource family: `MainLoop_Draw` calls the combined path `0024D540`, which calls
  the Presentation effect bodies `003A8FF0`/`003A9BA0`/`003AB500`/`003ACA80`/`003B4A30`/`003B4A40`
  (the `003Axxxx` EFX-runtime helpers). `003AB7F0` — the handle-resolve this contract's source path
  shares — is called by the whole `PresentationEntryReferenceContainer_*` family
  (`ResolveEntryById`, `ReleaseNodeById`, `ForEachActive`, `InitializeNodes`, ~20 callers), and
  `CharacterRenderRecord_MaintainPresentationResourceReferences`. 62 edges measured against
  `edges.tsv`; the crossing is that effects ARE presentation resources — the rebase runs on the
  render layer's tables.
- **UI — CLIENT (SWE2-CONTRACT 2026-09-20).** `0024ED80` — the make-a-container-current
  publication the §15 second-object row names — is also called by the UI-filed transform
  evaluator `0024B9B0` (the shared neighbour the pass-22 ledgers file alongside `002C7B10`).
  UI code drives container currency through the same publication the render path uses — a
  client of the mechanism, not a second owner of it.
- **CombatAction and Party — CLIENT (SWE2-CONTRACT 2026-09-20).** `002E73C0` — the mount
  path whose two jcc branches deliver to `003E6AA0` in the §15 trigger row — is called by
  the CombatAction-filed `002FE8D0` and the Party-filed `00303F00`. Both are clients of the
  queue primitive through the mount path: combat actions and party state attach mounts and
  the mount re-resolve is what they queue, not a second trigger of their own.
- **ActorEntity — SERVICE (SWE2-CONTRACT 2026-09-20).** `0022A0B0` — the boot allocator the
  §15 capacity row names for the nine fixed arena backings — calls the ActorEntity-filed boot
  helper `002368D0` (the shared neighbour a dozen boot-path pages already cite). The edge is
  boot code using a shared helper, not an actor path touching the arena: the crossing is that
  the arena's capacity evidence is a boot sequence, and boot sequences share their helpers.
- **Input — SERVICE (OPUS 2026-09-30, 1 edge).** The same boot root `0022A0B0` calls `0035B270` at `0022A429`. That
  body resets the input layer's 32-row, `0x20`-stride slot table at `02EC0B80` and sets `02EC0F60` / `02EC0B61` to
  `0xFF` — the pad slot state that [the boot contract](../00-Engine-Core-Runtime/CONTRACT-boot-fixups.md) lists as
  its Input service. It is one more boot step beside the arena backings; no efx source path touches it.
- **RNG_Random_Selection — SERVICE (OPUS 2026-09-30, 1 edge).** `0022A0B0` seeds the gameplay Mersenne Twister with
  the literal `0x11B9` (`mov ecx, 0x11B9` at `0022A40B`, then `RNG_MT19937_Seed` `00379CF0` at `0022A410`), the boot
  seed [the gameplay-generators contract](../21-RNG-And-Determinism/CONTRACT-gameplay-generators.md) records. The
  crossing is again the shared boot sequence; the rebase draws no random number.

**Movement — CLIENT (SWE2-EC7-166, 7 edges).** `003B8670`, the bootstrap
coordinator that drives this page's `003A8510`/`003A8660` list purges,
also reaches the Movement layer - `0024B6F0`/`0024C6B0`/`0024C870`/
`0024F9B0` and 3 more are its callees there. Consultation across the
shared coordinator, not shared ownership of the `02EBEF88` list.

**Script_VM_Native_Bridge — CLIENT (SWE2-EC7-167, 5 edges).** `0026FE50` — the world-tick caller
of this page's `0024DB80` unlink-and-republish — is called by `0050D360`, and `003697F0` (the
free helper `0024DB80` names) by `0050DD40`; `003401D0`, `0050DEB0` and `0050D5E0` complete the
pair's five edges through `002E73C0`/`0036A000`/`0036B130`. Script-bridge bodies consult the
rebase helpers; not a shared responsibility for the `02EBEF88` list.

## Frontier-hub interior verifications — 2026-09-17 (SWE2-EC7, shared-callee pass)

Three frontier hubs bearing on this contract, read in the shipping image:

- **`0020E620`** — the encode half of the §4 round-trip, already quoted in this document. Interior
  verified: [`0020E626`](../_index/ADDRESS-INDEX.md) is `mov eax, ecx` — the 32-bit-only result of
  `sub ecx, dword [01F83530]`, confirming the asymmetric-width claim: encode narrows to a dword
  where `0020E600` resolves with a qword add. **232 frontier callers** — the single most-called
  unresolved body in the image before this pass.
- **`00430AF0`** — a record-level application of the §4 round-trip: six encoded image-address
  dwords at `[rdi+0x00]`, `[+0x04]`, `[+0x10]`, `[+0x14]`, `[+0x20]`, `[+0x24]`, each resolved
  through `0020E600`, shifted by the caller's delta `edx`, re-encoded through `0020E620`, and
  stored back; returns `rdi+0x40` (the next record field past the pointer block). Interior
  verified at [`00430B01`](../_index/ADDRESS-INDEX.md) — the `0020E600` resolve of the second
  field. 148 B, 56 frontier callers.
- **`00500470`** — the composed driver: calls the two-field sibling `004304F0` on `rdi`, `+0x10`,
  `+0x20`, `+0x30` with the same delta, returns `rdi+0x80`. Interior verified at
  [`0050047F`](../_index/ADDRESS-INDEX.md) — the first `call 004304F0`. 71 B, 52 frontier
  callers. `004304F0` itself is the two-field primitive ([`00430501`](../_index/ADDRESS-INDEX.md)
  — `call 0020E600` on `[rdi]`): resolve dword, add delta, encode, store; twice; return
  `rdi+0x10`.

NOT claimed: which record types these fix up (callers are the element-types pages' bodies), or
that the delta is the §3 template delta — the mechanism is the §4 encode round-trip applied per
field, which is all the bytes show.

## Interior citation — frontier hub `0042FCF0` (2026-09-17, SWE2-EC7)

`0042FCF0` — 188 B, 52 frontier callers at census; the eight-field sibling of the rebase family
(`004304F0` two-field, `00430AF0` six-field, `00500470` four-substructure). Interior verified:
[`0042FD01`](../_index/ADDRESS-INDEX.md) is the first `call 0020E600` — the body resolves the
dword fields at `[rdi]+0x00/+0x04/+0x10/+0x14/+0x20/+0x24/+0x30/+0x34`, adds the caller delta in
`ebx`, re-encodes each through `0020E620`, stores back, and returns `rdi+0x50` in `rax`. The field
pairs are non-contiguous — four stride-0x10 pairs rather than a flat array.

NOT claimed: which record type carries the `+0x50` payload or why the pairs sit at stride 0x10 —
the helper is a pure pointer fixup pass and does not read the record's tag fields.

## Interior citation — frontier hub `00431770` (2026-09-17, SWE2-EC7)

`00431770` — 177 B, 30 frontier callers at census; the composite driver of the rebase family this
page owns. Interior verified: `call 00430AF0(rdi,ebx)` (six-field) then
`call 0042FCF0(rdi+0x40,ebx)` (eight-field) cover `+0x00..+0x74`, then four inline
`0020E600`-resolve / `+ebx` / `0020E620`-encode / store-back pairs fix the dword pairs at
`+0x90`/`+0x94` and `+0xE0`/`+0xE4` (first inline resolve at
[`00431795`](../_index/ADDRESS-INDEX.md)). A flag fix (`+0xAA & 0x30` set keeps `+0xA9`, else
clears it) and a `call 00431610(rdi)` tail complete the pass; `rax = rdi+0xF0`.

NOT claimed: the record type — the layout is at least `0xF0` bytes with an embedded second rebase
record at `+0x40`, consistent with the nested-structure shape `00500470` showed.

`0024B7B0` (511 B) is the gated packet build `0024D540` calls: `020926E4 & 0x40` and `ecx == 0` gate, `00861EC0` zeroes a 0x60 message, `+0xC8` takes `& 0xF2 | 2`, `+0x39`/`+0x37` = 4, `+0x1D` |= 9, `00182B20` posts it, and the `movabs 0xFFFFFFFE20113700` mask + OR does the bit surgery - the combined path's request packet.

Interior anchor `0024B7F4` (function `0024B7B0`).

`0042AC30` (457 B) is the deferred-apply step `00427DE0` calls: `004292B0(rcx, rcx, 1)` returns `-2` and `byte[rbx+0x40B] & 3` clear plus `word[rbx+0x3B4] >> 0xC` in `{1,2}` selects the arm - `dword[+0x42C]` copies to `+0x390`, `0020E600` + `00423B10` rebase, and `byte[rbx+0x3C] == 'c'`/`00425E70`/`0042E1F0`/`0042EF90` continue - the rebase's pending-slot drain.

Interior anchor `0042AC65` (function `0042AC30`).

`004292B0` (268 B) is the range-gate helper `0042AC30`/`0042E1F0` call (returns -2 when out of range): `word[rcx+0x2F8] == -1` and `word[rdx+0x3B4] < 0x1000` reject, `0x104A` remaps to `0x103D`, `byte[rdx+0x40B] << 6` sign-extends the selector into `0041E5B0`, then `0020E600([rsi+0x10])` + `[rax+0xD90]` + `00422C20`/`00423B10` finish - the rebase's slot-validity check.

Interior anchor `0042931E` (function `004292B0`).

`00427100` (377 B) is a record selector `00427DE0` calls: `word[rcx]` index `x 0x740` into `022C6F28` (0xFFFF skips), `word[rbx + 6]`/`word[rbx + 0x2F2] == 1` gates, `00422EB0` x2 and `0042EF90` x2 drive the rebase - the pair's first selector.

Interior anchor `00427174` (function `00427100`).

`0042A890` (374 B) is the sibling selector `00427DE0` calls: `dword[rcx + 0x284] & 0x8000000` gates the same `word[+6] x 0x740` `022C6F28` lookup, `cmov` on `[rdx + 0x284]`, then `00426220`/`0041FC80`/`00423A10` pairs x2 and `0042EF90` x2 - the flag-armed variant of `00427100`.

Interior anchor `0042A942` (function `0042A890`).

`003A8660` (332 B) is the keep-type purge on the `02EBEF88` repair-walk list: walks `[rdx+8]`, and for every node whose `byte[+0x1C]` does NOT equal `esi` unlinks prev/next, frees `rbx+0x110` through `003A92D0`+`003697F0`, and reindexes the `+0x18` index table (`-1` sentinel, `dword == r9d` match) - keeps only nodes of type `esi`.

Interior anchor `003A86E0` (function `003A8660`).

`003A8510` (332 B) is the remove-type purge on the `02EBEF88` repair-walk list: identical walk and index reindex to `003A8660` but the `byte[+0x1C]` compare is inverted (`jne` skips) - unlinks and frees exactly the nodes of type `esi`. The two bodies are complementary arms `003B8670` and the `00333xxx` callers drive.

Interior anchor `003A8590` (function `003A8510`).

`0024DB80` (318 B) is the unlink-and-republish `0026FE50` calls on `020910A0[byte[rcx]*8 + 0x50]` nodes: walks the `rbx+0x348`/`+0x350` chain until `word[rbx+4] == word[rsi+4]`, splices the node out (prev `+0x350` <-> next `+0x348`, head fix when `+0x350` null), then republishes three list heads - `02F97348`=rbx, `003A81E0` on `rbx+0x120` into `02EBEF98`, `003A72E0` on `rbx+0x130` into `02EBEFB0`, `003A8D70` on `rbx+0x1B8` into `02EBEF88`, with `00182CA0`/`003697F0` on `rbx+0x380` - the repair-walk list head rebuild the purge arms consume.

Interior anchor `0024DC2E` (function `0024DB80`).

`0042B130` (309 B) is the two-record vector push `00427DE0` calls: `word[rcx] != -1` resolves `sx*0x740 + 022C6F28`; `00426220` gates the record, then `00424010` stores the caller's `+0x3C0`/`+0x3C4`/`+0x3C8` float triple; the resolved record's `word[+8]` successor takes the same `00426220`/`00424010` pass on the same triple - the pair write the rebase's per-source arm runs.

Interior anchor `0042B1A5` (function `0042B130`).

`0042A580` (298 B) is the two-record conditional `00427DE0` calls: `word[rcx] != -1` resolves `sx*0x740 + 022C6F28`; `word[+6] == -1` zeroes `rsp+0x78` while `word[+0x2F2] == 1` or the `+6` miss runs `0016D6A0`; `word[+8]` repeats the lookup, then `word[+8]`/`word[+0xA]` successors each pass `0042EF90` with the `0042E4B0` template into `rsp+0x20`; `dword[+0x294] &= ~0x100000` closes - the rebase's template-emit arm `0042A050` parallels.

Interior anchor `0042A653` (function `0042A580`).

`0042A050` (289 B) is the flag-gated sibling `00427DE0` calls: `byte[rcx+0x294] & 8` fast-paths (`dword[+0x284] &= ~0x90000000 | 0x10000000`, `word[+0x5E] |= 1`, return); else `word[rcx]` resolves `sx*0x740 + 022C6F28` and both the record and its `word[+8]` successor run `00426220` with `00422C20` on the false arm, then `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E020` template - the same two-record walk under the `0x294` fast flag.

Interior anchor `0042A116` (function `0042A050`).

`0042BCB0` (287 B) is the bit-3-of-`+0x304` reconcile `00427DE0` calls: `word[rcx] != -1` resolves `sx x 0x740 + 022C6F28` and `00426220`'s false arm sets or clears `0x200000` in `dword[+0x284]` by the flag; `word[+8]` repeats the walk on the successor record, then `word[+8]`/`word[+0xA]` each pass `0042EF90` with the `0042E750` template - the same two-record shape as `0042A580` under the `+0x304` bit-3 source.

Interior anchor `0042BD8F` (function `0042BCB0`).

`00429E50` (284 B) is the flag-gated sibling `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28`; `00426220`'s false arm runs `00422DF0`, and with `edx` nonzero `00422D50`'s result ORs `0x20000` into `dword[rax+0xC]`; `word[+8]` repeats the pair on the successor, then `word[+8]`/`word[+0xA]` take `0042EF90` with the `0042DEC0` template - the sub-record flag arm.

Interior anchor `00429EF8` (function `00429E50`).

`0042B850` (283 B) is the bit-5-of-`+0x304` variant `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28` and `00426220`'s false arm runs `00420F50(record, flag)`; `word[+8]` repeats on the successor, `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E610` template, and `dword[rbx+0x290] &= ~0x10000000` clears the mark on both the walked and `-1` paths - the reconcile that always drops the high bit.

Interior anchor `0042B8F9` (function `0042B850`).

`0042AF10` (281 B) is the `+0x394`-context sibling `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28`; on `word[+6] == -1` or `word[+0x2F2] == 1` the record runs `0016D6A0(record, rcx+0x394, word[rcx+0x3B4], 1)`; `word[+8]` repeats the test on the successor, then `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E350` template - the resolver arm `0042A580` parallels without the `00426220` gate.

Interior anchor `0042AF86` (function `0042AF10`).

`0042BCB0` (287 B) is the bit-3-of-`+0x304` reconcile `00427DE0` calls: `word[rcx] != -1` resolves `sx x 0x740 + 022C6F28` and `00426220`'s false arm sets or clears `0x200000` in `dword[+0x284]` by the flag; `word[+8]` repeats the walk on the successor record, then `word[+8]`/`word[+0xA]` each pass `0042EF90` with the `0042E750` template - the same two-record shape as `0042A580` under the `+0x304` bit-3 source.

Interior anchor `0042BD8F` (function `0042BCB0`).

`00429E50` (284 B) is the flag-gated sibling `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28`; `00426220`'s false arm runs `00422DF0`, and with `edx` nonzero `00422D50`'s result ORs `0x20000` into `dword[rax+0xC]`; `word[+8]` repeats the pair on the successor, then `word[+8]`/`word[+0xA]` take `0042EF90` with the `0042DEC0` template - the sub-record flag arm.

Interior anchor `00429EF8` (function `00429E50`).

`0042B850` (283 B) is the bit-5-of-`+0x304` variant `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28` and `00426220`'s false arm runs `00420F50(record, flag)`; `word[+8]` repeats on the successor, `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E610` template, and `dword[rbx+0x290] &= ~0x10000000` clears the mark on both the walked and `-1` paths - the reconcile that always drops the high bit.

Interior anchor `0042B8F9` (function `0042B850`).

`0042AF10` (281 B) is the `+0x394`-context sibling `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28`; on `word[+6] == -1` or `word[+0x2F2] == 1` the record runs `0016D6A0(record, rcx+0x394, word[rcx+0x3B4], 1)`; `word[+8]` repeats the test on the successor, then `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E350` template - the resolver arm `0042A580` parallels without the `00426220` gate.

Interior anchor `0042AF86` (function `0042AF10`).

`00429D40` (271 B) is the bit-2-of-`+0x304` sibling `00427DE0` calls: `(dword[rcx+0x304] >> 2) & 1` stages the flag; `word[rcx]` resolves `sx x 0x740 + 022C6F28` and `00426220`'s false arm runs `0041FBF0(record, flag)` then `00421030`; `word[+8]` repeats the pair on the successor, then `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042DE50` template - the two-record reconcile under the `+0x304` bit-2 source.

Interior anchor `00429E0F` (function `00429D40`).

`0042AE00` (269 B) is the pending-slot arm `00427DE0` calls: `word[rcx]` resolves `sx x 0x740 + 022C6F28` and `rcx + 0x394` stages the context; records with `word[+6] == -1` or `word[+0x2F2] == 1` run `0016D6A0(record, ctx, 0, 1)`; `word[+8]` repeats the test on the successor, then `word[+8]`/`word[+0xA]` pass `0042EF90` with the `0042E320` template - `0042AF10`'s shape without the `word[+0x3B4]` arg.

Interior anchor `0042AE6C` (function `0042AE00`).

`0042AB20` (267 B) is the `022C6F28` reconcile `00427DE0` runs under a cleared busy bit: `dword[rcx+0x294] &= ~0x8000` drops the pending flag and `xmm0 = [rcx+0x3BC]` caches the scalar; `word[rcx]` (non-`0xFFFF`) resolves the `x 0x740` record for `00426220`, with `00423AB0(record, xmm1)` rerun when the check fails; the record's own `+8` link repeats the same pair, and non-`0xFFFF` `+8`/`+0xA` links each fire `0042EF90` with the `0042E1B0` callback - the sibling walk `0042B580` runs under its `+0x3F4` guard instead.

Interior anchor `0042AB83` (function `0042AB20`).

`0042F3B0` (266 B) is the two-record vector write `002E26F0` runs: `dx` and `cx` each index `022C6F28` `x 0x740` (null when `dword[+0x284] == 0`), the `dx` record's `+0x284` gaining bit `0x1E` when bit `4` was already set; on the `cx` record three vec3 calls land - `00420CF0` from `r9`, `00420F20` from `[rsp+0x50]`, `00420D50` from `[rsp+0x58]` - then `+0x3CE = di`, `+0x3CC = si`, and `+0x290` is masked `& 0xFFEBFFFF` (clearing bits `0x12`/`0x14`) with bit `0x13` set - the three-vector pose commit the ladder stages on linked records.

Interior anchor `0042F447` (function `0042F3B0`).

`0042B580` (263 B) is the recursion-guarded variant of the `0042AB20` walk: `byte[rcx+0x3F4]` is saved, forced to `0x80`, and restored on every exit; `word[rcx]` resolves the `x 0x740` record for `0042BED0`, its `+8` link resolves a second the same way, and that record's non-`0xFFFF` `+8`/`+0xA` links each fire `0042EF90` with `0042BED0` itself as the callback - the self-recursive arm the guard byte exists to serialize.

Interior anchor `0042B5EA` (function `0042B580`).

`00420F20` (45 B) is the plain vec3 commit `0042F3B0` and `002EDAA0` run on a `022C6F28` `x 0x740` record: `dword[+0x284] &= ~0x200`, `xmm1`/`xmm2`/`xmm3` land at `+0x140`/`+0x144`/`+0x148`, `+0x14C = 1.0f` - the direct three-float write of the pose ladder.

Interior anchor `00420F2A` (function `00420F20`).

`00420CF0` (81 B) is the stash-then-write variant `0042F3B0` and `002EDAA0` run: the old `+0x120`/`+0x124`/`+0x128` vec3 is first copied down to `+0x250`/`+0x254`/`+0x258`, then `xmm1`/`xmm2`/`xmm3` land at `+0x120`/`+0x124`/`+0x128`, `+0x12C = 1.0f`, `dword[+0x284] &= ~0x200` - the previous-value-preserving arm of the same commit.

Interior anchor `00420D1E` (function `00420CF0`).

`0042A180` (257 B) is the first `022C6F28` triplet `00427DE0` runs: `word[rcx]` (`!= 0xFFFF`) `x 0x740` selects the record, `00426220` gates it and on zero `00425510(rbx, xmm1 = [rcx+0x30C])` applies the float; `word[rbx+8]` links to the second record for the same gate, then `0042EF90` fires twice with `0042E050` - the `+0x30C` payload arm of the triple.

Interior anchor `0042A1D9` (function `0042A180`).

`0042AA10` (257 B) is the sibling triplet `00427DE0` runs - identical `word[rcx]` `x 0x740` select, `00426220` gate and `word[rbx+8]` follow, but the fallback is `00423A60(rbx, xmm1 = [rcx+0x3B8])` and the `0042EF90` pair carries `0042E170` - the `+0x3B8` payload arm.

Interior anchor `0042AA69` (function `0042AA10`).

`0042A290` (250 B) is the third triplet `00427DE0` runs - same select/gate/link shape, fallback `00423570(rbx, edx = word[rcx+0x3B6])` and `0042EF90` with `0042E090` - the integer-payload arm of the three.

Interior anchor `0042A2E6` (function `0042A290`).

`0042B030` (241 B) is the `+8`-chain `0042E380` walk `00427DE0` runs: `word[rcx] != 0xFFFF` resolves `sx x 0x740 + 022C6F28` and calls `0042E380` with a `rsp+0x20` out, then `word[rbx+8]` chains to the next record the same way until `-1`; the terminal legs run `0042EF90` twice - the two-record variant of the reconcile family.

Interior anchor `0042B07D` (function `0042B030`).

`00429410` (237 B) is the `+8`-chain `0042BDE0` walk `00427DE0` runs - the same `word[rcx] x 0x740 + 022C6F28` select and `word[rbx+8]` follow, calling `0042BDE0` per record with the `rsp+0x20` staging and closing on `0042EF90` x2; a `0xFFFF` head instead clears bit `0x10000` of `dword[rcx+0x290]` - the sibling whose empty-chain arm drops the flag.

Interior anchor `00429462` (function `00429410`).

`00429830` (237 B) is the `+8`-chain `0042D8B0` walk `00427DE0` runs - identical select/follow shape with `0042D8B0` as the per-record body and `0042EF90` x2 to close; a `0xFFFF` head clears bit `0x20000` of `dword[rcx+0x290]` - the third sibling of the chain-walk family.

Interior anchor `00429882` (function `00429830`).


## Source movement and ownership — SECTION-06 current boundary (2026-09-22)

[The new ownership contract](CONTRACT-resource-input-ownership.md) distinguishes the outer owner,
inner borrowed context, tree membership and actual reclamation. The existing rebase driver is the
missing connection between “resize itself does not repair borrowers” and the separate pointer
refresh mechanism; neither observation alone proves a safe whole-game schedule.

In the new native fixture, type3 construction and parsing run against a tagged slot's original
source. The fixture copies the source and changes that slot's owner pointer, explicitly simulating
movement; it does NOT run the engine's mover. Calling original `003B3480(context, NULL)` then
updates +858 and the 800 lookup element through original `0024D970`/`003A9860`. The next unchanged
call does not double-apply the delta. **The old +870 run origin remains unchanged.** The borrowed
cleanup branch subsequently ignores that old address while releasing the context's own table.
This proves a selected refresh/cleanup contract, not continuous pointer safety between callbacks.

The new [171-assertion production fixture](../_experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md)
uses default subtype255 and empty other lists. The optional instance branch and every specialized
rebaser remain outside its execution coverage. Historical signed-width controls remain historical;
no whole old campaign or current live movement observation is newly claimed.

## Original movement and consumer-order reconciliation — SECTION-07 (2026-09-23)

[Review, controls and limits](../_experiments/evidence/continuation-section07-source-movement/REVIEW.md).
Unlike SECTION-06's simulated move, the actual allocator now selects, unlinks, moves and reissues
source storage. The handle resolves to the new address while the tested context base and table
entry still contain the old one, until an original refresh path runs. The arena movement latch is
independent of a record's child-start pending bit. The combined walk is another refresh path; it is
not gated on that pending bit. The historical SECTION-06 subsection above remains a record of that
packet's scope, not a claim that movement is still simulated by this packet.

At the imported-copy boundary the slot already names the destination and the old source has been
released by the arena. This is a local ordering observation, not an atomic-publication or concurrent
safety proof. A smaller adjacent hole reaches overlapping copy ranges; that control stops BEFORE
copying and deliberately does not emulate Windows `memcpy` using a host `memmove`.

The native fixture has 123 named assertions and ten rejecting targeted variants, plus the separate
copy-boundary observation. It uses one diagnostic substitution, three imported bridges and a stated
combined-window entry/exit boundary. Formal independent acceptance is pending; historical audits,
TEAM and the L2 verdict are not promoted.


## SECTION-10 — nonempty A00 subtype0 repair (external production, 2026-09-23)

The [new fixture](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md) extends prior default/empty records with original specialized fixups.
`003A9BA0` first invokes `005004C0` on the moved record with the signed delta, then updates the
lookup pointer. For A00 subtype0 the original dispatcher reaches `00500470`, whose four
`004304F0` calls repair eight DWORD encoded-pointer fields at record+00/+04, +10/+14, +20/+24,
and +30/+34. Nonzero offsets are used, so a no-op dispatcher cannot pass.

The actual original compactor moves the allocation, preserving already-repaired words that still
name the old location. Original refresh repairs the context base, lookup entry and nested encoded
fields. Repeating refresh with an unchanged base preserves them. Identity/subtype are unchanged,
while the borrowed run-origin field remains stale. Original context disposal and owner free are
checked independently. This is not evidence that every specialized record or thread interleaving
is safe. Optional configuration, full child/render execution, other subtype walks and the Windows
overlap-copy dependency remain open. Local validation does not re-score an L2 verdict.

`003AA3D0` (92 B) is the type-letter dispatch `0024D540` and `0024D970` share over the `[02EBEF70]`-headed chain: each node is chased through `0020E600([rbx])`, and per node a `+0xE` byte of `0x52` ('R') fires `00501420` while `0x56` ('V') fires `00503F10` - the per-element fixup by record kind behind the rebase

Interior anchor `003AA412` (function `003AA3D0`).

`003A9BA0` (105 B) is the delta-rebase loop the same callers run over the `[02EBEF78]` table: for each `rbx` step of 8 through `0x1800`, a live slot gets `005004C0(old + rsi, esi)` and then the stored pointer itself shifts by `rsi` - ~~768~~ 767 entries repointed (indices 1 to 767; `rbx` starts at 8) by the source-move delta *(corrected 2026-10-02, OPUS: `003A9BA0+0xD` `mov ebx, 8` and `003A9BA0+0x50` `cmp rbx, 0x1800`)*

Interior anchor `003A9BEC` (function `003A9BA0`).

`003A9860` (105 B) is `003A9BA0`'s sibling rebase over the `[02EBEF90]` table, `rbx` stepping 8 through `0xA00` with `00442460` as the per-slot notify - ~~320~~ 319 entries repointed (indices 1 to 319) by the same delta *(corrected 2026-10-02, OPUS: `003A9860+0xD` `mov ebx, 8` and `003A9860+0x50` `cmp rbx, 0xa00`)*

Interior anchor `003A98AC` (function `003A9860`).

`0041E5B0` (212 B) is the tag-slot lookup `004292B0` runs on the `003E55F0` record: a six-entry byte table at `+0x2C` is scanned for `(byte & 0x7F) == (r8d & 0xFFF)` under the high-bit tag, `0x7F` terminating; `edi` selects whether the tagged or untagged arm wins first - the rebase's 'which slot carries tag X' probe

Interior anchor `0041E5C4` (function `0041E5B0`).

`00429760` (204 B) is the two-lane record resolve `00427DE0` runs: `[+0x2C8]` word (minus-1 gated) `x 0x740` selects the `022C6F28` row (zeroed when `[row+0x284] == 0`), `+0x3D1 & 7` arms `r9`, and `0041EDE0` consumes it; when `+0x3D1 & 0x38` is set the second lane resolves `[+0x2CA]` the same way through `003E5CF0` before its own `0041EDE0` - the paired primary/secondary selector inside the dirty pass

Interior anchor `00429788` (function `00429760`).

`0041EDE0` (555 B) is the mode-dispatched record writer `00429760` calls per resolved row: mode = 0 when `+0x284 & 0x8000000` is set, else `r9` (or the sign-extended top two bits of `+0x40B` when `r9 == 2`); it writes the mode into `+0x40B` bits 2-3, then mode 1 emits `004211B0` on the `[r15+0x36]` word and stores two `w = 1.0f` 16-byte rows at `+0x130`/`+0x150` plus the `[r14 + rbp*4 + 0x1C0]` vec3 at `+0x170`, while mode 0 walks a u16 index table (`[rax + rbp*2]`, `0xFFFF` skips) and emits the `[r14 + rbp*12 + 0x240]` vec3 - `003E55F0`/`003E5CD0` supply the two lookups

Interior anchor `0041EE45` (function `0041EDE0`).

`0042E380` (183 B) is the code-dispatched emit `0042B030` runs on a source record: records with `[rcx+6] == -1` or `[+0x2F2] == 1` read the code word `[rcx+0x3FA]` - under `0x1000`, or `0x2005` when the `003E55F0` row is missing or its `+1` byte is clear, the record is `0041FC80`-released first; a live `[+0x2F8]` record instead `0041E5B0`-submits with `edx` the sign-extended low six bits of `[[rdx+8]+0x40B]` and `r8d = [[rdx+8]+0xCC]`; either lane finishes through `00423FC0`, and when `[rbx+6] == -1` the result lands at `[rsi+0x58]`

Interior anchor `0042E3D1` (function `0042E380`).

`0041FC80` (26 B) is the bit-arm helper `0042A890` and `0042E380` call: `00422D50` resolves the shared record and, when it returns non-null, `or dword ptr [rax+0xC], 0x1000000` sets the bit - the single-flag publish the rebase path trips before returning

Interior anchor `0041FC8E` (function `0041FC80`).

`00423FC0` (74 B) is the shared finisher `0042DF10` and `0042E380` both tail into: a non`-1` `[rcx+0xC8]` id resolves through `0020E600([rcx+0x10])` then `0051B9E0` on `[rax+0xDA8]`, and a live result gets `or [rax+0xC], 2` plus `0041D790` before the record falls through to `004253D0`

Interior anchor `00423FE7` (function `00423FC0`).

`004253D0` (320 B) is the three-phase finish `00423FC0` tail-jumps into: with `[rcx+0xC4]` live it `0020E600`s `[+0x10]` and `0051B9E0`s `[rax+0xDA8]` - a `[+0x24] == 1` record whose `[+0x31A]` word matches `[rbx+0x413]` returns 0 untouched; otherwise the hit gets `or [rax+0xC], 2`, a set `[rbx+0x284]` bit `0x14` is cleared into `or [rdi+0xC], 0x4020000`, `0041D7E0` consumes the `[+0x2B0]`/`[+0x2B4]`/`[+0x2B8]` floats which reset to `-1.0f`, `0041D790` publishes, and a third pass re-resolves with `xmm6 = [rbx+0x2BC]`

Interior anchor `004253F7` (function `004253D0`).

`00425510` (152 B) is the paired-lane finish `0042A180` and `0042E050` call: with `[rcx+0xC4]` live it `0020E600`s `dword[+0x10]` and `0051B9E0`s `[rax+0xDA8]` into `rdi`, the same resolve runs for `[rbx+0xC8]` and a hit gets `or [rax+0xC], 2` + `0041D790`, then `004253D0(rbx)` finishes the record and `0041E330(rdi, xmm6)` runs with the preserved float - the two-row variant of the `00423FC0` lane.

Interior anchor `00425532` (function `00425510`).
