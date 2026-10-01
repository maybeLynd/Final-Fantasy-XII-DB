# An older-format manual save loads into initialized Southgate

**Player version:** FF12 accepted the older save, loaded Southgate, and restored
six level21 character records. Their gambit bank0 data matches the older save's
compatibility records. The title's existing battle state was not simply retained.

This is [EXP-080](../../EXP-080-older-save-live-load.md), **method C**, with a small
supporting method-A clock-helper read. The [review](review.json) and
[reviewer](review.py) operate only on retained captures. They do not open a game.

## Question and method selected before launch

Competing outcomes were: refusal of the older image, successful read with session
battle state retained, or compatibility import before continuing into the area.
Earlier complete source and isolated original short-read evidence cannot settle
initialized binding, actual ordinary load, or presentation. Thus C was necessary.
The minimum sufficient feasibility probe was fresh launch, ordinary manual004
load, then area entry; snapshots bracket the load popup and area state. A modern
save control and same-session modern-to-old comparison remained conditional on
that feasibility. They were **not performed** in this bounded run.

No injected calls, game-memory writes, hooks, debugger attachment, suspension,
modified executable or new runtime platform. Setup used the established EXP079
backup/environment method. Observation retained its exact process, module, full
text, known-byte, rejected-null-read and handle-close controls; only requested
data spans, labels and task identity changed. No earlier FF12 experiment or file
decode was replayed. UI automation used the existing computer-use skill.

## Identity and protected state

- [process.json](process.json): the explicitly launched Steam reference, PID46768,
  image base00120000, executable SHA-256
  `73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8`.
- [environment.json](environment.json) identifies the selected installation and
  rejected mod clients; [Cloud check](cloud-before.json) records the observed
  OFF toggle and empty advanced launch options. No Cloud setting was changed.
- [save-before.json](save-before.json): all26 original files copied and hash
  verified; original backup stays under ASTRA's workspace. The original live
  location is the disposable working copy for this session.
- [save-inputs.json](save-inputs.json): all nine current account save files match
  the existing EXP015 backups. Selected `FFXII_004` is7066 bytes, SHA-256
  `8fb99c6dc9956048af2f37b8ace57dd9e5b680967905ba5d72fdfa499acb63bc`,
  header `SAFH`, declared decoded size`0x4E690`, rotation26. This is a header
  observation and exact file identity, not a new decode or historical-build proof.
  Prior modification history of this preserved test save is not established here.

The ordinary menu selected **004 / Rabanastre / Southgate / 006:53:57**. Six
level21 portraits and9999999 gil were visible **in save-list metadata**; these are
not presented as post-load inventory/menu observations. Raw images and sidecars:
[selected save](old-selected-save.jpg), [load complete](old-complete-before.jpg),
[Southgate](old-field-before.jpg), with before/after capture pairs in this folder.
The sidecar timestamps are receipt times, not synchronized exposure timestamps.

## Controls and raw observations

Each state has two sequential samples about0.25 seconds apart. Every sample reads
the bound battle pointer, keep pointers, window/history/stamp, clock/parity,
whole active`0x56690` image, bound`0x7410` battle block, both`0x9400` keep banks,
authored definition/preset handle slots, then brackets the pointers and clocks.
All84 requested data spans were read in full with retained hex bytes/hashes.
These sequential reads are **not atomic snapshots**.

Each state also matched all7,996,981 disk `.text` bytes in live memory, SHA-256
`5421e8b234942659d6af8438bd65d830194d3c1cecb530c0bc515598e9354db4`.
Known nonzero `LUAC_TAIL` bytes at01CCD300 returned`19930d0a1a0a`; address-zero
read failed rather than returning synthetic zeroes. Complete module inventories
and source/tool hashes are retained. `clean` is the existing watched-module
verdict; it does not certify every loaded module's effects or every data byte.
All read handles closed. No debugger or instrument needed detaching.

The [first capture attempt](fresh-title-first-attempt-memory.json) is **INVALID**:
the sandbox could not read the module list. It stopped before any samples or
pass receipt. Supported elevated read access then allowed the **unchanged**
observer to complete; this did not change the game or bypass a security setting.
The reviewer explicitly requires the invalid attempt to remain excluded, and
requires successful controls and nonempty complete samples for accepted states.

| Observation | Fresh title | Load complete, before dismissal | Southgate after dismissal |
|---|---|---|---|
| Bound block | `021B290C`, active`+4E68C` | same | same |
| First six record levels | 1,1,1,1,2,1 | 21,21,21,21,21,21 | same21s |
| Block prefix`[0,5B10)` equals saved compatibility prefix | no | yes | yes |
| Bank0 equals saved older per-record set | 0/40 | 40/40 | 40/40 |
| Selected-bank indices | all0 | all0 | all0 |
| Field id, whole-image`+1244` | `000C` | `0132` | `0132` |
| Last / previous field | FFFF / FFFF | FFFF / FFFF | 0132 / FFFF |
| Transition stamp | 0 | 0 | 0 |
| Raw tick, two samples | 0,0 | 0,0 | 1414,1429 |
| Parity | 0 | 0 | 1 |

The title-to-complete battle block differs in1545 bytes, from offset4 through
`5EB6`. Both states retain the valid stamp`05071901`. Every loaded bank0's52
bytes equals the corresponding compatibility record at`legacy+90+i*1C8`.
Member0 bank0 begins`01 60 96 00`; banks1/2 begin`00 60 96 00`. This difference
is consistent with preserved older configuration versus authored preparation;
we did not read the native authored preset rows or identify their player labels.

Both keep banks stayed at their original pointers`6752FF80` / `67526B40`, and
were entirely zero in all samples. Therefore this run **cannot distinguish**
preservation, copying, swapping or wiping of bank contents. Likewise selectors
were already zero, so their final zero does not independently prove a reset write.
The live clock advanced15 ticks between the field samples. This demonstrates
sampled activity, not a general timer frequency or scheduling contract.

## Interpretation, limits and correction routing

The observed completed load and changed battle records refute the prediction
that this fresh-title older-save load merely keeps the existing battle block.
They support section27/28's source-derived compatibility import composition.
They **do not directly trace**233C10,235AF0,2EF4A0 or the next rotation call.
Field/history/parity changed between popup and field captures; intervening writers,
native chronology, nonzero keep preservation, reused session state, enemy respawn,
and loaded gambit/inventory menu presentation remain open.

FABLE's clock-reset source addition was separately verified:
[clock-primary.json](clock-primary.json), **0032A160**, eleven shipping bytes,
SHA-256`341fefc95f92b91553bba7849a9993eae55b49f0f801a48a3627554493d4a845`,
one dword-zero write to0208D45C then RET. The already captured237DF0 calls it at
237E37. This establishes a conditional native reset path, not that it ran in
this particular load. The reviewer checks those exact original bytes afresh.

Input feasibility was bounded: mouse wheel selected slots and mouse confirm
opened/loaded/dismissed the menu. Down, k and later the documented R binding had
no observed game response; middle click did not open the main menu. Do not infer
that all keyboard injection is impossible or that the native menu is unreachable.
Existing EXP006/EXP010 input receipts remain relevant; keyboard-dependent tests
were deferred rather than repeated blindly. The session was then ended.

[cleanup.json](cleanup.json) proves all26 original hashes restored and unchanged
backup, after process exit. Only GameSetting.ini's LUIDLow differed; the working
version was preserved before restoration. An exit-dialog element click was
rejected by the UI tool's cached-state lookup; a refreshed focused dialog accepted
Return. [exit-check.json](exit-check.json) records no remaining game process.
The PC-control session was reset when unused and after exit. No user takeover
occurred during this run; the existing live authorization remains active.

Affected claims: spawn L-13, old-save V-12, compatibility import/selected-bank
behavior, conditional clock reset. FABLE/OPUS own dependent save/gambit/types/
contracts and review. Their accepted static conversion correction5895b65 is
separate from this new live observation. Full database L1/L2 and final reviews
remain incomplete; no EC-7 family count or primary reconstruction phase changed.
