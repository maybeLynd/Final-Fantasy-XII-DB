"""rerun_sd182.py - SWE2-AUDIT-SPEC: re-run the package's sd182_nav_transform_pair.py unchanged, but with __file__ set
inside this review folder so its TSV side output (it writes sd182-subrecord-pairs.tsv next to itself) lands HERE and not
in the package folder. The package's img.py is imported from the package folder. The image hash is asserted first.
Run: python rerun_sd182.py > rerun_sd182_nav_transform_pair.out
"""
import hashlib, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.join(HERE, "..", "sd182-nav-transform-pair-0930")
EXE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", "Tools", "work", "exe", "FFXII_TZA.exe"))
assert hashlib.sha256(open(EXE, "rb").read()).hexdigest() == \
    "73461d0896204b1c259c52f61aef4efbc95a2ffc388cadb36493d5d1d89721f8"
sys.path.insert(0, os.path.abspath(PKG))
src = open(os.path.join(PKG, "sd182_nav_transform_pair.py"), encoding="utf-8").read()
g = {"__name__": "__main__", "__file__": os.path.join(HERE, "sd182_nav_transform_pair.py")}
exec(compile(src, "sd182_nav_transform_pair.py", "exec"), g)
