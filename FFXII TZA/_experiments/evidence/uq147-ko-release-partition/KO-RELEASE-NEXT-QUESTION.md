# Next bounded KO cleanup discriminator

Question: does the earlier general KO helper `00310780` itself overwrite the
acting or resolved target unit's committed `+0x714`, pending `+0xBA0`, or battle
mode, before the later Dismiss request/recomputation? This is a local-effect
question, separate from what its callees do and from natural KO scheduling.

H1: its direct writes clear the relevant command/mode state. H2: its own writes
release relation/presentation fields while command/mode effects, if any, belong
to called helpers. This distinction changes the UQ147 composition premises.

Method A first. Current retained-map lookup found no covering source map among
1343 searched maps; this is not global absence. Saved original disassembly
preview `preview-ko-release-01` completed successfully with pinned retool
`f6bb3757...`, interpreter `199ce15a...`. It shows a return at `00310860` and
four apparent direct non-stack write sites: target `+0xEA8`, target `+0xEA4`,
acting flags `+0`, acting presentation byte `+0x694`. The `+0x714` access shown
is a comparison against `0x414E`, guarding the already-known notification
forwarder `00317E50`. These are feasibility observations, not a qualified
whole-body or transitive effect conclusion.

Next action: validate the shipping `.pdata` root/chained extent, reuse the
existing reviewed capture path with its actual store/LEA/RMW controls, then
check all connected instructions and direct non-stack writes/call boundaries.
Use a positive detected write and a cause-specific altered command/mode store
control for the negative local-write claim. Do not rerun EXP-040, EXP-198, S20,
the mode-query proof, or earlier notification effects.

Acceptance: exhaustive local write set and qualified call order agree with
complete pinned shipping bytes/metadata and the actual shared access adapter;
controls discriminate an added/retargeted command write. A missing fragment,
failed prerequisite, unknown write role, or escaping selected CFG invalidates
the local proof. No full cleanup or natural lifecycle conclusion follows while
opaque callee effects remain open. Calls include `0031B7E0`, `00313B30`,
`002FEAD0`, `00308270`, `0030C970`, `00319420`, `00319140` and conditional
`00317E50`; consume existing owning evidence before expanding any one of them.

Consumers: existing FABLE UQ147/status/mode clauses and OPUS command contracts,
after a distinct scoped independent review. Parent
`FABLE-REQ-ASTRA-RT-REMAINDERS-PROBES-0929` owns these working files; checked
revision50292 showed no peer active claim on this target. No canonical page
edit or new claim over peer work. No game/process/input/native execution,
instrument, save/config/reference change; preview helper is terminal.

Prior stage-order evidence is committed `3a25a0be0c3a450c0d7d353d5c66096ff491a04e`,
verified/released; new scoped SPEC/FABLE/OPUS routes50288–50290 await acceptance
and consumption. That result does not close UQ147 or the full L1+L2 goal.
