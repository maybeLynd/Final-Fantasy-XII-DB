---
system: skeletonmapping.bin and highmodelreplace.bin — the add-motion folder's two boot-loaded tables
category: 17-Presentation-Rendering
status: AUDITED
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 14 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "2 of 2 files, both walked to their exact size by their loaders' rules, 2026-09-13"
container_format: "add-motion skeletonmapping / highmodelreplace"
last_reviewed: 2026-09-13
archive_formats:
  - "skeletonmapping | explained | skeletonmapping.bin (.bin member): count + 32-byte-name records - AddMotion_LoadSkeletonMapping 0036FFF0 parses into 02AD9E30 / 02AD9E38, section 3"
  - "highmodelreplace | explained | highmodelreplace.bin (.bin member): {a, b, c, pairs} records - AddMotion_LoadHighModelReplace 0037CCC0 parses into 02ADD940 / 02ADD938, section 3"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-add-motion-bin-tables-pass-1 - both files re-walked from the archive and every figure exact, including 540 = 22x12 + 23x8 + 22x4 + 4; NEW: 23/23 replacements keep the family letter and flip its case while 0/23 keep the number; and the VBF index is entirely lower-cased (0 of 89,414 entries), so no name-case question can be asked of it
  crossref_clean: false
  reopened_count: 0
---

# `skeletonmapping.bin` and `highmodelreplace.bin`

> Two small `.bin` files beside the [`.adm` tables](adm-add-motion-tables.md), each loaded once at start-up by
> its own reader. **`skeletonmapping.bin`** is a named list of per-joint indices, matched by model name when a
> model's pose record is set up. **`highmodelreplace.bin`** is a list of model ids, each with a replacement id
> chosen by the story-progress variable. Both are read onto the stack whole and trusted.

**Corpus validation.**

| | |
|---|---|
| files | **2 of 2** (the other `.bin` families are covered elsewhere or not yet) |
| `skeletonmapping.bin` | 196 bytes; **1 record**, name `hc1006_03`, 39 values (`-1` ×21, **`27`×3, `28`×3, `29`×3, `30`×1** — the multiplicities, §9 — `33` ×8); the walk ends exactly at the file size |
| `highmodelreplace.bin` | 540 bytes; **22 records**, 21 with one pair and 1 with two, never more than the four slots the parsed record holds; the walk through the closing `-1` ends exactly at the file size; the `(a, b, c)` keys are distinct |

Census: [`census.py`](../../_experiments/evidence/add-motion-bin-tables/census.py) →
[`census.out.txt`](../../_experiments/evidence/add-motion-bin-tables/census.out.txt).

---

## 1. What the player sees

**A model that changes as the story advances, and one model's joint remapping.** `highmodelreplace.bin` maps 22
model ids to replacement ids, with a story-progress threshold per replacement — one entry switches at progress
1570. `skeletonmapping.bin` gives the high-detail model `hc1006_03` a 39-slot joint index list. ~~Which models these~~
~~are on screen is not established here~~ *(answered: see §7, HM-1 2026-09-27 - the ids name a model's own high-detail variants; `hc1006_03` is `c1006`'s replacement body; 2026-10-02, OPUS)* (§7).

## 2. The layout

```struct SkeletonMappingHeader base=file size=0x04
+0x00  i32       count        1 in the shipped file
```

```struct SkeletonMappingRecord base=record size=0x24
+0x00  char[32]  name         model name, NUL-padded (hc1006_03)
+0x20  i32       n            number of i32 values that follow (39)
```

followed by `n` `i32` values, then the next record.

`highmodelreplace.bin` is a stream of records ended by a leading `-1`:

```struct HighModelReplaceRecordHead base=record size=0x0C
+0x00  i32       modelId      high word 99 / 110 / 115 in 14 / 6 / 2 records (ASCII c / n / s), low word a number
+0x04  i32       keyB         -1 in 18, 1 in 4; -1 matches any
+0x08  i32       keyC         -1 in 18, 0 in 4; -1 matches any
```

```struct HighModelReplacePair base=record size=0x08
+0x00  i32       replacement  high word 67 / 78 / 83 (ASCII C / N / S)
+0x04  i32       minProgress  0 in 22 pairs, 1570 in one
```

Pairs repeat until an `i32 -1`; the record list ends with a further `-1`.

## 3. The loader contract

**Both loaders** (`AddMotion_LoadSkeletonMapping` `0036FFF0`, `AddMotion_LoadHighModelReplace` `0037CCC0`, called
from `0022A0B0` at `0022A442` / `0022A43D`) open their fixed path with `001D6F20(path, 1)`, take the size, **allocate
`size + 1` rounded up to 16 bytes on the stack with `_alloca`** (`0037003C`–`00370061`, `0037CD08`–`0037CD29`), read the
whole file into it, close it, and parse from the stack copy. A zero size skips parsing. There is no upper bound on
the size before the stack allocation.

**`skeletonmapping.bin`** (`00370077`–`0037014B`): `count` goes to `02AD9E38`; an array of `count × 0x30` bytes is
allocated to `02AD9E30`; per record the 32 name bytes are copied (`003700D7`), `n` is stored at `+0x20`, an array of
`n × 4` bytes at `+0x28` receives the values. No check that the counts fit the file.

**`highmodelreplace.bin`** (`0037CD44`–`0037CE49`): a first pass counts records (`0037CD49`–`0037CD72`), then an array of
`count × 0x30` bytes (zeroed) goes to `02ADD940` and the count to `02ADD938`. Per record: `a`, `b`, `c` at `+0x00`,
`+0x04`, `+0x08`; each pair's replacement at `+0x10 + 4i` and threshold at `+0x20 + 4i`; the pair count at `+0x0C`.
**Nothing limits the pairs to four**, so a fifth pair would write past the record's `+0x30` into the next one.

**Consumers.**

- `00372820` (the pose-record setup, from `0046E4D0`) copies a 32-byte model name to the record's `+0x20` and scans
  every mapping record with a byte-wise string compare, storing the **last** matching index at `+0xB0` (`-1` when
  none, `003728A8`–`0037290B`). `Skeleton_UpdateFinalPoseAndCombatLook` (`003703A0`) later indexes `02AD9E30` by that
  field (`0037065D`–`00370673`).
- `0037CB90(modelId, b, c)` returns `-1` unless the byte `01E02800` is set (it is 1 in the image and has no RIP
  writer) and a table is loaded. It takes the **first** record whose `modelId` equals the argument and whose `b` and
  `c` each equal the argument or are `-1`, then walks that record's pairs and returns the replacement of the last
  pair whose threshold is `<=` the signed story-progress word `FieldData_GetVariable0` (`00265270`); `-1` if none
  (`0037CBC6`–`0037CC93`). Its callers are `003409F0`, the `bindhoff` handler (`0x00D8`, `003460F0`) and
  `0037B4D0` — the last read 2026-09-17 (SWE2-FRONTIER): a 3,175-B per-tick evaluator,
  `0020E600` row-lookups ×20 over the `002EBxxx`/`0031Bxxx` helper band (`002EB7A0` ×13,
  `0031BEC0`/`002E9810` ×9 each), first call at [`0037B4F7`](../../_index/ADDRESS-INDEX.md).

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| file size | both loaders | 0 → nothing parsed | **no bound** before the stack allocation | — |
| mapping `count`, `n` | `0037007C`, `003700DD` | — | none; not checked against the file | — |
| mapping `name` | `003728E0` (compare) | — | a 32-byte copy; the compare stops at a NUL | — |
| replace pair list | `0037CE10`–`0037CE39` | — | **none: more than four pairs overruns the record** | — |
| replace `b`, `c` | `0037CC05`–`0037CC1A` | a value other than the argument and not `-1` | — | — |
| replace thresholds | `0037CC74` | — | signed compare with the progress word | — |

**The write path.** None.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0036FFF0` | `AddMotion_LoadSkeletonMapping` | ✅ full body |
| `0037CCC0` | `AddMotion_LoadHighModelReplace` | ◐ to the pair loop's end (`0037CE49`) |
| `0037CB90` | replacement lookup | ✅ full body |
| `00372820` | pose-record setup — the name match | ◐ `00372820`–`0037290D` |
| `003703A0` | `Skeleton_UpdateFinalPoseAndCombatLook` — the mapping read | ◐ `0037065D`–`00370673` |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `00D110A8` | `./PS2Data/add_motion/SkeletonMapping.bin` | `.rdata` | path |
| `00D11190` | `./PS2Data/add_motion/HighModelReplace.bin` | `.rdata` | path |
| `02AD9E30` / `02AD9E38` | mapping array / count | `.data` BSS | set by `0036FFF0` |
| `02ADD940` / `02ADD938` | replacement array / count | `.data` BSS | set by `0037CCC0` |
| `01E02800` | lookup enable byte | `.data` | 1; read only at `0037CB9F` |

## 5. Corpus survey

The single mapping record's values: indices 0–19 are `-1`, 20–29 hold `27 28 29 27 28 29 30 27 28 29`, 30 is `-1`,
31–38 are `33`. The 22 replacement records' model ids carry the high words 99 / 110 / 115 and their replacements
67 / 78 / 83 — the lower- and upper-case forms of the same three letters.

## 6. Falsification pass

**Run 2026-09-15 (OPUS).** The earlier census only replayed the parsers, so it could not fail. This
one transcribes the loader's own loops from `AddMotion_LoadHighModelReplace` (`0037CCC0`) and replays
them against the shipped bytes, which can.

**The replace record is variable-length and the loader proves it.** The counting loop at
`0037CD44`-`0037CD72` advances `0x0C`, and on a non-`-1` continuation scans forward in steps of `8`
before a final `+4`; the store loop at `0037CDA9`-`0037CE53` copies three dwords, does `rbx += 0x0C`,
then consumes `(dword, dword)` pairs until a `-1` and steps over it with `rbx += 4`. So a source
record is **12 + 8N + 4 bytes**, not a fixed stride.

> **Three fixed-stride readings were tried against these bytes first and all three are wrong** - 12,
> 20 and 24. Each one aligns for the first few records and then desynchronises, and a stride of 24
> produces a plausible-looking `(source, replacement)` pair per row for six rows before it drifts.
> That is the failure mode this page already warns about elsewhere: a wrong reading that yields
> readable output rather than garbage.

**Replaying the engine's counting loop gives exactly 22 records**, confirming §5's figure from the
engine rather than from a parser written to match it, and consuming **536 of 540 bytes** with the
remaining 4 being the closing `FFFFFFFF`.

**Every one of the 22 source ids is lower-case and every replacement is upper-case** - 22 lower, 0
upper, 0 neither - so the `c`/`n`/`s` against `C`/`N`/`S` split is a property of the *position*, not a
coincidence of the data: the record's own id is always the lower-case form and its replacements are
always the upper-case form.

**Twenty-one records carry exactly one replacement; one carries two.** `c:11` is the exception, with
`(C:26, 0)` and `(C:43, 1570)`. That single extra pair is why a letter census of the file finds **23**
upper-case ids against 22 records, and the loose `1570` that a fixed-stride reading strands in the
middle of the file is simply that second pair's companion word.

The runtime record is **48 bytes** (`lea r9, [r10+r10*2]` / `shl r9, 4`):

```c
+0x00  u32   id            /* the record's own id, always the lower-case form */
+0x04  u32   f1            /* -1 in 18 records, 1 in c:6, c:19, s:1, s:24     */
+0x08  u32   f2            /* -1 in 18, 0 in the same four                    */
+0x0C  u32   extraCount    /* written last, from r8d                          */
+0x10  u32   extraA[4]     /* first word of each pair                          */
+0x20  u32   extraB[4]     /* second word of each pair                         */
```

**The shipped data uses at most 2 of the 4 extra slots**, so the runtime record has headroom the
authored table never fills. *Not claimed:* that 4 is a hard limit - nothing bounds-checks it in the
loop, so a longer authored list would overrun the record, and no such list ships.

## 7. What this document does not claim

- [x] **UQ-216.** *(SUPERSEDED in the register 2026-09-26, FABLE, Claude Opus 5.5: a duplicate; the open residue is carried by **HM-1**)* What the mapping's 39 values index and why only `hc1006_03` has one, what the replace table's `b` and `c`
      arguments are (the callers pass `002657E0(actor)` and `00263FC0(actor)`, not decoded here), how an id with
      high word `c`/`n`/`s` and one with `C`/`N`/`S` name models, and what `0022A0B0` is. `HM-1`.

  *`HM-1` narrowed further 2026-09-27 (OPUS): the replacement ids name files.*
  - An upper-case id `X:M` is entry M of the PS2 disc file list's high-model kind for its letter: C = kind 15 (`high\c*`), N = kind 20 (`high\n*`), S = kind 24 (`high\s*`).
  - The discriminator: those lists are unsorted, yet the resolved models rise strictly in record order (C: hc1004 to hc1044; N: hn1017 to hn1159; S: hs0003, hs0020).
  - `(C:26, 0)` / `(C:43, 1570)` are two variants of one model, hc1021_03 / hc1021_13.
  - *Narrowed further, the source ids too (OPUS, 2026-09-27):* a lower-case id `x:N` is the Nth `.cm` of its model kind (c 14, n 19, s 23). In all 22 records the source and every replacement are one model number's normal and high-detail files (c:0 c1004 -> hc1004, ...), so the table maps a model to its own high-detail variants (control H4).
  - *Narrowed further, the letter-to-kind step read in the executable (OPUS, 2026-09-27):* a model id is `(letter << 16) + N` (the id builder `002EB7A0`), and the model loader `002E6700` resolves it through `002ED6F0(id, &kind, &index)`, a jump table on the letter setting `index = stride x N` - c / n / s to kinds 14 / 19 / 23 at stride 25, m 34 at 11, b 22 and g 13 at 2, C / N / S / M / t / w to 15 / 20 / 24 / 18 / 25 / 16 at 1, any other letter kind 1 - then `0032E400` reads the `.fst` size of that (kind, index). Every decoded kind's list in the disc file list tiles into stride-sized model blocks (a `.cm`, then its `.ca` files), so `stride x N` is the Nth `.cm`: the readings above are the engine's own rule. Control [`hm1_letter_kind.py`](../../_index/candidates/hm1-high-ids/hm1_letter_kind.py) (5 checks).
  - *Narrowed further, the second skeleton is the element row's PARENT (OPUS, 2026-09-27):* `003703A0` reaches the other record through the element row's `+0x0C`, which every writer sets to the encoded pointer of the row at its own `+0x08` parentSlot on the same bank (or null), and a row's `+0xA8` is its character-render-record index. So the 39-value map retargets the mapped element's joints onto the model it is attached to. Control [`hm1_parent_skeleton.py`](../../_index/candidates/hm1-parent-skeleton/hm1_parent_skeleton.py) (4 checks).
  - *Narrowed further, the +0x08 parentSlot writer is the render-record ATTACH step (OPUS, 2026-09-27):* the attach bodies `00370180` / `00373160` store the parent row's `+0x04` slot in the child row's `+0x08`, reached only from the render-record attach helpers, which take the parent as the record indexed by the child record's `+0x3CE` and the attach point from its `+0x3CC` - words only the attach setters `0042F310` / `0042F3B0` store. So the parent is not in the skeleton or model data: it is whichever record a runtime attach names. Control [`hm1_parent_writer.py`](../../_index/candidates/hm1-parent-writer/hm1_parent_writer.py) (10 checks).
  - ~~Not claimed: which actor a shipped script or mount attaches the `c1006` model to.~~ *Narrowed further, HM-1 BODY BIND 2026-09-27 (OPUS): `hc1006_03` is `c1006`'s replacement BODY, attached by the bind machinery, not by a script's `attach`.* The record `c:3` (c1006) has key (-1,-1) and one pair `C:22` (hc1006_03) at threshold 0, so `0037CB90` always returns it. When a bind request (`bindp`, the `bindp2` family, `bindhoff`) binds a model with a replacement, the poll `003409F0` goes to mode 3 and the result `00342640` calls `002E3110` with k = 4. That binds the replacement into the unit's `+0x90` body element, makes it the child of the unit's own record (code `0x7FFF`, `0042F310`), and gives it binding state 2 (`002EDF90`). The dirty pass turns `0x7FFF` into a whole-skeleton bind (`004215A0` -> `004219C0`), and `003703A0` maps only at state 2. So the 39 values map `hc1006_03`'s joints onto the bound `c1006` model's skeleton. Control [`hm1_body_bind.py`](../../_index/candidates/hm1-body-bind/hm1_body_bind.py) (B1-B8, 10 mutants rejected).
  - ~~Not claimed: which shipped bind request names `c1006` in the four maps that load `C:22`~~ *BIND REQUESTS NAMED 2026-09-27 (OPUS): in each of the four maps one script - labelled Fran in all four - binds `c:3` with `bindp2` (`bindp2_d4` in dgl_g0102), and also `bindh`s `C:22` directly (k = 2, no mapping state). The argument is a pool value `0x3000000 + k` that `002E9A60` -> `00263F80` resolves to entry k of the EBP's section 12, the manifest. Control [`c22_bind.py`](../../_index/candidates/hm1-parent-writer/c22_bind.py).*
  - *LIP FLAP 2026-09-27 (OPUS):* the `+0x304` bit 6 that the k = 4 bind sets on the unit's own record (`002E31DB`) is not a hide flag but the **lip flap**. It is `setkutipakustatus`'s bit (`002E8570`), mirrored into `+0x40B` bit 5 by `00429C40`, which switches rig controller 9 on through `0042DD90` for the record and the records linked under it, the replacement body included. k = 4 stores a timer of 0, which the countdown `0042EE90` never counts, so the mouth stays on until k = 2 clears it. Control [`hm1_lipflap.py`](../../_index/candidates/hm1-body-bind/hm1_lipflap.py) (L1-L5).
  - Not claimed: what is drawn (nothing found hides the base model), and the run-time order of the `bindp2` / `bindh` calls.
  - Control: [`hm1_high_ids.py`](../../_index/candidates/hm1-high-ids/hm1_high_ids.py) (`c2f10a0aa`).
  *`HM-1` narrowed 2026-09-26 (FABLE, Claude Opus 5.5).* Control: [`hm1_model_selectors.py`](../../_index/candidates/hm1-model-selectors/hm1_model_selectors.py) (5 checks, FAILS 0). First read by a
  delegated read-only pass; every step re-checked.
  - **`b` and `c`** are the actor's secondary-context bytes `+0x14C` and `+0x14D`: the model **local number**
    (default 1) and **CLUT number** (default 0). The names come from the debug verbs `debug_tty_modellocalno` and
    `debug_tty_modelclutno`, which print them; they are developer labels, not a consumer's use.
  - **Their one writer.** A single setter stores both, and its only call, in the secondary-context initialiser,
    passes (1, 0). So in the shipped build every lookup is keyed `(1, 0)`. The four replace records keyed `(1, 0)`
    always match, and the other 18 are keyed `(-1, -1)`.
  - **The mapping's 39 values are joint indices into a second skeleton.** When the pose mode is 2, each non-`-1`
    value makes that joint follow the given joint of the skeleton the record names at `+0xC`; `-1` leaves the
    joint alone.
  - **`0022A0B0`** is the boot routine on [what the engine fixes at boot](../../00-Engine-Core-Runtime/what-the-engine-fixes-at-boot.md).
  - **Still open:** ~~which models the ids name (the id space is not a simple `c`+number rule: `C:43` has no~~
    ~~`c1043` model)~~ *(answered: see the OPUS narrowings above - the ids name files, and the second skeleton is the element row's parent; 2026-10-02, OPUS)*, what pose mode 2 is~~, and which model the mapping's second skeleton is~~.

## 8. Related

- [The `.adm` add-motion tables](adm-add-motion-tables.md) — the folder's per-bone tables.
- [Model and motion formats](README.md).

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### Both files reproduce, walked by their loaders' rules

| claim | measured |
|---|---|
| one copy of each, in `ps2data/add_motion/` | **one each** |
| `skeletonmapping.bin` **196** bytes, count **1**, name `hc1006_03`, `n` = **39** | **196 / 1 / `hc1006_03` / 39** |
| its walk ends exactly at the file size | **196 of 196** |
| `highmodelreplace.bin` **540** bytes, **22** records | **540 / 22** |
| the walk through the closing `-1` ends exactly at the file size | **540 of 540** |
| 21 records with one pair, 1 with two | **21 / 1** |
| `keyB` — `-1` in 18, `1` in 4 | **18 / 4** |
| `keyC` — `-1` in 18, `0` in 4 | **18 / 4** |
| `modelId` high word 99 / 110 / 115 in 14 / 6 / 2 | **14 / 6 / 2** |
| replacement high word 67 / 78 / 83 | **15 / 6 / 2** over the 23 pairs |
| `minProgress` — 0 in 22 pairs, 1570 in one | **22 / 1** |
| the `(a, b, c)` keys are distinct | **distinct** |

The record shape §2 describes is confirmed by arithmetic as well as by the walk:
`22 × 12 + 23 × 8 + 22 × 4 + 4 = 540`, the file exactly — twelve-byte heads, eight-byte pairs, a
`-1` closing each pair list and one more closing the stream.

**One sharpening.** §*Corpus validation* writes the joint list as *"`-1` ×21, `27`–`30`, `33` ×8"*.
The multiplicities are **`27`×3, `28`×3, `29`×3, `30`×1** — which with 21 and 8 sums to the 39 the
record declares. For a per-joint index list the multiplicity *is* the content, and a range shorthand
hides that three joints share each of 27, 28 and 29 while 30 is used once.

### ✔ New: a replacement keeps the family letter and flips its case, 23 times out of 23

§2 notes the high words are ASCII (`c` / `n` / `s` for sources, `C` / `N` / `S` for replacements) and
stops there. Paired up:

* **23 of 23** replacements carry **the uppercase of their own record's letter** — no `c` record ever
  points at an `N` or `S` replacement;
* **0 of 23** keep the number.

So the id is `(letter << 16) | number`, **the letter is the model family and the case marks the role**
— source or replacement — rather than naming a different family. A reader who took the case for part
of a file name would look for the wrong thing, which is exactly what I did next.

### A limit, recorded instead of a finding

I then searched the archive for model resources whose names begin `HC`, `HN` or `HS`, to see whether
the uppercase letter is a naming convention. It returned **0**, and the result is **worthless**:
**the archive index is entirely lower-cased — 0 of 89,414 entries contain a single uppercase
character.** The search could not have succeeded.

> **This is a limit on a whole class of question, not just this one.** Nothing about name *case* can
> be tested against the VBF index; the case survives only inside file contents (the `.ta` lists and
> `phyremaps.txt` carry `/GameData/D3D11/…` with capitals intact) and in `.rdata` literals. Any
> future census that keys on a capitalised name must go to those, never to the index.

**Not claimed.** What the 22 model ids and their replacements are on screen — §7's first unknown
stands. ~~What `keyB` / `keyC` select when they are not `-1` — four records set them and nothing here~~
~~says to what.~~ *(answered: see §7, HM-1 2026-09-26 - `b` / `c` are the actor's model local number and CLUT number, and every shipped lookup is keyed (1, 0); 2026-10-02, OPUS)* Whether `1570` is a story-progress value in the units the flag banks use — the number
is read, the scale is not. Whether an uppercase-lettered resource exists anywhere — **untestable
against the index, and not tested against file contents here.** The archive was **read, never
written**, and nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** A cited function is called by `BattleStats_ModifyStatusLayerStateAndProcessSideEffects`, `BattleStats_RecomputeDerivedStateAndAutoStatuses` and `BattleUnit_RunPeriodicCombatMaintenance`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Audio — CLIENT.** `FUN_00210760`, owned by that layer, calls `001D6F20` on this page. That caller is a 451-byte config read that names the file: it joins the base path and the literal **`.win.config`**, opens that, and sizes it before reading; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — SERVICE.** `0037B4D0` on this page calls `PartyRoster_IsFourSlotIndex`, owned by that layer. What it reaches is nine bytes that answer whether an index is inside the party: `index <= 3`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — SERVICE.** `0017D4C0` on this page calls `FUN_001c1710`, owned by that layer. What it reaches is **ten bytes**: it swaps zero into `byte[+0x10]` - an atomic clear that keeps the old value - and jumps on; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Movement — SERVICE (SWE2-CONTRACT 2026-09-15, 13 edges).** `0037B4D0` — the bind body — initializes the model's
movement presentation: it calls `Movement.CharacterPresentation.BindingInitialization` `002E28E0`
and `BindingUpdate` `002E3110` (2 edges each via `003409F0`/`003460F0`), `Actor_SetFacingHeading_Variant1`
`0026B620`, `Actor_SetDesiredMovementHeading` `0026A0D0`, `002E5C70`, `0026AF80`, `0031BAC0`,
`002E4A40`, `00263560`, `002E49B0` and `002681D0`. Binding a skeleton/motion pair writes the actor's
presentation-binding and heading state — a real initialization crossing, not fan-in.

**Script_VM_Native_Bridge — CLIENT (SWE2-CONTRACT 2026-09-15, 7 edges).** `003409F0` and `003460F0` — the bridge
bodies that drive `0037B4D0`'s binding — reach this page through `00263FC0`/`002657E0`/`0037CB90`
(3 edges each); `thunk_FUN_003409f0` `00342330` forwards to `003409F0`. The script VM triggers the
skeleton binding — the layer consults this page's functions.

**Combat — CLIENT (SWE2-EC7 2026-09-19, 1 edge).** `00263E30`, a callee this page's `0031BEC0`
section cites, is also called by the Combat-filed `003206E0`. The combat caller is a mechanical
user of the same shared helper.

**CoreRuntimeScheduling — MECHANICAL (SWE2-CONTRACT 2026-09-15, 9 edges).** 4 edges are `0020E600`/`0020E620` inside
`003703A0`/`00372820`/`0037B4D0`; `0022A0B0` trades calls with `0036FFF0`/`0037CCC0`/`0017D4C0`/
`0022BDF0`; `001EC760` reaches `00265270`. Fixup and frame helpers.

**Gameplay — SERVICE (SWE2-CONTRACT 2026-09-15, 3 edges).** The bind body `0037B4D0` calls `WorldActor_GetDefinitionByte12OrMinus1` `002E9C00` and `ActorHandle_GetPrimaryFormulaResourceByte26` `00321380`; `0031BAC0` calls `BattleEncodedId_IsValidForClass` `00322C50`. Binding a skeleton reads the unit's definition bytes — the substantive edge of the pair.

**Resource — SERVICE (SWE2-EC7-167, 67 edges).** `0036ED50` — a tail the batch-132 slot issuer
`0036F0F0` runs — calls `0032E620`/`0032E400` on the Resource layer; the rest of the pair is
`001D6F20`'s `00597930`/`0059D900` callees and its `0017D9D0`/`001A9050` callers (+63 more).
Slot init consults resource bodies through the shared helper; no resource ownership here.

**World — CLIENT and SERVICE (SWE2-EC7-168, 4 edges).** `0032E400`/`0032E620` — the record
issuers this page's `0036ED50` composer runs — are called by World body `00378540`; World body
`00266D10` calls `0022A0B0` and is itself called by `00314D40`. Shared-helper fan-in both
directions; no world ownership here. Edge list from `edges.tsv`.

**WorldAreaField — CLIENT and SERVICE (SWE2-EC7-168, 16 edges).** `00265270` — a helper this
page names — is called by `001EDCD0`/`003145E0`/`003EAA70` on the world-area layer, and
`0031C000` reaches the layer (+12 more). Shared-helper fan-in; no world-area relationship to
the skeleton tables. Edge list from `edges.tsv`.

## The `00372820` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)

The pose-record setup `00372820` (1,844 B): `ebx = r8w` tag (`0037284A`),
`0020E620`/`0020E600` hash helpers (`0037284E`/`0037285C`),
`00409F50`/`00409A30`/`004096C0` (`00372867`–`00372887`), then the
`02AD9E38`/`02AD9E30` name table (`003728B4`/`003728CE`) byte-compared
`byte[rax]` vs `byte[rax+r8]` (`003728E0`–`003728E3`), `word[rbp+0x38]`
and `word[rbp+0xC]` through `0020E620`/`0020E600` (`00372928`–
`0037296F`), `003AB7F0` (`00372977`).

| member | role | interior |
| --- | --- | --- |
| `00373DC0` (221 B) | pose-record initializer — `0046D120` ×2 (`00373DD0`/`00373DDC`), `1.0f` seeded at `+0x1AC`/`+0x1CC`/`+0x1EC`/`+0x1E8`/`+0x1E4`/`+0x1E0` (`00373DE1`–`00373E31`), `[+0x1A4]`/`[+0x1C4]` ptr + `[+0x1A0]`/`[+0x1C0]` dword = eax (`00373DED`–`00373E03`), `word[+0x280] = ax` (`00373E3B`) | [`00373DE1`](../../_index/ADDRESS-INDEX.md) |
| `004094D0` (200 B) | tail-word gather — `dword[rcx+4]` vs 2 (`004094D0`), `r9d = [rcx+0x34]`, `edx = [rdx+4]`, then `word[rdx+r10-6]`/`-4`/`-2` × `dword[r9+rax*4]` → `[r8-0x28]`/`-0x24`/… (`00409512`–`00409538`) | [`00409512`](../../_index/ADDRESS-INDEX.md) |
| `004095A0` (8 B) | index→offset helper — `rax = movsxd(ecx) + 0x40` (`004095A0`–`004095A3`) | [`004095A3`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0020E620`, `0020E600`, `00409F50`,
`00409A30`, `004096C0`, `003AB7F0`, `0046D120`. (`0051EE00` seen adjacent
belongs to sibling `004095B0`, not this subtree.)

## SWE2-EC7-41 update (2026-09-19) - `003409F0`

`003409F0` (340 B) is a motion-table body - `002E97C0`/`002EB540`/`002E9810`/`00314D40`/`002E4C20`/`00263FC0`/`002657E0`/`0037CB90`. Interior anchor `00340A23` (an `002E97C0` call).

## SWE2-EC7-51 update (2026-09-19) - `003460F0`

`003460F0` (179 B) is a body - `00263FC0`/`002657E0`/`002E3110`/`002E3C20`/`002E4C20`/`002E97B0`/`002EB540`/`002EBC90`. Interior anchor `00346100` (a `00263FC0` call).

## SWE2-EC7-51 update (2026-09-19) - `0046E4D0`

`0046E4D0` (178 B) is a body - `002ED570`/`003721E0`/`00372820`/`0046E6F0`/`0051FBB0`. Interior anchor `0046E4F0` (a `002ED570` call).

## SWE2-EC7-53 update (2026-09-19) - `0046E6F0`

`0046E6F0` (444 B) is a motion-table body the handlers page lists as a `00520010` caller - `00520010`/`00537170`/`00537180`/`00537260`/`002ED570`/`0020E600`/`003AB7F0`, `[rsi+0x60]`-list walk under `[rsi+0x40]` count. Interior anchor `0046E719` (a `00520010` call).

## SWE2-EC7-54 update (2026-09-19) - `0051FBB0`

`0051FBB0` (307 B) is a motion-table body - `003AB7F0`/`0051F7A0`. Interior anchor `0051FBDB` (a `0051F7A0` call).

## SWE2-EC7-56 update (2026-09-19) - `0051F7A0`

`0051F7A0` (216 B) is a motion-table body - `003AB7F0`/`0051F6B0`. Interior anchor `0051F7C1` (a `003AB7F0` call).


## SWE2-EC7-56 update (2026-09-19) - `002E3C20`

`002E3C20` (212 B) is a motion-table body - `002E3A60`/`002E42D0`. Interior anchor `002E3C8F` (a `002E3A60` call).

## SWE2-EC7-62 update (2026-09-19) - `003721E0`

`003721E0` (150 B) is an add-motion body - `0020E620` single call. Interior anchor `00372201` (a `0020E620` call).


## SWE2-EC7-62 update (2026-09-19) - `0031BEC0`

`0031BEC0` (146 B) is a definition-key compare body - `00263750`/`00263E30`/`0031C000`/`0031C0F0`. Interior anchor `0031BEE5` (a `00263750` call).


## SWE2-EC7-71 update (2026-09-19) - `002EB540` name-binding find-or-create measured

Measured on `how-a-script-names-a-thing-in-the-world.md`
(readiness SEMANTICALLY IDENTIFIED - non-bearing); mirrored here where
the motion-table callers live.

`002EB540` (130 B) measured: walks the `0215FD58` then `0215FD78` lists
for the entry whose `+0x14` equals `ecx`; on a miss it allocates through
`002E25E0`, pushes the entry onto the `0215FD78` head (with the old
head's `+0` backlink), and ORs `byte[+0x19]` bit 3 - the pin flag; then
`bts word[+0x20], r10b` sets the selector's holder bit either way.
Interior anchor `002EB5B5` (the `bts ecx, r10d` holder-bit set).

## SWE2-EC7-76 update (2026-09-19) - `002657E0` + `00263FC0` gated byte readers measured

`002657E0` (41 B) and `00263FC0` (38 B) are the `0x60`-kind `+0xC0`
byte readers: on kind match with `[rcx+0xC0]` non-NULL they return
`movsx byte[rax+0x14C]` / `movsx byte[rax+0x14D]`; defaults 1 and 0 -
the paired field reads the motion-table bodies share.
Interior anchors `002657FB` / `00263FDB` (the `movsx` reads).

## SWE2-EC7-83 update (2026-09-20) - `0046D120` identity-matrix init measured

`0046D120` (61 B) is the identity write the skeleton callers run:
the 0x38 block zeroes and `1.0f` lands at `+0`, `+0x14`, `+0x28` and
`+0x3C` - a 4x4 identity row-major, call-free.
Interior anchor `0046D141` (the `+0x3C` 1.0f store).

## SWE2-EC7-112 update (2026-09-20) - `0017EFC0` measured

`0017EFC0` (54 B) is the
gated predicate `003703A0`
and `0053AB50` run: a live
`001BC000()` object forwards
`ecx` to `001BB040` and the
boolean answer returns; a
null object answers 0
without calling.
Interior anchor `0017EFDC`
(the `001BB040` call).

`0017EF60` (82 B) is the
two-null-gated call
`003703A0` and `0053AB50`
run beside it: null `rcx` or
null `rdx` is a no-op, else a
live `001BDAB0()` object
takes `001BD630(obj, rcx,
rdx, r8)` - all three
arguments pass through.
Interior anchor `0017EF9D`
(the `001BD630` call).

`001BD630` (416 B) is the record-list compare `0017EF60` calls: `([rdx+0x38] - [rdx+0x30]) >> 3` and the same on `r8` gate empty lists, then the first elements' `[0] -> [0] -> +0x30`/`+0x48` fields are compared and `001F6E00` runs twice - the motion table's element-wise equality walk.

Interior anchor `001BD6E0` (function `001BD630`).

`0036F0F0` (318 B) is the four-slot allocator `003466A0`/`0037B4D0` call on the `021B9AE0` table (4 records x 24 B, `word[+0x16]` refcount): `0036F240` resolves `edx`; a hit bumps `+0x16`, clears `byte[+3]`, and returns `(sbyte[+2]<<4) | sbyte[+1]`; a miss scans the four slots for `word[+0x16]==0` then runs the `002DF440`/`00369800`/`0036ED50` init tail - the skeleton-adjacent slot issuer the bind body uses.

Interior anchor `0036F118` (function `0036F0F0`).

`0036ED50` (342 B) is the record composer `0036F050`/`0036F0F0` call: `0032E400(0x21, sword[rcx+0x14])` issues the first slot and packs `(sbyte[+2]<<4) | sbyte[+1]` into `esi`; `eax>0` runs `0036C1D0(6)`, `0036B160` -> `dword[+0xC]`, `byte[0]=1`, `byte[+3]=0`, `0036C140`/`0036A0B0`, then `0032E620` registers the record against the `0036EAB0` vtable with `r9d`=the first slot, `edx`=the `+0x14` word - a `eax<=0` leaves `dword[+4]=0xFFFF`; a second `0032E400(0x27)` tail follows - the init half the four-slot issuer defers to.

Interior anchor `0036EDF7` (function `0036ED50`).

`003713C0` (215 B) is the motion-table wiring: `[rbx+0x80]` resolves through `0020E600` + `003AB7F0` rebase + `0020E620` into `dword[+0x84]`; when `word[+0x16] != -1` the `[+0x18]` handle chains `00409F50` + `004096C0` into `+0xA0`/`+0x94`, and the `+0x90`-gated tail rebases `+0x84`/`+0x94` by the resolved bases then hands the block to `003E1C50` - the bind pass the motion-table and ramp-channel callers share.

Interior anchor `0037140A` (function `003713C0`).

`00520010` (228 B) is the chunked-list walk: `[rcx+0x40]` holds the chain head, each id `i` rebases `[+0x30]` through `003AB7F0` into `[+0x38]` and selects node `[+0x38]+i*16`, rebases `[+0x8]` into `[+0x10]` for the `(i >> [+0x4C]) * 0x20` sub-record whose `dword[+0x10]` decodes via `0020E600`, checks `dword[node]` against -1 or the `([+0x50] & i) * [+0x48]` mask word, and fires callback `r12(rcx, rdx)` per element until `[r14+8]` hits -1 - the motion-table and monster-viewer callers' shared enumerator.

Interior anchor `005200C6` (function `00520010`).

`003E1C50` (2992 B) is the load-side pointer fixup pass over a freshly read record: every stored offset field is resolved through `0020E600` (offset to live pointer) and rewritten in place with `0020E620`, word-indexed slots reach the 0x740-stride table at `022C6F28` only while its `+0x284` sentinel is nonzero, and nested structures recurse through the type-dispatched relocators `00421D20`, `00512A90`, `004719B0`, `0051A380`, `0051B850`, `005161D0` and `0040EEA0` - clearing the field to a fresh `0020E620(0)` offset when the sub-record is absent. Called from `003713C0` on the motion-table load path.

Interior anchor `003E1D9A` (function `003E1C50`).

`00421D20` (70 B) is the keyed sub-record probe the load-side fixup `003E1C50` and the staged-look command `003E3D70` share: when the record's `+0x18` index is not -1 it resolves the `+0x10` page offset through `0020E600`, probes the resolved page's `+0xD98` manager table with `002ED570` for that index, and on a hit tail-resolves the found record's `+0x84` field through `0020E600` - an absent index or empty slot returns 0.

Interior anchor `00421D49` (function `00421D20`).

`00415A80` (1117 B) is the delta-shifted offset rebase `003E1C50` applies to its nested record families: the head offset `[r13]` is resolved through `0020E600`, shifted by `edi` and stored back through `0020E620`, then for each of the `[r13+4]`-counted outer records the same resolve-shift-store pair fixes the `+0x8` section head before walking that record's own byte-counted `0x20`-stride sub-record array - each sub-record's offset fields (`[r15-0x1C]`, `[r15+8]`, and the deeper sub-arrays) receive the identical treatment, a uniform pointer-plus-delta rewrite over the whole nested layout.

Interior anchor `00415CF0` (function `00415A80`).

`001BB040` (224 B) is the paired-bound probe `0017EFC0` runs on the `rdi+0xB8`-headed BST: it lower-bounds `edx` against node key `+0x20`, requires the found node's resolved `+0x28` byte `+0x98` to be nonzero, then lower-bounds `0xFFFFFFFE - edx` and calls `001BB120` on that second node's `+0x28` - only when that precondition passes does it tail `001BB120` on the first bound's `+0x28`; any failure returns `0`

Interior anchor `001BB0C5` (function `001BB040`).

`00373D00` (188 B) is the per-slot combine `00372820` runs over the skeleton link list: `[rbp+0x84]` `0020E600`-resolves the `0x290`-stride row table `rbx`, `rdi = [rbp+0x88] * 0x290` walks the `+0x8A`-counted word index list, and for each entry the selected row `rcx` contributes its `+0x80`/`+0xC0` pair while its `+0x270` word picks the third argument - `rbx + 0x1F0` when the word is `-1`, else `ax * 0x290 + 0x80` into the same table - handed to `0046D350` once per linked slot

Interior anchor `00373D50` (function `00373D00`).

`0046E0F0` (186 B) is the attachment walk `0041E340` runs per model record between frames: `00537170`/`00537180` expose the `[rsi+0x60]` word table and its count; each entry's `-1`-guarded word `002ED570`-resolves to `rbx`, and when `[rbx+4] != -1`, flag `0x4` is set and `[rbx+0xA0]` `0020E600`-resolves, a second `002ED570` on `[rbx+8]` supplies `rdx` for `00373F40(rbx, rdx)` - then `003703A0(rbx)` runs unconditionally, the link-then-close the oscillator rows need

Interior anchor `0046E130` (function `0046E0F0`).

`00373F40` (279 B) is the pair-link pass `0046E0F0` runs between a bound record and its peer: `[rdi+0x84]` and `[rbp+0x84]` `0020E600`-resolve the two `0x290`-stride row tables (`rsi` target, `rbp` source); a live `[rdi+0x14]` word first `0046D350`-combines `rsi+0x1F0` against `rbp+0x1F0` for index 0 or `rbp + 0x80 + ax*0x290` otherwise, then the row at `[rdi+0x88]*0x290` supplies a `[rdi+0x8A]`-counted word list - each entry indexes `rsi`'s table and rows with `+0x270 == -1` but a live `+0x276` word are `0046D100`-linked (`row+0x1F0` against `rbp + 0x80 + ax*0x290`)

Interior anchor `00373F97` (function `00373F40`).

`00373EA0` (151 B) is the fan-out `00372820` runs on its record: `0020E600([rsi+0x84])` twice resolves the `0x290` table and the `[rsi+0x88]`-indexed row's embedded word list; then for each of `word[+0x8A]` entries it calls `0046D340(row + idx*0x290 + 0x150, row + idx*0x290 + 0x80)` - a per-index apply over the record's sub-table.

Interior anchor `00373F0C` (function `00373EA0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-add-motion-skeleton-and-high-model-table-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `001F6E00` | 77 B | measures the zero-terminated string at `rcx`; returns 0 when its first byte is `_` (`0x5F`), otherwise walks the bytes up to the next `_` or the string end, folding each byte from `0` to `9` into `value * 10 + digit` and skipping every other byte, and returns the value | `001F6E09`, `001F6E0F`, `001F6E31`, `001F6E3F`, `001F6E45` |
| `00263F80` | 35 B | masks `edx` to its low 24 bits; when qword `[rcx + 0x100]` is null it returns the masked value, when the value is below (signed) that table's first dword it returns dword `[table + 4 + value * 4]`, and otherwise it returns 0 | `00263F87`, `00263F90`, `00263F92`, `00263F97`, `00263F9D` |
| `002E3A60` | 134 B | returns 0 for a null `rcx`; otherwise, when dword `[rcx]` is not -1, it first (only if `edx` is nonzero) calls `0042F250(word [rcx])`, ORs `0xB` into byte `+0x10` and sets byte `+0x11` to `(byte AND 0x9F) OR 6`, then passes dword `[rcx]` to a 103-byte release and dword `+4` to a 92-byte list lookup and stores -1 to qword `[rcx]`; in both cases it then masks byte `+0x10` to its low nibble, stores -1 to dword `[rcx]` and 0 to qword `+8`, calls a 29-byte flag setter with both flags zero and stores 0 to dword `+0x20`, returning 1 when the release ran and 0 when `[rcx]` was -1 | `002E3A7B`, `002E3A87`, `002E3AAA`, `002E3AB6`, `002E3AD1` |
| `003466A0` | 71 B | pops a value through `VMValueStack_PopInt32CoerceFloat32(r9)`; when byte `[rdx + 0x20]` is non-negative it passes it sign-extended to a 63-byte slot release; it then stores to byte `[rdx + 0x20]` the result of the 318-byte four-slot allocator called with `(0, value)`, and tail-jumps a 7-byte byte-global setter with `ecx = 1` | `003466B0`, `003466BD`, `003466C2`, `003466D5`, `003466E2` |
| `0036EAB0` | 192 B | picks the 24-byte record `(ecx AND 0xF) * 0x18` into `022D9AE0` when any of bits 4 to 7 of `ecx` is set, else into `022D9AB0` (a null record when `ecx` is -1); it resolves dword `[rec + 0xC]` through a 79-byte resolver, reads dword `[resolved - 0x28]` (0 for null) through a 12-byte getter, and stores to dword `[rec + 4]` the result of a 5-byte thunk called with `ecx` = signed byte `+1` (plus 2 when byte `+2` is nonzero), `edx` = signed word `+0x14`, the resolved pointer, that dword and 1; a zero result passes `+0xC` to an 85-byte release, zeroes `+0xC` and stores 3 to byte `[rec]`, a nonzero result stores 3 there only when dword `+8` is nonzero | `0036EAE2`, `0036EB2C`, `0036EB34`, `0036EB4E`, `0036EB56` |
| `0036F050` | 145 B | when byte `022D9B40` is 2 it stores 1 there, calls a 5-byte thunk with `ecx = 0` and passes each 24-byte record from `022D9AB0` below `022D9AE0` whose first byte is 3 to a 342-byte routine; then, when byte `022D9B41` is 2, it stores 1 there, calls the same thunk with `ecx = 1` and does the same for the records from `022D9AE0` below `022D9B40` | `0036F05A`, `0036F065`, `0036F080`, `0036F0A4`, `0036F0C8` |
| `0036F240` | 128 B | when `ecx` is nonzero it scans the four 24-byte records at `022D9AE0`, else the two at `022D9AB0`, and returns the first record whose first byte is nonzero and whose sign-extended word `+0x14` equals `edx`; returns null when none matches | `0036F24C`, `0036F25F`, `0036F26D`, `0036F2AE`, `0036F27B` |
| `004719B0` | 54 B | resolves dword `[rdx]` through `ImageAddress_ResolveRuntimePointer`, stores `RuntimePointer_EncodeImageAddress` of the low 32 bits of `rdx` plus that result back to dword `[rdx]`, then stores `RuntimePointer_EncodeImageAddress(rdx)` to dword `[rcx]` | `004719C2`, `004719C7`, `004719D2`, `004719D4`, `004719DE` |
| `00512A90` | 56 B | resolves dword `[rdx + 0x30]` through `ImageAddress_ResolveRuntimePointer`, stores `RuntimePointer_EncodeImageAddress` of the low 32 bits of `rdx` plus that result back to dword `[rdx + 0x30]`, then stores `RuntimePointer_EncodeImageAddress(rdx)` to dword `[rcx]` | `00512AA3`, `00512AA8`, `00512AB3`, `00512AB6`, `00512AC0` |
| `005161D0` | 43 B | resolves dword `[rcx]` through `ImageAddress_ResolveRuntimePointer` and stores `RuntimePointer_EncodeImageAddress` of the low 32 bits of `edx` plus that result back to dword `[rcx]` | `005161E1`, `005161E6`, `005161E9`, `005161F3` |
| `0051A380` | 56 B | resolves dword `[rdx + 0x10]` through `ImageAddress_ResolveRuntimePointer`, stores `RuntimePointer_EncodeImageAddress` of the low 32 bits of `rdx` plus that result back to dword `[rdx + 0x10]`, then stores `RuntimePointer_EncodeImageAddress(rdx)` to dword `[rcx]` | `0051A393`, `0051A398`, `0051A3A3`, `0051A3A6`, `0051A3B0` |
| `0051B850` | 25 B | stores `RuntimePointer_EncodeImageAddress(rdx)` to dword `[rcx]` | `0051B859`, `0051B85C`, `0051B861` |
| `00537260` | 9 B | loads dword `[rcx + 0x20]` into `r8d` and tail-jumps to a 138-byte routine with `rcx` and `rdx` unchanged | `00537264` |

## Homed frontier bodies called from this page's functions (FABLE, 2026-10-03, cloud-drafted)

*Functions no page cited until now. Each is entered directly from a function this page already cites (the site is given as caller + offset). Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's homing pack and re-read by FABLE against the certified image; verified by [`homing_applier.py`](../../_index/candidates/fable-home-add-motion-skeleton-and-high-model-tabl-1003/homing_applier.py): every site transfers to its function, the page cites the caller, and every anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*

| function | size | entered from | what the body does | interior anchors |
|---|---|---|---|---|
| `0051B120` | 45 B | `003E1C50` + 0x818 | passes dword `rcx+0x10` to the site `0051B120` + 0x12, then passes `edx` plus that result (32-bit) to the site `0051B120` + 0x1A and stores that call's dword result back to `rcx+0x10` | Interior anchor `0051B12F`; Interior anchor `0051B132`; Interior anchor `0051B137`; Interior anchor `0051B13A`; Interior anchor `0051B144` |

## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, 2026-10-03, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read by FABLE against the certified image; verified by [`interior_applier.py`](../../_index/candidates/fable-add-motion-skeleton-and-high-model-table-homing-1003/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `003418B0` | 198 B | returns 0 when byte `r8+8` is 0; otherwise switches on word `r8+0xA`: for 0 it calls `002E97C0(dword [r8+4])` and, when that is null, stores `002E9810(002EB540(dword [r8], byte [rdx+0x15]))` at dword `r8+4`, calls `00314D40(1)` and returns 1, while for a non-null result it calls `002E4C20(result)` and does the same `00314D40(1)` and return 1 when that returns 0, else stores word 1 at `r8+0xA` and returns 0; for 2 it calls `002E4C20(002E97C0(dword [r8+4]))` and calls `00314D40(1)` and returns 1 when that returns 0, else stores word 3 at `r8+0xA` and returns 0; for any other value it returns the dword at `[rsp+0x40]` (the `r8` home slot, which this body never writes) | Interior anchor `003418BA`; Interior anchor `003418E5`; Interior anchor `003418FC`; Interior anchor `0034191F`; Interior anchor `00341954` |
| `00343B00` | 177 B | calls the functions at `00343B00` + 0x24, `00343B00` + 0x2F and `00343B00` + 0x39, each with `r9`, passes the second result to `002E9A60`, stores word 0 at `r8+0xA` and clamps the third result to 0..1 (signed: negative gives 0, above 1 gives 1); when the call at `00343B00` + 0x64 with byte `rdx+0x15` returns non-zero it stores byte 0 at `r8+8` and returns, otherwise it stores the `002E9A60` result at dword `r8`, `002E9810(002EB540(that result, byte [rdx+0x15]))` at dword `r8+4`, the first result at dword `r8+0xC`, the clamped value at byte `r8+9` and byte 1 at `r8+8` | Interior anchor `00343B4C`; Interior anchor `00343B5D`; Interior anchor `00343B6D`; Interior anchor `00343B7D`; Interior anchor `00343B94` |
| `00344F00` | 121 B | passes the result of the call at `00344F00` + 0x18 (with `r9`) to `002E9A60` and stores word 0 at `r8+0xA`; when the call at `00344F00` + 0x30 with byte `rdx+0x15` returns non-zero it stores byte 0 at `r8+8` and returns, otherwise it stores the `002E9A60` result at dword `r8`, `002E9810(002EB540(that result, byte [rdx+0x15]))` at dword `r8+4` and byte 1 at `r8+8` | Interior anchor `00344F1F`; Interior anchor `00344F28`; Interior anchor `00344F39`; Interior anchor `00344F55`; Interior anchor `00344F6A` |
| `0034CED0` | 66 B | calls the function at `0034CED0` + 0x10 with `r9` and, when its result is negative (signed), replaces it with the result of the call at `0034CED0` + 0x1B; calls the function at `0034CED0` + 0x25 with `r9` and passes its result to the call at `0034CED0` + 0x2C; then tail-jumps to `00314D40` with the kept value | Interior anchor `0034CEE9`; Interior anchor `0034CEEB`; Interior anchor `0034CEFC`; Interior anchor `0034CF01`; Interior anchor `0034CF0D` |
| `00352E40` | 60 B | calls the function at `00352E40` + 0x10 and then the one at `00352E40` + 0x1A, each with `r9`, passes the second result as the first argument and the first result as the second argument to the call at `00352E40` + 0x23, then tail-jumps to `00314D40(1)` | Interior anchor `00352E5A`; Interior anchor `00352E5F`; Interior anchor `00352E63`; Interior anchor `00352E68`; Interior anchor `00352E77` |
| `0036EB70` | 160 B | walks the 24-byte records at `022D9AEC` up to `022D9B4C` (four records) and then those at `022D9ABC` up to `022D9AEC` (two records); for each it calls `002DF440` with the sign-extended byte at record `-0xB`, plus 2 when the byte at record `-0xA` is non-zero, then calls `00369800` with dword `+0` and with dword `+4`, storing 0 to each dword after reading it | Interior anchor `0036EB9B`; Interior anchor `0036EB9E`; Interior anchor `0036EBA5`; Interior anchor `0036EBB4`; Interior anchor `0036EBDE` |
| `0050CA40` | 67 B | calls the function at `0050CA40` + 0x13 with `r9` and, when its result is greater than 0 (signed), replaces it with `002E9A60(result)`; stores the value at dword `r8` and, when it is not negative, stores `002EB540(value, byte [rdx+0x15])` at qword `r8+8` | Interior anchor `0050CA5A`; Interior anchor `0050CA5E`; Interior anchor `0050CA63`; Interior anchor `0050CA6F`; Interior anchor `0050CA74` |
| `0050CBD0` | 95 B | when dword `[r8]` is negative (signed) tail-jumps to `002E3C20(rdx, 0, 0)`; otherwise calls `002EBC90(rdx, 2, 1)` and then `002E3110(rdx, 0, 0, qword [r8+8])` with 0 as the fifth (stack) argument | Interior anchor `0050CBE7`; Interior anchor `0050CBF2`; Interior anchor `0050CC00`; Interior anchor `0050CC0B`; Interior anchor `0050CC2A` |
| `0050CD80` | 94 B | when dword `[r8]` is negative (signed) tail-jumps to `002E3C20(rdx, 1, 0)`; otherwise calls `002EBC90(rdx, 1, 1)` and then `002E3110(rdx, 1, 0, qword [r8+8])` with 0 as the fifth (stack) argument | Interior anchor `0050CD9C`; Interior anchor `0050CDA1`; Interior anchor `0050CDB8`; Interior anchor `0050CDBC`; Interior anchor `0050CDD9` |
| `0050CF20` | 99 B | when dword `[r8]` is negative (signed) tail-jumps to `002E3C20(rdx, 2, 0)`; otherwise calls `002EBC90(rdx, 3, 1)` and then `002E3110(rdx, 2, 0, qword [r8+8])` with 0 as the fifth (stack) argument | Interior anchor `0050CF37`; Interior anchor `0050CF42`; Interior anchor `0050CF5D`; Interior anchor `0050CF70`; Interior anchor `0050CF7E` |
