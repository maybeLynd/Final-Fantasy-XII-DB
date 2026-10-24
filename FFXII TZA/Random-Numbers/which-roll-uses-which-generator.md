---
title: "Which roll uses which generator: combat, chests, loot, the chain, spawning, AI, movement, script verbs and presentation, what reseeds each, and what loading a save changes"
kind: "system"
category: "Random numbers"
addresses: "0x00379CD0, 0x00379CE0, 0x00328370, 0x022C256C, 0x02EB3870, 0x008C3098, 0x003D8E50, 0x0022A410, 0x005843D3, 0x00234320"
---

## What the player sees

Two generators decide almost everything a player would call luck:

- Whether an attack hits, how much it does, whether a status lands, what a chest holds and whether
  a treasure appears at all are rolled on the first.
- Loot drops, the chain coin and chain level, the chain bonus, where an enemy spawns and what level
  it gets, which action an AI unit picks and the random turns units make are rolled on the second.

The two never mix: no amount of fighting changes the next loot roll through the damage numbers,
but the AI decisions taken during the fight do move it. Reloading a save rerolls the first group,
because that generator is reseeded from the clock on every load, and leaves the second group's
sequence exactly where it was. Entering an area restarts the second group from a counter of areas
entered since the game was started.

## How it works

### Rolls on the gameplay Mersenne Twister

The gameplay MT19937 (state `0x02EB3870`) is drawn through the thunk `0x00379CD0` for 32-bit values and
`0x00379CE0` for floats (see the [generators page](random-number-generators.md)). The 32-bit thunk
has 98 call sites in 66 functions; the float thunk 9 call sites in one function.

| Roll | Function | Draw site |
|---|---|---|
| battle formula and action effects: hit, guard and parry modes, knockback, combo count, attack variance, the percent gates, status candidates, poach item | 53 functions from `0x003851F0` to `0x00390680` (named ones include `0x00387FD0`, `0x00388350`, `0x00388440`, `0x003884F0`, `0x00388660`, `0x00389140`, `0x003896B0`, `0x0038A110`-`0x0038AE50`, `0x0038FB80`, `0x0038FBC0`, `0x00390680`) | 83 sites |
| Regen tick: `draw % level + 1` HP added to the result for status 25 | `0x00386C70` | `0x00386D27`-`0x00386D3A` |
| weather: keep the current weather when `(draw × 100) >> 32 < p`, else pick a new one with `0x0025ABA0`, which draws again | `0x0025ACA0`, run from the field runtime initialisation `0x002620E0` (`0x00262109`) | `0x0025ACDD`, `0x0025ABB8` |
| HP and MP growth bonus on a level-up | `0x002F9A60`, `0x002F9B20` | `0x002F9AD3`, `0x002F9B8C` |
| trap arming, the walk `0x003EC630` tail-jumps to (`0x003EC679`; [traps](../World-Areas-And-Travel/traps.md)): each of the first `min(count, 32)` records of the bound trap table (`0x002641B0`, `0x002FA765`; `0x002FA788`-`0x002FA797`) is armed and its marker placed (`0x002FA841`) when `draw % 100 <` record byte `+5`, unless its persistent flag `0x0032AA60(record byte +4)` is set (a flag id `0xFF` skips the test, `0x002FA7EC`) | `0x002FA740` | `0x002FA7FC` |
| treasure chest presence ([reward verbs](../Scripts-And-Script-Commands/reward-verbs.md)): no chest when the opened flag `0x0032AA60(record byte +9)` is 1; otherwise a chest when `draw % 100 <` record byte `+10`, both outcomes recorded through `0x002FB430` (`0x002FAF27`, `0x002FAF3F`) | `0x002FAED0` | `0x002FAEF2` |
| chest contents: gil or item (`draw % 100 >= row byte +11` is item), which of two items (`draw % 100 < 50`, or `< 95` with bit `0x2` of the augment layer bytes `+0x6B` or `+0x7B`, augment 25 (Treasure Hunter)), and the gil amount `draw % n + 1` when row byte `+8` has bit `0x40` | `0x002FAFD0` | `0x002FB01D`, `0x002FB082`, `0x002FB0AD` |
| trap trigger near a unit ([traps](../World-Areas-And-Travel/traps.md)): `draw % 100 < 75` picks word `+6` else `+8` of the trap record | `0x002F8060` | `0x002F8218` |
| script verb `rand` (`0x28`): the raw draw | `0x00355140` | `0x00355149` |
| script verb `rand_29` (`0x29`, one argument `n`): `(draw × n) >> 32` | `0x00354BF0` | `0x00354C08` |
| boot frame modes 0 and 1: one draw per dispatch, discarded | `0x0022B6E0`, `0x0022B7E0` | `0x0022B706`, `0x0022B7EB` |
| shake oscillator: sixteen float draws per step, eight in a loop over the channel accumulators (`0x0037D291`) and eight single draws, scaled by `0x01DFE0BC` | `0x0037D1F0` | `0x0037D291`-`0x0037D420` |

### Rolls on the shared gameplay LCG

The LCG (state `0x022C256C`) is drawn either by the out-of-line `0x00328370` or by an inline copy of
its three steps. Every draw, inline or not, advances the same word.

| Roll | Function | Draw |
|---|---|---|
| loot drop chance per slot | `0x003185D0` | inline, `0x003185E4`-`0x00318641` |
| loot quantity bucket | `0x003186F0` | inline, `0x00318704`-`0x00318741` |
| loot chance profile when breaks are counted | `0x00318820` | inline, `0x00318834`-`0x00318861` |
| the two extra drops | `0x00318510` | inline, `0x00318540`-`0x00318569` |
| chain coin on a continuing kill | `0x00317ED0` | inline, `0x00317FC1`-`0x00317FEA` |
| chain level rise | `0x003183D0` | inline, `0x0031844A`-`0x00318473` |
| chain bonus on a pickup | `0x00319530` | inline, `0x00319530`-`0x0031955F` |
| spawn placement: candidate position, random candidate, position inside an authored region, keep entries | `0x00234AF0` (2 sites), `0x002355A0`, `0x00236450` (6 sites), `0x002395A0` (2 sites) | `0x00328370` |
| enemy level at spawn: `draw % (range + 1) + base` through `0x0030C470` | `0x002398F0` | `0x0023991D` |
| spawn height term for an enemy with record flag bits | `0x00236210` | `0x002362B6` |
| spawn status seeding: per status, authored value 1 applies on `draw & 1`, value 2 always applies, value 3 sets the bit in `+0xE90` | `0x002394C0` | `0x00239547` |
| random facing: `draw % 360` degrees when the requested angle is negative | `0x00239210` | `0x00239243` |
| random heading goal `0x4150`: `draw % 340 + 10` degrees | `0x00312B40` | `0x00312C93` |
| random point within `±r` of a target, up to nine tries | `0x00312DF0` | `0x00312E50`, `0x00312E6B` |
| AI order evaluation and preconditions, `draw % 100` | `0x003014C0`, `0x00301830` | `0x0030160F`, `0x0030193F` |
| AI final target choice | `0x003087E0` | `0x00308B13` |
| weighted action id: walk the weight bytes until the running sum exceeds `draw % 100` | `0x00308EC0` | `0x00308F61` |
| party stance recheck timer: `now + 30 × scalar × ((draw & 3) × 0.25 + 0.5)` frames | `0x003081E0` | `0x003081FF` |

### Rolls on the C runtime rand

`rand` (import `0x008C3098`) has 48 direct call sites in 30 functions, plus one through the stub `0x00861F38` from `0x00149610` (`0x0014963E`), an SSE dither loop.

| Caller | What it is |
|---|---|
| `0x00819270` | the Lua binding `LuaMath_Random`: `rand() % 32767 / 32767.0`, scaled to the requested interval |
| `0x008193E0` | the Lua binding `LuaMath_RandomSeed`: `srand`, then one discarded `rand`; the other `srand` caller is the worker thread `0x007A5400` (`0x007A540B`) |
| `0x00338490` | `PartyFollow_SolveFormation` |
| `0x0033E1F0`, `0x003343D0`, `0x00334E00` | the randomised avoidance and detour choices of battle locomotion |
| `0x003BBD00` | `BattlePresentation_EnqueueReactionWithRandomizedVariant` |
| `0x002F8410` | `BattleAction_ComputeChargeLimitTicks` |
| `0x002F88B0` | `BattleSpecialSequence_BuildRandomizedCandidateActions` |
| `0x003FBE90` | the loot pickup object's initialiser, 6 sites |
| `0x00177850`, `0x001A7770`, `0x00866200`, `0x00336E40`, `0x0033DB60`, `0x00337D90`, `0x0029F130`, `0x002FA1A0`, `0x00384B10`, `0x004225A0`, `0x00530E40`, `0x0055B3F0`, `0x007D0260`, `0x007E6DD0`, `0x007E7E00`, `0x007E5160`, `0x007E5E80`, `0x007E65B0`, `0x007E6620`, `0x007F3E30` | the other twenty callers |

### Rolls on the presentation generator

`0x003D8E50` (220 call sites in 49 functions, all between `0x003D8190` and `0x0054E040`) and `0x004005E0`
(two sites in `0x004010A0`) serve presentation code: camera and backend orientation (`0x0040AAD0`
draws twice with amplitude 0.3), effect parameters and the script-side effect verbs in the
`0x00515DA0`-`0x0054E040` range. Seven more functions step the generator inline (listed on the
generators page). None of them touches a gameplay generator.

### What reseeds what

| Event | Gameplay MT | Shared LCG | Others |
|---|---|---|---|
| process start | lazy seed 5489 on first draw, then 4537 at `0x0022A410` | state 0 until an area initialises | graphics-noise MT from `_time64` and `clock` (`0x0015BCF0`); presentation generator `0x458DC800` (`0x00259216`); the counter hash and the PPFX counter start at their image values |
| area initialisation `0x002342F0` | nothing | seed = the counter `0x0208E6B0`, then the counter + 1 (`0x00234301`-`0x00234320`) | nothing |
| loading a save `0x00584210` | seed from the clock and the frame counter (`0x005843A5`-`0x005843D3`) | nothing | nothing |
| Lua `math.randomseed` | nothing | nothing | `srand` (`0x008193E0`) |

### What can influence what

- Rolls on the MT cannot move the LCG and rolls on the LCG cannot move the MT: no function draws
  from both (the MT thunk callers and the LCG draw and inline sites above are disjoint sets).
- Every LCG consumer moves every other: a gambit or AI decision that draws (`0x003014C0`,
  `0x00301830`, `0x003087E0`, `0x00308EC0`), a spawn, a random heading or the stance timer changes the
  next loot roll, the chain coin and the chain bonus.
- Within the MT, the order of draws is the only variation: a chest opened before a fight shifts
  every later hit and damage roll by its draws.
- The presentation generator, `rand`, the graphics-noise MT, the counter hash and the xorshift
  never move the two gameplay generators: their state words are untouched by those sources.
- `rand` does decide gameplay values of its own: the charge-time term in `0x002F8410`
  (`rand() % n / 100` added at `0x002F8703`, `0x002F8712`), the special-sequence candidate actions in
  `0x002F88B0` (`0x002F8A14`, `0x002F8B43`) and the locomotion detours in `0x0033E1F0`, `0x003343D0`,
  `0x00334E00`.

## Operations

| Function | Generator | Role |
|---|---|---|
| `0x00379CD0`, `0x00379CE0` | gameplay MT | the two draw thunks every consumer calls |
| `0x00328370` | shared LCG | the out-of-line draw, 23 call sites |
| `0x00317ED0`, `0x003183D0`, `0x00318510`, `0x003185D0`, `0x003186F0`, `0x00318820`, `0x00319530` | shared LCG | the seven inline draw sites |
| `0x00584210` | gameplay MT | reseed on save load |
| `0x002342F0` | shared LCG | reseed on area initialisation |
| `0x0022A0B0` | gameplay MT, presentation | boot seeds |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `0x02EB3870` / `0x02EB4230` | 624 × `u32` / `i32` | gameplay MT state and index | `0x00866D60`, `0x00866B90`, `0x00863BF0`, `0x00863C80` |
| `0x022C256C` | `u32` | shared LCG state | `0x00328370`, the seven inline sites, `0x00328D80` |
| `0x0208E6B0` | `u32` | areas initialised since process start, the next LCG seed | `0x002342F0` |

## Modding notes

- To make loot independent of AI decisions, give the loot functions their own state word; all
  seven inline sites read and write `0x022C256C` directly.
- To stop a save reload from rerolling combat, replace the seed computation at
  `0x005843A5`-`0x005843C2` with a constant or remove the tail jump at `0x005843D3`.
- A script can read the MT directly with the `rand` verbs (`0x28`, `0x29`); each call advances the
  combat stream by one.

## Related

- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](random-number-generators.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)
- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
- [Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)
