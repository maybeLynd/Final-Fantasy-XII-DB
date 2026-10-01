---
contract: Read and byte-order the packed namespace every .phyre file carries
category: 22-Middleware-PhyreEngine
scope: subsystem
level: L2
readiness: CONTRACT READY
confidence: PROVEN
implements: the-packed-namespace-and-the-file-side-schema.md
entries: ["0059A6F0", "0059C180", "0059A780", "0059A8B0", "0059A3B0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 33 addresses cited - 3 data, 5 entry, 25 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-phyre-packed-namespace-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — read and byte-order the packed namespace

> **Authored 2026-09-12 by OPUS.** The mechanism, the decoded table and the corpus arithmetic are
> the source page's,
> [the packed namespace and the file-side schema](the-packed-namespace-and-the-file-side-schema.md),
> which carries an audit pass. This states it as an interface and adds what re-reading the three
> swap routines gives: **each of the namespace's three regions has its own swap routine, and each
> one's shape matches that region's record shape.** The page says the swap routine is the structure
> written as code; all three halves of that are now verified against the image.
>
> Continues [the cluster header contract](CONTRACT-phyre-cluster-header.md), whose `PH-3` asked
> what `0059A6F0` bounds. **It bounds nothing** — which is why what the namespace *is* matters.

## 1. Purpose

**Every `.phyre` file carries its own schema, in plain ASCII, immediately after its 84-byte header.**
Open any of the game's 35,984 asset files, skip 84 bytes, and it names every class it contains and
every field of every class.

For a player, nothing. For anyone editing FFXII's models, textures or animations, **it is the
difference between guessing at a format and reading it** — and it is checkable: a rebuilt file that
no longer declares what it used to declare is wrong long before the game refuses it.

## 2. Interface

| | |
|---|---|
| reader | `0059A6F0`, 116 bytes — `int Read(Stream *rcx, bool wasByteSwapped dl, void *buffer r8, uint32 len r9d)` |
| where | bytes `[m_size, m_size + m_packedNamespaceSize)` of the file; in every shipped file that is `[84, 84 + size)` |
| returns | `0` success · `9` short read. **Nothing else.** |
| its one caller | `0059A3B0`, from all three of its size paths |
| fixup | `0059C180`, 202 bytes, called only when the header was byte-swapped; its only caller is `0059A6F0` |

**The reader is a single bulk read of a self-describing blob.** No parsing, no validation, no bound
of its own — the guards are a zero length and a null buffer, and **both succeed**. Whatever the
namespace contains, the loader has already accepted it by the time anything looks at it.

## 3. Types and state

### The block

> **Declared in `_types` 2026-09-25 (OPUS)** as `PhyrePackedNamespaceHeader` (0x20), `PhyrePackedNamespaceClassRecord`
> (0x24) and `PhyrePackedNamespaceMemberRecord` (0x18), placed by `0059C180`'s own arithmetic. Widths come from the code;
> word meanings beyond the three counts that routine walks come from the corpus below and are marked as data.

```
+0x00  u32       0x01020304            a byte-order mark, stored 04 03 02 01
+0x04  u32       namespaceSize         repeats m_packedNamespaceSize from the header
+0x08  u32       nTypes                (A)
+0x0C  u32       nClasses              (B)
+0x10  u32       nMembers              (C)
+0x14  u32       stringPoolSize        (D)
+0x18  u32       0 in every shipped file (35,984/35,984, §15)
+0x1C  u32       0 in every shipped file (35,984/35,984, §15)
+0x20  u32[A]                          string-pool offsets of type names
       class[9 words] x B              36 bytes each
       member[6 words] x C             24 bytes each
       char[D]                         NUL-separated ASCII
```

> **The byte-order mark is the namespace's own, separate from the header's `RYHP`.** Two independent
> endianness statements in the same file, four bytes and eighty bytes apart. ~~and the loader acts on
> the header's, not on this one.~~ *Corrected 2026-09-26 (FABLE): the byte-order **fixup** acts on the header's; the
> load path then **checks** this one (`0059E167`, §14 `NS-4`).*

### The class record — 9 words, 36 bytes

| word | meaning |
|---|---|
| `w0` | **1-based index of the parent class in this same table**, 0 for a root. `PTexture2D` → `PTexture2DD3D11` → `PTexture2DBase` → `PTextureCommonBase` → `PBase` |
| `w1` | a packed word: a kind nibble `0x2`/`0x3`/`0x4` over the class's instance size in bytes for the `0x2` family — **84 / 72 / 36 for the three header classes**, and 0 for `PBase`. *Extended 2026-09-26 (FABLE): in all 147 packed-layout classes, of kinds 1–4, the low 28 bits are the cumulative packed size, meaning the parent's size plus the members' widths (see the member-record note).* |
| `w2` | **name**, a string-pool offset |
| `w3` | **member count** |
| `w4`, `w5`, `w6`, `w8` | zero in all 684,244 shipped records |
| `w7` | a **per-class flags word**: five observed bits (`0x02`, `0x04`, `0x08`, `0x10`, `0x20`) combined as 0, 2, 8, 12, 20, 32, 34, 40 — constant per class name across the whole corpus, correlated with but not determined by `w1`'s kind nibble (§14 `NS-1`) |

### The member record — 6 words, 24 bytes

| word | meaning |
|---|---|
| `w0` | **name**, a string-pool offset |
| `w1` | a type reference: a **0-based type-table index** when `< nTypes`, otherwise `nTypes +` the class's 1-based id |
| `w2` | ~~**byte offset of the field within the class**~~ **the member's byte offset in its class's file-side layout** *(corrected 2026-09-26, FABLE: see the note below this table)* |
| `w3` | ~~element size in bytes — 4 for a `u32`, 1 for a byte~~ **the member's width in that layout** — 4 for a `u32` and 1 for a byte, but also 1 for an object pointer and 5 for a `PArray` in a packed class *(corrected 2026-09-26, FABLE)* |
| `w4` | attributes — ~~**bit 31 marks a pointer**~~ **the reflection attribute word. Bit 1 marks an object pointer (2,306 records without bit 31); bit 31 marks the counted-buffer members `PArray::m_els`, `PSharray::m_u` and `PString::m_buffer`, with bit 1 then meaning pointer elements.** Bits 3–4 carry the runtime registration's values; bit 5 (enum fields) and bit 6 (`PSharray::m_u`) are file-only. *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from the source page's 169-file join to the runtime field schema.* |
| `w5` | **fixed-array bound** — the C array element count, 0 for a scalar. `float m_elements[16]` on `PMatrix4`, `[12]` on `PMatrix4x3`, `[4]` on `Vector3`; `float m_min[3]`/`m_size[3]`; `PUInt16 m_parameterStart[4]`; `RenderTarget[8]` on `CD3D11_BLEND_DESC` = `D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT`. Non-zero in 21,459 of 2,192,621 shipped members (§14 `NS-3`) |

**Two layouts; `w2`/`w3` describe the one the class uses** *(2026-09-26, FABLE, Claude Opus 5.5.)*
The control is `members/w3_census.py` over the full archive (35,984 files, 2,192,621 members),
with FAILS 0. Of the 154 classes with members:

- **147 use a packed layout.** Sorted by `w2`, a class's members are contiguous with no padding. They start at the
  parent's packed size and end at the class word `w1`'s low 28 bits. In this layout an object pointer is 1 byte wide
  and a `PArray` 5, so `w2` is **not** the runtime offset: `PMaterial`'s members sit at 0, 1, 2, 6 and 7 in the file
  and at 0x0, 0x8, 0x10, 0x18 and 0x20 in the runtime registrations.
- **6 use the native layout**: `PParameterBuffer`, the four `PShaderParameterCaptureBuffer*` classes and
  `PModifierNetworkInfoPacket_ModifierCode`. There pointers are 8 bytes wide and a `PArray` 16. Every member joined
  to a runtime registration has `w2` equal to its runtime offset (10 of 10).
- **1 fits neither**: `PAnimationClipBindingDataBlockCache`. Its two reflected members sit at 16 and 20 in a 24-byte
  class, so its first 16 bytes are unreflected.

The records are not stored in offset order (`PLODGroup` lists `m_levels`, at 42, first). This table does not trace
what reads the packed layout, whether the instance data or only a tool. The header classes' fields are all `u32`,
where the two layouts coincide, which is why the 3,042 header-offset checks matched.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The caller supplies the length from the header and a buffer at least that large.
`0059A3B0` is the only caller and does both — the buffer is **aligned storage from `_aligned_malloc`**
at alignment 4, released through `_aligned_free`, both named from the import table in
[the cluster header contract](CONTRACT-phyre-cluster-header.md) §5.

**Postconditions.** `len` bytes are in the buffer, `stream->bytesConsumed` has advanced by what was
actually read, and — if the header was byte-swapped — the block has been byte-ordered in place.

**Invariants.**

1. **The size closes exactly:**

   > `0x20 + 4·A + 36·B + 24·C + D == m_packedNamespaceSize`

   in **35,984 / 35,984 shipped files, to the byte** — the whole archive, not a sample. This is
   the strongest single check a rebuilt namespace can be given, and it is arithmetic rather than
   a heuristic.
2. **`sum(class[i].w3) == nMembers`,** and members are stored **contiguously in class order** — class
   *i* owns the next `class[i].w3` member records. That is the entire class-to-field mapping.
3. **The reader validates nothing.** A namespace whose counts do not close, whose offsets point
   outside the pool, or whose parent indices form a cycle is read without complaint.
4. **A short read still advances `bytesConsumed`,** and still byte-swaps what arrived (§7).

## 5. Relationships

`0059A3B0` → `0059A6F0` → the stream's vtable `+0x28`, then `0059C180` → `0059A780` and `0059A8B0`.

## 6. State transitions

None. The block is transformed in place once, or not at all.

## 7. The swap routine is the structure written as code — and there are three of them

`0059C180` has to know the layout in order to byte-order it, so it *is* the layout. **Re-read for
this contract, and the important part is that each region gets a different routine whose shape
matches that region's records:**

| region | routine | shape, from the instructions |
|---|---|---|
| the 8-word header | inline in `0059C180` | **eight `bswap`s, one per fixed dword** (*"fourteen" corrected 2026-09-25, OPUS - counted at `0059C18B`...`0059C1C2`*) at `+0x00`…`+0x1C` — `0059C186`–`0059C1C4` |
| `u32[A]`, the type table | `0059A8B0` (246 B) | an **SSE-vectorised** loop — `cmp ecx, 8 / jb` to a scalar tail, then `movdqu`/`movdqa` with shuffle constants — which is what a **flat `u32` array** gets and nothing else would |
| `class[B]` | `0059A780` (294 B) | a loop striding **`0x24` = 36 bytes**, swapping **nine** words per record; the first is an inlined byte-reversal, the rest `bswap` |
| `member[C]` | inline in `0059C180` | a loop at `0059C200`–`0059C230` striding **`0x18` = 24 bytes**, swapping **six** words |

```asm
0059C1C7  mov  eax, [rcx+8]       ; A
0059C1CE  lea  rdx, [rcx+rax*4]   ; &ns[0x20 + 4A]      -> the class records
0059C1D2  mov  ecx, [rcx+0xc]     ; B
0059C1D5  call 0x59A780           ; nine words each
0059C1DD  lea  rcx, [rax+rax*8]   ; B*9                 -> class records ARE nine words
0059C1EF  mov  ecx, [rbx+0x10]    ; C
0059C200..0059C230                ; six words each, rax += 0x18
0059C239  mov  ecx, [rbx+8]       ; A
0059C245  jmp  0x59A8B0           ; the type table, vectorised
```

> **Three regions, three record widths, three swap shapes, and they agree.** The stride `0x24`, the
> `B*9` scale and the `0x18` stride are not inferred from the data — they are in the instructions,
> and the corpus arithmetic in §4 closes on the same numbers from the other side.

**The string pool is not swapped**, which is correct for NUL-separated ASCII and is a fourth
agreement: the routine stops where the text begins.

## 8. Script · resource · event interactions

None. The namespace is authored data read at load time; no script reaches it.

## 9. Determinism

Fully deterministic given the bytes.

## 10. Failure paths and edge conditions

| # | condition | result |
|---:|---|---|
| 1 | `len == 0` | **0** — nothing read, success |
| 2 | `buffer == NULL` | **0** — nothing read, success |
| 3 | the stream returns fewer than `len` bytes | **9**, and `bytesConsumed` has already advanced |
| 4 | anything wrong with the contents | **not detected**; see invariant 3 |
| 5 | counts that do not fit the block, reaching `0059C180` | **the routine walks off the buffer and faults** |

> **Row 5 is observed, not inferred.** A case was written for the pilot with a block whose header
> was little-endian while its regions were not — so the header swap produced enormous counts — and
> the original **faulted at `0059A790`, the first load of the class-record loop**
> (`Invalid memory read`). The case was withdrawn, because a fault cannot be compared against a
> return value; what it demonstrates is invariant 3. **The swap routine trusts the counts it just
> swapped, and nothing checks that they fit.** A malformed namespace is an access violation, not a
> rejection.

> **Row 3 still byte-swaps.** `0059A748`'s swap is gated on the buffer and the `wasByteSwapped`
> flag, **not on the result**, so a truncated namespace is transformed before the failure reaches
> the caller — over whatever bytes happened to arrive.

> **Rows 1 and 2 return success for doing nothing**, and row 2 is reachable: the header ladder
> installs a null buffer whenever `m_packedNamespaceSize` is 0 against a non-matching capacity. It
> refuses that case itself (`CONTRACT-phyre-cluster-header.md` §10 row 5a) **before** calling this
> reader, so the null path here is defensive rather than reachable through its one caller.

## 11. Observable behaviour

A buffer of bytes, a return code, and an advanced counter. Nothing is parsed, so nothing else is
observable until a consumer walks the table.

## 12. Reproduction formula

```c
int PackedNamespace_Read(Stream *s, bool wasByteSwapped, void *buf, uint32 len)
{
    int result = 0;
    if (len != 0 && buf != NULL) {              /* 0059A710 / 0059A715 - both succeed */
        int n = s->vtbl.read(s, buf, len);
        s->bytesConsumed += n;                  /* 0059A726, before the test */
        result = (n == len) ? 0 : 9;            /* 0059A72B cmp / mov ebx,9 / cmove */
    }
    if (buf != NULL && wasByteSwapped)          /* 0059A73B / 0059A740 - NOT gated on result */
        PackedNamespace_ByteSwap(buf);          /* 0059A748 call 0059C180 */
    return result;
}

void PackedNamespace_ByteSwap(uint32 *ns)       /* 0059C180 */
{
    for (int i = 0; i < 8; i++) ns[i] = bswap32(ns[i]);   /* the header, unrolled */
    uint32 A = ns[2], B = ns[3], C = ns[4];
    SwapClassRecords(&ns[8 + A], B);            /* 0059A780: 9 words, stride 0x24 */
    uint32 *m = &ns[8 + A + 9 * B];
    for (uint32 i = 0; i < C; i++)              /* inline: 6 words, stride 0x18 */
        for (int w = 0; w < 6; w++) m[i * 6 + w] = bswap32(m[i * 6 + w]);
    SwapU32Array(&ns[8], A);                    /* 0059A8B0: vectorised */
    /* the string pool is NOT swapped */
}
```

> **The order is not the layout order.** The class records are swapped *before* the type table, even
> though the type table comes first in the block — because `0059C180` needs `A` and `B` from the
> already-swapped header to find the later regions, and the type table is a tail jump. A
> reimplementation that swaps in layout order produces the same bytes and a different trace.

## 13. Runtime validation

**Evidence class: isolated original-code, and unusually complete — NOTHING IS SCRIPTED.**

**Executed 2026-09-12** by [`diff_phyre_namespace.py`](../../../../Reconstruction/Tests/Differential/diff_phyre_namespace.py)
against [`phyre_namespace.c`](../../../../Reconstruction/Game/Resource/phyre_namespace.c) — the
thirty-seventh pilot. **29 cases, 0 mismatches** against the shipped bytes at their real
virtual addresses under Unicorn.

**All three routines run, and so does the SSE.** `0059C180`, `0059A780` and `0059A8B0` are pure
in-place transforms with no callees outside each other, so there is **nothing to stub** — and the two
shuffle constants `0059A8B0` loads from `.rdata` at `00D27A80` and `00D27A90` are mapped from the
image, so its **vector body executes** rather than being stepped around. This is the first pilot in
the database with no scripted callee at all.

**The whole block is compared, byte for byte.** A region swapped at the wrong offset, with the wrong
stride, or in the wrong order differs in bytes; there is nothing to hide behind. 27 of the 29 cases
change the block, and the two that do not are the empty ones.

| what ran | cases |
|---|---:|
| `0059C180` end to end, with A, B and C distinct so no two region boundaries coincide | 11 |
| `0059A8B0` alone at 0, 1, 2, 3, 7, 8, 9, 15, 16, 17, 31, 32, 33 — **8 on the vector path, 4 on the scalar tail** | 13 |
| `0059A780` alone, to pin the `0x24` stride and the nine words | 4 |
| a count above 65535, whose type table alone is 256 KB | 1 |

**Mutation campaign: 64 points — 43 KILLED, 4 SURVIVED,
17 EQUIVALENT, 0 INVALID.** Survivors fell **10 → 7 → 4** across three runs.

### What the campaign forced, and it was the same lesson twice

**Every count in the first case set was small, so the upper bytes of a count were permanently zero
and any mis-assembly of them was invisible.** Counts of 300 and 258 killed the mutations of the
second byte; a count of 65,600 — a 256 KB type table, one case — killed the third. **Three runs, and
each one exposed a byte the previous case set could not reach.**

### The four survivors

- **Two are kind B, fixture scaffolding.** Both are bounds this reconstruction adds and the original
  does not have: `bytes < 32` and `need > bytes`. §10 row 5 records what the original does instead.
- **Two are kind D, and they are open.** They mutate the **fourth** byte of a count —
  `p[3] << 24`. Killing them needs a count above `2^24`, which is a **64 MB type table**: not a
  namespace any `.phyre` file could carry, and not something this fixture will be inflated to hold.
  **They are recorded as an open suite gap rather than adjudicated away**, because the reason is
  cost, not equivalence — the original's single `mov eax, [rcx+8]` reads all four bytes and would
  differ if it could be driven.

> **The bug the long cases exposed twice was in the fixture, not the engine.** The driver's `sscanf`
> field width was a literal that did not track its buffer size, so every long case was silently
> truncated — and it surfaced as *the reconstruction refusing on its own bound while the original
> proceeded*, which reads like a real disagreement. The width is now **derived from the buffer
> macro**: a literal that has to be kept in step with a constant eventually will not be.

**What this does NOT establish: the MEANING of any word.** That class `w0` is a parent index, that
`w1` packs a kind over an instance size, that member `w4` is the attribute word (bit 1 an object pointer, bit 31 a
counted buffer; *“bit 31 marks a pointer”* until 2026-09-26) — those are the
source page's corpus findings, now extended to the whole archive: 35,984 files, 684,244 class
records, 2,192,621 member records. **A byte-order transform cannot confirm any of them**, and
this suite does not claim to.

Receipts: `Database/Tools/work/OPUS/litsuffix/phyre_namespace`, `phyre_namespace2` and
`phyre_namespace3` (ignored path), and the counts row in
[`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md). The full-archive
structural census is reproduced by
`Database/Tools/analysis-kit/gfz-scripts/census_phyre_namespace_vbf.py` (in-memory VBF extraction,
no game code executed); per-record dump at
`Database/Tools/work/SWE2-CONTRACT/phyre_ns_census.json`.

## 14. Unresolved

1. **`NS-1`** — class word `w7`, narrowed by the full-corpus census (§15). It is a **per-class
   flags word**: five observed bits (`0x02`, `0x04`, `0x08`, `0x10`, `0x20`) occurring as 0, 2, 8,
   12, 20, 32, 34, 40 — **constant per class name with zero conflicts across all 35,984 files**,
   and correlated with but not determined by `w1`'s kind nibble (kind `0x2` → 32 dominant, `0x3` →
   8 dominant, `0x4` → 2 dominant; `34 = 32|2`, `40 = 32|8`, `12 = 8|4`, `20 = 16|4` combine
   flags). The bit **names** are still unknown — the swap routine (`0059C180`/`0059A780`) only
   byte-orders the word; the semantic consumer is the object-binder, which this contract does not
   cover. Four other class words (`w4`, `w5`, `w6`, `w8`) are zero in all 684,244 shipped records —
   **unused by this corpus** rather than unidentified.
   **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): `w7` is the file copy of the runtime class descriptor's `+0xFC` flag byte.
   Four bits are named, and the loader acts on two of them.** Control: [`ns1_w7_flags.py`](../../_index/candidates/ns1-class-word-w7/ns1_w7_flags.py) (5 checks, FAILS 0). First
   read by a delegated read-only pass; re-derived here.
   - **The join.** 115 corpus classes also have a carried runtime descriptor row. In all 115, `w7 & 0x0E` equals
     the `+0xFC & 0x0E` their descriptor's final template leaves. So the bits carry [the reflection page](../Reflection-And-Class-Metadata/class-descriptor-and-metadata-system.md)'s names: **`0x02`
     abstract, `0x04` header, `0x08` no default constructor.** Bit `0x10` is set exactly on the two `Header`
     classes in the corpus, which matches that page's registrars.
   - **What the loader does with them.** The namespace binder walks the class records at stride `0x24` and tests
     two bits of this word:
     - **`0x01`, "dynamic class".** When the runtime has no class of that name, a set bit builds a descriptor
       from the file instead of warning `File refers to compiled class '%s' which does not exist in the current
       runtime`. It is set in **no** shipped class.
     - **`0x04`, header.** In the instance-list walk, a class with no runtime descriptor refuses the whole file
       with **6** when the bit is set; when it is clear, the class's instances are dropped. The packed-offset
       resolver tests the bit again.
   - **`0x10` and `0x20` have no reader that was found.** Image-wide, no instruction isolates bit 4 or 5 of a
     `+0xFC` word in the reflection or loader code, directly or after a load. The only such tests are in actor-
     record code, which is a different structure. Control: the same sweep finds `PCluster::create`'s bit-3 test.
     So these two bits are set by member registrars, copied into every file, and read by nothing found. No use
     names them. Blind spot: the word read through a getter and tested in a caller.
2. **`NS-2` — resolved.** `+0x18`/`+0x1C` are zero in **all 35,984 shipped files**, not just the
   169-file sample — reserved header words. The reader byte-swaps them unconditionally along with
   the rest of the eight-word header, so they are layout space, not a dormant feature flag.
3. **`NS-3` — resolved.** Member word `w5` is the **fixed-array bound**: the declared C array
   element count, 0 for a scalar. The full-corpus census finds it non-zero in 21,459 of
   2,192,621 members, and every distinct value sits on a member whose declared shape is that
   fixed array: `PMatrix4.m_elements` = `float[16]`, `PMatrix4x3.m_elements` = `float[12]`,
   `Vector3.m_elements` = `float[4]`, `PMeshInstanceBounds`/`PSkeletonJointBounds` `m_min`/`m_size`
   = `float[3]`, `m_parameterStart`/`m_parameterCount` = `PUInt16[4]`,
   `CD3D11_BLEND_DESC.RenderTarget` = element class × **8** = `D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT`
   (with `w3` = 29, ~~= `sizeof(D3D11_RENDER_TARGET_BLEND_DESC)`~~ *corrected 2026-09-26 (FABLE): the struct's packed width, seven 4-byte fields and a 1-byte mask; its `sizeof` is 32*, the D3D11 struct mirrored
   verbatim). `m_elements` is the only member name taking multiple values ({4, 12, 16}), one per
   owning class — exactly what an array bound predicts.
4. **`NS-4` — answered 2026-09-26 (FABLE, Claude Opus 5.5): the loader does read it.** ~~why the namespace carries its
   own byte-order mark when the loader never reads it. The fixup is driven entirely by the header's marker test.
   Either the mark is for a tool outside the game, or a reader exists that this database has not found.~~
   - The byte-order **fixup** is driven by the header's marker, as §7 says.
   - After the header reader returns, its only caller `0059E070` tests the namespace's first dword against
     `0x01020304` (`0059E167`). A mismatch returns 6, the header reader's own refusal code (`0059E295`).
   - The same body then requires the namespace's self-size `+0x04` to equal
     `0x20 + [+0x1C] + 4·(nTypes + 9·nClasses + 6·nMembers) + [+0x14]` (`0059E173`–`0059E191`).
   - So the mark is the post-fixup check that the namespace's words came out in the order the header promised.
   - The namespace page has recorded the check since `b3d6f43df` (2026-09-14). This item was not updated then.
   - Scope: it is the only `.text` compare against `0x01020304` in the image
     (`_index/candidates/ns4-bom-reader/bom_reader.py`, with the header marker's two compares as the known positive).
   (Strengthened by §15: the mark is `0x01020304` in **all** 35,984 shipped files, so every shipped cluster passes.)
5. **`NS-5` — resolved.** The 169 files were a development extract; the shipped corpus is **35,984
   `.phyre` members of `FFXII_TZA.vbf`** (of 89,414 entries). A structural census over the whole
   archive — via `agent_flow/tools/vbfextract.py` in-memory extraction — confirms every format
   claim corpus-wide: BOM `0x01020304` in 35,984/35,984, the size equation closes in 35,984/35,984,
   zero parse failures, 684,244 class records, 2,192,621 member records. The page's name census
   (19 type-table names, 177 class names, 349 field names) was already corpus-wide; the structural
   figures that were "169/169" are now 35,984/35,984.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the reader is 116 bytes, reads in one call, and validates nothing | **re-read**: `0059A6F0` whole — guards at `0059A710`/`0059A715`, one `call qword ptr [rax+0x28]` at `0059A723`, no other branch | 1 | PROVEN |
| it returns only `0` or `9`, and `9` only for a short read | **re-read**: `0059A72B cmp eax, esi` / `mov ebx, 9` / `cmove ebx, ecx` | 1 | PROVEN |
| `bytesConsumed` advances before the test | **re-read**: `0059A726 add dword ptr [rbx+0x18], eax` precedes `0059A72B` | 1 | PROVEN |
| the swap fires even on a short read | **re-read**: `0059A73B`/`0059A740` gate on the buffer and the flag only; the result was already computed at `0059A72D` | 1 | PROVEN |
| the block is a 6-field header, two zero words, three regions and a string pool | the source page's §8, from `0059C180`'s own addressing | 1 | PROVEN |
| **`0x20 + 4A + 36B + 24C + D == m_packedNamespaceSize` in 35,984/35,984 shipped files** | full-archive census over every `.phyre` member of `FFXII_TZA.vbf` via `vbfextract.py` — **file-side arithmetic, no code executed** | 1 | PROVEN |
| **BOM `0x01020304` in 35,984/35,984; `+0x18` = `+0x1C` = 0 in 35,984/35,984** | same full-archive census; the reserved header words are universally zero, so `NS-2` is closed | 1 | PROVEN |
| **member `w5` is the fixed-array bound** | full-archive census: non-zero in 21,459/2,192,621 members, values {2,3,4,8,12,16,23}; each lands on a member whose declared shape is that array (`float[16]`/`[12]`/`[4]`/`[3]`, `PUInt16[4]`, `RenderTarget[8]` = `D3D11_SIMULTANEOUS_RENDER_TARGET_COUNT`, `esz` 29 = `sizeof(D3D11_RENDER_TARGET_BLEND_DESC)`) | 1 | PROVEN |
| **class `w7` is a per-class flags word, not per-record noise** | full-archive census: five observed bits, constant per class name (zero conflicts corpus-wide), kind-nibble-correlated but not determined; bit names unresolved — the reader only swaps it | 1 | PROVEN (structure) / UNKNOWN (bit names) |
| class `w4`, `w5`, `w6`, `w8` are zero in all 684,244 shipped records | same census | 1 | PROVEN |
| class records are 9 words of 36 bytes | **re-read by me**: `0059A780` strides `lea rax,[rax+0x24]` and swaps nine words per iteration; `0059C1DD lea rcx,[rax+rax*8]` scales `B` by 9 | 1 | PROVEN  **§15a: nine confirmed — but only FIVE use `bswap`.** The other four (`[rax-0x2c]`, `-0x1c`, `-0x18`, `-0x14`) are open-coded as `shl 0x10` / `and 0xff00` / `or` / `shl 8` / `sar 8` / `sar 0x18`. **Counting `bswap` to audit this claim returns 5 and looks like a defect** |
| member records are 6 words of 24 bytes | the source page's `0059C200`–`0059C230` loop, `rax += 0x18`, six swaps | 1 | PROVEN |
| **the type table is a flat `u32` array, and its swap is vectorised** | **re-read by me**: `0059A8B0` branches at `cmp ecx, 8 / jb` to a scalar tail and otherwise uses `movdqu`/`movdqa` with `.rdata` shuffle constants — a shape only a uniform `u32` array admits | 1 | PROVEN |
| the string pool is not swapped | **re-read by me**: `0059C180` ends at the type-table tail jump; no routine touches `[pool, pool+D)` | 1 | PROVEN |
| the swap order is not the layout order | **re-read by me**: classes at `0059C1D5`, members inline, type table last at `0059C245 jmp 0x59A8B0` | 1 | PROVEN |
| class `w0` is a 1-based parent index, `w2` a name offset, `w3` a member count | the source page's §8 — every column tested by whether it lands on the first byte of a NUL-terminated name across all records | 1 | PROVEN |
| member `w0` name, `w1` type reference, `w2` offset and `w3` width in the file layout of the class (packed for 147 of 154 classes), `w4` the attribute word (bit 1 object pointer, bit 31 counted buffer) | the source page's §8; `w4` corrected 2026-09-26 (FABLE, Claude Opus 5.5) from *bit 31 = pointer*, which missed the 2,306 object pointers that carry bit 1; `w2`/`w3` corrected the same day from *field offset* and *element size*, with the control `members/w3_census.py` | 1 | PROVEN |
| `sum(class.w3) == nMembers`, members contiguous in class order | the source page's §8; recounted in the full-archive census, 35,984/35,984 | 1 | PROVEN |
| the namespace's field list agrees with the reflection registrations | the source page — two independent sources, neither derived from the other | 1 (static) | PROVEN |
| **the swap routine has no bound and faults on counts that do not fit** | **observed**: a pilot case with a little-endian header produced enormous counts and the original faulted at `0059A790` with `Invalid memory read`; the case was withdrawn as uncomparable and the observation kept | 1 | PROVEN |
| class `w7` bit names | **not established** — the swap routine byte-orders it; the semantic consumer is the object-binder outside this contract | none | UNKNOWN (`NS-1` residual) *(superseded 2026-09-26 by the next row)* |
| **class `w7` is the runtime class descriptor's `+0xFC` flag byte: `0x01` dynamic class, `0x02` abstract, `0x04` header, `0x08` no default constructor; `0x10`/`0x20` set, no reader found** | **read and joined** (static, 2026-09-26, (FABLE, Claude Opus 5.5)): 115 of 115 joined classes agree on `0x0E`; the binder tests `0x01` and `0x04`; image-wide sweep for `0x10`/`0x20` tests with a bit-3 control. [`ns1_w7_flags.py`](../../_index/candidates/ns1-class-word-w7/ns1_w7_flags.py); §14 item 1 | 1 | PROVEN |
| the load path reads the namespace byte-order mark and refuses a mismatch | ~~**not established**; `NS-4` — the mark is emitted in all 35,984 files, so it is unconditional tooling metadata, not a per-file property~~ *corrected 2026-09-26 (FABLE)*: `0059E070` tests it after the fixup (`0059E167`) and returns 6 on a mismatch (`0059E295`), then checks the self-size (`0059E191`); `_index/candidates/ns4-bom-reader/bom_reader.py` | 1 | PROVEN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

### The reader, read whole

`0059A6F0` is **116 bytes**, exactly as claimed, and every clause of §15 is visible in it:

```asm
0059A710  test r9d, r9d / je      ; the length
0059A715  test r8,  r8  / je      ; the buffer     <- the only validation there is
0059A723  call qword [rax+0x28]   ; ONE read, through the stream vtable
0059A726  add  [rbx+0x18], eax    ; bytesConsumed advances ...
0059A72B  cmp  eax, esi           ; ... BEFORE the short-read test
0059A72D  mov  ebx, 9 / cmove ebx, ecx   ; 0 on a full read, 9 otherwise
0059A73B  test rdi, rdi / test bpl, bpl  ; the swap is gated on the BUFFER and the FLAG
0059A748  call 0059C180                  ; ... and not on ebx, which is already decided
```

**The swap really does fire on a short read**: the return value is computed at `0059A732` and never
consulted again. And the zero/null path at `0059A737` returns `0`, so "only `0` or `9`" holds on
every exit.

### The trap: counting `bswap` to audit "nine words" returns five

`0059A780` strides `lea rax, [rax + 0x24]` — **36 bytes** — and swaps **nine** consecutive dwords per
iteration, `[rax-0x2c]` through `[rax-0xc]`. But only **five** of the nine use the `bswap`
instruction. The other four — `-0x2c`, `-0x1c`, `-0x18`, `-0x14` — are **open-coded**:

```asm
shl ecx, 0x10 / and r8d, 0xff00 / or r8d, ecx / shl r8d, 8 / sar ecx, 8 / sar edx, 0x18 / movzx
```

Same operation, different codegen. **A reader or tool auditing "nine words" by counting `bswap`
finds 5 and reports a defect that is not there** — the same family of trap as a constant hoisted into
a register: the operation is present, its canonical spelling is not.

### Confirmed

| claim | image |
|---|---|
| member records are 6 words of 24 bytes | `0059C180` strides `[rax + 0x18]`, 14 `bswap` in the body |
| the type table's swap is **vectorised** | `0059A8B0` branches at `0059A8BE cmp ecx, 8`, then `movdqu`/`pand`/`pslld`/`psrld`/`por` — the swap is done by shift-and-mask in SSE, with one scalar `bswap` for the tail |
| the swap order is not the layout order | `0059C1D5 call 0059A780` (classes), members inline, and the type table **last and by tail `jmp`** at `0059C245 jmp 0059A8B0` |

**Not claimed:** the corpus arithmetic (`0x20 + 4A + 36B + 24C + D`) is file-side; it has since been
extended to the whole archive (35,984/35,984) by the full-corpus census (§14 `NS-5`). `NS-2`,
`NS-3` and `NS-5` are resolved by that census; `NS-1`'s bit names and `NS-4` stay open, and the
unbounded-swap kind D is untouched by this pass.

## 16. Parity plan

**Constructed and run, 2026-09-12** — `SERIALIZATION`, `STRUCTURAL`, `CALCULATION` and `EDGE-CASE`
are all `COVERED` by `diff_phyre_namespace.py`: the whole block compared byte for byte, both record
strides and all three region offsets, `0059A8B0` on **both sides** of its `cmp ecx, 8` split, and
every region count at zero.

**What is still not covered here:** the §4 size invariant as a *property test over generated
blocks*. The cases satisfy it by construction rather than asserting it, so a namespace that violates
it has never been built — and §10 row 5 says what the original does with one: it faults.

**Not constructible offline:** `INTEGRATION` — what a consumer does with the decoded schema;
`TIMING`; `RNG`; `PRESENTATION`; `STATE-TRANSITION` — there is no state; `FULL SUBSYSTEM`.

## 17. Related

- [`the-packed-namespace-and-the-file-side-schema.md`](the-packed-namespace-and-the-file-side-schema.md)
  — the mechanism, the decoded table and the corpus.
- [`CONTRACT-phyre-cluster-header.md`](CONTRACT-phyre-cluster-header.md) — the ladder that calls this
  reader, and where `m_packedNamespaceSize` and the byte-swap flag come from.
- [`../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md`](../Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md)
  — the same join taken from the binary's side.

## SWE2-EC7-45 update (2026-09-19) - `0059A8B0`

`0059A8B0` (246 B) is `SwapU32Array` - call-free SSE-vectorised u32 byte-swap: `cmp ecx,8` split, `movdqu`/`pand`/`pslld`/`psrld`/`por` with masks `00D27A80`/`00D27A90` at 8-per-0x20-stride, scalar `bswap` tail. Interior anchor `0059A900` (the SSE loop head).
