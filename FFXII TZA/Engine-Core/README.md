[Home](../../README.md) / Engine core

# Engine core

The main loop and per-frame update, startup and the values set at boot, the developer tuning console, logging, the object model and the engine's shared state.

Jump to: [Main loop and game states](#main-loop-and-game-states) · [Glossary, ids and limits](#glossary-ids-and-limits) · [Function and class indexes](#function-and-class-indexes) · [Debug tools](#debug-tools) · [PlayStation emulation](#playstation-emulation)

## Start here

Start with these pages, in this order:

1. [Game application object](game-application.md): starts with the root object
2. [Frame update order](frame-update-order.md): shows what it runs each frame
3. [Time stop and freeze](time-stop-and-freeze.md): shows what can pause that frame

## Main loop and game states

What runs each frame, what starts the game, and the states that stop or change it.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Game application object](game-application.md) | Explanation | The game's root object, its vtable and the boot order. |
| [Frame update order](frame-update-order.md) | Explanation | What runs each frame for the field, the battle layer and every unit. |
| [Time stop and freeze](time-stop-and-freeze.md) | Explanation | How menus, cutscenes, Stop magicks and skippable scenes halt actors. |
| [Force fight mode](force-fight-mode.md) | Explanation | The flag behind the fleeing state and what fleeing changes. |
| [Graphics settings](graphics-settings.md) | Explanation | The render settings block, its keys, defaults and shader constants. |
| [Party control modes](party-control-modes.md) | Explanation | The summon, chocobo, town and event-party levels and who sets them. |
| [Startup constants](startup-constants.md) | Explanation | The random seed, frame-rate constant, memory budget and confirm button. |
| [Subsystem update flags](subsystem-update-flags.md) | Explanation | The word switching interface update groups on or off each frame. |

## Glossary, ids and limits

Reference for the terms used here, the game's ids and the engine's fixed limits.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Item and ability ids](item-and-ability-ids.md) | Explanation | The id space behind items and abilities, and its validator. |
| [Engine types](engine-types.md) | Reference table | Every identified engine type with its purpose and owner page. |
| [Glossary](glossary.md) | Reference table | The words used here for engine objects, each with the page explaining it. |
| [Identifier spaces](identifier-spaces.md) | Reference table | The kinds of id and handle passed around, with ranges and invalid values. |
| [Native limits](native-limits.md) | Reference table | The engine's fixed counts and ranges, and what happens past them. |

## Function and class indexes

Lookup tables of functions, classes and virtual slots.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Class hierarchy](class-hierarchy.md) | Explanation | The C++ classes the executable names and what they are. |
| [Call signatures](call-signatures.md) | Reference table | The arguments each function reads and passes on. |
| [Global state accessors](global-state-accessors.md) | Reference table | Every one-instruction getter of a global, with its callers. |
| [Jump thunks](jump-thunks.md) | Reference table | Every one-instruction forwarder and its target. |
| [Vtable methods](vtable-methods.md) | Reference table | Every virtual slot with its class and function. |

## Debug tools

The log call and the developer console left in the game.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Debug logging](debug-logging.md) | Explanation | The log call, its sink and the console prints still in the game. |
| [Debug menu](debug-menu.md) | Explanation | The developer console object, its pages and the rows still reachable. |
| [Debug menu commands](debug-menu-commands.md) | Reference table | Every developer-console row with its label and what it sets. |

## PlayStation emulation

How translated PS2 code and its graphics microprograms still run.

| Page | Kind | What it helps you understand |
|---|---|---|
| [PS2 CPU emulation](ps2-cpu-emulation.md) | Explanation | The in-memory PS2 register set translated assembly runs on. |
| [PS2 VIF1 and VU1 emulation](ps2-vif1-vu1-emulation.md) | Explanation | The packet decoder, recompiled microprograms and GS replay. |
