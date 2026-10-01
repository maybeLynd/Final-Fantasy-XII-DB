"""Real-Git controls for source_lookup (no mocks). Positive: the candidate's HEAD 5a2435b23 blobs, checked against an
independent `git cat-file blob` digest. Failure: a missing -C directory (the exact case ASTRA reproduced, exits 128),
a path absent at the revision, an unknown revision, and a missing recorded hash - each must come back ok=False /
INCOMPLETE with the exits kept, never SHA256(b"") and never equal=True/False."""
import hashlib, os, subprocess, sys, tempfile
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import source_lookup as S

REPO = r"C:\Users\Kristian\source\repos\XIIOnline"
REV = "5a2435b23231c2a3e340b3fda32c70df6903965c"
EMPTY = hashlib.sha256(b"").hexdigest()
fails = []


def check(name, cond, detail=""):
    print("%s  %s %s" % ("PASS" if cond else "FAIL", name, detail))
    if not cond:
        fails.append(name)


# P1 positive: raw blob digest equals an independent cat-file read; commit is 40-hex
rel = "Database/Tools/dashboard/build_views.py"
indep = hashlib.sha256(subprocess.run(["git", "-C", REPO, "cat-file", "blob", "%s:%s" % (REV, rel)], capture_output=True, check=True).stdout).hexdigest()
r = S.lookup(REPO, rel, REV)
check("P1 positive lookup", r["ok"] and r["blob_sha256"] == indep and len(r["last_commit"]) == 40 and all(c["exit"] == 0 for c in r["calls"]),
      "%s %s" % (r["blob_sha256"][:12] if r["blob_sha256"] else None, r["last_commit"]))
# P2 bind raw form (the manifest's recorded build_views hash)
b = S.bind(REPO, rel, "820648358a3864643101a92cfd0169952ecaffb7c783953cdc010d263815c790", REV)
check("P2 bind raw blob", b["equal"] is True and b["state"] == "BOUND (raw blob)", b["state"])
# P3 bind checkout form (uc1_band: the manifest recorded the CRLF checkout bytes)
b = S.bind(REPO, "Database/Tools/analysis-kit/gfz-scripts/uc1_band.py", "746b6fabbee735e74b33a052da9088de8680743407ed601605100d2d8bdac86b", REV)
check("P3 bind checkout form", b["equal"] is True and b["state"].startswith("BOUND (checkout"), b["state"])
# P4 a real mismatch stays a mismatch (not incomplete, not bound)
b = S.bind(REPO, rel, "0" * 64, REV)
check("P4 mismatch", b["ok"] and b["equal"] is False and b["state"] == "MISMATCH", b["state"])
# F1 missing -C directory: ASTRA's reproduced case
missing = os.path.join(tempfile.gettempdir(), "no-such-repo-a23-%d" % os.getpid())
assert not os.path.exists(missing)
r = S.lookup(missing, rel, REV)
b = S.bind(missing, rel, EMPTY, REV)
check("F1 missing repo dir", (not r["ok"]) and r["blob_sha256"] is None and r["last_commit"] is None
      and all(c["exit"] not in (0, None) for c in r["calls"]) and b["equal"] is None and b["state"] == "INCOMPLETE",
      "exits %s; bind(EMPTY) -> %s" % ([c["exit"] for c in r["calls"]], b["state"]))
# F2 path absent at the revision
r = S.lookup(REPO, "Database/Tools/dashboard/no_such_file.py", REV)
check("F2 absent path", not r["ok"] and r["blob_sha256"] is None and r["calls"][0]["exit"] != 0, (r["why"] or "")[:80])
# F3 unknown revision
r = S.lookup(REPO, rel, "0" * 40)
check("F3 unknown revision", not r["ok"] and r["blob_sha256"] is None, (r["why"] or "")[:80])
# F4 no recorded hash is not a match
b = S.bind(REPO, rel, None, REV)
check("F4 missing recorded hash", b["equal"] is None and b["state"].startswith("INCOMPLETE"), b["state"])
# F5 the empty-stdout digest can never be returned for a failed lookup
check("F5 no empty digest on failure", S.lookup(missing, rel, REV)["blob_sha256"] != EMPTY)
print("FAILS", len(fails))
sys.exit(1 if fails else 0)
