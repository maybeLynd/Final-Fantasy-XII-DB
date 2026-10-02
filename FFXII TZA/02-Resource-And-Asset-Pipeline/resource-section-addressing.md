---
system: Resource section addressing (tag + name lookup)
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — owner re-status 2026-09-30 (OPUS, on SWE2-CONTRACT's reconciliation); it was reopened by the SECTION-10 overlay (60379fcbd); that section is now accepted by a non-author section review (SWE2-AUDIT-SPEC, FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929, ratified a95c664bf); residue reconciled 2026-09-30 (SWE2-CONTRACT, DD batch 6), with no open item left on the page; the owner read is done
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: "snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30"
    verified: "re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS"
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-30
audit:
  passes: 2
  last_pass: 2026-09-07
  last_pass_state: GN160-xiionline-61-crossref-disposition
  crossref_clean: true
  reopened_count: 0
external_production:
  section: SECTION-10
  date: 2026-09-23
  status: "locally validated; formal independent acceptance pending"
  evidence: _experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md
---

# Resource section addressing

> How the engine finds a specific piece of data inside a loaded resource file — by a four-byte
> **tag** and a thirty-two-byte **name**, with wildcards.

## 1. What the player sees

Nothing directly, but every loaded thing in the game arrives this way. A zone's script, a
model's mesh, a sound bank, a texture table — each lives as a named section inside a larger
resource, and the engine reaches it by asking for a tag and a name.

For a modder this is the addressing scheme. If you want to know how the engine locates the
part of a file you are trying to change, or why a hand-edited resource is not found, this is
the lookup that decides.

## 2. Native mechanism

### Matching a section

`ResourceSectionHeader_MatchesTagAndName32(header, tag, name)` decides whether one section
header matches a query. Both criteria support a wildcard:

```c
tag_matches  =  (tag == 0)                  // 0 is a wildcard
             || (tag == 0x4C4C4140)         // bytes "@ALL" - also a wildcard
             || (header->dwRawSectionTag == tag);

name_matches =  (name == NULL)              // NULL is a wildcard
             || memcmp(header->szNameKey32, name, 32) == 0;

return tag_matches && name_matches;
```

The name comparison is **not** a string compare. It is eight explicit 4-byte integer
comparisons covering a fixed **32-byte** field — offsets 0, 4, 8, 0xC, 0x10, 0x14, 0x18, 0x1C.
Every byte participates, so a name must match in full including whatever padding follows it.

**But the caller does not supply 32 bytes** (refined 2026-09-02, §9). The query name is normalised
first, into a fixed scratch buffer, so an ordinary C string works and the padding is supplied by the
engine — see §9 for the consequence, which is a **31-character limit** on section names.

`0x4C4C4140` is the little-endian dword whose bytes read **`@ALL`** — a literal wildcard tag
spelled in ASCII inside the binary.

### Resolving a section to a pointer

```c
void *ResourceEntry_ResolveSectionOffset(entry, int32_t section_offset)
{
    if (entry == NULL || section_offset == -1)   // -1 is the not-found sentinel
        return NULL;
    // 004096DF add eax, ebx / 004096E1 cdqe: a 32-bit sum, sign-extended
    uint32_t base = (uint32_t)ResourceEntry_GetResolvedBasePointer(entry);
    return (void *)(intptr_t)(int32_t)(base + (uint32_t)section_offset);
}
```

**Width, corrected 2026-09-13.** The earlier `base + section_offset` was unrestricted notation. The body adds
the **low 32 bits** of the base to the offset and sign-extends the sum (`ADD EAX,EBX; CDQE`), and
`ResourceEntry_FindSectionPointerByTagAndName` (`00409660`) does the same (`004096A4 add eax, [rsp+40]` /
`004096A8 movsxd rbx, eax`). A base above 4 GB does not survive either helper, and a base whose low 32 bits
plus the offset reach `0x80000000` comes back sign-extended. **The base is not checked:** a non-null entry of
an unsupported mode resolves to base 0, so any offset other than 0 and `-1` still returns a non-null
pointer — the offset itself, sign-extended. The correction is ASTRA's
([render-event selection evidence](../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md)
§11), re-read by FABLE against both bodies.

Section offsets are relative to the entry's resolved base, and **`-1` means "no such
section"** — the value the find-by-tag-and-name functions return on failure.

### Two storage modes

`ResourceEntry_GetResolvedBasePointer(entry)` branches on a mode field at `entry+4`:

```c
if (entry->mode /* +4 */ == 0)
    return FUN_0051ee00(entry + 0x10);          // resolve from inline data at +0x10

if (entry->mode == 1) {
    if (DAT_02b62e10 != 0) {                     // global re-resolve flag
        p = FUN_003ab7f0(entry->handle /* +0x30 */);
        entry->cached /* +0x38 */ = p;           // refresh the cache
        return p;
    }
    return entry->cached;                        // use the cached pointer
}
return NULL;                                     // any other mode
```

Mode 0 resolves from data carried **inline** in the entry. Mode 1 holds a **handle** at
`+0x30` and a **cached pointer** at `+0x38`, re-resolving through the handle only while a
global flag is set — so the cache can be invalidated engine-wide by flipping one byte, which
is the shape of a "resources may have moved" signal.

An entry with any mode other than 0 or 1 resolves its **base** to `NULL`. That does **not** make the section
lookup fail closed: `004096C0` adds the offset to that zero base without a test (above), so the explicit null-entry and `-1` guards do not validate the base. SECTION-10 also executes
zero-offset and modulo-sum returns of NULL; those guards are sufficient, not an exhaustive list of
all zero results.

## 2a. Nonempty PRF lookup and setup — SECTION-10

[Original-code production](../_experiments/evidence/continuation-section10-nonempty-registration/REVIEW.md) now executes both version0/+30 and version1/+40
nonempty offset tables. These are fixed table-relative DWORD offsets, not slot-relative ones.
Version1 skips zero slots; a later child keeps its original slot index. The root is tested first.
A PRF root match has offset0 but index-1; a plain root match has both0. Missing/unsupported-version
queries leave both-1. Callers must use the output appropriate to their API.

`00409A60` pads the root and child names in the INPUT, including before copy-mode allocation.
Borrowing does not make setup read-only. Query normalization uses shared scratch `02B62E20`;
no arbitrary reentrant/thread-safe lookup is established. Base0+offset0 and a wrapping low32 sum
can return NULL in addition to the explicit early guards.

`00409FE0` uses its named `@FEF` lookup as an admission check, then reads the actual effect-data
offset from a metadata-size-derived footer word. The two offsets are independently supplied and
made unequal in the fixture. See [the complete registration/lifetime mechanism](the-nonempty-prf-registration-and-specialized-relocation.md).

Historical page/audit receipts below remain history; they do not independently accept this update.

*Accepted since (SWE2-CONTRACT, DD batch 6, `_index/candidates/swe2contract-ddres-b6-0930/b6_section_addressing.py` A1):* SWE2-AUDIT-SPEC reviewed SECTION-10 as a non-author.
The review is on the board as `FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929`, verdict ACCEPT, and its record is
copied at `_index/candidates/auditspec-ratify-legacy-verdicts-0929/source-REVIEW-0929-FINAL-BATCH.md`
(ratified `a95c664bf`). It covers OV-28 and OV-44, both SECTION-10 pages. The review accepted the section only: its
fixture replays were Linux-gated and not re-run there, and the acceptance rests on byte-exact bodies and a semantic
re-read. The front matter's "formal independent acceptance pending" is superseded by this and kept as written.

## 3. Key addresses

| Address | Name | Role |
|---|---|---|
| `00409C30` | `ResourceSectionHeader_MatchesTagAndName32` | the match predicate |
| `00409600` | `ResourceEntry_GetResolvedBasePointer` | mode 0 / mode 1 base resolution |
| `004096C0` | `ResourceEntry_ResolveSectionOffset` | `sign32(low32(base) + offset)`, `-1` sentinel, base unchecked |
| `00409660` | `ResourceEntry_FindSectionPointerByTagAndName` | find and resolve in one call — same `sign32` sum |
| `00409F50` | word-id wrapper of `002ED570` | `FFFF` → `NULL`; otherwise **sign-extends the word** (`movsx`), so ids `8000`–`FFFE` are negative indices |
| `004090D0` | `@FRP` child-container selector | non-`@FRP` input returned unchanged; child pointers are **zero-extended** 32-bit sums (§4) |
| `00409780` | `ResourceEntry_FindSectionIndexAndOffset` | |
| `00409930` | `ResourceEntry_FindSectionIndexByTagAndName` | |
| `00409A30` | `ResourceEntry_FindSectionOffsetByTagAndName` | |
| `002ED570` | `ResourceTable_ResolveEntryByIndex` | entry lookup |
| `004780B0` | `ResourceTable_ResolveEntryBySignedIndex16` | 16-bit signed index variant |
| `00409210` | name normaliser — zero-fill 32, `strncpy` 32, force NUL at `[0x1F]` | ✅ read |
| `0051EE00` | mode 0 inline resolver — `003AB7F0(inline.q_08)`, 9 B | ✅ read 2026-09-12 |
| `003AB7F0` | mode 1 handle resolver — raw pointer or tagged handle through `0036B130` | ✅ read 2026-09-12 |
| `0036B130` | tagged-handle lookup: `[(h & ~3) + 8] + 0x40` for `h ≥ 0x100000` with low bits set, else 0 | ✅ read 2026-09-12 |
| `0041E500` | the only writer of the re-resolve flag — sets it around `00409F70([rec+0xD90])`, clears it after | ✅ read 2026-09-12 |

**These names came from prior GFZ annotation and were verified, not inherited.** Each body was
read this session and matches the name it carries.

## 4. Data structures and formulas

```
Resource section header            0x30 bytes
  +0x00  u32     dwRawSectionTag      four-byte tag
  ...    char[32] szNameKey32         fixed 32-byte name key, compared in full

Resource entry
  +0x04  i32     mode                 0 = inline, 1 = handle+cache, else NULL
  +0x10  ...     inline data          (mode 0, passed to 0051EE00)
  +0x30  ptr     handle               (mode 1, passed to 003AB7F0)
  +0x38  ptr     cachedBase           (mode 1, refreshed when DAT_02b62e10 != 0)

Globals
  DAT_02b62e10   u8   re-resolve flag; when set, mode-1 caches are refreshed on every access
                      (set to 1 and back to 0 inside 0041E500 only - 0041E509 / 0041E51C)

resolve(h)  [003AB7F0]:  h == 0            -> 0
                         (h & 3) == 0      -> h                (a raw pointer)
                         else              -> r = 0036B130(h); r <= 0x40 ? 0 : r   <- corrected 2026-10-02, OPUS: the test is unsigned(sext(low32(r))) <= 0x40, not the full pointer (003AB7F0+0x41 movsxd rcx, eax; 003AB7F0+0x44 cmp rcx, 0x40; 003AB7F0+0x48 cmovbe rax, rbx)
0036B130(h):  h (32-bit) >= 0x100000 and (h & ~3) != 0  ->  [(h & ~3) + 8] + 0x40   else 0
0051EE00(inline) = resolve(inline.q_08)      ; mode 0's "inline data" carries the handle at entry+0x18

Resource table descriptor (J-4, 2026-09-12)  -- the object whose rows are resource entries
  +0x08  handle  bankDirectory      resolved into +0x10 on every lookup when non-null (002ED5AE-002ED5BC)
  +0x10  ptr     bankDirectoryBase  0x20-byte records; record.+0x10 = image-relative offset of the bank
  +0x30  handle  slotTable          resolved into +0x38 on every lookup when non-null (002ED58A-002ED598)
  +0x38  ptr     slotTableBase      16-byte slots: +0x00 s32 key (-1 = empty), +0x08 s32 nextIndex
  +0x40  s32     activeHead         first index of the threaded slot list (-1 = none)
  +0x48  i32     rowStride          read as a dword, multiplied signed (imul)
  +0x4C  u32     bankShift          read as a DWORD (002ED59C); sar by CL uses its low 5 bits
  +0x50  u32     rowMask
  row(int32 index):                                                   ; 002ED570-002ED5EA, in this order
      bank  = ImageAddress_ResolveRuntimePointer(bankDirectory[sar32(index, bankShift & 0x1F)].+0x10)
                                         ; read and decoded BEFORE the key test, with no capacity check
      if (slot[index].key == -1) return NULL
      return bank + sign32(u32((index & rowMask) * rowStride))
  refresh(descriptor, fn)  [0051FF30]: for i = activeHead; i != -1; i = slot[i].nextIndex: fn(row(i))
  00409F70(descriptor) = refresh(descriptor, 0040A210)   ; 0040A210(row): row.+0x38 = resolve(row.+0x30)
```

**Section match:**

```
match  iff  (tag == 0 || tag == 0x4C4C4140 /* "@ALL" */ || header.tag == tag)
       &&   (name == NULL || all 32 bytes of header.szNameKey32 == name)
```

**Section pointer:**

```
ptr(entry, offset) = (offset == -1 || entry == NULL) ? NULL
                                                     : sign32(low32(base(entry)) + u32(offset))   ; base may be 0

child(frp, i)  [004090D0]:   frp == NULL -> NULL ; frp.magic != '@FRP' -> frp (the full input pointer)
  version 0:  i <u frp.+0x0C ? zext32(low32(frp) + 0x30 + frp.dword[0x30 + 4i])
                             : zext32(low32(frp) + 0x30 + frp.dword[0x30])          ; out of range -> the first child
  version 1:  if (row <u frp.+0x34) i = row * frp.+0x30 + col                        ; else i = col
              off = frp.dword[0x40 + 4 * sext(i)]      ; read BEFORE the bound test
              off == 0 -> NULL ; i >=u frp.+0x0C -> NULL ; else zext32(low32(frp) + 0x40 + off)
  other version: NULL
```

The two families differ and **neither the sign-extension nor the bounds behaviour generalises across helpers**:
the section helpers sign-extend, the child selector zero-extends, and only version 0 falls back instead of
failing. (ASTRA's §11, re-read against `004090D0`'s complete body, 2026-09-13.)

**Base resolution:**

```
base(entry) = entry.mode == 0 ? f_0051EE00(entry + 0x10)
            : entry.mode == 1 ? (DAT_02b62e10 ? refresh(entry) : entry.cachedBase)
            :                   NULL
```

## 5. Call chain

```
caller wants a named section
  -> ResourceEntry_FindSectionOffsetByTagAndName / ...IndexByTagAndName / ...PointerByTagAndName
     -> per candidate section header:
          ResourceSectionHeader_MatchesTagAndName32(header, tag, name)
     -> offset, or -1 if none matched
        -> ResourceEntry_ResolveSectionOffset(entry, offset)
           -> ResourceEntry_GetResolvedBasePointer(entry)
              -> mode 0: 0051EE00(entry+0x10)
              -> mode 1: cached, or 003AB7F0(handle) when DAT_02b62e10 is set
```

**Upstream:** any subsystem loading authored data — scripts, models, sound banks, tables.
**Downstream:** a raw pointer into the loaded resource.

**Do not confuse with:** `ResourceTable_ResolveEntryByIndex` and the signed-16 variant, which
find the *entry*; these functions find a *section inside* an entry.

## 6. Modding notes

- **A section is addressed by tag + 32-byte name.** The name compare covers all 32 bytes, so
  trailing bytes matter — a name that looks right but differs in padding will not match.
- **`@ALL` and `0` are wildcard tags**; `NULL` is a wildcard name. A query with both wildcards
  matches the first section.
- **`-1` is the not-found sentinel** throughout. Resolution returns `NULL` for a null entry or offset `-1`, but
  an entry whose base does not resolve still yields `0 + offset` — test the base, not only the result.
- **Mode-1 entries are cached.** If you relocate resource data at runtime, the cached pointer
  at `+0x38` is stale until `DAT_02b62e10` forces a re-resolve.
- **XIIOnline:** resource pointers are process-local by construction — mode-1 entries cache a
  raw address. Never treat a resolved section pointer as shareable identity.

## 7. What is not known

- [x] ~~What `0051EE00` does — the mode-0 inline resolver. **J-1.**~~ **Read 2026-09-12 (FABLE):**
      nine bytes — `mov rcx, [rcx+8]; jmp 003AB7F0`. Mode 0's "inline data" is the same
      handle-or-pointer as mode 1's `+0x30`, stored at `entry + 0x18`; the two modes differ only in
      where the handle sits and whether the result is cached at `+0x38`.
- [x] ~~What `003AB7F0` does — the mode-1 handle resolver. **J-2.**~~ **Read 2026-09-12 (FABLE):**
      a null handle resolves to 0; a handle with its two low bits clear **is the pointer** and is
      returned unchanged (`003AB846`); a handle with a low bit set is tagged and goes through
      `0036B130` (`003AB82C`), which requires the 32-bit value to be at least `0x100000`, masks the
      tag off and returns the qword at `+8` of the record it names **plus `0x40`** (`0036B14D`–
      `0036B155`) — the payload of an object header; a result of `0x40` or less (a null `+8`) is
      turned back into 0 (`003AB834`–`003AB838`). Six callers use the resolver directly
      (`ResourceTable_ResolveEntryByIndex` among them), so tagged handles are a general convention,
      not this table's alone.
- [x] ~~What sets and clears `DAT_02b62e10`, and when re-resolution is triggered. **J-3.**~~ **Read
      2026-09-12 (FABLE):** one writer in the image — `0041E500`, which sets the byte to 1, calls
      `00409F70` on the render root's resource table at `+0xD90` *(2026-09-12: the object is the **render root** every render record's `+0x10` resolves to — `00332660` passes `022C6F30`, `0042ED60` resolves the array's `+0x48830` — **but see the 2026-09-19 correction below: `0042ED60`'s `+0x48830` belongs to `022C6F28`, a different global** — not a render record; and its `+0xDA8` refresh is `0051B9F0`, which rebases every active node of the 64-slot presentation-entry container and then rebuilds each payload's derived pointers, [render-event selection evidence](../17-Presentation-Rendering/Character-Render-Records/render-event-selection-evidence.md) §6–8)*, and clears it (`0041E509`–
      `0041E51C`) before refreshing `+0xD98`, `+0xDA8` and `+0xDA0`. Re-resolution is therefore
      scoped to that single call: it runs when the render-record maintenance `0042ED60` (under
      `00332660`) finds the active-list-dirty bit set again after the remover and the promoter, and
      from `00332590` — [the render-record array page](../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) §"active list dirty". Outside that window every mode-1 access
      uses the cached base at `+0x38`.
- [x] The full resource-entry layout beyond `+0x04`, `+0x10`, `+0x30`, `+0x38`. **J-4.** *Narrowed
      2026-09-12 (FABLE):* the entry's **owner** is now read — a table descriptor (§4) that
      `ResourceTable_ResolveEntryByIndex` (`002ED570`) indexes in two levels (bank = `index >>
      +0x4C`, row = `index & +0x50`, row stride `+0x48`) after checking the 16-byte slot at
      `+0x38[index]` for `-1`, and that the refresh walker `0051FF30` traverses as a linked list
      threaded through the slots' `+0x08` from `+0x40`; the J-3 refresh (`00409F70`) applies
      `0040A210` to every listed row, re-resolving the **row's** `+0x30` into its `+0x38` — so each row
      *is* a mode-1 entry, and the entry's size is the descriptor's ~~data-defined~~ `+0x48`. What lies
      between `+0x18` (the mode-0 handle) and `+0x30`, and past `+0x40`, is still unread; ~~it needs a
      shipped descriptor instance (the render record's `+0xD90`) rather than more code.~~
      *Corrected 2026-09-26 (FABLE, Claude Opus 5.5), from `RS-1`'s answer (SWE2-DATA, 2026-09-16, below):* `+0x48` is
      not data. `0051F9F0` stores it from a `.text` immediate, and only three descriptors exist, embedded in the render
      root at `+0x000`, `+0x060` and `+0x0F0`, with strides `0x50`, `0xC0` and `0x260`. The path this row reads
      (`002ED610`) takes its descriptor from `[resolved + 0xD98]`, and `0041E3E5` stores `root + 0x60` there. The same
      path then reads the row's `+0x84` (`002ED670`), which rules out the `0x50` family. So ~~these rows~~ the rows `002ED610` reads are **`0xC0`
      bytes**; the resource entries this box asks about are the `[+0xD90]` bank's, whose stride is `0x50` (`RenderResourceEntry`) *(corrected 2026-10-02, OPUS: the J-3 refresh `0041E500+0x10` loads `[rcx+0xD90]` for `00409F70`; `0041E3A0+0x3E` stores `root + 0` there and `0041E3A0+0xA2` hands it to `00409F10`, whose `00409F10+0x13` is `mov edx, 0x50`; `[+0xD98]` gets stride `0xC0` at `0046E250+0x22`)*.
      **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5), from the type store:** the full layout is declared as
      `RenderStrideC0Element` (`0xC0`, rows of `RenderStrideC0Bank` at root `+0x60`; `_types/fields.tsv`). Every byte
      from `+0x000` to `+0x0BF` has a row: the flags and sentinel indices, the five encoded relative pointers, a
      4 × 4 local transform at `+0x40`, the skeleton reference `+0x94`, and the unobserved spans named as such. The
      `0x50` family (root `+0x000`) is a different descriptor, and its rows are ~~not this box's~~ this box's resource entries *(corrected 2026-10-02, OPUS: the mode-1 entries the J-3 refresh re-resolves are the `0x50` rows, as corrected above)*.
- [x] ~~The set of real section tags used by the game, and their meanings. **J-5.**~~ **Measured
      2026-09-12 (FABLE) over every `@FRP` container in the archive** — the 3,164 `.ca`, the 1,066
      `.cm` and the **9,909 containers embedded in the 4,392 `.mot` packs** (`PKFL` files whose
      `@FRP` blocks sit at `0x800`-aligned offsets; a two-file sample of the other 28 extensions found
      the magic nowhere else), every entry reached through the loader's own offset table: **eleven
      tags, all `@F` + two letters** — motion `@FRM`, `@FMC`, `@FMN`, `@FMW` (every `.ca`, every
      `.mot` block, 45 `.cm`); model `@FCP`, `@FTR`, `@FOR` (all 1,066 `.cm`), `@FDM` (1,045), `@FTE`
      / `@FCT` (1,044), `@FEF` (144). No entry carries any other tag. Meanings: `@FCP` is the character
      parameter block ([the FCP page](../17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md)); the others are named as populations on [the FRP container page](../17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md) §9
      and their readers are that page's residue, not this one's. Tally in
      `Tools/work/FABLE/bf3-scratch/frp_tags-2026-09-12.json`.
- [x] ~~Whether `@ALL` appears in authored data or only as a code-side wildcard. **J-6.**~~ **Answered
      2026-09-12 (FABLE): code-side only.** No entry of the 14,139 containers above carries `@ALL`,
      and the only `@ALL` byte sequences in a 300-file-per-extension sample of the archive are four
      incidental runs inside compressed `.mpk` / `.dat` payloads (`rwg0101.mpk`, `rbl0202.mpk`,
      `mfr0105.mpk`, `menuhandbook_person004.dat`), not tag fields.

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| Match predicate incl. both wildcards | complete body of `00409C30` | 1 |
| `0x4C4C4140` is `@ALL` | little-endian byte order of the literal: `40 41 4C 4C` | 1 |
| The eleven shipped tags, and no `@ALL` in data | in-process scan of `FFXII_TZA.vbf`: 3,164 `.ca`, 1,066 `.cm`, 9,909 `.mot`-embedded containers, entries through the offset table, 0 malformed; `@ALL` absent from every entry | ~~data (2026-09-12)~~ 9 |
| Name key is 32 bytes, compared in full | eight 4-byte comparisons at offsets 0…0x1C in `00409C30` | 1 |
| `-1` is the not-found sentinel | explicit `section_offset != -1` guard in `004096C0` | 1 |
| Two storage modes with a cached mode 1 | complete body of `00409600` | 1 |
| ~~Lookup fails closed~~ **Corrected 2026-09-13:** the null-entry and `-1` guards return NULL; the base is not tested, and the `sign32(low32(base) + offset)` sum may also be zero (SECTION-10) | `004096C8`–`004096E1` and `0040969C`–`004096A8` | 1 |
| §2a: nonempty PRF lookup and setup (SECTION-10) | retained original bodies, byte-exact (FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929); their isolated original-code fixture replays are Linux-gated and were not re-run by the acceptance | 1 (bodies); fixture execution UNMEASURED on Windows |

*(§8 narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../_index/candidates/auditspec-review-dd-02-restatus-0930/REVIEW.md) correction 2: the authored-data row's tier is 9, and §2a gets its row.)*

**On the inherited names.** Every function in §3 already carried a GFZ name. Under the rule
that *the GFZ is a claim, not a source*, each was read this session rather than trusted:
`ResourceSectionHeader_MatchesTagAndName32` does match a tag and a 32-byte name key;
`ResourceEntry_ResolveSectionOffset` does resolve an offset against a base;
`ResourceEntry_GetResolvedBasePointer` does resolve a base pointer. **The names were accurate.**
Recorded because verifying and confirming is a result, not a non-event — and the same check on
the ScriptVM dispatch table earlier today went the other way.

## 9. Related

- [`../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) — scripts are one kind of loaded resource
- [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md) — why inherited names get verified

## 9. Falsification pass 2026-09-02

**Attack chosen.** Two things here rest on weaker footing than the rest: the section header size
`0x30`, which the document takes from a **GFZ type name** (`FFXII_ResourceSectionHeader_0x30_Partial`)
rather than from a read, and the claim about name padding, which describes the *stored* name without
saying what the *caller* supplies.

### SURVIVED: everything already documented about matching and resolving

Re-read in full, and all of it holds exactly — both tag wildcards including the `@ALL` decode, the
eight-dword 32-byte comparison, the `-1` sentinel, the two storage modes, the `DAT_02B62E10`
re-resolve flag with its `+0x38` cache, and the fail-closed default. Nothing in §2 needed changing.

*Superseded in part (marked 2026-09-30, SWE2-CONTRACT; `_index/candidates/swe2contract-ddres-b6-0930/b6_section_addressing.py` F1):* "the fail-closed default" was withdrawn
by the 2026-09-13 width correction in §2. A non-null entry of another mode resolves its base to 0, and `004096C0`
still adds the offset (`004096DF add eax, ebx` / `004096E1 cdqe`), so the lookup does not fail closed. The rest of
this pass stands.

### CONFIRMED by stride, not by type name: the header is `0x30` bytes

`ResourceEntry_FindSectionIndexAndOffset` walks the table with

```c
pFVar5 = section_header + 1;      /* pointer arithmetic on the 0x30-byte type */
```

so ~~the iteration stride **is** `0x30`~~ the header is `0x30` bytes, but the walk steps a 4-byte DWORD offset table that starts there, and each section sits at `+0x30` plus its offset *(corrected 2026-10-02, OPUS: `00409780+0x13E` `lea r11, [r10 + 0x30]`, `00409780+0x15D` `add r11, 4`, and `00409780+0x148` `add ecx, 0x30` / `00409780+0x14D` `add ecx, r10d` locate each section)*. The size no longer rests on a Ghidra type having a number in
its name.

### NEW: the container has a magic, and `@`-prefixed tags are reserved

Before iterating, the finder validates the **first** header:

```c
if (section_header->dwRawSectionTag == 0x50524640) {     /* bytes "@FRP" */
    if (*(int *)&section_header->field_0x4 == 0) {
        ...
        count = *(uint *)&section_header->field_0xc;      /* section count */
```

`0x50524640` is little-endian for **`@FRP`**. So the first `0x30` bytes are a **container
descriptor**, not a section: tag `@FRP`, a variant field at `+0x04` that must be `0` **or `1`** —
the finder's next test (`0040982F`) accepts `1` and then takes its offset table from `+0x40`
instead of `+0x30`, which 1,195 shipped `.ca` files use ([the container page](../17-Presentation-Rendering/Model-And-Motion-Formats/frp-object-container.md);
corrected 2026-09-11 from "must be `0`") — and the **section count at `+0x0C`**. ~~Real sections~~
~~begin at `+0x30` (variant 0) or `+0x40` (variant 1).~~ The DWORD offset table begins at `+0x30` (variant 0) or `+0x40` (variant 1), and each real section at that position plus its dword *(corrected 2026-10-02, OPUS: `00409780+0xD9` `lea r11, [r10 + 0x40]` and `00409780+0xE7` `lea ecx, [rax + 0x40]`, and the `+0x30` pair at `00409780+0x13E` / `00409780+0x148`)*.

Together with the wildcard tag `@ALL`, this shows a convention the document did not state:
**a tag beginning `@` is reserved** — `@FRP` marks the container, `@ALL` means "any section". An
authored section tag should avoid `@`.

### REFINED: names are capped at 31 characters, and the engine pads them

The finder normalises the query before comparing:

```c
FUN_00409210(&DAT_02B62E20, name_key32_or_null);

void FUN_00409210(void *dst, const char *name) {
    dst[0] = dst[1] = dst[2] = dst[3] = 0;   /* zero all 32 bytes */
    strncpy(dst, name, 0x20);                /* at most 32 */
    ((char *)dst)[0x1F] = 0;                 /* force NUL in the last byte */
}
```

Three consequences, none previously recorded:

1. **The caller passes an ordinary C string.** §2's "a name must match in full including whatever
   padding follows it" is true of the **stored** name but would mislead anyone about the query — the
   engine supplies the padding.
2. **Section names are effectively limited to 31 characters.** Byte `0x1F` is forced to zero after
   the copy, so a 32-character name can never be matched: its final byte is destroyed in the query
   while the stored header keeps it.
3. **A stored name must be zero-padded to be findable by name.** The query's tail is zeros, so a
   header padded with anything else will never match a by-name lookup — though it remains reachable
   by tag, or by the `@ALL` wildcard with a `NULL` name.

The scratch buffer is a **single fixed global** (`0x02B62E20`), so by-name lookup is not
re-entrant — a detail worth knowing before calling it from a hook on another thread.

## Crossref disposition 2026-09-07 — the largest single finding in the database, and it was real

`audit_crossrefs.py` reported **117 edges to/from Presentation that this document never mentions** —
the biggest of its 384 findings, and 8 % of every implicated edge in the database. Dispositioned by
`xiionline-61` against GN160, by measuring rather than by judging it irrelevant.

### What the measurement says

`ResourceTable_ResolveEntryByIndex` (`002ED570`) — the function this document is about — has
**87 direct callers** (re-counted 2026-09-30 by SWE2-CONTRACT with `retool.py`: 87 calling functions, 115 call sites, `_index/candidates/swe2contract-ddres-b6-0930/b6_section_addressing.py` C1; the owner split below is `xiionline-61`'s GN160 measurement and was not re-derived):

| owner of the caller | callers | share |
|---|---:|---:|
| **Presentation** | **59** | **67.8 %** |
| *(unresolved)* | 16 | 18.4 % |
| `CodeDomain:Boundary` | 6 | 6.9 % |
| **Resource** | **6** | **6.9 %** |

> **This document is owned by Resource, and two-thirds of its subject's callers are the renderer.**
> Six are Resource's own.

### Why the finding was right and the document was not wrong

Section 1 already says *"every loaded thing in the game arrives this way — a zone's script, a model's
mesh, a sound bank, a texture table."* That claim is **true and unquantified**, and an unquantified
universal is exactly what hides a 68 % concentration.

**The finding is dispositioned as a real omission of emphasis, not of fact.** The correction is the
number: a modder changing this lookup should expect to affect **rendering first**, and everything
else second.

### What this does not license

`002ED570` is a **registered cross-subsystem hub** — see
[`../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md`](../00-Engine-Core-Runtime/Shared-State-Accessors/cross-subsystem-accessor-hubs.md),
which already records its 87 callers and correctly notes it is **owner `Resource`, not middleware**.
**A hub's caller list is not evidence of ownership** — 59 Presentation callers do not make this a
Presentation function, and this document does not become a Presentation document. That is the
distinction the mission's ban on inheriting ownership from a caller exists to protect.

**The general rule this establishes for the remaining findings:** where a crossref finding is driven
by a *registered hub*, disposition it by reference to the hub document and a caller census — never by
asserting the neighbour is irrelevant, and never by moving the document.

## OPUS independent review, 2026-09-13 — agreed, and the structured half is missing

**`ASTRA-CONTRA-OPUS-SECTION-POINTER`.** Re-derived from the shipping image before reading what this
page now says. **Both claims hold.**

`ResourceEntry_ResolveSectionOffset` `004096C0` is 41 bytes, and it has exactly two guards:

```
004096C6  mov  ebx, edx            ; the offset
004096C8  test rcx, rcx / jne      ; guard 1: null entry -> 0
004096D5  cmp  ebx, -1  / je       ; guard 2: the -1 sentinel -> 0
004096DA  call 00409600            ; the base -- 64-bit in RAX
004096DF  add  eax, ebx            ; ... but only EAX is used: a THIRTY-TWO-BIT add
004096E1  cdqe                     ; sign-extended back to 64
```

1. **The base is never rechecked.** `00409600` returns **0** for a null entry *and* for any mode
   other than 0 or 1 (`0040961D cmp ecx,1 / jne 0040960E / xor eax,eax`). An unsupported mode
   therefore yields `sign32(0 + offset)` - **a small absolute address, not a refusal.** The lookup
   does **not** fail closed.
2. **The arithmetic is 32-bit and sign-extended.** The high half of the base is **discarded**, and a
   low half with bit 31 set becomes a negative 64-bit value. `00409660` does the same thing with
   `movsxd` instead of `cdqe`.

### The part that is mine and is not done

*Done since (marked 2026-09-30, SWE2-CONTRACT; `_index/candidates/swe2contract-ddres-b6-0930/b6_section_addressing.py` T1):* `RS-1` was answered by SWE2-DATA on
2026-09-16 (below): an entry is a row in one of three compiled-stride banks. The rows are now declared in the type
store: `RenderResourceEntry` (`0x50`, rows of `RenderResourceEntryBank`), `RenderStrideC0Element` (`0xC0`) and
`RenderModelInstance` (`0x260`). The paragraph below is kept as the state on 2026-09-13.

This page carries the corrected formula and a prose layout for the entry - mode at `+0x04`, inline
data at `+0x10`, handle at `+0x30`, cached base at `+0x38`. **None of that is in the type store.**
`ResourceEntry` is **not one of its 247 declared types**; the only resource type there is
`ActorResourceEntry`, which is a different 0x14-byte structure.

> **A formula that lives only in prose has no consumer that can be checked against it.**
> `types_index.py` cannot validate a width it has never been told about, and the ~~nine functions~~ eleven functions *(answered: see *There are 17 call sites in 11 functions, not nine* below; 2026-10-02, OPUS)* that
> call `004096C0` - `PresentationEntry_RebuildDerivedReferences` `0041CA70` four times, `00372820`,
> `0041B4E0`, `00504940`, `0041FCF0`, `0042A390` and two more - have no declared type to disagree
> with. **ASTRA asked whether the structured consumers preserve the width. There are none.**

**Why it is not declared here and now:** the entry's **extent is not established**. The proven
fields reach `+0x40`, but nothing found in this pass allocates an entry, and the callers of
`00409600`/`004096C0` are consumers rather than constructors. **Declaring `0x40` would be asserting
a lower bound as a size**, which this store has been burned by before (`ActorStorageRecord`'s
`0x11C`, an underestimate by 3-6x). Registered as `RS-1` instead.

## `RS-2` answered — every consumer keeps the sign-extended value as a 64-bit pointer (FABLE, 2026-09-14)

*Static reading of the shipped image. Every direct call site of `004096C0` (`tools/rawcalls.json`) was disassembled up to
where the result stops being used.*

**There are 17 call sites in 11 functions, not nine.** `0041CA70` calls it four times, `00372820` twice, `0041B4E0` twice and
`00504940` twice; `00371330`, `003713C0`, `00372510`, `00373060`, `0041FCF0`, `0042A390` and `0042B270` once each.

| use of the result | sites |
|---|---|
| **stored as an 8-byte field** | `0041CADC` → `[rdi+0x370]`; `00504969` → `[rbx+0x1F8]`; `005049A2` → `[rbx+0x230]` |
| **dereferenced at once as a 64-bit base** | `0037135A` (`[rax+0x38]`), `00372557`, `00372887` (kept in `rbp`), `00372F1E`, `003730B5`, `0041FDFE` (kept in `rsi`, `[rax+0xC]`), `0042A430` (`[rax+rdx*2+0xC2]`, `+0xC4`) / `0042B310` (`[rax+rcx*2+0xC0]`, then `+0xC2`, `+0xC4`), both indexing 6-byte three-word records at `+0xC0` by `[rbx+0x3C4]`, and the five sites that pass it as `rcx` to `00408F80` (`0041B502`, `0041B52A`, `0041CAAD`, `0041CB2F`, `0041CB57`) |
| **re-encoded to 32 bits** | `00371415` → `RuntimePointer_EncodeImageAddress` (`rax − [01F83530]`) → `[rbx+0xA0]` |

- **So the answer to the question as asked is no declared type, but three undeclared 8-byte fields.** No row of
  `_types/fields.tsv` cites any of these sites or holds this result.
- **Every consumer treats the value as a full pointer.** None zero-extends it, re-adds a high half, or range-checks it.
- **What that means.** The high 32 bits of the resolved base never reach any consumer. The pointer is right only while the
  base plus offset lies in the low 2 GB, where the sign extension of `EAX` equals the true address. If the base's low half
  has bit 31 set, all 17 sites receive `0xFFFFFFFF8xxxxxxx`.
- **A lead, not a finding.** `EO-3` records crashes at `001D6E20` reading `0xFFFFFFFF8BC…`, the address shape this produces.
  Whether `001D6E20` is downstream of `004096C0` was not traced.
  *Traced the same day:* it is not. `001D6E20` is fed by the request queue's raw-path route, which truncates a heap path
  pointer in `0032E7C0` and sign-extends it in `0032E105`
  ([the request queue](the-resource-request-queue.md) §7, `EO-3`). The two sites share the defect class, not the path.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (1 edges, one fan-in).** All 1 edges are ActorEntity bodies reaching `00332590` on this page. `FUN_002628b0` is the worked example - it is a 1,689-byte manager routine that indexes `02098E10` at the **`0x288` stride** - the same records the manager indexer walks - in a `0x50`-byte frame with a stack cookie. The crossing is **one shared subject with 1 callers on that layer**, not 1 separate relationships. Edge count from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — CLIENT.** `FUN_003a1650`, owned by that layer, calls `0036B130` on this page. That caller is an audio lookup that resolves an object through `0036B130` and, when it exists, hands it to `002DEC10`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — MECHANICAL (SWE2-EC7-38, 1 edge).** `006C0520` — the shared helper this page cites inside `005049E0` — is called by a body on the Movement layer. Shared-helper fan-in; no movement relationship to section addressing.
- **CoreRuntimeScheduling — CLIENT and SERVICE (10 edges).** 9 inbound (CoreRuntimeScheduling bodies `0022BC20`, `MainLoop_UpdateAndRenderFrame` (0022B8C0), `0022B6E0` call page-cited `00332590`, `00332660`, `0024D540`); 1 outbound (page-cited `0024D540` call CoreRuntimeScheduling bodies `00229EA0`). Substantive edges include `00332590` is called by `0022B6E0`; `00332590` is called by `0022AF50`; `00332590` is called by `0022B000`; `00332590` is called by `0022B7E0`; the remaining edges run through shared helpers the page cites.
- **Presentation — CLIENT and SERVICE (482 edges).** 338 inbound (Presentation bodies `0041F340`, `0041FCF0`, `PresentationAuthoredCommand_Class09_ActivateLoadedResourceState` (00417F40) call page-cited `ResourceTable_ResolveEntryByIndex` (002ED570), `003D8E50`, `003AB7F0`); 144 outbound (page-cited `005004C0`, `CharacterRender_RebindCombatLookAndSkeletonResources` (003E3D70), `0024D540` call Presentation bodies `0041E500`, `CharacterRenderRecord_ResolveSkeletonBoneArray` (00421D20), `CharacterRenderRecord_GetFCPPresentationConfigurationPayload` (003E55F0)). Substantive edges include `00332590` calls `00426950`; `00332590` calls `0041E500`; `00332660` calls `00426950`; `00332660` calls `0041E500`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050D5E0` call page-cited `0036B130`). Substantive edges include `0036B130` is called by `0050D5E0`.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050D5E0` call page-cited `0036B130`). Substantive edges include `0036B130` is called by `0050D5E0`.
## 10. The `0041E500` exclusive subtree — all 5 members bound (SWE2-FRONTIER, followup queue)

`0041E500` is the 76-byte re-resolve battery §`RS-2` already isolates: it raises the
re-resolve flag byte at `02B62E10` (`0041E509`), runs `00409F70([+0xD90])`
(`0041E517`), drops the flag (`0041E51C`), then refreshes three more containers —
`0046E3E0([+0xD98])`, `0051B9F0([+0xDA8])`, and a tail call to
`00478030([+0xDA0])` (`0041E523`–`0041E547`). The four `+0xD9x` fields are four
side-by-side `PresentationEntryReferenceContainer` objects on the same parent record.

All five exclusive members are container rebases built on two shared walkers
(`0051FF30` visits each entry with a callback; `00520010` is the two-arg variant) and
the base resolver `003AB7F0`:

| member | role | interior |
| --- | --- | --- |
| `00409F70` (12 B) | forwards `[+0xD90]` to `0051FF30` with callback `0040A210` — the flag-guarded re-resolve pass | [`00409F77`](../_index/ADDRESS-INDEX.md) |
| `0046E3E0` (62 B) | three callbacks over `[+0xD98]`: `0051FF30` with `0046E8C0`, then `00520010` with `0046E910` and `0046E8CF` — re-resolve plus two derived-pointer fixups | [`0046E402`](../_index/ADDRESS-INDEX.md) |
| `0051B9F0` `PresentationEntryReferenceContainer_RebaseAndRefreshDerivedPointers` (37 B) | `[+0xDA8]`: runs member `0051F620` first, then tails `0051F580` with callback `0051BBF9` — rebase resolved pointers, then refresh the derived ones | [`0051B9F9`](../_index/ADDRESS-INDEX.md) |
| `0051F620` `PresentationEntryReferenceContainer_RebaseResolvedPointers` (131 B) | the real rebase walk: the container's `[+4]` top-2-bit field selects the entry base (`0` → `003AB7F0([+8])`, `1` → `[+8]` direct, `2`/`3` or `[+0x10]==0` → none, `0051F62A`–`0051F65C`); then the `+0x1C`→`+0xC` index chain walks `0x30`-stride entries writing `[+0x18] = 003AB7F0([+0x10]) + dword[+0x20]` — stored handle resolved to a base, plus the intra-record offset (`0051F670`–`0051F693`) | [`0051F687`](../_index/ADDRESS-INDEX.md) |
| `00478030` `RenderModelInstanceContainer_TeardownAllEntries` (12 B) | `[+0xDA0]` tail-forwards to `0051FF30` with callback `00478270` | [`00478037`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0051FF30`/`00520010`/`0051F580` (the container
walkers), `003AB7F0` (handle → base), the four callback bodies `0040A210`/`0046E8C0`/
`0046E910`/`0046E8CF`/`0051BBF9`/`00478270`, and `0051F580`'s refresh path. The sign-
extension caveat §`RS-2` documents applies to every `003AB7F0` result this subtree
consumes — the `+0x18` write is the full 64-bit `cdqe` of `resolved + offset`.

## `RS-1` narrowed — a `ResourceEntry` is a ROW IN A BANK, and its extent is authored, not compiled (OPUS, 2026-09-15)

`RS-1` asks for a `ResourceEntry`'s extent so the type can be declared, and records the blocker:
*"nothing found allocates one, and every caller of `00409600` / `004096C0` is a consumer rather than
a constructor."* **Nothing allocates one because nothing ever does.**

**Where a caller gets its entry, measured.** A byte-level `rel32` scan gives `00409600` four call
sites and `004096C0` seventeen. Three of the four, and the `0037135A` / `0041B502` shapes among the
seventeen, obtain the pointer the same way — from `00409F50`, the word-id wrapper this page already
documents, which tail-jumps `002ED570`:

```asm
0041B4F3  mov  rcx, qword ptr [rcx + 0x48]   ; the caller's descriptor pointer
0041B4F7  call 00409F50                      ; -> entry
0041B4FC  mov  edx, dword ptr [rbx + 0x54]
0041B502  call 004096C0                      ; ResourceEntry_ResolveSectionOffset(entry, offset)
```

And §"Resource table descriptor" already states what `002ED570` returns:

```
return bank + sign32(u32((index & rowMask) * rowStride))      ; rowStride = descriptor + 0x48
```

**So an entry is a row inside a loaded bank blob**, addressed by `index & rowMask` at a stride the
DESCRIPTOR carries at `+0x48`. It is never ~~a heap object~~ its own heap object (the bank blob it sits in is heap-allocated by `0051F9F0`, *(answered: see the `RS-1` answer below; 2026-10-02, OPUS)*), which is why no allocation site exists to
find, and why every caller looks like a consumer: they all are.

**What that means for declaring the type.** `rowStride` is a runtime dword read out of the
descriptor, not an immediate anywhere in `.text`. ~~**The extent is authored data.**~~ *(answered: see the `RS-1` answer below - falsified by the writer, the geometry comes from `.text` immediates; 2026-10-02, OPUS)* Declaring `0x40`
would still assert a lower bound as a size — the objection `RS-1` already makes — and no reading of
the code can raise it, because the code does not contain the number.

**What would settle it**, and it is a data question rather than a code one: a census of the authored
`rowStride` (and `rowMask`) over the shipped resource tables. If every table ships one stride, that
value is the type's size and `ResourceEntry` can be declared against it with the census as evidence;
if strides differ per table, then `ResourceEntry` is not one fixed-size type at all, and the store
should say so rather than pick a number. Routed to `SWE2-DATA`.

**Confirmed unchanged by this reading:** the fields `+0x04` mode, `+0x10` inline data, `+0x30`
handle and `+0x38` cached base. A parameter-displacement scan over `00409600`, `004096C0`,
`00409660`, `00409780`, `00409930` and `00409A30` finds those four displacements and **no others**,
so nothing here extends the known layout — it explains why the layout stops where it does.

## `RS-1` answered — the census result: three strides, all compiled; `rowMask` is derived, never authored (SWE2-DATA, 2026-09-16)

OPUS's premise — *"rowStride is a runtime dword read out of the descriptor, not an immediate
anywhere in `.text`; the extent is authored data"* — is **falsified by the writer**. The
descriptor's geometry is established by exactly one function and it is fed `.text` immediates, not
file data. No loader reads `rowStride`/`rowMask` out of any shipped resource.

**The writer.** `0051F9F0(desc, rowStride, bankShift, bankCount, [bankDir buf], [slotTable buf])`
is the only function that stores the complete geometry triple. An anchored byte-level scan for
stores to `+0x48`/`+0x4C`/`+0x50` over the whole `.text` produces thousands of same-offset false
positives in unrelated structures; filtered for the rare `+0x4C` field and verified by reading the
bodies, `0051F9F0` is the sole complete writer. Its stores (0051FA84–0051FAA6):

```asm
0051FA84  mov  dword ptr [rbx + 0x48], edx     ; rowStride      = arg2, a .text immediate
0051FA8E  mov  dword ptr [rbx + 0x4c], r8d     ; bankShift      = arg3, a .text immediate
0051FA89  mov  edx, 1
0051FA92  shl  edx, cl                          ; edx = 1 << bankShift
0051FA9C  lea  eax, [rdx - 1]
0051FAA3  mov  dword ptr [rbx + 0x50], eax     ; rowMask        = (1 << bankShift) - 1  DERIVED
0051FA9F  imul edx, r14d
0051FAA6  mov  dword ptr [rbx + 0x54], edx     ; capacity       = (1 << bankShift) * bankCount
```

`rowMask` is therefore **not an authored field and not even an argument** — the request's
"does rowMask vary with rowStride?" has the stronger answer: it varies with `bankShift`, and
`bankShift` is `5` at every site, so `rowMask` is `0x1F` everywhere. `0051F9F0` is reached only
by `E8` (no data references, no indirect calls — verified by a whole-image pointer scan).

**The census.** Exactly three call sites exist, all inside the render-root container's
construction `0041E3A0` (sole caller `0033263C`, building the four sub-containers of the
singleton at `022C6F30` / `+0x60` / `+0xF0` / `+0x160` — the fourth, at `+0x160`, is a
*different* container family configured by `0051B9D0`→`0051F170`, not a `002ED570`
descriptor):

| call site | wrapper | descriptor | rowStride | bankShift | rowMask | bankCount | capacity | bankDir buf | slotTable buf |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `00409F38` | `00409F10` | `022C6F30+0x000` | `0x50` | 5 | `0x1F` | `0x0A` | `0x140` | `02B62E40` | `02B62F80` |
| `0046E285` | `0046E250` | `022C6F30+0x060` | `0xC0` | 5 | `0x1F` | `0x05` | `0x0A0` | `02CA61B0` | `02CA6250` |
| `00477F0A` | `00477EE0` | `022C6F30+0x0F0` | `0x260` | 5 | `0x1F` | `0x05` | `0x0A0` | `02CA74A0` | `02CA7540` |

(`bankCount` arrives via each wrapper's `edx` from `0041E3A0`'s own arguments — `0x0A`, `5`,
`5` — and the two buffers are static `.data` arrays sized exactly to `bankCount`×`0x20` and
`capacity`×`0x10`, each pair contiguous end-to-start. The bank blob itself is heap-allocated
by `0051F9F0` at `capacity * rowStride` bytes into descriptor `+0x28`.)

**Answer to RS-1.** Several strides — `0x50`, `0xC0`, `0x260` — not one. `rowMask` does not
vary independently (always `0x1F`, computed). And the deeper correction to the RS-1 framing:
the extent is **neither authored nor one number** — it is three compiled constants attached to
three embedded descriptor instances of one container. `ResourceEntry` is not one fixed-size
type across the shipped tables; if a type is to be declared it must be declared per descriptor
family (`0x50`-row entries, `0xC0`-row entries, `0x260`-row entries), or the store records that
row extent is a per-descriptor runtime property set at construction. NATIVE/STATIC evidence;
the verifier `Database/Tools/work/DATA/rs1/census_rowstride.py` re-derives every cell of the
table from the shipping EXE, and `rowstride-census.tsv` is the durable artifact.

> **CORRECTION 2026-09-19 (OPUS) — `022C6F20` and `022C6F28` are two different globals, and
> the `+0x48830` extent is not the render root's.** This page says of the render root
> *"`00332660` passes `022C6F30`, `0042ED60` resolves the array's `+0x48830`"*. `0042ED60` loads
> `rbx` from **`022C6F28`** at `0042ED66`, not from the root's cache, and every offset it then
> touches — `+0x48800`, `+0x48818`, `+0x48830`, and a `0x740`-stride array — belongs to
> **that** object. The two globals sit eight bytes apart and are not the same thing:
> `022C6F20` is written with `&022C6F30` by the six `lea` sites and has a handful of references
> confined to the `00332xxx` cluster, while **`022C6F28` has 636 references in 372 functions**
> (measured under a passing positive control). Attributing `+0x48830` to the render root would
> have given it an extent of at least `0x48838` instead of its measured **`0xDB0`**.
>
> **The render root is now declared** as `RenderResourceRoot`, `size 0xDB0`, with the four
> sub-objects this section already identified as its four fields and the interior-pointer table
> at `+0xD90`–`+0xDAF` as the other four. The extent rests on three independent arguments that
> agree on the same byte: the tiling (`+0x160` + this page's own `0xC30` = `+0xD90`, and
> `+0x0F0` + `0x70` = `+0x160`), a route-seeded census that finds nothing above `+0xDA8` at
> three window sizes with all three cited sites present, and the fact that `022C7CE0` — root
> `+0xDB0` exactly — is independently and absolutely referenced by an unrelated float-using
> cluster while the qwords below it have no absolute references at all.

**The `0x260` family is now declared** (SWE2-STRUCT, 2026-09-17): `RenderModelInstance`,
`size 0x260`, 42 field rows covering `+0x00`..`+0x25F` — the object
`003E55B0` `CharacterRenderRecord_ResolveModelInstance` returns and `005049E0` initialises.
`00477EE0` hardcodes `mov edx,0x260` at `00477EF3`, so the `+0xDA0` container's rows are
this type. The `0x50` and `0xC0` families remain undeclared.

*Superseded (marked 2026-09-30, SWE2-CONTRACT; `_index/candidates/swe2contract-ddres-b6-0930/b6_section_addressing.py` T1):* both are declared now. The `0x50` family is
~~`RenderResourceEntry` (OPUS, with `RenderResourceEntryBank` at `0x60`, `aa3470a36` / `0cca6e0f0`), and the `0xC0`
family is `RenderStrideC0Element` (FABLE 2026-09-26, J-4, the box above).~~
`RenderResourceEntry` (declared by OPUS at `8c13cfe3f`, 2026-09-19; its bank `RenderResourceEntryBank`, `0x60`, at
`aa3470a36`), and the `0xC0` family is `RenderStrideC0Element` (declared by OPUS at `4fee674b9`, 2026-09-19; read
from the type store as J-4's answer by FABLE on 2026-09-26, the box above). *(narrowed 2026-10-01, SWE2-STRUCT for OPUS, on SWE2-AUDIT-SPEC's [review](../_index/candidates/auditspec-review-dd-02-restatus-0930/REVIEW.md) correction 3, which applies the [DDRES-B6 review](../_index/candidates/auditspec-review-ddres-b6-0930/REVIEW.md)'s correction 1.)*

## The `00409780` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00409780` (`ResourceEntry_FindSectionIndexAndOffset`, ~101 B) —
five-register walk (`00409780`/`00409794`).

| member | role | interior |
| --- | --- | --- |
| `00409C30` | `edx == 0x4C4C4140` ("@ALL") tag, `dword[rcx]` compare — section matcher (`00409C34`/`00409C3C`) | [`00409C34`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — `ResourceTable_ResolveEntryByIndex` (2026-09-17, SWE2-EC7)

`002ED570` — 146 B, 75 frontier callers at census (the document records 87 direct callers; the
difference is callers that have since been dispositioned). Interior verified:
[`002ED587`](../_index/ADDRESS-INDEX.md) is `movsxd rsi, edx` — the index sign-extension that the
document's row table predicts. The body then performs the two-level lookup the document
describes: `[rcx+0x30]` resolved through `003AB7F0` into `+0x38` (the slot table), `[rcx+8]`
resolved into `+0x10` (the bank table); bank = `index >> [+0x4C]`, row base = `+0x10 + bank*32`,
entry pointer resolved from `[row+0x10]` through `0020E600`; and the 16-byte slot at
`+0x38 + index*16` is the `-1` guard — on hit the row stride `[+0x48]` and mask `[+0x50]` produce
`base + (index & mask) * stride`.

NOT claimed: the `+0x18`..`+0x30` interior of the row (the page's standing residual), only the
index path.

*The standing residual named here, the entry's layout, was answered on 2026-09-26 by J-4 (the `0xC0` rows,
`RenderStrideC0Element`), and the `0x50` rows are declared too (above). This citation's own scope, the index path,
is unchanged. Marked 2026-09-30, SWE2-CONTRACT.*


## Interior citation — frontier hub `00409F50` (2026-09-18, SWE2-EC7)

`00409F50` — 17 B, 24 callers; the `-1`-sentinel wrapper over `002ED570`.
Interior verified: `cmp dx, -1` at [`00409F50`](../_index/ADDRESS-INDEX.md) returns 0 for the
absent index; otherwise `movsx edx, dx` sign-extends the 16-bit index and tail-jumps
`002ED570` at [`00409F5C`](../_index/ADDRESS-INDEX.md). Resource indices are `int16` with
`-1` = none — the two-level paged accessor never sees the sentinel.


### Interior citation — frontier hub `00332590` (2026-09-18, SWE2-EC7)

`00332590` — 42 B, 5 callers. A registration thunk: publishes its own
`lea`-computed object address (`rip+0x1F94995`) into `[02269020]`, runs
`0041E500` and `00426950`, then tail-dispatches `003697C0(6)`
([`003325B5`](../_index/ADDRESS-INDEX.md)) — the kind-6 registration the
section-addressing table records.

### Interior citation — frontier hubs `00409A30`, `00409FA0` (2026-09-18, SWE2-EC7)

`00409A30` — 33 B, 10 callers, `ResourceEntry_FindSectionOffsetByType`: a
shaped shim over `00409780` — two stack out-cells (`[rsp+0x30]` arg in `r9`,
`[rsp+0x68]` return cell) around the call at
[`00409A43`](../_index/ADDRESS-INDEX.md), returning the found offset in `eax`.

`00409FA0` — 35 B, 8 callers (`0041FCF0` and peers above): the sibling
boundary shim — packs `{edx, r8}` into a two-cell stack block and forwards to
`0051FE30` with `rdx = &0040A1E0` at
[`00409FB9`](../_index/ADDRESS-INDEX.md) — the `0040A1E0` callback through the
shared trampoline, same family as `00409F50`.

## SWE2-EC7-25 update (2026-09-18) — `00332660` section init compose

`00332660` (91 B) publishes `022C6F30` into `022C6F20`, gates on
`00369CF0(6)`, runs the `0041E500`/`00426950`/`003697C0(6)` triple, then
`004262E0` on `022C6F28` and tail-jumps `0042ED60` — the section-table
init arm. Interior anchor `00332684` (the `00369CF0` call).

## SWE2-EC7-38 update (2026-09-19) - `005049E0`

`005049E0` (470 B) is a section-addressing body - `01CEBBA8`/`008C5B40`, `006C0520` triple plus `0046D110`. Interior anchor `00504A7F` (a `006C0520` call).

## SWE2-EC7-46 update (2026-09-19) - `00520010`

`00520010` (228 B) is a record-pool sibling - `0020E600`/`003AB7F0` plus a `call r12` register call. Interior anchor `0052004B` (a `0020E600` call).

## SWE2-EC7-62 update (2026-09-19) - `0051F580`

`0051F580` (146 B) is a resource-section body - `003AB7F0` single call. Interior anchor `0051F5C7` (a `003AB7F0` call).


## SWE2-EC7-76 update (2026-09-19) - `003697C0` bitmask-gated slot clear measured

`003697C0` (47 B) is the `022D89B8` bitmask-gated clear: `bt` of bit
`ecx` on the dword gates, `ecx <= 0xE` bounds, then `022D7FD0 +
ecx*0xA8` record `+0x62` is zeroed - the resource-slot flag reset the
section readers share. (The `ecx > 0xE` fall-through writes
`byte[0x62]` - a degenerate path taken literally.)
Interior anchor `003697E4` (the `+0x62` byte store).

## SWE2-EC7-84 update (2026-09-20) - `00426950` + `00424010` measured

`00426950` (78 B) is the `word[+4]`-chain drain the section callers
run: from `dword[global+0x48800]` (`-1` early-out) it walks
0x740-stride records calling `0042DA30(rec)` on each until the
`word[rec+4]` link hits -1.
Interior anchor `0042697E` (the `0042DA30` call).

`00424010` (39 B) is the vec3 store + flag reset the same callers
run: bit 1 of `+0x4B7` clears, `xmm1`/`xmm2`/`xmm3` land at
`+0x2B0`/`+0x2B4`/`+0x2B8`, and `byte[+0x4B6]` zeroes - call-free.
Interior anchor `00424017` (the `+0x2B0` `movss`).

## SWE2-EC7-85 update (2026-09-20) - `0042DA30` PCF-section resolve measured

`0042DA30` (466 B) is the section-resolve the `00426950` chain drain
runs per record: `+0x284` bit 2 gates; `word[+0x408]` resolves through
`[+0x10]+0xD90` -> `00409F50` -> `00409660(tag 0x50434640, rec+0x3C)`
into `+0x400` (+0x30 when found); on a live `00422D50` probe the
`+0x68`/`+0xD8`/`+0xF0` ids run `0020E600`+`003AB7F0` into `+0xE0`/
`+0xF8` and `0020E620`-registered counts into `+0x69C`/`+0x558`/
`+0x560`; the dead arm zeroes `+0x400`/`+0x558`/`+0x560` and clears
`+0xF0`/`+0x68`/`+0xE0`/`+0xD8`/`+0xF8`; `+0x42C`/`+0x430` re-register
through `0020E620` whenever their resolve comes back null.
Interior anchor `0042DA78` (the `00409660` tag find).

`003E1C50` (2992 B) is the record walk `003713C0` runs: null `rcx` bails whole, `0020E600([rcx+0x70])` resolves, `word[+0x68] = -1` folds to 0, then a 137-call `0020E600` + 95-call `0020E620` walk over the section's records with `0051B850`, `004719B0`, `005161D0`, `00421D20`, `0040EEA0` - the dense resolution body behind the section address pass.

Interior anchor `003E2285` (function `003E1C50`).

`00421D20` (70 B) is the keyed chain walk `003E1C50`/`003E3CA0`/`003E3D70` share: `ebx = [rcx+0x18]` bails 0 on -1, `0020E600([rcx+0x10])` resolves, `002ED570([rax+0xD98], ebx)` looks the key up, and a non-null hit tail-jumps `0020E600([rax+0x84])` - a two-hop resolved-record chase.

Interior anchor `00421D31` (function `00421D20`).

`0040EEA0` (1252 B) is the relocation pass `003E1C50` and `0054A9C0` share: `0020E620`/`0020E600` chains rebase `[rdi]`'s stored offsets into resolved pointers, then a `byte[rdi+4]`-counted loop walks the `+8` table rebasing each entry (`0020E600` x42, `0020E620` x28, `003D8E50` x2 total) - the fixup body behind the section address pass and the `+0x148` sub-record init.

Interior anchor `0040F0BC` (function `0040EEA0`).

`00415A80` (1117 B) is the record-resolve walk `003E1C50` runs inside its dense loop: `0020E600([rcx])` resolves the head, `0020E620(edi+rax)` lands the result at `[r13]`, then a `byte[r13+4]`-bounded walk from `rax+0x1C` runs `0020E600` x42 and `0020E620` x26 over the sub-records - the per-record resolution half of the section address pass.

Interior anchor `00415A91` (function `00415A80`).

`0041F340` (1006 B) is the record walk `0041FCF0` runs: `byte[rax+1]` gates each step, `byte[r14+0x5D]`/`byte[r14+0x5C]` feed the fields, `0020E600` x14 resolves with `00409F50` x3/`00409660` x2/`00409FA0`/`00409240`, and `003712E0`, `003E6D10` x2, `003E55F0`, `003AB8B0`, `003AB7F0` x2, `003AB910`, `0046E4D0`, `002ED570`, `003E6CF0`, `0051D220`, `00372350`, `00373100`, `004780C0`, `00421CD0`, `003B3550` with `00861EC0`/`00861EBA` copies - the section pass's heaviest single-record walker.

Interior anchor `0041F527` (function `0041F340`).

`003B3550` (642 B) is the publish-and-register `0041F340` calls: `0036C1D0`/`0024F610` look the section record up, `003B3400` resolves the twin, and `byte[+2] & 4` publishes `rbx` plus its `+0x18`/`+0x38`/`+0x840`/`+0x848`/`+0x850` fields to `02F97340`/`02EBEF70`/`+0x20`-stride globals; `003AB7F0` + `+0x858` bounds the span for `0024D970`, then `00861EC0` + `word = 0x103` + `0024B270` seed the stack record and `byte[+0x30]`, `word[+0x368]`/`+0x36A` get masked - the section table's address install.

Interior anchor `003B3585` (function `003B3550`).

`0024D970` (73 B) is the rebase-and-register `003B3480` and `003B3550` call: `ebx = edx - dword[rcx+0x858]` rebases the incoming offset, `003AA3D0`/`003A9BA0`/`003A9860` each take `ebx`, then `qword[+0x858] <- rsi` stores the new base - the section's offset rebase.

Interior anchor `0024D996` (function `0024D970`).

`003AA3D0` (92 B) is the kind dispatch `0024D540` and `0024D970` call: `02EBEF70`'s list head, each node's `byte[+0xE]` selects `00501420` on 0x52 or `00503F10` on 0x56, and `0020E600([rbx])` walks the next id - the section list's per-kind rebase.

Interior anchor `003AA414` (function `003AA3D0`).

`003A9BA0` (105 B) is the pointer rebase `0024D540`/`0024D970` call: `rsi = movsxd ecx`, `rbx` strides 8 from 8 to 0x1800 over `02EBEF78`'s table, each non-null slot takes `005004C0(rsi+rax, esi)` then `qword[rbx+rcx] += rsi` - the table's delta fix-up.

Interior anchor `003A9BD9` (function `003A9BA0`).

`003A9860` (105 B) is the twin rebase on the sibling table: same `rsi = ecx`, stride-8 shape but bound 0xA00 over `02EBEF90`, with `00442460` per non-null slot and the same `qword += rsi` store - the second table's delta fix-up.

Interior anchor `003A9899` (function `003A9860`).
