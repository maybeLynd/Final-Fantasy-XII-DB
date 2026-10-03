"""controls.py - sensitivity controls for move_rows.py (FABLE, 2026-10-03; AUDIT-SPEC batch 6).

Each control mutates one entry of moves.json in a temporary copy and runs move_rows.py --moves on it (verify only,
nothing is written to the tree). Each must be refused (exit 1 with a VERIFY FAIL); the script exits 1 otherwise.
The first three are the host rule itself: the b5 rule (the address occurs on the page) passes each of them."""
import copy, json, os, subprocess, sys, tempfile

REC = os.path.dirname(os.path.abspath(__file__))
S = tempfile.mkdtemp(prefix="b6ctl_")
base = json.load(open(os.path.join(REC, "moves.json"), encoding="utf-8"))
MSGWIN = "16-UI/Message-Windows/the-message-window-layout-readers.md"
GAMEAPP = "00-Engine-Core-Runtime/Application-Root/game-application.md"


def mv(cfg, fn):
    return next(m for m in cfg["moves"] + cfg["edits"] + cfg["drops"] if m["fn"] == fn)


def as_move(c, fn, target):
    """turn a host_fails drop into a caller-host move to the page its review named"""
    d = mv(c, fn)
    c["drops"].remove(d)
    rows = json.load(open(os.path.join(REC, "..", "..", "..", *d["source_record"].split("/"), "rows.json"),
                          encoding="utf-8"))["rows"]
    r = next(x for x in rows if x["fn"] == fn)
    c["moves"].append({"fn": fn, "source_page": d["source_page"], "source_record": d["source_record"],
                       "source_section_date": d["source_section_date"], "review": d["review"],
                       "target_page": target, "entered_from": r["entered_from"], "source_text": r["text"],
                       "text": r["text"], "text_edit": None, "anchors": r["anchors"], "host": {"by": "caller"},
                       "evidence": []})


def c1(c):  # vbf 0028FF80 homed on the message-window page: 0035C630 is only inside the 002BDCE0 row's chain
    as_move(c, "0028FF80", MSGWIN)


def c2(c):  # lazy-statics 001D9F70 homed on game-application.md: 0017D940 is only inside the 001A07B0 paragraph
    as_move(c, "001D9F70", GAMEAPP)


def c3(c):  # 001D9F70 drop naming its own rejected host, where a pass-22 list item leads with 0017D940
    mv(c, "001D9F70")["host_fails"]["pages"][0]["page"] = \
        "24-Compiler-And-CRT-Runtime/Lazy-Static-Initialization/lazy-statics-and-the-one-time-init-lock.md"
    mv(c, "001D9F70")["host_fails"]["pages"][0]["quotes"] = []


def c4(c):  # thunk basis with a site that does not reach the thunk
    mv(c, "00408AD0")["host"]["thunk_callers"][1] = "`0026C8C0` + 0x191"


def c5(c):  # the 00623D70 narrowing striking text the row never said
    mv(c, "00623D70")["spans"][0][0] = "clears bit 31 of dword `rcx+0x1C`; when the result is above 1 (unsigned)"


def c6(c):  # the same narrowing with the wrong occurrence count for the `edx` span
    mv(c, "00623D70")["spans"][1][2] = 2


def c7(c):  # a moved row whose replacement wording is not the source text plus its text_edit
    mv(c, "00420860")["text"] = mv(c, "00420860")["text"].replace("xmm3", "xmm4")


def c8(c):  # the 0029D4D0 lea check pointed at the wrong address
    mv(c, "0029D4D0")["lea_checks"][0][1] = "0029D560"


def c9(c):  # a host_fails drop with one raw caller site missing
    mv(c, "004068B0")["host_fails"]["callers"]["004061F0"] = ["00406481"]


def c10(c):  # the efx section inserted before a heading the page does not have
    c["target_before"] = {k: "## 2z. " for k in c["target_before"]}


def c11(c):  # an anchor shifted by one byte
    mv(c, "004FE4A0")["anchors"][0][0] = "%08X" % (int(mv(c, "004FE4A0")["anchors"][0][0], 16) + 1)


CONTROLS = [("subject-chain-cell", c1), ("subject-passing-paragraph", c2), ("drop-names-a-documenting-page", c3),
            ("thunk-site-off", c4), ("strike-unsaid-text", c5), ("strike-count", c6), ("replace-not-derived", c7),
            ("lea-wrong-target", c8), ("drop-caller-site-missing", c9), ("insert-before-missing", c10),
            ("anchor-shift", c11)]
ONLY = sys.argv[1] if len(sys.argv) > 1 else ""
bad = 0
for name, f in CONTROLS:
    c = copy.deepcopy(base)
    f(c)
    p = os.path.join(S, "b6ctl_%s.json" % name)
    json.dump(c, open(p, "w", encoding="utf-8"), indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(REC, "move_rows.py"), "--moves", p],
                       capture_output=True, text=True)
    fl = [l for l in r.stdout.splitlines() if l.startswith("VERIFY FAIL")]
    ok = bool(r.returncode and fl)
    bad += not ok
    print("control %-30s exit %d, %d VERIFY FAIL: %s -> %s" % (
        name, r.returncode, len(fl), fl[0][12:120] if fl else "-", "refused" if ok else "NOT REFUSED"))
print("CONTROLS %d, NOT REFUSED %d" % (len(CONTROLS), bad))
sys.exit(1 if bad else 0)
