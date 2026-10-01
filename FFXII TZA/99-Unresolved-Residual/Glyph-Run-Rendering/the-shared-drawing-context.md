---
system: The shared drawing context behind 0209CC40
category: 99-Unresolved-Residual
status: AUDITED — every register row is closed (owner re-status 2026-09-30, OPUS): the field map is classified and GJ-1 to GJ-6 and GJ-10 are answered (§3a–§3g, §5a); who fills the three pointer slots (SD-103: rows 174-176 of the +0x000 table), the row's third qword, 10-bit id and decode loop (SD-104) and the reveal's authored inputs (SD-105) answered 2026-09-30
owner_layer: CodeDomain — residual; ancestors owned by UI
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN159 -> GN161 - every step of the certified lineage is additive on the canonical record (internal 38161, owner 9409 and finalNo 585 constant at all five generations; each step's codeDomain and explicit rise equals its unresolved fall). Of the functions classified since GN159 this document cites none of batch R109's 109; the 21 classified before GN160 are named in AUDIT-LOG's batch records and not in a tracked machine-readable list, so identity is not claimed. Voided by any delta that removes or rewrites a comment, tag, name, prototype or body range.; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md, lineage extension (twenty ledger figures across five generations)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-30
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-shared-drawing-context-pass-1 - the lifecycle reproduces to the address (69-byte writer, 121 reference sites in 26 functions with EXACTLY ONE write, and 0209D490 / 0x1108 / 0209CC40 / 01CEBC70 / 01E0CE0C all resolved from their own displacements); the field map was NOT re-derived - an independent linear register trace returned 67 offsets including impossible negative ones, reproducing from scratch the control-flow blindness section 3 already records, so the attempt is reported as a tool artefact and section 3's map is left untouched
  crossref_clean: true
  reopened_count: 0
  promoted: 2026-10-01 DOCUMENTED -> AUDITED by SWE2-AUDIT-SPEC (FRONTIER eligibility census sweep): falsification record opus-shared-drawing-context-pass-1; audit_crossrefs at HEAD reports 0 unresolved findings; cross-subsystem neighbours dispositioned in their section; killer observations recorded in the pass; promoter is not the last substantive author (last substantive commit: OPUS)
---

# The shared drawing context behind `0209CC40`

> One pointer, **one writer, a hundred and twenty-one readers**. It points at a **static 4,360-byte
> struct** that is zeroed once at startup and never reallocated — and the part of it this cluster
> touches directly is **the last sixty bytes**.

**PARTIAL.** The lifecycle, the size, the single initialiser and the directly-attributable field map
are read at tier 1. **Section 5 was corrected on 2026-09-03** after the instrument that produced it
was found to be control-flow blind; the correction is recorded there in full.

## 1. Why this object matters

The [text-element dispatch table](the-text-element-dispatch-table.md) showed that two of the three
dispatchers publish a field of the element into `[0209CC40] + 0x10D8` before tail-jumping to a
handler. That pointer is the cluster's spine: **121 reference sites**, more than any other datum in
this residual neighbourhood.

## 1b. What the player sees (SWE2-DATA, 2026-09-30)

- **Text that types itself out.** Dialogue appears character by character, and the newest character fades in rather than popping (§3g). The context holds the counters that pace it.
- **Captions for control codes, behind a console switch.** The `+0x400` table draws text for a control code, and it returns no row unless a developer-console byte is set (§3a). A retail player does not see that path.

## 2. Lifecycle: static, zeroed once, published once

`FUN_002B3550` (69 bytes) is the **only** function in the image that writes `0209CC40`:

```c
obj = &DAT_0209D490;            // a STATIC address, not an allocation
memset(obj, 0, 0x1108);         // 4,360 bytes
DAT_0209CC40 = obj;             // publish
if (FUN_00254A10() == 0)
    DAT_01E0CE0C = FUN_0024ABC0() * [01CEBC70];   // a conditional scale, computed once
```

Three things follow:

- **The object is static storage, not heap.** Its address is fixed at `0209D490`; nothing reallocates
  or replaces it, so the pointer at `0209CC40` has exactly one value for the life of the process.
- **It is zeroed exactly once**, so every field's initial value is 0 and nothing re-initialises it.
- **No vtable is written.** This is a plain struct, not a polymorphic object — which is consistent
  with the cluster's dispatch being a hand-rolled table (§1) rather than virtual calls.

## 3. The field map

Across every function that loads the pointer itself, **24 distinct offsets** are touched, and they
fall into two groups with a 4 KB gap before the first:

| offset | reads | writes | size | functions | note |
|---|---:|---:|---|---:|---|
| `+0x1060` | 1 | 0 | 8 | 1 | pointer read |
| `+0x1078` | 1 | 0 | 8 | 1 | pointer read |
| `+0x1090` | 1 | 0 | 8 | 1 | pointer read |
| `+0x10C8` | 10 | 14 | 8 | 10 | **touched by more functions than any other field** |
| `+0x10D0` | 2 | 2 | 4 | 2 | |
| `+0x10D4` | 9 | 17 | 4 | 8 | |
| **`+0x10D8`** | 7 | 12 | 4 | 7 | **what the dispatchers publish `obj[0x8C]` into** |
| `+0x10DC` | 6 | 10 | 4 | 4 | |
| `+0x10E0` … `+0x10F8` | | | 4, 8 | 1–6 each | seven more dword/qword slots |
| **`+0x10FC`** | 9 | **14** | 1, 4 | 10 | **the busiest field in the struct** |
| `+0x10FD` … `+0x1104` | | | 1, 2 | 1–5 each | a run of **single bytes** |

### 3a. The head is not a gap — it is two indexed arrays, and the census could not see them (FABLE, 2026-09-21)

**`GJ-1` answered in substance.** Two sweeps, in the order that makes the second necessary.

**First: the head is not reached by its own address.** A whole-image rip-relative sweep of the
object's own extent — `0209D490` to `0209E598`, all `0x1108` bytes — finds **exactly one reference in
the image**, and it is `002B3550`'s `lea` for the `memset` and the publish. So the head is touched
neither by a fixed displacement off the pointer (§3's census) nor by its address. If it is used at
all, it can only be through a **register base with a runtime index**, which is precisely the shape a
displacement census cannot see.

**Second: it is.** Tracking the register a load of `0209CC40` lands in and reporting every memory
operand that uses it as a *base with an index register* finds **25 functions that load the pointer
and 7 indexed accesses**, every one at **scale 8**:

| site | form | what it says |
|---|---|---|
| `002AECC8`, `002AEE4D` | `lea rsi, [ctx + idx*8]` | an array of qwords at `+0x000` |
| `002B34D7`, `002B351B` | `lea rcx, [ctx + idx*8]` | the same array |
| `002B5E98` | `lea rdi, [ctx + idx*8]` | the same array |
| `002B5D45`, `002B5DDC` | `mov rdx, qword ptr [ctx + idx*8 + 0x400]` | **a second array based at `+0x400`** |

**So the object is parallel qword tables with a control block at the end**, not a control block with
4 KB of padding in front of it. The `0x1060` bytes before `+0x10C8` are `524` qword slots, and at
least two array bases are in use within them.

**What the `+0x400` table is indexed by, read end to end.** At `002B5D3A` the index is
`rcx + rcx*2` — **the selector times three** — so the rows of that table are **three qwords, 24
bytes**, and the code takes `row[0]`:

```asm
002B5D29  call 001E0DA0          ; -> a byte selector
002B5D3A  lea  rdx, [rcx+rcx*2]  ; selector * 3
002B5D3E  mov  rcx, [0209CC40]   ; the drawing context
002B5D45  mov  rdx, [rcx+rdx*8+0x400]   ; row[0] of the selector's record
002B5D4D  mov  rbx, [rdx+8]
002B5D51  movsx ecx, word ptr [rbx+0xA]  ; read a field of the pointee
...
002B5D9A  mov  word ptr [rbx+0xA], di    ; and write it back
```

**And the selector comes from the input side.** `001E0DA0(code)` is
`InputManager_GetSingleton` → `00197790(mgr, code)`, and `00197790` is a **reverse lookup**: it takes
the developer-console settings singleton through `001D50D0`, **requires its byte `+0xC3D` to be
non-zero**, then scans the **106-dword table at `01DF1030`** for a dword equal to `code` and returns
its **index**, or `-1`. The table holds 106 distinct values in `1`–`152` — the control-code space,
whose `28`–`152` band is the keyboard set this database already decoded through the DirectInput
scancode table at `01F3DAB0` (`DM-2`).

> **So this cluster draws text for a CONTROL CODE, selected by that code's position in a 106-entry
> list, and the whole path is gated on a developer-console byte.** `00197790` returns `-1` — no row —
> unless `[console + 0xC3D]` is set. That gate is read by exactly two bodies, `00197790` and
> `00197800`, and **no function writes it by a fixed displacement**; the console's set/get arm
> reaches its rows by computed offset, so "no writer" here means *not written by name*, not *never
> set*. **This is why the cluster sits in `99-Unresolved-Residual`: it is reachable only with a
> console setting on.**

### 3b. The `+0x000` table's builder, its rows, and where its content comes from (FABLE, 2026-09-21)

**The `+0x000` table is filled row by row from an object hanging off the UI root.** `002B3480` is the
builder:

```asm
002B348A  call 0029CB50            ; rsi = *(*(0209AC30))         <- the UI ROOT's +0x00
002B3492  call 0029CB60            ; rbp = *((*(0209AC30))+0xB0)
002B349D  jne  ...                 ; a null source returns 0 and builds nothing
002B34BA  cmp  dword ptr [rsi+0x1C], ebx   ; the source's ROW COUNT
002B34CC  lea  rcx, [rax + rax*2]          ; edi * 3
002B34D0  mov  rax, [0209CC40]
002B34D7  lea  rcx, [rax + rcx*8]          ; -> &ctx[edi * 24]
002B34DB  call 002432B0                    ; write that row
```

**So both tables have 24-byte rows** — the one at `+0x000` here, the one at `+0x400` in §3a — and the
`+0x000` table's length is `[src + 0x1C]`, a runtime count rather than a constant. **`0209AC30` is
the UI root**, the same singleton the generic UI-request scheduler `00280A00` gates on through its
`+0xB8` / `+0xC0` slots, so this residual cluster is built from UI-root state rather than from
anything of its own.

**One row, written by `002432B0`:**

| offset | what the writer does |
|---|---|
| `+0x00` | a **packed dword of bit-fields**, assembled rather than assigned: bits `2..17` (`& 0x3FFFC`) carry a 10-bit id times four, **bit 1 is set** (`or edx, 2`), and **bit 0 is XOR-folded from bit 28 of the source record's first dword** (`[r12] >> 0x1C`) |
| `+0x08` | a **pointer to the source record** (`mov [r15+8], r12`) |
| `+0x10` | not read in this pass |

**The source records are 20 bytes and authored.** `002432B0` resolves `[src + 0x20]` through
`ImageAddress_ResolveRuntimePointer` and indexes the result by `idx * 5 * 4` — a **20-byte stride** —
taking a 10-bit field from `+0x00` and a dword from `+0x10`. So the `+0x000` table is a runtime index
**over an authored table**, one 24-byte row per source record, and the row keeps both a decoded key
and a back-pointer to the record it came from.

**Not claimed:** the third qword of the row, what the 10-bit id names, and the per-element decode loop
at `00243340` onward that walks `[r8+1]` through a jump table — all unread here. *(Registered 2026-09-30 as **SD-104**, SWE2-DATA.)*

### 3c. `GJ-2`: the three slots hold pointers to three arrays — and the arithmetic that says otherwise is a coincidence (FABLE, 2026-09-21)

**The near-miss first, because it is the transferable part.** `+0x1060`, `+0x1078` and `+0x1090` are
at **exactly** 24-byte boundaries from the `+0x400` table's base — rows **132, 133 and 134** — and at
**no** row boundary of the `+0x000` table (`174.67`, `175.67`, `176.67`). Three exact hits against
three misses is a discriminating test, and it is wrong. **Reading the sites settles it the other
way.** All three are read by one body, `002B5C90` — the same one that uses the `+0x400` indexed form
— and all three read identically:

```asm
002B5F53  mov   rcx, [ctx + 0x1060]              ; the slot holds a POINTER
002B5F5A  movsxd rdx, dword ptr [rsp+rdi*8+0x24] ; a runtime index from the caller's frame
002B5F5F  mov   rbx, [rcx + rdx*8]               ; index the POINTED-AT array of qwords
002B5F63  movsx ecx, word ptr [rbx + 0xa]        ; the same +0xA int16 the +0x400 path reads
```

`002B601A` and `002B60A6` are the same four instructions against `+0x1078` and `+0x1090`. **So they
are three genuine pointer slots, each holding the base of its own qword array** — not rows of the
`+0x400` table. *Exact arithmetic is not a structure proof; the row alignment is a coincidence, and
stopping at it would have published a wrong layout.*

**What they are, then.** Three parallel arrays of pointers-to-elements, selected **by code path**
rather than by index: each of the three sites is preceded by the same
`001E0BD0` → `001E0DA0` control-code lookup with a `cmp eax, -1` guard (§3a), and each then reads its
own slot. The element they reach has the `int16` at `+0xA` that §3a's `+0x400` path also reads and
rewrites, so the three arrays and the control-code table lead to **the same kind of element**.

**Why the census called them write-free, and what is still open.** They are "read and never written"
for the same reason the whole head looked empty: the writer does not reach them by a fixed
displacement off the published pointer. The whole-extent sweep (§3a) rules out an address-taken
write, and `002432B0` writes the `+0x000` table, where `+0x1060` is not a row boundary — so **who
fills these three slots is not answered here.** That is the residue of `GJ-2`, and it is narrower
than the question was. *(Registered 2026-09-30 as **SD-103**, SWE2-DATA.)*

### 3d. `GJ-5`: `0209CC48` and `0209CC50` are the render-buffer record and its write cursor (FABLE, 2026-09-21)

**They are not context fields at all — they are the cluster's PS2-style display-list state**, and the
three cells `0209CC40` / `0209CC48` / `0209CC50` are adjacent globals with different jobs rather than
a struct. `002B4730` (218 B) shows all of it, ending in a buffer swap:

```asm
002B4736  r8  = [0209E5A0]                 ; the current BUFFER BASE
002B473F  rdx = [0209CC50] ; rdx -= 0x10   ; the WRITE CURSOR, descending in 16-byte steps
002B474D  [0209CC50] = rdx
002B475B  edx = (rdx - r8) >> 4            ; the cursor's qword INDEX within the buffer
002B4763  bts eax, 0x1C                    ; tag bit 28
002B477B  or  eax, 0x6c008150              ; a GIF-shaped command word
...
002B47C9  call 003A1DB0                    ; RenderCommand_SubmitCurrentBufferAndSwap
002B47D2  eax = [02EBEFF0]                 ; the buffer INDEX
002B47D8  rcx = rax + rax*2                ; index * 3
002B47E3  rax = 02EBEFC0 + rcx*8           ; -> &record[index * 24]
002B47E7  [0209CC48] = rax                 ; <- the CURRENT RECORD
002B47EE  rax = [rax + 8]
002B47F2  [0209E5A0] = rax                 ; <- its buffer BASE
002B47FD  [0209CC50] = rax + 0x10          ; <- the cursor, one qword in
```

| cell | what it is |
|---|---|
| `0209CC40` | the shared drawing context (§2) — **1 writer, 25 readers** |
| **`0209CC48`** | **a pointer to the current 24-byte render-buffer record** in the table at `02EBEFC0`, selected by the index at `02EBEFF0` — 11 writers, 14 readers |
| **`0209CC50`** | **the write cursor** into that record's buffer, base `+0x10` at reset and moved in **16-byte** steps — 11 writers, 11 readers |
| `0209E5A0` | the record's `+8`: the buffer base itself — 6 writers, 6 readers, the same six bodies |

*(Counts anchored 2026-09-30, SWE2-DATA: they are function counts over the rip-relative operands into each cell, a write being a `mov` whose destination is the cell. The same sweep gives `0209CC40` 1 writer and 25 readers over 121 sites, the figures §2 states; `_index/candidates/dd-data-3-0930/shared_context_checks.py` S1, C1.)*

**So "cleared beside every column-1 dispatch" is a cursor reset**, not a flag clear: the dispatch
re-points `0209CC48` at the record the swap selected and rewinds `0209CC50` to its start. The
16-byte stride, the `bts` of **bit 28**, and constants of the shape `0x6C008150` / `0x10000000` /
`0x15000000` / `0x13000000` are **GS qwords with GIF-shaped tags** — the legacy PS2 display-list
family this database already reads elsewhere, reached here from the text cluster.

> **And the record table sits immediately below the authored-table registry.** `02EBEFC0` with
> 24-byte rows, its index at `02EBEFF0`, runs up to `02EBF000` — which is exactly the float that
> [the authored-data table registry](../../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md)
> identifies as the byte *below* its array, and which it uses to fix that array's lower bound. The two
> neighbourhoods meet at that boundary and neither page said so.

### 3e. `GJ-4`: `+0x10FC` is a BYTE, and the dword that says otherwise is a bulk clear (FABLE, 2026-09-21)

**The question was whether `+0x10FC` is one dword or overlapping fields**, since §3 measured it at
both 1 and 4 bytes. It is **a byte**, and the one 4-byte access is not a field at all — and the
function that makes it proves the point itself.

**Every other access in the image is byte-sized.** Across the run `+0x10FC`..`+0x1104` — nine
consecutive bytes — the sites are `mov byte`, `cmp byte`, `movzx byte`, `movsx byte`, in fourteen
functions. `+0x10FC` is a **three-state field**: the recurring shape is `cmp byte [+0x10FC], 2`
followed by setting it to `1` or `2`, with `0` written on several release paths.

**The single dword and word writes are one bulk clear**, in `002B24B0`, which is a **save / reset /
restore wrapper** around a nested drawing operation:

```asm
; SAVE - individually, and note the widths
002B2570  mov   esi, [ctx+0x10D8]
002B257D  movzx ebp, byte ptr [ctx+0x10FC]     ; <- saved as a BYTE
002B2584  mov   r14, [ctx+0x10C8]
002B258B  movsx r15d, byte ptr [ctx+0x10FF]    ; <- saved as a BYTE
002B2593  movss xmm6, [ctx+0x10E8]
; RESET - the widest stores that fit, over one contiguous region
002B2598  mov   [ctx+0x10C8], rdx              ; the new value
002B25A2  mov   [ctx+0x10D8], ecx
002B25A8  mov   dword ptr [ctx+0x10FC], ecx    ; 0x10FC..0x10FF
002B25AE  mov   qword ptr [ctx+0x10EC], rcx    ; 0x10EC..0x10F3
002B25B5  mov   qword ptr [ctx+0x10F4], rcx    ; 0x10F4..0x10FB
002B25BC  mov   word  ptr [ctx+0x1100], cx     ; 0x1100..0x1101
; RESTORE - individually, as bytes again
002B279F  mov   byte ptr [ctx+0x10FC], bpl
002B27AA  mov   [ctx+0x10D8], esi
002B27B0  mov   [ctx+0x10C8], r14
002B27B7  mov   byte ptr [ctx+0x10FF], r15b
002B27BE  mov   [0209CC48], r12                ; and the render-buffer record (§3d)
```

**The four stores at `+0x10EC`, `+0x10F4`, `+0x10FC` and `+0x1100` are contiguous** — `0x10EC`
through `0x1101` — and are the qword/dword/word split a compiler emits to zero a struct region. **A
function that saves `+0x10FC` as a byte, overwrites it inside a wider store, and restores it as a
byte is telling you the byte is the field and the dword is the sweep.**

> **And `002B24B0` is the object's nesting discipline.** It preserves exactly five things across a
> nested operation — `+0x10C8`, `+0x10D8`, `+0x10E8` (a float, in `xmm6`), `+0x10FC`, `+0x10FF` — and
> the render-buffer record pointer `0209CC48`, clearing the `+0x10EC`..`+0x1101` block in between.
> That is the ownership statement §3 could not make: **the control block is scoped, not global**, and
> those six are what a nested draw is allowed to disturb.

### 3f. `GJ-6`: the conditional float scales nothing, and on shipped data it is never computed (FABLE, 2026-09-21)

**`01E0CE0C` has one writer and ZERO readers in the image.** The writer is the initialiser itself
(§2). An image-wide rip-relative sweep of the cell finds no other reference of any kind, so whatever
it was meant to scale, nothing consults it.

**And the branch that computes it does not run on shipped data.** §2's condition is
`if (00254A10() == 0)`, and `00254A10` is a small predicate over a shipped id:

```asm
00254A14  call 00229E40          ; returns [01E02814], which SHIPS AS 0x0A
00254A19  cmp  eax, 0xB
00254A1C  ja   -> return 0
00254A1E  mov  ecx, 0xD81        ; bits 0, 7, 8, 10, 11
00254A23  bt   ecx, eax
00254A26  jae  -> return 0
00254A28  mov  eax, 1
```

`0xD81` sets bits **0, 7, 8, 10 and 11**, and the shipped id is **10**, so `00254A10` returns **1**
and the initialiser's `== 0` arm is **not taken**. The cell keeps its zeroed value.

**What the value would have been, for completeness.** `0024ABC0` is
`(float)[01E0C1D8] * 0.001953125`, and `[01E0C1D8]` ships as **512** — so that product is exactly
**1.0** — and §2 multiplies it by `[01CEBC70]`, which is **4.0**. **The float would be 4.0.**
(`[01E0C1D8]` itself is a heavily shared global: one writer, `0024B120`, and a hundred readers.)

> **So `GJ-6` closes as a double negative, both halves measured:** the cell is read by nothing, and on
> the shipped configuration it is not even written. It belongs with the *written and never consumed*
> findings elsewhere in this database rather than with the live scaling factors.

**What this does and does not settle.** It answers *what the object is for* at the level the question
asked — a per-control-code record table plus a second qword array, addressed by index, with the
control block at `+0x10C8` as its header. It does **not** name the 24-byte record's fields beyond
`row[0]` being a pointer whose `+8` leads to an object with an `int16` at `+0xA` that this path reads
and rewrites, and it does **not** answer `GJ-2` — the three pointer slots at `+0x1060`, `+0x1078` and
`+0x1090` are still read-and-never-written by anything that loads the pointer. *(Both answered since: GJ-2 in §3c,
and who fills the slots in SD-103, 2026-09-30, OPUS: they are rows 174–176 of the `+0x000` table, written by the row
builder's indexed stores, which a fixed-displacement census cannot see.)*

*Instruments: `_index/candidates/fable_ripband.py` for the own-extent sweep and
`_index/candidates/fable_ctx_indexed.py` for the indexed one, the latter carrying two controls — the
initialiser `002B3550` must NOT appear in the tracked set (it only takes the address), and at least
one body the page already names as touching the control block must, or the tracker is not reaching
the population §3 measured. Both hold.*

> **A 4,360-byte object whose directly-used region is its last sixty bytes.** The control block at
> `+0x10C8` is dense — dwords, then a run of individual bytes at `+0x10FC`–`+0x1104` — and it sits
> immediately after three pointer slots at `+0x1060`/`+0x1078`/`+0x1090`, which are **read and never
> written** by any function that loads the context. *(At a fixed displacement. The indexed row writes fill them:
> SD-103, above.)*

`+0x10FC` is accessed at **both 1 and 4 bytes**, ~~so it is either a dword whose low byte is written~~
~~separately or the head of overlapping fields; this document does not resolve which.~~ *(Corrected 2026-09-30, SWE2-DATA: §3e resolves it. It is a byte, and the dword access is a bulk clear (GJ-4).)*

### 3g. `GJ-10`: `+0x10D8` and `+0x10DC` are the text-reveal counters, and the fade is in `+0x10E4` (FABLE, 2026-09-21)

`UQ-369` established that `+0x10D8` and `+0x10DC` are copied from two words and that `+0x10D8` counts
down, and stopped there because **none of the eight bodies it scanned tested it**. The test is in a
ninth. Read out, the three fields are **one mechanism: the progressive text reveal.**

### Where all three come from — one setup, one line each (FABLE, 2026-09-21)

`002AF960` seeds the whole triple from the text-draw block in five instructions:

```asm
002AFB05  movsx eax, word ptr [rbx + 0x8c]
002AFB19  mov   dword ptr [rcx + 0x10d8], eax     ; the progress counter
002AFB1F  movsx eax, word ptr [rbx + 0x90]
002AFB26  mov   dword ptr [rcx + 0x10dc], eax     ; the full-opacity counter
002AFB39  movsx eax, byte ptr [rbx + 0x9d]
002AFB47  mulss xmm0, dword ptr [rbx + 0x50]
002AFB4C  movss dword ptr [rcx + 0x10e4], xmm0    ; the fade fraction = (s8)+0x9D * float +0x50
```

`+0x8C` is the word two initialisers set to **`0x7D00` (32,000)** *(anchored 2026-09-30, SWE2-DATA: `002B3400` at `002B3469` and `002A4830` at `002A49C2`; `_index/candidates/dd-data-3-0930/shared_context_checks.py` S2)*, so at rest the counter is
effectively unlimited. The column-1 dispatchers `002ABEC0` and `002ABF20` publish that same `+0x8C`
into `+0x10D8` on every dispatch. *`+0x90`'s own default is not established here and is not assumed.*

### Both counters are charged once per glyph (FABLE, 2026-09-21)

`002A9F00` — the per-glyph emit — decrements both in the same three instructions, every time:

```asm
002AA0B1  dec dword ptr [rdx + 0x10d8]
002AA0B7  lea eax, [rcx - 1]
002AA0BA  mov dword ptr [rdx + 0x10dc], eax
```

### `+0x10DC` is the test, and past it the glyph fades (FABLE, 2026-09-21)

Immediately before that decrement, `002A9F00` reads `+0x10DC` and branches on it:

```asm
002AA05C  mov   ecx, dword ptr [rdx + 0x10dc]
002AA062  test  ecx, ecx
002AA064  jg    002aa09c                       ; still positive -> 002AA09C: the glyph's own alpha
002AA066  movss xmm1, dword ptr [rdx + 0x10e4] ; else: the fade fraction
002AA079  mulss xmm0, xmm1                     ; alpha * fraction
002AA07D  subss xmm1, dword ptr [rbp - 0x50]   ; and the fraction STEPS DOWN
002AA086  movss dword ptr [rdx + 0x10e4], xmm1
```

**So while `+0x10DC` is positive a glyph draws at its own opacity; once it is not, each successive
glyph is drawn at that opacity times a fraction that shrinks by a fixed step per glyph** — a soft
leading edge that fades to nothing rather than a hard cut.

The same shape appears twice more in the font drawer `002AC5F0`, against a literal zero
(`xor r15d, r15d` at `002AC622`, never reassigned):

```asm
002AE0D3  cmp    dword ptr [rcx + 0x10dc], r15d
002AE0DA  jg     002ae10b                      ; -> the glyph's own alpha byte [r14+0x33]
002AE0E1  movss  xmm0, 128.0f
002AE0F0  mulss  xmm1, dword ptr [rcx + 0x10e4]
002AE0F8  comiss xmm1, xmm0
002AE0FB  ja     002ae104                      ; clamp high at 128
002AE0FD  xorps  xmm0, xmm0
002AE100  maxss  xmm0, xmm1                    ; clamp low at 0
```

and identically at `002AE27E`. **The alpha is `clamp(glyphAlpha * fraction, 0, 128)`** — 128, not 255,
which is the same half-scale opacity convention the message window's row draw uses when it scales its
RGBA bytes with `imul` then `sar 7`.

### `+0x10D8` is not a second copy of it — it is the progress *ratio* (FABLE, 2026-09-21)

`+0x10D8` is never tested. It is converted to a float and **divided**:

```asm
002AD670  movd   xmm2, dword ptr [r8 + 0x10d8]
002AD67F  cvtdq2ps xmm2, xmm2
002AD686  cvtdq2ps xmm0, xmm0          ; xmm0 = (float) the per-call total in [rbp-0x78]
002AD68C  divss  xmm2, xmm0            ; remaining / total
002AD697  mulss  xmm2, xmm1            ; scaling a signed word from the frame
```

So the pair is **a count and a fraction of the same run**: `+0x10DC` decides *whether this glyph is
revealed yet*, `+0x10D8` says *how far through the reveal we are*, as a number between 1 and 0 that
scales a geometric quantity.

### One character can be exempted from the budget (FABLE, 2026-09-21)

`002AE610`, the number formatter, **gives a unit back to both counters before emitting**, unless a
flag says otherwise:

```asm
002AE9D2  test dword ptr [rdi + 0x44], 0x400
002AE9D9  jne  002ae9ee                    ; flag set -> no refund
002AE9DB  mov  rax, qword ptr [0209CC40]
002AE9E2  inc  dword ptr [rax + 0x10d8]
002AE9E8  inc  dword ptr [rax + 0x10dc]
002AE9EE  ...
002AE9FC  call 002A9F00                    ; which decrements both again
```

An increment immediately before the call that decrements is a **refund**: that glyph is drawn but not
charged to the reveal. So an inserted number's digits do not consume the typewriter's budget unless
flag `0x400` is set.

### And the budget is per draw, not global (FABLE, 2026-09-21)

Both counters are saved and restored around nested work by the three wrappers already documented -
`002B24B0` (section 3e's save/reset/restore, which preserves `+0x10D8` among its five fields),
`002B2970`, and the argument-insertion control code, which the control-code page records as saving
`+0x10D8` / `+0x10DC` / `+0x10E4` together. That grouping is now explained: **they are saved together
because they are one state**, and a nested draw must not spend the outer run's reveal.

**In player terms:** this is the text that types itself out - dialogue appearing character by
character with the newest character faded in rather than popping - and the defaults make it
instantaneous, because 32,000 characters is more than any line.

*What this does not settle:* the default of the block's `+0x90`, ~~who writes `+0x9D` and~~ `+0x50` (the
fade's magnitude and step), and what the signed word at `[rbp+0x1C]` that the ratio scales is. The
mechanism is read; its authored inputs are not. *(Corrected 2026-09-30, SWE2-DATA: `+0x9D` is written by the reveal stepper `002ABF70` as the lag behind the head (`002AC0BF`, `002AC116`, `002AC129`; UQ-173), with its bound `+0x9E` set to 8 by the initialiser `002AC1E0` (`_index/candidates/dd-data-3-0930/shared_context_checks.py` S3). The rest is **SD-105**.)*

## 4. What connects to the dispatch table

`+0x10D8` is written 12 times across 7 functions, and two of those writes are the dispatchers of the
[dispatch-table document](the-text-element-dispatch-table.md) §4, publishing `(int16)element[0x8C]`
immediately before tail-jumping. **The dispatchers' only work besides dispatching is to write this
field** — so `+0x10D8` is how a per-element value reaches a handler that is not given the element.

## 5. What this instrument cannot see — corrected 2026-09-03

**This section first reported that the context pointer is passed as argument 1 at nine call sites to
seven functions, including `0017F850`.** That was **wrong**, and the way it was wrong matters more
than the claim.

The tracker followed the register a function loads the pointer into and walked instructions
**linearly, ignoring control flow**. At a jump target the linear predecessor is not the dynamic
predecessor, so a register killed on every real path still looked live. Reading one of the nine sites
settles it — at `002ADBFD` the three instructions before the call are `xor r9d,r9d ; xor r8d,r8d ;
xor edx,edx`, reached by a branch, and **`rcx` is not set on that path at all.**

**Made block-aware — `held` cleared at every branch target and after every unconditional transfer —
the same census returns ZERO argument-passing sites.** All nine were artifacts.

> **A register-tracking instrument that does not model control flow is not a conservative
> instrument; it is a wrong one.** It does not under-report, it **invents**, and every one of its
> nine inventions looked like an ordinary call site.

The field map in §3 was rebuilt with the same fix. **Its shape is unchanged** — the same three
pointer slots, the same tail block — which is why the correction moved counts and removed one
spurious offset (`+0x0000`) without moving any conclusion.

**What stands after the correction:**

- ~~**Indexed accesses: zero.** A counter that would have reported non-zero.~~ *(Corrected 2026-09-30, SWE2-DATA: §3a's base-with-index sweep finds seven indexed accesses, all at scale 8. The block-aware tracker's zero was wrong.)*
- **One static reference into the body** in the whole image: the initialiser's own `lea` at `002B3556`.
- **No call site was found passing the pointer as argument 1.**

**And the front 4,192 bytes are still not claimed to be unused.** The corrected tracker resets at
every join, so a pointer loaded before a branch and used after it is invisible to it — it now
**under**-reports by construction, which is the right direction for an instrument but still an edge.

> The original caveat survives its own evidence being withdrawn. **The reason to refuse the claim
> changed; the refusal did not.** A negative that only holds while one particular support holds was
> never worth making.

### The seven "callees" were read, and they are not callees

All seven functions the withdrawn claim named were read in full — 438 bytes between them — before the
defect was found, and **none of them takes this context as an argument**:

| Function | What it actually is |
|---|---|
| `003FFB90` | reads `[rcx+1]` and `[rcx+2]`, masks each with `0xF`, **returns 3** (`003FFBAB`) |
| `003FFAB0` | reads the same two bytes, masks `0xC0`/`0x7F`, branches on `[rcx+1] & 7`, **returns 3** (`003FFAE0`) |
| `003FFF10`, `003FFCE0`, `003FFDA0` | the same shape |
| `0017F850` | opens the `"display : draw Font"` scope (`0017F854`) and closes it — a scope wrapper, no context argument |
| `00254A10` | `bt` of a mode value against the mask `0xD81` (`00254A23`); a boolean predicate taking no pointer |

> **Returning the constant 3 after reading bytes 1 and 2 of `rcx` is a three-byte sequence decoder**,
> and `rcx` there is a pointer into a text stream, not a 4,360-byte context. Reading them is what
> exposed the defect: **the callees made no sense as callees**, which is a cheaper signal than any
> checker and is available to anyone who reads what an instrument hands them.

Those decoders belong to the glyph pipeline documented in
[`how-a-line-of-text-becomes-glyph-quads.md`](how-a-line-of-text-becomes-glyph-quads.md), not to this
object.

## 5a. `GJ-3`: the context is never passed — and the question had to be turned round to say so (FABLE, 2026-09-21)

Section 5 says its census "finds no argument-passing site, but it under-reports by construction", so
`GJ-3` stayed open rather than closing in the negative. **That was the right caution about the wrong
instrument.** A liveness walk over a linear disassembly — track the register a load of `0209CC40`
lands in, report the calls where it is still live — can only ever produce candidates: it needed three
separate corrections to get from 22 sites to 0 (32-bit alias writes do not kill the 64-bit value; a
live register is not an argument; the walk is not flow-aware), and even corrected, its blind spot is
exactly the case that matters — a pointer spilled to the stack and reloaded into `rcx` is a pass it
cannot see.

**So ask it at the other end, where no liveness is involved.** A function that **dereferences the
context without ever loading `0209CC40` itself must have been handed the pointer.** That is a direct
observation about a function's own bytes, not an inference across a call.

### Running it, with the premise tested rather than assumed (FABLE, 2026-09-21)

Sweeping every function for a dereference at nine offsets this database has already tied to this
object — `+0x10C8`, `+0x10D4`, the reveal triple `+0x10D8` / `+0x10DC` / `+0x10E4`, `+0x10E8`,
`+0x10FC`, `+0x10FF`, `+0x1102` — excluding stack-relative forms, gives **33 functions**, of which
**26 load `0209CC40`** and **14 do not**. Fourteen candidate receivers is not the answer, because the
sweep rests on a premise it has not earned: *that an offset this large belongs only to this object.* A
4 KB structure is not unique, and two discriminators settle every one of the fourteen:

| | ruled out by | how many |
|---|---|---|
| **Wrong width** — the context's `+0x10D4` / `+0x10D8` / `+0x10DC` are **dwords**, and these read or write the same displacement as a **byte**, **word** or **qword**: a different structure at the same offset | the access instruction itself | **6**: `001C2F50`, `001C3370` (`cmp byte [+0x10D4]`), `001CCB20` (`mov word [+0x10D8], 0x100`), `001CD0E0` (`cmp byte [+0x10D8]`), `00792350` (`mov qword [+0x10D8]`), and its neighbour |
| **Unreachable from anything holding the pointer** — not one of their callers loads `0209CC40`, so nothing supports them ever receiving it | the call graph | **8**: `0017E440`, `0017E470`, `001D1660` (0 callers), `002BF4F0`, `002BFB40`, `00793250`, `0079B300`, `0079CEB0` (0 callers), `0079EDD0` |

**Nothing survives. Zero receivers.** Every function in the image that touches this object fetches it
from the global first.

### What the two instruments together are worth (FABLE, 2026-09-21)

They fail in **opposite directions**, which is the only reason a negative is worth stating here. The
liveness walk under-reports passes (a stack round-trip hides one); the receiver test cannot see a
receiver that uses only fields outside the nine. But a pass the first misses would still surface in
the second **at the callee**, so long as the callee touches any of the nine — and the nine include
every field the cluster's own consumers use. **The negative is bounded by that, and by nothing softer.**

The loader census also tightens a number the page quotes: **26 functions, 121 sites** — the same 121
"reference sites" section 1 reports, now split into the functions that make them. And every one of
the 26 lies between `002A9F00` and `002B5C90`: **the object is not merely never passed, it is never
reached from outside the cluster that owns it.**

*What this does not claim.* It does not say the object could not be passed — it says nothing in this
image does it. And it does not extend to a receiver whose only contact with the object is at an
offset below `+0x10C8`; the whole-extent sweep in section 3a covers the head, but the middle of the
structure is not part of this test.

## 6. Key addresses

| Address | Role |
|---|---|
| `0209CC40` | the pointer; **1 writer, 121 reference sites** |
| `0209D490` | the struct itself, static, `0x1108` bytes |
| `002B3550` | the only initialiser: zeroes the struct, publishes the pointer |
| `0209CC48` | ~~cleared by both column-1 dispatchers alongside the publish~~ the current render-buffer record, re-pointed with its cursor `0209CC50` at each dispatch (§3d; corrected 2026-09-30, SWE2-DATA) |
| `002B3480` / `002432B0` | the `+0x000` table's builder and its row writer (§3b) |
| `002B5C90` | reads the `+0x400` table and the three pointer slots (§3a, §3c) |
| `002B4730` | the render-buffer swap (§3d) |
| `002AF960` | seeds the reveal triple `+0x10D8` / `+0x10DC` / `+0x10E4` (§3g) |
| `01E0CE0C` | a float the initialiser computes conditionally, once |

## 6b. Call chain (SWE2-DATA, 2026-09-30)

```
002B3550 initialiser: memset 0209D490, publish 0209CC40
002AF960 text draw setup -> seeds +0x10D8 / +0x10DC / +0x10E4 from the text block
002ABEC0 / 002ABF20 column-1 dispatchers -> publish element +0x8C into +0x10D8 -> handler
002B3480 -> 002432B0 (one +0x000 row per source record)
002B5C90 -> 001E0DA0 -> 00197790 (control-code index) -> +0x400 row, or +0x1060 / +0x1078 / +0x1090 arrays
002B4730 -> 003A1DB0 buffer swap; re-points 0209CC48 / 0209CC50
```

Every edge is a call site this page cites in §2–§3g.

## 6c. Modding notes (SWE2-DATA, 2026-09-30)

- The context is static at `0209D490` and never reallocated (§2), so a mod can hold its address for the life of the process.
- The reveal is bounded by the text block's `+0x8C`. Its default `0x7D00` makes text appear at once, and a smaller value makes it type out (§3g).
- The `+0x400` control-code path returns no row unless the console byte `+0xC3D` is set (§3a), so those captions cannot be restored by editing text alone.

## 7. What is not known

- **`GJ-1` — What the object is for.** ~~Its lifecycle, size and field map are read; nothing names it.~~ **ANSWERED 2026-09-21 (FABLE), §3a:** parallel indexed qword tables with the control block at the end. *(Pointer added 2026-09-30, SWE2-DATA.)*
  **Narrowed 2026-09-21 (FABLE), section 3g:** one region of it is named - `+0x10D8`, `+0x10DC` and
  `+0x10E4` are the **progressive text reveal's** counters and fade fraction.
- **`GJ-2` — What the three pointer slots at `+0x1060`, `+0x1078` and `+0x1090` point to.** Each is read by one
  function and written by none of the functions examined — so they are written either by a callee or
  before any of them run. **ANSWERED 2026-09-21 (FABLE), §3c:** each holds the base of its own qword array. Who fills them is **SD-103** *(pointer added 2026-09-30, SWE2-DATA)*.
- `GJ-3` — ~~**Whether the object is ever passed to another function at all.** The corrected census finds no
  argument-passing site, but it under-reports by construction (§5), so this is open rather than
  answered in the negative.~~ **ANSWERED 2026-09-21 (FABLE), section 5a: it is never passed.** Asked
  the other way round — which functions dereference it *without* loading `0209CC40` — the question
  needs no liveness at all. Fourteen candidates, **all fourteen ruled out**, six by access width and
  eight by having no caller that holds the pointer. All 26 users fetch it from the global, and all 26
  lie inside the cluster.
- **`GJ-4` — Whether `+0x10FC` is one dword or overlapping fields.** **ANSWERED 2026-09-21 (FABLE), §3e:** a byte; the dword access is a bulk clear. *(Pointer added 2026-09-30, SWE2-DATA.)*
- **`GJ-5` — What `[0209CC48]` is**, cleared beside every column-1 dispatch. **ANSWERED 2026-09-21 (FABLE), §3d:** the current render-buffer record, and the "clear" is a cursor reset. *(Pointer added 2026-09-30, SWE2-DATA.)*
- **`GJ-6` — What the initialiser's conditional float at `01E0CE0C` scales.** **ANSWERED 2026-09-21 (FABLE), §3f:** nothing, and on shipped data it is never computed. *(Pointer added 2026-09-30, SWE2-DATA.)*
- [x] **Who fills the three pointer slots `+0x1060`, `+0x1078` and `+0x1090`.** No fixed-displacement or address-taken write reaches them (§3a, §3c). **SD-103** (SWE2-DATA, 2026-09-30). *(SD-103 answered 2026-09-30 by OPUS `c2b5b9927`, [record](../../_index/candidates/sd103-104-context-rows-0930/README.md).)*
- [x] **The `+0x000` table row's third qword, what its 10-bit id names, and the decode loop at `00243340`.** §3b leaves all three unread. **SD-104** (SWE2-DATA, 2026-09-30). *(SD-104 answered 2026-09-30 by OPUS `c2b5b9927`, [record](../../_index/candidates/sd103-104-context-rows-0930/README.md).)*
- [x] **The reveal's authored inputs.** The text block's `+0x90` default, the writer of the fade step `+0x50`, and the signed word at `[rbp+0x1C]` that the ratio scales (§3g). **SD-105** (SWE2-DATA, 2026-09-30). *(SD-105 answered 2026-09-30 by OPUS `f2f55938a`, [record](../../_index/candidates/sd105-reveal-inputs-0930/README.md).)*

> **Every bullet in this section now carries its `GJ-` id, added 2026-09-22 (FABLE) on `AUDITSPEC-REQ-FABLE-REGISTER-71-OPEN-ITEMS`.** They were all registered already — the ids simply were not *in* the bullets, so a census that looks for an id in the item could not see them and fell back to matching this page's filename in the register, which for this page matched nothing. **An id-keyed register only works if the id is where the reader is.**


## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| One writer of the pointer | image-wide scan for rip-relative writes to `0209CC40` | 1 |
| The struct is static at `0209D490`, `0x1108` bytes | `lea rbx,[0209D490]` / `mov edx,0x1108` / call, then the publish | 1 |
| No vtable is written | the initialiser is 69 bytes and decoded in full | 1 |
| 24 directly-attributable offsets | per-function pointer tracking, **block-aware**: state cleared at every branch target and after every unconditional transfer | 1 |
| ~~Zero indexed accesses~~ **Seven indexed accesses, all at scale 8** *(corrected 2026-09-30, SWE2-DATA; §3a)* | ~~the same pass counts them separately and reports the count~~ §3a's base-with-index sweep | 1 |
| the §3d writer and reader counts | `_index/candidates/dd-data-3-0930/shared_context_checks.py` S1, C1 | 1 |
| the two `0x7D00` defaults of `+0x8C`, and the writer of `+0x9D` | `_index/candidates/dd-data-3-0930/shared_context_checks.py` S2, S3 | 1 |
| One static reference into the body | rip-relative scan over `[0209D490, +0x1108)`; the only hit is the initialiser's `lea` | 1 |
| **No** site passes the pointer as argument 1 | the same tracking made block-aware; the nine previously reported were artifacts (section 5) | 1 |

**Controls.** The absence claims are of different strengths and are labelled accordingly.
~~*"Zero indexed accesses"* comes from a counter that would have reported a non-zero number, so it is a~~
~~measurement.~~ *(Struck 2026-09-30, SWE2-DATA: §3a found seven.)* *"The front 4,192 bytes are untouched"* is **scoped to functions that load the pointer**
and to a tracker that resets at every join — it under-reports, and the document does not convert it
into a claim that the region is unused.

**The correction in section 5 is the control that matters most here**, because the defect it names
would not have been caught by any check this document runs: the artifacts were well-formed call sites
at real addresses. **It was caught by reading one of them.**

## 9. Related

- [`the-text-element-dispatch-table.md`](the-text-element-dispatch-table.md) — the dispatchers that write `+0x10D8`, and the handler table this context serves.
- [`how-a-line-of-text-becomes-glyph-quads.md`](how-a-line-of-text-becomes-glyph-quads.md) — the glyph pipeline below the handlers.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. Nothing executed.)*

### ✔ The lifecycle claims reproduce to the address

`FUN_002B3550` is **69 bytes** and is **the only writer** of `0209CC40` — a census of every
rip-relative operand in every function body finds **121 reference sites in 26 functions, of which
exactly one is a write**, `002B356A`. The body resolves every address the page names, from its own
displacements:

| instruction | resolves to | §2 says |
|---|---|---|
| `lea rbx, [rip + 0x1DE9F33]` | **`0209D490`** | the static object |
| `mov edx, 0x1108` | **4,360** | the memset length |
| `mov [rip + 0x1DE96CF], rbx` | **`0209CC40`** | the publish |
| `mulss xmm0, [rip + 0x1A386E9]` | **`01CEBC70`** | the conditional scale's constant |
| `movss [rip + 0x1B5987D], xmm0` | **`01E0CE0C`** | its destination |

**Static storage, one memset, one publish, no vtable write** — all four hold, and the 121 is exact.

### ⚠ The field map is not re-derivable by a linear trace — and my attempt proved §3's own point

§3 records that it was corrected on 2026-09-03 *"after the instrument that produced it was found to
be control-flow blind"*. I rebuilt an offset census independently — load the pointer into a register,
then attribute every later `[reg + disp]` in that function — and it returned **67 distinct offsets
including negative ones** (`+0x-080`, `+0x-010`, `+0x-001`). **A struct published at its own base has
no negative offsets.** The instrument never killed the register when the function reused it, so every
unrelated `[rax + disp]` after the load was counted.

> **That is the same failure mode §3 already names, reproduced from scratch.** It is recorded here
> rather than published as "67 offsets, not 24", because the number is an artefact of the tool and
> not a measurement of the struct. **§3's map is left exactly as it stands** — this pass did not
> confirm it and did not refute it, and a sound re-derivation needs register liveness, which is more
> than a linear disassembly gives.

**What the failure does establish** is that §3's caution is the right one to carry forward: any future
field census over this pointer must kill the register on redefinition and across the function's
branches, and a census that reports an offset the struct cannot have is announcing its own defect.

**Not claimed.** §3's 24 offsets and their read/write counts — **not re-derived**; §5 and everything
past it — **not read**; what any field means. The 121 sites were counted, not classified beyond the
single write. Nothing executed.

*(Pass 22 adjacency, 2026-09-14: `00254A10` calls the `CoreRuntimeScheduling` yield `00229E40`
(1 edge), and `00229E40` is itself called by `Script_VM_Native_Bridge` bodies `0033FED0`/
`0034BA00` and `Rewards_Progression_Economy` `00317ED0` (3). The drawing-context setup yields to
the scheduler like every other leg of the text walk; the shared yield accessor is consumed from
the script bridge and economy code too.)*

### Four layers section 5a cites only to EXCLUDE (FABLE, 2026-09-21)

Every address below appears on this page for one reason: section 5a's receiver sweep returned it as a
candidate and the discriminators **ruled it out**. They are cited so a reader can check the exclusion,
not because this object reaches them — the section's own finding is that it reaches nothing outside
`002A9F00`..`002B5C90`. All four are **MECHANICAL**, and in the strongest sense: the crossing is an
offset collision, and there is no call between them and this object at all.

- **Platform.** `001CCB20` (writes `+0x10D8` as a *word*), `00792350` (as a *qword*) and `0079B300`
  reach that layer through their own callees; they are different structures that happen to have a
  field at a displacement this one also uses.
- **Audio.** `001CD0E0` (reads `+0x10D8` as a *byte*) and `001D1660` (0 callers) call into it.
- **PlatformOnlineAchievements.** `001CD0E0` again.
- **Application.** `00792350` and `00793250` are called from it.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **UI — CLIENT, 15 edges.** Cited drawing-context functions are called by UI bodies of 725 to 1,692 bytes.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Application — MECHANICAL, 2 edges.** `00792350` is called by `0015BC40`; `00793250` is called by `008A6970`.

**Audio — MECHANICAL, 3 edges.** `001D1660` calls `001DBB00`, `002DEBA0`; `001CD0E0` calls `002DEBA0`.

**Input — MECHANICAL, 13 edges.** `001D50D0` is called by `InputManager_TranslateBindingProfileToControlState` (`00197160`), `00197790`, `00197800`; `002B5C90` calls `001E0B90`, `001E0BD0`, `001E0DA0`; `001E0DA0` calls `00197790`, `InputManager_GetSingleton` (`00198790`); `00197790` is called by `001E0DA0`; `00197800` is called by `001E0E70`; `0079B300` is called by `0079E520`; `0079EDD0` calls `InputSystem_DestroyRegisteredInputDevicesAndBackend` (`00799860`); `0079EDD0` is called by `0079E520`.

**Platform — MECHANICAL, 3 edges.** `001CCB20` calls `005CC930`; `00792350` calls `005CD0A0`; `0079B300` calls `0019A510`.

**PlatformOnlineAchievements — MECHANICAL, 1 edge.** `001CD0E0` calls `003166F0`.

**Resource — MECHANICAL, 2 edges.** `001CD0E0` calls `0020C700`; `001D1660` calls `002EEEE0`.

**Rewards_Progression_Economy — MECHANICAL, 3 edges.** `00229E40` is called by `EnemyChain_UpdateOnDefeat` (`00317ED0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) calls `EnemyChain_TryAdvanceRank` (`003183D0`); `EnemyChain_UpdateOnDefeat` (`00317ED0`) is called by `BattleUnit_ProcessDefeatRewardsAndLoot` (`00312280`).

**Save_Load_Settings — MECHANICAL, 2 edges.** `0017E470` is called by `SaveStorageQueue_CompleteFrontOperationAndNotify` (`00582240`); `00254A10` is called by `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`).

**Script_VM_Native_Bridge — MECHANICAL, 12 edges.** `001C3370` is called by `003522C0`, `00353080`, `003541B0`, `00354B20` and 3 more; `00229E40` is called by `0033FED0`, `0034BA00`; `002B5C90` is called by `003413E0`; `0033FED0` calls `VMResult_WriteInt32` (`0026B4E0`); `0034BA00` calls `VMResult_WriteInt32` (`0026B4E0`).

**WorldAreaField — MECHANICAL, 2 edges.** `001CD0E0` calls `FieldData_GetVariable0` (`00265270`), `WorldTransition_GetTransitionFieldId` (`00314910`).

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
