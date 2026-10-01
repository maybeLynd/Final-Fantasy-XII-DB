# GR-7 answered: operand-store kind 10 is the unit's "what was used on me" mask, read only by enemy AI (OPUS, 2026-09-30)

Register row GR-7 asks who reads operand-store kind 10: the per-unit mask that `00312170` builds from action row `+0x3A`,
the element byte `+0x13`, and `+0x0C` bits 13 and 14. It also says the reader fixes what the `+0x3A` category means.
The page is [the action definition row](../../../07-Combat-Action/Action-Definition-Row/the-action-definition-row.md),
§2.2 (`+0x3A`) and §7 (the GR-7 box).

Method: static reads of the certified image, plus a census of the shipped data. The checker is `gr7_kind10_check.py`
(output `gr7_kind10_check.out`, **`FAILS 0`**). It uses the kit's `retool.py` and `regval.py`, the `us` `battle_pack.bin`
and the 166 `.ard` files, the same corpus as [`fe7_order_reach.py`](../fe7-order-reach/fe7_order_reach.py) R7.

## The answer (OPUS)

**Where it lives (K1).** Kind 10 is the battle unit's dword **`+0xB90`**, index 0 only.

- The operand-store writer `00329E60` writes it in its case-10 arm, `00329F1C`–`00329F29`.
- `AiTargetSelector_ResolveOperandValue` `00321190` reads it in its case-10 arm, `0032126F`–`0032127C`.
- Both arms were found by decoding the two jump tables.

**Who writes it.** There are three writers:

| writer | what it does |
|---|---|
| **K2** the composer `00312170` | Sets bit `+0x3A` (when 1–254), ORs in the element byte `+0x13`, and sets bits 8 / 9 from `+0x0C` bits 13 / 14. It then ORs in the current value (`00312248`) and writes the result back (`0031225E`) on the second unit it is handed. |
| **K5** the enemy AI store op `002FE660` | Order ids **`0x4122`** (`bts`) and **`0x4123`** (`btr`) set or clear the order's parameter bit in kind 10 of the unit that `0031B7E0` resolves from `+0x710`. |
| the reset `BattleUnit_ResetStateForReuse` | Zeroes it (`00236BE0`), and the full 0xF50 clear of the slot on allocate (`002344D2`, `memset(slot, 0, 0xF50)` in `00234480`), which has no displacement. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr7-0930/REVIEW.md) item 2)* |

**Who reads it (K3, K4).** There is exactly one reader: **`AiOrder_EvaluateTargetSelector` `00301AD0`**.

- A selector entry is `{u16 operand, u8 mode, u8 opcode, s16 param}`.
- Opcode `0x36` / `0x37` with **mode 3** drops into the per-candidate loop. That loop's jump table sends cases 54 / 55
  to `00303079`, which reads the candidate unit's kind 10 and tests `bt mask, param`.
- `0x36` needs the bit set; `0x37` needs it clear.

Every other reader call site passes kind 3 or a kind decoded from authored data (`operand >> 12`). The composer and the
store op read the value only to modify it.

**Who uses that reader (K6).**

- **No player gambit.** None of the 256 target-condition rows carries opcode `0x36` / `0x37`. The gambit rebuild `00328140` writes row word `+8+2e` into entry e's {mode, opcode} word, so K6 reads the evaluator's opcode byte. The 256 rows are identical in all nine language packs. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr7-0930/REVIEW.md) item 3)*
- **Only enemy AI order sets.** There are 6,140 mode-3 tests across the 1,422 sets and 50,050 records. Almost all use
  relation 4 (self), so the enemy tests its **own** mask.
- **The bits it tests:**
  - 0–7, the element of what hit it;
  - 8 and 9, the `+0x0C` flags;
  - 10–16, the `+0x3A` category;
  - 25–28 and 31, bits the AI sets for itself with `0x4122`.
- No authored dynamic kind (selector modes 0–2, store ops `0x4149` / `0x4155`–`0x4157`) is ever 10, so kind 10 is
  reached only through the fixed paths above.

**What `+0x3A` means.** It is an **AI reaction class**. It is the bit that tells an enemy's authored logic "an action
of this class was used on me". The enemy typically reacts with an order and then clears the bit with `0x4123`
(`gil_b` set 2 records 63/64: bit 13 → action `0x148`, then `0x4123`). The users are:

| bit | tested by | actions carrying it |
|---|---|---|
| 16 | `mic_d`, `tri_g` | Cure … Curaja, the Potions, Float Mote |
| 15 | `mic_d`, `tri_g` | Balance / Reflectga Mote, 49 rows |
| 14 | `bds_f`, `hne_e` … | Dispel / Dispelga |
| 13 | `gil_b`, `mfr_c` … | – |
| 12 | `rbl_g` | Elixir / Megalixir |
| 11 | `rbl_g`, `rbl_k` | – |
| 10 | `rwg_a` | – |

**In player terms:** some enemies watch for what you do to them. Hitting one with an element, or using a cure, Dispel,
Balance-type or Elixir-type action on it, sets a bit on that enemy. Its script then answers with a counter-move and
clears the bit. Your own gambits cannot test any of this.

## Consumers (routed, not edited here)

- The action row page: the `+0x3A` cell ("who reads that kind-10 mask … is not read") and the §7 GR-7 box. That page
  is FABLE's.
- `_types/fields.tsv` **`BattleUnit +0xB90`** says "action-scoped dword - zeroed at reset (00236BE0), **no other
  writer**". That is now contradicted: it is operand-store kind 10, written at `00329F29` (via `00312170` and
  `002FE660`) and read at `0032127C` (via `00301AD0`). These are indexed forms the battle-unit census did not type. The
  battle-unit field map (`the-battle-unit-field-map.md` row `+0xB90`, "OPEN") needs the same fix. Routed to DATA.
- Register row **GR-7**, via a DATA restatement request.

## Limits

- ~~The other `+0xB90` accesses in the image, in `00172750`, `001728C0`, `00177A70`, `00186800`, `004B8F20` and
  `0070A7F0`, are outside the battle layer. The battle-unit census does not type them as battle units, and they were
  not re-typed here.~~ The other `+0xB90` accesses in the image are in `00172750`, `001728C0`, `00177A70` (fragment
  `00177B71`), `00186800`, `00186CD0`, `004B8F20`, `0052D1E7`, `0054FE00`, `0070A7F0` (fragments `0070A83C` /
  `0070A894`), `00791E70` and `007D44BC`. The raw disp32 census covers every width and form, and none of these bases
  is a BattleUnit (the review record types each one). A reader through a biased base (a unit pointer plus a folded
  offset) or a bulk copy of a unit is outside any displacement census. *(narrowed 2026-10-01, SWE2-CONTRACT for OPUS, on SWE2-AUDIT-SPEC's [review](../auditspec-review-gr7-0930/REVIEW.md) item 1)*
- Which unit the composer's "second unit" is, target or actor, is taken from the page. The relationship gate
  `0030AB40 > 1` is not re-read here.
- Only the `us` `battle_pack` was read for the player rows. The target-condition table is language-independent data,
  but the other eight packs were not compared.
