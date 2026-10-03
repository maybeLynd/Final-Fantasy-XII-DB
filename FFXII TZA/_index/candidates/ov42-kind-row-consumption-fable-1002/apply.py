"""apply.py [--apply] - consume FABLE's review of ASTRA's ov42-kind-row-coherence into FABLE's availability page
(FABLE, 2026-10-02).

The text is read from the reviewed draft (../fable-review-astra-ov42-kind-row-coherence-1002/consumption-draft.md).
Edits 1-2 are OLD -> NEW pairs; Edit 3 is appended at the page end. In Edit 3 the packet and record paths, written as
plain text in the draft, become page-relative links in the page's usual style. Dry run by default; prints FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
DB = os.path.normpath(os.path.join(CAND, "..", ".."))
AV = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
DRAFT = os.path.join(CAND, "fable-review-astra-ov42-kind-row-coherence-1002", "consumption-draft.md")
LAST_AV = "- Whole OV-42 stays OPEN."
LINKS = [
    ("ASTRA's packet `ov42-kind-row-coherence` (`_experiments/evidence/ov42-kind-row-coherence/README.md`,\n`d83287255`;",
     "ASTRA's packet [`ov42-kind-row-coherence`](../../_experiments/evidence/ov42-kind-row-coherence/README.md)\n(`d83287255`;"),
    ("ACCEPT-WITH-NARROWING (record\n`_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md`, 75 checks",
     "ACCEPT-WITH-NARROWING\n([record](../../_index/candidates/fable-review-astra-ov42-kind-row-coherence-1002/REVIEW.md), 75 checks"),
]


def sections():
    d = io.open(DRAFT, encoding="utf-8").read().replace("\r\n", "\n")
    out = {}
    for m in re.finditer(r"^## (Edit \d)[^\n]*\n(.*?)(?=^## |\Z)", d, re.S | re.M):
        out[m.group(1)] = re.findall(r"```\n(.*?)\n```", m.group(2), re.S)
    return out


def main():
    write = "--apply" in sys.argv
    S = sections()
    assert len(S["Edit 1"]) == 2 and len(S["Edit 2"]) == 2 and len(S["Edit 3"]) == 1, {k: len(v) for k, v in S.items()}
    sec = S["Edit 3"][0]
    for old, new in LINKS:
        assert sec.count(old) == 1, old[:50]
        sec = sec.replace(old, new)
    raw = io.open(AV, encoding="utf-8", newline="").read()
    crlf, t, fails = "\r\n" in raw, raw.replace("\r\n", "\n"), 0
    for k in ("Edit 1", "Edit 2"):
        old, new = S[k]
        if new in t:
            print("ALREADY", k); continue
        if t.count(old) != 1:
            print("MISS %s (%d)" % (k, t.count(old))); fails += 1; continue
        t = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", k)
    if sec in t:
        print("ALREADY Edit 3")
    elif not t.rstrip("\n").endswith(LAST_AV):
        print("MISS Edit 3 (page end moved)"); fails += 1
    else:
        t = t.rstrip("\n") + "\n\n" + sec + "\n"; print("WOULD PATCH" if not write else "PATCHED", "Edit 3")
    if write and not fails:
        io.open(AV, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n") if crlf else t)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)


main()
