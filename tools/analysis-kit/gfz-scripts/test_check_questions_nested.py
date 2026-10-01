"""test_check_questions_nested.py - a fixture database nested inside the database is not part of it (OPUS, 2026-09-29).

  N1  a real page's unticked box whose id has an OPEN row: the ledger is consistent (exit 0), the box is read
  N2  a nested fixture database (its own _index/OPEN-QUESTIONS.md) citing ids with no row HERE: still consistent, and
      read_boxes returns none of its boxes (the 2026-09-29 gate UNMET on W-902 / W-903)
  N3  the same orphan citation in a real page (no nested _index): the checker still refuses it - the prune is by the
      nested database's own register, never by folder name, so the safeguard is not weakened
"""
import os, shutil, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_questions as CQ  # noqa: E402
fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
T = tempfile.mkdtemp(prefix="cqn_")
HEAD = "| id | question | status |\n|---|---|---|\n"
def write(rel, text):
    p = os.path.join(T, rel); os.makedirs(os.path.dirname(p), exist_ok=True); open(p, "w", encoding="utf-8").write(text)
write("_index/OPEN-QUESTIONS.md", "# Open questions\n\n" + HEAD + "| UQ-1 | a real question [page](../04-A/p.md) | **OPEN** - live |\n")
write("04-A/p.md", "# page\n\n- [ ] **UQ-1.** a real question\n")
def run():
    r = subprocess.run([sys.executable, os.path.join(HERE, "check_questions.py"), "--db", T], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr
rc1, o1 = run()
check("N1", rc1 == 0 and any("UQ-1" in b[3] for b in CQ.read_boxes(T)), o1.strip().splitlines()[-1] if o1.strip() else "")
fx = "_experiments/evidence/x/fixture-db/"
write(fx + "_index/OPEN-QUESTIONS.md", "# fixture\n\n" + HEAD + "| W-902 | fixture [page](../04-A/f.md) | **OPEN** - fixture |\n")
write(fx + "04-A/f.md", "# fixture page\n\n- [ ] **W-902.** fixture box\n- [ ] **W-903.** fixture box\n")
rc2, o2 = run()
nested = [b for b in CQ.read_boxes(T) if "fixture-db" in b[0]]
check("N2", rc2 == 0 and not nested and "W-902" not in o2, "exit %d; nested boxes read %d" % (rc2, len(nested)))
shutil.rmtree(os.path.join(T, "_experiments"))
write("04-A/q.md", "# page two\n\n- [ ] **W-902.** an orphan in a real page\n")
rc3, o3 = run()
check("N3", rc3 != 0 and "W-902" in o3, "exit %d" % rc3)
shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
