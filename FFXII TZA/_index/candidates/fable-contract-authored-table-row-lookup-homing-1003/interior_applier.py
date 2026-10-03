"""interior_applier.py [--apply] - interior citations for the F-frontier functions that PAGE cites only by entry.

Rows are in rows.json beside this file: drafted by a cloud session from FABLE's F-interior pack (cloud-input/f-interior/
in maybeLynd/Final-Fantasy-XII-DB), then checked by FABLE's fable_ingest.py (anchors, addresses) and every sentence
re-read by FABLE against the bytes before applying (see README.md for the session and the corrections).

Verifies every anchor in the certified image (instruction boundary strictly inside the function's extent, recorded
mnemonic) and refuses a pipe in any sentence. Without --apply it only verifies; with --apply it appends one FABLE
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
HEAD = ("## Interior citations for the entry-cited functions (FABLE, %s, cloud-drafted)\n\n" % CFG["date"]
        + "*Functions this page named only at their entry. Each sentence states what the body does (access and "
        "representation, not purpose), and the anchors are instructions inside it that do it. Drafted by a cloud session "
        "from FABLE's disassembly pack and re-read by FABLE against the certified image; verified by "
        "[`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its function and decodes to "
        "the recorded mnemonic.*\n\n" % (os.path.basename(__file__), DEPTH, REC, os.path.basename(__file__))
        + "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
if CFG.get("mode") == "homing":
    # F homing (OPUS, 2026-10-03): bodies no page cited, reached only indirectly, homed on a page that cites a callee.
    HEAD = ("## Homed bodies: functions reached only indirectly whose callees this page cites (FABLE, %s, F homing)\n\n" % CFG["date"]
            + "*No page cited these functions and none of their callers is documented: they are reached by table or pointer "
            "dispatch or through undocumented callers. Each one calls something this page documents, which the sentence names. Each sentence states what the body does (access and "
            "representation, not purpose); the anchors are instructions inside it that do it. Drafted by a cloud session from FABLE's F homing pack and re-read "
            "by FABLE against the certified image; verified by [`%s`](%s_index/candidates/%s/%s): every anchor is an "
            "instruction boundary inside its function and decodes to the recorded mnemonic.*\n\n"
            % (os.path.basename(__file__), DEPTH, REC, os.path.basename(__file__))
            + "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
if CFG.get("mode") == "member":
    # family members (OPUS, 2026-10-03): one block per family part; the heading names the family and the record
    HEAD = ("## Family members explained one by one: %s (OPUS, %s, %s)\n\n" % (CFG.get("family", ""), CFG["date"], REC)
            + "*Members of the family `%s`, which this page declares, that no page explained. Each sentence states what "
            "the body does (access and representation, not purpose), and the anchors are instructions inside it that do "
            "it. Drafted locally from OPUS's pack and re-read by OPUS against the certified image; verified by "
            "[`%s`](%s_index/candidates/%s/%s): every anchor is an instruction boundary inside its function and decodes "
            "to the recorded mnemonic.*\n\n" % (CFG.get("family", ""), os.path.basename(__file__), DEPTH, REC,
                                                  os.path.basename(__file__))
            + "| function | size | what the body does | interior anchors |\n|---|---|---|---|\n")
if CFG.get("mode") == "uc1":
    # UC-1 game-code bodies (OPUS, 2026-10-03; FABLE's route ruling fable-uc1-gamecode-route-ruling-1003, test 3: the
    # count of such rows is stated once in the heading; each row carries the series-break phrase).
    HEAD = ("## %d UC-1 game-code bodies explained by interior citation (OPUS, %s)\n\n" % (len(ROWS), CFG["date"])
            + "*These %d bodies were admitted to the F frontier on 2026-09-28 by the UC-1 band (decoded code the function "
            "list never had) and are reached from game code, so no library span can take them. Under FABLE's route ruling "
            "each is explained by an interior citation instead: the row first states how the body is entered (a call or "
            "jump site, or no reference found and what the start follows), then what the body does (access and "
            "representation, not purpose), and ends with the series-break phrase. Drafted by an agent that is not OPUS and "
            "re-read by OPUS against the certified image; verified by [`%s`](%s_index/candidates/%s/%s): every anchor is "
            "an instruction boundary inside its body and decodes to the recorded mnemonic.*\n\n"
            % (len(ROWS), os.path.basename(__file__), DEPTH, REC, os.path.basename(__file__))
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
    body = HEAD + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, "; ".join("Interior anchor `%s`" % a for a, _m in anchors))
                          for fn, text, anchors in ROWS)
    b = open(P, "rb").read()
    crlf = b"\r\n" in b[:4000]
    # 2026-10-03 (OPUS): a block belongs to the record its lead links (`_index/candidates/<REC>/`), not to whoever
    # matches its heading. Two records of one mode and date render the same heading; the second record used to take the
    # first record's block and re-render it with its own rows (890844135, 33eb7192f, e63502b10: 55 published rows
    # deleted). Now: re-render only a block this record owns, never drop a row that is not this record's, and when
    # another record holds the heading append a block whose heading names this record.
    OWN = ("/_index/candidates/%s/" % REC).encode("utf-8")
    h0 = HEAD.splitlines()[0]
    ALT_H0 = h0[:-1] + ", " + REC + ")" if h0.endswith(")") and REC not in h0 else h0
    # the uc1 heading carries the row count, so find the block by its count-free tail (2026-10-03)
    keys = []
    for k0 in (h0, ALT_H0):
        kk = (k0.split(" ", 2)[2] if CFG.get("mode") == "uc1" else k0).encode("utf-8")
        if kk not in keys:
            keys.append(kk)

    def blocks(buf):
        """(start, end line index, lines) of every block whose heading matches a key."""
        out, pos = [], 0
        while True:
            hits = [(buf.find(kk, pos), kk) for kk in keys]
            hits = [h for h in hits if h[0] >= 0]
            if not hits:
                return out
            j, kk = min(hits)
            i = buf.rfind(b"\n", 0, j) + 1
            lines = buf[i:].split(b"\n")
            k, seen = 0, False
            for k, l in enumerate(lines):
                if l.startswith(b"| `"):
                    seen = True
                elif seen and not l.startswith(b"|"):
                    break
            else:
                k = len(lines)
            out.append((i, k, lines))
            pos = j + len(kk)

    found = blocks(b)
    owned = [x for x in found if OWN in b"\n".join(x[2][:x[1]])]
    # keep the heading form the owned block already has; a new block takes the shared heading only when it is free
    if owned:
        alt = ALT_H0 != h0 and REC.encode("utf-8") in owned[0][2][0]
    else:
        alt = bool(found)
    head_text = HEAD.replace(h0, ALT_H0, 1) if alt else HEAD
    body = head_text + "".join("| `%s` | %d B | %s | %s |\n" % (fn, sizes[int(fn, 16)], text, "; ".join("Interior anchor `%s`" % a for a, _m in anchors))
                               for fn, text, anchors in ROWS)
    s = body.encode("utf-8")
    if crlf:
        s = s.replace(b"\n", b"\r\n")
    if len(owned) > 1:
        print("REFUSED: %d blocks on the page link this record; resolve by hand" % len(owned)); fails += 1
    elif owned:
        # 2026-10-02 (OPUS): a rows.json corrected after a first apply used to stay ALREADY with the stale rows on the
        # page. Re-render the block (heading through its last table row) when it differs.
        i, k, lines = owned[0]
        old = b"\n".join(lines[:k])
        new = s.rstrip(b"\r\n")
        import re as _re
        mine = {fn.upper() for fn, _t, _a in ROWS}
        lost = sorted({m.decode().upper() for m in _re.findall(rb"^\| ~*`([0-9A-Fa-f]{8})`", old, _re.M)} - mine)
        if old.rstrip(b"\r") == new.rstrip(b"\r"):
            print("ALREADY")
        elif lost:
            print("REFUSED: re-rendering would drop %d row(s) not in this record's rows.json: %s" % (len(lost), ", ".join(lost)))
            fails += 1
        elif "--apply" not in sys.argv:
            print("DRY (block differs from rows.json; --apply rewrites it)")
        else:
            open(P, "wb").write(b[:i] + new + (b"\r" if old.endswith(b"\r") and not new.endswith(b"\r") else b"") +
                                b"\n".join([b""] + lines[k:]) if k < len(lines) else b[:i] + new + (b"\r\n" if crlf else b"\n"))
            print("REWRITTEN")
    elif "--apply" not in sys.argv:
        print("DRY (verified; --apply writes%s)" % (" a block headed for this record: another record holds the heading" if found else ""))
    else:
        nl = b"\r\n" if crlf else b"\n"
        b = b.rstrip(b"\r\n") + nl + nl + s
        open(P, "wb").write(b)
        print("PATCHED" + (" (own heading: another record holds the shared one)" if found else ""))
print("FAILS", fails)
sys.exit(1 if fails else 0)
