[Home](../../README.md) / Characters and objects

# Characters and objects

The records behind every character, enemy and object in an area, and how they are created, identified and removed.

Jump to: [Field actors](#field-actors) · [Battle units](#battle-units)

## Start here

Start with these pages, in this order:

1. [Actor record](actor-record.md): introduces the record
2. [Actor managers](actor-managers.md): shows who owns it
3. [Actor lifecycle](actor-lifecycle.md): follows one from start to end
4. [Field runtime](field-runtime.md): shows what runs them each frame
5. [Battle units](battle-units.md): moves to the combat side

## Field actors

The records, managers and frame steps behind the actors in an area.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Actor record](actor-record.md) | Explanation | The record behind every field actor: its pool, classes and sub-objects. |
| [Actor managers](actor-managers.md) | Explanation | The actor manager slots, their records and their camera tables. |
| [Actor lifecycle](actor-lifecycle.md) | Lifecycle | An actor from its manager's bind to release, and when its handle stops working. |
| [Field runtime](field-runtime.md) | Explanation | How each frame runs every actor's script through the manager slots. |
| [Actor model rebuild](actor-model-rebuild.md) | Explanation | How an actor's model, attachments and body are reloaded for its definition. |
| [NPC names](npc-names.md) | Explanation | Where NPC names come from and the story flag that swaps one. |
| [Actor record fields](actor-record-fields.md) | Reference table | The field actor record, offset by offset, with its flag bytes. |

## Battle units

The combat slots, how they are built and the records menus read.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Battle units](battle-units.md) | Explanation | The pool of combat slots, who gets one, and the unit's handle and flags. |
| [Battle unit construction](battle-unit-construction.md) | Explanation | How a party member or enemy definition becomes a battle unit. |
| [Party member status record](party-member-status-record.md) | Explanation | The snapshot of a party member that the menus and HUD read. |
| [Battle unit fields](battle-unit-fields.md) | Reference table | The battle unit record, offset by offset. |
