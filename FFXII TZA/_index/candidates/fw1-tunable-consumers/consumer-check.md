# Affected-consumer check: FW-1 answered by consumer; "the twelve cached tunables have no consumer" corrected (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `fw1_tunable_consumers.py` beside this file (3 checks, FAILS 0).

The FCP page said the unit's cached tunables had no consumer beyond their installer. The access census could not
see the consumers: the locomotion solvers read them through the solver context, whose builder stores unit + 0x80 at
ctx `+0x108`. Every tunable has a consumer on that route. The exceptions are `+0x180`, read by a unit-direct getter
whose caller stores the scaled result at `+0x17C`, and `+0x184`'s unit-direct forward to the render record.

| consumer | what it said | state |
|---|---|---|
| `17-Presentation-Rendering/Model-And-Motion-Formats/fcp-character-parameter-block.md` §6.1, last paragraph | "still have no consumer beyond the installer in the access census" | revised-here (struck; the consumers and the route beside it) |
| same page §7, the `UQ-217` box | "the twelve cached tunables' consumers are still unread. **FW-1.**" | revised-here (struck clause, pointer to §6.1). `UQ-217` itself stays open: the authoring names are not in the executable |
| `04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md` §2.6.2 row `+0x164` … | "One consumer is now known: `+0x16C` …"; meaning OPEN | revised-here (dated note in the row: every consumer by role; the status cell updated) |
| same row's field names `fcpRadiusSlot0or6` / `fcpRadiusSlot1or7` | radii | revised-here as a note (the names are kept as census labels; the consumers use a step length and a step-length threshold) |
| `06-Movement-And-Navigation/Battle-Locomotion/battle-locomotion-steering-and-recovery.md` (the published `+0x16C`/`+0x170` readers) | the slow/fast turn rate | agrees (the triage tracker's sensitivity control found all six published readers) |
| `_index/OPEN-QUESTIONS.md` FW-1 | OPEN; the consumers not reached | revised-here (ANSWERED by consumer; the authoring names stay with `UQ-217`) |
