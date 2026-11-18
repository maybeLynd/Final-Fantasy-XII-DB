[Home](../../README.md) / [Controls and input](README.md) / Control names

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Control names: every key and button name the game registers, the code each one stands for, and which names are aliases of one another | reference | Controls and input | Keys, bindings and names | Each name in the game's two input name registries, the key names and the channel names: the code its node holds, which is the code keymap.ini stores, the registries it is in, whether it is a pad button or a keyboard key, and the other names with the same code, with how the registries are built at start-up and why the mouse-button names bind pad buttons. | 0x00876C80, 0x00879570, 0x02EB83B8, 0x02EB9D80 |

## What it lists

The game names every key and button through two registries: the key names, type `PInputKeySemantic`, and the
channel names, type `PInputChannelSemantic`. Each name is a 32-byte node in the image; its value is the control code
that [keymap.ini](keymap-file.md) stores for that key or button.

### How the registries are built

At start-up one small static initialiser per node passes the node to a registry insert, `0x00876C80` for the key names
and `0x00879570` for the channel names, then registers its destructor with `atexit`. The insert¹:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00879570`-`0x008795F3` |

</details>

| Step | What happens | Where in the code |
|---|---|---|
| 1 | returns `0x11` when the node has no name; | `0x00879574`-`0x00879588` |
| 2 | returns `0x12` when a node with the same name is already in the list; | `0x0087958D`-`0x008795CE`, `0x008795E6` |
| 3 | otherwise puts the node at the front of the list whose head is `0x02EB9D80` for channels, `0x02EB83B8` for keys, and returns 0. | `0x008795D0`-`0x008795DA`<br>`0x008795D4` |

Names are compared byte by byte, the node's `+0x08` string against each listed node's¹.
`0x00876C80` is the same code over the key list `0x02EB83B8`: `0x11` at `0x00876C90`, `0x12` at `0x00876CF6`, and the
insert and 0 at `0x00876CE0`-`0x00876CEA`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x008795A0`-`0x008795C5` |

</details>

For example, `0x0016BDE0` inserts the key node of `Key_Numpad_8`¹ and registers `0x008BCF20`, which at exit
sets the node's type pointer to `0x01CD89D8` and unlinks it from the key list `0x02EB83B8`².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x01F458C8` |
| ² | `0x008BCF20`-`0x008BCF7A` |

</details>

| Node offset | Field |
|---|---|
| `+0x00` | type pointer |
| `+0x08` | the name, an ASCII string |
| `+0x10` | the next node, linked at start-up |
| `+0x18` | the code, a 32-bit integer |

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

[`control-names.tsv`](control-names.tsv), one row per name, sorted by code:

| Column | Meaning |
|---|---|
| `code` | the node's value, the code keymap.ini stores |
| `name` | the registered name |
| `registries` | `channel`, `key` or both |
| `band` | `pad button` or `keyboard`; `-` for code 0 (`Empty`) |
| `aliases` | the other channel names with the same code, or `-` |
| `channel_node`, `key_node` | the node's address in each registry, or `-` |

## Related

- [keymap.ini](keymap-file.md) - the file that stores these codes.
- [Phyre input semantics](phyre-input-semantics.md) - the engine's own named semantics for the same button codes, and its input-source classes.
