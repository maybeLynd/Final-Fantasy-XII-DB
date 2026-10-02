"""apply.py [--apply] - consume FABLE's review of ASTRA's ov42-sequence-queue-source into FABLE's availability page
(FABLE, 2026-10-02). Runs after ../ov42-effective-id-consumption-fable-1002/apply.py in the same package.

The text is read from the reviewed draft (../fable-review-astra-ov42-sequence-queue-source-1002/consumption-draft.md)
and its "(page-relative link: `x`)" forms are restored to links. Edit 1 carries two OLD -> NEW pairs (before and after
the effective-id edit); whichever OLD is on the page is used. Edits 2-3 are OLD -> NEW pairs; Edit 4 is appended at the
page end. Dry run by default; prints FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
DB = os.path.normpath(os.path.join(CAND, "..", ".."))
AV = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
DRAFT = os.path.join(CAND, "fable-review-astra-ov42-sequence-queue-source-1002", "consumption-draft.md")
LAST_AV = "- Whole OV-42 stays OPEN."

def sections():
    d = io.open(DRAFT, encoding="utf-8").read().replace("\r\n", "\n")
    d = re.sub(r"(\[[^\]]*\]) \(page-relative link: `([^`]+)`\)", r"\1(\2)", d)
    out = {}
    for m in re.finditer(r"^## (Edit \d)[^\n]*\n(.*?)(?=^## |\Z)", d, re.S | re.M):
        out[m.group(1)] = re.findall(r"```\n(.*?)\n```", m.group(2), re.S)
    return out

def main():
    write = "--apply" in sys.argv
    S = sections()
    assert len(S["Edit 1"]) == 4 and len(S["Edit 2"]) == 2 and len(S["Edit 3"]) == 2 and len(S["Edit 4"]) == 1
    raw = io.open(AV, encoding="utf-8", newline="").read()
    crlf, t, fails = "\r\n" in raw, raw.replace("\r\n", "\n"), 0
    e1 = [(S["Edit 1"][0], S["Edit 1"][1]), (S["Edit 1"][2], S["Edit 1"][3])]
    if any(new in t for _, new in e1):
        print("ALREADY E1")
    else:
        hit = [(o, n) for o, n in e1 if t.count(o) == 1]
        if len(hit) != 1: print("MISS E1 (%d variants match)" % len(hit)); fails += 1
        else: t = t.replace(*hit[0]); print("WOULD PATCH" if not write else "PATCHED", "E1")
    for k in ("Edit 2", "Edit 3"):
        old, new = S[k]
        if new in t: print("ALREADY", k); continue
        if t.count(old) != 1: print("MISS %s (%d)" % (k, t.count(old))); fails += 1; continue
        t = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", k)
    sec = S["Edit 4"][0]
    if sec in t: print("ALREADY E4")
    elif not t.rstrip("\n").endswith(LAST_AV): print("MISS E4 (page end moved)"); fails += 1
    else: t = t.rstrip("\n") + "\n\n" + sec + "\n"; print("WOULD PATCH" if not write else "PATCHED", "E4")
    if write and not fails:
        io.open(AV, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)

main()
