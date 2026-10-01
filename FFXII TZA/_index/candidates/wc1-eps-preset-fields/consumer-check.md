# Affected-consumer check: WC-1 answered - the eps preset fields read from the code (FABLE, Claude Opus 5.5, 2026-09-27)

affected: 18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md (section 7, the WC-1 box)
run: controls.py at 449a2832d (worktree = that HEAD plus this package): reproduces controls.out byte for byte, all asserts pass. Check (a) measures the class/vtable/classId table; (b) the known-answer constants.

| consumer | what it said | state |
|---|---|---|
| `18-Audio/Sound-Bank-And-Voice-Formats/sead-win-config.md`, section 7, WC-1 box | "Remaining: the per-field names inside each eps class's preset block" | revised-here: answered beneath; the box is ticked at publish time |
| same page, section 6d (SWE2-DATA): "param-descriptor tables (01CB7xxx - {metaPtr, ...} entry blocks, e.g. SurroundReverb's +0x30 entry 008F5F50)" | that the field names sit in those tables | routed to SWE2-DATA, the author: board note 34619 says 008F5F50 is MSVC FuncInfo. FABLE's answer does not depend on the sentence; the roles are read from the code |
| same page, section 7's "Still open (after section 6d)" list | eps field semantics, bus +0x0B, epsp stream-B tail, ctgl +0x04 | the eps item is answered here; the other three were already resolved in section 6d's own text (dead-authored or decoded) |
| _index/OPEN-QUESTIONS.md WC-1 | PARTIAL (lifetime half answered; mirrored 2026-09-26) | revised-here: ANSWERED, crediting section 6d for the other chunks |

Regenerated with it: nothing (fields.tsv is new).
