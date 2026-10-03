# Reconstruction readiness, pass 2 — `FFXII TZA/21-RNG-And-Determinism/`

| | |
|---|---|
| Stream | R2 (reconstruction readiness, pass 2), per [`docs/cloud-briefs/re-readiness-r2.md`](../../docs/cloud-briefs/re-readiness-r2.md) |
| Session | FABLE r2-22 |
| Date | 2026-10-03 |
| Snapshot | this repo's text snapshot (synced from XIIOnline `f9d9053b9`); no executable, Ghidra or live game was used |
| Branch | pass 1 did **not** map this system (`cloud-reports/re-readiness/` has no `21-*.md`), so this file follows part B: pass 1's full task (Interface, Gaps with a class column, Rating) |
| Status of this file | **draft / pointer**. Nothing here is evidence. Every item quotes or paraphrases a page, with its location. |

## Summary

*(Written last; see §3 and §4.)*

Citation form: `ABBREV:line`. Line numbers are those of the snapshot file.

| abbrev. | page (relative to `FFXII TZA/`) | lines |
|---|---|---:|
| `README` | `21-RNG-And-Determinism/README.md` | 29 |
| `RS` | `21-RNG-And-Determinism/rng-streams.md` (status `AUDITED`, `RS:4`) | 935 |
| `WR` | `21-RNG-And-Determinism/which-roll-is-on-which-generator.md` (status `AUDITED`, `WR:4`) | 519 |
| `CG` | `21-RNG-And-Determinism/CONTRACT-gameplay-generators.md` (readiness `DIFFERENTIAL TESTED`, "the ALGORITHM only", `CG:5`) | 766 |
| `CW` | `21-RNG-And-Determinism/CONTRACT-which-generator-serves-which-roll.md` (readiness `BEHAVIORALLY UNDERSTOOD`, `CW:5`) | 300 |
| `OQ` | `_index/OPEN-QUESTIONS.md` (the register; outside the folder) | — |

Member files opened for layout only: `procedural-stream-consumers.tsv` (114 rows, columns `function / name / route`),
`mt19937-state-accesses.tsv` (22 rows), `shared-gameplay-lcg-state-accesses.tsv` (17 rows), and the two census scripts in
`members/`. No item below rests on a `.tsv` alone.

"Not stated" means none of the four pages says it. A page outside the folder is cited by path only where it answers
or narrows a gap (those gaps are classed DOC).

---

## 1. Interface

The folder documents **at least eight generators** (`RS:32`, `README:3`). Two are specified draw for draw by a contract
(`CG:32-35`); a third (the CRT `rand()`) reaches gameplay but is routed by no contract (`CW:2`, `CW:44`). The rest are
presentation or engine streams. The interface is given per generator, then the routing (who draws from which), order,
and dependencies.

### 1.1 Generator inventory

| # | generator | state | seeded by | drives | spec level | cite |
|---|---|---|---|---|---|---|
| G1 | gameplay MT19937 | `Mt19937State` `0x9C4` at `02EB3870` (`mt[624]` +0, `index` +0x9C0 = `02EB4230`); lazy-seed latch `u8` at `02EB4234` outside the type | literal `0x11B9` (4537) at boot `0022A40B`; `_time64` + frame counter on save load `005843D3`; lazy 5489 if drawn unseeded | combat formula (53 of 66 thunk callers), weather, level-up growth, boot frame modes, camera shake (float draw) | exact, differentially tested | `CG:78-83`, `CG:178-244`, `CW:48`, `CW:65-67` |
| G2 | graphics-noise MT19937 | 624 words at `01F7F600`; `u32*` cursor `+0x9C0` (`01F7FFC0`), `u32` refill count `+0x9C8` (`01F7FFC8`); seed-mixer call counter `01F7FFD0` | `_time64(NULL)` and `clock()` folded by `0018D680`, once at static init (`0015BCF0`, CRT initialiser table `008C3200`) | one noise texture, `001946E0` | algorithm stated; per-texture draw count not | `RS:302-312`, `RS:812`, `RS:885-890`, `CW:49`, `CW:96-129` |
| G3 | shared gameplay LCG | `u32` at `022C256C` | pre-increment value of area counter `0208E6B0`, in `002342F0` at `00234320`, gated on `02089300` | loot, enemy chain, chain bonus, weighted action id, spawn placement, AI order, stance timer, yaw, avoidance | exact, differentially tested | `CG:154-190`, `WR:139-155`, `CW:50` |
| G4 | presentation bit-feedback PRNG | `01EF93E8`; mode word `022D9138` | `0x458DC800` at startup `00259180` (store at `00259216`), mode word set to 1 | procedural rendering, 114 consumer functions | recurrence and helper arithmetic exact; per-consumer step counts not | `RS:87-143`, `RS:193-216`, `CW:51` |
| G5 | CRT `rand()` (UCRT, per-thread) | external, in `api-ms-win-crt-utility-l1-1-0.dll` | `srand` at `007A540B` (thread function `007A5400`, QPC microseconds via `007AD680`) and Lua `math.randomseed` `008193E0` | 48 sites / 30 functions: movement, audio, charge-limit ticks, presentation, Lua `math.random` | census and seeding stated; algorithm not (external DLL) | `RS:496-547`, `CW:44` |
| G6 | Phyre counter hash ("stream 5") | `u32` counter `02E50260`, zero-initialised, never seeded | — | reached through pointer `02E502A8` (stored by `006B04B0`) | exact (`006B05E0`, 76 B) | `RS:867-883` |
| G7 | PPFX xorshift128 | locals; counter `01F3CD6C` (`.data`, initial 1); kernel table `02EA24A0`, flag `02EA3CA4` | four steps of MT's init recurrence from the counter | stratified unit-disk shader kernels | exact (incl. arithmetic `sar 8`) | `RS:722-778` |
| G8 | Bullet solver LCG | per-solver seed at `+0xC8`, reset to zero | — | physics solver | **not read** (tier 3, name only) | `RS:297`, `RS:299`, `RS:166` |

### 1.2 Entry points (with callers)

| entry | what | callers | cite |
|---|---|---|---|
| `00328370` `RNG_SharedGameplayLCG_NextU32` | LCG draw, no args, 31-bit `eax` | 23 sites / 15 functions (named in `CG:112`, `WR:99-109`) | `CG:48`, `CG:112` |
| inline LCG copies | `00317ED0`, `003183D0`, `00318510`, `003185D0`, `003186F0`, `00318820`, `00319530` — each "`00328370`'s three steps and assembly followed by `% 100`" | their own callers (e.g. `00319530` ← `00311146`; `003185D0` ← `Loot_RollDropEntries` `003180F0`) | `RS:600-619`, `RS:851`, `RS:455`, `CW:286` |
| `00328D80` `RNG_SharedGameplayLCG_SetState` | LCG seed, `ecx` | exactly one: `002342F0` at `00234320` | `CG:49`, `CG:113`, `CW:260` |
| `00379CD0` → `00863BF0` | MT `u32` draw | 98 sites / 66 functions | `CG:50`, `CG:114` |
| `00379CE0` → `00863C80` | MT float draw on the same cursor, `[0,1]` closed, double-precision scale `1/(2^32−1)` | 9 sites, all in the camera-shake sampler `0037D1F0` | `CG:51`, `CG:116`, `CG:436-442`, `CG:708-716` |
| `00379CF0` → `00863D30` | MT seed, `ecx` | two: `0022A410` (boot) and `005843D3` (save-load tail `jmp`) | `CG:52`, `CG:115`, `CG:555-566` |
| `00866D60` | MT `init_genrand`, `edx`; leaves cursor at 624 | `00863C13`, `00863CA3`, `00863D57`, `00863D6A` only | `CG:53`, `CG:227-238`, `CG:559-561` |
| `00866B90` | MT twist; SSE 224-element prefix + scalar remainder, one loop | the two draws on exhaustion | `CG:54`, `CG:267-335` |
| `003D8E50` | G4 scaled draw, 7 steps when `022D9138` ≠ 0; returns `f32(sample×A) − f32(A×vf00.w)` | 49 caller functions, 220 sites (incl. `0040AAD0` ×2) | `RS:98-126`, `RS:201-202` |
| `004005E0` | G4 one-step draw, returns `[0,1)`, scratch store to `022D92E0`/`022D8F90` | exactly one caller | `RS:128-133`, `RS:206`, `CW:300` |
| `00259180` | G4 seeder | `0022A0B0` | `RS:135-140`, `CW:281` |
| `0015BCF0` → `0018D680` → `0018D740` → `0018EE20` | G2 seed chain (mixer, `init_genrand` on caller-supplied state, twist that resets cursor/count) | CRT initialiser table `008C3200`, once | `RS:302-308`, `RS:885-890`, `RS:930`, `WR:503`, `CW:116-118` |
| `001946E0` | G2 draw-and-fill noise texture | `0018D850` ← `0017CF30` (device/viewport setup, slot 3) | `RS:306-309` |
| `006B05E0` | G6 counter hash | through pointer `02E502A8` only | `RS:869-883` |
| `0074BDE0` | G7 kernel builder | `0074C4D0`'s caller `00741680` ← `006F61F0` (one hop) | `RS:722-760` |
| IAT `008C3098` / thunk `00861F38` | G5 `rand` | 48 indirect sites / 30 functions; thunk 1 site from `00149610` | `RS:505-535` |

### 1.3 Inputs and outputs (record layouts)

- **LCG draw output**: `c ^ ((b ^ a) << 10)` with `a = ((s1>>16)&0x7FF)<<10`, `b = (s2>>16)&0x3FF`, `c = (s3>>16)&0x3FF`; one writeback of `s3` (`CG:154-173`, `CG:394-408`).
- **MT draw output**: stock tempering, masks pre-shifted (`0xFF3A58AD`, `0xFFFFDF8C`) (`CG:246-265`); float form `(float)((double)y * (1.0/4294967295.0))` (`CG:436-442`).
- **Save-load MT seed**: `(((u32)t + 0x2B5A5)*0x21 + (t>>32)) & 0x7FFFFFFF + [01FD4A80]*600`, mask before the frame term (`WR:303-312`, `CG:201-211`).
- **G4 recurrence**: `feedback = (((s>>18)^s)>>4)&1; s = (((s&0x3FFFFF)|0x1FC00000)<<1)|feedback`, bits read as an IEEE float in `[1,2)` (`RS:91-96`); bounded helper `trunc(f32(v×B) − f32(B))` on the authored-expression page (`RS:130-132`).
- **Weighted action id** (`00308EC0`, consumer of G3): word < `0x8000` returned as is; else index into directory `[02EBF160]` of `u32 offset[]` bounding runs of `{u16 actionId, u8 weight, u8 0}`; one draw `% 100`, first row whose cumulative weight exceeds it; `0xFFFF` on miss (`RS:345-360`; `OQ` AD-1 ANSWERED).
- **Chain-bonus roll** (`00319530`): `% 100` against a 4×7 byte table at `01EED3B8` indexed by chain rank `022C3158` (`RS:455`, `WR:423-428`; `OQ` AD-6, AE-3, CQ-1 ANSWERED).
- **G6 hash**: `c=++[02E50260]; x=(c^0x00BC602F)*0x9E3779B9; y=((x<<6)^(x>>26)^x)*0x9E3779B9; r=((y<<5)^(y>>12))+y; r·2⁻³²` in `[0,1]` (`RS:871-876`).
- **G7 kernel**: 16-byte entries `{r cosθ, r sinθ, 0, 0}`, `r = 0.01 + 0.99·sqrt((u₁+i)/N)`, `θ = 2π(u₂+j)/N`, `0x400`-byte level per `N` = 3…8 (`RS:740-751`).
- **Declared types**: `AreaEntryCounter` `0208E6B0` u32, `RngReseedGate` `02089300` u32, `TickCounter01FD4A80` u32, `Mt19937State` `0x9C4`, `GeneratorInitLatch` `02EB4234` u8 (`CW:57-67`).

### 1.4 State and lifetime

| state | initial value | lifetime / writers | cite |
|---|---|---|---|
| `022C256C` LCG | 0 (`.bss`) | image static; 9 writers (8 recurrence copies + setter) | `CG:95-102`, `RS:442-455` |
| `02EB3870`/`02EB4230`/`02EB4234` MT | 0 (`.bss`), so an unseeded stream self-seeds 5489 | image static; cursor 0→624 on seed, 624→0 on twist, +1 per draw; latch one-shot | `CG:95-102`, `CG:378-387` |
| `0208E6B0` area counter | not stated explicitly; implied by "seeded 0, 1, 2, 3 …" (`CW:94`) | 2 instructions, both in `002342F0` | `CW:61`, `CW:90-94` |
| `02089300` reseed gate | 0 until boot frame mode 0 sets it | cleared once by `002368D0` (from `0022A0B0` at `0022A41A`), set once by `00236A40` (from `0022B6E0` at `0022B77C`); 3 readers | `CW:181`, `WR:458-466` |
| `01FD4A80` frame counter | 0 (`.data` uninitialised tail) | `inc` once per dispatched tick at `0022A59F`; read once at `005843B4` | `CG:544-554` |
| `01EF93E8` G4 state / `022D9138` mode | `0x458DC800` / 1 after `00259180` | 10 direct touchers, 104 more callers | `RS:135-140`, `RS:198-204` |
| `01F7F600` G2 | seeded once at static init | two bodies only | `CW:107-112` |
| `02E50260` G6 | 0, never seeded | one reader/writer | `RS:879-881` |
| `01F3CD6C` G7 counter | 1 (`.data`) | one function | `RS:729`, `RS:756-758` |

### 1.5 Order and triggers

```
static init  : G2 seeded from time+clock (0015BCF0, CRT initialiser table)         RS:304-306
boot 0022A0B0: G4 seeded (00259180); MT <- 4537 (0022A40B); gate 02089300 <- 0     CW:159, CW:181, CG:192-199
boot mode 0  : MT draw discarded (0022B706); gate <- 1 (0022B77C)                  CG:129-139, CW:181
boot mode 1  : MT draw discarded (0022B7EB)                                        CG:131-133
area init    : if gate: LCG <- counter++ (002342F0)                                WR:143-146, CW:160
save load    : MT <- _time64 mix + frames*600 (00584210, tail jmp)                 CG:201-216, CW:161
every frame  : camera-shake driver 003DCFB0 samples up to 4 drivers x 16 floats    CG:742-752
on demand    : every listed consumer draws when its caller runs
```

**Not stated:** the order of LCG/MT draws within a frame or a combat turn (`WR:354-355`, `CW:226-227`, `CG:511-513`).

### 1.6 Dependencies

- **Consumers in other systems** (cross-subsystem blocks `RS:896-922`, `CW:275-292`): Spawn, CombatAI, ActorEntity, Movement, Party, Rewards (loot, chain), CombatFormula, Status, ScriptVM, Save/Load, Presentation, Audio (`rand`), Lua (`rand`).
- **Weighted directory data** `battle_pack.bin` +0x2C bound to `02EBF160` (`RS:355-356`); chain-bonus table `01EED3B8` (`RS:455`).
- **Boot and frame dispatcher**: `0022A0B0`, `0022A580`, modes `0022B6E0`/`0022B7E0` (`CG:129-139`); page `22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md` §2.2.
- **Save load**: `00584210` (`CG:144-150`, `CG:201-216`).
- **Authored expressions**: the G4 bounded helper and its contract `CONTRACT-authored-expression-evaluation.md` (S-10) (`RS:130-132`, `CW:150-153`).
- **CRT**: `__isa_available` `01F44858` gates the vectorised twist prefix (`CG:310-314`); `_time64`/`clock` imports (`RS:889-890`).
