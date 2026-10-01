"""census_mutants.py - SWE2-AUDIT-SPEC (OV-31 review, 2026-09-29).

ov31_title_asset.py --self-test mutates S, P, J and X only. This fires the C/O/K census family with three wrong
expectations, each of which must make check_census() return False:
  CM1  cell-seed expectation missing the real site (0xC0,1,00393A98)
  CM2  own-seed expectation carrying an invented +0xC4 site (i.e. the claim "+0xC4 is accessed by the own handler")
  CM3  +0xC4 control demanding a site the sibling census does not report (00394999)
and the unmodified expectations must return True (CM0). Imports the package module unmodified.
"""
import contextlib, io, os, sys

PKG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "ov31-title-asset-type-store-0929")
sys.path.insert(0, os.path.abspath(PKG))
import ov31_title_asset as M  # noqa: E402

cases = [
    ("CM0 unmodified", (M.CELL_TYPE_AREA, M.OWN_TYPE_AREA, M.CONTROL_C4), True),
    ("CM1 cell set missing 00393A98", (M.CELL_TYPE_AREA - {(0xC0, 1, "00393A98")}, M.OWN_TYPE_AREA, M.CONTROL_C4), False),
    ("CM2 own set with invented +C4", (M.CELL_TYPE_AREA, M.OWN_TYPE_AREA | {(0xC4, 4, "003940E3")}, M.CONTROL_C4), False),
    ("CM3 control demands 00394999", (M.CELL_TYPE_AREA, M.OWN_TYPE_AREA, M.CONTROL_C4 | {"00394999"}), False),
]
ok_all = True
for tag, args, want in cases:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        got = M.check_census(*args)
    ok = got == want
    ok_all &= ok
    print("%-4s %-34s want %-5s got %-5s %s" % ("OK" if ok else "BAD", tag, want, got, buf.getvalue().strip().replace("\n", " | ")))
print("census mutants as expected:", ok_all)
sys.exit(0 if ok_all else 1)
