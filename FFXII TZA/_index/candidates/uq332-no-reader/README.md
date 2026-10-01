# UQ-332 — nothing in this executable walks section 12

FABLE, Claude Opus 5.5, 2026-09-27. **NATIVE/STATIC. Nothing was executed.**
Control: `uq332_no_reader.py` (3 checks, FAILS 0).

**The question.** Who reads the section-12 pointer the handler stores, and walks its entries?
([section-012.md](../../../25-EBP-Script-Container/Sections/section-012.md) §7.)

**The 2026-09-14 census.** It found exactly two accesses to `managerRecord[+0x100]`, and both are writes (`0026CE51`
set, `0026CC31` clear). The global mirror `022C6DA8` has one load, which only tests the pointer before a release gated
on a return-zero stub. The census left three routes open. This record closes each one.

**R1 — the container route.** Across the image, only two instructions read an EBP container's section-12 directory
slot (a dword load of `[r + 0x40]` next to a count test on `[r + 4]`). Both are in the loader `003304A0`:
- **`003304E4`** tests whether the section is present and sets pending bit 9.
- **`003305EA`** feeds the handler `0032FB70`, which stores the pointer and clears that bit.

No function indexes the directory generically.

**R2 — the escapes.** The four table-dispatched `{record, index}` stores are the begin callbacks of the sync verbs:
- `entrysync` (015D);
- `eventstartsync` (0165), with its variants 0166 and 0167.

Their polls read one manager field, the byte `+0x10`. Every function they hand the record to, followed through its
whole callee closure, has no `+0x100` access.

**R3 — the inversion.** A section-12 entry is a packed model id, `(letter << 16) | id` (UQ-333). The engine's decoder
for that format is `002ED6F0`. None of its callers takes the id from a count-prefixed list. Each one takes it from:
- an entity's `+0x14`;
- its own argument;
- the static letter table at `00D0F870`.

The image also has no model-name format string.

**Answer.** The manifest is stored twice and cleared on teardown, and no code in this image walks it. A reader, if one
existed, would have been in the PS2 build's resource path.

**Not claimed:**
- An indirect caller of the decoder. The census uses the rel32 index, so an indirect call would not appear.
- A pointer copy held in a structure none of these routes reaches.
- What the manifest was for.
