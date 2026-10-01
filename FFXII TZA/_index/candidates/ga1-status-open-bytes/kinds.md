> Drafted by a Claude Opus 5.5 subagent pass under FABLE, 2026-09-27; the scratch instruments it names are not published. The control `ga1_open_bytes.py` (G4, G5) re-checks the table selection and each list user's call site from the bytes.

# GA-1: which on-screen list each status order key feeds

Date: 2026-09-27. Static reads of `Tools/work/exe/FFXII_TZA.exe` (image base 0x120000). The tools were capstone,
`y1p_all.txt`, `xref.py`, `riprefs.py` and `ibrel.py`, plus two scratch scripts: `ga1k_raw.py` (a raw branch index)
and `ga1k_cls26.py` (a sweep of the class-26 query sites). Every address below is an instruction or function entry
that I decoded.

## Control

| target | raw index (`ga1k_raw.py`: E8/E9 rel32, 0F 8x rel32, EB/7x rel8, each re-decoded) | `xref.py` | pointer constants |
|---|---|---|---|
| `00275E40` | 1: `0027304C call` (in `00272F80`) | same 1 | no VA qword. One RVA dword, in the `.pdata` begin slot |
| `002D02C0` | 7: `00273C63`, `00273CCA`, `00273D39`, `00273DA9` (in `00273BA0`); `00284044` (in `00283E40`); `002C5768`, `002C5791` (in `002C56F0`) | same 7 | no VA qword. RVA dwords: `.pdata`, plus a chained-unwind entry at `.rdata` `01D71570`/`01D71580` (not code) |
| `0035D490` (cache accessor) | 4: `00271FCD`, `0027319C`, `00273392`, `00273418` | same 4 | `.pdata` only |
| `0035D5C0` (cache init only) | 1: `0028E58A` | same | `.pdata` only |
| `00271FB0`, `00273160`, `00273380`, `00273410`, `00272F80`, `00272F60` | 1, 1, 1, 1, 2, 1 (listed below) | same | `.pdata` only. `00273410` also has an unwind-code coincidence at `01D8C17C` |

Both control functions have callers, so the method works.

**Direct readers of the keys.** `ga1k_cls26.py` found 13 `0035D330` calls with `mov ecx, 0x1a` among the 8 instructions
before them. It then looked for byte reads at `+0x20` to `+0x24` in the next 60 instructions. It found them only in
`00275E40`, `002D02C0` and `003BBD00` (`003BBD79 cmp byte ptr [rax + 0x24], 0xff`), and both known positives appear.
This sweep misses a class number passed in a register.

## Where the cache is, and who reads its tables

- **The cache is a static object at `022C8B08`, not a pointer.** `0035D490` returns it: `lea rax, [rip+..]` at
  `0035D4C4` returns `022C8B08`, and the first call builds it with `00273BA0` at `0035D4AC`.
- It holds 32 records of `0xA8` bytes at `+0x0` to `+0x14FF`, then four 32-qword tables.
- The builder runs `002D02C0` with `r9d` = 1, 2, 3, 4 (`00273C50`, `00273CB7`, `00273D26`, `00273D96`). The tables
  are stored from `lea r8,[rbx+0x1508]` (`00273C7A`), `+0x1608` (`00273CE1`), `+0x1708` (`00273D50`) and
  `+0x1808` (`00273DBD`).

**Reference sweep over `022C8B00` to `022CA420`:**
- `riprefs.py` finds only `0035D4A2`, `0035D4C4` and `0035D5D0`. `0035D510` reads `022C8B00`, a separate word just
  below the cache. The next object starts at `022CA408`.
- `ibrel.py` finds 0 image-base-relative operands.
- The raw cache (`=>022C8B..` to `=>022CA3..`) adds nothing.
- So every table read goes through `0035D490`'s return value, and its four callers are the complete reader set.

**The four readers use their own "listing" index L (`edx`), not `002D02C0`'s kind:**

| L | table | key checked | readers |
|---|---|---|---|
| 1 | `+0x1700` | `+0x23` | `00271FFB`/`0027205A`, `002733BB`, `00273450`; `00273160` has it hard-wired: `002731B0 mov r9,[rcx+rax+0x1700]`, `002731E1 cmp byte ptr [r9+0x23],0xff` |
| 2 | `+0x1600` | `+0x22` | `00271FF4`/`00272052`, `002733B4`, `00273444` |
| 3 | `+0x1800` | `+0x24` | `00271FED`/`0027204A`, `002733AD`, `00273438` |
| other (0) | `+0x1500` | `+0x21` | `00271FE6`/`00272044`, `002733A6`, `0027342C` |

`00275E40` uses exactly this L mapping: 1 -> `+0x23` (`00275ED7`), 2 -> `+0x22` (`00275EB4`), 3 -> `+0x24`
(`00275EAE`), otherwise `+0x21` (`00275EA8`). So `00275E40`'s "kind" is L, not `002D02C0`'s kind. They match as
**`002D02C0` kind = 1 + ...**: L0 -> kind 1, L1 -> kind 3, L2 -> kind 2, L3 -> kind 4.

## The answer

| row byte | record | `002D02C0` kind | table | L (`00275E40` / readers) | users (call site) | kind value passed | screen / list | named by | confidence |
|---|---|---|---|---|---|---|---|---|---|
| `+0x10` | `+0x20` | **0** | not cached | none | `00283E40` @`00284044` (`xor r9d,r9d` `0028403C`); `002C56F0` @`002C5768`, `002C5791` (`xor r9d,r9d` `002C5756`/`002C5780`) | 0 (immediate) | (a) **the party-member panel's status-icon row** in the menu screens (see below). (b) a 32-entry cursor list of statuses in the **action list** procedure (see below) | (a) atlas labels of the callers' procedures: `003FDFE0` "status window" (StatusAlone), `003FF360` "status window + action list", `00285290` "menu list", `00557DB0`/`0055CD40` "license board". (b) atlas label of `002C59D0` "action list" (ActionList) | medium. The screens are named, but the panel/list element inside them is not |
| `+0x26` | `+0x21` | 1 | `+0x1500` | 0 | `00273380` @`0029A423` (`xor edx,edx` `0029A417`); `00271FB0` @`00297D62` (`xor edx,edx` `00297D58`); `00272F60`->`00272F80` @`00298036` (`xor r8d,r8d` `0029802F`), which reaches `00275E40` @`0027304C` and `00273410` @`002730A9` with kind 0 | 0 (immediate) | **the four-slot HUD panel** at `[0209BE80]+0x10F78` (see below) | **not named.** The atlas row for `0029BE50` is unlabelled (layout key `GeneralFrame` only), and the four `0x160` slots are described on OPUS.md and CONTRACT-auto-status-rebuild §13l | medium on the element, low on a screen name |
| `+0x27` | `+0x22` | 2 | `+0x1600` | 2 | `00272F80` @`002C01D6` in `002BFD20` (`mov edx,0x1e` / `lea r8d,[rdx-0x1c]` = 2 at `002C01D2`), which reaches `00275E40` (kind 2) and `00273410` (2) | 2 | **the target-info window**: `002BFD20` is called by `002C0870` at `002C0976` and `002C0A95` | atlas row `002C0870` "target info" (layout key `TargetInfo`). battle-hud-layout-readers.md: `002C0870` reads `TargetInfoMoveY`, "the target-info window's Y" | high |
| `+0x13` | `+0x23` | 3 | `+0x1700` | 1 | `00273160` @`002C71D0` in `002C6F70` (table hard-wired) | none (fixed `+0x1700`) | **the overhead status icon above each unit**, with a two-digit count (see below) | battle-hud-layout-readers.md "Overhead": `002C84E0` (<- `002C7B10` <- `002C7660`) reads `OverHeadStatusNumXSpace/OffsetX/OffsetY`. The data chain into it is traced below | high |
| `+0x02` | `+0x24` | 4 | `+0x1800` | 3 | **no list user.** No caller of `00275E40`, `00271FB0`, `00273380`, `00273410` or `00272F80` passes 3. Every kind argument is an immediate 0 or 2 | n/a | **none on screen.** The table is built and never selected. The only reader of `+0x24` is the battle reaction queue `003BBD00` (`003BBD79`), a gate, not a list | this table's control rows | high for "no UI reader". What (if anything) `+0x1800` was for is not answered |

### The users, read

**`+0x10`, (a) `00283E40`.**
- `r14 = [[0209AC30] + idx*8 + 0xAC8]` (`00283E83`) is a party-member record. Its mask is `[r14+0x44]` (`00284035`).
- The body sorts, caps the list at 11 (`00284058 mov eax,0xb`) and skips status `0x1D`, HP Critical (`00284070`).
- For each remaining status it stores the id into an icon child (`002840A3 mov word ptr [r8+0xa], dx`) and a sprite
  byte from `[rax+rdx*8+7]` (`0028409A`).
- Callers:
  - `002858A0` (a nine-column sweep), which is called by `00285290`, `003FE3A0`, `003FFA20`, `00557DB0` and `0055CD40`;
  - `002C1FF0` (<- `002C2C50` <- `002C2200`/`002C2240`/`002C2320`);
  - `003FE3A0` and `003FE6E0` (<- `003FF360`);
  - `003FFA20` (<- `003FDFE0`, `003FF040`).
- The procedures carry the atlas labels listed in the table.

**`+0x10`, (b) `002C56F0`.**
- It fills a 32-entry list at `[rsi+0xC8]` (`002C5737`).
- The first `002D02C0` gives the count for the selected member's mask, taken from `[0209AC30]+0xDE0` -> `00282DF0`
  -> `+0x44` (`002C574A`-`002C5760`). The count goes to `[rsi+0x14C]` (`002C57C3`).
- The second `002D02C0` lists `ebp`, sorts it (`002C57A2`), and hands the count to `002D4930` (`002C57EC`).
- `ebp` is the member's mask, or `0xFFFFFFFF`, which lists all 32 statuses, when `00254A10()!=0` and
  `00264150()==0` (`002C570A`-`002C572F`).
- Callers: `002C2C50` and `002C59D0`. The latter is the atlas's "action list" procedure, whose `002C5810` walks a
  cursor over 0 to 0x1F.

**`+0x26`, the four-slot panel.**
- `002964D0` builds a `0xB68` widget with handler `0029BE50` and stores it at `[0209BE80]+0x10F78`
  (battle-runtime-mode-ladder.md, `0028FD70`).
- `0029BB40` builds four `0x160` children with handler `0029A0A0`. Each slot takes its unit from the
  `0209BFBE`/`0xC0` bank through `00297C10`.
- Message arm 2 of `0029A0A0` does the following with that unit's `[+0x44]` mask:
  - `00273380(mask, 0)`: the first present status in `+0x21` order goes to `[slot+0x108]` (`0029A42B`).
  - `00297FE0` runs the cycler `00272F60`->`00272F80` over the mask, with period `0x1E`. It then shows the current
    status's text `002F9860(id + 0x46B7)` (`0029805F`) and its icon `[rax+rdx*8+7]` (`002980EF`).
  - `00297D10` -> `00271FB0(mask, 0)` folds the listed statuses' `+0x25` bits into a colour flag word.
- `0x46B7` is not resolved to strings here.
- CONTRACT-auto-status-rebuild §13l/§13m shows that these slots are indexed by `00273320(id)`, the party-slot resolver
  over `022C8084`. That makes it the battle party panel in all likelihood, but no page calls it that.

**`+0x27`, target info.**
- `002BFD20` copies the target's display record into its widget at `+0xC0`. The cycler state at `[rdi+0x2A0]` takes
  `[rdi+0x104]`, which is record `+0x44` (`002C01A4`-`002C01AA`).
- It calls `00272F80(state, 0x1E, 2, [rdi+0x29C], unit)`. The unit is `[rdi+0x288]` or `esi`, chosen by
  `[rdi+0x280]` bit 1 (`002C01B8`-`002C01CE`).
- With a unit, kind 2 also requires `003178C0(unit, id)` (`00275ECE`, `0027310D`). That function returns 0 unless:
  - `[02089340]` bit `0x10` is set;
  - the unit's battle record has byte bit `0x10` set.

  Also, when `[unit+0x698]+5 == 1`, it drops statuses 0, 1 and 31 (`0031790A test eax, 0x80000003`). So the
  target-info list shows a status only when the target passes this gate. What the gate is (for example Libra) is not
  read here.

**`+0x13`, overhead.**
- `002C6F70` is called per actor by `002C8D60` (<- `002C6180`, per-frame group `0x8000`).
- It finds the actor's node in the list `[obj+0x1D70]` (next pointer `+0x18`, actor key `+0x10`) and calls
  `00273160` with the actor (`002C71D0`).
- `00273160` reads the mask `00320C60` = `+0x64 | +0x3C` and walks table `+0x1700`.
- On a hit whose flag has bit 2 (key present):
  - `002C71FD` stores the status index in node `+0x16`;
  - `002C7267` stores the count byte from `0031FC70` in node `+0x28`, the Petrify/Doom count per the status-write page;
  - `002C727A` formats it with `"%2.2d"` (`00915FA4`) into node `+0x29` (`002C7290`);
  - `002C725E` sets node `+0x17` bit `4`.
- The drawer side:
  - `002C62B0` walks the same `[obj+0x1D70]` list (`002C62F1`) and calls `002C7660(obj, node)` (`002C632F`).
  - `002C7660` calls `002C7B10(node)` (`002C78C8 mov rcx, rdi` / `002C78D5`).
  - `002C7B10` reads node `+0x16` as the icon (`002C7BA9`, `002C7C90`, `002C7D7B`). When `+0x17 & 4` (`002C7E59`)
    is set, it calls `002C84E0(node)` (`002C7E75 mov rcx, rsi` / `002C7EA8`), which reads node `+0x29` (`002C854C`)
    and the `OverHeadStatus*` keys.
- The object `002C6180` updates and the one `002C62B0` draws have the same field layout: the `+0x1D70` list,
  `+0x1D78` and `+0x1D7A`. I did not trace that the two pointers are the same instance.

## Side notes (not edits)

- **the-widget-message-protocol.md, `00297FE0`.** It "posts `00272F60` message `0x1E`". In fact `0x1E` is the
  cycler's period argument (`edx`), and `00272F60` is the status cycler, not a message post.
- **the-record-00329220-builds.md.**
  - It calls `00273160` "the privilege decode" and `00273BA0` "the neighbour table the record's grid queries walk".
  - It says the tables are stored "across the `+0x1508`/`+0x1608` regions".
  - In fact they are the four status order tables at `+0x1500`-`+0x18FF`, and `00273160` is the overhead status
    pick.
- **L versus kind.** Anyone citing `00275E40`'s kind as `002D02C0`'s kind will swap L1/L3 with kinds 3/4. The
  mapping in the table above is the one the code uses.
