# SD-20: which class is a `CoreSourceVoice`'s callback object (OPUS, 2026-09-30)

Register row SD-20 was registered by SWE2-DATA (`f7a3292bd`, sqex-sd-sound-driver-architecture.md §2b/§2c). It asks
which class the callback object at a `CoreSourceVoice`'s `+0x88` is in practice. The row's next step was: "read what
each caller [of the factory `007AEA20`] passes as the callback argument". This record is static. The checker is
`sd20_voice_callback.py` (output `sd20_voice_callback.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py`, including its reader for MSVC run-time type information (the vtable's
complete object locator).

## The answer (OPUS)

**Three classes, one per factory caller. Each passes its own `ICoreSourceVoiceCallback` sub-object.**

| factory caller (F4) | argument 5 (`[rsp + 0x20]`) | class (F3) | where that class keeps the interface (F2) |
|---|---|---|---|
| `007B9050` | `this + 0x10` (`007B91B8`) | `SQEX::Sd::Driver::ExternalSourceVoice` | `+0x10`: its constructor `007B8E50` stores the interface vtable there |
| `007DCE20` | `this + 8` (`007DCF69`) | `SQEX::Sd::Driver::CRI::HCAMixerVoice` | `+8`: constructor `007DC730` |
| `007EBAD0` (`Voice::Initialize`) | `this + 8` (`lea rdi, [rbx + 8]`, `007ED2EE`; null when `this` is null) | `SQEX::Sd::Driver::Voice` | `+8`: constructor `007EA050` |

- **F1:** the interface vtable `01CB5218` is `SQEX::Sd::Driver::Core::ICoreSourceVoiceCallback` by its own RTTI.
- **F2:** it is installed only by those three constructors and by the interface's own `007B8F70`.
- **F3:** each constructor's primary vtable names its class by RTTI (`01CB5238`, `01CB7B20`, `01CB92A8`).
- **F5 — how each caller is tied to its class.** This is by layout, which is a consistency test and not a proof of
  type:
  - `007B9050` reads `this + 0x500` beside the `+0x508` block `ExternalSourceVoice`'s constructor builds;
  - every field `007DCE20` touches on `this` before the call (`+0x8`, `+0x38`, `+0x48`, `+0x50`, `+0x90`, `+0xA4`) is
    one `HCAMixerVoice`'s constructor sets;
  - `007EBAD0` shares `Voice`'s fields (`+0x138`–`+0x158`, `+0x190`–`+0x1B0`, `+0x448`/`+0x450`).

So a voice's buffers, sends and markers are filled by whichever of the three owns it. External audio uses
`ExternalSourceVoice`, the CRI HCA mixer path uses `HCAMixerVoice`, and ordinary sound voices use `Voice`. The row's
single-class premise ("`ExternalSourceVoice` ... that it is the object the factory's callers pass is not shown") is
one case of three.

## Limits (OPUS)

- **Tying each caller to its class.** The callers are reached from `007A4930`, `007DCD70` and `007B5D20`, none of them
  vtable slots. The class of each caller's `this` rests on the field-layout match (F5), not on a traced construction.
- **Static only.** Which of the three kinds a given sound uses at run time is not measured.

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
