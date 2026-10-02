# bg6-slot0-replay — BG-6 executed confirmation

SWE2-ORACLE, 2026-10-02. NATIVE-REPLAY class. `live_game: false` —
the device object is a disclosed synthetic fixture; no game state is
claimed.

BG-6 ("does `[dev+0x000]` reserve vertices?") is already ANSWERED in the
ledger: `PrimitiveRendererD3D11` vtable `00D86960` slot 0 = `006CA760`
returns `dev + 0x10880 + index*0x7FE0` and zeroes the index
`d[dev+0x18860]`; the cell's only image-wide writes are this read and
this clear, so slot 0 always hands out the same 0x7FE0-byte staging
area (682 vertices of 0x30). This surrogate adds an executed check of
the body plus the counterfactual.

`check.py` maps the canonical exe (`73461D08…21F8`, sections at
RVA+0x120000) under Unicorn 2.1.4, fabricates a device buffer at
`0x40000000`, plants `d[dev+0x18860]`, calls `006CA760`, and reads back
rax / the index cell / `q[dev+0xB8]` (the published pointer).

## Cases — `result.json`, md5 `3198c99ce0ca05d8e3cf29e95c912511`

| planted idx | rax | idx after | published |
|---|---|---|---|
| 0 | `dev+0x10880` | 0 | same |
| 1 | `dev+0x18860` (`+1*0x7FE0`) | 0 | same |
| 3 | `dev+0x28820` (`+3*0x7FE0`) | 0 | same |

The `imul rdx, rax, 0x7FE0` is live: a nonzero index is honored — so
"slot 0 always returns `dev+0x10880`" is a *population* fact (nothing
in the image ever stores a nonzero value to `+0x18860`), not a constant
of the function. Index is consumed-then-cleared every call and the
pointer is republished at `+0xB8` unconditionally.
