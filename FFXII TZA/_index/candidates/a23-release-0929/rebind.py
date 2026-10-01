"""Re-bind the A23 candidate's recorded source hashes with the checked lookup (no recapture, no export).
Reads the published release-result.json, takes each recorded hash (manifest inputs, verifier, server.py on disk at the
run) and binds it at the run's HEAD 5a2435b23 (the only commit between the run's start 21:37:17Z and the next commit
b51b50668 at 21:43:02Z). Writes rebind-result.json beside itself; prints one line per component."""
import json, os, sys
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, H)
import source_lookup as S
REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
REV = "5a2435b23231c2a3e340b3fda32c70df6903965c"
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(H, "release-result.json")
old = json.load(open(src, encoding="utf-8"))["result"]["source_binding"]
paths = {"build_views.py": "Database/Tools/dashboard/build_views.py",
         "requirements.py": "Database/Tools/dashboard/requirements.py",
         "uc1_band.py": "Database/Tools/analysis-kit/gfz-scripts/uc1_band.py",
         "verifier(generation.py)": "Database/Tools/analysis-kit/gfz-scripts/generation.py",
         "server.py": "Database/Tools/dashboard/server.py"}
out = {"rev": REV, "source": os.path.basename(src), "components": {}}
for name, rel in paths.items():
    recorded = old[name].get("manifest", old[name].get("worktree"))
    b = S.bind(REPO, rel, recorded, REV)
    out["components"][name] = b
    print("%-24s %-38s commit %s" % (name, b["state"], (b["last_commit"] or "-")[:9]))
out["all_bound"] = all(c["equal"] is True for c in out["components"].values())
print("all_bound", out["all_bound"])
json.dump(out, open(os.path.join(H, "rebind-result.json"), "w", encoding="utf-8"), indent=1)
