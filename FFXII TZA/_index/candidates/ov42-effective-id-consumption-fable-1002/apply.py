"""apply.py [--apply] - consume FABLE's review of ASTRA's ov42-effective-id-source into FABLE's availability page, and
correct the handler-table page's "both calls and is called by" sentence (FABLE, 2026-10-02).

The text is read from the reviewed draft (../fable-review-astra-ov42-effective-id-source-1002/consumption-draft.md),
so what is published is exactly the reviewed text; its "(page-relative link: `x`)" forms are restored to links.
Edits 1-3 are OLD -> NEW fence pairs, Edit 4 (one fence) is appended at the availability page's end, and the
"Noted for FABLE" section's OLD -> NEW pair goes to the handler table. Dry run by default; prints FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
DB = os.path.normpath(os.path.join(CAND, "..", ".."))
AV = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
HT = os.path.join(DB, "07-Combat-Action", "Action-Dispatch", "battle-action-handler-table.md")
DRAFT = os.path.join(CAND, "fable-review-astra-ov42-effective-id-source-1002", "consumption-draft.md")
LAST_AV = "- Whole OV-42 stays OPEN."

def sections():
    d = io.open(DRAFT, encoding="utf-8").read().replace("\r\n", "\n")
    d = re.sub(r"(\[[^\]]*\]) \(page-relative link: `([^`]+)`\)", r"\1(\2)", d)
    out = {}
    for m in re.finditer(r"^## ([^\n]*)\n(.*?)(?=^## |\Z)", d, re.S | re.M):
        out[m.group(1).split(":")[0].split(" (")[0].strip()] = re.findall(r"```\n(.*?)\n```", m.group(2), re.S)
    return out

def main():
    write = "--apply" in sys.argv
    S = sections()
    noted = [v for k, v in S.items() if k.startswith("Noted for FABLE")][0]
    assert all(len(S[k]) == 2 for k in ("Edit 1", "Edit 2", "Edit 3")) and len(S["Edit 4"]) == 1 and len(noted) == 2
    plan = [(AV, "E1", S["Edit 1"][0], S["Edit 1"][1]), (AV, "E2", S["Edit 2"][0], S["Edit 2"][1]),
            (AV, "E3", S["Edit 3"][0], S["Edit 3"][1]), (HT, "HT", noted[0], noted[1])]
    texts, crlf, fails = {}, {}, 0
    for p in (AV, HT):
        t = io.open(p, encoding="utf-8", newline="").read()
        crlf[p] = "\r\n" in t; texts[p] = t.replace("\r\n", "\n")
    for p, k, old, new in plan:
        t = texts[p]
        if new in t: print("ALREADY", k); continue
        if t.count(old) != 1: print("MISS %s (%d)" % (k, t.count(old))); fails += 1; continue
        texts[p] = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", k)
    sec, t = S["Edit 4"][0], texts[AV]
    if sec in t: print("ALREADY E4")
    elif not t.rstrip("\n").endswith(LAST_AV): print("MISS E4 (page end moved)"); fails += 1
    else: texts[AV] = t.rstrip("\n") + "\n\n" + sec + "\n"; print("WOULD PATCH" if not write else "PATCHED", "E4")
    if write and not fails:
        for p, t in texts.items():
            io.open(p, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf[p] else t)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)

main()
