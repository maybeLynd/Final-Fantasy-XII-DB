# Phyre member registrations the `regcalls` count and the field schema missed (OPUS, 2026-09-27)

This answers `ASTRA-RETURN-OPUS-PHYRE-ARRAY-REGISTRATION-SENTINEL` as the owner of the type store, the
`regcalls` instrument (`gen_phyre_descriptor_vtables.py`) and the two claims it supported.
- It is not independent acceptance; review is routed to SWE2-AUDIT-SPEC.
- ASTRA's sentinel package (`../phyre-array-registration-sentinel/`) is the counterexample this starts from.
- Its inputs and results are unchanged.

## Question and discriminators

**The question.** ASTRA's sentinel shows `PMeshInstanceSegmentContext` registering `m_streamBindings` through the array
constructor while `regcalls` reads 0. That raises four questions:
1. How many classes and members did the direct count hide?
2. What is the member's exact native type and width?
3. Which store rows and published claims change?

**The discriminators:**
- **The whole constructor family, found image-wide.** A constructor is a small body that installs a `PClassDataMember*`
  vtable by RTTI, is called rather than tail-jumped, and builds a node. That set is fixed before counting, rather than
  adding only the one wrapper the sentinel names.
- **The header from the member classes' own accessors.** Those accessors are shared across instantiations, so they fix the
  layout per instantiation, not per template name.

## Result (`check.py`, exit 0; `result.json` sha256 `abbf16e0…065a`, identical over two runs)

| Check | Observation |
|---|---|
| **C1** | There are five member-node constructors. Their call sites, and how many of those sites `phyre-field-schema.tsv` holds: `00632960` 682 / 682; `00632A70` 29 / 4; array `00632A10` 165 / 0; enum `00632BE0` 21 / 0; dynamic `00632B30` 1. `00633300` installs the dynamic vtable but is its destructor. |
| **C2** | The `regcalls` column reproduces on all 315 registrars, and the wrapper-aware count is never below it. All 176 covered classes stay ≥ 1. Of the 139 zeros, **19 register 25 array members** and **120 register no data member**. |
| **C3** | Of the 120, eight register only reflected *method* callers (`00632FB0` with `*Caller*` vtables). None reaches a member constructor within two calls. |
| **C4** | For all 25 registrations, name, offset, a6, a7 and a8 resolve, as does the template vtable the caller installs. `a7` selects the member class: 3 = `PhyreArray`, 4 = `PhyreSharray`, 2 = `ArrayDynamic`. |
| **C5** | All 59 `PClassDataMemberPhyreArray<T>` vtables share one accessor pair, `006065E0` / `006045B0`. All 10 `PhyreSharray<T>` vtables share `006065E0` / `0063B9B0`. All 71 `ArrayDynamic` vtables share `006065D0` / `00604580` (callbacks). The header bytes are asserted. |
| **C6** | `+0xF4` for `PMeshInstanceSegmentContext` is 0: arg 7 is 0 at `005D98AE` and at `006B850B`. |
| **C7** | `_types/fields.tsv` carries the 25 members, and `PInstancesComponent +0x18` is 16 bytes. |

**The native header of every `PArray<T>` / `PSharray<T>` instantiation that has a member vtable (16 bytes):**
- **`+0x0`: a u32 element count.**
  - Every reader strips bit 31.
  - When bit 31 is set, the buffer is kept from release: resize `005C8BF0` / `006C7A40` and adopt `0062A870` / `006A5950`
    release through `00584730` only when it is clear. An adopted caller buffer is stored with it set.
- **`+0x4`: untouched** by every accessor.
- **`+0x8`: the element pointer.**
  - For `PArray`, it is always the pointer.
  - For `PSharray`, it is the pointer above count 1, **the single element stored inline** at count 1, and null at 0.

**`m_streamBindings`:**
- native `+0x38`, 16 bytes, `PSharray<PMeshInstanceSegmentStreamBinding*>`, ending exactly at the class's `0x48` extent;
- `+0x28`–`+0x37` stays a declared gap;
- file offset 0 (ASTRA's `c1004` read) is a different representation and is not the native offset.

## Mutants (each rejects a wrong reading)

- **M1.** Drop `00632A10` from the constructor set, and the sentinel counts 0. This is the old false negative.
- **M2.** `PInstancesComponent +0x18` at 8 bytes is rejected. The accessor `006AF560` returns the member's *address*.
- **M3.** Taking the file offset 0 as the native offset is rejected; the registration passes `0x38`.

## Limits

- The check is static. It does not prove that the lazy, guarded registrars run in any scene.
- Element meaning is not claimed, and neither is the `+0x4` dword's purpose.
- `ArrayDynamic` widths are not given by reflection. `PString`'s rows stay unchanged.
- **186 registrations stay unharvested:** 140 array, 25 fixed-size and 21 enum. They are open as `RM-1`.

## Reproduce

```
python "Database/FFXII TZA/_experiments/evidence/phyre-array-member-registrations-opus/check.py"
```

Needs `pefile` and `capstone`, the certified EXE `73461d08…21f8`, `Tools/work/graph/functions.tsv`, and the published member
tables.

- Consumers: `_index/candidates/phyre-array-member-registrations-consumer-check.md`.
- **DB_GOAL=NOT_MET.**
