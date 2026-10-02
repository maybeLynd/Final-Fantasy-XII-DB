---
system: EBP section_010 — the CML1 shake-name directory (engine name SHKCTL)
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain:Presentation.Camera
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
corpus_validated: "1115 / 1115 us .ebp scripts (1114 containers), 2026-09-03"
last_reviewed: 2026-09-12
ebp_units:
  - "section_010"
audit:
  passes: 1
  last_pass: 2026-09-05
  last_pass_state: "GN160 (gzf fa0db293…d2f708, snapshot b57264ba…d18fea34, exe 73461d08…d89721f8) — independent pass by repos-4b, author of the twin section_008: own parser over 1,114 containers + capstone read of SHKCTL_ResolveNames 0x003DD120"
  last_pass_by: repos-4b
  crossref_clean: true
  reopened_count: 1
---

# EBP section_010 — the `CML1` shake-name directory

> The lookup table that turns an authored name like `シェイク01` into the numbered slot the
> camera-shake curves live in. The engine calls this section **`SHKCTL`** — the *control* half of
> the `SHKCTL` / `SHKDAT` pair.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` scripts (1,114 real containers) |
| this unit present in | **113 (10.1 %)** |
| co-occurrence | **always with `section_011`** — 113/113, never observed alone. Also **always with `section_008` and `section_009`** (113/113), so the shake pair is a strict *subset* of the camera pair. *Not engine-enforced (BY-5, answered 2026-09-26, FABLE, Claude Opus 5.5). The ATEL registration `003306E0` gates each stream on its own lookup, and neither shake guard reads a camera guard: `SHKD` on record `rbp+0xB60` and `SHKC` on `rbp+0x500`, against `CAMC` on `rbp+0x3F0`. *(Qualified 2026-09-29, SWE2-DATA from OPUS `a31c65871`: true of the code after the body's first size query, which gates the whole body and, being a kind-`0xFF` lookup, never passes in this build.)* The shake resolver `003DD120` reads only the slot's shake list (`+0xF0`) and its own per-slot bank `02ADD980`, never the camera list `+0xD8`. In the shipped build even that lookup is gated off (`0032F3D0` returns 0, `BY-3`), so the authored index is the binding. So the subset is a property of how the files were authored (the `cml`, `cam` and `shk` formats sit side by side in the engine's format-name table), not a rule the loader applies. Control: `_index/candidates/by5-shake-camera-independence/independence.py`.* |
| size range | **64 B – 448 B, median 128 B** |
| where | 109 under `us/event/`, 4 under `us/plan_map/` |
| magic | `CML1` at `+0x00` in **113 of 113** |
| contents | **300 entries in total, 213 distinct names** |

---

## 1. What the player sees

**Nothing, directly — and that is the finding, not a gap.**

This section holds no motion, no timing and no picture. It is a small index: a list of the names a
cutscene's author gave to the camera shakes in that scene, each paired with the number of the shake
it refers to. `シェイク01` → 0. `振動02` → 1. `手ブレ01` → 2.

What it *causes* is that a cutscene can say "play the shake called `シェイク01`" instead of "play
shake number 0" — the ordinary reason authoring tools keep a name table. When the summon lands and
the camera trembles, this is the table that says which tremble was meant.

**CORRECTED 2026-09-05 — this paragraph previously said the shipped game appears never to consult
the table.** It does. At load the engine walks every entry~~, looks each **name** up in~~
~~`section_011`, and **writes the answer over the authored number**~~ and zeroes its two scratch words; the name lookup and its store over the authored number never run in the shipped build *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; §3 correction)*.

So the operative fact for a modder is the opposite of what this sheet first said, and sharper:
**~~renumbering `index` does nothing, because the engine recomputes it — but renaming a shake in~~
~~`section_011` breaks the link.~~** ~~The names are load-bearing; the numbers are not.~~ **Renumbering `index` changes which shake plays; renaming a shake in `section_011` changes nothing** *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; §3 correction)*.

## 2. The layout

**All offsets are from the start of the section body** — the byte the container's directory slot 10
points at.

### 2.1 Chunk header — 16 bytes

```struct Cml1Header base=section size=0x10
+0x00  char[4]  magic       'CML1' - bytes 43 4D 4C 31 = 0x314C4D43 little-endian
+0x04  u32      count       number of entries, 1 .. 13 observed
+0x08  u32      _reserved0  0 in 113 of 113
+0x0C  u32      _reserved1  0 in 113 of 113
```

**`CML1` is `CaMera List`, version 1** — the authoring extension `cml` sits at `0x00D109B8` in the
engine's own format-name table, next to `cam`, `shk` and `lgt`. The name is literal: this is the
camera-list chunk, and **`section_008` uses the identical magic and the identical layout** for the
camera pair. One chunk design, used twice — see §8.

### 2.2 Entry array — `count` entries, stride 16, starting at `+0x10`

```struct Cml1Entry base=record size=0x10
+0x00  u32  nameOffset  from the CHUNK start (not the entry), into the name blob
+0x04  i32  index       0-based slot in section_011's record array; -1 (0xFFFFFFFF) = bound to nothing, Shk1_FindByName's not-found return (0037DB8E)
+0x08  u32  _reserved0  0 in all 300 entries
+0x0C  u32  _reserved1  0 in all 300 entries
```

*(`+0x04` declared `i32` 2026-09-11 so that `section_008`'s fence and this one describe the one
chunk design once; the sentinel is the lookup's `or eax, -1`. OPUS-REQ-FABLE-FENCEDUP.)*

### 2.3 Name blob — immediately after the entry array

NUL-terminated Shift-JIS strings, **packed with no padding, in entry order**, starting at exactly
`0x10 + 16 * count`. Measured over all 113 files: the blob starts where that formula says and the
strings are contiguous in entry order — **113/113**. The bytes after the last string are zero out
to the container's `0x40` alignment — also **113/113**.

Names run **4 to 20 bytes**. The 213 distinct names are ordinary working labels: `シェイク01`
(shake 01, the commonest at 10 files), `振動01` (vibration 01), `手ブレ01` (handheld wobble 01),
`shake004`, `cut1_shake7`, `d2shake001`, and descriptive ones like `終始振動` ("shaking
throughout") and `デモンズ顔アップ` ("Demons face close-up").

### 2.4 The join to `section_011` — this is the whole point of the section

Entry `k` names the shake, and `entry[k].index` selects `section_011`'s record `index`. The join was
checked directly rather than assumed:

> **For every one of the 300 entries in all 113 files, the entry's name is byte-for-byte identical
> to the name in the `SHK1` record it points at.** 113/113 files, no exceptions.

That is a much stronger statement than "the counts match", and it is what makes the index field's
meaning a reading rather than a guess. Two further measurements pin it down:

- **The live indices are a permutation of `0 … liveCount-1`** in 113/113 files — every shake is
  named exactly once, and no index is used twice or skipped.
- **It is a bijection, and that is a stronger claim than a permutation.** Independently re-derived
  by `repos-c9` across the whole corpus: 300 entries, **exactly one** unbound (`0xFFFFFFFF`),
  **zero** out-of-range indices, and **no two entries in any file sharing a record index**. So
  `300 − 1 = 299`, which is exactly `section_011`'s record count. **Stated as a bijection because a
  single duplicate index, one out-of-range index, or one unmatched record would kill it** — where
  "the counts agree" survives all three.
- **The entries are in authoring order, not sorted.** 97 of 113 files happen to have their names in
  ascending byte order, which is enough to make "sorted for binary search" look true; the other 16
  are plainly unsorted (`bds_e0100.ebp` runs `合図`, `剣刺さり`, `剣刺さり2`; `mic_c0100.ebp` runs
  `振動02`, `振動01`). **A lookup over this table must be a linear scan, and the 97 are a
  coincidence of how the scenes were authored.**

## 3. The loader contract

**Section 2 says what the bytes are. This says what the engine does with them — and for this
section the answer is very nearly "nothing", which needs to be stated precisely.**

> **CORRECTED 2026-09-05.** Every row of this table previously read *"no reader found"*. That was
> wrong: `SHKCTL_ResolveNames` (`0x003DD120`) reads the chunk, and `repos-4b` found it while
> auditing this sheet. The correction trail is in §6a; the table below is the corrected reading.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | **never — the magic is not validated** | — | **yes.** `CML1` occurs **0 times in the whole 32,864,752-byte image**: 0 as the ASCII bytes, 0 as the dword `0x314C4D43`. Contrast `SHK1` in the sibling section, which occurs exactly once, as a `cmp` immediate |
| `+0x04` count | `SHKCTL_ResolveNames` `0x003DD183` | — | — | — |
| `+0x08`, `+0x0C` (chunk) | — | — | — | **no reader found by the searches in ~~§3b~~ §3, "How far 'no reader found' goes"** *(corrected 2026-10-02, OPUS: the page has no §3b)* |
| entry `+0x00` nameOffset | `0x003DD1A0` / `0x003DD1A8`, as a **signed** offset from the chunk base | — | — | — |
| entry `+0x04` index | **read — the binding.** `0x003DD230`, the shake start behind `camerashakestart_1a2` (`0x003492F0`) and `camerashakestart_1a3` (`0x00349730`), loads it at `0x003DD29F`. The store at `0x003DD1BF` is behind `0x0032F3D0`, which returns 0 in the shipped build | — | — | **no — the authored value selects the `section_011` record.** *Corrected 2026-09-12; this row read "not read — WRITTEN … the authored value is inert: it is overwritten before anything can use it".* |
| entry `+0x08`, `+0x0C` | — | — | — | **zeroed at load** (`0x003DD1C2`, `0x003DD1C6`) — authored contents cannot survive |
| name blob | `Shk1_FindByName` `0x0037DB80`, via the resolver | — | — | — |

### What the engine demonstrably does do

The section arrives as a **streamed resource under the engine's own tag `SHKCTL`** (the string at
`0x00D109F4`), registered in `FUN_003306e0` alongside its completion callback `FUN_00331610` and
pending-resource bit **`0x800`**.

`FUN_00331610` at `0x00331610` is the whole of the load-time handling, and it is 5 instructions of
substance:

1. `0x0033162E` — `and ecx, 0xf`: the low nibble of the argument is the manager index.
2. `0x00331636` — `and rdx, rax` with `rax = 0xFFFFFFF0`: the rest is the chunk pointer.
3. `0x0033163B` — `mov [r14 + rcx*8 + 0x21a6df8], rdx`: **store the pointer** into the per-manager
   array at `0x022C6DF8`. `r14` holds the image base `0x120000`.
4. `0x00331643` — `call FUN_0026d3a0`, which still has the chunk pointer in `rdx` and at
   `0x0026D3B1` stores **a second copy** into a per-manager table at `0x02098F00`, stride `0x288`.
5. `0x00331662` — `btr rdi, 0xb`: clear pending-resource bit `0x800`.

**CORRECTED.** This paragraph previously read *"No field of the chunk is read. Not the magic, not
the count, not one entry."* **That is false.** Step 4 above lists `0x00331643`; the very next call
in the same function, at **`0x00331652`**, is `call 0x3dd120` — `SHKCTL_ResolveNames`, which reads
the count, walks every entry ~~and overwrites each `index`~~ and would overwrite each `index` behind a gate that returns 0 in the shipped build *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run)*. **I disassembled that call site and
reasoned past it.** See §6a.

Teardown is ~~`FUN_0032ED70`~~ `FUN_0032ED80` (`ActorResource_ResetManagerLoadState`) *(corrected 2026-10-02, OPUS: `0x0032ED70` is four instructions that set bit 0 of the pending mask, `or qword ptr [rcx + rax*8], 1` on `022C6E48` at `0x0032ED70+0xA`; the addresses here lie in `0x0032ED80`'s body)*: `0x0032F06F` loads the pointer back, `0x0032F0A1` frees it, `0x0032F0A8`
nulls the slot. Initialisation nulls it at `0x0032F4C2`.

### How far "no reader found" goes, and exactly where it stops

**"No reader found" is not the same as "inert" unless the search that failed is named**, so here are
both searches, and the blind spot each has.

- **Search 1 — the constant.** `CML1` as bytes and as the dword `0x314C4D43`, over the whole image:
  **0 hits.** *Blind spot:* a constant can be built by arithmetic or compared as two 16-bit halves.
  This is the same blind spot that leaves the container's own `EBP2` magic unresolved, and it is
  catalogued in `COVERAGE.md`. **It is fair to say the magic is not validated by a direct compare;
  it is not fair to say no check exists in any form.**
- **Search 2 — every reference to the pointer.** All four references to `0x022C6DF8` were
  enumerated and read at the instruction level: initialise-to-null (`0x0032F4C2`), store
  (`0x0033163B`), load-and-free (`0x0032F06F`), null (`0x0032F0A8`). **None of them dereferences
  the chunk.** *Blind spot, and it is a real one:* the pointer is **copied** into a second table at
  `0x02098F00` with stride `0x288`, which is the shape of a field inside a per-manager structure. A
  reader holding that structure by pointer would access the field as `[reg + disp]`, and **no
  address-based scan can see that.** All four references to `0x02098F00` are the writing `lea`
  itself.

**A note on the method, because it cost time and will cost the next person the same.** A
conventional RIP-relative displacement scan finds **zero** references to any of these arrays. The
code addresses them image-base-relative — `lea r14, [rip - 0x21162e]` puts `0x120000` in `r14`, and
every access is then `[r14 + idx*8 + <VA - 0x120000>]`. **To find references to a data address in
this binary, scan `.text` for the raw dword `VA - 0x120000`, not for a RIP displacement.** That is
`COVERAGE.md`'s "a displacement search stops counting where a base pointer starts" blind spot, met
in the wild.

**So the honest statement is:** the magic is not directly compared anywhere; the load path parses
nothing; the two searches above found no reader; and one route out — through the copy at
`0x02098F00` — ~~is not closed. That residue is open question **PROPOSED-repos-c7-1**.~~ is closed *(answered: PROPOSED-repos-c7-1 is closed by `repos-4b`'s pass, §7, and `0x003DD230` reads entry `+0x04` at `0x003DD29F`, §3; 2026-10-02, OPUS)*.

### The one field with proven runtime meaning

`entry[k].index` is `0xFFFFFFFF` in exactly **one entry in the whole corpus**, in
`us/event/evt_t/evt_t0083.ebp`, which declares four names against three `SHK1` records.

That is not corruption, and the binary says so: the runtime shake-start function `FUN_0037d1f0` at
`0x0037D1F0` tests its shake-index argument against `-1` before using it. **`-1` is the engine's
"no shake" value**, so `evt_t0083` is a scene where an author named a shake and deliberately left it
bound to nothing — a stub that shipped. It is also the arithmetic that reconciles the corpus:
**300 entries − 1 unbound = 299 `SHK1` records.**

**The write path: there is none.** Nothing in the executable writes a `CML1` chunk; the `cml`
extension at `0x00D109B8` belongs to the offline toolchain.

> ### Audit finding, 2026-09-05 — the `index` field is OVERWRITTEN at load
>
> *Added by `repos-4b`, auditing this sheet as the author of the twin `section_008`.* This sheet
> describes `index` as *"0-based slot in `section_011`'s record array"*, which is what the authored
> value **is** — ~~but the engine does not read it.~~ **~~It recomputes it by name and stores the result~~
> ~~over the top~~**~~, exactly as its camera twin does.~~ and the engine uses it as authored: the recompute below sits behind a gate that returns 0 *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the correction after this box)*.
>
> `SHKCTL_ResolveNames` — **`0x003DD120`** — is structurally identical to `CML1_ResolveNames`
> (`0x003DA1F0`), documented for [`section_008`](section-008.md#3-the-loader-contract):
>
> ```
> blob = manager[+0xF0]                                   0x003DD12A
> reset five (u16,u16) pairs to (0, 0xFFFF)               0x003DD134 .. 0x003DD177   <- corrected 2026-10-02, OPUS - the first pair, +0x1C / +0x1E, is set to (0xFFFF, 0xFFFF) at 0x003DD134 / 0x003DD13B; the other four to (0, 0xFFFF)
> if (blob == NULL) return                                0x003DD17E
> count = blob[+0x04]                                     0x003DD183
> e     = blob + 0x10                                     0x003DD18C
> while (count--) {
>     name = blob + (i32)e[+0x00]                         0x003DD1A0, 0x003DD1A8
>     if (FUN_0032F3D0(1, name) != 0)                     0x003DD1AB
>         e[+0x04] = Shk1_FindByName(mgr[+0x28], name)    0x003DD1BA, **0x003DD1BF**
>     e[+0x08] = 0                                        0x003DD1C2
>     e[+0x0C] &= 0xFFFFFF00                              0x003DD1C6
>     e += 0x10                                           0x003DD1CA
> }
> ```
>
> `0x003DD1BF` is an unconditional `mov dword ptr [rbx + 4], eax`. `Shk1_FindByName`
> (**`0x0037DB80`**) is the `SHK1` counterpart of `CAM7_FindCameraByName`: slot bound `< 5` at
> `0x0037DB89`, per-manager stride `0x3D0` at `0x0037DB9F`, `-1` when the blob is null at
> `0x0037DBB8`. The handler reaching it is `SHKCTL_OnLoaded` (**`0x00331610`**) — blob stored at
> `0x0033163B`, resolver called at `0x00331652`, pending bit 11 cleared at `0x00331662`.
>
> **For a modder this is the operative fact: ~~renumbering `index` in `section_010` does nothing,~~
> ~~because the engine overwrites it; renaming a shake in `section_011` breaks the link.~~** renumbering `index` changes which shake plays and renaming a shake changes nothing *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run; the correction after this box)*. The
> corpus agreeing with the engine's answer — 299 of 300 indices in range, one `0xFFFFFFFF` — is what
> an offline tool running the same lookup would produce, and is **not** evidence that the field is
> read.
>
> **The two `_reserved` dwords at entry `+0x08`/`+0x0C` are likewise zeroed at load**
> (`0x003DD1C2`, `0x003DD1C6`), which is a stronger statement than "0 in all 300 entries": they are
> scratch, not constants.

> **CORRECTED 2026-09-12 (FABLE) — the resolving store above never executes in the shipped build.** The gate
> `FUN_0032F3D0(1, …)` at `0x003DD1AB` ends in `0x005C5230`, whose body is `xor eax, eax; ret`, and returns 0 for every
> kind the image passes it ([`section_008` §3, correction](section-008.md#3-the-loader-contract);
> [`census.out.txt`](../../_experiments/evidence/cml1-authored-index-binding/census.out.txt)). So **renumbering `index`
> in `section_010` changes which shake plays, and renaming a shake in `section_011` changes nothing**;
> `Shk1_FindByName` (`0x0037DB80`) is unreachable, its only call being `0x003DD1BA` inside the gated branch. The count,
> the name offsets and the zeroing of `+0x08`/`+0x0C` (`0x003DD1C2`, `0x003DD1C6`) still run. The field is read by
> `0x003DD230` at `0x003DD29F`, which hands it to `0x0037DCF0`. This sheet's §5 already found every entry's name equal
> to the record's at its index, so no shipped shake changes; what changes is which edit a modder must make.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x00331610` | `SHKCTL` stream-completion callback — the entire load-time handling of this section | ✅ full body, disassembled |
| `0x0033163B` | `mov [r14 + rcx*8 + 0x21a6df8], rdx` — the pointer store, and the only write of the primary slot | ✅ |
| `0x00331662` | `btr rdi, 0xb` — clears pending-resource bit `0x800` | ✅ |
| `0x0026D3A0` | stores the **second copy** of the pointer | ✅ full body, 5 instructions |
| `0x0026D3B1` | `mov [rcx + rax], rdx` into the table at `0x02098F00`, stride `0x288` | ✅ |
| `0x0032F06F` | teardown — loads the pointer back | ✅ |
| `0x0032F0A1` | teardown — frees the chunk | ✅ |
| `0x0032F0A8` | teardown — nulls the slot | ✅ |
| `0x0032F4C2` | initialisation — nulls the slot | ✅ |
| `0x0037D1F0` | runtime shake start; **tests the shake index against `-1`** | ✅ entry and index test |
| `0x003306E0` | `atelload` registration — pairs the `SHKCTL` tag, the callback and mask bit `0x800` | partial — the `SHKCTL` registration block only; **never runs in this build** - the whole body sits behind its first size query, a kind-`0xFF` lookup that returns -1 (`00330F7D jle 003315E7`; OPUS `a31c65871`, 2026-09-29) |
| `0x022C6DF8` | per-manager `SHKCTL` chunk pointer, 8-byte stride | data |
| `0x02098F00` | the second copy, stride `0x288` | data |
| `0x00D109F4` | the tag string `SHKCTL` | data |
| `0x00D109B8` | the toolchain extension string `cml` | data |

## 5. Corpus survey

**Invariants — every one measured over all 113 files.**

| | |
|---|---|
| `CML1` magic at `+0x00` | **113 / 113** |
| `+0x08` and `+0x0C` zero | **113 / 113** |
| entry `+0x08` and `+0x0C` zero | **300 / 300 entries** |
| name blob starts at `0x10 + 16 * count`, strings contiguous in entry order | **113 / 113** |
| bytes after the last name are zero to the `0x40` boundary | **113 / 113** |
| live indices are a permutation of `0 … liveCount-1` | **113 / 113** |
| **entry name == `section_011` record\[index\] name** | **113 / 113 files, 300 / 300 entries** |
| entry count equals `section_011`'s `recordCount` | **112 / 113** — the one exception is the unbound entry |

**What varies.** 1–13 entries per file; 50 of the 113 files have exactly one. 300 entries carry only
213 distinct names, so names are reused across scenes — `シェイク01` appears in 10 files, `シェイクc4`
in 9, `shake004` and `shake003` in 6 each. Sizes are small and tightly clustered: 64–448 bytes,
median 128.

**Outliers, each worth its own line:**

- **`evt_t0083.ebp` carries the corpus's only `0xFFFFFFFF` index** — see §3.
- **16 of 113 files have names out of byte order.** Easy to miss, and the reason this sheet does not
  describe the table as sorted. `rsn_z0201.ebp` interleaves `カット１・振動` and `終始振動` among
  `cut_04` … `cut_09`.
- **Names are Shift-JIS, not ASCII**, and mixed within a single file — `dgl_g0103.ebp` runs
  `shake001`, `shake004`, `d2shake001` while `dgl_h0100.ebp` runs `光輪通過１`, `光輪通過２`,
  `ハシュ着地`. A reader that assumes ASCII will mangle roughly half the corpus.

## 6. Falsification pass — 2026-09-03, and independent audit — 2026-09-05

> **Independent audit, `repos-4b`, 2026-09-05 — every corpus claim reproduced; one omission found.**
> Re-derived with an own parser over all 1,114 containers: **113** files carry the section, **300**
> entries, `count` **1..13**, both entry `_reserved` dwords zero in **300/300**, the name blob starts
> at exactly `0x10 + 16*count` in **113/113**, name offsets ascend in entry order in **113/113**,
> trailing bytes zero in **113/113**, names **4..20** bytes, and **299 of 300** `index` values fall
> inside `section_011`'s `recordCount` with **one** `0xFFFFFFFF` and **zero** out of range.
> **Nothing in §2 or §5 moved.** The omission is the write-back documented above §4.
>
> **What I attacked and failed to break.** (1) That `index` might be out of range somewhere in the
> corpus — it never is. (2) That the name blob might not be contiguous in some file — it is in all
> 113. (3) **That `section_011`'s `+0x04` is a `u32`** — my first range test read it that way and
> produced nonsense (393,217 as a "record count"). **`section-011` had already got this right**:
> `+0x04`/`+0x06` are two `u16`s, proven there from two different-width reads. *The sheet was
> correct and my instrument was wrong*, which is worth recording as an audit outcome in its own
> right.

| attack | result |
|---|---|
| Is the entry table sorted by name for binary search? | **No.** 97 of 113 files are in ascending byte order, which is exactly enough to make the hypothesis look confirmed on a sample. 16 files are not. **The 97 are a coincidence of authoring order**, and the hypothesis was dropped rather than qualified. |
| Is `entry[k].index` just a running index `k`? | **No.** It is a permutation. The first pass asserted `index == k` and produced 147 "anomalies" across 15 files — the assertion was wrong, not the data. Corrected to "permutation of `0 … liveCount-1`", which then held 113/113. |
| Does the name→record join hold, or do only the counts match? | **The join was checked directly, name by name: 300/300 entries.** The README warns that *a count match is suggestive, not deciding*, and a count match is all that was available before this test. It is not what this sheet rests on. |
| Is `0xFFFFFFFF` corruption or a sentinel? | **A sentinel.** `FUN_0037d1f0` tests the shake index against `-1` before use. The corpus alone could not have decided this; the instruction does. |
| Is the magic really unvalidated, or did the search miss it? | **Neither claim is made beyond what the search supports.** 0 occurrences of the constant is a fact; "no check exists in any form" is not, and §3 names the arithmetic-constant blind spot rather than papering over it. |
| Is the section really never parsed? | ~~**Not established, and deliberately not claimed.**~~ *(answered: it is read — `SHKCTL_ResolveNames` walks it at load and `0x003DD230` reads entry `+0x04` at `0x003DD29F`, §3 and §6a; 2026-10-02, OPUS)* Two searches found no reader; one route — the pointer copy at `0x02098F00` into a `0x288`-stride structure — is open, and address-based scanning is structurally blind to it. Recorded as PROPOSED-repos-c7-1 rather than written up as an inert section. |
| Could the decompiler have invented a value? | Ghidra renders `FUN_00331610` with **empty `if` bodies**, which would have hidden a parse if one existed. Every address cited here was taken from the **disassembly** instead. |
| Did an external tool supply any of this? | **No.** `ff12-script` was not consulted for this section, before or after. |
| Was the peer session's independent reading used as evidence? | `repos-c9` independently reported the `CML1` magic and its 0 occurrences in the image, matching this sheet. **Corroboration only** — both facts were re-derived here from the census and the binary. |

### Correction, 2026-09-04 — two citations were mid-instruction

**Two addresses in this sheet were not instruction boundaries and have been corrected.** Found by
running the citation check the gate could not run (see below), after `repos-c9` warned that an
address taken from a displacement scan by a fixed back-off is not an instruction start.

| was | is | the real instruction |
|---|---|---|
| `0x0032F073` | **`0x0032F06F`** | `mov rbx, qword ptr [r14 + rdi*8 + 0x21a6df8]` — cited address was **+4** into it |
| `0x0033163F` | **`0x0033163B`** | `mov qword ptr [r14 + rcx*8 + 0x21a6df8], rdx` — cited address was **+4** into it |

**Why the error was reachable, which is the part worth keeping.** Both came from the raw-dword scan
described in §3 — the one that finds image-base-relative references by searching `.text` for the
literal `VA − 0x120000`. **That scan reports the position of the displacement, not the position of
the instruction**, and the two differ by however many bytes of opcode and ModRM precede the
displacement — which is *not a constant*. Every address in this sheet that came from the
disassembler was already correct; every address that came from the scan was wrong by exactly the
prefix length. §4 already carried `0x0033163B` correctly from the disassembly while §3 carried
`0x0033163F` from the scan, so **the document described one instruction two ways** — precisely the
defect the citation gate exists to catch, in a document the gate could not see.

> **A displacement scan locates a field reference. It does not locate an instruction.** Converting
> one to the other requires decoding backwards from a known boundary, not subtracting a constant.

`section-011.md` was checked the same way and is clean — **32 of 32** cited `.text` addresses are
instruction boundaries — because its addresses were taken from the disassembly throughout.

**The killer observation for the central claim.** The claim is *"`entry[k].index` selects
`section_011`'s record and the pair is a name directory over a curve bank."* It would be false if
any entry's name disagreed with the record it points at. That is exactly what was tested, on all 300
entries. One mismatch kills it; there are none — and the one entry that *cannot* be tested is the
one carrying `-1`, which the binary independently shows is the "no shake" sentinel.

## 6a. Correction, 2026-09-05 — "no reader found" was wrong, and I had disassembled the disproof

**What was believed.** That nothing in the shipped executable reads this section. §3 carried
*"no reader found"* on every field, §1 said the game *"appears never to consult it"*, and §7 offered
that the whole section is probably inert and freely editable.

**What is now believed.** `SHKCTL_ResolveNames` (`0x003DD120`) reads the chunk at load: it takes the
count from `+0x04`, walks all `count` entries at stride `0x10`, resolves each entry's **name** through
`Shk1_FindByName` (`0x0037DB80`), and writes the result over the entry's `index` field. The authored
`index` is overwritten; the two `_reserved` dwords are zeroed. **The names are load-bearing and the
numbers are not** — the reverse of what this sheet first implied. *(Reversed again 2026-09-12: the store is behind a gate that returns 0 in the shipped build, so the numbers bind and the names do not — §3 correction. The call at `0x00331652` is real; what it does to `index` is nothing.)*

**What proved it.** `repos-4b`'s independent audit pass, made as the author of the twin
`section_008`, which carries the structurally identical `CML1_ResolveNames` (`0x003DA1F0`). Their
finding is quoted in full above.

**Why the earlier reading was reachable — and why that excuse does not cover it.** My two searches
were sound and their blind spots were correctly named: the constant scan found nothing because the
magic genuinely is not compared, and the pointer-slot scan found only store/free/null because
nothing dereferences that slot. Both negatives were true.

**But the reader was never behind either blind spot.** It is called directly from the function I
disassembled and described:

```
0x0033163B  mov  [r14 + rcx*8 + 0x21a6df8], rdx     <- I documented this store
0x00331643  call 0x26d3a0                            <- I documented this call
0x0033164A  call 0x263ff0
0x00331652  call 0x3dd120                            <- SHKCTL_ResolveNames. I saw it and passed over it
0x00331662  btr  rdi, 0xb                            <- I documented this
```

I described `FUN_00331610` as *"5 instructions of substance"* and listed four of the five lines
above, **skipping only the one that reads the chunk.** I had noted `call 0x3dd120` in my own notes
as *"receives the manager struct, not the chunk"* — an inference from the argument register, never
checked by reading the callee. **One `sed` of forty bytes at `0x003DD120` would have settled it.**

> **This is the third time in two days that I have published a negative while holding the evidence
> that refutes it** — after reading `in` paths inside the `uk` array and calling them walk leakage,
> and after testing a regex against my own house style. The common step is the same each time: **an
> inference about a piece of evidence was allowed to stand in for reading it.**
>
> A named blind spot is not a licence. *"No reader found by search X and search Y"* is only honest
> if nothing outside X and Y was in front of me — and here a call instruction was, in a listing I
> had already printed. **The failure was not the searches; it was calling the job done while an
> unread callee sat in the middle of the function I was describing.**

**What this does not change.** The corpus reading in §2 stands entirely, and `repos-4b` re-derived
it independently over 1,114 containers. The magic still is not validated — 0 occurrences remains
correct. The bijection still holds. **What changed is the direction of the arrow: the table is not a
leftover the engine ignores, it is an input the engine ~~consumes and then overwrites~~ consumes as authored — the overwrite never runs in the shipped build.** *(corrected 2026-10-02, OPUS: `0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = `xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run)*

## 7. What this document does not claim

> **RETRACTED 2026-09-12 (FABLE) — the CA-1 answer that follows misread its base.** `[actor + 0xB8]` is the actor
> record's `contextPtr`, the embedded **movement context** at record `+0x120`, not the actor-manager slot; that
> context's `+0xF0` is `steeringCursor`, an interior pointer to the current steering record (stored at `0x00269FAC`;
> both rows in `_types/fields.tsv`). So `00263230` and `002693D0` touch a steering record's `+0x62`, `+0x28` and
> `+0x65`, not this chunk, and the "live per-actor state" reading is withdrawn. The manager slot's `+0xF0`
> (`02098F00` = `02098E10 + 0xF0`) is still this chunk's second copy, and it has **two** readers: `SHKCTL_ResolveNames`
> (`0x003DD120`) and **`0x003DD230`**, the shake start, which reads entry `+0x04` at `0x003DD29F`. "Not inert" survives
> on that evidence; the evidence below does not.

> **CA-1 answered 2026-09-12 (FABLE): ~~the `CML1` chunk is read — through the per-record copy, for~~
> ~~kind-3 actors.~~** *(corrected 2026-10-02, OPUS: retracted above, and the bytes agree — `rbx` in `00263230` is an actor from `003588B0` (the manager slot's actor array `[slot + 8]`), and `00266B18`–`00266B2D` set actor `+0xB8` = actor `+0x120`, so `[[actor + 0xB8] + 0xF0]` at `0026338F`–`0026339D` and `00269441`–`00269453` is not this chunk)* The second pointer copy at `02098F00` (stride `0x288`) is actor storage record
> **`+0xF0`** (`02098E10 + 0xF0`), and two functions read it through the record: `00263230`, the
> mode-1 path of `ActorResource_StartEntryScriptExecution`, which for an actor whose kind byte masks
> to `0x60` loads `[[actor + 0xB8] + 0xF0]` and **sets bit 7 of chunk `+0x62`** (`0026338F`–`0026339D`)
> as the script starts; and `002693D0` (called from `ActorSystem_ReleaseManagerReco…`, `00269530`
> and `0026C5D0`), which for the same kind reads and **clears chunk `+0x28`** (`00269448`–`00269453`)
> and tests chunk `+0x65` to decide a `002EBE50` / `002E8EE0` teardown (`0026945B`–`00269478`). So the
> ~~shake directory is live per-actor state for kind-3 actors — a script-start flag and a release-time~~
> ~~counter live inside it —~~ *(corrected 2026-10-02, OPUS: not this chunk — the retraction above)* and the section is not `Inert`; the constant and the global's four direct
> references were the wrong instruments because the readers go through a structure field, as the
> row anticipated. What the fields at `+0x28`, `+0x62` and `+0x65` mean in shake terms is the residue.


- ~~*That the section is inert.*~~ **WITHDRAWN 2026-09-05.** The section is read:
  `SHKCTL_ResolveNames` (`0x003DD120`). What is inert is narrower and now stated in §3 —
  **the authored `index` value**, which the engine was believed to overwrite *(2026-09-12: it does not in the shipped build, and the value binds — §3 correction)*, and the two `_reserved` dwords,
  which it zeroes. **PROPOSED-repos-c7-1 is CLOSED** by `repos-4b`'s pass.
- **That the `CML1` magic is unchecked in every form.** 0 occurrences of the constant is what was
  measured. An arithmetic or split-half comparison would not appear in that search.
- **What `+0x08` and `+0x0C` were for.** Zero in every file and every entry, and no reader found.
  They are almost certainly the same reserved words the container header carries at the same
  offsets, but "almost certainly" is not a reading.
- **Whether the two pointer copies have different lifetimes or different owners.** Both are written
  at load and only the first is demonstrably freed at teardown. The second was not traced.
- **Why 213 distinct names are spread over 300 entries in a way that reuses some heavily.** An
  authoring-convention observation, not an engine fact.
- **How `section_000` bytecode actually names a shake.** If the resolution really is baked at
  compile time, the compiled form is in the bytecode and that is `section_000`'s sheet to write, not
  this one.

## 8. Related

- [`section-011.md`](section-011.md) — `SHKDAT`, the curve bank this table indexes. The two are one
  mechanism in two sections and neither is legible alone.
- `section-008.md` — **the same `CML1` chunk format, at a different slot.** `section_008` is
  `CAMCTL` and carries `CML1` in all 423 files that have it, exactly as `section_010` carries it in
  all 113. The CTL/DAT split is one design used twice: `CAMCTL`/`CAMDAT` for cameras,
  `SHKCTL`/`SHKDAT` for shakes. **Whoever writes `section-008.md` should expect this layout to hold
  there and should test it rather than assume it** — the corpus can answer it in one pass.
- `section-009.md` — `CAMDAT`, the `CAM7` camera bank. Its loader at `0x002561C0` is the sibling of
  the `SHK1` loader and, unlike this section, it **does** parse its control data, copying record
  names with `strncpy(…, 0x18)`.
- [`../README.md`](../README.md) — the `EBP2` container and the section directory.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Presentation — SERVICE and CLIENT.** Cited functions call Presentation bodies of 170 and 498 bytes, and one (712 bytes) is called by a 285-byte Presentation body.
- **CombatAction — CLIENT.** `BattleAction_InitializeGlobalSpecialSequenceMode` calls a 16-byte function this page cites.
- **RNG_Random_Selection — SERVICE.** A 712-byte function this page cites draws from `RNG_MT19937_NextFloatClosed`.
- **CoreRuntimeScheduling — SERVICE.** The same 712-byte function calls a 27-byte core helper.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**Party — SERVICE.** `00263230` on this page calls `PartyFocus_GetCurrentPackedActorHandle`, owned by that layer. What it reaches is a seven-byte getter returning the packed handle at `022C7FE0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Audio — MECHANICAL (SWE2-EC7-35, 1 edge).** `001EDDA0` — the shared callee this page cites inside `0037D1F0` — is called by a body on the Audio layer. Shared-helper fan-in; no audio relationship to the section.

**UI — MECHANICAL (SWE2-EC7-35, 1 edge).** `001EDDA0` is also called by a body on the UI layer. Same shared-helper fan-in.
- **ActorEntity — CLIENT and SERVICE (39 edges).** 20 inbound (ActorEntity bodies `002693D0`, `0026C5D0`, `00331610` call page-cited `002E8EE0`, `002EBE50`, `002693D0`); 19 outbound (page-cited `0026C5D0`, `002693D0`, `003306E0` call ActorEntity bodies `002693D0`, `ActorHandle_ResolveRegistryEntryByPackedId` (003588B0), `0035AE10`). Substantive edges include `002561C0` is called by `0032FAC0`; `002561C0` is called by `003306E0`; `00263230` is called by `ActorResource_StartEntryScriptExecution` (003DBDC0); `00263230` calls `0035AE10`; the remaining edges run through shared helpers the page cites.
- **Input — SERVICE (1 edge).** 1 outbound (page-cited `00263230` call Input bodies `00226BE0`). Substantive edges include `00263230` calls `00226BE0`.
- **Movement — CLIENT and SERVICE (24 edges).** 9 inbound (Movement bodies `0026C120`, `WorldActor_UpdateRuntimeAndScriptExecutionState` (0025DF00), `002E64E0` call page-cited `002E8EE0`, `002EBE50`, `001EDDA0`); 15 outbound (page-cited `00263230`, `002693D0`, `0026C5D0` call Movement bodies `002EBE50`, `Movement_SetRequestedSpeed` (0026D6F0), `002EC380`). Substantive edges include `00263230` calls `002EC380`; `00263230` calls `002EC2C0`; `00263230` calls `002EAB80`; `00263230` calls `002EBFA0`; the remaining edges run through shared helpers the page cites.
- **Resource — MECHANICAL (1 edge).** 1 call from page-cited bodies into shared Resource plumbing (`0032E400`) - the helpers' general call surface, not a Resource relationship of this page's subjects.
- **WorldAreaField — CLIENT and SERVICE (3 edges).** 1 inbound (WorldAreaField bodies `00378A60` call page-cited `0032F3D0`); 2 outbound (page-cited `00263230`, `0026C5D0` call WorldAreaField bodies `00377700`). Substantive edges include `00263230` calls `00377700`; `0026C5D0` calls `00377700`; `0032F3D0` is called by `00378A60`.
## SWE2-EC7-35 update (2026-09-19) - `0037D1F0`

`0037D1F0` (712 B) is an EBP script-section body - `02ADD990`/`02ADD980`/`01DFE0BC`/`01CEBB70`, nine `00379CE0` plus eight `00861F0E`, `0037D130`/`001EDDA0`. Interior anchor `0037D27C` (an `00379CE0` call).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-section-010-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00269530` | 105 B | for each of the four qwords at `0209A1F0` whose object has byte `+0x18` equal to 1, takes `q = 003587C0(byte +0x19 sign-extended, word +0x1A)` and calls `002693D0(q, 1)` when `q` is non-null and differs from that object | `0026954E`, `00269556`, `00269564`, `0026956E`, `0026957B` |
