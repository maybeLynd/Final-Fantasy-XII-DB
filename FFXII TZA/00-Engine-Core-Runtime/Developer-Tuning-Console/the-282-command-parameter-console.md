---
system: The 282-command developer tuning console
category: 00-Engine-Core-Runtime
status: DOCUMENTED — UQ-22, UQ-23 and RC-4 are ANSWERED and every box on the page is closed (owner re-status 2026-09-30, OPUS) — what each of the 226 arms tunes answered 2026-09-27 (UQ-22: every block tunable is a named SceneWideParameterConstantBuffer variable); why ids start at 12 answered 2026-09-18 (UQ-23); the direction flag's source answered (001CD040 from the Config screen's direction argument); RC-4 answered: nothing in the image stores the capture machine's entry states 1 or 6, so a press on rows 4 or 5 cannot start a capture (ORACLE's rc4b record, one stated assumption) (status line current 2026-09-30, SWE2-CONTRACT)
owner_layer: CodeDomain:Presentation.Rendering.NativeSupport + InputBoundary
evidence_tier: 1
verified_against:
  gzf_sha256: 2ed8affb732f0def0a7852e0788298ae36b81206099dd1712f59825fc1c00bb9
  snapshot_sha256: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
last_reviewed: 2026-09-03
audit:
  passes: 1
  last_pass: 2026-09-03
  last_pass_state: 46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2
  crossref_clean: true
  reopened_count: 0
---

# The 282-command developer tuning console

> **The largest single function in the game is a command table**, and about half of what it does is
> nudge a number up or down by a hundredth.

`FUN_001D1660` is **13,753 bytes** — the biggest function in the executable that no document has
cited — and it is one `switch`. It accepts a command id, dispatches through a 282-entry table, and
runs one of **226** distinct arms.

## 1. What the player sees

**Nothing, on a retail disc.** This is the machinery a developer used while the game was being made:
a console that takes a numbered command and adjusts one setting a small step at a time.

Think of the way a lighting artist works. You do not type "set the shadow softness to 0.37"; you hold
a button and watch the value creep while you look at the screen. **Half the commands here are that
button** — each one steps a value by a fixed amount, most often **one hundredth**, from some value
the renderer, the audio mixer or the battle system is using *right now*. **Each of those commands
moves the value either way**, up or down, depending on a direction the caller supplies: the command
id names the *parameter*, not the direction. So it really is a button you hold, and holding it the
other way walks the value back (§11). Another quarter reach into a
subsystem and ask it to do something. A tenth flip a switch on or off.

**One of them sets your gil to 99,999,999.** That command is real, it is in the shipped executable,
and it is exactly one of two hundred and twenty-six — which is the honest way to describe it. It is
the single most recognisable thing in here and it is not what this system is *for*.

**Fifty-six of the numbered commands do nothing at all.** Their table slots point at the same
do-nothing arm as an out-of-range id. Those are the gaps of a tool that was edited for years:
commands that were removed, or numbers reserved and never filled in.

## 2. Native mechanism

### One indirect jump, at the top

The whole 13,753 bytes is reached through a single dispatch, seventy-eight bytes in:

```asm
001D166F  add    r9d, -0xC                          ; ids start at 12
001D167D  cmp    r9d, 0x119                         ; 281
001D1684  ja     001D4C09                           ; out of range -> the do-nothing arm
001D168F  lea    rcx, [rip - 0xB1696]               ; = 00120000, the image base
001D1696  movsxd rax, r9d
001D16A3  mov    r9d, dword ptr [rcx + rax*4 + 0xB4C1C]   ; table at 001D4C1C
001D16AB  add    r9, rcx                            ; RVA -> VA
001D16AE  jmp    r9
```

**The table is 282 entries of 4 bytes at `001D4C1C`, holding image-base-relative offsets**, and it
sits immediately *after* the function body (`001D1660`-`001D4C19`) rather than inside it. All 282
entries land inside the body. **Valid command ids are 12 through 293.**

`ja` before the table read means the bound is unsigned, so a negative id also falls through to the
do-nothing arm — at `001D4C09`.

### What the arms actually do, counted rather than sampled

The 282 entries resolve to **227 distinct targets**: 226 real arms plus one shared do-nothing arm at
`001D4BFA` that **56 ids** point at. Classifying each of the 226 by the instructions between its
entry and the next arm's:

| what the arm does | arms | share |
|---|---:|---:|
| **steps a float up or down** (`addss` *and* `subss`, one arm doing both) | **110** | 49 % |
| calls out to a subsystem | 63 | 28 % |
| other | 31 | 14 % |

*Reconciled with §10 (2026-09-30, SWE2-CONTRACT):* §10's catalogue counts `other 32` over 282 rows. The two agree: the catalogue's `kind` column has no separate row for this table's one *reads or stores a float without arithmetic* arm, so 31 + 1 = 32, and 110 + 63 + 32 + 21 = 226 real arms plus 56 `unimplemented` = 282 (`Tools/work/repos-d2/console_arms.tsv`, re-tallied 2026-09-30).
| writes a byte or flag | 21 | 9 % |
| reads or stores a float without arithmetic | 1 | — |

**The step sizes are the tell.** Ranked by how often the constant is referenced across the body:

```
 0.01  x88     0.02  x19     0.001 x13     1.0  x8      -1.0  x3
-0.01  x28     0.1   x18     0.05  x12    -0.05 x8      -0.03 x3
```

**A hundredth, referenced eighty-eight times, is what this function is mostly made of.** That is a
value being walked by hand while somebody watches the result.

### It reaches across the engine, through singletons

The 226 arms share a small set of helpers, and the most-used are singleton getters and a generic
setter:

*(CORRECTED 2026-09-29, OPUS, falsification pass 1 on the console contract; slice D §5.2 found it first: "used by" counted **call sites**, not arms. The arms that reach each helper follow in brackets.)*

| helper | size | used by | what it is |
|---|---:|---:|---|
| `001A9930` | 8 B | ~~45 arms~~ 45 call sites (14 arms) | `return *(void **)0x01F81168` |
| `00193D50` | 66 B | ~~33 arms~~ 33 call sites (16 arms) | lazy-constructs a `0x4A8`-byte object at `0x01F7F5F0` |
| `001DF340` | 10 B | ~~13 arms~~ 13 call sites (15 arms, through shared tails) | `((u32 *)rcx)[edx] = r8d` — a generic indexed dword store |
| `001DDAB0` | 8 B | ~~10 arms~~ 10 call sites (2 arms) | `return *(void **)0x01F82D18` |
| `001C2F40` | 8 B | ~~9 arms~~ 9 call sites (4 arms) | `return *(void **)0x01F81270` |

Seventy-nine distinct callees in all, and they are not one subsystem: the set includes an
`Audio`-owned function (`001DBB00`), a `Resource`-owned one (`002EEEE0`), and battle-side helpers
that read the battle-unit selector table at `02EBF190`. **A tuning console has to reach everywhere,
and this one does.**

### The gil command, in proportion

`Debug_SetGilToMaximum` (`003058B0`) is ten bytes:

```asm
003058B0  mov ecx, 0x5F5E0FF        ; 99,999,999
003058B5  jmp 00254EE0
```

It is called **once**, from one arm, out of roughly 250 call sites in this function. It is recorded
here because it is real and because it is the one command a reader will have heard of — not because
it characterises the system.

## 3. Key addresses

| Address | Working name | Body | Role |
|---|---|---:|---|
| `001D1660` | `DevConsole_DispatchCommand` | 13,753 B | the console: one `switch`, 282 ids, 226 arms |
| `001CD040` | — | 14 B | its only caller, a bounded adapter |
| `0017DB90` | — | — | one hop above `001CD040` |
| `003058B0` | `Debug_SetGilToMaximum` | 10 B | sets gil to `0x5F5E0FF`, tail-jumps |
| `001A9930` | — | 8 B | singleton getter, ~~used by 45 arms~~ 45 call sites, 14 arms (corrected 2026-09-29) |
| `00193D50` | — | 66 B | lazy singleton constructor, `0x4A8` bytes |
| `001DF340` | — | 10 B | indexed dword store, ~~used by 13 arms~~ 13 call sites, 15 arms (corrected 2026-09-29) |
| `001DDAB0` | — | 8 B | singleton getter, ~~10 arms~~ 10 call sites, 2 arms (corrected 2026-09-29) |
| `001C2F40` | — | 8 B | singleton getter, ~~9 arms~~ 9 call sites, 4 arms (corrected 2026-09-30 from the contract's falsification pass 1, D8, 2026-09-29) |
| `001DBB00` | — | 46 B | an `Audio`-owned callee |
| `002EEEE0` | — | 295 B | a `Resource`-owned callee |

### Data addresses cited by this document

| Address | Kind | Contents |
|---|---|---|
| `001D4C1C` | `.text` jump table | 282 dword image-base-relative offsets, the dispatch table |
| `008F30E4` | `.rdata` f32 | `+0.01` — the dominant step, referenced 88 times |
| `009002F4` | `.rdata` f32 | `-0.01`, 28 times |
| `008C5F6C` | `.rdata` f32 | `+0.1` |
| `008C5B2C` | `.rdata` f32 | `+0.001` |
| `01F81168` | `.data` ptr | the singleton ~~45 arms fetch~~ fetched at 45 call sites by 14 arms (corrected 2026-09-29) |
| `01F7F5F0` | `.data` ptr | the lazily-constructed `0x4A8`-byte object |
| `01F82D18` | `.data` ptr | a second singleton |
| `01F81270` | `.data` ptr | a third singleton |

## 4. Data structures and formulas

**Dispatch, exactly:**

```c
int DevConsole_DispatchCommand(void *ctx, u8 a, u8 b, int id)
{
    unsigned slot = (unsigned)(id - 12);
    if (slot > 0x119)                      /* unsigned: also catches id < 12 */
        goto do_nothing;                   /* 001D4C09 */
    u32 rva = ((u32 *)0x001D4C1C)[slot];
    goto *(void *)(0x00120000 + rva);
}
```

**The command-id space:**

```
valid ids            12 .. 293          282 slots
implemented arms                        226
slots pointing at the do-nothing arm     56
```

**The nudge form**, which 110 of the 226 arms take:

```c
*target += 0.01f;      /* or -= ; or 0.1f, 0.001f, 0.05f, 0.02f, 1.0f */
```

## 5. Call chain

```
0023B330 / 0023B6F0
  -> 0017DB90
     -> 001CD040          (14 B adapter, the only caller)
        -> 001D1660       THIS SYSTEM
           -> 79 distinct callees across Presentation, Audio, Resource and battle state
           -> Debug_SetGilToMaximum (one arm of 226)
```

**Upstream:** a single adapter, itself reached from two functions two hops up. The console has
exactly one entry point.

> **That entry point is now named, and it is not a developer one — 2026-09-08.** `0023B330` and
> `0023B6F0` are the **procs of two row objects in the retail Config screen**, and **16 of these 282 ids**
> (`0x86`, `0xA6`, `0x10A`, `0x110`-`0x119`, `0x11B`-`0x11D`; `0x10A` added 2026-09-13 — the list named fifteen) are driven by menu rows a player can reach with the
> stick. Every fact in this document stands; the *name* overstates. **This is a shipped parameter
> dispatcher that a debug arm happens to live in, not a developer console that ships by accident.** See
> [the Config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md).
>
> The reachability also needed an instrument this document did not use: **`001CD040` reaches `001D1660`
> by a tail `jmp`**, so `001D1660` has **zero `E8` call sites in the image**.

**Downstream:** everywhere. That is what makes it a console rather than a subsystem.

**Do not confuse with:** the ScriptVM command tables
([the dispatch table](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md)), which
are also id-dispatched but are *authored-script* entry points with a record per command and three
callbacks. This is one function with an inline jump table and no records at all.

## 6. Modding notes

- **The table is in `.text` and immediately follows the body**, at `001D4C1C`. Entries are
  image-base-relative offsets, so re-pointing a command means writing an RVA, not a VA.
- **56 slots are free** in the sense that they already point at the do-nothing arm — they are the
  natural place to attach a new command without growing the table.
- **The bound is `unsigned > 0x119` after subtracting 12.** Raising the command count means editing
  that immediate as well as extending the table.
- **Half the commands are `+= 0.01f` on some address.** If you want to know what a given parameter
  does, this function is a catalogue of which addresses the developers thought were worth tuning
  by hand.

## 7. What is not known

- [x] **UQ-22.** **What each of the 226 arms tunes.** The catalogue is extracted (§10) and the targets are
      **97 addresses in a 1,132-byte block at `02CB7FD0`**; none is named. This is the whole
      remaining question and it is now divisible.
      ***NARROWED 2026-09-17 (FABLE): every arm is named by its own label, and 34 of the 97 addresses are named or read; the other 63 are traced no further.** Two pages written since this box answer most of it: [the command-names page](console-command-names.md) carries the developer's label for all 282 ids (`Invincible`, `Use PS2 lighting`, `SSS Width` and so on), and the slices give each id the address its arm writes, so what an arm *tunes* is its label at its address for every arm. What the box still wanted is the address's own name and reader. The scene-config loaders `001C7940` and `001C3D50` store 44 addresses under string keys (the nearest `lea` into the key run `008FA700`..`008FAB00` before each store), 22 of them among the 97 (`EnableIBL` at `01DFE190`, the `Shadow`, `AO`, `Dof` and `lightShaft` families in the block); and a rip-target census over `.text` finds a reader outside the console `001D1660`, the menu renderer `001CD0E0` and the two loaders for 14 of the 97 (frame skip `01E02801` in `001E05F0`, anisotropic filtering `01F7E340` in `0017D000` and two more, SSS enable and width `02CB8434`/`02CB8438` in `006084B0`, the PS2-lighting and Fresnel bytes `01DFE190`..`01DFE194` in `001BD9D0` and `001F8D10`, and the rest in the table). Both together name or trace 34; the remaining 63 are written by the console and shown by the menu renderer and reach no other rip-relative reference, so a reader of theirs, if any, goes through a base register that this census cannot see. The per-address result is [`members/console-tunables-consumers.tsv`](members/console-tunables-consumers.tsv) (97 rows: arm ids, labels, loader key, outside readers). *Corrected the same day (FABLE, own error): the table's key column first took the nearest key string before each store and so mis-keyed most block stores (twenty-one inherited `EnableIBL`); it is now the key whose `lea` precedes the map lookup `001FF740` that precedes the store, one key per address, and every key matches its arm's label (`02CB80A0` `chrFresnelSpecularIntensity` under *Fresnel Specular intensity*, `02CB8080` `mMapAmbientColorCutPercent` under *Use PS2 lighting*). The counts, 22 keyed, 14 read, 34 named or read, are unchanged.* The render settings reading of the block itself is [the console-tunes page](what-the-console-tunes.md)'s. Static.*
      *Narrowed 2026-09-18 (FABLE): the 63 are traced after all — to the staged shader-constant buffer, not to a body.* The table's 83 rows with no outside reader split 80 inside the block and 3 outside it. **Every one of the 80 sits at `+0x004` .. `+0x17C`**, and that whole span lies inside the `+0x000` .. `+0x18F` range that [the console-tunes page](what-the-console-tunes.md) §4 reads `006084B0` staging sixteen bytes at a time into the constant-buffer object's `+0x110` (a base-register walk `base+0x00` .. `base+0xD0` and on, the very access shape a rip-relative census cannot see). So a tunable the console writes and no body reads by address is still consumed: it is copied whole into the constant buffer and read by whichever shader binds that buffer, which is GPU bytecode outside this image. The block is taken whole by four other routes, none of which indexes the 80 by name: `00607F00` stores the base into an object's `+0x98` (`00607F12`–`00607F19`), ~~the 12-byte getter `008AB7C0` returns it and has no listed caller~~ the 12-byte `008AB7C0` is no getter: it loads the base and tail-jumps `005DDDB0` (`008AB7C0+0x0` `lea rcx, [02CB7FD0]`, `+0x7` `jmp 005DDDB0`), and `00162410` passes its address to `00808B90` after constructing the block (`00162410+0xB` `call 005DC720`, `+0x10` `lea rcx, [008AB7C0]`, `+0x1B` `jmp 00808B90`) *(corrected 2026-10-02, OPUS: read at those instructions)*; and `00162410` passes it to `005DC720`, the constructor the console-tunes page reads as the initialiser of `+0x000` .. `+0x0C4`, `+0x0D0` .. `+0x180` and `+0x42C` .. `+0x468`, while `001A2130` and `001BC9D0` pass it to the 36-byte `0060B720`, not read here *(read 2026-09-30, OPUS owner read: `0060B720(object, fn)` appends the code pointer `fn` - `001A97F0` from `001A2736`, `001BD9D0` from `001BCC6C` - to a pointer vector at the object's `+0x1010` through the push-back `0060AB10`; it reads none of the tunables)*. The three outside the block — `01DFE1AC` (*SSS Diffuse a*, arm 169), `01F82ED0` (*IBL Diffuse limit*, arm 112) and `01F82EE4` (*SSS Diffuse b*, arm 170) — have no rip-relative reader and no base route found, and stay unread. What remains is not a code question: which constant slot each of the 80 becomes in the staged object, and which shader reads it. Static: the consumers table, a base-register trace over the eight bodies that take `02CB7FD0`, and the console-tunes page's copy map.
      **ANSWERED 2026-09-27 (OPUS):** each of the 80 becomes a named variable of the shipped shaders' SceneWideParameterConstantBuffer. The per-offset map is [members/scenewide-cbuffer-map.tsv](members/scenewide-cbuffer-map.tsv). The chain is read at each link. (1) 006084B0 (only caller 00604750) copies the block into a CPU snapshot at 00604750's rbp+0x270, block +X at snapshot +0x110+X. The snapshot is 0x598 bytes, change-checked by a 0x598-byte memcmp and double-buffered at owner +0x4E0, and it is NOT the GPU layout. (2) 00604750 then writes the GPU-layout buffer through r14, one field at a time, from that snapshot (294 store offsets, no two disagreeing about one offset). (3) Those offsets are the compiled SceneWideParameterConstantBuffer: one layout (0x5F0 bytes, 154 variables) in all 4,799 shader blobs that declare it (phyrechrshader.fx and phyredefaultlitshader.fx, from each DXBC's RDEF chunk). In the exe, the name is one entry of a name-to-code table (.rdata 00D3EC90 -> 00D3F850, codes 0x13 and 0x34). All 80 map, and the developer labels agree with the variable names: Map BGNPC Fresnel Intensity -> mapFresnelSpecularIntensity (cbuffer 0x188), the Map Eye/Hair families -> eMap*/hMap* (0x19C-0x1F4), the water factors -> mapWater* (0x1F8-0x214), Map IBL Diffuse Intensity -> mapIrrCubeMapIntensity (0x234), the character Fresnel/Hair/Eye A-B families -> chrFresnel*/hChr*/eChr*/xChr*/yChr* (0x238-0x2C4), and the character intensities -> chr* (0x2C8-0x2E4). The snapshot is reordered against the cbuffer in places: the hair camera-light XYZ precede the hair specular terms in the cbuffer, and the IBL intensity follows the ambient colour. Two labels name a different term than the variable: Map Eye Diffuse Modifier is written to eMapShdwMdifir, and Eye A and B Cube Map Blend Factor to eChrCubeMapIntensityModifier. The shadow tail agrees too: block +0x190.. becomes mShadowCascadeProjection0..7 (0x2F0..). The three tunables outside the block - SSS Diffuse a 01DFE1AC, IBL Diffuse limit 01F82ED0, SSS Diffuse b 01F82EE4 - are touched only by the console 001D1660 and the menu renderer 001CD0E0, by rip-relative and by any base leaned within 0x400 below them. They tune nothing this executable reads. Which pixel the shaders compute from each variable is GPU bytecode and not claimed. Control _index/candidates/uq22-scenewide-cbuffer/uq22_scenewide_map.py (K1 shadow matrices, K2 chrFresnel keys, K3 no conflicts, K4 80/80).
- [x] ~~What the four singletons at `01F81168`, `01F7F5F0`, `01F82D18` and `01F81270` are.~~ **Answered 2026-09-14
      (FABLE), from their own pages:**
      - `01F81168` is the `0x520`-byte map-art (`.ta` texture-animation) context
        ([ta lists](../../02-Resource-And-Asset-Pipeline/Prefetch-And-Json-Data/ta-texture-animation-lists.md);
        its size is corrected on [the game application page](../Application-Root/game-application.md)).
      - `01F7F5F0` is the lazily built `0x4A8`-byte post-process parameter context that all twelve passes take
        ([post-process passes](../../22-Middleware-PhyreEngine/Post-Process-Chain/the-post-process-passes-and-their-shader-constants.md), `EA-2`).
      - `01F82D18` is the `0x180`-byte display object `001DDAB0` returns
        ([the config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md)).
      - `01F81270` is `MultipleDebugDisplay` (`0x4670` bytes, by RTTI; [game application](../Application-Root/game-application.md)).
- [x] ~~Whether the console is reachable at runtime in the retail build, or only linked.~~ **Answered 2026-09-13
      (FABLE), statically:** the dispatcher `001D1660` has one way in: the three-instruction adapter `001CD040` tail-jumps to it (`001CD049`), `001CD040` has one call site (`0017DD34` in `0017DB90`), and neither address is held in any data qword. `0017DB90` — called only by the Config screen's two row procs (`0023B3D0` in `0023B330`, `0023B84C` in `0023B6F0`) — passes the id as a literal `mov r8d` in each of its arms, and the arms carry exactly **16** ids: `0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D`. So the other 266 ids — every developer arm among them — are linked but issued by no code in the retail image. A patched or injected call could still issue them; the image does not.
- [x] **UQ-23.** Why ids start at **12** rather than 0.
      *Narrowed 2026-09-14 (FABLE), not answered: ids 1–11 are rows of the same menu that this dispatcher does not handle.* The
      label filler `001D0390` stores strings for ids 1–11 as well. They are information rows and one-shot actions, not
      tunables:
      - 1 *"Current BG:"*, 2 (empty), 3 *"Toggle screen mode:"*, 4 *"Capture 4K (A Frame)"*, 5 *"Capture Series 4K Image"*;
      - 6 *"Flex mem:"*, 7 *"CutSceneInfo:"*, 8 *"Current pointing map object:"*;
      - 9 *"YEBIS DOF Info:"*, 10 *"YEBIS DOF Info (2ndScreen):"*, 11 *"Focus Distance Helper:"*.
      ***NARROWED 2026-09-17 (FABLE): an id is the row's index in the menu's label array, and the table starts at 12 because rows 0..11 are not arms.** The label filler `001D0390` stores each row's string at the menu object's `+0x130` plus eight times the id (`001D04E7`..`001D0534`: id 1 `Current BG:` at `+0x138`, id 2 the empty string at `+0x140`, id 3 `Toggle screen mode:` at `+0x148`, ids 4 and 5 the two captures at `+0x150` and `+0x158`), the same slots the ids of 12 and above occupy, so the id space is one array of 294 rows and the dispatcher's `add r9d, -0xC` (`001D166F`) simply skips the first twelve. Those twelve carry no arm: the console's single caller `0017DB90` is the Config screen's row handler, a 23-way jump table (~~`0017DBC2`..`0017DBDE`~~ read at `0017DB90+0x44`) whose cases forward ids of 12 and above (~~`0x86`, `0x10A`, `0x110`..`0x11D`~~ `0x86`, `0xA6`, `0x10A`, `0x110`..`0x119`, `0x11B`..`0x11D`) and none below *(corrected 2026-10-02, OPUS: the `mov r8d, imm` set of `0017DB90`, e.g. `0017DB90+0x55` `mov r8d, 0x11b`; no `0x11A`; `0017DB90+0x2F`–`+0x4E` is the switch code, not its table)*. The action a low row suggests lives elsewhere: the screen-mode change is arm 263, `Game Window Mode:` (`001D45E9`, the string `Screen Mode Change by Debug Menu !!!` at `001D462D`), and the capture file names (`Capture 4K/capture%03d.tga`, `capture_series%03d_%04d.tga`) sit beside the render pass list's `output capture 4k images` string that only `00187950` references, so the captures run in the render pass list, not in an arm. What is not found is the handler that turns a press on rows 3..5 into those actions: it is neither in `001D1660`, which subtracts 12 first, nor in `0017DB90`; ~~a rip-target census finds no code reference to the two capture strings at all.~~ **Corrected the same day (FABLE, own error): the census had looked one byte past the strings' starts.** The names begin with a slash at `008C5EC0` (`/Capture 4K/capture_series%03d_%04d.tga`) and `008C5EE8` (`/Capture 4K/capture%03d.tga`), and both are referenced by `001876E0` (`00187728`, `0018774E`), the name builder of the render pass list's capture state machine `00187860` (its one caller), which runs only while the render object's byte `+0xDB8` is set and steps the object's `+0xDAC` through states that write the series name when the state is 7 and the single name otherwise (`00187714`); `/capture.tga` at `008C5EB0` is the pass list's own path (`00187550`). So rows 4 and 5 are performed by the render pass list's capture machine, and [the frame page](../../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md)'s one-shot capture modes 4 and 6 are the switches. Still not found: what starts the machine from a row press. `+0xDB8` has one writer, the object's constructor `00184F20` (`0018502B`), and `+0xDAC` is written only by the constructor and by the machine itself, so the press reaches it through a field this scan does not see. Static.*
      ***ANSWERED 2026-09-18 (FABLE) — because no caller ever presents an id below 12: rows 1–11 are label rows the menu draws, and the arm table begins at the first row that has an arm.** The dispatcher has one route in: the 14-byte adapter `001CD040` (`jmp 001D1660`, `001CD049`), whose only caller is `0017DB90` (§5), itself called from `0023B330` / `0023B6F0`. `0017DB90` switches on its own case index — `lea eax, [rbp-1]`, `cmp eax, 0x16`, a 23-entry table (~~`0017DBBF`..`0017DBDE`~~ read at `0017DB90+0x44` by `mov ecx, dword ptr [rdx+rax*4+0x5dd5c]`) *(corrected 2026-10-02, OPUS: `0017DB90+0x2F`–`+0x4E` is the switch code)* — and the ids it loads into `r8d` before the call at `0017DD34` are exactly sixteen: `0x86`, `0xA6`, `0x10A`, `0x110`–`0x119`, `0x11B`–`0x11D` (image read: the `mov r8d, imm` set of the body), every one at or above 12. So ids 1–11 never reach `add r9d, -0xC`; they exist only as rows of the menu's label array, where `001D0390` stores their strings (*Current BG:*, *Toggle screen mode:*, *Capture 4K*, the YEBIS DOF readouts, *Focus Distance Helper*), and the dispatcher's index space starts at 12 because that is the first row with an arm to run. What the information rows display is the menu's draw path, and what the two one-shot rows do when pressed lives outside this dispatcher — not a part of this question. Static: the adapter, its one caller, the caller's id set.*

      In `001D1660`, an id below 12 becomes a large unsigned value after `add r9d, -0xC`, fails `cmp r9d, 0x119`, and takes
      `ja 001D4C09`, the exit. So the table starts at the first adjustable row. Which code serves rows 1–11 was not traced.
      *Now traced as far as the image allows (2026-09-30, SWE2-CONTRACT, citing the ANSWERED paragraph above):* rows 1–11 are label rows the menu renderer draws; the captures of rows 4 and 5 are performed by the render pass list's capture machine `00187860`. What turns a press on those rows into that machine is the remaining residue and is registered below as RC-4.
- [x] **RC-4.** What turns a press on the console's capture rows (4 *Capture 4K (A Frame)*, 5 *Capture Series 4K Image*) into the render pass list's capture machine `00187860`: the render object's gate byte `+0xDB8` has one writer, the constructor `00184F20` (`0018502B`), and `+0xDAC` is written only by the constructor and the machine itself, so the press reaches it through a route a displacement scan does not see. Registered 2026-09-30 (SWE2-CONTRACT).
  *Narrowed the same day (static, OPUS's record [`rc4-capture-machine-0930`](../../_index/candidates/rc4-capture-machine-0930/README.md)):*
  the machine `00187860` runs every frame once `+0xDB8` is set; it idles at state 0, and a capture needs `+0xDAC` = 1
  (single: 1 → 3 → 4 → 0) or 6 (series: 6 → 7 → 7). A byte-pattern census of every `0xDAC` displacement and immediate
  finds render-object writes only in the constructor (0) and the machine itself (3, 4, 0, 7), and no store starting at
  `+0xDA5`..`+0xDAB` covers `+0xDAC`. So **the entry states 1 and 6 have no direct writer**, and by every directly visible
  write form a row press cannot start a capture, consistent with UQ-23. Still open, and static: a write through a
  pointer the render object hands out at another offset.
  *Round 3 (records) RC-4:* **ANSWERED 2026-09-30 (static; SWE2-CONTRACT on SWE2-ORACLE's `_index/candidates/rc4b-capture-residue-0930/`, `be7c6fcd6`, five scripts, FAILS 0):** no store reachable from the render object writes `+0xDAC` other than the constructor's 0 (`00185020`) and the machine's own 3, 4, 0 and 7, so nothing writes the entry states 1 or 6 and a press on rows 4 or 5 cannot start a capture. OPUS's four blind classes are closed: the 66 unknown-offset stores reach at most `A+0xCB0`; the self-pointer fields are modelled to a fixpoint (0 new writers); the virtual calls are resolved or seeded (0 new); the two escapes are rooted (0 new). Assumption 1 closed by OPUS in the same record: `[A+8]` is `app+0xE8`, a `Phyre::PRendering::PRenderer` (`00D49930`, base `PRendererBase` `00D498F0`), slot 2 `00600D20` under either class. **Assumption 2, stated:** the readers of `ext+0xA8` all lie in `00600000`-`00620000` (no whole-image value flow from every holder of `ext`). Also stated: the flow's depth limit (12; 916 cuts, none carrying the object); external writes (debugger or mod). Reviewed ACCEPT-WITH-NARROWING by SWE2-AUDIT-SPEC (`_index/candidates/auditspec-review-rc4-5-25-30-0930/`, `ccd10c206`): a raw `.text` sweep independent of the function list re-finds every `+0xDAC` store and none writes 1 or 6; the narrowing is wording only, the `+0xCB8` index writers are function-list-wide, and the one unlisted store (`00707657` in the leaf `00707610`) is on the object held in `[02EA0B70]`, not the render object, so RC-4 stands. *Narrowed earlier the same day on OPUS's `rc4-capture-machine-0930` (`ae79ff1b5`).*

## 8. Evidence

| Claim | Evidence | Tier |
|---|---|---|
| 13,753 B, the largest uncited function | ledger extent; uncited-function census | 1 |
| one indirect dispatch, ids 12-293 | complete disassembly of the head: `add r9d,-0xC` / `cmp r9d,0x119` / `ja` / table read / `jmp r9` | 1 |
| the table is at `001D4C1C`, 282 dword RVAs, all landing in-body | decoded from the image; 282 of 282 in `001D1660`-`001D4C19` | 1 |
| 226 distinct arms, 56 ids sharing a do-nothing arm | distinct-target count over the decoded table | 1 |
| 110 of 226 arms add or subtract a float step | each arm's instruction range classified between its entry and the next arm's | 1 |
| the step constants and their frequencies | RIP-relative `.rdata` operands over the whole body, read as f32 | 1 |
| helper usage counts | call-site census over the body | 1 |
| `Debug_SetGilToMaximum` is one arm | complete 10-byte body; **one** call site in this function | 1 |
| the console reaches Audio, Resource and battle state | the 79 callees' ledger owners; `00305A00` reads `02EBF190` | 1 + 11 |

**A naming hazard, recorded because it nearly happened.** The first callee list surfaced
`Debug_SetGilToMaximum`, and "the debug menu" is an inviting name for a function that contains it.
It would have been **true and misleading**: that command is one call of roughly 250, and the
measured shape of the system is parameter tuning, not cheats. **The name here is drawn from the
distribution, not from the most recognisable member.**

## 10. The arm catalogue, and the block it tunes

The frame in §2 makes the remaining work divisible: every id maps to one arm, and each arm is a
few instructions. **All 282 rows are extracted** to
`Tools/work/repos-d2/console_arms.tsv` as `id / arm / kind / step / data_touched / calls`, so what is
left is interpreting targets rather than re-deriving the frame.

```
kinds     nudge 110 | call 63 | unimplemented 56 | other 32 | flag 21
arms naming at least one .data address        112
arms with a step constant recovered           111
```

### The parameters live in one block

The arms touch **97 distinct `.data` addresses**, and **86 of them fall in one span**:

```
02CB7FD0 .. 02CB8438      1,132 bytes
81 of the 85 gaps between consecutive targets are exactly 4 bytes
```

**A densely packed array of 4-byte values**, in the zero-filled tail of `.data` — no file image, built
at run time. The hottest single address is `01F82D20`, ~~nudged by~~ dereferenced by **18** different commands *(corrected 2026-10-02, OPUS: the slot is only loaded, 24 times in `001D1660`, e.g. `001D1660+0x12C3`; its one store is at `+0x1C1` of a 2,153-byte Phyre framework body)* (18 rows of `console_arms.tsv` name it in `data_touched`, re-counted 2026-09-30; it is the `GameSettingConfig` singleton pointer, [what the console tunes](what-the-console-tunes.md) §7).

**And it is not the console's private scratch space.** Twenty-eight functions reference that span *(reproduced by OPUS's falsification pass 1 of [what the console tunes](what-the-console-tunes.md), 2026-09-12: 28 with any rip-relative reference, 4 of them taking only the address, 24 accessing it)*:
the console and **twenty-seven others**. So the commands are adjusting values the engine is already
reading elsewhere — which is what makes this a tuning console rather than a debug display.

**Three of the 88 nudged addresses are driven both up and down** by different commands
(`02CB8130`, `02CB8134`, `02CB8138`), the up/down pair a tuning UI implies. That only three show it
is a limitation of the extraction below, not a finding about the data.

### What the catalogue does not establish

- **The `step` column is indicative, not verified per row.** It records the first float operand of an
  `addss`/`subss`/`movss`/`mulss` in the arm and signs it by that mnemonic. An arm that loads a
  constant before stepping by a different one will be mis-signed or mis-valued. **The `kind` column
  is sound** — it rests only on whether `addss`/`subss` appears.
- **What any individual parameter *is*.** 97 addresses, none named *(answered: see the ANSWERED 2026-09-27 (OPUS) note, each becomes a named shader-constant variable; 2026-10-02, OPUS)*. This is the open question and it
  is the bulk of the remaining value. *Answered since (2026-09-30 pointer, SWE2-CONTRACT): every arm is named by its
  label ([console command names](console-command-names.md)), and UQ-22 (ANSWERED 2026-09-27, OPUS, §7 above) maps
  each of the 80 block tunables to a named variable of the shipped shaders' `SceneWideParameterConstantBuffer`
  ([`members/scenewide-cbuffer-map.tsv`](members/scenewide-cbuffer-map.tsv), control
  `_index/candidates/uq22-scenewide-cbuffer/uq22_scenewide_map.py`, tier 1 + shipped shader data); the three outside
  the block tune nothing this executable reads.*
- The 32 arms classified `other`, which by construction are the ones the classifier had nothing to
  say about. *Answered since (2026-09-30 pointer, SWE2-CONTRACT): each is catalogued per id, with its field,
  mechanism and bound, in the nine arm-catalogue slices (A–I, all boxes closed); for example slice B's UQ-10 finds
  that its twelve `other` arms touch fields of objects other than the console's own
  ([slice B](arm-catalogue-slice-B-ids-44-75.md)). Tier 1.*

## 9. Related

- [`../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md`](../../01-Script-VM-Native-Bridge/scriptvm-native-dispatch-table.md) — the other big id-dispatched command system, and a contrasting design
- [`../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md`](../../99-Unresolved-Residual/Unowned-Code-Census/why-the-unowned-code-has-no-owner.md) — the census that identified this function as the largest uncited one

## 11. Falsification pass 2026-09-03 (repos-2d) — first pass, by a session that did not write this

Run against snapshot `46f02e26104e44215f8793700fe95fc243394d6b966b366e74f16110627bbbb2`,
parent `2ed8affb…`, embedded EXE `73461d08…`. The dispatch table, the arm extents and every step
below were re-derived independently of `console_arms.tsv`, then compared to it.

**Attacked first: the extraction, because nine slices are about to be built on it.** §10 flags its
`kind`/step columns as unreliable. The measured asymmetry was worse than "unreliable" and turned
out to have a single clean cause.

### OVERTURNED — every stepping arm is **bidirectional**, and the document reads as though each is one direction

§1 says *"each one adds or subtracts a fixed step"* and §2's table counts **110** arms that *"add
**or** subtract"*. A reader takes that as one command to raise a value and another to lower it.
**Every one of them does both.** The complete arm at `001D1FB0`:

```asm
001D1FB0  movss xmm0, [02CB8140]      ; the parameter
001D1FB8  test  bl, bl                ; <- a direction flag, in a register
001D1FBA  je    0x1d1fd1
001D1FBC  subss xmm0, [008F30E8]      ; 0.05  -> decrement
001D1FC4  movss [02CB8140], xmm0
001D1FCC  jmp   0x1d4bfa
001D1FD1  addss xmm0, [008F30E8]      ; the SAME 0.05 -> increment
001D1FD9  movss [02CB8140], xmm0
001D1FE1  jmp   0x1d4bfa
```

**102 of 102** fixed-step arms have this shape — a `test` on a register flag, then a `subss` and an
`addss` against the *same* constant. Not one arm steps in a single direction.

So the console is **one command id per tunable parameter**, with direction supplied as a second
input — which is a better fit for §1's own "hold a button and watch the value creep" than the
reading the text currently invites. Held one way the value falls, the other way it rises, and the
command id names the *parameter*, not the direction.

**The sign composes from two sources, never one.** A step is negative if the mnemonic is `subss`
**or** the constant is itself negative — the pool holds ~~`+0.01` at `009002BC`~~ `+0.01` at `008F30E4` (`009002BC` holds `+0.02`) *(corrected 2026-10-02, OPUS: the floats read from the image)* and `-0.01` at
`009002F4` as separate floats. Signing by mnemonic alone, or by constant alone, is wrong in
opposite halves of the data:

| | count |
|---|---:|
| `addss` of a **positive** `0.01` → increment | 58 |
| `subss` of a **positive** `0.01` → decrement | 30 |
| `addss` of a **negative** `0.01` → decrement | 28 |
| | **58 up, 58 down** |

*(Independently confirmed: session `repos-d2` reached the same three figures from a constant census
over the function body, an instrument that does not walk the dispatch table at all. Two methods,
same three cells. What that census cannot do is attribute constants to **arms** — the next table
does that, and it changes the reading.)*

The step census, with the sign composed, is exactly symmetric — which is the same fact seen from
outside:

| step | + | − | | step | + | − |
|---|---:|---:|---|---|---:|---:|
| 0.01 | 58 | 58 | | 0.03 | 3 | 3 |
| 0.02 | 11 | 11 | | 1.0 | 2 | 2 |
| 0.05 | 10 | 10 | | 0.005556 | 1 | 1 |
| 0.1 | 9 | 9 | | 0.5 | 1 | 1 |
| 0.001 | 7 | 7 | | **total** | **102** | **102** |

### Per-arm attribution — 58/58 is **58 arms**, not 58 up and 58 down

Walking the 282-entry table and attributing every step to its arm:

| step magnitude | arms | | step magnitude | arms |
|---|---:|---|---|---:|
| 0.01 | **58** | | 0.03 | 3 |
| 0.02 | 11 | | 1.0 | 2 |
| 0.05 | 10 | | 0.005556 | 1 |
| 0.1 | 9 | | 0.5 | 1 |
| 0.001 | 7 | | **total** | **102** |

**Each of those arms carries the step and its inverse.** So "58 positive and 58 negative `0.01`
steps" is **58 commands that each move a value either way**, not 58 raise-commands paired with 58
lower-commands. A census of constants cannot tell those apart; only the table walk can.

**The magnitude is the property of the arm. The sign is not.**

### The extraction defect, diagnosed

`console_arms.tsv`'s step column reads **58 × `-0.01` and no `+0.01`**, and likewise `-0.02` ×11,
`-0.05` ×10, `-0.1` ×9, `-0.001` ×7, `-0.03` ×3 with no positive counterparts. **Those counts are
exactly the negative column above.**

The extractor records **one step per arm and takes the first**, and in every arm of this shape the
`subss` is emitted first. So the values are real, the arms are correctly identified, and **the sign
is an artifact of instruction order rather than a fact about the arm** — every row that reads
`-0.01` describes an arm that also adds `0.01`, on the branch the extractor never reached.

**Consequence for the nine slices:** a slice reading that column will describe every parameter as
decrement-only. The column is not wrong about *which* arms step or *by how much*; it is wrong about
*direction*, for all 102, in the same direction.

### Reconciled — 102 against the TSV's 110, and both instruments have blind spots

My set is a strict subset of the TSV's `nudge` set: 102 in both, **0** found by me and not by it.
The 8 remaining `nudge` arms are real nudges my rule missed, and reading two of them shows why:

- **`001D1867`** is bidirectional in the same way, but selects the sign by loading `+1.0`
  (`01CEBBA8`) or `-1.0` (`01CEBC9C`) into the register and then doing **one** `addss` against the
  *parameter* — `addss xmm0, [rdi + 0xcf4]`. The step is in the register and the parameter is the
  memory operand: the reverse of the common pattern, so a rip-relative-constant rule cannot see it.
- **`001D3CBD`** computes its step: an int at `[rdi + 0xc58]`, divided by 5 through the usual
  magic-number sequence, converted to float and scaled by `0.002`. That is a **scaled** step, not a
  fixed one, and arguably a third category rather than a nudge.

**Both extractions are blind to what the other catches** — mine to sign-by-constant and computed
steps, theirs to the second branch. Together they account for all 110.

### CORRECTED — `001D4BFA` is the shared epilogue, not only the do-nothing arm

§2 introduces `001D4BFA` as *"one shared do-nothing arm … that **56 ids** point at"*. The 56 is
right. But **212 of the 226 real arms jump to `001D4BFA` when they finish** — every stepping arm
ends there. It is the function's common tail, and a reader told only that it is the no-op target
will misread the 212 jumps as 212 commands doing nothing.

### Population note — two different censuses of the same constants

§2's ranked list (`0.01 x88`, `-0.01 x28`, …) counts **references to `.rdata` floats across the
body**; the table above counts **steps applied by arms**. They are different populations and should
not be reconciled: a single arm references its constant twice (once per branch), and other
instructions reference the same floats without stepping. The `-0.01` pool entry at `009002F4` being
referenced 28 times is consistent with arms that step by `addss` against a *negative* constant —
the `001D1867` shape — rather than with 28 decrement-only commands.

### What was not attacked

The 282-entry table read, the 226/227/56 counts, the singleton-helper analysis in §2, the gil
command, and §10's parameter-block claims (the 1,132-byte run and its 28 readers) were re-derived
only where they touch the arms above. The table bound, the arm extents and the do-nothing count
*were* reproduced exactly: 282 entries, 227 distinct targets, 56 ids at `001D4BFA`.

### Status

`audit.passes` 0 → 1. **Status stays `PARTIAL`.** §7's open items stand, and the bidirectional
finding adds one: what supplies the direction flag — the register differs between arms (`bl`,
`sil`), so it is an argument to the console, and this pass did not trace its caller.
*Answered since (2026-09-30 pointer, SWE2-CONTRACT):* the one way in, the 14-byte adapter `001CD040`, computes
`r8b = (dl == 0)` and tail-jumps to the dispatcher (`test dl,dl / mov r9d,r8d / sete r8b / jmp 001D1660`), and its
only caller `0017DB90(row, currentValue, direction)` is the Config screen's row handler, called with the left/right
direction of the press ([slice B](arm-catalogue-slice-B-ids-44-75.md)'s caller box;
[the config screen](../../16-UI/Config-Screen/the-config-screen-and-what-a-setting-change-runs.md), AX-6a). Tier 1.

## 12. Cross-subsystem neighbours — disposition (repos-2d, 2026-09-03)

§11 declared this document `crossref_clean: false` and said dispositioning was a separate job. This
is that job. All five findings arrive through **three** cited addresses, and one of them is worth
more than a disposition.

### The gil command uses the ordinary money path — which is why it works

Four of the five findings (**CombatAction** 3, **CombatFormula** 1, **Rewards/Progression** 5, and
one **achievements** edge) are the caller census of a single cited address: `00254EE0`
`GameState_SetGil`.

**13 callers across 5 owner subsystems** — Items/Equipment/Shops 4, Rewards/Progression 4,
Combat Action 3, Combat Formula 1, unowned 1. No document enumerates it, so the census is stated
here rather than deferred.

§1 describes the gil command as *"the single most recognisable thing in here and not what this
system is for."* The census sharpens that: **the console does not have a gil cheat, it has a call to
the same setter shops, battle rewards and the defeat/loot path all use.** It is one caller of
thirteen. That is why the command works at all — it is not writing a variable behind the game's
back, it is asking the money system to set money.

**And it is not invisible.** `GameState_SetGil` calls an achievement counter in
Platform/Online/Achievements, which is the fifth finding. The achievement catalogue documented
elsewhere in this database includes a gil-total counter; a developer setting gil through this
console therefore moves the same bookkeeping a player's gil would. *(The edge is recorded; what the
counter does with the value is that document's to say, not this one's.)*

*Disposition: `GameState_SetGil`'s own neighbourhood, stated. Not console relationships — the
console is one caller among many, which is the interesting part.*

### The other two

**`001DF340`** (10 B) has **15 callers, 14 unowned and one in Platform/Online/Achievements**. A
ten-byte helper with fifteen callers is a shared accessor; its Platform and achievements callers are
its own neighbourhood, not the console's. *Disposition: shared-helper neighbourhood.*

**`00305A00`** (170 B, three callers, all unowned) reaches a battle-stats slot accessor in Combat
Formula and a second achievements counter. Those are the callees of one arm doing its own work —
this arm reads a battle stat and touches achievement bookkeeping because that is what the parameter
it tunes belongs to. *Disposition: arm-local callees, explained.*

### Method note

Three addresses produced five findings across four subsystems, and **two of the three are shared
accessors rather than console machinery**. That is the hub-import effect on a document whose subject
legitimately reaches everywhere: a 13,753-byte function that tunes values across the engine will
cite other subsystems' entry points by construction, and each citation brings its census.

The one that mattered — `GameState_SetGil` — was worth enumerating precisely because the census
*changes the reading of §1*. The other two are neighbourhood and are named as such.

### BODY DRIFT corrected — `001C2F40` is 8 bytes, not 9

`audit_crossrefs` reported a body-size disagreement, and the binary settles it:

```
001C2F40  48 8b 05 29 e3 db 01   mov rax, [rip + 0x1dbe329]   ; 7 bytes
001C2F47  c3                     ret                          ; 1 byte
          cc cc cc …             padding (the 9th byte on)
```

**Eight bytes.** The ledger says 8, the disassembly says 8, and the ninth byte is `int3` padding.
Corrected in both places it appeared.

**The rest of the table was checked rather than assumed** — `001A9930` 8 B, `00193D50` 66 B,
`001DF340` 10 B, `001DDAB0` 8 B all match the ledger exactly, as do `001D1660` (13,753) and the
other cited helpers. The error is isolated, not systematic, and its likely origin is visible in the
row: the size column and the "9 arms" column both read 9.

*(Method note: this finding was missed on the first disposition pass because the report was read
from the `## UNACCOUNTED NEIGHBOUR` heading down, and `BODY DRIFT` is printed above it. **A report
read from a heading is a truncated view** — the same rule this database has for capped output,
applied to a section anchor.)*

## The `0023B6F0` exclusive subtree — all 2 members bound (SWE2-FRONTIER, followup queue)

`0023B6F0` — the second Config-screen row proc — dispatches on
`qword[rdx+8]` against `0x2CA2`/`0x2CA3`/`0x2CA4`/`0x2CA5`/`1`
(`0023B742`–`0023B7BF`), writing `dword[rsi+0x1CC]` (the row value)
or swapping `+0xC4`/`+0xC8` around `+0xC0` (`0023B771`–`0023B79E`),
calling member `0017E540` on the `0x2CA4`/`0x2CA5` arms
(`0023B783`/`0023B7A4`), `0017DB40` when `dword[rsi+0xC0]` hits 5
(`0023B7B2`), and `0017E070` ×2 on the id-1 arm (`0023B7CB`/
`0023B7D6`).

| member | role | interior |
| --- | --- | --- |
| `0017E540` (321 B) | the 22-case row dispatcher — `ecx` vs `0x16` bound (`0017E54A`), `jmp rcx` through `dword[rdx + rax*4 + 0x5E684]` (`0017E55D`/`0017E567`) | [`0017E567`](../../_index/ADDRESS-INDEX.md) |
| `001DC920` (31 B) | paired field setter — `[01F82D20]` non-null gate (`001DC927`), `dword[rcx+0x38]` then `dword[rcx+0x24]` = `edx` (`001DC932`/`001DC93B`) | [`001DC932`](../../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: `0017DB40`, `0017E070`. The row's
literal ids reach `0017DB90` through `0017DD34` — the chain this
page's census already maps.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22 (SWE2-CONTRACT)

- **Audio — CLIENT and SERVICE (8 edges).** 2 inbound (Audio bodies `001DC3D0`, `00182E80` call page-cited `001DDAB0`); 6 outbound (page-cited `001D1660`, `001DBB00`, `00187950` call Audio bodies `002DEBA0`, `00182E80`, `001DBB00`). Substantive edges include `00187950` calls `00182E80`; `001CD0E0` calls `002DEBA0`; `001D1660` calls `001DBB00`; `001D1660` calls `002DEBA0`; the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT (3 edges).** 3 inbound (CombatAction bodies `BattleAction_RefundReservedExecutionResources` (00300280), `BattleAction_ConsumeExecutionResources` (00305640), `BattleAction_PrepareExecutionResources` (0030EF20) call page-cited `GameState_SetGil` (00254EE0)). Substantive edges include `GameState_SetGil` (00254EE0) is called by `BattleAction_RefundReservedExecutionResources` (00300280); `GameState_SetGil` (00254EE0) is called by `BattleAction_ConsumeExecutionResources` (00305640); `GameState_SetGil` (00254EE0) is called by `BattleAction_PrepareExecutionResources` (0030EF20).
- **CombatFormula — CLIENT and SERVICE (2 edges).** 1 inbound (CombatFormula bodies `BattleFormula_ApplyTargetResult` (003112F0) call page-cited `GameState_SetGil` (00254EE0)); 1 outbound (page-cited `00305A00` call CombatFormula bodies `BattleStats_GetByMappedBattleSlot` (00320AB0)). Substantive edges include `GameState_SetGil` (00254EE0) is called by `BattleFormula_ApplyTargetResult` (003112F0); the remaining edges run through shared helpers the page cites.
- **Items_Equipment_Shops_License — CLIENT (4 edges).** 4 inbound (Items_Equipment_Shops_License bodies `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530), `Shop_CommitSaleItemAndGil` (00310870), `Shop_CommitPurchaseItemAndGil` (002FEEB0) call page-cited `GameState_SetGil` (00254EE0)). Substantive edges include `GameState_SetGil` (00254EE0) is called by `InventoryBundleClass09_ApplyGilAndNestedItems` (002FD530); `GameState_SetGil` (00254EE0) is called by `Shop_CommitSaleItemAndGil` (00310870); `GameState_SetGil` (00254EE0) is called by `Shop_CommitPurchaseItemAndGil` (002FEEB0); `GameState_SetGil` (00254EE0) is called by `InventoryEncodedGilClass0E_ApplyGilDelta` (002FD880).
- **Platform — CLIENT (1 edge).** 1 inbound (Platform bodies `001DD170` call page-cited `001DF340`). Substantive edges include `001DF340` is called by `001DD170`.
- **PlatformOnlineAchievements — CLIENT and SERVICE (4 edges).** 1 inbound (PlatformOnlineAchievements bodies `007A0C60` call page-cited `001DF340`); 3 outbound (page-cited `001CD0E0`, `GameState_SetGil` (00254EE0), `00305A00` call PlatformOnlineAchievements bodies `003166F0`, `00316A50`, `00316C60`). Substantive edges include `001CD0E0` calls `003166F0`; `001DF340` is called by `007A0C60`; `GameState_SetGil` (00254EE0) calls `00316A50`; `00305A00` calls `00316C60`.
- **Presentation — CLIENT and SERVICE (48 edges).** 37 inbound (Presentation bodies `001D1660`, `00187950`, `001CD0E0` call page-cited `001A9930`, `00193D50`, `001C2F40`); 11 outbound (page-cited `001D1660`, `00187950`, `00184F20` call Presentation bodies `00186CD0`, `001876E0`, `00187550`). Substantive edges include `00184F20` calls `00186CD0`; `00187550` is called by `00187950`; `00187860` is called by `00187950`; `00187860` calls `001876E0`.
- **Resource — CLIENT and SERVICE (5 edges).** 1 inbound (Resource bodies `001A7A50` call page-cited `00193D50`); 4 outbound (page-cited `002EEEE0`, `001CD0E0`, `001D1660` call Resource bodies `0020C700`, `002EEEE0`, `002DF8E0`). Substantive edges include `00193D50` is called by `001A7A50`; `001CD0E0` calls `0020C700`; `001D1660` calls `002EEEE0`; `002EEEE0` calls `002DF8E0`.
- **Rewards_Progression_Economy — CLIENT and SERVICE (5 edges).** 4 inbound (Rewards_Progression_Economy bodies `GameState_AddGilClampedAndNotify` (003004B0), `GameState_SetGilClampedNonnegative` (00300500), `003F4AA0` call page-cited `GameState_SetGil` (00254EE0)); 1 outbound (page-cited `Debug_SetGilToMaximum` (003058B0) call Rewards_Progression_Economy bodies `GameState_SetGil` (00254EE0)). Substantive edges include `GameState_SetGil` (00254EE0) is called by `GameState_AddGilClampedAndNotify` (003004B0); `GameState_SetGil` (00254EE0) is called by `GameState_SetGilClampedNonnegative` (00300500); `GameState_SetGil` (00254EE0) is called by `003F4AA0`; `Debug_SetGilToMaximum` (003058B0) calls `GameState_SetGil` (00254EE0); the remaining edges run through shared helpers the page cites.
- **WorldAreaField — SERVICE (2 edges).** 2 outbound (page-cited `001CD0E0` call WorldAreaField bodies `WorldTransition_GetTransitionFieldId` (00314910), `FieldData_GetVariable0` (00265270)). Substantive edges include `001CD0E0` calls `WorldTransition_GetTransitionFieldId` (00314910); `001CD0E0` calls `FieldData_GetVariable0` (00265270).
