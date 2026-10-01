# Approach angle: a fixed divisor behind a register

Player view: one movement-angle calculation uses the register XMM9 to divide, but that register holds180, the degrees-to-radians conversion constant. It is not an unknown value that can approach zero. This narrows a database question; it does not show which approach angles the player actually encounters.

**Method A only.** Original1061-byte catalog span `00339630`, complete bounded decoding and direct caller graph, shipping constant bytes, and an explicit ABI assumption for opaque calls. No original/native/emulator/live execution, PC controls, memory observations or writes. [PLAN.md](PLAN.md) names the competing explanations and controls.

The current maths page's53-caller residue says the register-divisor site `00339880` can grow without bound, unlike the literal180 divisor at `0033DC99`. Following the producer one hop distinguishes these explanations:

```
00339723 MOVSS XMM9,  dword[008F3138]   ; 43340000 = 180.0f
00339735 MOVSS XMM10, dword[01CEBC50]   ; 40490FDB = stored pi
...
00339871 IMUL EAX,EBX,90               ; low32 product
00339874 MOVD XMM0,EAX
00339878 CVTDQ2PS XMM0,XMM0            ; signed32 -> single
0033987B MULSS XMM0,XMM10
00339880 DIVSS XMM0,XMM9
00339885 CALL 0033CB70
```

Preserve that instruction order and the stored single-precision constant. It is not replaced by real-number algebra or called bit-exact here. Shipping bytes, RIP targets, widths and constant sections are retained in `result.json`; constants are source values, not sampled runtime values.

Every bounded direct path from normal entry reaching00339880 crosses both constant loads. The loopback00339958→00339781 stays after the loads. The only local XMM9 writes are the load and epilogue restore00339A02; removing that restore from the graph does not hide the division. XMM9 is saved at0033971A. XMM10 has the corresponding load/restore pair. All conditional edges are included, calls are opaque fallthroughs, and no computed branch or external direct jump is guessed.

Calls matter: the [Microsoft x64 calling convention](https://learn.microsoft.com/en-us/cpp/build/x64-calling-convention?view=msvc-170), Caller/callee saved registers, requires the low128bits of XMM6–XMM15 to survive returning calls. This is an **explicit precondition**, not a dynamic test that every callee obeys it. No exceptional/nonconforming call, external entry into the middle, code intervention or upper-YMM preservation is certified. Unchanged reference constant memory is also assumed.

Under those preconditions the divisor is fixed, finite and nonzero. The variable/near-zero-denominator rationale is refuted for this site. A coarse bound is possible without knowing upstream acos inputs: signed32-to-single has magnitude at most2^31; stored pi is less than4, so completed multiplication and division by180 remain finite with a weak magnitude bound2^33. This is a conditional safety bound, **not a bit-exact result**. It is far too weak to show an angle is at most4pi or to exclude the normalizer's fast path. No actual upstream angle, native rounding/exception state, invalid-conversion continuation, imported acos domain or gameplay reachability is established.

The actual capture invokes the shared reviewed `reg_tracking.written` and `op_kind` by default for register definitions and focused save/load/restore memory roles. Its exact source is retained. No direct raw memory-access-flag classification bypass is used. A labelled private same-sized source change loads XMM8 instead of XMM9 at00339723, preserving the RIP target. It removes the reaching XMM9 constant definition; the role/control check detects it and exact original-body binding rejects it. No mutated machine instructions were executed. This tests the producer path actually used, not just a helper's existence.

FABLE should correct only this caller's register-divisor/unbounded-growth rationale in the maths page. Keep the40 unresolved operand producers and the overall53-site question open. OPUS can use the exact ABI/units/preconditions; do not bulk classify callers or infer combat outcomes. The consumer preimage is retained. The readonly checker verifies source/graph/constants/actual policy controls and manifest; independent review and canonical incorporation remain separate.

One supported CURRENT refresh failed with a TEAM.json read permission error. The exact error is retained; subsequent supported boardcheck passed epoch3 and refresh succeeded. Cause is unassigned; no lock reaped, guard bypassed or board restored. The43 claim is supported and current. Source proof was produced only after the claim succeeded.

PC OFF, saves/config/reference/peer files untouched. Parked menu budget remains consumed/unapproved. Full L1+L2 goal remains NOT_MET; bounded source acceptance is not database completion.
