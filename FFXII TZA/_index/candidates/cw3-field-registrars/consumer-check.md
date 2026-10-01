# Affected-consumer check: CW-3 answered; "declared by files, never registered" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `cw3_field_registrars.py` beside this file (4 checks, FAILS 0).

The file-side schema page read the classes and fields missing from the recovered field schema as never registered
by the engine, and offered "built by hand-written D3D11 code rather than reflection" as the obvious cause. Neither
holds. The recovered schema is a census of one member registrar's call sites. All 85 corpus field names it lacks
are registered through three other registrars: 64 by the array-member form, 5 and 16 by the two variants. The class
half was already answered on the image side (`CL-1`, `CL-2`).

| consumer | what it said | state |
|---|---|---|
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` §2, the "obvious reading" quote | "No constructor for any of the 22 has been read"; the cause not established | revised-here (struck the stale sentence; the answer beneath) |
| same page §2, the modder paragraph | "even though the engine's reflection never registers them" | revised-here (struck, corrected beside it) |
| same page §2, the 169-file count table (39 / 47 "declared by files, never registered") | the counts | agrees as a measurement of the one-registrar census; the answer beneath says what they measure |
| same page §5, `UQ-288` box | ticked, superseded onto `CW-3` | agrees |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md` §7 corpus note | "the same boundary as the 22 / 47, at scale (`CW-3`, `CW-4`)" | revised-here (dated note: the boundary is a census limit) |
| same page, `CL-1` / `CL-2` | 21 of 22 classes have descriptors; `PContextSwitch` is a type-table entry | agrees (cited as the class half) |
| `_index/OPEN-QUESTIONS.md` CW-3 | OPEN | revised-here (ANSWERED; the previous status kept as history) |
