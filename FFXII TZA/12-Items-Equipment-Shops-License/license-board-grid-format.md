---
system: The License Board grid files — `licd`, the 24x24 node layouts
category: 12-Items-Equipment-Shops-License
status: AUDITED
owner_layer: PrimaryOwner:Items_Equipment_Shops_License
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
  parent_tag: GN160
corpus_validated: "13 of 13 licd units x 4 locale copies = 52 files, 2026-09-05; the four license_data.bin copies re-read and the language path arrays decoded, 2026-09-11"
container_format: licd
last_reviewed: 2026-09-11
archive_formats:
  - "licd | explained | board_#.bin / license_board.bin (.bin member, 13 units): {licd, u16 width, u16 height, u16 cell[w*h]} - grid builder 0055B3F0 and cell readers 00328990 / 0055E2C0 / 0055E600, section 3"
  - "licensechip | explained | license_chip.bin (.bin member): 361 ids x 2 variants x 32-byte records of four 8-byte layers {u16 sprite, u16 value, u8, u8, s8 dx, s8 dy} (23,104 B) - (kind 7, 0x7E) by 00561390 into 02CA9670, drawn by 0055BAC0, value read by 00556590 / 0055F010, section 6b"
audit:
  passes: 1
  last_pass: 2026-09-06
  last_pass_state: GN160-corpus-and-code-reparse-repos-1e — all 52 files re-detected and re-parsed, cited instructions re-decoded; 13/13 claims exact including the ch=in / cn=kr relocation of node 360, plus one addition (the 12 job boards cover only 347 of the 361 ids)
  crossref_clean: true
  reopened_count: 0
---

# The License Board grid files — `licd`

> **The shape of the License Board itself.** Thirteen files, each a 24x24 grid saying which squares
> exist and which node sits in each one. Twelve of them are the job boards; the thirteenth is a
> different board entirely.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **52** — 13 units x 4 locale copies (`ch`, `cn`, `in`, `kr`) |
| units | **13**: `license_board.bin` and `board_1.bin` … `board_12.bin` |
| magic `licd` at `+0x00` | **13 / 13** |
| file size | **1,160 bytes — every one of the 13, no exceptions** |
| grid | **24 x 24 in 13 / 13**, and `8 + 24*24*2 = 1160` **exactly — zero bytes unaccounted** |
| distinct contents | **13 of 13 differ**; no two boards are the same file |

> **A fixed 1,160 bytes across every unit, with the grid filling the file to the byte, is the
> strongest structural fact here** — there is no header slack, no trailing table and no padding for
> anything else to hide in.

---

## 1. What the player sees

**The License Board.** The grid you open from the menu to spend LP: a lattice of squares, most of
them blank, each filled one granting an ability, an item slot, a stat boost or a magick. You unlock
squares adjacent to ones you already own, so the *shape* of the board — which squares exist and
where — is what decides the order a character can grow in.

**In the Zodiac Job System each job has its own board**, and that is what the twelve `board_N` files
are: twelve different 24x24 layouts, one per job, each with **128 to 143 filled squares** out of 576
positions. A Knight's board and a Black Mage's board are different files with different squares in
different places, which is the whole reason picking a job matters.

`license_board.bin` is **not** one of the twelve and is not shaped like them: it has **300 filled
squares**, more than twice any job board, and its numbering is a dense run with no gaps. §5 sets out
what is and is not established about it.

**What this file does not contain:** what any square *grants*. A square holds a **node number**, and
the node table lives elsewhere — see §2.3 and
[`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md),
which documents what the engine does with a node the player already owns.

## 2. The layout

**All offsets are from the start of the file.** The whole file is a header and a grid.

### 2.1 Header — 8 bytes

```struct LicdHeader base=file size=0x8
+0x00  char[4]  magic   'licd' - bytes 6C 69 63 64, in 13 of 13
+0x04  u16      width   24 in 13 of 13
+0x06  u16      height  24 in 13 of 13
```

### 2.2 Grid — `width * height` cells of `u16`, starting at `+0x08`

```struct LicdCell base=record size=0x2
+0x00  u16  node  node number, or 0xFFFF for an empty square
```

Row-major, `cell[row * width + col]`, `24 * 24 = 576` cells at 2 bytes each. **`8 + 1152 = 1160` is
the whole file in all 13 units**, so the grid is the entire payload and the dimensions in the header
are consistent with the file size rather than merely plausible.

**`0xFFFF` means "no square here."** Between 433 and 448 of the 576 positions are empty in a job
board, which is what makes the boards look like lattices rather than solid blocks.

**No node number repeats within a board.** Measured on all 13 units: the count of live cells equals
the count of distinct live values, every time. A node appears at most once on any given board.

### 2.3 What the node number indexes — bound, with one exception

The node numbers used across all 13 boards are **exactly `0 … 360`, all 361 values, with no gaps.**

`license_data.bin` — shipped in the same folder, `st2e` — declares its own record count in its
header, and the arithmetic closes exactly:

```
32 + 360 * 24 = 8672 = the file size          (headerSize + count * recordSize)
```

So the node table holds **360 records, valid indices `0 … 359`** — and the boards use **361**
distinct values. **The id space is one larger than the table it indexes**, and §5 shows that the
extra value is not a rounding artefact but a specific, identifiable square.

> **This is deliberately stated as a binding with a hole in it, not as a clean join.** The
> `st2e` sheet already downgraded a `543 records against 543 ids` match to a lead (open question
> **AY-6**) on its own falsification pass, because a count match is suggestive and not deciding.
> **Here the counts do not even match** — 361 against 360 — so the binding is offered as the
> reading the arithmetic supports and the discrepancy is §5's subject rather than something smoothed
> over.

## 3. The loader contract

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| `+0x00` magic | — | **never** | — | **yes.** `licd` occurs **0 times in the whole 32,864,752-byte image**, as ASCII or as the dword `0x6463696C`. Nothing compares it |
| `+0x04` width | ~~—~~ **u8 by the view's grid builder `0055B3F0` (`0055B484`, stored +1 at view `+0x559`, [OPUS](../16-UI/License-Board-View/the-license-board-grid-build-and-its-change-sweep.md)); u16 by `00328990` (`003289F0`), `0055E2C0`, `0055E600`, `00560070`, `0055F830`, `003FC900`** | — | — | ~~**no reader found** — see the boundary below~~ *corrected 2026-09-13* |
| `+0x06` height | ~~—~~ **u8 by `0055B3F0` (`0055B493`, stored +1 at view `+0x55A`); u16 by the same six functions (`003289D3`)** | — | — | ~~**no reader found**~~ *corrected 2026-09-13* |
| grid cells | ~~—~~ **u16 `cell(col, row) = [blob + (row × width + col) × 2 + 8]`, `0xFFFF` when `col ≥ width` or `row ≥ height`: `00328990` (`00328A0C`–`00328A14`), `0055E2C0` (`0055E33D`–`0055E345`), `0055E600` (`0055E788`, `0055E87D`), `00560070` (`00560113`, `00560176`), `0055F830` (`0055F95A`), `003FC900` (`003FC9B4`)** | — | out of range → `0xFFFF` | ~~**no reader found**~~ *corrected 2026-09-13* |

**The magic is not validated.** That is a definite result, not an absence of searching: the constant
does not occur in the image in either form. Contrast `SHK1`, `CAM7` and `LGT2`, each of which occurs
exactly once, as a `cmp` immediate. **A modder can change `licd` to anything and nothing will
notice** — with the caveat §6 records about arithmetic-built constants.

### How the file is located, which is established in full

The boards are not opened by name at the point of use. Each is an entry at a **fixed index in a
per-locale path table**:

| index | file |
|---:|---|
| 70 | `license_board.bin` |
| 71 … 82 | `board_1.bin` … `board_12.bin` |

**Measured in 6 of 6 locale tables examined** (`ch`, `cn`, `de`, `fr`, `in`, `uk`): the thirteen
board paths sit at exactly indices 70-82, in the same order, every time. **`board_N` is at index
`70 + N`**, so the job number and the table index are the same number offset by a constant. The
requests for them are tracked in registry slots `02EBF1A0`–`02EBF1F8`: `BattleStorage_InitializeWorkArrays`
requests loader ids `0x47 + k` — the same indices — and a generated setter marks each completion (the
bytes live in the loader's resource block, not in the slot)
([the registry page](../02-Resource-And-Asset-Pipeline/authored-data-table-registry.md), *the tail
read*; sized at 1,160 bytes each by [the file-size table](../02-Resource-And-Asset-Pipeline/Loose-Files-And-Size-Tables/file-size-tables-fst.md), 2026-09-11).

That table is populated by **`FUN_002DF9A0`**, which is called **exactly once** — from
`FUN_0022A0B0` at `0x0022A159`, inside boot initialisation. It has zero image-base-relative
references and zero absolute pointers anywhere in the image, so **there is no second path to it.**
`FUN_002DF9A0` writes each path into a runtime object; the store for `board_1.bin` is visible at
`0x002E0052` — `mov qword ptr [rax + 0x238], rcx`, and `0x238 = 71 * 8`, the array index in bytes.

> **So a board's path is fixed for the life of the process at startup.** Nothing resolves it per
> request, and the index is a compile-time constant rather than a lookup by name.

**The write path: there is none.** Nothing in the executable writes a `licd` file. The board layouts
are authored offline and only read.

### The boundary — what is NOT established

~~**What parses the grid is not known, and the search that failed is named.**~~ **Corrected 2026-09-13 (FABLE, on OPUS-REQ-LICD-HEADER-READER): the grid has readers, and the failed search looked in the wrong place.** Every function that indexes the board slot array `02EBF1A0` + board × 8 was followed from the loaded blob pointer to its displacements (eleven functions): the view's grid builder `0055B3F0` reads the header bytes (OPUS); **six functions read cells** with the row-major formula in the table above — `00328990` (called from `00328BD0`), `0055E2C0` and `0055E600` (both called from `0055C530`), `00560070` (called from `00511F50`), `0055F830`, and `003FC900`, which then indexes the licence data table `02EBF038` by the cell value (`003FC9E8`–`003FC9F0`). *The first pass of this census tracked the blob pointer by register and lost it where `0055F830` and `003FC900` reload it from the slot (`003FC990`); those two were re-read by instruction.* **What a cell is:** `00328990(stats, bit, board)` rejects `board > 11` (`003289A4`), walks every cell, uses the u16 as a licence id in a class-`0x20` record query (`0031C5D0`, `00328A2D`–`00328A35`), and for each id that is learned (stats `+0x194` bitmap, `00328A51`) but whose record lacks `bit` in its mask byte, clears the learned bit (`00328A73`) and adds the record's cost to LP `+0x190`, capped at 99,999 (`00328AC2`–`00328AF2`) — **a cell is a licence id, and a board can be un-learned with refund.** The earlier paragraph, kept:  All rip-relative
references to the eight runtime path-table globals (`0x0215F008`, `0x0215F010`, `0x0215F028`,
`0x0215F038`, `0x0215F040`, `0x0215F048`, `0x0215F0A8`, `0x0215F128`) resolve into **one function —
`FUN_002DF9A0` itself**, the populator. The consumers reach the object some other way: as a call
argument, or through an accessor. **An address-based scan cannot follow that**, which is the same
structural limit recorded in `COVERAGE.md` for a base held in a register.

So §3 is honest about its own shape: **the location contract is complete and the parse contract is
empty.** Opened as **PROPOSED-repos-c7-11**.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `0x002DF9A0` | populates the per-locale path table; the board paths are indices 70-82 | partial — entry, the board store, the store block |
| `0x002E0052` | `mov qword ptr [rax + 0x238], rcx` — the `board_1.bin` path store, `0x238 = 71 * 8` | ✅ |
| `0x0022A0B0` | boot initialisation, the sole caller | partial — the call site and its surrounding block |
| `0x0022A159` | `call 0x2df9a0` — the only call to the populator | ✅ |
| `0x0215F038` | runtime path-table pointer, 270 rip-relative references, all inside `FUN_002DF9A0` | data |
| `0x00A79EB5` | the `board_1.bin` path string | data |
| `0x00A78E85` | the `license_board.bin` path string | data |

## 5. Corpus survey

**Invariants — every one measured over all 13 units, and over all 52 files where locale matters.**

| | |
|---|---|
| `licd` magic, 24 x 24, 1,160 bytes | **13 / 13** |
| grid fills the file exactly (`8 + w*h*2 == size`) | **13 / 13**, 0 bytes left over |
| no node number repeats within a board | **13 / 13** |
| node numbers used across all boards | **exactly `0 … 360`, no gaps** |
| `license_board.bin` locale copies byte-identical | **yes — 4 / 4** |
| job board locale copies byte-identical | **no** — see below |

**Filled squares per unit:** `license_board` 300; job boards 128 (`board_3`, `board_9`) to 143
(`board_4`), median 137.

### `license_board.bin` is a different kind of file

- **300 filled squares**, against 128-143 for a job board.
- Its numbers are **exactly `0 … 299`, dense, no gaps** — a complete consecutive run.
- It is the **only unit whose four locale copies are byte-identical**.
- It contains **no node 360**.

**What it is, is not established here.** A dense `0 … 299` layout is the shape of a board that
carries every node in one grid, which is what the single pre-Zodiac License Board was — but that is
an argument from shape and from the game's history, not a reading, and this sheet does not make it.
Recorded as **PROPOSED-repos-c7-12**.

### Node 360 — three independent properties, all singling out one square

This is the corpus's sharpest outlier and it was found twice by accident before it was tested for.

| property | measurement |
|---|---|
| out of range of the node table | `license_data.bin` holds **360** records, valid `0…359`; **360 is not one of them** |
| appears exactly once per job board | **12 of 12**, one cell each |
| absent from `license_board.bin` | **yes** |
| **the only value that ever differs between locale variants** | **12 of 12 job boards**, and no other value ever moves |

**The locale split is `ch`/`in` against `cn`/`kr`.** Within each job board, exactly two cells differ:
one holds 360 in `ch`/`in` and `0xFFFF` in `cn`/`kr`, the other the reverse. **The square is
relocated, not added or removed** — the board keeps the same number of filled squares either way.
`ch` and `in` are byte-identical to each other; so are `cn` and `kr`.

> **That is the same two-way regional split found independently in `action_data.bin`**, where the
> `ch`/`in` variant differs from the `cn`/`kr` variant by 15 bytes of 32,612. **Two unrelated files,
> the same partition of the same four locales** — which is evidence that the split is a real
> regional build distinction and not a per-file accident.

**What node 360 is, is not established.** It is out of the table's range, present once on every job
board and never on `license_board`, and it is the only thing regional builds disagree about.
**Naming it would be a guess and this sheet does not make one.** **PROPOSED-repos-c7-13.**

**The table that has a row for it, and the table this build loads (2026-09-11, OPUS-NOTICE-NODE360).**
The four `license_data.bin` copies are not alike: `in` and `ch` are byte-identical with **360**
records (8,672 B), while `kr` and `cn` are byte-identical with **361** records (8,696 B) — the
`kr` / `cn` copy also blanks the name word `+0` of 69 rows. Its row 360 is `LP 30, category 0x1E,
one id 0x0080, no name id`: the record the boards' extra square was authored to index. **No path in
the executable names the `kr` or `cn` copy.** `ResourcePath_Init` (`002DF9A0`) installs one kind-2
path array per language, with `license_data.bin` at index 12 and the boards at 70–82; the arrays for
US, FR, DE, IT, ES, UK, ASIA and IN (and JP, through the default arm) name `test_battle\in\BinaryFile\`,
and those for KR, CH and CN name `test_battle\ch\BinaryFile\` — the `kr` and `cn` directories
occur in the string pool only for their thirty text files (`battle_message.bin`, `listhelp_*.bin` …).
So every language of this build loads a 360-record table under 361-node boards, and the grant path
refuses the square (the licence-check page §11): the id space is the size of the largest table
shipped, and the tables actually loaded are one record short of it. On the `in` job boards the
square sits, for `board_1`, at row 9, column 14; on the `kr` boards at row 4, column 18.

## 5b. Independent audit pass — 2026-09-06, `repos-1e`

**Method.** Every archive entry tested for the `licd` magic across all extensions, all copies
decompressed and re-parsed with a fresh reader; the cited instructions re-decoded with capstone.
Program state: GN160 (`gzf fa0db293…`).

**Every claim reproduces.**

| claim | sheet | re-parse |
|---|---|---|
| files / units | 52 = 13 × 4 locales | **52 files, 13 basenames, locales `ch` `cn` `in` `kr`** |
| magic `licd` | 13 / 13 | **13 / 13** |
| file size | 1,160, no exceptions | **1,160 in 13 / 13** |
| grid | 24 × 24 in 13 / 13 | **24 × 24 in 13 / 13**, and `8 + 576*2 = 1160` closes to the byte |
| filled squares, the twelve job boards | 128 … 143 | **128 … 143** — `board_3`/`board_9` 128, `board_4` 143 |
| `license_board.bin` | 300 filled, `0 … 299` dense | **300 filled, 300 distinct, max 299** |
| no node repeats within a board | — | **distinct == filled in 13 / 13** |
| node numbers across all 13 boards | exactly `0 … 360`, all 361, no gaps | **361 distinct, contiguous `0 … 360`** |
| node 360 present on every job board, never on `license_board` | 12 / 12 | **12 / 12, and absent from `license_board`** |
| `ch` = `in`, `cn` = `kr`, node 360 **relocated** not added | — | **confirmed**: `board_1` holds it at cell **230** in `ch`/`in` and **114** in `cn`/`kr`; `board_10` at **249** / **207**. Filled count unchanged either way. |
| `0x002E0052` | `mov qword ptr [rax + 0x238], rcx`, `0x238 = 71*8` | **exact**, and `0x238 / 8 = 71` |
| `0x0022A159` | `call 0x2df9a0`, the only call | **exact**, and `0x002DF9A0` has exactly one caller, `0x0022A0B0` |
| `0x00A79EB5` | the `board_1.bin` path string | **`board_1.bin`** |

### One addition: the twelve job boards do **not** cover the node space by themselves

The sheet establishes contiguity *"across all 13 boards"*. Measured separately:

| set | distinct nodes | range | contiguous |
|---|---:|---|---|
| the 12 job boards | **347** | 0 … 360 | **no** |
| `license_board.bin` | 300 | 0 … 299 | yes |
| all 13 | 361 | 0 … 360 | yes |

**So 14 node ids exist only on `license_board.bin`** — 4, 5, 6, 7, 8, 9, 10, 11 among them — and 61
exist only on job boards. The full `0 … 360` run is a property of the *union*, and neither family
spans it alone. **That bears directly on `PROPOSED-repos-c7-13` and on the 361-against-360 hole:**
the "extra" id is not simply node 360 sitting above a 360-record table — the two board families
index overlapping but distinct subsets, so any binding to `license_data.bin` has to explain both.

### What was attacked and held

(a) **The "128 to 143" band looked wrong at first** — my initial sweep gave 128 … 300 — because I
counted all 13 units. The sheet's sentence says *twelve* job boards, and scoped that way it is exact;
`license_board.bin` at 300 is the thirteenth and a structurally different artefact. **The fourth
scoping miss of my audits this week, and the same shape as PKFL's 2,268.**
(b) That the regional difference might be an added or removed node — it is not; the filled count is
identical across locales and only the cell index moves, exactly as §5 says.
(c) That `0xFFFF` might be a real node — it cannot be, and the no-repeat invariant only holds with it
excluded, which is the sheet's own argument and reproduces.

**Not audited:** `license_data.bin`'s 360 records themselves, and what a node id *means* — §6 and
`PROPOSED-repos-c7-13` already hold both open.

## 6. Falsification pass — 2026-09-05

| attack | result |
|---|---|
| Is the grid really 24x24, or does the header mean something else? | **The arithmetic closes to the byte**: `8 + 24*24*2 = 1160` and every file is exactly 1,160 bytes, in 13 of 13. A wrong dimension would leave a remainder; there is none. |
| Is the cell 2 bytes, or 4 with the high half always zero? | 4-byte cells need 2,304 bytes plus a header and the files are 1,160. The size forbids it outright. |
| Is `0xFFFF` empty, or a real node? | It is 433-448 of 576 cells in every job board. A node table of 360 records cannot contain a node numbered 65,535, and the "no repeats" invariant holds only when `0xFFFF` is excluded. |
| Does the `license_data.bin` binding rest on a count match? | **It does not even have one — 361 ids against 360 records.** Recorded as a binding with a hole rather than a join, precisely because the `st2e` sheet's AY-6 downgrade shows a count match is not deciding. **This is the weaker case, and it says so.** |
| Was node 360 singled out to fit a story? | **No — it was found twice independently before being tested.** Once as "the id space is one wider than its table", once as "one cell moves between locales". The test that they are the same value came third, and a different mover in any of the twelve boards would have killed it. |
| Is the magic unchecked, or did the search miss it? | 0 occurrences as ASCII and as the dword. **The named blind spot stands**: a constant can be built by arithmetic or compared in halves, so this sheet claims *not directly compared*, not *no check exists*. |
| Could the decompiler have invented the path index? | Every address in §3 and §4 was taken from **disassembly**, not pseudocode — this module decompiles with elided bodies, recorded in the `section-010`/`011` sheets. |
| Did an external tool supply any of this? | **No.** The layout is the corpus; the location contract is the binary. |
| Was the 13-unit population assumed or measured? | Measured from the frozen `.bin` signature census (`bin-signature-census.tsv`), which classified all 1,439 `.bin` entries — `licd` is 52 files / 13 logical units there, and this sheet examined all 52. |

**The killer observation.** The central claim is *"the cell is a `u16` node number and `0xFFFF` is
empty."* It dies if any board's live-cell count differs from its distinct-value count, if any file
is not 1,160 bytes, or if any node number exceeds the node table by more than the single documented
exception. All three were tested across all 13 units; only the documented exception exists.

## 6b. The chip art table — `bin_menu/license_chip.bin` (2026-09-29, SWE2-DATA)

*`OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS`; check [`b4_license_chip.py`](../_index/candidates/bucket-members-0929/checks/b4_license_chip.py), 41 checks, FAILS 0.*
The cells the grid above places are drawn from a second `.bin`, shipped only in `ch` and `in`
(byte-identical, 23,104 bytes). It is **361 chip ids × 2 variants × 32-byte records**, headerless;
record `2·id + v` is four 8-byte layers:

```struct LicenseChipLayer base=file size=0x8
+0x00  u16      sprite         0xFFFF = empty layer (all its other bytes 0); the range picks the atlas
+0x02  u16      value          read on layer 0 only; 0 in layers 1-3 of every record
+0x04  u8       b4             read by the draw loop (0055BD33)
+0x05  u8       b5             read by the draw loop (0055BD18)
+0x06  i8       dx             offset, -11..22
+0x07  i8       dy             offset, -11..7
```

**Request.** `00561390` asks kind 7 id `0x7E` (`lea r8d, [rdx+0x77]` with `edx` = 7 at `0056165F`,
request call at `00561663`), keeps the data at `obj+0x118` (`00561680`) and publishes it to
**`02CA9670`** (`0056168B`); a raw sweep of that slot finds 1 store and 5 reads in 3 functions.

**Readers.** The chip id is cell `+0x0E` and the state is bits 4–7 of cell `+0x18`, in the grid of
`0x38`-byte cells at `[ctx+0x120]`.
- `0055BAC0` draws record `2·id + (state ≥ 5)` (`setae` at `0055BC66`, base added at `0055BC86`):
  four layers (`r15d = 4`, stride 8 at `0055BE60`), each choosing one of three atlases by sprite
  range (`cmp 0x8000` at `0055BCDC`, `cmp 0x4000` at `0055BDEA`; the corpus spreads 1,168 layers
  below `0x300`, 18 in `0x300`–`0x3FFF`, 76 in `0x4000`–`0x7FFF`, 359 at `0x8000`+) and reading bytes
  `+4`, `+5`, `+6`, `+7` at `0055BD33`, `0055BD18`, `0055BD95`, `0055BDA2`.
- `00556590` reads layer-0 word `+2` of record `2·id + 1` (`005565BC`) and `0055F010` that of record
  `2·id` (`0055F0CD`).

**Not claimed.** For chip id `0xFFFF` the code falls back to record `0x2D2` / `0x2D3`, i.e. byte
`0x5A40` / `0x5A60` — exactly the end of the file, so that read lands past the data; what it returns
is not pinned (inferred). What `+4` / `+5` and the layer-0 value mean is not named here.

## 7. What this document does not claim

- **Which job each `board_N` is.** There are twelve boards and twelve jobs, and that is a count
  match — the exact evidence this sheet declines to promote elsewhere. **No board is named.**
- **What node 360 is**, beyond the four measured properties in §5.
- **What `license_board.bin` is for.** Its shape is suggestive; shape is not a reading.
- ~~**What parses the grid.** §3 states the failed search and its structural limit.~~ **Answered 2026-09-13:** the header by `0055B3F0` and six others, the cells by `00328990`, `0055E2C0`, `0055E600`, `00560070`, `0055F830`, `003FC900` (§3).
- **What a node record contains.** That is `license_data.bin`'s 24-byte record, not this file, and
  [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md)
  documents the runtime side.
- ~~**Whether the grid's row/column order is row-major as written.** `24 x 24` is square, so the
  corpus alone cannot distinguish row-major from column-major.~~ **Answered 2026-09-13 by the code, not the corpus:** every cell reader computes `row × [+4] + col` with the outer loop bounded by `[+6]` (`00328A0C`, `00328A9B`), so the grid is row-major with `+0x04` the width. **A square grid hides its own
  transpose**, and settling it needs the reader.
- **Why the `ch`/`in` and `cn`/`kr` builds place one square differently.**

## 8. Related

- [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md)
  — the runtime side: what the engine tests when a character already owns a node. **This sheet is
  the board's shape; that one is what owning a square does.**
- [`item-id-encoding-and-equipment-compatibility.md`](item-id-encoding-and-equipment-compatibility.md)
  — `0xFFFF` as the empty marker recurs there, in item ids.
- `../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/README.md` —
  `license_data.bin` is an `st2e` table and its header arithmetic is the same family.
- `Tools/work/formats/bin-signature-census.tsv` — the frozen census this unit's population came
  from. **`bin` is 28 distinct signatures over 236 logical units and cannot be scored as one
  format row**, which is why this sheet declares `container_format: licd` rather than claiming the
  `bin` extension.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited. MECHANICAL-only crossings are recorded in the registry, not here.*

- **Script_VM_Native_Bridge — CLIENT.**
  - A 23-byte script verb pops an int with `VMValueStack_PopInt32CoerceFloat32` and calls `00328BD0`.
  - A 61-byte verb body (`00511F50`) pops two ints the same way and calls `00560070`.

  **Both grid readers are reachable from script.**
- **CombatAI — SERVICE.** `00328BD0` (424 B), which calls the grid reader `00328990` twice, also clears all
  equipment slots (`BattleStats_ClearAllEquipmentSlotsByStatsIndex`). It rebuilds gambit state through
  `GambitConfig_LoadAuthoredPresetAndRe…`, `GambitRuntime_RebuildOrderSetForStat…` and
  `GambitConfig_InitializeThreeBanksFro…`. What `00328BD0` is for as a whole is not read.
- **Party — CLIENT.** `00328BD0` itself is filed under Party.
- **Gameplay — MECHANICAL.** The 8,136-byte body `0031C5D0` asks the encoded-id queries `BattleEncodedId_IsValidForClass`,
  `…DispatchQueryMode1`, `…DispatchQueryMode0Va…` and `…QueryMode0Positive`. It is itself called by `00328990`.
- **Input — SERVICE, not read.** `00560070` calls a 20-byte Input-filed getter.
- **Resource - SERVICE (5 edges).** `0022A0B0` reaches bodies filed to resource: `00259DF0`, `002DF9A0`, `0032EAE0` - shared machinery across the layer boundary, no shared ownership.
- **UI - CLIENT (12 edges).** `002527B0` is also called by bodies filed to UI: `00280DE0`, `003FDAD0`, `005651E0` (Widget) - shared machinery across the layer boundary, no shared ownership.
- **World - SERVICE (1 edge).** `0022A0B0` reaches bodies filed to World: `00266D10` (NativeSupport) - shared machinery across the layer boundary, no shared ownership.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — SERVICE.** A cited function calls `BattleStats_RecomputeDerivedStateAndAutoStatuses`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — SERVICE.** `0022A0B0` on this page calls `BattleStorage_InitializeWorkArrays`, owned by that layer. What it reaches is an initialiser: it writes +inf to `[02F973B8]`, zeroes `[02089300]`, sets `[0208E6A0]` to `0x20` and calls `003844F0`; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**CoreRuntimeScheduling — SERVICE.** `0022A0B0` on this page calls `FUN_0022bdf0`, owned by that layer. What it reaches is a 146-byte loop bounded by its first argument, whose body it runs only when the mode query answers 1; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Presentation — SERVICE.** `0022A0B0` on this page calls `AddMotion_LoadHighModelReplace`, owned by that layer. What it reaches is the loader for **`./PS2Data/add_motion/HighModelReplace.bin`** - the path is a literal in its own body - which it opens, sizes and reads whole; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**RNG_Random_Selection — SERVICE.** `0022A0B0` on this page calls `RNG_MT19937_Seed`, owned by that layer. What it reaches is a five-byte thunk - `jmp 00863D30` - onto the CRT's Mersenne Twister seed; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

## SWE2-EC7-41 update (2026-09-19) - `0055C530`

`0055C530` (351 B) is the node-state apply pair the page names - `0055E2C0`/`0055E600`/`00808C40`, `008F311C`/`01CEBBA8`/`01CEBC08`/`01F2CACC`. Interior anchor `0055C5B4` (a `0055E2C0` call).

`00559760` (90 B) is the keyed stat writes `00328BD0` runs on the `00282E10()`-resolved record: `002527B0(8, 0, word[+0x60] + 0x4D)` first, then a three-iteration loop `002527B0(8, 0, word[+0x60]·2 + i + word[+0x60] + 0x53)` — four board-keyed fields written off the same base word.

Interior anchor `005597A3` (function `00559760`).
