---
title: "Which roll uses which generator: combat, chests, loot, the chain, spawning, AI, movement, script verbs and presentation, what reseeds each, and what loading a save changes"
kind: "system"
category: "Random numbers"
addresses: "00379CD0, 00379CE0, 00328370, 022C256C, 02EB3870, 008C3098, 003D8E50, 0022A410, 005843D3, 00234320"
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

The gameplay MT19937 (state `02EB3870`) is drawn through the thunk `00379CD0` for 32-bit values and
`00379CE0` for floats (see the [generators page](random-number-generators.md)). The 32-bit thunk
has 98 call sites in 66 functions; the float thunk 9 call sites in one function.

| Roll | Function | Draw site |
|---|---|---|
| battle formula and action effects: hit, guard and parry modes, knockback, combo count, attack variance, the percent gates, status candidates, poach item | 53 functions from `003851F0` to `00390680` (named ones include `00387FD0`, `00388350`, `00388440`, `003884F0`, `00388660`, `00389140`, `003896B0`, `0038A110`-`0038AE50`, `0038FB80`, `0038FBC0`, `00390680`) | 83 sites |
| Regen tick: `draw % level + 1` HP added to the result for status 25 | `00386C70` | `00386D27`-`00386D3A` |
| weather: keep the current weather when `(draw × 100) >> 32 < p`, else pick a new one with `0025ABA0`, which draws again | `0025ACA0`, run from the field runtime initialisation `002620E0` (`00262109`) | `0025ACDD`, `0025ABB8` |
| HP and MP growth bonus on a level-up | `002F9A60`, `002F9B20` | `002F9AD3`, `002F9B8C` |
| treasure placement: a treasure spawns when `draw % 100 < chance` (row byte `+5`), unless its persistent flag (`0032AA60(row byte +4)`) is set | `002FA740` | `002FA7FC` |
| second treasure roll: when the flag `0032AA60(row byte +9)` is not 1, `draw % 100 < row byte +10` marks the entry present | `002FAED0` | `002FAEF2` |
| chest contents: gil or item (`draw % 100 >= row byte +11` is item), which of two items (`draw % 100 < 50`, or `< 95` with effect bit 1 of stats `+0x6B` or `+0x7B`), and the gil amount `draw % n + 1` when row byte `+8` has bit `0x40` | `002FAFD0` | `002FB01D`, `002FB082`, `002FB0AD` |
| field action trigger near a unit: `draw % 100 < 75` picks word `+6` else `+8` of the entry | `002F8060` | `002F8218` |
| script verb `rand` (`0x28`): the raw draw | `00355140` | `00355149` |
| script verb `rand_29` (`0x29`, one argument `n`): `(draw × n) >> 32` | `00354BF0` | `00354C08` |
| boot frame modes 0 and 1: one draw per dispatch, discarded | `0022B6E0`, `0022B7E0` | `0022B706`, `0022B7EB` |
| shake oscillator: sixteen float draws per step, eight in a loop over the channel accumulators (`0037D291`) and eight single draws, scaled by `01DFE0BC` | `0037D1F0` | `0037D291`-`0037D420` |

### Rolls on the shared gameplay LCG

The LCG (state `022C256C`) is drawn either by the out-of-line `00328370` or by an inline copy of
its three steps. Every draw, inline or not, advances the same word.

| Roll | Function | Draw |
|---|---|---|
| loot drop chance per slot | `003185D0` | inline, `003185E4`-`00318641` |
| loot quantity bucket | `003186F0` | inline, `00318704`-`00318741` |
| loot chance profile when breaks are counted | `00318820` | inline, `00318834`-`00318861` |
| the two extra drops | `00318510` | inline, `00318540`-`00318569` |
| chain coin on a continuing kill | `00317ED0` | inline, `00317FC1`-`00317FEA` |
| chain level rise | `003183D0` | inline, `0031844A`-`00318473` |
| chain bonus on a pickup | `00319530` | inline, `00319530`-`0031955F` |
| spawn placement: candidate position, random candidate, position inside an authored region, keep entries | `00234AF0` (2 sites), `002355A0`, `00236450` (6 sites), `002395A0` (2 sites) | `00328370` |
| enemy level at spawn: `draw % (range + 1) + base` through `0030C470` | `002398F0` | `0023991D` |
| spawn height term for an enemy with record flag bits | `00236210` | `002362B6` |
| spawn status seeding: per status, authored value 1 applies on `draw & 1`, value 2 always applies, value 3 sets the bit in `+0xE90` | `002394C0` | `00239547` |
| random facing: `draw % 360` degrees when the requested angle is negative | `00239210` | `00239243` |
| random heading goal `0x4150`: `draw % 340 + 10` degrees | `00312B40` | `00312C93` |
| random point within `±r` of a target, up to nine tries | `00312DF0` | `00312E50`, `00312E6B` |
| AI order evaluation and preconditions, `draw % 100` | `003014C0`, `00301830` | `0030160F`, `0030193F` |
| AI final target choice | `003087E0` | `00308B13` |
| weighted action id: walk the weight bytes until the running sum exceeds `draw % 100` | `00308EC0` | `00308F61` |
| party stance recheck timer: `now + 30 × scalar × ((draw & 3) × 0.25 + 0.5)` frames | `003081E0` | `003081FF` |

### Rolls on the C runtime rand

`rand` (import `008C3098`) has 48 direct call sites in 30 functions, plus one through the stub `00861F38` from `00149610` (`0014963E`), an SSE dither loop.

| Caller | What it is |
|---|---|
| `00819270` | the Lua binding `LuaMath_Random`: `rand() % 32767 / 32767.0`, scaled to the requested interval |
| `008193E0` | the Lua binding `LuaMath_RandomSeed`: `srand`, then one discarded `rand`; the other `srand` caller is the worker thread `007A5400` (`007A540B`) |
| `00338490` | `PartyFollow_SolveFormation` |
| `0033E1F0`, `003343D0`, `00334E00` | the randomised avoidance and detour choices of battle locomotion |
| `003BBD00` | `BattlePresentation_EnqueueReactionWithRandomizedVariant` |
| `002F8410` | `BattleAction_ComputeChargeLimitTicks` |
| `002F88B0` | `BattleSpecialSequence_BuildRandomizedCandidateActions` |
| `003FBE90` | the loot pickup object's initialiser, 6 sites |
| `00177850`, `001A7770`, `00866200`, `00336E40`, `0033DB60`, `00337D90`, `0029F130`, `002FA1A0`, `00384B10`, `004225A0`, `00530E40`, `0055B3F0`, `007D0260`, `007E6DD0`, `007E7E00`, `007E5160`, `007E5E80`, `007E65B0`, `007E6620`, `007F3E30` | the other twenty callers |

### Rolls on the presentation generator

`003D8E50` (220 call sites in 49 functions, all between `003D8190` and `0054E040`) and `004005E0`
(two sites in `004010A0`) serve presentation code: camera and backend orientation (`0040AAD0`
draws twice with amplitude 0.3), effect parameters and the script-side effect verbs in the
`00515DA0`-`0054E040` range. Seven more functions step the generator inline (listed on the
generators page). None of them touches a gameplay generator.

### What reseeds what

| Event | Gameplay MT | Shared LCG | Others |
|---|---|---|---|
| process start | lazy seed 5489 on first draw, then 4537 at `0022A410` | state 0 until an area initialises | graphics-noise MT from `_time64` and `clock` (`0015BCF0`); presentation generator `0x458DC800` (`00259216`); the counter hash and the PPFX counter start at their image values |
| area initialisation `002342F0` | nothing | seed = the counter `0208E6B0`, then the counter + 1 (`00234301`-`00234320`) | nothing |
| loading a save `00584210` | seed from the clock and the frame counter (`005843A5`-`005843D3`) | nothing | nothing |
| Lua `math.randomseed` | nothing | nothing | `srand` (`008193E0`) |

### What can influence what

- Rolls on the MT cannot move the LCG and rolls on the LCG cannot move the MT: no function draws
  from both (the MT thunk callers and the LCG draw and inline sites above are disjoint sets).
- Every LCG consumer moves every other: a gambit or AI decision that draws (`003014C0`,
  `00301830`, `003087E0`, `00308EC0`), a spawn, a random heading or the stance timer changes the
  next loot roll, the chain coin and the chain bonus.
- Within the MT, the order of draws is the only variation: a chest opened before a fight shifts
  every later hit and damage roll by its draws.
- The presentation generator, `rand`, the graphics-noise MT, the counter hash and the xorshift
  never move the two gameplay generators: their state words are untouched by those sources.
- `rand` does decide gameplay values of its own: the charge-time term in `002F8410`
  (`rand() % n / 100` added at `002F8703`, `002F8712`), the special-sequence candidate actions in
  `002F88B0` (`002F8A14`, `002F8B43`) and the locomotion detours in `0033E1F0`, `003343D0`,
  `00334E00`.

## Operations

| Function | Generator | Role |
|---|---|---|
| `00379CD0`, `00379CE0` | gameplay MT | the two draw thunks every consumer calls |
| `00328370` | shared LCG | the out-of-line draw, 23 call sites |
| `00317ED0`, `003183D0`, `00318510`, `003185D0`, `003186F0`, `00318820`, `00319530` | shared LCG | the seven inline draw sites |
| `00584210` | gameplay MT | reseed on save load |
| `002342F0` | shared LCG | reseed on area initialisation |
| `0022A0B0` | gameplay MT, presentation | boot seeds |

## State

| Address | Width | Meaning | Written by |
|---|---|---|---|
| `02EB3870` / `02EB4230` | 624 × `u32` / `i32` | gameplay MT state and index | `00866D60`, `00866B90`, `00863BF0`, `00863C80` |
| `022C256C` | `u32` | shared LCG state | `00328370`, the seven inline sites, `00328D80` |
| `0208E6B0` | `u32` | areas initialised since process start, the next LCG seed | `002342F0` |

## Modding notes

- To make loot independent of AI decisions, give the loot functions their own state word; all
  seven inline sites read and write `022C256C` directly.
- To stop a save reload from rerolling combat, replace the seed computation at
  `005843A5`-`005843C2` with a constant or remove the tail jump at `005843D3`.
- A script can read the MT directly with the `rand` verbs (`0x28`, `0x29`); each call advances the
  combat stream by one.

## Related

- [Random number generators: the gameplay Mersenne Twister, the shared gameplay LCG, the graphics-noise Mersenne Twister, the C runtime rand, the presentation bit-feedback generator, the counter hash and the PPFX xorshift, with their constants, seeds and states](random-number-generators.md)
- [Loot drops: drop roll, item slots, quantities, drop tables and the chain bonus](../Rewards-EXP-Gil-And-Loot/loot-drops.md)
- [Kill chain: chain count, chain level, the chain coin and resets](../Rewards-EXP-Gil-And-Loot/kill-chain.md)
- [Loot pickups: the ten-slot pool, creation and eviction, the one-minute lifetime and blink, collection on contact, and the pickup object](../Rewards-EXP-Gil-And-Loot/loot-pickups.md)
