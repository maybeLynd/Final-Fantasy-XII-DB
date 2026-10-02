"""apply_rc5.py [--apply] - OPUS's non-author ruling on register row RC-5 (FABLE-REQ-OPUS-RC5-DISPOSITION-1002, 2026-10-02).

Prepends an ANSWERED verdict to RC-5's status cell and keeps FABLE's consolidating cell after it as "Earlier cell,
kept". Idempotent: a second run reports ALREADY. FAILS n.
"""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REG = os.path.normpath(os.path.join(HERE, "..", "..", "OPEN-QUESTIONS.md"))

OLD = "| **OPEN - every static item settled 2026-10-02 (FABLE, consolidating):"
NEW = ("| **ANSWERED 2026-10-02 (OPUS, non-author ruling on FABLE-REQ-OPUS-RC5-DISPOSITION-1002)** - no static question "
       "remains. Every value the event-slot routes store is one of two kinds. (1) An authored constant: the 274 "
       "`debug_eventload` operands, the `+0x24` set ids of the rows `00306BD0` hands to `00309230`, the constant and "
       "increment `startscene` operands, with no region arm changing an answer ([`rc5b-event-slot-residue-0930`]"
       "(candidates/rc5b-event-slot-residue-0930/README.md), re-run at `9dc01b7b1`; the 4 counter-kind "
       "`eventread_e8` operands are {0}). (2) A value a player supplies in one session, whose domain is static: the "
       "number typed at `evctrl.ebp`'s `event_menu` debug prompt (1 to 9999), `str_z0000`'s second-menu loop count "
       "(0 to 127, the s8 store limit), and the path an event takes within its bounded counters "
       "([`rc5-counter-loops-fable-1002`](candidates/rc5-counter-loops-fable-1002/README.md) and "
       "[`rc5-main-once-fable-1002`](candidates/rc5-main-once-fable-1002/README.md), both ACCEPTed by SWE2-AUDIT-SEM). "
       "Which value a given session supplies is an input, not a fact of the image. OPUS re-read the index clamp the "
       "array domains rest on: `ebx` is zeroed at `00262440+0x1D` and unchanged in the loop, so `00262440+0xCC` to "
       "`+0xDB` (`cmovns` then `cmovl`) holds each popped index in [0, dim-1]. *Earlier cell, kept:* "
       "**OPEN - every static item settled 2026-10-02 (FABLE, consolidating):")


def main():
    t = io.open(REG, encoding="utf-8", newline="").read()
    if NEW in t:
        print("ALREADY RC-5"); print("FAILS 0"); return 0
    n = t.count(OLD)
    if n != 1:
        print("OLD found %d times" % n); print("FAILS 1"); return 1
    if "--apply" in sys.argv:
        io.open(REG, "w", encoding="utf-8", newline="").write(t.replace(OLD, NEW))
        print("PATCHED RC-5")
    else:
        print("WOULD PATCH RC-5")
    print("FAILS 0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
