# World / Area / Field

**Engine category.** Zones, the field runtime, MapRef and environment data, and Weather.

| | |
|---|---|
| Classification source | PrimaryOwner: WorldAreaField |
| Functions | 108 |
| Status | see [`../_index/COVERAGE.md`](../_index/COVERAGE.md) |

Small owner count, disproportionate importance: this category decides what "where you are"
means, and it owns Weather, which reaches combat, spawning, presentation and resources.

## Systems in this category

### [`Weather/`](Weather/) - **documented**

- [`weather-slot-state-model.md`](Weather/weather-slot-state-model.md) - the durable slot and the transition flag next to it
- [`weather-probability-and-transition-roll.md`](Weather/weather-probability-and-transition-roll.md) - how the slot is chosen, and when
- [`weather-apply-and-environment-materialization.md`](Weather/weather-apply-and-environment-materialization.md) - what applying a slot actually does
- [`mweather-resource-format.md`](Weather/mweather-resource-format.md) - the authored packed record
- [`call-chains/field-init-weather-to-legacyps2gs-rebuild.md`](Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md)

### [`Field-Record-Table/`](Field-Record-Table/) - ~~**documented**~~ **AUDITED** *(corrected 2026-10-02, OPUS: both pages' front matter says `status: AUDITED`)*

- [`field-record-bit15-action-permission.md`](Field-Record-Table/field-record-bit15-action-permission.md) -
  a per-area flag that decides whether characters with certain disabling statuses can still
  act. 65 callers across 13 subsystems, 17 in CombatAction. Found by audit, not by reading.
- [`field-record-table-navimapdata.md`](Field-Record-Table/field-record-table-navimapdata.md) - `navimapdata.bin`, the 3-byte field record and its seven accessors - **AUDITED** *(corrected 2026-10-02, OPUS: a page this list omitted, added with the status its front matter states)*

### [`Map-Pack/`](Map-Pack/) - ~~**documented 2026-09-12**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*

- [`the-map-ctrl-pack.md`](Map-Pack/the-map-ctrl-pack.md) - the 550 `.mpk` packs: a count of 32 and 32
  section sizes, split in place by `0036B980`, dispatched by `00378BC0` in two modes per field — sound
  bank, positional sound map, `YM00` world data, navigation, `ACTL`, lights, map pictures and their
  placements; the embedded `EFB0` is discarded for the loose `.efb`.

### Root pages (added 2026-10-02, OPUS)

- [`walking-into-an-authored-trigger-point.md`](walking-into-an-authored-trigger-point.md) - authored field trigger points - **AUDITED**
- [`CONTRACT-authored-trigger-points.md`](CONTRACT-authored-trigger-points.md) - **CONTRACT READY**
- [`choosing-the-field-environment-variant.md`](choosing-the-field-environment-variant.md) - the field environment variant - **AUDITED**
- [`CONTRACT-field-environment-variant.md`](CONTRACT-field-environment-variant.md) - **CONTRACT READY**
- [`CONTRACT-field-record-accessors.md`](CONTRACT-field-record-accessors.md) - **DIFFERENTIAL TESTED**
- [`CONTRACT-weather.md`](CONTRACT-weather.md) - **BEHAVIORALLY UNDERSTOOD**
- *(corrected 2026-10-02, OPUS: six root pages this index omitted, added with the status each page's own front matter states)*

### Not yet documented

- ~~MapRef root and auxiliary data layout~~ *(answered: `map_ref.bin` is decoded — choosing-the-field-environment-variant.md and CONTRACT-weather.md §3; 2026-10-02, OPUS)*
- ~~Field runtime parameter derivation (`002E3D40` zero-mode path)~~ *(answered: `002E3D40` read 2026-09-18 — choosing-the-field-environment-variant.md and Weather/mweather-resource-format.md; 2026-10-02, OPUS)*
- ~~The field environment table and target-local environment index resolution~~ *(answered: the environment index and its two tables — CONTRACT-weather.md §3 and CONTRACT-field-environment-variant.md; 2026-10-02, OPUS)*
- Area/zone identity and transitions

## Audit disposition, and a name recovered (repos-2d, 2026-09-03)

`audit_crossrefs.py` reported two **Script VM / native bridge** edges against this README, both
callers of the `002E3D40` path named in the list above. They are not unaccounted — they are two
authored script verbs, and they name the function:

| Call id | Verb | Args | Handler | Arity verified |
|---|---|---:|---|---|
| `0x0481` | **`setmapwind`** | 3 | `0034B6C0` | **3** `VMValueStack_PopInt32CoerceFloat32` calls, then `jmp 002E3D40` with `mode = 1` |
| `0x0482` | **`defaultmapwind`** | 0 | `0034BD10` | **0** pops; zeroes all four arguments and `jmp 002E3D40` |

So `002E3D40(mode, a, b, c)` is the engine's **map wind** entry point: mode 1 with three script
arguments sets it, mode 0 resets it to the field default. That is what the *"zero-mode path"* in
the bullet above is — the default-wind call, which
[the weather apply path](Weather/weather-apply-and-environment-materialization.md) tail-enters when
a field's environment is materialised.

**The name comes from the game's own script vocabulary, not from a reading of the body.** Both
handlers are arity-verified against the dispatch catalog, which is the bar
[`../01-Script-VM-Native-Bridge/`](../01-Script-VM-Native-Bridge/) requires before a verb binding
counts as fact.

**What the three arguments are** — `setmapwind(elevation, azimuth, preset)`, derived from the
register plumbing rather than from the field order, which is the reverse — is worked out in
[Weather/mweather-resource-format.md](Weather/mweather-resource-format.md)
§ *The script interface*.

*Disposition: explained. The Script VM edges are the authored interface to a function this
category documents.*

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Classes per [PASS22-WHAT-ACCOUNTING-MEANS](../_index/PASS22-WHAT-ACCOUNTING-MEANS.md) §4.2. Edges are from `edges.tsv`; a role is the ledger name unless a body is cited.*

**CoreRuntimeScheduling — MECHANICAL.** `0036B980` converts between image addresses and runtime pointers through
`ImageAddress_ResolveRuntimePointer` and `RuntimePointer_EncodeImageAddress`, the image's ordinary table-access pair.
The edge carries no world-state meaning.
- **Presentation - SERVICE (1 edge).** `002E3D40` reaches bodies filed to presentation: `0040AAD0` - shared machinery across the layer boundary, no shared ownership.
- **Script_VM_Native_Bridge - CLIENT and SERVICE (3 edges).** `002E3D40` is also called by bodies filed to script VM / native bridge: `0034B6C0`, `0034BD10`; `0034B6C0` reaches bodies filed to script VM / native bridge: `00267E10` - shared machinery across the layer boundary, no shared ownership.
