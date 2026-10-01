"""SWE2-AUDIT-SEM GI-RESTATUS check (own code), on the 13 pages as committed at c97af7156 (git show, so peers'
uncommitted edits are not read).
A  each page's status line: the GI id it names, and that id's register row status at the same commit.
B  a residue sweep wider than residue_scan.py: every line, outside struck spans and outside the status line, that says
   'not yet', 'unknown', 'unresolved', 'still open', 'open question', 'TODO', 'not read', 'unverified', 'unclear',
   'to be determined' or 'remains open'. Printed with the heading it sits under, for reading.
C  the shop page: the two struck bullets' text, the 0xF / 0x12 decoding in the page, and the 0057A4E0 section."""
import re, subprocess
REPO = "C:/Users/Kristian/source/repos/XIIOnline"
C = "c97af7156"
PAGES = subprocess.run(["git", "-C", REPO, "show", "--name-only", "--format=", C], capture_output=True, text=True).stdout.split("\n")
PAGES = [p for p in PAGES if p.endswith(".md") and "/_index/" not in p]
def show(path):
    return subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (C, path)], capture_output=True, text=True,
                          encoding="utf-8").stdout
oq = show("Database/FFXII TZA/_index/OPEN-QUESTIONS.md")
rowstat = {}
for l in oq.split("\n"):
    m = re.match(r"\|\s*(GI-\d+)\s*\|", l)
    if m:
        cells = l.split("|")
        rowstat[m.group(1)] = re.sub(r"\s+", " ", cells[3])[:90] if len(cells) > 3 else "?"
RES = re.compile(r"not yet|unknown|unresolved|still open|open question|TODO|not read|unverified|unclear|to be determined|remains open", re.I)
for p in PAGES:
    t = show(p)
    lines = t.split("\n")
    st = next((l for l in lines[:15] if l.lower().startswith("status:")), "(no status line)")
    ids = sorted(set(re.findall(r"GI-\d+", st)))
    print("== %s" % p.replace("Database/FFXII TZA/", ""))
    print("   status: %s" % st[:230])
    for i in ids:
        print("   %s register: %s" % (i, rowstat.get(i, "(no row)")))
    head = ""
    hits = 0
    for n, l in enumerate(lines):
        if l.startswith("#"):
            head = l[:70]
        if l.lower().startswith("status:"):
            continue
        clean = re.sub(r"~~.*?~~", "", l)
        if RES.search(clean):
            hits += 1
            if hits <= 12:
                print("   B %4d [%s] %s" % (n + 1, head, clean.strip()[:190]))
    print("   B residue-word lines: %d" % hits)
shop = next(p for p in PAGES if "shop" in p)
t = show(shop)
print("== C shop page")
for n, l in enumerate(t.split("\n")):
    if "0057A4E0" in l or re.search(r"\b0x(F|12)\b", l) and ("notif" in l or "pre-destroy" in l or "list-mode" in l or "list mode" in l):
        print("   %4d %s" % (n + 1, l.strip()[:220]))
