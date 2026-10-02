"""apply_tick_tail.py [--apply] - the periodic tick 00310DB0 after its first apply, and its gate structure (OPUS,
2026-10-02; read by a read-only reader, byte-checked by OPUS, control tick_tail_check.py).

Adds a section to the periodic tick page (from tick_tail_section.md), corrects the "six gates, all must pass" text on
two pages (seven gates; only the first three stop everything; the readiness probe 00265680, the two eligibility masks
and the 0x1000000000 flag skip to the common tail 003112A1, which still runs the enmity decay and 002FE950; a party
Esper record can be dismissed before them), the pickup table address (02EC0FA0) and 00469E30's argument (the stats
record). Exact substrings, each once; tag-guarded; strikes per line; dry run unless --apply; FAILS n.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
PT = "10-Status-Periodic-Terminal/Periodic-Tick/what-the-periodic-tick-does.md"
CPT = "10-Status-Periodic-Terminal/CONTRACT-periodic-tick.md"
T = "the tick after its first apply"
EDITS = [
    (PT, "## 2. Nothing happens at all unless six gates pass",
     "## 2. ~~Nothing happens at all unless six gates pass~~ Three gates stop everything, four more skip to the tail (OPUS, 2026-10-02)"),
    (PT, "| the field permits action | `FieldData_GetActiveFieldRecordBit15()` returns 0 |",
     "| the field permits action | `FieldData_GetActiveFieldRecordBit15()` returns 0 |\n"
     "| *(added 2026-10-02, OPUS)* the actor manager is ready - fails to the tail | `00265680()` is non-zero (`00310F12`-`00310F19`) |"),
    (PT, "| a 64-bit unit flag is clear | `!(unit->qwFlags & 0x1000000000)` |",
     "| a 64-bit unit flag is clear | `!(unit->qwFlags & 0x1000000000)` |\n\n"
     "*(Corrected 2026-10-02, OPUS - section 14, " + T + ": only the first three gates stop everything (they exit to "
     "`003112D1`). The readiness probe, the two masks and the flag exit to the common tail `003112A1`, which still runs "
     "the enmity decay `00321530` and `002FE950`. Between gate 3 and the probe, a party Esper record whose HP is gone or "
     "whose summoner is unavailable is dismissed (`003138D0(0)` at `00310EF8`), and then nothing else runs.)*"),
    (CPT, "**Preconditions.** Six gates, all of which must pass, in `00310DB0`'s first ninety instructions, and",
     "**Preconditions.** ~~Six gates, all of which must pass,~~ Seven gates *(corrected 2026-10-02, OPUS: gates 1-3 "
     "stop everything; the readiness probe `00265680` (`00310F12`), gates 4-5 and gate 6 skip to the common tail "
     "`003112A1`, which still runs the enmity decay `00321530` and `002FE950`; a party Esper record can be dismissed "
     "(`00310EF8`) between gate 3 and the probe - the periodic tick page, section 14)*, in `00310DB0`'s first ninety "
     "instructions, and"),
    (PT, "into the `02EB0FA0` pickup table",
     "into the ~~`02EB0FA0`~~ `02EC0FA0` *(corrected 2026-10-02, OPUS: `0031983B`, `00319A0B`)* pickup table"),
    (PT, "when `002F8E90(unit)` returns 8",
     "when ~~`002F8E90(unit)`~~ `002F8E90(stats)` *(corrected 2026-10-02, OPUS: the tick passes the stats record, "
     "`00311114`)* returns 8"),
]
HEAD = "## 14. The tick after its first apply - the Esper dismiss, the traps, walk MP, the pickup and the common tail (OPUS, 2026-10-02)"
ANCHOR = "## Falsification pass 1 — 2026-09-12 (OPUS)"


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        texts[rel] = t
        eol = "\r\n" if "\r\n" in t else "\n"
        if new.replace("\n", eol) in t or new in t:
            print("ALREADY", old[:40]); continue
        if t.count(old) != 1:
            print("REFUSING", old[:50], t.count(old)); fails += 1; continue
        texts[rel] = t.replace(old, new.replace("\n", eol), 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + old[:40])
    t = texts[PT]
    eol = "\r\n" if "\r\n" in t else "\n"
    if HEAD in t:
        print("ALREADY section")
    elif t.count(ANCHOR) != 1:
        print("REFUSING anchor"); fails += 1
    else:
        sec = io.open(os.path.join(HERE, "tick_tail_section.md"), encoding="utf-8").read().strip("\n")
        block = HEAD + "\n\n" + sec + "\n\n"
        texts[PT] = t.replace(ANCHOR, block.replace("\n", eol) + ANCHOR, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + "section")
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
