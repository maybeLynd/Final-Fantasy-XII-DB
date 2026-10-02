---
system: Authored reference lifetime and resource allocation evidence
category: 02-Resource-And-Asset-Pipeline
status: "DOCUMENTED — evidence note for the ownership-to-disposal page; its residue is consolidated under Limits (2026-09-30, SWE2-CONTRACT, DD batch 7; brought current 2026-10-01, DD batch 18, items 17–23): each item is answered by a cited record or check, owned by a named page, or carried by a closed register row (SD-164, SD-165 and SD-166 ANSWERED; J-C, CD-2, BW-2 and OV-24 SUPERSEDED; OV-27 and OV-28 NOT A QUESTION); the base's live read is ASTRA's carrier OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME, and SECTION-06 package acceptance is a class-2 process item carried by board request SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930 (owner re-status 2026-10-01, OPUS)."
note_kind: evidence
parent: the-resource-owner-from-copy-or-borrow-to-disposal.md
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 261 addresses cited - 24 data,
    148 entry, 86 interior, 1 literal, 2 text-data, every one resolving into a known section
    of the authority image; both .text gap citations (004422E0, 004424B4) are adjudicated
    TABLE in _index/candidates/text-gap-citations-250.tsv. This document had no
    verified_against block at all; the line records a check performed on that date and is not
    a reconstruction of the original derivation, for which see `audit.last_pass_state`.
last_reviewed: 2026-09-12
audit:
  passes: 1
  last_pass: 2026-09-12
  last_pass_state: opus-authored-reference-lifetime-evidence-pass-1
external_production:
  section: SECTION-06
  date: 2026-09-22
  status: "locally validated; formal independent acceptance pending (a class-2 process item, carried by board request SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930, 2026-09-30)"
  evidence: _experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md
---

# Resource allocation, pointer width and the decoder base

> **Current production, SECTION-06 (2026-09-22):** [ownership-to-disposal mechanism](the-resource-owner-from-copy-or-borrow-to-disposal.md) and [review](../_experiments/evidence/continuation-section06-resource-lifetime/REVIEW.md). Sections 13–19 below remain the earlier static evidence; blanket execution-absence statements there are historical at the specifically tested boundary. No old peer receipt certifies the new work.

**The resource loader has an arena allocation layer. Its prefix-label helper was
misidentified as a release. Neither the import census nor a zero-base snapshot
establishes a lifetime address guarantee.** These are separate conclusions.

This is ASTRA's bounded primary-evidence review for J-C, CD-2 and BW-2. It records
static code and PE import evidence, plus the scope of existing observations.
No game process was accessed. The initial review added no original-code execution;
the later backing-path follow-up in sections 7–8 adds the explicitly bounded
initializer controls of EXP-077. [EXP-076](../_experiments/EXP-076-reward-decoder-composition.md) separately
executes the decoder with the installer in synthetic initialized states.

## Scope (SWE2-CONTRACT, 2026-09-30)

This is an **evidence note** (NOTE template, `note_kind: evidence`). It carries the primary evidence behind two pages:
- its parent, [who owns a resource and what can invalidate its pointers](the-resource-owner-from-copy-or-borrow-to-disposal.md);
- the arena system page, [where the game's memory comes from](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md).

It began as ASTRA's bounded review for register rows J-C, CD-2 and BW-2. All three have since closed SUPERSEDED onto
their static answers. The review was then extended one lifetime boundary at a time (sections 7–19) and tied to
SECTION-06's composed execution (section 20).

What it establishes, in outline:
- the resource allocation layer (arenas, blocks, headers, handles, the membership tree and the free routine);
- the decoder base and the 32-bit width constraints that follow from it;
- where arena backing comes from and where it was observed;
- how an effect file's input is copied or borrowed, relocated and torn down.

What it leaves to the pages it serves:
- the current ownership model (who owns a copy, who borrows it, the teardown order and the refresh a move needs) is on
  the parent, with its interface in [the ownership contract](CONTRACT-resource-input-ownership.md);
- the allocator's full field map and failure paths are on the arena page;
- the player view, call chain, key-address table and modding notes are not repeated here.

Sections 1–20 below are kept as written, in the order they were established. Earlier conclusions stay visible as dated
history. The **Limits** section at the end says what each "remains open" line in them now points to.

## Findings (SWE2-CONTRACT, 2026-09-30)

A digest of what sections 2–20 establish, each with its anchor. Hex throughout.

1. **The prefix helper tags, it does not release (§2).** `0036C660`'s only call is `0036C690`, through IAT `008C2F70`,
   which is `strncpy`. On a block with magic `FF12` and its allocated bit set, it writes seven name bytes at payload
   `-0C` and a 16-bit tag at `-22`.
2. **The resource path suballocates arena blocks (§3).** `0036A100` and `0036A1A0` reach `0036BC60`, which walks the
   record at `022D7FD0 + id * A8` (ids 0–14). It rounds to 64 bytes, splits with a `40`-byte header and returns block
   `+40`. A failure goes to the retry allocator `0036BFE0`.
3. **The decoder base is zero at load, and only its two converters name it (§4 and "The 01F83530 blind spot, closed").**
   The reads are `0020E602` and `0020E620`. No `lea` or data word points to `01F83530`. This is CD-2's static answer.
4. **Nine boot arenas are CRT blocks with no address check (§7).** Arenas 2–9 and 11 come from
   `0036D240` → `0085E730` → IAT `008C2B40` (`malloc`). No NULL or ceiling test runs before `00369D30`. Four more
   initializer callers build arenas 12–14 and replace arena 11's backing.
5. **The initializer keeps a full-width backing; block links do not (§8–9).** EXP-077 returns exact 64-bit pointers.
   Under EXP-078, with backing at `100010000`, the second allocation faults at `0036CA8A` (direction 0) and `0036CA75`
   (direction 1), because neighbour links are 32-bit.
6. **The selector map is identity-filled by exactly two writers (§10).** The initializer's first-use fill and the reset
   `0036A280` write `022D89A8`. The byte stack at `022D8DD0` (depth `022D89C8`) is a separate settings stack.
7. **Observed placement (§11).** In one live process at the title and after a load, every enabled backing sat below
   2 GiB and the base read zero (EXP-079). Arena 7 was enabled, but its header pointers designated zeroed bytes.
8. **Handles narrow the slot address (§12).** Handle issue `0036AF20` returns a 32-bit slot address with tag 3
   (`0036B018` / `0036B01B`). The unlinker `0036C9D0` stores the successor's `+0C` at `0036CA75` and the predecessor's
   `+10` at `0036CA8A`.
9. **Arena 7's backing is a resource destination (§13).** The boot backing, stored at `01FD4A30` by `0022A240`, is
   passed directly as a request destination by `003B0660`, `002FC860`, `003B2310` and `002FC4A0`. `0032E870` stores
   it at request `+38` / `+70`.
10. **An effect context borrows instead of copying when template byte `+2` mask `04` is set (§14, §16).** The tests
    are `003EE018` and `003EE117`. Of the context constructor's six direct callers, only the EFB wrapper `0026FB90`
    and the type-3 constructor `003B38B0` set the bit.
11. **Relocation repairs with a signed 32-bit delta and publishes the base last (§15).** The delta is formed at
    `0024D984` and the base written at `0024D9A7`. A 4-GiB move repairs nothing: the third controlled case.
12. **A mode-0 entry copies into arena-6 storage through a 32-bit destination (§17).** The destination is formed at
    `0051EFF2`–`0051EFF8`, and the copy is `memcpy` through `00861EBA`.
13. **Membership is a binary tree, and teardown disposes consumers first (§18).** The tree is rooted at arena `+50`
    and keyed by signed payload length (`0036B50D`). Entry removal runs `003B37E0` (context disposal) before
    `00409730` → `0051EE80` → `003AB7C0` (source release).
14. **Render cleanup is not reclamation; the free routine gates on the header (§19).** `00427B00` only clears render
    references. `00369860` refuses a block whose magic is not `FF12` or whose word `+3E` is nonzero.
15. **The composed chain (§20).** SECTION-06 runs the original functions together over synthetic arenas:
    - a mode-0 entry owns its copy, and a type-3 context borrows it;
    - removal destroys consumers before freeing the copy;
    - the context run origin `+870` stays stale after a move.

## Evidence (SWE2-CONTRACT, 2026-09-30)

Receipts are under `../_experiments/evidence/` unless named otherwise. A tier cell gives the tier and the method, as
EVIDENCE-STANDARD's 2026-09-13 addendum requires.

| claim | evidence | tier |
|---|---|---|
| Finding 1: the prefix tagger | §2; `authored-reference-lifetime-review/primary.json` (complete bodies, import walk, two predicate controls) | 1 (static) |
| Finding 2: arena suballocation | §3; the same receipt, `0036BC60` read whole (887 B) | 1 (static) |
| Finding 3: base zero at load, two readers | §4 and the closed-blind-spot section (FABLE's whole-image census, 2026-09-16 and 2026-09-18) | 1 (static) |
| Finding 3: base zero at the title screen | EXP-002, one instant | 10 (live) |
| Finding 4: CRT backing, no guard | §7; `resource-arena-backing/primary.json` (13 complete bodies) | 1 (static) |
| Finding 5: full-width init, 32-bit links | §8–9; EXP-077 (six controls, truncation mutant caught), EXP-078 (seven predictions) | 1 (isolated original-code) |
| Finding 6: two map writers | §10; `arena-selector-static/primary.json`; `b7_lifetime.py` M1 (below) | 1 (static) |
| Finding 7: placement below 2 GiB, arena 7 zeroed | §11; EXP-079 (two states, two samples each) | 10 (live) |
| Finding 8: narrowed handles, unlink stores | §12; `arena-handle-static/primary.json` (5 bodies) | 1 (static) |
| Finding 9: arena 7 as a destination | §13; `arena7-backing-use/` (consumers, queue, destination) | 1 (static) |
| Finding 10: borrow flag and its setters | §14, §16; `efx-input-lifetime-flag/`, `efx-source-initialization/` | 1 (static) |
| Finding 11: signed 32-bit repair | §15; `efx-rebase-primary/` (probe, result, execution review; 15 runs) | 1 (isolated original-code) |
| Finding 12: 32-bit memcpy destination | §17; `resource-entry-source-ownership/` (11 bodies) | 1 (static) |
| Finding 13: tree and teardown order | §18; `resource-entry-release-lists/` (13 bodies) | 1 (static) |
| Finding 14: cleanup vs reclamation | §19; `resource-native-reclamation/` | 1 (static) |
| Finding 15: the composed chain | §20; `continuation-section06-resource-lifetime/REVIEW.md` (171 assertions, ten mutants) | 1 (isolated original-code) |
| The answers the Limits section cites | [`b7_lifetime.py`](../_index/candidates/swe2contract-ddres-b7-0930/b7_lifetime.py) D1, M1, S1, E1, G1, R1, A1, FAILS 0 | 1 (static) |

## 1. Method — reference identity and receipts (heading renamed by SWE2-CONTRACT, 2026-09-30)

The reference EXE is SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`,
image base `00120000`. The [primary receipt](../_experiments/evidence/authored-reference-lifetime-review/primary.json)
contains the bytes of every decoded instruction, complete-body hashes and lengths,
PE section bounds, selected import identities, and two scanner-predicate controls.
The [collector](../_experiments/evidence/authored-reference-lifetime-review/collect.py)
adapts the existing `iat_xrefs.py` import walk and exact-body disassembly; it
does not build a new runtime instrument.

All fourteen captured bodies decoded to their complete listed length. Their
machine instructions were read, including the branches and caller arguments.
The import walk finds 538 symbols in 30 DLLs, no direct `VirtualAlloc` import,
and an empty delay-import directory. These are facts about this EXE's imports;
they are not a transitive inventory of allocation mechanisms.

**Method across the later sections (SWE2-CONTRACT, 2026-09-30).** Every section reads the same certified image, and
each receipt records the body hashes and lengths it read.

- **Three methods, kept apart.**
  - **A, static:** complete bodies decoded and read. This covers §2–§4, §7, §10, §12–§14 and §16–§19.
  - **B, isolated original-code execution:** EXP-077 and EXP-078 (§8–§9), §15's Unicorn probe and SECTION-06 (§20).
  - **C, live read-only observation:** EXP-079 (§11), plus the recovered EXP-002 result (§4).
- **Positive controls, each showing the instrument sees what it counts.**
  - §4: the operand predicate admits the decoder read `0020E602` and excludes the binder store `003845F4`.
  - §10: the scanner misses the known indexed read `0036C272`. This control is kept as a blind spot.
  - §13: the boot store and the initializer read are among the RIP candidates.
  - §16: the displacement scan misses the three stack-template stores, another kept blind spot.
  - EXP-077: a private truncation mutant is caught.
  - §15: a receipt copy with one table write removed fails the memory review.
- **Extent.** A function called "complete" was decoded to its full listed length. The exceptions are stated where they
  occur:
  - the eight step bodies of §14, read to their heads here;
  - the list handlers `00501420` / `00503F10` of §15;
  - every callee named as a call boundary.
- **This regrouping's checker.** It is
  [`b7_lifetime.py`](../_index/candidates/swe2contract-ddres-b7-0930/b7_lifetime.py), run with `python -B
  b7_lifetime.py` from its folder over `retool.py`'s extents. Its output is `b7_lifetime.out`, FAILS 0.

## 2. `0036C660` writes prefix metadata

The full 82-byte function has one call, at `0036C690`. Its RIP operand resolves
to IAT slot `008C2F70`, whose PE import is
`api-ms-win-crt-string-l1-1-0.dll!strncpy`. As a positive import-resolution
comparison, the allocator thunk `0085E730` resolves to `008C2B40`, which names
`api-ms-win-crt-heap-l1-1-0.dll!malloc`. The existing graph's edge from
`0036C660` also names `strncpy`; the conclusion does not rely on that graph.

For readable prefix storage and a valid source string on the taken path, the
function's behavior is:

```text
annotate(p, source, tag):
    if p != 0 and u16[p - 0x40] == 0xFF12 and (u8[p - 0x2C] & 1):
        strncpy(p - 0x0C, source, 7)
        u8 [p - 0x05] = 0
        u16[p - 0x02] = 0
        u16[p - 0x22] = low16(tag)
    return p
```

The seven-byte copy occupies `p-0x0C` through `p-0x06`; the explicit byte at
`p-0x05` terminates it. A short source is padded by the imported operation.
This external meaning follows the identified import and Microsoft's
[`strncpy` specification](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/strncpy-strncpy-l-wcsncpy-wcsncpy-l-mbsncpy-mbsncpy-l?view=msvc-170);
the CRT body was not executed here.

Two callers establish the distinction between allocation and annotation:

| Caller | Allocation | Annotation and subsequent use |
|---|---|---|
| `ActorResource_BeginPrimaryPayloadLoad`, `00330310` | Size from `0032E400`; call `0036A100` at `0033039C` | `003303AD` passes the returned pointer, a source basename and tag `0x95C`; the same pointer is then stored and supplied as the read destination |
| Loader registration `00384420` | Call `0036A190` at `00384479` | If the pointer is nonzero, `0038448F` passes it with the caller's name and loader id; the read request receives that allocation |

The first caller's source literal at `00D10958` is
`..\..\katano\atelload.c`. `0036C750` walks backward to the final slash, so this
case labels the allocation with the first seven bytes of `atelload.c`.
The tag resembles a source line in this caller and is a loader id in the
other; **a universal “line number” name for the field is not established**. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered: the field is a free-form 16-bit caller tag that no code reads for its value; see Limits item 17.)*

The EBP page's “release/free” interpretation is contradicted by the import,
arguments, stores and continued pointer use. This function neither allocates
nor calls a deallocator in the captured body.

## 3. The actual resource path suballocates arena blocks

`0036A100` calls `0036BC60` with the selected arena id from `022D89BC`,
the requested size, no supplied block, and direction 0. A null result invokes
`0036BFE0`. `0036A190` forwards to `0036A1A0`, whose first attempt uses direction
1; its failure path also reaches `0036BFE0`.

The full 887-byte `0036BC60` body supplies direct evidence of an arena layer:

- It selects a record at `022D7FD0 + id * 0xA8`, with supported ids `0..14`.
  The enabled-id mask is read from `022D89B8`.
- For ordinary nonnegative sizes without arithmetic overflow, it rounds the
  request to a multiple of 64. The exact instructions use signed 32-bit
  arithmetic; overflow behavior is not replaced here with an unlimited formula.
- With no supplied block, it walks from record `+0x90` or `+0x98`, tests
  block size `+0x18`, and follows encoded 32-bit links at block `+8` or `+4`
  through the original decoder.
- It computes an allocation and possible remainder within the selected block.
  The split subtracts the requested size and a `0x40` header. It updates the
  record's free-list ends and calls the block/list helpers.
- On the successful path it returns the chosen block address plus `0x40`.
  The prefix bit subsequently tested by `0036C660` is set by
  `0036BE7E` at block `+0x14`, which is payload `-0x2C`.

This establishes suballocation from linked blocks. The initial review did **not**
establish how those blocks were acquired; section 7 now follows the backing
provider for the known callers. The helpers that maintain every link have not
all been read in this package.

`0036BFE0` reads an arena callback at record `+0xA0`, invokes it if present,
runs possible reclamation helpers when record `+0x50` is nonzero, and retries
`0036BC60`. It contains explicit self-loops for disabled-state conditions and
a retry loop; a blanket “failed allocation immediately returns NULL” contract
would omit these paths. Callback side effects and liveness remain unproved. *(2026-09-30, SWE2-CONTRACT: see Limits item 6.)*

The CRT path is distinct: `00210EC0` tail-jumps through `0085E730` to the
imported `malloc`. Its existence does not erase the resource arena path.
The upstream question of whether CRT allocation supplies these arenas is answered
for nine boot arenas in section 7; their actual address placement remains open. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: placement was observed below 2 GiB at the title and after a load (§11, EXP-079); other states are Limits item 2.)*

## 4. What the decoder evidence proves

`0020E600` computes `uint64(base + uint32(reference))`, reading the qword
at `01F83530`. `0020E620` computes the low 32 bits of the input minus the
low 32 bits of that base. Neither operation validates storage. At base zero,
the decoder is an identity **on the unsigned 32-bit reference domain**.
EXP-076 preserves the distinction between that result and later 32-bit row
arithmetic; a decoded nonzero value can still become a stored NULL pointer.

The PE section bounds place the base in the zero-filled tail of `.data`.
That establishes its image-initialized value, not an invariant over execution.
The reviewed FABLE `ripscan.py` restricts its operands to RIP-relative memory
references in listed function bodies and tests the target's starting address.
It does not propagate aliases, evaluate indexed addresses, or prove the absence
of writes through pointers and bulk operations.

The receipt applies that existing operand predicate to two original
instructions: decoder read `0020E602` is admitted; binder store
`003845F4: mov qword ptr [rcx], rdx` is excluded. This confirms the blind spot
already recorded by the authored-table contract. No new whole-image census
was run. A missing nearby `lea` increases confidence but does not supply the
missing alias/range proof. **No writer to `01F83530` was discovered by this
review; a nonzero shipped value is not being asserted.**


**Whole-image census 2026-09-18 (FABLE): no instruction of any form names `01F83530`, and no data pointer to it exists.** *(Scope corrected 2026-09-25, FABLE, Claude Opus 5.5: `01F83530` is **zero at image load**, because it lies past `.data`'s file-backed extent. That is separate from whether later code can write it, and one in-image store route can. The texture-id table writer `00210570`, reached through GiSetTexture's execute, bounds its id only from above with a signed compare, so id `0xFFFB` stores a pointer into `01F83530`. That was replayed on the unmodified bytes. The id producers read keep ids below `0x4000` at the shipped frame width, so the route is **undriven, not absent**. "Zero for the process's life" is supported, not proven. See [the row-lookup contract](CONTRACT-authored-table-row-lookup.md) §7, the reconciliation.)* *This census counts instructions that NAME the base. It is not a no-writer fact.* Every instruction in `.text` was decoded: the only rip-relative references into `01F83500`..`01F83538` are the decoder read (`0020E602`, `add`), the encoder read (`0020E620`, `sub`) and two unrelated loads at `008A737B` / `008A738D` (`01F83520`, `01F83518`); there is no `lea` of any address in that window, no `mov` immediate naming `01F8350x`..`01F8353x`, no base-plus-displacement form carrying the displacement `0x1E63530`, and no qword or aligned dword equal to `01F83530` in any data section. A write through a pointer needs the pointer formed by a `lea`, an immediate or a data cell, and none exists, so the only remaining route would be an address computed from an unrelated base, which the sweep cannot rule out but for which no evidence exists. The base is zero-initialised `.data` and reads zero at the title screen (EXP-002); the two functions are therefore truncation and zero-extension in every shipped path. The nine boot arenas' placement follows from the same reading: their memory is CRT heap (no `VirtualAlloc`, `HeapAlloc` or `MapViewOfFile` import) in a large-address-aware process without `DYNAMIC_BASE`, so the runtime and the OS place them and the engine asks for nothing; that is why blocks can land above 2 GiB and why the convention needs them below 4 GiB. Type/spec propagation is the remaining item. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: closed: Limits item 23.)*

[EXP-002](../_experiments/EXP-002-st2e-group-tables.md) already reports base zero
at the title screen, with module/string and shifted-read controls. Its record
also gives sixteen low-address table pointers. This review recovered the
published observation, not its original raw read transcript or complete
module inventory. It therefore adds no fresh live validation. A repeated
title-screen snapshot would not prove the base or allocation range for the
whole process lifetime.

## 5. Low addresses are a separate proof obligation

The PE's `DllCharacteristics` is `0x8120`, with `DYNAMIC_BASE` clear.
Microsoft documents bottom-up randomization as a process/system option that
can be enabled even for an executable that did not opt in. The header alone
does not establish the effective process policy.
([MSRC explanation](https://www.microsoft.com/en-us/msrc/blog/2017/11/clarifying-the-behavior-of-mandatory-aslr),
[process policy structure](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-process_mitigation_aslr_policy))

An allocation starting low is also different from a proven upper bound over
later allocations. Neither the imported
[`malloc` contract](https://learn.microsoft.com/en-us/cpp/c-runtime-library/reference/malloc?view=msvc-170)
nor the observed EXE header supplies a sub-2-GB guarantee for these resource
buffers. Actual arena backing and the signed/unsigned conversions at each
consumer must be traced.

Historical mod-session notes in `Collaboration/CLAUDE_PROGRESS.md` (z146) and
`XIIOnlineNet/SemaphoreFix.h` describe zero-base reads and separate allocations
crossing 2 GB, with a separately installed allocator mod mentioned in the
history. These are leads, not controlled evidence of an unmodified shipped
resource arena. No raw crash attribution or module inventory was recovered
for them here, and no mod was installed, removed or changed.

## 6. Corrections and remaining work

`ASTRA-CONTRA-FABLE-RESOURCE-ARENA` routes the metadata-helper correction and
J-C/CD-2/BW-2 proof limits. `ASTRA-CONTRA-OPUS-REFERENCE-LIFETIME` routes the
contract's conflicting assumptions and existing snapshot evidence. Consumer
agreement, type/spec propagation and question reopening remain pending. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: closed: both routed contradictions are DONE on the board, and J-C, CD-2 and BW-2 are SUPERSEDED; see Limits items 2, 3 and 23.)*

The next bounded offline package identified by the initial review was the arena's
initialization and backing path. Its completed follow-up is recorded below.
Preserve the actual allocator family disposition while documenting this
architectural dependency. The no-arena conclusion cannot stand in for it.

The base's lifetime still needs adequate writer/alias coverage or appropriately
scoped authorized observation; one read cannot prove every instant. The live
pause remains. These unresolved claims do not block unrelated database work
and do not make the L1/L2 completion requirements disappear. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the base's lifetime is Limits item 3: the static route is exhausted, and the one live read is ASTRA's carrier `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`. The live pause was lifted by the user's authorization recorded in §10.)*

## 7. Backing acquisition follow-up — 2026-09-12

The [backing receipt](../_experiments/evidence/resource-arena-backing/primary.json)
captures thirteen complete original bodies, instruction bytes, hashes and the
same PE import walk. The EXE identity is unchanged. This is a static trace of
original calls and arguments, not an execution of boot or CRT allocation.

The boot function `0022A0B0` calls `0036D240`, stores each returned RAX as a qword,
and later passes the matching qword as RDX to initializer `00369D30`. The
14-byte `0036D240` sign-extends ECX to RCX, sets R8D to -1 and EDX to zero, then
tail-jumps through `0085E730` to IAT `008C2B40`, the imported `malloc`. There is
no returned-address check in these two tail thunks. The following nine boot
allocation/init pairs are directly recoverable; numbers in the table are hex.

| Arena id | `malloc` request | Initializer size | Bookkeeping slots | Initializer call site |
|---:|---|---|---|---|
| 2 | `1DC0010` | `1DC0000` | `10` | `0022A2AE` |
| 3 | `D20100` | `D20000` | `100` | `0022A2CB` |
| 4 | `100010` | `100000` | `10` | `0022A2E7` |
| 5 | `1C0100` | `1C0000` | `100` | `0022A304` |
| 6 | `6C00400` | `6C00000` | `400` | `0022A321` |
| 7 | `3000100` | `3000000` | `100` | `0022A33E` |
| 8 | `2000100` | `2000000` | `100` | `0022A35B` |
| 9 | `1200010` | `1200000` | `10` | `0022A377` |
| 11 | `400100` | `400000` | `100` | `0022A394` |

The boot sequence also makes requests `80000` and `100000` without pairing those
two returns with the initializer here. They are not counted as additional arenas.
There is no NULL, 2-GiB or 4-GiB returned-pointer guard between the nine traced
allocation returns and their initialization calls. This bounded negative comes
from complete instruction and control-flow review; it is not an import-count
inference. The other boot callees, CRT implementation and actual allocation
placement have not been executed or proven by this table. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: placement is §11 and Limits item 2.)*

The current direct-call graph lists four other initializer callers, all captured
and read in full. That graph is not an exhaustive indirect-call census:

| Caller | Backing acquisition and initialization |
|---|---|
| `0025A990` | Selects logical source 5, calls arena allocation `0036A190(100000)`, restores the prior selection, tests for NULL, annotates the prefix, then initializes arena 13 with size `100000` and zero bookkeeping slots |
| `0025AA30` | Same pattern for size `19000` and arena 14, again logical source 5 and zero slots |
| `003E9AA0` | Selects the nonnegative caller-supplied logical source, or 6 for a negative input; obtains the caller-supplied size through `0036A190`; NULL enters explicit self-loop `003E9AE0`; success initializes arena 12 with zero slots and then restores selection |
| `0037B3D0` | On its state-change branch, replaces arena 11's backing via `0036D240`, choosing size `3C0000` when state byte `02ADD930` is 3, otherwise `400000`; initializes with `100` slots. Prior teardown/helper effects are not established by this caller alone *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: established in FABLE's arena-residue record: it reports and disables arena 11 and frees the old backing before the new allocation; see Limits item 18.)* |

The nested-source qualification matters. `0036C1D0` forwards to the complete
150-byte `0036C1F0`, which saves the prior selection/settings, then loads the
active id from byte map `022D89A8[logicalSource]` into `022D89BC`.
`0036C140` restores the saved selection/settings. The initializer establishes
an identity map `0..14` when the enabled mask is initially zero. Thus logical
source 5 means arena 5 **under that identity map**, not under every possible later
mapping. Mapping writers/lifetime are a remaining dependency. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered: Limits item 4 (b7 M1).)* The allocation
layer still establishes nested arena backing regardless of that qualification.

## 8. Initialization, address width and remaining limits

`00369D30(id, backing, size, bookkeepingCount)` rejects unsigned ids above 14.
For admitted ids, it keeps backing in R14 and stores the full qword in arena
record `+08`. It aligns its internal regions to 64 bytes, lays out a map, a
qword array and optional 16-byte bookkeeping records, and establishes the first
free block. Record `+90` and `+98` both initially point to that block.
It then calls `0036A490` to write the initial block header. There is no
backing-NULL or address-ceiling test in this complete initializer body. Size and
bookkeeping arithmetic still includes signed 32-bit operations; this is not an
unlimited-size specification or an assertion that every admitted input is safe.

[EXP-077](../_experiments/EXP-077-arena-initializer-address-width.md) executed the
complete original initializer, block-header writer and encoder in initialized
synthetic state. The only substituted callee was a no-write formatter. Backing
addresses `40010000`, `80010000` and `100010000` all returned with the exact
expected full-width pointers for a one-MiB region and 16 bookkeeping slots.
Id 14 succeeded; ids 15 and -1 returned without changing the initialized fixture.
All six controls passed; a private `mov r14d,edx` truncation mutant was detected
by the previously passing above-4-GiB fixture, faulting at the first backing write.
No new live observation or CRT allocation was performed.

The high-address result closes an **initializer-level** ceiling hypothesis for
these inputs. It does not close downstream safety: the allocator uses encoded
32-bit block links, and its list/split/reclamation helpers require native
composition before their high-address consequences are established. The actual
process placement, decoder-base lifetime, selector-map lifetime, arbitrary size
boundaries and resource storage lifetime remain separate open obligations. *(2026-09-30, SWE2-CONTRACT: see Limits item 2, 3, 4, 8 and 9.)*

The immediate consecutive-allocation follow-up is now recorded in section 9;
the broader reclamation and lifetime obligations above remain open. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: reclamation is read in §19; lifetime is Limits item 9.)*

OPUS accepted the earlier reference-lifetime correction in `3a62fe9`, including
the existing EXP-002 observation and arena shape. FABLE's broader semantic
correction request remains open at this follow-up. The new backing table and
EXP-077 require peer consumer review; local evidence completion does not imply
contract/type/spec propagation or architectural closure. Preserve the existing
allocator family disposition while resolving these concrete obligations. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the correction request `ASTRA-CONTRA-FABLE-RESOURCE-ARENA` and the EXP-077 reviews `ASTRA-REQ-OPUS-ARENA-BACKING-REVIEW`, `ASTRA-REQ-FABLE-ARENA-BACKING-SUPPLEMENT` and `OPUS-ARENA-CONSUME-EXP077` are DONE on the board; see Limits item 23.)*

## 9. Saved allocation captures distinguish return values from link effects

[EXP-078](../_experiments/EXP-078-arena-allocation-link-width.md) uses EXP-077's
sealed output as the next operation's initialized fixture. It does not rerun the
initializer. Original selector, allocator, header, decoder/encoder and reached
list helpers execute without callee stubs in this stage. Subsequent review only
reads the saved data; it checks every recorded non-stack memory event against
the initialized bytes and earlier writes, plus all recorded final bytes.

At base zero and backing `100010000`, the first small allocation returns a full
high pointer. A second allocation reaches `0036C9D0` with a neighbor reference
that has been narrowed to 32 bits. In direction 0, its predecessor store faults
at `0036CA8A` on low address `10290`; in direction 1, its successor store faults
at `0036CA75` on low address `10FF8C`. The relevant fields are the neighbor links
at header `+0C/+10`, distinct from free-list links `+04/+08`. Low-address controls
complete in both directions. The above-2-GiB direction-0 control also completes,
so these observations do not establish a general 2-GiB ceiling.

A separate low mirror changes the direction-0 outcome: the second allocation
returns its expected high pointer but performs four writes and one read in that
separate region. Those exact mirrored bytes finish unchanged after a temporary
clear/restore. The evidence proves wrong-region access, not persistent corruption
in that control or a crash in the running game. A whole-block high allocation
also completes; creating and consuming a neighbor link is the distinguishing
operation. A completed targeted control loses a predecessor despite returning
both expected payload pointers, demonstrating why return-only checks miss it.

All seven original predictions, including the two controlled faults, match the
captured outcomes. Actual game placement, nonzero-base operating states,
reclamation, resource lifetime and integrated parity remain unobserved. FABLE
and OPUS received the earlier evidence in `1da16db`/`1feb742` and `579ae1a`;
the new allocation evidence still needs their consumer review. Two defects found
in those integrations are separately routed: the fourth initializer argument is
a bookkeeping **count**, not alignment, and the exact round-trip condition is
`((p - base) mod 2^64) < 2^32`, with the simpler signed-difference window requiring
a nonwrapping assumption. Existing EXP-076 already covers the wrap boundary. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: placement is §11, the base Limits item 3, reclamation §19, lifetime Limits item 9 and the integrated chain §20. The EXP-078 reviews `ASTRA-REQ-FABLE-ARENA-LINK-CONSUMER` and `ASTRA-REQ-OPUS-ARENA-LINK-CONSUMER` and both routed defects (`ASTRA-CONTRA-FABLE-ARENA-SLOT-COUNT`, `ASTRA-CONTRA-OPUS-REFERENCE-MODULO-WINDOW`) are DONE; see Limits item 23.)*

## 10. Selector-map reset and the adjacent settings stack

The [static selector receipt](../_experiments/evidence/arena-selector-static/primary.json)
preserves six complete original bodies and instruction bytes under the same EXE
identity. This follow-up uses method A; no game instructions were executed.
Besides the initializer's first-use identity map, `0036A280` unconditionally
writes the fifteen bytes `022D89A8..022D89B6` to `0..14`. Its 30-byte body uses
AL as both value and loop index and exits at 15. It is a reset, with no input
map or enabled-mask guard in that body.

The current direct graph has one caller, `002628B0`; the complete 1,689-byte
caller places the reset at `00262C84`. This call lies in the input-id-zero path
after the selected record's `+10` bit 0 test succeeds. The caller addresses
records at `02098E10 + signextend(id) * 288`, clears flags and pointer fields,
and later conditionally processes nested arena ids 13/14. This establishes a
record-clearing context, not a named initialization or gameplay event. An earlier
progress update called it another initialization path; that was too strong.
Unreviewed callees and actual scheduling are not established by reading this body. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the callees and the scheduling are the world-tick page's; see Limits item 19.)*

Nearby `0036C110` and `0036C1A0` operate a **different settings stack**:
depth `022D89C8`, byte buffer `022D8DD0`, current dword `022D8E1C`.
Push saves the low byte of the old setting, increments depth and installs ECX;
it rejects signed depth at least 31 but has no negative-depth rejection.
Pop rejects signed-negative depth, then decrements, restores a byte and
zero-extends it into the current setting. **Zero is not rejected**: that input
reads immediately before the buffer after storing depth -1. This is a local
boundary observation, not evidence that normal callers pop an empty stack.
Neither body writes the arena map. The setting's broader meaning remains open. *(2026-09-30, SWE2-CONTRACT: see Limits item 5.)*
`0036C100` is a NULL-tolerant dword getter at payload `-28` (header `+18`);
`0036C0F0` is a fixed-argument tail adapter to `0036A570`, also not a map writer.

The [scanner control receipt](../_experiments/evidence/arena-selector-static/review.json)
retains source/input hashes, the raw RIP candidates and exact graph rows.
The scan finds the known initializer and reset address materializations, but
**misses the known indexed selector read at `0036C272`**, which is present in
the image-base reference export and earlier complete selector body. Its `r`
label on LEA does not mean a memory read. This positive blind-spot control rules
out using the short result list as an exhaustive writer or lifetime proof.
Aliases, overlapping stores and unlisted/indirect code require separate coverage.

The fourth initializer argument's 16-byte bookkeeping-count role is already
established by EXP-077; FABLE's correction and EXP-078 integration are now in
`bd44aa4`, pending ASTRA's consumer review. Actual arena backing placement and
base/map lifetime remain open. The user's explicit authorization now supersedes
the historical live pause recorded above; [TEAM.md](../_index/_inbox/TEAM.md)
holds the current permission and stop/protection conditions. A bounded live
placement observation is the next sufficient method for placement, without
claiming that sampled values prove all-time lifetime. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: placement was then observed (§11); the base and the map are Limits items 3 and 4; the consumer review `ASTRA-ARENA-CONSUMER-PRIMARY-REVIEW` and FABLE's slot-count integration `FABLE-S24-ARENA-SLOTS` are DONE; see Limits item 23.)*

## 11. Actual title/load placement and the enabled-arena exception

[EXP-079](../_experiments/EXP-079-arena-live-placement.md) supplies method-C
observations in one verified reference process: ordinary title menu, then the
visibly selected The Stepping autosave loaded into the area. Two samples per
state preserve all fifteen arena records, selector/map/base and pointed bytes.
The full EXE text extent matches disk before each state capture; known nonzero
bytes and rejected null reads control the read-only observer. Full module paths
are retained, including Steam's overlay. No debugger or injected operation ran.

Enabled backings in both states are below 2 GiB. The mask changes `2BFC` to
`6BFC`, adding arena 14 at `6610EF40`; arena 11's backing changes `7C5D3040`
to `7C5D2040`. Base remains zero, selected arena 2 and the map `0..14` in all
four samples. These are actual placements and a changed record value. They do
not identify allocator/free order or prove the map/base at every instant.
The known replacement path is consistent with the observation, not live-traced.

Primary-byte review also finds a required exception: arena 7 remains enabled,
but its backing begins `EFX0010`, and its `+38/+90/+98` pointers all designate
`763A2940`, whose sampled 64 bytes are zero. Other arenas' `FF12` headers and
the nonzero/read-failure controls succeed. **An enabled mask is insufficient
proof of a currently usable block allocator.** The writer, purpose and lifecycle
of arena 7 remain open. *(2026-09-30, SWE2-CONTRACT: see Limits item 7.)* Arena 9 has null free-list ends despite being enabled;
zero-count nested records 13/14 have null `+38` and nonzero free-list ends.

All 154 pointed reads succeeded; captured nonzero link values numerically fit
the zero-base decoder, but their targets were not generally followed. EXP-078's
high-address failures remain isolated original-code evidence, not live failures.
The test instance exited, both read handles closed, all 26 original save/config
hashes were restored and Steam Cloud remained OFF. The tool's user-input halt
was honored; the user explicitly resumed exit/cleanup only. No further game
controls automatically resumed. Peer consumer review and the broader lifetime,
reclamation and arena-7 questions remain pending. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: arena 7's lifecycle is SD-166, ANSWERED (Limits item 7); reclamation is §19; lifetime is Limits item 9; the EXP-079 integration `FABLE-S24-ARENA079` is DONE.)*

## 12. Handle width and corrections found in actual consumers

The [handle receipt](../_experiments/evidence/arena-handle-static/primary.json)
preserves five complete shipping bodies under the same EXE identity. This is
method A, with no game-code execution. The 253-byte unlinker `0036C9D0` is
byte-for-byte identical to EXP-078's earlier primary receipt; the
[review](../_experiments/evidence/arena-handle-static/review.json) records the
exact FABLE/OPUS consumer versions inspected and retains seven original cases
plus the historical mutation control, without replaying or deleting either.

FABLE's handle-width finding is supported, with additional boundaries:

- `0036AF20(id, header)` first decodes header `+20`. If that associated slot is
  nonnull and its `+5` byte is nonzero, it returns the decoded slot's low 32 bits
  OR 3 (`0036AF88`) before inspecting the free-slot head. Otherwise it takes a
  new slot from arena `+40`, links it into `+48`, writes header pointer at slot
  `+8`, encodes the slot into header `+20`, copies header word `+1C` to slot `+6`
  and sets slot `+5` to 1. The new return also narrows the slot address (`0036B018`
  / `0036B01B`). Thus null `freeSlotHead` prevents **new** issue, not reuse of an
  already associated active handle. Exhaustion reaches a formatter call then
  returns zero; the formatter's native effects were not executed here.
- `00369800` tests low-32 nonzero, any low tag bit, and unsigned value at least
  `100000`; it masks RCX with zero-extended `FFFFFFFC`, reads slot `+8`, calls
  `0036A9C0`, and conditionally tail-calls `00369860(header+40,0)`. Its local
  tag test also admits low tags 1 and 2, although issue returns tag 3. It does
  not compare the copied slot `+6` / header `+1C` words before that read. These are local
  admission facts, not proof that arbitrary supplied handles are safe or that
  normal gameplay supplies those tags.
- `0036A9C0` removes an active slot from the index-linked in-use list and pushes
  it onto the free list, then clears slot `+5/+6/+8`. Header-flag changes and a
  conditional call to `0036C790` are visible; that callee's effects remain outside
  this package. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: `0036C790` is the tree removal read in §18.)* No direct store in this body clears header `+20`. Handle lifecycle and
  reuse safety therefore require their actual consumers, not a generation-safety
  inference from the copied word alone.
- `0036C4B0` also consumes the issued value: after its nonzero/tag/range branch,
  it masks to `FFFFFFFC` and writes the full header through low slot `+8` at
  `0036C572`. Truncation matters before the later release helper as well. Its
  failure path calls `00369860`; that call boundary is not a fresh execution
  proof of all reclamation effects. No high-slot live intervention ran.

OPUS's new unlink comments inverted the neighbor names. The actual loads set
RSI from decoded header `+10` (**successor**) and RDI from decoded `+0C`
(**predecessor**). `0036CA75` writes successor `+0C = encode(predecessor)`;
`0036CA8A` writes predecessor `+10 = encode(successor)`. This is consistent with
EXP-078's first allocation and the two recorded fault addresses.

The earlier prefix of that same complete body already decodes free-list `+08`
at `0036C9FA` and `+04` at `0036CA05`, and re-encodes their counterparts before
stores at `0036CA1D`/`0036CA32`. Their encoding is therefore established
**statically**, even though EXP-078 did not execute nonzero free-list links.
Unreached inserters do not erase evidence in another body. Incoming EDX zero
skips neighbor removal at `0036CA50`; the `FF99` tag and neighbor clearing occur
only on the nonzero path. The purpose of the repeated `+3E` zero writes remains
open. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered: the guard word, Limits item 14.)* Do not convert those conditional stores into an unconditional unlink rule.

`ASTRA-CONTRA-OPUS-ARENA-UNLINK-CONSUMER` routes these exact comment/type and
evidence-class corrections. `ASTRA-CONTRA-FABLE-ARENA-CONSUMER-BOUNDS` routes the
existing-handle exception, the surviving contradictory "no pool to size" reason,
and the case distinction: EXP-078 tested both low directions but above 2 GiB
only in direction 0. Consumer agreement and propagation remain pending. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: both requests are DONE on the board; see Limits item 23.)* The
modular pointer round-trip correction remains valid; it must not leave prose
calling the zero-base encoder an identity over arbitrary 64-bit pointers.

## 13. Arena 7 backing is also a direct resource destination

The arena-7 exception now has a concrete static context. The existing boot
receipt shows `0022A236` returning the `3000100` allocation, stored at
`01FD4A30` by `0022A240`. `0022A326..0022A33E` passes that same qword to
initializer id 7, size `3000000`, count `100`. The
[new consumer receipt](../_experiments/evidence/arena7-backing-use/consumers.json)
contains four complete original bodies that read this backing global. It is
passed directly to the resource layer, without adding an arena payload offset:

| Caller | Direct use of the boot backing |
|---|---|
| `003B0660` | Obtains size for kind `0A`, index 0; passes backing in R8 to `0032E620` at `003B070D`; calls `0032E520(0)` to drain; passes backing and its dword `+0C` to EFX loader `003EDAD0` at `003B0745` |
| `002FC860` | Selects kind `0B` or `26`, including its index fallback paths; passes the backing in R8 at `002FC96F` with status callback `002FC830` |
| `003B2310` | Selects kind `0C` and an adjusted/fallback index; stores backing in caller record `+28`, passes it in R8 at `003B2424` with callback `003B22D0` |
| `002FC4A0` | Reads backing dword `+0C` at `002FC56D`, then calls EFX loader with the same backing at `002FC5D2` |

Numbers in this table are hexadecimal. The complete
[queue bodies](../_experiments/evidence/arena7-backing-use/queue.json) verify that
`0032E620` preserves the full R8 pointer in RBP and passes it through either
branch to `0032E870`. That complete
[destination builder](../_experiments/evidence/arena7-backing-use/destination.json)
stores it as qwords at request `+38/+70` (`0032E94D`/`0032E970`). Thus this is an
actual destination field, not an inferred meaning of an arbitrary third argument.
The drain body loops over pending requests and read status; its idle return is
not proof that a particular file read succeeded. Native I/O/callback execution
and which request produced EXP-079's bytes remain unobserved. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: out of this note's scope, a property of one past sample: Limits item 10.)*

The eight [RIP candidates](../_experiments/evidence/arena7-backing-use/rip-candidates.txt)
include the known boot store and initializer read as controls. They lead to the
four consumers above, but are not an exhaustive alias/writer census. The prior
indexed-reference blind spot still applies. Exact EXE, source hashes, complete
body lengths and the three EFX magic strings are retained in the
[review receipt](../_experiments/evidence/arena7-backing-use/review.json).

This direct resource use explains why an arena's recorded backing can contain
an EFX input instead of the initial allocator annotation. It does **not** recover
the actual live write sequence or show that the generic allocator remains usable
afterward. The raw zeros at arena 7's recorded header pointers stay valid evidence;
they are not a read failure or a reason to delete the arena's lifecycle question. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the lifecycle is SD-166, ANSWERED (Limits item 7).)*

### EFX can retain its input instead of copying it

Reading the entire 1,934-byte `003EDAD0` exposes a relevant lifetime branch. The
current context is loaded through `02F97340`; for chunk families `A00` and `800`,
context byte `+2` bit `04` chooses the storage behavior:

| Chunk family | Bit clear | Bit set |
|---|---|---|
| `A00` | Select logical allocation source 8/settings `0A`, call `0036A100`, publish allocation to context `+878`, restore selection and copy the measured input run | `003EE078` stores input cursor R12 directly at context `+878` |
| `800` | Same allocation/copy pattern, publishing context `+870` | `003EE171` stores input cursor R12 directly at context `+870` |

The deciding tests are `003EE018` and `003EE117`. Source 8 maps to actual arena
8 under the observed identity map; do not assume that mapping in every state.
The parser then passes pointers into the selected storage to `003A9A70` or
`003A9730`. Those callees' native effects and context-flag ownership are outside
this package. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the two registrars are read in §14 below, and the flag's setters are Limits item 10.)* The `600`-family and `700` paths have their own measured allocation
and copy steps; "the entire EFX is copied" is not a valid generalization.

These published input pointers make storage lifetime a dependency for downstream
consumers. Their survival through the unreviewed callees and parser return is not
established here. The current EXP-079 context flag was not captured, so this is
**a static conditional lifetime dependency**, not a claim that the observed live
context borrowed the shared backing. Who sets the flag and how subsequent
resource requests avoid invalidating retained input remain required questions. *(2026-09-30, SWE2-CONTRACT: see Limits item 9 and 10.)*

A smaller layout correction arose in the same full-body read: the `610` sizing
path reads `[RAX+0F]` while RAX is **chunk+4**, so its byte is at **chunk+13**.
The copy path independently reads destination `+13`, consistent with that offset.
The older effect page's chunk-relative `+0F` description is incorrect. Its list
of special chunk families also needs the explicit `800/A00` branches; `701`
is not an explicit special comparison in this body. The generic fallback
`003EE2D0` remains a separate unreviewed consumer. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: read on the parent page; see Limits item 21.)*

FABLE/OPUS received `ASTRA-REQ-*-ARENA7-EFX-LIFETIME` with these primary receipts
and the requested owned-page/type/contract corrections. Peer agreement and
propagation, the context flag, exact live file and writer, shared-buffer lifetime
and subsequent consumer effects remain open. No live automation restarted. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the requests `ASTRA-REQ-FABLE-ARENA7-EFX-LIFETIME` and `ASTRA-REQ-OPUS-ARENA7-EFX-LIFETIME` are DONE. The flag and the live file are Limits item 10, the writer and lifecycle item 7, the shared-buffer lifetime item 9, and the subsequent consumers §14's registrars and their setup fronts (items 11 and 21).)*

## 14. EFX input mode comes from the template and affects payload mutation and teardown

Method A now resolves the local flag source and selected downstream effects.
The complete [constructor and payload consumers](../_experiments/evidence/efx-input-lifetime-flag/context.json),
[EFB, dispatch and teardown bodies](../_experiments/evidence/efx-input-lifetime-flag/retention.json),
and [substructure initializers](../_experiments/evidence/efx-input-lifetime-flag/init.json)
retain exact shipping bytes and hashes. The
[review receipt](../_experiments/evidence/efx-input-lifetime-flag/review.json)
records the boundaries; no original instructions were executed for this package.
Sixty [RIP candidates](../_experiments/evidence/efx-input-lifetime-flag/rip-candidates.txt)
include constructor publication and EFX context-read controls. They do not
exhaust aliases, indexed accesses or overlapping writes. Numbers below are hex
except explicitly decimal counts.

`0024B3A0` allocates and copies the full `890`-byte caller template, links it
into `020910A0[template byte 0]`, clears run pointers `+870/+878/+880/+888`,
and publishes it at `02F97340` (`0024B477`). The five substructure initializers
clear or allocate their separate ranges; with valid nonoverlapping allocations,
their direct stores do not overwrite template byte `+2`. Allocation and CRT
callee effects were not executed. This establishes the caller-template branch
input, not an exhaustive context-writer census.

The EFB wrapper `0026FB90` zeroes its template, sets type 2, and ORs byte `+2`
with `0C` at `0026FC60`, before constructing each embedded EFX context. Thus
the local EFB path supplies mask `04` set to the parser's input-pointer branch.
Its post-parse merge at `0026FD1A..0026FD26` computes
`new flags = (old flags & 0F) | (first nonnull entry flag & F0)`, preserving
mask `04`. By contrast, the reviewed arena-7 callers `003B0660` (type 5) and
`002FC4A0` (type 1) start from zeroed templates and set type/id without this
mask, requesting the copy branch. These are static caller paths; EXP-079 did
not capture its live context or flag. FABLE independently integrated the EFB
and type-5 distinction in `29a501e`; the type-1 caller is another known path.

### Selected handlers mutate the chosen storage and publish payload addresses

For an `800` chunk, `003A9730` receives chunk `+0C`, advances four bytes to
the payload at chunk `+10`, and writes the input subtype/id into payload
`+282/+280`. It then publishes the **full payload pointer** into a qword table
indexed by the input word id (`003A9767`). The table is reached through global
`02EBEF90`, context `+848`; its initializer allocates `A00` bytes, or 320
decimal slots. The analogous `A00` consumer `003A9A70` writes payload
`+44/+42` and publishes the pointer at `003A9AA1`, through `02EBEF78`, context
`+850`; that table has `1800` bytes, or 768 decimal slots. Neither body checks
the word id against table capacity before the store. Authored/admission bounds
remain a separate question; this is not evidence that normal ids exceed them. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered over the shipped data: every id is below capacity; see Limits item 20.)*

Both consumers form a subsequent argument in **EDX** by adding
`dword[02EBB738]` to the low 32 bits of the payload pointer, then call
`00442460` or `005004C0`. That width is observed in the instructions; the
downstream interpretation is not inferred from it. The two complete dispatch
fronts tail-dispatch by subtype to further handlers. `00442460` returns directly
for subtype above 8; `005004C0` has diagnostic bookkeeping, two-stage dispatch
and a default handler. Their table mappings and all native handler effects
are not covered here. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the `00442460` table is decoded below, the `005004C0` table is Limits item 11, and each subtype's setup is in FABLE's OV-41 record (item 21).)* The consumers return payload plus the sign-extended
supplied size, but return arithmetic does not establish handler side effects.

Consequently, input mode is **not a read-only file view**: these selected
handlers modify the borrowed bytes and publish addresses into them. Survival
through every native handler, parser return and later request remains open. *(2026-09-30, SWE2-CONTRACT: see Limits item 9.)*

### The `00442460` table, decoded (SWE2-FRONTIER, switch-families package)

`00442460` (82 B) bounds the payload's `+0x282` subtype byte ≤ 8 and tail-jumps through RVA
table `004424B4`; subtype above 8 returns the payload pointer unchanged (`004424AE`). Every
arm runs `00442380` — the **shared base rebase** (213 B): 7×`004304F0` (1T) at
`+0x00`–`+0x60` (`0x10` stride), 7×`00430AF0` (3G) at `+0x70`/`+0xB0`–`+0x1F0` (`0x40`
stride), 1×`0042FCF0` (4G) at `+0x230`, then it returns `rdi + 0x2DC` as the record-end
pointer (`00442443`–`0044244F`). The per-subtype extras:

| subtype | handler | extra work after the base rebase |
|---|---|---|
| 0 | `00442380` | none — base fields only, record ends `+0x2DC` |
| 1 | `005322F0` (27 B) | none — thunk returning the same `+0x2DC` end pointer |
| 2 | `00532310` (108 B) | 3×1T `+0x2DC`/`+0x2EC`/`+0x2FC` + 2×3G `+0x30C`/`+0x34C` |
| 3 | `00532380` (108 B) | 2×1T `+0x2DC`/`+0x2EC` + 3×3G `+0x2FC`/`+0x33C`/`+0x37C` |
| 4 | `005323F0` (80 B) | 3×3G `+0x2DC`/`+0x31C`/`+0x35C` |
| 5, 6 | `00532440` (122 B) | 4×1T `+0x2DC`–`+0x30C` + 2×3G `+0x31C`/`+0x35C` |
| 7 | `005324C0` (94 B) | 2×1T `+0x2DC`/`+0x2EC` + 2×3G `+0x2FC`/`+0x33C` |
| 8 | `00532520` (174 B) | 2×3G `+0x2DC`/`+0x31C` + 1×1T `+0x35C` + `003AA280`/`0020E620` child-ref resolve |

So the front is a **per-subtype pointer-rebase ladder**: a fixed common layout (7 single
tracks, 7 three-track groups, 1 four-track group) plus a subtype-specific tail, and subtype 8
additionally re-resolves a child reference. Subtypes 0 and 1 share the layout exactly. The
sibling front `005004C0` remains undecoded here. *(2026-09-30, SWE2-CONTRACT: see Limits item 11.)*

### The step-side front `00442170` over the same subtype byte

`00441B30` — reached from `003A8AE0` and `0043EF40` — gates on sub-record `+0x2C4` flag bits
(`0xC0` set, or `0xC & 8`), copies the `r8` transform (`+0x70`/`+0x80` → obj `+0x150` via
`0043EEB0`), then calls `00442170` (367 B). `00442170` dispatches on
`[[obj+0x100] + 0x282]` — the same subtype byte — through RVA table `004422E0`: subtype 0 is
an inline reset (`+0x9C = 1.0f`, `+0x80`–`+0x8B` and `+0x90`–`+0x9B` zeroed — `+0x8C`–`+0x8F` is
not written, `004421B3`–`004421D9`); subtypes 1–8
call large per-subtype step bodies `005315B0`, `0052F780`, `00531DB0`, `00530770`,
`0052FCA0`, `00530230`, `005318A0`, `00530E40` (740–1898 B each — bodies not read beyond
their heads). *(2026-09-30, SWE2-CONTRACT: see Limits item 12.)* A second stage then dispatches on `[[obj+0x100] + 0x283]` for values **0, 2 and 7**
(`00442239`–`0044224A`): 7 unconditionally runs the `+0x60` add block (three floats
`[rdi+0x60]`/`+0x64`/`+0x68` accumulated into `[rbx+0x80]`/`+0x84`/`+0x88`, `00442250`–`0044227A`);
0 runs the parallel `+0x70` add block (`00442295`–); **2 gates on the word compare
`[[rdi+0x18]+0x286] == [rdx+0x286]`** (`00442281`–`00442293`) — match takes the `+0x60` block,
mismatch the `+0x70` block. Which subtype values correspond to which
authored element types is **not established** here — the `+0x282` domain is internal to the
`800`-chunk payload, not the file's element-type byte. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered: they are separate families and do not correspond; see Limits item 21.)*

### Release calls are conditional, and a relocation front exists

The complete `003A9600`/`003A9950` first test context byte `+3` mask `01`.
When set, they call `003697F0` on nonnull chunk `+870/+878` only if byte `+2`
mask `04` is clear; either way they clear the chunk pointer. When byte `+3`
mask `01` is clear, they instead walk table entries starting at index **1**,
through 319 or 767 decimal respectively, release nonnull entries and clear
them. Both branches finally tail-call the same helper on the table allocation.
The mask-`04` release exemption must not be generalized to those individual
entries or the final table. The complete 13-byte `003697F0` returns for null
and otherwise tail-calls `00369860` with EDX zero; downstream reclamation is
a call boundary here, not a new execution result.

`003B3480` supplies a concrete next lifetime dependency. Only with context
mask `04` set, it binds/publishes the context, resolves signed field `+860`
through `003AB7F0`, adds signed `+864`, and compares the result with `+858`.
A change calls `0024D970(context, new base)`; an optional instance also compares
its `+390` and conditionally calls `0024D940`. The provider and rebase helpers
are the next bounded primary-code review. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: read in §15.)* This conditional front alone does
not prove that every retained address is repaired or survives resource reuse.

Focused peer review and owned prose/type/contract propagation are requested
under `ASTRA-REQ-*-EFX-INPUT-LIFETIME`. Keep actual live context identity,
EFB storage ownership/reuse, dispatch effects, admission bounds and relocation
coverage open. No runtime reservation or game restart was needed. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the live context is Limits item 10; EFB storage is the container page's §2b (one fixed block that only the map teardown `00378230` frees); dispatch effects are items 11 and 21; admission bounds item 20; relocation coverage items 13 and 16; the requests `ASTRA-REQ-FABLE-EFX-INPUT-LIFETIME` and `ASTRA-REQ-OPUS-EFX-INPUT-LIFETIME` are DONE.)*

## 15. EFX relocation repairs selected references with a signed 32-bit displacement

Following section 14's actual call edges, the complete
[provider and rebase fronts](../_experiments/evidence/efx-rebase-primary/primary.json)
and [repair helpers](../_experiments/evidence/efx-rebase-primary/repairs.json)
establish the arithmetic and affected fields. A bounded
[original-code probe](../_experiments/evidence/efx-rebase-primary/probe.py)
then tests the width boundaries in Unicorn with injected slots, contexts,
tables and payload bytes. It executes verified shipping instructions, with no
stubs, but does not initialize the game or move a real resource. The
[raw results](../_experiments/evidence/efx-rebase-primary/result.json),
[memory/ABI review](../_experiments/evidence/efx-rebase-primary/execution-review.json)
and [scope receipt](../_experiments/evidence/efx-rebase-primary/review.json)
separate method A from method B. Hexadecimal notation continues below.

### Provider output width differs from the caller's input width

`003AB7F0` returns a nonzero, untagged RCX unchanged. Any of the low two tag
bits instead sends its low 32 bits to `0036B130`. That resolver requires a
nonzero tagged value at least `100000` unsigned, masks the slot address to
`FFFFFFFC`, and returns the full qword at slot `+8` plus `40`. It does not
read the slot active byte or copied word. Valid slot storage remains a
precondition; this is not an arbitrary-input or stale-handle safety check.

On return, the wrapper compares **the unsigned 64-bit value of the
sign-extended low 32 bits** with `40`, replacing RAX with zero if it is at
most `40`. Otherwise the original full RAX survives. The controlled tagged
cases return `80002000` and `180002000` intact. Returned `100000040` is
suppressed, while `100000041` survives. Thus this is not a simple full-pointer
`p > 40` test or an unconditional truncation of the returned pointer.

The caller `003B3480` separately loads context dword `+860` using `MOVSXD`.
The untagged value `80002000` therefore reaches the provider as
`FFFFFFFF80002000`, confirmed by the original entry trace. Directly entering
the provider with untagged `180002000` preserves it; those two entry boundaries
must not be conflated. Meaning and initialization of the stored source field
remain on the frontier. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered in §16: `003B38B0` stores the original source value at `+860` and the offset at `+864`.)*

### Context repair order and table coverage

`0024D970` computes `delta32 = low32(new base) - low32(context[+858])`, then
calls `003AA3D0`, `003A9BA0`, and `003A9860` in that order. It writes the full
new base to context `+858` **after** these calls. The first helper walks the
context `+18` list, dispatching byte-`+0E` types `52/56` to `00501420` and
`00503F10`, and decodes each dword next link through `0020E600`. Those nonempty
list handlers are not executed or fully reviewed in this package. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered: Limits item 16.)*

The A00 and 800 table helpers sign-extend `delta32` to 64 bits. For each
nonnull slot from index 1 through 767 or 319 decimal, they call the subtype
dispatcher with `RCX = old slot pointer + signed delta`, EDX equal to the
32-bit delta, then add the signed delta to the current slot qword after the
call. Index **0 is skipped**. The post-call global/table reload matters:
the direct store alone does not prove what an arbitrary handler left there.
These bodies do not directly rebase context run pointers `+870/+878`.

The execution cases keep the list and A00 entries empty and set the first and
last 800 slots to payloads with subtype 9. That subtype takes `00442460`'s
original direct-return branch; no native effect handler is stubbed or claimed
executed. A nonzero index-0 entry remains unchanged as a skip control. Both
complete table traversal ranges, dispatcher reads, table writes and final
base publication are present in the raw trace.

| Controlled old/new bases | Signed repair delta | Tested entry before -> after | Published base |
|---|---|---|---|
| `40000000` -> `40002000` | `+2000` | `40000100` -> `40002100` | `40002000` |
| `40002000` -> `40000000` | `-2000` | `40002100` -> `40000100` | `40000000` |
| `40000000` -> `140000000` | `0` | `40000100` -> `40000100` | `140000000` |

The last case changes the supplied provider value by 4 GiB, without moving a
real buffer. It disproves a general 64-bit displacement repair contract for
this composed path. Exact repair requires the actual modulo-64-bit displacement
to equal the sign extension of its low 32 bits. High absolute placement alone
does not violate that condition. The flag-clear control performs no publication
or repair; an equal-base control skips the repair calls.

### Instance fields and binding preconditions

`0024D940` likewise passes a 32-bit difference from instance `+390` to
`003A8FF0`, then stores the full new base. The helper walks outer nodes through
`+8`, adjusting qwords `+100/+108`; each outer node's `+118` list advances
through `+30` and adjusts qwords `+18/+20`. It checks list-node pointers, but
does **not** filter zero values in the adjusted fields. A direct original-code
case with two outer and two inner nodes confirms a `-1000` adjustment, including
zero fields becoming `FFFFFFFFFFFFF000`; traversal links stay unchanged.
This injected boundary is not proof that initialized game nodes contain zero
in those fields.

When `003B3480` receives an optional instance, `0024ED80` obtains the active
context from instance `+340`, publishes its substructures plus instance state,
and tail-calls presentation-state helper `0024FCF0`. Consistency with the
separately supplied context is a composition precondition. The complete
`003B3550` also contains a guarded provider/rebase check before instance
construction and copies context `+858` into instance `+390` in input mode.
Those binding, construction and presentation effects are static evidence here;
the instance execution begins directly at `0024D940`.

All 15 bounded runs returned with unchanged original code, stack and nonvolatile
state intact. Every recorded nonstack read/write reconciles with the saved
initial and final bytes. A private receipt copy with one real table write
removed fails that review despite retaining successful return/ABI flags. The
[first setup failure](../_experiments/evidence/efx-rebase-primary/first-attempt.json)
executed zero game instructions because the emulator directory was inaccessible;
the same script subsequently ran with scoped tool authorization. That failed
attempt is preserved and is not a pass. No full mutation campaign was repeated.

`ASTRA-REQ-*-EFX-REBASE` requests focused peer review and propagation. Source-field
initialization, omitted subtype/list handlers, EFB storage ownership/reuse,
repair of all retained references and actual caller scheduling remain open. *(2026-09-30, SWE2-CONTRACT: see Limits item 9, 13 and 16.)*
The live-game controls remain halted after the exit/cleanup-only resumption.

## 16. A type-3 borrowed context tracks its source and offset from construction

Method A now identifies a second input-mode constructor, beyond the EFB path.
The complete [additional constructors](../_experiments/evidence/efx-source-initialization/constructors.json)
contain `003B38B0`: it sign-extends incoming ECX and EDX, resolves the first
through `003AB7F0`, and adds the second to obtain the full EFX base. After
obtaining a management record, it zeroes a stack template, sets type 3 and ORs
`0C` into template byte `+2`. It then stores the tracking fields before calling
`0024B3A0` and `003EDAD0`:

| Context field | Template store | Value |
|---|---|---|
| `+858`, qword | `003B399C`, stack `+878` | Resolved source plus signed offset |
| `+860`, dword | `003B398E`, stack `+880` | Original ECX source value |
| `+864`, dword | `003B3995`, stack `+884` | Original EDX offset |

The template starts at stack `+20`. The existing full constructor copies all
`890` bytes, including these fields. `003B39AD..003B39B3` passes the resolved
base and its dword `+0C` to EFX. Thus this context requests borrowed input and
has the exact source/offset pair consumed by the rebase paths. This is native
construction data flow; neither its actual scheduling nor source lifetime has
been observed live. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: scheduling is Limits item 13 and source lifetime item 9.)*

The [graph candidates](../_experiments/evidence/efx-source-initialization/edges.txt)
name six direct callers of the context constructor. Their original bodies are
now covered across sections 13–16:

| Caller | Template type | Mask `04` supplied |
|---|---|---|
| `0026FB90` | 2, EFB wrapper | Set; tracking fields start zero in this template |
| `002FC4A0` | 1 | Clear |
| `003B0660` | 5 | Clear |
| `003B2220` | 7 | Clear; its later nibble merge preserves the low nibble |
| `003B29B0` | 4 | Clear |
| `003B38B0` | 3 | Set; initializes source/base/offset as above |

These are known direct callers, not an exhaustive indirect-entry census. FABLE's
`29a501e` EFB/type-5 distinction remains valid; its two-template/exclusive EFB
framing is contradicted by the new type-3 body. This is routed immediately as
`ASTRA-CONTRA-FABLE-EFX-BORROW-SOURCES`; actual consumer correction is pending. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: DONE on the board; see Limits item 23.)*

### A direct-field scan would have missed this initialization

The [displacement scan](../_experiments/evidence/efx-source-initialization/scan.json)
finds 66 candidates and detects known direct write `0024D9A7` and read
`003B34F5`. It does not detect the three stack-template stores above, whose
displacements differ by `20`. The complete original constructor is therefore
an actual blind-spot control: no claim of zero or unique writers follows from
this scan. Candidates also include unrelated structures and stack operands.

The complete [context traversal/teardown bodies](../_experiments/evidence/efx-source-initialization/primary.json)
add a caller-side relocation route. For initial ECX zero, `0024D540` traverses
the list at `02091108` through instance `+348`, publishes each instance's
context from `+340`, and applies the guarded source-plus-offset comparison and
32-bit context/instance repairs before continuing its remaining system calls.
`0024D050` separately traverses ten list heads beginning `020910F0`, binds
the same context/instance globals, and calls `003A7420`. Their call frequency
and all intervening native effects remain unestablished here. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: answered at the call level: Limits items 13 and 22.)*

`0024F410` unlinks a context from its per-type list, publishes its substructures,
calls the five teardown helpers including the reviewed `003A9600/003A9950`,
then calls `0024F4D0` and `003697F0(context)`. Those call boundaries connect
the local release rules to context disposal; they do not establish every
callee's effects or prove safety for every context type.

### The source is supplied through a resource-entry ownership branch

The graph's direct caller of `003B38B0` is the complete
[`00409FE0`](../_experiments/evidence/efx-source-initialization/caller.json).
It resolves incoming RDX, then uses the complete 20-byte `003AB860` predicate
to distinguish a tagged value from an untagged one. Both paths initialize a
resource entry and call `00409A60`: mode 0 for untagged input, mode 1 for tagged.
Mode 0 subsequently replaces its source value with entry qword `+18`; mode 1
retains the incoming source and stores its resolved pointer at entry `+38`.
Later `0040A162` passes the selected source's **low 32 bits** to `003B38B0`,
with an offset read from the resolved resource. Complete offset-size helper
semantics and malformed-resource admission are outside this package. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: out of scope, with the shipped part registered: Limits item 8.)*

The [entry helpers](../_experiments/evidence/efx-source-initialization/owner.json)
show `00409A60` first resolving the source and normalizing the name padding
at resource `+10` to 32 bytes for a properly terminated, bounded name. Its
PRF branches also visit nested records with 32-bit base arithmetic; this does
not prove malformed names or offsets are bounded. Mode 1 stores the full
incoming source at entry `+30`. Mode 0 calls `003AB880`, then
`0051F020/006B5C70/0051EF90` around embedded storage `+10`, and finally
`003AB940`. These helpers' allocation/copy/release effects are the next bounded
ownership review. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: read in §17.)* `00409FE0` still uses the initially resolved pointer for a
later offset read; do not declare it freed, safe or dangling before that review.

The [receipt](../_experiments/evidence/efx-source-initialization/review.json)
seals eleven complete shipping bodies, both scan controls, graph identity and
unresolved boundaries. No additional original-code run or live automation was
needed. `ASTRA-REQ-OPUS-EFX-SOURCE-FIELDS` routes the field/provenance findings;
the FABLE contradiction routes semantic propagation. Source storage lifetime,
native effect repairs, context-type release preconditions and live scheduling
remain required work. *(2026-09-30, SWE2-CONTRACT: see Limits item 9 and 13.)*

## 17. Resource-entry copying preserves the raw input but narrows the destination

The complete [source/storage helpers](../_experiments/evidence/resource-entry-source-ownership/source.json)
and [allocation/access helpers](../_experiments/evidence/resource-entry-source-ownership/allocation.json)
resolve section 16's local ownership question by method A. In `00409FE0`'s
mode-0 branch, the input is untagged. `003AB880` returns that full pointer
unchanged, and the final `003AB940` returns immediately for untagged input,
without a callee or memory write. That final call therefore does **not** free
the original source before the caller's later offset read. All-time source
lifetime and effects of other callers remain separate questions. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: Limits item 9.)*

The embedded storage begins at resource entry `+10`. Its complete initializer
`0051EE10` sets kind `+0 = 0`, source qword `+8 = 0`, capacity dword `+10 = 0`,
growth dword `+14 = 800` and used dword `+18 = 0`. The last pair comes from a
single qword store of `800` at `+14`. Thus the source is entry qword `+18`,
the same field selected by `00409FE0` for the type-3 EFX constructor.

`0051F020` calls `003AB8B0(size, storage kind)`, stores its full result at
storage `+8`, and records capacity at `+10`. The allocator wrapper pushes
logical source 6/settings 6. Kind 0 calls `0036A100` and preserves full RAX;
kind 1 calls `0036B160` and saves EAX in EDI. It then restores the selector.
The initialized mode-0 entry takes kind 0, a raw allocation-pointer path.
Logical source 6 is actual arena 6 under the observed identity map; the map
must not be assumed immutable in every state.

### Append and growth have different destination arithmetic

The complete append helper `0051EF90` first compares unsigned 32-bit
`used + requested size` with capacity and invokes `0051EEB0` if necessary.
For a fresh entry with a valid nonnegative size equal to its capacity and
used zero, the requested copy fits without growth. Its later argument setup
is explicit:

- `0051EFED` resolves storage source through `003AB7F0`.
- `0051EFF2` adds the used count **in EAX**; `0051EFF8` moves EAX to ECX.
- `0051EFFA` supplies the original full source pointer in RDX, with the
  sign-extended requested dword size in R8.
- `0051EFFD` calls `00861EBA`, a shipping thunk whose decoded import is
  `VCRUNTIME140.dll!memcpy` at slot `008C2A68`.
- `0051F002` increments the used count after that call.

The destination passed to memcpy is therefore
`zero_extend32(low32(resolved destination) + used)`, not an arbitrary full
64-bit pointer. This is original argument-construction evidence, not a new
execution of the external memcpy or a live high-address failure. Overflowed
or negative sizes and malformed source headers do not inherit the fresh-entry
precondition above.

The complete growth helper `0051EEB0` differs: its preservation copy passes
both resolved pointers at full width and copies the smaller of old and new
capacity. Optional tail zeroing nevertheless forms its destination in ECX.
It calls `003AB7C0` on the old source and replaces the 32-byte storage record;
that release helper and its relation to final entry/context teardown remain
the next ownership boundary. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: read in §18 (`003AB7C0`).)* Do not propagate append's exact truncation site
as though every copy in this storage implementation uses the same arithmetic.

### Tagged access is not the same as the unchecked resolver

For tagged input, `003AB880` forwards to the complete `0036A000`, which checks
the masked low slot, nonnull header and equality of slot word `+6` with header
word `+1C`. If header byte `+15` mask `02` is set, it calls `0036C790`, clears
that mask and zeroes header `+3E`, then returns header `+40`. Conversely,
`003AB940`'s tagged branch forwards to complete `0036D170`: after the copied-word
comparison, a clear mask `02` causes a call to `0036B410`, setting the mask
and zeroing `+3E`. It reads header `+1C` without the other function's preceding
null-header test. These guards and effects differ from `0036B130`'s simple
slot resolver in section 15.

Section 18 now identifies the underlying membership structure as a tree;
its consumer purpose and copied-word lifecycle remain open. *(2026-09-30, SWE2-CONTRACT: see Limits item 15.)* Neither wrapper
is labeled a general lock, free or generation-safety
operation from its name. The complete untagged branch is sufficient to settle
the mode-0 no-release question without a live test or a stubbed callee.

The [review receipt](../_experiments/evidence/resource-entry-source-ownership/review.json)
seals eleven complete original bodies, exact code/import identity and remaining
boundaries. Focused review and owned prose/type/contract propagation are routed
as `ASTRA-REQ-*-RESOURCE-SOURCE-OWNERSHIP`. Actual lifetime, scheduling,
allocation placement and full release/relocation coverage stay open. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: lifetime is Limits item 9, scheduling item 13, placement item 2, release §19, relocation items 13 and 16; the requests are DONE (item 23).)*

## 18. Entry teardown orders context disposal before source release; membership is a tree

The complete [release and membership fronts](../_experiments/evidence/resource-entry-release-lists/release.json)
distinguish `003AB7C0` from section 17's `003AB940`: null returns, a tagged
source goes to `00369800`, and an untagged source goes to `003697F0`. Those
are the previously reviewed release fronts, including their low-slot and
conditional behavior; the full `00369860` reclamation body remains beyond
this package. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: read whole in §19.)* A call to `003AB940` must not inherit these different branches.

### The arena membership structure is a binary tree

The complete [insertion and child-link helpers](../_experiments/evidence/resource-entry-release-lists/tree.json)
establish a binary tree rooted at arena qword `+50`, with encoded header
dwords `+24 = left`, `+28 = right`, and `+2C = parent`. This corrects the
earlier provisional "list" shorthand; the evidence directory and task retain
their original names for history.

`0036B410` initializes all three node links with `encode(0)`, zeroes `+3E`,
and either installs an empty root or calls `0036B4E0`. That helper compares
header dword `+18` using **signed** `JLE` at `0036B50D`: smaller keys descend
left, equal or larger keys descend right. It stores encoded parent/child
links and zeroes `+3E` on the affected nodes. The key is the payload-length
field identified earlier; its storage width does not make this comparison
unsigned. The direct linker bodies contain no balancing operation.

`0036C790` removes a node using its decoded parent and children. If a right
child exists, it promotes that child and reinserts the left subtree under it;
otherwise it promotes the left child or clears the relevant root/parent link.
The complete `0036B490/0036B5A0` repair the corresponding left/right edge and
the replacement's parent. The removal body does not directly clear the
removed node's links or membership flag. Its caller `0036A000` clears header
`+15` mask `02`; `0036D170` inserts through `0036B410` and then sets that mask.
This identifies their membership effect, not the tree consumer's purpose or
an all-time pinning/lifetime guarantee. Header `+3E` meaning remains open. *(2026-09-30, SWE2-CONTRACT: see Limits item 14.)*

### The resource owner requests effect disposal before releasing its source

Both complete [entry-removal callers](../_experiments/evidence/resource-entry-release-lists/teardown.json),
`00409CA0` and `00409D60`, check entry dword `+44` against `-1`. When present,
they call `003B37E0(id)` before `00409730(entry)`, followed by registry removal
`0051FCF0`. This is a concrete static ordering of operations, not yet their
integrated live effect. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the integrated effect is SECTION-06's executed chain (§20).)*

`003B37E0` indexes the management table at `02EBCD80` using the low six id
bits and stride `38`, then requires equality with the **full stored id**.
Only a match proceeds. For a nonnull context it calls `0024F4D0(context)`
and `0024F410(context)`, then `003B39E0(id)`, recycles the management record
and clears its source/context fields. Valid id-to-context association is a
precondition; a stale id does not inherit successful disposal from this order.

The complete [inner teardown bodies](../_experiments/evidence/resource-entry-release-lists/inner.json)
show `0024F4D0` walking the context type's instance list, saving next `+348`
before unlinking instances whose `+340` equals the context. It calls the three
instance substructure cleanup helpers, queues instance `+380` or calls its
fallback when the queue is full, then calls `003697F0(instance)`. The complete
context disposer `0024F410` in section 16 also calls `0024F4D0`; the second
pass must not be described as a second free of the same still-linked instance
without tracing this unlinking and the intervening effects.

`00409730` next calls `00427B00(entry[+30])`, then `0051EE80(entry+10)`.
The latter calls `003AB7C0` on the embedded source **before** resetting the
storage record. Thus the mode-0 copy's release front is reached after the
identified effect/context disposal calls. The mode-1 source helper `00427B00`,
full allocator reclamation and all native instance/substructure cleanup effects
remain required boundaries. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: `00427B00` and `00369860` are read in §19; instance cleanup is Limits item 9.)* `003B39E0` separately recycles matching entries
in its 32-record management pool; its body contains no native heap-free call.

The [review receipt](../_experiments/evidence/resource-entry-release-lists/review.json)
seals thirteen complete original bodies and branch/order controls. This is
method A only. `ASTRA-REQ-*-RESOURCE-RELEASE-TREE` requests primary peer review
and field/contract propagation, including the signed tree comparison. Source
and instance lifetime, tree consumers, other teardown entry points and actual
scheduling remain open. No original-code campaign or live run was added. *(2026-09-30, SWE2-CONTRACT: see Limits item 9, 13 and 15.)*

## 19. Render-reference cleanup is distinct from native block reclamation

The complete [original cleanup/free bodies](../_experiments/evidence/resource-native-reclamation/free.json)
settle another boundary from section 18. `00427B00` does **not** free the
source supplied to it or adjust a source reference count. It traverses the
active `740`-byte render records through manager `022C6F28`, starting at index
`+48800` and following each record's signed word `+4`. It compares decoded
references at `+68/+D8/+F0` with its input, clearing matching reference pairs
`+68/+69C`, `+D8/+E0`, or `+F0/+F8`. Its only calls are the reference encoder
and decoder. A valid initialized manager is a precondition, including for a
null source argument. Thus mode-1 entry cleanup must not be mistaken for
reclaiming the owner of its borrowed data.

### The full free routine validates header state before reclamation

The entire 1,009-byte `00369860` is now read, rather than stopping at its
release wrappers. Null input returns. A pointer with either low tag bit set
takes a diagnostic path and bypasses reclamation. Otherwise its header is
input minus `40`, with these distinct gates:

| Condition | Original branch |
|---|---|
| Header magic differs from `FF12` | Diagnostic construction, arena reporting and an imported `exit(1)` call if diagnostics complete |
| Header word `+3E` is nonzero | `00369A80` selects the MCB-broken diagnostic, reporting and `exit(1)` path |
| Header byte `+14` mask `01` is clear | Already-free diagnostic, then return without the reclamation branch |
| Valid magic, zero `+3E`, mask `01` set | Clear the allocation state, update accounting, insert/coalesce the free block and refresh indexing |

The original diagnostic strings and
[free-order search bodies](../_experiments/evidence/resource-native-reclamation/order.json)
are retained. These are static paths, not executed failure outcomes. In
particular, the bad-magic diagnostic itself reads `B0` bytes from the header
and `D0` bytes from incoming RDX without validating those pointers; callers
that pass zero RDX do not thereby obtain a guaranteed clean diagnostic exit.
Header `+3E` now has a concrete **must-be-zero reclamation guard**, while the
algorithm or lifecycle that could make it nonzero remains unknown. Its zero
writes must not be dismissed as irrelevant, or promoted to a known checksum. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: a nonzero value is not a state the manager produces: Limits item 14.)*

The valid allocated branch marks arena byte `+2`, clears header `+14` mask
`01`, sets header byte `+2` to `FF`, debits payload length from the arena
counter selected by header `+16` and the optional category counter selected
by `+17`, then clears metadata at `+34/+1E/+17/+30/+3E`. These operations
assume a valid arena id and header indices; the body is not a comprehensive
validator for invented headers.

### Free-list ordering, coalescence and page indexing are connected

The new `0036ACE0/0036AE00` bodies search for following/preceding free blocks
using arena bitmap `+20`, qword pointer array `+28`, and free-list links
`+04/+08`. Under valid nonnegative within-arena addresses, buckets are 64 KiB
intervals relative to first header `+10`. This gives the previously initialized
arrays a concrete free-list search role.

The free routine first uses adjacent free physical blocks when available;
otherwise it chooses insertion through those searches. The already sealed
[EXP-078 helper bodies](../_experiments/evidence/arena-allocation-link-width/primary.json)
are reused, without rerunning the experiment. Complete `0036B670/0036B730`
explicitly decode and re-encode the free-list pairs. Their being unreached in
EXP-078 never made that static encoding unknown.

`0036B210/0036B2C0` coalesce only where free-list and physical adjacency agree.
The merged successor is passed to `0036C9D0` with EDX **1**, then its payload
length plus `40` is added to the retained block. Free ends `+90/+98` are
updated. `0036B5F0` refreshes the bucket representative and bitmap bit, while
`0036B2C0` clears or replaces a representative when its header is absorbed.
The representative comparison in `0036B5F0` uses low 32-bit pointer values;
full-width pointer storage must not erase that separate width constraint.

The [review receipt](../_experiments/evidence/resource-native-reclamation/review.json)
records four newly read complete bodies, six reused complete helper bodies,
their exact hashes and the diagnostic/control limits. No new native execution
or full campaign was needed to settle these branches. Focused requests
`ASTRA-REQ-*-NATIVE-RECLAMATION` route the render-cleanup distinction, page-index
role and `+3E` guard into owned prose/types/contracts. Mode-1 source ownership,
all instance cleanup effects, field producers, malformed-input bounds and
integrated runtime lifetime remain open. *(2026-09-30, SWE2-CONTRACT: see Limits item 8 and 9.)*

## Falsification pass 1 — 2026-09-12 (OPUS)

**passes: 1 · last_pass: 2026-09-12**

§15's relocation mechanism is the load-bearing claim here and the hardest to state correctly — a
32-bit delta, a fixed repair order, a deferred base write, and a sign-extension that decides which
width a value arrives in. **Every element of it reads back from the bytes exactly.**

### The repair order and the deferred write — `0024D970`, 73 bytes

```asm
0024D984  sub  ebx, dword ptr [rcx + 0x858]   ; delta32 — a 32-BIT subtract of a dword
0024D98F  call 003AA3D0                        ; the three helpers, in this order
0024D996  call 003A9BA0
0024D99D  call 003A9860
0024D9A7  mov  qword ptr [rdi + 0x858], rsi    ; the FULL qword base, written AFTER them
```

Four separate assertions — the delta's width, the three callees, their order, and that the base write
comes last — and all four hold. **The 32-bit `sub` against a 64-bit store in the same short function
is the whole point of the section**, and it is there in two instructions.

### The resolver's constants — `0036B130`, 41 bytes

| §15 says | image |
|---|---|
| requires at least `100000` unsigned | `0036B139 cmp ecx, 0x100000` |
| masks the slot address to `FFFFFFFC` | `0036B143 mov ecx, 0xfffffffc` |
| returns the full qword at slot `+8` … | `0036B14D mov rax, qword ptr [rax + 8]` |
| … plus `40` | `0036B151 add rax, 0x40` |

### The sign-extension that makes the width distinction real

§15 says the caller *"separately loads context dword `+860` using `MOVSXD`"*, which is why an untagged
`80002000` reaches the provider as `FFFFFFFF80002000`. It does: **`003B34F5 movsxd rcx, dword ptr
[rbx + 0x860]`**.

> **That one instruction is the reason the section's two entry boundaries must not be conflated**, and
> the document is right to insist on it: entering through the caller sign-extends, entering the
> provider directly does not, and the same stored value is therefore a different 64-bit number
> depending on which door it came through.

`audit_crossrefs.py` over this document: **0 findings** — every documented address resolves, every
body size matches, every cross-subsystem neighbour is accounted for.

**Not claimed:** nothing here re-runs the Unicorn probe or revisits its method-A/method-B split; the
list handlers §15 marks as not executed stay that way, and the frontier items in §15's closing
paragraphs are untouched.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `002FCCC0` | 562 | resource-release body on `[rdi+0x23]` byte + `[rdx+0x20]`/`+0x28`: `003AFFB0`, `0036C1D0`, `0024B270`, `0036C140` x2; callers `002EAD00`/`003B8670` |
| `003AEF90` | 655 | record-field mover between `rcx`/`rdi`/`rbx` records at `+0x10..0x48` (`[rbx+0x22]` byte keyed); single call `0020E600`; caller `003AF220` — bound as the move-queue fold: unlinks `word[+0x22]==0x16` nodes and accumulates `minss`-clamped floats ([the `0025DF00` subtree §13](../04-Actor-Entity/the-field-runtime-pass.md)) |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver / encoder fan-out is MECHANICAL.*

**The area unload `002628B0`, which this page cites, is a multi-layer teardown — SERVICE.** It calls `PartyControl_SetMovementSuppressionBit` and `PartyFocus_ClearCurrentActorIfEligible` (**Party**), six movement helpers (**Movement**), three small Audio-filed bodies (**Audio**), `CharacterRenderSystem_RefreshDistanceCullEna…` and three Presentation bodies (**Presentation**), and a 126-byte Input helper (**Input**).

- **CoreRuntimeScheduling — CLIENT and MECHANICAL.**
  - The arena initialiser `00369D30` (`"TKMALLOC EXECSPACE=%02d/START ADRS=%p"`) is run by the 978-byte boot initialiser.
  - `0024D540` is run by `MainLoop_UpdateAndRenderFrame` and by `0022B0B0` and `0022BC20` *(corrected 2026-10-02, OPUS: three direct callers, `0022B0B0+0xE1`, `0022B8C0+0x67` and `0022BC20+0x4F`; this line named one)*.
  - `0032E520` is run by boot modes 0 and 1 (255 B and 219 B).
  - The arena functions `0036A100` / `0036A1A0` / `0036A490` / `0036A570` / `0036ACE0` / `0036AE00` use the
    resolver / encoder pair, which is MECHANICAL.
- **Movement and Audio — SERVICE.** The 4,578-byte `003B8670` (`"sabf"`) calls seven movement bodies, including
  `Actor_SetFacingHeading_Variant0`, and three Audio-filed bodies (30–1,501 B). `0024D540` calls a 225-byte Audio body.
  The arena clients `0036B130` / `0036D170` / `00369800` include Audio bodies.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAction — CLIENT.** `FUN_002fc3c0`, owned by that layer, calls `0024F410` on this page. That caller is a 183-byte dispatcher: `byte[rec+0x23] & 0xF`, bounded to 7, into an eight-entry jump table *(anchors, re-read 2026-09-30 by SWE2-CONTRACT, b7 D1: the read `002FC3C6`, the mask and bound `002FC3CD` / `002FC3D0`, the RVA table (displacement `0x1DC478` from the image base, the bytes just past the body) read at `002FC3E2`, and the arm at `002FC442` that calls `0024F410`)*; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).
- **RNG_Random_Selection — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared RNG_Random_Selection plumbing (`RNG_MT19937_Seed` (00379CF0)) - the helpers' general call surface, not a RNG_Random_Selection relationship of this page's subjects.
- **Save_Load_Settings — CLIENT and SERVICE (2 edges).** 1 inbound (Save_Load_Settings bodies `002EF300` call page-cited `0032E620`); 1 outbound (page-cited `002628B0` call Save_Load_Settings bodies `SaveImage_GetPersistentPayloadBase` (002EF2B0)). Substantive edges include `0032E620` is called by `002EF300`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT and SERVICE (24 edges).** 19 inbound (Script_VM_Native_Bridge bodies `0050D8F0`, `0050DAD0`, `0050DF70` call page-cited `0032E520`, `0036C110`, `0036C1A0`); 5 outbound (page-cited `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) call Script_VM_Native_Bridge bodies `ScriptVM_WaitList_HasAnyActorChannelActive` (00267420), `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (002674B0), `00357760`). Substantive edges include `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `ScriptVM_WaitList_HasAnyActorChannelActive` (00267420); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `ScriptVM_WaitList_HasAnyActorResourceEntryActive` (002674B0); `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `00357760`; `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00) calls `00357770`; the remaining edges run through shared helpers the page cites.
- **UI — CLIENT (4 edges).** 4 inbound (UI bodies `003EF2E0`, `0024B9B0`, `00561390` call page-cited `003B29B0`, `0024D050`, `0024ED80`). Substantive edges include `0024D050` is called by `003EF2E0`; `0024ED80` is called by `0024B9B0`; `003B29B0` is called by `00561390`; `003B29B0` is called by `00558FB0`.
- **World — CLIENT and SERVICE (7 edges).** 6 inbound (World bodies `00378540` call page-cited `0032E400`, `0032E620`, `0036A190`); 1 outbound (page-cited `0022A0B0` call World bodies `00266D10`). Substantive edges include `0022A0B0` calls `00266D10`; `0032E400` is called by `00378540`; `0032E620` is called by `00378540`; `0036C110` is called by `00378540`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (43 edges).** 40 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0036C660`, `0036C110`, `0036C1A0`); 3 outbound (page-cited `002628B0` call WorldAreaField bodies `003DFA50`, `003EAA00`, `00378230`). Substantive edges include `002628B0` calls `003DFA50`; `002628B0` calls `003EAA00`; `002628B0` calls `00378230`; `0032E400` is called by `MapRef_BeginLoadResources` (00268750); the remaining edges run through shared helpers the page cites.
## The 01F83530 blind spot, closed (FABLE, 2026-09-16)

**THE BLIND SPOT IS NOW CLOSED - 2026-09-16 (FABLE), and *cannot be closed statically* does not follow from what the row says.** The row is unusually honest: it reports no writer **and** names the gap, *the same census the class registry page notes under-counts base-register access*. **That gap is testable, and it is empty.** **To write through a base register, something must first put the address in one.** In this image there are only three ways: take it with a rip-relative `lea`, load it from a place where it was stored as data, or compute it. The first two are measurable. **(1) Rip-relative accesses overlapping `01F83530`: exactly two, both reads, both in the resolvers themselves** - `0020E602` in `ImageAddress_ResolveRuntimePointer` (`add rax, qword ptr [01F83530]`) and `0020E620` in `RuntimePointer_EncodeImageAddress` (`sub ecx, dword ptr [01F83530]`). **Neither writes.** **(2) `lea` taking its address, over every listed body: ZERO.** Nothing anywhere in the image loads a pointer to this word. **(3) The address appears nowhere as data**: searched across every mapped section as a 64-bit VA, a 32-bit VA and a 32-bit RVA - **0, 0 and 0 occurrences.** So it cannot be loaded from a table either. **So no in-image code can obtain a pointer to `01F83530` at all**, which means the base-register shape the row worried about **cannot exist**. The static route is **exhausted, not blind**. **What is actually left is narrower and different.** A write would have to come from **outside the image** - another loaded module, an injected DLL, or a debugger - not from a path this census missed. That is still a runtime question, but it is *does anything outside the executable write it*, which is a far smaller claim than *cannot be closed statically*, and it matters for modding: **any mod that writes this word changes the resolved address for every `.ard`-family read at once.** *The one shape still outside the method.* A **computed** address - an anchor to some nearby global plus a delta, or two halves assembled - would leave no `lea` and no stored constant. I did not and cannot exclude it. **It is an unusual thing to do to a BSS word, and it is not excluded.** *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: this is Limits item 3; its runtime half is ASTRA's carrier `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`.)*

## The `0051EF90` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`0051EF90` (~208 B) — four-register body (`0051EF90`/`0051EFA0`).

| member | role | interior |
| --- | --- | --- |
| `0051EEB0` | `esi = edx` lifetime body (`0051EEBF`) | [`0051EEBF`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-70 update (2026-09-19) - `00369800` tagged-source release measured

`00369800` (85 B) measured - the page's tagged-source arm is exact: `ecx`
must carry a low tag bit (`cl & 3`) and a value `>= 0x100000`; it aligns
`ecx & ~3`, reads the owner at `[src+8]` first, runs `0036A9C0(src)`, and
when the owner is non-NULL tails `00369860(owner + 0x40, 0)` - the release
the untagged sibling `003697F0` pairs with.
Interior anchor `00369828` (the `0036A9C0` call).


## 20. Ownership from source entry to native disposal — SECTION-06 (2026-09-22)

The original functions now run together over synthetic arenas and input: entry mode0 copies into
owned backing, type3 borrows that backing, the parser mutates/publishes its interior, and matched
entry removal destroys context consumers before freeing the entry's owned backing. Mode1 removal
leaves external backing live. Copy-versus-borrow is a per-layer relation, not one global owner bit.
See the [current specification](the-resource-owner-from-copy-or-borrow-to-disposal.md) for exact
fields, operation order, 171 assertions, ten targeted mutants and remaining limits.

New execution also distinguishes original repeated tag/name lookup from source replacement: a
later equal key returns the existing entry without copying the new source contents. A direct
buffer resize does release old backing without fixing other objects' retained pointers; a separate
original driver repairs selected lookup entries after simulated source relocation. Context run
origin +870 remains stale even after its source base and lookup pointer are updated.

A structural correction closes the previously undecided 0x1C/0x20 buffer-extent question by a
producer write, not by tidy alignment: `0051EF73` and `0051EF76` store two 16-byte lanes into the
buffer descriptor. Its final four bytes are overwritten from a temporary whose corresponding
padding is not initialized in the reviewed body. The 0x20 transferred span is established; those
bytes' meaning or reproducible value is not. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: the parent's §8 records them as uninitialised padding, copied as opaque bytes.)* The parent's +2C is this embedded descriptor tail,
not a separately inferred control field. Per-row teardown is original `00409730`, even though
the bank-slot allocation itself is not freed per row.

## Limits (SWE2-CONTRACT, 2026-09-30)

Every "remains open" line in sections 1–20 is gathered here. Each is now either answered (the answer and its evidence
are cited), carried by a register row, or out of this note's scope (with the reason given). The checks marked `b7` are
in [`b7_lifetime.py`](../_index/candidates/swe2contract-ddres-b7-0930/b7_lifetime.py).

1. **SECTION-06 formal acceptance** (front matter, §20). **Carried.** This is a process item, not a knowledge question
   (class 2 of `_index/candidates/register-idless-boxes-0929/`). It is carried by the board request
   `SWE2CONTRACT-REQ-AUDITSPEC-SECTION06-ACCEPT-0930` to SWE2-AUDIT-SPEC.
   - SWE2-AUDIT-SPEC's OV acceptance batch (`FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929`) accepted OV-28 for the
     parent as SECTION-10. It byte-verified the SECTION-04/07/09/10 packages, not SECTION-06's.
2. **Where the backing is placed in other states** (§5, §8, §10, §11). **Register: BW-2, SUPERSEDED.** Nothing in the
   allocator guarantees a sub-4 GiB arena. The backing was observed low at two instants (EXP-079). Placement in other
   states is a live observation, not queued.
3. **The decoder base over the process lifetime** (§4, §6, §8). **Register: CD-2, SUPERSEDED** (J-C is superseded onto
   it).
   - The static route is exhausted: only the two converter reads name `01F83530`.
   - One in-image store route exists, the texture-id writer `00210570` with id `0xFFFB`, and the id producers never
     drive it.
   - The one live read left is the board request `OPUS-REQ-ASTRA-ARENA-BASE-AT-RUNTIME`. *(2026-10-01, SWE2-CONTRACT for OPUS, DD batch 18: still BLOCKED on the board, and ASTRA's queue parks it as live-only. It is ASTRA's existing runtime carrier, so batch 18 proposes no row for it.)*
4. **The selector map's lifetime, and "do not assume the identity map in every state"** (§7, §8, §10, §14, §17).
   **Answered.** The map `022D89A8` has exactly two rip-relative references, the LEAs in the identity fills `00369D30`
   and `0036A280`. The one instruction carrying its image displacement is the push's read `0036C272` (b7 M1; OPUS's
   SD-166 record, A2). So a logical source *n* selects arena *n* in every state, including sources 5, 6 and 8 in
   §7, §14 and §17.
5. **The settings byte's meaning** (§10). **Answered on the arena page.**
   [Where the game's memory comes from](../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
   ("The arena selection stack") reads `022D8E1C` as the arena allocator's fallback where a free-list record supplies no byte `+0x16`
   (`0036BD19`, `0036BD21`, `0036BD44`, `0036BD4F`; b7 G1 pins the first). It is pushed and popped by 18 functions.
   This note claims nothing beyond that page.
6. **The allocator's retry callback** (§3, "callback side effects and liveness remain unproved"). **Register: SD-164,
   ANSWERED** (OPUS `1f1defd7d`).
7. **Arena 7: writer, purpose and lifecycle** (§11, §13). Writer and purpose are **answered here**: §13 shows the boot
   backing is the EFX / resource load buffer of four bodies.
   - The lifecycle is **answered by OPUS's record** [`sd166-arena-7-0930`](../_index/candidates/sd166-arena-7-0930/README.md)
     (`b3f5172c9`; b7 A1). No shipped code path selects arena 7 for an allocation after boot: all 135 push sites are
     resolved, and shipped scripts never call the ~~two~~ four class-2 debug verbs (0x2003, 0x2004, 0x2008, 0x2009) (narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's review [`auditspec-review-sd166-0930`](../_index/candidates/auditspec-review-sd166-0930/REVIEW.md)).
   - ~~**Register: SD-166** still reads OPEN at HEAD. The row has not yet been updated with that answer, and that update
     is the register owner's. Until then this note stays PARTIAL on it.~~
     *Corrected 2026-10-01 (SWE2-CONTRACT for OPUS, DD batch 18)*: **Register: SD-166, ANSWERED**, restated by SWE2-DATA
     on OPUS's record (`06c849caf`; b18 R1). The note no longer stays PARTIAL on arena 7.
8. **Arbitrary and malformed sizes** (§3, §8, §17, §19). **Out of scope, with register pointers for the shipped part.**
   Behaviour on sizes or headers no shipped caller passes is a robustness property of invented input, not of the
   shipped mechanism. The shipped part is registered:
   - which callers test the allocator for null: **SD-165, ANSWERED** (OPUS `e87a83339`);
   - authored container bounds and copy-allocation failure: **OV-26, ANSWERED**.
9. **Storage, source and instance lifetime** (§8, §13, §14, §15, §16, §17, §18, §19). This covers survival through
   every native handler, repair of every retained reference, EFB storage ownership and mode-1 source ownership.
   **Owned by the parent**, which composes them (SECTION-06/07/08):
   - whole-schedule and reentrant safety for every consumer: **OV-24, SUPERSEDED** (a declared limit under the class-1
     ruling);
   - the external owner families and their release rules, which is where mode-1 ownership lands: **OV-25, ANSWERED**;
   - connecting further consumers only where original calls prove it: **OV-27, NOT A QUESTION**.
   - That the run origin `+870` stays stale after a move is the parent's finding in its §7; a move needs a separate
     refresh.
10. **Who sets the input-mode flag, and the live context** (§13, §14). The setter is **answered** in §14 and §16: the
    caller's template sets it, and of the six direct constructor callers only `0026FB90` and `003B38B0` set mask `04`.
    Which context produced EXP-079's arena-7 bytes is **out of scope**: it is a property of one past sample, and that
    sample did not capture the flag.
11. **The sibling front `005004C0`** (§14, "remains undecoded here"). **Answered.** It is the effect element's setup
    dispatcher. It switches on the definition byte `+0x44` (`0050050B`), bounded to `0xD1` (`00500510`), through a byte
    table and then a dword table (`0050051B`, `00500524`; b7 E1). Its 38 handlers are decoded in section 2.5 of
    [effect element type dispatch](../17-Presentation-Rendering/Effect-File-Formats/effect-element-type-dispatch.md).
12. **The eight step bodies behind `00442170`** (§14, "not read beyond their heads"). **Out of this note's scope.**
    They are the effect element's per-mode post-pass, a presentation step, catalogued on the same effect-dispatch page:
    the `00442170` entry names all eight, and seven have entries of their own (`00530E40` is named only in
    `00442170`'s). This note makes no lifetime claim about them.
13. **Caller scheduling of the relocation paths** (§15, §16, §18, "actual caller scheduling remains open").
    **Answered at the call level.**
    - The caller-side traversal `0024D540` is called only by the three main-loop frame functions `0022B0B0`,
      `0022B8C0` and `0022BC20`, so it runs from the frame.
    - The guarded check `003B3480` is reached only through the handle resolver `003B3C00`, which is called from
      `003B8670` and `00427DE0`.
    - `0024D970` is called only by `003B3480` and `003B3550` (b7 S1).
    - The frame-by-frame order of a move and its refresh is the parent's SECTION-07 mover.
14. **Header word `+3E`** (§12, §17, §18: "meaning remains open"; §19: "what could make it nonzero remains unknown").
    **Answered on the arena page** (OPUS, 2026-09-16). `+3E` is a guard word:
    - all 33 stores to it store zero, and both reads compare it with zero (the binder's `0036A270`, read for this
      note, is also a zero store);
    - so a nonzero value is not a state the manager produces, and the free routine treats it as corruption ("MCB
      broken").
    - Which overrun the guard is placed to catch is that page's open point, not this note's.
15. **The copied handle word and the tree's purpose** (§12, §17: "copied-word lifecycle remains open"). **Answered.**
    - Header `+1C` has one store in the arena code, `0036A517`, in the header writer `0036A490`. It stores the
      writer's fourth argument.
    - All seven callers of the header writer pass the arena's 16-bit counter `word [arena+0x60]`, which the allocation
      paths increment (`0036BC31`, `0036BFC5`, `0036C35B`, `0036C470`, `0036CE3E`). So each block header carries the
      arena's sequence number at the time it was written.
    - The binders copy it into slot `+6` (`0036A266`, `0036A36D`, `0036A45D`, `0036B005`). Tagged access compares the
      two (`0036A034` in `0036A000`, `0036D19A` in `0036D170`). The release path `00369800` does not compare them (§12).
    - All of this is b7 C1. That census covers the arena code range and register-plus-displacement forms only.
    - The tree's purpose is on the arena page: a handle-held block sits in its arena's size-ordered tree except while
      it is being accessed.
16. **The rebase's list handlers `00501420` / `00503F10`** (§15, "not executed or fully reviewed in this package").
    **Answered** in [the EFX source-rebase contract](CONTRACT-efx-source-rebase.md) §3–§4:
    - `003AA3D0` dispatches type `0x52` to `00501420` and type `0x56` to `00503F10`.
    - Both sign-extend the 32-bit delta (`movsxd`), so the signed-delta bound of Finding 11 holds on every path.
    - `00503F10` repairs a 32-bit offset field at `+0x10` by a round trip through the base.
    - [EXP-084](../_experiments/EXP-084-efx-source-rebase-execution.md) then executes the four walks with these real
      callees.

### Limits items 17–23, brought current 2026-10-01 (SWE2-CONTRACT for OPUS)

DD batch 18 read every remaining "remains open", "not established", "pending" and "unresolved" sentence in sections
1–20 against the items above, the register and the board. Each now carries a dated pointer, and seven needed an item of
their own. The checks marked `b18` are in
[`b18_checks.py`](../_index/candidates/swe2contract-ddres-b18-0930/b18_checks.py).

17. **The prefix tag at payload −0x22** (§2, "a universal 'line number' name for the field is not established").
    **Answered: it is a free-form 16-bit caller tag, and no code reads its value** (b18 T1–T5).
    - Both taggers store the low 16 bits of their third argument there, at header `+0x1E`: `0036C660` (a pointer) at
      `0036C6A0`, and `0036C6C0` (a tagged handle) at `0036C72C`.
    - What the 63 call sites of `0036C660` pass:
      - 25 pass a constant with a source-file basename from `0036C750` (`0xF3`–`0x16E6`, such as §2's `0x95C`);
      - 13 pass zero with a literal label (`MapNo`, `MapName`, `PCSkill` and others);
      - 3 pass a size with a label: `EVTMEM` `0x100000` (stored as 0), `SMNMEM` `0x19000` and `VOICEWK` `0x100`;
      - 22 pass a register or memory value, such as §2's loader id.
    - In the arena code the field is read five times. Four reads copy it into a header being rebuilt (`0036A309`,
      `0036BB61`, `0036CD0E`, `0036CF6B`). The fifth, in the report `0036A570` (`0036A6E0`), tests it against zero only to
      decide whether to print the block's seven-byte name. No other word access at payload −0x22 exists in the image's
      listed bodies (the one other hit is a stack slot). The free routine clears the field (`00369B3C`).
    - So "line number" is the convention of the 25 basename callers only. The field is a debug label kept beside the
      name.
    - Blind spots: the read census covers the arena code range `00369000..0036E000` and register-plus-displacement forms.
18. **Arena 11's backing replacement** (§7, `0037B3D0`, "prior teardown/helper effects are not established by this
    caller alone"). **Answered in FABLE's arena-residue record**
    ([`ov42-arena-residue-fable`](../_index/candidates/ov42-arena-residue-fable/README.md), `arena.py` T), re-pinned here
    (b18 A1–A3).
    - When the state byte changes, `0037B3D0` reports arena 11: `00369760` runs the report `0036A570` unless the arena is
      one whole free block. It then disables the arena (`0036D160`) and frees the old backing at `01FD4A18`, through
      `0036D250` → `0019C590` → IAT `008C2B48`, the CRT `free`.
    - Finally it allocates the new backing (`0036D240`), stores it at `01FD4A18` and re-initialises arena 11 with `0x100`
      slots.
    - So no block survives a replacement. An outstanding block is reported, and its memory goes with the backing.
19. **The area unload `002628B0`: its callees and its scheduling** (§10, "unreviewed callees and actual scheduling are
    not established by reading this body"). **Owned by the world-tick page.**
    [The world tick and the field frame](../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md) §3
    lists the unload's 26 exclusive helpers. Its box EX-9 (ANSWERED) covers the request mask that drives the unload.
    - Statically, `002628B0` has two direct callers: the manager-request drain `0025BFB0` (at `0025C036`) and
      `0032FCA0` (at `0032FCF6`) (b18 U1).
    - The drain is called only by the simulation tick `00314020` (at `00314078`), before the tick's first mode test, so
      it runs in every frame mode (b18 U2; the world-tick contract's drain-first rule).
    - How often an area unload happens is a property of play: once per area change. This note makes no timing claim.
20. **The `0x800` / `0xA00` table ids against capacity** (§14, "authored/admission bounds remain a separate question"
    and "admission bounds"). **Answered over the shipped data** (b18 B1–B5).
    - The tables hold 320 slots (`003A9560` allocates `0xA00` bytes, for `0x800`) and 768 slots (`003A9920`, `0x1800`
      bytes, for `0xA00`). Each registrar reads the id word at chunk `+0xC` and stores without a bound.
    - The walk covers every EFX stream in the extract: 4,229 streams, with 53,351 `0x800` and 48,868 `0xA00` chunks,
      the counts `type_census.py` publishes. The largest ids are 296 and 722, both in `c_all.efx` (`jp`).
    - No chunk uses id 0, the slot the teardown and the rebase skip, and no id repeats within a stream.
    - So no shipped stream overruns a table or overwrites a slot. The missing bound matters only for a file the game
      does not ship.
21. **The `+0x282` subtype, and the fallback `003EE2D0`** (§14, "which subtype values correspond to which authored
    element types is not established"; §13, "remains a separate unreviewed consumer").
    - **Answered by FABLE's OV-41 record** ([`ov41-efx-children-fable`](../_index/candidates/ov41-efx-children-fable/README.md);
      register OV-41, ANSWERED). `+0x282` is the `0x800` family's own subtype byte, chunk `+0xE`, which `003A9730`
      copies at `003A974F` (b18 B2). The `0xA00` element type is a different byte, record `+0x44`.
    - So the two do not correspond. The `0x800` family has nine setup arms for subtypes 0–8, and every shipped `0x800`
      chunk stays within 0–8 (b18 B6).
    - **`003EE2D0` is read on the parent**, as the walker's four-way record dispatch (b18 P1).
22. **`0024D050`, the second traversal** (§16, "their call frequency and all intervening native effects remain
    unestablished"). **Answered at the call level** (b18 G1–G5).
    - It has one direct caller and no other reference: `003EF2E0`, at `003EF419`. That function is a task callback.
      Its address is taken once, by the game-over widget `003EF830`, and handed to the task registrar `00244F50`. The
      widget names the game-over layout and image (`00D11C88` / `00D11CA0`; b15 P1).
    - The task calls `00363560` and then `0024D050` once, when its countdown `+0xC8` reaches zero. So the ten-list
      traversal runs on the game-over screen, not every frame. The frame traversal is `0024D540` (item 13).
    - For each instance it binds the context, calls `0024FCF0` and runs `003A7420`, which calls the slot teardown
      `00332FA0` on each of the instance's sixteen `+0x130` slots.
    - None of these bodies calls a release front directly (`003697F0`, `00369800`, `00369860` or the CRT `free`), so
      the traversal frees no storage. Deeper callees are call boundaries.
23. **Peer review, propagation and the routed corrections** (§6, §8, §9 to §19: "consumer review", "propagation" and
    "correction … pending"). **Closed on the board.** All 28 requests these sections route are DONE (b18 Q1, read from
    `TEAM.json`). The two board items still open are item 1's SECTION-06 acceptance (READY) and item 3's base read
    (BLOCKED, ASTRA's live-only carrier).
