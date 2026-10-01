---
system: <Short system name>
category: <parent category folder>
status: STUB | PARTIAL | DOCUMENTED | AUDITED | REOPENED
owner_layer: PrimaryOwner:<Category> | CodeDomain:<Path> | both
evidence_tier: 1-11 (see _index/EVIDENCE-STANDARD.md — lowest tier relied upon)
verified_against:
  # Take both from Database/Tools/ghidra/run/GfzEnv.ps1 ($GfzParentSha, $GfzParentSnapshot) at the
  # time you verify, and only after you have actually verified against that parent. These two go
  # STALE when the checkpoint advances; exe_sha256 below does not, because the authority image
  # never changes. A concrete hash used to sit here and it was GM160's - four generations back by
  # 2026-09-14 - so every page built from this template started life stamped to a parent nobody
  # had verified it against. No document inherited it, and it is a placeholder now for the same
  # reason FORMAT.md has always used one.
  gzf_sha256: <current checkpoint>
  snapshot_sha256: <current snapshot>
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: <YYYY-MM-DD>
# --- OPTIONAL, formats only. Delete both blocks if this document explains no format. ---
#
# registry_slots — which authored-data pointer-registry slots this document EXPLAINS.
#   Counted by check_formats.py into progress.py's `registry_explained` dimension
#   (denominator: 63, re-derived from the registry document's own bounds and stride).
#   ONE OWNER PER SLOT — a slot claimed by two documents is reported as a collision under
#   the standing no-address-described-two-ways rule.
#   Declare it only where this document establishes what the slot HOLDS. A mention is not an
#   explanation: `0x02EBF138` is mentioned in ten documents and explained in one.
# registry_slots:
#   - "0x02EBF0C0"
#
# archive_formats — shipped file extensions this document EXPLAINS, scored by check_assets.py
#   into `formats_explained` (48 extensions, censused over the 89,414-entry archive index).
#   Form: "ext" | "ext | disposition" | "ext | disposition | note", dispositions
#   explained (default) / standard / external. The latter two are REFUSED without a note.
#   Most documents want FORMAT.md instead; declare it here only when a SYSTEM document is
#   genuinely the reference for the file the system eats. See _index/ASSET-FORMATS.md.
# archive_formats:
#   - "sab"
#
# container_format — names a container/file format this document is the reference for
#   (`save-image`, `st2e`, `vbf-bigfile-index`, `game-settings-ini`, …).
#   COUNTED, NOT SCORED, and now for a narrower reason than before: it is for formats that are
#   NOT archive entries. Those ship loose in the install and still have no census, so a
#   percentage over them would be invented. Archive formats DO have one — `archive_formats:`
#   above — because the archive index enumerates every file the game ships.
# container_format: save-image
#
# ebp_units — for EBP container units, use FORMAT.md instead of this template. A section sheet
#   is a different genre: it opens with corpus validation and its centre is the loader contract,
#   not the call chain. This template is for SYSTEMS; FORMAT.md is for FILES.
audit:
  passes: 0                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: null              # YYYY-MM-DD
  last_pass_state: null        # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# <System name>

> One sentence: what this system is responsible for.

## 1. What the player sees

**Write this for someone who has played FFXII and never opened a disassembler.**

Describe the thing as it is *encountered*: what you see on screen, what you do with the
controller, what changes in the world, what you would notice if this system broke. Use the
names the game uses — Battle Menu, Agate Ring, Weather, the Zodiac Spear — not the names the
code uses.

A reader must be able to finish this section and correctly say *"oh, that's the thing that
does X"* without knowing a single address.

Test it: if every sentence here would still make sense read aloud to a player who is not a
programmer, it passes. If it needs a struct offset to make sense, it belongs in §2.

No code, no addresses, no offsets, no hex in this section.

## 2. Native mechanism

What the code actually does, in order. Enough detail that a reader could reimplement the
behaviour. Name the real primitives.

**Keep explaining in plain language as you go.** Technical does not mean unreadable. Every
time you introduce a mechanism, say what it *does for the player* before or alongside how it
works — "admits textures until the budget runs out, which is why a zone with too many
high-resolution textures silently drops some" beats a bare description of the loop.

A modder reading this should be able to follow the mechanism without already knowing the
subsystem. Assume they know the game well and the engine not at all.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `00000000` | `Name` | 000 B | what it does |

Addresses are Ghidra image base `0x00120000`. Body sizes are exact-current body extents.

**This table asserts "each of these addresses is a function."** `audit_crossrefs.py` reads it that
way and reports a `GHOST ADDRESS` for any row that is not one. So a `.data` / `.rdata` /
`.bss` address — a table, a constant, a global, a function *pointer* — **must not appear here**,
however important it is. Put it in a separate block, with no body-size column:

### Data addresses cited by this document

| Address | Name | Kind | Contents |
|---|---|---|---|
| `00000000` | `Name` | what kind of data | what it holds |

This split is not cosmetic. A body-size column on a data address is a false claim about the binary,
and it was the exact defect that produced ten spurious `GHOST ADDRESS` findings on 2026-09-02 in
three documents at once, after that check had reported zero in every prior pass. If an address is
cited only as a *value* (a constant a formula uses), prefer citing it inline in §4 instead.

## 4. Data structures and formulas

Records, offsets, bitfields, tables, enums. Give the exact offsets and widths.

**If the system computes anything, write the formula out.** Not prose describing it — the
actual expression, in a code block, as the engine evaluates it. This includes:

- damage / accuracy / stat formulas, with the real constants and divisors
- **condition expressions and gates** — the exact `if` a caller evaluates, including masks
- bit arithmetic: shifts, masks, packed-field extraction, index arithmetic
- budget, capacity, size and alignment arithmetic
- probability and RNG scaling

Write it so a reader can reproduce the engine's answer by hand. Give literals as they appear
(`0x80000003`, `/ 218`, `>> 0xf`, `0.00390625`) and name what each term is. If a formula is
composed from several stages, show the composition too.

```c
// good - the actual gate, reproducible
if (((bkbi->statusLayer0 | bkbi->statusLayer1) & 0x80000003) != 0 &&
     FieldData_GetActiveFieldRecordBit15() == 0)
        -> unit cannot act
```

A document that says "scales damage by a Strength-derived factor" instead of
`Strength * (Level + Speed) / 218 + 1` has not documented the formula.

**Write every record layout in a `struct` fence**, so the database can generate 010 Editor
templates, Kaitai specs and C headers from its own contents rather than someone re-extracting them
by hand later:

````
```struct StructName base=record size=0x24
+0x00  u32       fieldName   description
+0x04  u16[8]    masks       description
```
````

`+0xOFF` · `type` · `name` · comment. Types: `u8 u16 u32 u64 i8 i16 i32 i64 f32 f64`, `char[N]`,
`byte[N]`, any with `[N]`. `base=` says what offsets are relative to (`file`, `section`, `record`,
`payload`); `size=` optional. Validated by `check_layouts.py`, which flags unknown types,
overlaps, descending offsets, duplicate names, and reports gaps as **`UNACCOUNTED`**.

**An unaccounted range is a question, never a label** — `struct_map.py` exists because that
judgement was made by hand twice and was wrong twice.

## 4b. The loader contract  *(formats only — delete this section if not applicable)*

**Use this whenever the document explains a format: an authored table, a save image, a container,
a config file.** Section 4 says what the bytes *are*. This says **what the code does with them**,
which is the half a file-corpus reading cannot supply and a binary reading gets for free.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` | `Loader_ValidateHeader` (`00XXXXXX`) | magic != `st2e` | — | — |
| `+0x08` | `Loader_BindRecords` (`00XXXXXX`) | — | `[0, 0x3FF]` | — |
| `+0x1C` | — | — | — | **yes — no reader in this build** |

**`Inert` is the column a modder comes for.** A field nothing reads can be edited freely and
nothing will happen — and finding that out by experiment costs an evening. Mark it from the
absence of a reader in the binary, and say so; **"no reader found" is not the same as "inert"**
unless the search that failed is stated. Prefer *no reader found by <method>* when the search
has known blind spots (see `COVERAGE.md` — a displacement census stops counting where a base
pointer starts, and an instruction search cannot see undefined bytes).

Also record, when the format has them:

- **the version or format stamp**, its constant, and what changes when it differs;
- **what loading normalises** — fields the loader overwrites regardless of the file's contents;
- **the write path**, if the game writes this format. A file corpus never reveals the writer.

## 5. Call chain

The complete order, upstream to downstream. Say which transitions are the *owner*
transition and which are merely triggers.

```
upstream trigger
  -> intermediate
     -> THIS SYSTEM
        -> downstream consequence
```

**Upstream (who causes this):**

**Downstream (what this causes):**

**Do not confuse with:** neighbouring mechanisms that look similar.

## 6. Modding notes

- **Best intervention point:** the highest native transition that produces the desired
  outcome with the fewest direct writes.
- **Regenerates itself:** derived state you should *not* write directly.
- **Breaks if:** preconditions, ordering, threading requirements.
- **Multiplayer / XIIOnline:** what is authoritative world state vs. local derived state.
- **Mod compatibility:** which authored data other mods may legitimately change.

## 7. What is not known

Explicit list. Every entry here must also appear in `_index/OPEN-QUESTIONS.md`.
An empty list is the goal; a *missing* list is a defect.

- [ ] unknown thing

## 8. Evidence

How each non-obvious claim was proved, with the tier.

| Claim | Evidence | Tier |
|---|---|---|
| … | complete exact-current body of `00000000` | 1 |

**Superseded readings:** anything previously believed and later corrected, with why.

## 9. Related

- `../other-category/other-system/doc.md` — relationship
  *(make these real relative links in a real document; they are plain text here so the
  link checker does not flag the template)*
