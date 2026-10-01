# Affected-consumer check: a failed Yebis initialisation reaches the game (OPUS, 2026-09-26)

**The bound.** `CONTRACT-post-processing-subsystem.md` (FABLE) says in §3 that on a failed `006DAA70`, `006CBD20` *"logs
'Failed to initialize PPFX context.' … and continues"*. §5 I-5 is headed *"Library failures do not reach the game"*.

Both sentences are true as written: the failure is logged and `006CBD20` continues. But the continuation's next library
call, `006CBE27` → `006DB4C0` → `00708110`, dereferences `CPostEffect+0x108`:
- **`00708110` returns early only on `+0x147`**, which `Initialize` sets only under flag `0x800`. The build's constant
  flags `0x20001` do not include it.
- **`+0x108` is written only at `007009BB`**, behind the immediate-context test.

So an `Initialize` failure before `007009BB` faults creation at `00708186`. I-5 holds for `ApplyEffects` (§7's "Let a
library error abort the frame" is about that half), not for every initialisation failure.

The contract text is added to, not struck (§3 and §5 carry a dated *Bounded* note). The invariant's wording is FABLE's,
routed to FABLE.

**Regression:** `_index/candidates/s40-opus-replay-post-process-init/check.py`, ALL PASS (8/8, md5 `5d726159…` over two
runs). It is an executed control, not a word match:
- **P3:** the refused `Initialize` is logged, `006CBD20` continues, and the run faults at `00708186` reading `0x68`.
- **S1:** the stores and the gate, byte-verified.

A reimplementation that treats every initialisation failure as survivable does not match the shipped behaviour.

| consumer | state |
|---|---|
| `17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md` §5 I-5 | revised-here (a dated *Bounded* note: the executed failure, its fault, and the stores behind it) |
| same contract, §3 "on failure logs … and **continues**" | revised-here (a pointer to the bound) |
| same contract, §7 "Let a library error abort the frame. The game ignores it (I-5)" | agrees (it concerns a frame's `ApplyEffects` error, not creation) |
| same contract, §6 boundary, "I-1 to I-5" among what a reimplementation must match | agrees (the bound is part of I-5 now) |
| `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md` lines 1012–1016, "The game initialises the library exactly once, and always with `0x20001`" | agrees (P2 executes it: one pass through every link, `0x20001` stored at `+0x20C`) |
| `17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md` line 1705, `006CBD20` "one-shot feature init" | agrees |
| `23-Third-Party-Libraries/PostEffects-Yebis-PPFX/yebis-ppfx-source-map.md` line 407, inbound callers `006CBD20`, `006CBEA0` | agrees |
| `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md` line 190, the `0xD40` YEBIS state block through `006DA880` | agrees (P2 allocates it at `[02EA0B70]` through `006DA880`) |
| `_index/candidates/s40-types-cposteffect-and-cfg.md` | agrees (it types `CPostEffect` and the parameter block; no failure claim) |
| `_index/OPEN-QUESTIONS.md` UQ-227 (nine optional features never initialised) | agrees (P2: none of `0x40000` / `0x4000000` / `0x8000000` is set in the stored flags) |
