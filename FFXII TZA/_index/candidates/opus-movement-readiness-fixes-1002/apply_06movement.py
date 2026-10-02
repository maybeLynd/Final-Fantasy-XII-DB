"""apply_06movement.py [--apply] - 06-Movement-And-Navigation readiness map (cloud-reports/re-readiness/06-movement.md),
section 2.3 A value contradictions C-V01..C-V43 decided at the bytes, and the section 2.3 B stale / banner / count items,
settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the shipping image refutes) and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* with the deciding address, or, for a stale "not read / open" claim answered elsewhere,
*(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Two pre-existing spans that crossed a
line (3DF section 7, bit 0) are closed per line where an edit touches them, the struck text unchanged.
Code-block lines get a trailing `<- corrected 2026-10-02, OPUS - ...` comment in the block's own comment syntax instead of
a strike (their OLD includes the line end, so NEW never contains OLD). No front-matter edits; no heading changes.
Verdicts and deciding addresses: scratchpad mv06/verdicts-06.md (OPUS's 30 and the verifier's 10, 2026-10-02).
Left out: C-V25's and C-V39's right sides need nothing; C-S16 (two labelled measures, both true: 10 direct callers,
7 A-measured), C-S18 (census field counts, not one function's bytes), C-S22 (role names of nav-shape bodies, unread
here), C-S25 (both readings agree on the bytes), C-S26 (both clamps write 022D9198 and the workbench 022D92A0..; the
two ranges are consistent), the NAV front-matter note (a YAML plain scalar), the POOL `#` title (C-S20) and the
README's missing page list.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "06-Movement-And-Navigation/"
README = F + "README.md"
HSD = F + "heading-speed-to-position-delta.md"
CHSD = F + "CONTRACT-heading-speed-to-position-delta.md"
CFS = F + "CONTRACT-facing-and-steering.md"
TURN = F + "Facing-And-Steering/how-a-character-turns.md"
SLOTS = F + "Facing-And-Steering/the-two-steering-slots-and-what-a-character-resumes.md"
MODE = F + "Movement-Mode-Selection/setting-the-movement-mode-and-which-way-a-character-turns.md"
TDF = F + "Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md"
LOCO = F + "Battle-Locomotion/battle-locomotion-steering-and-recovery.md"
CTL = F + "CONTRACT-battle-locomotion-turn-limiter.md"
CCQ = F + "CONTRACT-corridor-query-family.md"
NAV = F + "how-a-unit-finds-its-way-across-the-navigation-mesh.md"
CNAV = F + "CONTRACT-navigation-search-and-follow.md"
POOL = F + "the-movement-body-pool-and-the-separation-pass.md"
CPOOL = F + "CONTRACT-movement-body-pool.md"
CSEP = F + "CONTRACT-separation-pass.md"
ANIM = F + "how-an-animation-moves-and-turns-a-character-toward-its-target.md"
CLAMP = F + "clamping-a-point-into-a-volume.md"
SHAPE = F + "the-unit-shape-distance-primitives.md"

C = "*(corrected 2026-10-02, OPUS: "
WRAP = "`0026A8E6` `comiss` / `jb` takes the bias `[00915620]` (`-π`) for a negative angle, else `[01CEBC50]` (`+π`)"
LOCO_LINK = "[battle locomotion](Battle-Locomotion/battle-locomotion-steering-and-recovery.md)"

EDITS = [
    # C-V01: the sign-biased truncating wrap is [-pi, pi] with the endpoints swapping (0026A8E6-0026A93B; 0026A870 and
    #        0026AC70 the same).
    (HSD, "Both angles are first wrapped into `(-π, π]` by the truncating-`fmod` idiom described in §4.",
     "Both angles are first wrapped into ~~`(-π, π]`~~ `[-π, π]`, an exact `+π` becoming `-π` and `-π` becoming `+π`, "
     + C + WRAP + ", then truncates at `0026A90E`–`0026A93B`; the contract's LD-6)* by the truncating-`fmod` idiom "
     "described in §4."),
    (HSD, "**Angle wrap into `(-π, π]`** — used identically",
     "**Angle wrap into ~~`(-π, π]`~~ `[-π, π]`, the endpoints swapping** " + C + WRAP + "; `+π` maps to `-π` and "
     "`-π` to `+π`)* — used identically"),
    (TURN, "makes the result land in (−π, +π] rather than [0, 2π).**",
     "makes the result land in ~~(−π, +π]~~ [−π, +π] rather than [0, 2π).** " + C + WRAP + "; [−π, +π) for a "
     "non-negative input and (−π, +π] for a negative one, so `+π` lands on `−π` and `−π` on `+π`)*"),
    (CFS, "`[-pi, pi)`; the result lands at",
     "~~`[-pi, pi)`~~ `[-pi, pi]` — `[-pi, pi)` for a non-negative input and `(-pi, pi]` for a negative one " + C
     + "`0026A8E6` `comiss` / `jb` selects the bias by sign; `0026A876`–`0026A8CB` the same in `0026A870`)*; the "
     "result lands at"),
    (MODE, "bias un-added - an exact `(-π, π]` normalize - and the result tails into",
     "bias un-added - an exact ~~`(-π, π]`~~ `[-π, π]` normalize, `+π` and `-π` swapping " + C + "`0026AC7E`–"
     "`0026ACC5`, the sign-biased truncation of `0026A8E0`)* - and the result tails into"),

    # C-V02: 003A1C50 is closed at both ends (003A1C58 / 003A1C76 return an exact -pi or +pi unchanged).
    (MODE, "call  0x3A1C50                           ; wrap into (-pi, pi]\n",
     "call  0x3A1C50                           ; wrap into (-pi, pi]   ; <- corrected 2026-10-02, OPUS - closed "
     "[-pi, pi]: 003A1C58 and 003A1C76 return an exact -pi or +pi unchanged\n"),
    (MODE, "because the difference is wrapped into (−π, π] before its sign is taken.**",
     "because the difference is wrapped into ~~(−π, π]~~ [−π, π] before its sign is taken.** " + C + "`003A1C50` is "
     "closed at both ends — `003A1C58` and `003A1C76` leave an exact `−π` or `+π` unchanged)*"),
    (MODE, "| `003A1C50` | the angle normaliser into (−π, π] | §5 |",
     "| `003A1C50` | the angle normaliser into ~~(−π, π]~~ [−π, π] " + C + "`003A1C58` / `003A1C76`)* | §5 |"),
    (MODE, "so the result is closed at `+π` and open\nat `-π` — which is what §5's \"(−π, π]\" says.",
     "so the result is closed at `+π` and ~~open~~ closed\n~~at `-π` — which is what §5's \"(−π, π]\" says.~~ at `-π` "
     "too: an input of exactly `-π` fails `-π > x`, skips both loops and is returned unchanged, so §5's \"(−π, π]\" is "
     "wrong " + C + "`003A1C58` `comiss xmm1(-π), xmm0` / `jbe` skips the `+2π` loop, `003A1C76` `comiss xmm0, "
     "xmm1(+π)` / `jbe` returns)*."),

    # C-V03: 0033CB70 loops only when abs(x) <= 4pi; above that it takes one truncating division and returns.
    (HSD, "division, and then it **loops** — `addss −2pi` while `x > pi`",
     "division ~~, and then it **loops**~~ and returns without a loop, leaving a result in `(−2pi, 2pi)` "
     "(`0033CBCD`–`0033CBEF`); only an input within `±4pi` **loops** " + C + "`0033CB73` / `0033CB84` jump to "
     "`0033CBCD` beyond `±4pi`)* — `addss −2pi` while `x > pi`"),
    (LOCO, "normalises an angle into (−π, π] by repeated addition",
     "normalises an angle into ~~(−π, π] by repeated addition~~ [−π, π] by repeated addition of ±2π when it lies "
     "within ±4π, and beyond that by one truncating division with no loop, which can leave a result in (−2π, 2π) " + C
     + "`0033CB73` / `0033CB84` against `[00D10B0C]` / `[00D10B20]` (±4π), loops `0033CBA0` / `0033CBC0`, division "
     "`0033CBCD`–`0033CBEF`)*"),

    # C-V04: 0026B5A0's bias is h >= 0 ? +pi : -pi (0026B5B4 / 0026B5B7 jb -> 0026B5C3 [00915620]).
    (CFS, "`comiss xmm6, 0` selects `xmm1 = [01CEBC50]` (a `+pi`-class constant) when the\n"
          "input is negative, else `[00915620]` (`-pi`-class), `addss` the correction,",
     "`comiss xmm6, 0` selects ~~`xmm1 = [01CEBC50]` (a `+pi`-class constant)~~ `xmm1 = [00915620]` (`-pi`) when the\n"
     "input is negative, else ~~`[00915620]` (`-pi`-class)~~ `[01CEBC50]` (`+pi`) " + C + "`0026B5B4` `comiss "
     "xmm6, 0` / `0026B5B7` `jb` → `0026B5C3` `movss xmm1, [00915620]`; otherwise `0026B5B9` `[01CEBC50]`; the "
     "bias is `h >= 0 ? +pi : -pi`, as §12 states)*, `addss` the correction,"),

    # C-V05 + C-V08: commit flag 0 also copies the old triple to +0x250..+0x258 when it changed; lane 0 is the +0xAC
    #        pitch (002E5FBA -> 002E5F4F -> 003EC348; 00420C00 -> 0046D380 rotates it about X).
    (CFS, "block: flag **0** stages the new `{rate, heading, 0}` triple into the steering slot's",
     "block: flag **0** stages the new ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple " + C + "lane 0 is "
     "context `+0xAC`, the pitch — `002E5FBA` loads it, `002E5F4F` passes it, `003EC348` stores it at `+0x120`, and "
     "`00420C00` → `0046D380` turns that lane into the rotation about X)* into the steering slot's"),
    (CFS, "`+0x120`–`+0x128` and returns; flag **1** additionally shifts",
     "`+0x120`–`+0x128` ~~and returns~~, after copying the old triple to `+0x250`–`+0x258` when it changed, and "
     "returns " + C + "`003EC316`–`003EC358` run before the flag test at `003EC362`)*; flag **1** additionally shifts"),
    (CFS, "`xmm2 = context[+0xAC]` (the prior rate, handed back unchanged)",
     "`xmm2 = context[+0xAC]` (~~the prior rate~~ the pitch, handed back unchanged " + C + "`002E5E88` stores it "
     "back to `+0xAC`, `003EC348` puts it in render lane `+0x120`, which `0046D380` rotates about X)*)"),
    (CFS, "`003EC260(word[record], prior_rate, heading, 0, flag!=0)` |",
     "~~`003EC260(word[record], prior_rate, heading, 0, flag!=0)`~~ `003EC260(word[record], pitch, heading, 0, "
     "flag!=0)` " + C + "`002E5F4F` `movaps xmm1, xmm8`, the `+0xAC` pitch)* |"),
    # C-V05 + C-V06 + C-V08 on one table row: and-then, not or (003EC39E then 003EC3A3-003EC3BC).
    (CFS, "0 stages the `{rate, heading, 0}` triple into slot `+0x120`–`+0x128`; 1 additionally shifts it to "
          "`+0x250`–`+0x258` and calls `004288B0(slot,-1)` or `003B3CA0([slot+0x288],0x1E)`",
     "0 stages the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple into slot `+0x120`–`+0x128`, copying the "
     "old triple to `+0x250`–`+0x258` when it changed; 1 additionally shifts it to `+0x250`–`+0x258` and calls "
     "`004288B0(slot,-1)` (unless `+0x284` bit 17 is set) ~~or~~ and then `003B3CA0([slot+0x288],0x1E)` when "
     "`+0x288 != -1` " + C + "`003EC316`–`003EC358` before the flag test; `003EC368`–`003EC39E`, then "
     "`003EC3A3`–`003EC3BC`)*"),
    (CFS, "stages the `{rate, heading, 0}` triple only; `0026B620` (flag 1) stages and",
     "stages the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple " + C + "lane 0 is the `+0xAC` pitch, "
     "`002E5F4F` → `003EC348`)* only; `0026B620` (flag 1) stages and"),
    (CFS, "commits through `004288B0` or `003B3CA0`.",
     "commits through `004288B0` ~~or~~ and then `003B3CA0` " + C + "`003EC39E`, then `003EC3A3`–`003EC3BC`)*."),
    (TURN, "Variant0 **stages** the `{rate, heading, 0}` triple;",
     "Variant0 **stages** the ~~`{rate, heading, 0}`~~ `{pitch, heading, 0}` triple " + C + "lane 0 is context "
     "`+0xAC`, `002E5FBA` → `002E5F4F` → `003EC348`)*;"),

    # C-V07: the reset arm needs word +6 != -1 (and +0x284 bit 27 clear); 003EC2AA-003EC2D5.
    (HSD, "with `+0x290` bit 20 clear and word `+6 == -1` it zeroes the",
     "with `+0x290` bit 20 clear and word ~~`+6 == -1`~~ `+6 != -1` (and `+0x284` bit 27 clear; with that bit set "
     "such a record returns untouched) " + C + "`003EC2AA`–`003EC2BB`, then `003EC2C1` `cmp word [rbx+6], -1` / `je` "
     "to the staging path; the reset `003EC2C8`–`003EC2D5` runs only for `+6 != -1`)* it zeroes the"),

    # C-V09: the +0x58 / +0x5C stamps are in the mode 2-3 block (0026C16A jle 0026C1E6).
    (TURN, "through `003A1C50`, set/clear `byte[obj+0x62]` bit `0x40` on the sign, and arm-4",
     "through `003A1C50`, set/clear `byte[obj+0x62]` bit `0x40` on the sign, and ~~arm-4~~ the mode 2–3 arm " + C
     + "`0026C167` `cmp edx, 3` / `0026C16A` `jle 0026C1E6`; the stores `0026C224` / `0026C237` are in that block, "
     "while mode 4 calls `0026B620` and clears `+0x28`)*"),

    # C-V10: only mode 0 reaches 002E6300; mode 1, negatives and modes above 4 take the epilogue.
    (TURN, "`002EBE50` + `002E8EE0`; `edx <= 1` falls to `002E6300(rec, rbx, sil)`.",
     "`002EBE50` + `002E8EE0` (when `+0x65` is set) ~~; `edx <= 1` falls to `002E6300(rec, rbx, sil)`.~~ and then "
     "`002E6300(rec, rbx, sil)` (`0026C26D`); `edx == 1`, negative modes and modes above 4 go straight to the epilogue "
     + C + "`0026C156` `je 0026C244` for 0 only, `0026C15E` `cmp edx, 1` / `0026C161` `jle 0026C272`, `0026C16F` "
     "`jne 0026C272`)*."),

    # C-V12: 002EBE50 runs 003A1C50 as the two-loop wrap, no absolute value.
    (TURN, "(fabsf-shaped) at",
     "~~(fabsf-shaped)~~ (the two-loop wrap into `[-pi, pi]`, no absolute value " + C + "`002EBEC3`–`002EBED0` and "
     "`002EBEE5`–`002EBEF2` call `003A1C50` on the signed difference)*) at"),

    # C-V13: op 4 pops on +0xB bit 4; op 2 does not pop (00263059 / 0026305E / 00263063).
    (SLOTS, "drives: **op 2** pops when",
     "drives: **~~op 2~~ op 4** pops " + C + "`00263059` `sub edx, 1` (op 1), `0026305E` `sub edx, 2` (op 3), "
     "`00263063` `cmp edx, 1` / `jne 0026321C` leaves op 2 without a pop; op 4 tests `+0xB` bit 4 at `0026306C`)* when"),

    # C-V14: 002651C0 selects class 1 / class 3.
    (SLOTS, "selected by kind 1/2;",
     "selected by kind ~~1/2~~ 1/3 " + C + "`002651C7` `sub edx, 1` / `je` class 1, `002651CC` `cmp edx, 2` / `je` "
     "class 3)*;"),

    # C-V15: 003A19C0's planar magnitude is sqrt(dz^2 + dx^2).
    (TURN, "square-roots `dy^2 + dx^2` for",
     "square-roots ~~`dy^2 + dx^2`~~ `dz^2 + dx^2` " + C + "`003A1A02`–`003A1A12` square `xmm7` and `xmm8`, the z "
     "and x lanes)* for"),

    # C-V16: the stall constants are thresholds, not steps (0033C2B7-0033C2ED; AM-4).
    (LOCO, "compares remaining path distance, decrements by **0.01**, adds **1.5**, and tests a counter against",
     "compares remaining path distance ~~, decrements by **0.01**, adds **1.5**,~~ with the stored one — a drop of "
     "more than **0.01** re-stores it and zeroes the counter, a rise past it **+ 1.5** re-stores it, anything else "
     "counts up " + C + "`0033C2B7`–`0033C2C9`, `0033C2CF`–`0033C2DC`, `0033C2E3`–`0033C2ED`; AM-4)* — and tests a "
     "counter against"),
    (LOCO, "distance stepped by -0.01, +1.5\n",
     "distance stepped by -0.01, +1.5   <- corrected 2026-10-02, OPUS - thresholds, not steps: a drop below old - "
     "0.01 or a rise above old + 1.5 re-stores the distance (0033C2B7-0033C2DC)\n"),

    # C-V17: the decoder takes 0x4000-0x4024 by switch, the band 0x4026-0x4035 and five higher ids.
    (LOCO, "at **`0x4000`-`0x4024`** (37 ids), and switches to **six** goal-resolution bodies,",
     "at ~~**`0x4000`-`0x4024`** (37 ids), and switches to~~ `0x4035` with five higher ids beside it, and switches its "
     "low band **`0x4000`-`0x4024`** (37 ids) to **six** goal-resolution bodies " + C + "`00312780` `cmp ebx, 0x4035` "
     "/ `ja` the ids `0x4124`, `0x4125`, `0x414A`, `0x414E`, `0x4165`; `0031278C` `cmp ebx, 0x4026` / `jae` the band "
     "`0x4026`–`0x4035`; `00312798`–`003127A1` the switch, `0x4025` rejected)*,"),
    (LOCO, "Movement bounds at `0x4024`, and the action table's",
     "Movement ~~bounds at `0x4024`~~ bounds its switch at `0x4024`, the decoder also taking `0x4026`–`0x4035` and "
     "five higher ids " + C + "`0031279E` `cmp ecx, 0x24`; `00312780`, `0031278C`)*, and the action table's"),

    # C-V18: 0x4020 samples around the SpawnRecord's +0x50 ([unit+0x6A0], 003127F1 / 003127FB).
    (LOCO, "`0x4020` samples around the actor record's `+0x50`",
     "`0x4020` samples around the ~~actor record's~~ SpawnRecord's (`[unit+0x6A0]`) `+0x50` " + C + "`003127F1` "
     "`mov rcx, [rdi+0x6A0]` / `003127FB` `add rcx, 0x50`)*"),

    # C-V19: 0x4125's 20 is the +-parameter around the unit's own +0xD0 (00312A50 / 00312A57).
    (LOCO, "— reference position **20** (`00312A50`–`00312A8F`)",
     "— ~~reference position **20**~~ around the unit's own `+0xD0` within **±20**, the parameter " + C
     + "`00312A50` `lea rcx, [rdi+0xD0]` is the reference, `00312A57` `mov r8d, 0x14` the third argument)* "
     "(`00312A50`–`00312A8F`)"),
    (LOCO, "and of `0x4125` (which samples around reference 20)",
     "and of `0x4125` (which samples around ~~reference 20~~ the unit's own `+0xD0` within ±20 " + C + "`00312A50`–"
     "`00312A57`)*)"),

    # C-V20: speed = (A > v) ? A : min(B, v) (00339DA8-00339DC0).
    (LOCO, "    speed = (st->[0xF8] > v) ? v : min(st->[0xFC], v);\n",
     "    speed = (st->[0xF8] > v) ? v : min(st->[0xFC], v);   /* <- corrected 2026-10-02, OPUS - (st->[0xF8] > v) "
     "? st->[0xF8] : min(st->[0xFC], v): 00339DA8 loads A, 00339DBB ja keeps it, 00339DBD-00339DC0 min(B, v) */\n"),

    # C-V21: the latched step above 120 deg has no wrap and no snap (0033659D-0033661D).
    (LOCO, "    d = Angle_NormalizeRadiansPi(desired - cur);\n",
     "    d = Angle_NormalizeRadiansPi(desired - cur);   /* <- corrected 2026-10-02, OPUS - not on the latched path: "
     "above 120 deg with fl[0x21] & 6 set, 0033659D-0033661D step cur +/- rate with no wrap and no snap */\n"),
    (CTL, "**BL-6 — Arrival SNAPS, and the snap is what clears the loop.** When the remaining delta is within",
     "**BL-6 — Arrival SNAPS, and the snap is what clears the loop.** When ~~the remaining delta is within~~ the step "
     "is not a latched one (a latched direction is read only above 120°) and the remaining delta is within " + C
     + "`0033654E` / `0033655F` split at 120°; above it `0033659D` reads `fl[0x21] & 6` and `003365FF`–`0033661D` "
     "step `cur ± rate` with no wrap and no snap, the 2026-09-23 closure below)*"),

    # C-V22: mode 3 is a constant step (003EC12E-003EC1E1); 002654E0 is the mode-3 arm's flag (002E596B).
    (MODE, "along the curve `003EC040(target, +0x78, …)`",
     "~~along the curve~~ by the constant step of `003EC040(target, +0x78, …)` " + C + "`003EC12E`–`003EC15A` "
     "step = `[01DFE0BC]` × `[rec+0x28]` or × `[rec+0x24]`; `003EC1C3` snaps within one step; SD-193)*"),
    (MODE, "003A1AD0 (approach), 003EC040 (mode-3 curve),\n",
     "003A1AD0 (approach), 003EC040 (mode-3 curve),   <- corrected 2026-10-02, OPUS - a constant angular step, not a "
     "curve (003EC12E-003EC1E1, SD-193)\n"),
    (MODE, "| the mode-4 curve-eligibility flag —",
     "| the ~~mode-4 curve-eligibility flag~~ mode-3 flag that picks the render-step path " + C + "its one caller "
     "`002E596B` is in `002E5750`'s mode-3 arm, reached by the third `sub edi, 1` at `002E583C` / `002E583F`; mode 4 "
     "is `002E5862`)* —"),

    # C-V23 + C-V24: per-fifty scale (003DAF68 [008F3130] = 50.0); class 3 takes the +0x104..+0x106 bytes, every other
    #        kind 37 / 50 / 37 (0026846F-00268496); the class-3 arms are r8d / ecx == 2 after sub 1.
    (POOL, "then `a % × +0xF0`, `c % × +0xF4`, `b % × +0xE0 + +0xE4` — 37 / 37 / 50 for the party class `0x60`, else "
           "the secondary context's bytes `+0x104`–`+0x106`",
     "then ~~`a % × +0xF0`, `c % × +0xF4`, `b % × +0xE0 + +0xE4`~~ `a × +0xF0 / 50`, `c × +0xF4 / 50`, "
     "`b × +0xE0 / 50 + +0xE4` — ~~37 / 37 / 50 for the party class `0x60`, else the secondary context's bytes "
     "`+0x104`–`+0x106`~~ `a`, `b`, `c` = the `[+0xB8]` context's bytes `+0x104` / `+0x105` / `+0x106` for class 3 "
     "(`0x60`), else 37 / 50 / 37 " + C + "`003DAF68` loads `[008F3130]` = 50.0 and `003DAFB9`–`003DAFF4` divide by "
     "it; `0026846F`–`0026847C` set `0x25` / `0x32` / `0x25` when `(+3 & 0xE0) != 0x60`, `00268481`–`00268496` load "
     "the bytes otherwise)*"),
    (POOL, "| `+0xF8` heading | secondary `+0xA8` (class 2) or `+0x38` (class 1), else 0 |",
     "| `+0xF8` heading | secondary `+0xA8` (class ~~2~~ 3) or `+0x38` (class 1), else 0 " + C + "`0026843F` "
     "`sub ecx, 1` / `00268444` `cmp ecx, 2` selects class 3, the `0x60` kind)* |"),
    (POOL, "| `+0xE0` height | secondary `+0xC0 × +0x24` (class 2) or `+0x68` (class 1), else 0 |",
     "| `+0xE0` height | secondary `+0xC0 × +0x24` (class ~~2~~ 3) or `+0x68` (class 1), else 0 " + C + "`002683FD` "
     "`sub r8d, 1` / `00268403` `cmp r8d, 2` selects class 3)* |"),
    (CPOOL, "- **`00268380` sizes the shape only for kind 3** — `(record[+3] & 0xE0) == 0x60` at\n"
            "  `00268386`–`00268391`, and `0x60 >> 5` is 3.",
     "- **`00268380` ~~sizes the shape only for kind 3~~ reads the radius pair only for kind 3** — `(record[+3] & "
     "0xE0) == 0x60` at\n  `00268386`–`00268391`, and `0x60 >> 5` is 3 " + C + "that gate guards only the "
     "`003DA710` call; every kind with a body is sized — kind 1 from `+0x68` / `+0x38`, kind 3 from `+0xC0 × +0x24` / "
     "`+0xA8`, others 0 — and `003DAF20` runs for all of them, with 37 / 50 / 37 unless kind 3, "
     "`002683AD`–`002684FD`; EXP-087)*."),

    # C-V25: a zero weight yields fully; the mask clause is a separate override (00314E10, 00314F50).
    (POOL, "- **The weight decides who yields.** A zero weight (or a mask bit `00314E10` honours) makes a body\n"
           "  immovable; the other body takes the whole separation.",
     "- **The weight decides who yields.** ~~A zero weight (or a mask bit `00314E10` honours) makes a body~~ A mask "
     "bit `00314E10` honours makes a body\n  immovable; the other body takes the whole separation. A zero weight does "
     "the opposite: with `wA = 0` and `wB > 0`, `w = wB / (wA + wB)` is 1 and the zero-weight body takes the whole "
     "separation, and two zero weights split it evenly " + C + "`00315017` / `0031502A` load the weights, "
     "`0031506A`–`0031506E` replace two zeros with 1.0, `00314E16`–`00314E27` form `w`, `003152BA` → `0031530F` give "
     "A `w × separation`; a mask hit returns 0 at `00314E83`)*."),

    # C-V26: the free-list head is 02B57CC4 (02B525C4 has no reference).
    (POOL, "| `02B525C4` / `02B57CC0` | — | 2 / 2 | free-list head / active-list head |",
     "| ~~`02B525C4`~~ `02B57CC4` / `02B57CC0` " + C + "`02B525C4` has no reference and lies inside the pool; "
     "`02B57CC4` is used by `003DA8A0`, `003DAD00`, `003DAE30` — the 2026-09-13 correction below)* | — | 2 / 2 | "
     "free-list head / active-list head |"),

    # C-V27 (+ O-07): the cell masks and the deferred list are 02B57CE0 and 02B57CC8 / 02B57CD0.
    (HSD, "ORs `1<<(id&0x3F)` into the `02AC7CE0` bucket array",
     "ORs `1<<(id&0x3F)` into the ~~`02AC7CE0`~~ `02B57CE0` bucket array " + C + "`02AC7CE0` has no reference; "
     "`02B57CE0` is used by `003DAA40`, `003DAAB0`, `003DAE30`, `003DB020`)*"),
    (HSD, "tail-appends the record to the `02AC7CC8`/`02AC7CD0` list via `003DB0D0`",
     "tail-appends the record to the ~~`02AC7CC8`/`02AC7CD0`~~ `02B57CC8`/`02B57CD0` list via `003DB0D0` " + C
     + "the `02AC7Cxx` pair has no reference; `02B57CC8` / `02B57CD0` are used by `003DAA20`, `003DAE30`, "
     "`003DB0D0`)*"),
    (HSD, "head `02AC7CC8` / tail `02AC7CD0`",
     "head ~~`02AC7CC8`~~ `02B57CC8` / tail ~~`02AC7CD0`~~ `02B57CD0` " + C + "the same references as the row "
     "above)*"),
    (TURN, "the `02AC7CC8` deferred-register tail",
     "the ~~`02AC7CC8`~~ `02B57CC8` " + C + "`02AC7CC8` has no reference; `02B57CC8` is the list head `003DB0D0` "
     "appends to)* deferred-register tail"),
    (POOL, "Recorded as\nunexplained rather than named.)*",
     "~~Recorded as~~\n~~unexplained rather than named.~~)* " + C + "they are the deferred-registration list's head "
     "and tail — `02B57CC8` is used by `003DAA20`, `003DAE20`, `003DAE30`, `003DB0D0` and `02B57CD0` by `003DAA20`, "
     "`003DAE30`, `003DB0D0`; `003DAE30` initialises them and `003DB0D0` appends — the list the heading page names "
     "`02AC7CC8` / `02AC7CD0`)*"),

    # C-V28: query mode stores the weight w, A's share (0031523C / 00315241 / 00315377).
    (POOL, "a mutual push, and the raw separation is written to `out` when the caller did not ask for a push",
     "a mutual push, and ~~the raw separation~~ A's share of it — the weight `w` from `00314E10` — is written to "
     "`out` when the caller did not ask for a push " + C + "`0031523C` `call 00314E10` / `00315241` `movaps xmm4, "
     "xmm0`, then `00315377` `movss [r15], xmm4`)*"),
    (CSEP, "writes the raw separation to `out` when the caller asked for no push.",
     "writes ~~the raw separation~~ A's share, the weight `w` from `00314E10`, to `out` when the caller asked for no "
     "push " + C + "`0031523C` `call 00314E10` / `00315241`, `00315377` `movss [r15], xmm4`)*."),
    (CSEP, "- What `00313F80`, the query-mode caller, uses the raw separation for.",
     "- What `00313F80`, the query-mode caller, uses ~~the raw separation~~ the weight `w` " + C + "`00315377` "
     "stores `w`, not a separation)* for."),

    # C-V29: the active-this-tick test is push mode only (00314FD2 / 00314FD4).
    (POOL, "`+0xF4` (`00314F97`–`00314FCC`), both are active this tick (`00314FD6`–`00314FE4`), their layer",
     "`+0xF4` (`00314F97`–`00314FCC`), ~~both are active this tick~~ in push mode both are active this tick "
     "(`00314FD6`–`00314FE4`) " + C + "`00314FD2` `test esi, esi` / `00314FD4` `je 00314FEA` skips both tests in query "
     "mode; the separation contract's P-4)*, their layer"),

    # C-V30: header +0xA is the region count (00383883 / 00383888).
    (NAV, "with `deg = w[root+0xA]` — the triangle count |",
     "with `deg = w[root+0xA]` — ~~the triangle count~~ the region count, §1's `regionCount` " + C + "`00383883` "
     "`movzx r10d, word [r11+0xA]` / `00383888` `imul r10d, ebx` make it the row stride of the region-by-region "
     "adjacency)* |"),

    # C-V31: portal bytes +4 gated, +5 map id, +6 class mask (003838C4 / 003838CC / 003838D3).
    (NAV, "`{w va, w vb, b +4, b class@+5, b flag@+6}`, at",
     "~~`{w va, w vb, b +4, b class@+5, b flag@+6}`~~ `{w va, w vb, b gated@+4, b mapId@+5, b classMask@+6}` " + C
     + "`003838C4` `test byte [rec+6], r8b` with `r8b = 1 << class`; `003838CC` `cmp byte [rec+4], 0xFF`; "
     "`003838D3` `movzx ecx, byte [rec+5]` → `0032A780`)*, at"),

    # C-V32: D5A0's fourth out lane is the horizontal distance (003DA663).
    (SHAPE, "ellA = A1D30(DA730(capA, posB, posA)), ellB symmetric; out = {posA - posB, 1.0};\n",
     "ellA = A1D30(DA730(capA, posB, posA)), ellB symmetric; out = {posA - posB, 1.0};   <- corrected 2026-10-02, "
     "OPUS - out.w is the horizontal distance sqrt(dz^2 + dx^2), not 1.0: 003DA663 overwrites the 1.0 stored at "
     "003DA62D-003DA63E\n"),

    # C-V34: the time base does leave 1 (001EDDC0: 2.0 / 0.5 / 2 when its argument is non-zero).
    (HSD, "missing. It does **not** show the triple ever being written away from `1.0` during play; the",
     "missing. ~~It does **not** show the triple ever being written away from `1.0` during play;~~ The image writes "
     "it away from `1.0`: `001EDDC0` stores 2.0, 0.5 and 2 into `01DFE0B8` / `01DFE0BC` / `01DFE0B4` when its "
     "argument is non-zero " + C + "`001EDDC4` `test ecx, ecx`, stores at `001EDDD8`, `001EDDE0`, `001EDDF2`; "
     "tail-jumped from `0022BDF0` at `0022BE7D`)*; the"),

    # C-V35: 02B40534 - three stores of 1, four of 0 (two through a zeroed register), one of the argument.
    (TDF, "| `02B40534` | **8** | `003B6ED0` and three others store `1`; **three store `0`**; two store a register |",
     "| `02B40534` | **8** | ~~`003B6ED0` and three others store `1`; **three store `0`**; two store a register~~ "
     "`003B6ED0`, `003B7BB0` and `003B7C60` store `1`; four store `0`, two of them through a zeroed register "
     "(`003B72F0`, `003B7E20`); `003B7E00` stores its argument " + C + "stores at `003B6ED7`, `003B6F37`, "
     "`003B7089`, `003B7308`, `003B7BCB`, `003B7CBE`, `003B7E00`, `003B7E4C`; BV-5)* |"),

    # C-V36: eight of the eleven +0x14F bit-0 readers refuse; the attach guard and the two presentation readers do not.
    (TDF, "~~every reader of bit 0\n        is a movement veto~~ **six of its eight readers are movement vetoes** — "
          "the two field-pass",
     "~~every reader of bit 0~~\n        ~~is a movement veto~~ ~~**six of its eight readers are movement "
     "vetoes**~~ **eight of its eleven readers refuse** — `00267260` (`00267286`) and the seven named next, while the "
     "attach guard `002E26F0` (`002E274A`, which detaches through `002E6B10`) and the two presentation readers below "
     "do not " + C + "every `+0x14F` bit-0 test in the image — `0025B637`, `0025B76F`, `00267286`, `002E506A`, "
     "`002E5776`, `002E602C`, `002E634B`, `002EA816` jump past their work; `002E274A`, `003B7812`, `003B7934` do "
     "not)* — the two field-pass"),

    # C-V37: the duration / move / turn windows and the curve index scale by the frame-rate word (003AF05A-003AF12F).
    (ANIM, "- the frame counter `+4` goes up; past `duration` the entry is unlinked and freed",
     "- the frame counter `+4` goes up; past ~~`duration`~~ `duration × [01DFE0B4]` " + C + "`003AF05A`–`003AF072` "
     "multiply by the frame-rate word before the compare; pass 1's A4)* the entry is unlinked and freed"),
    (ANIM, "- **while the counter is below `moveFrames`** and the move byte is set:",
     "- **while the counter is below ~~`moveFrames`~~ `moveFrames × [01DFE0B4]`** and the move byte is set " + C
     + "`003AF08A`–`003AF096`; `frame` below is counter / `[01DFE0B4]`, `003AF09E`–`003AF0A6`)*:"),
    (ANIM, "- **while it is below `turnFrames`** and the turn byte is set:",
     "- **while it is below ~~`turnFrames`~~ `turnFrames × [01DFE0B4]`** and the turn byte is set " + C
     + "`003AF10F`–`003AF11D`; `frame` is counter / `[01DFE0B4]`, `003AF12D`–`003AF12F`; the first accumulator's "
     "per-frame cap is `turnRate[frame] x scale` without the timebase, `003AF170`–`003AF17A`, the second's has it, "
     "`003AF1C0`–`003AF1CA`)*:"),

    # C-V38: one path passes a stack snapshot, not the unit (003019BF -> 0033A120 -> 00336710).
    (CCQ, "and every path passes `BattleUnit + 0x80` (`lea … + 0x80` at `0023406F`, `00308673`, `00317E9D`, "
          "`00325BC4`, `002FDC42`, `003048EF`, `003105F9`).",
     "and ~~every path passes~~ every path but one passes `BattleUnit + 0x80` (`lea … + 0x80` at `0023406F`, "
     "`00308673`, `00317E9D`, `00325BC4`, `002FDC42`, `003048EF`, `003105F9`); `AiOrder_CheckActionPreconditions` "
     "`00301830` passes a stack copy of `unit+0x80..+0x68F` instead " + C + "`003019BF` `lea rcx, [rsp+0x30]` → "
     "`0033A120`, whose `0033A144` `mov rdx, rcx` hands it to `00336710`; the copy is made at `00301857`–`003018DA`; "
     "§14)*."),

    # C-V39: ApplyStopAndTurn / ApplySimpleHeadingLimit are modes 3 / 5 of the family's own dispatcher (AM-7).
    (LOCO, "attribution was wrong**: neither is called from anywhere inside this family. The behaviour comes from\n"
           "the limiter's own 45° deadband. See section 9.)*",
     "attribution was ~~wrong~~ not wrong for `ApplyStopAndTurn`**: ~~neither is called from anywhere inside this "
     "family. The behaviour comes from~~ both are modes 3 and 5 of the family's own steering dispatcher, and the "
     "stop-and-pivot also comes from\nthe limiter's own 45° deadband. See section 9.)* " + C + "`0033BED0` calls "
     "`00339F00` at `0033BF8D`, which calls `ApplyStopAndTurn` `0033CE60` at `0033A06E`; `0033CE7B` zeroes the "
     "speed `+0xB0`; section 6, AM-7)*"),
    (LOCO, "called by `ApplyHeadingTurnLimiter`, and neither is called from anywhere inside this family** — their\n"
           "only callers are outside it (`00339F00`).",
     "called by `ApplyHeadingTurnLimiter`~~, and neither is called from anywhere inside this family~~** — their\n"
     "~~only callers are outside it~~ caller is the family's own steering dispatcher (`00339F00`) " + C
     + "`0033BED0` → `00339F00` at `0033BF8D` → `0033CE60` at `0033A06E`; section 6, AM-7)*."),
    (LOCO, "Their role is unread. **AM-7.**",
     "~~Their role is unread.~~ *(answered: see section 6, AM-7 — modes 3 and 5 of the dispatcher, `ApplyStopAndTurn` "
     "zeroing the speed; 2026-10-02, OPUS)* **AM-7.**"),

    # C-V40: the render-record trailer is 0x130 = 304 bytes (003325E7 mov ecx, 0x48930).
    (HSD, "256-byte trailer, allocated and initialised by",
     "~~256-byte~~ 304-byte (`0x130`) trailer " + C + "`003325E7` `mov ecx, 0x48930` allocates; 160 × `0x740` = "
     "`0x48800`; the 2026-09-19 propagation above)*, allocated and initialised by"),

    # C-V41: the README headline formula carries the pitch (002E454C-002E459C).
    (README, "`x = sin(heading)*speed`, `z = cos(heading)*speed`, plus a separate vertical term. Includes",
     "~~`x = sin(heading)*speed`, `z = cos(heading)*speed`, plus a separate vertical term.~~ "
     "`x = sin(yaw)*cos(pitch)*speed`, `y = sin(pitch)*speed`, `z = cos(yaw)*cos(pitch)*speed`, the pitch terms "
     "dropping out on the flat path " + C + "`002E454C`–`002E459C`, IAT `008C2BB0` sinf / `008C2BA8` cosf; the "
     "page's 2026-09-02 correction)*. Includes"),

    # C-V42: a facing change writes one to four copies (002E5EC6; 002E5ECB-002E5EE4; 002E5EF3-002E5F0B).
    (CFS, "(wraps again; context->+0xA8; three/four\n",
     "(wraps again; context->+0xA8; three/four   <- corrected 2026-10-02, OPUS - one to four: +0x50 always "
     "(002E5EC6), +0x70 / +0x60 only with actor +0x0D bit 5 clear (002E5ECB-002E5EE4), body +0xF0 only when one exists "
     "(002E5EF3-002E5F0B)\n"),

    # C-V11: turn_limit pi (+0x5C) is a dead store - no ceiling (002E57EE / 002E4BDD read +0x58 only; 00269345).
    (CFS, "- The turn is **9 degrees per step with a half-turn ceiling** (`π/20`, `π`).",
     "- The turn is **9 degrees per step ~~with a half-turn ceiling~~** (`π/20`~~, `π`~~) " + C + "`+0x5C` = `π` "
     "is never read — `002E5750` reads only `+0x58`, through `00264750` → `002E4BC0` (`002E4BDD`), and `002690D0` "
     "divides by `+0x58` at `00269345`; DP-1, §14)*."),
    (MODE, "**9 degrees per step, and never more than\na half-turn at once.**",
     "**9 degrees per step~~, and never more than~~\n~~a half-turn at once~~.** " + C + "the `π` stored at "
     "`0026C237` is never read — DP-1, §5)*"),
    (MODE, "**Nine degrees, and a ceiling of a half-turn.**",
     "**Nine degrees~~, and a ceiling of a half-turn~~.** " + C + "no instruction reads `+0x5C`; `002E5750` reads "
     "`+0x58` only, `002E57EE`; see the supersession note that follows)*"),

    # C-V33: every map-id override verb 00F6-0103, 0107-010B reaches the nav caches through 003278D0.
    (CNAV, "**`setmapidfloor` is the\nonly script verb that reaches this subsystem**",
     "~~**`setmapidfloor` is the~~\n~~only script verb that reaches this subsystem**~~ **Every verb of the map-id "
     "override family `00F6`–`0103` and `0107`–`010B` reaches this subsystem** — floor, wall and mj alike " + C
     + "`003278D0` is called by the setters `0026E130`, `0026E150`, `0026E850`, `0026E880` (and by `0026E960` at area "
     "start), whose callers `003791D0`..`003795A0` are the tails of those nineteen verbs)*"),
    (CNAV, "`setmapidfloor` is the\n  only verb that reaches this subsystem.",
     "~~`setmapidfloor` is the~~\n  ~~only verb that reaches this subsystem.~~ Every override verb `00F6`–`0103`, "
     "`0107`–`010B` reaches it through `003278D0` " + C + "the callers of `003278D0` and of its setters, §8)*."),

    # C-V43: a usemapid(0) actor is not flat and takes every consumer's 3-D side (+0x08 bit 2).
    (TDF, "actors a script (or the party verb) has put *on the map*; an actor with `usemapid(0)` is\n"
          "        neither flat nor 3-D by these selectors.",
     "actors a script (or the party verb) has put *on the map*; an actor with `usemapid(0)` is\n"
     "        ~~neither flat nor 3-D by these selectors.~~ not flat, and every consumer takes its 3-D side: `002E4380` "
     "the spherical delta, and `002E45E0` / `002E5610` the 3-D distance, because `usemapid(0)` sets `+0x08` bit 2 " + C
     + "`002E4528`–`002E452F` jump to the spherical path when `00267260` is 0; `002E475E`–`002E4773`, "
     "`002E4802`–`002E4817`, `002E56BC`–`002E56CC` OR `+0x08` bit 2 into the 3-D test; `0026AD60` sets bit 2 for "
     "`off`)*."),

    # C-S17: 00265200 has 33 callers at 37 sites.
    (TDF, "| It has 33 distinct callers at 33 sites |",
     "| It has 33 distinct callers at ~~33~~ 37 sites " + C + "`retool.py callers 00265200`, 37 call sites in 33 "
     "functions; §10's re-count)* |"),

    # C-S19: the creation sequence has five consumers (002E3550-002E3575).
    (CPOOL, "all four functions the creation sequence calls re-load the chain and test each hop:",
     "all ~~four~~ five functions the creation sequence calls " + C + "`00269EC0`, `002681D0`, `002682D0`, "
     "`002685F0` at `002E3550`–`002E3568` and `00268380` by the tail-jump at `002E3575`; pass 1's FIVE)* re-load the "
     "chain and test each hop:"),
    (CPOOL, "The allocator, the creator and all four consumers were",
     "The allocator, the creator and ~~all four~~ four of the five consumers " + C + "the fifth, `002681D0` at "
     "`002E3558`, was added by pass 1)* were"),
    (CPOOL, "the guards in all four consumers, which are",
     "the guards in all ~~four~~ five consumers " + C + "`002E3550`–`002E3575`, pass 1)*, which are"),

    # C-S01 (+ C-S20 on README:34): README banners against each page's front matter.
    (README, "**DOCUMENTED, tier 1.** How heading and speed",
     "~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* How "
     "heading and speed"),
    (README, "**DOCUMENTED, tier 1.** The attack step-in",
     "~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "attack step-in"),
    (README, "**DOCUMENTED, tier 1.** The battle pathfinder",
     "~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "battle pathfinder"),
    (README, "**PARTIAL, tier 1.** The shared geometry toolbox",
     "~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1.** " + C + "the page's front matter says `status: DOCUMENTED`)* "
     "The shared geometry toolbox"),
    (README, "**PARTIAL, tier 1.** The 128-entry movement-body pool behind the movement context's `+0x138`:",
     "~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1.** " + C + "the page's front matter says `status: AUDITED`)* The "
     "128-entry movement-body pool behind the ~~movement~~ secondary context's `+0x138` (actor `+0xC0`) " + C
     + "`002E353D` loads `[actor+0xC0]` and `002E3546` stores the body at its `+0x138`; the pool page's 2026-09-18 "
     "context correction)*:"),

    # C-S02: LOCO body banner against its front matter.
    (LOCO, "**PARTIAL.** The family's 26 functions",
     "~~**PARTIAL.**~~ **AUDITED.** " + C + "the front matter says `status: AUDITED`, every box closed 2026-09-30)* "
     "The family's 26 functions"),

    # C-S03: the locomotion solver is read (the NAV front-matter note is left: a YAML plain scalar).
    (NAV, "**Not read:** the locomotion solver that consumes the waypoint; the direct-route check",
     "**Not read:** ~~the locomotion solver that consumes the waypoint;~~ *(answered for the solver: see " + LOCO_LINK
     + ", whose turn limiter and step distance are read in full; 2026-10-02, OPUS)* the direct-route check"),
    (CNAV, "- The locomotion solver that consumes the waypoint.",
     "- ~~The locomotion solver that consumes the waypoint.~~ *(answered: see " + LOCO_LINK + ", the solver read; "
     "2026-10-02, OPUS)*"),

    # C-S04: 002E45E0 is read in full on the turning page.
    (HSD, "`002E45E0` is named but its body is not yet\nread here.",
     "`002E45E0` is named but its body is not yet\nread here *(answered: see [how a character turns]"
     "(Facing-And-Steering/how-a-character-turns.md), where `002E45E0` is read in full; 2026-10-02, OPUS)*."),

    # C-S05: what 00267260 tests is answered (K-7; the 3-D or flat page).
    (HSD, "**Not traced:** what `00267260` tests, and the part of `0033BFB0` after the angle.",
     "**Not traced:** ~~what `00267260` tests, and~~ *(answered for `00267260`: see K-7 below and [the 3-D or flat "
     "page](Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)'s flat selector; 2026-10-02, "
     "OPUS)* the part of `0033BFB0` after the angle."),

    # C-S06: 0026B6A0 / 0026C090 / 002E55C0 are read (ED-2, ED-3, ED-5).
    (TURN, "| `0026B6A0` | 120 B | the shared consumer of the wrapped angle — **not read** |",
     "| `0026B6A0` | 120 B | the shared consumer of the wrapped angle — ~~**not read**~~ *(answered: see ED-2 in §5 "
     "and the facing contract's §2 — kind 1 writes context `+0x38` / `+0x48`, kind 3 forwards the flag to "
     "`002E5FB0`; 2026-10-02, OPUS)* |"),
    (TURN, "| `0026C090` | 129 B | the tail target of both variants — **not read** |",
     "| `0026C090` | 129 B | the tail target of both variants — ~~**not read**~~ *(answered: see ED-3 in §5 — it "
     "wraps again and dispatches on the kind; 2026-10-02, OPUS)* |"),
    (TURN, "— called on the mode-0 path — **not read** (name and size filled in 2026-09-13) |",
     "— called on the mode-0 path — ~~**not read**~~ *(answered: see ED-5 in §2 — it clears `+0x29`, `+0x24` and "
     "`ctx+0xD0` and ends mode 2; 2026-10-02, OPUS)* (name and size filled in 2026-09-13) |"),
    (TURN, "| What `0026B6A0` / `0026C090` do | **not read** | — | UNKNOWN |",
     "| What `0026B6A0` / `0026C090` do | ~~**not read**~~ *(answered: see ED-2 and ED-3 in §5; 2026-10-02, OPUS)* "
     "| — | ~~UNKNOWN~~ PROVEN |"),
    (TURN, "`0026C090` and `002E55C0` remain unread, as § says;",
     "`0026C090` and `002E55C0` remain unread, as § says *(answered: see ED-2, ED-3 and ED-5 — all three read; "
     "2026-10-02, OPUS)*;"),

    # C-S07: the push/pop chain is read (the facing contract section 14 item 2, section 18).
    (SLOTS, "FUN_002627C0(ctx);                                      /* unread */\n",
     "FUN_002627C0(ctx);                                      /* unread */   /* <- corrected 2026-10-02, OPUS - read: "
     "it copies the 0x80 steering record from slot [+0xDC] to [+0xDC+1] (CONTRACT-facing-and-steering.md section 14 "
     "item 2) */\n"),
    (SLOTS, "  Named as the push/pop chain, unread.",
     "  Named as the push/pop chain, ~~unread~~ *(answered: see [the facing-and-steering contract]"
     "(../CONTRACT-facing-and-steering.md) §14 item 2 and §18 — all five read 2026-09-18; 2026-10-02, OPUS)*."),

    # C-S08 / C-S09: DW-1's 2026-09-15 census answers both.
    (SLOTS, "established, and no caller was traced that sets them. `DW-1`.",
     "established, and no caller was traced that sets them *(answered: see DW-1 in §8 — 4–7 are never written, "
     "FABLE 2026-09-15; 2026-10-02, OPUS)*. `DW-1`."),
    (SLOTS, "**Bits 3–5 and 7 are untouched by any site in the census.**",
     "**Bits 3–5 and 7 are untouched by any site in the census** *(answered: see DW-1's 2026-09-15 census in §8 — "
     "bits 3–5 are written by `002EC380` / `002EBE50`, bit 7 by `0026A1A0` / `00263230`; 2026-10-02, OPUS)*."),

    # C-S10: the named callees are read (section 14 items 1-2).
    (CFS, "**Not claimed:** the seven remaining named callees are still unread, and nothing here is a",
     "**Not claimed:** ~~the seven remaining named callees are still unread, and~~ *(answered: see §14 items 1–2, "
     "all read 2026-09-18; 2026-10-02, OPUS)* nothing here is a"),

    # C-S11: the weight masks are answered on the pool page (UQ-104).
    (CSEP, "- The units and meaning of the weight masks `+0x110` / `+0x114`.",
     "- ~~The units and meaning of the weight masks `+0x110` / `+0x114`.~~ *(answered: see [the pool page]"
     "(the-movement-body-pool-and-the-separation-pass.md) UQ-104, 2026-09-14 / -18 — priority bits, vetoes and "
     "freezes, `+0x114` never written; 2026-10-02, OPUS)*"),

    # C-S12: RDEC's scratch has one user thread (section 14 item 5).
    (CCQ, "**shared global buffer**, so two concurrent `RDEC` calls would race — nothing in this family",
     "**shared global buffer**, so two concurrent `RDEC` calls would race *(answered: see §14 item 5 — no caller can "
     "run concurrently, the bank has one user thread; 2026-10-02, OPUS)* — nothing in this family"),

    # C-S13: FZ-11 and UQ-103 are answered on the page.
    (POOL, "mask table, is **FZ-11**.",
     "mask table, is **FZ-11** *(answered: see FZ-11 in §7, ANSWERED 2026-09-18 — the map id, the ground type and the "
     "mj class, filled by the `setmapid*` verbs; 2026-10-02, OPUS)*."),
    (POOL, "body.** The bullet stays open for those.",
     "body.** ~~The bullet stays open for those.~~ *(answered: see UQ-103's ANSWERED 2026-09-18 note in this bullet — "
     "x and z from the caller, `200.0f` unused, the mean divided by `0046AFA0`; 2026-10-02, OPUS)*"),

    # C-S14: the refusal's reachability is answered 2026-09-30 (class stability stays open).
    (CHSD, "stability and the refusal's reachability stay OPEN.",
     "stability ~~and the refusal's reachability stay OPEN~~ stays OPEN *(answered for the refusal's reachability: "
     "see the ANSWERED 2026-09-30 item below — the refusal does not run there; 2026-10-02, OPUS)*."),
    (HSD, "the contract's section-14 closure that used one is reopened, CON-172)",
     "the contract's section-14 closure that used one is reopened, CON-172 *(answered: see the heading-speed "
     "contract's §14, ANSWERED 2026-09-30 (OPUS) — the refusal does not run there; 2026-10-02, OPUS)*)"),

    # C-S15: every order case is read; the 16-band path calls 002367A0 then 00312918.
    (LOCO, "**What is not read:** what any of the six cases *does*.",
     "**What is not read:** *(answered: see DE-1 to DE-4 below and the ANSWERED 2026-09-18 box — every case is "
     "read; 2026-10-02, OPUS)* what any of the six cases *does*."),
    (LOCO, "The shared handler is `002367A0`,",
     "The shared ~~handler is~~ path first calls `002367A0` and then goes to `00312918` " + C + "`00312970`–"
     "`0031297B`; the 2026-09-13 correction)*,"),

    # C-S20: the body hangs off the secondary context ([actor+0xC0]+0x138, 002E353D / 002E3546).
    (POOL, "attached to the actor's movement context at `+0x138` when its presentation",
     "attached to the actor's ~~movement~~ secondary context (actor `+0xC0`) at `+0x138` " + C + "`002E353D` loads "
     "`[actor+0xC0]`, `002E3546` stores there; §2.3's 2026-09-18 correction)* when its presentation"),
    (POOL, "stores it at the movement context's `+0x138` (`002E3546`)",
     "stores it at the ~~movement~~ secondary context's `+0x138` (`002E3546`) " + C + "`002E353D` loads "
     "`[actor+0xC0]`; §2.3's context correction)*"),

    # C-S21: the heading publish targets the 0x740 render record at 022C6F28 (002E5C33-002E5C4C).
    (HSD, "-> CharacterRenderObject +0x240\n",
     "-> CharacterRenderObject +0x240   <- corrected 2026-10-02, OPUS - the 0x740-byte render record at 022C6F28 "
     "(002E5C33-002E5C4C, section 8f), not CharacterRenderObject\n"),
    (HSD, "and the CharacterRenderObject record (`+0x240`).",
     "and the ~~CharacterRenderObject record~~ `0x740`-byte render record at `022C6F28` (`+0x240`) " + C
     + "`002E5C33`–`002E5C4C`; §8f)*."),
    (HSD, "the heading publication into the CharacterRenderObject\narray (`002E5C10`)",
     "the heading publication into the ~~CharacterRenderObject~~ render-record\narray (`002E5C10`) " + C
     + "`022C6F28` + id × `0x740`, `002E5C33`–`002E5C4C`; §8f)*"),

    # C-S23: 00263CC0 returns the desired movement heading (00263CD6-00263CED).
    (MODE, "| `00263CC0` | the movement-kind speed read (class 1 `+0x38`, class 3 `+0xA4`) |",
     "| `00263CC0` | ~~the movement-kind speed read~~ the desired-heading read (class 1 `+0x38`, class 3 `+0xA4`) "
     + C + "`00263CD6`–`00263CED` return context `+0xA4` / `+0x38`, the desired movement heading §10's mode-2 row "
     "names)* |"),
    (MODE, "`00263CC0` (55 B) is the movement-kind speed read:",
     "`00263CC0` (55 B) is the ~~movement-kind speed read~~ desired-heading read " + C + "`00263CDD` / `00263CED` "
     "load context `+0xA4` / `+0x38`, the field `Actor_SetDesiredMovementHeading` writes)*:"),
    (MODE, "- the two-speed branch the facing and battle-unit callers share.",
     "- the ~~two-speed~~ two-class heading branch the facing and battle-unit callers share " + C + "it returns a "
     "heading, not a speed, `00263CD6`–`00263CED`)*."),

    # C-S24: 00265600 returns the movement mode (+0x28 & 0x7F, 0026561B-0026561F).
    (SLOTS, "`edx==0` dispatches on the steering mode (`00265600`):",
     "`edx==0` dispatches on the ~~steering~~ movement mode (`00265600`) " + C + "`0026561B`–`0026561F` return "
     "`+0x28 & 0x7F`, the movement mode; `+0x29` is the steering mode, §4)*:"),

    # C-S27: the outcode history's reader is found (0025C830).
    (CLAMP, "**Nothing in this function reads the history back**, so what it is for is not\n"
            "established here; that it *is* a history is arithmetic.",
     "**Nothing in this function reads the history back**, so ~~what it is for is not~~\n~~established here~~ "
     "*(answered: see the falsification table below — its reader is `0025C830`, FABLE 2026-09-18; 2026-10-02, "
     "OPUS)*; that it *is* a history is arithmetic."),

    # C-S28: the two switches gate different stages (section 2, CON-186).
    (ANIM, "- Two global switches and a per-list enable can stop all of it; they were not traced to their setters.",
     "- Two global switches and a per-list enable ~~can stop all of it~~ gate different stages — the first switch and "
     "the list refuse new requests, the second stops the step while requests still queue *(answered: see §2, "
     "corrected 2026-09-29, `CON-186`; 2026-10-02, OPUS)*; they were not traced to their setters."),

    # C-S29: the mode bodies and the mode-bit authors are answered by SD-183.
    (LOCO, "*Not read:* modes 1 / 4, 2 and 6's bodies, and what authors the mode bits. **AM-7.**",
     "*Not read:* modes 1 / 4, 2 and 6's bodies, and what authors the mode bits *(answered: see the SD-183 answer in "
     "the next box — the flag word, the three bodies and the mode writers; 2026-10-02, OPUS)*. **AM-7.**"),

    # C-S30: the bootstrap-guard reading is overturned in section 10.
    (TDF, "It is *\"the actor system has been brought up\"*, and it reads as a\nguard against running the flat path "
          "during bootstrap or after a teardown, when the controller state\nit depends on is not valid.",
     "~~It is *\"the actor system has been brought up\"*, and it reads as a~~\n~~guard against running the flat path "
     "during bootstrap or after a teardown, when the controller state~~\n~~it depends on is not valid.~~ " + C
     + "overturned in §10 — `02B40530` is set by `003B7E10` from six sites and `02B40534` by eight stores, the "
     "party-swap verbs among them, during normal runtime)*"),
    (TDF, "actor system bootstrap\n",
     "actor system bootstrap   <- corrected 2026-10-02, OPUS - not only at bootstrap: both flags are also written at "
     "runtime (section 10; 003B7E10, the party-swap verbs)\n"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY", rel.split("/")[-1]); texts[rel] = t; continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING", rel.split("/")[-1], old[:40]); fails += 1; texts[rel] = t; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        texts[rel] = t.replace(hit[0], n, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
