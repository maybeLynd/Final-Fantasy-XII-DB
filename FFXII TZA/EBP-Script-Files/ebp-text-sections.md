---
title: "EBP text sections: the message bank and the field-sign caption bank a script's text ids index"
kind: "format"
category: "EBP script files"
addresses: "0x00330190, 0x00330220, 0x0026C880, 0x0026C8A0, 0x00264D60, 0x00264D90, 0x002673A0, 0x01CEB638, 0x00348DF0, 0x0034ADA0, 0x0050EAB0, 0x002E1E00, 0x002E0540, 0x00265680, 0x002E16B0, 0x002A2C00, 0x002B32D0, 0x00269F20, 0x00355A00, 0x00357120, 0x00356B70, 0x022C6CA0, 0x022C6CC8"
---

## What the player sees

Every line a zone or a cutscene says comes from its script's section 2: what an NPC says when
spoken to, a Save Crystal's prompt, a Moogle's yes-or-no question, a Way Stone's list of
destinations and the subtitles of a scene. Section 3 holds short captions such as `Ancient Door`,
`Way Stone` and `Exit`, which become the name tag of the object the player stands next to. The
script holds no text itself, only numbers: renumbering a bank changes what every speaker in the
zone says without touching the bytecode.

## Where it comes from

Both banks are sections of the `.ebp` container ([EBP script container](ebp-script-container.md)):
section 2 at directory slot 2 and section 3 at slot 3. When a script file loads for an actor
manager, the directory walker `0x003304A0` dispatches each present slot:

| Section | Gate in `0x003304A0` | Handler | Per-manager global | Manager record field | Pending bit |
|---|---|---|---|---|---|
| 2 | `0x00330519` (count above 2, offset non-zero) | `0x00330190` | `0x022C6CA0` | `+0xA0` (`0x0026C880`) | 4 |
| 3 | `0x00330534` (count above 3, offset non-zero) | `0x00330220` | `0x022C6CC8` | `+0xA8` (`0x0026C8A0`) | 5 |

The handler takes the manager index from the low four bits of its argument and the section
address from the rest. The manager bind `0x0026C8C0` zeroes both record fields (`0x0026CC49`,
`0x0026CC50`), so a script without a bank leaves a null pointer, not a stale one
([actor managers](../Characters-And-Objects/actor-managers.md)).

## Layouts

All multi-byte fields are little-endian.

Both sections have the same shape. Offsets are from the start of the section.

```
+0x00   u32[n]  entry      n = (entry 0 & 0xFFFF) / 4; there is no count field
                mask 0xFFFF   string offset from the section start
                bit 0x10000      flag (section 2; see Loader behaviour)
                mask 0xFFFE0000  0 in every shipped entry; never read
+4*n    char[]  strings    NUL-terminated, back to back in entry order
                zero fill to the next 0x40 boundary
```

Both banks are used in place inside the loaded `.ebp`. The handler stores only the section address (`0x003301BB`,
and the record field), and a lookup returns that address plus the entry's low 16 bits (`0x00264D85`-`0x00264D8A`), so
a string is read from the section itself ([looking up a string](#looking-up-a-string)).

A script text id is an entry number. The strings are glyph codes and text codes, not ASCII: the
character codes are on [battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)
and [fonts](../Menus-And-HUD/fonts.md), and the text codes, including the choice list `0x0E`, on
[text codes](../Menus-And-HUD/text-codes.md).

## Shipped data

Measured over every `.ebp` in the archive (`ps2data/plan_master/<language>/` for the nine
language trees, plus control scripts under `ps2data/image/ff12/{ch,in}/bin/`).

| Fact | Value |
|---|---|
| section 2 | in 7,466 files: 828 in each of `us`, `de`, `es`, `fr` and `it`, 829 in `ch` and `in`, 830 in `cn` and `kr`, and 8 control scripts |
| section 2 strings | 156,337; 17,327 in `us` |
| section 2 sizes | 64 to 60,544 bytes; 1 to 287 strings, median 7 |
| empty section 2 strings | 2,371 (466 in `us`); 0 in `ch`, `cn`, `in` and `kr` |
| flagged entries | 33,484 (3,692 in `us`); the upper half of every entry is 0 or 1 |
| strings holding a `0x0E` byte | 33,167, every one of them flagged; 317 more flagged strings hold no `0x0E` byte: 33 in each of the nine trees and 10 in each control set (`ctl-in`, `ctl-ch`) |
| entry 0 flagged | 1,929 sections (213 in each Latin tree), so the engine's count is 16,384 or more there |
| section 3 | in 3,232 files: 359 per tree, 360 in `in` |
| section 3 strings | 20,818 (2,313 in `us`), at most 38 bytes; no entry is flagged |
| empty section 3 strings | 328: 327 in `it` and 1 in `es`; 0 in the other trees |
| section 3 sizes | 64 to 1,472 bytes; 1 to 43 strings, median 2 |
| section 3 codes | in the Latin trees the only byte below `0x20` is the space `0x04`, plus lead byte `0x14` in `es`, `fr` and `it`; every caption in `ch`, `cn`, `in` and `kr` holds a `0x0F` escape |
| table checks | in every section the offsets ascend, the first string follows the table, the strings are contiguous and the bytes after the last are zero |

The most common `us` captions are `NOT USED` (351), `Ancient Door` (219), `dummy` (193),
`Way Stone` (130) and `Exit` (89).

## Loader behaviour

### Looking up a string

`0x00264D60(manager, id)` reads section 2 and `0x00264D90(manager, id)` section 3; the two differ only
in the record field (`+0xA0`, `+0xA8`):

1. A null bank returns `0x01CEB638`, an empty string.
2. The id is masked to 24 bits (`0x00264D77`), so bits `0xFF000000` of a script text id do nothing.
3. The count is the whole first dword, sign-extended and shifted right by 2 (`0x00264D74`,
   `0x00264D7D`); an id at or above it returns `0x01CEB638` (`0x00264D83`).
4. Otherwise the result is the section address plus the entry's low 16 bits (`0x00264D85`).

Step 3 reads the flag as part of the count. In the 1,929 sections whose entry 0 is flagged the
count is at least 16,384, and an id past the real table returns whatever the bytes there
point to. Nothing compares the table with the section's length.

### The flag

`0x002673A0(manager, id)` applies the same mask and bound to section 2 (`[manager + 0xA0]` only) and
returns bit `0x1` of the entry's upper half (`0x002673C0`, `0x002673C6`). Section 3 has no such reader.

- `mes` (`0x461`, `0x00348DF0`) stores the flag in the message slot's byte `+0x38` through
  `0x002E1E00` (slot record `0x0215F200 + slot * 0x68`), returns it in the call record, and opens the
  window through `0x002E16B0` only when the flag is clear.
- `aask_1ff` (`0x0034ADA0`) does the same but opens the window only when the flag is set.
- `debug_mesask_43` (`0x0050EAB0`) always opens the window, stores the flag at `+0x38` through
  `0x002E1D90`, and returns 1 in the call record when it is clear.
- `unkCall_5b6` (`0x003545B0`) hands the string to `0x00474070` only when the flag is clear.

`0x00474070(text, a, b, c, d, record)` builds a `0x1D8`-byte widget with procedure `0x00474100` (`0x00244F50`, `0x004740D3`)
from the string and the verb's other four arguments; `unkCall_5b6` passes its script record's `+0xB0` as `record`
(`0x00354628`-`0x00354644`). The widget's procedure `0x00474100`:

- on construction (message 1) builds the text through `0x002A3090` (`0x00474271`);
- on the draw after its content (message 4) draws the second picture at its `+0x1D0`, `+0x1D4` (`0x001829C0`,
  `0x0047416C`);
- on command `0x12` (message 12) destroys itself (`0x00474149`).

`unkCall_5b7` (`0x00354BE0`) tail-jumps to `0x00474040`, which destroys it.

| Global | Type | Start | Meaning | Set by | Read by |
|---|---|---|---|---|---|
| `0x02CA6C80` | `void*` | 0 (zero-filled tail) | the widget `0x00474070` built; a self-destroy on command `0x12` leaves it set | `0x00474070` (`0x004740D8`); `0x00474040`, 0 after destroying it with `0x00245020` (`0x00474055`) | `0x00474040` (`0x00474044`) |
| `0x02CA6C78` | `void*` | 0 (zero-filled tail) | the `record` argument, held only while the widget is built: `0x00474100` copies it into the text request on message 1 | `0x00474070` (`0x004740BF`), then 0 once the widget exists (`0x004740DF`) | `0x00474100` (`0x00474253`) |

No other instruction reaches either: no other RIP-relative, image-base-relative or 32-bit offset reference names them.

While a slot holds a window with `+0x38` set, `0x002E0540` returns 1 and `0x00265680` returns 0
(`0x002656F2`). The bodies that raise hold request 17 when `0x00265680` returns 0, among them `ucon`,
then keep the field held ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md))
until a close path clears the byte (`0x002E0780`).

### Readers

| Verb | Id | Handler | Bank | What it does with the string |
|---|---|---|---|---|
| `mes` | `0x461` | `0x00348DF0` | 2 | message window, as above |
| `aask_1ff` | `0x1FF` | `0x0034ADA0` | 2 | message window, as above |
| `debug_mesask_43` | `0x2043` | `0x0050EAB0` | 2 | message window, as above |
| `unkCall_5b6` | `0x5B6` | `0x003545B0` | 2 | `0x00474070` |
| `setgaugecounterlabel`, `setgaugecounterunit`, `setgaugetimerlabel` | `0x1BC`-`0x1BE` | `0x00352A50`, `0x00352EC0`, `0x003534F0` | 2 | the gauge, through `0x003E8F50`, `0x003E8FC0`, `0x003E9000` |
| `setfieldsign`, `setfieldsignonce` | `0x174`, `0x175` | `0x00354F20`, `0x003555F0` | 2 | the field-sign table `0x02B59C80` (`0x003DF760`), entries 6-7 and 4-5 |
| `fieldsignmes` | `0x178` | `0x00356B70` | 2 | the actor's name text (`0x00269F20`) |
| `fieldsign` | `0x176` | `0x00355A00` | 3 | the actor's name text, from the caption id in the sign record `0x002642C0` returns |
| `fieldsignmesbyid` | `0x179` | `0x00357120` | 3 | the actor's name text |

`0x00269F20(actor, text, 0)` stores the text at the actor's `+0xF8` and 0 at `+0x100`; that is the
literal name an actor with a negative name id shows ([NPC names](../Characters-And-Objects/npc-names.md)).

### From the message window to the screen

`0x002E16B0` places the string at `+0x38` of the request for a new window (`0x002A2C00`). On the
window's ordinary layout path `0x002A2C00` passes it to `0x002A6A80`, which hands it to the window's
text object at `+0xD0` (`0x002B32D0`); the
text object keeps it at `+0x28` and measures it with `0x002B2150` (`0x002B3D50`, `0x002B3C30`), the
routine that sends every byte below `0x10` to the text interpreter `0x002AC5F0`. Section 2 text is
therefore read with the codes and lengths on [text codes](../Menus-And-HUD/text-codes.md).

## Modding notes

- Keep each section below 64 KiB: an entry holds a 16-bit offset.
- Add a string by adding an entry and moving the strings; every later offset changes, and the
  first entry must still equal four times the entry count.
- Use only ids inside the table. When entry 0 is flagged, the bound check no longer catches a
  bad id, and the string comes from whatever lies past the table.
- Set bit `0x10000` on a section 2 entry whose string holds a choice list, as the shipped banks do; `mes`
  does not open a window for a flagged entry and `aask_1ff` opens one only for a flagged entry.
- The bits under mask `0xFFFE0000` of an entry and the bits under mask `0xFF000000` of a script text id have no effect, and section 3's flag is
  never read.
- Write strings in the language's glyph codes; captions in `ch`, `cn`, `in` and `kr` keep their
  `0x0F` escape.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches these sections.
- [Text codes](../Menus-And-HUD/text-codes.md): the text codes inside the strings.
- [Fonts](../Menus-And-HUD/fonts.md): how a character code becomes a glyph.
- [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md): the other text banks and their character codes.
- [NPC names](../Characters-And-Objects/npc-names.md): how the caption stored as an actor's name is shown.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record the banks are bound to.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the hold a flagged message keeps raised.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the verbs that read the banks.
