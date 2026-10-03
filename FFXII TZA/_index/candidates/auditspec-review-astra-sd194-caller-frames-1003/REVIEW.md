# SWE2-AUDIT-SPEC review: ASTRA SD-194 caller frames

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session) · 2026-10-03 ·
Task: `ASTRA-REQ-SPEC-SD194-CALLER-FRAMES-1003` · Package: `_experiments/evidence/sd194-caller-frames/`
(publisher commit `ace5507ec`), image pin `73461d08…21f8`.

## SWE2-AUDIT-SPEC verdict: ACCEPT

The two legs do **not** address the same name buffer. The second is 48 bytes higher, and the possible 260-byte spans
overlap by 212 bytes. Neither disjointness nor surviving old bytes is implied. This is a static source proof, not an
execution.

## SWE2-AUDIT-SPEC re-derivation from the shipping image (S = entry RSP of `00331990`)

- **`00331990` (52 B):**
  - `push rbx / sub rsp,20h`, then mode 0: `call 378A60` with `r8d=0` (`003319A4`).
  - Then `add rsp,20h / pop rbx` restores RSP to S, and mode 1 is a tail `jmp 378A60` with `r8d=1` (`003319BF`).
  - So `378A60` is entered at S−0x30 for mode 0 (8 push + 0x20 + 8 return address) and at S for mode 1.
- **`00378A60` (273 B):** `push r14 / sub rsp,30h`, then `call 377DC0` (`00378B2B`). The callee is entered 0x38 + 8
  bytes below `378A60`'s entry: **S−112** for mode 0 and **S−64** for mode 1, matching the record's table.
- **Name input:** with the accepted loader offset of −328 (consumed from the SPEC-accepted SD-194 packet, not
  re-derived), the inputs sit at S−440 and S−392. They are 48 bytes apart, and 260 − 48 = 212 bytes of overlap.

## SWE2-AUDIT-SPEC reproduction (disposable copy, repository-root cwd)

- `prove.py` (proof-02, `be8c4760`) re-run: exit 0, stdout identical, output **byte-identical** to `result-02.json`.
- `control.py` (`7ae4714b`) re-run into a fresh `controls-01`: exit 0, stdout identical
  (`THREE_ACTUAL_PREREQUISITE_REFUSALS`).

Natural absent-name contents and field entry, the mode-0 skip and opaque writes, queue acceptance, lifetime and
presentation stay OPEN.
