# Consumer check: GI-19 answered - the sway section's layout and the oscillator chain's objects (OPUS, 2026-10-01)

A read-only reader pass, byte-checked by OPUS (control `gi19_check.py`, 26 instructions). The oscillator record is
controller 0's authored sub-block of `@FCP` section 2, relocated by `0040EEA0`. The chain's three intermediate objects
are:
- the rig's own slot `+0x78`, set by `003E1C50`, which holds the encoded bone array from `00421D20`;
- the authored A array (`0x40`-byte records);
- the authored B array (`0x50`-byte link records with a u16 bone index).

- **Corrects:**
  - the oscillator page: the "second 4×4 at `[sub-obj + 0x150]`" is the bone row's `+0x150`–`+0x180`;
  - the oscillator page: the record and entry `+0x08` rows are qualified (not authored, and the A array);
  - the oscillator page's GI-19 note is answered, and its status line is re-statused DOCUMENTED (documented_rule READY);
  - CONTRACT-transform-primitives.md: the same `[sub-obj + 0x150]` wording;
  - register row GI-19: ANSWERED.
- **Affected:** 17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md, 00-Engine-Core-Runtime/CONTRACT-transform-primitives.md, _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the oscillator page's record / entry tables, §4 apply paragraph, GI-19 note, status line, new GI-19 section | revised-here |
  | CONTRACT-transform-primitives.md item 5 (the second 4×4's source) | revised-here |
  | OPEN-QUESTIONS row GI-19 | revised-here |
  | PROGRAM-STATE.md item-5 note (rows 5-8 written by `0040DBB0`; no source offset named) | agrees |
  | the-rig-of-seventeen-controllers.md §2 (controller 0 = sway; slots initialised by `003E1C50`) | agrees |
  | add-motion-skeleton-and-high-model-tables.md (the resource entry's `+0x84` bone table) | agrees |
  | GI-19 answer, for an independent check | routed-to-SWE2-AUDIT-SEM (review request filed with the publish) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-gi19-sway-layout-1001/gi19_check.py, verified at 5d0553380: 26 instructions decode as cited, FAILS 0 ([`gi19_check.out`](gi19_check.out)). `gi19_apply.py --register` re-runs as ALREADY, FAILS 0.
