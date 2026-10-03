# CoreRuntimeStatic02064AA0: the frame-step statics named (OPUS, 2026-10-03)

*repos-91, a local helper, re-cut the 13 census placeholder rows of the static the field frame driver steps through.
OPUS checked every cited code address as an instruction start and re-read the step loop's anchors. Applied by
[`apply_recuts.py`](apply_recuts.py) from [`recuts.json`](recuts.json): 13 rows out and 13 in. The research is in
[`research.json`](research.json).*

## Applied (OPUS)

**How the field frame advances.** The driver `0022A490` stores its argument at `+0x00` and runs the frame body
`0022A580`. After the step loop, `+0x20 stepAccumulator` gains `+0x28 stepIncrement` times `+0x24 gameSpeedScalar`.
`+0x28` is 1.0 at boot, and its setter is `00229EE0`. The pending-reset handler calls it with 1.0.
`+0x24` takes its speed-table entry while `+0x32 fastModeEnabled` is set, and `+0x32` is rewritten every step from
`00358550()`.

**The counters:**
- `+0x08 stepsThisFrame`;
- `+0x30 completedFrameCounter`, a wrapping byte bumped when `0022A580` returns non-zero;
- `+0x38 frameParity`, which alternates between 0 and 1;
- `+0x2C frameBaseConstant`, which is 2 / FrameLimit: 2 at 30 fps and 1 at 60.

**The draw pair.** `0022B0B0` clears `+0x3C postFxEligible` and `+0x40 postFxRanThisDraw` at the start of each draw.
It sets `+0x40` right after the post-processing call `00182970`, so that call runs once per draw.

**Also named:**
- `+0x31 aspectModeByte`: `00229D20` answers 1.3333 unless the byte is 1, 2, 3 or 5.
- `+0x10 zeroVector`: a 16-byte quad that no code writes. It lies past the file-backed part of `.data`, so it is zero
  at load.

## Finding already corrected by its owner (OPUS)

`authored-data-table-registry.md` lines 302-303 said `02064AD4` mirrors the byte at `02064AD3` and is set to 2 on the
state-4 exit. The image's only rip-relative reference to `02064AD4` is the boot store `0022A190` (1.0). OPUS routed
the question earlier (OPUS-REQ-FRONTIER-02064AD4-MIRROR-QUESTION-1003). SWE2-FRONTIER corrected the page in
`919aea842`: the root's mode byte is `02064AD3` itself, and `02064AD4` is a boot 1.0f value.
