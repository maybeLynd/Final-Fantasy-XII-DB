# Consumer check: 18-Audio contradictions from the reconstruction-readiness map, settled on the pages (OPUS, 2026-10-01)

The cloud readiness map for 18-Audio was produced by stream R (`session_014xapq8GYgyFvvwy2xRFAwk`). OPUS verified it
and filed it in maybeLynd/Final-Fantasy-XII-RE `docs/readiness/18-audio.md` (3b5fe44). It listed 36 places where
18-Audio pages contradict each other or themselves. The map is a pointer, not evidence. Each item was verified before
any edit:
- OPUS checked items 1, 3 and 6 in the image;
- two read-only verification passes checked the rest against the image or the pages' own dated corrections, reporting
  the exact stale text per item;
- OPUS then re-read the surprising ones itself: `002130E0` is the `DynGeoFontTextInstance` constructor, Ambient's
  slot 7 is inherited, `0x40` feeds the pan setter, and `007CF830` tests the weight byte.

FABLE is inactive. OPUS edits these pages under the user's 2026-10-01 authority and its DD claim
`OPUS-DD-UNCLAIMED-15-99-0930`; FABLE gets a notice.

- **Corrects:**
  - Item 1: a NON-ZERO from `003603C0` refuses.
  - Item 2: `003A13F0` is the boot bank setup; it writes −1 to A twice and to C, and never writes B.
  - Item 3: `002DF010` passes `0x40` and `0x7F`.
  - Item 4: `+3` is the slot index, returned by `00361630`.
  - Item 5: `003A0E20`'s argument order.
  - Item 6: the divisor is 1,000.
  - Item 7: the gate is raised in state 10.
  - Item 8: `+0x20` is the embedded bank pool, not a second base.
  - Item 9: the vtable load is inside the loop.
  - Item 10: the mask has six bits.
  - Item 11: the base constructor is `00212710`.
  - Item 12: the lazy object is at `+0x20`; `00221780` is the `AudioBank` base constructor.
  - Item 13: BR-8's withdrawn sentences are struck.
  - Item 14: the bank family has its own contract.
  - Item 15: the spatial page's superseded rows; Ambient's own bodies are 0, 34 and 35; five polygon modes; `+0xE0` is
    audibility.
  - Item 19: SEAD handle calls; the backend is WASAPI.
  - Item 20: `0x40` is the pan and `0x7F` the volume, and FZ-15's "not named" is stale.
  - Item 21: the largest span is 22.
  - Item 23: the `022CBA50` typo.
  - Item 24: 10 mutants.
  - Item 25: the producer is answered, the lifetime is not.
  - Item 26: `dt` cannot be negative.
  - Item 27: curve 0 is linear.
  - Item 28: the ramp records start at `+0x248`, G-14 names the parameters, and `007E7300` is read.
  - Item 29: `007CF830` tests the weight byte.
  - Item 30: there is no uniform second pass.
  - Item 31: the presentation PRNG.
  - Item 32: the voice-slot states.
  - Item 34: `00210C50` is read.
  - Item 35: isolated execution exists.
  - Item 36: stale PARTIAL banners and answered open items, and CoreSourceVoice has 17 slots.
- **Affected:** 18-Audio/Audio-Bank-And-Controller-Family/CONTRACT-audio-bank-and-controller-family.md, 18-Audio/Audio-Bank-And-Controller-Family/audio-bank-and-controller-family.md, 18-Audio/Audio-Boundary/CONTRACT-sound-request.md, 18-Audio/Audio-Boundary/how-a-sound-fades-the-ramp-and-its-six-curves.md, 18-Audio/Audio-Boundary/how-a-sound-request-becomes-a-voice.md, 18-Audio/Audio-Boundary/what-the-engine-calls-to-make-a-sound.md, 18-Audio/CONTRACT-field-music-selection.md, 18-Audio/CONTRACT-music-control-file-and-bgm-stream.md, 18-Audio/CONTRACT-spatial-source-objects.md, 18-Audio/README.md, 18-Audio/Sound-Bank-And-Voice-Formats/README.md, 18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md, 18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md, 18-Audio/Sound-Selection/sound-trigger.md, 18-Audio/Sound-Selection/sound-variant-selection.md, 18-Audio/how-an-animation-makes-a-sound.md, 18-Audio/how-the-music-changes-when-you-change-area.md, 18-Audio/sqex-sd-sound-driver-architecture.md, 18-Audio/the-music-control-file-and-the-bgm-stream.md, 18-Audio/the-spatial-audio-object-model.md, 18-Audio/the-voice-pack-slots-and-the-voice-verbs.md, 18-Audio/which-variation-of-a-sound-you-hear.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 77 edited passages on the 22 pages | revised-here |
  | the pages' own later dated corrections and sections (C-SR §14/§15, BK BD-4, C-BK AC-4, LAY CO-4/CO-8, C-SP SA-3, SAB §3, the map-sound-list page, FADE §4/§6, VAR §12, ANIM CON-190, VPK GA-4, TRG G-14, MCF §2.3/§3.3, C-MC MC-1/MC-8, C-FM §13a/§14.1) | agrees (the struck lines now point at them) |
  | register rows `FZ-15`, `SD-22`, `SR-7`, `UQ-243`, `UQ-244`, `UQ-267`, `G-14`, `DG-1`, `MC-1` | agrees |
  | `sead-function-identification.md` (items 16-18) | routed-to-a later pass (the page is held by SWE2-EC7's open publish task; not edited here) |
  | item 33's "350 distinct values" against 268 `se` folders plus the shout banks | routed-to-a later re-count over the VBF (left as written) |
  | item 22 (the music-block gate bits) | agrees (two different gates; not a defect) |
  | the RE repo readiness map `docs/readiness/18-audio.md` | routed-to-OPUS's next repo sync |

- **Applier:** [`apply_audio_fixes.py`](apply_audio_fixes.py) runs the image check first. It has 77 tagged,
  single-occurrence edits. The saved re-run [`apply_audio_fixes.out`](apply_audio_fixes.out) reads ALREADY throughout,
  FAILS 0.
- **Regression:** Database/FFXII TZA/_index/candidates/opus-audio-readiness-fixes-1001/audio_fixes_check.py, verified at 4ce70df03: 56 instructions (3 of them with their rip targets), the Ambient/SoundSourceObject vtable comparison and the CoreSourceVoice slot count, FAILS 0 ([`audio_fixes_check.out`](audio_fixes_check.out)).
