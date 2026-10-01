---
system: .seb — the SE block index behind each whole-block sound-effect bank
category: 18-Audio
status: AUDITED
owner_layer: PrimaryOwner:Audio
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 15 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "248 / 248 .seb in the archive index, all opened, 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "seb"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-seb-block-index-pass-1
  crossref_clean: false        # 2026-09-30 (SWE2-DATA): false until the pass-22 UNACCOUNTED NEIGHBOUR findings are accounted (FRONTIER-REQ-SWE2-DATA-PASS22-DEBT; OPUS-REQ-DATA-PASS30-CROSSREF-CLEAN-0930)
  reopened_count: 0
---

# `.seb` — the SE block index

> A 128-slot index for one numbered block of sound effects (`se000`, `se200`–`se434`, …). When an
> actor's resources ask for an SE block, the game loads `ps2data/sound/se/block/se<n>.seb`, registers
> it once in a 64-entry block registry, and builds a `SebAudioBank` from it — which reads the block's
> present slots and opens the real audio, `ps2data/sound/se/sead_data_win/se<n>/se<n>.win.sab`.

**Corpus validation.**

| | |
|---|---|
| files examined | **248 of 248** `.seb`, all opened |
| numbers shipped | `se000`, `se002`, `se007`, `se200`–`se434`, `se700`–`se709` |
| size | 708 B – 24,968 B |
| magic `SeBlock ` (8 bytes) | **248 / 248** — not checked by the reader |
| `+0x08` block id = the number in the file name | **248 / 248** |
| `+0x0A` slot count | **128 in 248 / 248** |
| `+0x0C` = file size | **248 / 248** |
| offsets ascending and in bounds | **248 / 248** |
| present slots per file | 15 (106 files), 12 (73), 32 (29), 31 (21), 13 (11) … one file with 123; 4,404 in all |
| the block's `se<n>/se<n>.win.sab` exists | **248 / 248** |

Census: [`census.py`](../../_experiments/evidence/seb-se-block-index/census.py) →
[`census.out.txt`](../../_experiments/evidence/seb-se-block-index/census.out.txt).

---

## 1. What the player sees

**Sound effects that come with an actor's resources rather than with the map.** The PS2 game grouped
sound effects into numbered blocks and let an actor-resource record name up to three of them. The remaster keeps those block files as small
indexes and plays the actual sounds from a `.sab` bank of the same number.

## 2. The layout

```struct SebHeader base=file size=0x210
+0x00  char[8]   magic      'SeBlock ' in 248 of 248 - not read
+0x08  i16       blockId    equals the file number in 248 of 248
+0x0A  i16       slotCount  128 in 248 of 248
+0x0C  u32       fileSize   equals the file size in 248 of 248
+0x10  i32[128]  slotOffset relative to +0x210; -1 = empty slot
```

A present slot's data starts at `0x10 + 4·slotCount + slotOffset`. The initialiser reads the first
five bytes there — a `u32` and a `u8` — and nothing else; the bytes after them are the PS2 block's
per-slot data, which nothing on PC reads (`UQ-256`). *The `u32` is dead too — write-twice, read-never
(§7, UQ-255); the `u8` is the authored flag byte the play path actually consumes.*

## 3. The loader contract

### 3.1 Which block an actor asks for

`002E60F0`, a step of an actor-resource state machine, takes the record `002ED950` resolves for the
entry's `+0x14` and reads up to three `u16` block ids from it (`002E6157`, one per pass, three passes,
`002E621D`). An id with bit 15 set means "none". Each id becomes a path-table index for resource
kind **32** (`002E6166`–`002E618E`):

```c
index = (id == 0) ? 0 : (id == 1) ? 1 : (id == 2) ? 3
      : (id < 500) ? id - 192 : id - 392;
size  = ResourcePath_Size(32, index);            // 0032E400 at 002E61A8
```

The kind-32 path array (pointer at `01E7FCF0`, 608 entries) is ordered `se000, se007, se001 … se006,
se200 … se499, se700 … se999`, so the rule sends ids 0, 1 and 2 to `se000`, **`se007`** and `se002`,
ids 200–499 and 700 and up to the file with the same number — exactly the numbers that ship. Ids 3–199
and 500–699 would index outside the matching run (§7).

> **The two bands fail differently (measured 2026-09-13, §6).** Ids **3–199** compute a
> **negative** index — `3 → −189`, `10 → −182` — so they address *before* the array, not
> elsewhere in it; only `199 → 7 → se006` lands inside at all. Ids **500–699** land **inside**
> the array on the wrong file: `500 → 108 → se300`, `600 → 208 → se400`, `699 → 307 → se499`.
> One band is an out-of-bounds read, the other a silent wrong load. A missing file gives size 0 and the step
records `-1` for that id (`002E61B8`–`002E61C9`).

The file is loaded into an arena block (`0036B160`, `0036A0B0`) with `0032E620(32, index)`
(`002E6277`), then registered by `003A1650`.

### 3.4 How a sound id decomposes into a block and a slot

*(2026-09-15, OPUS. This section exists because nothing joined the id arithmetic in code to the
index this document describes, and the two halves were being read separately.)*

§3.1 goes one way — a **block id** becomes a path-table index and names a file. This is the
other way: how a **sound id** becomes a *(block, slot)* pair in the first place.

**`003A1180` (111 B) builds the id, and the arithmetic is one shift and one add.** Its argument is
the **slot**, not the block:

```asm
003A11D7  shl  edx, 9        ; edx = the block word from the handle table
003A11DA  add  edx, ebx      ; ebx = the caller's argument, the SLOT
```

so **`id = (block << 9) + slot`**, and therefore `block = id >> 9`, `slot = id & 0x1FF`.

> **Restated 2026-09-26 (OPUS), on `FABLE-CONTRA-OPUS-SEB-ID-BLOCK-FIELD-IS-THE-REGISTRY-INDEX`:** the "block" in
> `id >> 9` is the **SE-block registry index** (0..63), not the `.seb` block number `n`.
> - **The id side.** The handle's low word `k` indexes the `0x18`-stride registry at `02AEEDC0`. Validation
>   (`003A11AB`–`003A11D1`) requires `(word +0xA << 16) | word +8` to equal the handle with bit 31 cleared, so the entry's
>   `word +8` equals `k`, its own index. That word is what `003A11D7` shifts left by 9.
> - **The loader side.** `003A1650` passes the same `word +8` to `002DEF00`, which masks it `& 0x3F`
>   (`002DEF00 and ecx,0x3f`) and hands it, with the file's own `word +8` (`n`, `002DEF0B`), through `001DBD20` →
>   `00210B60` → `0021B430` to `00223AD0(bank, idx, n, …)`. That call stores the index at **bank `+0x3C`**
>   (`00223C83`) and `n` at **bank `+0x38`** (`00223C9C`). Its entry check compares `n` with the file's `word +8`
>   (`00223B53`–`00223B59`).
> - **The lookup side.** `0021B5B0` matches `id >> 9` against bank **`+0x3C`** (`0021B5DF sar edi,9` /
>   `0021B5FA cmp [r10+0x3c],edi`), and `0021B430` finds an installed bank the same way (`0021B476`).
>
> So `id >> 9` names a registry slot, and the file `n` is reached only through that slot's bank (`+0x38`). The
> arithmetic above stands with "block" read as the registry index. The sentence below that took the field as `n` is
> corrected in place.

**The block is runtime state, and the function validates it rather than trusting it.** It reads the
packed handle at **`02AEF3FC`** and returns `-1` when that is `-1`; the handle's low word indexes a
**`0x18`-stride table at `02AEEDC0`**, whose words at `+8` and `+0xA` are rebuilt into a dword that
must equal the handle with bit 31 cleared (`003A11AB`–`003A11D1`), and a negative low word is
rejected. Only then is the id formed.

> ⚠ **The id-space stride is 512; this index has 128 slots. They are different numbers and
> both are right.** `+0x0A` is **128 in 248 / 248** files (§5), while the shift reserves **512**
> id positions per block. So **positions 128–511 of every block's id range are not addressable
> through this index** — the id space is deliberately sparser than the table.
>
> **The two call sites in evidence both fall inside 128**, which is what makes the join safe rather
> than a coincidence of arithmetic: `0030C831 mov ecx, 7` (the level-up fanfare, `UQ-135`) and
> `00366892 mov ecx, 0x52` = 82 (the R2 force-fight toggle, `UQ-149`). Both then play through
> `002DF220(id, pan 0x40, volume 0x7F)` — the same idiom, differing only in the slot.

**What this does and does not settle.** ~~Given a block number, this index resolves a slot to real
audio at `sead_data_win/se<n>/se<n>.win.sab` (§3.3).~~ *Corrected 2026-09-26 (OPUS): `id >> 9` is a registry index,
not a block number. Given the registry slot, the bank installed there carries the file's block number `n` at `+0x38`,
and through `n` this index resolves a slot to real audio at `sead_data_win/se<n>/se<n>.win.sab` (§3.3).* What it cannot
settle is *which registry slot, and so which block, is live* at a given call, because that comes from the runtime handle above — which is exactly the
residue `UQ-149` names as *“the runtime bank slot as well as the `sead` bank data”*, and it
is named there correctly.

### 3.2 Registration — `003A1650`

`003A0C90(blockId)` looks the id (`+0x08`, read by `002DEC10`) up in a 64-entry registry of 24-byte
records at `02AEEDC0`: a hit increments the record's use count (`+0x0E`) and the new file is released;
a miss claims a record, stores the loaded handle (`+0x14`) and marks it in the bitmap at `02AEF3F0`,
and calls `002DEF00(slot & 0x3F, blob)` → `001DBD20` → the Seb controller's load (`0021B430`), which
builds a `SebAudioBank` and initialises it with the blob (`00223AD0`).

### 3.3 The bank's read — `00223AD0`

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | — | — | **yes — no reader; the string `SeBlock` does not occur in the image** |
| `+0x08` blockId | `00223B53` | **no** — the comparison with the requested id feeds `_guard_check_icall` (`00223B5F`), a checking stub, not a branch | — | — |
| `+0x0A` slotCount | `00223B72`, `00223BBA` | — | none — a count above 128 walks past the table | — |
| `+0x0C` | copied with `+0x00..+0x0F` to the bank (`00223C76`) | — | — | no reader of the copy found here |
| `+0x10` slotOffset[n] | `00223B94` | **−1 → slot skipped** | — | — |
| slot `+0x00` u32 | `00223BC5`, `00223BD6` (into the node, twice) | — | — | **yes downstream — no consumer reads either copy** |
| slot `+0x04` u8 | `00223BCC`, `00223BDE` (into the node, twice) | — | — | consumed as flags — `§7`, UQ-255 |
| slot bytes after `+0x05` | — | — | — | **no reader in the initialiser** |

For each present slot the bank allocates a 10-byte node (`00220CD0`) holding the `u32` and `u8`
twice (`+0x00/+0x04` and `+0x05/+0x09`) and files it in its map under the slot number. *The second
half is the mutable half: `+0x09` is a live state byte re-seeded from the authored `u8` at every
start (`00224766`–`0022477C`), not a verbatim shadow — see §7.* It then stores
the requested block id at bank `+0x38`, formats the bank path with `"%s/se%03d/se%03d%s"` (`00908A38`) from
`PS2Data/sound/se/sead_data_win` (`00908950`) and `.win.sab` (`00908998`), and queues that bank's
load with completion `00222200` (`00223CB1`–`00223D05`).

**The write path.** None; authored offline.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `002E60F0` | actor-resource step: SE ids → kind-32 load | ✅ full body |
| `003A1650` | SE block registration | ✅ full body |
| `003A0C90` | the 64-entry block registry lookup/claim | ◐ |
| `002DEC10` | reads `+0x08` | ✅ full body |
| `002DEF00` → `001DBD20` → `0021B430` | into the Seb controller | ✅ full bodies |
| `00223AD0` | `SebAudioBank` initialiser | ✅ full body |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01E7FCF0` | kind-32 path array | `.data` | 608 `PS2Data\sound\se\block\se<n>.seb` pointers |
| `02AEEDC0` | SE block registry | `.data`, 64 × 24 B | id `+0x04`, handle `+0x14`, use count `+0x0E` |
| `00908A38` | `"%s/se%03d/se%03d%s"` | `.rdata` | the bank path format |
| `00908950` | `"PS2Data/sound/se/sead_data_win"` | `.rdata` | bank root |

## 5. Corpus survey

Every header field in §2 holds in all 248 files. Present slots are sparse in 247 files (the one block
that fills slots 0…n−1 without a gap is **`se407`**; the file with 123 present slots is **`se000`**).
In the 4,404 present slots the `u32`'s low byte is 2 in 3,541, 1 in 674, 4 in 134 **— and eight
further values in the remaining 55 slots; the `u8` is 0 in 2,647 and 128 in 1,574 — and five
further values in the remaining 183** (corrected 2026-09-13, §6). The 248 banks the rule addresses are the
single-name `se<n>/se<n>.win.sab` files; the other `sead_data_win` banks (4,345 in all, names like
`se001001.win.sab`) are not reached by this route.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full.)*

### The corpus reproduces exactly, re-walked from the archive

Re-extracted from `FFXII_TZA.vbf` and censused with independent code rather than by re-reading
`census.out.txt`: **248** `.seb`; magic `SeBlock ` **248/248**; `+0x08` = the file number **248/248**;
`+0x0A` = **128** in **248/248**; `+0x0C` = the file size **248/248**; offsets ascending and in bounds
**248/248**; a matching `se<n>/se<n>.win.sab` **248/248**; sizes **708 – 24,968 B**; **4,404** present
slots with the histogram **15 × 106, 12 × 73, 32 × 29, 31 × 21, 13 × 11**; the number set exactly
`se000, se002, se007, se200–se434, se700–se709`; **4,345** `sead_data_win` banks of which **248**
carry the single-name shape. Two the page leaves unnamed: the 123-slot file is **`se000`** and the one
contiguous file is **`se407`**.

§3.1's index rule reproduces against the array, including its odd middle:
`0 → se000`, `1 → `**`se007`**, `2 → se002`, `200 → se200`, `434 → se434`, `499 → se499`,
`700 → se700`, `709 → se709`. The kind-32 array is **608 entries**, indices 0–607 ending at
`se999.seb`, with a NULL at 608 and another kind's paths from 609 — exactly as stated. *(A first count
of 609 was my own terminator being counted as an entry.)*

### ⚠ §5's two value lists are truncated, and the omitted values are the interesting ones

§5 reads as a complete enumeration and is a partial one:

| field | §5 | measured |
|---|---|---|
| `u32` low byte | 2 × 3,541, 1 × 674, 4 × 134 — **4,349 of 4,404** | **eleven** values: those three plus **130 × 29, 131 × 9**, 3 × 7, 6 × 5, 8 × 2, 16 × 1, **132 × 1**, 7 × 1 |
| `u8` | 0 × 2,647, 128 × 1,574 — **4,221 of 4,404** | **seven** values: those two plus 1 × 133, 4 × 33, 5 × 11, 17 × 5, 8 × 1 |

> **The omissions are exactly the evidence `SB-1` needs.** `130`, `131` and `132` are `0x82`, `0x83`,
> `0x84` — the low bytes **2, 3, 4 with bit 7 set** — and the `u8`'s `128` is `0x80` against `0`. A
> field whose values are a small set *plus the same set with the high bit on* is a value-with-a-flag,
> and the three-and-two-value lists are precisely what hides that. The whole `u32` takes **15**
> distinct values across the corpus.

### The absence claim holds, with two controls

*"The string `SeBlock` does not occur in the image"*: `SeBlock `, `SeBlock` and `SeBlock\0` all occur
**zero** times in the whole file. **Controls:** `scnf` — a magic this chapter's sibling page shows is
carried in a tag table — occurs **once**, and `SRYK`, the BigFile magic that *is* compared, occurs
**once**. A four-byte-or-longer magic that a reader compares against shows up; this one does not.

**Not claimed.** `SB-1` stands: what the `u32` and `u8` *mean* is still unread, and the bit-7 pattern
above is a shape, not a semantic. `SB-2` stands: whether ids 3–199 or 500–699 are ever authored was
not searched for — only what the rule would do with them. *(Answered 2026-09-25 (UQ-257): none is authored,
and every authored id lands on its own file.)* §3.2 and §3.3's code readings were taken as
read; this pass re-derived the corpus, the array, the rule and the absence claim, not the
registration or the bank initialiser. The archive was **read, never written**, and nothing was
executed.

## 7. What this document does not claim

- [x] ~~**UQ-255.** What a slot's `u32` and `u8` mean, and how the Seb bank uses the two copies in its node. `SB-1`.~~
      ***ANSWERED 2026-09-27 (SWE2-DATA): the `u32` is dead-authored PS2 carryover (never read, both copies);
      the `u8` is an authored flag byte whose start-path semantics are decoded below; `+0x09` is a per-start
      state byte derived from it — not a verbatim shadow.***
      ***The "two copies" half is ANSWERED 2026-09-22 (FABLE): the bank does not use two copies — it uses ONE,
      and the `u32` it never reads at all.*** `SebAudioBank`'s vtable is at `00907D80`, resolved from its RTTI
      (`.?AVSebAudioBank@@`), and **five of its eleven slots walk the node map** at bank `+0x60`/`+0x70`, keyed
      on the slot number at `[entry + 0x20]` with the node pointer at `[entry + 0x28]`. Every one of the five
      reads **the byte at node `+0x09` — the SECOND copy of the slot's `u8`** — and **none of them reads node
      `+0x04`, the first copy, nor either `u32` at `+0x00` or `+0x05`.**

      | bank slot | body | test | acts when |
      |---|---|---|---|
      | `s1` | `00224A30` | `test byte [node + 9], 1` / `jne` | **bit 0 CLEAR** |
      | `s3` | `00224180` | `test cl, 0x68` / `jne`, then `test cl, 1` / `je` | **bits 3, 5, 6 all clear AND bit 0 SET** |
      | `s4` | `00223FA0` | `test byte [node + 9], 0x69` / `jne` | **bits 0, 3, 5, 6 all clear** |
      | `s5` | `00224360` | `test byte [node + 9], 1` / `jne` | **bit 0 CLEAR** |
      | `s6` | `002238F0` | `test byte [node + 9], 0x40` / `je` | **bit 6 SET** |

      > **CORRECTED 2026-09-22, same day, by its author.** This table first recorded `s3` as reading *"the
      > whole byte, passed on"* and gave no branch polarity, which left *"tests bit 0"* ambiguous. `s3` does
      > not forward the byte: it `movzx`es it and then applies **two** tests, `0x68` and bit 0. **And the
      > polarities differ** — `s1`, `s4` and `s5` act when their bits are **clear**, `s6` when bit 6 is
      > **set**. *A table of masks without polarities is half a reading.*

      ***So the `u8` is a FLAG byte***, and the five consumers partition on it: **bit 0 disqualifies `s1`,
      `s4` and `s5` and is REQUIRED by `s3`**, while **bits 3, 5 and 6 disqualify both `s3` and `s4`**. *That
      shape — one group acting on slots with bit 0 set and another on slots without — reads like a handled /
      unhandled split, but nothing here names it and it is not asserted.* **And one of those gates cannot fire on shipped data:** §6's corpus survey found the `u8` taking
      the seven values `0, 1, 4, 5, 8, 17, 128`, and **bit `0x40` is set in none of them**, so `s6`'s test at
      `002239A7` is dead for every one of the 4,404 present slots. *(`s4`'s `0x69` can still fire, through bits
      0, 3 and 5.)*

      ***And the `u32`'s second copy is read by nothing — measured 2026-09-22 (FABLE).*** The node's second
      `u32` sits at `+0x05`, an **unaligned** offset, which makes it a distinctive signature. An image-wide
      sweep for a `dword` access at displacement `+5` finds **eight reads in the whole executable, all of them
      `[rbp + 5]` inside two unrelated functions** (`0040EEA0`, `00415A80`) — stack frames, not this node —
      **and exactly one write, `00223BDA`, which is where the bank stores the copy in the first place.** So
      nothing reads it. *Bounded, not absolute:* a reader that first did `lea rcx, [node + 5]` and then
      dereferenced `[rcx]` would not appear in a displacement sweep, and 258 `lea` sites at `+5` exist
      image-wide; none of them is in the bank's five map-walking methods, which is as far as this goes.

      ***What stays open, and it is the larger half.*** **What the `u32` means is untouched** — no consumer
      among these five reads it, so its meaning has to come from somewhere other than the bank's map walk. The
      individual bit *meanings* are also unnamed: this establishes which bits are tested and by which method,
      not what any of them selects. And the scope is exactly those five methods; a reader of the node outside
      the bank's own map walk would not appear here.

      ***ANSWERED 2026-09-27 (SWE2-DATA, `SWE2-DATA-UQ255-SEB-SLOT-U32`), with one correction to the note
      above.*** The five vtable walkers are not the only map consumers — the enumerator's own
      key-compare-plus-payload shape finds **nine** bodies that resolve a node through the `+0x60`-head /
      `+0x70`-root map and read `[entry + 0x28]`: the initialiser `00223AD0`, the start path `00224570`, the
      five walkers FABLE listed, and three siblings (`002240B0` masking `0x69`, `00224290` reading `+9` for a
      `0x68`/bit-0 pair, `00224470` masking `0x01` — duplicate treatments of s4/s5/s3's tests). **The
      correction:** it is not true that nothing reads node `+0x04`. The start path `00224570` reads the
      *authored* u8 four times — `test [rsi+4], 8` (`00224657`), `test [rsi+4], 0x20` (`00224684`),
      `cmp byte [rsi+4], 0 / jge` (`002246E3`), and `movzx eax, [rsi+4]` (`00224766`) to derive `+9` — and it
      *writes* `+0x09` (`0022476E`, `0022477C`), so the second copy is re-seeded at every start, not just at
      bank init. Node `+0x00`/`+0x05` — both copies of the `u32` — are still read by none of the nine.

      **The `u32` is dead-authored on PC** — a write-twice, read-never field, carrying the same
      PS2-descriptor shape the rest of the slot tail carries (`UQ-256` proved bytes `+0x05`+ are unread too).
      Its packed bytes are `{b0: small value 1–16 with bit 7 as a flag, b1: 0xE0 in 4,403 of 4,404, b2: 0x01
      in 4,403, b3: 0 / 0x40 / 0x7F}` — a priority-and-volume-shaped PS2 driver word, kept structurally by
      the port. **The `u8` is the authored flag byte whose live half is `+0x09`.** Its consumed bits: bit 3
      (`0x08`, authored on exactly one slot) makes `00224570` abort the start when `00221F40` finds a playing
      object keyed `(id & ~0x1FF) | 0x80000007` — the block's slot-7 sound — unless this start *is* slot 7;
      bit 5 (`0x20`, never authored) routes through a second exclusion (`00210B30` → `00210710`); bit 7
      (`0x80`, 1,574 slots) selects the `007A7010`-checked arm, issues `007A7A20(obj, -1, 0.0)` when the check
      returns 3, and zeroes `+0x09`. The re-seed rule at `00224766`–`0022477C` is: bit 7 set → `+9 = 0`; bit 5
      set → `+9 = (u8 & 1) | 0x40`; else `+9 = u8` verbatim. So the walkers' tested bits are a *state* byte:
      authored bits 0 and 3 persist into `+9`, bit 6 marks "started through the bit-5 arm" (unreachable on
      shipped data — bit 5 is never authored), and **authored bits 2 (`0x04`, 44 slots) and 4 (`0x10`, 5
      slots) appear in no mask anywhere — dead-authored bits inside a live byte.**
- [x] ~~**UQ-256.** Whether any PC code reads a slot's bytes after `+0x05` (the PS2 per-slot data). `SB-1`.~~
      ***ANSWERED 2026-09-22 (FABLE): no, and the reason is REACHABILITY rather than a displacement sweep.***
      *A sweep for reads at `+0x05` and beyond cannot answer this — it cannot tell this buffer from any other
      structure at the same displacement. What can is that **the `.seb` buffer is held by exactly two functions and
      escapes neither.** It arrives as the fourth argument (`r9`) down a chain whose every link is read:*
      `001DBD20` *(tail-jump)* → `00210B60` *(a **9-byte** thunk, `mov rcx, [rcx+8]; jmp`, which does not touch
      `r9`)* → `0021B430` *(holds it in `r15` and uses it **exactly twice** — the null test `0021B4C8` and the call
      argument `0021B4F3`; its three virtual calls at `0021B492`, `0021B4BE` and `0021B4D3` all take `rsi`-derived
      arguments, never the buffer)* → `00223AD0`.
      ***Inside the initialiser the buffer is never stored and never passed on***, and every one of its **twelve**
      accesses to it is enumerated: `word +0x08` (file number, `00223B53`); `lea` of `+0x10` (`00223B6C`);
      `word +0x0A` three times (`00223B72`, `00223BBA`, `00223C54`); `dword [rsi]` twice, the offset array
      (`00223B94`, `00223BBF`); **slot `+0x00`** twice (`00223BC5`, `00223BD6`); **slot `+0x04`** twice
      (`00223BCC`, `00223BDE`); and `movups xmmword [rbp]`, the **16-byte header** copied into the bank object at
      `00223C93` (`00223C76`). *So the slot is read at exactly two displacements, and the largest displacement
      touched anywhere in the buffer is `+0x0F` — inside the header, before the offset array.* The 10-byte node the
      loop allocates holds the two **values** twice (`00223BC9`/`00223BD2` and `00223BDA`/`00223BE8`), **not a
      pointer back into the buffer**, so nothing downstream can follow one.
      **Bounds, stated rather than implied.** Each link has **exactly one caller**, and neither `0021B430` nor
      `00210B60` occurs as a stored pointer anywhere in the image, so no indirect call reaches them with a
      different buffer. **Not established:** what the loader that filled the buffer does with it before this chain,
      and whether `001DBD20`'s own callers retain it — the chain above `001DBD20` was not read. `SB-1`'s other
      half, what the `u32` and `u8` MEAN, is untouched by this and stays open as `UQ-255`.*
      *(The evidence was published on 2026-09-22 with this box left open, because
      [`OPEN-QUESTIONS.md`](../../_index/OPEN-QUESTIONS.md) then carried a peer's uncommitted rows and a closure
      must land on the page and the register in one commit. The tick and the row went together once that file
      was free.)*
- [x] ~~**UQ-257.** Which records `002ED950` returns the three SE ids from, and whether ids 3–199 or 500–699 are ever
      authored (the index rule would pick the wrong file for them). `SB-2`.~~ **ANSWERED 2026-09-25 (FABLE, Claude
      Opus 5.5).** The records are the **`charseinfo_<letter>` (CHSE) tables**, now traced rather than
      matched:
      - `002EA530` loads kind-9 ids 12–19 into `021641A8`…`021641E0`.
      - `002ED950` picks one by the letter in bits 16–23 of the actor resource id, and the row by the
        low 16 bits.
      - **No authored value lies in 3–199 or 500–699, and all 943 land on their own `se<n>.seb`.** See
        [the CHSE page](../../02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md#the-reader-traced--sb-2-answered-fable-claude-opus-55-2026-09-25).

## 8. Related

- [`.sab` — the sound bank container](sab-sound-bank-container.md) — the bank format each block opens.
- [How a sound request becomes a voice](../Audio-Boundary/how-a-sound-request-becomes-a-voice.md) — the `SebAudioBank` / `SebAudioController` classes.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Script_VM_Native_Bridge — CLIENT.**
  - The file-request pair `0032E400` / `0032E620` is also called by script-verb bodies (75 B and 115 B).
  - `0036B160` is called by a 174-byte verb body, and `003A0C90` by a 59-byte one.

  **Script verbs issue the same file requests.**
- **Presentation — CLIENT.** The same file pair is called by 119- and 337-byte Presentation bodies, and `0036B160` by a
  511-byte body.
- **Input — CLIENT.** The request `0032E620` is also issued by the 177-byte item-graphics loader.
- **CombatFormula — CLIENT.** §3.4 names `003A1180` and `002DF220`, and **both are also
  called by `003112F0`** (2,040 B), a battle-formula body. The crossing is that the formula layer
  plays sounds through the same resolve-then-play pair §3.4 describes; **nothing on this page
  depends on that body**, and the edge is recorded independently on
  [the shared-neighbours page](../../00-Engine-Core-Runtime/Shared-State-Accessors/the-shared-neighbours-pass-22-keeps-finding.md).
- **Rewards_Progression_Economy — CLIENT.** The same pair is called by **`0030C650`** (~~63 B~~ **570 B**; 63 bytes is its first unwind fragment, and the calls are at `0030C836`/`0030C84B` — 2026-09-29, OPUS, `CON-173`).
  Same class and same direction: the economy layer is a consumer of the resolver, not a participant
  in the index. The level-up fanfare that motivated §3.4's worked example (`UQ-135`) reaches the
  pair from this layer.

  *Both edges were added by §3.4 in the same commit and are accounted here because of it —
  `check_publish_neighbours` refused the first attempt at that section for naming the far ends
  without this paragraph, which is the guard working as intended.*

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Input — CLIENT.** `FUN_00291c80`, owned by that layer, calls `0032E620` on this page. That caller is a 177-byte walk of the table at `0209BEA0`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Platform — CLIENT (SWE2-EC7-166, 2 edges).** `005CD4F0`/`005CD820`,
the ordered-map helpers this page's `0020BE50` resolver uses, are also
called by `0019CC50` on the Platform layer. Shared container leaves.

**Resource — CLIENT (SWE2-EC7-166, 103 edges).** `001D6B40`, the caller
of this page's `0020BE50` mount resolver, sits inside the Resource
layer's request path - it calls `0020BE50`/`0020C700` and is called by
`002DF6C0`/`002DF780` there (+99 more of the same shape). The index is
consulted by the resource queue; not a shared responsibility.
## SWE2-EC7-44 update (2026-09-19) - `0021B430`

`0021B430` (268 B) is a body - `0016D6A0`/`002129F0`/`00212A70`/`00223AD0` plus `call [rax+0x18]`/`[rax+0x30]` vcalls. Interior anchor `0021B45D` (an `0016D6A0` call).


## SWE2-EC7-65 update (2026-09-19) - `002ED950`

`002ED950` (134 B) is a call-free CHSE-candidate jump-table leaf - `jmp rcx`, arms `mov rcx,[021641A8]`/`[021641D0]`/`[021641D8]`/`[021641B8]` -> `jmp 002ED9BD`. Interior anchor `002ED975` (the `jmp rcx` dispatch).


## SWE2-EC7-93 update (2026-09-20) - `0036D200` + `0036A0B0` measured

`0036D200` (60 B) is the flag-clear the `002E60F0` block-index caller
runs: `ecx` must be nonzero, `ecx & 3` nonzero, `>= 0x100000`, and
`ecx & ~3` nonzero before `[rax+8]` is dereferenced - then the
object's byte `+0x15` loses bit 2 and its word `+0x3E` is zeroed.
Interior anchor `0036D21D` (the `[rax+8]` object fetch).

`0036A0B0` (79 B) is the set-side sibling over the same validation:
identical `ecx` gates resolve `[rdx+8]`, then `+0x15` gains bit 2,
`+0x3E` is zeroed, and the body returns `rdx + 0x40` (or 0 when the
record fails validation).
Interior anchor `0036A0E9` (the `or al, 4` flag set).

## SWE2-EC7-110 update (2026-09-20) - `001D6B40` measured

`001D6B40` (34 B) is the
two-call query `00223AD0`,
`002DF6C0` and `002DF780`
run: `0020C700()` fetches
the dictionary context,
`0020BE50(context, rcx)`
runs the real lookup, and the
`movzx` byte answer returns -
the name/block membership
probe the sound-bank pages
share.
Interior anchor `001D6B49`
(the `0020C700` context
fetch).

`0020BE50` (334 B) is the mount-prefix resolver `001D6B40` calls: strips `/hostapp/` (9 chars) or `/app0/`/`/host/` (6) from the path, canonicalizes into a 0x100 buffer via `00861EC0`, `0020C440` resolves it, `00674A00` hashes the result, then an ordered-map walk over `rsi+0x28`/`+0x38` (`005CD4F0`/`005CD820`) registers or finds the entry by hash - the file path normalization half of the block-index lookup.

Interior anchor `0020BEBD` (function `0020BE50`).

`0020C440` (273 B) is the path canonicaliser `0020BE50`/`0020C1B0` run on the copied name: the leading-edge scan skips bytes until the first `a`-`z` or a `char - 0x30` bit set in `0x7FFFFFE03FF` (the digit-and-symbol band), interior `/` rewrites to `\`, a doubled `\` passes untouched, and every other byte maps through the `008C2FF0` import into `rsi`'s buffer; the tail NUL-terminates and strips trailing spaces - the mount resolver's name-normalising pass.

Interior anchor `0020C4F7` (function `0020C440`).
