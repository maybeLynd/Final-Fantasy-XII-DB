---
title: "Control names: every key and button name the game registers, the code each one stands for, and which names are aliases of one another"
kind: "reference"
category: "Controls and input"
addresses: "00876C80, 00879570, 02EB83B8, 02EB9D80"
---

## What it lists

The game names every key and button through two registries: the key names, type `PInputKeySemantic`, and the
channel names, type `PInputChannelSemantic`. Each name is a 32-byte node in the image; its value is the control code
that [keymap.ini](keymap-file.md) stores for that key or button.

### How the registries are built

At start-up one small static initialiser per node passes the node to a registry insert, `00876C80` for the key names
and `00879570` for the channel names, then registers its destructor with `atexit`. The insert
(`00879570`-`008795F3`):

1. returns `0x11` when the node has no name (`00879574`-`00879588`);
2. returns `0x12` when a node with the same name is already in the list (`0087958D`-`008795CE`, `008795E6`);
3. otherwise puts the node at the front of the list whose head is `02EB9D80` for channels, `02EB83B8` for keys
   (`008795D0`-`008795DA`).

For example, `0016BDE0` inserts the key node of `Key_Numpad_8` (`01F458C8`) and registers `008BCF20`, which at exit
sets the node's type pointer to `01CD89D8` and unlinks it from the key list `02EB83B8` (`008BCF20`-`008BCF7A`).

| Node offset | Field |
|---|---|
| `00` | type pointer |
| `08` | the name, an ASCII string |
| `10` | the next node, linked at start-up |
| `18` | the code, a 32-bit integer |

### What the codes are

- 0 is `Empty`, no binding.
- 11-26 are the sixteen pad buttons. Each has several names: a number, a PlayStation name, an Xbox name, and for
  11-13 a mouse-button name too, `Button_LeftMB`, `Button_MiddleMB` and `Button_RightMB`.
- 28-123 are the keyboard keys, 96 names, each with one name in both registries.

The mouse buttons the keymap can bind are codes 1-3, and no registered name has those codes
([keymap.ini](keymap-file.md)). So the `*MB` names bind pad buttons 11-13, not the mouse.

The key registry's 97 names are all in the channel registry; the channel registry adds the 46 button names. The
channel registry's 143 names have 113 distinct codes, in 16 groups of aliases.

## Columns

`control-names.tsv`, one row per name, sorted by code:

| Column | Meaning |
|---|---|
| `code` | the node's value, the code keymap.ini stores |
| `name` | the registered name |
| `registries` | `channel`, `key` or both |
| `band` | `none`, `pad button` or `keyboard` |
| `aliases` | the other channel names with the same code, or `-` |
| `channel_node`, `key_node` | the node's address in each registry, or `-` |

## Related

- [keymap.ini](keymap-file.md) - the file that stores these codes.
