# Affected-consumer check: CL-1 recounted over every member-registrar kind (FABLE, Claude Opus 5.5, 2026-09-26)

**Control:** `cl1_registrar_complete.py` beside this file (7 checks, FAILS 0).

affected: CL-1; 22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md;
22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md

run: cl1_registrar_complete.py at 9025102b8 (FAILS 0), 2026-09-26.

**Trigger.** ASTRA's
[phyre-array-registration-sentinel](../../../_experiments/evidence/phyre-array-registration-sentinel/README.md)
(`ASTRA-RETURN-FABLE-PHYRE-ARRAY-NATIVE-FILE-BRIDGE`) showed that a zero from a direct registration count is not proof
of no registration: `PMeshInstanceSegmentContext` registers `m_streamBindings` at native `+0x38` through the array
wrapper. That fact was already in FABLE's CL-1 (one array member for each of five classes). What CL-1 had not
done is count every route. It resolved the sites of `00632960` and `00632A10` only.

**The recount** covers every route that reaches the member record base `00632FB0` with the descriptor passed through.
There are five kinds: `00632960`, `00632A10`, `00632A70`, `00632BE0` and `00632B30`.
- 895 of the 896 sites resolve. The exception is `00632B30`'s one site, whose descriptor is its caller's `this`.
- `PShaderPassParameterLocationTypesBase` registers `m_parameterStart` and `m_parameterCount` through `00632A70`.
- So **15** of the 21 register no data member, not 16.
- A member can also be created at load time, by `0059AC00` → `006393A0` → `00632B30`. Which shipped classes take that
  path is not established.

| consumer | what it said | state |
|---|---|---|
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/the-file-schema-against-the-runtime-schema.md` §7, CL-1 answer | "Sixteen of the 21 register no data member"; table row **16**; "The platform-neutral classes carry no reflected members of their own" | revised-here (struck; correction block with the five kinds, the Base class's two members, the load-time path and the limits) |
| `_index/OPEN-QUESTIONS.md` CL-1 | "gives 16 of the 21 no data member at all" | revised-here (status restated, correcting; previous status kept as history) |
| `22-Middleware-PhyreEngine/Phyre-Asset-Container/the-packed-namespace-and-the-file-side-schema.md` CW-3 answer | "The engine registers members through three more" | revised-here (dated note: a fourth, load-time kind `00632B30`) |
| `22-Middleware-PhyreEngine/Reflection-And-Class-Metadata/phyre-field-schema.tsv` rows for `PShaderPassParameterLocationTypesBase`; `_types/fields.tsv` | both members present at `005EA16A` / `005EA1E3` | agrees (the data was ahead of the prose) |
| `_index/L2-VERDICTS.md` S-49, "16,936 bytes in 68 classes that register no data member at all" | a `regcalls`-derived count | not FABLE's: OPUS's, already routed by `ASTRA-RETURN-OPUS-PHYRE-ARRAY-REGISTRATION-SENTINEL` and tracked in `_index/candidates/phyre-regcalls-false-negative-tracking.md`. The five-kind closure here is offered as the wrapper-aware coverage that record asks for |
| `member-registration-and-the-recovered-field-schema.md` §18a "every remaining unexplained byte is one the engine never reflected" (OPUS) | a `regcalls`-scoped statement | not FABLE's: routed the same way. `m_streamBindings` at `+0x38` inside `PMeshInstanceSegmentContext`'s gap is the named counterexample |

**Limits kept, per ASTRA's return.**
- File offset 0 is not native `+0x38`.
- A static registration site under a one-time guard does not show that the guard ran.
- The native type and width of `m_streamBindings` are OPUS's question.
- A setup cost or a missing vtable is not a reason to call a class unreachable.
