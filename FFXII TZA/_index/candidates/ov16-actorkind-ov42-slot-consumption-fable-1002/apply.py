"""apply.py [--apply] - consume FABLE's reviews of ASTRA's actor-directory-kind-proof (OV-16) and ov42-slot-id-producer
(OV-42) into FABLE's pages (FABLE, 2026-10-02).

The edit text is read from the two reviewed drafts (consumption-draft.md in each review folder), so what is published is
exactly the reviewed text; the drafts' "(page-relative link: `x`)" forms are restored to links. OLD -> NEW pairs are the
first two fenced blocks of each "## Edit N" section; the slot draft's Edit 3 (one fence) is appended at the page end.
Dry run by default; prints FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
DB = os.path.normpath(os.path.join(CAND, "..", ".."))
OV16 = os.path.join(CAND, "ov16-motion-functions-fable-0930", "README.md")
AV = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
D_KIND = os.path.join(CAND, "fable-review-astra-actor-directory-kind-proof-1002", "consumption-draft.md")
D_SLOT = os.path.join(CAND, "fable-review-astra-ov42-slot-id-producer-1002", "consumption-draft.md")
LAST_AV = "- Whole OV-42 stays OPEN."

def edits_of(draft):
    d = io.open(draft, encoding="utf-8").read().replace("\r\n", "\n")
    d = re.sub(r"(\[[^\]]*\]) \(page-relative link: `([^`]+)`\)", r"\1(\2)", d)
    out = {}
    for m in re.finditer(r"^## (Edit \d)[^\n]*\n(.*?)(?=^## |\Z)", d, re.S | re.M):
        out[m.group(1)] = re.findall(r"```\n(.*?)\n```", m.group(2), re.S)
    return out

def main():
    write = "--apply" in sys.argv
    K, S = edits_of(D_KIND), edits_of(D_SLOT)
    assert len(K["Edit 1"]) == 2 and len(K["Edit 2"]) == 2 and len(S["Edit 1"]) == 2 and len(S["Edit 2"]) == 2
    assert len(S["Edit 3"]) == 1
    plan = [(OV16, "kind E1", K["Edit 1"][0], K["Edit 1"][1]),
            (OV16, "kind E2", K["Edit 2"][0], K["Edit 2"][1]),
            (AV, "slot E1", S["Edit 1"][0], S["Edit 1"][1]),
            (AV, "slot E2", S["Edit 2"][0], S["Edit 2"][1])]
    texts, crlf, fails = {}, {}, 0
    for p in (OV16, AV):
        t = io.open(p, encoding="utf-8", newline="").read()
        crlf[p] = "\r\n" in t; texts[p] = t.replace("\r\n", "\n")
    for p, k, old, new in plan:
        t = texts[p]
        if new in t: print("ALREADY", k); continue
        if t.count(old) != 1: print("MISS %s (%d)" % (k, t.count(old))); fails += 1; continue
        texts[p] = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", k)
    sec = S["Edit 3"][0]
    t = texts[AV]
    if sec in t:
        print("ALREADY slot E3")
    elif not t.rstrip("\n").endswith(LAST_AV):
        print("MISS slot E3 (page no longer ends with the queue-reader limits)"); fails += 1
    else:
        texts[AV] = t.rstrip("\n") + "\n\n" + sec + "\n"; print("WOULD PATCH" if not write else "PATCHED", "slot E3")
    if write and not fails:
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf[p] else t)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)

main()
