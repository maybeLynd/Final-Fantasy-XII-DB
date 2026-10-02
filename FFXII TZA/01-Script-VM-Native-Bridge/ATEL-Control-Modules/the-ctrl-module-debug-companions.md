---
system: .sbn, .msb, .dbg — the ATEL control modules' debug companions, shipped and not loaded
category: 01-Script-VM-Native-Bridge
status: AUDITED
owner_layer: PrimaryOwner:Script_VM_Native_Bridge
evidence_tier: 1
verified_against:
  gzf_sha256: fb9b5e7ea002c1626a53d47da0b0b69a2443e246f7ce2b64329be4e034a2d3f7
  snapshot_sha256: a9cead8777597cdca58f2a47f27153f5231d60ad2bc16c3da9df8253820b09bd
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity - every function this document cites has byte-identical per-function records in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: 2 cited function entries, 0 of them among the 128 records that changed across GN158..GN161 (check_delta_additivity.py, check_transfer_eligible.py); re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS-REQ-FABLE-PROVENANCE-TRANSFER-144 (9bedb5e0); re-targeted GN160 -> GN161 under EVIDENCE-STANDARD addendum 2026-09-14bh
    previously: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708 (GN160), superseded 2026-09-14
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "8 / 8 each of .sbn, .msb and .dbg in the archive index, all opened, 2026-09-12"
last_reviewed: 2026-09-12
archive_formats:
  - "sbn"
  - "msb"
  - "dbg"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-atel-companions-pass-1 - corpus and both negative routes reproduce exactly with controls (used extensions occur 129-10,380 times against 0 for these); the extension substitution is 25 unrolled lea sites, not a table walk over the cited range
  crossref_clean: true
  reopened_count: 0
---

# `.sbn`, `.msb`, `.dbg` — the ATEL control modules' debug companions

> Twelve distinct files, each shipped twice (`ps2data/image/ff12/ch/bin/` and `…/in/bin/`, byte-identical):
> the source-text, message and symbol companions of four PS2 ATEL scripts — `ctrl`, `btlctrl`, `evctrl`,
> `mapctrl`. In this build the
> extension-based loader that knows these extensions asks for their sizes through a lookup that returns
> −1 before searching, and nothing names the files — **they are inert**.

**Corpus validation.**

| | |
|---|---|
| files examined | **8 `.sbn`, 8 `.msb`, 8 `.dbg`**, all opened |
| modules | `ctrl`, `btlctrl`, `evctrl`, `mapctrl`, in `ch/bin` and `in/bin` |
| `ch` copy = `in` copy | **12 / 12** (md5) |
| `.sbn` block table valid (first offset = `4·(count+1)`, ascending, in bounds) | **8 / 8** |
| module stems, `systemctrl`, `\ctrl.`, `.sbn\0`, `.msb\0`, `.dbg\0` in the executable | **0 occurrences each** |

Census: [`census.py`](../../_experiments/evidence/atel-ctrl-modules/census.py) →
[`census.out.txt`](../../_experiments/evidence/atel-ctrl-modules/census.out.txt).

---

## 1. What the player sees

**Nothing.** On the PS2, *ATEL* was the scripting system and `ctrl` / `btlctrl` / `evctrl` / `mapctrl` were
its system-control scripts (the files carry `systemctrl.ath` includes and debug globals such as
`g_com_debug_flag` and `mp_debugmenu_flg`). By their contents the three extensions are companions produced beside each script — source text,
messages and a symbol table — of the kind a debugger reads. The remaster
ships them in two language folders and never opens them.

## 2. The layout

**`.sbn` — source text blocks.**

```struct SbnHeader base=file
+0x00  u32       blockCount   2 (ctrl, evctrl) or 3 (btlctrl, mapctrl)
+0x04  u32       blockOffset0 the first of blockCount offsets; equals 4 x (blockCount + 1)
```

`blockCount` `u32` offsets follow the count, ascending and in bounds in 8 of 8 files.

Each block begins with two `u32` (for example `977, 2124` then `79, 23356` in `ctrl.sbn`) followed by a `u16`
offset table and printable ATEL source — `#include "p:/tool/atel/header/common.ath"`,
`#macro _SYSTEM_USE_HDD()`, `for( i0 = 0 ; i0 < 255 ; i0 += 1 )`. The second and third blocks of the
three-block files start with `79` and `557` / `558`.

```struct SbnBlock base=block
+0x00  u32   lineCount
+0x04  u32   textOff     file-absolute offset of this block's text (chunk 0)
+0x08  u16   pageTable[]  ceil(lineCount/32) page entries (see below)
```

`textOff` resolves the second header word (§7): it is the **file-absolute offset of the text** — `0x84C` for
`ctrl.src`, `0x1484` `evctrl.src`, `0x1510` `btlctrl.src`, `0x1730` `mapctrl.src`. The `u16` table is a
**paged line map, 32 lines per page**: every full page is `{u16 lineStart[32]; u32 nextPageBase}` where
`nextPageBase` is the **file-absolute offset of the next page's first line**, and the final page is a bare
`u16 lineStart[32]` with unused slots zeroed — so the table spans `(pages−1)·34 + 32` u16s exactly (1052 for
`ctrl.src`, 100 for `systemctrl.ath`, verified on all 9 blocks). Line *j* of page *p* starts at
`pageBase[p] + lineStart[j]`, with `pageBase[0] = textOff` and each later page's base read from the preceding
u32 trailer; a page's base is always its own first line, so `lineStart[0] = 0` within every group.
**Corrected 2026-09-28 (OPUS SN-1 evidence,
[`_index/candidates/sn1-layouts/`](../../_index/candidates/sn1-layouts/README.md) `sn1_layouts.py` S1–S4,
FAILS 0):** the trailer is a single **u32**, not `{u16 chunkEnd; u16 0}` — 88 of the 312 trailers carry a
non-zero high half once a block's text runs past 64 KB, which the split reading cannot express; and reading
`chunkEnd` as the chunk's last byte (next chunk at `+1`) puts 917 of 10,139 line starts after a NUL, where
the u32-base reading puts all 10,139 on one. The earlier "slot may begin inside the NUL run" special case was
an artifact of the shifted reading and is retracted — every line start lands exactly after a NUL.

**`.dbg` — sectioned debug database.** Header: five `(u32, u32)` slots, three used — each slot is
**(section offset, table offset)**, not (offset, size) (corrected 2026-09-28 on OPUS's
`sn1_front_tables.py` F1–F4, FAILS 0): slot 0 = (`S0` = the per-scope-directory section; `T0`), slot 1
= (**S1 = the string-heap start** — the pool base; `T1`), slot 2 = (`S2`; `T2`). The second words index
the **front region** `[+0x6C, dirA[1])`, which holds the three counted `T` tables listed below — so the
`0x7C`/`0x78` word is **T0's offset**, exactly `0x6C + 4 + 4·n` for `n` `.sbn` blocks (`0x78` in the
2-block `ctrl`/`evctrl`, `0x7C` in the 3-block `btlctrl`/`mapctrl` — the "correlates with block count,
meaning unpinned" observation was T0's position, and it is pinned after all), and `0x6C` is **T1's**
offset, not the heap start. The heap (slot 1's first word — `0x88A0` in `ctrl`)
opens with the module's `.sbn` **block source paths** — `btlctrl.src`,
`c:/plan_work/jp/event/header/systemctrl.ath`, `mapctrl_mj.src` (dev-machine paths, `ctrl` uses a cygwin
variant) — i.e. the filenames q0's `blockIndex` selects; **S2 = a 64-slot directory**
(`{u32 count=0x40; u32 offs[64]}`) of count-headed `{u32 count; u32 tag; u32 positions[count]}` tables —
only slot 1 non-empty in all four modules, and it is the module's **`.msb` message-constant name
table** (resolved 2026-09-22): `count` is exactly the `.msb` message count (`48`/`42`/`47`/`57`), `tag`
is `1`, and `positions[i]` is the heap name start of message *i*'s source-level constant —
`select_base`, `select_base2`, `select_event_*`, `mmes_*`, `mes_*`, `MES_*` — in `.msb` index order
(the constants the `aask`-family calls pass as `0x010000NN` pool values; the earlier
"`global_debug_flag[734+]` module-global symbol list" reading was a wrong-heap-base artifact and is
retracted); then `dirA`, a 17-entry `u32` directory. `dirA[0]`
is 0; `dirA[1..16]` point at the count fields of packed `{u32 count; u32 entries[count]}` tables that tile
contiguously in directory order (`dirA[t+1] = dirA[t] + 4 + 4·count`), verified on all four files. The
front region `+0x6C` .. `dirA[1]` (the first section) is **three counted tables, not one pair stream**
(corrected 2026-09-28 on OPUS's `sn1_front_tables.py` F1–F4, FAILS 0, re-verified here on all four
modules; the `T`-names are OPUS's front-table names, distinct from dirA's `T1`/`T3`/`T4`/`T8`):

- **T1** at `+0x6C`: `{u32 n; u32 nameOff[n]}` — the **source files**, `n` = the `.sbn` block count
  (2 / 3 / 2 / 3; `ctrl.src`, the `systemctrl.ath` path, `mapctrl_mj.src`). Ends exactly at T0.
- **T0** at `+0x78` / `+0x7C`: `{u32 count; u32 nameOff[count]}` — the module's **source-declared
  variables** (56 / 92 / 115 / 127; every `ctrl` entry appears in its `.sbn` text, and a name recurs
  once per scope that declares it), followed by zero padding to 16 bytes.
  *Operand binding, qualified 2026-09-28 (FABLE, Claude Opus 5.5; [`t0_scope.py`](../../_index/candidates/sn1-q0-source-domain/t0_scope.py) S1–S4, C, FAILS 0).* The `.ebp`
  operand table (EBP2 `+0x28`) has T0's count in every module. A variable operand *n* reads operand-table record *n*, and that
  record's descriptor names a T2 record for 106 of the 390 entries. In every one of the 106, the T2 name is `T0[n]`, never
  `T0[n + 1]` (35 of them through a two-name T2 record). The covered ranges are ctrl `0`; btlctrl `0`–`4`; evctrl `0`–`0x43`;
  mapctrl `1`–`2` and `4`–`0x21`. That includes all 62 of evctrl `0x01`–`0x3E` (descriptors `0A03`–`0A40`), the globals a
  source-alignment reading had disputed: each has one T2 record, and its name is `T0[n]`, never `T0[n + 1]` (`t0_attribution.py` G).
  The other 284 entries (file, local and array classes) have no T2 record. Five source samples match `T0[operand]` (evctrl
  `0x61`, btlctrl `0x0D` and `0x0E`, mapctrl `0x52` and `0x20`), but `T0[operand]` is not established for the rest of the
  284, and no universal rule is claimed.

  *The disputed 62: a debug-line attribution, not a shifted name table (FABLE, Claude Opus 5.5, 2026-09-28, for the
  unavailable owner; [`sn1-layouts`](../../_index/candidates/sn1-layouts/README.md) Parts 8–10).*
  - **The observation, kept:** on the logical line q0 tags, the instructions of operands `0x01`–`0x3E` show `T0[n + 1]` 59
    times and `T0[n]` never (Part 8, check B).
  - **The earlier reading, superseded:** that the operand table is offset by one against T0 for this run, so these operands
    name `T0[n + 1]`. It was withdrawn in Part 9 and is not a current claim.
  - **Why the tag shows the next name:** the 62 are one run of one-line assignments (`g_btl_… = …`), and on them q0's tag runs
    one logical line late. `T0[operand]` is on the preceding logical line in all 63 of their statements, and on the tagged
    line in none (Part 9, check A). A tag one line late lands on the next variable's assignment. The binding itself needs no
    source line: it rests on the T2 names above (Part 10, check D). The same T2 test against a table shifted by one finds no
    match in any module ([`t0_scope.py`](../../_index/candidates/sn1-q0-source-domain/t0_scope.py) C).
  - **For a debugger:** a q0 tag gives an addressable logical line, not the statement that emitted the code. Attribute a
    statement allowing the preceding logical line; a `case` label's tag belongs to the line after it (Part 11, bucket E).

  OPUS's source-alignment census over every variable instruction (Parts 9 and 11) finds the `T0[operand]` name:
  - on the tagged line, 2,166 times;
  - on the preceding line, 304 times;
  - in an archived macro's expansion or at a case label, 188 times;
  - at calls of macros the archive does not carry, 84 more times.

  That agrees with `T0[operand]`, but alignment is not a binding proof: the same kind of reading first suggested `T0[n + 1]`
  for the 62, which the T2 route rejects.
  **Macro membership is not statement identity**
  ([`t0_attribution.py`](../../_index/candidates/sn1-q0-source-domain/t0_attribution.py) P, T, L, C, FAILS 0). The 188
  macro records match because `T0[operand]` occurs somewhere in the invoked macro's expansion. That does not say which
  statement of the expansion emitted the instruction:
  - the 188 fall on only 36 q0 tags, and 26 of those tags carry two or more different operands (158 records; one tag carries
    27 operands), so a tag names the invocation, not a statement;
  - in 97 of the 188 the name is on two to four expansion lines;
  - `T0[operand + 1]` passes the same membership test in 52 records.

  The 84 records at unarchived macros stop at header text that the archive does not carry; this page supplies no text for
  those macros.
- **T2** (header word `+0x14`): `{u32 count; {u32 id; u32 namePos}[count]}` — the **global-variable
  directory**, count explicit (815 / 4,950 / 943 / 4,953); zero-padded to 16 it ends exactly at the
  first section (`dirA[1]`).

All `nameOff`/`namePos` are byte positions into the string pool (base = header `+0x08` = S1) and land
on name starts. The earlier "**front pair stream**" reading — `u32` pairs `{id; nameHeapPos}` counted
846 / 5,000 / 1,004 / 5,020 — folded T1, T0, their padding and T2's count word into "pairs" (F4: the
reported counts equal T2's count plus the pre-T2 words / 2; the "out-of-order head entries" were T0
name offsets read as `id`s — no T2 `id` is a name start). That framing is **retracted**; inside T2 the
`namePos` element ascends the pool except for 4–6 inversions per file (`btlctrl`: 4,945/4,949 ascending
steps, inversions at entries 255, 369, 698, 811).

T2 is what the pair-stream reading described, and its `id`-to-name binding stands: the first `id`
`0x30000000` names `global_flag[0]`, and the directory covers `global_flag[0..510]`,
`battle_global_flag[]`, `quest_global_flag[]`, `event_global_flag[]`, `g_btl_*`/`g_com_*` module
globals, the block's own vars, then the `global_debug_flag[0..4095]` block. The `id` element is the
symbol's **variable descriptor** — the tag byte is the native descriptor's
`{width:4; float:1; class:3}` top byte **verbatim** (the §2.2 layout in
[script-variables-and-their-storage-classes](../Interpreter-Core/script-variables-and-their-storage-classes.md)),
so the width nibble is the resolver's six-case selector `0 u8 · 1 s8 · 2 u16 · 3 s16 · 4 s32 ·
5 f32`. All six cases occur in-corpus (`btlctrl` T2 tag bytes: `0x00` 4,479, `0x10` 11, `0x20` 32,
`0x30` 418, `0x40` 3, `0x58` 7) and every observed `id` has class `0` (global): `0x00` =
u8 (`global_debug_flag[N]`), `0x10` = s8 (`mp_*`), `0x20` = u16 (`g_menu_telepo_dest[N]`),
`0x30` = s16 (`global_flag[N]`, the `battle/quest/event_global_flag` arrays, `g_com_*`),
`0x40` = s32 (`g_com_set_get_label*`, `mp_map_flg`), `0x58` = f32 (width 5 **plus** the float
bit — `g_com_navi_footcalc[3]`, `mp_map_set_angle`). The low 24 bits are the variable's
**byte offset in global storage** (offsets stride by element size: `+1` for `0x00`/`0x10`,
`+2` for `0x20`/`0x30`, `+4` for `0x40`/`0x58`). Corroboration: **all five class-0 entries of `btlctrl`'s `.ebp`
descriptor table appear verbatim as T2 `id`s** (`0x30000000`, `0xA71`, `0xC7A`, `0x10000914`,
`0x10000915`). So T2 is the module's **global-variable directory** —
`descriptor → name start`, the `.dbg` side of the save-payload map. (The "~416 `id`s bound by two
names" alias claim was a fold artifact — within real T2 no two entries share a `namePos`, 0/4,950 in
`btlctrl`.) The `global_debug_flag` region is the same format with tag `0x00`:
T2 entries **854–4,949** (`btlctrl`) are `{ordinal N; pos}` for **exactly `N = 0..0xFFF` ↔
`global_debug_flag[N]` at its name start, 4,096/4,096 exact** — the `u8[4096]` debug-flag array's
descriptor range (offset `N`, width 0), and `btlctrl`'s T2 literally ends at `gdbg[4095]`. `ctrl`/`evctrl` have smaller
heaps without the full `global_debug_flag[0..4095]` block, so their T2 tables end after the tagged/head
region (815 / 943 entries, no `0..0xFFF` pass). *Misparse note:* earlier passes read
the stream past its true end (the first `dirA` table) and reported phantom classes `0x0002`/`0x0100`/
`0x0101`/`0x0102`/`0xFFFF` and a `0xFFFF` "scope sentinel" — those were `dirA`/`q`-table u32s (incl. q3's
`0xFFFFFFFF` headers) read as records; none exist in the real stream.
The **section directory is the 16 `u32` offsets at header `+0x2C..+0x68`** — they tile the section region
`[sec0_off .. 0xB7E0)` in order (`btlctrl`: `0x9CB0, 0xB268, 0xB26C, 0xB59C, 0xB7AC, …`); most slots point at
4-byte zero padding (empty sections). Each section is `{u32 count; u32 nameOff[count]}` with `nameOff`
relative to the string pool (base = header `+0x08`).

**Corrected 2026-09-28 (OPUS SN-1 evidence — `_index/candidates/sn1-layouts/sn1_layouts.py` D1–D4, FAILS 0,
re-verified here on all four modules): section *k*, entry *i* names native command `(k << 12) + i`.** The
non-empty sections are the module's native-command name tables in command-id order: **section 0** (the
`dirA[1]`/T1 table, 1,389–1,436 entries) = **class-0 script-verb names** (`wait`, `setpos`, `setvelr`, …);
**section 2** (dirA `T3`, 203–211) = **class-2 debug commands** (`debug_bindp`, `mapload`, `debug_tkmalloc`,
…); **section 3** (`T4`, exactly 131) = **class-3 `btlAtel*`**; **section 7** (`T8`, exactly 103; empty in
`btlctrl`) = **class-7 `fsmenu*`**. All 7,303 entries across the four files land on pool name starts (D1)
and **7,297 agree with the verb catalogue** (`gen_req_channel_census.load_verbs`); the six exceptions are
one pair — `0x20C8`/`0x20C9` are `debug_set_jfdemo_status`/`debug_get_jfdemo_status` in `ctrl`, `btlctrl`
and `mapctrl` but `e3demo` in `evctrl` and the catalogue — so the modules were built against different
verb tables (the class-0 counts diverge too: 1,410 / 1,389 / 1,436 / 1,407).

Two earlier readings are **retracted** on that evidence. The "67 ascending sub-lists = thematic verb
families → T1 is the ATEL verb-category directory" interpretation: every reset point is a name the pool
**already stores earlier in the section** (D4 — `setpos` at `0x19`, `setrect` at `0x25`, `show` at
`0x38`, …; the pool de-duplicates, so equal per-list lengths across modules follow from an identical
command-id order, not a shared category map). And the T3/T4/T8 name-range identifications
(`result`/`eventresult`/`wallescape`, `global_flag[]`, `battle_global_flag[]`) were offsets read without
the pool base (D3) — the real names are the command names above. The earlier "file offsets into the tail
slice" reading was a numeric coincidence (the heap positions sit in the same range as the pre-S0 record
stream). **Correction 2026-09-22, still standing:** under the correct heap
base (header `+0x08` = S1 = the heap origin — e.g. `0x1CA20` in `btlctrl`), **every** section entry and
**every** per-scope q1 entry lands exactly on a name start — 100 % corpus-wide (section 0: 1,389–1,436,
2: 203–211, 3: 131, 7: 103, q1 2,778 across all four modules, zero mid-name landings). The earlier
"land mid-string in 97 %+ of cases (`lag[209]`…)" and "referent = enclosing name span, depth
writer-internal" readings were measured under the wrong `0x5170` heap base and are **retracted** —
these tables are plain name-start position lists. The heap is suffix-compressed
(`global_flag[25]` ⊂ `event_global_flag[25]` at +6, `flag[25]` at +13). S0 is `{u32 scopeCount; u32
offs[4·scopeCount]; u32 0}` — 7 / 13 / 23 / 7 scopes for ctrl/evctrl/btlctrl/mapctrl — each scope a quartet
`{q0 posStream; q1 nameTable; q2 streamOffsets; q3 pageMap}`: **q0 is a byte-granular
bytecode→source map — RESOLVED.** Each scope corresponds 1:1 to a `.ebp` section-000 script-directory
entry (23 scopes = 23 scripts in `btlctrl`, 7/13/7 likewise), and the scope's q0 stream holds **one
4-byte record per bytecode byte** of that script, in code order: `{u16 lineNo; u8 blockIndex; u8 flag}`
= *"bytecode byte i of this script was compiled from line `lineNo` of `.sbn` block `blockIndex`; `flag=1`
marks the instruction's first byte"*. Verified exactly: decoding the script's bytecode with the opcode
length table (`0x03–0x47` → 1 byte, `0x48–0x63` → 3 bytes) reproduces the `flag=1` positions
**bit-for-bit in all scopes of all four modules** — `flag=1` count == the script-directory
`numOfInstructions` field (55/1404/226/993/… in `btlctrl`), and record count == `codeEnd` rounded
up to a multiple of 4 — the q0 table is a whole number of 16-byte rows, padded with ~~0–2~~ 0–3
trailing `(line 0, block 0, flag 0)` records (none before `codeEnd`, every record at or past it
zero). `codeEnd` is the last `flag=1` record's position plus the length of the opcode at that byte
of the script's `.ebp` code — equal to the directory's byte count in the 49 scopes where it fits;
for `evctrl` scope 1, whose tail runs 143 bytes past its directory span, it is q0's own extent. A
pad record describes no byte of its script: in the 45 packed scopes that position is the next
script's code. q0 and q1 start 16-aligned in all 50 scopes — the pad is what keeps q1 aligned. So the earlier "items of arity {1,3} headed by
`flag=1`" were simply **the instructions' own byte lengths** — a `reqsw(1,…)` line compiles to four
3-byte instructions = 12 records, a `}` to one 1-byte instruction. `blockIndex` selects the `.sbn`
block (`1` = shared `systemctrl.ath`, exactly 151 records in all four modules at `pos 0x21..0x4C`; `2` =
`mapctrl_mj.src`, only in the 3-block modules), and included blocks' byte maps embed **inline in the
including scope's stream** (`btlctrl` scope0 = the whole 151-byte compiled include + 1 end mark; scope1
embeds all 3450 block-2 records mid-stream — `#include` is expansion, not a separate scope). Edge case:
`evctrl` scope1's stream continues 144 bytes past its script's directory-bounded code — 48 extra
instruction-start marks attributed to one `case`-body line, consistent with a shared or duplicated
code tail (the runtime directory splits on `scriptStartOff`, the debug stream on the entity's compile).

*Qualified 2026-09-28 (FABLE, Claude Opus 5.5; DATA from the archive,
[`sn1-q0-source-domain`](../../_index/candidates/sn1-q0-source-domain/README.md): `q0_domain.py`, `entry_lines.py`, `logical_lines2.py`,
`assignment_attribution.py`, all FAILS 0; routed from ASTRA's SN-1 source-domain, entry-line, logical-source, CP932 and
attribution returns):*
- **`lineNo` is a 1-based logical line.** In the four samples that can tell (btlctrl scope 1 pcs 531 and 537, mapctrl scope 1
  pcs 729 and 736, each pushing the literal its line states), the 1-based reading names the statement and the 0-based one
  does not. No compiler rule beyond these samples is claimed.
- **Logical means backslash continuations are folded, tested on decoded CP932.** A physical line continues only when its last
  *character* is a single-byte `\`. A trail byte `5C` inside a double-byte character is not one: mapctrl's lines 977 and 1187
  end in `能` (`94 5C`) and do not continue. Genuine continuations: evctrl block 0 has 544, ctrl block 0 has 19, mapctrl and
  every other block have none. Without the fold, evctrl scope 1's lines 417, 418, 708 and 709 land on unrelated text; with it
  they land on the `askpos` / `mesopenspeed` calls.
- **Six records name a line one past their block.** btlctrl scope 1 records 3978–3980 (block 2, line 559 of 558) and mapctrl
  scope 1 records 5201–5203 (block 2, line 558 of 557), out of range under either numbering. The cause is not established,
  and the corpus tally does not settle the convention: 53,710 records address under either numbering, 9 only counting from 1,
  none only counting from 0 — the four literal samples above remain the discriminating evidence for 1-based (OPUS's
  `sn1_q0_domain.py` A/R, guarded resolver; the asymmetry itself does not prove the convention).
- **The end marks number 0–3 per scope, 59 in all** (ctrl 6, btlctrl 20, evctrl 23, mapctrl 10). Three occur in btlctrl 22,
  ctrl 1, evctrl 3, mapctrl 1 and mapctrl 3.
- **A tag addresses a logical line; it is not exact statement attribution.** The assignment at evctrl pc 16
  (`test_load_flg = 0`, logical line 416) and the `askpos` call at pc 22 both carry line 417. Four other `test_load_flg`
  assignments carry the next line's tag. OPUS's census over every variable instruction finds 2,166 on the tagged line and 304
  only on the line before. No emission rule is established.

**q1** is a counted `u32` table of heap positions — the scope's **jump-table name list**, sorted by
name. Corpus-wide it holds only `@`-labels (2,762) and named function/entry points (16: `DEBUG_MENU`,
`MJMENU_PAGE_CHG`, `MENU_TOP`, `summon`, `BEHIND_CAMERA`, `INDEX_MOVE`, …) — **no variable names at
all**; the earlier "`global_debug_flag[N]` partitioned per scope" and "named variables" readings were
wrong-heap-base artifacts and are retracted. q1 is index-parallel to the `.ebp` script record's
`+0x14` table — the script's **jump table** `{u32 count; u32 byteOff[count]}` — with `count == q1 count`
on 49/50 scopes (the exception, `evctrl` sc1 with its shared-code tail, has q1=160 vs table=158).
`jt[i]` is the byte position where `q1[i]` binds: `@CASE_N` → each case body (distinct ascending
offsets), `@WHJDE` → the loop head, `@WHTRS`/`@WHTRM` → the while term (`@WHTRM` = one past the last
instruction), `@IFELSE`/`@IFTERM` → the else/term point (a shared offset when the `if` has no `else`),
function names → their entry points — and the same entries are the targets the VM's jump opcodes select
(`4f idx; 09` → `jt[idx]`; verified: `jt[8]=0x7A`, `jt[2]=jt[3]=0x60` in `btlctrl` sc0 all land on
instruction starts). So **q1 × the `.ebp` `+0x14` table is the `@`-label → byte-position binding** —
the open "label binding table" was never in `.dbg`; the `.dbg` supplies the names and the `.ebp` the
positions, index-parallel. **q2** is a **stride-32 instruction checkpoint index**: its `j`-th entry
is the q0 record index (= bytecode byte offset) of the scope's `32j`-th instruction — verified exactly
(`ctrl` scope3: `q2[1]=0x5A` = the 32nd instruction's byte offset, `q2[2]=0xB8` = the 64th's; entry count
= ceil(instructionCount/32): 36 for 1134, 8 for 239, 3 for 70), a skip table for fast PC→record walks;
**q3** — *the two-list reading that follows is superseded; the correction closing this
paragraph resolves q3.* It was read as a **two-list** `u32` stream `{u32 countA; u32 0xFFFFFFFF; u32 listA[countA];
u32 listB[]; zero pad}` — ~~**`head` IS a count after all: it is listA's exact length**~~
(verified on all 50 scopes across the four modules: sentinel always `0xFFFFFFFF` at +4,
`listA = vals[:countA]`, `listB` = the remaining nonzero entries to the next table, ascending).
Zeros *inside* `listA` are legitimate entries — `btlctrl` sc19 `{2; FF; 0x0B; 0; 0}` decodes to
listA `{0x0B, 0x00}` = marks at bytes 11 **and 0** — which resolves the sc18/sc19 anomaly: the two
scopes have identical bytecode and identical `vals` bytes (`{0x0B, 0, 0}` both), differing only in
`countA` — sc19's countA=2 counts a trailing `0x00` as a real mark at the scope's first instruction
while sc18's countA=1 leaves it as padding.
The earlier "`head` is not the count / is scope-bound metadata" reading is retracted — `head` was
always listA's length; what differs between sc18 and sc19 is simply that sc19's first list carries
one more mark. All vals are **bytecode byte offsets** into the scope's script, ascending at a
steady ~11–12-byte stride covering only the scope's *prefix* (~12–30% of its code — `btlctrl`
sc1 marks stop at `0x574` of `0xFF2`, sc3 at `0xD7` of `0x25E`). The stride continues uniformly
across the A/B boundary — the split is positional, not spatial. Marks land interior to line runs
and uniformly across instruction byte positions (opcode/operand-low/operand-high ≈ 171/154/148) —
so they are not instruction boundaries, operand pointers, jump targets, or line-start bytes (all
tested, all fail). The mark *delta* histogram over the corpus peaks at 11 (10–13 typical) and
sc6's first twelve marks run exactly `+0x0C` each — a byte-periodic emission cursor, not an
instruction counter (instruction-index deltas vary 4 vs ~11–12 by scope). Scopes with identical
bytecode share identical mark *values* (`btlctrl`
sc12=sc16; all four modules' scope0 `[0xA,0x16,0x21,0x2D]` — the shared `systemctrl.ath` body).
Marks also appear with an **empty q1** (sc20: 4 marks, 0 names) — not q1 symbol bindings. The
listA/listB boundary correlates with structure: sc0's split is exactly the `.ebp` function-1
offset (`0x25`; A marks all below it, B above), and sc22's splits at the `switch(i0)` body
(lines ≤2379 vs ≥2384); other scopes split mid-stream with no func/jump boundary in the gap —
the semantic distinction between the two lists is unresolved. The strongest residual reading: a
per-prefix emission-cursor checkpoint stream; referent unresolved. *Narrowed 2026-09-23
(SWE2-DATA):* additional negatives measured — marks are not q0 line-run starts or ends (1–2
hits of 14–20), not instruction indices (index conversion yields no clean stride), not
`.ebp` jump-table positions (disjoint on all tested scopes), and the instruction-index delta at
each mark is irregular (~4–5 instructions, varying 3–8). The ~11–12-byte stride is
consistent with **one mark per emitted source statement** (a statement of debug-menu code
averages ~11–12 bytes), which would make q3 a per-statement emission checkpoint — but no
discriminator between "statement end" and "statement start +1" or a periodic cursor has been
found, and the listA/listB split still tracks nothing identified. *Narrowed further 2026-09-24
(SWE2-DATA):* the **mark count is exactly `floor(q0len/32)`** on ~all 50 scopes (all seven
`ctrl` scopes exact; a few others short by 1) — q3 is a **stride-32-budget checkpoint stream
parallel to q2** (q2 = stride-32 *instructions*; q3 gets one slot per 32 *bytes* of q0), and the
"prefix-only coverage" is simply that budget: ~`q0len/32` marks × ~11.6-byte spacing tiles only
the first ~36% of the code. Marks land on all byte positions of instructions uniformly (opcode/
imm-lo/imm-hi ≈ 171/154/148 in `btlctrl`) and their residues mod 32 march `+12` per mark with
occasional −1 slips — a near-fixed ~11.6-byte cursor, not a semantic sampler. Additional negatives
this pass: `.sbn` block-boundary positions (0 hits corpus-wide), `.sbn` **text** offsets (marks as
source-byte positions land mid-token with no boundary alignment), variable first-write positions
(imm values repeat freely), `@*JDE`/loop-head jump-table targets (sparse chance hits only),
control-flow opcodes at the listA/listB boundary (no consistent class), and exact stride-4
instruction indexing (`sc0` fits 3,7,11,15 exactly but `sc4`/`sc1` drift 3–5). The two live
readings: (a) **a per-emitting-line position sample** — marks advance ~1 source line each and hit
comment/blank/`}` lines indiscriminately, i.e. the cursor counts *emitted lines* at ~1.8 lines per
mark; (b) a flat ~11.6-byte periodic cursor recorded for a stride-32 budget — the line correlation
incidental because debug-menu lines average ~11–12 emitted bytes. The A/B split sits ~47–80%
through the mark run (usually near the median); it coincides with construct boundaries in `sc0`
(func1 entry) and `sc22` (switch body) but is mid-stream elsewhere — likely a writer-side
two-bucket partition of one stream, semantic unresolved. *Refined 2026-09-24d (SWE2-DATA):*
**the split is a clean positional cut of one ordered mark sequence** — `listA` and `listB` are each
ascending and `max(listA) < min(listB)` on every scope tested (marks continue the ~11.6-byte stride
seamlessly across the cut, e.g. `0xAD5 → 0xADF`), i.e. `listA` is the mark stream's sorted prefix
run and `listB` the contiguous suffix run. The cut lands at ~48–55% of the *marked byte span*
(≈ the median mark index: 254/246 for `mapctrl` sc1, 50/53 `ctrl` sc3, 97/99 `evctrl` sc1) and,
where visible, sits at a construct boundary — `mapctrl` sc1's cut falls between `break;` and the
next `case` inside `mapctrl_mj.src`'s page switch (block-2 lines ~170). The `blkIndex` hypothesis is
dead (both lists mix blocks 0/1/2), as is an interleaved even/odd split. Note: earlier reports of
last-scope `listB` anomalies (marks ascending past `q0len`) were a parse artifact — the true listB
ends at the next table, not the section end. The remaining live reading for the split itself: marks
may be **paired (begin,end) positions of nested emitted regions** — `max(A) < min(B)` is exactly the
signature of a family of intervals all containing the cut point — but `countA ≠ countB` (254 vs 246)
leaves that unproven. S2 is ~~a 0-terminated `u32` offset array (65 entries for ctrl/evctrl/btlctrl, 301 for~~ `{u32 count = 0x40; u32 offs[64]}` in all four modules *(corrected 2026-10-02, OPUS: the count word at S2 is `0x40` in the shipped `ctrl`, `evctrl`, `btlctrl` and `mapctrl` `.dbg`; §2's 64-slot directory)*
mapctrl) over 8-byte records and counted tables; the tail is a NUL-separated string heap ordered by class
(file paths, `global_flag[0..510]`, `event_global_flag[]`, `quest_global_flag[]`, `battle_global_flag[]`,
`g_menu_telepo_dest[]`, then scope-local identifiers); under the correct heap base every table position
is a name start (the earlier "may land mid-string" claim is retracted — a wrong-base artifact). The heap
is far larger than the name classes suggest — for
`btlctrl` it runs ~~`0x1CD7D..~0x41F4F`~~ `0x1CA20..~0x41F4F` *(corrected 2026-10-02, OPUS: the heap starts at header `+0x08` = `0x1CA20`, whose first bytes are `btlctrl.src` and the `systemctrl.ath` path; `0x1CD7D` lies inside it)* (≈150 KiB, essentially to EOF) and additionally contains the full
`global_debug_flag[0..4095]` block, module globals (`g_btl_hunt_*`, `g_com_mnp_*`), and the module's complete
set of **compiler-generated control-flow labels**, numbered by a global construct counter in compile order:
`@IFELSE_N`+`@IFTERM_N` pairs (per `if`: 213/234 for btlctrl/mapctrl, 33/63 ctrl/evctrl), `@WHJDE`/`@WHTRS`/
`@WHTRM` triples (per `while`: 21/8/10/9), `@SWJDE`/`@SWSFX`/`@SWCOD`/`@SWTRM` quads + `@CASE_N` + `@DFLT_N`
(per `switch`/`case`/`default`: 47/48/18/21 switches), `@FORJGE`/`@FORSFX`/`@FORCOD`/`@FORTRM` quads (per
`for`: 4/52/2/0) — e.g. `@IFELSE_000007`+`@IFTERM_000008` = one `if`. The labels **are** referenced by
q1 — under the corrected heap base each scope's q1 lists exactly its `@`-labels and named variables
(e.g. `btlctrl` sc0's 17-entry q1 = `@WHJDE_000000`, six `@IFELSE`/`@IFTERM` pairs, `@WHTRS_000001`,
`@WHTRM_000002`); the earlier "0 hits" reading is retracted. What stays open is the table binding each
`@`-label to its byte position in the script.

*CORRECTED 2026-09-28 (SWE2-DATA, on FABLE's
[`sn1-q3-page-map`](../../_index/candidates/sn1-q3-page-map/) record — M1/M2/X/C verified here, FAILS 0):*
**q3 is the byte→instruction page map, the inverse of q2** — `{u32 X; u32 map[E]; zero pad to the
next table}` where `map[k]` = the index of the last instruction that starts before byte `32k` of the
scope's code (`map[0]` = `0xFFFFFFFF` because no instruction starts before byte 0; `E = 1 +
floor((q0len−1)/32)`). Exact on **all 50 scopes** with every post-map word zero; the formula without
the `−1` matches none (control). The whole earlier chain — "bytecode byte offsets", "not instruction
indices", the `countA`/`listA`/`listB` cut, the ~11.6-byte stride, the "prefix-only coverage", the
sc0/sc22 construct-boundary coincidences — was an artifact of reading instruction indices as byte
offsets (the "not instruction indices" test converted mark *positions* to indices, the wrong
direction; any cut of an ascending array yields `max(A) < min(B)`, so the two-list split was never
evidence; sc19's `0`-valued "mark" is pad). What stays open is only the head word **`X`** — not a
count over the map (`btlctrl` sc18/sc19 carry byte-identical maps `{−1, 0x0B}` with X = 1 vs 2),
0.46–1.00 of E, semantic unresolved (FABLE's record lists the failed readings: code size, `.ebp`
directory fields, 32-line source pages, `.sbn` text span).

**`.msb` — message directory + tagged text streams.** A `u32[msgCount]` directory,
`msgCount = dir[0].offset / 4` (42 / 47 / 48 / 57 for ctrl/evctrl/btlctrl/mapctrl), each entry
`(flag << 16) | payloadOffset` with offsets strictly ascending. The payload is a NUL-terminated
(`00`) text stream in the module's custom charset (the JP glyph table, not the US one — so bytes
`≥ 0x80` are single-byte codes and must not be read with the `0x20..0x53` Latin mapping) with the
following verified token grammar:

- **`0F <cmd> <args>`** — variable-length escape, arity fixed by `cmd`: `cmd < 0x40` takes **2 arg
  bytes** (both observed `≥ 0x80` in every occurrence), `cmd ≥ 0x40` takes **1 arg byte** — with
  three verified exceptions: `!` (`0x21`) is zero-arg, `)` (`0x29`) takes `1+(a1&7)` packed bytes,
  `*` (`0x2A`) takes 2 args + `a2&0x7F` literal bytes (all pinned at instruction level — see the
  interpreter paragraph). The compact rule parses all 194 messages with **zero violations**. Observed cmds: 2-arg
  `{24, 25, 27, 28, 29, 2D, 2E, 2F, 37, 3C, 3E}`, 1-arg `{40, 42, 45, 48, 49, 4A, 4B, 50, 51}`.
  **The selector vocabulary is the same language the TZA interpreter `002AC5F0` speaks**
  (2026-09-22): that interpreter's escape prefix is `0x0F` followed by an ASCII selector in
  `0x20..0x70` ([the text control-code language](../../16-UI/Text-And-Number-Rendering/the-text-control-code-language.md)),
  and every `.msb` cmd is an ASCII char in that space. The arity split matches its semantics
  exactly: **every 1-arg cmd (`@ B E H I J K P Q`) lies in the TZA's `@`–`k` inline-icon-glyph
  block** (one byte = icon index), while the 2-arg cmds are its parameter escapes — `$` (+0x4C
  scalar; opens every message), `(` size-in-24ths, `)` **text colour** (the dominant per-span
  escape), `7` size-in-percent (`0F 37 81 <v>`, `v ∈ 0xBF..0xE4`), `%`/`'`/`&` left/centre/right
  justification, `.` insert-argument-`n` (pairs with the `10 C8 xx` argument counter), `-`
  number-format, `/` render-state, `>` context-actor name. Semantics are **inferred from the
  selector vocabulary** — the PS2 payload encoding (2 compact bytes vs the TZA's 3-byte parsed
  payload) differs, and no `.msb` consumer ships to verify against (§3).
  **Interpreter-level verification (2026-09-23, SWE2-DATA):** `002AC5F0`'s tag dispatch is a
  15-way jump table on `byte−1` (`002AE334`, arms at `byte 0x0F → 002AD01A`). The `0F` arm
  reads selector `0x20..0x70` through a two-level dispatch — `class = classtbl[sel−0x20]`
  (`002AE3FC`), `arm = casetbl[class]` (`002AE370`, 35 classes). It confirms the vocabulary at
  instruction level: **`@`–`k` (0x40–0x6B) all share one arm `002AE1F1`** — the inline-icon
  block, which copies the 0xD0-byte render state and derives a pixel advance from `[r14+0x33]`
  (glyph width × scale) — and **`%`/`&`/`'` share arm `002AD289`**, which stores the selector
  byte itself at `state+0x9A` and the arg at `state+0x99` before re-measuring — the alignment
  family, the selector carrying the meaning exactly as inferred. `(` (`002AD2F4`) is a
  signed-byte scale into `state+0x34` modulated by font field bits 4–8; ` ` (`002AD041`) the
  same into `state+0x40`. `0`/`_` and out-of-range selectors no-op (`002ACFC2`). The shared
  arg reader `003FFAB0` consumes a **2-byte packed argument**: `a2&0x7F` is the low 7 bits and
  `(a1&0xC0)<<1` the top 2 — a 9-bit value — except `a1&7==0`, which makes `a2&0x7F` a table
  index via `0039BA00` (font metric table). That is exactly the `0x80`-biased 2-byte argument
  the `.msb` streams carry (`81 xx`, `82 xx` …) — the PS2 compact arg and the TZA parsed arg
  are the same encoding, so the `.msb` payload arguments ARE verified-interpretable against a
  shipped consumer for the value; per-selector meaning still comes from the vocabulary mapping
  above (the PS2 `cmd` numbering vs the TZA ASCII selectors is not proven byte-identical).
  **Per-selector arity is fixed by a dedicated reader per arm** (each returns
  bytes-consumed in `eax`): `!` (`002AD151`) reads **no args** — a zero-arg
  "apply stored font" (installs `state+0xA6`'s font index via `0017FD30` into
  `state+0x60`/`+0x68`, fallback font 7 on lookup miss; `0F 21` never occurs
  in the control `.msb` corpus so the compact grammar was never exercised on
  it); `0x3FFAB0` readers = 2 args (` ` `#` `$` `%&'` `(` `7` `2` `4` `5` `6`
  `9` `V` `,` `/` `;` `p`); `0x3FFEE0` (`"`) = 2 args `a1&7F`/`a2&1F`;
  `0x3FFB90` (`m`,`n`) = 2 nibbles (`a1&0xF`,`a2&0xF`); `0x3FFDA0`
  (`3`) = 2 float args (`a&7F`/const); `0x3FFF10` (`.`/`1`, arm
  `002ADBF5`) consumes **3 bytes** (`a1&0xF`, `a2&0xF`, `a3&0x7F` —
  the `.` arm passes all-null outs, a pure skip) — but the `.msb`
  corpus shows `0F 2E` taking **2** args (`0F 2E 80 90 04` reads
  ` 0: ` under 2-arg, garbage under 3) — another PS2-vs-TZA arity
  divergence; `:` reads two packed args
  (`0x3FFAB0` ×2); **`*` (`002AD47C` → reader `003FFD6B`) is a
  variable inline string** — `a1`/`a2` words, cursor set to `cmd+3`,
  reader returns `(a2&0x7F)+3`, so `a2&0x7F` literal bytes trail the args;
  **`)` (`002AD3F7` → reader `003FFBC0`) is a different variable
  form** — `a1` packs `base<<3 | count`: `a1&7` = N (0–7) further
  bytes follow, decoded `out[i] = (a1>>3)<<7 | (b_i&0x7F)>>i` into
  `state+0x30` (the corpus's `0F 29 a3 b3 d5 99` runs; the bytes after
  `a1` are packed args, NOT glyphs — the old compact-2-arg reading
  misaligned them); `o`/`8`/`>`
  combine `0x3FFB00` (word reader) + `0x3FFAB0`. `0039BA00` indexes
  `tbl+1+idx*5` — 5-byte font-metric records, ≤511 entries.
  **Arg destinations pinned per arm (2026-09-23):** `$` (`002AD252`)
  packed arg → float `state+0x4C` (skipped when `state+0xB0 & 0x2000000`
  set); `7` (`002AE190`) packed arg → `state+0xA7` + sets
  `state+0xB0|0x200000`; `<` (`002AE1C5`) packed arg → `state+0xAB`;
  `/` (`002AE308`) reads a packed arg into scratch and discards it —
  a pure consume; `>` (`002ADE90`) packed arg then `00263990` on
  `state+0x78` (context-actor lookup, copies the 0xD0 render state);
  `-` (`002AD8AB`) reader `003FFC60` = `a1&0x7F` + `a2` split (low nibble
  clamped ≤8, top bits → third out) → `state+0xA1` region then
  `002AE610`; `"` = `a1&0x7F`,`a2&0x1F`.
- **Event-corpus extension (2026-09-23):** the ~10k `.ebp` modules under
  `plan_master/ch/event/` carry the same composition — **the slot map is
  uniform**: slot 0 = section-000 script image (`0x8000000B`, == the
  control modules' `.bin`), slot 2 = the message bank in the **same tagged
  `{u16 off; u16 flag}` format** (`nmsg = entry0.off/4`; entry0's flag
  varies 0/1 per module), slot 6 = `TIM2` icon sheet; event-only siblings
  are slot 8 = `CML1`, slot 9 = `CAM7` (camera choreography), slot 12 =
  a `{u32 count; {u16,u16}[]}` aux table, slot 14 = `LGT2` light group.
  Message bodies open `0F 24 81 81 · 0F 2F 81 80 · [0F 21]` then a glyph
  stream — `!` being zero-arg, the following `1c XX` bytes are the first
  glyphs, not arguments.
  Event text runs on leads `0x10`–`0x1D` (in-body census, 227 banks /
  4,229 messages: `10`=57,326, `1c`=44,830, `13`=2,467, `14`=2,617,
  `15`=2,359, `16`=1,863, `17`=1,722, `1d`=1,391, `11`=1,259,
  `12`=1,724, `18`=372, `19`=194, `1a`=15, plus 134 `0x81` bytes — those
  are **singles**, not a lead) — the 2-byte space is a flat
  `(lead,low)` index spanning `0x1000`–`0x1DFF`,
  with event dialog populating planes the menu modules never touch. The
  dialog codes are real text (scrambled order within messages, not glyph
  charts); the per-event `0F 21` (`!`) applies the font bound to the run.
  `12 xx` lows inside event text span `0x24`–`0xFE` — far beyond the
  menu punctuation/ASCII band — consistent with one glyph-ID space where
  menu text populates only `0x10`–`0x14` while dialog fills the rest.
  The ID→character table for the primary font IS shipped
  (`<loc>/font00.dat` record order — see the glyph-table bullet below);
  the residual is the secondary plane's font order (PS2 fontpack
  ordering, not reproduced by any shipped Unicode table).
  **One charset, verified**: event text reuses the single-byte kana range
  and the menu punctuation codes (`10 C4` = `。` ×113 in event bodies) —
  the `0x10`–`0x1D` leads are one glyph-ID space, not a per-module one.
  `evt_t0082` is a **charset/format conformance event**: its 67 messages
  enumerate every 3-glyph combination of the `0x1074`–`0x107D` block
  (which contains verified `10 75`=初 and `10 7A`=上), run `%`-format
  tests (`7%げこえけ / 8%うくげざえ`, `/ぺ0%` `/ぼ0%` — literal ASCII
  `0x20`–`0x3D` singles carry digits/`%`), and `alc_a0100`'s six messages
  are sequential `1c 20`→`1c 5E` glyph-chart pages. These test events are
  the best leverage for the remaining glyph map — glyph *order* is
  confirmed by the charts even where identity is not yet anchored.
- **Glyph-ID → character table (SOLVED 2026-09-23, primary plane):** the
  runtime maps a 2-byte code to a glyph index by
  `idx = LEADBASE[mode][lead & 0xF] + (sub − 0x20)` (`002AC2F0`), with the
  two tables lifted from the EXE — mode0 `00916570` =
  `[e0 1c0 2a0 380 460 540 620 700 | 0 e0 1c0 2a0 460 540 620 700]`,
  mode1 `009165B0` =
  `[e0 1c0 2a0 380 460 540 620 700 | 7e0 8c0 9a0 a80 0 e0 1c0 2a0]`.
  Mode and the font1/font2 threshold are **runtime-selected per language**
  at `002AB7D0`: language id `[01E02814]` ∈ {7,8,0xB} — the mask is
  `(id-7) & ~5 == 0` giving {7,8,0xB,0xC}, with `0xC` then excluded;
  shipped default `0xA` is *not* in the set — → threshold `0x1C` + mode1
  flag `[0209CC38]`; else `0x18`. (CORRECTED 2026-09-25 from `{7..0xA}` —
  the earlier range was a misread of the mask.)
  The index resolves in the locale's **`font00.dat` record order**
  (`gamedata/d3d11/artdata/font/<loc>/font00.dat` — 36-byte records
  `{utf8 cp; metrics; hash}`, header carries the font id) — **verified**:
  `10 75`→idx `0x135`→初, `10 7A`→上, `10 C4`→。, `10 68`→死, `10 99`→盗,
  `10 53`→技, `13 45`→読, plus full-sentence decodes (`btlctrl` msg10
  reads the reaction list `アクションモード【アクション/リアクション】`,
  `00:やめる 01:１撃 02:２連撃 … 10:カウンター … 16:吹っ飛び`).
  **Cross-locale**: `in` plan_map + `jp/font00` = natural Japanese
  (`あなたも政民でいらっしゃるの？`); `ch` plan_map + `ch/font00` = real
  Chinese (`往中層昇降梯`); `us` plan_map singles resolve through
  `us/font00` (`code−0x20` → Latin — the earlier `code−0x3A+'A'`
  approximation was the same table shifted by case).
  **Debug modules are JP-authored in the JP glyph space regardless of
  file locale** — `ch`/`in` `btlctrl.msb` byte-identical decodes under
  `jp/font00` (decode with `--font jp` always for `bin/` companions).
  `decode_msb.py --font <loc>` implements the formula + font00 table.
  **Residuals:** (a) the **JP-family secondary font** (`state+0xA6`,
  written outside the `0F` interpreter — only `!`/the common tail read
  it; the `0x2B18E6` region stores it per render job).
  **SOLVED 2026-09-24 — the `18`–`1B` planes are per-event glyph slots,
  not a font order.** `<loc>/fontex_subtitle.fex` (and
  `fontex_expand.fex`) are chained directories
  `{key; count; u32 cps[count]}` where **`key` = the engine path hash
  `00674A00` of `event\<dir>\<name>`** and `cps` = that event's
  expansion codepoints in first-use order; `18 xx`–`1B xx` index
  `cps[(lead−0x18)*0xE0 + sub−0x20]`. All **180 `in` event banks** that
  use the codes bind by key (158 subtitle + 22 expand), decode
  verbatim, and leave **zero font misses corpus-wide** — the earlier
  "fontpack order" residual was this mechanism seen without the key
  (the anchors `院商店興彼客` failed every global order because they are
  `alc_a0100`-local slots 0x2B/32/33/34/37 of that event's own table).
  Full write-up:
  [font-data-kerning-and-expansion.md](../../16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md)
  §"SWE2-DATA update (2026-09-24)". The secondary font IS proven for
  every other locale — `us` event `1c`-codes decode verbatim through
  `us/fontex_subtitle` at mode-0 base `0x460`, and `ch`/`cn`/`kr`
  `1c`-codes decode at mode-1 base `0` through their
  `fontex_subtitle` (`alc_a0100`:
  ch `元老院一派的抵抗已完全鎭壓住`,
  cn `元老院一派的抵抗已完全镇压住`,
  kr `원로원 일파의 저항은 완전` — the same opening
  line in each locale).
  **Corpus coverage** (345 `.ebp` banks per locale, message bodies only,
  2026-09-23): us **99.6%** resolved, ch **99.9%**, cn **99.9%**, kr
  **97.5%**, in **83.1%** (61,004 unresolved glyphs, all `g1h` =
  the `18`-plane font1 extension + `1f`-plane font2 misses) —
  **re-measured 2026-09-24 with the per-event `.fex` binding: `in` has
  ZERO font misses** (`g1h`/`g2` both 0 across all 345 banks; only 223
  unmapped `[xxxx]` FW-dictionary markers remain, icons/functional
  codes rather than glyphs). (b) `0x81` is a single glyph
  (font00[0x61] = `や`) — the former `81 xx` two-byte/digit-plane
  reading is retracted; the "verified `81 34..3D` digits" were actually
  singles `0x81` + ASCII `4`–`=`. (c) per-selector `0F` payload
  semantics on the PS2 numbering vs TZA selectors.
- **Prologue** — every message (194/194) opens `0F 24 81 81`, then 0–3 further escapes; the
  most common pattern is `0F 24 81 81 · [0F 37 81 CB] · 0F 2F 81 80` (the `0F 37` field is
  optional and appears in both flag classes).
- **`12 <b>`** — a 2-byte token whose arg is `≥ 0x80` in 10,730/10,742 occurrences; it is the
  dominant body token (~36 % of `evctrl`'s payload bytes) and reads as the regular text carrier.
- **`0E <t> <a> <b> <c>`** — a 4-arg line header (2026-09-22 arity fix; was read as 1-arg):
  every occurrence corpus-wide is `0e <type> 80 80 <80|81>` — a line-type byte then three
  `0x80`-biased fields (indent/extent/flags); `02 0E …` opens each item line in menus.
- **`02`** line break, **`04`** space — as in the documented charset. **`01`** is the
  **intra-item field separator** (576×, verified by ctrl msg29 — the `こうかおん・ボイス`
  SE/Voice menu whose items are `こうかおん` `01` `ボイス` `01` `オン`, three toggle
  positions per line; it also chains `01 01` for empty fields and precedes `0F` escapes
  at field boundaries). The only other low tag observed is `18` (5×, rare — `18 20`
  pairs; arity unpinned).
- **Positional census (2026-09-22):** `0F 24` is the *first* token in every message (194/194 —
  message-open); no single closing command exists (last token varies: `0F 29`/`0F 2F`/`0F 2D`/
  `0F 37`). `0F 37 81 <v>` recurs once per message with `v` ∈ `0xBF..0xE4` (a per-message scalar —
  window/voice-class parameter, meaning unpinned). The `(0F 2E, 0F 2F)` and `(0F 28, 0F 29)`
  consecutive-command pairs recur (30+ messages) consistent with region open/close, and the 1-arg
  family `(0F 48, 0F 49)`, `(0F 4A, 0F 4B)`, `(0F 50, 0F 51)` — always with arg `0x82` — pairs
  around item spans in menus (attribute on/off). Arg bytes are `0x80`-biased (`0x81`=1, `0x82`=2,
  `0x83`=3 …). Per-command semantics remain unverified without a consumer — these companions have
  no shipped loader (§3).
- Other bytes `< 0x80` (`10`, `11`, `18`, …) are tags/leads whose arities are partly pinned:
  `0E` is the 4-arg line header above, `01` is the field separator above, `10`–`1F`
  are the 2-byte glyph leads (`18` is rare in menus, 5× — its codes index font1's high
  range under `in`, see the font bullet). **Every byte `≥ 0x20` is a single glyph**
  `font1[c-0x20]` (`002AC376`): `0x20`–`0x3d` carry ASCII-ish text (`34 35` reads `45`,
  `27`/`28` bracket labels, `3c`=`<`, `3d`=`=` — item coordinates and ASCII runs inside
  Japanese strings), `0x3e`–`0xe3` are the interleaved kana planes, `0xe4`+ are fullwidth
  letters/`＿` label glyphs — **not** an icon texture plane (corrected 2026-09-23; the
  earlier `81`-lead and `e4+`-icon readings are retracted). The earlier
  "`10 C8 xx` argument-index counter" reading is also **corrected**: `10 c8` is a 2-byte
  glyph unit (font00[0x188] = `＿`, the per-item marker); the ascending bytes after it
  are ordinary singles.
- **JP glyph table — SOLVED (2026-09-23): the shipped `font00.dat` record order IS the
  table.** All earlier context-derived guesses in this bullet are superseded by the native
  formula (`002AC2F0`: `idx = LEADBASE[mode][lead&0xF] + (sub-0x20)`, mode/threshold chosen
  per language at `002AB7D0`) resolving into `<loc>/font00.dat` — see the font bullet above
  and `decode_msb.py --font <loc>`. Of the ~45 context-guessed glyph claims below, exactly
  the strongly-anchored ones hold under the table (技 死 盗 初 上 、 。 移 動 切 替 用 読 吹
  飛 and the punctuation run `10 c3`–`10 c8`); the rest were coincidental context fits
  (`10 67` is 士 not 現, `10 5e` is 効 not 変, `12 d1` is ASCII `+`, `12 dd`/`12 de` are
  ASCII `[`/`]` — "option brackets" were literal `[0:OFF&1:ON]` all along). **Do not use
  the old guess list; decode through the table.** What the table makes plain:
  - Bytes `0x20`–`0xFF` are **all single glyphs** `font1[c-0x20]` (`002AC376`) — `0x81` was
    never a lead (it is font00[0x61] = `や`; the "81 xx digit plane" and "81 7e bullet"
    readings were mis-pairings). jp font00 singles: `0x3e`–`0x90` hiragana (interleaved
    gojūon), `0x91`–`0xe3` katakana, `0xe4`+ = ヴ学ヶ and **fullwidth `Ａ`–`Ｙ`** — the
    former "e4+ icon plane" is the letter-label region (menu item markers/title bars);
    `0xff`→font00[0xdf]=`Ｙ` (the "indent pad" runs are letter glyphs in the real font,
    rendered as icon/blank cells). `0x35`–`0x3d` are fullwidth `１`–`９` (the old "5撃" read
    was byte-value confusion — actual text is `01:１撃 02:２連撃 03:３連撃` and
    `00:やめる` = "00:Cancel").
  - `0x10`-plane lows `0x10 20`–`0x10 3f` map to font00[0xe0–0xff] = fullwidth `Ｚ`,
    `ａ`–`ｚ`, then kanji `位囲移員愛` — the same letter-label class as the singles, not a
    texture-indexed icon block. `10 c8` → font00[0x188] = `＿` (the per-item marker). The
    "66% icons" residual evaporates: those codes were always decodable text/glyph IDs.
  - 2-byte codes: leads `0x10`–`0x1F` (font1) under the leadbase formula; `0x12`-plane
    lows are ASCII/halfwidth punct (`+ - [ ] < >` …) — e.g. `ギルたんまり[+999999]`,
    `[0:OFF & 1:ON]`. Kanji verified by the anchors above plus full-sentence decodes
    (mapctrl msg31, btlctrl msg10 reaction list, evctrl msg0 skeleton all read verbatim).
  - **Verified end-to-end**: evctrl msg0 (`select_base`) decodes as the title `Event Plan Menu`
    over items `Cancel / System menu / Map plan menu / Battle plan menu / Dev staff menu /
    Map jump / Reread map / Map jump [Location] / Map jump [Designated number] / Loading event
    … / MoB hunt menu / Entry setting / Scenario flag setting / Play BGM [designated number] /
    Boss Battle / Stop movie / Skip movie 0:watch/1:skip / Chapter txt preview`, and evctrl
    msg5 is the `Test Event` menu listing real event IDs with designer names —
    `EVT_T0017 [Iwabuchi]`, `EVT_T0015 [Tanaka Mizue]`, `EVT_T0087 [Kataoka]`,
    `EVT_T0010 [Matsuda]`, `EVT_T0007 [Miura]`. evctrl msgs 31–40 (`Scenario Event 1/1`…
    `10/10`) enumerate the **whole authored event list** by ID and English title —
    `NAF_A0100 [Reks Awakens]`, `NAL_B0100 [Battle with Seeq prisoners]`,
    `MIC_B0600 [Basch's Apology]`, `RSN_B0100 [Penelo joins the party]` … Third-module check: mapctrl's
    map-jump menus decode to real location names (ラバナスタ市街地, ガラムサイズ水路,
    空中要塞バハムート, ミリアム遺跡…) with `EVT_`-style `10xx` 4-glyph map codes per
    item, and mapctrl msg22's べんりメニュー includes `ビハインドカメラせってい` —
    the `behindcamera` sampler's menu entry.
  - **Verified against known plaintext**: msg37 `シナリオフラグ`, msg38 `スロットNにメモリーカード
    がささっていません`, msg40 `スロットNのメモリーカードをフォーマットしてよいですか？ いいえ/はい`,
    msg42/46 `セーブ`/`ロード` + slot digits, msg43/47 `セーブ/ロードに失敗しました`, msg39
    `セーブもしくはロード`. msg0 (`select_base`) decodes to the real debug menu — デバッグ設定,
    イベントスタートアップ, みんないなくなればいいんだ, チョコボ, キャラクター, マップ読みなおし,
    IDジャンプ, バトルテストマップ, ボスバトル, ロケーションジャンプ, セーブ/ロード — item for
    item matching `btlctrl.src`'s `case` comments. Kanji-plane (`12`–`14`) and `e2`+ single-byte
    assignments are per-glyph and still mostly unmapped; the kana coverage is complete.
    `decode_msb.py` next to this document implements the table and dumps all four modules.

The directory flag is **resolved**: `flag=1` is the authored **menu-class bit** — it marks
messages built to be the body of an **`aask`-family menu call** (`aask` verb `0x10`,
`aaske` `0x14A`, `aask_1ff` `0x1FF`). The call sites in the module's `.ebp` push the message
index as an int-pool `0x010000NN` constant (the pool is an identity map `pool[i]=0x01000000|i`),
and the constant-bound set equals the `flag=1` set **exactly** in `btlctrl` (22/22), `ctrl`
(35/35) and `mapctrl` (29/29); `evctrl` is 35/36 — and the exception is now explained
(2026-09-22): S2 names msg0's constant `select_base`, and its only source call site is
`basesel = aask(6, select_base, …)` inside `if(ISDEBUG()){ … } else { /* 本番用 */
aask(6, select_base2, …) }`. `ISDEBUG()` folds false in this build — the if-branch emitted
**no** code (no `4e 00` pool push and no `4f 00 00` literal push exists anywhere in the
module; the only emitted call in the region is the else-branch `select_base2` one), so the
debug-menu message is declared, named, pooled and flag-marked but never bound in emitted
bytecode. The flag therefore marks the constant's **authored menu class**, not a live call. `flag=0` messages are never menu-bound — they are plain display text, and `btlctrl`/`mapctrl`
run them as contiguous tails (19/21 entries) = a second, non-menu bank. The earlier byte-content
correlates (`10 C8` indexed items only in `flag=1`; the `02 0E` line-header, ~91% exact) follow
from this — menu bodies carry item markup — but the flag itself is authored binding metadata,
not a content predicate. **Corpus extension 2026-09-23 (SWE2-DATA):** the correlate holds at
scale — across **833 `ch` `.ebp` banks / 17,522 entries**, only flags `0` and `1` ship (78 % / 22 %);
**zero** flag-0 bodies contain the `0x0E` option-list header (0/13,705), while flag-1 bodies are the
interactive class: 3,774/3,817 carry the `0E`-header + option-marker items (`F是F否`,
`H保存L傳送移動H放棄`, numbered teleport lists), and the 43 exceptions are parameterized **input
prompts** (`公會位階：Ｌｖ<…>`, `請指定目的地：<…>`, `等級？<…>`) — still the ask-class, just without a
list body. So the authored bit reads *"this message feeds an interactive ask"* — menu bodies where
the list is literal, input prompts where the value is filled at runtime. What the flag does **not** gate: the `37` escape, length, or the
`0F`-cmd set. Per-`cmd` escape
semantics and the kanji-plane assignments are **not decoded** (§7); the kana/Latin table is.

**`.bin` — section 000 exported standalone (2026-09-22).** A fifth sibling carries the
module's linked form — and it is literally the `.ebp`'s section 000 in the documented
`0x8000000B` script-image format (see
`../../25-EBP-Script-Container/Bytecode-And-Opcodes/section-000-bytecode.md` — the `.bin`
"header" **is** the standard 0x90-byte section-000 header: `+0x14` sumTable, `+0x18` script
directory, `+0x20` u32-record int pool, `+0x24` float32 table, `+0x28` 8-byte-record table,
`+0x4C` name pool, `+0x50` i16 flag, metadata strings at `0x90`). On ctrl/btlctrl/mapctrl the
`.ebp` slot-0 payload is **byte-identical to the sibling `.bin` file** (zero divergences,
`ebp[0x80:0x80+binSize] == bin[0:]`); `evctrl` embeds an older link — its `.bin` is `0x80`
larger with section offsets shifted (+`0x10`…+`0xA0`), same format, different revision.
Metadata: `MM/DD HH:MM` build stamp (`ctrl` `01/15 23:18`, `btlctrl` `12/09 15:11`, `evctrl`
`09/12 15:44`, `mapctrl` `01/03 12:20`), author login (`katano`, `mtanaka`, `mtanaka`,
`Unknown`), source filename. The name pool (`+0x4C`) holds the module's entry points
(`init`, `main`, `callmenu`, `cancel_check`, `event_menu`, `mapjump_menu`,
`boot_boss_btl_ctrl`, `map_dsp_*`…) plus display strings in **Shift-JIS** (`コントロール`,
システム起動初期化…) — SJIS here vs the `.msb` custom table above.

**The `.ebp` embeds the `.msb` verbatim too.** The `EBP2` directory is 20 `u32` slot
offsets at `+0x10`; on `ctrl`/`btlctrl`/`mapctrl` **slot 2 (section 002) is the sibling
`.msb` byte-for-byte** (`ebp[dir[2] : dir[2]+msbSize] == msb`, zero divergences) — the
message bank ships inside the container as well as standalone. `evctrl` again embeds the
older revision (same directory shape, different offsets — matching its older `.bin`).
`btlctrl`/`evctrl`/`mapctrl` also carry slot 6 = a small `TIM2` texture (`0x180`–`0x540`;
a cursor/icon sheet, not the charset font); `ctrl` has slots 0+2 only. So the `.ebp`
container of each module is **envelope + section-000 image (== `.bin`) + message bank
(== `.msb`) + optional TIM2**, and the earlier "{u16;u16} tail records" reading was the
section-002 message directory mis-parsed — retracted.

New correlates this pass: the `+0x20` pool's `0x010000NN` message refs number **exactly
`msgCount` on all four modules** (42/48/47/57 — in mapctrl split into runs `0–0x1E` +
`0x1F`–`0x38` around `0x000080NN` ID-class entries and literals like `0x000F423F` = 999999);
`mapctrl`'s float table (`+0x24` → `0x3D4`) is `{count=6; float[6]}` = `-1.0, -0.4, 0.0, 0.3,
0.6, 1.0` — **verified as the `MAP_BEHIND_*` parameter table**: menu msg27 (`ビハインドカメラ
せってい`) prints each constant with its value in order — `MAP_BEHIND_LOOKUP[−1.0]`,
`PARALLEL[−0.4]`, `NORMAL[0.0]`, `NML2LD_1[0.3]`, `NML2LD_2[0.6]`, `LOOKDOWN[1.0]` — exactly
the table's six floats. No float literals appear in `mapctrl.sbn`, so the table is
header/toolchain-emitted (the `MAP_BEHIND_*` constants are header enum indices into it).

## 3. The loader contract

**No loader opens these files, by two independent routes.**

- **By name.** No path in the image names them: the stems `ctrl` (as a file component), `btlctrl`,
  `evctrl`, `mapctrl` and `systemctrl`, and the extensions `.sbn`, `.msb`, `.dbg` as NUL-terminated
  strings, all occur 0 times.
- **By the ATEL sibling loader.** `003306E0` (called from `ActorResource_BeginManagerResourceSetLoad`,
  `00330029`) takes a manager's resource path and writes sibling names by replacing its extension with
  the table at `00D10990` — `bin`, `dbg`, `sbn`, `msb`, `msf`, `fnt`, `cam`, … (~~`0033078D`–`00330A59`~~
**`0033078D` to at least `00330BD9`, 25 unrolled `lea` sites, one per extension — not a table walk;
the cited range covers the first six; §9**) — then
  asks each one's size with `0032E400(0xFF, name)` (`00330E47`–`00330F1E`). **`0032E400` returns −1 for
  kind `0xFF` before any lookup** (`0032E404 cmp ecx, 0xff` → `0032E438 or eax, -1`), so every sibling in
  this route reports no file. The base names are manager script paths, none of which has these stems.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| the whole file (all three extensions) | — | — | — | **yes — unnamed in the image, and the only route that forms these extensions resolves every size to −1** |

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `003306E0` | ATEL sibling loader: extension substitution and size queries | ◐ the name building and the size calls |
| `0032E400` | resource size by (kind, index); kind `0xFF` returns −1 | ✅ full body |

### Data addresses

| Address | Name | Kind | Contents |
|---|---|---|---|
| `00D10990` | ATEL extension table | `.rdata` | `bin dbg sbn msb msf fnt cam camera lgt cml cmi shk skl vld` |

## 5. Corpus survey

`btlctrl` 98,136 / 7,141 / 270,160 B (`.sbn` / `.msb` / `.dbg`), `ctrl` 24,976 / 3,029 / 83,120, `evctrl`
57,816 / 26,953 / 126,112, `mapctrl` 140,128 / 10,864 / 301,776. `evctrl.msb` has no printable run at all.
Symbol names include a flag named `g_com_e3_flag` and a second source file `mapctrl_mj.src`.

## 6. Falsification pass

~~Not yet run.~~ *(answered: falsification pass 1 ran 2026-09-13, §9; 2026-10-02, OPUS)*

## 7. What this document does not claim

- [x] **SN-1.** The inner layouts of the three companions — the `.sbn` block header pair and `u16` table, the
      `.dbg` symbol records, the `.msb` message encoding — and whether the `.sbn` blocks are the source
      the compiled scripts were built from. No reader exists in this build. `SN-1`.
      ***NARROWED 2026-09-18 (FABLE), DATA from the archive, and the second half answered: the blocks are the source the module was built from.** *`.sbn`.* One block per source file. Block 0 is the module's own `.src` (its `#include` lines open it: `p:/tool/atel/header/ateldebugfunc.ath`, `atelcommfunc.ath`, `common.ath` in `ctrl.sbn`; `${ATEL_HEADERPATH}/common.ath` and the flag headers in the other three); block 1 is `systemctrl.ath`, 1,828 bytes and byte-identical in all four files (header `(79, ...)`, 79 lines: `#ifndef __SYTEM_CTRL_ATH__`, the five `#define ATEL_EXECSPACE_*` lines); block 2, only in `btlctrl` and `mapctrl`, is `mapctrl_mj.src` (557 / 558 lines of the map-jump debug menu, the file the `.dbg` of those two names). The header pair is `(lineCount, x)`: the first word counts the block's lines (977 in `ctrl.src`, 2,507, 2,456, 2,768 in the other modules' sources) and is followed by `u16[lineCount]` line-start offsets, ascending in runs and resetting (0, 28, 30, 74 ... 789, then 0, 0, 39, 81 ... in the header block), then the text, NUL- and newline-separated; what the second word measures (2,124 for `ctrl.src`, 23,356 for the header block at `0x5A6C`, 208 past its own offset) was not resolved. *`.dbg`.* The header is three ~~`(offset, size)`~~ `(section offset, table offset)` *(corrected 2026-10-02, OPUS: the second words are `0x78`/`0x7C`, `0x6C` and `0x160`..`0x280` in the four shipped `.dbg` files, front-region offsets, while slot 1's section runs to the end of the file)* pairs (`0x8478, 0x78`; `0x88A0, 0x6C`; `0x8794, 0x160` in `ctrl.dbg`): the second names the source files and the declared variables (`ctrl.src`, `c:/cygwin/home/katano/ps2/ff12_ps2/katano/systemctrl.ath`, `eventlist`, `mimiclist`, `snapexec`, `snapshotpos`, `movienum`, `cameramode` ...; `btlctrl.src`, `c:/plan_work/jp/event/header/systemctrl.ath`, `mapctrl_mj.src`, `g_com_debug_flag` ...), the first and third are `u32` offset arrays (7 and 64 entries), and the body from `+0x30` is a further offset array over records that carry the element names `global_flag[0]`..`global_flag[510]` (511 in every file) and the headers' globals: 2,023 to 3,093 identifiers per file, of which 43 to 71 are declared in the `.sbn` text and 167 to 245 mentioned there; the record layout around those names was not read. *`.msb`.* A table of `(u16 offset, u16 flag)` entries up to the first offset (42, 48, 47 and 57 messages; flag 1 on 35, 22, 36, 29 of them), each message in the game text charset with the `{0F..}` escapes and about half its bytes in the CJK glyph range (47-53 %), i.e. Japanese debug-menu text (`mapctrl.sbn` opens with `MAP DEBUG MENU`). *The source question.* The compiled `ctrl.ebp` (EBP2, its script section decompiled with ff12-script) carries `Source: ctrl.src`, `Author: katano`, `Date: 01/15 23:18` and six actors, `control`, `snapcheck`, `push_button_actor`, `hddctrl`, `movie_atrac3_ctrl`, `saveactor`; every one is declared in `ctrl.sbn`'s text (`ctrl snapcheck`, `ctrl hddctrl`, `ctrl saveactor` ...), the `.dbg` names the same `ctrl.src`, and the author's own path is the `.dbg`'s. So the `.sbn` is the source of the shipped module, kept beside it with its symbol table and messages, and none of the three is read by this build (§3). Still open: the second header word and the exact run rule of the `u16` table, and the `.dbg` record layout.*
      ***NARROWED 2026-09-21 (SWE2-DATA), all four modules' companions decoded structurally — §2 has the layouts.** The `.sbn` block is fully resolved: the second header word is the **file-absolute offset of the block's text** (`0x84C` for `ctrl.src`; the 2,124 and 23,356 FABLE left open are exactly the two text starts), and the whole `u16` span is a **paged line map, 32 lines per page** — full pages are ~~`{u16 lineOff[32]; u16 chunkEnd; u16 0}` with `chunkEnd` the file-absolute last byte of the page's text chunk~~ `{u16 lineOff[32]; u32 nextPageBase}` *(corrected 2026-10-02, OPUS: 88 of the 312 trailers in the shipped `.sbn` files have a non-zero high half, read through `vbf_read_entry`)*, the final page a bare `u16 lineOff[32]` with unused slots zeroed, giving `(pages−1)·34 + 32` u16s exactly on all 9 blocks (1052 for `ctrl.src`, 100 for `systemctrl.ath`); chunks tile contiguously `[textOff .. blockEnd)` and `lineOff[j]` locates line *j*'s slot inside its page's chunk (a slot may begin inside a NUL-run where blank lines widen the gap). The "second `u16` array" previously reported was the tail pages read from a misdrawn boundary — it does not exist. `.dbg` is now mapped end-to-end: five ~~`(offset,size)`~~ `(section offset, table offset)` *(corrected 2026-10-02, OPUS: as §2; the second word `0x6C` is the same in all four files)* header slots (three used), a 17-entry `dirA` of packed `{count; u32[count]}` tables, a front `{u16 srcTextOff; u16 flags}` stream whose first field lands inside the module's `.sbn` block-0 text, the S0 per-scope directory (`{count; offs[4·count]; 0}`, 7/13/23/7 scopes — a scope is four tables: source-position stream, name index, two counted tables), the S2 record index, and the class-ordered string heap. `.msb` is a `(flag<<16)|offset` directory over NUL-terminated tagged text streams — the token grammar is now pinned: `0F <cmd> <args>` escapes are variable-length by `cmd` (2 arg bytes, both `≥ 0x80`, for `cmd < 0x40`; 1 arg byte for `cmd ≥ 0x40`; zero violations across all 194 messages), `0F 24 81 81` opens every payload, `12 <b≥0x80>` is the dominant 2-byte body token, `0E <b≥0x80>` a 1-arg tag, `02`/`04` are line break/space, and `10 C8 xx` runs as an argument-index counter; the flag bit has one correlate — `10 C8` sequences occur only in `flag=1` messages (one-directional; flag=1 messages without them exist), marking a menu/selectable class, and `btlctrl`/`mapctrl` run contiguous `flag=0` tails consistent with a second bank. *Still open:* the `.dbg` record-payload grammar (what T1's non-aligned offsets index, the mid-string heap anchoring rule, the flag classes), the `.msb` flag's exact semantics, the per-`cmd` escape semantics / JP glyph table, and the remaining low-tag arities. The `.sbn` format itself is fully decoded — nothing open remains there.*
      ***NARROWED further 2026-09-21 (SWE2-DATA), `.dbg` interior deepened.** The per-scope q0 stream is `{u16 pos; u8 blockIndex; u8 flag∈{0,1}}` 4-byte records where **`pos` is the ~~0-based~~ 1-based logical source line number in the `.sbn` block selected by `blockIndex`** *(corrected 2026-10-02, SWE2-DATA, on `q0_domain.py`/`entry_lines.py`/`logical_lines2.py` — see §q0 above: the four literal samples discriminate 1-based, backslash continuations fold, six records sit one past their block's end, cause unknown)* (block-1 records = exactly 151, `pos 0x21..0x4C`, byte-identical across all four modules = the shared `systemctrl.ath`; block-2 only in the 3-block modules; include blocks are embedded inline in the including scope's stream) — direct content verification: `flag=1` marks land on statement lines (`main`, `if( debug_padd() )`, `snapend();`, actor decls) and scope ranges tile the file sequentially (`evctrl` `0x21..0x4C → 0x198..0x4BF → 0x4C5..0x505 → …`, `mapctrl` likewise), i.e. each scope is one top-level entity's contiguous line region. Items are fixed-arity — 1 or 3 same-`pos` records; size-1 on structural lines, size-3 on statements. Quartet roles: q0 = position stream (line numbers), q1 = counted heap-position name table, q2 = stride-32 item checkpoint index (q0 record index of every 32nd item — exact on all scopes), q3 = counted list headed `0xFFFFFFFF` then ~11–12-stride item indices covering only a prefix of the scope (referent open). The heap is **suffix-compressed** (`global_flag[25]` ⊂ `event_global_flag[25]` at +6); T3/T4/T8/q1 land mid-string at irregular depth — heap positions, not name pointers; refined further: entries land anywhere in a name's span including its terminator (12–183/file) with exact duplicates, so the referent is the enclosing name span and the depth is writer-internal. T1 is a byte-granular position-ordered index over the scope-table region (all mod-4 classes, in-order → non-decreasing `pos`); what it marks per item is unresolved. Front stream resolved as a **pair directory**: `u32` pairs `{nameHeapPos; index}` — positions ascend the heap at name-length strides (the stride-24 lattice = `global_debug_flag[NNNN]`'s exact 24-byte names), indices count `+1` through a 12-bit (4096-slot) symbol space, wrapping once and re-covering a prefix (aliases). btlctrl index `N` ↔ `global_debug_flag[N+34]` (indices 0..4061 = debug flags, 4062..4095 = module names); tagged indices (`0x3000|counter`, `0x2000`, `0x5800`, `0x1000`, `0x4000`) mark additional index classes, some byte-identical across modules. **Retraction:** a8c4f705d's scope-sectioning via `0xFFFF` and the `(class<<8)|blockIndex` decomposition were misparse artifacts — the stream was read past its true end (the first `dirA` table) into the packed u32 tables, so `0x0002`/`0x0100`/`0x0101`/`0x0102`/`0xFFFF` "classes" and the sentinel count matching scope count (those were q3's `0xFFFFFFFF` list headers) do not exist in the real stream; and 99711fc65's "u32 tagged-value stream" framing is superseded — the tags sit in the index slot, not a position high-half.*
      ***q0 RESOLVED 2026-09-22 (SWE2-DATA): it is a byte-granular bytecode→source map.** Scope *i* is `.ebp` script-directory entry *i* (23 = 23 in `btlctrl`, 7/13/7 likewise), and q0 record *i* describes **byte *i* of that script's code** — `{u16 lineNo; u8 blockIndex; u8 flag}` where `flag=1` marks the instruction's first byte. Decoding the bytecode with the opcode length table (`0x03–0x47` → 1 B, `0x48–0x63` → 3 B) reproduces every `flag=1` position exactly in every scope of all four modules, `flag=1` count == the script's `numOfInstructions`, and record count == bytecode bytes + ~~0–2~~ 0–3 trailing `(0,0,0)` end marks *(corrected 2026-09-30, SWE2-DATA, on OPUS `397727019`: the suffix is padding to a multiple of 4 — 5 scopes carry 3)* — so the "arity-{1,3} items" were simply the instructions' own byte lengths. q2 = stride-32 **instruction** checkpoint (q2\[j\] = byte offset of instruction #32j). q3 = bytecode byte offsets landing on instruction-start and operand bytes (`PUSHV`/`POPV`/call-family recur) — referent open. **q1 correction:** q1 *does* list the `@`-labels — it is each scope's complete symbol set (compiler labels + named variables); the earlier "no `@`-label references" tested the wrong population. Edge case: `evctrl` scope1's stream runs 144 bytes past its script's directory bound (48 extra instruction marks attributed to one `case`-body line — a shared/dedup code tail).* The heap is **suffix-compressed** (`global_flag[25]` ⊂ `event_global_flag[25]` at +6); T3/T4/T8/q1 land mid-string at irregular depth — heap positions, not name pointers; refined further: entries land anywhere in a name's span including its terminator (12–183/file) with exact duplicates, so the referent is the enclosing name span and the depth is writer-internal. T1 is a byte-granular position-ordered index over the scope-table region (all mod-4 classes, in-order → non-decreasing `pos`); what it marks per item is unresolved. Front stream resolved as a **pair directory**: `u32` pairs `{nameHeapPos; index}` — positions ascend the heap at name-length strides (the stride-24 lattice = `global_debug_flag[NNNN]`'s exact 24-byte names), indices count `+1` through a 12-bit (4096-slot) symbol space, wrapping once and re-covering a prefix (aliases). btlctrl index `N` ↔ `global_debug_flag[N+34]` (indices 0..4061 = debug flags, 4062..4095 = module names); tagged indices (`0x3000|counter`, `0x2000`, `0x5800`, `0x1000`, `0x4000`) mark additional index classes, some byte-identical across modules. **Retraction:** a8c4f705d's scope-sectioning via `0xFFFF` and the `(class<<8)|blockIndex` decomposition were misparse artifacts — the stream was read past its true end (the first `dirA` table) into the packed u32 tables, so `0x0002`/`0x0100`/`0x0101`/`0x0102`/`0xFFFF` "classes" and the sentinel count matching scope count (those were q3's `0xFFFFFFFF` list headers) do not exist in the real stream; and 99711fc65's "u32 tagged-value stream" framing is superseded — the tags sit in the index slot, not a position high-half.* ***T1 RESOLVED 2026-09-22 (SWE2-DATA): it is the ATEL verb-category directory.** The 67 reset-delimited sub-lists are name-start heap positions (all 1,389/1,389 land on NUL-boundary name starts with base = header `+0x08` = S1 = the heap origin, *not* the earlier `0x5170`), and each bucket decodes to a thematic verb family — list 18 = `camerashake*`, 66 = `blur*`, 6 = `bganime*`/camera, 48 = `bgmstream*`, 24/30 = `anime*`/`lookat*`, 12 = `setmap*`/`resetmap*` — the same bucket→family mapping in all four modules, with byte-identical list lengths for buckets 0..65 and a module-specific tail in bucket 66. 1,153 distinct verb names in `btlctrl`. The earlier "file offsets into the tail slice" reading was a numeric coincidence with the pre-S0 record stream.*

      ***CORRECTED 2026-09-28 (SWE2-DATA, on OPUS's SN-1 candidate `_index/candidates/sn1-layouts/` `sn1_layouts.py` — S1–S4, D1–D4, FAILS 0, re-verified on all four modules).** Three claims in the narrowings above are superseded, §2 carries the corrected text: (1) the `.sbn` page trailer is a single **u32 = the next page's file-absolute first-line offset**, not `{u16 chunkEnd; u16 0}` — 88/312 trailers have a non-zero high half, and the `chunkEnd+1` reading misplaces 917 of 10,139 line starts; `lineOff` is **page-base-relative** and the NUL-run special case is retracted. (2) The `.dbg` `+0x2C` sections are the **native-command name tables**: section *k* entry *i* = command `(k << 12) + i` (7,297/7,303 catalogue agreement; `0x20C8`/`0x20C9` = `jfdemo` in ctrl/btlctrl/mapctrl vs `e3demo` in evctrl — different build verb tables). (3) T1's '67 verb-category sub-lists' are **pool de-duplication resets** (D4), so T1 = the class-0 verb-name table in id order; T3/T4/T8 = class-2 debug / class-3 `btlAtel` / class-7 `fsmenu` tables — the `result`/`eventresult`/`global_flag` name-range readings were pool-base-less artifacts.*
      *OUT OF EVIDENCE BOUNDARY 2026-09-29 (OPUS), for the one residue left, q3's head word X: the excluded artefact is the ATEL compiler that emitted each `.ebp` / `.dbg` pair, no admitted source carries it (no companion reader in the image, no PE or ELF in the extract), and the negatives hold. Signed by SWE2-AUDIT-SEM; package [`sn1-x-oeb-package`](../../_index/candidates/sn1-x-oeb-package/README.md); register row `SN-1`. What X counts is not claimed.*
## 8. Related

- [`section_009`](../../25-EBP-Script-Container/Sections/section-009.md) §3 — the same sibling loader binds `camera/<name>.cam`, also dead.
- [The script interpreter](../Interpreter-Core/worldactor-scriptvm-interpreter.md) — the shipped script format these PS2 files predate.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

*(`check_already_answered.py` run first, one query at a time and read in full.)*

### The corpus reproduces exactly

Re-extracted from `FFXII_TZA.vbf` and walked with independent code: **8 `.sbn`, 8 `.msb`, 8 `.dbg`**;
**12 / 12** `ch` copies byte-identical to their `in` copies by digest; **8 / 8** `.sbn` block tables
valid with the first offset exactly `4 × (count + 1)`, ascending and in bounds — and the counts fall
exactly as §2 says, **3** for `btlctrl` and `mapctrl`, **2** for `ctrl` and `evctrl`. Every one of the
twelve sizes in §5 is exact: `btlctrl` **98,136 / 7,141 / 270,160**, `ctrl` **24,976 / 3,029 /
83,120**, `evctrl` **57,816 / 26,953 / 126,112**, `mapctrl` **140,128 / 10,864 / 301,776**.

### The negative is sound, and its controls are worth writing down

Route 1's eight literals all occur **0** times, as claimed. What makes that a finding rather than a
failed search is what the same method returns for extensions this build *does* use:

| searched | occurrences |
|---|--:|
| `btlctrl`, `evctrl`, `mapctrl`, `systemctrl`, `\ctrl.`, `.sbn\0`, `.msb\0`, `.dbg\0` | **0 each** |
| `.ebp\0` | 10,380 |
| `.bin\0` | 2,144 |
| `.seb\0` | 608 |
| `.mpk\0` | 550 |
| `.sab\0` | 129 |

> **And the bare stems are present exactly where the page says they should be**: `sbn` and `msb`
> occur **once each** in the whole image, `dbg` eight times. Those single occurrences are the
> extension-substitution entries themselves. So the strings exist **only** as substitution material
> and **never** as part of a file name — which is a sharper statement of route 1 than "0 occurrences",
> and it is the shape the census's own controls were reaching for.

Route 2 reproduces to the instruction: `0032E404 cmp ecx, 0xFF` → `0032E40A je` →
**`0032E438 or eax, 0xFFFFFFFF`**, before any table is touched — the addresses §3 gives, exactly.

And the table at `00D10990` reads back as §4 lists it, in order: **`bin dbg sbn msb msf fnt cam
camera lgt cml cmi shk skl vld`** — fourteen inline NUL-separated strings, not a pointer array.

### ⚠ The substitution is unrolled, not a table walk

§3 cites `0033078D`–`00330A59` for the extension substitution. Those are **six** `lea` sites —
`00D10990` `bin`, `00D10994` `dbg`, `00D10998` `sbn`, `00D1099C` `msb`, `00D109A0` `msf`,
`00D109A4` `fnt` — and the references **do not stop there**: `003306E0` contains **25** `lea`
instructions into the block, continuing `00330AA4`/`00330AAB` (`cam` **and** `camera`, two strings in
one step), `00330AD4`/`00330ADB`, `00330B49` `cml`, `00330BD9` `cmi`, and on.

**There is no loop and no bound**: each extension is named by its own instruction at its own offset.
So the cited range covers the first six of the fourteen §4 lists, and *"replacing its extension with
the table"* describes the effect rather than the mechanism. **The conclusion is untouched** — every
one of those sites still ends at a `0032E400(0xFF, …)` that returns −1 — but a reader following the
range will find a sixth of the sites.

### Where the fourteen end

The block continues past `vld` with **`m%02d`**, **`.mld`**, **`CAMDAT`**, **`CAMCTL`**, **`SHKDAT`**,
**`SHKCTL`**, **`CHRMDL`**, **`LGTDAT`**, **`PREFIX`** — a printf format, a dotted name and uppercase
tags, none of them the shape of a bare extension. So the fourteen really are a group, **but nothing in
the data marks the boundary**: it is where the `lea` sites stop naming extensions, which is a fact
about the code and not about the table.

**Not claimed.** `SN-1` is narrowed to the residual below (§7) — the container layouts of all three
companions are decoded (§2); what remains is the *semantics* inside them. ~~Whether
`003306E0`'s size queries can reach a kind other than `0xFF` on some other path: **only the
`0xFF` call sites were read**, and the function is 3,882 bytes. What `00330E35 cmp esi, 0x10` bounds.
Whether the nine strings after `vld` belong to the same consumer.~~ *Answered 2026-09-29 (OPUS
record `a31c65871`, [`atel-sibling-loader-gate-opus`](../../_index/candidates/atel-sibling-loader-gate-opus/README.md),
`sibling_gate.py` FAILS 0, re-run by SWE2-DATA): all **14** `0032E400` sites in the body load
`ecx = 0xFF`, for which `0032E400` returns -1 before reading the id; the **first** query (the
manager's own path) gates everything after it - its result goes to `r15d` (`00330E58`) and
`00330F7D jle` jumps to the epilogue `003315E7`, with no jump entering past the gate - so
`003306E0` **returns without registering anything in this build**. `cmp esi, 0x10` bounds a
16-pass loop naming `<stem>.m00.mld` ... `<stem>.m15.mld` (`m%02d` at `00D109CC`, `.mld` at
`00D109D4`). Of the nine strings after `vld`, eight are this body's (`m%02d`, `.mld` and the six
tags `CAMDAT` ... `LGTDAT`); `PREFIX` (`00D10A0C`) is referenced only by `0032F67C`, another
loader's kind-8 buffer tag.* What the `.mld` files hold, and how any file behaves on a build where
kind `0xFF` resolves, is not claimed. The archive was **read, never
written**, and nothing was executed.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**Presentation — CLIENT and SERVICE.**

- The file-size probe `0032E400` is shared with two Presentation bodies, of 119 and 337 bytes.
- The 3,882-byte body `003306E0`, which carries `"camera"` strings, calls a 498-byte Presentation body.

Both are shared file and presentation services, not debug-companion logic.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**ActorEntity — CLIENT (7 edges through 2 of this page's functions).** The ActorEntity layer reaches this page at `003306E0`, `0032E400`. `FUN_00263ff0` is the worked example, read in full - it is **twenty-one bytes that state the manager stride**: index times **`0x288`** added to `02098E10`, with no bound and no null test; **4 of the 6 bodies on that layer are read, the rest are counted**. The crossing is that those functions are consulted by that layer, not a shared responsibility. Edge count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).
- **CoreRuntimeScheduling — CLIENT and SERVICE (3 edges).** 1 inbound (CoreRuntimeScheduling bodies `0022A0B0` call page-cited `002AB7D0`); 2 outbound (page-cited `002AB7D0`, `002AC5F0` call CoreRuntimeScheduling bodies `00229E40`). Substantive edges include `002AB7D0` is called by `0022A0B0`; the remaining edges run through shared helpers the page cites.
- **Resource — CLIENT and SERVICE (15 edges).** 14 inbound (Resource bodies `00384420`, `0039C3F0`, `0024AC30` call page-cited `0032E400`, `00674A00`); 1 outbound (page-cited `003306E0` call Resource bodies `0032E400`). Substantive edges include `0032E400` is called by `00384420`; `0032E400` is called by `0039C3F0`; `0032E400` is called by `0024AC30`; `0032E400` is called by `00249210`; the remaining edges run through shared helpers the page cites.
- **Story_Event_Quest_Hunt — SERVICE (1 edge).** 1 outbound (page-cited `00263990` call Story_Event_Quest_Hunt bodies `PersistentFlag_QueryBank2048` (0032A930)). Substantive edges include `00263990` calls `PersistentFlag_QueryBank2048` (0032A930).
- **UI — CLIENT and SERVICE (16 edges).** 14 inbound (UI bodies `002AC5F0`, `002AF340`, `002B2150` call page-cited `002AC2F0`, `0017FD30`, `002AC5F0`); 2 outbound (page-cited `002AC5F0` call UI bodies `002B2150`, `002AE610`). Substantive edges include `0017FD30` is called by `002AF960`; `0017FD30` is called by `002AC5F0`; `00263990` is called by `002AC5F0`; `002AC2F0` is called by `002AF340`.
- **World — CLIENT (1 edge).** 1 inbound (World bodies `00378540` call page-cited `0032E400`). Substantive edges include `0032E400` is called by `00378540`.
- **WorldAreaField — CLIENT (5 edges).** 5 inbound (WorldAreaField bodies `MapRef_BeginLoadResources` (00268750), `00378030`, `AreaArd_LoadOrUnloadFieldResource` (003EA820) call page-cited `0032E400`). Substantive edges include `0032E400` is called by `MapRef_BeginLoadResources` (00268750); `0032E400` is called by `00378030`; `0032E400` is called by `AreaArd_LoadOrUnloadFieldResource` (003EA820); `0032E400` is called by `00379A10`.
## The `003306E0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`003306E0` (~~~351 B~~ 3,882 B *(corrected 2026-10-02, OPUS: its last `ret` is `00331609`, the size the SN-1 answer above gives)*) — six-register ctrl-module body
(`003306E0`/`003306E7`).

| member | role | interior |
| --- | --- | --- |
| `0032F6F0` | stack-cookie `0x120` frame (`0032F6FD`/`0032F707`) | [`0032F6FD`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## Interior citation — frontier hub `0032E400` (2026-09-17, SWE2-EC7)

`0032E400` — 80 B, 18 A-measured callers at census; the "resource size by (kind, index)" getter
this page already documents (`0xFF` -> -1). Interior verified end-to-end: `ecx != 0xFF` indexes a
per-kind pointer table at `022C51F0` (`movsxd`/`[r8+rax*8]` at `0032E40C`); a null table or
`index >= 0x400` falls to `call 0046DE70`; the hit returns `[table + index*4]` at
[`0032E428`](../../_index/ADDRESS-INDEX.md), and the shared exit rounds a positive result UP to a
64-byte multiple (`+0x3F`, `cdq`/`and edx,0x3F` fixup, `and eax,~0x3F` at `0032E43F`–`0032E448`).
Negative/zero sizes pass through unrounded.
