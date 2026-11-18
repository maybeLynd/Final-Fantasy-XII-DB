[Home](../../README.md) / Scripts and script commands

# Scripts and script commands

How area and event scripts run: the script virtual machine, its instructions, and every native command a script can call.

Jump to: [The script machine](#the-script-machine) · [Script commands](#script-commands) · [Event scenes](#event-scenes)

## Start here

Start with these pages, in this order:

1. [Script interpreter](script-interpreter.md): starts with the machine itself
2. [Script variables](script-variables.md): adds where it keeps values
3. [Script requests](script-requests.md): shows how functions get run
4. [Verb dispatch](verb-dispatch.md): crosses into native code
5. [Native commands](native-commands.md): shows verbs that take time

## The script machine

How scripts run: the interpreter, its variables and requests, and how a script reaches native code.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Script interpreter](script-interpreter.md) | Explanation | The opcodes, value stack and registers, and how a script waits and resumes. |
| [Script variables](script-variables.md) | Explanation | The storage classes behind script variables and how long each lasts. |
| [Script requests](script-requests.md) | Explanation | How a script function is filed on an actor, started and retired. |
| [Verb dispatch](verb-dispatch.md) | Explanation | How a script's call id reaches a native handler and what the guards refuse. |
| [Native commands](native-commands.md) | Explanation | The command tables, their callbacks and how a long-running verb waits. |
| [Script name bindings](script-name-bindings.md) | Explanation | How a script names a model by number and the binding table behind it. |
| [Script binding lifecycle](script-binding-lifecycle.md) | Lifecycle | A model binding from the script naming it to its release. |

## Script commands

What script verbs can do, what their arguments address and the verb table itself.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Battle verbs](battle-verbs.md) | Explanation | What a script can do to a unit's battle actions. |
| [Party verbs](party-verbs.md) | Explanation | The verbs changing the battle party, appearance and standard motions. |
| [Reward verbs](reward-verbs.md) | Explanation | Every verb adding or removing items, gil, equipment or party members. |
| [Script verb arguments](verb-arguments.md) | Reference table | What each argument of a script verb addresses in the game. |
| [Script verb table](verb-table.md) | Reference table | Every script call id with its name, callbacks and argument count. |

## Event scenes

How scenes load, run and end, and what they do to the world and the party.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Event scenes](event-scenes.md) | Explanation | Loading, starting, waiting on and disposing a scene, movies and skips. |
| [Party during scenes](party-during-scenes.md) | Explanation | Hiding the party, the summon leader and the event party modes. |
| [World lock](world-lock.md) | Explanation | The stop request that holds the world still for a scene or talk. |
