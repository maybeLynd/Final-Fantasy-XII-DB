---
system: sead.win.config — the sound engine's chunked start-up configuration
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
    verified: 73 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "1 / 1 .config in the archive index (ps2data/sound/sead.win.config, 1,264 B), 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "config"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-sead-win-config-pass-1
  crossref_clean: true
  reopened_count: 0
---

# `sead.win.config` — the sound engine's start-up configuration

> One 1,264-byte file the audio layer reads whole at start-up and hands to the `[sead]` engine's
> initialiser: an `scnf` header, a directory of ten tagged chunks, and in them the four sound
> categories (`dummy0`, `music`, `se`, `voice`), the one `Master` bus, and the output settings.

**Corpus validation.** The archive holds exactly one `.config`: `ps2data/sound/sead.win.config`,
1,264 bytes; every figure below is read from it. Census:
[`census.py`](../../_experiments/evidence/sead-config-chunks/census.py) →
[`census.out.txt`](../../_experiments/evidence/sead-config-chunks/census.out.txt).

---

## 1. What the player sees

**The mixer the game starts with.** The sound engine groups what it plays into the categories this
file names — music, sound effects, voice — and sums them through its single `Master` bus. ~~Which game
setting drives which category is not traced here.~~ *(Superseded by §7 and `SD-22`: the Music / Sound Effect / Voice settings drive categories 1 / 2 / 3 through commands 0x13 / 0x14 / 0x15. Struck 2026-10-01, OPUS.)* Nothing in the file is per area or per scene.

## 2. The layout

```struct ScnfHeader base=file size=0x10
+0x00  char[4]  magic       'scnf' - not compared by the accessors, but by 007AE410 (§6b)
+0x04  u16      field04     0
+0x06  u16      dirOffset   0x10 - read by every chunk accessor
+0x08  u8       chunkCount  10 - read by every chunk accessor
+0x09  byte[3]  _pad        0
+0x0C  u32      fileSize    1,264 = the file size
```

```struct ScnfDirEntry base=record size=0x10
+0x00  char[4]  tag         compared with the accessor's tag constant
+0x04  u16      field04     0 in 10 of 10
+0x06  u16      field06     0x10 in 10 of 10
+0x08  u32      offset      chunk position from the file start
+0x0C  u32      field0C     0 in 10 of 10
```

Most chunks are **tables**: `+0x02 u16` is the offset of a `u32` table of element offsets (from the
chunk start) and `+0x04 u32` is the element count. Named elements start with `u8 version, u8 index,
u16 headerSize` and carry their name at `+headerSize`.

| # | tag | at | elements | contents |
|---:|---|---:|---:|---|
| 0 | `ctgr` | `0x0B0` | 4 | categories `dummy0`, `music`, `se`, `voice` (32 B each; `+0x04 u16` = 0, 4, 48, 8; `+0x06 u16` = 6, 5, 2, 5) |
| 1 | `bus ` | `0x150` | 1 | bus `Master` (48 B; `f32 1.0` at `+0x0C`, name at `+0x20`) |
| 2 | `mcr ` | `0x1A0` | 3 | unnamed 32 / 48 / 48 B records |
| 3 | `epsp` | `0x240` | 0 | empty |
| 4 | `eps ` | `0x250` | 11 | unnamed 16–144 B records |
| 5 | `curv` | `0x430` | 1 | one 48 B record (`f32 1.0` twice) |
| 6 | `expr` | `0x480` | 0 | empty |
| 7 | `hcam` | `0x490` | — | **not a table**: `+0x01 u8` 16, `+0x04 u32` 44,100, `+0x08 u8` 0 |
| 8 | `evt ` | `0x4A0` | 0 | empty |
| 9 | `ctgl` | `0x4B0` | 1 | `default` (32 B) |

## 3. The loader contract

**Reading the file — `00210760`.** Formats `"%s%s"` from `PS2Data/sound/sead` (`009068E0`, through
`01E027C8`) and `.win.config` (`00906A38`), opens and reads the whole file into a fresh buffer
(`001D6F20`, `001D6EE0`, `001D6FA0`), fills an initialisation block whose data pointer is that buffer,
and calls **`007A4D50`** (`00210889`) — the `[sead]` initialiser — then `007A5B50`, and **frees the buffer**
(`002108F1`). A missing file makes `00210760` return 1 before any initialisation (`002107CB`–`002107D0`).
Reached from `001DBA40`.

**Finding a chunk.** One accessor per tag scans the directory — `count = [cfg+8]`, entries at
`cfg + [cfg+6]`, 16 bytes each — for its tag constant from the table at `01CB4928`, and returns
`cfg + entry.offset` or null:

| tag | accessor | callers |
|---|---|---|
| `ctgr` | `007ADB20` | `007A4D50` (`007A50A7`), `007B0F90` |
| `ctgl` | `007ADBB0` | `007A4D50` (`007A50CA`) |
| `bus ` | `007AD9A0` | `007AC4F0`, `007ACD30` |
| `mcr ` | `007AE1D0` | `007B31A0` (interior verified 2026-09-17, SWE2-FRONTIER — calls its own accessor `007AE1D0` at [`007B3254`](../../_index/ADDRESS-INDEX.md), then the `007B2BD0` ×20 / `007B2880` ×15 driver-pool helpers; the 50 `02EADD70`-cluster references the static-init page counts are this body's) |
| `evt ` | `007ADF90` | `007A4D50` (`007A4FF7`) |
| `epsp` | `007ADE80` | `007ACD30` (interior verified 2026-09-17, SWE2-FRONTIER — 1,289 B; carries `"[sead][info]set effect preset [%s][fade:%f]"` and `"set effect preset number invalid [%d]"`, `007CA560`/`001243B0` ×4 + `007A5570`/`007A46E0` ×2, first call at [`007ACD8E`](../../_index/ADDRESS-INDEX.md)) |
| `eps ` | `007ADD30` | `007AD240` |
| `curv` | `007ADCA0` | nine sites in `007BDFA0`–`007F0320` |
| `expr` | `007AE080` | `007B0F90` |
| `hcam` | `007AE110` | `007A4D50` (`007A4F51`) |

`007ADF60(chunk, index)` returns element `index` as `chunk + table[index]` with the table at
`chunk + [chunk+2]`.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | **`007AE410`** (the parse's own validator, §6b) | **magic mismatch → parse returns −1, `007A4D50` bails** | — | **no — corrected 2026-09-27: inert only among the accessors; the loader rejects on it** |
| `+0x06` dirOffset, `+0x08` chunkCount | every accessor (e.g. `007ADB2A`, `007ADB2F`) | — | — | — |
| `+0x0C` fileSize | ~~no reader found among the accessors~~ **`007B0FE8` and `007B0FFE`** | — | — | **no — corrected 2026-09-13 (§6): it is the allocation size AND the copy length** |
| directory tag | the accessors (`007ADB5A` …) | **tag not found → null chunk** | — | — |
| directory `+0x08` offset | the accessors (`007ADB86` …) | — | — | — |
| `hcam +0x01`, `+0x04`, `+0x08` | `007A4F63`–`007A4F71`, into the device description passed to `007AC4F0` | missing chunk → `+0x08` flag taken as 0 | — | — |

**The write path.** None.

**`007AC4F0` interior read (2026-09-17, SWE2-FRONTIER).** The `hcam`-configured device creator is the
**sound-device factory**: it takes the driver global `02EAD3E0` (`007AC51B`), queries the `bus ` table via
`007AD9A0` (`007AC54E`), then constructs the device object graph — six distinct RTTI-anchored vtables
(`01CB44A0`/`01CB4700`/`01CB45F8`/`01CB45E8`/`01CB4690`/`01CB46D8`, first install's `lea` at
[`007AC5B0`](../../_index/ADDRESS-INDEX.md)) — each member registered through `007AD460` (×4), with the
device primitives `007AD550`, `007AEF30`, `007AE930`, `007AD950`, `007ADA30`, `007D2150`, `007DAFF0`
filling out the graph before it is handed back for `hcam` configuration.

**`007D2150` interior read (2026-09-17, SWE2-FRONTIER).** The `007AC4F0` callee is the
**`SurroundReverb` effect constructor**: RTTI names both vtables it installs (`01CB7528`/`01CB7578`
→ `SQEX::Sd::Driver::SurroundReverb`, two base subobjects) plus a `DynamicValue<2>` member
(`01CB7068`); it seeds the `02EADF00`–`02EADF30` vector globals with `movaps` pairs
(first at [`007D29EF`](../../_index/ADDRESS-INDEX.md)), runs six `007AD550` member-inits and three
`007AD460` registrations, then hands the object to the `007D0F60`/`007AECE0` attach chain.

**`007DAFF0` interior read (2026-09-17, SWE2-FRONTIER).** The `BuildReverb` sibling constructor:
installs `01CB7998`/`01CB79E0` (RTTI → `SQEX::Sd::Driver::BuildReverb`, two subobjects) plus the same
`DynamicValue<2>` member vtable `01CB7068`, then runs the identical helper shape as `007D2150` —
`007AD460` registrations ×6, `007AD550` member inits, `007A9E50` mode-normalise ×2 with
`expf`/`powf` (`00861FAA`/`00861F6E`) coefficient seeds, `007AED00` driver-global reads ×6
(first at [`007DB28D`](../../_index/ADDRESS-INDEX.md)). The family shape is now clear: each effect
type has a constructor (`007D2150` surround / `007DAFF0` build) plus a param-commit vtable slot
(`007D76E0` / `007DB8D0`) sharing the `007A9E50`+`007AED00` helper pair.

**`007AEF30` interior read (2026-09-17, SWE2-FRONTIER).** The **rendering-channel block initializer** —
the global the whole reverb family reads through `007AED00`: it sets `dword [02EAD34C] = 8`
(the channel count the `"enable SIMD, need rendering channel 8"` assert at `007AEF7B` demands, reported
via `0019C5D0`), then fills the channel-pointer array `02EAD358`/`02EAD360` from `007AD550`/`007DDED0`
returns, and stores the driver globals `02EAD348`/`02EAD350`/`02EAD354` (the `mov [02EAD34C],8` at
[`007AF06A`](../../_index/ADDRESS-INDEX.md)). `007AED00` is exactly `mov eax,[02EAD348]; ret` — the
driver-global getter these commits share.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00210760` | reads the file and calls the engine initialiser | ✅ full body |
| `007A4D50` | `[sead]` initialiser; reads `hcam`, `evt `, `ctgr`, `ctgl` | ◐ the chunk reads |
| `007ADB20`, `007ADBB0`, `007AD9A0`, `007AE1D0`, `007ADF90`, `007ADE80`, `007ADD30`, `007ADCA0`, `007AE080`, `007AE110` | per-tag chunk accessors | ✅ full bodies (identical shape) |
| `007ADF60` | element by index | ✅ full body |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01CB4928` | chunk tag table | `.rdata` | `scnf ctgr ctgl bus  mcr  evt  epsp eps  curv expr hcam` |
| `009068E0` | `"PS2Data/sound/sead"` | `.rdata` | path stem |
| `00906A38` | `".win.config"` | `.rdata` | path suffix |

## 5. Corpus survey

One file; §2 is its complete walk. Three chunks (`epsp`, `expr`, `evt `) are present but empty.

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one address at a time and read in full.)*

### Every figure reproduces, re-walked from the archive

The file was re-extracted from `FFXII_TZA.vbf` and walked with independent code rather than by
re-reading `census.out.txt`. The archive holds **exactly one** `.config`, `ps2data/sound/sead.win.config`,
**1,264 bytes**. Header: magic **`scnf`**, `+0x04` **0**, `dirOffset` **`0x10`**, `chunkCount` **10**,
pad **`00 00 00`**, `fileSize` **1,264** = the file length. **All ten directory entries** carry
`+0x04` **0** and `+0x06` **`0x10`** and `+0x0C` **0**, and every tag, offset and element count in
§2's table is exact:

`ctgr` `0x0B0`/4 · `bus ` `0x150`/1 · `mcr ` `0x1A0`/3 · `epsp` `0x240`/0 · `eps ` `0x250`/11 ·
`curv` `0x430`/1 · `expr` `0x480`/0 · `hcam` `0x490` · `evt ` `0x4A0`/0 · `ctgl` `0x4B0`/1.

So are the element readings: the four categories are **`dummy0`, `music`, `se`, `voice`** at 32 B
each with `+0x04` = **0, 4, 48, 8** and `+0x06` = **6, 5, 2, 5**; the one bus is **`Master`** with
**`1.0f` at `+0x0C`** and its name at **`+0x20`**; `hcam` reads **16**, **44,100**, **0**; `ctgl`
holds **`default`**; and `curv`'s single record carries **two `1.0f`**.

### ✔ `WC-1`'s lifetime half, answered: the engine copies the whole file

§7 asked whether anything is copied before `00210760` frees the buffer at `002108F1`. **It is.**

```asm
007B0FE2  mov  rax, [rbp - 0x48]     ; the config buffer
007B0FE8  mov  ecx, [rax + 0x0C]     ; <- the header's fileSize
007B0FEB  call 0x7AD550              ; [sead]'s allocator
007B0FF7  mov  [rip + ...], rax      ; -> 02EAD3E0, published
007B0FFE  mov  r8d, [rcx + 0x0C]     ; <- fileSize again, as the length
007B1002  mov  rcx, rax
007B1005  call 0x861EBA              ; memcpy
```

`007AD550` is the engine's allocator, and it identifies itself: it takes `size`, allocates
`size + 0x10`, writes **`0x5EAD5EAD`** at `+0x00`, the tag at `+0x04` and the size at `+0x08`, and
returns the pointer **past** that 16-byte header.

**`02EAD3E0` has exactly one writer and sixteen readers in fifteen functions** — the writer is
`007B0FF7` above; the readers include all nine `curv` sites, each of which wraps the pointer with
`007A46E0` (`mov [rcx], rdx ; mov rax, rcx ; ret`, a one-field handle) before handing it to the
accessor. **So the nine late reads are of the copy, and no pointer into the freed buffer survives.**

### ⚠ `+0x0C` is not unread — it is the most load-bearing field in the file

§3's field table records *"`+0x0C` fileSize — no reader found among the accessors"*. The qualifier is
true and the row still misleads: it is read **twice**, at `007B0FE8` as the **allocation size** and at
`007B0FFE` as the **`memcpy` length**. **Editing `+0x0C` without changing the file's length truncates
or over-reads the engine's only copy of the configuration** — which is the one thing a modder needs
to know about this header, and the table said nothing was reading it.

**Not claimed (superseded 2026-09-27 by §6c/§6d — those paragraphs now read all of it).** `WC-1`'s
first half was then untouched — what the `ctgr`, `bus `, `mcr `, `eps `, `curv`
and `ctgl` element fields *mean*, and what `hcam`'s 16 / 44,100 / flag configure, were still unread.
§3's ten accessors were not each re-read; only `007ADCA0` (`curv`) was decoded in full, and it matches
§3's description of the shape (`count = [cfg+8]`, entries at `cfg + [cfg+6]`, 16 bytes, tag from
`01CB4928`). Whether `007B0F90` runs before the free was taken from the call chain, **not** traced
instruction by instruction from `00210889`. The archive was **read, never written**, and nothing was
executed.

### ✔ §6b — the `scnf` magic is validated after all; `eps ` and `expr` payload content — 2026-09-27 (SWE2-DATA)

§2's *"magic — not compared by the accessors"* is true only of the ten finders. The parse's own
gate is `007AE410` — `test rcx,rcx; mov eax,[rcx]; cmp eax,[01CB4928] ("scnf"); sete al` — and
`007B0F90` calls it on `[ctx+0x38]` **before** the copy: `007B0FB4 test al,al / jne` proceeds,
else `or eax,-1` and `007B0F90` returns −1, which `007A4D50` tests (`007A4E7E js → -1`). **A bad
magic aborts the whole `[sead]` initialisation, not just the parse.** The `scnf` dword at
`01CB4928` sits at the head of the tag table — the validator reads the table's row 0 where the
finders read rows 1–10.

Two chunks' record payloads, read from the shipped file (distributional — no consumer bound):

- **`eps `** item 1 is a 0x90-byte float block whose values are reverb-shaped —
  `{1.0, 20.0, 1.0, 1.0, 500.0, 1.0, 1.0, 40.0, 1.414, 7, 200.0, 800.0, 2000.0, 8000.0}` —
  and item 10 carries `{1.0×4, 0.2, 0.08, 2.0, 2000.0}`, delay/chorus-shaped. The 11 records
  are unnamed (no name field in this chunk), so the effect→preset binding must come from a
  consumer read, not the data.
- **`expr`'s eager table** (`007B0F90` → `007AE080`/`007AE020`): each item lands in the
  `02EAD3F8` 0x40-stride table only when `item[0] == 1`; a `byte[+4] == 1` item then
  contributes two floats from `+0x10`/`+0x14` into `+0x34`/`+0x3C` of its row. Shipped
  `expr` is count 0, so the machinery is proven and the population is empty.

`mcr ` items 1/2 carry opcode streams (`04 12 08`, `04 A1 04`, `03 01/02 01`, `04 01 00`)
with a `0.1f` (`CD CC CC 3D`) tail each — §6c decodes the vocabulary.

### ✔ §6c — `mcr ` is a bytecode bank: stream grammar, opcode dispatch and the worklist model — 2026-09-27 (SWE2-DATA)

§6b named `007B3254` the executor; that is the interior call to the `mcr` chunk finder
`007AE1D0`. The executor is **`007B31A0`** (4,561 B), reached from `007BD120`, `007BD4E0` and
`007BED30` — virtual methods of a six-vtable object family.

**Record and stream grammar.** `007B31A0` bounds-checks the macro index against
`word[chunk+4]` (element count) and resolves the element through `007AE1A0`, the standard
accessor (`chunk + u16[+2]` = `u32` offset table, `chunk + table[i]` = record). A record is a
16-byte header with **`u16 streamOffset` at `+0x02`** (0x10 in all three shipped records) whose
other bytes are unread by the executor; the stream at `record + streamOffset` is a run of
instructions `{u8 flag +0, u8 headerLength +1, u8 opcode +2, u8 payloadLength +3, payload +4}`
with stride `headerLength + payloadLength` (headerLength is 4 in all shipped instructions).
Opcodes are 1..0xAB; dispatch is a `byte[(op-1)]` → case-index map at `0x7B43D0` feeding a
dword-offset table at `0x7B4374` (both `.text`). **23 opcodes are live**; every unmapped value
falls into the epilogue `0x7B42CB`, which advances the accumulator and loops while the run flag
(`op 0x01` clears it) is set.

**Invocation.** The caller supplies `(ctx, mode)`; the macro index is read from the context's
descriptor `[ctx+0x30]`: mode 0 → `desc+0x0A`, mode 1 → `desc+0x0B`, mode 3 → `desc+0x4F`
(modes 1/3 require `desc+0` ≥ `0xD`/`0xE`; index 0 = no macro). `007BD120` runs mode 0 while
`ctx+0x54` ∈ {1,2} and maps return status **4** to `ctx+0x54 = 7`; `007BD4E0` runs mode 3 on a
teardown path; `007BED30` runs mode 1 when `ctx+0x54` ∉ {0,6,7} — **corrected 2026-09-27:**
`007BED30` is `Sound::Stop` (vtable slot 2), so the three slots are start-step / **stop** /
teardown, not init / tick / release.

**The worklist model.** The executor resets the list object at `02EAD570` (`007B6AA0`: 0x28-stride
node array at `+0x10`, capacity `+0x08`, **active count `+0x0C` = `02EAD57C`**, free chain `+0x18`,
active head/tail `+0x20`/`+0x28` — the head is what handlers read as `02EAD590`), takes the
`02EAD4C8` critical section, and snapshots eligible objects from the source pool `02EAD560`
(node `+0x20` = object, kept when `object != ctx`, `object->vft[+0xA8]()` returns 2 and
`object->vft[+0x130]()` is false) via `007AF380`. Filters then unlink non-matching nodes with
`007B2880` (index-keyed unlink, `dec [head+0xC]`), so **every subsequent gate sees the count of
surviving nodes**.

**Gate.** All predicates funnel through `007B2BD0(op, lhs, rhs)` = `{0 ==, 1 !=, 2 >, 3 >=,
4 <, 5 <=}`; the float variant `007B2C40` serves ops 0x16/0x17. In the action opcodes the gate is
`[e+4]` vs `[e+5]` on `02EAD57C` — *"the filtered set holds at least/at most N nodes"*.

**Opcode vocabulary** (offsets from instruction start; `+4`/`+5`/`+6`/`+8`/`+0xC` are payload):

| op | handler | kind | semantics |
|---:|---|---|---|
| `0x01` | `007B33DF` | control | END — clears the run flag |
| `0x10` | `007B33E9` | control | resets the worklist and re-snapshots `02EAD560` |
| `0x11` | `007B3471` | filter | two descriptor-field gates per node |
| `0x12` | `007B3555` | filter | pair-key compare (`007BD5E0`: `(boundRecord+0xA u16)<<16 \| desc+8 u16`); `[e+5]` mode: 0 = absolute vs `[e+8]`, 1 = `ctxKey − nodeKey` vs `[e+8]` |
| `0x13` | `007B36BA` | filter | descriptor byte `+7` (`[e+5]` 0 = each node's, 1 = ctx's) vs `[e+8]` |
| `0x14` | `007B37A5` | filter | each node's **own macro index in the same slot** the executor is running (`desc+0xA`/`+0xB`/`+0x4F` by mode) vs `[e+8]` |
| `0x15` | `007B38FE` | filter | field of the `007BD8D0`-wrapped node object vs `[e+8]` |
| `0x16`/`0x17` | `007B3A3C`/`007B3B24` | filter | float predicates via `007B2C40` |
| `0x18` | `007B3C19` | filter | node test via `007B4800` |
| `0xA0` | `007B3D1D` | action | apply `f32 [e+8]` to survivors' resolved targets via `007A84A0` (enqueues a `{type 0xA/0xB, object, value}` action record); scope `[e+6]`: 0 = all, 1 = first, 2 = min, 3 = max by `vft[+0xD0]` float accessor |
| `0xA1` | `007B3F2F` | action | set executor status **4** |
| `0xA2` | `007B3F59` | action | resolve `02EAD008[[e+6]]` — the **Category table** — and call `007AA510` (`f32 [e+8]`, `f32 [e+0xC]` on the object at `+0x38`, the volume-ramp layer) |
| `0xA3`/`0xA4` | `007B3F9E`/`007B3FFB` | action | `007BE4D0` — reset the sub-object at `ctx+0x148` |
| `0xA5` | `007B402E` | action | store `count-arith × f32[e+8] + (instr flag ? f32[e+0xC] : 0)` into `ctx+0x51C` |
| `0xA6` | `007B409D` | action | same computed float → `ctx->vft[+0x88]` |
| `0xA7`/`0xA8`/`0xA9` | `007B4102`/`007B4147`/`007B4187` | action | resolve `02EAD008[[e+6]]` then `007AA4F0` / `007AA680` / `007AA3E0` (member ops on the resolved object's sub-components; `0xA7` targets the `+0x40`+`0x30` layer — the pitch side per §7's Category layout) |
| `0xAA` | `007B41C7` | action | apply via `007A8590` — second `{type, object, value}` action record flavour |
| `0xAB` | `007B424D` | action | apply via `007A7A20` — third action record flavour |

**What the shipped streams say.** With the grammar resolved the three records read:

- macro 0: `END` — an empty program.
- macro 1: `0x12` keep nodes whose key equals ctx's key → `0xA1` gate `count ≥ 1` → **status 4**
  (the caller maps it to `ctx+0x54 = 7`) → `END`.
- macro 2: `0x12` same-key filter → `0xA0` gate `count ≥ 2`, scope 1 (first node), apply
  **`0.1f`** → `END`.

Both are *same-key collision policies*: macro 1 marks its own object complete when a keyed peer
survives the filter; macro 2 attenuates a survivor by 0.1 when two keyed objects coexist. The
`+0x8` float semantics live in `007A84A0`'s action records, not in the stream itself.

**Provenance gaps.** The descriptor `[ctx+0x30]` — `+0` minimum-size byte, `+6` object-table
index (`007AAA20` → `02EAD008`), `+7` filter byte, `+8` key lo-word, `+0xA`/`+0xB`/`+0x4F` macro
indices, `+0x19` bit-7 gate — is **not authored in this file** (`evt ` and `epsp` are empty);
it is assembled from the per-bank sound data and its layout is not yet decoded. Likewise
`02EAD560`'s pool is populated by object creation outside the config path. `[e+4]`/`[e+5]` gate
bytes in filter opcodes other than `0x12` are partially assigned above from disassembly only.

### ✔ §6d — the remaining chunks' consumers, the descriptor's provenance, and the pool's population — 2026-09-27 (SWE2-DATA)

**Tag table.** The finder constants live at `01CB4940`–`01CB4978` (LE ASCII dwords, zero-padded):
`bus ` `mcr ` `evt ` `epsp` `eps ` `curv` `expr` `hcam`. `01CB4980` onward is ordinary data
(`-4.8f`, then a small struct table) — not tags. Finder → consumer map (all callers from
`edges.tsv`, each verified in body):

| chunk | finder | consumers |
|---|---|---|
| `bus ` | `007AD9A0` | `007AC4F0` (mixer init), `007ACD30` (preset applier) |
| `ctgr` | `007ADB20` | `007AAA40` (Category table), `007B0F90` (capacity sum → `02EAD3E8`) |
| `curv` | `007ADCA0` | `007BDFA0`, `007BE0B0`, `007BEAF0`, `007BED30` (Sound::Stop), `007BEF30`, `007C8890`, `007CA650`, `007CA9F0`, `007F0320` — all Sound-family methods |
| `eps ` | `007ADD30` | `007AD240` (preset applier, sole caller `007ACD30`) |
| `epsp` | `007ADE80` | `007ACD30` |
| `evt ` | `007ADF90` | `007A4D50` (init only; empty in shipped file) |
| `expr` | `007AE080` | `007B0F90` (eager table `02EAD3F8`/`02EAD3EC`, §6b; empty in shipped file) |
| `hcam` | `007AE110` | `007A4D50` (init only) |
| `mcr ` | `007AE1D0` | `007B31A0` (the executor, §6c) |

**`hcam` = mixer seed parameters.** `007A4D50` reads three fields of the single record and packs
them into the param block it hands to `007AC4F0(02EAD0A8, params)`: `u8 +0x01` → params `+8`
(shipped **16**), `u32 +0x04` → params `+4` (shipped **44,100** — the output sample rate), and
`u8 +0x08` → flag `+0xC` (shipped 0; when the chunk is absent the flag is forced 0 and the other
fields keep the caller's defaults `0x100`, `rbx+0x40`, `byte rbx+0x50`).

**`bus ` = the mixer topology.** `007AC4F0` sizes the mixer from `word[chunk+4]` (+1 when the
chunk kind byte is 0), allocates `count × 8` pointer table at `mixer+8`, and constructs one
**0x128-byte Bus object** per slot: `{vft 01CB4700, +0x08 link, +0x10/+0x18/+0x20/+0x28 = four
insert-FX slots, +0x30 = name, +0x38..+0x128 = five 0x30-stride ramp slots (vft 01CB44A0 — the
same ramp type the Category layers use)}`. The element record is
`{u8 kind@0, u8 busIdx@1, u16 nameOfs@2, s8 sendTarget0@4, u8 insertCnt@5, u8 sendTargets[4]@6,
u8 sendCnt@0xA, u8 @0xB, f32 sendLevel0@0xC, u32 sendLevels[]@0x10, name}`; sends wire bus→bus
(`+4`/`+0xC` is send 0; `sendCnt` additional `{target u8 @+6+i, level u32 @+0x10+i*4}` pairs).
Insert sub-records (count `+5`, iterator `007ADA30`) carry `u8 type@+1` ∈ 0..0xA dispatched
through the jump table at `0x68CCF0` to nine effect ctors — sizes 0x18, 0x60, 0x80, 0x170 (two
ctors), 0x178, 0x610, 0x1230, 0x10140, 0x708A0 — plus a null case; each built object attaches to
a bus `+0x10`..`+0x28` slot. **Shipped: one element `Master` (bus 0), send target −1, no sends,
no inserts** — the whole mixer is a single root bus and every effect ctor is dormant data.

**`eps ` = per-class effect parameter banks.** The chunk carries a `u32` table at
`chunk + u16[+2]` indexed **directly by class id** — `007ADDC0(epsChunk, classId, presetIdx,
&flag)` reads `u32[tbl + classId*4]` to a class section `{u16 @0, u16 dataOfs@2, u8 presetCnt@4,
u8 flag@5}`, bounds-checks `presetIdx < byte[sec+4]`, exports `byte[sec+5]` as the flag, and
returns `sec + u16[sec+2] + presetIdx × stride[classId]`. The 11-entry stride table is built
from `01CB49A0`/`01CB4990` plus three literals: **`{0, 0x80, 0x20, 0x10, 0x10, 0x10, 0, 0x10, 0,
0x10, 0x20}`** for classIds 0–10 — corrected 2026-09-27 (the earlier read mistook `0x80` for a
`0x80000000` sentinel). `classId` is the insert object's own `vft[+0x08]()` getter and the
returned block is applied through **`insert->vft[+0x30] (presetBlock, flag, fadeSeconds)`** —
each effect class interprets its own stride (`007AD240`). The classId ↔ effect ↔ stride map,
from the `bus ` insert arms (`0x68CCF0` jump table in `007AC4F0`) joined to `01CB49A0`:

| id | ctor | class | stride |
|---|---|---|---|
| 0 | — | placeholder object (`01CB4690`/`01CB46D8`) | 0 |
| 1 | `007D2150` | SurroundReverb | 0x80 (32 f32 — the §6b reverb-shaped block) |
| 2 | `007D85E0` | Compressor | 0x20 (8 f32) |
| 3 | `007D0AC0` | Filter | 0x10 (4 f32) |
| 4 | `007D80E0` | SideChainInput | 0x10 (4 f32) |
| 5 | `007D9530` | SimpleFilter | 0x10 (4 f32) |
| 6 | `007D99E0` | Flanger | 0 |
| 7 | `007DA0A0` | GranularPitchShift | 0x10 (4 f32) |
| 8 | `007DAAB0` | HilbertFilter | 0 |
| 9 | — | nop arm | 0x10 |
| 10 | `007DAFF0` | BuildReverb | 0x20 (8 f32 — the delay-shaped block) |

Shipped: 11 sections (ids 0–10). What each float *names* lives in the classes' `.rdata`
param-descriptor tables (`01CB7xxx` — `{metaPtr, …}` entry blocks, e.g. SurroundReverb's
`+0x30` entry `008F5F50`), dormant machinery since no insert is ever constructed; the
per-field names are the one residual this pass leaves. *Resolved 2026-09-27 (WC-1
verification, SWE2-DATA): the `008F5F50`-family blocks carry no name strings — `008F5F50`
is MSVC x64 exception metadata (magic `0x19930522`), and an image-wide sweep finds no
audio-parameter names at all. The field* roles *are instead recovered from each class's
applier/commit/process code — every slot of every non-zero stride is dispositioned in
`../../_index/candidates/wc1-eps-preset-fields/fields.tsv`; see the §7 WC-1 answer.*

**`epsp` = callable bus-automation presets — both streams now read.** `007ACD30(mixer, idx, rate)`
bounds-checks `word[chunk+4]`; each element is `{u8 ver@0, u8 nameLen@1, u16 tblOfs@2,
u16 cntB@4, u16 cntA@6, …}` with a versioned name (ver≥3: inline at `el+0x10`, `nameLen` long;
the `set effect preset [%s][fade:%f]` log formats it) and **two** sub-record streams under the
table at `el + u16[+2]`:

- **stream A** (`007ADE50`, `cntA` records via a `u32` offset table): `{u8@0, u8@1, u8 busIdx@2,
  s8 rampSlot@3 (must be < [mixer+0x10] and ≤4), f32 value@4}` — drives `007CA560` on
  `bus + 0x38 + rampSlot*0x30`, the five bus ramp slots.
- **stream B** (`007ADF10`, `cntB` fixed **16-byte** records at `tbl + ((nameLen+0x10) & 0xF0)`
  when ver≥3, else `tbl` directly): `{u8@0, u8@1, u8 busIdx@2, u8 fxSlot@3 (<4), u8 op@4}` —
  resolves `insert = [busTbl[busIdx] + 0x10 + fxSlot*8]`; `op == 0xFE` skips, `op == 0xFF` sets
  `insert+0x10 = 1` (the enable flag `007AC4F0`'s ctor path also sets), any other `op` clears
  the flag and calls **`007AD240(insert, op, rate)`** — `op` is the `eps ` preset index, so a
  stream-B record says "on bus N's insert slot M, load preset K."

**Empty in the shipped file** — but wired live, not dead code: `007ACD30`'s only caller is
the action dispatcher `007AB5C0`, arm **type `0x30`** (`{type, u32 epspIdx@8, f32 fade@0xC}` →
`007ACD30(mixer 02EAD0A8, idx, fade)`), so anything that can enqueue a type-`0x30` action
drives it; with `word[epsp+4] == 0` every call bounds-fails immediately.

**`curv` = the authored-curve bank — bound but never sampled.** `007ADC40` is the standard
accessor; the element is `SQEX::Sd::ConfigFile::Curve` (COL `01D40CB8`), a 48-B record
`{u16 @0, u16 ptsOfs@2 = 0x10, u16 nPts@4 = 2, …}` carrying two 16-B point records at
`el+0x10`: `{u32 0x00001000, f32 0.0, f32 0.0, u32 0}` and `{u32 0x00100000, f32 1.0, f32 1.0,
u32 0}` — plausibly `{time-fixed, value-from, value-to, pad}` but the packing is *formally
unfixed because nothing reads it*. All nine consumers are Sound-family methods that only
**store** the element pointer at ramp-slot `+0x38` and call the ramp setter — an image-wide
scan finds no function that dereferences a `+0x38`-bound element into its `+0x02`/`+0x04`/
`+0x10` payload. **What actually evaluates fades is `007A9E50`**, a fixed six-kind easing
table keyed on `slot+0x1C` (the `r9d`/`edi` arg `007CA560` stores there): arms compute
`t` (id 0, linear), `1−(1−t²)³`, `1−(1−t)²`, `t²`, `powf(C,t)−1` and `C−powf(C,1−t)` (ids 1-5; `C = [01CEBC08]`, via
`00861F6E`); ~~default `0`~~ an id above 5 returns 0 *(corrected 2026-10-01, OPUS: arm 0 at `007A9F17` returns `t`; the out-of-range exit is `007A9F14`)*. The tick is `007CD000`: `t = slot+0x10 / slot+0x14` → `007A9E50` →
`current = start + eased·(target−start)` on the `ctx+0x840` slot, then a completion callback
through `vft[+0x10]` once the eased output reaches `1.0`. So `curv` is **dead-authored on the
shipped title**: bound for provenance, never evaluated — the same disposition as `ctgr +0x06`.
The ramp slot itself (`007CA560`): `{+8 current, +0xC target, +0x10 elapsed, +0x14 duration,
+0x1C ease-kind, +0x20 active, +0x24 mode, +0x28/+0x2C slew limits (mode==1, abs-masked via
`00D27AA0`), +0x38 curve elem}`; `007CA750` is an idempotent setter over `this+0xF0` at 0x30
stride that skips re-arming an already-matching target. `007BDFA0` is the start-side binder
(gates `ctx+0x54 == 1`); `007BED30` (`Sound::Stop`) binds a curve for the stop fade. The
sound-context ramp slot is 0x40-sized (curve ptr at `+0x38`); bus/category ramps are 0x30 —
same leading shape, no curve field.

**`[ctx+0x30]` provenance — it is the `.sab` `SabFile::Sound` record.** The fields the executor
path consumes are the bank record's own bytes: `+0x00` u8 = **record version** (the mode gates
are version checks — modes 1/3 read `+0x0B`/`+0x4F`, which exist only at format ≥ 0xD/0xE; every
shipped record is version 16), `+0x04` u8 class selector, `+0x05` u8 candidate count (per the
sndclass census), `+0x06` u8 category index into `02EAD008`, `+0x07` u8 flags, `+0x08` u16 key
lo-word, `+0x0A`/`+0x0B`/`+0x4F` the three macro slots.

**Corpus census — all 4,609 `.sab` banks, 13,150 records** (NATIVE-STATIC; script
`Database/Tools/work/SWE2-DATA/snd_macro_census.py`): `+0x06` ∈ {1:1986, 2:8506, 3:2658} — every
record binds a real category (`dummy0` is never referenced); `+0x07` ∈ {0x80:12487, 0xFF:663};
`+0x08` is a small sequential id (0…≈bank size); **`+0x0A` is nonzero in exactly six records**,
all in `ps2data/sound/se/sead_data_win/se000/se000.win.sab` at record indices {1,2,3,5,7,90} —
five bind macro 2 at category 2 (`se`), and record 7 (the only category-1 record in the set)
binds macro 1; **`+0x0B` and `+0x4F` are zero in all 13,150 records** — nothing ships a stop- or
teardown-mode macro, so modes 1/3 always fall through to record 0 (`END`) on shipped data. The
`mcr` bank exists for exactly those six `se000` sounds, exercised only at start-step.

**`02EAD560` population — it is a descriptor head, not a bare list.** `02EAD540` is a 0x30-byte
list descriptor `{cap +0x08, count +0x0C (=02EAD54C), freeChain +0x18 (=558), head +0x20
(=02EAD560), tail +0x28 (=568)}`; `02EAD570` is the same descriptor type for the macro worklist
(head `02EAD590`, count `02EAD57C` — matching §6c) and `02EAD490` a third (head `02EAD4B0`, the
handle/arena list `007B1AB0`/`007B1E10` manage). This is why no direct writers to `02EAD560`
exist: inserts go through **`007AF380(desc, &outIdx, obj)`** — pops a node off `desc+0x18`,
link-prepends `{+8 prev, +0x10 next, +0x1C flags|=1, +0x20 payload}`, `count++`, returns
`node+0x18`. The registrar is **`007B2CB0`**: pops a 0x28 node from the `02EAD4F0` pool
(`007DF750`), pushes it onto `02EAD540`, and stamps the caller's handle `{u8 2, u16 nodeIdx,
u32 serial (02EAD4C4++)}` — the handle `007BD8D0`/`007B2470` later resolve through the
`02EAD410`/`02EAD404` block table that `007B2700` builds at init. Callers: `007D0940` (one-shot
register gated on `obj+0x1C == 0`) ← `007A87C0` ← `00221C70`, `007A4A10`, `007F0820`, and the
virtual `007E9E60`. `007B4840` drains all lists at teardown; everything runs under critsec
`02EAD4C8`. So `02EAD560` is the **live sound-object registry** — populated when sound objects
register, walked by the macro executor and by the broadcast helpers `007B48F0`/`007B4960`/
`007B4A00`/`007B4A70`.

**`ctgr +0x06`, `bus +0x0B`, `ctgl +0x04` — dead-authored, three of a kind.** `007ADAB0` is the
sole `ctgr` element accessor and both of its call sites (`007AAB07`, `007AABC7`) are inside
`007AAA40`; `007AAA40` itself reads `+0`/`+2` (name) and `+4` (capacity/alias), and the alias
fixup `007AA320` reads `+4` only. Nothing reads `ctgr +0x06` — the shipped {6, 5, 2, 5}
is authoring residue. The `bus ` element is read only by `007AC4F0` (`+0` ver, `+1` table idx,
`+2` nameOfs, `+4` send target, `+5` insert count, `+6`..`+9` send indices, `+0xA` send count,
`+0xC`/`+0x10` send floats) and `007ACD30` (`+1`, `+4`, `+5`, `+0xA` for validation) — `+0x0B`
(shipped value 6, the pad between send-count and the level floats) has no reader. And `ctgl`'s
one finder caller is `007A4D50`, which routes the element wrapper to `007AAA40` → `007AA110`;
`007AA110` reads only `+0`/`+2` (layer name, `cat+0x70`) and sizes layers from the element
*count*, so element `+0x04` = 7 has no reader either — the earlier "off-path readers" caveat is
closed: there is no other path.

## 7. What this document does not claim

- [x] **WC-1.** What the fields of the `ctgr`, `bus `, `mcr `, `eps `, `curv` and `ctgl` elements mean, and what
      `hcam`'s `16`, `44,100` and flag byte configure in the device `007AC4F0` creates. `WC-1`.
      *Narrowed 2026-09-14 (FABLE), not answered: the `ctgr` element's `+0x04` and the `ctgl` count are read.*
      *Narrowed again 2026-09-27 (SWE2-DATA, §6d): `hcam` fully read (mixer seed: `+1`=16, `+4`=44,100
      rate, `+8` flag); `bus `/`eps `/`epsp`/`curv` element grammars and consumers read; `ctgr`
      `+0x06`, `bus ` `+0x0B`, `ctgl` `+0x04` and **`curv` itself** all shown dead-authored
      (`curv` is bound into ramp `+0x38` by nine binders but never sampled — fades evaluate
      through the fixed six-kind `007A9E50` easing table on `slot+0x1C`, tick `007CD000`);
      `epsp` stream B is decoded (`{busIdx, fxSlot, op}` — op = `eps ` preset index);
      `mcr` grammar in §6c. Remaining: the per-field names inside each `eps ` class's
      preset block (dormant `01CB7xxx` param-descriptor tables — no insert is ever built).*
      ***ANSWERED 2026-09-27, FABLE, Claude Opus 5.5, static: the `eps ` preset fields are read from the code, not from names.** The per-field names are not in the image (no audio-parameter strings anywhere; board note 34619 to SWE2-DATA on `008F5F50`). Each class's applier (`vft+0x30`) sends every float through `setParam` (`vft+0x10`) into a ramped value, and the commit and process functions give it a role. Of the 68 slots across the eight non-zero strides *(count corrected 2026-09-27, SWE2-DATA — the strides sum to 0x110 B = 68 f32; `fields.tsv` carries one row per slot)*, 52 carry a role row — three of those flagged never-consumed/undetermined — and the rest are 5 ignored band-type ints, 7 padding slots no applier reads, and class 9's 4 (no class). SurroundReverb: wet, dry, late input gain, room size (`x/30` scales the delay lines, `007D7CFB`), RT60 ms, damping, diffusion, early and late levels, pre-delay, pattern, five EQ bands. Compressor: threshold dB, 1/ratio, input and make-up gain dB, attack ms, release ms, side-chain bus and slot. Filter: biquad type, cutoff Hz, 1/Q, gain. SideChainInput: capture gain. SimpleFilter: one-pole mode, cutoff. GranularPitchShift: pitch ratio, grain rate. BuildReverb: master, dry, wet, early, late, pre-delay s, RT60 s, damping Hz (flag byte = version gate). With section 6d above, every chunk's fields and `hcam` are now accounted for. Limits: Filter type 6's and SimpleFilter mode 2's filter shapes are not classified, four roles are medium confidence, and the whole bank is dormant in the shipped game. [Record and controls](../../_index/candidates/wc1-eps-preset-fields/README.md).*
      - **`007AAA40` builds the Category table.** The chunk's count (`+0x04`, 4) becomes `02EAD000`, and an array of
        that many pointers becomes `02EAD008`. Each element comes through `007ADAB0`, and its **`+0x04` `s16`** decides
        what happens:
        - **0:** no Category (the pointer stays null). That is `dummy0`.
        - **positive:** a `0x88`-byte Category is built (`007A96F0`) and initialised by `007AA110`.
        - **negative:** a second pass calls `007AA320` (*"Category::InitializeRefCategory"*), which makes the Category a
          reference to category `−value` (its `+0x58`).
      - **The positive value is the Category's sound-list capacity.** `007AA110` passes it to `007AA010`, which
        allocates that many `0x28`-byte nodes at Category `+0x10`/`+0x18`. `007AA770` walks those nodes when it pushes
        volume and pitch to attached sounds (`007AA958`–`007AA96A`). So **`music` holds 4 sounds, `se` 48 and
        `voice` 8.**
      - **`ctgl`'s element count sizes the volume layers.** `007AA110` gets `[ctgl]+0x04` (1 here; 1 if the chunk is
        absent) and makes `count + 1` volume ramps at Category `+0x38` (count `+0x78`). The pitch array at `+0x40` is
        always 2 ramps (`+0x7C`). All start at `1.0` with duration 0.
      - **Cross-check.** The element order `dummy0`, `music`, `se`, `voice` makes the category numbers 1 / 2 / 3 the
        game's volume commands `0x13` / `0x14` / `0x15` use, and the debug menu's labels independently name them
        Music / Sound Effect / Voice ([driver architecture](../sqex-sd-sound-driver-architecture.md) §7, `G-3`).
      - **`mcr` decoded 2026-09-27 (SWE2-DATA, §6c):** records are 16-byte headers + bytecode
        streams; `007B31A0` is the executor (start/stop/teardown slots on the sound-object
        descriptor); the opcode table resolves to 9 filters + 12 actions + 2 control; the
        shipped programs are same-key collision policies (peer-exists → status 4; two peers →
        apply 0.1f).
      - **Dormant-detail residue (after §6d + WC-1, 2026-09-27 verification, SWE2-DATA):** every prior
        item here is dispositioned — the `eps ` preset-record fields are answered by WC-1 above,
        `bus ` `+0x0B` (= 6) and `ctgl` element `+0x04` (= 7) are dead-authored, and `epsp`'s
        stream-B record tail beyond the `{busIdx, fxSlot, op}` triple is undecoded but unreachable
        (shipped `epsp` is empty). Genuinely open residue is confidence-level only: Filter type 6's
        and SimpleFilter mode 2's filter shapes are unclassified, four WC-1 roles are medium
        confidence, and the authored parameter *names* are unrecoverable (not in the image).
        Resolved there: `hcam` (mixer seed: rate 44,100, `+1` = 16), `curv` (dead-authored — bound into
        ramp `+0x38` but never sampled; fades evaluate through the fixed six-kind `007A9E50`
        easing table on `slot+0x1C`),
        `bus ` (one `Master` root, dormant effect ctors), `eps `/`epsp` roles, `ctgr` `+0x06`
        (dead-authored), the `[ctx+0x30]` descriptor (the `.sab` Sound record — six `se000`
        records bind macros, all mode-0), and `02EAD560` (head of list desc `02EAD540`, populated
        by registrar `007B2CB0`).
- [x] ~~Whether the engine copies what it needs before `00210760` frees the buffer — `curv` is read
      from nine later sites, which requires either a copy or a retained pointer. `WC-1`.~~
      **ANSWERED 2026-09-13 (OPUS, §6): it copies the whole file.** `007B0F90` reads the header's
      **`+0x0C` fileSize**, allocates that many bytes through `[sead]`'s own allocator
      (`007AD550`), publishes the block at **`02EAD3E0`**, and `memcpy`s the file into it — all
      before `00210760` frees the read buffer. The nine `curv` sites read **the copy**. No
      pointer into the freed buffer is retained.

## 8. The `00210760` exclusive subtree — SEAD's container machinery under the start-up

The exclusive-callee census assigns 40 frontier functions to `00210760` — SEAD internals the
start-up pulls in, none reached from outside this tree. All signature-swept 2026-09-15
(`bshape.py`); the layering is unusually clean:

| layer | members | role |
|---|---|---|
| record primitives | `0021D990`, `0021DA00`, `0021DA50`, `0021DAD0`, `0021DB50`, `0021DBE0`, `0021DC60`, `0021DD40`, `0021DDD0`, `0021DE80`, `0021DEE0`, `0021DF70`, `0021E020` (13) | call-free 70–251 B bodies keyed on the `009087A8`–`00908808` `.rdata` templates — per-record field ops |
| `001EDF00` apply arms | `0021E090`, `0021E190`, `0021E280`, `0021E370`, `0021E470` (5) | 234–251 B each, `001EDF00` ×5 over `008C5F58`/`008F3CB0` — five-field apply steps |
| combiner | `0021E570` (448 B) | runs all five apply arms plus `005CC8A0`/`005CD0A0` ×4 and `00220E80`/`00220F20`/`00220760` — the "apply everything" assembly |
| iterating processors | `0021F440`, `0021F790`, `0021FB20`, `0021FEF0` (4 — interior verified 2026-09-17, SWE2-FRONTIER: `0021DC60` ×4 confirmed, first at [`0022003A`](../../_index/ADDRESS-INDEX.md), `00225920` ×2 + `00808C40`), plus the 780 B `0021F130` | each calls one `0021Dxxx` primitive ×4 inside a `00225xxx` stepped loop, ending with `[r9+0x10]`/`[r9+0x18]` indirect calls — container iteration with a callback pair |
| element wrappers | `00220DE0`, `00220E80`, `00220F20`, `00220FC0`, `00221060` (5), `002207E0`, `00220860`, `00220960`, `00220A00`, `00220AE0` (5) | 146 B `00221xxx` + `00199DB0` shape, or `[rax]`-indirect thunks — per-element entry/alloc |
| dispatch layer | `00221310`, `00221390`, `00221450`, `00221510`, `002215D0`, `002216B0` (6) | each pairs a `00225xxx` step with a `0021Fxxx` processor and a `0022xxxx`/`0020xxxx` tail — the calls the start-up itself makes |

The shape says this is SEAD's list/queue machinery (`FixedList`/`FixedQueue` of the RTTI
inventory) plus the start-up's own registration loop — the `00225xxx` helpers are the
container's step/insert ops, `00199DB0` the element alloc, and the `009087xx` templates the
record layouts. Which SEAD container each `0021Fxxx` processor drives is not established.

## 9. Related

- [The audio bank and controller family](../Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) — the `AudioFileLoadManager` side that loads this file.
- [`.seb` — the SE block index](seb-se-block-index.md) and [`.sab`](sab-sound-bank-container.md) — the banks that play through these categories.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. The image-address resolver fan-out is MECHANICAL.*

- **Resource and Presentation — MECHANICAL.** The loose-file helpers `001D6EE0`, `001D6F20` (open) and `001D6FA0`
  (read) that the `.win.config` loader `00210760` uses are generic. They are also called by six to eight Resource
  bodies and by `AddMotion_LoadHighModelReplace`, `AddMotion_LoadResources` and `AddMotion_LoadSkeletonMapping`
  ([FF12CONFIG](../../19-Save-Load-Settings/Game-Settings-Config/ff12config-and-debglobal.md) crossings).
  - `001D6F20` calls two small Resource helpers, and `00210760` calls four (12–122 B).
  - The sead registration shape `00199DB0` / `005CC8A0` / `005CD0A0` is shared with Resource bodies (27–878 B), a
    703-byte and a 346-byte Presentation body, and a 1,101-byte **Platform** body.
  - `00220760` is called by a 254-byte Resource body.
- **Platform — SERVICE.** The `EASTL map` body `0021E570` calls a 63-byte Platform helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Application — CLIENT.** `FUN_0017d6b0`, owned by that layer, calls `001DBA40` on this page. That caller is a 45-byte startup sequencer: six calls in fixed order and a tail-jump into a final one, with no work of its own; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-18 update (2026-05-15) — `001D6FA0`/`001D6EE0` init-block copier fragments

`001D6FA0` (12 B) and `001D6EE0` (12 B) are the null-gate forwards inside the `0x800`-byte initialisation-block path this page describes (`ff12config` names the `0x800` copy and the close via `001D6E80`). Each is the same three-instruction shape — `test rcx,rcx`, forward on non-null, `xor eax,eax` + `ret` on null: `001D6FA0` forwards to `0059F4A0` (`001D6FA3`), `001D6EE0` forwards to `001FDF70` (`001D6EE3`). `001D6FA0` has 10 measured callers — the heaviest hub of this batch — spanning config, audio-init and the `0037xxxx` subsystems; `001D6EE0` sits in the same `001D6xxx` helper cluster this page groups as the SEAD/Win config openers.

## SWE2-EC7-34 update (2026-09-19) - `0021F440`

`0021F440` (842 B) is the first SEAD win-config sibling - `0021DD40`/`0021D990` then the `002254D0`/`0021F76C`/`0021F6B8`/`0021E020` chain. Interior anchor `0021F52D` (an `0021DD40` call).

## SWE2-EC7-34 update (2026-09-19) - `0021F790`

`0021F790` (908 B) is the second sibling - same frame, `0021DDD0`/`0021DA50` then `00225610`/`0021FAFE`/`0021FA49`/`0021DEE0`. Interior anchor `0021F892` (an `0021DDD0` call).

## SWE2-EC7-34 update (2026-09-19) - `0021FB20`

`0021FB20` (965 B) is the third sibling - `0x6666666666666667` divide magic over the `[rcx+8]`..`[rcx+0x10]` range, `0021DE80`/`0021DA00`/`002258D0`/`0021FED1`/`0021FD5C`. Interior anchor `0021FBE3` (an `0021DE80` call).

## SWE2-EC7-35 update (2026-09-19) - `0021F130`

`0021F130` (780 B) is the fourth config sibling - call-free container insert, `0x6666666666666667` divide-by-ten index magic over the `[rcx+0x10]` range, `movsd`/`movzx word+8` element reads. Interior anchor `0021F189` (the `movsd` element load).

## SWE2-EC7-45 update (2026-09-19) - `0021E090`

`0021E090` (251 B) is a body - `001EDF00`/`00220DE0`. Interior anchor `0021E0C5` (an `001EDF00` call).

## SWE2-EC7-45 update (2026-09-19) - `0021E370`

`0021E370` (251 B) is a body - `001EDF00`/`00220FC0`. Interior anchor `0021E3A5` (an `001EDF00` call).

## SWE2-EC7-45 update (2026-09-19) - `0021E470`

`0021E470` (251 B) is a body - `001EDF00`/`00221060`. Interior anchor `0021E4A5` (an `001EDF00` call).

## SWE2-EC7-45 update (2026-09-19) - `00220860`

`00220860` (251 B) is a vtable row body - a `call [rax]` vcall, no direct calls. Interior anchor `00220908` (the vcall).

## SWE2-EC7-46 update (2026-09-19) - `0021E190`

`0021E190` (234 B) is a body - `001EDF00` single call. Interior anchor `0021E1C1` (the `001EDF00` call).

## SWE2-EC7-46 update (2026-09-19) - `0021E280`

`0021E280` (234 B) is a body - `001EDF00` single call. Interior anchor `0021E2B1` (the `001EDF00` call).

## SWE2-EC7-46 update (2026-09-19) - `002215D0`

`002215D0` (223 B) is a body - `0021FEF0`/`00220AE0`/`00225880`/`00225920`/`00808C40`. Interior anchor `00221637` (a `0021FEF0` call).

## SWE2-EC7-47 update (2026-09-19) - `0021DC60`

`0021DC60` (222 B) is a call-free record ctor - installs vtable `009087E0`, `movups` four `0x80`-lane copies from `r10+0x10`, `+0x210` tail, `0x218` stride walk. Interior anchor `0021DCB0` (the copy loop head).

## SWE2-EC7-47 update (2026-09-19) - `00220A00`

`00220A00` (219 B) is a body - `call [rax]` vcalls only. Interior anchor `00220A88` (the first vcall).

## SWE2-EC7-50 update (2026-09-19) - `00221390`

`00221390` (185 B) is a body - `0021F440`/`00220860`/`00225490`/`002254D0`. Interior anchor `002213E2` (a `0021F440` call).

## SWE2-EC7-50 update (2026-09-19) - `00221450`

`00221450` (185 B) is a body - `0021F790`/`00220960`/`002255C0`/`00225610`. Interior anchor `002214A2` (a `0021F790` call).

## SWE2-EC7-50 update (2026-09-19) - `00221510`

`00221510` (182 B) is a body - `0021FB20`/`00220A00`/`00225830`/`002258D0`. Interior anchor `00221562` (a `0021FB20` call).

## SWE2-EC7-58 update (2026-09-19) - `0021DF70`

`0021DF70` (169 B) is a call-free `0x80`-stride record copier - 4-iteration `movups` pairs (`edx`=4), `009087E0`. Interior anchor `0021DFB7` (the first `movups` store).


## SWE2-EC7-58 update (2026-09-19) - `0021DDD0`

`0021DDD0` (167 B) is a call-free `0x10`-stride record copier stamping `009087C0` (RTTI `01CF0EB0`) per element - vector move-construct. Interior anchor `0021DE11` (the `009087C0` vtable stamp).

## SWE2-EC7-60 update (2026-09-19) - `00220AE0`

`00220AE0` (157 B) is a sead element wrapper - `0021DBE0` single call plus one vcall. Interior anchor `00220B0D` (a `0021DBE0` call).


## SWE2-EC7-60 update (2026-09-19) - `00220960`

`00220960` (155 B) is a sead element wrapper - `0021DAD0` single call plus one vcall. Interior anchor `0022098D` (a `0021DAD0` call).

## SWE2-EC7-62 update (2026-09-19) - `00221060`

`00221060` (149 B) is a sead element wrapper - `00199DB0`/`002215D0`. Interior anchor `0022107B` (a `002215D0` call).



## SWE2-EC7-65 update (2026-09-19) - `0021DD40`

`0021DD40` (137 B) is a call-free move-construct - `009087A8` vtable stamp into `[r8]`, `[rax-8]` header copy (`0021DDD0` sibling). Interior anchor `0021DD80` (the `009087A8` vtable stamp).



## SWE2-EC7-66 update (2026-09-19) - `0021DB50`

`0021DB50` (131 B) is a call-free `0x218`-stride record move - `r10-0x420` header, `[r8+8]` links, `edx=0x100` bound. Interior anchor `0021DB70` (the `r10-0x420` header load).



## SWE2-EC7-66 update (2026-09-19) - `0021DEE0`

`0021DEE0` (131 B) is a call-free move-construct - `[r9+8]`/`cmove` header copy into `[rcx-8]`, `009087C0` stamp (`0021DD40` sibling). Interior anchor `0021DF17` (the `[rcx-8]` header store).


## SWE2-EC7-108 update (2026-09-20) - `00225610` + `002254D0` measured

`00225610` (19 B) and `002254D0`
(19 B) are the vtable-seed ctor
tails `0021F790`/`00221450` /
`0089A1F0` and `0021F440` /
`00221390` / `0089A1E0` run: stamp
`00907860` or `00908790` onto
`[rcx]`, then tail `001243B0` on
`rcx + 8` for the member init -
the two-entrypoint construction
pair the sead config objects
share.
Interior anchors `0022561E` and
`002254DE` (the `jmp 001243B0`
tails).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-sead-win-config-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0021D990` | 100 B | copies `0x30`-byte records backward from the range `rcx` to `rdx` into the area ending at `r8`, moving each record's qword `+8` (read through a null guard), dword `+0x10`, byte `+0x14`, dword `+0x18` and qwords `+0x20` and `+0x28` but not its first qword, and returns the destination start; when `rdx` equals `rcx` it returns `r8` unchanged | `0021D996`, `0021D9A0`, `0021D9B2`, `0021D9E7`, `0021D9EB` |
| `0021DA00` | 70 B | copies `0x28`-byte records backward from the range `rcx` to `rdx` into the area ending at `r8`, moving each record's qword `+8`, dword `+0x10`, qword `+0x18` and byte `+0x20` but not its first qword, and returns the destination start; when `rdx` equals `rcx` it returns `r8` unchanged | `0021DA03`, `0021DA10`, `0021DA15`, `0021DA35`, `0021DA3D` |
| `0021DA50` | 118 B | copies `0x30`-byte records backward from the range `rcx` to `rdx` into the area ending at `r8`, moving each record's qword `+8` (read through a null guard) and the eight dwords `+0x10` to `+0x2C` but not its first qword, and returns the destination start; when `rdx` equals `rcx` it returns `r8` unchanged | `0021DA53`, `0021DA60`, `0021DA73`, `0021DAB9`, `0021DABD` |
| `0021DAD0` | 123 B | copies `0x30`-byte records forward from the range `rcx` to `rdx` to `r8`, moving each record's qword `+8` (read through a null guard) and the eight dwords `+0x10` to `+0x2C` but not its first qword, and returns the destination end (`r8` itself when `rcx` equals `rdx`) | `0021DAD3`, `0021DAEF`, `0021DB36`, `0021DB3E`, `0021DB42` |
| `0021DBE0` | 127 B | copies `0x218`-byte records forward from the range `rcx` to `rdx` to `r8`, moving each record's qword `+8`, the `0x200` bytes from `+0x10` two bytes per step over 256 steps, and qword `+0x210` but not its first qword, and returns the destination end (`r8` itself when `rcx` equals `rdx`) | `0021DC00`, `0021DC07`, `0021DC20`, `0021DC44`, `0021DC4B` |
| `0021DE80` | 84 B | copies `0x28`-byte records forward from the range `rcx` to `rdx` to `r8`, writing for each non-null destination record the template pointer `00908808` to its first qword and the source's qword `+8`, dword `+0x10`, qword `+0x18` and byte `+0x20`, and returns the destination end (`r8` itself when `rcx` equals `rdx`) | `0021DE8F`, `0021DE99`, `0021DE9B`, `0021DEBA`, `0021DEC3` |
| `0021E020` | 98 B | fills `edx` consecutive `0x30`-byte records from `rcx` (none when `edx` is zero) as copies of the record at `r8`: for each non-null slot it writes qword `+8` from the source (read through a null guard), the template pointer `009087A8` to the first qword, and the source's dword `+0x10`, byte `+0x14`, dword `+0x18` and qwords `+0x20` and `+0x28` | `0021E025`, `0021E02E`, `0021E050`, `0021E074`, `0021E07C` |
| `002207E0` | 113 B | moves the 10-byte elements (a qword then a word) from `r8` up to the end qword `[rcx + 8]` down to `rdx`, then adds the signed `(rdx - r8) / 10 * 10` to qword `[rcx + 8]` and returns `rdx` | `00220800`, `00220815`, `0022082C`, `00220844`, `00220848` |
| `00221310` | 113 B | counts the 10-byte elements between qwords `[rcx]` and `[rcx + 8]` (signed divide by 10); when `edx` is above that count (unsigned) it calls `0021F130(rcx, [rcx + 8], edx - count, &zeroed 10-byte stack element)`, otherwise it tail-jumps `002207E0(rcx, [rcx] + edx * 10, [rcx + 8])` | `00221317`, `0022133F`, `00221344`, `0022135F`, `0022137C` |
| `00225490` | 61 B | calls `007A5F10(rcx + 8)`, then stores the template pointer `009087A8` to qword `[rcx]`, -1 to dword `+0x10`, 0 to dword `+0x18`, byte `+0x14` and qwords `+0x20` and `+0x28`, and returns `rcx` | `0022549D`, `002254A2`, `002254A9`, `002254B0`, `002254C0` |
| `002255C0` | 74 B | calls `007A5F10(rcx + 8)`, then stores the template pointer `009087C0` to qword `[rcx]`, 0 to dwords `+0x10` and `+0x28`, -1 to qword `+0x14`, `0x7F` to dword `+0x1C`, `0x40` to dword `+0x20` and -1 to dword `+0x24`, and returns `rcx` | `002255CD`, `002255D9`, `002255E7`, `002255EF`, `002255F6` |
| `00225830` | 67 B | stores the template pointer `00908808` to qword `[rcx]` and 0 to qword `+8`, dword `+0x10` and byte `+0x20`, then stores to qword `+0x18` the result of an 11-byte wrapper that tail-jumps `malloc` with size `0x10000`, and returns `rcx` | `00225846`, `0022584D`, `0022585C`, `00225861`, `00225866` |
| `00225880` | 68 B | stores the template pointer `009087E0` to qword `[rcx]` and 0 to qwords `+8` and `+0x210`, then stores to qword `+8` the result of an 11-byte wrapper that tail-jumps `malloc` with size `0x100000`, and returns `rcx` | `00225896`, `0022589D`, `002258A6`, `002258B2`, `002258B7` |
