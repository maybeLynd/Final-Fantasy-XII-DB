[Home](../../README.md) / [Story, events and hunts](README.md) / Story progress

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Story progress: the main story counter at the start of the save, the script variables that live in the save, and how scenes move the story on | system | Story, events and hunts | Story progress and flags | Where the story stands and how it moves: the six classes of script variable and the one that is the save payload itself, read and written live, the main story counter as the payload's first word, the native code that reads it, how zone director scripts raise it behind a test of its current value, the values only the developer menus set, and where the flags and quests that sit beside it are described. | 0x002625E7, 0x002626A8, 0x0026CAF8, 0x002EF2B0, 0x00265270, 0x02098E58 |

## What the player sees

- In normal play the story moves forward one scene at a time: the zone scripts start most scenes behind a test of the
  story counter, so a scene that has played is passed over, and towns, people and menus change after it.
- The counter itself keeps no order. Each script write stores its value whatever the counter held, so a script that
  writes an earlier value moves the story back (How scenes move it on, below).
- Loading a save puts every scene, talk and menu back where the story stood.

## How it works

### Script variables

A script names a variable by a descriptor: a class in the top bits and an offset in the low 24 bits. The resolver
picks the base for the class through the jump table at `0x002626A8`¹ and adds the offset²:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002625EA`-`0x00262603` |
| ² | `0x00262639`-`0x00262641` |

</details>

| Class | Base | Set at |
|---:|---|---|
| `0` | the save payload, actor manager `+0x48` (`0x00262605`) | `0x0026CAF8`-`0x0026CAFD` |
| `1` | actor manager `+0x40` (`0x0026260B`) | - |
| `2` | the address the callback at `+0x98` returns (`0x00262611`-`0x00262617`) | - |
| `3` | the script image plus its own `+0x40` word (`0x00262633`-`0x00262636`) | - |
| `4` | actor manager `+0x58` (`0x00262627`) | - |
| `5` | actor manager `+0x60` (`0x0026262D`) | - |

Class 0 is the save payload itself: `0x002EF2B0` returns the active save buffer plus `0x200`¹, and
the actor manager keeps that pointer at `+0x48` when it binds the loaded definitions². So a
class-0 variable at offset *n* is payload byte *n*, read and written on every access with no copy.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002EF2B4`-`0x002EF2B9` |
| ² | `0x0026CAF8`-`0x0026CAFD` |

</details>

### The story counter

The main story counter is the 16-bit word at payload `+0x0`, class 0 offset 0. 513 scripts declare it alone and 193
declare a 256-word array that starts at the same byte ([Story counter values](story-counter-values.md)).

`0x00265270` is the native reader: while bit `0x1` of `0x02098E20` is set and the payload pointer `0x02098E58`, the
`+0x48` pointer of the slot-0 actor manager at `0x02098E10` stored at `0x0026CAFD`, is not null, it returns the word it
points at, zero-extended, else 0¹. 24 call sites in 22 functions read it, among them the
story schedule `0x00377970`², the input arbiter³ and the music table reader⁴.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00265270`-`0x0026528B` |
| ² | `0x003779A4` |
| ³ | `0x00253DD1` |
| ⁴ | `0x003EAA78` |

</details>

### How scenes move it on

Every script write is a literal, and 268 writes in shipping scripts are reachable:

1. Most are in a zone's director actor, such as `常駐監督` (81 writes), `イベント管理` (31) or `EventDirector` (25),
   most often in its `main` function.
2. 125 lie inside the branch of a test of the counter's current value: an `if`, as in `alc_c01` `EventDirector.main`
   writing 3,260 when the counter is below 3,260, or a case of a switch on it (68).
3. Of the other 143, 5 follow a test in their function but lie outside its branch, as `rwg_a01`
   `EventDirector.main`'s writes of 1,345, 1,355 and 1,360 after the test that guards its 1,342. The other 138
   have no test of the counter before them in their function, mostly `touch`, `touchon` and named event
   functions, which their callers start. A write outside a guard runs only when its function's own path reaches
   it, not on every call.

The first value a shipping script writes is 13 (`naf_a01` `常駐監督.main`) and the last 7,150 (`bhm_d01`
`ボス監督.main`).

The order comes from those tests, not from the store. `POPV`¹ pops the value and stores it through
`0x0026D530`², whose signed 16-bit arm clamps it, `w = v < -32767 ? -32767 : v > 32768 ? 32768 : v`
(-32,767 to 32,768, `0x0026D5C7`-`0x0026D5DF`; 32,768 is stored as the word `0x8000`), and writes the word without
reading the old one³. A write of a value below the counter's lowers it, and a write in item
3 runs whenever its function runs, whatever the counter holds.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00267E60` |
| ² | `0x00267F37` |
| ³ | `0x0026D5C4`-`0x0026D5E3` |

</details>

`0x0026ABA0(i, v)` stores the word `v`, as it is, as word `i` of the payload `[0x02098E58]`, the counter when `i` is 0,
for an `i` below `0x100` (a signed test), while bit `0x1` of `0x02098E20` is set and the pointer is not null¹. For kind 3, `0x00329E60(kind, unit, q, v)` calls it with `q` as `i` and the low word of `v`
(`0x00329EAB`-`0x00329EB2`; [Quests](quests.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0026ABA0`-`0x0026ABC0` |

</details>

The one call of `0x00329E60` in the action effect applier `0x00312170` passes kind 10¹. `0x002FE660`
calls it for the battle orders `0x4149` and `0x4155`-`0x4157` while the unit's phase byte `+0x6B4` is 0, with the kind
from the order record's word `+0x06 >> 12` and `q` the low byte of that word (`0x002FE67B`-`0x002FE6AD`; [Battle
orders](../Battle-Actions/battle-orders.md)).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0031225A`-`0x0031225E` |

</details>

`0x002FE660` reads the old value through `0x00321190`¹ and writes the record's signed word `+0x02` for
`0x4149`, the old value plus it for `0x4155`, and the old value with the bit that word numbers set or cleared for
`0x4156` and `0x4157`². An order record of kind 3 and a low byte of 0 therefore writes the
counter.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002FE6E7` |
| ² | `0x002FE71A`-`0x002FE74E` |

</details>

### Values only the developer menus set

The developer scripts `evt_t*` write 88 values no shipping script writes, reachable or not, among them 0 and 10. The clan board ladder
that writes 11,000 is in code no path reaches. So a counter outside the shipping values comes from a developer menu, an
edited save or native code.

### Flags and quests

The flag banks the story sets are on [Story flags](story-flags.md), with every id the scripts use on
[Story flag ids](story-flag-ids.md). The quest bits that follow the counter in the payload are on [Quests](quests.md).

## Modding notes

- Writing payload `+0x0` moves the story: every script and native reader sees the new value at its next access.
- A script cannot hold a reference to the counter: no script pushes it with `PUSHP`.
- The menus and map groups the counter unlocks are the story schedule in `mapjumpgroupflagrom.bin`
  ([Story flags](story-flags.md)).

## Related

- [Story counter values](story-counter-values.md) - every value written, by script.
- [Story flags](story-flags.md) - the flag banks and the story schedule.
- [Quests](quests.md) - the quest state.
- [Save data](../Saving-Loading-And-Settings/save-data-fields.md) - the payload layout.

### Calls to and from other topics

The functions on this page call, or are called by, functions that belong to other parts of the game. Each topic below lists those calls and the pages that explain the other side.

<details>
<summary>Show the 14 calls with 5 other topics</summary>

**Scripts and script commands** (explained on [script variables](../Scripts-And-Script-Commands/script-variables.md), [script interpreter](../Scripts-And-Script-Commands/script-interpreter.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00267E60`](story-progress.md) | calls | [`0x00262440`](../Scripts-And-Script-Commands/script-variables.md) (on script variables) |
| [`0x00267E60`](story-progress.md) | is called by | [`0x0025E4C0`](../Scripts-And-Script-Commands/script-interpreter.md) World actor script vm: interpret bytecode (on script interpreter) |
| [`0x0026D530`](story-progress.md) | is called by | [`0x00267E60`](story-progress.md) |

**Enemy AI and gambits** (explained on [frame update order](../Engine-Core/frame-update-order.md), [glossary](../Engine-Core/glossary.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FE660`](story-progress.md) | calls | [`0x00321190`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) |
| [`0x00312170`](story-progress.md) | calls | [`0x00321190`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) |
| [`0x00321190`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) | is called by | [`0x00301AD0`](../Enemy-AI-And-Gambits/enemy-order-sets.md) Ai order: evaluate target selector (on enemy order sets) |

**Battle actions** (explained on [battle verbs](../Scripts-And-Script-Commands/battle-verbs.md), [game over](../World-Areas-And-Travel/game-over.md), [action results](../Battle-Actions/action-results.md), [menu map files](../Game-Files-And-Data-Tables/menu-map-files.md), [action definition row](../Battle-Actions/action-definition-row.md))

Each row is a function this page names (left), whether it calls the functions on the right or is called by them, and those functions from this topic. Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x00312170`](story-progress.md) | calls | [`0x0030AB40`](../Battle-Actions/action-range.md) Battle target: classify relationship class (on action range) |
| [`0x00312170`](story-progress.md) | is called by | [`0x00307300`](../Battle-Actions/area-of-effect.md) Battle: process action target (on area of effect)<br>[`0x0030EC00`](../Battle-Actions/action-results.md) Battle action: resolve special sequence targets (on action results) |
| [`0x00321190`](../Enemy-AI-And-Gambits/enemy-order-sets.md) (on enemy order sets) | is called by | [`0x002FE660`](story-progress.md)<br>[`0x00312170`](story-progress.md) |
| [`0x00329E60`](quests.md) (on quests) | is called by | [`0x002FE660`](story-progress.md)<br>[`0x00312170`](story-progress.md) |

**Party** (explained on [identifier spaces](../Engine-Core/identifier-spaces.md))

Each row is a function this page names (left) and the functions from this topic it calls (right). Each function's name is given where the database has one, and the link goes to the page that explains it.

| Function named on this page | | Functions from this topic |
|---|---|---|
| [`0x002FE660`](story-progress.md) | calls | [`0x0031B7E0`](../Engine-Core/identifier-spaces.md) (on identifier spaces) |

</details>

---

[Story flags →](story-flags.md)
