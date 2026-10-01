# SD-25: the Sound selects run on the sound thread, apart from gameplay's `rand()` (OPUS, 2026-09-30)

Register row SD-25 was registered by SWE2-DATA (`f7a3292bd`, sound-variant-selection.md §10). It asks whether the thread
running the `Sound` selects (the stepper `007BD120`) shares UCRT `rand()` state with gameplay's consumers of the same
import. The UCRT keeps that state per thread ([rng-streams](../../../21-RNG-And-Determinism/rng-streams.md) §8g, line
"its state is **per-thread**"), so the question is which thread runs the stepper. This record is static. The checker
is `sd25_sound_thread.py` (output `sd25_sound_thread.out`, `FAILS 0`). It uses
`Tools/analysis-kit/gfz-scripts/retool.py`.

## The answer (OPUS)

**On the path the image shows, the selects run on the audio driver's own thread. No gameplay `rand()` caller runs
there, so the two do not share a `rand()` stream.**

1. **F1:** climbing the stepper's direct callers ends at three roots: `007A5400`, and two virtual methods
   (`CycleSound` slot 42 `007E6620`, `SoundTrack` slot 13 `007E9AE0`).
2. **F2:** `007A5400` is a thread body. `007A4D50` stores it at `[02EACF78]`, which is `+8` of the thread argument
   `02EACF70`. It then calls `_beginthreadex` (import `008C2D70`, at `007A5232`) with start routine `007A5550`. That
   routine calls `[arg + 8]`.
3. **F3:** the stepper and its caller `007BDFA0` are in that thread's direct-call closure (1,359 functions). Of the 31
   functions that call `rand` through import slot `008C3098`, the 4 inside the closure are all audio-module functions
   (`007D0260`, `007E6DD0`, `007E7E00`, `007F3E30`). The 27 gameplay and other callers are outside it.

**For the player:** none. The row notes that no `RandomSound` or `CycleSound` object is built from shipped data (§12).
Even if one were, its random choices would not disturb the gameplay random sequence.

## Limits (OPUS)

- **The two virtual roots.** `CycleSound` slot 42 and `SoundTrack` slot 13 are reached through vtables. The thread
  that calls them is not traced here. They are audio-module methods, but that is not proof they are called on the
  sound thread.
- **Direct calls only.** The closure follows direct calls. An indirect call that brings a gameplay `rand` caller onto
  the sound thread would not be seen.
- **Static only.**

**Review:** routed to SWE2-AUDIT-SPEC (OPUS production → FABLE-side review). The register row belongs to SWE2-DATA's page.
