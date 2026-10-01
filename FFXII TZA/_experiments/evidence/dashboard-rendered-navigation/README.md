# Bounded rendered navigation, 2026-09-29

Question: does navigation in the deployed local dashboard produce the requested
view, or merely accept a tool input while stale/failed content persists?
Consumer: OPUS UI/deployment acceptance. This is host browser evidence, not FF12
live-game or isolated original-game execution.

Existing HTTP shell evidence c466fc47 did not establish rendered navigation.
Controls: observed initial My Progress heading and completion warnings; currently
visible buttons; changed destination headings/content; owned-tab close/inventory.
Budget: at most ten input actions, no server restart/build or other tabs. Four
attempts occurred, two refused. No unchanged failed input was repeated.

Observed: Progress baseline, then Overview heading and its source/limits table;
then Activity heading, live-feed attribution and the actual named ASTRA task.
The immediate Activity AX receipt is intermediate, not proof of replacement;
the later DOM and screenshot establish the destination. Status changed STALE to
PARTIAL as a new generation appeared. The refused return click establishes no
return to Progress. Final DOM remains Activity. Raw captures remain immutable.

Failures: first click used index12 from an earlier emitted tree after a fresh
non-emitted observation had changed the button IDs to356 etc. This was a control
procedure error, not evidence the UI broke. Second click used the observed exact
name My Progress STALE, but polling/generation changes replaced it with PARTIAL
before dispatch; zero matches. The original failure records are retained.

Reusable procedure correction: after a capture/observation, derive targets from
that returned state; never reuse earlier AX IDs. For polling status-labelled
buttons, use the observed stable label with an anchored role-name expression
(e.g. /^My Progress(?: |$)/) and require one visible match before dispatch, then
verify the destination heading. That proposed targeting correction has NOT been
executed here. Do not rerun sufficient Overview/Activity observations merely to
make the incomplete return green. No universal input registration claim follows.

Identity: identity.json pins current source/Git/Python and later HTTP raw hashes;
server-source.py is the actual copied preimage. PAGE equals the later served HTML.
This supports shell byte identity only, not loaded Python process/module/dependency
identity. Browser tool reports IAB1/tab2; no browser build identity was exposed.
HTTP was obtained after the browser closed and is not atomic with UI captures.
Control-log timestamps were recorded after the ordered captures; they are not
precise input execution timings. UI generation/data changed during observation.
The Activity DOM names generation130427; its subsequent screenshot names131122.
They establish separate ordered presentation observations, not a single atomic state.
Screenshot byte signatures are JPEG although the capture names ended .png. The initial
reducer rejected its own PNG assumption (source/failure retained); the actual reducer
now checks JPEG framing. The readable .jpg deliverable is a byte-identical alias,
not edited/re-captured evidence. Future captures must derive suffix from actual bytes.

Cleanup: close returned successfully and browser inventory was empty. No FF12,
native desktop input, own server, save/config/reference write or runtime hook was
started. No user tab was touched. The screenshot/DOM prove presentation and rendered
content; no independent correctness award for totals, taxonomy, activity attribution,
real scheduling, all views, A17/M3 or full database completion. Required non-author
evidence acceptance and OPUS canonical consumption remain separate.

check.py is a retained-evidence reducer, not a browser replay. Missing cleanup,
changed source, missing destination or failed-input receipts cannot pass. External
review/checks are not our additional executions. Full L1+L2 goal remains ACTIVE.
