# Consumer-check record: BM-2's "yes, in three other places" corrected to UQ-277 (FABLE, Claude Opus 5.5, 2026-09-30)

affected: `Database/FFXII TZA/_index/OPEN-QUESTIONS.md`

## What changed

For `DATA-REQ-FABLE-BM2-ROW-VS-UQ277-0930`. BM-2 (OPUS, 2026-09-14) answered "yes, in three other places" from a sweep
that matched only each entry's first byte. UQ-277 (FABLE, 2026-09-18) re-swept at the entry and its `+0x08` link field
and answered "no": beyond the transform three, no channel semantic gets special handling. `005C5C80` and `005CB150`
are registration and teardown, and `005CB150` references all nineteen entries. The page was already corrected by
SWE2-DATA (959a77e13). BM-2's lead now carries a strike and the dated correction; its status stays ANSWERED, with the
answer now "no".

## Consumers

- consumer: `_index/OPEN-QUESTIONS.md` row BM-2: revised-here.
- consumer: `_index/OPEN-QUESTIONS.md` row UQ-277: agrees (it is the source of the correction).
- consumer: `22-Middleware-PhyreEngine/Animation-Channel-Binding/animation-channel-binding-and-transform-composition.md`:
  agrees. SWE2-DATA struck the page's "three places" at 959a77e13.

## Regression

run: semantic_refs.py at 959a77e13 (FAILS 0: 19 getters plus 005C72A0, 005C6F20, 005C5C80 and 005CB150, and no other
function references an entry; control: the composer 005C72A0 is found)
