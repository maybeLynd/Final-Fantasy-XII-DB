"""apply.py [--apply] - FABLE, 2026-10-03: home no-reference virtual methods on the page that documents their owning class.

Rows are in rows.json beside this file. Each body is one that no document cites and nothing calls directly; SWE2-EC7
handed it to FABLE (Database/Tools/work/SWE2-EC7/handoff_noref_to_fable_1003.tsv, rtti column) with its owning class and
vtable slot from rtti-methods.tsv. FABLE read every listing whole and wrote one sentence per body.

Checks, all before anything is written:
  1. the page is clean in git (`git status --short -- <page>` prints nothing);
  2. there is at least one row;
  3. every function is an entry in the certified function list, is not already cited on the page outside this block,
     and its sentence has no pipe and is under 1,200 characters;
  4. every anchor is an instruction boundary strictly inside its function and decodes to the recorded mnemonic
     (linear decode of the whole extent from the certified image);
  5. the page cites each row's owning-class token (the class name, or the PCaller template).
Without --apply it only verifies (DRY / ALREADY). With --apply it appends ONE section at the end of the page
(byte-preserving, CRLF kept, idempotent: an identical block prints ALREADY, a differing block is re-rendered).
Prints FAILS n as its last line and exits non-zero on any failure.
--test-copy FILE runs the same checks and writes against FILE (a copy of the page) instead of the page, skipping only the
git-clean check; it is how the CRLF handling and idempotency were exercised without touching the tracked page."""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64  # noqa: E402

CFG = json.load(open(os.path.join(HERE, "rows.json"), encoding="utf-8"))
REL = CFG["page"]
P = os.path.join(DB, *REL.split("/"))
TEST = sys.argv[sys.argv.index("--test-copy") + 1] if "--test-copy" in sys.argv else None
ROWS = CFG["rows"]
OWNERS = CFG.get("owner_tokens", {})
REC = os.path.basename(HERE)
ME = os.path.basename(__file__)
DEPTH = "../" * REL.count("/")
HEADING = "## No-reference bodies homed by owning class (FABLE, %s)" % CFG["date"]
NOTE = ("*No page cited these functions and nothing calls them directly: each is a virtual method, entered through its "
        "owning class's vtable, and this page documents that class. Each sentence states what the body does (access and "
        "representation, not purpose) and ends with the vtable slot and owning class from `rtti-methods.tsv`; the anchors "
        "are instructions inside the body that do it. %sHanded over by SWE2-EC7 and read whole by FABLE against the "
        "certified image; verified by [`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its "
        "function and decodes to the recorded mnemonic.*"
        % ((CFG.get("note_extra") + " ") if CFG.get("note_extra") else "", ME, DEPTH, REC, ME))

fails = 0


def fail(msg):
    global fails
    print("VERIFY FAIL " + msg)
    fails += 1


# 1. clean page
if TEST:
    print("TEST COPY %s (git-clean check skipped)" % TEST)
    P = TEST
else:
  try:
    st = subprocess.run(["git", "status", "--short", "--", P], cwd=DB, capture_output=True, text=True, check=True).stdout
  except Exception as e:  # noqa: BLE001
    st = None
    fail("git status failed: %s" % e)
  if st:
    fail("page is dirty in the working tree: %s" % st.strip())
if not os.path.exists(P):
    fail("page missing: %s" % REL)
    print("FAILS", fails)
    sys.exit(1)

raw = open(P, "rb").read()
crlf = b"\r\n" in raw[:4000]
text = raw.decode("utf-8")
cut = text.find(HEADING)
outside = text if cut < 0 else text[:cut]

# 2. rows
if not ROWS:
    fail("rows.json has zero rows")

sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
seen = set()
for r in ROWS:
    fn, t, anchors = r["fn"], r["text"], r["anchors"]
    f = int(fn, 16)
    n = sizes.get(f)
    if fn in seen:
        fail("%s: duplicate row" % fn)
    seen.add(fn)
    if not n:
        fail("%s: not a function entry" % fn)
        continue
    if "|" in t:
        fail("%s: pipe in text" % fn)
    if not t.strip() or len(t) >= 1200:
        fail("%s: text length %d" % (fn, len(t)))
    if not (1 <= len(anchors) <= 5):
        fail("%s: %d anchors (want 1-5)" % (fn, len(anchors)))
    if re.search(r"`%s`" % fn, outside):
        fail("%s: already cited on the page outside this block" % fn)
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            fail("%s: anchor %s outside the body (or at its entry)" % (fn, a))
        elif ins.get(av) != mn:
            fail("%s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn))
    tok = OWNERS.get(fn)
    if not tok:
        fail("%s: no owner token" % fn)
    elif tok not in outside:
        fail("%s: page does not cite %s" % (fn, tok))
print("VERIFY %d functions, %d anchors, page %s (%s)" % (len(ROWS), sum(len(r["anchors"]) for r in ROWS), REL,
                                                        "CRLF" if crlf else "LF"))

if not fails:
    body = (HEADING + "\n\n" + NOTE + "\n\n| function | size | what the body does | interior anchors |\n|---|---|---|---|\n"
            + "".join("| `%s` | %d B | %s | %s |\n" % (r["fn"], sizes[int(r["fn"], 16)], r["text"],
                                                       "; ".join("Interior anchor `%s`" % a for a, _m in r["anchors"]))
                      for r in ROWS))
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    key = HEADING.encode("utf-8")
    if key in raw:
        i = raw.index(key)
        old = raw[i:]
        if old.rstrip(b"\r\n") == s.rstrip(b"\r\n"):
            print("ALREADY")
        elif raw.count(key) != 1 or not old.rstrip(b"\r\n").endswith(b"|"):
            fail("existing block is not the last section of the page; refusing to re-render")
        elif "--apply" not in sys.argv:
            print("DRY (block differs from rows.json; --apply re-renders it)")
        else:
            open(P, "wb").write(raw[:i] + s)
            print("REWRITTEN")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply appends %d rows)" % len(ROWS))
    else:
        nl = b"\r\n" if crlf else b"\n"
        open(P, "wb").write(raw.rstrip(b"\r\n") + nl + nl + s)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
