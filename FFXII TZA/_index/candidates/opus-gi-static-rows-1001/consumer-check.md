# Consumer check: GI-16 / GI-17 / GI-18 answered, GI-14 / GI-19 narrowed, the layout page's `002D45C0` nibble corrected, and three pages re-statused (OPUS, 2026-10-01)

Static reads from the shipping image, under the board tasks OPUS-GI-STATIC-ROWS-1001, OPUS-GI14-ELEMENT-HELPERS-1001 and
OPUS-GI15-GI18-READS-1001 (the GI-18 half; GI-15 follows separately).
The five register rows were opened by SWE2-FRONTIER's re-status of c97af7156 (record `dd-restatus-gi-0930`, on
SWE2-AUDIT-SEM's REJECT).

- **Corrects:**
  - the layout page's `002D45C0` eligibility test: the kind nibble passes when it is **not 0, 1 or 4**, not when it is
    "5-or-negative" (`test eax, 0xFFFFFFFA` / `cmp eax, 5` at `002D4613`-`002D461D`);
  - the license-board page's `+0x37D` move mode: **five** states, not four (`00558607` stores `0x401` at `+0x37C`);
  - the element-types page: the blend value is the GiPrim command's `+0x30`, not a record `+0x38` with an unread
    consumer;
  - the oscillator page: two two-step resolves through `0020E600`, not one four-deep chain;
  - the gambit page's arm roles the GI-18 read refutes (list ids 1, 2, 8, 9, 10; editor ids 8, 9, 16, 17, 18, 19/20, 22,
    26; id-12 sub-ids `0x8000`, `0x8002`, `0x8003`, `0x8004`; the member table's `005679D0` / `005680E0`), each struck
    with a pointer to the new GI-18 section (record and applier: `../opus-gi18-gambit-arms-1001/`);
  - the shop, license-board and gambit pages' body PARTIAL banners: struck with a pointer to the new status lines.
  All three pages read READY under documented_rule.py after the register cells.
- **Affected:** 16-UI/Gambit-Screens/the-gambit-screens.md, 16-UI/Layout-Parameter-System/ui-layout-parameters-and-editor-schema.md, 16-UI/License-Board-View/the-license-board-screen-widgets.md, 16-UI/Shop-Screens/the-shop-screens.md, 17-Presentation-Rendering/Effect-File-Formats/the-element-types-00-0a.md, 17-Presentation-Rendering/Model-And-Motion-Formats/the-per-model-oscillator-subsystem.md, _index/OPEN-QUESTIONS.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the layout page's `002D45C0` bullet; the shop page's GI-17 section uses the same rule | revised-here |
  | the license-board page's move-mode paragraph and its section-7 bullet | revised-here |
  | the element-types page's three GI-14 mentions and its new GI-14 section | revised-here |
  | the oscillator page's chain paragraph and its record table (new `+0x08` row) | revised-here |
  | OPEN-QUESTIONS rows GI-14, GI-16, GI-17, GI-18, GI-19 (status cells only) | revised-here |
  | the shop, license-board and gambit status lines and body banners | revised-here |
  | the gambit page's list / editor / sub-id tables and member table | revised-here |
  | the-widget-message-protocol.md on `00569ED4` (calls `00568FE0(self, msg.b, msg.a)`) | agrees |
  | the-two-transform-primitives.md naming `005679D0` / `005680E0` pane rebuild / pane reset | agrees |
  | ui-layout-parameters-and-editor-schema.md listing `00569236` as a site | agrees |
  | the-two-transform-primitives.md and effect-element-type-dispatch.md on `0039D6C0` (slot builder, `0x28` stride; nothing on the blend value) | agrees |
  | CONTRACT-transform-primitives.md, the-ee-and-vu0-register-bank.md, how-a-character-fades-the-ten-channels.md and PROGRAM-STATE.md on `0040DBB0` (the second 4x4 write, the loop family; nothing on the resolve depth) | agrees |
  | ADDRESS-INDEX.md rows for `0039D6C0`, `0040DBB0`, `00557DF0` (links only) | agrees |
  | _index/progress/crosswalk.md GI-14 / GI-19 rows (generated from the register by progress_report.py) | agrees (regenerates) |
  | auditsem-review-gi-restatus-0930/REVIEW.md and dd-restatus-gi-0930/README.md (dated review records) | agrees (history; not edited) |
  | GI-16, GI-17 and GI-18 answers, for an independent check | routed-to-SWE2-AUDIT-SEM (review request filed with the publish) |

- **Regression:** Database/FFXII TZA/_index/candidates/opus-gi-static-rows-1001/gi_static_check.py, verified at 4ddb2b065: 52 instructions decode as cited, FAILS 0 ([`gi_static_check.out`](gi_static_check.out)). The appliers `gi_register.py`, `restatus_gi.py` and `../opus-gi18-gambit-arms-1001/gi18_apply.py` re-run as ALREADY, FAILS 0.
