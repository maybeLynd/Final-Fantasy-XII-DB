"""apply_pass.py PAGE PASS_MD STATE_TAG [DATE] - stamp a falsification pass on a page: audit block (passes 1, last_pass, kind, state),
last_reviewed, and append the pass section from PASS_MD (its first line is the section heading, used as the idempotence key).
Handles the three audit-block shapes seen in the tree; refuses anything else. OPUS, 2026-09-29."""
import io, re, sys

page, pass_md, tag = sys.argv[1:4]
date = sys.argv[4] if len(sys.argv) > 4 else "2026-09-29"  # the pass date; older runners passed none
s = io.open(page, encoding="utf-8", newline="").read()
nl = "\r\n" if "\r\n" in s else "\n"
body = io.open(pass_md, encoding="utf-8").read().strip("\n")
head = body.split("\n", 1)[0]
# the closing fence is found by its own line ending: a mixed-EOL page can close its frontmatter with LF while holding
# CRLF elsewhere, and a CRLF-only search then misses the fence and cuts the body away (six-vfx, 2026-09-29)
fence = re.search(r"\r?\n---[ \t]*(?:\r?\n|$)", s[3:])
if not fence:
    raise SystemExit("REFUSED: no closing frontmatter fence in " + page)
end = fence.start() + 3
fm, rest = s[:end], s[end:]
orig = s
if "last_pass_state: " + tag not in fm:
    new = ("audit:%s  passes: 1%s  last_pass: %s%s  last_pass_kind: falsification%s  last_pass_state: %s%s" % (nl, nl, date, nl, nl, tag, nl))
    m = re.search(r"^audit:[ \t]*\r?\n((?:[ \t]+.*\r?\n)*)", fm + nl, re.M)
    if m:
        blk = m.group(1)
        keep = "".join(l for l in blk.splitlines(True) if not re.match(r"\s+(passes|last_pass|last_pass_state|last_pass_kind):", l))
        # keep every frontmatter key after the audit block (external_production, local_production_*, ...)
        fm = (fm + nl)[:m.start()] + new + keep + (fm + nl)[m.end():]
        fm = fm[:-len(nl)] if fm.endswith(nl) else fm
    else:
        fm = fm + nl + new.rstrip("\r\n")
    fm = re.sub(r"^last_reviewed: .*$", "last_reviewed: " + date, fm, count=1, flags=re.M)
s = fm + rest
if head not in s:
    s = s.rstrip("\r\n") + nl + nl + body.replace("\n", nl) + nl
# the page body after the frontmatter must survive whole, and only the audit block may shrink
if rest.rstrip("\r\n") not in s or len(s) < len(orig) - 400:
    raise SystemExit("REFUSED: the stamp would drop page content from " + page)
io.open(page, "w", encoding="utf-8", newline="").write(s)
print("ok")
