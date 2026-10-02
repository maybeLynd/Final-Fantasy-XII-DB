---
system: How the BigFile index loads, and how it is verified
category: 02-Resource-And-Asset-Pipeline
status: DOCUMENTED — the per-entry record layout is read (§3a, SWE2-CONTRACT DD batch 9: {u32 firstBlock, u32 copy, u64 size, u64 offset, u64 nameOffset}, keys are the names' MD5) (owner re-status 2026-09-30, OPUS; was: the per-entry record layout inside the index is not read (§7))
owner_layer: PrimaryOwner:Resource
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  parent_tag: GN159
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-bigfile-index-pass-1
  crossref_clean: false
  reopened_count: 0
container_format: vbf-bigfile-index
---

# How the BigFile index loads, and how it is verified

> The engine calls it a **BigFile**. It opens `FFXII_TZA.vbf` with plain CRT `fopen`, reads the
> **entire index in one `fread`**, closes the file, and then **MD5s the index and compares it against
> the last sixteen bytes of the archive.** A modder who changes the index must recompute that digest;
> one who changes only payload bytes need not.

**PARTIAL.** The container header, the load sequence and the integrity check are read at tier 1.
~~**The per-entry record layout inside the index is not read here** (§7).~~
*Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): the per-entry record layout is now read from the code that parses
it and checked against the installed archive, field by field, in §3a.*

## 1. What the player sees

A thirty-one-gigabyte file that opens instantly, and a game that fails to start rather than
misbehaving if that file is edited carelessly. Both come from §3.

## 2. The engine's own name for it

```
009038C8   "BigFile head wrong!\n"
008C586B   "FFXII_TZA.vbf"
008F9AC4   "rb"
```

The failure path on a bad magic prints **`BigFile head wrong!`**, so *BigFile* is the developers'
term. The document's other name for the format, `SRYK`, is the four bytes of the magic itself.

## 3. The load sequence, in full

`FUN_001F4340(archive, path)` — owner `Resource`, 991 bytes — is the whole opener, and every step is
an imported call, so the sequence is unambiguous:

> **This listing stops one step early (noted 2026-09-13, §10).** After `CryptReleaseContext` the
> function **compares** the two digests, half by half, and takes one of two exits. Both are read
> in §10, which is where §7's second unknown is answered.

```c
archive[0x78] = alloc(0x104);                       // MAX_PATH
strcpy(archive[0x78], path);
f = fopen(archive[0x78], "rb");                     // CRT stdio, not Win32
if (!f) return;

fread(&magic, 4, 1, f);
if (magic != 0x4B595253) { Error("BigFile head wrong!\n"); return; }   // 'SRYK'

fread(&indexSize, 4, 1, f);                         // the second dword

_fseeki64(f, -16, SEEK_END);
fread(&storedDigest, 16, 1, f);                     // the LAST 16 BYTES of the archive

archive[0] = alloc(indexSize);
fseek(f, 0, SEEK_SET);
fread(archive[0], indexSize, 1, f);                 // the whole index, from offset 0
fclose(f);                                          // <- closed before anything is verified

CryptAcquireContextW(...);
CryptCreateHash(prov, 0x8003 /* CALG_MD5 */, 0, 0, &h);
CryptHashData(h, archive[0], indexSize, 0);
CryptGetHashParam(h, 2 /* HP_HASHVAL */, digest, &len /* = 0x10 */, 0);
CryptDestroyHash(h); CryptReleaseContext(...);
```

Four facts follow that are not obvious from outside:

- **The index is read from offset 0**, so the buffer that gets hashed **includes the magic and the
  size dword**. The digest covers the first `indexSize` bytes of the file, not a sub-range of them.
- **The digest lives in the last sixteen bytes of a 31 GB file** — nowhere near the data it protects.
- **The archive is closed before the check runs.** The integrity test is on the in-memory copy.
- **`fopen`, not `CreateFile`.** The whole open path is CRT stdio.

## 3a. The index layout, field by field (SWE2-CONTRACT, 2026-09-30)

*DD batch 9. Read from the opener `001F4340` after the digest check (`001F453B`–`001F4683`), the digest-tree insert
`001F4720` / `001F3FD0`, the lookup `001F47D0`, the read planner `0019A770` / `0019A860` / `0019AA20` and the stream
handle `00215110` / `00215220` / `00215280`. Every field is then measured on the installed `FFXII_TZA.vbf` (header
only, plus a three-entry payload sample). Record: [`swe2contract-ddres-b9-0930`](../../_index/candidates/swe2contract-ddres-b9-0930/README.md),
checker steps V1–V9 and A1–A9.*

The index is five parts laid end to end, all inside the `indexSize` bytes the MD5 covers:

| part | where | size | how the engine finds it |
|---|---|---|---|
| header | `+0x00` | 16 B | fixed |
| key array | `+0x10` | `count × 16` | `lea rdx, [r15 + 0x10]` (`001F453E`), `shl r12d, 4` (`001F4549`) |
| record array | after the keys | `count × 32` | `add r12, rdx` (`001F454D`), `shl rcx, 5` (`001F4550`) |
| name table | after the records | a `u32` length, then the names | `lea r13, [rcx + 4]` (`001F4554`); the length at `[r13 - 4]` counts its own 4 bytes (`001F455B` / `001F455F`) |
| block-size table | from the name table's end to `indexSize` | `u16` per 64 KiB block | stored at archive `+0x68` (`001F4566`) |

```struct VbfIndexHeader base=file size=0x10
+0x00  u32  magic      'SRYK' = 0x4B595253, the one compare (001F43D7)
+0x04  u32  indexSize  bytes read, hashed and kept - 11,995,716 in the shipped archive
+0x08  u32  count      entries - read as a dword (001F4542); 89,414 shipped
+0x0C  u32  _high      0 shipped; the engine never reads it (vbf_index.py reads +0x08 as a u64, which agrees only because this is 0)
```

```struct VbfIndexEntry base=record size=0x20
+0x00  u32  firstBlock   index of the entry's first 64 KiB block in the block-size table
+0x04  u32  firstBlock2  a copy of +0x00 - no engine reader found
+0x08  u64  size         the entry's uncompressed size in bytes
+0x10  u64  offset       archive byte offset of the entry's first stored block
+0x18  u64  nameOffset   into the name table, counted from its first name; rebased in place to a char* at load
```

**Key `i` belongs to record `i`.** The key is the MD5 of record `i`'s name (all 89,414 match, A3). The opener hands key
`i` (`lea rdx, [rdi + r9*8]` with `r9 = 2i`, `001F466C`) and a pointer to record `i` to the insert (`001F4677`). The
insert builds a red-black node `{three links, key at +0x18, record pointer at +0x28}` (`001F477E`, `001F4785`),
ordered as two **signed** 64-bit halves, `+0x18` first (`001F4008` / `001F4013`). The array itself is not sorted, so
a reader cannot binary-search it. The tree is the only index.

How to read each record field:

- **`+0x00` `firstBlock` (`u32`).** The entry's first entry in the block-size table. Its blocks are consecutive from
  there, `ceil(size / 65536)` of them. The engine reads it three times: the block count (`001F457D`), the last-block
  flag (`001F464B`) and the read planner (`0019A7AB`). Shipped entries are in block order, and each one starts where
  the one before it ends (A6).
- **`+0x04` (`u32`).** It equals `+0x00` in every entry that has bytes (89,388 of 89,388, A4). The 26 exceptions are
  the 26 zero-size entries (`jsondata/cutscenes/*.json`), where it reads `1,703,388`. The opener, the tree, the handle
  and the read planner never read it (V8). **A repacker should write it equal to `+0x00`.** Nothing read here
  depends on it.
- **`+0x08` `size` (`u64`).** The uncompressed size. Its low 16 bits are the tail block's length (`001F458F`,
  `001F463C`). The engine reads it for the block count, the tail flag, the read clamp (`00215143`), `SEEK_END`
  (`0021523E`) and the size getter (`00215284`). A zero-size entry returns 0 for any read, because the request is
  clamped to `size - position` = 0 bytes first (`00215149`–`00215150`).
- **`+0x10` `offset` (`u64`).** Where the entry's first stored block starts in the archive. The planner reads it
  (`0019A7AE`). To seek inside an entry, it adds the stored size of each whole block it skips (`0019A7D0`–`0019A7F4`).
  Shipped, it equals `indexSize` plus the stored sizes of every earlier block in all 89,388 entries with bytes (A5).
  The 26 zero-size entries hold an unused value. The payload runs from `indexSize` to 16 bytes before the end of the
  file, which is where the digest starts.
- **`+0x18` `nameOffset` (`u64`).** An offset into the name table, counted from its first name (`r13`, i.e. past
  the length word). The opener rebases it in place to a pointer (`add [r10 + 0x18], r13`, `001F462D`). No reader of
  that pointer was found (V8), because the lookup goes by the MD5 key, not by name. Names ascend with the entry
  index, and the whole name table is lower case (A7).

**The block-size table** holds one `u16` per 64 KiB block of the whole archive: 957,553 of them, which is exactly
the last record's `firstBlock` plus its block count (A2). Read each value like this:

- **0** means a full 64 KiB block stored raw (`0019A7E6`, `0019A8CD`).
- **The entry's `size mod 65536`, in an entry's last block**, means a tail stored raw.
- **Any other value** is the compressed length of a zlib stream that inflates to 64 KiB, or to the tail's length.

At load the opener turns the table into a one-byte-per-block "compressed" array at archive `+0x70`
(`001F45A1`–`001F45E1`, then `001F4658`–`001F4661` for the tails). The block reader then picks zlib's `uncompress`
(`0080C5A0`, zlib 1.2.11, `0019AAAE`) or a raw 64 KiB copy (`0019AA7D`) from that byte (`0019AA93`).
Shipped, 189,861 blocks are full raw blocks and 1,697 entries end in a raw tail (A8). A sample of three entries
decodes to its exact size under this rule: one all-zlib, one with a raw tail and one with full raw blocks (A9).

## 4. What the check does and does not protect

The hash input is `archive[0]` for `indexSize` bytes. **It covers the index and nothing else.**

> **Payload bytes are unprotected.** Replacing an entry's compressed data in place — same offset,
> same length — leaves the index unchanged, so the digest still matches and the game loads.
> **Changing the index in any way — adding an entry, moving one, changing a length — breaks it**, and
> the failure is at open, not at use.

That is the practical rule for anyone repacking this archive, and it is a consequence of *where* the
hash is taken, not of any stated policy.

## 5. After the index: how bytes actually arrive

The byte-delivery surface of the whole engine is small, and it was measured at the import boundary
rather than by name:

| Import | Sites | Owners |
|---|---:|---|
| `KERNEL32!ReadFile` | **3** | all `Resource` |
| `KERNEL32!SetFilePointer` | 2 | `Resource` |
| `KERNEL32!CreateFileA` | 2 | — |
| CRT `fread` | 17 | `Resource` 9, others 8 |
| CRT `fopen` / `_wfopen` / `_wfopen_s` | 12 / 1 / 8 | mixed |

**There is no memory-mapped path at all**: the image imports neither `CreateFileMapping` nor
`MapViewOfFile`. Every byte that reaches the engine does so through a `read`-family call.

Of the three `ReadFile` sites, `FUN_0059F4A0` is the one with reach — **12 callers across `Resource`
and `Audio`** — and it is a 92-byte leaf. `FUN_0059A9B0` and `FUN_0059D4B0` have one caller and none
respectively.

> **The index is loaded once and kept; the file handle is not.** `fclose` runs inside the opener, so
> every later read reopens or uses a separate handle. **What is cached is the index, not the file.**

## 6. Call chain

```
FUN_0019B070  (Resource, the only caller)
  -> FUN_001F4340        open, read index, close, MD5-verify
                         archive[0]    = the index buffer
                         archive[0x78] = the path string
later, per asset:
  -> FUN_0059F4A0        ReadFile leaf, 12 callers  (Resource, Audio)   <- corrected 2026-10-02, OPUS: archive blocks arrive through CRT fread instead, 0019A860+0x71 (§5 table)
```

## 7. What is not known

- [x] ~~**The per-entry record layout inside the index.** This document reads the *container* — magic, size,
  digest, and the single bulk read — and stops there. The entry structure is known operationally to
  `vbfextract.py` (see [the parent document](vbf-archive-and-st2e-tables.md) §1) but is **not read
  from the engine here**.~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): read, in §3a.* The index is a 16-byte header, `count` MD5 keys
  of 16 bytes, `count` 32-byte records `{u32 firstBlock, u32 copy of it, u64 size, u64 offset, u64 nameOffset}`, a
  name table with a self-counting `u32` length, and a `u16` block-size table. Each field is named by the instruction
  that reads it and checked on the installed archive. `vbfextract.py` and `vbf_index.py` agree with the engine on every
  field they use. The one field they leave unnamed (`+0x04`) has no engine reader and copies `+0x00`.
- [x] ~~**Whether the computed digest is actually compared, and what happens on mismatch.** The six
  CryptoAPI calls are read; the comparison that consumes `HP_HASHVAL` was not followed to its
  branch. **The check is present; its consequence is assumed, not read.**~~
  **ANSWERED 2026-09-13 (OPUS, §10): it is compared, and a mismatch returns `false` in silence.**
  `001F44FF`–`001F4535` compares both 64-bit halves; every failing test jumps to `001F4705`,
  which is `xor al, al` and the epilogue. **No message is printed** — `BigFile head wrong!`
  belongs to the magic branch only. The caller consumes it: `0019B0EA movzx esi, al` /
  `test al, al` / `jne`, and on failure frees the archive's `+0x20` through `001F4120`.
- [x] ~~**How a path or asset id resolves to an index entry** — the lookup between
  [the asset-category path directory at `0215F000`](vbf-archive-and-st2e-tables.md) and this index.~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): by the MD5 of the path.* `0019AEE0` hashes the caller's string
  with `CALG_MD5` (`0019AF2B`–`0019AF79`) and looks the digest up in each mounted archive's tree through `001F47D0`,
  its only caller (V5). The keys are the MD5s of the stored names (A3). The normalisation in front of that hash is
  [`how-a-path-is-resolved-to-bytes.md`](how-a-path-is-resolved-to-bytes.md) §6.
- [x] ~~**Where the archive is reopened** for payload reads, and whether a handle is pooled.~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): at open, into a pool of fifteen.* After building the tree, the
  opener allocates fifteen 0x30-byte reader handles (`0x2D8` = 8 + 15 × 0x30, `001F4687` / `001F4695`) and `fopen`s
  the archive path in each one (`001F46F2` → `00215290`, `"rb"`). A lookup takes the first free handle
  (`001F4290`–`001F42A2`). When all fifteen are busy it makes a sixteenth the same way (`001F42DC`–`001F4313`) (V9).
- [x] ~~**Whether entries are decompressed on read**, and by what codec.~~
  *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 9): yes, per 64 KiB block, with zlib.* Each block flagged
  compressed goes through zlib 1.2.11's `uncompress` (`0080C5A0`, from `0019AAAE`). Each other block is copied raw.
  The flag rule is in §3a (V3, V7, A9).
- [x] ~~What `FUN_005CCAB0` and `FUN_0079B1E0` open with `CreateFileA`.~~ **ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5): minidump files.** `005CCAB0` logs `Minidump file saved to %s`; `0079B1E0` formats `%s_%d_%d_%d_%d_%d_%d.dmp` and reports `Create dump file filed...`. They are the only two references to the `CreateFileA` slot (`005CCAE8`, `0079B298`), so no archive or asset open uses Win32 `CreateFile`. [Record](../../_index/candidates/pc1-config-route/README.md).

## Key addresses (SWE2-CONTRACT, 2026-09-30)

| address | role | section |
|---|---|---|
| `0019B070` | mounts one archive: allocates the `0xB0`-byte archive object, calls the opener, frees it on `false` | §6, §10 |
| `001F4340` | the opener: `fopen`, magic, `indexSize`, digest, the bulk read, MD5 compare, index parse, handle pool | §3, §3a, §10 |
| `001F4720` / `001F3FD0` | digest-tree insert: node `{links, key +0x18/+0x20, record +0x28}`, signed two-half order | §3a |
| `0019AEE0` → `001F47D0` | MD5 of the caller's path, then the digest-tree lookup across the mounted archives | §3a, §7 |
| `001F4250` | takes a free reader handle for the record (or makes a sixteenth) | §7 |
| `00214FC0` / `00215290` / `00215110` | reader handle: construct (64 KiB cache), `fopen` the archive, read clamped to the record's size | §3a, §7 |
| `0019A770` / `0019A860` / `0019AA20` | read planner: record `+0`/`+0x10` to a file offset, `fread` the stored blocks, inflate or copy | §3a |
| `0080C5A0` | zlib 1.2.11 `uncompress`, the codec of every compressed block | §3a, §7 |
| `0059F4A0` | the 92-byte `ReadFile` leaf (12 callers); the archive's own blocks arrive through CRT `fread` instead (`0019A8D1`) | §5 |

## Modding notes (SWE2-CONTRACT, 2026-09-30)

For a player, a repacked archive either loads normally or the game refuses it at start-up. The digest (§4) and the
field rules below decide which. To repack `FFXII_TZA.vbf` so that the engine reads it (§3a):

- **Give every entry a key equal to the MD5 of its lower-case, forward-slash name.** The lookup never compares
  names (§7).
- **Keep the blocks of each entry consecutive from `firstBlock`, and write `+0x04` equal to `+0x00`.**
- **Set `offset` to the archive position of the entry's first stored block.** It is an absolute file offset, not an
  offset past the index.
- **Store a block as a zlib stream,** with its compressed length in the block-size table, or store it raw. A raw
  block is written as 0 for a full 64 KiB block, or as exactly `size mod 65536` for an entry's last block. Any other
  value is treated as compressed. So a compressed tail whose stream happens to be exactly the tail's length would be
  read raw: store such a tail raw.
- **Recompute the MD5 of `[0, indexSize)` into the last 16 bytes** whenever the index changes (§4).

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| The index's five parts and their bounds (§3a) | `001F453B`–`001F4581` read in address order; checker V1–V2; the installed archive A1–A2 | 1 (static) + 9 (shipped archive) |
| The record fields `+0x00`, `+0x08`, `+0x10`, `+0x18` and what reads each (§3a) | V2–V6; structflow from every load of the handle's record pointer, V8 | 1 (static) |
| `+0x04` has no reader and copies `+0x00` | V8 (reads found only at `+0`, `+8`, `+0x10`); A4 over all 89,414 entries | 1 (static) + 9 (shipped archive) |
| Key `i` = MD5(name `i`); the tree is keyed by it | V4–V5; A3 (89,414 of 89,414) | 1 (static) + 9 (shipped archive) |
| `offset` = `indexSize` + the stored sizes before; the payload ends at the digest | A5–A6 | 9 (shipped archive) |
| The block-size table's three readings and the compressed-flag rule | V3, V6, V7; A8; A9 decodes three sample entries to their exact sizes | 1 (static) + 9 (shipped archive) |
| Fifteen pooled reader handles, a sixteenth on demand | V9 | 1 (static) |
| The codec is zlib 1.2.11's `uncompress` | V7 (the `"1.2.11"` version argument at `0080C5FD`); the zlib family in [`third-party-middleware-inventory.md`](../../23-Third-Party-Libraries/third-party-middleware-inventory.md) | 6 (upstream library) |
| Magic is `SRYK` = `0x4B595253` | `cmp dword ptr [rbp+0x50], 0x4B595253` at `001F43D7`, the only occurrence of those bytes in `.text` | 1 |
| The engine's term is "BigFile" | the error string at `009038C8`, referenced on the magic-mismatch branch | 1 |
| The load sequence | every call in `001F4340` resolved through the PE import descriptors, in address order | 1 |
| The digest is the last 16 bytes | `_fseeki64(f, -16, SEEK_END)` then a 16-byte `fread` | 1 |
| The index is read from offset 0 | `fseek(f, 0, SEEK_SET)` immediately before the bulk `fread` | 1 |
| The hash is MD5 over the index | `mov edx, 0x8003` (`CALG_MD5`) into `CryptCreateHash`; `CryptHashData(h, archive[0], indexSize, 0)` | 1 |
| The file is closed before verification | `fclose` at `001F4471`, `CryptAcquireContextW` at `001F4496` | 1 |
| Three `ReadFile` sites, all `Resource` | indirect-call census against the resolved IAT slot | 1 |
| No memory-mapped path | the import directory contains no `CreateFileMapping` or `MapViewOfFile` | 1 |

**Controls.** The import census keys on the **IAT slot address**, not on a function name or a call
convention — so it is immune to both hazards this session has been bitten by: a thunk cannot hide a
call that goes through the slot, and no naming convention is required. It does **not** see calls made
through a pointer copied out of the slot into a register or structure, which is the residual gap and
is why §5's counts are stated as sites, not as a guarantee.

The absence claim in §5 — no memory mapping — is a **directory-level** measurement: those names do
not appear among the image's imports at all, so no call site needs to be searched for.

`check_already_answered.py` was run before this block was started; the container-level load sequence
is not covered by the three existing documents in this category.

## 9. Related

- [`vbf-archive-and-st2e-tables.md`](vbf-archive-and-st2e-tables.md) — the archive census, the `st2e` table format, and the asset-category path directory.
- [`resource-section-addressing.md`](../resource-section-addressing.md) — how a loaded resource's sections are addressed once the bytes are in memory.
- [`authored-data-table-registry.md`](../authored-data-table-registry.md) — the registry the loaded tables land in.

## 10. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full, per
[`EVIDENCE-STANDARD.md`](../../_index/EVIDENCE-STANDARD.md) amendment 2026-09-13b. Neither
`001F4340` nor `0059F4A0` is cited outside this page and the address index.)*

### The integrity claim now closes against the archive itself, not only against the code

Every statement in §3 and §4 about the container is a claim about a file that is sitting on the
disk. It had never been checked against it. **It holds, exactly:**

| claim | measured on `FFXII_TZA.vbf` |
|---|---|
| magic is `SRYK` = `0x4B595253` | first four bytes **`53 52 59 4b`** |
| the second dword is the index size | **`0x00B70A44` = 11,995,716** |
| the digest is the last sixteen bytes | **`b7 41 87 bd 5c 88 f5 64 28 1d c2 90 ab 0e e0 51`** |
| MD5 over `[0, indexSize)` equals it | **`b74187bd5c88f564281dc290ab0ee051`** — **identical** |

```
file size            31,196,932,183 bytes
index size           11,995,716
MD5(file[0 .. 11995716))   b74187bd5c88f564281dc290ab0ee051
file[-16:]                 b74187bd5c88f564281dc290ab0ee051      MATCH
```

> **And two negative controls pin the range**, so §3's *"the buffer that gets hashed **includes the
> magic and the size dword**"* is proved rather than inferred:
>
> | range | MD5 |
> |---|---|
> | from offset **8**, `n − 8` bytes | `6a33366c09af867f0356d5f18ed8ca0a` |
> | from offset 0, `n − 16` bytes | `d9960efaea5114a099740b980566ae26` |
> | **from offset 0, `n` bytes** | **`b74187bd5c88f564281dc290ab0ee051`** |
>
> Skip the eight-byte header and the digest is wrong; stop sixteen bytes short and it is wrong. The
> engine hashes the index **including its own header**, and the shipped archive was built that way.

This is a different evidence class from the rest of the page — the shipped artifact rather than the
disassembly — and the two agree.

### ⚠ §3's "in full" stops one step early, and the missing step is §7's second unknown

The pseudocode ends at `CryptReleaseContext`. What follows is the comparison:

```asm
001F44FF  mov rax, [rbp - 0x20]    ; computed, low half
001F4503  mov rcx, [rbp - 0x10]    ; stored,   low half
001F4507  cmp rax, rcx
001F450A  jl  0x1F4705             ; -> fail
001F4510  jg  0x1F4705             ; -> fail
001F4516  mov rdx, [rbp - 0x18]    ; computed, high half
001F451A  mov r8,  [rbp - 8]       ; stored,   high half
001F451E  cmp rdx, r8
001F4521  jl  0x1F4705
001F4527  cmp rcx, rax
001F452A  jl  0x1F4705
001F4530  jg  0x1F453B
001F4532  cmp r8, rdx
001F4535  jl  0x1F4705
001F453B  ...                      ; accepted: the index is parsed from here
```

and the failure exit is three instructions long:

```asm
001F4705  xor al, al               ; return false
001F4707  ... epilogue ... ret
```

**So the digest is compared — both 64-bit halves — and a mismatch returns `false` in silence.** There
is no message: `BigFile head wrong!` occurs on the magic branch only. The return is not dropped:
`0019B0EA movzx esi, al` / `test al, al` / `jne 0x19B117`, and on the failing path the caller frees
the archive's `+0x20` through `001F4120` before returning the flag onward.

§7's second unknown is closed by that, and §4's *"the failure is at open, not at use"* gains its
missing half: the failure **is** produced at open, as a boolean, and the immediate caller acts on it.

### Everything else reproduces, exactly

| §5 / §8 claim | measured |
|---|---|
| `ReadFile` **3** sites, all `Resource` | **3**, all `Resource` |
| `SetFilePointer` 2 · `CreateFileA` 2 | **2 · 2** |
| `fread` **17** — `Resource` 9, others 8 | **17** — `Resource` **9**, others **8** |
| `fopen` 12 · `_wfopen` 1 · `_wfopen_s` 8 | **12 · 1 · 8** |
| no memory-mapped path | **no import contains `CreateFileMapping` or `MapViewOfFile`** — 538 slots parsed |
| `0059F4A0` is a 92-byte leaf with 12 callers; `0059A9B0` 1; `0059D4B0` 0 | **92 B / 12**, **1**, **0** |
| `0x4B595253` is the only occurrence of those bytes in `.text` | **exactly one** |
| `fclose` at `001F4471`, `CryptAcquireContextW` at `001F4496` | both, and the IAT slots resolve to `api-ms-win-crt-stdio-l1-1-0.dll!fclose` and `ADVAPI32.dll!CryptAcquireContextW` |
| `001F4340` is 991 bytes with one caller | **991 B**, **1** caller (`0019B070`) |

One point of precision: the twelve callers of `0059F4A0` are **`Resource` 8, `Audio` 1 and three
untagged**. *"12 callers across `Resource` and `Audio`"* is true of nine of them; a quarter of the
population has no owner tag at all, which is worth saying on a page whose §8 leans on owner counts.

### The index is entirely lower-cased (measured 2026-09-13)

Every name string in the archive index is lower case: **0 of 89,414 entries contains a single
uppercase character.** So **no question about name *case* can be asked of this index** — a search
for a capitalised file name returns 0 whatever the truth is.

Case survives only inside file **contents**: the `.ta` animation lists and `shared/phyremaps.txt`
both carry `/GameData/D3D11/…` with capitals intact, and `.rdata` path literals keep theirs. **A
census that keys on a capitalised name must go to those, never to the index.**

Recorded here because this is the page a name census starts from. Found while checking whether the
uppercase letter in
[`highmodelreplace.bin`](../../17-Presentation-Rendering/Model-And-Motion-Formats/add-motion-skeleton-and-high-model-tables.md)
is a naming convention: **the search that answered "no" could not have answered "yes"**, so the
question stays open rather than closed.

**Not claimed.** ~~The per-entry record layout — §7's first unknown is untouched.~~ *(Corrected 2026-09-30
(SWE2-CONTRACT, DD batch 9): now read, §3a.)* Whether a `false`
return from `0019B070` ultimately refuses to start the game: the flag was followed one level, not to
a message or an exit. ~~Which of the two `CreateFileA` sites opens what.~~ *(answered: see the §7 box - minidump files, 2026-09-27; 2026-10-02, OPUS)* The residual gap §8 already
states — a pointer copied out of an IAT slot into a register or structure is invisible to this census
— still stands, and this pass did not close it. **The archive was read, never written**, and nothing
was executed.

## The `001F4340` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

The 991-B opener `001F4340` additionally shows the CRT call path:
`00210EC0(0x104)` buffer → `[rbx+0x78]` (`001F4372`/`001F437C`),
`strcpy` of the source byte run (`001F4393`), path arg `008F9AC4`
through the IAT (`001F43A5`), the `008C2EF0`/`008C2E38` import pair
(`001F43D1`/`001F4424`), the `SRYK` magic compare `0x4B595253` at
`001F43D7`, and the `009038C8` "BigFile …" error string into
`0017D280` (`001F43E7`).

| member | role | interior |
| --- | --- | --- |
| `001F3FD0` (144 B) | intrusive red-black insert — `byte[rdx+0x10]` colour (`001F3FD0`), `[rdx]`/`[rdx+8]` link stores (`001F3FEC`/`001F3FEF`), parent walk `[rdx+0x18]` (`001F3FFD`) | [`001F3FEF`](../../_index/ADDRESS-INDEX.md) |
| `001F4720` (176 B) | index-record accessor — `rbx = [rcx+0x30]`, `edx = dword[rcx+0x4C]` (`001F4745`/`001F474E`) | [`001F4745`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `00210EC0`, `0017D280`, the CRT
imports `008C2EF8`/`008C2EF0`/`008C2E38`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (2026-09-17, SWE2-FRONTIER)

Both labels fan in through `0017D280`, the 85-B variadic diagnostic logger this page names among
the load's shared callees (49 call sites corpus-wide — `derived-call-signatures.md`):

- **Script_VM_Native_Bridge — CLIENT (24 edges).** `0050C670`, `0050C8D0`, `0050C990`, `0050CA10`
  and twenty more verb bodies, owned by that layer, call `0017D280` — they log through the same
  variadic diagnostic the bigfile load uses; fan-in to a shared logger, not a load ownership
  crossing.
- **WorldAreaField — CLIENT.** `00314020`, owned by that layer, calls `0017D280` — same shared
  logger consultation.
- **Audio — CLIENT (1 edge).** 1 inbound (Audio bodies `00225BA0` call page-cited `0059F4A0`). Substantive edges include `0059F4A0` is called by `00225BA0`.
- **Platform — SERVICE (1 edge).** 1 outbound (page-cited `0019AA20` call Platform bodies `0019A510`).
