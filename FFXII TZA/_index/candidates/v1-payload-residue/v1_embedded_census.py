"""V-1 close-out: the all-routes census of v1_residue_census.py, run over the UNKNOWN spans INSIDE the embedded types.

Every UNKNOWN row of a type embedded in SavePayload (walked through embedded types and their arrays, each element at its
own absolute payload offset) becomes a residue span; the same seeds, walk and controls as v1_residue_census.py run over
them. Output: embedded_result.json beside this script. Expected on the certified exe: 378 spans / 1,935 B, exactly one
touched - PersistentFlagPayload +0x1534 (AA-8's saved music override) - before that row is split; after the split the
touched row is no longer UNKNOWN and the census reports 0 touched.
"""
import collections, json, pathlib, re, sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import v1_residue_census as V  # noqa: E402

F = HERE.parents[2] / "_types" / "fields.tsv"


def embedded_unknown():
    by = collections.defaultdict(list)
    for l in open(F, encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if len(c) >= 9 and c[0] != "type":
            by[c[0]].append(c)
    out = []

    def go(t, base, depth):
        for r in by[t]:
            o = int(r[1], 16); n = int(r[2]) if r[2].isdigit() else 0
            ct = r[4].split("[")[0].strip()
            if ct in by and ct != t and n > 0:
                m = re.search(r"\[(\d+)\]", r[4]); cnt = int(m.group(1)) if m else 1
                for k in range(cnt):
                    go(ct, base + o + k * (n // cnt), depth + 1)
                continue
            if r[7] == "UNKNOWN" and depth > 0:
                out.append((base + o, n, "%s.%s@%X" % (t, r[3], base + o)))
    go("SavePayload", 0, 0)
    return out


def main():
    V.RESIDUE = embedded_unknown()
    out_dir = HERE / "_embedded_run"
    out_dir.mkdir(exist_ok=True)
    V.HERE = out_dir
    V.main()
    r = json.loads((out_dir / "result.json").read_text(encoding="utf-8"))
    touched = {k: v for k, v in r["residue"].items() if v["offsets_touched"]}
    summary = {"spans": len(r["residue"]), "bytes": sum(v["bytes"] for v in r["residue"].values()),
               "touched": {k: v["offsets_touched"] for k, v in touched.items()}, "controls_pass": r["controls_pass"]}
    (HERE / "embedded_result.json").write_text(json.dumps(summary, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(summary, indent=1))


if __name__ == "__main__":
    main()
