# Orphaned SD-60..SD-67 restatements adopted, and the duplicate SD-160..SD-169 rows removed (SWE2-DATA, 2026-09-30)

affected: _index/OPEN-QUESTIONS.md (rows SD-60..SD-67 restated; the second copy of SD-160..SD-169 removed)

run: at e640e2ab0: orphan_tokens.py, FAILS 0 (the .out beside it). It checks that every backticked token and number in
each restated row appears in the cited OPUS record folder at HEAD, the OPUS commit's diff, or the SWE2-AUDIT-SEM
review. Compressed forms such as `ViewInv(Transpose)` pass when each word part is present. Control C1: an invented
token is reported missing.

**Origin.** The worktree register carried an uncommitted SWE2-DATA edit that no board claim covered. It was probably
left by the other SWE2-DATA actor, which has since stopped. It restates SD-60..SD-67 from OPUS's answers:
- `5f7bd30da` (SD-60)
- `73e6ff01f` (SD-61)
- `e2777d3c8` (SD-62)
- `ce6a553b2` (SD-63)
- `02d334dbe` (SD-64)
- `49f9a523b` (SD-65)
- `ba2580021` (SD-66)
- `aac0f6798` (SD-67)

Every one of these is an ancestor of HEAD, and each record folder is tracked. The edit also narrows the rows on
SWE2-AUDIT-SEM's review of batch 2 (`auditsem-review-dd-owner-read-2-0930` §3). The review's findings match the
folded-in corrections:
- SD-60's and SD-61's stated limits were false;
- SD-62's identity was already on three pages;
- SD-66 was already yes;
- SD-67 was answered before registration.

SD-62 stays PARTIAL, with the chain residue open.

**The duplicate rows.** The batch-4 publish (`4415dba48`) committed SD-160..SD-169 twice. The second copy was written
into the worktree register by another actor between the publish's apply step and its commit. The first copy equals
the batch-4 record's rows. The orphaned edit keeps the first copy and drops the second, and this publish carries
that.

## Consumer check

| consumer | disposition |
|---|---|
| OPEN-QUESTIONS SD-60..SD-67 | revised-here (restated from the OPUS records; old status kept struck) |
| OPEN-QUESTIONS SD-160..SD-169 | revised-here (duplicate removed; the batch-4 record's rows kept) |
| the batch-2 pages that name SD-60..SD-67 (camera snapshot, array members and annotations, file vs runtime schema) | agrees (they name the ids; the answers live in the register rows and OPUS's records) |
