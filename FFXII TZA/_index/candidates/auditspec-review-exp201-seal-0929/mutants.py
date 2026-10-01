"""mutants.py - SWE2-AUDIT-SPEC independent falsification of exp201_receipts.py check (review of 8b269d9fa, 2026-09-29).

Each mutant copies the live input it perturbs to a temp dir, points the regression's module globals at the copy, runs
do_check() unmodified, and reports which rows flipped. Nothing under _experiments/ or the store is written.
A mutant is KILLED when the row that names its defect FAILs (and the run's FAILS count goes above 0).

  M0  baseline                                              -> FAILS 0
  M1  one byte flipped in the stored EXP-201 result         -> R-EXP-201-verify FAIL
  M2  result edited AND RECEIPT.json sha re-stamped to match -> seal.verify silent; R-EXP-201-hash must FAIL (pin)
  M3  one declared case dropped from RECEIPT.json cases      -> R-EXP-201-cases FAIL
  M4  record with the receipt id removed                     -> B-record FAIL
  M5  record with the cited result hash altered              -> B-record FAIL
  M6  contract: receipt id moved out of section 13j          -> B-contract-13j FAIL
  M7  live shared path restored to the EXP-201 bytes         -> P-live-moved FAIL (positive control is sensitive)
  M8  negative control fed the bound HEAD record             -> N-original-error-rejected FAIL (control can flip)
  M9  seal.py as of 475456436 (the package's own seal.py)    -> the three gate rows PEND, FAILS 0 (package-time claim)
"""
import contextlib, importlib.util, io, json, os, shutil, subprocess, sys, tempfile

REPO = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True,
                      cwd=os.path.dirname(os.path.abspath(__file__))).stdout.strip()
RC = os.path.join(REPO, "Database", "FFXII TZA", "_experiments", "evidence", "receipts")
GS = os.path.join(REPO, "Database", "Tools", "analysis-kit", "gfz-scripts")
R201 = "r-95260e713b7dba43"


def load_mod(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def fresh():
    sys.path.insert(0, GS)
    return load_mod("exp201_receipts_m", os.path.join(RC, "exp201_receipts.py"))


def run(m):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = m.do_check()
        except SystemExit as e:
            rc = "SystemExit(%s)" % e
        except Exception as e:  # a crash is fail-closed (non-zero exit) but prints no FAIL row
            rc = "CRASH %s" % type(e).__name__
            return rc, {"(crash)": "CRASH"}, rc
    out = buf.getvalue()
    rows = {}
    for ln in out.splitlines():
        p = ln.split()
        if len(p) >= 2 and p[0] in ("PASS", "FAIL", "PEND"):
            rows[p[1]] = p[0]
    last = [ln for ln in out.splitlines() if ln.startswith("FAILS")]
    return rc, rows, (last[0] if last else out.strip().splitlines()[-1:])


def copy_store(m, tmp):
    dst = os.path.join(tmp, "store")
    shutil.copytree(m.STORE, dst)
    m.STORE = dst
    return dst


def text_copy(tmp, rel, name, fn):
    src = os.path.join(REPO, rel)
    t = open(src, encoding="utf-8").read()
    t2 = fn(t)
    assert t2 != t, "mutant %s did not change the text" % name
    p = os.path.join(tmp, name)
    open(p, "w", encoding="utf-8", newline="").write(t2)
    return p


def main():
    base = fresh()
    RECORD, CONTRACT, EVID = base.RECORD, base.CONTRACT, base.EVID
    want201 = base.RUNS[0]["result_sha"]
    results = []

    def mutant(tag, expect_row, expect_state, setup):
        m = fresh()
        tmp = tempfile.mkdtemp(prefix="m201_")
        try:
            setup(m, tmp)
            rc, rows, last = run(m)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        got = rows.get(expect_row)
        ok = got == expect_state
        results.append((tag, expect_row, expect_state, got, last, ok))

    mutant("M0 baseline", "B-record", "PASS", lambda m, t: None)

    def digit_flip(p):
        """change one digit of a VALUE inside the JSON (stays valid JSON, same case ids): first ': <digit>'"""
        b = bytearray(open(p, "rb").read())
        i = next(k + 2 for k in range(200, len(b) - 2) if b[k] == 0x3A and b[k + 1] == 0x20 and 0x30 <= b[k + 2] <= 0x39)
        b[i] = 0x30 + ((b[i] - 0x30 + 1) % 10)
        open(p, "wb").write(bytes(b))

    def m1(m, t):
        d = copy_store(m, t)
        digit_flip(os.path.join(d, R201, "result"))
    mutant("M1 one digit changed in sealed result", "R-EXP-201-verify", "FAIL", m1)

    def m1b(m, t):
        d = copy_store(m, t)
        p = os.path.join(d, R201, "result")
        b = bytearray(open(p, "rb").read()); b[100] ^= 1
        open(p, "wb").write(bytes(b))
    mutant("M1b syntax-breaking byte in sealed result", "(crash)", "CRASH", m1b)

    def m2(m, t):
        d = copy_store(m, t)
        p = os.path.join(d, R201, "result")
        digit_flip(p)
        rp = os.path.join(d, R201, "RECEIPT.json")
        rec = json.load(open(rp, encoding="utf-8"))
        rec["result"]["sha256"] = m.SL.sha(p)
        json.dump(rec, open(rp, "w", encoding="utf-8"), indent=1, sort_keys=True)
        # the instrument-level fact: seal.verify alone is silent on a consistent re-stamp
        results.append(("M2a seal.verify on the re-stamped receipt", "(seal.verify problems)", "[]",
                        repr(m.SL.verify(d, R201)), "", m.SL.verify(d, R201) == []))
        pub = m.SL.publishable(d, R201)
        results.append(("M2b seal.publishable on the re-stamped receipt", "(publishable problems)", "[]",
                        repr(pub), "(the run id no longer derives from the content)", pub == []))
    mutant("M2 consistent re-stamp (result + RECEIPT sha)", "R-EXP-201-hash", "FAIL", m2)

    def m3(m, t):
        d = copy_store(m, t)
        rp = os.path.join(d, R201, "RECEIPT.json")
        rec = json.load(open(rp, encoding="utf-8"))
        rec["cases"] = rec["cases"][1:]
        json.dump(rec, open(rp, "w", encoding="utf-8"), indent=1, sort_keys=True)
    mutant("M3 one case dropped from RECEIPT cases", "R-EXP-201-cases", "FAIL", m3)

    def with_record(fn, name):
        def s(m, t):
            p = text_copy(t, RECORD, name, fn)
            m.RECORD = p  # os.path.join(REPO, abs) == abs; the negative control still reads git via the real path
            real_gb = m.git_bytes
            m.git_bytes = lambda spec, filters=True: real_gb(spec.replace(p, RECORD), filters)
        return s
    mutant("M4 record without receipt id", "B-record", "FAIL",
           with_record(lambda t: t.replace(R201, "r-0000000000000000"), "rec_m4.md"))
    mutant("M5 record with altered result hash", "B-record", "FAIL",
           with_record(lambda t: t.replace(want201, want201[:-1] + ("0" if want201[-1] != "0" else "1")), "rec_m5.md"))

    def m6(m, t):
        def fn(txt):
            head, sec = txt.split("### 13j.", 1)
            body, rest = (sec.split("\n### ", 1) + [""])[:2]
            body = body.replace(R201, "(receipt moved)")
            return head + "### 13j." + body + ("\n### " + rest if rest else "") + "\n<!-- " + R201 + " -->\n"
        m.CONTRACT = text_copy(t, CONTRACT, "con_m6.md", fn)
    mutant("M6 receipt id moved out of 13j", "B-contract-13j", "FAIL", m6)

    def m7(m, t):
        d = os.path.join(t, "evid") + os.sep
        os.makedirs(d)
        shutil.copyfile(os.path.join(m.STORE, R201, "result"), os.path.join(d, "result.json"))
        m.EVID = d
    mutant("M7 live path holds the EXP-201 bytes", "P-live-moved", "FAIL", m7)

    def m8(m, t):
        real_gb = m.git_bytes
        head_rec = open(os.path.join(REPO, RECORD), "rb").read()
        m.git_bytes = lambda spec, filters=True: head_rec if spec.endswith(RECORD) and not filters else real_gb(spec, filters)
    mutant("M8 negative control fed the bound record", "N-original-error-rejected", "FAIL", m8)

    def m9(m, t):
        old = subprocess.run(["git", "-C", REPO, "show", "475456436:Database/Tools/analysis-kit/gfz-scripts/seal.py"],
                             capture_output=True).stdout
        p = os.path.join(t, "seal_475456436.py")
        open(p, "wb").write(old)
        m.SL = load_mod("seal_old", p)
    mutant("M9 package-time seal.py (475456436)", "R-EXP-201-gate", "PEND", m9)

    killed = 0
    for tag, row, want, got, last, ok in results:
        killed += ok
        print("%-8s %-50s %-28s want %-4s got %-6s %s" % ("OK" if ok else "SURVIVED", tag, row, want, got, last))
    print("mutants as expected: %d of %d" % (killed, len(results)))
    return 0 if killed == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
