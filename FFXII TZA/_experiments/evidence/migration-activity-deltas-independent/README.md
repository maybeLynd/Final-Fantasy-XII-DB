# Activity review: writer attribution REJECT

Original `activity.py` at `8ddc8c7e8e91be7019229c3df8084f53430804bb` infers a lane's
recent board write from a task's `agent` / `assigned_to` / `requester` and `updated_at`.
A timestamp says when the row changed, not who changed it. The issuing identity already
exists in the supported board operation history. The function does not use that
provenance or the lane's actual last checkpoint for its recent-write fallback.

Six bounded Method A controls run original repository Python code. `team.apply` creates
an OPUS claim two hours old, then FABLE adds a fresh READY review assigned to OPUS.
History has only FABLE within the last hour. Original `activity.compute` calls OPUS
`recent`, classifies the old claim `working` and puts OPUS in Combat's coloured lanes,
both without a feed and with an explicit UNKNOWN Claude classification. The queued
review itself remains `waiting`; the defect is false credit for the separate old claim.
Conversely, an actual fresh OPUS `note` operation updates board history/agent checkpoint
but no task timestamp. Original compute leaves OPUS UNKNOWN/claimed. An unchanged old
claim without feed stays UNKNOWN/claimed; fresh busy and free poll controls produce
active/working and idle/claimed respectively. No need to repeat these settled cases.

The fixture clock is an explicit replacement of `team.now` solely at the in-memory API
boundary. Each fixture is validated by the original schema. No `team.transaction`,
production journal, mutex, deployed writer, game instructions or live FF12 ran. This
proves the original Python classifier's effect on these prepared boards, not a whole
host/session result. OPUS owns correction of the attribution and affected specification.
Acceptance discriminator: a foreign assignment must not credit the recipient's write;
a real lane note must count under the agreed one-hour write rule; busy/free controls
must remain correct. Do not weaken the rule to match the implementation silently.

`activity-01` is an INVALID preparation attempt: the claim lacked the original API's
required note and failed before any of the six cases. Exact original driver/source and
tool failure receipt are retained. No semantic conclusion depends on that attempt.
The changed `activity-02` supplies the precondition and records early setup exceptions
as incomplete raw evidence. Reusable lesson: read the actual supported operation API;
assert required note and terminal status, and never interpret absent raw as valid empty
output. Both runs stay distinct. Actual tool return status receipts are labelled as
such, not invented subprocess transcripts or extra executions.

Read-only actual HTTP observation captured activity/status/live/page across unchanged
TEAM rev39408 and generation `g20260929T090807Z-917468`. Controller before/after bytes
agree; status reports reader_stale=false. The one OK timer sample is last_run+1800.
Served raw page bytes exactly match the retained current server PAGE literal, and
retained current disk activity source equals the tested 8dd source. This does not prove
which activity module the serving process loaded: reader_stale monitors server and
generation, not every imported module. Runtime PID/build supplied in the old request
is not reused as current proof. No atomic snapshot, rendered UI/countdown reload,
all timer branches or delta calculation acceptance is awarded; these remain untested
by this package. No false current deployed colour is claimed from the fixture alone.

Raw board bracket bytes are gzip-compressed with deterministic header, hashes over
original uncompressed bytes, complete source/receipt identity and no store mutation.
`check.py` is read-only by default and verifies nonempty required cases, actual terminal
status, writer-history provenance, source/input hashes, original effects, preserved
failure, HTTP bracket/byte identities and the one timer arithmetic observation. Two
actual altered-receipt CLI controls refuse incomplete-good-cases and nonzero-good-results.
These are producer checker controls, not independent evidence acceptance.

Required non-author evidence review and OPUS cause/consumer repair remain separate.
Full M0–M5 and FF12 L1+L2 are NOT_MET; deltas/rendered UI/loaded module identity remain
explicitly open. No browser/PC/game control, restart, saves/config/reference/controller/
production-store edits or peer-owned producer edits. The parked menu budget persists.
