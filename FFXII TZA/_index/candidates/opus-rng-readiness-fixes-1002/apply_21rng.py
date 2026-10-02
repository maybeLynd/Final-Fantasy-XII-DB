"""apply_21rng.py [--apply] - 21-RNG-And-Determinism readiness map (readiness-21-rng.md), section 2.4
contradictions 1-23 and the section 2.5 claims the bytes refute or answer, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the image or the shipped data refutes) and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Item 1 favours only rng-streams.md's "at least" wording: every page that states six, seven, four, three or two as the
exact count is struck, and the opening line keeps "at least", raised to eight with the xorshift128 0074BDE0
(checked at 0074BFE0-0074C0C4).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike; front-matter lines get the same comment as a
YAML comment (`   # <- corrected ...`), with no value changed. Their OLD includes the line end, so NEW never contains OLD.
Item 20 renumbers the second section 8 to 8a and the second section 9 (Related) to 8h, each changed heading naming OPUS;
the section-8 Evidence heading and the section-9 falsification-pass heading keep their numbers, because the page's own
"section 9" / "section 8" references and the tier checker's Evidence heading pattern point at them.
X1-X9 are the section 2.5 refutations: the rand import thunk, the srand seeding, stream 5's closed upper bound, stream 5's
pointer holder, the seed mixer's time / clock inputs, the reseed gate's two writers, the MT draw duplicated in 00863C80,
the LCG inliners being behaviourally one function, and 0018D740's two +0x9BC operands.
The structural gaps (section 2.2) are left for later, as briefed.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "21-RNG-And-Determinism/"
R = F + "README.md"
RS = F + "rng-streams.md"
WR = F + "which-roll-is-on-which-generator.md"
CG = F + "CONTRACT-gameplay-generators.md"
CW = F + "CONTRACT-which-generator-serves-which-roll.md"

XOR = "the PPFX xorshift128 `0074BDE0`, checked at `0074BFE0`–`0074C0C4`"
F32 = "checked at `00863C80`–`00863D2C`"
GATE = ("`002368D0`, the only clear, is called once, from boot `0022A0B0` at `0022A41A`, and `00236A40`, the only set, "
        "once, from boot frame mode 0 `0022B6E0` at `0022B77C` — so the gate is 0 only between boot initialisation and "
        "boot mode 0, and 1 for the rest of the process")

EDITS = [
    # C1: at least eight generators - the GFZ's six families, the presentation PRNG and the xorshift128 0074BDE0
    #     (0074BFE0-0074C0C4). RS:32's "at least" is the only non-false figure; it is raised, the exact counts struck.
    (RS, "> FFXII has **at least seven** distinct random sources.",
     "> FFXII has **at least ~~seven~~ eight** distinct random sources *(corrected 2026-10-02, OPUS: the eighth is "
     + XOR + ", distinct from every other generator; §10, `CQ-6`)*."),
    (RS, "> *third* stream - a separate LCG - not from the Mersenne Twister. And there are **six** RNG\n"
         "> families in the binary, not two.",
     "> *third* stream - a separate LCG - not from the Mersenne Twister. ~~And there are **six** RNG~~\n"
     "> ~~families in the binary, not two.~~ And there are at least eight generators in the binary, not two *(corrected "
     "2026-10-02, OPUS: the GFZ's six families, the presentation PRNG of section 2 and " + XOR + ", §10)*."),
    (RS, "### Six RNG families, not two\n",
     "### ~~Six RNG families, not two~~ Six families in the GFZ, at least eight generators in the image *(corrected "
     "2026-10-02, OPUS: plus the presentation PRNG of section 2 and the xorshift128 `0074BDE0` of §10)*\n"),
    (RS, "This document describes **two** RNG streams. There is a **third**: the **CRT `rand()`**, imported",
     "~~This document describes **two** RNG streams. There is a **third**:~~ Beside the two gameplay streams there is "
     "the **CRT `rand()`** *(corrected 2026-10-02, OPUS: this document describes at least eight generators — the "
     "opening line; the CRT `rand()` is §8a's family 3)*, imported"),
    (CG, "`rng-streams.md` records six families; the other four are not specified\nhere",
     "`rng-streams.md` records ~~six families; the other four~~ at least eight generators *(corrected 2026-10-02, OPUS: "
     "the GFZ's six families, the presentation PRNG and " + XOR + ")*; the others are not specified\nhere"),
    (CG, "- The other four RNG families `rng-streams.md` records.",
     "- ~~The other four RNG families `rng-streams.md` records.~~ The other generators `rng-streams.md` records, at "
     "least six *(corrected 2026-10-02, OPUS: the image holds at least eight, the xorshift128 `0074BDE0` the eighth)*. "
     "Families 3, 4 and 5 and the xorshift128 are read there; only family 6, the Bullet solver LCG, is not *(answered: "
     "see rng-streams.md's `rand` census, its family-4 note of 2026-09-14, `CQ-6` and its streams-4-and-5 section of "
     "2026-09-19; 2026-10-02, OPUS)*. None of them is specified in this contract."),
    (CG, "`21-RNG-And-Determinism/rng-streams.md` — the six families and their consumers.",
     "`21-RNG-And-Determinism/rng-streams.md` — the ~~six families~~ generators, at least eight *(corrected 2026-10-02, "
     "OPUS: the GFZ's six families plus the presentation PRNG and the xorshift128 `0074BDE0`)*, and their consumers."),
    (WR, "## 2. Four generators\n",
     "## 2. ~~Four generators~~ Four of at least eight generators *(corrected 2026-10-02, OPUS: the table omits the CRT "
     "`rand()` — IAT `008C3098`, 48 call sites in 30 functions — which also decides gameplay (rng-streams.md §8g), and the "
     "presentation-only stream 5, the xorshift128 `0074BDE0` and the Bullet solver LCG)*\n"),
    (WR, "the three streams this builds on",
     "the ~~three streams~~ generators, at least eight *(corrected 2026-10-02, OPUS: rng-streams.md's opening line and "
     "§10, the xorshift128 `0074BDE0`)*, this builds on"),
    (R, "**Engine category.** The gameplay MT19937 stream and the separate shared procedural render PRNG - two different "
        "domains that must never be conflated.",
     "**Engine category.** ~~The gameplay MT19937 stream and the separate shared procedural render PRNG - two different "
     "domains that must never be conflated.~~ At least eight random generators that must never be conflated: the two "
     "gameplay generators specified exactly (the shared LCG and the gameplay MT19937), the CRT `rand()`, which also "
     "reaches gameplay, and the presentation and engine streams (the graphics-noise MT19937, the presentation "
     "bit-feedback PRNG, the stream-5 counter hash, the PPFX xorshift128 and the Bullet solver LCG) *(corrected "
     "2026-10-02, OPUS: rng-streams.md's opening line and §10 — " + XOR + "; the CRT `rand` at IAT `008C3098`, 48 call "
     "sites in 30 functions)*."),

    # C2: the routing omits the CRT rand(), which decides gameplay (retool refs 008C3098 = 48 calls in 30 functions plus
    #     the thunk 00861F38; 002FA1A0 returns rand() % (900*tb) + 1200*tb at 002FA1BB-002FA1D9).
    (CW, "contract: route every gameplay roll to one of four generators and keep their streams apart - which consumer "
         "draws from which, what reseeds each, and therefore what can correlate with what\n",
     "contract: route every gameplay roll to one of four generators and keep their streams apart - which consumer "
     "draws from which, what reseeds each, and therefore what can correlate with what   # <- corrected 2026-10-02, "
     "OPUS: not every gameplay roll - the CRT rand() (IAT 008C3098, 48 call sites in 30 functions, among them "
     "002FA1A0 at 002FA1BB-002FA1D9) also serves gameplay and is not routed here; see section 2\n"),
    (CW, "Four generators, and they are not interchangeable **[page]**:",
     "~~Four generators~~ Four of the image's generators *(corrected 2026-10-02, OPUS: at least eight exist, and a "
     "fifth, the CRT `rand()` — IAT `008C3098`, 48 call sites in 30 functions plus the thunk `00861F38` — also decides "
     "gameplay: `002FA1A0` returns `rand() % (900·tb) + 1200·tb` at `002FA1BB`–`002FA1D9`; rng-streams.md §8g. This "
     "routing does not cover it)*, and they are not interchangeable **[page]**:"),

    # C3: 67 MT consumer functions - callers 00379CD0 = 98 sites in 66 functions, callers 00379CE0 = 9 sites in 0037D1F0.
    (WR, "combat formula (53 sites), weather, and more — **66 consumer functions** |",
     "combat formula (53 sites), weather, and more — ~~**66 consumer functions**~~ **67 consumer functions**: 66 through "
     "`00379CD0` and the camera-shake sampler `0037D1F0` through the float thunk `00379CE0` *(corrected 2026-10-02, "
     "OPUS: `callers 00379CD0` = 98 sites in 66 functions, `callers 00379CE0` = 9 sites, all in `0037D1F0`; "
     "CONTRACT-gameplay-generators.md §12c)* |"),
    (WR, "| MT has 66 consumers, 53 in CombatFormula |",
     "| MT has ~~66 consumers, 53 in CombatFormula~~ 67 consumer functions: 66 on the draw thunk (53 in CombatFormula) "
     "and `0037D1F0` on the float thunk `00379CE0` *(corrected 2026-10-02, OPUS: `callers 00379CE0` = 9 sites, all in "
     "`0037D1F0`)* |"),
    (CW, "combat formula (53 sites), weather — 66 consumer functions |",
     "combat formula (53 sites), weather — ~~66 consumer functions~~ 67 consumer functions, 66 through `00379CD0` and "
     "the camera-shake sampler `0037D1F0` through `00379CE0` *(corrected 2026-10-02, OPUS: `callers 00379CE0` = 9 "
     "sites, all in `0037D1F0`; CONTRACT-gameplay-generators.md §12c)* |"),

    # C4 + X7: NextU32 is not the single MT intercept - 00863C80 reads and writes 02EB4230 itself and calls
    #     00866B90 / 00866D60 directly (00863C80-00863D2C); the hookability table counts it nowhere.
    (RS, "> **MT19937 is not inlined and the shared LCG is.** So `RNG_MT19937_NextU32` *is* a real intercept\n"
         "> point — hooking it catches every gameplay Mersenne draw — while hooking",
     "> **MT19937 is not inlined and the shared LCG is.** So `RNG_MT19937_NextU32` *is* ~~a real intercept~~\n"
     "> ~~point — hooking it catches every gameplay Mersenne draw~~ an intercept point for the integer draws only — "
     "the float draw `00863C80` repeats its body on the same cursor and never calls it, so hooking it misses camera "
     "shake *(corrected 2026-10-02, OPUS: " + F32 + ", which reads and writes `02EB4230` itself and calls `00866B90` / "
     "`00866D60` directly; CONTRACT-gameplay-generators.md §2)* — while hooking"),
    (RS, "| inlined? | **yes**, 8 functions / 24 sites | **no** |",
     "| inlined? | **yes**, 8 functions / 24 sites | ~~**no**~~ once — `00863C80` duplicates the draw on the same "
     "cursor *(corrected 2026-10-02, OPUS: " + F32 + ")* |"),
    # X8: the inline LCG copies are behaviourally one function (00317ED0, 003185D0, 00319530 decoded).
    (RS, "| single point to reimplement? | **no** — every consumer carries its own copy of the three-step draw | "
         "**yes** |",
     "| single point to reimplement? | ~~**no** — every consumer carries its own copy of the three-step draw~~ **yes, "
     "behaviourally** — every inline copy is `00328370`'s three steps and assembly followed by `% 100` *(corrected "
     "2026-10-02, OPUS: `00317ED0`, `003185D0` and `00319530` decoded identical to `00328370` plus `% 100`; the copies "
     "still have to be hooked one by one)* | ~~**yes**~~ **no** — two draw entries on one cursor, `00863BF0` and "
     "`00863C80` *(corrected 2026-10-02, OPUS: " + F32 + ")* |"),
    (RS, "| single point to hook? | no — hooking the one out-of-line copy catches one draw in eight | yes |",
     "| single point to hook? | no — hooking the one out-of-line copy catches one draw in eight | ~~yes~~ no — "
     "`00863BF0` misses the float draw `00863C80`, camera shake *(corrected 2026-10-02, OPUS: " + F32 + ")* |"),

    # C5: four functions touch the MT state (refs 02EB3870..02EB4233 = 4 + 4 + 11 + 3, mt19937-state-accesses.tsv).
    (WR, "every instruction touching `02EB3870` enumerated: three functions, none of them the graphics pair",
     "every instruction touching `02EB3870` enumerated: ~~three functions~~ four functions — `00863BF0`, `00863C80`, "
     "`00866B90`, `00866D60` *(corrected 2026-10-02, OPUS: `refs 02EB3870..02EB4233` = 4 + 4 + 11 + 3 instructions, the "
     "22 rows of `mt19937-state-accesses.tsv`; §13 and §2's correction)*, none of them the graphics pair"),

    # C6: the graphics MT keeps a u32* cursor at +0x9C0 and a u32 count at +0x9C8, set by the twist (0018EECD, 0018EED8).
    (CW, "`01F7F600` (624 dwords); **no index of its own** — see I5 |",
     "`01F7F600` (624 dwords); ~~**no index of its own**~~ an index kept as a `u32*` cursor at `+0x9C0` and a `u32` "
     "refill count at `+0x9C8`, both set by the twist *(corrected 2026-10-02, OPUS: `0018EECD` `mov dword [r10+0x9c8], "
     "0x270`, `0018EED8` `mov qword [r10+0x9c0], r10`; I5 as corrected 2026-09-29)* — see I5 |"),
    (RS, "reaching `mt[623]`. Same type, two storage classes. A",
     "reaching `mt[623]`. ~~Same type, two storage classes.~~ The same 624-word array but not the same type: the "
     "graphics instance keeps a `u32*` cursor at `+0x9C0` and a `u32` refill count at `+0x9C8`, where `Mt19937State` "
     "(`0x9C4`) keeps a `u32` index *(corrected 2026-10-02, OPUS: the twist sets both cells at `0018EECD` and "
     "`0018EED8`, the walk is `00194831`–`00194862`; CONTRACT-which-generator-serves-which-roll.md I5)*. A"),
    (RS, "> block `01F7F600`, with index words `01F7FFC0` / `01F7FFC8`.",
     "> block `01F7F600`, with ~~index words~~ a `u32*` cursor and a `u32` refill count *(corrected 2026-10-02, OPUS: "
     "`01F7FFC0` is walked as an 8-byte pointer at `00194855`–`00194862`, and the twist writes both cells at `0018EECD` "
     "/ `0018EED8`)* `01F7FFC0` / `01F7FFC8`."),

    # C7: the graphics twist is standard MT19937 - (mt[i]&0x80000001)|(mt[i+1]&0x7FFFFFFE), partner [+0x634] for 227
    #     iterations then [-0x38C] for 0x18C = 396, then the last element (0018EE30-0018EECA).
    (WR, "call-free MT twist: `(mt[i]&0x7FFFFFFE | mt[i+1]&1) >> 1 ^ (odd ? 0x9908B0DF : 0) ^ mt[i+0x18C]`, a "
         "227-iteration loop then a 396-iteration loop,",
     "call-free MT twist: ~~`(mt[i]&0x7FFFFFFE | mt[i+1]&1) >> 1 ^ (odd ? 0x9908B0DF : 0) ^ mt[i+0x18C]`, a "
     "227-iteration loop then a 396-iteration loop~~ `y = (mt[i]&0x80000001) | (mt[i+1]&0x7FFFFFFE)`, "
     "`mt[i] = partner ^ (y >> 1) ^ (mt[i+1]&1 ? 0x9908B0DF : 0)`, with partner `mt[i+397]` (`[+0x634]`) for 227 "
     "iterations, then `mt[i-227]` (`[-0x38C]`) for `0x18C` = 396 iterations, then the last element against `mt[0]` — "
     "standard MT19937 *(corrected 2026-10-02, OPUS: checked at `0018EE30`–`0018EECA`; the old text swapped the split "
     "masks and used the second loop's count `0x18C` as the partner offset; CONTRACT-gameplay-generators.md §7)*,"),

    # C8: only the gameplay twist (00866B96) and the graphics seed (0018D746) test 01F44858; 0018EE20-0018EEDF does not.
    (RS, "**The SIMD branch is not a behavioural one.** Both twist functions test the dword at `01F44858`",
     "**The SIMD branch is not a behavioural one.** ~~Both twist functions test~~ The gameplay twist `00866B90` and the "
     "graphics seed `0018D740` test *(corrected 2026-10-02, OPUS: the tests are at `00866B96` and `0018D746`; the "
     "graphics twist `0018EE20`–`0018EEDF` has no rip-relative operand and no `01F44858` test)* the dword at "
     "`01F44858`"),

    # C9: 0062BCB0 and 0062EC70 are renderer helpers, not generators.
    (RS, "`0062BCB0` (647 B) is an RNG stream body - `01F7F590`/`01F7F5B8` state,",
     "`0062BCB0` (647 B) is ~~an RNG stream body - `01F7F590`/`01F7F5B8` state~~ a renderer helper, not a generator: it "
     "walks a `0x58`-stride element array off `[rbx+0x38]` and calls `0062EC70`, with no generator constant or "
     "recurrence; `01F7F590` is a `u32` read by nine functions and `01F7F5B8` a pointer set by `005A08E0` *(corrected "
     "2026-10-02, OPUS: checked at `0062BCB0`, 34 call sites in 22 functions; §8a's family-4 note lists it among the "
     "renderer's receivers)* -"),
    (RS, "`0062EC70` (204 B) is an RNG stream body - `0016D6D0`/`0016DA60` plus one vcall.",
     "`0062EC70` (204 B) is ~~an RNG stream body~~ an ordered-tree lookup, not a generator — `0x38`-stride buckets, "
     "`cmp [rax+0x20], rdx`, left/right descent *(corrected 2026-10-02, OPUS: checked at `0062EC70`; no generator "
     "constant or recurrence)* - `0016D6D0`/`0016DA60` plus one vcall."),

    # C10: two callers seed the LCG through area init (callers 002342F0 = 00266D10@00267136, 0026CE60@0026CEC6).
    (WR, "  - Its caller is **ActorEntity** `ActorSystem_InitializeManagerRuntime` (`0026CE60`).",
     "  - ~~Its caller is~~ Its callers are **ActorEntity** `ActorSystem_InitializeManagerRuntime` (`0026CE60`) and the "
     "broad bootstrap `00266D10`, which also advances the counter *(corrected 2026-10-02, OPUS: `callers 002342F0` = "
     "`00266D10` at `00267136` and `0026CE60` at `0026CEC6`)*."),

    # C11: the 15 LCG callers - four Spawn bodies plus SpawnKeep, and the ActorEntity / Movement / Gameplay five.
    (CG, "`Spawn_*` position and candidate selection (6 functions), `SpawnKeep_InitializeEntriesFromDefinitionTable`, "
         "`AiOrder_*` target resolution and precondition checks, `BattleUnit_SeedPartyCombatStanceRecheckTimer`, "
         "`BattleData_ResolveWeightedId` |",
     "`Spawn_*` position and candidate selection ~~(6 functions)~~ (four functions: `00234AF0`, `002355A0`, `00236450`, "
     "`002398F0`), `SpawnKeep_InitializeEntriesFromDefinitionTable`, `AiOrder_*` target resolution and precondition "
     "checks, `BattleUnit_SeedPartyCombatStanceRecheckTimer`, `BattleData_ResolveWeightedId`, and five more — `00236210` "
     "and `002394C0` (ActorEntity), `00239210` and `00312DF0` (Movement), `00312B40` *(corrected 2026-10-02, OPUS: the "
     "15 callers of `00328370`, checked with `retool callers`; which-roll-is-on-which-generator.md §3 note)* |"),

    # C12: CQ-5 answered - the presentation stream is inlined (UQ-276, procedural-stream-consumers.tsv, refs 01EF93E8).
    (RS, "than a signature. **That census is reported as an instrument failure, not a result**; the question of\n"
         "whether the presentation stream is inlined remains open as `CQ-5`.",
     "than a signature. **That census is reported as an instrument failure, not a result**; ~~the question of~~\n"
     "~~whether the presentation stream is inlined remains open as `CQ-5`.~~ *(answered: it is — seven more functions "
     "step the same recurrence inline, §4's census `UQ-276` (2026-09-26) and `procedural-stream-consumers.tsv`, ten "
     "functions touching `01EF93E8`, the count `refs 01EF93E8` also gives; 2026-10-02, OPUS)*"),

    # C13: families 3, 4 and 5 have been read since; only family 6 (Bullet) is unread.
    (RS, "> rest were **not read by the session that added these anchors**, and an address supplied from a name",
     "> rest were ~~**not read by the session that added these anchors**~~ not read by that session, and three of the "
     "four families behind them have been read since *(answered: family 3's `rand` census, with `LuaMath_Random*` and "
     "`BattleLocomotion_*`, in §8g; family 4's builder `001946E0` in §8a's note of 2026-09-14; family 5's "
     "`RNG_D_Phyre_GenerateRandomFloat01`, `006B05E0`, in §12 (2026-09-19); only family 6, "
     "`BulletSequentialImpulseSolver_ResetRandomSeed`, stays unread; 2026-10-02, OPUS)*, and an address supplied from "
     "a name"),
    (RS, "Families 3-6 are recorded from GFZ annotation and function naming (tier 3); families 1 and 2 are\ntier 1.",
     "~~Families 3-6 are recorded from GFZ annotation and function naming (tier 3);~~ Family 6 alone is still recorded "
     "from GFZ annotation and function naming (tier 3) *(answered: families 3, 4 and 5 were read since — the `rand` "
     "census in §8g, the family-4 note below (2026-09-14) and §12 (2026-09-19); 2026-10-02, OPUS)*; families 1 and 2 "
     "are\ntier 1."),

    # C14: there is a fixed graphics state address, 01F7F600, passed as a literal lea at all four call sites.
    (WR, "  the gameplay MT, not enumerated. *Narrowed 2026-09-13 (§13):* **there may be no fixed address to\n  find.**",
     "  the gameplay MT, not enumerated. *Narrowed 2026-09-13 (§13):* **~~there may be no fixed address to~~\n"
     "  ~~find.~~** *(answered: there is one, `01F7F600` — every call site passes it as a literal `lea`, `0015BD13` and "
     "`0015BD1F` in `0015BCF0`, `0019483B` and `001948C9` in `001946E0`; CONTRACT-which-generator-serves-which-roll.md "
     "I5 and `EXP-144`; 2026-10-02, OPUS)*"),
    (WR, "difference, and it means the unknown may be mis-stated: there may be **no fixed graphics state\n"
         "address to enumerate.**",
     "difference, and it means the unknown may be mis-stated: ~~there may be~~ **~~no fixed graphics state~~\n"
     "~~address to enumerate.~~** *(answered: the fixed address is `01F7F600`, passed as a literal `lea` at all four "
     "call sites — CONTRACT-which-generator-serves-which-roll.md I5 and `EXP-144`; 2026-10-02, OPUS)*"),

    # C15: the twist initialises the graphics MT's index cells, and the seeder tail-jumps into it (0015BD2B).
    (RS, "  without writing a cursor, so who initialises that instance's index is **not** established.",
     "  without writing a cursor, ~~so who initialises that instance's index is **not** established~~ and its caller "
     "then tail-jumps into the twist, which writes both index cells *(answered: `0018EE20` sets `+0x9C8` = 624 at "
     "`0018EECD` and `+0x9C0` = the array at `0018EED8`, and the seeder `0015BCF0` jumps there at `0015BD2B`; "
     "CONTRACT-which-generator-serves-which-roll.md I5; 2026-10-02, OPUS)*."),

    # C16: 01FD4A80's role is answered (the dispatched-frame counter, inc at 0022A59F); only the runtime value is open.
    (WR, "- **What `01FD4A80` holds** — the second input to the save-load seed; it is in the zero-filled tail of",
     "- ~~**What `01FD4A80` holds**~~ **Its runtime value** *(answered: what `01FD4A80` holds is the dispatched-frame "
     "counter, `inc` at `0022A59F` — CONTRACT-gameplay-generators.md §14 and "
     "CONTRACT-which-generator-serves-which-roll.md §14; 2026-10-02, OPUS)* — the second input to the save-load seed; it "
     "is in the zero-filled tail of"),

    # C17: a fresh boot has a fixed seed, not an established position (CG section 9 narrowed 2026-09-14; 0022B706 /
    #     0022B7EB discarded draws; camera-shake float draws, CG section 12c).
    (CW, "differs per generator: the **PRNG** and the **boot MT** are constant-seeded and reproducible; the",
     "differs per generator: the **PRNG** and the **boot MT** are constant-seeded ~~and reproducible~~ — the boot MT's "
     "seed is fixed but its position at the first gameplay draw is not established *(corrected 2026-10-02, OPUS: the "
     "boot frame modes draw and discard at `0022B706` / `0022B7EB` once per dispatch, and camera shake's float draws "
     "advance the same cursor; CONTRACT-gameplay-generators.md §9, narrowed 2026-09-14, and §12c)*; the"),
    (CG, "calls). **The gameplay MT is seeded from a fixed constant at startup**, so a fresh run is\n"
         "deterministic — and 4537",
     "calls). **The gameplay MT is seeded from a fixed constant at startup**, so ~~a fresh run is~~\n"
     "~~deterministic~~ a fresh run has a fixed seed but not an established position *(corrected 2026-10-02, OPUS: §9's "
     "fresh-boot row, narrowed 2026-09-14 — the boot frame modes draw and discard at `0022B706` / `0022B7EB`, and camera "
     "shake's float draws advance the same cursor, §12c)* — and 4537"),

    # C18: the LCG also carries loot and the enemy chain (seven inliners; rng-streams.md struck the split at section 8b).
    (CG, "**the LCG is the SPAWN and AI-ORDER generator and the MT is the COMBAT-FORMULA generator**, and",
     "**~~the LCG is the SPAWN and AI-ORDER generator~~ the LCG is the spawn, AI-order, loot and enemy-chain "
     "generator *(corrected 2026-10-02, OPUS: seven loot and chain functions inline it — 21 `0x41C64E6D` sites in 7 "
     "functions, besides the 3 in `00328370`; rng-streams.md struck the call-census split in §8b and restated it in §8c)* and the MT is the "
     "COMBAT-FORMULA generator**, and"),

    # C19: README against the folder - the three pages it did not list, with each page's own front-matter status.
    (R, "- [`rng-streams.md`](rng-streams.md) - the two independent random streams\n",
     "- [`rng-streams.md`](rng-streams.md) - the ~~two independent random streams~~ generators, at least eight, and "
     "their streams *(corrected 2026-10-02, OPUS: rng-streams.md's opening line and §10)* — **AUDITED**\n"
     "- [`which-roll-is-on-which-generator.md`](which-roll-is-on-which-generator.md) - which roll is on which "
     "generator, and what reseeds each — **AUDITED**\n"
     "- [`CONTRACT-gameplay-generators.md`](CONTRACT-gameplay-generators.md) - the shared LCG and the gameplay MT19937, "
     "draw for draw — **DIFFERENTIAL TESTED** (the algorithm only)\n"
     "- [`CONTRACT-which-generator-serves-which-roll.md`](CONTRACT-which-generator-serves-which-roll.md) - the routing "
     "of consumers to generators — **BEHAVIORALLY UNDERSTOOD**\n"
     "- *(corrected 2026-10-02, OPUS: three pages this list omitted, added with the status or readiness each page's "
     "own front matter states)*\n"),

    # C20: rng-streams.md had two section 8s and two section 9s. The second 8 (Reopened) becomes 8a, which its three
    #     "section 8" references mean; the first 9 (Related) becomes 8h, so "section 9" means the falsification pass.
    (RS, "> **Corrected 2026-09-02 (section 8).**",
     "> **Corrected 2026-09-02 (section ~~8~~ 8a *(corrected 2026-10-02, OPUS: renumbered, this document had two "
     "§8s)*).**"),
    (RS, "> **Corrected 2026-09-02 (see section 8).**",
     "> **Corrected 2026-09-02 (see section ~~8~~ 8a *(corrected 2026-10-02, OPUS: renumbered, this document had two "
     "§8s)*).**"),
    (RS, "exclusivity; section 8 documents",
     "exclusivity; section ~~8~~ 8a *(corrected 2026-10-02, OPUS: renumbered, this document had two §8s)* documents"),
    (RS, "## 8. Reopened 2026-09-02 - six families, and a correction\n",
     "## 8a. Reopened 2026-09-02 - six families, and a correction *(renumbered 2026-10-02, OPUS: this document had two "
     "§8s; §8 is the evidence table)*\n"),
    (RS, "## 9. Related\n",
     "## 8h. Related *(renumbered 2026-10-02, OPUS: this document had two §9s; §9 is the falsification pass of "
     "2026-09-07)*\n"),

    # C21: CW's method and evidence lines against its own pass 1 (2026-09-29) and EXP-144.
    (CW, "    scoped this contract on 2026-09-20 and did not re-derive the bodies.\n",
     "    scoped this contract on 2026-09-20 and did not re-derive the bodies.   # <- corrected 2026-10-02, OPUS - "
     "falsification pass 1 (2026-09-29) re-derived every static claim from the shipping image, and EXP-144 executed "
     "the routing (section 13)\n"),
    (CW, "Entirely the page's, including its two published corrections",
     "~~Entirely the page's~~ The page's readings, re-derived from the shipping image in falsification pass 1 "
     "(2026-09-29, below) and executed for the routing in `EXP-144` (§13) *(corrected 2026-10-02, OPUS: the pass "
     "re-derived every static claim, `falsify_which_generator.py`)*, including its two published corrections"),
    (CW, "> settles. Nothing here is executed.",
     "> settles. ~~Nothing here is executed.~~ The routing was executed in `EXP-144` (§13) *(corrected 2026-10-02, "
     "OPUS: `EXP-144`, `s46-generator-routing`, 9 cases, superseded §13's nothing-executed line on 2026-09-22)*."),

    # C22: byte[02EB4234] is a lazy-init latch (00863C84 test, 00863C99 seed 5489, 00863CBA set 1).
    (CG, "| `00863C80` | `byte[02EB4234]` debug gate;",
     "| `00863C80` | `byte[02EB4234]` ~~debug gate~~ lazy-seed latch, `GeneratorInitLatch` *(corrected 2026-10-02, "
     "OPUS: `00863C84` tests it, `00863C99` seeds 5489, `00863CBA` sets it to 1 — a do-once latch; §2 and "
     "CONTRACT-which-generator-serves-which-roll.md §3)*;"),

    # C23: review dates and audit counters - a trailing YAML comment, no value changed (the counters are the audit
    #     lane's to advance). CG's crossref_clean: false states nothing the bytes refute and is left alone.
    (RS, "last_reviewed: 2026-09-02\n",
     "last_reviewed: 2026-09-02   # <- corrected 2026-10-02, OPUS: the last whole-page review, not the last change - "
     "the body carries dated edits through 2026-09-28\n"),
    (WR, "last_reviewed: 2026-09-03\n",
     "last_reviewed: 2026-09-03   # <- corrected 2026-10-02, OPUS: the last whole-page review, not the last change - "
     "the body carries dated edits through 2026-09-26\n"),
    (WR, "  reopened_count: 0\n",
     "  reopened_count: 0   # <- corrected 2026-10-02, OPUS: not advanced for the two adjudicated corrections of "
     "2026-09-14 (sections 3 and 5)\n"),
    (CG, "last_reviewed: 2026-09-11\n",
     "last_reviewed: 2026-09-11   # <- corrected 2026-10-02, OPUS: the last whole-page review, not the last change - "
     "the body carries additions through 2026-09-22 (section 14)\n"),

    # X1: 00861F38 is jmp qword ptr [008C3098] - the imported rand, not a statically linked one.
    (RS, "| **statically linked** `rand` | `0x00861F38` |",
     "| ~~**statically linked** `rand`~~ an import thunk, `jmp qword ptr [008C3098]` — the same imported `rand` and "
     "per-thread state *(corrected 2026-10-02, OPUS: checked at `00861F38`)* | `0x00861F38` |"),

    # X2: srand (IAT 008C30A0) has two callers - 007A540B (thread entry 007A5400, QPC microseconds via 007AD680) and
    #     Lua's 008193E0; "not reproducible across runs" holds only on that thread or after math.randomseed.
    (RS, "the counter-seeded shared LCG it is **not reproducible across runs** from saved state.",
     "the counter-seeded shared LCG it is **~~not reproducible across runs~~** irreproducible from saved state on the "
     "one thread that seeds it, or after a script `math.randomseed` *(corrected 2026-10-02, OPUS: `srand` (IAT "
     "`008C30A0`) has two callers — `007A540B`, at the entry of the thread function `007A5400` (installed at "
     "`02EACF78` beside `_beginthreadex` at `007A5232`), seeding from QueryPerformanceCounter microseconds through "
     "`007AD680`, and Lua's `math.randomseed` `008193E0`; any other thread's `rand` is never `srand`-ed outside Lua)*."),

    # X3: stream 5 can return exactly 1.0 (cvtsi2ss of a zero-extended u32, mulss by 2^-32, 006B061E-006B0623).
    (RS, "result = (float) r * 2^-32            in [0, 1)\n",
     "result = (float) r * 2^-32            in [0, 1)   <- corrected 2026-10-02, OPUS: in [0, 1] - cvtsi2ss of the "
     "zero-extended u32 rounds any r >= 0xFFFFFF80 to 2^32, so the mulss by 0x2F800000 (2^-32) returns exactly 1.0 "
     "(006B061E-006B0623)\n"),

    # X4: stream 5's pointer holder - 006B04B0 stores 006B05E0 at 02E502A8 (006B059F / 006B05A6).
    (RS, "it is reached through a pointer, and who holds that pointer was not\nestablished.",
     "it is reached through a pointer, ~~and who holds that pointer was not~~\n~~established~~ *(answered: `006B04B0` "
     "stores `006B05E0` at `02E502A8` (`006B059F` / `006B05A6`), in a static object at `02E502A0` with `00D34C08` at "
     "`+0` and `02E50298` → `02E502A0`; `006B04B0` is reached from `006B0300` (`jmp`) and `005A08E0`; 2026-10-02, "
     "OPUS)*."),

    # X5: the mixer's inputs - rcx = _time64(NULL) (008C3060), edx = clock() (008C3068), 0015BCF6-0015BD0C.
    (RS, "time-and-clock seeder of the graphics-noise twister. *Which bytes of the two arguments are the time and which "
         "the\nclock was not traced.*",
     "time-and-clock seeder of the graphics-noise twister. *~~Which bytes of the two arguments are the time and which "
     "the~~\n~~clock was not traced.~~* *(answered: the first argument is the time and the second the clock — "
     "`0015BCF6`–`0015BD0C` pass `rcx = _time64(NULL)` (IAT `008C3060`) and `edx = clock()` (IAT `008C3068`); "
     "2026-10-02, OPUS)*"),

    # X6: the reseed gate's only writers - 002368D0 (clear, once, from boot at 0022A41A) and 00236A40 (set, once, from
    #     boot frame mode 0 at 0022B77C). A code reading, not an observation.
    (WR, "  answer to *\"can it be false\"* is **yes, by construction**; whether that path precedes an area\n"
         "  init in normal play is a runtime question and is not established.",
     "  answer to *\"can it be false\"* is **yes, by construction**; ~~whether that path precedes an area~~\n"
     "  ~~init in normal play is a runtime question and is not established.~~ *(answered from the code, not observed: "
     + GATE + "; 2026-10-02, OPUS)*"),
    (WR, "**Whether that clear precedes an area init\nin normal play is a runtime question and is not answered here** — but",
     "**~~Whether that clear precedes an area init~~\n~~in normal play is a runtime question and is not answered "
     "here~~** *(answered from the code, not observed: the clear runs once, from boot at `0022A41A`, and the set once, "
     "from boot frame mode 0 at `0022B77C`; 2026-10-02, OPUS)* — but"),
    (CW, "so the gate is reachable in code; **whether it is ever false\n  in normal play is not established** **[page]**.",
     "so the gate is reachable in code; **~~whether it is ever false~~\n  ~~in normal play is not established~~** "
     "**[page]** *(answered from the code, not observed: " + GATE + "; 2026-10-02, OPUS)*."),
    (CW, "* **Whether `DAT_02089300` is ever false in play** (§10) **[live]**.",
     "* ~~**Whether `DAT_02089300` is ever false in play** (§10) **[live]**.~~ *(answered from the code, not observed: "
     + GATE + "; only a live capture would confirm it; 2026-10-02, OPUS)*"),

    # X9: 0018D740 has two +0x9BC operands (0018D761 lea rdx,[rcx+0x9bc]; 0018D76C lea r10,[r9+0x9bc]).
    (CW, "`0018D740` has one operand there, `lea rdx, [rcx + 0x9bc]`, the array's",
     "`0018D740` has ~~one operand~~ two operands there, `lea rdx, [rcx + 0x9bc]` and `lea r10, [r9 + 0x9bc]` "
     "*(corrected 2026-10-02, OPUS: `0018D761` and `0018D76C`)*, the array's"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
