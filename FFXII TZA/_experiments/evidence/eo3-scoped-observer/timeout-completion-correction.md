# ASTRA — incomplete timeout is not a matched request

During pre-live assembly, `capture_scoped.py` was challenged with one owned
event whose observer said CONTINUE, followed by a deadline. Cleanup, detach and
handle closure succeeded, but the outer result said MATCHED_PENDING_HEALTH.
`timeout-repro.initial.json` preserves the first reproducer. This is a synthetic
dispatch finding, with no new process access or FF12 behavior observed.

The classification condition had required nonempty hits and observations, but
did not require the callback's completed-request decision. An empty run was
INVALID; a partial nonempty run could be mislabeled. This is an instrument-result
defect even though `Recorder.finish()` independently rejects incomplete chains.
No runner may accept the old outer status as proof of an EO3 match.

`capture_scoped_v2.py` records completion only after the explicit
STOP_MATCHED_PENDING_HEALTH decision, successful resume, and successful event
continuation. An otherwise clean timeout is INCOMPLETE, including zero events.
Failed cleanup remains INVALID even when the match flag is true. All outcomes
still require the separate game-health and restoration checks for live use.

The original source remains unchanged because six native controls pin it.
Those controls requested explicit completion or abort at their first event;
none used CONTINUE followed by timeout as its successful observation. Their
source/API/context/effect/cleanup conclusions remain bounded and reviewable.
There has been no EO3 live semantic conclusion to retract. The old source is
historical evidence; v2 is the next deployment candidate.

The smallest regression uses the existing event fixture: zero events, one or
two partial events then timeout, immediate completion, partial then completion,
and completion with failed cleanup. It reproduces v1's false match and checks
v2's outcome. The successful normal control's API/dispatch call sequence remains
identical in this fixture. This is not a new native qualification of v2.

Independent review remains ASTRA-REVIEW-EO3-STOPPED-OBSERVER. Review the retained
failure and correction together with the native stop controls. No FF12 launch,
PC control, @runtime reservation, save/config/reference change or claim about
EXP127's unknown crash cause follows from this repair.
