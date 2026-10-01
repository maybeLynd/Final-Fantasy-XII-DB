---
experiment: EXP-069
title: native UI request feedback across two router calls
status: COMPLETE - bounded isolated original-code evidence
contract: ../16-UI/Widget-Object-Model/CONTRACT-widget-object.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Original router, generic handler and setter composed across two calls on unchanged intermediate memory; factory and other dependencies controlled.
contract_coverage: Same factory caller boundary composed with original router and setter feedback; native factory and widget effects remain stubbed, with no live UI timing.
tool: evidence/EXP-069-ui-native-feedback/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-069: native UI request feedback across two router calls

**Result:** 11 two-call controls passed on the first execution; a mutation that
posts zero to the gate was detected. ASTRA, 2026-09-11. Offline original-code
composition with synthetic state; no game process or UI access.

## Question, hypotheses and method

[EXP-067](EXP-067-ui-router-controls.md) established router dispatch and
[EXP-068](EXP-068-ui-generic-controls.md) established the generic caller's literal
setter argument and packet. Does that argument cause a native global write that
refuses the next router call, or is this feedback merely an assumption made at
stub boundaries?

The [checker](evidence/EXP-069-ui-native-feedback/check.py) executes three complete
original bodies together: router `00254B50` (263 bytes), generic handler
`00280A00` (193), and setter `00252B40` (29, ending in a tail jump to `00254740`).
It uses the original policy table, selector map and jump table from EXP-067,
checking all table values against that experiment's independently transcribed
oracle. The EXE SHA-256 is verified before extracting code or tables.

Each control executes two router invocations on **the same memory fixture**.
Only caller argument registers, saved-register sentinels, RSP and the return
address are re-established for the second invocation. No gate/id global, root,
or packet is reset between them; no expected intermediate write is injected.

The policy producer, four preparation boundaries, setter's tail-jump destination
`00254740`, widget factory `00244F50`, finalization `0028E860`, and cookie checker
`00808C40` remain explicit recording stubs. The cookie stub preserves EAX; other
stubs clobber volatile integer registers and return configured values. Special
route entries fail the checker if reached: this package covers the generic path.

[Raw results](evidence/EXP-069-ui-native-feedback/result.json), all six code/table
byte files, [disassembly](evidence/EXP-069-ui-native-feedback/disassembly.txt), and
executed source are sealed in the [manifest](evidence/EXP-069-ui-native-feedback/manifest.json).

## Observations and causal sequence

With initial gate zero, no policy inhibition, and empty root busy slots, request
2 with parameter `12345678` and flag `87654321` produces:

1. Original router entry, policy and preparation callbacks, original generic
   entry with all three incoming dwords intact.
2. Original setter entry with `(2, 1)`; it masks ECX with `7FFF` and performs
   **three native dword writes in order**: `02092734 = 1` at `00252B46`,
   `020927D8 = 2` at `00252B4C`, `02092730 = 2` at `00252B52`.
3. Tail prelude entry and both widget factory entries observe those global values.
   Both factory calls receive the same descriptor and the original payload
   `[2, 12345678, 87654321, 0]`; finalization follows and the router returns 1.
4. The next router invocation, request 6 with different parameter/flag, returns
   **zero before even calling the policy producer**. No further global write,
   generic entry, or callback occurs.

Thus, under the stated downstream boundaries, an accepted generic request itself
sets the native value that blocks the next router invocation. The gate is not
the incoming payload parameter: parameters 0 and 1 produce the same gate write.
This does not establish how long the real game leaves it set or who clears it.

Request `8002` retains `8002` in the payload/token but writes normalized id 2 to
both globals. Request `FFFFFFFF` retains that payload dword and signed token -1,
while the globals receive `7FFF`. Request 25 also reaches this native path.
These are boundary controls, not friendly screen identities.

The controls distinguish refusal before and after preparation:

| fixture | first return / global effect | second request 6 |
|---|---|---|
| initial gate 1 | zero, no callbacks or writes | zero, no callbacks or writes |
| initial gate 2 | one, setter replaces it with 1 | zero at gate |
| root +C0 occupied | zero after router preparation and generic entry; no setter writes | repeats busy refusal |
| policy bit 0 set | request 2 inhibited; no preparation or setter writes | request 6 admitted, posts gate 1 and id 6 |

Changing non-policy stub returns from zero to `FFFFFFFF` does not change the
accepted/then-gated result. Native allocation, prelude and finalization effects
remain excluded rather than being inferred from those stub returns.

## Validation and falsification

Eleven fixtures cover baseline, high/negative/out-of-range request values,
parameter zero/one, initial gates one/two, busy root, policy refusal followed by
admission, and alternate stub returns. All 22 invocations must reach STOP and
restore RSP plus eight nonvolatile integer registers. Each compares full EAX,
exact interleaved native-entry/write/stub sequence, multiplicity, tested arguments,
packet snapshots and global snapshots. Complete root/global/cookie/policy fixture
pages are compared against the independently predicted writes after each call.
Reads and visited instructions are retained; stack and SIMD preservation beyond
the stated assertions are not claimed.

A private mutation changes `MOV EDX, 1` at `00280A3C` to `MOV EDX, 0`. Both calls
still return normally, but the first native gate write is wrong and the second
request now reaches the generic path instead of stopping at the gate. The exact
event, global, memory-page and return oracles reject it. The installed executable
and production source remain unchanged.

## Scope and integration

This is stronger than separate stubbed calls: the original setter writes the
actual memory subsequently read by the original router. It is still not a live
UI session, an allocation/lifetime test, or proof of real downstream timing and
re-entrancy. The factory and two widget procedures are not executed here.

The result supports the setter-argument correction routed to FABLE as
`ASTRA-CONTRA-FABLE-UI-PACKET` for the
[router page](../16-UI/Request-Router/ui-request-router.md). It qualifies the
meaning of `02092734` at this caller: literal 1 is posted independently of the
request payload parameter. Other callers and reset paths require their own
evidence before assigning a universal semantic name or release rule.
