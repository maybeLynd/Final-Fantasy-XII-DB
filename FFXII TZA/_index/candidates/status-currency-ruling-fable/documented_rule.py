"""documented_rule.py - FABLE's ruling on OPUS-REQ-FABLE-STATUS-CURRENCY-RULE, as a check a page must pass before its
status line moves PARTIAL -> DOCUMENTED on closed register rows (FABLE, Claude Opus 5.5, 2026-09-29). Reads only.

For every page OPUS's census (../status-currency-census-0929/census.tsv) classes every-named-row-closed, or for the pages
given on the command line:
  K  the KIND of each row the status line names, from the register row's own lead words (check_questions folds these into
     ANSWERED / WITHDRAWN, which hides the difference this ruling turns on):
       answered   ANSWERED / CLOSED words                               -> closes the page residue
       withdrawn  WITHDRAWN / DISSOLVED / NOT A DEFECT / DUPLICATE       -> the question was wrong; closes it
       disposed   SUPERSEDED / NOT A QUESTION / NO ADMISSIBLE SOURCE /
                  OUT OF EVIDENCE BOUNDARY                              -> closes it for the page; residue moved or declared
  B  open boxes ('- [ ]', and the partial marker '- [~]', 2026-09-30) on the page. Any open box is page residue: the page stays PARTIAL
  L  live register ids (OPEN / PARTIAL / BLOCKED / UNKNOWN) named anywhere in the page body. Also page residue
  D  a row closed as a DUPLICATE of another carries its residue there: a live target counts as a live id (L)
  P  POINTER: for each disposed row, the status line carries the disposition word, so a reader of the status line sees
     that the residue was moved or declared, not answered. Missing before a re-status is expected; missing after it fails
  E  a NO ADMISSIBLE SOURCE / OUT OF EVIDENCE BOUNDARY row is closed for the gate but unanswered in fact: the page BODY must
     name it, so the page states its own limit (a status-line pointer alone fails)
  U  UNKNOWN ID (added 2026-09-30 on OPUS-REQ-FABLE-DD-RULE-UNKNOWN-ID-AND-TEMPLATES-0929): an id of a register family
     (its prefix is used by some register row) that is NOT in the register, named anywhere on the page. Before this, L read
     such an id as "not live" and the page passed while citing questions that do not exist (the largest-unclassified page
     named BI-17..BI-19). An unknown id is a citation defect the owner must resolve - register the question, correct the id,
     or reword a non-register token so it is not written as an id - so the page is never READY while one stands. Ids of
     families the register does not use (CON-, EXP-, ...) are not register citations and are not judged here
  N  NOTE template (FABLE ruling 2026-09-30, note-template-ruling.md): a page declaring `note_kind:` must name a known
     kind, a resolvable `parent:`, carry the five sections (Scope, Findings, Evidence, Method, Limits - by keyword) and
     an evidence table with a tier column; otherwise NOTE-INCOMPLETE, never READY. Pages without note_kind are judged
     against their SYSTEM / FORMAT / CONTRACT template by the owner read, as before
  T  TRACKED EVIDENCE (added 2026-09-29 on SWE2-AUDIT-SPEC's AUDITSPEC-REQ-OPUS-ANSWERED-ROW-EVIDENCE-TRACKED-0930): a closed
     row the status line names must not cite an evidence record (`_index/candidates/...`, `candidates/...` or
     `_experiments/evidence/...`) that git does not track. A file path must be tracked; a directory must hold at least one
     tracked file. RC-2 and RC-10 read ANSWERED on records that were never committed, and their pages counted READY.
     A page citing such a row is EVIDENCE-UNTRACKED, never READY
  S  self-test: a clean synthetic page passes; adding an open box, naming a live id, dropping a disposition pointer,
     stating an OEB limit only in the status line, a duplicate whose target is live, or naming an unknown register-family
     id each fails it; naming a non-register-family id (CON-195) does not

Verdicts: READY (B, L, U clean; no disposed rows), READY-WITH-POINTER (B, L, U clean; every disposed row's pointer present,
and E met), NEEDS-POINTER (B, L, U clean; a pointer or an E statement missing), UNKNOWN-ID (B, L clean; an unknown
register-family id named - never READY), EVIDENCE-UNTRACKED (B, L, U clean; a named closed row cites an untracked
evidence record - never READY), PARTIAL (an open box or a live id).
READY is not DOCUMENTED: the owner still confirms the sections are filled and every claim tier-cited.
"""
import csv, io, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_questions as C

DISPOSED = ("SUPERSEDED", "NOT A QUESTION", "NO ADMISSIBLE SOURCE", "OUT OF EVIDENCE BOUNDARY")
WITHDRAWN = ("WITHDRAWN", "DISSOLVED", "NOT A DEFECT", "DUPLICATE")
UNANSWERED_IN_FACT = ("NO ADMISSIBLE SOURCE", "OUT OF EVIDENCE BOUNDARY")
LIVE = ("OPEN", "PARTIAL", "BLOCKED", "UNKNOWN")
ID = r"\b([A-Z]{1,4}-\d{1,4}[a-z]?)\b"


def register():
    """id -> state (as check_questions reads it), kind, disposition word ('' if none), duplicate target (or None)."""
    t = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", errors="replace").read()
    state, kind, word, dup = {}, {}, {}, {}
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % C.QID, t, re.M):
        rid = m.group(1)
        st, cells = C.classify(m.group(2))
        cell = C.live_lead(cells[-1]) if len(cells) >= 2 else ""
        lead = cell.lstrip("*~ \t").upper()[:48]
        w = next((k for k in DISPOSED if lead.startswith(k)), "")
        state[rid], word[rid] = st, w
        kind[rid] = "disposed" if w else "withdrawn" if any(lead.startswith(k) for k in WITHDRAWN) \
            else ("answered" if st == "ANSWERED" else st.lower())
        d = re.search(r"duplicate of `?(%s)`?" % C.QID, cell[:200], re.I)
        dup[rid] = d.group(1) if d and d.group(1) != rid else None
    return state, kind, word, dup


def foreign_ids():
    """U repair (2026-09-30, on SWE2-AUDIT-SEM's REJECT, auditsem-review-dd-rule-0930): id systems other than the question
    register that share its prefixes, read from their own registries - never a hand list:
      S-NN  the L2 subsystem ids (_index/IMPORTANT-SUBSYSTEMS.md, two-digit form)
      AQ-n  the ASTRA-QUEUE items (_index/_inbox/ASTRA-QUEUE.md '###' headings)
      I-n   contract invariant ids, where a CONTRACT page defines them ('| I-n |' row or '**I-n' lead)
      MP-n  the My Progress requirements (Database/Tools/dashboard/requirements.py, _index/workflow/MY-PROGRESS-METRICS.md)
    A token in one of these is not a register citation, so U does not judge it."""
    def rd(*p):
        f = os.path.join(*p)
        return io.open(f, encoding="utf-8", errors="replace").read() if os.path.isfile(f) else ""
    out = set(re.findall(r"\bS-\d{2}\b", rd(DB, "_index", "IMPORTANT-SUBSYSTEMS.md")))
    for line in rd(DB, "_index", "_inbox", "ASTRA-QUEUE.md").splitlines():
        if line.startswith("###"):
            out |= set(re.findall(r"\bAQ-\d+\b", line))
    for root, dirs, files in os.walk(DB):
        dirs[:] = [x for x in dirs if not x.startswith(("_experiments", ".", "_index"))]
        for fn in files:
            if fn.startswith("CONTRACT-") and fn.endswith(".md"):
                t = rd(root, fn)
                out |= set(re.findall(r"^\|\s*(I-\d+)\s*\|", t, re.M)) | set(re.findall(r"\*\*(I-\d+)\b", t))
    out |= set(re.findall(r"\bMP-\d+\b", rd(DB, "..", "Tools", "dashboard", "requirements.py")))
    out |= set(re.findall(r"\bMP-\d+\b", rd(DB, "_index", "workflow", "MY-PROGRESS-METRICS.md")))
    return out


# T also reads (Database/)Tools/work/... paths: that tree is gitignored, so such a record is ALWAYS untracked
# (SWE2-AUDIT-SEM, auditsem-review-ddrule-t-0930 section 4; applied 2026-09-30, FABLE).
EVID = re.compile(r"(?:(?:Database/)?Tools/work|_index/candidates|candidates|_experiments/evidence)/[A-Za-z0-9._\-]+(?:/[A-Za-z0-9._\-]+)*/?")


def tracked_paths():
    """Paths git tracks under the database, relative to it (forward slashes)."""
    import subprocess
    out = subprocess.run(["git", "-C", DB, "ls-files", "-z", "--", "_index/candidates", "_experiments"],
                         capture_output=True).stdout.decode("utf-8", "replace")
    return set(x for x in out.split("\0") if x)


def cited_untracked(cell, tracked):
    """The evidence paths a register cell cites that git does not track (T)."""
    bad = []
    for m in EVID.finditer(cell):
        p = m.group(0).rstrip(".,)")
        if p.startswith("Tools/work/") or p.startswith("Database/Tools/work/"):
            if p not in bad:
                bad.append(p)                         # gitignored: never tracked
            continue
        if p.startswith("candidates/"):
            p = "_index/" + p
        is_file = "." in os.path.basename(p.rstrip("/")) and not p.endswith("/")
        ok = p in tracked if is_file else any(t.startswith(p.rstrip("/") + "/") for t in tracked)
        if not ok and p not in bad:
            bad.append(p)
    return bad


def evidence_status():
    """id -> the untracked evidence paths its register cell cites (only ids with at least one)."""
    t = io.open(os.path.join(DB, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", errors="replace").read()
    tracked, out = tracked_paths(), {}
    for m in re.finditer(r"^\|\s*(%s)\s*\|(.*)$" % C.QID, t, re.M):
        bad = cited_untracked(m.group(2), tracked)
        if bad:
            out[m.group(1)] = bad
    return out


def judge(text, state, kind, word, dup, prefixes=None, page_dir=None, foreign=frozenset(), page_path=None,
          untracked=None):
    head = text[:text.find("\n---", 3)] if text.startswith("---") else text[:4000]
    m = re.search(r"^status:\s*(.*)$", head, re.M)
    st = m.group(1) if m else ""
    named = sorted(set(i for i in re.findall(ID, st) if i in state))
    body = text.replace(st, "") if st else text
    boxes = len(re.findall(r"^\s*[-*]\s*\[[ ~]\]", text, re.M))  # '[~]' (partial) is residue too (FABLE 2026-09-30)
    live = set(i for i in re.findall(ID, body) if state.get(i) in LIVE)
    live |= set(dup[i] for i in named if dup.get(i) and state.get(dup[i]) in LIVE)          # D
    prefixes = prefixes if prefixes is not None else {i.split("-")[0] for i in state}
    # U reads the page without its front matter (as L reads the body), and skips ids of the foreign id systems
    after_fm = text[text.find("\n---", 3) + 4:] if text.startswith("---") and text.find("\n---", 3) > 0 else text
    unknown = sorted(set(i for i in re.findall(ID, after_fm)
                         if i not in state and i not in foreign and i.split("-")[0] in prefixes))  # U
    disposed = [i for i in named if kind[i] == "disposed"]
    missing = [i for i in disposed if word[i] not in st.upper()]                            # P
    unstated = [i for i in disposed if word[i] in UNANSWERED_IN_FACT
                and not re.search(r"\b%s\b" % re.escape(i), body)]                          # E
    note = note_gaps(text, head, page_dir, page_path)                                          # N
    untr = [i for i in named if kind.get(i) != "open" and (untracked or {}).get(i)]              # T
    if boxes or live:
        v = "PARTIAL"
    elif unknown:
        v = "UNKNOWN-ID"
    elif untr:
        v = "EVIDENCE-UNTRACKED"
    elif note:
        v = "NOTE-INCOMPLETE"
    elif missing or unstated:
        v = "NEEDS-POINTER"
    else:
        v = "READY-WITH-POINTER" if disposed else "READY"
    return v, named, boxes, sorted(live), disposed, (missing + ["%s(body)" % i for i in unstated]
                                                     + ["%s(unknown)" % i for i in unknown]
                                                     + ["%s(untracked:%s)" % (i, ",".join(untracked[i])) for i in untr] + note)


NOTE_KINDS = ("census", "evidence", "function", "residual")
# N repair (2026-09-30, on SWE2-AUDIT-SEM's REJECT): a heading counts only if it STARTS with its keyword (after optional
# numbering), so "Out of scope" or "No limits" do not satisfy Scope / Limits.
NUM = r"^(?:[0-9]+[.)]?\s+|[0-9]+\.[0-9]+\s+)?"
NOTE_SECTIONS = (("scope", NUM + r"scope\b"), ("findings", NUM + r"(findings?|what is established|results?)\b"),
                 ("evidence", NUM + r"evidence\b"), ("method", NUM + r"(method|reproduc)"),
                 ("limits", NUM + r"(limits?\b|what is not (known|established)|not established)"))


def sections(text):
    """[(heading lower, level, body lines)] for every level-2/3 heading, body up to the next heading of level <= 3."""
    out, cur = [], None
    for line in text.splitlines():
        m = re.match(r"^(#{1,3})\s+(.+?)\s*$", line)
        if m:
            cur = [m.group(2).lower(), len(m.group(1)), []]
            if len(m.group(1)) >= 2:
                out.append(cur)
            else:
                cur = None
        elif cur is not None:
            cur[2].append(line)
    return out


def tier_table_with_row(lines):
    """True if the lines hold a table whose header row has a tier column, a separator, and at least one data row."""
    for k, line in enumerate(lines):
        if re.match(r"^\|.*\btier\b.*\|\s*$", line, re.I) and k + 1 < len(lines) and re.match(r"^\|[\s:|-]+\|\s*$", lines[k + 1]):
            return any(l.strip().startswith("|") and not re.match(r"^\|[\s:|-]+\|\s*$", l)
                       for l in lines[k + 2:k + 3])
    return False


def note_gaps(text, head, page_dir=None, page_path=None):
    """N: a page declaring `note_kind:` meets the NOTE template (FABLE ruling 2026-09-30, note-template-ruling.md,
    repaired the same day on SWE2-AUDIT-SEM's review):
      - a known kind;
      - `parent:` present; when the page's location is known, it resolves to an existing .md FILE other than the note
        itself, and that parent links back to the note (R2);
      - the five sections, each heading starting with its keyword, each with a non-empty body;
      - under the Evidence heading, a table with a tier column and at least one data row.
    [] when the page declares no note_kind or meets all."""
    m = re.search(r"^note_kind:\s*(\S+)", head, re.M)
    if not m:
        return []
    gaps = [] if m.group(1).lower() in NOTE_KINDS else ["note_kind:%s" % m.group(1)]
    par = re.search(r"^parent:\s*(\S+)", head, re.M)
    if not par:
        gaps.append("parent(missing)")
    elif page_dir is not None:
        pp = os.path.normpath(os.path.join(page_dir, par.group(1)))
        if not (os.path.isfile(pp) and pp.lower().endswith(".md")):
            gaps.append("parent(unresolved or not a .md file)")
        elif page_path is not None and os.path.normcase(os.path.abspath(pp)) == os.path.normcase(os.path.abspath(page_path)):
            gaps.append("parent(is the note itself)")
        elif page_path is not None:
            ptxt = io.open(pp, encoding="utf-8", errors="replace").read()
            if os.path.basename(page_path) not in ptxt:
                gaps.append("parent(no back-link to the note)")
    secs = sections(text)
    for n, rx in NOTE_SECTIONS:
        hits = [s for s in secs if re.search(rx, s[0])]
        if not hits:
            gaps.append("section:%s" % n)
        elif not any(any(l.strip() for l in s[2]) for s in hits):
            gaps.append("section:%s(empty)" % n)
        elif n == "evidence" and not any(tier_table_with_row(s[2]) for s in hits):
            gaps.append("evidence-table(no tier column with a data row under Evidence)")
    return gaps


def main():
    state, kind, word, dup = register()
    fails = 0
    # S: synthetic pages against the real register (plus one synthetic live id: the register has no OPEN row today)
    plain = [i for i in sorted(state) if re.fullmatch(ID[2:-2], i)]   # ids the page scanner can see as whole words
    ans = next(i for i in plain if kind[i] == "answered")
    sup = next(i for i in plain if word[i] == "SUPERSEDED" and not dup[i])
    oeb = next(i for i in plain if word[i] == "OUT OF EVIDENCE BOUNDARY")
    dpl = next(i for i in plain if dup[i] and state.get(dup[i]) == "ANSWERED")
    liv = "ZZ-999"
    st2, kd2 = dict(state, **{liv: "OPEN"}), dict(kind, **{liv: "open"})
    page = lambda rid, extra="body": "---\nstatus: DOCUMENTED (%s answered; %s %s)\n---\n# x\n%s\n" % (ans, rid, word[rid], extra)
    cases = [("clean", page(sup), dup, "READY-WITH-POINTER"),
             ("open box", page(sup) + "- [ ] still to read\n", dup, "PARTIAL"),
             ("partial box", page(sup) + "- [~] half read\n", dup, "PARTIAL"),
             ("live id", page(sup) + "see %s\n" % liv, dup, "PARTIAL"),
             ("no pointer", page(sup).replace(word[sup], "closed"), dup, "NEEDS-POINTER"),
             ("oeb stated", page(oeb, "the limit %s is stated here" % oeb), dup, "READY-WITH-POINTER"),
             ("oeb status only", page(oeb), dup, "NEEDS-POINTER"),
             ("dup to closed", page(dpl), dup, "READY-WITH-POINTER"),
             ("dup to live", page(dpl), dict(dup, **{dpl: liv}), "PARTIAL")]
    pre = ans.split("-")[0]
    unk = next("%s-%d" % (pre, n) for n in range(9999, 0, -1) if "%s-%d" % (pre, n) not in state)
    assert "CON" not in {i.split("-")[0] for i in state}, "control needs a non-register family"
    cases += [("unknown id", page(sup) + "see %s\n" % unk, dup, "UNKNOWN-ID"),
              ("non-register family id", page(sup) + "see CON-195\n", dup, "READY-WITH-POINTER")]
    foreign = foreign_ids()
    # U controls, one per foreign family (SWE2-AUDIT-SEM asked for them): a real id of each family that shares a register
    # prefix and is not a register id must NOT fire; an unknown id in front matter only must not fire either.
    fam = {}
    for pfx, rx in (("S", r"S-\d{2}"), ("AQ", r"AQ-\d+"), ("I", r"I-\d+"), ("MP", r"MP-\d+")):
        c = sorted(i for i in foreign if re.fullmatch(rx, i) and i not in state and pfx in {x.split("-")[0] for x in state})
        if c:
            fam[pfx] = c[-1]
    assert {"S", "AQ"} <= set(fam), "foreign-family controls missing: %s" % fam
    cases += [("foreign %s id %s" % (k, v), page(sup) + "see %s\n" % v, dup, "READY-WITH-POINTER") for k, v in sorted(fam.items())]
    cases += [("unknown id in front matter only", page(sup).replace("status:", "note: %s\nstatus:" % unk, 1), dup,
               "READY-WITH-POINTER")]
    tier_row = "| claim | evidence | tier |"
    NL = chr(10)
    good_note = page(sup, NL.join(["## Scope", "x", "## Findings", "x", "## Evidence", tier_row, "|---|---|---|",
                                   "| c | e | 1 |", "## Method", "x", "## Limits", "x"]))
    good_note = good_note.replace("status:", "note_kind: census" + NL + "parent: x.md" + NL + "status:", 1)
    empty_note = good_note
    for s in ("## Scope", "## Findings", "## Method", "## Limits"):
        empty_note = empty_note.replace(s + NL + "x", s)
    cases += [("note complete", good_note, dup, "READY-WITH-POINTER"),
              ("note no method", good_note.replace("## Method", "## Other"), dup, "NOTE-INCOMPLETE"),
              ("note no tier column", good_note.replace(tier_row, "| claim | evidence |"), dup, "NOTE-INCOMPLETE"),
              ("note no parent", good_note.replace("parent: x.md" + NL, ""), dup, "NOTE-INCOMPLETE"),
              ("note bad kind", good_note.replace("note_kind: census", "note_kind: essay"), dup, "NOTE-INCOMPLETE"),
              ("note empty sections", empty_note, dup, "NOTE-INCOMPLETE"),
              ("note header-only tier table", good_note.replace("| c | e | 1 |" + NL, ""), dup, "NOTE-INCOMPLETE"),
              ("note keyword not leading", good_note.replace("## Scope", "## Out of scope").replace("## Limits", "## No limits"),
               dup, "NOTE-INCOMPLETE"),
              ("note tier table outside Evidence", good_note.replace("## Evidence" + NL + tier_row + NL + "|---|---|---|" + NL
                                                                     + "| c | e | 1 |", "## Evidence" + NL + "prose")
               + NL.join([tier_row, "|---|---|---|", "| c | e | 1 |"]), dup, "NOTE-INCOMPLETE")]
    prefixes2 = {i.split("-")[0] for i in state}
    got = [(n, judge(p, st2, kd2, word, dp, prefixes2, foreign=foreign)[0], want) for n, p, dp, want in cases]
    # T: a named answered row citing an untracked record is never READY; the same row with its record tracked is
    tracked = tracked_paths()
    real = next(p for p in sorted(tracked) if p.startswith("_index/candidates/") and p.count("/") >= 3)
    real_dir = real.rsplit("/", 1)[0] + "/"
    ghost = "_index/candidates/zz-never-committed-record-0000/"
    got += [("T untracked evidence", judge(page(sup), st2, kd2, word, dup, prefixes2, foreign=foreign,
                                           untracked={ans: cited_untracked("see `%s`" % ghost, tracked)})[0], "EVIDENCE-UNTRACKED"),
            ("T tracked evidence", judge(page(sup), st2, kd2, word, dup, prefixes2, foreign=foreign,
                                         untracked={ans: cited_untracked("see `%s` and `%s`" % (real_dir, real), tracked)})[0],
             "READY-WITH-POINTER"),
            ("T short form candidates/", judge(page(sup), st2, kd2, word, dup, prefixes2, foreign=foreign,
                                               untracked={ans: cited_untracked("(candidates/zz-never-committed-record-0000/x.py)",
                                                                               tracked)})[0], "EVIDENCE-UNTRACKED"),
            ("T Tools/work evidence", judge(page(sup), st2, kd2, word, dup, prefixes2, foreign=foreign,
                                            untracked={ans: cited_untracked("(`Database/Tools/work/SWE2-X/REVIEW.md`)",
                                                                            tracked)})[0], "EVIDENCE-UNTRACKED")]
    # parent resolution, with real files (SWE2-AUDIT-SEM: the branch was never run by S before)
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        note_path = os.path.join(td, "note.md")
        # the note exists on disk and names itself, so only the self-parent check can refuse "parent: note.md"
        io.open(note_path, "w", encoding="utf-8").write(good_note + "(this is note.md)\n")
        io.open(os.path.join(td, "x.md"), "w", encoding="utf-8").write("parent page; see [the note](note.md)\n")
        io.open(os.path.join(td, "y.md"), "w", encoding="utf-8").write("parent page with no link to it\n")
        os.mkdir(os.path.join(td, "sub"))
        pcases = [("parent resolves with back-link", good_note, "READY-WITH-POINTER"),
                  ("parent unresolvable", good_note.replace("parent: x.md", "parent: nothere.md"), "NOTE-INCOMPLETE"),
                  ("parent is a directory", good_note.replace("parent: x.md", "parent: sub"), "NOTE-INCOMPLETE"),
                  ("parent is the note itself", good_note.replace("parent: x.md", "parent: note.md"), "NOTE-INCOMPLETE"),
                  ("parent without back-link", good_note.replace("parent: x.md", "parent: y.md"), "NOTE-INCOMPLETE")]
        got += [(n, judge(p, st2, kd2, word, dup, prefixes2, page_dir=td, foreign=foreign, page_path=note_path)[0], w)
                for n, p, w in pcases]
    s_ok = all(g == w for _, g, w in got)
    fails += not s_ok
    print("%s  S self-test (%d cases) %s" % ("PASS" if s_ok else "FAIL", len(got), ["%s->%s" % (n, g) for n, g, _ in got]))
    print("   foreign id systems loaded: %d ids; controls %s" % (len(foreign), fam))
    pages = sys.argv[1:] or [r["page"] for r in csv.DictReader(
        io.open(os.path.join(HERE, "..", "status-currency-census-0929", "census.tsv"), encoding="utf-8"), delimiter="\t")
        if r["class"] == "every-named-row-closed"]
    tally = {}
    untracked = evidence_status()
    print("   T: register rows citing untracked evidence: %d %s" % (len(untracked), sorted(untracked)[:12]))
    for p in pages:
        text = io.open(os.path.join(DB, p), encoding="utf-8", errors="replace").read()
        v, named, boxes, live, disposed, missing = judge(text, state, kind, word, dup,
                                                         page_dir=os.path.dirname(os.path.join(DB, p)), foreign=foreign,
                                                         page_path=os.path.join(DB, p), untracked=untracked)
        tally[v] = tally.get(v, 0) + 1
        print("%-19s %s  kinds=%s boxes=%d live=%s disposed=%s missing=%s" % (
            v, p, ",".join("%s:%s%s" % (i, kind[i], "->" + dup[i] if dup[i] else "") for i in named), boxes,
            ",".join(live) or "-", ",".join("%s:%s" % (i, word[i]) for i in disposed) or "-", ",".join(missing) or "-"))
    print("TALLY", " ".join("%s=%d" % kv for kv in sorted(tally.items())), "of", len(pages))
    print("FAILS %d" % fails)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
