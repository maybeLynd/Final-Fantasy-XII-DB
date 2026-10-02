"""apply_batch.py GLOB [--skip SLUG ...] - run interior_ingest.py apply on every staged record matching GLOB (OPUS, 2026-10-02).

Records with 0 rows are skipped. Prints one line per record: QUEUED / NOT QUEUED / REFUSED, plus the gate dict.
Run only after the OPUS semantic re-read of every row (rows.json 'corrections'); never re-run `check` on re-read
records (it rewrites rows.json).
"""
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "FFXII TZA"))


def main():
    pat = sys.argv[1]
    skip = set(sys.argv[sys.argv.index("--skip") + 1:]) if "--skip" in sys.argv else set()
    for rj in sorted(glob.glob(os.path.join(DB, "_index", "candidates", pat, "rows.json"))):
        rec = os.path.basename(os.path.dirname(rj))
        if rec in skip:
            print(rec, "SKIP (asked)", flush=True)
            continue
        if not json.load(open(rj, encoding="utf-8"))["rows"]:
            print(rec, "SKIP (0 rows)", flush=True)
            continue
        o = subprocess.run([sys.executable, "-B", os.path.join(HERE, "interior_ingest.py"), "apply", rec],
                           capture_output=True, text=True, cwd=HERE).stdout
        keep = [l for l in o.splitlines() if l.startswith(("QUEUED", "NOT QUEUED", "REFUSED", "GATES", "FAILS"))]
        print(rec, "::", " | ".join(keep)[:400], flush=True)


if __name__ == "__main__":
    main()
