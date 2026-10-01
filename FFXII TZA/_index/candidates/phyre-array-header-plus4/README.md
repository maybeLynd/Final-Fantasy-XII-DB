# The Phyre array header's `+0x4` dword, and which array functions are shared (OPUS, 2026-09-27)

**State: PENDING REVIEW.** This is board task OPUS-STRUCT-PHYRE-ARRAY-PLUS4. The control passing is not acceptance;
an independent reviewer is requested.

**Question.** Both `PArray` and `PSharray` rows carried `+0x4` as a DISCOVERED `u8[4]`, with "no accessor touches
it". Is that dword a field that some other path reads or writes, such as serialization, the loader or a resize, or is
it unused space between the u32 count and the 8-aligned pointer?

**Result** (`plus4_check.py`, static, certified EXE):

| check | observation |
|---|---|
| Q1 | The 59 `PhyreArray` and 10 `PhyreSharray` member vtables share slots 4, 6 and 7, the count and element accessors. Slots 5 and 8, resize and set-from-buffer, are **per element type**: `PArray` has 45 resizes and 21 setters, `PSharray` five of each. |
| Q2 | A register-offset trace starts from the field address that all 79 slot entries compute (`object + member[+0x48] − class[+0xF4]`) and follows tail targets and callees. It finds 636 header accesses and **none at `+0x4`**. Controls: it sees the `+0` count, the `+8` pointer and the `+0x48` inline copy. |
| Q2c | The same trace **does** report a seeded `+4` write (`0057DAD0` with rcx = header − 8), so the absence in Q2 is not blindness. |
| Q3 | An image-wide census of 812 bit-31 count loads (475 with a `+8` access nearby) finds `+4` accesses only in four non-array functions: an item-record bitfield merge and a tagged-chunk walker. |
| Q4 | The cluster-load array fix-up `0059C250` stores a zero **qword** at the field (`0059C5E8`) and only then calls the slot-8 setter (`0059C5FC`), which writes `+0` and `+8`. After a load, `+0x4` is 0. |
| Q5 | The by-value setter `00672F30` copies the whole `0x48`-byte `PDataBlockBufferD3D11` inline at count one, which corroborates 3d95e439c. It stores the `TAsyncUpdate<PDataBlockD3D11>` vtable (`00D68DD0`) at element `+0x28`. |
| S | Regression: both `+0x4` rows, the `PSharray +0x8` row and page §20 follow the result. S FAILED before the patch. |

**Kept separate:**
- **Native layout.** `+0x4` is four bytes the accessors never use, and the load path zeroes them.
- **Serialized form.** The loaded object's bytes come from the file, but the fix-up overwrites `+0..+7` before use, so
  whatever the file held at `+4` is discarded for every fixed-up array.
- **Ownership.** Unaffected: bit 31 lives in the count.
- **Meaning.** None is claimed. Alignment padding fits every observation; that is a reading, not a proof. Indirect
  accesses and code outside the trace are not covered, and the create path's bytes (copied from each class's default
  instance) are not read here.

**Also corrected.** The phyre-array package and page §20 named `005C8BF0` / `006C7A40` / `0062A870` / `006A5950` as "the"
resizes and adopts. Those are single families' functions. Slots 5 and 8 vary by element, and my own RM-1-era wording
generalised one family to the template. The immutable evidence package stays as run; this record supersedes that
sentence.

**Not changed.** Both `+0x4` rows stay DISCOVERED and keep their name and `u8[4]` type. A cleared, unread dword is not
a semantic answer.

**Next obligation noticed, not taken here.** `PDataBlockBufferD3D11` (0x48) is a single unobserved span in the store.
`00672F30` and `0066F970` give it representation evidence:
- `+0x00` receives a device-created buffer pointer;
- `+0x28` holds an embedded `TAsyncUpdate<PDataBlockD3D11>` vtable;
- `+0x40` is zeroed at creation.

Affected: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
(§20: one sentence struck and corrected, the `+0x4` bullet extended, a closing note added).

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv` `PArray +0x0004`, `PSharray +0x0004` | the zeroing fix-up and the reach stated; still DISCOVERED | revised-here |
| `_types/fields.tsv` `PSharray +0x0008` | the per-element resize and setter list | revised-here |
| member-registration page §20 | the "the resizes / adopts" sentence struck; the `+0x4` note added | revised-here |
| `_experiments/evidence/phyre-array-member-registrations-opus/` | immutable; its shared-resize sentence is superseded here | superseded-here |

**Regressions.**
- `types_index.py --validate`: 8200 fields, 0 errors.
- `check_type_refs.py`: 0 dangling.
- `check_census_widths.py`: 0 disagreements.
- `check_questions.py`: consistent.
- `psharray_extent.py`: FAILS 0.

**Run receipt.** Run verified at 64c2d929d: `plus4_check.py` Q1, Q2, Q2c, Q3, Q4, Q5 and S PASS, FAILS 0. S FAILED
before the patch.
