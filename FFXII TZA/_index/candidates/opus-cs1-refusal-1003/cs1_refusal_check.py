"""cs1_refusal_check.py [--apply] - CS-1's return-value sentence corrected (ASTRA-REQ-OPUS-CS1-RETAINED-DISMISS-REFUSAL-1003),
OPUS 2026-10-03. Checks the three -2 paths of 00311CF0 and its call sites in the image, and that the contract no longer
states the two-case exclusivity unstruck. --apply makes the edit (idempotent). --rejected tests the pre-edit text."""
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DBR = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DBR, "..", "Tools", "analysis-kit", "gfz-scripts")))
import retool  # noqa: E402

P = os.path.join(DBR, "07-Combat-Action", "CONTRACT-native-command-seam.md")
OLD = "Only a null stats\n  record, or the `0x80000003` status gate with the field bit clear, returns −2."
OLD1 = "Only a null stats"
NEW_TAIL = ("~~Only a null stats record, or the `0x80000003` status gate with the field bit clear, returns −2.~~ Three "
            "cases return −2 (`00311DF1`): a null stats record (`00311D1B`), the `0x80000003` status gate with the field "
            "bit clear (`00311D35`), and command `0x113` while the unit's word `+0x714` already holds `0x113` "
            "(`00311D40`–`00311D4C`), each with nothing recorded; for command `0x113` over any other `+0x714` it first "
            "clears bit `0x1` of word `+0x5AD0` of the record at qword `02EBF190`. OPUS block 351's retained run records "
            "the third case (`s20-opus-replay-command-seam/result.json`: return `0xFFFFFFFE`, `+0xBA0` unchanged, no "
            "calls). *(corrected 2026-10-03, OPUS, on ASTRA-REQ-OPUS-CS1-RETAINED-DISMISS-REFUSAL-1003)*")
CALLERS_OLD = "through two callers only — the by-focus-handles fan-out and the defeat-cleanup step — and its"
CALLERS_NEW = ("through two callers only — the by-focus-handles fan-out and the defeat-cleanup step (three call sites: "
               "`00311B20` at `00311C7B` and `00311CA6`, `003138D0` at `0031395D`) — and its")


def apply():
    t = io.open(P, encoding="utf-8", newline="").read()
    nl = "\r\n" if "\r\n" in t else "\n"
    old = OLD.replace("\n", nl)
    if NEW_TAIL not in t:
        assert t.count(old) == 1, "old sentence not found once"
        t = t.replace(old, NEW_TAIL)
    if CALLERS_NEW not in t:
        assert t.count(CALLERS_OLD) == 1
        t = t.replace(CALLERS_OLD, CALLERS_NEW)
    io.open(P, "w", encoding="utf-8", newline="").write(t)


def ins(a):
    return next(iter(retool.R.md.disasm(retool.R.at(a, 16), a)))


def check(rejected):
    fails = []
    want = {0x00311D1B: ("je", "0x311df1"), 0x00311D35: ("je", "0x311df1"), 0x00311D40: ("cmp", "si, ax"),
            0x00311D45: ("cmp", "word ptr [rbx + 0x714], ax"), 0x00311D4C: ("je", "0x311df1"),
            0x00311D3B: ("mov", "eax, 0x113")}
    for a, w in want.items():
        i = ins(a)
        if (i.mnemonic, i.op_str) != w:
            fails.append("%08X is %s %s" % (a, i.mnemonic, i.op_str))
    calls = sorted(retool.scan()["calls"].get(0x00311CF0, set()))
    if [s for _f, s in calls] != [0x00311C7B, 0x00311CA6, 0x0031395D]:
        fails.append("call sites %s" % ["%08X" % s for _f, s in calls])
    t = OLD.replace("\n", " ") if rejected else re.sub(r"~~.*?~~", "", io.open(P, encoding="utf-8").read().replace("\r\n", "\n"))
    if "Only a null stats" in t and "returns −2." in t.split("Only a null stats", 1)[1][:120]:
        fails.append("the two-case exclusivity is still stated unstruck")
    for f in fails:
        print("FAIL", f)
    print("checks 6 bytes + call sites + text%s  FAILS %d" % ("  (rejected text)" if rejected else "", len(fails)))
    return 1 if fails else 0


if __name__ == "__main__":
    if "--apply" in sys.argv:
        apply()
    sys.exit(check("--rejected" in sys.argv))
