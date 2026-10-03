---
contract: Accept or refuse a .phyre cluster header
category: 22-Middleware-PhyreEngine
scope: subsystem
readiness: CONTRACT READY
confidence: PROVEN
implements: the-cluster-header-and-what-the-loader-rejects.md
entries: ["0059A3B0", "0059E070", "00686D00", "0069E780", "0059A6F0",
          "005983E0", "00598C50", "00598DF0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 95 addresses cited - 4 data, 20 entry, 71 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-12
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-phyre-cluster-header-pass-1  # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — accept or refuse a `.phyre` cluster header

> **Authored 2026-09-12 by OPUS.** The mechanism, the recovered field schema and the 169-file corpus
> are the source page's,
> [the cluster header and what this build's loader rejects](the-cluster-header-and-what-the-loader-rejects.md),
> which carries an audit pass. **This is the first contract in `22-Middleware-PhyreEngine`**, which
> had seventeen documented pages and none.
>
> `0059A3B0` was **re-read in full for this contract**, and the reading sharpens the page in four
> places — the truncation code is computed rather than literal, both constant leaves are called even
> when the check is disabled, the oversized-header copy is SSE rather than a dword loop, and
> `m_size` is compared **twice**.

## 1. Purpose

**Every model, texture, animation, shader and font in FFXII: The Zodiac Age is a `.phyre` file** —
35,984 of them, 72 % of the archive by size. This is the gate each one passes before the loader will
touch its contents.

For a player, it is invisible until a mod is wrong, and then **the asset simply does not appear**.
The game does not crash on a bad `.phyre` file and it does not say why: it gives up at one of the
checks and returns a number nobody displays.

## 2. Interface

| | |
|---|---|
| entry | `0059A3B0`, 589 bytes |
| signature | `int Read(Stream *rcx, ClusterHeader *rdx, NsBuffer *r8, Buffer *r9, bool *outWasByteSwapped [rsp+0x28], uint32 *outSize [rsp+0x30], bool checkPlatform [rsp+0x38])` |
| `r8` | the namespace buffer: `+0x00` capacity, `+0x08` data. Only reallocated when the capacity differs from `m_packedNamespaceSize` (`0059A479`) |
| `r9` | **a SECOND buffer of the same shape as `r8`, and a stack local in that one caller** — `0059E142 lea r9, [rsp+0x48]`. Its `+0x08` is where the oversized path copies the 84 bytes (`0059A52E mov rdx, [r12+8]`). Zeroed before the call exactly as `r8` is, and released by the same ownership-bit rule afterwards (§2a) |
| returns | `0` success · `6` refused · `9` truncated · `0xD` allocation failed |
| callers | **exactly one**, `0059E070` at `0059E153`, and it passes `checkPlatform` as the literal `1` |
| reads | exactly `0x54` = **84** bytes through the stream vtable slot `+0x28` |

**There is no configuration and no second call site.** The platform and physics checks always run.

## 3. Types and state

> **All three layouts below are now in the type store** under their registered class names: the header as `PClusterHeaderBase` + `PClusterHeaderD3D11` (0x48 + the three concrete fields = 0x54, 21 fields), the instance list as `PInstanceListHeader` (0x24, 9 fields), and `PhyreNamespaceBuffer` (0x10, 2 fields and one undeclared dword). `PhyreClusterHeader` and `PhyreInstanceListHeader` were the same objects under file-format names and were retired as aliases on the canonical rows 2026-09-21 (OPUS-REQ-STRUCT-TWO-HEADER-ROWS-DUPLICATE-REGISTERED-CLASSES) — the file maps in place, so the header bytes are the registered class. The buffer is `CLASSIFIED / HIGH` because it has no registration and was read out of `0059A3B0`.

**The 84-byte header — 21 `unsigned int` fields.** Recovered from the engine's own reflection
registrations: `005983E0` registers `PClusterHeaderBase` (18 fields, attribute word `8`) and
`00598C50` registers `PClusterHeaderD3D11` (3 more, attribute word `0`). Every field passes the same
`PTypeDefault<unsigned int>` singleton at `01F2E5A0`.

| offset | field | this build's value |
|---|---|---|
| `+0x00` | `m_phyreMarker` | `0x50485952` — the bytes `R Y H P` |
| `+0x04` | `m_size` | **84** in all 169 sampled files |
| `+0x08` | `m_packedNamespaceSize` | bytes of class-name namespace following the header |
| `+0x0C` | `m_platformID` | `0x44583131` — `1 1 X D` |
| `+0x10`…`+0x40` | the fixup and instance-list counts and sizes | |
| `+0x44` | `m_physicsEngineID` | `0x424C4C54` (`T L L B`, Bullet) **or 0** |
| `+0x48`, `+0x4C`, `+0x50` | index / vertex / max-texture buffer sizes | the D3D11 subclass |

`m_size` is the header's own length, and **84 is exactly `0x48` of base plus `0x0C` of D3D11
extension** — the schema predicts the number and the files state it, neither derived from the other.

**Each instance list then carries its own 36-byte header**, `PInstanceListHeader`, registered at
`00598DF0` with **nine** `unsigned int` fields.

### The namespace buffer, and its ownership bit

`r8` is a small object the loader both reads and rewrites:

| offset | width | meaning |
|---|---|---|
| `+0x00` | 4 | the capacity **word**. `0059A479` compares it against `m_packedNamespaceSize` **whole**, so a set bit 31 can never match and always forces a replacement |
| `+0x08` | 8 | the data pointer |

> **Bit 31 of the capacity word is an ownership flag.** `0059A4AB shr edx, 0x1f` / `not dl` /
> `test dl, 1` gates the release at `0059A4BA`: **set means the buffer is borrowed and its old data
> is not freed.** The release is skipped in three cases — the new pointer equals the old, bit 31 is
> set, or the old pointer is null — and otherwise `00584730` releases it before `0059A4BF` installs
> the new one and `0059A4C8` writes the new capacity.

**Found by the pilot, not by reading.** The first case with a zero-size namespace against a
non-matching capacity **faulted on an unmapped fetch** at `00584730`, because no earlier case had
ever reached the release. The branch was read afterwards.

## 4. Preconditions · postconditions · invariants

**Preconditions.** The caller pre-seeds the header buffer with a valid default —
`0059E0D7` writes `RYHP` and `0059E0DE` writes `84`, then `0059E0E5` zeroes the other 19 fields — so
**a failed read leaves a well-formed header rather than stack garbage.**

**Postconditions on success.** `*outSize` holds the file's `m_size`; `*outWasByteSwapped` records
whether the file was big-endian; the packed namespace has been read; `stream->bytesConsumed` has
advanced by the bytes actually read.

**Invariants.**

1. **A big-endian file is not refused.** `PHYR` — the marker reversed — is accepted by flipping the
   whole header and re-testing the *same* constant (§7).
2. **`bytesConsumed` advances by what was read, not by what was wanted.** `0059A3DA` adds `eax`
   before the truncation test, so a short read still moves the counter.
3. **A header of a different length is not an automatic rejection** (§8). Both tolerance paths are
   **dead against shipped data** — all 169 sampled files report 84.
4. **Nothing here validates the contents.** Every count and size in the header is read and none is
   bounds-checked by this function.

## 5. Relationships

`0059E070` → `0059A3B0` → the stream's vtable `+0x28` (read), `0063E2E0` (byte-swap block),
`00686D00` / `0069E780` (the two id leaves), `0017D260` (**`_aligned_malloc`**), `0067B100`
(grow), `00861EBA` (memcpy), `00584730` (**`_aligned_free`**), and `0059A6F0` — **the
packed-namespace reader, which all three size paths converge on.**

> **Both allocator helpers are named from the import table, not described.** `0017D260(size,
> align)` tail-jumps through `0019C580` to the IAT slot at `008C2B60`, `_aligned_malloc`;
> `00584730(p)` null-checks and tail-jumps through `0019C570` to `008C2B70`, `_aligned_free`.
> **So the namespace buffer is aligned storage, allocated at alignment 4**, and the same pair
> is what the reflection system uses for class descriptors — which is why that page says
> Phyre descriptors are not plain `operator new`.
>
> A dead-code detail worth having before anyone reimplements the wrapper: **`0017D260` sets
> `r9d = -1` and `r8d = 0` before the jump, and `_aligned_malloc` takes two arguments.** Those
> two stores cannot be read by anything.

### The namespace reader imposes no bound of its own — `0059A6F0`, 116 bytes, read in full

```asm
0059A710  test  r9d, r9d / je  ->  result 0      ; length 0: do nothing, SUCCEED
0059A715  test  r8, r8   / je  ->  result 0      ; null buffer: the same
0059A723  call  qword ptr [rax + 0x28]           ; read EXACTLY the length it was handed
0059A726  add   dword ptr [rbx + 0x18], eax      ; bytesConsumed += n, again before the test
0059A72B  cmp   eax, esi / mov ebx, 9 / cmove    ; n == len ? 0 : 9
0059A740  test  bpl, bpl / je                    ; if the header was byte-swapped...
0059A748  call  0x59c180                         ; ...swap the NAMESPACE too
```

**It reads the length it is given and checks nothing else** — no cap, no comparison against the
buffer's capacity, no sanity limit on `m_packedNamespaceSize`. The caller's allocation is the only
thing that sizes it.

> **A short namespace read returns `9` and byte-swaps anyway.** The swap at `0059A748` is gated on
> the buffer and the flag, not on the result, so a truncated namespace is still transformed before
> the failure reaches the caller.

**And that swap says what "byte-swapped" means here.** `0059C180` is 202 bytes of
`mov eax, [rcx+n]` / `bswap eax` / `mov [rcx+n], eax` — **~~fourteen~~ eight `bswap`s over eight fixed dwords *(corrected 2026-10-02, OPUS: `0059C18B`-`0059C1C2`; the body has fourteen in all, six more in the loop at `0059C206`-`0059C22E`)*,
then a counted loop**, before tail-jumping to `0059A8B0`. So this loader's convention is a
**per-dword `bswap`**, not a reversal of the byte range.

> That is the convention, **not a proof about the cluster header**: `0063E2E0` is descriptor-driven
> and its descriptor at `02CAA0A0` is `.bss`. But it moves the pilot's model of the header swap from
> *"the only reading consistent with what the ladder then does"* to *"the transformation this
> loader's own sibling swap demonstrably performs"*, which is a materially better footing for a
> scripted callee.

## 6. State transitions

None of its own. What changes is the caller's header buffer, the two out-parameters, the namespace
buffer and `stream->bytesConsumed`.

## 7. The marker check, and why a constant census would get it wrong

```asm
0059A3C6  mov   ebp, 0x54                       ; 84, kept in ebp for the whole body
0059A3D7  call  qword ptr [rax + 0x28]          ; stream read
0059A3DA  add   dword ptr [r14 + 0x18], eax     ; bytesConsumed += n  -- BEFORE the test
0059A3DE  cmp   eax, ebp
0059A3E2  lea   eax, [rbp - 0x4b]               ; 0x54 - 0x4B = 9 -- TRUNCATED
0059A3FB  mov   byte ptr [r15], 0               ; *outWasByteSwapped = 0
0059A3FF  cmp   dword ptr [rsi], 0x50485952     ; 'RYHP'
0059A40A  lea   rcx, [rip + 0x270fc8f]          ; -> 02CAA0A0, the swap descriptor
0059A414  call  0x63e2e0                        ; flip the whole header
0059A419  cmp   dword ptr [rsi], 0x50485952     ; ...and re-test THE SAME constant
0059A421  mov   eax, 6
0059A437  mov   byte ptr [r15], 1               ; it was big-endian; remember it
```

> **The truncation code is not a literal.** `lea eax, [rbp - 0x4b]` computes `9` from the 84 already
> in `ebp`. A search for an immediate `9` on this path finds nothing, and a decompiler that folds it
> prints a constant the bytes do not contain.

> **`0x52594850` (`PHYR`) occurs zero times in `.text`.** There is no second marker constant because
> the loader **transforms the data and re-tests the first one.** A constant census would conclude
> this build refuses big-endian files; the body says it accepts them and sets a flag that rides
> along with the rest of the load.

## 8. The platform and physics checks, and both tolerance paths

```asm
0059A440  call  0x686d00                        ; GetPlatformID  -- UNCONDITIONAL
0059A44D  test  dil, dil / je                   ; checkPlatform gates only the COMPARE
0059A452  cmp   dword ptr [rsi + 0xc], eax      ; m_platformID
0059A457  call  0x69e780                        ; GetPhysicsEngineID -- ALSO UNCONDITIONAL
0059A461  mov   ecx, dword ptr [rsi + 0x44]     ; m_physicsEngineID
0059A464  cmp   ecx, eax / je ok
0059A468  test  ecx, ecx / je ok                ; 0 is the explicit wildcard
0059A46C  mov   eax, 6
```

> **Both leaves are called even when `checkPlatform` is false.** Only the comparisons are guarded, so
> a reimplementation that skips the calls under the flag has a different call graph for the same
> result. Each leaf is six bytes: `00686D00 mov eax, 0x44583131` and `0069E780 mov eax, 0x424C4C54`.

### ⚠ CORRECTED 2026-09-12 — `m_size` is compared twice, and NOT for the reason first published

**This contract said the second comparison exists "because the swap changes it". It does not.**

```asm
0059A4DF  mov   rbx, qword ptr [rsp + 0x78]   ; rbx = the outSize OUT-PARAMETER
0059A4E4  mov   dword ptr [rbx], eax          ; *outSize = m_size
0059A4E6  cmp   eax, ebp                      ; first comparison
0059A4F7  ...   call the byte-swap block      ; swaps the HEADER back; clobbers eax
0059A506  mov   eax, dword ptr [rbx]          ; reloads *outSize -- NOT the header
0059A508  cmp   eax, ebp                      ; second comparison, on the SAME value
```

`rbx` is the out-parameter, not the header, so **the second comparison can never disagree with the
first.** It is a register reload after a call clobbered `eax`. Two consequences:

1. **The size the loader uses is the swapped one.** For a big-endian file, `m_size` is published
   and compared from the *swapped* header; swapping the header back afterwards does not revise it.
2. **`0059A586`'s `jae 0059A5E0` is unreachable.** Equality was already taken at `0059A4E6` with the
   identical value, so the `jbe`/`jae` pair can only fall through. It joins the database's other
   provably dead branches.

> **How the error was caught, because the method is the point.** A reconstruction was written from
> this contract's own §12, and `diff_phyre_header.py` ran it against the shipped bytes. The case
> that separated them is a big-endian header whose **raw** `m_size` is already 84: the contract's
> reading predicts `0` with the namespace skipped, and **the original returns `9`** with
> `*outSize = 0x54000000`. The contract was wrong and the bytes said so.

| path | guard | what happens | failure |
|---|---|---|---|
| **equal** | `m_size == 84` | straight to the namespace reader `0059A6F0` | — |
| **short** | `m_size < 84` | the surplus already read *is* the namespace head: `take = min(84 - m_size, m_packedNamespaceSize)` via `cmovb` at `0059A58F`, `memcpy` from `header + m_size`, then the remainder from the stream | **`6`** when `84 - m_size` exceeds the namespace size — `0059A593 cmp ebp, r12d / jne` |
| **long** | `m_size > 84` | grow the buffer (`0067B100`), copy the 84 bytes already read, then read `m_size - 84` more | **`0xD`** on grow failure (`0059A51A`); a short read on the remainder returns **`9`** |

> **The oversized copy is SSE, and it is not a call.** `0059A536`–`0059A55F` is ~~five `movups` of 16~~ ten `movups`, five 16-byte loads and five stores *(corrected 2026-10-02, OPUS: §15a)*, of 16
> bytes plus one 4-byte `mov` — `0x50 + 4 = 84` — **inline**, so the oversized path makes **no**
> `memcpy` call at all, while the short path at `0059A5A9` makes exactly one. The source page
> describes the copy as "21 dwords", which is the field count rather than the instruction shape.
> **The pilot compares the memcpy count and caught a reconstruction that modelled the inline copy
> as a call**: same bytes, same return code, different trace.

## 9. Determinism

Fully deterministic given the byte stream. No RNG, no clock, no global state beyond the two constant
leaves.

## 10. Failure paths and edge conditions

| # | condition | returns |
|---:|---|---|
| 1 | the stream returned fewer than 84 bytes | **`9`**, and `bytesConsumed` has already advanced |
| 2 | the marker is neither `RYHP` nor `RYHP` byte-reversed | **`6`** |
| 3 | `checkPlatform` and `m_platformID != 0x44583131` | **`6`** |
| 4 | `checkPlatform` and `m_physicsEngineID` is neither `0x424C4C54` nor `0` | **`6`** |
| 5 | the namespace allocation fails (`_aligned_malloc` via `0017D260` returns null for a non-zero size) | **`0xD`** (`0059A524`) |
| 5a | **the namespace buffer ends up NULL** — which is exactly what a `m_packedNamespaceSize` of **0** against a non-matching capacity produces: nothing is allocated, null is installed at `0059A4BF`, and `0059A4D3 test r13,r13` sees it | **`6`** (`0059A598`) |
| 6 | short header whose surplus exceeds the namespace size | **`6`** |
| 7 | oversized header, grow fails | **`0xD`** |
| 8 | oversized header, the remainder read is short | **`9`** |

> **Five distinct causes share the code `6`,** and nothing the caller receives distinguishes them. The fifth — row 5a — was **missing from this contract until the pilot drove it**, and it is the one a reader is least likely to predict: a *zero-length* namespace is refused, while a zero-length namespace whose capacity already reads zero is ~~accepted, because the second never replaces the buffer~~ refused too in this build *(corrected 2026-10-02, OPUS: the null-buffer test at `0059A4D3`-`0059A4D6` comes first, as §13a says, and the only caller `0059E070` zeroes the buffer, `0059E115`-`0059E11A`; it would pass only with a non-null buffer of capacity zero, which nothing supplies)*.
> `PResult` is the enum's name — isolated under `AZ-3` — but **its symbolic values are not
> established**, so this contract reports numbers as numbers.

## 11. Observable behaviour

A return code nobody displays, and an asset that does or does not appear. In memory: the header
buffer, `*outSize`, `*outWasByteSwapped`, the namespace buffer and `bytesConsumed`.

## 12. Reproduction formula

```c
int PhyreClusterHeader_Read(Stream *s, ClusterHeader *h, Buf *nsBuf,
                            bool checkPlatform, uint32 *outSize, bool *outSwapped)   // <- corrected 2026-10-02, OPUS - real order is (s, h, nsBuf r8, buf r9, outSwapped [rsp+0x28], outSize [rsp+0x30], checkPlatform [rsp+0x38]): 0059A3C3, 0059A3CB, 0059A3F6, 0059A4DF, 0059A445 - section 2
{
    int n = s->vtbl.read(s, h, 84);
    s->bytesConsumed += n;                       /* BEFORE the test */
    if (n != 84) return 9;

    *outSwapped = 0;
    if (h->m_phyreMarker != 0x50485952) {
        ByteSwapBlock(&DESC_02CAA0A0, h, 1);
        if (h->m_phyreMarker != 0x50485952) return 6;
        *outSwapped = 1;
    }
    uint32 plat = GetPlatformID();                /* called either way */
    if (checkPlatform && h->m_platformID != plat) return 6;
    uint32 phys = GetPhysicsEngineID();           /* called either way */
    if (checkPlatform && h->m_physicsEngineID != phys
                      && h->m_physicsEngineID != 0) return 6;

    /* 0059A476-0059A4C8: replace the buffer only when the capacity WORD differs. */
    if (h->m_packedNamespaceSize != nsBuf->capacityWord) {
        void *fresh = 0;
        if (h->m_packedNamespaceSize != 0) {
            fresh = AlignedAlloc(h->m_packedNamespaceSize, 4);
            if (!fresh) return 0xD;
        }
        if (fresh != nsBuf->data && !(nsBuf->capacityWord & 0x80000000u) && nsBuf->data)
            Release(nsBuf->data);                 /* 00584730; bit 31 set means BORROWED */
        nsBuf->data = fresh;
        nsBuf->capacityWord = h->m_packedNamespaceSize;
    }
    if (!nsBuf->data) return 6;                   /* 0059A4D3 -> 0059A598 */

    *outSize = h->m_size;                         /* from the SWAPPED header, if it was */
    uint32 size = *outSize;
    if (size != 84 && *outSwapped)
        ByteSwapBlock(&DESC_02CAA0A0, h, 1);       /* the header goes back; `size` does NOT */

    if (size < 84) {
        uint32 surplus = 84 - size;
        uint32 take = surplus < h->m_packedNamespaceSize ? surplus
                                                         : h->m_packedNamespaceSize;
        if (surplus != take) return 6;            /* surplus exceeds the namespace */
        memcpy(nsBuf->p, (char *)h + size, take);
        return ReadPackedNamespace(s, nsBuf->p + take,
                                   h->m_packedNamespaceSize - take, *outSwapped);   // <- corrected 2026-10-02, OPUS - 0059A6F0 takes (s, swapped dl, buffer r8, length r9d): 0059A5B5-0059A5BF
    }
    if (size > 84) {
        if (!grow(nsBuf, size)) return 0xD;   // <- corrected 2026-10-02, OPUS - the grown buffer is r9's, not nsBuf: 0059A50E mov rcx, r12 (r9) then 0067B100
        memcpy(nsBuf->p, h, 84);                  /* 5 x movups + 1 dword */   // <- corrected 2026-10-02, OPUS - into r9's buffer (0059A52E rdx = [r12+8]), as ten movups plus one dword
        /* read size - 84 more; a short read returns 9 */
    }
    return ReadPackedNamespace(s, nsBuf->p, h->m_packedNamespaceSize, *outSwapped);
}
```

## 13. Runtime validation

**Evidence class: isolated original-code. No live capture, and none is queued** — see below for why
that is a conclusion rather than a gap.

**Executed 2026-09-12** by [`diff_phyre_header.py`](../../../../Reconstruction/Tests/Differential/diff_phyre_header.py)
against [`phyre_header.c`](../../../../Reconstruction/Game/Resource/phyre_header.c) — the
thirty-sixth pilot, and the first in this category. **42 cases, 0 mismatches** against the
shipped bytes at their real virtual address under Unicorn.

**Thirteen observables per case, not the return value alone:**

```
result  bytesConsumed  outSize  outWasByteSwapped  swapCalls  freeCalls  nsReaderCalls
memcpyCalls  memcpySrcOff  memcpyLen  allocSize  allocAlign  namespaceBufferIsNull
```

That is the point. **Five causes share the code `6`**, the byte counter advances on a path that
returns `9`, the short path's memcpy source is `header + m_size`, and the release decision turns on
a single bit — none of which a return-value comparison can see. All five return codes occur:
**0 ×23, 6 ×9, 9 ×6, 0xD ×3**, plus one propagated namespace-reader result.

**What ran and what did not.** `0059A3B0` itself, and **both id leaves `00686D00` and `0069E780` are
executed**, not answered. ~~Seven callees are **scripted**~~ — **as of 2026-09-18 that is down to the
stream read, the allocator, the grow and the buffer release; the BYTE-SWAP BLOCK and the namespace
reader ran as shipped bytes (§13a).** The memcpy was always performed by the hook, so its bytes were
real even though the call was not. **A stub is not proof of its native effects.**

> **The byte-swap block is the one that matters and the one that cannot be run.** *(answered: see §13a - it was run 2026-09-18; 2026-10-02, OPUS)* Its descriptor at
> `02CAA0A0` is `.bss` — zero at load — so it is built at runtime and cannot be read out of the
> image.
>
> **THE PREMISE IS FALSE - 2026-09-16 (FABLE). `02CAA0A0` IS NOT OPAQUE, AND THE OBJECT HAS A NAME.** *In `.bss`, therefore zero at load, therefore built at runtime and cannot be read out of the image at all* conflates **zero at load** with **unknowable**. A CRT static initializer runs before `main` and writes a **`.rdata` constant** into it. **The two writers, and there are only two.** An overlapping-byte-range census of `02CAA080`–`02CAA140` over all listed bodies finds exactly two writes of the qword at `02CAA0A0`. `00160210` is a **static initializer**: it constructs the object (`lea rcx, [02CAA0A0]` / `call 00597690`), clears a flag bit at `02CAA19C`, stores **`lea rax, [00D249A8]`** into `02CAA0A0`, and tail-jumps to `atexit` having registered `008A8150`. **`008A8150` is that destructor** - it installs `[00D24898]` and jumps to `00633390`, the ordinary MSVC vtable-swap-then-destroy shape. **`00D249A8` is a VTABLE, in `.rdata`, and it is complete.** Its eleven slots are all listed functions - `00584C20`, `0016D680`, `005C5230`, `00584E10`, `00584D30`, `00584C50`, `00584C70`, `00584E60`, `0062EFD0`, `0062F080`, `00584DB0` - and the qword before it, `00D249A0` = `01CF15C0`, is the RTTI Complete Object Locator. **RTTI NAMES THE CLASS.** Locator `01CF15C0` → TypeDescriptor `01F498A0` → `.?AV?$PClassDescriptorConcrete@VPClusterHeader@PBinary@PSerialization@Phyre@@@Phyre@@` - **`Phyre::PClassDescriptorConcrete<Phyre::PSerialization::PBinary::PClusterHeader>`**. The destructor's vtable `00D24898` carries `01CF1818` → `01F49980` → **`PClassDescriptorForType<…PClusterHeader>`**. **So this is not *a swap descriptor built at runtime*. It is a PhyreEngine reflection class descriptor for `PClusterHeader`,** of the same family as the `PClassDataMember_Register` machinery `BJ-4` reads, and **what it is is settled statically.** **WHY THIS MATTERS BEYOND THE ROW.** §13 models the byte swap as a per-dword `bswap` *because the descriptor cannot be read*. That reason does not hold: **the object's behaviour is virtual methods in `.text`, reachable through a vtable whose address is a link-time constant.** The model may still be right - but it is now a choice, not a necessity, and eleven readable bodies stand between it and a measurement. **WHAT THIS DOES NOT ANSWER.** The row asks **what `0063E2E0` does with the descriptor**, and this does not say: `0063E2E0` (231 B) makes **no indirect call at all** - its only two calls are direct, both to `0063CE80` - so it does not dispatch through this vtable and the swap is not reached from there. **The object's fields beyond `+0`** are also still unread; I have the vtable pointer and what `00597690` installs, not the rest of the construction. *The premise is falsified and the object is named; the row's own question stays open.* The swap is therefore **modelled** as a per-dword `bswap` on both sides, and what the suite
> establishes is **when it is called and what the ladder does after**, never what it does to the
> bytes. The model is not arbitrary: `0059C180`, the namespace swap this same loader calls, is 202
> bytes of `mov / bswap / mov`. That is a reason to prefer this model, and still not a measurement.

**Three controls, and the suite refuses to pass without them**: all four return codes must occur; at
least one header must be accepted as byte-swapped; and at least one case must reach the **second**
swap at `0059A4F7`, which is where a reimplementation that re-reads the field instead of the
out-parameter diverges.

**Mutation campaign: 62 points — 60 KILLED, 2 SURVIVED,
0 EQUIVALENT, 0 INVALID.** Both survivors are fixture scaffolding; **no
undefined behaviour and no suite defect.**

### What the pilot found that reading did not

**Three defects in the reconstruction, and two of them were defects in this contract.**

1. **The `m_size` double comparison.** The contract said the second one exists "because the swap-back
   changes it". It does not — `0059A506` reloads the **out-parameter**. The reconstruction built
   from the contract's own text returned `0` where the original returns `9`. §8 now carries the
   correction and the dead branch it implies.
2. **The oversized copy is inline.** It makes **no** `memcpy` call, while the short path makes
   exactly one. The reconstruction counted both, and only the memcpy observable separated them.
3. **The buffer release.** A case with a zero-size namespace against a non-matching capacity
   **faulted on an unmapped fetch** at `00584730` — a branch no earlier case had reached. Following
   it gave the **ownership bit** and a **ninth failure row** (§10 row 5a), neither of which is in
   the source page.

**Two real gaps in the cases, both closed by the campaign.** The allocator guard `nsSize != 0`
survived a mutation to `!= 1`, because every case either matched the capacity exactly or used a size
far from 0 and 1; and the ownership mask survived `0x80000000 → 0x80000001`, because **every
capacity driven was even**. Cases at exactly 0 and 1 against a differing capacity, and an odd
capacity word, killed both. Survivors fell 3 → 3 → 2 across three runs while the case count rose
34 → 40 → 42.

### 13a. The block that "cannot be run" was run — 2026-09-18 (OPUS, consuming SWE2-ORACLE's EXP-094)

§13 says of the byte-swap block: *"the one that matters and the one that cannot be run"*, because
its descriptor at `02CAA0A0` is `.bss` and nothing in a static image fills it. **EXP-094 built it and
ran it** — 21 real bodies, **25/25 cases and 10/10 mutants killed across two processes** — and
identifies `02CAA0A0` as the `PClusterHeader` descriptor constructed by `00160210`. That is the
sentence this section discharges, and §5's note that the per-dword `bswap` convention was *"not a
proof about the cluster header"* is now a proof about it.

#### The ABI, read off the real caller — and `arg7` is a BYTE

`0059E070` calls `0059A3B0` at `0059E153` with the stack arguments set immediately above:

```asm
0059E129  mov  byte ptr [rsp + 0x30], 1   ; arg7 = the id gate, ONE BYTE
0059E133  mov  qword ptr [rsp + 0x28], rax ; arg6 = &outLen
0059E13D  mov  qword ptr [rsp + 0x20], rax ; arg5 = &swapFlag
0059E142  lea  r9,  [rsp + 0x48]           ; arg4 = gvec {size, buf}
0059E147  lea  r8,  [rsp + 0x58]           ; arg3 = nsRec {cap|bit31, buf}
0059E14C  lea  rdx, [rbp - 0x40]           ; arg2 = header buffer
0059E150  mov  rcx, rsi                    ; arg1 = stream
```

**The gate is written as a byte and read with `movzx`.** A reimplementation that declares it `int`
and passes a value whose low byte happens to be zero — `0x100`, say — **silently disables id
validation** and accepts headers this loader refuses. The real caller always passes `1`, so **ids are
validated even on native-endian headers**; `arg7 = 0` tolerates wrong ids, which is a path no shipped
caller takes.

#### `outLen` is a three-way dispatch, and the swap can run twice

`hdr+4` selects the shape of everything after the header:

| `outLen` | what happens |
|---|---|
| `== 0x54` | plain namespace read |
| `> 0x54` | `0067B100` grows `gvec`, the whole header is copied into `gvec.buf`, and `outLen − 0x54` tail bytes are streamed in |
| `< 0x54` | the header tail is `memcpy`'d into `nsRec.buf`, which must have `nsSize ≥ 0x54 − outLen` or the loader answers `6` |

**And when the swap flag was set *and* `outLen != 0x54`, `0063E2E0` runs a SECOND time on the header
before the ext-tail read** — EXP-094 counts ten leaf hits where five members would be one pass. A
reimplementation that swaps once produces a header that is byte-reversed in the extended case only,
which is the kind of defect that survives every small test.

#### The refusals, with their codes

`9` for a short header, short namespace or short ext-tail read — and the short-header return is
literally `0x54 − 0x4B`. `6` for a bad marker on the post-swap retest, for bad ids, for
`nsSize < 0x54 − outLen`, and for a **null `nsRec.buf` regardless of namespace length**: the
`test r13, r13` at `0059A4D3` precedes the length paths, so it is not a case of the length check
failing first. `0xD` for an allocation or `gvec` growth failure.

**Stream accounting at `stream+0x18` is cumulative** across the header, namespace and ext-tail reads
— the mutation kills it at *both* `add` sites, which is how the suite knows it is one running total
rather than two independent ones.

#### Consumed on EXP-094's evidence, not re-derived here

Findings 7–10 — the descriptor walk's direction flag and parent chain, the member-node gate layout,
the element engine's leaf ABI, and the namespace swap's structure (8 fixed dwords, a counted `0x24`
record table, an SSE2 dword tail) — are taken on the experiment's evidence. **They were not re-read
from the image in this pass.** The ABI, the `outLen` dispatch, the double swap and the refusal codes
are what this section stands behind at tier 1.

#### What did not become established

The descriptor was **built by the fixture**, not observed being built in a running game, so what
§13a proves is the swap's behaviour given a descriptor of that shape rather than the shape the game
constructs at run time. §14's open items are untouched, and the live gate is unchanged.
*(2026-09-26 (FABLE, Claude Opus 5.5): that shape is now read statically. The game registers 21 members, and the
fixture's five are a subset of them; see §14 item 2. The fixture itself still did not observe the game building it.)*

### The two survivors

Both are **kind B, fixture scaffolding with no counterpart in the original**: the fill value of the
padding this reconstruction writes after a short read — which the original does not write at all,
and which no path reads because a short read returns `9` first — and `PH_MAX_READ`, the fixture's
own stream buffer size.

**No live validation is queued, and that is a conclusion.** This function is a pure byte-stream
parser over one scripted stream; every branch it has is reachable from a buffer. What live capture
would add is not the ladder but its callers, and those are `INTEGRATION` (§16).

Receipts: `Database/Tools/work/OPUS/litsuffix/phyre_header`, `phyre_header2` and `phyre_header3`
(ignored path), and the counts row in
[`MUTATION-CAMPAIGNS.md`](../../../../Reconstruction/MUTATION-CAMPAIGNS.md).

## 14. Unresolved

1. ~~**`PH-1`** — the symbolic values of `PResult`. Four causes share `6` and the enum's names are not
   established, so §10 reports numbers.~~
   **RESOLVED 2026-09-22 (FABLE) — this is `UQ-286`, answered 2026-09-18 and never propagated here.**
   `UQ-286` asks the same thing and closed as **NO ADMISSIBLE SOURCE for the names**: the executable
   reflects `PResult` as `PTypeDefault<unsigned int>` — a name, a size and an alignment, **no
   enumerators** (`AZ-3`); `PE_RESULT` occurs **0** times in the executable, **0** in the installed
   game's `.dll`/`.exe`, and **0** in the archive's text-like files; and `PResult` itself occurs only
   inside RTTI type strings. **So §10 reporting numbers is not a gap — the numbers ARE the
   identifiers**, and what a reimplementation needs does not depend on the names: `0` success, `6` the
   header is refused, `9` the read came up short, `0xD` an allocation failed. *If an SDK header is ever
   admitted as a source, `UQ-286` reopens with a one-line table.* **Follow `UQ-286`.**
2. **`PH-2`** — **ADVANCED 2026-09-15 (OPUS): the function is read and the builder is found;
   the descriptor's CONTENTS are still not in the image, so §13's decision to model the swap
   stands unchanged.**
   **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): the member lists are in the image, as registration code with
   constant arguments, and the swap is all 21 header dwords.** The member reading is OPUS's [the static bound](../../_index/candidates/s49-header-i1-static-bound.md)
   (2026-09-25), which never reached this item. Control: [`ph2_header_swap_members.py`](../../_index/candidates/ph2-header-swap-members/ph2_header_swap_members.py) (10 checks,
   FAILS 0).
   - **What `0063E2E0` does with the descriptor.** `PClusterHeader` registers no member of its own. The walk
     follows `+0x78` to `PClusterHeaderD3D11`, which has 3 members at `+0x48`, `+0x4C` and `+0x50`, and then to
     `PClusterHeaderBase`, which has 18 at `+0x00`–`+0x44`. Every member is an `unsigned int` whose swap leaf is
     an in-place `bswap`. So one pass swaps all 21 dwords of the `0x54`-byte header, each exactly once.
   - **Who fills the lists.** The two class registrars are called by the init method (vtable slot `+0x08`) of
     `PSerialization::PUtilitySerialization`. The engine-init walk calls that slot once for every module on the
     chain ([the module registry](../Subsystem-Map/the-fifteen-modules-registered-before-main.md)).
   - **Absence domain.** No `lea rdx` aimed at the `PClusterHeader` descriptor precedes a member registration
     anywhere in `.text`. The same sweep on the base class's descriptor finds its 18, and a third class's
     registrations are parsed as a control. A descriptor pointer reaching the registrar any other way is not covered.
   - **Not established:** that every header load runs after the engine-init walk. The run-time order is not read.
   - **For §13.** The per-dword `bswap` model is now what the image's registrations produce, not only a model.
     §13a's five fixture members are a subset of the 21, as the static bound shows.
   - **What `0063E2E0` does.** It is generic — it never names `02CAA0A0`. Given
     `(descriptor, object, direction)` it treats `descriptor+0x80` as a **circular member-list
     head** (the walk ends when the cursor equals that address), converts each node to its member
     with `-8`, and calls **`0063CE80`** (`Phyre.Reflection.CallbackAdapter`) on each. It then
     follows **`descriptor+0x78` to the base-class descriptor** and repeats until that is null, so
     **inherited members are swapped too**. The bool picks the order: forward walks `[rsi]` then
     `[rbx+8]`, reverse walks `[rsi+8]` then `[rbx+0x10]`.
   - **So `ByteSwapBlock` is reflection-driven**, which is what §13 assumed without being able
     to say it: the swap applied to the header is exactly the member list the descriptor carries,
     plus its bases. The per-dword `bswap` model is a model of `0063CE80`, not of this function.
   - **The builder, which this row asked for.** `00160210`, and it is a **CRT static
     constructor** — proven from the file rather than inferred from absence: `00160210` occurs
     **exactly once** as a qword in the whole image, at `.rdata` `008C3518`, inside a dense array
     of `.text` pointers. It has no code callers and nothing references its address. It calls
     `00597690`, whose own tag is `Phyre.Reflection.AbstractClassDescriptor.Construct`, clears
     bit 1 of `02CAA19C`, installs vtable `00D249A8`, and registers `008A8150` as the destructor
     through `00808B90`.
   - **WHY THIS DOES NOT REOPEN §13.** The static constructor builds an EMPTY descriptor; the
     member list it walks is populated afterwards, at runtime, ~~and none of it is in the image.
     **The row's premise was right and stays right**~~ *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): the
     population is image code with constant arguments; see the answer above)* — what changes is that the builder is no
     longer unknown, and the shape of what it builds is now three named fields: `+0x38` a dword
     handed to every member callback, `+0x78` the base descriptor, `+0x80` the member-list head.
   - ~~**Still open:** the member list's runtime contents, which is what the pilot would need to run
     the swap instead of modelling it.~~ *(Answered 2026-09-26 (FABLE, Claude Opus 5.5): 21 dwords, above. What
     stays open is the run-time order, not the contents.)*
3. ~~**`PH-3`**~~ — **ANSWERED 2026-09-12: it imposes none** (§5). It reads exactly the length it
   is handed and guards only on a zero length and a null buffer, both of which succeed. What
   remains of the question is `0059C180`, the namespace byte-swap it calls, which ~~is unread~~
   **was read since — 2026-09-18 re-check:** it is the table layout made executable — ~~fourteen~~ eight *(corrected 2026-10-02, OPUS: `0059C18B`-`0059C1C2`; fourteen is the whole body's count)*
   `bswap`s over eight fixed dwords at `+0x00`…`+0x1C`, documented in
   [the packed namespace's file-side schema](the-packed-namespace-and-the-file-side-schema.md) §8 —
   and which `check_caller_claims` confirms has this function as its only caller.
4. ~~**`PH-5`**~~ — **ANSWERED 2026-09-15 (OPUS): `r9` is a second `PhyreNamespaceBuffer`, and
   it is a stack local of the only caller.** Both halves the row asked for are now read, from
   `0059E070` rather than from this function.
   - **Shape.** `0059E142 lea r9, [rsp+0x48]`, and the frame is initialised two fields at a time:
     `0059E11F mov dword [rsp+0x48], 0` and `0059E124 mov qword [rsp+0x50], 0` — the same
     `+0x00` dword / `+0x08` pointer pair, zeroed the same way, as `r8` gets at `0059E115` and
     `0059E11A`. So the two arguments are **two instances of one 0x10 type**, not a buffer and
     something buffer-shaped.
   - **Lifetime.** The caller's frame, and no longer. After the call the epilogue releases each
     buffer under the ownership bit §2a already establishes: `0059E29A`–`0059E2B6` does
     `shr eax, 0x1f` / `not al` / `test al, 1` on `r9`'s capacity word and calls `_aligned_free`
     (`00584730`) only when the bit is CLEAR **and** the pointer is non-null;
     `0059E2B7`–`0059E2D2` does exactly the same for `r8`. **So the ownership bit is honoured at
     both ends** — inside the callee at `0059A4AB`, which this page already published, and in
     the caller for both buffers, which it did not.
   - **And it is not a dead output.** `0059E200 lea r8, [rsp+0x48]` hands `r9` straight on to
     `00599500` with `edx = [rsp+0x44]`, the size the call wrote out. The oversized path's 84
     bytes leave through it.
   - **Not claimed, and outside what this row asked:** what `00599500` makes of those bytes. The
     row named two unknowns, shape and lifetime; the downstream semantics were never part of it
     and no verdict is offered on them here.
5. **`PH-4`** — the 169-file corpus is **0.47 %** of the 35,984 shipped files, and it is the sample
   behind "84 in every shipped file". The claim is about the sample, and the tolerance paths exist
   precisely for files unlike it.
   **ANSWERED 2026-09-12 by `CU-4` (FABLE); noted here 2026-09-26 (FABLE, Claude Opus 5.5).** Every `.phyre` entry
   in `FFXII_TZA.vbf` was checked from its first compressed block: `m_size` = 84 (with `RYHP`, `11XD` and physics
   engine 0) in **35,984 / 35,984**
   ([the cluster header page](the-cluster-header-and-what-the-loader-rejects.md), CU-4). The claim now holds for the
   shipping data, not just the sample, and the tolerance paths are dead against every shipped file.

## 15. Evidence

| claim | evidence | tier | confidence |
|---|---|---|---|
| the header is 84 bytes of 21 `unsigned int` fields | the source page, from the reflection registrations `005983E0` (18) and `00598C50` (3); `0x48 + 0x0C = 0x54` | 1 | PROVEN |
| the instance-list header is 36 bytes of nine fields | the source page's `00598DF0`, after its own audit corrected a tenth field that a case-insensitive grep had introduced | 1 | PROVEN |
| exactly 84 bytes are read, through the stream vtable `+0x28` | **re-read**: `0059A3C6 mov ebp, 0x54` and `0059A3D7 call qword ptr [rax + 0x28]` | 1 | PROVEN |
| **`bytesConsumed` advances before the truncation test** | **re-read**: `0059A3DA add dword ptr [r14+0x18], eax` precedes `0059A3DE cmp eax, ebp` | 1 | PROVEN |
| **the truncated code `9` is computed, not a literal** | **re-read**: `0059A3E2 lea eax, [rbp - 0x4b]` with `ebp = 0x54` | 1 | PROVEN |
| a reversed marker is byte-swapped and re-tested against the same constant | **re-read**: `0059A3FF` and `0059A419` both `cmp dword ptr [rsi], 0x50485952`, with `0059A414 call 0x63e2e0` between them | 1 | PROVEN |
| `PHYR` appears zero times in `.text` | the source page's constant census | 1 | PROVEN  **§15a: confirmed — 0 occurrences in `.text`'s 7,997,440 raw bytes, and the reason is that the constant is stored BYTE-REVERSED: `RYHP` occurs 7 times.** The marker is not absent from the engine; it is spelled the other way round |
| the platform and physics ids are `0x44583131` and `0x424C4C54`, with `0` a wildcard | **re-read**: `00686D00` and `0069E780`, six bytes each; `0059A468 test ecx, ecx / je` is the wildcard | 1 | PROVEN |
| **both id leaves are called even when `checkPlatform` is false** | **re-read**: `0059A440 call` and `0059A457 call` precede their `test dil, dil` guards | 1 | PROVEN |
| the one caller passes `checkPlatform` as a literal `1` | the source page's `0059E129 mov byte ptr [rsp+0x30], 1`; `check_caller_claims` independently reports 1 caller, 1 function | 1 | PROVEN |
| the caller pre-seeds a valid header before reading over it | the source page's `0059E0D7` / `0059E0DE` / `0059E0E5` | 1 | PROVEN |
| **`m_size` is compared twice, and the second comparison reloads the OUT-PARAMETER so it cannot disagree** | **re-read and then EXECUTED**: `0059A4DF mov rbx, [rsp+0x78]` / `0059A4E4 mov [rbx], eax` / `0059A506 mov eax, [rbx]`. This row first read *"because the swap-back changes it"*; the pilot's big-endian case refuted it — the original returns `9` where that reading predicts `0` | 1 | PROVEN |
| **`0059A586`'s `jae 0059A5E0` is unreachable** | follows from the row above: equality is taken at `0059A4E6` on the same value, so the `jbe`/`jae` pair can only fall through | 1 | PROVEN |
| the oversized copy is INLINE and makes no `memcpy` call, while the short path makes exactly one | **executed**: the pilot compares the memcpy count and separated the two paths | 1 | PROVEN |
| **`0017D260` is `_aligned_malloc` and `00584730` is `_aligned_free`** | **resolved by me through the import table**: `0017D260` → `0019C580` → IAT `008C2B60`; `00584730` → `0019C570` → IAT `008C2B70`. `functions.tsv` already names `0019C570` `_aligned_free`, which agrees | 1 | PROVEN |
| `0017D260` sets two argument registers `_aligned_malloc` does not read | **re-read**: `0017D260 or r9d, 0xffffffff` / `xor r8d, r8d` before the tail jump | 1 | PROVEN |
| `r9`'s `+0x08` is the oversized copy's destination | **re-read**: `0059A52E mov rdx, [r12+8]` with `r12 = r9` on the path where no allocation replaced it | 1 | PROVEN |
| **`r9` is a stack local of the sole caller, with `r8`'s layout and `r8`'s ownership discipline** | **re-read `0059E070`** (§2a): `0059E142 lea r9, [rsp+0x48]`; zeroed at `0059E11F`/`0059E124` as `r8` is at `0059E115`/`0059E11A`; released at `0059E29A`–`0059E2B6` by the same `shr 0x1f` / `not` / `test 1` gate that `0059E2B7`–`0059E2D2` applies to `r8` | 1 | PROVEN |
| `r9` is the same TYPE as `r8` (`PhyreNamespaceBuffer`) | inference from identical layout, identical zero-init, identical release gate and adjacent parameter position - no reflection registration names it | 2 | HIGH |
| the short path takes `min(84 - m_size, namespaceSize)` and refuses when the surplus exceeds it | **re-read**: `0059A588 sub ebp, eax`, `0059A58F cmovb r12d, ebp`, `0059A593 cmp ebp, r12d / jne` to `mov eax, 6` | 1 | PROVEN |
| **the oversized copy is five `movups` plus one dword, not a dword loop** | **re-read**: `0059A536`–`0059A55F` | 1 | PROVEN  **§15a: five 16-byte TRANSFERS, which are TEN `movups` instructions** — each transfer is a load and a store (`0059A536`/`39`, `3C`/`40`, `44`/`48`, `4C`/`50`, `54`/`58`), then `0059A55C mov eax, [rsi+0x50]`. **5 × 16 + 4 = 84**, which re-derives the header size from the copy |
| the three size paths converge on `0059A6F0` | **re-read**: ~~`0059A5BF`, `0059A5D7` and the equal path all call it~~ two call sites, `0059A5BF` for the short and long paths and `0059A5D7` for the equal path *(corrected 2026-10-02, OPUS: the only two direct callers of `0059A6F0`)* | 1 | PROVEN |
| `m_size == 84` in 169 of 169 sampled files | the source page's corpus — **0.47 % of the shipped files**, and a file-side measurement that executed no code | 1 | PROVEN |
| **bit 31 of the capacity word is an ownership flag, and a set bit skips the release** | **executed**: `0059A4AB shr edx,0x1f / not dl / test dl,1` gating `0059A4BA call 0x584730`, driven with the bit set and clear against the same sizes — the pilot compares the release count | 1 | PROVEN |
| **a NULL namespace buffer is refused with 6, which is what a zero size against a non-matching capacity produces** | **executed**: `0059A4D3 test r13,r13 / je 0059A598` where `0059A598 mov eax, 6`. **Found by the pilot** — the case faulted on the unmapped release before this branch had ever been reached | 1 | PROVEN |
| the namespace reader imposes NO bound: it reads the length it is handed | **read in full by me**: `0059A6F0`'s only guards are `test r9d,r9d` and `test r8,r8`, both succeeding, and the read at `0059A723` passes `r9d` straight through. **Static: the pilot scripts this function** | 1 | PROVEN |
| a short namespace read returns 9 and byte-swaps anyway | **read in full by me**: `0059A748 call 0x59c180` is gated at `0059A73B`/`0059A740` on the buffer and the flag, not on the result computed at `0059A72D` | 1 | PROVEN |
| any execution of this ladder, isolated or live | ~~**none**; §13~~ *(answered: see §13, executed 2026-09-12 by diff_phyre_header.py, and §13a, 2026-09-18; 2026-10-02, OPUS)* | none | UNKNOWN |
| the symbolic values of `PResult` | **not established, and dispositioned rather than open** — `UQ-286` (2026-09-22, FABLE: `PH-1` is its duplicate) closed it as **NO ADMISSIBLE SOURCE**: the image reflects the type with no enumerators and the names appear in no admissible file, so the numbers are the identifiers | none | UNKNOWN |
| **`0063E2E0` walks the descriptor's member list and its base chain, calling `0063CE80` per member** | **read**: `rsi = desc+0x80` is a circular list head (loop ends when the cursor equals `rsi`); each node becomes its member by `-8` (`0063E324`); `0063CE80(&ctx, member)` at `0063E338`/`0063E398`; then `rdi = [desc+0x78]` and repeat while non-null (`0063E351`, `0063E3B4`). `r8b` picks the direction: forward uses `[rsi]` then `[rbx+8]`, reverse uses `[rsi+8]` then `[rbx+0x10]` | 1 | PROVEN |
| the descriptor's `+0x38` dword is handed to every member callback | **read**: `0063E2EF mov eax, [rcx+0x38]` stored into the context at `+0x04` (`0063E2F5`); the context is `{dword 0, dword desc+0x38, qword object, byte direction}` at `[rsp+0x20]` | 1 | PROVEN |
| **the descriptor at `02CAA0A0` is built by a CRT STATIC CONSTRUCTOR, `00160210`** | **proven from the file**: `00160210` occurs exactly ONCE as a qword in the whole image, at `.rdata` `008C3518`, inside a dense array of `.text` pointers - a CRT initializer table. It has zero code callers and zero code references. It calls `00597690` (`Phyre.Reflection.AbstractClassDescriptor.Construct`), clears bit 1 of `02CAA19C`, installs vtable `00D249A8`, and tail-jumps to `00808B90` with `rcx = 008A8150` - registering that as the destructor, which swaps the vptr to `00D24898` and tail-jumps to `00633390` | 1 | PROVEN |
| **the header's member lists are image code: 21 `unsigned int` members, 18 on `PClusterHeaderBase` (`+0x00`–`+0x44`) and 3 on `PClusterHeaderD3D11` (`+0x48`–`+0x50`), none on `PClusterHeader`** | **read** (static, 2026-09-26, (FABLE, Claude Opus 5.5)): constant descriptor and offset arguments at every registration; the swap leaf is an in-place `bswap`. [`ph2_header_swap_members.py`](../../_index/candidates/ph2-header-swap-members/ph2_header_swap_members.py); §14 item 2 | 1 | PROVEN |
| what `0059A6F0` does | **not established**; `PH-3`'s residue | none | UNKNOWN |

## 15a. Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

Every claim in this contract names an address and an instruction, so each was checked where it
stands rather than in summary.

| claim | read at that address |
|---|---|
| exactly 84 bytes are read | `0059A3C6 mov ebp, 0x54` |
| **the truncated code `9` is computed, not a literal** | `0059A3E2 lea eax, [rbp - 0x4b]` — `0x54 − 0x4B = 9` |
| the marker is re-tested against **the same** constant after the swap | `0059A3FF` and `0059A419`, **both** `cmp dword [rsi], 0x50485952` |
| the platform and physics ids, six bytes each | `00686D00: B8 31 31 58 44 C3` = `mov eax, 0x44583131` / `ret`; `0069E780: B8 54 4C 4C 42 C3` = `mov eax, 0x424C4C54` / `ret` |
| `0059A586`'s `jae 0059A5E0` | present as described |

### The negative about `PHYR` is true, and its reason matters more than its truth

`PHYR` occurs **0 times** in `.text` — across **7,997,440** raw bytes, so the zero is a real zero and
not a wrong-section artefact. But the marker is not absent from the engine: **`RYHP` occurs 7 times**,
because the compared constant is `0x50485952`, which in little-endian memory *is* the bytes `R Y H P`.

> A reader who greps `.text` for `PHYR`, finds nothing, and concludes the engine never names the
> marker would be wrong twice over — it names it seven times, spelled the other way round. The row
> now carries both numbers.

### Corrected: five 16-byte transfers are ten `movups` instructions

§15 says the oversized copy is *"five `movups` plus one dword"*. The block `0059A536`–`0059A55F` is:

```asm
0059A536  movups xmm0, [rsi]        0059A539  movups [rdx], xmm0
0059A53C  movups xmm1, [rsi+0x10]   0059A540  movups [rdx+0x10], xmm1
0059A544  movups xmm0, [rsi+0x20]   0059A548  movups [rdx+0x20], xmm0
0059A54C  movups xmm1, [rsi+0x30]   0059A550  movups [rdx+0x30], xmm1
0059A554  movups xmm0, [rsi+0x40]   0059A558  movups [rdx+0x40], xmm0
0059A55C  mov    eax, [rsi+0x50]
```

**Ten `movups`, forming five 16-byte transfers**, each a load and a store — the claim's substance
("not a dword loop") is right and its instruction count is half the real one. The useful part is the
arithmetic it exposes: **5 × 16 + 4 = 84**, so the copy re-derives the header size independently of
the reflection registrations and of `mov ebp, 0x54`.

**Not re-derived here:** that `0059A586`'s `jae` is *unreachable* — that rests on equality being taken
earlier at `0059A4E6` on the same value, which is a dataflow argument this pass did not repeat. The
branch's existence and target are confirmed; its unreachability is left as the document has it.

**Not claimed:** no live observation and no execution; §13 unchanged, and `PH-1`/`PH-2`/`PH-3` stay
open.

## 16. Parity plan

**Constructed and run, 2026-09-12** — `STRUCTURAL`, `EDGE-CASE` and `SERIALIZATION` are `COVERED`
by [`diff_phyre_header.py`](../../../../Reconstruction/Tests/Differential/diff_phyre_header.py):
the 84-byte layout and every field the ladder reads, **all nine rows of §10** including the `cmovb`
boundary and the ownership bit, and a big-endian header driven end to end.

**The 36-byte instance-list header is NOT covered.** It is in the type store from its registration,
and `0059A3B0` never touches it — the pilot stops at the namespace reader's door.

`CALCULATION` is `N/A`: there is no arithmetic here beyond the two size differences, which
`EDGE-CASE` drives directly.

**Not constructible offline:** `INTEGRATION` — what the namespace reader and the rest of the load do
with the result; `TIMING`; `RNG`; `PRESENTATION`; `CALCULATION` — there is no arithmetic here beyond
the size differences, which `EDGE-CASE` already drives; `FULL SUBSYSTEM`.

## 17. Related

- [`the-cluster-header-and-what-the-loader-rejects.md`](the-cluster-header-and-what-the-loader-rejects.md)
  — the mechanism and the corpus.
- [`the-packed-namespace-and-the-file-side-schema.md`](the-packed-namespace-and-the-file-side-schema.md)
  — what `0059A6F0` reads, and the file-side view of the same schema.
- [`../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`](../Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md)
  — how the layout was recovered from the engine's own registrations.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `001C22A0` | 962 | cluster field-pair copy `rdx`/`rcx` at `+0x10..0x30`: `0017D260` x2, `001C19A0`, `00584730` x3 (CRT init/finalizer), `0067ADD0` |

## SWE2-EC7-20 update (2026-09-18) — loader-side fragment set: `005CD5E0`, `005CD0E0`, `0059BED0`, `00599670`

`005CD5E0` (98 B) is an IAT-driven create-probe: `rcx = [rcx]` dereferences the
handle slot, then `call [008C2198]` runs the open attempt — non-zero returns 0
(`005CD5E4`..`005CD5F7`); else `call [008C20A8]` re-arms, and `call [008C2208]`
runs a `ecx=0x1300`/`r9d=0x400` create into `[rsp+0x50]` (`005CD5FE`..`005CD623`);
a created handle closes through `call [008C21F8]` (`005CD62D`..`005CD632`).
Both arms return 9 (`005CD638`) — a status-code path, not a deleter. Callers
`005FE1A0`/`00600D20`/`00600E30`/`00609720`/`00610210`/`006793E0`/`006794D0`/
`00679BF0`/`0067A240`/`0067A440`/`0067A480`/`0067A970`/`0067A9B0`/`006CC550`/
`006CC670`/`006CC710`/`006CC920` — the movie-loader object family.

`005CD0E0` (126 B) is the event-handle creator: `edx` bit 1 shifts down as the
manual-reset flag and `not edx & 1` as the initial-state flag (`005CD0E6`..
`005CD0F5`), `call [008C21A8]` creates the event into `[rbx]` (`005CD0FD`..
`005CD103`); a null handle runs the `008C20A8` + `008C2208(0x1300,…,&out)` +
`008C21F8` report-close chain and returns 9 (`005CD10B`..`005CD14B`), success
returns 0 (`005CD156`). [Corrected 2026-09-18 — the earlier `lea r8,[rip+…]=
02CB8600` quote was a misaligned-decode artifact; the verified body holds no
such `lea`.] Callers `005CD0A0`/`00606600`/`00607D20`/`00679130`/`0067A350`/
`0067A480`.

`0059BED0` (687 B) is the range-fit scan behind the `0059C700` load path:
`rdx == 0` exits (`0059BEF7`); it walks `r10`'s `+0x10`/`+0x8` descriptor pair
— `r9d + [rdi+0x18]` must stay under `[rdi+4] & 0x0FFFFFFF` (`0059BF22`..`0059BF32`)
— then scans `esi = [rdi+0xC]` `0x38`-stride entries at `rbx = [r10+0x20]` for
the first whose `[+0x8]` base is `<= r11d = [rdi+0x14]+r9d` while `base +
max(1, [+0x14]) * [+0xC]` exceeds it (`0059BF50`..`0059BF77`). The
offset-coverage lookup that maps a serialized run onto its resident entries.
Callers `0059BED0` (self)/`0059C250`/`0059C700`/`0059CE30`/`005A0120`.

`00599670` (254 B) is a stride-broadcast + descriptor submit: `r13 = [rcx+0x10]`
supplies the source — `0063BB10(r13)` resolves it (`005996AC`..`005996B5`) — and
when non-null `r9d` rows of `r15 = [r13+0x38]` bytes are `00861EBA`-copied from
`rbp` into the `r14` output run (`005996BD`..`005996F4`). It then packs
`{edi, [rax+4]&0x0FFFFFFF, r15d, word 1}` at `rsp+0x38` (`00599729`..`00599746`)
and submits through `0059B090` with `r8 = ([rax+0x18]−[rax+0x14]) + [rsp+0x30]`
and `r9 = ([r13+0xF8]−[r13+0xF4]) + r14` (`00599700`..`0059974D`). Callers
`00599500`/`0059D590`/`0059D940`/`0059E300` — the namespace-schema readers this
contract covers.

## Cross-subsystem neighbours — SWE2-EC7 2026-09-18

**Audio — CLIENT (9 edges).** `005CD0A0`, the event-handle adapter's sibling head cited
above, is called by nine Audio-filed bodies (`002116B0`, `00212130`, `00219400`,
`0021A9F0`, and five more `0021xxxx` callers); the crossing is that the audio layer
creates the same event object the loader-side code waits on — it consults the shared
adapter, it does not share ownership of it.

**Input — SERVICE (1 edge).** `0016C6A0`, the sized free every `??_G` tail on this page
ends on, calls `00879570`, an Input-filed body — the CRT delete path reaching a body the
ledger files under Input; a one-edge filing artifact, not a shared responsibility.
- **Platform - MECHANICAL (5 edges).** Shared-helper fan-in on `005CD0A0`. All 5 edges run through it - one accessor’s spread, not a per-caller relationship.
- **Presentation - CLIENT and SERVICE (16 edges).** `0016D680`, `0019C580`, `001B8100`, `005CD0A0` (+2 more) are called by bodies filed to Presentation: `00183A00`, `00183C60`, `00183EE0`, Renderer_CreateRandomNoiseTextureFromGraphicsMT19937 (`001946E0`) (+11 more); `0063BB10` reaches bodies filed to Presentation: `00639A60` - shared machinery across the layer boundary, no shared ownership.
- **SaveLoad - CLIENT (1 edge).** `0019C580` is called by bodies filed to SaveLoad: `00866200` - shared machinery across the layer boundary, no shared ownership.
- **Save_Load_Settings - CLIENT (2 edges).** `0017D280` is called by bodies filed to Save_Load_Settings: GameSettingConfig_ParseText (`001DE5D0`), GameSettingConfig_ParseOneSettingValue (`001DF350`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - MECHANICAL (24 edges).** Fan-in on the shared accessor `0017D280`. All 24 edges run through it - one accessor’s spread, not a per-caller relationship.
- **WorldAreaField - CLIENT (1 edge).** `0017D280` is called by bodies filed to WorldAreaField: World_UpdateSimulationTick (`00314020`) - shared machinery across the layer boundary, no shared ownership.

## SWE2-EC7-34 update (2026-09-19) - `001C22A0`

`001C22A0` (962 B) is an EH-framed container lifecycle body - the `0017D260`/`00584730` CRT pair plus `001C19A0`/`0067ADD0`/`00861EBA`. Interior anchor `001C2317` (an `0017D260` call).

## SWE2-EC7-34 update (2026-09-19) - `0059B090`

`0059B090` (919 B) is the cluster-header vtable op - arg spill, `[rcx+0x10]` object load, then the `[rdx+8]`/`[rax+8]` vfunc pair plus `0063BC70`. Interior anchor `0059B14F` (the `[rdx+8]` vfunc call site).

## SWE2-EC7-35 update (2026-09-19) - `00679BF0`

`00679BF0` (722 B) is a cluster-header import bridge - `00D6CDC0`/`00D6CDA0`/`02D3F800`, `006CC670`/`0017D280` pairs plus five `008028xx` import thunks. Interior anchor `00679C27` (an `008028xx` thunk call).

## SWE2-EC7-43 update (2026-09-19) - `00610210`

`00610210` (284 B) is a Phyre-cluster-header body - `005FE1A0`/`01F44830`, `005CD5E0`/`005CD840`/`00606600`/`00808C40`. Interior anchor `00610240` (a `005CD5E0` call).

## SWE2-EC7-45 update (2026-09-19) - `0063CE80`

`0063CE80` (252 B) is the `Phyre.Reflection.CallbackAdapter` - `0059FDB0` single call; the page's per-member dispatch. Interior anchor `0063CEA2` (the `0059FDB0` call).

## SWE2-EC7-45 update (2026-09-19) - `00607D20`

`00607D20` (245 B) is a Phyre-caller body - `0016D6A0`/`005CC8C0`/`005CD0E0`/`005CD160`/`005CD1E0`. Interior anchor `00607D57` (an `0016D6A0` call).

## SWE2-EC7-46 update (2026-09-19) - `006793E0`

`006793E0` (225 B) is a Phyre-caller body - `00584730`/`00861EC0` plus `call [rax+8]`/`[rax+0x10]`/`[rax+0x30]` vcalls. Interior anchor `006793FC` (a `00584730` call).

## SWE2-EC7-49 update (2026-09-19) - `0067A350`

`0067A350` (190 B) is a Phyre cluster-header body - `005CC8C0`/`005CD0E0`/`005CD1E0`. Interior anchor `0067A3A3` (a `005CC8C0` call).

## SWE2-EC7-50 update (2026-09-19) - `001C19A0`

`001C19A0` (185 B) is a body - `0017D260`/`00861EBA`. Interior anchor `001C1A16` (an `0017D260` call).


## SWE2-EC7-66 update (2026-09-19) - `00609720`

`00609720` (133 B) is a phyre-cluster body - `005CD5E0`/`005CD840`. Interior anchor `00609747` (a `005CD840` call).


## SWE2-EC7-70 update (2026-09-19) - `005CC8C0` PhyreEngineThread ctor measured

`005CC8C0` (55 B) is the thread-descriptor ctor the cluster-header bodies
call: stores `rdx` at `[+0]`, the `00D36048` `"PhyreEngineThread"` string
pointer at `[+0x20]`, `dword[+8] = 0x10000`, `qword[+0x10] = 0`,
`dword[+0x18] = 1`, `dword[+0x28] = 1`, `qword[+0x30] = -1`, and returns
`rcx`. Call-free - a fixed 0x38-byte record initializer.
Interior anchor `005CC8D1` (the `0x10000` store).

## SWE2-EC7-72 update (2026-09-19) - `005CD840` + `0059FDB0` thread/member helpers measured

`005CD840` (104 B) is the wait-and-take body the cluster thread helpers
call: `[rcx]` is a waitable handle passed to `[008C20E0]` with
`INFINITE`; result `0x80` short-circuits to 0, otherwise `[008C20A8]`
supplies a size and `[008C2208]` allocs `0x1300`-family storage before
`[008C21F8]` releases - returning 9 on the taken path.
Interior anchor `005CD882` (the `[008C2208]` alloc call).

`0059FDB0` (102 B) is the virtual member fold: for `r8` elements strided
by `[rcx+0x38]`, calls vtable slot 0 (`call [r9]`) on each and ORs the
byte results into `bl` - the any-member predicate over the cluster's
member array.
Interior anchor `0059FDED` (the `call [r9]` vcall).

## SWE2-EC7-78 update (2026-09-20) - `006CC670` dual release measured

`006CC670` (36 B) is the teardown sibling of the pool pair:
`byte[+0x48]` cleared, `005CD5E0(rcx+0x28)` released, tail
`005CD5E0(+0x38)` - the matching unlock for the `006CC5A0` init's
two slots.
Interior anchor `006CC681` (the `005CD5E0` call).

## SWE2-EC7-79 update (2026-09-20) - `0067B100` counted-buffer replace measured

`0067B100` (127 B) is the `001B8100`-family replace: `edx == [rcx]`
early-outs; `ebx` nonzero allocates `rsi = 0017D260(ebx, 1)`, and
`ebx == 0` with no block returns `0xD`. When the old `[rdi+8]`
differs and `[rdi]` bit31 is clear, the old block gets `00584730`;
then `[rdi+8] = rsi`, `[rdi] = ebx` commit and 0 returns.
Interior anchor `0067B123` (the `0017D260` alloc call).

## SWE2-EC7-80 update (2026-09-20) - `005CD160` clamped-alloc wrapper measured

`005CD160` (127 B) is the size-clamped allocate-and-store the
`00607D20`/`00607E20` callers use: `r8d` clamps to `0x7FFFFFFF`,
`008C2210(0, 0, r8d, 0)` allocates and the pointer stores to `[rcx]`;
on NULL it fetches the error via `008C20A8`, formats through
`008C2208(0x1300, 0, err, 0x400, &buf)`, frees via `008C21F8` and
returns 9 - success returns 0. Same error arm as `005CD570`.
Interior anchor `005CD17E` (the `008C2210` alloc call).

## SWE2-EC7-116 update (2026-09-21) - `006CC6A0` measured

`006CC6A0` (110 B) is the
pair append `00679BF0` and
`0067A010` run: the
`006CC7C0` capacity check
on `(+0x18, [+0x14], edx,
+0x28, +0x10)`, then
`(edi, esi)` stores as a
dword pair at `[[+8] +
[+0x14]]` - the cursor
write the buffer family's
`006CC580`/`006CC4F0`
expose.
Interior anchor `006CC6D4`
(the `006CC7C0` call).

## SWE2-EC7-117 update (2026-09-21) - `006CC7C0` / `006A5950` / `00686D10` / `00686C20` measured

`006CC7C0` (146 B) is the
capacity check `006CC4F0`
and `006CC6A0` gate on:
`*rdx = r8 + r9 + 0x10`,
then a poll loop compares
`r14` against `dword[r15]`
(extended by `+0x4C` when
over) against
`dword[rdi]`; while the
budget is unmet and
`byte[+0x48]` is set it
calls `005CD840(rsi)` and
re-reads - a wait-gated
availability probe that
returns 1 after debiting
`+0x4C` from `*rdx`.
Interior anchor `006CC81E`
(the `005CD840` call).

`006A5950` (180 B) is the
small-vector store
`0059E300` and seven more
call: `r8d < 0` returns 5;
the bit-31-ownership count
at `[rcx]` selects the
`+8` inline slot or the
`qword[+8]` heap block, an
`r8d == 1` path writes
`[rdx]`'s first qword into
the inline slot, the old
`+8` frees through
`00584730` when its
ownership bit is clear and
it is not the inline
buffer, and `esi`
relatches the count.
Interior anchor `006A59DE`
(the `00584730` call).

`00686D10` (43 B) is the
three-field ~~status~~ size copy *(corrected 2026-10-02, OPUS: it returns 0 on both paths, `00686D26` and `00686D38`)*
`0059E300` runs: when
`r8`'s `+0x48`/`+0x4C`/
`+0x50` are not all zero it
writes them to `rcx`'s
`+0x20`/`+0x1C` and
conditionally `+0x24` -
~~the loader's error-field~~
~~propagation.~~ the header's three D3D11 sizes, which `00686DE0` allocates (`00686E2C`-`00686E32`) and reads from the file (`00686E44`) *(corrected 2026-10-02, OPUS: no error is produced or propagated)*.
Interior anchor `00686D28`
(the `+0x20` store).

`00686C20` (25 B) zeroes
the five qwords `+0`..
`+0x20` and returns `rcx` -
the record init
`0059E300` pairs with it.
Interior anchor `00686C2D`
(the `+0x18` store).

## Interior citations for the entry-cited functions (FABLE, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-contract-phyre-cluster-header-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00584E10` | 67 B | calls `00599770(rdx)` and copies `0x54` bytes from the returned pointer to `r8` (five 16-byte `movups` blocks at `+0` through `+0x40`, then dword `+0x50`), returning that last dword in `eax` | `00584E1C`, `00584E24`, `00584E43`, `00584E4A` |
| `0062F080` | 27 B | on the two-qword link pair at `rdx+8` (next at `+0`, previous at `+8`), stores the previous pointer at `+8` of the next node and the next pointer at `+0` of the previous node, then points both of the pair's own qwords at `rdx+8` itself | `0062F084`, `0062F08C`, `0062F090`, `0062F093`, `0062F096` |
| `0067ADD0` | 89 B | copies dword `rdx+0x10` to `rcx+0x10` and returns `rcx` at once when it is zero; otherwise calls `0067B100(rcx, dword [rdx] with bit 31 cleared)` and then, when qword `rcx+8` is non-null, `00861EBA(qword rcx+8, qword rdx+8, dword rcx+0x10)`, and returns `rcx` | `0067ADDC`, `0067ADED`, `0067ADF4`, `0067ADF8`, `0067AE0D` |
| `006CC920` | 56 B | returns 0 in `al` when byte `rcx+0x48` is zero; otherwise calls `005CD840(rcx+0x28)` and `005CD5E0(rcx+0x28)` and returns 1 | `006CC928`, `006CC938`, `006CC940`, `006CC94A`, `006CC951` |
