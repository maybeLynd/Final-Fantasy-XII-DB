# SWE2-AUDIT-SPEC review: ASTRA mixed science/owner publication prerequisite repair (mixed-publication-prerequisite-fix)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-MIXED-PUBLICATION-PREREQUISITE-FIX-1003` (reviews `ASTRA-PUBLISH-MIXED-PREREQUISITE-FIX-1003`) · Evidence: commit `ecc16850c936acaa57b97dc1194f01a4623ea945`, `_experiments/evidence/mixed-publication-prerequisite-fix/` · Real continuation: `64cb2c0c330931d7511a930c722b17a86afa6cfc`

## SWE2-AUDIT-SPEC verdict: ACCEPT

The repair does what the README says. It replaces one inline gate with one function and leaves every other guard unchanged. It refuses everything the request lists, and the producer's positive control is sensitive to the defect it repairs. The remarks below are limits and hygiene, not defects.

## SWE2-AUDIT-SPEC checks

**Provenance and bytes.**

- `manifest.json` sha256 is `ebf0ce56f8c74b092fb9e1db56e0a892ad7b37c11714b3dd81c63c82173a0734` (2386 B), as cited.
- All 14 members match their recorded bytes and sha256, both in the working tree and in the blobs of `ecc16850c`. The folder holds no unlisted file except `manifest.json`.
- The live working copies match the evidence copies:
  - `prepare-residue-packet-publication.py` = `publisher-after.py` (`eb288544...`).
  - `...before-owner-prerequisite-fix.py` = `publisher-before.py` (`5c1b458f...`).
  - `deliver-gauge-checkpoint77.py` = `gauge-delivery-after.py` (`3e8c5082...`).
  - `control-mixed-publication-prerequisite.py` = `control.py` (`05b4b3db...`).
- The control result's `prepared_qualification_sha256` `274a2e50...` equals the current `publication-ov42-gauge-and-checkpoint77-01/source-annotations-prerequisite-01.json`.
- The real attempt receipt records `driver_sha256` `eb288544...`, so the after-publisher ran the real publish. It records `publisher_exit` 0, commit `64cb2c0c3`, 93 explicit paths and `VERIFIED_AND_RELEASED`.
- `git show --name-only 64cb2c0c3` lists 93 paths, and `commit-verification.json` says `exact_paths` 93.

**Newline variants.**

- Every member is pure CRLF (no lone CR, no bare LF) except `control.py` and `.gitattributes`, which are pure LF.
- `publisher-before.py` has 8081 CRLF lines, of which 620 are non-blank. `publisher-after.py` has 16199 lines, of which 655 are non-blank. The extra lines are blank-line doubling inside triple-quoted docstrings, an artefact of repeated text-mode CRLF rewrites.
- With docstrings stripped, the two ASTs are identical except for the change described below. The newline-collapsed `verify_copied_render_review_links` is identical, and all 151 top-level non-def statements are equal. The inflation therefore changes only `__doc__` values, with no runtime effect.

**AST diff (the entire semantic change).**

1. In `publish_prepared`, the inline `status=='VERIFIED_PREREQUISITE' and validator_sha and source_checks for every saved q` test is replaced by `check_publication_annotation_prerequisite(id, job, qualifier)`. `validator_sha` is still assigned and is now a dead store, which is harmless.
2. The new top-level function `check_publication_annotation_prerequisite` is added.
3. Nothing else changed. The downstream guards are byte-for-byte the same AST:
   - frozen manifest pin and member count;
   - canonical member bytes and sha256;
   - canonical manifest;
   - `.gitattributes` byte policy;
   - missing/extra artifact set;
   - reviewed preimage;
   - `git hash-object` filter equality;
   - `publisher_argv`, attempt receipt, publisher exit, diff-tree path set, `verify_git_blobs`, supported finish.
4. Both drivers add only `--load-only` (pass) and `--continue` (`publish_prepared(ID)`).

**Gate semantics, read from the code.**

- **List checks.** The function refuses a wrong task id, and a list of qualifications that is not a list, is empty, or differs in length from `job['pairs']`.
- **Fresh check of every pair.** For each pair, in order, it recomputes `fresh` through the module-global `verify_packet_annotations`, which is the driver-patched owner verifier where a driver installs one. It requires `saved == fresh` exactly.
- **Scientific pairs** (no `owner_specs` entry) need all of:
  - `fresh.status == VERIFIED_PREREQUISITE`;
  - the current validator digest;
  - non-empty `source_checks`.
- **Owner pairs** are only the two keys `(GAUGE-AND-CHECKPOINT77-1003, …checkpoint77)` and `(SD194-COPIER-AND-QUEUE78-1003, …checkpoint78)`. Each needs all of:
  - the exact result filename;
  - `src == name+'-frozen-ready'`;
  - the exact fresh owner status;
  - the record's `status` and `accepted_prefix` (`1..61` / `1..118`);
  - for 78 only, `notices_handled == 26`.
- **No science credit for owners.** Owner history never acquires scientific status. The return value is unused by the caller.

**Replay on a disposable fixture.**

The fixture copied the publisher, both drivers, the validator, the four frozen folders, the pre-attempt files of the prepared folder, `reg_tracking.py` (adapter sha matches) and the two canonical evidence folders into the scratch directory. The board is a stub (`board_status` true, task ACTIVE/ASTRA with the four resources). The producer's own interceptor stops the run at the first `git hash-object`. Nothing touched the real board, the repository's git or the publisher.

- **After-publisher.** `control.py` reproduces the recorded result exactly: `actual-mixed-science-owner` BEFORE_GIT and four REFUSED_BEFORE_GIT, with identical diagnostics. Because the positive case reached the `git hash-object` stop, the unchanged downstream manifest/member/preimage guards also passed on the canonical copies.
- **Before-publisher, same inputs.** The positive case is refused with `missing/stale annotation prerequisite; no publication`. That is the exact diagnostic transcribed in `failure.json`, so the producer's positive control discriminates the defect. The `empty-required-qualifications` case is also refused by the old gate, so it is a negative control only, not a discriminator.

**Controls the producer did not run.** Producer coverage was thin in two places:

- The three non-empty negatives all refused at the single `saved != fresh` line.
- No producer case reached the typed owner branch (filename, folder, fresh status, record status and prefix, notices 26), and no producer case exercised the copier/queue78 job at all.

I ran 18 further cases on the fixture: 18/18 behaved as expected, with 4 accepted and 14 refused.

| case | result | diagnostic |
|---|---|---|
| saved qualifier unchanged | accepted | |
| qualifications in reversed order | refused | disagrees with current actual checker |
| wrong task id | refused | missing/empty/stale |
| one extra qualification | refused | missing/empty/stale |
| qualifications not a list | refused | missing/empty/stale |
| one science `agreement.instruction_records` changed 145→146 | refused | disagrees with current actual checker |
| publisher with no driver owner verifier | refused | `missing/incomplete source prerequisite map`: an owner capsule cannot pass as science |
| science pair relabelled as owner in both the fresh and saved results | refused | `scientific annotation prerequisite failed` |
| unknown owner kind `checkpoint79` | refused | `scientific annotation prerequisite failed` |
| owner result filename changed | refused | `invalid owner receipt qualification` |
| permissive owner verifier, record left intact | accepted | |
| permissive owner verifier, record `status` set to complete | refused | `owner transition record incomplete` |
| permissive owner verifier, `accepted_prefix` `1..62` | refused | `owner transition record incomplete` |
| 78: fresh qualifier (`VERIFIED_PREREQUISITE` + `OWNER_TRANSITION_RECEIPTS_NOT_SCIENTIFIC_ANNOTATION`) | accepted | |
| 78: owner relabelled scientific | refused | |
| 78: complete owner relabelled partial | refused | |
| 78: permissive owner verifier, `notices_handled` 26 | accepted | |
| 78: permissive owner verifier, `notices_handled` 25 | refused | `owner transition count/record mismatch` |

**Frozen inputs.** Both frozen folders of the published pair match their manifests in the frozen copy and the canonical copy: 65 members (`03ce4f39...`) and 25 members (`65a44f41...`), with `result-01.json` and `result-partial-01.json` listed as members. Their manifest digests equal the job pins.

## SWE2-AUDIT-SPEC limits and remarks (not defects)

- **No independent test for the typed owner checks.** The driver-installed owner verifiers already refuse a changed record status, prefix or notice count before the publisher's own typed checks run. Those checks are defence in depth and are reachable only through a permissive verifier, which is how I exercised them. The producer's controls do not test them independently.
- **The 78 job has not run end to end.** Its prepared folder does not exist yet, so its first real `publish_prepared` is still untested. My function-level replay covers only the prerequisite gate.
- **The original control is not repeatable as run.** It read the live board read-only and needs an ACTIVE, owned, unattempted package, so it cannot be rerun unchanged, as the README states. My replay used a stub board and fixture ownership, which is not a real-board observation.
- **Two hygiene items in the publisher, neither a defect.** `publisher-after.py` doubles its docstring blank lines on each rewrite, and `validator_sha` is now a dead store in `publish_prepared`.
- **Scope.** This is a procedure review of the publication path only. It gives no FF12 semantic credit. Queue history stays non-scientific, and the packet is not a committed-before-execution ORACLE seal.
