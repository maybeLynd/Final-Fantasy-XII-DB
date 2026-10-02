"""apply_03world.py [--apply] - 03-World-Area-Field readiness map (cloud-reports/re-readiness/03-world.md), section 3.1
value items C-V1..C-V28 and the section 3.2 stale / banner items, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the image or the shipped data refutes) and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*. The verdicts and their deciding
addresses are in OPUS's scratch verdicts-03.md (2026-10-02).
C-V7 favours no page and none is wrong alone: the two figures are not a partition, so the third class is added.
C-V8: the bit-15 page's 65 / 47 / 2 / 110 hold when the thunk 00313F60 is not counted as a caller of 00377C20; the
contract's "79 | 66" mixes the two countings and its "three functions use both routes" is two. Only those are edited.
C-V13 is a medium verdict: the restatement says only what the bytes show (who sets and who clears +0x1061).
C-V20: the pages' u16 / i16 differ only in the sign of the last two row words; only that is corrected.
C-V27: the contract line omits the debug override for all three arguments, so its code comment names all three.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` note instead of a strike (their OLD includes the line end, so NEW never
contains OLD); the one front-matter line (an archive_formats entry) gets a YAML `# <- corrected` comment.
Left out (section 3.2): C-S3 (both names are used and D-9 supports "wind"), C-S8 (the ledger names CombatAction as
002F8060's primary owner, so the page front matter, not line 247, is what disagrees), C-S9 / C-S14 / C-S17 / C-S24 /
C-S32 / C-S38 / C-S46 (front-matter dates and status ladders: a later dated edit is not a review), C-S28 (the name
equivalence is already recorded on the roll page), C-S31 (the seven callees are still FUN_ in the ledger), and the
structural gaps of section 2.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "03-World-Area-Field/"
R = F + "README.md"
WT = F + "walking-into-an-authored-trigger-point.md"
CTP = F + "CONTRACT-authored-trigger-points.md"
CEV = F + "CONTRACT-field-environment-variant.md"
CV = F + "choosing-the-field-environment-variant.md"
CFA = F + "CONTRACT-field-record-accessors.md"
CW = F + "CONTRACT-weather.md"
NAV = F + "Field-Record-Table/field-record-table-navimapdata.md"
B15 = F + "Field-Record-Table/field-record-bit15-action-permission.md"
SS = F + "Weather/weather-slot-state-model.md"
PR = F + "Weather/weather-probability-and-transition-roll.md"
AP = F + "Weather/weather-apply-and-environment-materialization.md"
MW = F + "Weather/mweather-resource-format.md"
CC = F + "Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md"
MP = F + "Map-Pack/the-map-ctrl-pack.md"

RING = "`002FB3B0` stores `{field, mask}` at the ring index `+0x24`, advances it modulo 3 and caps the count `+0x28` at 3"
FLAG = ("the body never sets `+0x1061` - its setters are `0026D8F0` (`0026D8F9`) and `00268320` (`0026836C`), and "
        "`00280140` stores `dil` there at `00280213`")
WHOLE = "`002620F7 jne 002621A8`; `002621A8 mov ecx, 0xB` / `002621AD call 003601C0`, `002621BC jmp 003601C0`"

EDITS = [
    # C-V1: both heights are zeroed (002F80A5 xor edi, edi; unit position into [rsp+0x50/0x54/0x58] at 002F811F-002F8131;
    #     002F8150 mov [rsp+0x54], edi; point y = 0 at 002F81C1; 002F81EF call 003A1920).
    (WT, "> `mov dword ptr [rsp+0x44], 0`) while the unit's own position is real in all three. **The unit's\n"
         "> height therefore counts against the 1.3 budget directly** — a point is harder to reach from above or\n"
         "> below it, and how much harder is a property of the area's authored ground level, not of the point.",
     "> `mov dword ptr [rsp+0x44], 0`) ~~while the unit's own position is real in all three.~~ and so is the unit's: "
     "`002F8150 mov [rsp+0x54], edi` overwrites the height `Actor_GetWorldPosition` returned with `edi = 0` (zeroed "
     "at `002F80A5`) *(corrected 2026-10-02, OPUS: unit position into `[rsp+0x50/0x54/0x58]` at "
     "`002F811F`–`002F8131`, point height 0 at `002F81C1`, distance `003A1920` at `002F81EF`; "
     "CONTRACT-authored-trigger-points.md TP-2)*. ~~**The unit's~~\n"
     "> ~~height therefore counts against the 1.3 budget directly** — a point is harder to reach from above or~~\n"
     "> ~~below it, and how much harder is a property of the area's authored ground level, not of the point.~~ "
     "**The radius is horizontal; height does not count.**"),
    (WT, "(`003A1950`). So `1.3` is a radius in world units, and the zero height of the authored point counts against it\n"
         "linearly.",
     "(`003A1950`). So `1.3` is a radius in world units, ~~and the zero height of the authored point counts against "
     "it~~\n~~linearly~~ and a horizontal one: both heights are zeroed before the call *(corrected 2026-10-02, OPUS: "
     "`002F8150 mov [rsp+0x54], edi` zeroes the unit's, `002F81C1` the point's)*."),
    (CTP, "Place it at the point's coordinates but a height away and assert the height is charged\n"
          "against the same budget (TP-2).",
     "~~Place it at the point's coordinates but a height away and assert the height is charged~~\n"
     "~~against the same budget (TP-2).~~ Place it at the point's coordinates but a height away and assert it fires, "
     "because the height is not charged (TP-2) *(corrected 2026-10-02, OPUS: `002F8150 mov [rsp+0x54], edi` zeroes the "
     "unit's height before `003A1920`, as TP-2's correction of 2026-09-25 says)*."),

    # C-V2: the threshold is the f32 at 00901B34 = 1.2999999523162842 (002F81F4 comiss xmm7, xmm0).
    (WT, "horizontal pair. The threshold is **1.3**.",
     "horizontal pair. The threshold is ~~**1.3**~~ **`1.2999999523162842`**, the `f32` nearest 1.3 *(corrected "
     "2026-10-02, OPUS: read at `00901B34`, compared by `002F81F4 comiss xmm7, xmm0`)*."),

    # C-V3: the live set is a three-slot ring (002FB3B0: 002FB3CF-002FB409 index modulo 3, 002FB40D-002FB417 count
    #     capped at 3; 002FA230 clears it).
    (WT, "**Every field can carry up to 32 invisible authored points. Walk close enough to one and it fires —\n"
         "once, ever.** The point is removed from the field's live set the moment it triggers, so nothing about\n"
         "the encounter is repeatable by walking back over the same ground.",
     "**Every field can carry up to 32 invisible authored points. Walk close enough to one and it fires —\n"
     "~~once, ever.~~** once, while its field keeps one of three ring slots *(corrected 2026-10-02, OPUS: " + RING
     + ", `002FB3CF`–`002FB417`, so a fourth fired-in field overwrites the oldest; `002FA230` clears all three)*. The "
     "point is removed from the field's live set the moment it triggers, so ~~nothing about~~\n"
     "~~the encounter is repeatable by walking back over the same ground.~~ it does not fire again while that "
     "field's ring entry survives."),
    (WT, "**The live set is a 32-bit mask stored per field** in a 12-byte-stride table at `0x2EC3EA0`, found by\n"
         "scanning for the current field id. **Clearing the bit is what makes the trigger once-only**, and the",
     "**The live set is a 32-bit mask stored per field** in a ~~12-byte-stride table~~ three-slot ring of 12-byte "
     "`{field, mask}` records *(corrected 2026-10-02, OPUS: " + RING + ", `002FB3CF`–`002FB417`)* at `0x2EC3EA0`, "
     "found by\nscanning for the current field id. **Clearing the bit is what makes the trigger ~~once-only~~ not fire "
     "again** while the field keeps its ring slot, and the"),
    (WT, "The once-ever guarantee itself is still the per-field mask clear described above.",
     "The ~~once-ever~~ once-only guarantee itself is still the per-field mask clear described above, held in a "
     "three-field ring *(corrected 2026-10-02, OPUS: `002FB3B0`, `002FB3CF`–`002FB417`)*."),
    (CTP, "spent` exactly once and never back.",
     "spent` exactly once ~~and never back~~, and stays spent while its field keeps one of the ring's three slots "
     "(TP-4) *(corrected 2026-10-02, OPUS: " + RING + ", `002FB3CF`–`002FB417`; `002FA230` clears the ring)*."),
    (CTP, "Walking over a spot in the field makes something happen once and never again;",
     "Walking over a spot in the field makes something happen once ~~and never again~~, and not again while the field "
     "is among the three most recently fired-in fields (TP-4) *(corrected 2026-10-02, OPUS: the three-slot ring, "
     "`002FB3CF`–`002FB417`)*;"),

    # C-V4: 00377700's failure default is permissive (00377713 je / 00377718 jae -> 00377728 xor dl, dl; 0037772D not /
    #     0037772F test al, 1; 0037773C mov eax, 1 unless the save veto 00314A60 fires).
    (NAV, "the *permissive* value for the navigation-map id (`0xFFF` = \"none\") and the *restrictive* value for\n"
          "every flag.",
     "the *permissive* value for the navigation-map id (`0xFFF` = \"none\") and the *restrictive* value for\n"
     "~~every flag.~~ every flag but the third byte's bit 0, which `00377700` reads inverted, so its default is the "
     "permissive 1 *(corrected 2026-10-02, OPUS: `00377713 je` / `00377718 jae` → `00377728 xor dl, dl`, then "
     "`0037772D not` / `0037772F test al, 1` and `0037773C mov eax, 1` unless the save veto `00314A60` fires)*."),
    (NAV, "- **It fails closed.** An absent table or an out-of-range field id yields record `0x0FFF` /\n"
          "  third byte `0`: no navigation map, and every flag clear — the restrictive answer. Preserve that",
     "- **It fails closed except at `00377700`.** An absent table or an out-of-range field id yields record "
     "`0x0FFF` /\n  third byte `0`: no navigation map, and every flag clear ~~— the restrictive answer~~, which "
     "`00377700` reads inverted as the permissive 1 *(corrected 2026-10-02, OPUS: `00377728 xor dl, dl` / "
     "`0037772D not` / `0037773C mov eax, 1`; CONTRACT-field-record-accessors.md §10)*. Preserve that"),

    # C-V5: 00377C70 takes bits 4-6 (00377C91 movzx edx, byte [rcx+rax+0xA]; 00377C99 shr eax, 4; 00377C9C and eax, 7).
    (CFA, "| | **bits 4–7** | `00377C70` | `shr 4` |",
     "| | ~~**bits 4–7**~~ **bits 4–6** | `00377C70` | `shr 4` then `and 7` *(corrected 2026-10-02, OPUS: "
     "`00377C99 shr eax, 4` / `00377C9C and eax, 7`; bit 7 is never taken)* |"),
    (CFA, "is at least two. **Bits 1–3 of the byte are the only part no accessor touches.**",
     "is at least two. **~~Bits 1–3 of the byte are the only part no accessor touches.~~** **Bits 1–3 and bit 7 of the "
     "byte are the parts no accessor touches** *(corrected 2026-10-02, OPUS: `00377C70` takes bits 4–6, "
     "`00377C9C and eax, 7`; §14's execution note)*."),

    # C-V6: the table is bound once per boot (00377CC0 has one caller, 00266D10 at 00267146; 00266D10 has one caller,
    #     the boot routine 0022A0B0 at 0022A3F7).
    (NAV, "area load / transition\n  -> 00377CC0  WorldAreaField_BootMapTables\n",
     "area load / transition   <- corrected 2026-10-02, OPUS: boot, once - 00377CC0's one caller is 00266D10 "
     "(00267146), whose one caller is the boot routine 0022A0B0 (0022A3F7)\n"
     "  -> 00377CC0  WorldAreaField_BootMapTables\n"),
    (B15, "area load / transition\n  -> field record table bound (DAT_02add100)\n",
     "area load / transition   <- corrected 2026-10-02, OPUS: boot, once - the binder 00377CC0 has one caller, "
     "00266D10 (00267146), run once by the boot routine 0022A0B0 (0022A3F7)\n"
     "  -> field record table bound (DAT_02add100)\n"),
    (B15, "**Upstream:** the active-or-pending field id, and the field record table bound at area load.",
     "**Upstream:** the active-or-pending field id, and the field record table bound ~~at area load~~ once at boot "
     "*(corrected 2026-10-02, OPUS: `00377CC0` ← `00266D10` at `00267146` ← the boot routine `0022A0B0` at "
     "`0022A3F7`, one caller each)*."),

    # C-V7: 173 sites in 131 functions; 55 in the 42 functions with no 00377C20 / 00313F60 call; of the other 118, 116
    #     lie within +-8 instructions of the call and 117 within +-25 (the far ones: 0030E454, 0030E48A in 0030E360).
    (NAV, "At ±25: 117 / 55. The statistic does not move with",
     "At ±25: 117 / 55. *(corrected 2026-10-02, OPUS: the two figures are not a partition of 173. The 55 are the "
     "sites in the 42 functions that never call `00377C20` or its thunk `00313F60`; the other 118 lie in functions "
     "that do, and the third class — the call present but outside the window — holds 2 at ±8 and 1 at ±25, both in "
     "`0030E360` (`0030E454`, 28 instructions from the nearest call, and `0030E48A`, 12). So 116 + 2 + 55 = "
     "117 + 1 + 55 = 173, re-derived over `retool.py grep 0x80000003`: 173 sites in 131 functions.)* The statistic "
     "does not move with"),

    # C-V8: retool.py callers - 00377C20: 80 sites in 66 functions, one of them the thunk 00313F60 (its jmp is the 80th
    #     site); 00313F60: 67 sites in 47 functions; both routes: 00253C70 and 003266C0; union 110 without the thunk.
    (CFA, "numbers and \"65 direct callers\" is neither of them:",
     "numbers and \"65 direct callers\" is ~~neither of them~~ the function count without the thunk itself "
     "*(corrected 2026-10-02, OPUS: `retool.py callers 00377C20` lists 80 sites in 66 functions, and one of the 66 is "
     "the thunk `00313F60`, whose `jmp` is the 80th site; without it, 79 sites in 65 functions)*:"),
    (CFA, "| `00377C20` bit 15 | **79** | **66** | plus one `jmp` from its thunk |",
     "| `00377C20` bit 15 | **79** | ~~**66**~~ **65** | plus one `jmp` from its thunk, whose function makes 66 "
     "*(corrected 2026-10-02, OPUS: the 79 sites lie in 65 functions; the thunk `00313F60` is the 66th, `retool.py "
     "callers 00377C20`)* |"),
    (CFA, "the 47 matches the old figure; the 65 does not match either column |",
     "the 47 matches the old figure; ~~the 65 does not match either column~~ the 65 is the direct column without the "
     "thunk *(corrected 2026-10-02, OPUS: `retool.py callers 00377C20 00313F60`)* |"),
    (CFA, "these are the same population counted differently, and three functions use\n   both routes.)",
     "these are the same population counted differently, and ~~three functions use~~\n   ~~both routes~~ two "
     "functions use both routes, `00253C70` and `003266C0` *(corrected 2026-10-02, OPUS: `retool.py callers 00377C20 "
     "00313F60`; 65 + 47 − 2 = 110)*.)"),

    # C-V9: the resolver's one draw is 0025ABB8, in the current-slot-2 arm, before any probability is read
    #     (0025ABAA sub ecx, 1 / 0025ABAD je; 0025ABB3 cmp ecx, 2 / 0025ABB6 je).
    (PR, "picks the single eligible one directly, and draws MT19937 only when two\nremain.",
     "picks the single eligible one directly, ~~and draws MT19937 only when two~~\n~~remain.~~ and draws MT19937 "
     "once, before any probability is read, only when the current slot is 2; from slots 1 and 3 the order is fixed, "
     "slot 2 first *(corrected 2026-10-02, OPUS: `0025ABAA sub ecx, 1` / `0025ABAD je`, `0025ABB3 cmp ecx, 2` / "
     "`0025ABB6 je`; the only call to `00379CD0` is `0025ABB8`; CON-147 below)*."),

    # C-V10: an all-zero weatherProbability pins the slot - every resolver arm falls back to the current slot
    #     (0025ABF0, 0025AC1D, 0025AC47, 0025AC88).
    (PR, "never change weather (probability 100), some always re-roll (probability 0), most sit",
     "never change weather (probability 100), ~~some always re-roll (probability 0)~~ some leave the current slot "
     "whenever another slot is eligible (probability 0), an area whose three probabilities are all 0 never changes "
     "*(corrected 2026-10-02, OPUS: every arm of `0025ABA0` falls back to the current slot — `0025ABF0`, `0025AC1D`, "
     "`0025AC47`, `0025AC88`; the 2026-09-21 correction below)*, most sit"),
    (PR, "3. probability **0** → current slot cannot be retained → pick an alternate;",
     "3. probability **0** → ~~current slot cannot be retained →~~ pick an alternate with non-zero probability, or "
     "keep the current slot when neither has one *(corrected 2026-10-02, OPUS: `0025ABA0` reads only the alternates' "
     "probabilities, `002658B0(slot) > 0`, and every arm falls back to the current slot — `0025ABF0`, `0025AC1D`, "
     "`0025AC47`, `0025AC88`)*;"),

    # C-V11: the latched path still posts 003601C0(0x0B) and (0x0C) (002620F7 jne 002621A8).
    (PR, "- if already set, the whole weather/resource initialization core is skipped;",
     "- if already set, the ~~whole~~ weather/resource initialization core is skipped, but the two event posts still "
     "run *(corrected 2026-10-02, OPUS: " + WHOLE + ")*;"),
    (PR, "skips its whole body if `byte [rcx + 0x10] & 4` (`002620F3`–`002620F7`)",
     "~~skips its whole body~~ skips the roll and the resource posts, but not the two `003601C0` event posts at "
     "`002621A8` *(corrected 2026-10-02, OPUS: " + WHOLE + ")*, if `byte [rcx + 0x10] & 4` (`002620F3`–`002620F7`)"),

    # C-V12: 02099DA8 = A[4 + 4*envIdx] (0026DA10-0026DA26), A = map_ref.bin +0x10 = {4,4,4,0,0,1,2,2,3,0,...}; over the
    #     279 shipped lanes 4 x246, 3 x16, 0 x12, 2 x4, 1 x1 (map_ref.bin read through vbf_read_entry).
    (AP, "02099DA8         u32  global environment class 0..3\n",
     "02099DA8         u32  global environment class 0..3   <- corrected 2026-10-02, OPUS: 0..4 as authored - "
     "0026DA1E loads A[4 + 4*envIdx] from the map_ref +0x10 table {4,4,4,0,0,1,2,2,3,0,...}, and 4 is the value on 246 "
     "of the 279 shipped lanes (map_ref.bin read through vbf_read_entry; CON-146 below)\n"),

    # C-V13 (medium): +0x1061 is a skip flag 0026D910 only clears (0026D951 cmp / 0026D957 jne over the 0026D95E store;
    #     0026DA92 clears); set by 0026D8F9 (0026D8F0) and 0026836C (00268320); 00280140 stores dil at 00280213.
    (CEV, "**EV-3 — The selector is latched, and the latch is FIRST-WRITER-WINS and released on exit.**\n"
          "`0026D951` tests `[ctx + 0x1061]`; only when it is clear does `0026D95E` write the selector to\n"
          "`[ctx + 0x1060]`. At the end, `0026DA92` clears `[ctx + 0x1061]` to zero. *So the selector written by\n"
          "whoever got there first is consumed exactly once per pass, and a second caller within the same pass\n"
          "publishes the first caller's choice.*",
     "**EV-3 — The selector is ~~latched, and the latch is FIRST-WRITER-WINS and released on exit~~ gated by a skip "
     "flag that this body only clears.**\n"
     "`0026D951` tests `[ctx + 0x1061]`; only when it is clear does `0026D95E` write the selector to\n"
     "`[ctx + 0x1060]`. At the end, `0026DA92` clears `[ctx + 0x1061]` to zero. *~~So the selector written by~~\n"
     "~~whoever got there first is consumed exactly once per pass, and a second caller within the same pass~~\n"
     "~~publishes the first caller's choice.~~* *(corrected 2026-10-02, OPUS: " + FLAG + ". So with the flag set, "
     "the first call publishes the slot already in `+0x1060` and consumes the flag, and a second call in the same "
     "pass writes its own selector unless a setter runs between them; with the flag clear, every call writes its "
     "own.)*"),
    (CEV, "tail-call.* The\nlatch transitions `free → held → free` within one call.",
     "tail-call.* The\n~~latch transitions `free → held → free` within one call.~~ flag is only cleared here (`0026DA92`); it is set "
     "outside the body *(corrected 2026-10-02, OPUS: " + FLAG + "; EV-3)*."),
    (CEV, "Call twice within one pass with different counts and assert the second publishes the **first's**\n"
          "selector (EV-3).",
     "~~Call twice within one pass with different counts and assert the second publishes the **first's**~~\n"
     "~~selector (EV-3).~~ Set `+0x1061`, call twice within one pass with different counts, and assert the first "
     "publishes the slot already stored and the second its own selector (EV-3) *(corrected 2026-10-02, OPUS: "
     "`0026D951` / `0026D957` skip the `0026D95E` store only while the flag is set, and `0026DA92` clears it)*."),
    (CV, "if [ctx + 0x1061] == 0:  [ctx + 0x1060] = selector ; a latch: first writer wins\n",
     "if [ctx + 0x1061] == 0:  [ctx + 0x1060] = selector ; a latch: first writer wins   <- corrected 2026-10-02, "
     "OPUS: not first-writer-wins - this body only clears +0x1061 (0026DA92); its setters are 0026D8F9 and 0026836C, "
     "so of two calls in one pass the second writes its own selector\n"),

    # C-V14: four direct entries into 0026D910 - 0025ACA0@0025AD06 (jmp), 00266D10@00266E74 / @00266E7B,
    #     003565C0@0035660E (retool.py callers 0026D910).
    (SS, "has exactly three call sites: the script verb **`setweatherslot`**",
     "has ~~exactly three call sites~~ four direct entries, the three named here and the field-entry roll's tail "
     "jump at `0025AD06` *(corrected 2026-10-02, OPUS: `retool.py callers 0026D910` — `0025ACA0`@`0025AD06` (`jmp`), "
     "`00266D10`@`00266E74` and @`00266E7B`, `003565C0`@`0035660E`)*: the script verb **`setweatherslot`**"),
    (SS, "So at runtime every weather apply comes through the VM verb;",
     "So at runtime ~~every weather apply comes through the VM verb~~ a weather apply comes through the VM verb or "
     "through the field-entry roll `0025ACA0` *(corrected 2026-10-02, OPUS: its tail jump at `0025AD06`)*;"),
    (AP, "has exactly three call sites: the script verb **`setweatherslot`**",
     "has ~~exactly three call sites~~ four direct entries, the three named here and the field-entry roll's tail "
     "jump at `0025AD06` *(corrected 2026-10-02, OPUS: `retool.py callers 0026D910`, and this page's own entry census "
     "above)*: the script verb **`setweatherslot`**"),
    (AP, "So at runtime every weather apply comes through the VM verb;",
     "So at runtime ~~every weather apply comes through the VM verb~~ a weather apply comes through the VM verb or "
     "through the field-entry roll `0025ACA0` *(corrected 2026-10-02, OPUS: its tail jump at `0025AD06`)*;"),

    # C-V15: 0209A6E8 is the weather slot 1..3 (writers 0026E8E1 = 00265920() from 003792A5 / 0037969B, and the reset
    #     to 1 at 0026E653); 002F7394 add ecx, 0x17 / 002F74C9 test dword [r9-0x11] = entry +0x0C.
    (MP, "— **the flag dword's bits\n  24–31 (the byte at `+0x0F`) are a per-bank presence mask** (`0209A6E8` = the\n"
         "  active bank, so bank *n* = bit *n*+0x17; the census `+0x0E` values `0x8000`/\n"
         "  `0x8700`/`0x9700` decode as banks {14} / {7,8,9,14} / {7,8,9,11,14}).",
     "— **the flag dword's bits\n  24–31 (the byte at `+0x0F`) are a ~~per-bank presence mask~~ per-weather-slot "
     "membership mask** (`0209A6E8` = the\n"
     "  ~~active bank, so bank *n* = bit *n*+0x17~~ weather slot `1..3`, so slot *n* = bit *n*+0x17 and slots 1–3 are "
     "bits 24–26; ~~the census `+0x0E` values `0x8000`/~~\n"
     "  ~~`0x8700`/`0x9700` decode as banks {14} / {7,8,9,14} / {7,8,9,11,14}~~ the census `+0x0E` words `0x8000` / "
     "`0x8700` / `0x9700` set dword bits {31} / {24,25,26,31} / {24,25,26,28,31}, so slots {none} / {1,2,3} / "
     "{1,2,3} *(corrected 2026-10-02, OPUS: `0209A6E8`'s writers are `0026E8E1`, storing the argument both callers "
     "take from `00265920()` (`003792A5`, `0037969B`), and the reset to 1 at `0026E653`; `002F7394 add ecx, 0x17` and "
     "`002F74C9 test dword ptr [r9 - 0x11], esi` test entry `+0x0C`; "
     "Weather/call-chains/field-init-weather-to-legacyps2gs-rebuild.md UQ-88)*)."),
    # C-V15 + C-V17: the +0x218 fill writes +0x00/+0x08/+0x10/+0x18 and the byte +0x20 only (002F7600-002F7628).
    (MP, "get a `count×0x28` zeroed table at `ctx+0x218` — **the active-bank working set**.",
     "get a `count×0x28` ~~zeroed~~ table at `ctx+0x218`, whose fill writes only `+0x00`, `+0x08`, `+0x10`, `+0x18` "
     "and the byte `+0x20` — **the ~~active-bank~~ current weather slot's working set** *(corrected 2026-10-02, OPUS: "
     "fill loop `002F7600`–`002F7628`; the table comes from `003EC8D0` at `002F75DC`, whose own zeroing is not "
     "checked here; the slot is `0209A6E8`, as above)*."),
    (MP, "select among per bank, and `002F7380` is the bank-change reselection.",
     "select among per ~~bank~~ weather slot, and `002F7380` is the ~~bank-change~~ weather-slot reselection "
     "*(corrected 2026-10-02, OPUS: `0209A6E8` is the weather slot, as above)*."),

    # C-V16: 00466220 passes {0x14, 0x1C, 0x24, 0x2C} and returns 1 except for 0x1C (00466225 lea ecx, [rdx-0x14];
    #     00466228 test cl, 0xE7; 0046622D cmp dl, 0x1C; 00466235 cmovne eax, 1).
    (MP, "`00466220` (`byte[entry]` ∈ `{0x14,0x1C}`). The survivors",
     "`00466220` (`byte[entry]` ∈ ~~`{0x14,0x1C}`~~ `{0x14, 0x1C, 0x24, 0x2C}`, returning 1 for `0x14`, `0x24`, "
     "`0x2C` and 0 for `0x1C` *(corrected 2026-10-02, OPUS: `00466225 lea ecx, [rdx-0x14]` / `00466228 test cl, 0xE7` "
     "/ `0046622D cmp dl, 0x1C` / `00466235 cmovne`)*). The survivors"),

    # C-V18: the pass-1 increment is 1 or 4 (002F73D0 xor ecx, ecx; 002F7416 lea ebp, [rcx+1]; 002F744A mov edx, 4 /
    #     002F744F cmovne edx, ebp / 002F7455 add r15d, edx).
    (CC, "`00466220(rec)` is a predicate selecting an increment of either `i+1` or `4`, accumulated into a",
     "`00466220(rec)` is a predicate selecting an increment of either ~~`i+1`~~ `1` *(corrected 2026-10-02, OPUS: "
     "`002F73D0 xor ecx, ecx`, `002F7416 lea ebp, [rcx+1]`, `002F744A mov edx, 4` / `002F744F cmovne edx, ebp`)* or "
     "`4`, accumulated into a"),

    # C-V19: 0026FAD0 -> 0026F470 walks the EFB binding table [02F8F228] (row count word[02F8F23A]) and builds an effect
    #     per row whose channel byte +4 matches and whose enable byte +7+value is set (0026F522-0026F53B); {2, idx, mode}
    #     is the 0024F680 key (0026FB03-0026FB12); flags[idx] |= 8, |= 4 (0026FB5D-0026FB69).
    (MP, "message `{u16 idx; u16 mode}` through `0026F470` (queue\n",
     "message `{u16 idx; u16 mode}` through `0026F470` (queue   <- corrected 2026-10-02, OPUS: not a message post - "
     "0026F470 walks the EFB binding table qword[02F8F228] (row count word[02F8F23A], not a queue and a channel) and "
     "builds an effect for every row whose channel byte +4 equals idx and whose enable byte +7+value is set "
     "(0026F522-0026F53B); {2, idx, mode} is the 0024F680 lookup key (0026FB03-0026FB12), stamped into each built "
     "effect's descriptor (0026F597-0026F5B6)\n"),

    # C-V20: map_ref row words +4 / +6 are loaded zero-extended (00264EF9 movzx word [rax+4]; 00264FB9, 0026DBB2,
    #     0026DBE7 movzx word [rax+6]).
    (MP, "1,315 field rows of 8 bytes `{u16 own pack index, i16 block index, i16, i16}`",
     "1,315 field rows of 8 bytes ~~`{u16 own pack index, i16 block index, i16, i16}`~~ `{u16 own pack index, i16 "
     "block index, u16 area, u16 group}` *(corrected 2026-10-02, OPUS: the last two words are loaded zero-extended — "
     "`movzx` at `00264EF9` (`+4`) and at `00264FB9`, `0026DBB2`, `0026DBE7` (`+6`))*"),
    (CW, "  +0x04  s32  (not read by weather)\n",
     "  +0x04  s32  (not read by weather)   <- corrected 2026-10-02, OPUS: two u16 words as read - +0x04 the area "
     "(movzx 00264EF9), +0x06 the group (movzx 00264FB9 / 0026DBB2 / 0026DBE7)\n"),

    # C-V21: 00210570 can write 01F83530 (00210575 cmp cx, 0x4000 / jge signed; 0021057A movsx rax, cx; 0021057E lea rcx,
    #     [01F83580]; 00210588 mov [rcx+rax*16], rdx) - id 0xFFFB = -5 -> 01F83530; no rip-relative writer.
    (MP, "§4c and OPEN-QUESTIONS CD-2/UQ-83): it is zero-initialised `.data` that no instruction in\n"
         "the image writes — the static route to a writer is exhausted (no rip-relative store, no\n"
         "`lea`, no stored pointer, no absolute-addressing form), so the decode is zero-extension\n"
         "for the process life and the `+0x04` field is an ordinary u32 byte offset.",
     "§4c and OPEN-QUESTIONS CD-2/UQ-83): it is zero-initialised `.data` ~~that no instruction in~~\n"
     "~~the image writes — the static route to a writer is exhausted~~ that no rip-relative instruction writes, though "
     "one indexed store can *(corrected 2026-10-02, OPUS: `00210570` tests `cmp cx, 0x4000` / `jge` signed at "
     "`00210575`, then `movsx rax, cx` and stores at `[01F83580 + id·16]` (`00210588`, `0021058C`), so id `0xFFFB` "
     "= −5 lands on `01F83530`; the route is undriven, not absent — field-record-table-navimapdata.md, the "
     "2026-09-25 scope correction)* (no rip-relative store, no\n"
     "`lea`, no stored pointer, no absolute-addressing form), so the decode is zero-extension\n"
     "~~for the process life~~ while that route stays undriven, and the `+0x04` field is an ordinary u32 byte "
     "offset."),

    # C-V22: 0026D910 is 0x1A2 = 418 B (last 0026DAAD jmp); 00378540 0x3AF = 943 B (last 003788EE ret); 00326500
    #     0x112 = 274 B (last 00326610 jmp short).
    (CC, "`0026D910` (`WorldField_InitializeCurrentFieldRuntimeParameters`, ~44 B)",
     "`0026D910` (`WorldField_InitializeCurrentFieldRuntimeParameters`~~, ~44 B~~, 418 B *(corrected 2026-10-02, "
     "OPUS: its last instruction is the 5-byte `jmp` at `0026DAAD`, so `0x1A2` bytes)*)"),
    (NAV, "`00326500` (`PartyFocus_SelectAndRequestDefaultActor`, ~119 B)",
     "`00326500` (`PartyFocus_SelectAndRequestDefaultActor`~~, ~119 B~~, 274 B *(corrected 2026-10-02, OPUS: its last "
     "instruction is the short `jmp` at `00326610`, so `0x112` bytes)*)"),
    (NAV, "`00378540` (~85 B) —",
     "`00378540` ~~(~85 B)~~ (943 B *(corrected 2026-10-02, OPUS: its last instruction is the `ret` at `003788EE`, so "
     "`0x3AF` bytes, as §2a says)*) —"),

    # C-V23: 003777C0's first bit is 9*(3*sel + slot) - 9 + bitOffset + width - 1 (003777DC / 003777E3 3*sel + slot,
    #     003777E9 x9, 003777F9 lea r10d, [r9-9]); the callers pass slot 1..3, so the entry is 3*sel + slot - 1.
    (MW, "read by 003777C0 (bit base 9*(3*selector+slot)); corpus decode D-7\"\n",
     "read by 003777C0 (bit base 9*(3*selector+slot)); corpus decode D-7\"   # <- corrected 2026-10-02, OPUS - with a "
     "zero-based slot; the callers pass 1..3 and 003777C0 subtracts 9 (003777F9 lea r10d,[r9-9]), so the entry is "
     "3*selector + slot - 1\n"),
    (MW, "```\n9 * (3 * selector + weatherSlotIndex)\n```",
     "```\n9 * (3 * selector + weatherSlotIndex)   <- corrected 2026-10-02, OPUS: for the 1..3 slot the callers pass it "
     "is 9 * (3 * selector + slot - 1) - 003777E9 lea eax,[rcx+rcx*8], 003777F9 lea r10d,[r9-9] (CONTRACT-weather.md "
     "I-4)\n```"),
    (MW, "  bitBase = 9 * (3 * selector + weatherSlotIndex)\n",
     "  bitBase = 9 * (3 * selector + weatherSlotIndex)   <- corrected 2026-10-02, OPUS: 9 * (3 * selector + slot - 1) "
     "for the 1..3 slot the callers pass (003777F9 lea r10d,[r9-9]; CONTRACT-weather.md I-4)\n"),
    (MW, "slot)`, `width` bits read most-significant first — gives",
     "slot)` with the slot zero-based *(corrected 2026-10-02, OPUS: the callers pass `1..3` and `003777C0` takes the "
     "9 bits back off, `003777F9 lea r10d, [r9-9]`; CONTRACT-weather.md I-4)*, `width` bits read most-significant "
     "first — gives"),
    (CV, "whose bit base is `9 × (3 × selector + slot)` ([the MWeather page]",
     "whose bit base is ~~`9 × (3 × selector + slot)`~~ `9 × (3 × selector + slot − 1)` for this call's `1..3` slot "
     "*(corrected 2026-10-02, OPUS: `003777F9 lea r10d, [r9-9]` takes one entry back off; CONTRACT-weather.md I-4)* "
     "([the MWeather page]"),

    # C-V24: +0x1060 is read sign-extended by 0025ACC1, 00262123, 0026214E, 0026217C, 0026593B, 0026D96F (movsx); only
    #     0026D9BB zero-extends.
    (PR, "+0x1060   u8   field runtime parameter        WorldField_InitializeCurrentFieldRuntimeParameters\n",
     "+0x1060   u8   field runtime parameter        WorldField_InitializeCurrentFieldRuntimeParameters   <- corrected "
     "2026-10-02, OPUS: s8 - six of its seven readers sign-extend (movsx at 0025ACC1, 00262123, 0026214E, 0026217C, "
     "0026593B, 0026D96F); only 0026D9BB zero-extends\n"),

    # C-V25: 02099DA8 has a reader (retool.py refs: R 00263E10, W 0026DA26).
    (CW, "sibling `02099DA8` identical (one store, `0026DA26`). Residual:",
     "sibling `02099DA8` ~~identical (one store, `0026DA26`)~~ not identical: one store, `0026DA26`, and one reader, "
     "the getter `00263E10` *(corrected 2026-10-02, OPUS: `retool.py refs 02099DA8`; the 2026-09-30 correction in "
     "§14)*. Residual:"),

    # C-V26: the tag-24 entry +0xC0 is written only inside 002F6AB0 - zeroed at 002F6FA5, marked at 002F701D-002F7037
    #     for bit-30 records (entry word[rec+0x14], value r8 = 0x00000000FFFFFFFF from 002F6FD8 mov r8d, -1), then
    #     allocated for every marked entry at 002F71F0-002F7211; 002F4520 and 002F5550 only read it.
    (MP, "(the periodic tick's post-recovery mark writes `+0xC0` of entry `[+8]`) |",
     "(~~the periodic tick's post-recovery mark writes `+0xC0` of entry `[+8]`~~ the constructor's tag-30 expansion "
     "marks `+0xC0` of the entry a bit-30 record names, and a later loop in the same body allocates it *(corrected "
     "2026-10-02, OPUS: `002F701D`–`002F7037` and `002F71F0`–`002F7211` are inside `002F6AB0`; the table's other users "
     "`002F4520`, `002F5450` and `002F5550` were read for `+0xC0` and none writes it)*) |"),
    (MP, "honoring the bit-30 post-recovery mark by writing `-1` into the\n"
         "unit's `0xE0` presentation entry `+0xC0` (`002F701D`–`002F7037` — the periodic-tick contract),",
     "honoring the bit-30 ~~post-recovery mark~~ tag-24 link by writing `-1` into the\n"
     "~~unit's~~ linked `0xE0` presentation entry `+0xC0` (`002F701D`–`002F7037` ~~— the periodic-tick contract~~, "
     "in this constructor at pack bind, not in a periodic tick *(corrected 2026-10-02, OPUS: the entry index is "
     "`word[rec+0x14]`, `002F7025`; the stored qword is `0x00000000FFFFFFFF` from `002F6FD8 mov r8d, 0xffffffff`; "
     "`002F71F0`–`002F7211` then allocate every marked entry)*),"),

    # C-V27: 00379860's argument takes the debug override when positive (00262167 call 0017D490 / test / jle;
    #     00262170 call 0017D490; else 00262177-00262183), as the two 0026FAD0 posts do (0026210E-0026212A,
    #     00262139-00262155).
    (CW, "       -> 00379860(committedSlot+1) ; 00379290 ; 003DE920(0,1,0) ; 00363B40\n",
     "       -> 00379860(committedSlot+1) ; 00379290 ; 003DE920(0,1,0) ; 00363B40   <- corrected 2026-10-02, OPUS: "
     "00379860 takes 0017D490() when positive, else committedSlot+1 (00262167-00262187), the same override the two "
     "0026FAD0 posts take (0026210E-0026212A, 00262139-00262155)\n"),

    # C-V28: the success path of 00377BA0 has no 0xFFF mask (00377BD4 movzx edx, byte [..+9] / 00377BDD movzx ecx,
    #     byte [..+8] / 00377BE2 shl edx, 8 / 00377BE5 add / 00377BE7 shr edx, 0xC / 00377BEA and edx, 3 / 00377BF3 ret);
    #     00377BF4 is the missing-table path.
    (CFA, "the compared kind bytes (`00377BD4`/`00377BDD`), and the value is\n"
          "masked to `0xFFF` (`00377BF4`) — matching the documented `shr 0xC /",
     "~~the compared kind bytes~~ the two bytes of the flags `u16`, combined by `00377BE2 shl edx, 8` / `00377BE5 add` "
     "(`00377BD4`/`00377BDD`), ~~and the value is~~\n"
     "~~masked to `0xFFF` (`00377BF4`)~~ and the success path has no `0xFFF` mask: `00377BF4` is the missing-table "
     "path's failure constant *(corrected 2026-10-02, OPUS: `00377BE7 shr edx, 0xC` / `00377BEA and edx, 3` / "
     "`00377BF3 ret`)* — matching the documented `shr 0xC /"),

    # Counts. C-S11 / CW section 3: 0026D910 stores four globals - 02099DA8 (0026DA26), 02099DAC (0026DA3C, 0026DA4E),
    #     02099DB0 (0026DA5B), 02099DBC (0026D946, 0026DA7D).
    (CW, "The subsystem owns **two persistent bytes, five published globals and one authored table shape**.",
     "The subsystem owns **two persistent bytes, ~~five published globals~~ four published globals and one authored "
     "table shape** *(corrected 2026-10-02, OPUS: `0026D910` stores `02099DA8` (`0026DA26`), `02099DAC` "
     "(`0026DA3C`, `0026DA4E`), `02099DB0` (`0026DA5B`) and `02099DBC` (`0026D946`, `0026DA7D`); the old fifth was the "
     "selector, which is the first persistent byte)*."),
    # C-S34: five payload-getter call sites, all before the tail jump 0026DAAD; 0026D957 jne skips 0026D959 when
    #     +0x1061 is set.
    (CW, "(`002EF2B0`, 20 B) — obtained **four separate times** inside one `0026D910` call\n"
         "(`0026D94C`, `0026D959`, `0026D96A`, `0026D9AF`, `0026DA83`; five call sites, four of them before\n"
         "the tail).",
     "(`002EF2B0`, 20 B) — obtained ~~**four separate times**~~ **five times, or four while `+0x1061` is set,** inside "
     "one `0026D910` call\n"
     "(`0026D94C`, `0026D959`, `0026D96A`, `0026D9AF`, `0026DA83`; five call sites, ~~four of them before~~\n"
     "~~the tail~~ all five before the tail jump at `0026DAAD`; `0026D957 jne` skips `0026D959` while the flag is set) "
     "*(corrected 2026-10-02, OPUS: read in order through `0026D910`)*."),
    # C-S35 + G-12: 02099DB4 is read by eight cmp sites and the getter 00265450 (mov eax); 0026D910 stores neither
    #     02099DB4 (writers 002628B0, 00263050, 00263230, 00266D10, 0026CE60) nor 02099DB8 (writers 0025B500,
    #     0025C830, 002628B0, 00266D10).
    (CW, "> `02099DA8`–`02099DBC` is written together by `0026D910` and read through dedicated 7-byte",
     "> `02099DA8`–`02099DBC` is ~~written together by `0026D910`~~ written by `0026D910` except `02099DB4` and "
     "`02099DB8`, which it never stores *(corrected 2026-10-02, OPUS: `retool.py refs 02099DB4 02099DBB` — `02099DB4` "
     "is written by `002628B0`, `00263050`, `00263230`, `00266D10` and `0026CE60`, `02099DB8` by `0025B500`, "
     "`0025C830`, `002628B0` and `00266D10`)*, and read through dedicated 7-byte"),
    (CW, "returns `02099DBC`, `02099DB4` is read by five `cmp` sites (`0026324D`, `00265450`,",
     "returns `02099DBC`, `02099DB4` is read by ~~five `cmp` sites~~ eight `cmp` sites and the 7-byte getter "
     "`00265450` *(corrected 2026-10-02, OPUS: `retool.py refs 02099DB4` — `00265450` is `mov eax, [02099DB4]`, the "
     "other eight are `cmp`)* (`0026324D`, `00265450`,"),
    # C-S33: the entry table lists six; the resolver's invariant is I-6.
    (CW, "The subsystem has **four entry points**, and they are not peers:",
     "The subsystem has ~~**four entry points**~~ **six entry points** in the table below *(corrected 2026-10-02, "
     "OPUS: the table lists six; the four roles are those of `0025ACA0`, `0026D910`, `0026D8F0` and `00265920`)*, "
     "and they are not peers:"),
    (CW, "**and may return the slot it was asked to leave** (I-5). |",
     "**and may return the slot it was asked to leave** (~~I-5~~ I-6 *(corrected 2026-10-02, OPUS: I-6 is the "
     "resolver's invariant; I-5 is the slot bound)*). |"),
    # C-S36: F-1 superseded 2026-09-26 (the Threading paragraph).
    (CW, "safely.** Unchanged and still open.",
     "safely.** ~~Unchanged and still open.~~ *(answered: SUPERSEDED 2026-09-26 — the static half is settled, the "
     "Threading paragraph; 2026-10-02, OPUS)*"),
    (CW, "the frame phase and thread requirements are open (§14.4). A",
     "the frame phase ~~and thread requirements are open~~ is untested, and the thread requirement's static half is "
     "settled *(answered: F-1 SUPERSEDED 2026-09-26, the Threading paragraph; 2026-10-02, OPUS)* (§14.4). A"),
    # C-S37: the softer GB-3 wording (choosing-the-field-environment-variant.md, 2026-09-30).
    (CW, "**`02099DB0` is published and never read.** Two independent facts say so:",
     "**`02099DB0` is published and ~~never read~~ has no reader found** *(corrected 2026-10-02, OPUS: an absence "
     "claim, bounded as the GB-3 residual below states; choosing-the-field-environment-variant.md, 2026-09-30)*. Two "
     "independent facts say so:"),
    (AP, "read by nothing — and is `0` in all 279 shipped lanes",
     "~~read by nothing~~ has no reader found (GB-3) *(corrected 2026-10-02, OPUS: an absence claim bounded by "
     "CONTRACT-weather.md's GB-3 residual)* — and is `0` in all 279 shipped lanes"),

    # C-S1: three of the four "not yet documented" items are documented.
    (R, "- MapRef root and auxiliary data layout\n- Field runtime parameter derivation (`002E3D40` zero-mode path)\n"
        "- The field environment table and target-local environment index resolution\n",
     "- ~~MapRef root and auxiliary data layout~~ *(answered: `map_ref.bin` is decoded — "
     "choosing-the-field-environment-variant.md and CONTRACT-weather.md §3; 2026-10-02, OPUS)*\n"
     "- ~~Field runtime parameter derivation (`002E3D40` zero-mode path)~~ *(answered: `002E3D40` read 2026-09-18 — "
     "choosing-the-field-environment-variant.md and Weather/mweather-resource-format.md; 2026-10-02, OPUS)*\n"
     "- ~~The field environment table and target-local environment index resolution~~ *(answered: the environment "
     "index and its two tables — CONTRACT-weather.md §3 and CONTRACT-field-environment-variant.md; 2026-10-02, "
     "OPUS)*\n"),
    # C-S2: README labels against the pages' front matter, and the seven pages it does not list.
    (R, "### [`Field-Record-Table/`](Field-Record-Table/) - **documented**\n",
     "### [`Field-Record-Table/`](Field-Record-Table/) - ~~**documented**~~ **AUDITED** *(corrected 2026-10-02, OPUS: "
     "both pages' front matter says `status: AUDITED`)*\n"),
    (R, "### [`Map-Pack/`](Map-Pack/) - **documented 2026-09-12**\n",
     "### [`Map-Pack/`](Map-Pack/) - ~~**documented 2026-09-12**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the "
     "page's front matter says `status: AUDITED`)*\n"),
    (R, "Found by audit, not by reading.\n\n### [`Map-Pack/`]",
     "Found by audit, not by reading.\n"
     "- [`field-record-table-navimapdata.md`](Field-Record-Table/field-record-table-navimapdata.md) - "
     "`navimapdata.bin`, the 3-byte field record and its seven accessors - **AUDITED** *(corrected 2026-10-02, OPUS: "
     "a page this list omitted, added with the status its front matter states)*\n\n### [`Map-Pack/`]"),
    (R, "discarded for the loose `.efb`.\n\n### Not yet documented",
     "discarded for the loose `.efb`.\n\n"
     "### Root pages (added 2026-10-02, OPUS)\n\n"
     "- [`walking-into-an-authored-trigger-point.md`](walking-into-an-authored-trigger-point.md) - authored field "
     "trigger points - **AUDITED**\n"
     "- [`CONTRACT-authored-trigger-points.md`](CONTRACT-authored-trigger-points.md) - **CONTRACT READY**\n"
     "- [`choosing-the-field-environment-variant.md`](choosing-the-field-environment-variant.md) - the field "
     "environment variant - **AUDITED**\n"
     "- [`CONTRACT-field-environment-variant.md`](CONTRACT-field-environment-variant.md) - **CONTRACT READY**\n"
     "- [`CONTRACT-field-record-accessors.md`](CONTRACT-field-record-accessors.md) - **DIFFERENTIAL TESTED**\n"
     "- [`CONTRACT-weather.md`](CONTRACT-weather.md) - **BEHAVIORALLY UNDERSTOOD**\n"
     "- *(corrected 2026-10-02, OPUS: six root pages this index omitted, added with the status each page's own front "
     "matter states)*\n\n### Not yet documented"),

    # C-S4: the ledger name (functions.tsv) is ...FieldAction.
    (WT, "`BattleUnit_TryTriggerNearbyAuthoredFieldActivation` at **`002F8060`**",
     "~~`BattleUnit_TryTriggerNearbyAuthoredFieldActivation`~~ `BattleUnit_TryTriggerNearbyAuthoredFieldAction` "
     "*(corrected 2026-10-02, OPUS: the ledger name in `functions.tsv`, as this page's crossings section and the "
     "contract use)* at **`002F8060`**"),
    # C-S5: the band is the thirteen Espers (CONTRACT-authored-trigger-points.md section 14, closed 2026-09-23).
    (WT, "kinds is a fact about the band, and neither function says what it is.**",
     "kinds is a fact about the band, ~~and neither function says what it is.~~** *(answered: the band is the "
     "thirteen Espers — CONTRACT-authored-trigger-points.md §14, closed 2026-09-23; 2026-10-02, OPUS)*"),
    (WT, "what `003EC700`'s second argument `3` selects, or what\nthe excluded kind band `0x1B … 0x27` contains.",
     "what `003EC700`'s second argument `3` selects~~, or what~~\n~~the excluded kind band `0x1B … 0x27` contains~~ "
     "*(answered for the band: the thirteen Espers — CONTRACT-authored-trigger-points.md §14; 2026-10-02, OPUS)*."),
    # C-S6: OPUS block 317 executed the body (the contract's own TP-1, TP-2, TP-4 corrections).
    (CTP, "**None.** No experiment executes this body. S-11's runtime cell is not addressed by this contract.",
     "~~**None.** No experiment executes this body.~~ *(answered: OPUS block 317 executed it — the 2026-09-25 "
     "corrections to TP-1, TP-2 and TP-4 and the falsification pass's note; 2026-10-02, OPUS)* S-11's runtime cell is "
     "not addressed by this contract."),
    # C-S7: the environment variant has its own contract.
    (CTP, "**This takes the trigger points**; the environment variant remains\n"
          "> uncontracted and this document does not claim it.",
     "**This takes the trigger points**; ~~the environment variant remains~~\n"
     "> ~~uncontracted and this document does not claim it~~ *(answered: the environment variant has its own "
     "contract, CONTRACT-field-environment-variant.md; 2026-10-02, OPUS)*."),
    (CTP, "| **Uncontracted** | the field environment variant — S-11's remaining page, not claimed here |",
     "| ~~**Uncontracted**~~ **Sibling** | the field environment variant — ~~S-11's remaining page, not claimed here~~ "
     "[`CONTRACT-field-environment-variant.md`](CONTRACT-field-environment-variant.md) *(answered: contracted "
     "2026-09-22; 2026-10-02, OPUS)* |"),
    (CTP, "- The field environment variant, S-11's other uncontracted page.",
     "- ~~The field environment variant, S-11's other uncontracted page.~~ *(answered: "
     "CONTRACT-field-environment-variant.md contracts it; 2026-10-02, OPUS)*"),

    # C-S10: the "fourth" count was struck on the variant page 2026-09-30.
    (CEV, "a body is what a reader believes.* The\n"
          "> variant page records this as the **fourth** distinct way this executable's decompiled output has\n"
          "> misdescribed a function boundary, and the only one of the four that is about the body rather than\n"
          "> the return.",
     "a body is what a reader believes.* ~~The~~\n"
     "> ~~variant page records this as the **fourth** distinct way this executable's decompiled output has~~\n"
     "> ~~misdescribed a function boundary, and the only one of the four that is about the body rather than~~\n"
     "> ~~the return.~~ *(answered: the variant page struck that count on 2026-09-30 — the three earlier cases are not "
     "cited, so it has no anchor; 2026-10-02, OPUS)*"),
    # C-S11: section 14's first two items are answered (choosing-the-field-environment-variant.md, 2026-09-30).
    (CEV, "- What the five globals feed — published here, consumed elsewhere.\n"
          "- What the three variants mean to a player; three states exist and nothing names them.",
     "- ~~What the five globals feed — published here, consumed elsewhere.~~ *(answered: the four globals' readers are "
     "censused in CONTRACT-weather.md §5 — `00263E10`, `00263E20`, `00264D50`, and none found for `02099DB0`; "
     "choosing-the-field-environment-variant.md, reconciled 2026-09-30; 2026-10-02, OPUS)*\n"
     "- ~~What the three variants mean to a player; three states exist and nothing names them.~~ *(answered: the "
     "selector is the field's weather slot — choosing-the-field-environment-variant.md and CONTRACT-weather.md §1; "
     "2026-10-02, OPUS)*"),
    # C-S12: the selector is the persistent payload byte +0x1060 (021654E0, this contract's V5).
    (CEV, "**whether any of it reaches the save\n  image is not established here**, and this edge is not evidence that it "
          "does.",
     "~~**whether any of it reaches the save~~\n  ~~image is not established here**, and this edge is not evidence "
     "that it does.~~ *(answered: the selector is the persistent payload byte `+0x1060`, `021654E0` — this contract's "
     "falsification pass V5 and CONTRACT-weather.md §3 — so it is in the save image; 2026-10-02, OPUS)*"),
    # C-S13: the combat side reads the published cells too.
    (CEV, "publish the result for the presentation\nside to read.",
     "publish the result for the presentation\nside to read *(answered: and for the combat side, which reads "
     "`02099DA8` and `02099DAC` through `00263E10` / `00263E20` — CONTRACT-weather.md §5; 2026-10-02, OPUS)*."),

    # C-S15, C-S16: the accessor contract's own open list.
    (CFA, "- What the bit regions mean. The referenced page carries what is known; this contract deliberately\n"
          "  adds nothing to it.",
     "- ~~What the bit regions mean. The referenced page carries what is known; this contract deliberately~~\n"
     "  ~~adds nothing to it.~~ *(answered: the semantics are cited in §2, \"The semantics arrived\", 2026-09-12; "
     "2026-10-02, OPUS)*"),
    (CFA, "left undeclared — see the type store. **Still open**, and",
     "left undeclared — see the type store. ~~**Still open**~~ *(answered: the magic `'N''A''V'` `0x02` — "
     "field-record-table-navimapdata.md's file layout and this contract's own table row; 2026-10-02, OPUS)*, and"),

    # C-S18: 00378540 installs seven publishers (seven 0032E620 submissions).
    (NAV, "**Three were read here; two more\nwere found on 2026-09-08 and are marked below.** The routine is 943 bytes "
          "and has been read only\nat the registration sites an operand scan pointed to, so five is a floor, not a "
          "total:",
     "~~**Three were read here; two more~~\n~~were found on 2026-09-08 and are marked below.**~~ The routine is 943 "
     "bytes ~~and has been read only~~\n~~at the registration sites an operand scan pointed to, so five is a floor, "
     "not a total~~ and installs seven *(answered: the 2026-09-14 note below; `00378540` makes seven `0032E620` "
     "submissions; 2026-10-02, OPUS)*:"),
    (NAV, "because **the string keys were not read** — only",
     "because ~~**the string keys were not read**~~ *(answered: decoded 2026-09-14, the note above; 2026-10-02, "
     "OPUS)* — only"),
    (NAV, "| 943 B | requests all three map tables |",
     "| 943 B | requests ~~all three map tables~~ seven authored tables *(corrected 2026-10-02, OPUS: seven "
     "`0032E620` submissions in `00378540`; §2a's 2026-09-14 note)* |"),
    (NAV, "request (9,39) gramap_weatherinfo.bin -> 00378F70 -> 02ADD0B0\n",
     "request (9,39) gramap_weatherinfo.bin -> 00378F70 -> 02ADD0B0   <- corrected 2026-10-02, OPUS: four more "
     "requests follow - seven 0032E620 submissions in 00378540 (section 2a)\n"),
    # C-S19: the AiOrder_EvaluateTargetSelector consumer was read 2026-09-12 (00303043-0030304D).
    (NAV, "1,154 fields.** The `AiOrder_EvaluateTargetSelector` use is **not** examined, so **PROPOSED-repos2d-2 stays "
          "open**.",
     "1,154 fields.** ~~The `AiOrder_EvaluateTargetSelector` use is **not** examined, so **PROPOSED-repos2d-2 stays open**.~~ "
     "*(answered: examined 2026-09-12 — one selector predicate compares the raw value with its operand, "
     "`00303043`–`0030304D`; 2026-10-02, OPUS)*"),
    (NAV, "do nothing.\n      **The `AiOrder_EvaluateTargetSelector` consumer is still unread, so this box stays "
          "unticked.**",
     "do nothing.\n      ~~**The `AiOrder_EvaluateTargetSelector` consumer is still unread, so this box stays unticked.**~~ "
     "*(answered: read 2026-09-12, `00303043`–`0030304D`, as C-11's box records; 2026-10-02, OPUS)*"),
    # C-S20: 020927E0 is the R2 force-fight toggle.
    (NAV, "**What the toggle is remains unnamed** — that is 15-Input's to close, and this session does not",
     "~~**What the toggle is remains unnamed** — that is 15-Input's to close~~ *(answered: `020927E0` is the R2 "
     "force-fight toggle, this page's 2026-09-12 note; 2026-10-02, OPUS)*, and this session does not"),
    (B15, "predicate forces its toggle off; what the toggle *is* remains open and belongs to 15-Input.",
     "predicate forces its toggle off; ~~what the toggle *is* remains open and belongs to 15-Input~~ *(answered: the "
     "R2 force-fight toggle, as this bullet's 2026-09-30 marker says; 2026-10-02, OPUS)*."),
    # C-S21: crossref_clean is true in the front matter.
    (NAV, "- `audit_crossrefs.py` has not yet been run against this document — `crossref_clean: false`.",
     "- ~~`audit_crossrefs.py` has not yet been run against this document — `crossref_clean: false`.~~ *(answered: "
     "run since — the front matter says `crossref_clean: true`; 2026-10-02, OPUS)*"),
    # C-S22: status 31 is X-Zone in the name bank.
    (NAV, "cannot be reversed.\"* — **Vanished** |",
     "cannot be reversed.\"* — ~~**Vanished**~~ **X-Zone** *(corrected 2026-10-02, OPUS: status 31's name in bank 5, "
     "this page's 2026-09-26 note)* |"),
    (NAV, "| 31 | Vanished | 0 |",
     "| 31 | ~~Vanished~~ X-Zone *(corrected 2026-10-02, OPUS: status 31's name in bank 5)* | 0 |"),
    (B15, "**31 = Vanished**",
     "**31 = ~~Vanished~~ X-Zone** *(corrected 2026-10-02, OPUS: status 31's name in bank 5 — "
     "field-record-table-navimapdata.md, 2026-09-26)*"),
    # C-S23: three masks, two OR'd (this page's correction to sections 2 and 4).
    (B15, "Both effect layers are OR'd (see the",
     "~~Both effect layers are OR'd~~ Two of the three 32-bit status masks, `+0x3C` and `+0x64`, are OR'd "
     "*(answered: see the correction to §2 and §4 below; 2026-10-02, OPUS)* (see the"),

    # C-S25: 02099DBC is the +0x18 boolean table's value, read by 00264D50, second writer 0026AB40.
    (SS, "nothing here reads it back; what it means is not established.",
     "nothing here reads it back; ~~what it means is not established~~ *(answered: it is the `map_ref` `+0x18` "
     "boolean table's entry for the lane's environment index, read through the getter `00264D50`, with a second "
     "writer `0026AB40` — CONTRACT-weather.md §5; 2026-10-02, OPUS)*."),
    # C-S26: 02EC3EA0 is the authored-trigger live-set ring (002F8060 passes it to 002FB3B0 at 002F829D).
    (SS, "reset to `002FA260`'s `02BE3E60` block, same shape, different\nslot array.",
     "reset to `002FA260`'s `02BE3E60` block, same shape, different\nslot array *(answered: that array is the "
     "authored-trigger live-set ring, not weather state — `002F8060` passes `02EC3EA0` to `002FB3B0` at `002F829D`; "
     "CONTRACT-authored-trigger-points.md TP-4; 2026-10-02, OPUS)*."),
    # C-S27: 0017D490 returns dword [001D50D0() + 0xAAC], the debug weather-slot override.
    (AP, "Interior verified: `0017D490()` answers the pending-state count",
     "Interior verified: `0017D490()` ~~answers the pending-state count~~ returns the debug weather-slot override, "
     "`dword [001D50D0() + 0xAAC]` *(corrected 2026-10-02, OPUS: `0017D494 call 001D50D0` / `0017D499 mov eax, "
     "[rax + 0xaac]`; weather-slot-state-model.md §3)*"),
    (AP, "— the\nstored mode plus one, the \"next state\" convention this page's transition roll consumes.",
     "— the\n~~stored mode plus one, the \"next state\" convention this page's transition roll consumes.~~ committed "
     "zero-based slot plus one, the `1..3` slot *(corrected 2026-10-02, OPUS: `0026593B movsx` / `00265942 inc`)*."),
    # C-S29: channels 0 and 0x1F are EFB binding channels (0026FAD0 -> 0026F470, row channel byte +4).
    (CC, "|-> publish to notification channel 0\n",
     "|-> publish to notification channel 0   <- corrected 2026-10-02, OPUS: EFB binding channel 0 - 0026FAD0 -> "
     "0026F470 builds the rows whose channel byte +4 is 0 (0026F534)\n"),
    (CC, "|-> publish to notification channel 0x1F\n",
     "|-> publish to notification channel 0x1F   <- corrected 2026-10-02, OPUS: EFB binding channel 0x1F, as above\n"),
    # C-S30: UQ-89 answered 2026-09-26 - the two bytes are written, nothing reads the entries.
    (CC, "- **Two of the forty bytes are read.** `+0x00` is cleared",
     "- **Two of the forty bytes are ~~read~~ written, and none is read** *(corrected 2026-10-02, OPUS: UQ-89's "
     "answer below — only their initial and per-frame reset values exist, because nothing reads them)*. `+0x00` is "
     "cleared"),
    (CC, "selected-record entries' content) stays open: none of the six",
     "selected-record entries' content) ~~stays open~~ *(answered 2026-09-26: see UQ-89 above — nothing reads them; "
     "2026-10-02, OPUS)*: none of the six"),

    # C-S39, C-S40, C-S41, C-S42: the MWeather page's own later answers, and the two map_ref requests
    #     (002687CF stores the kind-4 buffer at 02099D88, 00268829 the kind-2 buffer at 02099D98).
    (MW, "2026-09-26) has always pointed.*\n",
     "2026-09-26) has always pointed.* *(answered: see the ANSWERED 2026-09-26 note above — the map's wind direction, "
     "read through `0040FF30`; 2026-10-02, OPUS)*\n"),
    (MW, "The widths 4 and 2 are inferred from the offsets being 3 and 7 with a 9-bit total,\nnot read directly.",
     "~~The widths 4 and 2 are inferred from the offsets being 3 and 7 with a 9-bit total,~~\n~~not read directly.~~ "
     "*(answered: the widths are read, not inferred — \"The field widths are read\" below closes this caveat; "
     "2026-10-02, OPUS)*"),
    (MW, "as loader id 9, kinds 4 and 2 (`00268803`–`0026883E`), and that carries",
     "as loader id 9, ~~kinds 4 and 2~~ kind 4 (`00268803`–`00268809`; the kind-2 request at `0026880E`–`0026883E` is "
     "a second file, `test_area_ref.bin`, kept at `02099D98`) *(corrected 2026-10-02, OPUS: `002687CF` stores the "
     "kind-4 buffer at `02099D88` and `00268829` the kind-2 buffer at `02099D98`; "
     "choosing-the-field-environment-variant.md, the two test_ siblings)*, and that carries"),
    (MW, "`003777C0` (144 B) is the 3-bit weather preset body",
     "`003777C0` (144 B) is ~~the 3-bit weather preset body~~ the packed-bit reader the three extractors share, and "
     "the preset is `00377850`'s *(corrected 2026-10-02, OPUS: `retool.py callers 003777C0` — `00377850`, `003777A0` "
     "and `003777B0` all enter it)*"),

    # C-S43, C-S44, C-S45: the map-pack page's own later answers.
    (MP, "## 6. Falsification pass\n\nNot yet run.\n",
     "## 6. Falsification pass\n\n~~Not yet run.~~ *(answered: run 2026-09-13 — §9, Falsification pass 1; "
     "2026-10-02, OPUS)*\n"),
    (MP, "`+0x20C`'s writer is outside\n`002F6AB0` (residue).",
     "~~`+0x20C`'s writer is outside~~\n~~`002F6AB0` (residue).~~ *(answered: `ctx+0x20C` was never a standalone "
     "field — the closure further down this section; 2026-10-02, OPUS)*"),
    (MP, "| `00466E70` (1453 B handler, unread) |",
     "| `00466E70` (1453 B handler, ~~unread~~ read: it builds the `02EBB6E0` slot family *(answered: the tag table's "
     "row 23, interior verified 2026-09-17; 2026-10-02, OPUS)*) |"),
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
