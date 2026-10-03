---
contract: draw from the two gameplay-affecting generators, exactly, including the parts that look wrong and are not
category: 21-RNG-And-Determinism
scope: family
readiness: DIFFERENTIAL TESTED   # the ALGORITHM only; the streams the game actually sees are not — see §13
confidence: PROVEN
implements: 21-RNG-And-Determinism/rng-streams.md
entries: ["00328370", "00328D80", "00863BF0", "00863C80", "00863D30", "00866B90", "00866D60",
          "00379CD0", "00379CE0", "00379CF0"]
verified_against:
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
  method: address-resolution verification 2026-09-14 (OPUS) - 82 addresses cited - 12 data, 14 entry, 56 interior, every one resolving
    into a known section of the authority image. **This records a check performed on
    that date, NOT the method of the original derivation**, which this block never
    carried; see this document's own Evidence section and `audit.last_pass_state`
    for that.
last_reviewed: 2026-09-11   # <- corrected 2026-10-02, OPUS: the last whole-page review, not the last change - the body carries additions through 2026-09-22 (section 14)
audit:
  passes: 1                    # falsification passes survived. 0 = NOT yet fact.
  last_pass: 2026-09-12        # YYYY-MM-DD
  last_pass_state: opus-rng-pass-1           # snapshot SHA the pass ran against
  crossref_clean: false        # audit_crossrefs.py reports nothing for this document
  reopened_count: 0
---

# Contract — the two gameplay generators

Determinism is the one subsystem a reconstruction cannot be approximately right about. A wrong
constant, a wrong number of steps per draw or a wrong bit order does not degrade gracefully — it
diverges on the first roll and every comparison after it is meaningless.

**Scope, stated first because it is narrower than the category.** This contract covers the two
generators whose bodies were read end to end: the **shared LCG** at `022C256C` and the **gameplay
MT19937** at `02EB3870`. `rng-streams.md` records ~~six families; the other four~~ at least eight generators *(corrected 2026-10-02, OPUS: the GFZ's six families, the presentation PRNG and the PPFX xorshift128 `0074BDE0`, checked at `0074BFE0`–`0074C0C4`)*; the others are not specified
here, and nothing below should be read as covering them.

The first contract in `21-RNG-And-Determinism`.

## 1. Purpose

To state each generator exactly enough that a reimplementation can be compared draw for draw, and to
record the two places where the binary looks like it disagrees with a textbook and does not.

## 2. Interface

| | |
|---|---|
| LCG draw | `00328370` — no arguments, returns a 31-bit value in `eax` |
| LCG seed | `00328D80` — `ecx` = seed, writes it and returns |
| MT draw | `00863BF0`, reached through the thunk `00379CD0` — returns `u32` |
| **MT float draw** | **`00863C80`, reached through the thunk `00379CE0` — returns `float` in `xmm0`, and ADVANCES THE SAME CURSOR** |
| MT seed | `00863D30`, reached through `00379CF0` — `ecx` = seed |
| MT seed impl | `00866D60` — `edx` = seed; both seed paths and both draw paths reach it |
| MT twist | `00866B90` — called from either draw when the cursor is exhausted |

> **⚠ The float draw was added 2026-09-11 and the omission was not cosmetic.** This table listed
> five entries and the reproduction formula in §12 gave two. `00863C80` repeats `00863BF0`
> instruction for instruction — the same lazy-seed flag, the same twist test, the same tempering —
> and then scales the tempered word into a float. **It takes a word from the shared cursor.** A
> reimplementation built from the old table stays in step only until the first consumer calls the
> float entry, and is then off by one for the rest of the stream: a divergence that presents as a
> wrong formula and is a missing entry point. Found by a caller census, not by re-reading the
> draw; `00379CE0` sits between the two thunks this contract already named, in the same padded
> block of three.

**Calling convention, for all seven.** `__fastcall`/x64, caller-cleaned, no arguments beyond the
one named. `00863BF0`, `00863C80` and `00863D30` each construct a temporary object in their own
argument home area (`[rsp+0x30]`, first qword a vtable — `01CCFAC8`, and `01CCFAD8` in the float
path after the seed call) and pass a pointer to it as `this` to the twist and the seed impl.
**Neither callee ever dereferences it**: `00866B90`'s second instruction is `xor ecx, ecx` and
`00866D60` takes its seed in `edx`. The generator state is entirely in image statics and the
object is vestigial. Checked mechanically on every harness run, with a positive control.

## 3. Types

| | |
|---|---|
| `SharedGameplayLcgState` | `u32` at `0x022C256C` — the whole state |
| `Mt19937State` | `0x9C4` at `0x02EB3870`: `mt[624]` at `+0x000`, `index` at `+0x9C0` (absolute `02EB4230`) |

**And one byte that is not in the type.** `0x02EB4234` — immediately after the state, one dword past
its declared size — is a **lazy-seed flag**. It is not part of `Mt19937State` and a reconstruction
that omits it diverges on the first draw of a stream nobody seeded; see §7.

## 4. Preconditions · postconditions · invariants

There are no preconditions: both draws are callable at any time and neither validates anything.

**The invariant that matters is the step count.** One call to the LCG draw advances its state by
**three** multiply-add steps, not one. Anything predicting or replaying the stream must count draws,
not steps.

## 5. State

`022C256C` for the LCG; `02EB3870`+`02EB4230`+`02EB4234` for the MT. Both are image statics, never
allocated and never freed.

**All four lie past `SizeOfRawData`, in `.bss`.** Their load-time value is therefore zero, and
that is the initial state of both streams — including the lazy-seed flag, which is *why* an
unseeded MT stream self-seeds. This is not a detail: it means "the state before anything runs" is
a defined value a reconstruction and a replay can both start from, and the differential harness
does start from it.

## 6. Relationships

**Measured 2026-09-11 by a call-site census** — disassembly from every recorded function entry
bounded by the recorded body length, never a linear `.text` sweep, with `memcpy` as a positive
control returning 637 sites. Counts exclude `CompilerGeneratedEH` bodies.

| | sites | functions | what they are |
|---|---:|---:|---|
| LCG draw `00328370` | 23 | 15 | `Spawn_*` position and candidate selection ~~(6 functions)~~ (four functions: `00234AF0`, `002355A0`, `00236450`, `002398F0`), `SpawnKeep_InitializeEntriesFromDefinitionTable`, `AiOrder_*` target resolution and precondition checks, `BattleUnit_SeedPartyCombatStanceRecheckTimer`, `BattleData_ResolveWeightedId`, and five more — `00236210` and `002394C0` (ActorEntity), `00239210` and `00312DF0` (Movement), `00312B40` *(corrected 2026-10-02, OPUS: the 15 callers of `00328370`, checked with `retool callers`; which-roll-is-on-which-generator.md §3 note)* |
| LCG seed `00328D80` | **1** | **1** | `BattleSystem_InitializeAreaState` at `00234320` — see §7 |
| MT draw thunk `00379CD0` | 98 | 66 | overwhelmingly `BattleFormula_*`: knockback, guard/parry, combo count, poach selection, the four `Prepare*AttackVsDefense` variants, status masks and timers |
| MT seed thunk `00379CF0` | 2 | 2 | a boot-time init call and a save-load tail jump — see §7 |
| **MT FLOAT draw thunk `00379CE0`** | **9** | **1** | **camera shake, and nothing else in the image.** The sampler `0037D1F0`, whose nine sites are **sixteen draws per evaluation** — one site sits in a loop of eight. **This row was missing from the census until 2026-09-19; see §12c** |


This replaces the earlier prose, which named `BattleData_ResolveWeightedId` and `0025ACA0` as
examples. Both survive the census — but the shape it shows is sharper than "a gameplay stream":
**~~the LCG is the SPAWN and AI-ORDER generator~~ the LCG is the spawn, AI-order, loot and enemy-chain generator *(corrected 2026-10-02, OPUS: seven loot and chain functions inline it — 21 `0x41C64E6D` sites in 7 functions, besides the 3 in `00328370`; rng-streams.md struck the call-census split in §8b and restated it in §8c)* and the MT is the COMBAT-FORMULA generator**, and
they barely overlap in consumers.

Because many consumers share each state, a later value cannot be predicted from the seed alone
without replaying every intervening draw — and, per §2, the replay must include the float draws.

> **Crossings the census table does not name — FINAL-AUDIT pass 22 (FABLE, 2026-09-14).**
>
> - **CoreRuntimeScheduling.** The boot seed sits in `0022A0B0`, which the game application's init burst `0017D4C0`
>   calls. `0022A0B0` also calls the frame-base selector `0022BDF0`. **Two of the
>   MT draw thunk's 66 callers are the boot frame modes.** Mode 0 `0022B6E0` calls `00379CD0` at `0022B706`, and mode 1
>   `0022B7E0` calls it at `0022B7EB`. Each draws once per entry and discards the value: the next call takes no argument
>   from `eax`. The frame-mode switch `0022A580` enters one mode body per dispatch. Mode 0 stays current until
>   `0032E520(1) == 0 && [0209273C] == 5`, and mode 1 until `0032E520(1) == 0 && 0037C2E0() == 0`
>   ([between two frames](../22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md) §2.2). **So by the
>   time a fresh boot reaches mode 2, the MT has already advanced once for every dispatch spent in mode 0 and once for
>   every dispatch spent in mode 1.** §9's fresh-boot row, *deterministic across runs: yes*, therefore needs a condition: it holds only if those
>   two dispatch counts are the same on every run. They wait on load conditions, and whether they vary is a runtime
>   question this contract does not answer. *Narrowed, not withdrawn.*
> - **Rewards_Progression_Economy.** The level-up growth functions `002F9A60` (HP) and `002F9B20` (MP) draw the MT
>   for their random bonus below a fifth of the table base
>   ([what happens when a character levels up](../13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md)).
>   They are two of the census's non-`BattleFormula_*` MT consumers.
> - **PlatformOnlineAchievements.** On the save-load path, `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG`
>   (`00584210`) calls `00316810` at `00584398`, immediately before `_time64` and the MT reseed. `00316810` is a pass
>   over the achievement counters. It re-reads each counter through `00316760` and rewrites any that read at or above
>   `0x7FFFFFFF` (4-byte kind) or `0x7FFF` (2-byte kind)
>   ([version stamps and what loading normalises](../19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/version-stamps-and-what-loading-normalises.md)).
>   It neither draws on nor seeds either generator: no path reaches a draw or seed body within six levels of the call
>   graph, and indirect calls were not followed.

## 7. State transitions

**The LCG draw — three steps, and this is the part most likely to be got wrong.**

```
s1 = state * 0x41C64E6D + 0x3039           00328370, 0032837A
s2 = s1    * 0x41C64E6D + 0x3039           0032837F, 00328393
s3 = s2    * 0x41C64E6D + 0x3039           00328399, 003283B4
state = s3                                 003283B9   <- the only writeback

a = ((s1 >> 16) & 0x7FF) << 10             00328385-00328390   11 bits
b =  (s2 >> 16) & 0x3FF                    0032839F-003283A6   10 bits
c =  (s3 >> 16) & 0x3FF                    003283BF-003283C2   10 bits

return c ^ (((b ^ a) << 10))               003283AD, 003283B0, 003283C7
```

`0x41C64E6D` and `0x3039` are the ANSI C `rand()` constants exactly. **The result is 31 bits
assembled from three consecutive draws with XOR, not OR, and the middle term is shifted twice** —
once as `a`, and again with `b` folded into it. A reimplementation that took one step per call, or
used OR, or assembled the three 10/11-bit fields in a different order, would produce plausible
random numbers and a different game.

**Where the three seeds actually come from — established 2026-09-11, and §14's open question
about this is now closed.**

```
LCG,  once per area init   00234301  eax = [0208E6B0]        a counter
                           00234307  ecx = eax               the seed is the PRE-increment value
                           00234309  eax = eax + 1
                           00234315  [0208E6B0] = eax
                           00234320  call 00328D80
```

**The LCG's seed is the number of area initialisations so far**, not a clock and not a constant,
and `BattleSystem_InitializeAreaState` is its only caller anywhere in the image. So the LCG stream
is *reproducible from a counter a replay can hold*, and it restarts at every area init — which is
what makes spawn placement repeatable across a reload of the same area at the same count, and
different at a different count.

```
MT, at boot                0022A40B  ecx = 0x11B9            4537, a literal
                           0022A410  call 00379CF0
```

seeded inside a long sequential subsystem-initialisation function (`0022A0B0`, ~40 consecutive
calls). **The gameplay MT is seeded from a fixed constant at startup**, so ~~a fresh run is~~
~~deterministic~~ a fresh run has a fixed seed but not an established position *(corrected 2026-10-02, OPUS: §9's fresh-boot row, narrowed 2026-09-14 — the boot frame modes draw and discard at `0022B706` / `0022B7EB`, and camera shake's float draws advance the same cursor, §12c)* — and 4537 is *not* 5489: the lazy default in §7 is never what a real session uses.

```
MT, on save load           0058439F  call [008C3060]         api-ms-win-crt-time-l1-1-0!_time64
                           005843A5  ecx = (u32)(t + 0x2B5A5)
                           005843AB  rax = t >> 32           arithmetic
                           005843AF  ecx = ecx * 0x21
                           005843B2  ecx = ecx + (u32)rax
                           005843B4  eax = [01FD4A80] * 0x258  session frame counter (§14)
                           005843BE  ecx = ecx & ~(1u << 31)
                           005843C2  ecx = ecx + eax
                           005843D3  jmp 00379CF0            a TAIL jump, so ecx is the seed
```

in `SaveLoad_NormalizeLoadedRuntimeStateAndReseedRNG` (`00584210`). The import is named from the
image's own import table (538 slots parsed; its neighbours are `_gmtime64` and `clock`), not
inferred from the `xor ecx, ecx` argument. **See §9: this is the one place the subsystem reads a
clock, and it is reached by a tail jump that a `call`-only sweep does not see.**

**The MT draw.**

```
if (byte [02EB4234] == 0)  seed(0x1571)    00863BF4-00863C13   <- 5489, the MT19937 default
byte [02EB4234] = 1                        00863C1E
if (index == 0x270)  twist(); reload index 00863C25-00863C37   <- 624, exhausted
y = mt[index]; index++                     00863C3D-00863C4F
```

**And the seed implementation leaves the cursor EXHAUSTED, which the earlier revision of this
contract did not record.** `00866D60` is stock `init_genrand` — `mt[0] = seed`, then
`mt[i] = 0x6C078965 * (mt[i-1] ^ (mt[i-1] >> 30)) + i` for `i` in 1…623 — and then:

```
00866D98  mov dword ptr [02EB4230], 0x270
```

so the cursor is 624, not 0, and **the next draw twists before it returns anything**. A
reconstruction that set the cursor to 0 after seeding would return an un-twisted `mt[0]` on draw
one, from a correct seed routine and a correct twist. The differential harness kills that mutant
explicitly: 1,289 mismatches on a 40-draw script.

The lazy seed is the trap. **An unseeded stream seeds itself with 5489 on its first draw, not with
zero and not with a clock**, and the flag that decides this lives outside the state structure. The
seed entry `00863D30` performs the same lazy default *before* applying the caller's seed, so the
default is immediately overwritten there — it is only observable on a stream that is drawn from
before it is ever seeded.

**The tempering, which LOOKS wrong and is not.** The binary does:

```
y ^= y >> 11                               00863C54
y ^= (y & 0xFF3A58AD) << 7                 00863C5B-00863C63
y ^= (y & 0xFFFFDF8C) << 15                00863C67-00863C6F
y ^= y >> 18                               00863C73
```

The textbook constants are `0x9D2C5680` and `0xEFC60000`, and **neither appears in this binary**.
Someone checking constants against the reference would find two unknown masks and conclude the game
uses a modified tempering. It does not: the compiler applied the mask **before** the shift, and

```
0xFF3A58AD << 7  = 0x9D2C5680     (mod 2^32)
0xFFFFDF8C << 15 = 0xEFC60000     (mod 2^32)
```

so `(y & M) << k` is `(y << k) & (M << k)` with `M << k` being exactly the textbook mask. **This is
stock MT19937 tempering**, and this paragraph exists so that nobody has to rediscover that.

**The twist, `00866B90` — and there are two of them.**

```
00866B94  xor   ecx, ecx                    ; the cursor starts at 0
00866B96  cmp   dword ptr [01F44858], 2
00866B9D  jl    00866C89                    ; SKIP THE PREFIX - ecx stays 0
00866BC4  mov   ecx, 0xe0                   ; the prefix will cover 224 elements
          ...                               ; SSE, eight dwords per pass (add rax,0x20),
                                            ; xmm6 = 0x9908B0DF broadcast (00866BC9)
00866C89  movsxd rcx, ecx                   ; <-- BOTH PATHS ARRIVE HERE
00866C93  cmp   rcx, 0xe3                   ; 227
00866CA3  lea   r8, [rdx + rcx*4]           ; the scalar loop STARTS AT rcx
```

The scalar loop is stock MT19937 and three constants prove it independently:

| | |
|---|---|
| `0x9908B0DF` | `MATRIX_A`, applied branchlessly as `imul ecx, ecx, 0x9908b0df` on a 0-or-1 select (`00866CC2`) |
| `0x634 / 4 = 397` | `M`, as the displacement of the xor partner — `xor edx, dword ptr [r8 + 0x634]` (`00866CCF`) |
| `227` | `624 - 397`, the first loop's bound: `02EB3BFC - 02EB3870 = 0x38C` = 227 dwords (`00866C8C`, `00866C93`) |

**Unlike the tempering, `MATRIX_A` appears literally.** The two missing-constant situations in this
subsystem have opposite causes, and only one of them is a compiler transformation.

**A second looks-wrong-isn't.** The scalar twist splits the word pair with `0x80000001` and
`0x7FFFFFFE`; the textbook uses `0x80000000` and `0x7FFFFFFF`. The difference is bit 0 — here `y`'s
bit 0 comes from `mt[i]` rather than `mt[i+1]`. It cannot matter: bit 0 is shifted out by
`shr edx, 1` at `00866CCB`, and its only other use, the `MATRIX_A` select, is taken **separately**
from `mt[i+1]` at `00866CB9`. The code never consults `y`'s bit 0.

**It is a PREFIX, not an arm — CORRECTED 2026-09-19 (OPUS), from
[`EXP-111`](../_experiments/EXP-111-mt-twist-simd-exec.md).** The snippet above used to read
*"`jl` → the SCALAR loop … otherwise an SSE path"*, and this section called them *"two
implementations"*. **There is one loop.** `00866C89` is a join, not a branch target: `ecx` is `0`
when the guard skipped the vector section and `0xE0` when it ran, and the scalar loop begins at
`rcx` in both cases. **The vector section is a 224-element prefix and the scalar loop always runs
the remainder** — indices 224–226 of the first 227-element section, then the whole second section.
`EXP-111` drives it directly: flipping the guard (`jl` → `jge`) makes flag `1` run *both* the
prefix and the full scalar loop, and the resulting state is still byte-identical. **A
reconstruction that implements this as "pick one of two loops" is wrong in shape even though it
lands on the right answer** — and it will read the `0xE0` as a magic number instead of a cursor.

**Two code paths, and they are compiler output — CORRECTED 2026-09-11.** `01F44858` is the
MSVC CRT's `__isa_available`, written only by `__isa_available_init` with `1`, `2`, `3` or `5` and
read at nineteen sites across the binary, almost all of them CRT or compiler-generated code using
this identical `cmp ..., 2` shape. So the two twists are **one source loop, auto-vectorised**, with
the ISA guard MSVC emits everywhere — not a decision anyone in this game made.

An earlier revision of this contract called that "a determinism property in its own right" and
warned that the paths might produce different sequences on different machines. **That was
overstated.** The paths agree because semantics-preserving vectorisation is what the transformation
means.

> **AND THAT ARGUMENT IS NOW UNNECESSARY, WHICH IS THE POINT.** *"Vectorisation is
> semantics-preserving"* is a claim about what compilers are supposed to do, not about this binary.
> `EXP-111` executed both paths over **eight planted 624-word states** — zeros, ones, incremental,
> PRNG-random, lsb-alternating, high-bit-only, mixed-edge, and the standard seed 5489 — and every
> one comes out **bit-exact under both guard values and against an independent reference**. The
> equivalence is measured. A reader no longer has to trust the compiler to trust this contract.
>
> The mask difference is covered by the same pass: patching the scalar mask's bit 0 changes
> nothing, which is the positive control for the paragraph above. The fact remains worth recording here only as a **reading aid**: someone disassembling
`00866B90` lands in SSE code, and should know the scalar loop below it is the same algorithm, is
the one to read, **and runs in both cases**.

**One more thing execution pinned:** `mti` is reset unconditionally — `d[02EB4230] = 0` on both paths, checked against a
`0xDEADBEEF` sentinel. A reconstruction must clear the cursor even when it takes the scalar path
only.

## 8. Script · resource · event interactions

None. Neither generator reads authored data.

## 9. Determinism

Both **draws** are deterministic given their state. Neither draw reads a clock, a frame counter or
any input.

**The seeding is where determinism is decided, and it is not uniform — EXTENDED 2026-09-11.**

| stream | seeded from | deterministic across runs? |
|---|---|---|
| LCG | an area-initialisation counter at `0208E6B0` | **yes**, given the same counter value |
| MT, fresh boot | the literal `0x11B9` | **same seed, yes. Same position, NOT established** - the boot frame modes each draw once per dispatch and discard it (`0022B706`, `0022B7EB`), so the first gameplay draw sits at an offset equal to the dispatch count. Narrowed 2026-09-14 (OPUS adjudication), verified from the shipping bytes. |
| MT, after a save load | **`_time64(NULL)`**, folded with `[01FD4A80] * 600` — the session frame counter | **no** |

> **The earlier revision's sentence was true and is not enough.** It said *"neither reads a clock
> … on the paths read here"* — correctly scoped to the draws, which is all it had read. Extending
> that scope to the subsystem would have been wrong: **loading a save reseeds the gameplay MT from
> the wall clock.** Every combat-formula roll after a load therefore differs between two loads of
> the same save, and any replay, parity test or deterministic-rerun scheme must either capture the
> post-load seed or accept divergence from that point. This is recorded as an **extension, not a
> falsification** — no claim in this contract is withdrawn.

The reseed site is reached by a **tail jump**, `005843D3 jmp 00379CF0`. A `call`-only census would
have reported the MT seed as having a single boot-time caller and the whole clock dependency would
have stayed invisible; the census that found it counts jumps separately for exactly that reason.

## 10. Failure paths and edge conditions

- **Neither draw can fail.** There is no error return and no validation.
- **The LCG has no seeding discipline**: `00328D80` is a single store with no guard, so any caller
  can reset the shared state at any time and every consumer downstream is affected.
- **The MT's first draw on an unseeded stream is not an error path** but it is a distinct one, and
  it is invisible to anything that only inspects `Mt19937State` — the deciding byte is outside it.
- **`index == 624` is the twist condition**, tested with `jne`, so a cursor that somehow exceeded
  624 would read past the state vector. Nothing bounds it other than the twist resetting it.

## 11. Observable behaviour

**Established by execution 2026-09-11, at the isolated original-code class.** Running the shipped
bodies at their real virtual addresses over a command script, with the statics live between calls:

- one LCG draw advances `022C256C` by **three** multiply-add steps — read back and compared after
  every one of 768 draws;
- the MT cursor at `02EB4230` transitions **0 → 624 on seeding**, **624 → 0 on twisting**, and
  **+1 per draw through either entry**;
- the flag at `02EB4234` is one-shot: zero until the first draw or seed, `1` forever after, and
  nothing in either generator ever clears it;
- an unseeded stream's first 1,300 draws are **exactly** MT19937 seeded with 5489.

**Still not observable here:** any of this *in the running game*. What an emulated call cannot show
is which consumer draws when, and therefore what any particular roll in play was — see §13.

## 12. Reproduction formula

```c
static uint32_t lcg_state;            /* 0x022C256C */

uint32_t Rng_LcgDraw(void)            /* 00328370 */
{
    uint32_t s1 = lcg_state * 0x41C64E6Du + 0x3039u;
    uint32_t s2 = s1        * 0x41C64E6Du + 0x3039u;
    uint32_t s3 = s2        * 0x41C64E6Du + 0x3039u;
    lcg_state = s3;

    uint32_t a = ((s1 >> 16) & 0x7FFu) << 10;
    uint32_t b =  (s2 >> 16) & 0x3FFu;
    uint32_t c =  (s3 >> 16) & 0x3FFu;
    return c ^ (((b ^ a) << 10));
}

void mt_seed_impl(uint32_t seed)      /* 00866D60 — reached by BOTH seed and BOTH draw paths */
{
    mt[0] = seed;
    for (int i = 1; i < 624; ++i)
        mt[i] = 0x6C078965u * (mt[i - 1] ^ (mt[i - 1] >> 30)) + (uint32_t)i;
    mt_index = 624;                         /* 00866D98 — EXHAUSTED, so the next draw twists */
}

static uint32_t mt_next_tempered(void)  /* the shared body of 00863BF0 and 00863C80 */
{
    if (!mt_seeded) { mt_seed_impl(5489); } /* the flag at 0x02EB4234 */
    mt_seeded = 1;
    if (mt_index == 624) { mt_twist(); }
    uint32_t y = mt[mt_index++];
    y ^= y >> 11;
    y ^= (y << 7)  & 0x9D2C5680u;           /* == (y & 0xFF3A58AD) << 7  */
    y ^= (y << 15) & 0xEFC60000u;           /* == (y & 0xFFFFDF8C) << 15 */
    y ^= y >> 18;
    return y;
}

uint32_t Rng_MtDraw(void)             /* 00863BF0 */
{
    return mt_next_tempered();
}

float Rng_MtDrawFloatClosed(void)     /* 00863C80 — THE SAME CURSOR */
{
    /* The scale at 01CCFAE0 is 0x3DF0000000100000 == 1/(2^32 - 1), a CLOSED interval, and NOT
     * 1/2^32. The multiply is done in double and only the result is narrowed - `cvtsi2sd`,
     * `mulsd`, `cvtpd2ps` - which is not the same as multiplying in float. */
    return (float)((double)mt_next_tempered() * (1.0 / 4294967295.0));
}
```

**How wrong the easy mistake is, measured.** A reconstruction using `1/2^32` disagrees on only
**24 of 2,598** float draws — about 1% — because the two scales differ by one ULP and most results
round identically. It is caught, but only by a case set large enough; a handful of float cases
would pass with the wrong constant.

## 13. Runtime validation

**Evidence class: isolated original-code. Live capture: still absent.** (2026-09-11)
~~None. Neither generator has been executed under
observation, in any evidence class.~~ Both generators have now been executed — the shipped bodies,
at their real virtual addresses, under Unicorn, against an independent reconstruction.

**Instrument:** [`Reconstruction/Tests/Differential/diff_rng_generators.py`](../../../Reconstruction/Tests/Differential/diff_rng_generators.py)
against [`Reconstruction/Game/Rng/rng_generators.c`](../../../Reconstruction/Game/Rng/rng_generators.c),
on `FFXII_TZA.exe` `73461D08…` (size and SHA-256 both checked). Both sides replay the **same
command script** against live state, because every fact worth testing here is an ordering fact and
none of them survives being cut into independent cases.

**Result: 6,167 commands, 15,682 comparisons, 0 mismatches.** By kind: 7,270 `u32` draws, 2,598
float draws compared as bit patterns, 768 LCG state words, 4,992 MT vector words, 54 cursor/flag
readings.

| §13's own checks | outcome |
|---|---|
| 1. the LCG's three-step composition | **PASS** — value *and* state compared after every draw, over 24 seeds including 0, 1, `0x7FFFFFFF`, `0x80000000`, `0xFFFFFFFF` |
| 2. the MT lazy seed | **PASS** — a stream drawn with `02EB4234` clear matches MT19937 seeded 5489 for 1,300 draws, and matches an explicitly-5489-seeded stream word for word |
| 3. the two twists agree | **PASS** — `__isa_available` forced to 1 and to 5 over the same vector; 0 of 624 words differ, and a control confirms the twist changed all 624 (so the agreement is not two no-ops agreeing) |

**Claims about the bytes, re-derived on every run rather than inherited:** three `imul 0x41C64E6D`
and three `add 0x3039` in `00328370`; `0xFF3A58AD` and `0xFFFFDF8C` present as immediates with
their shift identities computed, and **neither textbook constant present literally**; zero
`rcx`-based memory operands in `00866B90`/`00866D60` against a control of 49 register-based
operands.

**The harness was shown to have teeth, not assumed to.** Four deliberately wrong reconstructions
were built and run: a two-step LCG (24 mismatches), a cursor-0-after-seed (1,289), a `1/2^32`
float scale (24), and a float draw on a private stream (40 — the arrangement that proves the
cursor is shared is the *interleaved* script, not a run of floats).

**What this is NOT.** It is isolated original-code evidence, not live evidence, and the distinction
is load-bearing here rather than pedantic:

- **Nothing observed the game.** No consumer ran. Which roll belongs to which draw, and what any
  particular outcome in play was, remains unobserved.
- **`readiness` moved to `DIFFERENTIAL TESTED` and this subsystem is NOT entitled to the shortcut
  that `field_music` took.** The audit log's rule is explicit — *"an entity with state, timing or
  RNG cannot take this shortcut"* — and this entity has state and **is** the RNG. The value moved
  because the *algorithm* is now differentially tested end to end; **`RUNTIME VALIDATED` is not
  claimed and is still owed**, for the consumer ordering and for the post-load reseed in §9, both
  of which need a live process.
- **The save-load reseed was read, not run.** `_time64` was not called under observation.

This is, however, the subsystem where **isolated original-code execution would be nearly free and
decisive**: both draws are self-contained, take no arguments, touch only two statics and return a
value. Seeding a known state and comparing a few hundred draws against the formulas above would
settle the whole contract in one run — and `EXP-013` has already demonstrated the harness for
exactly this shape, running original bytes under Unicorn with a SHA-gated reader.

**What is still owed, and it is live-only.** Three things, each with the decision it blocks:

1. **The post-load MT seed.** Read `02EB3870`+`02EB4230` immediately before and after a save load,
   twice, and confirm the two loads differ. Blocks: whether any deterministic replay of post-load
   play is possible at all.
2. **The LCG's area counter.** Watch `0208E6B0` across two entries to the same area and confirm it
   increments rather than resetting. Blocks: whether spawn placement is reproducible per area or
   per session.
3. **Consumer ordering.** A watch on `022C256C` across one combat turn, to see which of the 15
   LCG consumers draw and in what order. Blocks: any parity test at the outcome level rather than
   the algorithm level.

Queued, not requested of an absent agent; the live-automation pause stands.

<!-- OPUS-MUT-S13-RESTATE -->
### Mutation campaign, re-run 2026-09-12 on the full literal surface

**69 generated points: 64 KILLED · 2 SURVIVED · 3 EQUIVALENT · 0 NO_BUILD · 0 TIMEOUT · 0 INVALID. Verdict `FAIL`.**
Receipts: `Database/Tools/work/OPUS/litsuffix/rng_generators` (ignored path). Instrument: `Reconstruction/Tests/mutation_test.py`. The table for every pilot, and the four kinds a survivor can be, are on [`MUTATION-CAMPAIGNS.md`](../../../Reconstruction/MUTATION-CAMPAIGNS.md).

Both survivors are **kind A, provably equivalent**, and they are the same fact twice: `g_mt_seeded == 0` mutated to `== 1` and to `!=` both change whether the LAZY seed runs, and `Rng_MtSeed` calls `mt_seed_impl(seed)` immediately after it over the same state. **The lazy seed is unobservable through this entry point** — which is what the reconstruction's own comment says, now measured.

**Experiment records that name this contract** — found by `OPUS-CONTRACT-RUNTIME-AUDIT`, 2026-09-13. Each names this
contract in its own `contract:` frontmatter while this section did not cite it back.

- [`EXP-056`](../_experiments/EXP-056-save-normalize-roundtrip.md) — **method B**, isolated original-code execution.

**None of these is a live run**, so none of them changes the evidence-class statement at the
top of this section. They are listed because a reader auditing what has been executed against
this contract should not have to find them from the experiment side only.

## 14. Unresolved

- ~~The other four RNG families `rng-streams.md` records.~~ The other generators `rng-streams.md` records, at least six *(corrected 2026-10-02, OPUS: the image holds at least eight, the xorshift128 `0074BDE0` the eighth)*. Families 3, 4 and 5 and the xorshift128 are read there; only family 6, the Bullet solver LCG, is not *(answered: see rng-streams.md's `rand` census, its family-4 note of 2026-09-14, `CQ-6` and its streams-4-and-5 section of 2026-09-19; 2026-10-02, OPUS)*. None of them is specified in this contract.
- ~~`00866B90`, the twist body~~ — **read, and it is the standard twist**; see §7 for the three
  constants that establish it independently. ~~And what the dispatch value at `01F44858` is~~ —
  **resolved**: it is the CRT's `__isa_available`, so the two paths are one auto-vectorised loop.
- ~~Which callers reset the LCG seed through `00328D80`, and when.~~ **CLOSED 2026-09-11.**
  Exactly one caller in the image — `BattleSystem_InitializeAreaState` at `00234320` — seeding
  with the pre-increment value of a counter at `0208E6B0`. See §7. Census control: `memcpy`, 637
  sites.
- ~~What the dword at `01FD4A80` is~~ — **resolved 2026-09-22 (SWE2-CONTRACT): it is the
  session frame counter.** A per-body rip-relative census over all 35,713 `.pdata` bodies
  finds exactly two operands against `01FD4A80` in the whole image: `0022A59F`
  `inc dword [01FD4A80]`, executed once per dispatched tick at the head of the master frame
  dispatcher `0022A580` (the `00184AD0` gate returning zero falls through to the increment),
  and the seed read `005843B4`. The dword lives in `.data`'s uninitialised tail — born 0 at
  process start, never reset, never written by anything else — so it counts dispatched frames
  since boot. The post-load seed is therefore `_time64`-folded plus **elapsed session frames
  times 600**; 600-as-ten-minutes is refuted (the input is a frame count, not seconds), while
  what the scaling is *for* — decorrelating the tick term from the time term — is not
  recoverable from the bytes and is not claimed.
- ~~Whether anything other than `0022A40B` and the save-load path ever reseeds the MT
  *indirectly*~~ — **closed 2026-09-22 (SWE2-CONTRACT): no such path exists, and the bound is
  now airtight.** Extending the census past direct E8/E9 edges to every remaining route form —
  rip-relative `lea`, immediate materialisation, and absolute qword slots in every data
  section — finds: `00866D60` has exactly four direct calls, all inside the three RNG bodies
  (`00863C13` in `00863BF0`, `00863CA3` in `00863C80`, `00863D57`+`00863D6A` in `00863D30`);
  `00863D30`, the only body that seeds unconditionally with a caller value, has **zero**
  direct callers and is reached solely through the one-insn thunk `00379CF0`
  (`jmp 00863D30`), whose only referents are `0022A410` (boot, `0x11B9`) and `005843D3`
  (save load). No `lea`, immediate, or data pointer targets `00866D60`, `00863D30`,
  `00379CF0`, `00863BF0`, or `00863C80` anywhere in the image — the RNG interface is not
  registered, vtable'd, or callback'd at all.
- ~~Why the float draw swaps the vestigial object's vtable from `01CCFAC8` to `01CCFAD8`~~ —
  **resolved 2026-09-22 (SWE2-CONTRACT): the two vftables are `MTRand_int32` and
  `MTRand_closed`.** Their RTTI complete-object locators (`01D49198` / `01D49210`) name
  `.?AVMTRand_int32@@` and `.?AVMTRand_closed@@` — the two draw-specialisation wrappers of the
  MTRand library. Both are adjacent single-slot vftables whose sole entry is the same
  destructor `00863BC0`. The pattern is the compiler's, not the game's: the lazy-seed preamble
  (`cmp flag` / `lea vftable` / `edx=0x1571` / `call 00866D60`) is inlined identically into
  all three entries and is typed `MTRand_int32` in each (`00863BFB`, `00863C8B`, `00863D3D`);
  only the float draw then re-stamps the shared stack slot `MTRand_closed` (`00863CAE`)
  because that is the wrapper its draw expression uses. Neither `00866D60` nor `00866B90`
  reads `[rcx]`, so the stamp is dead either way — the swap is inlined-construction artefact,
  not behaviour.

## 15. Evidence

All from the shipping image (`73461D08…`), by three methods: disassembly, a call-site census with a
positive control, and **execution of the shipped bodies** under Unicorn against a reconstruction.

| claim | evidence | tier | confidence |
|---|---|---|---|
| the LCG advances three steps per draw | three `imul 0x41C64E6D` / `add 0x3039` pairs at `00328370`–`003283B4`, one writeback at `003283B9`; **and the state read back after each of 768 executed draws** | 1 | PROVEN |
| the LCG's XOR assembly and field order | `003283AD` `xor r8d,edx`, `003283B0` `shl r8d,0xa`, `003283C7` `xor eax,r8d`; **executed over 24 seeds incl. 0, 1, 0x7FFFFFFF, 0x80000000, 0xFFFFFFFF** | 1 | PROVEN |
| `0x41C64E6D` and `0x3039` are the ANSI C constants | immediate operands re-counted from the shipped bytes on every harness run: 3 and 3 — `00328376`/`00328381`/`0032839B` and `0032837B`/`00328395`/`003283B5` inside `00328370` | 1 | PROVEN |
| the MT's lazy 5489 seed and the flag outside the state | `00863BF4` tests `02EB4234`, `00863C09` passes `0x1571`, `00863C1E` sets the flag; **an unseeded 1,300-draw stream matches a 5489-seeded one exactly** | 1 | PROVEN |
| seeding leaves the cursor at 624 | `00866D98 mov dword [02EB4230], 0x270`; **compared on both sides after every seed**, and the cursor-0 mutant fails with 1,289 mismatches | 1 | PROVEN |
| the tempering masks are the textbook ones, pre-shifted | `0xFF3A58AD` at `00863C5B` and `0xFFFFDF8C` at `00863C67`, with `<<7` and `<<15` computed to `0x9D2C5680` / `0xEFC60000`; neither textbook constant appears literally | 1 | PROVEN |
| the twist at exactly 624 with `M = 397` | `00866CCF xor edx,[r8+0x634]`, bound `0xE3` at `00866C93`, `02EB3BFC − 02EB3870 = 0x38C`; **more than two full periods per seed executed, all 624 words compared** | 1 | PROVEN |
| the two twists are one auto-vectorised loop | `01F44858` is `__isa_available`; **both paths run over the same vector, 0 of 624 words differ**, with a control showing all 624 changed | 1 | PROVEN |
| which callers reset the LCG seed through `00328D80` | **closed** — one caller, `00234320` in `BattleSystem_InitializeAreaState`; see §7 and §14 | 1 | PROVEN |
| `01FD4A80` is the session frame counter | per-body rip-relative census over all 35,713 `.pdata` bodies: exactly two image operands — `inc dword [01FD4A80]` at `0022A59F` (head of `0022A580`, once per dispatched tick) and the `imul eax, […], 0x258` seed read at `005843B4`; `.data` uninitialised tail (born 0, no reset) | 1 | PROVEN |
| no unattributed path reseeds the MT | four-route census (`00866D60`, `00863D30`, `00379CF0`, `00863BF0`, `00863C80`): E8/E9 edges are the four internal sites plus `0022A410`/`005843D3` only; zero `lea`, zero immediate materialisations, zero data-section qword slots for all five | 1 | PROVEN |
| the float draw's vftable pair is `MTRand_int32`/`MTRand_closed` | RTTI locators `01D49198`/`01D49210` → `.?AVMTRand_int32@@`/`.?AVMTRand_closed@@`; both single-slot vftables, sole entry `00863BC0`; the `MTRand_int32` stamp is the shared inlined lazy-seed preamble (`00863BFB`/`00863C8B`/`00863D3D`), the `MTRand_closed` re-stamp at `00863CAE` is the float draw's own wrapper | 1 | PROVEN |

The single most useful *negative* remains: two constants that do not match the MT19937 reference are
not a modified algorithm, and the check that establishes it is one multiplication.

**The single most useful thing this round is an absence that was not there.** The interface table
was missing an entry point — `00863C80`, a third draw on the same cursor — and no amount of
re-reading `00863BF0` would have found it, because nothing in that function mentions it. It came
out of a caller census run for an unrelated question. **A contract's interface list is an absence
claim about every function not on it, and it had never been checked as one.**

## 15a. Falsification pass 1 — 2026-09-12 (OPUS), SURVIVED — nothing added

**Every constant and every idiom was re-derived from the bytes by an instrument written for this
pass, and this document already had all of them, correctly.**

| checked | found |
|---|---|
| the LCG constants | `0x41C64E6D` and `0x3039` at `00328370`, `0032837F`, `00328399` and `0032837A`, `00328393`, `003283B4` — **three multiply-adds, as §3 says** |
| the LCG's output assembly | `and 0x7FF << 10`, `and 0x3FF`, `and 0x3FF`, XOR-folded, writeback at `003283B9` — **the widths and addresses in §3's table are exact** |
| the MT parameters | `0x6C078965`, `0x270` (624), `0x9908B0DF`, and `0x1571` (5489) as the lazy seed |
| the twist's `mag01` | `00866CB9 and ecx, 1` / `00866CC2 **imul** ecx, ecx, 0x9908b0df` / `xor` — **branchless, exactly as §3 records at `00866CC2`** |
| the masks | `0x7FFFFFFE`, and §3 **already names the difference from the textbook's `0x80000000`/`0x7FFFFFFF`** |

**Nothing was found to add.** That is the honest result, and it is the first time in this sweep — the
other passes each turned up an unnamed callee, an uncovered path, a miscounted population or an
understated scope.

> **The reason is visible in the document.** §15 says its claims about the bytes are *"re-derived on
> every run rather than inherited"*, and the pilot re-derives the three `imul 0x41C64E6D` pairs and
> the state writeback on every execution. **A claim that is re-checked by its own suite does not
> drift**, and a pass against it can only confirm.

**Mechanical:** no body-size drift; banned-evidence sweep clean; all fourteen cited functions
resolve. `00379CD0` carries **66 callers, 53 of them CombatFormula**, and `00328370` fifteen across
spawn, movement, actor, AI and party — the split §3 already draws.

## 16. Parity plan

Reproduce: the LCG's three steps per draw, its XOR assembly and field order; the MT's lazy 5489 seed
and the flag that gates it; the twist at exactly 624 with `M = 397`. Of these, the three-step LCG is
the one a reimplementation would most plausibly get wrong while looking correct — and a
reimplementation needs only ONE twist, since the two here must agree by construction.

**Done, at the algorithm level** — see §13. Per-dimension verdicts are declared by the harness and
generated into [`PARITY-STATUS.md`](../_index/PARITY-STATUS.md): `CALCULATION`, `STRUCTURAL`,
`STATE-TRANSITION`, `EDGE-CASE` and `RNG` covered; `INTEGRATION` and `FULL-SUBSYSTEM` not, and
`SERIALIZATION`, `TIMING` and `PRESENTATION` not applicable.

**Three things a reimplementer must take from this contract that the old plan did not name:**

1. **Implement `00863C80` as well.** It is a draw on the same cursor. Omitting it desynchronises
   the stream on the first consumer that uses it.
2. **Seed leaves the cursor at 624.** Not 0.
3. **Decide, explicitly, what to do about the post-load `_time64` reseed** (§9). Reproducing it
   faithfully makes the reimplementation non-deterministic after a load, exactly as the original
   is. Replacing it with a fixed seed is a *deliberate divergence* and must be recorded as one —
   it is not a bug fix.

## 17. Related

- `21-RNG-And-Determinism/rng-streams.md` — the ~~six families~~ generators, at least eight *(corrected 2026-10-02, OPUS: the GFZ's six families plus the presentation PRNG and the xorshift128 `0074BDE0`)*, and their consumers.
- `21-RNG-And-Determinism/which-roll-is-on-which-generator.md`
- `_types` — `Mt19937State`, `SharedGameplayLcgState`

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**CombatAI — CLIENT.** `AiOrder_CheckActionPreconditions`, owned by that layer, calls `00328370` on this page. That caller is the precondition check: a `0x650`-byte frame with a stack cookie into which it copies **twelve `0x80`-byte blocks** from the unit's `+0x80` before testing the order's `word[+0]` and signed `word[+2]`; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

## The `00379CE0` exclusive subtree — 1 member bound (SWE2-FRONTIER, followup queue)

`00379CE0` (`RNG_MT19937_NextFloatClosed`, 5 B) — `jmp 00863C80`.

| member | role | interior |
| --- | --- | --- |
| `00863C80` | `byte[02EB4234]` ~~debug gate~~ lazy-seed latch, `GeneratorInitLatch` *(corrected 2026-10-02, OPUS: `00863C84` tests it, `00863C99` seeds 5489, `00863CBA` sets it to 1 — a do-once latch; §2 and CONTRACT-which-generator-serves-which-roll.md §3)*; `01CCFAC8` vtable-ref local; `edx = 0x1571` fallback seed (`00863C84`/`00863C99`) | [`00863C84`](../_index/ADDRESS-INDEX.md) |

Shared callees outside the census: none.

## SWE2-EC7-20 update (2026-09-18) — `00866D60` MT19937 lazy seed-record init

`00866D60` (67 B) is the MT19937 `init_genrand` this contract's streams reach
through the `00379CD0` thunk → `00863BF0`: `[02EB3870] = edx` stores the seed
(`00866D60`), then the recurrence `mt[i] = 1812433253 * (mt[i-1] ^ (mt[i-1] >>
30)) + i` runs `i = 1..0x26F` over `02EB3874` — `shr edx,0x1E` / `xor` /
`imul ecx,edx,0x6C078965` / `add ecx,r8d` (`00866D73`..`00866D96`) — and
`[02EB4230] = 0x270` marks the state index 624 (`00866D98`). The canonical
5489-path seeding the draw bodies run on the uninitialized path. Three callers:
`00863BF0`/`00863C80`/`00863D30` — the generator-draw bodies the gameplay
streams share.


---

## §12c — the census had four entry points and the cursor has five (OPUS, 2026-09-19)

**§2 of this contract already says `00863C80`, reached through the thunk `00379CE0`, "ADVANCES THE
SAME CURSOR", and §12 warns that a reimplementation omitting it desynchronises. The consumer census
above never counted it.** So "98 sites, 66 functions" was the consumer population of *one of two
draw entry points* on the MT cursor, presented as the consumer population of the cursor. A replay
built from that table replays the wrong stream — which is the failure §12 predicts, arriving
through the table rather than through the code.

### The instrument reproduces the rows that were already there

The same scan — direct `call`/`jmp` to the entry point, across every function in `.text` — gives
**98 sites over 66 functions for `00379CD0`** and **23 over 15 for `00328370`**, matching the two
published rows exactly. That is the control: the new row is produced by an instrument that
reproduces the old ones.

### The float draw has exactly one consumer

| | |
|---|---|
| callers of the thunk `00379CE0` | **`0037D1F0` only**, 9 sites |
| callers of the body `00863C80` | **none but the thunk's own `jmp`** |

**`0037D1F0` is the camera-shake sampler, and it is the entire consumer population of the float
draw.** The function is unnamed in the symbol table (`FUN_0037d1f0`); this is what it does.

### Why nine sites are sixteen draws

```
0037D288  mov  ebp, 8                       ; eight channels
0037D28D  lea  rdi, [rsi + 0x14]            ; an 0x10-stride parameter table
0037D291  call 0x379ce0                     ; THE DRAW
0037D296  mulss xmm0, dword ptr [rdi + 4]   ; * per-channel scale
0037D29B  addss xmm0, dword ptr [rdi]       ; + per-channel bias
0037D29F  add  rdi, 0x10
0037D2A3  mulss xmm0, dword ptr [01DFE0BC]  ; a .data scalar, 1.0f in the file image
0037D2AB  addss xmm0, dword ptr [rbx]       ; accumulate into rsi+0xC8 + 4*i
0037D2AF  movss dword ptr [rbx], xmm0
0037D2B3  add  rbx, 4
0037D2B7  sub  rbp, 1
0037D2BB  jne  0x37d291
```

Eight draws accumulate eight running values; then **eight further draws in straight line** at
`0037D2D8`, `D303`, `D32E`, `D359`, `D38C`, `D3BF`, `D3F2`, `D420`. **Sixteen per evaluation.**

> `01DFE0BC` is in `.data`, not `.rdata`, and holds `1.0f` in the file image. **It is a writable
> global, so "multiply by one" is what the *file* says, not necessarily what runs.** It is named
> here as an unresolved scalar, not consumed as a no-op.

### And how often the evaluation runs

The driver `003DCFB0` walks four shake drivers — `rbx = rsi + 0x178`, `add rbx, 0x18`, `cmp edi, 4`,
`jl 0x3dd044` — and calls the sampler at `003DD06B` for **every driver whose state word is
non-zero**. That includes **state 2**: the `test word ptr [rbx], 0xFFFD` at `003DD085` which
excludes state 2 is *after* the sampler call, and gates only the trailing decay block.

> **So a finished shake still draws.** Four active-or-finished drivers advance the shared gameplay
> MT cursor by **64 floats in one frame**, against the whole `BattleFormula_*` population's 98
> *static* integer-draw sites. **On volume, camera shake is the dominant consumer of this cursor,
> and it was not in the census.**

### What this does not establish

Four drivers per frame is the **loop bound**, not a measured rate: how many drivers are non-zero in
any real frame is a runtime question this contract does not answer, and no claim about a typical
frame is made here. §9's determinism rows are **not** revised — whether shake makes the stream
run-to-run divergent depends on when drivers start, which is exactly the unmeasured quantity.
**Routed to ASTRA** as a live question: the per-frame count of non-zero shake drivers, in and out of
battle.

*(OPUS 2026-09-19, on FABLE's `FABLE-REQ-OPUS-SHAKE-IS-A-CONSUMER-OF-THE-GAMEPLAY-MT-STREAM`. The
request asked for shake to be listed among the consumers; verifying it found the census was missing
the entry point rather than the consumer. FABLE's three stated facts — sixteen draws, the eight/eight
split, and the state-2 drive — all verify from the bytes.)*
