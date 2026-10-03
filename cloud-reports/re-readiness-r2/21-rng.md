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

---

## 2. Gaps

Pass 1 did not map this system, so every gap below is **NEW** (part B). Each is classed per the R2 brief:
**STATIC** (a desk read of the executable or data answers it), **RUNTIME** (needs a live observation), **DATA**
(needs a census of shipped data) or **DOC** (the answer is on another page; this page lacks the pointer, or two pages
disagree). The register (`OQ`) was searched for every gap by address and by subject; "—" means no row was found.

### 2.1 Generators the folder names but does not specify

| id | gap | class | evidence | register |
|---|---|---|---|---|
| N-01 | **Family 6, the Bullet solver LCG, is unread.** Its recurrence, constants, draw count per solve and the claim that it is "reset to zero per solve" rest on GFZ naming only. `RS:332` draws a determinism conclusion ("physics is not a divergence source through RNG") from that tier-3 row. | STATIC | `RS:297` ("per-solver seed at `+0xC8`, reset to zero"), `RS:299` ("Family 6 alone is still recorded from GFZ annotation and function naming (tier 3)"), `RS:166` ("only family 6 … stays unread"), `CG:536` | — |
| N-02 | **The CRT `rand()` algorithm and the state an un-`srand`-ed thread starts from are not stated.** The pages give the import, the per-thread state and the two `srand` callers, but no recurrence, output width or default seed. The generator sits in `api-ms-win-crt-utility-l1-1-0.dll`, not in the executable, so the desk read is of that DLL. | STATIC | `RS:498-499`, `RS:539-542` ("any other thread's `rand` is never `srand`-ed outside Lua"); no page in the database contains the UCRT constants (searched `214013`, `0x343FD`) | — |
| N-03 | **Which thread each gameplay `rand` consumer runs on is not established**, so whether a movement draw and a charge-limit draw share one `rand` state is not stated. The register answers this for the Sound selects only. | STATIC | `RS:540-542` ("whether the audio, movement and combat consumers here share a thread is **not established**") | `SD-25` ANSWERED 2026-09-30, audio thread only |
| N-04 | **No `rand` consumer's reduction is stated except one.** `002FA1A0`'s `rand() % (900·tb) + 1200·tb` is the only formula. How `LuaMath_Random` maps `rand()` onto Lua's `math.random(m, n)` is not stated on this folder or on the Lua page, which lists only the `randomseed` address. | STATIC | `CW:44`; `RS:509-525`; `22-Middleware-PhyreEngine/Embedded-Lua-And-Object-Bindings/embedded-lua-and-phyre-object-bindings.md:710` | — |
| N-05 | **The 30 `rand` consumer functions are not listed.** The census gives counts by subsystem and names about ten; "Combat Formula 1", "UI 1" and "unowned 7" are unnamed. Unlike the LCG and the G4 stream, there is no member `.tsv`. | STATIC | `RS:509-518` | — |
| N-06 | **Two counts of `rand` callers disagree.** The RNG page says 30 functions; the register's SD-25 row says "of the 31 `rand` callers". The thunk `00861F38`'s one caller `00149610` may account for the difference, but neither text says so. | DOC | `RS:505` ("48 call sites across 30 functions"), `RS:531-532`; `OQ:3574` (SD-25: "of the 31 `rand` callers, 4 are inside the sound thread's direct-call closure") | `SD-25` |
| N-07 | **The 66 MT `u32` consumer functions are not listed on any page in the folder.** About fifteen are named (`RS:383-390`, `CG:114`, `CG:129-143`). The census is cited from `edges.tsv` (`WR:417`), which is not part of the folder. A re-implementer cannot enumerate the gameplay MT's consumers from the pages. | STATIC | `RS:371`, `RS:383-390`, `CG:114`, `WR:417-419` | — |

### 2.2 Order, position and live validation

| id | gap | class | evidence | register |
|---|---|---|---|---|
| N-08 | **The order of draws within a frame or a combat turn is not stated for any generator.** On these fixed streams "draw ordering is the entire source of variation" (`WR:256`), so an outcome-level parity test cannot be written. | RUNTIME | `WR:354-355` ("How many draws precede a given roll … is not traced here"), `CW:226-227`, `CG:511-513` | — |
| N-09 | **The gameplay MT's position at the first gameplay draw after a fresh boot is not established.** Boot frame modes 0 and 1 each draw and discard once per dispatch, and the dispatch counts wait on load conditions. | RUNTIME | `CG:129-139` ("whether they vary is a runtime question this contract does not answer"), `CG:351`, `WR:186-195` | — |
| N-10 | **How many camera-shake drivers are non-zero per frame is not measured**, and the bound (4 drivers × 16 floats = 64 draws per frame) makes shake the dominant consumer of the MT cursor by volume. Finished drivers (state 2) still draw. | RUNTIME | `CG:744-761` ("Routed to ASTRA as a live question") | — (routed to ASTRA in text, no row) |
| N-11 | **Two seeding facts are read but not run**: that two loads of the same save produce different MT states, and that `0208E6B0` increments rather than resets across two entries to the same area. The runtime value of `01FD4A80` at any save is inherently live. | RUNTIME | `CG:495`, `CG:503-510`, `CW:217-224` | — |

### 2.3 Seeding and initial state

| id | gap | class | evidence | register |
|---|---|---|---|---|
| N-12 | **The LCG seed used by the first gameplay area after boot is not stated.** The broad bootstrap `00266D10` also calls `002342F0` and "also advances the counter" (`WR:291`), but the reseed only runs when the gate `02089300` is 1, and the gate is set in boot frame mode 0 (`0022B77C`). Whether the bootstrap call runs before or after that set, and so whether the first gameplay seed is 0 or 1 (or more), is not stated. The counter's load-time value is also not stated outright: `CW:94` gives "seeded 0, 1, 2, 3 …" but no page says `0208E6B0` is in `.bss` or zero in the file image, as `CG:98` does for the other four statics. | STATIC | `WR:143-146`, `WR:291`, `CW:94`, `CW:181`, `CG:98-102` | — |
| N-13 | **Where the reseed falls inside `002342F0` relative to that function's other LCG-reaching calls is not stated.** The page says only that "Around the LCG reseed it calls `SpawnKeep_RotatePersistenceBanksForAreaTransition` … and `SpawnGroup_ResetLifecycleLedger`"; whether any spawn or keep draw in area init happens before the reseed (and so on the old stream) is not given. | STATIC | `WR:290-295` | — |
| N-14 | **The second writer of the G4 mode word `022D9138` is unnamed.** "Every rip-relative store to `022D9138` writes 1: the startup seed `00259220`, and two more stores in one other function." Since mode 0 freezes the stream (`RS:123-125`), what clears or sets it matters for phase, even though every store found writes 1. | STATIC | `RS:125-126` | — |

### 2.4 Per-consumer accounting

| id | gap | class | evidence | register |
|---|---|---|---|---|
| N-15 | **The G4 stream's per-consumer step counts are not stated.** The census lists 114 functions and their route (`procedural-stream-consumers.tsv`: `function / name / route`), but the steps per call are given only for `003D8E50` (7) and `004005E0` (1). The seven inline steppers, two of them shared helpers with 36 callers each, have no step count. The page itself recommends regenerating render randomness locally rather than replaying the phase (`RS:208-210`), which bounds how much this matters. | STATIC | `RS:198-204`; `procedural-stream-consumers.tsv` header | `UQ-276` ANSWERED (census only) |
| N-16 | **G2's draws per noise texture, and the texture's size, are not stated.** The draw window `00194831`–`001948D0` is cited, but neither the count nor the dimensions are. The stream is presentation-only. | STATIC | `RS:306-307` | — |
| N-17 | **Who calls G6 through its pointer is not stated.** The page answers who *stores* `006B05E0` at `02E502A8` (`006B04B0`), not who loads and calls it, so G6's consumers and draw rate are unknown. | STATIC | `RS:882-883` | — |
| N-18 | **Which PPFX effect owns G7's kernel path is not established**, so when G7 rebuilds (and advances its counter) is not tied to any effect. | STATIC | `RS:759-763` ("Which effect owns `006F61F0` remains unestablished") | — |
| N-19 | **No texture-readback census was run**, so "gameplay could only depend on [G2] by reading that texture back, which nothing here was found to do" is an absence without a complete census. | STATIC | `RS:309-311` | `AD-3` ANSWERED with this caveat (`OQ:657`) |
| N-20 | **Whether the gameplay MT or the shared LCG is ever stepped from a thread other than the main one is not stated.** | STATIC | `WR:356` | — |

### 2.5 Answers on other pages, and pages that disagree

| id | gap | class | evidence | register |
|---|---|---|---|---|
| N-21 | **`01DFE0BC` is called "an unresolved scalar" in the camera-shake sampler, but the register has answered it.** K-8 and Z-11: it is the reciprocal of the frame-rate triple at `01DFE0B4`–`01DFE0BC`, `1.0` by default and `0.5` at 60 fps, written only at startup by `001EDDC0`. The contract lacks the pointer. | DOC | `CG:738-740` ("It is named here as an unresolved scalar, not consumed as a no-op."); `OQ:298` (K-8 ANSWERED 2026-09-02), `OQ:591` (Z-11 ANSWERED) | `K-8`, `Z-11` ANSWERED |
| N-22 | **The address of `vf00.w` is not given where the G4 scaled draw depends on it.** `RS:103-105` cites "`mulss` by `vf00.w`" and says both writers set it to 1.0, without an address. The register-bank page says `01EF93F0` is vf00 = (0, 0, 0, 1), so `vf00.w` is `01EF93FC`, which `RS:190` lists only as "constant 1.0". | DOC | `RS:103-105`, `RS:190`; `00-Engine-Core-Runtime/Shared-Transform-Workbench/the-ee-and-vu0-register-bank.md:35` | — |
| N-23 | **`00319A00` is called "not read" beside the chain-bonus roll, but other pages describe it.** It is `Loot_CollectWorldPickupByIndex`, a 26-byte index adapter: `idx × 0x60` into the pickup table `02EC0FA0`, tail to `00319920`. | DOC | `WR:486` ("`00319A00`, called immediately before it, was not read"); `13-Rewards-Progression-Economy/world-loot-pickups-the-ten-slot-pool-and-the-despawn.md:297`, `:374`; `10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md:246` | — |
| N-24 | **`which-roll-is-on-which-generator.md` still states the LCG's consumers as the eight writers in three places**, after its own §3 note and the contract widened them to 8 writers + 15 callers: §2's generator 3 "drives loot, the enemy chain, weighted action selection" (no spawn, AI order or stance timer, unlike `CW:50`); "Loot rolls, enemy-chain rolls and the weighted action selector … All eight read the same state" (the weighted selector `00308EC0` is a caller, not one of the eight); and §6 "One state, eight draw sites". | DOC | `WR:48`, `WR:90-92`, `WR:234-235`; against `WR:84-88`, `WR:117-119`, `CW:50` | `AD-2` ANSWERED (`OQ:656`) |
| N-25 | **`CONTRACT-which-generator-serves-which-roll.md` §13 opens "None for the routing" and leaves it unstruck**, two paragraphs above its own note that `EXP-144` executed the routing on 2026-09-22. The front-matter correction (`CW:34`) struck the matching line in the header, but not this one. | DOC | `CW:198-202` against `CW:204-213`, `CW:34` | — |

### 2.6 Counts

| class | count | ids |
|---|---:|---|
| STATIC | 15 | N-01, N-02, N-03, N-04, N-05, N-07, N-12, N-13, N-14, N-15, N-16, N-17, N-18, N-19, N-20 |
| RUNTIME | 4 | N-08, N-09, N-10, N-11 |
| DATA | 0 | — |
| DOC | 6 | N-06, N-21, N-22, N-23, N-24, N-25 |
| **total** | **25** | |

Gaps the folder's register rows track: 5 (N-03 `SD-25`, N-15 `UQ-276`, N-19 `AD-3`, N-21 `K-8`/`Z-11`, N-24 `AD-2`;
N-06 also cites `SD-25`). All of those rows read ANSWERED; each gap is the remainder that row leaves, or a pointer the
page lacks. The other 19 have no register row.

**Closed in the pages, so not gaps** (checked, listed so a later pass does not reopen them): the MT float draw and
its scale (`CG:51`, `CG:436-442`); the save-load seed formula and `01FD4A80`'s role (`WR:303-312`, `CG:544-554`);
the reseed gate's lifetime (`CW:181`); the graphics MT's state address and index cells (`CW:96-129`, falsification
pass `CW:244-273`); the twist's prefix-plus-remainder shape (`CG:298-308`); the LCG census's completeness (`WR:115-132`,
`OQ` AD-2); the G4 consumer census (`RS:193-210`, `OQ` UQ-276); the weighted-id walk and the chain-bonus roll
(`RS:345-360`, `RS:455`, `OQ` AD-1, AD-6, AE-3, CQ-1); stream 5's pointer holder and stream 4's seed arguments
(`RS:882-890`); the PPFX xorshift128 (`RS:722-758`, `OQ` CQ-6); the camera-shake channel table (`OQ:1578` CA-2).
