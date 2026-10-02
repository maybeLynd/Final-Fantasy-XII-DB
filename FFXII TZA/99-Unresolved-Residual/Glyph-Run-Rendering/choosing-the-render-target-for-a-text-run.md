---
system: Choosing the render target for a text run
category: 99-Unresolved-Residual
owner_layer: CodeDomain — Glyph run rendering
status: AUDITED — the selection, its tree, the vertex batches (UQ-358), the font-size index (UQ-360) and the key's two halves (UQ-356: b a mode of 0..2, a a window kind or the run's origin cell) answered 2026-09-17; the tree's populator (UQ-357) answered 2026-09-17
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation delta - every function this document cites whose record differs between the stamped snapshot and GN161's gained a plate comment and tags ONLY (empty comment before, tag set a subset, checked field by field), and this document makes no uncorrected absence claim about any of them; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 3 cited address(es) among the 128 records changed across GN158..GN161; each differs only in comment and tags; 0 live absence claims (check_stranded_absence.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-DELTA-RELIANCE-BASIS; re-measured and applied for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708, on SNAPSHOT-IDENTITY - replaced rather than re-targeted because that basis is FALSE for this document, which cites a record that changed
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-13
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-render-target-pass-1 - the structure reproduces to the address: both body sizes, both ret addresses with no padding after the second, section 2.1's four-condition guard instruction for instruction, the bare epilogue, and the memo's closure (the last two stores are the two fields the guard compares); the two-record bound is the immediate cmp rcx, 2 at 001E9E17; CORRECTED: the body is 133 instructions, not 130
  crossref_clean: true
  reopened_count: 0
---

# Choosing the render target for a text run

[`painting-a-line-of-text-into-a-render-target.md`](painting-a-line-of-text-into-a-render-target.md)
establishes the two `0x2C`-byte descriptors at `+0x2320` and says of the first field: *"read and
written by `001E9D20` … **neither function in this pair touches it**."* This is that function.

**Extents checked**: `001E9D20` 472 B, complete, **133** instructions (~~130~~, corrected §11 — the 472 bytes disassemble to 133 with no padding), two `ret`s at `001E9ED3` and
`001E9EF7`; `001E9C30` 7 B, complete.

## 1. What the player sees

Before a line of text is drawn, the engine picks **where** to draw it, and it works in one of two
modes. In one, every run shares a single record. In the other, a run **claims one of exactly two
records for itself** — and if both are already claimed, **the second is reused rather than the
request being refused.** Nothing is ever dropped for want of a target, and that means a reused record
can accumulate work from two different owners.

The whole selection is **skipped entirely when the request repeats** — same two parameters, same
mode, target already resolved — but **only in the shared mode**; a claiming run always does the full
work.

> **`+0x2379` is a mode selector, not a suspend or offscreen flag.** This document originally called
> it "the offscreen flag" and described the zero path as "the screen". **Neither was read here** —
> both were imported from the name. The correction comes from
> [`painting-a-line-of-text-into-a-render-target.md`](painting-a-line-of-text-into-a-render-target.md),
> which weighs **four** readers of the byte against the one this document had: flush and begin stand
> aside when it is set, the transform setter refuses the matrix, and **this function does *more* work,
> not less.** Everything below is what was actually read; the interpretation has been removed.

## 2. Native mechanism

`001E9D20(state, a, b, key)` — `a` and `b` are `int`s, `key` arrives in `r9d`.

### 2.1 It begins by trying to do nothing

```asm
001E9D2A  cmp   qword ptr [rcx], 0
001E9D36  je    0x1e9d50
001E9D38  cmp   eax, dword ptr [rcx + 0x18]      ; a == last a?
001E9D3B  jne   0x1e9d50
001E9D3D  cmp   r8d, dword ptr [rcx + 0x1c]      ; b == last b?
001E9D41  jne   0x1e9d50
001E9D43  cmp   byte ptr [rcx + 0x2379], 0
001E9D4A  je    0x1e9eed                          ; -> plain return, nothing written
```

**Four conditions, all of which must hold to skip the work**, and `001E9EED` is a bare epilogue —
no state is cleared on that path. The last two fields written by a successful call
(`001E9EBB`, `001E9EC6`) are exactly the two this guard compares, so **the memo is closed**: the
function stores the key it will next test.

> **The fourth condition is `+0x2379 == 0`, so the memo only fires in the shared mode.** A run in the
> claiming mode can never take the early return — it does the tree lookup, the allocator and the
> buffer rebuild every time. **That is a fifth site agreeing that the non-zero mode is the one that
> does more work**, and it is inside this function rather than around it.

### 2.2 The descriptor comes from a tree keyed on both arguments

```asm
001E9D50  mov   rcx, qword ptr [rcx + 0xf48]     ; root
001E9D5A  lea   r8,  [rbx + 0xf38]               ; sentinel
001E9D61  shl   rdx, 0x20
001E9D65  or    rdx, rax                          ; key = (b << 32) | a
001E9D70  cmp   qword ptr [rcx + 0x20], rdx
001E9D74  jb    0x1e9d7f
001E9D76  mov   rax, rcx
001E9D79  mov   rcx, qword ptr [rcx + 8]          ; left
001E9D7D  jmp   0x1e9d82
001E9D7F  mov   rcx, qword ptr [rcx]              ; right
001E9D85  jne   0x1e9d70
```

**The two `int` arguments are packed into one 64-bit key** and used to walk an ordered binary tree —
node key at `+0x20`, children at `+0x00` and `+0x08`, mapped value at `+0x28`. The descent keeps the
last node not less than the key and then re-tests it (`001E9D8C`), which is a lower-bound search
followed by an equality check: **a miss lands on the sentinel** and takes the reset path.

### 2.3 The two-slot allocator

Only when `byte [state + 0x2379]` is set:

```asm
001E9DF2  xor   edx, edx
001E9DF4  lea   rax, [rbx + 0x2320]      ; the descriptor array
001E9DFB  mov   qword ptr [rbx + 0x10], rdx
001E9E01  mov   r8d, dword ptr [rax]
001E9E04  test  r8d, r8d
001E9E07  je    0x1e9e1f                 ; slot is FREE -> take it
001E9E09  cmp   r8d, esi
001E9E0C  je    0x1e9e1f                 ; slot already MINE -> take it
001E9E0E  inc   edx
001E9E13  add   rax, 0x2c
001E9E17  cmp   rcx, 2
001E9E1B  jl    0x1e9e01
001E9E1D  jmp   0x1e9e4a                 ; neither -> fall through with a null buffer
001E9E1F  movsxd rcx, edx
001E9E22  imul  rax, rcx, 0x2c
001E9E2A  mov   dword ptr [rax + rbx + 0x2320], esi   ; claim it
```

**First-free-or-already-mine, over exactly two slots** (`001E9E17 cmp rcx, 2`), and the claim writes
the caller's `key` into the slot's first dword. **A slot holding `0` is free** — which is what the
initialiser at `001E73A0` writes.

### 2.3a Nothing releases a slot

The obvious follow-up is what frees one. **Searched image-wide, in the two ways that can hide it:**

| search | result |
|---|---:|
| functions taking a `lea` to the array base `+0x2320` | **2** — `001E71B0` (`001E7396`) and this one (`001E9DF4`) |
| writes at displacement `+0x2320` in any form, indexed included | **1** — `001E9E2A`, the claim |

**Those two functions are the only code that can reach the array**, and in neither does the
materialised pointer escape: there is no call between `001E7396` and `001E73DA`, nor between
`001E9DF4` and `001E9E46`, so it is never handed to a callee that could write through it.

> **So the owner field has exactly two writers image-wide: the initialiser sets it to `0`, and this
> function sets it to a key. Nothing sets it back.** A slot is claimed for the life of the record.
>
> **The consequence is the overflow path in 2.3**: the first two distinct owners take a slot each,
> and **every owner after that shares slot 1** until `001E71B0` rebuilds the record. That is the
> mechanism behind the caution in the sibling document that a reused record accumulates work from two
> owners — it is not an edge case, it is the steady state from the third owner onward.

**This absence is measured, not assumed.** It is stated only because the same two searches
positively return the initialiser, the claim, and both `lea` sites — and because the address
provably does not escape. **Had either search returned nothing at all, this section would say
nothing.**

**When neither slot is available the request is not refused.** `[state + 0x10]` was zeroed at
`001E9DFB`, so `001E9E4A` sees null and takes:

```asm
001E9E51  movsxd rax, dword ptr [rdi + 4]
001E9E55  imul   rcx, rax, 0x38
001E9E59  lea    rax, [rbx + 0x730]
001E9E60  mov    dword ptr [rbx + 0x20], 1     ; slot 1, unconditionally
```

**The overflow path reuses slot 1**, whoever owns it.

### 2.4 The buffer address, and a bound that closes a structure

The selected buffer is

```
state + 0x30 + (slot * 32 + n) * 0x38        where n = [descriptor + 4], 1 <= n <= 31
```

from `001E9E26 shl rcx, 5` (slot × 32), `001E9E35 add rcx, rax` and `001E9E3B imul rax, rcx, 0x38`.
The range of `n` is enforced at `001E9DDD`–`001E9DE3` (`lea eax, [rcx-1]; cmp eax, 0x1e; ja` →
reject), so **`n` is 1 to 31 and index 0 of each block is never used.**

> **Two slots of 32 entries of `0x38` bytes is `0xE00`, and `0x30 + 0xE00 = 0xE30`.** The overflow
> path's literal `state + 0x730` is the same arithmetic for slot 1 (`0x30 + 0x700`), which confirms
> the block size independently of the multiply. **The array therefore ends exactly at `+0xE30`** —
> where a separate reading of `001E8580` finds a 4×4 float matrix beginning. **Two independent
> derivations meet at one boundary**, and neither was looking for the other.

### 2.5 The shared-record path

`byte [state + 0x2379] == 0` skips the allocator entirely: buffer = `state + 0x30 + n * 0x38` and
`[state + 0x20] = 0` (`001E9E6C`–`001E9E7C`). **Block 0 is used without claiming a record**, which is
what makes this the shared mode — nothing here says what block 0 is drawn to.

## 3. Key addresses

| Address | Name | Size | Verified |
|---|---|---:|---|
| `001E9D20` | (render-target selection) | 472 B | **read here, complete — previously unread** |
| `001E9C30` | (setter for `+0x2379`) | 7 B | read here, complete |
| `001E71B0` | (record initialiser) | 717 B | initialiser loop read in context |
| `001B5FB0`, `001B51C0`, `001FDD60` | resource acquisition | — | **not read** *(answered: see UQ-359 in §8: all read; 2026-10-02, OPUS)* |
| `006B5C70`, `005C5310` | buffer rebuild | — | **not read** *(answered: see UQ-359 in §8: plain field getters; 2026-10-02, OPUS)* |

## 4. Data structures

### 4.1 The state object, as far as this function shows it

| offset | what |
|---|---|
| `+0x00` | primary resource, from `001B51C0`; **~~null means the whole call failed~~** *(answered: see §8: "This falsifies §4.1's null means the whole call failed"; 2026-10-02, OPUS)* |
| `+0x08` | secondary resource, from `001FDD60` |
| `+0x10` | the selected `0x38`-byte buffer |
| `+0x18`, `+0x1C` | the memo keys, copied from descriptor `+0x00` and `+0x0C` |
| `+0x20` | the selected slot index, `0` or `1` |
| `+0x30` … `+0xE2F` | **2 × 32 × `0x38` buffers** |
| `+0xE30` | (a 4×4 float matrix, per the sibling document) |
| `+0xF38`, `+0xF48` | tree sentinel and root |
| `+0x2320` | the two `0x2C`-byte descriptors |
| `+0x2379` | **mode selector** — non-zero claims a record, zero shares block 0; `001E9C30` is its 7-byte setter |

### 4.2 The failure path resets five fields

`001E9ED4` clears `+0x00`, `+0x08`, `+0x10`, `+0x18`, `+0x20` — **including the memo keys**, so a
failed call cannot be skipped by the next one. **The reset is what keeps the memo honest.**

## 5. A correction for the sibling document

[`painting-a-line-of-text-into-a-render-target.md`](painting-a-line-of-text-into-a-render-target.md)
corrected its record base from `+0x2324` to `+0x2320` in place. **The absolute column and every
semantic reading are right. The record-relative column was not carried through** — its first two
rows and its last row were updated, the ten between them still measure from `+0x2324`:

| that document says | absolute | correct record offset |
|---|---|---|
| `+0x04` | `+0x2328` | **`+0x08`** — currently duplicates the row above it |
| `+0x08` | `+0x232C` | **`+0x0C`** |
| `+0x0C` | `+0x2330` | **`+0x10`** |
| `+0x10` | `+0x2334` | **`+0x14`** |
| `+0x14` | `+0x2338` | **`+0x18`** |
| `+0x18` | `+0x233C` | **`+0x1C`** |
| `+0x1C` | `+0x2340` | **`+0x20`** |
| `+0x20` | `+0x2344` | **`+0x24`** |
| `+0x24` | `+0x2348` | **`+0x28`** |
| `+0x25` | `+0x2349` | **`+0x29`** |

**The initialiser settles it independently of any base**: `001E73A0`-`001E73CA` writes at
`rax + 0`, `+4`, `+8`, `+0xC`, `+0x14`, `+0x1C`, `+0x20`, `+0x24`, `+0x28` where `rax` is the array
base, and `001E73CA` is the `+0x28`/`+0x29` pair. **The visible symptom is the duplicated `+0x04`.**

## 6. What the census cannot see here, and why it is structural

**The two descriptors do not occupy two sets of displacements.** Both are reached as
`base + index*0x2C + fieldoffset`, so **every access to descriptor 1 is recorded at descriptor 0's
displacement**. Measured: in `+0x2320`…`+0x2377`, the census names **11 offsets, all inside the first
`0x2C` bytes, and none in the second** — not because the second is unused, but because **it is not
addressable by a distinct displacement at all.**

That is a fifth item for the list of ways a field hides, and it differs in kind from the others:

| mode | what is lost |
|---|---|
| base materialised by `lea` | the displacement |
| offset folded into a scaled index | the displacement |
| size or offset passed as a value | the object's extent |
| one store covering two fields | the second field |
| **entry number carried in the index** | **every element after the first** |

**A displacement census over an array reports the element layout, not the array.** Reading a row as
"this field has 11 touchers" is right; reading it as "this record is 11 fields" is not.

## 7. Modding notes

- **There are exactly two claimable records**, and the overflow path silently reuses slot 1. Raising
  the count means the `cmp rcx, 2` at `001E9E17`, the `shl rcx, 5` block stride, **and** the literal
  `+0x730` at `001E9E59`, which encodes the same number a third way.
- **A slot is freed by writing `0` to its first dword.** Nothing in this function frees one.
- **`001E9C30` is a 7-byte setter for the mode byte** — the cheapest place to force every text run
  into one mode or the other.
- **The memo at `+0x18`/`+0x1C` will skip the whole selection.** A hook that changes the descriptor
  without disturbing those two fields will not take effect until the parameters change.

## 8. What is not known

- [x] **UQ-356.** ~~What `a` and `b` are.~~ They are packed `(b << 32) | a` into the tree key and stored as the memo,
      and nothing here names them.
      ***NARROWED 2026-09-17 (FABLE): `b` is a mode in {0, 1, 2}; `a` is a small id whose meaning differs by mode.** The chooser's two wrappers fix `b`: `0017FD00(a)` passes 2, `0017FD30(a, flag, key)` passes 1 when the flag is set and 0 otherwise. Mode 2 entries are registered by `0017FC00`, which packs `a` into the low five bits under a slot index (`(index << 5) + a`, `0017FC1B`..`0017FC1E`), so there `a` is an id below 32; the message-window caller `00364530` passes `11 + byte` (`003645D9`..`003645E0`). Modes 0 and 1 are the glyph-run family: `002A9F00`, `002AA800` and `002AAE40` pass `a = [0209CC30]`, `flag = [0209CC34]` and `key = [0209D480]` (`002AB371`..`002AB388`), the pair the numeric-formatting page calls the queued run's origin cells, and their entries come from `001B4590` (`b = 0`) and `001B6470`. What the id enumerates in each family is not named by a table read here.*
      ***ANSWERED 2026-09-17 (FABLE): `a` is a message-window kind in mode 2 and the text run's origin cell in modes 0 and 1, and every call site says which.** A census of the constant arguments at all call sites of the two wrappers and the registrar: the mode-2 registrar `0017FC00` is called by the message-window registrar `003643A0` with `a` = 11, 13 and 14 (`00364404`, `00364436`, `00364468`) and by the menu-bin requester `00365810` with a computed id (`003658D4`); the mode-2 chooser `0017FD00` is called only by the message-window family (`00364530`, which passes 11 plus a window byte, `003647E0`, `003649A0`, `003655F0`), so in mode 2 `a` enumerates the message-window kinds, 11 upward, and the packed `(index << 5) + a` key is *window kind under slot*. The modes 0 and 1 chooser `0017FD30(a, flag, key)` has eight callers, all in the glyph-run family: `002AC2F0`, `002AC5F0`, `002AF960` and `002B0280` pass `a` = 0 at every constant site (with `flag` 0, and 1 once at `002AD1AB`), and `002A9F00`, `002AA800` and `002AAE40` pass the queued run's origin cell `[0209CC30]` with `[0209CC34]` as the flag, so in those modes `a` is the run's origin cell, 0 for a run drawn at the default origin. So the tree key `(b << 32) or a` reads *mode, then window kind or origin cell*, and the memo caches the last such pair. Static; every call site read.*
- [x] ~~**UQ-357.** What the tree at `+0xF38`/`+0xF48` is populated by — this function only reads it.~~
      ***ANSWERED 2026-09-17 (FABLE): the tree is a map from the packed key to a 16-byte record, filled by one inserter and emptied per id by one eraser.** `001E7F90(state, a, x, y, b)` takes a 16-byte record from the pool at `state+0xE70` (`001BA860`), fills it `{a, x, y, b}` (`001E7FD2`..`001E7FDD`), walks the tree from `+0xF48` with the same lower-bound search on the packed key, `b` shifted up 32 bits over `a` (`001E7FE4`..`001E8010`) and links the node in; its three callers register entries: `0017FC00` with `b = 2` and `x = (001FDF70() << 5) + a`, `001B4590` with `b = 0` and `x = 001FDF70()`, `001B6470` with `b` from its own argument, all on the text state `01F811F8` that `001B5FA0` returns. `001E9A30(state, id)` walks the tree in order from `+0xF40` and, for every node whose record's `+0` equals `id`, decrements the count at `+0xF58`, unlinks the node (`0016DA60`), releases it through the allocator at `+0xF60` (size `0x30`) and returns the record to the pool (`002124C0`): the per-id release. The chooser `001E9D20` is the tree's only other reader. Static, bodies read.*
- [x] ~~**UQ-358.** What the `0x38`-byte buffer holds beyond `+0x00` (a size or id compared against `n`), `+0x08`,
      `+0x10`, `+0x18` and `+0x20`.~~
      ***ANSWERED 2026-09-17 (FABLE): each `0x38`-byte buffer is one vertex batch, and its layout is its constructor's.** The record initialiser `001E71B0` builds the region with the array-constructor helper `00808FE4(state+0x30, 0x38, 0x40, ctor 001E7480, dtor 001E7710)` (`001E71E3`..`001E7201`): sixty-four elements of `0x38` bytes, the two blocks of thirty-two. The element constructor `001E7480` zeroes the dword at `+0x00` and the qwords at `+0x08` and `+0x10`, zeroes three qwords at `+0x18`, `+0x20` and `+0x28`, installs the `eastl::allocator_memory_log` vtable `00902720` at `+0x30` through `001EDF00`, and reserves the object at `+0x18` for 0x400 elements through `001E9AE0` (`001E74BB`..`001E74D4`), whose capacity arithmetic divides by `0x3C`; the destructor `001E7710` frees `(capacity - begin) / 0x3C` elements through the allocator's slot 3 (`001E7737`..`001E775C`). So `+0x18`, `+0x20` and `+0x28` are begin, cursor and capacity of an EASTL vector of `0x3C`-byte glyph vertices, [the painting page](painting-a-line-of-text-into-a-render-target.md)'s open batch (cursor `+0x20`, capacity `+0x28`, vertex `0x3C`), `+0x08` and `+0x10` are the two handles that page says a flush hands to the draw object, and `+0x00` is the state word the chooser compares against `n` (zero is free). Static; constructor, destructor and reserve read.*
- [x] **UQ-359 ANSWERED 2026-09-15 (OPUS) — all five read. They are three field getters and two
      identical tree lookups. Nothing is acquired and nothing is rebuilt, so both labels in §3 are
      wrong.**
      - **`001B5FB0` (33 B) returns the singleton pointer `[01F81200]` — it does not acquire it.**
        Its `call 0016D6A0` is a **3-byte `ret 0`**, an `/OPT:ICF`-folded empty stub, so the
        `setne cl` “already constructed” argument it computes is discarded and **nothing is
        created here**. The creator is the ensure-stub **`001B5F10`** (alloc `0x2380`, ctor
        `001B3940` + `001E71B0`), listed in
        [game-application.md](../../00-Engine-Core-Runtime/Application-Root/game-application.md).
      - **`001B51C0` is a binary-search-tree find by `u32` key.** Root `[rcx+0x40]`, terminator
        `rcx+0x30`, key at `node+0x20`: it descends `[node]` while `node->key < edx` and `[node+8]`
        otherwise, keeping the last non-less node, then returns it only if `edx >= node->key` — an
        exact-match find that returns the terminator on a miss.
      - **`001FDD60` is the same ~~algorithm byte for byte~~ walk with a different exit** *(corrected 2026-10-02, OPUS: a miss returns 0, `xor eax, eax` at `001FDD60`+0x4B, and a hit returns `node + 0x28` at +0x46; the terminator is never returned)*, on the container at `[rcx+0xC0]` with
        terminator `rcx+0xB0`. The caller hands it the node `001B51C0` just returned
        (`001E9DCD mov rcx, rax`), so §4.1's “primary” and “secondary resource” are really
        **one two-level nested lookup** — outer key `[rdi+4]`, inner key `[rdi+8]`.
      - **`006B5C70` is `mov rax,[rcx+8]; ret` (5 B)** and **`005C5310` is `mov rax,[rcx+0x10]; ret`**
        **(5 B)** — plain field getters. The “buffer rebuild” at `001E9E90`–`001E9EB5` is three
        field copies: `[buf+8]` ← `node+0x08`, `[buf+0x10]` ← `node+0x10`, `[buf+0x20]` ← `[buf+0x18]`.
      - ⚠ **This falsifies §4.1's “null means the whole call failed”.** `001B51C0` **cannot return
        null** — it returns either a node or `rcx+0x30`. The `test rax, rax` / `je 001E9ED4` at
        `001E9DC1`–`001E9DC4` can therefore never be taken by a returned value; a null `rcx` would
        already have faulted inside the callee on `[rcx+0x40]`. The branch is dead in any run that
        returns at all.
      - **One tension left open rather than resolved by guess.** If the container is an EASTL
        red-black tree (right `+0x00`, left `+0x08`, parent `+0x10`, value from `+0x20` — which the
        key at `+0x20` fits), then `006B5C70` and `005C5310` are reading the found node's **left-child
        and parent links** into the buffer, which would be an odd thing to copy. Either the container
        is not that layout or the caller reads those fields deliberately. **The bytes do not settle
        it**, and it belongs with `UQ-357`, which already asks what populates the tree. **UQ-359.**
- [x] ~~**UQ-360.** Why `n = 0` is excluded, leaving the first `0x38` bytes of each block unused.~~
      ***ANSWERED 2026-09-17 (FABLE): `n` is the font size, so 0 is not a size, and slot 0 is unused by construction.** The descriptor's `+4` is the second field of the tree record (`x`, stored at `001E7FD7`), which the record initialiser sets to 0 for every descriptor (`001E73A2`), so 0 is the unassigned value; [the painting page](painting-a-line-of-text-into-a-render-target.md) reads the same index from the other end: the flush walks thirty-one batches from index 1 because the batch index is the font size, `1 <= n <= 31`, and slot 0 of each group of thirty-two is never selected. Both readings agree, and nothing else addresses slot 0. Static.*

## 9. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Four-condition memo, returning without writing | `001E9D2A`-`001E9D4A`, target `001E9EED` is a bare epilogue | 1 |
| The memo keys are what a successful call last wrote | `001E9EBB`, `001E9EC6` writing `+0x18`/`+0x1C` | 1 |
| The tree key packs both arguments | `001E9D61 shl rdx, 0x20`, `001E9D65 or rdx, rax` | 1 |
| First-free-or-mine over exactly two slots | `001E9E01`-`001E9E1B`, bound at `001E9E17` | 1 |
| Claiming writes the key into the slot | `001E9E2A` | 1 |
| Overflow reuses slot 1 | `001E9E51`-`001E9E60`, reached only when `+0x10` is still null | 1 |
| Buffer = `+0x30 + (slot*32 + n) * 0x38` | `001E9E26`, `001E9E35`, `001E9E3B`, `001E9E3F` | 1 |
| `1 <= n <= 31` | `001E9DDD`-`001E9DE3` | 1 |
| The array ends at `+0xE30` | the arithmetic above, corroborated by the literal `+0x730` at `001E9E59` | 1 |
| The failure path clears the memo | `001E9ED4`-`001E9EEA` | 1 |
| Descriptor 1 is unaddressable by displacement | 11 named offsets in `[0x2320, 0x234C)`, none in `[0x234C, 0x2378)`, over a 25,234-row census | 2 |

**Control on the "none in the second descriptor" measurement.** The claim is an absence over a
sub-range. The same census **positively returns 11 offsets in the first descriptor and 4 rows at
`+0x2378`/`+0x2379` immediately after the array**, so it is resolving this address region, not
skipping it. The census carries an `index_reg` column, and **every one of `001E8070`'s ten accesses
in this range is indexed** — which is the mechanism, not just the outcome.

## 10. Related

- [`painting-a-line-of-text-into-a-render-target.md`](painting-a-line-of-text-into-a-render-target.md)
  — the descriptor layout, the initialiser, and the flush; section 5 above corrects its
  record-relative column
- [`how-a-line-of-text-becomes-glyph-quads.md`](how-a-line-of-text-becomes-glyph-quads.md) — the
  emitter that fills the buffer this function selects
- [`../../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md`](../../16-UI/Widget-Object-Model/the-widget-constructor-and-object-sizes.md)
  — the other three invisibility modes, and object sizes as a typing filter

## 11. Falsification pass 1 — 2026-09-13 (OPUS)

*(Static only. Nothing executed.)*

### ✔ The structure reproduces, to the address

| claim | measured |
|---|---|
| `001E9D20` is **472 B**, `001E9C30` **7 B** | **472 / 7** |
| two `ret`s at **`001E9ED3`** and **`001E9EF7`** | **exactly those two**, and the 472 bytes end at `001E9EF8`, so there is no padding after the second |
| §2.1's four-condition guard | **instruction for instruction**, including `cmp byte ptr [rcx + 0x2379], 0` as the **fourth** and `je 0x1E9EED` |
| `001E9EED` is a bare epilogue | **`mov rbx, [rsp+0x38]`** — a restore, not a clear |
| "the memo is closed": the last two fields written are the two the guard compares | **`001E9EBB` writes `+0x18` and `001E9EC6` writes `+0x1C`** — exactly the pair compared at `001E9D38` and `001E9D3D` |
| `001E9C30` sets the mode byte | **`mov byte ptr [rcx + 0x2379], dl` / `ret`** — the whole function, and the *only* thing it does |

**The memo argument is the page's sharpest and it is exact.** The guard reads `+0x18`, `+0x1C` and
`+0x2379`; the success path writes `+0x18` and `+0x1C` as its last two stores. A reader does not have
to take "the memo is closed" on trust — the two addresses are four instructions apart at each end.

### ➕ "Exactly two records" is an immediate

§1 says a claiming run takes **one of exactly two** records. The bound is in the body:
**`001E9E17 cmp rcx, 2`** — a literal, not a variable or a table length. (A second bound,
`001E9DE0 cmp eax, 0x1E`, sits earlier on a different path and is **not** read here.)

### ✖ Corrected: 133 instructions, not 130

The 472 bytes disassemble to **133** instructions ending at the `ret` at `001E9EF7`, with **no `int3`
padding** inside the body. The extent, the boundaries and the two `ret`s are right; only the count is
off by three.

**Not claimed.** Anything past §2.1 — the claiming path, the reuse rule and the descriptor pair were
**not re-read**; the five callees (`001B5FB0`, `001B51C0`, `001FDD60`, `006B5C70`, `005C5310`) were
**~~not read at all~~** *(answered: see UQ-359 in §8; 2026-10-02, OPUS)*; and the `0x1E` bound is recorded as present, not as understood. The `+0x2379`
interpretation stays where the page put it — with the four-reader argument on the sibling page, not
here. Nothing executed.

*(Pass 22 adjacency, 2026-09-14: `001E8580` calls the `CoreRuntimeScheduling` body `001A1470`,
`001E8070` calls `Audio` `00225690`, and `00225690` itself is called by `Platform` bodies
`0061F200`/`006209C0`/`0061F710`/`006239C0` (6 edges) — the same yield-plus-shared-accessor shape
as the rest of the text walk, with the audio accessor reached from platform code as well.)*

*(Subtree followup, 2026-09-15 (SWE2-FRONTIER): `001E8580`'s full 21-member callee family is now
opened on
[painting-a-line-of-text-into-a-render-target.md](painting-a-line-of-text-into-a-render-target.md)
— "The `001E8580` exclusive subtree" — including the `009018F0` rung chooser, the `+0x1500` slot
cache this page's `0x38`-stride blocks match, and the transform/vertex-append pipeline.)*

## SWE2-EC7-37 update (2026-09-19) - `001B4590`

`001B4590` (520 B) is the `b = 0` glyph-run entry registrar the page names - `01F811F8` text state, `001FDD60`/`001FDF70` triples plus `001E7F90` pair (the `{a,x,y,b}` tree insert). Interior anchor `001B4652` (an `001FDD60` call).

## SWE2-EC7-46 update (2026-09-19) - `001E9AE0`

`001E9AE0` (225 B) is a body - `001E6F50` plus a `call [r9+0x18]` vcall. Interior anchor `001E9B32` (the `001E6F50` call).

## SWE2-EC7-60 update (2026-09-19) - `001B6470`

`001B6470` (158 B) is a render-target body - `001BA860`/`001E7F90` plus `008F8948`/`01F811F8` and the `"Error :can't add Font By Expand!"` literal. Interior anchor `001B648E` (a `001BA860` call).



## SWE2-EC7-65 update (2026-09-19) - `001B5F10`

`001B5F10` (137 B) is the ensure-stub creator (alloc `0x2380`, ctor) - `0016D6A0`/`001B3940`/`001E71B0`/`00210EC0` plus `01F811F8`/`01F81200`. Interior anchor `001B5F2D` (a `0016D6A0` call).


## SWE2-EC7-67 update - `001E6F50`

`001E6F50` (128 B) is an indirect-only `0x3C`-stride erase-range - `edx!=0` vcalls `[r10+0x10]`, then `movups`/`movsd` 0x3C records down over `[r8..r9)`. Interior anchor `001E6F75` (the `call [r10+0x10]` vcall).

## SWE2-EC7-101 update (2026-09-20) - `002AE450` measured

`002AE450` (448 B) is the position composer `002AC5F0`
and `002B0280` call: `0039BB00(r9d)` resolves the record
whose `+0x20+0x30` block yields two `0xFFF`-masked fields
scaled by `dword[+0x34]`/`+0x38`/`+0x3C` into the
`0209CC60`/`0209CC64`/`0209CC68` position globals,
`byte[+0xAB] + byte[+0x44]` adds a scaled offset, `bl`
bits 1/2/4 add `6.0`/`2.0`/`-6.0`, bit 8 adds `2.0` only
while `00254A10` is quiet, a nonzero `byte[+0xA9]`
overrides `0209CC68` then clears, and `002AFDC0` submits
with `xmm8`/`xmm6`/`xmm9`/`xmm10` - the flag-offset
cursor write the render-target choice lands on.
Interior anchor `002AE5D7` (the `002AFDC0` call).

Cross-subsystem note (pass 22): **Save_Load_Settings —
MECHANICAL (1 edge).** `005832B0` calls `00254A10`, the
shared quiet-check `002AE450`'s bit-8 arm consults.
Fan-in on one predicate, not a save relationship.

## SWE2-EC7-109 update (2026-09-20) - `001FDD60` measured

`001FDD60` (78 B) is the EASTL
map find `001B4590` and
`001E9D20` run: the same
lower-bound walk as `0020B5F0`
but rooted at sentinel
`rcx + 0xB0` / head
`qword[rcx + 0xC0]`, keyed by
`edx`, and it inserts nothing -
hit returns `node + 0x28`, miss
returns 0.
Interior anchor `001FDD76` (the
`dword[r8 + 0x20]` compare loop
head).

`001E78D0` (335 B) is the link walk `001E7F90` calls: `rcx + 8` chain, `[r8]` vs `rbx`/end sentinel checks, `0016D6D0` resolves each node and `[r14]`/`[rbp]` compare the pair - the text run's target fetch.

Interior anchor `001E7905` (function `001E78D0`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-EC7-163, 2026-09-22)

**Platform — SERVICE (17 edges).** The container/link helpers this page's
`001E78D0` walk runs (`0016D6D0`/`0016DA60`) are called from Platform —
`0019CC50`/`001B1960` among them (+13 more). Shared-accessor fan-in, not a
platform relationship to the text run.

**Resource — SERVICE (25 edges).** The same helpers are called from the
Resource layer — `0016D6D0`/`0016DA60` by `0020B840`/`0020BFA0`/`006761F0`
(+21 more). Same mechanical fan-in.

`001E7770` (346 B) is the ordered-map insert `001E78D0` calls: walks the `rcx+0x18` red-black tree comparing `*r8` against node `+0x20` (left `+0x00`/right `+0x08`), `0016D720` rebalances on the `rcx+0x10` head, then a `rax+0x10` virtual call on `[rcx+0x30]` allocates the node - the text-run registry's std::map-style insert.

Interior anchor `001E7830` (function `001E7770`).

`001E7C90` (156 B) is the same-shape adapter `001E78D0` runs - the qword-compare twin of the `001FB5C0` arm: `esi` from `qword[r8+0x20]` vs `[r9]`, `[rcx+0x30]`'s `+0x10` virtual at `edx = 0x30`, a 16-byte `r9` copy into `[rax+0x20]`, `0016D840(r14, rdi, rbx+8, esi)`, `[rbx+0x28]` bumped, `r14` stored to `[r15]`.

Interior anchor `001E7D05` (function `001E7C90`).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

This page describes unowned code in the residual folder, and it cites the bodies that supply or consume that code. Each layer below arrives with those bodies' other call edges. The page claims only the mechanism it reads, not the layers they touch.

**Save_Load_Settings — MECHANICAL, 3 edges.** `00254A10` is called by `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`); `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`) calls `SavePath_BuildSlotAssetName` (`005837F0`); `SaveSlotMetadata_BuildSubmissionDescriptor` (`005832B0`) is called by `SaveSlotTransaction_StateMachine` (`00581DA0`).

**UI — MECHANICAL, 35 edges.** `00254A10` is called by `00273E30`, `00295D90`, `00298250`, `002A4430` and 8 more; `002AC2F0` is called by `002AE610`, `002AF340`, `002B2150`; `0017FD30` is called by `002AC5F0`, `002AF960`; `002A9F00` is called by `002AC5F0`, `002AE610`; `002AAE40` calls `002AC5F0`, `002B2150`; `002AC5F0` calls `002AE610`, `002B2150`; `002AC5F0` is called by `002AF340`, `002B2150`; `002AF960` is called by `002A4430`, `002A4830`; `002B0280` calls `002AE610`, `002B2150`; `002B0280` is called by `00243860`, `002A86A0`; `001A1470` is called by `0018EEE0`; `002A9F00` calls `002AC5F0`; `002AE450` is called by `002AC5F0`; `002AF960` calls `002B2150`.

*Tier 2: ledger names and `edges.tsv`; no body read for this note (OPUS, 2026-09-29, pass-22 slice OPUS-P22-SLICE-24-99).*
