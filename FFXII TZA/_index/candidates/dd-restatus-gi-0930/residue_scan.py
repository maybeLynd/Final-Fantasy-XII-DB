"""residue_scan.py LISTFILE - for each page, report residue in two ways:

  A  every line outside struck spans and outside the status line carrying a residue word
     (not yet/unknown/unresolved/still open/open question/TODO/not read/unverified/unclear/
     to be determined/remains open) - the residue words ANYWHERE, headings included;
  B  every non-empty line of CONTENT under a residue-style heading ('## Not read', 'Not yet
     established', 'Unresolved', 'Open', 'Remaining', 'Unknown', 'Limits' ...) - bullets AND
     paragraphs. The residue word must START the heading text ('## The remaining walks' is a
     content heading, not a residue section).

Widened 2026-10-01 on SWE2-AUDIT-SEM's REJECT of c97af7156 (auditsem-review-gi-restatus-0930):
the old scan read only BULLETS under residue-style headings, so the 80-97 '## Not read' PARAGRAPH
printed as a heading with no content, and residue words in tables/body prose/front matter were
never seen. Strike spans are tracked ACROSS lines - a multi-line struck bullet's continuation
lines are not live residue. A reported line is a defect ('!!') only when it carries neither a
settled word nor a register id (GI-n, UQ-n, ...); 'rg' marks registered residue and '  ' a settled
mention. Per the status-currency ruling, a 'not read / not resolved' sentence with no register id
keeps its page PARTIAL.

--selftest embeds the 80-97 '## Not read' paragraph exactly as it stood at c97af7156 and asserts
the sweep flags it: the rejecting regression the review asked for."""
import io, re, sys
DB = "C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/"
SEC = re.compile(r"^#{2,3}\s+(?:\d+[.)]?\s*)?(?:not\b|unresolved\b|open\b|still\b|remaining\b|unknown\b|limits?\b)", re.I)
RES = re.compile(r"(?<![-\w])(?:not yet|unknown|unresolved|still open|open question|TODO|not read|unverified|unclear|to be determined|remains open|not established)", re.I)
DONE = re.compile(r"answered|resolved|confirmed|corrected|narrowed|decoded|closed|withdrawn|settled|out of scope|documented|read\b[^.]{0,40}?20\d{2}", re.I)
RID = re.compile(r"\b[A-Z]{1,4}-\d{1,4}[a-z]?\b")


def strip_struck(line, instr):
    """Remove ~~..~~ spans; instr carries strike state across lines. -> (clean, instr)"""
    out, i = [], 0
    while i < len(line):
        if line.startswith("~~", i):
            instr = not instr
            i += 2
        elif not instr:
            out.append(line[i])
            i += 1
        else:
            i += 1
    return "".join(out), instr


def tag(clean):
    """-> '!!' unregistered residue / 'rg' register id present / '  ' settled mention / None no residue."""
    if RID.search(clean):
        return "rg"
    if DONE.search(clean):
        return "  "
    if RES.search(clean):
        return "!!"
    return None


def scan(rel):
    t = io.open(DB + rel, encoding="utf-8", errors="replace").read().split("\n")
    out, head, on, instr, prev = [], "", False, False, None
    for i, line in enumerate(t):
        if line.lower().startswith("status:"):
            continue
        if re.match(r"^#{1,6}\s", line):
            on = bool(SEC.match(line))
            head = line[:70]
            prev = None
            if on:
                out.append("  [%d] %s" % (i + 1, line[:100]))
            continue
        clean, instr = strip_struck(line, instr)
        if not clean.strip() or not re.sub(r"[\s\-*—~|]+", "", clean):
            prev = None
            continue                                   # blank, fully struck, or a struck bullet's ' - —' stub
        t_ = tag(clean)
        if t_ is None:
            if not on:
                prev = None
                continue
            # mechanism B: content under a residue heading; an indented continuation of a
            # bullet the previous line already settled inherits its tag
            if line.startswith((" ", "\t")) and not re.match(r"^\s*[-*] ", line) and prev in ("rg", "  "):
                t_ = prev
            else:
                t_ = "!!"
        out.append("    %s%4d %s" % (t_, i + 1, clean.strip()[:170]))
        prev = t_
    return out


def main():
    if "--selftest" in sys.argv:
        # Regression on the REJECT: the 80-97 '## Not read' paragraph as committed at c97af7156 -
        # paragraph content under a residue heading must be flagged even though the words
        # 'not read' appear only in the heading.
        fixture = [
            "## Not read",
            "~~All step/update tails listed above;~~ *(tails read 2026-09-29)*; emit calls `00394DA0`, `003970A0`,",
            "`00398030`, `00399600`, `0039A9B0`, `0039B550`, `0039B620`, `003A2B20`,",
            "`003A2D80`, `003A3010`, `003A34D0`, `003A35E0`, `0042FDB0`, `004309C0`,",
            "`003A6E60`, `003D8E50`, `0020E610`, `0017FFD0`, `002F1D90`; selector targets",
            "`0045AEF0`, `004559C0`, `00455560`, `0045A6A0`, `0045A220`, `004584E0`,",
            "`00458CA0`, and the `0045B2A0`/`0045BAD0` tails; `00431770`, `003AA280`.",
        ]
        assert SEC.match(fixture[0]), "fixture heading not recognised as residue heading"
        flagged, instr = [], False
        for l in fixture[1:]:
            clean, instr = strip_struck(l, instr)
            if clean.strip() and tag(clean) in (None, "!!"):
                flagged.append(l)
        assert flagged, "regression FAILED: c97af7156 '## Not read' paragraph not flagged"
        # controls
        assert tag("the tail helpers were not instruction-read - registered as GI-14.") == "rg"
        c, _ = strip_struck("~~`00431770` still `not read`~~ *(read 2026-09-19)*", False)
        assert tag(c) == "  "
        assert tag("the emit calls are not read - answered 2026-09-29") == "  "
        assert tag("None is a previously-unknown top-level surface") is None   # hyphenated - not a residue claim
        print("selftest OK - %d fixture lines flagged" % len(flagged))
        return
    fails = 0
    for rel in [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]:
        out = scan(rel)
        fails += sum(1 for l in out if l.startswith("    !!"))
        print("===", rel)
        print("\n".join(out) if out else "  (no residue outside strikes)")
    print("!! residue-without-id lines:", fails)


main()
