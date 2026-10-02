"""apply_17render_a.py [--apply] - 17-Presentation-Rendering readiness map (cloud-reports/re-readiness/17-render.md),
section 3.1 value-changing items AC.CV-1 .. GP.CV-9 (report lines 2383-2800, part A), settled at the shipping image
(OPUS, 2026-10-02).

Each edit strikes the side the image REFUTES and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*; every
deciding address inside a function is cited as entry+offset. The verdict table is
scratchpad re17a/verdicts-17a.md (copied into consumer-check.md when this candidate is published).
Items decided with no page wrong, or left undecided, carry no edit: AC.CV-7, RO.CV-7/8/10/18, RA.CV-8/11,
RG.CV-4/9/13/15, CL.CV-6/8/11/12/13/14/15/16, GP.CV-9. Stale/banner items (section 3.3) are part B's.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; no heading changes; no census TSV edits.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "17-Presentation-Rendering/"
RAMP = F + "CONTRACT-authored-command-ramp-channels.md"
HND = F + "Authored-Commands/the-authored-presentation-command-handlers.md"
FEF = F + "Model-And-Motion-Formats/fef-and-motion-entries.md"
CRO = F + "Character-Rendering/character-render-object.md"
CDL = F + "CONTRACT-coast-down-latch.md"
CRR = F + "Character-Render-Records/the-character-render-record-array.md"
RES = F + "Character-Render-Records/render-event-selection-evidence.md"
POOL = F + "CONTRACT-render-record-pool-lifecycle.md"
PUB = F + "CONTRACT-character-transform-publish.md"
LIT = F + "Character-Rendering/how-a-character-is-lit.md"
FADE = F + "Character-Render-Records/how-a-character-fades-the-ten-channels.md"
TRAIL = F + "Character-Render-Records/the-bone-trails.md"
STAT = F + "Character-Render-Records/how-a-status-shows-on-a-character.md"
LOOK = F + "Character-Render-Records/the-staged-look-command.md"
L = F + "Render-Command-List/the-ordered-render-command-list.md"
R = F + "README.md"
C = F + "CONTRACT-render-command-list-and-graphics-handshake.md"
GI = F + "Gi-Render-Commands/gi-render-command-family.md"

T = "*(corrected 2026-10-02, OPUS: "
MASK = "`0018B100`+0x67 `test dword ptr [rsi + 0x20], eax`"

EDITS = [
    # AC.CV-1: 003AFD30's five call sites pass 1 at 0024D9C0+0x65 and 00520800+0x1A, 0 at 003B8670+0x10E4 and
    #     00520800+0x36, r12d at 003B8670+0x1098 - 0 at two sites, not three.
    (RAMP, "**mode values** — 0 at three sites, 1 on `00520800`'s record-`+3`-nonzero path, and `r12d` at",
     "**mode values** — 0 at ~~three~~ two sites (`003B8670`+0x10E4, `00520800`+0x36), 1 on `00520800`'s "
     "record-`+3`-nonzero path and at the presentation reset `0024D9C0`+0x65 " + T + "`mov ecx, 1` precedes the "
     "call at `0024D9C0`+0x65, `xor ecx, ecx` the calls at `003B8670`+0x10E4 and `00520800`+0x36)*, and `r12d` at"),

    # AC.CV-2: the pair callback 004173D0 takes the slot handle from entry +0x35C, not from the command.
    (RAMP, "`0x0D`–`0x10` carries `(slot id, steps, target)` — the two pair classes carry two targets — and",
     "`0x0D`–`0x10` carries ~~`(slot id, steps, target)`~~ `(steps, target)` and no slot id; the callback takes the "
     "slot handle from the presentation entry's `+0x35C` " + T + "`004173D0`+0x13 `mov eax, dword ptr [r8 + 0x35c]`, "
     "`004173D0`+0x2E `movzx edx, byte ptr [rcx + 2]`; section 6)* — the two pair classes carry two targets — and"),

    # AC.CV-3: 003B5C00 steps five channels - the fifth is +0x43 / +0x98 += +0x9C at 003B5C00+0xB0..+0xCD.
    (RAMP, "decrements byte counters `+0..+3` and folds `+0x60`/`+0x64`/`+0x68`/`+0x6C`/`+0x70`/`+0x74`/`+0x78`/`+0x7C` "
           "deltas into the `+0x50`/`+0x54`/`+0x58`/`+0x5C`/`+0x70`/`+0x78` float pairs.",
     "decrements byte counters `+0..+3` ~~and folds `+0x60`/`+0x64`/`+0x68`/`+0x6C`/`+0x70`/`+0x74`/`+0x78`/`+0x7C` "
     "deltas into the `+0x50`/`+0x54`/`+0x58`/`+0x5C`/`+0x70`/`+0x78` float pairs.~~ and `+0x43`, five channels: "
     "counter `+0` folds `+0x60`/`+0x64` into `+0x50`/`+0x54`, `+2` folds `+0x68`/`+0x6C` into `+0x58`/`+0x5C`, `+1` "
     "folds `+0x74` into `+0x70`, `+3` folds `+0x7C` into `+0x78`, and `+0x43` folds `+0x9C` into `+0x98` " + T +
     "the fifth channel is `003B5C00`+0xB0..+0xCD, `movzx ecx, byte ptr [rax + 0x43]` through `movss dword ptr "
     "[rax + 0x98], xmm0`; the five-channel step section 6 states)*."),

    # AC.CV-4: 00520510 (0x3F) passes word +2 as the bone and word +0x10 as preset (& 0xFFF) and flag (>> 15) - GI-15.
    (HND, "which hands the rig's controller 0 a preset (word `+2`; 0 = off), a direction (floats `+4`..`+0xC`), an id "
          "and a flag (word `+0x10`)",
     "which hands the rig's controller 0 ~~a preset (word `+2`; 0 = off), a direction (floats `+4`..`+0xC`), an id "
     "and a flag (word `+0x10`)~~ a bone (word `+2`), a direction (floats `+4`..`+0xC`), a preset (word `+0x10` "
     "masked `0xFFF`; 0 = off) and a flag (word `+0x10` bit 15) " + T + "`00520510`+0x18 reads `word [r8 + 0x10]` "
     "and `00520510`+0x23 `word [rdx + 2]`; the GI-15 section)*"),

    # AC.CV-5 / RO.CV-2: the pool pointer is 022C6F28 (639 references); 02B3EF28 has none; CRO's 02095210 is a
    #     miscomputed rip target (0042EF90+0x2E, next instruction 0042EF90+0x35, gives 022C6F28).
    (HND, "`[02B3EF28]`); record init `0041F730` zeroes",
     "~~`[02B3EF28]`~~ `[022C6F28]` " + T + "`02B3EF28` has no reference in the image; the pool pointer is "
     "`022C6F28`, read by the pool init at `004269A0`+0xF)*); record init `0041F730` zeroes"),
    (FEF, "at `[02B3EF28]` (pool init `004269A0` → `0041F730`: `memset 0x740`, then",
     "at ~~`[02B3EF28]`~~ `[022C6F28]` " + T + "`02B3EF28` has no reference in the image; `004269A0`+0xF reads the "
     "pool pointer `022C6F28`)* (pool init `004269A0` → `0041F730`: `memset 0x740`, then"),
    (CRO, "`[rip+0x1e97f63]` (`02095210`): per node",
     "`[rip+0x1e97f63]` (~~`02095210`~~ `022C6F28` " + T + "the displacement counts from the next instruction, "
     "`0042EF90`+0x35, so the target is the pool pointer `022C6F28`)*): per node"),

    # AC.CV-6 / RA.CV-10: 01DFE0B4 holds 1 in the image; 001EDDC0+0x32 stores 2 only behind 001EDDC0+0x6 (ecx != 0,
    #     the 60 fps switch). The clamp is 90 x timeBase (004256E0+0x545), so the wrap needs timeBase 2.
    (CDL, "The counter is clamped to 180 and",
     "The counter is clamped to ~~180~~ `90 x timeBase`, which is 180 when the time base is 2; at the image value 1 the "
     "clamp is 90, which fits, and the byte never wraps " + T + "`004256E0`+0x545 `imul ecx, dword ptr [01DFE0B4], "
     "0x5a`)*; at 180 it is"),
    (CDL, "(`movsx eax, byte ptr [01DFE0B4]`). Its value is `2`, so",
     "(`movsx eax, byte ptr [01DFE0B4]`). ~~Its value is `2`, so~~ It holds `1` in the image and `2` once "
     "`001EDDC0` runs with a non-zero argument (the 60 fps switch); either value fits a byte, so " + T + "the one "
     "writer `001EDDC0`+0x32 sits behind `001EDDC0`+0x6 `je`, taken when `ecx` is 0)*"),
    (CDL, "                 /* timeBase is 2 -- ONE writer in the image, 001EDDF2 stores the        */\n",
     "                 /* timeBase is 2 -- ONE writer in the image, 001EDDF2 stores the        */   /* <- corrected "
     "2026-10-02, OPUS - the image holds 1; 001EDDC0+0x32 stores 2 only when 001EDDC0 is entered with a non-zero ecx "
     "(the 60 fps switch), so the threshold is 30 or 60 */\n"),

    # AC.CV-8: arming replays the cached pair (00424080+0xD8..+0xFB); the live-to-cache copy is the not-armed path.
    (CRR, "   -> cachedHeading = liveHeading; cachedSpeed = liveSpeed; flags |= 1;\n",
     "   -> cachedHeading = liveHeading; cachedSpeed = liveSpeed; flags |= 1;   // <- corrected 2026-10-02, OPUS - "
     "arming replays the CACHED pair (+0x620 heading, +0x624 speed times 0.83) to the caller and sets +0x62C bit 0 "
     "(00424080+0xD8..+0xFB); the live-to-cache copy runs only when the test fails (00424080+0x105)\n"),

    # AC.CV-9: the allocator 003B56D0 writes +0x30 (qword) and +0xBC..+0xD4 (003B56D0+0x17C..+0x1A7).
    (RAMP, "touch no `+0x30`/`+0x34` either. One writer (`003B5CE0`), zero readers — a",
     "touch no `+0x30`/`+0x34` either~~. One writer (`003B5CE0`)~~, except the allocator `003B56D0`, which zeroes the "
     "pair " + T + "`003B56D0`+0x17C `mov qword ptr [rbx + 0x30], rsi`)*. One value writer (`003B5CE0`), zero "
     "readers — a"),
    (RAMP, "ends at `+0x9C`; the highest written field anywhere is `003B62D0`'s `+0xD4` cache",
     "ends at ~~`+0x9C`~~ `+0xD4`: it also writes `+0xBC`..`+0xD4` " + T + "`003B56D0`+0x180 through `003B56D0`+0x1A7 "
     "`mov dword ptr [rbx + 0xd4], 0x3f800000`)*; the highest written field anywhere is `003B62D0`'s `+0xD4` cache"),

    # AC.CV-10: 00521000 / 00521050 are the 0x2F / 0x14 per-node bodies; the handle-table family starts at 005210F0.
    (HND, "- The `00520xxx` bodies at `00521000`+ (handle-table allocate/resolve/release, `005210F0`/",
     "- The `00520xxx` bodies at ~~`00521000`+~~ `005210F0`+ " + T + "`00521000` and `00521050` are the per-node "
     "bodies the `0x2F` and `0x14` handlers post, `00520E30`+0x1A and `00520E70`+0xA `lea`)* (handle-table "
     "allocate/resolve/release, `005210F0`/"),

    # AC.CV-11: 00520E70 posts 00521050 through 00426870 (00520E70+0xA, +0x11).
    (RES, "| 0x14 | `00520E70` | tail into `0042DC10` region | `00520E70` |",
     "| 0x14 | `00520E70` | ~~tail into `0042DC10` region~~ posts the per-node body `00521050` through `00426870` "
     "with `word[rec + 0]` and the command " + T + "`00520E70`+0xA `lea rdx, [00521050]`, `00520E70`+0x11 `call "
     "00426870`)* | `00520E70` |"),

    # AC.CV-12: 003AF340 stores 1.0 at +0x24/+0x28/+0x34/+0x38 and 0 at +0x2C/+0x30/+0x3C (003AF340+0xC9..+0xE2).
    (FEF, "`+0x24..+0x38` = `1.0`, `+0x1C` = `0x11000000`, `+0x18` =",
     "~~`+0x24..+0x38` = `1.0`~~ `+0x24`/`+0x28`/`+0x34`/`+0x38` = `1.0` and `+0x2C`/`+0x30`/`+0x3C` = 0 " + T +
     "`003AF340`+0xC9..+0xE2; the stores at `+0x28` and `+0x38` are qwords of `0x3f800000`, which zero `+0x2C` and "
     "`+0x3C`, and `+0x30` is stored 0)*, `+0x1C` = `0x11000000`, `+0x18` ="),

    # AC.CV-13: 0xB9 = 1011 1001.
    (HND, "*(`0xB9` is `1000 1001 1` — bits 0, 3, 4, 5 and 7;",
     "*(`0xB9` is ~~`1000 1001 1`~~ `1011 1001` " + T + "`0xB9` = 128 + 32 + 16 + 8 + 1)* — bits 0, 3, 4, 5 and 7;"),

    # RO.CV-1: the transform publish 001FB120 indexes the object's 0x318 array, never the 0x740 pool.
    (POOL, "- **Consumer:** `CONTRACT-character-transform-publish` operates on records reached by walking the\n"
           "  active list from `+0x00`. It sees a record only after `00428710` has promoted it, which is the\n"
           "  ordering guarantee this contract exists to state.",
     "- **Consumer:** ~~`CONTRACT-character-transform-publish` operates on records reached by walking the~~\n"
     "  ~~active list from `+0x00`. It sees a record only after `00428710` has promoted it, which is the~~\n"
     "  ~~ordering guarantee this contract exists to state.~~ not `CONTRACT-character-transform-publish`, which reads "
     "no record of this pool " + T + "`001FB120`+0x2A `imul rdi, rax, 0x318` and `001FB120`+0x3C `add rdi, qword "
     "ptr [rcx + 0x58]` index the render object's own `0x318`-stride array; `001FB120` never reads `022C6F28`)*."),

    # RO.CV-3: 160 x 0x740 = 0x48800; 00426480+0x13 writes +0x48830.
    (CRO, "**exactly 160** — `160 × 0x740 = 0x48830`, the offset at which `FUN_00426480` writes a trailing dword",
     "**exactly 160** — ~~`160 × 0x740 = 0x48830`, the offset at which~~ `160 × 0x740 = 0x48800`, where the tail "
     "block starts; `FUN_00426480` writes a trailing dword at `+0x48830` " + T + "160 x 1,856 = 296,960 = `0x48800`; "
     "the store is `00426480`+0x13 `mov dword ptr [rcx + 0x48830], eax`)*"),

    # RO.CV-4 / RO.CV-5: the singleton's constructor is 00184F20 (00189000+0x61); 00189CE0 is a per-frame method
    #     (0017D6E0+0x89) and a third writer of +0x1C (00189CE0+0x40A). 003829D0 calls one wrapper, chosen on
    #     00259FA0's result (003829D0+0x14D/+0x14F).
    (PUB, "are the only two other writers image-wide, both reached through the getter `00189120`; and",
     "are ~~the only two other writers image-wide~~ two of the three writers besides the constructor (the third is the "
     "per-frame method `00189CE0`, at `00189CE0`+0x40A) " + T + "the constructor is `00184F20`, `00184F20`+0x39 `mov "
     "word ptr [rcx + 0x1c], si`; `00189CE0` is called from `0017D6E0`+0x89)*, both reached through the getter "
     "`00189120`; and"),
    (PUB, "   > `00189CE0`, which zeroes the byte at `0018A0EA`). Image-wide, the byte has exactly two other",
     "   > ~~`00189CE0`, which zeroes the byte at `0018A0EA`~~ `00184F20` (`00189000`+0x61); `00189CE0` is a per-frame "
     "method that also zeroes the byte, at `00189CE0`+0x40A " + T + "`00189000`+0x67 stores the constructed object in "
     "`01F7F598`; `00189CE0` is called from the frame body `0017D6E0`+0x89)*). ~~Image-wide,~~ Besides it, the byte "
     "has exactly two other"),
    (CRO, "`this + 0x690`. `003829D0` calls the two back to back (`00382B21`, `00382B28`).",
     "`this + 0x690`. ~~`003829D0` calls the two back to back (`00382B21`, `00382B28`).~~ `003829D0` calls one of the two, chosen on "
     "`00259FA0`'s result " + T + "`003829D0`+0x14D `test eax, eax` and `003829D0`+0x14F `je` to the `00182340` "
     "call, else `call 001821F0` and `jmp` past it)*."),

    # RO.CV-6: 001FAD50 copies three 64-byte matrices of ONE bank (+0x1D picks it) into +0x100/+0x108/+0x110.
    (PUB, "two 192-byte matrix banks (`+0x4C4` / `+0x584`) into the last two (`001FADCD`–`001FAE23`,",
     "~~two 192-byte matrix banks (`+0x4C4` / `+0x584`) into the last two~~ three 64-byte matrices of one bank "
     "(`+0x4C4` or `+0x584`, chosen by byte `+0x1D`) into `+0x100`, `+0x108` and a third slot `+0x110` " + T +
     "`001FAD50`+0x71, `001FAD50`+0xAF and `001FAD50`+0xED test the record's `+0x100`, `+0x108` and `+0x110`; the bank "
     "test is `001FAD50`+0x3B `cmp byte ptr [rax + 0x1d], 0`)* (`001FADCD`–`001FAE23`,"),

    # RO.CV-9: the constructor zeroes this+0x78..+0x38F (memset 001F4DA0+0x16D, copy 001F4DA0+0x172..+0x1DC), which
    #     covers +0x80 and +0x118; +0x420 is outside it.
    (CRO, "So the 632 bytes at `+0x118` are **allocated from an unzeroed heap, never cleared, never written\n"
          "individually, and never read**. They hold whatever the allocator last left there.",
     "So the 632 bytes at `+0x118` are **allocated from an unzeroed heap, ~~never cleared~~ then cleared with the "
     "rest of `+0x78`..`+0x38F` " + T + "`001F4DA0`+0x16D `memset(stack buffer, 0, 0x318)` and the copy to "
     "`this+0x78` at `001F4DA0`+0x172..+0x1DC, quoted above)*, never written\n"
     "individually, and never read**. ~~They hold whatever the allocator last left there.~~ They hold zero."),
    (CRO, "*The other two `CharacterRenderObject` spans, `+0x80` (144 B) and `+0x420` (96 B), are in the same",
     "*The other two `CharacterRenderObject` spans, ~~`+0x80` (144 B) and~~ `+0x420` (96 B) " + T + "`+0x80` lies "
     "inside the block the constructor zeroes at `001F4DA0`+0x172..+0x1DC; `+0x420` lies outside it)*, are in the same"),

    # RO.CV-11: both refusals leave through 004279B0+0x32; 00427A7D is 004279B0+0xCD on the success path.
    (POOL, "both are `xor eax, eax` — `004279E2` (duplicate refused) and `00427A7D` (pool full); a refused duplicate and "
           "a full pool look the same",
     "~~both are `xor eax, eax` — `004279E2` (duplicate refused) and `00427A7D` (pool full)~~ both leave through the "
     "one `xor eax, eax` at `004279B0`+0x32: a duplicate falls into it and the pool-full test `004279B0`+0x39 (`cmp "
     "..., 0xa0` then `jge`) jumps back to it " + T + "the other cited site is `004279B0`+0xCD, on the success path, "
     "the zero the free-cursor wrap uses)*; a refused duplicate and a full pool look the same"),

    # RO.CV-12: tail +0x1C has a third writer, the keyed setter 002EBC30 (002EBC30+0x7), reached from 0026C8C0+0x4F9.
    (POOL, "that list stands: written only by the constructor and by the reset helper `0042ED30`.",
     "that list stands~~: written only by the constructor and by the reset helper `0042ED30`.~~: written by the "
     "constructor and by the reset helper `0042ED30`, and `+0x1C` also by the keyed setter `002EBC30` " + T +
     "`002EBC30`+0x7 `movss dword ptr [rax + 0x4881c], xmm0`, reached from `0026C8C0`+0x4F9)*."),
    (POOL, "`+0x1C`, `+0x20`, `+0x24`, `+0x40` and `+0x4C..+0x70` are written only by the constructor and by `0042ED30`;",
     "`+0x1C`, `+0x20`, `+0x24`, `+0x40` and `+0x4C..+0x70` are written ~~only~~ by the constructor and by "
     "`0042ED30`, and `+0x1C` also by the keyed setter `002EBC30` " + T + "`002EBC30`+0x7, reached from "
     "`0026C8C0`+0x4F9)*;"),

    # RO.CV-13: the constructor stores flag word 0 (004269A0+0x60) and ors 5 into it at its end (004269A0+0x2B9).
    (POOL, "`tailPending = -1`, flag word `= 0`, `+0x2C`",
     "`tailPending = -1`, flag word `= 0` " + T + "not its final value - `004269A0`+0x2B9 `or dword ptr [rax + "
     "0x48818], 5` runs at the end of the constructor, so a constructed pool's flag word is 5)*, `+0x2C`"),

    # RO.CV-14: construct writes +0x2C = 0xFFFF (004269A0+0x66).
    (POOL, "above and no lifecycle operation here touches it.",
     "above ~~and no lifecycle operation here touches it~~; construct stores `0xFFFF` in it (section 7) and no other "
     "lifecycle operation here touches it " + T + "`004269A0`+0x66 `mov word ptr [rsi + 0x4882c], ax` with `eax` = "
     "-1)*."),
    (POOL, "| the +0x2C index is a third width again and no lifecycle operation touches it |",
     "| the +0x2C index is a third width again and ~~no lifecycle operation touches it~~ only construct touches it, "
     "storing `0xFFFF` " + T + "`004269A0`+0x66 `mov word ptr [rsi + 0x4882c], ax`)* |"),

    # RO.CV-15: the constructor fills +0x08..+0x77 as three vectors with allocator objects and two refs.
    (CRO, "+0x0C .. +0x74    early scalar block (slots 2, 13 read; not characterised)\n",
     "+0x0C .. +0x74    early scalar block (slots 2, 13 read; not characterised)   <- corrected 2026-10-02, OPUS - no "
     "such block: the constructor fills +0x08..+0x77 as the three vectors, their allocator objects and the two refs "
     "above (001F4DA0+0x41..+0x95), and slot 13's only read in this range is the +0x58 vector (001FB120+0x3C)\n"),

    # RO.CV-16 / RA.CV-1: 00426480 stores 0020E620(rdx), the caller's pointer; the 0xA0 in ecx is unused.
    (CRR, "30 B — `0020E620` image-pointer store of the `0xA0` handle into pool `+0x48830`",
     "30 B — `0020E620` image-pointer store of ~~the `0xA0` handle~~ the caller's pointer (`rdx`, `[022C6F20]`; the "
     "`0xA0` in `ecx` is unused) into pool `+0x48830` " + T + "`00426480`+0x4 `mov rcx, rdx` before `call "
     "0020E620`)*"),

    # RO.CV-17: 003AC110 walks the light list 02B3F508 (003AC110+0xB1, +0xE8); 01FD4A78 is a work-area base.
    (LIT, "`003AC110` (1876 B) is the record-less light gather - `01FD4A78` list,",
     "`003AC110` (1876 B) is the record-less light gather - ~~`01FD4A78` list~~ it walks the light list `02B3F508`; "
     "`01FD4A78` is a work-area base whose `+0x1000` and `+0x2000` it takes as two sub-areas " + T + "`003AC110`+0xB1 "
     "`mov r10, qword ptr [02B3F508]` and `003AC110`+0xE8 `test r10, r10`; `003AC110`+0x1F, +0x49 and +0x58 for "
     "`01FD4A78`)*,"),

    # RA.CV-2: 003B6890 clears 160 records of 0xE0, two per 0x1C0 step (003B6890+0x52 .. +0x67).
    (CRR, "flag clears over 80×`0x1C0` records",
     "flag clears over ~~80×`0x1C0` records~~ the 160 `0xE0`-byte records, two per `0x1C0` step of an 80-pass loop "
     + T + "`003B6890`+0x52 clears `+0x40` bit 0 at `-0xE0` and at `+0`, looping at `003B6890`+0x67; `0x8C00` / "
     "`0xE0` = 160)*"),

    # RA.CV-3 / RG.CV-12: +0x114 is the 003B56D0 slot handle (00428710+0x75 call, +0x7A store).
    (CRR, "**`+0x114` `animPhaseHandle`**",
     "**`+0x114` ~~`animPhaseHandle`~~** the slot handle `003B56D0` returns - the ramp-channel (shadow) slot of the "
     "pool at `02B40528` " + T + "stored at `00428710`+0x7A after the call at `00428710`+0x75; not an animation-phase "
     "handle)*"),

    # RA.CV-4: +6 is the parent link (00420FB0+0x1B walks it up, 00424080+0xAB tests -1); the own index is word +0
    #     (00425E70+0x19); +0xA is the next-sibling link of the depth-first walk 0042EF90 (+0x3A on +8, +0x4F on +0xA).
    (CRR, "Fourth tier (array-index fields): **`+0x6` `ownArrayIndex`** — sign-extended, multiplied by `0x740` (CRR "
          "stride), added to pool `022C6F28` at `00425E97` to compute the record's own base address;",
     "Fourth tier (array-index fields): ~~**`+0x6` `ownArrayIndex`** — sign-extended, multiplied by `0x740` (CRR stride), added to pool `022C6F28` at "
     "`00425E97` to compute the record's own base address;~~ **`+0x6`** — the parent (owner) record's index, `-1` at "
     "a root: `00420FB0`+0x1B walks it up the chain and `00424080`+0xAB tests it for `-1`; the record's own index is "
     "word `+0x0` " + T + "`00425E70`+0x19 `movzx eax, word ptr [rcx]`; the cited site lies inside the `je` at "
     "`00425E70`+0x24)*;"),
    (CRR, "**`+0xA` `altLinkedIndex`** — same pattern for an alternate/parent linked record (`00425EE4`);",
     "**`+0xA` `altLinkedIndex`** — ~~same pattern for an alternate/parent linked record (`00425EE4`)~~ the "
     "next-sibling link: the depth-first walk recurses on `+0x8`, the first child, and iterates `+0xA` " + T +
     "`0042EF90`+0x3A and `0042EF90`+0x4F; the parent is `+0x6`)*;"),

    # RA.CV-5: +0x670/+0x674/+0x678 are the focus point's three components (003E43D0); +0x66D bit 1 snaps +0x680.
    (CRR, "byte bitfield with bit 1 gating the three-channel auxiliary transform interpolation;",
     "byte bitfield with bit 1 ~~gating the three-channel auxiliary transform interpolation~~ asking the focus-point "
     "update to snap the smoothed vector `+0x680` once and clear the bit " + T + "`003E43D0`+0x25F `test al, 2` "
     "through `003E43D0`+0x270 `movdqa xmmword ptr [rbx + 0x680], xmm0`)*;"),
    (CRR, "bit 2 reset by `ResetDefaults`. **`+0x674`/`+0x678` are the previous X/Y scalars** for that interpolation.",
     "bit 2 reset by `ResetDefaults`. ~~**`+0x674`/`+0x678` are the previous X/Y scalars** for that interpolation.~~ **`+0x670`/`+0x674`/`+0x678` "
     "are the focus point's three components** " + T + "`003E43D0` blends all three in one pass, reading `+0x674` at "
     "`003E43D0`+0xD2 and storing `+0x678` at `003E43D0`+0x12D; the focus-point page)*."),

    # RA.CV-6: 0016D6A0 is `ret 0` (called at 0042A580+0x5E).
    (CRR, "  re-resolve helper `0016D6A0` on the record (`0042A5D1`); written by setters",
     "  ~~re-resolve helper~~ empty function `0016D6A0` (`ret 0`, so nothing is re-resolved) " + T + "`0016D6A0`+0x0 "
     "is `ret 0`; the call is `0042A580`+0x5E; as corrected 2026-09-19 above)* on the record (`0042A5D1`); written "
     "by setters"),

    # RA.CV-7: 00417A80 coerces the MULTIPLIER to 1 when the word is -1 (cmove at +0x38), so -1 stays -1.
    (HND, "with word `+2` times the frame-rate word (or 1 when the word is -1)",
     "with word `+2` times the frame-rate word ~~(or 1 when the word is -1)~~ (times 1 instead when the word is -1, "
     "so -1 stays -1) " + T + "`00417A80`+0x38 `cmove cx, r8w` replaces the multiplier, not the value, before "
     "`00417A80`+0x40 `imul ecx, eax`)*"),
    (FEF, "(with a `−1→1` coercion)",
     "(with ~~a `−1→1` coercion~~ the multiplier coerced to 1 when the word is −1, so −1 stays −1 " + T +
     "`00417A80`+0x38 `cmove cx, r8w`)*)"),

    # RA.CV-9: pass 1 tests bit 18 (00427DE0+0x1B4); bit 27 of +0x290 is tested only in pass 4 (00427DE0+0x7F7).
    (CRR, "`+0x290` bits {2,3,12,19,20,22,23,24,25,29,30} and `+0x294` bit 26.",
     "`+0x290` bits ~~{2,3,12,19,20,22,23,24,25,29,30}~~ {2,3,12,18,19,20,22,23,24,25,29,30} and `+0x294` bit 26 " +
     T + "bit 18 is tested at `00427DE0`+0x1B4 `bt eax, 0x12`; twelve bits plus one make the 13 blocks)*."),
    (CRR, "`+0x290` bits {26,27,28,31,9-again}",
     "`+0x290` bits ~~{26,27,28,31,9-again}~~ {26,28,31,9-again} " + T + "bit 27 is tested only in pass 4, at "
     "`00427DE0`+0x7F7; four bits plus 22 make the 26 blocks)*"),

    # RA.CV-12: ids 0x00..0x4B are 76 (0041DA90+0x95 cmp al, 0x4b / jbe).
    (RES, "so the table covers all 75 ids.",
     "so the table covers ~~all 75 ids~~ 76 ids, `0x00`–`0x4B`, one more than the 75-slot banks " + T +
     "`0041DA90`+0x95 `cmp al, 0x4b` then `jbe` keeps `0x4B` itself)*."),

    # RA.CV-13: the 160 limit is in more than four places.
    (CRR, "pool means patching all four and nothing in the data will tell you that.",
     "pool means patching ~~all four~~ more than four - the three in `004279B0` (`004279B0`+0x39, +0xD5, +0x108), "
     "the size `0x48930` at `003325D0`+0x17, and also the constructor's loop count (`004269A0`+0x16) and the refusal "
     "in `0042FB80` (`0042FB80`+0x88) " + T + "`mov edi, 0xa0` and `cmp dword ptr [rax + 0x4880c], 0xa0`)* - and "
     "nothing in the data will tell you that."),

    # RA.CV-14: +0x734 is per-model by name, 1.0 to 2.0 (00420480+0x1F4..+0x394).
    (CRR, "**`+0x734` `kindTunedFloat`** — a per-kind constant (`2.0`/`1.7`/`1.3`)",
     "**`+0x734` `kindTunedFloat`** — a ~~per-kind constant (`2.0`/`1.7`/`1.3`)~~ per-model constant chosen by "
     "directory letter and name, 1.0 to 2.0 (the full table is in section 7) " + T + "`00420480`+0x1F4 through "
     "`00420480`+0x394 store 2.0, 1.7, 1.3, 1.5, 1.2 and 1.6)*"),

    # RG.CV-1: 003E5D00 zeroes the +6 word too (xor at +0x18 before the store at +0x22).
    (FADE, "`[+0x4C2]` dword zeroed and the word echoed at `[+0x4C6]` - an 8-byte",
     "`[+0x4C2]` dword zeroed and ~~the word echoed at `[+0x4C6]`~~ the word at `[+0x4C6]` zeroed too " + T +
     "`003E5D00`+0x18 `xor eax, eax` comes before `003E5D00`+0x22 `mov word ptr [rcx + r8*8 + 0x4c6], ax`)* - an "
     "8-byte"),

    # RG.CV-2: the stepper adds delta into base (003E4370+0x2D add word ptr [rax], cx).
    (FADE, "`0x1000`, where `word[+0]` takes `word[+2]` and the `+4` counter",
     "`0x1000`, where ~~`word[+0]` takes `word[+2]`~~ `word[+2]` is added into `word[+0]` " + T + "`003E4370`+0x2D "
     "`add word ptr [rax], cx`)* and the `+4` counter"),

    # RG.CV-3: 00D117C0 is the double 2^-12; 00D117C8 the double 1/255 (003E4730+0x25, +0x35).
    (FADE, "multiplied by `00D117C0` (2^-13), `float[+0x22C]`, `float[+0x2EC]`",
     "multiplied by `00D117C0` (~~2^-13~~ the double 2^-12, 1/4096) " + T + "read from the image; `00D117C8` is the "
     "double 1/255, so this is the `/4096 ... /255` formula above; the multiplies are `003E4730`+0x25 and "
     "`003E4730`+0x35)*, `float[+0x22C]`, `float[+0x2EC]`"),

    # RG.CV-5: 00420FB0 requires bit 3 AND (flags & 0x30) == 0x30 on every record of the chain.
    (FADE, "while bit 3 persists on each linked record - 1 at chain end, else 0.",
     "while ~~bit 3 persists~~ bit 3 and `(flags & 0x30) == 0x30` both hold on each linked record " + T +
     "`00420FB0`+0x46 `jne` returns to the mask test at `00420FB0`+0x14)* - 1 at chain end, else 0."),

    # RG.CV-6: 0051BC10 uses 02CA8420 / 02CA8400 / 02CA8408 / 02CA8410; the 02A48xxx family has no reference.
    (TRAIL, "run: `cl * 0x3C0` into the `02A48F40` slot table, and when",
     "run: `cl * 0x3C0` into the ~~`02A48F40`~~ `02CA8420` slot table " + T + "`0051BC10`+0xA `add r8, qword ptr "
     "[02CA8420]`; `02A48F40`, `02A48F04`, `02A48EF4` and `02A48F08` have no reference in the image)*, and when"),
    (TRAIL, "`02A48F04` decrements, and the slot unlinks from the `+0x18`/`+0x20`",
     "~~`02A48F04`~~ `02CA8400` (u16) decrements " + T + "`0051BC10`+0x22 `add word ptr [02CA8400], ax`)*, and the "
     "slot unlinks from the `+0x18`/`+0x20`"),
    (TRAIL, "doubly-linked chain (head/tail at `02A48EF4`/`02A48F08` updated when",
     "doubly-linked chain (head/tail at ~~`02A48EF4`/`02A48F08`~~ `02CA8408`/`02CA8410` " + T + "`0051BC10`+0x3C and "
     "`0051BC10`+0x55)* updated when"),

    # RG.CV-7: the template's UNPACK is 0x6C450000 - NUM 0x45 (005409C0+0x2D).
    (TRAIL, "**out of a VU cell** — one of the twenty-seven the template's",
     "**out of a VU cell** — one of the ~~twenty-seven~~ 69 " + T + "NUM `0x45`, `005409C0`+0x2D)* the template's"),
    (TRAIL, "`UNPACK V4-32 num=27` at `+0x1C` uploads from `005409C0`'s own bytes.",
     "~~`UNPACK V4-32 num=27`~~ `UNPACK V4-32` with NUM `0x45` at `+0x1C` uploads from `005409C0`'s own bytes " + T +
     "`005409C0`+0x2D stores `0x6C450000` at `+0x1C`; the template table's NUM `0x45` is right)*."),
    (TRAIL, "template's `UNPACK V4-32 num=27 addr=0` fills from `005409C0`'s bytes at `+0x20`:",
     "template's ~~`UNPACK V4-32 num=27 addr=0`~~ `UNPACK V4-32 NUM 0x45 addr=0` " + T + "`005409C0`+0x2D stores "
     "`0x6C450000`)* fills from `005409C0`'s bytes at `+0x20`:"),

    # RG.CV-8: 00428AF0 writes bits 17 and 18 and the whole third-argument byte at 19..26 (mask 0xF801FFFF).
    (STAT, "sets a two-bit field of the render record (`00428AF0`, arguments 1, 1 and the mask byte `0x60`).",
     "sets ~~a two-bit field of the render record~~ two flag bits (17 and 18) and a byte field (bits 19 to 26) of the "
     "render record's `+0x304` (`00428AF0`, arguments 1, 1 and the mask byte `0x60`, which lands in bits 24 and 25) "
     + T + "`00428AF0`+0x0 clears `0xF801FFFF`, ten bits; `00428AF0`+0xE `movzx eax, r9b` takes the whole byte, "
     "unmasked; `00428AF0`+0x1E `shl eax, 0x11`)*."),
    (STAT, "exact and slightly wider: `+0x304` is masked `0xF801FFFF`, then",
     "~~exact and slightly wider~~ too narrow " + T + "the mask clears ten bits, 17 to 26)*: `+0x304` is masked "
     "`0xF801FFFF`, then"),
    (STAT, "is folded in - three\nflag bits at `+0x304`[17..19] - and `+0x294` gets `0x4000000`.",
     "is folded in - ~~three~~\n~~flag bits at `+0x304`[17..19]~~ two flag bits at `+0x304` 17 and 18 and the unmasked "
     "byte `r9b` at 19 to 26 " + T + "`00428AF0`+0xE `movzx eax, r9b` has no `and 1`)* - and `+0x294` gets "
     "`0x4000000`."),

    # RG.CV-10: 003E2810 is (rig, frames, x, y) - xmm1 is the frame count (003E2810+0x19, stored +0x74).
    (LOOK, "| `003E2810` `(controller, x, y, z)` | `003E29D0` - verb **`eyemove_381`** |",
     "| `003E2810` ~~`(controller, x, y, z)`~~ `(controller, frames, x, y)` " + T + "`003E2810`+0x19 keeps `xmm1` as "
     "the frame count, stored at `+0x2C` at `003E2810`+0x74; `xmm2`/`xmm3` are the targets; section 4a)* | "
     "`003E29D0` - verb **`eyemove_381`** |"),

    # RG.CV-11: 003E3340 multiplies [01DFE0B8] (003E3340+0x2D), not a literal 1.0.
    (LOOK, "`1.0f * [rdi+0x18]` is `maxss`-floored at the caller's xmm argument",
     "~~`1.0f * [rdi+0x18]`~~ `[01DFE0B8] * [rdi+0x18]` is `maxss`-floored at the caller's xmm argument " + T +
     "`003E3340`+0x2D loads `[01DFE0B8]`, not a literal - 1.0 in the image, 2.0 once `001EDDC0` runs with a non-zero "
     "argument)*"),

    # RG.CV-14: +0x640 is a float countdown (0042EE90+0x27..+0x36), the lip-flap timer.
    (CRR, "**`+0x640` `bindingResultDword`** — written by the binding update",
     "**`+0x640` ~~`bindingResultDword`~~** — a float countdown, the lip-flap timer of the rig page " + T +
     "`0042EE90`+0x27 reads it as a float and `0042EE90`+0x36 subtracts `[01DFE0BC]` each tick, clearing `+0x304` bit "
     "6 at zero)*; written by the binding update"),

    # CL.CV-1: slot 2 is a class mask the walks AND; nothing sorts (0018B100+0x67).
    (L, "> Every one carries a **draw-order number**, and that number — not the order the frame enqueued\n"
        "> them — decides what ends up in front of what.",
     "> Every one carries a ~~**draw-order number**, and that number — not the order the frame enqueued~~\n"
     "> ~~them — decides what ends up in front of what.~~ **class mask**, and the list runs in the order the frame "
     "enqueued " + T + "the walk runs the list in stored order and only ANDs slot 2's value, " + MASK + ")*."),
    (L, "each stamped with a number saying how late it belongs, and runs the list in number order. That",
     "each stamped with ~~a number saying how late it belongs, and runs the list in number order~~ a class mask, and "
     "runs the list in the order the jobs were added " + T + MASK + "; nothing sorts)*. That"),
    (L, "That is the **draw-order key**. It is what makes the base class `OrderedObject` an ordered\n"
        "object, and it is why enqueue order does not determine draw order.",
     "That is the ~~**draw-order key**~~ **class mask** " + T + MASK + ", and `0018B1B0` ANDs it too; no comparator "
     "runs)*. It is what makes the base class `OrderedObject` an ordered\n"
     "object, ~~and it is why enqueue order does not determine draw order~~ and enqueue order is the draw order."),
    (L, "| `0x80` | `VideoObj` | composited last, over everything |",
     "| `0x80` | `VideoObj` | ~~composited last, over everything~~ its mask value; where it draws follows its "
     "enqueue position " + T + MASK + ")* |"),
    (L, "                 later: the list is ordered by slot 2 and each slot 1 is executed\n",
     "                 later: the list is ordered by slot 2 and each slot 1 is executed   <- corrected 2026-10-02, OPUS "
     "- nothing orders it: the walk 0018B100 runs it in stored order and ANDs slot 2 with the list's mask "
     "(0018B100+0x67)\n"),
    (L, "- **Best intervention point for changing layering:** slot 2 of a class's vtable. Returning a\n"
        "  larger constant moves that pass later. This is a 6-byte function per class and it is the only\n"
        "  thing that determines order — the enqueue sequence does not.",
     "- **Best intervention point for changing layering:** ~~slot 2 of a class's vtable. Returning a~~ the enqueue "
     "order " + T + MASK + "; no comparator runs)*.\n"
     "  ~~larger constant moves that pass later. This is a 6-byte function per class and it is the only~~\n"
     "  ~~thing that determines order — the enqueue sequence does not.~~ Slot 2 is ANDed with each walk's mask, so "
     "changing it changes which walks run the pass, not its place."),
    (R, "returns a **draw-order key** — `1` for scene begin, `0x10` for the ordinary passes, `0x80` for video.",
     "returns a ~~**draw-order key**~~ **class mask** — `1` for scene begin, `0x10` for ~~the ordinary passes~~ most "
     "ordinary passes and `0x100` for the opaque and after-water passes, `0x80` for video " + T + "the walks AND it "
     "and never sort, " + MASK + "; `001F2890` is `mov eax, 0x100`)*."),

    # CL.CV-7: RenderOpaqueObj / RenderAfterWaterObj / RenderMapOpaqueObj / RenderMonsterGalleryChara share slot 2
    #     001F2890 = mov eax, 0x100.
    (L, "first; `0x10` for the ordinary render passes; `0x80` for `VideoObj` — the job that must cover",
     "first; `0x10` for ~~the ordinary render passes~~ most ordinary render passes and `0x100` for `RenderOpaqueObj`, "
     "`RenderAfterWaterObj`, `RenderMapOpaqueObj` and `RenderMonsterGalleryChara` " + T + "their shared slot 2 "
     "`001F2890` is `mov eax, 0x100`)*; `0x80` for `VideoObj` — the job that must cover"),
    (L, "`AmbientOcclusionObj`, `MaskBorderObj` and the other ordinary passes | the main body of the frame |",
     "`AmbientOcclusionObj`, `MaskBorderObj` and ~~the other ordinary passes~~ most other ordinary passes; "
     "`RenderOpaqueObj`, `RenderAfterWaterObj`, `RenderMapOpaqueObj` and `RenderMonsterGalleryChara` carry `0x100` " +
     T + "`001F2890`, their shared slot 2, is `mov eax, 0x100`)* | the main body of the frame |"),

    # CL.CV-2: +0x10 is the flush selector (0018C8F0+0x43 executes the entry when it is 0); the walks never read it.
    (L, "*(u8*)(obj + 2) = 1;                     // +0x10  enabled, on by default\n",
     "*(u8*)(obj + 2) = 1;                     // +0x10  enabled, on by default   // <- corrected 2026-10-02, OPUS - "
     "not an enable: the flush 0018C8F0 executes an entry only when this byte is 0 (0018C8F0+0x43), and neither walk "
     "reads it\n"),
    (L, "+0x10  u8   enabled    set to 1 by the base constructor\n",
     "+0x10  u8   enabled    set to 1 by the base constructor   <- corrected 2026-10-02, OPUS - flushSelector, not an "
     "enable: read only by the flush at 0018C8F0+0x43, which executes the entry when it is 0\n"),
    (L, "stores `OrderedObject::vftable`, order 0, enabled 1 |",
     "stores `OrderedObject::vftable`, order 0, ~~enabled 1~~ flush selector 1 " + T + "`0018C8F0`+0x43 is the byte's "
     "only reader and executes the entry when it is 0)* |"),

    # CL.CV-3: four appenders push to the ordered list only (001E5270+0x1A, 001F89B0+0x1F tail-jump to 0018AFF0).
    (C, "**I-1 — OWNERSHIP IS SPLIT, AND ONLY ONE LIST OWNS.** Every enqueue appends the same pointer to",
     "**I-1 — OWNERSHIP IS SPLIT, AND ONLY ONE LIST OWNS.** ~~Every enqueue appends~~ The 36 owner-side enqueues "
     "append " + T + "not every appender - `001E5270`+0x1A and `001F89B0`+0x1F tail-jump to `0018AFF0` with no owner "
     "push; the list page counts 40 = 36 + 4)* the same pointer to"),

    # CL.CV-4 / CL.CV-5: the owning vector has no reserve (0018C9E0+0x30) and grows from its first push
    #     (0018C610+0x50 test, +0x70 grow call); only the ordered list reserves 5,000 (0018AD00+0x48).
    (C, "one element array per list, 5,000 entries reserved;",
     "~~one element array per list, 5,000 entries reserved~~ 5,000 entries reserved for the ordered list only "
     "(`0018AD00`+0x48), none for the owning vector, which `0018C9E0` creates empty (`0018C9E0`+0x30) " + T +
     "I-3's dated note)*;"),
    (C, "push_backs branch to it (`0018C664`, `0018B004`), but a frame would need five thousand commands to",
     "push_backs branch to it (`0018C664`, `0018B004`), but ~~a frame would need five thousand commands to~~ only the "
     "ordered list's needs five thousand commands to " + T + "the first cited branch is `0018C610`+0x54, the OWNING "
     "vector's push, whose capacity starts at 0, so its grow call `0018C610`+0x70 runs from the first enqueue)*"),
    (C, "any enqueue; the push_back's capacity test at `0018C660` never takes the grow arm in practice (I-3) |",
     "any enqueue; the ~~push_back's capacity test at `0018C660` never takes the grow arm in practice (I-3)~~ ordered "
     "list's push never grows in practice, but the owning vector's capacity test `0018C610`+0x50 takes the grow arm "
     "from the first enqueue " + T + "I-3's dated note, capacities 1, 2, 4, 8)* |"),
    (C, "6. **Capacity exhausted** → `001AB570` reallocates and moves. Unreached in practice (I-3) and\n"
        "   therefore **untested by the shipped game**, which is a risk a reimplementation inherits.",
     "6. **Capacity exhausted** → `001AB570` reallocates and moves. ~~Unreached in practice (I-3) and~~ Reached on "
     "the owning vector from the first enqueue (`0018C610`+0x70), so exercised every frame " + T + "I-3's dated "
     "note)*.\n"
     "   ~~therefore **untested by the shipped game**, which is a risk a reimplementation inherits.~~"),
    (C, "    else: grow_and_insert(list, p, &v)            # 001AB570 - never reached, see I-3\n",
     "    else: grow_and_insert(list, p, &v)            # 001AB570 - never reached, see I-3   # <- corrected "
     "2026-10-02, OPUS - reached on the owning vector from its first push (0018C610+0x70); only the reserved ordered "
     "list never grows\n"),
    (C, "6. **The grow path is untested by the shipped game** (§10.6) and therefore unverifiable from\n   behaviour.",
     "6. ~~**The grow path is untested by the shipped game** (§10.6) and therefore unverifiable from~~ The grow path "
     "runs on the owning vector every frame (`0018C610`+0x70) " + T + "I-3's dated note)*.\n   ~~behaviour.~~"),

    # CL.CV-9: BegineSceneObj::Execute 001F29E0 and ApplyJson's slot 1 001F29C0 never read 01DFE0C4.
    (L, "| `01DFE0C4` | **master render enable** | `.data` | a byte; every execute body checks it |",
     "| `01DFE0C4` | **master render enable** | `.data` | a byte; ~~every execute body checks it~~ most execute bodies "
     "check it; `BegineSceneObj`'s `001F29E0` and `ApplyJsonForCutSceneObj`'s `001F29C0` do not " + T + "both bodies "
     "read whole, 50 and 8 bytes, no `01DFE0C4` reference)* |"),
    (L, "`01DFE0C4`. Every execute body\n  read in this pass checks it.",
     "`01DFE0C4`. ~~Every execute body~~\n  ~~read in this pass checks it.~~ Most execute bodies check it; `001F29E0` "
     "(`BegineSceneObj`) and `001F29C0` (`ApplyJsonForCutSceneObj`) do not " + T + "both read whole)*."),

    # CL.CV-10: 009010B8 has 3 slots - the complete object locator at 009010D0 starts MapOrderedObject's vtable.
    (C, "  +0x00  void*   vftable            3 slots in subclasses; base vtable 009010B8 has 7;\n",
     "  +0x00  void*   vftable            3 slots in subclasses; base vtable 009010B8 has 7;   <- corrected 2026-10-02, "
     "OPUS - 009010B8 has 3 slots; the qword at 009010D0 is MapOrderedObject's complete object locator, and its "
     "vtable 009010D8 follows\n"),
    (C, "base vtable `009010B8` slot map (7 slots, slot 5 = `00212C60`)",
     "base vtable `009010B8` slot map (~~7 slots, slot 5 = `00212C60`~~ 3 slots; `00212C60` is slot 1 of "
     "`MapOrderedObject` `009010D8` " + T + "the complete object locator at `009010D0` ends the base vtable)*)"),

    # GP.CV-1: GiTrans / GiTransNz / GiNormal make six device calls including the +0x78 / +0x98 / +0x80 triple.
    (GI, "`GiZNormalOnOff` entirely**, which reach the device only through `+0x78`/`+0x88`/`+0xA0`/`+0xA8`.",
     "`GiZNormalOnOff` entirely**, which reach the device ~~only~~ through `+0x78`/`+0x88`/`+0xA0`/`+0xA8` and, for "
     "`GiTrans`, `GiTransNz` and `GiNormal`, also `+0x98` and `+0x80` " + T + "`00862D40`+0xCA and +0xF4, "
     "`00862EC0`+0xC8 and +0xF2; the eight-of-eight triple holds)*."),
    (GI, "`[rax+0x88]` vcalls. Interior anchor `008651C0`",
     "`[rax+0x88]` vcalls, and `[rax+0xA0]`/`[rax+0xA8]` " + T + "`008651A0`+0xE8 and +0xF6, six device calls)*. "
     "Interior anchor `008651C0`"),
    (GI, "`[r10+0x78]` vcalls. Interior anchor `00862D60`",
     "`[r10+0x78]` vcalls, and `[rax+0x98]`/`[rax+0x80]` " + T + "`00862D40`+0xCA and +0xF4, six device calls)*. "
     "Interior anchor `00862D60`"),
    (GI, "`[r10+0x78]` vcalls. Interior anchor `00862EE0`",
     "`[r10+0x78]` vcalls, and `[rax+0x98]`/`[rax+0x80]` " + T + "`00862EC0`+0xC8 and +0xF2, six device calls)*. "
     "Interior anchor `00862EE0`"),

    # GP.CV-2: device slot 0 006CA760 overwrites the count (006CA760+0x6) - the 2026-09-26 correction.
    (GI, "| class | slot 1 | reservation count |",
     "| class | slot 1 | ~~reservation count~~ count passed to slot 0, which ignores it " + T + "`006CA760`+0x6 "
     "overwrites `rdx` before any read; the 2026-09-26 correction above)* |"),
    (GI, "its body passes literal `4` to the reservation call.",
     "its body passes literal `4` to ~~the reservation call~~ slot 0, which ignores it " + T + "`006CA760`+0x6 "
     "`imul rdx, rax, 0x7fe0` overwrites the count)*."),
    (GI, "   GiPolyGT4T slot 1   [dev+0x000] reserve 4 vertices -> write pointer\n",
     "   GiPolyGT4T slot 1   [dev+0x000] reserve 4 vertices -> write pointer   <- corrected 2026-10-02, OPUS - slot 0 "
     "(006CA760) ignores the 4 and returns a fixed 0x7FE0-byte staging area (006CA760+0x6)\n"),

    # GP.CV-3: 01F83078 is the +8 of 01F83070, which 001FB840 reads (001FB840+0x6).
    (GI, "most recently created command of its class, and nothing reads it back.**",
     "most recently created command of its class, ~~and nothing reads it back.~~ and only `01F83078` is read "
     "back.** " + T + "`01F83078`, `GiBeginScene`'s global, is the `+8` of the node `01F83070` that `001FBD80`+0x4F "
     "passes to `001FB840`, which reads it at `001FB840`+0x6 `mov rdx, qword ptr [rcx + 8]`)*"),

    # GP.CV-4: the device is 02CC0410 + 0x18C0 (005FD050+0x47/+0x74, 00615840+0x310), not the walker's argument's.
    (GI, "therefore not the table the commands call** — it is the container, and `+0x18C0` of it is the device "
         "(§12d, §13b).",
     "therefore not the table the commands call** — ~~it is the container, and `+0x18C0` of it is the device (§12d, §13b).~~ and it is not the device's container "
     "either: the device is `02CC0410` + `0x18C0`, a separate magic-static singleton " + T + "`005FD050`+0x47 and "
     "`005FD050`+0x74 return `02CC0410`; `00615840`+0x310 builds the `+0x18C0` subobject; section 20f)*."),

    # GP.CV-5: 001F48B0+0x90 only appends; slot 1 runs later from the pass-list walk (0018B100+0x87).
    (GI, "   -> its slot 1 (FUN_001F49F0) -> FUN_005FEA50 with callback FUN_001F4A10\n",
     "   -> its slot 1 (FUN_001F49F0) -> FUN_005FEA50 with callback FUN_001F4A10   <- corrected 2026-10-02, OPUS - not "
     "part of this chain: 001F48B0+0x90 only appends the wrapper to the ordered list; slot 1 runs later from the "
     "pass-list walk 0018B100+0x87 (section 12e)\n"),

    # GP.CV-6: R(i) = r14 + 0x30 + 0x28i; +0x20 is the completion object, the signal target is R(i)+0x10.
    (GI, "00600DD9  [02CE4720 + i*0x28 + 0x50] = rbx        ; +0x20  event\n",
     "00600DD9  [02CE4720 + i*0x28 + 0x50] = rbx        ; +0x20  event   ; <- corrected 2026-10-02, OPUS - +0x20 is the "
     "completion object [target+0x78]; the per-slot event is +0x10 (section 20a)\n"),
    (GI, "00600DF9  005CD5E0(&entry + 0x40)                 ; signal\n",
     "00600DF9  005CD5E0(&entry + 0x40)                 ; signal   ; <- corrected 2026-10-02, OPUS - the signal "
     "target is the slot's event at entry +0x10, r14 + 0x40 + 0x28i (00600D20+0xD1..+0xD9)\n"),

    # GP.CV-7: commands come from the ring 001A1470 on [01F7F4C0]; the per-frame rewind 003A3A00+0xE is of 02F8F2D0.
    (GI, "(§2); the commands come from a bump allocator (§10); and **the arena is rewound by a single pointer",
     "(§2); the commands come from ~~a bump allocator~~ the ring allocator `001A1470` (§10) " + T + "`001A1470`+0x35 "
     "restarts at the base when full; the rewind `003A3A00`+0xE stores `02F8F2D0`, the display list's data arena, "
     "not the command arena `01F7F4C0`)*; and **the ~~arena~~ display list's data arena is rewound by a single "
     "pointer"),

    # GP.CV-8: 001DB220 is the GiVmax constructor (vtable 009007E8 at 001DB220+0xF, arena at +0x47).
    (GI, "`001DB220` (273 B) is a sound-request body - `0016D6A0`/`001A1470`/`00861EC0`.",
     "`001DB220` (273 B) is ~~a sound-request body~~ the `GiVmax` constructor: it installs vtable `009007E8` (RTTI "
     "`GiVmax`) and takes its arrays from the command arena " + T + "`001DB220`+0xF `lea rax, [009007E8]`, "
     "`001DB220`+0x47 `call 001A1470`)* - `0016D6A0`/`001A1470`/`00861EC0`."),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('`00189CE0` is called from `0017D6E0`+0x89',
     '`00189CE0` is called from the per-frame pump at its `+0x89`'),
    ('is called from the frame body `0017D6E0`+0x89',
     'is called from the per-frame pump at its `+0x89`'),
]
_rn = lambda s: __import__('functools').reduce(lambda a, p: a.replace(p[0], p[1]), ROLE_NAMES, s)
EDITS = [(e[0], _rn(e[1])) if len(e) == 2 else (e[0], e[1], _rn(e[2])) + tuple(e[3:]) for e in EDITS]


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
