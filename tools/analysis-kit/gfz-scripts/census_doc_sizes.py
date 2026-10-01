"""CT-4, second attempt. The first matcher took any size within 120 chars after any address and
returned 146 'findings' that were mostly offsets ('+116 bytes in'), sizes belonging to a different
column of a multi-address table row, or corpus byte totals.

Discriminating rule instead: the line must contain EXACTLY ONE address and EXACTLY ONE size, the
size must not be an offset (+N) and must not be a thousands-grouped corpus figure, and the address
must precede the size. Anything else is not a size claim this instrument can read, and is counted
as UNREADABLE rather than as a finding.
"""
import re, pathlib
import kit_paths as KP  # noqa: E402
import os

DB = pathlib.Path(os.path.join(KP.ROOT, "Database", "FFXII TZA"))
TSV = pathlib.Path(os.path.join(KP.ROOT, "Database", "Tools", "work", "graph", "functions.tsv"))

sizes, names = {}, {}
with TSV.open(encoding="utf-8", errors="replace") as fh:
    next(fh)
    for line in fh:
        p = line.rstrip("\r\n").split("\t")
        if len(p) >= 3 and p[2].isdigit():
            sizes[p[0].upper()] = int(p[2])
            names[p[0].upper()] = p[1]

ADDR = re.compile(r"`(00[0-9A-Fa-f]{6})`")
SIZE = re.compile(r"(?<![+\w,])([0-9][0-9,]{0,7})\s*(?:B|bytes)\b")

ok = bad = unreadable = 0
findings = []
for md in sorted(DB.rglob("*.md")):
    rel = md.relative_to(DB).as_posix()
    if rel.startswith("_index/"):
        continue
    for ln, line in enumerate(md.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        a = ADDR.findall(line)
        s = SIZE.findall(line)
        if not a or not s:
            continue
        if len(a) != 1 or len(s) != 1:
            unreadable += 1
            continue
        addr = a[0].upper()
        if addr not in sizes:
            unreadable += 1
            continue
        if line.index("`" + a[0] + "`") > SIZE.search(line).start():
            unreadable += 1
            continue
        claim = int(s[0].replace(",", ""))
        if sizes[addr] == claim:
            ok += 1
        else:
            bad += 1
            findings.append((rel, ln, addr, claim, sizes[addr], names[addr], line.strip()[:170]))

print(f"readable size claims matched : {ok}")
print(f"readable size claims WRONG   : {bad}")
print(f"lines this instrument cannot read (not findings): {unreadable}")
print()
for rel, ln, a, claim, real, nm, ctx in findings:
    print(f"{rel}:{ln}  {a}  doc says {claim} B, graph says {real} B   ({nm})")
    print(f"    {ctx}")
