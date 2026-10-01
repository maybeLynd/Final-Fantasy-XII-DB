# Model and motion file formats

| ext | files | size | tree | note |
|---|---:|---:|---|---|
| `mot` | 4,392 | 2,552 MB | `ps2data/plan_master` | motion |
| `ca` | 3,164 | 632 MB | `ps2data/obj_finish` | |
| `cm` | 1,066 | 147 MB | `ps2data/obj_finish` | |
| `nmb` | 332 | 18 KB | `ps2data/plan_master` | **56 bytes per file** |
| `adm` | 39 | 109 KB | `ps2data/add_motion` | per-bone add-motion tables — **[explained](adm-add-motion-tables.md)** 2026-09-13 |

## The magic census changed this folder's premise — 2026-09-03

**`.mot` is `PKFL`, and so are `.snd`, `.vpc` and `.vpcjp`.** Twelve samples each, one signature
across all four: **10,314 files are a single container format**, split between what this folder
calls motion and what 18-Audio calls voice and sound.

> **So `.mot` is probably not a motion format at all — it is a package that happens to hold
> motion.** The premise of this folder was that motion is a format; the bytes say motion is a
> payload. **Splitting `PKFL` across two owning categories is now the thing that needs justifying,
> and one `PKFL` sheet should serve both** — `check_assets.py` enforces exactly that: a sheet
> explaining the layout must declare all four census rows.

**`.ca` and `.cm` are both `@FRP`** — one format, two extensions, 4,230 files. The 3:1 file ratio is
still the only hint about what distinguishes them, and it may distinguish nothing. *2026-09-11:*
[the container page](frp-object-container.md) §9 settles it at the entry level — `.cm` is a model
whose first entry is the `@FCP` parameter block ([decoded](fcp-character-parameter-block.md)), `.ca` a
motion set.

`.adm` is `04 00 01 00` and the binary names it `./PS2Data/add_motion/%s.adm` and `%s_town.adm`
(`008F…`), so the "additive motion" reading now has a **`_town` variant** to explain.
*2026-09-13:* [the `.adm` sheet](adm-add-motion-tables.md) walks all 39 by the parser's rules — tracks of groups of
28-byte per-bone records, loaded for the 23 stems in `add_motion_list.txt` (`hn1018_12.adm` is never loaded); the
`_town` twin is parsed but what selects it, and what the values mean, stay open (`MA-1`). *(MA-1 was answered on 2026-09-24 by SWE2-DATA: the record fields are decoded, and `_town` is the civilian variant, picked by a combat flag and an override. Noted 2026-09-26, FABLE, Claude Opus 5.5.)*
*2026-09-13:* the folder's two `.bin` files have [their own sheet](add-motion-skeleton-and-high-model-tables.md) — a
name-matched joint index list and a story-progress model replacement table, both loaded at start-up (`HM-1`).

*2026-09-15:* [the per-model oscillator subsystem](the-per-model-oscillator-subsystem.md) —
the `0040ACF0`/`0040D890` driver family under `Skeleton_UpdateFinalPoseAndCombatLook`, its
phase/perturbation record layout, three cost-tier transform paths, and the `0054B1F0`
parameter-install API (36 members).

*2026-09-28:* [the `@FEF` and motion-entry sheet](fef-and-motion-entries.md) — `@FEF` is a
0x30 header around a verbatim `EFX0010` whose only binder-path consumer is a `ret 0` stub;
the live spawn is name-keyed to external `chara\h*.efx` through `00409FE0`. `@FMC` carries
the weapon/treasure command names, `@FMN`/`@FMW` the 1:1 name/blend pair, `@FRM` the
`.ca`-only motion resource bound at `entry+0x378/+0x37C`.

> **`nmb` at 56 bytes per file is the most tractable unknown in the archive.** A 332-file corpus of
> apparently fixed-size records is the easiest possible thing to census, and small formats are where
> a corpus survey pays for itself fastest.

**Ownership is proposed from archive location.** These may belong to 04-Actor-Entity rather than
17-Presentation; a sheet decides that, this README does not.

Write sheets to `_templates/FORMAT.md`. See [_index/ASSET-FORMATS.md](../../_index/ASSET-FORMATS.md).

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**WorldAreaField — SERVICE.** `0040ACF0` on this page calls `FUN_001edcd0`, owned by that layer. What it reaches is a 203-byte area allowlist behind the same gate as the cutscene-override table: it takes the current area id and compares it against a hard-coded list - `0x190`, `0x294`, `0x37A`, `0x3E8`, `0x618`, `0x67C`, `0x6D1`, `0x6DC`, `0x712`, `0xFD2` and more - before doing anything; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).
- **Resource - SERVICE (8 edges).** `00409FE0` reaches bodies filed to Resource: `001D6EC0`, `002DF960`, ResourceTable_ResolveEntryByIndex (`002ED570`), `00409710` (+4 more) - shared machinery across the layer boundary, no shared ownership.

