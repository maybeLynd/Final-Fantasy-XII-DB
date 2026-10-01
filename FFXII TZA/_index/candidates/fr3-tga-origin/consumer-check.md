# FR-3 consumer check (FABLE, Claude Opus 5.5, 2026-09-26)

**Corrected claim.** `shipped-standard-formats.md` §2.1 said the TGA decode lay in "`001D8D60`'s image path
(`00597970` / `0059D920`)". Its pass-22 crossings note called the same two functions "the image-path helpers".
Both labels are wrong. `00597970` constructs the file stream (`PStreamReaderFile`) and `0059D920` is its `IsOpen`
test, as the owning page, `how-a-path-is-resolved-to-bytes.md`, already says. The decode is `001D8D60` itself.
It reads only the width and height from the header, and it copies rows top-down through `001EE820` with the flip
argument fixed at `0`. So the descriptor's origin bit is not honoured.

**Regression:** `tga_origin.py` in this directory, 7 checks, FAILS 0.

## Consumers of the corrected text

A grep of the database for `00597970` and `0059D920` finds these citations, each checked:

| Consumer | What it says | Disposition |
|---|---|---|
| `shipped-standard-formats.md` §2.1 | "image path (`00597970` / `0059D920`)" | Struck and corrected in this publish |
| `shipped-standard-formats.md` pass-22 crossings | "The image-path helpers" | Struck and corrected in this publish |
| `shipped-standard-formats.md` FR-3 box | "the decoder beneath `001D8D60`" | Ticked with the answer. The wording names no helper, so it stands |
| `OPEN-QUESTIONS.md` FR-3 row | "the TGA decoder beneath `001D8D60` (`00597970` / `0059D920`)" | Restated ANSWERED in this publish. The status says the two are the stream constructor and `IsOpen` |
| `how-a-path-is-resolved-to-bytes.md` | `00597970` = `PStreamReaderFile` constructor; `0059D920` = **IsOpen** | Agrees. It is the source of the correction |
| `language-selection-and-locale-ids.md` line 568 | "the `0059xxxx` text-service battery" in `001D8D60`'s row | Does not claim an image decode. It is a family label from a peer's interior citation. Not changed |
| `game-application.md`, `how-the-prefetch-manifests-are-read.md`, `game-settings-ini-and-runtime-config.md`, `the-post-process-passes-and-their-shader-constants.md`, `object-construction-destruction-and-static-lifetime.md`, `lazy-statics-and-the-one-time-init-lock.md` | Stream, file-cache or serialisation roles | None calls them an image decoder. Not affected |
| `ADDRESS-INDEX.md` | Links only | Not affected |

No other page states where the title-image TGA is decoded or how its origin is treated. The inventory line
"tga : ... top-left origin" (§3 and the format-sheet summary) describes the shipped file's header. It stays true.
