[Home](../../README.md) / Sound and music

# Sound and music

Sound effects, music and voice playback.

Jump to: [Music](#music) · [Sound effects and voices](#sound-effects-and-voices) · [The sound engine](#the-sound-engine)

## Music

Which music plays, how it changes and how the driver runs it.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Interactive music](interactive-music.md) | Explanation | The driver's music object: sections, modes, layers and timing. |
| [Music](music.md) | Explanation | Which track plays in an area, crossfades and the saved override. |
| [Music table](music-table.md) | Format | The file naming each area's track, story changes and boss-music flags. |

## Sound effects and voices

How individual sounds and voice lines are requested, varied and placed in space.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Animation sounds](animation-sounds.md) | Explanation | Footsteps, swings and voices authored into animations. |
| [Sound effects](sound-effects.md) | Explanation | How a request becomes a playing voice, with volume, pan and fades. |
| [Sound variations](sound-variations.md) | Explanation | The random, ordered, cycling and switched sound kinds, and arming a sound. |
| [Spatial sound](spatial-sound.md) | Explanation | The listener, source shapes and how distance sets volume and direction. |
| [Voices](voices.md) | Explanation | Cutscene voice packs, the language choice and the verbs that play a line. |
| [Map sounds](map-sounds.md) | Format | The per-map sound list, its emitters and the weather ambience. |

## The sound engine

The driver underneath: its banks, objects, effects, streams and start-up configuration.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Audio effects](audio-effects.md) | Explanation | The filters, reverbs and other effects the driver can run. |
| [Audio manager](audio-manager.md) | Explanation | The bank controllers and how a game request reaches a bank. |
| [Sound driver objects](sound-driver-objects.md) | Explanation | The handles, pools and calls for banks, sounds and music. |
| [Sound engine](sound-engine.md) | Explanation | The driver's class families and what a voice does each tick. |
| [Sound streaming](sound-streaming.md) | Explanation | Streaming banks, their ring buffers and how a voice reads a stream. |
| [Sound banks](sound-banks.md) | Format | The files holding sounds and music, and how a sound id finds one. |
| [Sound engine configuration](sound-engine-config.md) | Format | The start-up file setting sound categories, the master bus and effect presets. |
