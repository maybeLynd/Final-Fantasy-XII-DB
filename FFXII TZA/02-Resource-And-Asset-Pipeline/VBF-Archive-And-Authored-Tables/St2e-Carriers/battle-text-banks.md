---
system: The battle text banks — battle_pack.bin's two-level string section behind registry slot 45
category: 02-Resource-And-Asset-Pipeline
status: AUDITED — the banks and their readers read; the 13000 + n composition is closed (the second id is stored in the row, 2026-09-11) and rows 116-127 are the twelve Lore nodes (FX-2, answered 2026-09-15, carried here 2026-09-18); every box ticked
owner_layer: both
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: additive-annotation across GN160 -> GN161 - the records this document rests on are unchanged except for `0023F8B0`, `002875D0`, which gained a plate comment and CodeDomain tags in batch R109 and lost nothing; voided by any delta that removes or rewrites a comment, tag, name, prototype or body range; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "all nine per-language battle_pack.bin copies (us, de, es, fr, it, kr, cn, ch, in): the same fifteen banks with the same counts, and every authored st2e table byte-identical to the us copy; the us banks walked and every action row's name reference resolved (543 / 543), 2026-09-11"
last_reviewed: 2026-09-12
registry_slots:
  - "0x02EBF170"
archive_formats:
  - "wordbanks | explained | word.bin (.bin member): {u32 count 15, u32 offsets[16] (first 68, last the end)}, each block {u32 count, u32 offsets[count+1], packed strings} - the fifteen battle text banks, byte-identical to battle_pack directory entry 61 (+0xF8), the section registry slot 45 binds, rebased by 003846F0 and read through 002B58B0, section 2"
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-battle-text-banks-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The battle text banks — `battle_pack.bin`'s two-level string section behind registry slot 45

> **Every name the battle side prints — actions, equipment, statuses, gambit conditions,
> characters, locations, enemy classes — lives in one section of `battle_pack.bin`, as fifteen
> banks of packed strings addressed by a 16-bit `bank : index` word.** The action table's `+0x34`
> is such a word, which is why the earlier scan of the action table against the *string-id* files
> found nothing: the names are not string ids, they are bank references, and they resolve.

**Corpus validation, before anything else.**

| | |
|---|---|
| file examined | `ps2data/image/ff12/test_battle/us/binaryfile/battle_pack.bin` (281,128 B) — the `us` copy; the other eight copies (`de` 284,048 B, `es` 282,528, `fr` 297,280, `it` 285,176, `kr` 254,944, `cn` 247,208, `ch` 247,384, `in` 246,920) were compared 2026-09-11 (§5.2) |
| section | the directory entry the loaded blob names at `+0xF8`: file offset `0x2BBA8` in `us` |
| banks | **15**, counts 545 · 544 · 1 · 362 · 63 · 32 · 284 · 16 · 629 · 128 · 129 · 512 · 512 · 16 · 64 |
| action rows resolving | **543 / 543** `action_data.bin` rows have `+0x34 >> 11 == 0` and `+0x34 & 0x7FF ≤ 542`; 528 are the identity, 15 are permuted within the same bank |
| positive controls | bank 0 `0x106`–`0x112` = the thirteen Espers (the count [the string-table page](../vbf-archive-and-st2e-tables.md) §7 validated from `help_action.bin`'s block 10); bank 5 entries 2 / 16 / 17 = Petrify / Disease / Lure, the three status names [the two-layer page](../../../10-Status-Periodic-Terminal/Status-And-Augment-Layers/two-layer-effect-model.md) had from a tier-6 source |

---

## 1. What the player sees

"Dismiss", "Belias", "Poison", "Foe: party leader's target", "Rabanastre" — every short battle
string is one entry of one bank here. Modders who change a name change one packed string in the
bank; the engine never sees a string id for these.

## 2. Native mechanism

### 2.1 Binding — the two-level rebase

`FUN_00236C30` binds the battle registry from the loaded `battle_pack.bin` blob (the "STATIC" blob,
resource-pool entry 19). Most slots go through `AreaData_BindAndRebaseSectionDescriptor`
`003845F0`; slot 45 at `02EBF170` goes through **`003846F0` with a depth of 1**
(`00236FCF`–`00236FEA`: `rcx = &02EBF170`, `rdx = blob + [blob + 0xF8]`, `r8d = 1`). `003846F0`
stores the image-relative encoding of the section (`0020E620`, `00384704`–`00384709`), reads its
16-bit count (`00384727`) and walks `count + 1` dword offsets from `+4` (`00384746`, `0038478B`):
with depth left it **recurses** into each entry (`0038476B`), otherwise it **adds the section base
to the offset in place** (`00384780`). So after binding, the table at `02EBF170 + 4` holds
image-relative pointers to fifteen banks, and each bank's `+4` holds image-relative pointers to
its blocks.

### 2.2 Addressing — the `bank : index` word and the packed-string indexer

A reference is a 16-bit word split **5 : 11**: `word >> 11` is the bank (up to 32; 15 exist),
`word & 0x7FF` the block within it. The reader resolves the bank pointer through
`ImageAddress_ResolveRuntimePointer` `0020E600`, then the block pointer, then hands the block to
`002B58B0(block, n)` — the packed-string indexer [the unit-definition page](../../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md)
§2.7 read: a block whose first two bytes are zero holds NUL-terminated strings from `+2` and the
indexer returns the *n*-th; any other block is returned as it is.

Three readers are established:

| reader | word | bank | what it names |
|---|---|---|---|
| `00305F10` (`00305F90`–`00305FD8`) | ~~`action_data.bin`~~ action-table row `+0x34` (`battle_pack.bin` `+0x3C`; corrected 2026-09-12, AY-6) | 0 | the action — the HUD post of the current action's name through `002902D0` |
| `BattleUnit_ApplyUnitDefinition` (`0023A88A`–`0023A8E1`) | enemy row `+0x08` | by the word | the unit's name text, stored at unit `+0x18` |
| `BattleUnit_ApplyUnitDefinition` (`0023AB03`–`0023AB57`) | party row `+0x30` | by the word | the same for a party unit |

Six more functions touch `02EBF170` (`002960B0`, `0031C5D0`, `003214B0`, `00329220`, `00536280`,
`00536410`, found by scanning every rip-relative reference in `.text`); ~~which words they pass is not
read here~~ **§5.1 reads all six (FX-1, 2026-09-11)**.

### 2.3 The character set

The `us` strings use the custom charset the string-table page decoded (`0x20`–`0x39` → `A`–`Z`,
`0x3A`–`0x53` → `a`–`z`, `0x04` space, `0x02` line break, ~~`0xAA` `&`~~ **`0xA0` `&` and `0xAA` `:`** *(corrected 2026-09-17, FABLE, from the `us` pack's bytes: `Axes 04 A0 04 Hammers`, `Salts A7 04 A0 c A8` for "Salts, &c.", and `Foe AA` 159 times for "Foe: "; the st2e page's AY-8 census had it right)*, `0xA8` `.`, `0xA7` `,`,
`0xAC` `'`); the seven bytes after a `0x0F` are an inline escape (colour or numeric variable), seen
as the `<0F>J…` prefix of every `Reserve` / `No name` placeholder.

## 3. Key addresses

| Address | Role | Read? |
|---|---|---|
| `00236C30` | binds the battle registry from the STATIC blob; `00236FCF`–`00236FEA` is slot 45 | the slot-45 site |
| `003846F0` | two-level rebase of a `{u16 count; u32 offset[count+1]}` section (depth in `r8d`) | ✅ |
| `0020E600` / `0020E620` | image-relative pointer resolve / encode | by reference |
| `002B58B0` | packed-string indexer | by reference (unit-definition §2.7) |
| `00305F10` | posts the current action's name to the HUD: row `+0x34` → bank 0 → `002902D0` | ✅ |
| `02EBF170` | registry slot 45 — the bank table | ✅ |

## 4. Data structures and formulas

```struct TextBankTable base=section
+0x00  u16       bankCount      15 in the us file
+0x02  u16       _pad
+0x04  u32[16]   bankOffset     bankCount + 1 entries, section-relative on disk, image-relative after binding
```

```struct TextBank base=bank
+0x00  u16       blockCount
+0x02  u16       _pad
+0x04  u32[1]    blockOffset    blockCount + 1 entries, bank-relative on disk; each block is a packed string list
```

*Not a fence: the offset arrays are `count + 1` long and the last entry is the end sentinel; the
fence grammar cannot express a length read from the header.*

| bank | count | first entries | what it is |
|---:|---:|---|---|
| 0 | 545 | Cure, Blindna, Vox, … Dismount (`0x95`) … Belias–Zodiark (`0x106`–`0x112`) … Dismiss (`0x113`), Quickening (543), SecondJob (544) | **action names**, indexed by ~~`action_data.bin`~~ action-table row `+0x34` *(answered: see the row-`+0x34` entry above - the table is `battle_pack.bin` `+0x3C`, AY-6; 2026-10-02, OPUS)* |
| 1 | 544 | Unarmed, Broadsword, Longsword, … Agate Ring (345), Cameo Belt (372) | equipment names |
| 2 | 1 | dummy | — |
| 3 | 362 | Red Spiral, White Whorl, … Serenity (226), Spellbound (228), Channeling (233–235), … Second Board, Quickening | licence-board node names |
| 4 | 63 | Attack, Magicks, Technicks, … | the battle command list (the same 63 entries as `word.bin` block ~~3~~ 4 *(corrected 2026-10-02, OPUS: `offsets[4]` of `word.bin`, 0-based as `003846F0` walks them; it was block 3 only under the struck `headerSize` reading)*) |
| 5 | 32 | KO, Stone, Petrify, Stop, Sleep, Confuse, Doom, Blind, Poison, Silence, Sap, Oil, Reverse, Disable, Immobilize, Slow, Disease, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Invisible, Regen, Float, Berserk, Bubble, HP Critical, Libra, X-Zone | **status names in status-id order** (0–31) |
| 6 | 284 | Foe: party leader's target, Foe: nearest visible, Foe: any, … | gambit target conditions |
| 7 | 16 | NOT USED × … | — |
| 8 | 629 | No name, Vaan, Balthier, … | character and NPC names |
| 9 | 128 | Antidote Set, Unassuming Surcoat, Gilt Shield, … | bazaar goods |
| 10 | 129 | NOT USED × …, "Increases physical attack damage." (64), "Additional License Board unlocked." (128) | ~~—~~ **the augment table's texts** (class 29 `02EBF040` row `+2`, corrected 2026-09-11, §5.1); mostly NOT USED |
| 11 | 512 | Teleport Stone, Reserve …, Empty Bottle (256) | ~~key items~~ **loot** — the names of class 7 `02EBF098`, a packed-count class (corrected 2026-09-11, §5.1) |
| 12 | 512 | Rabanastre, Nalbina Fortress, Bhujerba, … Giruvegan (80), Blue Bottle (96), Green Bottle … | ~~locations~~ **key items** — class 13's three sub-tables (64 area maps, 32 area names, 416 objects), a bitset class (corrected 2026-09-11, §5.1) |
| 13 | 16 | Hume, Humanoid, Giant, Dragon, Beast, Insect, Plant, Avion, Amorph, Fiend, Elemental, Warmech, ?, Undead, Construct, Ichthian | enemy classes |
| 14 | 64 | Titantoise, Gator, Serpent, Behemoth, Wolf, … Judge, … Rat, Cactus, Pirate, Imperial Army, Dalmascan Army, Rook, Commoner, Unclassified, Ancient Bomb, Yensa | enemy genera |

## 5. What the banks settle, and what they do not

- **`0x113` is Dismiss and `0x95` is Dismount** — the two command ids the engine hard-codes against
  `BattleUnit + 0xBA0` and exempts from the availability gates: dismissing an Esper and dismounting
  a chocobo are the commands that must stay available.
- **`0x106`–`0x112` are the thirteen Espers** (Belias, Mateus, Adrammelech, Hashmal, Cúchulainn,
  Famfrit, Zalera, Shemhazai, Chaos, Zeromus, Exodus, Ultima, Zodiark) and **`0xD0`–`0xE1` the
  eighteen Quickenings** (Red Spiral … Resplendence) — the two id ranges the MP-cost modifier
  leaves untouched.
- **The 32 status names are bank 5 in id order**: 8 Poison, 9 Silence, 10 Sap, 11 Oil, 13 Disable,
  14 Immobilize, 15 Slow, 18 Protect for the ids the formula slots test.
- **The party definition table decodes to its cast.** Registry slot `02EBF130` is the directory
  entry at the blob's `+0x44` (`us` file offset `0x1B6A0`, `00236D99`–`00236DAB`): `st2e`, 40 rows ×
  128 bytes, each row's `+0x30` a bank reference (bank 8, the character names): rows 0–5 **Vaan,
  Ashe, Fran, Balthier, Basch, Penelo**; 6–16 **Reks, Amalia, Basch, Basch, Lamont, Vossler,
  Vossler, Larsa, Reddas, Basch, Reddas** (the guest variants); 17–25 **No name**; 26 **Chocobo**;
  27–39 **Belias, Mateus, Adrammelech, Hashmal, Cúchulainn, Famfrit, Zalera, Shemhazai, Chaos,
  Zeromus, Exodus, Ultima, Zodiark**. Row byte `+0x2B` is 13 for every human, 30 for the Chocobo and
  20 for every Esper. The kind page's "type ids `0x1B`–`0x27`" are rows 27–39: the Espers.
- **The augment rows are named elsewhere.** The 129-row augment table (registry slot 29,
  directory offset `+0xEC`, ~~`{u16 nameId, u16 0x5000 + row, u16 parameter, u16 0xFF}`~~ `{u16 helpId, u16 nameWord = 0x5000 + row, u16 parameter, u16 0xFF}`) *(corrected 2026-10-02, OPUS: the query-record filler reads the augment name from word `+2` (its `+0x1F0A` `movzx ecx, word ptr [rax + 2]`, bank `>> 11`, index `& 0x7FF`); word `+0` is a help id `13000 + n` with `n` the help-text index, not the row (row 103 carries 13041, the `us` `listhelp_ability.bin` text 41 "Increases magick power when HP is full."; row 115 carries 13063))* carries
  `nameId = 13000 + n` for the rows that have a description and `0` for the rest; `13000 + n`
  corresponds to string id `130000 + n` of `listhelp_ability.bin` (64 ids, `130000`–`130063`):
  row 2 → "Improves chance to hit." (the AccuracyBoost the formula pages name), row 16 →
  "Nullifies weather and terrain effects on elemental damage." (Weatherproof), row 17 → "Enables
  the theft of superior and rare items." (Thievery), row 103 → "Increases magick power when HP is
  full."; rows 116–127 have `nameId = 0` and only parameters (`0, 0, 0, 40, 30, 20, 30, 20, 10, 10,
  10, 10`). ~~How the engine composes `13000 + n` into `130000 + n` is not read;~~ *(answered: see §7 - nothing composes it, the row stores the second id; 2026-10-02, OPUS)* the correspondence
  is asserted from the three rows whose descriptions match names the database already had.

### 5.1 The six other readers of `02EBF170`, and which words they pass (FX-1, 2026-09-11)

| reader | what it passes | for |
|---|---|---|
| `FUN_0031C5D0` — the query-record filler ([the encoded-id space page](../../../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md) §2.4) | the **name word of the class's table row**, one arm per class: party `+0x30`, items `+0x08`, equipment `+0x02`, loot `+0x06`, magicks / technicks `+0x04`, gambit conditions `+0x14`, key items `+0x08`, quickenings / bazaar / licence nodes / statuses / elements `+0x00`, actions `+0x34`, commands / schools / categories / augments `+0x02` (21 sites, `0031C6B5` … `0031E4DE`) | record `+0x18`, the name every menu prints |
| `FUN_003214B0` | any `bank : index` word, bounds-checked against the bank count and the bank's block count (`003214CD`–`003214ED`), 0 when either fails | a general resolver; sole caller `005760A0` |
| `FUN_00536280` | `(word, flag)`: flag set → the NPC name dictionary `0026DEA0(word, 1)` ([the NPC name page](../../../04-Actor-Entity/Actor-Names/the-npc-name-dictionary.md)); `0xFFFF` → the empty string at `01CEB638`; else the bank word through `002B58B0(block, 0)` | the battle-message realiser `005369C0` and the slot formatter `00536410` |
| `FUN_00536410` | the **status row's `+0x00`** (`02EBF118`, `00536638`) and the **action row's `+0x34`** (`02EBF138`, `005367FC`–`00536841`), the latter through `00536280` when `00254A10` says so | the formatted battle line ([the message-table page](../../../07-Combat-Action/Post-Result-Events/the-post-result-events-and-the-battle-message-table.md)) |
| `FUN_00329220` | the **party row's `+0x30`** by the display record's `+0x60` (`00329592`) | display record `+0x10` ([the display-record page](../../../04-Actor-Entity/Unit-Display-Record/the-record-00329220-builds.md)) |
| `FUN_002960B0` | the **licence node's `+0x00`** — it walks the class-25 rows whose query record `+0x23` is 1, tests each of the node's eight member words (row `+8` …) as class-20 actions against its argument (query `+0x2C`, `0029615D`), and names the node that contains it (`002961D9`–`0029621F`) | callers `00294860`, `002957C0`: "which licence grants this action" |

So every reader passes a table row's name word or a word it was handed; **none addresses a bank
by number** — the bank is always the top five bits of the word. Three bank labels in §4 were
wrong and are corrected there: bank 11 is the **loot** names (class 7, a packed-count class), bank
12 the **key items** (class 13, a bitset class: 96 area names, then 416 objects), bank 10 the
**augment table's texts** (class 29 reads it).
### 5.2 The nine language copies (FX-3, 2026-09-11)

Every `test_battle/<lang>/binaryfile/battle_pack.bin` in the archive — `us`, `de`, `es`, `fr`,
`it`, `kr`, `cn`, `ch`, `in` — was extracted and compared: **fifteen banks in every copy, with the
same fifteen counts** (545 · 544 · 1 · 362 · 63 · 32 · 284 · 16 · 629 · 128 · 129 · 512 · 512 · 16 · 64),
and **every authored `st2e` table byte-identical to the `us` copy** — licence, equipment, action,
status, party, item, magick, loot, reward, bazaar, augment and gambit sections hash the same in all
nine. Only the strings differ: the five Latin-script copies encode *Vaan* with the same four
bytes (`35 3A 3A 47`), the `kr`, `cn`, `ch` and `in` copies with multi-byte sequences of their own.
So a table edit is language-independent, a name edit is per copy, and the `bank : index` words
that tie the two together are the same in all nine.
## 6. Modding notes

- An action's displayed name is bank 0 entry `row + 0x34 & 0x7FF`; renaming an action is a
  string edit, and giving an action another action's name is a one-word edit of the row.
- Status names come from bank 5 by id; there is no separate table to keep in step.
- The unit name path (enemy row `+0x08`, party row `+0x30`) goes through the same banks, so a new
  unit needs a bank entry, not a string id.

## 7. What is not known

- [x] ~~Which banks the other six readers of `02EBF170` address, and which row words they pass.~~
      **FX-1 ANSWERED 2026-09-11 (§5.1):** each passes a table row's name word — the query-record
      filler for twenty-one classes, the message formatter the status and action words, the display
      record the party word, `002960B0` the licence-node word; none addresses a bank by number.
- [x] ~~How `nameId = 13000 + n` is composed into the `130000 + n` string id~~ — **narrowed
      2026-09-11: nothing composes it.** `13000 + n` is a **low-pool** string id: the resolver
      `002F9860` divides by 1000 (`0x10624DD3`, `sar 6`) — group **13**, index `n` — checks the
      group's blob at `[02F973C0 + 13 × 8]` and returns row `n`'s `u32` through
      `ImageAddress_ResolveRuntimePointer` (`002F98EF`–`002F98FD`); group 13's blob is
      `listhelp_ability.bin`'s own first section, an `st2e` of 64 `u32` rows that read `0x1FBD0 + n`
      = `130000 + n` (the shipped file, decoded). So the second id is *stored in the row*, not
      computed; no constant 13000, 117000, 120000 or 130000 occurs anywhere in `.text`. The file's
      string section decodes to 64 help texts (row 2 *Improves chance to hit*, 9 *Increases physical
      damage dealt while empty-handed*, 16 *Nullifies weather and terrain effects*, 17 *Enables the
      theft of superior and rare items*, 27 *Doubles EXP earned*, 36 *Reduces MP cost by half*, 63
      *Move with great celerity* …; 19, 22, 24, 26, 35, 38 and 42–61 empty; 20, 21, 23, 30, 33, 34,
      40 `NOT USED`), so **rows 116–127 have no help text at all** — their identity is still what the
      formula slots do with them. What `0020E600` makes of a row word of 130,000 is not read. **FX-2.**
      > *Narrowed further 2026-09-12 (FABLE).* Two facts from the bytes. **(1) Rows 116–127 do carry a
      > text reference**: their word `+2` is ~~`0x5070`–`0x507F` = 20,592–20,607~~ `0x5074`–`0x507F` = 20,596–20,607, bank 10 rows 116–127 *(corrected 2026-10-02, OPUS: `0x5000 + row` in the shipped `us` augment table; the query-record filler reads it as a bank word, `>> 11` and `& 0x7FF`)* — in the same low-pool
      > scheme that is **group 20, rows 592–607**, a group this page has not yet bound to a file (the
      > `13000 + n` rows are group 13); their `+4` parameters are 0, 0, 0, 40, 30, 20, 30, 20, 10, 10, 10, 10.
      > **(2) Only 116, 117 and 118 are consumed by an immediate mask anywhere in `.text`** — an image-wide
      > scan of every byte / word / dword test on the layer bytes that hold ids 112–127 finds them in one
      > function, `BattleAction_ComputeAuthoredStatusMask` (`003872D0`): when the acting unit carries
      > 116 / 117 / 118 in either layer (`+0x76` / `+0x86` bits 4 / 5 / 6, `00387412`–`003874FE`), it ORs
      > into the action's authored status mask **every status whose `status_data` word `+6` has bit
      > 14 / 12 / 11** (`00387428`, `00387498`, `0038750A`; [the thirty-two statuses](../../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md)) — ~~three "attacks also
      > inflict a status class" augments, parameterless~~ *(wrong: see the answer below)*. Ids 119–127, the ones with the 40 / 30 / 20 / 10
      > parameters, are tested by no immediate mask; their consumers, if any, address the layers
      > through computed bit indices and remain to be found.
- [x] ~~What augments 116–127 are (FX-2).~~ **ANSWERED 2026-09-15 in the register, carried here 2026-09-18 (FABLE):** the licence board names them. The twelve Lore nodes (group `0x1B`, byte `+5` = 16) each grant one of ids `0x74`–`0x7F`: Remedy Lore 3/2/1 = 116/117/118 (parameter 0), Potion Lore 3/2/1 = 119/120/121 (40/30/20), Ether Lore 3/2/1 = 122/123/124 (30/20/10), Phoenix Lore = 125/126/127 (10 each); 116–118 act only for action `0x62` Remedy through `BattleAction_ComputeAuthoredStatusMask`, and their name ids ~~`0x5070`–`0x507F` are low-pool group 20 rows 592–607~~ `0x5074`–`0x507F` are bank 10 rows 116–127 *(corrected 2026-10-02, OPUS: `0x5000 + row` in the shipped augment table; the query-record filler reads word `+2` as a bank word)*. The composition residue above is closed by the same box: nothing composes `13000 + n` into `130000 + n`, the second id is stored in the row.

      **FX-2 ANSWERED 2026-09-15 (FABLE): the twelve are the Lore augments — the licence board names them.**
      Static reading plus authored data; nothing was executed.
      - **The licence board grants exactly these ids.** In the battle pack's licence-node table (directory `+0x34`, 361 × 24)
        the twelve group-`0x1B` nodes with byte `+5` = 16 and these names carry one augment id each in their `+8` word
        list, and the ids are `0x74`–`0x7F`:

        | augment | node | parameter `+4` |
        |---:|---|---:|
        | 116 / 117 / 118 | Remedy Lore 3 / 2 / 1 (nodes 241 / 240 / 239) | 0 / 0 / 0 |
        | 119 / 120 / 121 | Potion Lore 3 / 2 / 1 (nodes 244 / 243 / 242) | 40 / 30 / 20 |
        | 122 / 123 / 124 | Ether Lore 3 / 2 / 1 (nodes 247 / 246 / 245) | 30 / 20 / 10 |
        | 125 / 126 / 127 | Phoenix Lore (nodes 250 / 249 / 248) | 10 / 10 / 10 |

        Each family's first node in bank order grants the highest id. The node names' trailing bytes `0x86`–`0x88` are the
        digits 1–3.
      - **Correction of the 2026-09-12 narrowing above:** 116–118 are not attack augments.
        `BattleAction_ComputeAuthoredStatusMask` takes the augment branch only when the action id is `0x62`
        (`0038738C cmp si, 0x62` / `jne 00387579`), and action row `0x62` is **Remedy** (recipe 34).
        - For Remedy it always gathers every status whose `status_data` word `+6` has bit 10: Blind, Poison, Silence,
          Slow (`003873C0`–`00387410`).
        - Remedy Lore then adds a group:
          - 116: bit 14, Stop, Doom, Disease;
          - 117: bit 12, Petrify, Confuse, Oil;
          - 118: bit 11, Sleep, Sap, Disable, Immobilize.
        - The four bits partition the fifteen statuses 2–16 without overlap, and Reverse (12) carries none of them.
      - ~~**Not traced:** how Potion, Ether and Phoenix Lore's parameters are consumed. No immediate mask tests ids 119–127,
        so their readers index the layers by computed bit.~~ **Corrected the same day.** The readers are recorded on
        [the evaluation context](../../../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) (`+0x28` / `+0x29`),
        which FABLE's scan of the stats-record layer bytes had not covered. Each is the committed step of one item recipe:
        - **Potion Lore, calculator slot 127 `0038DD20`**, the last step of recipe 31 (Potion, Hi-Potion, X-Potion). It sums
          the `+4` parameter of each of 119 / 120 / 121 the source holds (40 / 30 / 20) and scales the heal by
          `(100 + sum) / 100` (`0038DD43`–`0038DE51`).
        - **Ether Lore, slot 128 `0038DF00`**, recipe 32 (Ether, Hi-Ether). It does the same with 122 / 123 / 124
          (30 / 20 / 10) (`0038DF23`–`0038E028`).
        - **Phoenix Lore, slot 130 `0038E2D0`**, recipe 36 (Phoenix Down):
          - it adds the three parameters (10 each) to the action row's percentage byte `+0x10`;
          - it doubles the result when the source's merged layer holds id 14 (context `+0x1B` bit 6);
          - it caps the result at 100;
          - it writes `cap × percent / 100`, at least 1, as the HP gain (`0038E32D`–`0038E46E`).
- [x] ~~Whether the `in` / `kr` / `cn` copies of `battle_pack.bin` carry the same bank layout with a
      different charset.~~ **FX-3 ANSWERED 2026-09-11 (§5.2):** all nine copies carry the same fifteen
      banks with the same counts and byte-identical authored tables; the Latin copies share this
      charset, the `kr` / `cn` / `ch` / `in` copies encode their strings differently.

## 8. Evidence

| claim | how | tier |
|---|---|---|
| slot 45 is bound from the blob's `+0xF8` through the two-level rebase | `00236FCF`–`00236FEA`, `003846F0` read in full | 1 |
| the reference is a 5 : 11 `bank : index` word | `00305F94`–`00305FD8`; the unit-definition page's two sites | 1 |
| bank contents | the `us` section walked in full with the rebase rule; 15 banks, counts as listed | data (`us` only) |
| the action names | all 543 rows' `+0x34` resolve inside bank 0; the Esper block's count and the three known status names are the controls | data |
| the augment descriptions | three rows' descriptions match names the database already had from a tier-6 source | data, correspondence asserted |

## 9. Related

- [`../vbf-archive-and-st2e-tables.md`](../vbf-archive-and-st2e-tables.md) — the string-id files and the charset; its §7 negative about the action table is corrected today.
- [`../../authored-data-table-registry.md`](../../authored-data-table-registry.md) — slot 45.
- [`../../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md`](../../../04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md) — §2.7, the unit-name reader.
- [`../../../10-Status-Periodic-Terminal/where-mp-comes-from.md`](../../../10-Status-Periodic-Terminal/where-mp-comes-from.md) — the augment table behind registry slot 29.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

The section was re-decoded from the shipped `us` copy without reading the prose.

| claim | measured |
|---|---|
| the `us` file | **281,128 bytes** |
| the directory entry at `+0xF8` | file offset **`0x2BBA8`** |
| the section header | a `u16` count of **15**, then **16** (`count + 1`) dword offsets from `+4` |
| the fifteen bank counts | **545 · 544 · 1 · 362 · 63 · 32 · 284 · 16 · 629 · 128 · 129 · 512 · 512 · 16 · 64** — every one, in order |
| "543 / 543 rows have `+0x34 >> 11 == 0` and `& 0x7FF ≤ 542`" | the word runs **0–542** over all 543 rows and is **all-distinct**, so both hold by construction |
| "528 are the identity, 15 are permuted" | the word differs from the row index on **exactly fifteen rows, 128–142**; `543 − 15 = 528` |

### Two bank counts are corroborated by their consumers' own tables

A bank count is only as good as the thing it names, and two of the fifteen can be checked from the
other side:

- **Bank 5 holds 32**, and `status_data.bin` — decoded independently in
  [the thirty-two statuses](../../../10-Status-Periodic-Terminal/the-thirty-two-statuses.md) pass —
  is `st2e` with a count of **32**. The table that supplies the names and the table that supplies the
  ids agree without either page having been written from the other.
- **Bank 10 holds 129**, matching the **129-row augment table** cited by
  [the evaluation context](../../../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md)
  §2.3.

And **bank 0's 545 against 543 action rows** is not a discrepancy: §3's own row shows entries past the
table — `Quickening` at 543 and `SecondJob` at 544 — so `543 + 2 = 545` closes exactly.

### ⚠ The nine-language claim could not be re-tested here

`corpus_validated` states that **all nine** per-language copies carry the same fifteen banks with the
same counts. This working tree holds **one**: only `us/binaryfile/battle_pack.bin` exists — the `in`
directory is present but contains no `battle_pack.bin`, and `de`, `es`, `fr`, `it`, `kr`, `cn` and
`ch` are absent altogether.

> **This is a limit of the pass, not a finding against the page.** One of the nine was re-derived and
> matches in every figure. The other eight are unreachable from here, so the nine-language claim
> stands on its original evidence and is neither confirmed nor challenged by this pass.

**Not claimed:** no string was decoded — the charset, the packed-string walk, the per-bank contents
in §3 and every name attributed to an index were taken as given. §2.1's binder reading was not
re-derived. Nothing was executed or observed live.

## Residual placements — 2026-09-14 (SWE2-FRONTIER, residual-placement package)

| function | size | role (call-signature read) |
|---|---:|---|
| `0023F8B0` | 714 | text-record handler on `[rcx+0xC0]`: `0029FE20`, `00254DD0`, `00393240`, `002F9860`, `0020E620` |
| `002875D0` | 638 | four-iteration cleanup loop on `[rbx+0x60]`/`[rdi+0x18..0x20]`/`[r9+0x28]`: alternating `002F9860` x4/`0020E620` x4, `002AB860` head; callers `002878E0`/`00287C20` |

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

*Tightened word test (R3 clauses 1+2), 2026-09-14 (FABLE):* these crossings were previously matched only through front matter or a link path; tier 2: ledger names, sizes and `edges.tsv`; no body read for this note.

- **CombatFormula — SERVICE.** The unit display-record builder calls `BattleRuntime_GetEffectiveActionId`, and another cited body calls `BattleStats_FindOwningBattleUnit`.
- **CoreRuntimeScheduling — CLIENT and SERVICE.** One cited body is called by `MainLoop_UpdateAndRenderFrame` and two core frame bodies (463 and 2,001 bytes), and another reads a 7-byte core getter.

## Cross-subsystem neighbours — FINAL-AUDIT pass 22

**PlatformOnlineAchievements — SERVICE.** `005760A0` on this page calls `FUN_00315420`, owned by that layer. What it reaches is an 80-byte per-id lookup: ids at or above `0x200` return `-1`, and the rest index `byte[singleton + id + 0x3404]` - the same query the equipment-slot eligibility test recurses into; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Rewards_Progression_Economy — SERVICE.** `00329220` on this page calls `FUN_002f8f20`, owned by that layer. What it reaches is a bounded id mapping: zero returns zero and ids outside `1..0x62` take the out-of-range path; the crossing is that call, not a shared responsibility. Read from the shipping bytes 2026-09-14 (OPUS).

**Save_Load_Settings — CLIENT.** `SaveSlotMetadata_BuildSubmissionDescriptor`, owned by that layer, calls `00254A10` on this page. That caller is the descriptor build, working over a **`0x3C4`-byte** region from `[02CA99B8]` in a `0xA8`-byte frame with a stack cookie; the crossing is that the layer consults this page's function, not that this page owns anything in that layer. Read from the shipping bytes 2026-09-14 (OPUS).

**Input — SERVICE (SWE2-CONTRACT 2026-09-15, 3 edges).** Text-bank bodies `002878E0`/`00287C20` call ~~the input helpers `001E0B90` and~~ a keyboard-layout language selector (French 1, German 2, else 0, from `GetKeyboardLayout`) and the input helper `0017DE60` *(corrected 2026-10-02, OPUS: the first is no input poll, the SWE2-EC7-71 update below)* — the bank playback path consults ~~input state~~ the layout language and input state. 3 edges, named.
- **ActorEntity — CLIENT and SERVICE (7 edges).** 1 inbound (ActorEntity bodies `BattleUnit_ApplyUnitDefinition` (0023A570) call page-cited `002B58B0`); 6 outbound (page-cited `00329220` call ActorEntity bodies `ActorHandle_ResolveRegistryEntryByPackedId` (003588B0), `BattleUnit_GetBySlotIndex` (00236820), `ActorRuntime_GetClassNibble` (00263C20)). Substantive edges include `00329220` calls `ActorRuntime_GetClassNibble` (00263C20); the remaining edges run through shared helpers the page cites.
- **CombatAI — CLIENT and SERVICE (3 edges).** 2 inbound (CombatAI bodies `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880), `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (0030F130) call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `BattleAction_ComputeAuthoredStatusMask` (003872D0)); 1 outbound (page-cited `00236C30` call CombatAI bodies `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880)). Substantive edges include `00236C30` calls `GambitTargetDefinition_BindAndBuildMenuLookup` (00238880); `BattleAction_ComputeAuthoredStatusMask` (003872D0) is called by `AiOrder_BuildCandidateTargetBufferFromStoredRangeAndStatus` (0030F130); the remaining edges run through shared helpers the page cites.
- **CombatAction — CLIENT and SERVICE (4 edges).** 2 inbound (CombatAction bodies `00237FC0`, `BattleAction_ComputeActiveTargetStatusIntersection` (0031C500) call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `BattleAction_ComputeAuthoredStatusMask` (003872D0)); 2 outbound (page-cited `00236C30`, `00329220` call CombatAction bodies `00237FC0`, `003879C0`). Substantive edges include `00236C30` calls `00237FC0`; `00329220` calls `003879C0`; `BattleAction_ComputeAuthoredStatusMask` (003872D0) is called by `BattleAction_ComputeActiveTargetStatusIntersection` (0031C500); the remaining edges run through shared helpers the page cites.
- **Party — MECHANICAL (2 edges).** 2 calls from page-cited bodies into shared Party plumbing (`PartyFocus_GetCurrentPackedActorHandle` (003590D0), `PartyRoster_GetActorBySlot` (00263750)) - the helpers' general call surface, not a Party relationship of this page's subjects.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0034FFC0` call page-cited `00305F10`). Substantive edges include `00305F10` is called by `0034FFC0`.
- **UI — CLIENT and SERVICE (80 edges).** 77 inbound (UI bodies `002C4720`, `00559E30`, `002C38B0` call page-cited `002DD7E0`, `002B58B0`, `00254A10`); 3 outbound (page-cited `002878E0`, `002B41F0`, `002B5390` call UI bodies `002814E0`, `002AF340`, `002B2150`). Read (2026-09-30, SWE2-CONTRACT): `002DD7E0`, `002B58B0` and `00254A10` are UI-wide helpers the page cites, MECHANICAL. The relationship is UI widgets laying out battle text through the page's text entries: `002C38B0`, `005569F0`, `00559E30` and `0055FB20` call `002B3050`, and `00243860` and `002C4720` call the scaled dual-extent measure `0029FE20`. Substantive edges include `002B3050` is called by `002C38B0`; `002B3050` is called by `00559E30`; `0029FE20` is called by `00243860`; `0029FE20` is called by `002C4720`; the remaining edges run through shared helpers the page cites.
- **World — CLIENT and SERVICE (3 edges).** 2 inbound (World bodies `003847B0`, `00238640` call page-cited `AreaData_BindAndRebaseSectionDescriptor` (003845F0)); 1 outbound (page-cited `00236C30` call World bodies `003847B0`). Substantive edges include `00236C30` calls `003847B0`; the remaining edges run through shared helpers the page cites.
- **WorldAreaField — CLIENT and SERVICE (17 edges).** 10 inbound (WorldAreaField bodies `00238850`, `BattleData_SetAreaArdSectionCategory` (0023A160), `00236C30` call page-cited `003846F0`, `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `00228480`); 7 outbound (page-cited `00236C30`, `005369C0`, `00329220` call WorldAreaField bodies `003846F0`, `AreaData_BindAndRebaseSectionDescriptor` (003845F0), `FieldData_GetActiveFieldRecordBit15` (00313F60)). Substantive edges include `00236C30` is called by `00238850`; `00236C30` calls `003846F0`; `0029FE20` is called by `0057FB00`; `003846F0` is called by `BattleData_SetAreaArdSectionCategory` (0023A160); the remaining edges run through shared helpers the page cites.
- **Script_VM_Native_Bridge — CLIENT (1 edge).** 1 inbound (Script_VM_Native_Bridge bodies `0034FFC0` call page-cited `00305F10`). Substantive edges include `00305F10` is called by `0034FFC0`.
## SWE2-EC7-28 update (2026-09-18) — `0029FE20` scaled dual-extent measure

`0029FE20` (138 B) extracts the 10-bit signed field `([rcx+8] << 0x10)
>> 0x16`, resolves `[rcx+0x20]` through `0020E600`, then `002D8B00`
measures into two stack words using `[rcx+0x18]` and the field; both
results come back `* float[+0x28]` truncated and land in `[rdi]` /
`[r14]` — the scaled width/height pair the bank readers fill for the
caller. Interior anchor `0029FE7E` (the first scale).

## SWE2-EC7-29 update (2026-09-18) — `002D8B00` `00364980`-gated dual path

`002D8B00` (172 B) is the `00364980`-gated dual path the text formatters
share: `00364980(r8)` true builds the staged record — `+0` = 1.0f
(`01CEBBA8`), the `arg5` byte at `rsp+0x90` decremented-or-zeroed,
trailing `0` — and calls `003656A0(r8, rdi, rsi, &rec, 0)`; false
forwards `(rbp, r8, rdi, rsi)` to `002B3050`. The split routes the
measure-capable and plain paths behind the same call site. Interior
anchor `002D8B78` (the `call 003656A0`).

## SWE2-EC7-35 update (2026-09-19) - `0023F8B0`

`0023F8B0` (714 B) is a battle-text bank accessor - the `00914C98`/`00914CA0`/`00914CA8` rdata triple, `00393240`/`002F9860`/`0029FE20`/`00254DD0`/`0020E620`. Interior anchor `0023FA8C` (a `00393240` call).

## SWE2-EC7-36 update (2026-09-19) - `002875D0`

`002875D0` (638 B) is a battle-text bank body - `01E0C3F0`, `002F9860`/`0020E620` quadruples plus `002AB860`. Interior anchor `002875F3` (a `002F9860` call).

## SWE2-EC7-43 update (2026-09-19) - `00393240`

`00393240` (290 B) is a battle-text-bank body - `002DD7E0`/`00392F30`/`003932C0`-`00393340` sibling cascade. Interior anchor `00393269` (a `002DD7E0` call).

## SWE2-EC7-46 update (2026-09-19) - `00287C20`

`00287C20` (223 B) is a body - `0017E270`/`001E0B90`/`00285F60`/`00286010`/`002862A0`/`00286500`/`00286780`. Interior anchor `00287C41` (an `0017E270` call).

## SWE2-EC7-52 update (2026-09-19) - `00286500`

`00286500` (626 B) is a `0028[6-8]xxx` bank-family body - `002AB860`/`00285F40`/`002F9860`/`0020E620`/`0029FA40`/`001E0BD0` shared skeleton plus `01E0C3F0`. Interior anchor `00286526` (a `002AB860` call).


## SWE2-EC7-52 update (2026-09-19) - `002862A0`

`002862A0` (608 B) is a `0028[6-8]xxx` bank-family body - `002AB860`/`00285F40`/`002F9860`/`0020E620`/`0029FA40` shared skeleton plus `01E0C3F0`. Interior anchor `002862C9` (a `002AB860` call).


## SWE2-EC7-52 update (2026-09-19) - `00286780`

`00286780` (760 B) is a `0028[6-8]xxx` bank-family body - `002AB860`/`00285F40`/`002F9860`/`0020E620`/`0029FA40`/`001E0BD0`/`001E0DA0` plus `01E0C3F0`. Interior anchor `002867A6` (a `002AB860` call).


## SWE2-EC7-52 update (2026-09-19) - `00286010`

`00286010` (656 B) is a `0028[6-8]xxx` bank-family body - `002AB860`/`00285F40`/`002F9860`/`0020E620`/`0029FA40` shared skeleton plus `01E0C3F0`. Interior anchor `00286035` (a `002AB860` call).


## SWE2-EC7-65 update (2026-09-19) - `0029FA40`

`0029FA40` (134 B) is a bank-family shared-skeleton callee - `0020E600`/`002D8B00`. Interior anchor `0029FA65` (a `0020E600` call).


## SWE2-EC7-68 update (2026-09-19) - `001E0BD0` singleton three-byte forwarder

`001E0BD0` (62 B) is the forwarder the battle-text bank bodies
(`00286010`/`002862A0`/`00286500`/`00286780`) share: `00198790()`
fetches the singleton, then the tail `00197710(obj, sil, dil, bl)`
hands it the caller's three byte arguments (each `movzx`-widened) -
a three-channel write into the profile object. Interior anchor
`001E0BE6` (the `00198790` call).

## SWE2-EC7-69 update (2026-09-19) - `00285F40` bank-context indexed get measured

`00285F40` (21 B) is the null-safe indexed member get the `00286xxx` bank
bodies share: NULL `rcx` returns NULL; otherwise it loads the pointer array
at `[rcx+0x60]` and returns `[array + movsx(edx)*8]` - no bound check, the
caller's index is trusted. Call-free.
Interior anchor `00285F4D` (the `movsxd` index sign-extension).

## SWE2-EC7-71 update (2026-09-19) - `001E0B90` locale selector measured - NOT an input helper

`001E0B90` (58 B) measured - **correction: the page's "input helper"
label is wrong.** The body calls `[008C29B8]` (the keyboard-layout/LCID
IAT), masks `eax & 0xFFF`, and compares: `0x40C` (fr-FR) returns 1,
`0x407` (de-DE) returns 2, everything else returns 0 - a language-index
selector the bank bodies use to pick the localised row, not an input
poll.
Interior anchor `001E0BA5` (the `cmp eax, 0x40c` branch).

## SWE2-EC7-76 update (2026-09-19) - `00285F60` bank-class jump table measured

`00285F60` (88 B) is the class decoder the bank readers call:
`ecx - 2` bounds a ten-entry jump table returning 0..6 (the `00120000`
base-relative table at `+0x165FB8`) - the bank-kind to enum fold.
Interior anchor `00285F81` (the `jmp rcx` dispatch).

## SWE2-EC7-101 update (2026-09-20) - `002AC1E0` measured

`002AC1E0` (153 B) is the `0xD0` record initializer
`002A5460`, `002B3050`, `002B32D0`, `002B3400` and
`002B5390` call: `00861EC0` clears the block, `+0x44`
gains `0x200` (its bit-11 state recomputed), and the
canonical text-record stamps land - `+0x30` colour
`0x80808080`, `+0x9C` size `0x1E`, `+0x34`/`+0x38`/`+0x3C`
scale `1.0`, `+0xA0`/`+0x9A`/`+0xA8`/`+0x9E` bytes
`1`/`0x25`/`0xFF`/`8`, `0039C4A0` resolved into `+0x60`,
`+0xB8` flags `0x30000`, `+0xAE` `0xFF` - the same stamp
family `002B41F0` stages inline.
Interior anchor `002AC1FD` (the flag recompute).

## SWE2-EC7-102 update (2026-09-20) - `002870D0` + `00286D60` + `00286A80` measured

`002870D0` (807 B), `00286D60` (865 B) and
`00286A80` (730 B) are the three nested
counted-list walks `002878E0` and `00287C20` call.
All three open with `002AB860()`, null-safely
resolve the `[rbx + 0x60]` node's `+0x48`/`+0x40`/
`+0x38` variant link, then walk the `[+0x18]` list
root's `[+0x60]`-indexed `+0x18` records under an
outer `+0x50 & 0x3FFFC` count and an inner
`(+0x50 >> 2) & 0xFFFF` element count. Element
`+0x8 & 0x3C == 0x14` runs `00285F40` on the record,
then a `002F9860` row fetch (`00286D60` first gates
on `001E0F00(2)` to pick between two id tables)
publishes the row to `[rbx + 0x18]` and an
`0020E620(0)` value to `[rbx + 0x20]`; element
`== 4` instead clears bit 0 of `+8` on the
`[+0x60]`-linked node, matches `sar [rsi+8], 0x10`
against the 21-dword `01E0C3F0` table to pick
between the two stack arguments, resolves a glyph
index into `[rsi + 0x20]`, runs `001E0BD0` then
`001E0DA0` to publish `word[+0xA]`, and copies the
16-byte `+0x28..+0x37` field from `rsi`/`rbx` into
the node - the id-table variants are
`0x593`/`0x55B`/`0x55D`, `0x55A`/`0x558`/`0x58F`/
`0x555` and `0x559`/`0x55C` respectively. The
banked text-list publish the carrier walks
drive.
Interior anchors `002871F9`, `00286E88` and
`00286B68` (the `00285F40` calls).

## SWE2-EC7-103 update (2026-09-20) - `001E0F00` measured

`001E0F00` (32 B) is the two-call row resolve
`002862A0`, `00286D60`, `002880B0` and `00288A60`
call: `00198790()` supplies the record, then
`00197A40(record, ecx)` answers a byte which is
`movzx`'d into the return - the indexed predicate
the `== 0x14` element arm of the nested-list walks
consults (`00286D60` passes `ecx = 2` to pick
between its two id tables).
Interior anchor `001E0F12` (the `00197A40`
call).

`00289390` (1171 B) is the bank-playback body `002878E0` runs: `002AB860` opens the record, `00228480` early-outs when the state forbids, `[rbx+0x60]` supplies the object, and the `001E0E00` x2/`001E0E30` x6/`001E0D80` x4 input battery drives the playback decisions - the input-coupled half of the text-bank path.

Interior anchor `0028939B` (function `00289390`).

## Homed bodies: functions reached only indirectly whose callees this page cites (OPUS, 2026-10-02, F homing)

*No page cited these functions and none of their callers is documented: they are reached by table or pointer dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and representation, not purpose); the anchors are instructions inside it that do it. Drafted locally and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../../../_index/candidates/opus-battle-text-banks-homing-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00393950` | 83 B | calls `00264150` with the incoming registers and, when it returns non-zero, calls `00393240(W, 1 when r9d is 0 else 0)` where W is the first qword of the array at qword `[rdx+0x10]`; then always stores `r9w` at W's word `+0xA` and byte `+7` of the 8-byte entry `r9d` of the table at W's qword `+0x20` at W's byte `+0x39`, and returns 1 | `0039395A`, `00393960`, `00393977`, `00393987`, `0039399A` |
| `00510E40` | 232 B | keeps `rcx` and `r9`; when `00280120` (incoming registers) returns non-zero it returns at once; otherwise it calls `002640C0`, makes four pointers `002650B0(that result, rcx, 00267E10(r9))` in turn, reads a fifth value `00267E10(r9)` and calls `0055FB20(that value, a local of four words)`, then stores the four words sign-extended as dwords through the pointers in reverse order (word 0 to the fourth pointer, word 3 to the first) | `00510E4E`, `00510E88`, `00510EEA`, `00510EF4`, `00510F18` |
| `0056CF10` | 660 B | when qword `+0xC8` of `rcx` is null it clears bit `0x1` of dword `+8` in the nine objects at qwords `+0` to `+0x40` of the array at qword `[rdx+0x10]` and returns 1; otherwise, for the 32-byte entry `r9d` of that table, it builds a local flags dword (low two bits from dword `+0xE4`; bit `0x4` when bit `0x2` of it is set and the slot index of qword `+0xC0` equals `r9d`), calls `00253690`, derives a value from the flags, the entry and that result (2 or 0 when flag bit `0x2` is set, else 1 or 0) and passes it to `00393240` for the four array elements indexed by the dwords at `00D23608`; then fills the first element's word `+0xA` / byte `+0x39` from the entry's byte `+0xA`, the second element's qword `+0x18` / dword `+0x20` from the entry's first qword and `0020E620(0)`, calls `0029FF60` and `0029FB50` on element `+0x18` and `0056DA80(entry, rdx, &flags, the address 00D23520)`; returns 1 | `0056CF28`, `0056CFA7`, `0056CFCF`, `0056D060`, `0056D103` |
