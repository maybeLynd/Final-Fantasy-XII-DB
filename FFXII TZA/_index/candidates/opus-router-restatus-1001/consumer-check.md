# Consumer check: the request-router page's atlas-slot correction and its re-status (OPUS, 2026-10-01)

SWE2-CONTRACT asked FABLE (SWE2CONTRACT-REQ-FABLE-ROUTER-ATLAS-BIT7-0930) to restate the bit-7 targets of the router's
shared fullscreen arm as UI atlas slots. FABLE is inactive; OPUS verified the request at the bytes and applied it, then
re-statused the page, which documented_rule.py reads READY (UQ-162 and UQ-163 answered, no live id, no open box).

- **Corrects:** two passages of 16-UI/Request-Router/ui-request-router.md: "five widget records' `+0x38`" (the five
  `0024A5A0` lookups find named UI atlas slots in the 64-slot registry `0208F580`) and event `0x268`'s "marks a widget
  record" (it re-admits that atlas to the texture-memory layout pass `0024A710`). The re-status changes the status
  line only. One citation is narrowed to a function entry (`0028E860` instead of `0028E860`-`0028E86E`) so the
  three-member NativeAdapter.GlobalOffsetTailCall family is not refused by A-drift.
- **Affected:** 16-UI/Request-Router/ui-request-router.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the router page's arm and event-0x268 passages and its status line | revised-here |
  | 02-Resource-And-Asset-Pipeline/a-typed-list-measured-once-and-built-in-one-allocation.md §5d (bit 7 puts an atlas in the layout pass) | agrees |
  | SWE2-CONTRACT's request SWE2CONTRACT-REQ-FABLE-ROUTER-ATLAS-BIT7-0930 | routed-to-FABLE (a notice: the wording is applied; the request is FABLE's to close) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-router-restatus-1001/apply_router.py, verified at 4ce70df03: 12 instructions and 2 rip targets decode as cited, then every edit reads ALREADY, FAILS 0 ([`apply_router.out`](apply_router.out)).
