# UQ-218 residue - .cm entries @FTE / @FCT / @FDM / @FEF / @FTR (read-only research, 2026-09-27)

Exe: Database/Tools/work/exe/FFXII_TZA.exe, base 0x120000, section-aware reads (lib.py `va2off`).
Corpus: 1,066 .cm under D:/FFXII_TZA_extract/ps2data/obj_finish/in (census0.py: @FCP 1066, @FCT 1044,
@FDM 1045, @FEF 144, @FMC 209, @FMN 111, @FMW 111, @FOR 1066, @FTE 1044, @FTR 1066).
Controls: controls.py -> controls.out, **FAILS 0** (16 checks, 5 of them defect-sensitive mutants or negatives).
One control failed on its first run and exposed a page error, see "Page corrections" below.

## Task 1 - @FTE: ANSWERED (STATIC + DATA)

Reader: the one draw builder 0053AB50 (called twice from 0053D780) plus the texture-resource
filler 00504520. `FTE = rec+0x1F8 + dword[rec+0x218]` at 0053B2BE/0053B306; record address
`((idx+2)<<5) + FTE` at 0053B6C3..0053B6CB, i.e. **records are 0x20 bytes from +0x40**.

- **Multi-texture cadence**: `count` x 0x20-byte descriptors, then every payload in record order.
  dataOff chain contiguous 2,127/2,127, payloads end exactly at entryLen 1,044/1,044.
  (The page's single "+0x40 texture record" with pixels after it is the count=1 case.)
- **"+0x4C dword"** = record-0 `+0x0C` u16 **RRH** and `+0x0E` u16 **DPSM** of the GS upload.
  00504520 copies +0x0A/+0x0C/+0x0E to pool +0x26/+0x28/+0x2A (00504589..0050459D); the builder
  reloads them (0053B739..0053B75D) and packs BITBLTBUF (reg 0x50: DBW = +0x0A>>6 min 1, DPSM = +0x0E,
  0053B826..0053B854) and TRXREG (reg 0x52: RRW = +0x0A, RRH = +0x0C, 0053B85B..0053B8A7).
  DATA: `+0x14 == +0x0A * +0x0C * 4` in 2,127/2,127; `+0x0E == 0` (PSMCT32) in 2,127/2,127.
  So **u16 +0x4A is not a palette count** (page wording) - it is the upload width.
- **Format word +0x08**: census over ALL records (not only record 0): **0x13 = 2,081, 0x14 = 46, nothing else.**
  Reader: 005045B4 -> pool +0x22 -> 0053BF8A, packed into TEX0 bits 20-25 (0053BFD7). No switch on it:
  it is the GS PSM code passed through (0x13 PSMT8, 0x14 PSMT4). The image-wide compare search for a
  PSM switch (psm_*.txt) found only 002FA560, a 0..0x1B dispatcher unrelated to textures.
  Data join: PSMT4 records pair with a 16-colour CLUT (36) or a 256-colour 8x32 CLUT (10).
- Other fields: +0x00 = VRAM bytes reserved (00537AA0 bottom-up allocator, pool 02EBA460, top
  0x3C0000; multiple of 0x2000 in 2,127/2,127); +0x10 unread and 0; +0x14 upload bytes; +0x18 payload
  offset; +0x1C = texture-cache key (00521290 / 005210F0, 256 slots x 0x30 at [02CA8450], refcount +0x24).
  Key form: prefix letter<<24 | set number<<4 | record index; 87 ids occur in more than one file (80 with identical payloads).
- Header `u8 +0x30` list: the textures uploaded unconditionally, seeded into the frame list before the
  @FOR table-B picks (0053B45A..0053B48A); values < count in 1,044/1,044.

## Task 2 - @FCT: ANSWERED (STATIC + DATA)

Readers (the `dword[rec+0x21C]` / `cmp -1` idiom finds exactly three): 005044D0, 00504D30, 0053AB50.
Record = 0x10 bytes from +0x30 (0053BB4D..0053BB59).

- +0x00 u16 = 0x2000 (1,972/1,972) = **VRAM bytes per CLUT**, allocated top-down: 00537AA0(1, v, 1) at
  0053BB73; summed with the @FTE reservations for the 00537AF0 fit test (0053B620..0053B67E).
- +0x04 u8 = CLUT upload RRW / DBW source (0053BC16..0053BC27, 0053BC8E); +0x06 u16 = RRH (0053BC92).
  `rrw*rrh*4 == clutBytes` 1,972/1,972.
- **+0x05 u8 = page count** (4 in 1,972/1,972): the builder clamps `s8[rec+0xBA]` to `v-1` (0053BB5D..0053BB68).
- +0x08 u32: no read found in the three readers; equals the same-index @FTE id in 1,911/1,972.
- +0x0C u32 = payload offset. **Payload = 4 pages of clutBytes, selected by render-record byte +0xBA**:
  005044D0 returns `entry + off + s8[rec+0xBA] * clutBytes` (005044F8..0050450D). Neither mips nor GS pages.
  +0xBA is written only by the setter 00504D20 (7 B), called by 00428CD0 (twice) and 0042E520. The
  status-look page (how-a-status-shows-on-a-character.md) already names +0xBA the "record mode", and
  Stone as mode 3. With mode 3, 0053BD30 skips the palette-resource copy path and uploads the page directly.
- DATA join: **page 3 is grey in 1,914/1,970** (mean chroma 1.6, against 30.6 for page 0). Pages 1 and 2
  are brighter (luminance 98.7/98.3 against 78.9), and page 2 is desaturated (chroma 21.4). Every page
  1-3 differs from page 0 (1,970/1,970). So page 3 = the Stone palette. Pages 1 and 2 are the variants
  the status looks select (the status page gives mode 2 for the HP-critical/Doom flash frames).
- Anomaly: 10 records (hc1005_0x, hc1006_0x, hn1164_01; PSMT4 textures with a 0x400 CLUT) have a
  0x100 span to the next record, so their 4-page windows overlap the following palettes. 2 records'
  4-page windows run past the entry end (fct_pages measured 1,970 of 1,972).

## Task 3 - @FDM w2/w4/w6 source: ANSWERED, and its sink resolved (STATIC + DATA)

- Producer (prior art, re-read): authored presentation **command 0x14** (7,193, event blocks only) ->
  00520E70 -> 00521050 (its only reference is the `lea` at 00520E7A) -> 005048A0 / 00373060.
- **Sink, new**: 00373060(res, ordinal, w6) bounds the ordinal by the **@FTR `+0x38` count** (003730BA).
  It writes w6 into u16 slot `core + count*0x292 + 2*ordinal`, which is the @FTR "tailU16" region.
  0x7FFF is stored without a flag; any other value also sets `res dword[+0] |= 0x1000` (003730C2..003730D6).
  00372820 initialises every slot to 0x7FFF and clears 0x1000 (00372F26..00372F45); 00372510 resets the same way.
- **DATA join: the @FDM key count equals @FTR u32 +0x38 in 1,045/1,045 files**, and +0x38 is 0 in all
  21 files without @FDM. Control mutant: key count == @FTR node count holds in only 148/1,045.
- Reader of the slots: 00371330 (called only at 0053C36F / 0053C3AD). For each @FDM part record the
  builder takes `slotA = (dword[+4] >> 8) & 0x3FF` and `slotB = (dword[+4] >> 18) & 0x3FF` (0x3FF = none).
  Only while res flag 0x1000 is set, it replaces the part's authored defaults `s8 +2` / `s8 +3` with the
  slot values (0053C34C..0053C3CF). It hands them to 0053D4B0, which uploads them to VU1 through a VIF
  UNPACK V4-32 (0x6C020041) row `{bit0, A|B != 0, B, A}` (0053D50F..0053D57A).
  DATA: every slot field < +0x38 (20,913/20,913). slotB is absent in exactly the 3,175 records whose
  bit0 = 0 (and bit29 = 0); bit28 is set in all 12,044.
- So an event's 0x14 command sets a per-model, key-addressed pair of integers on chosen draw parts.
  **Not established:** what the VU1 program does with the pair (texture-offset/expression-style use
  would fit the shape, but no VU1 microcode was read), and which commands run in play.

## Task 4 - @FEF: FORMAT CONFIRMED; consumer NARROWED (DATA + partial STATIC)

- DATA (144/144): one @FEF per file, always entry index 6 of 7 and the last. kind 0, +0x0C = 1, name ==
  basename (zero-filled), **"EFX0010\0" at +0x30, f32 1.0 at +0x38, and u32 at +0x3C == entryLen - 0x30**
  (the EFX file's own size fills the rest of the entry). The entry ends exactly at the @FRP length.
  Dirs: monster 82, npc 27, summon 26, gadget 9.
- 00504940 (called from 00504F00 at 00505026) resolves the @FEF sub-record into rec+0x230
  (005049A2..005049A7) and calls `0016D6A0(dword[file+0x44], FEF+0x30)` (005049B3..005049BD).
  **0016D6A0 is `ret 0` (C2 00 00, checked in controls)**, so on this path the embedded EFX pointer
  reaches a stub.
- 00409FE0 (via 0041E580; callers 002E4DB4, 002E4EFA, 003DC371, 003DD8AB) gates on the @FEF lookup
  (0040A0A4..0040A0B4). It then parses the container name's last five characters into a letter+number
  index into the pointer table 02B64380 (a null entry faults, 0040A135) and builds an EFX context with
  `003B38B0(source, offset)` at 0040A174, storing the handle at resource +0x44 (the same +0x44 that
  00504940 passes). It also parses "chara\h" + "%d.efx" (strings at 00D122F0 / 00D122F8) into
  003B3B10. **Not established:** whether that source+offset is the embedded @FEF. The offset is the
  dword at `source + roundup64(size) - 4` (0040A15F..0040A16F), and no .cm dword equals the EFX file
  offset in 143/144 files. External effect files exist at ps2data/effect_finish/jp/chara/h*.efx
  (126 files).

## Task 5 - @FTR: NARROWED (node = bone; the link is a PARENT; tailU16 answered)

- The authored `link` bits 12-23 are stored to runtime +0x270 (00372B15..00372B34) and threaded as
  first-child +0x274 / next-sibling +0x272 under the parent (00372B3B..00372B99); a root joins node 0's
  sibling chain. DATA: exactly one root per file, always node 0 (1,066/1,066). Every other link is
  < its own index (26,495/26,495), so this is a topologically ordered tree. Mutant (low 12 bits as parent): 3,700/26,495.
  So the page's "next record index ... a sibling order" is wrong: it is a parent index.
- The 0x290 runtime records are already named bone records by prior art (the Skeleton_* family:
  003703A0, 00373860, 003714A0, 00514F20, 003E3C30, 00373F40); 71 functions stride 0x290
  (imul290.txt). *(Count annotated 2026-09-29, FABLE, on OPUS's CON-181 `ee21b57cb`: of the 71 functions imul290.txt lists, 55 multiply an index by 0x290; the other 16 carry 0x290 as a stack frame (12), a size argument or an offset, and three rows also count add-strides. The bone-record naming rests on the Skeleton_* bodies, not on the count. Regression: falsify_ftr_node_table.py N10.)* With the parent tree that makes @FTR the model skeleton, 27,561 bones over 1,066 models.
- tailU16 (+0x38) = the @FDM override-slot array (task 3). Max 1188 (m1208); 4 files exceed 363.
- Link bits 0-11: unique within the file in 1,057/1,066. Unread by the binder and by the other four
  @FTR-entry resolvers (00371330, 003713C0, 00372510, 00373060, found by the `+0x1C` -> 004096C0 idiom).
  A per-bone id is plausible but not established. Bits 24-31 = 0xFF in 27,561/27,561.
- **Not reached:** the aux pool vocabulary (00409300 / 004094D0 arms).

## Page corrections found (for the owner, not applied)

1. fte-fct page: `u16 +0x4A` is not a palette count (it is TRXREG.RRW). The record is 0x20 bytes and
   the "+0x4C dword" is RRH + DPSM. The FCT `+0x00 flags = 0x2000` is a VRAM reservation, and
   "+0x04..+0x0F params" are RRW / pages / RRH / id / payloadOff.
2. fte-fct page: the "two inlined copies at 00532Cxx / 005339xx" are qword loads of `[rbp + 0x218]`
   (a frame local) in 005325D0 / 00533250. The builder's frame buffers +0x83B0/+0x8430/+0x8530
   occur only in 0053AB50 (22 lines).
3. fdm-and-for page: `00D10824` is **1.0e8f** (bytes 20 BC BE 4C), not 9.99e7.
4. ftr page: "tailU16 sizes run 0-363": the max is 1188 (m1208), and 4 files exceed 363. The "next"
   link is a parent link.

## Limits

- Reader claims come from the y1p_all.txt cache (direct E8/E9 calls, rip refs, the `-1` idiom). They
  are not an image-wide jcc/thunk sweep. "No read found" for FCT +0x08, FTE +0x10 and FTR link bits
  0-11 are scoped to the named readers.
- The palette page meanings rest on one code fact (mode 3 = Stone, prior art) plus a colour statistic.
  Page 1's use is not tied to a setter value: the setters seen pass 0, 2, 3 and byte[+0x235].
- No runtime observation was made. Everything is static reading plus file census.

## Files
lib.py (exe + corpus helpers) - census0.py - fte_fct_census.py/.out - fte_sizes.py/.out -
fte_idform.py/.out - fct_pages.py/.out - fdm_slots.py/.out - fef_census.py/.out - ftr_census.py/.out -
controls.py/.out - d_0053AB50.txt, d_00372820.txt, d_0053D4B0.txt (disassembly extracts) - imul290.txt -
fte.tsv fct.tsv fdm.tsv fef.tsv ftr.tsv
