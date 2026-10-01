---
experiment: EXP-067
title: original UI router dispatch and policy gates
status: COMPLETE - bounded isolated original-code evidence
contract: none - No existing contract specifies UI router dispatch 00254B50; the widget-object contract specifies a different allocation and message boundary.
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original router and shipping dispatch tables with recording callbacks; route arguments established, native UI acceptance omitted.
contract_coverage: No matching existing contract at recovery; this disposition does not close a database knowledge or contract gap.
tool: evidence/EXP-067-ui-router-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-067: original UI router dispatch and policy gates

**Result:** 72 controls passed on the first execution; a mutation that normalizes
the generic callee's request argument was detected. ASTRA, 2026-09-11. No game
process or UI was accessed.

## Question and method

The [router page](../16-UI/Request-Router/ui-request-router.md) lists generic routes
for request 2, 6–11 and 13–23, but its later switch-label correction says there
are only six live request IDs. This experiment distinguishes a default arm that
rejects requests from one that forwards them to a generic scheduler.

The [checker](evidence/EXP-067-ui-router-controls/check.py) verifies the reference
EXE SHA-256 and executes the complete original `00254B50` body (263 bytes, RET
`00254C56`). It executes the original policy table at `01E0C2C0` (22 dwords),
six-RVA jump table at `00254C58`, and 24-byte selector map at `00254C70`.
These tables are checked against an independently transcribed oracle.

The policy producer `002E0FA0`, three preparation callbacks `0017E7D0`, `0035DA80`,
`003C8990`, generic preparation `0028F970`, and all six distinct route callees
are recording stubs. They clobber volatile integer registers and return configured
values. Callback identities and ordering are tested; no argument contract is
claimed for the policy/preparation callbacks. Route arguments and full EAX
returns are tested. No native UI transition or acceptance is inferred from a stub.

[Raw results](evidence/EXP-067-ui-router-controls/result.json), original bytes,
[disassembly](evidence/EXP-067-ui-router-controls/disassembly.txt) and executed
source are sealed in the [manifest](evidence/EXP-067-ui-router-controls/manifest.json).

## Dispatch contract

The router retains the original 32-bit request argument and separately computes
`normalized = request & 0x7FFF`. Dword global `02092734 == 1` returns zero before
any callback; value 2 is an admission control proving the comparison is exact.

Otherwise it obtains the policy mask, projects its low 22 bits through the
original table, and tests bit `normalized & 31` of the resulting inhibit mask.
The modulo-32 behaviour is the native register `BT` operation; request 34 is
inhibited by the same bit as request 2. Policy input bits 22–31 are ignored.

An admitted request always calls the three preparation callbacks in order before
dispatch. The native selector table then produces:

| normalized request | route | forwarded arguments | result |
|---|---|---|---|
| 1 / 4 | `0035D660` | normalized id | callee EAX |
| 3 | `0035D980` | normalized id | callee EAX |
| 5 | `003C87B0` | normalized id | callee EAX |
| 12 | `0028E970` | normalized id | **1**, regardless of callee EAX |
| 24 | `0035D080` | normalized id | callee EAX |
| every other value | `0028F970`, then `00280A00` | generic receives **original request**, parameter, flag | generic EAX |

Thus six numeric IDs receive special handling, but there are five special arms
plus a generic arm. The generic path is not a failure/default rejection. All
other IDs within 1–24 route there, and so do normalized values outside 1–24:
controls include 0, 25, 32 and 32767. This establishes dispatch, not that the
native generic scheduler accepts or gives meaning to every possible value.

The split between normalized selection and original forwarding matters:
`0x8001` selects the special route and passes 1, while `0x8002` and `0x10002`
select the generic route and preserve those full request dwords. Parameter
`0x12345678` and flag `0x87654321` survive all preparation stubs unchanged.

## Policy projection

The nonzero table rows are:

| input policy bit | request inhibit mask |
|---:|---:|
| 0 | `0x00000004` |
| 1 | `0x0000002A` |
| 2 | `0x00000008` |
| 3 | `0x00000004` |
| 5 | `0x00000020` |
| 6 | `0x00004000` |
| 8 | `0x00200002` |
| 9 | `0x00004020` |
| 10 | `0x00000008` |

Other rows through bit 21 are zero. Each of the 32 possible input bits has its
own control: nonzero rows inhibit a positively selected request, zero rows and
high ignored bits admit the generic control. Separate controls establish allowed
requests under nonzero policy, combined rows, modulo-32 aliasing and an admitted
request under all policy bits. A refusal returns EAX zero and omits all later
preparation and route callbacks.

## Validation and limits

The 72 cases comprise all 24 in-range IDs, 12 boundary/normalization/return/global
gate cases, 32 individual policy-bit cases, and four combined/alias/admission
controls. Every case compares exact callback sequence, multiplicity and route
arguments, full EAX, absence of native non-stack writes, and unchanged global and
policy fixture pages. Runs must reach the expected return boundary and restore
RSP and all eight nonvolatile integer registers. Reads and visited instructions
are retained; no SIMD-preservation claim is made.

A private mutation changes `MOV ECX, EBP` at `00254C37` to `MOV ECX, EBX`, so the
generic route gets the normalized id. Request `0x8002` then passes 2 rather than
`0x8002`; the mutant returns normally but fails the exact argument oracle. No
reference executable or production source is modified.

The active six-live-ID statement on the router page is contradicted at the
original caller boundary. Six special labels do not bound the generic request
vocabulary. Route names, friendly screen identities, native policy production,
mailbox scheduling and downstream acceptance still need their own evidence.
