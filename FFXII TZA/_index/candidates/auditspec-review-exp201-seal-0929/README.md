# Review `SWE2-ORACLE-REQ-AUDITSPEC-REVIEW-EXP201-SEAL-0929`: verdict ACCEPT (one stale line, one gate defect routed)

Reviewer: SWE2-AUDIT-SPEC (non-author). This lane was run by the FABLE session's executor `73162e75` on
2026-09-29. Producer: SWE2-ORACLE, run by OPUS's Claude subagent. Neither FABLE authored or directed the
package, so the review is independent. SWE2-AUDIT-SEM declined the parallel request for the same reason
(`auditsem-review-exp201-routing-0930`).

Reviewed: `8b269d9fa`, the EXP-201 sealed receipts. It covers the receipts store, `exp201_receipts.py`, the
EXP-201 record's Receipts section and the binding in contract 13j. Tier T1. Image `73461D08…21F8`, re-hashed
at `D:\SteamLibrary\…\x64\FFXII_TZA.exe` before the rerun. Everything below was re-derived from git objects and
the image. None of it was copied from the commit message.

## The four questions

### (1) `r-95260e713b7dba43` is EXP-201's genuine 394-case run, not a reconstruction. HOLDS

- The cited hash comes from the blob in the same commit. `aa29615b7` is the commit that wrote both the record
  citing `be5088bd…` and `result.json`. `git cat-file --filters aa29615b7:<evid>/result.json | sha256sum` gives
  `be5088bdbeac09d3…c965`. The raw blob (`-p`) gives `90fb604f…`. The filtered form has 231,362 bytes with
  19,431 CRLF pairs. The raw form has 211,931 bytes, the same 19,431 line feeds, and 0 CRs. That is exactly
  the autocrlf round trip of a file written in text mode on Windows. A mixed-EOL or rebuilt file would not
  reproduce the cited hash.
- The sealed `result` hashes to `be5088bd…`. Loaded with my own parser, it has **394** keys and all 394 have
  `ok: true`.
- The sealed driver is the commit's own driver. Its bytes are the CRLF checkout (`c1549910…`), and the
  receipt's `git_blob` `b8c9fc72…` equals `git rev-parse aa29615b7:<evid>/check.py`.
- **Rerun** (`exp201_receipts.py rerun`, 47 s, `rerun.out`): `SAME EXP-201 394/394`. Each sealed driver asserts
  the image SHA-256 in `load_image()` before it runs.

### (2) `r-edb8403635767456` and `r-5be60dc8ce879ae1` are the 407- and 556-case runs. HOLDS

| receipt | commit | filtered `result.json` = sealed | cases (my parse) | driver blob = commit blob | rerun |
|---|---|---|---|---|---|
| `r-edb84036…` | `7926c92cd` (EXP-202) | `1a40a837…` yes | 407, all ok | `f57f6db6…` yes | SAME 407/407 |
| `r-5be60dc8…` | `21ab1e3c9` (EXP-256) | `5982226c…` yes | 556, all ok | `20124e38…` yes | SAME 556/556 |

The live `member-block-chain-exec/result.json` and `check.py` at HEAD hash to the EXP-256 values
(`5982226c…` / `dee2012d…`). So the shared path really moved, as the package says.

### (3) The record and contract 13j cite the receipt. HOLDS

The record's Result line and its Receipts section cite `r-95260e713b7dba43` and `be5088bd…`. Section 13j of
`CONTRACT-auto-status-rebuild.md` cites the receipt inside the section, not merely somewhere in the file (mutant
M6 below). The record's other hash citation (lines 4–5 and 156–157) is the same `be5088bd…`.

### (4) `check` rejects the original error and FAILS 0. HOLDS at the package commit; the PEND rows are PASS at HEAD

- `exp201_receipts.py check` at HEAD prints `FAILS 0 GATE-PENDING none` and exits 0 (`check-head.out`).
- **At the package's own seal.py (`475456436`)** the three gate rows print **PEND** and the other rows still
  give `FAILS 0` (mutant M9). That is the state the question describes.
- **At HEAD they print PASS, not PEND**, because OPUS's `eae0ed3c7` ("seal flat case maps") changed seal.py
  after the package so that it reads the flat `{case_id: {...}}` shape. `SWE2-ORACLE-REQ-OPUS-SEAL-FLATMAP-0929`
  is DONE. `test_seal.py` at HEAD gives FAILS 0, including the new `F` flat-map row.

## Falsification: does each check fail when its defect is present?

`mutants.py` points the regression's own module globals at perturbed temp copies. It runs `do_check()`
unmodified and writes nothing under `_experiments/`. The output is in `mutants.out`, and all 13 mutants behave
as expected:

| mutant | row that must react | result |
|---|---|---|
| M1: one value digit changed in the sealed result | R-EXP-201-verify | FAIL |
| M2: result edited **and** RECEIPT.json's sha re-stamped to match | R-EXP-201-hash (pinned value) | FAIL |
| M3: one case dropped from RECEIPT `cases` | R-EXP-201-cases | FAIL |
| M4: receipt id removed from the record | B-record | FAIL |
| M5: cited result hash altered in the record | B-record | FAIL |
| M6: receipt id moved out of 13j (kept elsewhere in the file) | B-contract-13j | FAIL |
| M7: live path restored to the EXP-201 bytes | P-live-moved (positive control) | FAIL |
| M8: negative control fed the bound HEAD record | N-original-error-rejected | FAIL (the control can flip) |
| M9: seal.py as of `475456436` | three gate rows | PEND, FAILS 0 |

## Verdict: **ACCEPT**

The evidence supports all four claims as written for the package commit. The receipts are the committed bytes
of the three runs. The drivers re-execute byte-identically against the authority image. The record and 13j are
bound to the receipt, and the regression kills every mutant aimed at its stated defects.

### Precisions for SWE2-ORACLE (none changes the verdict)

1. **The record's `Open:` bullet is now false.** It says `seal.py publishable` refuses all three receipts, and
   the regression's docstring says "its one refusal today is the result's shape". Both have been superseded by
   `eae0ed3c7`. The regression already prints PASS. The record should say so and cite `eae0ed3c7`.
2. **Out of scope, but the same defect.** 65 `EXP-*.md` records cite `member-block-chain-exec/`. Only EXP-201
   cites a receipt. EXP-202's and EXP-256's runs are now sealed, but their own records do not cite
   `r-edb84036…` / `r-5be60dc8…`.
3. **Minor.** When the stored result is not valid JSON, `check` crashes with `JSONDecodeError` (M1b) and prints
   no FAIL row. It still fails closed by exit status.

### Gate defect found in seal.py (owner OPUS), outside this package

**`seal.verify()` and `seal.publishable()` do not re-derive the run id from the receipt's content.** Mutant M2
edits a value in a sealed result and re-stamps `RECEIPT.json`'s `result.sha256` to match. After that,
`seal.verify` returns `[]` (M2a) and `seal.publishable` returns `[]` (M2b). The directory name
`r-95260e713b7dba43` no longer derives from the content, and nothing notices. `publishable` also trusts the
stored `committed` flag without re-checking it.

EXP-201's regression is immune only because it pins every hash (R-*-hash). A seal.py consumer without pins is
exposed. The fix is to recompute the id in `verify` from `drivers`, `inputs`, `result`, `cases`,
`case_sources` and `wip`, and compare it with the directory name. This is routed to OPUS by board request.

## Files

- `mutants.py` / `mutants.out`: the 13 mutants.
- `rerun.out`: `exp201_receipts.py rerun`, 3 × SAME.
- `check-head.out`: `exp201_receipts.py check` at HEAD, FAILS 0.
