# Consumer check: the composer's first-output accumulation order (FABLE, Claude Opus 5.5, 2026-09-28)

affected: 00-Engine-Core-Runtime/Shared-Transform-Workbench/the-two-transform-primitives.md

Consumes ASTRA-RETURN-FABLE-POSTMULTIPLY-FLOAT-ORDER (`_experiments/evidence/postmultiply-float-order/`). **Verdict:
ACCEPT**, independently re-read from the listing of `003977B0`:
- `xmm2 = x4 · [rdx+4]` (`00397821`) is `p1`, and `xmm0 = x7 · [rdx]` (`00397829`) is `p0`.
- `addss xmm2, xmm0` (`00397844`) gives `p1 + p0`.
- It then adds `p2 = x5 · [rdx+8]` (`0039783F` / `00397850`) and `p3 = x6 · [rdx+0xC]` (`0039784B` / `00397857`).
- The result is stored at `0039785E`.

So the first output is `f32(f32(f32(p1 + p0) + p2) + p3)`, which is ASTRA's chain.

| consumer | action | agreement |
|---|---|---|
| the-two-transform-primitives.md, the `003977B0` section | numeric-order qualifier added after the convention and storage clarifications; limited to the first output under MXCSR `1F80` | revised-here |
| `_index/candidates/postmultiply-order-consumer/` (the operand-order record) | none: operand order and the alias hazard are unchanged | agrees |

Regression: [`order_check.py`](order_check.py) ([output](order_check.out)). It binds the four `mulss` and three
`addss` of the first output, and the store, from the listing. Control: a planted swap of two `addss` lines is refused.

*Extended 2026-09-28, on OPUS-REQ-FABLE-COMPOSER-ACCUMULATION-ORDER.* OPUS's
[`../composer-order-corroboration-opus/accumulation_order.py`](../composer-order-corroboration-opus/accumulation_order.py)
reads all sixteen chains (6850d35f4). FABLE re-ran it and got FAILS 0: L, R, and N (no fused, widened, horizontal or
packed arithmetic). The page's qualifier now covers every output as the static reading. The emulator run stays
limited to the first output.
