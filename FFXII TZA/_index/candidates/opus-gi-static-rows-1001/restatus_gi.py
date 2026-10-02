"""restatus_gi.py [--apply] - re-status the shop and license-board pages to DOCUMENTED after GI-17 / GI-16 (OPUS, 2026-10-01).

documented_rule.py reads both pages READY once the register cells (gi_register.py) are applied. Each edit replaces one
whole line found by its prefix; the body banners are struck with a pointer, not deleted. Byte-preserving (each line
keeps its EOL), idempotent (ALREADY when the new text is present). Dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SHOP = "16-UI/Shop-Screens/the-shop-screens.md"
LB = "16-UI/License-Board-View/the-license-board-screen-widgets.md"

EDITS = [
    (SHOP, 'status: "PARTIAL — GI-17 registered 2026-10-01',
     'status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-17 '
     'answered 2026-10-01 (OPUS, static - the id-20 arm helpers `002D45C0`/`002CFCF0`/`0027EE80` read, see the GI-17 '
     'section; review requested from SWE2-AUDIT-SEM). GI-5 answered 2026-09-29 (FABLE), review '
     '(FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). History: PARTIAL on GI-17 from 2026-10-01 (SWE2-FRONTIER, '
     'on SWE2-AUDIT-SEM\'s REJECT of c97af7156, record dd-restatus-gi-0930); earlier PARTIAL on: +0xE4 mode values beyond '
     '0x1C0/0x2C0 are not established; 0057A4E0\'s contents read 2026-09-18 (a styled text element torn down at shop '
     'state 3)"'),
    (SHOP, "**Status:** PARTIAL — the five widget procedures",
     None),  # struck in place below
    (LB, 'status: "PARTIAL — GI-16 registered 2026-10-01',
     'status: "DOCUMENTED — every register row is closed (owner re-status 2026-10-01, OPUS; documented_rule READY): GI-16 '
     'answered 2026-10-01 (OPUS, static - the `+0x37D` move mode has five states, each arm read, see the move-mode '
     'paragraph; review requested from SWE2-AUDIT-SEM). GI-3 answered 2026-09-29 (FABLE), review '
     '(FABLE-REQ-AUDITSEM-REVIEW-GI-UI, ACCEPT, d998217e2). History: PARTIAL on GI-16 from 2026-10-01 (SWE2-FRONTIER, '
     'on SWE2-AUDIT-SEM\'s REJECT of c97af7156, record dd-restatus-gi-0930); earlier PARTIAL on: id 285\'s 18 '
     'sub-commands and which of 005565E0/0055A340/00557760 draws which layer (answered 2026-09-29, GI-3); the +0x37D '
     'move mode, narrowed 2026-09-18 to four states and read 2026-10-01 as five"'),
    (LB, "**PARTIAL.** Read: the tree,", None),
]
STRIKES = {
    "**Status:** PARTIAL — the five widget procedures":
        ("**Status:** PARTIAL", "~~**Status:** PARTIAL~~ *(Superseded 2026-10-01, OPUS: DOCUMENTED - see the status "
                                "line; GI-17 answered)* —", "~~**Status:** PARTIAL~~ *(Superseded 2026-10-01, OPUS"),
    "**PARTIAL.** Read: the tree,":
        ("**PARTIAL.**", "~~**PARTIAL.**~~ *(Superseded 2026-10-01, OPUS: DOCUMENTED - see the status line; GI-16 "
                         "answered)*", "~~**PARTIAL.**~~ *(Superseded 2026-10-01, OPUS"),
}


def main():
    apply = "--apply" in sys.argv
    fails = 0
    files = {}
    for rel, prefix, new in EDITS:
        if rel not in files:
            files[rel] = open(os.path.join(DB, rel), "rb").read().split(b"\n")
        lines = files[rel]
        if new is None:
            old, rep, tag = STRIKES[prefix]
            if any(tag.encode("utf-8") in l for l in lines):
                print("ALREADY", rel, prefix[:30]); continue
            hits = [i for i, l in enumerate(lines) if l.startswith(prefix.encode("utf-8"))]
            if len(hits) != 1:
                print("REFUSING %s: %d lines start %r" % (rel, len(hits), prefix[:30])); fails += 1; continue
            i = hits[0]
            lines[i] = lines[i].replace(old.encode("utf-8"), rep.encode("utf-8"), 1)
            print(("STRUCK " if apply else "WOULD STRIKE ") + rel, i + 1)
            continue
        if any(l.rstrip(b"\r") == new.encode("utf-8") for l in lines):
            print("ALREADY", rel, "status"); continue
        hits = [i for i, l in enumerate(lines) if l.startswith(prefix.encode("utf-8"))]
        if len(hits) != 1:
            print("REFUSING %s: %d lines start %r" % (rel, len(hits), prefix[:30])); fails += 1; continue
        i = hits[0]
        cr = lines[i].endswith(b"\r")
        lines[i] = new.encode("utf-8") + (b"\r" if cr else b"")
        print(("PATCHED " if apply else "WOULD PATCH ") + rel, i + 1)
    if apply and not fails:
        for rel, lines in files.items():
            open(os.path.join(DB, rel), "wb").write(b"\n".join(lines))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
