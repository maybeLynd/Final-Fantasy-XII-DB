"""apply_c21.py [--apply] - qualify the 2026-10-02 C21 answer on CONTRACT-periodic-tick.md (OPUS, 2026-10-02).

An audit of the 10-Status readiness package's page-text-only value items (items 10, 11, 12, 19, 21, 22) re-read them
at the bytes. Items 10, 12, 19 and 22 hold; 11 rests on the pages' own consistent sections. Item 21's answer said
0030AB40 returns 1 or 2; it also returns 0 when its input guards fail (0030AC42 / 0030AC46). Tag-guarded; FAILS n.
"""
import os
import sys

P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..",
                                  "10-Status-Periodic-Terminal", "CONTRACT-periodic-tick.md"))
OLD = "`0030AB40` returns `(computed == expected) + 1`, 1 or 2; 2026-10-02, OPUS)*"
NEW = ("`0030AB40` returns `(computed == expected) + 1`, 1 or 2, and 0 when its input guards fail (`0030AC42` / "
       "`0030AC46`); 2026-10-02, OPUS)*")


def main():
    t = open(P, "rb").read().decode("utf-8")
    if NEW in t:
        print("ALREADY"); print("FAILS 0"); return 0
    if t.count(OLD) != 1:
        print("REFUSING", t.count(OLD)); print("FAILS 1"); return 1
    if "--apply" in sys.argv:
        open(P, "wb").write(t.replace(OLD, NEW, 1).encode("utf-8"))
        print("PATCHED")
    else:
        print("WOULD PATCH")
    print("FAILS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
