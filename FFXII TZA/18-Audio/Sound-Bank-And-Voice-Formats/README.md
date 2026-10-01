# Sound bank and voice file formats

**The largest undocumented hole in the database by file count.** Audio has eleven documents and
2,064 owned functions — the engine is well read — and the files it eats had two passing mentions
between them.

| ext | files | size | tree |
|---|---:|---:|---|
| `sab` | 4,609 | 838 MB | `ps2data/sound` |
| `snd` | 2,304 | 146 MB | `ps2data/plan_master` |
| `vpc` | 1,809 | 1,240 MB | `ps2data/plan_master` |
| `vpcjp` | 1,809 | 1,298 MB | `ps2data/plan_master` |
| `seb` | 248 | 0.5 MB | `ps2data/sound` |
| `mab` | 116 | 1,312 MB | `ps2data/sound` |
| `spp` | 1 | 3 KB | `ps2data/sound` |
| `config` | 1 | 1 KB | `ps2data/sound` |

**Two observations that are findings before anyone opens a file:**

> **`vpc` and `vpcjp` occur 1,809 times each.** A strict pair — the same shape as EBP's `008`/`009`,
> which the EBP census established never appear alone. The English and Japanese voice sets are
> almost certainly the same container twice.

> **`mab` averages 11 MB per file against `sab`'s 182 KB.** Two orders of magnitude apart in the
> same directory: streams and banks, not one format with a wide size range.

## What the bytes and the binary added — 2026-09-03

| ext | signature | |
|---|---|---|
| `sab` | `sabf` | |
| `mab` | `mabf` | sibling naming, confirming the bank/stream split above |
| `seb` | `SeBl` | binary: `PS2Data\sound\se\block\se915.seb` — **SE block** — *explained 2026-09-12: [the SE block index](seb-se-block-index.md)* |
| `spp` | `SPP1` | binary: `sound/se/map/position_map/spp/env/env99.spp` — *explained 2026-09-13: [the map sound list](spp-map-sound-list.md)* — the per-field list of SE ids that `mapsoundplay`, the `SP1` emitters and the weather ambience index; 545 more ship inside `.mpk` slot 10 |
| `config` | `scnf` | *explained 2026-09-12: [the sound engine configuration](sead-win-config.md)* |
| `snd` · `vpc` · `vpcjp` | **`PKFL`** | **and so is `.mot`** |

> **The `plan_master` question above is answered, and not the way the folder assumed.** `snd`, `vpc`
> and `vpcjp` are not audio formats — they are `PKFL` packages, the *same container* as `.mot`.
> 10,314 files, one layout. **One `PKFL` sheet serves this folder and 17-Presentation both**, and
> `check_assets.py` refuses to let one be declared without the others.

**The PC build loads `.win.`-infixed audio.** The binary carries `.win.sab` (`00908998`),
`.win.mab` (`00908930`) and `.win.config` (`00906A38`), with real paths like
`PS2Data\sound\shout\us\shout00\shout00.win.sab`. **The remaster substitutes Windows audio assets by
filename convention** — a loader-contract fact a file corpus alone would never show, and the first
thing a `sab` sheet should nail down.

Write sheets to `_templates/FORMAT.md`. **Start with `sab`**: the engine half is already documented,
which makes it the cheapest sheet in the whole format plan. Order and rationale in
[_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md) §8.
