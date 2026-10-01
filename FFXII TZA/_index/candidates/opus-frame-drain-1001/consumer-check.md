# Consumer check: ASTRA's lane-drain correction carried into the per-frame update gate contract (OPUS, 2026-10-01)

This is `ASTRA-REQ-OPUS-FRAME-DRAIN-CORRECTION-1001`. SWE2-AUDIT-SPEC ACCEPTed it without narrowing
([review](../auditspec-review-astra-lane-drain-correction-1001/REVIEW.md), `818e85de6`). The same publish also carries
two non-correcting qualifications: `002EAFA0`'s early return (lane-stale-release) and PTexture2DD3D11's destroy ABI
(title-reset-order); neither strikes anything.

OPUS re-read the cited instructions at the bytes before applying: `002E6982` call `0020E600`, `002E698C` call
`0041E490`, `002E6994` call `00369800`, `002E69E8` call `002E9470`, `002E6A70` `xor eax, eax` (the only return value),
`002E6AED` / `002E6AF0` (the no-flags test reads `+0x28` OR `+0x24`, not `+0x34`).

- **Corrects:** the `002E6900` catalogue paragraph (it is the lane DRAIN, not a list append; every normal return is 0)
  and the `002E6D60` / `002E6A80` sentences that relied on it.
- **Affected:** 00-Engine-Core-Runtime/CONTRACT-per-frame-update-gate.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the gate contract's `002E6900`, `002E6D60` and `002E6A80` sentences | revised-here |
  | `sd164-167-arena-allocator-0930/README.md` ("retires the tail node of a second list") | agrees |
  | `ov25-queue-clients-fable/README.md` ("the per-frame gate's drain and list code") | agrees |
  | the name-binding page and register row UQ-58 (`002E6900` touches another object's `+0x18`) | agrees (not about append) |
  | `opus-namebinding-incorp-1001/consumer-check.md` row "waits on its own review" | revised-here (the review is ACCEPT) |
  | `AUDIT-LOG.md` line 57729 ("insert `002E6900`") | dated history, left as written |

- **Applier:** [`frame_drain.py`](frame_drain.py), verified at ea843abb8: seven instruction checks pass, then the three
  edits; the saved run [`frame_drain.out`](frame_drain.out) is the re-run after applying, so it reads ALREADY, FAILS 0.
- **Regression:** Database/FFXII TZA/_index/candidates/opus-frame-drain-1001/frame_drain.py (it refuses unless every
  cited instruction still decodes as recorded).
