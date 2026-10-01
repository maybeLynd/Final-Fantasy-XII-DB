# SD-67: `PMeshInstanceSegmentContext::m_streamBindings` is a 16-byte `PSharray` of pointers at `+0x38` (OPUS, 2026-09-30)

Register row SD-67 was registered by SWE2-DATA (`the-file-schema-against-the-runtime-schema.md` §7). The file record
puts the member at file offset 0 and the native registration at `+0x38`, and the row asks for its native type and
width. This record is static. The checker is `sd67_stream_bindings.py` (output `sd67_stream_bindings.out`, `FAILS 0`).
It uses `Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**`Phyre::PSharray<const Phyre::PRendering::PMeshInstanceSegmentStreamBinding *>`, 16 bytes, at native `+0x38`.
Its elements are 8-byte pointers.**

- **F1: the registration call.** The only reference to the name string `"m_streamBindings"` (`00D4A1C0`) is the
  registration in `005E67C0`. It calls the array-member constructor `00632A10` with offset `0x38`, `0`, kind **4** and
  element size **8** (`005E6828`–`005E6840`), and an element type returned by `005EFE60`.
- **F2: what the constructor stores.** `00632A10` is `Phyre::PClassDataMemberArray`, by the RTTI of the vtable it
  installs (`00D58100`). It stores the kind at `+0x5C` and the element size at `+0x58`. Kind 4 is `PSharray`, as
  UQ-281 answered (kinds 1–4 are a fixed C array, a dynamic array through a pointer, `PArray` and `PSharray`).
- **F3: the element type and the width.** `005EFE60` builds the member's type descriptor, a static at `02CEC990`, via
  `00632D80`, with size **`0x10`** and alignment 8 (`005EFEF1` / `005EFEF9`). It installs vtable `00D4DD98`, whose RTTI
  name is `PClassDescriptorAbstract<PSharray<PEBV PMeshInstanceSegmentStreamBinding>>` (raw
  `.?AV?$PClassDescriptorAbstract@V?$PSharray@PEBVPMeshInstanceSegmentStreamBinding@PRendering@Phyre@@@Phyre@@@Phyre@@`).
  `PEBV` is the MSVC mangling of a 64-bit pointer to a const class.

**The two offsets are two layouts, not a contradiction.** File offset 0 is the serialized record's layout. `+0x38` is
where the native object keeps the 16-byte container.

## Limits (OPUS)

- **Inside the container.** The internal layout of the 16-byte `PSharray` (pointer and count, and in which order) is
  not read here.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
