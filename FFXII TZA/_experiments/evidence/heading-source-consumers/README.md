# Heading source consumers: one local argument and three candidate node readers

**STATIC_ONLY.** This is a bounded supplement to the immutable
`heading-class-effects-slice` (`c957be221b4210a361400c4188d399f79425ae89`)
and four-tail supplement (`eab9cdf341fe4734e7e61fb33095c2270bf85e06`).
It uses original FF12 shipping bytes and retained published inputs. No original
machine-code execution, live FF12, process injection or additional tail capture
occurred. Certified EXE SHA256 is
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.

The first selected position call at `002E4751` has fifth DWORD argument zero:
`002E4735 xor ebx,ebx` precedes a contiguous no-call/no-RBX-write interval,
`002E474D` stores EBX at caller `[rsp+0x20]`, and the callee frame maps that
slot to its `0026B014 [rsp+0x80]` comparison. `002E4739` can skip the call;
the finding concerns the selected arm under normal entry and valid stack.
It needs no assumption about calls before the local XOR. The later call at
`002E4928` remains conditional on intervening native/library ABI behavior.
The original PE declares the tail thunk `00861F14` through IAT `008C2BB8`
as `api-ms-win-crt-math-l1-1-0.dll!sqrtf`; that is a static import, not a
running module or observed native effect. See `ARG5-PLAN.md` and the raw
driver/result/terminal receipts. The two fault runs are labelled alternative
analysis inputs, not FF12 interventions.

The type-specific source scan has a different consumer question. It found
direct offset reads in the matching `0x6B`, `0x71` and `0x72` step bodies,
with bounded compare/write or compare/call branches. The matching `0x67`
56-byte body contains no direct `+0x3D8` operand; it still calls two routines.
`NODE-READER-RESULT.md` gives exact addresses and limits. The source moves
entry RCX into RBX before the reads and has no explicit RBX rewrite until
afterward; intervening calls make continuity conditional on their ordinary
nonvolatile-register ABI. No initialized node identity, full nested effects,
step scheduling, reuse/lifetime, class stability or player-visible consequence
is established. The `0x67` no-hit is a bounded candidate rejection only.

`check.py` verifies actual successful upstream process receipts and current
original-source invocations, published input/EXE identity, read/store roles,
the three candidate reader shapes, and limits. Missing or failed prerequisite
is not a valid empty result. Producer checks and source integrity are not
independent acceptance. OPUS owns contract/type incorporation and a separate
non-author review must assess the evidence before project acceptance. Keep
the second-call ABI question and actual initialized/runtime questions open.

No game, save, config, reference binary, process-control or instrumentation
state was changed. The menu recovery remains parked with its prior consumed
allowance. The full L1+L2 goal remains active and incomplete.

Player version: one movement call definitely asks for its zero-argument path
when that call is reached. Three of four nearby type updates inspect a field
that the earlier movement-linked code sets. This still does not show that the
player saw an effect or that a whole game rule is settled.
