#!/usr/bin/env python3
"""check_questions.py - make the question ledger countable.

WHY THIS EXISTS
---------------
The mission's completion gate is "unresolved = 0", so the question ledger has to
be countable by machine. On 2026-09-02 an audit found it was not:

  * 20 distinct status markers were in use across 411 rows
    (ANSWERED / CLOSED / RECOVERED / ADVANCED / PARTLY ANSWERED / SHARPENED /
     BOUNDED / CHARACTERISED / LEANS NO / IN PROGRESS / STILL OPEN / OPEN / ...)
  * status lives in a different COLUMN depending on whether the row has a link
    cell, so "the last cell" is not the status
  * `progress.py` never read this table at all - its `questions_closed` metric
    counts per-document `- [ ]` checkboxes, a SECOND ledger that had drifted
    from this one.

This tool reads the table with a documented precedence, reports the counts, and
cross-checks the two ledgers against each other.

A CAUTION, LEARNED THE HARD WAY
-------------------------------
The first detector written for this required an entire bolded token to be
upper-case, so `**ANSWERED - yes.**` fell through and 67 rows looked unmarked.
The status keyword is a PREFIX of the bolded run, not the whole of it. Match a
prefix. (Same session also produced three other instruments that returned their
answer by construction - see _index/EVIDENCE-STANDARD.md.)

PRECEDENCE (first match wins)
-----------------------------
1. a cell that is exactly OPEN / BLOCKED / IN PROGRESS / PARTIAL / CLOSED / ANSWERED
2. the first bolded run whose text STARTS WITH a known keyword
3. a row with no answer cell at all  ->  OPEN
4. anything else                     ->  UNMARKED (reported, never guessed)

Rule 4 is deliberate: an unmarked row is a defect to fix by hand, not something
to classify heuristically. Never change a status to make a count come out.
"""
import argparse, io, os, re, sys, collections

CLOSED = ("ANSWERED", "CLOSED", "RECOVERED", "RESOLVED", "IDENTIFIED", "CONFIRMED",
          "ALREADY ANSWERED")
BLOCKED = ("STILL OPEN", "BLOCKED")
# A question that was MALFORMED, superseded, or turned out not to describe a real thing is
# neither answered nor outstanding. Counting it OPEN says work remains that does not; counting
# it ANSWERED claims a finding nobody made. It gets its own bucket and leaves the score's
# denominator. Two rows in this register read "DISSOLVED - the premise was wrong".
# `NO ADMISSIBLE SOURCE` joins this bucket and is NOT a synonym of the others (OPUS ruling
# 2026-09-15, EVIDENCE-STANDARD addendum 15bk). Every other word here says the question should not
# have been asked. This one says the opposite: it is well-formed, its mechanism is established at
# tier 1, and the part that remains is a fact about PEOPLE rather than about the binary - a
# designer's chosen name, or whether a shipped behaviour was deliberate. Intent is not in the
# executable and no admissible source carries it.
#
# The guard is at the ROW, not here: the ruling requires the mechanism cited, the inadmissible
# source named, THE NEGATIVE ACTUALLY CHECKED with the scan that was run, and a reviewer who is not
# the author. Adding the word makes the ruling operative; it closes nothing by itself.
#
# It is deliberately NOT for a row whose answer needs only a live run - a runtime observation IS an
# admissible source. Those close as SUPERSEDED when the claim is already tier-1 static, and stay
# OPEN otherwise. Expensive is not unanswerable.
WITHDRAWN = ("WITHDRAWN", "DISSOLVED", "SUPERSEDED", "NOT A DEFECT", "NOT A QUESTION")
# MOVED OUT OF `WITHDRAWN` 2026-09-17, on FABLE-ANSWER-OPUS-NAS-SCORES-CLOSED-SIGNED. It sat in that
# tuple with ten lines of comment above it explaining that it is NOT a synonym of the others - and
# A BUCKET WHOSE OWN COMMENT HAS TO EXCEPT ITS NEWEST MEMBER IS MIS-BUCKETED. Every other word there
# says the question SHOULD NOT HAVE BEEN ASKED; this one says the opposite - the question is well
# formed, its mechanism is established at tier 1, and what remains is a fact about PEOPLE that no
# admissible source carries.
#
# THE TWO READERS DISAGREED BY DESIGN, WHICH IS WORSE THAN EITHER BEING WRONG: progress.py already
# counts it in REG_CLOSED, so the same row scored CLOSED there and left the denominator entirely
# here. Two instruments that disagree on purpose are two instruments nobody can cite without saying
# which one they used. It now counts CLOSED in both.
#
# AND THE INCENTIVE POINTED THE WRONG WAY, which is FABLE's argument and the reason this is not
# cosmetic: the four conditions this status requires - mechanism cited, inadmissible source named,
# THE NEGATIVE ACTUALLY CHECKED, and a reviewer who is not the author - are MORE work than an
# ordinary answer, and it was bucketed with verdicts that require none. A status created so an
# unanswerable question can be closed HONESTLY must not be cheaper to award than answering one.
NO_ADMISSIBLE = ("NO ADMISSIBLE SOURCE",)
# OUT OF EVIDENCE BOUNDARY (FRONTIER ruling 2026-09-27, batch-K extension): the class-3
# terminal state. NOT a synonym of NO ADMISSIBLE SOURCE - that one is a fact about PEOPLE
# (a designer's name or intent) no source carries; this one is a fact about the BUILD whose
# only carrier is an artefact outside the admitted evidence base (a debug build never
# shipped, a comparison build the program does not admit). The question stays well-formed
# and honestly unanswered; the status counts CLOSED so the gate can complete, and the row
# keeps its residue text. Same guard as NAS, applied per row: the excluded source named
# exactly, why no admitted source carries the answer stated, the negative actually checked,
# a reviewer who is not the author. Rows with a live carrier do not qualify.
NO_ADMISSIBLE += ("OUT OF EVIDENCE BOUNDARY",)
PARTIAL = ("ADVANCED", "PARTIAL", "PARTLY", "SHARPENED", "BOUNDED", "CHARACTERISED",
           "REVISED", "SUPPORTED", "IN PROGRESS", "LEANS", "VALUES ANSWERED",
           "LOCATION ANSWERED", "ANSWERED STRUCTURALLY", "THE FILE IS IDENTIFIED")
BARE = {"OPEN": "OPEN", "BLOCKED": "BLOCKED", "IN PROGRESS": "PARTIAL",
        "PARTIAL": "PARTIAL", "CLOSED": "ANSWERED", "ANSWERED": "ANSWERED"}

# Documents also spawn SUB-QUESTIONS as `B-2/a` .. `B-2/e`.  Without the `/x` alternative every
# one of them collapses onto its parent, so five open sub-parts read as five stale boxes for an
# ANSWERED parent -- **the parent really is answered; the sub-parts are new questions it spawned.**
# Matching them separately turns a false "the answer is stale" into a true "these ids have no row".
QID = r"[A-Z]+-\d+(?:/[a-z]|[a-z])?"


# A CELL ENDS AT AN UNESCAPED PIPE, and only there (GFM). `rest.split("|")` also split on `\|`,
# so an escaped pipe inside a verdict moved the "last cell" into the middle of it; and a row
# carrying an UNESCAPED pipe inside a code span was read at a different cell boundary from the one
# every renderer draws. Measured 2026-09-15 (OPUS): 123 register rows differed from their table's
# header width, and one of them - EE-1, whose last cell is `**ANSWERED 2026-09-13 (FABLE)**` -
# was scored PARTIAL because the split landed after the `||` inside its code span and the
# fallback read the question cell's first bold run. The rows were normalised in the same commit
# (escapes and empty cells only, wording unchanged, per-row status control) and
# `read_structure` below now fails the gate on any row that drifts again.
CELL = re.compile(r"(?<!\\)\|")

# A STRUCK VERDICT IS NOT THE LIVE VERDICT. This register corrects a row by striking the old
# verdict and appending the new one in the same cell -- `~~**ANSWERED ...**~~ **PARTLY ANSWERED
# 2026-09-14 (FABLE) ...**` -- and `lead`'s `lstrip("*~ \t")` removed the `~~` along with the
# bold markers and then read the RETRACTED word as the row's status.
#
# Stripping `*` is deliberate: a bold lead is how every row is written. Stripping `~` was not
# deliberate; it silently gave a withdrawn verdict priority over the one that replaced it.
#
# MEASURED BEFORE CHANGING ANYTHING, 2026-09-20 (OPUS), over all 1551 rows: FOUR verdict cells
# open with a struck verdict, and only ONE is actually mis-scored -- AA-2, scored ANSWERED where
# the live verdict is PARTLY ANSWERED. UQ-208 restates ANSWERED after the strike and is
# unaffected. AB-7 (`REOPENED AND ANSWERED`) and AX-2 (`CORRECTED`) carry live leads this
# vocabulary does not know, so they fall past `lead` to the bold-span scan below, which still
# reads the struck span and still returns ANSWERED -- which is the right bucket for both, by the
# wrong route. THE SAME HAZARD IS THEREFORE STILL PRESENT ONE LAYER DOWN, deliberately: removing
# it here would turn two correctly-scored rows into UNKNOWN, and the fix for those two is to
# normalise the ROWS, which is this module's own stated doctrine and FABLE's call rather than
# this reader's. Routed as OPUS-REQ-FABLE-STRUCK-VERDICT-LEADS.
#
# The precedent is parity_status.py, which normalises `~~claim~~ correction` for claim identity
# and reports a struck-but-verdicted claim as its own named condition rather than dropping it.
LEAD_STRUCK = re.compile(r"^\s*~~(.+?)~~\s*", re.S)


def live_lead(cell):
    """The verdict cell with a leading STRUCK verdict removed, so the live one is read."""
    return LEAD_STRUCK.sub("", cell or "")


def classify(rest):
    cells = [c.strip() for c in CELL.split(rest) if c.strip() != ""]
    if cells and cells[-1] in BARE:
        return BARE[cells[-1]], cells
    # The ANSWER CELL's own leading words are the status, and reading them directly is
    # immune to a defect the bold-span scan below has:
    #
    #   `\*\*([^*]{2,}?)\*\*` cannot match a ONE-CHARACTER bold span such as `**Y**`.
    #   Having failed there, the scanner pairs that span's CLOSING `**` with the NEXT span's
    #   OPENING `**` -- and from that point on it reads the GAPS BETWEEN bold spans instead of
    #   the spans themselves.  Every status after the first short span is invisible.
    #
    # Measured on 2026-09-03: L-7's answer cell begins `**ANSWERED 2026-09-02 ...**` and the row
    # was classified OPEN, because its question cell contains `**Y**`.  The row had been correct
    # in the register for a day; the reader was wrong.  questions_closed reads this same table,
    # so the project score was under-counting answered questions.
    # `cells` excludes the id, so an answered row has TWO cells: question, answer.
    # Requiring more than two skipped every one of them -- the first version of this fix
    # changed nothing and said so, which is why the guard got checked.
    lead = live_lead(cells[-1]).lstrip("*~ 	").upper()[:48] if len(cells) >= 2 else ""
    # NO_ADMISSIBLE is tested BEFORE the others and returns ANSWERED: it is a closed question, not a
    # retracted one, and progress.py has counted it that way since the ruling.
    for group, verdict in ((BLOCKED, "BLOCKED"), (NO_ADMISSIBLE, "ANSWERED"),
                           (WITHDRAWN, "WITHDRAWN"),
                           (CLOSED, "ANSWERED"), (PARTIAL, "PARTIAL")):
        for k in group:
            if lead.startswith(k):
                return verdict, cells
    if lead.startswith("OPEN"):
        return "OPEN", cells

    body = " ".join(cells)
    for m in re.finditer(r"\*\*([^*]{2,}?)\*\*", body):
        # only the LEADING words carry the status; a long bold lead is common
        tok = m.group(1).upper().lstrip()[:48]
        for k in BLOCKED:
            if tok.startswith(k):
                return "BLOCKED", cells
        for k in CLOSED:
            if tok.startswith(k):
                return "ANSWERED", cells
        for k in PARTIAL:
            if tok.startswith(k):
                return "PARTIAL", cells
        if tok.startswith("OPEN"):
            return "OPEN", cells
    # A row with a question and NO answer cell is genuinely open.
    if len(cells) < 2:
        return "OPEN", cells

    # A row that HAS an answer cell whose lead word this vocabulary does not know is NOT open --
    # it is unreadable, and the two are worth telling apart.
    #
    # Measured 2026-09-03 by repos-78: **36 rows across 24 distinct lead words** fell through to
    # OPEN silently -- `NARROWED` (6), `LARGELY ANSWERED` (3), `DONE` (3), `DISSOLVED` (2),
    # `MEASURED PROPERLY` (2), `HALF ANSWERED` (2), `SUPERSEDED`, `DOCUMENTED`, `TRIAGED`,
    # `NEGATIVE NOW EXHAUSTIVE` ... **At least two dozen are demonstrably not open**, so
    # `questions_closed` under-counts and the totals still look stable.
    #
    # The fix for the ROWS is to normalise them, not to add 24 keywords -- teaching a reader more
    # synonyms teaches it to guess. The fix for the READER is this: **say so instead of defaulting.**
    # An unknown status word is today indistinguishable from an unanswered question; that silence
    # is the property being removed. `DISSOLVED` matters most -- it means *the premise was wrong*,
    # and a register that renders a withdrawn question as OPEN cannot tell "nobody answered this"
    # from "this should never have been asked".
    return "UNKNOWN", cells


def read_table(db):
    p = os.path.join(db, "_index", "OPEN-QUESTIONS.md")
    with io.open(p, encoding="utf-8", errors="replace") as fh:
        t = fh.read()
    out = {}
    dupes = []
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % QID, t, re.M):
        st, _ = classify(m.group(2))
        if m.group(1) in out:
            dupes.append(m.group(1))
        out[m.group(1)] = st
    return out, sorted(set(dupes))


def row_cells(line):
    """GFM cells of one table row: outer pipes are delimiters, escaped pipes are content."""
    t = line.strip()
    if t.startswith("|"):
        t = t[1:]
    if t.endswith("|") and not t.endswith("\\|"):
        t = t[:-1]
    return CELL.split(t)


def read_structure(db):
    """Register rows whose GFM cell count differs from their table's header.

    A wider row has its excess dropped by every renderer - usually the LAST cell, which is the
    authoritative verdict. A narrower row renders a cell as blank, and a row missing its closing
    pipe continues mid-cell into following lines (every renderer ends the table at the first
    non-pipe line, so the continuation renders as stray paragraphs and the verdict cell is
    truncated). None of these changes a count, which is why no counting check ever saw them.

    The metric is delimiter-count, matching _index/candidates/register-pipe-escapes/
    cell_count_scan.py: a well-formed row starts AND ends with '|', so the number of
    unescaped-pipe fields minus the two outer empty fields is the cell count. A row without its
    closing pipe undercounts by one and is caught.

    Repair rule (FABLE-NOTICE-FRONTIER-CELL-REPAIR-FOLD, 2026-09-28): when folding a malformed
    row, the STATUS is the last NON-EMPTY split field - the field after a row's final '|' is
    empty and is NOT a cell. Surplus middle fields are folded by rejoining on raw delimiters and
    escaping every internal pipe as '\\|' - never rewrite them as ' - ' (that corrupts code like
    '0x8000|n'), and never fold the status into the question text."""
    p = os.path.join(db, "_index", "OPEN-QUESTIONS.md")
    lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
    bad = []
    i = 0
    while i < len(lines):
        t = lines[i].strip()
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if t.startswith("|") and nxt.startswith("|") and set(nxt) <= set("|-: "):
            width = len(row_cells(t))
            j = i + 2
            while j < len(lines) and lines[j].strip().startswith("|"):
                n = len(CELL.split(lines[j].strip())) - 2
                if n != width:
                    bad.append((j + 1, row_cells(lines[j])[0].strip()[:16], width, n))
                j += 1
            i = j
        else:
            i += 1
    return bad


def live_dirs(root, dirs):
    """The subdirectories of `root` whose pages are live ledger entries. Skipped: `_index` and `_templates`; `retained`
    preimages (see read_boxes); and any NESTED DATABASE - a directory holding its own `_index/OPEN-QUESTIONS.md`. A
    verifier's fixture database is not part of this one: on 2026-09-29 two fixture copies under
    `_experiments/evidence/migration-my-progress-independent/` cited W-902 / W-903, which have no row here, and the
    governing gate read UNMET on them (OPUS). test_check_questions_nested.py holds the case."""
    return [d for d in dirs if d not in ("_index", "_templates", "retained")
            and not os.path.isfile(os.path.join(root, d, "_index", "OPEN-QUESTIONS.md"))]


def read_boxes(db):
    """Every '- [ ]' / '- [x]' block in every document, with the question ids it names."""
    boxes = []
    for root, dirs, files in os.walk(db):
        # 'retained' dirs hold byte-identical page copies kept as hash-verified consumer
        # preimages (FABLE-REQ-FRONTIER-CHECKLISTS-SKIP-RETAINED-PREIMAGES, 2026-09-27).
        # Their boxes are receipts, not live ledger entries: counting them makes an
        # answered row report STALE on the immutable copy and refuses the publish.
        dirs[:] = live_dirs(root, dirs)
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, db).replace("\\", "/")
            lines = io.open(p, encoding="utf-8", errors="replace").read().split("\n")
            i = 0
            while i < len(lines):
                if re.match(r"^\s*-\s*\[[x ]\]", lines[i]):
                    # A BLOCK ENDS AT THE NEXT BOX, NOT AT SIX SPACES. This required a
                    # continuation line to start with SIX spaces, and markdown continuation under
                    # "- [ ]" is conventionally TWO. The corpus uses both, so an id written on a
                    # two-space continuation was invisible to every reader built on this function.
                    #
                    # THAT IS WHAT MINTED THE DUPLICATE IDS. UQ-91's box already said `**FS-1.**`
                    # - on its second line, indented two spaces. The box therefore read as having
                    # no id, gen_unidentified_questions listed it as unidentified, and the
                    # 2026-09-14 pass gave it a fresh UQ-, putting one question in the register
                    # twice. Nine went that way (FS-1/UQ-91, FI-1/UQ-93, FI-3/UQ-94, FF-4/UQ-96,
                    # FJ-4/UQ-98, FE-4/UQ-119, FT-2/UQ-120, FO-5/UQ-127, FW-1/UQ-217) and FABLE
                    # merged them, then asked for the durable half
                    # (FABLE-REQ-OPUS-THE-ID-GENERATOR-CREATES-ALIASES...). The generator is not
                    # the bug: it mints an id for a box this reader says has none, and it was
                    # telling the truth about what it could see.
                    #
                    # MEASURED BEFORE CHANGING, over 1,359 blocks: 286 blocks grow, 42 change the
                    # ids they carry, and ALL 42 CHANGES ARE GAINS - no block loses or swaps an id.
                    # All 42 are TICKED boxes whose ids the register ALREADY records as CLOSED,
                    # so no register row changes state and check_questions still reports
                    # "questions consistent" with 0 ticked boxes calling an open question. They
                    # escaped the minting only because gen_unidentified_questions lists UNTICKED
                    # boxes.
                    #
                    # THE HEADLINE METRIC DOES MOVE, and it should: questions_closed goes
                    # 1341/2009 to 1299/1967, minus 42 from BOTH sides, because those 42 were
                    # counted TWICE - once as a closed page checkbox and once as the closed
                    # register row it could not be matched to. The overlap count rises 964 -> 1006
                    # by the same 42. The percentage falls, 66.75% to 66.04%, which is what
                    # removing equal amounts from both sides of a fraction below one does; the
                    # lower figure is the true one and the higher one was double counting.
                    # 2026-09-16, OPUS.
                    block = [lines[i]]
                    j = i + 1
                    while (j < len(lines) and lines[j].strip()
                           and lines[j][:1] in (" ", "\t")
                           and not re.match(r"^\s*-\s*\[[x ]\]", lines[j])):
                        block.append(lines[j])
                        j += 1
                    txt = "\n".join(block)
                    # A box's OWN id is the LABEL FORM - the id bolded with its period inside
                    # the bold, `**BQ-3.**` - wherever it sits in the block. A box with no
                    # label-form id belongs to the FIRST bolded id in it. Every other bolded id
                    # is a CROSS-REFERENCE and neither opens nor closes that id's row.
                    # (FABLE ruling 2026-09-14, OPEN-QUESTIONS.md header, "Which id a checkbox
                    # belongs to" - "Box readers should implement this rule rather than
                    # attribute a box to every id it mentions.")
                    #
                    # The earlier fix (2026-09-03) caught label form only at the START of the
                    # first line, so `... tracked separately as **BG-6**. **BG-1.**` let BG-6
                    # in through the fallback as a co-owner - the sentence that OPENS a new
                    # question was being read as TICKING it.
                    # BACKTICKS INSIDE THE BOLD. The corpus writes an id three ways - `**BQ-3.**`,
                    # `**\u0060BQ-3\u0060.**` and `See **\u0060UQ-383\u0060**` - and these patterns only
                    # matched the first, because both required the id IMMEDIATELY after the `**`.
                    # An id in bold-with-backticks was invisible, which is the same class of
                    # defect as the six-space continuation above: the reader could not see a form
                    # the corpus actually uses, and everything built on it inherited the blindness.
                    #
                    # Found by regenerating UNIDENTIFIED-OPEN-QUESTIONS.md after the continuation
                    # fix: it reported exactly one unticked box with no id, and that box reads
                    # `See **\u0060UQ-383\u0060**` - the row FABLE created yesterday from the AC-6 ruling.
                    #
                    # MEASURED BEFORE CHANGING, over 1,359 blocks: 58 gain an id and NONE changes
                    # or loses one. All 58 ids are ALREADY CLOSED in the register, so no row
                    # changes state. 57 are ticked; the 58th is the UQ-383 box.
                    #
                    # The first measurement of this said SIX, and it was wrong: it read the
                    # truncated display string read_boxes returns as its last element rather than
                    # the block text, so every block was cut at about seventy characters and most
                    # ids fell off the end. Measuring the wrong input is how a change gets sized at
                    # a tenth of itself. 2026-09-16, OPUS.
                    label = re.search(r"\*\*\s*`?(%s)`?\s*(?:\([^)]*\))?\s*\.\s*`?\*\*" % QID, txt)
                    first = re.search(r"\*\*\s*`?(%s)\b" % QID, txt)
                    ids = ({label.group(1)} if label
                           else ({first.group(1)} if first else set()))
                    boxes.append((rel, i + 1, "[x]" in lines[i], ids,
                                  block[0].strip()[:64]))
                    i = j
                else:
                    i += 1
    return boxes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--db", required=True)
    ap.add_argument("--drift", action="store_true",
                    help="list every checkbox disagreeing with the table")
    a = ap.parse_args()

    table, dupes = read_table(a.db)
    boxes = read_boxes(a.db)
    counts = collections.Counter(table.values())

    print("QUESTION LEDGER  (_index/OPEN-QUESTIONS.md)")
    print("   rows: %d" % len(table))
    for k in ("ANSWERED", "PARTIAL", "OPEN", "BLOCKED", "UNMARKED"):
        # OPEN/BLOCKED/PARTIAL always print - goal_gate requires each line and fails
        # closed when one is missing, so a count of zero must still say "0"
        # (OPUS-NOTICE-FRONTIER-GATE-UNREADABLE-AT-ZERO-BLOCKED, 2026-09-27).
        if counts.get(k) or k in ("OPEN", "BLOCKED", "PARTIAL"):
            print("      %-9s %d" % (k, counts[k]))

    # RULE 4 WAS SILENT FOR ITS WHOLE LIFE. `classify` returns "UNKNOWN" for a row whose verdict word
    # the vocabulary does not know; this filter asked for "UNMARKED", a value nothing ever returns, so
    # the list was always empty and the docstring's *"reported, never guessed"* reported nothing.
    # Found 2026-09-15 (OPUS) while surveying the register: five rows were in that state - ES-1 (DONE),
    # BQ-27 (NARROWED), CH-1 (RECORDED), CO-3 (EXTRACTED), CX-1 (REFUTED).
    #
    # FABLE normalised all five in c6e4308c, each adjudicated from the row's CONTENT rather than its
    # lead word, so `unknown` is now empty and rule 4 FAILS the gate (2026-09-15, OPUS). It was
    # reported-not-failed for exactly as long as failing it would have turned the gate red for every
    # publisher over wording that was not the reporter's to change. The repair remains normalising the
    # ROW: do not add a synonym to the vocabulary to make this line go quiet.
    unmarked = sorted(q for q, s in table.items() if s == "UNMARKED")
    unknown = sorted(q for q, s in table.items() if s == "UNKNOWN")
    if dupes:
        print("      DUPLICATE ids: %d  (%s)" % (len(dupes), " ".join(dupes)))
    print()
    print("DOCUMENT CHECKLISTS")
    print("   checkbox blocks: %d   ticked: %d" % (
        len(boxes), sum(1 for b in boxes if b[2])))

    # DANGLING: an id a document cites that has no row in the table at all.
    # Found 2026-09-02 - H-1 was cited by 18-Audio and existed in neither ledger,
    # invisible to both because each only checks what it itself contains.
    cited = set()
    for _rel, _ln, _ch, ids, _txt in boxes:
        cited |= ids
    for root, dirs, files in os.walk(a.db):
        dirs[:] = live_dirs(root, dirs)
        for fn in files:
            if fn.endswith(".md"):
                body = io.open(os.path.join(root, fn), encoding="utf-8",
                               errors="replace").read()
                cited |= set(re.findall(r"\*\*(%s)\.\*\*" % QID, body))
    dangling = sorted(cited - set(table))

    ans = {q for q, s in table.items() if s == "ANSWERED"}
    stale = [b for b in boxes if not b[2] and (b[3] & ans)]
    early = [b for b in boxes if b[2] and b[3] and not (b[3] & ans)
             and all(table.get(q, "OPEN") == "OPEN" for q in b[3])]

    print()
    print("CROSS-CHECK")
    print("   unticked boxes whose question the table calls ANSWERED : %d" % len(stale))
    print("   ticked boxes whose question the table still calls OPEN : %d" % len(early))
    if unmarked:
        print("   rows with no status marker                             : %d  (%s)"
              % (len(unmarked), " ".join(unmarked)))
    # CONSTRUCTED CONTROL FOR RULE 4, because this line's whole history is a zero that meant
    # nothing. A row whose answer cell leads with a word the vocabulary does not know must classify
    # UNKNOWN, and a row leading with a known one must not. Without this, "0 unknown" is once again
    # indistinguishable from a filter that can never match - which is the exact defect repaired
    # today, and it went unnoticed for the tool's whole life.
    _r4 = classify(" X-1 | does the fade ramp clamp? | **HARVESTED 2026-09-15 (NOBODY)** ")[0]
    _r4ok = classify(" X-2 | same | **ANSWERED 2026-09-15 (NOBODY)** ")[0]
    if (_r4, _r4ok) != ("UNKNOWN", "ANSWERED"):
        print("   RULE-4 CONTROL FAILED - classify returned %r/%r, expected UNKNOWN/ANSWERED;"
              " the unknown count below asserts nothing" % (_r4, _r4ok))
        unknown = list(unknown) + ["CONTROL"]
    if unknown:
        print("   rows whose verdict word this vocabulary does not know  : %d  (%s)"
              % (len(unknown), " ".join(unknown)))
        print("      NORMALISE THE ROW, do not add a synonym - see the comment above `unknown`")
    if dangling:
        print("   ids cited by a document with NO row in the table       : %d  (%s)"
              % (len(dangling), " ".join(dangling)))

    # CONSUMER DRIFT, report-only (FABLE-REQ-FRONTIER-STALE-OPEN-CLAIM-REPORT).
    # Pages that still call an ANSWERED/CLOSED row open are consumers the
    # answer never reached - but a dated falsification sentence kept as
    # history, or an id cited for an unanswered sub-scope, is a legitimate
    # hit, so the count is printed for hand review and NEVER counted in `bad`.
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import open_claim_drift
        _hits = open_claim_drift.drift_hits()
        drift = [h for h in _hits if h[0] != "SCANNER-MISSING"]
        for h in _hits:
            if h[0] == "SCANNER-MISSING":
                print("   DRIFT SCANNER MISSING: %s" % h[2])
    except Exception as e:
        drift = None
        print("   DRIFT SCAN FAILED: %r" % e)
    if drift is not None:
        print("   open-claim drift candidates (hand review, not a gate): %d"
              % len(drift))
        if a.drift:
            for qid, st, rel, ln, txt in drift:
                print("      %-8s %s:%s %s" % (qid, rel[-60:], ln, txt[:60]))

    # PREMISE DRIFT, report-only (EC-3 / FRONTIER-TODO-REGISTER-INSTRUMENT-
    # BACKLOG): rows citing a figure the owning page has since struck.
    # RETRACTED-class hits are the strong candidates; struck+live counts are
    # reported for completeness. Never counted in `bad`.
    try:
        import premise_drift
        _ph, _checked, _unlinked = premise_drift.scan(a.db)
        strong = [h for h in _ph if h[2] == "RETRACTED"]
    except Exception as e:
        _ph, strong = None, None
        print("   PREMISE-DRIFT SCAN FAILED: %r" % e)
    if _ph is not None:
        print("   premise-drift candidates (EC-3; hand review): "
              "%d retracted-only, %d struck+live (%d rows checked)" %
              (len(strong), len(_ph) - len(strong), _checked))
        if a.drift:
            for qid, v, cls, rel in strong:
                print("      %-8s %s %s" % (qid, v, rel[-70:]))

    structure = read_structure(a.db)
    # Constructed control, so a zero is a property of the register and not of the scanner: a
    # three-cell header with one row carrying a code-span pipe, one row with an escaped pipe and
    # one row missing its closing pipe must yield exactly the first and the third.
    _probe = ["| ID | Q | Status |", "|---|---|---|", "| X-1 | `a | b` | OPEN |",
              "| X-2 | a \\| b | OPEN |", "| X-3 | a | OPEN"]
    _w = len(row_cells(_probe[0]))
    if [len(CELL.split(r.strip())) - 2 != _w for r in _probe[2:]] != [True, False, True]:
        print("   STRUCTURE CONTROL FAILED - the cell splitter is wrong; no structure result")
        structure = [(0, "CONTROL", 0, 0)]
    print("   rows whose cell count differs from their table header  : %d" % len(structure))
    for ln, rid, w, n in structure[:40]:
        print("      L%-6d %-16s header %d, row %d" % (ln, rid, w, n))

    if a.drift:
        for label, group in (("STALE (tick it, or correct the table)", stale),
                             ("EARLY (untick it, or answer the table row)", early)):
            if group:
                print()
                print("  %s" % label)
                for rel, ln, ch, ids, txt in group:
                    print("     %-52s:%-4d %-9s %s"
                          % (rel.split("/")[-1][:52], ln,
                             ",".join(sorted(ids)), txt[:52]))

    bad = (len(stale) + len(early) + len(unmarked) + len(unknown) + len(dupes)
           + len(dangling) + len(structure))
    print()
    if bad == 0:
        print("questions consistent: the table and the document checklists agree")
    else:
        print("QUESTION LEDGER INCONSISTENT: %d item(s) - rerun with --drift" % bad)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
