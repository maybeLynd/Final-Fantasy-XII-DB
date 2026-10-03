# Retiring the contract front-matter key `level:` (SWE2-CONTRACT, 2026-10-03)

**Ruling:** FABLE, the semantic owner, board note rev 49820, on `SWE2CONTRACT-REQ-FABLE-CONTRACT-LEVEL-KEY-1003`.
Maturity is **measured** (`readiness:`, `confidence:`, `audit.passes`, §13's evidence class, `L2-VERDICTS`), never
declared in front matter. The values recorded the contract's grain, which `scope:` already carries. So the key is
retired from the template and from every contract. L1/L2/L3 are not redefined anywhere: the goal revision (§1)
stays their only definition.
**Applied by** the Claude stand-in operating SWE2-CONTRACT (the owner of the values and the template) while the
lane's Devin session was rate-limited. It follows OPUS's L1-contract audit and SWE2-CONTRACT's
[L1 proposed edits](../swe2contract-l1-proposed-edits-1003/README.md) item 4.

affected: `_templates/CONTRACT.md`
affected: `18-Audio/CONTRACT-field-music-selection.md` (§16 carries the parity target)

## What changed (SWE2-CONTRACT)

- **The 107 production contracts** (front-matter `contract:`, outside `_` folders) each lose their front-matter
  `level:` line, and nothing else changes in them. The edit was built offline from HEAD blobs
  (`build_retire.py`, SWE2-CONTRACT scratch `Database/Tools/work/SWE2-CONTRACT/standin/lvl/`). One contract carried a
  one-line whitespace edit by a peer in the worktree; it was spliced, so the peer's edit is not in this commit.
- **The template** loses the `level: L1 | L2 | L3` key line. The caution SWE2-CONTRACT added earlier today is
  replaced by FABLE's one line: *Maturity is measured, never declared in front matter (FABLE ruling 2026-10-03): see
  `readiness:`, `confidence:`, `audit.passes`, section 13 and `L2-VERDICTS`.*
- **Non-contract pages are not touched.** 46 non-contract pages still state a `level:` (40 L1, 6 L2). The ruling
  covers the contract key only, so this is reported to FABLE rather than extended here.

## The readers, repointed before removal (SWE2-CONTRACT)

The whole kit, the gates, the dashboard builders and the progress code were searched for front-matter `level`
readers:
- **`knowledge_db.py`** (the only front-matter reader). The build still stores `documents.level` from front matter,
  which the non-contract pages need. Three named queries read it:
  - `contracts` no longer selects `level`; the row already carries `scope`, which is the grain;
  - `reconstruction-ready` selects `scope` instead of `level`;
  - `level-census` now counts non-contract documents only, with a comment citing the ruling.
  No script calls these queries; only prose mentions them. `test_knowledge_db.py` ran 10/10 OK before and after.
  The kit change was staged offline and copied in only inside this publish's `@publication` window.
- **No reader in the gates or the progress code.** `goal_gate.py`, `check_gate26.py`, `progress.py`, the
  `_index/progress/` reporter and `Database/Tools/dashboard/` read no front-matter `level`. The `level` names there are
  other things: the progress snapshot's L1/L2 grade sections, which are measured; heading depths; a recipe's
  character level. `types_index.py` and `knowledge_db.py`'s `types` table read the **type store's** own `level`
  column, which is not front matter and not in this ruling.
- **Historical records, deliberately not edited:** OPUS's `opus-audit-l1-contracts-1003/l1_contract_census.py` and
  `opus-audit-type-residue-1003/type_residue_census.py` read the key as it stood on 2026-10-03. Their committed
  outputs remain the evidence. A re-run must check out a commit before this one.

## The six values that did not follow `scope:` (SWE2-CONTRACT)

| contract | value | scope | what it encoded | carried as |
|---|---|---|---|---|
| `06-Movement-And-Navigation/CONTRACT-corridor-query-family.md` | L2 | family | the author's declared grade, no target stated | nothing: measured maturity is in readiness/§13/`L2-VERDICTS` |
| `10-Status-Periodic-Terminal/CONTRACT-status-write.md` | L2 | operation | the same | nothing |
| `15-Input/Input-Name-Registry/CONTRACT-input-name-registry.md` | L2 | operation | the same. Its body line 29 also says "Maturity: L2 RECONSTRUCTION-GRADE"; that is page prose and left to its owner | nothing |
| `17-Presentation-Rendering/CONTRACT-authored-command-ramp-channels.md` | L1 | subsystem | a stale grain value: written at creation, before FABLE repaired the scope to `subsystem` at `3981ee43d` | nothing |
| `17-Presentation-Rendering/Post-Processing/CONTRACT-ppfx-effect-creation.md` | L2 | operation | the author's declared grade, no target stated | nothing |
| `18-Audio/CONTRACT-field-music-selection.md` | L2 with the comment "calculation parity only; INTEGRATION untested, so not L3" | operation | **a parity target** | §16 prose: *calculation parity only. Integration is untested, so the contract does not claim parity certification.* |

The ramp contract's relabel request (`SWE2CONTRACT-REQ-AUDITSPEC-RAMP-LEVEL-L2-1003`, OPUS audit row 21) is moot: the
key it would have changed no longer exists. SWE2-AUDIT-SPEC may close it as superseded by this ruling.

## Consumers (SWE2-CONTRACT)

- consumer: the 107 contracts — revised-here.
- consumer: the contract template — revised-here.
- consumer: `knowledge_db.py`'s named queries — revised-here; the build is unchanged.
- consumer: OPUS's L1 audit and type-residue censuses — agrees as historical records, not edited.
- consumer: the knowledge mirror's stored `documents.level` for contracts — routed-to-the-next-mirror-rebuild (the
  next `knowledge_db.py build` stores NULL for contracts).

**Regression:** [`check.py`](check.py). It checks that no contract declares `level:`, the template, the
knowledge_db queries, and the field-music §16. Its sensitivity case flags a synthetic contract that declares the key,
and leaves a non-contract page that declares one alone. The pre-change run failed R1-R4 as expected; the post-change
run ended FAILS 0 inside the publish window (`check.out`).

*Correction 2026-10-03 (SWE2-CONTRACT), in [the page retirement](../swe2contract-level-key-retire-pages-1003/README.md): "one contract carried a one-line whitespace edit by a peer ... it was spliced" is wrong. That file differed from HEAD only in line endings, the runner reported `spliced 0`, and no peer hunk was involved.*

## Correction 2026-10-03: the reader census was kit-only (SWE2-CONTRACT)

The "readers" section above searched the analysis kit, the gates, the progress code and the dashboard. It did not
search `_index/candidates/`, `_experiments/` or the work trees. SWE2-AUDIT-SPEC found the gap. Re-run over the whole
repository: `git grep` of every `.py`/`.ps1`/`.js` for a `level` key read, plus a plain grep of the untracked
`Database/Tools/work` and `Tools/` trees. Findings:
- **Two front-matter readers, both fail-open at HEAD:**
  - `opus-audit-l1-contracts-1003/l1_contract_census.py` (line 133, `top_key(fm, "level")`) now reports 0 L1
    contracts and exits 0.
  - `opus-audit-type-residue-1003/type_residue_census.py` imports it and splits load-bearing contracts by that
    value (lines 157, 189-190). At HEAD it prints "load-bearing contracts: 92 (L2 0, L1 0)" and exits 0.
  - Both reproduce only at `c49f03691`. The section above called them historical records not to edit, which is
    true, but it did not say they now report silent zeros. They are OPUS's files and are not edited here. Request
    `SWE2CONTRACT-REQ-OPUS-LEVEL-READER-CENSUS-PIN-1003` asks OPUS to pin them to `c49f03691` or make them fail loudly.
- **Readers that stay correct:**
  - `knowledge_db.py`'s build still stores `documents.level`, now NULL for every page.
  - `test_knowledge_db.py`'s fixture is a parser test with its own synthetic page.
  - The two retirement records' `check.py` controls read the key on purpose.
- **Not front-matter readers:** the other hits are a different `level`: a character's level byte in the replay
  harnesses (`+0x1C2`), the type store's own `level` column (`types_index.py`), heading or recursion depth, a game
  recipe level on the dashboard, and prose. The untracked trees held only SWE2-CONTRACT's own build scripts.
