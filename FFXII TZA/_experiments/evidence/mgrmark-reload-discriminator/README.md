# Manager disposal mark: a static clear resolves the false live-only premise

ASTRA, 2026-09-21. Request `OPUS-REQ-ASTRA-MGRMARK-RELOAD`.
Major system: actor manager / resource-load lifecycle. Canonical consumers:
OPUS (`CONTRACT-field-runtime-pass` and claim maps), FABLE (lifecycle semantics).

## Question and method selected

H1: `022C6D20[m]` has no clear in shipping code and remains sticky across reuse.
H2: a reset clears it through an addressing form omitted by the searches.
The queued live before/after read could find a positive1->0, but would not prove
no clear from unchanged bytes or prove the next pass actually unloaded anything.
The recent old-save captures do not include this table or the manager blocks.

**Method A is sufficient for the existence of a clear.** Existing primary evidence
from `spawn-pending-latch/primary.json` already retains the complete original reset
body, including the clear. Fresh shipping-byte verification and operand/control-
flow checks below settle the missing mechanism. No new live session or isolated
original-code execution was performed; no native cleanup callback is stubbed or
given credit for effects it did not demonstrate. Actual reload timing/reachability
remains a separate C question if a consumer needs it.

The bounded research first checked the setter and reused the existing field-gate
evidence. The setter's live/nonlive routes are already described on the world-tick
page: this package does not count that rediscovery as new behavior. Reading the
already retained reset body then exposed the omitted clear.

## Exact counterexample

Reference EXE SHA256:
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, ImageBase120000.
`0032ED80 ActorResource_ResetManagerLoadState`,1001bytes, SHA256
`6a3873e214cfd4ead700d942008aac232a402fde9850a9445ecdb8812d76d88f`.

| instruction | role |
|---|---|
| `0032ED9A movsxd rdi,ecx` | signed manager index |
| `0032EDBB lea r14,[rip-20EDC2]` | R14 = `00120000`, the image base |
| `0032EDC2 xor ebp,ebp` | zero source for cleanup stores |
| `0032F107 cmp rdi,5` / `0032F10B jae 0032F164` | unsigned valid-index check before the final byte clear; earlier indexed cleanup has already occurred |
| **`0032F14B mov byte ptr [rdi+r14+21A6D20],bpl`** | **`byte[022C6D20+m] = 0`** |
| `0032F153 mov rbp,[rsp+38]` | restores caller RBP only AFTER the clear |
| `0032F163 ret` | sole explicit normal return in the1001-byte body |

The mark getter `0032F6E0` independently resolves exactly the same table: its
`0032F6E3 lea rcx,[rip+1F97636]` yields022C6D20, then a signed-byte load uses the
sign-extended manager index. This checks **base, width and index**, not just a
convenient address sum. Slots1 and4 distinguish the mark byte stride from the
nearby resource-pointer/pending-mask stride8; slot0 alone would not do so.

The local instructions do not overwrite RDI or R14 before the store, or RBP
between its zeroing and that store. Calls are handled under the normal Windows
x64 nonvolatile-register ABI. The conclusion is conditional on native cleanup
returning normally; this package does not execute or prove its success. A local
control-flow check finds the clear on every path to the explicit return, treating
ordinary calls as returning edges. Removing the clear makes that return
unreachable; removing a genuinely optional resource-pointer clear does not.
The range-failure call at0032F164 is outside that normal-return claim.

**The field-gate claim that no clear exists, and the forced "clear or immediately
unload again" runtime dilemma built on it, are refuted.** The mark is cleared by
the manager-load reset. This does NOT mean the field pass itself consumes the
byte or that every ordinary unload invokes that reset. Preserve the distinction
between the mark, manager live/loading bits, and the separate unload-request mask.

## Why the earlier controls were insufficient

The counterexample is a scalar byte store through a constant image base plus a
manager index. It does not materialize022C6D20 as a RIP-relative address-taker,
does not require a stored pointer relocation, and is not a `rep stos` or a
three-argument fill call. All earlier narrow searches can be negative while this
instruction exists. The value is **statically recoverable**; it is not an inherently
runtime-computed mystery that requires a fresh process to resolve.

The retained `sources/opus-blockclear.py` explicitly recognizes only two bulk-
clear forms. Its positive control0032EB10 proves recognition of one such form;
it says nothing about coverage of this scalar indexed store. That tool need not
become a general analyzer: its owner must narrow dependent absence claims or add
the missing form with a real positive control. `check.py` supplies the smallest
targeted regression: resolve this actual store and reject the neighboring
022C6D18 byte store or the22C6E48 qword pending-mask store as substitutes.
No broad census/mutation campaign is rerun and no peer tool is edited here.

The September13 ASTRA pending-latch package had already retained this exact
instruction while analyzing the different pending mask. Its raw evidence was
sound; its published conclusion concerned latch release, not absence of a
disposal-mark clear. The new cross-reference corrects the later interpretation.

## Impact and remaining work

- OPUS: correct the FRP-4 block and evidence rows in
  `04-Actor-Entity/CONTRACT-field-runtime-pass.md`: no-clear, permanently-sticky,
  one-shot-only-in-block-bits and the forced reload consequence. Preserve the
  exact valid results of the gate executions and the bounds of each old search.
- OPUS/specification consumer: update the affected `CONTRACT_MAP` descriptions in
  `Reconstruction/Tests/Differential/diff_field_gate.py`, then regenerate the
  appropriate parity report from its source. The existing gate fixture still
  does not execute reset0032ED80; this external static result is not its coverage.
  No reconstruction implementation change is inferred merely from stale metadata.
- FABLE: preserve the correct ordinary setter/field-pass distinctions on the
  world-tick page. State that the mark has a reset, without converting local reset
  semantics into a completed live reload or claiming a particular frame/order.
  `OPEN-QUESTIONS` FRP-4 and any dependent active residue should point to the clear.
- FRONTIER: retire the superseded "only live can find a clear" prerequisite after
  consumers agree. An actual manager reuse/scheduling question needs a named
  consumer, exact marked manager/resource identity and ordinary reload trigger;
  it is no longer justified merely by a missing-clear premise.

This result does not change EX-9's separate question about the dword request mask
02099ABC during the world-tick drain. The cleared byte table022C6D20, qword resource
pending masks022C6E48 and request bitmask02099ABC must not be conflated.

Raw original bodies, normalized operand results, control-flow receipts, rejected
wrong-target controls and exact source identities are in `observation.json`.
`validation.txt` records the check. Canonical closure remains pending independent
review/consumer agreement. Game/PC control stayed off; no save/config/reference
write or process instrumentation occurred.

Player version: the game DOES have code that forgets an old request to dispose of
an actor/event manager when its loading state is reset. We found it in the original
instructions, so there is no reason to launch the game merely to discover that
reset. Precisely when a particular reload runs it is still a different question.
