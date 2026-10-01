# Each normal BMASK entry requests a fresh shared mask

Player view: the nearby-object query clears its shared working mask before collecting the selected cells. Reproducing “zero once when the map is built, then keep adding” would let old candidates accumulate. The original source instead requests a reset at the start of each call. This is a code/contract finding, not a captured game-memory change.

**Method A:** exact certified73461d292B BMASK003912E0 through00391403, corroborated by its PEunwind record ending00391404, plus6B memset thunk00861EC0. Existing47 import descriptor/name evidence is dependency-verified against the original image, not recaptured or inferred from a label. Full source, raw roles from the shared reviewed op_kind/written default invocation, driver/source/tool identities, consumer preimages and normalized result are retained. No original/private/native/emulator/live FF12 instruction execution or loop/query-fixture replay.

Competing explanations: reset only during construction; per-query shared scratch reset; caller-supplied destination. The exact entry bindings distinguish them:

```text
003912F9 MOVSXD R8,DWORD[02AEE0B8] ; signed-widen mask length
00391302 MOV RCX,QWORD[02AEE0B0]   ; shared scratch pointer
00391309 XOR EDX,EDX               ; zero fill
0039130E CALL 00861EC0              ; qualified memset import
```

No early branch/call precedes this clear request on normal entry. All clamps and loops follow it. The sole call in the body is that memset route. The inner OR accumulation reloads its RDX base from **the same global pointer cell** at003913B1, writes a byte through RDX+RAX−1 at003913C4, and the return reloads that pointer cell into RAX at003913E8. Caller ECX/EDX/R8D/R9D supply indices; the clear destination is not an incoming argument. The source does not write the global pointer slot: it calls a clear through its loaded pointer and OR-writes its pointee. A census of RIP-relative global stores alone cannot describe that shared heap-state effect.

Source implication: normal entry requests per-query zeroing, followed by accumulation into shared scratch. Successful clearing requires valid writable storage, appropriate nonnegative length and conforming imported memset behavior. The loaded CRT and actual memory bytes were not observed. Repeated loads from one global **do not** guarantee stable pointer identity across the call or under reentrancy/concurrency; scheduling/exclusive use, lifetime and atomicity remain separate. No claim that all malformed inputs clear safely or that an arbitrary injected midfunction entry runs the reset.

Controls: a private one-byte MOV RCX,[global]→MOV RDX,[global] source change fails the destination binding; five private NOP bytes replacing the clear call fail its call binding. Both fail immutable original-source identity. Original pointer/import/length bindings are positive controls. Changed bytes were data only, never executed; they prove the source detector distinguishes the relevant request, not native clearing effects.

Affected claims are exact: NavGridParams+50 workingCandidateMask's “zeroed once ... rather than per query” interpretation, and corridor contract's BMASK “caller-supplied record mask” wording. Construction's original zeroing remains true; it is not the sole reset request. OPUS owns the type/contract qualification; FABLE consumes query semantics. Do not broadly reject the closure census, prior clamp/upper-edge/authored/thin-grid results or all caller/out-parameter semantics. Required independent SPEC review and consumer agreement stay separate from own source/manifest checks.

Tool limits: original capture recorded Python executable hash and Capstone version; validation-tool-identity.json additionally pins the current readonly validator's Capstone module/native DLL before and after its decode. It is not retroactive proof of an unrecorded historical capture-DLL hash. Exact raw code and role results are independently re-derived against those pinned current inputs.

Cleanup: reference/peer/save/config read only; no process/input/memory/hook/game controls/deployment or native intervention. PC OFF, menu allowance spent/extension unapproved. FullL1+L2NOT_MET. Learned next discriminator: actual initialized pointer stability/concurrency only if a prepared runtime question requires it; do not repeat this clear binding or treat its call as an observed memory effect.
