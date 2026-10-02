---
system: The thirty-two statuses — id, name, help text, default timer, clear-on-apply mask, and what the engine has been read doing with each
category: 10-Status-Periodic-Terminal
status: AUDITED
owner_layer: PrimaryOwner:Status_Periodic_Terminal
evidence_tier: 1
verified_against:
  gzf_sha256: fa0db2933c988211ed4f3c76a7dbe3454fc95866745af4605c35177943d2f708
  transfers_to:
    parent: 59629b9b9a2f482e602f16fd0501c11948606dca4bd9150dbcb7a1137e65cf92
    parent_tag: GN162
    basis: snapshot-identity across GN160 -> GN161 - this document cites none of the 109 functions batch R109 touched, so every per-function record it rests on is byte-identical in both annotation snapshots; CARRIED TO GN162 2026-09-21 (OPUS): the GN161 -> GN162 advance is batch R30 and is MEASURED additive - 30 records changed, comment and tags only, 0 added, 0 removed, 0 immutable-field changes, 0 tag removals, 0 comments rewritten - and this document cites none of the 30
    verified: re-verified 2026-09-21 (OPUS) against the CURRENT certified parent: check_delta_additivity.py GN161 -> PARENT reports ADDITIVE with its control passing, and the two snapshots it read hash to the certified endpoints c16409ec (GN161) and 16a2a832 (GN162). check_transfer_eligible.py returns this document's clause as HOLDS
    adjudicated: OPUS ruling 2026-09-14, _index/PROVENANCE-TRANSFER.md (six ledger figures re-derived)
    previously_transferred_to: 11110a34acf6d0fc9ecd1727945bb3ac7bf582c55170c1c971ebcfdcb8d77500 (GN161), superseded 2026-09-21
  snapshot_sha256: b57264ba73231665bf226da6d5761feee72df36c5999fc68ae14adfdd18fea34
  exe_sha256: 73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8
corpus_validated: "ps2data/image/ff12/test_battle/us/binaryfile/listhelp_status.bin (3,568 B, st2e, 32 string ids 120,000-120,031, ~~33 string offsets from +0xAC of which entries 1-32 are the statuses in id order and 33 is empty~~ 34 u32 offsets from +0xAC, entry 0 not a string, entries 1-32 the statuses in id order and entry 33 empty (corrected 2026-10-02, OPUS, as the evidence table and section 9 count them)) decoded with the battle-text charset; status_data.bin (battle_pack.bin directory +0x40, 32 x 40 B) read for the name reference at +0, the timer units at +9 and the clear mask at +0xC; the 32 names resolved through text bank 5 in id order, 2026-09-11"
last_reviewed: 2026-09-11
audit:
  passes: 1
  last_pass: 2026-09-13
  last_pass_state: opus-thirty-two-statuses-pass-1
  crossref_clean: true
  reopened_count: 0
---

# The thirty-two statuses — id, name, help text, default timer, clear-on-apply mask, and what the engine has been read doing with each

> **One sheet for the number every status page has to translate.** The status words at stats record
> `+0x64` and `+0x3C` are bitmaps over ids 0–31; the name of each id is text bank 5 in id order, its
> definition row is `status_data.bin` (bound at `02EBF118`), and its player-facing description is
> string `120,000 + id` of `listhelp_status.bin`. All three are read here, so a bit named elsewhere
> as "bit 28" can be called Bubble with the help text that says *doubling max HP* beside the
> instruction that doubles it.

**Corpus validation, before anything else.**

| | |
|---|---|
| `listhelp_status.bin` (`us`) | 3,568 B; `st2e`, 32 rows of one `u32` string id (`0x1D4C0` … `0x1D4DF` = 120,000 … 120,031); a second section at `+0xA0` — `{u32 1, u32 0xC, u32 size}` then 34 `u32` offsets from `+0xAC`, entries 1–32 the statuses in id order, entry 0 not a string, entry 33 empty |
| charset | the one [the string-table page](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/vbf-archive-and-st2e-tables.md) §7 decoded: `0x20`–`0x39` → `A`–`Z`, `0x3A`–`0x53` → `a`–`z`, `0x04` space, `0x02` line break; ~~three codes are left undecoded below (`<85>` where a count would print, `<AE>` / `<AF>` around *Requires the proper license*)~~ the three codes are decoded in §3 and §4 `GA-2` (2026-09-15): `<85>` is the digit 0, `<AE>` / `<AF>` are `(` / `)` *(corrected 2026-10-02, OPUS)* |
| `status_data.bin` | 32 rows × 40 B ([the field-record page](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) §*the status definition table*): `+0` the name reference, `+9` the default timer in units, `+0xC` the clear-on-apply mask |
| positive control | row 0's name reference resolves to bank 5 string 0 `KO`, and the help text for id 0 says *lost consciousness … Phoenix Down*; row 31 → `X-Zone`, *vanished without a trace* |
| other languages | `in` 2,440 B, `kr` 3,336 B, `it` 3,508 B — different sizes, not decoded |

## 1. What the player sees

The status list in the menu, in the order the engine numbers them. That order is the bit order of
the status words, so a status's number is a fact about the save file and the battle formulas, not
only about the menu.

## 2. The table

~~Timer units are `status_data.bin` `+9`~~ The beat is `status_data.bin` `+9` and the duration is `+8` *(corrected 2026-10-02, OPUS: `003876D0` reads `+9`, `00387730` reads `+8` at `0038788D` / `0038792C`; §2.1 and the status write §2.4a, 2026-09-12)*; the beat's frame count is `units × DAT_01DFE0B4 × 30`
(`003876D0`). "Clears" is the `+0xC` mask decoded to ids — every set bit is removed with mode 0 when
the status is applied ([the status write](Status-Write/the-status-write-and-its-side-effects.md) §2.6).
"Read" points at where the database has read the engine acting on that id; a blank means no page
has yet.

| id | name | help text (abridged) | timer | clears | read |
|---:|---|---|---:|---|---|
| 0 | KO | lost consciousness, cannot move or act; Phoenix Down | — | 2–6, 8, 10, 12–15, 17–30 | terminal: defeat cleanup and rewards ([status write](Status-Write/the-status-write-and-its-side-effects.md) §2.7); the `0x80000003` gate on the HP write, spawn validation and retirement |
| 1 | Stone | turned to stone; Gold Needle | — | 2, 18–28 | terminal (event `0x200C`); the same gate |
| 2 | Petrify | turning to stone, KO'd when the count reaches …; Gold Needle | 45 | — | unit `+0xE9A` bit 1 when applied by a party record ([status write](Status-Write/the-status-write-and-its-side-effects.md) §2.7); merged-layer id 2 is also the AccuracyBoost augment for the weather accuracy slots ([evaluation context](../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) §2.2) |
| 3 | Stop | frozen in time; Chronos Tear | — | 17 | Stopped or Confused refuses commands ([availability](../07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md)) |
| 4 | Sleep | deep sleep; Prince's Kiss | — | — | event `0x2001` on add and remove (§2.7) |
| 5 | Confuse | cannot tell friend from foe, takes no commands; Nu Khai Sand | — | — | action-control reset with 27 (§2.7); the gambit page's bit 5 |
| 6 | Doom | KO'd when the count reaches …; Remedy (licence) | 100 | — | |
| 7 | Blind | reduced chance to hit; Eye Drops | — | — | |
| 8 | Poison | drains HP for the duration; Antidote | 120 | — | unit `+0xE9A` bit 0 (§2.7); the tick's damage goes through the ordinary apply path ([periodic tick](Periodic-Tick/what-the-periodic-tick-does.md)) |
| 9 | Silence | voice lost, no magicks; Echo Herbs | — | — | merged-layer id 9 gates the unarmed half-formula in calculator slot 72 — the augment sharing the bit is Brawler ([attack-defence](../08-Combat-Formula/Attack-Vs-Defense/attack-defense-preparation-and-stat-scaling.md) §5.1) |
| 10 | Sap | HP drops swiftly; Regen | 1 | 25 | |
| 11 | Oil | vulnerable to fire; Handkerchief | — | — | |
| 12 | Reverse | damage and healing reversed | — | — | |
| 13 | Disable | unable to act; Remedy (licence) | — | — | |
| 14 | Immobilize | cannot move; Remedy (licence) | — | — | |
| 15 | Slow | time slowed; Haste | — | 20 | the builder clears merged id 15 in two forced cases; sign tests in six slots ([evaluation context](../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) §2.2) |
| 16 | Disease | wounds cannot heal; Serum | — | — | HP frozen at `max(old, 1)` — status bit 16 on [the HP write](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2.3; merged id 16 is also Weatherproof |
| 17 | Lure | sole target of foes; temporary | — | — | merged id 17 is also Thievery, the steal's three-roll branch |
| 18 | Protect | physical damage reduced; temporary | — | — | |
| 19 | Shell | magick damage reduced; temporary | — | — | |
| 20 | Haste | time hastened; temporary | — | 15 | |
| 21 | Bravery | physical damage dealt increased; temporary | — | — | |
| 22 | Faith | magick potency increased; temporary | — | — | |
| 23 | Reflect | magicks bounced back; temporary | — | — | |
| 24 | Invisible | cannot be targeted by foes; temporary | — | — | |
| 25 | Regen | HP restored over time; temporary | 15 | 10 | |
| 26 | Float | safe from traps; temporary | — | — | |
| 27 | Berserk | relentless, heightened attack; Dispel | — | — | action-control reset with 5 (§2.7); the gambit page's bit 27 |
| 28 | Bubble | doubling max HP; temporary | — | — | the HP cap doubled while bit 28 is set ([HP write](../08-Combat-Formula/Current-HP/the-hp-write-and-the-lethal-transition.md) §2.3); its removal is the one status transition that applies a result record, halving HP (status write §2.6) |
| 29 | HP Critical | gravely injured but acts normally; restore HP | — | — | |
| 30 | Libra | detailed information about foes; temporary | — | — | |
| 31 | X-Zone | vanished without a trace; cannot be reversed | — | 2–30 | terminal (event `0x200E`); the third member of `0x80000003`; the pages call it "Vanished" after the help text |

*On the body (2026-09-19, FABLE):* what each status bit does to a character's **presentation** is a separate fan-out,
one set arm and one clear arm per bit -
[the rig page](../17-Presentation-Rendering/Character-Render-Records/the-rig-of-seventeen-controllers.md) section 4.
Float, Immobilize and Confuse each own a procedural motion controller; Reverse, Lure, Protect, Shell, Haste, Bravery,
Faith, Reflect, Regen and Libra have empty arms there.

### 2.1 The duration base and the class bit (2026-09-12, FABLE-S26-STATUS-FA)

Two more columns of the row are now read by the engine code on [the status write](Status-Write/the-status-write-and-its-side-effects.md)
§2.4a. **`+8` is the base duration** — the default dword is `+8 × Vitality factor × [01DFE0B4] × 300`
and the periodic tick spends 10 of it per tick, so `+8` is seconds if the tick is per-frame, as
[the periodic tick page](Periodic-Tick/what-the-periodic-tick-does.md) reads it; `0xFF` means
the status has no duration and lasts until something removes it. **Bit 13 of the word at `+6` is
the harmful class**: Vitality *shortens* those (`2·base − base·Vit/100`) and *lengthens* the rest
(`base + base·Vit/100`, and ×1.5 under effect id 30). The `+9` column above is not a duration at
all but the **beat** — how often Poison, Sap and Regen land and how often the Petrify / Doom count
steps — which is why it is blank on every status that has no periodic effect.

| id | name | `+8` base | class | id | name | `+8` base | class |
|---:|---|---:|---|---:|---|---:|---|
| 0 | KO | — | harmful | 16 | Disease | — | harmful |
| 1 | Stone | — | harmful | 17 | Lure | 20 | beneficial |
| 2 | Petrify | — (count ~~10~~ 11 stored, shown as 10 *(corrected 2026-10-02, OPUS: `00387740`–`00387759`)*) | harmful | 18 | Protect | 72 | beneficial |
| 3 | Stop | 30 | harmful | 19 | Shell | 72 | beneficial |
| 4 | Sleep | 25 | harmful | 20 | Haste | 40 | beneficial |
| 5 | Confuse | 40 | harmful | 21 | Bravery | 40 | beneficial |
| 6 | Doom | — (count ~~10~~ 11 stored, shown as 10 *(corrected 2026-10-02, OPUS: `00387740`–`00387759`)*) | harmful | 22 | Faith | 50 | beneficial |
| 7 | Blind | — | harmful | 23 | Reflect | 60 | beneficial |
| 8 | Poison | 50 | harmful | 24 | Invisible | 90 | beneficial |
| 9 | Silence | — | harmful | 25 | Regen | 100 | beneficial |
| 10 | Sap | — | harmful | 26 | Float | 60 | beneficial |
| 11 | Oil | — | harmful | 27 | Berserk | 45 | beneficial |
| 12 | Reverse | 15 | harmful | 28 | Bubble | 60 | beneficial |
| 13 | Disable | 20 | harmful | 29 | HP Critical | — | harmful |
| 14 | Immobilize | 50 | harmful | 30 | Libra | 240 | beneficial |
| 15 | Slow | 60 | harmful | 31 | X-Zone | — | harmful |

"Harmful" and "beneficial" are this page's names for the two values of the bit; the engine only
knows which way Vitality pushes the duration. Blind, Silence, Sap, Oil and Disease carry no
duration in the shipped table — they persist until cured — and Berserk is in the class Vitality
lengthens.

**Two things the merged layers imply.** ~~`BattleFormula_BuildEvaluationContext` ORs the status layer
and the augment layer into one bitmap per id (`00384820`–`00384858`), so a calculator that tests
merged id 9 cannot tell Silence from Brawler, nor id 16 Disease from Weatherproof, nor id 17 Lure
from Thievery. Slot 72's half-formula is therefore reachable by a **Silenced** unarmed attacker as
well as by one with Brawler — a consequence of the merge as read, not observed.~~ `BattleFormula_BuildEvaluationContext` ORs the two effect-id layers `+0x68` / `+0x78` into one bitmap (`00384820`–`00384858`). The 32 statuses are in neither layer: they are the status words, copied to context `+4` / `+8`, so a merged-id test does not see Silence, Disease or Lure, and this merge does not open slot 72's half-formula to a Silenced attacker *(corrected 2026-10-02, OPUS: checked at `003847C0`; two-layer-effect-model.md §5, clarified 2026-09-29)*.

## 3. Modding notes

- **A status's number is its bit** in `+0x64` / `+0x3C`, its row in `status_data.bin`, its string in
  bank 5 and its help text at `120,000 + id`; all four must move together.
- **The clear masks are where mutual exclusion lives** — Slow ↔ Haste, Sap ↔ Regen, and the wide
  masks on KO / Stone / X-Zone — not in the code that applies a status.
- ~~**The timers are in `status_data.bin` `+9`**~~ **The beats are in `status_data.bin` `+9`** (the durations are `+8`, §2.1) *(corrected 2026-10-02, OPUS: `003876D0` reads `+9`, `00387730` reads `+8`)*, in units the engine scales by `DAT_01DFE0B4 × 30`;
  only Petrify (45), Doom (100), Poison (120), Sap (1) and Regen (15) ship one.
- ~~The help text's `<85>` is where the Petrify / Doom count prints;~~ The help text's `<85>` is the **digit 0**, so the
  sentence reads *…KO'd when the count reaches 0*, not a placeholder (corrected 2026-09-15). The `<AE>` … `<AF>` pair is
  **`(` … `)`** around *Requires the proper license*.

## 4. What is not known

- [x] **GA-1 ANSWERED 2026-09-27 (FABLE, Claude Opus 5.5).** The last open bytes:
      - `+0x11`, `+0x12` and `+0x14`–`+0x1D` are read by no code; they are authored and unread.
      - `+0x08` becomes the running timer through the default-duration computation (stats field map, `+0x0BC`).
      - The five order keys feed the party panel, a HUD panel, the target-info window and the overhead icon; `+0x02`
        feeds no list.
      - `+0x0A` is a text id.
      [Record](../_index/candidates/ga1-status-open-bytes/README.md). *Earlier state, kept:* The rest of the
      `status_data.bin` row. **Four of the asked bytes are now read from the
      shipped table (2026-09-15, OPUS); twenty-one are not, so this stays open.** The file is 32 rows of
      40 bytes behind the standard `st2e` header, and it is **byte-identical in all four copies** — it
      ships only for `kr`, `in`, `cn` and `ch`, with no `us` copy in the archive.
      *Row join confirmed before anything was read off it:* `+0x00` is the row index in all 32 rows and
      the rows line up with the 32 status names in `word.bin` bank 5. **This page's own two examples
      then fall out of the data unprompted** — `+0x02` is 29 at Stone and 0 at Libra, exactly as stated
      above — and the four rows carrying `0xFF` at `+0x02` are exactly KO, Invisible, HP Critical and
      X-Zone, again exactly as stated. That is three independent confirmations that the join is right.
      - ~~**`+0x01` is the stride itself**, `0x28` = 40, in all 32 rows.~~ **Corrected 2026-09-15 (FABLE):** `+0x00`–`+0x01`
        is one `u16`, the name word `0x2800 + id`. Bank `word >> 11` = 5 is the status names; entry `word & 0x7FF` = the id.
        The high byte `0x28` is `5 << 3`, and its equality with the 40-byte stride is a coincidence. This is the
        "`+0` the name reference" of the table above.
      - **`+0x03`, `+0x04`, `+0x05` are zero** in all 32 rows.
      - **`+0x02`, `+0x10`, `+0x26` and `+0x27` are one small index space, `0x00`–`0x1F`, and it is not
        the row id.** It is ordered **buffs first then debuffs**: Libra `0x00`, Bubble `0x01`, Berserk
        `0x02`, Float `0x03`, Regen `0x04`, Invisible `0x05`, Faith `0x06`, Bravery `0x07`, Haste
        `0x08`, Shell `0x09`, Protect `0x0A`, Reflect `0x0B` — a contiguous run — then Lure `0x0C`,
        HP Critical `0x0D`, Sap `0x0F` … KO `0x1E`, X-Zone `0x1F`. `0x0E` and `0x11` are unused, and two
        pairs share a value: Silence/Immobilize both `0x14`, Reverse/Disease both `0x17`.
      - **`+0x10` carries that index in all 32 rows**; `+0x02` repeats it except in the four rows above,
        where it is `0xFF`; `+0x27` repeats it except HP Critical, where it is `0xFF`.
      - **The tail `+0x11`–`+0x1F`, narrowed 2026-09-15 (FABLE): two bytes closed, and the rest obey
        one law. No meaning is claimed — this is the shape, and it is offered so any future reading has
        something to fail against.**
        - **`+0x1E` and `+0x1F` are `0xFF` in all 32 rows.** The open range is `+0x11`–`+0x1D`.
        - **`+0x13` is ~~the row's own index~~** *(corrected 2026-09-26 (FABLE, Claude Opus 5.5): it is not the row id but the
          display index, below)* — the same `0x00`–`0x1F` space as `+0x02` / `+0x10` /
          `+0x26` / `+0x27`. It equals `+0x10` in the 28 rows that carry it and is `0xFF` in exactly
          four: ~~KO, Invisible, HP Critical and X-Zone~~ **KO, Stone, HP Critical and X-Zone** *(corrected 2026-09-26
          (FABLE, Claude Opus 5.5), from the table ASTRA retained: Stone is `0xFF` at `+0x13` and Invisible carries `05`; the
          KO / Invisible / HP Critical / X-Zone set is `+0x02`'s)*. It reproduces the two shared values
          (Silence/Immobilize, Reverse/Disease) that the index space already has. *(The sentence that followed called
          this a fourth independent confirmation of the row join. It rested on reading the `+0x13` and `+0x02` sets
          as one set, and is withdrawn. The join stands on the name key at `+0x00`.)*
        - **The other twelve columns obey a single law.** For each column *c* in `+0x11`, `+0x12`,
          `+0x14`–`+0x1D`, let *n* be the number of rows whose byte at *c* is not `0xFF`. Then the
          values in that column are **exactly `{32 − n, …, 31}`, each value appearing exactly once**.
          Measured across all twelve, with no exception:
      ***NARROWED 2026-09-18 (FABLE), DATA: four of the read-but-uninterpreted fields named from their values.** The dataflow pass above reaches `+0x08`, `+0x09`, `+0x0C` and (through a word read) `+0x0A` without saying what they hold; the shipped rows say it. *`+0x08` is the default duration in seconds, 255 for no timer:* Stop 30, Sleep 25, Confuse 40, Poison 50, Reverse 15, Disable 20, Immobilize 50, Slow 60, Lure 20, Protect 72, Shell 72, Haste 40, Bravery 40, Faith 50, Reflect 60, Invisible 90, Regen 100, Float 60, Berserk 45, Bubble 60, Libra 240; KO, Stone, Petrify, Doom, Blind, Silence, Sap, Oil, Disease, HP Critical and X-Zone carry 255. *`+0x09` is a second timing parameter carried by exactly the five periodic or countdown statuses:* Petrify 45, Doom 100, Poison 120, Sap 1, Regen 15, zero elsewhere. *`+0x0A`..`+0x0B` is the word `0x2EE0 + id`* (`+0x0A` = `0xE0 + id` in every row, `+0x0B` = `0x2E` constant), read as a word at ~~`0031C81A`~~ **`0031E288`** in `0031C5D0`; ~~it is not a string-pool key (12000..12031 in the pool are the clan ranks and `Select Leader`), so it is a per-status index in a second space, 224..255, whose consumer is the residue~~ **it is a banked string-pool key, and its consumer is traced — both corrections below.**

      ***Both halves of that sentence were wrong, and the correction is OPUS's — amended 2026-09-21 (FABLE) on
      `OPUS-REQ-FABLE-STATUS-0X0A-READER-SITE-AND-POOL-KEY-CORRECTION`. The values above are unaffected; only the
      reader attribution and the negative conclusion were.*** Both points re-measured from the image here.

      - **Wrong instruction, right function.** `0031C81A` reads `[rbp + 0x0A]` where `rbp` is a resolver return built
        from the **`02EBF100`** registry slot (`0031C7A3`–`0031C803`), not `02EBF118`. That table's records carry
        their name word at `+0x08`, packed — `0031C7B7` takes it and shifts right by 11, `0031C7F5` takes it and masks
        with `0x7FF` — whereas a status row's name word is at `+0x00`. **Different record type, so `0031C81A` was
        never reading this field.** The real site is `0031E288`, where `0031E268`–`0031E286` builds the pointer from
        `[02EBF118] + 0x0C` resolved, plus `[rbx + 4]` times the header stride at `+0x08`.
      - **It is a string-pool key after all, in a banked pool I had not sampled.** `0031E28C` passes the word straight
        into `002F9860` and stores the returned **pointer** at the applied record's `+0x10`. `002F9860` divides the key
        by 1000 (`imul` by `0x10624DD3`, `sar 6`), returns the empty sentinel `01CEB638` for a bank at or above `0x1C`,
        takes `entry = key − bank × 1000`, and looks the bank up in a 28-entry table at `02EC3D80` with a per-bank
        table at `02F973C0`, bound-checking `entry` against that bank's count at `+0x04`. So `0x2EE0 + id` is
        **bank 12, entry = the status id** — and the `12000..12031 are clan ranks` observation was about a *flat* pool,
        not this one. The negative it supported is withdrawn.
      - **What is now open instead, and it is narrower.** Bank 12's slot `02EC3DE0` is written by exactly one body in
        the image, `002F7800`, which hard-codes the bank number `0xC` and tail-jumps to `00238640`, which hands
        `&02F973C0[12]` on to a single loader entry — named by role, not by address, because that body's own callers
        cross into a layer this page does not discuss. `002F7800` has **no direct call site and no aligned qword pointer to it**
        anywhere in the image — an RVA jump-table route is not excluded. So *what bank 12 holds* is a loader and data
        question, not an executable one. `GE-1`.
        ***GE-1 resolved 2026-09-24 (SWE2-CONTRACT), static + shipped data.*** The missing dispatch is a bank-index
        switch, not a call edge: `002F7800` is one of ~~**27 sibling stubs** (`002F7680`–`002F79C0`, `0x20` stride,
        one per bank 1–27~~ **28 case bodies** (`002F7660`–`002F79C0`, one per bank `0..0x1B`: case 0 → `002F7660`, case 4 → `002F7680`, … *(corrected 2026-10-02, OPUS: checked at `002FA560`, as pass 22 below reads it)* — the "MMSG value receiver adapters" census already catalogued) reached through
        **`002FA560(bank)`**, a linear `cmp ecx, K; lea rdx,[stubK]; jmp 002385D0` switch. `002385D0` bounds-checks
        the bank (`≤ 0x1B`), maps it through the per-bank group byte table `01E09F68` (bank 12 → **`0x31` = 49**),
        and issues `00384420(group, rdx = stub, r8 = "MMSG", r9 = 3, stack: 4, 8)` — a resource request whose
        completion calls the stub back with the delivered ref, which is what `002F7800` stores into `02EC3DE0`
        and binds into `02F973C0[12]` via `00238640` → `003845F0`. So bank 12 is the **`MMSG` resource of
        resource kind 2, id 49** — and the shipped manifest resolves it by itself:
        `FileSizeTable_US.fst[2][49]` = **3568 bytes**, which is byte-for-byte
        `test_battle/us/binaryfile/listhelp_status.bin`. That file is an `st2e` carrier of exactly **32 rows**,
        `0x1D4C0 + n` (= `120000 + n`, the matching high-pool ids), followed by an offset table over an encoded
        help-string heap. So **bank 12 holds the status help-text block** — `+0x0A`'s `0x2EE0 + id` resolves to
        the description shown for status `id`, consistent with `+0x00`'s `0x2800 + id` being the name from bank 5.
        Caveat for the record: the encoded-id page's "bank 12 is the Key Items tab" is a **different bank
        namespace** (the packed `name-word` banks — "status names are bank 5" there), not this
        `002F9860`/`02F973C0` pool — same number 12, different table; flagged rather than silently reconciled.
        Residual: the group→path naming rests on the `.fst` size match plus the file's self-declared row shape
        (`002DF9A0`'s path arrays are runtime-installed); `0053EC75`/`0053EC8B` request banks 25/26 at init and
        `0024877E` requests `[obj+0xC8]` on demand, so bank 12's bind timing is "when the status screen needs it".
      - **A shape worth recording while the site is open.** The record pointer for this read is formed in **32-bit**
        arithmetic over a 64-bit resolver return: `0031E27E`–`0031E286` is `movzx esi` / `imul esi` / `add esi, eax`,
        so `rsi` is the zero-extended low 32 bits of `stride × index + resolved base`. The sibling build at
        `0031C7B5` does the same. That is correct only while the resolved base is below 4 GiB — the same truncation
        shape `EO-3` tracks on the resource queue, on a different table. Nothing here observes it going wrong, and no
        defect is claimed. `GE-2`.
      - **And the read is not guarded by its own build.** `0031E259` and `0031E266` both branch to `0031E288` — the
        read itself — when the registry slot is null or the resolve fails, so on those paths `[rsi + 0x0A]` is taken
        through whatever `rsi` already held. `GE-3`. *`+0x0C`..`+0x0F` is a 32-bit status mask, the statuses this one removes:* KO `0x7FFEF57C` (everything but Stone, Doom, Reverse, Lure and X-Zone), Stone `0x1FFC0004` (Petrify and the eleven buffs Protect..Bubble), X-Zone `0x7FFFFFFC` (everything but KO and Stone), and four mutual pairs, Haste `0x8000` (Slow) and Slow `0x100000` (Haste), Sap `0x2000000` (Regen) and Regen `0x400` (Sap), plus Stop `0x20000` (Lure); the other 24 rows are zero. *Also from the rows:* `+0x06`..`+0x07` is a flag word with ~~`0x0020` on every buff~~ `0x0020` (bit 5) on exactly fourteen rows — Stop, Sleep, Confuse, Lure, Protect, Shell, Haste, Bravery, Faith, Reflect, Invisible, Regen, Float and Bubble — and not on Berserk (`0x0040`) or Libra (`0x0100`) *(corrected 2026-10-02, OPUS: checked against `status_data.bin`; CONTRACT-status-write.md §4, invariant 3)*, `0xA000` and above on the debuffs (`0xA0DF` on KO and Stone, `0x21DF` on X-Zone, `0x2000` on HP Critical), and `+0x21`, `+0x22`, `+0x25` are zero except `+0x22` = 1 on Bubble. Which reader turns `+0x08` into the running timer (the candidates are the two `ComputeDefault*` bodies the pass tagged) and what consumes the `+0x0A` index are what remains. DATA from `status_data.bin` (the four copies are identical) joined to bank 5's names.*
      - ***GE-3 and GE-2 resolved 2026-09-23 (SWE2-CONTRACT), static.*** `rsi` is not "whatever it already held" — it is
        the function's null constant. `0031C5D0`'s prologue clears it at `0031C5EC` (`xor esi, esi`) and no dispatch
        path writes it before an arm runs: the only `mov rsi, rax` sites (`0031C6FF`, `0031C808`) sit on other arms'
        success paths that exit through the epilogue, and the class-1 arm's re-dispatch (`0031C632`–`0031C639`) never
        touches it — every `cmp qword [rip+d], rsi` in the filler is a null test against zero. So on the
        `0031E259`/`0031E266` fail paths `0031E288` reads **`word [0x0A]` — the null page, a guaranteed fault, not a
        graceful fallback**. The arm has no missing-slot path at all; it trusts the descriptor. Reachability is the
        install window and only the install window: `02EBF118` is written by `003847B0`, a three-instruction shim
        (`movsxd rdx, ecx` / `lea rcx, [02EBF118]` at `003847B3` / `jmp 003845F0`) that resolves the master record's
        `+0x40` field into the slot through the shared installer `003845F0` — the same mechanism the class-13 slots
        use. Once it runs, `desc+0x0C` is a shipped non-zero offset and `0020E600` cannot return zero, so both fail
        branches are dead code in normal play; a class-26 query issued before install faults on `[0x0A]` rather than
        mis-resolving. **`GE-2`: it can truncate, in exactly one window.** `rsi = u32(low32(rowbase) + stride × idx)`;
        the carry out of `add esi, eax` is dropped, so truncation needs `low32(rowbase) + 40 × idx ≥ 2³²` — with the
        shipped stride 40 and 32 rows, a resolved base in the top ~1.2 KiB under 4 GiB, or above it. The sibling
        `0031C7B5` build has the same shape on its own descriptor. Whether the arena ever lands there is the `J-C`
        live read of `01F83530` — the design assumes sub-4 GiB backing (the arena's own links are 32-bit, FABLE's
        `CD-2`/`J-C` static finding), so the truncation window is a configuration the rest of the arena cannot
        address either. Nothing shipped observes it; no defect claimed.

          | column | `+0x11` | `+0x12` | `+0x14` | `+0x15` | `+0x16` | `+0x17` | `+0x18` | `+0x19` | `+0x1A` | `+0x1B` | `+0x1C` | `+0x1D` |
          |---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
          | *n* | 5 | 1 | 4 | 3 | 4 | 7 | 3 | 4 | 5 | 1 | 3 | 2 |
          | values | 27–31 | 31 | 28–31 | 29–31 | 28–31 | 25–31 | 29–31 | 28–31 | 27–31 | 31 | 29–31 | 30–31 |

        - **What the law rules out, which is the useful part.** The values are **not** free-form and
          they are **not** an ordinary index list: a column never holds an arbitrary status, only the
          top *n* of the index space, and never twice. So a reading of these bytes as "a list of
          statuses this one interacts with" has to explain why every column is a *prefix from the top*
          with no repeats — and none of the obvious readings does.
        - **No consumer is traced, and none is claimed to be absent — but the negative is now
          population-wide rather than anecdotal.** A whole-image displacement scan for `0x11`–`0x1D`
          returns **24,730** sites and is useless at this offset range, so the search has to start
          from the table. Every body with a rip-relative read of the registry slot `02EBF118` —
          **eighteen bodies that reach the table through the registry slot** — was decoded, tagging
          the register that receives the pointer and every register derived from it (including
          `lea`-formed row pointers), and **eight** displacements are reached in total:
          `−1`, `+0x00`, `+0x04`, `+0x06`, `+0x08`, `+0x09`, `+0x0C` and `+0x20`. **None of them is in
          `+0x11`–`+0x1D`.** The one `[rsi + 0x1b]` in `00387CB0` is not a counter-example: it is on a
          different record, guarded by `cmp word ptr [rsi], 0x59`, which a status row can never
          satisfy because its `+0` is the name word `0x2800 + id`.
        - **Why that is still not a closure, from this page's own evidence.** §below records that the
          encoded-id query-record filler copies **`+0x13`** into record `+0x23` — and `+0x13` is **not**
          in the eight displacements above. So at least one real reader of a row field reaches rows by
          a route this census does not see, which is exactly the tracker's known limit: it is local to
          one body, so a callee handed a row pointer as an *argument* is invisible to it. **The
          eighteen-body result bounds where a consumer is not~~, it does not prove there is none~~.** *(answered: see GA-1 at the top of §4 — the later census of 44 status rows across the 18 users of the slot finds no reader of `+0x11`, `+0x12`, `+0x14`–`+0x1D`; 2026-10-02, OPUS)*
        - *Also confirmed while reading:* the header is the standard **`st2e`** container — magic
          `st2e`, count `32`, stride `40`, header size `32`, and the `+0x18` / `+0x1C` trailing-byte
          declarations that `AY-11` established are both zero here. All four copies are byte-identical.
      - **`+0x26` is `0xFF` in exactly 12 rows** — Protect, Shell, Haste, Bravery, Faith, Invisible,
        Regen, Float, Berserk, Bubble, Libra and HP Critical — and carries the index in the other 20.
        *Not claimed:* that this is the beneficial/harmful split. It nearly is, but **Reflect is a
        beneficial status and carries the index, not `0xFF`**, so a one-line reading of `+0x26` as
        “is a buff” is refuted by the data and is not offered.
      ~~**Still open: `+0x11` … `+0x25`**, twenty-one bytes per row.~~ *(answered: see GA-1 at the top of §4 — `+0x11`, `+0x12` and `+0x14`–`+0x1D` are read by no code, and the narrowings below decode the rest; 2026-10-02, OPUS)* They are mostly `0xFF` with a
      scattering of small values in the same `0x00`–`0x1F` space, which looks like a per-status list of
      other statuses, but nothing here reads a consumer and no reader has been traced. `GA-1`.
      *Narrowed 2026-09-15 (FABLE): six more of those bytes are decoded; `+0x11`–`+0x1F` stay open.* Evidence is the
      `us` `battle_pack.bin` `+0x40` section, which the four `status_data.bin` copies equal, plus the readers.
      - **`+0x20`–`+0x23` is a `u32` status mask: the statuses that block this one from being added.**
        - The candidate-status applier behind calculator slots 181 / 182 (`00387CB0`) walks the action's
          candidate statuses. For each status *s* it loads row *s* and tests `+0x20` against
          [evaluation context](../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) `+0x08`, the
          target's current statuses (`00387E5D`–`00387E63`). A shared bit skips the add.
        - `003908A0` makes the same test for its Protect / Shell add (`003909DC`), and calculator slot 118
          (`0038FCE0`) makes it before OR-ing into the result (`0038FE0D`).
        - The shipped masks read exactly that way. Every row has `0x80000003`: a target in KO, Stone or X-Zone takes
          no new status.
        - Beyond that, only seven rows add bits, as three mutual pairs and one single block:
          - Petrify is blocked by Doom (`0x40`) and Doom by Petrify (`0x04`);
          - Confuse by Berserk (`0x08000000`) and Berserk by Confuse (`0x20`);
          - Disease by Bubble (`0x10000000`) and Bubble by Disease (`0x00010000`);
          - Lure by Stop (`0x08`).
        - *Corroborated 2026-09-17 (OPUS, `OPUS-CORROBORATE-FABLE-GA1-BLOCK-MASK`, from the bytes): read as a 32-bit mask over the 32 status ids, every row carries three or four bits and none is zero, and only three rows, KO, Stone and X-Zone, carry their own bit; so `+0x20` is the set of incapacitating states that make any add impossible (KO, Stone, HP Critical and X-Zone all carry `0x80000003`; Petrify adds Doom, a pending death), not a self-exclusion flag.*
      - **`+0x24` is a flag byte:** `0x01` on KO, Stone and X-Zone; `0x08` on Poison; `0x02` on Bubble;
        `0x04` on HP Critical; 0 on the other 26 rows. ~~reader not traced~~ *Corrected the same day:* the status arm of
        the encoded-id query-record filler reads it.
        - The filler copies its four low bits into bits 1–4 of the record's `+0x25`; bit 0
          comes from `+0x06` bit 13.
        - The same arm copies `+0x10`, `+0x26`, `+0x27` and **`+0x13`** into record `+0x20`–`+0x23`, and `+0x02` into
          `+0x24`.
        - So `+0x13` has a reader too, though what its value selects is not read here. The query-record fields
          themselves are on [the encoded-id space page](../00-Engine-Core-Runtime/the-encoded-id-space-and-the-query-record.md).
        - **What the five copied bytes select — NARROWED 2026-09-26 (FABLE, Claude Opus 5.5): they are order keys for five status
          listings, and `0xFF` leaves a status out of a listing.** Every one is the same master order, `+0x10`'s:
          buffs first (Libra, Bubble, Berserk, Float, Regen, Invisible, Faith, Bravery, Haste, Shell, Protect,
          Reflect), then Lure and HP Critical, then the debuffs down to Petrify, Stone, KO and X-Zone. Where a byte is
          not `0xFF` it equals `+0x10`, so each byte differs from `+0x10` only in which statuses it omits:

          | row byte | record | omitted (`0xFF`) | read by |
          |---|---|---|---|
          | `+0x10` | `+0x20` | none | the per-unit list builder, over a unit's status mask (listing 0) |
          | `+0x26` | `+0x21` | 12: Protect, Shell, Haste, Bravery, Faith, Invisible, Regen, Float, Berserk, Bubble, Libra, HP Critical | cached ordering 1; the counter's default kind |
          | `+0x27` | `+0x22` | HP Critical | cached ordering 2; the counter's kind 2, with a per-unit test |
          | `+0x13` | `+0x23` | KO, Stone, HP Critical, X-Zone | cached ordering 3 (the unit status view's slot lookup scans it); the counter's kind 1 |
          | `+0x02` | `+0x24` | KO, Invisible, HP Critical, X-Zone | cached ordering 4; the counter's kind 3; **the battle reaction queue** |

          - **The list builder** takes a status mask and a kind 0–4. It emits `{status id, key, record +0x25 bit 0}`
            for each status in the mask, keyed by record `+0x20 + kind`, and counts the keys that are not `0xFF`.
            A shared sort then orders the entries by the key as a **signed** byte, so omitted statuses sort first.
          - **The four cached orderings.** A lazily built UI cache holds all 32 status query records and one sorted
            32-entry pointer table per kind 1–4. The unit status view and the widget layer read them.
          - **The counter** returns how many statuses of a mask a given listing would show. It selects the key by
            kind: 1 → record `+0x23`, 2 → `+0x22`, 3 → `+0x24`, anything else → `+0x21`.
          - **The battle reaction queue** (`BattlePresentation_EnqueueReactionWithRandomizedVariant`) refuses a status
            reaction and returns `0xFF` when the status's `+0x02` is `0xFF`. **So KO, Invisible, HP Critical and
            X-Zone never queue a status reaction through it**; every other status can.

          *Limits:*
          - which on-screen list each kind is (the listing names above are the readers', not screens);
          - which readers of the cached orderings run in which menu;
          - `+0x11`–`+0x1D`, which none of these readers touch, ~~stay open~~ are read by no code *(answered: see GA-1 at the top of §4; 2026-10-02, OPUS)*.

          Static, from the image and the retained table. The code addresses are in the control, [`ga1_status_order_keys.py`](../_index/candidates/ga1-status-order-keys/ga1_status_order_keys.py)
          (7 checks, FAILS 0). Its sensitivity check shows the old `+0x13` reading fails against the table.
      - **`+0x25` is 0** in all 32 rows.
  **NARROWED FURTHER 2026-09-27 (OPUS). Two of the three open clauses move and the third is bounded. (1) The reader that turns +0x08 into the running timer is already on record: BattleStatus_ComputeDefaultDwordParameter (00387730, FA-1, answered 2026-09-12) scales row +0x08 by the target's Vitality, x [01DFE0B4] x 300, 0 when 0xFF; this row had not taken it. (2) The query arm reads three more row fields. The +0x0A word goes through 002F9860 into record +0x10. 002F9860 is a text resolver: bank = id / 1000 (fewer than 28 banks), entry = the remainder, the empty string otherwise. So +0x0A is the status's text id. The +0x06 bit 13 and the +0x24 bits 0-3 are packed into record +0x25 bits 0 and 1-4. (3) +0x11, +0x12 and +0x14..+0x1D are twelve sparse ranking columns. Each is 0xFF in most rows and otherwise one of 25..31, distinct and counting down from 31, never equal to +0x10, so they are NOT the listing-key family. +0x1E / +0x1F are 0xFF in every row. No reader: 44 status rows formed across the 18 users of the class-26 slot 02EBF118, receiver-typed and followed through unconditional jumps, read no byte of the band. The positive control finds the arm's +0x13 / +0x26 / +0x27 reads. The arm copies only the five keys into its record. ~~Still open: what the twelve rankings rank, a reader that resolves class 26 without naming the slot, and~~ *(answered: see GA-1 at the top of §4, 2026-09-27 — the band is read by no code, authored and unread; 2026-10-02, OPUS)* Still open: which on-screen list each key kind drives. Control _index/candidates/ga1-row-band/ga1_row_band.py (B1-B4, FAILS 0).**
- [x] **GA-2.** The three undecoded help-text codes (`<85>`, `<AE>`, `<AF>`) and whether the other language
      copies carry the same 32 entries. `GA-2`.
      *Codes decoded 2026-09-15 (FABLE); the language-copy half is answered below.* All 3837 strings in the `us` battle pack's
      15 text banks were read (`work/FABLE/drift4/ga2_byte_contexts.py`), and the bytes are ordinary characters:
      - `0x85`–`0x8E` are the digits `0`–`9`: `1000 Needles`, `Heavy Armor 10`, `Lv.3 Disable`, `+30 HP` (`0x85`
        201 times in 149 strings).
      - `0xAE` / `0xAF` are `(` / `)`: 17 pairs, e.g. `Sword (1H)`, `Katana (2H)`.
      - The same census gives `0xA4` `+` (`+30 HP`, 26 occurrences) and `0xA6` `=` (`Foe: status = Petrify`, 88).
      - ~~Only the `us` copy of `listhelp_status.bin` is in the local extract, so whether the other copies carry the same
        32 entries is not checked (routed with AY-8's CJK request).~~ **Wrong, corrected the same day:** the search
        covered only the repository's work tree. The full game extract `D:/FFXII_TZA_extract` has all nine copies.
      **ANSWERED 2026-09-15 (FABLE): all nine language copies carry the same 32 entries**
      (`work/FABLE/drift4/ga2_language_copies.py`, reading `test_battle/<lang>/binaryfile/listhelp_status.bin`):
      - **The same records in every copy.** `us`, `de`, `es`, `fr`, `it`, `in`, `kr`, `cn` and `ch` each have 32
        records of 4 bytes with the same string ids, `120000`–`120031` in row order. Each has a text heap of
        `count` 32, and none of the 288 strings is empty.
      - **Only the text differs**: file sizes run from 2,304 B (`ch`) to 4,108 B (`es`).
      - **The Latin copies confirm the digit reading.** `de` and `es` also put `0x85` in the Petrify and Doom entries
        (2, 6), decoding as *auf 0 steht* and *llega a 0*. `fr` and `it` spell the number (*zéro*, *zero*) and have no
        `0x85`. The parentheses are a `us` spelling: no other copy brackets the licence clause.
      - Whether the CJK copies use the same byte values for digits is AY-8's charset question, not this one.

## 5. Evidence

| claim | evidence | tier |
|---|---|---|
| the 32 names in id order | `status_data.bin` row `+0` → text bank 5 string `id`, all 32 resolved | 1 |
| the help text | `listhelp_status.bin` decoded as in the corpus block; ids 0 and 31 as the positive control | 1 |
| timers and clear masks | `status_data.bin` `+9`, `+0xC`, all 32 rows | 1 |
| the `+8` durations and the `+6` bit-13 class | `status_data.bin` rows decoded through the header's stride (`+8`) and row pointer (`+0xC`), all 32 rows; the readers on the status-write page §2.4a | 1 |
| what each id does | the linked pages, each tier 1 on its own reading | 1 (by reference) |

## 6. Related

- [`Status-Write/the-status-write-and-its-side-effects.md`](Status-Write/the-status-write-and-its-side-effects.md) — the write, the per-status terminal table, the cascade the clear mask drives.
- [`../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md`](../03-World-Area-Field/Field-Record-Table/field-record-table-navimapdata.md) — the definition table's layout and the `0x80000003` argument.
- [`../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md`](../02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md) — bank 5.
- [`../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md`](../08-Combat-Formula/Evaluation-Context/the-evaluation-context-field-map.md) — the merged layers and which slots read which id.

## 9. Falsification pass 1 — 2026-09-13 (OPUS)

Both shipped files were re-decoded from the archive without reading the prose. **Every tabulated
cell reproduces** — roughly 128 of them across two tables — and so does every structural statement.

### `status_data.bin`

The section at `battle_pack.bin` directory `+0x40` is `st2e`, **count 32, stride 40**, data at
`+0x20`, spanning `0x1B178`–`0x1B6A0`.

| §2 column | measured |
|---|---|
| the 32 `+9` values | **all 32 exact** — non-zero only on ids 2 (45), 6 (100), 8 (120), 10 (1), 25 (15), blank everywhere else |
| the 32 `+0xC` clear masks | **all 32 exact**, decoded to ids: id 0 `7FFEF57C` → **2–6, 8, 10, 12–15, 17–30**; id 1 `1FFC0004` → **2, 18–28**; id 31 `7FFFFFFC` → **2–30**; the singletons 3→17, 10→25, 15→20, 20→15, 25→10; every other row zero |

| §2.1 column | measured |
|---|---|
| the 32 `+8` bases | **all 32 exact**, including `0xFF` on precisely the eleven rows the table writes "—" (0, 1, 2, 6, 7, 9, 10, 11, 16, 29, 31) |
| the harmful / beneficial class | **bit 13 of the word at `+6` is set on exactly ids 0–16, 29, 31 and clear on exactly 17–28, 30** — the table's split, cell for cell, Berserk included |

### `listhelp_status.bin`

**3,568 bytes**; `st2e`, count 32, stride 4; the 32 string ids are **120,000…120,031, contiguous**;
the second section at `+0xA0` is `{1, 0xC, 3407}`; 34 `u32` offsets follow from `+0xAC`.

**And the offset table explains the two conventions the header note states rather than derives:**

| | |
|---|---|
| "entry 0 not a string" | its offset resolves to file `0xCC` — **inside the offset array itself** (`0xAC`–`0x134`), so it cannot be one |
| "entries 1–32 the statuses in id order" | entry 1's offset resolves to **exactly `0x134`, the first byte past the array** — the string block *begins* at entry 1, which is what puts status `id` at entry `id + 1` |
| "entry 33 empty" | it points at file `0xDEF`, the **last byte of the file**, and that byte is `00` — an empty string, literally |

### Nothing was found wrong

Every figure, mask, duration, class bit, file size, id range and section header this pass could
reach reproduced exactly. That is worth recording as a result rather than passed over: the page's
`corpus_validated` line claims a decode of two files and 32 rows each, and the decode holds.

**Not claimed:** the name resolution through text bank 5, the help-text decoding and its three
undecoded control codes, the duration formula `2·base − base·Vit/100`, the periodic beat, and the
"removed with mode 0" reading of the clear mask were **not** re-derived — this pass checked the
tables against the shipped bytes, not the engine against the tables. The other-language copies were
not decoded. Nothing was executed or observed live.

## Crossings into other layers — FINAL-AUDIT pass 22 (OPUS, 2026-09-18)

**Gameplay — this page is the CALLER.** `0031C5D0` (8,136 B) consults the encoded-id query family
at **fourteen** sites across four entries:
`BattleEncodedId_IsValidForClass` (`00322C50`) at `0031C643`, `0031C662`, `0031C716`, `0031C85C`;
`BattleEncodedId_DispatchQueryMode0Value` (`00309EC0`) at `0031C828`, `0031C98F`, `0031CC08`,
`0031CD6C`; `BattleEncodedId_DispatchQueryMode1` (`0030AE30`) at `0031C836`, `0031C9A6`,
`0031CC16`, `0031CD7A`; and `BattleEncodedId_QueryMode0Positive` (`0030B0E0`) at `0031DFD3` and
`0031E0C3`. **The mode-0 and mode-1 dispatchers are called in pairs** — each `00309EC0` site is
followed within fourteen to twenty-three bytes by a `0030AE30` site — so the body asks both
modes about the same id rather than choosing between them. **This page consults that family and
owns nothing in Gameplay;** the validator `00322C50` is accounted the same way from
[the party-read page](../01-Script-VM-Native-Bridge/Party-Presentation-Verbs/the-party-read-in-state-machine.md).

## Crossings into other layers — FINAL-AUDIT pass 22 (FABLE, 2026-09-14)

**CoreRuntimeScheduling.** `BattleStatus_ComputeDefaultShortTimer` (`003876D0`) reaches its authored table through
`ImageAddress_ResolveRuntimePointer`, the image-address resolver that most table readers call. The edge is mechanical
and says nothing about the status table's meaning.

`002FA560` (476 B) is ~~the status-handler dispatch~~ the MMSG text-bank switch of §4 `GE-1` *(corrected 2026-10-02, OPUS: checked at `002FA560` and `002F7800`, which sets `ecx = 0xC`, stores `02EC3DE0` and jumps to `00238640`)*: `ecx` 0..0x1B selects one of twenty-eight dedicated bodies in the `002F7660`..`002F79C0` run (ids 0x00,0x04,0x08,0x0D,0x0E,0x0F,0x14,0x16,0x17,0x18,0x19 in the 0x7xx band, the rest in 0x79x) and tail-jumps `002385D0` with it; out-of-range returns ~~- the effect-id to executor switch the statuses callers share~~ - a bank selector, not an effect-id executor switch *(corrected 2026-10-02, OPUS)*.

Interior anchor `002FA5E2` (function `002FA560`).

**Resource — SERVICE.** `002FA560` tail-jumps `002385D0`, a resource-layer body that calls `00384420`/`008478A0` on that layer; `00384420` in turn calls `0032E400`/`0032E620` — the status dispatch's real work crosses into resource handling.

**World — PEER.** `003845F0`, cited on this page, sits inside the world-field call graph in both directions — `003847B0`, `00236C30`, `0023A160` and `00238640` call it, it calls `003846F0`, and `00236C30` also calls `003847B0` — the status rows and the field layer share the graph, not the ownership.

**CombatAI — CLIENT.** `00238880` on the combat-ai layer calls `003845F0`.

**CombatAction — CLIENT.** `00237FC0` on the combat-action layer calls `003845F0`.

*Added 2026-09-29 (FABLE, pass-22 debt): one paragraph per layer the audit still reported for this page.*

**CombatFormula — CLIENT and SERVICE (8 edges).** `BattleFormula_AppendStatusAddOperation` (`00387BB0`) calls `BattleStatus_ComputeDefaultShortTimer` (`003876D0`) for a status's default timer; the candidate-status applier `BattleFormula_ResolveCandidateStatusApplications` (`00387CB0`) calls `BattleFormula_BuildCandidateStatusMask` (`003851F0`), `00387BB0` and `0038D680`, and is itself called by the two calculator-slot wrappers `BattleFormula_CalcApplyCandidateStatusesRequired` (`0038FCC0`) and `BattleFormula_CalcApplyCandidateStatusesOptional` (`0038FCD0`); the apply-mask writer `0038FCE0` also calls `0038D680`, a 41-byte step that sets the miss pair at `02AEDFBC`/`02AEDFB8` when the entry's word `+0x18` is `0xD` and otherwise stores twice the dword at `+0x48` into `02AEE02C`; and the Protect/Shell add `003908A0` calls `00387BB0`. The formula layer is where a status id from this table is turned into an add operation on a result: it reads the table's default timer and clear masks through these bodies, and the table itself is data this page describes.

**UI — CLIENT (3 edges).** The UI bodies `00273E30` (2,382 B), `002BFD20` (1,652 B) and `0035D380` call `0031C5D0`, the 8,136-byte generic per-class encoded-id query that fills a caller-supplied 0x98-byte record (the page locates the read of the status row's ~~`+0x0B`~~ `+0x0A` word inside it — `[rsi + 0x0A]` at `0031E288`, §4 *(corrected 2026-10-02, OPUS)*); `0035D380` stores the id pair into a static record at `022CA480`, calls the query and zeroes the record when it fails. Menus fetch a status's descriptive record through the same query this page read; the UI owns the display, not the status rows.

## Interior citations for the entry-cited functions (OPUS, 2026-10-02, cloud-drafted)

*Functions this page named only at their entry. Each sentence states what the body does (access and representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by [`interior_applier.py`](../_index/candidates/opus-the-thirty-two-statuses-cloudint-1002/interior_applier.py): every anchor is an instruction boundary inside its function and decodes to the recorded mnemonic.*

| function | size | what the body does | interior anchors |
|---|---|---|---|
| `00238640` | 19 B | tail-jumps `003845F0` with `rcx` set to `02F973C0` plus the sign-extended `ecx` times 8 | `00238643`, `0023864A`, `0023864E` |
| `0030AE30` | 105 B | returns -1 when the word `cx` is `0xFFFF` or its top nibble field (`AND 0xF000`) is above `0xE000` unsigned; otherwise takes the record at `01EEBCC0` plus (word >> 12) times `0x58`, returns 0 when the low 12 bits exceed (signed) the record's dword `+0x3C` minus 1 or when its qword `+0x50` is null, and else tail-jumps that qword with `ecx` = the word and `edx` = 1 | `0030AE39`, `0030AE53`, `0030AE60`, `0030AE7D`, `0030AE93` |
