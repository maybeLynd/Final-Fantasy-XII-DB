# Navigation builder provisional-count boundary

Question: do positive finite extents alone ensure nonzero provisional counts before the builder divides by them? Competing explanations are (1) positivity is sufficient, or (2) truncation can still produce a zero count for a thin rectangle. This matters to the navigation constructor's input domain and malformed-state modeling, not to proving a live scene safe or unsafe.

Method B executes verified original 123 bytes at `0039258C..00392606`, immediately after the `sqrtf` call and before the `floorf` call. Shipping executable SHA-256 is `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`; retained parent builder is 607 bytes at `003924B0`, SHA-256 `0a7ec1000ef3d48a471ff9200675b11ef90717fedcb53b50afa84a4281e236f5`. Matching parent manifest/body/reference was checked before capture. No calls, branches or stubs occur inside the executed window.

The supplied XMM0 return boundary is a **host prediction**, `f32(sqrt(f32(f32(w*h)/f32(275))))`, not an executed original/native `sqrtf` result. Width/height/minima/maxima, stack padding and MXCSR `1F80` were injected and read back. DLL identities were captured before execution and checked unchanged afterward. Instruction/read/write traces, committed store bytes and register snapshots are retained in `raw.json`; `check.py` validates these without rerunning the experiment.

| Case | Supplied c0 bits | First count | Second count | Width/count bits | Argument at the unexecuted floorf call |
|---|---|---:|---:|---|---|
| Original 16×16 positive control | `3F76FF83` | 16 | 16 | `3F800000` | `3F800000` (1) |
| Original 1×400 thin discriminator | `3F9A5FB2` | 0 | 331 | `7F800000` | `7F800000` (+infinity) |
| Labelled first-conversion CVTT→CVT intervention | `3F9A5FB2` | 1 | 331 | `3F800000` | `3F9AAECB` (finite) |

Each case stops at `00392607`, before executing `floorf`, with the original stack restored/unchanged by this slice. Six original global stores are observed per case, including the supplied padding bytes. A budget of 128 instructions per case bounds execution; a failed control would stop subsequent cases. The changed conversion case uses private nonshipping bytes and the same read-back initial state as the thin original case. It proves this detector distinguishes the relevant count conversion; it is not evidence about original behavior under that modification.

Established: **within the supplied post-sqrt boundary and masked emulator environment**, a positive width of 1 and height of 400 produce a zero provisional width count, then +infinity as the refinement/floor-call argument. Positive finite extents alone are an insufficient precondition for claiming a finite refinement in this original arithmetic slice. The conversion is truncating, not nearest-integer rounding or a lower bound of one. A constructor specification needs the provisional conversion/division domain stated explicitly, or evidence of a stronger upstream invariant.

Source representation calculation: getter fields can encode this rectangle with bytes `01 14 01 14 00 00 00 00` (u8 cell width 1, height 20, columns 1, rows 20; signed16 origins 0). This is **not** a captured authored record, executed getter, normal caller or occurrence claim. It does not prove any scene actually uses it.

Unresolved: native/imported `sqrtf` return identity and bits, native `floorf` behavior, full constructor outcomes/final cell sizes/dimensions/allocation, original scheduling/resource state, exceptions/faults and normal reachability. The emulator's recorded MXCSR readback is retained; its exception/status behavior is not certified as native CPU parity. The test does not establish array lifetime, all malformed-input safety or a live game failure. Prior retained 50×50→13×13 calculations, upper-edge query controls and conversion-domain evidence retain their separate scopes.

Consumer requests: OPUS should qualify the corridor/nav-builder constructor domain and any producer arithmetic obligations; FABLE should preserve the conditional semantic boundary rather than promote a hypothetical authored shape to a real scene. Independent review must accept, narrow or reject the original slice/control and upstream-invariant implication. Own producer checks and exact-byte publication are not independent acceptance.

Cleanup: disposable emulators only; no game process, PC controls, saves/configuration/reference binary or peer consumers were changed. S19 menu setup remains parked at its spent allowance. Full L1+L2 completion and final reviews/audit remain pending.

Learned retry rule: this question is settled at the injected boundary. Do not repeat these three cases; the next discriminator, if needed by the owner, concerns an actual upstream invariant or native library boundary, with a separately prepared claim. Do not execute the rest of the constructor merely to expand the result.
