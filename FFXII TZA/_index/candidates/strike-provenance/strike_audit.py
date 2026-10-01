# strike_audit.py (FABLE, Claude Opus 5.5, 2026-09-26) - for each FABLE commit today, every ~~struck~~ span in an added line must occur (whitespace-normalised)
# in the commit's removed lines of the same file, or in the file at some earlier revision (git log -S on its longest
# plain run); print the ones that do not (candidate invented or paraphrased history).
import re, subprocess
ROOT = str(__import__("pathlib").Path(__file__).resolve().parents[5])
def git(*a): return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
commits = [l.split()[0] for l in git("log", "--since=2026-09-26 00:00", "--author=Kristian", "--format=%h %s").splitlines() if " FABLE" in l]
norm = lambda s: re.sub(r"\s+", " ", s).strip()
bad = 0
for c in commits:
    diff = git("show", "--format=", "-U0", c)
    for fd in re.split(r"^diff --git ", diff, flags=re.M)[1:]:
        added = "\n".join(l[1:] for l in fd.splitlines() if l.startswith("+") and not l.startswith("+++"))
        removed = norm(" ".join(l[1:] for l in fd.splitlines() if l.startswith("-") and not l.startswith("---")))
        for m in re.finditer(r"~~(.+?)~~", added, re.S):
            s = norm(m.group(1))
            if len(s) > 8 and s not in removed and norm(s.replace("**", "")) not in removed.replace("**", ""):
                # not removed by this commit: accept it if the file said it at any earlier revision (a re-quote of older
                # history, e.g. a strike made verbatim later); probe with its longest plain run of words
                path = fd.split(" b/")[0][2:].strip()
                probe = max(re.split(r"[`*\[\]()]", s), key=len).strip()[:60]
                if probe and git("log", "--format=%h", "-S", probe, c + "~1", "--", path).strip():
                    continue
                bad += 1
                print(c, fd.split(" b/")[0][:70], "| STRUCK NOT IN REMOVED:", s[:120])
print("commits %d, suspicious strikes %d" % (len(commits), bad))
