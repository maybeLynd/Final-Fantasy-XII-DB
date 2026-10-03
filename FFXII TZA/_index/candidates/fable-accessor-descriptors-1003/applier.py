"""applier.py [--apply] - append section.txt (FABLE's per-member descriptor rows) to phyre-script-object-accessors.md.
Before patching it re-checks every row at the bytes: the anchor is a `lea rdx,[rip+d]` inside the accessor's listed
extent whose target is the row's descriptor, and the row's accessor/type pair is the appendix's. Refuses while the
page has uncommitted changes, and when the section is already there. Prints FAILS N last."""
import io, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(DB, "_index", "candidates", "fable-review-astra-ov42-caller-quotient-bound-1002"))
from rvlib import Img  # noqa: E402
sys.path.insert(0, os.path.join(DB, "..", "Tools", "analysis-kit", "gfz-scripts"))
import check_dispositions as cd  # noqa: E402
P = os.path.join(DB, "22-Middleware-PhyreEngine", "Script-Object-Accessors", "phyre-script-object-accessors.md")
sec = io.open(os.path.join(HERE, "section.txt"), encoding="utf-8").read()
head = sec.splitlines()[0]
if subprocess.run(["git", "diff", "--quiet", "--", P], cwd=HERE).returncode != 0:
    print("REFUSED: the page has uncommitted changes"); print("FAILS 1"); sys.exit(1)
raw = io.open(P, encoding="utf-8", newline="").read()
if head in raw:
    print("ALREADY"); print("FAILS 0"); sys.exit(0)
app = raw[raw.index("## Appendix"):raw.index("## Audit pass 1")]
TYPE = dict(re.findall(r"`([0-9A-F]{8})` \| `([^`]+)`", app))
img = Img.load(); img.cs.detail = True
sizes = cd.load_functions()
rows = re.findall(r"^\| `([0-9A-F]{8})` \| `([^`]+)` \| requires class descriptor `([0-9A-F]{8})`[^|]*\| "
                  r"Interior anchor `([0-9A-F]{8})` \(`lea`, entry \+ 0x([0-9A-F]+)\)", sec, re.M)
fails = 0
for a, ty, X, an, off in rows:
    if int(an, 16) - int(a, 16) != int(off, 16):
        print("OFFSET %s: anchor %s is not entry + 0x%s" % (a, an, off)); fails += 1; continue
    f, x = int(a, 16), int(an, 16)
    if TYPE.get(a) != ty:
        print("TYPE %s: row %r, appendix %r" % (a, ty, TYPE.get(a))); fails += 1; continue
    if not (f < x < f + sizes.get(f, 0)):
        print("EXTENT %s: anchor %s not strictly inside" % (a, an)); fails += 1; continue
    i = next(img.cs.disasm(img.read(x, 16), x), None)
    if not i or i.mnemonic != "lea" or not i.op_str.startswith("rdx, [rip") \
            or i.address + i.size + i.operands[1].mem.disp != int(X, 16):
        print("ANCHOR %s: %s is not lea rdx,[rip->%s]" % (a, an, X)); fails += 1
n_table = len(re.findall(r"^\| `[0-9A-F]{8}` \|", sec, re.M))
if n_table != len(rows):
    print("PARSE: %d table rows, %d parsed" % (n_table, len(rows))); fails += 1
print("rows %d checked at the bytes" % len(rows))
if fails == 0 and "--apply" in sys.argv:
    nl = "\r\n" if "\r\n" in raw else "\n"
    body = sec.replace("\n", nl)
    io.open(P, "w", encoding="utf-8", newline="").write(raw.rstrip("\r\n") + nl + nl + body); print("PATCHED")
elif fails == 0:
    print("WOULD PATCH")
print("FAILS %d" % fails)
