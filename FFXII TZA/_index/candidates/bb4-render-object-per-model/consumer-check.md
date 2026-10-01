# Affected-consumer check: BB-4 — a render object per record, recycled per model, never shared (FABLE, Claude Opus 5.5, 2026-09-26)

affected: BB-4; 17-Presentation-Rendering/Character-Rendering/character-render-object.md (the BB-4 box and its 2026-09-15 narrowing)

**Regression:** `bb4_render_object_per_model.py` beside this file (5 checks, FAILS 0).

run: bb4_render_object_per_model.py at 8a409b895 (FAILS 0), 2026-09-26.

**The correction.** OPUS's 2026-09-15 narrowing read the construction site `001BD4A0` as "one `CharacterRenderObject`
per distinct `[record+0x2A0]`, created lazily on first miss and shared thereafter". It said that two records with the
same value share one object, and that there is no count because the objects are held in a tree.

Read past the construction, the function says otherwise:
- **The hit path takes the object out of the tree node.** It pops the node's first list element, resets the object,
  unlinks and frees the element, erases an empty node, and appends the object to an active vector.
- **The release `001BD840` puts it back** under the model key `[[object+0x488]+0x2A0]`.
- **The acquirers and releaser are the character render records** (`+0x6B0` model id, `+0x6B8` object).

So each active record holds its own object; the tree holds only released objects, as a per-model pool.

**Also mine, caught before publishing.** Earlier this session I read the same function the same way and drafted
"one per model resource, shared". That draft never published: its runner was stopped and the page restored. The
reading and correction are recorded here so the error is not repeated.

| consumer | what it says | state |
|---|---|---|
| `17-Presentation-Rendering/Character-Rendering/character-render-object.md` BB-4 narrowing (2026-09-15, OPUS) | "shared thereafter"; "Two character records carrying the same value share one object"; "two visible characters with the same key share one"; "there is no count to establish … held in a tree, not in an array" | revised-here (struck verbatim, corrected; answer added) |
| `_index/OPEN-QUESTIONS.md` BB-4 | the same rule in the 2026-09-15 narrowing | revised-here (status restated ANSWERED, correcting it; history kept) |
| `06-Movement-And-Navigation/heading-speed-to-position-delta.md` ~799 | "`FUN_001BD4A0` (sole construction site)" | agrees (it is the only allocation site; nothing about sharing) |
| `17-Presentation-Rendering/CONTRACT-character-render-object.md` | no cardinality statement | agrees |
| the narrowing's author | OPUS | routed-to-FABLE-REQ-OPUS-ACCEPT-BB4-RECYCLE-POOL for independent acceptance of this co-authored repair |

**Bounds, kept on the page:**
- the pool singleton's update also acquires, with id `−1`;
- the `3` stored with a pooled object (a likely expiry count) is not followed.
