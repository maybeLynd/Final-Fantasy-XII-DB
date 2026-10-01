# Native control exposes a bounded emulator precision-status omission

Question: in the retained circle-cell test, the next-above5 radius squared to41C80003 while Unicorn's observed MXCSR stayed1F80. Does native execution preserve that status too, or does the emulator omit a status effect? **Method B** answered with one verified original instruction, not a new game session or general runtime platform.

Shipping `MULSS XMM2,XMM2`, original `0046912E`, four bytes `F30F59D2`, is bound to the certified image SHA256 `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8` and the committed237B circle-cell parent `9998e98b8ae823f8fc703bccfe23118f1de8b5e9`. Only these four shipping bytes execute. The disclosed private straight-line14-instruction Win64 wrapper sets XMM2 from ECX, saves/sets/restores MXCSR, reads status into a disjoint local output, and returns result bits. It has no call, branch, callback or nonvolatile-register clobber. It runs in the current standalone Python host process, **never in FF12 or another process**. The same wrapper is separately run in Unicorn with a64-instruction limit. This is native isolated original-code execution plus an emulator control; not a live observation or full-function native parity.

| Controlled input / code | Result bits native / guest | Controlled MXCSR native | Guest |
|---|---|---|---|
| Exact5, original MULSS | 41C80000 / 41C80000 | 1F80 | 1F80 |
| Next-above5 (40A00001), original MULSS | 41C80003 / 41C80003 | **1FA0** | **1F80** |
| Private omit-MUL (four NOPs), same input | 40A00001 / 40A00001 | 1F80 | 1F80 |

Thus the observed result bits agree for this original instruction/input, but **the emulator omits native bit5** in the inexact square. Exact/inexact/private omission controls distinguish the effect of MULSS from stale flags, state setup, wrapper or observer behavior. The private code is rejected as shipping identity. Native MXCSR is recorded before injection and after restoration with exact equality in every call. Output cells startA5, three DWORD slots are observed written and the fourth sentinel remainsA5. Native code bytes are checked before/after execution; the private4096B RW→RX allocation is freed and VirtualQuery reports MEM_FREE. Guests complete their full source paths to RET with stack advanced8, expected five stores and restored MXCSR. No instrumentation attaches to a game. Source/raw/native preflight/partial-case record/reducer/interpreter/backend/decoder/ctypes/kernel file identities and cleanup receipts are preserved.

Bit5 is the precision/inexact-result flag; the architecture describes status flags as sticky and distinguishes them from exception mask and rounding-control bits. See [Intel SDM Volume1, 253665-081US, September2023](https://cdrdv2-public.intel.com/789574/253665-sdm-vol-1.pdf), §10.2.3.1 and §11.5.2.6, printed11-16/PDF page282. The search extract of an older manual misstated the bit position; the current primary text at §11.5.2.6 was checked directly. Native empirical values above are our observations, not additional vendor tests.

Affected-claim reconciliation is bounded: the circle-cell capture's unchanged emulator `after.mxcsr` is **not proof of native absence of precision effects**. Its original published README already excluded native exception/status validation; the finite contact-return interpretation does not depend on status parity. The RNG `scaled-random-range-boundary` actual checker masks status bits (`& ~0x3F`) and explicitly excludes native status semantics. The matrix `postmultiply-float-order` actual checker uses initial1F80 for its tested output order and its README excludes native CPU parity; it does not assert native absence of inexact status. Those output/control findings are retained, not broadly retracted or certified. Other captures or consumers that interpret emulator status as native effects must be individually identified and downgraded/rerun with adequate native controls. This package does not certify all prior probes.

Procedure correction: retain MXCSR **control** preconditions separately from captured **status**. The new one-purpose producer/default checker makes exact5, inexact-next-up and omit-MUL controls mandatory and detects result-equal/status-unequal evidence. A unchanged emulator status can never close a native no-exception claim without appropriate detection controls. Use this native control only for the bounded status question; it is not a generic platform or a reason to rerun every accepted fixture. Existing published parents remain immutable; this additive package supplies the correction/qualification and is routed to OPUS, ORACLE and SPEC. Required independent acceptance is separate.

Limits: one scalar square on this host/build and pinned backend, masked round-nearest1F80, exact finite inputs. No actual FF12 MXCSR, full predicate/caller/resource initialization, unmasked exceptions, NaNs, denormals, overflow, all-instruction status behavior or native whole-program parity proved. The wrapper injects state and observes it; it cannot establish omitted game initialization/scheduling. DLL identities are loaded-provider file identities, not a claim to hash all memory-resident modules.

Reproduce **only the retained reduction**, without re-execution, from repo root:

```
Collaboration/Tools/analysis/venv/Scripts/python.exe "Database/FFXII TZA/_experiments/evidence/original-mulss-status-control/check.py"
```

PC control remains off; no FF12 process, save/config/reference or peer edits. Reference bytes were read-only and checked unchanged. S19's spent setup allowance and unapproved extension persist. Full L1+L2 database NOT_MET, L3 later.

Player view: the numeric answer matched, but the emulator missed the CPU's record that rounding occurred. This prevents us from calling an unchanged emulator status “no native floating-point exception.” It does not change the tested cell-contact result.
