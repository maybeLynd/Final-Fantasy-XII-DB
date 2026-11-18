[Home](../../README.md) / [Menus and HUD](README.md) / Widget messages

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Widget messages: every message id a menu element answers, what it means and who sends it | reference | Menus and HUD | How menus work | The 24-byte message record and the 56 message ids menu widgets use: the framework ids 1-26 with their senders (construction, per-tick update, draw, activation, focus, input turn, owner commands, runs and tweens, destruction and release), the command sub-codes a list or dialog posts to its owner, the private ids 29-53 of the battle menu and map screens and 285-289 of single screens, with handler counts and example senders in widget-messages.tsv. | 0x00247510, 0x002465F0, 0x00248030, 0x00245E60, 0x002473F0, 0x00244830, 0x002481C0, 0x00246C20 |

## What it lists

[`widget-messages.tsv`](widget-messages.tsv) has one row per message id that a widget procedure answers or a sender raises, 56 in all:
1-26, 29-53 and 285-289. The counts come from decoding the 274 widget procedures of the image: the 267 built by
[Widgets](widgets.md)'s constructors, the six base procedures their defaults pass messages to¹, and `0x005651E0`.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003EE420`, `0x003F7F50`, `0x002B6DB0`, `0x002BC3E0`, `0x005519E0`, `0x00553F40` |

</details>

The four item list pane procedures `0x005636F0`, `0x00563930`, `0x00563B10` and `0x00563D20` jump to `0x005651E0` for ids 4,
8-10, 12, 18, 26 and 286 (`0x0056370B`-`0x005637BE`, jumps `0x00563721`, `0x00563953`, `0x00563B41`, `0x00563D43`).
`0x005651E0` answers all of them but 4, so ids 8-10, 12, 18, 26 and 286 count it as well as the four panes.

### The message record

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | id | message id |
| `+0x08` | `u32[2]` | a | first argument |
| `+0x10` | `u32[2]` | b | second argument |

A procedure is called as `procedure(widget, message)` and returns a value that some senders read. Most procedures
dispatch through a jump table and send any other id to `0x005C5230`, which returns 0; 51 procedures have table arms that
do no more than that.

### Framework ids

| Id | Meaning | Sender |
|---:|---|---|
| `1` | construct, with the creator's `a` and `b` | `0x002465F0` |
| `2` | per-tick update | the drain `0x00248030` |
| `3`, `4`, `5` | draw: before the widget's content, after it, after the children | the draw pass `0x00245E60` (`0x002462D0`, `0x0024635A`, `0x002463BC`) |
| `6`, `7` | activated, deactivated | `0x002473F0(widget, on)` (`0x0024740C`-`0x00247418`), repeated down the subtree; a widget changes only when it has bit `0x2` and its bit `0x1` differs from `on`: the bit is then set to `on` and the message sent when it has a procedure (`0x00247423`-`0x0024744E`). The descent goes through `0x00247490`, which applies the same test to each child and does not go below a child it leaves unchanged (`0x002474AB`-`0x002474F4`) |
| `8`, `9` | focus gained, focus lost | `0x00244830` |
| `10`, `11` | input turn for the focus widget; 11 while a widget up its chain is running | `0x002481C0`; also `0x002286B0` |
| `12` | command to an owner: `a` is a sub-command, `b` its argument | `0x00247510` (101 calls in 67 functions) and 11 other sites |
| `13` | a notice carrying an id | the Config screens, `0x002D4330` |
| `14` | opening run started | `0x00246AD0` |
| `15` | closing begins | `0x00244F00`, `0x00244DD0` (`0x00244EF5`), `0x00241940`, `0x002419B0`, `0x00550470` |
| `16` | a resource batch has loaded | `0x00249410`, `0x002494F0`, `0x002495C0` and screen code |
| `17`, `22` | tween channel 0 finished, stepped | `0x00246C20` (`0x00246D7E`-`0x00246DB7`) |
| `18` | being destroyed | `0x00245020` to the widget, `0x002473B0` to its subtree |
| `19`, `20` | forward run finished, backward run finished | `0x00246C20` (`0x0024701E`-`0x0024706B`) |
| `21` | tween channel 1 stepped | `0x00246C20` (`0x00246EF8`) |
| `23` | tween channel 2 stepped | `0x00246C20` (`0x00246F9D`) |
| `24` | released | `0x002482E0` (`0x002483A8`-`0x002483B2`) |
| `25` | animation tick | `0x00246C20` (`0x00246C51`) |
| `26` | per-element query; the reply is used | `0x002D2600`, `0x002D28E0` |

No procedure answers ids 27 or 28.

### Command sub-codes (message 12)

`0x00247510(widget, a, b)` builds message 12 and returns the reply¹. It builds the 24-byte
record on its stack (id 12 at `+0x00`, `a` at `+0x08`, `b` at `+0x10`) and calls the procedure pointer at the
widget's `+0x00` with the widget and the record². For a null widget, or a widget whose
procedure pointer is null, it sends nothing and returns 0³. The sub-codes a list or
dialog posts to its owner:

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00247523`-`0x0024755B` |
| ² | `0x00247523`-`0x00247547` |
| ³ | `0x00247535`-`0x00247540`, `0x0024755B` |

</details>

| `a` | Means | Sent by |
|---|---|---|
| `0x8000` | the cursor moved; `b` is the row | the list `0x002D3BA0` (`0x002D4199`) |
| `0x8001` | the row was confirmed; a non-zero reply stops the list's own handling | `0x002D40FF` |
| `0x8002` | cancel | the list owners, for example `0x0057C480`, `0x00557B90` |
| `0x8003` | clear | `0x00561390` and the gambit editor's list ([Gambits screen](gambit-screen.md)) |
| `0x8004` | a move has ended | `0x002D2DB0` (`0x002D38B5`) |
| `0x8005` | posted right after `0x8000` with the same row | `0x002D41E8` |
| `0x8100`-`0x8103` | the confirmation window's yes, no, cancel and cursor row | `0x0057C480` ([Dialogs](dialogs.md)) |
| `0x8102`-`0x8106` | the item sort bar's close, help and three sorts, to its procedure `0x00566680` | `0x0057C480` |

Screens also use small codes among themselves: `0`, `6` and `7` (two sends each) and `0xE`-`0x1D`, most often `0x12`
(18 of the 101 sends through `0x00247510`) and `0xF` (13).

### Private ids

Ids 29-53 belong to two families only, which use them differently:

- the battle menu (`0x00279E20`, `0x002778C0`, `0x00276D30`, `0x0027AA70`; [Battle menu](battle-menu.md));
- the map screens (`0x002B7590`, `0x002BA700`, `0x002B7B80`, `0x002BAF80`, `0x003CB650`, `0x00552250`, `0x005528C0`;
  [Map screens](map-screens.md)), where 31 is a cancelled page, 32 an open request, 33 a new page and 43 an opened page.

The relay `0x00275F10` sends a chosen id to a chosen widget when it is destroyed: 35 for the map containers and 40 for the
World Map¹. Ids 285-289 each belong to one screen: 285 the yes-or-no and notice
boxes, 286 the item sort bar, 287 the main menu's lists, 288 the script menu host, 289 the gambit lists.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00275F55`-`0x00275F82`, `0x002747B0` |

</details>

The relay is made by `0x002747B0(object, id, key, target)` (137 bytes), under a stack cookie¹. `0x002747B0`
fills a stack record with `target` at `+0x00`, `id` at `+0x08` and `key` at `+0x0C`, and a creation record whose dword
`+0x00` and qword `+0x10` are 0 and whose qword `+0x08` points at the first; message 1 below copies those three fields².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00808C40` |
| ² | `0x002747B7`-`0x002747E1` |

</details>

With a non-null `object` it builds the `0xD8`-byte relay there through
`0x00245000(object, 0xD8, 0x00275F10, creation record)`, else through the factory
`0x00244F50(0xD8, 0x00275F10, creation record)`, and returns that call's answer¹. Both builders are
told on [Widgets](widgets.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002747E5`-`0x00274838` |

</details>

Every call of `0x002747B0` passes a null `object`, the key `0x101` and the caller's own object as `target`: id 35 from
the map containers `0x002B7590`¹ and `0x002BA700`² and from the field-time container `0x003CB650`³, which draws nothing, and id 40 from the World Map's `0x00552250`⁴. `0x003CB650` is told on [Map
screens](map-screens.md).

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x002B76A3` |
| ² | `0x002BA811` |
| ³ | `0x003CB746` |
| ⁴ | `0x005523A4` |

</details>

The relay acts on three messages. Message 1 copies from the record its qword `+0x08` points at: the
qword `+0x00` to the relay's `+0xC0` (the target), the dword `+0x08` to `+0xC8` (the id) and the dword
`+0x0C` to `+0xCC`¹. Message 16 calls `0x00244F00` on the relay when its qword
`+0x08` equals the sign-extended `+0xCC`². Message 18 sends the id; a null
target, or a target whose first qword is null, gets nothing³. Any other message
goes to `0x005C5230`, which answers 0⁴. All four answer 0.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00275FC1`-`0x00275FDC` |
| ² | `0x00275F98`-`0x00275FA8` |
| ³ | `0x00275F70`-`0x00275F7B` |
| ⁴ | `0x00275F3E` |

</details>

The message 18 sends is a stack record with the id in its first dword and 16 zero bytes from `+0x08`;
its dword `+0x04` is not written. The call is to the target's first qword with the target and the
record¹. Message 1 uses the record pointer with no null test².

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00275F55`-`0x00275F82` |
| ² | `0x00275FC1` |

</details>

## Columns

| Column | Meaning |
|---|---|
| `id` | the message id |
| `meaning` | what receiving it means, with the sender's addresses |
| `record_fields` | what `a` and `b` carry |
| `handler_count` | procedures with an arm for the id that does more than the default |
| `example_handlers` | procedures that answer it |
| `example_senders` | delivering functions, with the delivery site |

## Related

- [Widgets](widgets.md) - how widgets are built, attached and animated.
- [Dialogs](dialogs.md) - the list and confirmation widgets' sub-codes.
- [Battle menu](battle-menu.md) and [Map screens](map-screens.md) - the two families of private ids.

---

[← Widgets](widgets.md) | [Menu lists →](menu-lists.md)
