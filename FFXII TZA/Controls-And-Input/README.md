[Home](../../README.md) / Controls and input

# Controls and input

Controller, keyboard and mouse input and how it reaches the game.

Jump to: [How input works](#how-input-works) · [Keys, bindings and names](#keys-bindings-and-names) · [Escape Mode and vibration](#escape-mode-and-vibration) · [Engine input registries](#engine-input-registries)

## How input works

How devices are found, how their input reaches the game and what can block it.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Action availability](action-availability.md) | Explanation | How the game decides a menu or button cannot be used right now. |
| [Controllers](controllers.md) | Explanation | How a pad is detected and which controller object ends up handling it. |
| [Controls](controls.md) | Explanation | How input reaches the game, from codes to the button mask and stick bytes. |

## Keys, bindings and names

How keys and buttons are bound, stored, shown and named.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Control remapping](control-remapping.md) | Explanation | How the Config screen's binding rows edit the keyboard profiles. |
| [On-Screen Keyboard](on-screen-keyboard.md) | Explanation | How the On-Screen Keyboard opens with F9 and what its panels show. |
| [Keymap file](keymap-file.md) | Format | The keymap.ini file: its rules, slots and what makes the game discard it. |
| [Control names](control-names.md) | Reference table | Each input name the game knows and the code keymap.ini stores for it. |

## Escape Mode and vibration

Escape Mode's binding and latch, and how a pad vibrates.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Escape Mode](escape.md) | Explanation | How Escape Mode's R2 binding, latch and shutoffs work. |
| [Vibration](vibration.md) | Explanation | How the game starts, steps and pauses pad vibration patterns. |

## Engine input registries

Every named input object of the engine's input registries.

| Page | Kind | What it helps you understand |
|---|---|---|
| [Phyre input semantics](phyre-input-semantics.md) | Reference table | Each named engine input object: its class, code and who reads it. |
