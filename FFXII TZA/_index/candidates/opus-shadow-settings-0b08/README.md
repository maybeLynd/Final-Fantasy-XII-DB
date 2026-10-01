# `ShadowSettings01F82EA8`: the 0xB08 shadow-settings object, declared (OPUS, 2026-09-26)

**Evidence class: NATIVE/STATIC.** This is a receiver-proven census plus instruction reads. No execution.

**Why.** `FABLE-REQ-OPUS-NAME-SCENE-LIGHTING-AND-SHADOW-FIELDS-FROM-JSON-KEYS` asked for field names on the 0xB08
object behind `001F0850` (cache `01F812C8`). The type store had **no type** for it.
- Its offsets coincide with `CPostEffect` rows only by chance. `CPostEffect`'s `+0x870` and `+0x890` are u64 fields
  written by its own methods, and it reaches `+0xD38`.
- So the object is declared here first, and its key-stored fields are then named.

## Identity

| item | value |
|---|---|
| allocation | `001F0869 mov ecx, 0xB08` → `operator new` `00210EC0` on the first call of the getter `001F0850` |
| constructor | `001EF2D0` (called at `001F0880`, 462 bytes) |
| cells | `01F82EA8` (the getter's own lazy cell). `0015CC00` re-caches the pointer at `01F812C8` |
| vtable | no install seen by any seed. Polymorphism is undetermined and not asserted |

## Census

`census_receiver_fixpoint.py` from all four applicable seeds, extent `0xB08`, unioned **by site**. The same instruction
reached by two seeds counts once.

| seed | file | converged | displacements |
|---|---|---|---|
| `call 001F0850` (the getter) | `census_call_001F0850.json` | yes | 224 |
| `ctor 001EF2D0` | `census_ctor_001EF2D0.json` | yes | 47 |
| `cell 01F812C8` | `census_cell_01F812C8.json` | yes | 21 |
| `cell 01F82EA8` | `census_cell_01F82EA8.json` | yes | 7 |

**Union: 227 displacements, 523 accesses.**

## Names

**The key → getter → store pairs.** `keystore_trace.py 1C3D50 2400` produces `keystore_trace_001C3D50.txt`. It pairs
each key-string `lea` with the next store after the getter call, in the cutscene-JSON loader `001C3D50`. The pairs agree,
site for site, with FABLE's independent reading.
- **14 fields are named from the keys.** Their widths are checked against the census. The three that the constructor
  touches with an 8-byte store (`+0xEC`, `+0x830`, `+0x83C`) are merged initialisations of two adjacent floats. The
  field stays 4 bytes; the merge is an access width.
- **`+0xFC..+0x104` `lightDirection`** is named from the weather page's D-4, which FABLE answered 2026-09-26: the scene's
  key-light direction. Its sense (towards or away from the light) is not established.
- **The rest** is census spans ("an unnamed stretch", with counts) or unobserved spans. A zero here is a lower bound,
  not proof of disuse.
- **Two 0xD8-periodic runs** (8 stretches from `+0x1C0`, 3 from `+0x8C0`) are **noted, not declared** as an element
  type. The first run's last stretch overlaps the dense `+0x800` region.

`build_rows.py` regenerates the 101 rows (tiling `0..0xB08`) from the files in this directory. Run with `--write`, it
appends them, and it refuses when the type is already declared.

**Not covered:** what the unnamed spans hold; the map loader's key set (`001C7xxx`); any execution.
