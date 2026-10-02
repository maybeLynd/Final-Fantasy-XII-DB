"""interior_applier.py [--apply] - interior citations for the F-frontier functions that PAGE cites only by entry.

Rows are in rows.json beside this file: drafted by a cloud session from OPUS's F-interior pack (cloud-input/f-interior/
in maybeLynd/Final-Fantasy-XII-DB), then checked by OPUS's interior_ingest.py (anchors, addresses) and every sentence
re-read by OPUS against the bytes before applying (see README.md for the session and the corrections).

Verifies every anchor in the certified image (instruction boundary strictly inside the function's extent, recorded
mnemonic) and refuses a pipe in any sentence. Without --apply it only verifies; with --apply it appends one OPUS
section (byte-preserving, CRLF-aware, idempotent). Prints VERIFY, PATCHED / ALREADY / DRY, FAILS n."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

CFG = json.load(open(os.path.join(HERE, "rows.json"), encoding="utf-8"))
P = os.path.join(DB, *CFG["page"].split("/"))
ROWS = [(r["fn"], r["text"], [tuple(a) for a in r["anchors"]]) for r in CFG["rows"]]
REC = os.path.basename(HERE)
DEPTH = "../" * CFG["page"].count("/")
HEAD = ("## Interior citations for the entry-cited functions (OPUS, %s, cloud-drafted)\n\n" % CFG["date"]
        + "*Functions this page named only at their entry. Each sentence states what the body does (access and "
        "representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session "
        "from OPUS's disassembly pack and re-read by OPUS against the certified image; verified by "
        "[`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its function and decodes to "
        "the recorded mnemonic.*\n\n" % (os.path.basename(__file__), DEPTH, REC, os.path.basename(__file__))
        + "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
for fn, text, anchors in ROWS:
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        print("VERIFY FAIL %s: not a function entry" % fn); fails += 1; continue
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            print("VERIFY FAIL %s: anchor %s outside the body" % (fn, a)); fails += 1
        elif ins.get(av) != mn:
            print("VERIFY FAIL %s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn)); fails += 1
    if "|" in text:
        print("VERIFY FAIL %s: pipe in text" % fn); fails += 1
print("VERIFY %d functions, %d anchors" % (len(ROWS), sum(len(r[2]) for r in ROWS)))
if not fails:
    body = HEAD + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, ", ".join("`%s`" % a for a, _m in anchors))
                          for fn, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if HEAD.splitlines()[0].encode("utf-8") in b:
        print("ALREADY")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply writes)")
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
