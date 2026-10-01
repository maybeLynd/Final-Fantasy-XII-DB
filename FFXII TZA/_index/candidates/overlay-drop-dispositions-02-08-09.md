# SECTIONs 02 / 08 / 09 overlay: per-token drop dispositions for the queue contract (OPUS, 2026-09-25)

This is the gate file for `overlay-publication-plan.md` ruling 2, covering
`02-Resource-And-Asset-Pipeline/CONTRACT-resource-request-queue.md` (OPUS). The owner-merge of ruling 3 is
done in the worktree: see the overlay's §6 "Restored by the owner" and its §13 "Invariant verdicts".
Nothing is published by OPUS; FRONTIER publishes. The census was re-run after the merge.

| token | disposition | where / why |
|---|---|---|
| `003EB050` | **restored** | §6: `0032EA90` → `0032EA99 call 003EB050` (read-layer reset), re-read |
| `00379E30` | **restored, and corrected** | §6: HEAD cited it among the `0032E040` pump drivers, and that is right (`00379E41`). The asking-form claim is carried by its real callers, `0022B737` / `0022B837` / `00314609` / `0050E1E4` (`mov ecx, 1`). |
| `0036C1F0` | **restored** | §6: the staged-selection push; only entry is the tail jump at `0036C1DF` |
| `0032E721`, `0032E730` | (not dropped) | §13 cites the idiom's range |
| `0032E724`, `0032E728`, `0032E72E`, `0032E735` | **restated** | the individual instructions of the signed-bias alignment idiom; the overlay's I6 wording and §13's range `0032E721`–`0032E730` carry it |
| `0035EB70` | **restated** | EXP-146's scripted pacer; the overlay's §13 keeps "all external service/pacer … bridges are named in the source" |
| `0046DFE0` | **restated** | the stall-loop callee; the overlay keeps the full-pool retry loop, and §6 names the loop `0032E040` / `0035EA30(0)` drives |

**Other files in these sections:**

- `CONTRACT-resource-input-ownership.md` (28 tokens, sections 06/08/09/10) is FABLE's contract.
  FABLE's ruling is **RESTORE all** (`fable-overlay-dispositions-2026-09-25.md` §3), and that
  disposition stands for those rows.
- `the-resource-request-queue.md` loses nothing.

**Status: every census row for the OPUS contract is disposed.** FRONTIER publishes; OPUS re-verifies.
