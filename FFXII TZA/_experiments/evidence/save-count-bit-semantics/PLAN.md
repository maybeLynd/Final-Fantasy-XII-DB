# Raw Save count bits versus the signed pseudocode

Question: for count bits with the sign bit set, does original Save skip work like the contract's signed `for (int i=0; i<count; i++)` illustration, or enter the same unchecked countdown used by other nonzero counts? Consumer: OPUS ABI/procedure and SWE2-CONTRACT Save/Restore exact interface description.

Method A suffices: reuse exact retained 89-byte shipping Save. Distinguishing instructions: TEST ECX/JE zero gate, MOV R10D,ECX zero extension, SUB R10,1/JNE loop. Examine the first-iteration path for raw zero/one/high-bit/all-ones count. No billion-item run, fault claim, safe malformed-input guarantee or inferred original C declaration. Counts outside the already documented structural safe range are not valid uses; this question clarifies what the native precondition protects against and the limits of signed pseudocode.

Controls: exact complete body/hash and decoded gate/register widths/loop backedge; zero skips to depth store, one traverses once in the source calculation, high-bit count is nonzero and zero-extended rather than negative-skipped. Reject instruction/branch mismatch. Keep source calculation separate from original execution. Any fault, completion, allocator/scheduling or normal caller claim remains outside.

Selection lessons: the 32-item boundary is already answered in contract sections14/15; EXP070 already proves disabled one-step returns zero rather than raw seed minus one. Do not replay either. Prior Save pointer-slot result is distinct and in review. Do not take peer S05 ordinary pair work or edit a claimed canonical consumer.

Fresh supported board/current and explicit own bounded claim precede derivation. Byte freeze must reuse existing * -text and test Git filtered/unfiltered equivalence; published/raw results immutable. PC OFF, S19 two attempts/ten minutes spent, extra recovery unapproved. Full accepted L1+L2/final audit NOT_MET.
