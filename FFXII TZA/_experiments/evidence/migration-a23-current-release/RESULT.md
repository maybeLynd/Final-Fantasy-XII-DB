# A23 current release: a verified served generation, no matching release export

Independent ASTRA/SOL read-only A23 slice. The release record itself is
**DELIVERED, NOT ACCEPTED**. I did not adopt its historical PID/generation as
live identity. The exact current endpoint was `http://127.0.0.1:8765`.

On the bounded HTTP capture, `/api/status` before and after the root,
progress and overview GETs reported the same
`g20260929T184345Z-92fe9f` generation, `problems=[]` and
`reader_stale=false`; all five GETs returned HTTP 200. The progress view was
PARTIAL and overview OK, matching `/api/status`. A separate call earlier
showed `g20260929T183844Z-d50c67`; CURRENT later moved to
`g20260929T184850Z-14a883`. This is an updating service, so the bounded
capture is not a claim that one generation remains current forever.

The actual `generation.Store.open_generation` verifier returned no problems
for the captured generation, with its `history.jsonl` manifest hash. The
served progress and overview `view` objects exactly equalled their generation
output JSON; output hashes matched the manifest. The manifest's builder and
verifier SHA256 equalled the current checkout files at this observation.
`source-identity.json` binds server, builder, requirements and generation
source files to their current Git blobs and last path commits. This is
checkout identity. `reader_stale=false` checks server/verifier loaded-source
hashes against their files; it is not a PID, path or module attestation.
Targeted `Get-NetTCPConnection` returned `CimException Access denied`, so
loaded process identity remains UNMEASURED; no bypass was attempted.

The release record's historical
`g20260929T075521Z-fbf2f8.zip` still passes the current `generation.py
verify-zip` path: 33 members, SHA256
`595f86d6e856333a648d4707af66450b3cd695abe7f4acefc20cb1a0d17049b3`
matches its sidecar. It does **not** match the captured 18:43 served
generation; no matching ZIP was present in `dashboard-exports` at the check.
That historical validation cannot award a current A23 release.

**A23 verdict: INCOMPLETE / NOT ACCEPTED** at full scope. This package
supports a bounded served-generation/manifest/HTTP identity slice only.
It does not exercise the launcher, restart, loaded PID/module, current
portable export, complete dashboard UI, other A23 requirements or final
adoption. FRONTIER owns deployment: choose one current generation and export
it through the guarded release path, retain ZIP/sidecar and actual verifier
exit, bind its deployed source/PID if the host permits, and update the release
record. SOL can then independently compare the export to the served version.
If host process identity remains unavailable, mark that component
UNSUPPORTED/UNMEASURED rather than silently accepting it. No dashboard
server/controller/store or peer source was restarted or modified here.

Player version: the dashboard answered from a real checked data snapshot,
but the downloadable package on record belongs to an older snapshot. Its
current release still needs a matching package and deployment proof.
