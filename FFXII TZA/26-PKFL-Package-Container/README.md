# 26 — The PKFL package container

**`PKFL` is the second EBP, and slightly larger.** 10,314 shipped files against EBP's 10,045, an
indexed directory like EBP's, and — like EBP — **one container format wearing several extensions**:

| ext | files | size | archive tree |
|---|---:|---:|---|
| `.mot` | 4,392 | 2,552 MB | `ps2data/plan_master` |
| `.snd` | 2,304 | 146 MB | `ps2data/plan_master` |
| `.vpc` | 1,809 | 1,240 MB | `ps2data/plan_master` |
| `.vpcjp` | 1,809 | 1,298 MB | `ps2data/plan_master` |

**Sampled 160 files across all four: 160/160 carry the `PKFL` magic.** The extensions say what a
package is *for*; they do not say it is a different format.

> **This category exists because `.mot` was nearly documented as "a motion format".** It is not.
> It is a package that happens to hold motion, and `.snd` / `.vpc` / `.vpcjp` are the same package
> holding other things. Filing them under Audio and Presentation separately would have split one
> mechanism across two categories and produced four partial readings of one layout.

## CENSUSED — 10,314 of 10,314, 2026-09-04

`census_pkfl_container.py` → `Tools\work\formats\pkfl-container-census.tsv`. **Every shipped file
parsed; zero failures.** The sample estimate below is superseded — and it was wrong *in kind*, not
merely in number.

### The directory size is decided by the extension pair

| slotCount | files | extensions |
|---:|---:|---|
| **16** | 6,696 | `.mot` (4,392) + `.snd` (2,304) |
| **64** | 3,618 | `.vpc` (1,809) + `.vpcjp` (1,809) |

**No file mixes them.** The 16/64 question is answered: it is not a version, it is which pair of
extensions the package belongs to.

### Slots are strictly PAIRED — and this is the finding

> ### ⚠ Withdrawn 2026-09-11 — the pairing is the directory's entry width
>
> A directory entry is **`{u32 offset, u32 size}`**, eight bytes, so the "odd slot" of every pair
> is the size of the even one, and this section's headline, its medians and the aliasing story
> below all read sizes as offsets. The engine loads `0x88` / `0x208` bytes as the directory and
> indexes pairs by slot (`0032F320` / `0032F360`);
> [the container sheet](Container/pkfl-package-container.md) §2, §5 and §8 carry the correction and
> the re-measured invariants. Kept as history.

~~**Every occupied slot has its even/odd partner present. Zero exceptions in 10,314 files.**~~

| pair | files | even slot median | odd slot median |
|---|---:|---:|---:|
| 0/1 | 7,407 | 71,888 B | 2,976 B |
| 2/3 | 7,380 | 47,696 B | 3,056 B |
| 4/5 | 5,445 | 24,928 B | 8,208 B |
| 6/7 | 4,320 | 2,048 B | 192 B |
| 8/9 · 10/11 · 12/13 | 3,636 · 3,204 · 2,934 | 2,048 B | **0 B** |
| 14/15 | 2,646 | 49,152 B | 1,984 B |
| 16/17 · 18/19 | 54 each | | |
| 20/21 | 36 | | |
| 22/23 · 24/25 · 26/27 | 18 each | | |

> ### ⚠ The reading below was WRONG. Corrected 2026-09-04 by the container sheet.
>
> This README originally said: *"the even slot carries the payload and the odd slot is a small
> companion — often zero bytes… the DAT/CTL shape, appearing again one container up."*
>
> **The zero-byte medians are an artefact of my own census, not a property of the format.**
> [The container sheet](Container/pkfl-package-container.md) re-parsed all 10,314 files and found
> that **slots share offsets**: 2,349 files have two or more slots pointing at the same place, and
> **2,385 of 2,403 duplicate groups are entirely odd slots, 2,259 of them pointing inside the
> directory itself.**
>
> In `alc_a0100.snd`, slots 1, 5, 7, 9, 11, 13 and 15 all carry offset `0x40` — which is slot 14's
> *own directory entry*. The bytes there are the pair of directory words read as data. It is a
> canonical **"this half is empty"** marker, cheaper than a null.
>
> **Computing a slot's length as the distance to the next present offset gives an aliased slot a
> length of 0.** That is exactly where my `0 B` medians for slots 9, 11 and 13 came from, and the
> *last* alias in a group gets a spurious ~1,984 B spanning the gap to the first real payload.
> **Neither number was ever a payload size, and I read them as one.**

**What survives.** *"Every occupied slot has its even/odd partner"* is **true, 10,314 / 10,314** —
but it is **partly an artefact of that aliasing rather than of every partner carrying data.** The
invariant as counted is correct; **what it implies about content is weaker than it looks.**

**So the 14-pair denominator is NOT established, and no sheet should be scored against it yet.**
The pairing is a real structural fact and a poor unit of explanation until the container sheet's
open questions are settled. **The denominator was inferred from medians that were measurement
artefacts** — the census's one job was to fix a population *before* anyone wrote against it, and it
came within one careful re-parse of fixing the wrong one.

Two further corrections from the same re-parse: **offsets are not ascending in slot order** (unlike
EBP), and **the first payload is not at the directory end** — in 2,268 files the smallest offset is
`0x40`, *before* the 16-slot directory ends at `0x48`.

### The directory IS sparse — correcting this script's first answer

**36 of the 64 declared slots are never used in any of the 3,618 64-slot files.** Nothing above
index 27 is ever occupied.

> **The census script's first run announced the opposite** — *"0 never present, a DENSE directory,
> absence carries no information."* That conclusion was **produced by construction**: it ranged only
> to the highest *occupied* index, and a range that stops at the last occupied slot cannot contain
> an empty one. Fixed to range over the *declared* `slotCount`.
>
> This is the metric-that-returns-its-value-by-construction failure in `EVIDENCE-STANDARD.md`,
> committed by the coordinator, in a script written to avoid exactly that class of error.

So PKFL is bounded the same way EBP is: **the always-zero slots are how the population is fixed.**

### Pair index carries meaning — it is not a list position

**2,952 files do not fill their pairs contiguously from 0.** If the directory were a simple list of
N tracks, every file would occupy pairs 0..k-1. Nearly a third skip. **So a pair index is a typed
slot, not a sequence number** — which is what makes 14 a population rather than a maximum.

Pairs per file range 0–14; 4,212 files carry exactly one pair, 2,331 carry eight, and **27 files
carry none at all** — a PKFL container with an empty directory.

## What the sample said before the census (superseded)

**Measured** (container-detection sweep + 160-file sample, 2026-09-03):

- indexed directory: a leading count followed by that many ascending, in-range offsets
- **two slot-count variants — 16 slots (108 of 160) and 64 slots (52 of 160)**
- **28 distinct slot indices occupied, indices 0–27, none skipped**

**Not measured, and required before any sheet is written:**

- the full slot census over the whole corpus, not a 160-file sample
- whether the 16-slot and 64-slot forms are versions, or two different package kinds
- **what each slot index holds** — nothing here claims to know
- the header beyond the count, and whether a magic/version field is validated

> **A densely packed directory is the opposite of EBP's.** EBP's 20 slots are sparse — seven are
> permanently zero, which is *how the census learned they existed*. PKFL indices 0–27 are all
> occupied, so **absence carries no information here** and the census must be read from occupancy
> frequency instead.

## Do the census before the sheets

**This is not optional and the precedent is one folder over.** `25-EBP-Script-Container` has a
trustworthy 14-unit denominator for exactly one reason: **it was censused before anyone wrote a
sheet.** `census_ebp_container.py` derived occupancy from the container's own directory across
1,115 files, and it independently confirmed a denominator that had been produced by a completely
different route.

Writing PKFL sheets against the four *extension* rows would repeat the extension-versus-format
error at more than twice EBP's scale — and it would surface afterwards instead of before. The
sequence is:

1. **Census** — a `census_pkfl_container.py` mirroring `census_ebp_container.py`: parse the header,
   read the directory, report occupancy per slot index over all 10,314 files, freeze it to a TSV.
2. **Denominator** — a `check_pkfl.py` scoring the frozen unit list, one owner per unit.
3. **Then sheets**, to `_templates/FORMAT.md`, one file per unit.

**Until step 1 lands, the unit count in this README is a sample estimate and must be quoted as
one.** *"~28 units from 160 files"* is not *"28 units"*.

## Folders

| folder | holds |
|---|---|
| `Container/` | the `PKFL` header and its directory — the layout every slot sheet builds on |
| `Slots/` | one sheet per slot index, once the census fixes the population |
| `Variants/` | the 16-slot versus 64-slot question, and any version field |

## Where it sits

The container is documented here. **What a slot's payload *means* belongs to the owning system** —
motion payloads to `17-Presentation-Rendering`, audio payloads to `18-Audio` — and those documents
cross-link here rather than re-describing the wrapper.

## Related

- [`_index/ASSET-FORMATS.md`](../_index/ASSET-FORMATS.md) §4d — the measurement behind this category
- [`25-EBP-Script-Container`](../25-EBP-Script-Container/README.md) — the pattern this follows
- `Tools/work/formats/format-magic-census.tsv` — the signature census that grouped the four extensions
