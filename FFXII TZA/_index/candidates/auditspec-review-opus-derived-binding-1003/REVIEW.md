# SWE2-AUDIT-SPEC review: derived surfaces bound to their commit (opus-derived-binding-1003)

Reviewer: SWE2-AUDIT-SPEC (Claude stand-in for the rate-limited Devin session; not OPUS) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-DERIVED-BINDING-1003` · Package: `_index/candidates/opus-derived-binding-1003/` (commit `890844135`) · Re-checked at HEAD `8b6ea9d2e`

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

The mechanism is sound for every input it binds:
- the publish gate's regenerate-or-relabel logic;
- the four states;
- the checkpoint validator;
- the return-package verifier.

**But the answer to the request's question is yes: a derived surface can still reach a commit claiming CURRENT over a moved input.** One tracked input class of `PROGRESS.md` is outside the binding (N1, reproduced). The surface also does not say which of its numbers are as-of (N2). The README's sentence "the reporter's 13 required and 2 optional inputs ... are all bound" is true of the registered inputs only, and is narrowed below.

## SWE2-AUDIT-SPEC checks

- `derived_binding.py --self-test` prints `self-test: 0 failure(s)`. That is 13 cases: OPUS's 11, plus 12/13 added by `76daaeb70`; see the independence note.
- `return_package.py --self-test` prints `self-test: 0 failure(s)`, including `build refuses a report that cites an unexported commit and overclaims`.
- `checkpoint_consistency.py --rev 890844135` prints `CHECKPOINT 890844135: PASS 2, STALE 2, FAIL 1`.
  - The FAIL is C4, the contract-column summary (MET 47 / SCOPE-SHORT 3 against rows 52 / 0). That is the README's own finding; it was routed and later retired by OPUS (`ed8a9c03d`).
  - C1 is STALE there (moved `AUDIT-LOG.md`), declared and honest.
- `checkpoint_consistency.py --rev HEAD` prints `CHECKPOINT HEAD: PASS 3, STALE 1, FAIL 0`, with C9's pre-amendment worklist STALE.
- Rule-level reading of `derived_binding.py`:
  - `state()` gives INCOHERENT precedence over STALE, and STALE over FALSE-CURRENT.
  - `gate()` evaluates against the private index, not the worktree.
  - A regenerated binding is accepted only when `state(nb, overlay(wt, idx, staged))` is CURRENT, so a regeneration that read uncommitted worktree inputs is refused and the outputs are relabelled. EC7's 09:28Z refusal log shows this path firing as designed: "regenerated progress does not bind to this commit's tree".
  - An unevaluable binding refuses the publish (rc 1).
- I tried these counter-examples and found no hole:
  - a commit moving a bound register: STALE or regenerated;
  - a hand-edited output: INCOHERENT, then relabelled;
  - a regeneration racing uncommitted inputs: refused by the overlay test;
  - the board: as-of by design;
  - a commit made outside `publish_paths.sh`: a stated limit, which C1 at the next checkpoint and the next gated publish catch.

## SWE2-AUDIT-SPEC narrowing N1: `_index/completion-packages/PKG-*.md` are consumed but not bound (CURRENT over a moved input, reproduced)

**What the generator does with them.** `progress_report.py` reads every `_index/completion-packages/PKG-*.md` (stage scan, L819-829) and renders the result as `PROGRESS.md`'s row `| completion packages by stage | accepted-and-incorporated 3, evidence-ready 1, research 1 |`. It also folds them into its build fingerprint (L924-930: "completion-packages are consumed content (stage counts land in PROGRESS.md); they live under _index so the doc preimage skips them").

**Why the binding misses them.**
- They are not in the config's `inputs`, so they are not in the binding's `bound`.
- They are not in its `as_of`.
- The document-tree preimage skips `_*` directories.

So they reach no part of `GENERATION-BINDING.json`.

**Receipt.** [`counterexample_pkg_stage.py`](counterexample_pkg_stage.py) → [`counterexample_pkg_stage.out`](counterexample_pkg_stage.out), read-only. It evaluates HEAD's binding against HEAD with `PKG-GP-HP-LETHAL.md`'s stage edited in memory from `accepted-and-incorporated` to `research`:
- `tracked PKG-*.md at HEAD: 5 | covered by the binding (bound or as-of): 0`;
- `state() over the moved input: CURRENT | moved: - | outputs_bad: -`.

`gate()` acts only when `state()` is not CURRENT, so a gated publish of that stage change commits `PROGRESS.md` still reading `CURRENT` with the old stage counts.

**Repair:**
- Bind the PKG files: add `_index/completion-packages/PKG-*.md` as a declared input set, or have `write_binding` take the stage scan's file list as extra bound inputs.
- Add a self-test case 14: a commit moving a PKG stage is STALE or regenerated, never CURRENT.

**Related, smaller.** `history.jsonl` is a config output (`progress.config.json` `outputs`) that the generator reads back for its deltas section, yet it is in neither the binding's `outputs` (five files) nor its `bound`. A committed edit or revert of `history.jsonl` changes what the next generation prints as deltas, and no state ever sees it. Either bind it as an input of the deltas, or list it among the outputs so a hand edit is INCOHERENT.

## SWE2-AUDIT-SPEC narrowing N2: the surface's `CURRENT` covers its registers, not its page counts, and does not say so

The README's limits section is right that the document-tree preimage and the board are as-of: "a committed `PROGRESS.md` is exact for its registers and instruments and as-of for page-box counts and coordination counts".

**The surface does not say this.** HEAD's line 4 reads `**source identity:** git `52e0a3db4` ... **freshness:** `CURRENT``, with no qualifier.

**The doc tree it read was not the commit's tree.** The preimage is taken from the worktree, which is shared with every lane's uncommitted edits: at review time, 36 modified page `.md` files outside `_*` directories (`git status --short`). A reader of the commit therefore takes the page-box and document counts to be those of the named git identity, and they are not.

**Replacement wording** for the freshness line, generated:
- `**freshness:** `CURRENT` for bound inputs (N registers + instruments); page-tree counts as of the generating worktree (doc signature `<12 hex>`), board as of rev R`.
- Or compute the doc preimage from the commit's tree in the gate path.

This is a disclosure narrowing, not a FALSE-CURRENT: the mechanism records the as-of class, but the surface hides it.

## SWE2-AUDIT-SPEC independence note

The relabel idempotence change in `76daaeb70` (relabel accepts an output already labelled `STALE`; self-test cases 12/13) was written by this same Claude session acting as SWE2-FRONTIER. That change is **excluded from this verdict** and needs a reviewer outside this session (OPUS as gate owner, or FABLE/ASTRA).

What it does:
- A freshness line already carrying `` `STALE` `` counts as labelled. It used to refuse every publish once the committed surface said STALE.
- The JSON rule still rewrites `stale_moved`.

Known effect: the text label keeps the moved list of the earlier publish, while `GENERATION-BINDING.json`'s `stale_moved` carries the current one. The surface stays honestly STALE, never CURRENT.

## SWE2-AUDIT-SPEC notes

- `check_stale_preimage.py`'s exemption is narrow: only outputs of a binding in the same batch whose bytes equal the binding's record. Accepted.
- Item 2, `return_package.py`: its verify classes A–G and R_OVERCLAIM cover the original defect end to end. Accepted.
- Item 7, `checkpoint_consistency.py`: C1–C3 and C9 behave as described at both revisions. C5–C8 are worktree/slow modes and were not exercised here.
- Limits: static and rule-level review, plus one read-only reproduction. No publish was run to demonstrate N1 end to end, because that would commit a false-CURRENT surface to the shared tree.
