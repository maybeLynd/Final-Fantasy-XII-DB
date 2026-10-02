"""apply.py [--apply] - insert section 5a (the cache insertion takes a ready-made 32-bit key) into the path-resolution
page, before section 6 (FABLE, 2026-10-02, ASTRA-REQ-FABLE-FILECACHE-INSERT-KEY-ADMISSION-1002). Refuses if the
anchor is not unique or 5a is already present. Path resolved from this file."""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "..", "..", "..", "02-Resource-And-Asset-Pipeline", "VBF-Archive-And-Authored-Tables",
                 "how-a-path-is-resolved-to-bytes.md")
SECTION = io.open(os.path.join(HERE, "section-5a.txt"), encoding="utf-8").read().rstrip("\n")
ANCHOR = "\n## 6. Route 2"
t = io.open(P, encoding="utf-8", newline="").read(); crlf = "\r\n" in t; u = t.replace("\r\n", "\n")
if u.count(ANCHOR) != 1 or "### 5a. " in u:
    print("MISS: section 6 anchor not unique, or 5a already present"); print("FAILS 1"); sys.exit(1)
u = u.replace(ANCHOR, "\n" + SECTION + "\n" + ANCHOR, 1)
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8", newline="").write(u.replace("\n", "\r\n") if crlf else u); print("APPLIED")
else:
    print("DRY: section 5a before section 6")
print("FAILS 0")
