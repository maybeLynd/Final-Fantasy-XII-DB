---
system: The PKFL package container
category: 26-PKFL-Package-Container
status: AUDITED — the layout, the walker and the corpus read; the four residues of section 7 closed 2026-09-18 (the magic negative by a body read of every directory reader, the 27 empties, slots 16-27 and the 64-slot ceiling by a full census under the pair reading)
owner_layer: CodeDomain:Resource.PackageContainer
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 9 cited function entries, 0 of them among the 109 records that changed GN160 -> GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0), established for this document 2026-09-14 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "10,314 / 10,314 shipped packages, every header and directory re-parsed from FFXII_TZA.vbf 2026-09-04" # <- corrected 2026-10-02, OPUS - that parse read the withdrawn four-byte entry; re-parsed under the pair reading 2026-09-11 (section 5) and 2026-10-02
last_reviewed: 2026-09-04
archive_formats:
  - "mot"
  - "snd"
  - "vpc"
  - "vpcjp"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: GN160-corpus-reparse-repos-1e — independent VBF parse of all 10,314 packages, not this sheet's census; every corpus claim reproduced, §3 loader contract NOT audited
  crossref_clean: true
  reopened_count: 0
---

# The `PKFL` package container

> **One container wearing four extensions.** `.mot`, `.snd`, `.vpc` and `.vpcjp` — 10,314 files,
> 5.2 GB — are the same eight-byte header and the same indexed offset directory. The extension
> says what a package is *for*; it does not say it is a different format.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **10,314 of 10,314** — every shipped package, header and directory re-parsed from the archive |
| magic `PKFL` | **10,314 / 10,314** |
| `.mot` | 4,392 files, 2,552 MB, `slotCount` **16** in all |
| `.snd` | 2,304 files, 146 MB, `slotCount` **16** in all |
| `.vpc` | 1,809 files, 1,240 MB, `slotCount` **64** in all |
| `.vpcjp` | 1,809 files, 1,298 MB, `slotCount` **64** in all |
| occupied slot indices | ~~**0–27**, densely — no index in that range is ever unused~~ **0–15** in `.mot` / `.snd` and **0–13** in `.vpc` / `.vpcjp`, each index in those ranges used somewhere *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages; §7's 2026-09-18 closures)* |

**Independently re-derived, not inherited.** The occupancy in this sheet was parsed here from the
archive and then compared against the frozen `pkfl-container-census.tsv`: ~~**10,314 common paths,~~
~~10,314 agree, 0 differ.**~~ 10,314 common paths, which agree only because both parses used the withdrawn four-byte entry *(corrected 2026-10-02, OPUS: the TSV's `present` column is the four-byte word indices of `census_pkfl_container.py`'s `read_dir`; re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages, 27 of its 10,314 rows agree - the empty packages; a re-freeze is SWE2-DATA's)*. Two independent parses of the same 10,314 files reaching the same
occupancy is worth much more than either alone.

---

## 1. What the player sees

**Nothing, directly — this is a wrapper.** But it is the wrapper around a great deal of what you do
see. `.mot` holds motion, `.snd` the per-map sound set, `.vpc`/`.vpcjp` the voice clips for a map in
two languages. Every one of them arrives inside this same small structure: a tag, a count, and a
list of offsets saying where each piece begins.

The one player-facing consequence worth stating plainly is the language split. **`.vpc` and
`.vpcjp` are not two formats and not two halves of one file — they are the same package built
twice**, and the engine chooses between them by asking for a different *resource namespace*, not a
different filename (§3). That is why the two counts are identical at 1,809 each.

## 2. The layout

```struct PkflHeader base=file size=0x08
+0x00  char[4]  magic       'PKFL' -- 10,314 / 10,314
+0x04  u32      slotCount   16 (.mot, .snd) or 64 (.vpc, .vpcjp); no file mixes them
```

~~The directory follows immediately: `slotCount` `u32` offsets, one per slot index, **`0` meaning the
slot is absent**. The directory therefore ends at `8 + 4*slotCount` — `0x48` for a 16-slot package,
`0x108` for a 64-slot one.~~

**Corrected 2026-09-11 (§8): the directory is `slotCount` pairs of `{u32 offset, u32 size}`**, eight
bytes per slot, `{0, 0}` meaning the slot is absent; it ends at `8 + 8 × slotCount` — **`0x88`** for a
16-slot package, **`0x208`** for a 64-slot one — which is exactly what the engine reads as the
directory (§3).

    +0x08  { u32 offset, u32 size }[slotCount]   file-relative; {0, 0} = slot absent

*Deliberately not a `struct` fence: the array length is `slotCount`, a runtime value, and
`check_layouts.py` requires a literal. A fence with an invented length would be worse than prose.*

**The directory is indexed, not packed** — the same idiom as
[EBP's container](../../25-EBP-Script-Container/README.md) — so a slot's index is its identity and
a zero entry means that index is unused in this package.

> **Three things a reader will assume from that idiom and which are false here.** Each is measured
> over all 10,314 files in §5: ~~offsets are **not** ascending in slot order;~~ the first payload is
> **not** at the directory end; ~~and a slot's length is **not** reliably the distance to the next~~
> ~~slot's offset, because slots may share one.~~ *(corrected 2026-10-02, OPUS: two of the three are four-byte-reading artefacts - re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages, offsets ascend in slot order in all 10,287 non-empty packages, no two slots share an offset, and a slot's length is its stored size, which `0032F360` reads at `+0xC + 8k`)*

## 3. The loader contract

**The magic is never validated.** `PKFL` occurs **zero times in the entire image** — not as ASCII,
not as a little-endian dword, not byte-reversed, in any section. So there is no constant anywhere
for a `cmp eax, [rip+X]` to reference, which is the form that hides a real check from a `.text`
scan (that form is documented on [`.sab`](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md#3-the-loader-contract),
where the magic *is* checked and `.text` shows nothing). **Both the positive and the negative
pattern were tested here; this is the negative.** ~~Corrupting the first four bytes of a package is~~
~~expected to change nothing — see §6 for the limit on that expectation.~~ Corrupting bytes 1-3 changes nothing, and so does any non-zero byte 0; a zero byte 0 makes every slot read of the package return -1 *(corrected 2026-10-02, OPUS: the seven slot readers test only `cmp byte ptr [buf], 0`, e.g. `0032F260+0x13`; §7's 2026-09-18 closure)*.

**A package is addressed as `(namespace, index)`** through the resource-kind path table documented
in
[`area-nmb-index.md` §3](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md#3-the-loader-contract):
`ResourcePath_Get` (`0x002DF980`) returns `g_pathTables[namespace][index]`, 22 bytes, **with no
bound on either argument.**

**Three namespaces carry PKFL packages, and each is a fixed-width interleaved record per map:**

| ns | slot | record | maps | region variants | stride and order |
|---:|---|---|---:|---:|---|
| **5** | `+0x028` | `{ebp, mot, fpk}` | 709 | 10 | `i%3 == 0,1,2` |
| **8** | `+0x040` | `{ebp, mot, snd, vpc}` | 329 | 10 | `i%4 == 0,1,2,3` |
| **37** | `+0x128` | `{ebp, mot, snd, vpcjp}` | 329 | 2 | `i%4 == 0,1,2,3` |

**Namespaces 8 and 37 are the same 329-map set differing only in the fourth field** — `.vpc` against
`.vpcjp`. That is the whole explanation for the strict 1,809 / 1,809 pair: **one authored map list,
two namespaces, and the engine selects the namespace.**

The arithmetic checks out against the string counts in `.rdata`, which is an independent route:

```
.mot   709 x 10 (ns 5)  +  329 x 10 (ns 8)   =  7,090 + 3,290  =  10,380   measured 10,380
.snd                       329 x 10 (ns 8)   =           3,290              measured  3,290
.vpc                       329 x 10 (ns 8)   =           3,290
.vpcjp                     329 x  2 (ns 37)  =             658
.vpc + .vpcjp (the search for '.vpc' matches both)        3,948             measured  3,948
```

> **The variant multiplier is 10, measured without any initialiser extraction.** Each region variant
> emits its own full path string for the same file stem, so **distinct strings ÷ distinct stems is
> the variant count**: `.mot` 10,380 / 1,038, `.snd` 3,290 / 329, `.vpc` 3,290 / 329, `.ebp`
> 10,380 / 1,038 — **all exactly 10.0** — and `.vpcjp` 658 / 329 = **2.0**. Independently,
> `1,038 = 709 + 329`, the ns 5 and ns 8 map counts.

> **The `.fpk` count reconciles exactly, and it closes a question from another sheet.** `.fpk` has
> **7,520 strings over 924 stems** — *not* a whole multiple, so its stems do not share one
> multiplicity. They resolve as two populations:
> **709 map stems × 10 (namespace 5) + 215 area stems × 2 (namespace 21) = 7,520**, with
> `709 + 215 = 924`. Both halves land exactly.
>
> So the 7,520 `.fpk` paths that ship **zero files**
> ([St2e-Carriers README](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/README.md))
> are not authored intent: **the path is emitted for every map and every area because the record is
> three fields wide here and two fields wide there.** A `.fpk` name exists wherever a record exists,
> whether or not a file was ever meant to.

**All three namespace slots are written only by `ResourcePath_Init` and read by nobody by name** —
ten writes each to `0x0215F028` and `0x0215F040`, two to `0x0215F128`, all inside `0x002DF9A0`.
Consumers reach them through `ResourcePath_Get`, so a reference census on the slot finds no reader
and that is expected, not a finding.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | ~~—~~ byte 0 only, by the seven slot readers (`0032F260+0x13` `cmp byte ptr [rcx], 0` and its six twins) | ~~—~~ byte 0 zero: every slot read returns -1 | — | ~~**yes — `PKFL` occurs 0 times in the whole image, so no memory-operand comparison is possible either**~~ **bytes 1-3 yes, byte 0 no** - nothing compares the magic, which occurs 0 times in the image *(corrected 2026-10-02, OPUS: §7's 2026-09-18 closure)* |
| `+0x04` slotCount | not read by any function read here | — | — | — |
| `+0x08` pairs | **read (2026-09-11)**: `ActorResource_BeginManagerResourceSetLoad` (`0032FCA0`) requests exactly `0x88` bytes of a manager's `.snd` and `.mot` and `0x208` of its `.vpc` and `.vpcjp` into four per-manager tables (`022C6E98`, `022C6E70`, `022C6EE8`, `022C6EC0`; `0032FE60`–`0032FFE2`); `0032F320` returns slot `k`'s **offset** (`[table + 8k + 8]`) and `0032F360` its **size** (`[table + 8k + 0xC]`); the voice loader `003E9EF0` issues ~~`0032E620(kind, packId, dest, size)` with that offset as the request's file offset~~ `0032E620(kind, packId, dest, size, &record)` with that offset as the record's first dword *(corrected 2026-10-02, OPUS: `003E9EF0+0x36` stores the `0032F320` result at `[rsp + 0x30]`, `003E9EF0+0x64` passes `rsp + 0x30` as the fifth argument, and `0032E620+0x3D` loads it to copy the record)* | not bounded (`k` comes from the script) | — | the pair `{0, 0}` — a zero size loads nothing (`003EA011`–`003EA013`) |

> **Crossing named for FINAL-AUDIT pass 22 (FABLE, 2026-09-14).** `0032E620` has 51 raw call sites. One caller,
> `00291C80`, is filed under **Input** by the ledger, and the code does not support that label. It is a boot-time
> loader, called at `0022A4B4`, that loops `n = 0 … 9` (`00291CB0`–`00291D15`). For each `n` it:
>
> 1. queries `0024AB90(7, 0x98 + n)`;
> 2. allocates `00249810(2, result)`;
> 3. requests the file with `0032E620(7, 0x98 + n, buffer, result, &record)`, where the stack record carries the
>    callback `00291C60`;
> 4. stores the returned handle and the buffer as a 16-byte entry from `0209BEA0`.
>
> Kind 7, id `0x98` is `itemgra_c.tm2`
> ([the VBF archive page](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md)).
> This is an ordinary resource request in the same argument shape the voice loader uses, not an input dependency.

> ~~**§3 is deliberately incomplete and the sheet says so rather than padding it.** What is
> established at tier 1 is how a package is *addressed* and that its magic is *not* validated. **The
> function that walks the directory has not been found**, so what the engine does with `slotCount`
> and the offsets — whether it bounds them, what it does with a zero entry, how it computes a slot's
> length given §5 — is **not** documented. → `PROPOSED-repos-4b-13`~~
>
> **Found 2026-09-11.** The engine never walks the directory: it loads the directory's bytes as a
> block (`0x88` / `0x208`) and indexes it by slot — ~~`0032F320` for the offset, `0032F360` for the~~
> ~~size~~ the slot readers *(corrected 2026-10-02, OPUS: two readers read the `.mot` table and `0032F2C0` / `0032F2F0` / `0032F3A0` the `.snd` one; `0032F320` / `0032F360` read only the two 64-slot tables, picked by `r8d`)* — and a slot's length is **stored**, not computed. `slotCount` is not read; the slot index
> comes from the script (`voiceread`'s argument) and is bounded only by the table it indexes.
> [The voice page](../../18-Audio/the-voice-pack-slots-and-the-voice-verbs.md) §2.5 has the chain.

**The write path.** None found. Nothing in the executable emits `PKFL`.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x002DF980` | `ResourcePath_Get(ns, index)` — `g_pathTables[ns][index]`, no bounds check; table base `0x002DF983`, ns fetch `0x002DF98D`, index fetch `0x002DF991` | ✅ full body |
| `0x002DF9A0` | `ResourcePath_Init` — installs ns 5 (`0x002DFC03` and nine more), ns 8 (`0x002DFBE7` and nine more), ns 37 (`0x002DFB7E`, `0x002DFE74`) | ◐ the slot-install region |
| `0x0215F028` | `g_pathTables[5]` — `{ebp, mot, fpk}` arrays | — |
| `0x0215F040` | `g_pathTables[8]` — `{ebp, mot, snd, vpc}` arrays | — |
| `0x0215F128` | `g_pathTables[37]` — `{ebp, mot, snd, vpcjp}` arrays | — |

~~**No PKFL directory-walking function is listed here because none was found.**~~ Listed 2026-09-11:
`0032FCA0` `ActorResource_BeginManagerResourceSetLoad` (loads the four directories), `0032F320` /
`0032F360` (offset / size of slot `k` in the two 64-slot tables *(corrected 2026-10-02, OPUS: two readers read the `.mot` table and `0032F2C0` / `0032F2F0` / `0032F3A0` the `.snd` one; `0032F320` / `0032F360` read only the two 64-slot tables, picked by `r8d`)*), `003E9EF0` (the sub-file request), `0032F430` (allocates the
four per-manager directory tables at boot), `0032ED80` `ActorResource_ResetManagerLoadState`
(clears them).

## 5. Corpus survey

**Invariants — every one measured over all 10,314 packages and all ~~74,340 present offsets~~ 74,340 non-zero words of the four-byte reading.** *(corrected 2026-10-02, OPUS: under the pair reading 40,203 pairs are present; the banner below)*

| | |
|---|---|
| magic `PKFL` | **10,314 / 10,314** |
| `slotCount` ∈ {16, 64}, never mixed within an extension | **10,314 / 10,314** |
| every present offset lies inside the file | **10,314 / 10,314** |
| every present offset is **`0x10`-aligned** | ~~**74,340 / 74,340**~~ **40,203 / 40,203** pairs, offset and size alike *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)* |
| every occupied slot has its even/odd partner occupied | **10,314 / 10,314** |
| occupancy agrees with the independent frozen census | ~~**10,314 / 10,314, zero differences**~~ 10,314 / 10,314 under the four-byte reading only, **27 / 10,314** under the pair reading *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)* |

~~**Occupancy is dense and perfectly paired:**~~ **The four-byte reading's word occupancy, withdrawn below:** *(corrected 2026-10-02, OPUS: under the pair reading `.mot` slots 0-15 hold 1,539, 3,186, 1,737, 1,134, 774, 540, 378, 270, 108, 54, 54, 36, 36, 27, 18, 18 packages and `.snd` slots 0-15 hold 2,304 for 0-7, then 9, 1,809, 324, 225, 153, 99, 45, 18; re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)*

```
slot  0/1  7,407    2/3  7,380    4/5  5,445    6/7  4,320
      8/9  3,636  10/11  3,204  12/13  2,934  14/15  2,646
    16/17     54  18/19     54  20/21     36  22..27    18
```

> ### ⚠ Corrected 2026-09-11 — the survey below read pairs as single offsets
>
> Every figure in this section was measured with a 4-byte directory entry. The entry is 8 bytes —
> `{offset, size}` — so the "odd slots" below are the **sizes** of the even ones, and everything built
> on them (the even/odd pairing, the aliasing at `0x40`, the shared offsets, the 74,340 "present
> offsets", the 0 B medians) is an artefact of that reading. Re-measured over all 10,314 packages
> under the pair reading, decompressing only block 0 of each:
>
> | | |
> |---|---|
> | `{offset, size}` pairs with `8 + 8n ≤ offset` and `offset + size ≤ file` | **10,314 / 10,314 packages** |
> | pairs with exactly one of offset / size zero | **0** |
> | slots used | `.mot` and `.snd` indices 0–15; `.vpc` and `.vpcjp` indices **0–13** of 64 |
> | `.snd` | every package fills slots 0–7; slot 9 in 1,809; the "offset `0x40`" of the old reading was **14,337 sizes of `0x40` bytes** |
> | `.vpc` / `.vpcjp` | identical occupancy by slot (1,782, 945, 702, 441, 279, 180, 126, 36, 27, 27, 18, 9, 9, 9) |
> | empty packages | 27 — the same `spc_z0000.vpc` / `.vpcjp` and `evt_t0005.mot` copies |
>
> What survives: the magic, the two slot counts, the 27 empties, the first payload at `0x800`
> (now the first *pair's* offset), and the namespace record widths of §3. ~~"Offsets are not~~
> ~~ascending in slot order" was not re-measured and is not asserted.~~ *(answered: re-measured 2026-10-02 - offsets ascend in slot order in all 10,287 non-empty packages, the first at `0x800` in every one and each later payload at the next `0x800` boundary after the one before; 2026-10-02, OPUS)*

### Three things the EBP analogy gets wrong — *as first read; see the correction above*

~~**1. Offsets are not ascending in slot order — only 4,833 of 10,314.**~~ Slot index is an identity,
not a position. ~~Anything that computes a slot's length by walking slot indices in order is wrong in~~
~~more than half the corpus; lengths must be derived after sorting by offset.~~ *(corrected 2026-10-02, OPUS: four-byte-reading figures; under the pair reading offsets ascend in slot order in all 10,287 non-empty packages and a length is the stored size)*

**2. The first payload is never at the directory end.** The gap is ~~1,976 bytes in 4,356 files and~~
~~1,784 in 3,573 — the first payload usually sits at `0x800`.~~ 1,912 bytes in every non-empty 16-slot package and 1,528 in every non-empty 64-slot one, the first payload sitting at `0x800` in all 10,287 *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages; the old gaps were measured from `0x48` / `0x108`)*. ~~And in **2,268 files the smallest~~
~~present offset is `0x40`, which is *before* the 16-slot directory ends at `0x48`.**~~

**3. Slots share offsets — and that is what makes the pairing invariant true.**

**2,349 of 10,314 files have two or more slots pointing at the same offset**, overwhelmingly `.snd`
(2,268 files). Of 2,403 duplicate groups, **2,385 consist entirely of odd slots** and **2,259 point
to an offset inside the directory itself.**

The dominant case is exact and worth spelling out. In a 16-slot package the directory runs
~~`+0x08 .. +0x48`, so slot 14's offset word lives at `+0x40` and slot 15's at `+0x44`.~~ `+0x08 .. +0x88`, and `+0x40` / `+0x44` are slot 7's offset and size *(corrected 2026-10-02, OPUS: the pair `{offset, size}` of slot `k` sits at `+8 + 8k`, which every reader indexes, e.g. `0032F260+0x1B`)*. In
`alc_a0100.snd`, slots **1, 5, 7, 9, 11, 13 and 15 all carry the offset `0x40`** — they point at
slot 14's own directory entry. The bytes there are `00 40 00 00 40 00 00 00`, which is simply the
pair of directory words read as data.

> **So "every occupied slot has its even/odd partner" is true, and it is partly an artefact of that
> aliasing rather than of every partner carrying a payload.** In these files the odd partner is not
> independent data: several odd slots share one in-directory location, which reads as a canonical
> *"this half is empty"* marker — cheaper than a null, and it keeps the pair invariant intact. The
> invariant as counted is correct; **what it implies about content is weaker than it looks.** This
> qualifies the category README's headline finding rather than contradicting it.

**The same aliasing explains the census's odd-slot medians.** Computing a slot's length as the
distance to the next present offset gives an aliased slot a length of **0** — which is where the
README's `0 B` medians for slots 9, 11 and 13 come from — and gives the *last* alias in a group a
spurious ~1,984 bytes spanning the gap to the first real payload. **Neither number is a payload
size.**

**27 packages have no occupied slots at all** — every offset zero. They are `evt_t0005.mot`,
`spc_z0000.vpc` and `spc_z0000.vpcjp`, across their locale copies. A valid, empty package.

## 6. Falsification pass — 2026-09-04

| attack | result |
|---|---|
| Is the occupancy inherited or measured? | **Measured here and then cross-checked.** An independent parse of all 10,314 files agrees with the frozen census on ~~**10,314 of 10,314 paths, zero differences.**~~ 10,314 of 10,314 paths under the four-byte entry both used, and on 27 under the pair reading *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)*. |
| Is "the magic is never validated" carried by a `.text` scan alone? | **No, and that distinction is the point.** A `.text`-only scan settles nothing — `.sab`'s magic *is* checked and shows zero `.text` hits, because it is compared against an `.rdata` constant. Here the scan is **whole-image**: `PKFL` occurs **0 times in any section**, so no constant exists for that form of comparison either. That is the shape of negative the rule allows. ~~**It is still weaker than a body read**, which is why §7 keeps it open.~~ *(answered: §7 closed it 2026-09-18 by a body read of every directory reader; 2026-10-02, OPUS)* |
| Are offsets really not ascending? | ~~**4,833 / 10,314 ascending in slot-index order.**~~ **All 10,287 non-empty packages ascend** under the pair reading; 4,833 is the four-byte reading's figure *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)*. My first pass reported "7,965 ascending" — but that test sorted the offsets before comparing them, so it could only ever have detected duplicates. **The 7,965 figure was measuring something other than what it was named**, and it was re-run rather than reported. |
| Are the shared offsets a parse bug? | **No.** They are read straight from the directory words, and ~~the shared value `0x40` is independently explained: it is the byte offset of slot 14's own directory entry in a 16-slot package, and the bytes there are the slot-14/15 offset words.~~ the repeated `0x40` is a size - 14,337 `.snd` pairs have size `0x40` - and `+0x40` of a 16-slot package is slot 7's offset word *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)*. Three worked examples in §5. |
| Do the namespace record widths hold, or were they read off a few entries? | **Cross-checked against an independent quantity.** The interleave predicts `.mot` string count `709*10 + 329*10 = 10,380` and `.snd` `329*10 = 3,290`; the measured counts in `.rdata` are **10,380** and **3,290**. `.vpc`+`.vpcjp` predicts 3,948 and measures 3,948. |
| Is the **×10 region-variant count** right? `repos-1e`'s initialiser extraction found 8 arrays for namespace 8, not 10. | **Settled by a third method that needs no initialiser extraction at all: strings ÷ stems.** Every region variant emits its own full path string for the same file stem, so *distinct strings per distinct stem* **is** the variant count. Measured over the image: `.mot` **10,380 / 1,038 = 10.0**, `.snd` **3,290 / 329 = 10.0**, `.vpc` **3,290 / 329 = 10.0**, `.ebp` **10,380 / 1,038 = 10.0**, `.vpcjp` **658 / 329 = 2.0** — five exact integers. And `1,038 = 709 + 329`, the ns 5 and ns 8 map counts, independently. **The multiplier is 10**, and an extraction returning 8 arrays for namespace 8 is incomplete rather than contradictory. |
| Were the namespace figures re-derived with a walker that **cannot** commit the unbounded-walk error? | **Yes — every one of them, and they reproduce exactly.** The record widths and array counts above were originally produced by a walk I bounded by hand. They were re-run through `repos-1e`'s `walk_array`, which requires an explicit slot count (an unbounded call raises) and stops at the first slot with no file backing. Result: ns 5 → **10 arrays × 709** `{ebp, mot, fpk}` at `i%3 = 0,1,2`; ns 8 → **10 arrays × 329** `{ebp, mot, snd, vpc}`; ns 37 → **2 arrays × 329** with `vpcjp`. Unchanged. |
| Could those counts be an artefact of where the walk was cut off? | **No — but not for the reason this row first gave, which was wrong. See §8.** The anchor is *external string exhaustion*, which does not depend on a walk bound at all: `.mot` has **10,380 strings over 1,038 stems = 10.000** with `1,038 = 709 + 329`; `.snd` **3,290 / 329 = 10.000**; `.vpc` **3,290 / 329 = 10.000**; `.vpcjp` **658 / 329 = 2.000**. Every `.mot`, `.snd`, `.vpc` and `.vpcjp` string in the image is accounted for by those namespace records, none unreached. Independently, **ten separate ns 5 arrays each yield exactly 709** and ten ns 8 arrays each yield exactly 329 — a repeated exact count across independent arrays is evidence no single walk can give. |
| Did an external tool supply any of this? | **No.** No oracle reads PKFL. |

**What was tried and failed to break it.** The natural reading of a densely occupied paired
directory is that each pair is one logical item split in two, with both halves carrying data. That
predicts distinct offsets for the two halves. ~~**It fails in 2,349 files**, where the odd halves~~
~~alias one location — so the pairing is a directory-level invariant and not a content-level one.~~ *(corrected 2026-10-02, OPUS: the odd halves are sizes, so equal values are equal sizes, not a shared location - under the pair reading no two slots of any package share an offset)*

## 6b. Independent audit pass — 2026-09-05, `repos-1e`

**Method: a fresh parser against the archive, not this sheet's census.** `audit_pkfl.py` reads the
VBF index directly and decompresses only block 0 of each entry to reach the header and directory. It
**does not import `census_pkfl_container.py` and does not read `pkfl-container-census.tsv`** — an
audit that reuses the author's instrument tests transcription, not parsing. Program state: GN160
(`gzf fa0db293…`), archive `FFXII_TZA.vbf` as shipped.

**Every checkable claim reproduced** - under the same withdrawn four-byte entry *(corrected 2026-10-02, OPUS: under the pair reading 40,203 pairs are present, the smallest offset is `0x800` and offsets ascend in every non-empty package, and no two slots share an offset; §5's banner)*.

| claim | sheet | independent re-parse |
|---|---|---|
| files carrying the four extensions | 10,314 | **10,314** |
| magic `PKFL` | 10,314 / 10,314 | **10,314, 0 bad** |
| per-extension counts | 4,392 / 2,304 / 1,809 / 1,809 | **identical** |
| `slotCount` 16 for `.mot`/`.snd`, 64 for `.vpc`/`.vpcjp`, never mixed | 10,314 / 10,314 | **identical, no exceptions** |
| present offsets | 74,340 | **74,340** |
| every offset `0x10`-aligned | 74,340 / 74,340 | **74,340, 0 unaligned** |
| every offset inside the file | 10,314 / 10,314 | **74,340 inside, 0 outside** |
| every occupied slot has its even/odd partner | 10,314 / 10,314 | **10,314, 0 without** |
| files with ≥2 slots aliasing | 2,349 | **2,349** |
| duplicate groups / all-odd / in-directory | 2,403 / 2,385 / 2,259 | **2,403 / 2,385 / 2,259** |
| gap to first payload | 1,976 in 4,356; 1,784 in 3,573 | **identical** |
| smallest offset `0x40`, 16-slot files | ~~2,268~~ 0 | ~~**2,268**~~ **0** - the smallest offset is `0x800` in all 10,287 non-empty packages *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)* |
| `alc_a0100.snd` slots at `0x40` | 1, 5, 7, 9, 11, 13, 15 | **identical** |
| bytes at `+0x40` | `00 40 00 00 40 00 00 00` | **identical** |
| offsets ascending in slot order | ~~4,833 / 10,314~~ 10,287 / 10,287 non-empty | ~~**4,833**~~ **10,287** *(corrected 2026-10-02, OPUS: re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)* |
| packages with no occupied slot | 27 | **27** — `evt_t0005.mot`, `spc_z0000.vpc`, `spc_z0000.vpcjp`, 9 locale copies each, all 2,048 B |
| `PKFL` in the image | 0, any section | **0** as ASCII, LE dword, BE dword and reversed |

**Two figures appeared to disagree, and both were the auditor's error.** Recorded because the
mechanisms recur:

- **"4,833 ascending" first came out as 4,860.** My comparison was `present == sorted(present)`, and
  **the 27 empty packages have `present == []`, which is vacuously sorted.** `4,860 − 27 = 4,833`.
  *An empty set satisfies a universal claim* — the sheet's figure was right and correctly excluded
  them.
- **"2,268 files with smallest offset `0x40`" first came out as 2,286.** The sheet's sentence scopes
  itself to the 16-slot directory ending at `0x48`; 18 of the 2,286 are 64-slot files where `0x40`
  means something else. **Scoped as written, 2,268 is exact.**

**What was attacked and held.** (a) That the four extensions might differ in directory shape — they
do not; `slotCount` is a clean function of extension with no exceptions in 10,314 files. (b) That
the aliasing might be a parse artefact of my own reader — it is not; I read the raw directory words
and reproduced the worked example byte-for-byte. (c) That the pairing invariant might be inflated by
the empty packages — it is not; all 27 have *no* occupied slots, so they satisfy it trivially and do
not change the 10,314. (d) That "ascending" might hold under a different definition — strictly
ascending gives 4,851 and over all slots including zeros gives 27, so ~~**no reading makes the~~
~~directory ordered**, and §5's conclusion is stronger than the single figure carrying it.~~ *(corrected 2026-10-02, OPUS: the pair reading makes it ordered - offsets ascend in slot order in all 10,287 non-empty packages; re-parsed under the `{offset, size}` reading from `FFXII_TZA.vbf`, all 10,314 packages)*

**Not audited here:** §3's loader contract. ~~`PKFL_Bind` and the slot-consumer functions were not~~
~~read, so the *"magic never validated"* row still rests on the whole-image scan the sheet itself~~
~~flags as the weaker instrument in §7.~~ *(answered: the magic row rests on a body read since 2026-09-18 - §7, every directory reader; the loader contract itself is still unaudited; 2026-10-02, OPUS)* **The corpus half of this sheet is now independently
confirmed; the code half is not.**

## 7. What this document does not claim

- ~~**The directory-walking loader has not been found, so §3 is a partial contract.** How the engine
  bounds `slotCount`, what it does with a zero entry, and how it computes a slot's extent given the
  aliasing in §5 are all unknown. Everything above is *how a package is addressed* and *what the
  bytes are*, and no reader body backs the field table. → `PROPOSED-repos-4b-13`~~
  **SUPERSEDED by §8's 2026-09-11 correction, which this bullet outlived by three days.** The walker
  exists and is named there: `0032FCA0` requests the directory (`0x88` / `0x208`), and `0032F320` /
  `0032F360` read slot *k* at `+8 + 8k` and `+0xC + 8k`. A reader body does back the field table.
  *Found 2026-09-14 (OPUS) while auditing why this page still reads `PARTIAL`: §7 said the loader
  had not been found and §8 said it had, in the same document. `check_self_contradiction` did not
  see it - that tool matches absence claims about ADDRESSES BEING WRITTEN, not about a MECHANISM
  HAVING BEEN FOUND.*
- ~~**The magic negative rests on a whole-image scan, not a body read.** That is a weaker instrument
  than the one used for `CML1`, where the only dereferencing function was read in full. If a walker
  is found and it does compare `+0x00` against a value built by arithmetic, this claim falls.~~
  **Closed 2026-09-18 (FABLE) by a body read of every reader of the directory.** The walker `0032FCA0`
  reads each package's first `0x88` or `0x208` bytes into one of four per-manager buffer tables at
  `022C6E70` (record field +1, `0x88`, completion `003302B0`), `022C6E98` (field +2, `0x88`, completion
  `00331760`), `022C6EE8` (field +3 of namespace 8, `0x208`, completion `00331820`) and `022C6EC0`
  (field +3 of namespace 37, `0x208`, completion `003317C0`); the allocator `0032F430` gives each
  manager slot a `0x208` buffer and zeroes its first byte. The image-wide sweep for the tables'
  addresses (rip-relative and base-plus-displacement forms both) finds exactly ~~six~~ seven slot readers *(corrected 2026-10-02, OPUS: the list names seven; a grep of every reference to the four tables finds these seven, the allocator `0032F430` and the walker `0032FCA0`)*,
  `0032F260` / `0032F290` (field +1 offset and size), `0032F2C0` / `0032F2F0` / `0032F3A0` (field +2
  offset, size, and slot `k+8`'s size at `+0x4C`) and `0032F320` / `0032F360` (the two 64-slot
  tables, selected by `r8d`), and every one of them reads slot `k` at `+8 + 8k` / `+0xC + 8k` after
  one test only: `cmp byte ptr [buf], 0` and return -1 if zero. Nothing compares `+0x00` or `+0x04`
  against any value, built or loaded; ~~the two completions clear a pending bit in the manager's state~~
  ~~word (`022C6E48`, bits 14 and 15)~~ the four completions each clear one pending bit of the manager's state word `022C6E48` - `003302B0` bit 13 (`.mot`), `00331760` bit 12 (`.snd`), `00331820` bit 15 (`.vpc`), `003317C0` bit 14 (`.vpcjp`) *(corrected 2026-10-02, OPUS: `003302B0+0x20` `btr rbx, 0xd` and its three twins; the walker sets the same bits, `0032FCA0+0x20A`, `+0x277`, `+0x2E2`, `+0x34E`)* - and never touch the buffer. So the magic is never validated, but
  its first byte is load-bearing in one way: the walker writes a zero into byte 0 when it does not
  request a package (`0032FEC7`, `0032FF2D`, `0032FF98`, `00330004`), and a loaded directory is
  recognised by that byte being non-zero, which is the `P`. Corrupting the magic to any non-zero
  first byte changes nothing; zeroing byte 0 makes every slot read of that package return -1.
  Static, tier 1: the walker, the allocator, the ~~six~~ seven readers and the ~~two~~ four completions read in full *(corrected 2026-10-02, OPUS: as above)*.
- **Nothing is claimed about what any slot holds.** Slot payload semantics belong to
  `17-Presentation-Rendering` (motion) and `18-Audio` (sound, voice), per this category's README.
  ~~The even/odd pairing is described structurally and **no reading of "even = data, odd = descriptor"~~
  ~~is asserted**, though the aliasing evidence is consistent with it.~~ The second word of each pair is the slot's size, not a descriptor *(corrected 2026-10-02, OPUS: `0032F360+0x2E` reads `[table + 8k + 0xC]` as the size; the 2026-09-11 correction in §8)*.
- ~~**The 27 empty packages are reported, not explained.**~~ **Explained 2026-09-18 (FABLE), DATA from
  the archive.** They are two authored stems in every one of the nine locale roots under
  `ps2data/plan_master/<lang>/event/`: `spc_z0000.vpc` and `spc_z0000.vpcjp` (9 + 9) and
  `evt_t0005.mot` (9): each is one 2,048-byte file, `PKFL`, count word 64 or 16, and every `{offset, size}`
  pair zero, so the header and the empty directory alone, padded to the sector. The `us` scripts agree
  with the voice side: `spc_z0000.ebp` (decompiled with ff12-script) plays no voice and loads no
  motion, so its two empty voice packs are the authoring's empties for a scene without lines.
  `evt_t0005.ebp` does load and play motion (`motionread` four times, `motionplay_bb` fifty-nine) while
  its own `.mot` is empty, so what it plays is served from another package, not from this one.
- ~~**Slots 16–27 occur in 18–54 files each and were not examined separately.**~~ **Dissolved 2026-09-18
  (FABLE) under the pair reading.** The 18–54 counts were the size words of slots 8–13 read as offsets
  under the withdrawn four-byte reading (§8). Re-parsed as `{offset, size}` pairs, all 10,314 packages
  (4,392 `.mot`, 2,304 `.snd`, 1,809 `.vpc`, 1,809 `.vpcjp`) populate no slot from 16 to 27: the
  16-slot families reach slot 15 at most and the 64-slot families slot 13. DATA from the archive.
- ~~**Whether a 64-slot package uses indices above 27 is not established** — none was observed, but
  the 64-slot directory has room for them.~~ **Established 2026-09-18 (FABLE): none does.** Over all
  3,618 64-slot packages (`.vpc` and `.vpcjp`) the highest populated slot is 13; no package uses any
  index above 13, so none above 27. The 64-slot directory is authored capacity the shipped data never
  fills past its fourteenth entry, and the engine's readers (`0032F320` / `0032F360`) index it without
  a bound of their own. DATA from the archive.

## 8. Corrections

**2026-09-11 — the directory is `{offset, size}` pairs, and the walker exists.** FABLE, from the
voice-pack loader. *What was believed.* `slotCount` 4-byte offsets, directory end `0x48` / `0x108`,
lengths computed from neighbouring offsets, an even/odd pairing with odd slots aliasing an
in-directory word. *What is now established.* `0032FCA0` requests exactly `0x88` (16-slot) and
`0x208` (64-slot) bytes as the directory — eight per slot — and `0032F320` / `0032F360` read slot
`k`'s offset at `+8 + 8k` and size at `+0xC + 8k`; `nal_a0100.snd`'s directory reads
`{0x800, 0x2300}, {0x3000, 0x40}, {0x3800, 0x40} …` — the `0x40`s are sizes. All 10,314 packages
re-parsed under the pair reading: every pair in bounds, never a lone zero. *Consequence.* §2, §3 and
§5 carry the correction in place; the README's headline finding is withdrawn there; the `.sab`
sheet's "voice" pairing is unaffected. *Why it was reachable.* The old reading was consistent with
itself — every "odd offset" landed inside the file — and the census checked bounds, not meaning;
only the engine's read width settles the entry size.

**2026-09-04 — the "different bounds, identical counts" control was invalid and is withdrawn.**
`repos-4b`, after `repos-1e` tested the claim against their own arrays.

*What was believed.* §6 argued that because the walk extent is bounded by the next array's base and
therefore varies between siblings — 5,126 slots for `0x01EBF8A0` against 3,936 for the others, 4,154
for `0x01E276D0` against 2,964 — and the per-extension counts stayed at 709 and 329 regardless, the
counts must belong to the data rather than to the bound.

*What is now believed.* **The control cannot work on these arrays, and I did not check whether it
could.** It discriminates only where an array leaves slack inside its extent: you widen the bound
and watch the count fail to grow. **Measured: every one of these arrays has a headroom of zero** —
the last populated slot is the last slot before the next base, because the arrays are packed
back-to-back. Sweeping the bound wider makes the count climb immediately (`0x01E1F7D0`: 2,127 at
1× → 3,422 at 1.5× → 4,097 at 2×), because past the boundary the walk is simply counting the
neighbouring array. There is no plateau to observe.

*What was actually compared.* Not one array under two bounds, but **two different arrays that happen
to have different extents.** That the larger one also contains 709 `.mot` is a fact about its
contents, not a demonstration that the bound is irrelevant — the extra 1,190 slots hold 865 strings
of other extensions.

*What proved it.* `repos-1e` ran the control against their own ns 21 and ns 37 arrays, found them
dense to the boundary with counts still climbing at every bound, and reported that it validates my
figures but not theirs. **Checking my own arrays showed the same density, so it does not validate
mine either.**

*Why the earlier reading was reachable.* The observation was true — the counts *are* stable across
siblings — and a true observation was fitted to the wrong mechanism. **The claim was about what the
stability proves, and that is the part I did not test.**

*Consequence.* **No figure changes.** 709, 329, 321 and the ten/two array counts are unaffected;
they rest on external string exhaustion and on exact repetition across independent arrays, neither
of which depends on a walk bound. §6's row now says so. **What was withdrawn is a piece of
reasoning, not a number** — but a sheet that supports a right answer with a broken argument invites
the next reader to reuse the argument.

## 9. Related

- [`26-PKFL-Package-Container/README.md`](../README.md) — the category, the census, and the
  build-out order this sheet is step 3 of.
- [`area-nmb-index.md`](../../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/area-nmb-index.md)
  — the resource-kind path table and `ResourcePath_Get`, which address every package here.
- [`sab-sound-bank-container.md`](../../18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md)
  — the contrasting case where a magic *is* validated and a `.text` scan cannot see it.
- [`25-EBP-Script-Container`](../../25-EBP-Script-Container/README.md) — the indexed-directory idiom
  this container shares and the three ways it diverges.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** `ResourcePath_Init` (2,831 bytes), which this page cites, is called from the 978-byte core start-up root.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (18 edges through 4 of this page's functions).** The ActorEntity layer reaches this page at `0032ED80`, `0032FCA0`, `0032E620`, `002DF980`. `FUN_002628b0` is the worked example, read in full - it is a 1,689-byte manager routine that indexes `02098E10` at the **`0x288` stride** - the same records the manager indexer walks - in a `0x50`-byte frame with a stack cookie; **4 of the 15 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — CLIENT.** `FUN_002ef300`, owned by that layer, calls `0032E620` on this page. That caller is a 65-byte slot entry, and the clamp is the fact: the index is held to **`0..0xF` - sixteen slots** - before it is offset by `0x75` and paired with the size `0xE240`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (1 edge through 1 of this page's functions).** The UI layer reaches this page through the allocation arm `00249810` — a UI-side caller consults it for the (kind=2, out-result) marshalling this page's container init describes; the crossing is that the layer calls this page's function, not that this page owns anything in that layer. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-18 (SWE2-EC7).
- **Presentation — CLIENT (5 edges).** 5 inbound (Presentation bodies `003DD4C0`, `001BB2B0`, `003B53C0` call page-cited `0032E620`, `002DF980`, `0032F260`). Substantive edges include `002DF980` is called by `001BB2B0`; `0032E620` is called by `003B53C0`; `0032E620` is called by `003B2310`; `0032F260` is called by `003DD4C0`.
- **Resource — CLIENT and SERVICE (21 edges).** 11 inbound (Resource bodies `002EEEE0`, `001DA290`, `0032EB40` call page-cited `0032E620`, `002DF980`); 10 outbound (page-cited `0032F430`, `ActorResource_BeginManagerResourceSetLoad` (0032FCA0), `0024AB90` call Resource bodies `0032E620`, `0032E400`, `0032E870`). Substantive edges include `002DF980` is called by `002EEEE0`; `002DF980` is called by `001DA290`; `0032E620` is called by `0032EB40`; `0032E620` is called by `00384420`; the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DFE0` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `0050DFE0`.
- **World — CLIENT (2 edges).** 2 inbound (World bodies `00378540`, `00266D10` call page-cited `0032E620`, `0032F430`). Substantive edges include `0032E620` is called by `00378540`; `0032F430` is called by `00266D10`.
- **WorldAreaField — CLIENT and SERVICE (6 edges).** 5 inbound (WorldAreaField bodies `00379A10`, `MapRef_BeginLoadResources` (00268750), `00378030` call page-cited `0032E620`, `002DF980`, `ActorResource_BeginManagerResourceSetLoad` (0032FCA0)); 1 outbound (page-cited `0032F430` call WorldAreaField bodies `003EA6B0`). Substantive edges include `002DF980` is called by `00379A10`; `0032E620` is called by `MapRef_BeginLoadResources` (00268750); `0032E620` is called by `00378030`; `0032E620` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820).
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0050DFE0` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `0050DFE0`.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-pkfl-package-container-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `0032F320` | 55 B | returns -1 when `ecx` is above 3 (signed); otherwise takes the pointer at `022C6EC0` + `ecx`*8 when `r8d` is 0, or at `022C6EE8` + `ecx`*8 when it is non-zero, returns -1 when the first byte it points at is 0, and otherwise returns the dword at that pointer + `edx`*8 + 8 (`edx` sign-extended) | `0032F323`, `0032F334`, `0032F33E`, `0032F346`, `0032F34E` |
