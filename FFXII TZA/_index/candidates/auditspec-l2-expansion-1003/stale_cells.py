"""stale_cells.py - invariants added or amended in a credited contract after the runtime cell was scored
(SWE2-AUDIT-SPEC, 2026-10-03, item 4 of OPUS-REQ-AUDITSPEC-L2-EXPANSION-1003).

Method.
  1. For every verdict row whose runtime cell leads MET or LIVE, take the first YYYY-MM-DD in the runtime cell as the
     scoring date (rows.tsv's rule); when those first 400 characters carry none, the latest date anywhere in the cell.
     A cell with no date at all is reported as UNDATED and skipped.
  2. For each credited contract (important-subsystems.tsv column 6), list the commits touching it since that date
     (`git log --since=<date> 00:00`, core.longpaths on). Same-day commits are kept and marked SAME-DAY, because the
     order of the cell edit and the contract edit within a day is not recorded.
  3. For each commit, compare the contract's invariant DEFINITIONS before and after: a definition is a line that
     starts (after `- `, `> `, `| ` or bold markers) with an invariant-like id - `XX-n`, `XXX-n`, `I-n`, `In`, `Vn`,
     `N-n`, `ST-n` - followed by an em dash, a colon, a period or a table cell. The id's definition text is the line.
       ADDED    the id has a definition after the commit and none before it
       AMENDED  the id's definition line differs (ignoring strike-through markup and whitespace)
       REMOVED  the id had a definition before and none after
  4. A commit whose subject marks it as a pass-22 crossings block, a citation pass or a front-matter stamp is still
     listed but tagged COSMETIC-SUBJECT; an AMENDED line whose only difference is an appended "(answered: ...)" /
     "(corrected ...)" parenthetical is tagged ANNOTATION. Both still need a read: an annotation can change meaning.

Limits. Invariants defined in prose without an id, or whose id appears only mid-line, are invisible. A rename of an id
reads as REMOVED + ADDED. Read-only over the database; writes stale.tsv next to this file.
"""
import csv
import os
import re
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
ROOT = os.path.normpath(os.path.join(DB, "..", ".."))
IDX = os.path.join(DB, "_index")
DEF = re.compile(r"^\s*(?:[-*>]\s*)*(?:\|\s*)?(?:\*\*|~~)*\s*((?:[A-Z]{1,4}-\d+[a-z]?)|(?:I\d+)|(?:V\d+))\b(?:\*\*)?\s*(?:—|–|-|:|\.|\|)")
COSMETIC = re.compile(r"pass 22|pass-22|crossings|citation|interior citations|neighbour|front.?matter|stamp", re.I)


def git(*a):
    return subprocess.run(["git", "-c", "core.longpaths=true", *a], cwd=ROOT, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def defs(text):
    out = {}
    for line in text.splitlines():
        m = DEF.match(line)
        if m and m.group(1) not in out:
            out[m.group(1)] = line.strip()
    return out


def norm(s):
    s = re.sub(r"~~.*?~~", "", s)
    return re.sub(r"\s+", " ", s).strip()


def full_cell_date(sid):
    """Fallback when the first 400 characters of the runtime cell carry no date: the LATEST date anywhere in it."""
    for line in open(os.path.join(IDX, "L2-VERDICTS.md"), encoding="utf-8").read().splitlines():
        if re.match(r"^\|\s*\*\*%s\*\*" % re.escape(sid), line):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
            if len(cells) >= 8:
                ds = re.findall(r"20\d\d-\d\d-\d\d", cells[4])
                return max(ds) if ds else ""
    return ""


def main():
    reg = {}
    for line in open(os.path.join(IDX, "important-subsystems.tsv"), encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if p and p[0].startswith("S-"):
            reg[p[0]] = p
    rows = list(csv.DictReader(open(os.path.join(HERE, "rows.tsv"), encoding="utf-8"), delimiter="\t"))
    out = []
    for r in rows:
        if r["runtime_lead"] not in ("MET", "LIVE"):
            continue
        date = r["runtime_date"] or full_cell_date(r["system"])
        if not date:
            out.append((r["system"], "-", "-", "-", "-", "UNDATED", ""))
            continue
        for c in [x.strip() for x in reg[r["system"]][5].split(";") if x.strip()]:
            rel = os.path.relpath(os.path.normpath(os.path.join(IDX, c)), ROOT).replace("\\", "/")
            log = git("log", "--reverse", "--format=%h\t%ad\t%s", "--date=short", "--since=%s 00:00" % date, "--", rel)
            for entry in [x for x in log.splitlines() if x.strip()]:
                h, d, subj = entry.split("\t", 2)
                before = defs(git("show", "%s^:%s" % (h, rel)))
                after = defs(git("show", "%s:%s" % (h, rel)))
                tags = []
                if d == date:
                    tags.append("SAME-DAY")
                if COSMETIC.search(subj):
                    tags.append("COSMETIC-SUBJECT")
                for k in sorted(set(before) | set(after)):
                    if k in after and k not in before:
                        kind = "ADDED"
                    elif k in before and k not in after:
                        kind = "REMOVED"
                    elif norm(before[k]) != norm(after[k]):
                        b, a = norm(before[k]), norm(after[k])
                        kind = "AMENDED"
                        if a.startswith(b[: max(20, len(b) - 3)]) and re.search(r"\((answered|corrected|qualified|amended)", a[len(b) - 3:], re.I):
                            kind = "AMENDED/ANNOTATION"
                    else:
                        continue
                    out.append((r["system"], os.path.basename(rel), k, h, d, kind + ("/" + "/".join(tags) if tags else ""),
                                subj[:90]))
    with open(os.path.join(HERE, "stale.tsv"), "w", encoding="utf-8") as f:
        f.write("system\tcontract\tinvariant\tcommit\tdate\tchange\tsubject\n")
        for o in out:
            f.write("\t".join(str(x).replace("\t", " ") for x in o) + "\n")
    from collections import Counter
    print(len(out), "rows;", Counter(o[0] for o in out).most_common())


if __name__ == "__main__":
    main()
