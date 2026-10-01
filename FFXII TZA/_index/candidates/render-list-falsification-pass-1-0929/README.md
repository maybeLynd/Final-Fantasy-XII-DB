# Consumer check: falsification pass 1 on CONTRACT-render-command-list-and-graphics-handshake (OPUS, 2026-09-29)

corrects: 17-Presentation-Rendering/CONTRACT-render-command-list-and-graphics-handshake.md (I-6's reader address in §3, I-6 and §15; I-2's leftover "two sites", §15 and §16; I-5 sharpened)
corrects: 17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md (the +0x10 reader's address)

## What was corrected

- **I-6's reader address.** The one reader of `OrderedObject +0x10` is `cmp byte ptr [rdi+0x10], bpl` at `0018C933`, a
  4-byte instruction; the cited `0018C934` is inside it. The `jne` at `0018C937` confirms the boundary. The claim itself
  (one reader, executed when zero) holds.
- **I-2's count.** Three teardown sites, not two. The image-wide census of both destroyers' callers finds exactly
  three, each with the clear first. The page had already added the third to I-2's first sentence but not to its last
  sentence, §15 or §16.
- **I-5, sharpened.** Both arms of `0018B1B0` call slot 2 twice per entry.

## Current consumers

- consumer: [the-ordered-render-command-list.md](../../../17-Presentation-Rendering/Render-Command-List/the-ordered-render-command-list.md): revised-here. Its `CON-149` paragraph cited `0018C934`.
- consumer: [the-shared-command-state-word.md](../../../17-Presentation-Rendering/Graphics-Thread-Handshake/the-shared-command-state-word.md) agrees. It carries neither the reader's address nor the site count.
- consumer: `_index/_inbox/OPUS.md` carries `0018C934` in a dated 2026-09-21 narrative. It is operational history, not a claim page, and stays as written.

## Regression

regression: `Database/Tools/analysis-kit/gfz-scripts/falsify_render_command_list.py`, checks R0-R13:
- R6 fails if `0018C934` becomes an instruction start or the reader moves;
- R2 fails if a destroyer gains a caller without the clear first.

run: verified at d9595b0e8 (BROKEN 0), against the certified image `73461d08…`.
