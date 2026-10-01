---
system: .ker and .fex — the PC fonts' kerning pairs and expansion character lists, requested by the font .dat flags
category: 16-UI
status: AUDITED
owner_layer: PrimaryOwner:UI
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 18 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "34 / 34 .ker and 14 / 14 .fex, with the 63 font .dat and 5 fontlist.ah that decide which are requested, 2026-09-13"
last_reviewed: 2026-09-13
archive_formats:
  - "ker"
  - "fex"
  - "fontdat | explained | the 63 gamedata/d3d11/artdata/font/*.dat font tables (.dat member; 17 numeric leading dwords): 0x28-byte header (+0x04 glyph count, flags word) + 0x24-byte glyph records, 0x28 + 0x24*n on 62 of 63 - completion 001B4D70, font build 001FC060"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-font-ker-fex-pass-1 - every published figure reproduces including all 34 .ker pair counts and the five language arms; NEW: no .dat flag ever asks for a file that is not there (0 of 63 either way) while 9 .ker and 1 .fex sit unrequested, the two unrequested .fex are unrequested for two different reasons, and the triple layout is 001FDB50's own argument list (9,032/483 and 11,481/217 with per-key indices 0,1,2,...); CORRECTED: the walk dies on the SECOND record and the two files' blocking numbers differ, and the flags distribution is over 62 not 63
  crossref_clean: true
  reopened_count: 0
---

# `.ker` and `.fex` — font kerning and expansion lists

> The PC build's fonts live in `gamedata/d3d11/artdata/font/<lang>/`. A language's `fontlist.ah` names
> the fonts; each font's `.dat` carries a flags word whose bit 0 asks for `<font>.ker` — a flat list of
> kerning pairs — and bit 1 for `<font>.fex` — lists of character codes under 32-bit keys. **Every file a
> list and its flags request parses exactly; the ones that do not parse are exactly the ones nothing
> requests.**

**Corpus validation.**

| | |
|---|---|
| files | **34 `.ker`, 14 `.fex`**, 63 font `.dat`, 5 `fontlist.ah` (`ch`, `cn`, `jp`, `kr`, `us`) |
| `.dat` requested by a list | **62 of 63** (not `us/fontex_expand.dat`); all 62 are `0x28 + 0x24 × glyphCount` bytes |
| `.dat` flags | **of the 62 a list names**: 0 in 26, 1 in 24, 2 in 11, 3 in 1. Over all 63, 2 is in **12** — `us/fontex_expand` is the twelfth (§6) |
| `.ker` requested | **25 of 34**, all a whole number of 12-byte records (so are the other 9) |
| `.fex` requested | **12 of 14**, all walk exactly to the end by the parser's rules, no repeated key |
| not requested | 9 `.ker` (`font00` in `ch` `cn` `jp` `us`, `fontex_expand` in `ch` `cn` `kr`, `font_iwa_g12` in `jp` `us`); 2 `.fex` (`us/fontex_expand`, `us/fontex_subtitle`) |
| the 2 unrequested `.fex` | **do not parse** by the shipped rules — the *first* record is fine (count 0) and the walk dies on the **second**, whose count field holds the file's own first key: `0x2294A029` in `us/fontex_expand`, **`0x22949AE0`** in `us/fontex_subtitle` (§6). Read as 12-byte `{key, index, value}` triples they are whole — **9,032 triples / 483 keys** and **11,481 / 217** — with every key's indices running 0, 1, 2, … |

Census: [`census.py`](../../_experiments/evidence/font-kerning-and-expansion/census.py) →
[`census.out.txt`](../../_experiments/evidence/font-kerning-and-expansion/census.out.txt) (two runs byte-identical).

---

## 1. What the player sees

**The spacing between particular letter pairs, and — in the Japanese, Korean and Chinese builds — the
character sets of the subtitle, expansion and monster-name fonts.** The English font list requests
kerning for its subtitle, `venus`, `square` and six `stf` fonts, and no `.fex` at all; the CJK lists request
`.fex` for `fontex_expand`, `fontex_subtitle` and `fontmonster`. (The paired-kern path itself is
**structurally inert in the shipped build** — §3: the loader stores a flat `map<rightCp, adjust>` while the
only reader walks a nested `map<cur, map<prev, adj>>` that can never be populated; the authored pair data is
unreachable.) What a `.fex` key names is not established (§7).

## 2. The layout

```struct KerPair base=record size=0x0C
+0x00  u32       first        character code of the RIGHT glyph — the kerned glyph; the pair-map's outer key (0x41 'A', 0x20 ' ', ...)
+0x04  i32       second       character code of the LEFT (preceding) glyph; the intended inner key — loaded, then dead-dropped by the shipped store
+0x08  i32       adjust       spacing adjustment (-2, -1, 0 in the samples)
```

The pair direction reads out of the consumer, not the record alone: `001FDDD0(font, prevKernCp, curKernCp)` searches the
outer map by the **current** glyph's kern cp and the inner map by the **previous** glyph's — `kerMap[cur][prev]`. The
writer keys the outer map by `first`, so `first` is the glyph being advanced now (the right element) and `second` is
its predecessor. The corpus agrees: `us/font_venus` carries `{0x41 'A', 0x56 'V', -2}`-shaped records — `VA`, `WA`,
`YA`, `TA` and `T `, `V `, `W `, `Y ` are exactly the classic pairs.

A `.ker` is nothing but these records to the end of the file.

```struct FexRecordHeader base=record size=0x08
+0x00  u32       key          must not repeat within the font
+0x04  i32       count        u32 values follow; 0 is allowed
```

A `.fex` is a sequence of `{key, count, value[count]}` to the end of the file. The values in the requested
files are character codes (hiragana `0x3082`, `0x3046`, CJK ideographs, Hangul `0xC6D0` …).

The font `.dat` that requests them: a `0x28`-byte header — `+0x04` glyph count, `+0x18` a float (1.0 in 62
of 63, 2.4 in `us/fontex_expand`), **`+0x1C` flags** — then `glyphCount` records of `0x24` bytes. Its other
header words and the glyph record fields are passed to the font constructor `001FC060` and the glyph insert
`001FDCC0`; the corpus decode of both is in §"the `.dat` section and the unified key space" below.

## 3. The loader contract

**Choosing the list.** `001B44A0(fontSystem, language, …)` sets the list path `01DF6DE8` and directory
`01DF6DF0`: language `1`–`6` → `us`, `7` → `kr`, `8` → `ch`, `11` → `cn`, anything else (including `<= 0`)
→ `jp` (`001B44A9`–`001B4532`). `001B4930` reads the list with `"%s"` one name at a time, skipping CR/LF, and
formats `<dir><name>` for a request; the request whose completion is `001B4D70` is not traced link by link here.

**The `.dat` completion** `001B4D70` builds the font from the header and glyph records (`001B4DE1`–`001B4F52`),
then tests the header's flags word (`001B4E19`): **bit 0** → `001B5750` requests `<dir><name>.ker` with
completion `001B6080` → `001B5230`; **bit 1** → `001B5480` requests `<dir><name>.fex` with completion
`001B6030` → `001B4C00` (`001B5024`–`001B5061`).

**`.ker` (`001B5230`).** Finds the font by id; while the cursor is below the buffer end, reads `{first, second, adjust}` and calls `001FDC10(font, first, second, adjust)`, which
stores `adjust` at `node+0x24` in the font's `+0x70` map **keyed by the record's first dword** (signed compare
`001FDC45`/`001FDC61` of `edx` against `node+0x20`), **overwriting an existing pair** (`001FDC66`). The second
record dword is passed in `r8d` — saved to the stack at `001FDC15` and **never read back**: the shipped store is a
flat `map<u32 first, i32 adjust>` (verified at the allocator — `001FC9F0` requests `0x28`-byte nodes, links `0x20` +
`pair<u32,u32>` 8 B). Then frees the buffer.

**The read side expects a nested map the writer never builds.** The only kern reader is `001FDDD0` (sole caller
`001E9780` ← `0017F8E0` ← the text walker's kern arm at `002AC52F`): it lower-bounds the same `+0x70` map by the
**current** kern cp, then treats the found node's `+0x30`/`+0x40` as an **inner map's sentinel/root** and searches it
by the **previous** kern cp — the intended structure is `map<u32 rightCp, {u32 pad; map<u32 leftCp, i32>}>` with nodes
≥ `0x50` bytes. `001FDC10`/`001FC9F0` are the map's only writers (single-caller verified) and build `0x28`-byte flat
nodes — the inner-map object can never exist, and `second` never reaches the tree. So on an outer hit `001FDDD0`'s
inner walk reads past the node into adjacent heap; the authored two-codepoint pair adjustment is **structurally
unreachable** in the shipped build — the kern term cannot return what the `.ker` files authored.

**`.fex` (`001B4C00`).** Finds the font by id; while the cursor is below the end, reads `key` and `count`, calls
`001FDB90(font, key, count)` — which **refuses a key already present** (`001FDBE3`–`001FDBEF`) and otherwise
creates the entry and sizes it to `count` (`001FDF90`) — then stores `count` values with `001FDB50(font, key,
i, value)` (`001B4CD0`–`001B4CE9`).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `.dat` flags bit 0 / bit 1 | `001B5024` / `001B5045` | — | — | the other bits |
| `.ker` record | `001B52B0`–`001B52B9` | — | — | — |
| `.ker` length | `001B52C6` | — | **no check that 12 bytes remain**: a trailing partial record is read past the end | — |
| `.fex` `key` | `001B4CA0` | a repeated key: `001FDB90` returns false and the walk **stops** (`001B4CBA` → `001B4D03`), skipping the buffer free at `001B4D21` | — | — |
| `.fex` `count` | `001B4CA6` | — | **no check against the buffer end**: the inner loop reads `count` values whatever remains; `count <= 0` stores nothing | — |
| `.fex` `value[i]` | `001B4CD0` | — | — | — |

The failure strings (`"Font data Try to add Ex pack have !!"`, `"Font data Load over buffer end data!!!"`) go
to `0016D6A0`, which is `ret 0` in this build: **the checks log nothing.**

**The write path.** None.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `001B44A0` | language → font list and directory | ✅ full body |
| `001B4930` | list reader, one formatted path per name | ◐ the name loop |
| `001B4D70` | `.dat` completion: font build, flags, `.ker` / `.fex` requests | ◐ header, glyph loop and the two requests |
| `001B5750` / `001B5480` | `.ker` / `.fex` request | ✅ full bodies (to the queue call) |
| `001B6080` / `001B6030` | completions → `001B5230` / `001B4C00` | ✅ full bodies |
| `001B5230` | `.ker` reader | ✅ full body |
| `001B4C00` | `.fex` reader | ✅ full body |
| `001FDC10` | kerning pair store | ✅ full body |
| `001FDB90` / `001FDB50` | `.fex` entry create / value store | ✅ full bodies |
| `0016D6A0` | message stub (`ret 0`) — carries the name `_guard_check_icall`, which does not match its body | ✅ |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `01DF6DE8` / `01DF6DF0` | font list path / font directory | `.data` ptr | set by `001B44A0` |
| `01DF6E08` / `01DF6E10` / `01DF6E18` | extension slots | `.data` ptr | `.dat`, `.ker`, `.fex` (`008F81F4`, `008F81FC`, `008F8204`) |
| `008F8188`, `008F8620`, `008F8678`, `008F86D0`, `008F8728` | list paths | `.rdata` | `jp`, `us`, `ch`, `cn`, `kr` `fontlist.ah` |

### The `001B4D70` exclusive subtree — all 13 members bound (SWE2-FRONTIER, followup queue)

The exclusive-callee census assigns the `.dat` completion **13 frontier functions**. Roles below
are what the bodies do; interior cites are one instruction inside each declared extent
(`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| request issue | `001B5750` (399 B), `001B5480` (399 B) | the `.ker` / `.fex` requesters §3 describes — format `<dir><name>.<ext>` and queue the request with completion `001B6080` / `001B6030` | `001B5757` / `001B5487` |
| font lookup | `001B58E0` (631 B) | ordered-tree walk of the font system's font-id map (head `rcx+0x30`, key `node+0x20`) — the "find the font by id" step both list readers open with | `001B5903` |
| font build | `001FC060` (518 B) | the font constructor — consumes the `0x28` `.dat` header and the `0x24` glyph records | `001FC066` |
| glyph insert | `001FDCC0` (147 B), `001FC580` (190 B) | the glyph-record insert §2 names, and its one-hop delegate into `001FD010` | `001FDCC8` / `001FC58B` |
| map insert layer | `001FD010` (382 B), `001FCE80` (390 B), `001FD610` (176 B) | the std::map-style emplace beneath the `.fex` value store: `001FD010` is insert-at-hint (node alloc through the `+0x30` fn table, node size `0x48`), `001FCE80` is the ordered lower-bound walk over a `+0x8`-headed tree keyed at `node+0x20`, `001FD610` the hint-position check + node allocation | `001FD020` / `001FCE99` / `001FD628` |
| string stores | `001FE020` (92 B), `001FE080` (92 B) | ~~twin clear-and-free passes over the font's two maps at `+0x100` and `+0xE0` — the kerning and expansion maps' erase-all~~ *Corrected 2026-09-14 (FABLE, `FRONTIER-CONTRA-001B4D70-NAMEFIELDS`):* **move-assign stores into two string fields.** Each takes a temporary `{begin, end, capacity, allocator}` string. It range-assigns the temporary into font `+0x100` / `+0xE0` through the 154-byte assign-or-grow body (skipped when source and destination are the same field), then frees the temporary's buffer through its allocator's `+0x18` virtual when the capacity exceeds 1 (`001FE042`–`001FE072`). The root calls them right after building each temporary through `001EDF00` + `001A4BF0` (`001B4F90`–`001B4FF3`). Neither body walks a tree or unlinks a node. Which names the two strings hold is not read here. | `001FE036` / `001FE096` |
| accessors | `001E9A20` (8 B), `001FDF80` (10 B) | a byte-field getter (`[rcx+0x2378]`) and the `[+0x18]==[+0x60]` equality predicate | `001E9A20` / `001FDF86` |

So the completion's reach is exactly the font object's own data layer: issue the two list
requests, look the font up in the id map, build it, and insert glyph/expansion records through
one shared ordered-map implementation — the same tree shape (`head +0x8`, key `+0x20`, node
`0x48`) at every level.

### The `001FDC10` exclusive subtree — all 7 members bound (SWE2-FRONTIER, followup queue)

The `.ker` pair store `001FDC10` — find the record's first dword in `font+0x70`'s ordered map,
overwrite `node+0x24` with `adjust` on a hit (`001FDC66`), else insert (the `r8d` middle field is
passed but unread) — owns **7 frontier functions**:
the EASTL ordered-container insert layer beneath it. The family is a 2×2 — {unique,
hint-aware} × {formed-node, copy-constructed pair} — over the same `+0x8`-headed tree keyed at
`node+0x20`. Interior cites are one instruction inside each declared extent
(`interior_cite.py scan`; no boundary crossings).

| cluster | members | role | interior |
|---|---|---|---|
| find + miss insert | `001FC420` (339 B) | the lower-bound walk the root opens with: descends `head+0x18` by signed compare on `node+0x20`; on a miss it range-inits a local pair (`001EDF00`), copy-constructs `{first,0}` through `001FBEF0`, inserts via `001FCCE0`, then frees the temporaries | `001FC460` |
| unique insert (formed node) | `001FC890` (342 B) | the no-copy unique-insert backstop: tree descent, ~~node alloc~~ **iterator step** `0016D720` + the allocator's `[rax+0x10]` virtual, ~~`0016D840` release on the duplicate path~~ **`0016D840` insert-and-rebalance** (see the correction below) | `001FC94E` |
| hinted insert (formed node) | `001FC9F0` (330 B) | the hint-aware unique insert `001FDC10` calls directly on a lower-bound miss: ~~`0016D6D0` alloc~~ **`0016D6D0` iterator step — the hint validation**, node constructor `001FD4B0`, falls back to `001FC890` | `001FCA98` |
| unique insert (copy pair) | `001FCB40` (404 B) | `001FC890`'s copy-construct twin — same descent and alloc, but `001FBEF0` builds the `{key, adjust}` pair into the fresh node | `001FCC18` |
| hinted insert (copy pair) | `001FCCE0` (412 B) | `001FC9F0`'s copy-construct twin, called by `001FC420`: ~~`0016D6D0` alloc~~ **`0016D6D0` iterator step**, value constructor `001FD550`, falls back to `001FCB40` | `001FCDBB` |
| node ctor (formed) | `001FD4B0` (155 B) | links the already-formed node — allocator `[rax+0x10]` virtual + ~~`0016D840` on the bail path~~ **`0016D840`, which is the insert itself rather than a bail** | `001FD505` |
| node ctor (copy) | `001FD550` (178 B) | the copy flavor — `001FBEF0` pair copy-construct into the node before ~~the `0016D840` bail path~~ **the `0016D840` insert** | `001FD5D0` |

`001EDF00`/`001FBEF0`/`001FC320`/`0016D6A0`/`0016D720`/`0016D6D0`/`0016D840` are shared
~~allocator/string/CRT~~ **EASTL container-runtime, allocator and CRT** helpers — deliberately not
census members.

> **CORRECTED 2026-09-15 (OPUS) — three of these are the red-black tree's OWN operations, not
> memory operations, and the control is that not one of the four has a single callee.**
>
> Read whole from the shipping image, authority hash `73461D08…9721F8`, image base `0x120000`.
> Degrees from `work/graph/edges.tsv`.
>
> | address | size | callees | the page said | what the bytes do |
> |---|---:|---:|---|---|
> | `0016D6D0` | 68 B | **0** | “alloc” | rb-tree **iterator step**: if `[this]` is non-null, descend the `+8` chain to its last node; otherwise climb `+0x10` parents while this is the parent's `+0` child |
> | `0016D720` | 94 B | **0** | “node alloc” | the **mirror iterator step**, gated on the nil/colour byte `+0x18`: descends the `+0` chain, climbs while this is the parent's `+8` child |
> | `0016D840` | 532 B | **0** | “release” / “bail path” | rb-tree **insert and rebalance**. Its first four stores BUILD a node — `[rcx+0x10] = rdx` (parent), `[rcx] = 0`, `[rcx+8] = 0`, `[rcx+0x18] = 0` — then `r9d` picks the side and the head's `[r8]`/`[r8+8]`/`[r8+0x10]` min/max/root are updated |
> | `0016D6A0` | 3 B | **0** | (lumped in) | a Control Flow Guard dispatch stub, 2,479 callers |
>
> **The control.** An allocator must call something. `0016D6A0`, `0016D720`, `0016D6D0` and
> `0016D840` have **zero callees between them** — they are leaf routines that only walk pointers.
> `0016D840`'s own GFZ code domain already said so: `CxxStandardLibrary.OrderedContainerRuntime.
> RedBlackTreeInsertRebalance`.
>
> **The node layout falls out of the three bodies and agrees with this page.** `+0` and `+8` are
> the two child pointers, `+0x10` the parent, `+0x18` the nil/colour byte — which puts the key at
> `+0x20`, exactly where §4.2 above already says the tree is keyed. Two independent readings, one
> from the walk functions and one from the insert cluster, agree.
>
> **Why the page read it this way, which is worth recording.** A hint-aware insert calls the
> iterator step to validate its hint before deciding where to link, and it does so at exactly the
> position an allocation would occupy. The mistake is a plausible one and the surrounding cluster
> analysis — the 2×2 family, the descent, the interior cites — is unaffected.
>
> **NOT corrected, and NOT closed by this — and the subsystems are deliberately NOT named here.**
> `0016D6D0` still raises two `UNACCOUNTED NEIGHBOUR` rows on this page in `audit_crossrefs`
> (13 edges and 2). The audit tests whether a document MENTIONS the neighbouring subsystem, so
> writing their names into this block — even inside a sentence saying the finding stands — would
> close it. A first draft of this block did exactly that: `check_publish_neighbours.py` reported
> HEAD 2, HEAD+publish 0, and refused it with *“ADDS NOTHING. A finding already standing at HEAD
> is not this publish's to answer.”* It was right, and this is the corrected block. The two names
> are in `OPUS-REQ-FRONTIER-PASS22-FONT-0016D6D0`, which is the page owner's to answer; whether
> the rule that raises the rows is right at all is `OPUS-REQ-FABLE-PASS22-SUBSTRATE-SYMMETRY`,
> which is FABLE's ruling and not OPUS's. The sentence above that calls these helpers shared and
> deliberately excluded is the page's own accounting and predates both.
>
> **The three of them belong to one family, and it is not documented anywhere.** `0016D840`'s
> own code domain names it — `CxxStandardLibrary.OrderedContainerRuntime.RedBlackTreeInsertRebalance`
> — and reading the two iterator steps against it gives a coherent set with the node layout above.
> The rest of that family, its rotations and its erase, its caller census and the four different
> code-domain heads its six members carry, are **deliberately not cited on this page**: a page
> that cites an address inherits its whole caller set as neighbours, and citing the erase here
> would have raised a **new** `UNACCOUNTED NEIGHBOUR` against a subsystem this page has never
> mentioned — six edges, manufactured by a correction. A draft of this block did cite it. The
> family goes to `OPUS-PROPOSE-ORDERED-CONTAINER-FAMILY-PAGE`, which is where a container
> runtime should be documented rather than on a page about kerning.
>
> **A CORRECTION TO THIS CORRECTION, 2026-09-15 (OPUS), made the same day:** my first pass replaced
> *“allocator/string/CRT”* with *“container-runtime and CRT”* and that dropped a word which was right
> for one of the seven. **`001EDF00` really is an allocator**: 14 bytes, `lea` a vtable, store it at
> `[rcx]`, return `rcx` — the trivial constructor of a class the image's own RTTI names
> `.?AVallocator_memory_log@eastl@@`, constructed at 230 sites. `001FC320` is a container list
> destroy and `001FBEF0` a pair copy-construct; neither is an allocator either, and **“string” was
> wrong for all seven.** The line now reads EASTL container-runtime, allocator and CRT. Correcting a
> wrong word with a differently wrong word is still a defect, and this is the second half of it.
>
> **That RTTI name was not mine to find:** [eastl-strings-containers-and-the-logging-allocator.md](../../23-Third-Party-Libraries/EASTL/eastl-strings-containers-and-the-logging-allocator.md)
> already carries `001EDF00` in its key-address table and already records that its
> `Runtime.ContainerStringSupport` tag is a category-boundary defect. I re-derived both and cited
> neither until now.
>
> It is also what identified the tree family's library — see
> [the-ordered-container-runtime.md](../../24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-ordered-container-runtime.md),
> `OC-1`. The cluster this page documents is an **EASTL** ordered container, which §4.2's own heading
> said before any of this was read.
>
> **One naming point for the type registry.** `0016D6D0` carries the code domain
> `Runtime.ContainerStringSupport` while its sibling `0016D840` carries
> `CxxStandardLibrary.OrderedContainerRuntime.RedBlackTreeInsertRebalance`. Nothing in `0016D6D0`
> touches a string. Two members of one family are tagged into two different domains.

## 5. Corpus survey

Requested kerning: `us` subtitle 8,887 pairs, `us` `venus` 1,111, six `stf` fonts 1,237 each (`us` and `jp`),
`venus` 325 and `square` 51 in every CJK list, `kr` `font00` 380 and `kr` subtitle 39. Requested expansion
lists: `fontex_expand` 389–482 keys, `fontex_subtitle` 171–177 keys with 17,334–21,001 values, `fontmonster`
6–14 keys. The same keys recur across languages (`0x22949AE0`, `0x2294A029`, `0x5202F7B0`, …).

## 6. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run on the page's addresses and on the ones this pass introduced; only
`KE-1`, this page's own row, comes back. Archive read, never written; nothing executed.)*

### Every published figure reproduces

**34 `.ker`, 14 `.fex`, 63 `.dat`, 5 `fontlist.ah`** under `gamedata/d3d11/artdata/font/`; **62 of 63**
`.dat` named by a list, all 62 sized `0x28 + 0x24 × glyphCount`, the one exception `us/fontex_expand`
both unnamed **and** the only size mismatch and the only `+0x18` float that is not 1.0 (2.4).
**25 of 34** `.ker` requested and the nine that are not are exactly the nine named — `font00` in `ch`,
`cn`, `jp`, `us`, `fontex_expand` in `ch`, `cn`, `kr`, `font_iwa_g12` in `jp`, `us`. **12 of 14** `.fex`
requested, every one walking to its exact end with no repeated key; the two that are not requested do
not parse.

§5's counts are exact, file by file: `us/fontex_subtitle` **8,887** pairs, `us/font_venus` **1,111**,
six `stf` fonts **1,237** each in both `us` and `jp`, `font_venus` **325** and `font_square` **51** in
every CJK list, `kr/font00` **380**, `kr/fontex_subtitle` **39**.

§3's language map reproduces from the bytes: `<= 0` and anything unmatched → `008F8188` (`jp`),
`1`–`6` → `008F8620` (`us`), `7` → `008F8728` (`kr`), `8` → `008F8678` (`ch`), `11` → `008F86D0`
(`cn`) — `001B44A9`–`001B4532`, all five paths matching §4's table.

### ✔ New: no flag ever asks for a file that is not there

The page tests the correspondence from the file side. From the **flag** side, over all 63 `.dat`:

| | |
|---|---:|
| flags bit 0 set, `<font>.ker` **missing** | **0** |
| flags bit 1 set, `<font>.fex` **missing** | **0** |
| `.ker` present, bit 0 clear | 9 |
| `.fex` present, bit 1 clear | 1 |

**All the slack is in one direction.** Given §3's table — the readers have no check that the request
succeeded, and the two failure strings go to a `ret 0` stub — *"every flag's file exists"* is the
invariant the shipped data actually keeps, and the one a modified font set has to keep too.

### ✔ New: the two unrequested `.fex` are unrequested for two different reasons

§*Corpus validation* groups them. They are not alike:

* **`us/fontex_expand`** — its `.dat` is **in no list at all**, the only one of 63. Its flags are 2,
  so if a list named it the `.fex` *would* be requested, and it does not parse.
* **`us/fontex_subtitle`** — its `.dat` **is** in the `us` list, and its flags are **1**: bit 0 only.
  So its `.ker` is requested (and is the **largest in the corpus**, 8,887 pairs) while its `.fex`,
  sitting beside it, is not.

### ✔ New: the triple layout is the value store's own argument list

Read as `{key, index, value}` the two files are whole — both sizes divisible by 12, and **per key the
index column runs 0, 1, 2, … with no gap**:

| file | bytes | triples | distinct keys |
|---|---:|---:|---:|
| `us/fontex_expand.fex` | 108,384 | **9,032** | **483** |
| `us/fontex_subtitle.fex` | 137,772 | **11,481** | **217** |

`{key, index, value}` is exactly the argument list of **`001FDB50(font, key, i, value)`**, the
per-value store the `.fex` reader calls. So these two files hold the same data as a requested `.fex`
**written one row per value** instead of `{key, count, value[count]}` — an unpacked form of the same
key space: their key counts (483, 217) sit beside the requested files' (`fontex_expand` 389–482,
`fontex_subtitle` 171–177), and their first keys, `0x2294A029` and `0x22949AE0`, are keys the
requested files carry too. **Stated as a reading of the layout**; no code writes this form, and
nothing here says what wrote it.

### ✖ Corrected: where the walk actually dies, and which number is in the way

The corpus row says *"the second word, read as a count, is `0x2294A029`"*, for both files. Measured:

* the **first** record parses in both — key `0x2294A029` / `0x22949AE0`, count **0** (the second word
  is `0`, not the key);
* the walk dies on the **second** record, whose count field at file offset 12 holds **the file's own
  first key** — `0x2294A029` in `us/fontex_expand` and **`0x22949AE0`** in `us/fontex_subtitle`.

The two numbers are different, and that the failing count *is* the first key again is the tell for the
triple reading rather than an incidental value.

### ✖ Clarified: the flags distribution is over 62, not 63

`0 in 26, 1 in 24, 2 in 11, 3 in 1` sums to **62**, and sits in a table whose row above reads
"63 font `.dat`". Over all 63 the distribution is **26 / 24 / 12 / 1** — `us/fontex_expand`, flags 2,
is the twelfth.

### Where the headline's second clause actually bites

*"The ones that do not parse are exactly the ones nothing requests"* is carried **entirely by two
`.fex` files**: all 34 `.ker` are a whole number of 12-byte records, requested or not, so on that side
the correspondence cannot fail. The page half-says this with *"(so are the other 9)"*; worth saying
outright, because the `.ker` half is a vacuous truth and the `.fex` half is a 12-against-2 result.

**Not claimed.** Anything in `KE-1`: what a key identifies, what the lists are for, the rest of the
`.dat` header and the `0x24`-byte glyph records, which in-game value selects which list. What wrote
the two triple-form files. Whether the over-read holes §3 names can be reached by shipped data —
**none of the shipped files reaches them**, which is a property of the data, not a check in the code.


## 7. What this document does not claim

- [x] **KE-1.** What a `.fex` key identifies and what the character lists are used for — the key is the
      event path hash and the lists are per-event expansion-glyph tables; the `+0xA8` map's reader is
      `001E9D20`/`001FDD60` (2026-09-25 section). ~~Still open: what the other `.dat` header words and
      the `0x24`-byte glyph records hold, which
      in-game language value selects which list (the caller `0017F9E0` was not read), and why the `us`
      directory ships `fontex_expand.dat` and two `.fex` files in a triple layout that no list requests.~~
      **CLOSED 2026-09-27 (SWE2-DATA):** the `.dat` header words and glyph records are corpus-decoded
      (2026-09-26e section); the language selector is `001B44A0` via the `0017F9E0` adapter (below);
      the `+0x20`/`+0x24` header pair is **dead-authored** — written to record `+0x1C`/`+0x20`, read by
      nothing (accessor census in the 2026-09-27 section); and the `us` `fontex_expand.dat`/triple
      `.fex` files are orphaned **older serializations** nothing requests — the `.dat` is an 8-word-header
      variant and the triple `.fex` cannot flow through `001B4C00`'s `{key,count,cps[]}` grammar.
      `KE-1`.
      **FIRST SUB-QUESTION ANSWERED 2026-09-24 (SWE2-DATA, section below): the `.fex` key is
      `00674A00("event\<dir>\<name>")` and the lists are per-event expansion-glyph tables.**
      **ONE SUB-QUESTION ANSWERED 2026-09-13 (OPUS): the language-to-font-list mapping, read out of
      the caller this bullet says was not read.** `0017F9E0` is 44 bytes and is **an adapter, not the
      selector** — it fetches a context from `001B5FB0` (33 B) and tail-jumps to **`001B44A0`** (236 B)
      with the original two arguments. `001B44A0` is the dispatch, and `edx` is the language value:

      | `edx` | branch | font directory |
      |---|---|---|
      | `1`–`6` | `cmp edx,6 / jle` | **`us`** |
      | `7` | `cmp edx,7 / je` | **`kr`** |
      | `8` | `cmp edx,8 / je` | **`ch`** |
      | `11` (`0x0B`) | `cmp edx,0x0B / jne` → else | **`cn`** |
      | `≤ 0`, `9`, `10`, `≥ 12` | fall through to `0x1B451D` | **`jp`** |

      Each arm `lea`s **two** strings — `./GameData/D3D11/ArtData/font/<dir>/fontlist.ah` and the bare
      directory `./GameData/D3D11/ArtData/font/<dir>/` — so the function yields the manifest path and
      its base directory together. **`jp` is the default**, reached by every value the four explicit
      comparisons do not claim, including the gaps at `9` and `10`.

      **AND IT BEARS ON THE LAST SUB-QUESTION.** *"Why the `us` directory ships `fontex_expand.dat`
      and two `.fex` files in a triple layout that no list requests"* — **six language values
      (`1`–`6`) all resolve to `us`**, against one value each for `kr`, `ch` and `cn`. A directory
      serving six languages is the one place a triple layout would be needed. **That is a motive, not
      a mechanism**, and it does not identify which of the six wants which file.

      **The rest of KE-1 stands closed:** the `+0xA8` map's reader is traced
      (2026-09-25 — `001E9D20`/`001FDD60` bind `mapA8[eventKey]` into `ctx+8`);
      the `.dat` header words and `0x24`-byte glyph records are corpus-decoded
      (2026-09-26e); the `(eax,r8d)` binding key is decomposed (dedup tag only —
      the session key is the `lib+0x278` descriptor slot); and the
      `+0x20`/`+0x24` header pair is closed as **dead-authored** by the
      2026-09-27 accessor census below — written to rec `+0x1C`/`+0x20`,
      never read.

## SWE2-DATA update (2026-09-24) — the `.fex` key is the event path hash; the lists are per-event expansion glyphs

**The CJK `.fex` record** (`{key; count; u32 cps[count]}`, chained to EOF) binds to one
event file: **`key` is the engine path hash `00674A00`** (`eax = 0x1505`; per byte
`eax = eax*0x21 + movsx(c)`; finished by `btr 0x1F`) **of the windows-style path
`event\<dir>\<name>`** — `event\alc_a\alc_a0100` → `0x22949AE0`,
`event\bhm_d\bhm_d0101` → `0x48196775`, `event\gil_z\gil_z0100` → `0x419B382A`,
`event\rbn_a\rbn_a0980` → `0x6357FC94`. Reproduced for 9 verified events; sibling
scene names (`…a0100`/`…a0101`) produce keys differing by +1 because the name's
last char lands at the hash end. The same keys appear in the `jp`, `ch`, `cn` and
`kr` files — the key is a locale-invariant event identity.

**The values** are the event file's expansion-glyph codepoints in first-use order —
the same glyphs the event's embedded TIM2 sheet (`.ebp` section 6) holds as bitmaps
**in the same record order** (verified on `alc_a0100`: cells read 元老院一派…, ~10 px
packed pitch for subtitle sheets, ~20 px for `fontex_expand` sheets — see
[`section-006.md`](../../25-EBP-Script-Container/Sections/section-006.md) §5).
In an `.msb` subtitle bank, codes `18 xx`–`1B xx` index
`cps[(lead - 0x18) * 0xE0 + sub - 0x20]`: `alc_a0100` decodes to the Rabanastre
senate briefing verbatim ("元老院一派の抵抗は完全に鎮圧しました…"), `bhm_d0101`
to the Bahamut airship battle ("どうだ 飛べそうか？"…"主砲をアレキサンダーへ向けろ！"),
`naf_b0400`, `nal_c0200`, `rbn_a0980`, `dor_c1200` et al. all verbatim.

**The `us` serialization is the same keying, different layout:** `{key; index; u32 cp}`
12-byte triples — `us/fontex_subtitle.fex` opens with
`{0x22949AE0; 0; 'T'}{;1;'h'}{;2;'e'}{;3;'c'}{;4;'o'}…` = "The complices of the
Senate…" — the English text of `alc_a0100`'s opening line. This is the
§6 "triple layout" the audit measured (9,032 / 483 keys and 11,481 / 217): the
keys are the same event hashes, one triple per slot instead of one headered
list per event.

**Which plane needs the table.** `18`–`1B` codes are `font1` indices
`tbl[lead & 0xF] + sub - 0x20` (`0x7E0+` for `18` in mode1). A `.fex` chunk is
only consulted past the end of `font00.dat` — so `ch`/`cn` (`font00` ≈ 2,360
records, covering `0x7E0+` entirely) resolve the plane globally and their event
banks barely use the codes (26–29 files, all resolved or short-chunk benign),
`us` mode0 routes `18`-codes to the global `fontex_subtitle.dat` (10 banks), and
`jp`/`in` (`font00` = 1,319 < `0x7E0`) are the locales where every `18`-code is a
slot in the event's own `.fex` chunk — the `in` archive ships no `fontex_*.dat`
at all, so the `.fex` lists **are** its expansion font.

**Corpus verification (2026-09-24):** all **180 `in` event banks** that use
expansion codes bind by key — 158 into `fontex_subtitle.fex`, 22 into
`fontex_expand.fex` (same chained structure; 8 events have a chunk in both);
0 misses, 0 short chunks, 0 unresolved glyph tokens. Key derivation and
decoding are implemented in
[`decode_msb.py`](../../01-Script-VM-Native-Bridge/ATEL-Control-Modules/decode_msb.py)
(`fex_magic`, `load_fex_chunks`, `msb_codes`; `bind_fex` survives as a
score-based fallback for non-event banks such as control-module `.msb`s).

This answers KE-1's first sub-question — **the `.fex` key is the event path
hash `00674A00("event\<dir>\<name>")`, and the lists are per-event-file
expansion character tables consumed by the `.msb` subtitle decoder.** What a
key's *map at font `+0xA8`* is for at runtime, and the other `.dat` header
words, remain open.

## SWE2-DATA update (2026-09-25) — the `+0xA8` map's reader is found: `001E9D20` binds it per text run

The `.fex` two-sided contract is now closed. **Two singletons are
involved, corrected 2026-09-26d (earlier drafts conflated them as
"ctx"):** the **font library `lib` at `0x1F81200`** — asserted and
loaded by every `001Bxxxx` wrapper (`001B5FE0`/`001B6030`/`001B5FB0`
the getter; `001B4D70`/`001B4C00`/`001B5750`/`001B5480`/`001B4590`/
`001B47A0`/`001B6350`/`001B58E0`/`001B51C0` all operate on it) — and
the **text context `ctx` at `0x1F811F8`** (a 0x2380-byte object
lazy-built by `001B5F10` ← `0017D4C0`, the object `001E9D20`/`001E9860`
bind). `lib` layout relevant here:

| offset | contents |
|---|---|
| `+0x00` | `fontSetBase` — `fileId = base*32 + member` (`001B4590`); no writer found — every shipped `.dat` fileId is `1`–`22` (`< 32`), so `base = 0` in all five locales and the field stays ctor-zero |
| `+0x28` | second `fileId→record` map — `0020B5F0(lib+0x28, &fileId)` insert |
| `+0x30` | `map<u32 fileId, r15*>` — written by `001B4D70`/`001B4C00`, read by getter `001B51C0` |
| `+0x68`/`+0x98` | session-activation maps filled by `001B58E0` |
| `+0xD0` | dependent-load node pool (`001BA860`; `002124C0` unregisters) |
| `+0x190` | pending-binding descriptor pool |
| `+0x250`/`+0x258`/`+0x260`/`+0x270` | pending-binding queue vector (begin/end/cap/last-found) |
| `+0x278` | descriptor slot table, 16 entries — slot index = the session `sel` |

`ctx` (`0x1F811F8`) layout relevant here:

| offset | contents |
|---|---|
| `+0x00` | active bound `r15` (the 0x120-byte font record) — `[ctx]` read by `001E9860`/`001E9BD0`/`001E8070` |
| `+0x08` | **pointer to the bound `vector<u32>` cp table** — `mapA8[eventKey]` node value, installed by `001E9D20` |
| `+0x10` | bound-font resource record slot — `0x38`-byte records on the `ctx+0x30`/`ctx+0x730` grids (`fileId + slotIdx*32` index; `{fileId@0; resA@8 via 006B5C70(r15); resB@0x10 via 005C5310(r15)}`, the subtitle advance source) |
| `+0x18`/`+0x1C` | last-bound key pair (cache in `001E9D20`) |
| `+0x28` | **previous glyph record** — `001E9780` reads its `+0x20` (the kern cp) as the pair's left element |
| `+0xE70` | session-record pool |
| `+0xF38` | `map<u64 {lo,hi}, session*>` — per-source binding table read by `001E9D20` |
| `+0xF68` | **fontclut table: 28 × `0x24`-byte colour slots** `{inited@0; mShadowRGBA@4..0x10; mFontRGBA@0x14..0x20}` — see the 2026-09-27 section |
| `+0x1358` | default fontclut record (used when the run's slot index is negative) |

`r15` (0x120 bytes, ctor `001FC060`): `+0xA8` = `map<u32 eventKey, vector<u32> cps>` (sentinel `+0xB0`, root `+0xC0`, written by `001FDB90`/`001FDB50` from `.fex` records), `+0x40` = `map<u32 cp, glyph-record>` (the cp→bitmap-record map — the slot-6 TIM2 side), `+0x34` = a float metric (`001FDDB0`).

**The read chain:**

- **`001E9D20(ctx, lo=eax, hi=r8d, id=r9d)`** — the activator, run per text
  source change: walks `ctx+0xF38` for the u64 key `(r8d<<32)|eax` → session
  record `rdi` (`[rdi+4]` = fileId 1–31, `[rdi+8]` = eventKey). Then
  `r15 = 001B51C0(lib, [rdi+4])` (the `lib+0x30` find via `001B5FB0()`) and
  **`[ctx+8] = 001FDD60(r15, [rdi+8])`** — `001FDD60` is the `mapA8`
  tree-find returning `node+0x28`, the `.fex` cp vector. It then selects the
  `(fileId,slot)` metric slot into `[ctx+0x10]` via `006B5C70(r15)` and
  `005C5310(r15)` and caches the key at `ctx+0x18`/`+0x1C`.
- **`001B58E0(lib, key)`** — session creation: `lib+0x30[key]` → r15, then a
  refcounted session object (`[s+8]` = vfn `001B6229`, `[s+0x10]` = r15,
  `[s+0x20]` = a copied table via `001FDF10(r15)` → `001A1E40` vector-assign)
  linked into `lib+0x68`/`+0x98`.
- **Walker `002AC2F0`** (the compiled-protocol glyph fetch): for two-byte
  codes, `esi = tbl[lead & 0xF] + sub - 0x20` — `tbl` is **two parallel
  16-entry u32 tables at `0x916570`/`0x9165B0`** selected by flag
  `0x209CC38`, which is **not a build constant**: `002AB7D0` (the
  language-mode boot init already documented for the msb decoder) writes
  flag and bound *together* from language id `[0x1E02814]` (`00229E40`):

  | language ∈ {7,8,0xB} (CJK family — `(id-7)&~5==0` minus `0xC`) | `0x209CC38` = 1 | `0x1E0CDF8` bound = **`0x1C`** |
  |---|---|---|
  | all other languages | `0x209CC38` = 0 | bound = **`0x18`** |

  | table | planes `10`–`17` | planes `18`–`1B` | planes `1C`–`1F` |
  |---|---|---|---|
  | `0x916570` (default) | `0xE0,0x1C0,0x2A0,0x380,0x460,0x540,0x620,0x700` | `0,0xE0,0x1C0,0x2A0` | `0x460,0x540,0x620,0x700` |
  | `0x9165B0` (CJK) | same | **`0x7E0,0x8C0,0x9A0,0xA80`** | `0,0xE0,0x1C0,0x2A0` |

  So the two modes swap the lead classes: in the default mode expansion
  leads are `18`–`1F` (low-window `esi` for `18`–`1B`, `0x460`–`0x7DF`
  for `1C`–`1F`); in CJK mode expansion leads are `1C`–`1F` (low window
  `0`–~`0x33F` — exactly the ≤342-entry `.fex` vector extent) while
  planes `18`–`1B` become *ordinary font planes* covering the real CJK
  glyph range at `esi` `0x7E0`–`0xA80`. The event `.fex` codes land in
  the same low `esi` window under either mode. (`002B0280` — the
  line-layout walker — reads the same flag/table pair; only `002AB7D0`
  writes either global.)

  `lead >= [0x1E0CDF8]` takes the expansion arm:
  `[rdi+0x60] = [rdi+0x68]` when the run's cached expansion table exists,
  else it is built via `0039BA30([rdi+0xA6])` and
  `0017FD30(sel=[rdi+0xA6], plane 0)` re-binds the ctx session; `lead <
  bound` binds the default `0039C4A0` table + `0017FD30(sel 7|0)`. Both arms
  converge on the *same* `esi` resolution — the arm selects only the atlas
  object (`[rdi+0x60]`, whose `+0xC` feeds `0020E600` → the per-index 8-byte
  flag/pitch slot at `table + esi*8`).

  `001E9860(ctx, esi)` then resolves the index: **`esi < size(ctx+8)` →
  key = `ctx+8[esi]`; `ctx+8 == NULL` → key = `esi` raw; `esi` out of
  bounds → return 0** (the walker's miss arm takes the 5-bit pitch field
  `[r14]>>32 & 0x1F` instead of a glyph record). In-range keys go to
  `001FDEC0([ctx], key)` = `r15+0x40` map lookup → glyph record.

  Which arm a code takes is decided by the *session's* binding:
  `001E9D20` stores `ctx+8 = 001FDD60(r15, sess.eventKey)` — **NULL on a
  miss**. The `sel 7|0` sessions the normal arm binds are filed with
  `eventKey = 0` by `0017FC00`/`001B6470` *without* `001B4590`'s
  `mapA8` validation, and `mapA8[0]` can never exist (every `mapA8` key
  is a nonzero `h33` path hash) — so **default bindings always get
  `ctx+8 = NULL` → raw-`esi` keys into `r15+0x40`**. That is the
  ordinary-text path: `r15+0x40` is keyed by compiled index (the
  verified `font00.dat` record order), covering the CJK `0x7E0`–`0xA80`
  planes directly. Only an event-bound session (validated `mapA8`
  entry) produces a non-NULL `ctx+8` — the `.fex` vector is a small
  index→key remap covering exactly the low expansion window (`us`
  `alc_a0100`: `lead 0x18` + `sub = 0x20+i` → `esi = i < 66` →
  remapped), and `esi ≥ 0x7E0` needs no vector coverage at all.
- Per-glyph advance: `rbx+0x1C` = record `w7` (the `adv` word — `w6`
  is a byte-identical duplicate corpus-wide) via `0017F9C0` →
  `trunc(adv / fontScale)`; `rbx+0x20` = `w8` kern cp, `−1` gated at
  `002AC527` → `0017F8E0` → `001E9780` → `001FDDD0` pair find
  (structurally unreachable — see §3). Plus `[r14]` flag bits —
  the advance for expansion glyphs routes through the `(fileId,slot)` metric
  slot bound at `ctx+0x10`, not through the TIM2.

### SWE2-DATA update (2026-09-25b) — the binding producer: session `+8` is `h33` of the event's own path

The `(eax,r8d)` key and the session-record writer are now traced end-to-end.

**Session record** (16 bytes, pool `ctx+0xE70`, filed by `001E7F90`):
`{u32 sel, u32 fileId-composite, u32 eventKey, u32 plane}` — inserted into
`ctx+0xF38` under the u64 key `(plane<<32)|sel`. `001E9D20`'s `(eax,r8d)` is
exactly that pair: **`eax` = font-selector, `r8d` = plane**.

**Adapters that key it:**

| caller | shape | meaning |
|---|---|---|
| `0017FD00(x)` | `001E9D20(ctx, lo=x, hi=2, id=0)` | plane **2** — the default plane (see below) |
| `0017FD30(fontSel, flag, srcId)` | `hi = flag ? 1 : 0`, `id = srcId` | planes **0/1** — the live text-source planes; `fontSel` selects the font slot, `srcId` is passed through to the metric-slot bind |

**Registration.** `001E7F90` has exactly three callers:

- `0017FC00(idx)` — init-time default: `001FDF70(lib)` (current font-set index)
  `*32 + idx` as the fileId-composite, **eventKey = 0, plane = 2**. Called
  only by `003643A0`/`00365810` (font subsystem init).
- `001B6470(obj, slot, index)` — `obj+0x278[index]` record install,
  `composite = [obj]*32 + slot`, **eventKey = 0**.
- `001B4590(lib, desc)` — **the event-bound registrar**: for each arm it first
  calls `001FDD60(r15, [desc+0x14])` — *validating that `mapA8[eventKey]`
  exists before binding* — then `001E7F90(ctx, sel, [desc+0x18],
  eventKey=[desc+0x14], plane)`. `desc+0` holds the font-set id (used as
  `[desc]*32 + plane+2`-style composites for the `lib+0x30` walk).

**The pending-binding queue** at `lib+0x250` (vector of descriptors; `+0x258`
end, `+0x260` cap, `+0x270` last-found):

- **`001B6350(lib, sel, flag, pathStr)` — the event-key producer.** Scans the
  queue for a duplicate `{+4==sel, +0x10==flag}` (a hit jumps to the
  `0016D6A0` stub), else pool-allocs a descriptor from `lib+0x190`, stores
  **`[desc+0x14] = 00674A00(pathStr)`** — the same packfile path hash used for
  `.ebp` directory keys — plus `+4=sel`, `+0x10=flag`, `+0x18=arg4`, and pushes
  it onto the queue (growth via `001AB570`).
- `001B6430(lib, id)` finds a queued entry by `+4`/`+0x10` and sets `lib+0x270`.
- `001B5330` pops/erases a queued entry (same head/tail walk, `+0x258 -= 8`).
- **`001B47A0(lib, arg)` — the drain**: takes `lib+0x270` (or scans
  `lib+0x250..0x258` for `{+4==id, +0x10==0}`), removes it from the queue, sets
  `[desc+8]=arg`, and calls `001B4590` — which validates `mapA8[eventKey]` and
  files the session.

**Who feeds it.** `0017FA90(sel, flag, pathStr, arg4)` is a thin lib-thunk
into `001B6350`, called from:

- **`00332250(kind, id, sel, flag)`** — resolves the resource's canonical
  path via `002DF980(kind, id)` — the in-image `g_pathTables` at `0x0215F000`
  (the same `\plan_master\<X>\event\<X>` table verified for the event-slot
  feeder) — copies/normalizes it on the stack, then `0017FA90`. Called by
  `00330310`/`003306E0`, the resource-registration layer.
- `00575710` — calls `0017FA90`, `0017FB70` (→`001B6430` queue-find) and
  `0017FBE0` (→`001B5330` queue-erase) — the driver that queues, finds and
  clears pending bindings.
- `003304A0` — the `.ebp` directory dispatcher — calls `0017FB70`/`0017FBE0`
  while walking section entries, clearing pending bindings as the event's
  files arrive.

So the event half of the contract is: **the resource layer queues
`{sel, flag, h33("event\<dir>\<name>")}` when a text-binding-eligible resource
registers; `001B4590` only files the session once the `.fex` chunk for that
key provably exists in `mapA8`; `001E9D20` then binds it per text-run.** A
binding requested before its `.fex` loads waits in `lib+0x250`; a `.fex`-less
eventKey can sit queued until `001B5330`/`001E9A30` evicts it.

### SWE2-DATA update (2026-09-26) — the `.dat` section and the unified key space

`001B4D70(lib, blob)` is the `.dat` binder (`font00.dat`, `fontex_*.dat`
alike). `rbx = [blob+0x20]`..`[blob+0x28]` is the section image; layout:

| offset | field | meaning |
|---|---|---|
| `+0x00` | u32 | **fileId** — the `lib+0x30`/`lib+0x28` map key; the `.fex` section of the same font asserts on this already existing (`001B4D13` assert) |
| `+0x04` | u32 | record capacity — `edx` to ctor `001FC060`, lands at rec `+0x18` |
| `+0x08` | u32 | **atlas width** in px (0x800 / 0x400 / 0x200) → rec `+0x24` |
| `+0x0C` | u32 | **used tile extent** `ceil(glyphCount / floor(atlasW/cellH)) × cellH` → rec `+0x28` — reproduces on every listed font (`font00` jp: `ceil(1319/37)×55 = 0x7BC`, `fontex_subtitle` us: `ceil(1301/31)×66 = 0xAD4`, `bookman`: `1×40`, `stf_a`: `2×32`); `square`/`venus` carry authored values that don't reduce to it |
| `+0x10` / `+0x14` | u32 | **glyph cell width / height** in px (48×55, 40×40, 32×32, 64×66 …) → rec `+0x2C`/`+0x30`; each glyph record repeats them at `+0x10`/`+0x14` |
| `+0x18` | float | the font metric — lands at `r15+0x34` (`001FDDB0` reads it back); 1.0 in 62 of 63, 2.4 in `us/fontex_expand` |
| `+0x1C` | u32 | flag bits: `&1` → `001B5750` requests `name.ker` (completion `001B6080`); `&2` → `001B5480` requests `name.fex` (completion `001B6030`) — see below |
| `+0x20` / `+0x24` | u32 | **dead-authored metric pair** → rec `+0x1C`/`+0x20` — authored pairs `15/36` (font00, guide, quest, tutorial, monster, expand), `25/48` (`fontex_subtitle`), `20/20` (venus, square, stf), `40/40` (bookman). Written by the ctor, **read by nothing in the shipped image** — see the 2026-09-27 census below; the consistent line-metric shape is a legacy-format field, not live TZA semantics |
| `+0x28..` | `0x24` × N | records: `{u32 key; 0x20-byte payload}` |

**Glyph record (`0x24` B, corpus-decoded 2026-09-26e):** `{u32 key;
u32 utf8; u32 tileY; u32 0; u32 cellW; u32 cellH; u32 advA; u32 advB;
i32 kernCp}`. `utf8` is the glyph's UTF-8 bytes packed little-endian
(`困` U+56F0 → `E5 9B B0`; `≦` U+2266 → `E2 89 A6`; ASCII `'0'` →
`0x30`) — the record's human-readable name, and the reason
`font00`'s index-keyed map can still say which character each index
is. `tileY` walks `0, cellH, 2·cellH, …` down a
`floor(2048/cellH)`-row column then wraps — records tile the atlas
**column-major** in file order (the X is `column × cellW`, implicit
in sequence). **`advA` and `advB` are byte-identical in every record
corpus-wide** (21,269 records, zero diffs — a duplicated per-glyph
**advance**: 36/36 font00, 22/22 bookman, 20/20 venus). The renderer
reads payload `+0x1C` (`advB`) through `0017F9C0` → `001E9BD0` =
`trunc(advance / fontScale)` (`fontScale` = `record+0x34`, read back
by `001FDDB0`) and adds it to the pen. The trailing word is the
glyph's **kern codepoint**: `−1` = not kerned, else the glyph's own
codepoint (69/69 `kernCp` == `utf8` cp on `us/font_stf_a`; every
non-`−1` value corpus-wide is an ASCII/Latin cp — `A`–`Z`, `a`–`z`,
digits, accented Latin `0xC0`–`0xFC`, `0x2014`, `0x201C`/`0x201D`).
It is populated **exactly in the fonts whose flags bit 0 requests
`.ker`** (six stf, venus, square, `kr/font00`, `kr/fontex_subtitle`,
`us/fontex_subtitle`; every flags-bit0-clear `.dat` has all-`−1` —
sole exception the orphaned `us/fontex_expand`). The walker compares
payload `+0x20` against `−1` at `002AC527` and calls `0017F8E0` —
`trunc(001E9780 / fontScale)` — only for kerned glyphs. |

**The record (`001FC060`, 0x120 B).** The ctor maps the header onto the
record verbatim — `+0x00` fileId, `+0x18` capacity, `+0x1C`/`+0x20`
/`+0x24`/`+0x28`/`+0x2C`/`+0x30` ← header `+0x20`/`+0x24`/`+0x08`/`+0x0C`
/`+0x10`/`+0x14`, `+0x34` float — then builds **three EASTL maps**
(`+0x38` = the glyph-record map, `+0x70` = the `.ker` pair map §3 names,
`+0xA8` = `mapA8` the event→cp-vector map) and two EASTL strings
(`+0xE0`, `+0x100`). The six formerly-spare header words are now
corpus-named in the header table above: atlas width, tile extent,
cell W/H, and the line-metric pair.

**The flag arms (`001B5750`/`001B5480`)** are identical twins: walk
`lib+0x30[fileId]` (the just-filed record must exist), allocate a
registration node from `lib+0xD0` (`001BA860`; the node gets the
record's name copied via `001A5760` and `node+0x30 = fileId`), mint a
type-4 request `{+0:type=4; +8:completion; +0x10:node; +0x20:name[0x100]}` and queue it via `001A0BB0`. The two differ only in the
completion callback (`001B6080` vs `001B6030`) and the extension tag
appended to the font's base name by `001B31E0` — `.data` slot
`01DF6E10` → `".ker"`, `01DF6E18` → `".fex"`. (`001B4D70` itself
pre-formats the three sibling names `.dds.phyre` / `_shadow.dds.phyre`
/ `.dat` from `01DF6DF8`/`01DF6E00`/`01DF6E08` for the path build.)
So the `.dat`→`.fex` binding is **authored in the `.dat` flags word**,
and the request rides the font's own record as anchor.

Each record is filed by `001FDCC0` into the `r15+0x40` map keyed by
`rec[0]`; `001FDEC0` returns `node+0x24` — a pointer to the **32-byte
payload** (the glyph record; `rbx+0x1C` = payload `+0x1C` is the advance
word read through `0017F9C0`). `001B4D70` then calls
`001B58E0(lib, fileId)` to mint the font's session, and files the
record under fileId via `0020B5F0(lib+0x28, &fileId)` → `[slot] = r14`
(the `lib+0x28` fileId→record map).

**Key space** — the two record families share one find (`001FDEC0`), and
the bound *session's fileId* picks the r15 (and therefore the map).
`font00.dat` records are keyed by **compiled index** (the verified
record-order decode — normal arm, `ctx+8 = NULL`, raw `esi`; keys
0..`glyphCount`). The
`.fex` section stores raw cps into `mapA8[eventKey]` (`001B4C00`:
`{u32 eventKey; u32 count; u32 cps[count]}*` chunks, `001FDB90`
find-or-create + `001FDB50` push, no translation), and `001FDCC0` has
exactly one caller (`001B4D70`) — the `.fex` path never touches
`r15+0x40`. So the event-bound session's `ctx+8[esi]` = cp keys
the *bound fileId's* `.dat` map — **the fontex font's `.dat`
records are cp-keyed, now corpus-measured** (2026-09-26e): every cp in
every listed `.fex` chunk lands on a sibling `.dat` record key —
jp/kr/ch/cn `fontex_expand` + `fontex_subtitle`, **56,451 of 56,451
cps (100%)**, and the fontex `.dat` key ranges are real codepoint
runs (jp expand `U+2015`–`U+FF5E`, subtitle `U+0021`–`U+FF1F`). The
`.dat` key space is per-font: index-keyed for `font00`,
codepoint-keyed for the fontex fonts.

**`00332250(kind, id, sel, flag)` mechanics** (2026-09-26): `kind`
chooses how much of the `002DF980` canonical path the hash sees.
`002DF980` resolves `g_pathTables@0x215F000[kind][id]` — strings of
the form **`PS2Data\plan_master\<loc>\event\<dir>\<name>\<name>.<ext>`**
(6 separators, `.rdata` literals). The backward-separator scan cuts
`path[r10+1 .. r9-1]` where `r9` = `edi`-th and `r10` = `edi+3`-th
separator *from the end*: kinds 8/0x25 (`edi=1`) drop the filename and
the `PS2Data\plan_master\<loc>` prefix → **`event\<dir>\<name>`** —
the verified `.fex` chunk key; kind 5 (`edi=2`) keeps the directory
level → **`<loc>\event\<dir>`** — a locale-qualified *directory*-level
binding key (no filename). Other kinds never reach the queue.
`sel` = caller's
composite and `flag` = a byte, passed verbatim through
`0017FA90(ecx→edx, dl→r8d, path→r9)` into `001B6350`; `arg4 = 0`.
The two feeders: `00330310` (`ActorResource_BeginPrimaryPayloadLoad`)
files with **flag = 1**, `sel = r15d|r14d` (resource handle |
slot index); `003306E0` (the big section-registration body) files
with **flag = 0**, `sel = r8d|eax` — and `flag = 0` is exactly what
`001B47A0`'s drain scans for (`+0x10 == 0`), so the `003306E0`
queueing is the drainable pending-bind while `00330310`'s sits
flagged non-drainable until `001B5330`/`001E9A30` clears it.

**Drain mechanics (`001B47A0` → `001B4590`, 2026-09-26d).** The queue
descriptor is `{u8 inuse@0x00; u32 selTag@0x04; u8 flag@0x10;
u32 eventKey@0x14; u32 memberIdx@0x18}` — `001B6350` dedups on
`(selTag, flag)`; `001B47A0`'s drain scan matches `desc+4 == sel`
AND `desc+0x10 == 0` (so `flag` = drainability, and the `ptr|idx`
composite seen at `00330310` is only a **dedup identity tag**, never
a session key). `001B4590(lib, desc)` files the desc into
`lib+0x278[slot]` (16 slots; the slot index `ebx` becomes the session's
`sel` — so `001E9D20`'s `{eax,plane}` lookup keys sessions by
**descriptor slot**, which is the byte the text runs carry at
`[rdi+0xA6]`-family fields). Then, keyed on `lib`'s own dword
(`fontSetBase`):

| `desc` state | fileId | plane | eventKey |
|---|---|---|---|
| `+0x00 == 0` | `desc+0x18` raw | 0 | 0 (default/clear bind) |
| `+0x18 == 0` | `fontSetBase*32 + 2` **and** `+ 3` | 0 / 1 | `desc+0x14` |
| `+0x18 != 0` | `fontSetBase*32 + desc+0x18` | 0 | `desc+0x14` |

So font fileIds are `fontSetBase*32 + member` composites (32 members
per set; 2/3 are the primary pair, `memberIdx` overrides member 2 on
plane 0), and **every event-bound descriptor binds two sessions** —
primary on plane 0, the `+3` sibling font on plane 1 — each gated by
`mapA8[eventKey]` existing in *that* member's `.fex` map (`001FDD60`
check per member). `001E7F90` then files `{slot, fileIdComp, eventKey,
plane}` into `ctx+0xF38` keyed `(plane<<32)|slot` — `001FDF70(rec)`
produces `fileIdComp`. The writer of the `fontSetBase` dword (`lib+0`)
is closed as **never-written** (2026-09-26e): zero hits on direct
`[0x1F81200]` stores, `[rax+0]` writes through getter `001B5FB0`, and
rip-load→offset-0-write scans; the corpus agrees — authored fileIds are
`1`–`22` across all five locales, all members of **set 0**, so
`fontSetBase` is the ctor-zero the constructor leaves and the `*32`
composite degenerates to the authored member id. (`fontlist.ah`
files the members: jp lists `fontex_expand`, `fontex_subtitle`,
`font00`, `font_bookman`, `font_iwa_g12`, `font_venus`, `font_square`,
`fontguide`, `fonttutorial`, `fontquest`, `fontmonster`,
`font_stf_{a,as,b,bs,c,cs}` — ids 2,3,1,13,14,11,15,4,5,6,7,17–22.)

### SWE2-DATA update (2026-09-27) — the header metric pair is dead-authored; the fontclut table is colour, not metrics

The `.dat` header `+0x20`/`+0x24` pair lands at font-record `+0x1C`/`+0x20`
in the `001FC060` ctor. **No code in the shipped image reads those two
record fields.** The accessor domain is closed:

- The record is created only by `001FC060` (called only by the `.dat`
  binder `001B4D70`) and stored only in the `lib+0x30` fileId map
  (retriever `001B51C0` — all five callers verified: `001E9D20`,
  `001E93C0`, `001E9450`, `001E9580`, `001E9610`) and the bound `[ctx]`
  slot (readers `001E9BD0` → `+0x34` fontScale; `001E8070` → `+0x24`/`+0x28`;
  the glyph and `.ker` paths → the `+0x40`/`+0x70`/`+0xA8` maps).
- Every verified reader reaches record fields only through the getter set
  `{+0x08` (`006B5C70`), `+0x10` (`005C5310`), `+0x24` (`00225690` — atlas
  width), `+0x28` (`0079E3C0` — tile extent), `+0x2C` (`00225670` — cellW),
  `+0x30` (`0079CFA0` — cellH), `+0x34` (`001FDDB0` — fontScale)`} plus the
  three maps. `001FDDC0`, a `+0x1C` getter, has exactly three callers —
  `0046B690`, `0046B870`, `0046BAC0` — and all three pass a different
  record type (they test flag bits `al & 4`, `[rdi+0xE] & 0x40`, not a
  metric). `001F49E0`, a `+0x20` dword getter, has **zero callers**;
  `00802900`, the other `+0x20` dword getter, is called only outside the
  font family (`00679BF0`/`0067A480`).
- An operand-level sweep of the font families (`0x1B`/`0x1E`/`0x17F`/
  `0x2AC`/`0x366` ranges) for `[reg+0x1C]`/`[reg+0x20]` reads finds only
  qword internals of maps/strings and other record types (the `0x58`-stride
  clut slots, the blob section header at `001B4D70`+`0x1C` = the flag
  word, the 0x24-byte glyph payload's own `+0x1C`/`+0x20`). Positive
  control: the same sweep finds the live consumers of `+0x24`/`+0x28`/
  `+0x2C`/`+0x30`/`+0x34`, so the instrument detects these reads when they
  exist.

**Consequence:** the `15/36`, `25/48`, `20/20`, `40/40` pairs are a
legacy-format field carried verbatim — their names cannot be established
from TZA code because TZA never consumes them (the same vestigial pattern
as the structurally unreachable `.ker` pairs and the orphaned us `.fex`
files). They remain useful corpus provenance — the authored values still
correlate with cell height — but no semantic role may be claimed.

**The `fontclut` table is a colour table, not a metric table.** `001E8070`,
which at first read looks like a line-layout consumer of `rec+0x1C`/`+0x20`,
actually indexes a different 0x24-byte record family: 28 slots at
`ctx+0xF68` (accessor `001E94E0`, bulk init `001E98A0`, ctor defaults
`{inited=0; -1,-1,-1,128; -1,-1,-1,128}` written by `001E71B0`). `001C76E0`
populates each slot from named config members — `+0x04..+0x10` =
`mShadowRed/Green/Blue/Alpha`, `+0x14..+0x20` = `mFontRed/Green/Blue/Alpha`,
selected by `mClutIndex` (`01F81378`). `001E8070(ctx, quadSpec)` picks the
slot by `[param+0x9c] mod 28` (default record `ctx+0x1358` when negative),
converts each channel with `cvtsi2ss`, normalizes colour by `÷255` and the
two alpha/scale words by `×1/128` (`xmm9 = 255.0`, `xmm8 = 0.0078125`), and
emits 0x3C-byte `{f4; f4; f4; f2; u32}` records into the `[ctx+0x10]` queue
— shadow RGBA + font RGBA styling for glyph quads. On the bound font
record itself it reads only `+0x24` (atlas width) and `+0x28` (tile
extent) for UV normalization — the first confirmed live consumers of
those two header fields.

**The `us/fontex_expand.dat` anomaly is an older serialization, not a
metric outlier.** The file is a `0x20`-byte header (8 words — it simply
has no `+0x20`/`+0x24` pair) followed by 810 standard `0x24`-byte
records (810 × 0x24 + 0x20 = 29,192 B exactly, matching capacity
`0x32A`). What the earlier header scan reported as `+0x20 = 22256`,
`+0x24 = 11574245` is record[0]'s `{key = U+56F0; utf8 = E5 9B B0 = 困}`.
The records are real-cp-keyed like the jp fontex fonts. It stays
orphaned: `us/fontlist.ah` never lists it, and even if it were requested
the loader would mis-slice it (records read at `+0x28` fall 8 bytes into
record 0) — moot in both directions since the metric fields are
dead-authored anyway.

**Residual (2026-09-27):** the `sel` composite is resolved (dedup tag
only — the session key is the `lib+0x278` descriptor slot). The
`esi ≥ 0x7E0` and
`ctx+8`-binding questions are **resolved** (above): `002AB7D0` writes the
mode flag and bound together — CJK languages {7,8,0xB} raise the bound to
`0x1C`, making `18`–`1B` ordinary font planes (`esi` `0x7E0`–`0xA80`) and
moving event expansion to `1C`–`1F`; `eventKey = 0` default sessions bind
`ctx+8 = NULL` (`mapA8[0]` can never exist), so ordinary text keys
`r15+0x40` raw by compiled index and only validated event-bound sessions
remap through the `.fex` vector. The `.dat` header and record
payloads are corpus-decoded (§above): the header words are the atlas
width, tile extent, cell W/H and scale (live), plus the `+0x20`/`+0x24`
pair — now closed as **dead-authored** (census above). The flag
sub-handlers are resolved —
`001B5750` = the `.ker` requester, `001B5480` = the `.fex` requester,
both keyed off the just-filed record. `fontSetBase` (`lib+0`) is closed
as never-written — all shipped fileIds are members of set 0.

## 8. Related

- [The `.ah` manifests](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ah-asset-header-manifests.md) — `fontlist.ah` among the five builders.
- [The text control-code language](the-text-control-code-language.md) — how game text is walked.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Audio — CLIENT, 13 edges, and the crossing is a shared container helper rather than a
  relationship.** Thirteen Audio bodies call `0016D6D0`, which this page names only to correct its
  label (§4, `CON-121`): it is the EASTL red-black-tree **iterator step**, 68 bytes with zero
  stores. Worked example, body read: `002187D0` (161 B, `PrimaryOwner.Audio`) operates on the
  ordered container at `[rdi+0x58]` through `00199DB0` and reaches the iterator step from there —
  an Audio object's own map, nothing font-related. **The direction is one-way**: every one of the
  thirteen edges is *inbound* to the helper, and no font function on this page calls into Audio.
- **Platform — CLIENT, 2 edges.** Two `Platform.Windows.NativeSupport` bodies call the same
  helper: `0019CC50` (232 B) and `001B1960` (182 B). Same shape, same direction, same reason.

> **These two crossings are OPUS's own doing, and are recorded rather than quietly cleared.**
> The warning at §4 — that citing an address inherits its whole caller set as neighbours —
> was written here to justify *not* citing the erase `0016DA60`. Citing `0016D6D0` in the same
> correction had exactly the effect that warning describes, and raised these two findings against
> subsystems this page has no relationship with. The citation is load-bearing: the correction
> cannot say what `0016D6D0` is without naming it. So the crossings are accounted here instead,
> and `the-ordered-container-runtime.md` carries the family itself.

- **Resource — CLIENT and SERVICE, 19 edges.** Cited font functions are called by Resource bodies (970 bytes 4 times, 72 bytes 3 times, and 119 bytes). They call Resource helpers of 8 to 399 bytes.

- **CoreRuntimeScheduling — CLIENT.** `0017D6E0`, owned by that layer — the per-frame pump — calls
  `001A1220`, the fontlist-load body this page names (`fontlist.a` via IAT `008C3038`). The scheduler
  drives the load during its own frame work; consultation, not shared ownership. Read from
  `edges.tsv` 2026-09-17 (SWE2-FRONTIER).
- **Input - CLIENT and SERVICE (10 edges).** `00263FF0`, ActorManager_GetRecordByOrdinal (`00358940`), `005CD4F0`, `005CD820` are called by bodies filed to Input: `00226BE0`, `002E09A0`, `0079C140`, `007A0340`; `0017D4C0`, `0079C140` reach bodies filed to Input: InputManager_CreateSingleton (`00198750`), `0079D010`, `0079D920` - shared machinery across the layer boundary, no shared ownership.
- **Rewards_Progression_Economy - CLIENT (1 edge).** `00229E40` is called by bodies filed to Rewards_Progression_Economy: EnemyChain_UpdateOnDefeat (`00317ED0`) - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT (39 edges).** `00229E40`, `00263FF0`, ActorManager_GetRecordByOrdinal (`00358940`) are called by bodies filed to Script_VM_Native_Bridge: WorldActorScriptVM_InterpretBytecode (`0025E4C0`), VMNativeCommand_ExecuteLifecycle (`002621D0`), ScriptVM_WaitList_HasAnyActorChannelActive (`00267420`), ScriptVM_WaitList_HasAnyActorResourceEntryActive (`002674B0`) (+35 more) - shared machinery across the layer boundary, no shared ownership.
- **WorldAreaField - CLIENT (2 edges).** `002DF980`, ActorResource_BeginManagerResourceSetLoad (`0032FCA0`) are called by bodies filed to WorldAreaField: WorldSimulation_ProcessDeferredModeRequest (`0032FC30`), `00379A10` - shared machinery across the layer boundary, no shared ownership.
- **CombatAction - CLIENT (3 edges).** combat-action bodies call this page's subjects: `BattleAction_InitializeGlobalSpecialSequenceMode` (`00306BD0`) calls `0032FC30`, `BattleTarget_ClassifyRelationshipClass` (`0030AB40`) calls `ActorRuntime_GetClassNibble` (`00263C20`), and `00313DB0` calls `00226BE0`.
- **Movement - CLIENT (9 edges).** movement-layer bodies call this page's subjects: `WorldActor_UpdateRuntimeAndScriptExecutionState` (`0025DF00`) calls `WorldActorScriptVM_InterpretBytecode` (`0025E4C0`), `PartyFollow_SolveFormation` (`00338490`) calls `00263C20`, and six more callers reach `00226BE0`/`00263C20`/`00263FF0`.
- **Party - SERVICE (2 edges).** `00226BE0` reaches `PartyRoster_GetActorBySlot` (`00263750`) and `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) - party-table lookups behind the formatting path.
- **CombatAI - MECHANICAL (2 edges).** both edges are combat-AI bodies (`AiOrder_EvaluateTargetSelector` `00301AD0`, `BattleTarget_MatchesRelationMode` `0030BD00`) calling `BattleTarget_ClassifyRelationshipClass` (`0030AB40`) - fan-in on one relationship-class query.
- **Gameplay - MECHANICAL and SERVICE (5 edges).** four gameplay bodies (`0030B050`, `0030BB30`, `0030C210`, `0031ADB0`) call the shared queries `BattleTarget_ClassifyRelationshipClass` (`0030AB40`) and `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) - accessor fan-in; `00313DB0` also reaches `BattleRuntime_GetMode0To5FromFlagsAndFieldBit15` (`0030D9A0`).

## The `001B44A0` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

`001B44A0` (236 B) is the language → font-list selector §88 documents. After
the path pair lands at `01DF6DE8`/`01DF6DF0` (`001B44C8`–`001B453D`), it calls
`001E9F30` on the `[01F811F8]` object (`001B4544`), `001B53F0` (`001B454C`)
loads the list, seeds `+0x2F8`/`+0x300`/`+0x308` from `01E0CF90`/`01E0CF94`/
`01DF6DE0` (`001B4551`–`001B4574`), and tail-calls `001E98A0` (`001B4587`).

| member | role | interior |
| --- | --- | --- |
| `001B53F0` (134 B) | the list loader — `001A1220`/`001A0A90`, IAT call `008C3038` with `r8 = [01DF6DE8]` (the chosen `fontlist.ah`), `[01F81208]` check, `0016D6A0`, `001A1220`, tail `001A0BB0` (`001B5434`–`001B5471`) | [`001B5434`](../../_index/ADDRESS-INDEX.md) |
| `001E98A0` (126 B) | the fontclut slot initializer — names all 28 `ctx+0xF68` colour slots `fontclut_%d`, `ebx` clamped at `0x1B`/`0x1C` (27/28), `0019C5D0`, `001C5F20` (`001E98C2`–`001E9901`) | [`001E98C2`](../../_index/ADDRESS-INDEX.md) |
| `001E9F30` (7 B) | one-byte setter — `[rcx + 0x2378] = dl` | [`001E9F30`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001A1220`, `001A0A90`, `001A0BB0`,
`0016D6A0`, `0019C5D0`, `001C5F20`, `008C3038` (IAT), `00808C40`.

## The `001FDB90` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`001FDB90(font, key, count)` — the `.fex` entry create — is an
ordered-map lower_bound + insert: walks `rax = [r10+0x18]` via
`[rax+8]` links comparing `dword[+0x20]` against `edx` (`001FDBC0`–
`001FDBCE`), refuses the duplicate when `rcx == r9` (`001FDBD6`),
inserts through `001FC640` + member `001FDF90` (`001FDBF8`/
`001FDC02`), and the second arm repeats the walk off `001FC420`
(`001FDC2D`) ending in `dword[rcx+0x24] = edi` — the value store
(`001FDC66`).

| member | role | interior |
| --- | --- | --- |
| `001FD780` (540 B) | the ordered-map insert machinery — `rsi = [rcx+8]` head, `rax = [rcx+0x10]` end (`001FD79E`/`001FD7A5`) | [`001FD7A5`](../../_index/ADDRESS-INDEX.md) |
| `001FDF90` (137 B) | keyed node accessor — `rdi = [rcx+8]` walk, `edx` compare (`001FDF9A`/`001FDFAE`), `dword[rsp+0x38] = 0` init (`001FDFB4`) | [`001FDFAE`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001FC640`, `001FC420`. The
duplicate-key refusal at `001FDBD6`/`001FDBE3` is what makes the
`.fex` walk stop at `001B4CBA` on the caller page.

## The `001B4C00` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`001B4C00` (~360 B) — `rdx` null-gated table walk: reads
`qword[rcx+0x40]`/`[rdx+0x30]` against the `+0x30` sub-table
(`001B4C10`/`001B4C1B`).

| member | role | interior |
| --- | --- | --- |
| `001FDB50` | `+0xA8` map lookup — `001FC640(rcx+0xA8, &out)` then deref (`001FDB5E`/`001FDB70`) | [`001FDB70`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `001FC640`.

## Interior citation — frontier hub `001A4BF0` (2026-09-17, SWE2-EC7)

`001A4BF0` — 155 B, 27 frontier callers at census; the assign-or-grow this page's temporary
strings are built through (`001EDF00` + `001A4BF0`). Interior verified: when the
`r8d - edx + 1` span exceeds 1 it allocates via the `+0x18`-slot object's `vtable[+0x10]` virtual
([`001A4C24`](../../_index/ADDRESS-INDEX.md)) and writes the `{begin,end,cap}` triple at `rdi`;
otherwise it seeds the triple from the static empty buffer at `02EBA2E0`. Then
`call [rip+0x71DDD8]` — the indirect copy through the pointer at `008C2A40` — copies the
`[rdx,r8)` source and `byte [end] = 0`
terminates. This is the grow path of the assign pair `001FE020`/`001FE080` describe from the store
side.

NOT claimed: which allocator object supplies `+0x18`'s vtable, or the source encoding.

## Interior citation — frontier hubs `001A0A90`, `001A0BB0` (2026-09-18, SWE2-EC7)

`001A0A90` — 93 B, 9 A-measured callers; the locked accessor the list loader runs before its
tail push. Interior verified: `005CD4F0(&[rcx+0x178])` takes the record's lock
(`001A0AB6`), `001BA860(rcx+0xB8)` resolves the container slot at [`001A0AC3`](../../_index/ADDRESS-INDEX.md),
`[result+0x128]` is zeroed (`001A0AD6`), `005CD820` releases at `001A0AD9`, and the slot
pointer is returned. The `qword[rsp+0x20] = -2` guard word is the SEH-scope cookie the CRT
emits around the locked region.

`001A0BB0` — 160 B, 8 callers; the locked intrusive push the loader tail-calls. Interior
verified: when `[rdx]` is non-zero, `r8b` non-zero routes to the immediate variant
`001A07B0` (`001A0BDE`); otherwise `005CD4F0` locks `[rcx+0x28]` (`001A0BF1`), the
allocator at `[+0x60]` is vcall-`+0x10`'d for a `0x18`-byte node (`001A0C09`), `[node+0x10]`
receives `rdx`, the node is spliced after `[+0x50]`'s `+8` link at `001A0C18`–`001A0C2A`,
`[+0x68]` is cleared ([`001A0C2E`](../../_index/ADDRESS-INDEX.md)), and `005CD820` unlocks. Deferred-call queue
insert — same lock/unlock pair as `001A0A90`.
The `005CD4F0`/`005CD820` pair is the shared CRT-region lock — Input's `0079C140` and
`007A0340` run the same acquire/release on their own objects (mechanical, not a font
relationship).

### Interior citation — frontier hub 001FBEF0 (2026-09-18, SWE2-EC7)

**001FBEF0** (138 B, 4 A-measured callers) — the kerning table's list-reparent helper. Handles the empty-chain init (`rax==0` → `+0x58` head written twice) and the non-empty splice: walks `[r9]`'s `+0x58` chain, relocates `rsi`'s node pointer at `+0x40` if it still points at the old head, then `001FC770(rcx)` — the sibling list op in the same family — and zeroes the link at `[r9+0x18]`. This is the companion of the kern-pair insertion: that one links a node in, this one re-homes the chain when the head changes. In-scope: head-init store [`001FBEF6`](../../_index/ADDRESS-INDEX.md); `001FC770` call [`001FBF53`](../../_index/ADDRESS-INDEX.md) — 4 callers, all A.

## SWE2-EC7-35 update (2026-09-19) - `001B4930`

`001B4930` (713 B) is a font/string expansion body - `01F81208`/`02EBA2E0`/`02EBA2E1`/`008F4438`, `001EDF00`/`00861EC0` plus `00808C40`/`00210EB0`/`001AB6B0`/`0019C5D0`/`0018A330`. Interior anchor `001B4986` (an `001EDF00` call).

## SWE2-EC7-42 update (2026-09-19) - `001FC640`

`001FC640` (303 B) is a font-data body - `"EASTL vector"`, `008C5F58`, `001EDF00`/`001FBFC0`/`001FD310`. Interior anchor `001FC6B9` (an `001EDF00` call).

## SWE2-EC7-44 update (2026-09-19) - `001FC770`

`001FC770` (274 B) is a vtable row body - two `call [rax+0x10]` vcalls. Interior anchor `001FC79E` (the first vcall).

Corrected 2026-09-27 (FABLE BQ-23 tier-6b, `FABLE-REQ-SWE2EC7-BQ23-RELABEL-AND-TWO-NOTES`): the earlier "no direct calls" claim was wrong - `001FC770` calls itself (`call 0x1fc770`). It is EASTL `rbtree::DoCopySubtree`: allocates through the tree's `[rax+0x10]` slot vcall (or DoCreateNode `001FFAB0`), copies the parent and the colour byte `+0x18` (`movzx ecx, byte ptr [rdi+0x18]` -> `mov byte ptr [rbp+0x18], cl`), recurses on the source's `[+0]` and walks its `[+8]`; sibling `001FF990` is the same routine for another instantiation. Label now `GFZ.V121.CodeDomain.EASTL.OrderedContainerRuntime.TreeClone`.

## SWE2-EC7-50 update (2026-09-19) - `001B1960`

`001B1960` (182 B) is the shared 182-B helper - `0016D6D0`/`0016DA60`/`001B1440`/`001FB660`/`002124C0` plus a `call [rax+0x18]` vcall. Interior anchor `001B196D` (an `0016D6D0` call).

## SWE2-EC7-53 update (2026-09-19) - `001AB6B0`

`001AB6B0` (484 B) is a `0x20`-stride vector element-move helper shared by the font/string bodies - begin/end `[rcx+8]`/`[rcx+0x10]`, `001A5760`/`001AA570`/`001AA7D0` plus three vcalls. Interior anchor `001AB708` (a `001AA7D0` call).


## SWE2-EC7-53 update (2026-09-19) - `001FD310`

`001FD310` (406 B) is a font-data body - `0016D6D0`/`0016D840`/`001FBFC0`/`001FD190`/`001FD6C0` plus two vcalls. Interior anchor `001FD357` (a `0016D6D0` call).

## SWE2-EC7-54 update (2026-09-19) - `001FD190`

`001FD190` (383 B) is a font-data body - `0016D720`/`0016D840`/`001FBFC0` plus two vcalls. Interior anchor `001FD202` (a `0016D720` call).

## SWE2-EC7-57 update (2026-09-19) - `001FB660`

`001FB660` (188 B) is the shared 182-B helper's sibling - `0016D6D0`/`00183720`/`001AF2B0` plus one vcall. Interior anchor `001FB67A` (a `00183720` call).


## SWE2-EC7-57 update (2026-09-19) - `001AA570`

`001AA570` (178 B) is a font-data body - `001EDF00` single call. Interior anchor `001AA5C5` (a `001EDF00` call).


## SWE2-EC7-57 update (2026-09-19) - `001FD6C0`

`001FD6C0` (177 B) is a font-data body - `0016D840`/`001FBFC0` plus one vcall. Interior anchor `001FD73F` (a `001FBFC0` call).

## SWE2-EC7-59 update (2026-09-19) - `001B1440`

`001B1440` (159 B) is the shared helper the font page names - `0019C5D0`/`00674A00`/`00808C40` plus `008F80C8`/`01DF1B90`/`01DF1BA0`/`01F44830` and the `"%s%s%s"` literal. Interior anchor `001B1482` (a `0019C5D0` call).

## SWE2-EC7-60 update (2026-09-19) - `001FBFC0`

`001FBFC0` (155 B) is a font-data body - `001EDF00` single call plus two vcalls, `008C2A40`. Interior anchor `001FBFEE` (a `001EDF00` call).

