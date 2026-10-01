"""Differential check: original vs patched team.validate on the live board copy and on mutants built to hit each
check the patch touches (duplicate id, unknown dependency, self dependency, 2- and 3-cycles) plus two it does not."""
import copy, importlib.util, json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, H / (name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


O, N = load("team_orig"), load("team_new")
board = json.loads((H / "TEAM.json").read_text(encoding="utf-8"))


def run(m, b):
    t = time.time()
    try:
        m.validate(b); r = "OK"
    except Exception as e:
        r = "%s: %s" % (type(e).__name__, e)
    return r, time.time() - t


def mut(f):
    b = copy.deepcopy(board); f(b["tasks"]); return b


T = board["tasks"]
i, j, k = 100, 200, 300
cases = {
    "live board": board,
    "duplicate id": mut(lambda ts: ts.append(copy.deepcopy(ts[i]))),
    "unknown dependency": mut(lambda ts: ts[i]["dependencies"].append("NO-SUCH-TASK-X")),
    "self dependency": mut(lambda ts: ts[i]["dependencies"].append(ts[i]["id"])),
    "2-cycle": mut(lambda ts: (ts[i]["dependencies"].append(ts[j]["id"]), ts[j]["dependencies"].append(ts[i]["id"]))),
    "3-cycle": mut(lambda ts: (ts[i]["dependencies"].append(ts[j]["id"]), ts[j]["dependencies"].append(ts[k]["id"]), ts[k]["dependencies"].append(ts[i]["id"]))),
    "valid chain": mut(lambda ts: (ts[i]["dependencies"].append(ts[j]["id"]), ts[j]["dependencies"].append(ts[k]["id"]))),
    "bad priority (untouched check)": mut(lambda ts: ts[i].__setitem__("priority", "P9")),
    "done without refs (untouched check)": mut(lambda ts: [t for t in ts if t["status"] == "DONE" and not t.get("retired")][0].__setitem__("result_refs", [])),
}
bad = 0
for name, b in cases.items():
    ro, to = run(O, copy.deepcopy(b)); rn, tn = run(N, copy.deepcopy(b))
    same = ro == rn
    bad += not same
    print("%-38s %s  orig %6.2fs  new %5.2fs  | %s" % (name, "SAME" if same else "DIFF", to, tn, rn[:90]))
    if not same:
        print("     orig:", ro[:200])
print("DIFFS", bad)
sys.exit(1 if bad else 0)
