---
system: How a path is resolved to bytes - the file stream reader and its two lookups
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED - every §8 question is answered (owner re-status 2026-09-30, OPUS, on SWE2-CONTRACT's DD batch 8; the Audio and Input callers are named as this page's boundary) - §8's route questions answered 2026-09-27 (no loose-file route; route 1 is the RAM file cache); the +0x20 layout question answered 2026-09-27 (a base); residue reconciled 2026-09-30 (SWE2-CONTRACT, DD batch 8): the selector values' effects read from the resolver, the UTF-16 copy shown to have no consumer, route 1's lookup anchored, the prefetch loop placed as one client of route 1; key addresses, modding and evidence sections added
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-21 (FABLE) - 39 addresses cited - 5 data, 18 entry, 16 interior, every one resolving into a known section of the authority image.
    **This records a check performed on that date, NOT the method of the
    original derivation**, which this block never carried; see this
    document's own evidence section for that.
last_reviewed: 2026-09-29
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-path-resolve-falsification-pass-1
  crossref_clean: false
  reopened_count: 0
---

# How a path is resolved to bytes - the file stream reader and its two lookups

> Seven documents cite `00597970` without reading it - calling it "the file-cache request" and listing
> a battery of `0059xxxx` neighbours as unread. It is the **constructor of a PhyreEngine file
> stream reader**, and the routine behind it resolves a path through **two different lookups with
> two different hashes** - one keyed by an **uppercased** backslash path, the other by a
> **lowercased** forward-slash path. This page reads that interface and both key derivations.

**Scope.** Static disassembly of the shipping EXE plus its PE import directory, and one control
against the shipped file tree. **No runtime observation.** Where a branch is named, it is named
from a body read end to end; where it is not, §8 says so.

## What the player sees (SWE2-CONTRACT, 2026-09-30)

Every asset the game opens by name, such as a model, texture, script or table, passes through this reader. The file
is looked up first in a RAM cache and otherwise in the single `FFXII_TZA.vbf` archive. There are no loose files on
disk to fall back to. A name that neither lookup finds logs `Big file open failed`, and that asset does not load.
Nothing here is visible in play except as load time: a cached asset is served from memory, and an uncached one is
read from the archive.

## 1. The class

`00597970` constructs **`Phyre::PSerialization::PStreamReaderFile`**, read from the RTTI
complete-object locator behind its vtable. The constructor installs the base vtable and then
overwrites it with the derived one, which is the ordinary two-phase MSVC construction:

| vtable | class | slots |
|---|---|---|
| `00D26C60` | `Phyre::PSerialization::PStream` | slot 0 only; slots 1-4 are `_purecall` - an abstract base |
| `00D26C90` | `Phyre::PSerialization::PStreamReaderFile` | seven, bases `PStreamFile`, `PStreamFileWin32`, `PStreamReader`, `PStream`, `PMemoryBase` |

**The identity is not new.** [`vtable-method-index.md`](../../00-Engine-Core-Runtime/Object-Model/vtable-method-index.md)
already names this class and gives slot numbers for four of the seven entries. **What was missing is
what the slots do**, which is what `BA-2` asks for: *the index gives identity - class and slot - not
behaviour.*

## 2. What the seven slots do

| slot | body | what it does |
|---:|---|---|
| 0 | `00598280` | destructor, over `PStream`'s `00598210` |
| 1 | `0059BD40` | **Close** - releases the buffer backing, then the second backing, returns true |
| 2 | `0059D920` | **IsOpen** |
| 3 | `0059ED70` | **Rebind** - re-resolves a new path, re-copies it, frees the old copy conditionally |
| 4 | `0059FAC0` | **Close-then-rebind** - slot 1, then slot 3, then clears `+0x18` |
| 5 | `0059D4B0` | **Read** - from the buffer, else `ReadFile`, else the second backing |
| 6 | `0059FDA0` | **Seek** on the buffer backing |

**Slot 2 is twenty-seven bytes and settles what "open" means here.** It returns
`!(+0x28 == -1 && +0x30 == 0 && +0x40 == -1)` - false in exactly the state the constructor writes,
true as soon as any one of the three backings is bound. That is the test
[the resource request queue](../the-resource-request-queue.md) means when it says a kind-2 record
proceeds "when `0059D920` accepts it".

**Slot 5 is where the three backings show themselves.** It reads from the in-memory buffer if there
is one; otherwise, if its third argument is set and `+0x28` is not `-1`, it calls
**`KERNEL32!ReadFile`** on that handle (resolved from the import directory, not guessed); otherwise
it falls to `+0x40`. So a stream is backed by *a buffer, a Win32 handle, or a package entry*, and
`IsOpen` is the disjunction of the three.

### 2a. The path pointer carries an ownership bit

`+0x10` holds a `strdup` of the path (`001C26B0`: `strlen`, allocate, `memcpy` - **a copy, not a
hash**). **Its low bit is an ownership tag**, and three independent sites agree on it:

- slot 3 frees the old pointer only when `(ptr & 1) == 0` (`0059EDBF`-`0059EDC9`);
- slot 4 computes `ptr - (ptr & 1)` before handing it on (`0059FADB`-`0059FAE9`);
- the base destructor `00598100` frees only when the bit is clear (`00598120`-`0059812B`).

*One site would have been a curiosity; three make it the calling convention.* A borrowed literal is
passed with the bit set and never freed.

## 3. The data-source selector

The constructor takes a third argument and stores it as a byte. **The resolver may then overwrite
it**, so it is not simply "what the caller asked for". Measured over **every** call site -
eighteen of `00597970` and two of `00597930`, with completeness cross-checked against the raw
call index rather than the call-graph tool alone:

| selector | sites |
|---:|---:|
| `0` | 5 |
| `1` | 13 |
| `5` | 1 |
| ~~`24`~~ `3` or `4` | 1 |

*Corrected 2026-09-29 (OPUS, falsification pass 1, `CON-165`): the fourth row is `001DAFD8`'s `lea r8d, [r14 + 3]`. Every path to
it sets `r14b` to 0 or 1 first, so it passes 3 or 4 and never 24. The 13 is 11 sites of `00597970` plus both sites of
`00597930`, whose selector arrives in `r9b`.*

**This corrects a published figure.**
[How the prefetch manifests are read](../Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md)
states that each token is passed to `FUN_00597970(…, token, 5)` at `001DA758` and `001D9B75`, and
its own open-questions section says "the mode argument `5` is passed at every call site". **Both
cited sites pass zero** - `001DA74C` and `001D9B6A` are each `xor r8d, r8d` immediately before the
call. Filed as `FABLE-CONTRA-PREFETCH-SELECTOR-IS-ZERO-NOT-FIVE`.

**But that page's instinct was right, and the correction is narrower than it first looks.** The two
sites it cites are the opens of the *manifest files themselves*; the **tokens** parsed out of them
are opened in a loop immediately afterwards, and that loop does pass **5**, every time. So "5 per
token" is correct and "5 at these two sites" is not.

**And what the loop does with each token is the answer to that page's first open question.** Per
token it **constructs a stream and then immediately closes and destroys it, without ever reading**:

```asm
001DA810  mov  r8b, 5                 ; the selector
001DA813  mov  rdx, [rbx + 0x10]      ; the token
001DA81B  call 00597970               ; construct - which resolves
001DA825  call 0059BD40               ; Close
001DA82F  call 00598100               ; destroy
001DA83F  jne  001DA810               ; next token
```

*Construction is the whole operation.* Resolving with selector 5 takes a branch in §5's lookup that
bumps a counter and stamps the entry rather than delivering bytes - so **a prefetch token is a
resolve-and-mark, not a read**, which is what "handed to the file cache" was standing in for.

## 4. The resolver, and what it logs

`0059EE90` is the routine the constructor and slot 3 both call. A raw `rel32` index over the image
gives it **six** call sites: **five inside the stream family** - three constructors, including the
`0x30`-byte context constructor and this class's own, each writing the same `-1` / `0` field
pattern, and two rebinds, one of them slot 3 - and **one from the Audio layer**. *None of the six is
locale-specific.* **So it is not the language/locale init**, as one update row on
[language selection](../../19-Save-Load-Settings/Language-And-Locale/language-selection-and-locale-ids.md)
has it - that row's size, call list and anchor are all correct, only the name is wrong, and it is
reachable from locale code because locale code opens files. Filed as
`FABLE-CONTRA-0059EE90-IS-NOT-THE-LOCALE-INIT`.

**Its own strings name it.** Three authored tags live in `.rdata` beside it:

```
00D27930   "[FFXII_data] %s \n"
00D27910   "[FFXII_data_notcache] %s \n"
00D27948   "[FFXII_ERROR] Big file open failed %s \n"
```

and the logging rule is a three-way test on the selector: **selectors 3, 4 and 5 log nothing**;
**selector 0 logs `[FFXII_data]`**; **anything else logs `[FFXII_data_notcache]`**.

## 5. Route 1 - an uppercased key and a 31-bit multiplicative hash

Taken when the resolver's gates pass. `001D6D20` fetches a manager and calls `0020C1B0`, which
builds a key, hashes it, and searches a tree:

1. **`0020C440` builds the key.** It copies the path, then **skips leading non-alphanumerics** -
   the loop advances while the character is neither `a`-`z` nor, by a 64-bit mask test, `0`-`9` or
   `A`-`Z` - so a leading `.\` or drive prefix is dropped and the key starts at the first
   alphanumeric. It then converts `/` to `\`, copies through **CRT `toupper`** while **collapsing
   doubled backslashes**, and strips **trailing spaces**.
2. **The hash is the 33-multiplicative path hash** already published in full on
   [`ta-texture-animation-lists.md`](../Prefetch-And-Json-Data/ta-texture-animation-lists.md) -
   seed `0x1505`, `hash*33 + (signed char)c`, finished by clearing bit 31. *That page derived it;
   this one only records that the same hash keys this index.*
3. **The lookup is a tree** rooted at the manager's `+0x38` against a sentinel at `+0x28`, comparing
   a `u32` at each node's `+0x20`, under the manager's own lock at `+0x58`. *(Anchors, 2026-09-30, SWE2-CONTRACT,
   `b8` A1: the lock `+0x58` is taken at `0020C230` / `0020C23C` and released at `0020C2B3` / `0020C2C1`; the root
   `+0x38` is read at `0020C242`, the sentinel `+0x28` at `0020C246`, and the node key `+0x20` compared at
   `0020C255`.)*

## 6. Route 2 - a lowercased key and MD5

Taken when the gates fail. The path is normalized **twice and differently**: leading `.`, `/` and
`\` are skipped, `\` becomes **`/`**, and the result is **lowercased**. Then:

- **`CryptCreateHash` with `ALG_ID 0x8003` - `CALG_MD5`**, `CryptHashData` over the normalized path,
  `CryptGetHashParam` with `HP_HASHVAL` into a **sixteen-byte** buffer. All three resolved from the
  import directory.
- The sixteen bytes are carried as **two quadwords** and looked up in each mounted package's own
  **red-black tree keyed on the 128-bit digest** (`001F47D0` compares `+0x18` then `+0x20`).
- **On failure the resolver logs `[FFXII_ERROR] Big file open failed` and returns 10**; success
  returns 0.

That error tag is the engine's own word for the archive
[the BigFile index page](how-the-bigfile-index-loads-and-is-verified.md) reads - `FFXII_TZA.vbf`,
whose index is itself MD5-verified. **So route 2 is the package lookup.**

## 7. The asymmetry is the point

| | route 1 | route 2 |
|---|---|---|
| separator | `\` | `/` |
| case | **upper**, via CRT `toupper` | **lower**, inline `+0x20` on `A`-`Z` |
| leading text | skipped to the first alphanumeric | leading `.`, `/`, `\` skipped |
| extra normalization | doubled `\` collapsed, trailing spaces stripped | none |
| hash | 33-multiplicative, 31 bits | **MD5**, 128 bits |
| container | one tree on a `u32` | per-package tree on the digest |

**Two lookups, two conventions, opposite in both separator and case.** This also answers the second
open question on the prefetch page - *"where case-insensitive path lookup happens; the engine's
literals are capitalised and the archive's are not"*: **it happens in these two key builders, at
lookup time**, and they disagree on direction. A reimplementation that picks one convention for both
will miss in one of them.

## 7a. Who else reaches this interface

The stream reader is not a Resource-layer-only facility, and two crossings are worth naming so a
reader is not surprised by them:

- **the Audio layer** reaches the resolver directly, through a body that builds a stream context
  rather than a full reader;
- **the Input layer** constructs, tests and closes a reader of its own - constructor, `IsOpen` and
  the base destructor in one body.

*Both are named by layer and role deliberately.* Naming the far-end functions by address would pull
their own callers' layers onto this page, and neither body is read here. *(2026-09-30, SWE2-CONTRACT: the two
bodies are the Audio body `00225BA0`, one of the resolver's six callers, and the Input body `0079FB10`, which calls
`00597970`, `0059D920` and `00598100` (`b8` B1). The pass-22 section below names them too; they are still not read
here.)*

## 8. What this page does not claim

- **Which route serves loose files.** No `CreateFile` appears anywhere in the chain as read. Either
  loose-file support lives below the package entry or this resolver only ever serves packaged
  content; the bodies that would settle it are not read here.
  ***Answered 2026-09-27 (FABLE, Claude Opus 5.5): neither route serves a loose file.** The resolver stores a source in only `+0x20` (route 1) and `+0x10` (route 2), never the `+8` handle; route 2's five package slots are filled only by `0019B070`, whose one call site (`0017CEF6`) mounts `../FFXII_TZA.vbf`; and the image's only `CreateFile*` import, `CreateFileA`, is used by two minidump writers (`005CCAB0`, `0079B1E0`). [Record](../../_index/candidates/pc1-config-route/README.md).*
- **What route 1's manager is.** Its own console-facing label is *resource*, and the prefetch system
  names a `FileCachePrefetchManager` while these log tags read `[FFXII_data]` and
  `[FFXII_data_notcache]`. *That correspondence is suggestive and is deliberately left as a
  hypothesis* - nothing here traces a prefetched token into this tree.
  ***Answered 2026-09-27 (FABLE, Claude Opus 5.5): route 1 is a RAM file cache.** Its enable byte `01F83440` has one writer, `0020C610`, which sizes a budget at `01F83448` from `GlobalMemoryStatusEx` (total physical memory / 3, clamped to 32 MB-4 GB) and sets the byte to 1; the cache is filled by route 2's own hits through `0059A9B0` (`0059F1B7`). Whether the prefetch manager is its front end stays a hypothesis. [Record](../../_index/candidates/pc1-config-route/README.md).*
  ***Placed 2026-09-30 (SWE2-CONTRACT, DD batch 8): the prefetch loop is one client of route 1, not its front end.**
  Route 1 is tried by every open whose selector is not 0 (S3 below), which covers 15 of the 20 sites in §3's census.
  The prefetch token loop (`001DA810`) is the one site that passes 5. So the RAM cache is the general cache, and a
  prefetch token is one way of stamping an entry in it.*
- ~~**What the selector values mean** beyond which branch and which log tag they select.~~ ***Answered 2026-09-30
  (SWE2-CONTRACT, DD batch 8), from the resolver `0059EE90` read whole (`b8` S1–S5):** the selector byte `+0x18`
  decides three things.
  - **The log line.** Selectors 3–5 log nothing, 0 logs `[FFXII_data]` and any other value logs
    `[FFXII_data_notcache]` (`0059EEFB`–`0059EF10`).
  - **Whether route 1 is tried.** Selector 0 never tries it (`0059EF38`). Any other selector tries it when the cache
    is enabled, the resolver's own flag argument is set and the name passes the extension tests below. Route 1 also
    receives the selector (`0059EFD2` → `001D6D20` → `0020C1B0`'s `r8d`).
  - **Whether a route-2 hit is copied into the cache** (`0059A9B0` at `0059F1B7`). The copy is armed only on the path
    that tried route 1 and missed. There, if `001D6B90()` returns zero or the selector is 5, it is armed when
    `001D6B70()` is positive **or the selector is not 1** (`0059EFAB`–`0059EFCE`). Otherwise it is not armed.
    - **So selector 1 is the one value that does not fill the cache on a miss** (unless `001D6B70`'s flag is set),
      which is what its `notcache` log tag says.
    - Selector 0 is a plain archive read that bypasses the cache.
    - 3–5 are silent and cacheable.
  - **The resolver can force 5 itself** (`0059EEF1`). With the cache enabled, it does so when `00865390(path)` is true.
    That predicate (`001DB050`) matches a path beginning `PS2Data\obj_finish\in\chara\c10\<name>\` for four names,
    `c1004`, `c1005`, `c1006` and `c1019`. These four character folders are always resolved as selector 5.
  - **The two helpers** (`b8` S6):
    - `001D6B90` returns the cache's low-memory byte `01F83441`. The budget setter `0020C610` sets it to 1 when
      total physical memory is under 1 GiB (`0020C674`) or the budget is clamped to its 32 MB floor (`0020C684`).
    - `001D6B70` returns byte `+0x88` of the FileCache singleton `[01F82CF0]`, which
      [the game-settings page](../../19-Save-Load-Settings/Game-Settings-Config/game-settings-ini-and-runtime-config.md)
      names the "map jump pending" byte.
    - So on an ordinary machine a miss is cached unless the selector is 1 and no map jump is pending.
    - In low-memory mode only selector-5 opens are cached.
- ~~**Whether `+0x20` is a nested member or a base sub-object.**~~ *Answered 2026-09-25/27 (OPUS, f96ae6a4c; applied here 2026-09-27 (FABLE, Claude Opus 5.5)): a **base**. `PStreamReaderFile`'s RTTI base-class array puts `PStreamFile` and `PStreamFileWin32` at `mdisp 0x20` (non-virtual), `PStreamReader`/`PStream` at 0 and `PMemoryBase` at 8; `00597930` installs no vtable, so the base is non-polymorphic. [Record](../../_index/candidates/pstreamreaderfile-base-0x20/README.md).* The original item: A 0x30-byte standalone constructor
  `00597930` writes the same six fields at the same relative offsets, which is why the fields are
  given here as offsets from the stream object. Deciding member-versus-base is an object-layout
  question and is routed to OPUS-STRUCTURAL rather than guessed.
- ~~**Where the UTF-16 buffer goes.** Route 2 widens its first normalized path with `00599250` and the
  consumer of that buffer was not found.~~ ***Answered 2026-09-30 (SWE2-CONTRACT, DD batch 8, `b8` U1): nowhere. The
  widened copy has no consumer.**
  - `00599250` is a UTF-8 to UTF-16 converter (it tests the surrogate range at `005992E2`). It writes into the stack
    buffer whose address is passed in `rdx` (`0059F0DD`), and nothing else keeps that address.
  - Its return value is overwritten at `0059F0EF`.
  - After the call, the only instructions that form an address from `rsp` are the next stack allocation (`0059F104`),
    the new key buffer (`0059F107`) and the epilogue.
  - The MD5 key is built afresh from the caller's original path. So the first normalized copy (backslashes,
    lowercase) and its UTF-16 widening are computed and dropped: inert work in the shipped build.

### A control worth stating, and its limit

The resolver rejects a path before route 1 if its name has a dot four or five characters from the
end *(qualified 2026-09-27, FABLE: the bytes carry nine single-character tests on the last five characters, `0059EF4B`-`0059EFA9` - the dot at -4 or -5, but also `m`, `a`, `b` at -3..-1 and `w`, `e`, `b`, `m` at -4..-1, any match sending the path to route 2; the prediction below holds under either reading)* - an OR of character tests whose opcodes were checked in raw bytes, not taken from a
disassembler's rendering. Against the shipped file tree that predicts `.phyre`, by far the most
common asset extension, reaches route 1 while three- and four-character extensions do not. **The
limit: that tree is extracted content, so it shows which names exist, not which route serves them
at runtime.**

## Key addresses (SWE2-CONTRACT, 2026-09-30)

| address | role | section |
|---|---|---|
| `00D26C60` / `00D26C90` | `PStream` / `PStreamReaderFile` vtables | §1 |
| `00597970` | the reader's constructor (selector in `r8b`) | §1, §3 |
| `00597930` | the `0x30`-byte stream-context constructor (selector in `r9b`) | §3, §8 |
| `0059D920` / `0059D4B0` / `0059BD40` | `IsOpen` / `Read` / `Close` (slots 2, 5, 1) | §2 |
| `0059EE90` | the resolver: selector rules, both routes, the error tag | §4, §8 |
| `00865390` → `001DB050` | the four-folder predicate that forces selector 5 | §8 |
| `001D6D20` → `0020C1B0` | route 1: the RAM-cache lookup, lock `+0x58`, tree `+0x38` / `+0x28` | §5 |
| `0020C440` / `00674A00` | route 1's key builder and its 33-multiplicative hash | §5 |
| `0019AEE0` / `001F47D0` | route 2: MD5 of the lowercased key and the digest-tree compare | §6 |
| `0059A9B0` | copies a route-2 hit into the RAM cache | §8 |
| `00599250` | UTF-8 to UTF-16 conversion whose output nothing reads | §8 |
| `001DA810` | the prefetch token loop (selector 5, construct and close) | §3 |

## Modding notes (SWE2-CONTRACT, 2026-09-30)

A replacement asset has to be reachable through route 2, because neither route opens a loose file (§8). In practice
that means an entry in `FFXII_TZA.vbf` under the MD5 of its lowercased, forward-slash path. Route 1 is a RAM cache filled from route
2's hits during a run (`0059A9B0`), so it adds no second place a file could be replaced.
Anything that hooks file access, such as a loader, has to act at or above this resolver.

## Evidence (SWE2-CONTRACT, 2026-09-30)

| claim | evidence | tier |
|---|---|---|
| The class and its seven slots | RTTI locator behind `00D26C90`; the slot bodies read (§1–§2); falsification R0–R2 | 1 (static) |
| The selector census and the prefetch loop | whole-image call index; falsification R3–R4 (`falsify_path_resolve.py`) | 1 (static) |
| The six resolver callers and the three tags | falsification R5–R6 | 1 (static) |
| Route 1's key, hash and tree | `0020C1B0` / `0020C440` / `00674A00`; falsification R7; `b8` A1 | 1 (static) |
| Route 2's MD5 and digest tree | `0019AEE0` / `001F47D0`, the `CryptCreateHash` imports; falsification R8 | 1 (static) |
| The selector's three effects, the forced 5 and the two helpers | `0059EE90` read whole; `b8` S1–S6 | 1 (static) |
| The UTF-16 copy is unread | `b8` U1 | 1 (static) |
| No loose-file route; route 1 is a RAM cache | FABLE's `pc1-config-route` record | 1 (static) |
| `.phyre` reaches route 1 while short extensions do not | the name tests against the extracted file tree (§8 control) | 9 (authored data), names only |

## Falsification pass 1 — 2026-09-29 (OPUS): the "selector 24" row refuted; everything else survives

**Attack.** Every structural clause of §1-§6 became a check that fails if the shipping image says otherwise. The checks decode
every listed body in `.text`, so the call-site counts and the census are whole-image. Script:
`Tools/analysis-kit/gfz-scripts/falsify_path_resolve.py`, output `falsify_path_resolve.out`, image `73461d08…`, 0 BROKEN.

| # | Clause attacked | Killer | Result |
|---|---|---|---|
| R0 | §1 the two vtables and seven slots | another body in a slot | **survives** |
| R1 | §2 `IsOpen` | another size or test | **survives**: 27 B, false only when `+0x28 == -1`, `+0x30 == 0` and `+0x40 == -1` |
| R2 | §2a the ownership bit at three sites | a site without the bit test | **survives**: slot 3, slot 4, and the base destructor `00598100` |
| R3 | §3 the selector census | a value other than the table's | **REFUTED for one row** (below) |
| R4 | §3 the prefetch token loop | a read in the loop | **survives**: `mov r8b, 5`, construct, `0059BD40`, `00598100`, next |
| R5 | §4 six callers of `0059EE90` | another count or layer | **survives**: five Resource bodies (`00597930`, `00597970`, `00597A70`, `0059ED70`, `0059EE10`) and the Audio body `00225BA0` |
| R6 | §4 the three tags | another string or no reference | **survives**: all three at the cited addresses, all referenced by `0059EE90` |
| R7 | §5 route 1's key and hash | another seed or finish | **survives, made exact**: `0020C1B0` builds the key with `0020C440` and hashes it with `00674A00`: `mov eax, 0x1505`, `imul eax, eax, 0x21` plus the `movsx` char, `btr eax, 0x1f` |
| R8 | §6 route 2's MD5 and tree | another `ALG_ID` or comparison | **survives, made exact**: the MD5 is in `0019AEE0`, which the resolver calls and which is the only caller of `001F47D0` (`+0x18`, then `+0x20`); failure returns 10 |

* **R3: the one computed selector is 3 or 4, not 24.** The site is `001DAFD8` in `001DADC0`, with `lea r8d, [r14 + 3]`. In
  that body `r14b` has two writes: `xor r14b, r14b` (`001DAEA2`) and `mov r14b, 1` (`001DAFB5`). A reachability walk from
  the entry finds no path to the `lea` that avoids both. The constructor keeps the selector as a byte, so this site passes
  **3 or 4**, and by §4's rule it logs nothing either way.
  [The prefetch page](../Prefetch-And-Json-Data/how-the-prefetch-manifests-are-read.md) already says "3 or 4". The other
  rows hold: `0` × 5, `5` × 1, and `1` × 13, which is 11 sites of `00597970` plus the two of `00597930`, which takes its
  selector in `r9b`. `CON-165`.

Consumer record: [`_index/candidates/path-resolve-falsification-pass-1-0929/`](../../_index/candidates/path-resolve-falsification-pass-1-0929/README.md).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Audio — CLIENT (1 edge).** 1 inbound (Audio bodies `00225BA0` call page-cited `0059EE90`). Substantive edges include `0059EE90` is called by `00225BA0`.
- **Input — CLIENT (3 edges).** 3 inbound (Input bodies `0079FB10` call page-cited `00597970`, `00598100`, `0059D920`). Substantive edges include `00597970` is called by `0079FB10`; `00598100` is called by `0079FB10`; `0059D920` is called by `0079FB10`.
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `001DADC0` call Platform bodies `005CC930`).
