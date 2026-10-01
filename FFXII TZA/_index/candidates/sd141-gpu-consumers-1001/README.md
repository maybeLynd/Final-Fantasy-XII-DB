# SD-141 answered: the flying-fade pair reaches the scene-wide constant buffer and 517 lit shaders read it (OPUS, 2026-10-01)

SWE2-AUDIT-SPEC's REJECT ([review](../auditspec-review-sd141-0930/REVIEW.md)) reopened SD-141: "who consumes the
flying-fade pair". The pair is read by a struct copy, and the copy's consumers had not been traced. This record traces
them. Static, the certified image and the shipped shader packs.

## The chain (OPUS)

| step | what | evidence |
|---|---|---|
| 1 | `001C7940` stores `mMapShadowFlyingFadeRange` / `...Speed` into `02CB8414` / `02CB8410` | the original record (`001C9040`, `001C8FFF`) |
| 2 | `006084B0` hands the block, at the pair − 0x2B0, to the dword copy `005DEC50`, which reads both into `00604750`'s snapshot `+0x550` / `+0x554` | the review's H1-H3 (`sd141_handon.py`, FAILS 0) |
| 3 | `00604750` writes the snapshot field by field through `r14`, the pointer `006097B0(rbx, &out)` returns (`00604BEC`, `00604BF9`) | read 2026-10-01 |
| 4 | `006097B0` picks the next slot of a ring of buffers, waits while it is busy (`005CCB80` loop), and calls `00626060`, which returns the slot's memory. ~~Its error path logs "Performance warning: mapping buffer that was not created with D3D11_CPU_ACCESS_WRITE flag specified" (`00D55300`), so `r14` is a mapped D3D11 buffer~~ *(Narrowed 2026-10-01, OPUS, on SWE2-AUDIT-SPEC's [repair review](../auditspec-review-sd141-0930/REVIEW-REPAIR-1001.md): the string is at `00D53100`, not `00D55300`, and no instruction references it, so it is not this function's error path. That `r14` is a mapped buffer rests on the ring-pick / busy-wait / `00626060` call shape only. Step 5's offsets and step 6's shader census do not depend on it.)* | read 2026-10-01 |
| 5 | UQ-22's map ([`uq22-scenewide-cbuffer/map.tsv`](../uq22-scenewide-cbuffer/map.tsv)) places the two stores at `SceneWideParameterConstantBuffer` `+0x5D4` **`mShadowFlyingFadeSpeed`** and `+0x5DC` **`mShadowFlyingFadeRange`** | `uq22_scenewide_map.py` (OPUS, 2026-09-27) |
| 6 | **The shader readers.** Across the 4,799 DXBC blobs that declare the buffer, D3D_SVF_USED (the compiler's "this shader reads the variable") is set for both variables in **517 blobs, all in `phyredefaultlitshader.fx`** | [`sd141_gpu_used.py`](sd141_gpu_used.py) / [`.out`](sd141_gpu_used.out), FAILS 0 |

Controls (in the checker):
- L1: UQ-22's layout (one layout, 0x5F0 bytes, 154 variables, 4,799 blobs).
- L2: the pair's offsets.
- K1: `EyePosition` USED in 3,632 blobs.
- K2: the non-flying pair `mShadowFadeSpeed` / `mShadowFadeRange` USED in 517 blobs each.

## The answer (OPUS)

**The flying-fade pair is consumed on the GPU.** The CPU copies it into the per-frame scene-wide constant buffer, and
517 compiled variants of the default lit shader read both values. That is the same number of variants that read the
ordinary shadow-fade pair. So, by its names, it tunes how the map shadow fades for flying units in lit-scene shading.

**For modding:** changing `mMapShadowFlyingFadeRange` / `mMapShadowFlyingFadeSpeed` reaches the default lit shader.

## Limits (OPUS)

- What the shader computes from the two values (the fade arithmetic) is not decompiled. "Flying" and "shadow fade"
  are read from the names.
- Which of the 517 variants a given scene binds is a runtime question; the variants exist in the shipped packs.
- The blob counts match the non-flying pair's; that the two sets are the same 517 blobs is not checked one by one.

run: sd141_gpu_used.py (FAILS 0)

## Review (OPUS)

SWE2-AUDIT-SPEC, the lane that issued the REJECT, reviewed this record:
**ACCEPT-WITH-NARROWING** ([REVIEW-REPAIR-1001.md](../auditspec-review-sd141-0930/REVIEW-REPAIR-1001.md), `386729b76`).
It re-ran every control and byte-checked hop 4. Its one narrowing (the string anchor) is applied in step 4 above.

SWE2-STRUCT traced the same consumers independently, in
[`swe2struct-sd141-receiver-1001`](../swe2struct-sd141-receiver-1001/README.md) (`911aff55b`), and found the same thing:
the pair is GPU-only. That answers STRUCT's trace request, `OPUS-REQ-STRUCT-SD141-CONSUMERS-1001`.
