# Consumer check: GI-15 answered - the authored-commands page's per-site helpers read, five pages corrected (OPUS, 2026-10-01)

A read-only reader pass under OPUS-GI15-GI18-READS-1001 (the GI-15 half), with every correction checked at the bytes by
OPUS (control `gi15_check.py`). The page is re-statused DOCUMENTED once the register row is ANSWERED
(`gi15_register.py`).

- **Corrects:**
  - the authored-commands page:
    - `0x34` arm `0x01` uses the float in every case;
    - `0x3F` fills the bone from `word+2` and the preset from `word+0x10`, the reverse of the page's table;
    - `0x48`'s `0xFFFF` zeroes the preset, not the index;
    - "one by index, the other by name" is restated;
    - `+0x2F2 = 1` is the whole-skeleton bind (attach code `0x7FFF`), not a placeholder;
    - `003E5D30` runs on the no-key path itself, so "leaving that state restores three fades" is struck;
    - `0x2A`'s floats are the camera-shake source's intensity, time rate and radius scale;
    - the eleven "not read (GI-15)" passages are struck with pointers to the new section;
  - how-a-character-fades-the-ten-channels.md: `003737C0` takes a record when flags bit 8 is **set**, not clear;
  - ftr-node-table.md: link bits 0-11 are read (`00409250` returns them as the key when flags bit 30 is clear);
  - fcp-character-parameter-block.md: section 5 (`+0x0A`) has a reader, inline in `003E7210`;
  - when-a-group-is-wiped-and-when-it-comes-back.md: the priority map is `01F00410`, not `01E6B410` (two rows);
  - the-per-model-oscillator-subsystem.md: the `0x3F` section's preset and id words were swapped; `+0x3C` is the bone.
- **Affected:** 17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md, 17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md, 17-Presentation-Rendering/Model-And-Motion-Formats/ftr-node-table.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md, 17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md, 05-Spawn-Encounter-Lifecycle/Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md, _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the authored-commands page's `0x34`, `0x3F`/`0x48`, `0x13`/`0x14` (`+0x2F2`), `0x2A`, `0x16`, `0x09` and id-4/6 passages, status line and new GI-15 section | revised-here |
  | the oscillator page's `0x3F` section (preset / bone words, `+0x3C`) | revised-here |
  | the fades page's `003737C0` row | revised-here |
  | the FTR page's link-field bits 0-11 | revised-here |
  | the FCP page's section-word reader inventory, `+0x0A` row | revised-here |
  | the group-wipe page's `00422DE0` and `00423790` rows | revised-here |
  | OPEN-QUESTIONS row GI-15 (status cell only) | revised-here |
  | fef-and-motion-entries.md's `0x3F` row (block `{word+2, word+0x10&0xFFF, bit15, ...}`, which is the corrected order) | agrees |
  | render-event-selection-evidence.md's `0x3F` row (handler size and site only) | agrees |
  | the-element-types-40-42-a0-ab-d0-d1.md `0x42` (the camera-shake pool, slot `+0x30`/`+0x34`/`+0x38`) | agrees (cited) |
  | CONTRACT-authored-command-ramp-channels.md (the ramp tick) | agrees (cited) |
  | the-character-render-record-array.md, fdm-and-for-entries.md, fef-and-motion-entries.md on `+0x2F2` (a gate / filter field; none calls it a placeholder) | agrees |
  | ADDRESS-INDEX.md rows (links only) | agrees |
  | GI-15 answer, for an independent check | routed-to-SWE2-AUDIT-SEM (review request filed with the publish) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-gi15-helpers-1001/gi15_check.py, verified at 22ae17df7: 42 instructions decode as cited and the three rip targets (`01F00410` twice, `02B4D7A2`) resolve, FAILS 0 ([`gi15_check.out`](gi15_check.out)). `gi15_apply.py` and `gi15_register.py` re-run as ALREADY, FAILS 0.
