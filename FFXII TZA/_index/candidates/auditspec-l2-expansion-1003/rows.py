"""rows.py - the 52-row matrix the expansion works from (SWE2-AUDIT-SPEC, 2026-10-03).

For every verdict row in L2-VERDICTS.md: the registry subject and credited contracts (important-subsystems.tsv),
the leading token of each requirement cell, the lane named in each cell's decisive (first) re-score, the first
date in the cell, and whether SWE2-AUDIT-SPEC appears as a scorer anywhere in the cell (the self-audit rule:
no verdict author audits its own cells).
Writes rows.tsv next to this file. Read-only over the database."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
IDX = os.path.join(DB, "_index")
NAMES = ["contract", "types", "relationships", "runtime", "script_data", "L2"]
LANE = re.compile(r"\b(SWE2-[A-Z0-9-]+|OPUS|FABLE|ASTRA)\b")
DATE = re.compile(r"(20\d\d-\d\d-\d\d)")


def registry():
    reg = {}
    for line in open(os.path.join(IDX, "important-subsystems.tsv"), encoding="utf-8"):
        p = line.rstrip("\n").split("\t")
        if p and p[0].startswith("S-"):
            reg[p[0]] = p
    return reg


def verdict_rows():
    out = {}
    for line in open(os.path.join(IDX, "L2-VERDICTS.md"), encoding="utf-8").read().splitlines():
        m = re.match(r"^\|\s*\*\*(S-\d+)\*\*([^|]*)\|", line)
        if not m:
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(cells) < 8 or m.group(1) in out:
            continue
        out[m.group(1)] = (m.group(2).strip(), cells[1:8])
    return out


def lead(c):
    c = re.sub(r"~~.*?~~\s*(→|->)?\s*", "", c).strip().strip("*").strip()
    return re.split(r"[\s—(:]", c, 1)[0].strip("*") if c else ""


def main():
    reg, rows = registry(), verdict_rows()
    with open(os.path.join(HERE, "rows.tsv"), "w", encoding="utf-8") as f:
        f.write("system\ttitle\tsubject\tcontracts\t" + "\t".join(
            "%s_lead\t%s_lane\t%s_date" % (n, n, n) for n in NAMES) + "\tspec_in_row\n")
        for sid in sorted(rows, key=lambda s: int(s[2:])):
            title, cells = rows[sid]
            r = reg.get(sid, [""] * 6)
            cols = []
            for n, c in zip(NAMES, cells):
                m = LANE.search(c[:400])
                d = DATE.search(c[:400])
                cols += [lead(c), m.group(1) if m else ("bare" if c.strip("* ") else "empty"), d.group(1) if d else ""]
            spec = "yes" if any("SWE2-AUDIT-SPEC" in c for c in cells) else "no"
            f.write("\t".join([sid, title, r[2], r[5]] + cols + [spec]) + "\n")
    print("rows:", len(rows))


if __name__ == "__main__":
    main()
