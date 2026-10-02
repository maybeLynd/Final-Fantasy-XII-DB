"""script_verb_census.py - every call of chosen script verbs across the shipped .ebp scripts, with the calling script's
name (OPUS, 2026-09-30; generalised from _index/candidates/sd160-free-target-type3-0930/sd160_census.py).

  python -B script_verb_census.py --verbs 0x202,0x232,0x195 [--out calls.tsv]

Decoding is FABLE's (25-EBP-Script-Container/Bytecode-And-Opcodes/members/gen_req_channel_census.py): each script
function's bytecode is decoded and every CALL-family instruction (0x58/0x59/0x5D/0x5E) whose immediate is a chosen verb
is listed with its resolved push arguments. Script names come from the section's name pool at header +0x4C (directory
entry +0x00 is the name offset, +0x08 the code start; BW-5). The plan_master language copies are all visited; the
summary folds them into one zone file per language-independent path and reports whether the copies agree.

Refuses to write when no CALL-family instruction was decoded at all (a broken decoder would otherwise report zero).
"""
import argparse, collections, io, os, struct, sys

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.abspath(os.path.join(HERE, "..", "..", "..", "FFXII TZA"))
sys.path.insert(0, os.path.join(DB, "25-EBP-Script-Container", "Bytecode-And-Opcodes", "members"))
U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]


def census(want):
    cwd = os.getcwd()
    os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))
    try:
        import gen_req_channel_census as G
        verbs = G.load_verbs()
        f = io.open(G.VBF, "rb")
        names, blocks = G.V.load_index(f)
    finally:
        os.chdir(cwd)
    rows, seen, calls_total = [], set(), 0
    for path in sorted(p for p in names if p.lower().endswith(".ebp")):
        try:
            b = G.V.read_entry(f, names, blocks, path)
        except Exception:
            continue
        if len(b) < 0x80 or U32(b, 0x80) != 0x8000000B:
            continue
        sec = b[0x80:0x80 + U32(b, 0x84)]
        diroff = U32(sec, 0x18)
        cnt = U32(sec, diroff)
        if cnt > 0x400 or diroff + 4 + cnt * 0x30 > len(sec):
            continue
        pool = U32(sec, 0x4C)
        sname = {}
        for s in range(cnt):
            o = pool + U32(sec, diroff + 4 + s * 0x30)
            sname.setdefault(U32(sec, diroff + 4 + s * 0x30 + 8), sec[o:sec.find(b"\0", o)].decode("cp932", "replace"))
        starts = sorted(sname)
        bounds = sorted(set(starts) | {diroff, len(sec)})
        for start in starts:
            end = min((x for x in bounds if x > start), default=len(sec))
            if start >= len(sec) or end <= start:
                continue
            ins, _ = G.decode(sec[start:end])
            for j, (pc, op, imm) in enumerate(ins):
                if op not in (0x58, 0x59, 0x5D, 0x5E):
                    continue
                calls_total += 1
                if imm not in want:
                    continue
                key = (path, start + pc)
                if key in seen:
                    continue
                seen.add(key)
                v = verbs.get(imm)
                need = (v[0] if v and v[0] is not None else 0) + (1 if op in (0x59, 0x5E) else 0)
                args, st = G.resolve_args(ins, j, need, verbs) if need else ([], "ok")
                rows.append((path, sname[start], "%x" % (start + pc), "0x%03X" % imm, want[imm], G.OPN.get(op), st,
                             ";".join("%s:%s" % (a[0], a[1]) for a in args) if args else ""))
    return rows, calls_total


def fold(path):
    p = path.split("/")
    return ("/".join(p[:2] + p[3:]), p[2]) if len(p) > 3 and p[1] == "plan_master" else (path, "-")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbs", required=True, help="comma list of call ids, e.g. 0x202,0x232")
    ap.add_argument("--out")
    a = ap.parse_args()
    out = os.path.abspath(a.out) if a.out else None
    os.chdir(os.path.abspath(os.path.join(DB, "..", "..")))   # the decoder resolves its own imports from the repo root
    import gen_req_channel_census as G
    verbs_tab = G.load_verbs()
    want = {}
    for v in a.verbs.split(","):
        i = int(v, 0)
        want[i] = (verbs_tab.get(i) or (None, None, "?"))[2]
    rows, total = census(want)
    if total == 0:
        sys.exit("REFUSE: control failed - no CALL-family site decoded")
    print("CALL-family sites decoded: %d | matching calls: %d" % (total, len(rows)))
    for v, n in sorted(collections.Counter((r[3], r[4]) for r in rows).items()):
        print("  %5d  %s %s" % (n, v[0], v[1]))
    zones = collections.defaultdict(lambda: collections.defaultdict(collections.Counter))
    for r in rows:
        z, lang = fold(r[0])
        zones[z][lang][(r[1], r[3])] += 1
    agree = sum(1 for z in zones.values() if len(set(frozenset(c.items()) for c in z.values())) == 1)
    print("zone files: %d (language copies agree on (script, verb) in %d)" % (len(zones), agree))
    if out:
        with open(out, "w", encoding="utf-8", newline="\n") as w:
            w.write("file\tscript\tpc\tverb\tname\topcode\tstatus\targs_push_order\n")
            for r in rows:
                w.write("\t".join(r) + "\n")
    return rows


if __name__ == "__main__":
    main()
