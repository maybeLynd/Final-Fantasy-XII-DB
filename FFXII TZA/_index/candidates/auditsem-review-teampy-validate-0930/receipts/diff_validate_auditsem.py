"""SWE2-AUDIT-SEM differential: team.validate at d20b7b69b^ (team_orig.py) vs d20b7b69b (team_new.py) on a FIXTURE copy
of the current board (TEAM.json in this folder, never the live path) and on mutants the producer's diff did not build.
Each case is run on a fresh deep copy for each version; outcome = 'OK' or '<ExceptionType>: <message>'."""
import copy, importlib.util, json, sys, time
from pathlib import Path
H = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, H / (name + ".py"))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


O, N = load("team_orig"), load("team_new")
board = json.loads((H / "TEAM.json").read_text(encoding="utf-8"))
print("fixture board revision", board.get("revision"), "tasks", len(board["tasks"]))


def run(m, b):
    t = time.time()
    try:
        m.validate(b); r = "OK"
    except Exception as e:
        r = "%s: %s" % (type(e).__name__, str(e)[:120])
    return r, time.time() - t


def mut(f):
    b = copy.deepcopy(board); f(b["tasks"]); return b


T = board["tasks"]
# pick tasks with no dependencies so the mutants are the only edges we add
free = [n for n, t in enumerate(T) if not t["dependencies"] and t["status"] != "ACTIVE"]
a, b_, c, d = free[10], free[20], free[30], free[40]


def dup_with_cycle(ts):
    x = copy.deepcopy(ts[a]); x["dependencies"] = [ts[b_]["id"]]
    ts[b_]["dependencies"].append(ts[a]["id"]); ts.append(x)


def forward_ref(ts):
    ts[a]["dependencies"].append(ts[-1]["id"])


def diamond(ts):
    for n in free[50:250]:
        ts[n]["dependencies"] += [ts[a]["id"], ts[b_]["id"]]
    ts[a]["dependencies"].append(ts[c]["id"]); ts[b_]["dependencies"].append(ts[c]["id"])


def chain(n):
    def f(ts):
        idx = free[300:300 + n]
        for p, q in zip(idx, idx[1:]):
            ts[p]["dependencies"].append(ts[q]["id"])
    return f


def cycle_in_done(ts):
    dn = [n for n, t in enumerate(ts) if t["status"] == "DONE" and not t["dependencies"]][:2]
    ts[dn[0]]["dependencies"].append(ts[dn[1]]["id"]); ts[dn[1]]["dependencies"].append(ts[dn[0]]["id"])


cases = {
    "fixture board": board,
    "duplicate id whose copies differ (one closes a cycle)": mut(dup_with_cycle),
    "forward reference to the last task": mut(forward_ref),
    "200-task diamond (valid)": mut(diamond),
    "non-string dependency (int)": mut(lambda ts: ts[a]["dependencies"].append(5)),
    "dependencies = None": mut(lambda ts: ts[a].__setitem__("dependencies", None)),
    "unhashable dependency (list)": mut(lambda ts: ts[a]["dependencies"].append(["X"])),
    "task without id": mut(lambda ts: ts[a].pop("id")),
    "unhashable id (list)": mut(lambda ts: ts[a].__setitem__("id", ["X"])),
    "2-cycle between DONE tasks": mut(cycle_in_done),
    "cycle through the appended duplicate only": mut(lambda ts: (ts.append(copy.deepcopy(ts[a])))),
    "chain of 400 (valid)": mut(chain(400)),
}
# recursion-depth boundary: find the longest valid chain each version accepts
bad = 0
for name, bb in cases.items():
    ro, to = run(O, copy.deepcopy(bb)); rn, tn = run(N, copy.deepcopy(bb))
    same = ro == rn
    bad += not same
    print("%-52s %s  orig %6.2fs new %5.2fs | %s" % (name, "SAME" if same else "DIFF", to, tn, rn))
    if not same:
        print("      orig:", ro)
lim = sys.getrecursionlimit()
for n in (lim - 60, lim - 40, lim - 20, lim - 10, lim - 5, lim - 2):
    bb = mut(chain(n))
    ro, _ = run(O, copy.deepcopy(bb)); rn, _ = run(N, copy.deepcopy(bb))
    print("chain %4d (recursion limit %d): orig %-14s new %-14s %s" % (n, lim, ro[:14], rn[:14], "SAME" if ro == rn else "DIFF (stack-depth boundary)"))
print("DIFFS (named cases)", bad)
sys.exit(1 if bad else 0)
