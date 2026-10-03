"""uc1_pack.py - one drafting pack for the 59 F-unmet UC-1 game-code bodies (OPUS, 2026-10-03; FABLE's route ruling
fable-uc1-gamecode-route-ruling-1003, tests 1-3). Per body: its uc1_band extent, how it is entered (from
uc1_credible.json: direct call / jmp sites, rip references, table qwords, or what precedes the start), and the
annotated listing. Writes inbox/uc1/PACK.md. The drafter is not OPUS; OPUS re-reads every row (test 2)."""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def entry_text(o):
    if o["direct"]:
        return "direct call/jmp sites (calling function@site address): " + ", ".join(o["direct"])
    if o["rip"]:
        return "rip references: " + ", ".join(o["rip"])
    if o["tables"]:
        return "aligned qword table entries at: " + ", ".join(o["tables"])
    prev = {"c3": "a `ret`", "cc": "`int3` padding", "90": "`nop` padding"}.get(o["prev_byte"], "byte %s" % o["prev_byte"])
    if o["after_jmp"]:
        prev = "a 5-byte `jmp rel32`"
    return ("no direct reference found (direct-call/jmp scan, rip-reference scan and aligned-qword table scan over "
            "every section); the start follows %s%s" % (prev, "" if o["aligned16"] else ", and is NOT 16-byte aligned"))


def main():
    d = json.load(open(os.path.join(HERE, "uc1_credible.json")))
    out = ["# UC-1 drafting pack (OPUS, %s) - %d bodies" % (cl.stamp(), len(d)), "",
           "Shipping EXE sha256 73461D08...21F8, image base 00120000. Each body is a UC-1 frontier body (admitted to "
           "the frontier 2026-09-28) that no rule explains yet.", ""]
    for o in d:
        a = int(o["body"], 16)
        lines, _tok = L.listing(a)
        out += ["## %s (%d B, extent %s-%08X)" % (o["body"], o["size"], o["body"], a + o["size"]), "",
                "Entered: " + entry_text(o), "", "```"] + lines + ["```", ""]
    os.makedirs(os.path.join(HERE, "inbox", "uc1"), exist_ok=True)
    p = os.path.join(HERE, "inbox", "uc1", "PACK.md")
    io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
    print("wrote", p, len(d), "bodies")


if __name__ == "__main__":
    main()
