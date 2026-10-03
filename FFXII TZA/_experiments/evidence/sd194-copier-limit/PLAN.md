# SD194 namespace copier: the actual limit prerequisite

Question: does `002DF880(..., R9D=259)` establish a first NUL inside 260 destination bytes, including when the namespace entry is absent? Does a zero/negative limit suppress all writes?

Hypotheses: (1) limit is destination capacity including NUL; (2) limit is a character count followed by an extra NUL; (3) absent entries initialize an empty destination; (4) absent entries leave it untouched. A separate boundary is the unconditional first byte copy and its next-byte termination check.

Method A: consume the already captured, SPEC-accepted complete 89-byte function and caller argument. Bind every operation to shipping bytes and reviewed access annotations; prove the counter/write invariant for the entire signed-32 limit domain. Focused boundary calculations and actual reducer refusal controls check the prerequisite path. These are analysis controls, not execution of original code.

Why sufficient: the function has no calls and its complete control flow contains the entire bounded copy. Original-code or live execution would add samples to a deterministic local bound. Neither this proof nor a composed harness can reveal the absent-entry inherited stack bytes or which fields ordinary gameplay loads.

Reference: EXE SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`, base `0x120000`; retained packet `_experiments/evidence/sd194-stale-name-slice`. Initial state: valid namespace table/index/entry accesses; non-null branch has valid source/destination spans through every selected access, normal ABI and no concurrent modification. General termination/write bound needs no source/destination-disjoint assumption; the formula for an unchanged source's next NUL does. No real process state is assumed or observed.

Acceptance: exact complete bytes/operations/role annotations and successful upstream receipt; closed two-return CFG; a proof that writes are bounded by max(1, signed limit)+1 on the non-null branch, with a separate no-write null branch. Caller 259 specialization must prove offsets 0..259 only. Reject missing/failed upstream, incomplete or modified source, and wrong decoding/roles. Controls include limits INT_MIN/-1/0/1/2/259/INT_MAX, short/at-limit source termination, and an empty source followed by nonzero bytes.

Consumers: SWE2-DATA's SD194 and OPUS's copier/buffer contract. Required change: distinguish count from capacity and successful lookup's bound from the absent-entry exception; preserve actual inherited bytes, natural field entry, and interpreter/resource acceptance as OPEN. Independent SPEC review must precede semantic acceptance. Existing builder proof/census is not repeated.

Stop/escalation: any original identity, receipt, annotation or invariant failure stops reduction. Native/invalid-span effects are outside the claim; do not manufacture a live run to settle them. No game, save, config, instrumentation or reference write; all helper processes finite and terminal status checked.
