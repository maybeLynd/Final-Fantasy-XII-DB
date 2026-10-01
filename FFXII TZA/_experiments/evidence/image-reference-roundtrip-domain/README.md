# Compact references: the exact inverse domain

Player view: FF12 stores these references in32bits. Converting a reference to an address and back works at a stable shared base. Converting an arbitrary64-bit address to a reference and back can lose its upper bits. The helpers themselves do not treat zero as a special null marker.

**Method A.** Complete shipping leaves `0020E600` (10bytes) and `0020E620` (9bytes), exact widths/operands/RIP target, and modular integer source proof. The selected Python calculations discriminate the hypotheses; they are not executions of original FF12 instructions. No emulator, native harness, game, PC control, instrumentation or memory writes.

The resolver executes `MOV EAX,ECX` (zero-extend the input's low32bits), `ADD RAX,qword[01F83530]`, then `RET`. The encoder executes `SUB ECX,dword[01F83530]`, `MOV EAX,ECX`, then `RET`. The subtraction is at **0020E620**, not0020E626; the latter is the MOV. Both read the same cell, but at different widths. Neither leaf contains a null test or memory store.

For a fixed64-bit cell value B, let D resolve and E encode:

```
D_B(u) = (B + u32(u)) mod2^64
E_B(p) = (u32(p) - u32(B)) mod2^32
```

Reducing D's result modulo2^32 and subtracting B's low32bits gives **E_B(D_B(u))=u for every unsigned32-bit u**. In the other direction, E keeps only the low32bits of `(p-B) mod2^64`. Therefore **D_B(E_B(p))=p iff `(p-B) mod2^64 < 2^32`**. This is a translated modulo64 window; near the64-bit upper edge it can wrap. It is not arbitrary64-bit inverse or general mapped-address safety. Pointers sharing their low32bits encode identically at fixed B.

| conditional input | calculation |
|---|---|
| B=0x120000, p=B+0x1234 | encode0x1234, decode recovers p |
| p=B+0xFFFFFFFF | upper reference edge still round-trips |
| p=B+0x100000000 | encodes0, decodes B; original p is lost |
| p=0, B=0x120000 | encode0xFFEE0000, decode0x100000000 |
| u=0 at any B | D_B(0)=B; zero reference need not be null |

Additional selected calculations cover a conditional high base and a wrapping window. They are invented control inputs, **not observed game values**. Base changing from0x120000 during resolution to0x120001 during encoding changes reference0x1234 to0x1233. No atomicity/stability guarantee follows from these two separate loads.

A labelled private SUB→ADD source/model control preserves the operand width and RIP target. A zero-base calculation does not distinguish it, but the nonzero-base control does; the original-byte binding rejects it. No mutated machine instruction was executed. This establishes a useful control precondition, not a defect in an unnamed earlier checker.

Reuse the existing owner contract's load-time-zero and computed-writer R6 findings: the cell is BSS zero at image load, with an undriven computed texture-id writer rather than a whole-process no-writer guarantee. **No census or original-code writer replay was repeated.** The retained writer producer's R1 control already names0020E602/0020E620 correctly; the consumer contract's two0020E626 citations are the defect. The shared cell is called ImageRelativeReferenceBase; its equivalence to the PE/module base is not established.

FABLE's shared-neighbours §4c and function table need the inverse-domain qualifier and careful base terminology. OPUS's representation contract should retain the width/stability/null domain and correct only the stale subtraction-site citations. Existing full-QWORD/low-DWORD downstream consumer evidence, image-load finding and undriven-writer limits remain valid. No bulk EC7/caller disposition or new representation system is requested.

`retained/` preserves both leaves, exact reader, catalog rows and contemporaneous consumer/producer preimages; `result.json` has normalized controls, proof and identities. Readonly `check.py` binds the original source and each control. Producer checks, manifest integrity and independent project acceptance are distinct. Owner incorporation and SPEC review remain required.

Unresolved: actual runtime B/p domains, base lifetime or changes, native caller preconditions, null conventions imposed elsewhere, mapped-memory validity, ownership, allocation, resource initialization and normal reachability. No save/config/reference/peer changes. Parked menu allowance remains consumed/unapproved. Full L1+L2 database goal remains NOT_MET.
