"""requirements.py - the requirement catalog behind the "My Progress" tab (OPUS, 2026-09-29; metric version MP-2).

MP-2 applies FABLE's meaning review (_index/candidates/mp1-meanings-review/, ACCEPT with C1-C4): a bucketed extension is
not one requirement - its member formats are, and until they are declared (BUCKET_MEMBERS, owned by DATA) the bucket is a
named GAP that keeps the overall figure UNMEASURED (C4); register rows split into answered and dispositioned (C2); folder
99 is "not yet tied to a system" (C3); the tab shows the per-family table first and a functions-excluded line (C1).

Definitions: Database/FFXII TZA/_index/workflow/MY-PROGRESS-METRICS.md. Category map: _index/workflow/my-progress/category-map.tsv.

THE UNIT. One requirement = one governing criterion applied to one canonical object that the governing records already
name (a register id, a page box, a function entry, a document path, a registry slot, a format, an EBP unit, a
contradiction id, an S-id x L2 dimension, a terminal pass number). It measures requirements, not effort or time.

TWO LAYERS, so the numbers are bound to one generation:
  collect(db)   runs BEFORE a generation begins (it walks the corpus with the existing readers: check_questions,
                check_dispositions, check_provenance, check_formats, check_assets, check_ebp, transfer_audit, progress)
                and writes one facts file, which the generation then snapshots like any other input.
  measure(...)  pure: reads only the facts, the map, the board, DATA's reporter snapshot, the goal gate output and the
                subsystem registry, and returns the aggregates. The tests drive it with fixture facts.

A family whose reader raises is recorded in facts["failed"]; measure() then reports the overall figure UNMEASURED and
shows the rest as "known requirements only". Missing data is never zero remaining.
"""
import collections, hashlib, io, json, os, re, sys

VERSION = "MP-2"
HERE = os.path.dirname(os.path.abspath(__file__))
GS = os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts")
# DATA's declared members of each bucketed extension: ext, family, signatures (comma-separated), entries. Absent -> a GAP.
# It lives in the tracked database (MP-3, OPUS 2026-09-29): the first request named Tools/work/formats/, which is gitignored,
# so a file there could never be published, exported or reproduced. That untracked path is deliberately NOT read.
DBROOT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "FFXII TZA")
BUCKET_MEMBERS = os.path.join(DBROOT, "_index", "bucket-members.tsv")
BUCKET_MEMBERS_UNTRACKED = os.path.join(os.path.dirname(HERE), "work", "formats", "bucket-members.tsv")
# the full-archive leading-signature census the member rows must cover exactly (every entry, not the 12-file sample)
MAGIC_CENSUS = os.path.join(DBROOT, "_index", "candidates", "bucket-members-input-0929", "format-magic-census-full.tsv")
BUCKET_REPAIR = "OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS (SWE2-DATA)"


_PART = re.compile(r"^(.*?)\s*=\s*(\d+)\s*$")   # a SIG=N take (DATA's shared-signature split)


def _sig(s):
    """One comparable form for a census signature: 'text' magics keep their case, hex dwords ignore spacing and case."""
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] == "'":
        return "t:" + s[1:-1]
    return "h:" + s.replace(" ", "").lower()


def bucket_members_check(bucketed, members_path=None, census_path=None):
    """-> (members {ext: [(family, [sig...])]}, problems [str]).

    A bucket's gap closes only when its member rows cover the full census EXACTLY (MP-3): every census signature of the
    extension is held in full - by one bare holder, or split `SIG=N` among holders whose takes sum to its census count -
    no member names a signature the census lacks, and each member's `entries` equals the sum of its takes. A declaration with one row per extension used to clear the gap on its
    own (the first MP-2 reader checked only that some row existed) - a partial file must leave the figure UNMEASURED, not complete."""
    members_path = members_path or BUCKET_MEMBERS
    census_path = census_path or MAGIC_CENSUS
    members, problems, rows = collections.defaultdict(list), [], collections.defaultdict(list)
    if not os.path.isfile(members_path):
        extra = (" (a copy at the gitignored Tools/work/formats path is not read)"
                 if members_path == BUCKET_MEMBERS and os.path.isfile(BUCKET_MEMBERS_UNTRACKED) else "")
        problems.append("member formats of the bucketed extension(s) %s are not declared (Database/FFXII TZA/_index/"
                        "bucket-members.tsv)%s" % (", ".join("." + e for e in bucketed), extra))
        return members, problems
    for i, l in enumerate(io.open(members_path, encoding="utf-8-sig").read().splitlines(), 1):
        if not l.strip() or l.startswith(("#", "ext\t")):
            continue
        c = l.split("\t")
        if len(c) < 4:
            problems.append("bucket-members.tsv line %d has %d columns, 4 required (ext, family, signatures, entries)" % (i, len(c)))
            continue
        sigs = [x.strip() for x in c[2].split(",") if x.strip()]
        try:
            n = int(c[3])
        except ValueError:
            n = None
        rows[c[0].strip()].append((c[1].strip(), sigs, n, i))
    census = collections.defaultdict(dict)
    try:
        for l in io.open(census_path, encoding="utf-8-sig").read().splitlines():
            c = l.split("\t")
            if l.startswith("#") or len(c) < 4 or c[0] == "ext":
                continue
            census[c[0]][_sig(c[2])] = (c[2].strip(), int(c[3]))
    except (OSError, ValueError) as e:
        problems.append("the full signature census is unreadable (%s); member coverage cannot be checked" % e)
        return members, problems
    for ext in bucketed:
        declared = rows.get(ext, [])
        if not declared:
            problems.append("member formats of .%s are not declared" % ext)
            continue
        if not census.get(ext):
            problems.append(".%s has no rows in the full signature census; coverage cannot be checked" % ext)
            continue
        # SIG=N (adopted 2026-09-29 from SWE2-DATA's DATA-REQ-OPUS-BUCKET-MEMBERS-SHARED-SIGNATURES proposal, reviewed by
        # OPUS): the census key is the leading dword, not a format identity, and four .bin dwords are shared by distinct
        # consumer-bound formats. A member may take N entries of a signature; the takes of every holder must sum to the
        # census count, and a bare signature takes all of it and must be its only holder. Coverage stays exact.
        holders = collections.defaultdict(list)          # sig key -> [(family, take or None for bare)]
        for fam_, sigs, n, i in declared:
            bare, got = [], 0
            for sg in sigs:
                m = _PART.match(sg)
                part = int(m.group(2)) if m else None
                s = m.group(1) if m else sg
                bare.append(s)
                k = _sig(s)
                if k not in census[ext]:
                    problems.append(".%s member %s names signature %s, which the census does not have" % (ext, fam_, s))
                    continue
                holders[k].append((fam_, part))
                got += census[ext][k][1] if part is None else part
            members[ext].append((fam_, bare))
            if n is None or n != got:
                problems.append(".%s member %s declares %s entries; its signatures cover %d in the census" % (ext, fam_, n, got))
        for k, hs in holders.items():
            printed, cnt = census[ext][k]
            if len(hs) > 1 and any(p is None for _f, p in hs):
                problems.append(".%s signature %s is in two members (%s) and not split by entry count"
                                % (ext, printed, ", ".join(f for f, _p in hs)))
            elif len(hs) > 1 or hs[0][1] is not None:
                took = sum(p for _f, p in hs)
                if took != cnt:
                    problems.append(".%s signature %s is split %s = %d, the census has %d"
                                    % (ext, printed, "+".join("%s:%d" % (f, p) for f, p in hs), took, cnt))
        missing = [v[0] for k, v in sorted(census[ext].items(), key=lambda kv: -kv[1][1]) if k not in holders]
        if missing:
            problems.append(".%s: %d census signature(s) in no member (%s%s)" % (
                ext, len(missing), ", ".join(missing[:6]), ", ..." if len(missing) > 6 else ""))
    return members, problems
GROUPS = collections.OrderedDict([
    ("W", "World & maps"), ("C", "Combat & damage"), ("E", "Enemies & AI"), ("S", "Spawning, death & respawn"),
    ("P", "Player & party"), ("I", "Items, equipment & progression"), ("T", "Story, quests & events"),
    ("M", "Menus & controls"), ("G", "Animation, graphics & audio"), ("V", "Save/load & persistence"),
    ("D", "Scripts & game data/VBF"), ("N", "Engine & supporting systems")])
TERMINAL_PASSES = 30       # FINAL-AUDIT-PROTOCOL: thirty consecutive passes; never read from a producer
WHOLE = "whole"          # a requirement about the whole database (terminal passes, cross-cutting integrity)
UNTIED = "untied"        # a function whose system is not yet known (no page, no owner, only a generic shape class)
FAMILIES = collections.OrderedDict([
    ("Q", "register questions (OPEN-QUESTIONS.md rows)"),
    ("P", "page obligations (unticked page boxes with no live register row)"),
    ("F", "function dispositions (every function explained A, class-explained B or dispositioned C)"),
    ("DD", "documents documented (status DOCUMENTED/AUDITED, or readiness when no status)"),
    ("DA", "documents with a named falsification pass"),
    ("DV", "documents verified against the certified parent (provenance)"),
    ("R", "authored-data registry slots explained"),
    ("X", "shipped file formats explained"),
    ("E", "EBP container units explained"),
    ("K", "contradictions carrying a resolved disposition"),
    ("L2", "L2 cells: registered system x required dimension"),
    ("T", "terminal final-audit passes (30 consecutive)")])
LEVELS = {"Q": "L1", "P": "L1", "F": "L1", "DD": "L1", "DA": "L1", "DV": "L1", "R": "L1", "X": "L1", "E": "L1",
          "K": "L1L2", "L2": "L2", "T": "L1L2"}
FAMILY_GROUP = {"R": ["D"], "X": ["D"], "E": ["D"], "T": [WHOLE]}


def _rel_top(rel):
    top = rel.replace("\\", "/").split("/")[0]
    m = re.match(r"^(\d\d)-", top)
    return m.group(1) if m else top


# ------------------------------------------------------------------------------------------------ collect (heavy)
def collect(db, residual_path=None, functions_path=None, board_path=None):
    """Facts for every family except L2 and T (those are measured from their own inputs). Each fact:
    {"k": key, "f": family, "ok": bool, "st": state word, "doc": owning page (DB-relative) or None,
     "h": [[kind, key], ...] placement hints, "o": owner, "e": evidence locator, "n": next action}."""
    sys.path.insert(0, GS)
    facts, failed, excluded, counts, gaps = [], {}, [], {}, {}
    fam = lambda name: (lambda fn: _run(name, fn, failed))
    board_path = board_path or os.path.join(db, "_index", "_inbox", "TEAM.json")

    @fam("Q")
    def _q():
        import check_questions as C, transfer_audit as TA
        text = io.open(os.path.join(db, "_index", "OPEN-QUESTIONS.md"), encoding="utf-8", errors="replace").read()
        batch = io.open(os.path.join(db, TA.BATCH), encoding="utf-8", errors="replace").read()
        class1 = {r for r, _ in TA._table_rows(batch, "class 1")}
        class2 = {r: TA.TASK_TOK.findall(" ".join(c)) for r, c in TA._table_rows(batch, "class 2")}
        problems, _ = TA.audit(db, board_path)
        broken = {p.split(":", 1)[0] for p in problems}
        tasks = {t["id"]: t for t in json.load(io.open(board_path, encoding="utf-8"))["tasks"]}
        leads = [(g, k) for g in ("NO_ADMISSIBLE", "WITHDRAWN", "CLOSED", "PARTIAL", "BLOCKED") for k in getattr(C, g)]
        sec, seen = None, set()
        for line in text.split("\n"):
            if line.startswith("## "):
                m = re.match(r"^##\s+([A-Z]+)\b", line); sec = m.group(1) if m else None
                continue
            s = re.match(r"^\|\s*~~(%s)~~\s*\|" % C.QID, line)
            if s:
                excluded.append(["Q:" + s.group(1), "struck row id (removed from the register; not read by the gate)"])
                continue
            m = re.match(r"^\|\s*(%s)\s*\|(.*)$" % C.QID, line)
            if not m:
                continue
            rid = m.group(1)
            if rid in seen:
                excluded.append(["Q:" + rid, "duplicate id - counted once, at its first row"]); continue
            seen.add(rid)
            verdict, cells = C.classify(m.group(2))
            lead = C.live_lead(cells[-1]).lstrip("*~ \t").upper() if len(cells) >= 2 else ""
            word = next((k for _g, k in leads if lead.startswith(k)), verdict)
            link = re.search(r"\]\((?:\.\./)*((?:\d\d-|_experiments/|_types/)[^)#\s]*\.md)", line)
            doc = link.group(1) if link else None
            hints = [["folder", _rel_top(doc)]] if doc else ([["section", sec]] if sec else [])
            ev = "_index/OPEN-QUESTIONS.md row %s" % rid + ("; page %s" % doc if doc else "")
            if verdict == "WITHDRAWN":
                if word == "SUPERSEDED":
                    ok = rid not in broken
                    st = "SUPERSEDED (accepted disposition%s)" % ("; class-1 residue carried by its instrument" if rid in class1 else
                                                                  "; runtime remainder not queued" if "under the runtime rule" in line else "")
                    if not ok:
                        st = "SUPERSEDED but its transfer destination is missing (transfer_audit)"
                elif word == "NOT A QUESTION" and class2.get(rid):
                    carriers = class2[rid]
                    open_c = [c for c in carriers if (tasks.get(c) or {}).get("status") != "DONE"]
                    ok = not open_c and rid not in broken
                    st = ("transferred to %s (carrier DONE)" % ", ".join(carriers) if ok else
                          "transferred to %s - carrier open, obligation not closed" % ", ".join(open_c or carriers))
                else:
                    excluded.append(["Q:" + rid, "%s - not a requirement (%s)" % (word or "WITHDRAWN", "withdrawn")]); continue
            elif verdict == "ANSWERED":
                ok, st = True, ("disposition: " + word if word in C.NO_ADMISSIBLE else "ANSWERED")
            else:
                ok, st = False, verdict
            facts.append({"k": "Q:" + rid, "f": "Q", "ok": ok, "st": st, "doc": doc, "h": hints, "o": "", "e": ev,
                          "n": "" if ok else "answer the row, or record an accepted disposition under the register rules"})
        counts["Q_rows"] = len(seen)

    @fam("P")
    def _p():
        import check_questions as C
        boxes = C.read_boxes(db)
        reg, _d = C.read_table(db)
        n = collections.Counter()
        for rel, line, ticked, ids, txt in boxes:
            if ticked:
                continue
            live = [i for i in ids if reg.get(i, "OPEN") not in ("ANSWERED", "WITHDRAWN")]
            if ids and live:
                continue                 # the same obligation as its live register row: counted once, there
            base = "P:%s#%s" % (rel, hashlib.sha1(txt.encode("utf-8")).hexdigest()[:8])
            n[base] += 1
            key = base if n[base] == 1 else "%s.%d" % (base, n[base])
            st = "unticked box with no register id" if not ids else "unticked box naming closed row(s) %s" % ",".join(sorted(ids))
            facts.append({"k": key, "f": "P", "ok": False, "st": st, "doc": rel, "h": [["folder", _rel_top(rel)]], "o": "",
                          "e": "%s line %d: %s" % (rel, line, txt),
                          "n": "give the box a register id and row, or close it with evidence (register header rule; audit pass 29)"
                               if not ids else "tick the box to match the closed row, or reopen the row"})

    @fam("F")
    def _f():
        import check_dispositions as CD, uc1_band
        sizes = CD.load_functions(functions_path)
        r = CD.evaluate(db, sizes)
        explained = r["explained_set"]
        # which page explains each function: A = evidence-bearing pages citing it interior; B/C/D = the declaring page
        entries = sorted(sizes); import bisect
        pages = collections.defaultdict(set)
        uc1f = uc1_band.frontier_starts() & set(sizes)
        for p in CD.docs(db):
            t = io.open(p, encoding="utf-8", errors="replace").read()
            if not CD._bearing(t):
                continue
            rel = os.path.relpath(p, db).replace("\\", "/")
            for h in CD.CITE.findall(t):
                v = int(h, 16); i = bisect.bisect_right(entries, v) - 1
                if i >= 0 and entries[i] < v < entries[i] + sizes[entries[i]] and entries[i] not in uc1f:
                    pages[entries[i]].add(rel)
        accepted = {w for w, _l, _n in r["accepted"]}
        letter = {}
        for doc, parts in CD.parse_families(db):
            who = "%s :: %s" % (os.path.basename(doc), parts[0] if parts else "(unnamed)")
            if who not in accepted or len(parts) < 5:
                continue
            for m in CD.read_members(doc, parts[2]):
                letter[m] = parts[1]; pages.setdefault(m, set()).add(os.path.relpath(doc, db).replace("\\", "/"))
        resid = set()
        rp = residual_path
        if rp and os.path.isfile(rp):
            for l in io.open(rp, encoding="utf-8", errors="replace"):
                l = l.strip()
                if re.fullmatch(r"(0x)?[0-9A-Fa-f]{6,8}", l):
                    resid.add(int(l, 16))
        tags = {}
        fp = functions_path or CD.DEFAULT_FN
        with io.open(fp, encoding="utf-8", errors="replace") as fh:
            head = fh.readline().rstrip("\n").split("\t")
            ia, io_, it = head.index("entry"), head.index("owner"), head.index("tags")
            for line in fh:
                c = line.rstrip("\n").split("\t")
                if len(c) > it:
                    try: tags[int(c[ia], 16)] = (c[io_], c[it])
                    except ValueError: pass
        for a in sorted(sizes):
            own, tg = tags.get(a, ("", ""))
            dm = re.search(r"CodeDomain\.([A-Za-z]+)\.([A-Za-z]+)", tg)
            hints = [["folder", _rel_top(p)] for p in sorted(pages.get(a, ()))]
            if own: hints.append(["owner", own])
            if dm:
                hints.append(["boundary", dm.group(2)] if dm.group(1) == "Boundary" else ["domain", dm.group(1)])
            ok = a in explained and a not in resid
            if a in resid:
                st = "unresolved residual"
            elif a in explained:
                st = letter.get(a, "A")          # families overlapping A are refused, so a lettered member is not A
            elif letter.get(a) == "D":
                st = "D (explicit unresolved exception)"
            else:
                st = "UC-1 frontier body (unexplained by ruling)" if a in uc1f else "frontier (no disposition)"
            facts.append({"k": "F:%08X" % a, "f": "F", "ok": ok, "st": st, "doc": None, "h": hints, "o": own,
                          "e": "functions.tsv %08X%s" % (a, (" " + dm.group(0)) if dm else ""),
                          "n": "" if ok else "explain it on a page, or declare it in a B/C family (check_dispositions.py)"})
        counts["F_population"] = len(sizes); counts["F_refused_families"] = r["families_refused"]

    @fam("D")
    def _d():
        import progress as PR, check_provenance as CP
        prov = {d["rel"].replace("\\", "/"): d for d in CP.scan(db)}
        for p in PR.docs(db):
            rel = os.path.relpath(p, db).replace("\\", "/")
            t = io.open(p, encoding="utf-8", errors="replace").read()
            h = [["folder", _rel_top(rel)]]
            documented = PR.coverage_documented(t)
            head = t[:t.find("\n---", 3)] if t.startswith("---") else t[:4000]
            sl = re.search(r"^status:\s*(.*)$", head, re.M)
            # FABLE's status-currency ruling (b27e23f80): a documented page whose status line carries a disposition word has a
            # dispositioned residue, not an answered one - shown apart (same acceptance, different meaning)
            disp = bool(sl and re.search(r"SUPERSEDED|NOT A QUESTION|NO ADMISSIBLE SOURCE|OUT OF EVIDENCE BOUNDARY", sl.group(1)))
            facts.append({"k": "DD:" + rel, "f": "DD", "ok": bool(documented),
                          "st": ("documented with a dispositioned residue" if disp else "documented, all answered") if documented else "not documented",
                          "doc": rel, "h": h, "o": "", "e": rel + " front matter status/readiness",
                          "n": "" if documented else "bring the page to DOCUMENTED (or readiness at BEHAVIORALLY UNDERSTOOD)"})
            aud = audited(t)
            facts.append({"k": "DA:" + rel, "f": "DA", "ok": aud, "st": "falsification pass recorded" if aud else "no named falsification pass",
                          "doc": rel, "h": h, "o": "", "e": rel + " audit block",
                          "n": "" if aud else "run one named falsification pass and stamp audit.last_pass_state"})
            d = prov.get(rel)
            if d is None:
                pv, why = False, "not scanned by check_provenance"
            else:
                stale = bool(d["gzf"]) and d["gzf"] != CP.CUR_GZF and d["transfers"] != CP.CUR_GZF
                pv = not (stale or d["exe"] is None or d["exe"] != CP.CUR_EXE)
                why = ("verified against the certified parent" if pv else "no exe_sha256 stamp" if d["exe"] is None else
                       "different binary" if d["exe"] != CP.CUR_EXE else "stale parent stamp")
            facts.append({"k": "DV:" + rel, "f": "DV", "ok": pv, "st": why, "doc": rel, "h": h, "o": "", "e": rel + " verified_against",
                          "n": "" if pv else "re-verify against the certified parent, then update the stamp"})

    @fam("R")
    def _r():
        import check_formats as CF
        s, e, stp, tot = CF.derive_population(db)
        claims, _c = CF.claimed_slots(db)
        slots = list(range(s, e + 1, stp))
        if len(slots) != tot:
            raise ValueError("registry bounds give %d slots, the document states %d" % (len(slots), tot))
        for k in slots:
            ok = k in claims
            facts.append({"k": "R:%08X" % k, "f": "R", "ok": ok, "st": "explained" if ok else "unexplained", "doc": None, "h": [],
                          "o": "", "e": "registry slot %08X%s" % (k, (" (" + ", ".join(claims[k][:2]) + ")") if ok else ""),
                          "n": "" if ok else "read the slot's principal consumer and declare it (registry_slots:)"})

    @fam("X")
    def _x():
        import check_assets as CA
        census = CA.load_census()
        claims = CA.claimed_formats(db)
        counted, _r, _c, _s, bucketed, _m = CA.evaluate(census, claims)
        for ext in sorted(census):
            if ext in bucketed:
                continue                  # C4: a bucket is not a requirement; its member formats are (below)
            ok = ext in counted
            facts.append({"k": "X:" + ext, "f": "X", "ok": ok, "st": "explained/dispositioned" if ok else "not dispositioned", "doc": None,
                          "h": [], "o": "", "e": "archive format .%s (census_archive_formats)" % ext,
                          "n": "" if ok else "disposition the format (explained / standard / external)"})
        if not bucketed:
            return
        members, problems = bucket_members_check(sorted(bucketed))
        if problems:
            gaps["X"] = ("%s; until the member rows cover the full signature census, those files are UNMEASURED at format "
                         "granularity - repair: %s" % ("; ".join(problems[:8]), BUCKET_REPAIR))
        good = {t for t, rows in claims.items() for _d, disp, _n in rows if disp in ("explained", "standard", "external")}
        for ext in sorted(bucketed):
            for fam_, sigs in members.get(ext, []):
                ok = fam_ in good or any(sg in good for sg in sigs)
                facts.append({"k": "X:%s/%s" % (ext, fam_), "f": "X", "ok": ok,
                              "st": "member format explained" if ok else "member format not declared", "doc": None, "h": [],
                              "o": "SWE2-DATA (formats)", "e": ".%s member %s (signatures %s)" % (ext, fam_, ",".join(sigs)),
                              "n": "" if ok else "declare the member format (archive_formats: signature-scoped row)"})

    @fam("E")
    def _e():
        import check_ebp as CE
        claimed = CE.claimed_units(db)
        for u in CE.UNITS:
            ok = u in claimed
            facts.append({"k": "E:" + u, "f": "E", "ok": ok, "st": "explained" if ok else "unexplained", "doc": None, "h": [], "o": "",
                          "e": "EBP unit %s" % u, "n": "" if ok else "explain the unit (ebp_units:)"})

    @fam("K")
    def _k():
        import goal_gate as GG
        for l in io.open(os.path.join(db, "_index", "CONTRADICTIONS.tsv"), encoding="utf-8", errors="replace"):
            if l.startswith("#") or not l.strip():
                continue
            c = l.rstrip("\r\n").split("\t")
            if len(c) < 3 or c[0] == "id":
                continue
            kind = c[2].strip().upper(); ok = kind in GG.RESOLVED_CONTRA_KINDS
            top = _rel_top(c[4]) if len(c) > 4 and c[4] else (c[3] if len(c) > 3 else "")
            h = [["folder", top]] if re.fullmatch(r"\d\d|_experiments|_types", top or "") else []
            facts.append({"k": "K:" + c[0], "f": "K", "ok": ok, "st": kind, "doc": c[4] if len(c) > 4 and top != "_index" else None,
                          "h": h, "o": "", "e": "_index/CONTRADICTIONS.tsv %s" % c[0], "n": "" if ok else "disposition the contradiction"})

    for f in (_q, _p, _f, _d, _r, _x, _e, _k):
        f()
    return {"version": VERSION, "facts": facts, "failed": failed, "gaps": gaps, "excluded": excluded, "counts": counts}


def _run(name, fn, failed):
    def go():
        try:
            fn()
        except Exception as e:  # a family that cannot be read is UNMEASURED, never zero
            failed[name] = "%s: %s" % (type(e).__name__, e)
    return go


def audited(t):
    """progress.py's audit_coverage rule - shared, not ported. DATA's
    MY-PROGRESS-METRICS review (2026-10-01) found this function was a
    hand-copied port of the scorer's inline rule: a rule corrected three
    times in one night is exactly the kind that drifts when kept in two
    places, and the review decided the dashboard must import the canonical
    `progress.audit_pass_recorded` rather than keep its own copy."""
    sys.path.insert(0, GS)
    import progress as PR
    return PR.audit_pass_recorded(t)


# ------------------------------------------------------------------------------------------------ measure (pure)
def load_map(path):
    out = collections.defaultdict(dict)
    for l in io.open(path, encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        c = l.rstrip("\r\n").split("\t")
        if c[0] == "kind" or len(c) < 3:
            continue
        out[c[0]][c[1]] = [g.strip() for g in c[2].split(",") if g.strip()]
    bad = [(k, x) for kind in out.values() for k, gs in kind.items() for x in gs if x not in GROUPS and x not in (WHOLE, UNTIED)]
    if bad:
        raise ValueError("category map names unknown group(s): %s" % bad[:3])
    return out


def place(fact, cmap):
    """Groups for one fact: every hint of the first kind that resolves; family defaults; else unplaced (None)."""
    if fact["f"] in FAMILY_GROUP:
        return FAMILY_GROUP[fact["f"]]
    by = collections.OrderedDict()
    for kind, key in fact.get("h", []):
        gs = cmap.get(kind, {}).get(key)
        if gs is not None:
            by.setdefault(kind, set()).update(gs)
    for kind in ("folder", "section", "owner", "boundary", "domain"):
        if kind in by:
            return sorted(by[kind])
    if fact["f"] == "F":
        return [UNTIED]
    if fact["f"] == "K":
        return [WHOLE]
    return None


def l2_pages(subsystems_tsv):
    pages, bysys = set(), {}
    rows = [l.rstrip("\r\n").split("\t") for l in io.open(subsystems_tsv, encoding="utf-8")]
    for r in rows[1:]:
        if len(r) < 5 or not r[0].startswith("S-"):
            continue
        ps = [re.sub(r"^(\.\./)+", "", x.strip()) for x in (r[4] + ";" + (r[5] if len(r) > 5 else "")).split(";") if x.strip()]
        pages.update(ps); bysys[r[0]] = {"category": r[1][:2], "name": r[2], "pages": ps}
    return pages, bysys


def l2_facts(reporter, bysys):
    """L2 cells from DATA's reporter snapshot: S-id x dimension; N/A is not a requirement; LIVE counts only when the
    reporter records no unruled LIVE cell in that dimension."""
    L2 = reporter["levels"]["L2_reconstruction_grade"]
    unruled = L2.get("per_dimension_live_unruled", {})
    out = []
    for s in L2.get("systems", []):
        for dim in ("contract", "types", "relationships", "runtime", "script_data"):
            v = (s.get(dim) or "UNSCORED").upper()
            if v == "N/A":
                continue
            ok = v == "MET" or (v == "LIVE" and unruled.get(dim, 1) == 0)
            cat = (bysys.get(s["system"]) or {}).get("category")
            out.append({"k": "L2:%s:%s" % (s["system"], dim), "f": "L2", "ok": ok, "st": v, "doc": None,
                        "h": [["folder", cat]] if cat else [], "o": "SWE2-AUDIT-SEM (scoring)", "e": "_index/L2-VERDICTS.md %s %s" % (s["system"], dim),
                        "n": "" if ok else "close the binding gap recorded for %s (%s)" % (s["system"], dim)})
    return out


def terminal_facts(gate, reporter):
    """Thirty passes, accepted whole or not at all (DASHBOARD-MEANINGS 4e, FABLE-REQ-OPUS-MP2-TERMINAL-COUNT): 30 only when
    the governing gate's acceptance check passed, otherwise 0. The reporter's counter (final_audits_declared) is a run in
    progress - observed, never accepted - and terminal_observed() carries it beside T, never inside it."""
    tc = reporter["levels"].get("terminal_certification", {})
    req = tc.get("required_consecutive", TERMINAL_PASSES)
    if isinstance(req, bool) or not isinstance(req, int) or req != TERMINAL_PASSES:
        # ASTRA's My Progress REJECT (037557884): a supplied required 0 made T read accepted 0 of 0 and the tab Ready. The
        # protocol fixes thirty; any other supplied count is a failed prerequisite, never a smaller requirement.
        raise ValueError("the reporter supplies %r terminal passes; the final-audit protocol requires exactly %d" % (req, TERMINAL_PASSES))
    acc_line = next((d for d in gate.get("detail", []) if d.startswith("acceptance:")), "")
    n = req if " OK " in acc_line else 0
    return [{"k": "T:%02d" % i, "f": "T", "ok": i <= n, "st": "accepted" if i <= n else "not run", "doc": None, "h": [],
             "o": "final-audit protocol (FRONTIER operates, independent auditors run)", "e": "_index/AUDIT-LOG.md; FINAL-AUDIT-PROTOCOL.md pass %d" % i,
             "n": "" if i <= n else "runs only after every other requirement is accepted"} for i in range(1, req + 1)], n, req


def terminal_observed(gate, reporter):
    """The run in progress, shown beside T: pass k of 30 from the reporter's counter while 0 < k < 30 and the gate has not
    accepted a run. None when no run is in progress. It is observed progress: never summed with T or any accepted count."""
    tc = reporter["levels"].get("terminal_certification", {})
    acc_line = next((d for d in gate.get("detail", []) if d.startswith("acceptance:")), "")
    k = tc.get("final_audits_declared")
    if " OK " in acc_line or isinstance(k, bool) or not isinstance(k, int) or not 0 < k < TERMINAL_PASSES:
        return None
    return {"pass": k, "of": TERMINAL_PASSES, "state": "observed, not accepted",
            "source": "PROGRAM-STATE final_audits counter; a failed pass or database drift ends the run (not carried over)"}


def board_index(board):
    """Open (non-DONE) tasks by every register-style id they mention - the owner and next action of a requirement."""
    idx = collections.defaultdict(list)
    for t in board.get("tasks", []):
        if t.get("status") in ("DONE", "CANCELLED", "WITHDRAWN"):
            continue
        txt = json.dumps({k: t.get(k) for k in ("id", "title", "question", "scope", "target", "checkpoint")})
        for rid in set(re.findall(r"\b([A-Z]{1,4}-\d{1,4}[a-z]?)\b", txt)):
            idx[rid].append(t)
    return idx


def measure(facts_doc, cmap, board, reporter, gate, subsystems_tsv, prior=None):
    facts = list(facts_doc["facts"])
    failed = dict(facts_doc.get("failed", {}))
    gaps = dict(facts_doc.get("gaps", {}))
    pages, bysys = l2_pages(subsystems_tsv)
    try:
        facts += l2_facts(reporter, bysys)
    except Exception as e:
        failed["L2"] = "%s: %s" % (type(e).__name__, e)
    try:
        tf, t_acc, t_req = terminal_facts(gate, reporter)
        facts += tf
    except Exception as e:
        failed["T"] = "%s: %s" % (type(e).__name__, e); t_acc, t_req = None, 30
    try:
        t_obs = terminal_observed(gate, reporter)
    except Exception:
        t_obs = None
    idx = board_index(board)
    seen, uniq, dup = {}, [], 0
    for f in facts:                      # one requirement per key: a key seen twice is the same requirement (dedup)
        if f["k"] in seen:
            dup += 1; prev = seen[f["k"]]; prev["ok"] = prev["ok"] and f["ok"]; continue
        seen[f["k"]] = f; uniq.append(f)
    unplaced = []
    for f in uniq:
        lv = LEVELS[f["f"]]
        if f["f"] in ("Q", "P", "DD", "DA", "DV") and f.get("doc") in pages:
            lv = "L1L2"
        f["lv"] = lv
        g = place(f, cmap)
        if g is None:
            unplaced.append(f["k"]); g = [WHOLE]
        f["g"] = g
        if (f.get("doc") or "").startswith("_experiments"):          # C3: an evidence record, not a game system
            f["st"] = "evidence record - " + f["st"]
        if not f["ok"] and f["f"] == "Q":
            ts = idx.get(f["k"][2:], [])
            if ts:
                t = sorted(ts, key=lambda x: x.get("updated_at") or "")[-1]
                f["o"] = t.get("assigned_to") or t.get("agent") or ""
                f["n"] = "%s (%s): %s" % (t["id"], t.get("status"), (t.get("title") or t.get("question") or "")[:140])
    def agg(sel):
        xs = [f for f in uniq if sel(f)]
        return {"accepted": sum(1 for f in xs if f["ok"]), "total": len(xs)}
    scopes = {"union": agg(lambda f: True), "L1": agg(lambda f: "L1" in f["lv"]), "L2": agg(lambda f: "L2" in f["lv"]),
              "union_exF": agg(lambda f: f["f"] != "F"),                 # C1: the same figure without the function population
              "L2_specific": agg(lambda f: f["lv"] == "L2")}             # the L2-only (scoped) requirements, e.g. the S-id x dimension cells
    scopes["L2_cumulative"] = cumulative_l2(scopes["L1"], scopes["L2_specific"])
    qs = [f for f in uniq if f["f"] == "Q"]
    bare = lambda st: st[len("evidence record - "):] if st.startswith("evidence record - ") else st   # the C3 label is display only
    q_split = {"answered": sum(1 for f in qs if f["ok"] and bare(f["st"]) == "ANSWERED"),       # C2
               "dispositioned": sum(1 for f in qs if f["ok"] and bare(f["st"]) != "ANSWERED"),
               "remaining": sum(1 for f in qs if not f["ok"]),
               "excluded": sum(1 for k_, _w in facts_doc.get("excluded", []) if k_.startswith("Q:")),
               "dd_answered": sum(1 for f in uniq if f["f"] == "DD" and f["ok"] and f["st"] != "documented with a dispositioned residue"),
               "dd_dispositioned": sum(1 for f in uniq if f["f"] == "DD" and f["ok"] and f["st"] == "documented with a dispositioned residue")}
    fams = {k: agg(lambda f, k=k: f["f"] == k) for k in FAMILIES}
    cats = collections.OrderedDict((g, agg(lambda f, g=g: g in f["g"])) for g in list(GROUPS) + [WHOLE, UNTIED])
    measured = not failed and not gaps
    remaining = collections.defaultdict(list)
    for f in uniq:
        if not f["ok"]:
            for g in f["g"]:
                remaining[g].append(f)
    ready = (measured and gate.get("verdict") == "MET" and scopes["union"]["accepted"] == scopes["union"]["total"])
    why_not = ("the governing goal gate reads %s: %s" % (gate.get("verdict"), gate.get("remaining")) if gate.get("verdict") != "MET" else
               "requirements remain (%d)" % (scopes["union"]["total"] - scopes["union"]["accepted"]) if measured else
               "requirements are not fully enumerated: %s" % "; ".join(["%s: reader failed" % k for k in sorted(failed)] +
                                                                       ["%s: %s" % kv for kv in sorted(gaps.items())]))
    return {"version": VERSION, "measured": measured, "failed": failed, "gaps": gaps, "q_split": q_split, "scopes": scopes, "families": fams, "categories": cats,
            "terminal": {"accepted": t_acc, "required": t_req}, "terminal_observed": t_obs, "unplaced": unplaced, "duplicates_merged": dup,
            "excluded": facts_doc.get("excluded", []), "remaining": remaining, "ready": ready, "why_not_ready": "" if ready else why_not,
            "change": change(prior, scopes, cats) if prior is not None else None}


def cumulative_l2(l1, l2s):
    """Cumulative L2 (user ruling 2026-09-30): L2 presupposes L1, so cumulative L2 is gated by L1 and never exceeds it.
    It reports the LOWER of the two fractions with that scope's own numerator and denominator - never an average of
    unrelated denominators - and is COMPLETE only when L1 and the L2-specific requirements are both complete. While L1
    is incomplete it reads NOT COMPLETE even when the L2-specific requirements are at 100 %."""
    frac = lambda s: (s["accepted"] / s["total"]) if s["total"] else 0.0
    done = lambda s: bool(s["total"]) and s["accepted"] == s["total"]
    bound, by = (l1, "L1") if frac(l1) <= frac(l2s) else (l2s, "L2_specific")
    state = "COMPLETE" if done(l1) and done(l2s) else "NOT COMPLETE"
    why = ("" if state == "COMPLETE" else "L1 is incomplete (%d of %d); cumulative L2 cannot be complete before L1" % (l1["accepted"], l1["total"])
           if not done(l1) else "L2-specific requirements remain (%d of %d)" % (l2s["accepted"], l2s["total"]))
    return {"accepted": bound["accepted"], "total": bound["total"], "bounded_by": by, "state": state, "why": why}


def change(prior, scopes, cats):
    """Accepted-work movement and scope movement, kept apart. `prior` is the progress block of an earlier verified
    generation; a different metric version is not comparable."""
    if prior.get("version") != VERSION:
        return {"comparable": False, "why": "definition changed (%s -> %s); not comparable" % (prior.get("version"), VERSION)}
    def d(now, then):
        if not then:
            return {"new": True}
        return {"accepted": now["accepted"] - then["accepted"], "scope": now["total"] - then["total"],
                "pct": (100.0 * now["accepted"] / now["total"] if now["total"] else 0) - (100.0 * then["accepted"] / then["total"] if then["total"] else 0)}
    return {"comparable": True, "generation": prior.get("generation"), "committed_at": prior.get("committed_at"),
            "scopes": {k: d(v, prior.get("scopes", {}).get(k)) for k, v in scopes.items()},
            "categories": {k: d(v, prior.get("categories", {}).get(k)) for k, v in cats.items()}}


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="collect requirement facts (MP-1) into a JSON file")
    ap.add_argument("--db", required=True); ap.add_argument("--out", required=True)
    ap.add_argument("--residual"); ap.add_argument("--functions"); ap.add_argument("--board")
    a = ap.parse_args()
    doc = collect(a.db, a.residual, a.functions, a.board)
    json.dump(doc, open(a.out, "w", encoding="utf-8"), separators=(",", ":"))
    print("facts %d, failed %s, excluded %d" % (len(doc["facts"]), doc["failed"] or "none", len(doc["excluded"])))
