"""apply_growth.py [--apply] - the four float stats' growth formula 002F9BD0 (OPUS, 2026-10-02; read by a read-only
reader, byte-checked by OPUS, control growth_check.py).

Adds section 4a to the level-up page (from growth_section.md), corrects its 002F9BD0 signature (no level argument:
value in xmm0, growth byte in edx, an unused 0 in r8d), adds the formula to the contract's determinism note, and
corrects the unit-definition page's "456-byte rows" for the party definition table (rows are the descriptor's word +8
long, 128 in the shipped battle_pack.bin; 0x1C8 = 456 is the spacing of the party stats records). Exact substrings,
each once; strikes per line; tag-guarded; dry run unless --apply; FAILS n.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
LU = "13-Rewards-Progression-Economy/what-happens-when-a-character-levels-up.md"
CLU = "13-Rewards-Progression-Economy/CONTRACT-level-advance-and-growth.md"
UD = "04-Actor-Entity/Unit-Definition/how-a-battle-unit-is-built-from-its-definition.md"
EDITS = [
    (LU, "`002F9BD0(level, growth, 0, value)`",
     "~~`002F9BD0(level, growth, 0, value)`~~ `002F9BD0(value, growth)` *(corrected 2026-10-02, OPUS: the value in "
     "`xmm0`, the growth byte in `edx`, an unused 0 in `r8d`; no level argument - section 4a)*"),
    (CLU, "The four float stats **are** deterministic; only HP and MP roll.",
     "The four float stats **are** deterministic; only HP and MP roll. *(Added 2026-10-02, OPUS: each grows by "
     "`g / 128` per level with no draw, `stat(L) = base + L * g / 128`, clamped to `99.99999237` once a sum exceeds "
     "`100.0` - `002F9BD0`; the level-up page, section 4a.)*"),
    (UD, "| `02EBF130` | party definition table, 456-byte rows;",
     "| `02EBF130` | party definition table, ~~456-byte rows~~ rows of the descriptor's word `+8` bytes, 128 in the shipped "
     "`battle_pack.bin` *(corrected 2026-10-02, OPUS: `0030C70B`-`0030C71D` multiply that word by the type byte; "
     "`0x1C8` = 456 is the spacing of the party stats records at `[02EBF190]`)*;"),
]
HEAD = "## 4a. The four float stats grow linearly: base + level x g / 128 (OPUS, 2026-10-02)"
ANCHOR = "## 5. The third argument is a silence flag"


def main():
    apply = "--apply" in sys.argv
    fails = 0
    texts = {}
    for rel, old, new in EDITS:
        t = texts.get(rel) or open(os.path.join(DB, rel), "rb").read().decode("utf-8")
        texts[rel] = t
        if new in t:
            print("ALREADY", old[:40]); continue
        if t.count(old) != 1:
            print("REFUSING", rel.split("/")[-1], old[:40], t.count(old)); fails += 1; continue
        texts[rel] = t.replace(old, new, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + old[:40])
    t = texts[LU]
    eol = "\r\n" if "\r\n" in t else "\n"
    if HEAD in t:
        print("ALREADY section")
    elif t.count(ANCHOR) != 1:
        print("REFUSING anchor"); fails += 1
    else:
        sec = io.open(os.path.join(HERE, "growth_section.md"), encoding="utf-8").read().strip("\n")
        texts[LU] = t.replace(ANCHOR, (HEAD + "\n\n" + sec + "\n\n").replace("\n", eol) + ANCHOR, 1)
        print(("PATCHED " if apply else "WOULD PATCH ") + "section")
    if apply and not fails:
        for rel, x in texts.items():
            open(os.path.join(DB, rel), "wb").write(x.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
