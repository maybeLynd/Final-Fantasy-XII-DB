"""residue_scan.py LISTFILE - for each page, print the bullets of 'Not yet established' / 'Unresolved' / 'Open' /
'Limits' style sections, flagging bullets with no strike and no answered/read/resolved word."""
import io, re, sys
DB = "C:/Users/Kristian/source/repos/XIIOnline/Database/FFXII TZA/"
SEC = re.compile(r"^#{2,3} .*(not yet established|unresolved|open question|still open|remaining|not read|unknown)", re.I)
DONE = re.compile(r"~~|answered|resolved|read 20|confirmed|corrected|narrowed|decoded|closed|withdrawn", re.I)
for rel in [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]:
    t = io.open(DB + rel, encoding="utf-8").read().split("\n")
    out, on = [], False
    for i, line in enumerate(t):
        if line.startswith("#"):
            on = bool(SEC.match(line))
            if on:
                out.append("  [%d] %s" % (i + 1, line[:100]))
            continue
        if on and re.match(r"^\s*[-*] ", line):
            # join continuation lines
            j, buf = i + 1, line
            while j < len(t) and t[j].startswith("  ") and not re.match(r"^\s*[-*] ", t[j]):
                buf += " " + t[j].strip(); j += 1
            flag = "   " if DONE.search(buf) else "!! "
            out.append("    %s%s" % (flag, buf.strip()[:170]))
    print("===", rel)
    print("\n".join(out) if out else "  (no residue section)")
