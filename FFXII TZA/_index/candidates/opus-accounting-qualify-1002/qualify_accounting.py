"""qualify_accounting.py [--apply] - qualify OPUS's 2026-09-14 closure of OPUS-CONTRA-ARENA-ACCOUNTING-ARRAY on
ASTRA's accounting-dispatch-index (OPUS, 2026-10-02; re-read at the bytes, control accounting_check.py).

The closure called 003AB910 "a boolean dispatch". Its boolean only picks the helper (0036C5D0 or 0036C620). The new
index rides in edx unchanged, and both helpers use it sign-extended with no 0/1 bound. 003AB910 has one caller, the
factory 0041F340, which forwards CharacterRenderRecord +0x0C1. Its two known writers store a source byte's upper
nibble (0..15). So "022D8E18 is element 2 and is never reached" holds for the literal call sites only.

Strikes with a pointer, exact substrings, tag-guarded; dry run unless --apply; FAILS n.
"""
import os
import sys

P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                  "24-Compiler-And-CRT-Runtime", "Memory-And-Allocation",
                                  "where-the-games-memory-comes-from.md"))
Q = " *(qualified 2026-10-02, OPUS - see the qualification below)*"
EDITS = [
    ("then `jmp 0036C5D0` when it is 1 and `jmp 0036C620` when it is not. **A boolean dispatch.**",
     "then `jmp 0036C5D0` when it is 1 and `jmp 0036C620` when it is not. ~~**A boolean dispatch.**~~ The boolean only "
     "picks the helper; the index rides in `edx` unchanged" + Q + "."),
    ("reached.** The current-category byte is safe, `022D8E1C`, `022D8E20` and `022D8E28` are safe, and\n"
     "**this page's scalar model stands.**",
     "reached.** ~~The current-category byte is safe, `022D8E1C`, `022D8E20` and `022D8E28` are safe, and\n"
     "**this page's scalar model stands.**~~ That holds for the literal call sites" + Q + "."),
]
ANCHOR = "## The `0036CB00` exclusive subtree — all 3 members bound (SWE2-FRONTIER, followup queue)"
HEAD = "### The closure qualified: the forwarding path carries a nibble, not a boolean (OPUS, 2026-10-02)"
SECTION = """### The closure qualified: the forwarding path carries a nibble, not a boolean (OPUS, 2026-10-02)

*On ASTRA's accounting-dispatch-index (`_experiments/evidence/accounting-dispatch-index/`), re-read at the bytes
(control: `_index/candidates/opus-accounting-qualify-1002/accounting_check.py`).* The closure above called `003AB910` a
boolean dispatch. It is not.
- The boolean in `r8` (`test cl, 3` / `setne r8b`) only picks the helper for the storage representation: `0036C5D0`
  or `0036C620`.
- The new index rides in `edx`, which `003AB910` never writes.
- `0036C5D0` replaces `r8` at once (`movsxd r8, edx`, `0036C5D0`), and `0036C620` sign-extends `edx` the same way.
  Both debit `022D8E10 + old * 4`, credit `022D8E10 + new * 4`, and store the low byte at `+0x17`, with no 0/1
  bound.

`003AB910` has one caller: the instance factory `0041F340`. It forwards CharacterRenderRecord `+0x0C1`, read with
`movsx` (`0041F515`, `0041F525`). Both known writers of `+0x0C1`, `002E28E0` and `002E3110`, store a source byte's
upper nibble (`shr edx, 4`), so on those paths the index is 0..15. It is 0 or 1 exactly when the source byte is below
`0x20`.

**So the closure holds for the literal call sites, and is open for this one path.** If a source byte at or above
`0x20` reaches the factory, the credit lands at `022D8E18` or beyond, on the struct fields the initializer writes.
Whether the shipped game ever supplies such a byte, and whether other writers of `+0x0C1` exist, is not established
statically. The stored fields' own record is the type store's CharacterRenderRecord `+0x0C1` row (`b83439b6c`).
"""


def main():
    apply = "--apply" in sys.argv
    t = open(P, "rb").read().decode("utf-8")
    eol = "\r\n" if "\r\n" in t else "\n"
    fails = 0
    for old, new in EDITS:
        if new in t or new.replace("\n", "\r\n") in t:
            print("ALREADY edit"); continue
        hit = [c for c in (old, old.replace("\n", "\r\n")) if t.count(c) == 1]
        if not hit:
            print("REFUSING edit", old[:50]); fails += 1; continue
        n = new.replace("\n", "\r\n") if "\r\n" in hit[0] else new
        t = t.replace(hit[0], n, 1)
        print(("PATCHED" if apply else "WOULD PATCH") + " edit")
    if HEAD in t:
        print("ALREADY section")
    elif t.count(ANCHOR) != 1:
        print("REFUSING anchor"); fails += 1
    else:
        t = t.replace(ANCHOR, SECTION.replace("\n", eol) + eol + ANCHOR, 1)
        print(("PATCHED" if apply else "WOULD PATCH") + " section")
    if apply and not fails:
        open(P, "wb").write(t.encode("utf-8"))
    print("FAILS", fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
