# Effect file formats

| ext | files | size | tree |
|---|---:|---:|---|
| `efx` | 3,288 | 4,368 MB | `ps2data/effect_finish` |
| `efb` | 410 | 216 MB | `ps2data/efb` |

**4.5 GB — the second-largest format family in the archive after `.phyre`**~~, and nothing in the~~
~~database describes either one~~. *(answered: see efx-and-efb-effect-containers.md; 2026-10-02, OPUS)*

**What the player sees:** every spell animation, every summon, every hit flash. This is the family
a modder reaches for to change what a Quickening looks like.

`efx` and `efb` sit in *different* directories, which is weak evidence against the obvious guess
that they are a container and its payload. ~~A sheet should settle that rather than inherit it.~~ *(answered: see efx-and-efb-effect-containers.md - two formats sharing one container convention; 2026-10-02, OPUS)*

Write sheets to `_templates/FORMAT.md`. See [_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md).
