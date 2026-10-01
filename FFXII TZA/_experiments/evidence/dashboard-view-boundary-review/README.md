# Independent review: two rejected boundaries, retained valid controls

OPUS source eae0ed3c7, review OPUS-REQ-ASTRA-VERIFY-DASHBOARD-VIEWS-0929-R.
Verdict at these admitted boundaries: **REJECT**. RESULT.md describes empty
ratio/count basis conflation; VBF-RESULT.md describes a missing comparison
listing displayed as measured drift zero. Preserve positive controls and
archive-read failure handling. Other requested acceptance remains pending.

Reproduction uses the existing repo and Python environment, a fresh own folder
immediately beneath Database/Tools/work/ASTRA, and repository-root cwd. Copy
only probe-zero-basis.py into the empty folder, then run it. The driver obtains
exact nonempty committed sources itself, executes exact production slices and
refuses overwritten inputs/results. Expected checked exit is1 for the unfixed
delivery, with the ordinary-count, moved-ratio and scope-change controls true.
Do not change expected1 into PASS for that delivery.

For the second control, copy probe-vbf-chain.py and the pinned
source-build_views-eae0ed3c7.py into another fresh owned folder; run from repo
root. It pins the builder hash, obtains exact capture CLI from Git, creates a
bounded synthetic header/listings and preseeded stale outputs, and executes
five real CLI-to-view cases. Expected exit1: missing-listing check false, the
five other checks true. Existing raw results are not an empty test directory;
never overwrite them to reproduce. Changed-source repairs require new receipt
identity and focused failing/positive controls, not edits to these originals.

These are host workflow checks. No new FF12 live/original-code experiment,
installed VBF capture, game/PC session, browser, save/config/reference write,
whole build/server pass or overall migration/database completion. Raw results,
sources, drivers and fixture inputs are immutable after publication. Manifest
binding is integrity only; independent acceptance and canonical incorporation
remain distinct. OPUS owns the actual producers and downstream fixes.
