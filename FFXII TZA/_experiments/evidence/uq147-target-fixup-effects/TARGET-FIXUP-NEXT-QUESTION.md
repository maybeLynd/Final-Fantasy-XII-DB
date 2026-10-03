# Remaining native target-fixup effect boundary

Claim: does `002FEAD0`, called on the resolved target after contributor release,
have any command/mode mutation beyond target flag bit52? Its own disassembly
apparently writes only target DWORD+4 bit20 (QWORD flag bit52). Its callees must
be closed before claiming that complete normal-path effect set.

Competing explanations: the effect is confined to that target flag under valid
state; or a called helper can change command/mode/ownership. Method A is first:
retain verified shipping bytes/CFG and compose exact helper access summaries.
No live observation is required to distinguish these local implementation
claims. Natural KO scheduling and intervening callback state remain separate.

Current finite previews (not qualified evidence): `002FEAD0..002FEB7C` calls
already analyzed field helper `00377C20` and roster predicate
`0030C0E0..0030C202`. The latter scans active units and targets, current command
WORD+714, action-definition byte+6; it calls `00236850`, `00236820`, `0031B7E0`,
`00377C20`, `0020E600`. Consume existing original source/contract evidence for
those getters before any new capture. The mode-query package closes field
helper local reads but remains pending new review; do not call it accepted.

The table-null/address-null arm sets row pointer0 and then reads byte+6. It is
not a successful empty predicate; malformed/unprepared state can fault.
Roster count is reread per iteration, so termination needs a finite stable
valid roster/noninterference premise. Action-row binding, readable structures,
valid private stack and returning ABI are explicit. Do not infer a valid live
table from shipping BSS bytes or synthetic fixture placement.

Controls should discriminate a new command store, an opaque new call, changed
field/row identity, missed scan branch and failed upstream proof. Use the
already reviewed shared access adapter in the actual path. Positive source
writes must remain detected; absence in a preview is not complete effect proof.
Do not re-run accepted restore-copy/79 intervals, EXP-091 fixup fixtures,
EXP-198/231 or the now-settled bit22 partition.

Output: exact closed or still-opaque helper list, original identities/metadata,
normal CFG and state preconditions, deterministic result and targeted controls,
raw receipts; new independent review/consumer scope only if it changes UQ147
composition. Parent ASTRA work claim owns this file. Checked revision50302
showed no peer active target2FEAD0 claim. No PC/game/native/emulator/input,
instrument/save/config/reference changes. The two previews are terminal.
