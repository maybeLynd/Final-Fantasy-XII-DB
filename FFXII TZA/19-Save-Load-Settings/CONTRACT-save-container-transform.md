---
contract: wrap and unwrap a save file - compress, then derive a key from the rotated game title and encrypt
category: 19-Save-Load-Settings
scope: family
level: L1
readiness: BEHAVIORALLY UNDERSTOOD
confidence: PROVEN
implements: 19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md
entries: ["00866200", "008666B0", "00865840", "00865AE0", "00865D90"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 40 addresses cited - 3 data, 8 entry, 29 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-13
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-13
  last_pass_state: opus-falsification-pass-1-2026-09-13
  crossref_clean: false
  reopened_count: 0
---

# Contract — the save container: compress, then encrypt under a rotated-title key

A save file is **compressed and then encrypted**. Recognising that wrapper is a separate question from
validating the game state inside it, and this contract covers only the wrapper.

Raised by ASTRA (`ASTRA-REQ-OPUS-SAVE-CONTAINER`, section 26) and re-derived here from the shipping
bodies, the import table and the string pool.

## 1. The key is derived from the game's own title, rotated

`00865840` (decrypt) and `00865AE0` (encrypt) share one derivation, and every step of it is a named
Windows CryptoAPI call rather than hand-rolled arithmetic:

| step | evidence |
|---|---|
| acquire a provider | `ADVAPI32!CryptAcquireContextW` at `008658AF` — container `L"RSA_SQEX_FFXII_TZA"` (`01CCFD20`), provider `L"Microsoft Enhanced Cryptographic Provider v1.0"` (`01CCFD90`), `dwProvType = 1` (`PROV_RSA_FULL`) — retried at `008658D6` with `dwFlags = 8` (`CRYPT_NEWKEYSET`) |
| create an **MD5** hash | `008658F7 mov edx, 0x8003` — **`CALG_MD5`** — into `CryptCreateHash` at `008658FC` |
| hash the rotated title | `CryptHashData` at `00865985` |
| derive a **128-bit RC4** key | `008659A5 mov edx, 0x6801` — **`CALG_RC4`** — with `0086599F mov r9d, 0x800000`, whose **upper 16 bits are `0x0080` = 128**, into `CryptDeriveKey` at `008659AF` |
| decrypt | `CryptDecrypt` at `00865A1F` in a **`0x3E8`-chunked in-place loop** — each iteration `memcpy`s up to `0x3E8` bytes into the output buffer, then decrypts that chunk in place with `Final = (chunk < 0x3E8)` so the RC4 stream chains across calls — then `CryptDestroyKey` / `CryptDestroyHash` / `CryptReleaseContext` |

**Handle cleanup is a single-exit epilogue.** Every failure bail and the success path funnel to
`00865A3F`/`00865A49`, which runs all three releases unconditionally, each null-guarded and nulled
on success: `CryptDestroyKey` at `00865A72`, `CryptDestroyHash` at `00865A8F`,
`CryptReleaseContext(hProv, 0)` at `00865AB6`. `00865AE0` (encrypt) has the same epilogue —
`00865D24`/`00865D41`/`00865D68` — and swaps `CryptEncrypt` (`008C2020`) for `CryptDecrypt` at
`00865CCA`. No arm leaks a handle, and no handle outlives the call: **the provider, hash and key
exist only for the duration of one transform.** The one lasting effect is the `RSA_SQEX_FFXII_TZA`
keyset container the `CRYPT_NEWKEYSET` retry creates — persistent in the user key store from the
first save operation onward.

**The key material is the game's own title string**, `'FINAL FANTASY XII THE ZODIAC AGE'` at
`01CCFCF8` — **exactly 32 characters**, matched by `00865918 mov ebx, 0x20`.

### The rotation, and why the hash is over 31 bytes rather than 32

```asm
0086592C  call strncpy                ; A <- the 32-char title
00865932  sub  ebx, edi               ; 32 - n
00865945  call memcpy                 ; B[0 .. 32-n)  = A[n .. 32)
0086595C  call memcpy                 ; B[32-n .. 32) = A[0 .. n)      -> B = rotl(title, n)
00865961  mov  byte ptr [rbp-0x12], 0 ; B + 0x1F  ->  B[31] = NUL
00865970  inc r8 / cmp byte [rax+r8],0 / jne     ; strlen(B)
00865985  call CryptHashData          ; (hash, B, strlen(B), 0)
```

> **The 31 is computed, not written down.** Byte 31 is NUL'd and the length passed to `CryptHashData`
> comes from an inline `strlen`, so it is 31 *because the title contains no earlier NUL*. A
> reimplementation that hard-codes 31 agrees with this build by coincidence; one that NULs byte 31
> and takes `strlen` agrees by construction.

## 2. The rotation amount travels through a global, and only one end bounds it

`n` is **not a parameter**. Both transforms read it from the same `.bss` dword:

```asm
0086590A  movsxd rdi, dword ptr [02EB3868]   ; in 00865840 (decrypt)
00865BAA  movsxd rdi, dword ptr [02EB3868]   ; in 00865AE0 (encrypt)
```

and exactly two bodies write it — the container reader and the container writer:

| writer | how it bounds the value |
|---|---|
| **`008666B0`** (read a save) | `00866802 mov eax, [rsi+8]` — **`header+8`** — then `00866805 cmp eax, 0x1F` / `00866808 ja` **bails out**, so the stored value is **0..31** |
| **`00866200`** (write a save) | `008663D0 and eax, 0x8000001F` with the `jge` / `dec` / `or 0xFFFFFFE0` / `inc` fixup — MSVC's **signed `% 32`**, whose result for a negative input is **negative** |

> **ASTRA's "header+8, range 0..31, not a slot or a seed" is confirmed — and on the reading side it
> is *enforced*, not merely observed.** `ja` is an unsigned test, so a huge or negative `header+8`
> from a malformed file is rejected before it ever reaches the transform. **The file-facing path is
> guarded.**
>
> **The asymmetry is the part worth recording.** The transforms `movsxd` the value — they *expect* a
> signed quantity — while only the reader constrains it to be non-negative. The writer's signed
> `% 32` can produce a negative `n`, and with a negative `n` the first `memcpy` length `32 - n`
> exceeds 32 and its source `A + n` points before the buffer. **Nothing in the transform re-checks.**
> Whether the writer's input can actually go negative is a property of its caller and **is not
> established here**; what is established is that the guard lives at the reader, not at the transform,
> so the invariant belongs to the producer.
>
> **Answered by falsification pass 1, section 5 (2026-09-13): it cannot.** The writer's input
> to the `% 32` is `abs(rand())`, so no reachable value is negative, and `INT_MIN` maps to `0`.
> The producer does enforce it. **The structural point above is unchanged** - the guard is at the
> producer and the reader, never at the transform - so this is an invariant to preserve rather
> than a hazard to fix.

## 3. Order of operations

**Write:** `00866200` mode 0 calls `0087AF40` (deflate at **level 9**) and then `00865AE0` — so the
payload is **compressed first, then encrypted**. **Read:** `008666B0` → `00865D90` calls `00865840`
(decrypt) and then the `0080C5A0` / `0080C5C0` uncompress wrapper — the exact inverse.

## 4. What this contract does not establish

- **The codec/file round trip**, caller allocation preconditions and ordinary scheduling — still
  open. Provider/allocator effects and handle cleanup are established 2026-09-18: the provider is
  `Microsoft Enhanced Cryptographic Provider v1.0` (`PROV_RSA_FULL`) under a persistent
  `RSA_SQEX_FFXII_TZA` keyset created by the `CRYPT_NEWKEYSET` retry, and cleanup is a single-exit
  epilogue releasing key/hash/context on every arm (§1's tail).
- **The outer reader's admission rules** — re-derived from `008666B0` 2026-09-14 (was ASTRA's
  reading carried forward). Admission is, in order: file length **> 4** and the four bytes
  `'SAFH'` (`008667C2`–`008667E3` — the writer stamps `0x48464153` at `008663BD`); file length
  **> 12** (`008667E9`), so the 12-byte header exists; `header+8` `<= 0x1F` unsigned
  (`00866805`/`00866808`); `header+4` `<= 0x100000` unsigned (`00866817`/`0086681D`). The payload
  is `file[+0x0C .. size)`, passed to `00865D90` as `size − 12`. On return the reader requires
  the actual decompressed length — which `00865D90` writes back through its out-dword — to
  **equal `header+4` exactly** (`00866866`–`0086686D`) and `header+4` **> 0** (`0086686F`–
  `00866871`). **There is no version field and no checksum**: the header is exactly magic +
  declared size + rotation. The uncompress wrapper (`0080C5A0` → `0080C5C0`, zlib **1.2.11**
  `inflateInit_`/`inflate`/`inflateEnd` at `0080E040`/`0080C750`/`0080DF00`, stream `0x58`; `0080C750` interior read 2026-09-17 (SWE2-FRONTIER): `0080E1C0` first at [`0080C76A`](../_index/ADDRESS-INDEX.md), `0080E5F0` at `0080C88B` — the zlib state-machine calls)
  **exposes no full-consumption check** — `Z_STREAM_END` returns success with input remaining;
  the consumed count is written back through `[r12]` but never tested (`0080C6A1`–`0080C6A3`).
- **No malformed save was constructed and no failure path was executed.** Every statement here comes
  from the shipping instructions, the import table and the string pool.
- The **zlib family disposition** is connected to these actual callers only; it is not a claim of
  full-library parity.

## 5. State

| | fields / globals | evidence |
|---|---|---|
| read | title literal `01CCFCF8` (32 chars); rotation dword `02EB3868`; save header `+8` | `0086590A` / `00865BAA` `movsxd`; `00866802` |
| written | `02EB3868` (by `00866200` at `008663ED` and `008666B0` at `00866802`); save header `+8` (`008663F3`) | pass 1 |
| allocated | CryptoAPI provider context, hash and key handles — per call, all released | §1's table |
| deallocated | `CryptDestroyKey` / `CryptDestroyHash` / `CryptReleaseContext` after each transform | `00865A1F` tail |

No persistent engine state is touched: the only cross-call state is the rotation dword and the
header field that carries it inside the file.

## 6. Relationships

**Write path:** `00866200` (container writer) mode 0 → `0087AF40` (deflate, level 9) → `00865AE0`
(encrypt) → `ADVAPI32` `CryptAcquireContextW` / `CryptCreateHash` / `CryptHashData` /
`CryptDeriveKey` / `CryptEncrypt` family, plus `rand` through IAT `008C3098`.

**Read path:** `008666B0` (container reader) → `00865D90` → `00865840` (decrypt) →
`0080C5A0` / `0080C5C0` (the uncompress wrapper) — the exact inverse of the write order.
The uncompress shim is **not** exclusive to this path: loader `0019AA20` calls it at four
sites (chunked inflate into a `0x10000` output bound). Compress2 `0087AF40` has exactly one
caller, the writer `00866200` — the write side is exclusive, the read side is shared.

- **Platform — SERVICE (SWE2-CONTRACT 2026-09-20).** `0019AA20` — the loader the §14
  zlib-disposition census names as the uncompress shim's second client — calls the
  Platform-filed `0019A510`. The loader is engine code renting two libraries at once:
  zlib's `uncompress` for the compressed arm and the platform service `0019A510` provides.
  Neither edge makes the loader's work part of this contract; the crossing is that the
  read side's shared client is itself a client of a third family.

The two writers of `02EB3868` are the container reader and the container writer themselves; the two
readers are the transforms. Nothing else touches it.

## 7. State transitions

```
plain image --00866200: deflate(level 9) then encrypt(rotl(title, n))--> container on disk
container --008666B0: admit (size > 4 and 'SAFH'; size > 12; header+8 <= 31 unsigned;
    header+4 <= 1 MiB unsigned; after transform actual_out == header+4 and header+4 > 0)-->
    decrypt then uncompress--> plain image
rotation n: write side chosen fresh per save (abs(rand()) % 32, stored header+8);
            read side taken from header+8 of the file being read
```

## 8. Script · resource · event interactions

The resource is the save file itself — this contract is the container format layer. No script verb,
opcode or authored table participates; the only external inputs are the file bytes, the title
literal and the `rand()` stream on the write side.

## 9. Determinism

- **RNG** — `rand()` (CRT, IAT `008C3098`) drawn **once per save written**; `abs(rand()) % 32`
  becomes the rotation amount `n`, stored at `header+8`. The write side is therefore not
  reproducible by input alone — a round-trip test must take `n` from the file's header.
- **Timing / ordering** — compression strictly precedes encryption on write; decryption strictly
  precedes decompression on read. No interleaving exists.
- **Threading** — no cross-call synchronization is established or needed by the transform itself:
  each call provably acquires and releases its own provider/hash/key triplet (§1's tail), so two
  concurrent transforms hold independent CryptoAPI state.

## 10. Failure paths and edge conditions

- **Provider acquisition** — `CryptAcquireContextW` is retried with `dwFlags = 8`
  (`CRYPT_NEWKEYSET`) on failure, so a missing keyset is created rather than fatal.
- **`header+8` out of range** — the reader's unsigned `ja` rejects values above `0x1F` before any
  transform runs; the file-facing path is guarded.
- **Bad magic or truncated header** — files `<= 4` bytes, files whose first four bytes are not
  `'SAFH'`, and files `<= 12` bytes are rejected before the rotation field is even read
  (`008667B8`–`008667E9`). The writer stamps the magic itself at `008663BD`.
- **Declared size out of range** — `header+4` `> 0x100000` (unsigned) rejects before allocation
  (`00866817`); a negative-as-signed field is a large unsigned value and fails the same `ja`.
- **Length mismatch** — after the transform the actual decompressed length must equal `header+4`
  exactly and `header+4` must be `> 0` (`00866866`–`00866871`); either failure discards the image.
- **Negative `n`** — impossible on reachable inputs: the writer computes `abs(rand()) % 32` and
  even `INT_MIN` maps to `0` (pass 1, §"Falsification"). The transform itself never re-checks —
  the invariant is enforced at the producers, and a reimplementation must preserve that placement.
- **No full-consumption check** — the zlib 1.2.11 inflate wrapper returns success on
  `Z_STREAM_END` even with compressed input remaining (`0080C6D0`); trailing bytes after the
  deflate stream are ignored rather than rejected.

## 11. Observable behaviour

The save file's ciphertext, its `header+8` rotation field, and the global `02EB3868` are all
externally measurable. A correct reimplementation produces a container the shipping reader accepts —
and §13 names the experiment that would prove it.

## 12. Reproduction formula

```
write (00866200, mode 0):
    n      = abs(rand()) % 32                  # signed %, fixup makes INT_MIN -> 0
    [02EB3868] = n;  header[8] = n
    B      = rotl("FINAL FANTASY XII THE ZODIAC AGE", n)   # B[0..32-n)=A[n..32); B[32-n..32)=A[0..n)
    B[31]  = 0                                             # so strlen(B) == 31
    key    = CryptDeriveKey(MD5(B, strlen(B)), CALG_RC4, 0x800000)   # 128-bit RC4
    out    = RC4_encrypt(key, deflate(payload, level=9))   # compress FIRST, then encrypt

read (008666B0 -> 00865D90 -> (00865840 decrypt, 0080C5A0/0080C5C0 zlib-1.2.11 inflate)):
    if size <= 4 or file[0..4) != 'SAFH' or size <= 12: reject
    n      = header[8];  if (u32)n > 0x1F: reject          # unsigned guard at the reader
    if (u32)header[4] > 0x100000: reject                   # declared size <= 1 MiB
    [02EB3868] = n
    B, key as above
    out    = uncompress(RC4_decrypt(key, file[0x0C..size)))  # input length = size - 12
    if len(out) != header[4] or header[4] <= 0: reject     # exact-length, positive
```

## Falsification pass 1 — 2026-09-13 (OPUS): the open question is closed, and the answer adds a fact

*(Unnumbered: it previously held the `## 5.` heading, which collides with the template's State
section now written above.)*

Re-derived from the shipping image
([`falsify_save_container.py`](../../Tools/analysis-kit/gfz-scripts/falsify_save_container.py)).
§1's `CALG_MD5`, `CALG_RC4`/`0x800000`, the 32-character literal and §2's two-readers/two-writers all
confirm independently. **The pass was aimed at the one row §15 marks `not established`.**

### `whether the writer's input can actually go negative` — **no, and it is provable**

§2's warning rests on the writer's signed `% 32` being able to produce a negative `n`, which would
make the first `memcpy` length `32 − n` exceed 32 and its source point before the buffer. The three
instructions **immediately above** the `% 32` decide it, and §2's listing starts one instruction too
late:

```asm
008663C5  call qword ptr [rip + 0x5CCCD]   ; -> 008C3098 = api-ms-win-crt-utility-l1-1-0!rand
008663CB  cdq                              ; \
008663CC  xor  eax, edx                    ;  >  branchless abs(eax)
008663CE  sub  eax, edx                    ; /
008663D0  and  eax, 0x8000001F             ; MSVC signed % 32, as §2 says
```

**The writer computes `abs(rand()) % 32`.** `rand()` returns `0..RAND_MAX` and is never negative, so
the `abs` is a no-op on every reachable value. And the single input whose `abs` *is* negative —
`INT_MIN` — runs the fixup to `0x80000000 → dec → 0x7FFFFFFF → or 0xFFFFFFE0 → 0xFFFFFFFF → inc → 0`.
**The rotation amount is `0..31` on the write side for every possible input**, by two independent
arguments, so the invariant §2 attributes to the producer is in fact enforced *inside the producer*.

> **§2's structural point survives and should not be softened.** The guard still lives at the reader
> and at the writer, **not** at the transform; the transforms still `movsxd` a value nobody re-checks.
> What changes is the risk, not the shape: there is no reachable path today that hands the transform a
> negative `n`, so this is an invariant to preserve rather than a defect to fix.

### The fact the contract did not carry: the rotation amount is **random per save**

§2 says `n` travels through a global and is bounded by its two writers. It never says **where the
write-side value comes from**, and the answer is `rand()` — a fresh amount each time a save is
written, stored at `header+8` so the reader can undo it. That is not a detail: a reimplementation of
the *writer* that picks a fixed `n` still produces files this build reads correctly, and is still
wrong about the format, while one that reads `header+8` on the *read* side is correct either way.
**The asymmetry the contract already noticed has a cause, and the cause is that the value is chosen,
not derived.**

### One of my own results was wrong before the contract's was

The first run reported the 32-character title claim **FAILED**, reading three bytes of garbage at
`01CCFCF8`. The claim is correct; my reader used the database's usual shorthand
`VA − 0x121000 + 0x600`, which is the **`.text`** mapping and nothing else, on an address in a data
section. Resolved through the PE section table it reads `FINAL FANTASY XII THE ZODIAC AGE`, 32 bytes.
*A shorthand that is right everywhere it has been used is not a shorthand that is right everywhere* —
and it produced a confident refutation of a true claim, which is the more dangerous direction.

## 13. Runtime validation

**Evidence class: isolated original-code execution, plus static reading, the import table and the
string pool.** ~~Nothing has been executed.~~ (2026-09-13, falsification pass 1.)

> **CORRECTED 2026-09-16 (OPUS). "NOTHING HAS BEEN EXECUTED" WAS FALSE BY THE NEXT DAY.**
> [`EXP-088`](../_experiments/EXP-088-save-container-transform.md) (SWE2-ORACLE, 2026-09-14, method
> B, isolated original-code under Unicorn against the shipping EXE) executed **five bodies** — writer
> `00866200`, reader `008666B0`, reader inner `00865D90`, decrypt `00865840`, encrypt `00865AE0` —
> and reports **46/46 cases pass, 9/9 byte-level mutants detected**.
>
> Found by `check_experiments.py`, which lists EXP-088 under **NOT CITED — a RUN experiment its
> contract never names** *and exits 0*, so nothing had to look. The missing back-link was hiding a
> flatly false sentence, and this is the bluntest of the four found at the same HEAD: not a stale
> qualifier but a categorical negative that a published experiment had already contradicted.
>
> **What is still true from the struck sentence, and §4 still says it:** *no malformed save was
> constructed and no failure path was executed*. Executing the transform is not executing its
> failure modes, and isolated original-code is not live evidence.

§4 says it directly: *no malformed save was constructed and no failure path was executed*. The
CryptoAPI constants, the rotation, the `abs(rand()) % 32` amount and the compress-then-encrypt order
are all read from instructions and imports.

**What would move this.** Round-tripping one real save file: deflate at level 9, rotate the title by
a chosen `n`, MD5 it, derive the RC4 key and compare the ciphertext against the shipped file, then
invert. That is `INTEGRATION` parity in the `PARITY-STANDARD` sense and needs no running game — the
container is a pure function of the file and the title — so it is a **`SWE2-ORACLE`-shaped experiment,
not an `ASTRA` one**, and does not wait on the usage window.

**One caution for whoever writes it.** `n` is `rand()`, so the writer is not reproducible by input
alone; a round-trip test must take `n` from `header+8` of the file under test rather than expect a
particular value.

## 14. Unresolved

1. ~~**The codec/file round trip** — provider and allocator effects, handle cleanup paths, caller
   allocation preconditions (§4). *Resolved by:* the ORACLE-shaped round-trip experiment §13 names.~~
   **RESOLVED 2026-09-16 by [`EXP-088`](../_experiments/EXP-088-save-container-transform.md)** — the
   experiment this item named has run: SWE2-ORACLE, method B, isolated original-code under Unicorn
   against the shipping EXE, **46/46 cases, 9/9 byte-level mutants**, five bodies (writer `00866200`,
   reader `008666B0`, reader inner `00865D90`, decrypt `00865840`, encrypt `00865AE0`). The round
   trip passed **in both directions** and every admission gate executed.

   **Five executed facts this contract did not describe, and four of them are failure behaviour —
   which is the half a reimplementer gets wrong:**
   - the reader's `size <= 4` and bad-magic gates **push the RAW FILE into the output vector**. That
     is a fallback fill, not a refusal, and nothing in §4 said so;
   - `n > 31` rejects **before** the `02EB3868` store **but still truncates the vector**;
   - the writer returns `eax = 0` on **both** success and deflate-overflow abort, leaving a
     header-only `sav_tmp` **abandoned rather than removed** — a silent abort indistinguishable from
     success at the call site;
   - the `sav_org` backup runs **only** when the global `02B40E04` is set **and** the target already
     exists;
   - the encrypt/decrypt chunk `Final` flag is `chunk < 0x3E8` **literally**, so a length that is an
     exact multiple of 1000 **never sets Final**; and the reader fills the vector to the **declared**
     size rather than the actual one.

   **AND THE LIMIT ORACLE DISCLOSED, which bounds what §13 may claim: the CryptoAPI is HLE.** Call
   order, algorithm constants, flags and hash-data are *measured*; the **derived key bytes against a
   real `advapi32` are not**. A real `.sav` cross-check, or a live call into the system provider, is
   the remaining parity step — so this item is resolved for the round trip and **not** for the
   cryptography. *An emulated provider agreeing with itself is not the same as agreeing with
   Windows.*
2. ~~**The outer reader's admission details** — ASTRA's readings carried forward, not
   re-derived.~~ **RESOLVED 2026-09-14** — re-derived from `008666B0`; every ASTRA reading
   confirmed, plus two the contract did not carry: the `'SAFH'` magic gate (writer stamps it at
   `008663BD`) and the >4/>12 length gates. The "positive exact output length" is precisely
   `actual_decompressed == header+4` and `header+4 > 0` (`00866866`–`00866871`). The uncompress
   path is zlib **1.2.11** inflate and exposes no full-consumption check. Full gate order in §4.
3. ~~**The zlib family disposition** — connected to these callers only; full-library parity is not
   claimed.~~ **RESOLVED 2026-09-20 (SWE2-CONTRACT), disposition: stock zlib 1.2.11, linked
   twice.** The middleware inventory's family census
   ([`third-party-middleware-inventory`](../23-Third-Party-Libraries/third-party-middleware-inventory.md),
   56 members in `members/zlib.tsv`, ranges `0080C5A0`–`0080F2BC` inflate and `0087AF40`–`0087F180`
   deflate) is independently reproduced and extended:

   - **The "these callers only" framing was wrong, and the correction is in the contract's own
     favour.** An image-wide inbound census shows `uncompress` `0080C5A0` is called by the save
     reader *and* by loader `0019AA20` at four sites (`0019ABD7`, `0019AC82`, `0019AD2B`,
     `0019AAAE` — chunked inflate with a `0x10000` output bound), matching the inventory's
     inbound control exactly. `compress2` `0087AF40` is called only by the save writer. So the
     family is a *shared library* the save path rents, not save-path code — which is precisely
     why reconstructing it from upstream 1.2.11 source is the right move.
   - **The shipped fixed Huffman tables are byte-identical to stock.** `lenfix[512]` at
     `01CC73B0` and `distfix[32]` at `01CC7BB0` were compared entry-by-entry against the
     generated `inffixed.h` — **0/544 mismatches**. `inflate.c`'s `order[]` sits at `01CDACF8`,
     the crc32 table at `01CC7E70`.
   - **Every stock message string is present**: the 15 inflate.c `msg` literals, the 5
     inftrees.c messages, and the `z_errmsg` set including `incompatible version`. Both
     copyright banners (`inflate 1.2.11`, `deflate 1.2.11`) stand.
   - **The entry-point shapes are stock**: `0087C9F0` is the `deflateInit_` thunk forwarding to
     `deflateInit2_` `0087C760` with stock defaults (windowBits 15, memLevel 8, default
     strategy); `deflate` `0087BD60` opens with `deflateStateCheck` `0087CB10` and the
     `flush > Z_BLOCK` gate; `deflateEnd` `0087C6C0` returns `Z_STREAM_ERROR` on a bad state;
     `0087AF40` is `compress2` (stack `z_stream`, `deflateInit_` → `deflate` loop →
     `deflateEnd`), which is why "deflate at level 9" is really `compress2(…, 9)`.

   **What is NOT claimed, deliberately:** instruction-level identity with any particular
   upstream *build* — compiler and flag differences make the bytes differ without the source
   differing — and parity of entry points the reachable set never exercises (`inflateBack*`,
   `deflateSetDictionary`, the gzip-arm internals beyond their message strings). The claim is
   the inventory's: **nothing FFXII-specific is interposed; the save container can be
   reconstructed against upstream zlib 1.2.11 source directly.**

## 15. Evidence

> **Numbered 15, header lowercase `claim`, on purpose.** `parity_status.py` reads a
> contract's claim list from a heading that literally begins `## 15.` and keeps only a table
> whose first header cell is `claim`; miss either and it finds **zero** claims and refuses
> any harness written against this page instead of reporting a mismatch.

| claim | evidence | tier |
|---|---|---|
| the key is MD5 over the rotated 32-character game title, deriving a 128-bit RC4 key | `CALG_MD5` `0x8003` at `008658F7`; `CALG_RC4` `0x6801` at `008659A5`; `0x800000` at `0086599F`; the literal at `01CCFCF8` | 1 |
| the hashed length is 31 because byte 31 is NUL'd and the length comes from an inline strlen | `00865961` writes NUL at B+0x1F; `00865970`-`00865978` is the strlen | 1 |
| the rotation amount is a global, not a parameter | read `movsxd` at `0086590A` and `00865BAA`; written only by `00866200` and `008666B0` | 1 |
| the reader ENFORCES header+8 <= 31 with an unsigned test | `00866805 cmp eax, 0x1F` / `00866808 ja` | 1 |
| ~~the writer's signed % 32 can produce a negative amount~~ **SUPERSEDED by pass 1** - the `% 32` would, but its input is `abs(rand())`, so no reachable input is negative. **What stands: the transform never re-checks the amount** | `008663D0 and eax, 0x8000001F` with the `jge`/`dec`/`or`/`inc` fixup | 1 |
| the writer's rotation amount is `0..31` and **cannot** go negative — it is `abs(rand()) % 32`, and even `INT_MIN` maps to `0` | `008663C5` calls `rand` (IAT `008C3098`, resolved through the import table); `008663CB`-`008663CE` is a branchless `abs`; `008663D0` is the signed `% 32`. Closed by falsification pass 1, §5 | 1 |
| the rotation amount is **chosen at random per save**, not derived from the data | the same `rand()` call at `008663C5`, whose result is stored to `02EB3868` at `008663ED` and to the header at `008663F3` | 1 |
| the reader gates admission on a `'SAFH'` magic and file length | `008667C2`-`008667E3` four byte-compares `0x53`/`0x41`/`0x46`/`0x48`; `008667B8 cmp rbp, 4` and `008667E9 cmp rbp, 0xC` length gates; writer stamps `0x48464153` at `008663BD` | 1 |
| the reader enforces declared size `header+4 <= 1 MiB` | `0086680E mov edx, [rsi+4]` / `00866817 cmp edx, 0x100000` / `0086681D ja` | 1 |
| the decompressed length must equal `header+4` exactly, and `header+4` must be positive | `00865D90` writes the actual out-length back through its out-dword (`00865E08`-`00865E0E`); `00866866`-`0086686D` compares it to `[rsi+4]`; `0086686F`-`00866871` rejects `header+4 <= 0` | 1 |
| no version field and no checksum exist in the 12-byte header | the header is exactly `+0` magic, `+4` declared size, `+8` rotation; every gate in `008666B0` enumerated in §4 | 1 |
| the uncompress path is zlib 1.2.11 inflate with no full-consumption check | `0080C5FD` passes `"1.2.11"` (`01CC73A4`) and `0x58` to `inflateInit_` (`0080E040`); `0080C67F` is `inflate`, `0080C6CB` is `inflateEnd`; `Z_STREAM_END` returns 0 with input possibly remaining (`0080C6D0` `je` leaves `ebp` 0); consumed count written to `[r12]` at `0080C6A1` but untested | 1 |
| the provider is `Microsoft Enhanced Cryptographic Provider v1.0` (`PROV_RSA_FULL`) under container `RSA_SQEX_FFXII_TZA` | `L"RSA_SQEX_FFXII_TZA"` at `01CCFD20`, `L"Microsoft Enhanced Cryptographic Provider v1.0"` at `01CCFD90`, `dwProvType = 1` into `CryptAcquireContextW` at `008658AF`; the `008658D6` retry carries `dwFlags = 8` (`CRYPT_NEWKEYSET`), which creates the keyset on first use | 1 |
| CryptoAPI handle cleanup is a single-exit epilogue — key, hash and context released on every arm, none outliving the call | `00865A3F`/`00865A49` is the common tail: `CryptDestroyKey` `00865A72`, `CryptDestroyHash` `00865A8F`, `CryptReleaseContext` `00865AB6`, each null-guarded and nulled on success; `00865AE0` mirrors it at `00865D24`/`00865D41`/`00865D68` with `CryptEncrypt` (`008C2020`) at `00865CCA` | 1 |
| the payload is processed in `0x3E8`-byte in-place chunks, RC4 stream chaining across calls | `008659E0` caps `esi` at `0x3E8`; the loop `memcpy`s the chunk into the output buffer then `CryptDecrypt(hKey, 0, Final = (chunk < 0x3E8), 0, out, &len)` at `00865A1F`; total processed written to the caller's out-dword at `00865A37` | 1 |
| the zlib family is stock 1.2.11, a shared library the save path rents — not save-path code | `lenfix[512]` `01CC73B0` + `distfix[32]` `01CC7BB0` byte-identical to `inffixed.h` (0/544 mismatches); all 15 inflate.c + 5 inftrees.c + `z_errmsg` strings present; `order[]` `01CDACF8`; inbound census: `0080C5A0` ← `0019AA20`×4 + `00865D90`, `0087AF40` ← `00866200` only; `0087C9F0`/`0087BD60`/`0087C6C0` stock `deflateInit_`/`deflate`/`deflateEnd` shapes | 1 |

## 16. Parity plan

No differential harness exists for this contract — §13 is honest that nothing has been executed.
The test §13 names is a container **round-trip**, not an instruction-level fixture: deflate a known
payload at level 9, rotate the title by the `n` read from `header+8`, MD5 it, derive the RC4 key and
compare ciphertext against a shipped save — `INTEGRATION` parity, ORACLE-shaped, needing no running
game.

**Dimensions that apply when it is built:** `CALCULATION` (the rotation, the 31-byte hash length,
`abs(rand()) % 32`), `SERIALIZATION` (the container byte format), `EDGE-CASE` (`header+8 > 31`
rejected; `INT_MIN` → 0). `INTEGRATION` is bounded at the `ADVAPI32` import — a stubbed CryptoAPI
proves only the boundary observed, per the pass rules. `RNG` is present exactly once (the write-side
`rand()`); `TIMING`, `PRESENTATION`, `STATE-TRANSITION` and `FULL-SUBSYSTEM` do not apply to a pure
file transform.

## SWE2-EC7-112 update (2026-09-20) - `00866150` measured

`00866150` (172 B) is the
vector set_capacity
`008666B0` runs: `edx`
bytes against the
`[+0x10] - [+0]` capacity
span return early when the
request fits; else the
`[+0x18]` allocator's
`vtable[+0x10]` call reserves
`rsi`, `008C2A40` memmoves
the `[+8] - [+0]` used span,
the old block goes back
through `vtable[+0x18]`, and
`[+0]`/`[+8]`/`[+0x10]`
relatch to the new buffer.
A zero request still moves
the pointers - the free is
skipped only when `[+0]`
was null.
Interior anchor `008661A9`
(the `008C2A40` memmove).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (OPUS, 2026-09-29)

The read side's uncompress shim `0080C5A0` is shared (§ read path). Its second client, the loader `0019AA20`, brings
the loader's own neighbours onto this page. None of them is a save-container relationship.

- **Resource — CLIENT, three edges.**
  - `0019AA20` (1,099 B, filed `Resource`) calls `0080C5A0` at four sites to chunk-inflate into a `0x10000` bound.
  - `0019AA20` also calls `0019A510`.
  - It is itself called by the file-size-table record commit `0019AFE0`.

  The loader's inputs are the file-size tables (`file-size-tables-fst`), not save containers.
- **Platform — SERVICE, two edges.**
  - `0019A510` is the `FindResourceW` loop over `"class%d"` names that
    [the game is a Phyre application](../22-Middleware-PhyreEngine/Application-Framework-Boundary/the-game-is-a-phyre-application.md)
    reads. It hands each hit to the selector `0019A5B0`.
  - `0019AA20` calls it.

  So the loader reads an embedded Windows resource, which is platform glue this contract never touches (the
  SWE2-CONTRACT note under the read path says the same).

*Tier 2: ledger names, sizes and `edges.tsv`, with roles as the cited pages read them; no body read for this note.*
