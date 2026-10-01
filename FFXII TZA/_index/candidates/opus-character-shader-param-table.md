# CharacterShaderParamTable (0x318) declared; the object's +0x78 unit is the same table (OPUS, 2026-09-26)

**Evidence class: STATIC**, shipping image (sha256 `73461d08…21f8`). Independent review is requested (author OPUS).

## What was already known, and by whom

- **The slot map.** `001F7790` is the character material's shader-parameter binder (BB-7, FABLE 2026-09-14). The
  map from its 92 `FindShaderParameter` (`0018D240`) results to slots `+0x30`..`+0x310` was emitted on 2026-09-21
  (OPUS) in `17-Presentation-Rendering/Character-Rendering/shader-binding-record-0x318-slots.tsv`, and a re-extraction
  today matches it slot for slot. The record's `+0x00` (the binder's first argument, the owner of the parameter data
  block) is UQ-202 (OPUS, 2026-09-21).
- **The two z-bias banks** (entry `+0x08`/`+0x0C` and `+0x10`/`+0x14`) are UQ-201 (FABLE, 2026-09-25).
- **The `+0x78` unit.** The object's `+0x78`..`+0x38F` is one 792-byte unit that the constructor zero-builds and
  copies in (the page's section of 2026-09-18). That section explicitly left what those bytes mean open.

## What is new here

1. **The type is declared in the store.** Until now `CharacterRenderObject +0x58` read *"the 792-byte record is an
   undeclared type"*. `CharacterShaderParamTable` (0x318, `TYPE RESOLVED`, L1) now has 99 rows:
   - `+0x00` the data-block owner;
   - `+0x08`..`+0x14` the two z-bias banks;
   - 92 named parameter handles;
   - two declared gaps: `+0x18` (24 bytes), and `+0x238` (the one qword in the handle run that the binder does not
     fill; it goes from `cubeMapEnabled` at `+0x230` to `eTp` at `+0x240`).
2. **The object's `+0x78` unit is this table.** The binder's first call site in `001F6E70` passes
   `r9 = [rsp+0x48] + 0x78` (`001F70DE`-`001F70F3`), and `[rsp+0x48]` is the object (`001F7087`-`001F708C` read its
   `+0x50`). So the zero-built 792 bytes are the object's own parameter-handle table. The six rows that described them
   piecemeal become one embedded row, and their facts carry over:
   - `writeBufferPtr78` is table `+0x00`;
   - `writeIndexSourcePtr110` is table `+0x98`, the `lichtAmbient` handle;
   - `floatBlock0088` / `copiedTail0108` are the constructor's copy lanes;
   - `block0118` is the handles the binder writes.
3. **The second call site.** `001F74F6` passes a stack table (`rsp+0xA0`), with an existing vector element as the
   template (`001F74C0`-`001F74EE`). That is how new elements of the `+0x58` vector are built.
4. **A representation split in `BootSingleton01F7F598`.** Its `+0x1C` was one `uint16` row "read as a byte". But the
   **writer** tests byte `+0x1C` (`001FB1B1`) and the **uploader** tests byte `+0x1D` on its own (`001FAD8B`), so they
   are two byte fields. The constructor still zeroes them as one word.
   - *Precision note for the page's UQ-201 answer:* it says the uploader's bank is chosen by `+0x1D` "as for the
     writer". The writer uses `+0x1C`.

## The handle and the binder

- **`0018D240(effect, name)`.** It searches the effect's two lists of 0x18-byte parameter entries (count/base at
  `+0x40`/`+0x48`, then `+0x50`/`+0x58`), comparing the entry's name at `+0x08` (a tagged pointer), and returns the
  entry or null. Users take the entry's word `+0x10` as the parameter's byte offset into the data block. Example:
  `001F6065`-`001F60A1` bound-checks `offset + (word+0x12 & mask)` against the block's size dword, then reads.
- **`001F7790(owner, effect, dataBlock, table, template)`:**
  - stores `owner` at `+0x00` (`001F8452`);
  - zeroes `+0x08..+0x17` (`001F8447`, `001F844E`);
  - with a template, copies `6 × 0x80 + 0x18` bytes from it;
  - otherwise performs the 98 lookups (92 stored; the six `…SamplerSampler` names are bound as samplers);
  - writes the parameters' default values into the data block.

## Census

A small taint scan, from every `imul …, 0x318` site through `add r, [obj+0x58]` (19 functions), reaches `+0x00`,
`+0x08`..`+0x14` and 32 of the 92 handle slots. That is a lower bound. The handle slots are otherwise read through the table's
base, and the binder writes every one.

`types_index.py --validate`: 782 types, 0 errors, 0 gaps. `check_storage_class.py`: 0 hard failures.

## Not claimed

- what any parameter does in the shader beyond its name;
- what `BootSingleton01F7F598 +0x1C`/`+0x1D` are beyond the bank tests (a writer/reader double-buffer pair is
  consistent with them, but their writers were not identified);
- the contents of `+0x18`..`+0x2F`.
