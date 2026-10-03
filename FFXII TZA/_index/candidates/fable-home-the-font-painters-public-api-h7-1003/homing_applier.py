"""homing_applier.py [--apply] - homed frontier bodies for PAGE: functions no page cited, each called from a function
PAGE cites (FABLE homing stream H, 2026-10-03).

Rows are in rows.json beside this file: drafted by a cloud session from FABLE's homing pack (cloud-input/homing/ in
maybeLynd/Final-Fantasy-XII-DB), checked by FABLE's homing_ingest.py and every sentence re-read by FABLE against the
bytes before applying (README.md lists the session and the corrections).

Verifies, in the certified image: every anchor is an instruction boundary strictly inside its function with the
recorded mnemonic; every `entered_from` site is a direct call or jump to that function from inside the named caller;
the page cites that caller; no sentence has a pipe. Without --apply it only verifies; with --apply it appends one FABLE
section (byte-preserving, CRLF-aware, idempotent). Prints VERIFY, PATCHED / ALREADY / DRY, FAILS n."""
import json, os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.normpath(os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts")))
import check_dispositions as cd  # noqa: E402
import family_prover as fp  # noqa: E402
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

CFG = json.load(open(os.path.join(HERE, "rows.json"), encoding="utf-8"))
P = os.path.join(DB, *CFG["page"].split("/"))
ROWS = [(r["fn"], r["entered_from"], r["text"], [tuple(a) for a in r["anchors"]]) for r in CFG["rows"]]
REC = os.path.basename(HERE)
DEPTH = "../" * CFG["page"].count("/")
HEAD = ("## Homed frontier bodies called from this page's functions (FABLE, %s, cloud-drafted)\n\n" % CFG["date"]
        + "*Functions no page cited until now. Each is entered directly from a function this page already cites (the "
        "site is given as caller + offset). Each sentence states what the body does (access and representation, not "
        "purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's "
        "homing pack and re-read by FABLE against the certified image; verified by "
        "[`%s`](%s_index/candidates/%s/%s): every site transfers to its function, the page cites the caller, and every "
        "anchor is an instruction boundary inside its function that decodes to the recorded mnemonic.*\n\n"
        % (os.path.basename(__file__), DEPTH, REC, os.path.basename(__file__))
        + "| function | size | entered from | what the body does | interior anchors |\n|---|---|---|---|---|\n")
SITE = re.compile(r"`?([0-9A-F]{8})`?\s*\+\s*0x([0-9A-Fa-f]+)")
fails = 0
sizes = cd.load_functions()
d, off = fp.load_image()
md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = True
page_text = open(P, encoding="utf-8", errors="replace").read()
# 2026-10-03 (FABLE, on SWE2-AUDIT-SPEC's advisory): the caller must be a DOCUMENTED SUBJECT of the page - the first
# cell of a table row, an address in a heading, or the lead of a paragraph / list item - not a passing mention.
import re as _re
_SUBJ = [_re.compile(r"^\|\s*(?:\*\*)?\s*`?([0-9A-Fa-f]{8})`?"), _re.compile(r"^#{1,6} .*?`?([0-9A-Fa-f]{8})`?"),
         _re.compile(r"^\s*(?:[-*]\s+|\d+\.\s+)?(?:\*\*)?\s*`([0-9A-Fa-f]{8})`")]
SUBJECTS = set()
_prev = ""
for _ln in page_text.split("\n"):
    _p, _prev = _prev, _ln
    if "~~" in _ln[:40]:
        continue
    for _i, _rx in enumerate(_SUBJ):
        _m = _rx.match(_ln)
        # 2026-10-03: a plain (unmarked) lead must open a paragraph - a wrapped continuation line is not a lead.
        if _m and _i == 2 and not _re.match(r"^\s*(?:[-*]\s+|\d+\.\s+)", _ln) and _p.strip() and not _p.startswith("#"):
            continue
        if _m:
            SUBJECTS.add(_m.group(1).upper())
    if _ln.startswith("#"):
        SUBJECTS.update(x.upper() for x in _re.findall(r"`([0-9A-Fa-f]{8})`", _ln))
for fn, site, text, anchors in ROWS:
    f = int(fn, 16)
    n = sizes.get(f)
    if not n:
        print("VERIFY FAIL %s: not a function entry" % fn); fails += 1; continue
    m = SITE.fullmatch(site.strip())
    if not m:
        print("VERIFY FAIL %s: entered_from %r is not `caller` + 0xNN" % (fn, site)); fails += 1
    else:
        c, o = int(m.group(1), 16), int(m.group(2), 16)
        cn = sizes.get(c)
        ci = next(md.disasm(d[off(c + o):off(c + o) + 16], c + o), None) if cn and o < cn else None
        if not ci or ci.mnemonic not in ("call", "jmp") or not ci.operands or ci.operands[0].type != 2 \
                or ci.operands[0].imm != f:
            print("VERIFY FAIL %s: %s is not a direct call/jmp to it" % (fn, site)); fails += 1
        elif m.group(1).upper() not in SUBJECTS:
            print("VERIFY FAIL %s: the page does not document the caller %s as a subject (row, heading or lead)" % (fn, m.group(1))); fails += 1
    ins = {i.address: i.mnemonic for i in md.disasm(d[off(f):off(f) + n], f)}
    for a, mn in anchors:
        av = int(a, 16)
        if not (f < av < f + n):
            print("VERIFY FAIL %s: anchor %s outside the body" % (fn, a)); fails += 1
        elif ins.get(av) != mn:
            print("VERIFY FAIL %s: %s decodes to %r, recorded %r" % (fn, a, ins.get(av), mn)); fails += 1
    if "|" in text:
        print("VERIFY FAIL %s: pipe in text" % fn); fails += 1
print("VERIFY %d functions, %d anchors" % (len(ROWS), sum(len(r[3]) for r in ROWS)))
if not fails:
    body = HEAD + "".join("| `%s` | %d B | %s | %s | %s |\n" % (
        fn, sizes[int(fn, 16)], site.strip() if site.strip().startswith("`") else "`%s`" % site.strip(), text,
        "; ".join("Interior anchor `%s`" % a for a, _m in anchors)) for fn, site, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if not ROWS:
        # 2026-10-03 (FABLE, on SWE2-AUDIT-SPEC batch 5): a package whose rows were all held or rejected must not
        # append an empty section (the gambit-evaluation package did).
        print("NOTHING TO HOME (0 rows) - page untouched")
    elif all(("`%s`" % r[0]).encode("utf-8") in b for r in ROWS):
        print("ALREADY")
    elif HEAD.splitlines()[0].encode("utf-8") in b and "--apply" in sys.argv and \
            HEAD.splitlines()[0].replace("cloud-drafted)", "cloud-drafted, continued)").encode("utf-8") in b:
        print("VERIFY FAIL: both dated headings present but rows missing"); fails += 1
    elif HEAD.splitlines()[0].encode("utf-8") in b and "--apply" in sys.argv:
        # 2026-10-03: same page, same date, another record's section already there - append under a continued heading.
        s = s.replace(HEAD.splitlines()[0].encode("utf-8"),
                      HEAD.splitlines()[0].replace("cloud-drafted)", "cloud-drafted, continued)").encode("utf-8"), 1)
        nl = b"\r\n" if crlf else b"\n"
        open(P, "wb").write(b.rstrip(b"\r\n") + nl + nl + s)
        print("PATCHED (continued heading)")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply writes)")
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED")
print("FAILS", fails)
sys.exit(1 if fails else 0)
