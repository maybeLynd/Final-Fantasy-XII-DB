# RC residue, round 2: RC-25's value domain, RC-30's computed-id bounds, RC-28's three leftovers, the unrequested `.mrp` (SWE2-DATA, 2026-09-30)

**Question.** The first record ([`../rc22-34-resource-readers-0930/`](../rc22-34-resource-readers-0930/README.md),
`1261e2044`) left one open fact each for RC-25, RC-28 and RC-30, plus a side result for RC-29. The coordinator asked
for all of them from static and shipped-data evidence. Every script prints its checks with a positive control and
ends `FAILS 0` at `937feca35`. Nothing is routed to ASTRA.

| item | verdict |
|---|---|
| RC-25: which values the menu record's word `+0x60` takes | **ANSWERED** — the party row `0`–`0x27`, or `0xFFFF`, provided the mirror `02166480` carries pages written by the same initialiser (N3: `002EF4A0` overwrites all 40 pages from it); the six main rows `0`–`5` select all six silhouette blocks |
| RC-30 A: `002CEAE0` | **bounded** — ids `0x17`–`0x29` |
| RC-30 B: `003C9950` | **bounded** — ids at most `0x1A` |
| RC-30 C: `00575C30` | **bounded** — ids at least `0x228` |
| RC-30 D: computed-kind path-API calls | ~~**NARROWED** — 54 sites listed; the data-driven `(kind, id)` sources are the remaining fact~~ **superseded: `../rc30-census-0930/` answers RC-30** (corrected 2026-09-30) |
| RC-28 (1): language index → path arm | **ANSWERED** |
| RC-28 (2): the absent KR / CN `.btm` | **ANSWERED** for the load — no file is opened and no fallback path is tried; the completion side is a static leftover |
| RC-28 (3): accented staff-roll glyphs | **ANSWERED** — the shipped staff roll never draws them |
| RC-29 side: `title_menu.mrp`, `E3_Logo.mrp` | **bounded absence** — no request site forms either id |

## 1. RC-25: the silhouette index is the member's party row (`rc25_domain.py`)

The chain:
1. The pane reset `0056A010` passes `movsx word [record + 0x60]` to the silhouette setter `002CEE00` (P1).
2. `00329220` writes that word exactly twice: `0xFFFF` at `0032925D`, and the stats page's **byte** `+4`, zero-extended,
   at `00329471` (`0032946C movzx eax, byte [r14 + 4]`) (P2).
3. The page is `*(02EBF190) + 8 + slot·0x1C8`. Its `+4` is written by `BattleStats_InitializeDefinitionRecord`
   `0023AC80` at `0023AD8E` (`word [rdi + 4] = r15w`, `r15d = edx`) (P3).
4. Its three raw callers:
   - two party loops, `00237DF0` and `00239960`, pass `edx` = the page index for pages `0`–`0x27` (P4);
   - the third, `0023A7A9`, initialises a SpawnKeep entry's embedded record, not a party page (P5).
5. Over the 176 functions that reference `02EBF190` (318 raw sites), a register tracker finds no other byte or word
   write at `+4` / `+5` of a page derived from it (W1).
   - Control C1: seeded on `0023AC80`'s page argument, the tracker finds `0023AD8E`.
   - Control C2: through the same derivation it sees 30 byte/word writes at other displacements.
   - *Narrowed 2026-09-30 (SWE2-AUDIT-SEM, `../auditsem-review-rc-residue-0930/REVIEW.md` §6 N3):* "`0023AD8E` is the
     only byte/word writer of a page's `+4` among code that reaches the block through `02EBF190`. The block is
     static (`021B290C` = `02164280 + 0x4E68C`) and `002EF4A0` (called only from `00235AF0`) overwrites all 40
     pages from the mirror `02166480`; a page's `+4` therefore also takes the mirror's value (mirror writers: the
     live-block snapshot `00229B76`, the save-load copy `00866A4D`, and `00583C00` from an untraced external
     buffer)."
6. The shipped zone scripts (the BQ-10 decompile, 1,114 files) add main-character selectors **exactly `0`–`5`**
   (`addpartymember`, 45 calls) and guest selectors `7`–`14` (`addguestbattlemember`, 27 calls) (S1).

**So a member's `+0x60` is its party row (page index) `0`–`0x27`, or `0xFFFF` — provided the mirror carries pages
written by the same initialiser** (N3).
- Rows `0`–`5` select blocks `T[0..5] = {0,1,3,2,4,5}`, which together cover all 3,096 pages.
- Row 6, the guests `7`–`25` and the higher rows turn the silhouette off.

## 2. RC-30: the three index-computed sites' bounds, and the fourth site (`rc30_bounds.py`) (SWE2-DATA)

*Narrowed 2026-09-30 (SWE2-AUDIT-SEM, `../auditsem-review-rc-residue-0930/REVIEW.md` §6 N1):* "Sites `002CEAE0`,
`003C9950` and `00575C30` cannot form `0xE2`–`0xE4`. A fourth computed site, `003C208D` in the location-map loader
`003C1F00`, requests kind 7 id `0xE1 + byte [entry + 1]` for a non-zero byte, so it forms `0xE2`–`0xE4` for bytes
1–3; the RC-30 route question turns on the shipped entries' `+1` bytes and on that site's consumer, not on the
computed-kind structures alone." (This heading's earlier form — "the index-computed sites cannot produce
`0xE2`–`0xE4`" — was false: the record's list was not the census of computed-id sites. `../rc30-census-0930/`
settles the shipped-`+1`-byte and consumer questions it left open.)

**A — `002CEAE0`, id `0x10 + byte [[0209AC30] + 0xB2D]`, gated by `+0xD3C` bit 1.**
- Image-wide there are exactly two byte writes at `+0xB2D`: `002832C7` (`0xFF`) and `00283400` (A1).
- *Narrowed (§6 N2):* nine wider stores image-wide also cover `+0xB2D`; two write other objects (`002969E0`'s
  receiver `[[0209BE80] + 0x10F78]`, the console filler `001D0390`), five are not type-traced — the same limit B
  states for its 18 other `+0xC1` writers.
- `00283400` stores the member copy's `+0x60` byte on the branch where the copy's flag bit 1 is set, and sets the gate
  bit there too (A2).
- `00329220` sets that flag bit only for a party row `7`–`0x19` (A3).
- So the id is `0x17`–`0x29` (`face_guest07`…). Control CA: the census shows `002CEAE0`'s own read.

**B — `003C9950`, id `0xE + byte [obj + 0xC1]`.**
- The widget procedure `003C9A30` writes the byte only with `dl` = the first `i < 7` whose bit is set in a mask
  (table `00D11710` = 1, 2, 4, …, 64). It skips the write when `dl = 7` (B1).
- The child procedure `003C95C0` writes values from `00D11720[0..7]`, and the word `0x0A02`; all are ≤ 12 (B2).
- These four are the widget module's only writers (B3).
- So the id is at most `0x1A` (the `map_efe` family).
- The other 18 image-wide `+0xC1` byte writes sit in modules that are not handed this widget object. They were not
  type-traced.

**C — `00575C30`, id `u16 base[cat] + u16 [pane + 0xCA] (+ u16 [req + 2])`.**
- The bases `00D23740[0..5]` are `0x228`, `0x294`, `0x2CC`, `0x2F4`, `0x31C`, `0x354`: `menuhandbook_story` …
  `_monster` (control CC).
- The category comes from three places:
  - `00577880`, whose only caller `0056F2A0` reaches it only on its `dl ≤ 5` branch (C1);
  - the pane's `+0xD2`, written only at `00575CD2` with the category (C2, C3);
  - the pane's history of earlier categories.
- So the category is ≤ 5 and the id is ≥ `0x228`.

**D — the computed-kind path-API calls (NARROWED).** The rel32 call/jmp/jcc sweep of `0032E400` / `0032E620` /
`0032E3F0` finds 124 sites; 54 of them set the kind from a register or memory. All 54 are listed in the output. By
kind source they fall into three groups:
- **caller arguments:** the pool core `00249210`, `0024AB90`, `00332250`, `00379A10`, the actor-resource loaders
  (`0032FCA0`, `00330310`, `003306E0`);
- **loop or offset arithmetic:** `00268750` (`rdi + 9`), `00378540`, `0036ED50`;
- **`(kind, id)` pairs read from loaded structures:** `003A13F0` (`+0x20` / `+0x18`), `003DDA70` (`+0x10` / `+0x12`),
  `003DF550` (`+0x2C` / `+0x2E`), `003E9EF0` (`[rdi + rbx·2 + 0xC]` / `+0x10`), `003EADE0` (`+0x1C` / `+0x20`), and
  `003DC5B0` / `003DC8D0` (stack copies).

**The fact still open, and it is static:** whether any shipped instance of those structures holds kind 7 with id
`0xE2`–`0xE4`. It is a data census of each structure's source file, not a runtime question. ~~Until it is run, no
reader of a `loca_*.cl2` is reachable through any route this record or the first one traced.~~

*Corrected 2026-09-30 (SWE2-DATA, [the RC-30 census](../rc30-census-0930/README.md)): the location-map pane loader `003C1F00` requests kind 7 id `0xE1 + byte [menumap_common entry + 1]` at `003C207A`-`003C208D`, a register-held site this record's list missed (its `0x142 + byte` row is the other request in the same function), and `003C26C0` reads the file as an external CLUT. The census supersedes this paragraph.* *Sites A, B and C above stay bounded as stated; the census also finds every data-driven `(kind, id)` source carries a constant non-7 kind.*

## 3. RC-28's three leftovers

**(1) Language index → arm (`rc28_lang_arms.py`).**
- `002DF9A0(lang)` switches on `lang − 1` through the table at image base `+ 0x1C04B0`. Out of range goes to the
  default arm `002DFF32`.
- The name table `01E88B00` spells `JP US FR DE IT ES UK KR CH ASIA IN CN` (C2).
- Following every arm to its `ret`, keeping the last store to each directory slot, gives:

| lang | name | kind-7 array | `fontpack_fs.bin` | `.btm` |
|---|---|---|---|---|
| 0 | JP | `01EDD7E0` | `in` | `in` |
| 1–6 | US FR DE IT ES UK | per language | **`us`** | **`in`** |
| 7 | KR | `01E0E530` | `kr` | `kr` |
| 8 | CH | `01E5A3D0` | `ch` | `ch` |
| 9, 10 | ASIA, IN | `01EDD7E0` | `in` | `in` |
| 11 | CN | `01EABBA0` | `cn` | `cn` |

**(2) The absent KR / CN `.btm` (`rc28_staffroll.py`).**
- `FileSizeTable_KR.fst` and `_CN.fst` hold `0xFFFFFFFF` (no file) for all six `.btm` ids. `FileSizeTable_US.fst`
  holds 42,240 / 29,184 / 32,256 (control C3).
- The read issuer `002DF780` refuses a `(kind, id)` whose entry is −1 before it resolves any path (`002DF7B0`,
  `002DF7B9` → `002DF85D`, returns 0), so **no file is opened and no fallback path is tried**.
- The size query `0032E400` returns the −1 unrounded (`0032E43D jle`), and `00365810` allocates with it.

**Static leftover:** what the request queue (`0032E620` → `0032E870`) does with a request whose read was refused.
That is whether the `.btm` completion callback `00364380` ever sets its ready bit, which decides whether the KR / CN
staff roll waits or draws without a sheet.

**(3) Accented glyphs in the staff roll (`rc28_staffroll.py`, `rc28_staffroll_faces.py`).**
- **The text.**
  - Staff-roll names are text group 26 → kind-2 id `0x42` `menu04.bin`; roles are group 25 → `0x41` `menu03.bin`
    (byte table `01E09F68`, S0).
  - Each file holds 1,024 / 512 `ex00` UTF-16 rows. The row offsets ascend, so scan order is row order (S0b).
  - The 49 glyphs only the `us` tables 8–11 carry occur only in the **`fr` / `de` / `it` / `es`** `menu04.bin`: rows
    894–944, the localization staff. They use nine letters, Á á è é í ñ ó ö ú, 72 occurrences in all.
  - The `us` files and the UK arm's `in` files have none.
- **The face.**
  - `0053DD20` sets a name line's font slot to `(class + 3)·2`: 6 / 8 / 10 for `fsroll_nameA` / `B` / `C`. The draw
    uses that slot and the next one, the shadow face.
  - The text id is `0x6590 + id` (names) or `0x61A8 + (id & 0x7FFF)` (roles, bit 15) (C2).
- **The script.**
  - The staff-roll actor in `men_z0005` has 688 `fsroll_nameX` call sites; the evaluator visits every one grep finds
    (C1) and resolves every argument (E0).
  - They request 638 distinct name ids: class A 28, B 39, C 571.
  - `men_z0005.ebp` is byte-identical in `us` / `fr` / `de` / `it` / `es` / `in` (S1).
- **Result:** no `fsroll_nameA/B/C` call requests any of rows 894–944 (S2). **The shipped staff roll never draws one
  of the 49 accented glyphs, so the "past the end of the loaded sheet" case in the first record is never reached by
  shipped data.**

## 4. RC-29 side result: `title_menu.mrp` and `E3_Logo.mrp` (`rc29_mrp_requesters.py`)

The scan covers all 186 raw call/jmp/jcc sites of the eight request entry points (the five pool entries and the three
path entries). Each is read with its 14 preceding instructions, looking for:
- a constant equal to the id in the id register;
- the compiler's `mov edx, 7` / `lea r8d, [rdx + k]` idiom.

Controls: C1 finds `title.mrp` at `00394044` and `Loca.mrp` at `004040FE`; C2 finds `title_logo.tm2` through the idiom
at `00394025`.

Neither `0x3B` (`title_menu.mrp`) nor `0x89` (`E3_Logo.mrp`) is formed at any site (R1). Neither id is in the three
`.rdata` request lists (the first record's `request_lists.py`). `nowload.mrp` and `title_fore3.mrp` ship but have no
kind-7 path at all (R2), so no id request can name them.

This is a **bounded absence**. An id computed at a register-held site outside the window is outside it, the same
scope the first record states for the `.cl2` ids.

## Crossings into other layers

These are reads of neighbours' code and data, named by role:
- **Party**: the party stats block and its initialiser.
- **Script VM**: the staff-roll verbs and their handlers.
- **UI**: the handbook, location-map and member panes.
- **Resource**: the request API, the file-size tables and the kind path arrays.

No neighbour body's semantics is claimed beyond the instructions pinned in the scripts.

## Relation to ORACLE's parallel records

SWE2-ORACLE wrote uncommitted records on the same rows while this work ran (`rc25-party-definition-rows-0930`, …).
Its RC-25 result (row = record index, rows 0–5 select the six blocks) and its RC-30 site-A bound agree with §1 and §2.
They are not linked here until they are at HEAD.
