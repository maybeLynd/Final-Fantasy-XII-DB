"""denominators.py - every runtime cell of L2-VERDICTS.md that moves named material out of its denominator, printed
next to the registry subject it is scored for (SWE2-AUDIT-SPEC, 2026-10-03, expansion item 2).

The pattern list is AUDIT-SEM's denom.py plus the exclusion wordings found in this sample's rows ("outside this
contract's subject", "callee-depth", "contract-excluded"). A worklist for a hand read, not a score.
Writes denominators.txt next to this file."""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
IDX = os.path.normpath(os.path.join(HERE, "..", ".."))
PAT = re.compile(r"out of (the|this) (runtime )?denominator|outside the (L2 |runtime )?denominator|"
                 r"outside this contract's subject|out of this contract's runtime denominator|static-structure|"
                 r"ruled outside|unreachable from every disclosed|device-gated|not in the denominator|callee-depth|"
                 r"contract-excluded", re.I)


def main():
    reg = {}
    for line in open(os.path.join(IDX, "important-subsystems.tsv"), encoding="utf-8"):
        p = line.split("\t")
        if p[0].startswith("S-"):
            reg[p[0]] = p[2]
    out, seen = [], set()
    for line in open(os.path.join(IDX, "L2-VERDICTS.md"), encoding="utf-8").read().splitlines():
        m = re.match(r"\| \*\*(S-\d+)\*\*", line)
        if not m or m.group(1) in seen:
            continue
        c = [x.strip() for x in re.split(r"(?<!\\)\|", line)[1:-1]]
        if len(c) < 8:
            continue
        seen.add(m.group(1))
        hits = list(PAT.finditer(c[4]))
        if not hits:
            continue
        out.append("===== %s | L2 %s | SUBJECT: %s" % (m.group(1), c[6][:12], reg.get(m.group(1), "?")))
        for h in hits:
            a = max(0, h.start() - 300)
            out.append("   ..." + c[4][a:h.end() + 120] + "...")
    open(os.path.join(HERE, "denominators.txt"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("rows:", sum(1 for x in out if x.startswith("=====")))


if __name__ == "__main__":
    main()
