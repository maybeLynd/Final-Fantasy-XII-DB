"""ee_pack.py PAGE [PAGE...] - drafting packs for engine_explained (OPUS, 2026-10-03): the bodies of 128 B or more that
the page cites only at the entry and that nothing explains yet (Tools/work/OPUS/family/entry_big.json, written by
entry_big.py). F-frontier or family member alike: an interior anchor on the page counts under the base rule 9efc6221.
Writes inbox/ee/<slug>.md with each body's annotated listing; rows come back as {"mode": "ee"} reports."""
import io
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cloudlib as cl  # noqa: E402
import listing as L  # noqa: E402
import f_pack  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
EB = os.path.normpath(os.path.join(HERE, "..", "family", "entry_big.json"))


def main():
    eb = json.load(open(EB))
    MAXSZ = int(os.environ.get("EE_MAX_SIZE", "100000"))
    os.makedirs(os.path.join(HERE, "inbox", "ee"), exist_ok=True)
    for page in sys.argv[1:]:
        fs = [h for h in eb.get(page, []) if L.sizes()[int(h, 16)] <= MAXSZ]
        slug = f_pack.slug_of(page)
        out = ["# engine_explained drafting pack: `%s` (OPUS, %s) - %d bodies" % (page, cl.stamp(), len(fs)), "",
               "Each body is cited on this page only at its entry and is 128 B or more, so the citation does not explain "
               "it. Write one row per body: a sentence of what the body does (access and representation, every path), "
               "with 1-5 anchors strictly inside it.", ""]
        for h in fs:
            f = int(h, 16)
            lines, _t = L.listing(f)
            out += ["## %s (%d B)" % (h, L.sizes()[f]), "", "```"] + lines + ["```", ""]
        p = os.path.join(HERE, "inbox", "ee", slug + ".md")
        io.open(p, "w", encoding="utf-8", newline="\n").write("\n".join(out))
        print("wrote", p, len(fs), "bodies")


if __name__ == "__main__":
    main()
