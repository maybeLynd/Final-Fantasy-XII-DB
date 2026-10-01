# Same-process older-save load: explicit Start=P intervention

Run complete; **bounded observations checked, independent review and canonical
incorporation pending**. Task `FABLE-REQ-ASTRA-OLD-SAVE-LOAD`. Consumers:
FABLE save-image V-12 / spawn-load L-13; OPUS corresponding save/battle contracts.

Player version: the modern Stepping save, title return, and old Southgate load all
ran in one process. The older save replaced the modern party/battle records before
the load-complete prompt was dismissed. The old party and key items were visible.
FF12 exited normally, all original files were restored, and PC control ended.

The following is the prelaunch plan; actual results and limits follow below.

H1: legacy compatibility records replace the modern battle prefix/bank0.
H2: previous modern state survives instead. H3: returning to title already clears
some state, so a field-to-old difference cannot all be assigned to the old loader.
Keep-bank endpoint equality alone does not prove uninterrupted lifetime or writers.

Method C is required for actual initialized same-process loading. EXP080 already
established fresh-title legacy import, EXP081 modern-load positive; EXP082 and the
preceding old-save-same-process run did not reach the same-process old load. Reuse
their bounded read observer and input instrument. No debugger, memory writes,
injected calls or trace breakpoints. Do not repeat the failed Config/Exit-cancel route.

Reference SHA256 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8;
mapped .text SHA256 5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4,
7996981 bytes, image base120000. Fresh Cloud OFF/empty launch options receipt,
full verified save/config backup, no existing game and clean module controls required.
Modern FFXII_000 hash859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825;
old FFXII_004 hash8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc.
The old test save's prior modification history is unknown.

One labelled file intervention: current-account Keyboard2 Start=0 ->43 (P), exactly
the candidate already checked against original registry/name/scancode/reserved data
in ../old-save-same-process/next-start-binding. Primary Escape and all other bytes
remain unchanged. Native parsing/Start acceptance still requires live proof.

Feasibility: modern field -> one P pulse, with35 zero baselines, expected index15
held positive and zero release -> visible PAUSE with an ordinary title-return action.
Follow only observed prompts. Registration alone does not establish acceptance.
If no usable Pause route, stop that method and preserve the narrower result.

Capture two samples at each of modern field, returned title, old load-complete,
old field; optional modern-complete gives at most10 samples. Maximum20 minutes
from launch. Snapshot active image02164280, B via02EBF190, keep banks0208E690/698,
actor bindings and field/tick using the existing observer. Compare pre-gambit prefix,
40 bank0 records, selectors, levels and nonzero keep evidence across each transition.
Full before/after code/module identity, known read/null controls, pointer brackets,
nonempty raw reads and handle closure required. Missing state/failed controls/stop
ends the run. Fatal dialogs or failed responsiveness invalidate semantic acceptance.

Preserve screenshots for visible state and raw memory for internal state separately.
Sequential reads are not atomic; no claim about intermediate writers, universal
defaults, stable pointer identity or lifecycle from endpoints. An imported block
must be compared to independently decoded old records and prior modern/title state.

Exit the owned instance normally, verify absence, immediately end PC control,
preserve and review changed working files, restore this fresh backup byte-for-byte,
recheck reference/save/config hashes. Unexpected changes stop automatic restoration
for review. Return raw evidence, normalized reducer with negative controls, limits,
health/cleanup receipts and consumer routing. No claim closes before these checks.

## Observed route and input evidence

PID34844 / window1902042, 2026-09-21, 06:07:52 through06:17:49 UTC (597seconds).
Fresh [backup](save-before.json), [environment](environment.json), [Cloud screenshot](cloud-before-0.jpg),
[deployment](deployment.json) and [process](process.json) identify the run.
The input-binding intervention was accepted: P registered index15, released to
zero, and [opened PAUSE](pause-response-0.jpg). The game displayed **F Exit to
Title Menu**. [F's exact registry/scancode check](f-key-preflight.json) preceded
its bounded pulse; it registered index5 and opened the title-return confirmation.
Wheel+120 selected Yes; Enter returned to title in the same process.

Thirteen [input receipts](observation.json) retain35 zero baselines each, positive
held detection, zero release, two delivered input forms each way, code/module
identity brackets and closed handles. These establish sampled registration;
the associated screenshots separately establish menu acceptance. No combat action
or consequence is claimed. The wheel actions have presentation evidence but no
raw keyboard-registration receipt; do not conflate these two methods.

Save-list wheel-360 moved upward one entry and wheel+480 moved downward one entry
in this route. Subsequent separate+120 actions selected004. The initial immediate
screenshots sometimes retained the prior hand position while the highlight moved;
settled screenshots were checked before confirming. These values are observations
of this UI/tool combination, not universal step-count guarantees.

Old004 reported [Load complete](old-load-complete-0.jpg), entered
[Rabanastre/Southgate](old-field-before-0.jpg), and accepted R to open its
[party menu](old-menu-response-0.jpg). That menu showed six level21 characters,
9999999gil, and HP742/722/668/778/674/661 respectively. Inventory displayed
[seven key items](old-inventory-open-0.jpg): Clan Primer, Writ of Transit,
Crescent Stone, No.1 Brig Key, Systems Access Key, Manufactured Nethicite, Dawn Shard.
These are post-load presentation observations, unlike the prior save-list-only
metadata. The test save's prior modification history is still unknown.

## Normalized state comparison

[check.py](check.py) reduces retained raw bytes; [observation.json](observation.json)
and [validation.txt](validation.txt) contain the complete comparison. Eight accepted
samples cover170 complete spans. All retain the exact executable/full mapped text,
nonempty module list, known nonzero read control, rejected null read, raw binding
brackets and handle closure. The watched-module verdict is bounded by that detector;
it does not certify every module effect.

The comparator reuses the existing save-container roundtrip's four decoding
functions only, without rerunning that campaign. The fresh backup's exact004
decodes to4E690bytes, rotation26, plaintext SHA256
`9d7314c38ed17619f7abb84ce0e084bbe2cbbca2a9e2dfb040012ff3b06eba38`, matching its
retained real-file roundtrip receipt. This documented offline decoder is **not**
original-code execution. It provides an independent saved-byte reference for the
live block rather than merely comparing the live block against another live copy.

| State (both samples agree on these columns) | First six levels | B prefix[0,5B10) equals saved old compatibility | Bank0 records matching old save | Nonzero bytes, keep1/keep2 |
|---|---|---|---|---|
| Modern field |1,1,1,1,2,1|no|22/40|328/0|
| Returned title |1,1,1,1,2,1|no|34/40|0/346|
| Old Load complete |21,21,21,21,21,21|yes|40/40|0/346|
| Settled old field |21,21,21,21,21,21|yes|40/40|0/0|

Partial bank matches at modern/title do **not** mean those records were imported;
common/default records can agree across saves. The full-prefix and differing
party records provide the discriminator. B stays at021B290C (active image02164280
+4E68C), with stamp05071901 and all40 selectors0 in these samples. Equal stamps or
zero selectors alone do not prove compatibility import or a selector-reset write.

Between modern field and returned title,220 battle bytes differ (E..6B82); between
returned title and old Load complete,1572 differ (4..5EB6). The two old-stage battle
blocks are byte-identical. Thus the sampled old load refutes **H2's simple retention
of the previous modern battle state** and supports H1's compatibility import for
the checked prefix/bank0. It does not establish the writer instruction or universal
behavior for other files/builds. Title transition also changed state (H3 matters),
but did not itself produce the older party records.

Keep pointers are recorded separately from contents. Keep1's328 nonzero bytes at
modern field are zero at returned title; keep2 has346 nonzero bytes at returned
title and is byte-identical at old Load complete, then zero at settled old field.
Modern keep1 is **not** byte-identical to returned-title keep2. Do not describe
this as a proven direct bank copy, swap, wipe instruction, or uninterrupted lifetime.
Only the sampled values and stage-bounded changes are established. No enemy death,
respawn consequence or native callback ordering was tested.

## Rejected transition capture and regression control

The initial [old-field capture](old-after-current-field-memory.json) is **INVALID**.
Its registry+68 changed0 ->6F6343C0 during the sequential read; the other pointer
brackets and unit identities matched. It was collected shortly after field entry,
before the later responsive menu/inventory/back cycle. The cause of that particular
write and its scheduling are not established. A snapshot cannot be called atomic
merely because the field is visible.

The [amendment](settled-capture-amendment.json) required a visibly settled field
after successful ordinary menu actions, retained a distinct output label and left
all observer checks intact. The two settled samples passed; total attempted
samples9 remained below10. No rejected bytes are used in the accepted comparison.
The checker rejects the actual failed sample even when its `registry_stable` flag
is forged true, using the raw bracket mismatch. Empty memory, empty input and
no-held-detection cases are also rejected. Independent review remains required.

Two initial offline reducer runs stopped on mismatched convenience-field schemas
between the reused input/memory instruments; [development-failures.txt](development-failures.txt)
records the correction. Exact raw code hashes and module inventories are required
in both formats. No failed reducer run produced an acceptance artifact.
[source-catalog.json](source-catalog.json) retains11 exact tool versions, including
the pre-F sender and pre-settled-label observer; source history was not overwritten.

## Health, cleanup and downstream boundaries

[Health evidence](health.json) consists of observed menu/field acceptance, inventory
opening/cancellation, post-capture presentation, and the normal exit dialog. No
fatal dialog was observed. This is point-in-time visual inspection, not exhaustive
monitoring of every interval. The rejected transition sample was an observer
consistency failure; it was not accepted as a healthy semantic snapshot.

[Normal exit](exit-action.json) and [process absence](process-after.json) were
followed immediately by PC-control reset. No hook/debugger was attached. All18
read sessions (13 input +5 memory, including the invalid one) closed their handles.
[Cleanup](cleanup.json) preserved the working differences and restored all26 original
hashes; only the intentional Start binding and GameSetting.ini LUIDLow changed.
The fresh backup and [reference executable](reference-after.json) remained unchanged.
Runtime is released; live authorization remains active absent a new stop/takeover.

Consumers: FABLE's save-image V-12 and spawn/load L-13; OPUS's save-image/battle
contracts. Incorporate same-process import, title-versus-load distinctions and
post-load party/key-item presentation. Leave native writer/order, ownership
continuity, selector-reset observation, gambit UI, enemy consequences and universal
save compatibility open. Sequential observations cannot close those claims.
This completes this bounded capture, not the full database or L3 parity.
