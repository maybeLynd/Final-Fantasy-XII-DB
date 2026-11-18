[Home](../../README.md) / [EBP script files](README.md) / Actor manifest

| title | kind | category | group | summary | addresses |
|---|---|---|---|---|---|
| Actor manifest: the script section that lists the models its bind verbs name by position | format | EBP script files | Script sections | Section 12 of an .ebp script: a count and a list of 32-bit bound ids, each a model number and a letter class, stored on the script's actor manager at +0x100 and read back by index whenever a bind verb is given an argument above 0xFFFFFF; the loader, the reader, the 60,939 shipped entries and their letters, and the rules for editing the table. | 0x0032FB70, 0x0026CE40, 0x00263F80, 0x002E9A60, 0x002640C0, 0x002ED6F0, 0x003304A0, 0x022C6DA8, 0x02099D70, 0x0026C8C0, 0x0032ED80 |

## What the player sees

The characters, monsters, treasure chests, gadgets and weapons a zone or event script brings on
screen. When a script binds a model to an actor it usually names the model by its position in this
table, so the table decides which body, chest or prop appears. A wrong entry puts a different model
in the scene; a missing one gives the bind no model.

Each entry is a letter and a number. The letter picks the kind of resource the model is loaded from, and the number,
counted in steps that depend on the letter, picks the file within that kind.

## Where it comes from

Slot 12 of the [EBP script container](ebp-script-container.md) directory, in zone scripts
(`ps2data/plan_master/<language>/plan_map/...`) and event scripts (`.../event/...`). The container
walker `0x003304A0` hands it to `0x0032FB70` with the script's actor manager index packed into the low
four bits of the pointer.

## Layouts

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u32` | count | entries that follow |
| `+0x04` | `entry[count]` |  | 4 bytes each |

```
then zero padding to the section's 0x40-byte boundary
```

Entry:

| Offset | Type | Name | Meaning |
|---|---|---|---|
| `+0x00` | `u16` | number | model number within its letter class |
| `+0x02` | `u16` | letter | ASCII letter class, high byte 0 |

Read as one little-endian dword, an entry is `(letter << 16) | number`, which is the engine's bound
id: the bits under mask `0xFF0000` are the letter class and the bits under mask `0xFFFF` the number
([script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md)). `0x002ED6F0` maps the
letter to a resource kind and file index: `C`, `M`, `N`, `S`, `t` and `w` index directly, `b` and `g`
by two, `m` by 11, and `c`, `n` and `s` by 25; any other letter becomes kind 1.

## Shipped data

<details>
<summary>Show the shipped data</summary>

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
| a stem built as number plus 1000 is the name of some `obj_finish` model | `m` 50 of 57, `n` 76 of 112, `c` 5 of 16 distinct numbers |
| a built stem is the file the game loads for that number | 2 of the 482 pairs, `c` 5 and `m` 76 |
| a stem built from the number itself is the name of some model | `g` 77 of 97, `w` 14 of 54, `b` 10 of 12, `s` 10 of 13, `t` 8 of 10 |
| high-detail models | `obj_finish/in/high` ships 47 `hc*.cm`, 80 `hn*.cm` and 5 `hs*.cm` files |

The per-number table is [`ebp-actor-manifest-ids.tsv`](ebp-actor-manifest-ids.tsv) beside this page: letter, number,
a stem
built by the rules above, whether a model of that name ships, and how many `us` containers use the pair.

### Columns of ebp-actor-manifest-ids.tsv

| Column | Holds |
|---|---|
| `model_stem` | a name built from the number by the rules above; the game does not read it, and the file of each entry is in the table below |
| `resolves` | `yes` when a model file with the name in `model_stem` ships, `no` when none does, which says nothing of the entry's own file: `yes` on 250 of the 482 rows, the per-letter counts in the two stem rows of the table above; `no` on all rows of the letters `C`, `N` and `S` |

### Every entry and what names it

`Database/Tools/catalogues/script_model_bindings.py` reads the `us` scripts and writes three tables:

- [`ebp-actor-manifest-entries.tsv`](ebp-actor-manifest-entries.tsv): one row per entry, 6,771, with its file.
- [`ebp-actor-manifest-calls.tsv`](ebp-actor-manifest-calls.tsv): one row per call that names an entry, 25,316, with
  its actor and the blocks around it.
- [`ebp-actor-manifest-header-references.tsv`](ebp-actor-manifest-header-references.tsv): one row per header field
  that names an entry, 1,083.

An entry's file is the one the executable's path array names. `0x002ED6F0` gives the resource kind and the file index,
and the array holds the path. All 6,771 entries have a path there and the file ships. Entry `c` 0 is
`chara\c10\c1004\c1004.cm`, for example, and the name built from its number, `c1000`, is no file at all.

A verb names an entry with a constant of this form:

```python
reference = 0x3000000 + entry        the argument 0x002E9A60 receives
```

All 25,316 model arguments in the `us` scripts have this form, and each entry is below its table's count. The calls
come from the instruction stream. The argument text and the blocks come from the decompiled listing of the same file.
In every function the two list the same verbs and the same constants of `0x1000000` and above, in the same order.

| Verb | Calls | Model argument | Resolved at |
|---|---|---|---|
| `bindp2_d4` | 9,877 | first of three | `0x0033F378` |
| `modelread` | 4,539 | only | `0x00340FB7` |
| `modelreadsync` | 4,531 | only | `0x003414B3` |
| `bindp2` | 2,061 | only | `0x0033F378`, entered from `0x00340380` |
| `bindc` | 1,561 | second of three | `0x00343B42` |
| `modeldispose` | 1,319 | only | `0x0034234E` |
| `bindh` | 706 | only | `0x00344F1F` |
| `settrapresource` | 390 | only | `0x0035540E` |
| `puppetbind` | 285 | second of four | `0x00343A99` |
| `puppetbind_41d` | 24 | second of two | `0x00343A99`, entered from `0x00345AE0` |
| `bindp2_d6` | 22 | first of two | `0x0033F378`, entered from `0x0033FC60` |
| `unkCall_5cb` | 1 | only | `0x0033F378`, entered from `0x00340380` |

The image header names entries in two more places. Both are in `header-references`:

- The chest word at `+0x88`, read by `0x0026E060` for `setuptreasure` while manager 0 is current. All 385 words at or
  above 0 name a letter `t` entry: entry 0 in 364 scripts, 4 in 19 and 5 in 2. All 1,966 `setuptreasure` calls are in
  zone scripts.
- The list at `+0x80`, in 141 zone scripts, 698 pairs, each id a reference of the form above. `0x0035A270`
 ¹ and `0x0035AB50`² walk it, and `0x0037C3F0` reads one id³.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x0035A2E7` |
| ² | `0x0035ABC7` |
| ³ | `0x0037C50B` |

</details>

| `named_by` | Entries | Meaning |
|---|---|---|
| `calls` | 5,663 | at least one verb call in the script's code |
| `calls+list` | 617 | verb calls, and the `+0x80` list |
| `chest` | 385 | the chest word only |
| `list` | 81 | the `+0x80` list only |
| `no_call_found` | 25 | 23 in event scripts and 2 in zone scripts |

`no_call_found` reports the end of this reading: no call in that script's code and no header field names the entry.
It does not say that the game never binds it. Of the entries with calls, 537 have only loading or release verbs in
their script, with no bind verb; the `verbs` column shows which.

A call's `conditions` are the blocks around it in its function. A function runs when a request is filed for it
([script requests](../Scripts-And-Script-Commands/script-requests.md)): by a REQ-family verb in another function, by
the engine through `0x003DBB60`, or from the start list¹. The
rows are from the `us` scripts, and the manifests are the same in all nine trees, as the table above says.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x00266C50` |

</details>

### Columns of the three tables

| column | what it holds |
|---|---|
| all: `script`, `kind` | the script's path under `plan_master/us`, and `zone` or `event` |
| all: `entry`, `bound_id`, `letter`, `number` | the position in the table, its dword in hexadecimal, and the two parts |
| all: `path` | the file as the executable writes it |
| entries: `reference` | the constant that names the entry, in hexadecimal |
| entries: `resource_kind`, `file_index` | what `0x002ED6F0` gives, the kind in hexadecimal |
| entries: `constructed_stem` | `model_stem` of the ids table, the built name |
| entries: `stem_is_file` | `yes` when the built name is the name of the file in `path` |
| entries: `calls`, `verbs` | the number of calls, and the count for each verb |
| entries: `actors`, `named_by` | the actors holding those calls, and the table above |
| calls: `actor`, `actor_index`, `function` | where the call is; the index is the actor's place in the directory |
| calls: `symlink_actors` | actors that run the same code under their own names, `-` for none |
| calls: `code_offset` | the call instruction's offset in the code section, in hexadecimal |
| calls: `verb`, `verb_id`, `arguments` | the verb and the argument text |
| calls: `conditions` | the enclosing blocks, outermost first, `-` for none |
| header: `source`, `position` | `chest_word` and `0x88`, or `list_80` and the pair's place |
| header: `raw` | the word with the reference form applied, or the list's id, in hexadecimal |
| header: `mask` | the pair's second dword, in hexadecimal, `-` for the chest word |
| header: `setuptreasure_calls` | the script's `setuptreasure` calls, `-` for a list pair |

</details>

## Loader behaviour

### Binding

- The walker sets pending bit `0x200` of the manager's word in `0x022C6E48` when slot 12 is present
 ¹, then calls `0x0032FB70`².
- `0x0032FB70` splits the argument into manager index (low four bits) and pointer, stores the pointer
  at `0x022C6DA8 + index × 8`³ and passes it to `0x0026CE40`, which stores it at `+0x100` of
  the manager's `0x288`-byte record (`0x0026CE51`;
  [actor managers](../Characters-And-Objects/actor-managers.md)).
- It clears bit `0x200`⁴ and, when the pending word has emptied, runs the manager's finaliser
  `0x0032F1B0`.
- When the pending word holds no bit other than bit `0x1`, it also clears bit `0x08` of byte `+0x11` of the
  manager record that `0x00263FF0` returns.
- For manager 0, when bits `0x202` of the pending word are clear, it runs `0x0025AFC0(0)` and
  `0x002EACC0(0x00331990, [0x022C6D28])`.
- Nothing is parsed, copied or checked at load. The pointer refers into the loaded file, so the table
  is live for as long as the script stays loaded.
- The manager bind `0x0026C8C0` zeroes `+0x100`⁵ and the manager reset `0x0032ED80` reads and
  clears the `0x022C6DA8` copy⁶.

<details>
<summary>Where in the code</summary>

| | Code |
|---|---|
| ¹ | `0x003304F0` |
| ² | `0x003305FA` |
| ³ | `0x0032FB9B` |
| ⁴ | `0x0032FBB3` |
| ⁵ | `0x0026CC31` |
| ⁶ | `0x0032F0B7`, `0x0032F0F0` |

</details>

### Reading

`0x002E9A60` turns a script's model argument into a bound id. An argument above `0xFFFFFF` is a table
reference: it calls `0x00263F80` with the current manager record (`0x002640C0` returns `[0x02099D70]`),
which keeps the low 24 bits as the index and:

- returns entry `index` as a dword when the table exists and the index is below `count`
  (`0x00263F92`, signed compare; `0x00263F97`);
- returns 0 when the index is at or past `count`;
- returns the low 24 bits unchanged when the manager has no table.

Arguments up to `0xFFFFFF` skip the table and go through `0x002EB7A0`. The bind verbs that reach
`0x002E9A60` and what they do with the bound id are on the script name bindings page.

## Modding notes

- A script refers to entry `k` by position, so append new models at the end; inserting or removing
  an entry renumbers every later reference in that script, which includes its chest word and its
  `+0x80` list.
- Keep `count` equal to the number of entries and pad the section with zeros to its 64-byte slot.
- Use a letter `0x002ED6F0` knows (`b`, `c`, `g`, `m`, `n`, `s`, `t`, `w`, `C`, `M`, `N`, `S`) and keep
  the high byte 0, as every shipped entry does; any other letter loads from resource kind 1.
- An index past `count` binds model 0 rather than failing, so a short table fails quietly.
- The nine language copies are identical; change all of them, or the scene differs by language.

## Related

- [EBP script container](ebp-script-container.md): the directory and the walker.
- [Script name bindings](../Scripts-And-Script-Commands/script-name-bindings.md): bound ids, the letter table and the bind verbs.
- [Actor managers](../Characters-And-Objects/actor-managers.md): the manager record and its `+0x100` field.
- [Actor model rebuild](../Characters-And-Objects/actor-model-rebuild.md): how a bound model is applied to an actor.
