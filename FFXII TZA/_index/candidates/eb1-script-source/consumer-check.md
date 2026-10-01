# Affected-consumer check: EB-1 answered; the loader page's +0x50/+0x60 reading corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `script_class_census.py` beside this file (5 checks, FAILS 0).

The 2026-09-22 reading took `[obj + 0x50]` as the chunk buffer and `[obj + 0x60]`, with bit 0 masked, as its length.
The registered field schema and `00683C30`'s own reads say otherwise:
- `+0x50` is `PClassCallableMethodScript::m_script`, a `PScript` pointer;
- `+0x60` is the tagged `m_entryPoint` string;
- `00683C30` reads the source bytes from `PScript + 0x18`, the size from dword `+0x10` (bit 31 cleared) and the name
  from `+0x48` (`m_sourceName`).

The conclusions that rested on the old reading still hold. All three suppliers take the chunk from an object, not a
path, and the asset route needs the class named in data, which no shipped namespace does.

| consumer | what it said | state |
|---|---|---|
| `23-Third-Party-Libraries/Lua-Core/the-lua-loader-and-what-it-accepts.md` (the `UQ-312` paragraph) | "the buffer from `[obj + 0x50]` and the length from `[obj + 0x60]` with bit 0 masked off … returning at once on a zero length" | revised-here (struck, corrected beside it) |
| same page, the `0x68` corroboration sentence | "the buffer at `+0x50` and the length at `+0x60`" | revised-here (struck, corrected) |
| same page, the `UQ-313` / `EB-1` box | open; its 2026-09-14 narrowing calls `+0x50` "the buffer" | revised-here (ticked, answer beside it; the narrowing is kept as history) |
| `23-Third-Party-Libraries/Lua-Core/CONTRACT-lua-chunk-loader.md`, `EB-1` row | open | revised-here (dated note in the cell) |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv` | `m_script` 0x50, `m_entryPoint` 0x60, `PScript::m_sourceName` 0x48 | agrees (the correction adopts it) |
| `_index/OPEN-QUESTIONS.md` EB-1 | PARTIAL | revised-here (ANSWERED; the previous status kept as history). UQ-313 was already SUPERSEDED onto EB-1. |
| `_index/OPEN-QUESTIONS.md` UQ-312 (does the shipped game supply a chunk) | open | agrees. It stays open: the asset route is now closed for `PScript` too, but programmatic creation through the descriptor is not read. |
