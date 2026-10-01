"""test_check_questions_partial.py - the partial marker '- [~]' and '*' bullets are boxes, and a partial box is OPEN
(OPUS, 2026-10-01, FABLE-REQ-OPUS-CHECKQUESTIONS-PARTIAL-MARKER-0930). Builds a throwaway database in a temp dir."""
import os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_questions as C

fails = 0


def check(tag, ok, text):
    global fails
    fails += 0 if ok else 1
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))


with tempfile.TemporaryDirectory() as db:
    os.makedirs(os.path.join(db, "10-Pages"))
    with open(os.path.join(db, "10-Pages", "page.md"), "w", encoding="utf-8") as f:
        f.write("# A page\n\n"
                "- [x] **ZZ-1.** a ticked box\n"
                "- [~] **ZZ-2.** a partial box\n"
                "  continued on a two-space line\n"
                "* [ ] **ZZ-3.** an asterisk box\n"
                "- [ ] **ZZ-4.** an open box\n")
    boxes = {tuple(sorted(ids)): ticked for _rel, _line, ticked, ids, _txt in C.read_boxes(db)}
    check("P1", len(boxes) == 4, "four boxes read (dash, partial, asterisk, open): %d" % len(boxes))
    check("P2", boxes.get(("ZZ-2",)) is False, "the partial box is OPEN (not ticked): %r" % boxes.get(("ZZ-2",)))
    check("P3", boxes.get(("ZZ-3",)) is False, "the asterisk box is read and open: %r" % boxes.get(("ZZ-3",)))
    check("P4", boxes.get(("ZZ-1",)) is True, "control: the ticked box stays ticked: %r" % boxes.get(("ZZ-1",)))
print("FAILS %d" % fails)
