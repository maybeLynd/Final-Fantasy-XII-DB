# Affected-consumer check — the image-backed block's +0x30 region (FABLE, Claude Opus 5.5, 2026-09-26)

FABLE's 2026-09-15 reading on the save-payload page said "block `+0x30` is a `u16[48]` and `+0x90` a `u32[101]`",
written "in two modes selected by `ecx == 1`". The FG-1 row repeated it: "`+0x8030` / `+0x8090` head a `u16[48]` and a
`u32[101]` cleared together".

**What the accessors show.** `00252610`, `002527B0` and `002526F0` take a class code in `ecx`. Their
`sub ecx, 6` / `sub ecx, 1` / `cmp ecx, 1` chain selects:
- class 6: a `u16` at `+0x30`, index clamped to 31;
- class 7: a `u8` at `+0x70`, index clamped to 31;
- class 8: a `u32` at `+0x90`, index clamped to 100.

So the region is **three** arrays, `u16[32]`, `u8[32]` and `u32[101]`, and together they tile the 500-byte `memset`
exactly. A `u16[48]` would have overlapped the `u8` array, which the page never named. The "two modes" were a
misreading of the class chain.

**Regression:** `_index/candidates/fg1-typed-store/typed_store.py`, 9 checks, FAILS 0. The planted negative: no
accessor reaches the `u16` class past `+0x6F`.

| consumer | state |
|---|---|
| `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/the-save-payload-field-map.md`, the FG-1 narrowing's array bullet | revised-here (struck, corrected; notes the missing `+0x8070` census row) |
| `_index/OPEN-QUESTIONS.md` FG-1 row ("head a `u16[48]` …") | revised-here (struck, corrected; status unchanged, the meaning stays open) |
| the same page's census table rows `+0x8030` / `+0x8090` | agrees (offsets and access sites; the table carries no element count) |
| `_types` | no `ImageBackedStateBlock` rows declare this region (grepped 2026-09-26) |
| `_index/AUDIT-LOG.md`, `_index/_inbox/*` | history |
