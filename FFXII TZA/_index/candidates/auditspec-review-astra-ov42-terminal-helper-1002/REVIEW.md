# SWE2-AUDIT-SPEC review: ASTRA OV-42 terminal resource helper

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-TERMINAL-HELPER-1002` · Package: `_experiments/evidence/ov42-terminal-resource-helper/`
(publisher commit `d66234298`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00305640` (`BattleAction_ConsumeExecutionResources`, 189h = 393 bytes):**
  - The first unsigned 32-bit quotient (`div r10d`, `00305690`) goes to EDI. It is narrowed with `movzx edx,di` for
    `309110` and `308FF0` (`003056C1`, `003056CC`).
  - On the row-type path it re-reads the binding (`02EBF138`, `20E600`) and divides again (`00305783`), then passes
    the **full 32-bit** quotient as EDX with `ECX=0Dh` to `253770` (`00305785..003057A5`).
  - Discriminator: q = 65744 → cost index 208 (low 16) versus counter 65744 (full width). This is mathematical, not
    a native or natural state.
- **Mode:** `r12d = r8d` at entry, normalized as `16 + (r8d != 0)`. The exact caller site `00304F38` passes
  `r8d = 1` (`00304F2C`), which gives 17.
- **NULL unit:** the early NULL/`+698h`/`byte+5` branch gates only the `E58h`/`DC8h` resets (`003056AE..003056BA`).
  Later, `[rbp+698h]` and stats `+28h` are read unconditionally after the callees return.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (proof-02, `2fd6d8e8`) re-run: exit 0, output **byte-identical** to `result-02.json`.
- `control.py` (`fca182c7`) re-run: exit 0. The five artifact refusal cases (false extent result, false capture
  wrapper, missing metadata, changed physical extent, binding false extent) are identical to retained.

## SWE2-AUDIT-SPEC consumer note

Consumers of the earlier helper and of the `ca2dd6483` binder packet must also consume the binding-qualification
gate: an old producer exit-0 receipt alone is insufficient under the repaired artifact gate. Callee effects,
initialization and normal reach stay OPEN.
