# Prefetch lists and JSON data

| ext | files | tree |
|---|---:|---|
| `txt` | 10,253 | `prefetchdata/<lang>` — ~1,040 per language |
| `json` | 830 | `jsondata/maps` (459), `jsondata/cutscenes` (337), `jsondata/fontcluts` (28) |
| `csv` | 17 | `ps2data/soft_particle`, `jsondata`, `prefetchdata` |

**Both are readable text, which makes them the fastest win in the format plan** — and readability is
exactly why they stay undocumented. Nobody needs a sheet to open one; everybody needs a sheet to
know what the loader does with it.

**`prefetchdata` is a streaming hint system.** 10,253 files, roughly 1,040 per language. **What it
does for the player is hide loading**; what it does to a modder is decide whether a replaced asset
is even fetched.

**`jsondata` is this remaster's own addition** — `ps2data` contains no JSON at all. Maps and
cutscenes as authored data in a format a human can edit today makes these unusually high-value per
hour spent.

> **The `standard` disposition applies to the syntax only. JSON is a standard; the schema in these
> 830 files is not** — and the schema is the entire point.

## Measured — 2026-09-03

**`prefetchdata` is a per-scene asset manifest with a declared budget.** 9,351 entries, ~1,040 per
language across nine languages. Each file is a flat list of asset paths preceded by a header:

```
##Total_data_Size:_361_MB
./GameData/D3D11/ArtData/shaders/anisolighting.dds.phyre
```

**That size header is the interesting part.** It is an authored, per-scene data budget — observed
from 0 MB to 1,548 MB — and what a sheet must establish is whether the engine *reads* it (a
reservation) or merely records it (a build-time note). `common.txt` additionally carries category
sections: `##PhyreShader`, `##UI`, `##JSON`, `##OTHERS`.

**What this buys beyond format completeness:** it is a complete **asset → scene map** for the whole
game. Which files an area loads is otherwise only recoverable by watching the game run.

**`jsondata/maps` is a name oracle, not just data** — 459 files, 175 named rendering parameters, of
which **137 are literal strings in the binary**. That work belongs with the system it names:
see [17-Presentation-Rendering/Visual-Tuning-Parameters](../../17-Presentation-Rendering/Visual-Tuning-Parameters/README.md)
and the rule in [_index/EVIDENCE-STANDARD.md](../../_index/EVIDENCE-STANDARD.md).

`eventlist.csv` sits in the same tree and is a four-column integer table
(`274,0,240,0`) — unexamined.

Write sheets to `_templates/FORMAT.md`. See [_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md).

## `.ta` — explained 2026-09-12

[`ta-texture-animation-lists.md`](ta-texture-animation-lists.md): 45 CRLF text lists, one per animated
map texture — frame 0 plus `_pic_1` … `_pic_n` — discovered by counting `<map>_anime_0`, `_1`, … until the
first missing number, bound to already-loaded textures through `shared/phyremaps.txt`, and flipped by
the renderer through the material's `TextureSampler`.
