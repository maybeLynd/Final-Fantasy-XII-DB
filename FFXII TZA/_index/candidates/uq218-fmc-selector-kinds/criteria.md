# UQ-218: what `0x0B`'s selector kinds 1, 2, `0x20`, `0x21`, `0x24` and `0x25` choose by (FABLE, Claude Opus 5.5, 2026-09-29)

affected: `17-Presentation-Rendering/Authored-Commands/the-authored-presentation-command-handlers.md` (the selectors paragraph, "What
those other kinds decide by is not read")

This follows [`README.md`](README.md), which covers S1–S4 and kind `0x10`. [`selector_criteria.py`](selector_criteria.py)
([output](selector_criteria.out)) runs N, Q, K1, K2 and Y, FAILS 0. It is static, on the certified image.

- **N: how `0x0B` treats the answer.** −1 means "no change" (`00417262`). Otherwise the low half is the list index and the
  high half the track offset.
- **Q: the two flags the selectors ask for.** They come from the battle unit's view request `0031ADB0`:
  - query bit `0x10` answers "may the combo continue" (`0030C010`, the force-fight page's combo predicate);
  - query bit `0x20` answers "the unit's primary target evaded or absorbed its last action, and no knockback was rolled".
    That is target-entry code 2–5 or 7, which is result kinds 1–4 (band A/B evade, plain or with parry) or 7 (absorbed by
    a defensive layer).
- **K1: kind 1 is a random variant that can turn into its "evaded" pair.** (`00422420`, verified end-to-end
  2026-09-29.)
  - The selector state record is `qword[ctx+0x2E0]` — one of `0xA0` records × `0x740` in pool `[02B3EF28]` (pool init
    `004269A0` → `0041F730`: `memset(0x740)` then `word[+0x40F] = 0xFFFF`).
  - `+0x40E` is the arm timer, `+0x411` the drawn variant. First call after reset (`+0x40E == 0`) draws *r* in 0..4
    with `003A6E60(5)` → `+0x411`, arms `+0x40E = frameLimit` (`01DFE0B4`), returns *r*.
  - Each later call increments `+0x40E` (saturating at `0x64`); on the single pass where `+0x40E` equals
    `11 × frameLimit` it queries `0x20` via `0041F2F0` and if the absorbed/evaded bit (`out+?` bit 4) is set adds 5
    to `+0x411` and returns it.
  - Every other call returns −1.
- **K2: kind 2 is a sticky three-way follow-up.** (`00422500`, verified end-to-end 2026-09-29.) `+0x410` is the
  choice (`0xFF` = undecided, from the init's `word[+0x40F] = 0xFFFF`), `+0x40E` re-used as the combo-age counter:
  - undecided + query-`0x30` bit 2 (combo may continue): `+0x40E++` (clamped to `frameLimit` once past
    `3 × frameLimit`), `+0x410 = 0`;
  - undecided + bit 4 (evaded/absorbed): `+0x40E = 0`, `+0x410 = 1`;
  - otherwise `+0x40E = 0`, `+0x410 = 2`.
  - Later calls return `+0x410` unchanged — sticky until the record re-inits or a new `@FMC` binds.
- **State-byte resets (2026-09-29, verified):** the bytes live in the `0x740`-record, not on `obj`. Two external
  reset sites: the pool/record init `0041F730` (callers `004269C3`/`00427A13`/`00429291` — `memset 0x740`,
  `word[+0x40F] = 0xFFFF` ⇒ `+0x40E`/`+0x411` = 0, `+0x410` = `0xFF`; `ebp`-fill `0xFFFFFFFF` ⇒ `+0x412` = `0xFF`,
  `+0x2AF` = `0xFF`, `+0x408`/`+0x24C` = `0xFFFF`, `+0x288`/`+0xC4`/`+0xC8`/`+0x2C4`/`+0x434` = `−1`); and the
  `@FMC`-bind body containing `004252A7` (the `00409FA0`/`00409FD0` `'@FMC'`/`'@FRP'` name-query path inside
  `004250AC`'s function) which zeroes `+0x40E` and sets `+0x412 = 0xFF` on every new motion block. No external
  writer touches `+0x410` (kind-2's stick survives a rebind until the record is re-initialised) or `+0x411`
  (gated by `+0x40E`). Kind-`0x10`'s `+0x412` is `004225A0`'s own byte: `0xFF` → roll
  `((rand % (ctx+0x2DE − ctx+0x2DD + 1)) + ctx+0x2DD − 1) × frameLimit` into it; `0` → re-arm `0xFF` and return 1;
  otherwise returns the stored byte.
- **Y: the yaw family.** Each takes the yaw to a point in degrees:
  - `0x20` answers "is the target within ±90°", 0 or 1.
  - `0x21` gives 0 within ±60°, otherwise 1 or 2 by the yaw's sign. A coin adds 3.
  - `0x24` gives four quadrants at ±45° and ±135°, stored in record `+0x2AF`. A coin adds 4.
  - `0x25` gives four quadrants at 0° and ±90°, measured toward the actor named by record `+0x18` (0 when it does not
    resolve).

  Record `+0x2AF` is the byte that command `0x1A`'s mode `0xA` tests
  ([how an animation moves and turns a character](../../../06-Movement-And-Navigation/how-an-animation-moves-and-turns-a-character-toward-its-target.md)).

**Still open:**
- ~~Kinds 0, `0xA` and `0xB`: the locomotion classifier `004256E0`~~ — resolved by
  [`classifier.md`](classifier.md) (same date; geometry, availability gating and fallback verified, `classifier.py`
  FAILS 0; folded into the motion page 2026-09-29). Each band's exact human-readable name is inference — the `.ca`
  `@FMN` locomotion set (`idle`, `walk_f`, `run`, `walk_l`, `walk_r`, `walk_b`, `stp`, `run_l`, `run_r` in `_l`/`_r`
  pairs) is a positional match but not a code-proven binding.
- Which sign of the yaw is the character's left.
- ~~Where the kind-1 and kind-2 state bytes are reset.~~ — resolved above (record init `0041F730` + the
  `@FMC`-bind site `004252A7`; `+0x410`/`+0x411` have no external reset).

| consumer | action | agreement |
|---|---|---|
| handler page, "What those other kinds decide by is not read" | struck for kinds 1, 2 and the yaw family; classifier resolved by `classifier.md`, folded into the motion page | revised-here |
| `README.md` (this folder), "Still open, exactly" | narrowed by this file; that text stays as dated history | agrees |
| UQ-218 register row (SWE2-DATA's) and FABLE-REQ-DATA-UQ218-FMC-CROSSWALK | the `@FMC` residue narrows to the classifier's bands | routed-to-FABLE-REQ-DATA-UQ218-FMC-CROSSWALK |

Regression: selector_criteria.py N Q K1 K2 Y. Y models each band with its boundary cases, and N rejects "−1 plays entry 0".
run: selector_criteria.py at 6be90c7ee, FAILS 0.
