# Old-save preparation: the compatibility copy before the stamp check

ASTRA, 2026-09-13. [Spawn page section27](../../../05-Spawn-Encounter-Lifecycle/spawn-placement-and-retirement.md#27-load-preparation-can-convert-an-earlier-battle-state-region--astra-2026-09-13).

Player version: the game can copy an earlier save-data region into its current
battle-state block and rebuild gambit records before checking that block's stamp.
The earlier prediction that old saves simply retain the session block omitted
this step. Actual party/inventory outcomes still require initialized evidence.

Method A only,8 collected original bodies and3 reused. Shipping EXE SHA256
73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8,
base00120000, Capstone5.0.7. Exact bytes in primary/helpers/mirror/capture.json;
check.json verifies all11 spans, fresh decodes and local branch targets. No live
FF12, original-code execution, provider calls or save decoding by ASTRA here.

Claim/hypotheses: does old short-read tail retention imply the final block remains
unchanged? Source is sufficient to reject that inference:233C10 first calls235AF0.
A nonnull block is compared against active+2200 at0,4,5B42,5B12; any difference
calls2EF4A0, which copies6000 bytes fromactive+2200 toactive+4E68C, then rebuilds
40 three-bank gambit records at5B10 and zeros40 dwords at7370. Later stamp
mismatch/reset is a distinct branch. Pointer binding and valid authored tables
are preconditions; not every injected memory configuration can finish the helper.

Controls: exact source/destination RIP addresses, both equality and difference
branches, null pointer,11 original extents, C0*80 copy size,40*9C and40*4 array
bounds, and4-byte overlap of oldlength4E690 with blockstart4E68C. Both writers
5844A0 and229B40 independently copy6000 back intoactive+2200 after234ED0; the
former skips on blockbyte0 and the latter separately captures8000 into staging.
The former80-byte mirror claim counted one iteration. Guard/reset original
233C10/237DF0/23AF50/2370C0 and memset import are retained. Native234ED0 export
prelude and authored-table effects remain separate. These are source controls,
not executed fixture cases or a whole native conversion test.

Original-byte/library effects and initialized outcome are distinguished:
235AF0 fixed-address copy and pointer-relative rebuild require the bound pointer
to identify the same current image; snapshot coherency is not proved. Converted
bank padding is not fully rewritten. Current reset explicitly resets the spawn
tick and field ids only on its admitted path; no all-load timer claim follows.

FABLE's original decoder/claim scripts are read-only snapshots in existing-work.json.
ASTRA did not rerun nine reported file decodes or invent missing raw output. The
helper's built-in32-byte alternative only runs after31-byte failure; the separately
reported negative-control receipt and input/tool hashes were requested from FABLE.
The native recipe remains independently supported by eaed0a7 original bytes.

P1 contradictions ASTRA-CONTRA-FABLE/OPUS-OLD-SAVE-CONVERSION and companion
MIRROR-COPY-EXTENT requests route the affected save/battle-state/gambit/type/
contract claims and live prediction. Corrections stay pending until consumers
agree. Historical mutations and earlier raw memory-copy tests remain unchanged.
The initial ASTRA idea that four-byte overlap necessarily resets the block also
missed the prelude and is explicitly rejected as incomplete. No full campaign.

Live authorization was explicitly renewed by the user during this package;
recorded in ASTRA.md and shared via TEAM transactions. NoFFXII process or runtime
claim was active in the reconciliation. Existing Python processes are analysis
MCP services/children and were preserved. Metadata query needed supported sandbox
escalation; no OS security or process state was changed. PC control remains off
until actually needed and ends when unused; a NEW stop/takeover pauses automation.
Next: original234ED0 export boundary, peer raw receipts/response, then a bounded
live old-save/L13 test against the corrected hypotheses. Full L1/L2 remains active.
