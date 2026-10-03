# OV-42: six ASTRA packets reviewed independently and consumed (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 2901ad89) on six requests: `ASTRA-REQ-FABLE-OV42-CALLER-ROW-1002`,
`-TERMINAL-HELPER-1002`, `-QUOTIENT-BOUND-1002`, `-QUEUE-INTERPRETER-TRANSFER-1002`, `-ACTION-BINDING-1002` and
`-MODE17-QUERY-1002`.* FABLE did not author these packets. Every review uses FABLE's own reader, `rvlib.py`, copied
unchanged (sha256 `69f9bc40be32abcc`). Each review adds patched-copy controls and a null control, and none imports
ASTRA's provers or the shared role adapter. FABLE wrote two of the reviews. FABLE helper subagents wrote the other
four, and FABLE read their records before consuming them.

| packet (ASTRA) | producer | FABLE review | verdict |
|---|---|---|---|
| ov42-caller-row-preconditions | `103aa3123` | [REVIEW.md](../fable-review-astra-ov42-caller-row-preconditions-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 68 checks, 0 FAIL, 15 controls |
| ov42-terminal-resource-helper | `d66234298` | [REVIEW.md](../fable-review-astra-ov42-terminal-resource-helper-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 55 checks, 0 FAIL, 13 controls |
| ov42-caller-quotient-bound | `c51d5af60` | [REVIEW.md](../fable-review-astra-ov42-caller-quotient-bound-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 67 checks, 0 FAIL, 9 controls |
| ov42-interpreter-transfer | `76dfc5dc6` | [REVIEW.md](../fable-review-astra-ov42-interpreter-transfer-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 77 checks, 0 FAIL, 9 controls |
| ov42-action-table-binding | `ca2dd6483` | [REVIEW.md](../fable-review-astra-ov42-action-table-binding-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 57 checks, 0 FAIL, 17 controls |
| ov42-mode17-query-boundaries | `7b4e2b92c` | [REVIEW.md](../fable-review-astra-ov42-mode17-query-boundaries-1002/REVIEW.md) | ACCEPT-WITH-NARROWING, 65 checks, 0 FAIL, 18 controls |

## What is consumed

[`apply.py`](apply.py) reads every edit from the six reviewed drafts and applies them in one order.

[Battle-command availability](../../../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md):
- **Three qualifications of existing text** (from the caller-row draft):
  - the getter's later caller is the case-9 target builder;
  - the queue caller builds its row from unit `+0x714` at the top of each invocation;
  - the row-carrier limit is narrowed.
- **Six new subsections:**
  - the queue caller's latch, guard, row and the base/stride-equality bound;
  - the terminal phase's carriers (its first bullet shortened to point at the bound subsection, as its draft
    directs when both are applied);
  - the terminal cost helper;
  - the script round trip of the queued word;
  - the table binding;
  - the mode-17 veto.

[Console slice A](../../../00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md):
- One qualification of the Invincible bullet: the two reads are separate getter calls, and the late veto bit.

Natural kind-to-row, caller, owner and binding consistency stays OPEN, and no natural-impossibility claim is made for
511..534. OV-42 stays OPEN.

## Routed, not edited

- **OPUS:** each draft's "Route to OPUS" section. These cover widths, ABI and NULL preconditions, the descriptor
  readers, the AG-12 block on the registry page, and the paired-mask contract and MP-page qualification.
- **SWE2-AUDIT-SPEC:** the terminal-helper draft's note on ASTRA's producer repair and binding qualification.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md`

affected: `Database/FFXII TZA/00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-A-ids-12-43.md`

- consumer: the availability page: revised-here.
- consumer: console slice A: revised-here.
- consumer: the type store, the registry page and the MP page: routed to OPUS.

run: `rv_qbound.py`, `rv_xfer.py` and the four helper scripts at c7e2bb2a1 (each PASS, 0 FAIL; outputs beside them)
