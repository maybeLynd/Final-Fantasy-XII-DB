# 25 — The EBP script container

> **`.ebp` is the file the game's behaviour is written in.** Every map's spawn table, trigger
> volume, door, weather chance and trap; every cutscene's direction. **1,115 scripts per language,
> nine languages, 10,045 files in the archive.**

This category documents **the file**. The virtual machine that executes it is category
[01 — Script VM & Native Bridge](../01-Script-VM-Native-Bridge/README.md) and stays there.

---

## What is already known, and where it lives

**The expensive half is done and it is not in this folder.** Before writing anything here, know
what exists:

| | Where | What |
|---|---|---|
| the interpreter | [`01/Interpreter-Core`](../01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md) | `0x0025E4C0`, **100 opcodes**, jump table `0x00261DF8`, bound `0x00–0x63`, one-byte opcode, 92 distinct targets, **six opcodes inert in the shipped build** |
| the verbs | [`01/Verb-Dispatch`](../01-Script-VM-Native-Bridge/Verb-Dispatch/scriptvm-verb-dispatch-and-parameter-encoding.md) + `scriptvm-verb-table.tsv` | **1,960 rows** — id, verb name, three callback addresses, measured argument count, operand encoding |
| the dispatch table | [`01/scriptvm-native-dispatch-table.md`](../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) | how a verb id reaches native code |

**What is missing is the container around it**, and that is what this category is for.

---

## The population — censused, not chosen

`ebp_explained` is scored against **14 units**: the container itself, plus **every section type
present in the corpus**.

**The 13 section types were censused by unpacking all 1,115 `us` scripts** — not sampled, not
guessed. A 30-file sample also found 13, and the full run confirmed it; the numbers below are the
full run.

| Unit | Present in | Lead |
|---|---:|---|
| `container` | — | the `EBP2` header and its offset table |
| `section_000` | **1114 / 1115** (99.9 %) | **the bytecode.** `ff12-script.exe -dc` decompiles it |
| `section_002` | 828 (74.3 %) | text — `ff12-text.exe` reads it |
| `section_003` | 359 (32.2 %) | text — same tool |
| `section_004` | 209 (18.7 %) | ~~*unknown*~~ `NAVIICN2` map-icon table, stored and never read in this build — [section-004](Sections/section-004.md) *(answered: see that sheet; 2026-10-02, OPUS)* |
| `section_006` | 67 (6.0 %) | a `TIM2` picture — [section-006](Sections/section-006.md); **2026-09-12:** 556–633 files in the `kr` / `cn` / `ch` / `in` trees against 67–68 in every Latin-script tree, 23-pixel-high strips of varying width — ~~pre-rendered text lines~~ per-event expansion-glyph sheets in the `in` / `ch` / `cn` / `kr` trees, the Latin-tree strips possibly captions (section-006 §5) *(answered: the 2026-09-24 refinement there; 2026-10-02, OPUS)* |
| `section_008` | 423 (37.9 %) | ~~*unknown*~~ `CML1` camera-name list — [section-008](Sections/section-008.md) *(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 009** |
| `section_009` | 423 (37.9 %) | ~~*unknown*~~ `CAM7` camera table — [section-009](Sections/section-009.md) *(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 008** |
| `section_010` | 113 (10.1 %) | ~~*unknown*~~ `CML1` shake-name list — [section-010](Sections/section-010.md) *(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 011** |
| `section_011` | 113 (10.1 %) | ~~*unknown*~~ `SHK1` shake curves — [section-011](Sections/section-011.md) *(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 010** |
| `section_012` | 842 (75.5 %) | model references — `ff12-model.exe` reads it |
| `section_014` | 140 (12.6 %) | ~~*unknown*~~ `LGT2` light set — [section-014](Sections/section-014.md) *(answered: see that sheet; 2026-10-02, OPUS)* |
| `section_016` | 517 (46.4 %) | positions — `ff12-pos.exe` reads it |
| `section_019` | 271 (24.3 %) | ~~*unknown*~~ `FF12AR03` area data (`MAPARD`) — [section-019](Sections/section-019.md) *(answered: see that sheet; 2026-10-02, OPUS)* |

**Findings the census produced before anything was read:**

- **Two strict pairs.** `008`/`009` co-occur 423 times and **never appear alone**; `010`/`011` the
  same at 113. Whatever they are, they are two halves of one thing.
- **`002`/`003` are NOT a pair** — 328 together, 500 with `002` alone, 31 with `003` alone. The
  toolchain feeds both to the same text reader, and the corpus says they are independent.
- **The index space is sparse.** `001`, `005`, `007`, `013`, `015`, `017`, `018` **never occur** in
  1,115 files. Reserved, PS2-era, or unused by this title.
- **One file has no `section_000`** — a script container with no script.
- **Fourteen slots are dispatchable, thirteen ship data.** `section_017` has a live handler
  (`FUN_00332110` → `FUN_003DFE60(1, ptr)`) and zero files in all nine language trees (10,036
  containers; BW-1 / CD-3, 2026-09-12), so the thirteen section types censused here are the shipped
  population, and the dispatcher's fourteenth is authored capacity nothing uses.

> ~~**Seven of the fourteen units have no tool-side lead at all.** That is the real work here, and it~~
> ~~is not large.~~ *(answered: all seven now have section sheets — the table above; 2026-10-02, OPUS)*

---

## What 100 % means

**14 of 14 units documented**, each carrying a **loader contract** — not just the layout, but what
the engine reads, rejects, clamps and ignores. Section 4b of
[`_templates/SYSTEM.md`](../_templates/SYSTEM.md) is the shape.

Declare coverage in frontmatter; the metric counts declarations, not prose:

```yaml
ebp_units:
#   - "container"        <- uncomment in a real sheet; commented here so this
#   - "section_000"         README does not register as covering them itself
```

> **The example above is commented out on purpose.** The first version of this README was not, and
> `check_ebp.py` promptly counted the README as covering two units — **2 / 14 for a file that
> documents nothing.** A metric that counts declarations will count an example as a declaration.

**One owner per unit** — `check_ebp.py` reports a unit claimed by two documents as a collision.

**Use [`_templates/FORMAT.md`](../_templates/FORMAT.md), not `SYSTEM.md`.** A section sheet is a
different genre: it opens with **corpus validation** — *"present in 423 of 1,115 files, never
observed without `section_009`"* — and its centre of gravity is the loader contract, not the call
chain. `SYSTEM.md` is for systems; `FORMAT.md` is for files.

---

## The build-out, in the order it should happen

**Phase 1 — the container (1 unit).** `EBP2` magic at `+0x00`, a ~~version/count~~ slot count `0x14` at `+0x04`,
and an offset table in ~~8-byte slots~~ 4-byte slots, `u32[20]` at `+0x10` *(corrected 2026-10-02, OPUS: the walker `003304A0` compares `[rdi + 4]` with each slot number before reading slot `n` at `[rdi + 0x10 + 4n]` — slot 2 at `0033051F` `[rdi + 0x18]`, slot 19 at `00330656` `[rdi + 0x5c]`; Container/ebp2-container.md)*. Find the loader by searching `.text` for `0x32504245`, the
method the [VBF sheet](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/how-the-bigfile-index-loads-and-is-verified.md)
used to find `SRYK` (*"the only occurrence of those bytes in `.text`"*). **This unlocks everything
else, because the section directory is what names the sections.**
→ `Container/`

**Phase 2 — the four sections with an oracle (4 units).** `000`, `002`/`003`, `012`, `016` all have
a tool that already reads them. Read the engine's loader, write the contract, **and check it against
the tool's output.** Disagreement means one of the two is wrong and you find out which — a luxury no
other format in this database has.
→ `Sections/`, and `000` also feeds `Bytecode-And-Opcodes/`

**Phase 3 — the seven unknowns (7 units).** `004`, `006`, `008`+`009`, `010`+`011`, `014`, `019`.
No tool reads these. **Attack the two strict pairs first** — a pair is a stronger signal than a
singleton, and 423 co-occurrences is a lot of evidence about what they are together.
→ `Sections/`

**Phase 4 — the authoring model (part of the container unit, not extra).** What the decompiled form
already shows: `option` blocks (`spawnOrder`, `weatherProbability`, `trapOffset`), `import global`
declarations whose addresses are **offsets into the save's persistent flag bank**, actors with
handler functions (`init`, `main`, `touch`/`touchon`/`touchoff`, `mapjump`). This is where the
cross-subsystem joins get written down.
→ `Authoring-Model/`

---

## Why this category matters beyond the format

**Three subsystems this database already documents separately meet in one `.ebp` header**, and
nothing yet says so:

- **`option weatherProbability = {100, 0, 0}`** — the [glossary](../_index/GLOSSARY.md) already
  defines this as *"authored per-slot chance the current slot survives the transition roll, script
  header `+0x64`."* **The database has been reading `.ebp` header fields without documenting the
  container they sit in.**
- **`import global short シナリオフラグ = 0x00`** — script globals are *addresses*, and
  [the save image](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)
  documents `WorldPersistence_ImportGroupPersistentBank` restoring that bank on load. **A script
  global's address is an offset into the save's persistent flag bank.**
- **`option spawnOrder`** — spawn setup, which category 05 documents from the engine side.

---

## Evidence: there is an independent oracle, and it must be used carefully

`ff12-script` v2.83 decompiles these files today. **That is unusual and valuable, and it is also a
hazard.**

> **The tool is not authority.** It is a second reading of the same bytes by someone else, and this
> database's standard is the binary. Use it to **falsify** — where the loader reading and the tool
> disagree, say so and resolve it — never to source a claim. A claim that rests on the tool is
> tier 6 at best and must say so.

**A concrete instance of why: the file magic.** An earlier note in this project recorded the `.ebp`
magic as `0x8000000B`. It is not — **the file magic is ASCII `EBP2`**, and `0x8000000B` is a
*section* marker that appears inside. Two magics at two levels, conflated in one sentence. **The
census caught it; a tool would not have.**

---

## Files here

- `Container/` — the `EBP2` header, the offset table, the section directory
- `Sections/` — one sheet per section type
- `Bytecode-And-Opcodes/` — instruction encoding; opcode *semantics* stay in category 01
- `Authoring-Model/` — actors, handlers, `option` blocks, global imports and their joins

---

## The container, read across the whole corpus — 2026-09-03

`census_ebp_container.py` over **1,115 files** in `Tools/work/repos-d2/ebp`. Output:
`Tools/work/formats/ebp-container-census.tsv`.

```
+0x00  u32       magic       'EBP2'
+0x04  u32       slotCount   0x14 = 20 -- the length of the directory that follows
+0x08  u32       0
+0x0C  u32       0
+0x10  u32[20]   section offsets, INDEXED BY SECTION NUMBER, 0 = absent
                 (directory ends at 0x60; payload begins at 0x80)
```

**The directory is indexed, not packed.** That is the whole explanation for the sparse numbering:
`001`, `005`, `007`, `013`, `015`, `017` and `018` are not missing sections, they are **slots that
are always zero**. A packed list would have made those indices unobservable, and the census would
have had no way to know they existed.

### Invariants — every one checked over all 1,114 containers, not over one file

| | |
|---|---|
| `+0x04` slot count | **`0x14`, all 1,114** |
| `+0x08`, `+0x0C` | **`0`, all 1,114** |
| first section offset | **`0x80`, all 1,114** |
| section offsets | **`0x40`-aligned — all 5,419 offsets**, ascending in every file, none past EOF |

Section length is not stored. **It is the distance to the next present offset**, and the last
section runs to EOF — which is why a truncated file would silently yield a short final section.

### The frozen denominator, confirmed by a second instrument

`check_ebp.py` scores `ebp_explained` against 13 section types censused with an **external
unpacker**. Re-deriving occupancy from the container's **own directory** — a completely different
route — gives:

> **All 13 section slots agree exactly.** 000/1114, 002/828, 003/359, 004/209, 006/67, 008/423,
> 009/423, 010/113, 011/113, 012/842, 014/140, 016/517, 019/271.

**A scored denominator that two independent readings agree on is worth much more than one nobody
has re-checked.** The strict pairs hold in the directory too: `008`/`009` at 423 each, `010`/`011`
at 113 each.

### The 1,114-of-1,115 anomaly is resolved

`section_000` was censused at **1,114 of 1,115**, and the missing file is
`us/event/evt_t/evt_t0020/evt_t0020.ebp`. **It is not a container at all.** It begins
`07 00 00 80` — the section marker `0x80000007` — so it is a **bare section body saved with a
`.ebp` name**, 2,416 bytes, no `EBP2` header.

One file in the shipped corpus is a different kind of thing wearing the same extension. That is a
fact a sheet must state, because a reader that assumes a header will misparse it.

### `EBP2` appears nowhere in the binary

Neither as a string (`EBP` uppercase: **0 occurrences**) nor as the dword `0x32504245`
(**0 occurrences**), while `.ebp` appears 10,380 times as path text.

**Two readings, and this does not choose between them:**

1. **The loader never validates the magic** — it is dispatched by extension or by a table, and the
   first four bytes are simply skipped. If so, corrupting them changes nothing, which is a real
   `Inert` entry for the loader contract.
2. **The check exists in a form this search cannot see** — built by arithmetic, compared as two
   16-bit halves, or folded into a hash. `COVERAGE.md` lists the arithmetic-constant blind spot for
   exactly this case.

~~**Settling it needs the loader body read in Ghidra.** Until then the sheet may not claim either.~~ *(answered: the loader body is read, and the first reading holds — the walker `003304A0` never references `+0x00`; [Container/ebp2-container.md](Container/ebp2-container.md) §3; 2026-10-02, OPUS)*

### The marker scan was too noisy to use, and here is the measurement

An attempt to census which sections the *engine* supports by counting `0x80000000|n` constants
**fails, and the noise floor proves it.** Indices 20–31 cannot be section markers — the directory
only has 20 slots — so their counts measure the background directly:

```
indices 20..31 : 66, 2, 3, 3, 55, 1, 1, 4, 84, 0, 1, 14      median 3, MAX 84
```

Against a floor of 84, **six of the thirteen real section indices are indistinguishable from
noise** (`006`:19, `010`:3, `011`:19, `014`:7, `016`:49, `019`:12), while `001` — which never occurs
in 1,114 files — scores 518. **A raw dword scan cannot tell a section marker from any other use of
the same constant**, and `0x80000000` alone occurs 36,519 times because it is also the float sign
mask.

> **Recorded as a negative result rather than dropped.** The next person to have this idea should
> find the measurement that kills it, not repeat it.

### What is still needed for the container sheet

The census supplies §2 (layout), §5 (corpus survey) and the invariants. ~~**§3, the loader contract,~~
~~is still empty**~~ *(answered: §3 is written — [Container/ebp2-container.md](Container/ebp2-container.md), `status: AUDITED`; 2026-10-02, OPUS)* and it is the point of the document: which fields the engine reads, what it
rejects, what it clamps, what it ignores. That needs the loader function read at tier 1.

~~**The sheet is deliberately not written yet.**~~ *(answered: it is written — [Container/ebp2-container.md](Container/ebp2-container.md); 2026-10-02, OPUS)* A `FORMAT.md` with an empty §3 would count in
`audit_coverage`'s denominator while explaining nothing — the metric defect this database keeps
finding in other forms.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings become reportable once citations written 0x... or FUN_... count (R5); tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Movement — CLIENT.** `WorldActorScriptVM_InterpretBytecode` is called by `WorldActor_UpdateRuntimeAndScriptExecutionState`, which the ledger files under Movement.
- **ActorEntity — SERVICE and CLIENT, 13 edges.** `WorldActorScriptVM_InterpretBytecode` calls `ActorResource_FindActiveEntryByIdOrClass`, `ActorResource_GetEntryByOrdinal`, `ActorResource_RecycleEntryRange` and a 50-byte actor helper. Two small cited functions are called by `ActorResource_OnPrimaryPayloadLoadedAndDispatchSubresources` and by two small actor bodies.
- **WorldAreaField — SERVICE (1 edge).** 1 outbound (page-cited `00332110` call WorldAreaField bodies `003DFE60`). Substantive edges include `00332110` calls `003DFE60`.
