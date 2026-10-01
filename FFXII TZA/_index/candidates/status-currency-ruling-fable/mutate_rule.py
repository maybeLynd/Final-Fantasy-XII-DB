# mutate_rule.py - mutation check of documented_rule.py's self-test S after the 2026-09-30 repair (FABLE). Each mutant removes
# one repaired or original check; S must FAIL for every one. Mutants run from a copy placed beside the original, so the
# DB-relative paths resolve the same way; the copy is removed afterwards.
import io, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = io.open(os.path.join(HERE, "documented_rule.py"), encoding="utf-8").read()
MUTANTS = [
    ("U disabled", "    unknown = sorted(set(i for i in re.findall(ID, after_fm)", "    unknown = [] and sorted(set(i for i in re.findall(ID, after_fm)"),
    # anchored on foreign_ids' own return (2026-09-29: evidence_status() now also ends "return out" before judge, and the
    # old anchor silently mutated that function instead - the mutant then survived)
    ("foreign registries empty", "    return out\n\n\nEVID = ", "    return set()\n\n\nEVID = "),
    ("front matter scanned", "    unknown = sorted(set(i for i in re.findall(ID, after_fm)", "    unknown = sorted(set(i for i in re.findall(ID, text)"),
    ("N disabled", "    m = re.search(r\"^note_kind:\\s*(\\S+)\", head, re.M)\n    if not m:\n        return []",
     "    m = re.search(r\"^note_kind:\\s*(\\S+)\", head, re.M)\n    if True:\n        return []"),
    ("parent resolution removed", "        if not (os.path.isfile(pp) and pp.lower().endswith(\".md\")):", "        if False:"),
    ("self-parent check removed", "        elif page_path is not None and os.path.normcase(os.path.abspath(pp)) == os.path.normcase(os.path.abspath(page_path)):",
     "        elif False:"),
    ("back-link check removed", "            if os.path.basename(page_path) not in ptxt:", "            if False:"),
    ("empty-section check removed", "        elif not any(any(l.strip() for l in s[2]) for s in hits):", "        elif False:"),
    ("tier data-row check removed", "            return any(l.strip().startswith(\"|\") and not re.match(r\"^\\|[\\s:|-]+\\|\\s*$\", l)\n                       for l in lines[k + 2:k + 3])",
     "            return True"),
    ("keyword anchoring removed", "NUM = r\"^(?:[0-9]+[.)]?\\s+|[0-9]+\\.[0-9]+\\s+)?\"", "NUM = r\"(?:[0-9]+[.)]?\\s+|[0-9]+\\.[0-9]+\\s+)?|.*\""),
    ("T disabled", "    elif untr:\n        v = \"EVIDENCE-UNTRACKED\"", "    elif False:\n        v = \"EVIDENCE-UNTRACKED\""),
    ("T extractor blind", "        if not ok and p not in bad:", "        if False:"),
    ("Evidence-section scoping removed", "        elif n == \"evidence\" and not any(tier_table_with_row(s[2]) for s in hits):",
     "        elif n == \"evidence\" and not any(tier_table_with_row(t[2]) for t in secs):"),
]
fails = 0
for name, old, new in MUTANTS:
    if old not in SRC:
        print("NOANCHOR  %s" % name); fails += 1; continue
    if SRC.count(old) != 1:   # an ambiguous anchor mutates whichever match comes first (2026-09-29: it hit the wrong function)
        print("AMBIGUOUS %s (%d matches)" % (name, SRC.count(old))); fails += 1; continue
    path = os.path.join(HERE, "_mutant_rule.py")
    io.open(path, "w", encoding="utf-8").write(SRC.replace(old, new, 1))
    try:
        r = subprocess.run([sys.executable, path, "no-such-page.md"], capture_output=True, text=True, cwd=HERE)
    finally:
        os.remove(path)
    s_line = next((l for l in r.stdout.splitlines() if " S self-test" in l), r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "?")
    # caught = S does not PASS: an explicit FAIL, a failed assertion, or a crash before S reports (the defect surfaces)
    caught = not s_line.startswith("PASS")
    fails += not caught
    print("%-8s %s" % ("CAUGHT" if caught else "SURVIVES", name))
print("FAILS", fails)
