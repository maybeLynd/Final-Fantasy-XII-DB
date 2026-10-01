# Glossary

Engine terms as FFXII TZA actually uses them. Where a term has a formal native identity, the
address is given.

## Combat

| Term | Meaning |
|---|---|
| **BattleUnit** | A combat participant's runtime object. Process-local; **never** a network identity. |
| **BKBI** | The battle stats/state block carrying the two effect layers (`+0x68` mutable status, `+0x78` derived augment) and combat stats (Level `+0x1C2`, Strength `+0x2A`, Speed `+0x2D`, AttackPower `+0x2E`, Defense `+0x2F`). |
| **ActionDefinition** | Authored record describing an action. `+0x08` recipe ID, `+0x12` hit rate, `+0x13` element mask. |
| **Recipe** | One of **109** formula definitions at `0x01EF96C0`. Holds two calculator-slot lists: preview and committed. |
| **Calculator slot** | Index into the calculator function table at `0x01EFA5C0`. |
| **FormulaEvaluationContext** | Per-resolution context. `+0x1A` holds the **merged** effect bitmap (status OR augment). |
| **PARY** | The executable's own spelling of "parry" in outcome codes. Codes: 1 GUARD_WEAPON, 2 PARY_WEAPON, 3 GUARD_SHIELD, 4 PARY_SHIELD, 5 AVOID. |
| **Augment** | A derived automatic effect from equipment/passives/licences, living in BKBI `+0x78`. Equipment definitions store a raw `Augment` byte. |
| **Presentation slot** | A limited pool a committed action must acquire before its visuals play. Readiness feeds a 64-entry notification ring. |

## World

| Term | Meaning |
|---|---|
| **Weather Slot** | The durable per-area weather selection, `1..3` authored / `0..2` persisted at `payload+0x1060`. |
| **`weatherProbability`** | Authored per-slot chance the **current** slot survives the transition roll. Script header `+0x64`. |
| **MWeather** | Authored resource, 9 bits per (selector, Weather Slot): 3-bit preset, 4-bit azimuth, 2-bit elevation. Affects **both** visuals and combat. |
| **MapRef** | Authored map/area reference data the environment realization indexes. |
| **`bInitializationRestoreState`** | `payload+0x1061`. World-transition policy, **not** a weather flag. |
| **ActorManager** | Actor management record, stride `0x288`, index at `+0x28`. Index 0 is primary and is the only one that runs field-runtime weather/resource init. |

## Input / UI

| Term | Meaning |
|---|---|
| **Capability policy** | A shared 16-row x 32-bit inhibition table, OR-reduced by `002E0FA0`, deciding which player operations are allowed. |
| **UI request** | A numeric ID `1..24` posted to the native router `00254B50`, refusable by the capability policy. |
| **DecideButton** | Settings entry 25, values `Circle`/`Cross`, swapping the masks at `01E0C2A0`/`01E0C2A4`. |
| **Request mailbox** | The deferred request store `002E1B10` holding a pending request ID + parameter. |

## Audio

| Term | Meaning |
|---|---|
| **SEAD** | The sound engine's own name, from 159 authored `[sead]` diagnostic strings. Same engine as the `SQEX::Sd` RTTI namespace. |
| **HCA** | CRI Middleware's High Compression Audio. One of two decoded formats; output is 32-bit float. |
| **SAB / MAB** | SEAD container formats. `SABSOUNDSEQUENCEINFO` records hold sound candidates; the layout is versioned across at least three generations. |
| **Sequence** | A bound playback unit. States: 1 initialised, 2 armed, 4 invalid. |
| **Source voice** | `CoreSourceVoice` / `ExternalSourceVoice` — the rendering units below sequences. |
| **Meter / timing** | Music's bar/beat/tick system. `timing` is a 3-tuple converting bidirectionally with sample position. |
| **Lay** | SEAD's spatial layer — `PointSound`, `PolygonSound`, `DirectionSound`, `AmbientSound`. |

## Data / formats

| Term | Meaning |
|---|---|
| **VBF** | The game's archive, `FFXII_TZA.vbf`, 31 GB. Container magic **`SRYK`**; the developers' own term for it is *BigFile* (from the failure string `BigFile head wrong!`). **89,414 entries, 48 extensions.** Read with `agent_flow/tools/vbfextract.py`. |
| **EBP** | Compiled zone/event script container. **File magic is ASCII `EBP2`**; `0x8000000B` is a *section* marker inside it, not the file magic — the two were conflated in an earlier version of this entry. Decompile bytecode with `ff12-script.exe`. |
| **PKFL** | Package container behind **`.mot`, `.snd`, `.vpc`, `.vpcjp`** — one format, four extensions, 10,314 files. |
| **`st2e`** | The authored-table format. Ships **wrapped** inside carriers (`.ard`, `battle_pack.bin`), and lands at run time in the 63-slot authored-data registry. |
| **ScriptVM** | The VM running `.ebp` bytecode. Its verbs are **authored-intent evidence, never replay seams**. |
| **PSM** | PlayStation 2 GS pixel storage mode. `0x14`/`0x24`/`0x2C` are the 4-bit indexed family. |
| **GS** | PlayStation 2 Graphics Synthesizer. The PC port retains a 4 MiB local-memory / 8 KiB page model. |
| **VIF/VU** | PS2 vector-unit interface. The PC executable retains a genuine VIF command interpreter and UNPACK decoder. |

### The archive's four trees

`ps2data/` is the original game data carried forward · `gamedata/d3d11/` is what this remaster
added · `jsondata/` and `prefetchdata/` are also remaster-only. **A file's tree is the strongest
cheap signal of which subsystem owns it** — but it is a signal, not a proof: `.ker` and `.fex` sit
beside `.phyre` in `d3d11` and are font files, nothing to do with PhyreEngine.

### Container families — formats that hold other formats

| family | magic | directory | holds |
|---|---|---|---|
| **EBP2** | `EBP2` | 20 slots, **sparse** — 7 permanently zero | 13 section types; that sparseness is *how* the census found them |
| **PKFL** | `PKFL` | 16- or 64-slot, **dense** — indices 0–27 all used | motion, sound and voice payloads |
| **FF12AR03** | `FF12AR03` | — | `st2e` tables, one file per **area** |
| **`battle_pack.bin`** | 71-slot offset table | 71 slots | 37 `st2e` tables |
| **SRYK** (VBF) | `SRYK` | 89,414 entries | everything |

> **The engine reuses one container idea — a count followed by ascending offsets — in at least
> four places.** Similar shapes are a lead, not an identity: whether these are literally the same
> loader is unestablished.

### Every shipped extension

**Counts and magics are measured** (`archive-extension-census.tsv`, `format-magic-census.tsv`);
the *meaning* column is a mixture of established fact and marked leads. **Where it says "lead", no
reader has been named in the binary.**

| ext | files | magic | what it is |
|---|---:|---|---|
| `.phyre` | 35,984 | `RYHP` | PhyreEngine asset container — models, textures, shaders. Documented externally; cross-linked, not re-derived |
| `.txt` | 10,253 | text | **prefetch manifests** — per-scene asset lists under a `##Total_data_Size:_N_MB` budget header |
| `.ebp` | 10,045 | `EBP2` | zone/event scripts — cutscenes, map triggers, NPC dialogue |
| `.sab` | 4,609 | `sabf` | sound bank. PC build loads a **`.win.sab`** variant |
| `.mot` | 4,392 | `PKFL` | package holding **motion** — *not itself a motion format* |
| `.efx` | 3,288 | `EFX0` | effects — spells, summons, hit effects |
| `.ca` | 3,164 | `@FRP` | model data (`obj_finish`) |
| `.dat` | 2,948 | `himg`/`hdat` | image data, mostly menu |
| `.ah` | 2,564 | text `/Gam…` | **asset list** — e.g. `fontlist.ah`, `map/%s_srm.ah` |
| `.snd` | 2,304 | `PKFL` | package holding sound |
| `.vpc` / `.vpcjp` | 1,809 each | `PKFL` | voice packages — a **strict pair**, EN and JP |
| `.bin` | 1,439 | **7 signatures** | a bag: `sloc`, **`st2e`**, `FLAG`, `gmap`, `CCdd`, `hctg`. Includes `battle_pack.bin` |
| `.cm` | 1,066 | `@FRP` | same format as `.ca` |
| `.json` | 830 | text | **per-map render parameters** (175 named keys) and cutscene overrides |
| `.mpk` | 550 | `20 00 00 00` | `plan_master/map_ctrl` — **unknown**, 3 MB average |
| `.tm2` | 447 | `TIM2` | PS2 TIM2 image |
| `.efb` | 410 | `EFB0` | effects, second family |
| `.ard` | 332 | `FF12AR03` | per-**area** `st2e` carrier — *lead:* enemy status/attributes. **166 areas × 2 locale trees** |
| `.nmb` | 332 | `?? 00 64 00` | **strict pair with `.ard`**, ~56 B/file — index or name list |
| `.seb` | 248 | `SeBl` | SE block (`sound/se/block`) |
| `.mab` | 116 | `mabf` | music/stream bank — 11 MB average vs `.sab`'s 182 KB |
| `.mrp` | 116 | `MRP\0` | menu graphic |
| `.ta` | 45 | text `/Gam…` | asset list, same shape as `.ah` |
| `.mh` | 43 | `.mhe` | per-movie sidecar |
| `.webm` | 40 | `1A 45 DF A3` | **EBML/Matroska** — 10.4 GB, the largest thing shipped |
| `.adm` | 39 | `04 00 01 00` | `add_motion`, with a `_town` variant |
| `.ker` | 34 | varies | **font kerning** — extension string sits in the font block at `008F81FC` |
| `.cl2` | 20 | `CLT2` | UI localisation graphic (`Bin_Menu/Loca_*`) |
| `.as7` | 18 | `A7..` | UI silhouette graphic |
| `.csv` | 17 | text | small tables — `opt.csv`, `eventList.csv` |
| `.sav` | 16 | `FF12`/zero | save-related |
| `.fex` | 14 | varies | **font**, beside `.ker` in the binary's string block |
| `.btm` | 12 | `00 00 00 00` | **font bitmap** (`ExFont/font_stf_*`) |
| `.lst` | 9 | `qstl` | **quest menu list** — *not* a build artefact |
| `.nfs` | 9 | `TIM2` | **the same format as `.tm2`** |
| `.dbg` · `.msb` · `.sbn` | 8 each | varies | **unknown**, and no string in the binary |
| `.h` | 6 | text | C-style header text |
| `.ico` | 2 | `00 00 01 00` | **a real Windows ICO** |
| `.mg` | 2 | `10 00 00 00` | world-map mesh (`WorldMap/meshdata.mg`) |
| `.sys` | 2 | `PS2D` | PS2 `icon.sys` |
| `.tga` | 2 | `00 00 02 00` | title image |
| `.cnf` | 1 | `BOOT` | PS2 `SYSTEM.CNF` |
| `.config` | 1 | `scnf` | sound config; PC loads `.win.config` |
| `.spp` | 1 | `SPP1` | positional SE environment |
| `(none)` | 2 | — | extensionless entries under `ps2data/` |

### Two conventions worth knowing

**The `.win.` infix.** The PC build substitutes Windows audio assets by filename —
`shout00.win.sab`, `.win.mab`, `.win.config`. A file corpus alone never reveals this; it came from
strings in the binary.

**Locale trees.** Most `ps2data` content is duplicated per language (`us`, `jp`, `ch`, `cn`, `kr`,
`de`, `es`, `fr`, `it`, `in`, `uk`). **File counts therefore over-count logical units** — `.ard` is
332 files but 166 areas.

## Rendering / post-processing

Recovered 2026-09-03 from `TEXSHADERSET::CreateEffect` and the console's settings block. **These are
the game's own spellings**, not descriptions of them.

| Term | Meaning |
|---|---|
| **Yebis** | The post-processing middleware. Named by the engine's own `EnableYebis` setting, and the layer that owns the 325 shader techniques `TEXSHADERSET::CreateEffect` registers. One console dial switches the whole layer on and off. |
| **Alchemy SSAO** | The ambient-occlusion technique family, named outright in the shader technique table. Not a description — the engine's own name for it. |
| **FXAA 2** | The anti-aliasing family. The only AA family present. |
| **Bokeh** | A 40-technique family **separate from** the 63-technique depth-of-field family. **This game spends more shader variety on defocus than on anything else.** |
| **LOGRGB / REINHARDRGB / RGBALUM** | The three HDR tone-mapping encodings the technique table names. |
| **`fParam_FocusDistance`** | Shader uniform. The far end of `mDofFocusDistance`. **Name correspondence, not a traced dataflow.** |
| **`mDofFocusDistance` / `mDofApertureFnumber`** | Keys a scene author types into `JsonData/CutScenes/<name>.json`. Focus distance and aperture — the two parameters a depth-of-field effect needs. |
| **`*Obj`** | The render-command class suffix. 32 of them: `BegineSceneObj` (the engine's spelling), `PostProcessObj`, `AmbientOcclusionObj`, `ZBufferObj`, `EnableDofObj`, `ApplyJsonForCutSceneObj`, `ReadPresetDofForCutSceneObj`, and 25 more. |
| **`EnableYebis` / `EnableAO` / `EnableDof` / `EnableShadow` / `EnableIBL` / `AODepthFullRes` / `ShadowBias` / `ShadowValueB` / `ShadowValueG`** | Render-setting names carried as strings by five of the 25 functions that reference the settings block. **Naming the block is not naming its fields** — no verified name-to-offset binding exists yet. |

## Authored script vocabulary

**Verbs and names the game's own scripts and data use.** Every one of these arrived from authored
data rather than from a reading of a function body — which is why they are names rather than
descriptions.

| Term | Meaning |
|---|---|
| **`setmapwind` / `defaultmapwind`** | Script verbs, command ids `0x0481` / `0x0482`. `setmapwind(elevation, azimuth, preset)` — **argument order is the reverse of the packed record's field order**. `defaultmapwind` restores from the record for the current field and Weather Slot. |
| **`setforcefightmode`** | The script verb that names the flag at `01E0C2B8`. **R2 toggles it, and the polarity is inverted twice** — pressing it in the field *clears* force fight mode. |
| **`btlAtelCanselInitialSpawnFlag`** | Script primitive, bit 45. The engine's own spelling, misspelling included. Declares a placement non-initial; used by 167 zone scripts. |
| **`sum_` / `spc_`** | Cutscene asset-name prefixes that decide whether a scene gets a depth-of-field sidecar. **What they denote is not established** — the bridge is authored data in the VBF, not code. |
| **Developer tuning console** | 282 command ids, 226 arms, reached through one indirect jump. **A command id names the parameter, not the direction** — every stepping arm carries a step and its inverse. |


## GFZ project

| Term | Meaning |
|---|---|
| **GFZ / GZF** | The reconstruction project / the packed Ghidra archive that carries its state. |
| **PrimaryOwner** | V120 layer: which subsystem owns a state/resource/lifecycle transaction. |
| **CodeDomain** | V121 layer: what mechanism a function implements. Orthogonal to PrimaryOwner. |
| **FinalNoPrimaryOwner** | Deliberately owned by nobody. |
| **Explicit / unresolved** | Explicit = carries any of the three classifications. Unresolved = none. |
| **FAS2** | The `GFZANN2\0` binary annotation snapshot of all 38,161 functions. |
| **Residual** | The current unresolved address list. Must be regenerated after every mutation. |
| **Exact-current body fence** | Verifying a function's identity and body hash against the live parent before mutating it. |
| **PACK_PASS** | The token a valid pack must print. File existence alone is not a pack. |
| **Immutable drift** | Any change to a snapshot field other than `comment`/`tags`. Must be 0. |
