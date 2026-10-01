# Derived-data freshness policy

**Canonical policy, established 2026-09-26 (SWE2-FRONTIER) and binding on every lane.**

The knowledge base's derived artifacts — `_index/knowledge.sqlite`,
`Tools/work/knowledge/knowledge.sqlite`, dashboards and summaries generated from them — are
**dated snapshots of their inputs**, not live views. The permanent rule:

> **A derived snapshot may be old. It must never present itself as current.**

`integrity_check=ok`, a file timestamp, and "built from HEAD" are none of them freshness
evidence. The only admissible answer to "is this current?" is a re-computation of the
inputs the snapshot recorded.

## What is recorded

Every build writes `provenance` (schema 4+): one row per (table, dependency) carrying

- `source` — the dependency label (`file:<relpath>` or `tree:<reldir>;<suffix>`);
- `source_sha256` — the dependency's **content fingerprint**. For trees this is a manifest
  digest over sorted relpath + per-file hash, so **added and deleted files count as much as
  edits**, and uncommitted edits count the same as committed ones. Hashes are
  CRLF/LF-normalised so checkout style is never a false stale report;
- `git_blob` / `pinned_commit` — the versioned identity when the source has one;
- `generator_sha256` — the digest of the module set + schema version that produced the
  rows. A parser change stales **every** table, because every row is downstream of it;
- `output_sha256` — the digest of the table's own rows, so a hand-edited database is
  distinguishable from what the generator wrote;
- `rows`, `built_at`, `schema_version`.

A table that is computed **through** another — `citations` resolving through
`functions.tsv`, a `JOIN` or the `cited` view — records every input it uses. A joined view
depends on every table it reads.

## What readers must do

- **Normal (CURRENT) reads** check the dependencies the query touches first
  (`knowledge_db.py` does this for `query`/`sql`/`info`; `charter_grade_audit`,
  `readiness_rank` and `tools_provenance` call `knowledge_db.freshness_report`). A stale
  dependency produces an explicit `STALE` report naming the moved inputs — never
  apparently-current rows, and especially never an apparently-current **absence**
  conclusion ("no writers", "no citations").
- **Rebuild** is `knowledge_db.py build` (or `query --refresh`). Builds go through a
  staging file: inputs are fingerprinted before and after, and if anything moved mid-build
  the staged result is discarded and the last usable index is kept. Data and provenance
  publish together, atomically.
- **Explicit snapshot reads** (`query --snapshot`) are legal and labelled: the output
  carries `built_at`, the pin or `worktree` marker, and the stale list. Labelled history
  stays labelled history.
- **Publishing** prints the mirror's freshness at the checkpoint (`publish_paths.sh`) as a
  warning. It does not block — raw-source research must never wait on a derived table —
  but a stale report beside a publish means the numbers in the commit message need a
  rebuild first.

## Ownership and closure

- **SWE2-DATA** is accountable for mirror/query/dashboard freshness — keeping the
  canonical mirror rebuilt and honest — and for the type/field stores it generates.
- The query-side guarantees already in place are permanent controls, not one-off fixes:
  `writers-of-field` includes `w` **and** `rw` kinds (1,740 RMW writers were invisible to
  `w`-only queries); field `size` parses authored hex (`0x18`); blank field rows are
  skipped; instruction read/write direction comes from the decoder, not the mnemonic's
  name. Do not reopen these without evidence.
- A finding closes when its canonical consumers are updated and its safeguard exercised,
  with an independent reviewer's name on the acceptance — not when the fix is routed,
  rebuilt once, or mentioned in a handoff.

## Team operative headers — TEAM-CURRENT (SWE2-FRONTIER, 2026-09-26)

Lane inbox operative headers are a second derived view: they present an agent's
selection-relevant queue and used to be maintained by hand — which is how a stale
header silently replayed completed work. They are now generated blocks:

    <!-- TEAM-CURRENT:begin agent=<ID> board_rev=<n> epoch=<e> queue_sha=<16 hex> -->
    ... operative header text generated from live board state ...
    <!-- TEAM-CURRENT:end -->

- The **fingerprint** (`queue_sha`) covers only selection-relevant state: the agent's
  ACTIVE and BLOCKED tasks, tasks addressed to the agent in READY, the unassigned
  READY pool, and resources the agent holds. A peer's unrelated op changes
  `board_rev` but not the fingerprint.
- **`team.py current --check --file <inbox>`** verdicts:
  `CURRENT` — block matches live board; `MOVED` — board advanced, queue unchanged
  (usable); `STALE-QUEUE` — selection-relevant state changed (non-authoritative);
  `STALE-LABELLED` — inputs moved mid-generation, honestly labelled;
  `UNKNOWN-AGENT` — the embedded agent id is not a board identity.
- **Refresh** is `team.py current --agent <ID> --write --file <inbox>`; it replaces
  only the block matching that agent. If the board moves during generation the block
  is written with a `stale-inputs` label rather than presented as current.
- **`publish_paths.sh`** refreshes the block automatically for any named markdown
  file that contains a `TEAM-CURRENT` marker before staging.
- Authored research notes and dated history outside the block are untouched.
