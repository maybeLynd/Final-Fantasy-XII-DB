"""nb_fix_pub_1002.py [--apply] - name other layers' functions by role in OPUS interior-citation rows ALREADY PUBLISHED
on 2026-10-01/02, whose callee names added unaccounted pass-22 crossings (measured by nb_page.py --vs-stripped: 30
new hits on 12 pages). Rewrites the page row and the record's rows.json alike; adds one crossing bullet where the row's
own function carries the edge. Prints changed / already / MISSING per file. FAILS n.
"""
import glob
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))

FIG = "the framework-singleton getter"
FIXES = [  # (page, old, new) - the generating rows.json is found by content
    ("00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md",
     "calls `0017FE30()` and", "calls a 21-byte framework forwarder and"),
    ("00-Engine-Core-Runtime/Developer-Tuning-Console/arm-catalogue-slice-I-ids-268-293.md",
     "result of `00184950()`", "result of the getter of dword `01F3DA18`"),
    ("02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/cmap-menumap-common-sublocation-directory.md",
     "`f = 003148F0()`", "`f = WorldTransition_GetActiveOrPendingFieldId()`"),
    ("04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md",
     "`p = 00263750(index)`", "`p = PartyRoster_GetActorBySlot(index)`"),
    ("04-Actor-Entity/Battle-Record-Kind/actor-type-id-partition-and-the-13-value-band.md",
     "calls `003601B0(0x13)`", "sets bit 0x13 of dword `022CB720` (a 14-byte bit setter)"),
    ("15-Input/Input-Name-Registry/the-input-name-registry-and-channel-aliases.md",
     "calls `00796E20()` and", "calls " + FIG + " and"),
    ("16-UI/CONTRACT-text-control-codes-and-dyngeo-draw.md",
     "calls `00796E20()` and", "calls " + FIG + " and"),
    ("16-UI/Widget-Object-Model/the-widget-message-protocol.md",
     "`0053DD10(003148F0())`", "`0053DD10(WorldTransition_GetActiveOrPendingFieldId())`"),
    ("17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md",
     "passed through `003AB880`", "passed through the 42-byte external-source handle check"),
    ("17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md",
     "calls `003AB880` on the new qword", "calls the 42-byte external-source handle check on the new qword"),
    ("17-Presentation-Rendering/Character-Render-Records/the-character-render-record-array.md",
     "calls `00426FA0` and", "calls a 249-byte record helper and"),
    ("19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md",
     "of `00796E20()`", "of " + FIG),
    ("19-Save-Load-Settings/Game-Settings-Config/the-settings-command-table.md",
     "`0079AE40(00796E20(), i, 0)`", "`0079AE40(g, i, 0)` (g = what " + FIG + " returns)"),
    ("22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md",
     "when `00267310(byte +0x15 of argument 2)` is 0",
     "when the byte at `02099011 + 0x288 * (byte +0x15 of argument 2)` is 0 (a 22-byte table read)"),
    ("22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md",
     "calls `0035B1A0(id)`", "calls a 158-byte Input-layer body on id"),
    ("22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md",
     "reads an integer through `00537410`", "reads an integer through a 409-byte reader"),
    ("22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md",
     "calls `00863520(dword 022CFEF4 + 4*slot, 0x24)`",
     "calls a 31-byte import wrapper on (dword `022CFEF4` + 4*slot, 0x24)"),
    ("22-Middleware-PhyreEngine/The-Frame/what-happens-between-two-frames.md",
     "calls `00863650` with", "calls a 61-byte helper with"),
    ("99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md",
     "`003601B0(0x13)` and `003172E0(byte r8[+4])`",
     "the bit setter on 0x13 (bit 0x13 of dword `022CB720`) and `PartyConfiguration_AddSelector00To06ToAvailableIndex4To8(byte r8[+4])`"),
    ("99-Unresolved-Residual/Cutscene-Asset-Slots/cutscene-name-slots-and-the-depth-of-field-sidecar.md",
     "calls `00332130`,", "calls a 93-byte actor helper,"),
    ("99-Unresolved-Residual/Largest-Unclassified-Code/the-largest-unclassified-functions.md",
     "to `0017D280`", "to the 85-byte varargs log printer"),
]

SLOC = "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/sloc-menumap-container.md"
SLOC_ADD = ("## Cross-subsystem neighbours of the interior rows (OPUS, 2026-10-02)\n\n"
            "- **Script/VM native bridge — CLIENT (1 edge).** The 23-byte script verb `00356BF0` pops one operand "
            "through `00267E10` and tail-jumps into the row's `00377400` with it, so a script selects which of the four "
            "`02ADD010` entries is opened. Edge from `edges.tsv`; both bodies read.\n")


def rows_for(page):
    out = []
    for rj in glob.glob(os.path.join(DB, "_index", "candidates", "opus-*-cloudint-100*", "rows.json")):
        t = io.open(rj, encoding="utf-8").read()
        if ('"page": "%s"' % page) in t:
            out.append(rj)
    return out


def sub(path, old, new, apply):
    t = io.open(path, encoding="utf-8", newline="").read()
    if old in t:
        if apply:
            io.open(path, "w", encoding="utf-8", newline="").write(t.replace(old, new))
        return "changed x%d" % t.count(old)
    return "already" if new in t else "MISSING"


def main():
    apply = "--apply" in sys.argv
    fails = 0
    for page, old, new in FIXES:
        for path in [os.path.join(DB, *page.split("/"))] + rows_for(page):
            r = sub(path, old, new, apply)
            fails += r == "MISSING"
            print("%-11s %s :: %s" % (r, os.path.relpath(path, DB)[-60:], old[:40]))
    p = os.path.join(DB, *SLOC.split("/"))
    b = open(p, "rb").read()
    if SLOC_ADD.splitlines()[0].encode("utf-8") in b:
        print("already     sloc crossing bullet")
    else:
        nl = b"\r\n" if b"\r\n" in b[-4000:] else b"\n"
        add = SLOC_ADD.encode("utf-8").replace(b"\n", nl)
        if apply:
            open(p, "wb").write(b.rstrip(b"\r\n") + nl + nl + add)
        print("changed     sloc crossing bullet")
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
