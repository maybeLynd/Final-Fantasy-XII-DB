# UQ-218 pass 18: the band names, the yaw sign, the `@FOR` tail lists, `@FDM` `+0x08` and the `@FEF` companion table (SWE2-DATA, 2026-09-30)

affected: 17-Presentation-Rendering/Model-And-Motion-Formats/fdm-and-for-entries.md, 17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md, _index/OPEN-QUESTIONS.md, _index/candidates/uq218-cm-entry-residues/README.md

**Question.** UQ-218 (register row PARTIAL) named five residues after pass 17: the exact locomotion band → `@FMN` name
binding, which yaw sign is the character's left, the `@FOR` record's three u16 tail index lists, the `@FDM`
descriptor `+0x08` field, and (after OPUS's CON-195 refuted "the `02B64380` table is never filled") what the `@FEF`
arm of `00409FE0` does with its seeded row. All five are answered here from the certified image
(`73461d08…`) and the full extract; no runtime evidence is used or needed.

Three scripts, each printing its checks and `FAILS`; every one FAILS 0 at `43b8ff75ea`:

| script | what it pins |
|---|---|
| [`band_names.py`](band_names.py) ([out](band_names.out)) | the op `0x0A`/`0x0B` → record → op `0x09` → `@FMN` join over all 3,164 `.ca`, 10 code sites |
| [`for_tail_census.py`](for_tail_census.py) ([out](for_tail_census.out)) | the tail lists and descriptor bytes under the builder's decoding over all 1,045 `.cm` with `@FOR` + `@FDM`, 19 code sites |
| [`fef_tables.py`](fef_tables.py) ([out](fef_tables.out)) | the two start-up path tables decoded from their populators, their join and archive membership, 12 code sites |

## 1. The band → `@FMN` binding is a code path, measured

- `00417110` (op `0x0B`) takes the selector result as **list index** `i = result & 0xFFFF` and **track offset**
  `h = result >> 16` (`00417281`, `0041727D`) and issues a synthetic op `0x01` for track `list[i] + h`
  (`0041735C`, `00417367`).
- The track is a **record index inside the bound `@FMC` entry**: `0041CD30` walks the entry's records by their `u16 +4`
  length and stamps the index at row `+0x80` (`0041CDC8`).
- The record's op `0x09` names the motion: `@FMN` index `word[cmd+2] >> 1`. Read as a `.ca` slot, all **33,753** such
  indexes reached from the classifier's lists land on an `@FMN` entry — the control on that reading ~~(the `s16[ctx+0x2A]`
  base the page records adds 0 on these paths)~~. *(Corrected 2026-09-30, SWE2-DATA, on SWE2-AUDIT-SEM's review `auditsem-review-uq218-p18-0930` §3 N1: the index reading holds on the index arm of `00417F40` (taken when `[ctx+0x368]+4 & 3` is non-zero); the other arm looks the motion up by name through `00409930`/`00409780`. The `s16[ctx+0x2A]` base is shown to be 0 on the shipped `.ca` paths only by the 33,753/33,753 data control; its writers are not traced.)*
- Measured over 1,489 selector commands (kind `0` 782, `0xA` 700, `0xB` 7): band 1 → `walk_f`, 2 → `run`, 3 →
  `walk_l_*`, 4 → `walk_r_*`, 5 → `walk_b_*`, 6 → `trn_l` / `trn_r` (or `walk_f` where no turn motion is authored),
  7 → `hi_trn_*`, 8 → `stp_*` (kind `0xA`), kind `0xA` 9 → `run_l_*`, 10 → `run_r_*`, 11 → `run`, 12 → `sleep`; kinds
  `0` and `0xB` carry the documented renumbering (their 8–10 are run tracks, the last entry `sleep`); band 0 enters a
  nested kind-`0x10` idle pick. Where a model lacks a motion the authored list repeats a simpler one (`walk_f` in the
  side slots, `CreateStartPoseDammyActFile` for monsters). Kind `0xB`'s lists add `rlx_escape_*` at entries 11/12,
  which the classifier's renumbering never produces.
- **The offset is the foot:** `h` picks the `_l` / `_r` start-foot variant of the same motion (`walk_f_l` / `walk_f_r`
  …), from `esi = byte[+0x418] & 1` on the walk bands.

## 2. The yaw sign: a positive delta is the character's left

The classifier's two signed tests both route a **positive** angle to the `_l` motions, with no exception in the corpus:
- heading − facing (`+0x244` − `+0x124`, degrees, `004258C6`) in (45°, 135°] is band 3 (`00425919`) → `walk_l_*`
  (287 / 281 bindings by offset, `walk_r` **0**); [−135°, −45°) is band 4 → `walk_r_*` (287 / 281, `walk_l` 0);
- facing − previous facing (`+0x124` − `+0x254`, `0042576B`) ≥ 0 sets `esi` (`0042588F`), offset `1 − esi` = 0 → `trn_l`
  (226, `trn_r` 0); a negative turn → `trn_r` (226, `trn_l` 0); band 7 likewise `hi_trn_l` (37 / 0).

This agrees with the movement step `(sin yaw, cos yaw)` on X / Z (`heading-speed-to-position-delta.md`) in a right-handed,
Y-up frame, where +X is the left of a body facing +Z — stated as agreement, not as the proof. The target-bearing arm
(`00424370` = `atan2(local x, local z)` of the target) maps (45°, 135°] to band `0xA` = `run_r_*`; what that motion looks
like relative to the target is not claimed.

## 3. The `@FOR` tail lists are read — the per-part draw lists

**Correction.** The motion/format pages said no `0xE0`-stride walker reads the three u16 tail lists. `0053AB50` does,
through the selected record it keeps at `rbp+0x40`:
- list `recordBase + word[rec + 8 + 2·part]`, count `word[rec + 0x10 + 2·part]` (`0053C16B`, `0053C187`);
- the **packing kind** is `byte[rec + 2 + part]` (`0053C227`) — the bytes the page recorded as "enable flags = 1".
  Kind 3 = 4-byte `{d, s, a, b}`, 2 = 3-byte `{d, s, a:4|b:4}`, 1 = 2-byte `{d:5|s:3, a:4|b:4}` (cursors step 4 / 3 / 2,
  `0053CDF3`–`0053CE02`); kind 0 ⟺ an empty list (1,871 of 1,871);
- `d` selects the part's `@FDM` descriptor (`0053C308`), `s` the descriptor's sub-record (`0053C320`), and `a`/`b` go with
  the sub-record to `0053D140`, which uses them as indexes (`0053D3E0`–`0053D3E8`, `byte[sub+2]` of them) into the
  builder's per-draw table at `rbp+0x2B0` — packed texture-register qwords built from each texture the table-A/B
  selection resolved (`0053BF85`–`0053BFEC`). So an element binds one descriptor, one sub-record and up to two textures;
- a second pass (argument 6 = 1) reads a fourth list, `word[rec+0xE]` / count `word[rec+0x16]`, packing `byte[rec+1]`
  (`0053C173`, `0053C18F`, `0053C22F`). `0053D780` makes that pass only for a class-`'h'` object
  (`byte[obj+0xC] == 0x68`, `0053D8C9`), and for those the first pass draws the high model's records against its
  partner's `@FDM`.

**Corpus (1,045 `.cm`):** 1,759 lists of the 913 normal models all resolve in their own `@FDM`; all 132 high-model
(`obj_finish/in/high/h*.cm`) first-pass lists resolve in the base model `<name>.cm`'s `@FDM` — 59 of them would **not**
resolve in their own, the control that the partner is real — and every non-empty fourth list (132) is a high model's
and resolves in its own `@FDM` part 0. 18,049 elements. Which file the partner index names is inferred from this fit
(the naming join), not traced.

## 4. `@FDM` descriptor `+0x08`

**Correction.** "Not consumed" is wrong: `0053D4B0`, called with the descriptor (`0053C403`), writes `s8 desc+8` and
`s8 desc+9` into the VU1 packet (`0053D585`, `0053D592`) beside `desc+4` bit 0, bits 1–7, 28 and 29. Bytes `+0xA`/`+0xB`
have no reader there. **All four bytes are zero in all 12,044 shipped descriptors**, so the pair is read and constant.

## 5. The `@FEF` arm: a start-up companion table appends `chara\hNNNN.efx` to each model

- `0019FFD0` (the `AsyncLoadManager` at `01F81160`) clears a 0x140000-byte table at `+0x228` and seeds **144** `.rdata`
  paths at `qword[+0x228 + 8·(letter·0x500 + num)]`; `001A09E0` looks a `.cm` path up by its class letter and four
  digits. Every seeded path is `PS2Data\effect_finish\jp\chara\hNNNN.efx`.
- The file layer (`001A0CF0`, `001A0E50`) appends that companion after the main file and stores the main length in
  the buffer's last dword (`001A0F4E`).
- `00409FE0`'s arm: the `02B64380` row (seeded by `0040A230`, CON-195) is the model's own path; the effect instance is
  created from the appended companion at the tail offset (`0040A16F`, `003B38B0`); `001D6EC0(row)` is the same
  companion lookup, `strstr(…, "chara\\h")` + `sscanf("%d.efx")` recover `NNNN`, stored at the effect record `+0x30` by
  `003B3B10` (`003B3B2C`). The number's reader is `003B33D0(handle)` (called from `0024D140` and `0024D330`; the latter
  asks whether the current type-3 effect is number `0x34`).
- **All 144** `02B64380` rows key a companion, and ~~all 144 models and 144 companions are shipped files~~ all 144 models are shipped, and the rows name 125 distinct companion files, all shipped (`h0000.efx` ships unnamed). *(Corrected 2026-09-30, SWE2-DATA, on SWE2-AUDIT-SEM's review `auditsem-review-uq218-p18-0930` §3 N2.)* So the arm runs
  whenever one of the 144 `@FEF`-bearing models (monster 82, npc 27, summon 26, gadget 9) completes a load
  (`0041E580` is its load-completion entry). Which of them a given session loads is content, not code.

**Not claimed:** the `.efx` payloads; what `0024D140` does with the number; the GS meaning of the texture-register fields.

## Consumer check (EVIDENCE-POLICY 4a)

| consumer | action | state |
|---|---|---|
| `fdm-and-for-entries.md` `@FOR` record table (`+0x02` "enable flags"), "the three u16 index lists … none reads them", `@FDM` "kind byte in the pool head", descriptor `+0x08` "not consumed" | struck and corrected | revised-here |
| `fef-and-motion-entries.md` residue: band → name "inference", yaw sign open, `02B64380` reachability | resolved | revised-here |
| `_index/OPEN-QUESTIONS.md` UQ-218 "Still open" | closed, row ANSWERED | revised-here |
| `the-authored-presentation-command-handlers.md` selectors paragraph ("band names themselves are inference"; "Still open: which yaw sign") | the exact text is in `DATA-REQ-FABLE-HANDLERS-UQ218-P18` (the page is in FABLE's active publish) | routed-to-FABLE |
| CON-195 (OPUS `35321544f`, `OPUS-REQ-DATA-UQ218-ROW-CON195-0929`): the UQ-218 row's pass-13 wording ("dead-stripped", "ships all-NULL", "arm is vestigial"), the motion page's last "survives as dead-stripped" line, the `uq218-cm-entry-residues` record's pass-13 paragraph, this lane's inbox history | struck and corrected; `fef_tables.py` T1 decodes the seeded rows | revised-here |
| `uq218-fmc-selector-kinds/classifier.md` / `README.md` (FABLE records, "Not claimed: which yaw sign is left") | historical records; this record answers them | agrees |

Regressions: `band_names.py` (S0/S1/T/T7/R fail if the side-step or turn bindings flip), `for_tail_census.py` (C2–C5 fail
under the old "unread" / "enable flag" / "+8 unused" readings), `fef_tables.py` (J, X); run at 43b8ff75ea, FAILS 0.
