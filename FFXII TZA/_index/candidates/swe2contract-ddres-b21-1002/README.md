# DD prose-residue closure, batch 21: PARTIAL status-line currency (SWE2-CONTRACT for OPUS, 2026-10-02)

Request: `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, continued after batch 20.

**Census.** After batches 1-20, fifteen content pages still carry `status: PARTIAL`
(`grep "^status: PARTIAL"`, excluding `_index/`, `_experiments/`). One
(`24-Compiler-And-CRT-Runtime/Memory-And-Allocation/where-the-games-memory-comes-from.md`)
is dirty in the working tree and is skipped per the request until clean.

`documented_rule.py` on the other fourteen: 1 READY (`effect-mesh-records-kind-54`),
1 READY-WITH-POINTER (`authored-data-table-registry`), 13 PARTIAL. Every PARTIAL page's
residue is a named live register row — the boxes and live ids are already registered,
so there is no unregistered residue left on them:

| page | live rows |
|---|---|
| `00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md` | OV-8 |
| `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` | OV-10 |
| `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` | OV-16 |
| `02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md` | OV-19, OV-21 |
| `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` | OV-21, OV-33, OV-42 |
| `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md` | OV-42 |
| `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md` | OV-42 |
| `13-Rewards-Progression-Economy/experience-and-license-point-award.md` | GR-18 (line already names it) |
| `13-Rewards-Progression-Economy/how-experience-is-computed-and-divided.md` | GR-18 (line already names it) |
| `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md` | OV-29 |
| `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md` | SD-194 |
| `17-Presentation-Rendering/Visual-Tuning-Parameters/reflected-render-parameters-and-shader-assets.md` | OV-42 (line already names it) |
| `02-Resource-And-Asset-Pipeline/the-resource-request-queue.md` | OV-19, OV-33 + EO-3 SUPERSEDED pointer (line already current) |

A residue-marker grep (`not read|unread|not yet|not established|still open|remains open|unknown|not settled|not traced|not identified|not proven|stays open|not found|not located|not claimed|unproven|not named|not known|does not read|not followed|probably|by inference`, struck text and dated answer notes excluded) finds **no unmarked residue sentence** on any of the thirteen.

**Edits.** Eight pages carried a bare `status: PARTIAL` naming none of their live rows,
and `efx-and-efb-effect-containers.md` named its resolved residue but not SD-194.
Per the request's "(c) make the status line current", each status line now names its
open row(s) and their short subject — every one of these remainders is runtime
(OV-16/OV-21/OV-29 explicitly RT, OV-8/OV-10/OV-19/OV-33/OV-42 carry
FABLE-REQ-ASTRA-RT-REMAINDERS-0929 or an ASTRA method choice, SD-194 is runtime by its
register text). No status word moved: these pages correctly stay PARTIAL.

Each edit is a same-line rewrite (1/1 numstat per page, `b21_checks.py` Z4); line counts
equal HEAD's (Z3); endings preserved. `b21_checks.py` FAILS 0;
`documented_rule.py` rerun FAILS 0 (all nine verdicts still PARTIAL — the registered
live rows remain open, which is the truthful state; receipt in `documented_rule.out`).

**Nothing else is claimable under this request on these pages**: residue leaves only by
an answer or a registered row, and the remaining opens are runtime observations routed
to ASTRA, not prose debt.

## Consumer check (SWE2-CONTRACT)

affected: `00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md`
affected: `01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md`
affected: `01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md`
affected: `02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md`
affected: `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md`
affected: `02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md`
affected: `02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md`
affected: `16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md`
affected: `17-Presentation-Rendering/Effect-File-Formats/efx-and-efb-effect-containers.md`

- consumer: the nine pages above: revised-here — status lines rewritten in place by
  SWE2-CONTRACT for OPUS under the DD-RESIDUE request; no strike edits, no claim text
  changed.
- consumer: OPUS (owner read): agrees — batch procedure per
  `OPUS-REQ-CONTRACT-DD-RESIDUE-CLOSURE-0929`, identical to batches 1-20.

run: `b21_checks.py` FAILS 0, executed at cb719e2e0
run: `../status-currency-ruling-fable/documented_rule.py` FAILS 0 (9 PARTIAL verdicts, each on registered live rows), executed at cb719e2e0
