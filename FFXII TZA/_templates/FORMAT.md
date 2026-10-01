---
system: <Format or section name — e.g. "EBP section_008" or "st2e authored table container">
category: <parent category folder>
status: STUB | PARTIAL | DOCUMENTED | AUDITED | REOPENED
owner_layer: PrimaryOwner:<Category> | CodeDomain:<Path> | both
evidence_tier: 1-11 (see _index/EVIDENCE-STANDARD.md — lowest tier relied upon)
verified_against:
  gzf_sha256: <current checkpoint>
  snapshot_sha256: <current snapshot>
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: <e.g. "1115 / 1115 us .ebp scripts, 2026-09-03">
last_reviewed: YYYY-MM-DD
# --- Declare exactly the units this document EXPLAINS. Declared, never scraped. ---
# One owner per unit; a unit claimed twice is reported as a collision.
#
# ebp_units:           check_ebp.py -> `ebp_explained` (14 units: container + 13 sections)
#   - "container"
#   - "section_008"
#
# registry_slots:      check_formats.py -> `registry_explained` (63 authored-data slots)
#   - "0x02EBF0C0"
#
# archive_formats:     check_assets.py -> `formats_explained` (48 shipped extensions, censused
#                      over the 89,414-entry archive index by census_archive_formats.py)
#   Form: "ext", or "ext | disposition", or "ext | disposition | note".
#   Dispositions: explained (default) | standard | external.
#   `standard` and `external` are REFUSED without a note and do not count — the cheap disposition
#   is the one that makes you write down a checkable claim. See _index/ASSET-FORMATS.md §3.
#   - "sab"
#   - "webm | standard | WebM/Matroska container, VP8 video"
#   - "phyre | external | ffxii-tza-tools docs/formats/phyre.md"
#
# container_format:    counted, NOT scored — for formats that are NOT archive entries (the save
#                      image, the VBF container itself, GameSetting.ini). Those ship loose and have
#                      no census, which was always the stated reason for not scoring them.
# container_format: st2e
audit:
  passes: 0
  last_pass: null
  last_pass_state: null
  crossref_clean: false
  reopened_count: 0
---

# <Format or section name>

> One sentence: what this holds and who reads it.

**Corpus validation, before anything else.** A format claim without a file count is a guess about
one file:

| | |
|---|---|
| files examined | *e.g. 1,115 of 1,115 `us` `.ebp` scripts* |
| this unit present in | *e.g. 423 (37.9 %)* |
| co-occurrence | *e.g. always with `section_009`; never observed alone in 1,115 files* |
| size range | *e.g. 64 B – 3,584 B, median 448 B* |

**If a claim below holds for every file, say so. If it holds for the one you opened, say that
instead.** The difference is the whole value of this section.

> **A `standard` or `external` disposition does not excuse §3.** Naming the spec says what the
> format is; it does not say what *this build* accepts, rejects, clamps or ignores — and that half
> is the only part no external reference can supply. A sheet that names a standard and stops has
> documented the format and not the game.

---

## 1. What the player sees

**Write this for someone who has played FFXII and never opened a hex editor.** A section of a
script file still causes something: a door works, a chest has contents, the weather changes, a
cutscene camera moves. Name it in the game's own words.

If the honest answer is "nothing directly", **say that plainly** rather than inventing a
player-facing story — and then say what it *causes*.

## 2. The layout

**Write every layout in a `struct` fence.** Same block you would have written by hand, with the
columns fixed so a machine can read it too:

````
```struct EbpContainer base=file size=0x80
+0x00  u32       magic       'EBP2'
+0x04  u32       slotCount   always 0x14 = 20
+0x08  u32       _reserved0  always 0 in 1,114 of 1,114
+0x0C  u32       _reserved1  always 0 in 1,114 of 1,114
+0x10  u32[20]   sectionOff  INDEXED BY section number, 0 = absent
```
````

`+0xOFF` · `type` · `name` · free-text comment. Types: `u8 u16 u32 u64 i8 i16 i32 i64 f32 f64`,
`char[N]`, `byte[N]`, or any of those with `[N]` for an array. `base=` names **what the offsets are
relative to** — `file`, `section`, `payload`, `record`. `size=` is optional.

> **`base=` is not bureaucracy.** Chunk start, payload start, file start and section start are four
> different origins, and mixing them is the most common way a format sheet goes wrong.

`check_layouts.py` validates every fence: unknown types, overlapping fields, descending offsets and
duplicate names are all errors, and **gaps are reported as `UNACCOUNTED`** — in the same spirit as
`struct_map.py`, where *leftover space is not evidence of what occupies it.* **An unaccounted range
is a question, never a label.**

**Why the fence matters beyond tidiness:** one strict block is enough to generate 010 Editor
templates, Kaitai specs, ImHex patterns and C headers from the database itself. The prose stays the
deliverable; those are a lossy view of it. **Lossy because none of them can carry §3** — a template
shows what bytes *are*, and cannot tell you a field is read by nothing.

## 3. The loader contract

**The point of this document.** Section 2 says what the bytes *are*; this says **what the engine
does with them** — the half a file-corpus reading cannot supply.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` | `Loader_ValidateHeader` (`00XXXXXX`) | magic mismatch | — | — |
| `+0x08` | `Loader_BindRecords` (`00XXXXXX`) | — | `[0, 0x3FF]` | — |
| `+0x1C` | — | — | — | **yes — no reader found by \<method\>** |

**`Inert` is the column a modder comes for.** A field nothing reads can be edited freely and
nothing happens; finding that out by experiment costs an evening.

> **"No reader found" is not the same as "inert"** unless the search that failed is named.
> `COVERAGE.md` catalogues seven ways a census goes blind — a displacement search stops counting
> where a base pointer starts, an instruction search cannot see undefined bytes, a wide store is
> credited to one field, a constant can be built by arithmetic. **Write *"no reader found by X"*,
> not *"unused"*.**

Also record, where the unit has them:

- **the version or format stamp**, its constant, and what changes when it differs;
- **what loading normalises** — fields the loader overwrites regardless of file contents;
- **the write path.** If the game writes this, say how. A file corpus never reveals a writer.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00XXXXXX` | the loader | ✅ |

## 5. Corpus survey

What varies across the corpus and what never does. **Invariants are findings**: a field that is
`0` in 1,115 of 1,115 files is a different fact from a field nobody has looked at.

Outliers deserve their own line — *"one file has no `section_000`"* is worth more than a paragraph
of averages.

## 6. Falsification pass — YYYY-MM-DD

| attack | result |
|---|---|
| Is the offset relative to the file or the section? | |
| Does this hold on the whole corpus or on the file that was opened? | |
| Could the decompiler have invented a value the instruction stream does not have? | |
| If an external tool agrees, was it consulted **after** the reading or **before**? | |

**If an external tool reads this format, it is an oracle and not an authority.** Use it to
falsify — where the loader reading and the tool disagree, say so and resolve it. **A claim resting
on the tool is tier 6 at best and must say so.** Consulting it first and then "confirming" from the
binary is not a check; it is a way to inherit its errors.

## 7. What this document does not claim

Name the fields left unread, the invariants unexplained, and the searches that came back empty
**with the method that failed**.

## 8. Related

- the consumer of this data
- the format sheet upstream or downstream of this one
