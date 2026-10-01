# SD register rows brought current with answers already committed (FABLE, Claude Opus 5.5, 2026-09-30)

`lagscan.py` found 39 live register rows whose ids were answered or narrowed in commits the same day. This package
incorporates the 36 SD rows among them, which belong to SWE2-DATA's register section; OPUS's records name that
section's owner as the row's editor. SWE2-DATA is operated by FABLE. RC-4 and RC-5 are SWE2-CONTRACT's section and
are left to it (board note). OV-16 is a false positive: its residue is live by design.

For every row:
- **Record re-checked.** The cited record is tracked at HEAD, and its script was re-run from its own directory:
  every one prints FAILS 0. `sd5_display_requests.py` and `sd160_census.py` print no FAILS line and exit 0.
- **Answer wording.** The one-line answer is the author's own commit subject. The row cites the commit and the
  record, and keeps the prior OPEN text as "*Was:*".
- **Answered rows.** The row leads ANSWERED, and each unticked page box that names the id is ticked, with a
  dated note linking the record.
- **Narrowed rows.** The existing lead is kept and a dated narrowing is inserted. Boxes are untouched.
- **Review.** Review stays as the record routes it (mostly SWE2-AUDIT-SPEC). This package awards none.

| id | verdict | commit | record | re-run | answer (author's subject) |
|---|---|---|---|---|---|
| SD-1 | answered | `473de1075` | [sd1-force-fight-enemy-consumers-0930](../sd1-force-fight-enemy-consumers-0930/README.md) | sd1_consumers.py:0 | which force-fight consumers act on enemy units |
| SD-2 | answered | `7573a1b87` | [sd2-r2-label-element-0930](../sd2-r2-label-element-0930/README.md) | sd2_check.py:0 | the R2 label widget draws FLEEING, letter by letter |
| SD-3 | narrowed | `1113232aa` | [sd3-policy-bit21-0930](../sd3-policy-bit21-0930/README.md) | sd3_bit21.py:0 | what capability-policy bit 21 changes in audio and input |
| SD-4 | answered | `35db7fbb2` | [sd4-unit-flag-bit24-0930](../sd4-unit-flag-bit24-0930/README.md) | sd4_bit24.py:0 | unit flag bit 24 marks a transition in progress |
| SD-5 | answered | `ce2b4380d` | [sd5-display-requests-0930](../sd5-display-requests-0930/README.md) | sd5_display_requests.py:rc0 | only a failed resize leaves a display request set |
| SD-20 | answered | `fd421c927` | [sd20-voice-callback-0930](../sd20-voice-callback-0930/README.md) | sd20_voice_callback.py:0 | three voice classes pass their own source-voice callback |
| SD-21 | answered | `819bda0de` | [sd21-mix-path-remainder-0930](../sd21-mix-path-remainder-0930/README.md) | sd21_mix_remainder.py:0 | the mix path's slots, pool, factory paths, callers and SIMD kernels |
| SD-22 | answered | `500458a73` | [sd22-options-volume-rows-0930](../sd22-options-volume-rows-0930/README.md) | sd22_volume_rows.py:0 | the volume commands are options rows 0x13-0x15 |
| SD-23 | narrowed | `acb04148d` | [sd23-sound-slots-38-39-0930](../sd23-sound-slots-38-39-0930/README.md) | sd23_sound_slots.py:0 | what Sound slots 38 and 39 answer and what callers do with it |
| SD-25 | answered | `d7d7e52c9` | [sd25-sound-thread-rand-0930](../sd25-sound-thread-rand-0930/README.md) | sd25_sound_thread.py:0 | the Sound selects run on the audio thread, apart from gameplay rand() |
| SD-62 | narrowed | `e2777d3c8` | [sd62-static-array-elements-0930](../sd62-static-array-elements-0930/README.md) | sd62_elements.py:0 | the two non-type static elements are registry objects |
| SD-80 | answered | `6836e8067` | [sd80-82-ordered-containers-0930](../sd80-82-ordered-containers-0930/README.md) | sd80_82_trees.py:0 | the fourteen MSVC tree bodies read; no single-direction EASTL rotation anywhere |
| SD-81 | answered | `08f4c0821` | [sd81-eastl-callers-0930](../sd81-eastl-callers-0930/README.md) | sd81_callers.py:0 | the 99 EASTL rbtree callers typed: 24 unique-key map/set instantiations, tree owners, wrappers |
| SD-82 | answered | `6836e8067` | [sd80-82-ordered-containers-0930](../sd80-82-ordered-containers-0930/README.md) | sd80_82_trees.py:0 | the fourteen MSVC tree bodies read; no single-direction EASTL rotation anywhere |
| SD-100 | answered | `da3426b96` | [sd100-reveal-modes-0930](../sd100-reveal-modes-0930/README.md) | sd100_modes.py:0 | the reveal stepper's eight modes and who sets each |
| SD-101 | answered | `b545fdb02` | [sd101-pass1-widgets-0930](../sd101-pass1-widgets-0930/README.md) | sd101_pass1.py:0 | flag bit 24 is a per-subtree second-pass switch set by six screens |
| SD-102 | answered | `d1f7f06ac` | [sd102-glyph-emitter-commands-0930](../sd102-glyph-emitter-commands-0930/README.md) | sd102_emitters.py:0 | the glyph emitters build PS2 VIF/GIF packets and mirror the state into the draw context |
| SD-103 | answered | `c2b5b9927` | [sd103-104-context-rows-0930](../sd103-104-context-rows-0930/README.md) | sd103_slots.py:0 | the context's three pointer slots are rows 174-176's allocations |
| SD-104 | answered | `c2b5b9927` | [sd103-104-context-rows-0930](../sd103-104-context-rows-0930/README.md) | sd103_slots.py:0 | the context's three pointer slots are rows 174-176's allocations |
| SD-105 | answered | `f2f55938a` | [sd105-reveal-inputs-0930](../sd105-reveal-inputs-0930/README.md) | sd105_inputs.py:0 | the text reveal's three inputs come from the lag bound and the nested run |
| SD-106 | answered | `349fc1359` | [sd106-measure-sites-0930](../sd106-measure-sites-0930/README.md) | sd106_sites.py:0 | the five 002B3280 sites measure a message line and the confirm dialog's caption and choices |
| SD-107 | narrowed | `0b1f3a2fb` | [sd107-kind1-writers-0930](../sd107-kind1-writers-0930/README.md) | sd107_kind1.py:0 | the only store of 1 at +0xA3 is a sound object's; no traced text element gets kind 1 |
| SD-121 | answered | `06230b6a0` | [sd121-effect-actor-slots-0930](../sd121-effect-actor-slots-0930/README.md) | sd121_slots.py:0 | the three dword arrays are the script-assigned effect-actor slots |
| SD-123 | answered | `524d5aacd` | [sd123-kind52-image-record-0930](../sd123-kind52-image-record-0930/README.md) | sd123_kind52.py:0 | effect record kind 0x52 is the effect container's paletted image (texture) record |
| SD-126 | answered | `c3570bf4b` | [sd126-hud-proc-arms-0930](../sd126-hud-proc-arms-0930/README.md) | sd126_arms.py:0 | the four battle-HUD widget procedures' message arms decoded |
| SD-127 | answered | `23a99db40` | [sd127-hud-key-base-reads-0930](../sd127-hud-key-base-reads-0930/README.md) | sd127_keys.py:0 | no battle-HUD layout key is read through a base pointer; the console is the only pointer route |
| SD-141 | answered | `940b5ffcf` | [sd141-flying-fade-readers-0930](../sd141-flying-fade-readers-0930/README.md) | sd141_readers.py:0 | nothing reads the flying-fade pair; it is stored and never used |
| SD-160 | answered | `af6684173` | [sd160-free-target-type3-0930](../sd160-free-target-type3-0930/README.md) | sd160_census.py:rc0,sd160_check.py:0 | the scripts that give units free-target type 3 (the bestiary tally skip) |
| SD-161 | narrowed | `b7689491e` | [sd161-counter11-writers-0930](../sd161-counter11-writers-0930/README.md) | sd161_check.py:0 | a new game zeroes achievement counter 11, and no census writer stores a negative |
| SD-163 | answered | `e5e8d6013` | [sd163-steamcontroller-poll-0930](../sd163-steamcontroller-poll-0930/README.md) | sd163_poll.py:0 | SteamController_PollState reads 16 buttons and two sticks and drives the rumble |
| SD-164 | answered | `1f1defd7d` | [sd164-167-arena-allocator-0930](../sd164-167-arena-allocator-0930/README.md) | sd164_arena.py:0 | the arena allocator's callback, arena 7 and the handle callers |
| SD-165 | answered | `e87a83339` | [sd165-alloc-null-tests-0930](../sd165-alloc-null-tests-0930/README.md) | sd165_nulltests.py:0 | a census of the arena allocator's 206 call sites by whether they test for null |
| SD-166 | narrowed | `1f1defd7d` | [sd164-167-arena-allocator-0930](../sd164-167-arena-allocator-0930/README.md) | sd164_arena.py:0 | the arena allocator's callback, arena 7 and the handle callers |
| SD-167 | answered | `1f1defd7d` | [sd164-167-arena-allocator-0930](../sd164-167-arena-allocator-0930/README.md) | sd164_arena.py:0 | the arena allocator's callback, arena 7 and the handle callers |
| SD-168 | answered | `d9806dfff` | [sd168-arena-tail-bytes-0930](../sd168-arena-tail-bytes-0930/README.md) | sd168_tail.py:0 | the extra count bytes are allocation slack the arena never addresses |
| SD-169 | answered | `569685cbb` | [sd169-draw-surface-cells-0930](../sd169-draw-surface-cells-0930/README.md) | sd169_cells.py:0 | +0x9C is the VRAM-copy width (BITBLTBUF / TRXREG); +0xA0 reaches no register |

## Consumers

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

- consumer: `_index/OPEN-QUESTIONS.md` SD rows listed above: revised-here.
- consumer: the 12 owning pages whose boxes name an answered id: revised-here (box ticked with a dated note).
- consumer: SD-62's page (`how-a-class-registers-its-array-members-and-annotations.md`): agrees. SD-62 is only
  narrowed, so its box stays unticked; the page carries another lane's uncommitted edits and is not touched.
- consumer: RC-4 / RC-5 (SWE2-CONTRACT's section): routed-to-board-note.
