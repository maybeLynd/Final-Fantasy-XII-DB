# A23: independently checked served generation, release still incomplete

**Method:** read-only deployed HTTP plus offline generation and export verification.
No FF12 game/process control or dashboard write/restart. The selected capture
was `http://127.0.0.1:8765` at generation
`g20260929T184345Z-92fe9f`; this is a bounded observation, not an ongoing
claim about the moving `CURRENT` pointer.

`PLAN.md` states the competing hypotheses and controls. `capture.json`, its
terminal receipt and five `raw-http/*.body` files retain the original served
bytes. `verify-result.json`, its driver/terminal receipt, the retained
generation manifest, history and two view outputs establish that the served
progress/overview views agreed with that generation's declared outputs at the
observation. `source-identity.json` identifies current checkout files, not
the modules loaded in the server process. `historical-export-terminal.json`
records a real `generation.py verify-zip` success for the older
`g20260929T075521Z-fbf2f8` ZIP and sidecar. Its validity cannot bind that ZIP
to the captured newer served generation.

`check.py` is a read-only reducer over the frozen package. The actual
`checks-terminal.json` has one positive and three consequential refusals:
failed generation verifier, changed served view bytes, and a fictional A23
PASS. `run-checks.py` records exactly how those controlled copies were made;
its historical terminal run is distinct from independent acceptance. The
source drivers' external paths and dynamic generation are historical inputs;
do not rerun them as if they were the original capture.

`RESULT.md` and `verdict.json` carry the supported conclusion:
**A23 INCOMPLETE / NOT ACCEPTED**. FRONTIER has one named deployment request,
`ASTRA-REQ-FRONTIER-A23-RELEASE-EXPORT-IDENTITY`: choose a release candidate,
provide its matching portable export/sidecar and actual verifier receipt,
deployed source/process identity where accessible, and launcher/restart/
adoption evidence. SOL independently compares those receipts; inaccessible
host identity remains UNMEASURED. Producer checks and this package's exact
Git publication are not non-author acceptance of the whole migration.

Player version: the dashboard showed a checked snapshot; its recorded
download belongs to an older snapshot. The release is not proven complete.
