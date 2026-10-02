---
system: EBP section_003 — the field-sign caption bank
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Script/VM/NativeBridge
evidence_tier: 9
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
corpus_validated: "1115 / 1115 us .ebp scripts (1114 containers), 2026-09-03"
last_reviewed: 2026-09-03
ebp_units:
  - "section_003"
audit:
  passes: 2
  last_pass: 2026-09-05
  last_pass_state: "GN160 (gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8) — independent pass by repos-4b: own offset-table parser over every section, plus capstone read of the accessor at 0x00264D60-0x00264D8D"
  last_pass_by: repos-4b
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 0
---

# EBP `section_003` — the field-sign caption bank

> The short label on a thing you walk up to: **`Ancient Door`**, **`Bulkhead Controls`**,
> **`Way Stone`**, **`Exit`**. Two verbs in the whole engine read it, and both are field signs.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115** `us` `.ebp` files — 1,114 containers plus one non-container |
| this unit present in | **359 of 1,114 containers (32.2 %)** |
| co-occurrence | **not a pair with `section_002`** — 328 together, 500 with `002` alone, **31 with `003` alone**, 255 with neither |
| section size range | 64 B – 1,152 B, **median 64 B** (54,208 B total — the whole corpus of this unit is smaller than one large `section_002`) |
| strings per file | 1 – 43, **median 2** (2,313 strings total) |
| string length | 3 – 30 bytes, median 12; **no empty strings** |

The 31 files carrying `003` **without** `002` are the ones that kill the "these are one mechanism"
reading from the file side; §3 kills it from the engine side.

---

## 1. What the player sees

**This is the caption on scenery you can interact with.** Stand in front of a door in the Barheim
Passage and the game tells you it is `Bulkhead Controls`; in the Great Crystal, the thing you are
about to touch is a `Way Stone` or an `Aries Gate Stone`; on the *Shiva* it is the `Air Deck`; in a
shop doorway it is `Charlotte's Magickery`. Short, fixed, one line — the name of a **thing**, not
something anybody says.

That is the whole difference between this section and [`section_002`](section-002-text.md). `002` is
**speech** — long, formatted, full of colour codes and line breaks, and it changes as the story
moves. `003` is a **nameplate**: 12 bytes on average, no formatting of any kind, and the same in
every visit.

Only a third of zones have one, because only a third of zones have labelled scenery. And you can
see the developers at work in it: **350 of the 2,313 captions in the game read `NOT USED`, and
another 193 read `dummy`** — 543 of them, close to a quarter of the whole bank, are placeholders
sitting in id slots that were reserved and never filled.

## 2. The layout

**Identical in shape to [`section_002`](section-002-text.md)**, and simpler in practice because two
of that section's features are never used here. Offsets are from the **start of the section**.

```
+0x00   u32[count]   the offset table
+first  bytes        the strings, NUL-terminated, back to back
        bytes        zero padding to the next 0x40 boundary
```

There is no count field; the first entry's value **is** the table's byte length, so:

```
count = *(u32 *)section >> 2
```

> **AUDIT 2026-09-05 — the same latent hazard as `section_002`, dormant here.** That shift is on the
> **whole** dword (`0x00264DA4` `movsxd`, `0x00264DAD` `shr`), so a first entry carrying the bit-16
> flag would inflate `count` by 16,384 and the range check at `0x00264DB1` — the only guard — would
> stop guarding. **In `section_002` this fires in 213 of 828 sections**
> ([details there](section-002-text.md#2-the-layout)). **Here it fires in none, because the flag is
> zero on all 2,313 entries** — which is the invariant §2 already records, now with a consequence
> attached. **The bank is safe by its data, not by its code**, and a hand-edited `section_003` that
> sets bit 16 on entry 0 inherits `section_002`'s problem exactly. *(`repos-4b`.)*

Each entry is a `u32` read as two halves — but in this section only one half is ever populated:

```
entry = (flag << 16) | offset16

  bits  0-15   offset of the string, from the start of the section
  bit   16     the flag -- ZERO on all 2,313 entries in the corpus, and there is
               no accessor in the binary that could read it for this bank (§3)
  bits 17-31   never observed non-zero
```

Measured over all 359 sections and all 2,313 entries — **every single check is 359 / 359**:

| claim | holds in |
|---|---|
| first entry is a non-zero multiple of 4 | **359 / 359** |
| the table fits inside the section | **359 / 359** |
| offsets are **strictly** ascending | **359 / 359** |
| every offset lands inside the section, at or after the table | **359 / 359** |
| the byte before each string is `0x00` | **359 / 359** |
| every string's terminator is inside the section | **359 / 359** |
| the bytes after the last terminator are all zero | **359 / 359** |

### The text encoding, and what this section does *not* contain

Same table as `section_002`:

```
0x04         space
0x20 - 0x39  'A' - 'Z'
0x3A - 0x53  'a' - 'z'
0x85 - 0x8E  '0' - '9'
0x00         terminator
0x99 '!'   0x9A '?'   0xA7 ','   0xA8 '.'   0xAC apostrophe
0xA3 / 0xA5 hyphen        (BX-2, 2026-09-15)
```

That decodes **99.80 %** of this section's payload bytes (29,091 of 29,148). The digit run is pinned
by captions that decode to real FFXII scenery — `Bulkhead 2`, `Site 5 Cart`, `Site 9 Cart`,
`Rm 6601 East`.

**The invariant that matters here is an absence.** `section_002` uses three escape introducers
(`0x0E`, `0x0F`, `0x10`) 90,260 times between them. In `section_003`:

> **Zero escape introducers, across all 2,313 strings and all 29,148 payload bytes.**

No colour, no line break (`0x02` never appears either), no glyph escapes, no choice lists. Every
high-bit byte in this section — all 432 of them — is a digit or a punctuation glyph from the table
above. **A caption is plain text and the corpus has no counter-example.** That is a finding, not an
observation about the file somebody opened.

## 3. The loader contract

**The engine never parses this section**, exactly as with `002`: it binds a base pointer at load and
every access afterwards is one bounds-checked table lookup returning a raw pointer.

### How the section is bound

`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`0x003304A0`), the completion
callback for the whole-file read, has a **slot 3 gate** immediately after the slot 2 gate:

```
00330534   cmp  dword ptr [rdi + 4], 3      ; slotCount > 3 ?
00330538   jbe  0x33054f                    ; no -> skip section_003 entirely
0033053A   mov  eax, dword ptr [rdi + 0x1c] ; directory slot 3
0033053D   test eax, eax                    ; 0 = absent
0033053F   je   0x33054f
0033054A   call 0x330220                    ; -> FUN_00330220
```

`FUN_00330220` (`0x00330220`) stores the base into the per-manager global `DAT_022C6CC8`, calls the
binder `FUN_0026C8A0` (`0x0026C8A0`) which writes it to `ctx+0xA8`, then clears **bit 5** of
`g_qwActorManagerPendingResourceMask`. `ActorManager_BindLoadedDefinitionPayload` zeroes `ctx+0xA8`
at `0x0026CC50` on field entry, so an unbound bank is `NULL`.

**Every one of those is a different object from `section_002`'s** — different gate, different
directory slot, different global, different binder, different context slot, different mask bit.

### The accessor

`FUN_00264D90` (`0x00264D90`, 14 instructions). It is `FUN_00264D60` with one byte changed —
`ctx+0xA8` instead of `ctx+0xA0`:

```c
base = *(int **)(ctx + 0xA8);                       // 00264D90
if (base == NULL) return &DAT_01CEB638;             // 00264D9A / 00264D9C
count = (int)((longlong)*base >> 2);                // 00264DA4, 00264DAD
if ((int)(id & 0xFFFFFF) >= count)                  // 00264DA7, 00264DB1, 00264DB3
    return &DAT_01CEB638;
return base + *(u16 *)((char *)base + 4*(id & 0xFFFFFF));   // 00264DB5, 00264DBA
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| container `+0x00` (`EBP2` magic) | — | — | — | **yes — never referenced** in any of the 570 bytes of `0x003304A0` |
| container `+0x04` slotCount | `0x00330534` | — | — | no — gates this section (`slotCount > 3`) |
| directory slot 3 (`+0x1C`) | `0x0033053A` | `== 0` → section skipped | — | no |
| section `+0x00` low u16 | `0x00264DA4` | — | — | no — ~~**doubles as the entry count** (`>> 2`)~~ the entry count is the whole sign-extended first dword `>> 2`, not this u16 *(corrected 2026-10-02, OPUS: `0x00264DA4` `movsxd rax, dword ptr [r8]`, `0x00264DAD` `shr rax, 2`; the u16 is read only as the offset at `0x00264DB5`; the two agree in all 359 `us` sections)* |
| entry offset (low u16) | `0x00264DB5` | — | — | no |
| entry **bit 16** | — | — | — | **yes — for this bank, absolutely.** See below |
| entry **bits 17-31** | — | — | — | **yes** |
| caption id **bits 24-31** | — | — | — | **yes — `and edx, 0xFFFFFF` at `0x00264DA7`** |

**The bit-16 row is the strongest `Inert` in this sheet, and it is a two-sided proof.** The flag
accessor `FUN_002673A0` (`0x002673A0`) reads `ctx+0xA0` hard-coded at `0x002673A0`
(`mov r8, qword ptr [rcx + 0xa0]`). **There is no `+0xA8` counterpart anywhere in the binary** — a
`DumpDataXrefs` sweep of the three accessors returns 16 call sites and not one of them reaches an
`0xA8` flag reader, because none exists. So for this bank the high half of every entry is
unreachable by construction, *and* it is zero in all 2,313 shipped entries. A modder can put
anything in it.

### Who reads it — the whole list

`section_003` has **exactly two consumers in the entire executable**, and both are field signs:

| Verb | id | Handler | Calls |
|---|---|---|---|
| `fieldsign` | `0x0176` | `FUN_00355A00` | `0x00264D90` at `0x00355A9F` |
| `fieldsignmesbyid` | `0x0179` | `FUN_00357120` | `0x00264D90` at `0x0035714A` |

For comparison, `section_002`'s bank has **ten** call sites. **`fieldsignmes` (`0x0178`) is not in
this list** — it reads the `002` bank (`0x00356B9A`). So the sign system draws from *both* banks and
the verb name chooses which: `fieldsign` and `fieldsignmesbyid` take a `003` caption id,
`fieldsignmes` takes a `002` message id. Both render through `FUN_00269F20`.

### What happens when it goes wrong, and the write path

Out of range, or bank absent → **`&DAT_01CEB638`, which is eight zero bytes in `.rdata`**: an empty
caption, not a crash. As with `002`, the entry count is taken from the file's own first dword and
is never checked against the section's real length — the container does not store section lengths,
so it cannot be. **There is no writer**: `DumpDataXrefs` over `0x02098EB8` (`ctx+0xA8`, manager 0)
returns three sites — the binder, its `LEA`, and the zeroing store. No version stamp; nothing
normalised on load.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00264D90` | `section_003` caption fetch — bank at `ctx+0xA8` | ✅ full body, 14 instructions |
| `0x00330220` | slot-3 load completion → stores `DAT_022C6CC8`, clears mask bit 5 | ✅ |
| `0x0026C8A0` | binder — writes `ctx+0xA8` | ✅ 1 instruction |
| `0x003304A0` | directory walker; slot-3 gate at `0x00330534`-`0x0033054A` | ✅ gate read at instruction level |
| `0x0026CC50` | zeroes `ctx+0xA8` on field entry | ✅ |
| `0x00355A00` | `fieldsign` verb — consumer 1 of 2 | ✅ call site `0x00355A9F` |
| `0x00357120` | `fieldsignmesbyid` verb — consumer 2 of 2 | ✅ call site `0x0035714A` |
| `0x002673A0` | flag accessor — **hard-wired to `ctx+0xA0`**, proving no `003` equivalent | ✅ full body |
| `0x01CEB638` | the fallback string — zero bytes in `.rdata` | ✅ bytes read from the authorized EXE |

## 5. Corpus survey

**Invariants** — all checked over 359 sections, none sampled:

- The seven structural properties in §2: **359 / 359**, with no exceptions at all. This unit is the
  cleanest in the two-section pair — `002` needed the bit-16 correction, `003` never did, precisely
  because it never sets the flag.
- **Zero escape bytes** and **zero line breaks** in 29,148 payload bytes.
- **Zero empty strings** — unlike `002`, which has 466. Every id in a `003` bank resolves to real
  text, even if that text is the word `dummy`.
- Entry bit 16 zero on **2,313 / 2,313**.
- `section_003` is the last present section in **26** of 359 files.

**What varies, and the outliers:**

- The median section is **64 bytes holding 2 captions** — this is a small format. The largest is
  1,152 bytes with 43 captions.
- The most common captions across the game:
  `NOT USED` ×350 · `Ancient Door` ×219 · `dummy` ×193 · `Way Stone` ×130 · `Exit` ×89 ·
  `Fool's Facade` ×65 · `Bulkhead Controls` ×60 · then the twelve zodiac `… Gate Stone` captions at
  54-55 each.
- **543 placeholders (`NOT USED` + `dummy`) out of 2,313 = 23.5 %.** A modder reading this bank
  should expect a quarter of it to be dead slots, and should not conclude a file is corrupt on
  finding them.
- The twelve zodiac Gate Stones appearing at a near-identical count is the Great Crystal repeating
  one authored room layout; it is a fact about the level, not about the format.
- One file in the corpus, `us/event/evt_t/evt_t0020/evt_t0020.ebp`, **is not a container** and has
  no sections. Excluded from all 1,114 denominators.

## 6. Falsification pass — 2026-09-03

> **Pass PERFORMED 2026-09-05 (`repos-4b`) — the audit block above recorded this pass before it
> had been run; this is the run.** Own offset-table parser over every section of both banks, plus a
> capstone decode of the accessor. **`section_002`:** 828 sections, first dword `>= 0x10000` in
> **213** — the sheet's own figure — engine count `fd>>2` equal to the true table length in **615 /
> 828**, i.e. wrong in exactly those 213; **17,327 / 17,327** low-16 offsets land inside the
> section; padding zero **828 / 828**. **`section_003`:** 359 sections, the flag set in **0**, the
> formula therefore correct in **359 / 359**, **2,313 / 2,313** offsets in range, padding zero
> **359 / 359**.
>
> **Stronger than 'bit 16 is a flag':** across all 17,327 `section_002` entries the **upper 16 bits
> take exactly two values — 0 (13,635) and 1 (3,692)** — so no other bit of that half is ever used,
> and in `section_003` the upper half is 0 on all 2,313. **All seven cited instruction anchors
> re-decoded and exact:** `0x00264D74`, `0x00264D77`, `0x00264D7D`, `0x00264D81`, `0x00264D83`,
> `0x00264D85`, `0x00264D8A`, in a function running `0x00264D60`–`0x00264D8D`.
>
> **What I attacked and failed to break:** that the 213 might be an artefact of deriving the true
> count from the first entry's low half — it is not, because every one of the 17,327 low-16 offsets
> independently lands inside its section, which a wrong table length would not produce.

| attack | result |
|---|---|
| Is the offset relative to the file, the container, or the section? | **The section.** `add rax, r8` at `0x00264DBA` adds to the bank base, which is directory slot 3 plus the container base (`0x00330541`). |
| Does this hold on the corpus or on one file? | 359 / 359 on every row of §2. |
| **Killer for "`002` and `003` are one mechanism":** find one engine path that treats them together. | **Not found; six independent separations found instead.** Different dispatch gate (`0x00330519` vs `0x00330534`), different directory slot (`+0x18` vs `+0x1C`), different completion handler, different global (`DAT_022C6CA0` vs `DAT_022C6CC8`), different binder, different context slot, different mask bit (4 vs 5), and disjoint consumer sets (10 call sites vs 2, no overlap). The census said 500 files carry `002` alone and 31 carry `003` alone; **the engine agrees for reasons the census could not have seen.** |
| **Killer for "bit 16 is inert here":** find any read of `ctx+0xA8`'s high half. | Searched every call site of all three accessors (16 rows from `DumpDataXrefs`) and disassembled `FUN_002673A0` in full: the bank pointer is `[rcx+0xa0]`, encoded in the instruction at `0x002673A0`, with no `0xA8` variant in the binary. **The claim survived.** |
| Is "no escapes" real, or just rare? | It is exhaustive: every one of the 29,148 payload bytes was classified, and 432 high-bit bytes were all accounted for as digits or punctuation. Zero remained. |
| Could the decompiler have invented the structure? | The whole contract was re-read from raw instruction bytes via capstone against the authorized EXE, independent of Ghidra's decompiler. Both agree. |
| If an external tool agrees, was it consulted before or after? | **`ff12-text` was never run** — it is not present in this working tree. Nothing here rests on it. That is an unused falsification opportunity, recorded in §7, not a support gap. |

**Cross-check against an independent session.** `repos-1e`, working the container unit separately,
reported the same slot-3 gate, the same handler, the same global and the same mask bit, having
disassembled `0x003304A0` byte by byte. Two readings that did not share intermediate results agree
on every address. Its stronger result — that **`[rdi+0]` is never referenced in all 570 bytes of the
walker**, so the `EBP2` magic is genuinely never validated — is what lets the magic row in §3 be
stated as `Inert` rather than "no reader found".

## 7. What this document does not claim

- ~~**The full character table.** `0xA5` and `0xA3` are unresolved.~~ **BX-2 ANSWERED 2026-09-15
  (OPUS) — both are the hyphen, and the font/renderer never had to be opened.** This section's
  charset is the *same table* as the authored `st2e` string heaps, which
  [the string-table page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)
  §7 documents independently from the `us` text banks. Six mappings agree exactly and none
  disagrees: `0x04` space, `0x20`–`0x39` `A`–`Z`, `0x3A`–`0x53` `a`–`z`, `0xA7` comma, `0xA8` stop,
  `0xAC` apostrophe. That page already maps **`0xA3` / `0xA5` to a hyphen**.
  **Confirmed directly against the banks rather than taken on trust:** in `word.bin`'s fifteen banks
  `0xA5` has **87 occurrences** and they are item names — `Hi<A5>Potion`, `X<A5>Potion`,
  `Hi<A5>Ether` — which are *Hi-Potion*, *X-Potion* and *Hi-Ether*. `0xA3` has 5, all compound
  labels (`all<A3>cancel`, `escape<A3>cancel`, `no<A3>chip`). Reading this section's own example
  back, `Way Stone <A5> Sigil of Sacrifice` is **`Way Stone - Sigil of Sacrifice`**.
  *The cross-check runs both ways:* this page's `0x99 '!'` and `0x9A '?'`, which the `st2e` table
  lacks, are confirmed in the banks too — `Fly<9A> Enkidu<99>` is *Fly? Enkidu!* — so neither table
  is complete on its own and the two are halves of one charset. Carried to `section_002`'s 4,262
  occurrences by the shared table; the merge itself is offered to AY-8's owner, not taken here.
- **Where the caption is drawn, and what a "field sign" looks like on screen.** Both consumers hand
  the pointer to `FUN_00269F20`, which was not read. The player-facing description in §1 is grounded
  in the *decoded caption text* and the verb names, not in the render path.
- **Why 543 slots are placeholders.** That they are placeholders is observed; whether they are
  reserved for cut content, for other languages, or for alignment is not established.
- **Anything about non-`us` languages.** The corpus is the `us` set only; nine languages ship, and
  caption lengths in particular would be expected to differ.
- **That bit 16 is meaningless in the format** — only that **nothing in this build can read it for
  this bank**. If a tool or another build reads it, this document is wrong and should reopen.

## 8. Related

- [`section_002`](section-002-text.md) — the message bank; same layout, different content,
  **not this one's pair**
- [the container](../README.md) — the `EBP2` header and the directory this section is reached through
- [ScriptVM verb dispatch](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)
  — `fieldsign`, `fieldsignmesbyid`, and `fieldsignmes` which reads the *other* bank
- [ScriptVM interpreter](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — what executes the script that names the caption id

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Movement — SERVICE.** A 487-byte function this page cites calls `Actor_SetFacingHeading_Variant1` and Movement helpers of 66, 113 (twice) and 165 bytes.
