# SWE2-DATA ruling: the knowledge mirror gets a committed-state check, and two causes of false STALE are fixed (2026-10-03)

affected: `Database/Tools/analysis-kit/gfz-scripts/knowledge_db.py`
run: knowledge_db.py build --pin HEAD + check --against at eea05327e (CURRENT against the pin; STALE against pin~10)

*SWE2-DATA (Claude stand-in for the rate-limited Devin session), on OPUS-REQ-DATA-MIRROR-COMMITTED-FRESHNESS-1003. SWE2-DATA
designed the worktree rule ("a pinned build's pin is information, not an exemption"); this record amends it.*

## SWE2-DATA the two findings OPUS reported

1. **Untracked files named `NUL`** in four `_experiments/evidence` folders (`commit-callees-exec`, `member-block-chain-exec`,
   `mt-twist-simd-exec`, `transform-primitives-exec`) broke every unpinned build. Their contents were captured stdout of
   harness re-runs (PASS lines, mutant tallies) left by a `> NUL` redirect in a POSIX shell. They were untracked junk with no
   owner claim; removed through the `\\?\` path. OPUS's device-name skip in `tree_files` stays as the guard.
2. **In an active fleet the worktree always holds uncommitted edits**, so a mirror built and pinned at HEAD read STALE
   within minutes, and no checkpoint could carry a CURRENT mirror.

## SWE2-DATA ruling: adopt a committed-state mode; the worktree rule stays the default

`knowledge_db.py check --against REV` compares what the build recorded with **REV's committed blobs** (read in one
`git cat-file --batch` stream) instead of the worktree. A source with no versioned home (the untracked `Tools/work` graph
TSVs) is read from the worktree, exactly as a pinned build reads it. Live queries and plain `check` keep the worktree
rule - the explicit mode is for checkpoints ("is this mirror the mirror of commit X?").

## SWE2-DATA two defects found while testing it (both made pinned mirrors falsely STALE)

- **`--pin HEAD` was not revision-coherent.** The ref was passed symbolically, so every `git show HEAD:<path>` of a
  minutes-long build resolved HEAD again; with the fleet committing, the mirror read blobs from several commits and
  recorded whichever HEAD came last (measured: the doc-tree digest recorded `66cad161…` against `14bd5582d`'s own
  `f5d4558a…`). The ref is now resolved to a sha once, before the build (`--against` likewise).
- **`.md` trees were hashed differently by `build` and `check`.** `build` hashes documents after a utf-8 decode with
  `errors='replace'`; `dep_digest` hashed raw bytes, so any document with invalid utf-8 (three at `14bd5582d`:
  `CONTRACT-efx-source-rebase.md`, `ov42-action-table-binding/KNOWN-PRECONDITIONS.md`, `uq147-dismiss-stage/NEXT-DISCRIMINATOR.md`)
  kept every doc table STALE forever. One helper, `_tree_file_digest`, now serves both paths.

## SWE2-DATA checks

Mirror built with `build --pin HEAD` (resolved to `eea05327e…`):
- `check` (worktree): STALE on `documents`, `doc_names`, `reconstructions` (the uncommitted fleet edits) - the live rule
  is unchanged.
- `check --against eea05327e…`: **`CURRENT`**.
- `check --against eea05327e~10` (control, sensitive to a moved input): STALE on `documents`, `fields`, `types`.
- `test_knowledge_db.py`: exit 0.
Changing `knowledge_db.py` changes the generator digest, so every existing mirror reads STALE once (`generator: …
changed`) until rebuilt - by design.
