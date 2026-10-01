---
experiment: EXP-081
title: Initialized BattleUnit stats and authored-row bindings after loading The Stepping
status: COMPLETE
contract: none — bounded initialized bindings for FABLE-REQ-ASTRA-BU-POINTERS
tool: evidence/battleunit-live-bindings/observe.py
method: C - ordinary UI input and read-only process observation
live_game: true
date_designed: 2026-09-13
date_run: 2026-09-13
---

# EXP-081 — live stats have different owners from authored definitions

**Result:** in two samples of one ordinarily loaded field, Vaan's bound stats
point into the battle-state save block. Three kind-1 units' stats point into
their respective SpawnKeep records at `+0x80`. Their `+0xE68` pointers instead
identify separate rows of the area's class-definition table. This agrees with
FABLE's corrected original-code reading and refutes the competing mapping in
this initialized state. No installer call was injected or traced.

**Player version:** a spawned enemy's current condition, such as its HP, lives
with that spawned unit. The definition of its kind is separate. Party characters
use their records in the party save data. Loading the save and initializing the
field also proved to be different observed stages.

## Question, method and initial state

The existing task recorded before setup:

- H1: kind 1 has `unit[+698] = unit[+6A0] + 80`, inside primary SpawnKeep;
  `+E60` is the selected area enemy row and `+E68` its referenced class row.
  Kind 0 has `+698 = *(02EBF190) + 8 + k*1C8`, `+6A0 = 0`, `+E68 = 0`.
- H2: the spawn record's embedded stats feed `+E68`, or kind-1 stats are taken
  from the party battle-state array instead.

Method A first: read the [installer account](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
and [authored-row contract](../02-Resource-And-Asset-Pipeline/CONTRACT-authored-table-row-lookup.md),
then verify EXP075's preserved [1,808 shipping bytes](evidence/EXP-075-reward-index-prechecks/0023A570.bin)
against the exact executable. SHA-256 is
`a5194ef62b2556c92117b3ae40980d2ff334a08d495ec9cca82995209cd1d39a`.
The relevant original stores are `0023A915/0023A91C` (enemy row/class),
`0023AAAA..0023AAC1` (party stats), and `0023ABFA/0023AC01` (common stats/spawn).
The earlier reward-boundary emulator was **not rerun**; its callee stubs cannot
establish live allocation or resource binding. [Source identity receipt](evidence/battleunit-live-bindings/source-review.json).

EXP026 already recorded stats/spawn relationships but omitted `+E60/+E68` and
their table bindings. C was therefore necessary for the missing initialized
addresses. The existing EXP080 read-only observer was adapted only for the
requested regions, labels and runtime task. No new runtime platform.

`@runtime` was held under FABLE-REQ-ASTRA-BU-POINTERS from revision6370 to6381.
Reference PID **30640**, ordinary Steam executable, base `00120000`, SHA-256
`73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
The selected autosave was **Dalmasca Estersand / The Stepping, 000:08:42**,
level01/gil150 as save-list metadata. Backed-up `FFXII_000` was5,331B,
SHA-256 `859a83073daa95b13db9b6461d336d5ccb2e4e94252a8d167194bae35d6cb825`;
its SAFH header declares `56690` decoded bytes and rotation12. No new decode.
All26 save/config files were backed up and hash checked; Steam Cloud was
visibly OFF and advanced launch options empty.

## Input and presentation controls

The [selected save](evidence/battleunit-live-bindings/selected-save.jpg) was
reached from the title with a mouse click. Two brief clicks on the selected
autosave did not produce an observed load. Those failed controls are retained:
[first](evidence/battleunit-live-bindings/load-click-not-observed.jpg),
[before alternate gesture](evidence/battleunit-live-bindings/before-drag-control.jpg).
A single supported `sky.drag` from `(600,240)` to `(602,240)` was followed by
loading and the completion popup. One equivalent two-pixel gesture dismissed it.
This is a bounded successful gesture, **not** proof that hold duration caused
the difference; neither mouse registration nor the input-handler calls were traced.

Each capture is bracketed by screenshots:
[popup before](evidence/battleunit-live-bindings/current-complete-before.jpg),
[popup after](evidence/battleunit-live-bindings/current-complete-after.jpg),
[field before](evidence/battleunit-live-bindings/current-field-before.jpg),
[field after](evidence/battleunit-live-bindings/current-field-after.jpg).
The field screenshots show Vaan at HP103/103, MP33. They do not identify each
off-camera unit's species or prove an internal pointer interpretation. No movement,
target selection or combat command was sent.

An initial Steam capture showed an occluding browser's pixels despite the target
window metadata. It was rejected as settings evidence. Explicit activation and a
fresh capture showed the actual [FF12 General properties](evidence/battleunit-live-bindings/cloud-before.jpg).
No input was sent based on the wrong pixels, no setting changed, and unrelated
browser pixels were not copied into the experiment. No stop/takeover was reported.

## Raw evidence and observer controls

Raw [completed-load receipt](evidence/battleunit-live-bindings/current-complete-memory.json)
and [field receipt](evidence/battleunit-live-bindings/current-field-memory.json)
contain **four samples /88 full-span reads**, with each requested address, size,
returned bytes, SHA-256 and sample timestamps. The [normalizer](evidence/battleunit-live-bindings/review.py)
checks identities, nonempty case populations and raw spans before producing the
[observation](evidence/battleunit-live-bindings/observation.json). It only reads files.

Both states passed full live `.text` equality:7,996,981B, SHA-256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
Known `LUAC_TAIL` returned `19930d0a1a0a`; a null read was rejected; all reads
required their complete requested extent. Both process handles closed successfully.
The observer source SHA-256 is
`3fd84bbf8ffb7acb6f398333275193d7af13bea895f284ded4ccda86689b5438`;
runtime_probe/ffxii_runtime source hashes and102 loaded modules are retained in
each receipt. The watched-name `clean` verdict does not certify every module,
IAT entry or heap byte. No game-memory writes, suspension, debugger, hook or
injected native call was used.

The reads include the complete32-slot BattleUnit pool before/after, bound stats
records, both keep banks, the full save image/current block, three complete
authored tables, registry pointers and the address base. Unit handle/actor/slot
and binding bytes agree across the bracket. Registry/pool/base brackets also
agree. These are **sequential, non-atomic reads**; no claim of a simultaneous
whole-process snapshot or continuous stability follows.

## Initialized ownership and resource membership

In both field samples `*(02EBF190) = 021B290C`; address base `01F83530 = 0`.
Primary/secondary keep pointers are `67556F80 /6754DB40`. Table headers supply
the row strides; no stats-record stride was substituted for an authored stride.

| Registry /table | Descriptor | Row base | Count | Stride |
|---|---:|---:|---:|---:|
| `02EBF130` party | `67524760` | `67524780` |40|`80`|
| `02EBF120` area enemy | `67483670` | `67483690` |15|`58`|
| `02EBF150` area class | `6747F330` | `6747F350` |12|`54`|

Addresses, offsets, definition ids and strides below are hexadecimal; slot and
row indices are decimal. Both field samples have the same four bindings.

| Unit slot /address | Definition id | `+698` stats | `+6A0` spawn | `+E60` definition row | `+E68` class row |
|---|---:|---:|---:|---:|---:|
|0 /`675603C0`|`0000`|`021B2914`|`0`|`67524780`|`0`|
|4 /`67564100`|`0106`|`67557000`|`67556F80`|`674838A0`|`6747F4A0`|
|5 /`67565050`|`0105`|`67557250`|`675571D0`|`67483848`|`6747F44C`|
|7 /`67566EF0`|`0100`|`675576F0`|`67557670`|`67483690`|`6747F350`|

- Kind0 slot0 stats = `B+8`, with all456 returned bytes equal to the current
  block's slot0. Spawn/class pointers are null. Its authored definition is party
  row0. The observed HP103 agrees with Vaan's separately captured display.
- Kind1 slots4/5/7 use primary keep entries0/1/3; every stats pointer is exactly
  `spawn+80` and every456-byte stats record equals that bank slice. The stats
  kind byte is1; observed HP values are134/6111/84, not screenshot-derived.
- Their `+E60` pointers identify enemy rows6/5/0, exactly their definition-id
  low bytes. Those rows' word `+0` values are4/3/0; `+E68` identifies precisely
  class rows4/3/0. All three class pointers lie outside **both** keep banks and
  differ from the stats pointers. Kind1 stats are outside the battle-state block.

This supplies the requested independent address/range/index distinctions. Kind1
means the spawn-backed definition path; no broader allegiance classification,
rendered enemy identity, native installer chronology or reuse lifetime is proved.

## Useful transition result, with the remaining load question kept open

| Observation | Load complete, before dismissal | The Stepping field |
|---|---|---|
| Image field id |`00E3`|`00E3`|
| First six party levels |1/1/1/1/2/1|1/1/1/1/2/1|
| Enemy/class registry slots |both null|both bound as above|
| Units with occupied flag, actor and stats pointer |0|4|
| Primary/secondary keep nonzero bytes |0 /0|328 /0|
| History last/previous |`FFFF /FFFF`|`00E3 /0131`|
| Raw clock in the two samples |0 /0|1408 /1423|
| Parity byte |0|1|

The party table was already bound at the popup; area tables and the four unit
bindings were observed only after dismissal. Null registry slots **do not prove
that the underlying resources were absent everywhere in memory**. The populated
primary bank is initialization evidence, not a kill-history or respawn test.
The history values are observations; which intermediate native writer supplied
`0131` was not traced.

This adds a fresh-process modern-save control to EXP080's fresh-process older
manual-save observation. Different saves and processes are not a same-session
modern-to-old test. FABLE's full older-load request, L13's nonzero-bank retention
and rotation questions, menu presentation and causal load chronology stay open.

## Cleanup, consumers and review

Normal Alt+F4 raised Exit Dialog; Return was followed by verified process exit.
[Exit receipt](evidence/battleunit-live-bindings/exit-check.json) and
[cleanup receipt](evidence/battleunit-live-bindings/cleanup.json) confirm no game
remains, all26 original hashes restored and the backup unchanged. Only account
GameSetting.ini LUIDLow changed79439→78642; the working config was preserved
before restoring it. No debugger attachment means no debugger detach was claimed.
The unused PC-control JS session was reset immediately after exit verification.

Consumers: the [unit installer](../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md),
[kind-byte account](../04-Actor-Entity/Battle-Record-Kind/battle-record-kind-byte.md),
[BattleUnit map](../04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md),
[ARD binder](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/how-the-ard-loader-binds-area-battle-data.md),
OPUS's `+698/+6A0/+E60/+E68` fields/contracts, and the open spawn/load frontier.
High-impact primary review and owned propagation are routed to FABLE/OPUS.
Do not promote a complete contract or full database on the strength of this run.

## SECTION-03 reward-binding consumption — 2026-09-22

The [independent retained review](evidence/continuation-section03-reward-bindings/REVIEW.md)
reconstructs all 88 captured spans in four samples and checks 10 deliberately corrupted variants
without importing the original observer/normalizer. Replaying the separate historical retained
checker also exactly reproduces its observation and four negative controls. This is retrospective
verification of the original files, **not a new live capture or new process-health test**.

The two field samples retain stable registry words and three kind-1 units' reward-pointer pairs;
working stats bind to their retained SpawnKeep records, not directly to authored definition rows.
Their selector/address differences are consistent with stride `0x38` and an index-zero address at
`descriptor+0x20`, but no actual reward header or required row prefix was captured. Header
contents, reward coefficient values, payout, lifetime and producer timing remain unestablished by
these observations. Zero registry words at the completed-load popup do not demonstrate a reached
NULL-row reward call.

The updated [award contract](../13-Rewards-Progression-Economy/CONTRACT-experience-and-licence-award.md)
consumes exactly that bounded observation alongside separately verified producer instructions and
71 synthetic original-code consumer checks. Raw EXP-081 files, prior acceptance records and TEAM
claims are unchanged; peer acceptance of these new canonical edits remains pending.
