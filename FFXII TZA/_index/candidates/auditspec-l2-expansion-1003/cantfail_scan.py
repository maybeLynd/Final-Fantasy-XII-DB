"""cantfail_scan.py - worklist of replay cases that may be unable to fail (SWE2-AUDIT-SPEC, 2026-10-03, item 4 of
OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003).

Method.
  1. For every verdict row of L2-VERDICTS.md whose runtime cell is MET or LIVE, find the replay packages the cell
     names: any directory under _index/candidates/ or _experiments/evidence/ whose name occurs in the cell text.
     A cited EXP-NNN is resolved to _experiments/evidence/ directories named in that EXP record, if any; a cited
     `name.py` resolves to every package directory holding that file; and every candidates/sNN-* directory of
     the row's own system is included (the closer packages are named that way).
  2. Scan every .py file of those packages, line by line, for six shapes:
       LITERAL_PASS   a case/record call whose verdict argument is the literal True
                      (record("x", True ... / cases["x"] = True / ok("x", True)
       SELF_COMPARE   `A == A` or `A is A` with the same expression on both sides
       NO_COMPARE     a case assignment whose right-hand side contains no comparison/boolean operator
                      (==, !=, <, >, <=, >=, in, not, and, or, all(, any(, is)
       PRINT_ONLY     an `observed`/`seen`/`_observed` key written into results but never used in a case
       FROM_INPUT     a case comparing an output to the very name it planted on the same line pattern
                      (expected = planted; heuristic: `== planted`/`== fixture`/`== PLANT`)
       SINGLE_THREAD  a package whose cited invariant text mentions thread/handshake/concurrent while the
                      harness never creates a second emulator/thread (no `threading`, no second `Uc(`)
     The scan is lexical. Every hit is a candidate only; the judgment is made by reading the case and the
     contract invariant it is credited to (item4.md).

Limits. Lexical patterns miss cases built through helper functions and over-report boolean flags computed
elsewhere. Packages not named in the cell text (credited only through a page) are not scanned. Read-only over
the database; writes cantfail.tsv next to this file.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
IDX = os.path.join(DB, "_index")
CAND = os.path.join(IDX, "candidates")
EVID = os.path.join(DB, "_experiments", "evidence")
EXPD = os.path.join(DB, "_experiments")

CMP = re.compile(r"==|!=|<=|>=|<|>|\bin\b|\bnot\b|\band\b|\bor\b|\ball\(|\bany\(|\bis\b")
LIT = re.compile(r"""(?:record|ok|check|case|add_case|res|R)\(\s*["'][^"']+["']\s*,\s*True\s*[,)]""")
ASSIGN_CASE = re.compile(r"""(?:cases|CASES|results\[["']cases["']\])\[\s*["']([^"']+)["']\s*\]\s*(?:&=|=)\s*(.+)$""")
SELF = re.compile(r"(?<![\w.&|])([A-Za-z_][\w.\[\]'\"]*)\s*(?:==|\s\bis\b\s)\s*\1(?![\w.(\[])")
OBS = re.compile(r"""["']([A-Za-z0-9_]*observed[A-Za-z0-9_]*)["']""")
THREADWORD = re.compile(r"\bthread|\bhandshake|concurren|\brace\b|\braces\b", re.I)


def verdict_runtime_cells():
    seen, out = set(), []
    for line in open(os.path.join(IDX, "L2-VERDICTS.md"), encoding="utf-8").read().splitlines():
        m = re.match(r"^\|\s*\*\*(S-\d+)\*\*", line)
        if not m or m.group(1) in seen:
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 8:
            continue
        seen.add(m.group(1))
        rt = cells[4]
        lead = re.sub(r"~~.*?~~", "", rt).strip().strip("*").strip()
        if lead.startswith(("MET", "LIVE")):
            out.append((m.group(1), rt))
    return out


def package_dirs():
    dirs = {}
    for base in (CAND, EVID):
        if os.path.isdir(base):
            for n in os.listdir(base):
                p = os.path.join(base, n)
                if os.path.isdir(p) and len(n) >= 8:
                    dirs[n] = p
    return dirs


def exp_dirs(exp, dirs):
    hits = set()
    for n in os.listdir(EXPD):
        if n.startswith(exp + "-") and n.endswith(".md"):
            t = open(os.path.join(EXPD, n), encoding="utf-8", errors="replace").read()
            for d in dirs:
                if d in t and dirs[d].startswith(EVID):
                    hits.add(d)
    return hits


def scan_file(pkg, path, threaded_claim):
    rows = []
    try:
        lines = open(path, encoding="utf-8", errors="replace").read().splitlines()
    except OSError:
        return rows
    text = "\n".join(lines)
    used_obs = set()
    for ln, l in enumerate(lines, 1):
        s = l.strip()
        if s.startswith("#"):
            continue
        if LIT.search(s):
            rows.append((pkg, "%s:%d" % (os.path.basename(path), ln), "LITERAL_PASS", s[:140]))
        m = ASSIGN_CASE.search(s)
        if m:
            rhs = m.group(2)
            if rhs.strip() in ("True", "1"):
                rows.append((pkg, "%s:%d" % (os.path.basename(path), ln), "LITERAL_PASS", m.group(1)))
            elif not CMP.search(rhs) and "(" not in rhs:
                rows.append((pkg, "%s:%d" % (os.path.basename(path), ln), "NO_COMPARE", m.group(1)))
            if re.search(r"==\s*(?:planted|fixture|PLANT\w*)\b", rhs):
                rows.append((pkg, "%s:%d" % (os.path.basename(path), ln), "FROM_INPUT", m.group(1)))
        for sm in SELF.finditer(s):
            if not sm.group(1).isdigit() and sm.group(1) not in ("None", "True", "False"):
                rows.append((pkg, "%s:%d" % (os.path.basename(path), ln), "SELF_COMPARE", s[:140]))
    for ob in set(OBS.findall(text)):
        uses = [l for l in lines if ob in l]
        if not any(ASSIGN_CASE.search(u.strip()) or "assert" in u for u in uses):
            rows.append((pkg, os.path.basename(path), "PRINT_ONLY", ob))
    if threaded_claim and "threading" not in text and len(re.findall(r"\bUc\(", text)) <= 1 and "Uc(" in text:
        rows.append((pkg, os.path.basename(path), "SINGLE_THREAD", "cell cites thread/handshake; one emulator"))
    return rows


def main():
    dirs = package_dirs()
    out = []
    for sid, rt in verdict_runtime_cells():
        pk = {d for d in dirs if d in rt}
        for exp in set(re.findall(r"EXP-\d+", rt)):
            pk |= exp_dirs(exp, dirs)
        # a cited script name (`pump_states.py`) resolves to every package directory holding that file
        generic = {"check.py", "world.py", "run.py", "main.py", "harness.py", "common.py", "run_review.py"}
        for py in set(re.findall(r"([A-Za-z0-9_]+\.py)", rt)) - generic:
            pk |= {d for d, p in dirs.items() if os.path.isfile(os.path.join(p, py))}
        # the system's own closer packages: candidates/sNN-* (S-22 -> s22-...)
        pre = "s%02d-" % int(sid[2:])
        pk |= {d for d, p in dirs.items() if d.startswith(pre) and p.startswith(CAND)}
        threaded = bool(THREADWORD.search(rt))
        if not pk:
            out.append((sid, "-", "-", "NO_PACKAGE_NAMED", "runtime cell names no package directory"))
        for d in sorted(pk):
            for root, _, files in os.walk(dirs[d]):
                if "__pycache__" in root:
                    continue
                for fn in files:
                    if fn.endswith(".py"):
                        for r in scan_file(d, os.path.join(root, fn), threaded):
                            out.append((sid,) + r)
    with open(os.path.join(HERE, "cantfail.tsv"), "w", encoding="utf-8") as f:
        f.write("system\tpackage\tsite\tpattern\tcase\n")
        for r in out:
            f.write("\t".join(x.replace("\t", " ") for x in r) + "\n")
    from collections import Counter
    print("rows with MET/LIVE runtime:", len(verdict_runtime_cells()))
    print(Counter(r[3] for r in out))


if __name__ == "__main__":
    main()
