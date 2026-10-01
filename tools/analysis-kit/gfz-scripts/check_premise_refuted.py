#!/usr/bin/env python3
"""check_premise_refuted.py - an OPEN question whose premise the type store has already answered.

THE CLASS, and none of the thirty FINAL-AUDIT passes looks for it. `EH-4` read "not one bit's
semantics is known" of the actor storage record's flag bytes while nineteen bits carried published
meanings on nine other pages, some of them six days old. It cost FABLE a full round of
re-derivation before anyone checked (FABLE-REQ-OPUS-NO-GATE-COMPARES-A-QUESTIONS-PREMISE-AGAINST-
THE-CORPUS, 2026-09-16).

`check_questions --drift` cannot see it. It compares boxes to rows, and both agreed perfectly the
whole time, because the question was consistently OPEN in both places. **The defect is not
inconsistency between the two ledgers - it is a question that is consistent with itself and false.**

FINDING THE SUBJECT IS THE WHOLE PROBLEM, and three obvious joins all fail on the motivating case:

    the row's TEXT names a type     EH-4 never writes "ActorStorageRecord"
    the row LINKS a document        EH-4 carries no links at all
    the question owns a BOX         EH-4 is register-only; read_boxes has nothing for it

What does carry the subject is the SECTION HEADING - "## EH. The actor storage record -
2026-09-08". Dropping the id prefix and the date, stripping articles and joining the words gives
`actorstoragerecord`, which is a type the store knows. So the join is

    section heading -> type -> how many of that type's fields the DATABASE ITSELF has named

and the comparison needs no corpus sweep and no prose matching: one committed store answers it.

WHAT IT DOES NOT DO. A universal negative is narrow on purpose - "not one X is known", "nothing is
known", "no X has been established", "entirely unread". An ordinary open question about one field
("what bit 3 means is not known") is not a claim that nothing is known and must never fire. Nor
does a hit mean the question is worthless: the premise being too strong is not the same as the
question being answered, and EH-4 remained open and useful after its premise was corrected.

IT READS ZERO AT HEAD, AND THAT IS NOT A REASON TO SKIP IT. The one historical instance is in the
self-test, taken verbatim from the register as it stood before the repair, so the gate can always
demonstrate it would catch the real thing rather than asserting it.

usage: check_premise_refuted.py [--db DB] [--self-test]
"""
import argparse
import collections
import io
import os
import re
import sys

UNIVERSAL = re.compile(
    r"not one [\w' ]{0,24}(?:is|are) known|nothing[\w' ]{0,24}(?:is|has been) (?:known|read)"
    r"|no [\w' ]{0,24}(?:is|are|has been) (?:known|established|read)|entirely unread"
    r"|none [\w' ]{0,20}(?:is|are|has been) (?:known|read)", re.I)
STRUCK = re.compile(r"~~.*?~~", re.S)
CLOSED = re.compile(r"\bANSWERED\b|\bRESOLVED\b|\bCLOSED\b|\bWITHDRAWN\b|\bSUPERSED", re.I)
HEAD = re.compile(r"^#{1,6}\s+(?:[A-Z]{1,4}[.:]\s*)?(.+?)(?:\s+[-—]\s*20\d\d-\d\d-\d\d.*)?$")


def norm_subject(s):
    """'The actor storage record' -> 'actorstoragerecord'."""
    s = re.sub(r"[^A-Za-z ]", " ", s)
    return "".join(w for w in s.split() if w.lower() not in ("the", "a", "an", "and", "of")).lower()


def load_types(db):
    p = os.path.join(db, "_types", "fields.tsv")
    named, total = collections.Counter(), collections.Counter()
    if not os.path.exists(p):
        return named, total
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    hdr = lines[0].split("\t")
    I = {k: hdr.index(k) for k in hdr}
    for l in lines[1:]:
        if not l.strip():
            continue
        r = l.split("\t")
        if len(r) <= I["name"]:
            continue
        total[r[I["type"]]] += 1
        if r[I["name"]].strip() not in ("", "UNRESOLVED"):
            named[r[I["type"]]] += 1
    return named, total


# A row whose VERDICT records progress the question cell denies. FABLE measured this shape on
# 2026-09-16: three register rows carry a universal negative in the question cell that their own
# verdict refutes. Two are ANSWERED, where a question recording what was asked and a verdict
# recording the answer is the register WORKING CORRECTLY - so only an OPEN row counts.
PROGRESS = re.compile(r"\bSTARTED\b|first [\w ]{0,20}read|\bread out of\b|families read|"
                      r"\bNARROWED\b|\bADVANCED\b|every [\w ]{0,20}body (?:was )?read", re.I)


def scan_self_refuting(reg_text):
    """Rows that are OPEN, deny that anything is known, and record progress in the same row."""
    out = []
    for n, line in enumerate(reg_text.split("\n"), 1):
        m = re.match(r"\|\s*([A-Z]{1,4}-\d+)\s*\|", line)
        if not m:
            continue
        cells = line.rstrip("\n").strip("|").split("|")
        if len(cells) < 3:
            continue
        q = STRUCK.sub("", cells[1])
        v = STRUCK.sub("", "|".join(cells[2:]))
        if CLOSED.search(v):
            continue                      # answered: question asked, verdict answers. Correct.
        u = UNIVERSAL.search(q)
        p = PROGRESS.search(v)
        if u and p:
            out.append((m.group(1), n, u.group(0), p.group(0)))
    return out


def scan(reg_text, named, total):
    by_norm = {t.lower(): t for t in total}
    out, section = [], None
    for n, line in enumerate(reg_text.split("\n"), 1):
        if line.startswith("#"):
            h = HEAD.match(line)
            section = (norm_subject(h.group(1)), h.group(1).strip()) if h else None
            continue
        m = re.match(r"\|\s*([A-Z]{1,4}-\d+)\s*\|", line)
        if not m or not section:
            continue
        body = STRUCK.sub("", line[m.end():])
        if CLOSED.search(body):
            continue                      # a closed row's premise is history
        u = UNIVERSAL.search(body)
        if not u:
            continue
        t = by_norm.get(section[0])
        if t and named[t]:
            out.append((m.group(1), n, section[1], t, named[t], total[t], u.group(0)))
    return out


# The real thing, verbatim from the register before FABLE struck the premise on 2026-09-16. A gate
# whose corpus count is zero must be able to SHOW it would catch the case it was built for.
EH4 = ("## EH. The actor storage record — 2026-09-08\n"
       "| id | question | status |\n|---|---|---|\n"
       "| EH-4 | **What any flag bit means.** Eleven bytes are read-modify-written with exact "
       "masks (`&0x7F`, `&0xDF`) and **not one bit's semantics is known.** The masks are the "
       "strongest possible evidence that the bits are meaningful. | OPEN |\n")


def self_test():
    named = collections.Counter({"ActorStorageRecord": 45, "Untouched": 0})
    total = collections.Counter({"ActorStorageRecord": 89, "Untouched": 12})
    ok = True

    def check(label, got, want):
        nonlocal ok
        if got != want:
            ok = False
        print("  %s %-54s %r" % ("ok  " if got == want else "FAIL", label, got))

    check("the real EH-4 text fires", len(scan(EH4, named, total)), 1)
    check("...and names the right type",
          scan(EH4, named, total)[0][3] if scan(EH4, named, total) else None,
          "ActorStorageRecord")
    check("the same row CLOSED does not fire",
          len(scan(EH4.replace("| OPEN |", "| **ANSWERED 2026-09-16** |"), named, total)), 0)
    check("the premise STRUCK does not fire",
          len(scan(EH4.replace("**not one bit's semantics is known.**",
                               "~~**not one bit's semantics is known**~~"), named, total)), 0)
    check("a type with NO named fields does not fire",
          len(scan(EH4.replace("The actor storage record", "Untouched"), named, total)), 0)
    check("an ordinary single-field question does not fire",
          len(scan(EH4.replace("not one bit's semantics is known",
                               "what bit 3 means is not known"), named, total)), 0)
    check("a heading that matches no type does not fire",
          len(scan(EH4.replace("The actor storage record", "Some prose heading"), named, total)), 0)

    # THE SECOND TEST: a row whose own VERDICT refutes its question cell.
    pa1 = ("| PA-1 | What the slots do. All nine are overridden; none has been read. "
           "| PARTIAL - *Narrowed 2026-09-14*: every override body was read |\n")
    check("a verdict that refutes its own question fires", len(scan_self_refuting(pa1)), 1)
    check("the same row ANSWERED does not fire",
          len(scan_self_refuting(pa1.replace("PARTIAL -", "ANSWERED 2026-09-14 -"))), 0)
    check("a universal negative with NO progress does not fire",
          len(scan_self_refuting("| X-1 | none has been read. | OPEN |\n")), 0)
    check("progress with NO universal negative does not fire",
          len(scan_self_refuting("| X-2 | what slot 8 does. | PARTIAL - Narrowed |\n")), 0)
    return ok


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", default=os.path.join("Database", "FFXII TZA"))
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args()
    if a.self_test:
        print("check_premise_refuted self-test")
        return 0 if self_test() else 1

    reg = os.path.join(a.db, "_index", "OPEN-QUESTIONS.md")
    if not os.path.exists(reg):
        print("no register at %s" % reg)
        return 2
    named, total = load_types(a.db)
    if not total:
        print("no type store; nothing to compare a premise against")
        return 2

    import contextlib
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        control = self_test()
    if not control:
        print("CONTROL FAILED: the self-test does not pass, so the count below means nothing.")
        return 2

    reg_text = io.open(reg, encoding="utf-8", errors="replace").read()
    hits = scan(reg_text, named, total)
    selfref = scan_self_refuting(reg_text)
    print("an open question whose premise the type store already answers\n")
    print("  types in the store            : %d" % len(total))
    print("  control                       : the real pre-repair EH-4 text still fires")
    print("  refuted by the TYPE STORE        : %d" % len(hits))
    print("  refuted by the ROW'S OWN VERDICT : %d" % len(selfref))
    if not hits and not selfref:
        print("\nno open question denies knowledge that the store or its own verdict records.")
        return 0
    print()
    for qid, n, sec, t, nm, tot, phrase in hits:
        print("  %s  (register line %d, section %r)" % (qid, n, sec))
        print("      says \"%s\"" % phrase)
        print("      but the store names %d of %s's %d fields" % (nm, t, tot))
    for qid, n, phrase, prog in selfref:
        print("  %s  (register line %d)" % (qid, n))
        print("      the question cell says %r" % phrase)
        print("      while the SAME ROW's verdict records %r" % prog)
    print("\n  The premise being too strong is not the same as the question being answered.")
    print("  Correct the premise; the question may well still be open and useful.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
