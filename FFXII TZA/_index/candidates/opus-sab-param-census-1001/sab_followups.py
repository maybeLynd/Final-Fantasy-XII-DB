"""sab_followups.py [--apply] - carry the .sab census into the container page and register row SQ-1 (OPUS, 2026-10-01).

Exact substrings, each once; tag-guarded, so a re-run reads ALREADY. The SQ-1 text is a register cell, so the new text
carries no pipe. Dry run unless --apply; FAILS n.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
SAB = "18-Audio/Sound-Bank-And-Voice-Formats/sab-sound-bank-container.md"
REG = "_index/OPEN-QUESTIONS.md"
CEN = "`../../_index/candidates/opus-sab-param-census-1001/`"

EDITS = [
    (SAB, "agree with 268 `se` folders plus the `shout` banks is not re-counted here.)*",
     "agree with ~~268~~ 267 `se` folders plus the `shout` banks ~~is not re-counted here~~ is re-counted 2026-10-01 "
     "(OPUS): they do - 267 `se` ordinals (0-267, slot 3 unused) plus 83 `shout` values (`5172`-`5256`) make the 350, "
     "one value per folder; census " + CEN + ".)*",
     "is re-counted 2026-10-01 (OPUS): they do"),
    (SAB, "`+0x0A` takes 350 distinct values in",
     "`+0x0A` takes 350 distinct values *(267 `se` folder ordinals plus 83 `shout` values, one per folder - census "
     "2026-10-01, OPUS, " + CEN + ")* in",
     "350 distinct values *(267 `se` folder ordinals plus 83"),
    (REG, "(0–267 over 268 folders)",
     "(0–267 over ~~268~~ 267 `se` folders, slot 3 unused; corrected 2026-10-01, OPUS, by a census of all 4,609 `.sab` "
     "headers)",
     "(0–267 over ~~268~~ 267 `se` folders, slot 3 unused"),
]


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new, tag in EDITS:
        if rel not in texts:
            texts[rel] = open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        t = texts[rel]
        if tag in t:
            print("ALREADY", rel, tag[:30]); continue
        if rel == REG and "|" in new:
            print("REFUSING pipe in register text"); fails += 1; continue
        if t.count(old) != 1:
            print("REFUSING %s: %d hits for %r" % (rel, t.count(old), old[:40])); fails += 1; continue
        texts[rel] = t.replace(old, new, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + rel, tag[:30])
    if apply and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
