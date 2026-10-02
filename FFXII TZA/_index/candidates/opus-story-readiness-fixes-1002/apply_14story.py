"""apply_14story.py [--apply] - OPUS's share of the 14-Story readiness corrections (OPUS, 2026-10-02).

Cloud wave 3 mapped 14-Story-Event-Quest-Hunt without the executable; OPUS decided 13 of its 18 value items at the
shipping image (verdicts in the RE repo docs/readiness/14-story.md, control story_check.py). Most fall on FABLE's two
flag-bank pages, which FABLE edits from the verdicts (request). OPUS edits only the shared README lines and its own
event-memory page: the bank count (five storage banks; Bank512's Low and High accessor pairs address one region) and
the README's status banner. Tag-guarded; ALREADY when present; FAILS n.
"""
import os
import sys

DB = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
F = "14-Story-Event-Quest-Hunt/"
WHY = ("*(corrected 2026-10-02, OPUS: `Bank512`'s Low and High pairs address one `+0x14B4` region - queries `0032AA60` "
       "/ `0032AAD0`, setters `0032AD70` / `0032ADF0`, the High pair adding `0x100` at `0032AAE7` / `0032AE04`; "
       "persistent-flag-banks.md AA-4)*")
BANNER = "*(corrected 2026-10-02, OPUS: the page's front matter says `status: AUDITED`)*"

EDITS = [
    (F + "README.md",
     "  **DOCUMENTED, tier 1.** Story progress is **bits** in six banks at mapped save-payload\n",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** " + BANNER + ". Story progress is **bits** in ~~six banks~~ "
     "five banks, six accessor families " + WHY + ", at mapped save-payload\n"),
    (F + "README.md",
     "  **DOCUMENTED, tier 1.** Story progress is **bits** in six banks at mapped save-payload offsets\n",
     "  ~~**DOCUMENTED, tier 1.**~~ **AUDITED, tier 1** " + BANNER + ". Story progress is **bits** in ~~six banks~~ "
     "five banks, six accessor families " + WHY + ", at mapped save-payload offsets\n"),
    (F + "event-memory-at-actor-bind.md",
     "- **six persistent flag banks**, each with an identical script-VM surface",
     "- **~~six~~ five persistent flag banks** (six accessor families) " + WHY + ", each with an identical script-VM "
     "surface"),
    (F + "event-memory-at-actor-bind.md",
     "— the six banks, their payload offsets,",
     "— the ~~six~~ five banks *(corrected 2026-10-02, OPUS: five storage regions, six accessor families; AA-4)*, "
     "their payload offsets,"),
]


def main():
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        p = os.path.join(DB, rel)
        t = texts.get(rel) or open(p, "rb").read().decode("utf-8")
        crlf = "\r\n" in t
        o = old.replace("\n", "\r\n") if crlf else old
        n = new.replace("\n", "\r\n") if crlf else new
        if n in t:
            print("ALREADY", rel)
            texts[rel] = t
            continue
        if t.count(o) != 1:
            print("REFUSING", rel, t.count(o), repr(old[:50]))
            fails += 1
            continue
        texts[rel] = t.replace(o, n, 1)
        print("WOULD PATCH" if "--apply" not in sys.argv else "PATCHED", rel)
    if "--apply" in sys.argv and not fails:
        for rel, t in texts.items():
            open(os.path.join(DB, rel), "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
