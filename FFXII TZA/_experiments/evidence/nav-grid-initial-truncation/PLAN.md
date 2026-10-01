# Grid refinement provisional-count precondition

Question: are positive finite rectangle extents alone sufficient for the original
grid refinement to avoid a zero provisional count? Competing explanations:
CVTT results are clamped to1; a zero exits before refinement; or zero is divided
into a positive width. Consumers: OPUS NavGridParams/corridor constructor rule,
FABLE navigation builder semantics. Final BMASK interval precondition is a separate
result (33); builder positive-final-dimensions are not assumed from that result.

Known primary: immutable nav-grid-quantization607B003924B0, getter252B/decoder10B,
shipping73461d. At3925A9/CE CVTT;3925E9/FC divides by converted counts;
MAXSS392600, floorf call392607. No intervening count test in the123B prefix.
Positive finite original header1x400 can be represented by u8(1,20,1,20),
s16 origins0. Nominal source sqrt preparation from400/275 predicts c0>1, so
1/c0<1, nx0, width/nx+Inf with masked exceptions. Native sqrtf effects remain
unproved; this prediction is not an original run.

Method B: exact original123B39258C..392606, entry aftersqrtf/stopbeforefloorf.
Supply and read back finite c0 bits inXMM0, widthsXMM10/11, min/maxXMM6/7/8/9,
alignedstack including disclosed padding+24/+34, globals andMXCSR1F80. No stubs
or native calls in the executed window. Disclose host c0 preparation/injected
boundary, omitted getter/wholebuilder/library effects; do not label a modelled
math return as original native sqrtf evidence.

Controls:16x16 prepared input yields positive counts/finite refined output;
1x400 discriminates. Labelled firstCVTTSS2SI->CVTSS2SI changes nx0 to1 under
nearest, so refined input no longerInf; source identity must reject mutant.
Capture PC-proportional read/write/initialized-state evidence and count snapshots
at instruction boundaries, budget128instructions/case. Stop on first control,
identity or observer failure; retain incomplete receipts, no blind rerun.

Acceptance: original code unchanged, exactentry/stop/initialstate, nonempty counts
and writes, expected0 versuspositive count/refinedbits, detector changes result.
No actual authored occurrence, nativeCPUexceptionstatus/librarybinding/floorf/
allocation/fault/normalcaller/scene guarantee. Positive intermediate count is
separate from initial positive rectangle and final dimensions. No old13x13,
50x50 or upper-bound capture repeated. Freeze existingbytepolicy beforemanifest,
explicitreviewedpaths, ownerprecondition/exactspec propagation and independentreview.

PC OFF; disposable emulator only, no reference/save/config/peer/process writes.
General boundedlivepermissionACTIVE; S19 budgetspent/extraunapproved unaffected.
