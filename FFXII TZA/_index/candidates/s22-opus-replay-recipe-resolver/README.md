# S-22: the weapon-recipe resolver executed as shipped code on authored recipes (OPUS, 2026-09-25, block 316)

**Evidence class: NATIVE-REPLAY (unicorn), `live_game: false`.**
- `CONTRACT-weapon-recipes.md` §13 reads "None. No experiment executes this resolver".
- With block 311 (steps and element scaling) and the preparation-step differential, **all four S-22 contracts now
  have execution**.

## What was run

`check.py`:
- **Image.** It maps the whole SHA-asserted image. **No application stub.**
- **Allowed set: 871 functions.** The resolver's static closure, plus every step-table target's closure (the loop
  reaches them through `call [table + slot*8]`, which `edges.tsv` cannot follow), plus the MT19937 body.
- **Imports.** Every IAT slot is trapped; only memset / memcpy / memmove are bridged.
- **The recipes are the shipped ones** (pointer table `01EF96C0`, step table `01EFA5C0`). Nothing in them is planted;
  each case picks an action row whose `+8` byte is the recipe id.
- **Fixtures** are planted data only: both stats blocks, the result record, the action table, zeroed per-side records
  at `0208D480`, and an empty unit table.
- **Hooks** at the loop's indirect call (`003863D0`) record the slot, and the instruction after it records
  `[02AEDFB8]`.

**All checks pass, and `result.json` is byte-identical over three runs.**

| case | contract item | observed |
|---|---|---|
| `RW1_table_extent_static` | RW-1 | ids 0..108 point into the image's data; the 110th qword (`000000B4FFFFFFFF`) does not |
| `RW2_RW4_static` | RW-2, RW-4 (§12) | recipe 25 is two `−1`-terminated runs; none of its seven preview slots is in its committed run. Recipes 25 and 26 differ in **exactly three positions**: preview 5 (`35`/`36`), preview 6 (`42`/`43`), committed 1 (`66`/`65`) |
| `RW2_committed_list_only` | RW-2 | **recipe 39** (preview `[193]`, committed `[]`) **calls no step**. Recipes 74 `[152]`, 90 `[198]`, 5 `[3, 111]` and 4 `[60, 90, 91, 110]` call **exactly their committed lists, in order** |
| `loop_early_exit_observed` | not in the contract | **recipe 6** `[3, 4, 61, 90, 91, 112, 180]` **stops after slot 4**, and **recipe 2** `[20, 30, 32, 40, 181]` **stops after slot 40**. In each, the step just run left `[02AEDFB8] = 1`, and `003863D7 cmp / je` ends the loop |

Recipe 25 (bow) was run too: its first committed slot, 29, needs objects this fixture does not plant (a read at
`0x1C`), so it is **not covered**.

## What the execution adds to the contract

1. **A recipe is not always run to its end.** After every committed step the loop tests `[02AEDFB8]` and stops when a
   step set it. Several steps set it (for example slot 0 at `00387F56`, slot 4 at `00388341`, slots 11–14). On the
   authored recipes 6 and 2 it cut five steps and one step respectively. The contract's §7 ("run that list against
   the step table") and RW-2 describe which list runs, not that it can be cut short.
2. **The same flag can skip the loop entirely.** Before the loop, `00386249`–`00386278` loads `[02AEDFB8]` for
   recipes in the bitmask `0x4000140000004E`. For the others it sets the flag to 1 when the prepared context carries
   `0x80000003`, and `003862AE` skips the loop when the flag is non-zero. This part is static only.
3. **Recipe id 0 is the weapon's recipe.** When the action row's `+8` is 0, `0038618B`–`00386210` takes the recipe id
   from the attacker's equipped item (`[att+0x50] − 0x1000`, row `+0x19`). That is where "weapon recipes" come from
   (static only).

## Not covered

- recipes whose first steps need richer objects (25, 26, the other weapon families);
- the post-loop call `00390F20`'s effects (it ran in every completed case; its writes are not asserted);
- the preview-side consumer;
- a live game.

## WE-1 executed on the shipped recipes: `we1.py` (OPUS, 2026-09-26)

**The claim.** `CONTRACT-environmental-element-scaling.md` WE-1: the environment-scaling stage runs **before** the affinity
stage `0038B6A0`, and **both read the element mask at `ActionDefinition + 0x13`**.
- In the shipped step table `01EFA5C0` they are **adjacent ids: 94 (`0038B220`) and 95 (`0038B6A0`)**.
- `we1.py` loads `check.py` (its cases run first, unchanged; `result.json` unchanged). It reads every shipped recipe from
  `01EF96C0`, and runs those holding both steps through the real resolver `00385F60`, exactly as this harness runs recipes.
- A read hook on the action row's `+0x13` records which function read it. **No application stub.**

**4 / 4 pass, and `we1_result.json` is byte-identical over two runs** (md5 `5680857b37dea30c63e4dbdc9d214019`).

| case | observed |
|---|---|
| `static_every_recipe_with_both_lists_94_before_95` | seven shipped recipes list both steps (**7, 14, 37, 63, 83, 105, 106**), and 94 precedes 95 in every one |
| `executed_94_runs_before_95_wherever_both_run` | recipes 7, 63, 83, 105 and 106 run `… 94, 95 …`, **94 immediately before 95**. Recipes 14 and 37 stop early (the `[02AEDFB8]` flag, see above) before reaching either |
| `executed_both_stages_read_the_element_byte_plus13` | in every recipe that reaches them, **both `0038B220` and `0038B6A0` read the action row's `+0x13`** |
| `executed_recipes_return` | every run returns |

**Observation (not a contract item).** Recipes **65, 66 and 68** carry the affinity stage 95 **without** the environment
stage 94; no shipped recipe carries 94 without 95. So "the stage that follows" always follows, but the affinity stage does
not always have a pre-affinity stage in front of it.
