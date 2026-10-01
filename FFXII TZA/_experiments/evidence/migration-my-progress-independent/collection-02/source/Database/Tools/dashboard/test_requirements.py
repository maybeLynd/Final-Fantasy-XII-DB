"""test_requirements.py - My Progress (MP-1) requirement accounting (OPUS, 2026-09-29). Fixtures only; no live claims.

  MP1  one accepted closure: a PARTIAL row becomes ANSWERED -> accepted +1, scope unchanged, change shows +1
  MP2  one reopened requirement: an ANSWERED row reopens -> accepted -1; it is listed with the board's owner and next action
  MP3  one transfer (collect over a fixture database): NOT A QUESTION onto a carrier stays remaining while the carrier is
       open and is accepted only when the carrier is DONE
  MP4  overlap deduplication: a box naming a live row is not a second requirement; a repeated key counts once; a
       requirement shared by two categories appears in both rows and once in the union
  MP5  incomplete scope: a family that cannot be read -> overall UNMEASURED (known requirements only), NOT READY with reason
  MP6  stale / missing data: a missing reporter snapshot fails the adapter (FAILED view, never zeros); a moved strict
       input marks the served progress view STALE; no prior checkpoint -> no change claimed
  MP7  all L2 cells MET with residual work open under an L2 system page -> L2 below 100 %, NOT READY even if the gate says MET
  MP8  the server refuses a progress block that disagrees with its measures or claims READY while anything remains;
       progress is the first required view and the page opens on it; the page never rounds up to 100 %
  MP9  excluded rows (withdrawn, struck) are listed and never enter a denominator; a definition change is not compared
  MP10 terminal passes: 30 accepted only when the gate's acceptance check is OK
"""
import copy, io, json, os, shutil, sys, tempfile, threading, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, "..", "analysis-kit", "gfz-scripts"))
import requirements as R  # noqa: E402
import build_views as BV  # noqa: E402
import server as S  # noqa: E402
import generation as G  # noqa: E402

fails = 0
def check(tag, ok, text=""):
    global fails
    fails += not ok; print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))

T = tempfile.mkdtemp(prefix="mp1_")
MAP = os.path.join(HERE, "..", "..", "FFXII TZA", "_index", "workflow", "my-progress", "category-map.tsv")
cmap = R.load_map(MAP)
SUBS = os.path.join(T, "subs.tsv")
open(SUBS, "w", encoding="utf-8").write("id\tcategory\tsubsystem\ttier\tprimary_pages\tcontracts\tnote\n"
                                        "S-01\t03 World\tfixture system\tcore\t../03-World-Area-Field/x.md\t\t\n")
def reporter(cells="MET"):
    return {"commit_id": "fixture", "levels": {"L2_reconstruction_grade": {"systems": [
        {"system": "S-01", "contract": cells, "types": "MET", "relationships": "MET", "runtime": "MET", "script_data": "N/A"}],
        "per_dimension_live_unruled": {}}, "terminal_certification": {"required_consecutive": 30, "final_audits_declared": 0}}}
GATE_NOT = {"verdict": "NOT_MET", "remaining": "questions outstanding", "detail": ["acceptance: UNMET -- no receipt"]}
GATE_MET = {"verdict": "MET", "remaining": None, "detail": ["acceptance: OK -- terminal receipt at abc covers HEAD"]}
def fact(k, f, ok, doc=None, h=None, st="x"):
    return {"k": k, "f": f, "ok": ok, "st": st, "doc": doc, "h": h if h is not None else ([["folder", doc.split("/")[0][:2]]] if doc else []),
            "o": "", "e": "fixture", "n": ""}
BOARD = {"tasks": [{"id": "FIX-REQ-X-1", "status": "READY", "assigned_to": "SWE2-DATA", "title": "answer X-1"}]}
base = [fact("Q:X-1", "Q", False, "03-World-Area-Field/x.md", st="PARTIAL"), fact("Q:X-9", "Q", True, "18-Audio/a.md", st="ANSWERED"),
        fact("F:00400000", "F", True, h=[["folder", "18"]], st="A")]
doc = lambda fs, failed=None: {"version": R.VERSION, "facts": fs, "failed": failed or {}, "excluded": []}
def snap(r):
    return {"version": r["version"], "generation": "gPRIOR", "committed_at": "2026-09-28T23:00:00Z", "scopes": r["scopes"],
            "categories": r["categories"]}

# MP1 - accepted closure
r0 = R.measure(doc(base), cmap, BOARD, reporter(), GATE_NOT, SUBS)
closed = copy.deepcopy(base); closed[0]["ok"] = True; closed[0]["st"] = "ANSWERED"
r1 = R.measure(doc(closed), cmap, BOARD, reporter(), GATE_NOT, SUBS, prior=snap(r0))
c = r1["change"]["scopes"]["union"]
check("MP1", c["accepted"] == 1 and c["scope"] == 0 and r1["scopes"]["union"]["accepted"] == r0["scopes"]["union"]["accepted"] + 1,
      "closure: accepted %+d, scope %+d" % (c["accepted"], c["scope"]))
# MP2 - reopened
r2 = R.measure(doc(base), cmap, BOARD, reporter(), GATE_NOT, SUBS, prior=snap(r1))
rw = [f for f in r2["remaining"]["W"] if f["k"] == "Q:X-1"]
check("MP2", r2["change"]["scopes"]["union"]["accepted"] == -1 and r2["change"]["categories"]["W"]["accepted"] == -1
      and rw and rw[0]["o"] == "SWE2-DATA" and rw[0]["n"].startswith("FIX-REQ-X-1"),
      "reopen: accepted -1; listed with owner %s, next %r" % (rw[0]["o"] if rw else None, rw[0]["n"][:30] if rw else None))

# MP3 - transfer, through collect() over a fixture database
db = os.path.join(T, "db"); os.makedirs(os.path.join(db, "_index", "_inbox")); os.makedirs(os.path.join(db, "_index", "candidates", "register-triage"))
os.makedirs(os.path.join(db, "03-World-Area-Field")); os.makedirs(os.path.join(db, "18-Audio"))
open(os.path.join(db, "_index", "OPEN-QUESTIONS.md"), "w", encoding="utf-8").write(
    "# Open questions\n\n## X. Fixture\n\n| ID | Question | Status |\n|---|---|---|\n"
    "| X-1 | first [page](../03-World-Area-Field/x.md) | **PARTIAL** - half |\n"
    "| X-2 | second | **OPEN** |\n"
    "| X-3 | third | **NOT A QUESTION 2026-09-26** - carried by the carrier |\n"
    "| X-4 | fourth | **WITHDRAWN** - malformed |\n"
    "| ~~X-5~~ | fifth | **CLOSED** |\n"
    "| X-6 | sixth [page](../18-Audio/a.md) | **ANSWERED** - yes |\n")
open(os.path.join(db, R_BATCH := "_index/candidates/register-triage/batch-K-scope-rulings.md"), "w", encoding="utf-8").write(
    "# batch K\n\n## Class 2: NOT A QUESTION, with a carrier (1)\n\n| row | carrier |\n|---|---|\n| X-3 | `FIX-CARRIER-0001` |\n")
open(os.path.join(db, "03-World-Area-Field", "x.md"), "w", encoding="utf-8").write(
    "---\nstatus: PARTIAL\n---\n# x\n\n- [ ] **X-1.** still half open\n- [ ] a box that names no register row\n- [x] **X-6.** done\n")
open(os.path.join(db, "18-Audio", "a.md"), "w", encoding="utf-8").write(
    "---\nstatus: DOCUMENTED\n---\n# a\n\nThe body at `00400010` does it.\n")
FN = os.path.join(T, "functions.tsv")
open(FN, "w", encoding="utf-8").write("entry\tname\tbody_bytes\towner\tfinal_no_owner\tthunk\tnoreturn\tcomment_len\ttags\n"
                                      "00400000\tFUN_00400000\t64\tAudio\tfalse\tfalse\tfalse\t0\t\n"
                                      "00400100\tFUN_00400100\t64\t\tfalse\tfalse\tfalse\t0\tGFZ.V1.CodeDomain.NativeRoutine.Fixture\n")
bp = os.path.join(db, "_index", "_inbox", "TEAM.json")
def board(status):
    json.dump({"tasks": [{"id": "FIX-CARRIER-0001", "status": status, "assigned_to": "SWE2-X"}]}, open(bp, "w", encoding="utf-8"))
board("READY"); f_open = R.collect(db, functions_path=FN, board_path=bp)
board("DONE"); f_done = R.collect(db, functions_path=FN, board_path=bp)
q = lambda d, k: next((f for f in d["facts"] if f["k"] == k), None)
check("MP3", q(f_open, "Q:X-3") and not q(f_open, "Q:X-3")["ok"] and "carrier open" in q(f_open, "Q:X-3")["st"] and q(f_done, "Q:X-3")["ok"],
      "open carrier: %r; DONE carrier: accepted" % (q(f_open, "Q:X-3") or {}).get("st"))

# MP4 - overlap
P = [f for f in f_open["facts"] if f["f"] == "P"]
dup = base + [fact("Q:X-1", "Q", False, "03-World-Area-Field/x.md")]
shared = base + [fact("Q:X-7", "Q", False, "04-Actor-Entity/y.md")]
r4a = R.measure(doc(dup), cmap, BOARD, reporter(), GATE_NOT, SUBS); r4b = R.measure(doc(shared), cmap, BOARD, reporter(), GATE_NOT, SUBS)
check("MP4", len(P) == 1 and "no register id" in P[0]["st"] and r4a["duplicates_merged"] == 1 and r4a["scopes"]["union"] == r0["scopes"]["union"]
      and any(f["k"] == "Q:X-7" for f in r4b["remaining"]["E"]) and any(f["k"] == "Q:X-7" for f in r4b["remaining"]["P"])
      and r4b["scopes"]["union"]["total"] == r0["scopes"]["union"]["total"] + 1,
      "box naming live X-1 not counted; page residue %d; duplicate key merged; shared 04 row in E and P, union +1" % len(P))

# MP5 - incomplete scope (the fixture database has no registry doc, no contradiction ledger)
r5 = R.measure(f_open, cmap, BOARD, reporter(), GATE_MET, SUBS)
check("MP5", not r5["measured"] and {"R", "K"} <= set(r5["failed"]) and not r5["ready"] and "not fully enumerated" in r5["why_not_ready"] and "R: reader failed" in r5["why_not_ready"],
      "failed families %s; NOT READY: %s" % (sorted(r5["failed"]), r5["why_not_ready"][:70]))

# MP6 - stale / missing
inp = {"requirement_facts": os.path.join(T, "facts.json"), "category_map": MAP, "team": os.path.join(T, "team.json"),
       "progress_snapshot": os.path.join(T, "nope.json"), "goal_gate": os.path.join(T, "gate.json"), "subsystems": SUBS}
json.dump(doc(base), open(inp["requirement_facts"], "w")); json.dump(BOARD, open(inp["team"], "w")); json.dump(GATE_NOT, open(inp["goal_gate"], "w"))
try:
    BV.v_progress(inp, "2026-09-29T00:00:00Z"); raised = False
except (OSError, ValueError):
    raised = True
json.dump(reporter(), open(os.path.join(T, "rep.json"), "w")); inp["progress_snapshot"] = os.path.join(T, "rep.json")
v6 = BV.v_progress(inp, "2026-09-29T00:00:00Z")
st = G.Store(os.path.join(T, "gens")); src = os.path.join(T, "src.txt"); open(src, "w").write("1")
b = st.begin({"src": {"path": src}}, {"name": "fixture"}); json.dump(v6, open(b.output_path("view-progress.json"), "w")); st.commit(b, ["view-progress.json"])
srv = S.serve(st.root, 0); port = srv.server_address[1]; threading.Thread(target=srv.serve_forever, daemon=True).start()
J = lambda p: json.loads(urllib.request.urlopen("http://127.0.0.1:%d%s" % (port, p), timeout=10).read())
s_ok = J("/api/status")["views"]["progress"]; open(src, "w").write("2"); s_st = J("/api/status")["views"]["progress"]
check("MP6", raised and v6["progress"]["change"] is None and s_ok == "OK" and s_st == "STALE",
      "missing reporter -> adapter raises (FAILED view); no prior -> no change; served %s then %s after a strict input moved" % (s_ok, s_st))

# MP7 - all L2 MET, residual open under the system page
r7 = R.measure(doc(base), cmap, BOARD, reporter("MET"), GATE_MET, SUBS)
l2cells = r7["families"]["L2"]
check("MP7", l2cells["accepted"] == l2cells["total"] and r7["scopes"]["L2"]["accepted"] < r7["scopes"]["L2"]["total"] and not r7["ready"]
      and any(f["k"] == "Q:X-1" and "L2" in f["lv"] for f in r7["remaining"]["W"]),
      "L2 cells %d/%d MET, L2 scope %d/%d, gate MET but NOT READY: %s" % (l2cells["accepted"], l2cells["total"], r7["scopes"]["L2"]["accepted"],
                                                                         r7["scopes"]["L2"]["total"], r7["why_not_ready"]))

# MP8 - server refusals, first tab, rounding
bad = copy.deepcopy(v6); bad["progress"]["scopes"]["union"]["accepted"] += 1
ready = copy.deepcopy(v6); ready["progress"]["reconstruction"]["state"] = "DATABASE READY - awaiting user authorization"
page = S.PAGE
check("MP8", S.check_view(v6, S.load_vocabulary()) is None and "disagrees" in (S.check_view(bad, S.load_vocabulary()) or "")
      and "READY" in (S.check_view(ready, S.load_vocabulary()) or "") and S.REQUIRED[0] == "progress"
      and 'let cur="progress"' in page and "if(n<d&&a>=100)a=99.9" in page and "My Progress" in page,
      "disagreeing block and false READY -> MALFORMED; progress first and default; no rounding to 100%")

# MP9 - exclusions and definition changes
ex = dict(f_open["excluded"])
old = snap(r0); old["version"] = "MP-0"
r9 = R.measure(doc(base), cmap, BOARD, reporter(), GATE_NOT, SUBS, prior=old)
check("MP9", ex.get("Q:X-5", "").startswith("struck") and "withdrawn" in ex.get("Q:X-4", "") and not q(f_open, "Q:X-4") and not q(f_open, "Q:X-5")
      and r9["change"]["comparable"] is False, "excluded %s; MP-0 prior -> %s" % (sorted(ex), r9["change"]["why"]))

# MP10 - terminal passes
t_not = R.terminal_facts(GATE_NOT, reporter()); t_met = R.terminal_facts(GATE_MET, reporter())
check("MP10", t_not[1] == 0 and t_met[1] == 30 and t_met[2] == 30, "gate acceptance UNMET -> 0/30; OK -> 30/30")

# MP11 (MP-2, FABLE C4) - a declared gap (a bucket whose member formats are not declared) keeps the overall figure UNMEASURED,
# names the gap and its repair, and the known subset is still reported
g = doc(base); g["gaps"] = {"X": "member formats of .bin are not declared - repair: OPUS-REQ-DATA-BUCKET-MEMBER-FORMATS"}
r11 = R.measure(g, cmap, BOARD, reporter(), GATE_MET, SUBS)
check("MP11", not r11["measured"] and not r11["ready"] and "member formats of .bin" in r11["why_not_ready"] and r11["scopes"]["union"]["total"] == r0["scopes"]["union"]["total"],
      "gap -> UNMEASURED, NOT READY: %s" % r11["why_not_ready"][:90])
# MP12 (MP-2, FABLE C2/C1) - answered and dispositioned are separate accepted counts; the union without F is its own scope
qd = base + [fact("Q:X-8", "Q", True, "03-World-Area-Field/x.md", st="SUPERSEDED (accepted disposition; runtime remainder not queued)")]
r12 = R.measure(doc(qd), cmap, BOARD, reporter(), GATE_NOT, SUBS)
check("MP12", r12["q_split"]["answered"] == 1 and r12["q_split"]["dispositioned"] == 1 and r12["q_split"]["remaining"] == 1
      and r12["scopes"]["union_exF"]["total"] == r12["scopes"]["union"]["total"] - r12["families"]["F"]["total"],
      "q split %s; union without F %s" % (r12["q_split"], r12["scopes"]["union_exF"]))

srv.shutdown(); shutil.rmtree(T, ignore_errors=True)
print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
