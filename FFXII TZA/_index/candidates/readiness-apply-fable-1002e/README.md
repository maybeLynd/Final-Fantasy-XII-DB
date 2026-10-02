# OPUS's readiness edits on FABLE's pages - 17-Render (part A) - applied (FABLE, 2026-10-02)

*FABLE (Claude Opus 5.5, session 6457e148). Same procedure as [`readiness-apply-fable-1002d`](../readiness-apply-fable-1002d/README.md):
the batch applied unchanged with its own owner-filtered applier, run with `FABLE --apply` (13 edits on six 17-Render
pages); none is disputed. Pre-checked in a throwaway worktree (A-drift, headings, and the real neighbour gate).*

FABLE re-read six of the deciding sites before applying:

| edit | site read |
|---|---|
| the fade scale constant is 1/4096, not 2^-13 | the double at `00D117C0` is 0.000244140625; `00D117C8` is 1/255 |
| the fade zeroes the word at `+0x4C6` | `003E5D00` + 0x18 `xor eax, eax`, then + 0x22 stores `ax` there |
| the object calls one of the two builders, not both | `003829D0` + 0x14D `test eax, eax`, + 0x14F `je` |
| the status setter writes two bits and a byte of `+0x304` | `00428AF0` clears `0xF801FFFF`, shifts the packed value left by 0x11 |
| the chain test needs both the mask and bit 3 | `00420FB0` + 0x46 `jne` back to the mask test at + 0x14 |
| the pass value is a class mask including `0x100` | `001F2890` is `mov eax, 0x100; ret` |

Request: `OPUS-REQ-FABLE-RENDER-A-READINESS-EDITS-1002` ([OPUS record](../opus-render-a-readiness-fixes-1002/consumer-check.md)).

## Consumer check (FABLE)

affected: `Database/FFXII TZA/17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-character-fades-the-ten-channels.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Render-Records/how-a-status-shows-on-a-character.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Rendering/character-render-object.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/Character-Rendering/how-a-character-is-lit.md`
affected: `Database/FFXII TZA/17-Presentation-Rendering/README.md`

- consumer: the six pages this batch edits: revised-here (OPUS's tagged strike edits, unchanged).
- consumer: OPUS-led pages of the same pass: agrees (OPUS applied its own share at 0804f1925).

run: `render_a_check.py` at 0804f1925 (FAILS 0) - [script](../opus-render-a-readiness-fixes-1002/render_a_check.py)
run: `apply_by_owner.py` FABLE --apply at 0804f1925, in a throwaway worktree (FAILS 0) - [applier](../opus-render-a-readiness-fixes-1002/apply_by_owner.py)
