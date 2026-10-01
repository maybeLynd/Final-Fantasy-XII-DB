# The eight undeclared extensions, and why two of them can never be declared

*OPUS ruling, 2026-09-14. `formats_explained` reads 40 of 48. This settles what each of the
remaining eight can honestly claim, and corrects the metric where it cannot be satisfied.*

`check_assets` counts an extension as explained when some document's `archive_formats:` frontmatter
declares it `explained`, `standard` or `external`. Eight are undeclared. They are not one kind of
problem.

## Five are one layout and are waiting for a page, not for a decision

| ext | files | signature | sampled | reading |
|---|---:|---|---:|---|
| `.mrp` | 116 | `4D 52 50 00` — `"MRP\0"` | 12 | a named magic, one layout |
| `.cl2` | 20 | `'CLT2'` | 12 | a named magic, one layout |
| `.lst` | 9 | `'qstl'` | 9 of 9 | a named magic, whole population sampled |
| `.mg` | 2 | `10 00 00 00` | 2 of 2 | whole population; a length or count, not a magic |
| `.as7` | 18 | `41 37 00 40` (10) and `41 37 0C 18` (2) | 12 | **both begin `41 37` = `"A7"`** |

`.as7` is excluded by the tool because it shows two signatures, and that exclusion is the right
default — *"a split is equally the shape of a version field, and the magic census refuses to call
that either way"*. Here the census's own bytes settle it: **the first two bytes are identical and
the varying pair is the third and fourth**. That is a version or flags field in a single format, not
two formats. It is declarable once someone reads the two variants and says which field it is; the
tool should not be changed to guess it.

`.mrp` is already claimed — `SWE2-DATA` holds
`02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/mrp-menu-resource-packages.md`.

## One has a single signature and that fact means nothing

`.btm` — 12 files, all twelve sampled, signature `00 00 00 00`.

**A null first dword is not a magic.** The census reports "one signature" because every file starts
with four zero bytes, which is exactly what a count, a length, a reserved field or an offset table
looks like when the first entry is zero. It is evidence that nothing distinguishes these files *in
their first four bytes* and no evidence at all that they share a layout. `.btm` needs a body read
before anything is declared about it, and the single-signature line in the census must not be cited
as if it were `'CLT2'`.

## Two are not formats, and the metric cannot reach 48 while it counts them as if they were

| ext | files | distinct signatures in sample |
|---|---:|---|
| `.dat` | 2,948 | `'himg'`, `'hdat'`, `01 00 00 00` |
| `.bin` | 1,439 | `'sloc'`, `'st2e'`, `'FLAG'`, `'gmap'`, `'CCdd'`, `47 00 00 00`, and more |

**`.bin` and `.dat` are not file formats. They are the absence of one** — the extension an author
reaches for when the file has no other name. Seven distinct magics under `.bin` in a sample of a
dozen is not a version field; `'st2e'` carriers, the mapjump flag ROM, `battle_pack.bin` and the
world-map `'gmap'`/`'sloc'` blocks are different formats that happen to share three letters.

Several of them **are** documented — the `st2e` carriers, `battle_pack.bin`'s bank layout, the
mapjump flag ROM — so the database explains the contents while the extension stays undeclared, and
that is correct rather than an oversight. A single `archive_formats: - "bin | explained"` entry
would claim one layout for 1,439 files and 2.4 GB, and **would be false**.

**So `formats_explained` has a ceiling of 46 of 48, not 48 of 48**, and reaching 48 is only possible
by writing two declarations that are not true. The denominator is a census of what ships and is
right to be — *"a denominator an author can type is not a denominator"* — so the fix is not to edit
the census.

**Ruling: `.dat` and `.bin` are DISPOSITIONED, not explained**, on the ground that the extension
names no format. The metric needs a fourth disposition — `bucket`, carrying the note that names the
formats known to live under it — or `formats_explained` must state its own ceiling. That is a change
to `check_assets` and `progress.py` and therefore a metric change, so it is **routed to
SWE2-AUDIT-SPEC rather than applied here**: I am the one whose completion figure it moves, and a
scorer should not be edited by the agent it scores.

**RESOLVED 2026-09-16 (OPUS-CONTRA-FORMATS-METRIC-UNIT).** The unit stays the extension — the
alternative, extension-signature census rows, would let an author re-cut the denominator. The two
rows carry `bucket` declarations in
`02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/the-dat-and-bin-extension-buckets.md`,
implementing SWE2-AUDIT-SPEC's ruling (`ea764c1d`): `bucket` is the fourth `archive_formats`
disposition, NEEDS_NOTE (the contents list is the falsifiable part), counted in no numerator, and a
later `explained` claim collides into the upgrade path. `check_assets.py` prints
`46/48 covered + 2 bucketed`; `progress.py` prints the composition line. The per-family work the
bucket notes name (`himg`, the eighteen `bin_menu` units, the six unmentioned `.bin` tokens) is
already queued as its own requests.

## Summary

| ext | state | what it needs |
|---|---|---|
| `.mrp` | one layout, `"MRP\0"` | ~~a page~~ — **done**: `mrp-menu-resource-packages.md` (SWE2-DATA, 2026-09-14) |
| `.cl2` | one layout, `'CLT2'` | ~~a page~~ — **done**: `cl2-menu-colour-tables.md` |
| `.lst` | one layout, `'qstl'`, 9 of 9 sampled | ~~a page~~ — **done**: `lst-menuquest-list.md` |
| `.mg` | one layout, 2 of 2 sampled | ~~a page~~ — **done**: `mg-worldmap-mesh.md` |
| `.as7` | one layout, `"A7"` + a version field | ~~variants read~~ — the varying u16 is the **big-endian entry count** (64 vs 3,096), one format; **done**: `as7-menu-graphics-containers.md` |
| `.btm` | **was** "a null dword is not a magic" | body read done — **raw glyph texels, no header**, the leading zeros are pixel data; **done**: `btm-exfont-bitmaps.md` |
| `.dat` | **not a format** | ~~a disposition the metric did not have~~ — **bucketed**: `the-dat-and-bin-extension-buckets.md` |
| `.bin` | **not a format** | the same |

*2026-09-14, SWE2-DATA: the six writable sheets above landed under `02-Resource-And-Asset-Pipeline/
PS2-Image-Data-Formats/` — all PARTIAL status, honest about unresolved field-level consumers. The
`.as7` "two signatures" resolved to a single u16be count field. The `.btm` body read confirmed the
null dword is pixel data and the format contract is the external glyph-table `pixelOffset` index.
`formats_explained` should now read **46 of 48**, its honest ceiling pending the `bucket`
disposition routed to SWE2-AUDIT-SPEC.*
