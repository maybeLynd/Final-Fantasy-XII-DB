# ASTRA — retained reward-binding observations

**Result:** existing EXP-081 spans establish different reward-registry and unit
binding values at its load-complete popup and field samples. No fresh game run
was needed. This package finishes the already-claimed extraction; the owner has
incorporated the observations in commit `21f25545b`, reward contract §11.

Player version: the loading popup is an earlier stage than the playable field.
In that field, three enemies had nonzero references to reward data. This capture
does not show a kill, the amount awarded or whether the same data stays valid
through every spawn and unload.

## ASTRA — claim, method, state and controls

Question: do the existing full-unit/registry reads already distinguish absent
reward slots and NULL cached bindings from their initialized field values?
Competing explanations: the retained field contains missing slots/NULL enemy
bindings, or these words are nonzero; exact reward-header/row contents may still
be outside the captured extents. Consumers are FABLE's unit-definition account
and OPUS's experience/licence award contract. FABLE's UQ-97 authored-file census
is separate; it does not observe running registry lifetime.

Method **A**, offline reduction of retained **C** observations. `check.py`
performs file reads only. Budget is the original four samples, their full spans
and selected installer bytes; no new process, synthetic fixture or original-code
execution. Acceptance requires pinned raw identity, successful original read
controls, complete hashed extents, actual before/after reward-byte comparisons,
nonempty field units and matching historical exit/restoration. Any mismatch
invalidates this reduction; absence applies only to those retained extents.

Original process PID30640, image base `00120000`, executable SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
Selected save: The Stepping, `000:08:42`, backed-up `FFXII_000` 5,331 bytes,
SHA-256 `859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`.
The original [EXP-081](../../EXP-081-live-battleunit-bindings.md) documents ordinary
input, before/after screenshots, exact observer/module identity and setup.
There was no injected installer or observed combat action. Its successful
gesture is not a trace of input registration or command execution.

Raw inputs remain immutable in [battleunit-live-bindings](../battleunit-live-bindings/).
The known `LUAC_TAIL` bytes and rejected null read are original detection
controls. Its complete live `.text` matches the reference; that does not certify
all modules, heap state or imports. The new reducer verifies the prior manifest,
raw hashes, addresses and sizes, exact registry brackets and unit identity.
Unlike the old observer's `E60..E6F` stability tuple, it also compares the
actual `E70..E7F` reward words across both full pool reads. The captured registry
and enemy header are positive controls for the extent-coverage query.

## ASTRA — normalized observations

All addresses here belong to that historical process and are not portable defaults.

| Original state | Observed result, in both samples |
|---|---|
| Load-complete popup | Slots `02EBF148` and `02EBF140` are zero; no unit meets occupied + actor + stats selection |
| Field registry | Base slot value `67483C20`; per-level slot value `67483F50` |
| Kind1 unit slot4 | Base selector6, cached `67483D90`; per-level selector4, cached `67484050` |
| Kind1 unit slot5 | Base selector5, cached `67483D58`; per-level selector3, cached `67484018` |
| Kind1 unit slot7 | Both selectors0; cached `67483C40` / `67483F70` |
| Kind0 unit slot0 | Both reward words zero |

The enemy definition rows and their selectors were actually read. The registry
slot values and cached reward words were actually read. **Neither a reward
descriptor's 32-byte header nor even the cached reward row's first byte is in
any retained span.** Pointer differences alone cannot recover counts, encoded
bases, coefficients or lifetime. The null popup slots are not an observed NULL
installation/death path. The kind0 NULL fields are not proof of a crashing
consumer. Sequential equal brackets do not exclude an intermediate rebind.

## ASTRA — interpretation, propagation and verification

This supplies bounded initialized-state witnesses; it cannot establish the
installer-to-consumer sequence, universal table availability or reward effects.
The original EXP-075/076 positive-count, missing-descriptor, decoded-zero and
truncated-zero distinctions remain intact. No historical fixture is rerun.

Canonical propagation is **owner-published** for these observations:
`21f25545b`, [award contract](../../../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md)
§11 and §13. SECTION-03's [independent production reduction](../continuation-section03-reward-bindings/REVIEW.md)
agrees and retains formal peer acceptance as pending. This package does not
self-award that acceptance or any whole-system verdict. FABLE's current UQ-97
is answered for authored files; runtime storage/rebinding remains a distinct
question and is not reopened merely to count another experiment.

`check.py --mutations` rejects a changed after-read reward word even with a
recomputed digest and the old stability flag true, wrong registry address,
empty field samples and inconsistent restoration. A final added coverage
positive changes no normalized observations; the previously consumed checker
is retained as `check.before-coverage-positive.py`. SECTION-03's receipt pins
that earlier dependency. Its affected checker-replay acceptance needs explicit
review of this final version; native reward controls and original C evidence
are unchanged.

`observation.json`, `validation.txt` and `manifest.json` identify exact inputs,
result and final sources. The original cleanup records show process exit and
matching 26-file restoration, with the rewritten adapter-LUID config retained
before restoration. Those are historical receipts, not a new cleanup check.
No live session, save/config/reference change or PC control occurred here.
