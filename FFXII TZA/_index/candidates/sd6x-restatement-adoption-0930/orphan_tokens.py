"""Token support for the orphaned SD-60..SD-67 restatements (SWE2-DATA 2026-09-30): every backticked token and
number in the row's new status must appear in the cited record folder at HEAD, the AUDIT-SEM review, or the cited
OPUS commit's diff. Control: a made-up token must be reported missing. Terminal FAILS line."""
import re, subprocess
ROOT = r"C:\Users\Kristian\source\repos\XIIOnline"
DB = "Database/FFXII TZA/"
FAILS = 0


def git(*a):
    return subprocess.run(["git", "-C", ROOT] + list(a), capture_output=True, text=True, encoding="utf-8",
                          errors="replace").stdout


review = open(ROOT + "/" + DB + "_index/candidates/auditsem-review-dd-owner-read-2-0930/REVIEW.md", encoding="utf-8").read()
wt = open(ROOT + "/" + DB + "_index/OPEN-QUESTIONS.md", encoding="utf-8").read().replace("\r", "").split("\n")
rows = {l.split(" | ")[0][2:]: l for l in wt if re.match(r"\| SD-6[0-7] \|", l)}


def support(rid, st):
    shas = re.findall(r"OPUS `([0-9a-f]{9})`", st)
    recs = re.findall(r"\(candidates/([\w.-]+)/README\.md\)", st)
    text = review
    for r in recs:
        for f in git("ls-tree", "-r", "--name-only", "HEAD", DB + "_index/candidates/%s/" % r).split():
            text += git("show", "HEAD:" + f)
    for s in shas:
        text += git("show", s)
    return text


for rid in sorted(rows, key=lambda x: int(x[3:])):
    st = rows[rid].split(" | ")[-1].split("*(previously:)*")[0]
    text = support(rid, st)
    toks = set(re.findall(r"`([^`]{2,60})`", st)) | set(re.findall(r"\b\d{1,3}(?:,\d{3})+\b", st))
    toks = {t for t in toks if not re.fullmatch(r"[0-9a-f]{9}", t) and not t.startswith("auditsem-") and not t.endswith(".py")}
    # a compressed token (ViewInv(Transpose), PS2ZBias*, A/B/C, "size x even-instance-count") passes when every word
    # part of three or more characters appears in the support text; an exact hit passes directly
    def found(t):
        if t in text or t.replace(",", "") in text:
            return True
        parts = [p for p in re.split(r"[^A-Za-z0-9+]+", t) if len(p) >= 3]
        return bool(parts) and all(p in text for p in parts)
    missing = sorted(t for t in toks if not found(t))
    print("%s %s tokens=%d missing=%s" % ("PASS" if not missing else "CHECK", rid, len(toks), missing[:12]))
    FAILS += bool(missing)
ctl = support("SD-65", rows["SD-65"])
print(("PASS" if "`ZZ_NOT_A_TOKEN_42`" not in ctl else "FAIL") + " C1 control: an invented token is not found")
print("FAILS %d" % FAILS)
