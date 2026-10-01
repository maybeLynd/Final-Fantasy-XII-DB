# OV-36: a queue slot delivers its callback at most once, and an owner has one live request (FABLE, Claude Opus 5.5, 2026-09-29)

**Box (OV-36, `02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` §8):** "Complete callback
single-delivery/reuse and relevant scheduling/reentrancy obligations." The register classes the re-entrancy universality
part as superseded under OV-2's limit; the delivery specifics are static.

[`delivery.py`](delivery.py) runs D, P, H, O and R: FAILS 0 ([output](delivery.out)). Static.

- **D.** The pump `0032E070` dispatches the head slot only in states 1–6. State 0 is never dispatched.
- **P.** At all six delivery sites, the pump writes slot state 0 and recycles the slot (`0032EC40`) before the loop runs
  again:
  - the completion helper, three sites;
  - the error completion, two sites;
  - the cancel callback, one site.

  **So a slot delivers at most once.**
- **H.** The helpers call the completion pointer without clearing it. Uniqueness therefore comes from P, not from the
  pointer being consumed.
- **O.** The armer admits only owner state 0, and the producer only state 2, which it leaves at 3
  ([OV-34's record](../ov34-state1-owner-fable/README.md)). So an owner never has two queued slots. The same owner address
  across successive requests (the page's §8) is sequential, not concurrent, and a recycled slot cannot deliver an earlier
  request's callback.
- **R (bounded).** The owner callback runs before its slot is reset. Its direct callees do not include the pump: the
  resolve, the release, the unpin, the dispose and the registration. Whether any of them reaches the pump transitively is
  not claimed. That is the re-entrancy part the register leaves under OV-2's limit.

**For OV-19.** Its "callback single-delivery/reuse preconditions" half is the same answer.

run: delivery.py at b6061b9f3, FAILS 0.
