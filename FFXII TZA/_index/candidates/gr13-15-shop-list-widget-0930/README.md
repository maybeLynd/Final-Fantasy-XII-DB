# GR-13 / GR-14 / GR-15: the shop list rows, the message-26 layout write, and the list kind of each widget family (OPUS, 2026-09-30)

These three register rows are about the shop list interface on
[the shop table and its stock gates](../../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md).
The static work is from the certified image. The checker is `gr13_15_shop_list_check.py` (output
`gr13_15_shop_list_check.out`, 32 steps, **`FAILS 0`**). It uses the kit's `retool.py`, `regval.py` and `structflow.py`.
Work by SWE2-STRUCT for OPUS. Nothing outside this folder was edited except `structflow.py` (see the last section).

## The answers

### GR-13: the premise is wrong; there is no layout B

**In player terms:** loot and ordinary items are listed the same way as every other shop category. The price you see
and the price you pay come from the same slot of the row. In the sell list, loot that would sell for 0 gil cannot be
picked.

- **`0057DAD0` writes layout A.** Its cursor is `entry + 8` (`0057DAFF lea rbx, [rcx + 8]`), and `entry + 0` is
  `rbx - 8` (`0057DB55`). The page read the cursor as the entry base. The real stores are: the name pointer at `+0`
  (`0057DB98`), the id at `+8` (`0057DB7E`), the class byte at `+0xA`, the owned count or `0xFFFF` at `+0xC`, channel 1 at
  `+0xE`, and **the price at `+0x10`** (`0057DB9F`, `0057DBCC`, `0057DBE0`; the zero-price `bts` is at `0057DBDC`). These
  are the offsets the other three fillers write. The only difference is that `0057DED0` also writes `+0xB`.
- **Such lists do reach the driver, and the driver reads them correctly.** `0057DAD0` fills selectors `0x18` (shop
  category 4, items, class 5) and `0x1B` (shop category 7, loot, class 7) on the Buy tab. On the Sell tab it fills
  `0x0C` and `0x0F`. The driver `0056D370` reads the unit price at `+0x10` and clears bit 31 (`0056D461`, `0056D468`).
- **Who reads a row's price.** There are 14 dword reads of `+0x10` outside the fillers, all in the shop driver's
  family:
  - the driver itself (`0056D461`);
  - its selection test `0056E700` (`0056E71A`, `0056E797`);
  - the four row callbacks `0056CBC0`, `0056CD50`, `0056CF10` and `0056D1B0`, which the driver installs on its list
    control (`0056D66E`–`0056D6A5`, `0056D7EE`);
  - their two draw helpers `0056D870` and `0056DA80`.

  Each of them either compares the whole dword with `0x80000000` (5 sites) or clears bit 31 before using it (9 sites).
  Every `+0x08` read (34 sites) is a word read of the id. Nothing reads a price at `+8`.
- **Who reads the zero-price bit.** The sale path reads it. In sale mode (driver `+0xD8` bit 0), `0056E700` scores 8
  when `dword[row + 0x10] >= 0x80000000` (`0056E715`–`0056E72B`), and the driver then declines the selection
  (`0056D576`–`0056D57D`). The row callback `0056CF10` scores the row the same way (`0056CFF3`). The Sell tab runs the
  driver in sale mode: the shop widget's id `0x5A2` sets `+0x194` bit 0 (`0056DE3D`–`0056DE72`), and `0056C950` passes
  it to the driver's create (`0056D71D`–`0056D736`). The sentinel flag `0x20` is set **only for selector `0x0F`**
  (`0057D3EA or ebx, 0x20` / `0057D3ED cmp esi, 0xf` / `0057D3F0 cmovne`). That selector is the Sell tab's loot row,
  priced at half (band tag 4). So "bit 31" means "cannot be sold" to the sale test, whichever filler set it.
- **Category 7 is loot.** `ItemDefinition_ClassifyEncodedItemCategory` (`002FABD0`) maps id nibble 2 (`0x2xxx`) to 7
  through the table at `00D0F990` (`4, −1, 7, 6, 5, 8, 9, 10`). The shop category is `selector − 0x14` (`0057CFB9`), so
  `0x1B` is category 7. Tail arm 3 resolves those ids with class 7 (`0057D3FF`), and the category-to-class table
  `00D113B8[7]` is also 7.

### GR-14: no, the message-26 write can never reach a shop list

**In player terms:** the scrolling-text animation that rewrites list rows exists only in the inventory menu's lists.
The shop's Buy, Sell and Bazaar lists never run it, so nothing can change a price between the list appearing and your
purchase.

- **`005651E0` runs only inside the four list procedures.** It is entered only by tail jumps from `005636F0`,
  `00563930`, `00563B10` and `00563D20`. No rip reference or data qword names it.
- **Those four procedures are installed in one place.** They are named only by the four `lea`s in `00564B90` and by no
  data qword. The creation path `00564AC0` → `00244F50` → `002465F0` stores the procedure at the widget's `+0`
  (`00246641`). `00564B90` installs one only for widget ids `0x405`–`0x40F`, which have kinds 0–7 (the table at
  `00D233A0`). Kinds 0–7 are selectors 0–7, and none of them is a shop selector (see GR-15).
- **The shop widget has its own procedure.** It is created with `0056E140` (`0056DD66`, the only reference). That
  procedure dispatches messages 1–20 through its table at `0056E3B8` and sends message 26 to `005C5230`, which is
  `xor eax, eax / ret`. The driver `0056D370` sends message 26 to the same stub (`0056D3B8`).
- **So the timing question has no case to answer.** Between the build at `005656AE` and the move at `0056E55A` the
  shop widget does call `002F9860`, `0020E620`, `002D48C0` and `00565A00`. `00565A00` reads only the ids (`+8`) while
  searching. But a message 26 sent to the shop widget or the driver at any time lands in the empty stub.
- **Where the shop list can be.** On the shop widget, `+0xE0` is written only by `005655F0` (`0056563E`, `005656AE`),
  `0056E410` (`0056E561`) and `0056E140`'s message-18 arm (`0056E398`). On a shop widget, `005655F0` runs only from
  `0056E410` (`0056E535`), which moves the list to the driver at `0056E55A`.
- **Who sends message 26.** The senders are the list-control draw bodies `002D2600` and `002D28E0` (both called only
  from `002D1420`). ~~They call the target's own procedure.~~ They call the list control's procedure (`002D2DB0`,
  `002D279E` / `002D2B5C`), which forwards message 26 to the procedure of the control's `+0xC8`
  (`002D2E11`–`002D2E29`). For the shop's list control, that is the driver `0056D370`: it is set at creation from
  the layout loader's owner argument (`0056D776` → `002432CB` → `0029F9AC` → `002D16B0`). The driver sends
  message 26 to the stub (`0056D3B8`). *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr13-15-0930/REVIEW.md) correction wording; the B6 check text in `gr13_15_shop_list_check.py` follows)*

### GR-15: the kind comes from a constant table in every family, except the equip screen's slot index

**In player terms:** what a list shows depends only on the screen and the tab or slot that opened it. That is one of
the inventory menu's eight categories, the shop's Buy, Sell or Bazaar tab, or one of the equip screen's five slots.

| family | writer | where the kind comes from | kinds | selectors reaching `0057CF20` |
|---|---|---|---|---|
| **A**: list procedures `005636F0` / `00563930` / `00563B10` / `00563D20` | `00564780` via `00564010` (source 1, `005640ED`) | the create message `+8`, copied by each procedure to its message's `+0xC` (`0056372F`, `0056395F`, `00563B4D`, `00563D4F`). That is `002465F0`'s copy of create data `+8` (`00246726`), which is `00564AC0`'s slot for the widget id in `00D233A0` (`00564B01`, `00564B0C`). The ids are the eight constants the menu `00565E00` binds: `0x405`–`0x409`, `0x40D`–`0x40F`. | **0–7** (`0x405`→0 … `0x409`→4, `0x40D`→5, `0x40E`→6, `0x40F`→7) | 0–7 (no remap) |
| **B**: the shop widget, procedure `0056E140` | `00564780` via `0056DD50` (source 2, `0056DD8B`) | byte `+0x192`, set from create message `+8` (`0056E16D`–`0056E173`). That is the `00D233A0` slot of the id `00D23920[tab]` (`0057C0F7`–`0057C0FE`). The ids are `0x5AF`, `0x5A2` and `0x5AE`, and the tab is bounded by the three-tab loop (`0057BEA0`). | **32** (Buy), **19** (Sell), **31** (Bazaar) | `005655F0` remaps by row through `0057D5E0`. Kind 32 goes through `00D23D60` to `0x14`–`0x1B` and `0x1D`. Kind 19 goes through `00D23D6C` to `0x08`–`0x0C` and `0x0F`. Kind 31 stays `0x1F`. |
| **C**: procedure `003FDFE0` | `003FD360`: source 3 is `003FD6B0` (`003FD76A`), source 4 is `003FD860` (`003FD8DC`) | The create message `+8` is tested against 1 (`003FE30F`). If it is 1, the path is `003FD860` with **the constant 1** (regval `('C', 1)`). Otherwise it is `003FD6B0` with the message value (`003FE30B`). That value is `003FDA20`'s `ecx`. The only caller of `003FDA20` is `003FF040`, and only when `+0x178 == 0x400`. The only caller of `003FF040` is the equip menu `003FF360` (message 12, sub `0x8001`, `+0x10`), so the value is **the slot row the player picked**. | **0–4** | `0x40`–`0x44` (`dl + 0x40`) |

The table read from the image gives every kind the route kind → selector → filler (step C5). **No selector is shared
between the shop family and the other two.** A and B share the writer `00564780`, and C is the `+0x40`-biased family.
In the whole image, the only byte stores to `+0x17F` are `005647B4` and `003FD371`. Inside the three families'
call-closure (97 functions), no store of any width covers `+0x17F` (step C4).

## Step table

| step | addresses | what it shows |
|---|---|---|
| A1a–c | `0057DAFF`, `0057DB55`, `0057DB7E`, `0057DB98`, `0057DB9F`, `0057DBCC`, `0057DBE0` | `0057DAD0`'s rows are layout A. structflow's write sets for the four fillers agree except `+0xB`. |
| A2a–c | 11 filler calls in `0057CF20`, ret `0057D513`; `005656AE`, `00565785`; 9 `xor ecx, ecx` in `0057D620` | The list is handed to the fillers, returned, and stored only into a widget's `+0xE0`. `0057D620` only counts. |
| A3a–b | 37 + 39 census sites; 41 typed seeds | The holder-field census of the shop, driver and list-widget closures reaches a fixpoint (depth 3 = 12, 5 = 12). Every census load is either a seed or a null test, a store, or the shop widget's child pointer. |
| A4a–e | 14 `+0x10` reads; 34 `+0x08` reads; escapes `0056D56F`, `0056E55A`, `00566631` | Every price consumer masks bit 31 or tests it as a sentinel. `+8` is always the id. Only family-A bodies write `+0x10`–`+0x15` outside the fillers. |
| A5 | `0056E715`–`0056E72B`, `0056D576`–`0056D598`, `0056CFF3`, `0056DE3D`–`0056DE72`, `0056D71D`–`0056D736` | The sale test refuses a bit-31 row. The Sell tab (id `0x5A2`) runs the driver in sale mode. |
| A6 | `0057D3EA`–`0057D3FF`, `0057D33F`, `0057D47F` | Selectors filled by `0057DAD0`: `0x04`, `0x06`, `0x07`, `0x0C`, `0x0F`, `0x18`, `0x1B`. The sentinel is set only for `0x0F`. |
| A7 | `00D0F990`, `0057CFB9`, `00D113B8` | Category 7 is loot. |
| B1–B3 | `00563721`/`53`/`41`/`43`; `00564C0A`–`00564C25`; `00564C4C`; `00246641` | The message-26 arm lives only in the four list procedures, which are created only for ids `0x405`–`0x40F` (kinds 0–7). |
| B4 | `0056DD66`, `0056E14B`–`0056E150`, `0056E3B3`, `005C5230`, `0056D3B8` | The shop widget and the driver route message 26 to the empty stub. |
| B5 | `0056563E`, `005656AE`, `0056E398`, `0056E561`, `0056E535`, `0056E55A` | Every write of the shop widget's `+0xE0`. |
| B6 | `002D2680`, `002D2924`, `002D279E`, `002D2B5C` | The message-26 senders. |
| C1a–b | `005640ED`, `0056372F`…, `00246726`, `00564B01`/`0C`; `00565E81`–`00565F5B` | Family A's kind is the id-table slot. The eight bound ids. |
| C2a–b | `0056DD8B`, `0056E16D`–`73`, `00D23920`, `0057BEA0`, `00D23D60`/`6C`, `01F2CB90` | Family B's kinds 32, 19 and 31, and the remap tables. |
| C3a–b | `003FE30B`–`003FE324`, `003FD8E1`, `003FDA35`/`4B`, `003FF084`, `003FF75F`, `003FE20C`–`003FE27A`, `01F2CC98`, `003FF656`/`78`, `00D23988` | Family C's kind: 1 is a constant, and 0 and 2–4 are the equip slot picked. The high band has five records: `{1,1} {2,3} {2,4} {2,4} {3,5}`. |
| C4 | `003FD371`, `005647B4` | The `+0x17F` writers. |
| C5 | `0057D528`/`14`, `0057D594`/`68` | The kind → selector → filler table. |
| C6 | — | Stable at depth 5. Negative control: without the new seeds the run finds nothing. |
| D1 | `00565C25`, `00565D06`, `00563E37`, `00563F5B`, `003FE2C5` | The band tables have five more reference sites. Three of them read the record's second word (see contradictions). |

**Positive controls** are inside the steps: the driver's known price read `0056D461` (A4a), the 16 known message-26
layout stores such as `005654E1`, `00565508` and `00565537` (A4d), and the known transfer `0056E55A` (A4e).

## Page contradictions found (routed to FABLE, not edited)

On [the-shop-table-and-its-stock-gates.md](../../../12-Items-Equipment-Shops-License/the-shop-table-and-its-stock-gates.md):

1. **The layout table and "a tighter row with no name pointer".** The table gives `0057DAD0` as `+0x00` id, `+0x04`
   count and `+0x08` price. That is the cursor-relative reading. Entry-relative, it is `+0` name, `+8` id, `+0xC` count
   and `+0x10` price (A1). The heading "three fillers because there are two row layouts", and every sentence built on
   layout B, need correcting. GR-13's premise falls with them.
2. **"`+0x10` is not a stable price field … overwritten when the row is laid out."** This is true only for family-A
   lists (the inventory menu). A shop list never receives message 26 (GR-14), so on a shop list `+0x10` is the price
   from build to purchase.
3. **"The three tables have nine reference sites in the entire image, and all nine are inside these two builders …
   `+2` is skipped every time."** This is false image-wide. There are five more rip-relative sites (D1). Three of them
   read the second word: `00563E3E` and `00563F62` on the low band, and `003FE2CC` on the high band. Each passes it
   to `00293110`. The "unread by these two builders" wording still holds.
4. **"The four high-band words at `0x00D23988` are 1, 1, 2, 3" and "the second family's kinds 0 and 1 arrive as
   selectors 0x40 and 0x41".** The high band holds five records, used by kinds 0–4 (selectors `0x40`–`0x44`, C3b).
   The head table also misses the selectors that head arm 4 takes as its default: 0–4 (family A) and `0x42`–`0x44`
   (family C).
5. **The bit table's "bit 5 set by tail arm 3 `0057D3EA`".** The bit is set for selector `0x0F` only (`cmovne` at
   `0057D3F0`), not for `0x06` or `0x1B`. The GR-13 row's reason, "so the question is live for shop stock", does not
   hold for the Buy tab.
6. **§5's "that the object at the widget's `+0xC0` is the driver is read from this pairing, not proven separately".**
   This is now proven: `0056C9BC`–`0056C9CB` creates the widget with procedure `0056D370` and stores it at the shop
   widget's `+0xC0`.

## Limits

- **Family C's range is 0–4 by construction, not by a clamp that was read.** The kind is the row the player picks in
  the equip menu's list. The bound rests on three facts: that list allocates five rows (`003FF656 mov r8d, 5` →
  `002CD4D0`), `003FDFE0` handles cases 0–4, and `01F2CC98` holds five row tables. The list control's own index
  clamp was not read. *Runtime settles it: read `+0x17E` of the equip-slot list widget for each slot.*
- **The census is a direct-call closure of the procedures and the installed row callbacks, restricted to
  `00560000`–`0057FFFF` and `003FC000`–`003FFFFF`.** Within that window it is at a fixpoint. Code that reaches these
  objects only through other indirect calls or from outside the window is not seen. Family-A rows also escape once into
  a constructor message (`005665B0` `00566631`), and that path was not followed. It does not matter for the shop,
  because those lists are never shop lists.
- **The 0x405–0x40F menu is called "the inventory menu" by inference.** The inference rests on its kinds' fillers
  (equipment `0057DED0` class 6, items class 5, loot class 7, class `0xD`) and on its `00252D10(k)` gates. That
  function has no name in the database. The equip menu is `003FF360`, as the database already records.

## Consumers (routed, not edited)

- **The shop page (FABLE):** the six items above; GR-13, GR-14 and GR-15 can be ticked once OPUS publishes the
  register rows.
- **[The encoded id space and the query record](../../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md):**
  that page says `byte[rec + 0x54]` is never written by the fill. This lane shows its consumer: as bit 31 of a
  `0057DED0` row, it makes the sale test refuse the row (A5). So on the static-record path, whether an equipment row on
  the Sell tab can be sold depends on that stale byte. This is a consequence to record there. It was not measured
  here.
- **`_index/OPEN-QUESTIONS.md`** rows GR-13, GR-14 and GR-15: OPUS.

## structflow change (kit)

`Database/Tools/analysis-kit/gfz-scripts/structflow.py` gained two opt-in seeds:

- `seed_calls={(func, callee)}` treats the `rax` after that direct call as the base.
- `(func, disp, address)` triples in `seed_loads` seed only that load. At that address they also seed
  `add r64, qword ptr [X + disp]` as an element pointer at offset 0, which is the `index << 5` + list form.

With neither passed, nothing changes. The gr1, gr4-gr5, gr6 and gr8 checkers were re-run after the change and their
outputs are byte-identical to their committed `.out` files.
