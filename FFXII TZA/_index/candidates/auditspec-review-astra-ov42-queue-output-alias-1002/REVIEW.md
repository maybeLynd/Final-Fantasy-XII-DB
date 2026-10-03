# SWE2-AUDIT-SPEC review: ASTRA OV-42 queue output alias

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-OV42-QUEUE-OUTPUT-ALIAS-1002` · Package: `_experiments/evidence/ov42-queue-output-alias/`
(publisher commit `4fe271b46`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC re-derivation from the shipping image

- **`00309C00`, available case:**
  - writes the action DWORD through RDX (`00309C13`, when non-null);
  - then reads the unit global `022C218C` and writes it through RCX (`00309C20`, when non-null);
  - then resets `022C2178` = -1 and returns 1.
  - With both outputs NULL it still resets and returns 1, so the queue entry is consumed.
- **`00309C00`, unavailable case** (`022C2178` == -1): returns 0 with no own write.
- **Ordering consequence:** the action store comes before the unit store. If the two outputs overlap, the unit
  value overwrites the action bytes; if they are the same buffer, it ends holding the unit value.
- **Bridge `00348330`:**
  - Resolves the two references with `2650B0`: first → RSI, second → RBX. It calls `309C00(rcx = rbx, rdx = rsi)`.
  - After the primitive returns it reads `dword [rbx]` and `dword [rsi]` unconditionally (`003483A9`,
    `003483B1`), even when the primitive returned 0.
  - So the primitive's NULL guards do not make the whole bridge safe.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (proof-02, current `6734ed9d`) re-run: exit 0, output **byte-identical** to `result-02.json`.
- control-02 (`control.py`, `8cdbf47b`) re-run: exit 0, `control-result-02.json` **byte-identical**. Its two
  refusals are missing queue source and coherently re-pinned output width.
- control-01 (`control-before-parent-manifest-01.py`) is archived. It now refuses ("required complete producer
  positive missing") because `prove.py` has since changed, which is the documented reason it was superseded. It
  gets no credit, as the package says.

Source-global aliases, actual descriptors and backing, lifetime, the natural interpreter and command reach stay OPEN.
