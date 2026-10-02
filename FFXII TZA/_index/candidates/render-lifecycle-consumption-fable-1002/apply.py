"""apply.py [--apply] - consume three accepted render-lifecycle reviews into the character render record array page
(FABLE, 2026-10-02, ASTRA-REQ-FABLE-RENDER-CANONICAL-CONSUMPTION-1002). Three in-place qualifications of text that
over-states (each struck and tagged), and one new subsection 11a inserted before section 12. Every anchor must match
exactly once; any miss refuses the whole edit. Path resolved from this file."""
import io, os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "17-Presentation-Rendering",
                 "Character-Render-Records", "the-character-render-record-array.md")
TAG = "*(corrected 2026-10-02, FABLE, Claude Opus 5.5: see section 11a)*"
EDITS = [
    ("A record's `+0x00` is a 16-bit id which is `-1`\nwhen the slot is not in use, and every consumer tests that first.",
     "A record's `+0x00` is a 16-bit id which is `-1`\nwhen the slot is not in use~~, and every consumer tests that first~~; "
     "the id is not a validity test every consumer makes first - the list walks select by link, and the allocator "
     "publishes a new slot into the pending list before it writes the id " + TAG + "."),
    ("  +0x000  i16   id                 -1 when the slot is free; every consumer tests this first",
     "  +0x000  i16   id                 -1 when the slot is free (was 'every consumer tests this first' - corrected 2026-10-02, section 11a)"),
    ("| hands the record to `CharacterRenderRecord_ResetDefaults` | `00429291` → `0041F730` | same |",
     "| hands the record to `CharacterRenderRecord_ResetDefaults` | `00429291` → `0041F730` | ~~same~~ only through the "
     "per-record teardown called at `00427DAE`, which tail-jumps there " + TAG + " |"),
]
SECTION = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "section-11a.txt"), encoding="utf-8").read()
ANCHOR = "\n## 12. Extension 2026-09-11"
t = io.open(P, encoding="utf-8", newline="").read()
crlf = "\r\n" in t
u = t.replace("\r\n", "\n")
fails = 0
for old, new in EDITS:
    n = u.count(old)
    if n != 1:
        print("MISS (%d): %s" % (n, old[:80])); fails += 1
    else:
        u = u.replace(old, new)
if u.count(ANCHOR) != 1 or "### 11a. " in u:
    print("MISS: section 12 anchor not unique, or 11a already present"); fails += 1
else:
    u = u.replace(ANCHOR, "\n" + SECTION.rstrip("\n") + "\n" + ANCHOR, 1)
if fails:
    print("FAILS %d" % fails); sys.exit(1)
if "--apply" in sys.argv:
    io.open(P, "w", encoding="utf-8", newline="").write(u.replace("\n", "\r\n") if crlf else u); print("APPLIED")
else:
    print("DRY: 3 qualifications + section 11a")
print("FAILS 0")
