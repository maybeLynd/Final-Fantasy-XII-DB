# Review `ASTRA-REQ-SPEC-HEADING-ZERO-ABI-0930`: verdict ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author). This lane was run by the FABLE session's executor `73162e75` on 2026-09-29.
Producer: ASTRA. The consumer is OPUS (`ASTRA-RETURN-OPUS-HEADING-ZERO-ABI-0930`). No FABLE authorship or direction
was found: FABLE's heading-contract commit `9ca3df0ac` touches none of these sites.

Reviewed: `8969fe745`, the two immutable packets `_experiments/evidence/heading-6b-zero-definition/` and
`heading-native-helper-saved-registers/`. Image `73461D08…21F8`, static; no execution of original code.

## 1. The producer's checkers reproduce

I ran the three canonical drivers from the repository root with the pinned interpreter, exactly as each
`terminal.json` records. Each exits 0. **Each fresh JSON is identical to its committed result**:

- `r13-dominance.py` → `result.json`;
- `callee-saved-registers.py` → `result.json`;
- `callee-abi-feasibility.py` → `callee-abi-feasibility.json`.

Every file in both packets hashed the same before and after the run, so reproducing does not overwrite the receipts.
Both drivers assert the image SHA-256.

**The corrected sibling binding is real.** `callee-abi-feasibility.json` hashes to `fd6f1845…0e72`, the value the
driver asserts. A copy of the packet with one byte of that sibling changed makes the driver fail with
`AssertionError` (rc 1). So the v1 mutable-path input is excluded in fact, not only in the manifest.

## 2. Independent re-derivation (`hz_indep.py/.out`: pefile and capstone, without the producer's `reg_tracking.py`)

**`00529D50`, 917 bytes, 187 instructions, 32 blocks:**

- The entry reaches both the compare `0052A063` and the store `0052A06C`. With the block holding
  `00529FEC xor r13d,r13d` removed, **neither is reachable**. The XOR dominates both.
- The body's only R13 writes are `00529FEC` and the epilogue restore `0052A0AA`. Nothing writes R13 between the zero
  and the store.

  *Disclosed:* my first run flagged `0052A01F cmp r13w, ax` as a write. It is a read, and the checker was corrected
  and re-run.
- Two calls cross the zero-to-compare region: `0052A03A` and `0052A05E`, both to `00533B20`. Their normal return and
  R13 preservation are the package's stated conditions.
- **Controls:**
  - the package's own same-size mutation (`00529E48` jcc retargeted to `0052A063`) produces a bypass;
  - removing an unrelated later block (`0052A080`) leaves both uses reachable.

**`00533B20`, 9,526 bytes, 1,653 instructions, decoded exactly to its declared end `00536056`:**

- The prologue pushes `rbx`, `rsi`, `r13`, `r14`, `r15` and then does `sub rsp, 0x3A0`.
- There is **one** `ret` (`00536055`), after `add rsp, 0x3A0` and the pops in reverse order.
- There are **no** jumps leaving the body and no indirect jumps (`exits_533B20.out`).
- The only `rsp` adjustments are the prologue `sub` and the epilogue `add`.
- There are **no** direct `[rsp+d]` stores into the pushed-register area `[rsp+0x3A0, rsp+0x3C8)`.
- So on a normal return, R13, RBX and RSI are restored from their own push slots. This matches
  `STATIC_NORMAL_RETURN_SAVE_RESTORE_CONDITIONAL`.

## Verdict: **ACCEPT**

The evidence supports the claims exactly as scoped:

- a conditional local-zero definition dominating both uses, under the stated call conditions;
- a normal-return save and restore of R13, RBX and RSI in `00533B20`, with coherent RSP and no direct store into the
  saved slots.

The package's own limits stand and are not widened. This does not cover:

- exception paths;
- stores through an RSP alias (for example `lea reg, [rsp+…]`) or through a callee;
- the natural-state or class-stability question;
- the helper's full semantics.

No precision is needed. Nothing here routes to ASTRA.
