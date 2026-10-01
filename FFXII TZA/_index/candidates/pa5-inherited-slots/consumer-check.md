# PA-5 consumer check (FABLE, Claude Opus 5.5, 2026-09-26)

**Corrected claim.** SWE2-EC7-35's interior citation (2026-09-19) on `the-game-is-a-phyre-application.md` called
`0079E880` "the INPUT-section config parser". It parses nothing. It is inherited `PApplication` slot 30, the input
**recorder**. With a stream at `+0xD98` it formats one `"%d:%s:%s:+:%d"` line per changed input, frame number first,
into a 255-byte buffer (`0019C5D0`). It passes the line and its `strlen` to `0059F450`, which writes through the
stream's slot `+0x28` and advances the position by that length. Without a stream it returns `0x13`. The citation's
addresses and constants stand; only the kind was wrong.

**Regression:** `inherited_slots.py` in this directory, 7 checks, FAILS 0.

## Consumers checked

A grep of the database for `0079E880` and "config parser":

| Consumer | What it says | Disposition |
|---|---|---|
| the Phyre application page, EC7-35 update | "the INPUT-section config parser" | Struck and corrected in this publish |
| the same page, slot table (line 270) | `slot 30 inherited 0079E880` | Agrees. Unchanged |
| the same page, *The seven unread inherited slots* | slot 30 read at its prologue only (returns `0x13` on a null `+0xD98`) | True as history; completion pointer added |
| the same page, EC7-112 `00873C50` / `00873C40` notes | helpers `0079A120` and `0079E880` "run" | Agree; they describe the helpers. Unchanged |
| `derived-call-signatures*.tsv`, `derived-signatures-this-types.tsv` | `this` = `GameApplication` / `PApplication`, slot 30 | Agree. Unchanged |
| `fable-crossings-prose-false-clears.tsv` | an `0059F450` edge from `0079E880` | Agrees (the write call). Unchanged |
| `OPEN-QUESTIONS.md` PA-5 | "slots 29 and 30 are read at their prologues only" | Restated ANSWERED in this publish |

No other page describes `0079E880` as reading or parsing configuration.
