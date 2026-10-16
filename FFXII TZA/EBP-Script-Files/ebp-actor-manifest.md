---
title: "Actor manifest: the script section that lists the models its bind verbs name by position"
kind: "format"
category: "EBP script files"
addresses: "0032FB70, 0026CE40, 00263F80, 002E9A60, 002640C0, 002ED6F0, 003304A0, 022C6DA8, 02099D70, 0026C8C0, 0032ED80"
---

## What the player sees

The characters, monsters, treasure chests, gadgets and weapons a zone or event script brings on
screen. When a script binds a model to an actor it usually names the model by its position in this
table, so the table decides which body, chest or prop appears. A wrong entry puts a different model
in the scene; a missing one gives the bind no model.

## Where it comes from

Slot 12 of the [EBP script container](ebp-script-container.md) directory, in zone scripts
(`ps2data/plan_master/<language>/plan_map/...`) and event scripts (`.../event/...`). The container
walker `003304A0` hands it to `0032FB70` with the script's actor manager index packed into the low
four bits of the pointer.

## Layouts

```
+0x00  u32  count     entries that follow
+0x04  entry[count]   4 bytes each
then zero padding to the section's 0x40-byte boundary

entry
+0x00  u16  number    model number within its letter class
+0x02  u16  letter    ASCII letter class, high byte 0
```

Read as one little-endian dword, an entry is `(letter << 16) | number`, which is the engine's bound
id: bits 16 to 23 are the letter class and bits 0 to 15 the number
([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)). `002ED6F0` maps the
letter to a resource kind and file index: `C`, `M`, `N`, `S`, `t` and `w` index directly, `b` and `g`
by two, `m` by 11, and `c`, `n` and `s` by 25; any other letter becomes kind 1.

## Shipped data

Measured over all 10,036 EBP2 containers in the nine language trees.

| Fact | Value |
|---|---|
| containers with section 12 | 7,578: 842 per language, 587 zone scripts and 255 event scripts |
| languages | the 842 tables are byte-identical in all nine trees |
| entries | 60,939 (6,771 per language); 1 to 55 per table, median 3 |
| section lengths | 64 bytes (6,534), 128 (567), 192 (9), 256 (468); padding zero in all |
| letters per language | `n` 3,100, `g` 1,287, `c` 819, `C` 440, `t` 410, `m` 348, `w` 157, `N` 131, `b` 39, `s` 32, `S` 8; no `M` |
| letter high byte | 0 in every entry |
| distinct numbers (`us`) | `n` 112 (0 to 174), `g` 97 (0 to 103), `N` 66 (1 to 86), `m` 57 (1 to 253), `w` 54 (1 to 321), `C` 40 (0 to 46), `c` 16 (0 to 21), `s` 13, `b` 12, `t` 10, `S` 5 (0 to 4) |
| number plus 1000 names an `obj_finish` model stem | `m` 50 of 57, `n` 76 of 112, `c` 5 of 16 distinct numbers |
| number names a stem directly | `g` 77 of 97, `w` 14 of 54, `b` 10 of 12, `s` 10 of 13, `t` 8 of 10 |
| high-detail models | `obj_finish/in/high` ships 47 `hc*.cm`, 80 `hn*.cm` and 5 `hs*.cm` files |

The per-number census is `ebp-actor-manifest-ids.tsv` beside this page: letter, number, the model
stem by the rules above, whether that stem ships, and how many `us` containers use the pair.

## Loader behaviour

### Binding

- The walker sets pending bit 9 of the manager's word in `022C6E48` when slot 12 is present
  (`003304F0`), then calls `0032FB70` (`003305FA`).
- `0032FB70` splits the argument into manager index (low four bits) and pointer, stores the pointer
  at `022C6DA8 + index × 8` (`0032FB9B`) and passes it to `0026CE40`, which stores it at `+100`<sub>h</sub> of
  the manager's `288`<sub>h</sub>-byte record (`0026CE51`;
  [actor managers](../Characters-And-Objects/actor-managers.md)).
- It clears bit 9 (`0032FBB3`) and, when the pending word has emptied, runs the manager's finaliser
  `0032F1B0`.
- When the pending word holds no bit other than bit 0, it also clears bit `08`<sub>h</sub> of byte `+11`<sub>h</sub> of the
  manager record that `00263FF0` returns.
- For manager 0, when bits `202`<sub>h</sub> of the pending word are clear, it runs `0025AFC0(0)` and
  `002EACC0(00331990, [022C6D28])`.
- Nothing is parsed, copied or checked at load. The pointer refers into the loaded file, so the table
  is live for as long as the script stays loaded.
- The manager bind `0026C8C0` zeroes `+100`<sub>h</sub> (`0026CC31`) and the manager reset `0032ED80` reads and
  clears the `022C6DA8` copy (`0032F0B7`, `0032F0F0`).

### Reading

`002E9A60` turns a script's model argument into a bound id. An argument above `FFFFFF`<sub>h</sub> is a table
reference: it calls `00263F80` with the current manager record (`002640C0` returns `[02099D70]`),
which keeps the low 24 bits as the index and:

- returns entry `index` as a dword when the table exists and the index is below `count`
  (`00263F92`, signed compare; `00263F97`);
- returns 0 when the index is at or past `count`;
- returns the low 24 bits unchanged when the manager has no table.

Arguments up to `FFFFFF`<sub>h</sub> skip the table and go through `002EB7A0`. The bind verbs that reach
`002E9A60` and what they do with the bound id are on the script name bindings page.

## Modding notes

- A script refers to entry `k` by position, so append new models at the end; inserting or removing
  an entry renumbers every later reference in that script.
- Keep `count` equal to the number of entries and pad the section with zeros to its 64-byte slot.
- Use a letter `002ED6F0` knows (`b`, `c`, `g`, `m`, `n`, `s`, `t`, `w`, `C`, `M`, `N`, `S`) and keep
  the high byte 0, as every shipped entry does; any other letter loads from resource kind 1.
- An index past `count` binds model 0 rather than failing, so a short table fails quietly.
- The nine language copies are identical; change all of them, or the scene differs by language.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): bound ids, the letter table and the bind verbs.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record and its `+100`<sub>h</sub> field.
- [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md): how a bound model is applied to an actor.
