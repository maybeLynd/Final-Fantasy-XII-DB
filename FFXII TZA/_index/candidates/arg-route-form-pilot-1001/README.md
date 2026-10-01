# ARG route form — implementation and pilot measurement (SWE2-STRUCT, 2026-10-01)

Answers the open grammar question in `candidates/derived-route-parent-roots.md`
(OPUS, 2026-09-25): `ARG <reg> 0xFUNC` — "the object is in `<reg>` at the entry of
FUNC" — was proposed to FRONTIER as the form for argument-rooted parents. The form
is now **implemented** in `gen_route_seeded_census.py` (parse + seedable + host +
entry-register seed, exactly the VTABLE shape with a named register). This record
measures what the form yields on the three sites the proposal named.

**Nothing was written to `types.tsv`.** The pilots ran in-process with the route
injected into the store map; the rows keep their `DYNAMIC - reached as ...` prose
until the form is ruled on. The generator change is additive and inert for every
existing route.

## Pilot results (exe 73461d08…, in-process driver)

| type | route tested | result |
|---|---|---|
| `ActorDefinitionPayload` (0x4C) | `ARG rdx 0x0026C8C0` | **7 offsets** — `+0x04, +0x14, +0x20, +0x24, +0x28, +0x2C, +0x48`: the binder's own field reads. Real census. |
| `AuthoredExpressionBlock` (floor 0x41; size UNRESOLVED) | `ARG rcx 0x0042FDB0` | **21 offsets** `+0x00..+0x40` — independently re-derives the documented layout: four records at `+0x00/+0x10/+0x20/+0x30` (interior offsets `+0x04/+0x0C/+0x0D/+0x0E` per record) and the mode byte at `+0x40`. Real census. |
| `AuthoredExpressionRecord` (0x10) | `EMBED AuthoredExpressionBlock +0x00 stride=0x10 count=4` over the ARG parent | 6 offsets `+0x00..+0x0E` — one element's window, reached through the parent's four `call 004314E0` sites. Real but redundant: the parent's own census covers the same bytes. |
| `ActorDefinitionCountedU16Section` (0x4) | `RELOFF ActorDefinitionPayload +0x14` over the ARG parent | **0 offsets** — the RELOFF combine (`child = parent + *(int32*)(parent+off)`) is not modelled when the parent base lives in an arg register at entry; the rel dword is loaded but never carried. Empty — do not emit. |
| `PaneListWidget0B68` / `PaneSlotWidget0160` | `ARG rcx 0x0029BE50` | **Not run** — both already carry registered censuses (`pane-list-widget-0b68-accesses.tsv`, `pane-slot-widget-0160-accesses.tsv`); ARG would be redundant for them. |

## Assessment for the ruling

- The form is honest: each route states where the object provably is (the named
  register at a named entry, cited per row), satisfying the "no route merely to
  make a census runnable" rule.
- Yield is modest: two real parent censuses (~28 offsets total), one redundant
  child, one no-op. The store's three `DYNAMIC - … ARG proposed` rows already
  carry the fact as prose; `ARG` only makes it parseable.
- Recommended only if the grammar ruling accepts the form; otherwise the prose
  rows already preserve the evidence and nothing is lost.

## Files

- `gen_route_seeded_census.py` — `R_ARG` grammar + `ARG` in `SEEDABLE` +
  `hosts_for` case + entry-register seed in `Census.run`.
- Driver: `/tmp/drive_arg.py`, `/tmp/drive_arg2.py` (session-local).
