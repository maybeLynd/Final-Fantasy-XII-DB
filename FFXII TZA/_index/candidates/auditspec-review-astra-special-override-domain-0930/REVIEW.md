# SWE2-AUDIT-SPEC review of ASTRA special-action-override-domain (30754ad4b): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75), 2026-09-30. Producer: ASTRA.
Reviewed: `ASTRA-PUBLISH-SPECIAL-OVERRIDE-DOMAIN-0930` at `30754ad4b`, packet
`_experiments/evidence/special-action-override-domain/` (manifest status PRODUCER_VALIDATED_PENDING_INDEPENDENT_REVIEW),
image SHA `73461d08…21f8`. Static only; nothing was executed natively.

| request | reviewed task | commit | verdict |
|---|---|---|---|
| ASTRA-REQ-SPEC-SPECIAL-OVERRIDE-DOMAIN-0930 | ASTRA-PUBLISH-SPECIAL-OVERRIDE-DOMAIN-0930 | 30754ad4b | ACCEPT-WITH-NARROWING |

The scoped invariant holds as stated, and every clause re-derives. The narrowing is one README sentence about
the corrupt state 9, which is true only for one of the arm's two inputs (wording below).

**Clause by clause** (from [domain_indep.out](domain_indep.out) and [domain_context.out](domain_context.out); tk.py decode,
not the packet's capture driver)

- *High DWORD +AE0 zero from QWORD 2710 at +ADC.* `001CCC06 mov qword ptr [rdi + 0xadc], 0x2710` is an 8-byte store
  covering +0xADC..+0xAE3, and the immediate's high dword is 0. `rdi` is set once at `001CCB42 mov rdi, rcx`, with no
  redefinition before the store. No later access to +0xAD5..+0xAE3 occurs in `001CCB20`..`001CCFDA`. HOLDS.
- *Under a valid same-object, no-overwrite state 0..8, the control preserves 0..8 and the setter gets -1..7.* I ran a
  small interpreter over the arm's own decoded instructions `001D2DD3`..`001D2DFA`, not the prover's `step()`. It is
  closed on 0..8 for both inputs: state 0 dec keeps 0 (index -1), state 8 inc keeps 8 (index 7), and the index is
  always state-1 in -1..7. HOLDS.
- *Eight initializer words and identity.* `002F79E0 movdqa xmm0, [00D0F9E0]` (.rdata, 16 bytes) and
  `002F79E8 movdqu [022BE930], xmm0` give 241, 231, 234, 237, 229, 228, 227, 226. None is in 511..534. The setter is
  `002F7A00 mov [01EEBAF0], ecx; ret`. HOLDS.
- *Narrow-store refusal, widened bound, corrupt initial 9.* Reproduced (see Re-run). The corrupt-9 row depends on the
  input: the increment input keeps 9 and writes index 8, while the decrement input moves it to 8 and writes index 7.
  State -1 on the decrement input stays -1 and writes index -2. Both sides confirm that the arm is not a sanitizer;
  "9 stays 9" needs its input named (narrowing).
- *No all-writer, alias or lifetime closure, and no natural caller binding.* The packet does not award these, and I
  award none. For sizing:
  - Direct callers are complete in every form I swept (raw E8/E9/jcc/rel8, `rawcalls.json`, rip address-taken,
    DIR64): `002F7A00` has exactly one, `001D2DFA` in `001D1660`; `002F79E0` has exactly one, `001D03DC` in
    `001D0390`. There are no address-taken references or relocations.
  - The index cell `01EEBAF0` has one writer (the setter) and one reader, `002F8D66` in `002F8D60`, which takes
    `js` to a separate path for a negative index. No image-base or relocation form exists.
  - The word array `022BE930` has one writer (the initializer) and one address-taking reader (`002F8D74`). It lies in
    the `.data` virtual tail (no file bytes), so it is zero until `002F79E0` runs.
  - Image-wide, 9 disp32 stores overlap +0xAE0..+0xAE3. Besides the constructor (`001CCC06`) and the arm
    (`001D2DEC`), four are object stores on unidentified objects (`00184FBA`, `001881BF`, `006DD2D0`, `007049B8`)
    and three are `rsp` stack stores. None of the four is tied to this object; they are the candidate set for the
    OPEN writer closure.
- *EXP190 is not an ASTRA run.* The README says so; nothing in the packet depends on it.

**Re-run.** I ran the packet's `prove-special-override-domain.py` and both capture drivers from the repository root
into fresh files in this directory. The result and both raw captures are byte-identical to the committed
`special-override-domain-result-01.json`, `-control-raw-01.json` and `-constructor-raw-01.json`
([compare_rerun.out](compare_rerun.out); the redundant raw copies were then removed, and the result copy is kept).
The capture found the same 2 direct call prefixes with 0 unresolved, and 01EEBAF0's file value is ffffffff (-1).
The packet directory was clean before and after.

**Controls.**
- The three role controls (SSE store `w`, LEA `addr`, RMW `rw`) run inside the real capture path and would catch a
  broken role adapter, so they are sensitive.
- `narrowed_constructor_store_refused` and `widened_control_bound_refused` mutate the capture's `args` text and are
  refused by the witness table. They show that the witness table pins the text. They are not a semantic width test;
  the real guard against a narrower image store is the byte-for-byte match of every instruction against the pinned
  EXE, which does hold.
- `initial_domain_required` evaluates the prover's model for the increment input only. My interpreter covers both.

**Correction wording for ASTRA** (README "Limits" sentence and the result's `limits`):
> Initial corruption 9 is not repaired: on the increment input it stays 9 and writes index 8; on the decrement input
> it becomes 8 (index 7). A state of -1 stays -1 on the decrement input and writes index -2, which the reader
> 002F8D60 routes to its negative-index path. The arm is not an arbitrary-state sanitizer.

Limits of this review: static decode only. I did not verify that the control arm's `rdi` in `001D1660` and the
constructor's object are the same instance; that is a premise.
