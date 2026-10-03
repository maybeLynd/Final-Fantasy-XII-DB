"""check.py - the committed snapshot members/rtti-methods.tsv, minus its '#' provenance header, is byte-identical
(line endings normalised) to the gitignored Tools/work/rtti/methods.tsv that register rows AQ-2, BA-1, BQ-27 and B-3
were measured on. Prints both sha256 values, both line counts and SAME / DIFFERENT."""
import hashlib, io, os
HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", ".."))
snap = os.path.join(DB, "FFXII TZA", "00-Engine-Core-Runtime", "Object-Model", "members", "rtti-methods.tsv")
local = os.path.join(DB, "Tools", "work", "rtti", "methods.tsv")
a = [l for l in io.open(snap, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n") if not l.startswith("#")]
if not os.path.exists(local):
    print("local Tools/work/rtti/methods.tsv absent (gitignored); snapshot body rows:", len(a) - 1)
else:
    b = io.open(local, encoding="utf-8", newline="").read().replace("\r\n", "\n").split("\n")
    ha, hb = (hashlib.sha256("\n".join(x).encode("utf-8")).hexdigest() for x in (a, b))
    print("snapshot body sha256", ha, "lines", len(a))
    print("local methods sha256", hb, "lines", len(b))
    print("SAME" if a == b else "DIFFERENT")
