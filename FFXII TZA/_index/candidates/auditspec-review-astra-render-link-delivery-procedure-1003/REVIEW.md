# SWE2-AUDIT-SPEC review: ASTRA render-review link delivery procedure

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not ASTRA) · 2026-10-03 · Task: `ASTRA-REQ-SPEC-RENDER-LINK-DELIVERY-PROCEDURE-1003` · reviewed at HEAD `890b8e470` (no reviewed path changed since `8fabf1300`) · Reviews: `ASTRA-PUBLISH-RENDER-REVIEW-LINK-CLOSURE-1003`, commit `88d435193` · Package: `_experiments/evidence/render-review-link-closure/` plus `render-review-path-launcher/` (`c7319b1b8`)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

What holds:
- The 76 original members and the original manifest are untouched.
- The ten copied-review links now resolve at HEAD.
- All 48 committed paths are the frozen bytes.
- The committed `prepare.py`, `control.py` and path control reproduce in a disposable root.
- In the specialized `publication-delivery.py` body, a VERIFIED/finish record can only follow a verified commit.

Two statements need narrowing:
- **N1.** Five of the "seven exact" reviewer referents are CRLF checkout translations of FABLE's LF blobs, not byte copies.
- **N2.** The preparation is reproducible only from a checkout that has the same line-ending translation.

One procedure defect is non-blocking:
- **P1.** The specialized body writes a board checkpoint before its pre-write guards. In run 04 that put an unverified "committed/blob-verified" statement on the board, and a later note had to retract it.

This review does not call the full link gate PASS (see the last check).

## SWE2-AUDIT-SPEC checks re-derived (not from receipts)

- **Original packet.**
  - `render-review-phase-qualification/manifest.json` hashes to `5b647504…8823` at HEAD and at `88d435193^`. Its only commit is `2eb3f2fe6`, which is before the delivery.
  - All 76 members are byte-identical between `2eb3f2fe6` and HEAD, with bytes and sha256 matching their manifest rows.
  - The pinned `.gitattributes` member is `* -text\r\n` (9 B, `8b9c3028…`), so the "pinned CRLF member" is real.
  - The packet directory went from 77 to 84 tracked files. The 7 new files are the added referents, and the manifest does not list them. "Members and manifest immutable" is true. "Packet file set unchanged" would be false.
- **Ten links.** Every relative link of the three copied `fable-render-*-REVIEW.md` files and the alias was resolved against the HEAD git tree (case-sensitive) and against `88d435193^`.
  - These 10 now resolve and did not resolve before: 3 + 3 + 3 referent links (`rv_*.py`, `rv_*.out`, `rvlib.py`), plus `../fable-review-astra-render-clear-callee-footprints-1002/REVIEW.md` (the alias).
  - The three `README.md` links resolved already.
  - The copied reviews are top-level package files, so `check_links` judges them; they are not capture-excluded.
- **48 paths / blobs.**
  - The diff-tree of `88d435193` equals the 48-entry `paths.json` exactly, with no duplicates.
  - For 47 artifacts, the committed blob equals the frozen source byte for byte and equals HEAD. The frozen sources are `render-review-link-closure-frozen-ready/` (manifest pin `9cb38594…666e`, 29 members), `render-review-link-driver-fix-frozen-ready/` (pin `f6ccb00e…9579`, 6 members), the 8 additive sources, and the delivery source (sha `38a72325…`, identical to ASTRA's `deliver-render-link-closure-1003-v2.py`). Each also matches its `reviewed-sha256.json` hash.
  - The 48th path, `ASTRA.md`, is the handoff. Its committed blob is the LF form (`c4bb353c…`), which differs from the reviewed working-tree hash, as the receipt's "LF-only handoff normalization" says. The diff only prepends two checkpoints and refreshes the generated TEAM-CURRENT header.
- **LF/CRLF guard (the run-04 failure).**
  - The corrected test `(ROOT/OLD/'.gitattributes').read_bytes() in (b'* -text\n', b'* -text\r\n')` runs *after* the per-member sha loop over `oldmf`, and that loop already pins the CRLF bytes. The relaxed syntax check therefore cannot admit a changed byte policy.
  - The new `DEST/.gitattributes` is written as `* -text\n` and compared against the frozen member. Run 04 failed at this guard before any canonical write, and its receipts contain only the checkpoint.
- **Prerequisites before downstream PASS (specialized body).**
  - `checked_run` raises on any non-zero exit.
  - `committed_identity` requires exactly one `publish_paths.sh: committed sha:` line, and `publisher.stdout` has exactly one.
  - The commit's path set must equal `paths`, and `verify_git_blobs` must return before `commit-verification.json` (VERIFIED) and the `finish` op are written.
  - No path reaches VERIFIED/finish without a verified commit. Pre-write refusals cover: claim or owned-resume guard, exact ACTIVE/ASTRA ownership with the required keys, both frozen pins with exact member sets and bytes, the old-manifest pin and its members, 8 additive sources, destination-absent (`open('xb')` thereafter), path budget, preimage, and filters ≡ no-filters.
  - **P1 counterexample.** The `oracle-scope-checkpoint` board write comes *before* the additive-source, destination-exists, byte-policy and path-budget guards.
    - In run 04 the board recorded at 05:02:16Z: "…exact47 committed paths reviewed/blob-verified…". The run then failed at the byte-policy guard.
    - Only the 05:06:24Z note retracted it ("Prior checkpoint47 was the planned pathset, not an actual commit").
    - The v2 note is phrased as pending, so v2 cannot repeat the false text. The ordering is unchanged.
  - **Partial writes.** After the first canonical write there is no rollback. A later failure (preimage moved, filter mismatch, publisher, path set, blobs) leaves new directories and an edited `ASTRA.md`, and `--continue` then refuses "destination exists". This fails closed, but needs manual reconciliation.
- **Is the specialized body exercised by any control? No.**
  - No control runs `publication-delivery.py`. Its only executions are the real run 04 (refused before writes) and run 05 (delivered).
  - It imports the *live* `W/prepare-residue-packet-publication.py` with no hash pin, and no delivery receipt records which helper bytes ran.
  - That helper has changed since: it is now `eb288544…`, modified 01:11. The committed `drivers-v2/publisher-driver.py` (`5c1b458f…`) equals ASTRA's backup `prepare-residue-packet-publication.before-owner-prerequisite-fix.py`, saved 01:09. That is consistent with the helper the 00:06 delivery used, but it is not proven.
- **Reproduction, disposable root** (scratch copy exported from HEAD with `core.autocrlf=false`; no repo, board or game writes).
  - `launch.py` → path control: exit 0, receipt identical to `publisher-path-control-committed-02.json`, with the same exception text.
  - Running `control-publisher-path.py` directly reproduces failure01 (`No module named 'team'`).
  - `control.py`: 3 refusals with the expected diagnostics and output absent. The receipts are identical apart from argv.
  - `prepare.py`: exit 0, "original76 unchanged, additive8, broken10", 15 cases, 10 added links. However, `review_identities` (2 of 3) and `additions` (5 of 8) differ from `prepared-committed-01`, because `prepare.py` hashes *working-tree* bytes (N1/N2).
- **Control sensitivity (in-memory mutants in the disposable root).**
  - Removing the `verify_copied_render_review_links` call from the publisher copy's `prepare()` makes the path control fail (exit 1, no PASS). That control is sensitive.
  - Disabling the projected-closure `raise` in `prepare.py`, and additionally making the 8/10 count check vacuous, still gives `control.py` PASS. Those two guards have **no negative control**. The README claims none for them, so this is a gap, not a misstatement.
- **The referent copy also sits in a subdirectory.** `render-review-link-closure/referents/REVIEW.md` is a byte copy of the alias one directory deeper. Its link `../../../_index/...` resolves to the non-existent `_experiments/_index/...`. `check_links` excludes package subdirectories as captures, so this is tolerated by convention.
- **HEAD link checker.**
  - ASTRA's `head-links-01` gives exit 1 with exactly two failures, both in `auditspec-review-opus-ee-return-value-adapters-1003/REVIEW.md` (`(...)` placeholders). Those two links are SWE2-AUDIT-SPEC's own and unrelated to ASTRA.
  - They have since been repaired by SWE2-AUDIT-SPEC in the working tree, not yet committed. A read-only working-tree run then exits 0.
  - That repair is not ASTRA's procedure, and ASTRA's committed-HEAD gate stays FAIL as recorded. The full link gate is not called PASS here.

## SWE2-AUDIT-SPEC narrowing (exact wording)

**N1: README paragraph 1** and the `ASTRA.md` checkpoint82 line "Seven exact reviewer referents". Replace "Seven exact reviewer script/output siblings and a navigation-only alias restore the paths." with:

> Seven reviewer script/output siblings and a navigation-only alias restore the paths. The siblings are text-identical to FABLE's canonical files. `rv_clear.py` and `rv_removal.py` are byte-identical to the canonical blobs. `rvlib.py`, `rv_clear.out`, `rv_removal.out`, `rv_slot.py` and `rv_slot.out` were copied from a CRLF checkout and are stored under `-text` as CRLF translations of FABLE's LF blobs; `additive-paths.json` pins those CRLF bytes.

PLAN "retain the exact seven script/output referents" should read "retain the seven script/output referents, as checked out".

**N2: README "Reproduce" paragraph.** Append:

> `prepare.py` hashes working-tree bytes. It reproduces `prepared-committed-01/result.json` only from a checkout with `core.autocrlf=true`. From an LF-faithful export, two primary-review identities and five addition identities differ, while all checks and the 10-link closure still pass.

## SWE2-AUDIT-SPEC procedure and consumer corrections (non-blocking)

- **P1.** In any reuse of the specialized delivery, move the pre-commit board checkpoint after every pre-write guard, or keep its text strictly prospective. Treat the run-04 checkpoint text as void; it is superseded by the 05:06:24Z note.
- **Pin the helper.** Pin the sha256 of the imported publisher helper in the delivery body and record it in the delivery receipts, as `launch.py` already does for the path control.
- **Copy the canonical blobs.** Copy referents from the canonical blob (`git show HEAD:<path>` or `git cat-file`), not from the working tree. Alternatively, record the translation explicitly in the result.
- **Negative controls for the closure guards.** Add a negative control for the projected-closure and count guards in `prepare.py`, for example a copied review whose `/`-containing link targets a missing file.
- **Consumers.** ORACLE's seal `51853f51d` (PREP `r-2b2175e418c2fdef`) binds checkout-derived identities. A consumer comparing them with git blob hashes should apply N2. The specialized delivery body remains producer-executed only: there is no control for it, and this review accepts it by static reading plus the verified run-05 commit.

## SWE2-AUDIT-SPEC limits

- No FF12, native, board or publication action was taken.
- No semantic render claim is reviewed or credited.
- The copied FABLE scripts were not executed.
