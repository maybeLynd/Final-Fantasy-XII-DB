"""ee_set.py - the functions engine_explained credits now, as progress.py measures them (OPUS, 2026-10-03).

progress.py prints counts only. This runs its own source unchanged except for one injected line after the
engine_explained count, which writes the credited set to ee_set.json beside this script, so a caller never
re-implements the rule (evidence-bearing page, interior or small-entry cite, the family-declaring-page rule, index-only
sections, the UC-1 phrase rule). Needed since FRONTIER's A-overlap family rule (1e64e4042): check_dispositions'
explained_set now holds accepted family members that engine_explained does not credit.
Import: ee_set.load(max_age_s) -> set of entry addresses (re-measures when the cache is older)."""
import io
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "analysis-kit", "gfz-scripts"))
OUT = os.path.join(HERE, "ee_set.json")
ANCHOR = 'comp["engine_explained"] = (len(explained), total_fn)'


def measure():
    src = io.open(os.path.join(KIT, "progress.py"), encoding="utf-8").read()
    assert src.count(ANCHOR) == 1, "progress.py changed: the engine_explained line is not there exactly once"
    inj = ANCHOR + "\n    import json as _j; _j.dump(sorted(explained), open(%r, 'w'))" % OUT
    src = src.replace(ANCHOR, inj)
    # the copy runs from this folder: its one __file__ use must still name the kit
    src = src.replace("_os.path.dirname(_os.path.abspath(__file__))", repr(KIT))
    tmp = os.path.join(HERE, "_progress_ee.py")
    io.open(tmp, "w", encoding="utf-8").write(src)
    try:
        r = subprocess.run([sys.executable, "-B", tmp], cwd=KIT, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=KIT))
        if not os.path.exists(OUT) or os.path.getmtime(OUT) < time.time() - 600:
            raise SystemExit("progress run did not write the set: %s" % (r.stderr[-800:]))
    finally:
        os.remove(tmp)


def load(max_age_s=1800):
    if not os.path.exists(OUT) or os.path.getmtime(OUT) < time.time() - max_age_s:
        measure()
    return set(json.load(open(OUT)))


if __name__ == "__main__":
    measure()
    print("engine_explained set:", len(load()))
