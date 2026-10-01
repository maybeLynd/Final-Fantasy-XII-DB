"""arc.py - shared archive + image helpers for ORACLE's RC-22..RC-34 records (ORACLE, 2026-09-30).
Reads files straight out of the shipped FFXII_TZA.vbf with agent_flow/tools/vbfextract.py (as in RC-5/RC-6) and
re-exports the image helpers of ../rc8-cascade-count-0930/img.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "rc8-cascade-count-0930"))
import img  # noqa: E402,F401
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "..", "agent_flow", "tools")))
import vbfextract  # noqa: E402
VBF = os.environ.get("FFXII_VBF") or r"D:\FFXII MP Mod\FFXII_TestClient1\FFXII_TZA.vbf"
_f = open(VBF, "rb")
NAMES, BLOCKS = vbfextract.load_index(_f)[:2]


def find(sub):
    s = sub.lower()
    return [n for n in NAMES if s in n.lower()]


def get(path):
    return vbfextract.read_entry(_f, NAMES, BLOCKS, path)
