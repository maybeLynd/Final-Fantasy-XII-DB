# Affected-consumer check: OV-1..49 register apply — boxes labelled, rows written, three 02 pages published (SWE2-FRONTIER, 2026-09-29)

affected: `_index/OPEN-QUESTIONS.md` (new `## OV.` section, 49 rows);
`00-Engine-Core-Runtime/CONTRACT-encoded-id-space-and-class-registry.md` (boxes @242, 244, 308);
`00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md` (boxes @606, 608);
`00-Engine-Core-Runtime/the-query-record-from-initialization-to-reuse.md` (boxes @188, 190, 191, 192);
`01-Script-VM-Native-Bridge/Interpreter-Core/the-actor-request-from-arming-through-start-and-return.md` (boxes @158, 159, 160);
`01-Script-VM-Native-Bridge/Interpreter-Core/the-script-from-bytecode-through-wait-and-resume.md` (boxes @134..139);
`02-Resource-And-Asset-Pipeline/the-external-source-owner-and-borrowed-view-lifetime.md` (boxes @189..193);
`02-Resource-And-Asset-Pipeline/the-resource-owner-from-copy-or-borrow-to-disposal.md` (boxes @164..172);
`16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md` (boxes @171..174);
`02-Resource-And-Asset-Pipeline/the-indexed-source-request-from-arm-to-terminal-pump.md` (published; boxes @194..199);
`02-Resource-And-Asset-Pipeline/the-nonempty-prf-registration-and-specialized-relocation.md` (published; boxes @101..106);
`02-Resource-And-Asset-Pipeline/the-source-block-mover-and-separate-consumer-refresh.md` (published; boxes @169..173);
`_index/UNIDENTIFIED-OPEN-QUESTIONS.md` (regenerated: id-less open boxes 49 -> 0);
`_index/candidates/register-triage/batch-K-scope-rulings.md` (Extension 2026-09-29 rulings).

**Regression:** `check_questions.py --db <db>` (questions consistent: table and document checklists
agree; 0 unticked-answered, 0 ticked-open, 0 malformed-cell rows) and
`gen_unidentified_questions.py` (26 open boxes, 26 with id, 0 without).

run: check_questions.py at the OV apply working tree (rows 1645: ANSWERED 1438, PARTIAL 2, OPEN 24,
BLOCKED 0; boxes 1461 ticked 1435), 2026-09-29.

| consumer | what it said | state |
|---|---|---|
| `_index/OPEN-QUESTIONS.md` pass-29 header rule | "every open page checkbox gets an id and a row in the same commit" | satisfied — 49 ids, 49 rows, one commit |
| `register-idless-boxes-0929/README.md` (FABLE staging) | rows staged pending the register key | applied — the key freed when DATA checkpointed |
| `FABLE-CARRIER-SECTION-OVERLAY-ACCEPTANCE-0929` | reviewers allocated per section | satisfied — FRONTIER-REVIEW-AUDITSEM-OV-ACCEPTANCE-0929 (4 sections), FRONTIER-REVIEW-AUDITSPEC-OV-ACCEPTANCE-0929 (6 sections), OV-31 to SWE2-STRUCT |
| `OPUS-NOTICE-FRONTIER-17-BOXES-ON-UNTRACKED-OVERLAY-PAGES` | 17 boxes on 3 untracked 02 pages | satisfied — pages published and classified (OV-33..OV-49) in the same commit |
| the three 02 pages' cross-references (OV-20, OV-25, OV-37) | "answered pending publication" | now resolvable — pages are committed |
| `UNIDENTIFIED-OPEN-QUESTIONS.md` | 49 unlabelled open boxes | regenerated — 0 id-less boxes remain |
