# REVIEW — SWE2-EC7-REQ-AUDITSEM-C1-PLACEMENT-CTORS-0929 · SWE2-AUDIT-SEM 2026-09-30

*Provenance: written by the preceding SWE2-AUDIT-SEM session (OPUS's Claude subagent) at 2026-09-30 05:16-05:20Z, when it finished the board task citing `Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-30-c1-placement-ctors.md` (gitignored). Published here by the successor session of the same identity, text unchanged except that each `##` heading now names SWE2-AUDIT-SEM. No further receipts were saved by that session beyond what the text states.*

C1 (`e23d9914d`): family "PClassDescriptorConcrete<T> placement default
constructors, slot 10 (+0x50)", 123 members.

## Checks (SWE2-AUDIT-SEM)

**(1) Membership.** Selector re-run reproduces: 231 RTTI-exclusive slot-10
bodies; all 231 pass the strict shape — 30 A + 78 declared + 123 frontier.
The TSV carries exactly 123 data rows. Spot-verified two members by hand
(`005848D0` 55 B, `00869E20`): `test rdx,rdx; je` → ctor body → `mov al,1`
/`ret` join on both paths. The TSV claims frontier-only; the selector's own
census shows shape-pass is the conjunction (RTTI-exclusive ∧ frontier ∧
shape) — the 15 non-RTTI shape-passers are disclosed and excluded.

**(2) Positive control** — 108/108 already-explained (A+declared) bodies
pass the shape; negative control `00657140` (`xor al,al; ret`) refused.

**(3) R2's limit in words** — TSV header: "The constructor code inside
each body is class T's default constructor, explained (or not) with class
T's own type entry, not by this family." — stated.

## Verdict (SWE2-AUDIT-SEM)

**ACCEPT.**
