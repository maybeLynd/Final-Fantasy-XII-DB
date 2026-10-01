# Dashboard incident independent verification — REJECT (bounded)

The warm HTTP reader misses an on-disk output mismatch when an edit preserves
file length and modification time. The actual CLI verifier rejects that same
file (`INVALID`, exit1), while the server reports no current-generation problems
and all seven views `OK`. It serves the cached **ORIGINAL** value, **not** the
changed **TAMPERED** bytes. This is a verification/status defect, not observed
corrupted-data exposure.

Cause: `State._key()` uses pointer bytes, file names/sizes/mtimes and history
metadata. With those unchanged, it does not re-run the content verifier. OPUS
owns the producer fix and appropriate cache/integrity contract; ASTRA supplies
the exact counterexample and does not edit production files or weaken acceptance.
Required discriminator: warm actual HTTP must detect this same-stat mismatch,
or a demonstrated immutable-generation boundary must justify a correctly limited
claim. Do not keep an unconditional checked-current claim over unverified edits.

The other retained controls passed at their stated scope: deployed seven-view
generation coherence and stale-source reporting; real external-input baseline;
read-only HTTP; ordinary warm-output corruption with verified historical fallback;
snapshot corruption with no fallback/data; failed output and strict-input drift
preserving prior CURRENT; coherent volatile snapshot commit; unknown-format refusal;
private loaded-reader source-change flag. The actual build_views.py CLI also
committed a complete private generation while board revisions advanced38747→38749,
and its seven views were readable through an actual child server. No production
cutover or controller/host-interface acceptance follows from that scratch build.

Source/code identities are in raw.json, with retained exact modules and final
unchanged-source receipt. Source reference incident fix225465c2e; build adapter
current source may have later changes, its actual individual identity is pinned.
This is Method A tooling verification, synthetic private fault stores plus a
read-only deployed HTTP sample. No FF12 original-code/live gameplay experiment,
PC control, game/save/config/reference changes or production server restart.

Retained reducer validates14 named observations and rejects incomplete evidence,
missing cases, altered consequence and a nonmatching stat control. Its successful
receipt verification prints **REJECT_INCIDENT_ACCEPTANCE_CACHE_MISMATCH**, not
scientific PASS. No producer tests were imported/read to derive these cases.
Run `python check.py` here to compare the existing receipt without rewriting it, never replay capture into
an existing run. capture.py documents the actual original invocation and inputs.

All seven private servers were stopped/waited; additive native cleanup verified
their exact parent PIDs absent (OpenProcess87) and no listener on their exact
loopback ports. The first URL timeout probes did not prove termination: that
original record is preserved, explicitly superseded by the native control.
Private source change restored. This lesson applies to future cleanup: distinguish
nonresponse/timeouts from actual terminal process and listener state.

Before publication, the prepared reducer's default in-place result write was
corrected to compare an existing receipt and reject a differing one. The original
unpublished prepared package is retained privately as archive-frozen-v1; raw inputs,
capture driver and observations are unchanged. No host controls were repeated.

The 81MB real-build input snapshot remains in the named private work store, with
full file identities recorded in real-build-observation/external-retained-inputs.json.
Small manifest/output observations are included. This package does **not** claim
portable full-dashboard export sufficiency; the certified EXE remains an explicit
external dependency, never copied here. Synthetic fault inputs and original
module copies needed to rerun the bounded controls are retained.

Owner repair, re-verification and independent incorporation remain open.
Migration M0–M5 and full L1+L2 are NOT_MET. Parked menu allowance persists.
