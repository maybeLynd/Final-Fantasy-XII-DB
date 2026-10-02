---
system: EBP2 script container — the header and section directory of every `.ebp` file
category: 25-EBP-Script-Container
status: AUDITED
owner_layer: CodeDomain — the loader is owned by PrimaryOwner:ActorEntity; the format itself is not a function
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
corpus_validated: "1115 / 1115 us .ebp files (1114 containers + 1 non-container), 2026-09-03"
last_reviewed: 2026-09-12
archive_formats:
  - "ebp"
ebp_units:
  - "container"
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: GN160-repos-1e-falsification-1
  crossref_clean: true
  crossref_checked: null
  crossref_report: null
  reopened_count: 0
---

# The EBP2 script container

> Every `.ebp` file is a **directory of up to 20 numbered sections**, and the engine reads that
> directory with exactly one function. This sheet documents the wrapper; the sections themselves
> have their own sheets.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,115 of 1,115** `us` `.ebp` files |
| containers among them | **1,114** — one file is not a container (§5) |
| this unit present in | 1,114 (100 % of containers, by definition) |
| size range | 640 B – 1.06 MB; the directory is always exactly 0x60 B and the payload always starts at 0x80 |
| section offsets seen | **5,419**, every one `0x40`-aligned |

Two independent censuses agree on the occupancy figures: an external unpacker's, and a re-derivation
from the container's own directory (this sheet's, run 2026-09-03). **A scored denominator that two
readings agree on is worth much more than one nobody re-checked.**

---

## 1. What the player sees

**Nothing directly — and everything indirectly.**

`.ebp` is the file FFXII's *behaviour* is written in. One file per map or cutscene: the guards that
walk a patrol in Rabanastre, the chest that holds a Potion, the door that will not open until you
have the right key item, the chance of a sandstorm in the Westersand, the camera that swings around
Vaan during a cutscene. **1,115 of them per language, nine languages, 10,045 files in the archive.**

This document is about the **wrapper** around all that — the first 128 bytes of the file, which say
*which kinds of content this particular map uses and where each kind starts*. A modder who wants to
change a spawn table or a weather chance has to get past this header first, and the two facts that
matter most are in §3: **the `EBP2` magic is never checked, and six of the twenty slots are wired to
nothing.**

## 2. The layout

Offsets from the **start of the file**.

```struct EbpContainerHeader base=file size=0x60
+0x00  u32      magic       'EBP2' (45 42 50 32) — never read by the engine, see §3
+0x04  u32      slotCount   0x14 = 20 — the directory bound, and it IS enforced
+0x08  u32      _reserved0  0 in 1,114 of 1,114 — never read
+0x0C  u32      _reserved1  0 in 1,114 of 1,114 — never read
+0x10  u32[20]  sectionOff  INDEXED BY section number, 0 = absent, file-relative
```

The directory ends at `0x60`; the payload begins at `0x80`. **The 32 bytes between are not part of
this struct** — they are alignment padding, settled in §5.

**The directory is indexed, not packed.** Slot `n` is at `+0x10 + 4*n`, and the value is a
**file-relative** byte offset. That single fact explains the whole sparse numbering: `001`, `005`,
`007`, `013`, `015`, `017` and `018` are not "missing sections", they are **slots that are always
zero**. A packed list would have made those indices unobservable.

> **BW-1 answered 2026-09-12 (FABLE): the always-zero slots are zero in every language tree.** A
> census of every `.ebp` in `FFXII_TZA.vbf` — 10,045 entries, of which 10,036 are `EBP2`
> containers across the nine trees `us`, `kr`, `it`, `in`, `fr`, `es`, `de`, `cn`, `ch` (the nine
> non-containers are the known `evt_t0020` outlier, once per tree) — finds slot **17** non-zero in
> **0** files, and likewise slots 1, 5, 7, 13, 15 and 18. `section_017`'s live handler (`FUN_00332110`
> at `00330630`) is authored capacity no shipped language uses; the same shape as the `NOT USED`
> battle-command markers and the inert VM opcodes.

**Section length is not stored.** A section runs from its own offset to the **next present offset**,
and the last section runs to EOF. A truncated file therefore yields a silently short final section
rather than an error — nothing in the engine cross-checks a section's extent. (`section_000` happens
to carry its own length at *its* `+0x04`; that is a property of that section, not of the container —
see [`section-000-bytecode.md`](../Bytecode-And-Opcodes/section-000-bytecode.md).)

## 3. The loader contract

**One function reads this directory:**
**`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources`, `0x003304A0`, 570 bytes.**

It is the completion callback of the file read, and the path to it has no branches — each step is
the *only* caller of the next:

```
WorldSimulation_ProcessDeferredModeRequest      0x0032FC30
  → ActorResource_BeginManagerResourceSetLoad   0x0032FCA0
    → ActorResource_BeginPrimaryPayloadLoad     0x00330310
        size = FUN_0032e400(ns, idx)                   -- the file's own size
        buf  = FUN_0036a100(size)                      -- one ARENA allocation, whole file (corrected 2026-09-12)
        buf  = FUN_0036c660(buf, name, 0x95C)          -- tags the block header; returns buf (003303AD)
        FUN_0032e620(ns, idx, buf, size, ctx)          -- async read; completion callback =
      → ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources   0x003304A0
```

**The whole file is read in one shot at its natural size.** There is no streaming, no per-section
read, and nothing that could reject a file for being the wrong kind.

### Which resource namespace, and the per-namespace index stride

`.ebp` is not opened by name. It is requested as a **`(namespace, index)`** pair through the same
resolver the `.ard` carrier uses — `ResourcePath_Get`, `0x002DF980`, which returns
`pathTables[namespace][index]`. `ActorResource_BeginManagerResourceSetLoad` picks both from the
manager index (`edi`) in one three-way branch at `0x0032FD19`–`0x0032FD44`:

| manager index | namespace | index expression | instruction |
|---:|---:|---|---|
| `<= 0` | **5** | `id * 3` | `0032FD44 lea ebp, [r15 + r15*2]` |
| `1 – 3` | **8** | `id * 4` | `0032FD35 lea ebp, [r15*4]` |
| `4` | **1** | **`id + 0x6B`** | `0032FD2A lea ebp, [r15 + 0x6b]` |

**The index is an affine function of the id — multiplier, addend, or both — chosen per namespace by
the requesting code.** Two of these branches multiply; **the third only adds.** Namespace 21's
`.ard` table is the multiplier case at ×2, where `{ardPath, fpkPath}` at `2i` and `2i+1` reads from
the corpus as a 16-byte record.

> **The addend is the dangerous half, and it is the one that ships.** A multiplier at least leaves a
> visible interleave — two extensions alternating is exactly how the `.ard`/`.fpk` parity gave
> itself away. **An addend leaves no trace whatsoever: a flat array is byte-identical under `id + 0`
> and `id + 0x6B`.** No inspection of the array can recover it.

**So an index expression cannot be read out of an array at all** — not the multiplier, and
especially not the addend. It is knowable only from the requesting code. *(This correction is a
neighbouring session's: the first version of this paragraph said "the index is scaled", which is
false for the `0032FD2A` branch, and then inferred a stride for a third namespace from the shape of
its array — the exact inference the paragraph forbids.)*

### Namespace 37 is an override, and it completes the set

The same function consults a **fourth** namespace, `0x25` = 37, and only for one manager range:

```asm
0032FDB9  lea  eax, [rdi - 1]      ; rdi = manager index
0032FDBC  cmp  eax, 2
0032FDBF  ja   0x32fdf1            ; not 1..3 -> keep the primary size
0032FDC1  lea  eax, [rbp + 3]      ; the same index for both probes
0032FDC4  mov  ecx, esi            ; the primary namespace (8 here)
0032FDCC  call 0x32e400            ; Resource_GetSize(primary, idx)
0032FDD9  mov  r12d, eax           ;   kept only for the skip path   <- corrected 2026-10-02, OPUS - in the image this follows 0032FDD4 (0032FDD1 mov rdx, rbx; 0032FDD4 mov ecx, 0x25; 0032FDD9 mov r12d, eax)
0032FDD4  mov  ecx, 0x25           ; namespace 37
0032FDDC  call 0x32e400            ; Resource_GetSize(37, idx) -- SAME index
0032FDE8  mov  [rsp + 0xb0], eax   ; the ns-37 answer WINS
0032FDF1  mov  [rsp + 0xb0], r12d  ; (skip path: the primary answer)
```

**For manager indices 1–3 the size is taken from namespace 37 in place of namespace 8**, at the same
index; every other manager keeps its primary namespace. The primary probe's result is computed and
then discarded on that path.

**Namespace 37 is a fully populated parallel table, and its layout is identical to namespace 8's.**

An array's **extent** is taken as the distance to the next base in address order, over all **83**
path-table bases recovered from `FUN_002DF9A0`'s own stores — 2,964 slots for each namespace-37
array, 642 for each namespace-21 array. Within those bounds:

| namespace | base | entries | first index | `index mod 4` → extension |
|---:|---|---:|---:|---|
| 37 | `0x01EA4D00` (ch) | **1,316** | 120 | 0 `.ebp` · 1 `.mot` · 2 `.snd` · 3 `.vpcjp` — **329 each, no exceptions** |
| 37 | `0x01ECBCF0` (in) | **1,316** | 120 | identical |
| 21 | `0x01E0CFA0` (ch) | 430 | 24 | `.ard` 215 even · `.fpk` 215 odd |
| 21 | `0x01EDC280` (in) | 430 | 24 | identical |

**329 logical ids × 4 assets each — exactly the `index = id * 4` rule namespace 8 uses.** That
structural identity is *why* 37 can be substituted for 8 at the same index: same stride, same slot
meanings, different content. An override must have the overridden table's shape, and it does.

> **Two corrections, both recorded rather than quietly folded in.**
>
> **(1)** An earlier draft called 37 *"not a separate content kind"*. False — it has 1,316 real
> paths. A neighbouring session independently reported both arrays as **empty**, which is the
> *sparse-head* error a third time: the first 120 slots are NULL, so a head-only read returns zeros.
> The override reading was never at risk; only the "no content" half was.
>
> **(2)** That same draft counted **2,168** and **1,972** entries and described the `ch` array as
> *mixed*, carrying `ca`/`bin`/`tm2` alongside the four asset types. **Both were artefacts of
> scanning past the array's end** — I had used a fixed 4,000-slot window instead of a derived
> extent, and the surplus was the *neighbouring* array read as if it were this one. Bounded properly
> the table is **1,316 entries and perfectly clean in both trees.** The peer's independently derived
> 1,316 and this one agree exactly.
>
> **This is the span-is-not-a-structure error again, in its third costume** — after the README's
> "table span" and my own inbound-pointer range. *Where an array ends is not observable from the
> array;* it has to come from the next base. **And the extent rule is only as good as the base set
> is complete** — 83 bases here, and completeness is not proven, so a tighter base set could shrink
> these bounds further. The **parity partition and the "not empty" result are robust to the extent
> rule; the totals are not.**
>
> **6 of the 83 hold no path at all, and they are explained rather than discarded.** `.data` is
> file-backed only to RVA `0x01E5E400` (VA `0x01F7E400`); above that it is uninitialized and zero at
> load. All six — `0x0215EFF8`, `0x0215F148`, `0x0215F150`, `0x0215F158`, `0x0215F160`,
> `0x0215F168` — lie in that tail, **as does the selector block `0x0215F000` itself, which is why
> `FUN_002DF9A0` exists at all: it populates a zero-initialized pointer array at runtime.** So those
> six are real stores pointing at empty tables, **not extraction artefacts.**
>
> **That gives a cheap discriminator for anyone recovering these bases:** a base above
> `0x01F7E400` cannot hold file-backed path strings, so "no entries" there means *empty by
> construction*, not *mis-paired `lea`*. A base **below** it with no entries would be the suspicious
> case. **77 of the 83 are file-backed and every one of those resolves.** A second session applied
> the same test to their independently recovered 94 and got **88 file-backed, all resolving, and the
> same six above the boundary — the identical six addresses.** Neither extractor has a mis-pairing
> problem.
>
> **This is also why the base must come from the initialiser, and it is a stronger reason than
> "be careful".** The selector array is in uninitialized `.data`, so **the image contains no address
> for it at all** — `FUN_002DF9A0` is not a convenience that happens to record the bases, it is
> **the only thing that ever puts an address in that array.** There is no other source to prefer or
> to cross-check against, which is what makes recovering a base from anywhere else — the first
> pointer, the densest run — not merely risky but unfounded.

**That closes the whitelist exactly.** `FUN_00332250` accepts `cmp ebx, 8` / `cmp ebx, 0x25` /
`cmp ebx, 5` at `00332285`, `0033228A`, `0033228F` and branches past its work otherwise — and
**{5, 8, 37} is precisely the set of namespaces this load path can present**: 5 for manager 0, 8 for
managers 1–3, and 37 overriding 8 for those same managers. **Manager 4's namespace 1 is absent from
the whitelist and also absent from the override probe**, which is the same boundary drawn twice.
That makes `FUN_00332250` a script-container helper rather than a general one.

*(The whitelist was found by another session on a different question and is reproduced here from the
bytes; the override and the set-closure are this document's.)*

### The field table

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | — | — | **YES — never read. See below.** |
| `+0x04` slotCount | `0x003304A0` at 15 sites, e.g. `003304DE`, `00330519` | — | — | — |
| `+0x08` | — | — | — | **YES — never read** |
| `+0x0C` | — | — | — | **YES — never read** |
| slot 0 `+0x10` | read `00330504`, dispatched `00330514` | — | — | — |
| slot 1 `+0x14` | — | — | — | **YES — no handler exists** |
| slot 2 `+0x18` | read `0033051F`, dispatched `0033052F` | — | — | — |
| slot 3 `+0x1C` | read `0033053A`, dispatched `0033054A` | — | — | — |
| slot 4 `+0x20` | read `0033063B`, dispatched `0033064B` | — | — | — |
| slot 5 `+0x24` | — | — | — | **YES — no handler exists** |
| slot 6 `+0x28` | read `00330555`, dispatched `00330565` | — | — | — |
| slot 7 `+0x2C` | — | — | — | **YES — no handler exists** |
| slot 8 `+0x30` | read `00330599`, dispatched `003305A9` | — | — | — |
| slot 9 `+0x34` | read `0033057E`, dispatched `0033058E` | — | — | — |
| slot 10 `+0x38` | read `003305CF`, dispatched `003305DF` | — | — | — |
| slot 11 `+0x3C` | read `003305B4`, dispatched `003305C4` | — | — | — |
| slot 12 `+0x40` | read `003304E4` (pre-pass) and `003305EA`, dispatched `003305FA` | — | — | — |
| slot 13 `+0x44` | — | — | — | **YES — no handler exists** |
| slot 14 `+0x48` | read `0033067A`, dispatched `0033068A` | — | — | skipped when `manager_index == 0` |
| slot 15 `+0x4C` | — | — | — | **YES — no handler exists** |
| slot 16 `+0x50` | read `00330605`, dispatched `00330615` | — | — | — |
| slot 17 `+0x54` | read `00330620`, dispatched `00330630` | — | — | handler exists; **0 files use it** |
| slot 18 `+0x58` | — | — | — | **YES — no handler exists** |
| slot 19 `+0x5C` | read `00330656`, dispatched `00330666` | — | — | — |

### The magic is never validated — and this is proven, not assumed

An earlier note recorded that `EBP2` appears **nowhere** in the executable: zero occurrences as an
uppercase string, zero as the dword `0x32504245`, while `.ebp` appears 10,380 times as path text.
That left two possibilities — the check does not exist, or it is built in a form a byte search
cannot see (arithmetic, two 16-bit halves, a hash). **A failed search cannot choose between them.**
The loader body can, and does.

Disassembling all 570 bytes of `0x003304A0` and collecting **every** `[rdi + N]` reference — `rdi`
being the file base, established at `003304D9 and rdi, rax` with `rax = 0xFFFFFFF0` — gives the
complete set of container bytes this build ever touches:

```
offsets touched  = { 0x04, 0x10, 0x18, 0x1C, 0x20, 0x28, 0x30, 0x34,
                     0x38, 0x3C, 0x40, 0x48, 0x50, 0x54, 0x5C }
references to [rdi]  (i.e. +0x00, the magic)  =  0
```

`+0x00` sits four bytes below a field the function reads ~~fourteen~~ fifteen times *(corrected 2026-10-02, OPUS: fifteen `cmp dword ptr [rdi + 4], N` sites over fourteen slot numbers — slot 12 is tested twice, at `003304DE` and `003305E4`; §6)*, and it is never touched.
Upstream is no better placed to check it: `BeginPrimaryPayloadLoad` allocates by size and hands the
buffer to a generic resource reader that has no `.ebp`-specific behaviour.

> **So the first reading is the correct one, and the second should not be carried forward.**
> The bytes `E B P 2` are **authoring provenance**. Overwrite them with anything and the game loads
> the file identically. `+0x08` and `+0x0C` are inert in the same sense — their being `0` in all
> 1,114 files is now known to be *because nothing reads them*, not merely a constant nobody varied.

### `+0x04` is the directory length, and it is enforced

Every dispatch is guarded, and the guard is always the same shape:

```asm
00330519  cmp  dword ptr [rdi + 4], 2     ; slotCount vs the slot index
0033051D  jbe  0x330534                   ; UNSIGNED — skip if slotCount <= 2
0033051F  mov  eax, dword ptr [rdi + 0x18]; slot 2's offset
00330522  test eax, eax                   ; 0 means absent
00330524  je   0x330534
00330526  add  rax, rdi                   ; file base + offset
00330529  je   0x330534
0033052B  or   eax, ebx                   ; pack the manager index into the low nibble
0033052D  mov  ecx, eax
0033052F  call 0x330190                   ; the slot-2 handler
```

Extracting the constant from all 15 `cmp dword ptr [rdi+4], N` sites and pairing it with the slot
index derived from the offset that follows, **`bound == slotIndex` holds at every one**. So the rule
is exactly:

> **slot `n` is dispatched only if `slotCount > n`**, compared unsigned.

`+0x04` is therefore **not a version stamp**. A file declaring `slotCount = 3` would have every slot
from 4 upward ignored even with perfectly valid offsets — a real and cheap way to disable content,
and a real way to break a file by accident.

**A zero offset means "absent"** (`test eax, eax`), which is why the directory can be sparse at all.
The `je` after `add rax, rdi` is dead in practice — it fires only if base+offset is exactly 0.

### The dispatch table

Fourteen slots reach code. There is **no loop and no jump table** — the function is a flat
open-coded sequence, which is precisely why it can be read exhaustively.

| slot | handler | files | what it does with the pointer |
|---:|---|---:|---|
| 0 | `ActorResource_OnDefinitionPayloadLoaded` `0x0032F850` | 1114/1114 | the script image — see the `section_000` sheet |
| 2 | `FUN_00330190` | 828 | stores to `DAT_022c6ca0[mgr]`, binder `FUN_0026c880`, mask bit 4 |
| 3 | `FUN_00330220` | 359 | stores to `DAT_022c6cc8[mgr]`, binder `FUN_0026c8a0`, mask bit 5 |
| 4 | `FUN_00332100` | 209 | → `FUN_003dfdc0(base)` — immediate, no mask accounting |
| 6 | `FUN_00330060` | 67 | stores to `DAT_022c6cf0[mgr]`, binder `FUN_0026c860(mgr, base)` → `slot+0xB0`, mask bit 6 — consumed as a **resref**: forwarded as `r9` to the window opener `FUN_002e16b0` (`00348EF8`/`0034AE91`/`0050EB57`, → `window+0x1A8`) and as `r8` to the kind-2 text-element ctor `FUN_002b3400` (`002C8D26`, → `element+0xA6`/`+0x60` texture bind) |
| 8 | `FUN_0032fa10` | 423 | stores to `DAT_022c6d80[mgr]`, binder `FUN_0026ce00(mgr, base)`, mask bit 8 |
| 9 | `FUN_0032fac0` | 423 | stores to `DAT_022c6d58[mgr]`, `FUN_002566e0(mgr, 0..3)`, mask bit 7 |
| 10 | `FUN_00331610` | 113 | stores to `DAT_022c6df8[mgr]`, binder `FUN_0026d3a0`, mask bit 11 |
| 11 | `FUN_003316b0` | 113 | stores to `DAT_022c6dd0[mgr]`, binder `FUN_0026d3c0`, mask bit 10 |
| 12 | `FUN_0032fb70` | 842 | stores to `DAT_022c6da8[mgr]`, binder `FUN_0026ce40`, mask bit 9 |
| 14 | `FUN_00330110` | 140 | stores to `DAT_022c6e20[mgr]`, mask bit 16 — **only when `manager_index != 0`** |
| 16 | `FUN_003320e0` | 517 | → **`FUN_003dfe60(0, base)`** |
| 17 | `FUN_00332110` | 0 | → **`FUN_003dfe60(1, base)`** — same binder, selector `1` |
| 19 | `FUN_003320d0` | 271 | → `FUN_003eaa00(base)` |

The `files` column is the US-corpus population of that slot — control
[`members/ebp2_slot_populations.py`](members/ebp2_slot_populations.py), run over all 1,115 `.ebp`
paths (1,114 containers) 2026-09-27. The carriers split by **pack family**, and each family
keeps its own payload profile: `plan_map/<zone>/<map>/global` packs own the map fixtures — all
359 slot-3 field-sign tables, all 209 `NAVI` slot-4, all 517 + 271 `FF12` slot-16/19 — while
`event/*` packs own slot-14 `LGT2` (all 140; cutscene lighting is event-scoped, and manager 0's
field lighting comes from the `.mpk` map pack instead, BW-3). Slot 2 rides both (602 globals +
226 events), and slot-6 `TIM2` mostly rides globals (55 of 67; 12 events ship their own texture).
A running event therefore leaves `slot+0xA8` holding whatever the map's global pack installed —
the installer only writes slots that exist.

### The section fields are write-only through the accessor family (2026-09-28, SWE2-CONTRACT)

Every `imul reg, reg, 0x288` site in the image is a slot-array accessor — there are **63**, and
each was decoded to its touched field. The result partitions them cleanly: the eight section
fields (`+0xA0`/`+0xA8`/`+0xB0`/`+0xD8`/`+0xE0`/`+0xF0`/`+0xF8`/`+0x100`) are touched **only by
binder-stub writes** (`0026C860`/`880`/`8A0`, `0026CE00`/`20`/`40`, `0026D3A0`/`C0`) — no
index-computed reader exists for any of them. All section consumption goes through
**arg-passed slot pointers**: `+0xA0`/`+0xA8` via `00264D60`/`00264D90`/`002673A0` (fed
`[02099D70]` by `002640C0` callers), `+0xB0` via the `002E16B0`/`002B3400` call sites, and the
camera/shake fields via the `0037AA90`-bound subsystem tables — outside this pattern by
construction. The family's actual readers cover only bookkeeping: `+0x10` pump flag
(`00264190`, `002671F0` getters + inline pump tests), `+0x00` record-array pointer,
`+0x20`/`+0x1D0`–`+0x1DC` counter/`u16` arrays, `+0x17` flags, `+0x108` teardown callback
(`ActorManager_SetResourceTeardownCallback` `00268630`), `+0x201`, `+0x13`, and the wholesale
`rep stosd` slot zeroer `0026B870`. Two of the 63 are notable by role rather than field:
`0026CE60` is where `rbx = base + index*0x288` gets **installed as the cached slot**
`[02099D70]` (gated on `+0x10`/`+0x13` flags), and `0025D9F6` is the per-slot pump that issues
the kind-`0xD4` request while `+0x10` bit4 is clear.

Three consequences a file-corpus reading could not have produced:

- **`section_017` is real code with zero shipped users.** Its handler calls the *same* binder as
  `section_016` with the selector flipped from `0` to `1`, so **`017` is a second instance of the
  `016` format**. The index space is not "13 types with gaps"; it is 14 dispatchable slots of which
  one is unused in this territory's data. ~~Open question `PROPOSED-repos-1e-1`.~~ *(answered: BW-1 above — slot 17 is zero in all nine shipped language trees; 2026-10-02, OPUS)*
- **Slots 1, 5, 7, 13, 15 and 18 are wired to nothing.** Not "absent from the corpus" —
  **structurally unreachable**. A modder can put a valid offset there and the engine will never look.
  This is the strongest possible form of the `Inert` column.
- **Slot 14 is skipped entirely for manager 0** (`0033066B test ebx, ebx ; je`), so its content
  loads for some managers and not others. Open question `PROPOSED-repos-1e-3`.
  *Answered 2026-09-14 (FABLE, `BW-3`): **manager 0's lighting comes from the map-control pack, not from EBP.** The skip at
  `0033066B` stops only the EBP route. On that route `00330110` stores the section-14 block per slot (`022C6E20[mgr]`), and
  `ActorResource_FinalizeManagerRuntimeAfterLoads` (`0032F1B0`) binds it through `0037AA90(block, slot)` once the slot's
  loads finish (`0032F1F9`); for manager 0 that table entry stays empty. Manager 0 is the primary area manager that runs the
  field frame ([the actor manager record](../../04-Actor-Entity/Actor-Manager-Record/the-actor-manager-record-field-map.md)).
  Its `LGT2` light set is slot 17 of the `.mpk` map-control pack
  ([the map ctrl pack](../../03-World-Area-Field/Map-Pack/the-map-ctrl-pack.md), row 17 and section 3.3). The pack dispatch
  `00378BC0` stores it at `02ADD090` and sets bit 8 of `02ADD0F0` (`00378EB9`–`00378ED6`), and `003775D0` binds it to slot
  0 with `0037AA90([02ADD090], 0)` (`00377697`–`003776A6`). **So the base field is lit by its map pack, and the sub-managers
  by their scripts' `section_014`**, through the same binder.

### Two mechanical constraints the file corpus cannot explain

**Why offsets must be 16-byte aligned.** `0033052B or eax, ebx` packs the 4-bit manager index into
the low nibble of the **resolved** pointer, and every handler recovers the pointer with
`and reg, 0xFFFFFFF0` (e.g. `0032F860`–`0032F871`). **An offset with any of the low four bits set
would corrupt the manager index.** The shipped corpus is `0x40`-aligned in all 5,419 offsets, so the
data over-delivers — but **16 is the hard requirement**, and that is the number a modder editing
offsets needs.

**The resolved pointer is carried through 32 bits.** `or eax, ebx` and `mov ecx, eax` are 32-bit
operations; the handler re-widens with `and rdi, 0xFFFFFFF0`. The upper 32 bits of the section
pointer are discarded and rebuilt as zero, so **the `.ebp` buffer must live below 4 GiB**. *(This is an **absolute** condition — the pointer is zero-extended with no base; the arena's own links obey a
different, base-relative window. §7, `BW-2` block, 2026-09-12.)* That is a
property of the allocator rather than of the file, but it is a real property of this build. Open
question `PROPOSED-repos-1e-2`.

### What loading normalises, and the write path

**Nothing is normalised.** The loader neither rewrites nor validates any container field; it reads
offsets and hands out pointers into the buffer it just read.

**There is no write path.** Nothing in the executable constructs an `EBP2` header. These files are
built by an offline toolchain — `section_000` records the author name and source filename of the
`.src` file it was compiled from (see the `section_000` sheet), which is direct evidence of an
external compiler and no runtime writer.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| **`0x003304A0`** | **`ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` — the directory walk** | ✅ complete, 570 B |
| `0x003304D9` | `and rdi, rax` — recovers the file base from the packed pointer | ✅ |
| `0x003304DE` | first `cmp dword ptr [rdi+4]` — the slotCount bound | ✅ |
| `0x00330504` | `mov eax, [rdi+0x10]` — slot 0's offset | ✅ |
| `0x0033052B` | `or eax, ebx` — the 4-bit manager-index packing that forces alignment | ✅ |
| `0x0033066B` | `test ebx, ebx` — the manager-0 exclusion on slot 14 | ✅ |
| `0x00330310` | `ActorResource_BeginPrimaryPayloadLoad` — sizes, allocates, async-reads | ✅ |
| `0x0032FCA0` | `ActorResource_BeginManagerResourceSetLoad` | partial |
| `0x0032FC30` | `WorldSimulation_ProcessDeferredModeRequest` | partial |
| `0x0032F850` | slot 0 handler | ✅ |
| `0x00263FF0` | `FUN_00263ff0(idx)` → `0x02098E10 + idx*0x288`, the actor-manager record | ✅ |
| `0x003DFE60` | shared binder for slot 16 (selector 0) and slot 17 (selector 1) | ~~not read~~ read — `g_fieldRoots[selector] = ptr`, the store at `0x003DFE6A` *(answered: section-016.md key addresses; 2026-10-02, OPUS)* |

## 5. Corpus survey

> **Cross-tree census 2026-09-12 (FABLE) — which of this page's `us` counts hold for the whole
> archive.** `FFXII_TZA.vbf` carries nine `plan_master` trees — `us`, `fr`, `de`, `es`, `it` (1,114
> containers each), `kr`, `cn` (1,115), `ch`, `in` (1,114) — and every non-`us` container was compared
> with its `us` counterpart section by section (content, not offsets): **2,342 of 8,930 are
> byte-identical; 6,578 differ**, and the differences fall in exactly five directory slots —
> `section_000` (2,323 files), `section_002` (6,192), `section_003` (2,835), `section_004` (24) and
> `section_006` (2,454) — while **slots 8–19 are byte-identical in every file of every tree**. So
> every `us`-tree count on the `section_008` … `section_019` pages (the `1,114/1,114`, `517 of 517`,
> `271 of 271` invariants, CC-2, BZ-2) is a corpus-wide fact, and the counts on the `section_000`,
> `002`, `003`, `004` and `006` pages are `us`-tree facts. Presence differs only for `section_006`
> (in 2,230 files where `us` lacks it, absent in 120 where `us` has it) and marginally `002` / `003`
> (4 and 1): `section_006` is present in **67–68** files of each Latin-script tree but in **556 (kr),
> 584 (cn), 603 (ch) and 633 (in)** — a localisation-carried section the CJK and Indian trees need
> eight times more often, which is the first lead on what the "unknown" `section_006` holds. Ten
> non-`us` containers have no `us` counterpart: `ttl_a01_e3.ebp` (kr, cn only) and the four
> `image/ff12/<lang>/bin/` control scripts (`btlctrl`, `ctrl`, `evctrl`, `mapctrl`), which exist under
> `in` and `ch` only. The always-zero slots (1, 5, 7, 13, 15, 17, 18) are zero in all 10,036
> containers (BW-1, CD-3).

**Invariants — every one checked over all 1,114 containers, not over one file:**

| | |
|---|---|
| `+0x00` = `'EBP2'` | 1,114 / 1,114 |
| `+0x04` = `0x14` | **1,114 / 1,114** — no file ever varies the slot count |
| `+0x08`, `+0x0C` = 0 | 1,114 / 1,114 |
| first present offset = `0x80` | 1,114 / 1,114 |
| all offsets `0x40`-aligned | **5,419 / 5,419** |
| offsets ascending, none past EOF | 1,114 / 1,114 |

**Because `slotCount` is `0x14` in every shipped file, the enforcement in §3 never fires in
practice.** That is worth saying plainly: the bound is real code, and it is also dead code against
this corpus. It becomes live the moment someone edits a file.

### The 32 bytes between the directory and the payload — settled

`check_layouts.py` flagged `+0x60 .. +0x80` as unaccounted in all 1,114 containers. The directory
ends at `0x60` (`0x10` + 20 × 4) and the first section begins at `0x80`, leaving 32 bytes.

Three readings were open: **alignment padding**, **a second header the reader consumes**, or
**authored bytes nothing reads**. Two of them are now dead.

| | |
|---|---|
| the 32 bytes are all-zero | **1,114 / 1,114** |
| distinct bit patterns across the corpus | **1** |
| offsets in `0x60..0x80` touched by the loader | **0** — the read set in §3 is `+0x04` plus the 14 slot offsets, every one below `0x60` |

**It is alignment padding, and the arithmetic says why it is exactly 32 bytes.** Section offsets are
`0x40`-aligned in this data (all 5,419), and `0x60` **is not** a multiple of `0x40`. The next
`0x40`-aligned position at or after the directory's end is `0x80`. So the gap is forced:

```
directory ends            0x60
next 0x40 boundary        0x80
padding                   0x80 - 0x60 = 0x20 = 32 bytes
```

**"A second header" is excluded twice over** — by the instruction-level read set (nothing reads
there) and by the content (a header that is identically zero in every file carries no information).
**"Authored bytes nothing reads" is excluded** for the same content reason: there is nothing
authored in 32 zero bytes repeated 1,114 times.

A modder may write anything into `+0x60 .. +0x80` with no effect, on the same evidence as the magic.

**Occupancy, re-derived from the directory itself** (independent of the external unpacker, and in
exact agreement with it):

| slot | files | slot | files | slot | files |
|---:|---:|---:|---:|---:|---:|
| 000 | 1114 | 008 | 423 | 012 | 842 |
| 002 | 828 | 009 | 423 | 014 | 140 |
| 003 | 359 | 010 | 113 | 016 | 517 |
| 004 | 209 | 011 | 113 | 019 | 271 |
| 006 | 67 | | | | |

Slots 1, 5, 7, 13, 15, 17, 18: **0 files**.

### The section bodies are individually tagged

Reading the first four bytes of every present section across the corpus gives a magic that is
**100 % consistent wherever the section occurs** — no exceptions in 5,419 observations:

| slot | first 4 bytes | slot | first 4 bytes |
|---:|---|---:|---|
| 000 | `0x8000000B` | 011 | `SHK1` |
| 002 | *none* (leading u32 varies) | 012 | *none* (small leading count) |
| 003 | *none* (leading u32 varies) | 014 | `LGT2` |
| 004 | `NAVI` | 016 | `FF12` |
| 006 | `TIM2` | 019 | `FF12` |
| 008 | `CML1` | | |
| 009 | `CAM7` | 010 | `CML1` |

**`CML1` occupies two different slots.** It is not "the section-8 format" — it is a control/track
container that the directory carries twice, paired once with `CAM7` (slots 8+9, 423 files) and once
with `SHK1` (slots 10+11, 113 files). **That is what the two "strict pairs" actually are**, and it
means the 008/009 and 010/011 co-occurrence is the *format's* structure rather than a statistical
curiosity. The section sheets carry the detail.

*(A four-byte magic identifies a body's **wrapper**, not its record layout. `CML1` appearing in two
slots is exactly the case where assuming otherwise would mislead.)*

### The outlier: one file in the corpus is not a container

`us/event/evt_t/evt_t0020/evt_t0020.ebp` — **2,416 bytes, and it has no `EBP2` header.** It begins
`07 00 00 80`, i.e. the section marker `0x80000007`. It is a **bare section body saved with a `.ebp`
extension**.

That is why `section_000` is present in 1,114 of 1,115 files rather than all of them, and it is a
fact a reader must be told: **a parser that assumes a header will misparse this file**, reading the
marker `0x80000007` as a magic and `0x00000000` as a slot count. Under this build's own rule
(`slotCount > n`) a slot count of zero dispatches *nothing*, so the engine would simply do nothing
with it — which is consistent with it never being loaded as a container at all.

## 6. Falsification pass — 2026-09-03

| attack | result |
|---|---|
| Is the magic checked somewhere the string search could not see — arithmetic, 16-bit halves, a hash? | **Killed.** The question is not answerable by *searching*, so it was answered by *reading*: every `[rdi+N]` reference in the 570-byte loader was enumerated from the instruction stream, and `[rdi]` appears zero times. A hidden check would still have to load the bytes. |
| Is the check upstream instead, in the reader that filled the buffer? | **No.** `BeginPrimaryPayloadLoad` sizes the file, allocates, and calls a generic resource reader with a completion callback; nothing on that path is `.ebp`-aware. Each step is the single caller of the next, so there is no third path in. |
| **Could the magic be compared against a constant held in `.rdata`, so that no immediate ever appears in code?** | **No — and this is a real pattern, not a hypothetical.** Another session found exactly it for `.sab`: `Sab_IsSabf` (`0x007CFF90`) does `cmp eax, [rip+0x541614]` against a four-byte tag at `0x00D115B4`, so a `.text` scan for `sabf` returns zero while the magic *is* checked on every load. Applying that method here: **`EBP2` occurs 0 times in the WHOLE image** — every section, as ASCII and as the dword in both endiannesses — so **there is no constant anywhere to compare against.** Positive control: the same scan finds `sabf` exactly once, in `.rdata`. |
| Does the `section_000` marker `0x8000000B` fare the same way? | **No, and this is the instructive case.** It occurs **19 times in the image** (8 `.text`, 11 `.rdata`), so unlike `EBP2` a byte scan is *not* empty and would read as evidence of a check. Decoding every containing function and testing operands: **no instruction anywhere takes `0x8000000B` as an immediate or a displacement.** Reproduced independently by a second session with a separate implementation, same 8 sites. |
| What are the 8 `.text` hits, then? | **All eight are the tail of a small little-endian value followed by a high-bit byte** — the pattern needs only `0B 00 00` then anything ≥ `0x80`. Four are `rel32`/`disp32` fields whose upper bytes are zero (`002A8DB2` `je` `+0xB28`, `002971C0` `disp 0xB4A`, `004055AD` `call` `+0xB00`, `0074F79E` `jmp` `+0xBBA`), and **in those the match straddles an instruction boundary** — it takes the next instruction's first byte as its `0x80`, so it cannot be an operand at all. Two more are `mov dword ptr [rbp + 0xb], 0x3f800000` (`002FB5B9`, `00404388`): displacement `0x0B` plus the low three bytes of **`1.0f`**. **Because `1.0f` is `3F800000`, any marker of the form `0x8000000X` will collide with it wherever a `[reg+0x0X]` store of `1.0f` occurs** — this recurs by construction, not by luck. |
| Is `+0x04` a version stamp that happens to equal 20? | **No.** It is compared against **fourteen different constants**, each equal to the index of the slot that follows it. A version stamp is compared against one value. |
| Is the offset relative to the file or to the directory? | **File.** `add rax, rdi` with `rdi` = the base recovered at `003304D9`. Slot 0 = `0x80` in every file and the payload does begin at `0x80`. |
| Does the "no handler" claim hold, or did the extraction miss a dispatch? | The extraction is mechanical over every `cmp dword ptr [rdi+4], N` site and returns 15 sites → 14 distinct slots. The set of touched offsets, derived **separately**, contains exactly `+0x04` plus those 14 slot offsets. Two derivations, same answer. |
| Could the decompiler have invented the gate? | The gate is quoted from raw instruction bytes (`83 7f 04 02` / `76 15`), read out of the PE image independently of Ghidra's decompiler. |
| Does the `0x40` alignment invariant prove `0x40` is required? | **No, and the sheet does not say so.** The code requires 16. The corpus supplies 64. Conflating "what the data does" with "what the code demands" is the error this row exists to prevent. |
| The oracle: does `ff12-script` agree? | **Not consulted for any claim here.** Every statement in §3 comes from the loader body; the tool reads `section_000`'s bytecode and says nothing about the container's dispatch. Nothing in this sheet rests on it. |

~~**Not yet attacked:** whether another language's archive populates slot 17~~
~~(`PROPOSED-repos-1e-1`) — that needs the `jp`/`eu` trees, which are not unpacked here.~~ *(answered: BW-1, §2 — no shipped tree populates slot 17, and `FFXII_TZA.vbf` carries no `jp` or `eu` tree, only `ch`, `cn`, `de`, `es`, `fr`, `in`, `it`, `kr` and `us`; 2026-10-02, OPUS)*

## 7. What this document does not claim

- **The section bodies.** Only the wrapper is documented here. The magics in §5 are a corpus
  observation handed to the section sheets; **this sheet does not claim to know what `CML1` or
  `NAVI` contain.**
- **The binders.** `FUN_003dfe60`, `FUN_003eaa00`, `FUN_003dfdc0`, `FUN_0026c8xx`, `FUN_0026ceXX`
  and `FUN_0026d3xx` are named as the destinations of the dispatch. ~~**Their bodies were not read**,~~
  ~~so the "what it does with the pointer" column in §3 describes the *handler*, not the consumer.~~ *(answered: the section sheets have read them since — `0026C880` (section-002), `0026CE00` (section-008), `0026CE40` (section-012), `0026D3A0` (section-010), `003DFE60` (section-016); 2026-10-02, OPUS)*
  A neighbouring session found that a handler passes `(slot, base)` and the binder copies the base
  into a **second** global inside the `0x02098E10 + idx*0x288` manager record — so an xref census on
  the handler's own global under-counts consumers. That is the displacement blind spot
  `COVERAGE.md` catalogues, and it is why no `Inert` claim is made about any *section body* here.
- **Sub-4-GiB allocation.** §3 states that the pointer is truncated to 32 bits, which is observed.
  It does **not** claim the allocator guarantees a low arena~~ — `FUN_0036c660` was not read~~ *(answered: read since — a header tagger, not an allocator, the 2026-09-12 correction directly below; 2026-10-02, OPUS)*.
  > ~~**BW-2 answered 2026-09-12 (FABLE): there is no arena, and the image gives no guarantee — the
  > truncation is sound only by OS policy.** `FUN_0036C660` read whole (82 bytes): it is not an
  > allocator but a **release** — it checks a `0xFF12` magic at `[rcx − 0x40]` and a flag bit at
  > `[rcx − 0x2C]`, frees `rcx − 0xC` through the import at `008C2F70` with `r8d = 7`, and clears
  > the header fields (`0036C675`–`0036C6A0`); the pseudo-code at §2 that shows it as the
  > whole-file allocation names the wrong half of the pair.~~
  >
  > **CORRECTED 2026-09-12 (ASTRA-CONTRA-FABLE-RESOURCE-ARENA; re-derived by FABLE from the bytes and the
  > PE import directory).** `008C2F70` is `api-ms-win-crt-string-l1-1-0.dll!strncpy`, not a free
  > (`malloc` is `008C2B40`, `free` the slot beside it). `FUN_0036C660(p, name, tag)` is a **header
  > tagger**: when `p` is non-null, `word [p − 0x40] == 0xFF12` and `[p − 0x2C]` bit 0 is set, it copies
  > up to 7 characters of `name` to `p − 0xC`, terminates at `p − 5`, zeroes `word [p − 2]`, stores the low
  > 16 bits of `tag` at `p − 0x22`, and returns `p` (`0036C670`–`0036C6A4`). The `.ebp` buffer is
  > allocated first, by `0036A100(size)` (`0033039C`), and tagged with `0x95C` (`003303A4`–`003303AD`).
  > **And there is an arena.** `0036BC60` (887 B) is the game's own arena allocator: fifteen heaps (index ≤ `0xE`) as `0xA8`-byte
  > records at `022D7FD0`, an enable mask at `022D89B8`, request sizes rounded up to 64 bytes, a `0x40`-byte
  > block header, first-fit from the free list's head (`+0x90`) or last-fit from its tail (`+0x98`), and
  > splitting (`0036BC89`–`0036BDE0`). **Its block links are 32-bit values decoded through
  > `ImageAddress_ResolveRuntimePointer` `0020E600`** (`0036BD09`, `0036BD37`, `0036BD6C`–`0036BDA4`) — the
  > same `base + (u32)x` pair the authored tables use — so the arena's own bookkeeping only works if every
  > block lies within 4 GiB above the base `01F83530`. `0036A100` / `0036A190` / `0036A1A0` are its entry
  > wrappers (`0036BFE0` retries and reclaims). So the 32-bit truncation this
  > sheet observes is not an isolated accident: the resource arena is built on the same 32-bit
  > reference convention. The backing is established as nine CRT `malloc` blocks made at boot by `0022A0B0` (about 256 MiB;
  > nested arenas carved from them), and the initializer keeps full 64-bit pointers (ASTRA's EXP-077;
  > [the memory page](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md)
  > has the table). What is **not** established is where those blocks land in a running process, nor whether `DYNAMIC_BASE` clear describes the
  > running process (a header request, `CI-1`). "A latent defect the shipped process never trips" is
  > withdrawn as a proof; it is an expectation the arena's own design shares. The reconstruction
  > rule stands: keep resource buffers within 4 GiB of the base, or widen every reference and link. ~~The image imports **no `VirtualAlloc`** (538 imports; the allocators are the CRT's `malloc` / `calloc` / `realloc` / `_aligned_malloc` from `api-ms-win-crt-heap-l1-1-0` plus `GlobalAlloc` / `LocalAlloc`), so every `.ebp` buffer comes from the process heap *(qualified 2026-09-12: from the arena above, whose backing is not established)*, and the PE header clears `DYNAMIC_BASE` (`DllCharacteristics 0x8120`), so Windows applies no address-space randomisation and the heap grows bottom-up from the lowest free addresses above the image at `00120000`. The same convention was settled the same day for the authored-table resolver (`01F83530`, J-C): a **latent 64-bit defect** the shipped process never trips because its allocations sit low. A reimplementation must keep its buffers below 4 GiB or carry the full pointer.~~
  >
  > **Two different width conditions, stated separately (2026-09-12, OPUS-NOTICE-FABLE-ARENA-WINDOW).** (1) **This sheet's section pointer is an absolute address carried through 32 bits with no base**: `0033050B add rax, rdi` then `00330510 or eax, ebx` pack the absolute buffer address and the manager nibble into a 32-bit value, and the handler zero-extends it (`0032F860 mov edi, ecx`, `0032F871 and rdi, rax`) — so the `.ebp` buffer itself must lie **below 4 GiB absolute**. (2) **The arena's links and the authored-table references are base-relative**: `0020E600` decodes `zext32(x) + [01F83530]` (a 64-bit add) and `0020E620` encodes `trunc32(p) − lo32(base)`, so they round-trip only for `0 ≤ p − base < 2^32` — a window **above the base**, not an absolute ceiling (OPUS's byte-level reading; the memory page states it the same way). With the base observed `0` at the title screen (EXP-002) the two coincide today; if the base ever became non-zero, condition (1) would still require an absolute low buffer while (2) would move. A reimplementation must meet both, or carry full pointers in both places.
  >
  > **A third condition and an executed consequence (2026-09-12).** (3) Arena **handles** are absolute slot
  > addresses carried in 32 bits (`0036AF20` returns the slot's low 32 bits OR 3; `00369800` masks with
  > `0xFFFFFFFC`), so a handle-issued block's slot table must lie below 4 GiB absolute
  > ([the memory page](../../24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md) §2).
  > And condition (2) is not only arithmetic: ASTRA's
  > [EXP-078](../../_experiments/EXP-078-arena-allocation-link-width.md) ran the original allocator on high backing with
  > base `0`, and the **second** allocation followed a 32-bit neighbour link into low memory — a fault, or with a copy
  > mapped there, the correct return value while reading and writing the copy. That is an isolated-execution result;
  > where the shipped game's backing lands is still open.
- ~~**Slot 14's manager-0 exclusion is described, not explained.** What distinguishes manager 0 is~~
  ~~open.~~ *(answered: BW-3, §3 — manager 0's lighting comes from the map-control pack, not from EBP; 2026-10-02, OPUS)*
- **No search for a writer was run beyond the absence of any header-constructing code on the read
  path.** "The game does not write `.ebp`" rests on that plus the authored provenance strings in
  `section_000`, not on an exhaustive scan.

## 8. Corrections and record

- **`0x8000000B` is not the file magic.** An earlier note in this project recorded it as such. It is
  the **`section_000` marker**, one level down; the file magic is ASCII `EBP2`. Both appear in the
  first bytes of a file — the section marker at `+0x80`, the magic at `+0x00` — which is how they
  came to be conflated. The census caught it; the loader reading confirms the levels are distinct
  (the dispatcher reads neither).
- **"An offset table in 8-byte slots"** appeared in an early plan for this category. The directory is
  **`u32[20]`, 4-byte slots**. Corrected by the census before any code was read.
- **The constant-scan census of section indices is a dead end, and the measurement that kills it is
  preserved.** Counting `0x80000000|n` constants in `.text` has a noise floor of 84 (measured on
  indices 20–31, which cannot be section markers because the directory holds only 20), which swamps
  six of the thirteen real indices, while `001` — present in *zero* files — scores 518. **This sheet
  did not repeat it.** The dispatch table came from the branch structure of one function instead,
  which yields all 14 slots with no false positives and additionally finds slot 17, something the
  scan could never have distinguished from noise.

## 9. Related

- [`section-000-bytecode.md`](../Bytecode-And-Opcodes/section-000-bytecode.md) — slot 0, the script
  image; the only section this sheet's author also documents
- [`../README.md`](../README.md) — the category census and the 14-unit denominator
- [`01 — Script VM & Native Bridge`](../../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md)
  — the interpreter that executes what slot 0 contains
- The `Sections/` sheets for slots 2, 3, 4, 6, 8, 9, 10, 11, 12, 14, 16, 19

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

- **Presentation — CLIENT and SERVICE.**
  - The arena entries `0036A100` and `0036A190` have 26 and 17 Presentation-filed callers respectively. **The container
    arena is shared with character rendering** (`CharacterRenderSystem_AllocateAndInitialize` among them).
  - The boot initialiser `0022A0B0` loads `AddMotion_LoadHighModelReplace` and `AddMotion_LoadSkeletonMapping`.
- **Audio — CLIENT and SERVICE.**
  - `00369800` is called by a 256-byte Audio-filed body.
  - The binder caller `003775D0` calls a 188-byte Audio-filed helper.
- **Input — SERVICE.** The boot initialiser `0022A0B0` calls the 119-byte Input-filed initialiser.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CoreRuntimeScheduling — CLIENT.** The start-up subtree's root cited here is reached from a 387-byte core start-up body and calls the 146-byte core start-up helper. 

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Citation spellings (R5), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatAction — CLIENT.** `WorldSimulation_ProcessDeferredModeRequest` is called by `BattleAction_InitializeGlobalSpecialSequenceMode`.
- **Movement — CLIENT.** The 21-byte manager-record accessor this page cites is called by Movement bodies of 702 and 2,026 bytes.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**UI — CLIENT (SWE2-EC7 batch-150).** The `0029AEF0` flag sweep runs on the shared `0035BB60`/`0035BB00` record accessors the UI layer calls heavily (`002737B0`/`00297640`/`002734F0`/`002964D0` among them), and `00297170` itself sits inside that layer's call neighbourhood (`002904D0`/`00273A20`/`0029AE50`) - shared accessor fan-in over container records, not UI ownership of the container.

**Gameplay — CLIENT (SWE2-EC7-164, 3 edges).** The vector helpers `00202D20`/`00202E10` and the angle leaf `0046F460` this page's `003355A0` cites are also called by gameplay-filed `00339630` — shared math, not container plumbing.
- **Actor — SERVICE (2 edges).** 2 outbound (page-cited `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `003775D0` call Actor bodies `0037AA90`). Substantive edges include `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) calls `0037AA90`; `003775D0` calls `0037AA90`.
- **ActorEntity — CLIENT and SERVICE (173 edges).** 99 inbound (ActorEntity bodies `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorResource_BeginPrimaryPayloadLoad` (00330310), `003306E0` call page-cited `00263FF0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `002566E0`); 74 outbound (page-cited `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` (003304A0), `ActorSystem_InitializeManagerRuntime` (0026CE60), `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0) call ActorEntity bodies `00263FF0`, `ActorResource_FinalizeManagerRuntimeAfterLoads` (0032F1B0), `0037B230`). Substantive edges include `0022A0B0` calls `BattleStorage_InitializeWorkArrays` (002368D0); `002566E0` is called by `ActorResource_ResetManagerLoadState` (0032ED80); `002566E0` is called by `0032FAC0`; `002566E0` is called by `003306E0`; the remaining edges run through shared helpers the page cites.
- **Party — CLIENT and SERVICE (4 edges).** 3 inbound (Party bodies `PartyFocus_ClearCurrentActorIfEligible` (00358B40), `PartyControl_UpdateControlledActorLocomotion` (00358C60), `PartyFocus_UpdatePrimarySecondaryActorProcessing` (00358EE0) call page-cited `002671F0`); 1 outbound (page-cited `ActorSystem_InitializeManagerRuntime` (0026CE60) call Party bodies `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0)). Substantive edges include `002671F0` is called by `PartyFocus_ClearCurrentActorIfEligible` (00358B40); `002671F0` is called by `PartyControl_UpdateControlledActorLocomotion` (00358C60); `002671F0` is called by `PartyFocus_UpdatePrimarySecondaryActorProcessing` (00358EE0); `ActorSystem_InitializeManagerRuntime` (0026CE60) calls `PartyFocus_CommitPendingPackedActorHandle_Thunk` (00358BB0).
- **Resource — CLIENT and SERVICE (44 edges).** 30 inbound (Resource bodies `00384420`, `00249210`, `00379E90` call page-cited `0032E620`, `0032E400`, `0036A190`); 14 outbound (page-cited `0022A0B0`, `ActorResource_BeginManagerResourceSetLoad` (0032FCA0), `ActorResource_BeginPrimaryPayloadLoad` (00330310) call Resource bodies `0032E400`, `002DF980`, `0032E620`). Substantive edges include `0022A0B0` calls `0032EAE0`; `0022A0B0` calls `002DF9A0`; `0022A0B0` calls `00379E90`; `0022A0B0` calls `00379D20`; the remaining edges run through shared helpers the page cites.
- **Save_Load_Settings — CLIENT (1 edge).** 1 inbound (Save_Load_Settings bodies `002EF300` call page-cited `0032E620`). Substantive edges include `0032E620` is called by `002EF300`.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `002E16B0` call Story_Event_Quest_Hunt bodies `PersistentFlag_SetBank2048` (0032ABF0)). Substantive edges include `002E16B0` calls `PersistentFlag_SetBank2048` (0032ABF0).
- **World — CLIENT and SERVICE (5 edges).** 4 inbound (World bodies `00378540` call page-cited `0032E400`, `0032E620`, `0036A190`); 1 outbound (page-cited `0022A0B0` call World bodies `00266D10`). Substantive edges include `0022A0B0` calls `00266D10`; `0032E400` is called by `00378540`; `0032E620` is called by `00378540`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (40 edges).** 29 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0036C660`, `0032E400`, `0036A190`); 11 outbound (page-cited `WorldSimulation_ProcessDeferredModeRequest` (0032FC30), `ActorSystem_InitializeManagerRuntime` (0026CE60), `003320D0` call WorldAreaField bodies `003DFE60`, `BattleSystem_InitializeAreaState` (002342F0), `AreaArd_RefreshForMapRefField` (003EA6E0)). Substantive edges include `ActorSystem_InitializeManagerRuntime` (0026CE60) calls `BattleSystem_InitializeAreaState` (002342F0); `002DF980` is called by `00379A10`; `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; the remaining edges run through shared helpers the page cites.
## SWE2-EC7-112 update (2026-09-20) - `0017FA90` measured

`0017FA90` (78 B) is the
argument repack `00332250`
and `00575710` run:
`001B5FB0()` fetches the
object, then `001B6350` is
called with `edx = ecx`,
`r8d` zero-extended from
`dl`, `r9` passed through and
`r9d` re-pushed as the stack
argument - a four-in/four-out
forwarder.
Interior anchor `0017FAC4`
(the `001B6350` call).

`0017F790` (43 B) is the
thin forwarder `00330060`
and `00575710` run:
`001B5FB0()` fetches the same
object and the tail jumps
`001B47A0(obj, edx = ecx,
r8 = rdx)` - no repack beyond
the singleton fetch.
Interior anchor `0017F7B6`
(the `001B47A0` tail).

`0029AEF0` (230 B) is the per-record flag sweep `00297170` runs: over `0035BB60()` records it resolves each index through `0035BB00`, normalises every record's `+0xD8` word to `(w & ~7) | 0x82`, and scans the `[rbp+0x40]`-counted pair array at `rbp+0x50` for the resolved id - a hit ORs `+0xD8` bit `0`, a pair `+4` byte lacking bit `1` clears `+0xD8` bit `1`, and a pair `+4` bit `0` records that index for return; no hit returns `-1`

Interior anchor `0029AF7C` (function `0029AEF0`).

`003355A0` (157 B) is the wrapped-angle helper `002FB560` calls: `004692E0` reads both operands, `00202D20` produces the cosine-like scalar (clamped by `1.0f` + `-1.0f` fold), `0046F460` converts it, `00202E10` writes the cross at `[rsp+0x20]`, and the result is `xmm6` or `0x40EA0EA1 - xmm6` depending on the cross's `[+4]` sign - an angle normalized to one interval

Interior anchor `003355C4` (function `003355A0`).

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-ebp2-container-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00297640` | 167 B | returns 0 for `edx` above 7 (unsigned); otherwise dispatches on `edx` through an 8-entry case table (decoded from the bytes): 0 returns 1; 1 calls `0029B440(0035BB00(r8d))` and `00249C60(1)` and returns 1; 2 tests bit 1 of byte `+0x318` of the `0x160`-byte record `r9d` at `rcx` and returns 0 after `00249C60(5)` when it is set, else 1 after `00249C60(0x15)`; 3 returns 0 after `00249C60(5)` when `00299B90(signed word +0x14 of 0035D320())` is zero, else calls `0035BC30()` and `00249C60(3)` and returns 1; 6 returns 0 after `00249C60(5)`; 4, 5 and 7 return 0 | `00297644`, `0029765E`, `0029766A`, `002976A3`, `002976C5` |
