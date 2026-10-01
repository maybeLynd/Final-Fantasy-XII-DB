# Affected-consumer check: BG-5 and BG-6 answered; "vertex reservation" and "begins a batch" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `bg56_gi_bodies.py` beside this file (6 checks, FAILS 0).

The Gi page read device slot 0 as "vertex reservation", taking the count in `edx`. The DynGeo page said the same body
"begins a batch". Read against the device's own vtable (`PrimitiveRendererD3D11`, named on the Gi page §20e), slot 0:
- overwrites `rdx` before reading it;
- returns a fixed `0x7FE0`-byte staging area (682 vertices) and publishes it at `+0xB8`.

The count goes to slot 4, whose batcher checks it against 682 and flushes. Also on the Gi page's triple and bracket:
`+0x80` and `+0x88` are a constant stub, and `+0x128` is called by `GiSprite` and `GiPrim` too, not only by
`GiEndScene`.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Gi-Render-Commands/gi-render-command-family.md` §2 | "`[dev+0x000]` is vertex reservation" | revised-here (struck; corrected beside it) |
| same page §2, the triple and the scene bracket | `+0x78`/`+0x80`/`+0x98` a triple; `+0x128` the end-scene | revised-here (dated note: `+0x80` is a stub; `+0x128` is shared) |
| same page, "What this section does not deliver", the `[dev+0x000]` bullet | "still unread … exactly as unconfirmed as before" | revised-here (struck; answered beside it) |
| same page §7, the six shape-A bodies box | not read line by line | revised-here (ticked; per-body reading beneath) |
| same page §4 (the PS2 naming test: constant 4 against `[r14+0x60]`) | what the bodies pass | agrees (the counts are what the bodies pass to slot 4) |
| `16-UI/Dynamic-Geometry-Instances/dyngeo-instance-family.md`, the slot 0 / 1 row | "`006CA760` begins a batch and publishes `+0xB8`" | revised-here (struck clause; corrected beside it) |
| `_index/OPEN-QUESTIONS.md` BG-5, BG-6 | OPEN | revised-here (ANSWERED; the previous status kept as history) |
