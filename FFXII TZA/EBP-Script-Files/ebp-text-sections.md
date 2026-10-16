---
title: "EBP text sections: the message bank and the field-sign caption bank a script's text ids index"
kind: "format"
category: "EBP script files"
summary: "Sections 2 and 3 of an .ebp script: the offset-table layout both banks share, the flag bit section 2 carries, how each bank is bound to its actor manager, the lookups that turn a text id into a string and what they fail to check, every verb that reads them and where the text ends up on screen, the shipped banks in all nine language trees, and the rules an edit must follow."
addresses: ["00330190", "00330220", "0026C880", "0026C8A0", "00264D60", "00264D90", "002673A0", "01CEB638", "00348DF0", "0034ADA0", "0050EAB0", "002E1E00", "002E0540", "00265680", "002E16B0", "002A2C00", "002B32D0", "00269F20", "00355A00", "00357120", "00356B70", "022C6CA0", "022C6CC8"]
---

# EBP text sections: the message bank and the field-sign caption bank a script's text ids index

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
manager, the directory walker `003304A0` dispatches each present slot:

| Section | Gate in `003304A0` | Handler | Per-manager global | Manager record field | Pending bit |
|---|---|---|---|---|---|
| 2 | `00330519` (count above 2, offset non-zero) | `00330190` | `022C6CA0` | `+0xA0` (`0026C880`) | 4 |
| 3 | `00330534` (count above 3, offset non-zero) | `00330220` | `022C6CC8` | `+0xA8` (`0026C8A0`) | 5 |

The handler takes the manager index from the low four bits of its argument and the section
address from the rest. The manager bind `0026C8C0` zeroes both record fields (`0026CC49`,
`0026CC50`), so a script without a bank leaves a null pointer, not a stale one
([actor managers](../Characters-And-Objects/actor-managers.md)).

## Layouts

Both sections have the same shape. Offsets are from the start of the section.

```
+0x00   u32[n]  entry      n = (entry 0 & 0xFFFF) / 4; there is no count field
                bits 0-15   string offset from the section start
                bit 16      flag (section 2; see Loader behaviour)
                bits 17-31  0 in every shipped entry; never read
+4*n    char[]  strings    NUL-terminated, back to back in entry order
                zero fill to the next 0x40 boundary
```

A text id is an entry number. The strings are glyph codes and control codes, not ASCII: the
character codes are on [battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md)
and [fonts](../Menus-And-HUD/fonts.md), and the control codes, including the choice list `0x0E`, on
[text codes](../Menus-And-HUD/text-codes.md).

## Shipped data

Measured over every `.ebp` in the archive (`ps2data/plan_master/<language>/` for the nine
language trees, plus control scripts under `ps2data/image/ff12/{ch,in}/bin/`).

| Fact | Value |
|---|---|
| section 2 | in 7,466 files: 828 in each of `us`, `de`, `es`, `fr` and `it`, 829 in `ch` and `in`, 830 in `cn` and `kr`, and 8 control scripts |
| section 2 strings | 156,337; 17,327 in `us` |
| section 2 sizes | 64 to 60,544 bytes; 1 to 287 strings, median 7 |
| empty section 2 strings | 2,371 (466 in `us`); none in `ch`, `cn`, `in` and `kr` |
| flagged entries | 33,484 (3,692 in `us`); the upper half of every entry is 0 or 1 |
| strings holding a `0x0E` byte | 33,167, every one of them flagged; 317 more flagged strings hold none: 33 in each of the nine trees and 10 in each control set (`ctl-in`, `ctl-ch`) |
| entry 0 flagged | 1,929 sections (213 in each Latin tree), so the engine's count is 16,384 or more there |
| section 3 | in 3,232 files: 359 per tree, 360 in `in` |
| section 3 strings | 20,818 (2,313 in `us`), at most 38 bytes; no entry is flagged |
| empty section 3 strings | 328: 327 in `it` and 1 in `es`; none in the other trees |
| section 3 sizes | 64 to 1,472 bytes; 1 to 43 strings, median 2 |
| section 3 codes | in the Latin trees the only byte below `0x20` is the space `0x04`, plus lead byte `0x14` in `es`, `fr` and `it`; every caption in `ch`, `cn`, `in` and `kr` holds a `0x0F` escape |
| table checks | in every section the offsets ascend, the first string follows the table, the strings are contiguous and the bytes after the last are zero |

The most common `us` captions are `NOT USED` (351), `Ancient Door` (219), `dummy` (193),
`Way Stone` (130) and `Exit` (89).

## Loader behaviour

### Looking up a string

`00264D60(manager, id)` reads section 2 and `00264D90(manager, id)` section 3; the two differ only
in the record field (`+0xA0`, `+0xA8`):

1. A null bank returns `01CEB638`, an empty string.
2. The id is masked to 24 bits (`00264D77`), so bits 24-31 of a text id do nothing.
3. The count is the whole first dword, sign-extended and shifted right by 2 (`00264D74`,
   `00264D7D`); an id at or above it returns `01CEB638` (`00264D83`).
4. Otherwise the result is the section address plus the entry's low 16 bits (`00264D85`).

Step 3 reads the flag as part of the count. In the 1,929 sections whose entry 0 is flagged the
count is at least 16,384, and an id past the real table returns whatever the bytes there
point to. Nothing compares the table with the section's length.

### The flag

`002673A0(manager, id)` applies the same mask and bound to section 2 (`[manager + 0xA0]` only) and
returns bit 0 of the entry's upper half (`002673C0`, `002673C6`). Section 3 has no such reader.

- `mes` (`0x461`, `00348DF0`) stores the flag in the message slot's byte `+0x38` through
  `002E1E00` (slot record `0215F200 + slot * 0x68`), returns it in the call record, and opens the
  window through `002E16B0` only when the flag is clear.
- `aask_1ff` (`0034ADA0`) does the same but opens the window only when the flag is set.
- `debug_mesask_43` (`0050EAB0`) always opens the window, stores the flag at `+0x38` through
  `002E1D90`, and returns 1 in the call record when it is clear.
- `unkCall_5b6` (`003545B0`) hands the string to `00474070` only when the flag is clear.

While a slot holds a window with `+0x38` set, `002E0540` returns 1 and `00265680` returns 0
(`002656F2`). The bodies that raise hold request 17 when `00265680` returns 0, among them `ucon`,
then keep the field held ([time stop and freeze](../Engine-Core/time-stop-and-freeze.md))
until a close path clears the byte (`002E0780`).

### Readers

| Verb | Id | Handler | Bank | What it does with the string |
|---|---|---|---|---|
| `mes` | `0x461` | `00348DF0` | 2 | message window, as above |
| `aask_1ff` | `0x1FF` | `0034ADA0` | 2 | message window, as above |
| `debug_mesask_43` | `0x2043` | `0050EAB0` | 2 | message window, as above |
| `unkCall_5b6` | `0x5B6` | `003545B0` | 2 | `00474070` |
| `setgaugecounterlabel`, `setgaugecounterunit`, `setgaugetimerlabel` | `0x1BC`-`0x1BE` | `00352A50`, `00352EC0`, `003534F0` | 2 | the gauge, through `003E8F50`, `003E8FC0`, `003E9000` |
| `setfieldsign`, `setfieldsignonce` | `0x174`, `0x175` | `00354F20`, `003555F0` | 2 | the field-sign table `02B59C80` (`003DF760`), entries 6-7 and 4-5 |
| `fieldsignmes` | `0x178` | `00356B70` | 2 | the actor's name text (`00269F20`) |
| `fieldsign` | `0x176` | `00355A00` | 3 | the actor's name text, from the caption id in the sign record `002642C0` returns |
| `fieldsignmesbyid` | `0x179` | `00357120` | 3 | the actor's name text |

`00269F20(actor, text, 0)` stores the text at the actor's `+0xF8` and 0 at `+0x100`; that is the
literal name an actor with a negative name id shows ([NPC names](../Characters-And-Objects/npc-names.md)).

### From the message window to the screen

`002E16B0` places the string at `+0x38` of the request for a new window (`002A2C00`). On the
window's ordinary layout path `002A2C00` passes it to `002A6A80`, which hands it to the window's
text object at `+0xD0` (`002B32D0`); the
text object keeps it at `+0x28` and measures it with `002B2150` (`002B3D50`, `002B3C30`), the
routine that sends every byte below `0x10` to the text interpreter `002AC5F0`. Section 2 text is
therefore read with the codes and lengths on [text codes](../Menus-And-HUD/text-codes.md).

## Modding notes

- Keep each section below 64 KiB: an entry holds a 16-bit offset.
- Add a string by adding an entry and moving the strings; every later offset changes, and the
  first entry must still equal four times the entry count.
- Use only ids inside the table. When entry 0 is flagged, the bound check no longer catches a
  bad id, and the string comes from whatever lies past the table.
- Set bit 16 on a section 2 entry whose string holds a choice list, as the shipped banks do; `mes`
  does not open a window for a flagged entry and `aask_1ff` opens one only for a flagged entry.
- Bits 17-31 of an entry and bits 24-31 of a text id have no effect, and section 3's flag is
  never read.
- Write strings in the language's glyph codes; captions in `ch`, `cn`, `in` and `kr` keep their
  `0x0F` escape.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker that dispatches these sections.
- [Text codes](../Menus-And-HUD/text-codes.md): the control codes inside the strings.
- [Fonts](../Menus-And-HUD/fonts.md): how a character code becomes a glyph.
- [Battle and menu text tables](../Game-Files-And-Data-Tables/battle-text-tables.md): the other text banks and their character codes.
- [NPC names](../Characters-And-Objects/npc-names.md): how the caption stored as an actor's name is shown.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record the banks are bound to.
- [Time stop and freeze](../Engine-Core/time-stop-and-freeze.md): the hold a flagged message keeps raised.
- [Verb table](../Scripts-And-Script-Commands/verb-table.md): the verbs that read the banks.
