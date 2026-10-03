"""test_recent_changes.py - Recent meaningful changes (improvement addendum section 2; DASHBOARD-MEANINGS 6.3;
SWE2-FRONTIER, 2026-10-03). Fixtures only.
  A1  no classifier output -> UNMEASURED, no counts (never zeros)
  A2  knowledge, activity and unclassified are separate counts per window; 24h is the subset of 7d by `at >= since`;
      no combined total
  A3  the adapter never classifies: an unknown class string is reported (PARTIAL); an event without a class is
      UNCLASSIFIED; an event without an axis takes the axis of its class
"""
import json, os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "analysis-kit", "gfz-scripts"))
import build_views as BV  # noqa: E402

fails = 0


def check(tag, ok, text=""):
    global fails
    print("%s  %s %s" % ("PASS" if ok else "FAIL", tag, text))
    fails += (not ok)


tmp = tempfile.mkdtemp(prefix="addendum-test-")
T = "2026-10-03T12:00:00Z"


def jfile(name, obj):
    p = os.path.join(tmp, name)
    json.dump(obj, open(p, "w", encoding="utf-8"))
    return p


# A1
r = BV.recent_changes_block({"recent_changes": os.path.join(tmp, "absent.json"), "recent_changes.py": ""})
check("A1 absent -> UNMEASURED", r["status"] == "UNMEASURED" and "windows" not in r, r.get("why"))
# A2 / A3
ev = [{"class": "NEW FF12 KNOWLEDGE", "axis": "knowledge", "at": "2026-10-03T10:00:00Z", "title": "k1"},
      {"class": "CORRECTED / FALSIFIED FF12 CLAIM", "at": "2026-09-30T10:00:00Z", "title": "k2 (7d only, no axis given)"},
      {"class": "WORKFLOW / COORDINATION", "axis": "activity", "at": "2026-10-03T11:00:00Z", "title": "w1"},
      {"class": "GENERATED / BOOKKEEPING ONLY", "at": "2026-10-03T11:30:00Z", "title": "g1"},
      {"class": "UNCLASSIFIED", "at": "2026-10-03T09:00:00Z", "title": "u1"},
      {"at": "2026-10-03T09:30:00Z", "title": "no class at all"},
      {"class": "SOMETHING NEW", "at": "2026-10-03T08:00:00Z", "title": "unknown class"}]
p = jfile("rc.json", {"version": "1", "generated_at": T, "source_commit": "abc", "events": ev,
                      "windows": {"24h": {"since": "2026-10-02T12:00:00Z"}, "7d": {"since": "2026-09-26T12:00:00Z"}}})
r = BV.recent_changes_block({"recent_changes": p, "recent_changes.py": ""})
w24, w7 = r["windows"]["24h"], r["windows"]["7d"]
check("A2 24h split", (w24["knowledge"], w24["activity"], w24["unclassified"]) == (1, 2, 3), w24)
check("A2 7d split", (w7["knowledge"], w7["activity"], w7["unclassified"]) == (2, 2, 3), w7)
check("A2 no combined total", not any(k in w24 for k in ("total", "score", "sum")))
check("A3 unknown class reported", r["status"] == "PARTIAL" and r["unknown_classes"] == ["SOMETHING NEW"], r["unknown_classes"])
check("A3 axis from class when omitted", [e[2] for e in r["knowledge_events"]] == ["k1", "k2 (7d only, no axis given)"])
check("A3 classes are the classifier's", {c for c, _n in w7["by_class"]} == {"NEW FF12 KNOWLEDGE", "CORRECTED / FALSIFIED FF12 CLAIM",
      "WORKFLOW / COORDINATION", "GENERATED / BOOKKEEPING ONLY", "UNCLASSIFIED", "SOMETHING NEW"}, w7["by_class"])



print("FAILS %d" % fails)
sys.exit(1 if fails else 0)
