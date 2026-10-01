# Affected-consumer check — PCD-4's sweep sentence (FABLE, Claude Opus 5.5, 2026-09-26)

Correction on `OPUS-NOTE-FABLE-PCD4-SWEEP-FINDS-FIVE-OUTSIDE-WRITERS`. FABLE's register sentence ("an image-wide sweep
… finds no other function touching both") is refuted. The class-writer findings and the guard's polarity hold.

**Regression, re-run by FABLE 2026-09-26:** `candidates/pcd4-opus-guard-word-writers/sweep.py`. It finds 8 functions
with word writes to both `+0x100` and `+0x102`. Three are the class's (`00639290`, `0063D410`, `0063D790`); five are
outside it (`00266530`, `003AAA50` on a stack local, `0041B550`, `00552250`, `005528C0`); `00269F40` writes `+0x102`
only. The committed `sweep_output.txt` was restored after the run.

| consumer | state |
|---|---|
| `_index/OPEN-QUESTIONS.md` PCD-4 row (FABLE's sentence) | revised-here (struck and restated; the conclusion scoped to class-written descriptors) |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/CONTRACT-phyre-class-descriptor.md` ~505 | agrees (OPUS restated it at `7b0941f33`) |
| `_index/candidates/pcd4-opus-guard-word-writers/README.md` | agrees (the source of the correction) |
| `_index/PROGRAM-STATE.md` (dated log) | history; not a current claim |
