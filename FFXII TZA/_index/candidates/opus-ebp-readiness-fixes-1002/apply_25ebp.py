"""apply_25ebp.py [--apply] - 25-EBP-Script-Container readiness map (cloud-reports/re-readiness/25-ebp.md), section 2.3
contradictions A1-A16 and B1-B18 settled at the shipping image and the shipped scripts, plus the C stale / banner items
(OPUS, 2026-10-02).

Each edit strikes the side the bytes REFUTE and restates it, tagged *(corrected 2026-10-02, OPUS: ...)*, or marks a
stale "open / not read" claim *(answered: see ...; 2026-10-02, OPUS)*. Verdicts and deciding instructions:
scratchpad eb25/verdicts-25.md.
Map favourites the bytes overturn: A5 (BW-4 "never compared to the roll" - 0025ACA0 rolls the current weather's byte
against RNG % 100) and A15/B5 stand; A4 is both partly (+0x64 byte-counted, +0x6C / +0x70 u32-counted).
Items with no edit: A6/A7 sides already right elsewhere get their wrong side struck here; B5 is a generated TSV
(SWE2-DATA regenerate request, not a hand edit); B17's 332 stands as a file count (only the "332 map groups" reading is
struck); B18 is undecided for the `.ard` sibling path; C13 (last_reviewed dates), C19 (BY-4 naming), C23 (duplicate
heading) and C28 (evidence_tier) are left - no front-matter or heading edits, no label upgrades.
Every ~~ span opens and closes on one line; multi-line text is struck line by line. Code-block lines get a trailing
`<- corrected` comment instead of a strike (their OLD includes the line end, so NEW never contains OLD).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "25-EBP-Script-Container/"
R = F + "README.md"
CON = F + "Container/ebp2-container.md"
S000 = F + "Bytecode-And-Opcodes/section-000-bytecode.md"
S002 = F + "Sections/section-002-text.md"
S003 = F + "Sections/section-003-text.md"
S004 = F + "Sections/section-004.md"
S006 = F + "Sections/section-006.md"
S008 = F + "Sections/section-008.md"
S009 = F + "Sections/section-009.md"
S010 = F + "Sections/section-010.md"
S011 = F + "Sections/section-011.md"
S012 = F + "Sections/section-012.md"
S014 = F + "Sections/section-014.md"
S016 = F + "Sections/section-016.md"
S019 = F + "Sections/section-019.md"

GATE = ("`0x003DA27B` and `0x003DD1AB` pass kind 1 to `FUN_0032F3D0`, whose kind-1 arm ends in `0x005C5230` = "
        "`xor eax, eax; ret`, so the stores at `0x003DA28F` / `0x003DD1BF` never run")
C = "*(corrected 2026-10-02, OPUS: "
VBF = "read through `vbf_read_entry` from `FFXII_TZA.vbf`"

EDITS = [
    # C-V1 (A1): CML1 binds by the authored index - both resolvers pass kind 1 to 0032F3D0, whose kind-1 arm ends in
    #     005C5230 (xor eax, eax; ret); the write-backs 003DA28F / 003DD1BF never execute.
    (S008, "each paired with a slot the engine\n> fills in at load time with the matching camera's index in\n"
           "> [`section_009`](section-009.md). **The index that ships in the file is never used** — the\n"
           "> engine recomputes it by name.",
     "each paired with ~~a slot the engine~~\n> ~~fills in at load time with~~ the matching camera's index in\n"
     "> [`section_009`](section-009.md). ~~**The index that ships in the file is never used** — the~~\n"
     "> ~~engine recomputes it by name.~~ **The index that ships in the file is the binding**; the name lookup never "
     "runs in the shipped build " + C + GATE + "; the correction in §3)*."),
    (S008, "> **Three of the four dwords in every entry are overwritten at load.**",
     "> **~~Three~~ Two of the four dwords in every entry are overwritten at load.** " + C + "`+0x08` is zeroed at "
     "`0x003DA292` and `+0x0C`'s low byte at `0x003DA296`; the `+0x04` store never runs — " + GATE + ")*"),
    (S008, "— but the engine never looks: it calls\n> `CAM7_FindCameraByName` and **stores the result over the top**, "
           "at `0x003DA28F`.",
     "~~— but the engine never looks: it calls~~\n> ~~`CAM7_FindCameraByName` and **stores the result over the top**, "
     "at `0x003DA28F`.~~ — and the engine uses it as authored: the call and its store sit behind a gate that returns 0 "
     + C + GATE + "; the reversal below)*."),
    (S008, "> For a modder this is the useful half of the sheet. **Renaming a camera in `section_009` breaks\n"
           "> the link; renumbering the index column in `section_008` does nothing at all.** The file is a\n"
           "> runtime structure that ships pre-filled, not a table of authored parameters.",
     "> For a modder this is the useful half of the sheet. **~~Renaming a camera in `section_009` breaks~~\n"
     "> ~~the link; renumbering the index column in `section_008` does nothing at all.~~** **Renumbering the index "
     "column in `section_008` changes which camera plays; renaming a camera in `section_009` changes nothing** "
     + C + GATE + "; the reversal below)*. ~~The file is a~~\n"
     "> ~~runtime structure that ships pre-filled, not a table of authored parameters.~~"),
    (S008, "| `0x003DA1F0` | `CML1_ResolveNames` — the only reader of this section (count",
     "| `0x003DA1F0` | `CML1_ResolveNames` — ~~the only reader of this section~~ the load-time pass over this section, "
     "whose index write-back never runs; entry `+0x04` is read at run time by the §3 readers and by `0x003DA300` at "
     "`0x003DA31F` " + C + GATE + ")* (count"),
    (S010, "the table.** It does. At load the engine walks every entry, looks each **name** up in\n"
           "`section_011`, and **writes the answer over the authored number**.",
     "the table.** It does. At load the engine walks every entry~~, looks each **name** up in~~\n"
     "~~`section_011`, and **writes the answer over the authored number**~~ and zeroes its two scratch words; the name "
     "lookup and its store over the authored number never run in the shipped build " + C + GATE + "; §3 correction)*."),
    (S010, "**renumbering `index` does nothing, because the engine recomputes it — but renaming a shake in\n"
           "`section_011` breaks the link.** The names are load-bearing; the numbers are not.",
     "**~~renumbering `index` does nothing, because the engine recomputes it — but renaming a shake in~~\n"
     "~~`section_011` breaks the link.~~** ~~The names are load-bearing; the numbers are not.~~ **Renumbering `index` "
     "changes which shake plays; renaming a shake in `section_011` changes nothing** " + C + GATE
     + "; §3 correction)*."),
    (S010, "the count, walks every entry and overwrites each `index`. **I disassembled",
     "the count, walks every entry ~~and overwrites each `index`~~ and would overwrite each `index` behind a gate that "
     "returns 0 in the shipped build " + C + GATE + ")*. **I disassembled"),
    (S010, "> value **is** — but the engine does not read it. **It recomputes it by name and stores the result\n"
           "> over the top**, exactly as its camera twin does.",
     "> value **is** — ~~but the engine does not read it.~~ **~~It recomputes it by name and stores the result~~\n"
     "> ~~over the top~~**~~, exactly as its camera twin does.~~ and the engine uses it as authored: the recompute below "
     "sits behind a gate that returns 0 " + C + GATE + "; the correction after this box)*."),
    (S010, "> **For a modder this is the operative fact: renumbering `index` in `section_010` does nothing,\n"
           "> because the engine overwrites it; renaming a shake in `section_011` breaks the link.** The",
     "> **For a modder this is the operative fact: ~~renumbering `index` in `section_010` does nothing,~~\n"
     "> ~~because the engine overwrites it; renaming a shake in `section_011` breaks the link.~~** renumbering `index` "
     "changes which shake plays and renaming a shake changes nothing " + C + GATE
     + "; the correction after this box)*. The"),
    (S010, "leftover the engine ignores, it is an input the engine consumes and then overwrites.**",
     "leftover the engine ignores, it is an input the engine ~~consumes and then overwrites~~ consumes as authored — "
     "the overwrite never runs in the shipped build.** " + C + GATE + ")*"),
    (S011, "found `SHKCTL_ResolveNames` (`0x003DD120`), which resolves\n> `section_010`'s entries by **name** through",
     "found `SHKCTL_ResolveNames` (`0x003DD120`), which ~~resolves~~ would resolve\n> `section_010`'s entries by "
     "**name** " + C + "its store never runs in the shipped build — " + GATE + "; the 2026-09-12 note above)* "
     "through"),

    # C-V2 (A2): the text-bank count is the whole sign-extended first dword >> 2 (00264D74 / 00264DA4 movsxd,
    #     00264D7D / 00264DAD shr rax, 2); the low u16 is only the offset (00264D85 / 00264DB5).
    (S002, "| section `+0x00` low u16 (first offset) | `0x00264D74` | — | — | no — **doubles as the entry count** "
           "(`>> 2`) |",
     "| section `+0x00` low u16 (first offset) | `0x00264D74` | — | — | no — ~~**doubles as the entry count** "
     "(`>> 2`)~~ the entry count is the whole sign-extended first dword `>> 2`, not this u16 " + C + "`0x00264D74` "
     "`movsxd rax, dword ptr [r8]`, `0x00264D7D` `shr rax, 2`; the u16 is read only as the offset at `0x00264D85`; "
     "the two differ in 213 of the 828 `us` sections, the 2026-09-05 audit above)* |"),
    (S003, "| section `+0x00` low u16 | `0x00264DA4` | — | — | no — **doubles as the entry count** (`>> 2`) |",
     "| section `+0x00` low u16 | `0x00264DA4` | — | — | no — ~~**doubles as the entry count** (`>> 2`)~~ the entry "
     "count is the whole sign-extended first dword `>> 2`, not this u16 " + C + "`0x00264DA4` `movsxd rax, dword ptr "
     "[r8]`, `0x00264DAD` `shr rax, 2`; the u16 is read only as the offset at `0x00264DB5`; the two agree in all 359 "
     "`us` sections)* |"),

    # C-V3 (A3): 00358A0F reads [r8 + id*8 + 8]; entries start at +4 after the u32 count, so that is the entry's
    #     second dword; shipped tables hold {name offset ('init', 'main'), offset within script}.
    (S000, "00358A0F  mov    eax, dword ptr [r8 + rax*8 + 8]  ; 8-byte stride, dword at entry+0\n",
     "00358A0F  mov    eax, dword ptr [r8 + rax*8 + 8]  ; 8-byte stride, dword at entry+0   <- corrected 2026-10-02, "
     "OPUS - entries start at +4 after the u32 count, so +8 + 8*id is the entry's SECOND dword (offsetWithinScript); "
     "the shipped tables put the name-pool offset first ('init', 'main'), BW-5 below\n"),

    # C-V4 (A4): +0x6C is {u32 count; u32 ref[]} (002641FF cmp esi, [rcx]; 00264203 mov ebx, [rcx + rsi*4 + 4]);
    #     +0x70 is a u32 count 5 then five u32 offsets; only +0x64 is a count byte then bytes (002658B0).
    (S000, "`+0x60` through `+0x74` each point at an array whose **first byte is the element count**, followed\n"
           "by that many bytes.",
     "~~`+0x60` through `+0x74` each point at an array whose **first byte is the element count**, followed~~\n"
     "~~by that many bytes.~~ `+0x60` through `+0x74` each point at a counted array, but not of one shape: `+0x64` is a "
     "count byte then that many bytes, while `+0x6C` and `+0x70` are a `u32` count then `u32` elements " + C
     + "`002641FF` `cmp esi, dword ptr [rcx]` and `00264203` `mov ebx, dword ptr [rcx + rsi*4 + 4]` read `+0x6C`'s "
     "target as `{u32 count; u32 ref[]}`, and `+0x70`'s target is `05 00 00 00` then five ascending `u32` offsets in "
     "the shipped images; `+0x60`, `+0x68` and `+0x74` carry three zero bytes after the count in every file, so the "
     "data does not settle their width)*."),
    (S000, "| `+0x6C` | **`1` in 1114/1114** | a 1-element authored option |",
     "| `+0x6C` | **`1` in 1114/1114** | ~~a 1-element authored option~~ `{u32 count = 1; u32 packedRef}`, the trap "
     "reference " + C + "`002641FF` / `00264203`; the header map above, corrected 2026-09-12)* |"),

    # C-V5 (A5, both partly): the alternatives' bytes are availability flags (0025ABA0 tests > 0), but the CURRENT
    #     weather's byte is a survival chance against RNG % 100 (0025ACCC -> 0025ACEF); 002658B0 has two callers.
    (S000, "> availability flags to their one consumer, not chances against a roll.** `002658B0(idx)` reads",
     "> availability flags to ~~their one consumer, not chances against a roll~~ the transition chooser, and the "
     "current weather's own byte is a chance against a roll.** " + C + "the survival roll is `0025ACA0`, below)* "
     "`002658B0(idx)` reads"),
    (S000, "Its only caller is the transition chooser `0025ABA0` (`0025ABD4`,\n"
           "> `0025ABE4`, `0025AC05`, `0025AC11`, `0025AC30`): from",
     "~~Its only caller is~~ Its callers are `0025ACA0` (`0025ACCC`) and the transition chooser `0025ABA0` "
     "(`0025ABD4`,\n> `0025ABE4`, `0025AC05`, `0025AC11`, `0025AC30`, and `0025AC40`, `0025AC61`, `0025AC81` " + C
     + "`retool.py callers 002658B0`, nine sites)*): from"),
    (S000, "and the byte's *value* is never\n> compared to the roll. `0025ABA0` is called from `0025ACA0`,",
     "~~and the byte's *value* is never~~\n> ~~compared to the roll.~~ and the current weather's byte *is* compared to a "
     "roll before the chooser runs " + C + "`0025ACA0` reads it at `0025ACCC`; `0` re-chooses (`0025ACD6`), `>= 100` "
     "keeps (`0025ACD8` `cmp edi, 0x64` / `jge`), otherwise `0025ACDD`–`0025ACEF` draw `00379CD0`, scale it to "
     "`0..99` (`imul rcx, rax, 0x64` / `shr rcx, 0x20`) and keep the weather when the draw is below the byte (`jb`); "
     "only a failed roll calls `0025ABA0` at `0025ACF3`)*. `0025ABA0` is called from `0025ACA0`,"),
    (S000, "the glossary's\n> \"chance\" is a misnomer for this consumer, and whether another reader weighs the values is not\n"
           "> established (the `+0x64` load census",
     "~~the glossary's~~\n> ~~\"chance\" is a misnomer for this consumer, and whether another reader weighs the values is "
     "not~~\n> ~~established~~ the glossary's \"chance\" is right for the current weather's byte, which `0025ACA0` weighs "
     + C + "`0025ACD8`–`0025ACEF`, as above)* (the `+0x64` load census"),

    # C-V6 (A6): the slot-6 handler stores at 022C6CF0[mgr] (00330097) and clears 0x40 in 022C6E48[mgr]
    #     (003300A4-003300B3), r15 = 00120000 (0033007D).
    (S000, "(stored at `0233A6F0 + lane*8`) and lane `ecx & 0xF`; `0026C860` resolves the base, the "
           "`0233AE48 + lane*8` word",
     "(stored at ~~`0233A6F0 + lane*8`~~ `022C6CF0 + lane*8`) and lane `ecx & 0xF`; `0026C860` resolves the base, the "
     "~~`0233AE48 + lane*8`~~ `022C6E48 + lane*8` word " + C + "`00330097` `mov qword ptr [r15 + rax*8 + 0x21a6cf0], "
     "rbx` and `003300A4` / `003300B3` `[r15 + rdi*8 + 0x21a6e48]`, with `r15` = `00120000` at `0033007D`)*"),

    # C-V7 (A7): slot 11 clears bit 0x400 with btr rbx, 0xa at 00331715; 0033166F is slot 10's test rdi, -2.
    (S011, "| `0x0033166F` | `btr rdi, 0xb` — clears pending-resource bit `0x400` | ✅ |",
     "| ~~`0x0033166F`~~ `0x00331715` | ~~`btr rdi, 0xb`~~ `btr rbx, 0xa` — clears pending-resource bit `0x400` " + C
     + "`0x0033166F` is `test rdi, -2` in slot 10's handler, whose `btr rdi, 0xb` at `0x00331662` clears `0x800`; "
     "`FUN_003316b0` clears `0x400` at `0x00331715`)* | ✅ |"),

    # C-V8 (A8): CML1_ResolveNames sets +0x18 and +0x1A to 0xFFFF (003DA204, 003DA20B); the four channel pairs get
    #     (0, 0xFFFF). SHKCTL_ResolveNames does the same with +0x1C / +0x1E (003DD134, 003DD13B).
    (S008, "record are reset to `(0, 0xFFFF)` on every resolve — `+0x18`, `+0x118`, `+0x130`, `+0x148`,\n`+0x160`.",
     "record are reset ~~to `(0, 0xFFFF)`~~ on every resolve — `+0x18` to `(0xFFFF, 0xFFFF)`, and `+0x118`, `+0x130`, "
     "`+0x148`,\n`+0x160` to `(0, 0xFFFF)` " + C + "`0x003DA204` / `0x003DA20B` store `0xFFFF` to both `+0x18` and "
     "`+0x1A`; `0x003DA212`–`0x003DA247` store `0` / `0xFFFF` to the other four; BY-4 below)*."),
    (S010, "> reset five (u16,u16) pairs to (0, 0xFFFF)               0x003DD134 .. 0x003DD177\n",
     "> reset five (u16,u16) pairs to (0, 0xFFFF)               0x003DD134 .. 0x003DD177   <- corrected 2026-10-02, "
     "OPUS - the first pair, +0x1C / +0x1E, is set to (0xFFFF, 0xFFFF) at 0x003DD134 / 0x003DD13B; the other four to "
     "(0, 0xFFFF)\n"),

    # C-V9 (A9): +0x04 and +0x06 are two u16 (0037DAC4 cmp word [rcx + 4], 0; 0037DADD movzx ebx, word [rdi + 6]);
    #     +0x06 (curveCount) is 2..127, never 0, in all 113 us sections - there is no zero "upper half".
    (S011, "The loader reads only the low half. No\n  shipped file has a non-zero upper half, so the corpus cannot say "
           "whether the field was ever\n  intended to be 32 bits wide.",
     "The loader reads only the low half. ~~No~~\n  ~~shipped file has a non-zero upper half, so the corpus cannot say "
     "whether the field was ever~~\n  ~~intended to be 32 bits wide.~~ " + C + "there is no upper half — `+0x06` is "
     "`curveCount`, read on its own at `0x0037DADD` `movzx ebx, word ptr [rdi + 6]` and non-zero (2..127) in all 113 "
     "`us` sections, " + VBF + ")*"),

    # C-V10 (A10): [actor + 0xB8] is actor + 0x120 (00266B18-00266B2D); rbx comes from 003588B0 (the slot's actor
    #     array), so 0026338F-0026339D and 00269441-00269453 do not touch the shake chunk.
    (S010, "> **CA-1 answered 2026-09-12 (FABLE): the `CML1` chunk is read — through the per-record copy, for\n"
           "> kind-3 actors.** The second",
     "> **CA-1 answered 2026-09-12 (FABLE): ~~the `CML1` chunk is read — through the per-record copy, for~~\n"
     "> ~~kind-3 actors.~~** " + C + "retracted above, and the bytes agree — `rbx` in `00263230` is an actor from "
     "`003588B0` (the manager slot's actor array `[slot + 8]`), and `00266B18`–`00266B2D` set actor `+0xB8` = actor "
     "`+0x120`, so `[[actor + 0xB8] + 0xF0]` at `0026338F`–`0026339D` and `00269441`–`00269453` is not this chunk)* "
     "The second"),
    (S010, "> shake directory is live per-actor state for kind-3 actors — a script-start flag and a release-time\n"
           "> counter live inside it — and the section",
     "> ~~shake directory is live per-actor state for kind-3 actors — a script-start flag and a release-time~~\n"
     "> ~~counter live inside it —~~ " + C + "not this chunk — the retraction above)* and the section"),

    # C-V11 (A11): per-letter rule - at id + 1000 g 0/97, b 0/12, s 0/13, t 0/10; directly 77, 10, 10, 8 (VBF stems).
    (S012, "**Column 1 is the model number less 1000**, tested against",
     "**~~Column 1 is the model number less 1000~~** Column 1 is the model number less 1000 for `c`, `m` and `n` "
     "only; for `b`, `g`, `s` and `t` it is the model number itself " + C + "re-run against the `obj_finish` stems "
     "in `FFXII_TZA.vbf` — at `id + 1000` `g` 0 of 97, `b` 0 of 12, `s` 0 of 13, `t` 0 of 10; directly 77, 10, 10 and "
     "8; the per-letter table below)*, tested against"),

    # C-V12 (A12): 003DCA30 matches u32 +0x00 (003DCA70), u16 +0x06 (003DCA75) and u16 +0x04 (003DCADD) and returns
    #     u16 +0x08 (003DCA8C / 003DCAF2) - +0x08 is the result, not a key.
    (S019, "`+0x08`, at the other end, is nearly unique per record and reads\nlike an identifier.",
     "`+0x08`, at the other end, is nearly unique per record and ~~reads~~\n~~like an identifier~~ is the value the "
     "reader returns, the per-model motion index, not a key " + C + "`003DCA30` matches the `u32` at `+0x00` "
     "(`003DCA70`), the `u16` at `+0x06` (`003DCA75`) and at `+0x04` (`003DCADD`) and returns the `u16` at `+0x08` "
     "(`003DCA8C`, `003DCAF2`); §7, CC-10)*."),

    # C-V13 (A13): two header fields are read - +0x2C (003EAA32) and +0x0C (003EA650 at 003EA671, base 02B5E0C8).
    (S019, "**So four of the eight constant header fields are now proven inert and one is proven live.** The",
     "**So four of the eight constant header fields are now proven inert and ~~one is proven live~~ two are read — "
     "`+0x2C` here and `+0x0C` by the trailer reader.** " + C + "`003EA650(1)` loads `02B5E0C8` and reads `[base + "
     "0x0C]` at `003EA671`, besides `003EAA32` `mov ecx, dword ptr [rbx + 0x2c]`; BZ-2)* The"),

    # C-V14 (A14 + C5): the directory is u32[20] at +0x10 (0033051F [rdi + 0x18] = slot 2, 00330656 [rdi + 0x5c] =
    #     slot 19); +0x04 is compared against each slot number, a count, not a version.
    (R, "a version/count `0x14` at `+0x04`,\nand an offset table in 8-byte slots.",
     "a ~~version/count~~ slot count `0x14` at `+0x04`,\nand an offset table in ~~8-byte slots~~ 4-byte slots, `u32[20]` "
     "at `+0x10` " + C + "the walker `003304A0` compares `[rdi + 4]` with each slot number before reading slot `n` at "
     "`[rdi + 0x10 + 4n]` — slot 2 at `0033051F` `[rdi + 0x18]`, slot 19 at `00330656` `[rdi + 0x5c]`; "
     "Container/ebp2-container.md)*."),

    # C-V15 (A15): REQALL / REQIALL pop a channel - 00261B6C / 00261C69 call 00267E10 (VM pop), 00261B80 / 00261C7D
    #     mov [rsi + 0x26], al. The census TSV's channel_class n/a rows (B5) go to SWE2-DATA as a regenerate request.
    (S000, "`REQCHG`/`REQCANCEL`/`REQALL`/`REQIALL`\n",
     "`REQCHG`/`REQCANCEL`~~/`REQALL`/`REQIALL`~~ " + C + "`REQALL` and `REQIALL` pop a channel — `00261B6C` / "
     "`00261C69` `call 00267E10` into `[rsi + 0x26]` at `00261B80` / `00261C7D` — the correction that follows)*\n"),

    # C-V16 (A16): CAM7 record +0x20 is read by 002572E0 (00257341 and edx, 0x1ff; bit 15 at 002573BB-002573C6).
    (S009, "| **Not resolved by search alone, and it is not claimed.** The loader",
     "| ~~**Not resolved by search alone, and it is not claimed.**~~ **Yes — `002572E0` reads it** " + C
     + "`00257341` `mov edx, dword ptr [rdi + 0x20]` with `rdi` = blob + `[blob + 0x1C]`, the first record, and bit "
     "15 — the `0x8000` — at `002573BB`–`002573C6` `shr ecx, 0xf` / `and cl, 1`; §3's attachment word, corrected "
     "2026-09-12)*. The loader"),
    (S009, "Listed inert **with that method named**, not asserted unused. |",
     "~~Listed inert **with that method named**, not asserted unused.~~ *(answered: read — the correction at the head "
     "of this cell; 2026-10-02, OPUS)* |"),

    # C-V17 (B1): fifteen cmp [rdi + 4] sites, fourteen slot numbers (slot 12 at 003304DE and 003305E4).
    (CON, "a field the function reads fourteen times, and it is never touched.",
     "a field the function reads ~~fourteen~~ fifteen times " + C + "fifteen `cmp dword ptr [rdi + 4], N` sites over "
     "fourteen slot numbers — slot 12 is tested twice, at `003304DE` and `003305E4`; §6)*, and it is never touched."),

    # C-V18 (B2): image order is 0032FDD1 mov rdx, rbx; 0032FDD4 mov ecx, 0x25; 0032FDD9 mov r12d, eax.
    (CON, "0032FDD9  mov  r12d, eax           ;   kept only for the skip path\n",
     "0032FDD9  mov  r12d, eax           ;   kept only for the skip path   <- corrected 2026-10-02, OPUS - in the "
     "image this follows 0032FDD4 (0032FDD1 mov rdx, rbx; 0032FDD4 mov ecx, 0x25; 0032FDD9 mov r12d, eax)\n"),

    # C-V19 (B3): 17 distinct triples; the table's eight cover 1,087 of 1,114.
    (S000, "and the value triples distribute as:",
     "and the ~~value triples distribute as~~ eight most common of the 17 distinct triples are (1,087 of the 1,114 "
     "files) " + C + VBF + "; missing are `{30, 50, 20}` 9, `{80, 10, 5}` 5, `{0, 70, 30}` 4, `{1, 1, 1}` 4 and five "
     "single-file triples)*:"),

    # C-V20 (B4, both partly): no class-3 variable descriptor (0 of 43,466), but 389 scripts carry a tag-3 trap ref
    #     that 002641B0 -> 00265770 case 3 (002657B2) resolves to image + [image + 0x40].
    (S000, "class 3, no\n> shipped script uses it)",
     "class 3, ~~no~~\n> ~~shipped script uses it~~ which no shipped variable descriptor uses, though 389 of the 1,114 "
     "scripts reach it through the tag-3 trap reference at `+0x6C` " + C + "`002641B0` → `00265770` case 3 at "
     "`002657B2` = image + `[image + 0x40]`; 0 class-3 descriptors among 43,466 in the `+0x28` tables, " + VBF + ")*)"),

    # C-V21 (B6-B9): us section 6 - 67 files, 58 single / 9 two-picture, 56 at 448 B (55 24 x 23 + alc_f02 8 x 22);
    #     the table misses rwg_d01 64 x 23, alc_f02 8 x 22, nac_a0300 40 x 14.
    (S006, "11 distinct sizes; 57 of 67 are exactly 448 B |",
     "11 distinct sizes; ~~57~~ 56 of 67 are exactly 448 B " + C + VBF + " — the 55 24 × 23 files and `alc_f02`'s "
     "8 × 22)* |"),
    (S006, "+0x06  u16      pictureCount   1 (57 files) or 2 (10)\n",
     "+0x06  u16      pictureCount   1 (57 files) or 2 (10)   <- corrected 2026-10-02, OPUS - 1 in 58 files, 2 in 9 "
     "(us tree, read through vbf_read_entry)\n"),
    (S006, "which is `0x70` in the 57 single-picture 448 B files, and",
     "which is `0x70` in the ~~57 single-picture 448 B files~~ 55 single-picture 24 × 23 files (`headerSize` 96; the "
     "56th 448 B file, `alc_f02`'s 8 × 22, has `headerSize` 288) " + C + VBF + ")*, and"),
    (S006, "Height is 16, 21, 23 or 46 and never anything else — four values over 67 files.",
     "Height is ~~16, 21, 23 or 46 and never anything else — four values over 67 files~~ 14, 16, 21, 22, 23 or 46 — "
     "six values over 67 files, counting each file's first picture " + C + "the table above omits three files and so "
     "sums to 64 — 64 × 23 (`rwg_d01`), 8 × 22 (`alc_f02`) and 40 × 14 (`nac_a0300`, with a second 24 × 9 picture), "
     "one each; " + VBF + ")*."),
    (S006, "In every Latin-script tree the population is the same: 55–57 files carry one",
     "In every Latin-script tree the population is the same: ~~55–57~~ 55–56 " + C + "55 in `us`, `fr`, `it` and `es`, "
     "56 in `de`, " + VBF + ")* files carry one"),
    (S006, "one two-picture 640 × 46 (`evt_t0505`, 22,400 B). In",
     "one two-picture 640 × 46 (`evt_t0505`, 22,400 B) — and, not listed here, one 40 × 23 (two in `es`) and the "
     "two-picture 80 × 21, 576 × 21, 616 × 16 and 200 × 16 " + C + "the list is partial; " + VBF + ")*. In"),
    (S006, "- **10 files carry `pictureCount == 2`**,",
     "- **~~10~~ 9 files carry `pictureCount == 2`** " + C + "58 carry 1 and 9 carry 2 in the `us` tree, " + VBF
     + ")*,"),
    (S006, "With 57 of 67 at exactly 448 B,",
     "With ~~57~~ 56 " + C + "as §1's corrected size row)* of 67 at exactly 448 B,"),
    (S006, "- **The second picture header is not walked** in the 10 multi-picture files.",
     "- **The second picture header is not walked** in the ~~10~~ 9 " + C + "`pictureCount == 2` in 9 `us` files, "
     + VBF + ")* multi-picture files."),

    # C-V22 (B10): twelve distinct CAM7 record lengths over 3,942 records.
    (S009, "zero). Record length takes 11 distinct values.",
     "zero). Record length takes ~~11~~ 12 distinct values " + C + "3,942 records walked in the 423 `us` sections, "
     + VBF + " — 108, 152, 216, 280, 324, 388, 432, 496, 540, 560, 648, 1,296; the 2026-09-13 pass)*."),

    # C-V23 (B11): CAM7_Load has two call sites - 0032FB0A (in 0032FAC0) and 003312A7 (in the dead 003306E0).
    (S009, "was not established here; the one caller reads",
     "was not established here; ~~the one caller reads~~ the live caller, `0032FAC0` (call at `0032FB0A`), reads "
     + C + "`CAM7_Load` has two call sites — `0032FB0A`, and `003312A7` in `003306E0`, the loose-file route §6 finds "
     "dead in the shipped build)*"),

    # C-V24 (B12): 0032ED70 is or qword [022C6E48 + mgr*8], 1 (a pending-bit setter); teardown is 0032ED80.
    (S010, "Teardown is `FUN_0032ED70`: `0x0032F06F` loads",
     "Teardown is ~~`FUN_0032ED70`~~ `FUN_0032ED80` (`ActorResource_ResetManagerLoadState`) " + C + "`0x0032ED70` is "
     "four instructions that set bit 0 of the pending mask, `or qword ptr [rcx + rax*8], 1` on `022C6E48` at "
     "`0x0032ED70+0xA`; the addresses here lie in `0x0032ED80`'s body)*: `0x0032F06F` loads"),
    (S011, "Teardown is `FUN_0032ED70`: at `0x0032F027`",
     "Teardown is ~~`FUN_0032ED70`~~ `FUN_0032ED80` (`ActorResource_ResetManagerLoadState`) " + C + "`0x0032ED70` is "
     "`or qword ptr [022C6E48 + mgr*8], 1`, a pending-bit setter, `0x0032ED70+0xA`)*: at `0x0032F027`"),
    (S011, "| `0x0032ED70` | teardown — unbind, free, null |",
     "| ~~`0x0032ED70`~~ `0x0032ED80` | teardown — unbind, free, null " + C + "`0x0032ED70` is `or qword ptr "
     "[022C6E48 + mgr*8], 1`, a pending-bit setter)* |"),

    # C-V25 (B13): slot 8's blob is freed at 0032F005 (slot 9's at 0032EFBD), and only when 005C5230(5) != 0.
    (S008, "frees it at `0x0032EFBD`, and clears the slot at `0x0032F00C`.",
     "~~frees it at `0x0032EFBD`~~ passes it to the free at `0x0032F005` only when `0x005C5230(5)` returns non-zero, "
     "which it never does, and clears the slot at `0x0032F00C` " + C + "`0x0032EFBD` frees the slot-9 blob; slot 8's "
     "`[r14 + rdi*8 + 0x21a6d80]` is loaded at `0x0032EFD3` and its free is gated at `0x0032EFF4`–`0x0032F000`)*."),

    # C-V26 (B14): section 12 is in 842 of 1,114 us containers.
    (S012, "> A short list, in every third map file, naming",
     "> A short list, in ~~every third map file~~ 842 of the 1,114 map containers (75.6 %) " + C + VBF + "; §1's own "
     "count)*, naming"),

    # C-V27 (B15 + C24): the uppercase ids index a flat per-file list, not stems - 47 hc*.cm files over 17 stems ship in
    #     obj_finish/in/high (UQ-333 reads 48 table entries).
    (S012, "13 of 66 and 1 of 5 — **better than zero and not a finding**: each id set is larger than its\n"
           "candidate pool (40 ids against 17 `hc` stems), so the mapping cannot be complete whatever it means.\n"
           "Recorded as a lead.",
     "13 of 66 and 1 of 5 — ~~**better than zero and not a finding**: each id set is larger than its~~\n"
     "~~candidate pool (40 ids against 17 `hc` stems), so the mapping cannot be complete whatever it means.~~\n"
     "~~Recorded as a lead.~~ *(answered: the uppercase letters are the high-detail tables, indexed per file, not per "
     "stem — UQ-333 below; 2026-10-02, OPUS)* " + C + "`obj_finish/in/high` ships 47 `hc*.cm` files over those 17 "
     "stems, read through `vbf_load_index`; UQ-333's table holds 48 entries)*"),

    # C-V28 (B16): 423 files carry the 008/009 pair, 140 with 014, so 283 without.
    (S014, "while 423 files have the pair without `014`.",
     "while ~~423~~ 283 files have the pair without `014` " + C + "423 `us` files carry the pair and 140 of them "
     "`014`; " + VBF + ")*."),

    # C-V29 (B17): the 332 .ard files are 166 in `in` and 166 in `ch`; there are 166 map groups per tree.
    (S019, "(271 map instances against 332 map groups);",
     "(271 map instances against ~~332 map groups~~ 166 map groups per tree " + C + "the 332 `.ard` files are 166 in "
     "`in` and 166 in `ch`, counted in `vbf_load_index`'s names)*);"),

    # C-V30 (C1, C2, C3, C4): README stale - the container sheet is written, the magic reading is settled, the seven
    #     units have sheets, section 6's strips are expansion-glyph sheets in the in/ch/cn/kr trees.
    (R, "| `section_004` | 209 (18.7 %) | *unknown* |",
     "| `section_004` | 209 (18.7 %) | ~~*unknown*~~ `NAVIICN2` map-icon table, stored and never read in this build — "
     "[section-004](Sections/section-004.md) *(answered: see that sheet; 2026-10-02, OPUS)* |"),
    (R, "| `section_008` | 423 (37.9 %) | *unknown* — **strict pair with 009** |",
     "| `section_008` | 423 (37.9 %) | ~~*unknown*~~ `CML1` camera-name list — [section-008](Sections/section-008.md) "
     "*(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 009** |"),
    (R, "| `section_009` | 423 (37.9 %) | *unknown* — **strict pair with 008** |",
     "| `section_009` | 423 (37.9 %) | ~~*unknown*~~ `CAM7` camera table — [section-009](Sections/section-009.md) "
     "*(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 008** |"),
    (R, "| `section_010` | 113 (10.1 %) | *unknown* — **strict pair with 011** |",
     "| `section_010` | 113 (10.1 %) | ~~*unknown*~~ `CML1` shake-name list — [section-010](Sections/section-010.md) "
     "*(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 011** |"),
    (R, "| `section_011` | 113 (10.1 %) | *unknown* — **strict pair with 010** |",
     "| `section_011` | 113 (10.1 %) | ~~*unknown*~~ `SHK1` shake curves — [section-011](Sections/section-011.md) "
     "*(answered: see that sheet; 2026-10-02, OPUS)* — **strict pair with 010** |"),
    (R, "| `section_014` | 140 (12.6 %) | *unknown* |",
     "| `section_014` | 140 (12.6 %) | ~~*unknown*~~ `LGT2` light set — [section-014](Sections/section-014.md) "
     "*(answered: see that sheet; 2026-10-02, OPUS)* |"),
    (R, "| `section_019` | 271 (24.3 %) | *unknown* |",
     "| `section_019` | 271 (24.3 %) | ~~*unknown*~~ `FF12AR03` area data (`MAPARD`) — "
     "[section-019](Sections/section-019.md) *(answered: see that sheet; 2026-10-02, OPUS)* |"),
    (R, "> **Seven of the fourteen units have no tool-side lead at all.** That is the real work here, and it\n"
        "> is not large.",
     "> ~~**Seven of the fourteen units have no tool-side lead at all.** That is the real work here, and it~~\n"
     "> ~~is not large.~~ *(answered: all seven now have section sheets — the table above; 2026-10-02, OPUS)*"),
    (R, "23-pixel-high strips of varying width — pre-rendered text lines (section-006 §5) |",
     "23-pixel-high strips of varying width — ~~pre-rendered text lines~~ per-event expansion-glyph sheets in the "
     "`in` / `ch` / `cn` / `kr` trees, the Latin-tree strips possibly captions (section-006 §5) *(answered: the "
     "2026-09-24 refinement there; 2026-10-02, OPUS)* |"),
    (R, "**Settling it needs the loader body read in Ghidra.** Until then the sheet may not claim either.\n",
     "~~**Settling it needs the loader body read in Ghidra.** Until then the sheet may not claim either.~~ *(answered: "
     "the loader body is read, and the first reading holds — the walker `003304A0` never references `+0x00`; "
     "[Container/ebp2-container.md](Container/ebp2-container.md) §3; 2026-10-02, OPUS)*\n"),
    (R, "invariants. **§3, the loader contract,\nis still empty** and it is the point",
     "invariants. ~~**§3, the loader contract,~~\n~~is still empty**~~ *(answered: §3 is written — "
     "[Container/ebp2-container.md](Container/ebp2-container.md), `status: AUDITED`; 2026-10-02, OPUS)* and it is the point"),
    (R, "**The sheet is deliberately not written yet.** A `FORMAT.md`",
     "~~**The sheet is deliberately not written yet.**~~ *(answered: it is written — "
     "[Container/ebp2-container.md](Container/ebp2-container.md); 2026-10-02, OPUS)* A `FORMAT.md`"),

    # C-V31 (C6, C7, C8, C9): the container page's stale opens.
    (CON, "one is unused in this territory's data. Open question `PROPOSED-repos-1e-1`.",
     "one is unused in this territory's data. ~~Open question `PROPOSED-repos-1e-1`.~~ *(answered: BW-1 above — slot "
     "17 is zero in all nine shipped language trees; 2026-10-02, OPUS)*"),
    (CON, "**Not yet attacked:** whether another language's archive populates slot 17\n"
          "(`PROPOSED-repos-1e-1`) — that needs the `jp`/`eu` trees, which are not unpacked here.",
     "~~**Not yet attacked:** whether another language's archive populates slot 17~~\n"
     "~~(`PROPOSED-repos-1e-1`) — that needs the `jp`/`eu` trees, which are not unpacked here.~~ *(answered: BW-1, "
     "§2 — no shipped tree populates slot 17, and `FFXII_TZA.vbf` carries no `jp` or `eu` tree, only `ch`, `cn`, "
     "`de`, `es`, `fr`, `in`, `it`, `kr` and `us`; 2026-10-02, OPUS)*"),
    (CON, "- **Slot 14's manager-0 exclusion is described, not explained.** What distinguishes manager 0 is\n  open.",
     "- ~~**Slot 14's manager-0 exclusion is described, not explained.** What distinguishes manager 0 is~~\n"
     "  ~~open.~~ *(answered: BW-3, §3 — manager 0's lighting comes from the map-control pack, not from EBP; "
     "2026-10-02, OPUS)*"),
    (CON, "guarantees a low arena — `FUN_0036c660` was not read.",
     "guarantees a low arena~~ — `FUN_0036c660` was not read~~ *(answered: read since — a header tagger, not an "
     "allocator, the 2026-09-12 correction directly below; 2026-10-02, OPUS)*."),
    (CON, "| `0x003DFE60` | shared binder for slot 16 (selector 0) and slot 17 (selector 1) | not read |",
     "| `0x003DFE60` | shared binder for slot 16 (selector 0) and slot 17 (selector 1) | ~~not read~~ read — "
     "`g_fieldRoots[selector] = ptr`, the store at `0x003DFE6A` *(answered: section-016.md key addresses; "
     "2026-10-02, OPUS)* |"),
    (CON, "destinations of the dispatch. **Their bodies were not read**,\n  so the \"what it does with the pointer\" "
          "column in §3 describes the *handler*, not the consumer.",
     "destinations of the dispatch. ~~**Their bodies were not read**,~~\n  ~~so the \"what it does with the "
     "pointer\" column in §3 describes the *handler*, not the consumer.~~ *(answered: the section sheets have read "
     "them since — `0026C880` (section-002), `0026CE00` (section-008), `0026CE40` (section-012), `0026D3A0` "
     "(section-010), `003DFE60` (section-016); 2026-10-02, OPUS)*"),

    # C-V32 (C10): the weather reader is found (002658EB, BW-4; the roll in 0025ACA0).
    (S000, "strong, but the *reader* was not found — see §7. |",
     "strong~~, but the *reader* was not found — see §7.~~ *(answered: `002658B0` reads it at `002658EB` — BW-4 in "
     "§4; 2026-10-02, OPUS)* |"),
    (S000, "- **Who reads `weatherProbability` was not found.** `ActorManager_BindLoadedDefinitionPayload` does\n"
           "  **not** read `+0x64`; the consumer is in the weather subsystem and was not identified. So the",
     "- ~~**Who reads `weatherProbability` was not found.**~~ `ActorManager_BindLoadedDefinitionPayload` does\n"
     "  **not** read `+0x64`; ~~the consumer is in the weather subsystem and was not identified.~~ *(answered: "
     "`002658B0` reads it for the chooser `0025ABA0` and the survival roll `0025ACA0` — BW-4 in §4, corrected "
     "2026-10-02; 2026-10-02, OPUS)* So the"),

    # C-V33 (C11, C12): section 2's character table and renderer opens.
    (S002, "  <A5> Sigil of Sacrifice`) and `0xA3` are unresolved.",
     "  <A5> Sigil of Sacrifice`) and `0xA3` ~~are unresolved~~ are the hyphen *(answered: section-003-text.md, BX-2 "
     "of 2026-09-15; 2026-10-02, OPUS)*."),
    (S002, "(`FUN_00269F20`, `FUN_002E16B0`), which this document did not read. The",
     "(`FUN_00269F20`, `FUN_002E16B0`)~~, which this document did not read~~ *(answered in part: BX-1 below reads the "
     "window path through `002E16B0`; the escape semantics stay open; 2026-10-02, OPUS)*. The"),

    # C-V34 (C14): section 4's section 7 against its own section 3 and front matter.
    (S004, "- **No loader contract.** Section 3 has no `Read by` entry that is a real instruction address. That\n"
           "  is the main gap in this sheet and the reason its status is `PARTIAL`, not `DOCUMENTED`. Until the",
     "- ~~**No loader contract.** Section 3 has no `Read by` entry that is a real instruction address. That~~\n"
     "  ~~is the main gap in this sheet and the reason its status is `PARTIAL`, not `DOCUMENTED`.~~ *(answered: §3, "
     "established 2026-09-04, is the loader contract — `FUN_00332100` → `FUN_003DFDC0` stores the pointer and reads "
     "nothing; the front matter says `status: AUDITED`; 2026-10-02, OPUS)* Until the"),
    (S004, "clamped or ignored — and **no field\n  below is marked `Inert`**, because \"no reader found\" is not "
           "\"inert\" when the reader itself has not\n  been located.",
     "clamped or ignored~~ — and **no field~~\n  ~~below is marked `Inert`**, because \"no reader found\" is not "
     "\"inert\" when the reader itself has not~~\n  ~~been located.~~ *(answered: §3 marks four fields `YES — never "
     "read` on the handler path; 2026-10-02, OPUS)*."),

    # C-V35 (C15): section 19's section 7 and section 2 against its corrections.
    (S019, "- **No loader contract.** No `Read by` cell in section 3 holds a real instruction address, which is\n"
           "  why the status is `PARTIAL`. **No field is marked `Inert`**, because a field cannot be shown inert\n"
           "  by a search that never found the reader.",
     "- ~~**No loader contract.** No `Read by` cell in section 3 holds a real instruction address, which is~~\n"
     "  ~~why the status is `PARTIAL`. **No field is marked `Inert`**, because a field cannot be shown inert~~\n"
     "  ~~by a search that never found the reader.~~ *(answered: §3, established 2026-09-04, is the loader contract — "
     "`003EAA32` reads `+0x2C`, and the field table marks the never-read fields; the front matter says `status: "
     "AUDITED`; 2026-10-02, OPUS)*"),
    (S019, "- **The eight constant `u32` in the header are not explained**, and `0x30` being the offset of\n"
           "  `countA` is noted as suggestive and nothing more.",
     "- ~~**The eight constant `u32` in the header are not explained**, and `0x30` being the offset of~~\n"
     "  ~~`countA` is noted as suggestive and nothing more.~~ *(answered: they are the eight directory slots, and "
     "`+0x2C = 0x30` is the slot-7 offset the handler follows to `countA` — BZ-2, §2 and §3; 2026-10-02, OPUS)*"),
    (S019, "> directory, same size, same absent slots — and structural",
     "> directory, same size~~, same absent slots~~ " + C + "the absent slots are not the same — the 2026-09-05 audit "
     "correction above)* — and structural"),
    (S019, "is not tested here** — the\n`.ard` files were not extracted from the archive for this block, and a claim",
     "is not tested here** — ~~the~~\n~~`.ard` files were not extracted from the archive for this block, and~~ "
     "*(answered: the 166 `.ard` files were since parsed for the 2026-09-05 audit, §2, though not compared byte for "
     "byte; 2026-10-02, OPUS)* a claim"),
    (S019, "| `003320D0` | the `.ard` stream-completion callback, installed at `00331D89`+ | ❌ not read |",
     "| `003320D0` | the `.ard` stream-completion callback, installed at `00331D89`+ | ~~❌ not read~~ read in full in "
     "§3 — 13 bytes, `and rcx, 0xFFFFFFF0` then `jmp FUN_003EAA00` *(answered: §3; 2026-10-02, OPUS)* |"),

    # C-V36 (C16): section 6's not-read / open rows against its section 3 and section 5.
    (S006, "| `0037F1F0`, `003BC4E0`, `00575710`, `0029CAC0` | the four callers | ❌ not read |",
     "| `0037F1F0`, `003BC4E0`, `00575710`, `0029CAC0` | the four callers | ~~❌ not read~~ `0029CAC0` read in §3 "
     "and `003BC4E0` read as an event dispatcher (the `003BC4E0` subtree section); `0037F1F0` and `00575710` not read "
     "*(answered in part; 2026-10-02, OPUS)* |"),
    (S006, "**none of its four callers is in the `atelload.c` unit**. Left open rather than asserted. |",
     "**none of its four callers is in the `atelload.c` unit**. ~~Left open rather than asserted.~~ *(answered: §3 "
     "makes the link through the container directory — the slot-6 handler `00330060` tail-jumps to `0029CAC0` at "
     "`00330105`, which tail-jumps to `0039BEC0` at `0029CAFE`; 2026-10-02, OPUS)* |"),
    (S006, "looking for any of its callers inside `atelload.c`'s address range. All four are outside it. The\n"
           "attempt failed to confirm the link,",
     "looking for any of its callers inside `atelload.c`'s address range. All four are outside it. ~~The~~\n"
     "~~attempt failed to confirm the link,~~ *(answered: the link runs through the container walker, not "
     "`atelload.c` — `00330105` `jmp 0029CAC0`, `0029CAFE` `jmp 0039BEC0`, §3; 2026-10-02, OPUS)* The attempt by "
     "address range could not confirm it,"),
    (S006, "- **The palette source is unknown.** All 67 blocks",
     "- ~~**The palette source is unknown.**~~ *(answered in part: the text renderer supplies the colours — §5, "
     "2026-09-25; which table it uses is not stated; 2026-10-02, OPUS)* All 67 blocks"),

    # C-V37 (C17): section 8's section 7 / 8 against BY-5 and the written section-010 sheet.
    (S008, "- **`section_010`'s subset relationship is stated, not explained.** All 113 files with the shake\n"
           "  pair also have the camera pair; no mechanism is offered for why.",
     "- ~~**`section_010`'s subset relationship is stated, not explained.**~~ All 113 files with the shake\n"
     "  pair also have the camera pair; ~~no mechanism is offered for why.~~ *(answered: the co-occurrence is not "
     "engine-enforced — BY-5, answered 2026-09-26, §2; 2026-10-02, OPUS)*"),
    (S008, "`repos-c7`'s unit; the sheet does not exist yet, so this is\n  deliberately not a link.",
     "`repos-c7`'s unit; ~~the sheet does not exist yet, so this is~~\n  ~~deliberately not a link.~~ its sheet is "
     "[`section-010.md`](section-010.md) *(answered: written since; 2026-10-02, OPUS)*."),

    # C-V38 (C18): CAM7 record +0x28 is firstCommand, not subCount.
    (S009, "**`subCount` at record `+0x28` is 1 in 3,941 of 3,942 records.** The single",
     "**~~`subCount`~~ `firstCommand` (the first command's type) at record `+0x28` is 1 in 3,941 of 3,942 records.** "
     "*(answered: \"The lead held (2026-09-12)\" below and the §2 fence; 2026-10-02, OPUS)* The single"),

    # C-V39 (C20): section 10's PROPOSED-repos-c7-1 closed, and the missing section 3b.
    (S010, "**no reader found by the searches in §3b** |",
     "**no reader found by the searches in ~~§3b~~ §3, \"How far 'no reader found' goes\"** " + C + "the page has no "
     "§3b)* |"),
    (S010, "`0x02098F00` — is not closed. That residue is open question **PROPOSED-repos-c7-1**.",
     "`0x02098F00` — ~~is not closed. That residue is open question **PROPOSED-repos-c7-1**.~~ is closed *(answered: "
     "PROPOSED-repos-c7-1 is closed by `repos-4b`'s pass, §7, and `0x003DD230` reads entry `+0x04` at `0x003DD29F`, "
     "§3; 2026-10-02, OPUS)*."),
    (S010, "| Is the section really never parsed? | **Not established, and deliberately not claimed.** Two",
     "| Is the section really never parsed? | ~~**Not established, and deliberately not claimed.**~~ *(answered: it "
     "is read — `SHKCTL_ResolveNames` walks it at load and `0x003DD230` reads entry `+0x04` at `0x003DD29F`, §3 and "
     "§6a; 2026-10-02, OPUS)* Two"),

    # C-V40 (C21, C22): section 11's dataOffset width and the unnamed key floats.
    (S011, "**read 16-bit only — the high half of the u32 is discarded.**",
     "**read 16-bit only~~ — the high half of the u32 is discarded~~.** " + C + "`+0x08` is a `u16` and `+0x0A` its "
     "own unread `u16` — §2.1's fence, audit note of 2026-09-05)*"),
    (S011, "Declared `u32` at `+0x08` in §2.1 and read",
     "Declared ~~`u32`~~ `u16` " + C + "§2.1's fence, audit note of 2026-09-05)* at `+0x08` in §2.1 and read"),
    (S011, "| `0x0037DAF5` | **16-bit read of the 32-bit `+0x08`** — the truncation |",
     "| `0x0037DAF5` | **16-bit read of the ~~32-bit~~ `u16` `+0x08`** " + C + "§2.1's fence)* ~~— the truncation~~ |"),
    (S011, "**Seven of the nine are named `_unnamedN` on purpose.** Every",
     "**~~Seven~~ Three of the nine are named `_unnamedN` on purpose.** " + C + "the fence names six — `startFrame`, "
     "`coefA`–`coefD`, `weight` — and leaves three `_unnamed`, the 2026-09-26 note below)* Every"),

    # C-V41 (C24): section 12's consumer and id-list opens, answered 2026-09-25 to 2026-09-27.
    (S012, "> **The consumer is not in this function and this document does not claim to have found it.** It",
     "> **The consumer is not in this function~~ and this document does not claim to have found it~~.** *(answered: "
     "there is none — nothing in this executable walks the section, §7, 2026-09-27; 2026-10-02, OPUS)* It"),
    (S012, "> needs the id list, and the database does not store one**: the 112 came from `repos-4b`'s own\n"
           "> parser over 1,114 containers, and no `members/` file on this page carries them.",
     "> ~~needs the id list, and the database does not store one~~**~~: the 112 came from `repos-4b`'s own~~\n"
     "> ~~parser over 1,114 containers, and no `members/` file on this page carries them.~~ *(answered: "
     "`members/section012-model-ids.tsv` stores it, and UQ-334 is answered from it, 2026-09-25; 2026-10-02, OPUS)*"),
    (S012, "suffices without a second numbering. **Not closed** — that is sufficiency, not proof, and the id\n"
           "      list needed to finish it is not stored anywhere.",
     "suffices without a second numbering. ~~**Not closed** — that is sufficiency, not proof, and the id~~\n"
     "      ~~list needed to finish it is not stored anywhere.~~ *(answered: closed by the 2026-09-25 answer above, "
     "from `members/section012-model-ids.tsv`; 2026-10-02, OPUS)*"),

    # C-V42 (C25): 0032F1B0 is the load finalizer (0032F1F9 call 0037AA90), not a teardown.
    (S012, "| `0032F1B0` | teardown path when the flags word goes to zero | ❌ |",
     "| `0032F1B0` | ~~teardown path~~ the load finalizer, `ActorResource_FinalizeManagerRuntimeAfterLoads`, run "
     "when the flags word goes to zero " + C + "`0032F1F9` calls the light binder `0037AA90` and `0032F227` "
     "`0026CE60`; section-014.md)* | ❌ |"),

    # C-V43 (C26): 003775D0 is read (CD-1) - it passes slot 0 (003776A4 xor edx, edx; 003776A6 call 0037AA90).
    (S014, "| `003775D0` | `FUN_003775d0` — the second binder caller (site `003776A6`) | ❌ not read |",
     "| `003775D0` | `FUN_003775d0` — the second binder caller (site `003776A6`) | ~~❌ not read~~ read — it passes "
     "manager slot 0, `003776A4` `xor edx, edx` *(answered: CD-1, 2026-09-12; 2026-10-02, OPUS)* |"),
    (S014, "and that caller is unread — so the branch is **not**\n  claimed dead, only shown to be unreachable by the "
           "one route this sheet establishes.",
     "~~and that caller is unread — so the branch is **not**~~\n  ~~claimed dead, only shown to be unreachable by the "
     "one route this sheet establishes.~~ *(answered: it does pass 0 — CD-1 directly below; 2026-10-02, OPUS)*"),
    (S014, "— **not read.** The second binder caller may pass a\n    different manager index and I have not checked "
           "which; see",
     "— ~~**not read.** The second binder caller may pass a~~\n    ~~different manager index and I have not checked "
     "which;~~ *(answered: read — it passes slot 0, `003776A4` `xor edx, edx`, CD-1; 2026-10-02, OPUS)* see"),

    # C-V44 (C27): type 2 is the ellipse (CC-3, 00236513-00236586).
    (S016, "| a third shape, too rare to characterise |",
     "| a third shape~~, too rare to characterise~~: an ellipse *(answered: `CC-3`, §5 — `00236513`–`00236586`; "
     "2026-10-02, OPUS)* |"),
    (S016, "Nineteen records in 25,687. Too few to characterise honestly.",
     "Nineteen records in 25,687. ~~Too few to characterise honestly.~~ *(answered: an elliptical region — `CC-3` "
     "above, `00236513`–`00236586`; 2026-10-02, OPUS)*"),
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
