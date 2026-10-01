"""t2_compare.py RUNS_DIR - FABLE family ruling R1 test 2: each family's own selector re-run with the UC-1 bodies of its
span INCLUDED, compared with the committed (UC-1-excluding) run.  (SWE2-EC7, 2026-09-29)

RUNS_DIR holds, per family, <tag>.out.txt / <tag>.out/ (committed selector, output redirected) and <tag>.in.txt /
<tag>.in/ (same selector with its `uc1_band.frontier_starts()` exclusion replaced so the UC-1 bodies inside that
family's span are in its population; ../../../Tools/work/SWE2-EC7/r1/scratch_sel3.py, env UC1IN=LO:HI).
The test holds when the in-run exits 0 (every assertion the selector makes still holds), every control line the
selector prints is identical, and the in-run's members file = the out-run's + exactly the UC-1 bodies it admits.
"""
import io, os, re, sys, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", "Tools", "analysis-kit", "gfz-scripts"))
import uc1_band
R = sys.argv[1]
uc1 = uc1_band.frontier_starts()
FAM = [("PPFX", "ppfx", "ppfx-span.tsv", 0x6DA880, 0x7911E0),
       ("SEAD", "sead", "sead-library-span.tsv", 0x7A4380, 0x7F41A0),
       ("libvorbis", "vorbis", "libvorbis.tsv", 0x8800C0, 0x8958B0),
       ("libvpx", "vpx", "libvpx-vp8-decoder.tsv", 0x16DDD0, 0x17C890)]
def addrs(p):
    s = set()
    if os.path.exists(p):
        for l in io.open(p, encoding="utf-8"):
            l = l.split("#", 1)[0].strip()
            if l and re.fullmatch(r"[0-9A-Fa-f]{8}", l.split()[0]): s.add(int(l.split()[0], 16))
    return s
def controls(p):
    return [l.rstrip() for l in io.open(p, encoding="utf-8", errors="replace")
            if l.startswith(("control", "evidence", "DSP kernels")) ]
def findings(lines):
    """what a boundary control FINDS: the outside targets / zones it names (8- or 4-hex tokens), counts dropped.
    A control holds when no new outside target or zone appears; a count rising because a UC-1 body is now one more
    caller of an already-listed target is reported, not hidden."""
    return [(l.split(":")[0], frozenset(re.findall(r"'([0-9A-F,]{4,})'|\b([0-9A-F]{8})\(", l))) for l in lines]
for name, tag, mf, lo, hi in FAM:
    t_in, t_out = os.path.join(R, tag + ".in.txt"), os.path.join(R, tag + ".out.txt")
    txt_in = io.open(t_in, encoding="utf-8", errors="replace").read()
    failed = "Traceback" in txt_in or "AssertionError" in txt_in
    span_uc1 = {b for b in uc1 if lo <= b < hi}
    m_in, m_out = addrs(os.path.join(R, tag + ".in", mf)), addrs(os.path.join(R, tag + ".out", mf))
    add = m_in - m_out
    exact = controls(t_in) == controls(t_out)
    c_same = findings(controls(t_in)) == findings(controls(t_out))
    print("%-10s UC-1 in span %3d | in-run %s | members out %d -> in %d (+%d, of them UC-1 %d, other %d; dropped %d) | control findings identical: %s (lines byte-identical: %s)"
          % (name, len(span_uc1), "ASSERTION FAILED" if failed else "ok", len(m_out), len(m_in), len(add), len(add & span_uc1),
             len(add - span_uc1), len(m_out - m_in), c_same if not failed else "n/a (run stopped)", exact))
    if not exact and not failed:
        a, b = controls(t_out), controls(t_in)
        for x, y in zip(a, b):
            if x != y:
                cx = dict(re.findall(r"([0-9A-F]{8})\((\d+)\)", x)); cy = dict(re.findall(r"([0-9A-F]{8})\((\d+)\)", y))
                print("    count changes in '%s': %s" % (x.split(":")[0], {k: (cx.get(k), cy.get(k)) for k in set(cx) | set(cy) if cx.get(k) != cy.get(k)}))
    if failed:
        for l in txt_in.splitlines():
            if "joined by nothing" in l or "Error" in l:
                print("    " + l.strip()[:400])
    print("    TEST 2 %s" % ("FAILS" if failed or not c_same or (add - span_uc1) or (m_out - m_in) else "holds"))
