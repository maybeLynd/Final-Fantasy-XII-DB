---
system: The @FTR entry of .cm files - the model's node table, and where the FCP section-2 blob lands
category: 17-Presentation-Rendering
status: DOCUMENTED — flags, aux values, consumers and tail readers read (DD batches 10 and 14); bit 29's value is NO ADMISSIBLE SOURCE (SD-195) (owner re-status 2026-10-01, OPUS, on SWE2-CONTRACT's proposed line; documented_rule READY)
owner_layer: PrimaryOwner:Presentation
evidence_tier: 1
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: the binder 00372820, the sizer 003712E0, the field copiers 00409300/004094D0 and the
    wiring pass 003713C0 disassembled from the authority image and read whole; the authored layout
    they imply then re-parsed out of all 1,066 .cm files in the archive with every structural
    check passing (members/ftr_entry_census.py), 2026-09-28
last_reviewed: 2026-09-29
archive_formats:
  - "cm"
audit:
  passes: 1
  last_pass: 2026-09-29
  last_pass_kind: falsification
  last_pass_state: opus-ftr-node-table-falsification-pass-1
  note: written by SWE2-DATA as the UQ-218 @FTR slice, following on UQ-220 (which proved the FCP
    section-2 memcpy into this entry's tail); corrected 2026-09-28 on FABLE's
    uq218-cm-entry-residues record — the link field is a parent index (the entry
    is the model skeleton) and the +0x38 tailU16 count is the @FDM
    override-slot array bound. Authored layout, index-table encoding and runtime
    record sizing are code-proven and census-verified; the record
    flag vocabulary ~~is not established~~ is narrowed to the bits the bind
    path tests and the stream data each bit adds (2026-09-30, SWE2-CONTRACT
    DD batch 10, R1-R2). ~~Not read - the runtime consumers
    of the 0x290 records and of the relinked tail beyond the address pass.~~
    Read 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14,
    swe2contract-ddres-b14-0930) - what each aux-pool value is (G1-G6), the
    fields the located 0x290 consumers use (C1-C5) and the 28 readers of the
    +0x94 tail (C6). Bit 29's value has no reader, and the bones used as
    attachment points are named from outside the entry (B1-B2).
---

# The `@FTR` node table — and where FCP section 2 lands (SWE2-DATA)

A `.cm` carries a per-model **node table — the model skeleton**: `count` small records, each
naming its parent by a 12-bit index (one root, node 0, per file; parents always below their
child's index) and carrying a flag word that selects which parameters it draws from a shared
u32/f32 constant pool at the end of the entry. At load the engine expands it into a bigger
record array, threads the flagged records into a u16 index list, and then **appends the FCP
block's section-2 blob verbatim** and runs the shared section-address pass over the copy —
that blob is a serialized sub-structure whose embedded offsets are patched into pointers in
place (UQ-220 proven the copy; this page names the container and the pass).

## 1. The authored layout (kind 2 — every shipped entry) (SWE2-DATA)

```struct FtrEntry base=entry
+0x00  char[4]  tag        '@FTR'
+0x04  u32      kind       2 in 1,066 / 1,066 files (the kind-0 binder arm is dead code)
+0x08  u32      entryLen   bytes of the whole entry, header included
+0x0C  u32      count      node records
+0x10  char[32] name       model name, matches the file stem
+0x30  u32      count2     == count in 1,066 / 1,066 (duplicated)
+0x34  u32      auxOff     entry-relative offset of the shared u32/f32 constant pool
+0x38  u32      tailU16    count of the u16 override slots after the node list
                          (== the @FDM key count in 1,045/1,045 files; the
                          `00373060` bound)
+0x3C  u32      _zero      0 in 1,066 / 1,066
+0x40  u32[cnt] index      entry value = (recordByteOffset << 12) | ordinal;
                          low 12 bits equal the slot index in every record of every file
```

Records begin at `align16(0x40 + 4*count)` and tile up to `auxOff`; each is variable length:

```struct FtrRecord base=rec
+0x00  u32  link    bits 12..23 = PARENT record index; all-ones = the root
                   (corrected 2026-09-28 — see below); bits 0..11 unique per
                   file in 1,057/1,066, unread by the binder and the four
                   resolvers (a per-bone id, unproven); bits 24..31 = 0xFF in
                   27,561/27,561
                   [CORRECTED 2026-10-01, OPUS: bits 0..11 are not unread -
                   00409250 returns them as the record key when +0x04
                   bit 30 is clear; the tag search 003737C0 uses it]
+0x04  u32  flags   presence bitstream - which u16 indices follow at +0x08
+0x08  u16[] indexStream  each present slot contributes one u16 index into the aux pool
```

The flag bits the binder tests (`00409300` / `004094D0`, kind-2 arms):

| flag | effect on the runtime record |
|---|---|
| `0x40000000` (bit 30) | skip a leading u16 before the index stream |
| `0x00800000` / `0x01000000` / `0x02000000` (bits 23–25) | one u16 each → aux-pool u32 → out `+0x30` / `+0x34` / `+0x38` |
| `0x04000000` / `0x08000000` / `0x10000000` (bits 26–28) | one u16 each → aux-pool f32 → the vec3 passed to `0046D560` |
| `0x00200000` (bit 21) | in the second copier `004094D0`: ~~a fixed fan of ~16 u16 aux indices~~ *(corrected 2026-09-30, SWE2-CONTRACT DD batch 10, R1: exactly sixteen, copied as sixteen consecutive dwords of the aux pool into the copier's output, two passes of eight, `00409509`–`0040958D`)* |
| `0x00200100` together | the gate for the "rich" arm of `00409300`; otherwise `0046D110` defaults |
| `0x80000000` / `0x00400000` (bits 31, 22) | *added 2026-09-29 (OPUS falsification pass 1)*: in the rich arm each skips one more u16, bit 31 after bit 30's and bit 22 after bit 21's sixteen (`0040936A`..`00409385`); `004094D0` skips bit 31's too (`004094F5`). ~~Whether shipped records set them is the census's to say~~ *Corrected 2026-09-30 (SWE2-CONTRACT, DD batch 10, R2): they do. Bit 31 is set in 11,243 and bit 22 in 23,694 of the 27,561 records, so both skips run on shipped data* |
| `0x00000100` (bit 8) | record also gets the `00373DC0` init (identity transforms at `+0x1F0` / `+0x230`, cleared links at `+0x270`..`+0x27C`) **and its index is appended** to the u16 list after the record array — set on every record of every file (27,561 / 27,561) |

**Corrected 2026-09-28 (FABLE evidence record
`_index/candidates/uq218-cm-entry-residues/`, controls FAILS 0):** record
`+0x00` bits 12–23 are the **parent** index, not a "next" link. The binder
(`00372B15`–`00372B34`) stores them to the runtime `+0xB8`/`+0x270` parent
word and threads the runtime first-child `+0x274` / next-sibling `+0x272`
links under the parent (`00372B3B`–`00372B99`); a root joins node 0's
sibling chain. Data: exactly **one root per file, always node 0**
(1,066/1,066), and every other record's parent is **strictly below its own
index** (26,495/26,495) — a topologically ordered tree. So `@FTR` is the
**model skeleton**: the `0x290` records are the bone records the
`Skeleton_*` family already strides (~~71 functions stride `0x290` —
`imul290.txt`~~ **55 listed functions multiply an index by `0x290`; the other 16 in `imul290.txt` carry `0x290` as a stack frame,
a size or an offset (corrected 2026-09-29, OPUS falsification pass 1, `CON-181`)**), 27,561 bones over 1,066 models.

## 2. The runtime allocation (`003712E0` / `00372820`) (SWE2-DATA)

```
coreBytes = align16( (count * 0x149 + tailU16) * 2 )   ; the sizer's exact formula
alloc     = coreBytes + align16-padded ftrTailLen      ; ftrTailLen = FCP dword +0x24
```

`00372820` writes into the render-record:

| field | value |
|---|---|
| `+0x80` | ~~arena handle of the entry (`0020E620` of the `00409A30` lookup)~~ **the arena offset (`0020E620`, `x − [01F83530]`) of the core block the caller passes as the fifth argument (`00372944`); the `00409A30` lookup goes to `+0x1C` (`00372881`) (corrected 2026-09-29, OPUS falsification pass 1, `CON-181`)** |
| `+0x84` | ~~resolved pointer to the runtime core~~ **the arena offset of that block after `003AB7F0`'s live resolution (`00372977`..`00372986`) - a dword, not a pointer; readers turn it back with `0020E600` (corrected 2026-09-29, OPUS falsification pass 1, `CON-181`)** |
| `+0x88` | u16 `count` |
| `+0x8A` | u16 `count2` (`entry+0x30`) |
| `+0x90` | `coreBytes` (written only when the caller's block `[rsp + 0x80]` is non-zero, `00372962`; otherwise it keeps `r12d` from `0037291A`) |
| `+0x94` | ~~tail pointer = `core + coreBytes`~~ **the arena offset of `core + coreBytes` (`0037299A`..`003729A9`; corrected 2026-09-29, OPUS falsification pass 1, `CON-181`)** — where the FCP section-2 copy lands. *Precision (2026-09-29, OPUS, on SWE2-AUDIT-SPEC's batch-7 review): the `core` is the live-resolved `+0x84` block, not the caller's `+0x80` one; the sum is taken in 32 bits (`add eax, [rsi + 0x90]`), exact modulo 2^32. On the `[rsp + 0x80] == 0` path (`00372965`) `+0x84` is not written and `+0x94` keeps `0020E620(0)` from `0037290F`, the offset of NULL.* |
| `+0xB0` | matched-name index into the shared name table (`02AD9E30`, u16+stride 0x30) |

The core is **`count` records of `0x290` bytes followed by `count + tailU16` u16 slots**
(`count*0x292 + tailU16*2` bytes total). The bind loop walks the authored index table,
expands each record through `00409300` + `004094D0` (or `00373DC0` alone when only flag
`0x100` matters), threads links through runtime words `+0x270`/`+0x272`/`+0x274`, and
appends every flag-`0x100` record's index to the u16 region — which fills its first
`count` slots in all shipped data. **The remaining `tailU16` slots are the
`@FDM` override-slot array** (corrected 2026-09-28, FABLE record): `@FDM` key
count == `+0x38` in 1,045/1,045 files, `00373060` writes `w6` bounded by it,
`00371330` reads the pairs into the VU1 upload — see
`fdm-and-for-entries.md`. Sizes run 0–**1,188** (m1208; the earlier "0–363"
was a truncated census — 4 files exceed 363).

After the records are built, `memcpy(core + coreBytes, fcp + fcpSection2, ftrTailLen)`
(`003729B7`) appends the FCP section-2 blob, then `003E1C50` — the shared section-address
pass already documented in `resource-section-addressing.md` — walks the copy: its sub-record
`+0x68` / `+0x6C` u16s index the character render record array (`022C6F28`, stride `0x740`,
gated on `dword[+0x284]`), and `+0x70` / `+0x74` / `+0x78` dwords are rebased into pointers
through `0020E600` / `0020E620` and the `0040EEA0` / `00415A80` / `00421D20` helpers.

## 3. The dead kind-0 arm (SWE2-DATA)

When `dword[entry+4]` ~~`!= 2`~~ **is 0** *(corrected 2026-09-29, OPUS falsification pass 1, `CON-181`: kind 0 branches to `00372CBE`; any other non-2 kind
branches to `00372E84`, which builds no records and only fills the `0x7FFF` override slots)* the binder runs a second loop instead: records start at
`entry+0x30` with stride **`0x4C`**, links are `word[rec+0x20]`, and no aux pool is used.
No shipped `@FTR` has kind ≠ 2, so that arm is compiled but unreachable — same situation
as the FCP section-6 reader.

## 4. What is not established (SWE2-DATA)

- The node records' gameplay **semantics** — the record shape is now the
  skeleton's bone tree (parent link proven; `Skeleton_*` family strides
  `0x290`), but which bones carry attachments/effect markers vs. pure
  transforms is unproven. *(DD batch 10, SWE2-CONTRACT: ~~still open, and proposed as a register row for SWE2-DATA in
  the batch record.~~)* *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: answered (B1–B2). No bone record marks itself as an attachment point
  or a marker. The bind path reads only the parent link, the flag word and the transform stream. Other tables name the
  bones by index: FCP section 3's slot words (the attachment table, `0041EDE0` / `0041F010`), the special-bone ids
  that `003E5AD0` resolves (below `0x20` through the `u16` table at `+0x14C`; `0x104`–`0x106` from payload `+0x3A` /
  `+0x3C` / `+0x3E`), and the bone-trail descriptors, whose index `003711D0` checks against the skeleton's count
  `+0x88`. So the attachment bones are a per-model join of those tables, which
  [the FCP page](fcp-character-parameter-block.md) and
  [the bone-trails page](../Character-Render-Records/the-bone-trails.md) document. See the batch-14 section below.
- The aux pool's element vocabulary (mixed u32 scalars and f32s; values include `1.0` and
  mirrored bound pairs). *(DD batch 10, SWE2-CONTRACT: narrowed. The pool's type is set by the bit that reads a slot:
  bits 23–25 and bit 21's sixteen copy dwords, and bits 26–28 load floats (the section below). ~~What the values mean
  is still open, and proposed as a register row.~~)* *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: answered (G1–G6). Bits 23–25 are the bone's rest
  translation, bits 26–28 its rest rotation (three angles in radians), and bit 21's sixteen dwords its `+0x150`
  matrix. Bit 29's value is never read. The batch-14 section below gives the details.
- The FCP section-2 blob's internal structure after `003E1C50`'s fixups — its 19-slot
  offset table and 68-byte anchor are described in `fcp-character-parameter-block.md`;
  ~~its field semantics stay open (UQ-218 residue).~~ *(DD batch 10, SWE2-CONTRACT: that is the FCP page's question, ~~and
  it is proposed as a register row~~.)* *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: stale. `UQ-220` was answered on 2026-09-26 (FABLE, on
  [the FCP page](fcp-character-parameter-block.md)): section 2 is the character's rig, the table of seventeen
  controllers that hangs at the tail `+0x94`. Slot n is controller n, and the fixed record at `+0x4C` is the rig's
  header. What each controller's record holds is the open section 7 of
  [the rig page](../Character-Render-Records/the-rig-of-seventeen-controllers.md) (check D1).
- Runtime consumers of the `0x290` records and of the tail's resolved pointers. *(DD batch 10, SWE2-CONTRACT: the
  `0x290` consumers are located. They are the snapshot arm `0041C260` (`0041C2E5`), the pose pass `00373860`
  (`003738BE`, `00373974`) with its composer `00372610` (`00373B85`), and the readers named in
  [`fef-and-motion-entries.md`](fef-and-motion-entries.md) (the `@FMW` apply path and the skinning palette). ~~Which
  fields each one reads, and who reads the tail's resolved pointers, are proposed as a register row.~~)* *Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*:
  answered (C1–C6). The fields each consumer uses are in the batch-14 section below. On every route the census follows,
  the tail `+0x94` is written only by the binder and `003713C0`, and 28 functions read it. Each turns the offset back into the rig's address through
  `0020E600`.

## DD batch 10: the flag census and the record length (SWE2-CONTRACT for OPUS)

*For the player:* nothing is visible. For a modder, every bone record's length follows from its flag word by one
rule. A record that breaks the rule shifts every record after it, and the loader does not check.
The checks are in [`b10_checks.py`](../../_index/candidates/swe2contract-ddres-b10-0930/b10_checks.py) (R1–R3): static,
over all 1,066 `.cm` files of the extract. Control X1 re-decodes `m1132.cm` from the archive.

**Which bits the code tests (R1).** The binder `00372820` tests the authored flag word only for `0x100`. It does not
copy the word into the runtime record. The copiers test bits 30 and 31 (the two leading skips), the `0x200100` gate,
bit 21 (sixteen indices, `004094D0`), bit 22 (a skip), bits 23–25 (three dwords to `+0x30` / `+0x34` / `+0x38`) and
bits 26–28 (three floats to `0046D560`). **No body in the bind path tests bits 0–2, 9–19 or 29.**

**Which bits the files set, and the record length (R2).** Over the 27,561 records:
- bits 0, 8, 21 and 30 are set in every record;
- bits 3–7 and 20 are never set;
- bit 31 is set in 11,243, bit 22 in 23,694 and bit 29 in 1,953;
- 2,151 distinct flag words occur.

Every record except the last in each file is exactly `8 + 2 × (b30 + b31 + 16·b21 + b22 + b23 + … + b29)` bytes long,
padded to 4. The last record ends at the aux pool within its padding. So **bit 29 also carries one `u16`**: it is the
last one in the stream, the copiers stop before it, and nothing in the bind path reads it. Bits 0–2 and 9–19 add
nothing to the stream and no bind-path code tests them. They are flags whose reader, if any, is outside the bind
path.

**Runtime consumers located (R3).** `0041C260` strides the runtime records by `0x290` (`0041C2E5`) and works on
`+0xC0` / `+0x120` and `+0xF0`–`+0x10C`. `00373860` strides them twice (`003738BE`, `00373974`) and calls the
composer `00372610` (`00373B85`). ~~Their full field use is proposed as a register row (the batch record).~~
*Corrected 2026-09-30 (SWE2-CONTRACT for OPUS, DD batch 14)*: their field use is read in the batch-14 section below (C1–C5).

| claim | evidence | tier |
|---|---|---|
| the flag bits the bind path tests | R1 | 1 |
| which bits are set; the length rule, bit 29's unread `u16` | R2, all 27,561 records | 1 |
| two runtime consumers located | R3 | 1 |

## DD batch 14: the aux pool, the bone consumers and the tail readers (SWE2-CONTRACT for OPUS)

*For the player:* this is how a character's skeleton gets its resting pose. Each bone record says where the bone sits
and how it is turned before any animation plays, and it carries one matrix that the skinning uses. Animations then
overwrite the place and the turn every frame. In 1,953 bones the record carries one more value, close to 1.0, that the
game never uses. For a modder: changing a bone's bit 23–28 values moves or turns it at rest, and its bit-29 value can be
anything.

The checks are in [`b14_checks.py`](../../_index/candidates/swe2contract-ddres-b14-0930/b14_checks.py) (G1–G6, C1–C6, B1–B2, D1). They are static, and the
corpus is the 1,066 `.cm` files of the extract. Control Z1 re-decodes `m1132.cm` from the archive.

**Where the copiers write (G1–G5).** The binder hands `00409300` the record's `+0xC0` and `004094D0` its `+0x150`.
- `00409300`'s rich arm sets `+0xFC` to 1.0. It writes bits 23–25's dwords to `+0xF0` / `+0xF4` / `+0xF8`, which are
  zero when a bit is clear. Then it calls `0046D560(+0xC0, x, y, z)` with bits 26–28's floats.
- `0046D560` divides each angle by 2π, scales it by 32,768 and looks the sine and cosine up in `01F004E0`. That is the
  table and scale `0046D380` uses, the `@FMW` rotation channel. It writes rows 0–2 only.
- `004094D0` copies bit 21's sixteen dwords to `+0x150`–`+0x18F`. Without bit 21 it copies the identity (`0046D110`,
  `01F204E0`).
- The binder then copies the translation `+0xF0`–`+0xFC` to the `@FMW` staging `+0x1B0` and to the snapshot `+0x130`.
  It sets the scale vec4s `+0x100`, `+0x140` and `+0x1D0` to 1.0.

So bits 23–25 are the bone's rest translation (row 3 of its local matrix), bits 26–28 its rest rotation, and bit 21 its
`+0x150` matrix.

**The shipped values (G6).** Over the 27,561 records:
- every stream index lands inside the pool;
- all 36,871 rotation values lie in [−π, π], as radians would;
- the last column of every bit-21 matrix is (0, 0, 0, 1);
- bit 29's index lands inside the pool in all 1,953 records that set it. It names a float between 0.92 and 1.38, which
  is 1.0 (to four places) in 1,697. Nothing reads it, and the binder sets every bone's scale to 1.0, so what the value
  means has no code source: **SD-195**, NO ADMISSIBLE SOURCE (registered 2026-10-01, OPUS for SWE2-DATA).

**What each consumer uses (C1–C5).**

| consumer | reads | writes |
|---|---|---|
| snapshot arm `0041C260` | the local matrix `+0xC0` (through `0046D730`), `+0xF0`–`+0x10C` | `+0x120` (matrix), `+0x130`–`+0x14C` |
| pose pass `00373860` | the parent `+0x270`, the cross-skeleton parent `+0x276` with its remap index `+0x27E`, the flags `+0x280`, and the parent's `+0x80`. Its composer gets `+0xC0`, `+0x230`, `+0x100` and `+0x150`. When `+0x280` bit 4 is set it composes inline instead, from the same four plus `+0x1A0`, `+0xF0`, `+0x1C0`, `+0x1E0` and `+0x10C` | `+0x284` (the output handle), `+0x80` (the pose), and the matrix `+0x284` names |
| composer `00372610` | it composes the parent, `+0xC0` and `+0x230` into the pose. The pose's four rows, scaled by `+0x100`–`+0x10C` and composed with `+0x150`, give the output matrix | the pose and the output matrix (`02AD9E40`, `02AD9E80`), which `00373860` copies back |
| `@FMW` apply `00418880` | the staging groups `+0x190`, `+0x1A0`, `+0x1B0` and `+0x1D0`, and the flags `+0x280` / `+0x28A` | the local matrix `+0xC0`–`+0xFF` and the scale `+0x100`–`+0x10C` |
| skinning palette `003703A0` | `+0x150` and `+0x80` of the remapped bone | the palette entry (`renderRecord +0x6C0`) |

**Who reads the tail (C6).** A census from both skeleton pools (the render root's `+0xD98` and an entry's `+0x330`)
followed calls three deep. On those routes it finds `+0x94` written only by `00372820` and `003713C0`, which is its
control, and read by 28 functions at 104 sites. Every read loads `ecx` and resolves it through `0020E600`, turning the arena offset back into
the rig's address. `003713C0` hands the result to `003E1C50`, the address pass. The other readers are the rig's users,
most of them named on [the rig page](../Character-Render-Records/the-rig-of-seventeen-controllers.md): `003703A0`,
`00370E20`, `00372710`, `003B8260`, `003E6DF0`, `003E6F90`, `003E7040`, `00417F40`, `0041D220`, `0041D560`,
`0041DD40`, `004213E0`, `004215A0`, `00421B00`, `00422940`, `00427320`, `0042BDE0`, `0042BED0`, `0042C410`,
`0042C8F0`, `0042D8B0`, `0042DCD0`, `0042DD90`, `0042E690`, `005201B0`, `00520320` and `00520E90`.

**Which bones carry attachments (B1–B2).** None says so itself. The bind path reads only the parent link, the flag
word and the transform stream. The tables listed in section 4 name the bones by index.

**FCP section 2 (D1)** is the rig. `UQ-220` answered that on 2026-09-26, as section 4 now notes.

**Not settled, and why.** Bit 29's value has no reader, so what it names has no admissible static source. A proposed
register row in [the batch record](../../_index/candidates/swe2contract-ddres-b14-0930/README.md) records this.

| claim | evidence | tier |
|---|---|---|
| bits 23–25 = rest translation, 26–28 = rest rotation, bit 21 = the `+0x150` matrix | G1–G5 | 1 |
| the shipped values fit (all 27,561 records); bit 29's value range | G6 | 1 |
| each located consumer's fields | C1–C5 | 1 |
| the `+0x94` writers and its 28 readers | C6 (census, call depth 3, control) | 1 |
| attachment bones are named outside the entry | B1–B2 | 1 |

## Evidence (SWE2-DATA)

`members/ftr_entry_census.py` re-derives every structural claim above from the archive:
kind `2`, `count2 == count`, index low-12 = ordinal, records inside `[align16, auxOff)`,
aux size divisible by 4 — each `1,066 / 1,066`. Functions read whole from the authority
image: `003712E0` (sizing), `00372820` (bind + tail copy), `003713C0` (wiring +
`003E1C50` hand-off), `00409300` / `004094D0` (kind-2 field copiers), `00373DC0`
(flagged-record init), `004095A0` (`ecx+0x40` index-table accessor).

## Falsification pass 1 — 2026-09-29 (OPUS): the sizer, flags, tree and tail survive; the field table's representation, the dead arm and the stride count do not

**Attack.** Sections 1 to 3 and the correction box were turned into checks at their instructions. The competing case
was re-counted from a fresh sweep: FABLE's stride list against the listed bodies. Script:
`Tools/analysis-kit/gfz-scripts/falsify_ftr_node_table.py`, output `falsify_ftr_node_table.out`, image `73461d08…`,
0 BROKEN, exit 0. Carried, not re-run: the 1,066-file census and FABLE's parent-tree controls.

| # | Clause attacked | Result |
|---|---|---|
| N3 | section 2: "`+0x80` arena handle of the entry (`0020E620` of the `00409A30` lookup)", "`+0x84` resolved pointer", "`+0x94` tail pointer" | **refuted** (`CON-181`). The lookup is stored at `+0x1C`. The three fields are dword arena offsets (`x − [01F83530]`) of the caller's core block, of its live resolution, and of `core + coreBytes` |
| N8 | section 3: "`!= 2` → a second loop" | **refuted** (`CON-181`). Only kind 0 runs the `0x4C` loop. Other non-2 kinds build no records |
| N10 | the correction box: "71 functions stride `0x290`" | **refuted** (`CON-181`). 55 listed bodies multiply by `0x290`. The other 16 hold it as a stack frame (12), a size or an offset |
| N5 | section 1's flag table | **omission, added**: bits 31 and 22 each skip one more u16 in the rich arm, and `004094D0` skips bit 31's |
| N0 | sizes | **survives**: all ten |
| N1 | the sizer | **survives**: `align16((count × 0x149 + u16 +0x38) × 2)` plus the fifth argument |
| N2 | the field table's other rows | **survives**: `+0x88`, `+0x8A`, `+0x90`, `+0xB0` (stride `0x30`); the tail copy at `core + coreBytes` |
| N4 | the flag table's listed bits | **survives**: bit 30, the `0x200100` gate, bits 23–25 and 26–28, bit 21's sixteen |
| N6 | `00373DC0` | **survives** |
| N7 | the parent tree | **survives**: parent at record `+0x270`, first child `+0x274`, next sibling `+0x272`; roots on record 0's chain |
| N9 | `003E1C50` | **survives**: the `0x740` index on `[022C6F28]` gated on `+0x284`; `+0x70` / `+0x74` / `+0x78` rebased; the three helpers |

Corrected in place: section 2's field table, section 3 and the correction box, plus one added flag row. FABLE's
evidence record is routed, not edited. The consumer record is `_index/candidates/ftr-node-table-falsification-pass-1-0929/`.

## Cross-subsystem neighbours — SWE2-STRUCT (pass-22 dispositions)

- **Resource - CLIENT and SERVICE (27 edges).** `003AB7F0`, ResourceEntry_FindSectionOffsetByTagAndName (`00409A30`) are called by bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), ResourceEntry_GetResolvedBasePointer (`00409600`), ResourceEntry_FindSectionIndexAndOffset (`00409780`), `00409A60` (+9 more); `003712E0`, `00371330`, `003713C0`, `00372820` (+3 more) reach bodies filed to Resource: ResourceTable_ResolveEntryByIndex (`002ED570`), ResourceEntry_FindSectionPointerByTagAndName (`00409660`), ResourceEntry_ResolveSectionOffset (`004096C0`), ResourceEntry_FindSectionIndexAndOffset (`00409780`) (+2 more) - shared machinery across the layer boundary, no shared ownership.
