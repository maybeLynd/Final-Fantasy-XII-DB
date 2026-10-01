# Affected-consumer check: MT-1 answered; `006FF900` corrected from "teardown" to initialiser (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `mt1_container_values.py` beside this file (11 checks, FAILS 0).

The container page's 2026-09-17 narrowing called `006FF900` "the object's teardown". It is the block's initialiser:
- the allocating routine calls it on the freshly constructed, just-published block and sign-tests its status;
- it creates the `IGPUDevice` the three caches use;
- its own diagnostic strings name it `CPostEffect::Initialize`, as the post-processing pages already did.

The narrowing's structural facts are unaffected: it runs the three map tidies, and its two callers are as stated.

| consumer | what it said | state |
|---|---|---|
| `24-Compiler-And-CRT-Runtime/Cxx-Runtime-Families/the-msvc-ordered-container-runtime.md` §7, the 2026-09-17 narrowing | "`006FF900`, the object's teardown" | revised-here (struck, corrected beside it) |
| same page §7, the MT-1 box | open; `+0xA8`/`+0xB8` value types unread; B's keys and values unread | revised-here (ticked; A, B and C answered beneath) |
| same page §7, the MT-2 box | "What is still not named is the tree's key/value types — that is MT-1's question" | revised-here (dated note: one 8-byte element, and no use in the shipped code to name it) |
| same page §7, the 2026-09-18 narrowing (`+0xC8` is a `CRenderTexture` cache) | the `+0xC8` reading | agrees (the control's A1 finds the same slot-60 creator; the `CRenderTexture` wrapping is that narrowing's reading and is not re-derived here) |
| `17-Presentation-Rendering/Post-Processing/CONTRACT-post-processing-subsystem.md` | `006FF900` is `Initialize` | agrees |
| `17-Presentation-Rendering/Post-Processing/the-post-processing-effect-catalogue.md` | `006FF900` `Initialize`; the one live route to it | agrees |
| `22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md` | `006FF900` the `CPostEffect` member-resource populate | agrees (a populate run at initialisation) |
| `24-Compiler-And-CRT-Runtime/Runtime-Service-Surface/ppfx-diagnostic-strings.tsv` | the `CPostEffect::Initialize()` strings attributed to `006FF900` | agrees (the correction rests on them) |
| `_types/types.tsv` `CPostEffect` | `0xD40`, published at `02EA0B70` | agrees (the answer names the block by it) |
| `01-Script-VM-Native-Bridge/Interpreter-Core/worldactor-scriptvm-interpreter.md` (outlier note) | `006FF900` is 23,568 B | agrees (size only) |
| `_index/OPEN-QUESTIONS.md` MT-1 | PARTIAL; its question cell repeats "the object's teardown" | revised-here (ANSWERED, and the status cell says the question cell's "teardown" is superseded) |
