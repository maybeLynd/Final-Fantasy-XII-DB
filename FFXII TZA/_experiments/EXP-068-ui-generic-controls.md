---
experiment: EXP-068
title: original generic UI request packet and busy gates
status: COMPLETE - bounded isolated original-code evidence
contract: ../16-UI/Widget-Object-Model/CONTRACT-widget-object.md
evidence_class: isolated original-code
method: B - isolated original-code execution
live_game: false
execution_scope: Complete original generic handler with recording factory/finalization/cookie stubs and a labeled packet/busy intervention.
contract_coverage: Caller-side 00244F50 size, proc and descriptor/payload snapshots; factory is a recording stub, so allocation, copying, ownership and widget procedures are untested.
tool: evidence/EXP-068-ui-generic-controls/check.py
date_designed: 2026-09-11
date_run: 2026-09-11
metadata_recovered: 2026-09-12
---

# EXP-068: original generic UI request packet and busy gates

**Result:** 15 controls passed on the first execution; a zero-extension mutation
was detected. ASTRA, 2026-09-11. Isolated original-code execution, no game/UI access.

## Question and method

[EXP-067](EXP-067-ui-router-controls.md) proved that the router forwards generic
requests without normalizing their dword. This experiment tests what original
`00280A00` does at its own boundary: busy refusal, packet widths, ordered calls,
return value, and whether a later callback sees the same stack storage.

The [checker](evidence/EXP-068-ui-generic-controls/check.py) checks the installed
EXE SHA-256 and executes all 193 original bytes, including both return paths.
It supplies synthetic root and stack pages. The four distinct native callees
`00252B40`, `00244F50`, `0028E860`, and `00808C40` are recording RET stubs.
The first three clobber volatile integer registers and return configured EAX;
the cookie stub records RCX and preserves EAX. Original cookie setup and argument
recovery execute, but native cookie verification does not.

[Raw results](evidence/EXP-068-ui-generic-controls/result.json), original bytes,
[disassembly](evidence/EXP-068-ui-generic-controls/disassembly.txt), and the exact
executed source are sealed in the [manifest](evidence/EXP-068-ui-generic-controls/manifest.json).

## Observations

The function reads the root pointer from `0209AC30`, then tests root `+0xC0` and
`+0xB8`, in that order, as **qwords**. Either nonzero value returns EAX zero
without entering the request/factory/finalization stubs. The upper-qword control
uses `0x100000000`. A null root faults on the eight-byte read at address `0xC0`;
it is not a clean refusal.

With both slots empty, the function makes this ordered sequence:

1. `00252B40(original_request, 1)`. EDX is explicitly **1**, not the incoming
   parameter. The incoming parameter is retained in the payload below.
2. `00244F50(0xD8, 0027FB70, descriptor)`.
3. `00244F50(0xD8, 00280140, same_descriptor)`.
4. `0028E860()`, followed by EAX = 1 and the cookie boundary.

There is no request range test in this body. Controls for 0, 2, 25, `0x8002`,
`0x80000000` and `0xFFFFFFFF` reach the calls. This is local acceptance with
controlled downstream boundaries, not proof that every value names a valid UI.

Let `S` be RSP on entry and `P = S - 0x38`. The payload occupies 16 bytes:

| offset from P | width | value |
|---|---|---|
| +0 | dword | original request |
| +4 | dword | incoming parameter |
| +8 | dword | incoming flag |
| +12 | dword | zero |

The factory receives **D = P + 16**, a separate 24-byte descriptor:

| offset from D | width | value |
|---|---|---|
| +0 | dword | zero |
| +4 | four bytes | not initialized by this body; fixture retains A5 bytes |
| +8 | qword | pointer P |
| +16 | qword | sign-extended original request dword |

The two objects span 40 bytes together. This does not establish a single native
40-byte structure or a semantic role for the uninitialized bytes. There is no
extra zero qword or self-pointer in the observed layout. Negative request -1
has payload dword `FFFFFFFF` and descriptor token `FFFFFFFFFFFFFFFF`.

A labeled intervention in the first factory stub changes payload request to
`0x55`, descriptor token to -99, and root `+0xC0` to 1. The second factory entry
sees those changed packet values at the same addresses. Finalization still runs
and the function returns 1: no second busy check occurs after the initial gates.
This establishes pointer reuse, not that the native factory makes these writes.

## Validation, falsification and limits

The 15 cases cover the six request values, zero/full parameter and flag dwords,
four busy combinations/width controls, alternative callback EAX, packet/busy
intervention, and null root. Every valid-root run must reach STOP, restore RSP
and all eight nonvolatile integer registers, match full EAX, exact call order,
multiplicity, tested arguments, descriptor/payload snapshots, interventions, and
unchanged root/global pages except the specified intervention. Native non-stack
writes must be absent. Reads and visited instructions are retained. The null-root
case instead requires the precise invalid read and an execution error.

The private mutation changes `MOVSXD RAX, ECX` at `00280A4F` to `MOV EAX, ECX; NOP`.
Request -1 then supplies token `00000000FFFFFFFF`; it returns normally but fails
the exact packet oracle. No reference executable or production source is edited.

Native global writes by `00252B40`, allocation/initialization by `00244F50`, the
two widget procs, finalization effects, and cookie verification are excluded.
Stack lifetime is observed only at callback entries. Copying, ownership, async
retention and actual UI scheduling need their own native evidence.

## Affected claims

The [router page](../16-UI/Request-Router/ui-request-router.md), revision `c93abce`,
correctly adds the busy gates but describes a 32-byte request record with an
extra zero qword/self-pointer and calls `00252B40(request, parameter)`. Both
descriptions conflict with the original instructions and these controls. The
incoming parameter and the setter's second argument must stay distinct; broader
interpretations of `02092734` must be checked against individual callers.
The correction is routed to FABLE through the existing contradiction queue.
