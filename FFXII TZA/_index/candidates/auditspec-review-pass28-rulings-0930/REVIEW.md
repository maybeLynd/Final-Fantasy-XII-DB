# Audit-spec review: OPUS pass-28 — 24 cross-document claim rulings

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `doc-claim-crossrefs.tsv` rows at `4a6286062`
Board task: `OPUS-REQ-AUDITSPEC-PASS28-RULINGS-0930`

## Verdict: ACCEPT (rulings correct at the reviewed commit; drift noted)

## What was checked — sample re-reads against both documents

| verdict word | sampled row | finding |
|---|---|---|
| LINK-TEXT | CONTRACT-boot-fixups → `boot-fixups-falsification-pass-1-0929` | line 845's link text is the record dir name; the README doesn't repeat it; link resolves ✓ |
| PARAPHRASE | mweather → choosing-the-field-environment-variant | target line 134: `003777C0` with `(bit 0, width 3)` — the citing `(selector, slot, bitOffset 0, width 3)` is the same call ✓ |
| OWN-EVIDENCE | map-screens → CONTRACT-widget-object `+0x5C` | +0x5C appears in the citing page's own sentences (759/767/773); the link supports a different clause ✓ |
| RESOLVER-ARTIFACT | actor-record → backticked `OPEN-QUESTIONS.md` | backtick citation, not a link; checker resolved the bare name to a fixture copy — neither page wrong ✓ |
| RETAINED-SNAPSHOT | facing-wrap-antipode/retained/question-ledger.md + script-array-flatten-width/retained/opus-index-primary-before.md | both are retained historical copies under `_experiments/evidence/`; correctly ruled "must not be edited to follow" ✓ |

## The two new verdict words — ruled acceptable

- **RESOLVER-ARTIFACT** is correctly scoped: it names the *checker's* misresolution of a bare
  filename, declaring neither page defective. Sound.
- **RETAINED-SNAPSHOT** is correctly scoped: evidence preimages must not chase their targets —
  editing them would falsify history. Sound and required by evidence policy.

## Forward drift (information only)

`check_doc_claims.py` at HEAD reports **99 claims / 68 documents, 53 unruled** — the
"exits 0" state held at `4a6286062` and has since drifted: post-commit incorporations cite new
terms (record dir names, commit shas like `59ec09a95`/`ce2b4380d`, `sd140-vertex-prep-kernel-0930`
etc.). The TSV's own header warning is vindicated — each new cite needs a row. A further ruling
pass is owed; the pass-28 record itself verifies.

## Narrowing / notes

None required on the package. The unruled-claim growth is follow-up work, not a defect in the
reviewed rulings.
