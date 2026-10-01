"""SWE2-AUDIT-SEM attacks on documented_rule.py at 48391d7f6 (conditions U and N, self-test S).
Part 1 - adversarial pages judged by the shipped judge() against the real register.
Part 2 - mutants of the rule (scratch copies): each must make the S self-test FAIL, or S does not guard that code."""
import sys, os, io, re, subprocess, shutil
R = r"C:\Users\Kristian\source\repos\XIIOnline\Database\FFXII TZA\_index\candidates\status-currency-ruling-fable"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, R)
import documented_rule as D
state, kind, word, dup = D.register()
ans = next(i for i in sorted(state) if kind[i] == "answered" and re.fullmatch(D.ID[2:-2], i))
NL = "\n"
base = "---\nstatus: DOCUMENTED (%s answered)\n---\n# x\nbody\n" % ans


def note(kind_line="note_kind: census", parent="parent: authored-data-table-registry.md", sections=None, table="| claim | evidence | tier |\n|---|---|---|"):
    sec = sections if sections is not None else ["## Scope", "x", "## Findings", "x", "## Evidence", table, "## Method", "x", "## Limits", "x"]
    return base.replace("status:", kind_line + NL + parent + NL + "status:", 1) + NL.join(sec) + NL


pd = os.path.join(D.DB, "02-Resource-And-Asset-Pipeline")  # a real page directory, so parent resolution runs
cases = [
    # U: legitimate non-register tokens that share a register prefix
    ("subsystem id S-31 (L2-VERDICTS row, not a register question)", base + "S-31's verdict turns on it\n", None),
    ("zero-padded subsystem id S-05 (register has S-5)", base + "see S-05's contract\n", None),
    ("ASTRA-QUEUE item AQ-9 (register AQ-1..6 are other questions)", base + "AQ-9 prediction recorded\n", None),
    ("contract invariant I-10", base + "see invariant I-10\n", None),
    ("My Progress requirement MP-3", base + "MP-3 reads the declaration\n", None),
    ("register id EC-7 used as the mechanism name", base + "the EC-7 mechanism\n", None),
    ("unknown token only in YAML frontmatter", base.replace("status:", "sources: [S-44]\nstatus:", 1), None),
    # N: hollow notes
    ("note: five headings, no content, header-only tier table", note(sections=["## Scope", "## Findings", "## Evidence", "| claim | evidence | tier |", "|---|---|---|", "## Method", "## Limits"]), pd),
    ("note: 'Out of scope' / 'Results' / 'No limits' headings", note(sections=["## Out of scope", "## Results", "## Evidence", "| a | tier |", "## Methodology", "## No limits"]), pd),
    ("note: parent is the directory itself", note(parent="parent: ."), pd),
    ("note: parent is the page's own folder file README-less path ..", note(parent="parent: .."), pd),
    ("note: tier column only in an unrelated table", note(sections=["## Scope", "x", "## Findings", "x", "## Evidence", "prose only", "## Method", "x", "## Limits", "x", "| name | tier |"]), pd),
    ("note: note_kind in the BODY, not the frontmatter", base + "note_kind: essay\n", pd),
    ("note: missing parent, page_dir given (control)", note(parent=""), pd),
    ("note: unresolved parent (control)", note(parent="parent: no/such/page.md"), pd),
]
print("== Part 1: adversarial pages")
for name, text, pdir in cases:
    v = D.judge(text, state, kind, word, dup, page_dir=pdir)
    print("%-62s -> %-16s %s" % (name, v[0], v[5]))

print("== Part 2: mutants of the rule; S must FAIL on each")
src = io.open(os.path.join(R, "documented_rule.py"), encoding="utf-8").read()
MUT = [
    ("U disabled (elif unknown never true)", "    elif unknown:\n", "    elif False:\n"),
    ("N disabled (note_gaps returns [])", "    m = re.search(r\"^note_kind:", "    return []\n    m = re.search(r\"^note_kind:"),
    ("N section check removed", "    gaps += [\"section:%s\"", "    gaps += [] and [\"section:%s\"" ),
    ("N tier-column check removed", "        gaps.append(\"evidence-table(no tier column)\")", "        pass"),
    ("N parent-resolution check removed", "        gaps.append(\"parent(unresolved)\")", "        pass"),
    ("N kind check removed", "    gaps = [] if m.group(1).lower() in NOTE_KINDS else [\"note_kind:%s\" % m.group(1)]", "    gaps = []"),
    ("U prefix test dropped (every unregistered id fails)", "if i not in state and i.split(\"-\")[0] in prefixes", "if i not in state"),
]
RUNNER = r'''
import sys, io
src = io.open(sys.argv[1], encoding="utf-8").read()
orig = sys.argv[2]
sys.argv = [orig, "02-Resource-And-Asset-Pipeline/PS2-Image-Data-Formats/chse-character-se-tables.md"]
g = {"__name__": "__main__", "__file__": orig}
try:
    exec(compile(src, orig, "exec"), g)
except SystemExit:
    pass
'''
work = os.path.join(HERE, "mut")
os.makedirs(work, exist_ok=True)
io.open(os.path.join(work, "runner.py"), "w", encoding="utf-8").write(RUNNER)
for name, a, b in MUT:
    if a not in src:
        print("%-52s ANCHOR-NOT-FOUND" % name); continue
    m = src.replace(a, b, 1)
    # the mutant lives in this work folder and is executed with __file__ = the original path, so DB resolves identically
    p = os.path.join(work, "mutant.py")
    io.open(p, "w", encoding="utf-8").write(m)
    out = subprocess.run([sys.executable, "-B", os.path.join(work, "runner.py"), p, os.path.join(R, "documented_rule.py")],
                         capture_output=True, text=True, timeout=600)
    line = next((l for l in (out.stdout + out.stderr).splitlines() if "S self-test" in l), "(no S line) " + out.stderr[-200:])
    print("%-52s %s" % (name, "CAUGHT (S FAIL)" if line.startswith("FAIL") else "NOT CAUGHT: " + line[:160]))
