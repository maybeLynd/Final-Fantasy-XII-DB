# Correction: `003A1DB0`'s caller count in the auto-status rebuild's crossing paragraph (FABLE, 2026-10-03)

*FABLE, on `OPUS-REQ-FABLE-AUTOSTATUS-3A1DB0-CALLERS-1002`.* FABLE's pass-22 crossing paragraph (Presentation) on
[CONTRACT-auto-status-rebuild](../../../10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md) said
`RenderCommand_SubmitCurrentBufferAndSwap` `003A1DB0` has "16 callers".

**At the bytes.** A raw `E8`/`E9` rel32 scan of `.text` gives 47 direct sites: 41 calls and 6 tail jumps. They lie in
38 distinct functions, and every site is inside a listed function. This matches OPUS's count and what
[what-happens-between-two-frames](../../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)
states. Where the "16" came from is not recorded; it is not the image-wide count.

**Edit.** "16 callers" is struck and replaced by "47 direct call sites in 38 functions", with the correction note. Indirect
callers are not covered.

## Consumer check (FABLE)

affected: `Database/FFXII TZA/10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md`

- consumer: the crossing paragraph on the auto-status page: revised-here.
- consumer: what-happens-between-two-frames.md: already states 47 (no change).

run: raw E8/E9 census of 003A1DB0 at 8e19fc948 (41 call + 6 jmp sites, 38 functions, 0 outside a listed function)
