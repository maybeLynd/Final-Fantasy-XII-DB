# SWE2-AUDIT-SPEC review of SD-160 (sd160-free-target-type3-0930, OPUS, af6684173): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, FABLE session 0aca3c35 review worker, 2026-09-30). Reviewed:
OPUS's `af6684173` (the record's only commit), [README](../sd160-free-target-type3-0930/README.md), `sd160_check.py`
and `sd160_census.py`. Measured at HEAD 17a959c94. Static, certified image, plus the shipped scripts in
D:/FFXII_TZA_extract.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD160-0930 | sd160-free-target-type3-0930 | `af6684173` | ACCEPT-WITH-NARROWING |

F1-F3 and every census number reproduce independently. The narrowing is two sentences: one names a character the
evidence does not support, and one misdescribes an output file.

**Re-run.**
- `sd160_check.py` gives [rerun_sd160_check.out](rerun_sd160_check.out), identical to the committed output
  (ignoring CR). F1-F3 and C1-C3 PASS, `FAILS 0`.
- **`sd160_census.py` writes its two TSVs into its own folder** (`HERE`). So I ran a byte copy
  ([rerun_copy_sd160_census.py](rerun_copy_sd160_census.py)) from this folder; the relative paths resolve the same.
  - Its [rerun_sd160_census.out](rerun_sd160_census.out), [sd160-census.tsv](sd160-census.tsv) and
    [sd160-type3-scripts.tsv](sd160-type3-scripts.tsv) are identical to the committed files (ignoring CR).
  - The committed TSVs carry a 14:05 mtime, after the 08:46 commit. Someone re-ran the script in place. The content
    is unchanged, and git status is clean.
- Package dir clean after my runs: yes (`git status --porcelain` prints nothing).

**Re-derived independently.**

The static part: [sd160_static_indep.py](sd160_static_indep.py) / [.out](sd160_static_indep.out) (lane loader
`ov31_indep.py`), and [dis_static.out](dis_static.out) / [dis_other_writers.out](dis_other_writers.out)
(`b8dis.py`).
- **F1 holds.**
  - `003171D9` / `003171F8` check `cmp byte [[unit+0x698]+5], 1`.
  - `00253770(4, 1)` is called unconditionally at `003171E7`.
  - Then come `00263C20([unit+0x10])` (= `byte [+0x0E] & 0xF`), `cmp eax,3` / `je` skip (`00317207` / `0031720A`),
    and `word [[unit+0xE68]+0x52] == 0xFFFF` skip (`00317217`).
  - Only then is `00253750` called (`0031721F`).
  - The only caller of `003171C0` is `003122D5`.
- **F2 holds.** `003528C0` passes `00267E10`'s pop to `00269FE0(actor, v)`. That clears and ORs the low nibble at
  `0026A033`..`0026A03B` for every record kind; only the `+0x1C` bits are kind-gated.
- **F3 holds.**
  - `00510340` tail-jumps `002396B0`.
  - `cmp ebx,3; ja` stores 0 for v > 3 (and, unsigned, for v < 0). Otherwise it stores dword `[01E09EE8 + 4v]`, and
    the table reads `(1, 5, 3, 4)`.
  - The store is `byte [unit+0x58]` (`002396D6`).
- **Routes into the writers.**
  - `00269FE0` has exactly two rel32 callers: the verb (`003528D6`) and the refresh (`00238E3E`, `edx = movsx
    [unit+0x58]`, skipped when 0). Neither has a jcc caller or a data slot.
  - `002396B0` has one caller, `0051035B`.
  - The refresh rewrites `+0x58` only to 1 (`00238DC3`, from 4) or 7 (`00238E02`). So a 3 in `+0x58` comes from
    F3's table, which agrees with the battle-unit field map's `+0x058` writer list (2 / 2).
- **The nibble's other writers.** An image-wide `and byte [r+0xe], 0xf0` scan finds 2 sites: `0026A033` (F2) and
  `002666F8` (the record initialisation, which clears it).
  - The scan is limited to that idiom. A whole-byte store to `+0x0E` would not show, so the scan cannot rule one out.

The census: [sd160_indep_census.py](sd160_indep_census.py) / [.out](sd160_indep_census.out). It uses my own container
parse and 1/3-byte decode over the **extract**, where the package reads the VBF, and neither
`gen_req_channel_census.py` nor `script_verb_census.py`.
- **Coverage.** 10,045 `.ebp` files. The 9 skipped are `evt_t0020.ebp` × 9 languages, which have no script section
  and no raw call pattern ([sd160_rawgap.out](sd160_rawgap.out)).
- **63,432** call sites of the two verbs, all `CALLPOPA` (0x5D). The value histogram is identical to the package's:
  `btlAtelSetUnitType` 0 / 1 / 2 / 3 = 59,814 / 234 / 297 / 369, and `setfreetargettype` 1 / 3 / 4 / 6 = 18 / 315 /
  2,340 / 45.
- **Constants.** Each argument is the instruction immediately before the call, a `PUSHI` / `PUSHII` immediate: 0 sites
  otherwise.
- **The type-3 sites.** 612 sites in 261 files, 0 outside `plan_master`. Each of the 9 languages has 68 sites in 29
  zone files, identical (zone, verb, script, count) across all 9.
  - That is 68 distinct (zone, script) pairs.
  - The families are THIRD 10, npc_battle 6, event_garif 1, DAL_SOLDIER 9, BASH 3, ex_trial 4 and disp_tama 35. These
    match the README table, zone by zone.

**Controls.**
- **The decode must not drift** (the defect: a missed call). A raw byte search for the six 3-byte call encodings finds
  63,446, which is 14 more than decoded. [sd160_bul_b01.py](sd160_bul_b01.py) / [.out](sd160_bul_b01.out) and
  sd160_rawgap account for every one:
  - 5 lie outside the script section;
  - 9 are `bul_b01.ebp` sec+0x26E9C in each language, inside the script directory (directory at 0x267D0, 45 × 0x30
    entries), so they are data, not code.
  - So no call is missed.
- **The total must reproduce** 63,432 from a different input (the extract, not the VBF), and it does.
- **The package's own gate has a latent weakness.** C1's constant test is `startswith("PUSHI")`, which would also
  accept the decoder's `PUSHI0`..`PUSHI3` (0x3E..0x41, variable-slot pushes with no immediate). No site has such a
  predecessor, so it did not bite here.

**Citations checked.**
- `00317207`, `0031720A`, `00317217`, `0031721F`, `0026A033`..`0026A03B`, `0051035B`, `002396C3`, `002396C8` and
  `002396D6` support their sentences.
- **Defect:** the README says `sd160-census.tsv` is "every call of the two verbs". It holds only the 612 type-3 sites
  (613 lines with the header), as the script's own comment says.
- **Name readings.** ガブラス → Gabranth and ラーサー → Larsa are the standard Japanese names. **モーニ is not
  Montblanc**: his Japanese name is モンブラン. Nothing in the package resolves モーニ to a character.

**Runtime routing.** The Limits' "which of these units is ever defeated, and with what type at that moment" is a
genuine run-time fact. The refresh (`00238E3E`) or a later verb can rewrite the nibble. Static evidence settles which
scripts ask for type 3, not the value at defeat.

**Correction wording** (the producer applies it to the README):
- In "The evidence is of two kinds": "Its output is `sd160-census.tsv` (the 612 type-3 sites, all languages) and
  `sd160-type3-scripts.tsv` (one row per zone, verb and script)".
- In the C3 table and Limits:
  > `THIRD_*` (Gabranth and Larsa, from `ガブラス` / `ラーサー`, and eight more third-party scripts, among them
  > `モーニ` twice; `モーニ` is not Montblanc's Japanese name `モンブラン` and is not resolved to a character here)

  Drop "Montblanc" from the Limits' readings sentence.
