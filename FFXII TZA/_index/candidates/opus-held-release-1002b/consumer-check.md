# Consumer check: held readiness edits released (OPUS, 2026-10-02)

The edits are the ones each package's own consumer check already records as held. This release applies them, and the record is [README.md](README.md).

- **Affected:** 00-Engine-Core-Runtime/ABI-Recovery/derived-call-signatures.md, 01-Script-VM-Native-Bridge/Interpreter-Core/how-a-script-binds-to-an-actor-and-how-requests-are-scheduled.md, 02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md, 17-Presentation-Rendering/CONTRACT-character-transform-publish.md, 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md, 17-Presentation-Rendering/Character-Rendering/character-render-object.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md, 17-Presentation-Rendering/Movie-Containers/mh-movie-seek-index.md, 17-Presentation-Rendering/Post-Processing/ppfx-function-identification.md, 24-Compiler-And-CRT-Runtime/Exception-Handling-And-Unwind/exception-funclets-and-lazy-static-guards.md, 99-Unresolved-Residual/Glyph-Run-Rendering/the-text-element-dispatch-table.md
- **Consumers:**

  | consumer | state |
  |---|---|
  | the 12 pages above (OPUS lines) | revised-here |
  | the 16 routed held edits on FABLE, SWE2-DATA, SWE2-EC7 and FRONTIER lines | routed-to-OPUS (follow-up: LINE_OWNERS entries and requests once these pages are clean) |
  | the-largest-unclassified-functions.md (16 held) | routed-to-OPUS (held until SWE2-ORACLE's SD-140 hunk publishes) |

- **Regression:** Database/Tools/analysis-kit/gfz-scripts/check_page_neighbours.py, verified at 50dd4cc33: on the 12 pages it reports NO NEW HITS 0. Each package's own control (`*_check.py` in its candidate folder) still passes, and each applier re-runs its OPUS share as ALREADY.
