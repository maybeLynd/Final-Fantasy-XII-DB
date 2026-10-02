"""apply_12items.py [--apply] - 12-Items-Equipment-Shops-License readiness map (readiness-12-items.md), section 2.4
contradictions 1-43 and the one section 2.5 finding that is not an unstated map, settled on the pages (OPUS, 2026-10-02).

Each edit strikes the DISFAVOURED side only (the side the map's dated correction, the bytes or the shipped data
refute) and restates it, tagged *(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
Every ~~ span opens and closes on one line; multi-line text is struck line by line.
Code-block lines (and the one YAML front-matter line) get a trailing comment instead of a strike; their OLD runs into
the next line so NEW never contains OLD. No heading changes.
The three maps no page states (licence-node class map, 0031E9A0 grouping, shop tab remap) and the structural gaps are
left for later, as briefed.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "12-Items-Equipment-Shops-License/"
R = F + "README.md"
IE = F + "item-id-encoding-and-equipment-compatibility.md"
CEQ = F + "CONTRACT-equipment-compatibility.md"
CIN = F + "CONTRACT-inventory-class-storage.md"
IU = F + "using-an-item-is-an-action-that-costs-an-item.md"
ES = F + "equipment-slots-and-the-single-stat-rebuild.md"
LC = F + "license-check-what-the-board-actually-tests.md"
CLC = F + "CONTRACT-license-check.md"
LB = F + "license-board-grid-format.md"
ST = F + "the-shop-table-and-its-stock-gates.md"
BZ = F + "the-bazaar-recipe-unlock-and-purchase.md"
CBZ = F + "CONTRACT-bazaar-unlock-and-purchase.md"

EDITS = [
    # C8 (favoured page, stale line): 00328BD0 is the resetJobs body (only caller 00342230)
    ("12-Items-Equipment-Shops-License/license-board-grid-format.md",
     "What `00328BD0` is for as a whole is not read.",
     "~~What `00328BD0` is for as a whole is not read.~~ *(answered: it is the `resetJobs` body - it clears equipment, "
     "un-learns licences with an LP refund and rebuilds gambits; its only caller is `00342230`; 2026-10-02, OPUS)*"),
    # C1: queries dispatch through +0x50 (00309F96), writes through +0x48 (00300943-00300960).
    (CIN, "**Dispatch is per class, through a pointer in the descriptor** (`+0x50`), not by a switch.",
     "**Dispatch is per class, through a pointer in the descriptor** (~~`+0x50`~~ `+0x50` for a query, `+0x48` for "
     "a mutate *(corrected 2026-10-02, OPUS: checked at `00309F96` `mov rax, [rdx+0x50]` and `00300943`–`00300960` "
     "`mov rax, [rsi+0x48]` / `test` / `call rax`; CONTRACT-bazaar-unlock-and-purchase.md §13a)*), not by a switch."),
    (CIN, "| `+0x50` | the handler, or **NULL** |",
     "| `+0x50` | ~~the handler, or **NULL**~~ the query handler, or **NULL**; the mutate handler is a second pointer "
     "at `+0x48` *(corrected 2026-10-02, OPUS: checked at `00300943`–`00300960`; CONTRACT-bazaar-unlock-and-purchase.md "
     "§13a)* |"),
    (CIN, "**Dispatch is per class, through a function pointer in the descriptor at `+0x50`** — not a switch —",
     "**Dispatch is per class, through a function pointer in the descriptor at ~~`+0x50`~~ `+0x50` (query) or "
     "`+0x48` (mutate)** *(corrected 2026-10-02, OPUS: `00309F96`, `00300943`–`00300960`)* — not a switch —"),
    (CIN, "Both call sites null-test `+0x50` (`00309F9A`, `00300946`), so a",
     "Both call sites null-test ~~`+0x50` (`00309F9A`, `00300946`)~~ their own slot, the query entry `+0x50` "
     "(`00309F9A`) and the ±1 entry `+0x48` (`00300946`) *(corrected 2026-10-02, OPUS: checked at "
     "`00300943`–`00300960`)*, so a"),
    (CIN, "    QueryFn   handler;           /* +0x50  NULL on seven of fifteen */\n} ItemClassDescriptor;",
     "    QueryFn   handler;           /* +0x50  NULL on seven of fifteen */   // <- corrected 2026-10-02, OPUS: the "
     "query handler; the mutate handler is a separate pointer at +0x48 (00300943-00300960), null only on rows 5, 7, 11\n"
     "} ItemClassDescriptor;"),

    # C2: classes 9, 10, 13, 14 are grant-expanding, not inert (+0x48 = 002FD530 / 002FD640 / 002FD780 / 002FD880).
    (CIN, "512, 256, 128 and 4095 with **no handler and `+0x10 == 0`** — two independent fields agreeing. Those\n"
          "ids pass the bound check and then reach nothing. **4,991 encodable, inert ids.**",
     "512, 256, 128 and 4095 with ~~**no handler and `+0x10 == 0`** — two independent fields agreeing. Those~~\n"
     "~~ids pass the bound check and then reach nothing. **4,991 encodable, inert ids.**~~ `+0x10 == 0` and no "
     "**query** handler, so a query answers 0 — but each has a **mutate** handler at `+0x48`: `002FD530` (reward "
     "package: gil and nested items), `002FD640` (package selector), `002FD780` (bazaar good: its granted pairs) and "
     "`002FD880` (gil as the id, `(id & 0xFFF) × delta`, `002FD89A`–`002FD8B4`). They are grant-expanding classes, not "
     "inert ones *(corrected 2026-10-02, OPUS: descriptor `+0x48` of rows 9, 10, 13 and 14 read from `01EEBCC0`; "
     "item-id-encoding-and-equipment-compatibility.md §3)*."),
    (CIN, "- Whether the four inert classes are unreleased content or an allocation that moved.",
     "- ~~Whether the four inert classes are unreleased content or an allocation that moved.~~ *(answered: see §10 — "
     "classes 9, 10, 13 and 14 are not inert; their `+0x48` mutate handlers expand a write into gil or nested items; "
     "2026-10-02, OPUS)*"),
    (CIN, "NULL handler (§9); and the **inert classes** — giving them working storage would make a\n"
          "reimplementation more capable than the original in a way no test notices until something addresses one\n"
          "of those 4,991 ids.",
     "NULL handler (§9); and ~~the **inert classes** — giving them working storage would make a~~\n"
     "~~reimplementation more capable than the original in a way no test notices until something addresses one~~\n"
     "~~of those 4,991 ids.~~ the **grant-expanding classes** 9, 10, 13 and 14: no storage and a query that answers 0, "
     "but a write through `+0x48` that grants gil or nested items — modelling them as inert breaks every bazaar "
     "purchase and reward bundle *(corrected 2026-10-02, OPUS: §10)*."),

    # C3: hi6 is the equipped count (channel 2 on equip 0030C447-0030C45C / unequip 0030F9D7-0030F9EB).
    (CIN, "`reserved`, and **kind 0 returns `owned - reserved`**. That subtraction is the availability the\n"
          "item-use path needs, because an item is reserved when the character commits and consumed later.",
     "`reserved`, and **kind 0 returns `owned - reserved`**. ~~That subtraction is the availability the~~\n"
     "~~item-use path needs, because an item is reserved when the character commits and consumed later.~~ The high six "
     "bits are the **equipped** count, not an item-use reservation: equipping adds 1 on channel 2 "
     "(`0030C447`–`0030C45C`) and unequipping takes 1 (`0030F9D7`–`0030F9EB`), only for `0x1nnn` ids other than "
     "`0x1000` (`0030C426`–`0030C445`), while an item action takes from the owned count at once on channel 1 "
     "(`0030EF9F`–`0030EFB0`) and keeps its reservation on the unit at `+0xDC8`. So kind 0 is owned minus equipped, "
     "the free copies *(corrected 2026-10-02, OPUS: checked at those addresses; "
     "equipment-slots-and-the-single-stat-rebuild.md §3, using-an-item-is-an-action-that-costs-an-item.md §3)*."),
    (CIN, "| 2 | `word >> 10` — the **reserved** count, six bits |",
     "| 2 | `word >> 10` — the ~~**reserved**~~ **equipped** count, six bits *(corrected 2026-10-02, OPUS: channel 2 "
     "moves it on equip and unequip, `0030C447`–`0030C45C`, `0030F9D7`–`0030F9EB`; §7)* |"),
    (CIN, "the **`owned - reserved` availability** of kind 0;",
     "the ~~**`owned - reserved` availability**~~ **`owned - equipped` free count** *(corrected 2026-10-02, OPUS: §7)* "
     "of kind 0;"),

    # C4: 00308FF0 returns row.b_0A for categories 5 / 6, else 0, and faults on a failed resolution (0030904A-0030905D).
    (IU, "([`00309041`](../_index/ADDRESS-INDEX.md)) is returned — the flat secondary\n"
         "resource offset for a 0x21F-entry table. Null resolutions return 0.",
     "([`00309041`](../_index/ADDRESS-INDEX.md)) ~~is returned — the flat secondary~~\n"
     "~~resource offset for a 0x21F-entry table. Null resolutions return 0.~~ is the row address, not the result: the "
     "function returns the row's byte `+0x0A` when its category byte `+0x1E` is 5 or 6 (`movzx eax, byte [rcx+0x1e]` / "
     "`sub al, 5` / `cmp al, 1` / `ja`, then `movzx eax, byte [rcx+0xa]`), else 0; a failed resolution zeroes `rcx` "
     "(`00309048`) and still reads `[0x1E]`, so it faults rather than returning 0 *(corrected 2026-10-02, OPUS: checked "
     "at `0030904A`–`0030905D`; §4's `row.b_0A for kinds 5 / 6, else 0`)*."),

    # C5: the licence check's one argument is the stats record (00323ECD mov rsi, rcx; no +0x698 hop).
    (LC, "    if (unit[0x194 + i] & req[i])  return 1;             // ANY overlapping bit\nreturn 0;",
     "    if (unit[0x194 + i] & req[i])  return 1;             // ANY overlapping bit   <- corrected 2026-10-02, OPUS: "
     "the stats record, not the unit (00323ECD mov rsi, rcx; one argument, no +0x698 hop)\nreturn 0;"),
    (LC, "unit + 0x005   record kind byte      (licensed only when 0)\n"
         "unit + 0x194   owned-License bitmask, 46 bytes / 368 bits, one bit per board node\n\nlicense node row",
     "unit + 0x005   record kind byte      (licensed only when 0)   <- corrected 2026-10-02, OPUS: statsRecord + "
     "0x005 (00323EF3)\n"
     "unit + 0x194   owned-License bitmask, 46 bytes / 368 bits, one bit per board node   <- corrected 2026-10-02, "
     "OPUS: statsRecord + 0x194, the check's one argument (00323ECD), as section 4 says\n\nlicense node row"),
    (LC, "in the 46-byte mask at `unit + 0x194`. There",
     "in the 46-byte mask at ~~`unit + 0x194`~~ `statsRecord + 0x194` *(corrected 2026-10-02, OPUS: the check's one "
     "argument is the stats record, `00323ECD`; §4's correction of 2026-09-11)*. There"),

    # C6: +4 is the type id; ids 0-6 reach the board, so guest row 6 (Reks) is board-checked (00323EFF).
    (LC, "> Guests and non-party units do not fail this check; they never reach it.",
     "> ~~Guests and non-party units do not fail this check; they never reach it.~~ The test is on the type id at "
     "`+4`, not a party slot: type ids 0–6 reach the board — the six party members and row 6, the guest Reks — while "
     "guests 7–16 and non-party units never do *(corrected 2026-10-02, OPUS: checked at `00323EFF` "
     "`cmp byte [rsi+4], 6` / `ja` → licensed; CONTRACT-license-check.md §10, \"slot 6 included\")*."),
    (LC, "if (unit[4] > 6)           return 1;                          // party slot index\n```",
     "if (unit[4] > 6)           return 1;                          // party slot index   <- corrected 2026-10-02, "
     "OPUS: the party-table type id (0-5 the party, 6 Reks, 7-16 the other guests), 00323EFF\n```"),
    (LC, "unit + 0x004   party slot index      (licensed only when <= 6)\nunit + 0x005",
     "unit + 0x004   party slot index      (licensed only when <= 6)   <- corrected 2026-10-02, OPUS: statsRecord + "
     "0x004, the party-table type id (0-5 the party, 6 Reks, 7-16 the other guests); 00323EFF\nunit + 0x005"),
    (CLC, "licensed party member** — guests and non-party units do not\n*fail* this check, they never reach it **[page]**.",
     "licensed party member** — ~~guests and non-party units do not~~\n~~*fail* this check, they never reach it~~ "
     "**[page]**; non-party units and guests 7–16 never reach it, but the guest row 6, Reks, does: the test is the "
     "type id `+4` ≤ 6 *(corrected 2026-10-02, OPUS: checked at `00323EFF`; §10, \"slot 6 included\")*."),

    # C7: the main hand's +0x11 must equal the off-hand's +0x09 (002F7ECF / 002F7F76; C-EQ EQ-1).
    (IE, "  `+0x09` (primary side) and `+0x11` (secondary side) on the definitions — no code patch needed.",
     "  `+0x09` ~~(primary side)~~ on the off-hand item and `+0x11` ~~(secondary side)~~ on the main-hand weapon "
     "*(corrected 2026-10-02, OPUS: the main hand's `+0x11` must equal the off-hand's `+0x09`, checked at "
     "`002F7ECF` / `002F7F76` and both call sites `002FA00D`–`002FA013`, `002FA062`–`002FA069`; "
     "CONTRACT-equipment-compatibility.md EQ-1)* on the definitions — no code patch needed."),

    # C8: 00328BD0 is the resetJobs body (only caller 00342230 at 00342242); the shared preset loader is 00327CB0.
    (ES, "names it: it is\n"
         "  `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`, reached by the script verb\n"
         "  **`resetJobs` (`05D6`)** through `00342230` and the family-0 handler table, as well as by the\n"
         "  definition initialiser and the SetSaveData apply. §10.",
     "names it: ~~it is~~\n"
     "  ~~`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`,~~ the body reached by the script verb\n"
     "  **`resetJobs` (`05D6`)** through `00342230` and the family-0 handler table~~, as well as by the~~\n"
     "  ~~definition initialiser and the SetSaveData apply~~. It is not the gambit preset loader: its only caller is "
     "`00342230` (`00342242`), and it clears every equipment slot (`0031A260`, `00328C11`), un-learns licences with an "
     "LP refund through `00328990` twice (`00328C23`, `00328C35`; license-board-grid-format.md §3), rebuilds the stats "
     "(`0030FED0`, `00328C66`) and then calls the preset loader `00327CB0` (`00328CAA`) — the callee the definition "
     "initialiser and the SetSaveData apply share (its callers `0023AC80`, `00239960`) *(corrected 2026-10-02, OPUS: "
     "checked by `retool.py callers`)*. §10."),
    (ES, "`00328BD0` is `GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`, and the\n"
         "script verb **`resetJobs` (`05D6`)** reaches it through `00342230` and the family-0 handler table at\n"
         "`01EF91E0` — alongside the definition initialiser and the SetSaveData apply.",
     "`00328BD0` is ~~`GambitConfig_LoadAuthoredPresetAndRebuildRuntimeOrders`, and the~~ the `resetJobs` body: the\n"
     "script verb **`resetJobs` (`05D6`)** reaches it through `00342230` and the family-0 handler table at\n"
     "`01EF91E0` ~~— alongside the definition initialiser and the SetSaveData apply~~, its only caller (`00342242`); it "
     "strips the equipment, un-learns licences with an LP refund (`00328990`, twice) and rebuilds the gambits through "
     "its callee `00327CB0`, the preset loader that the definition initialiser and the SetSaveData apply call directly "
     "*(corrected 2026-10-02, OPUS: checked by `retool.py callers` and at `00328C11`–`00328CAA`; §7's item, corrected "
     "the same day)*."),

    # C9: refresh 0030B270 has one caller, the sale commit 00310870 at 003108ED; nothing re-runs it on reload.
    (CBZ, "- on reload, refresh runs over every row. For a row that is **not** repeatable",
     "- ~~on reload, refresh runs over every row.~~ on reload nothing recomputes the flag bytes: refresh `0030B270` has "
     "one caller, the sale commit `00310870` at `003108ED`, so it runs only after a sale and the loaded bytes stand "
     "*(corrected 2026-10-02, OPUS: checked by `retool.py callers 0030B270`; "
     "the-bazaar-recipe-unlock-and-purchase.md §2.3)*. When a later sale runs it: For a row that is **not** "
     "repeatable"),

    # C10: section 12 omits step 0, the 00322C50(0x12, id, 0) gate and its return (0030B194-0030B19F).
    (CBZ, "void Bazaar_Purchase(uint16_t goodId)\n{",
     "void Bazaar_Purchase(uint16_t goodId)   // <- corrected 2026-10-02, OPUS: returns int; section 7 step 0 is "
     "missing here - if (!00322C50(0x12, goodId, 0)) return 0; before anything is touched (0030B194-0030B19F)\n{"),

    # C11: the commits get (id, panel quantity +0xDC, total, 0) (0056D457-0056D49A, xor r9d, r9d).
    (BZ, "  -> Shop_CommitSaleItemAndGil(item, n, gil, flags)\n       -> 003008A0(item, -n",
     "  -> Shop_CommitSaleItemAndGil(item, n, gil, flags)   <- corrected 2026-10-02, OPUS: (id, qty, total, 0) - the "
     "fourth argument is a literal 0 (0056D457 xor r9d, r9d), so no gil line\n       -> 003008A0(item, -n"),
    (BZ, "  -> Shop_CommitPurchaseItemAndGil(good, 1, price, flags)\n       -> 003008A0(good, 1",
     "  -> Shop_CommitPurchaseItemAndGil(good, 1, price, flags)   <- corrected 2026-10-02, OPUS: (good, qty, total, 0) "
     "- qty is the panel's word +0xDC, total = (price & 0x7FFFFFFF) x qty, the fourth argument 0 (0056D457-0056D49A); "
     "section 7, UQ-131\n       -> 003008A0(good, 1"),

    # C12: counter 19 fires on every purchase; the 0x2C0 test skips only call 0030B630 (0056D4AC-0056D4D2).
    (BZ, "`BattleIdClassD_SetRuntimeFlagBit2(id, 0)` (`0056D4AC`–`0056D4C0`). Then:\n"
         "        - a purchase calls the 411-byte achievement routine with id `0x13` and the good;",
     "`BattleIdClassD_SetRuntimeFlagBit2(id, 0)` (`0056D4AC`–`0056D4C0`). ~~Then:~~ That test guards only this call; "
     "the rest runs in every mode *(corrected 2026-10-02, OPUS: checked at `0056D4AC`–`0056D4D2` — the `0x2C0` test "
     "skips only `call 0030B630`, and `cl = 0x13` / `call 00316A50` runs on every purchase; the PlatformOnline"
     "Achievements crossing below)*:\n"
     "        - a purchase, bazaar or not, calls the 411-byte achievement routine with id `0x13` and the good;"),

    # C13: the pointer-decode base is 01F83530 (0020E602 add rax, qword ptr [01F83530]).
    (CBZ, "  `ref + *(01F85530)` (`0020E602`), so a zero",
     "  ~~`ref + *(01F85530)`~~ `ref + *(01F83530)` (`0020E602`) *(corrected 2026-10-02, OPUS: checked at `0020E602` "
     "`add rax, qword ptr [01F83530]`)*, so a zero"),
    (CBZ, "and `0020E600` is `ref + *(01F85530)`, so the",
     "and `0020E600` is ~~`ref + *(01F85530)`~~ `ref + *(01F83530)` *(corrected 2026-10-02, OPUS: `0020E602`)*, so "
     "the"),

    # C14: 00317B20's table is rooted at [02EBF190] + 8 (00317B36-00317B41).
    (IE, "same `02EBF183`-rooted table, but",
     "same ~~`02EBF183`-rooted~~ table, rooted at `[02EBF190] + 8` with stride `0x1C8` *(corrected 2026-10-02, OPUS: "
     "checked at `00317B36`–`00317B41` `mov rax, [02EBF190]` / `add rax, 8`; `02EBF183` is not even pointer-aligned)*, "
     "but"),

    # C15: the node table holds 360 records (32 + 360 * 24 = 8672), so 360 bits can be granted.
    (CLC, "`uint8[46]`, **node ids 0..360, so 361 of the 368 bits are spoken for**. The",
     "`uint8[46]`, ~~**node ids 0..360, so 361 of the 368 bits are spoken for**~~ **the boards use node ids 0..360, "
     "but the node table holds 360 records, ids 0..359, so 360 bits can be granted**; bit 360 is set only by a save "
     "image that already carries it *(corrected 2026-10-02, OPUS: license-board-grid-format.md §2.3, "
     "`32 + 360 * 24 = 8672` on the four shipped `license_data.bin` copies; "
     "license-check-what-the-board-actually-tests.md §11)*. The"),

    # C16: three classes (5, 7, 11) have itemCount 0, not two.
    (CIN, "**Two of the fifteen answers are \"it does\n"
          "not work\", and four more classes declare items with no storage behind them.**",
     "**~~Two~~ Three of the fifteen answers are \"it does\n"
     "not work\", and four more classes declare items with no storage behind them.** *(corrected 2026-10-02, OPUS: "
     "descriptor `+0x3C` is 0 on rows 5, 7 and 11, §10; the four storage-less classes 9, 10, 13 and 14 still grant "
     "through their `+0x48` handlers)*"),

    # C17: the rebase 0030B6A0 binds +0x08 / +0x20 / +0x30 (C-IN 3; TSV rows 4, 11, 14).
    (CIN, "- **Who binds `+0x08`, `+0x20` and `+0x30` at runtime, and from where.** Routed as",
     "- ~~**Who binds `+0x08`, `+0x20` and `+0x30` at runtime, and from where.**~~ *(answered: see §3 — the rebase "
     "pass `0030B6A0` binds them, run from the state block's first bind `00233C10` and the save rebind `00238A80`; "
     "item-class-descriptor-accesses.tsv, its `+0x08`, `+0x20` and `+0x30` rows; 2026-10-02, OPUS)* Routed as"),

    # C18: the 2026-09-26 replay ran the +-1 entry and both mutators (C-IN 13, 16 / 16).
    (CIN, "**What did not:** both mutators, the clear-all and the ±1 entry — they dispatch through the function\n"
          "pointer at descriptor `+0x50`, which is a different shape and a different fixture. Said here rather",
     "**What did not:** ~~both mutators, the clear-all and the ±1 entry — they dispatch through the function~~\n"
     "~~pointer at descriptor `+0x50`, which is a different shape and a different fixture.~~ *(answered: see the "
     "supersession directly below — on 2026-09-26 the ±1 entry `003008A0` and both mutators ran as native replay, "
     "16 / 16; they dispatch through descriptor `+0x48`, not `+0x50` (`00300943`–`00300960`); only the clear-all "
     "`003047F0` has not run; 2026-10-02, OPUS)* Said here rather"),
    (CIN, "for the **three read entry points**, which is why so many rows below are not exercised.",
     "for the **three read entry points**~~, which is why so many rows below are not exercised~~ *(answered: see §13's "
     "supersession of 2026-09-26 — the ±1 entry, the query entry and all four storage handlers have since run as "
     "native replay, 16 / 16; 2026-10-02, OPUS)*."),
    (CIN, "in `002FD150`, which this pilot does not execute | 1 (static) | PROVEN |",
     "in `002FD150`, ~~which this pilot does not execute~~ executed since by the 2026-09-26 replay, whose "
     "postcondition holds over 168 mutates *(answered: see §13; 2026-10-02, OPUS)* | 1 (static) | PROVEN |"),

    # C19: IE's body banner against its own front matter (AUDITED).
    (IE, "**PARTIAL.** The ID encoding and the compatibility test are read at tier 1. The full category\n"
         "enumeration and the comparison/optimise logic are not.",
     "~~**PARTIAL.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter says `status: AUDITED`)*. The ID "
     "encoding and the compatibility test are read at tier 1. ~~The full category~~\n"
     "~~enumeration and the comparison/optimise logic are not.~~ The full category enumeration and the comparison / "
     "Optimise logic are read too (§7, P-1 and P-4; §3, the `002F9F20` row)."),

    # C20: the three Optimise functions are read (IE 3: P-4 2026-09-12, 002F9F20 2026-09-18).
    (IE, "  -> Equipment_BuildRecommendedLoadoutForMappedStats     (not read)\n"
         "     -> Equipment_SelectPreferredCandidateByAuthoredStats (not read)\n"
         "        -> Equipment_ComputeComparisonMetricWithCompatiblePartner (not read)",
     "  -> Equipment_BuildRecommendedLoadoutForMappedStats     (not read)   <- corrected 2026-10-02, OPUS: read "
     "2026-09-18 (section 3)\n"
     "     -> Equipment_SelectPreferredCandidateByAuthoredStats (not read)   <- corrected 2026-10-02, OPUS: read, P-4, "
     "2026-09-12 (section 3)\n"
     "        -> Equipment_ComputeComparisonMetricWithCompatiblePartner (not read)   <- corrected 2026-10-02, OPUS: "
     "read, P-4, 2026-09-12 (section 3)"),
    (IE, "**Scope honesty.** Only two of this category's functions were read. The \"Optimise\" behaviour —\n"
         "which most players would consider the interesting part — sits in three unread functions and is\n"
         "recorded as **P-4** rather than guessed at from their names.",
     "**Scope honesty.** ~~Only two of this category's functions were read. The \"Optimise\" behaviour —~~\n"
     "~~which most players would consider the interesting part — sits in three unread functions and is~~\n"
     "~~recorded as **P-4** rather than guessed at from their names.~~ *(answered: see §3 and §7 — the three Optimise "
     "functions `002F9F20`, `002F7A10` and `002F7C80` are read, P-4 answered 2026-09-12 and the builder 2026-09-18; "
     "2026-10-02, OPUS)*"),

    # C21: P-2 was answered 2026-09-12 (IE 7).
    (IE, "is still not established — **P-2 stays\nopen** — but the direction",
     "~~is still not established — **P-2 stays~~\n~~open**~~ *(answered: see §7, P-2 ANSWERED 2026-09-12 — `+0x09` "
     "is the item's own equipment class and `+0x11` the class the other slot's item must carry; 2026-10-02, OPUS)* — "
     "but the direction"),

    # C22: 002FD880 is read (IE 7, P-5; checked at 002FD880-002FD8C5).
    (IE, "| `002FD880` | `InventoryEncodedGilClass0E_ApplyGilDelta` | not read |",
     "| `002FD880` | `InventoryEncodedGilClass0E_ApplyGilDelta` | ~~not read~~ read: adds `(id & 0xFFF) × delta` gil, "
     "the id is the amount *(answered: see §7, P-5; checked at `002FD880`–`002FD8C5`; 2026-10-02, OPUS)* |"),

    # C23: the non-weapon +0x18 / +0x19 bytes are named in ES 6.1 (and grouped by 0031E9A0).
    (IE, "(`002F7B15`–`002F7B76`; what the two bytes are on non-weapon rows this page\n      has not named — on weapon",
     "(`002F7B15`–`002F7B76`; ~~what the two bytes are on non-weapon rows this page~~\n      ~~has not named~~ "
     "*(answered: see equipment-slots-and-the-single-stat-rebuild.md §6.1 — a shield's evade and magick evade; a "
     "helmet's, armour's or accessory's defence and magick resist, grouped by `0031E9A0`, checked at "
     "`0031E9A0`–`0031E9DF`; 2026-10-02, OPUS)* — on weapon"),

    # C24: 002F9F20 is 435 B (ret at 002FA0D2); 212 B is 002F7EC0.
    (IE, "(`Equipment_BuildRecommendedLoadoutForMappedStats`, ~212 B) —",
     "(`Equipment_BuildRecommendedLoadoutForMappedStats`~~, ~212 B~~, 435 B *(corrected 2026-10-02, OPUS: its `ret` "
     "is at `002FA0D2`; 212 B is `002F7EC0`'s size; CONTRACT-equipment-compatibility.md §2)*) —"),

    # C25: IE's slot-1 bound was corrected 2026-09-22 to 0x11A3.
    (CEQ, "The item-id page's §3 lists slot 1 as\n`0x10C8`..`0x10DB` — the value that would make the four ranges "
          "contiguous — while",
     "The item-id page's §3 ~~lists~~ listed slot 1 as\n`0x10C8`..`0x10DB` — the value that would make the four ranges "
     "contiguous — *(answered: corrected there 2026-09-22 to `0x10C8`..`0x11A3`; see "
     "item-id-encoding-and-equipment-compatibility.md §3, the `002F9F20` row; 2026-10-02, OPUS)* while"),

    # C26: +0x1E categories are tabulated over all 543 rows (IU 9).
    (IU, "- **Whether any category other than 3 exists at `+0x1E`**, and what it means.",
     "- ~~**Whether any category other than 3 exists at `+0x1E`**, and what it means.~~ *(answered: see §9's "
     "falsification pass, \"`+0x1E` is a category that selects `+0x22`'s id space\" — 1 magick, 2 technick, 3 item, "
     "5 / 6 nibble `C`, 255 retired, over all 543 rows; 2026-10-02, OPUS)*"),

    # C27: the third / fourth / fifth arguments are decoded (C-BZ 13a; IU 11).
    (IU, "are passed as constants\n  that were not traced. The \"discovery state\"",
     "are passed as constants\n  ~~that were not traced~~ *(answered: the third is the absolute / relative "
     "selector, 0 = relative, the fourth the channel, 1 = owned, and the fifth is 0 — "
     "CONTRACT-bazaar-unlock-and-purchase.md §13a, \"`(loot, 0, 1, 3)` decoded\", and §11's evidence table; 2026-10-02, "
     "OPUS)*. The \"discovery state\""),

    # C28: ES's banner and GR-12 (answered 2026-09-30, ES front matter and 11.3).
    (ES, "**PARTIAL.** The slot model, the equip path and the complete set of rebuild triggers are read at",
     "~~**PARTIAL.**~~ **AUDITED** *(corrected 2026-10-02, OPUS: the front matter's status; GR-12 answered "
     "2026-09-30)*. The slot model, the equip path and the complete set of rebuild triggers are read at"),
    (ES, "its formula is written out in §6; the one item still open is what the\n"
         "battle menu's two equip-branch actions `0x9C` / `0x9D` do (§11.3, `GR-12`).*",
     "its formula is written out in §6; ~~the one item still open is what the~~\n"
     "~~battle menu's two equip-branch actions `0x9C` / `0x9D` do (§11.3, `GR-12`).~~* *(answered: see §11.3 — "
     "`GR-12` ANSWERED 2026-09-30, actions `0x9C` / `0x9D` do nothing; 2026-10-02, OPUS)*"),
    (ES, "- **What battle actions `0x9C` and `0x9D` do** — the two the battle menu issues",
     "- ~~**What battle actions `0x9C` and `0x9D` do**~~ *(answered: see §11.3 — `GR-12` ANSWERED 2026-09-30, "
     "neither action does anything; 2026-10-02, OPUS)* — the two the battle menu issues"),
    (ES, "The authored order table is answered in §11.4. The command ids remain `GR-12`\n(§11.3).",
     "The authored order table is answered in §11.4. ~~The command ids remain `GR-12`~~\n~~(§11.3).~~ *(answered: "
     "`GR-12` is ANSWERED 2026-09-30 — the two command ids do nothing, §11.3; 2026-10-02, OPUS)*"),

    # C29: old is captured before the store (0031A68E); the slot is re-read after reconciliation (0031A6BB).
    (ES, "Note the comparison is against `old`, re-read *after* reconciliation, so the test is",
     "Note the comparison is against `old`, ~~re-read *after* reconciliation~~ captured *before* the store "
     "(`0031A68E`), against the slot re-read after reconciliation (`0031A6BB`) *(corrected 2026-10-02, OPUS: §10, "
     "the falsification pass)*, so the test is"),

    # C30: the preview diffs five slots (0030A565-0030A5BA).
    (ES, "`[rbp+0x50/0x52/0x54]` in `0030A4E0` | 1 |",
     "~~`[rbp+0x50/0x52/0x54]` in `0030A4E0`~~ `+0x50` … `+0x58`, all five, in `0030A4E0` (`0030A565`–`0030A5BA`) "
     "*(corrected 2026-10-02, OPUS: §10, \"the preview diffs five slots, not three\")* | 1 |"),

    # C31: 002F8FA0 is read (LC 6 and its 2026-09-27 qualification; C-LC 13).
    (LC, "**Not claimed:** §4's `LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`, 287 B) was\n"
         "not read, so *what* requirement mask a kind and id produce is untouched.",
     "**Not claimed:** ~~§4's `LicenseData_BuildPrerequisiteNodeMaskForRequirement` (`002F8FA0`, 287 B) was~~\n"
     "~~not read, so *what* requirement mask a kind and id produce is untouched.~~ *(answered: see §6 and its "
     "2026-09-27 qualification — `002F8FA0` is read whole, and CONTRACT-license-check.md §13 re-reads it statically; "
     "2026-10-02, OPUS)*"),

    # C32: bits 0-17 feed only the Quickening count in the shipped tables (C-LC 14).
    (LC, "- **What License bits 0–17 are**, beyond that their popcount gates Quickenings (§5).",
     "- ~~**What License bits 0–17 are**, beyond that their popcount gates Quickenings (§5).~~ *(answered for the "
     "shipped tables: see CONTRACT-license-check.md §14 — licence records 0–17 list no id, the action mask builder "
     "never sets those bits over all 543 ability ids, and party rows 0–5 name exactly the 18 Quickenings "
     "`0xD0`–`0xE1`; whether the board can grant four of them to one record stays open; 2026-10-02, OPUS)*"),
    (LC, "**What is not established here:** whether bits 0–17 are exclusively the Quickening squares, and what",
     "**What is not established here:** ~~whether bits 0–17 are exclusively the Quickening squares,~~ *(answered "
     "for the shipped tables: CONTRACT-license-check.md §14 — bits 0–17 do nothing but feed this count; 2026-10-02, "
     "OPUS)* and what"),
    (LC, "§5's open item — whether\nbits 0–17 are exclusively Quickening squares — stands.",
     "~~§5's open item — whether~~\n~~bits 0–17 are exclusively Quickening squares — stands.~~ *(answered for the "
     "shipped tables: CONTRACT-license-check.md §14; 2026-10-02, OPUS)*"),

    # C33: 00322C50 is (class, id), a bounds check of the id (LC 9, "Both gates are passed the id").
    (LC, "- **What `00322C50(class)` tests.** It is a 1,025-byte shared validator; the action path passes",
     "- ~~**What `00322C50(class)` tests.**~~ *(answered: see §9's falsification pass, \"Both gates are passed the "
     "id\" — it is `00322C50(class, id)`, a bounds check of this id: class 20 admits `0 ≤ id < count` of the action "
     "table, class 1 derives the id's class; 2026-10-02, OPUS)* It is a 1,025-byte shared validator; the action path "
     "passes"),
    (LC, "  observed play state reaches. **Read as a gate, not understood.**",
     "  observed play state reaches. ~~**Read as a gate, not understood.**~~ *(answered: §9; 2026-10-02, OPUS)*"),

    # C34: the shipped node table is 360 records of 24 bytes (LB 2.3).
    (LC, "- **The live node count and stride** — both runtime-loaded; the image holds only the descriptor.",
     "- ~~**The live node count and stride** — both runtime-loaded; the image holds only the descriptor.~~ "
     "*(answered: see license-board-grid-format.md §2.3 — the shipped `license_data.bin` holds 360 records of 24 "
     "bytes, `32 + 360 * 24 = 8672`; 2026-10-02, OPUS)*"),

    # C35: 00324020 is a loop of three passes over six bits (C-LC 15).
    (LC, "(`00324020`) is an unrolled popcount over the **same",
     "(`00324020`) is ~~an unrolled popcount~~ a loop of three passes over six bits *(corrected 2026-10-02, OPUS: "
     "`lea edi, [r9+3]` / `sub rdi, 1` / `jne 00324040`; CONTRACT-license-check.md §15)* over the **same"),

    # C36: the grid has readers (LB 3, corrected 2026-09-13; LB 7).
    (LB, "**the location contract is complete and the parse contract is\nempty.** Opened as "
         "**PROPOSED-repos-c7-11**.",
     "**the location contract is complete and ~~the parse contract is~~\n~~empty.~~** Opened as "
     "**PROPOSED-repos-c7-11**. *(answered: see the correction at the top of this subsection, 2026-09-13 — the header "
     "is read by `0055B3F0` and the cells by six readers, `00328990`, `0055E2C0`, `0055E600`, `00560070`, `0055F830` "
     "and `003FC900`; §7; 2026-10-02, OPUS)*"),

    # C37: 00315390 is 94 B (ret at 003153ED); 289 B is 00316480.
    (ST, "`00315390` (~289 B) — `002536A0()`",
     "`00315390` ~~(~289 B)~~ (94 B *(corrected 2026-10-02, OPUS: its `ret` is at `003153ED`; §3; 289 B is "
     "`00316480`'s size)*) — `002536A0()`"),

    # C38: +0x22 is the good's icon frame (UQ-130 answered 2026-09-17).
    (BZ, "| `+0x22` | u16 | 120 on every shipped row; no reader found | — |",
     "| `+0x22` | u16 | 120 on every shipped row; ~~no reader found~~ the good's icon frame, read by `0057AC10`, "
     "`0057B1A0`, `003F41C0` and `0057DC30` *(answered: see §7, UQ-130 ANSWERED 2026-09-17; 2026-10-02, OPUS)* | — |"),

    # C39: front-matter entries: 0030B1D0 / 0030B33F are interior (C-BZ 2). YAML line: trailing comment, no strike.
    (CBZ, "entries: [\"0030B1D0\", \"0030B33F\", \"0030B570\", \"003008A0\", \"003108ED\"]\nverified_against:",
     "entries: [\"0030B1D0\", \"0030B33F\", \"0030B570\", \"003008A0\", \"003108ED\"]  # <- corrected 2026-10-02, "
     "OPUS: per section 2, 0030B1D0 is 0x50 into the purchase entry 0030B180 and 0030B33F is the loop body of the "
     "refresh entry 0030B270; 003108ED is the refresh call site inside the sale commit 00310870\nverified_against:"),

    # C40: 0030B270 IS BattleIdClassD_RefreshPrerequisiteRuntimeFlags; its caller is 00310870 at 003108ED.
    (CBZ, "called only from `BattleIdClassD_RefreshPrerequisiteRuntimeFlags` `003108ED`. `0030B33F`",
     "called only from ~~`BattleIdClassD_RefreshPrerequisiteRuntimeFlags`~~ the sale commit "
     "`Shop_CommitSaleItemAndGil` (`00310870`), at `003108ED`. *(corrected 2026-10-02, OPUS: `retool.py callers "
     "0030B270`; `0030B270` is itself `BattleIdClassD_RefreshPrerequisiteRuntimeFlags`, "
     "the-bazaar-recipe-unlock-and-purchase.md §2.3–§2.4)* `0030B33F`"),

    # C41: the claim table's rows marked isolated original-code were executed (C-BZ 13).
    (CBZ, "**Nothing here has been executed** (§13). Two rows are cited",
     "~~**Nothing here has been executed** (§13).~~ *(answered: see §13 — the twenty-ninth differential pilot of "
     "2026-09-12 ran the three entry points as shipped bytes, 297 lines, and the rows below marked \"isolated "
     "original-code\" are executed; nothing is observed live; 2026-10-02, OPUS)* Two rows are cited"),

    # C42: the loaded flag bytes and tallies were observed after a live load (BZ 7, FZ-3, ASTRA 2026-09-21).
    (CBZ, "Not established. What would be observable: a one-time good bought",
     "~~Not established.~~ *(answered in part: see the-bazaar-recipe-unlock-and-purchase.md §7, FZ-3 — an older "
     "`FFXII_004` loaded in a live process brought both regions back full, 18 nonzero flag bytes and 44 nonzero "
     "loot-sold counters, each matching the file's decoding (ASTRA, 2026-09-21); the purchase round trip below is "
     "still unobserved; 2026-10-02, OPUS)* What would be observable: a one-time good bought"),

    # C43: README labels against the pages' own front matter, and the nine pages it omitted.
    (R, "  **PARTIAL, tier 1.** The 57-shop table",
     "  ~~**PARTIAL, tier 1.**~~ **DOCUMENTED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: DOCUMENTED`)*. The 57-shop table"),
    (R, "  **PARTIAL, tier 1.** The 128-row bazaar table",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. The 128-row bazaar table"),
    (R, "  **PARTIAL, tier 1.** Item IDs encode",
     "  ~~**PARTIAL, tier 1.**~~ **AUDITED, tier 1** *(corrected 2026-10-02, OPUS: the page's front matter says "
     "`status: AUDITED`)*. Item IDs encode"),
    (R, "one byte compared against another** — asymmetrically.\n\nDocumented adjacency",
     "one byte compared against another** — asymmetrically.\n"
     "- [`CONTRACT-inventory-class-storage.md`](CONTRACT-inventory-class-storage.md) — the fifteen class descriptors "
     "and their packed and bitset storage — **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`CONTRACT-equipment-compatibility.md`](CONTRACT-equipment-compatibility.md) — equip eligibility and the "
     "pairing byte, EQ-1 to EQ-8 — **CONTRACT READY**\n"
     "- [`equipment-slots-and-the-single-stat-rebuild.md`](equipment-slots-and-the-single-stat-rebuild.md) — the five "
     "slots, the setter and the stat rebuild `002FEF30` — **AUDITED**\n"
     "- [`using-an-item-is-an-action-that-costs-an-item.md`](using-an-item-is-an-action-that-costs-an-item.md) — "
     "prepare, consume and refund of an item action — **AUDITED**\n"
     "- [`license-check-what-the-board-actually-tests.md`](license-check-what-the-board-actually-tests.md) — the "
     "licence check for actions and equipment — **AUDITED**\n"
     "- [`CONTRACT-license-check.md`](CONTRACT-license-check.md) — **BEHAVIORALLY UNDERSTOOD**\n"
     "- [`license-board-grid-format.md`](license-board-grid-format.md) — the `licd` board files and their readers — "
     "**AUDITED**\n"
     "- [`CONTRACT-shop-stock-ladders.md`](CONTRACT-shop-stock-ladders.md) — the shop gate walk, SG-1 to SG-7 — "
     "**CONTRACT READY**\n"
     "- [`CONTRACT-bazaar-unlock-and-purchase.md`](CONTRACT-bazaar-unlock-and-purchase.md) — "
     "**BEHAVIORALLY UNDERSTOOD**\n"
     "- *(nine pages added to this list 2026-10-02, OPUS, each with the status its own front matter states)*\n"
     "\nDocumented adjacency"),

    # F1 (2.5): the rebaser also zeroes the 512 tally bytes at +0x57C8 before the flag mask (0030B702-0030B737).
    (BZ, "masks all 128 bytes\nwith `0xF8` (`0030B739`–`0030B75B`) when the block is bound",
     "masks all 128 bytes\nwith `0xF8` (`0030B739`–`0030B75B`), having first zeroed the 512 loot-sold tally bytes "
     "at `+0x57C8` (`0030B702`–`0030B737`) *(corrected 2026-10-02, OPUS: checked at `0030B702`–`0030B737`; "
     "CONTRACT-bazaar-unlock-and-purchase.md §14 states it)*, when the block is bound"),
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
