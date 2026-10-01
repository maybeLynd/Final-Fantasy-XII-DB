# Static gap-row audit: do "unobserved" rows on STATIC/ARRAY types hide direct references? (OPUS, 2026-09-25, block 255)

**Why.** Block 254 found one of my own 2026-09-22 rows (`EeVu0RegisterBank +0x224`, 100 bytes) declared
"not reached by the census" although about 70 instructions reference it directly. If that census missed
rip-relative access into an object's interior, other gap rows could be wrong in the same way. This checks all of
them.

**Instrument.** `gap_rows_audit.py`: every DISCOVERED gap row, meaning an `unobserved*` / `gap*` / `pad*` name or a
"no censused access" / "not reached" / "no observed access" meaning, on a type with a `STATIC` route or a numeric
`ARRAY` route. For each, it asks whether any rip-relative operand in any function body targets a byte inside the
row, in any array element. It uses the existing `data_xref_scan.scan`; it is not a new scanner.
`span_census.py BASE LO HI` then gives width (operand size) and direction (capstone access) per offset.

**Result (before):** 3 of 140 gap rows were contradicted.

| row | finding | disposition |
|---|---|---|
| `EeVu0RegisterBank +0x490` (256 B) | 47 references: 18 qwords zeroed by the bank clear `0036D9E0`; 4 dwords written by `002487A0`/`00248A90`; the sticky flag word `+0x560` (two read-modify-write `or`s, no consumer, matching FABLE's bank page); `+0x568` stored by three functions | **re-cut** into 8 rows |
| `AppBootStatic01F7F480 +0x0E` (34 B) | `+0x10` / `+0x20` address-taken, passed to `0017D9D0`, which `memcpy`s a string into each | **re-cut** into 3 rows (two `char[16]` buffers) |
| `TextPainter +0x0000` (4296 B) | one `lea` of the **object base**, passed with its size `0x1108` to `008620A0` (`002B3556`) | **row stands**: an address-of-object is not a field access |

**Result (after):** 1 of 143, and that one is the TextPainter base address. **137 of 140 original gap rows
were confirmed** by the audit for direct references.

**Bound.** Direct (rip-relative) references only. Accesses through a register-held base (for example an `ARRAY`
indexed by a register, or a `PTR` object) are not covered. Those rows are outside this audit's domain, and a
negative here says nothing about them.

## Block 256 (OPUS, 2026-09-25): pointer-reached types, checked with an independent seed

Types reached through a pointer cell (`PTR` / `PARRAY`) are outside the direct-reference audit, and their gap rows
came from a **cell-seeded** receiver census. `ptr_gap_ctor_cross.py` reruns `census_receiver_fixpoint` **seeded from
each type's constructor** (`SEED=ctor`, the address taken from the type row's `ctor` column) and flags any gap row it
reaches. Output: `ptr_gap_ctor_cross.out.txt`.

**68 types checked; 62 have no hit. 6 have hits, and each seed was verified before use:**

| type | seed | receiver check | disposition |
|---|---|---|---|
| `GlyphRunWidget1498` | `0053E380` | the `proc` that the widget base constructor runs on the new object | re-cut |
| `MapScreenContainer` | `002B7590` | the same pattern | re-cut |
| `WidgetConsumer02AEE4C8` | `002465F0` | the shared widget base constructor: `00244F50` calls it with `rcx = allocation` (`00244FC2`–`00244FCD`) | re-cut |
| `LegacyPs2GsTextureContext` | `002F6AB0` | called with `rcx = allocation` (`0026E7AB`) | re-cut |
| `PostProcessingLibraryWrapper` | `0065E530` | `mov rbx, rcx; mov [rcx], rdi; mov [rcx+8], dil` | re-cut |
| `AuthoredTableHeader` | `003845F0` | **wrong receiver.** It is the registrar: `[rcx] = rdx` stores the header pointer into a **registry slot**, and the header is `rdx`. Its hits are the slot's, not the header's | **withdrawn**; the rows are restored to `HEAD` |

**The re-cut** (`Tools/work/OPUS/recut_gap_rows_ctor.py`) replaces only the gap rows the ctor census reaches:
- 1/2/4/8-byte accesses delimit fields;
- overlapping widths stay `mixed`;
- bytes reached only by 16-byte moves become `copiedSpan`;
- the remaining bytes become smaller unobserved spans.

Meanings are not claimed. 17 gap rows became 97 rows across the five types.

**Lesson for the instrument.** A `ctor` column can name a function whose `rcx` is not the object: a registrar, a
relocator or a publisher. The receiver has to be checked before a seed's hits are attributed to the type.
