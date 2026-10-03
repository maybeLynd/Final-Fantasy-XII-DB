"""controls.py - sensitivity controls for move_rows.py (FABLE, 2026-10-03; AUDIT-SPEC batch 5).

Each control mutates one entry of moves.json in a temporary copy and runs move_rows.py --moves on it (verify only,
nothing is written to the tree). Each must be refused (exit 1 with a VERIFY FAIL); the script exits 1 otherwise."""
import copy, json, os, subprocess, sys, tempfile

REC = os.path.dirname(os.path.abspath(__file__))
S = tempfile.mkdtemp(prefix="b5ctl_")
base = json.load(open(os.path.join(REC, "moves.json"), encoding="utf-8"))


def mv(cfg, fn):
    return next(m for m in cfg["moves"] + cfg["adds"] + cfg["drops"] if m["fn"] == fn)


def c1(c):  # 004EB910 as a caller-host on VIF1: the page does not cite 004EBE80
    mv(c, "004EB910")["host"] = {"by": "caller"}


def c2(c):  # 004EB910 callee-host naming 0022CC20, which the VIF1 page does not cite
    mv(c, "004EB910")["host"]["callees"] = ["0022CC20"]


def c3(c):  # 00314D60 callee-host naming a function it does not call
    mv(c, "00314D60")["host"]["callees"] = ["00314D40"]


def c4(c):  # 001DD0B0 row-caller with the 0017FF20 add removed
    c["adds"] = []


def c5(c):  # 00361480 unbound with one raw caller missing from the record
    del mv(c, "00361480")["unbound"]["callers"]["00341C80"]


def c6(c):  # 00361480 unbound with the input-contract cite unlisted
    mv(c, "00361480")["unbound"]["cites"] = []


def c7(c):  # 0017FF20 anchor shifted by one byte
    mv(c, "0017FF20")["anchors"][0][0] = "0017FF25"


CONTROLS = [("caller-host-004EB910", c1), ("uncited-callee", c2), ("not-a-callee", c3),
            ("row-caller-missing", c4), ("unbound-caller-missing", c5), ("unbound-cite-unlisted", c6),
            ("anchor-shift", c7)]
bad = 0
for name, f in CONTROLS:
    c = copy.deepcopy(base)
    f(c)
    p = os.path.join(S, "b5ctl_%s.json" % name)
    json.dump(c, open(p, "w", encoding="utf-8"), indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(REC, "move_rows.py"), "--moves", p],
                       capture_output=True, text=True)
    fl = [l for l in r.stdout.splitlines() if l.startswith("VERIFY FAIL")]
    ok = bool(r.returncode and fl)
    bad += not ok
    print("control %-24s exit %d, %d VERIFY FAIL: %s -> %s" % (
        name, r.returncode, len(fl), fl[0][12:110] if fl else "-", "refused" if ok else "NOT REFUSED"))
print("CONTROLS %d, NOT REFUSED %d" % (len(CONTROLS), bad))
sys.exit(1 if bad else 0)
