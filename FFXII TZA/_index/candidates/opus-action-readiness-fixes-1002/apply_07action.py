"""apply_07action.py [--apply] - 07-Combat-Action readiness map (cloud-reports/re-readiness/07-action.md), section 2.4
contradictions A1-A17 and B1-B9 checked at the bytes, plus the map's stale (C) and banner (D) items (OPUS, 2026-10-02).

The map was written from a text snapshot without the executable, so each value item was re-decided at the shipping
image (retool.py) before an edit was drafted; verdicts in the OPUS scratch file verdicts-07.md.
Each edit strikes the DISFAVOURED side only (the side the image refutes) and restates it, tagged
*(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
A4 favours neither page whole: both tables are real (CB-5), but the party table's index is the stats record's byte +4,
not "kind"; every "kind * 0x40" is struck. B4 favours neither count: 3 battle-unit writers plus at least 8 others.
Left out: B6 and B9 (no contradiction - different scopes / the fan-out issuer's callers), B7 and B8 (member-TSV
bookkeeping, not bytes), D4 (the two "pending first review" notes sit inside YAML front-matter scalars), D5 (flags).
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines get a trailing `# <- corrected` comment instead of a strike (their OLD includes the line end, so NEW
never contains OLD). No front-matter edits; the one heading change (C5) names OPUS.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "07-Combat-Action/"
RM = F + "README.md"
TM = F + "the-moment-an-action-is-committed.md"
CCA = F + "CONTRACT-commit-action.md"
CTM = F + "CONTRACT-the-moment-an-action-is-committed.md"
NS = F + "Command-And-Action-Seam/native-command-seam.md"
CNS = F + "CONTRACT-native-command-seam.md"
HT = F + "Action-Dispatch/battle-action-handler-table.md"
CHT = F + "CONTRACT-battle-action-handler-table.md"
AV = F + "Action-Availability/battle-command-availability-and-reason-codes.md"
DR = F + "Action-Definition-Row/the-action-definition-row.md"
HG = F + "how-an-action-gathers-its-targets.md"
HCL = F + "how-close-a-unit-must-stand-to-act.md"
HC = F + "how-a-combo-continues-and-what-it-blocks.md"
CCC = F + "CONTRACT-combo-continuation.md"
TB = F + "CONTRACT-battle-target-buffer.md"
RR = F + "Result-Record/the-result-record-field-map.md"
AP = F + "applying-a-result-to-a-target.md"
PR = F + "Post-Result-Events/the-post-result-events-and-the-battle-message-table.md"

EDITS = [
    # A1: the reproduction formula - the reset is band one only (0030F7A5 ja 0030F7D9 -> 0030F7F2), +0x770 is the latch
    #     (the kind byte is [+0x698]+5, 0030F83A-0030F841), and the +0x6B0 copy and the walk are missing.
    (CCA, "    resetTargetBuffer(actor)                                  /* 00316CF0 */\n",
     "    resetTargetBuffer(actor)                                  /* 00316CF0 */   # <- corrected 2026-10-02, OPUS - "
     "band one only (id <= 0x21E); 0030F7A5 ja 0030F7D9 takes band two to 0030F7F2, past this reset and the append at "
     "0030F7CD\n"),
    (CCA, "    consult actor+0x770 (stats kind byte) and actor+0x744 (last cancelled id)\n",
     "    consult actor+0x770 (stats kind byte) and actor+0x744 (last cancelled id)   # <- corrected 2026-10-02, OPUS - "
     "+0x770 is the re-commit latch, not the stats kind byte; the kind byte is [+0x698]+5 (0030F83A-0030F841) and the "
     "latch also compares +0x740 (0030F857). Missing here - the +0x6B0 bit-1 copy of 022C1DB8[slot*12] to +0x6B9 with "
     "+0x6B6 = 1 (0030F865-0030F894), the +0x750 clear (0030F89B-0030F8A3) and the band-one propagation walk "
     "(0030F8BC-0030F931)\n"),
    (CCA, "    updateAttackerMask(target)                                /* §6 */\n",
     "    updateAttackerMask(target)                                /* §6 */   # <- corrected 2026-10-02, OPUS - band one "
     "with a resolved target only; 0030F8A9 je 0030F97A and 0030F8B6 ja 0030F97A skip the mask block 0030F937-0030F975\n"),

    # A2: a band-two commit skips the mask - 0030F8B2 cmp di, r13w / 0030F8B6 ja 0030F97A (mov eax, 1), past the mask
    #     block 0030F937-0030F975; no target unit skips it too (0030F8A9). The-moment's "JA refuses" is wrong as well.
    (CCA, "8. update the target's attacker mask, if it is not already set, and return 1",
     "8. **band one, with a resolved target, only:** update the target's attacker mask, if it is not already set; "
     "~~and return 1~~ every accepted commit returns 1 at `0030F97A` *(corrected 2026-10-02, OPUS: `0030F8A9 je "
     "0030F97A` (no target unit) and `0030F8B6 ja 0030F97A` (band two) jump past the mask block "
     "`0030F937`–`0030F975`)*"),
    (CCA, "so a band-two commit writes the block, settles `+0x770`, and goes straight to the mask.",
     "so a band-two commit writes the block, settles `+0x770`, ~~and goes straight to the mask.~~ re-picks the "
     "`+0x6B0` bit-1 slot and returns 1 **without** the mask *(corrected 2026-10-02, OPUS: `0030F8B6 ja 0030F97A` also "
     "jumps past the mask block `0030F937`–`0030F975`, and `0030F97A` is `mov eax, 1`)*."),
    (TM, "0030F8B6  ja   0030F97A\n",
     "0030F8B6  ja   0030F97A   # <- corrected 2026-10-02, OPUS - this ja accepts, it does not refuse; 0030F97A is mov "
     "eax, 1 (committed). It skips the propagation walk and the attacker mask for ids above 0x21E (band two); the "
     "refusal is 0030F7EC ja 0030F981\n"),

    # A3: the +0x770 latch - kind 1 keeps it whatever is committed (0030F849 cmp ecx, 1 / 0030F85D je 0030F865); the
    #     id/target compare (0030F84E, 0030F857) applies to kind 0 only; anything else clears it (0030F85F).
    (TM, "action id and target — a re-issued action that matches what was just cancelled keeps `+0x770`,\n"
         "any other clears it (`0030F85F`).",
     "action id and target — ~~a re-issued action that matches what was just cancelled keeps `+0x770`,~~\n"
     "~~any other clears it~~ for a unit whose stats kind byte `[+0x698]+5` is 0, a re-issued action that matches what "
     "was just cancelled keeps a non-zero `+0x770`; a kind-1 unit keeps it whatever it commits, and any other "
     "combination clears it (`0030F85F`) *(corrected 2026-10-02, OPUS: `0030F841` loads the kind byte, `0030F849 cmp "
     "ecx, 1` and `0030F85D je 0030F865` keep the latch for kind 1 without the id and target compares; "
     "CONTRACT-commit-action.md §13a)*."),
    (TM, "4. A queued repeat is dropped if the action or the target has changed — compared against",
     "4. A queued repeat is dropped if the action or the target has changed *(for a stats kind-0 unit; kind 1 keeps it "
     "whatever changed, and any other kind drops it — corrected 2026-10-02, OPUS: `0030F841`–`0030F85F`)* — compared "
     "against"),

    # A4: the party table's index is the stats record's byte +4 (003886A7), taken only when stats[+5] == 0
    #     (0038869F-003886A5); otherwise 0208DE80 + unit[+0xEA9] * 0x40 (003886CF-003886E1).
    (HC, "`rdi` is the 64-byte record (`0208D480 + kind * 0x40`),",
     "`rdi` is the 64-byte record (~~`0208D480 + kind * 0x40`~~ `0208D480 + stats[+4] × 0x40` when the stats kind byte "
     "`+5` is 0, else `0208DE80 + unit[+0xEA9] × 0x40` *(corrected 2026-10-02, OPUS: `0038869F`–`003886B6` and "
     "`003886CF`–`003886E1`)*),"),
    (HC, "| `0208D480` | 64-byte per-kind record table | `003886AB` |",
     "| `0208D480` | 64-byte ~~per-kind~~ record table for a stats kind-0 (party) record, indexed by the stats record's "
     "byte `+4` *(corrected 2026-10-02, OPUS: `003886A7 movzx edi, byte ptr [rsi + 4]`, taken only when `[rsi+5]` is 0 "
     "at `0038869F`–`003886A5`)* | `003886AB` |"),
    (HC, "003886A7  movzx edi, byte ptr [rsi + 4]       ; \\  rdi = 0208D480 + kind*0x40\n",
     "003886A7  movzx edi, byte ptr [rsi + 4]       ; \\  rdi = 0208D480 + kind*0x40   # <- corrected 2026-10-02, OPUS - "
     "the index is the stats record's byte +4, not its kind; this arm runs only when stats[+5] == 0 "
     "(0038869F-003886A5), otherwise rdi = 0208DE80 + unit[+0xEA9]*0x40 (003886CF-003886E1)\n"),
    (HC, "- **The combo length lives in the high nibble of `0208D480 + kind * 0x40 + 0x12`** and is rewritten",
     "- **The combo length lives in the high nibble of ~~`0208D480 + kind * 0x40 + 0x12`~~ `+0x12` of the 64-byte "
     "record** — `0208D480 + stats[+4] × 0x40` for a kind-0 (party) stats record, `0208DE80 + unit[+0xEA9] × 0x40` "
     "otherwise *(corrected 2026-10-02, OPUS: `0038869F`–`003886E1`)* — and is rewritten"),
    (CCC, "per-kind record   0208D480 + kind * 0x40\n",
     "per-kind record   0208D480 + kind * 0x40   # <- corrected 2026-10-02, OPUS - the index is the stats record's byte "
     "+4 (003886A7), and only for a kind-0 stats record (0038869F-003886A5); otherwise 0208DE80 + unit[+0xEA9]*0x40 "
     "(003886CF-003886E1)\n"),
    (CCC, "per-kind record** at `0208D480 + kind * 0x40` *(for a party record only;",
     "per-kind record** at ~~`0208D480 + kind * 0x40`~~ `0208D480 + stats[+4] × 0x40` *(corrected 2026-10-02, OPUS: "
     "the index is `003886A7 movzx edi, byte ptr [rsi + 4]`, not the kind byte `+5`, which only selects the table at "
     "`0038869F`–`003886A5`)* *(for a party record only;"),

    # A5: the first hit draws once (003886FD; a failed gate 0038871D jbe 0038887E ends it) or twelve times (the 11-pass
    #     loop 003887DA-00388807 around 003887E3).
    (CCC, "**CB-3 — The roll happens ONCE PER COMBO, on the first hit, and the first hit draws the generator\n"
          "TWICE.**",
     "**CB-3 — The roll happens ONCE PER COMBO, on the first hit, and the first hit draws the generator\n"
     "~~TWICE.~~ once or twelve times.** *(corrected 2026-10-02, OPUS: one draw at `003886FD`; a failed gate `0038871D "
     "jbe 0038887E` stops there, a passed one runs the 11-pass loop `003887DA`–`00388807` around `003887E3`)*"),
    (CCC, "*first hit → roll twice → memoise the count → counter 0.*",
     "*first hit → roll ~~twice~~ once, or twelve times when the percent gate passes → memoise the count → counter 0.* "
     "*(corrected 2026-10-02, OPUS: `003886FD`, `0038871D`, `003887DA`–`00388807`)*"),
    (CCC, "**Not deterministic on the first hit** — two generator draws decide the count — and **fully",
     "**Not deterministic on the first hit** — ~~two generator draws decide~~ one draw, or twelve when the gate passes, "
     "decides the count *(corrected 2026-10-02, OPUS: `003886FD`, `0038871D jbe 0038887E`, the loop "
     "`003887E3`–`00388807`)* — and **fully"),
    (CCC, "Set the counter to 0 and assert `00388660` draws the generator **twice** and writes the high nibble",
     "Set the counter to 0 and assert `00388660` draws the generator ~~**twice**~~ **once** when the percent gate fails "
     "and **twelve** times when it passes *(corrected 2026-10-02, OPUS: `0038871D jbe 0038887E`, the loop "
     "`003887DA`–`00388807`)* and writes the high nibble"),
    (CCC, "`00379CD0` twice on a unit whose counter is zero (CB-3).",
     "`00379CD0` ~~twice~~ from two call sites, once or twelve times, on a unit whose counter is zero (CB-3) "
     "*(corrected 2026-10-02, OPUS: `003886FD`, and `003887E3` inside the 11-pass loop `003887DA`–`00388807`)*."),

    # A6 + A7: the pending ring is 64 entries (00313D18 and cl, 0x3f), drained up to 8 per call (00313CF7 mov edi, 8);
    #     the two drains differ (00313D31 je 00313D8E counts an unresolved entry; 00313E11 je 00313EAC stops on one).
    (NS, "advance, same resolve-then-act loop. That is exactly why",
     "advance~~, same resolve-then-act loop~~ *(corrected 2026-10-02, OPUS: the drains differ - `00313CD0` pops eight "
     "entries whatever they resolve to (`00313CF7 mov edi, 8`, `00313D31 je 00313D8E`), `00313DB0` stops at the first "
     "entry that does not resolve (`00313E11 je 00313EAC`); CONTRACT-native-command-seam.md CS-3)*. That is exactly "
     "why"),
    (NS, "| `00313CD0` is a different 8-entry queue | complete body",
     "| `00313CD0` is a different ~~8-entry queue~~ 64-entry ring drained up to 8 entries per call *(corrected "
     "2026-10-02, OPUS: `00313D18 and cl, 0x3f`, trip count `00313CF7 mov edi, 8`; section 7)* | complete body"),

    # A8 + A9: +0x01 is read at 00308813 (movzx edx, byte ptr [rsi + 1]) on a stack instance; 003014C0 keeps two
    #     stack buffers ([rsp+0x460] reset at 0030167C, [rsp+0x40] reset by 003087E0 at 0030880E).
    (TB, "`BattleTargetBuffer`, total size **0x208**, never independently allocated — it exists only inline,\n"
         "twice, inside `BattleUnit`.",
     "`BattleTargetBuffer`, total size **0x208**, ~~never independently allocated — it exists only inline,~~\n"
     "~~twice, inside `BattleUnit`.~~ inline twice inside `BattleUnit` (`+0x778`, `+0xBC0`) and also as stack locals "
     "*(corrected 2026-10-02, OPUS: `AiOrder_EvaluateAndResolveActionTarget` resets a candidate buffer at "
     "`[rsp+0x460]` (`00301674`–`0030167C call 00316CF0`) and hands `003087E0` an out buffer at `[rsp+0x40]` "
     "(`003017AF`–`003017BF`), which it resets at `0030880E`)*."),
    (TB, "3. **`+0x01` has no reader anywhere in the image, and that is now measured, not assumed**",
     "3. ~~**`+0x01` has no reader anywhere in the image, and that is now measured, not assumed**~~ **`+0x01` has a "
     "reader, on a stack instance** *(corrected 2026-10-02, OPUS: `00308813 movzx edx, byte ptr [rsi + 1]` in "
     "`003087E0`, where `rsi` is `003014C0`'s stack candidate buffer `[rsp+0x460]`; item 3 of the list verified "
     "owner-side 2026-09-22 below)*"),
    (TB, "It does not. The buffer is never\n   independently allocated, so any outside reader must reach the word "
         "through an inline base",
     "~~It does not. The buffer is never~~\n   ~~independently allocated, so any outside reader must reach the word through an "
     "inline base~~ *(corrected 2026-10-02, OPUS: stack instances exist, `[rsp+0x460]` and `[rsp+0x40]` in "
     "`003014C0`, so this scan's inline bases could not see the reader at `00308813`)*"),
    (TB, "structures. **The field stays UNRESOLVED on purpose.**",
     "structures. ~~**The field stays UNRESOLVED on purpose.**~~ *(answered: resolved, the candidate buffer's "
     "selection recipe - see item 3 of the list verified owner-side 2026-09-22 below; 2026-10-02, OPUS)*"),

    # A10: 32 parameter entries - 00384925 lea edx, [r8 + 0x21] with r8 = -1, loop 00384950-00384963.
    (RR, "- **Two 32-bit masks and two parameter arrays of 33** — the status",
     "- **Two 32-bit masks and two parameter arrays of ~~33~~ 32** *(corrected 2026-10-02, OPUS: `00384925 lea edx, "
     "[r8 + 0x21]` with `r8 = -1` sets the loop count to 32, `00384950`–`00384963`)* — the status"),
    (RM, "the two status masks with their 33-entry parameter arrays,",
     "the two status masks with their ~~33-entry~~ 32-entry parameter arrays *(corrected 2026-10-02, OPUS: `00384925 "
     "lea edx, [r8 + 0x21]`, `r8 = -1`)*,"),

    # A11: +0x3C-+0x3D two layer effects to add (00311788, loop of 2, mode 2), +0x3E-+0x41 four to clear (003117E4,
    #     loop of 4, mode 0).
    (RR, "  +0x3C  u16 + u8, +0x3E u32 + u8  statuses to remove\n",
     "  +0x3C  u16 + u8, +0x3E u32 + u8  statuses to remove   # <- corrected 2026-10-02, OPUS - six bytes, not statuses; "
     "+0x3C-+0x3D two layer effects to add (mode 2, the loop of 2 at 00311788) and +0x3E-+0x41 four to clear (mode 0, "
     "the loop of 4 at 003117E4), 0xFF = none (00384941, 00384946)\n"),
    (RR, "| the remove-status writers (`+0x3C`–`+0x3F`, timer 0) |",
     "| the ~~remove-status writers~~ layer-effect writers: `0038FF20` the two to add (`+0x3C`, `+0x3D`, timer 0), "
     "`003900C0` the first two to clear (`+0x3E`, `+0x3F`) *(corrected 2026-10-02, OPUS: the applier sends "
     "`+0x3C`–`+0x3D` in mode 2 and `+0x3E`–`+0x41` in mode 0, `00311788`–`00311819`)* |"),

    # A12: +0x38 - a dword absence test (0031148D cmp dword ptr [rbx + 0x38], -1), the low word dispatched (00311493).
    (AP, "record `+0x38` (`u16`, `-1` = none) → the same inventory add",
     "record `+0x38` (~~`u16`, `-1` = none~~ `i32`, absent when the dword is `-1`; the low word is the id) *(corrected "
     "2026-10-02, OPUS: `0031148D cmp dword ptr [rbx + 0x38], -1`, then `00311493 movzx ecx, word ptr [rbx + 0x38]`)* → "
     "the same inventory add"),

    # A13: +0x11C is one signed byte - written 003867DE (byte), read 003113CB / 003113D6 movsx; +0x11D is written at
    #     003867EB; only the initialiser's word store 0038490F spans both.
    (RR, "| `+0x11C` | 2 | u16 | **the target's new level** in the low byte (`0xFF` = none): scratch `02AEE044` "
         "(`003867DE`; the high byte keeps the initialiser's `0xFF`)",
     "| `+0x11C` | ~~2~~ 1 | ~~u16~~ s8 | **the target's new level** ~~in the low byte~~ (`0xFF` = none): scratch "
     "`02AEE044` (`003867DE` `mov byte ptr [rbx + 0x11c], al`; ~~the high byte keeps the initialiser's `0xFF`~~ the byte "
     "above is `+0x11D`, the source's level, written at `003867EB`; only the initialiser's word store `0038490F` spans "
     "both) *(corrected 2026-10-02, OPUS: the applier reads one byte and sign-extends it, `003113CB`, `003113D2 cmp al, "
     "0xff`, `003113D6 movsx edx, al`)*"),
    (RR, "  +0x1C  u8   resolved mark                        +0x11C u16, +0x11D u8\n",
     "  +0x1C  u8   resolved mark                        +0x11C u16, +0x11D u8   # <- corrected 2026-10-02, OPUS - "
     "+0x11C is one byte (s8, 0xFF = none), written at 003867DE and read at 003113CB; the word is only the "
     "initialiser's 0038490F\n"),

    # A14: the availability clear is the gate's - 0031137A call 00385BA0 runs before the kind-1 loop and ANDs the bit
    #     for every non-zero result byte (00385C17 / 00385C41 / 00385C6B); the loop's btr at 0031146C is a no-op.
    (AP, "on a hit the\n   engine clears the matching bit in `targetActor[+0x6A0][+0x14]`.",
     "~~on a hit the~~\n   ~~engine clears the matching bit in `targetActor[+0x6A0][+0x14]`.~~ the item is granted; "
     "the matching bit in `targetActor[+0x6A0][+0x14]` is already clear, because `BattleFormula_ApplyResultMetadata` "
     "cleared it for every non-zero slot byte, on any target, before this loop *(corrected 2026-10-02, OPUS: `0031137A "
     "call 00385BA0` precedes the kind-1 loop; the gate's `and` at `00385C17` / `00385C41` / `00385C6B` tests only the "
     "result byte; the loop's `btr` at `0031146C` finds the bit clear)*."),
    (AP, "then **bit *i* of the spawn record's `+0x14` is cleared** (`0031145C`–`0031146F`)",
     "then **bit *i* of the spawn record's `+0x14` is ~~cleared~~ re-cleared, a no-op** (`0031145C`–`0031146F`) "
     "*(corrected 2026-10-02, OPUS: step 1's `00385BA0`, called at `0031137A`, has already cleared that bit for every "
     "non-zero slot byte, without the kind-1 gate; CONTRACT-apply-result-to-target.md I8)*"),

    # A15: the stand window is 30 x [01DFE0B4] (00337B75 imul ecx, [01DFE0B4], 0x1e); 01DFE0B4 ships as 1, 2 at 60 fps.
    (HCL, "it **stands still** for the first 30 steps of the charge",
     "it **stands still** for the first ~~30 steps~~ `30 × [01DFE0B4]` steps of the charge, 30 at the 30 fps setting "
     "and 60 at the 60 fps one *(corrected 2026-10-02, OPUS: `00337B75 imul ecx, dword ptr [01DFE0B4], 0x1e`; "
     "`01DFE0B4` ships as 1 and the 60 fps setter stores 2 at `001EDDF2`; falsification B9)*"),

    # A16: 004697C0 posts 0x05, 0x06 or 0x07 (00469894 mov edx, 6; 0046987B-00469899 esi 1/2/3 -> 5/7/6).
    (PR, "| `004697C0` | `0x06` | \"Action interrupted. … cancels ….\" |",
     "| `004697C0` | ~~`0x06`~~ `0x05` / `0x06` / `0x07` | ~~\"Action interrupted. … cancels ….\"~~ \"Time exceeded. … "
     "cancels ….\" / \"Action interrupted. … cancels ….\" / \"Target out of range. … cancels ….\" *(corrected "
     "2026-10-02, OPUS: `00469894 mov edx, 6`, and the arm at `0046987B`–`00469899` maps `esi` 1 / 2 / 3 to `edx` 5 / 7 "
     "/ 6 before `004698A1 call 0046AB10`; the texts are rows 05-07 of battle-message-rows.tsv)* |"),

    # A17: 022C1DB8 is byte +8 of a 12-byte per-slot row at 022C1DB0 - the slot IssueCommand parks (00311DA5), copied to
    #     +0x6B9 (0030F88E) and read as a battle-stats record index (00385756 -> 00320A40); +0 / +4 hold the saved
    #     +0xDC8 / +0xE58 (00312FA0 saves, 00308270 restores). No posture.
    (CCA, "- **The posture byte is re-picked only when bit 1 of `+0x6B0` is set, and that bit is consumed**;\n"
          "  the byte comes from `022C1DB8 + slot * 12`, driven at slots 0, 1, 3 and 255.",
     "- **The ~~posture byte~~ parked slot byte `+0x6B9` is re-picked only when bit 1 of `+0x6B0` is set, and that bit "
     "is consumed**;\n"
     "  the byte comes from `022C1DB8 + slot * 12`, driven at slots 0, 1, 3 and 255 *(corrected 2026-10-02, OPUS: not a "
     "posture - `BattleUnit_IssueCommand` parks a slot byte there when its target handle is 0 (`00311D8C`–`00311DA5`), "
     "the commit copies it to `+0x6B9` and sets the count `+0x6B6` = 1 (`0030F88E`, `0030F894`), and "
     "`00385756`–`0038575D` hands it to `00320A40`, a battle-stats record index of at most `0x27`)*."),
    (CCA, "then `+0x28 = 0`, `unlink(+0x695)`, `+0x695 = 0xFF`, posture row `0x22C1DB0 + ea9*12` |",
     "then `+0x28 = 0`, `unlink(+0x695)`, `+0x695 = 0xFF`, ~~posture row~~ the per-slot save row `0x22C1DB0 + "
     "ea9*12`, restoring `+0xDC8` from its word `+0` and `+0xE58` from its dword `+4` (`003082AE`–`003082C0`; "
     "`00312FA0` saved them at `003130AB`–`003130C7`) *(corrected 2026-10-02, OPUS: no posture is read)* |"),
    (CCA, "| the posture byte is re-picked only when bit 1 of +0x6B0 is set, and that bit is consumed |",
     "| the ~~posture byte~~ parked slot byte +0x6B9 is re-picked only when bit 1 of +0x6B0 is set, and that bit is "
     "consumed *(corrected 2026-10-02, OPUS: a battle-stats record index, not a posture; `00311DA5` parks it, "
     "`00385756`–`0038575D` reads it)* |"),
    (TM, "**What this document does not claim:** what `0030AB40` classifies, what `00313B30` does with the\n"
         "enmity it is handed, what the `0x4000`–`0x4166` id block contains, or what the byte table at\n"
         "`022C1DB8` (indexed by slot × 12, read into `+0x6B9` when `+0x6B0` bit 1 is set) holds.",
     "**What this document does not claim:** ~~what `0030AB40` classifies, what `00313B30` does with the~~\n"
     "~~enmity it is handed, what the `0x4000`–`0x4166` id block contains, or what the byte table at~~\n"
     "~~`022C1DB8` (indexed by slot × 12, read into `+0x6B9` when `+0x6B0` bit 1 is set) holds.~~ *(answered: "
     "`0030AB40` in the interior citation below; `00313B30` is the notify, CONTRACT-commit-action.md §13a; the "
     "`0x4000`–`0x4166` block is the order space, Action-Dispatch/battle-action-handler-table.md; `022C1DB8` is byte "
     "`+8` of a 12-byte per-slot row at `022C1DB0`, the reserve-member slot `BattleUnit_IssueCommand` parks "
     "(`00311DA5`) and `00385756`–`0038575D` hands to `00320A40` as a battle-stats record index - "
     "Post-Result-Events/the-post-result-events-and-the-battle-message-table.md, the reserve route; 2026-10-02, OPUS)*"),

    # B1: 0030CA80 is 352 B (0030CA80-0030CBDF ret). B2: 003083B0 is 596 B (-00308603 ret). B3: 002FE910 is 52 B.
    (NS, "(`BattleAction_CheckPresentationSlotReady`, ~21 B) — arg",
     "~~(`BattleAction_CheckPresentationSlotReady`, ~21 B)~~ (`BattleAction_CheckPresentationSlotReady`, 352 B "
     "*(corrected 2026-10-02, OPUS: `0030CA80`–`0030CBDF ret`, 104 instructions, as the section on `0030CA80` above "
     "states)*) — arg"),
    (HT, "`003083B0` `BattleAction_CheckTargetEligibility` (307 B) — the",
     "`003083B0` `BattleAction_CheckTargetEligibility` (~~307 B~~ 596 B *(corrected 2026-10-02, OPUS: "
     "`003083B0`–`00308603 ret`, int3 padding to `00308610`)*) — the"),
    (HT, "`002FE910` (~55 B) — `byte[+0x6B4] == 0`",
     "`002FE910` ~~(~55 B)~~ (52 B *(corrected 2026-10-02, OPUS: `002FE910`–`002FE943 ret`, as the handler table in "
     "section 3 states)*) — `byte[+0x6B4] == 0`"),

    # B4: writes at +0x714 - the three battle-unit writers (00236B55, 0030F806, 0031071B) plus nine stores in at least
    #     eight other bodies (retool.py grep "+ 0x714],").
    (HT, "Four other `[reg+0x714]` writes exist and are **different structures** — three store the float\n"
         "`0x3F490FDB` (π/4) and one is `Audio`.",
     "~~Four~~ Nine other `[reg+0x714]` writes, in eight bodies, exist and are **different structures** — ~~three store "
     "the float~~\n"
     "~~`0x3F490FDB` (π/4) and one is `Audio`.~~ five store the float `0x3F490FDB` (π/4), in `007084E0`, `00708540`, "
     "`007085A0` and `00708600`, and the others are in `00542740`, `006FEF20`, `00708470` and `007D2150` *(corrected "
     "2026-10-02, OPUS: `retool.py grep \"+ 0x714],\"`, sites `0054323E`, `006FEF28`, `007084B2`, `00708527`, "
     "`00708587`, `007085EB`, `0070865F`, `007086B7`, `007D28EF`; a census over the known extents, so a lower "
     "bound)*."),
    (CNS, "A whole-image sweep for writes at `+0x714` returns **eight bodies**, of which\n"
          "only three are battle-unit bodies; the other five sit in",
     "A whole-image sweep for writes at `+0x714` returns ~~**eight bodies**~~ **at least eleven bodies** *(corrected "
     "2026-10-02, OPUS: `retool.py grep \"+ 0x714],\"` finds the three battle-unit writers `00236B55`, `0030F806`, "
     "`0031071B` and nine stores in eight other bodies - `00542740`, `006FEF20`, `00708470`, `007084E0`, `00708540`, "
     "`007085A0`, `00708600`, `007D2150`)*, of which\n"
     "only three are battle-unit bodies; the other ~~five~~ eight sit in"),
    (CNS, "and quoting the raw eight would contradict",
     "and quoting the raw ~~eight~~ eleven *(corrected 2026-10-02, OPUS: the sweep figure above)* would contradict"),

    # B5: +0x6B8 has 64 displacement sites, three of them lea (retool.py grep "+ 0x6b8]").
    (HC, "**Scope limit.** `+0x6B8` has 65 sites image-wide,",
     "**Scope limit.** `+0x6B8` has ~~65~~ 64 sites image-wide *(corrected 2026-10-02, OPUS: `retool.py grep \"+ "
     "0x6b8]\"` lists 64, three of them `lea`; CONTRACT-combo-continuation.md CB-1 and its falsification C1 say the "
     "same)*,"),

    # C1 (+ A6): the README's "Not yet documented" list - all five are documented.
    (RM, "- The 13-phase standard-action pipeline (`00304850` `BattleUnit_AdvanceStandardActionState`)\n"
         "- Presentation slot pool (`0030C970` / `0030CA80` / `0030CF40` / `0030CFB0` / `0030D070`)\n"
         "- `BattleUnit_CommitAction` (`0030F760`) and the action context at `BattleUnit+0x708/0x710/0x714/0x6B4`\n"
         "- Pending action-selection queue (`00313CD0`, up to 8 entries)\n"
         "- Target set materialization, reservation, enmity",
     "- ~~The 13-phase standard-action pipeline (`00304850` `BattleUnit_AdvanceStandardActionState`)~~ *(answered: see "
     "Command-And-Action-Seam/native-command-seam.md, UQ-108; 2026-10-02, OPUS)*\n"
     "- ~~Presentation slot pool (`0030C970` / `0030CA80` / `0030CF40` / `0030CFB0` / `0030D070`)~~ *(answered: see "
     "Command-And-Action-Seam/native-command-seam.md, UQ-112 and the section on `0030CA80`; 2026-10-02, OPUS)*\n"
     "- ~~`BattleUnit_CommitAction` (`0030F760`) and the action context at `BattleUnit+0x708/0x710/0x714/0x6B4`~~ "
     "*(answered: see the-moment-an-action-is-committed.md, CONTRACT-commit-action.md and "
     "CONTRACT-the-moment-an-action-is-committed.md; 2026-10-02, OPUS)*\n"
     "- ~~Pending action-selection queue (`00313CD0`, up to 8 entries)~~ the pending action-selection queue "
     "(`00313CD0`) is a 64-entry ring drained up to 8 entries per call *(corrected 2026-10-02, OPUS: `00313D18 and cl, "
     "0x3f`, `00313CF7 mov edi, 8`; documented in Command-And-Action-Seam/native-command-seam.md section 7)*\n"
     "- ~~Target set materialization, reservation, enmity~~ *(answered: see how-an-action-gathers-its-targets.md and "
     "CONTRACT-battle-target-buffer.md; the attacker mask and enmity in the-moment-an-action-is-committed.md; "
     "2026-10-02, OPUS)*"),

    # C2-C5: the availability page.
    (AV, "The enumerated table is therefore **not** the complete reason-code set — it is the set\n"
         "raised by the two functions that were read.",
     "~~The enumerated table is therefore **not** the complete reason-code set — it is the set~~\n"
     "~~raised by the two functions that were read.~~ *(answered: the table was completed the same day - nineteen "
     "codes from every leg, section 10, AI-4; 2026-10-02, OPUS)*"),
    (AV, "bit identified); **AI-1 remains fully open** — nothing here maps a code to on-screen text.",
     "bit identified); ~~**AI-1 remains fully open** — nothing here maps a code to on-screen text.~~ *(answered: AI-1, 2026-09-02 - the "
     "codes never reach a screen, §7 and §11; 2026-10-02, OPUS)*"),
    (AV, "and a **global** amount with a per-unit fallback.",
     "and a **global** amount ~~with a per-unit fallback~~ checked together with the gil cost already reserved for the "
     "action in progress at `unit[0xE58]` *(corrected 2026-10-02, OPUS: `+0xE58` is not a purse - `0030EFC0 mov dword "
     "ptr [rbx + 0xe58], eax` stores `00309060`'s result there, the refund `00300280` adds it back and `00305640` "
     "clears it; row `0x15` of the reason-code table)*."),
    (AV, "a party-wide pool checked before a per-unit one,",
     "a party-wide pool checked before ~~a per-unit one~~ the cost already reserved at `unit[0xE58]` *(corrected "
     "2026-10-02, OPUS: `+0xE58` is a reserved cost, not a per-unit pool, `0030EFC0`; row `0x15`)*,"),
    (AV, "## SWE2-EC7-19 update (2026-05-15) — `00322490`",
     "## SWE2-EC7-19 update (~~2026-05-15~~ 2026-09-18 *(corrected 2026-10-02, OPUS: committed in `add029c9c`)*) — "
     "`00322490`"),

    # C6: when targets are gathered - after the charge (phase 4 charge step, phase 9 Battle_BuildActionTargetSet).
    (HG, "chosen. *Which step of the action that is - before or after the charge - was not read.*",
     "chosen. ~~*Which step of the action that is - before or after the charge - was not read.*~~ *(answered: after the charge "
     "- phase 4 of `BattleUnit_AdvanceStandardActionState` runs the charge progress step and phase 9 runs "
     "`Battle_BuildActionTargetSet`; see Command-And-Action-Seam/native-command-seam.md, UQ-108; 2026-10-02, OPUS)*"),

    # C7 + C8: the commit is executed (CONTRACT-commit-action.md §13, §13a); the +0x730 record's reader is the next
    #     commit (0030F84E cmp di, [rbx+0x744]; 0030F857 cmp ebp, [rbx+0x740]).
    (CTM, "naming**, not as execution of the commit itself, which is unexecuted.",
     "naming**, not as execution of the commit itself~~, which is unexecuted~~ *(answered: the commit is executed as "
     "shipped bytes under Unicorn, 1309 commands, 704 compared lines, 0 mismatches, and its nine callees by EXP-091 - "
     "CONTRACT-commit-action.md §13 and §13a; 2026-10-02, OPUS)*."),
    (CTM, "`+0x730`–`+0x747`; its readers were not in this census's band and stay unenumerated.",
     "`+0x730`–`+0x747`; ~~its readers were not in this census's band and stay unenumerated.~~ its reader is the next "
     "commit, `0030F84E cmp di, word ptr [rbx + 0x744]` and `0030F857 cmp ebp, dword ptr [rbx + 0x740]` *(corrected "
     "2026-10-02, OPUS: the cancel `003105D0` writes the cancelled record there and `BattleUnit_CommitAction` reads it; "
     "the-moment-an-action-is-committed.md, the cancellation section)*."),

    # C9: the commit does raise a notify - 0030F975 call 00313B30, which hands a record per unit to 002ED2A0.
    (CCA, "does not read a script, touch a resource, or raise an event of its own. What it does emit is a",
     "does not read a script~~, touch a resource, or raise an event of its own~~ or touch a resource; it does notify "
     "*(corrected 2026-10-02, OPUS: on a mask change `0030F975 call 00313B30`, which hands a record per unit to "
     "`002ED2A0`, §13a)*. What it does emit is a"),

    # C10: the commit page's "not claimed" rows.
    (TM, "| **Not established either way, and left that way.** Nothing in this function reads it. |",
     "| ~~**Not established either way, and left that way.**~~ *(answered: a shadow - the cancel `003105D0` copies it to "
     "the cancelled record `+0x730`–`+0x747` (`003106B9`–`003106E3`), which the next commit reads; see the "
     "cancellation section above; 2026-10-02, OPUS)* Nothing in this function reads it. |"),
    (TM, "— a two-word eligibility gate on receiving the broadcast — and its *meaning* is not. See",
     "— a two-word eligibility gate on receiving the broadcast — ~~and its *meaning* is not~~ *(answered: KO, Stone "
     "and X-Zone / Vanished - how-a-combo-continues-and-what-it-blocks.md, condition 4, and "
     "how-an-action-gathers-its-targets.md; 2026-10-02, OPUS)*. See"),

    # C11 + C12: what carries +0xBA0 into the funnel (00305AE4-00305B2F); the seam does not call the commit.
    (CNS, "and what carries `+0xBA0` into\n  the funnel is not read here.",
     "~~and what carries `+0xBA0` into~~\n  ~~the funnel is not read here.~~ *(answered: "
     "`BattleUnit_SelectAndCommitNextAction` commits the issued command, `+0xBA0` id and `+0xBB8` handle, at "
     "`00305AE4`–`00305B2F`; see Command-And-Action-Seam/native-command-seam.md, E-5 settled 2026-09-12; 2026-10-02, "
     "OPUS)*"),
    (NS, "             -> 0030F760 BattleUnit_CommitAction  (where flow reaches it)\n",
     "             -> 0030F760 BattleUnit_CommitAction  (where flow reaches it)   # <- corrected 2026-10-02, OPUS - the "
     "seam does not reach the commit; 00311CF0 records +0xBA0 / +0xBB8 only (00311D7A, 00311DB0), and "
     "BattleUnit_SelectAndCommitNextAction commits the issued command later (00305AE4-00305B2F); "
     "CONTRACT-native-command-seam.md CS-1\n"),

    # C13: slot bytes +0x1E-+0x1F are alignment padding (answered 2026-09-18).
    (NS, "      | `+0x1E` | 2 | **no access found** in any of the nine functions | — |",
     "      | `+0x1E` | 2 | **no access found** in any of the nine functions *(answered: alignment padding after the "
     "`u16` action id, accessed by nothing - the 2026-09-18 answer above; 2026-10-02, OPUS)* | — |"),
    (NS, "      - **Still open:** `+0x1E`–`+0x1F`, the `+0x2C` bits",
     "      - **Still open:** ~~`+0x1E`–`+0x1F`,~~ *(answered: padding, 2026-09-18 above; 2026-10-02, OPUS)* the `+0x2C` "
     "bits"),

    # C14: the handler-table contract's open items (AT-2, AT-3, AT-4, section 8).
    (CHT, "  page's §8 decodes the locomotion sub-range and the rest is its open work.\n"
          "- Why 18 slots are empty, and whether any id in those gaps is ever issued.",
     "  page's §8 decodes the locomotion sub-range and the rest is its open work *(answered in part: see "
     "Action-Dispatch/battle-action-handler-table.md - AT-3, the `0x4021` wait handler, and AT-4 with section 10, the "
     "set/clear-status runs; 2026-10-02, OPUS)*.\n"
     "- ~~Why 18 slots are empty, and whether any id in those gaps is ever issued.~~ *(answered: AT-2, closed "
     "2026-09-12 - rejected everywhere and never authored, Action-Dispatch/battle-action-handler-table.md section 4; "
     "2026-10-02, OPUS)*"),

    # C15 + C16: the handler page's stale negatives (AT-8, AT-9, EI-2, the 004697C0 section, the 003083B0 subtree).
    (HT, "**AT-5's negative therefore stands in its exact original form**: *id → player-visible command name\n"
         "cannot be completed*",
     "**AT-5's negative therefore stands in its exact original form**: ~~*id → player-visible command name~~\n"
     "~~cannot be completed*~~ *(answered: each id is named through its row's `+0x34` into bank 0 of the battle text - "
     "AT-8 answered by reference 2026-09-14 and AT-9 answered 2026-09-11, section 6 above; Action-Availability AI-2; "
     "2026-10-02, OPUS)*"),
    (HT, "**AT-9 is blocked on the same join.** Command ids",
     "~~**AT-9 is blocked on the same join.**~~ *(answered: AT-9 ANSWERED 2026-09-11, `0x113` Dismiss and `0x95` "
     "Dismount, section 6; 2026-10-02, OPUS)* Command ids"),
    (HT, "- **Not what lies above id 542.** `AT-8` remains open on the contents of the space;",
     "- **Not what lies above id 542.** ~~`AT-8` remains open on the contents of the space;~~ *(answered: EI-2, "
     "2026-09-12 - above 542 is the order space, section 2; 2026-10-02, OPUS)*"),
    (HT, "- **Not what `FUN_004697C0` does** with",
     "- ~~**Not what `FUN_004697C0` does**~~ *(answered: it posts battle message `0x05`, `0x06` or `0x07` - "
     "Post-Result-Events/the-post-result-events-and-the-battle-message-table.md, the SWE2-EC7-21 update; 2026-10-02, "
     "OPUS)* with"),
    (HT, "  body past `003083FF` is unread, and",
     "  body past `003083FF` ~~is unread,~~ *(answered: its subtree is bound in the section on the `003083B0` exclusive "
     "subtree below; 2026-10-02, OPUS)* and"),

    # C17: the combo contract's stale items (contracts since authored; CB-3; UQ-115; +0x12 is written at 0038885D).
    (CCC, "> **combos**; the native command seam and the handler table remain uncontracted and this document",
     "> **combos**; the native command seam and the handler table ~~remain uncontracted~~ *(answered: contracted since, "
     "CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md; 2026-10-02, OPUS)* and this "
     "document"),
    (CCC, "| **Uncontracted** | the native command seam and the handler table — S-20's other two pages, not claimed here |",
     "| **~~Uncontracted~~ Sibling** | the native command seam and the handler table — S-20's other two pages, not "
     "claimed here *(answered: see CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md; "
     "2026-10-02, OPUS)* |"),
    (CCC, "- What the second draw at `003887E3` contributes that the first does not.",
     "- ~~What the second draw at `003887E3` contributes that the first does not.~~ *(answered: see CB-3 items 1-3 - "
     "the first draw is the percent gate, `003887E3` the 11-pass HP-band loop that sets the count; 2026-10-02, OPUS)*"),
    (CCC, "- What `+0x6B8` is, beyond being preserved (CB-6).",
     "- ~~What `+0x6B8` is, beyond being preserved (CB-6).~~ *(answered: the combo's running hit tally, UQ-115 in "
     "how-a-combo-continues-and-what-it-blocks.md; 2026-10-02, OPUS)*"),
    (CCC, "- The native command seam and the handler table — S-20's other two pages.",
     "- ~~The native command seam and the handler table — S-20's other two pages.~~ *(answered: see "
     "CONTRACT-native-command-seam.md and CONTRACT-battle-action-handler-table.md, both authored 2026-09-22; "
     "2026-10-02, OPUS)*"),
    (CCC, "The per-kind record at `0208D480` is authored data; the roll's distribution is not read here.",
     "The per-kind record at `0208D480` is ~~authored data~~ runtime state the roll writes *(corrected 2026-10-02, "
     "OPUS: `0038885D and byte ptr [rdi + 0x12], 0xf` and `00388865 or byte ptr [rdi + 0x12], r14b` rewrite it on every "
     "first hit that passes the gate)*; the roll's distribution is ~~not read here~~ read in CB-3 *(answered: see CB-3 "
     "items 1-4; 2026-10-02, OPUS)*."),

    # C18: the action row's layout block and falsification table.
    (DR, "  +0x00 u16  helpTextId (4000 = none)      +0x1E u8   messageKind (255 = unused row)\n",
     "  +0x00 u16  helpTextId (4000 = none)      +0x1E u8   messageKind (255 = unused row)   # <- corrected 2026-10-02, "
     "OPUS - +0x1E is the id-class byte (renamed 2026-09-30, field map row +0x1E)\n"),
    (DR, "  +0x08 u8   recipe (0 = weapon's)         +0x22 u16  linkedMenuId (0xFFFF = none)\n",
     "  +0x08 u8   recipe (0 = weapon's)         +0x22 u16  linkedMenuId (0xFFFF = none)   # <- corrected 2026-10-02, "
     "OPUS - +0x22 is an id whose space +0x1E names (field map row +0x22)\n"),
    (DR, "  +0x0A u8   mpCost                        +0x28 u8   quickeningIndex (120..153, reader not found)\n",
     "  +0x0A u8   mpCost                        +0x28 u8   quickeningIndex (120..153, reader not found)   # <- "
     "corrected 2026-10-02, OPUS - the reader is 0030A190 (word read 0030A209), GR-4\n"),
    (DR, "| `+0x28` — 26 Esper attacks, `120`–`153` |",
     "| `+0x28` — 26 ~~Esper attacks~~ Quickening-family rows *(corrected 2026-10-02, OPUS: as the field map row "
     "`+0x28` was corrected 2026-09-27)*, `120`–`153` |"),

    # C19: the result record's stale lines.
    (RR, "ResultRecord (>= 0x148 B; -1 / 0xFFFF = untouched)\n",
     "ResultRecord (>= 0x148 B; -1 / 0xFFFF = untouched)   # <- corrected 2026-10-02, OPUS - exactly 0x148 B, a stack "
     "local at every call site (FP-2, section 2.3)\n"),
    (RR, "  +0x08  u32  (context +0x10)                      +0x5C  i32[32] parameter A per status bit\n",
     "  +0x08  u32  (context +0x10)                      +0x5C  i32[32] parameter A per status bit   # <- corrected "
     "2026-10-02, OPUS - +0x08 is the gil amount the applier deducts (FP-1, row +0x008)\n"),
    (RR, "  +0x38  i32  (context +0x20)\n",
     "  +0x38  i32  (context +0x20)   # <- corrected 2026-10-02, OPUS - the poach reward item, -1 = none (row +0x038)\n"),
    (RR, "- **The record is at least 0x148 bytes**; allocate more only if the allocation site says so.",
     "- ~~**The record is at least 0x148 bytes**; allocate more only if the allocation site says so.~~ *(answered: "
     "FP-2 - a `0x148`-byte stack local at every call site, nothing above `+0x147`, section 2.3; 2026-10-02, OPUS)*"),
    (RR, "Which actions reach the two writers is not enumerated.",
     "Which actions reach ~~the two writers~~ `00388D50` is not enumerated *(answered for `0038F6F0`: step slot 163, "
     "the whole committed list of recipe 99, action `0x103` - the `+0x008` row above and the applier's step 18; "
     "2026-10-02, OPUS)*."),

    # C20: the status-layer modes are read (mode 2 sets, mode 0 clears the layer +0x68).
    (AP, "`0`. What that function's modes do is not read here;",
     "`0`. ~~What that function's modes do is not read here;~~ *(answered: mode 2 sets and mode 0 clears the mutable layer "
     "`+0x68`, step 14 above; 2026-10-02, OPUS)*"),

    # C21: the target-buffer contract's stale items - the bit-8 writer (003075CB), the script path (003495A0 ->
    #     00313120, 0031325F / 0031328C), and outcome-word bits 9 and 11 (003075E8-003075EC; 00389140).
    (TB, "so **something else fills it** and this contract does\n   not say what.",
     "so **something else fills it** ~~and this contract does~~\n   ~~not say what.~~ *(answered: "
     "`Battle_ProcessActionTarget` ORs `0x100` into the entry's `+8` at `003075CB` when the result's flag word B bit "
     "3, knockback, is set - see THE WRITER IS KNOWN below; 2026-10-02, OPUS)*"),
    (TB, "None directly. The buffer is populated from actor queries and consumed by action dispatch; no opcode,\n"
         "verb or authored table reaches it.",
     "None directly. The buffer is populated from actor queries and consumed by action dispatch; ~~no opcode,~~\n"
     "~~verb or authored table reaches it.~~ a script verb body reaches it *(corrected 2026-10-02, OPUS: `003495A0` "
     "calls `00313120` (`003495B2`), which resets the buffer and appends to it at `0031325F` / `0031328C`; "
     "the-moment-an-action-is-committed.md, the Script_VM crossing)*."),
    (TB, "   > knockback / parry / combo-continues and bit 11 the result's flag word B bit 0 — the\n"
         "   > mode-2 resource-reaction chance rolled (`test r12b, al` at `003075F4`,",
     "   > knockback / ~~parry~~ counter / combo-continues and bit 11 the result's flag word B bit 0 — the\n"
     "   > ~~mode-2 resource-reaction chance rolled~~ ranged critical rolled *(corrected 2026-10-02, OPUS: bit 9 is "
     "`0x200` from flag B bit 2 at `003075E8`–`003075EC`, the counter flag; bit 11 is flag B bit 0, which `00389140` "
     "sets on the ranged critical, `003891B7`–`003891D9`; Result-Record/the-result-record-field-map.md row "
     "`+0x018`)* (`test r12b, al` at `003075F4`,"),

    # C22: FL-2 closed SUPERSEDED 2026-09-26 in the register (not WITHDRAWN, not open).
    (PR, "*(closed — the register row is WITHDRAWN.)*",
     "*(closed — the register row is ~~WITHDRAWN~~ SUPERSEDED, 2026-09-26.)* *(corrected 2026-10-02, OPUS: "
     "_index/OPEN-QUESTIONS.md row FL-2 reads SUPERSEDED under the runtime rule; the live read is ASTRA-QUEUE AQ-16)*"),
    (PR, "  **The row stays open**: no process was read,",
     "  ~~**The row stays open**~~ *(answered: the register row closed SUPERSEDED 2026-09-26, the live read carried by "
     "ASTRA-QUEUE AQ-16; 2026-10-02, OPUS)*: no process was read,"),

    # D1: the README's statuses against each page's front matter.
    (RM, "  **DOCUMENTED, tier 1.** The three range bands",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`, promoted 2026-10-01)* The three range bands"),
    (RM, "  **PARTIAL, tier 1.** `unit + 0x6B7` is",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: DOCUMENTED`)* `unit + 0x6B7` is"),
    (RM, "  **DOCUMENTED, tier 1.** How a resolved result",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)* How a resolved result"),
    (RM, "  **DOCUMENTED, tier 1.** The record a resolution",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1.** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)* The record a resolution"),

    # D2: the README lists six of the eleven mechanism pages and no contract - the twelve missing, with the status each
    #     page's own front matter states.
    (RM, "  table is published beside it.\n",
     "  table is published beside it *(2026-10-02, OPUS: the twelve pages below were missing from this list; each "
     "status is the one its own front matter states)*.\n"
     "\n"
     "- [`the-moment-an-action-is-committed.md`](the-moment-an-action-is-committed.md) — the commit, its copy, the "
     "leader broadcast and the attacker mask — **AUDITED**\n"
     "- [`applying-a-result-to-a-target.md`](applying-a-result-to-a-target.md) — the result applier, step by step — "
     "**DOCUMENTED**\n"
     "- [`Action-Availability/battle-command-availability-and-reason-codes.md`]"
     "(Action-Availability/battle-command-availability-and-reason-codes.md) — why a command is refused, and the "
     "nineteen reason codes — **AUDITED**\n"
     "- [`Action-Dispatch/battle-action-handler-table.md`](Action-Dispatch/battle-action-handler-table.md) — the order "
     "handler table and the two id spaces — **DOCUMENTED**\n"
     "- [`Action-Definition-Row/the-action-definition-row.md`](Action-Definition-Row/the-action-definition-row.md) — "
     "the 60-byte action row, field by field — **DOCUMENTED**\n"
     "- [`CONTRACT-commit-action.md`](CONTRACT-commit-action.md) — L1, **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-the-moment-an-action-is-committed.md`](CONTRACT-the-moment-an-action-is-committed.md) — L2, "
     "**CONTRACT READY**\n"
     "- [`CONTRACT-native-command-seam.md`](CONTRACT-native-command-seam.md) — L2, **CONTRACT READY**\n"
     "- [`CONTRACT-battle-action-handler-table.md`](CONTRACT-battle-action-handler-table.md) — L2, **CONTRACT READY**\n"
     "- [`CONTRACT-combo-continuation.md`](CONTRACT-combo-continuation.md) — L2, **CONTRACT READY**\n"
     "- [`CONTRACT-battle-target-buffer.md`](CONTRACT-battle-target-buffer.md) — L1, **DIFFERENTIAL TESTED**\n"
     "- [`CONTRACT-apply-result-to-target.md`](CONTRACT-apply-result-to-target.md) — L2, **BEHAVIORALLY "
     "UNDERSTOOD**\n"),

    # D3: the availability page's body banner against its front matter (AUDITED; AI-1 answered).
    (AV, "**PARTIAL.** The top-level cascade is read at instruction level.",
     "~~**PARTIAL.**~~ **AUDITED.** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`, every box "
     "ticked; the codes never reach a screen, AI-1 answered 2026-09-02 in §7 and §11, so the unmapped-message clause "
     "below is stale)* The top-level cascade is read at instruction level."),
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
