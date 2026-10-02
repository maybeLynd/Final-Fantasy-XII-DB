
## GI-18: the editor's and the pick list's arms below entry level (OPUS, 2026-10-01)

Static, read whole from the shipping image, one level into each callee. The message names are the framework's
(the-widget-message-protocol.md): 1 construct, 2 reconcile, 5 draw after children, 8 / 9 focus gained / lost,
10 directional input, 12 sub-command, 15 about to be destroyed, 16 resource batch complete, 17 position tween
finished, 18 being destroyed, 19 / 20 transition finished, 22 position tween stepped, 26 per-element query.
Id-12 messages are `{12, a, b}` records from `00247510`. Both screens post them to themselves through
`002D1AC0(child, a)`, which supplies the child's cursor slot `(+0xF2 + +0xF4) * +0xEC + +0xEE + +0xED` as `b`.
The editor's row `i` is `self + 0x160 + i * 0x20`. `02CA96E0`, `02CA96F8` and `02CA9700` / `02CA9708` are the
three-editor pointer tables, one editor per gambit set.

**The editor `005691E0`.** Twelve table arms (ids 1, 2, 5, 8, 9, 10, 12, 16, 17, 18, 19/20, 22, 26 - 19 and 20 share
one) plus the peeled `0x121`:

| id | arm | work |
|---|---|---|
| 1 | `005692A2` | Setup. `+0x360 = 0`; claims the first free entry of `02CA96E0[0..2]` (`005692EB`) into `+0x35C`. Compared with the member's current set index (`dword [[02EBF190] + 0x7370 + member * 4]`), it places itself as the centre pane (`02CA9700`, layout element 6), the next pane (`02CA9708`, element 8) or the previous one (`02CA96F8`, element 7), each through `002432B0`. It wires the two list children, calls `002D45C0(child, 0)` (`0056945E`) and seeds nine word pairs at `+0x300`: the first word 1, the second 0 when `00264150()` is non-zero and 1 otherwise (`005694C6`-`005694F2`). It sets `+0x354 = 0x80808080`, `00285F20(member)` and `+0x343 = 0x80`. It then opens a resource batch (`00249580` / `00292210` / `00249410`) whose completion is message 16. |
| 2 | `005696A5` | `0056A3D0(self)` (the pane-transition state machine), then `005678F0(self)` (the cursor blink tick). |
| 5 | `00569718` | When the cursor row's byte `+0x17` is set (`00569751`), draws one fixed sprite from `[+0x38]` at `+0x348` / `+0x34A` (`002426F0`); `0056B350` writes all three when the pick list opens. |
| 8 | `0056961E` | `+0x358 \|= 1`; `002D45C0([+0xD8], 1)`; then posts `0x8000` to itself (`002D1AC0`). |
| 9 | `00569671` | `+0x358 &= ~1`; `002D45C0([+0xD8], 0)`. |
| 10 | `0056981E` | Nothing while `+0x360` is set. If the active editor's `+0x340` bit 0 is set, the input goes to the list child (`002D3A50`). Otherwise `002D45C0(child, 1)`; a non-zero `002C1A80` party gate undoes it and returns. It stores the slot and `+0x33E` in the editor's pair table. One pad branch moves the member's set index -1 mod 3 (`005699F0`), the other +1 mod 3 (`00569AF1`). Each plays sound `0x51`, slides the three panes (`002468A0`) and rotates the three pane pointers (`00569BED`-`00569C0C`). Masks `0x800` / `0x400` step to the next / previous member (`00568280` / `00567990`). With a non-zero slot, two more bits cycle `+0x33E` through 0-2. |
| 12 | `00569DC1` | Sub-command switch on `msg->a - 0x8000` (below). |
| 16 | `0056955F` | Starts the forward transition (`00246AD0`), lazy-creates two helper widgets (`002CBE40`, `002CF3E0`), then **snapshots** the live set `+0xF4..+0x127` into `+0x128..+0x15B` (`005695CE`-`005695FE`). |
| 17 | `00569781` | Only for `msg->a == 1`. A pending edit (`+0x360`) is committed through `00569F90` and cleared. A pending pick-list close (`+0x342`) clears the cursor row's `+0x17` (`005697F5`) and re-enables the list child (`002D49C0(child, 0)`). |
| 18 | `00569236` | `002922F0()`. **Only when byte `[[0209AC30] + 0xDEB]` is set** does it write the id-16 snapshot `+0x128`, not the live set, through `003282C0(member, self + 0x128)` (`0056924B`-`00569259`). The centre editor also calls `002814E0(0x4B9)`. It then nulls `02CA96E0` / `02CA96F8` at `+0x35C` (`0056928F`, `00569293`). |
| 19, 20 | `0056960B` | `002D7580(0, 1)`. |
| 22 | `005696B9` | When `+0x33B` is set, `005685B0(+0x336, +0x337, &rect)` and `002D78B0(6, rect)`. |
| 26 | `00569ED4` | `00568FE0(self, msg->b, msg->a)`: the per-row slide step (rows `+0x18` state, `+0x1A` current, `+0x1C` target, 4 units per call), copied to the child's `+0x114` / `+0x116`. |
| `0x121` | `00569EE3` | `+0x331 = 6` when `+0x331` is non-zero. |

| id-12 sub-id | arm | work |
|---|---|---|
| `0x8000` | `00569E6D` | Prompt text `0xCF1`, or `0xCEE` / `0xCEF` for `+0x33E` 1 / 2, or `0xCF2` when `msg->b` is 0 (`002F9860`, `00291D70`, `00291D80`); then `+0x344 = [0208F570]`, the tick (`00569ECA`). |
| `0x8001` | `00569E4C` | `00567D80(self, msg->b)` when the centre editor's `+0x360` is clear: opens the pick list (`0056B350`, modes 1 / 2). |
| `0x8002` | `00569E42` | `005679D0(self)`, the pane rebuild. |
| `0x8003` | `00569E06` | When `00264150()` is 0: `0056A1D0(self, -1, msg->b, 0, 0)`, mode -1. That empties row `b`: both texts `0x3EB`, id `-1`, bit `b - 1` of `+0x124` cleared, then committed. A result other than -1 is played as a sound (`00249C60`). |
| `0x8004` | `00569DED` | `005680E0(self)`, the pane reset, when `+0x342` is clear. |
| other | `00569EF3` | returns 0. |

**The pick list `0056B4D0`.** The 19 table entries; ids 3-7, 11, 13, 14, 16 and 17 share `0056BB53` (`005C5230`,
`xor eax, eax; ret`):

| id | arm | work |
|---|---|---|
| 1 | `0056B57F` | `[02CA96D8] + 0xC8 = 0` (`0056B58D`). Builds two layout descriptors, `00D234A8` (callback `0056BBD0`) and `00D234D0` (callback `0056A780`). It copies the create record (editor `+0xC8`, `+0x584`, `+0xD0`, mode `+0x588`) and the editor's cursor bytes into `+0x58E`..`+0x59C`, then lays out the first page (`0056ADA0`, `0056BC70` / `0056A890`). |
| 2 | `0056B9D4` | `0056BE40(self)`; then counts `+0x580` down. At zero it posts `0x8000` to itself (`0056BA04`). `+0x580` is a frame countdown, set to `0xB4` by `0056AC50` (`0056ACBB`). |
| 8 | `0056B7E9` | `+0x5A0 \|= 2`; `002D45C0([+0xC0], 1)`. |
| 9 | `0056B808` | `+0x5A0 &= ~2`, then the id-15 tail. |
| 10 | `0056B81E` | Page up / page down on the pad masks (`0056AAC0` / `0056AD50`; wrapping needs a second mask), clamping the cursor to the new page's count. Without a page change the input goes to the list child (`002D3A50`). |
| 12 | `0056BA10` | `0x8001` → `0056AC50(self, row)`. It shows a refusal text and arms the `0xB4` countdown for a disabled row. Otherwise `0056A1D0` writes the picked id into the editor's row (mode 1: word `+0x10`, mode 2: word `+0x12`) and commits. `0x8002` → `0056AB00`, the close. |
| 15 | `0056B80F` | `+0x580 = 0`. |
| 18 | `0056B516` | Sends `{0x121}` to the editor `[+0xC8]` when `+0x58E` is set; `[02CA96D8] + 0xC8 = 1`. |
| 19 | `0056B7AE` | With `+0x58E`: `+0x58F = 0x18`, word `+0x58C = 0x302`; with `+0x5A0` bit 2: editor `+0x358 \|= 2`. |

**Not established here:** what sets `[0209AC30] + 0xDEB` (no writer in the gambit region), so whether id 18's
snapshot write is a revert-on-cancel; which of the three pad words `02F97390` / `02F97392` / `02F97394` is pressed,
repeat or held. What the player sees is not claimed.
