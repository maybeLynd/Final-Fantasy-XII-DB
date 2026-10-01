"""Generic read-side re-cut of a type's DISCOVERED spans from the flow-aware census (OPUS, 2026-09-27).

derive(rows, spans) returns, for every DISCOVERED span of the type the census resolves, the read-side layout:
  - the census's reads (width <= 8) inside the span tile it exactly, without overlap;
  - every other access that touches the span starts and ends on those boundaries (so a wider store is a pair / block
    store over whole fields) or is a 16-byte move;
  - each field's type comes from how it is read (movss family -> float, movsx / movsxd -> signed, else unsigned).
"""
import csv, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
def run_census(exe, fun, out, seeds):
    # clear every seed variable an outer environment might carry, then apply this type's seeds (a POOL seed used to
    # collide with the cleared default here - found 2026-09-27 on CharacterRenderRecord)
    env = {k: v for k, v in os.environ.items() if k not in ("POOL", "CELLS", "STATIC", "GETTERS", "ENTRIES", "TYPE_SIZE", "SHIFT", "ARRAYS")}
    env["POOL"] = "0"; env.update(seeds)
    subprocess.run([sys.executable, os.path.join(HERE, "type_flow_census.py"), exe, fun, out], env=env, check=True,
                   capture_output=True)
    return [r for r in csv.DictReader(open(out, encoding="latin1"), delimiter="\t")]


def spans_of(fields_path, typ, only_discovered=True):
    out = []
    for l in open(fields_path, encoding="utf-8"):
        c = l.rstrip("\r\n").split("\t")
        if c[0] == typ and (c[6] == "DISCOVERED" or not only_discovered):
            out.append((int(c[1], 16), int(c[2]), c))
    return out


def ctype(ins, w):
    m = ins.split()[0]
    if m.endswith("ss") or m in ("comiss", "ucomiss") or m.startswith("cvtss"): return "float"
    if m == "movsxd": return "int32"
    if m == "movsx": return {1: "int8", 2: "int16"}.get(w, "int%d" % (8 * w))
    return {1: "uint8", 2: "uint16", 4: "uint32", 8: "uint64"}[w]


def derive(rows, spans):
    acc_all = [(int(r["field"], 16), int(r["width"]), r["kind"], r["instruction"], r["site"]) for r in rows if r["kind"] != "addr"]
    out = []
    for o, n, cells in spans:
        acc = [a for a in acc_all if a[0] < o + n and a[0] + a[1] > o]
        reads = [a for a in acc if "r" in a[2] and a[1] <= 8 and o <= a[0] and a[0] + a[1] <= o + n]
        rl = sorted({(a[0], a[1]) for a in reads})
        if not rl: continue
        if any(x[0] < y[0] + y[1] and y[0] < x[0] + x[1] and x != y for x in rl for y in rl): continue
        if not (rl[0][0] == o and sum(w for f, w in rl) == n and all(rl[i][0] + rl[i][1] == rl[i + 1][0] for i in range(len(rl) - 1))): continue
        bounds = {f for f, w in rl} | {o + n}
        if any(a[1] != 16 and ((o <= a[0] < o + n and a[0] not in bounds) or (o < a[0] + a[1] <= o + n and a[0] + a[1] not in bounds)) for a in acc):
            continue
        fields = []
        for f, w in rl:
            ts = sorted({ctype(a[3], w) for a in reads if (a[0], a[1]) == (f, w)})
            t = ts[0] if len(ts) == 1 else next((x for x in ts if x.startswith("int")), ts[0])
            if len(ts) > 1 and not all(x.lstrip("u") == t.lstrip("u") for x in ts): break
            sites = sorted({a[4] for a in reads if (a[0], a[1]) == (f, w)})
            wider = sorted({a[4] for a in acc if a[1] > w and a[1] != 16 and a[0] <= f and f + w <= a[0] + a[1] and "w" in a[2]})
            fields.append((f, w, t, sites, wider))
        else:
            out.append((o, n, cells, fields))
    return out
