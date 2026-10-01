#!/usr/bin/env python3
"""Census of the list-wait producers REQALL (0x5F), REQWAITALL (0x61) and REQIALL (0x63) across every
shipped EBP script, joined to the actor-list table each script carries at payload header +0x30.

Model (NATIVE/STATIC, FABLE 2026-09-24, read from the handlers 00261B15 / 00261CCD / 00261C12 and the
submitter 00268B10): the opcode's 16-bit operand indexes the table at payload + [payload+0x30]
({u32 count; u32 listOffset[count]}, offsets payload-relative); each list is
{u32 count; {u16 actorOrdinal; u16 functionId}[count]}. An operand >= count arms a NULL list
(the handler stores encode(0)) - the wait completes at once and the submitter returns without
submitting anything.

Control: the site counts must equal the REQ-family census (req-channel-census.tsv) for the three
opcodes, or the run refuses to report.
Outputs list-wait-census.tsv (one row per site) and prints the summary.
"""
import io, os, sys, struct, collections

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_req_channel_census as G           # decode(), the VBF reader set-up and paths

U32 = lambda b, o: struct.unpack_from("<I", b, o)[0]
U16 = lambda b, o: struct.unpack_from("<H", b, o)[0]
OPS = {0x5F: "REQALL", 0x61: "REQWAITALL", 0x63: "REQIALL"}
OUT = os.path.join(HERE, "list-wait-census.tsv")


def main():
    f = io.open(G.VBF, "rb")
    names, blocks = G.V.load_index(f)
    ebps = sorted(p for p in names if p.lower().endswith(".ebp"))
    rows, seen = [], set()
    tables = {}
    for path in ebps:
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
        t = U32(sec, 0x30)
        nlists = U32(sec, t) if 0 < t + 4 <= len(sec) else 0
        lists = []
        for i in range(nlists):
            lo = U32(sec, t + 4 + 4 * i)
            c = U32(sec, lo) if lo + 4 <= len(sec) else -1
            pairs = [(U16(sec, lo + 4 + 4 * k), U16(sec, lo + 6 + 4 * k)) for k in range(max(c, 0))
                     if lo + 8 + 4 * k <= len(sec)]
            lists.append(pairs)
        tables[path] = lists
        starts = sorted(U32(sec, diroff + 4 + s * 0x30 + 8) for s in range(cnt))
        bounds = sorted(set(starts) | {diroff, len(sec)})
        for si, start in enumerate(starts):
            end = min((x for x in bounds if x > start), default=len(sec))
            if start >= len(sec) or end <= start:
                continue
            ins, _ = G.decode(sec[start:end])
            for pc, op, imm in ins:
                if op not in OPS:
                    continue
                key = (path, start + pc)
                if key in seen:
                    continue
                seen.add(key)
                inr = imm < nlists
                pairs = lists[imm] if inr else []
                rows.append((path, si, "%x" % (start + pc), OPS[op], imm, nlists, int(inr), len(pairs),
                             ",".join("%d:%d" % p for p in pairs[:12])))
    with open(OUT, "w", newline="") as w:
        w.write("file\tscript\tpc\topname\tlist_index\tlists_in_script\tin_range\tlist_len\tpairs(ordinal:funcid, first 12)\n")
        for r in rows:
            w.write("\t".join(str(x) for x in r) + "\n")
    # control against the published census
    ref = collections.Counter()
    for line in open(os.path.join(HERE, "req-channel-census.tsv"), encoding="utf-8"):
        p = line.split("\t")
        if len(p) > 4 and p[4] in OPS.values():
            ref[p[4]] += 1
    got = collections.Counter(r[3] for r in rows)
    print("site counts:", dict(got), "reference:", dict(ref))
    if got != ref:
        sys.exit("REFUSE: control failed - site counts differ from req-channel-census.tsv")
    for op in OPS.values():
        rs = [r for r in rows if r[3] == op]
        out = [r for r in rs if not r[6]]
        lens = collections.Counter(r[7] for r in rs if r[6])
        print(f"{op}: {len(rs)} sites, out-of-range index {len(out)}, list length "
              f"min {min(lens) if lens else '-'} max {max(lens) if lens else '-'}, "
              f"top lengths {sorted(lens.items(), key=lambda kv: (-kv[1], kv[0]))[:6]}")
    allpairs = [p for ls in tables.values() for l in ls for p in l]
    print(f"scripts with a list table: {sum(1 for v in tables.values() if v)} of {len(tables)}; "
          f"lists {sum(len(v) for v in tables.values())}; pairs {len(allpairs)}; "
          f"max ordinal {max(p[0] for p in allpairs)}; function ids {min(p[1] for p in allpairs)}..{max(p[1] for p in allpairs)}")


if __name__ == "__main__":
    main()
