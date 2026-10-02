**Scope and method.** Five step bodies of the standard hit pipeline, each read whole with `retool.py dis` against the shipping image (image base `0x120000` included in every address), one level into callees: the generator thunk `00379CD0` (`jmp 00863BF0`, the MT19937 tempering output, a full `u32`), the registry resolver `0020E600` (`eax = ecx; rax += [01F83530]`, the offset-to-pointer step every table lookup below goes through), and the consumers `00388440`, `003884F0`, `00388660` (head), `003896B0` and `0038BE00` where a comparison direction had to be pinned. Calculator slots take `(source stats, target stats, &ctx)` in `rcx, rdx, r8` (the resolver's call at `003863CA`-`003863D0`; `00390F20` gets the same three at `003863ED`-`003863F8`). Step-table slots confirmed by reading `01EFA5C0`: slot 5 = `00388350`, 6 = `00388440`, 7 = `00388490`, 8 = `003884F0`, 9 = `00388550`, 10 = `00388660`, 29 = `00389140`, 98 = `0038BE00`. Shipped values come from `battle_pack.bin` (equipment table at directory `+0x38`, 557 rows of 52 B; augment table at `+0xEC`) read with `Tools/dashboard/ff12_content.py`'s decoders from `FFXII_TZA.vbf`.

**The weapon-row lookup all three weapon readers share.** `00388350`, `00388550` and `00389140` resolve the source's weapon the same way (first copy at `003883AA`-`00388409`):

```
tbl = [02EBF0F8]                      ; equipment registry
id  = source.u16[+0x50]               ; equipment slot 0, the weapon (0xFFFF = empty)
if id >= 0x1000 + (tbl ? tbl.u32[+4] : 0)  -> byte = 0         ; out of range (incl. 0xFFFF)
row = 0020E600(tbl.u32[+0xC]) + (id - 0x1000) * tbl.u16[+8]     ; 32-bit add, row index = id - 0x1000
byte = row[+0x1B] or row[+0x1C]
```

The row address is formed with 32-bit `imul`/`add` (`00388403`-`00388407`, `003885BD`-`003885C0`, `003891AE`-`003891B1`), so the table is assumed to live below 4 GB; a port simply indexes the equipment table by `id - 0x1000`. A null registry (or a null return from `0020E600`) reaches `movzx eax, byte ptr [0 + 0x1B]` (`0038840F`-`00388412`; `003885C2`, `003891B3` likewise), a fault path a port need not reproduce. Shipped row 0 is *Unarmed* (`0x1000`), so an empty-handed attacker still resolves a row.

**New weapon-row fields.** The equipment row's `+0x1B` is the **knockback base** and `+0x1C` the **combo / critical rate**. Neither appears in the dashboard decoder's field list (it states "combo and critical rates are not located", `Tools/dashboard/ff12_content.py:1124`). Shipped census over the weapon classes 0-16:

| class (recipe) | rows | `+0x1B` | `+0x1C` | example |
|---|---:|---|---|---|
| 1 swords (20) | 25 | 10 (24 rows), 0 (1) | 5 (19 rows) … 30, 100 | Broadsword `0x1001`: 10 / 5; Hero's Blade `0x10A1`: 0 / 100 |
| 2 greatswords (20) | 12 | 0, 10, 15 | 5 … 25, 80 | Wyrmhero Blade `0x10AD`: 10 / 80 |
| 3 katanas (22) | 10 | 0 | 20 (9), 30 | Kotetsu `0x1019`: 0 / 20 |
| 4 ninja swords (21) | 8 | 0 | 12 … 32 | Ashura `0x1023`: 0 / 12 |
| 5 spears (20) | 15 | 10 | 4 (12), 0, 10 | Javelin `0x102A`: 10 / 4 |
| 6 poles (24) | 13 | 10 | 15 (12), 35 | Oaken Pole `0x1036`: 10 / 15 |
| 7 bows (25) | 16 | 0 | 5 (14), 20, 25 | Shortbow `0x1042`: 0 / 5 |
| 8 crossbows (26) | 8 | 0 | 7 | Bowgun `0x1050`: 0 / 7 |
| 9 guns (27) | 12 | 10 | 5 (11), 10 | Altair `0x1057`: 10 / 5 |
| 10 axes, 11 hammers (23) | 13 | 10 | 6, 8, 20 | Handaxe `0x1062`: 10 / 6 |
| 12 daggers (21) | 12 | 0 | 12 (10), 5, 15 | Dagger `0x106E`: 0 / 12 |
| 13 rods, 14 staves (20/22/27) | 18 | 10 | 0 | Oak Staff `0x1081`: 10 / 0 |
| 15 maces (104) | 10 | 0 | 5 | Mace `0x108B`: 0 / 5 |
| 16 measures (27) | 6 | 0 | 0 | Gilt Measure `0x1094`: 0 / 0 |

**Which recipes run these slots.** Decoded from the recipe table `01EF96C0`: slots 5-10 open the first list of recipes 20-24, 28, 29, 64, 103 and 104 (`[5, 6, 7, 8, 9, 10, 22, 33, 34, 41]`); recipes 25 / 26 / 27 (bows, crossbows, guns and measures) run only 5 and 6 of them in the first list and open the **second** list with slot 29. No other recipe names 5-10 or 29. So bows, crossbows and guns roll knockback but never counter-chance or combo, and only they roll slot 29.

**1. `00388350` `BattleFormula_ComputeKnockbackChance` (slot 5, 236 B).**

```
sRoll = source[+0x1C2] ? mt() % source[+0x1C2] : 0      ; 0038836C-00388389 (div, unsigned)
tRoll = target[+0x1C2] ? mt() % target[+0x1C2] : 0      ; 0038838B-003883A8
kb    = weaponRow(source)[+0x1B]  or 0                  ; 003883AA-00388418
chance = kb - tRoll + sRoll; if (chance < 0) chance = 0 ; 0038841F-00388428 (cmovs)
[02AEDFD8] = chance                                     ; 00388430
```

- Inputs: source and target level `+0x1C2` (u8, `[0, 99]`), the source's weapon slot `+0x50`, weapon row `+0x1B`.
- Draws: **two** from MT19937 via `00379CD0` (`00388379` source first, `00388398` target second), each reduced `% level`, range `[0, level-1]`. A level of 0 skips that draw (`00388373`, `00388392`); in play both are always taken.
- No cap above: a chance over 100 makes the roll certain. Floor 0 (`00388428`).
- Consumer, slot 6 `00388440`: no roll at all when the **target**'s layer id 0 is set in either raw layer (`00388444 test [rdx+0x68],1`, `0038844A test [rdx+0x78],1`); else one draw `mt() % 100` (`00388450`-`0038846B`) and `[02AEDFC8] = (roll < chance)` (`00388474 cmp r8d,[02AEDFD8]` / `0038847B cmovb`, unsigned, strict). `02AEDFC8` is only reported into flag word B bit 3 when the outcome is kind 1, 3 or a hit (`00389734`-`00389741`, `003897F8`-`00389805`); kinds 2 and 4 skip it (`0038978A`, `00389717`-`0038972F`).
- `02AEDFD8` has a second writer, `00388B50` (`00388BFB`, per the scratch-block census), not read here.

**2. `00388490` `BattleFormula_ComputeParryChanceFromSpeed` (slot 7, 90 B) — a counter chance.**

```
if (ctx.u32[+0x08] & 0x2018)  -> [02AEDFDC] = 0                 ; 00388490-00388498, 003884DF
has6 = (target[+0x68] | target[+0x78]) & 0x40                   ; 0038849A-003884AE, 003884BD-003884C3
has7 = (target[+0x68] | target[+0x78]) & 0x80                   ; 003884B0-003884BB (js)
if (!has6)        [02AEDFDC] = 0                                ; 003884DF
else if (has7)    [02AEDFDC] = target[+0x2D] * 2                ; 003884D2-003884D8
else              [02AEDFDC] = target[+0x2D] >> 1               ; 003884C5-003884CB
```

- Inputs: **the target only** (`rdx`): Speed `+0x2D` (rebuild output), the two raw 128-bit layers' ids 6 and 7, and context `+0x08` (the target's `+0x64 | +0x3C` status word). Mask `0x2018` = statuses 3 Stop, 4 Sleep, 13 Disable (bank 5 order): a stopped, sleeping or disabled target gets 0.
- **What ids 6 and 7 are, from the data.** The augment table's description ids resolve (text group 13, `listhelp_ability.bin`) to augment 6 "When attacked, automatically counter with weapon in hand." and augment 7 "Improves chance to counter." Equipment rows carrying them in `+0x1A` (armour / accessory kinds only): Genji Helm `0x1115` (6), Battle Harness `0x1177` (6), Genji Armor `0x1151` (7); party row 31 has both innate (row `+0x50` mask). So this is the **counter** chance: Speed / 2 with Counter, Speed × 2 with Counter and its booster, 0 with the booster alone. No Speed-to-percent clamp: Speed 50+ with both gives ≥ 100.
- Draws: none. Constants: none (shift and add only).
- Consumer, slot 8 `003884F0`: only when the target's unit flag bit 23 (engaged) is set (`00388508`-`00388510`); one draw `mt() % 100` (`00388512`-`00388528`) and `[02AEDFC4] = (chance > roll)` (`0038852D cmp [02AEDFDC], r8d` / `00388534 seta`), i.e. `roll < chance`, unsigned. In the outcome roller the flag only re-labels an evade: band A evade → kind **4** instead of 3 (`0038970A`-`00389717`), band B evade → kind **2** instead of 1 (`00389779`-`00389786`), and those two kinds skip the knockback bit. It does not change whether the hit lands. An accepted combo zeroes it (`003888A1`, per the combos page).

**3. `00388550` `BattleFormula_ComputeComboChance` (slot 9, 260 B).**

```
rate = weaponRow(source)[+0x1C]  or 0                   ; 0038856D-003885C2 / 003885D7-0038862C
f    = (ctx[+0x1B] & 0x20) ? 1.8f : 0.7f                ; 0038855F test; 003885CD [00908E1C]; 00388637 [008F3104]
[02AEDFE4] = (int)trunc((float)rate * f)                ; cvtdq2ps, mulss, 00388644 cvttss2si, 00388648
```

- Inputs: the source's weapon `+0x1C`; context `+0x1B` bit 5 = **merged id 13** of the source (status layer OR augment layer, so either source of id 13 qualifies). Augment 13's description is "Improves chance of scoring multiple hits."; Genji Gloves `0x1164` carries it.
- Constants: `00908E1C` = `0x3FE66666` = 1.8f (≈1.79999995); `008F3104` = `0x3F333333` = 0.7f (≈0.69999999). Single-precision multiply, truncation toward zero: rate 5 → 3 / 9, 7 → 4 / 12, 15 → 10 / 27, 20 → 14 / 36.
- Draws: none. No cap: rate 56+ with id 13 reaches ≥ 100 (Wyrmhero Blade 80 → 144, Hero's Blade 100 → 180 = every swing combos).
- Out-of-range weapon id → `rate = 0` → chance 0 (`00388585 jae 003885C6` skips the load with `ebx = 0`).
- Consumer, slot 10 `00388660`: when the unit's combo counter `+0x6B7` is 0 (`0038868A`, `003886F5`), one draw `mt() % 100` (`003886FD`-`00388713`); no combo when `chance <= roll` (`00388716 cmp [02AEDFE4], r8d` / `0038871D jbe`), i.e. combo iff `roll < chance`. The extra-hit loop that follows is on the combos page.

**4. `00389140` `RollPrimaryFormulaResourceReactionMode2Chance` (slot 29, 173 B) — a ×2 roll.**

```
rate = weaponRow(source)[+0x1C]  or 0                   ; 00389154-003891B3 (same byte as the combo rate)
roll = mt() % 100                                       ; 003891B7 call 00379CD0; 003891BF-003891CD (0x51EB851F, *100)
if (rate > roll) result[+0x18] |= 1                     ; 003891D0 cmp ebx, r8d / 003891D3 jbe; 003891D5-003891D9
```

- Exactly **one** draw, always taken (even with rate 0), range `[0, 99]`, set iff `roll < rate` (unsigned, strict). Merged id 13 is **not** tested: Genji Gloves does not raise it.
- Output: flag word B bit 0 of the result record (`ctx[+0x10]` is the result, `003891D5`). Its only consumer in the formula is slot 98 `0038BE00`: `if (result[+0x18] & 1) [02AEE054] *= 2.0f` (`0038BE00`-`0038BE1A`, constant `01CEBC08` = 2.0). Downstream, `Battle_ProcessActionTarget` reads the same bit as entry bit 11 (scratch-block page).
- Reach: the result initialiser zeroes `+0x18` (`003848F5`, `memset(result+8, 0, 0x140)`); the resolver copies only bits 1-3 from the preview memo (`003860DF`-`00386108`); a byte-pattern scan of `00380000`-`00395000` for `or dword [reg+0x18], 1` finds only `003891D9`. Slot 29 runs only in recipes 25 / 26 / 27. **So slot 98's doubling fires only on recipes 25 / 26 / 27, and among shipped rows only where `+0x1C` is nonzero: bows, crossbows, guns and Excalipur (`0x10C1`, recipe 27, rate 20); measures and the Healing Rod (recipe 27, rate 0) never double;** on recipes 20-24, 28, 29, 64, 103 and 104 slot 98 is reached but its bit is always 0. A failed (kind 6) or immune-by-kind (`0xA`) result clears bit 0 afterwards (`003866E3`, `003866EB`).
- Behaviour, stated plainly: a weapon-rate percent chance that the shot's damage multiplier is doubled before the finaliser, i.e. the ranged critical hit. The page name "resource reaction mode 2" does not describe it.

**5. `00390F20` `BattleFormula_ApplyTargetStatusActionPostModifiers` (679 B), after every committed list.** Called once at `003863F8`, outside the stop-flag test; `rdi` = target stats, `rsi` = ctx. No draws, no constants beyond the masks below. Layer ids read from the **target's raw** layers (`+0x68` mutable, `+0x78` augment), never the merged context.

```
loss = [02AEE004]                                           ; 00390F36 (target HP loss, -1 = none)
if (has(target,58) && loss != -1) {                         ; 00390F2F/00390F42 (+0x6F/+0x7F bit 2), 00390F48
    q = loss / 20                                           ; 00390F54-00390F6D (0x66666667, sar 3, trunc toward 0)
    [02AEE014] = min(([02AEE014] == -1 ? 0 : [02AEE014]) + q, 9999)   ; 00390F4E-00390F85 (source HP loss, cmovg)
}
if (has(target,48) && [02AEDFD4] != 0xB3 && loss != -1)     ; 00390F8B-00390F9A (+0x6E/+0x7E bit 0), 00390F9C, 00390FA8
    [02AEE004] = loss * 7 / 10                              ; 00390FAE-00390FC3 (trunc toward 0)
row = actionRow([02AEDFD4])                                 ; [02EBF138] + id * u16[+8], via 0020E600
if (has(target,55) && (row.u32[+0x0C] & 0x4000)) goto VOID  ; 00390FCB-00390FD3 (+0x6E/+0x7E bit 7), 00391076
if (has(target,56) && (row.u32[+0x0C] & 0x2000)) goto VOID  ; 00390FDC-00390FE6 (+0x6F/+0x7F bit 0), 003910C3
if (row.u16[+0x2C] & 0x400) {                               ; 0039110D-00391116
    w = target[+0x64] | target[+0x3C]
    if ((w & 0x10) && !(target[+0x3C] & 0x10)) result[+0x58] |= 0x10   ; 00391118-0039112D (Sleep)
    if ((w & 0x20) && !(target[+0x3C] & 0x20)) result[+0x58] |= 0x20   ; 00391138-0039114D (Confuse)
}
if (row.u16[+0x2C] & 0x800) {                               ; 0039118D-00391196
    if (bit24(w) && !bit24(target[+0x3C])) result[+0x58] |= 0x1000000   ; 00391198-003911B0 (Invisible)
}
return
VOID: [02AEE004] = -1; [02AEE008] = -1; [02AEDFB8] = 1; result[+4] = 7; return    ; 00391083-003910A5
```

- **Layer id 58** (no augment description; no equipment carries it): the target reflects 1/20 of the HP damage to the attacker as source HP loss, capped 9,999. It is computed from the uncut loss, before id 48.
- **Layer id 48** (no augment description): HP damage to the target × 7/10, except action `0xB3` (1000 Needles, recipe 59).
- **Paling (55) / Magick Shield (56)**: an action whose row `+0x0C` has bit 14 (physical) / bit 13 (magick) is voided into kind 7. The void clears the target HP loss and gain words only, so a recoil already added to `02AEE014` by id 58 **stands** on a voided hit; MP words are untouched; the remove-mask stage is skipped.
- **Action row word `+0x2C` bits 10 and 11** (= byte `+0x2D` bits 2 and 3): wake from Sleep and clear Confuse (bit 10), clear Invisible (bit 11), each only when the status sits in the target's status word 1 (`+0x64`) and not in word 2 (`+0x3C`). Result `+0x58` is the remove mask the applier reads. The shipped *Attack* row (`0x96`) carries word `0x6428`: bit 10 set, bit 11 clear, and `+0x0C` = `0x0C16408C` (bit 14 set).

**Worked examples.** Levels and Speed are illustrative; weapon bytes are shipped.

| case | inputs | arithmetic | odds |
|---|---|---|---|
| knockback | level-20 attacker with Broadsword (`+0x1B` 10) vs level-20 foe | `max(0, 10 + U[0,19] − U[0,19])`, then `mt()%100 < chance` | mean **10.4 %** (e.g. draws 7 / 12 → chance 5 → 5 %) |
| knockback | same weapon, level 50 vs level 10 | `10 + U[0,49] − U[0,9]`, never below 1 | mean **30.0 %** |
| knockback | same weapon, level 10 vs level 50 | mostly floored at 0 | mean **2.3 %** |
| knockback | Kotetsu (`+0x1B` 0), level 30 vs 30 | `max(0, U[0,29] − U[0,29])` | mean **5.0 %**; zero if the target has layer id 0 |
| counter | engaged target, Speed 30 (illustrative), Battle Harness (id 6) | `30 >> 1` | **15 %**, applied only when the hit is evaded through band A or B |
| counter | same, plus Genji Armor (id 7) | `30 × 2` | **60 %**; Speed 31 alone with id 6 still gives 15 |
| combo | Kotetsu (`+0x1C` 20), no id 13 | `trunc(20 × 0.7f)` | **14 %** |
| combo | Kotetsu with Genji Gloves (id 13) | `trunc(20 × 1.8f)` | **36 %** |
| combo | Broadsword (`+0x1C` 5) / with Genji Gloves | `trunc(3.5)` / `trunc(9.0)` | **3 %** / **9 %** |
| ×2 roll (slot 29) | Shortbow (`+0x1C` 5); Bowgun (7) | `mt()%100 < 5`; `< 7` | **5 %** / **7 %** chance of `02AEE054 × 2.0` (Genji Gloves no help) |
| post-modifier | target with ids 48 and 58 takes `02AEE004 = 1000` from Attack | recoil `1000/20 = 50` → `02AEE014`; loss `1000 × 7/10` | target loses **700**, attacker **50** |
| post-modifier | same, target also under Paling (55) | Attack `+0x0C` bit 14 → VOID | target loses **0** (kind 7), attacker still **50** |

**Draw accounting per resolution (MT19937 stream).** Slot 5: two draws (source then target); slot 6: one, unless the target has layer id 0; slot 7: none; slot 8: one, only on an engaged target; slot 9: none; slot 10: one when the combo counter is 0, plus the extra-hit loop; slot 29: one, always; `00390F20`: none. All five compare `mt() % 100` (or `% level`) as **unsigned and strict** (`roll < chance`); with `2^32 mod 100 = 96`, the modulo bias is below 3 × 10⁻⁸ per percent.
