"""apply_05spawn.py [--apply] - 05-Spawn-Encounter-Lifecycle readiness map (cloud-reports/re-readiness/05-spawn.md),
section 2.3 contradictions A1-A18 and B1-B5 settled at the shipping image, plus its C (stale / banner) items, on the
pages (OPUS, 2026-10-02).

The map was written from a text snapshot without the executable, so every A and B item was re-decided at the
instructions (retool.py over the certified image; verdicts and deciding addresses in the OPUS scratch file
verdicts-05.md). Each edit strikes the side the bytes refute and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*
with the deciding address, or marks a stale claim *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`# <- corrected 2026-10-02, OPUS - ...` comment instead of a strike (their OLD includes the line end, so NEW never
contains OLD). One front-matter line (SPR last_pass_state, C6) gets the same trailing comment; one heading (GC, C18)
changes and names OPUS.
Left out: A1/A3/A6 sides the bytes confirm (no edit there); B3 (the member TSV is a generated census, regenerate it,
do not strike it); B4 (script-corpus counts, not decidable at the image); C4/C10 (already annotated); C20 (names kept
knowingly); C21/C24/C25 (no side decided).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "05-Spawn-Encounter-Lifecycle/"
README = F + "README.md"
SPR = F + "spawn-placement-and-retirement.md"
HT = F + "spawn-placement-height-and-authored-tunables.md"
WHY = F + "why-the-enemies-you-killed-come-back.md"
CSP = F + "CONTRACT-spawn-placement.md"
CGC = F + "CONTRACT-group-completion-and-respawn.md"
GC = F + "Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md"
FM = F + "Spawn-Record/the-spawn-keep-entry-field-map.md"

ARMB = ("`002EA4C5` registers the guard `002E70A0` in slot 0xC (`0041D6C0` stores `[02CA4410 + 0xC*8]` = `02CA4470`), "
        "the engine calls the slot at `0041DC9E`/`0041DD1D`/`0041CEE3`, `002E70B0` is `jne 003250F0`, and `003251A4` "
        "calls `00307110`")
CLEAR = "`and dword ptr [rcx], 0xffffff7a`"

EDITS = [
    # A1: the dead-mask bit is a sign-extended 32-bit shift (00306F6F mov eax, 1 / 00306F74 shl eax, cl /
    #     00306F76 cdqe / 00306F78 or [rdx+8], rax). C-GC is right; GC's section 5 pseudocode is not.
    (GC, "            L->deadMask |= (1ull << lane);\n",
     "            L->deadMask |= (1ull << lane);   # <- corrected 2026-10-02, OPUS - a sign-extended 32-bit shift, "
     "(int64)(int32)(1u << (lane & 31)); 00306F6F mov eax, 1 / 00306F74 shl eax, cl / 00306F76 cdqe / 00306F78 "
     "or [rdx+8], rax; contract section 12\n"),

    # A2: storage is a plain 16-bit word; the getter 00264D20 zero-extends (00264D3D movzx), the operand consumer
    #     00321190 sign-extends the getter's result (003211BD call 00264D20; 003211C2 movsx ecx, ax). Both partly.
    (CGC, "the element is **signed**: the consumer",
     "~~the element is **signed**~~ the element is a plain 16-bit word, read unsigned by the getter `00264D20` "
     "(`00264D3D` `movzx`) and signed by this consumer *(corrected 2026-10-02, OPUS: signedness is per reader - "
     "`003211BD` `call 00264D20`, then `003211C2` `movsx ecx, ax`)*: the consumer"),
    (GC, "`0026ADC0(index, value)` stores `value` as a `u16` into a 64-entry table",
     "`0026ADC0(index, value)` stores `value` as a ~~`u16`~~ 16-bit word *(corrected 2026-10-02, OPUS: the store "
     "carries no sign; the getter `00264D20` zero-extends it at `00264D3D`, and its consumer `00321190` sign-extends "
     "that result at `003211C2` `movsx ecx, ax`, so signedness is per reader)* into a 64-entry table"),

    # A3: the continuous-entry match is (f & 2) && (f & 5) && b17 (00235413 test r8b, 2 / je; 00235419 test r8b, 5 /
    #     je; 0023541F cmp r9b, [rax+0x17]). FM's +0x17 row is right; FM section 4 keeps the "neither" reading.
    (FM, "**The continuous-entry match**: `history[j].flags & 2 && !(history[j].flags & 5) && history[j].b_17 == "
         "live.b_17`",
     "**The continuous-entry match**: ~~`history[j].flags & 2 && !(history[j].flags & 5) && history[j].b_17 == "
     "live.b_17`~~ `history[j].flags & 2 && (history[j].flags & 5) && history[j].b_17 == live.b_17` *(corrected "
     "2026-10-02, OPUS: `00235413` `test r8b, 2` / `je` skip, `00235419` `test r8b, 5` / `je` skip, `0023541F` "
     "`cmp r9b, byte ptr [rax + 0x17]`; the `+0x17` row in §2.2 already says so)*"),

    # A4: bits 0, 2 and 7 are cleared by 00236860 (002368AA) and 00237080 (00237085), unconditionally, and by
    #     0023A2E0 (0023A34E) on fresh entries only - all three with and ..., 0xFFFFFF7A.
    (FM, "| `0023A410` (`0023A46F`), `00239840` (`002398C2`, with bit 2) |",
     "| `0023A410` (`0023A46F`), `00239840` (`002398C2`, with bit 2); `00236860` (`002368AA`) and `00237080` "
     "(`00237085`), unconditionally, with bits 2 and 7 *(corrected 2026-10-02, OPUS: both " + CLEAR + "; "
     "`0023A2E0`'s same mask at `0023A34E` runs only on fresh entries, where bits 0 and 2 are already clear)* |"),
    (FM, "| `0023A410` (`0023A465`), `00239840` (`002398C2`) |",
     "| `0023A410` (`0023A465`), `00239840` (`002398C2`); `00236860` (`002368AA`) and `00237080` (`00237085`), "
     "unconditionally *(corrected 2026-10-02, OPUS: both " + CLEAR + ")* |"),
    (FM, "| `0030FED0` does not clear it — nothing found does |",
     "| `0030FED0` does not clear it — ~~nothing found does~~ `00236860` (`002368AA`) and `00237080` (`00237085`) "
     "do, and `0023A2E0` (`0023A34E`) on fresh entries *(corrected 2026-10-02, OPUS: each masks the flags with "
     "`0xffffff7a`, clearing bits 0, 2 and 7)* |"),
    (FM, "`005104D0`): the same clears for one entry |",
     "`005104D0`): ~~the same clears for one entry~~ `0023A2E0`'s mask for one entry, applied without the fresh test, "
     "and `+0x17` zeroed rather than restored *(corrected 2026-10-02, OPUS: `002368AA` " + CLEAR + " runs on any mapped "
     "entry; `002368B0` `mov word ptr [rcx + 0x16], 0xff` writes `+0x17` = 0)* |"),
    (FM, "minus `00236860`'s `+0x17` restore.",
     "~~minus `00236860`'s `+0x17` restore~~ the same four stores as `00236860`, which restores no `+0x17` either "
     "*(corrected 2026-10-02, OPUS: `00237085`–`00237098` and `002368AA`–`002368BD` match store for store; both zero "
     "`+0x17` through the word store at `+0x16`)*."),

    # A5: +0x14 is the steal-flag byte (0023A7AE-0023A7D3 [rbp+0x14], rbp = the keep entry); the enmity block is
    #     +0x19 (decay) and +0x1A..+0x41 (0032156D / 00321D61 lea [rax+0x19]; bound 0x28 at 00321DA3). FM is right.
    (SPR, "2 authored point +0x14.. bEnmityTableHeader + aEnmityByCombatantId[0x2E]\n",
     "2 authored point +0x14.. bEnmityTableHeader + aEnmityByCombatantId[0x2E]   # <- corrected 2026-10-02, OPUS - "
     "+0x14 is bStealAvailabilityFlags (0023A7AE-0023A7D3); the decay byte is +0x19 and the enmity table "
     "+0x1A..+0x41, 40 bytes (0032156D, 00321D61, bound 0x28 at 00321DA3); the field map is the authority\n"),
    (SPR, "The per-entry\nfield offsets in §4 stand;",
     "~~The per-entry~~\n~~field offsets in §4 stand;~~ The per-entry field offsets in §4 do not all stand - its "
     "`+0x14..` enmity label is wrong: `+0x14` is the steal-flag byte and the enmity block is `+0x19..+0x41` "
     "*(corrected 2026-10-02, OPUS: `0023A7AE`–`0023A7D3` write the steal bits at `[rbp + 0x14]`; `0032156D` and "
     "`00321D61` `lea …, [rax + 0x19]`, loop bound `0x28` at `00321DA3`; the field map is the authority, §8g)*;"),

    # A6: 0208E6A0 is the battle-unit slot count (only writer 002368D0: 002368EB mov eax, 0x20 / 002368FE store;
    #     loops bound on cmp ebx, [0208E6A0]). FM's "bank flag" is wrong; no bank flag was located.
    (FM, "`0208E698` the history bank; `0208E6A0` the bank flag |",
     "`0208E698` the history bank; ~~`0208E6A0` the bank flag~~ *(corrected 2026-10-02, OPUS: `0208E6A0` is the "
     "battle-unit slot count, 32 - its only writer `002368D0` stores `0x20` (`002368EB`/`002368FE`) and the unit "
     "loops bound on `cmp ebx, [0208E6A0]`; no bank flag was found)* |"),

    # A7: the slot flag is 00234DA0's FIFTH argument (00234DC3 mov r12d, [rsp + 0xb0] = the first stack argument
    #     after 7 pushes and sub 0x50; callers 00234C2B / 003080C0 store it at [rsp + 0x20]). It is 00234AF0's sixth.
    (CSP, "  * Its sixth argument decides eligibility.",
     "  * Its ~~sixth argument~~ fifth argument (`00234AF0`'s sixth) decides eligibility *(corrected 2026-10-02, "
     "OPUS: `00234DC3` `mov r12d, dword ptr [rsp + 0xb0]` is the first stack argument; both callers store it at "
     "`[rsp + 0x20]`, `00234C2B` and `003080C0`; P0 below agrees)*."),

    # A8: the mode-2 retire threshold is the battle unit's +0x4C (0023519C movss xmm6, [rsi+0x4c], rsi = 0031B760()
    #     at 002350F3-002350F8; mode byte +0x50 at 00235162, point id +0x51 at 0023518A). Keep +0x04 is another field.
    (FM, "| `+0x04` | f32 | `flLifecyclePointThreshold` (placement page) ✓ |",
     "| `+0x04` | f32 | ~~`flLifecyclePointThreshold` (placement page) ✓~~ *(no GFZ name)* - not the placement "
     "page's mode-2 threshold, which is the battle unit's `+0x4C` *(corrected 2026-10-02, OPUS: `0023519C` "
     "`movss xmm6, dword ptr [rsi + 0x4c]` with `rsi` = `0031B760()`, the battle unit, `002350F3`–`002350F8`; mode "
     "at unit `+0x50`, point id at `+0x51`)* |"),
    (FM, "  +0x04 f32  lifecycle threshold (|value|; sign chose b3/b6)\n",
     "  +0x04 f32  lifecycle threshold (|value|; sign chose b3/b6)   # <- corrected 2026-10-02, OPUS - not the mode-2 "
     "retire threshold (unit +0x4C, 0023519C); read only by 00308040 (003080D0)\n"),

    # A9: 0208D45C is a field-frame counter - 0032A100 increments it (0032A135) once per 00234590 call (002345CA)
    #     when the frame float changed; the divisor is 30 x 01DFE0B8 = 30 or 60 (2.0 stored at 001EDDD8).
    (CGC, "> 00235FFA  call 0x32A150                ; the 30 Hz tick counter at 0208D45C\n",
     "> 00235FFA  call 0x32A150                ; the 30 Hz tick counter at 0208D45C   # <- corrected 2026-10-02, OPUS "
     "- a field-frame counter, not 30 Hz; 0032A100 increments it once per 00234590 frame (0032A135), and the "
     "divisor below is 30 x [01DFE0B8] = 30 or 60 (2.0 stored at 001EDDD8)\n"),

    # A10: neither 00233440 nor 00233550 saves or restores the stamp 02089374 or the window 0208936C; only the
    #      field-id pair (00233529-0023353A; 002335B9-002335C7). The window test reads the stamp at 002337F0.
    (SPR, "`00233550`. The return window therefore survives a save/load in both directions.",
     "`00233550`. ~~The return window therefore survives a save/load in both directions.~~ The field-id pair survives "
     "a save/load; the transition stamp `02089374` and the window setting `0208936C` do not *(corrected 2026-10-02, "
     "OPUS: `00233440` stores only `02089372`/`02089370` at buffer `+0x00`/`+0x02` (`00233529`–`0023353A`) and "
     "`00233550` restores only those (`002335B9`–`002335C7`); the window test reads `02089374` at `002337F0`; §2)*."),

    # A11: the selector compares natively (002358D1 sub ecx, [r14+0xc] / 002358D5 cmp ecx, eax / 002358D7 jb skip,
    #      i.e. re-admits at elapsed >= cooldown); the three accessors are not the only readers.
    (CGC, "     -> the three record accessors                     [THE ONLY READERS]\n",
     "     -> the three record accessors                     [THE ONLY READERS]   # <- corrected 2026-10-02, OPUS - "
     "not the only readers; Spawn_SelectAndPrepareAutomaticEntry reads +0x08/+0x0A/+0x0C/+0x10 directly "
     "(002358A1-002358D7), section 2\n"),
    (CGC, "**Nothing native relates the two\n> values**:",
     "**~~Nothing native relates the two~~\n> ~~values~~** *(corrected 2026-10-02, OPUS: "
     "`Spawn_SelectAndPrepareAutomaticEntry` relates them natively - `002358D1` `sub ecx, dword ptr [r14 + 0xc]`, "
     "`002358D5` `cmp ecx, eax`, `002358D7` `jb` skips while elapsed < cooldown; the 2026-09-29 correction in §2)*:"),
    (CGC, "**The comparison is made in authored script or not at\n> all**, so the unit is a script-side convention.",
     "**~~The comparison is made in authored script or not at~~\n> ~~all~~** **the scripts compare with `>` and the "
     "selector natively with `>=`**, ~~so the unit is a script-side convention~~ and both read it as whole seconds "
     "*(corrected 2026-10-02, OPUS: the selector divides the frame counter by `30 × [01DFE0B8]` at `002357F9`)*."),
    (GC, "**yes — the only consumer compares it with the elapsed seconds.**",
     "**yes — ~~the only consumer~~ the script consumer compares it with the elapsed seconds.** *(corrected "
     "2026-10-02, OPUS: `Spawn_SelectAndPrepareAutomaticEntry` compares it too, below)*"),
    (GC, "and by script, not native code;",
     "and by script~~, not native code~~ *(corrected 2026-10-02, OPUS: and natively - "
     "`Spawn_SelectAndPrepareAutomaticEntry` skips while elapsed < cooldown, `002358D1`–`002358D7` `sub`/`cmp`/`jb`, "
     "so it re-admits at elapsed ≥ cooldown; the contract's 2026-09-29 correction)*;"),

    # A12: a mode != 1 completion posts - ARMB, and 00307110 clears bit 47 (0030711A) and sets flags bit 0 (00307133).
    (GC, "**So the static reading of arm B is: bit 47 is set, `0x2008` is played, and nothing observed\n"
         "> clears bit 47 or raises the ledger flag.** Only mode-1 groups post their completion to slot 3.",
     "**~~So the static reading of arm B is: bit 47 is set, `0x2008` is played, and nothing observed~~\n"
     "> ~~clears bit 47 or raises the ledger flag.~~** ~~Only mode-1 groups post their completion to slot 3.~~ "
     "*(corrected 2026-10-02, OPUS: arm B posts - " + ARMB + ", which clears bit 47 (`0030711A`) and sets the ledger "
     "flag (`00307133`); `EE-12`, §8)*"),
    (GC, "No static route of any enumerated\n"
         "  form reaches them; if they are dead, mode ≠ 1 groups never post their completion.",
     "~~No static route of any enumerated~~\n"
     "  ~~form reaches them; if they are dead, mode ≠ 1 groups never post their completion.~~ *(corrected 2026-10-02, "
     "OPUS: they run and mode ≠ 1 groups post - " + ARMB + ")*"),
    (CGC, "has NO static route (section 10)\n",
     "has NO static route (section 10)   # <- corrected 2026-10-02, OPUS - it has one; 002EA4C5 registers 002E70A0 "
     "in slot 0xC (02CA4470), the engine calls it at 0041DC9E/0041DD1D/0041CEE3, 002E70B0 jne 003250F0, and "
     "003251A4 calls 00307110 (section 10)\n"),

    # A13: 00236140 returns -2 (00236194 mov eax, 0xfffffffe); the three respawn readers return -1 (00235FA4,
    #      00236020, 00236734). "Every accessor" is wrong; C-GC's three-reader statement stands.
    (CGC, "- **Every accessor failure is `-1`**,",
     "- **Every ~~accessor~~ respawn-reader failure is `-1`** *(corrected 2026-10-02, OPUS: in the wider family "
     "`SpawnEntry_GetScriptSelection` `00236140` returns `-2`, `00236194` `mov eax, 0xfffffffe`; the three readers "
     "return `-1` at `00235FA4`, `00236020`, `00236734`)*,"),

    # A14: the ledger has 64 entries - the reset 00307090 walks 02EC13D0..02EC19D0 in 0x60 steps of four 0x18 entries.
    (CGC, "so entries exist for groups 1–5 and there is no slot a 0 could address.",
     "so entries exist for groups ~~1–5~~ 1–64 (the authored corpus uses 1–5) *(corrected 2026-10-02, OPUS: the reset "
     "`00307090` walks `02EC13D0` to `02EC19D0` in `0x60` steps of four `0x18` entries, 64 entries)* and there is no "
     "slot a 0 could address."),

    # A15: 00235AF0 calls 002EF4A0 when any of the four compared values DIFFERS (00235B1E / 00235B27 / 00235B37 jne
    #      0x235b4e -> 00235B76 call); all-equal reaches 00235B48 je 0x235dac, the skip. SPR section 27 is right.
    (SPR, "`002EF4A0` copies the\nmatched row (`00235B76`)",
     "`002EF4A0` ~~copies the~~\n~~matched row~~ copies the `0x6000`-byte block when any of the four compared values "
     "differs *(corrected 2026-10-02, OPUS: `00235B1E`, `00235B27` and `00235B37` `jne 0x235b4e` to the call; only "
     "all-equal reaches `00235B48` `je 0x235dac`, the skip; §27)* (`00235B76`)"),

    # A16: 00233C10 - null path (00233C23 jne not taken): 00233C25 call 002EF640 (lea rax, [02164280]; ret), add
    #      0x4E68C, store 02EBF190 (00233C33), call 0030B6A0 (00233C3A), call 00237DF0 (00233C3F), tail 00237DF0
    #      (00233C48). Stamp != 0x05071901 (00233C4D): tail 00237DF0 at 00233C59. The body ends at 00233CE5 (214 B).
    (WHY, "snapshots the block (`00233C25`)",
     "~~snapshots the block~~ returns the active image, to which `0x4E68C` is added *(corrected 2026-10-02, OPUS: "
     "`002EF640` is `lea rax, [02164280]; ret`; `00233C2A` `add rax, 0x4e68c`)* (`00233C25`)"),
    (WHY, "(`00233C48`/`00233C59` — the null-path first-bind).",
     "(~~`00233C48`/`00233C59` — the null-path first-bind~~ the call at `00233C3F` and the tail at `00233C48` on the "
     "null path, so the reset runs twice there; `00233C59` is the tail for a non-null block whose stamp is not "
     "`0x05071901` (`00233C4D`) *(corrected 2026-10-02, OPUS: `00233C23` `jne 0x233c4d` splits the two paths)*)."),
    (WHY, "`0016D6A0`, `003266C0`, `00311E10`, `00226BD0` ×2\n"
          "(`00233D35`/`00233D59`), `0031B760` (`00233D74`), `00313F60`, `00320A00`\n"
          "(`00233DC4`).",
     "`0016D6A0`, ~~`003266C0`, `00311E10`, `00226BD0` ×2~~\n"
     "~~(`00233D35`/`00233D59`), `0031B760` (`00233D74`), `00313F60`, `00320A00`~~\n"
     "~~(`00233DC4`)~~ and `00229ED0` (`00233CD1`), then zeroes `0208E6B4` (`00233CD6`) and returns at `00233CE5` "
     "*(corrected 2026-10-02, OPUS: the body is 214 B, `00233C10`–`00233CE5`; the struck calls and sites lie past "
     "its `ret`, from `00233D20` on)*."),

    # A17: the slot-0xC dispatch calls are call rax at 0041DC9E / 0041DD1D / 0041CEE3; the cited 0041DC84 /
    #      0041DD03 / 0041CEC6 are the mov rax, [02CA4470] loads and 0041CEC0 the function entry. Both partly.
    (CGC, "(id 6) at `00417CC6`, `call rax` on `[02CA4470]` (id 0xC) at `0041DC84`/`0041DD03`/`0041CEC6`.",
     "(id 6) at ~~`00417CC6`~~ `00417CDF`, `call rax` on `[02CA4470]` (id 0xC) at ~~`0041DC84`/`0041DD03`/`0041CEC6`~~ "
     "`0041DC9E`/`0041DD1D`/`0041CEE3` *(corrected 2026-10-02, OPUS: the struck addresses are the `mov rax, [slot]` "
     "loads; the `call rax` instructions are the ones restated)*."),
    (GC, "(`0041DC84`, `0041DD03`, `0041CEC0`)",
     "(~~`0041DC84`, `0041DD03`, `0041CEC0`~~ `call rax` at `0041DC9E`, `0041DD1D`, `0041CEE3` *(corrected 2026-10-02, "
     "OPUS: the struck sites are the two `mov rax, [02CA4470]` loads and the entry of `0041CEC0`, whose load is at "
     "`0041CEC6`)*)"),

    # A18: a non-spawn-backed unit's height mode is 1 - esi = 1 at 00239E33, not written before 00239FA7; 2 and 3
    #      are later values for +0x1F4 (00239FEC, 00239FF9). The esi path is taken only when pBkbi[5] == 0
    #      (00239FA3 test eax, eax / jne); a null unit or pBkbi goes to the definition path (00239F91, 00239F9D).
    (HT, "00239FA7  mov   ecx, esi                        ; NOT spawn-backed -> esi (1, 2 or 3)\n",
     "00239FA7  mov   ecx, esi                        ; NOT spawn-backed -> esi (1, 2 or 3)   # <- corrected "
     "2026-10-02, OPUS - esi is 1 here (00239E33 mov esi, 1, not rewritten before 00239FA7); 2 and 3 are later "
     "values for +0x1F4 (00239FEC, 00239FF9)\n"),
    (HT, "whose values are 1, 2 and 3 — never 8",
     "whose ~~values are 1, 2 and 3~~ value is 1 *(corrected 2026-10-02, OPUS: `esi` is set to 1 at `00239E33` and "
     "not written again before `00239FA7`; it becomes 2 or 3 only afterwards, for `+0x1F4`, at `00239FEC`/`00239FF9`; "
     "§7 says a party unit gets 1)* — never 8"),
    (HT, "    mode = esi;                                        // 1, 2 or 3 - never 8\n",
     "    mode = esi;                                        // 1, 2 or 3 - never 8   # <- corrected 2026-10-02, OPUS "
     "- esi is 1 here (00239E33); and the test above is pBkbi[5] == 0 (00239FA3 test eax, eax / jne), with a null "
     "unit or pBkbi taking the definition path (00239F91, 00239F9D)\n"),

    # B1: 27 imul r, r, 0x250 sites in 18 functions, 10 in 0043F450 (retool.py grep and a raw .text scan agree).
    (HT, "stride    'imul reg, reg, 0x250' -> 50 sites, concentrated in Spawn*/SpawnKeep*/SpawnEntry*\n",
     "stride    'imul reg, reg, 0x250' -> 50 sites, concentrated in Spawn*/SpawnKeep*/SpawnEntry*   # <- corrected "
     "2026-10-02, OPUS - 27 sites in 18 functions (retool.py grep and a raw .text scan agree), 16 Spawn-owned, 10 in "
     "0043F450; section 12 Finding 3\n"),
    (HT, "The stride sweep found **18 of its 50 sites inside one function**,",
     "The stride sweep found **~~18 of its 50 sites~~ 10 of its 27 sites inside one function** *(corrected 2026-10-02, "
     "OPUS: `retool.py grep` and a raw `.text` scan both give 27 `imul r, r, 0x250` sites in 18 functions, ten of "
     "them in `0043F450`; §12 Finding 3)*,"),

    # B2: 00307140 is 183 B (tail jmp 0x26bd20 at 003071F2, end 003071F7); 00312EE0 is 187 B (ret at 00312F9A;
    #     00312FA0 begins the next function).
    (CGC, "`00307140` (~97 B) — `ecx` switch",
     "`00307140` ~~(~97 B)~~ (183 B *(corrected 2026-10-02, OPUS: the body runs `00307140`–`003071F6`, ending in the "
     "tail `jmp 0x26bd20` at `003071F2`)*) — `ecx` switch"),
    (FM, "`00312EE0` (~208 B) — `qword[+0x698]` null-gated walk",
     "`00312EE0` ~~(~208 B)~~ (187 B *(corrected 2026-10-02, OPUS: `ret` at `00312F9A`; `00312FA0` begins the next "
     "function)*) — `qword[+0x698]` null-gated walk"),

    # B5: the two unread accessors carry the dead arm in another register form (00236071 movzx ecx, al / 00236074
    #     test ecx, ecx / 00236076 js; 002366A3 movzx eax, cl / 002366A6 test eax, eax / 002366A8 js) - all nine.
    (GC, "`00236030` and `00236670` — were\nnot read here, so whether they carry the same branch in a different form "
         "is open.",
     "`00236030` and `00236670` — ~~were~~\n~~not read here, so whether they carry the same branch in a different form "
     "is open.~~ carry it in another register form, so the dead arm is in all nine *(corrected 2026-10-02, OPUS: "
     "`00236071` `movzx ecx, al` / `00236074` `test ecx, ecx` / `00236076` `js`, and `002366A3` `movzx eax, cl` / "
     "`002366A6` `test eax, eax` / `002366A8` `js`)*."),

    # C1-C3: README status lines against front matter, and the five pages it does not index.
    (README, "(spawn-placement-and-retirement.md) — **PARTIAL.**",
     "(spawn-placement-and-retirement.md) — ~~**PARTIAL.**~~ **DOCUMENTED.** *(corrected 2026-10-02, OPUS: the "
     "page's front matter says `status: DOCUMENTED`, owner re-status 2026-10-01)*"),
    (README, "  **DOCUMENTED, tier 1.** The `0x250` spawn-keep entry",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)* The `0x250` spawn-keep entry"),
    (README, "persisted affinity bytes, the stats page, and the three ranges nothing touches.\n\n## How to add a system here",
     "persisted affinity bytes, the stats page, and the three ranges nothing touches.\n"
     "- [`why-the-enemies-you-killed-come-back.md`](why-the-enemies-you-killed-come-back.md) — the two keep banks, "
     "their rotation on area transition and the return window — **AUDITED**\n"
     "- [`spawn-placement-height-and-authored-tunables.md`](spawn-placement-height-and-authored-tunables.md) — the "
     "activation-time height, the minimum-distance flags and the script-installed tunables — **AUDITED**\n"
     "- [`CONTRACT-spawn-placement.md`](CONTRACT-spawn-placement.md) — contract, spawn placement and the return "
     "window — readiness **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md`]"
     "(Group-Completion-And-Respawn/when-a-group-is-wiped-and-when-it-comes-back.md) — the group ledger, completion "
     "and respawn timing — **AUDITED**\n"
     "- [`CONTRACT-group-completion-and-respawn.md`](CONTRACT-group-completion-and-respawn.md) — contract, group "
     "completion and respawn — readiness **CONTRACT READY**\n"
     "- *(corrected 2026-10-02, OPUS: five pages this list omitted, added with the status or readiness each page's own "
     "front matter states)*\n"
     "\n## How to add a system here"),

    # C5: SPR section 11's crossref_clean line against the 2026-10-01 front matter and status line.
    (SPR, "`crossref_clean` is now false because this amended citation surface has not had a fresh graph\naudit.",
     "~~`crossref_clean` is now false because this amended citation surface has not had a fresh graph~~\n~~audit.~~ "
     "*(answered: see the front matter, `crossref_clean` true, and the status line - a fresh graph audit of this page "
     "reports 0 findings, owner re-status 2026-10-01; 2026-10-02, OPUS)*"),

    # C6: SPR front matter last_pass_state (trailing comment, no strike in front matter).
    (SPR, "consumer propagation and remaining caller questions open (§11)\n",
     "consumer propagation and remaining caller questions open (§11)   # <- corrected 2026-10-02, OPUS - superseded by "
     "the status line (2026-10-01); L-12 and L-13 are SUPERSEDED, section 7\n"),

    # C7: HT section 10's status sentence against the front matter (AUDITED, passes 1, crossref_clean true).
    (HT, "`audit_crossrefs.py` has **not** been run against this document, and no independent party has\n"
         "attacked it. `status` is `DOCUMENTED`, `audit.passes` is `0`.",
     "~~`audit_crossrefs.py` has **not** been run against this document, and no independent party has~~\n"
     "~~attacked it. `status` is `DOCUMENTED`, `audit.passes` is `0`.~~ *(answered: see §11 and §12, the later passes, "
     "and the front matter - `status` AUDITED, `audit.passes` 1, `crossref_clean` true; 2026-10-02, OPUS)*"),

    # C8: SPR section 2's L-7 pointer against L-7 ANSWERED in section 7.
    (SPR, "supplies the vertical coordinate is recorded as **L-7**.",
     "supplies the vertical coordinate ~~is recorded as **L-7**~~ is nothing at generation; a terrain probe supplies "
     "it at activation *(answered: see §7, L-7 ANSWERED, and spawn-placement-height-and-authored-tunables.md; "
     "2026-10-02, OPUS)*."),

    # C9: WHY's L-13 "open" lines against SPR section 7 (SUPERSEDED 2026-09-27; 00233550 never reads bank 1 back).
    (WHY, "timer is the open question `L-13` on the retirement page, and nothing here closes it.",
     "timer ~~is the open question `L-13` on the retirement page, and nothing here closes it~~ is nothing: bank 1 is "
     "never read back and the stamp is not restored *(answered: see the retirement page §7, `L-13` SUPERSEDED "
     "2026-09-27 on this static answer, only its live residue open; `00233550` restores the field-id pair at "
     "`002335B9`–`002335C7` and nothing else; 2026-10-02, OPUS)*."),
    (WHY, "did not test them. `L-13` keeps bank 1 and the timer.",
     "did not test them. ~~`L-13` keeps bank 1 and the timer.~~ *(answered: see the retirement page §7 - `L-13` is SUPERSEDED "
     "2026-09-27 on its static answer; only the live residue stays open; 2026-10-02, OPUS)*"),

    # C11 / C12 / C13: EE-11 observed in the shipped scripts (2026-09-13).
    (CGC, "`(group, mode)` by the pop-order law; no decompiled script has confirmed it (`EE-11`).",
     "`(group, mode)` by the pop-order law; ~~no decompiled script has confirmed it~~ *(answered: see §4a and §14 item "
     "8 - observed in 6,746 shipped calls, `EE-11` 2026-09-13; 2026-10-02, OPUS)* (`EE-11`)."),
    (CGC, "| script-side order `(group, mode)` | pop-order law only; no decompiled script | 2 (static) | PROBABLE |",
     "| script-side order `(group, mode)` | pop-order law only; ~~no decompiled script~~ observed in 6,746 shipped "
     "calls *(answered: see §4a, `EE-11` 2026-09-13; 2026-10-02, OPUS)* | ~~2 (static)~~ 2 (static) + authored-data "
     "census | ~~PROBABLE~~ OBSERVED |"),
    (GC, "| Script-side argument order `(group, mode)` | inferred from the pop-order law; no decompiled script seen | 2 "
         "| PROBABLE |",
     "| Script-side argument order `(group, mode)` | inferred from the pop-order law; ~~no decompiled script seen~~ "
     "observed in 6,746 shipped calls *(answered: see §8, `EE-11` 2026-09-13; 2026-10-02, OPUS)* | ~~2~~ 2 + "
     "authored-data census | ~~PROBABLE~~ OBSERVED |"),
    (GC, "second. No\n> shipped script has been decompiled to confirm it — the two `.ebp` files on hand are containers "
         "the\n> decompiler rejects unpacked.",
     "second. ~~No~~\n> ~~shipped script has been decompiled to confirm it — the two `.ebp` files on hand are "
     "containers the~~\n> ~~decompiler rejects unpacked.~~ *(answered: see the next paragraph - `EE-11` observed in "
     "the shipped scripts 2026-09-13; 2026-10-02, OPUS)*"),

    # C14 / C15 / C16: GC section 9 evidence rows answered since.
    (GC, "| Whether `+0x10` is seconds | **not established** | — | UNKNOWN |",
     "| Whether `+0x10` is seconds | ~~**not established**~~ yes, whole seconds - `EE-1` 2026-09-13, and the "
     "selector compares it with seconds natively (`002357F9` divide, `002358D7` `jb`) *(answered: see §8; 2026-10-02, "
     "OPUS)* | ~~—~~ 1 + authored-data census | ~~UNKNOWN~~ PROVEN |"),
    (GC, "| `003250F0`, `00325090`, `00325260` have no static route |",
     "| ~~`003250F0`, `00325090`, `00325260` have no static route~~ *(corrected 2026-10-02, OPUS: refuted - " + ARMB
     + "; `EE-12`, §8)* |"),
    (GC, "| 1 | PROVEN (as a negative over the listed routes) |",
     "| 1 | ~~PROVEN (as a negative over the listed routes)~~ REFUTED |"),
    (GC, "| What the row-12 bits and slot 3's reader are | **not established** | — | UNKNOWN |",
     "| What the row-12 bits and slot 3's reader are | ~~**not established**~~ `EE-8` answered 2026-09-12 (bits 7, "
     "11, 12 and 20 left as residue); `EE-9` answered 2026-09-18 - the zone script sleeps on slot 3 *(answered: see "
     "§8; 2026-10-02, OPUS)* | ~~—~~ 1 + authored-data census | ~~UNKNOWN~~ PROVEN, with the EE-8 residue |"),
    (GC, "which script or operand reads slot 3 is `EE-9`.",
     "~~which script or operand reads slot 3 is `EE-9`~~ the zone script reads slot 3, by `waitv` on `scratch1` "
     "*(answered: see §8, `EE-9` 2026-09-18; 2026-10-02, OPUS)*."),

    # C17: EE-12's handlers were verified statically, not live.
    (GC, "§14, whose EE-12 handlers were verified live)",
     "§14, whose EE-12 handlers were verified ~~live~~ statically, by the slot registration and the engine's "
     "`call rax` sites; no live verification is recorded *(corrected 2026-10-02, OPUS: `002EA4C5`, `0041DC9E`/"
     "`0041DD1D`/`0041CEE3`)*)"),

    # C18: the reset heading - masks zeroed, flags bit 0 only (003070A0-003070AB and byte ptr [...], 0xFE).
    (GC, "### The reset zeroes all three fields — added 2026-09-10",
     "### The reset zeroes ~~all three fields~~ both masks and flag bit 0 only — added 2026-09-10 *(corrected "
     "2026-10-02, OPUS: `003070A0`–`003070AB` are `and byte ptr [...], 0xFE`)*"),

    # C19: the C-GC interface rows below section 4a sit inside the quote with no header.
    (CGC, "Party (kind 0) units never reach the group logic at all.\n| set group id + mode, then register |",
     "Party (kind 0) units never reach the group logic at all.\n\n*(table header restored 2026-10-02, OPUS: the rows "
     "below continue the interface table above §4a; without a blank line and a header they rendered inside the "
     "quote)*\n\n| operation | entry | signature | returns |\n|---|---|---|---|\n| set group id + mode, then register |"),

    # C22: 0043F210 is not a spawn-placement body - sole caller 0043F450 (Presentation) at 0043F488, one call 003697F0.
    (HT, "`0043F210` (159 B) is a spawn-placement body - `003697F0` single call.",
     "`0043F210` (159 B) ~~is a spawn-placement body~~ is not a spawn-placement body: its only caller is the "
     "Presentation function `0043F450` (`0043F488`, §11), and it reads no spawn global or keep entry *(corrected "
     "2026-10-02, OPUS: `retool.py callers 0043F210`, body read)* - `003697F0` single call."),

    # C23: 003C9250 references no ledger, keep bank or spawn global (02B47730; 0035BAD0/0035D3E0/0035DCC0/0035DEB0/
    #      0035DC90; callers 003C87B0, 003C8B70); 003E6770 per FABLE's correction directly above.
    (GC, "`003C9250` (280 B) is a group-respawn body -",
     "`003C9250` (280 B) ~~is a group-respawn body~~ is not shown to be a group-respawn body: it references no ledger, "
     "keep bank or spawn global, and its callers are `003C87B0` and `003C8B70` *(corrected 2026-10-02, OPUS: body "
     "read)* -"),
    (GC, "`003E6770` (276 B) is a group-respawn body -",
     "`003E6770` (276 B) ~~is a group-respawn body~~ is not a group-respawn body *(corrected 2026-10-02, OPUS: see "
     "FABLE's 2026-09-19 correction directly above)* -"),
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
