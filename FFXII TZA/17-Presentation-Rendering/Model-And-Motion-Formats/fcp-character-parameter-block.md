---
system: The @FCP character parameter block inside every .cm container
category: 17-Presentation-Rendering
status: DOCUMENTED — every register row is closed or dispositioned and the page's residue is answered (owner re-status 2026-10-01, OPUS, on SWE2-STRUCT's batch 12 and residue record) — what each slot means (UQ-217) is SUPERSEDED as a duplicate of FW-1, answered 2026-09-26 (every cached tunable has a reader; the unaddressed slots have none in the image); the other @Fx entries (UQ-218) answered 2026-09-30 (SWE2-DATA pass 18); the payload sections (UQ-220) answered 2026-09-26 (section 2 is the rig, 3 the attachment table, 6 dead, 18 and 21-24 absent); the one-slot-behind default table (UQ-219) and the section-1 pairs (UQ-221) answered 2026-09-18; the readers of the section-8 runtime copy answered 2026-09-30 (swe2struct-residue3-0930 P1-P9: a per-frame update, a draw, on/off, a LOD scale and a hide/freeze merge, reached only through the four +0x300 accessors)
owner_layer: both
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
corpus_validated: "1,066 / 1,066 .cm entries (the @FCP entry of each, sections 1 and 9 read where present) and 3,164 / 3,164 .ca entries (entry tags only), read from FFXII_TZA.vbf 2026-09-11"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-fcp-character-parameter-block-pass-2
  crossref_clean: false
  reopened_count: 0
---

# The `@FCP` character parameter block — the first entry of every `.cm`

> **Every character, monster, NPC, gadget and weapon model container opens with a tagged block of
> authored floats, and the battle engine reads twelve of them into the battle unit at spawn.** The
> block is found by tag and name, read through property ids that carry a section number, a
> minimum version and *two* slot numbers — one for the file, one for a built-in default table —
> and falls back to that table when a section is absent, which it is for every weapon.

**Corpus validation, before anything else.**

| | |
|---|---|
| files examined | **1,066 of 1,066 `.cm`** — the `@FCP` entry of each, sections 1 and 9 decoded; **3,164 of 3,164 `.ca`** — entry tags only |
| `@FCP` present | **1,066 / 1,066 `.cm`, always entry 0**; 0 / 3,164 `.ca` |
| entry name equals the container name | **1,066 / 1,066** |
| payload version byte `+0x32` | `0x0A` in **1,066 / 1,066** |
| section 1 present | **1,066 / 1,066** |
| section 9 (the battle tunables) present | **723 / 1,066** — every `monster` (254), `npc` (174), `high` (132), `gadget` (103), `summon` (26), `chara` (17) and `treasure` (17); **absent in all 326 `weapon` and 17 `bg_obj`** |
| `@FCP` entry size | 976 B – 42,960 B, 255 distinct; 1,072 B commonest (178), 1,376 B next (87) |

The container — `@FRP` header, `variant`, `contentLength`, offset table — is
[the `@FRP` object container](frp-object-container.md); this sheet starts where that one stops,
at the first entry.

---

## 1. What the player sees

How close a character walks up to what it is going to hit, how wide a body counts as for the AI's
crowding test, how fast a facing turns, how tall the renderer takes a model to be when it fades
and culls it, and how big a monster's collision extent is relative to a human's — the numbers
behind those are authored per model in this block, not in the enemy or party tables. A monster's
file carries a second set of radii roughly twice the party's (`0.1333 / 0.2667 / 0.4` beside
`0.0667 / 0.1333 / 0.2` in the files opened), and the engine selects that set for a unit built from
the enemy table whose definition byte `+0x13` is not `0xFF`. Weapons have no section 9 at all; for
them every one of these reads returns the engine's built-in default.

## 2. The layout

The `.cm` container's entry 0 is a section with the `0x30`-byte header the container's finder
walks; its payload begins `0x30` bytes in. Offsets below are **payload-relative** unless the fence
says otherwise.

```struct FcpSectionHeader base=section size=0x30
+0x00  char[4]   tag            '@FCP' -- 1,066 / 1,066 .cm
+0x04  u32       _w04           0 in 1,066 / 1,066 (other tags carry other values)
+0x08  u32       size           bytes from the header start to the entry's end
+0x0C  u32       _w0C           1 in 1,066 / 1,066
+0x10  char[32]  name           NUL-padded; equals the container name in 1,066 / 1,066
```

```struct FcpPayloadHeader base=payload size=0x40
+0x00  u16[18]   sectionOffset  payload-relative offset of section n, 0 = absent; [0] is 4 or 260 -- see below;
                                *[17] is 0 in all 1,066 (2026-09-21)*
+0x24  u32       ftrTailLen    bytes memcpy'd from `sectionOffset[2]` into the @FTR tail (2026-09-21 -- the last section);
                                *was misread as `sectionOffset[18]`/`[19]` — they are one dword, not two offsets*
+0x28  u16       _zero28       0 in 1,066 / 1,066
+0x2A  u16       _perFileValue  NOT an offset -- 924 distinct values, outside the payload in 988 (2026-09-13)
+0x2C  u8[6]     eventMap       the six-byte event map read by 0041E5B0 -- see below
+0x32  u8        version        0x0A in 1,066 / 1,066; every property id carries a minimum version compared against it
+0x33  u8        _pad33         0 in 1,066 / 1,066
+0x34  u16       _ffff34        0xFFFF in 1,066 / 1,066
+0x36  u16       _w36           2 in 993, 3 in 54, 14 in 19
+0x38  u16       _w38           0 in 723; 1-22 in the rest
+0x3A  u16       _w3A           1 in 628, 0xFFFF in 426, other small values in 12
+0x3C  u16       _w3C           0xFFFF in 762, 1 in 301, three other values
+0x3E  u16       _w3E           0 in 1,066 / 1,066
```

The property getters index `sectionOffset` with a **five-bit** section number (`id >> 24 & 0x1F`),
so sections 19–31 alias the words that follow the offsets the corpus actually uses; **no shipped id addresses any section but 1 and 9** (FW-2, 2026-09-13).
**Entries 22–24 (`+0x2C`–`+0x31`) are not offsets but a six-byte event map** read by `0041E5B0`:
each byte is `0x80 | (eventId & 0x7F)` for an entry the record may select, `0x7F` ends the list, and
a byte without the high bit matches only when the record's animation-set state is non-zero
(`0041E5D1`–`0041E649`, added 2026-09-11). The corpus holds four patterns: all zero (723 files —
every character, monster, NPC, gadget, summon, `high` and `bg_obj`), `7F 7F 7F 7F 7F 7F` (297
weapons and one treasure), `3D 36 35 01 81 7F` (29 weapons) and `08 01 05 00 7F 7F` (16 treasures).
`sectionOffset[0]` is `4` in 939 files and `260` in 127 — a section whose "offset" lands inside the
table itself, so section 0 is not a data section and no shipped id addresses it.

**Sections seen**, in the file order of `c1054` (a party member): `1` (`+0x40`), `2` (`+0x1D0`),
`3` (`+0x2BE0`), `6`, `7`, `9` (`+0x30E0`). *(`21` was listed here until
2026-09-13; payload `+0x2A` is not a section offset — see the falsification pass. `18` was listed
here until 2026-09-21; `+0x24` is the u32 `@FTR`-tail copy length, not an offset — see the last
section.)* Six presence patterns
cover 997 of the 1,066 files. The two sections the engine's static readers address:

```struct FcpSection1 base=section1 size=0x190
+0x00  f32[100]  slot           authored floats; slots 67, 68, 79 and 80 are read by the engine (section 3)
```

*Corrected 2026-09-18 (FABLE): the last 64 bytes of section 1 (`+0x14C`..`+0x18B`, float slots 83–98) are not floats but a `u16[32]` table of bone indices, indexed by special-bone ids 0–31 through `003E5AD0(record, id)` (`section1 + 0x14C + id × 2`, `003E5AEF`). Across all 1,066 blocks ids 0–25 hold `0xFFFF` or a bone index (id 4 and 5 are 1 in 482, id 25 is 1 in 193, id 0 is `0xFFFF` in 627), and ids 26–31 are `0xFFFF` everywhere — which is what §5's “non-numeric bit patterns” in slots 87–98 were.*

```struct FcpSection9 base=section9 size=0x180
+0x00  f32[49]   slot           authored floats; slots 0-9, 30, 32-36, 38-41, 43, 45-48 are read (section 3)   <- corrected 2026-10-02, OPUS - slots 10, 14-25 and 31 are read too: 01EED320 indices 11, 12-23 and 33 hold 09000A0A, 09000E0F..09001819 and 09001E1F; slots 40 and 41 are read as dwords (29010128, 29010229)
+0xC4  u32       slot49         an integer: 60 in 420 files, -1 in 173, 15 / 30 / 120 in the rest
+0xC8  f32[46]   slot50plus     slot 50 is read (an angle: 0.7854 in 426, 0 in 173, 1.5708 in 39, 6.2832 in 25); 57-67 are -1.0 and 68-95 zero in the files opened
```

Section 9 spans 384 bytes wherever a higher section follows it (610 files). *(A warning stood here
until 2026-09-13 that in five files — `c1030`, `g0031`, `g0032`, `hc1006_01`, `hc1006_02` — "section 21
begins 13–339 bytes after section 9 starts, so a read of a high slot there returns section 21's
bytes". **There is no section 21**: those five are files where `+0x2A`'s per-file value happened to
land just past section 9's start. Nothing truncates section 9 in them.)* The first 48 slots of the
three files opened, beside the engine's default table at `01F265B0` (indexed by the id's *other*
slot byte — section 3):

| slot | default table | `c1054` (party) | `c1011` (party) | `m1002` (monster) |
|---:|---:|---:|---:|---:|
| 0 | 0.0667 | 0.0667 | 0.0667 | 0.0667 |
| 1 | 0.1333 | 0.1333 | 0.1 | 0.1333 |
| 2 | 0.2 | 0.2 | 0.1667 | 0.2 |
| 3 | 0.1047 | 0.1047 | 0.1571 | 0.0262 |
| 4 | 0.1047 | 0.1047 | 0.2094 | 0.0931 |
| 5 | 0 | 0 | 0 | 0 |
| 6 | 0.0667 | 0.0667 | 0.0447 | 0.1333 |
| 7 | 0.1333 | 0.1333 | 0.1077 | 0.2667 |
| 8 | 0.2 | 0.2 | 0.1707 | 0.4 |
| 9 | 0.1047 | 0.1047 | 0.1571 | 0.1047 |
| 10 | 0.1047 | 0.448 | 0.448 | 0.448 |
| 11, 12, 13 | 0.0111, 0.0111, 1.0 | 0, 0.0111, 0.0111 | 0, 0.0111, 0.0074 | 0, 0.0111, 0.0222 |
| 14–28 | 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0 | 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1 | 1, 0.01, 1, 0.01, 0, 2.5, 1, 0.01, 1, 0.4, 1, 0.4, 1, 0, 1 | 0.02, 1.3, 2, 0, 0, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2 |
| 29, 30, 31, 32 | 1.7, 60, 0.5, 0.77 | 0, 1.7, 60, 0.5 | 0, 1.85, 200, 0.7 | 0, 4.4, 25, 0.5 |
| 33–37 | 0.5, 0.5, 0.75, 0.75, 1.0 | 0.67, 0.75, 0.75, 1, 1 | 0.9, 0.75, 0.75, 1, 1 | 0.67, 0.75, 0.75, 1, 1 |
| 38–44 | 1.0, 0.1047, 0.7854, 0.1047, 0.7, 0.0931, 0.7854 | 0.1047, 0.7854, 0, 0, 0.1047, 0, 0 | 0.2094, 0.1745, 0, 0, 0.1833, 0, 0 | 0.1105, 0.3491, 0, 0, 0.0684, 0, 0 |
| 45–47 | −1, −1, −1 | 0, 0.7, 0.0931 | 0, 0.7, 0.0931 | 0, 0.8, 0.0291 |

From slot 11 on the table sits **one slot behind** the files (the table's 29 is the files' 30, and
so on): the files inserted a zero at slot 11. The ids carry both numberings, so nothing is out of
step at run time — see the next section.

## 3. The loader contract

**Finding the block.** `CharacterRenderRecord_RefreshFCPPayloadByRecordId` `002EDBD0` takes a
render-record index, reads the record's model id word `+0x408` (`002EDC14`), resolves it through
`00409F50` → `ResourceTable_ResolveEntryByIndex` `002ED570` from the table at `[record + 0x10] +
0xD90` (`002EDC21`–`002EDC33`), and asks `ResourceEntry_FindSectionPointerByTagAndName` `00409660`
for the entry tagged `'@FCP'` (`0x50434640`, `002EDC3C`) **whose name equals the 32 bytes at record
`+0x3C`** — the record's own model name. The section pointer plus `0x30` is stored at record
`+0x400` (`002EDC49`–`002EDC59`); a missing entry stores 0. Every later read goes through
`CharacterRenderRecord_GetFCPPresentationConfigurationPayload` `003E55F0`, which returns `+0x400`.

**Property ids.** A 32-bit id `SS VV DD FF`: `SS & 0x1F` the section (`004FE2B6`); `VV` the
minimum payload version (`004FE27A`–`004FE287`); `DD` the slot **in the default table**
(`004FE28B`–`004FE29E`, `004FE2C6`–`004FE2D9`); `FF` the slot **in the file** (`004FE2DA`–`004FE2E9`
— the `movzx edx, cl` there sees the unshifted id). The two slot bytes are equal up to slot 10 and
differ by one from slot 11 on, which is the whole story of the table's offset in the previous
section. The top three bits of `SS` select the getter's mode.

| Field | Read by | Rejected if | Clamped to | Inert |
|---|---|---|---|---|
| payload `+0x32` version | `004FE270` (`004FE280`–`004FE287`), `004FE2F0` (`004FE320`–`004FE327`, `004FE386`–`004FE38D`) | `VV > version` → **the default table's slot `DD` is returned instead of the file's slot `FF`** | — | — |
| `sectionOffset[s]` | `004FE270` (`004FE2BB`), `004FE2F0` (`004FE34B`) | `0` → default table | five-bit `s` | — |
| section `s` slot `FF` (float) | `004FE270` (`004FE2DA`–`004FE2E9`) | — | — | — |
| section `s` slot `FF` (dword, ids `0x2xxxxxxx`) | `004FE2F0` (`004FE368`–`004FE372`) | — | — | — |
| payload `+0x12` — which is `sectionOffset[9]` — for the bit-field ids `0x6xxxxxxx` | `004FE2F0` (`004FE38F`–`004FE3B7`): the dword at section 9 + `FF × 4`, shifted right by `8 × (SS & 0x1F)` and masked — so `SS & 0x1F` is the **byte index** 0–3 inside slot `FF`, not a section | `0` → default | — | — |
| payload `+0x01` | `004FE2F0` for the single id `0x40000000` (`004FE2F6`–`004FE302`) | — | — | — |
| ids `≥ 0x20000000` asked as floats | `004FE270` returns **−1.0** (`004FE29F`–`004FE2AF`, `01CEBC9C`) | — | — | — |
| section header `+0x04`, `+0x0C` | — | — | — | **no reader found by the tag scan** (the six `'@FCP'` sites) and the finder |
| `+0x36`–`+0x3E` | `0041EDE0` (`0041EE76`) and `0041F010` (`0041F0B1`) pass `+0x36` as a bone id to `003E5AD0`; `003E5AD0(record, id)` returns `+0x3A` / `+0x3C` / `+0x3E` for ids `0x104` / `0x105` / `0x106` (`003E5B00`..`003E5B1C`); `00421CD0` (`00421CE7`..`00421D07`) and `004221F0` (`0042225D`) read them directly as a first-non-`0xFFFF` chain | — | — | ~~**no reader found** by the same scan~~ **readers found 2026-09-18 (FABLE)** by following the payload getter `003E55F0` into its eleven callers: `+0x36` is a special-bone id (2 / 3 / 14 in 993 / 54 / 19 files) resolved through section 1's bone table, and `+0x3A` / `+0x3C` / `+0x3E` are the three model-declared special bones (`(1, 0xFFFF, 0)` in 625 blocks, `(0xFFFF, 1, 0)` in 301, `(0xFFFF, 0xFFFF, 0)` in 125) that [the render-record page](../../17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md) names *(roles read 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, [record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md) SB1-SB9: the image gives the three ids no name, so they are named by consumer. `0x104` (`+0x3A`) is the body bone: the shadow measures its height from it and anchors on it, lights flagged for it are evaluated at it, and the hit-flinch, Immobilize and Float-bob applies move it. `0x105` (`+0x3C`) is read only as the chain's second link; 284 of the 326 weapons declare it instead of `0x104`. `0x106` (`+0x3E`) is the shadow's second anchor, and it is bone 0, the root, in every block)* |
| `+0x2C`–`+0x31` event map | `0041E5B0(record, state, eventId)` from `004292B0` (`004292D8`–`0042931E`): the index `i` of the matching byte selects animation `[record + 0x2FA] + i` of the model container's own `@FMC` motion entry (`+0x2F8` = the model resource id `+0x408`, `+0x2FA` = its first `@FMC` entry index, both set by `0041FCF0` at `0041FE66`–`0041FE97`) and starts it through `00423B10` (`0042933F`–`0042936E`); no match → the raw event id is the selector into the loaded motion resource at `+0x390` (`00429395`–`004293B5`) | `0x7F` or an empty map → no entry | — | — |

**The default table.** Floats at `01F265B0` and integers at `01F266B0`, indexed by `DD`: what a
missing section, a too-old version or an absent block yields. Every weapon's section-9 reads
return it.

**Scaling.** `003E6150(recordIndex, id)` wraps the float getter for the battle side: after the read
it **multiplies by the render record's scale float `+0x26C`** for the ids `0x9000000`,
`0x9000101`, `0x9000202`, `0x9000505`, `0x9000606`, `0x9000707`, `0x9000808`, `0x9000B0C`,
`0x9000C0D`, `0x9000D0E`, `0x9000E0F`, `0x9000F10`, `0x9001011`, `0x9001112`, `0x9001213`–`0x9001D1E`,
`0x9042A2E`, `0x1002143`, `0x1002244` (`003E61AF`–`003E62E9`) and **divides** for `0x9001E1F`
(`003E62F4`); every other id is returned unscaled. `003E54B0` reads `0x9042A2E` directly and
multiplies by `+0x268 × +0x168 × +0x26C` (`003E54C5`–`003E54EA`).

**The twelve battle-unit tunables.** `FUN_00239E10` (from `BattleUnit_ActivateAppliedDefinitionRuntime` `00233AD0`)
calls `003204D0(actorWork, index, out)` → `003204E0` twelve times (`00239E64`–`00239F5B`); the
index selects an id from the 34-entry table at `01EED320`, the id's mode selects float
(`002ECE50` → `003E6150`) or integer (`002ECE80` → `003E6310` → `004FE2F0`) reading, and a
second jump table (`003205F0`, `00320614`) applies a scale: **multiply by the actor's y-scale**
(`00265240` → `movementState + 0x24`, `00320570`–`0032057A`), divide by it (`00320560`–`0032056A`),
or leave it. `sel` is true for a unit whose stats record is kind 1 and whose definition's `+0x13`
is not `0xFF` (`00239E3D`–`00239E5C`).

| unit field | index (`sel`) | id | section · min-ver · file slot (default slot) | scaled | `c1054` / `m1002` |
|---|---|---|---|---|---|
| `+0x178` | 0 (7) | `0x09000000` (~~`0x09000706`~~ `0x09000606`) | 9 · 0 · 0 (0), or ~~6 (7)~~ 6 (6) *(corrected 2026-10-02, OPUS: `01EED320` index 7)* | × y-scale; `003E6150` × | 0.0667 / 0.1333 |
| `+0x180` → `+0x17C` → `+0x150` | 1 (8) | `0x09000202` (~~`0x09000908`~~ `0x09000808`) | 9 · 0 · 2 (2), or ~~8 (9)~~ 8 (8) *(corrected 2026-10-02, OPUS: `01EED320` index 8)* | × y-scale; `003E6150` × | 0.2 / 0.4 |
| `+0x184` → render record `+0x420` | 2 (9) | ~~`0x09000201` (`0x09000807`)~~ `0x09000101` (`0x09000707`) | ~~9 · 0 · 1 (2), or 7 (8)~~ 9 · 0 · 1 (1), or 7 (7) | × y-scale; `003E6150` ~~leaves it~~ × *(corrected 2026-10-02, OPUS: `01EED320` indices 2 and 9; `003E6150`+0x7D `cmp ebx, 0x9000101` and +0x71 `cmp ebx, 0x9000707` are on its multiply list)* | 0.1333 / 0.2667 |
| `+0x16C` | 3 (10) | ~~`0x09000403` (`0x09000A09`)~~ `0x09000303` (`0x09000909`) | ~~9 · 0 · 3 (4), or 9 (10)~~ 9 · 0 · 3 (3), or 9 (9) *(corrected 2026-10-02, OPUS: `01EED320` indices 3 and 10)* | raw | 0.1047 / 0.1047 |
| `+0x164` | 4 | ~~`0x09000504`~~ `0x09000404` | ~~9 · 0 · 4 (5)~~ 9 · 0 · 4 (4) *(corrected 2026-10-02, OPUS: `01EED320` index 4)* | raw | 0.1047 / 0.0931 |
| `+0x168` | 5 | ~~`0x09052A2F`~~ `0x09052B2F` | ~~9 · 5 · 47 (42)~~ 9 · 5 · 47 (43) *(corrected 2026-10-02, OPUS: `01EED320` index 5)* | raw | 0.0931 / 0.0291 |
| `+0x170` | 25 | `0x09012726` | 9 · 1 · 38 (39) | raw | 0.1047 / 0.1105 |
| `+0x198` | 27 | `0x09012827` | 9 · 1 · 39 (40) | raw | 0.7854 / 0.3491 |
| `+0x1AC` | 32 | ~~`0x09082032`~~ `0x09082C32` | ~~9 · 8 · 50 (32)~~ 9 · 8 · 50 (44) *(corrected 2026-10-02, OPUS: `01EED320` index 32)* | raw | 0.7854 / 0 |
| `+0x1B0` (int) | 31 | ~~`0x29081131`~~ `0x29081031` | 9 · 8 · 49 ~~(17)~~ (16), dword mode *(corrected 2026-10-02, OPUS: `01EED320` index 31)* | — | 0 / −1 (60 in 420 files) |
| `+0x1F0` bit 2 | 24 | `0x29010229` | 9 · 1 · 41 (2), dword mode: set when the dword is non-zero | — | clear / clear (slot 41 is non-zero in 360 of 723 files) |
| `+0x1F5` (byte) | 26 | `0x29010128` | 9 · 1 · 40 (1), dword mode: the low byte | — | 0 / 0 |

**Other engine reads**, by id (file slot first, default slot in brackets):

| id | section · slot | read by | for |
|---|---|---|---|
| `0x9000707` / `0x9000101` | 9 · 7 (7) / 1 (1) | `002E7DD0(actor, which)` — `which == 0` selects slot 7 | a scaled radius pair (party 0.1333 / monster 0.2667 against 0.1333) |
| `0x9000808` / `0x9000202` | 9 · 8 / 2 | `002E7E10(actor, which)` | the pair 0.4 / 0.2 |
| `0x9000606` / `0x9000000` | 9 · 6 / 0 | `002E7E50(actor, which)` | the pair 0.1333 / 0.0667 |
| `0x9000909` | 9 · 9 | `002E9B10` (`002E9B30`) | a scaled angle |
| `0x9001D1E` | 9 · 30 (29) | `002E9630`, `CharacterRenderRecord_UpdateDistanceFadeAndCull` (`0042EBE7`), `0046C6E0` / `0046C8F0` / `0046CC70` (through `004FE270`), `0053AB50` (`0053AF7C`, × record `+0x734`) | a scaled height-like length — 1.7 in 217 files (124 distinct values), 1.85 for `c1011`, 4.4 for `m1002` |
| `0x9000505` | 9 · 5 | `0053AB50` (`0053AFA6`) | — |
| `0x9000606`, `0x9000707`, `0x9001F20`, `0x9002021` | 9 · 6, 7, 32, 33 | `002E28E0` (`002E2CA1`–`002E2E88`), the actor re-apply function that also re-posts facing | — |
| `0x1002143` / `0x1002244`, or `0x1002D4F` / `0x1002E50` when `FieldData_GetActiveFieldRecordBit15` `00377C20` | 1 · 67 / 68, or 79 / 80 | `002E9660` (`002E9681`–`002E968D`), `002E28E0` (`002E2E9D`–`002E2EB8`) | an equal-valued pair with a per-field alternate: (0.5, 0.5) in 288 files and (1.0, 1.0) in 229 for the alternate; `m1002` 1.6 / 3.4 — the actor's default radius pair (width, depth) behind `setradius` / `getdefaultradiusw` / `getdefaultradiusd`, UQ-221 (2026-09-18) |
| `0x9002322`, `0x9002423`, `0x9002524` | 9 · 34, 35, 36 | `0026A490` (`0026A4B8`–`0026A4E6`), each × a constant and truncated to an integer | three counts |
| `0x9042A2E` | 9 · 46 (42) | `003E54B0` | × `+0x268 × +0x168 × +0x26C` |
| `0x63070F30`, `0x62070E30`, `0x61070D30`, `0x60070C30`, `0x63070B2D` | bit-field mode: bytes 3, 2, 1, 0 of section 9's slot 48 and byte 3 of slot 45 | `004256E0` (`00425A28`–`00425BA9`) | four bytes packed in slot 48 |
| `0x2902032B`, `0x6003082D`, `0x62060A2D` | dword 9 · 43; bytes 0 and 2 of slot 45 | `00384E50` (`00384EBC`, `00384F0A`), `003E56E0` | — |

**Version stamp.** `+0x32` is the only stamp; no shipped id's `VV` exceeds `0x08`, so the file
value wins everywhere a section exists. **Nothing normalises the block on load** — `002EDBD0`
stores a pointer and the getters read through it. **No write path**: the block is authored data
inside the model container.

## 4. Key addresses

| Address | Role | Read? |
|---|---|---|
| `002EDBD0` | `CharacterRenderRecord_RefreshFCPPayloadByRecordId` — finds `'@FCP'` by tag and record name, stores the payload at record `+0x400` | ✅ |
| `00409660` | `ResourceEntry_FindSectionPointerByTagAndName` — the container's tag + name lookup ([the addressing page](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md)) | ✅ |
| `003E55F0` | `CharacterRenderRecord_GetFCPPresentationConfigurationPayload` — returns record `+0x400` | ✅ |
| `004FE270` | the float property getter: section · min-version · two slots, defaults at `01F265B0`, −1.0 for non-float ids | ✅ |
| `004FE2F0` | the integer / bit-field property getter, defaults at `01F266B0` | ✅ |
| `003E6150` | float read scaled by the render record's `+0x26C` for the listed ids | ✅ |
| `003E6310` | integer read by record index | ✅ |
| `002ECE50` / `002ECE80` | actor → controller → record index → the two readers | ✅ |
| `003204E0` (`003204D0`) | the battle unit's twelve-tunable reader: index table `01EED320`, y-scale via `00265240` | ✅ |
| `00239E10` | the installer that fills the unit's tunables ([the unit field map](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) §2.6.2) | ✅ |
| `003E54B0`, `002E7DD0`, `002E7E10`, `002E7E50`, `002E9630`, `002E9660`, `002E9B10`, `0026A490` | the small readers of section 3 | ✅ |
| `002E28E0`, `0042E850`, `0046C6E0`, `0046C8F0`, `0046CC70`, `0053AB50`, `004256E0`, `00384E50`, `003E56E0` | larger consumers, read only at their property reads | partly |
| `01EED320` | the 34-entry id table behind the unit's tunables | ✅ |
| `01F265B0` / `01F266B0` | the float / integer default tables | ✅ |

## 5. Corpus survey

**Invariants, 1,066 `.cm`:** `@FCP` is entry 0; its name is the container's; section header
`+0x04 = 0`, `+0x0C = 1`; payload `+0x32 = 0x0A`, `+0x33 = 0`, `+0x34 = 0xFFFF`, `+0x3E = 0`;
section 1 present; `sectionOffset[0] ∈ {4, 260}`; no section offset points outside the entry.

**Entry tag sets** (the whole 4,230-file container corpus): every `.cm` is `@FCP @FTR @FDM @FOR
@FTE @FCT` (855), the same plus `@FEF` (144: 82 monsters, 27 NPCs, 26 summons, 9 gadgets), or the
same plus motion entries `@FMC` / `@FMN` / `@FMW` (29 weapons and 16 treasures); 21 weapons carry only
`@FCP @FTR @FOR` and one `@FCP @FTR @FDM @FOR`. Every variant-0 `.ca` (1,969) is `@FMC @FMN @FMW
@FRM`; every variant-1 `.ca` (1,195) is a table of 81–311 entries (46 distinct counts, 81 in 378
files) most of which carry a **zero tag** — the finder's wildcard — beside `@FRM`, with `@FMC` /
`@FMN` / `@FMW` in 817 of them. So variant 1 is the fixed-slot motion library, which answers the
container page's open question about it at the entry level.

**What varies in section 9.** File slot 2 (the party body radius behind `+0x180`) is `0.2` in 611 of
723 files, `0.1667` in 40, and takes 24 distinct values in all; slots 0–2 are `0.0667 / 0.1333 /
0.2` in 566. Slot 30 (the height-like value behind `0x9001D1E`) takes 124 distinct values, `1.7` in
217. Slot 49, the only integer the battle unit reads, is `60` in 420 files and `−1` in 173.
**Outlier:** 38 monsters (`m1039`, `m1040`, `m1049`, `m1050`, …) carry `3333.3` in slot 1 — the
radius `+0x184` and `002E7DD0` read.

**Section 1.** The pair at slots 67 / 68 is equal-valued in every file opened — `(0.5, 0.5)` in
288 files, `(1.0, 1.0)` in 186, `(0.6, 0.6)` in 125 — and so is the alternate pair at 79 / 80.
Slot 75 and several of slots 87–98 hold non-numeric bit patterns in the three files opened; no shipped id addresses them. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: slots 83–98 are not floats. They are section 1's `u16[32]` special-bone table, which `003E5AD0` indexes (§2, corrected 2026-09-18).)*

## 6. Falsification pass — 2026-09-11

| Attacked | Result |
|---|---|
| Is `'@FCP'` compared, or are the immediates coincidence? | Compared: the four bytes occur in exactly six `.text` sites — `002EDC3D`, `0041FDE9`, `00420589`, `004205C4`, `0042DA71`, `00505011` — every one a `mov edx, 0x50434640` feeding the tag lookup, and once in `.rdata` (`00D122CC`) in the tag list `@FVX … @FCP` that precedes `"unknown format!!"`. |
| Does the same slot byte index the file and the default table? | **No, and the first draft of this sheet said yes.** The default path shifts the id right by eight before taking the low byte (`004FE2C6`–`004FE2D1`); the file path takes the low byte of the unshifted id (`004FE2DA`). Reading `0x9001D1E` as file slot 29 gave `0.0` in every file opened; as slot 30 it gives the 1.7 / 1.85 / 4.4 the default table's slot 29 predicts. |
| Could section 9 be shorter than the slots the ids reach? | Slot 50 is the highest the battle unit addresses; section 9 spans 384 bytes (96 slots) wherever a higher section follows it, and no offset points outside its entry in 1,066 / 1,066. ~~The five files where section 21 starts inside that span are named in section 2.~~ *(corrected 2026-10-02, OPUS: there is no section 21, §2's correction)* |
| Is the y-scale really the multiplier? | `00265240` copies `movementState + 0x20 / +0x24 / +0x28` into three outputs and `003204E0` divides or multiplies by the second (`[rsp + 0x68]`, `00320564`, `00320576`); `002E5FD0` writes the same three from one uniform argument. |
| Positive control for the corpus reader | The reader applies the finder's own rule (offset table at `+0x30` or `+0x40` by `variant`, entries tagged at those offsets) to all 4,230 files, re-derives the container page's invariants (magic, variant, `+0x08` equal to the last entry's end in every variant-0 file) and finds a valid tag at every offset; the three files opened decode to the values `004FE270` would return for the twelve ids. |

## 6.1 Extension 2026-09-11 — the tunable index table, and the four consumers that name slots (FW-1)

`003204E0(actorWork, index, out)` (and `003204D0`, its unit-pointer wrapper) accepts indices 0–33
and maps each through the table at `01EED320` to a property id:

| index | id | section · default · file slot | index | id | section · default · file slot |
|---:|---|---|---:|---|---|
| 0 | `09000000` | 9 · 0 · 0 | 17 | `09001213` | 9 · 18 · 19 |
| 1 | `09000202` | 9 · 2 · 2 | 18 | `09001314` | 9 · 19 · 20 |
| 2 | `09000101` | 9 · 1 · 1 | 19 | `09001415` | 9 · 20 · 21 |
| 3 | `09000303` | 9 · 3 · 3 | 20 | `09001516` | 9 · 21 · 22 |
| 4 | `09000404` | 9 · 4 · 4 | 21 | `09001617` | 9 · 22 · 23 |
| 5 | `09052B2F` | 9 · v5 · 43 · 47 | 22 | `09001718` | 9 · 23 · 24 |
| 6 | `09000505` | 9 · 5 · 5 | 23 | `09001819` | 9 · 24 · 25 |
| 7 | `09000606` | 9 · 6 · 6 | 24 | `29010229` | 9 · v1 · 2 · 41, dword mode |
| 8 | `09000808` | 9 · 8 · 8 | 25 | `09012726` | 9 · v1 · 39 · 38 |
| 9 | `09000707` | 9 · 7 · 7 | 26 | `29010128` | 9 · v1 · 1 · 40, dword mode |
| 10 | `09000909` | 9 · 9 · 9 | 27 | `09012827` | 9 · v1 · 40 · 39 |
| 11 | `09000A0A` | 9 · 10 · 10 | 28 | `40000000` | no section |
| 12 | `09000D0E` | 9 · 13 · 14 | 29 | `01002143` | 1 · 33 · 67 |
| 13 | `09000E0F` | 9 · 14 · 15 | 30 | `01002244` | 1 · 34 · 68 |
| 14 | `09000F10` | 9 · 15 · 16 | 31 | `29081031` | 9 · v8 · 16 · 49, dword mode |
| 15 | `09001011` | 9 · 16 · 17 | 32 | `09082C32` | 9 · v8 · 44 · 50 |
| 16 | `09001112` | 9 · 17 · 18 | 33 | `09001E1F` | 9 · 30 · 31 |

Besides the installer `00239E10`, four functions call the getter, and each names what its slot is
for:

- **Range bands.** `BattleAction_GetAuthoredRangeBandComponent(unit, actionRow, equipmentRow,
  component)` (`00320D70`): when the action row's `+0xC` has bit 26, the band comes from the
  **character's FCP** — index `01EED288[component + 2 × kind]` with `kind` the equipment row's byte
  `+0x25` (0–5, 2 excluded; no equipment → 0): kind 0 → indices 13 / 12 (**file slots 15 / 14**),
  1 → 15 / 14 (17 / 16), 3 → 19 / 18 (21 / 20), 4 → 21 / 20 (23 / 22), 5 → 23 / 22 (25 / 24), with
  a trailing pair 2 / 4 (slots 2 / 4) (`00320DB1`–`00320DD1`); without the bit, the band is the
  action row's own bytes `+2` / `+3` ÷ a constant (`00320DE6`–`00320DF5`). **Section-9 slots 14–25
  are therefore the per-weapon-kind range bands, six kinds × two components.** *(What the bands are for, and how they
  combine with the reach into near / middle / reach, is on
  [how close a unit must stand to act](../../07-Combat-Action/how-close-a-unit-must-stand-to-act.md), 2026-09-19.)*
- **Knockback.** `BattleFormula_ComputeKnockbackImpulseScale` reads index 33 — **slot 31** — for the
  target and divides it by a constant before the kind-mask test (`00385E84`–`00385EBC`).
- **The focus unit's body radius.** `003045A0` reads index 1 — **slot 2**, the body radius the
  render path also uses — for the focus unit, times a constant when state `+0x5AE0` bit 1 is set.
- **An enemy's slot-5 value with variance.** `00236210(unit)` (← `BattleUnit_RefreshActorRuntimeFromDefinition`,
  the installer) reads index 6 — **slot 5** — for an enemy whose definition page byte `+0x18` has
  bits `0x10` / `0x20` and returns it as is when the row's byte `+3` has bit `0x10`, else plus
  `(RNG_SharedGameplayLCG_NextU32() mod 50) ÷ constant` (`0023627E`–`002362EC`).

~~The twelve cached tunables (`+0x164` …) still have no consumer beyond the installer in the access
census; their meanings stay with FW-1.~~ *(Corrected 2026-09-26 (FABLE, Claude Opus 5.5): every one has a consumer. The access
census missed them because the locomotion solvers read them through the solver context: its builder stores
unit + 0x80 at ctx `+0x108`, and the solvers read `[[ctx+0x108] + field − 0x80]`. By consumer they are
the fast-moving turn step (`+0x164`) and the other turn step (`+0x168`), chosen by whether the step length exceeds the threshold `+0x184`; the minimum step length (`+0x178`); the maximum step length, derived from `+0x180` (scaled by 1.0, 1.5 or 1.2 and stored at `+0x17C`); a bound on how far the limited heading may sit from the desired one (`+0x198`); the avoidance manoeuvre's sweep angle (`+0x1AC`) and its chance divisor (`+0x1B0`, `-1` disables it); and a profile index into a speed/heading table (`+0x1F5`). Control: [`fw1_tunable_consumers.py`](../../_index/candidates/fw1-tunable-consumers/fw1_tunable_consumers.py); `FW-1`.)*
## 7. What is not known

- [x] **UQ-217.** **What each slot means.** Section 3 names the slots by consumer; the authoring names are *(closed — the register row is WITHDRAWN.)*
  not in the executable. *Narrowed 2026-09-11 (§6.1):* slots 14–25 are the per-weapon-kind range
  bands, slot 31 the knockback scale, slot 2 the body radius the focus path reads, slot 5 an enemy
  value read with variance; ~~the twelve cached tunables' consumers are still unread~~ *(read 2026-09-26, §6.1)*.
  **FW-1.**
  **Narrowed 2026-09-18 (FABLE), by the same id sweep and archive census as UQ-219:* the slots that can still be given a meaning by a reader are only the addressed ones. **Authored, varying, and addressed by no shipped id:** file slots 12 and 13 (`0.0111` in 642 / 583 of 723, 23 / 39 distinct values), 26 and 28 (`1.0` in 674, 14 distinct, always equal to each other), 42 (`0.1047` in 340, 28 distinct) and 52–54 (6 / 51 / 46 distinct; 53 is `−1.2` in 117 and `0.4` in 111). Constant across the 723 and unaddressed: 11, 27, 29, 44, 51, 55, 56 (`0.0`) and 37 (`1.0`). Whatever those slots meant to the authoring tool, the shipping engine never reads them, so their meaning is not recoverable from the image; the remaining readable residue is the twelve cached tunables' consumers (FW-1).*
- [x] **UQ-218.** **The other entries** — `@FTR`, `@FDM`, `@FOR`, `@FTE`, `@FCT`, `@FEF` and the motion
  entries `@FMC` / `@FMN` / `@FMW` / `@FRM`; their readers are `00504F00` (loads all six),
  `CharacterRenderRecord_SelectLODForViewDepth` `004201F0` (`@FOR`), `0041F340` / `003712E0` / `00372820`
  (`@FTR`), unread here.
  **Narrowed 2026-09-18 (FABLE):* `0041F340(record, modelId, name, flag, base, fcpLen)` finds the `@FTR` entry by the record's model name (`00409660` with tag `0x52544640`, `0041F3A1` / `0041F40B`), sizes it through `00409240` and `003712E0` — `(dword +0xC × 0x149 + word +0x38)` sixteen-bit units, plus the FCP length it is handed (UQ-220) — and is called by the render-record initialiser `0041FCF0` once for the model (`0041FF7C`) and once per further entry (`0041FFDA`, stride `0x30`). The `@FOR`, `@FDM`, `@FTE`, `@FCT`, `@FEF` and motion-entry readers stay unread here.* *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. The answer below covers `@FOR`, `@FDM`, `@FEF` and the motion entries. `@FTE` and `@FCT` are read by the entry binder `00504F00`, the `@FCT` accessor `00504D30` and the draw builder `0053AB50`, on [fte-fct-texture-colour-tables.md](fte-fct-texture-colour-tables.md).)*
  ***ANSWERED 2026-09-30 (SWE2-DATA, pass 18):** the last residues are read - the locomotion band -> `@FMN` binding through op `0x0B` -> `@FMC` record -> op `0x09` (a positive yaw delta is the character's left), the `@FOR` record's tail lists (the per-part draw lists, read by `0053AB50`), the `@FDM` descriptor `+0x08` s8 pair (read by `0053D4B0`, zero in all 12,044 shipped descriptors) and the `@FEF` companion table that appends `chara\hNNNN.efx` to each of the 144 `@FEF` models. [Record](../../_index/candidates/uq218-pass18-0930/README.md); pages [fef-and-motion-entries.md](fef-and-motion-entries.md), [fdm-and-for-entries.md](fdm-and-for-entries.md).*
- [x] **UQ-219.** **Why the default table is one slot behind the files from slot 11**, and whether the two
  slot bytes were ever meant to differ.
  ***ANSWERED 2026-09-18 (FABLE) — the two slot bytes are two numberings by design, and the offset is not one insertion.** `DD` indexes the engine's per-mode default tables (floats `01F265B0` for mode 0, integers `01F266B0` for modes 1 and 3) and `FF` a position in section 9, which the float, dword and bit-field ids share. Read off all 50 ids the image passes (the 40 immediates at the getters' call sites, found again by disassembling every listed caller of `004FE270` / `004FE2F0` / `003E6150` / `003E6310` and the two adapters, plus the 34-entry table `01EED320`; the three computed sites are the table's own adapters and the wrapper's pass-through), the float ids run: file = default for slots 0–10; file = default + 1 for 14–25 and 30–33, because **file slot 11 is a hole** — `0.0` in 723 / 723 blocks that carry a section 9, addressed by no id; file = default − 1 for 34–36, because the default table's 33 and 34 (both `0.5`) are addressed by nothing; and from the version-tagged ids on the two drift apart — v1 file 38 / 39 ↔ default 39 / 40, v4 file 46 ↔ default 42, v5 47 ↔ 43, v8 50 ↔ 44 — because each version's new ids took the *next default index* (39, 40, 42, 43, 44) while their file slots were placed positionally in a section the dword ids were filling too (v1 dwords at 40 / 41, v2 at 43, v3 bit-field dword 45, v7 bit-field 48, v8 dword 49, v10 bit-field 68). So the id carries both bytes because they were never the same thing: an append-ordered default registry against a positional file layout, with the file path reading `FF` and only the fallback reading `DD` (§3). Defaults no shipped id addresses: float 11, 12, 25–28, 33, 34, 38, 41. Static and DATA: the id sweep and a census of every `.cm` in the archive (1,066; 723 with a section 9).*
- [x] **UQ-220.** **Sections 2, 3, 6, 7, 18, 21–24 of the payload** — present, addressed by a handful of ids,
  not decoded.
  **Narrowed 2026-09-18 (FABLE): two scans now bound the readers.* No shipped id addresses sections 2, 3, 6, 7 or 18 (FW-2's call sites, re-swept today as 50 ids by disassembling every listed caller of the four getters), and none of the eleven callers of the payload getter `003E55F0` reads their offsets (`+0x04`, `+0x06`, `+0x0C`, `+0x0E`): followed through callee-saved copies, the direct readers touch only `+0x2C` (the event map), `+0x36`..`+0x3E` (§3, corrected today) and `+0x24`. That last one is `0041FCF0`, which loads the dword at `+0x24` (`sectionOffset[18]`, with the always-zero `[19]` above it; `0041FE40`) and passes it through `0041F340` (`[rsp+0xA8]`, `0041F423` / `0041F544`) to the `@FTR` sizing function `003712E0`, which **adds it as a byte count** to the 16-aligned `@FTR`-derived size `((dword +0xC × 0x149 + word +0x38) × 2 + 15) & ~15` (`003712FE`..`0037131B`). So `sectionOffset[18]` is consumed as a length, never as a section pointer, and what lies at it (present in 1,066 / 1,066 blocks, first four words zero in 707) has no reader. The “handful of ids” above was the pre-FW-2 bucketing. ~~Sections 2, 3, 6 and 7 are authored data the shipping engine's static paths never read, so their meaning is not recoverable from readers; a layout could still be censused from the files, which is the part that stays open.~~ **CORRECTED 2026-09-19 (FABLE) - wrong for section 3, and the scan was scoped wrongly; see "Section 3 is the attachment table" at the end of this page.*** ***SUPERSEDED 2026-09-21 (SWE2-DATA) — every offset word now has an inventoried reader fate, and "section 18" was a misread.** `+0x04` is read by `003E4B40`, whose only callers (`0041FE24`/`0041FE3B` in the initialiser) compute `payload + word[2]` as the source of `memcpy(FTR_tail, src, dword[+0x24])` (`003729B7`) — **section 2 is live**: it is appended verbatim into the `@FTR` allocation, `dword +0x24` its byte length (equal to section 2's size in 528 blocks and to its end offset in 538 — two tool generations; used as a length either way). `+0x0C` is read by `003E5C0E`, which proves section 6 = 16 records of `{u16 key|0xFFFF, u16, u32, f32, f32}` but is **unreferenced dead code**. Section 8 is `memcpy`'d whole at init (`0041F5CE`/`0041F5D9`), record internals partially decoded; section 10's single caller reads only `f32[+8]` ÷ `u8[+0x10]` of its 48 bytes. Sections 5 and 11–17 are authored-only — never present or never read. Remaining open residue: the section-2 slot domain and record semantics, and the FTR-side consumers of the copy (both UQ-218 territory). The whole inventory is in the last section.*
  **ANSWERED 2026-09-26 (FABLE, Claude Opus 5.5): section 2 is the character's rig, the table of seventeen controllers, and every
  section the question names is now accounted for.** Control: [`uq220_section2_rig.py`](../../_index/candidates/uq220-section2-rig/uq220_section2_rig.py) (8 checks, FAILS 0).
  - **Section 2.** The tail copy lands at the resource entry's `+0x94`, which is where [the rig of seventeen controllers](../Character-Render-Records/the-rig-of-seventeen-controllers.md) hangs the rig.
    The same load path then hands `+0x94` to the rig's slot initialiser. For each populated slot, that initialiser
    calls the controller's own init on rig + slot offset, and it stores null for an empty slot.
    - **Slot *n* is controller *n*** (0 sway … 16 body shake). Slots 0–3 and 5–16 are initialised.
    - **Slot 4** is authored in 52 blocks (chara 17, npc 24, monster 11), but no initialiser addresses it. The rig
      page already finds no switch arm for it.
    - **Slots 17 and 18** are zero in all 1,066 blocks, and nothing addresses them.
    - The fixed record at `+0x4C` is the rig's own header. The initialiser tests its two `-1` fields (`+0x68`,
      `+0x6C`) and fills its pointer fields `+0x70`–`+0x7C` at load.
  - **Sections 3 and 7** are answered elsewhere: 3 is the attachment table (the correction above), and 7 is
    [the pose sequencer](the-pose-sequencer.md).
  - **Section 6** is a dead table whose layout is proven. **Section 18** and **21–24** do not exist (`FW-2`, and
    SWE2-DATA's corrected header).
  - **Not answered here, and not this row's question:**
    - what each controller's record holds. Those are the rig page's own unknowns (its section 7).
    - the readers of section 8's copy, which stay with `UQ-218`. Section 8 is not among the sections this row names.
      *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: `UQ-218`'s 2026-09-30 answer does not cover them, so this residue
      has no open row. A new register row is proposed for SWE2-DATA in the
      [batch-12 record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md). The lead is check C3: the copy's
      offset is the record's `+0x300`, read by four accessors, `003E6680` (from `00425DC0`), `003E66D0` (from `00425E10`),
      `003E6710` (from `0041FCF0` and `00520140`) and `003E6D40` (from the LOD updates `0042CBF0` and `0042D050`, and from
      `00421280` and `004213E0`).)*
      *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: answered. The copy's readers are the six `0051Cxxx`/`0051Dxxx`
      routines listed under "Section 8" at the end of this page: a per-frame update, a draw, on/off, a LOD scale and a
      hide/freeze merge. [Record](../../_index/candidates/swe2struct-residue3-0930/README.md), checks P1-P9.)*
- [x] **UQ-221.** **The section-1 pairs 67 / 68 and 79 / 80** — read with a per-field alternate; what they
  bound is not established.
  ***ANSWERED 2026-09-18 (FABLE) — the pair is the actor's default footprint radius, width and depth, and the field bit selects an alternate set.** The bind `002E28E0` fetches 67 / 68 (79 / 80 when `FieldData_GetActiveFieldRecordBit15` holds) and hands them to `0026B2E0(actor, x, y)` (`002E2F8A`..`002E2F95`), which is also the tail of script verbs `0220 setradius` (`0033F890` → `0026B2D0`) and `0221 setradius_221` (`0033FCD0`); and the getter `002E9660` (kind-3 gate, behind the 22-byte adapter `00263860`) returns the pair's first value unchanged for verbs `02B1 getdefaultradiusw` / `02B2 getdefaultradiusd` (`00350910`). So the FCP pair is the *default radius* a script's `setradius` overrides. For a kind-3 actor `0026B2E0` stores the raw pair at movement-context `+0x80` / `+0x84`, the pair times the actor's x / z scale (`+0x20` / `+0x28`; `+0x24` is the y-scale the tunable installer uses) at `+0x50` / `+0x54` (`003DA860`), and `max(0.01, (x·sx + y·sy) × 0.5)` — the floor is `008F30E4` = 0.01 — at `+0xFC`; then it tail-jumps the body shape `00268380`, which reads `+0x50` / `+0x54` (`002683A8`, via `003DA710`) into the movement body's radii `+0xF0` / `+0xF4`, the footprint the separation pass pushes bodies apart by. For kind 1 the pair × 1.0 (`01CEBBA8`) goes to `+0x30` / `+0x34` and the scalar to `+0x70`. `002E8E20` re-applies the stored pair `+0x80` / `+0x84` after a scale change. The values fit: 0.5 / 1.0 / 0.6 for characters, `m1002` 1.6 / 3.4 for a wide monster. Static: the bodies, the verb dispatch table (rows `0220`, `0221`, `02B1`, `02B2`) and the archive census above.*

## 8. Related

- [`frp-object-container.md`](frp-object-container.md) — the container this block is the first entry of.
- [`../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md`](../../02-Resource-And-Asset-Pipeline/resource-section-addressing.md) — the tag + name lookup.
- [`../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md`](../../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md) — §2.6.2, where the twelve tunables land.
- [`../Character-Render-Records/the-character-render-record-array.md`](../Character-Render-Records/the-character-render-record-array.md) — the `0x740`-byte record whose `+0x3C`, `+0x400`, `+0x408` and `+0x26C` this sheet reads.

## Falsification pass 2 — 2026-09-13 (OPUS)

All 1,066 `.cm` were re-extracted from `FFXII_TZA.vbf` and every corpus figure in §2 and §5
re-derived, with the container walk taken from the bytes: `@FRP`, count at `+0x0C`, a 32-byte name at
`+0x10`, and an offset table at `+0x30` **whose entries are relative to the table base** — which is
why entry 0's `0x20` puts `@FCP` at `0x50`.

**The archive index itself gives 1,066 `.cm`**, so even the denominator is independent of the sheet.

| claim | measured |
|---|---|
| `@FCP` on entry 0; `+0x04 = 0`; `+0x0C = 1`; name = the container's | **1,066 / 1,066** on all four |
| payload `+0x32 = 0x0A`, `+0x33 = 0`, `+0x34 = 0xFFFF`, `+0x3E = 0` | **1,066 / 1,066** on all four |
| `+0x36`: 2 in 993, 3 in 54, 14 in 19 | **993 · 54 · 19** |
| `+0x3A`: 1 in 628, `0xFFFF` in 426, other in 12 | **628 · 426 · 12** |
| `+0x3C`: `0xFFFF` in 762, 1 in 301, **three** other values | **762 · 301**, and exactly **three** others (2, 8, 15 — one each) |
| `sectionOffset[0]` 4 in 939, 260 in 127 | **939 · 127** |
| the event map's four patterns | **723** all-zero · **298** `7F×6` (§5's "297 weapons and one treasure") · **29** `3D 36 35 01 81 7F` · **16** `08 01 05 00 7F 7F` |
| section 1 present | **1,066 / 1,066** |

### `sectionOffset[21]` is not a section offset

§5's invariant *"no section offset points outside the entry"* holds for **every real offset** and
fails only at slot 21. Profiling all 25 slots over the corpus separates them cleanly:

| slots | non-zero in | distinct values | out of range |
|---|---|---|---|
| 0–10~~, 18~~ — the real table *(corrected 2026-10-02, OPUS: no section 18 exists, the 2026-09-21 tail-section extension)* | 7 to 1,066 files | 1–239 | **0** |
| 11–17, 19, 20 | **0** | — | 0 |
| **21** | **1,066** | **924** | **988** |
| 22–24 | the six-byte event map | 3–4 | (bytes, not offsets) |

**924 distinct values in 1,066 files is not an offset table — it is a per-file value.** It is out of
range in **988** of them, and the 78 that are in range are in range *by coincidence*: their mean
payload is `0x306B` against `0xF26` for the rest, which is exactly how a random 16-bit number behaves
— it looks like a valid offset only in the big files.

`c1054` is one of those 78. Its `+0x2A` reads `0x11DF`, which lands inside its `0x3260`-byte payload,
and §2 listed it as *"`21` (`+0x11DF`)"* among the sections in file order. **That was a coincidence,
and the corpus shows it.** `+0x2A` is removed from the section list and the fence narrowed to
~~`u16[19]`~~ `u16[18]` *(corrected 2026-10-02, OPUS: the current fence, §2 and the 2026-09-21 extension)*, since slots 11–17 are zero in every file.

> This is the shape a layout sheet is most vulnerable to: **one file, read carefully, cannot tell a
> field from a value that happens to look like one.** Only the population separates them — and the
> separator here is not the invariant failing, it is *924 distinct values*.

### `FW-2` — answered the same day: no shipped id addresses section 21

I opened `FW-2` above because an id naming section 21 would index `payload + 0x11DF`-style garbage.
The ids are compile-time constants, so it is answerable: **43 call sites** of the float getter
`004FE270`, the dword getter `004FE2F0` and the scaling wrapper `003E6150`, **40 with the id as an
immediate**, three computed.

**No id addresses section 21.** Nor any section but **1** and **9**:

| ids | sections indexed |
|---|---|
| 3 ids `0x0100xxxx` | section **1** |
| 16 ids `0x09xxxxxx`, 29 call sites | section **9** |
| 7 ids `0x6xxxxxxx` | **none** — these are the bit-field ids, which read `sectionOffset[9]` (§3) |

So `+0x2A` being a value rather than an offset is a **documentation error, not a live out-of-bounds
read**, and §'s "the two sections the engine's static readers address" is exactly right.

> **And the same trap caught me twice on one page.** My first bucketing of these ids reported
> sections 0, 2 and 3 as addressed — because I took `SS & 0x1F` from every id, including the
> `0x6xxxxxxx` ones whose `SS` byte is `0x60`, `0x61`, `0x62`, `0x63`. **Those low five bits are not
> a section number**, exactly as `+0x2A` is not an offset. §3 says so — *"the top three bits of `SS`
> select the getter's mode"* — and I applied the mask without the mode. A byte that looks like a
> field is the failure mode of this whole document, in both directions.

**Control:** the sweep recovers sections 1 and 9, which § documents independently. Without that, its
silence about 21 would mean nothing. The three computed-id sites (`002E9698`, `002ECE69`,
`003E6332`) are **not** covered by this answer; nothing establishes what they pass. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. `UQ-219`'s 2026-09-18 answer in §7 settles it, and the [batch-12 record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md) check C2 pins it. `002E9698` passes one of two constants, `0x1002143` or `0x1002D4F` (a `cmovne` on the field bit, both in §3's table). `002ECE69` and `003E6332` are pass-throughs: the adapter `002ECE50` never writes `edx`, and `003E6310` passes its caller's id (`mov edx, ebx`). So their ids are their callers' immediates, which the 50-id sweep covers.)*

**Not claimed:** nothing here was executed or observed live. §5's section-9 and section-1 slot
distributions, the 4,230-file entry-tag survey and §6.1's tunable index table were not re-derived;
this pass took the header invariants, the five histograms, the event map and the offset table.

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **Status_Periodic_Terminal — CLIENT.** A cited function is called by `BattleStats_RemoveStatusesFromMaskAndRecompute`, `BattleUnit_RunPeriodicCombatMaintenance` and `BattleStats_ChangeStatusAndProcessSideEffects`.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_EvaluateAndResolveActionTarget`, owned by that layer, calls `00377C20` on this page. That caller is the order evaluation: a `0xAB8`-byte frame with a stack cookie that writes a resolved id into the caller's word - `0xFFFF` for none - and refuses entirely while `byte[02089340] & 0x20` is set; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Gameplay — CLIENT.** `FUN_0030a8a0`, owned by that layer, calls `00377C20` on this page. That caller is a 204-byte walk whose first act is to keep only **bit 0** of its third argument, so the flag word it is handed carries exactly one meaningful bit here; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**InputGameplay — CLIENT.** `FUN_00313a00`, owned by that layer, calls `00377C20` on this page. That caller is a state query that tests the pointer at `[02089350]` and the global equality predicate `00253B90`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — CLIENT.** `BattleUnit_ProcessDefeatRewardsAndLoot`, owned by that layer, calls `00377C20` on this page. That caller is defeat-and-loot processing, which reads the defeated unit's `+0x698` block, needs `byte[+5] == 1`, and is suppressed entirely by bit 3 of `byte[+0xE9A]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Script_VM_Native_Bridge — CLIENT (SWE2-CONTRACT 2026-09-15, 18 edges).** Eighteen script-bridge
bodies consult this page's parameter-block accessors: `002E28E0` is called by `003409F0`/`00342640`/
`00355210`/`0050D810`, `002E5FD0` by `0050E6F0`/`0050E7B0`, `002E7DD0`/`002E7E10`/`002E7E50` by the
`0034D300`/`0034CB30`/`0034C7A0` family, `002E9B10` by `0034EFE0`/`003578B0`/`0050F6E0`/`0034E710`/
`0034F4F0`, and `00377C20` by `00352FA0`/`00355680`/`00344740`/`003537D0`. The script VM reads FCP
character parameters through these getters — the same shape as the InputGameplay and Rewards rows
above: the layer consults the block, the block owns nothing in the VM.

**CombatFormula — MECHANICAL (SWE2-CONTRACT 2026-09-15, 6 edges).** `00233AD0` calls
`BattleRuntime_ResetPersistentStatePrefix`; `00384E50` calls `BattleStats_FindOwningBattleUnit` and
is reached by `BattleFormula_ComputeKnockbackImpulseScale`/`00389370`/`004FE2F0`; `00377C20` is
reached by `BattleStats_ModifyHPAndProcessLethalState`. Shared combat-state accessors — the
parameter block is consulted by the formula layer, no ownership crossing.

**Movement — CLIENT on fifty-two edges, SERVICE on seven (59 edges through 33 movement bodies; five
read in full).** The functions cited here reach the movement layer widely rather than through one
accessor: 33 distinct bodies, the busiest taking 7, 5, 5, 5 and 4 edges. Reading five of them turned
up the thing worth writing down.

**Four of the five busiest share one admission test**, and it is the same field
`Actor_GetWorldPosition` uses. `0026AC70`, `002690D0`, `002EC510` and `0026A1A0` each begin with
`movzx eax, byte [actor+3] / and al, 0xE0 / cmp al, 0x60` and do nothing at all unless it matches —
that is **kind 3**, the top three bits of byte 3, one of the two kinds `00265020` will return a
position for. So the movement layer is not guarded per entry point; it has one shared idea of what
it will move, tested separately in each body. `002EC510` adds a second gate on the same line,
requiring `[actor+0xB8]` to be non-null before it dispatches on its mode argument.

Of the five, `0026AC70` is the one doing arithmetic rather than checking: it wraps an angle, adding
`+π` (`01CEBC50`) when the scaled value is at or above zero and a negative constant from `00915620`
when it is below, before applying the kind test. `0026A1A0` reaches `[actor+0xB8]`, takes the
sub-object at `+0xF0`, and merges one flag into **bit 7 of `byte[+0x62]` while preserving the low
seven bits**. `002E28E0`, the busiest at 7 edges, works `[+0xB8]`, `[+0xC0]` and `byte[+0x15]`
together.

Seven edges run the other way: five movement bodies read `FieldData_GetActiveFieldRecordBit15` and
two read `003E6150`. **Five of the 33 bodies on that layer are read; the rest are counted.** Edge
count and subject list from `edges.tsv`. Read from the shipping bytes 2026-09-14 (OPUS).

**Party — CLIENT and SERVICE (OPUS 2026-10-02, 4 edges).** CLIENT: the analog movement-scale computation `PartyControl_ComputeAnalogMovementScale` (`00358A20`) calls this page's `002E7E50`, the reader of the `0x9000606` / `0x9000000` pair in section 3, at `00358A20+0x29`; the 639-byte Party body `00304180` calls `FieldData_GetActiveFieldRecordBit15` (`00377C20`) at `00304180+0xB2`. SERVICE: `003045A0` takes the focus unit through `PartyRoster_GetActorBySlot` (`0031ABF0`, at `003045A0+0x18`) before it reads slot 2, the body radius; `0046CC70` asks `PartyFocus_GetCurrentPackedActorHandle` (`003590D0`) at `0046CC70+0xEF`. Edges from `edges.tsv`; the four call sites read.

## CORRECTED 2026-09-19 (FABLE) - Section 3 is the attachment table, and "no reader" was a statement about one getter

**Claim (2026-09-18, FABLE, UQ-220):** sections 2, 3, 6 and 7 are authored data the shipping engine's static paths never
read. **Correction:** the scan behind it followed the eleven callers of the payload getter `003E55F0`. The accessors
beside it **do not call the getter** - they load the render record's payload pointer `+0x400` themselves and add a
section-offset word. Direct readers, by header word: `+2` (section 1), **`+6` (section 3: `003E5CD0`, 32 B, read
whole)**, `+8` (section 4), `+0xE` (section 7), **`+0x10` (section 8: `003E6D10`, 44 B, read whole - the section's first
word x `0x1D0` + `0x10`, a byte size)**, `+0x12` (section 9) and `+0x14` (section 10). None for `+4` (section 2) or
`+0xC` (section 6). **Instrument:** a displacement sweep for loads of record `+0x400` across `003E5000`..`003E7800`,
then the first word read through each. **Kind:** `no-reader-found`, `scope-too-narrow`. ***SUPERSEDED 2026-09-21
(SWE2-DATA) — sections 2 and 6 both have readers, and "section 18" never existed.** A whole-image sweep for the same
accessor shape found `+4` read by `003E4B40` (below the swept range; its only callers compute the section-2 pointer
for the `@FTR`-tail memcpy — `dword +0x24` is the copy length, not an offset) and `+0xC` read by `003E5C0E` — which
decodes section 6 as 16 keyed `{u16 key|0xFFFF, u16, u32, f32, f32}` records but is itself **unreferenced** (dead
code; no E8/E9/dword/qword ref). Details in the last section.*

**Section 3, from its consumer.** `0041EDE0(parent, child, slot, mode)` (555 B, read whole) attaches a child render
record to a bone of a parent; 0041F010 repeats the same section-3 reads (skimmed, not read whole, so not cited).
*(Read whole 2026-09-30, SWE2-STRUCT for OPUS, DD batch 12, [record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md)
check C1. `0041F010(parent, child)` makes the same section-3 reads with the same two modes: mode 1 takes the bone from
the child's `+0x36`, and mode 0 takes the bone, offset, scale and rotation from the table. It differs from `0041EDE0` in
three ways:*
- *the slot comes from the child's own `@FOR` byte `+0x6A0` (`003E5CF0`), not from an argument, and a slot below `0x16`
  is also stored at the parent's `+0x40C`;*
- *there is no requested mode: the mode is the parent's default (`+0x40B` bits 0-1), or 0 when `+0x284` bit 27 is set;*
- *the child's index is kept at the parent's `+0x2C8` (slot below `0x16`) or `+0x2CA` (slot `0x16`). Those are the two
  children `00429760` re-attaches for authored command `0x15`.*

*Its callers are the dirty-bit-19 handler `004215A0` and `00424D80` (twice).*

```struct FcpSection3 base=section3 size=0x3C0
+0x000  u16[32]     bone       bone id per attachment slot, 0xFFFF = the slot names no bone
+0x040  f32[3][32]  offset     per slot; multiplied by the parent's scale factors +0x160.., +0x260.. and +0x26C into the child's +0x150..+0x158
+0x1C0  f32[32]     scale      per slot; copied to all three of the child's +0x170..+0x178
+0x240  f32[3][32]  rotation   per slot; into the child's +0x130..+0x138
```

- **Mode 0:** bone, offset, rotation and scale all come from this table - unless the slot's bone word is `0xFFFF` (or the
  parent has no section 3), in which case the bone is found as in mode 1.
- **Mode 1:** the bone comes from **the child's own** header word `+0x36` (through the special-bone lookup), the offset
  and rotation are zeroed, and **only the scale** is taken from this table - which is why slots with no bone still carry
  authored scales.
- Which mode: bit 27 of the parent's `+0x284` forces mode 0; a requested mode of 2 means "use the parent's default",
  the signed two-bit field in bits 0-1 of the parent's byte `+0x40B`; the mode actually used is recorded in bits 2-3 of
  that byte. *Who asks, found 2026-09-20 (FABLE): authored command `0x15` - mode 1 in every `active` block and mode 0 in
  every `deact` block, 609 each, through the dirty-pass routine `00429760`. Drawing a weapon moves it from the table's
  slot to the bone the weapon itself names; sheathing moves it back
  ([the authored-command page](../Authored-Commands/the-authored-presentation-command-handlers.md), row `0x15`).*

**The size was a prediction, and it holds.** The code gives four array bases and no count; they abut only if there are
32 slots, which makes the section `0x3C0` bytes. Over the files
([`census.py`](../../_experiments/evidence/fcp-section3-attachment-table/census.py) →
[`census.out.txt`](../../_experiments/evidence/fcp-section3-attachment-table/census.out.txt)): **603 of the 1,066 blocks
have a section 3, and it is exactly `0x3C0` bytes in all 603.** Bone ids run to 41; every used slot's floats are finite
with a positive scale (1.0 in 1,882 used slots, then 1.3, 1.2, 2.5, 1.5); 428 of the 603 name no bone in any slot.

**Section 8's size rule holds too.** `003E6D10` returns the section's first word x `0x1D0` + `0x10`; section 8 is present
in 28 blocks and is exactly `0x10 + n x 0x1D0` bytes long in all 28 (n = 1 in 3, 2 in 25) - a 16-byte header and `n`
records of `0x1D0` bytes. What a record holds was not read. *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: partly stale. The 2026-09-21 "Section 8" extension at the end of this page decodes the record's header, transform and tail. Who reads the runtime copy has no register row yet, and a row is proposed in the [batch-12 record](../../_index/candidates/swe2struct-ddres-b12-0930/README.md); see the `UQ-220` box.)* *(2026-09-30, SWE2-STRUCT for OPUS, residue 3: the runtime readers are now answered under "Section 8" at the end of this page ([record](../../_index/candidates/swe2struct-residue3-0930/README.md), P1-P9).)*

**Section 4 is what makes a record's four auxiliary objects.** `003E6770(record, enable)` (276 B, read whole) reads a
`u32` count at the section's start, caps it at 4, and for each `0x50`-byte descriptor from `+0x10` writes the record's
own index into the descriptor's `+4`, has the `0x3C0`-stride pool at `02CA8420` build an object from it, and keeps the
handle in the record's `+0x438`..`+0x444` - the four auxiliary handles
[the fade page](../Character-Render-Records/how-a-character-fades-the-ten-channels.md) hands the opacity to; with
`enable` = 0 it switches each object off instead. It runs only while the first handle is still `0xFFFF`. On the files:
section 4 is present in 216 blocks - **202 of them weapons**, 9 gadgets, 4 summons, 1 monster - and is exactly
`0x10 + n x 0x50` bytes with n <= 4 in all 216 (n = 1 in 199). *What the objects are was not established; a weapon's
descriptor carries little more than two floats (1.0 and 2.0-2.4 in the two opened).* **Established the same day: they are
[bone trails](../Character-Render-Records/the-bone-trails.md) - the descriptor's word `+2` is the bone, and a census of
all 238 descriptors finds nothing else in them that varies but one float.**

*Not decoded here: sections 7 (decoded on its own page, published separately), 8 and 10, which now have named readers; sections 2 and 6, which still have none by
this wider sweep - itself bounded to one address range.* *(2026-09-30, SWE2-STRUCT for OPUS, DD batch 12: stale. Both now have readers. The 2026-09-21 whole-image sweep below finds `003E4B40` for section 2, the source of the `@FTR`-tail copy, and `003E5C0E` for section 6, which is dead code. `UQ-220` is ANSWERED.)* Interior of `0041EDE0`: `0041EE02`, `0041EE22`, `0041EE40`,
`0041EE5F`, `0041EE7E`, `0041EE96`, `0041EED0`, `0041EF22`, `0041EF3A`, `0041EF55`, `0041EF99`, `0041EFFE`.

## Extension 2026-09-21 (SWE2-DATA) — the tail sections: a corrected header, and section 2 is live

A whole-image sweep for the accessor shape `mov r64, [rec+0x400]` → `movzx r, word[r+off]` (every
`.text` occurrence, not bounded to one range) produced the complete reader inventory for the
payload offset words. Two earlier claims need correcting.

### The header's `+0x24` is not `sectionOffset[18]` — there is no section 18 (SWE2-DATA)

`0041FCF0` (the render-record initialiser) reads the payload twice at `0041FE24` / `0041FE3B`
through `003E4B40`, which returns **`word[+0x04]` itself** — section 2's offset — then
`lea ecx, [rsi+0x30]` + that word gives `r14 = payload + sectionOffset[2]` and
`r15d = dword[payload+0x24]` (`0041FE40`). The pair is passed as the fifth/sixth stack arguments
to `0041F340` (`0041FF70`, `0041FFD5`) and forwarded to `00372820`, which — after sizing the
`@FTR` allocation through `003712E0` (which adds the `+0x24` dword to the 16-aligned
`((dword+0xC × 0x149 + word+0x38) × 2)` core) — performs

```
003729B7  r8  = dword[payload+0x24]        ; length
003729BA  rdx = payload + sectionOffset[2] ; source
003729BD  call 861eba                      ; memcpy(FTR_alloc + coreSize, section2, dword+0x24)
```

— i.e. **section 2 is live: its bytes are appended verbatim into the tail of the `@FTR`
allocation** (the runtime pointer `record+0x94` holds the tail; `record+0x90` the core size).
`dword +0x24` is that copy's **byte length**. It reads as a section offset only numerically:
in 538 of 1,066 blocks it equals section 2's end offset (the next section's start), and in the
other 528 it equals section 2's byte size — two authoring generations; the runtime uses it as a
length either way, so the second population copies section 2 plus the head of whatever follows
it into the (correctly sized) tail. Every "section 18" byte region reported earlier is section
2's own extent or its neighbour — no section 18 exists. Consequence for the header:

```struct FcpPayloadHeader base=payload size=0x40
+0x00  u16[18]  sectionOffset  payload-relative offset of section n, 0 = absent; [17] is 0 in 1,066 / 1,066
+0x24  u32      ftrTailLen     bytes memcpy'd from sectionOffset[2] into the @FTR tail (0 for s2-absent would be pointless; never 0)
+0x28  u16      _zero28        0 in 1,066 / 1,066
+0x2A  u16      _perFileValue  (unchanged)
```

### The complete offset-word reader inventory (SWE2-DATA)

| word | section | readers (all instruments: E8/E9 + absolute-dword/qword scans of the whole image) |
|---|---|---|
| `+0x02` | 1 | `003E56A0` + wrapper `003E6F70`; inline `003E4700`, `003E4B71`, `003E561B`, `003E592F`, `003E5A0F`, `003E5EFB`, `003E60B3` |
| `+0x04` | 2 | `003E4B40` — returns the raw word; only callers `0041FE24` / `0041FE3B` (the copy-source computation above) |
| `+0x06` | 3 | `003E5CD0` + the attachment consumers (§ "Section 3 is the attachment table") |
| `+0x08` | 4 | `003E6D80` (callers `0051BEAD`, `0052448A`) + inline `003E677C` |
| `+0x0A` | 5 | ~~**none** — present in 7 blocks, unread~~ inline in `003E7210`, the palette-binding walk of authored command `0x16` - present in 7 blocks *(corrected 2026-10-01, OPUS: the authored-commands page's GI-15 section; the scans above missed the `[record + 0x400]` load)* |
| `+0x0C` | 6 | `003E5C0E` — **dead code**: no E8/E9/dword/qword reference anywhere |
| `+0x0E` | 7 | `003E6F50` + inline `003E6A2D`, `003E7464` |
| `+0x10` | 8 | `003E6CF0` / `003E6D10`, both called only by the initialiser's copy at `0041F5CE` / `0041F5D9` |
| `+0x12` | 9 | `003E56C0` + inline `003E58B0`, `003E5C90`, `003E5EA0` |
| `+0x14` | 10 | `003E6E40`, sole caller `003AF3B0` |
| `+0x16`..`+0x22` | 11–17 | never present in any block |

### Section 2 — the `@FTR` tail blob, `1,066 / 1,066` blocks (SWE2-DATA)

```struct FcpSection2 base=section2 size=var
+0x00  u32[19]  slotOffset   byte offset of that slot's record, 0 = absent; smallest nonzero >= 0x90 in every populated file
+0x4C  byte[68] anchor       the fixed record, present in every block -- see below
+0x90  ...      blob         the slot records (variable positions)
```

- The 19-slot table then a fixed record reproduces exactly in the minimal case: all-zero
  sections are exactly 144 B = 19×4 + 68 (306 files). Slot values point into the blob; a
  character block indexes 13 of 19 slots, records scattered at authored offsets.
- The 68-byte anchor's invariants across weapons, characters and monsters:
  `f32[3]` then `{u16 pair, u32, u16 pair, u32 0x1E, i32 -1, i32 -1, u32 0×5, u32 0x103,
  u32 0, u32 0x90, u32 count}` — the `0x90` self-offset and the count bound what follows.
- Slot records are float/u32 mixes; ~~their key domain (the 19 slots) is **not yet named** —
  the copy lands beside `@FTR`'s `count × 0x149` node records (`word[rbp+0xC]` →
  `record+0x88`), so the FTR node table is the prime suspect for the key domain. The
  tail-copy consumers live on the FTR side (UQ-218).~~ *(Named 2026-09-26 (FABLE, Claude Opus 5.5): the key domain is
  the rig's controllers, not the FTR nodes. Slot *n* is controller *n* of [the rig of seventeen controllers](../Character-Render-Records/the-rig-of-seventeen-controllers.md). Slots 17 and 18 are
  empty in every block. The consumers are the rig's initialiser, its per-frame update and its switches; see the
  `UQ-220` box.)*

### Section 6 — a dead key→vec3 table, `256` bytes in `1,066 / 1,066` (SWE2-DATA)

`003E5C0E` proves the authored layout: 16 records of `0x10` bytes, indexed by argument —

```struct FcpSection6Record base=section6 size=0x10
+0x0  u16  key      0xFFFF = empty; live keys run 0..~125
+0x2  u16  _pad
+0x4  u32  x        small dword (id or scalar-bits)
+0x8  f32  y
+0xC  f32  z
```

The reader copies `{x, y, z}` plus a `1.0f` pad into a `vec4` out and returns the key
(`0xFFFF` → caller sees `-1`). **No shipped code calls it** — every reference kind (E8, E9,
absolute dword, qword) is empty, so the table is authored data with no live consumer on PC.
Census of all 1,066 blocks: key `0` is nearly universal (1,813 records), keys `0`–`61`
dominate and slot patterns are per-class — weapons carry 0–2 populated slots, humanoids up
to a dozen.

### Section 8 — a verbatim initialiser copy, 28 blocks (SWE2-DATA)

`003E6D10` (`u16[0] × 0x1D0 + 0x10`) and `003E6CF0` are called back-to-back only at
`0041F5CE` / `0041F5D9`: the section is `memcpy`'d whole (`861eba`) into the model
container's aux region (`003AB7F0` result + `ebp`; `[dst+8]` gets the record's `+0` word).
Header `{u16 n, u16 0x10, u16 flag?, u8?}` then `n` records of `0x1D0`: a record opens
`{u32 0, u32 8, u32 7, u32 id}` (`id` = `0x4C0E` on treasures, `3` on the NPC/monster
samples), carries a 4×4 float transform at `+0x10`..`+0x4F`, two u32 quartets at `+0x60` /
`+0x80`, a `0x120`-byte zero region, and a three-float tail at `+0x1B0`. Present only on
treasure and a few NPC/monster blocks (25 two-record, 3 one-record). Consumers read the
copied buffer, not the FCP — the runtime side stays with UQ-218.
*(2026-09-30, SWE2-STRUCT for OPUS, residue 3: the runtime side is answered here; it was never `UQ-218`'s. **In play:**
on treasure and the few NPC and monster models that carry section 8, each record is a point fixed to one of the model's
bones. While the model is on screen the engine remembers where that point has been over its last sixteen updates and
draws the history every frame, faded with the model, through the legacy packet path - the same shape as the
[bone trails](../Character-Render-Records/the-bone-trails.md). What the packet looks like on screen is not read. It is
switched on when the render record is promoted, frozen while the record's `+0x284` bit 24 (the time-stop page's set 3)
is set, and hidden or shown by the channel setter. **The readers.** The copy (aux base + record `+0x300`) is reached only
through the four `+0x300` accessors, which hand it to six routines and to nothing else:*
- *`0051D310`, the per-frame update, from `00425E10` in `RenderSystem_RunCharacterUpdatePipeline` (`003323D0`). While
  header `+6` is set and `(+7 | [02CA8428])` bit 0 is clear, each `0x1D0` record maps its point `+0x1A0` through the bone
  that `+0xC` names on the owning render record (header `+8`; `00421D70`, `004220F0`), counts `+0` up to 16, and rewrites
  the history rows `+0xA0`..`+0x19F` and `+0x10`.*
- *`0051CDE0`, the draw, from `00425DC0` (the after-emission stage of the pass dispatcher `00332440`). While `+6` is set
  and bit 1 is clear, it submits at once, through `00540C70` (whose only caller it is), the template packet `02AEC180`
  and, per record, the template `02AEC2D0` with the record's first `0x1A0` bytes spliced in. The values are scaled by the
  render record's fade product `003E5770` (`+0x260` x `+0x160` x `+0x26C`), by record `+0x1C0` and by header `+0xC`.
  `0051D1D0` first binds the two resources that `0051D220` builds once from the image block `01F2B340`.*
- *`0051DB60` and `00519720`, on and off, from `003E6710`. The promoter path `0041FCF0` passes 1. Command `0x1F`'s
  handler `00520140` passes its word, and no shipped motion authors that command. "On" resets every record (`+0` = 0,
  `+0x10` = 0, `+0x14` = 1.0, `+0x1C4` = 1, history zeroed) and sets `+6` = 1, `+7` = 0.*
- *`0051DBE0`, which stores render record `+0x49C` at header `+0xC`, from the LOD updates `0042CBF0` and `0042D050`.*
- *`0051D2F0`, which merges into header `+7`: `00421280` sets or clears bit 1 (hide), and `004213E0` sets bit 0 (freeze)
  while `+0x284` bit 24 is set.*

*No reader keeps the copy or passes it on (structflow from each entry: no escape, and the one hand-off is the reset's
memset). So at run time record `+0`, `+0x10`, `+0x14` and `+0xA0`..`+0x19F` are the engine's, not the file's. The
authored values that are read are the bone selector `+0xC`, the point `+0x1A0`, the tail `+0x1B0`, `+0x1C0` and the
packet bytes the draw splices in. Checks P1-P9 in the
[residue-3 record](../../_index/candidates/swe2struct-residue3-0930/README.md), `residue3_check.py` FAILS 0.)*

### Section 10 — a 48-byte spawn block, only two fields live (SWE2-DATA)

`003E6E40` → `payload + word[+0x14]`; the sole caller `003AF3B0` (inside `003AF390`) builds a
spawn record `rbx` (`+0x1C = 0x11000000`, serial `counter<<8 | id` at `+4`) and reads only two
of the 48 bytes' fields:

```
003AF436  ecx = u8[s10 + 0x10]           ; divisor (8 in the samples)
003AF43A  xmm1 = f32[s10 + 8]            ; duration-ish (75.0 typical)
003AF44A  rbx+0x18 = duration / count    ; spawn period
```

The remaining 42 bytes of the 48 (104 distinct patterns across the 613 blocks) have no
reader — the pointer is only reachable through this one call. Present in 613 blocks, always
exactly 48 bytes.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../_index/candidates/opus-fcp-character-parameter-block-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00265240` | 43 B | returns 0 unless byte `+3` of `rcx` ANDed with `0xE0` equals `0x60`; on that path loads qword `+0xB8`, copies its dwords `+0x20`, `+0x24` and `+0x28` to `[rdx]`, `[r8]` and `[r9]`, and returns 1 | `00265246`, `0026524A`, `00265254`, `0026525F`, `00265262` |
| `0026B2D0` | 8 B | copies the second float argument `xmm1` into `xmm2` and tail-jumps `0026B2E0`, so the callee receives the same value as its second and third arguments | `0026B2D3` |
| `002E7DD0` | 59 B | returns 0.0 when `rcx` is null, its qword `+0xC0` is null or the dword at that pointer is -1; otherwise clamps `edx` to 0 when negative and tail-jumps `003E6150(that dword, 0x9000707)` when the clamped value is 0, else `003E6150(that dword, 0x9000101)` | `002E7DD5`, `002E7DE3`, `002E7DEC`, `002E7DF8`, `002E7E02` |
| `002E7E10` | 59 B | returns 0.0 when `rcx` is null, its qword `+0xC0` is null or the dword at that pointer is -1; otherwise clamps `edx` to 0 when negative and tail-jumps `003E6150(that dword, 0x9000808)` when the clamped value is 0, else `003E6150(that dword, 0x9000202)` | `002E7E15`, `002E7E23`, `002E7E2C`, `002E7E38`, `002E7E42` |
| `002E9630` | 39 B | returns 0.0 when `rcx` is null, its qword `+0xC0` is null or the dword at that pointer is -1; otherwise tail-jumps `003E6150(low word of that dword, 0x9001D1E)` | `002E9635`, `002E9641`, `002E9646`, `002E964E`, `002E9653` |
| `00342640` | 163 B | when byte `+8` of `r8` is non-zero, word `+0xA` of `r8` selects: 1 calls `002EBC90(rdx, 0, 1)` and `002E28E0(rdx, 002E97C0(dword r8+4))`, 3 calls `002EBC90(rdx, 3, 1)` and `002E3110(rdx, 4, 0, 002E97C0(dword r8+4), 0)`, each followed by `002EAC90(rdx)`, and any other value does neither; every path then tail-jumps `0025B470(rdx, 00265950(rdx))` | `0034264A`, `0034265C`, `0034267E`, `003426B9`, `003426DE` |
| `0034EFE0` | 122 B | calls `0026A1A0(rdx, 0)` and `0034BE50(rcx, rdx, r8, r9)`, passes `002E9B10(rdx)` as the float to `0026AC70(rdx, value)`, calls `002EC510(1, rdx, qword [r8])` and tail-jumps `002690D0(rdx)` | `0034F005`, `0034F016`, `0034F029`, `0034F039`, `0034F055` |
| `0034F4F0` | 125 B | calls `0026A1A0(rdx, 1)` and `0034BE50(rcx, rdx, r8, r9)`, passes `002E9B10(rdx)` as the float to `0026AC70(rdx, value)`, calls `002EC510(1, rdx, qword [r8])` and tail-jumps `002690D0(rdx)` | `0034F518`, `0034F529`, `0034F53C`, `0034F54C`, `0034F568` |
| `003E4700` | 41 B | loads qword `+0x400` of `rcx` and returns the float at `+0x144` of the address formed by adding its word `+2` to the pointer's low 32 bits and sign-extending the sum; returns 1.0 (`01CEBBA8`) when the qword is null or that 32-bit sum is zero | `003E4707`, `003E470C`, `003E4710`, `003E4717`, `003E4720` |
| `003E4B40` | 12 B | returns the zero-extended word `+4` of the block that qword `+0x400` of `rcx` points to, with no null check | `003E4B47` |
| `003E56E0` | 25 B | returns 0 when qword `+0x400` of `rcx` is null; otherwise tail-jumps `004FE2F0(that qword, 0x62060A2D)` | `003E56E7`, `003E56EC`, `003E56F1`, `003E56F6` |
| `003E5C90` | 49 B | loads qword `+0x400` of `rcx` and, when it is non-null and its word `+0x12` is non-zero, returns the float at `+0xA8` of the pointer's low 32 bits plus that word, sign-extended; returns 0.10472 (`00D117BC`) when the qword is null, the word is zero or the 32-bit sum is zero | `003E5C97`, `003E5C9C`, `003E5CA3`, `003E5CAF`, `003E5CB8` |
| `003E5EA0` | 41 B | loads qword `+0x400` of `rcx` and, when it is non-null and its word `+0x12` is non-zero, returns the dword at `+0xA4` of the pointer's low 32 bits plus that word, sign-extended; returns 0 when the qword is null, the word is zero or the 32-bit sum is zero | `003E5EA7`, `003E5EAC`, `003E5EB3`, `003E5EBF`, `003E5EC6` |
| `003E66D0` | 63 B | returns at once when dword `+0x300` of `rcx` is 0; otherwise adds that dword to `003AB7F0(0020E600(dword +0x2FC))` and, when the 32-bit sum is non-zero, tail-jumps `0051D310(sum)`, else returns | `003E66D6`, `003E66E8`, `003E66F0`, `003E66F5`, `003E6704` |
| `003E6710` | 88 B | returns at once when dword `+0x300` of `rcx` is 0; otherwise adds that dword to `003AB7F0(0020E600(dword +0x2FC))` and, when the 32-bit sum is non-zero, tail-jumps `0051DB60(sum)` if `edx` is non-zero or calls `00519720(sum)` if `edx` is zero; a zero sum returns without either call | `003E671A`, `003E6736`, `003E673B`, `003E6753`, `003E6758` |
| `003E6D10` | 44 B | loads qword `+0x400` of `rcx` and, when it is non-null and its word `+0x10` is non-zero, reads the word at the pointer's low 32 bits plus that word (sign-extended) and returns it times `0x1D0` plus `0x10`; returns 0 when the qword is null or the word is zero | `003E6D17`, `003E6D1C`, `003E6D2C`, `003E6D2F`, `003E6D35` |
| `00409240` | 15 B | returns zero-extended word `+0x30` of `rcx` when its dword `+4` equals 2, else dword `+0xC` | `00409244`, `00409246`, `0040924A` |
| `00425E10` | 87 B | walks the `0x740`-stride records under qword `022C6F28` starting at the index in dword `+0x48800` of that base and following each record's signed word `+4` until -1, calling `003E66D0(record)` (and reloading the base) for each record whose byte `+0x290` has its `0x2` bit (bit 1) clear; returns at once when the start index is -1 | `00425E1B`, `00425E33`, `00425E3E`, `00425E47`, `00425E53` |
| `0050D810` | 73 B | calls `002EBC90(rdx, 0, 1)`, `002E28E0(rdx, qword [r8+8])` and `002EAC90(rdx)`, then tail-jumps `002EB330(rdx, 0x1001)` | `0050D829`, `0050D82E`, `0050D835`, `0050D83D`, `0050D854` |
| `0051CDE0` | 999 B | calls `001FBD80(2)` and `0039D3F0()`; resolves word `+8` of `rcx` (unless `0xFFFF`) to the `0x740`-stride record under qword `022C6F28`, nulled when its dword `+0x284` is 0; returns without further work when byte `+6` is 0 or the `0x2` bit (bit 1) of (byte `+7` OR dword `02CA8428`) is set; otherwise copies `0x150` bytes of `02AEC180` to the stack, patches in a qword built from the bytes `01F2B349`-`01F2B34D` ORed with `0x2005C00400002A00`, vectors from `02AEDD30`-`02AEDEA0` and lane 2 of `02AEDD60` plus 30000.0 (`009146FC`), and submits `00540C70(packet, 0x15, 0)`; then copies `0x1E0` bytes of `02AEC2D0` once into a second stack packet and, for each of word `+0` records of stride `0x1D0` from `rcx` plus word `+2`, splices the record's first `0x1A0` bytes at packet `+0x10`, multiplies packet floats `+0x3C` and `+0x5C` by `003E5770(resolved record)`, `+0x20` by record float `+0x1C0` and `+0x24` by header float `+0xC` widened to double (passed through the import thunk `00861F5C` first when `001EDDA0()` returns 0), and submits `00540C70(packet, 0x1E, 0)`; finally calls `001FBE50()` | `0051CE5F`, `0051CE73`, `0051CFD4`, `0051D0F4`, `0051D17D` |
| `0051D1D0` | 78 B | calls `00861EC0(02064E30, 0, 0x4000)` and `00258EE0(3)`, then `002D7E00(0x2A00, qword 02CA8430, 0)` and a tail-jump to `002D7E00(0x2E00, qword 02CA8438, 0)` | `0051D1E3`, `0051D1ED`, `0051D201`, `0051D219` |
| `0051DB60` | 127 B | stores word 1 at `+6` of `rcx`, then for each of word `+0` records of stride `0x1D0` starting at the 32-bit sum of `rcx` and word `+2` stores 1.0 (`0x3F800000`) at `+0x14`, 0 at `+0` and `+0x10`, 1 at `+0x1C4`, and calls `00861EC0(record+0xA0, 0, 0x100)` | `0051DB7C`, `0051DB97`, `0051DBA8`, `0051DBB5`, `0051DBBD` |
