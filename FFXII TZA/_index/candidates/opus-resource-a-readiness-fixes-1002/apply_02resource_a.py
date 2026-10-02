"""apply_02resource_a.py [--apply] - 02-Resource-And-Asset-Pipeline readiness map (cloud-reports/re-readiness/02-resource.md),
section 3.1 part A: value items C-V1 onward through the archive / st2e / battle_pack / text group (60 items), settled on
the pages (OPUS, 2026-10-02).

Each edit strikes the side the shipping image (or the shipped data) REFUTES and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* with the deciding instruction cited as entry+offset. Items whose favoured side the
bytes confirm get edits only on the unstruck refuted lines; items the bytes leave undecided, or where both sides hold,
get no edit (C-V11, C-V15, C-V118, C-V120, C-V121 - see verdicts-02a.md in the OPUS scratch).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `<- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; no heading changes (the VBF ### heading "block 3 is the battle command
menu" is left; the body lines under it are corrected).
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "02-Resource-And-Asset-Pipeline/"
FST = F + "Loose-Files-And-Size-Tables/file-size-tables-fst.md"
RQ = F + "the-resource-request-queue.md"
TREE = F + "CONTRACT-resource-entry-tree.md"
RSA = F + "resource-section-addressing.md"
CSA = F + "CONTRACT-resource-section-addressing.md"
EFX = F + "CONTRACT-efx-source-rebase.md"
EXT = F + "the-external-source-owner-and-borrowed-view-lifetime.md"
EV = F + "authored-reference-lifetime-evidence.md"
OWN = F + "the-resource-owner-from-copy-or-borrow-to-disposal.md"
ROW = F + "CONTRACT-authored-table-row-lookup.md"
REG = F + "authored-data-table-registry.md"
RM = F + "README.md"
V = F + "VBF-Archive-And-Authored-Tables/"
VBF = V + "vbf-archive-and-st2e-tables.md"
S2R = V + "St2e-Carriers/README.md"
BTB = V + "St2e-Carriers/battle-text-banks.md"
BIG = V + "how-the-bigfile-index-loads-and-is-verified.md"
PATH = V + "how-a-path-is-resolved-to-bytes.md"

C = "*(corrected 2026-10-02, OPUS: "
BSS = "past `.data`'s raw end `0x01F7E400`"
SETTER = "`00238390+0x1A` writes `0x02EBF1A0`"
DIR72 = ("`003846F0+0x56` `lea rbx, [r9 + 4]`, `003846F0+0x97` `add rbx, 4`, over count + 1 entries to "
         "`003846F0+0x9B` `cmp rdi, rax` and the `jle` at `003846F0+0x9E`")
TAILS = ("`003847B0+0xA`, `00238640+0xE` and `0023A160+0x22` / `0023A160+0x31` / `0023A160+0x40` / `0023A160+0x61` "
         "jump to `003845F0`, and `0023A160+0x52` to `003846F0`")
CODEC = ("`0020E620` subtracts the base's low dword and `0020E600+0x2` adds the full qword back, so the pair returns "
         "`base + ((p - base) mod 2^32)`")
CALLERS_D540 = "three direct callers, `0022B0B0+0xE1`, `0022B8C0+0x67` and `0022BC20+0x4F`"

EDITS = [
    # ---- File-size table, request queue, read path ----
    # C-V1: +0x40 is the done callback (0032E330+0x6, ok = 1); +0x48 is called only on cancel (0032E070+0x106,
    #       0032E2F0+0x6).
    (FST, "the completion callback at slot `+0x48` — is read only far enough",
     "~~the completion callback at slot `+0x48`~~ the done callback at slot `+0x40` and the cancel callback at `+0x48` "
     + C + "`0032E330+0x6` loads `+0x40` and calls it with ok = 1; `+0x48` is called only on cancel, at "
     "`0032E070+0x106` in state 4 and `0032E2F0+0x6`)* — is read only far enough"),
    # C-V2: the 4th argument is the byte count (0032E870+0xBC stores it at +0x28; 0032E620+0xF3 cmp eax, 0x80000).
    (FST, "`0032E620(kind, index, dest, id, …)` records",
     "`0032E620(kind, index, dest, ~~id~~ bytes, …)` " + C + "the fourth argument is the byte count — "
     "`0032E870+0xBC` `mov dword ptr [r10 + 0x28], esi` stores it and `0032E620+0xF3` compares it with `0x80000`)* "
     "records"),
    # C-V3: 0046DD50 is dormant (state word BSS, only self-writers) and its state 2 rounds UP (0046DD50+0x96).
    (FST, "after the `0016D6A0` fill, state 4 gates on `0053DD10` and clears, state 3 needs `0053DD10` + `00368F30` "
          "quiet then arms `00369050` on `00536F30` and steps to 4, state 2 does `0053DD10` + `00368F30` then zeroes "
          "the state, and state 1 sizes the next stage from `02EBB52C`/`02EBB528`/`02EBB520` (each `(x + (x>>31 & "
          "0x7FF))` rounded down by `>> 0xB`) into `02EBA520` via `0016D6A0` before stepping to 3 - the four-state load "
          "pipeline the pump advances",
     "after the `0016D6A0` fill, ~~state 4 gates on `0053DD10` and clears, state 3 needs `0053DD10` + `00368F30` "
     "quiet then arms `00369050` on `00536F30` and steps to 4, state 2 does `0053DD10` + `00368F30` then zeroes "
     "the state, and state 1 sizes the next stage from `02EBB52C`/`02EBB528`/`02EBB520` (each `(x + (x>>31 & "
     "0x7FF))` rounded down by `>> 0xB`) into `02EBA520` via `0016D6A0` before stepping to 3 - the four-state load "
     "pipeline the pump advances~~ state 1 clears once `0053DD10` returns 0; state 2 needs `0053DD10` at 0, rounds "
     "`02EBB52C` and `02EBB528` **up** to the `0x800` sector (`x + 0x7FF` before the sign bias, then the mask or "
     "`>> 0xB`) and passes them, with `02EBB520` and `02EBA520`, to `0016D6A0` before stepping to 3; state 3 needs "
     "`0053DD10` + `00368F30` quiet, arms `00369050` on `00536F30` and steps to 4; state 4 clears once `00368F30` is "
     "quiet. None of it runs: `02CA6068` is BSS (" + BSS + ") and its only writers are this function's own stores, "
     "so the word stays 0 and the stepper returns at once " + C + "the dispatch at `0046DD50+0x12` .. `0046DD50+0x25` "
     "sends states 1-4 to `0046DD50+0xDE` / `0046DD50+0x80` / `0046DD50+0x47` / `0046DD50+0x2B`; `0046DD50+0x96` is "
     "`add eax, 0x7ff`; the writers are `0046DD50+0x3C`, `0046DD50+0x71`, `0046DD50+0xCF` and `0046DD50+0xF0`; the "
     "queue page's §8 reads it as dormant)*"),
    # C-V73: 002DF6C0 serves kind 0xFF only (one call site 0032E070+0xA1, behind 0032E070+0x67 cmp al, 0xff).
    (FST, "is the gated submit-or-decline wrapper `0032E070` runs per request:",
     "is the gated submit-or-decline wrapper `0032E070` runs ~~per request~~ for kind-`0xFF` (raw-path) requests only "
     + C + "its one call site `0032E070+0xA1` sits behind `0032E070+0x67` `cmp al, 0xff`; every other kind goes "
     "`0046E030` → `002DF780`)*:"),
    # C-V4: the cancel 0032E590 has four direct callers; the struck list is 0032E4D0's.
    (RQ, "Callers: `00280140`,\n`00291D90`, `002CEB40`, `002E60F0`, `002FC3C0`, `002FCF00` and the `003B1310`–`003B21E0` "
         "family.",
     "Callers: ~~`00280140`,~~\n~~`00291D90`, `002CEB40`, `002E60F0`, `002FC3C0`, `002FCF00` and the "
     "`003B1310`–`003B21E0` family.~~ `002FC3C0`, `003B1310`, `003B1710` and `003B18E0`, four in all " + C
     + "the direct calls are `002FC3C0+0x66`, `003B1310+0x9F`, `003B1710+0xAD` and `003B18E0+0xBD`, with no `jmp` or "
     "thunk; the struck list is the callers of the in-flight test `0032E4D0`)*."),
    # C-V64: 003EADE0 is 522 B.
    (RQ, "`003EADE0` (512 B) — the request state machine",
     "`003EADE0` (~~512 B~~ 522 B " + C + "the body runs 522 bytes from `003EADE0`, as the key-address table "
     "states)*) — the request state machine"),
    # C-V65: 0032E040 has ten calling functions at eleven sites.
    (RQ, "`0032E040` — 38 B, 8 A-measured callers;",
     "`0032E040` — 38 B, ~~8 A-measured callers~~ ten calling functions at eleven sites " + C + "direct calls from "
     "`0022A0B0`, `0022A770`, `0022AF50`, `0022B000`, `0022B6E0`, `0022B7E0`, `0022B8C0`, `0022BC20`, `00379E30` and "
     "twice from `0036EEB0`, the set §2.3 lists)*;"),
    # C-V108: the builder writes +4 = 0x80000 into its own stack copy; the caller's descriptor is only read.
    (RQ, "  +0x00 i32 fileOffset   +0x04 i32 (set to 0x80000 by the builder)   +0x08 i32 arg\n",
     "  +0x00 i32 fileOffset   +0x04 i32 (set to 0x80000 by the builder)   +0x08 i32 arg   <- corrected 2026-10-02, "
     "OPUS: the builder sets +0x04 in its own stack copy (0032E620+0xAC mov dword ptr [rsp + 0x34], 0x80000); the "
     "caller's descriptor is only read (0032E620+0x58)\n"),
    # C-V35: the board slots hold the loaded boards' addresses (00384420+0x5E mov rbx, rax; 00384420+0x99 desc +8).
    (RQ, "requester that wants its bytes reads them at `dest0`. The twelve licence-board requests of\n"
         "`00238260` hand `3` in that word (`00238364`), so their generated setters (`00238390` + `0x30·k`)\n"
         "store **3** into registry slots `02EBF1A0`–`02EBF1F8` on delivery and on failure alike — the slots\n"
         "are completion markers, and the board bytes live in the resource block the loader allocated\n"
         "([the registry page](authored-data-table-registry.md), *the tail read*, corrected 2026-09-11).",
     "requester that wants its bytes reads them at `dest0`. ~~The twelve licence-board requests of~~\n"
     "~~`00238260` hand `3` in that word (`00238364`), so their generated setters (`00238390` + `0x30·k`)~~\n"
     "~~store **3** into registry slots `02EBF1A0`–`02EBF1F8` on delivery and on failure alike — the slots~~\n"
     "~~are completion markers, and the board bytes live in the resource block the loader allocated~~\n"
     "~~([the registry page](authored-data-table-registry.md), *the tail read*, corrected 2026-09-11).~~ The twelve "
     "licence-board requests of `00238260` go through `00384420`, which replaces the `3` with the buffer it "
     "allocated before it builds the descriptor, so their generated setters (`00238390` + `0x30·k`) store the "
     "loaded board's address into registry slots `02EBF1A0`–`02EBF1F8` on delivery and on failure alike: the slots "
     "are pointers to the boards " + C + "`00384420+0x5E` `mov rbx, rax` after the `0036A190` allocation, then "
     "`00384420+0x99` `mov dword ptr [rsp + 0x38], ebx` writes the descriptor's `+8`; "
     "[the registry page](authored-data-table-registry.md), *the tail read*, corrected 2026-09-30)*."),

    # ---- Arena, tree, handles, image address ----
    # C-V6: the re-resolve flag is 02B62E10 (00409600+0x22); 027A2E10 has no reference.
    (TREE, "the `027A2E10` flag is armed,",
     "the ~~`027A2E10`~~ `02B62E10` flag " + C + "`00409600+0x22` compares the byte at `02B62E10` with 0, and "
     "`0041E500+0x9` / `0041E500+0x1C` set and clear it; nothing in the image references `027A2E10`)* is armed,"),
    # C-V7: the 003AB7F0 guard compares unsigned(sext(low32(r))) with 0x40.
    (RSA, "                         else              -> r = 0036B130(h); r <= 0x40 ? 0 : r\n",
     "                         else              -> r = 0036B130(h); r <= 0x40 ? 0 : r   <- corrected 2026-10-02, "
     "OPUS: the test is unsigned(sext(low32(r))) <= 0x40, not the full pointer (003AB7F0+0x41 movsxd rcx, eax; "
     "003AB7F0+0x44 cmp rcx, 0x40; 003AB7F0+0x48 cmovbe rax, rbx)\n"),
    # C-V8: via 003AB7F0 an untagged handle comes back unchanged (003AB7F0+0x56 mov rax, rdx).
    (EFX, "    if handle == 0 or (handle & 3) == 0: return 0      # tag required\n",
     "    if handle == 0 or (handle & 3) == 0: return 0      # tag required   <- corrected 2026-10-02, OPUS - "
     "through 003AB7F0 an untagged handle is returned unchanged (003AB7F0+0x13 test dl, 3; 003AB7F0+0x56 mov rax, "
     "rdx); only 0036B130 itself returns 0 for it\n"),
    # C-V13: 767 and 319 entries (rbx starts at 8).
    (EFX, "- 768 entries repointed by the source-move delta",
     "- ~~768~~ 767 entries repointed (indices 1 to 767; `rbx` starts at 8) by the source-move delta " + C
     + "`003A9BA0+0xD` `mov ebx, 8` and `003A9BA0+0x50` `cmp rbx, 0x1800`)*"),
    (EFX, "- 320 entries repointed by the same delta",
     "- ~~320~~ 319 entries repointed (indices 1 to 319) by the same delta " + C + "`003A9860+0xD` `mov ebx, 8` and "
     "`003A9860+0x50` `cmp rbx, 0xa00`)*"),
    # C-V14: above the window the offset wraps back inside it; below the base it decodes 2^32 too high.
    (EFX, "Past that the stored offset wraps and later\n> resolves to the wrong address *inside* the arena — silently, "
          "and without the delta being wrong.",
     "~~Past that~~ Above that window the stored offset wraps and later\n> resolves to the wrong address ~~*inside* the "
     "arena~~ back inside the window — silently, and without the delta being wrong; below the base it decodes `2^32` "
     "too high, outside the window " + C + "`0020E620` keeps 32 bits and `0020E600+0x2` adds the qword base to the "
     "zero-extended offset, so a pointer below the base comes back as `p + 2^32`; the entry-tree contract's "
     "2026-09-15 correction, EXP-083)*."),
    # C-V16: the exact range is -2^31 <= delta < 2^31.
    (EFX, "- **`|delta| >= 2 GiB`** — pointers shift by `delta - 2^32`;",
     "- **~~`|delta| >= 2 GiB`~~ `delta` outside `[-2^31, 2^31)`** — pointers shift by ~~`delta - 2^32`~~ "
     "`delta - 2^32` above and `delta + 2^32` below (`-2^31` itself is exact) " + C + "`0024D970+0x14` "
     "`sub ebx, dword ptr [rcx + 0x858]` forms a 32-bit delta and `003A9BA0+0xA` `movsxd rsi, ecx` sign-extends it; "
     "§13's `reb-delta-neg2gib-exact`)*;"),
    # C-V18: 0024D540 has three callers.
    (EFX, "is run by `MainLoop_UpdateAndRenderFrame` and a 463-byte core body, and it calls an",
     "is run by `MainLoop_UpdateAndRenderFrame` ~~and a 463-byte core body~~, the 463-byte core body and the "
     "1,583-byte frame body `0022B0B0` " + C + CALLERS_D540 + ")*, and it calls an"),
    (EV, "  - `0024D540` is run by `MainLoop_UpdateAndRenderFrame`.",
     "  - `0024D540` is run by `MainLoop_UpdateAndRenderFrame` and by `0022B0B0` and `0022BC20` " + C
     + CALLERS_D540 + "; this line named one)*."),
    # C-V19: 0024D970's delta is a relocation delta added to every stored pointer.
    (EXT, "`arg2 - [rcx+0x858]` becomes a signed count fed in order to `003AA3D0`, `003A9BA0` and `003A9860`, and the "
          "new extent is then stored back into `+0x858` - the three callees consuming the queue backlog the delta "
          "represents before the record is marked current.",
     "`arg2 - [rcx+0x858]` becomes a ~~signed count~~ signed 32-bit address delta fed in order to `003AA3D0`, "
     "`003A9BA0` and `003A9860`, and the new ~~extent~~ base is then stored back into `+0x858` - the three ~~callees "
     "consuming the queue backlog the delta represents~~ walks that add the delta to every stored pointer " + C
     + "`0024D970+0x14` `sub ebx, dword ptr [rcx + 0x858]` is the low-32 difference of two bases, `0024D970+0x37` "
     "stores the new 64-bit base, and `003A9BA0+0x48` `add qword ptr [rbx + rcx], rsi` adds the sign-extended delta "
     "to each live slot: a relocation, the EFX source-rebase contract §3)* before the record is marked current."),
    # C-V66 (+ C-V10 on this line): +0x40 is copied into a dead stack slot; 00409780 hands back the offset.
    (EXT, "`00409780` yields the index (-1 returns 0); `+4 == 0` resolves the inline `+0x10` array through "
          "`0051EE30`/`006B5C70`, `+4 == 1` resolves the `+0x30` external row through `003AB880`, and `+0x40` adds a "
          "base offset",
     "`00409780` yields the ~~index~~ section offset (-1 returns 0); `+4 == 0` resolves the inline `+0x10` array "
     "through `0051EE30`/`006B5C70`, `+4 == 1` resolves the `+0x30` external row through `003AB880`, and ~~`+0x40` "
     "adds a base offset~~ that offset is added to the resolved base, while `+0x40` is only copied into the stack "
     "view and never read back " + C + "`00409960+0x8A` `mov eax, dword ptr [rdi + 0x40]` and `00409960+0x8D` "
     "`mov dword ptr [rsp + 0x70], eax`; the result is `00409960+0xAE` `lea eax, [rsi + rbx]` with `esi` the fifth "
     "output of `00409780`, and neither `0051EE30` nor `006B5C70` reads that view slot)*"),
    # C-V17: 003AB880 releases a tagged handle through 0036A000 (generation check, tree removal).
    (EXT, "is the alignment guard `00409960` and `0041E490` both run on a resolved record pointer: a null input returns "
          "0, a pointer with `ptr & 3 == 0` returns itself, and anything misaligned tail-jumps `0036A000` (the "
          "subsystem's invalid-parameter handler) with `ecx = ptr` - the 'aligned or die' check both record-resolver "
          "families share",
     "is ~~the alignment guard~~ the tagged-handle release `00409960` and `0041E490` both run on a ~~resolved record "
     "pointer~~ record handle: a null input returns 0, a pointer with `ptr & 3 == 0` (an untagged raw pointer) "
     "returns itself, and ~~anything misaligned~~ a tagged handle tail-jumps `0036A000` ~~(the subsystem's "
     "invalid-parameter handler)~~ with `ecx = ptr`, which checks the generation, removes the node from its arena "
     "tree and returns the payload ~~- the 'aligned or die' check both record-resolver families share~~ " + C
     + "`003AB880+0x21` `jmp 0x36a000`; `0036A000+0x38` `cmp word ptr [rdx + 6], ax` is the generation test, "
     "`0036A000+0x73` `call 0x36c790` the tree removal and `0036A000+0x78` `and byte ptr [rbx + 0x15], 0xfd` clears "
     "membership before `rbx + 0x40` is returned)*"),
    # C-V60: 00442460 is 82 B; the case table after it is data.
    (EXT, "`00442460` (121 B) is",
     "`00442460` (~~121 B~~ 82 B " + C + "the body ends with `00442460+0x51` `ret`; the nine-entry case table that "
     "follows it is data, not code)*) is"),
    # C-V61: 00442380 makes fifteen applies (0042FCF0 at +0x230).
    (EXT, "`00442380` (213 B) is the fourteen-slot field apply",
     "`00442380` (213 B) is the ~~fourteen-slot~~ fifteen-slot field apply"),
    (EXT, "then `00430AF0` over the seven `0x40`-stride subfields `+0x70`..`+0x1F0` - the common sweep",
     "then `00430AF0` over the seven `0x40`-stride subfields `+0x70`..`+0x1F0`, then `0042FCF0` once at `+0x230` "
     + C + "`00442380+0xB5` `lea rcx, [rdi + 0x230]` and `00442380+0xBE` `call 0x42fcf0`)* - the common sweep"),
    # C-V63: the ticket pool at 02EBCD80 has 32 records; 02EBD480 is a second 32-record pool.
    (OWN, "Type3 creation uses the 64 slots at `02EBCD80`, each0x38 bytes,",
     "Type3 creation uses the ~~64 slots~~ 32 slots at `02EBCD80`, each0x38 bytes " + C + "`003B3160+0x87` "
     "`cmp r8d, 0x20` ends the free-list build at 32 records whose words carry the slot index 0-31 "
     "(`003B3160+0x57` `and eax, 0x3f`); the next 32 records, at `02EBD480`, are the separate container-handle pool "
     "`003B3160+0x9B` builds)*,"),
    (OWN, "| O2 | §4 the ticket pool | **survives**: 64 slots of `0x38` at `02EBCD80`,",
     "| O2 | §4 the ticket pool | **survives**: ~~64 slots~~ 32 slots " + C + "`003B3160+0x87` `cmp r8d, 0x20`)* of "
     "`0x38` at `02EBCD80`,"),
    # C-V109: the copy length is truncated toward zero to a multiple of 16.
    (OWN, "signed32 rounded-down copy;",
     "~~signed32 rounded-down copy~~ copy of the signed-32 length truncated toward zero to a multiple of 16 " + C
     + "`003EDAD0+0x67D` `cdq`, `003EDAD0+0x67E` `and edx, 0xf`, `003EDAD0+0x681` `add eax, edx` and "
     "`003EDAD0+0x68D` `and eax, 0xfffffff0`)*;"),

    # ---- Section addressing ----
    # C-V5: the resource entries the J-3 refresh re-resolves are the [+0xD90] bank's 0x50 rows.
    (RSA, "So these rows are **`0xC0`\n      bytes**.",
     "So ~~these rows~~ the rows `002ED610` reads are **`0xC0`\n      bytes**; the resource entries this box asks "
     "about are the `[+0xD90]` bank's, whose stride is `0x50` (`RenderResourceEntry`) " + C + "the J-3 refresh "
     "`0041E500+0x10` loads `[rcx+0xD90]` for `00409F70`; `0041E3A0+0x3E` stores `root + 0` there and "
     "`0041E3A0+0xA2` hands it to `00409F10`, whose `00409F10+0x13` is `mov edx, 0x50`; `[+0xD98]` gets stride "
     "`0xC0` at `0046E250+0x22`)*."),
    (RSA, "`0x50` family (root `+0x000`) is a different descriptor, and its rows are not this box's.",
     "`0x50` family (root `+0x000`) is a different descriptor, and its rows are ~~not this box's~~ this box's resource "
     "entries " + C + "the mode-1 entries the J-3 refresh re-resolves are the `0x50` rows, as corrected above)*."),
    # C-V9: 00409780 is 429 B.
    (RSA, "`00409780` (`ResourceEntry_FindSectionIndexAndOffset`, ~101 B) —",
     "`00409780` (`ResourceEntry_FindSectionIndexAndOffset`~~, ~101 B~~, 429 B " + C + "the body runs 429 bytes "
     "from `00409780`; 101 B is the matcher `00409C30`)*) —"),
    # C-V10: 00409780 writes the offset through the fifth argument and the index through the fourth.
    (CSA, "the first hit writes its index to `*rsi` and its count to `*r9`, all misses writing -1.",
     "the first hit writes ~~its index to `*rsi` and its count to `*r9`~~ its table-relative offset through the "
     "fifth argument (`*rsi`) and its index through the fourth (`*r9`) " + C + "`00409780+0x1A` loads `rsi` from the "
     "fifth-argument slot, `00409780+0x118` `mov dword ptr [rsi], ecx` stores `offset + 0x40` and `00409780+0x18F` "
     "`mov dword ptr [r14], r9d` the loop index, `r14` being `r9`)*, all misses writing -1."),
    # C-V12: a DWORD offset table walked 4 bytes at a time; stored offsets are relative to the table's +0x30/+0x40.
    (RSA, "so the iteration stride **is** `0x30`.",
     "so ~~the iteration stride **is** `0x30`~~ the header is `0x30` bytes, but the walk steps a 4-byte DWORD offset "
     "table that starts there, and each section sits at `+0x30` plus its offset " + C + "`00409780+0x13E` "
     "`lea r11, [r10 + 0x30]`, `00409780+0x15D` `add r11, 4`, and `00409780+0x148` `add ecx, 0x30` / "
     "`00409780+0x14D` `add ecx, r10d` locate each section)*."),
    (RSA, "Real sections\nbegin at `+0x30` (variant 0) or `+0x40` (variant 1).",
     "~~Real sections~~\n~~begin at `+0x30` (variant 0) or `+0x40` (variant 1).~~ The DWORD offset table begins at "
     "`+0x30` (variant 0) or `+0x40` (variant 1), and each real section at that position plus its dword " + C
     + "`00409780+0xD9` `lea r11, [r10 + 0x40]` and `00409780+0xE7` `lea ecx, [rax + 0x40]`, and the `+0x30` pair at "
     "`00409780+0x13E` / `00409780+0x148`)*."),
    (CSA, "Offsets are relative to the TABLE\nBASE, not to each slot.",
     "Offsets are relative to ~~the TABLE~~\n~~BASE~~ the start of that offset array (`+0x30` or `+0x40`); the offset "
     "the lookup returns adds that bias and so is table-base relative " + C + "`00409780+0xE7` "
     "`lea ecx, [rax + 0x40]` then `00409780+0xED` `add ecx, r10d` locates a section, and `00409780+0x115` "
     "`add ecx, 0x40` forms the returned offset; `00409780+0x148` / `00409780+0x170` for `+0x30`)*, not to each slot."),

    # ---- Authored data registry and row lookup ----
    # C-V23: 723 references (722 reads + 1 lea).
    (VBF, "with 720 references — the second-highest in",
     "with ~~720~~ 723 references " + C + "722 reads and one `lea` over every function body)* — the second-highest "
     "in"),
    (REG, "carries **720 references**",
     "carries ~~**720 references**~~ **723 references** " + C + "722 reads and one `lea` over every function body, "
     "the count the slot census and the upper-slot pass below give)*"),
    (REG, "| `0x02EBF138` | 720 | action definitions |",
     "| `0x02EBF138` | ~~720~~ 723 " + C + "722 reads and one `lea`)* | action definitions |"),
    # C-V24: 60-byte rows (u16 stride at header +8; battle_pack +0x3C declares 543 x 60).
    (REG, "at **720-byte rows**",
     "at ~~**720-byte rows**~~ **60-byte rows** " + C + "the stride is the header's `u16 +8`, read at "
     "`002376F0+0x73` `movzx ecx, word ptr [rax + 8]`, and the section bound there, `battle_pack.bin` directory "
     "`+0x3C`, declares 543 x 60; 720 was a reference figure, not a size)*"),
    # C-V25: 33 + 2 registrar triples in 00236C30, and 37 slot addresses in its body.
    (REG, "contains **34 `lea <slot>` / `movsxd rdx, [rax + <field>]`\n> / `call 0x003845F0` triples in a row, with 34 "
          "DISTINCT field offsets and no loop**.",
     "contains **~~34~~ 33 `lea <slot>` / `movsxd rdx, [rax + <field>]`\n> / `call 0x003845F0` triples in a row, "
     "with ~~34~~ 33 DISTINCT field offsets and no loop**, plus two `call 0x003846F0` triples " + C + "33 "
     "`call 0x3845f0` and 2 `call 0x3846f0` sites in `00236C30`, the first at `00236C30+0x56` and "
     "`00236C30+0x109`)*."),
    (REG, "It is also **not** among the 38",
     "It is also **not** among the ~~38~~ 37 " + C + "35 `lea`s and the two direct stores `00236C30+0x44` and "
     "`00236C30+0x401`)*"),
    # C-V31: 64 slots ending 0x02EBF200 (00236C30+0x401 stores it).
    (REG, "Registry            0x02EBF008 .. 0x02EBF1F8\n  slot[i]  = *(void **)(0x02EBF008 + i * 8)        i = 0 .. "
          "62\n",
     "Registry            0x02EBF008 .. 0x02EBF1F8   <- corrected 2026-10-02, OPUS: .. 0x02EBF200, 64 slots "
     "(00236C30+0x401 stores 0x02EBF200)\n  slot[i]  = *(void **)(0x02EBF008 + i * 8)        i = 0 .. 62   <- "
     "corrected 2026-10-02, OPUS: i = 0 .. 63\n"),
    (REG, "> fields; the band is 63 separately-named globals that happen to be adjacent.",
     "> fields; the band is ~~63~~ 64 separately-named globals that happen to be adjacent " + C + "`0x02EBF008`–"
     "`0x02EBF200`, the extent §2 corrected)*."),
    (RM, "**Every authored number in FFXII is reached through one 63-slot pointer\n  array**",
     "**Every authored number in FFXII is reached through one ~~63-slot~~ 64-slot pointer\n  array** " + C
     + "`0x02EBF008`–`0x02EBF200`; `00236C30+0x401` stores the last slot)*"),
    # C-V33: the canonical lookup is not fail-closed.
    (REG, "- **Bounds are fail-closed.** An out-of-range index returns a miss, not garbage.",
     "- **Bounds are ~~fail-closed~~ per consumer.** ~~An out-of-range index returns a miss, not garbage.~~ The "
     "canonical row lookup tests neither the index nor a null table, and reads a null table at a near-null address; "
     "only the consumers that compare the index with the `+0x04` count fail closed " + C + "`003876D0` multiplies the "
     "index at `003876D0+0x3B` with no compare, and on a null slot `003876D0+0x42` `xor ecx, ecx` is followed by "
     "`003876D0+0x44` `movzx eax, byte ptr [rcx + 9]`; the row-lookup contract §10)*."),
    # C-V35: the twelve board slots are pointers.
    (REG, "— corrected 2026-09-11: the completion words of the twelve board requests (*the tail read*, below) |",
     "— corrected 2026-09-11: ~~the completion words of~~ the loaded-board pointers of the twelve board requests "
     "(*the tail read*, below) " + C + "the setters store the buffer address `00384420+0x99` puts in the descriptor's "
     "`+8`)* |"),
    (REG, "**`02EBF1A0`–`02EBF1F8` — the completion words of twelve board requests**",
     "**`02EBF1A0`–`02EBF1F8` — ~~the completion words of~~ the loaded-board pointers of twelve board requests** "
     + C + "`00384420+0x99` writes the buffer address into the descriptor's `+8`; the 2026-09-30 correction "
     "below)*"),
    # C-V36: 0x02EBF198 (and its neighbours) are BSS.
    (REG, "the slot is *initialised in the image* (`0x009224A8`, a pointer into the\n      static region)",
     "the slot is ~~*initialised in the image* (`0x009224A8`, a pointer into the~~\n      ~~static region)~~ BSS, "
     "zero at load " + C + "`0x02EBF198` lies " + BSS + "; AG-4's answer above)*"),
    (REG, "| `0x02EBF198` | 0 | **Initialised but never named** — disposition below | n/a |",
     "| `0x02EBF198` | 0 | **~~Initialised but~~ BSS and never named** " + C + BSS + ")* — disposition below | n/a |"),
    (REG, "read (the image-initial values below are already pointers), or",
     "read ~~(the image-initial values below are already pointers)~~ (the slots are BSS, zero at load " + C
     + "`0x02EBF1A0`–`0x02EBF1F8` lie " + BSS + ")*), or"),
    (REG, "Allocated and initialised, never named",
     "Allocated ~~and initialised~~ in BSS " + C + "zero at load, " + BSS + ")*, never named"),
    (REG, "- **Initialised in the image.** The `.data` bytes hold `0x009224A8` — a non-zero pointer into the\n"
          "  image's static region, of the same shape as its fifteen neighbours (each holds a distinct\n"
          "  pointer-like initial value, e.g. `0x1A0` → `0x009234D8`). It is not reserved padding and it is not\n"
          "  BSS.",
     "- **~~Initialised in the image.~~ BSS.** ~~The `.data` bytes hold `0x009224A8` — a non-zero pointer into the~~\n"
     "  ~~image's static region, of the same shape as its fifteen neighbours (each holds a distinct~~\n"
     "  ~~pointer-like initial value, e.g. `0x1A0` → `0x009234D8`). It is not reserved padding and it is not~~\n"
     "  ~~BSS.~~ The slot and its fifteen neighbours lie " + BSS + ", so all are zero at load; `0x009224A8` is a "
     "path string's address, not this slot's value " + C + "the section table gives `.data` a raw size of "
     "`0x18E400` from `0x01DF0000`; AG-4's answer in §7)*."),
    (REG, "- **Bounded claim.** The slot is populated at image load and consultable",
     "- **Bounded claim.** The slot is ~~populated at image load~~ zero at load (BSS) " + C + BSS + ")* and "
     "consultable"),
    # C-V37: class 13 sums four row counts (02EBF078 at 00322C50+0x21E).
    (REG, "| 13 | `02EBF090` **+ `02EBF088` + `02EBF080`** |",
     "| 13 | `02EBF090` **+ `02EBF088` + `02EBF080` + `02EBF078`** " + C + "`00322C50+0x21E` reads the fourth)* |"),
    (REG, "it reads three\nslots and a `0x8000` constant",
     "it reads ~~three~~ four\nslots " + C + "`02EBF078` too, read at `00322C50+0x21E` and summed at "
     "`00322C50+0x22D`)* and a `0x8000` constant"),
    (REG, "`02EBF078` `s_daiji_data` (empty), `02EBF048`",
     "`02EBF078` `s_daiji_data` (empty) " + C + "it is class 13's fourth table, read at `00322C50+0x21E`)*, "
     "`02EBF048`"),
    # C-V38: twelve setters (00238390 for 0x02EBF1A0).
    (REG, "| `002383C0`–`002385A0` | 11 generated 39-byte slot setters, `0x30` apart | ✅ read |",
     "| ~~`002383C0`~~ `00238390`–`002385A0` | ~~11~~ 12 generated 39-byte slot setters, `0x30` apart " + C
     + "`00238260+0x1D` names `00238390`, the setter for `0x02EBF1A0`, ahead of `002383C0`)* | ✅ read |"),
    (REG, "Eleven consecutive slots - `0x02EBF1A8` through `0x02EBF1F8` - each have a **39-byte** consumer, and\n"
          "those consumers sit at `0x002383C0`,",
     "~~Eleven~~ Twelve consecutive slots - ~~`0x02EBF1A8`~~ `0x02EBF1A0` through `0x02EBF1F8` - each have a "
     "**39-byte** consumer " + C + SETTER + "; §5 of the AG-2 ruling below)*, and\nthose consumers sit at "
     "`0x00238390`, `0x002383C0`,"),
    (REG, "> **But `each has its own generated setter` is true of 11 slots out of 63**",
     "> **But `each has its own generated setter` is true of ~~11 slots out of 63~~ 12 slots out of 64** " + C
     + "setters `00238390`–`002385A0`, and `00236C30+0x401` stores the 64th slot `0x02EBF200`)*"),
    (REG, "> **What survives:** eleven slots have generated setters; those eleven are mutable",
     "> **What survives:** ~~eleven~~ twelve slots have generated setters " + C + "`00238390` is the twelfth, for "
     "`0x02EBF1A0`)*; those ~~eleven~~ twelve are mutable"),
    (REG, "**Established, restated with its scope:** *eleven* slots (`0x02EBF1A8`–`0x02EBF1F8`) each have a",
     "**Established, restated with its scope:** ~~*eleven* slots (`0x02EBF1A8`–`0x02EBF1F8`)~~ *twelve* slots "
     "(`0x02EBF1A0`–`0x02EBF1F8`) " + C + SETTER + ")* each have a"),
    (REG, "> eleven setter slots (`0x02EBF1A8`–`0x1F8`) are bound",
     "> ~~eleven~~ twelve setter slots (~~`0x02EBF1A8`–`0x1F8`~~ `0x02EBF1A0`–`0x1F8`) " + C + SETTER + ")* are "
     "bound"),
    # C-V41: the grouped table's count is the first dword of the +0x1C list.
    (REG, "if ((unsigned)group > *(uint32_t *)hdr - 1) return 0;        /* 0032A26D: the count is at +0x00 */\n",
     "if ((unsigned)group > *(uint32_t *)hdr - 1) return 0;        /* 0032A26D: the count is at +0x00 */   /* <- "
     "corrected 2026-10-02, OPUS: the count is the first dword of the +0x1C list, *(uint32_t *)idx_list "
     "(0032A230+0x2A mov ecx, dword ptr [rax + 0x1c]; 0032A230+0x3D mov eax, dword ptr [rax] on the 0020E600 "
     "result) */\n"),
    (REG, "**Its count lives at `+0x00`,\nnot at `+0x04`**",
     "**Its count lives at ~~`+0x00`,~~ `+0x00` of the `+0x1C` group list,\nnot at `+0x04`** " + C + "`0032A230+0x2A` "
     "`mov ecx, dword ptr [rax + 0x1c]` and `0032A230+0x3D` `mov eax, dword ptr [rax]` on `0020E600`'s result; the "
     "header's own `+0x00` is the `st2e` magic)*"),
    # C-V42: Row(i) returns the row's leading dword.
    (REG, "and returns `rows + *(uint16_t *)(hdr + 8) * i` |",
     "and returns ~~`rows + *(uint16_t *)(hdr + 8) * i`~~ the row's leading dword, "
     "`*(u32 *)(rows + *(u16 *)(hdr + 8) * i)` " + C + "`00320B30+0x58` `mov eax, dword ptr [rax]`, as the subtree "
     "table below says)* |"),
    # C-V43: state 3 loops to 1; state 4 exits.
    (REG, "state `3` exits - the `4`-write and `0`/`1` return encode done vs still-pumping",
     "state `3` ~~exits~~ loops back to state `1` and state `4` exits " + C + "`0037C2E0+0x29` `mov ebx, 1` loops "
     "for state 3; state 4 reaches `0037C2E0+0xBC`, stores 4 and returns 0)* - the `4`-write and `0`/`1` return "
     "encode done vs still-pumping"),
    # C-V111: five .ard categories.
    (REG, "**Four `.ard` section categories** (`0`, `1`, `2`, `3`) are dispatched explicitly",
     "**~~Four~~ Five `.ard` section categories** (`0`, `1`, `2`, `3`, `4`) " + C + "`0023A160` dispatches "
     "categories 0 to 4, and category 4 binds `02EBF140` at `0023A160+0x18`; the audit note in §2)* are dispatched "
     "explicitly"),
    # C-V112: 00236C30 fills four slots without 003845F0.
    (REG, "the only slot it fills without\n`AreaData_BindAndRebaseSectionDescriptor`;",
     "~~the only slot it fills without~~\n"
     "~~`AreaData_BindAndRebaseSectionDescriptor`~~ one of four slots it fills without "
     "`AreaData_BindAndRebaseSectionDescriptor` - `0x02EBF200` is stored the same way, and `02EBF160` / `02EBF170` "
     "go through `003846F0` " + C + "`00236C30+0x401` stores `0x02EBF200`; `00236C30+0x109` and `00236C30+0x3BA` "
     "call `003846F0`)*;"),

    # ---- ROW (held: OPUS's own uncommitted interior-citation section) ----
    # C-V32: the census band is not the registry array.
    (ROW, "The registry is a band of qword slots at `02EBEF70..02EBF3FC`, 8 bytes apart. **Forty of them are",
     "~~The registry is a band of qword slots at `02EBEF70..02EBF3FC`, 8 bytes apart.~~ The census band is "
     "`02EBEF70..02EBF3FC`, 8 bytes apart; the registry array inside it is `02EBF008`–`02EBF200`, and the band also "
     "holds other globals " + C + "`00236C30+0x3E0` binds `02EBF008` and `00236C30+0x401` stores `02EBF200`; "
     "`02EBF000` is a float that `0039AF20+0x7` stores with `movss`, and `02EBEF78` is the EFX rebase table "
     "`003A9BA0+0x20` loads)*. **Forty of them are"),
    # C-V26: the jmp sweep finds six tail-jump sites of 003845F0 and one of 003846F0.
    (ROW, "finds exactly one tail-jump binder image-wide, this.",
     "finds ~~exactly one tail-jump binder image-wide, this~~ six tail-jump sites: this one, `00238640` (into "
     "`02F973C0`, outside the registry) and four in `0023A160` (the `.ard` slots `02EBF120`/`140`/`148`/`150`), "
     "plus a seventh in `0023A160` that jumps to `003846F0` for `02EBF168` " + C + TAILS + ")*."),
    # C-V113 + C-V30 + C-V26: five inner binders; only 02EBF000 and 02EBF0D0 lack binder provenance.
    (ROW, "Six more calls consume the blob whole; three of them are\n"
          "   inner binders that fill four additional slots — `00237FC0`→`02EBF138`,\n"
          "   `00238160`→`02EBF0F8`, `00238880` (`GambitTargetDefinition_BindAndBuildMenuLookup`, fed\n"
          "   `blob+0x20`)→`02EBF0D8`, and `00238660`→`02EBF158`. **39 of the 47 slots' provenance is\n"
          "   thus named.**\n"
          "   The remaining eight — `02EBF000`, `02EBF0D0`, `02EBF118`, `02EBF120`, `02EBF140`,\n"
          "   `02EBF148`, `02EBF150`, `02EBF168` — have **no binder-family provenance**: the\n"
          "   `003845F0`/`003846F0` caller census is complete (36 and 5 sites, all enumerated above or\n"
          "   internal),",
     "Six more calls consume the blob whole; ~~three of them are~~ five of them are\n"
     "   inner binders that fill ~~four~~ five additional slots — `00237FC0`→`02EBF138`,\n"
     "   `00238160`→`02EBF0F8`, `00238880` (`GambitTargetDefinition_BindAndBuildMenuLookup`, fed\n"
     "   `blob+0x20`)→`02EBF0D8`, ~~and~~ `00238660`→`02EBF158` and `003847B0`→`02EBF118` " + C + "`00236C30+0x164` "
     "calls `003847B0` with `blob+0x40`, and `003847B0+0x3` names `02EBF118` before its `jmp 0x3845f0`)*. "
     "**~~39~~ 40 of the 47 slots' provenance is\n"
     "   thus named.**\n"
     "   The remaining ~~eight — `02EBF000`, `02EBF0D0`, `02EBF118`, `02EBF120`, `02EBF140`,~~ seven split: the five "
     "`.ard` slots `02EBF150`, `02EBF168`, `02EBF120`, `02EBF148` and `02EBF140` are bound by the dispatcher "
     "`0023A160` through tail-jumps, and only `02EBF000` and `02EBF0D0`\n"
     "   ~~`02EBF148`, `02EBF150`, `02EBF168` —~~ have **no binder-family provenance** " + C + TAILS + ")*: the\n"
     "   `003845F0`/`003846F0` caller census is complete ~~(36 and 5 sites, all enumerated above or~~ for `call` "
     "(36 and 5 sites), and the tail-jumps add six and one,\n"
     "   ~~internal)~~,"),
    # C-V114: 00324510 stores 02EBF178 twice.
    (ROW, "capstone pass over every function; the only stores in the band are `00238660`'s `02EBF158`\n"
          "   > and `0039AF20`'s float block)",
     "capstone pass over every function; ~~the only stores in the band are~~ the stores in the band are "
     "`00238660`'s `02EBF158`\n   > and `0039AF20`'s float block, and `00324510`'s two at `02EBF178` " + C
     + "`00324510+0x48` and `00324510+0x18A` store `rax` there)*)"),
    # C-V29: 00236C30 is tail-jumped to by the registered stub 00238850.
    (ROW, "`00236C30` is not called by anyone: it is the **delivery",
     "`00236C30` is ~~not called by anyone: it is~~ tail-jumped to by the registered stub `00238850` " + C
     + "`00238850+0x1F` `jmp 0x236c30` with `ecx = 1`; the call at `002368D0+0xFE` registers `00238850`, whose "
     "address `002368D0+0xF7` loads)*, the body of the **delivery"),
    (ROW, "`003843F0` → `00384420(0x13, 00236C30, \"STATIC\", 4, 6, 4)`, the",
     "`003843F0` → ~~`00384420(0x13, 00236C30, \"STATIC\", 4, 6, 4)`~~ `00384420(0x13, 00238850, \"STATIC\", 4, 6, 4)` "
     + C + "`002368D0+0xF7` loads `00238850` into `rdx`)*, the"),
    # C-V34: the codec pair round-trips exactly while (p - base) mod 2^64 < 2^32.
    (ROW, "| the encoder subtracts the same global read as a DWORD, so the two are inverses only below 4 GB | `0020E620` "
          "whole. Executed in both directions at a base of `0x100000000`, where the round trip does not return the "
          "reference |",
     "| the encoder subtracts the same global read as a DWORD, so the two are inverses ~~only below 4 GB~~ exactly "
     "while `(p - base) mod 2^64 < 2^32`, whatever the base's high half " + C + CODEC + "; the next row's ruling)* | "
     "`0020E620` whole. Executed in both directions at a base of `0x100000000`, ~~where the round trip does not "
     "return the reference~~ where a reference below `2^32` comes back unchanged by that algebra |"),
    (ROW, "the pair round-trips only while the base's high half is zero and the delta fits 32 bits — the",
     "the pair round-trips ~~only while the base's high half is zero and the delta fits 32 bits~~ exactly while "
     "`(p - base) mod 2^64 < 2^32`, whatever the base's high half " + C + CODEC + ")* — the"),
    # C-V26 + C-V113 in the evidence table.
    (ROW, "| the STATIC delivery populates 39 of the 47 band slots,",
     "| the STATIC delivery populates ~~39~~ 40 " + C + "`003847B0`→`02EBF118` is the fifth inner binder, "
     "`00236C30+0x164`)* of the 47 band slots,"),
    (ROW, "+ four inner-binder slots (`00237FC0`→`02EBF138`, `00238160`→`02EBF0F8`, `00238880`→`02EBF0D8`, "
          "`00238660`→`02EBF158`). Binder caller census complete: 36 `003845F0` + 5 `003846F0` sites |",
     "+ ~~four~~ five inner-binder slots (`00237FC0`→`02EBF138`, `00238160`→`02EBF0F8`, `00238880`→`02EBF0D8`, "
     "`00238660`→`02EBF158`, `003847B0`→`02EBF118`). Binder caller census ~~complete: 36 `003845F0` + 5 `003846F0` "
     "sites~~: 36 `call` and 6 `jmp` sites of `003845F0`, 5 `call` and 1 `jmp` of `003846F0` " + C + TAILS + ")* |"),
    # C-V62: 0036BC60 is 887 B.
    (ROW, "`0036BC60` (~179 B) —",
     "`0036BC60` ~~(~179 B)~~ (887 B) " + C + "the body runs 887 bytes from `0036BC60`)* —"),
    # C-V110: 0036C660 tags a block header; it does not rebase.
    (ROW, "the row fetch `0036A190` and the rebase `0036C660`.",
     "the row fetch `0036A190` and ~~the rebase~~ the header tagger `0036C660` " + C + "`0036C660+0x1A` checks the "
     "`0xFF12` block magic at payload `-0x40`, `0036C660+0x30` `strncpy`s seven name bytes into payload `-0xC` and "
     "`0036C660+0x40` stores the tag word at `-0x22`; nothing is rebased)*."),

    # ---- Archive, st2e, battle_pack, text ----
    # C-V20: count + 72 four-byte offsets, table end 0x124 (003846F0 walks count + 1 entries from +4).
    (VBF, "`battle_pack.bin` opens with `{u32 count = 71; u32 offset[71]}`",
     "`battle_pack.bin` opens with ~~`{u32 count = 71; u32 offset[71]}`~~ `{u32 count = 71; u32 offset[72]}`, the "
     "last an end sentinel " + C + DIR72 + ")*"),
    (S2R, "table ending `0x120` and first payload at `0x128`.",
     "table ending ~~`0x120`~~ `0x124` (the count and 72 four-byte offsets) and first payload at `0x128` " + C
     + DIR72 + ")*."),
    (S2R, "> 8-byte entries, and 29 of its 71 slots aliased** —",
     "> ~~8-byte entries~~ 4-byte entries, and 29 of its 71 slots aliased** " + C + "the binder steps 4 bytes, "
     "`003846F0+0x97` `add rbx, 4`)* —"),
    # C-V21: word.bin is {u32 count; u32 offsets[count+1]} (003846F0 rebases 16 words from +4 for slot 02EBF170).
    (VBF, "`{u32 count = 15; u32 headerSize = 68; u32 blockOffsets[15]}`, each block",
     "~~`{u32 count = 15; u32 headerSize = 68; u32 blockOffsets[15]}`~~ `{u32 count = 15; u32 offsets[16]}`, "
     "`offsets[0]` = 68 being block 0's start and `offsets[15]` the end " + C + "the binder `003846F0` rebases "
     "count + 1 words from `+4` (`003846F0+0x56`, `003846F0+0x9B` / `003846F0+0x9E`) for slot `02EBF170`, called at "
     "`00236C30+0x3BA`; AY-4 above)*, each block"),
    # C-V22: the 63-entry command block is block 4, 0-based.
    (VBF, "**Block 3, 63 entries — the player's battle command list**, decoded from the bytes:",
     "**Block ~~3~~ 4, 63 entries — the player's battle command list** " + C + "0-based, `offsets[4]` = 35,444 in "
     "`us`; the binder `003846F0` rebases all sixteen words from `+4`, and the struck `headerSize` reading numbered "
     "it 3)*, decoded from the bytes:"),
    (VBF, "the same order as `word.bin` block 3 entries 18–22",
     "the same order as `word.bin` block ~~3~~ 4 " + C + "0-based, as corrected above)* entries 18–22"),
    (BTB, "(the same 63 entries as `word.bin` block 3) |",
     "(the same 63 entries as `word.bin` block ~~3~~ 4 " + C + "`offsets[4]` of `word.bin`, 0-based as `003846F0` "
     "walks them; it was block 3 only under the struck `headerSize` reading)*) |"),
    # C-V115: the heap offset rule fails for the two mons_act.bin (headerSize 0, heap 0x20).
    (VBF, "(`== headerSize + count*recordSize`), which separates the",
     "(~~`== headerSize + count*recordSize`~~ `headerSize + count*recordSize` in 255 files, but `0x20` in the two "
     "`mons_act.bin`, whose `headerSize` and `recordSize` are 0 " + C + "the shipped headers, `headerSize` 32 in 393 "
     "of 407; §2's corrected struct)*), which separates the"),
    (VBF, "    u32  headerSize; /* 32 */         u32 count;\n",
     "    u32  headerSize; /* 32 */         u32 count;   /* <- corrected 2026-10-02, OPUS: headerSize is 32 in 393 of "
     "407 and 0 in 14; the two mons_act.bin keep heapOffset 0x20 with headerSize 0 */\n"),
    # C-V116: 001F4720 is the digest-tree insert; 001F3FD0's [rdx+0x18] is the key.
    (BIG, "parent walk `[rdx+0x18]` (",
     "~~parent walk `[rdx+0x18]`~~ the key walk, `[rdx+0x18]` being the new node's key half " + C + "`001F3FD0+0x2D` "
     "`mov rdx, qword ptr [rdx + 0x18]` loads the inserted key and `001F3FD0+0x38` compares it with each node's "
     "`[r8 + 0x18]`)* ("),
    (BIG, "| `001F4720` (176 B) | index-record accessor — `rbx = [rcx+0x30]`, `edx = dword[rcx+0x4C]` (",
     "| `001F4720` (176 B) | ~~index-record accessor~~ the digest-tree insert: it pops a node from the free list "
     "`rbx = [rcx+0x30]` (refilled through `00680150` with `edx = dword[rcx+0x4C]`), copies the key to `+0x18` and "
     "the record pointer to `+0x28`, and calls `001F3FD0` " + C + "`001F4720+0x5E` "
     "`movups xmmword ptr [rbx + 0x18], xmm0`, `001F4720+0x65` `mov qword ptr [rbx + 0x28], rax` and "
     "`001F4720+0x6F` `call 0x1f3fd0`; the opener calls it per record at `001F4340+0x337`)* ("),
    # C-V117: the resolver's offsets are relative to this + 0x20.
    (PATH, "The resolver stores a source in only `+0x20` (route 1) and `+0x10` (route 2), never the `+8` handle;",
     "The resolver stores a source in only ~~`+0x20` (route 1) and `+0x10` (route 2), never the `+8` handle~~ the "
     "stream's `+0x40` (route 1) and `+0x30` (route 2), never the `+0x28` handle - `+0x20`, `+0x10` and `+8` of the "
     "frame it is handed, `this + 0x20` " + C + "`0059ED70+0x20` `add rcx, 0x20` before the call; the resolver "
     "stores at `0059EE90+0x15A` `[r15 + 0x20]` and `0059EE90+0x307` `[r15 + 0x10]`, and IsOpen `0059D920` tests the "
     "stream's `+0x28`, `+0x30` and `+0x40`)*;"),
    (PATH, "the selector byte `+0x18`\n  decides three things.",
     "the selector byte `+0x18` " + C + "of the resolver's frame `this + 0x20`, so the stream's `+0x38`; "
     "`0059EE90+0x66` `movzx ecx, byte ptr [r15 + 0x18]`)*\n  decides three things."),
]


# Pass-22 neighbours (2026-10-02, OPUS): functions of other layers are named by role in NEW text, so the page
# takes on no unaccounted crossing (check_publish_neighbours.py refused the address form).
ROLE_NAMES = [
    ('`00236C30+0x401` stores the last slot',
     'the registry builder stores the last slot at its `+0x401`'),
    ('`003846F0+0x56` `lea rbx, [r9 + 4]`, `003846F0+0x97` `add rbx, 4`, over count + 1 entries to `003846F0+0x9B` `cmp rdi, rax` and the `jle` at `003846F0+0x9E`',
     "the binder's `+0x56` `lea rbx, [r9 + 4]` and `+0x97` `add rbx, 4`, over count + 1 entries to its `+0x9B` `cmp rdi, rax` and the `jle` at its `+0x9E`"),
    ('the binder steps 4 bytes, `003846F0+0x97` `add rbx, 4`',
     'the binder steps 4 bytes, its `+0x97` `add rbx, 4`'),
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
