# Navigation grid allocation-return boundary

Player view: the grid builder's helper skips initialization if its allocator returns no block. The builder itself then stores that return value as the grid base and calls the clearing function without a local null check. Reproduction needs a successful allocation precondition or evidence of a stronger allocator policy. This does not show the game ever runs out of memory or crashes here.

**Method A:** exact certified73461d shipping607B builder003924B0 (unchanged previously retained parent),104B allocation/init wrapper00384580 and6B import thunk00861EC0. PE descriptor/lookup/name bytes bind the latter to the intended `memset` import. Its loaded native implementation is not executed or identified. Full bodies terminate in RET/thunk JMP; source/reader/shared access-policy/driver/tool identities and consumer preimages are retained. This is source analysis with conditional CFG calculations, not a stubbed or executed original/native/emulator/live test.

Question and competing explanations: the caller may guard the returning null; the wrapper may conditionally return null and the caller still clear it; or actual allocator/synchronizer policy may prevent that return. The local code distinguishes the first two. The third needs separate native/source evidence and remains open.

After0036A190 returns,003845B5 saves RAX to nonvolatile RBX; TEST RAX,RAX and JE003845CB skip the initializer0036C660 only when zero. Both local paths call the two unlock functions and finish with MOV RAX,RBX. Conditional on those opaque calls returning conformingly and preserving RBX, zero returns zero; nonzero gets the initializer and returns the same pointer. The native allocator may throw, stop or have a stronger policy; lock/unlock effects, failure reachability and initializer behavior are not supplied by this path calculation.

The builder writes final dimensions before calling that wrapper. Its exact return-to-clear interval is:

```text
0039266F MOVSXD R8,EBX            ; signed-widen original low32 total
00392672 XOR EDX,EDX              ; zero fill
00392674 MOV RCX,RAX              ; wrapper return is destination
00392677 MOV QWORD[02AEE0A0],RAX  ; publish base before clear call
0039267E CALL 00861EC0             ; qualified memset thunk
```

There is no local conditional branch/test/alternate exit in this interval. This is a source-order fact; it is not an atomic publication or observer-timing observation. Under a returning-zero hypothesis, the source reaches the clear call with RCX0 and has stored0 to the base. No imported clear behavior, fault, health failure or actual allocation consequence is inferred. Later interior-pointer carve arithmetic does not prove the clear returns normally; old state retention, ownership release and lifetime remain separate.

The size boundary is also explicit: before the allocation-wrapper call MOV ECX,EBX supplies the low32 total with architectural zero-extension in the argument register; the wrapper forwards those low32 bits to0036A190. Before the clear the builder instead MOVSXD widens EBX to R8. These widths must not be conflated. Downstream allocator interpretation, overflow reachability, full constructor domain and native CRT size behavior are not established. The normal positive finite examples in earlier packages are unchanged.

Controls could reject the preferred answer: a private JE→JNE source change reverses which null path reaches the initializer; a private MOV RCX,RAX→MOV RCX,RBX change fails the destination-from-return detector. Both differ by exactly one byte and fail the immutable original-body binding predicate. The original nonzero path is the positive initializer control. Changed bytes are data only, never executed. `raw-source.json` preserves every body/instruction and memory roles from the **actual default shared reviewed reg_tracking.op_kind/written invocation**. The capture does not bypass policy through raw operand access flags. Readonly check re-derives source/import/role/branch/destination bindings and rejects altered source identity, without repeating an experiment.

Required consumer change: OPUS qualifies NavGridParams allocation/base/carve/constructor preconditions with valid successful storage and the exact width boundary; FABLE qualifies the rebuild row's alloc/init description and caller failure boundary. Do not label the wrapper null-safe as proof its caller handles failure. Keep actual failure policy and native effects open until independently established. Route independent SPEC review; own controls, source identity and consumer agreement are distinct.

Cleanup: only read certified image/peer sources. Retained source/control bytes and files are data; no deployment/execution/process/input/memory/hook/save/config writes. Checker rereads the certified reference; reader/policy unchanged at capture readback. PC OFF. Parked S19 allowance spent/extension unapproved. Full L1+L2 goal NOT_MET. Learned limit: these local guard/order paths are now settled; next discriminator is an actual stronger allocator/caller policy, not rerunning the same source branches or a blind live OOM experiment.
