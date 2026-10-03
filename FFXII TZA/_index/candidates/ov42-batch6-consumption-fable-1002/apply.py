"""apply.py [--apply] - consume FABLE's reviews of six ASTRA OV-42 packets in one package (FABLE, 2026-10-02).

Every edit's text is read from the reviewed drafts (../fable-review-astra-<packet>-1002/consumption-draft.md), in this
order (the caller-row draft's own ordering rule, with the quotient-bound subsection kept for the latch, guard, row
and bound):
  1. caller-row Edits 1-3: OLD -> NEW on the availability page;
  2. appended at the availability page's end: quotient-bound; caller-row (its first bullet replaced by the draft's
     one-sentence form, as that draft directs when both are applied); terminal-helper; interpreter-transfer;
     action-binding; mode17;
  3. mode17 Edit 2: OLD -> NEW on console slice A (FABLE-led).
In appended text, plain packet and record paths become page-relative links. Dry run by default; FAILS N last."""
import io, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
CAND = os.path.dirname(HERE)
DB = os.path.normpath(os.path.join(CAND, "..", ".."))
AV = os.path.join(DB, "07-Combat-Action", "Action-Availability", "battle-command-availability-and-reason-codes.md")
CA = os.path.join(DB, "00-Engine-Core-Runtime", "Developer-Tuning-Console", "arm-catalogue-slice-A-ids-12-43.md")
R = lambda p: "fable-review-astra-ov42-%s-1002" % p
PKT = re.compile(r"ASTRA's packet `(?P<slug>[^`]+)` \(`_experiments/evidence/(?P=slug)/README\.md`,(?P<ws>\s+)`(?P<sha>[0-9a-f]+)`")
EVI = re.compile(r"(?<!\()`_experiments/evidence/(?P<slug>[^`/]+)/README\.md`")
REC = re.compile(r" \(record(?P<ws>\s+)`_index/candidates/(?P<rec>[^`]+)/REVIEW\.md`,")


def links(t):
    t = PKT.sub(lambda m: "ASTRA's packet [`%s`](../../_experiments/evidence/%s/README.md)%s(`%s`" % (
        m.group("slug"), m.group("slug"), m.group("ws"), m.group("sha")), t)
    t = EVI.sub(lambda m: "[`%s`](../../_experiments/evidence/%s/README.md)" % (m.group("slug"), m.group("slug")), t)
    t = REC.sub(lambda m: "%s([record](../../_index/candidates/%s/REVIEW.md)," % (m.group("ws"), m.group("rec")), t)
    return t


def edit(draft, name):
    d = io.open(os.path.join(CAND, draft, "consumption-draft.md"), encoding="utf-8").read().replace("\r\n", "\n")
    m = re.search(r"^## %s\b[^\n]*\n(.*?)(?=^## |\Z)" % re.escape(name), d, re.S | re.M)
    if not m:
        raise SystemExit("no %s in %s" % (name, draft))
    return re.findall(r"```\n(.*?)\n```", m.group(1), re.S)


def first_bullet_replaced(sec, bullet):
    lines = sec.split("\n")
    i = next(k for k, l in enumerate(lines) if l.startswith("- "))
    j = next(k for k in range(i + 1, len(lines)) if lines[k].startswith("- ") or not lines[k].startswith("  "))
    return "\n".join(lines[:i] + bullet.split("\n") + lines[j:])


def main():
    write = "--apply" in sys.argv
    fails = 0
    pages = {}
    for p in (AV, CA):
        raw = io.open(p, encoding="utf-8", newline="").read()
        pages[p] = ["\r\n" in raw, raw.replace("\r\n", "\n"), raw]

    def pair(p, tag, old, new):
        nonlocal fails
        t = pages[p][1]
        if new in t:
            print("ALREADY", tag); return
        if t.count(old) != 1:
            print("MISS %s (%d)" % (tag, t.count(old))); fails += 1; return
        pages[p][1] = t.replace(old, new); print("WOULD PATCH" if not write else "PATCHED", tag)

    def append(tag, sec):
        nonlocal fails
        sec = links(sec)
        if "](../../_experiments/evidence/" not in sec or "([record](../../_index/candidates/" not in sec:
            print("MISS %s (packet or record link not formed)" % tag); fails += 1; return
        t = pages[AV][1]
        if sec in t:
            print("ALREADY", tag); return
        pages[AV][1] = t.rstrip("\n") + "\n\n" + sec + "\n"
        print("WOULD APPEND" if not write else "APPENDED", tag)

    cr = R("caller-row-preconditions")
    for n in ("Edit 1", "Edit 2", "Edit 3"):
        b = edit(cr, n)
        assert len(b) == 2, (n, len(b))
        pair(AV, "caller-row " + n, b[0], b[1])
    b = edit(R("caller-quotient-bound"), "Edit 1"); assert len(b) == 1
    append("quotient-bound", b[0])
    b = edit(cr, "Edit 4"); assert len(b) == 2, len(b)
    append("caller-row Edit 4 (short first bullet)", first_bullet_replaced(b[0], b[1]))
    for p in ("terminal-resource-helper", "interpreter-transfer", "action-table-binding", "mode17-query-boundaries"):
        b = edit(R(p), "Edit 1"); assert len(b) == 1, (p, len(b))
        append(p, b[0])
    b = edit(R("mode17-query-boundaries"), "Edit 2"); assert len(b) == 2
    pair(CA, "mode17 Edit 2 (console slice A)", b[0], b[1])
    if write and not fails:
        for p, (crlf, t, raw) in pages.items():
            out = t.replace("\n", "\r\n") if crlf else t
            if out != raw:
                io.open(p, "w", encoding="utf-8", newline="").write(out)
    print("FAILS %d" % fails); sys.exit(1 if fails else 0)


main()
