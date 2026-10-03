---
system: EBP section_002 — the zone message bank
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
  - "section_002"
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

# EBP `section_002` — the zone message bank

> Every line of text a zone can say. The script names a number; this section turns that number
> into the words on screen.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115** `us` `.ebp` files — 1,114 containers plus one non-container |
| this unit present in | **828 of 1,114 containers (74.3 %)** |
| co-occurrence | **not a pair with `section_003`** — 328 together, **500 with `002` alone**, 31 with `003` alone, 255 with neither |
| section size range | 64 B – 58,496 B, median 768 B (2,229,760 B total) |
| strings per file | 1 – 287, median 7 (**17,327 strings total**) |
| string length | 0 – 4,282 bytes, median 87; **466 strings are empty** |

Occupancy was re-derived from the container's own directory and agrees with the frozen census
exactly (828). The independence claim is not a guess either: **the engine binds `002` and `003`
through separate globals, separate binder functions and separate load-completion bits** (§3), which
is engine-side confirmation of what the file census already said.

---

## 1. What the player sees

**This is the talking.** Walk up to a Nalbina guard and press the action button; the line he says is
in here. So is the sign you read, the "Save?" prompt at a Save Crystal, the yes/no question a Moogle
asks you, the choice list when a Way Stone offers you destinations, and the subtitle under a
cutscene. When a zone has anything to say to you, the words are in this section of that zone's
`.ebp`.

The script itself contains **no text at all** — it contains numbers. A script line that means
*"say message 12"* is what causes a sentence to appear. Which sentence depends entirely on what is
sitting at index 12 in this section. That is why re-ordering these strings changes what every NPC in
the zone says without touching a single line of script.

Three quarters of zones have one. The ones that do not are zones with nothing to say — a corridor,
a transition, an area whose talking is done elsewhere.

## 2. The layout

Offsets are from the **start of the section**, which is the byte the container directory points at.
Nothing here is relative to the file.

```
+0x00   u32[count]   the offset table -- see below
+first  bytes        the strings, NUL-terminated, laid out back to back
        bytes        zero padding to the next 0x40 boundary
```

The table has no separate count field. **The first entry's own value is the table's byte length**,
so the engine recovers the entry count by dividing it by four:

```
count = *(u32 *)section >> 2
```

> ### AUDIT 2026-09-05 — that formula is exactly what the engine does, and in 213 of 828 sections it is wrong
>
> **The instruction confirms the formula, unmasked:**
>
> ```asm
> 00264D74  movsxd rax, dword ptr [r8]      ; the WHOLE first dword, sign-extended
> 00264D77  and    edx, 0xffffff            ; the index is masked; the count is not
> 00264D7D  shr    rax, 2                   ; count = firstDword >> 2
> 00264D81  cmp    edx, eax
> 00264D83  jge    0x264d6c                 ; the ONLY bound check -> fallback string
> 00264D85  movzx  eax, word ptr [r8+rdx*4] ; offset, 16-bit
> 00264D8A  add    rax, r8
> ```
>
> **But the first entry is an entry**, and this section's own layout says bit 16 is a flag. When the
> first entry carries that flag, `firstDword ≥ 0x10000`, so **`count ≥ 16,384`** while the real table
> has a handful of entries. The true count is `(firstDword & 0xFFFF) >> 2`.
>
> **This happens in 213 of the 828 sections.** Worst case `alc_a0100.ebp`: a **448-byte** section
> with **7** real entries, and the guard at `0x00264D81` admits indices **0 … 16,390**. Past the real
> table, `movzx` reads whatever follows and `add rax, r8` returns it as a string pointer. **The range
> check is the only guard on this path, and on those 213 sections it is not guarding.**
>
> **How this sheet's two halves disagreed without either being wrong.** The formula above is faithful
> to the instruction. The corpus table below is faithful to the data — **but it only holds under the
> masked count**: re-derived with `count = firstDword >> 2` as printed, six of its seven rows fall
> from **828/828 to 615/828**, and `615 + 213 = 828` exactly. With the mask, every row returns
> **828/828**, **17,327** entries and **3,692** flagged — matching this sheet to the entry.
> **Each half was checked; the two were never checked against each other.**
>
> *Nothing in §5 or the encoding work is affected — those rest on the masked walk, which is the
> correct parse of the data. What changes is that the engine does not perform it.*
> → `PROPOSED-repos-4b-10`. *(`repos-4b`, audit pass; own parser over all 828 sections, both formulas.)*

Every entry is one `u32` carrying two things:

```
entry = (flag << 16) | offset16

  bits  0-15   offset of the string, from the start of the section
  bit   16     a flag -- read by the engine, see below
  bits 17-31   never observed non-zero, and never read (§3)
```

**Why the offset is only 16 bits:** the largest `section_002` in the corpus is 58,496 bytes, which
fits in `u16` with room to spare. The engine reads exactly two bytes (`movzx eax, word ptr [r8 +
rdx*4]`, `00264D85`) and adds the section base, so a section larger than 64 KiB could not be
addressed past its first 64 KiB.

Measured over all 828 sections and all 17,327 entries:

| claim | holds in |
|---|---|
| first entry is a non-zero multiple of 4 | **828 / 828** |
| the table fits inside the section | **828 / 828** |
| offsets are **strictly** ascending | **828 / 828** |
| every offset lands inside the section, at or after the table | **828 / 828** |
| the byte before each string is `0x00` (strings are contiguous, in table order) | **828 / 828** |
| every string's terminator is inside the section | **828 / 828** |
| the bytes after the last terminator are all zero | **828 / 828** |

The flag in bit 16 is set on **3,692 of 17,327** entries. Bits 17-31 were zero on every entry.

### The text encoding

The strings are **not ASCII**. Letters occupy one contiguous run:

```
0x04         space
0x20 - 0x39  'A' - 'Z'
0x3A - 0x53  'a' - 'z'
0x85 - 0x8E  '0' - '9'
0x02         line break
0x00         terminator
0x99 '!'   0x9A '?'   0xA7 ','   0xA8 '.'   0xAC apostrophe
```

That table decodes **99.80 %** of `section_003`'s payload bytes and **85.9 %** of `section_002`'s;
the rest of `002` is escape sequences. It was derived by reading known words out of the corpus, not
assumed: `21 3A 45 4D 41 42 3E 4B` is `Balthier`, `35 3A 3A 47` is `Vaan`, `24 51 42 4D` is `Exit`,
`2D 2E 33 04 34 32 24 23` is `NOT USED`. The digits are pinned by `Bulkhead 2/3/4` and `Site 5/9/11
Cart` decoding to real FFXII area names.

Three bytes introduce **escapes**, measured across all 17,327 strings:

| introducer | occurrences | distinct following codes | operand bytes (`>= 0x80`) after the code |
|---|---:|---:|---|
| `0x0F` | 50,193 | 44 | usually 2 (31,755), sometimes 3 (11,046) |
| `0x10` | 36,408 | 196 | usually **0** (29,881) |
| `0x0E` | 3,659 | 32 | usually **4** (3,480) |

Only **5.79 %** of payload bytes have the high bit set outside an escape — those are the digits and
punctuation above. `0x10` with 196 distinct second bytes and no operands has the shape of a
**two-byte glyph escape** (an extended character), not a formatting command; `0x0F` and `0x0E` carry
operands and behave like formatting and choice-list commands. **This document does not claim what
any individual code means** — see §7.

## 3. The loader contract

**The engine never parses this section.** It binds the section's base pointer once at load, and
thereafter every access is a single bounds-checked table lookup that hands back a raw pointer into
the file image. All parsing happens downstream in the text renderer.

### How the section is bound

`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (`0x003304A0`) is the completion
callback for the whole-file read. Its **slot 2 gate** is four instructions:

```
00330519   cmp  dword ptr [rdi + 4], 2      ; slotCount > 2 ?
0033051D   jbe  0x330534                    ; no -> skip section_002 entirely
0033051F   mov  eax, dword ptr [rdi + 0x18] ; directory slot 2
00330522   test eax, eax                    ; 0 = absent
00330524   je   0x330534
0033052F   call 0x330190                    ; -> FUN_00330190
```

`FUN_00330190` (`0x00330190`) stores the base into the per-manager global `DAT_022C6CA0`, calls the
binder `FUN_0026C880` (`0x0026C880`) which writes it to `ctx+0xA0`, then clears **bit 4** of
`g_qwActorManagerPendingResourceMask` and calls
`ActorResource_FinalizeManagerRuntimeAfterLoads` once the mask reaches zero.

`ActorManager_BindLoadedDefinitionPayload` **zeroes `ctx+0xA0` at `0x0026CC49`** on every field
entry, so an unbound bank is `NULL`, not stale.

### The accessors

`FUN_00264D60` (`0x00264D60`, 14 instructions) — **fetch the string for a message id**:

```c
base = *(int **)(ctx + 0xA0);                       // 00264D60
if (base == NULL) return &DAT_01CEB638;             // 00264D6A / 00264D6C
count = (int)((longlong)*base >> 2);                // 00264D74, 00264D7D
if ((int)(id & 0xFFFFFF) >= count)                  // 00264D77, 00264D81, 00264D83
    return &DAT_01CEB638;
return base + *(u16 *)((char *)base + 4*(id & 0xFFFFFF));   // 00264D85, 00264D8A
```

`FUN_002673A0` (`0x002673A0`) — **fetch bit 16 of the same entry**, with the identical guard, then:

```
002673C0   movzx eax, word ptr [r8 + rdx*4 + 2]   ; the HIGH half of the entry
002673C6   and   eax, 1                           ; bit 0 of it = bit 16 of the entry
```

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| container `+0x00` (`EBP2` magic) | — | — | — | **yes — never referenced.** repos-1e disassembled all 570 bytes of `0x003304A0` and found zero references to `[rdi+0]` |
| container `+0x04` slotCount | `0x00330519` | — | — | no — gates this section (`slotCount > 2`) |
| directory slot 2 (`+0x18`) | `0x0033051F` | `== 0` → section skipped | — | no |
| section `+0x00` low u16 (first offset) | `0x00264D74` | — | — | no — ~~**doubles as the entry count** (`>> 2`)~~ the entry count is the whole sign-extended first dword `>> 2`, not this u16 *(corrected 2026-10-02, OPUS: `0x00264D74` `movsxd rax, dword ptr [r8]`, `0x00264D7D` `shr rax, 2`; the u16 is read only as the offset at `0x00264D85`; the two differ in 213 of the 828 `us` sections, the 2026-09-05 audit above)* |
| entry offset (low u16) | `0x00264D85` | — | — | no |
| entry **bit 16** | `0x002673C0` | — | — | no — `mes` branches on it (`0x00348DF0`) |
| entry **bits 17-31** | — | — | — | **yes — masked off by `and eax, 1` at `0x002673C6`.** Zero in all 17,327 entries; nothing could observe a change |
| message id **bits 24-31** | — | — | — | **yes — `and edx, 0xFFFFFF` at `0x00264D77` and `0x002673B2`** |

**What a modder gets from that table.** `mes 5` and `mes 0x01000005` are the same call. Setting any
of bits 17-31 in a table entry does nothing. And **corrupting the `EBP2` magic does nothing at
all** — the four bytes the file is named for are never looked at.

### What happens when it goes wrong

**An out-of-range id is not a crash and not a placeholder — it is the empty string.** Both failure
paths return `&DAT_01CEB638`, and that address is **eight zero bytes in `.rdata`**. A script asking
for message 900 in a bank of 7 gets a message box with nothing in it. So does every `mes` in a zone
whose `section_002` is absent, because the bank pointer is then `NULL`.

**The bound check protects against a bad index, not against a bad file.** The count comes from the
file's own first dword and is never checked against the section's actual length — and it *cannot*
be, because [the container](../README.md) does not store section lengths; a section's extent is
only the distance to the next directory entry. Inflate that first dword in a hex editor and the
engine will happily index past the end of the section into whatever follows. Two mitigations fall
out of the exact instructions rather than from intent: `movsxd` + `shr rax, 2` turns a first dword
with bit 31 set into a *negative* `eax`, which the signed `jge` at `0x00264D83` rejects; and the
id is masked to 24 bits, so the index can never be negative.

### The write path

**There is none.** `DumpDataXrefs` over `0x02098EB0` (`ctx+0xA0` for manager 0) returns exactly
three sites: the binder `FUN_0026C880`, its `LEA`, and the zeroing store in
`ActorManager_BindLoadedDefinitionPayload`. Nothing writes *into* the section body — the game reads
this data and never authors it. There is no version stamp anywhere in the section, and nothing in
the section is normalised on load.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00264D60` | `section_002` string fetch — bank at `ctx+0xA0` | ✅ full body, 14 instructions |
| `0x002673A0` | entry bit-16 flag fetch, same bank | ✅ full body |
| `0x00330190` | slot-2 load completion → stores `DAT_022C6CA0`, clears mask bit 4 | ✅ |
| `0x0026C880` | binder — writes `ctx+0xA0` | ✅ 1 instruction |
| `0x003304A0` | directory walker; slot-2 gate at `0x00330519`-`0x0033052F` | ✅ gate read at instruction level |
| `0x0026CC49` | zeroes `ctx+0xA0` on field entry | ✅ |
| `0x00348DF0` | `mes` verb — calls both accessors, branches on the flag at the tail | ✅ |
| `0x00356B70` | `fieldsignmes` verb — reads **this** bank | ✅ |
| `0x01CEB638` | the fallback string — zero bytes in `.rdata` | ✅ bytes read from the authorized EXE |

## 5. Corpus survey

**Invariants** — each checked over all 828 sections, never over one file:

- The seven structural properties in §2 hold at **828 / 828**. None is a sample.
- Section length is a multiple of `0x40` in **828 / 828** — but this is **not a property of the
  section**. It follows mechanically from the container aligning every directory offset to `0x40`.
  Recorded so nobody re-derives it as a finding about `section_002`.
- Entry bits 17-31 were **zero on all 17,327 entries**.
- `section_002` is the last present section in only **14** of 828 files, so the "runs to EOF" case
  is rare for this unit but real.

**Outliers and things worth a modder's attention:**

- **466 strings are empty** (a terminator at the entry offset). They are deliberate holes in the id
  space, not corruption — the table stays strictly ascending through them.
- The largest single string is **4,282 bytes**; the largest section is **58,496 bytes**
  (`section_002` is by far the largest text unit in the format — `003` totals 54 KB across the
  whole corpus, less than one big `002`).
- One file in the corpus, `us/event/evt_t/evt_t0020/evt_t0020.ebp`, **is not a container at all**
  and has no sections. It is excluded from all 1,114 denominators here.

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
| Is the offset relative to the file, the container, or the section? | **The section.** `add rax, r8` at `0x00264D8A` adds the value to the bank base, and the bank base is the directory slot plus the container base (`0x00330526`). Settled at instruction level, not inferred. |
| Does the layout hold on the corpus or on the file I opened? | **The corpus.** Every row in §2 is 828/828. The first version of this reading was *wrong* — see below. |
| Is the first dword really an offset table, or did I pattern-match? | The engine computes `count = first >> 2` at `0x00264D7D` and indexes `[r8 + rdx*4]`. The file layout and the code agree independently. |
| Could the decompiler have invented the `& 0xFFFFFF` mask? | No — `81 e2 ff ff ff 00` is in the instruction bytes at `0x00264D77`. |
| Is bit 16 really a flag, or is it part of the offset? | `movzx eax, word ptr [r8 + rdx*4]` reads only the low half for the offset; `movzx eax, word ptr [r8 + rdx*4 + 2]` reads only the high half for the flag. Two disjoint reads of the same dword. |
| **Killer for "002 and 003 are one mechanism":** find one engine path that treats them together. | **Not found, and the opposite was found.** Separate accessors (`0x00264D60` / `0x00264D90`), separate context slots (`+0xA0` / `+0xA8`), separate binders, separate globals, separate mask bits (4 / 5), separate dispatch gates. The census (500 files with `002` alone) and the engine agree. |
| If an external tool agrees, was it consulted before or after? | **`ff12-text` was never run.** No part of this sheet rests on it; the tool was not available in this working tree. Every claim is from the corpus bytes and the instruction stream. That is a gap in falsification, not in support — see §7. |

**A correction, recorded rather than rewritten.** The first pass of this reading treated the section's
leading `u32` as a plain offset and concluded that **`section_002` was structurally broken** —
only 38.8 % of files had an ascending table, against 100 % for `section_003`, and the sheet was
briefly headed toward "these are two different formats". That was wrong, and the tell was in the
data: entry values like `0x00010055` sat between `0x54` and `0x74`, which only makes sense if the
high half is not part of the number. Masking to 16 bits took every check to 828/828. The wrong
reading was reachable because `section_003` never sets the flag (0 of 2,313), so the simple reading
works perfectly on `003` and fails only on `002`. **The engine settles it and the corpus alone could
not have**: bit 16 is read by a different instruction than the offset.

## 7. What this document does not claim

- **What any escape code means.** The 44 `0x0F` codes, 32 `0x0E` codes and 196 `0x10` codes are
  framed and counted here, not interpreted. Their semantics belong to the text renderer
  (`FUN_00269F20`, `FUN_002E16B0`)~~, which this document did not read~~ *(answered in part: BX-1 below reads the window path through `002E16B0`; the escape semantics stay open; 2026-10-02, OPUS)*. The `0x10` = glyph-escape
  reading is stated as a shape, not a claim.
- ~~**What bit 16 means.** The engine's use is established exactly — `mes` (`0x00348DF0`) calls
  `FUN_002673A0` and, **when the result is zero**, calls `FUN_002E16B0`; when it is one it does not.
  So the flag selects between two message paths. *Which* two is a claim about the renderer.~~
  **BX-1 answered 2026-09-12 (FABLE): the flag makes the message *modal* — it holds the field
  frame — and the two paths are "open now" versus "mark and defer".** `002673A0(actor, id)` reads
  the entry word `+2` of the actor's `section_002` table (`[actor + 0xA0]`, count = `[table] >> 2`,
  4-byte entries) and returns its bit 0 — bit 16 of the entry. `mes` writes that bit into the
  message slot's byte **`+0x38`** (`002E1E00(slot, flag)` → `0215F200 + slot × 0x68 + 0x38`, slot
  clamped to `0 … 7`) along with the other slot setters, returns the VM record `{slot, flag, 0}`
  (`00348ED7`–`00348EDC`), and **only when the flag is 0 opens the window itself** (`002E16B0`,
  `00348EFF`). The frame's entry gate `00265680` refuses the world tick while any of the eight slots
  has `+0x38` set or `+0x3E` ~~bit 7~~ **bit 0** (`002E0540`'s `shl 7` / `sar 7` keeps bit 0, corrected 2026-09-26; [the world tick](../../00-Engine-Core-Runtime/Battle-Frame/the-world-tick-and-the-field-frame.md)),
  so a flagged message freezes the field until the window's own close and advance paths clear
  the byte (`002E0780` at `002E087E`, `002E09A0` at `002E0A71` / `002E0A9B`, `002E1D90` at `002E1DD8`).
  The other openers of `002E16B0` are `shapewin` (`0033F950`, a tail-jump), the `mes` sibling
  `0034ADA0` (the same setter sequence, reached from `0034B760` / `0034BB10`) and `0050EAB0` (from
  `0050EE30` / `0050EFF0`); which of them opens a deferred flagged window is the residue, and the
  corpus correlation with `0E:82` escapes (2,327 of 3,692 flagged strings) remains a correlation —
  "presents a choice" is consistent with a modal message but is not what the code proves.
- **The full character table.** `0xA5` (4,262 occurrences in `002`, 56 in `003` — e.g. `Way Stone
  <A5> Sigil of Sacrifice`) and `0xA3` ~~are unresolved~~ are the hyphen *(answered: section-003-text.md, BX-2 of 2026-09-15; 2026-10-02, OPUS)*. No glyph table was located in the binary; the
  search that failed was a decompiled-body reading of the two accessors, which do not touch glyphs.
- **Whether the 24-bit id has structure in its top byte.** Bits 24-31 are masked off, so the engine
  cannot see them; whether authored scripts ever set them was not surveyed.
- **Anything about non-`us` languages.** The corpus is the `us` set only. Nine languages ship.

## 8. Related

- [`section_003`](section-003-text.md) — the other text bank, and **not** this one's pair
- [the container](../README.md) — the `EBP2` header and the directory this section is reached through
- [ScriptVM verb dispatch](../../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md)
  — `mes`, `ames`, `mesisselect`, `fieldsignmes` and the rest of the consumers
- [ScriptVM interpreter](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — what executes the script that names the message id

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**The world-tick entry gate `00265680` is consulted outside the frame.**

- **Input — CLIENT and SERVICE.**
  - It is called by `InputGameplay_ArbitrateDigitalInputAndModalS…` and by a 1,002-byte body (`002E09A0`). That body
    in turn asks `InputGameplay_GetActorStateAwareRemappedMask`.
- **Party — CLIENT.** It is called by `PartyControl_ApplyAnalogLocomotionToActor` and
  `PartyFocus_ProcessActorControlPresentationSt…`.
- **Movement and Presentation — CLIENT.** It is called by a 475-byte movement body and a 59-byte Presentation body.

So the gate that stops the world tick while a slot is occupied is also asked by input arbitration and by party
control.

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — SERVICE.** A cited reader calls a 7-byte core getter.
- **Status_Periodic_Terminal — CLIENT.** `BattleUnit_RunPeriodicCombatMaintenance` calls a 149-byte body this page cites.
- **ActorEntity — CLIENT and SERVICE (30 edges).** 9 inbound (ActorEntity bodies `0025B600`, `0026C5D0`, `0026DFB0` call page-cited `00265680`, `00269F20`, `0026C880`); 21 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `00330190`, `002E0780` call ActorEntity bodies `00263FF0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `ActorResource_OnDefinitionPayloadLoaded` (0032F850)). Substantive edges include `00265680` is called by `0025B600`; `00265680` is called by `0026C5D0`; `00265680` is called by `0026DFB0`; `00265680` is called by `00263660`; the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `002E16B0` call Story_Event_Quest_Hunt bodies `PersistentFlag_SetBank2048` (0032ABF0)). Substantive edges include `002E16B0` calls `PersistentFlag_SetBank2048` (0032ABF0).
- **UI — CLIENT and SERVICE (2 edges).** 1 inbound (UI bodies `00279E20` call page-cited `00265680`); 1 outbound (page-cited `002E09A0` call UI bodies `00254B50`). Substantive edges include `00265680` is called by `00279E20`; `002E09A0` calls `00254B50`.
## SWE2-EC7-46 update (2026-09-19) - `0050EAB0`

`0050EAB0` (232 B) is a body - `002640C0`/`00264D60`/`002673A0`/`00267E10`/`002E16B0`/`002E1D50`/`002E1D90`. Interior anchor `0050EAD5` (a `002640C0` call).

## SWE2-EC7-48 update (2026-09-19) - `0033F950`

`0033F950` (205 B) is a body - `00267E10`/`002E1D90`/`002E1E40`/`002E1E70`/`002E1EA0`/`002E1F80`/`002E1FD0`. Interior anchor `0033F96E` (a `00267E10` call).

## SWE2-EC7-62 update (2026-09-19) - `002E1EA0`

`002E1EA0` (146 B) is a call-free `edx`-countdown dispatch - arms 1/2/3/4 each `movsxd` index x`0x68` into the `0215F23D` table. Interior anchor `002E1ED7` (the first `x0x68` index into `0215F23D`).


## SWE2-EC7-75 update (2026-09-19) - `002E1F80` + `002E1E70` + `002E1E40` `0215F200` slot helpers measured

`002E1F80` (74 B) is the `0215F200` eight-slot record write: `ecx`
clamped to [0,7], `0x68` stride - `+0x3A` set, `+0x10 = dx`,
`+0x12 = r8w`, `+0x14 = r9w`, `+0x16` from the fifth stack arg.
Interior anchor `002E1FA6` (the `+0x3A` flag store).

`002E1E70` (45 B) and `002E1E40` (43 B) are the paired `+0x3E` bit
writers on the same clamped `0x68`-stride slot (`0215F23E` base +
index): `002E1E70` writes bit 1 (`(b & 0xFD) | ((dl & 1) << 1)`),
`002E1E40` writes bit 0 (`(b & 0xFE) | (dl & 1)`).
Interior anchors `002E1E95` / `002E1E63` (the mask arms).

## Interior citations for the entry-cited functions (OPUS, 2026-10-03, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-section-002-text-cloudint-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `002E1D50` | 52 B | clamps `ecx` to 0..7 (signed) and, in the 0x68-byte entry `i` of the table at `0215F200`, stores byte 1 at `+0x3b`, `edx` at dword `+0x24`, `r8d` at dword `+0x28` and `r9b` at byte `+0x39` | `002E1D52`, `002E1D5F`, `002E1D70`, `002E1D75`, `002E1D7E` |
| `002E1FD0` | 63 B | clamps `ecx` to 0..7 (signed) and stores `dl` at byte `0215F242` + `i`*0x68, on both of its paths | `002E1FDD`, `002E1FEE`, `002E1FF4`, `002E200B` |
