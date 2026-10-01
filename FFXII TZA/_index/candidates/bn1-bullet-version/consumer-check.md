# Affected-consumer check: BN-1 answered; "nothing in it separates those releases" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `bn1_bullet_version.py` beside this file (3 checks, FAILS 0).

The Bullet page's 2026-09-17 narrowing said the serializer's type-name set "bounds the version without pinning
it … nothing in it separates those releases. The exact number is not in the image." One chunk name does separate
them:
- the triplet short-index name exists only after 2010-02-27;
- the missing `PHY_UCHAR` case and its name exist only from 2011-01-07.

Between those dates the only release is 2.77. The RTTI's local island-callback class gives an independent upper
bound.

| consumer | what it said | state |
|---|---|---|
| `23-Third-Party-Libraries/Bullet-Physics-Integration/phyre-to-bullet-rigid-body-materialization.md`, `UQ-302` box | "nothing in it separates those releases. The exact number is not in the image" | revised-here (struck; answered beneath; box ticked) |
| same page, frontmatter `status` | "the exact Bullet version (UQ-302, bounded below 2.82 …)" | not revised: a status summary; the ticked box and this record carry the answer, and the frontmatter is refreshed with the page's next status review |
| `_index/OPEN-QUESTIONS.md` UQ-302 | SUPERSEDED onto `BN-1` | agrees |
| `_index/OPEN-QUESTIONS.md` X-8 (exact versions of six libraries) | Bullet among the unknown versions | agrees as an open row; its Bullet clause is answered by `BN-1`, the other five libraries stay open |
| `_index/OPEN-QUESTIONS.md` BN-1 | PARTIAL; bounded below 2.82 | revised-here (ANSWERED; the previous status kept as history) |
