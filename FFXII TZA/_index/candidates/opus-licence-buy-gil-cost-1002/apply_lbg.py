"""apply_lbg.py [--apply] - buying a licence square (00323D10) and the action gil cost (00309060), with the
statements those reads overturn, settled on the pages (OPUS, 2026-10-02).

Facts the edits rest on (checked at the bytes / shipped data):
  F1  the licence node table the game checks is 02EBF038, bound only by 00236C30 (00236D5C-00236D67) from the
      battle_pack.bin blob (0208E680) directory +0x34: an st2e table of 361 records of 24 bytes in all nine
      language copies; 00322C50 reads its count [02EBF038]+4 (00322FCB-00322FD9); the license_data.bin path
      strings 00A400B8 / 00C19F18 have no code reference. Node 360 passes the range check; its gate is the
      presence bit 0xC01F (00323E88).
  F2  00323D10(stats, node, flags) returns a reason code (0 = can take) and writes nothing.
  F3  00309060(unit, actionId) is the action gil cost, 10 * trunc(row.b+0x0A * 64.0 / 50.0) under its gates;
      unit+0xE58 is the cost reserved for the action in progress, not a purse.

Each edit strikes only the wrong words (every ~~ span opens and closes on one line, struck text verbatim) and
restates them, tagged *(corrected 2026-10-02, OPUS: ...)* or *(answered: see ...; 2026-10-02, OPUS)*.
The same-day correction on CONTRACT-license-check.md section 3 was itself wrong and is struck and restated.
No code-block lines, no table column changes, no heading changes. Two sections are inserted, each only when its
heading is absent, before an anchor heading that occurs exactly once on its page.
Exact substrings, each once; tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
HERE = os.path.dirname(os.path.abspath(__file__))
F = "12-Items-Equipment-Shops-License/"
LC = F + "license-check-what-the-board-actually-tests.md"
CLC = F + "CONTRACT-license-check.md"
LB = F + "license-board-grid-format.md"
IU = F + "using-an-item-is-an-action-that-costs-an-item.md"
AS = "10-Status-Periodic-Terminal/CONTRACT-auto-status-rebuild.md"
GS = "13-Rewards-Progression-Economy/gil-storage-clamp-and-every-path-that-moves-it.md"
BC = "07-Combat-Action/Action-Availability/battle-command-availability-and-reason-codes.md"

# F1, as a tag reason
R1 = ("the node table the game checks is `02EBF038`, bound only by `00236C30` at `00236D5C`–`00236D67` from the "
      "`battle_pack.bin` blob (`0208E680`) directory `+0x34`, an `st2e` table of 361 records of 24 bytes in all nine "
      "language copies; `00322C50` reads its count `[02EBF038]+4` (`00322FCB`–`00322FD9`); the `license_data.bin` "
      "path strings `00A400B8` and `00C19F18` have no code reference, so the standalone 360-record files are not what "
      "the game loads")
# F3, as a tag reason
R3 = ("`+0xE58` is the gil cost reserved for the action in progress, not a purse: `0030EFC0` stores `00309060`'s "
      "result there, the refund `00300280` adds it back and the consume path `00305640` clears it; "
      "04-Actor-Entity/Battle-Unit/the-battle-unit-field-map.md:234; using-an-item-is-an-action-that-costs-an-item.md, "
      "\"The action gil cost: 00309060\"")
SEC_LC = "the section \"13. Buying a licence square: 00323D10\""
SEC_IU = "the section \"The action gil cost: 00309060\""

EDITS = [
    # OPUS: the menu guard at 0055D9B1 tests the cursor square's node id, not a record count; node 360 still reaches
    # the grant 003235C0 at 0055DA6E (word +8 is passed as the node, 0055DA6A).
    (LC, "the body loads the record count `[rcx+8]` and compares\n"
         "  it to `0x168`; on the stock count it substitutes the sentinel pair `0x1690169`",
     "the body loads ~~the record count~~ the cursor square's node id `[rcx+8]` and compares\n"
     "  it to `0x168`; ~~on the stock count~~ for node 360 it substitutes the sentinel pair `0x1690169` *(corrected "
     "2026-10-02, OPUS: word `+8` is the node the grant receives, `0055DA6A` passes it to `003235C0` at `0055DA6E`, "
     "and node 360 still reaches that grant, where `00323D10` gates it on bit `0xC01F`)*"),
    # ---- node 360: the loaded table has 361 records (F1) ----
    # CONTRACT-license-check section 3: today's correction was wrong; the original statement was right.
    (CLC,
     "~~**node ids 0..360, so 361 of the 368 bits are spoken for**~~ **the boards use node ids 0..360, but the node "
     "table holds 360 records, ids 0..359, so 360 bits can be granted**; bit 360 is set only by a save image that "
     "already carries it *(corrected 2026-10-02, OPUS: license-board-grid-format.md §2.3, `32 + 360 * 24 = 8672` on "
     "the four shipped `license_data.bin` copies; license-check-what-the-board-actually-tests.md §11)*. The",
     "~~**node ids 0..360, so 361 of the 368 bits are spoken for**~~ ~~**the boards use node ids 0..360, but the node "
     "table holds 360 records, ids 0..359, so 360 bits can be granted**; bit 360 is set only by a save image that "
     "already carries it *(corrected 2026-10-02, OPUS: license-board-grid-format.md §2.3, `32 + 360 * 24 = 8672` on "
     "the four shipped `license_data.bin` copies; license-check-what-the-board-actually-tests.md §11)*~~ **node ids "
     "0..360, so 361 of the 368 bits are spoken for**: the node table the game loads holds 361 records, ids 0..360, "
     "and node 360 passes the range check; the square is refused with reason 8 until presence bit `0xC01F` is set "
     "*(corrected 2026-10-02, OPUS: the same-day correction struck here was wrong - " + R1 + "; the 360 records are "
     "the standalone file's; the `0xC01F` test is at `00323E88`, license-check-what-the-board-actually-tests.md "
     + SEC_LC + ")*. The"),

    # license-board-grid-format section 2.3: the 360 records are the standalone file's.
    (LB,
     "So the node table holds **360 records, valid indices `0 … 359`** — and the boards use **361**\n"
     "distinct values. **The id space is one larger than the table it indexes**, and §5 shows that the",
     "So ~~the node table~~ `license_data.bin` holds **360 records, valid indices `0 … 359`** — and the boards use "
     "**361**\n"
     "distinct values. ~~**The id space is one larger than the table it indexes**~~ **The id space is one larger than "
     "this file, and exactly the size of the node table the game loads** *(corrected 2026-10-02, OPUS: " + R1 + ")*, "
     "and §5 shows that the"),

    # license-board-grid-format section 5 table: out of range of the file only.
    (LB,
     "| out of range of the node table | `license_data.bin` holds **360** records, valid `0…359`; **360 is not one of "
     "them** |",
     "| ~~out of range of the node table~~ out of range of `license_data.bin`, not of the table the game loads | "
     "`license_data.bin` holds **360** records, valid `0…359`; **360 is not one of them**; the node table the game "
     "checks, `02EBF038`, holds 361, and node 360 is its only category-`0x1E` row *(corrected 2026-10-02, OPUS: "
     + R1 + ")* |"),

    # license-board-grid-format section 5: "out of the table's range".
    (LB,
     "It is out of the table's range, present once on every job",
     "~~It is out of the table's range,~~ It is out of `license_data.bin`'s range but in range of the table the game "
     "loads, where it is the only category-`0x1E` square, gated by presence bit `0xC01F` (`00323E88`) *(corrected "
     "2026-10-02, OPUS: " + R1 + ")*, present once on every job"),

    # license-board-grid-format section 5, OPUS-NOTICE-NODE360 paragraph: the conclusion about what is loaded.
    (LB,
     "So every language of this build loads a 360-record table under 361-node boards, and the grant path\n"
     "refuses the square (the licence-check page §11): the id space is the size of the largest table\n"
     "shipped, and the tables actually loaded are one record short of it. On the `in` job boards the",
     "~~So every language of this build loads a 360-record table under 361-node boards, and the grant path~~\n"
     "~~refuses the square (the licence-check page §11):~~ No language loads the standalone file into the node "
     "table, and the grant path does not refuse the square on range: the id space is the size of the largest table\n"
     "shipped~~, and the tables actually loaded are one record short of it~~, and that 361-record table is the one "
     "loaded *(corrected 2026-10-02, OPUS: " + R1 + "; node 360 passes `00322C50`'s range check and is gated by "
     "presence bit `0xC01F` at `00323E88`, the licence-check page's " + SEC_LC + ")*. On the `in` job boards the"),

    # license-check section 11: today's answer named the standalone file as the live table.
    (LC,
     "image holds only the descriptor.~~ *(answered: see license-board-grid-format.md §2.3 — the shipped "
     "`license_data.bin` holds 360 records of 24 bytes, `32 + 360 * 24 = 8672`; 2026-10-02, OPUS)*",
     "image holds only the descriptor.~~ ~~*(answered: see license-board-grid-format.md §2.3 — the shipped "
     "`license_data.bin` holds 360 records of 24 bytes, `32 + 360 * 24 = 8672`; 2026-10-02, OPUS)*~~ *(answered: the "
     "live table `02EBF038` holds 361 records of 24 bytes, the `st2e` section at `battle_pack.bin` directory `+0x34`; "
     "the image's descriptor carries the count `+4`, the `u16` stride `+8` and the row handle `+0xC`; see "
     + SEC_LC + " below; 2026-10-02, OPUS)* *(corrected 2026-10-02, OPUS: " + R1 + ")*"),

    # license-check section 11: "node 360 cannot be granted".
    (LC,
     "  menu (`0055CD40` → `BattleStats_SetLicenseNodeStateByStatsIndex` `003235C0`). **So node 360 —\n"
     "  present on every job board — cannot be granted with the 360-record table every language of this\n"
     "  build loads** (the grid page §5); the auto-status rebuild's read of row 360 is unreachable from\n"
     "  the game. Two residuals: a save image whose bitmap already carries bit 360 (whether the save-side\n"
     "  copy masks bits beyond the count is unread), and the menu's own row lookup for the square under",
     "  menu (`0055CD40` → `BattleStats_SetLicenseNodeStateByStatsIndex` `003235C0`). ~~**So node 360 —~~\n"
     "  ~~present on every job board — cannot be granted with the 360-record table every language of this~~\n"
     "  ~~build loads** (the grid page §5); the auto-status rebuild's read of row 360 is unreachable from~~\n"
     "  ~~the game. Two residuals: a save image whose bitmap already carries bit 360 (whether the save-side~~\n"
     "  ~~copy masks bits beyond the count is unread), and~~ **Node 360, present on every job board, passes this "
     "range check**: the table the game loads holds 361 records, so the auto-status rebuild's read of row 360 is in "
     "range, and the square, the only category-`0x1E` row, is gated by presence bit `0xC01F`, tested by `00323D10` "
     "at `00323E88` (" + SEC_LC + " below) *(corrected 2026-10-02, OPUS: " + R1 + ")*. The one residual is the "
     "menu's own row lookup for the square under"),

    # CONTRACT-auto-status-rebuild section 10: the row-360 read is in range.
    (AS,
     "  `cmp ebp, 0x169`. Since the id space is 361 and `license_data.bin` declares 360 records, a set bit\n"
     "  for node 360 reads one record past the end. **Whether that bit is reachable is open**",
     "  `cmp ebp, 0x169`. Since the id space is 361 and ~~`license_data.bin` declares 360 records, a set bit~~\n"
     "  ~~for node 360 reads one record past the end.~~ so is the table this loop indexes, a set bit for node 360 "
     "reads that table's last row, in range: `license_data.bin` declares 360 records, but the game does not load it "
     "into `02EBF038` *(corrected 2026-10-02, OPUS: " + R1 + ")*. **Whether that bit is reachable is open** — the "
     "grant refuses node 360 with reason 8 until presence bit `0xC01F` is set (`00323E88`; "
     "license-check-what-the-board-actually-tests.md, " + SEC_LC + "), and what sets that bit is not traced"),

    # ---- stale "unread" claims (F2, F3) ----
    (LC,
     "  cannot read past the table.** `00323D10` remains unread.",
     "  cannot read past the table.** ~~`00323D10` remains unread.~~ *(answered: see " + SEC_LC + " below - it "
     "returns a reason code, 0 when the square may be taken, and writes nothing; 2026-10-02, OPUS)*"),
    (IU,
     "- **What `FUN_00309060` computes** as the gil cost of an action.",
     "- ~~**What `FUN_00309060` computes** as the gil cost of an action.~~ *(answered: see " + SEC_IU + " below - "
     "`10 × trunc(row.b[+0x0A] × 64.0 / 50.0)` for a kind-0 record whose status effect 32 is set, an id up to "
     "`0x21E` and a row category other than 5 or 6, else 0; 2026-10-02, OPUS)*"),
    (GS,
     "- **What determines an action's gil cost** — `00309060` in §5 is called but not read.",
     "- ~~**What determines an action's gil cost** — `00309060` in §5 is called but not read.~~ *(answered: see "
     "using-an-item-is-an-action-that-costs-an-item.md, " + SEC_IU + " - `10 × trunc(row.b[+0x0A] × 64.0 / 50.0)` "
     "under its gates, else 0; 2026-10-02, OPUS)*"),
    (GS,
     "Still not claimed: what determines an action's gil cost (`00309060`\nunread) and what `00320D50` returns.",
     "Still not claimed: ~~what determines an action's gil cost (`00309060`~~\n~~unread)~~ *(answered: see "
     "using-an-item-is-an-action-that-costs-an-item.md, " + SEC_IU + "; 2026-10-02, OPUS)* and what `00320D50` "
     "returns."),
    (BC,
     "`FUN_003037A0`, `FUN_00309110`, `FUN_00308FF0`, `FUN_00309060` and `FUN_00253690` are unread, so the",
     "`FUN_003037A0`, `FUN_00309110`, `FUN_00308FF0`, ~~`FUN_00309060`~~ and `FUN_00253690` are unread *(answered "
     "for `00309060`: see using-an-item-is-an-action-that-costs-an-item.md, " + SEC_IU + " - the gil cost reason "
     "`0x15` compares; 2026-10-02, OPUS)*, so the"),

    # ---- +0xE58 is the reserved cost, not a pool (F3) ----
    (GS,
     "pool via `FUN_00253690` with per-unit fallback `unit[0xE58]` — and records **gil as a flagged",
     "pool via `FUN_00253690` with ~~per-unit fallback~~ `unit[0xE58]` *(corrected 2026-10-02, OPUS: " + R3 + ")* — "
     "and records **gil as a flagged"),
    (GS,
     "cost, and writes the result back** — with the reserved amount stored at `unit + 0xE58`, exactly the\n"
     "per-unit fallback field `AI-8` names.",
     "cost, and writes the result back** — with the reserved amount stored at `unit + 0xE58`, exactly the\n"
     "~~per-unit fallback~~ field `AI-8` names *(corrected 2026-10-02, OPUS: a reservation, not a fallback pool; "
     + R3 + ")*."),
    (BC,
     "confirmed 2026-09-03 from `0030EFBB`–`0030EFD8` (reason `0x15`), and its check runs only for a",
     "confirmed 2026-09-03 from `0030EFBB`–`0030EFD8` (reason `0x15`); the struck question's `unit[0xE58]` is not a "
     "per-unit fallback pool but the gil cost reserved for the action in progress *(corrected 2026-10-02, OPUS: "
     + R3 + ")*, and its check runs only for a"),
    (BC,
     "| `0x15` | `00303BD0` | a **global** pool *and* a per-unit pool `unit[0xE58]` both below the cost |",
     "| `0x15` | `00303BD0` | a **global** pool *and* ~~a per-unit pool~~ `unit[0xE58]`, the gil cost already "
     "reserved for the action in progress, both below the cost *(corrected 2026-10-02, OPUS: " + R3 + ")* |"),
    (BC,
     "exceeds both the party's gil and the unit's own pool at `+0xE58`.",
     "exceeds both the party's gil and ~~the unit's own pool~~ the cost already reserved for the unit's action in "
     "progress at `+0xE58` *(corrected 2026-10-02, OPUS: " + R3 + ")*."),
]

ANCHOR = "## 9. Falsification pass 1 — 2026-09-13 (OPUS)"
SECTIONS = [
    (LC, "## 13. Buying a licence square: 00323D10 (OPUS, 2026-10-02)", ANCHOR, "licence_buy_section.md"),
    (IU, "## The action gil cost: 00309060 (OPUS, 2026-10-02)", ANCHOR, "gil_cost_section.md"),
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
    for rel, heading, anchor, src in SECTIONS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        texts[rel] = t
        lines = t.replace("\r\n", "\n").split("\n")
        if heading in lines:
            print("ALREADY section", rel.split("/")[-1]); continue
        if lines.count(anchor) != 1:
            print("REFUSING section", rel.split("/")[-1], "anchor count", lines.count(anchor)); fails += 1; continue
        body = open(os.path.join(HERE, src), "rb").read().decode("utf-8").replace("\r\n", "\n").strip("\n")
        block = heading + "\n\n" + body + "\n\n"
        crlf = "\r\n" in t
        eol = "\r\n" if crlf else "\n"
        a = eol + anchor + eol
        if t.count(a) != 1:
            print("REFUSING section", rel.split("/")[-1], "anchor line"); fails += 1; continue
        texts[rel] = t.replace(a, eol + block.replace("\n", eol) + anchor + eol, 1)
        print(("PATCHED section " if apply else "WOULD PATCH section ") + rel.split("/")[-1])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
