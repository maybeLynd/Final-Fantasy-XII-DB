# Audio

**Engine category.** SQEX sound runtime, ambient pools, streaming, and resource request callbacks.

| | |
|---|---|
| Classification source | PrimaryOwner: Audio |
| Functions | 2,064 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

## Systems in this category


- [`Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md`](Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md) —
  **DOCUMENTED, tier 1.** Twelve classes in **two unrelated vtable layouts**, with object
  sizes stated by their own sized deleting destructors. **`Seb` and `Sep` are one bank
  format (`.sab`) with two id widths**, not two kinds of audio.
- [`how-an-animation-makes-a-sound.md`](how-an-animation-makes-a-sound.md) —
  **DOCUMENTED, tier 1.** Footsteps, swings and voices are authored into the animation: two commands, the
  character's sound emitter, twelve types, a picker that rolls the presentation PRNG (footsteps excepted; corrected 2026-09-29, CON-190),
  the bone each type is heard from, and the actor's sound set with its ground term.
- [`the-music-control-file-and-the-bgm-stream.md`](the-music-control-file-and-the-bgm-stream.md) —
  **DOCUMENTED, tier 1.** The field → track table is `in/common/musicctrl.bin` (kind 9 index 32),
  loaded whole at boot and rebased in place; 291 runs, 48 with a story-progress ladder. The
  `0x38`-byte descriptor beside it is the **script BGM stream** (verbs `0448`–`044F`) — dormant in
  the shipped build (no kind-`0x24` paths, sizes or script callers) and the only thing that makes
  the request queue chunk.
- [`the-voice-pack-slots-and-the-voice-verbs.md`](the-voice-pack-slots-and-the-voice-verbs.md) —
  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(per the page's status line; corrected 2026-10-01, OPUS)*. The 64 voice slots behind `voiceread` / `voiceplay` / `voicestop`: each loads
  an event's or map's `.vpc` (language) and `.vpcjp` (`in`) pack for a manager, one config bit picks
  which plays, cues are `sabf` banks handed to the stream controller and started by the request
  pump's post-pass helper.
~~_None yet._ **This is the second-largest owner category in the engine and is entirely undocumented.**~~ *(Superseded: the systems listed above are documented; struck 2026-10-01, OPUS.)* Codec paths (Vorbis/Tremor) belong in [`../23-Third-Party-Libraries/`](../23-Third-Party-Libraries/); the FFXII-side sound runtime belongs here.

## How to add a system here

1. Copy [`../_templates/SYSTEM.md`](../_templates/SYSTEM.md) into a descriptively-named
   subfolder (or as a `.md` file if it is a single mechanism).
2. Fill all eight sections. A missing section means `STUB` or `PARTIAL`, never `DOCUMENTED`.
3. Mirror every "What is not known" entry into
   [`../_index/OPEN-QUESTIONS.md`](../_index/OPEN-QUESTIONS.md).
4. Register any cross-subsystem chain in
   [`../_index/CALL-CHAINS.md`](../_index/CALL-CHAINS.md).
5. Obey [`../_index/EVIDENCE-STANDARD.md`](../_index/EVIDENCE-STANDARD.md).
   No banned evidence class, ever.
