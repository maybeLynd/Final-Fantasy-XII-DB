# PSharray's size follows its element: a by-value element is stored inline (OPUS, 2026-09-27)

**State: PENDING REVIEW.** The author is OPUS, which also wrote the claim it corrects (RM-1, the
`phyre-array-member-registrations-opus` package). Acceptance needs an independent reviewer; the control passing is not
acceptance.

**Question.** RM-1 carved every `PSharray<T>` member as a 16-byte header, and the type row gave `PSharray` the single
size `0x10`, because all ten `PClassDataMemberPhyreSharray` vtables share one accessor set. Shared accessors fix the
**header**. Do they also fix the **extent**?

**Answer: no.** A count-1 `PSharray` stores its one element **inline** at `+0x8`, so the object is
`8 + max(8, sizeof T)` (`psharray_extent.py`, static, certified EXE):

| check | observation |
|---|---|
| V1 | The nine `PSharray<T>` class descriptors state their size to `00632D80`. Seven are `0x10`: five pointer elements, `PEBV…StreamBinding*` and `uint`. `PSharray<PDataBlockBufferD3D11>` (`0066A849`) and `PSharray<PIndexDataBlockBufferD3D11>` (`0066AB99`) are **`0x50`**. |
| V2 | Both by-value element classes are `0x48`, from their own descriptor construction. |
| V3 | All nine sizes equal `8 + max(8, sizeof T)`. |
| V4 | `0066F970` / `0066FAB0` walk `m_buffers` of `PDataBlockD3D11` / `PIndexDataBlockD3D11`. The count is at `+0x20` / `+0x18`; at count one the base is the **inline address** `+0x28` / `+0x20`; the element stride is `i*9*8 = 0x48`; `m_dataSize` is read at `+0x78` / `+0x70`. |
| V5 | `m_buffers + 0x50` is the next registered member in both classes (`m_offsetInVertexBuffer +0x70`, `m_offsetInIndexBuffer +0x68`), with nothing registered between. |
| V6 | The shared accessor `0063B9B0` returns the address `+8` at count one and null at zero. The member address is `member[+0x48] − classdesc[+0xF4]`. The resize `006C7A40` never releases the inline address, or storage whose bit 31 is set. |
| N | The tile rule rejects a 16-byte by-value member followed by a 64-byte gap. It keeps the 16-byte pointer members (`PMeshInstanceSegmentContext +0x38`, `PPhysicsRigidBodyBase +0xB0`, `PLODLevel +0x8`). |
| S | Regression: the store and the page follow the inline extent. S FAILED before the patch. |

**Four separate things a PSharray row can mean**, answered separately:
- **Native layout.** This package: the header plus a union of `T*` and one inline `T`.
- **Serialized offsets.** The member address subtracts the class's `+0xF4` adjustment. The file schema's member order
  is another representation and is not used for any width here. `m_streamBindings`' file offset 0 versus native
  `+0x38` stays as recorded.
- **The ownership flag.** Bit 31 of the count keeps an adopted buffer from release, and an inline element is never
  released. This was already in the phyre-array package, and the resize is re-read here.
- **Element semantics.** Not claimed. The walkers pass each element's address to a device call together with a
  buffer-description argument. That is the call's argument shape, not a meaning for the element's `0x48` bytes.

**Not generalised.**
- `PArray`'s `0x10` is unanimous across its 60 descriptors. It has no inline arm, so it is unchanged.
- The six pointer members and the one `uint` member keep their 16-byte header: five as one row each, and
  `PMaterialSet`'s split word by word.
- No negative census is re-read as a wrapper miss because of this correction. The 120 registrars with no data member
  stay as the phyre-array package measured them.

**The earlier reading, kept and qualified.** On 2026-09-19 the type row read the 0x50 pair as "embeds its element
INLINE where the others hold it by pointer" and left the size UNRESOLVED. On 2026-09-27 RM-1 replaced that with one
`0x10`. The split was right. The reason was not: every instantiation embeds at count one, and only a by-value `T`
makes the embedded element wider than a pointer. Both earlier texts stay in the cells.

Affected: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
(§20: one size struck; a correction paragraph added) and `_index/OPEN-QUESTIONS.md` (RM-1, a correction sentence, the
status unchanged).

Also revised in the store:
- `PDataBlockD3D11 +0x20` and `PIndexDataBlockD3D11 +0x18` `m_buffers` go from 16 to 80 bytes. Each absorbs the 64-byte
  gap row behind it, and that row's meaning and evidence are kept verbatim inside it.
- `PSharray`'s size becomes `VARIABLE 8 + max(8, sizeof T)`.
- The `PSharray +0x8` `m_u` row is qualified as the pointer arm.

| consumer | action | agreement |
|---|---|---|
| `_types/fields.tsv`, the two `m_buffers` rows plus their absorbed gaps | widened, with the old evidence kept | revised-here |
| `_types/fields.tsv` `PSharray +0x8` | qualified | revised-here |
| `_types/types.tsv` `PSharray` size and evidence | `VARIABLE`, with the correction prepended | revised-here |
| member-registration page §20 | struck and corrected | revised-here |
| `_index/OPEN-QUESTIONS.md` RM-1 | a correction sentence; still ANSWERED | revised-here |
| `_experiments/evidence/phyre-array-member-registrations-opus/` | immutable receipt; its "16 bytes" statement covers the header and not the extent, and is superseded here, not edited | superseded-here |
| `_index/candidates/rm1-array-members/` | carve record left as run; this package is its follow-up | superseded-here |

**Regressions.**
- `types_index.py --validate`: 8200 fields (8202 − 2 absorbed), 0 errors, 0 gaps, 0 meaning-rung reviews.
- `check_census_widths.py`: 0 disagreements.
- `check_type_refs.py`: 0 dangling.
- `check_embed_overlap.py`: every control PASS. The Widget drift rule still reports 0. Its one parent/child report
  (BattleStatsRecord ← GambitConfig) concerns rows this package does not touch.
- `check_questions.py`: consistent.

**Run receipt.** Run verified at fe8f6fc8b: `psharray_extent.py` V1–V6, N and S PASS, FAILS 0; S FAILED before the
patch.

## Review completion (OPUS, 2026-09-28)

The four questions were re-asked against the actual instantiations: the types instantiated, the header bits, element
lifetime, and native versus serialized form. [`psharray_review.py`](psharray_review.py) is STATIC and refuses any image
but the certified one. Its checks are I1, I2, B1, B2, L1, L2, C1 and S, and it reports FAILS 0.

**A correction to this record: ten instantiations, not nine.** RTTI has ten `PClassDescriptorForType<PSharray<T>>`
(I1). The tenth is `PSharray<PString>`. Its descriptor `02CF9530` is built by `006316C0`, which writes the size `0x10`
at `+0x38`, the field `00632D80` also sizes. V1's registrar list was keyed on `00632D80`, so it missed that descriptor.
- `PString` is by value but 8 bytes wide: its array code strides 8 when it allocates, copies and tears down (I2).
- So `8 + max(8, sizeof T)` holds for all ten. Eight are `0x10`: the six pointer elements, `uint` and `PString`. The two
  D3D11 elements make `0x50`.
- **Controls (C1).** A fixed-16 rule fails on the D3D11 pair. A "by-value means wider" rule fails on `PString`.

**Header bits (B1, B2).**
- Across the ten resize and setter bodies, the only count bit operated on is bit 31. Bits 0-30 are the count.
- Bit 31 means **adopted storage**. The slot-8 setters, which the cluster-load fix-up calls, keep the caller's buffer
  for any count other than one and set bit 31. At count one they copy the element inline and store a plain 1.
- The resizes allocate owned storage and store the plain count. Old storage is freed only when it is neither inline
  nor adopted.
- The `+0x4` dword stays unassigned, as the plus4 record left it.

**Element lifetime (L1, L2), which differs by kind:**

| element | copy | destruction |
|---|---|---|
| pointer, `uint` | by value | none (not owned) |
| D3D11 buffer, `0x48` | field by field (`00661720`); the `TAsyncUpdate` vtable at `+0x28` is re-stored, not copied; no AddRef or Release | a resize never destroys a dropped element; the array does not manage the device buffers |
| `PString`, 8 B | deep copy (`001C19A0`: strlen, allocate, memcpy) | `001C2720` frees each buffer whose bit 0 is clear, only for owned (bit 31 clear) storage |

**Native versus serialized.** The file holds the elements out of line. The load fix-up zeroes the header, then the
setter either adopts the file's array (bit 31) or, at count one, copies the element inline. Adoption means the file's
out-of-line layout survives as native storage. The inline element is the one native-only arrangement.

Affected: `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md`
(section 20: "All nine" struck and corrected; the ownership bullet completed).

| consumer | action | agreement |
|---|---|---|
| `_types/types.tsv` `PSharray` size | ten instantiations; `PString` in the `0x10` group | revised-here |
| `_types/fields.tsv` `PSharray +0x000` `m_count` | bit-31 meaning (adopted storage), with the ten bodies as evidence | revised-here |
| `_types/fields.tsv` `PSharray +0x0008` `m_u` | element lifetime per kind; why RM-1's harvest lists nine | revised-here |
| page section 20 | struck and corrected | revised-here |
| the D3D11 element rows (`PDataBlockBufferD3D11`, `PIndexDataBlockBufferD3D11`) | already carved at exactly the widths `00661720` copies | agrees |

**Regressions.**
- `types_index.py --validate`: 795 types, 8311 fields, 0 errors, 0 gaps.
- `check_type_refs.py`: 0 dangling.
- `check_census_widths.py`: 0 disagreements.
- `psharray_extent.py`: FAILS 0 (unchanged).

**Run receipt.** Run verified at b8f336c1e: `psharray_review.py` FAILS 0. S FAILED before the patch.
