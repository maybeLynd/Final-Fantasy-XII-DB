# Audit-spec review: SECTION-03 reward bindings (second auditor)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: overlay merged `21f25545b`,
owner review `2ff93a3ff`, AUDIT-SEM review `auditsem-review-section03-1001` (`f41194772`)
Board task: `FABLE-REQ-AUDITSPEC-SECTION03-REVIEW-0930` (register row GR-16)

## Disposition

The task is satisfied by a delivered substitute verdict: `auditsem-review-section03-1001`
explicitly stands in for this request while FABLE is inactive (user-authorized 2026-10-01) —
**ACCEPT-WITH-NARROWING** with narrowing N1 (reproduction holds only against the pinned
pre-image of the historical reward-binding checker, which ASTRA's seal later changed). GR-16 is
restated ANSWERED on the register and the three pages' pending markers are updated.

## This lane's independent check of the same material

I did not take the verdict on trust. Byte-verifying on the certified image (`73461D08…`):

- `002F8BB0` (EXP computer): `002F8BC7 xor esi,esi`; `002F8BCF test rcx,rcx` (NULL recipient);
  `002F8C34 call 003135C0`; shared path loops ebx 0..3 through `0031B810` with `002F8CE2 cmp ebx,4`;
  `002F8CD8 cmp byte [rcx+4],0x1A` excludes the 0x1A recipient from the divisor count;
  `002F8D1C cdq; 002F8D1D idiv ebp` — the divide is **independent of rdi**: the
  owner-review/audit claim "a NULL recipient still divides in shared mode" is byte-true, and the
  FABLE-contract correction ("display shows undivided award" is wrong in shared mode) stands.
- `002F8CEC test ebp,ebp` — empty roster returns before row reads; `002F8D21 test rdi,rdi` —
  NULL skips effect modifiers. Both hold.
- §15a (falsification pass 1) survives at HEAD, kept whole per the owner review's condition —
  CONTRACT-experience-and-licence-award.md line 355 ("From HEAD's §15a (kept whole)").
- `002367E3`/`002367EE` `cmp edi,0xff; mov ecx,0xffff; cmovne` — the 0xFF→0xFFFF sentinel
  widening AUDIT-SEM's table describes (spot-verified).

## Verdict: concur — ACCEPT-WITH-NARROWING (N1 stands; add nothing)

The substitute review's narrowing is the right one: the sealed checker changed after the
pinned pre-image, so "reproduces" is bounded to that pin. No further narrowing required.
This lane's contribution is confirmation, not a replacement verdict.
