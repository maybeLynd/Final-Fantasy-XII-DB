# Affected-consumer check: BL-8 - the descriptor's `+0xB0` list is never read (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md (§14 item 1, the `+0xB0` row and its "Not established" line), 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/member-registration-and-the-recovered-field-schema.md (the BL-8 box)
run: bl8_walkers.py at 939c7f6d7 (worktree = that HEAD plus this package), FAILS 0; the +0x90/+0xA0 name-lookup walkers are the sensitivity control and the destructor the known positive.

| consumer | what it said | state |
|---|---|---|
| `CONTRACT-phyre-class-descriptor.md` §14 item 1, `+0xB0` row | "nothing, as far as the sweeps below reach ... no insert found" | agrees; extended beneath with the walker census (no reader) |
| same, "*Not established:* what `+0xB0` was meant to hold" | open | agrees; stays open as intent, NAS review requested |
| `member-registration-and-the-recovered-field-schema.md`, BL-8 box | `+0xB0` still unnamed; no insert | revised-here: narrowing added beneath; box stays open |
| same page ~281 | `+0xB0` still unnamed, no insert found | agrees |
| _index/OPEN-QUESTIONS.md BL-8 | PARTIAL, `+0xB0` unnamed | revised-here: PARTIAL, narrowed (never read) |

Regenerated with it: nothing.
