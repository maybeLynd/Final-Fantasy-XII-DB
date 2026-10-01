# 00533B20 restores R12 on its normal return (OPUS, 2026-09-30)

Consumer: `06-Movement-And-Navigation/CONTRACT-heading-speed-to-position-delta.md` (CON-172), the `0x67` reader.
Static, the certified image; no original-code execution, no live run.

## Why (OPUS)

`004607C0` zeroes `r12d` at `00460A5B`, then calls `00533B20` three times (`00460A9A`, `00460AB6`, `00460AC5`), then
compares the `0x67` flag with `r12d` at `00460ACA`. ASTRA's accepted packet (`8969fe745`; ACCEPT by SWE2-AUDIT-SPEC at
`cd86f404d`) grounds R13, RSI and RBX through `00533B20`'s pushes. It does not cover R12, which `00533B20` does not push
and does write (`005341AF`, `0053450F`).

## Result (OPUS, `r12_restore.py`, output `r12_restore.out`)

- Decoded from the entry over direct branches: 1,653 instructions (ASTRA's count), one `ret` at `00536055`.
- **S1.** The spill `00533C56 mov [rsp+0x390], r12` dominates both R12 writes. Removing it makes both unreachable
  from the entry, and no R12 write precedes it, so the slot holds the caller's R12.
- **S2.** The reload `00534540 mov r12, [rsp+0x390]` lies on every path from each write to the `ret`. Removing it
  makes the `ret` unreachable from both writes.
- **S3.** No other direct store covers `[rsp+0x390]`. RSP changes only at `00533B29` (`sub`) and `00536046` (`add`),
  so the spill and the reload address the same bytes.
- **Verdict:** on a normal return, `00533B20` gives the caller's R12 back.

Controls:
- **C1.** The same checker on R13 reports "pushed" and claims no spill.
- **C2.** A private copy whose reload is re-encoded to load R13 instead (`4c8ba42490030000` →
  `4c8bac2490030000`, same size) fails.

## Conditions and limits (OPUS)

These are the same conditions as ASTRA's packet:
- a normal return;
- calls inside `00533B20` return normally with a coherent RSP;
- no aliasing store into the slot through a pointer (this is a direct-store check only);
- the stack-cookie check at `00536038` passes (not observed).

This says nothing about what `00533B20` computes. It also does not show that `002F2530` returns non-zero (the gate on
`004607C0`), or that the loop runs live.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The contract text marks the R12 clause as
pending that review.
