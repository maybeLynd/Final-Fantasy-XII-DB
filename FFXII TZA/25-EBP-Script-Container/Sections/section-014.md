---
system: EBP section_014 — the LGT2 lighting block
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Actor.ResourceAuxiliaryTable
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "1115 / 1115 us .ebp scripts, 2026-09-03 (1114 containers; section_014 in 140)"
last_reviewed: 2026-09-12
ebp_units:
  - "section_014"
audit:
  passes: 2
  last_pass: 2026-09-04
  last_pass_state: GN160-repos-c9-falsification-2-after-reopen
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 1
---

# EBP `section_014` — the `LGT2` lighting block

> Per-map authored lighting: a fixed-stride array of light records plus a tagged chunk list, bound
> into one of five manager slots by `FUN_0037aa90`, which validates the `LGT2` magic and **rewrites
> two bytes of every light record in place** as it binds.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 containers; one file is not a container) |
| this unit present in | **140 (12.6 %)** |
| co-occurrence | **always with `section_008` and `section_009` — 140 of 140.** Also with `000` (140), `002` (137), `012` (138). Never observed with `003`, `004`, `016` or `019` in any of the 140. |
| size range | **64 B – 34,304 B, median 3,712 B**, 89 distinct sizes, every one a multiple of 16 |

`section_014` is a **strict subset of the `008`/`009` pair**: every file that has `014` has both,
while 423 files have the pair without `014`. That is a one-way implication, not a pair — a different
shape of fact from the `008`/`009` and `010`/`011` pairs, and it should not be filed with them.

---

## 1. What the player sees

**The lighting of a field map** — how bright an area is, what colour the ambient is, where the local
lights sit. Nothing here is an object the player can walk up to; it is the reason one room reads as
torchlit and the next as daylight.

One detail *is* directly visible and is decided here rather than by the renderer: **the loader
rewrites a per-light byte through a six-entry translation table on load, and for manager slot 0 it
additionally sets bit `0x20` in a second per-light byte** (§3). Two maps with byte-identical
`section_014` payloads can therefore light differently depending on which slot they are bound into.

## 2. The layout

Offsets from the **start of the section body**, which is where the container directory's slot-14
offset points. All fields little-endian.

```
+0x00  char[4]  magic        'LGT2'  (0x3254474C as a dword)   -- 140/140
+0x04  u16      listOffset   offset of the chunk list, from section start
+0x06  u16      0                                              -- 140/140
+0x08  u16      1                                              -- 139/140 (one file: 2)
+0x0A  u16      lightCount   number of 0x70-byte light records -- 0 .. 287
+0x0C  u32      0                                              -- 140/140
+0x10  <lightCount * 0x70 bytes>   the light records
[listOffset]    the chunk list (below)
```

**`listOffset` is exactly `0x10 + lightCount * 0x70` in 140 of 140 files** — the chunk list begins
immediately after the light array. The array stride `0x70` is not stored anywhere; it is fixed in
the code (§3).

**`+0x04` is read as a `u16`, not a `u32`** — `MOVZX EDI, word ptr [R13 + 0x4]` at `0037AAE7`.
The upper half is `0` in all 140 files, so no shipped file distinguishes the two readings; the
instruction does. A section whose light array exceeded 64 KiB would be misparsed, and the largest
shipped `section_014` is 34,304 B, so the corpus never approaches the limit.

### The chunk list

A self-sizing list, walked to a terminator:

```
+0x00  u16  size    total bytes of this chunk, including this header; 0 terminates the list
+0x02  u16  type    0 .. 7 are dispatched; anything else is skipped
+0x04  ...  payload (type-dependent; type 2 and type 5 payloads are described in section 3)
```

Measured over all 140 files by executing exactly the walk the loader performs
(`p += *(u16 *)p` until `*(u16 *)p == 0`): **0 violations** — every list terminates inside the
section, none runs past the end, none loops. Chunks per file: 4 in 137 files, 5 in 2, 3 in 1.

Chunk sizes range 8 B – 1,164 B and are always a multiple of 4.

**Chunk types actually authored**, over all 140 files:

| type | occurrences | dispatched by the loader? |
|---:|---:|---|
| 0 | 2 | yes |
| 1 | **0** | yes — handler exists, nothing uses it |
| 2 | 139 | yes |
| 3 | 140 | yes |
| 4 | **0** | **no — the jump table sends it to the default arm** |
| 5 | 140 | yes |
| 6 | 140 | yes |
| 7 | **0** | yes — handler exists, nothing uses it |

Types `3`, `5` and `6` are in **every** file that has the section; `2` in 139 of 140.

## 3. The loader contract

`FUN_0037aa90`, body sha256 `41fd91bc1b4f904868638338ca3b55761b0575a66e123b79ae8935284bafe7c0`,
signature `(void *section, unsigned slot)`.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `slot` (argument, not a field) | `0037AA9E` `CMP R12D,0x4` / `JA` | — | — | **out of range ≥ 5 → the whole call is a silent no-op**; not even the ready flag is set |
| `+0x00` magic | `0037AABF` `CMP dword ptr [RCX],0x3254474C` | mismatch → **nothing is bound**, but see the trap below | — | — |
| `+0x04` `listOffset` | `0037AAE7` `MOVZX EDI,word ptr [R13+0x4]` (**u16**) | — | — | upper 16 bits **never read** |
| `+0x06` | — | — | — | **yes — no read found by a full-body instruction walk of `FUN_0037aa90`** |
| `+0x08` | — | — | — | **yes — same method.** It is `1` in 139 files and `2` in one, and nothing in this loader looks at it |
| `+0x0A` `lightCount` | `0037AC03` onward, twice | — | — | — |
| `+0x0C` | — | — | — | **yes — same method** |
| chunk `+0x00` size | the walk itself | `0` terminates the list | — | — |
| chunk `+0x02` type | `0037AB10`–`0037AB28`, jump table at `0037AC7C` | — | — | `> 7` and `== 4` are **skipped, not rejected**; the walk continues by `size` |

### What binding actually does

The destination is a **five-slot table of `0x50`-byte records at `02EBF420`**, addressed
`02EBF420 + slot * 0x50` (`LEA RAX,[0x2ebf420]` at `0037AAAD`, then
`LEA RBX,[R12 + R12*4]` / `SHL RBX,0x4` — i.e. `slot * 80`). `FUN_0037b230(slot)` is called first,
at `0037AAD8`, before anything is stored.

| slot record offset | receives |
|---|---|
| `+0x00` | the section base pointer |
| `+0x08` | first chunk of type **0** |
| `+0x10` | first chunk of type **1** |
| `+0x18` | first chunk of type **2** |
| `+0x20` | first chunk of type **3** |
| `+0x28` | first chunk of type **6** |
| `+0x30` | first chunk of type **7** |
| `+0x38` | type **5** chunk **+ 8** — the payload, not the chunk header |
| `+0x4C` | `1` — see the trap below |

**The stored chunk pointers point into the loaded file buffer.** Nothing is copied out, so the
section body must stay resident for as long as the slot is bound.

### The trap: `+0x4C` is set even when the magic is rejected

`MOV byte ptr [RBX + 0x4c],0x1` at `0037AC69` sits **outside** the magic test and inside the
`slot < 5` test. So a `section_014` whose magic is corrupted produces a slot that is **marked ready
while every pointer in it still refers to the previously bound map's lighting**. It is not a crash
and not a visible rejection; it is a stale bind. This is the single most important thing on this
page for anyone editing the section.

The only true rejection is `slot >= 5`, which returns without touching anything at all.

### What loading normalises — the loader writes to the file buffer

Three separate in-place mutations, all after a successful magic check:

1. **Per-light byte remap.** For `i` in `[0, lightCount)`, the byte at
   `section + 0x31 + i * 0x70` — i.e. **`+0x21` of each light record** — is replaced by
   `DAT_01ef94e4[value]` **when `value < 6`**. Values `>= 6` are left untouched. So `+0x21` is a
   six-entry enumeration translated through a runtime table, and a value outside that range passes
   through unchanged rather than being clamped.
2. **Slot-0 flag.** *Only when `slot == 0`*, the byte at `section + 0x37 + i * 0x70` — **`+0x27` of
   each light record** — gets `|= 0x20`. Four other slots exist and none of them does this.
3. **Type-5 pointer encoding.** For each of the `*(u32 *)(chunk + 4)` sub-entries, the loader walks
   a secondary list beginning at `chunk + (count + 2) * 4`, each sub-entry advancing by its own
   leading `u32` size, and writes `RuntimePointer_EncodeImageAddress(subEntry)` as a 4-byte value
   into the array at `slotRecord[+0x38]`. **The type-5 payload is rewritten from file contents into
   encoded runtime addresses.**

Consequence for modders: **`section_014` is not a read-only resource.** Anything that hashes or
re-reads the buffer after `FUN_0037aa90` has run sees different bytes than the file on disk.

### Type 2 is conditional on a global

`case 2` stores the chunk pointer unconditionally, then — **only if `DAT_01ef94e0 != 0`** — zeroes
the byte at `+0x12` of each of `*(u32 *)(chunk + 4)` sub-entries at stride 8, and calls
`FUN_0037a9b0(slot, 0)`. With that global clear, the type-2 payload is bound and never initialised.
`DAT_01ef94e0` is referenced from exactly three instructions — `00379B1C` (`LEA R11,[rip+…]`),
`0037AA80` (`MOV dword ptr [rip+…],ECX`) and `0037AB3C` (`CMP dword ptr [rip+…],R15D`).

**The remap table at `01EF94E4` has zero direct references**, and that is a finding rather than a
gap: it is reached by *indexing off* `01EF94E0`, because x86-64 has no RIP-relative addressing with
an index register — the code must materialise the block base in a register first, which is what the
`LEA R11` at `00379B1C` does. So the two are **one runtime configuration block addressed through one
base**, which is a stronger statement than "adjacent and referenced from the same sites", and it is
the one the instruction encoding actually supports.

### The write path

**None found.** No caller of `FUN_0037aa90` writes a `LGT2` block, and `.lgt` ships zero times
(section 5). Nothing in this build authors `section_014`; it is produced offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0037AA90` | `FUN_0037aa90` — the `LGT2` binder | ✅ full body |
| `0037AABF` | the magic compare `CMP dword ptr [RCX],0x3254474C` | ✅ |
| `0037AAAD` | `LEA RAX,[0x2ebf420]` — the bind table base | ✅ |
| `0037AAE7` | `listOffset` read as a **u16** | ✅ |
| `0037AB28` | `JMP RCX` — the chunk-type dispatch | ✅ |
| `0037AC7C` | the 8-entry jump table (image-base-relative offsets) | ✅ |
| `0037AC69` | `MOV byte ptr [RBX+0x4C],1` — the ready flag, set on the reject path too | ✅ |
| `0037AC03` | start of the per-light `+0x21` remap loop | ✅ |
| `02EBF420` | the five-slot × `0x50` bind table | ✅ (RIP-relative from 25 sites) |
| `01EF94E0` | the type-2 enable global, and the base the remap table is indexed from | ✅ `00379B1C`, `0037AA80`, `0037AB3C` — decoded, not inferred |
| `01EF94E4` | the 6-entry `+0x21` translation table | ✅ reached by indexing off `01EF94E0`; **0 direct references**, see §3 |
| `0032F1B0` | `ActorResource_FinalizeManagerRuntimeAfterLoads` — calls the binder | ✅ full listing |
| `0032F1C9` | `LEA RDI,[0x22C6E20]` — the per-slot source-pointer table | ✅ |
| `0032F1F2` | `JZ` — a null source pointer skips the bind entirely | ✅ |
| `0032F1F9` | `CALL 0037AA90` | ✅ |
| `00330110` | `FUN_00330110` — the `LGTDAT` stream-completion callback | ⚠️ entry and its write to `022C6E20` only |
| `00330144` | that write, found as the image-base-relative dword `021A6E20` | ✅ |
| `00331555` | `LEA RCX,[00D10958]` — `"..\..\katano\atelload.c"` as the allocation tag | ✅ |
| `0033156E` | `MOV R8D,0x8B8` — `atelload.c` line 2232 | ✅ |
| `00331587` | `LEA RDX,[00D10A04]` — `"LGTDAT"` names the allocation | ✅ |
| `003315BA` | `LEA RAX,[00330110]` — the completion callback | ✅ |
| `003315DB` | `OR qword ptr [RDI],0x10000` — the `LGTDAT` pending-resource bit | ✅ |
| `003775D0` | `FUN_003775d0` — the second binder caller (site `003776A6`) | ❌ not read |
| `0037B230` | slot reset, called before binding | ❌ not read |
| `0037A9B0` | type-2 initialiser | ❌ not read |

### Disposition of `verify_doc_addresses.py`'s three `REVIEW` addresses

The gate reports three `.text` addresses in this sheet that are not function entries and asks for
context. **All three are dispositioned; none is a citation error.**

| address | what it is | why it is not a function |
|---|---|---|
| `003306DA` | the **end** of `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` | a body-extent boundary, not an instruction to cite. `003304A0 + 570 = 003306DA`, followed by exactly six `CC` bytes before `FUN_003306E0` |
| `0037AC7C` | the 8-entry **jump table** for the chunk-type switch | data emitted after the function body. Verified: its eight dwords resolve to `0037AB2A`, `0037AB33`, `0037AB3C`, `0037AB8B`, `0037ABE4`, `0037AB97`, `0037AB91`, `0037ABE0` — exactly the case arms in §2 |
| `0037AA7F` | an `INT3` padding byte | **named deliberately, as the wrong address**, in the correction record below. The gate cannot distinguish a citation from a correction trail, and the trail has to name what was wrong |

*Recorded because a flagged finding that is merely "known to be fine" is undispositioned until
somebody writes down why.*

### The chain, end to end — corrected 2026-09-04

**The live route is the container directory, not a filename.** `section_014` is slot 14 of the
`EBP2` directory, and the whole flow lives inside one dispatcher:

```
ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources   003304A0
  0033066B  TEST EBX,EBX ; JE            ; manager 0 -> slot 14 skipped entirely
  00330674  CMP dword ptr [RDI+4],0xE    ; slotCount > 14
  0033067A  MOV EAX,[RDI+0x48]           ; slot 14's offset; 0 -> absent
  00330681  ADD RAX,RDI                  ; file base + offset
  00330686  OR EAX,EBX                   ; pack the manager index into the low nibble
  0033068A  CALL FUN_00330110
        |
        v
FUN_00330110   (122 bytes)
  00330123  AND EBX,0xF                  ; recover the manager index
  0033012B  AND RAX,0xFFFFFFF0           ; recover the section pointer
  00330140  MOV [rcx + rbx*8 + 0x21A6E20],RAX   ; 022C6E20[mgr] = section
  00330148  BTR RDI,0x10                 ; clear pending bit 16
  0033014D  MOV [rcx + rbx*8 + 0x21A6E48],RDI   ; 022C6E48[mgr] = mask
  00330169  TEST RSI,RSI ; JE            ; only when the mask has just drained to 0
  00330175  CALL 0032F1B0
        |
        v
ActorResource_FinalizeManagerRuntimeAfterLoads (0032F1B0)
  0032F1C9  LEA RDI,[022C6E20] ; MOV RDI,[RDI + RBX*8]
  0032F1F2  JZ ...                       ; null pointer -> skip: no bind, no flag
  0032F1F9  CALL FUN_0037aa90(ptr, mgr)
```

**`022C6E20` and `022C6E48` are two per-manager arrays indexed identically**, `base + mgr*8`,
and they sit back to back: five 8-byte entries from `022C6E20` end at `022C6E48`, where the
pending-mask array begins. The five pointer entries and the five bind slots of `FUN_0037aa90` are
therefore the same five, and the `slot` argument is the **manager index**, not a section index.

**`FUN_0037aa90` runs only when the manager's whole pending-resource mask reaches zero** — the
finalizer is called from `FUN_00330110` at `00330175`, and from the dispatcher's own tail at
`003306BF`, in both cases only on the transition to an empty mask. Binding is therefore not
per-section-arrival; it is a barrier across every resource the manager is waiting for.

### Correction — the `LGTDAT` filename route is the dead one

**What was believed** (this sheet, 2026-09-03): that `section_014` reached `022C6E20` through the
`LGTDAT` registration in `FUN_003306e0` — `00331555` tags an allocation with
`"..\..\katano\atelload.c"` and `atelload.c` line `0x8B8`, `00331587` names it `"LGTDAT"`,
`003315BA` installs `FUN_00330110` as the completion callback, `003315D6` enqueues a streamed
read and `003315DB` sets pending bit `0x10000`. The sheet flagged the contradiction honestly —
`/lgt/` occurs 0 times in the 89,414-entry archive index — and left it unresolved.

**What is now believed:** both routes exist and reach the same function, and **the container route is
the live one.** `FUN_00330110` is simultaneously the `EBP2` slot-14 handler and the `LGTDAT` stream
callback. The filename route builds `.../lgt/...` via `FUN_0032F6F0(buf, "camera", "lgt")` at
`00330AE9`, the size probe fails because the directory does not ship, and the branch is skipped.

**What proved it:** the dispatcher body at `003304A0`, disassembled independently with capstone
(not Ghidra) — `CALL 0x330110` at `0033068A`, guarded by `CMP [RDI+4],0xE` and the slot-14 offset
at `[RDI+0x48]`. Independently, `FUN_00330110` clears pending **bit 16**, the same bit the `LGTDAT`
registration sets with `OR ...,0x10000`, which is what ties the two routes to one function.

**Why the earlier reading was reachable:** the filename route is the only one that *names* the
section — `"LGTDAT"` is a string, `slot 14` is an offset in a table. A search that starts from names
finds the legacy path first and never sees the live one. The general lesson is in §6.

**This is not unique to `section_014`.** The same two-route shape holds for `section_019`, whose
stream callback `FUN_003320D0` is also its container slot-19 handler, and the same dead-directory
measurement applies. See `Sections/section-019.md`.

## 5. Corpus survey

**Invariants over all 140 files** — each checked on the whole population, not on one file:

| | |
|---|---|
| `+0x00` magic `LGT2` | 140 / 140 |
| `+0x04 == 0x10 + lightCount * 0x70` | **140 / 140** |
| `+0x04` upper 16 bits `0` | 140 / 140 |
| `+0x06 == 0` | 140 / 140 |
| `+0x0C == 0` | 140 / 140 |
| chunk walk terminates inside the section | **140 / 140, 0 violations** |
| section length a multiple of 16 | 140 / 140 |

What varies: `lightCount` `0 .. 287` across 72 distinct values; chunk sizes across 84 distinct
values; section length across 89.

**Outliers, each worth its own line:**

- **One file has `+0x08 == 2`** where the other 139 have `1`. Nothing in `FUN_0037aa90` reads the
  field, so this is a difference the shipped loader cannot act on.
- **`lightCount == 0` occurs.** The smallest section is 64 B and consists of magic, header and a
  three-chunk list with no lights at all.
- **Type `0` chunks occur in only 2 files.** Types `1` and `7` have handlers and **zero**
  occurrences in 140 files; type `4` has neither.

**`.lgt` ships zero times.** The archive index (`Tools/work/repos-2d/vbf_list.txt`, 89,414 entries,
48 distinct extensions) contains no `lgt` extension, and the directory component `/lgt/` occurs
**0** times in it. `section_014` inside the `.ebp` container is the only form of this data that
ships.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is `+0x04` relative to the file or the section? | **Section.** `ADD RDI,R13` at `0037AAEF` adds it to the section base held in `R13`, which was `RCX`, the first argument. The container's own directory offset never enters this function. |
| Does the `0x10 + n*0x70` relation hold on the whole corpus, or on the file I opened? | **All 140.** Checked by computation over every file; a mismatch would have printed. |
| Is the chunk list really self-sizing, or was the stride inferred from one file? | Executed the loader's exact walk on all 140 files: 0 runaways, 0 overruns. A fixed stride would have failed immediately — chunk sizes take 84 distinct values. |
| Could the decompiler have invented the `+0x21` remap? | **No.** It appears in the disassembly as an explicit loop from `0037AC03` with the `< 6` test and the `0x70` stride. I read the listing because the decompiled C for the *caller* proved unreliable — Ghidra rendered `ActorResource_FinalizeManagerRuntimeAfterLoads` with two calls where the listing has eight, and the call to `FUN_0037aa90` was not among them. **Every address cited here comes from the listing.** |
| Is `+0x4C` really set on the reject path, or is that a misread branch? | The magic `JNZ` at `0037AAC5` targets `0037AC69`, and `0037AC69` **is** the `MOV byte ptr [RBX+0x4C],1`. The success path falls through to the same instruction. Both readings agree: it is set either way. |
| Are types 1, 4 and 7 unused, or did the walk miss them? | The walk enumerated 561 chunks across 140 files and found types 0/2/3/5/6 only. Type 4 additionally has no jump-table arm. **"Never authored in the `us` corpus"** is the claim; another language's scripts are not evidence I have. |
| If an external tool agrees, was it consulted before or after? | **`ff12-script` was not consulted at all for this section.** It decompiles `section_000` bytecode and does not read `LGT2`. Nothing here rests on it, so nothing here is tier 6. |
| Could `02EBF420` be something else that merely happens to be 5 × `0x50`? | The independent corroboration is `022C6E20`, a *different* table, also five entries, whose consumer passes the index straight into the `slot < 5` test. Two unrelated tables agreeing on five is the check. |

**What I tried that failed to break it.** I looked for a second writer of the `+0x21` byte that
would make the remap redundant, scanning `.text` for **both** the RIP-relative and the
image-base-relative encodings of `01EF94E4`. Both scans return the same three sites, all inside
this module. The remap has no competitor.

## 6b. Second falsification pass — 2026-09-04, after reopen

Reopened under trigger 7 (an open question closed in a way that touches the document) and trigger 1
(`0032F1B0`, cited here, gained a caller at `003306BF` in a function this sheet did not mention).
Program state: GN160, `fa0db293…d2f708`, unchanged.

| attack | result |
|---|---|
| Was the 2026-09-03 chain wrong, or merely incomplete? | **Incomplete, not wrong.** Every address it cited still resolves and still does what was claimed; the `LGTDAT` registration really does install `FUN_00330110` and really does set bit `0x10000`. What was missing is that the *same* function is also the container's slot-14 handler. Recorded as a correction rather than a rewrite, per the standing rule. |
| Does the container route actually reach `FUN_0037aa90`, or only look like it? | Traced instruction by instruction with capstone: `0033068A CALL 0x330110` → `00330140` stores the pointer → `00330175 CALL 0x32F1B0` → `0032F1F9 CALL 0x37AA90`. No branch in that path depends on anything but the pending mask and null checks. |
| Is `022C6E48` really an array, or one qword that Ghidra resolved for one path? | **An array.** `MOV [rcx + rbx*8 + 0x21A6E48],RDI` at `0033014D` is indexed by `rbx`, the manager index. The 2026-09-03 sheet described it as "the next qword after a five-entry array", which reached the right conclusion by a weaker argument; the indexed form is the actual evidence and now replaces it. |
| Does the magic-reject trap still hold after re-derivation? | Yes — re-checked in the disassembly. `0037AAC5 JNZ 0037AC69` and `0037AC69` is the `MOV byte ptr [RBX+0x4C],1`, still outside the magic test. |
| Do the corpus invariants still reproduce? | Re-run 2026-09-04 against all 1,115 files from the raw containers: 140 sections, `+0x04 == 0x10 + lightCount*0x70` in 140/140, chunk walk 0 violations. Unchanged. |
| Did any banned evidence enter through the new citations? | No `.pdata`/`.xdata`/unwind/EH reasoning is used. Function extents came from disassembly terminating at `ret` followed by `CC` padding, and the 570-byte extent of `003304A0` was confirmed that way rather than from an unwind record. |

**What I tried that failed to break it.** I disassembled `003304A0` linearly for 600 bytes and got
597, which would have contradicted the container sheet's stated 570. It does not: the sweep ran past
the function into `FUN_003306E0`. Bounding it at 570 disassembles cleanly to `003306DA` followed by
exactly six `CC` bytes. **The instrument was wrong, not the document** — and a linear sweep with no
terminator rule is exactly the kind of thing that manufactures a false discrepancy.

### Correction — a cited address was off by one byte

**What was believed** (2026-09-03 and the first correction of 2026-09-04): that `01EF94E0` and
`01EF94E4` were each referenced from three sites, one of them `0037AA7F`.

**What is now believed:** the three sites reference `01EF94E0` only, and the middle one is at
**`0037AA80`, not `0037AA7F`**. `0037AA7F` is an `INT3` padding byte and is not an instruction at
all.

**What proved it:** `verify_doc_addresses.py` flagged `0037AA7F` as a `.text` non-function address;
disassembling `0037AA60`–`0037AA95` shows `0037AA7E RET`, `0037AA7F INT3`, then
`0037AA80 MOV dword ptr [rip + 0x1b7ea5a],ECX`, whose target resolves to `01EF94E0` exactly.

**Why the earlier reading was reachable, and this is the part worth keeping:** the address came from
a displacement scan that reported the *disp32 position minus 3* as the instruction start. That
guess is right for the 3-byte-prefix forms (`LEA r64,[rip+d32]`, `CMP dword ptr [rip+d32],r32`) and
wrong for `MOV dword ptr [rip+d32],r32`, which is `89 0D` + disp32 — only two bytes. **A fixed
back-off is not instruction decoding**, and the one place it differs is the one place it was wrong.
Every address in this sheet has since been re-derived by decoding from the byte stream.

**And the gate could only catch it after the citation format changed.** While this sheet wrote
addresses as `0x0037AA7F`, `verify_doc_addresses.py` matched **zero** citations in it and reported
`ok`. The defect was present the whole time and the instrument was structurally unable to see it.
See the inbox report for the corpus-wide extent of that.

**A method note worth carrying.** A RIP-relative displacement scan alone is not a complete xref
search in this binary: `022C6E20` has **1** RIP-relative reference and **5** image-base-relative
ones (the code materialises `0x00120000` in a register and indexes off it), while `02EBF420` has
**25** RIP-relative and **0** image-base-relative. Neither scan alone finds both tables. This is the
"displacement search stops counting where a base pointer starts" blind spot in `COVERAGE.md`,
observed live. *(Credit: `repos-c7` raised the image-base-relative form independently; the
measurement above is mine and refines it — both encodings are in use and both scans are needed.)*

## 7. What this document does not claim

- **The light record itself is not decoded.** `0x70` bytes × up to 287 per file, and this sheet
  names exactly two bytes in it — `+0x21` and `+0x27` — because those are the two the loader
  touches. The other 110 bytes are read by the renderer, not by `FUN_0037aa90`, and that code is not
  read here.
- **The type-3 and type-6 payloads are not decoded.** They are in every file, and the loader only
  stores a pointer to each. Their consumers are among the functions in the `0x00379xxx`–`0x0037Axxx`
  range that read `02EBF420`, none of which is read here.
- **`FUN_00330110` is now read in full** (122 bytes, §4) — that item is closed.
- **How a `section_014` body reaches `022C6E20` is now established** and is written up above; the
  open question is closed. What remains open is narrower: `FUN_003DCF10`-style consumers of the
  bound chunk pointers are still unread, and *which* manager index a given map gets is not
  established here.
- **The `slot == 0` branch may be unreachable through the container route.** `FUN_0037aa90` sets
  `|= 0x20` on every light record when `slot == 0`, but the dispatcher **skips slot 14 entirely for
  manager 0** (`0033066B TEST EBX,EBX ; JE`). So on the `EBP2` path that branch never runs. It is
  reachable only if `FUN_003775d0` passes 0, and that caller is unread — so the branch is **not**
  claimed dead, only shown to be unreachable by the one route this sheet establishes.
  > **CD-1 answered 2026-09-12 (FABLE): the branch is live, on the lighting-set route.**
  > `003775D0` is read: it calls `0037AA90(rcx = [02ADD090], edx = 0)` at `003776A6` — manager slot
  > **0** — whenever the lighting flag word `02ADD0F0` has **bit 8** set (`00377697 bt eax, 8`), after
  > clearing bit 4 (`0037768E`). `003775D0` has one caller, the lighting-set loader `00378BC0`
  > (`00378F39`), and that loader sets bit 8 exactly when the block it stores at `02ADD090` is
  > non-null (`00378EB9`–`00378ED6`: `mov [02ADD090], rcx ; test rcx ; bts r8d, 8`), beside bit 7 for
  > the `02ADD060` block and bit 4 for `02ADD0B8`. `00378BC0` itself has no `E8`/`E9` caller — it is
  > entered through a relative dispatch table whose entries at `01D7BC70` / `01D7BCA4` carry its RVA —
  > so the route is: lighting-set load → `00378BC0` fills the per-slot blocks and flags → `003775D0`
  > binds the `02ADD090` block into manager slot 0 → `0037AA90`'s `slot == 0` arm ORs `0x20` into every
  > light record of that block. The `EBP2` route indeed never reaches it; the lighting-set route
  > does, whenever that block loads. Which authored file fills `02ADD090` is the residue.
  >
  > **Residue answered and two words corrected, 2026-09-12 (FABLE):** `02ADD090` is **slot 17 of the
  > map's `.mpk` pack** (`LGT2` in 212 of 550 packs), stored by `00378BC0`, which is **not a lighting-set
  > loader and not table-dispatched**: it is the completion routine of the map-pack load, installed as
  > the request's callback by `00378030` (`003780B1 lea rax, [00378BC0]`). The two `.rdata` records at
  > `01D7BC70` / `01D7BCA4` that carry its RVA are begin/end/unwind triples (`0x258BC0`, `0x258C14`,
  > `0x1C5BC50`) — exception metadata, not callers. The route is therefore: field load `00331990` →
  > `00378A60` → pack completion `00378BC0` → `003775D0` → `0037AA90(block, 0)`, for every map whose pack
  > has a light set. See [the map_ctrl pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md) §3.
- **Searches that came back empty, with the method that failed:**
  - `FUN_003775d0`'s call at `003776A6` — **not read.** The second binder caller may pass a
    different manager index and I have not checked which; see the `slot == 0` item above.
  - A writer of `LGT2` data — a literal byte search of the whole 32,864,752-byte image for `LGT2`
    returns **exactly one** hit, the compare immediate at `0037AAC1`. There is no second site that
    could be a writer emitting the magic.

## 8. Related

- [`25 — the EBP script container`](../README.md) — the directory that supplies this section's offset
- `Sections/section-004.md`, `Sections/section-006.md`, `Sections/section-019.md` — the other three
  sections in this lane
- `Sections/section-008.md` and `Sections/section-009.md` — **`section_014` never occurs without
  both of them**
- [`04 — Actor / Entity`](../../04-Actor-Entity/README.md) — `FUN_0037aa90` carries the CodeDomain
  `Actor.ResourceAuxiliaryTable`, and its caller is `ActorResource_FinalizeManagerRuntimeAfterLoads`

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Audio — SERVICE.** The second binder caller `003775D0` calls a 188-byte Audio-filed helper beside its
`0037AA90` manager-slot bind. What that helper does for lighting sets is not read.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — SERVICE.** A 3,882-byte function this page cites calls a 498-byte Presentation body.
- **Actor — CLIENT and SERVICE (4 edges).** 2 inbound (Actor bodies `0037AA90` call page-cited `0037A9B0`, `0037B230`); 2 outbound (page-cited `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `003775D0` call Actor bodies `0037AA90`). Substantive edges include `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) calls `0037AA90`; `003775D0` calls `0037AA90`; `0037A9B0` is called by `0037AA90`; `0037B230` is called by `0037AA90`.
- **ActorEntity — CLIENT and SERVICE (53 edges).** 24 inbound (ActorEntity bodies `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `ActorResource_OnDefinitionPayloadLoaded` (0032F850) call page-cited `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `0037B230`, `0032F6F0`); 29 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `003306E0` call ActorEntity bodies `00263FF0`, `0037B230`, `003DE920`). Substantive edges include `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) is called by `ActorResource_OnDefinitionPayloadLoaded` (0032F850); `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) is called by `00330220`; `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) is called by `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0); `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) is called by `0032FB70`; the remaining edges run through shared helpers the page cites.
- **Resource — MECHANICAL (3 edges).** 3 calls from page-cited bodies into shared Resource plumbing (`0032E400`, `0032E620`) - the helpers' general call surface, not a Resource relationship of this page's subjects.
- **World — SERVICE (1 edge).** 1 outbound (page-cited `00378A60` call World bodies `003C63A0`). Substantive edges include `00378A60` calls `003C63A0`.
- **WorldAreaField — CLIENT and SERVICE (18 edges).** 6 inbound (WorldAreaField bodies `00378BC0`, `00378A60`, `00331990` call page-cited `003DCF10`, `003775D0`, `00378030`); 12 outbound (page-cited `00378A60`, `00331990`, `003320D0` call WorldAreaField bodies `MapRef_GetPrimaryFieldValue` (00264F10), `MapRef_GetAuxValue0` (00264F40), `00378A60`). Substantive edges include `00331990` calls `MapRef_GetPrimaryFieldValue` (00264F10); `00331990` calls `MapRef_GetAuxValue0` (00264F40); `00331990` calls `00378A60`; `003320D0` calls `003EAA00`.
