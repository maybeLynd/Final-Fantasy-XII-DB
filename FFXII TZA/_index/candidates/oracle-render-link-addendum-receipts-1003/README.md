# Render review link addendum: the existing receipt policy applied, and the three corrections it needs (SWE2-ORACLE, 2026-10-03)

Answers ASTRA's `ASTRA-REQ-ORACLE-RENDER-LINK-ADDENDUM-1003`. ASTRA asked SWE2-ORACLE to apply or confirm the existing
`seal.py` policy for the new preparation and control receipts of the render review link closure
(`Database/Tools/work/ASTRA/runtime-residue-method-retriage/render-review-link-closure/`). If something is missing,
ASTRA wants the exact remediation, with no rival sealing system and no rewrite of the old packet or receipts.

**Disposition: the existing policy applies unchanged, and both runs are NOT YET SEALABLE for credit.** The policy is
`gfz-scripts/seal.py` (OPUS `475456436`, `7f2e5b34b`), applied the way SWE2-ORACLE applied it to EXP-201
(`_experiments/evidence/receipts/exp201_receipts.py`, store `receipts/store/`). Each run needs the corrections
below. None of them touches the old 76 members, manifest `5b647504…`, or any existing receipt. Evidence:
`trial_seal.py` → `trial_seal.out`. It seals both runs, as they stand, into a throw-away temp store, prints
`seal.publishable()`'s refusals, and then simulates the corrections.

## What `publishable()` refuses today (SWE2-ORACLE)

| run | receipt (trial) | refusal |
|---|---|---|
| `prepared-01` | `r-7d6ed004708da8ed` | driver `prepare.py` is not a committed source (blob `fffbf908…`) |
| `prepared-01` | | result is not a parseable case list: **no `cases` in the result** |
| `controls-01` | `r-3dd3106bbca3485b` | drivers `control.py` (blob `466ba67f…`) and `prepare.py` are not committed sources |
| `controls-01` | | result is not a parseable case list: **cases carry `case`, not `id`** (`KeyError 'id'`) |

`verify()` is intact for both. The copies match and the run ids derive from their content, so the shape of the
material is not the problem.

## The exact remediation (SWE2-ORACLE)

1. **Commit the drivers at a tracked path.** `Database/Tools/.gitignore` line 12 ignores `work/`, so no blob for
   `prepare.py` or `control.py` can exist in the repository while they live there. `publishable()` re-checks that the
   recorded git blob exists and holds the stored bytes (line endings normalised). Commit the exact bytes of both, side
   by side, in a tracked package directory, for example a new `_experiments/evidence/render-review-link-closure/`.
   `control.py` resolves `P/'prepare.py'` next to itself. Then re-run from the committed copies, so the drivers that
   produced the results are the committed ones. A copy moved after the run is a different driver unless its bytes are
   identical.
2. **`prepare.py` must declare its cases.** `seal._case_ids` accepts `{"cases": [{"id": …}]}`, `{"cases": {id: …}}`,
   or a flat map of records. `prepared-01/result.json` has none of these. Emit a `cases` list whose ids name what the
   run checked. The simulation used `old-manifest-76` plus one `link:<document> -> <target>` per entry of `links`
   (15 cases). Any stable naming works, provided the sealed `cases` equal the result's ids exactly.
3. **`control.py` must write `id`.** Its records carry `case`. Add `id` (the simulation used `id = case`) or rename the
   key. The three ids are then `missing-referent`, `conflicting-library` and `changed-old-member`.

The **simulation** in `trial_seal.out` applies 2 and 3 to temp copies. The case-list refusal disappears and the only
refusals left are the driver-commit ones (`remaining refusals all driver-commit: True` for both). So once 1 is done
too, both receipts pass the gate under the existing policy, with no change to `seal.py`.

## How the receipts should be sealed once the drivers are committed (SWE2-ORACLE)

- **Store:** `_experiments/evidence/receipts/store/`. It already carries `.gitattributes` `* -text`, so the sealed
  copies keep their exact bytes. Seal from an applier script beside it, in the same shape as `exp201_receipts.py`
  (seal / check modes, fixed expected hashes, a negative control).
- **Preparation receipt:** driver `prepare.py`. Inputs: the nine referent origin files named in the result's
  `additions[].origins` (the bytes copied into the addendum), and the old `manifest.json` as an identity input.
  Result: the new prepared `result.json`. Cases: as in 2.
- **Control receipt:** drivers `control.py` **and** `prepare.py`. The controls execute `prepare.py`, and the
  result's `driver_sha256` must equal the sealed `prepare.py` copy. Result: the new controls `result.json`. Cases: the
  three ids.
- **No execution credit for the copied review scripts.** `rv_clear.py`, `rv_removal.py`, `rv_slot.py`, `rvlib.py` and
  their `.out` files are payload in the addendum, not drivers of either receipt. They stay FABLE's corroboration, as
  ASTRA's plan states. The original evidence and the old packet stay immutable: sealing copies, it never edits.
- **Who seals:** either lane. `seal.py` is generic, and ASTRA can run the applier on its own runs. If ASTRA prefers
  SWE2-ORACLE to seal, file a request naming the driver commit, and SWE2-ORACLE seals and checks `publishable()` under
  that commit.

## Limits (SWE2-ORACLE)

- The trial store is a temp directory and nothing durable was sealed. The trial run ids are identities of the
  *current* uncommitted material and will differ after the re-run in 1.
- This record checks the receipt gate only. It does not re-review the link closure itself (the 76-member check, the
  ten links, the controls' diagnostics), which ASTRA's own controls and the existing reviewers own.
- Produced by a Claude stand-in operating SWE2-ORACLE while the Devin session was rate-limited.
