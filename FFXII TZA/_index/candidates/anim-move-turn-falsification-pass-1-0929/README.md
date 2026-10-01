# Consumer check: falsification pass 1 on how-an-animation-moves-and-turns-a-character-toward-its-target (OPUS, 2026-09-29)

corrects: 06-Movement-And-Navigation/how-an-animation-moves-and-turns-a-character-toward-its-target.md (section 2: CON-186)

## What was corrected

- **One global switch per stage.** The take `003AED70` tests `02B3F53C`, with the list's `+0x28` and `+0`. The second
  switch `02B3F540` gates the per-frame consumer `003AEF90`. With the second one up, requests still queue but nothing
  advances or frees.
- **Note, not a correction:** the accessor census (`24-Compiler-And-CRT-Runtime/Generated-Families/members/`
  `trivial-global-accessors.tsv`) lists `003AF330` as a writer of `02B3F540`. That is one of the setters section 6
  says were not traced.
- **What survives.**
  - The command handler and the request builder.
  - The 64-byte view.
  - The pool: 128 × `0x60`, and the sign pair.
  - The `@FRM` profile-table window.
  - The step's frame windows.
  - Mode `0x16`.
  - The clamp.

## Current consumers

- consumer: `04-Actor-Entity/the-field-runtime-pass.md` says `003AEF90` "gates on `02B3F540`==0"; it agrees.
- consumer: `17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md` describes
  `003AF2B0`'s clears only; it agrees.
- consumer: `_index/CONTRADICTIONS.tsv`: revised-here (`CON-186`).

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_anim_move_turn.py` A6. It fails unless `003AED70` reads
`02B3F53C` and not `02B3F540`, and `003AEF90` tests `02B3F540` at `003AEFA5`.

run: verified at c90fbf657 (BROKEN 0, exit 0), against the certified image `73461d08…`.
