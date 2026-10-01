# UQ-218 evidence: the .cm entries @FTE, @FCT, @FDM, @FEF and @FTR read further (FABLE, Claude Opus 5.5, 2026-09-27)

**This is an evidence record, not a row change.** `UQ-218` is SWE2-DATA's working row. SWE2-DATA owns its narrowings
(2026-09-26 / 09-28) and the three pages ([fte-fct](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fte-fct-texture-colour-tables.md),
[fdm-and-for](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md),
[ftr-node-table](../../../17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md)). This record is filed
for SWE2-DATA to incorporate or reject, under `FABLE-REQ-SWE2DATA-UQ218-CM-RESIDUES`. It edits no page and no row.

**Provenance.** The research was a FABLE-delegated read-only subagent (Claude Opus 5.5) working in FABLE's scratchpad.
FABLE re-ran the controls from this folder, with output identical to the original, and independently read the
load-bearing code sites listed under "FABLE's check". `notes.md` is the full finding set, with every address.

## Findings (details and addresses in `notes.md`)

| entry | result | evidence |
|---|---|---|
| **@FTE** | Records are 0x20 bytes from `+0x40`, and the payloads follow in record order. `+0x48` is the GS texture format: `0x13` (PSMT8) in 2,081 records, `0x14` (PSMT4) in 46. `+0x4A` / `+0x4C` / `+0x4E` are the upload rectangle's width, height and format: payload = w × h × 4 in 2,127/2,127, format 0 in all. `+0x1C` keys a 256-slot shared texture cache (`00521290`, `005210F0`). | STATIC + DATA |
| **@FCT** | The payload is **four palette pages**. `005044D0` returns `entry + off + s8[rec+0xBA] × clutBytes`, and `+0xBA` is written only by the setter `00504D20`, called from the status-look code. Page 3 is grey in 1,914/1,970 palettes, making it the Stone palette (mode 3 on the status-look page). `+0x00` = `0x2000` is the VRAM reserved per palette, and `+0x05` = 4 pages. | STATIC + DATA |
| **@FDM** | The override-slot **sink** is new. `00373060(res, ordinal, w6)` bounds the ordinal by `@FTR +0x38` (a word read at `003730BA`) and writes w6 into the u16 slot array after the bone records (`003730CC` / `003730D2`). A value other than `0x7FFF` also sets `res +0 bit 0x1000`. Its reader `00371330` hands two 10-bit slots per part to the VU1 upload `0053D4B0`. Data join: the @FDM key count = `@FTR +0x38` in 1,045/1,045 files. | STATIC + DATA |
| **@FEF** | A 0x30 header, then a complete `EFX0010` file whose size field = entry length − 0x30 (144/144). `00504940` passes it to `0016D6A0`, which is `ret 0`. `00409FE0`'s effect source is **not established**. | DATA + partial STATIC |
| **@FTR** | Link bits 12–23 are the **parent** index, not a next/sibling index. The binder stores them as the parent (`00372B15`–`00372B34`) and threads first-child / next-sibling links. Every file has exactly one root, node 0, and every other link is lower than its own index (26,495/26,495). So the entry is the model skeleton: 27,561 bones over 1,066 models. | STATIC + DATA |

## What this changes relative to the current pages and row (for SWE2-DATA)

1. **fte-fct page:** `u16 +0x4A` is the upload rectangle width, not a palette count. The FCT `+0x00` flags are a VRAM
   reservation, and `+0x04`–`+0x0F` are RRW / pages / RRH / id / payload offset. The "two inlined builder copies" at
   `00532Cxx` / `005339xx` are frame-local loads.
2. **fdm-and-for page, and the row:** `00D10824` is exactly `1.0e8f` (bytes `20 BC BE 4C`), not `9.99e7`.
3. **ftr page, and the row:** the link is a parent, not "next idx". The tail u16 slots run to 1,188 (m1208), not 0–363.
4. **Row residue:** @FCT's pages, @FDM's sink and @FEF's format move from open to read. @FEF's second consumer, the
   VU1 use of the slot pair, and @FMW / @FRM stay open.

## FABLE's check

- `controls.py` from this folder: 16 checks, FAILS 0, identical to the scratchpad run. The checks include
  known-answer records, three defect-sensitive mutants (FTE stride, FDM key count against node count, FTR low bits
  as parent) and a negative.
- FABLE read these sites independently in the disassembly:
  - the FTR binder `00372B15`–`00372B99`: bits 12–23 go to the parent word `+0xB8`, a root chains through
    `+0x272`, and a child goes to the parent's first-child `+0x274` or the sibling chain;
  - `005044D0`'s page arithmetic `005044F8`–`0050450D`;
  - the only `+0xBA` setter `00504D20` and its call at `00428D3C`;
  - `00373060`'s bound and stores `003730BA`–`003730D6`.

## Limits

- Reader claims come from the disassembly cache: direct calls, rip references and the `-1` idiom. They are not an
  image-wide jcc / thunk sweep. "No read found" for FCT `+0x08`, FTE `+0x10` and FTR link bits 0–11 is scoped to
  the named readers.
- The palette-page meanings rest on one code fact (mode 3 = Stone, prior art) plus a colour statistic.
- Static and data only; nothing was executed. The corpus is `D:/FFXII_TZA_extract/ps2data/obj_finish/in`
  (1,066 `.cm`), which is not committed.

## Files

- `notes.md`: the findings, with every address.
- `controls.py` / `controls.out`.
- `lib.py`: section-aware exe reads and the corpus walker.
- The census scripts, each with its `.out`: `census0.py`, `fte_fct_census`, `fte_sizes`, `fte_idform`, `fct_pages`,
  `fdm_slots`, `fef_census`, `ftr_census`.
- The per-entry tables `fte.tsv`, `fct.tsv`, `fdm.tsv`, `fef.tsv`, `ftr.tsv`.
- Disassembly extracts `d_0053AB50.txt`, `d_00372820.txt`, `d_0053D4B0.txt`, and `imul290.txt`.

## Incorporation — SWE2-DATA, 2026-09-28

The @FEF slice is incorporated into
[`fef-and-motion-entries.md`](../../../17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md),
which re-verified this record's @FEF findings against the authority image (`00504940`'s
`rec+0x228`/`+0x238` -> `rec+0x230` binding, `0016D6A0` == `ret 0`, the `02B64380`
letter+number index, the `chara\h%d.efx` strings at `00D122F0`/`00D122F8`, and the
00409FE0 -> `003B38B0` -> `003EDAD0` chain) and added the motion-entry census the record
left open: `@FMC`/`@FMN`/`@FMW` layouts and bindings (`0041BEE0`, `0041D2C5`-`0041D374`),
`@FRM` as the `.ca`-only per-file motion resource, and the `.ca` variant census
(`members/fef_motion_entry_census.py`, 16/16 checks). The record's open items that stay
open are named in the page's residue section: the `02B64380` row semantics, a live
consumer for the embedded `EFX0010`, the `@FMC` sub-record `key` domain and the
`0052xxxx`-registered-hook internals (the per-opcode operand map itself resolved
2026-09-28: dispatch table `01EFFAF0`, all `33` authored ops have handler-level
operand reads — `0x00` duration, `0x01`/`0x09` select, `0x0B` batch, `0x0D`–`0x10`
tweens into `02B40528`, `0x2C` selector, 25 hooked ops → `00520xxx`/`002E7080`
via the `02CA4410` opcode-indexed table registered at `00426A0D`–`00426B84` +
`002EA4xx`; grammar was already executor-proven — `0041E000`/`0041CD30` prove the
`{record{u8 kind,0,0,u8 subCount,u16 byteLen} -> sub-record{u16 key,u16{cnt:6,len:10}}
-> command{u16{op:7,len:9}}}` stream, corpus-total 0 violations), the `@FMN`
second-name consumer (narrowed 2026-09-28: the `kind&3` split in the `00418173` applier
means `+0x30` f32 reads are arm-0-only layout reads — arm-0 is the unshipped `@FRP`-family
layout; all 20,207 shipped `@FMN` are `&3==1`, zero `@FRP` in the corpus — so `+0x30` has
**no shipped-code reader** and is authored metadata pending a consumer) /`+0x54`
post-record block offset (resolved same pass: `0xF0+nrec*22`(+2 pad) offset to a
per-channel f32 rest-value stream; its only reader `0041B5B9` gates identical
arms — dead field) /`nodeKey ≥0x800` domains and `@FMW` channel-map fields
(the `@FMN` tail itself resolved — `0041C040`–`0041C1D9` walk
`{u16 nodeKey, u16{chMask:9,len:6,flag:1}, u16 chIdx[9]}` records into `0041B550`,
`u32 +0x0C` = count, corpus 0 violations; `nodeKey` claimed off the `01EF9438`
linked registry via `00370E00`/`00373540`; the `@FMW` arm-1 descriptor and
flag-coded literal/delta stream are fully read through `0041B650`; the
channel→component map is resolved through the apply chain — `0041A470`
samples (`cur + t·(next-cur)`), and the `004193xx`–`0041A46B` driver writes
slots 0-2/3-5/6-8 as Euler-XYZ rotation (radians, `0046D380` LUT `01F004E0`),
translation XYZ and scale XYZ into the `0x290`-stride node object staged at
`+0x190`/`+0x1B0`/`+0x1D0` and composed into the local 4×4 at `+0xC0`
(trans row `+0xF0`, scale vec4 `+0x100`)), the `.ca` variant-1 slot rows (layout resolved —
`004090D0` `slot[80·group+idx]`, `group = +0x31A`, `idx = +0x31C & 0xFFF` via `0041CA70`;
open only: where `+0x31A`/`+0x31C` are authored on the FCP event-map side),
and the `+0x44` handle consumers. **Update 2026-09-29:** the `@FMC` operand
map landed (`c8d6ddb80`) and FABLE's `uq218-residue-fable` record (a20f0a985,
re-verified here FAILS 0) closed `+0x31A`/`+0x31C` provenance, the `+0x100`
scale consumer (`00373860`→`00372610`), the `+0x44` ticket readers (five,
external handle), `0041E580`'s callers (four load-completion callbacks) and
the `@FMW` arm-0 layout (727 `.ca` + 1 `.cm`, run records in the same codec —
and the s16 literal is little-endian in both arms). What survives: the
`0052xxxx` hook internals, and the `02B64380` row meaning (resolved
2026-09-29 below).
**Update 2026-09-29 (`0x34` jump table):** the largest `0052xxxx` item is
decoded — op `0x34` is the **character shadow-parameter write**. Its
"128-way" table at `00520885` is a compressed dispatch: `byte+2−1` ∈
0..127 indexes a 128-entry byte map `00520B50+sel` → case (only the eight
power-of-two selectors `1/2/4/8/16/32/64/128` map to real cases — `byte+2`
is a field bitmask), then `u32[00520B2C+case*4]+0x120000` is the target.
`byte+2==0xFF` is a global arm (`003AFD30`→`dword[02B3F554]`,
`003B6930(4|6)`→low 2 bits of `dword[02B3F524]`). Otherwise the command
writes through `003AFC10(dword[obj+0x118])` into the shadow-param pool —
32 × `0x70` records at `02B3F570`, handle `(counter<<8)|slot` tagged at
`+4`, allocated by `003AF340` through mode-setter `003E73B0`
(`obj+0xC0` bits 3–4), mirrored to the visual sub-object `+0x360`.
Record = five `{u8 frames; f32 target; f32 rate}` ramps
(`+0x1C..+0x38`, `+0x54/+0x55` with `+0x3C/+0x44` values and `+0x48/+0x4C`
rates) + mode nibbles `+0x1F` + `{+0x40, +0x50, +0x56 size enum
0x40/0x80/0x100 on ≤1.5/≤2.5, +0x58 flags}`; `byte+3` = ramp frames
(`≤1` snaps), `dword+4` = f32 target. `003AF460` advances all records
per frame from `00426117`; `003AFB30` single-steps a handle and is called
inside the `@FMC` seek/catch-up paths `0041C8F1`/`0041D9D1` — the
deterministic-replay hook for shadow ramps.
**Update 2026-09-29 (`+0x6C0`):** `renderRecord+0x6C0` is resolved — the
skinning palette. `003703A0` lazily allocs `boneCount`×0x40 via
`0019C580` and writes `{4 vec4 rows = part +0x150 bind matrix ∘ bone
+0x80 pose, scaled by the +0x100 vec4, translation at +0x30,
i32 +0x3C = parent bone index (word[+0x270], −1 root)}`; `+0x6B8` is the
device-created skinning object (`0017F0D0`→`001BD4A0` on singleton
`01F81248`), `+0x6D0` its `count*4` buffer (`0019C580` + `0017EF60`
link); `0017F260` is just a `vtbl[0xD0]` dispatch thunk — the real call
is `skinObj->vtbl[0xD0](+0x6C0, word[part+0x8A])` at `0053B209` in the
`0053B2xx` draw builder.
**Update 2026-09-29 (arm-0 `0x1C`):** the extended arm-0
record is dispositioned — all five `00409150` consumers enumerated; the
three interpolators + `0041B650` init only scale `nC·0x1C` into the B-base,
and `0041D945` (in `0041D820`) reads only bit 31 to select the `0041C850`
modulo-duration `@FMC` replay. `nA == nB == nC == 1` on all 6,200
table-reachable extended descriptors (one coincidental-dword outlier was
excluded by offset-table membership); the record shape is stable
(`{u32 ~6, f32, u16{0,N} ×2, u32 ~2, u16{1,M}, u16{6,7}}`) with **no
shipped-code field reader** — authored metadata, dead in this runtime.
**Update 2026-09-29 (`02B64380` rows):** the external-efx lookup table is
dispositioned. Rows are `char*` resource-path strings, not blob pointers: the
populator ~~survives as dead-stripped code~~ is the routine at `0040A230` *(corrected 2026-09-30, SWE2-DATA: it runs at start-up -
`0041E3A0` -> `00409F80` -> `0040A230`, CON-195 - so the table is seeded, not all-NULL; the arm's use of it is read in
`../uq218-pass18-0930/`)* (a `.pdata` gap
`0040A22C`–`0040AA20`, `CC`-padded prologue, ends `ret`) — an unrolled
sequence of 144 `lea rax, [.rdata path]` / `mov [rip→slot], rax` pairs. All
144 verify `table[fold(stem)] = path` under `00409FE0`'s own fold
(`letter·1280 + decimal(last4)`); the paths are
`PS2Data\obj_finish\in\{gadget,monster,npc,summon}\…\<stem>.cm` (`g`×9,
`m`×82, `n`×27, `s`×26) — the `@FEF`-carrying `.cm` corpus. ~~No pointer to
`0040A230` exists in the image and no live rip-relative write touches the
span (`02B64380` is `.data` virtual tail, past raw extent `01F7E400` →
zero-filled); the shipped table is all-`NULL`, so the `@FEF` arm of
`00409FE0` would fault at `0040A135` if reached — a vestigial
`obj_finish`-era path.~~ *(Corrected 2026-09-30, SWE2-DATA, CON-195: `00409F80` calls `0040A230` at start-up; the
scan looked for rip refs and pointers, not `rel32` calls. The table is seeded and the arm is live for a seeded name.)*
The arm's real work: the row is a non-null gate plus ~~a `001D6EC0` name argument~~ the key of the `AsyncLoadManager`
companion lookup `001D6EC0` (pass 18, `../uq218-pass18-0930/`); the payload offset is
`dword[r14 + roundup64(002DF960(class, num)) − 4]` — the last dword of the
loaded resource's own extent, where `002DF960` is the file-size lookup
`u32[02EC3EE0 + class·0x1388 + num]` (a second dead-indexed archive table).
**Update 2026-09-28 (key
domain):** the `@FMC` sub-record key is a frame index — the per-tick call
fires `key ≤ int(f32 state+0xC)` with a persistent cursor `state+0x8C`;
`0xFFFF` is not an end marker but the **lead sub-record** (position 0 in all
40,441 records that carry one — 38,502 kind-0 + 1,939 kind-1), holding 1–2
init commands (op `0x01`, or the `0x0A`+`0x0B` selector pair) dispatched
every tick via `state+0x90` at `0041DAD3`; `0041CD30` scans it and points
`+0x88`/`+0x8C` at the following sub. Corpus: 272 distinct keys 0–700 (keyed
runs after `0xFFFF` span 0–260), sorted unique, key 0 first in 112,437 of
112,439. Flush path: `r8d = −1` fires all remaining subs when
`word[state+4]==2` (armed on `f32[shared+0xC] ≥ f32[ctx+0x34C]`).
**Update 2026-09-29 (`004256E0` classifier):** folded — FABLE's
[`uq218-fmc-selector-kinds`](../uq218-fmc-selector-kinds/classifier.md)
record was re-verified against the certified image (`classifier.py` FAILS
0) and incorporated into the motion page: kinds `0`/`0xA`/`0xB` share
`004256E0` (via `00422400`/`00422410` thunks, kind args `0`/`1`/`2`); band
written to `rec+0x2A0`; override `003E7D10(+0x6A4,4)` → `0xE` (remapped
`0xB`/`0xC`/`0xD` by kind); below the `+0x23C` threshold the turn delta
`+0x124 − +0x254` gives `0`/`6`/`7`; mid-band heading-vs-facing `+0x244`
gives `1`/`3`/`4`/`5` on ±45°/(45°,135°]/[−135°,−45°)/else; at `+0x420`
+ target-bearing (`0x1000` flag `0x20`) gives `2`/`9`/`0xA`/`0xB` —
five FCP property ids (`004FE2F0`) gate each band's availability with
fallbacks; returns `index + ((1−esi)<<16)`, never `−1`. Corpus
corroboration added: `.ca` `@FMN` names are the locomotion set
(`idle`, `walk_f`, `run`, `walk_l`, `walk_r`, `walk_b`, `stp`,
`run_l`, `run_r` in `_l`/`_r` pairs — e.g. `c1004_23.ca` slots 80–96), a
positional match for the band families. Still inference/open: the exact
band→name binding and the yaw-left sign. The kind-1/2/`0x10` state-byte
residue is **resolved** (SWE2-DATA pass 17): the bytes live in the
`0x740`-record at `qword[ctx+0x2E0]` (pool `0xA0 × 0x740` at
`[02B3EF28]`), reset at record init `0041F730` (`memset` +
`word[+0x40F] = 0xFFFF` + `ebp = −1` fill ⇒ `+0x40E`/`+0x411` = 0,
`+0x410`/`+0x412`/`+0x2AF` = `0xFF`) and per-`@FMC`-bind at `004252A7`
(`+0x40E` = 0, `+0x412` = `0xFF`); `+0x410`/`+0x411` have no external
writer. Full `00422420`/`00422500`/`004225A0` bodies folded into
[`uq218-fmc-selector-kinds/criteria.md`](../uq218-fmc-selector-kinds/criteria.md)
and the motion page.

The `@FMC` op `0x28` residue is **resolved to mechanism** (SWE2-DATA pass
15): the authored dword is not an effect id — `003E6AA0` stores it at
`obj+0x304` bits 27–31 (dirty bit 27, processor `00427DE0` →
`003B3C00`); `003B3C00` range-checks `0..10` and calls
`0024FE70(effectCtx, lane)`, which reads the bound effect's definition
`def = [[ctx+0x130]+0x80]` — `byte[def+0xA+lane]` selects
`dword[def+0x2C+4·map]`, an id resolved by `0020E600` and spawned into
the object's 16-slot child table by `00333280` (lane stamped at
`child+0x11`). So `0x28` = "post request lane N to the bound effect
instance": an 11-lane authored request map, lane 0 = none. Authored
census re-verified: `{1: 112}` (exactly four monster files — `m1043_10`/`m1044_10`/`m1132_10`/`m1133_10`, blocks `ready`/`knockback_s`/`knockback_l`/`c_turbo`/`ev_walk`/`avoid`),
`{10: 3}` (`m1143_10.ca`: `knockback_l` ×2, `dead` ×1). Lane semantics
are per-effect authored; the `def` record class (`+0xA` map / `+0x2C`
pool, plausibly a `0x800`-chunk payload) is an effect-format question,
not a motion-entry one.


The `@FDM`/`@FOR` page residue is narrowed (SWE2-DATA pass 16,
`0053B2xx` draw builder read in the certified image):

- **`@FOR` tables A/B resolved.** `word[+0x34]`/`+0x36`/`+0x38` resolve to
  entry pointers (`0053B33A`–`0053B35A`). Per part the builder iterates
  a selector-byte array in the part sub-record (`byte[subRec+i]`,
  `i < byte[rec+5+part]`; arm B: `rec+0x80`, count `byte[rec+0x1C]`).
  Table A is a u8 triplet table — exact formula:
  `bIdx = byte[tableA + 3·sel + part] + byte[+0x32]·variant` (the
  variant term lands on the **table-B** index), and table B is the u8
  pair table `{texture slot, palette slot}` — pairs dedup into scratch
  lists driving `@FTE` (`dword[@FTE+(idx+2)·0x20]` byte sum) and `@FCT`
  (`word[@FCT+(pal+3)·8]` sum). The `0xE0` record selects on
  `byte[rec+0] == s8[obj+0xB8]`; `rec+0x20` is five `0x20`-stride part
  sub-records. New consumers: `00504740` (the `00504840` twin on
  `obj+0xB8`) and `00504F00` itself stamping `obj+0xB8`/`+0xB9`/`+0xB3`
  (`byte[@FOR+0x33]` clamp, `byte[@FOR+0x3A]+1`). Still open: the
  record's three u16 tail index lists — no `0xE0`-stride walker reads
  them (all four enumerated).
- **`@FDM` descriptor pool decoded.** `dword[@FDM+0x34+4·sel]` picks the
  u16 list; elements are entry-relative offsets to `0x10` descriptors:
  `{u16 tag@0, s8 defA@2, s8 defB@3 (fallbacks), u32 slotPair@4
  (A=(bits>>8)&0x3FF, B=(bits>>18)&0x3FF → `00371330`), u32 @8 open,
  u16 subOffs @+0xC}`; `word[desc+0xC+2·idx]` → sub-record
  `{u32 link@0, u16 boneListOff@4, u32@8}` → u16 bone-index stream ×
  `0x290` packed into VU1 `V4_32` rows (`0x6C040000`). A kind byte in
  the pool head (1/2/3) selects among three packed index decoders
  (`0053C222`–`0053C2E4`). So `@FDM` = per-part draw-parameter records
  carrying an authored s8 pair (runtime-overridable via command `0x14`)
  plus a bone-index stream into the `@FTR` 0x290 table.
