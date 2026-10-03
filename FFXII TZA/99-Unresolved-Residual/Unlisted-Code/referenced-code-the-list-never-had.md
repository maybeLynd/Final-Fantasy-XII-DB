---
system: Referenced code the function list never had - twelve implementations the database calls and has never named
category: 99-Unresolved-Residual
status: DOCUMENTED — every register row is closed: the 129 blocks called only from unlisted code (UQ-371) are SUPERSEDED 2026-09-26 under FRONTIER's class-1 ruling, the population carried by this page's tables; whether owning pages absorb the entries (UQ-372) is NOT A QUESTION 2026-09-26, carried by FABLE-CARRIER-PAGE-OWNERSHIP-AND-PROPAGATION-0926 (done); the flag meanings (UQ-373), kind 3 (UQ-374), the three globals (UQ-375) and the zero cases (UQ-376) are answered; owner read 2026-09-29 (OPUS)
owner_layer: multiple - these bodies belong to the subsystems that jump into them
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: every unlisted block intersected with the four static reference forms; the fourteen with
    a listed caller decoded in full; every rip-relative operand resolved to its target address
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_kind: derivation
  last_pass_state: opus-referenced-unlisted-1 - fourteen bodies reached by a tail jmp from a listed
    function, twelve of them named nowhere in the database before this page. The other 130
    referenced blocks are called only from other unlisted code.
  crossref_clean: false
  reopened_count: 0
---

# Referenced code the function list never had

> Code that nothing points at being absent from a reference-derived census is expected.
> **Referenced code being absent is a different and worse defect**, and it is what this page is.
> Fourteen bodies are reached by a `jmp` from inside a listed function - **the list stopped at the
> thunk and never recorded the implementation** - and **twelve of the fourteen appear nowhere in
> this database**.

## 1. The population

Of the 1,471 unlisted code blocks in
[`the-code-the-function-list-does-not-contain.md`](the-code-the-function-list-does-not-contain.md),
**143 carry at least one static reference** - 6,038 bytes in all. **142 by admissible routes:** one of the
143 is named only by a chained `.pdata` range, which is banned as evidence and does not count toward
anything here (pass 6, 2026-09-15; the instrument still unions it,
`OPUS-REQ-SWE2-EC7-UNLISTED-REFERENCED-ROUTES`).

| how it is referenced | blocks |
|---|---:|
| a direct `call` or `jmp` | 135 |
| a relocated pointer in a data table | 6 |
| ~~a chained `.pdata` range~~ | ~~1~~ banned as evidence; not a reference |
| a rip-relative `lea` | 1 |

**~~129~~ 121 of the 135 are called only from other unlisted code.** *(corrected 2026-10-02, OPUS: 135 − 14 = 121, rel32 sweep against the listed extents; 129 is 143 − 14 and counts the six relocated, the one `lea` and the one `.pdata` block)* The remaining **fourteen have a caller
the function list does contain**, and every one of those fourteen is reached by a **tail `jmp`**,
never a `call`.

> That is the shape of the defect. `0034ED80` is listed at 56 bytes; its real body is **eleven**,
> ending `jmp 0x2ec3c0`. The recorded size then runs past the padding and swallows a **second,
> unrelated function**. The list took the thunk, gave it the wrong length, and never took what the
> thunk jumps to.

## 2. The fourteen

`rcx`, `edx`, `r8d` are the arguments as they arrive at the tail jump, not necessarily the
caller's own.

| body | B | jumped to from | what the instructions do |
|---|---:|---|---|
| `001DDAC0` | 223 | `001DDBA0` | **aspect fit**: `w/h` against `16/9` (`008C5B38`) and `16/3` (`00900A0C`); writes a 0x18-byte record - mode at `+0x00`, two scales at `+0x04`/`+0x08`, a third at `+0x0C`, `w` at `+0x10`, `h` at `+0x14` |
| `0055B310` | 209 | `0055BFF0` | sweeps a table at `[rcx+0x120]`, stride `0x38`, `[rcx+0x55A]` rows of `[rcx+0x559]`; per entry compares nibbles of `+0x18`; **when `[rcx+0x570]` bit 0 is set** collects up to `0x20` entry pointers into `[rcx+0x308]` counting at `[rcx+0x408]`, **otherwise** rewrites `+0x18` in place; clears `[rcx+0x570]` bit 0 and returns 1 if anything changed |
| `003B6950` | 83 | `004174D0` | slot record at `[02B40528] + id*0xE0`, id checked against `+0x10`; if the step count `dl` is non-zero, stores it at `+0x03` and writes `(target - [+0x78]) / dl` to `+0x7C`; if zero, writes the target straight to `+0x78` and clears `+0x03` |
| `003B69B0` | 83 | `00417440` | **the same, one channel over**: `+0x01`, `+0x70`, `+0x74` |
| `002EC3C0` | 43 | `0034ED80` | if `([rcx+0x03] & 0xE0) == 0x60`, takes `[[rcx+0xB8] + 0xF0]` and sets bit 0 of its `+0x6A` from `edx != 0` |
| `003594C0` | 27 | `0034ED30` | global byte `022C7FF8`: ~~**writes `cl` only if the byte is currently zero** - a first-writer-wins latch~~ **writes `cl` only if the byte is currently non-zero** (`test dl, dl` / `cmovne r8d, eax`, `003594C7`..`003594CF`) - an upgrade of a pending request; corrected 2026-09-18 (FABLE) |
| `00269E00` | 24 | `00353630`, `00353A50` | `[rcx+0x14]` **bit 5** := `dl & 1`; when `edx` is zero, tail-jumps `0025B500` |
| `003DE3E0` | 23 | `00354950` | global byte `02B58C3C` bit 0 := `ecx != 0` |
| `00269F00` | 21 | `00353D00`, `00354910` | `[rcx+0x08]` **bit 0** := `dl & 1`; when `edx` is zero, tail-jumps `0025B500`. **Already known** - the movement-mode page found it by hand |
| `0025D9C0` | 18 | `0034C880` | loads the global at `02099D70`, passes `word [rcx]` and `[global+0x28]`, tail-jumps `00263A30` |
| `002697F0` | 10 | `0050E390` | `edx := 1`, tail-jumps `00269860` |
| `0026AF70` | 7 | `0034D350` | global byte `02099DA0` := `cl` |
| `0026DC50` | 5 | `00350320`, `003505F0` | `jmp 002ECD20` |
| `0036E9A0` | 5 | `00340010` | `jmp 003B1560` |

`003594C0` is the second of the two the database already had: the party page names it.

**Twelve of the fourteen are named nowhere else in this database**, and their callers are:
`_index/ADDRESS-INDEX.md` (six), `the-shape-of-the-verb-population.md` (three),
`the-encoded-id-space-and-the-query-record.md`, `scriptvm-verb-dispatch-and-parameter-encoding.md`,
`how-the-engine-chooses-3d-or-flat-movement.md`.

## 3. Why this matters more than its 6 KB

**The database already documents the callers.** A reconstruction that follows a documented page to
`00353D00` finds thirteen bytes and a jump into nothing the database has ever described. The
movement-mode page shows the way out of it - **it read through the jump and recorded
`00269F00`'s `+0x08` bit 0 by hand** - but that was one person noticing one case, not a property of
the census.

> **A thunk is not the function.** The list contains the thunk, the page documents the thunk's
> address, and the write that actually happens is in a body neither of them has.

## 4. The same instrument found a third defect: bodies that overlap

The boundary rule was pointed inside the listed bodies as well as between them.

| | |
|---|---:|
| listed bodies whose recorded range **contains another listed body** | **29** |
| bodies contained | 49 |
| bytes counted twice as a result | 1,759 |

`002673D0` is listed at 95 bytes and its range covers **three further listed bodies** -
`002673F0`, `00267410` and `00267420`. `001DDBA0` is listed at 381 bytes and covers `001DDC40`,
which is 430 bytes long and reaches past its container's end.

**This is small and it is not nothing:** `progress.py` sums body sizes to compute span coverage, so
1,759 bytes are counted twice there, and any citation into an overlapped body is ambiguous about
which function it names.

## 5. What is not known

- [x] ~~**What the twelve mean in their own subsystems.**~~ **ANSWERED — `UD-1`, 2026-09-13, and
      the answer is in §8 of this page.** All twelve were read. Four closed as their own contracts:
      the screen-mode **aspect fit** `001DDAC0`, the **License Board change sweep** `0055B310`, and
      the two **authored-command ramp setters** `003B6950` / `003B69B0`. The remaining eight are
      tabulated in §8, with a fifteenth body `002ECD20` one hop past the fourteen through the thunk
      `0026DC50`.
      **This bullet said the opposite until 2026-09-14** — *"the purpose is not established for any
      of them"* — and it said so while §8 of the same page carried the reading. It also called
      `001DDAC0`'s two constants `16/9` and `16/3` *"suggestive and not a finding"*; they are the
      aspect-fit ratios, and `001DDAC0` is the screen-mode aspect fit. Corrected rather than
      quietly deleted, because the stale reading was cited from here.
- [x] **UQ-371.** **The 129 blocks called only from other unlisted code.** They form chains inside the
      residue and none has been read.
      *SUPERSEDED 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-1 ruling: a population-coverage statement; the population is carried by 99-Unresolved-Residual/Unlisted-Code/referenced-code-the-list-never-had.md. See the register row.*
- [x] ~~**The six blocks reached by a relocated pointer.**~~ **Followed 2026-09-13.** Four are
      **libvpx VP8 control handlers** whose only reference is a qword in the codec interface's control
      map - see [the VP8 codec interface page](../../23-Third-Party-Libraries/LibVPX-VP8-Decoder/the-vp8-codec-interface-and-its-control-map.md).
      `002FE7D0` was **already documented** as the `0x4021` wait handler and an independent decode agrees.
      **`004223F0` is read too**: slot 1 of the 14-entry dispatch table at `01F00398`, `xor edx,edx /
      jmp 004256E0` - the selector-**0** member of an adapter family whose siblings `00422400` and
      `00422410` pass 1 and 2 and **are** in the census. Only the one passing zero is missing, because
      its seven bytes are reached by nothing but the table slot. **All six accounted for.**
- [x] **UQ-372.** **Whether the owning pages should absorb these entries.** Routed, not done - the pages belong
      to other lanes.
      *NOT A QUESTION 2026-09-26 (FABLE, Claude Opus 5.5) under FRONTIER's class-2 ruling: the work is carried by the board task `FABLE-CARRIER-PAGE-OWNERSHIP-AND-PROPAGATION-0926`.*

## 6. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 143 referenced blocks, 6,038 bytes | the four reference forms intersected with the block list | 1 |
| fourteen have a listed caller, all reached by `jmp` | every call site decoded, caller resolved by containing body | 1 |
| the decoded behaviour of each of the fourteen | full disassembly; every rip-relative operand resolved | 1 |
| twelve are named nowhere in the database | literal search for each address across 537 documents | 1 |
| 29 listed bodies contain 49 others, 1,759 bytes | interval census over the function list | 1 |
| `001DDAC0` is an aspect fit | the constants are `16/9` and `16/3` and the record holds two scales - **inference** | 3 |

## 8. The remaining eight, read — and a fifteenth body

`UD-1` asked what the twelve unnamed bodies mean. Four were closed as their own contracts - the
[aspect fit](../../17-Presentation-Rendering/Screen-Mode-And-Aspect-Fit/the-aspect-fit-and-the-super-wide-bound.md),
the [License Board sweep](../../16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md),
and the two [ramp setters](../../17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md).
**These are the other eight**, and they are small enough that a page each would be worse than one
table.

### 8.1 A fifteenth body, one hop past the fourteen

Following the fourteen's own direct branches reaches **exactly one** further unlisted block:
**`002ECD20`, 41 bytes**, through the five-byte thunk `0026DC50`. So a documented caller
(`00350320` / `003505F0`) reaches unlisted code **two hops deep**, and the earlier "29 call sites
into unlisted blocks" understates the reachable set by one body.

**Nothing is reached at hop 2 or beyond.** The set closes at fifteen.

### 8.2 Two siblings behind one kind gate

`002EC3C0` and `002ECD20` open with the **same three instructions**:

```
movzx eax, byte ptr [rcx+3] / and al, 0xE0 / cmp al, 0x60
```

A kind test on the object's byte `+3`, top three bits, value `3`. `002EC3C0` then walks
`[rcx+0xB8]` → `+0xF0` and sets **bit 0 of that object's `+0x6A`** from `edx != 0`; `002ECD20`
takes the same gate after an extra `[rcx+0x18] == 1` test and walks `[rcx+0xC0]`. **Same kind, two
different sub-objects.**

### 8.3 The eight

| body | B | what it does |
|---|---:|---|
| `002EC3C0` | 43 | kind gate above; `[[rcx+0xB8]+0xF0]+0x6A` **bit 0** := `edx != 0` |
| `003594C0` | 27 | global byte `022C7FF8`: ~~**writes `cl` only if the byte is currently zero** - first-writer-wins~~ **writes `cl` only if the byte is non-zero** (`cmovne`, corrected 2026-09-18): the `changetosummonparty` verb (`0034ED30`, `ecx = 2`) upgrades a pending leader-change request to kind 2. Already named by [the party page](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) |
| `00269E00` | 24 | `[rcx+0x14]` **bit 5** := `dl & 1`; when `edx == 0`, tail-jumps `0025B500` |
| `003DE3E0` | 23 | global byte `02B58C3C` **bit 0** := `ecx != 0` |
| `00269F00` | 21 | `[rcx+0x08]` **bit 0** := `dl & 1`; same `0025B500` tail. Already named by [the movement-mode page](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md) |
| `0025D9C0` | 18 | loads global `02099D70`, passes `word [rcx]` and `[global+0x28]`, tail-jumps `00263A30` |
| `002697F0` | 10 | `edx := 1`, tail-jumps `00269860` - a **one-argument-fixed adapter** |
| `0026AF70` | 7 | global byte `02099DA0` := `cl`, unconditionally |
| `0026DC50` | 5 | `jmp 002ECD20` - the thunk of §8.1 |
| `0036E9A0` | 5 | `jmp 003B1560` |

*(Where the tails land, Pass 22 2026-09-14: the adapters' callees are **actor-entity** bodies —
`0025B500` is tail-called by `0025C830`/`00263050`, and `00263A30`/`00267420`/`00269860` forward
into `00358940` (10 edges); `00267420`/`00269860` also reach **scheduling** `0020E600` (2); and
`004256E0` calls **resource** `00409600`/`00409F50` (2). An adapter's callee *is* its target —
the edges name what is being forwarded to, not who owns the adapter.)*

### 8.4 The idiom they share, and why it is worth naming

Five of them are the same three-step shape:

```
and  byte ptr [x], ~(1 << k)      ; clear the bit
<compute a 0/1 from an argument>  ; and al,1  or  test/setne
or   byte ptr [x], value << k     ; put it back
```

**A boolean written into one bit of a byte, leaving the other seven alone.** `003DE3E0` and
`002EC3C0` use `test`/`setne` to make the 0/1; `00269E00` and `00269F00` use `and al, 1`, which
means **they take the low bit of the argument rather than its truthiness** - passing `2` clears the
bit where `setne` would have set it. That difference is invisible in prose that says "sets the
flag", and it is the kind of thing a reimplementation gets wrong once and never notices.

### 8.5 What is still not known

- [x] **UQ-373.** **What any of these flags mean.** Every entry above is a write, a mask and a position; **not
      one of them has a reader traced to it here.**
      ***ANSWERED 2026-09-18 (FABLE) — every flag writer of §8.3 is a script verb's tail, and each flag now has a reader-backed meaning.** The verb dispatch table names their thunks. `00269E00` is `001E enable` / `001F disable` (`00353630` / `00353A50`): `+0x14` bit 5 is the actor entry's script *enable* flag, read by seven pass sites that skip a clear entry (`0025C170` twice, `0025B250`, `0025B820` twice, `002675C0`, `003DF6F0`), and the disable side tail-jumps the entry removal `0025B500` — FRP-1, answered today on [the field-runtime contract](../../04-Actor-Entity/CONTRACT-field-runtime-pass.md). `00269F00` is `0020`/`0022` lineenable / rectenable and `0021`/`0023` linedisable / rectdisable (`00353D00` / `00354910`): `+0x08` bit 0, the line enable the line pass `0025B250` consumes ([the movement-mode page](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)). `002EC3C0` is `0435 lookat_maxvelr_limit_unlock` (`0034ED80`): bit 0 of `+0x6A` of the steering profile record at the movement context's `+0xF0` is a one-shot *velocity-limit unlock* — the steering-parameter writer `002EC3F0` folds the high mode 2 of `+0x62` to 1 when the bit is set and clears it (`002EC424`..`002EC433`, [the facing-and-steering contract](../../06-Movement-And-Navigation/CONTRACT-facing-and-steering.md) §18), and the context reset `00265FF0` clears it with bit 1 (`0026617B`, `00266201`); its sibling `002EC380`, called by twelve verb handlers and two movement functions, writes the three-bit mode into `+0x62` bits 3..5 and the frame count into the word `+0x60`. `003594C0` is `0205 changetosummonparty` (`0034ED30`, `ecx = 2`) and writes the party-focus request kind `022C7FF8` — **only when a request is already pending**: `test dl, dl` / `cmovne r8d, eax` (`003594C7`..`003594CF`) keeps the old value when the byte is 0, so it is an upgrade of a pending leader change to the summon-party variant (kind 2), not the first-writer-wins latch the rows above called it (corrected there today). `0026AF70` is `011C lock_charmotion_once`, the one-shot hold-keeper `02099DA0`, and `003DE3E0` is `03AC moveblurcaptureonce` (`00354950`), the unread bit at `02B58C3C` — the globals of UQ-375. Static: the dispatch table, the bodies, and image-wide `test` / `and` / `or` sweeps on each byte.*
- [x] **UQ-374.** **What kind `3` is** in the `(byte[+3] & 0xE0) == 0x60` gate, and what `[rcx+0xB8]` and
      `[rcx+0xC0]` point at.
      ***ANSWERED 2026-09-18 (FABLE).** The gate reads the packed byte `+0x03` of the actor storage record: its low five bits are the row index into the eight-row kind table at `01E0C328` and its top three bits are that row's *kind* field, as [the actor-record page](../../04-Actor-Entity/Actor-Storage-Record/the-record-behind-every-actor.md) derives from the initialiser's presets (`00266BD0`, jump table `00266C30`); `0x60` is kind 3, which rows 5, 6 and 7 carry, the three largest records (1,760, 1,760 and 1,640 bytes), the actors that have a movement body and a render record at all. `[rcx+0xB8]` is that movement body: the position re-place `002E5C90` writes the point at its `+0`..`+8`, adds the attachment offset `+0x40`..`+0x48` when its `+0x107` bit 1 is set, and the render-side setter `002E6000` reads the same `+0`..`+8` back. `[rcx+0xC0]` is the character render record: its word `+0` indexes the array `022C6F28` by `0x740`, `+0x138` holds the transform node the position is pushed into (`003DB1B0` writes `node+0x30`), `+0x14F` bit 0 gates every presentation write, and `+0x284` non-zero marks a live LOD record ([the party-looks page](../../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/how-a-script-changes-how-the-party-looks.md), read 2026-09-18). Static, from the bodies and the kind table.*
      **Corrected 2026-09-18 (FABLE), the same day: the two pointers carry the context census's names, not the ones first written here.* The initialiser plants `[+0xB8] = record + 0x120`, the 0x230-byte **movement context** (`00266B2D`, `00266B4B`), and `[+0xC0]` the **secondary context** (`00266B1F`, `00266B40`), as [the context census](../../04-Actor-Entity/Actor-Contexts/the-movement-and-secondary-context-censuses.md) has them; so `[rcx+0xB8]` is the movement context (position at `+0`, the attachment offset `+0x40`..`+0x48` under `+0x107` bit 1, the steering profile pointer at `+0xF0`), not “the movement body” — the body is the pooled record the secondary context's `+0x138` points to (`002E508A`), the one `003DB1B0` writes at `+0x30`; and `[rcx+0xC0]` is the secondary context (word `+0` the render-record id into `022C6F28 × 0x740`, `+0x138` the body, `+0x14F` bit 0 the presentation gate), while `+0x284` belongs to the 0x740-byte render record itself, not to this pointer. The kind reading stands.*
- [x] **UQ-375.** **The three globals** `022C7FF8`, `02B58C3C`, `02099DA0` and the pointer `02099D70`.
      *Narrowed 2026-09-15 (OPUS) — shapes measured for all four; the box stays open because a
      reference census gives shape, not meaning. Whole-image census, control `02098E10` returning
      **61** references so absence is meaningful.*
      - **`02B58C3C` has NO references anywhere in the image — that quarter is closed.** Not read,
        not written, and no instruction takes its address, so nothing can reach it another way.
      - **`02099D70` is a pointer saved and restored around a scope** — **50 references in 20
        functions**, almost all the same triple: load the old value, install a new one, restore the
        old one (`0025AFC6`/`0025AFE1`/`0025B055`, `002623AA`/`002623C5`/`002623E4`,
        `00263146`/`0026314D`/`00263167`, and so on). That is a *current-item* pointer with strict
        nesting, not a container.
      - **`02099DA0` is a byte flag** — 7 references in 4 functions: tested against `0` at
        `0025AFFB` and `00261FDA`, cleared at `0025B02F`, and written **and** compared from the same
        boolean register inside `002628B0` (`00262D4B`, `00262D63`, `00262D8F`). It sits in the same
        cluster as `02099DB8`, the system-stop total (`UQ-376`).
      - **`022C7FF8` is a mode byte gating a transition, and `2` is a distinct mode.** `00358BC0`
        **returns immediately when it is `0`** (`00358BC4`); otherwise it compares `[022C7FE0]`
        (current) against `[022C7FE4]` (requested) and, when they differ, drives the change — and
        at `00358C05` a value of **`2`** routes completion to `0025A690` instead of `0025A680`.
        Also written `0` at `00358C35`, a computed byte at `00359109`, and `1` at `003594B6`, so it
        takes at least `0`, `1` and `2`. **What the transition is** is the part still open.
      ***ANSWERED 2026-09-18 (FABLE) — all four have a meaning, and one consult of the byte is dead code.** `02099D70` is the bound `ActorManagerSlot` pointer (`02098E10 + slot × 0x288`), the scoped *current manager* [the actor-manager page](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md) (FH-3) and [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) document: the bind publishes it at `0026C911` and twelve functions save, bind and restore it. `022C7FF8` is the party-focus *request kind* [the party page](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) tables beside `022C7FE0` / `022C7FE4` (0 nothing pending, 1 a leader change requested by `PartyFocus_RequestPackedActorHandle`, 2 the variant whose old-leader teardown goes to `0025A690`): the transition is the leader change, committed when `PartyFocus_CommitPendingPackedActorHandle` copies `022C7FE4` into `022C7FE0` and writes the kind back to 0. `02099DA0` is the one-shot byte behind script verb `011C` `lock_charmotion_once`: the verb's handler `0034D350` is `mov ecx, 1; jmp 0026AF70`, and `0026AF70` is the unlisted seven-byte store above, the only non-zero writer in the image (the boot slot reset `00266D10` stores 0 at `00266DF7`, `esi` cleared at `00266D3E`; every other write is 0). Three unload-side paths consult it: when it is 0 they call `002E4000(slot, 1)` and `002E3E20(slot, 1)`, which walk the resource records under `0215FD68` and the name bindings under `0215FD58` ([the naming page](../../01-Script-VM-Native-Bridge/how-a-script-names-a-thing-in-the-world.md)) and drop the slot's bit from each record's holder masks (the dword `+0x48 + 4 × slot` per selector, the word `+0x20`), releasing a record whose masks empty (`002EAEB0`; the `0215FD90` list); when it is 1 those holds survive, the slot's bound resources kept once. The definition-payload arm `0025AFC0` (slot 0) consults it at `0025AFFB` and clears it at `0025B02F`; the field-runtime record step `00261F90` (called per record by `ActorManager_RunFieldRuntimePass`) consults it at `00261FDA` and leaves it; the manager-slot unload `002628B0` consults it at `00262D63` but that consult is dead: it first calls `005C5230`, which is `xor eax, eax; ret`, and on that constant zero stores 0 into the byte (`00262D4B`) before the compare, then stores 0 again at `00262D8F`. So the verb's hold is honoured by the payload arm and the record step, never by a slot unload. `02B58C3C` stays what the 2026-09-16 trace found: bit 0 of the second float of the three-float vector at `02B58C38` (`003DE160` copies the twelve bytes), written by `003DE3E0` and read by nothing; a name is not derivable from a write nothing reads, and the quarter closes as that: an unread bit in a vector component. Static: the bodies, the verb dispatch table ([`scriptvm-dispatch.tsv`](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-dispatch.tsv) row `011C`) and the image-wide reference sweeps.*
      **Refined 2026-09-18 (FABLE): kind 2 is written by the `changetosummonparty` verb (`0034ED30`: `ecx = 2` into `003594C0`), and that setter stores only when a request is already pending (`cmovne`, `003594CF`), so 2 is a pending leader change upgraded to the summon-party variant; the “writes only if zero” wording of §8.3 was inverted and is corrected there.**
- [x] **UQ-376 ANSWERED 2026-09-15 (OPUS) — they are not “zero” cases. They are the
      *clear* half of a set/clear pair, and clearing a stop flag has to release it.**
      `0025B500` (125 B) is **system-stop registry index 18's release side**, which
      [the-time-stop-and-system-stop-registry.md](../../00-Engine-Core-Runtime/System-Stop-Registry/the-time-stop-and-system-stop-registry.md)
      already lists opposite `0025C830`. Its body, read here:
      - **It is idempotent by construction.** It returns immediately unless `[rcx+0xC] & 0x40` is
        set, and clears that bit first (`0025B504`–`0025B50E`) — so a second release does nothing.
      - **It decrements a per-actor-manager counter:** `[02098E10 + [rcx+0x15]*0x288 + 0x1E4] -= 1`
        (`0025B511`–`0025B523`). `02098E10` stride `0x288` is the **actor-manager slot array** the
        [world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)
        documents, and `[rcx+0x15]` is the slot index.
      - **Then it re-folds the three global stop flags and republishes the total:** `eax = 0`;
        `if ([02098E20] & 1) eax = [02098FF4]`; `if ([020990A8] & 1) eax += [0209927C]`;
        `if ([02099330] & 1) eax += [02099504]`; `[02099DB8] = eax` (`0025B52A`–`0025B558`).
      - **And only if the total has fallen to `<= 0`** does it call `00226100` and tail-jump to
        `002E1CD0` with `ecx = 1`, `edx = 0xD` (`0025B55E`–`0025B573`) — the *last holder released*
        path. Otherwise it just returns.
      **So the asymmetry is the point, not an oddity:** setting the bit is a state write and nothing
      more; clearing it must give back a stop count and, if nobody else is holding one, resume.
      - ⚠ **A latent mismatch, measured and found harmless.** The branch is `test edx, edx` — the
        **whole** argument — while the bit stored is `edx & 1`. An **even non-zero** argument (`2`,
        `4`, …) would therefore clear the stored bit **without** performing the release, leaving the
        flag and the count disagreeing. **No shipped caller can do that:** all four callers are
        8-byte thunks passing a literal `0` or `1` — `00353630` → `00269E00(1)` and `00353A50` →
        `00269E00(0)`; `00353D00` → `00269F00(1)` and `00354910` → `00269F00(0)` — two clean
        set/clear pairs. The hazard is real in the code and unreachable in this image. **UQ-376.**

## 9. Related

- [`the-code-the-function-list-does-not-contain.md`](the-code-the-function-list-does-not-contain.md) - the 244,619 bytes this population is drawn from
- [`../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md`](../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md) - the one page that read through a tail jump on its own
- [`../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md`](../../11-Party/active-party-reserve-and-the-moment-the-leader-changes.md) - names `003594C0`
- [`referenced-unlisted-blocks.tsv`](referenced-unlisted-blocks.tsv) - all 143 with their reference forms

*(Pass 22 live-graph completion, 2026-09-15: the adapters' tails keep landing out-of-folder —
`0025C830`/`00263050`/`00267420`/`00269860` also call `CoreRuntimeScheduling` `0020E600` (4);
`00358940` is called by `World` `002623A0`/`0025E400` and `Input` `00226BE0` (3); `0025C830`
calls `WorldAreaField` `00377C20` (1). An adapter census records where forwards land; these
land in the scheduling, world and input layers.)*

*(Pass 22 live-graph sweep 2, 2026-09-15: the adapter targets' callers spread wider —
`00377C20` is called by `CombatAI` (`003014C0`, `00301AD0`, 3), `CombatAction` (18 edges,
largest fan-in on this page), `CombatFormula` `00300530` (1), `Gameplay` (`00307D10`,
`0030C210`, 4) and `Rewards_Progression_Economy` `00312280` (1); `00226BE0` is called by
`CombatAction` `00313DB0`. The field-adapter target sits under the combat stack — where the
calls come from, not who owns the target.)*

*(Pass 22 live-graph sweep 3, 2026-09-15: the combat callers' own callees — `00313DB0` calls
`Audio` `002DEE70`, `00312280` calls `Platform_Online_Achievements` `00316A50`, `00300530` calls
`Spawn_Encounter_Lifecycle` `00306F00` (3 edges). The fan-in keeps resolving into the same shared
accessor populations.)*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — CLIENT and SERVICE, 35 edges.** Cited functions are called by Presentation bodies of 963 to 4,782 bytes and by `BattleUnit_ComputePartyBattleStance`. They call Presentation bodies (53 to 1,662 bytes), `BattleUnit_TestActorViewFrustumAtCurrentPosition` and `Reward_PublishExpLpPresentation`.
- **Status_Periodic_Terminal — CLIENT and SERVICE.** Cited functions are called by `BattleStats_ChangeStatusAndProcessSideEffects` (3), `BattleStats_RemoveStatusesFromMaskAndRecompute` and `BattleUnit_RunPeriodicCombatMaintenance`, and one calls `BattleStats_ChangeStatusAndProcessSideEffects`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Save_Load_Settings — SERVICE.** `001DDBA0` on this page calls `GameSettingConfig_WriteFile`, owned by that layer. What it reaches is the settings writer: it builds a path from its argument's `+0x450`, opens it through the CRT import at `008C2E00`, and does nothing at all when that fails; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).


### The readers, traced (FABLE, 2026-09-16)

**TRACED 2026-09-16 (FABLE) - two of the three global flags have readers, and the third has something better than a reader.** The negative was scoped - *traced to it **here***, meaning the page did not look - so looking is the whole job. Three of the eight write a **named global**, which makes their readers directly censusable. **`022C7FF8` - read, and it is a three-state handshake.** `PartyFocus_CommitPendingPackedActorHandle` tests it **twice**: `cmp byte, 0` at `00358BC4` and `cmp byte, 2` at `00358C05`, then clears it to 0 at `00358C35`. `PartyFocus_RequestPackedActorHandle` writes **1** at `003594B6` - that is `003594C0`'s first-writer-wins site - and `PartyFocus_ResetState` writes `al` at `00359109`. **So the flag is request(1) / something(2) / idle(0) between three named Party functions**, not an untraced write. **`02099DA0` - three readers, and one crosses a layer.** `cmp byte, 0` at `0025AFFB` (`FUN_0025AFC0`, ActorEntity), at `00261FDA` (`FUN_00261F90`, **Audio**) and at `00262D63` (`FUN_002628B0`, ActorEntity); four writers including `00266DF7`. **An ActorEntity flag that Audio consults** is worth more than the write that set it. **`02B58C3C` - the negative HOLDS, and the reason is structural.** No reader tests its bit. But it is **not a standalone byte**: `FUN_003DE160` copies **twelve bytes** starting at `02B58C38` onto its stack - `movsd xmm0, qword ptr [02B58C38]` at `003DE177` and `mov eax, dword ptr [02B58C40]` at `003DE183` - which is the shape of a **three-float vector** at `+0`, `+4`, `+8`. **`02B58C3C` is the second float.** And `003DE3E0` is confirmed byte-exact: `movzx eax, byte ptr [02B58C3C]` / `setne cl` / `and al, 0xFE` / `or cl, al` / store - **it writes bit 0 of that float's low byte.** **So the *flag* is the least significant bit of a float's mantissa.** That is a real technique - it perturbs the value by one ULP and nothing notices - but it is unusual enough that I am **flagging the overlap rather than asserting the intent**. Either the byte reading is right and someone is stuffing a boolean into a vector component, or the two uses are a union and one of them is misattributed. **Nothing reads the bit back, so the image does not say which.** *Scope.* Only the three flags that write a **global** are traced. The object-field flags - `002EC3C0`'s `[[rcx+0xB8]+0xF0]+0x6A` bit 0, `00269E00`'s `[rcx+0x14]` bit 5, `00269F00`'s `[rcx+0x08]` bit 0 - need the object type first and are untouched here. **The row's negative is falsified, not discharged.**

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

**Every citation on this page is a referrer or neighbour of code the function list never had, so the layers below
arrive with those bodies' ordinary call graphs. None of them is a claim this page makes about the layer.** The
residue this page owns is the unlisted code itself (`UQ-371` to `UQ-375`).

**Script_VM_Native_Bridge — CLIENT, 55 edges.**
- `ActorManager_GetRecordByOrdinal` (`00358940`) is read by 17 script bodies, among them
  `WorldActorScriptVM_InterpretBytecode`, `VMNativeCommand_ExecuteLifecycle` and the `ScriptVM_WaitList_*` probes.
- Script handlers also call `002EC380` (12), `00263A30` (8), `002E1CD0` (4), the field flag (4), `002673D0`,
  `002E3E20`, `002E4000`, `0025B500` and `002DEE70`.
- The area initialiser `00266D10` calls `VMNativeCommandDispatch_InitializeFamilyTables`.

**Movement — BOTH DIRECTIONS, 45 edges.**
- The area unload `002628B0` and initialiser `00266D10` call movement bodies (`00263560`, `0026A1D0`, `00379070`,
  `003791C0`, `002EBE40`, `003DAE30`).
- `00265FF0` sets `Movement_SetRequestedSpeed` and the `003DA830`-`003DA890` family.
- The movement bodies `002E28E0`, `002E3110`, `002E64E0` and `002EAAA0` call `002EC3F0`. `002E5C90` / `002E6000` /
  `003DB1B0` sit inside the locomotion call graph.
- `WorldActor_UpdateRuntimeAndScriptExecutionState` asks `ScriptVM_WaitList_HasAnyActorChannelActive`.

**WorldAreaField and World — CLIENT, 27 edges.**
- The area initialiser `00266D10` calls `BattleSystem_InitializeAreaState`, `MapRef_BeginLoadResources`,
  `WorldField_InitializeCurrentFieldRuntimeParameters` and `WorldPersistence_ResetBanksForFieldTransition`.
- The area unload calls `00378230`, `003DFA50` and `003EAA00`.
- `World_UpdateSimulationTick` calls `002623A0`.
- `FieldData_GetActiveFieldRecordBit15` is read by the battle bodies this page cites: the target selector, the lethal
  transition, `BattleUnit_UpdateEngagementStateFlag` and `BattleUnit_ProcessDefeatRewardsAndLoot`.

**Party — BOTH DIRECTIONS, 18 edges.** The focus-handle family links the cited bodies to the party layer:
- `PartyFocus_CommitPendingPackedActorHandle`, `PartyFocus_SetSecondaryPackedActorHandle` and
  `PartyRoster_AssignActorAndCommitFocusWhenEligible` call `0025A680` / `0025A690`;
- `00226BE0`, `0025E400`, `002623A0` and `00263050` read `PartyFocus_GetCurrentPackedActorHandle`;
- the area unload calls `PartyFocus_ClearCurrentActorIfEligible` and `PartyControl_SetMovementSuppressionBit`.

**Input, InputGameplay, UI, Items_Equipment_Shops_License and RNG_Random_Selection — MECHANICAL, 17 edges.**
- The area bodies call the input-filed `0035B5D0` and `00226BE0`.
- `InputGameplay_ArbitrateDigitalInputAndModalState` and `00313A00` read the field flag.
- The licence-board body `0055BFF0` calls four UI bodies and `BattleStats_CheckLicenseNodeAcquireReasonByStatsIndex`.
- The inventory and equipment bodies read the field flag.
- The action-target resolver draws the shared generator.

*Tier 2: ledger names, sizes and `edges.tsv`; no new body read (OPUS, 2026-09-29, pass-22 debt `42a617a9a`).*

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-referenced-code-the-list-never-had-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00263A30` | 109 B | returns the string "NOACTOR" (`00915708`) unless `ecx` is at most 4 (unsigned), bit 0 of byte `+0x10` of the `0x288`-byte record `ecx` at `02098E10` is set, that record's qword `+0` is non-null, `edx` is below its dword `+0x20` (signed), and `00358940(record, edx)` returns non-null with a non-null qword `+0x40`; then it returns that qword `+0` plus its dword `+0x4C` plus the sign-extended dword the `+0x40` qword points at | `00263A3D`, `00263A58`, `00263A6B`, `00263A70`, `00263A8C` |
| `0034ED80` | 56 B | tail-jumps to `002EC3C0` with `rcx` = the incoming `rdx` and `edx` = 1 | `0034ED83`, `0034ED88` |
| `00350320` | 56 B | tail-jumps to `0026DC50` with `rcx` = the incoming `rdx` and `edx` = 0 | `00350323`, `00350325` |
| `00354950` | 33 B | sets `ecx` to 1 at the entry and tail-jumps to `003DE3E0` | `00354955` |

## 53 UC-1 game-code bodies explained by interior citation (OPUS, 2026-10-02)

*These 53 bodies were admitted to the F frontier on 2026-09-28 by the UC-1 band (decoded code the function list never had) and are reached from game code, so no library span can take them. Under FABLE's route ruling each is explained by an interior citation instead: the row first states how the body is entered (a call or jump site, or no reference found and what the start follows), then what the body does (access and representation, not purpose), and ends with the series-break phrase. Drafted by an agent that is not OPUS and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-referenced-code-the-list-never-had-uc1-1002/interior_applier.py): every anchor is an instruction boundary inside its body and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00125743` | 16 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after a `ret` and is not 16-byte aligned; it reserves 8 bytes of stack, stores the incoming `rcx` to `[rsp]`, loads the x87 control word from that slot's low word with `fldcw`, releases the slot and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00125747`, `0012574B`, `0012574E` |
| `00125753` | 17 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after a `ret` and is not 16-byte aligned; it reserves 8 bytes of stack, executes `wait`, stores the x87 control word to the low word of `[rsp]` with `fnstcw`, loads the qword at `[rsp]` into `rax` (its upper six bytes are not written by the body), releases the slot and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00125757`, `00125758`, `0012575B` |
| `00195340` | 21 B | entered through the 32-bit image-relative destructor field at `01DEAAA4` of the C++ throw-info record for `std::bad_cast` at `01DEAAA0`; it starts right after `int3` padding; it stores the address `008F35E8` to qword `+0x0` of `rcx`, advances `rcx` by 8 and tail-jumps through the qword at `008C2A28` with the other registers incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00195347`, `0019534A`, `0019534E` |
| `001DDAC0` | 223 B | entered from `001DDBA0` + 0x99; it stores `edx` to dword `+0x10` and `r8d` to dword `+0x14` of `rcx` and forms the f32 ratio `edx` / `r8d` (both zero-extended); when the ratio is at or below f32 1.777778 (`008C5B38`) it stores f32 1.0 to `+0x4` and `+0x8`, 0 to `+0xC` and `+0x0` and the truncated `edx` / 1.777778 to `+0x14`; when it is above f32 5.333333 (`00900A0C`) it stores f32 1.0 to `+0x4` and `+0x8`, 0 to `+0xC`, `r8d` to `+0x14`, 1 to `+0x0` and the truncated `r8d` * 5.333333 to `+0x10`; otherwise (`001DDB53`) it stores `r8d` to `+0x14`, 1 to `+0x0`, the f32 of `edx` minus the unsigned quotient `r8d` / `edx` to `+0x4` and the f32 of the unsigned quotient (`edx` - `r8d`) / `edx` times f32 0.5 (`01CEBB70`) to `+0xC`; it returns on every path; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `001DDAD7`, `001DDAF0`, `001DDB21`, `001DDB63`, `001DDB98` |
| `0025D9C0` | 18 B | entered from `0034C880` + 0x3; it reads the qword at `02099D70`, sets `edx` to the zero-extended word at `[rcx]` and `ecx` to dword `+0x28` of that qword's target, and tail-jumps to `00263A30` with the other registers incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0025D9C7`, `0025D9CA`, `0025D9CD` |
| `002697F0` | 10 B | entered from `0050E390` + 0x3; it sets `edx` to 1 and tail-jumps to `00269860` with the other registers incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002697F5` |
| `00269E00` | 24 B | entered from `00353630` + 0x8 and `00353A50` + 0x5; it clears bit `0x20` of byte `+0x14` of `rcx` and ORs in bit `0x1` of `dl` shifted up to bit `0x20`; when `edx` is zero it tail-jumps (conditional `je`) to `0025B500` with `rcx` and `edx` as incoming (`eax` holds the shifted bit), otherwise it returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00269E04`, `00269E0C`, `00269E11` |
| `00269F00` | 21 B | entered from `00353D00` + 0x8 and `00354910` + 0x5; it clears bit `0x1` of byte `+0x8` of `rcx` and ORs in bit `0x1` of `dl`; when `edx` is zero it tail-jumps (conditional `je`) to `0025B500` with `rcx` and `edx` as incoming (`eax` holds the masked bit), otherwise it returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00269F04`, `00269F09`, `00269F0E` |
| `0026AF70` | 7 B | entered from `0034D350` + 0x5; it stores the incoming `cl` to byte `02099DA0` and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0026AF76` |
| `002969D0` | 12 B | entered by a conditional jump (`jne`) from `002905B0` + 0x13; it starts right after `int3` padding; when `rcx` is non-null it stores `dl` to byte `+0xB43` of `rcx`; it returns on both paths; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002969D3`, `002969D5` |
| `002E4C90` | 70 B | entered by a conditional jump (`je`) from `002673D0` + 0xD; it starts right after `int3` padding; it returns 1 in `eax` when `rcx` is null, when qword `+0xC0` of `rcx` is null, when the dword it points to is -1, when that dword's low word is -1, when that word sign-extended times 0x740 plus qword `022C6F28` is zero, or when dword `+0x284` of that entry is zero; otherwise it tail-jumps (conditional `jne`) to `004232D0` with `rcx` = the entry address, `rax` = the sign-extended word and `rdx`, `r8`, `r9` incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002E4C95`, `002E4CB3`, `002E4CBA`, `002E4CC3`, `002E4CCA` |
| `002E5B00` | 96 B | entered by a conditional jump (`je`) from `0026A420` + 0x8; it starts right after `int3` padding; it returns when `rcx` is null, when qword `+0xC0` of `rcx` is null, when the dword that block starts with is -1, or when qword `+0x138` of the block (loaded into `rdx`) is null; when bit `0x10` of byte `+0x151` of the block is clear it tail-jumps to `002ED6A0` with `rcx` incoming, `rax` = the block and `rdx` = that qword; when the bit is set it stores the f32 stack argument at `[rsp+0x28]` to `+0x5C` and `+0x6C`, `xmm1` to `+0x50` and `+0x60`, `xmm2` to `+0x54` and `+0x64` and `xmm3` to `+0x58` and `+0x68` of the `rdx` target and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002E5B16`, `002E5B22`, `002E5B31`, `002E5B5A` |
| `002EB5D0` | 11 B | entered from `0037C3F0` + 0x1F8; it zeroes `r9d` and `r8d` and tail-jumps to `002EB5E0` with `rcx` and `rdx` incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002EB5D3`, `002EB5D6` |
| `002EBD40` | 19 B | entered from `0037C3F0` + 0x150; when `rcx` is non-null it clears bit `0x10` of byte `+0x19` of `rcx` and ORs in bit `0x1` of `dl` shifted up to bit `0x10`; it returns on both paths; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002EBD43`, `002EBD45`, `002EBD4F` |
| `002EC3C0` | 43 B | entered from `0034ED80` + 0x8; when byte `+0x3` of `rcx` masked with 0xE0 equals 0x60 it loads qword `+0xB8` of `rcx`, then qword `+0xF0` of that target into `r8`, and rewrites byte `+0x6A` of the `r8` target with bit `0x1` set when `edx` is non-zero and cleared otherwise (other bits kept); otherwise it returns without a write; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002EC3C6`, `002EC3CA`, `002EC3D6`, `002EC3E6` |
| `002ECD20` | 41 B | entered by a jump from `0026DC50` + 0x0; it returns when byte `+0x18` of `rcx` equals 1 or when byte `+0x3` masked with 0xE0 is not 0x60; otherwise it loads qword `+0xC0` of `rcx` into `rax`, clears bit `0x2` of byte `+0x11` of that target and ORs in bit `0x1` of `dl` shifted up to bit `0x2`, then tail-jumps to `002E8FD0` with `rcx` incoming and `dl` holding the shifted bit; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002ECD24`, `002ECD2C`, `002ECD30`, `002ECD40`, `002ECD43` |
| `002ED250` | 68 B | entered by a conditional jump (`jge`) from `003EB8C0` + 0xC; it starts right after a `ret`; it returns when `rcx` is null, when dword `[rcx]` is -1 or when word `[rcx]` is -1; it forms the entry address as that word sign-extended times 0x740 plus qword `022C6F28` and returns when that sum is zero or dword `+0x284` of the entry is zero; otherwise it clears bit `0x10` of byte `+0xD2` of the entry and sets it again when `edx` is non-zero (`neg`/`sbb`), then returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002ED267`, `002ED26E`, `002ED277`, `002ED280`, `002ED28D` |
| `002ED350` | 76 B | entered by a conditional jump (`jge`) from `003EB960` + 0xC; it starts right after `int3` padding; it returns when `rcx` is null, when dword `[rcx]` is -1 or when word `[rcx]` is -1; it forms the entry address as that word sign-extended times 0x740 plus qword `022C6F28` and returns when that sum is zero or dword `+0x284` of the entry is zero; otherwise it clears bit `0x8` of dword `+0x304` of the entry and sets it again when `edx` is non-zero (`neg`/`sbb`), ORs bit `0x40` into dword `+0x290` and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002ED36E`, `002ED377`, `002ED380`, `002ED38E`, `002ED394` |
| `002FE7D0` | 106 B | entered through the qword table entry at `01EEC568`; it loads qword `+0x708` of `rcx` into `r8` and switches on byte `+0x6B4`: for a value other than 0 or 1 it returns 1; for 0 it stores 0 to qword `+0x750`, sets byte `+0x6B4` to 1 and continues as for 1; for 1 it returns 0 when word `+0x2` of the `r8` target is zero, otherwise it compares dword `+0x75C` (signed) with the truncated f32 product of the f32 at `01DFE0B8` (1.0 in the image; writable data) and `008F8D80` (30.0) times that sign-extended word, returning 0 when below and otherwise incrementing byte `+0x6B4` and returning 1; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `002FE7DA`, `002FE7F4`, `002FE801`, `002FE823`, `002FE82B` |
| `0031AD90` | 17 B | entered by a conditional jump (`jne`) from `00359B80` + 0xC; it starts right after a `ret`; it returns in `rax` the incoming `rcx` plus 0xED0, or 0 when `rcx` is null (`cmove`); UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0031AD92`, `0031AD9C` |
| `003594C0` | 27 B | entered from `0034ED30` + 0x5; it reads byte `022C7FF8` and, when it is non-zero, stores the incoming `cl` to it, otherwise stores the read value (zero) back; it returns with `eax` = the zero-extended `cl`; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003594C7`, `003594CF`, `003594D3` |
| `00365660` | 55 B | entered by a conditional jump (`jg`) from `0029CCF0` + 0x5; it starts right after `int3` padding; when `edx` (signed) is below 8 it returns 0; otherwise it stores the bytes 0x65, 0x78, 0x30, 0x30 to `+0x0` of `rcx`, word 0x2B to `+0x4` when `r8d` is non-zero or word 0x2D when it is zero, word 0 to `+0x6`, and returns 8; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00365663`, `00365668`, `00365673`, `00365685` |
| `00379F50` | 18 B | entered by a conditional jump (`jne`) from `00379860` + 0x8; it starts right after `int3` padding; when `ecx` - 1 is at most 2 unsigned (`ecx` 1 to 3) it stores `ecx` - 1 to dword `02EBF408`; it returns on both paths; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00379F53`, `00379F5B` |
| `0037AA00` | 69 B | entered by a conditional jump (`jne`) from `003DEA10` + 0x2; it starts right after `int3` padding; it forms `r8` = `02EBF420` + sign-extended `ecx` times 0x50 and loads qword `+0x18` of it; when that qword is null or dword `+0x4` of its target is zero it returns; otherwise for each index i from 0 while i is below dword `+0x4` (re-read through qword `+0x18` every pass) it stores byte 1 at `+0x12` + i*8 of the target, then returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0037AA07`, `0037AA15`, `0037AA30`, `0037AA3F` |
| `003B6950` | 83 B | entered from `004174D0` + 0x17; it forms `r9` = qword `02B40528` + zero-extended `cl` times 0xE0 and returns when dword `+0x10` of that entry differs from `ecx`; when `dl` is non-zero it stores `dl` to byte `+0x3` and stores (`xmm2` - f32 `+0x78`) times (f32 1.0 from `01CEBBA8` divided by `dl`) to f32 `+0x7C`; when `dl` is zero it stores `xmm2` to f32 `+0x78` and 0 to byte `+0x3`; it returns on every path; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003B695B`, `003B6962`, `003B697D`, `003B6990`, `003B6997` |
| `003B69B0` | 83 B | entered from `00417440` + 0x17; it forms `r9` = qword `02B40528` + zero-extended `cl` times 0xE0 and returns when dword `+0x10` of that entry differs from `ecx`; when `dl` is non-zero it stores `dl` to byte `+0x1` and stores (`xmm2` - f32 `+0x70`) times (f32 1.0 from `01CEBBA8` divided by `dl`) to f32 `+0x74`; when `dl` is zero it stores `xmm2` to f32 `+0x70` and 0 to byte `+0x1`; it returns on every path; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003B69BB`, `003B69C2`, `003B69DD`, `003B69F0`, `003B69F7` |
| `003DCF20` | 51 B | entered by a conditional jump (`je`) from `003DC780` + 0x43; it starts right after `int3` padding; when byte `+0x6` of `rcx` equals 3 and word `+0x4` is zero it adds 0x10 to dword `+0x8`, sets byte `+0x6` to 4, stores 1 to dword `02B58170` and, when dword `+0x8` masked with 0xFFFF0 is then zero, stores the zero-extended byte `+0x13` ORed with 0x10 to dword `+0x8`; otherwise it returns without a write; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003DCF2D`, `003DCF31`, `003DCF3C`, `003DCF4F` |
| `003DE3E0` | 23 B | entered from `00354950` + 0x5; it rewrites byte `02B58C3C` with bit `0x1` set when `ecx` is non-zero and cleared otherwise, other bits kept, and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003DE3E9`, `003DE3EC`, `003DE3F0` |
| `003F5030` | 52 B | entered by a conditional jump (`jne`) from `00290BE0` + 0x16; it starts right after a `ret`; when `rcx` is non-null it walks the list linked through qword `+0x868` and for each node clears bit `0x2` of word `+0x842`, stores 0 to dword `+0x83C` and word 5 to `+0x850`; it returns when the link is null or `rcx` was null; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003F5042`, `003F5049`, `003F504F`, `003F5057` |
| `003F7000` | 79 B | entered by a conditional jump (`jne`) from `00290940` + 0x13; it starts right after `int3` padding; when `rcx` is non-null it walks the list linked through qword `+0x300` and, for each node whose dword `+0x2D0` equals `edx` and whose word `+0x2F0` has any bit other than `0x4` set, stores word 4 to `+0x2F0` when it was 1 and word 3 otherwise; it returns when the link is null or `rcx` was null; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `003F7015`, `003F7024`, `003F7030`, `003F703A`, `003F7042` |
| `004223F0` | 7 B | entered through the qword table entry at `01F003A0`; it zeroes `edx` and tail-jumps to `004256E0` with the other registers incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `004223F2` |
| `004278D0` | 11 B | entered by a conditional jump (`jne`) from `002EB4A0` + 0x3A; it starts right after `int3` padding; it ORs bit `0x2000` into dword `+0x294` of `rcx` and returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `004278DA` |
| `0042FCC0` | 18 B | entered by a conditional jump (`ja`) from `00317EC0` + 0x6; it starts right after `int3` padding; when `ecx` is zero it returns 0; otherwise it increments dword `02CA4ED8` and tail-jumps to `002FCB60` with the incoming registers; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0042FCC2`, `0042FCC7`, `0042FCCD` |
| `0055B310` | 209 B | entered from `0055BFF0` + 0x463; with `r10d` = 0 it clears byte `+0x408` of `rcx` when bit `0x1` of dword `+0x570` is set, then for each row below signed byte `+0x55A` and each column below signed byte `+0x559` takes the 0x38-byte element at qword `+0x120` + (row times byte `+0x559` + column) * 0x38 and, when bits `0xF0` of its dword `+0x18` differ from its bits `0xF00` shifted down 4, sets `r10d` = 1 and either (bit `0x1` of `+0x570` set) stores the element address into the qword array at `+0x308` indexed by byte `+0x408` and increments that byte while it is below 0x20 (signed), or (bit clear) copies bits `0xF0` of dword `+0x18` up into bits `0xF00`; finally it clears bit `0x1` of dword `+0x570` and returns `r10d`; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0055B313`, `0055B36C`, `0055B388`, `0055B3A6`, `0055B3D6` |
| `00710000` | 73 B | entered from `006DE0D0` + 0x7; it copies the 64 bytes at `r8` to `rcx` + 0x7A4 + sign-extended `edx` times 0x40, stores byte 1 at `rcx` + `edx` + 0x924 and returns 0; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0071000E`, `00710035`, `0071003D`, `00710046` |
| `00710050` | 61 B | entered from `006DE0F0` + 0x7; it copies the 64 bytes at `rcx` + 0x7A4 + sign-extended `edx` times 0x40 to `r8` and returns 0; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0071005F`, `00710085`, `00710087` |
| `008824F0` | 98 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it rotates `ecx` by 16 and then swaps bytes, nibbles, bit pairs and single bits with mask-and-shift steps (masks 0xFF00FF, 0xF0F0F0F and the alternating 2-bit and 1-bit masks), returning in `eax` the incoming `ecx` with its 32 bits in reversed order; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00882502`, `00882519`, `00882536`, `0088254A`, `0088254F` |
| `008832D0` | 13 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it returns in `eax` the number of right shifts by 1 that bring `ecx` to zero (0 when `ecx` is zero), the count of bits up to and including the highest set bit; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008832D6`, `008832D8`, `008832DA` |
| `00884090` | 98 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it rotates `ecx` by 16 and then swaps bytes, nibbles, bit pairs and single bits with mask-and-shift steps (masks 0xFF00FF, 0xF0F0F0F and the alternating 2-bit and 1-bit masks), returning in `eax` the incoming `ecx` with its 32 bits in reversed order; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008840A2`, `008840B9`, `008840D6`, `008840EA`, `008840EF` |
| `008858B0` | 117 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it takes a count from the dword stack argument at `[rsp+0x40]` and returns when it is not positive; otherwise for each index i below the count it writes dword 1 or 0 to the i-th dword of the array at qword `[rsp+0x30]`: 1 when the threshold (incoming `xmm1` while i is below `ecx` minus dword `[rsp+0x38]`, else incoming `xmm2`) is at or below, or unordered with, the double absolute value of the i-th f32 of the `r9` array (mask at `01CEBD80`) divided by the i-th f32 of the array at qword `[rsp+0x28]`, rounded back to f32; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008858C7`, `008858E0`, `00885904`, `00885907`, `00885917` |
| `00888650` | 54 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it broadcasts the low f32 of `xmm1` to all four lanes and adds it to each of the 56 f32 values at `rcx` (seven passes of two unaligned 16-byte loads and stores), then returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00888655`, `00888667`, `0088866A`, `0088867F` |
| `00888690` | 92 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; for 56 f32 positions (14 passes of four) it stores the f32 at `rdx` + i*4 into `rcx` + i*4 when it is above the f32 already there (ordered `comiss`), leaving it otherwise, then returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008886A6`, `008886AC`, `008886E5` |
| `00888700` | 108 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; for 56 f32 positions (14 passes of four) it stores the f32 at `rdx` + i*4 into `rcx` + i*4 when the f32 already there is above it (ordered `comiss`), leaving it otherwise, then returns; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0088871B`, `00888720`, `00888765` |
| `00888780` | 31 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it spills `xmm0` to `[rsp+8]`, keeps only the sign bit and the f32 1.0 exponent bits of it (`and`), ORs in the f32 1.0 bit pattern and reloads `xmm0`, so it returns f32 1.0 carrying the incoming sign bit; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00888786`, `0088878A`, `0088878F`, `00888798` |
| `008888C0` | 34 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; when `rcx` is null it returns; otherwise it zeroes the five qwords `+0x0` to `+0x20` of `rcx` and tail-jumps through the qword at `01CEB630` with `rcx` incoming and `rax` = 0; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008888C3`, `008888C7`, `008888D6`, `008888DA` |
| `00889330` | 30 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it zeroes the seven qwords `+0x0` to `+0x30` of `rcx` and returns 0 in `rax`; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00889332`, `00889349` |
| `0088D4E0` | 18 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; when `ecx` equals 1 it returns; otherwise it advances `rdx` by sign-extended `ecx` times 4 and tail-jumps to `0088D500` with `rcx`, `r8` and `r9` incoming; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0088D4E3`, `0088D4E8`, `0088D4EC` |
| `0088DB60` | 15 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it returns in `rax` the qword at `01CEAE30` + sign-extended `ecx` times 8 (`rcx` is overwritten with the table address); UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0088DB63`, `0088DB6A` |
| `008922A0` | 28 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it returns in `eax` the number of set bits in `ecx`, adding bit `0x1` of `ecx` per right shift until `ecx` is zero (0 when `ecx` is zero); UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `008922B2`, `008922B5`, `008922B7` |
| `00892990` | 29 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; with i = sign-extended `r8d` it reads dword `[rcx+i*4]` into `eax` and dword `[rdx+i*4]` into `r8d`; when the `rdx` value is negative it returns the `rcx` value, otherwise it returns their 32-bit sum shifted right arithmetically by 1; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0089299B`, `0089299F`, `008929A5`, `008929AA` |
| `00893A80` | 45 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it reads f32 `[rcx]`, multiplies it by f32 7.314286 (`01CEBC7C`), adds f32 1023.5 (`01CEBC94`), truncates to `eax` and returns 0x3FF when that is greater than 0x3FF (signed), 0 when it is negative (`cmovs`), else the value; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00893A84`, `00893A8C`, `00893A98`, `00893AA9` |
| `00893AC0` | 64 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; with `r8d` and `r9d` masked to 0x7FFF it computes `eax` = the absolute value of (`r9d` - `r8d`) times (dword stack argument `[rsp+0x28]` - `ecx`) divided signed by (`edx` - `ecx`) (`idiv`), then returns `r8d` - `eax` when `r9d` - `r8d` is negative, else `r8d` + `eax`; UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `00893ACA`, `00893AE9`, `00893AED`, `00893AF5`, `00893AFC` |
| `00895570` | 27 B | no direct reference was found (census of `E8`/`E9`, `0F 8x`, `EB`/`7x` and rip-relative targets at every `.text` offset, and of qwords and 32-bit image-relative values in every section, `.pdata` included: SWE2-AUDIT-SPEC re-review 2026-10-03); it starts right after `int3` padding; it reads f32 `[rcx]` and f32 `[rdx]` and returns in `eax` 1 when the `rdx` value is above the `rcx` value, -1 when the `rcx` value is above, else 0 (also when unordered); UC-1 body admitted to frontier 2026-09-28, explained by interior citation 2026-10-03 | `0089557C`, `0089557F`, `00895585`, `00895588` |
